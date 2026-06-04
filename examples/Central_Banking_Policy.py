"""
Ternary Logic Framework: Central Banking Policy Analysis
=========================================================

Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com
Successor: support@tl-goukassian.org
Repository: https://github.com/FractonicMind/TernaryLogic

DOI 1: 10.1007/s43681-025-00910-6, Auditable AI: Tracing the Ethical History of a Model
DOI 2: 10.1007/s43681-026-01124-0, A Ternary Logic Framework for Institutional Governance

The Goukassian Vow:
    "Pause when truth is uncertain"  ->  State  0  (Epistemic Hold)
    "Refuse when harm is clear"      ->  State -1  (Refuse)
    "Proceed where truth is"         ->  State +1  (Proceed)

This example demonstrates TL applied to central bank monetary policy:
    - Dual mandate analysis (inflation stability + maximum employment)
    - Basel III capital adequacy monitoring
    - FATF AML/CFT compliance
    - IOSCO market integrity verification
    - Regime-aware signal weighting
    - Solvency Protocol during Epistemic Hold
    - NL=NA write-before-act for every policy decision

THRESHOLD GOVERNANCE:
    Central banks must calibrate thresholds through their own governance process.
    The values used here are labeled as demonstration values only.
    Different central banks, different mandates, different calibrations.
    No universal values exist. See docs/Threshold_Calibration.md.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import numpy as np

# TL Framework imports
from ternary_logic import TLEngine, TLState, TLValue, verify_mandate, calculate_confidence


# =============================================================================
# SECTION 1: Regulatory Context Builder
# Maps central banking regulatory requirements to TL schema structures.
# Covers Basel III, FATF, IOSCO, GDPR, Paris Agreement.
# =============================================================================

def build_regulatory_context(
    economic_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build a RegulatoryContext record conforming to tl_schema.json.

    In production this is constructed by the Governance Lane from verified
    regulatory feeds. Each sub-object maps to a specific regulatory framework.
    The Governance Lane evaluates all checks before issuing a PermissionToken.
    """
    # Basel III: capital adequacy, liquidity, leverage
    tier1_ratio = economic_data.get("tier1_capital_ratio", 0.0)
    lcr = economic_data.get("liquidity_coverage_ratio", 0.0)
    nsfr = economic_data.get("net_stable_funding_ratio", 0.0)

    basel = {
        "lcr": lcr,
        "nsfr": nsfr,
        "capitalRatio": tier1_ratio,
        "stressTestRequired": tier1_ratio < 0.10,
        "counterpartyExposureWithinLimits": economic_data.get(
            "counterparty_within_limits", True
        )
    }

    # FATF: AML/CFT screening
    fatf = {
        "amlCheckRequired": True,
        "sanctionsScreened": economic_data.get("sanctions_screened", False),
        "pepInvolved": economic_data.get("pep_involved", False),
        "sarGenerated": economic_data.get("sar_required", False)
    }

    # IOSCO: market integrity
    iosco = {
        "layeringDetected": economic_data.get("layering_detected", False),
        "spoofingDetected": economic_data.get("spoofing_detected", False),
        "washTradingDetected": economic_data.get("wash_trading_detected", False),
        "crossMarketManipulationDetected": economic_data.get(
            "cross_market_manipulation", False
        )
    }

    # GDPR: data privacy
    gdpr = {
        "jurisdiction": economic_data.get("jurisdiction", "EU"),
        "consentAttestation": economic_data.get("consent_attested", True),
        "erasureEligible": economic_data.get("erasure_eligible", False)
    }

    # Paris Agreement: sustainability
    paris = {
        "carbonFootprintVerified": economic_data.get(
            "carbon_footprint_verified", False
        ),
        "greenBondEligibility": economic_data.get("green_bond_eligible", False),
        "esgScore": economic_data.get("esg_score", 0.0)
    }

    return {
        "baselIii": basel,
        "fatf": fatf,
        "iosco": iosco,
        "gdpr": gdpr,
        "parisAgreement": paris,
        "regulatoryFrameworkVersion": {
            "baselVersion": "Basel III 2023",
            "fatfVersion": "FATF 40+9 2023",
            "ioscoVersion": "IOSCO Principles 2023",
            "gdprVersion": "GDPR 2018"
        }
    }


