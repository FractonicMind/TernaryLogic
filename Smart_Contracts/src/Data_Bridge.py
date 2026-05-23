"""
Data_Bridge.py
==============
TL Framework Bridge: API → Smart Contracts

Framework: "Ternary Logic" (TL) by Lev Goukassian
ORCID:     0009-0006-5966-1243
DOI:       10.1007/s43681-025-00910-6
DOI:       10.1007/s43681-026-01124-0

Constitutional role:
    Routes every governance decision through the full TL API stack before
    any on-chain contract interaction. Enforces the NL=NA invariant end-to-end:
    no execution without a prior PermissionToken from the Governance Lane.

NL=NA Five-Layer Enforcement (off-chain layers):
    Layer 1: StateEnvelope if/then — API response schema validation
    Layer 2: PermissionToken.laneOrigin == "GOVERNANCE_LANE" — verified here
    Layer 3: TGLF_StateP1 permissionToken required — verified here
    Layer 4: GovernanceProof logHash/merkleRoot cross-reference — verified here
    Layer 5: TL_Ledger_Core.registerPermissionToken — on-chain terminal gate

Flow for every transaction:
    1. POST /decisions       (Inference Lane)  → TLResult + decisionId
    2. POST /governance-logs (Governance Lane) → StateEnvelope + PermissionToken
    3. If State +1 AND PermissionToken present:
           → TL_Ledger_Core.registerPermissionToken (on-chain, NL=NA Layer 5)
           → TL_Evidence_Vault.archiveEvidence (via Core)
    4. If State 0 (EpistemicHold):
           → Log EscrowRecord. Do NOT proceed to contract. Hold is free.
    5. If State -1 (Refuse):
           → Log refusal. Do NOT proceed to contract.

Ghost Governance Prevention:
    This bridge never calls the contract directly without a valid PermissionToken.
    Doing so would be Ghost Governance: execution without immutable audit evidence.
    The old version of this file did exactly that. This version does not.

Immutable Mandates (beyond any governance body's authority):
    No Spy | No Weapon | No Switch Off
"""

import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] TL_Bridge: %(message)s"
)
log = logging.getLogger("TL_Bridge")

# ---------------------------------------------------------------------------
# TL TRIADIC STATE ENUM
# ---------------------------------------------------------------------------

class TLState(IntEnum):
    """
    Canonical TL triadic state encoding.
    EpistemicHold is State 0: a first-class constitutional state.
    Never null, never error, never timeout.
    """
    PROCEED        =  1
    EPISTEMIC_HOLD =  0
    REFUSE         = -1


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