def check_regulatory_compliance(
    regulatory_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Evaluate regulatory context for compliance flags.

    Returns a compliance summary with specific failures identified.
    Any FATAL flag triggers Epistemic Hold via force_state override.
    """
    failures = []
    warnings = []

    # Basel III checks
    basel = regulatory_context["baselIii"]
    if basel["capitalRatio"] < 0.08:
        failures.append(f"Basel III: Tier 1 capital ratio {basel['capitalRatio']:.2%} below 8% minimum")
    elif basel["capitalRatio"] < 0.10:
        warnings.append(f"Basel III: Tier 1 capital ratio {basel['capitalRatio']:.2%} below 10% buffer")
    if basel["lcr"] < 1.0:
        failures.append(f"Basel III: LCR {basel['lcr']:.2f} below 1.0 minimum")
    if basel["stressTestRequired"]:
        warnings.append("Basel III: Stress test required before rate change")

    # FATF checks
    fatf = regulatory_context["fatf"]
    if not fatf["sanctionsScreened"]:
        failures.append("FATF: Sanctions screening not completed")
    if fatf["sarGenerated"]:
        warnings.append("FATF: SAR generated; enhanced monitoring required")

    # IOSCO checks
    iosco = regulatory_context["iosco"]
    if iosco["layeringDetected"] or iosco["spoofingDetected"]:
        failures.append("IOSCO: Market manipulation detected")
    if iosco["crossMarketManipulationDetected"]:
        failures.append("IOSCO: Cross-market manipulation detected; FATAL")

    return {
        "compliant": len(failures) == 0,
        "failures": failures,
        "warnings": warnings,
        "pillarImplicated": (
            "EconomicRightsAndTransparencyMandate"
            if failures else "EpistemicHold"
        )
    }


# =============================================================================
# SECTION 2: Macroeconomic Signal Analysis
# Converts economic indicators into normalized confidence signals.
# =============================================================================

class DualMandateAnalyzer:
    """
    Analyze economic indicators for monetary policy implications.

    Implements the dual mandate framework:
    Pillar 1 (Price Stability): inflation target convergence
    Pillar 2 (Maximum Employment): labor market strength

    When the mandates conflict, the system enters Epistemic Hold pending
    human review by the monetary policy committee.

    Threshold calibration note: central banks calibrate their own thresholds
    through historical backtesting, regulatory requirements, and board
    approval. The analyzer produces confidence signals; the TLEngine
    evaluates them against institution-calibrated thresholds.
    """

    def __init__(
        self,
        inflation_target: float = 0.02,
        unemployment_target: float = 0.04
    ):
        self.inflation_target = inflation_target
        self.unemployment_target = unemployment_target

    def analyze_inflation(self, inflation_data: List[float]) -> Optional[float]:
        """Analyze inflation trend relative to target. Returns signal [-1, +1]."""
        if not inflation_data or len(inflation_data) < 3:
            return None

        recent = np.mean(inflation_data[-3:])
        trend = float(np.polyfit(range(len(inflation_data)), inflation_data, 1)[0])

        target_deviation = (recent - self.inflation_target) / self.inflation_target
        annualized_trend = trend * 12

        signal = (target_deviation * 0.7) + (annualized_trend * 0.3)
        return float(np.clip(signal * 2, -1, 1))

    def analyze_inflation_expectations(
        self, expectations: Dict[str, float]
    ) -> Optional[float]:
        """Analyze inflation expectations anchoring. Returns signal [-1, +1]."""
        if "five_year_forward" not in expectations:
            return None

        five_yr = expectations["five_year_forward"]
        deviation = (five_yr - self.inflation_target) / self.inflation_target

        if abs(deviation) < 0.10:
            return 0.0
        return float(np.clip(deviation * 2, -1, 1))

    def analyze_labor_market(
        self,
        unemployment_rate: float,
        job_openings: Optional[float] = None
    ) -> float:
        """Analyze labor market strength. Returns signal [-1, +1]."""
        gap = (unemployment_rate - self.unemployment_target) / self.unemployment_target
        signal = -gap

        if job_openings is not None and unemployment_rate > 0:
            ratio = job_openings / unemployment_rate
            if ratio > 1.5:
                signal += 0.3
            elif ratio < 0.8:
                signal -= 0.3

        return float(np.clip(signal, -1, 1))

    def analyze_gdp_growth(self, gdp_growth: List[float]) -> Optional[float]:
        """Analyze GDP growth momentum. Returns signal [-1, +1]."""
        if not gdp_growth or len(gdp_growth) < 2:
            return None

        recent = np.mean(gdp_growth[-2:])
        trend_growth = 0.025
        gap = (recent - trend_growth) / trend_growth
        return float(np.clip(gap, -1, 1))

    def analyze_financial_conditions(self, fci: float) -> float:
        """Analyze financial conditions index. Returns signal [-1, +1]."""
        return float(np.clip(-fci / 2, -1, 1))

    def detect_mandate_conflict(self, signals: Dict[str, Any]) -> bool:
        """
        Detect dual mandate conflict.

        Returns True when inflation signals and employment signals point
        in opposite directions beyond a threshold. Conflict triggers
        Epistemic Hold pending monetary policy committee review.
        """
        inflation_sig = signals.get("inflation_trend")
        employment_sig = signals.get("labor_market_strength")

        if inflation_sig is None or employment_sig is None:
            return False

        # Conflict: inflation wants tightening, employment wants easing (or vice versa)
        # Both signals strong enough to be constitutionally significant
        return (
            inflation_sig > 0.30 and employment_sig < -0.30
        ) or (
            inflation_sig < -0.30 and employment_sig > 0.30
        )

    def analyze_all(self, economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run all signal analyses. Returns dict of signals."""
        signals = {}

        if "core_pce_inflation" in economic_data:
            signals["inflation_trend"] = self.analyze_inflation(
                economic_data["core_pce_inflation"]
            )

        if "inflation_expectations" in economic_data:
            signals["inflation_expectations"] = self.analyze_inflation_expectations(
                economic_data["inflation_expectations"]
            )

        if "unemployment_rate" in economic_data:
            signals["labor_market_strength"] = self.analyze_labor_market(
                economic_data["unemployment_rate"],
                economic_data.get("job_openings")
            )

        if "gdp_growth" in economic_data:
            signals["economic_momentum"] = self.analyze_gdp_growth(
                economic_data["gdp_growth"]
            )

        if "financial_conditions_index" in economic_data:
            signals["financial_conditions"] = self.analyze_financial_conditions(
                economic_data["financial_conditions_index"]
            )

        signals["mandate_conflict"] = self.detect_mandate_conflict(signals)

        return signals


# =============================================================================
# SECTION 3: Governance Artifacts (from Quickstart pattern)
# =============================================================================

def create_goukassian_principle_block(
    decision_payload: str,
    agent_id: str,
    license_scopes: list
) -> Dict[str, Any]:
    """Three Goukassian Principle artifacts. See Quickstart_Example.py."""
    payload_bytes = decision_payload.encode("utf-8")
    return {
        "lantern": {
            "artifactName": "lantern",
            "lanternHash": hashlib.sha256(payload_bytes).hexdigest()
        },
        "signature": {
            "artifactName": "signature",
            "agentSignature": hashlib.sha512(
                (agent_id + decision_payload).encode("utf-8")
            ).hexdigest()
        },
        "license": {
            "artifactName": "license",
            "licenseScope": license_scopes
        }
    }


def commit_log_entry(
    decision: TLValue,
    engine: TLEngine,
    goukassian_block: Dict[str, Any],
    previous_hash: str,
    extra_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Commit governance log entry to Immutable Ledger. NL=NA: before actuation."""
    log_id = str(uuid.uuid4())
    committed_at = datetime.now(timezone.utc).isoformat()

    canonical = json.dumps({
        "logId": log_id,
        "state": decision.state.name,
        "stateValue": decision.state.value,
        "confidence": decision.confidence,
        "reasoning": decision.reasoning,
        "committedAt": committed_at
    }, sort_keys=True)

    log_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    merkle_root = hashlib.sha256(
        (previous_hash + log_hash).encode("utf-8")
    ).hexdigest()

    entry = {
        "logId": log_id,
        "currentState": decision.state.value,
        "stateLabel": decision.state.name,
        "processActive": {
            TLState.PROCEED: "ProceedAuthorized",
            TLState.EPISTEMIC_HOLD: "GovernancePause",
            TLState.REFUSE: "RefusalPermanent"
        }[decision.state],
        "confidence": decision.confidence,
        "reasoning": decision.reasoning,
        "logHash": log_hash,
        "merkleRoot": merkle_root,
        "previousHash": previous_hash,
        "committedAt": committed_at,
        "goukassianPrinciple": goukassian_block,
        "pufAttestation": "NULL_PUF_DEPLOYMENT",
        "architectureMode": "ARCHITECTURE_B",
        "engineConfig": {
            "proceedThreshold": engine.proceed_threshold,
            "holdThreshold": engine.hold_threshold
        }
    }
    if extra_context:
        entry["domainContext"] = extra_context

    return entry


def build_permission_token(log_entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """PermissionToken for PROCEED. laneOrigin const GOVERNANCE_LANE. NL=NA Layer 2."""
    if log_entry["currentState"] != TLState.PROCEED.value:
        return None

    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(milliseconds=300000)

    return {
        "tokenId": str(uuid.uuid4()),
        "logHash": log_entry["logHash"],
        "merkleRoot": log_entry["merkleRoot"],
        "laneOrigin": "GOVERNANCE_LANE",  # NL=NA Layer 2 const
        "issuedAt": issued_at.isoformat(),
        "expiresAt": expires_at.isoformat(),
        "maxLifetimeMs": 300000,
        "revocationStatus": "ACTIVE",
        "signerKeyId": "central-bank-hsm-001",
        "epochTimestamp": int(issued_at.timestamp()),
        "signatureValue": hashlib.sha256(
            log_entry["logHash"].encode()
        ).hexdigest()
    }


class ImmutableLedger:
    """Pillar II: append-only hash chain. See Quickstart_Example.py."""

    def __init__(self):
        self._entries = []
        self._genesis_hash = hashlib.sha256(b"TL_CENTRAL_BANK_GENESIS").hexdigest()

    @property
    def previous_hash(self) -> str:
        return self._entries[-1]["merkleRoot"] if self._entries else self._genesis_hash

    def commit(self, entry: Dict[str, Any]) -> str:
        self._entries.append(entry)
        return entry["logHash"]

    @property
    def size(self) -> int:
        return len(self._entries)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "totalEntries": self.size,
            "latestMerkleRoot": self.previous_hash,
            "states": {
                "PROCEED": sum(1 for e in self._entries if e["currentState"] == 1),
                "EPISTEMIC_HOLD": sum(1 for e in self._entries if e["currentState"] == 0),
                "REFUSE": sum(1 for e in self._entries if e["currentState"] == -1)
            }
        }


# =============================================================================
# SECTION 4: Central Bank Policy Engine
# =============================================================================

class CentralBankPolicyEngine:
    """
    Central Bank Monetary Policy Engine using Ternary Logic.

    Implements sovereign-grade accountability for monetary policy decisions
    through Eight Pillars architecture:
        Pillar I:   Epistemic Hold (dual mandate conflict, data gaps)
        Pillar II:  Immutable Ledger (every decision committed before acting)
        Pillar III: Goukassian Principle (lantern, signature, license)
        Pillar IV:  Decision Logs (complete audit trail)
        Pillar V:   Economic Rights (FATF, IOSCO, Basel III compliance)
        Pillar VI:  Sustainable Capital (Paris Agreement, ESG verification)
        Pillar VII: Hybrid Shield (privacy-preserving transparency)
        Pillar VIII:Anchors (Merkle root anchoring, RFC 3161 timestamps)

    THRESHOLD GOVERNANCE:
        The old API parameter halt_threshold is replaced by
        proceed_threshold and hold_threshold in the current TLEngine.
        Central banks calibrate these through their own governance process.
        Demonstration values are labeled clearly. Not for production use.
    """

    def __init__(
        self,
        proceed_threshold: float,
        hold_threshold: float,
        inflation_target: float = 0.02,
        unemployment_target: float = 0.04,
        current_policy_rate: float = 0.05
    ):
        """
        Initialize Central Bank Policy Engine.

        Args:
            proceed_threshold: Institution-calibrated PROCEED threshold.
                               REQUIRED. No default.
            hold_threshold:    Institution-calibrated REFUSE threshold.
                               REQUIRED. No default.
            inflation_target:  Central bank inflation target (e.g. 0.02 for 2%).
            unemployment_target: Natural rate of unemployment estimate.
            current_policy_rate: Current policy interest rate.
        """
        self.engine = TLEngine(
            proceed_threshold=proceed_threshold,
            hold_threshold=hold_threshold,
            epistemic_hold_rate_target=0.20
        )
        self.analyzer = DualMandateAnalyzer(
            inflation_target=inflation_target,
            unemployment_target=unemployment_target
        )
        self.current_policy_rate = current_policy_rate
        self.ledger = ImmutableLedger()
        self.license_scopes = [
            "monetary.policy",
            "regulatory.compliance",
            "audit.governance"
        ]
        self._policy_decisions = []

    def make_policy_decision(
        self,
        economic_data: Dict[str, Any],
        scenario_label: str = "Policy Decision"
    ) -> Dict[str, Any]:
        """
        Make a monetary policy decision under full TL constitutional governance.

        Sequence:
            1. Analyze economic signals (dual mandate)
            2. Check regulatory compliance (Pillar V)
            3. Check sustainable capital (Pillar VI)
            4. Calculate composite confidence
            5. Evaluate with TLEngine
            6. Commit log entry (NL=NA: before any action fires)
            7. Issue Permission Token if PROCEED
            8. Return full governance record

        Returns a complete governance record including state, confidence,
        regulatory context, log entry, and permission token if applicable.
        """
        # Step 1: Analyze economic signals
        signals = self.analyzer.analyze_all(economic_data)

        # Step 2: Regulatory compliance check (Pillar V)
        regulatory_context = build_regulatory_context(economic_data)
        compliance = check_regulatory_compliance(regulatory_context)

        # Step 3: Sustainable capital check (Pillar VI)
        sustainability_data = {
            "esg_verified": economic_data.get("esg_verified", False),
            "emissions_anchored": economic_data.get("emissions_anchored", False),
            "use_of_proceeds_tracked": economic_data.get(
                "use_of_proceeds_tracked", False
            )
        }

        # Step 4: Determine state
        # Mandate failures force Epistemic Hold regardless of confidence
        if not compliance["compliant"]:
            forced_state = TLState.EPISTEMIC_HOLD
            confidence = 0.0
            reasoning = (
                f"Regulatory compliance failure prevents policy action. "
                f"Failures: {'; '.join(compliance['failures'])}"
            )
        elif signals.get("mandate_conflict"):
            forced_state = TLState.EPISTEMIC_HOLD
            confidence = 0.30
            reasoning = (
                "Dual mandate conflict detected: inflation and employment "
                "signals point in opposite directions. Monetary Policy "
                "Committee review required before rate decision."
            )
        else:
            forced_state = None
            # Calculate composite confidence from available signals
            clean_signals = {
                k: v for k, v in signals.items()
                if v is not None and k != "mandate_conflict"
                and isinstance(v, (int, float))
            }

            if clean_signals:
                # Normalize signals from [-1,+1] to [0,1] for confidence scoring
                normalized = [(v + 1) / 2 for v in clean_signals.values()]
                confidence = float(np.mean(normalized))
            else:
                # No signals available: Epistemic Hold on data absence
                forced_state = TLState.EPISTEMIC_HOLD
                confidence = 0.0

            reasoning = self._build_reasoning(signals, economic_data)

        # Step 5: Evaluate with TLEngine
        decision = self.engine.evaluate(
            confidence=confidence,
            reasoning=reasoning,
            metadata={
                "scenario": scenario_label,
                "signalCount": len([
                    v for v in signals.values()
                    if v is not None and isinstance(v, (int, float))
                ]),
                "mandateConflict": signals.get("mandate_conflict", False),
                "complianceFailures": compliance["failures"],
                "pillarImplicated": compliance.get(
                    "pillarImplicated", "EpistemicHold"
                )
            },
            force_state=forced_state
        )

        # Step 6: Commit log entry (NL=NA: BEFORE any policy action fires)
        goukassian = create_goukassian_principle_block(
            decision_payload=decision.reasoning,
            agent_id="central-bank-governance-001",
            license_scopes=self.license_scopes
        )
        log_entry = commit_log_entry(
            decision=decision,
            engine=self.engine,
            goukassian_block=goukassian,
            previous_hash=self.ledger.previous_hash,
            extra_context={
                "signals": {
                    k: round(v, 4)
                    for k, v in signals.items()
                    if v is not None and isinstance(v, (int, float))
                },
                "regulatoryCompliant": compliance["compliant"],
                "regulatoryWarnings": compliance["warnings"],
                "currentPolicyRate": self.current_policy_rate
            }
        )
        self.ledger.commit(log_entry)

        # Step 7: Permission Token (PROCEED only)
        token = build_permission_token(log_entry)

        # Step 8: Policy rate recommendation (for PROCEED only)
        rate_recommendation = None
        if decision.state == TLState.PROCEED:
            rate_recommendation = self._recommend_rate_change(signals)

        # Assemble governance record
        record = {
            "scenario": scenario_label,
            "state": decision.state.name,
            "stateValue": decision.state.value,
            "processActive": log_entry["processActive"],
            "confidence": decision.confidence,
            "positionLabel": decision.position_label,
            "reasoning": decision.reasoning,
            "logHash": log_entry["logHash"][:16] + "...",
            "merkleRoot": log_entry["merkleRoot"][:16] + "...",
            "permissionToken": (
                token["tokenId"][:16] + "..." if token else None
            ),
            "laneOrigin": token["laneOrigin"] if token else "N/A",
            "rateRecommendation": rate_recommendation,
            "dualMandateConflict": signals.get("mandate_conflict", False),
            "regulatoryCompliant": compliance["compliant"],
            "regulatoryWarnings": compliance["warnings"],
            "regulatoryFailures": compliance["failures"],
            "nlNaStatus": "Log committed before policy action authorized"
        }

        self._policy_decisions.append(record)
        return record

    def _build_reasoning(
        self,
        signals: Dict[str, Any],
        economic_data: Dict[str, Any]
    ) -> str:
        """Build human-readable reasoning string from signals."""
        parts = []

        inflation = signals.get("inflation_trend")
        if inflation is not None:
            if inflation > 0.30:
                parts.append("Inflation above target: tightening signal")
            elif inflation < -0.30:
                parts.append("Inflation below target: easing signal")
            else:
                parts.append("Inflation near target: neutral signal")

        labor = signals.get("labor_market_strength")
        if labor is not None:
            if labor > 0.30:
                parts.append("Labor market tight: limited slack for easing")
            elif labor < -0.30:
                parts.append("Labor market weak: easing supportive")
            else:
                parts.append("Labor market balanced")

        momentum = signals.get("economic_momentum")
        if momentum is not None:
            if momentum > 0.20:
                parts.append("GDP above trend: supportive of tightening")
            elif momentum < -0.20:
                parts.append("GDP below trend: supportive of easing")

        regime = economic_data.get("inflation_regime", "normal")
        if regime == "high":
            parts.append("Regime: elevated inflation; inflation signals weighted higher")
        elif regime == "low":
            parts.append("Regime: low inflation; employment signals weighted higher")

        return ". ".join(parts) if parts else "Insufficient signal data for determination"

    def _recommend_rate_change(self, signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend a rate change direction for PROCEED decisions.

        This is advisory only. The monetary policy committee makes the
        final determination. TL authorizes the decision process, not the
        specific rate level.
        """
        inflation = signals.get("inflation_trend", 0.0) or 0.0
        labor = signals.get("labor_market_strength", 0.0) or 0.0
        momentum = signals.get("economic_momentum", 0.0) or 0.0

        composite = (inflation * 0.45) + (labor * 0.35) + (momentum * 0.20)

        # Rate signal thresholds: domain-specific parameters for rate
        # direction recommendations, NOT confidence thresholds.
        # Advisory only. Monetary policy committee decides the actual rate.
        strong_signal = 0.40
        if composite > strong_signal:
            direction = "TIGHTEN"
            basis_points_range = "25-50 bps"
        elif composite < -strong_signal:
            direction = "EASE"
            basis_points_range = "25-50 bps"
        elif -0.15 < composite < 0.15:
            direction = "HOLD"
            basis_points_range = "0 bps"
        elif composite > 0:
            direction = "TIGHTEN"
            basis_points_range = "0-25 bps"
        else:
            direction = "EASE"
            basis_points_range = "0-25 bps"

        return {
            "direction": direction,
            "basisPointsRange": basis_points_range,
            "compositeSignal": round(composite, 4),
            "note": (
                "Advisory only. Monetary policy committee "
                "makes final rate determination."
            )
        }

    def get_policy_summary(self) -> Dict[str, Any]:
        """Return summary of all policy decisions and ledger state."""
        engine_stats = self.engine.get_statistics()
        ledger_summary = self.ledger.get_summary()

        return {
            "totalDecisions": engine_stats["total_decisions"],
            "proceedCount": engine_stats["proceed_count"],
            "epistemicHoldCount": engine_stats["hold_count"],
            "refuseCount": engine_stats["refuse_count"],
            "epistemicHoldRate": engine_stats["epistemic_hold_rate"],
            "targetHoldRate": engine_stats["target_hold_rate"],
            "averageConfidence": engine_stats["average_confidence"],
            "ledgerEntries": ledger_summary["totalEntries"],
            "latestMerkleRoot": ledger_summary["latestMerkleRoot"][:16] + "...",
            "architectureMode": "ARCHITECTURE_B",
            "pufAttestation": "NULL_PUF_DEPLOYMENT"
        }


# =============================================================================
# SECTION 5: Demonstration Scenarios
# =============================================================================

def run_central_banking_demo():
    """
    Demonstrate TL central banking policy analysis across four scenarios:
        1. Rate hike justified: inflation above target, labor tight
        2. Epistemic Hold: dual mandate conflict
        3. Compliance failure: regulatory mandate forces hold
        4. Easing justified: below-target inflation, weak labor

    DEMONSTRATION THRESHOLD VALUES: not for production use.
    Central banks calibrate their own thresholds through:
        - 20+ years of historical backtesting
        - Regulatory requirements (BIS, FSB, national mandates)
        - Board-approved risk appetite
        - Monetary policy committee approval
        - TriCameralApproval and ledger anchoring before activation
    See docs/Threshold_Calibration.md.
    """

    print()
    print("=" * 70)
    print("  TERNARY LOGIC: CENTRAL BANKING POLICY ANALYSIS")
    print("  Lev Goukassian (ORCID: 0009-0006-5966-1243)")
    print("=" * 70)

    # DEMONSTRATION VALUES ONLY: not recommendations, not standards.
    DEMO_PROCEED = 0.72
    DEMO_HOLD = 0.32

    engine = CentralBankPolicyEngine(
        proceed_threshold=DEMO_PROCEED,
        hold_threshold=DEMO_HOLD,
        inflation_target=0.02,
        unemployment_target=0.04,
        current_policy_rate=0.05
    )

    print()
    print(f"  Engine initialized (demonstration thresholds: not for production)")
    print(f"  PROCEED >= {DEMO_PROCEED} | REFUSE < {DEMO_HOLD}")
    print(f"  Inflation target: 2% | Unemployment target: 4%")

    # ------------------------------------------------------------------
    # SCENARIO 1: Rate hike signal
    # Inflation above target, tight labor market, GDP above trend.
    # Expected: PROCEED with tightening recommendation.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 1: Rate Hike Signal")
    print("-" * 70)

    data_hike = {
        "core_pce_inflation": [0.031, 0.034, 0.036, 0.038, 0.040],
        "inflation_expectations": {"five_year_forward": 0.028},
        "unemployment_rate": 0.035,
        "job_openings": 0.055,
        "gdp_growth": [0.030, 0.032],
        "financial_conditions_index": -0.3,
        "tier1_capital_ratio": 0.135,
        "liquidity_coverage_ratio": 1.42,
        "net_stable_funding_ratio": 1.18,
        "sanctions_screened": True,
        "pep_involved": False,
        "sar_required": False,
        "layering_detected": False,
        "spoofing_detected": False,
        "wash_trading_detected": False,
        "cross_market_manipulation": False,
        "inflation_regime": "high",
        "jurisdiction": "EU",
        "consent_attested": True,
        "esg_score": 72.0
    }

    result1 = engine.make_policy_decision(data_hike, "Rate Hike Signal")
    _print_policy_result(result1)

    # ------------------------------------------------------------------
    # SCENARIO 2: Epistemic Hold via dual mandate conflict
    # Inflation above target (wants tightening) but unemployment rising
    # (wants easing). Conflicting mandates. MPC review required.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 2: Epistemic Hold via Dual Mandate Conflict")
    print("-" * 70)

    data_conflict = {
        "core_pce_inflation": [0.030, 0.033, 0.036, 0.038, 0.041],
        "inflation_expectations": {"five_year_forward": 0.026},
        "unemployment_rate": 0.052,
        "job_openings": 0.038,
        "gdp_growth": [0.018, 0.012],
        "financial_conditions_index": 0.8,
        "tier1_capital_ratio": 0.125,
        "liquidity_coverage_ratio": 1.28,
        "net_stable_funding_ratio": 1.09,
        "sanctions_screened": True,
        "pep_involved": False,
        "sar_required": False,
        "layering_detected": False,
        "spoofing_detected": False,
        "wash_trading_detected": False,
        "cross_market_manipulation": False,
        "inflation_regime": "high",
        "jurisdiction": "EU",
        "consent_attested": True,
        "esg_score": 68.0
    }

    result2 = engine.make_policy_decision(
        data_conflict, "Dual Mandate Conflict"
    )
    _print_policy_result(result2)

    # ------------------------------------------------------------------
    # SCENARIO 3: Regulatory compliance failure forces Epistemic Hold
    # Sanctions screening incomplete, IOSCO manipulation detected.
    # Even if economic signals are favorable, compliance failure
    # forces Epistemic Hold via Pillar V.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 3: Regulatory Compliance Failure (Pillar V)")
    print("-" * 70)

    data_compliance = {
        "core_pce_inflation": [0.018, 0.019, 0.020, 0.019, 0.021],
        "inflation_expectations": {"five_year_forward": 0.021},
        "unemployment_rate": 0.042,
        "gdp_growth": [0.025, 0.028],
        "financial_conditions_index": -0.1,
        "tier1_capital_ratio": 0.078,  # Below 8% minimum: FAIL
        "liquidity_coverage_ratio": 0.92,  # Below 1.0 minimum: FAIL
        "net_stable_funding_ratio": 1.05,
        "sanctions_screened": False,  # FAIL
        "pep_involved": False,
        "sar_required": False,
        "layering_detected": True,  # IOSCO FAIL
        "spoofing_detected": False,
        "wash_trading_detected": False,
        "cross_market_manipulation": False,
        "inflation_regime": "normal",
        "jurisdiction": "EU",
        "consent_attested": True,
        "esg_score": 55.0
    }

    result3 = engine.make_policy_decision(
        data_compliance, "Regulatory Compliance Failure"
    )
    _print_policy_result(result3)

    # ------------------------------------------------------------------
    # SCENARIO 4: Rate cut signal
    # Below-target inflation, rising unemployment, weak GDP.
    # Expected: PROCEED with easing recommendation.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 4: Rate Cut Signal")
    print("-" * 70)

    data_cut = {
        "core_pce_inflation": [0.016, 0.015, 0.014, 0.013, 0.012],
        "inflation_expectations": {"five_year_forward": 0.018},
        "unemployment_rate": 0.055,
        "job_openings": 0.040,
        "gdp_growth": [0.012, 0.008],
        "financial_conditions_index": 1.2,
        "tier1_capital_ratio": 0.148,
        "liquidity_coverage_ratio": 1.55,
        "net_stable_funding_ratio": 1.22,
        "sanctions_screened": True,
        "pep_involved": False,
        "sar_required": False,
        "layering_detected": False,
        "spoofing_detected": False,
        "wash_trading_detected": False,
        "cross_market_manipulation": False,
        "inflation_regime": "low",
        "jurisdiction": "EU",
        "consent_attested": True,
        "esg_score": 78.0
    }

    result4 = engine.make_policy_decision(data_cut, "Rate Cut Signal")
    _print_policy_result(result4)

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("POLICY SESSION SUMMARY")
    print("=" * 70)

    summary = engine.get_policy_summary()
    print(f"  Total decisions:     {summary['totalDecisions']}")
    print(f"  PROCEED:             {summary['proceedCount']}")
    print(f"  EPISTEMIC_HOLD:      {summary['epistemicHoldCount']}")
    print(f"  REFUSE:              {summary['refuseCount']}")
    print(f"  Hold rate:           {summary['epistemicHoldRate']:.1%} "
          f"(target: {summary['targetHoldRate']:.1%})")
    print(f"  Average confidence:  {summary['averageConfidence']:.3f}")
    print(f"  Ledger entries:      {summary['ledgerEntries']}")
    print(f"  Latest Merkle root:  {summary['latestMerkleRoot']}")
    print(f"  Architecture mode:   {summary['architectureMode']}")
    print(f"  PUF attestation:     {summary['pufAttestation']}")
    print()
    print("  NL=NA: Every policy decision was logged to the Immutable Ledger")
    print("  before any rate action was authorized. No log, no action.")
    print()
    print("  Three immutable mandates:")
    print("    No Spy. No Weapon. No Switch Off.")
    print("=" * 70)
    print()

    # Export audit trail (Pillar IV)
    engine.engine.export_audit_trail("/tmp/tl_central_bank_audit.json")
    print("  Audit trail exported: /tmp/tl_central_bank_audit.json")
    print()


def _print_policy_result(result: Dict[str, Any]):
    """Print a formatted policy decision result."""
    state_icons = {
        "PROCEED": "OK",
        "EPISTEMIC_HOLD": "HOLD",
        "REFUSE": "REFUSE"
    }

    print(f"  State:               {state_icons.get(result['state'], '')} "
          f"{result['state']} ({result['stateValue']})")
    print(f"  processActive:       {result['processActive']}")
    print(f"  Confidence:          {result['confidence']:.3f}")
    print(f"  Position:            {result['positionLabel']}")
    print(f"  Log committed:       {result['logHash']}")
    print(f"  Merkle root:         {result['merkleRoot']}")

    if result.get("permissionToken"):
        print(f"  Permission token:    {result['permissionToken']}")
        print(f"  laneOrigin:          {result['laneOrigin']}")
    else:
        print(f"  Permission token:    None (no actuation authorized)")

    if result.get("rateRecommendation"):
        rec = result["rateRecommendation"]
        print(f"  Rate recommendation: {rec['direction']} {rec['basisPointsRange']} "
              f"(composite signal: {rec['compositeSignal']:.3f})")

    if result.get("dualMandateConflict"):
        print(f"  Dual mandate:        CONFLICT DETECTED - MPC review required")

    if result.get("regulatoryFailures"):
        for failure in result["regulatoryFailures"]:
            print(f"  Compliance FAIL:     {failure}")

    if result.get("regulatoryWarnings"):
        for warning in result["regulatoryWarnings"][:2]:
            print(f"  Compliance warning:  {warning}")

    print(f"  NL=NA:               {result['nlNaStatus']}")


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    run_central_banking_demo()


"""
---
Creator: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Email: leogouk@gmail.com
Repository: https://github.com/FractonicMind/TernaryLogic
Successor: support@tl-goukassian.org
DOI 1: 10.1007/s43681-025-00910-6
DOI 2: 10.1007/s43681-026-01124-0
---
"""