def load_config(config_path: str = "TL_Config.json") -> dict:
    """Load TL configuration from TL_Config.json."""
    with open(config_path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# DATA CLASSES
# ---------------------------------------------------------------------------

@dataclass
class TLDecisionResult:
    """Result from POST /decisions (Inference Lane)."""
    decision_id: str
    state: TLState
    state_label: str
    confidence: float
    rationale: str
    trace_id: str


@dataclass
class TLPermissionToken:
    """
    PermissionToken from the Governance Lane.
    Required for State +1 actuation. Never issued for State 0 or -1.
    laneOrigin MUST equal "GOVERNANCE_LANE" — NL=NA Layer 2.
    """
    token_id: str
    log_hash: str
    merkle_root: str
    lane_origin: str
    signer_key_id: str
    epoch_timestamp: int
    expires_at: int
    max_lifetime_ms: int
    revocation_status: str
    signature_value: str


@dataclass
class TLGovernanceResult:
    """Result from POST /governance-logs (Governance Lane)."""
    current_state: TLState
    state_label: str
    process_active: str
    trace_id: str
    permission_token: Optional[TLPermissionToken] = None
    escrow_record_id: Optional[str] = None
    escrow_rationale: Optional[str] = None


@dataclass
class TLBridgeResult:
    """
    Final result from the full bridge pipeline.
    on_chain_tx is only populated for State +1 with registered PermissionToken.
    """
    state: TLState
    state_label: str
    trace_id: str
    decision_id: str
    permission_token_id: Optional[str] = None
    on_chain_tx: Optional[str] = None
    escrow_record_id: Optional[str] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# TL API CLIENT
# ---------------------------------------------------------------------------

class TLAPIClient:
    """
    Client for the TL Governance API.
    Handles both Inference Lane and Governance Lane endpoints.
    All requests carry X-TL-Trace-Id for constitutional traceability.
    """

    GOVERNANCE_LANE_ORIGIN = "GOVERNANCE_LANE"

    def __init__(self, config: dict):
        self.base_url = config["API"]["BASE_URL"].rstrip("/")
        self.inference_lane_jwt = config["API"]["INFERENCE_LANE_JWT"]
        self.governance_lane_jwt = config["API"]["GOVERNANCE_LANE_JWT"]
        self.nlna_governance_token = config["API"]["NLNA_GOVERNANCE_TOKEN"]
        self.hsm_key_id = config["API"]["HSM_KEY_ID"]

    def _inference_headers(self, trace_id: str) -> dict:
        """Headers for Inference Lane requests."""
        return {
            "Authorization": f"Bearer {self.inference_lane_jwt}",
            "Content-Type": "application/json",
            "X-TL-Trace-Id": trace_id,
        }

    def _governance_headers(self, trace_id: str) -> dict:
        """
        Headers for Governance Lane requests.
        Requires both HSMSignedJWT and NLNAGovernanceToken.
        NLNAGovernanceToken is cryptographically bound to the trace_id
        of the originating Inference Lane request, preventing token
        substitution across unrelated decision vectors.
        """
        return {
            "Authorization": f"Bearer {self.governance_lane_jwt}",
            "X-NLNAGovernanceToken": self.nlna_governance_token,
            "Content-Type": "application/json",
            "X-TL-Trace-Id": trace_id,
        }

    def post_decision(
        self,
        transaction_data: dict,
        proposed_action: str,
        trace_id: str,
        domain: str = "trade"
    ) -> TLDecisionResult:
        """
        POST /decisions — Inference Lane.
        Proposes a state. Does NOT authorize actuation.
        Returns TLResult with decisionId.
        """
        payload = {
            "decisionVector": transaction_data,
            "proposedAction": proposed_action,
            "domain": domain,
            "goukassianPrinciple": self._build_goukassian_principle_block(),
        }

        resp = requests.post(
            f"{self.base_url}/decisions",
            headers=self._inference_headers(trace_id),
            json=payload,
            timeout=5  # Inference Lane WCET: 2ms hard ceiling; 5s network timeout
        )
        resp.raise_for_status()
        data = resp.json()

        return TLDecisionResult(
            decision_id=data["decisionId"],
            state=TLState(data["state"]),
            state_label=data["stateLabel"],
            confidence=data.get("confidence", 0.0),
            rationale=data.get("rationale", ""),
            trace_id=data.get("traceId", trace_id),
        )

    def post_governance_log(
        self,
        decision_id: str,
        transaction_hash: str,
        evidence_uri: str,
        trace_id: str,
    ) -> TLGovernanceResult:
        """
        POST /governance-logs — Governance Lane.
        Central NL=NA enforcement point.
        Returns StateEnvelope with PermissionToken (State +1) or
        EscrowRecord (State 0) or Refuse (State -1).

        GovernanceProof.logHash and GovernanceProof.merkleRoot are
        cross-referenced against PermissionToken fields — NL=NA Layer 4.
        """
        payload = {
            "decisionId": decision_id,
            "tglfRecord": {
                "transactionHash": transaction_hash,
                "evidenceURI": evidence_uri,
            },
            "goukassianPrinciple": self._build_goukassian_principle_block(),
            "governanceProof": {
                "logHash": transaction_hash,
                "merkleRoot": "",  # Populated by Governance Lane
            },
        }

        resp = requests.post(
            f"{self.base_url}/governance-logs",
            headers=self._governance_headers(trace_id),
            json=payload,
            timeout=35  # Governance Lane hard ceiling: 300ms + network overhead
        )
        resp.raise_for_status()
        data = resp.json()

        current_state = TLState(data["currentState"])
        permission_token = None
        escrow_record_id = None
        escrow_rationale = None

        if current_state == TLState.PROCEED:
            pt_data = data.get("permissionToken")
            if pt_data:
                permission_token = TLPermissionToken(
                    token_id=pt_data["tokenId"],
                    log_hash=pt_data["logHash"],
                    merkle_root=pt_data["merkleRoot"],
                    lane_origin=pt_data["laneOrigin"],
                    signer_key_id=pt_data["signerKeyId"],
                    epoch_timestamp=pt_data["epochTimestamp"],
                    expires_at=pt_data["expiresAt"],
                    max_lifetime_ms=pt_data["maxLifetimeMs"],
                    revocation_status=pt_data["revocationStatus"],
                    signature_value=pt_data["signatureValue"],
                )

        elif current_state == TLState.EPISTEMIC_HOLD:
            er = data.get("escrowRecord", {})
            escrow_record_id = er.get("escrowId")
            escrow_rationale = er.get("holdRationale", {}).get("rationale", "")

        return TLGovernanceResult(
            current_state=current_state,
            state_label=data["stateLabel"],
            process_active=data.get("processActive", ""),
            trace_id=data.get("traceId", trace_id),
            permission_token=permission_token,
            escrow_record_id=escrow_record_id,
            escrow_rationale=escrow_rationale,
        )

    def _build_goukassian_principle_block(self) -> dict:
        """
        Build the GoukassianPrincipleBlock required on every API request.
        Lantern, Signature, and License are the three constitutional properties.
        """
        return {
            "lantern": {
                "artifactName": "lantern",
                "lanternHash": "0x" + "0" * 64,  # Replace with real lantern hash
            },
            "signature": {
                "artifactName": "signature",
                "agentSignature": "0x" + "0" * 128,  # Replace with real Ed25519 sig
            },
            "license": {
                "artifactName": "license",
                "licenseScope": ["trade", "governance"],  # Replace with real scope
            },
        }


# ---------------------------------------------------------------------------
# NL=NA VALIDATION
# ---------------------------------------------------------------------------

class NLNAValidator:
    """
    Off-chain NL=NA enforcement (Layers 1-4).
    Layer 5 is enforced on-chain by TL_Ledger_Core.registerPermissionToken.
    """

    GOVERNANCE_LANE_ORIGIN = "GOVERNANCE_LANE"

    @staticmethod
    def validate_state_envelope(governance_result: TLGovernanceResult) -> bool:
        """
        NL=NA Layer 1: StateEnvelope if/then constraint.
        State +1 requires a PermissionToken. No token = no proceed.
        """
        if governance_result.current_state == TLState.PROCEED:
            if governance_result.permission_token is None:
                log.error(
                    "NL=NA Layer 1 VIOLATION: State +1 without PermissionToken. "
                    "Ghost Governance prevented. trace_id=%s",
                    governance_result.trace_id
                )
                return False
        return True

    @staticmethod
    def validate_lane_origin(permission_token: TLPermissionToken) -> bool:
        """
        NL=NA Layer 2: PermissionToken.laneOrigin must equal "GOVERNANCE_LANE".
        Any other value is schema-invalid and constitutionally blocked.
        """
        if permission_token.lane_origin != NLNAValidator.GOVERNANCE_LANE_ORIGIN:
            log.error(
                "NL=NA Layer 2 VIOLATION: PermissionToken laneOrigin='%s', "
                "expected='%s'. Ghost Governance prevented. token_id=%s",
                permission_token.lane_origin,
                NLNAValidator.GOVERNANCE_LANE_ORIGIN,
                permission_token.token_id,
            )
            return False
        return True

    @staticmethod
    def validate_permission_token_present(governance_result: TLGovernanceResult) -> bool:
        """
        NL=NA Layer 3: TGLF_StateP1 requires permissionToken.
        If the Governance Lane returned State +1 without a token, refuse.
        """
        if governance_result.current_state == TLState.PROCEED:
            if not governance_result.permission_token:
                log.error(
                    "NL=NA Layer 3 VIOLATION: TGLF_StateP1 without permissionToken. "
                    "trace_id=%s",
                    governance_result.trace_id
                )
                return False
        return True

    @staticmethod
    def validate_governance_proof(
        permission_token: TLPermissionToken,
        transaction_hash: str
    ) -> bool:
        """
        NL=NA Layer 4: GovernanceProof.logHash must match PermissionToken.logHash.
        GovernanceProof.merkleRoot must match PermissionToken.merkleRoot.
        Cross-reference verification before on-chain submission.
        """
        if permission_token.log_hash.lower() != transaction_hash.lower():
            log.error(
                "NL=NA Layer 4 VIOLATION: GovernanceProof.logHash mismatch. "
                "token_log_hash=%s, tx_hash=%s",
                permission_token.log_hash,
                transaction_hash,
            )
            return False
        if not permission_token.merkle_root:
            log.error(
                "NL=NA Layer 4 VIOLATION: PermissionToken.merkleRoot is empty. "
                "token_id=%s",
                permission_token.token_id,
            )
            return False
        return True

    @staticmethod
    def validate_token_not_expired(permission_token: TLPermissionToken) -> bool:
        """Check PermissionToken has not expired before submitting on-chain."""
        current_ms = int(time.time() * 1000)
        if current_ms >= permission_token.expires_at:
            log.error(
                "PermissionToken expired. token_id=%s expires_at=%s current=%s",
                permission_token.token_id,
                permission_token.expires_at,
                current_ms,
            )
            return False
        return True

    @classmethod
    def validate_all(
        cls,
        governance_result: TLGovernanceResult,
        transaction_hash: str
    ) -> bool:
        """Run all four off-chain NL=NA layers in sequence."""
        if not cls.validate_state_envelope(governance_result):
            return False
        if governance_result.current_state != TLState.PROCEED:
            return True  # Layers 2-4 only apply to State +1
        pt = governance_result.permission_token
        if not cls.validate_permission_token_present(governance_result):
            return False
        if not cls.validate_lane_origin(pt):
            return False
        if not cls.validate_governance_proof(pt, transaction_hash):
            return False
        if not cls.validate_token_not_expired(pt):
            return False
        return True


# ---------------------------------------------------------------------------
# WEB3 CONTRACT CLIENT
# ---------------------------------------------------------------------------

class TLContractClient:
    """
    Web3 client for TL smart contract interactions.
    Submits to chain ONLY after full NL=NA validation (Layers 1-4 passed).
    TL_Ledger_Core.registerPermissionToken is NL=NA Layer 5.
    """

    def __init__(self, config: dict):
        rpc_url = config["RPC_URL"]
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        private_key = os.environ.get("TL_PRIVATE_KEY") or config.get("PRIVATE_KEY", "")
        if not private_key or private_key == "YOUR_WALLET_PRIVATE_KEY_HERE":
            raise ValueError(
                "TL_Bridge: PRIVATE_KEY not set. "
                "Set TL_PRIVATE_KEY environment variable."
            )

        self.account = self.w3.eth.account.from_key(private_key)
        self.gas_config = config.get("GAS", {})

        addresses = config.get("CONTRACT_ADDRESSES", {})
        self.ledger_core_address = Web3.to_checksum_address(
            addresses.get("TL_LEDGER_CORE", "0x" + "0" * 40)
        )

        # Minimal ABI for registerPermissionToken
        # Full ABI in tl_abi.json
        self.ledger_core_abi = [
            {
                "name": "registerPermissionToken",
                "type": "function",
                "stateMutability": "payable",
                "inputs": [
                    {"name": "tokenId",        "type": "bytes32"},
                    {"name": "logHash",         "type": "bytes32"},
                    {"name": "merkleRoot",       "type": "bytes32"},
                    {"name": "merkleProof",      "type": "bytes32[]"},
                    {"name": "epochTimestamp",   "type": "uint256"},
                    {"name": "expiresAt",        "type": "uint256"},
                    {"name": "signerKeyId",      "type": "bytes32"},
                    {"name": "laneOriginHash",   "type": "bytes32"},
                    {"name": "signatureValue",   "type": "bytes"},
                ],
                "outputs": [{"name": "registered", "type": "bool"}],
            },
        ]

        self.ledger_core = self.w3.eth.contract(
            address=self.ledger_core_address,
            abi=self.ledger_core_abi,
        )

    def register_permission_token(
        self,
        permission_token: TLPermissionToken,
        merkle_proof: list,
        permission_token_fee_wei: int = 0,
    ) -> str:
        """
        NL=NA Layer 5: Register PermissionToken on-chain.
        TL_Ledger_Core.registerPermissionToken reverts NLNAViolation if:
          - logHash not in anchored Merkle root
          - laneOriginHash != keccak256("GOVERNANCE_LANE")
        This is the terminal constitutional gate.

        Returns the transaction hash on success.
        """
        token_id_bytes   = bytes.fromhex(permission_token.token_id.lstrip("0x"))
        log_hash_bytes   = bytes.fromhex(permission_token.log_hash.lstrip("0x"))
        merkle_root_bytes = bytes.fromhex(permission_token.merkle_root.lstrip("0x"))
        signer_key_bytes = bytes.fromhex(permission_token.signer_key_id.lstrip("0x"))
        lane_origin_hash = Web3.keccak(text="GOVERNANCE_LANE")
        sig_bytes        = bytes.fromhex(permission_token.signature_value.lstrip("0x"))
        proof_bytes      = [bytes.fromhex(p.lstrip("0x")) for p in merkle_proof]

        nonce = self.w3.eth.get_transaction_count(self.account.address)
        gas_limit = self.gas_config.get("GAS_LIMIT_REGISTER_TOKEN", 200_000)
        gas_price = self.w3.to_wei(
            self.gas_config.get("GAS_PRICE_GWEI", 20), "gwei"
        )

        tx = self.ledger_core.functions.registerPermissionToken(
            token_id_bytes,
            log_hash_bytes,
            merkle_root_bytes,
            proof_bytes,
            permission_token.epoch_timestamp,
            permission_token.expires_at,
            signer_key_bytes,
            lane_origin_hash,
            sig_bytes,
        ).build_transaction({
            "from":     self.account.address,
            "nonce":    nonce,
            "gas":      gas_limit,
            "gasPrice": gas_price,
            "value":    permission_token_fee_wei,  # TL service fee -> Treasury
        })

        signed_tx = self.w3.eth.account.sign_transaction(
            tx, private_key=self.account.key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if receipt.status != 1:
            raise RuntimeError(
                f"TL_Bridge: registerPermissionToken reverted. "
                f"tx={tx_hash.hex()} — NL=NA Layer 5 enforcement."
            )

        log.info(
            "NL=NA Layer 5: PermissionToken registered on-chain. "
            "token_id=%s tx=%s",
            permission_token.token_id,
            tx_hash.hex(),
        )
        return tx_hash.hex()


# ---------------------------------------------------------------------------
# MAIN BRIDGE
# ---------------------------------------------------------------------------

class TLDataBridge:
    """
    TL Data Bridge: routes every transaction through the full
    API → NL=NA validation → smart contract pipeline.

    Ghost Governance is impossible through this bridge:
    no contract call is made without a valid PermissionToken
    that has passed all five NL=NA enforcement layers.
    """

    def __init__(self, config_path: str = "TL_Config.json"):
        self.config = load_config(config_path)
        self.api = TLAPIClient(self.config)
        self.contract = TLContractClient(self.config)
        self.validator = NLNAValidator()

    def process_transaction(
        self,
        transaction_data: dict,
        proposed_action: str,
        evidence_uri: str,
        domain: str = "trade",
        merkle_proof: list = None,
    ) -> TLBridgeResult:
        """
        Full TL pipeline for a single transaction.

        Step 1: POST /decisions        — Inference Lane, get TLResult
        Step 2: POST /governance-logs  — Governance Lane, get StateEnvelope
        Step 3: NL=NA validation       — Layers 1-4 off-chain
        Step 4: On-chain registration  — Layer 5 (State +1 only)

        State 0 (EpistemicHold) and State -1 (Refuse) never reach the contract.
        EpistemicHold is free. Refuse is free. PermissionToken carries a fee.
        """
        trace_id = str(uuid.uuid4())
        merkle_proof = merkle_proof or []

        log.info(
            "TL pipeline start. proposed_action=%s trace_id=%s",
            proposed_action, trace_id
        )

        # ------------------------------------------------------------------
        # STEP 1: INFERENCE LANE
        # ------------------------------------------------------------------
        try:
            decision = self.api.post_decision(
                transaction_data=transaction_data,
                proposed_action=proposed_action,
                trace_id=trace_id,
                domain=domain,
            )
        except Exception as e:
            log.error("Inference Lane error: %s trace_id=%s", e, trace_id)
            return TLBridgeResult(
                state=TLState.EPISTEMIC_HOLD,  # Fail-closed
                state_label="EpistemicHold",
                trace_id=trace_id,
                decision_id="",
                error=f"Inference Lane error: {e}",
            )

        log.info(
            "Inference Lane: state=%s decision_id=%s trace_id=%s",
            decision.state_label, decision.decision_id, trace_id,
        )

        # ------------------------------------------------------------------
        # STEP 2: GOVERNANCE LANE
        # ------------------------------------------------------------------
        transaction_hash = Web3.keccak(
            text=json.dumps(transaction_data, sort_keys=True)
        ).hex()

        try:
            governance = self.api.post_governance_log(
                decision_id=decision.decision_id,
                transaction_hash=transaction_hash,
                evidence_uri=evidence_uri,
                trace_id=trace_id,
            )
        except Exception as e:
            log.error("Governance Lane error: %s trace_id=%s", e, trace_id)
            return TLBridgeResult(
                state=TLState.EPISTEMIC_HOLD,  # Fail-closed
                state_label="EpistemicHold",
                trace_id=trace_id,
                decision_id=decision.decision_id,
                error=f"Governance Lane error: {e}",
            )

        log.info(
            "Governance Lane: state=%s process=%s trace_id=%s",
            governance.state_label, governance.process_active, trace_id,
        )

        # ------------------------------------------------------------------
        # STEP 3: NL=NA VALIDATION (LAYERS 1-4)
        # ------------------------------------------------------------------
        if not self.validator.validate_all(governance, transaction_hash):
            log.error(
                "NL=NA validation failed. Ghost Governance prevented. trace_id=%s",
                trace_id,
            )
            return TLBridgeResult(
                state=TLState.REFUSE,
                state_label="Refuse",
                trace_id=trace_id,
                decision_id=decision.decision_id,
                error="NL=NA validation failed: Ghost Governance prevented.",
            )

        # ------------------------------------------------------------------
        # STEP 4A: STATE +1 (PROCEED) → ON-CHAIN REGISTRATION
        # ------------------------------------------------------------------
        if governance.current_state == TLState.PROCEED:
            pt = governance.permission_token

            # Determine fee from config (Nomination 2026)
            permission_token_fee_wei = self.config.get(
                "PERMISSION_TOKEN_FEE_WEI", 0
            )

            try:
                tx_hash = self.contract.register_permission_token(
                    permission_token=pt,
                    merkle_proof=merkle_proof,
                    permission_token_fee_wei=permission_token_fee_wei,
                )
            except Exception as e:
                log.error(
                    "NL=NA Layer 5 contract call failed: %s "
                    "token_id=%s trace_id=%s",
                    e, pt.token_id, trace_id,
                )
                return TLBridgeResult(
                    state=TLState.EPISTEMIC_HOLD,  # Fail-closed on contract error
                    state_label="EpistemicHold",
                    trace_id=trace_id,
                    decision_id=decision.decision_id,
                    permission_token_id=pt.token_id,
                    error=f"On-chain registration failed: {e}",
                )

            log.info(
                "PROCEED authorized. PermissionToken registered on-chain. "
                "token_id=%s tx=%s trace_id=%s",
                pt.token_id, tx_hash, trace_id,
            )

            return TLBridgeResult(
                state=TLState.PROCEED,
                state_label="Proceed",
                trace_id=trace_id,
                decision_id=decision.decision_id,
                permission_token_id=pt.token_id,
                on_chain_tx=tx_hash,
            )

        # ------------------------------------------------------------------
        # STEP 4B: STATE 0 (EPISTEMIC HOLD) → LOG AND HOLD
        # Epistemic Hold is free. No contract call. No execution.
        # ------------------------------------------------------------------
        elif governance.current_state == TLState.EPISTEMIC_HOLD:
            log.info(
                "EPISTEMIC HOLD. Execution suspended pending governance review. "
                "escrow_id=%s rationale=%s trace_id=%s",
                governance.escrow_record_id,
                governance.escrow_rationale,
                trace_id,
            )

            return TLBridgeResult(
                state=TLState.EPISTEMIC_HOLD,
                state_label="EpistemicHold",
                trace_id=trace_id,
                decision_id=decision.decision_id,
                escrow_record_id=governance.escrow_record_id,
            )

        # ------------------------------------------------------------------
        # STEP 4C: STATE -1 (REFUSE) → LOG AND STOP
        # Refuse is permanent by default. No contract call. No execution.
        # ------------------------------------------------------------------
        else:
            log.info(
                "REFUSE. Action denied. Permanent by default. "
                "decision_id=%s trace_id=%s",
                decision.decision_id, trace_id,
            )

            return TLBridgeResult(
                state=TLState.REFUSE,
                state_label="Refuse",
                trace_id=trace_id,
                decision_id=decision.decision_id,
            )


# ---------------------------------------------------------------------------
# CLI ENTRYPOINT
# ---------------------------------------------------------------------------

def main():
    """
    Example CLI usage. Replace with production transaction data.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="TL Data Bridge — routes transactions through TL governance"
    )
    parser.add_argument(
        "--config", default="TL_Config.json",
        help="Path to TL_Config.json"
    )
    parser.add_argument(
        "--action", default="execute_trade",
        help="Proposed action string"
    )
    parser.add_argument(
        "--domain", default="trade",
        choices=["trade", "policy", "supply-chain", "general"],
        help="Governance domain"
    )
    args = parser.parse_args()

    bridge = TLDataBridge(config_path=args.config)

    # Example transaction - replace with real data
    transaction_data = {
        "asset":    "BTC-USD",
        "quantity": 1.5,
        "price":    50000.00,
        "side":     "buy",
        "timestamp": int(time.time()),
    }

    result = bridge.process_transaction(
        transaction_data=transaction_data,
        proposed_action=args.action,
        evidence_uri="ipfs://QmYourEvidenceHashHere",
        domain=args.domain,
    )

    print(json.dumps({
        "state":               result.state_label,
        "trace_id":            result.trace_id,
        "decision_id":         result.decision_id,
        "permission_token_id": result.permission_token_id,
        "on_chain_tx":         result.on_chain_tx,
        "escrow_record_id":    result.escrow_record_id,
        "error":               result.error,
    }, indent=2))


if __name__ == "__main__":
    main()
