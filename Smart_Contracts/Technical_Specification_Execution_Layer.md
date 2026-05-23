# Specification: The Ternary Logic (TL) Smart Contract Execution Layer

**Framework:** "Ternary Logic" (TL) by Lev Goukassian
**ORCID:** 0009-0006-5966-1243
**DOI:** 10.1007/s43681-025-00910-6
**DOI:** 10.1007/s43681-026-01124-0

---

## 1. Core Architectural Principles

The Ternary Logic (TL) framework is an operational governance and economic system designed to enforce accountability and transparency through a set of core architectural principles. These principles are instantiated in smart contracts to create a robust and verifiable system for managing value and state transitions. The framework is built upon three operational states, eight architectural pillars, a governance trinity, and four hard constraints, collectively forming a comprehensive system that moves from trust-based promises to cryptographic verification.

The design prioritizes value management and state enforcement, ensuring that every action is recorded, auditable, and governed by a clear set of rules. The system's architecture is platform-agnostic, with a primary focus on Ethereum and its ecosystem, with considerations for adaptation to other blockchain platforms including Bitcoin and Polygon. The ultimate goal is to create "constitutional code" where the rules of economic interaction are embedded in immutable and transparent smart contracts, making them harder to break than traditional legal agreements.

In the V2.0 implementation, the Dual-Lane Latency Architecture (DLLA) establishes the timing framework within which all state transitions occur. The Inference Lane operates with a 2ms WCET hard ceiling at the 99.99th percentile. The Governance Lane operates with a 300ms hard ceiling and 50ms jitter maximum. The execution gate does not release until the Governance Lane confirms log completion and a valid PermissionToken has been registered on-chain via `TL_Ledger_Core.registerPermissionToken` (NL=NA Layer 5).

### 1.1. The Three Operational States

The Ternary Logic system is fundamentally defined by three distinct operational states that govern the flow of assets and the finality of transactions. These states — **Proceed (+1)**, **Epistemic Hold (0)**, and **Refuse (-1)** — provide a more nuanced and secure model for transaction processing compared to the binary success/failure outcomes of traditional smart contracts.

The introduction of the **Epistemic Hold** state is a key innovation, creating a deliberate constitutional pause in execution to allow for verification and dispute resolution, thereby mitigating risks associated with uncertainty and incomplete information. This ternary model ensures that the system does not default to a potentially harmful "fail-open" or "fail-closed" state in the face of ambiguity, but instead enters a controlled, escrow-like state pending further input.

In the V2.0 smart contract implementation, states are stored as `int8` values in `TL_Evidence_Vault.sol`:
- `+1` = Proceed
- `0` = Epistemic Hold
- `-1` = Refuse

When a transaction's evidence has not yet been archived, `getTransactionState()` returns `0` (Epistemic Hold) as the fail-closed default. This is the NL=NA invariant in action: `G(execute implies P(escrow_recorded and auditable))`.

#### 1.1.1. State (+1): Proceed

The **Proceed** state, represented numerically as **(+1)**, signifies the successful and final confirmation of a transaction. When a transaction enters this state, all predefined conditions have been met, all necessary verifications have been completed, and the system has reached a state of cryptographic certainty. In financial terms, this state corresponds to the finalization of an asset transfer.

In the V2.0 implementation, a Proceed state requires:
1. A valid `PermissionToken` issued by the Governance Lane with `laneOrigin == keccak256("GOVERNANCE_LANE")` (NL=NA Layer 2)
2. The `PermissionToken.logHash` provably included in an anchored Merkle root (NL=NA Layer 5)
3. `TL_Ledger_Core.registerPermissionToken()` successfully called on-chain

A Proceed authorization without a registered PermissionToken is Ghost Governance — execution without immutable audit evidence — and is constitutionally prohibited.

#### 1.1.2. State (0): Epistemic Hold

The **Epistemic Hold** state, represented as **(0)**, is a cornerstone of the Ternary Logic framework. It is a constitutional pause — not an administrative override, not a timeout, not an error state. It is a first-class constitutional state with its own identity, its own mandatory process, and its own immutable record.

The Epistemic Hold is triggered when there is a predefined level of uncertainty or risk associated with a transaction: conflicting oracle data, a detected anomaly, a dispute raised by a stakeholder, or the absence of sufficient information to make a definitive Proceed or Refuse determination. When the system encounters such a situation, it transitions to the Epistemic Hold state, locking associated assets in escrow pending resolution.

The Epistemic Hold carries no fee by constitutional design. Charging for a constitutional pause creates a perverse incentive to avoid holds. Holds protect the system's users and the integrity of its governance record. They are free.

Resolution of the Epistemic Hold requires a determination of either Proceed (+1) or Refuse (-1). Re-resolution to Epistemic Hold (0) is constitutionally prohibited. In `TL_Ledger_Core.sol`, `resolveEpistemicHoldSystemWide()` reverts `InvalidResolutionState` for any value other than `uint8(0)` (encoding Refuse) or `uint8(1)` (encoding Proceed).

In the V2.0 API specification, the Epistemic Hold is implemented as `EscrowRecord_v1_0_0` with `processActive` const `"GovernancePause"`. The Governance Lane hard ceiling of 300ms is the physical interval between intent and irreversible action.

#### 1.1.3. State (-1): Refuse

The **Refuse** state, represented as **(-1)**, is the definitive rejection of a transaction. This state is reached when the conditions for proceeding are not met, a dispute is resolved against the transaction's initiator, or a critical failure occurs that prevents the transaction from being completed safely. In financial terms, the Refuse state results in the reversion of the transaction, with any assets that were to be transferred being returned to their original owners.

The Refuse state is permanent by default. A refused transaction cannot be directly re-approved; it must be re-initiated as a new proposal following the standard state transition path.

### 1.2. The Eight Architectural Pillars

The Ternary Logic framework is constructed upon eight foundational pillars that collectively define its technical implementation and operational characteristics. These pillars are not merely abstract principles but are implemented as concrete logic within the smart contract code. The pillars work in concert to create a system that is resilient, auditable, and resistant to both technical failures and malicious manipulation.

#### 1.2.1. Pillar 1: Epistemic Hold

The **Epistemic Hold** pillar is the technical implementation of the system's ability to pause execution in the face of uncertainty. This is not an administrative `pause()` function controlled by a central authority, but a logic gate automatically triggered by specific, predefined conditions related to data quality, risk, or ambiguity.

For example, a smart contract managing a supply chain might enter an Epistemic Hold if an IoT sensor reports a temperature deviation for a shipment of perishable goods. The contract locks the payment and awaits further input — a signed report from a third-party inspector or a consensus from a network of oracles.

In the V2.0 implementation, `TL_Evidence_Vault.sol` enforces the Epistemic Hold as the fail-closed default. Any transaction whose evidence has not been archived returns `int8(0)` from `getTransactionState()`. The Governance Lane must complete log confirmation and PermissionToken registration before any Proceed state can be recognized on-chain.

#### 1.2.2. Pillar 2: Immutable Ledger

The **Immutable Ledger** pillar ensures that the history of all decisions and state changes is permanently and transparently recorded. Every significant action, particularly state transitions between (+1), (0), and (-1), must be accompanied by a corresponding event emission.

In the V2.0 implementation, this is enforced through `TL_Evidence_Vault.sol`, which writes all evidence records as write-once entries. Any overwrite attempt reverts `ImmutabilityViolation`. Every `archiveEvidence` call includes a `traceId` field corresponding to the `X-TL-Trace-Id` UUID v4 header from the originating API request, enabling end-to-end traceability from the Inference Lane through the Governance Lane to the on-chain record.

The immutability of the blockchain ensures that this ledger of events is tamper-proof, providing a permanent record for regulatory compliance, forensic analysis, and public accountability.

#### 1.2.3. Pillar 3: Goukassian Principle

The **Goukassian Principle** is a core safety mechanism that dictates the system's behavior in the presence of ambiguity or uncertainty. It is a logic gate that defaults to the **Epistemic Hold (0) state** rather than allowing the system to "Fail Open" (proceed with a potentially risky transaction) or "Fail Closed" (revert without a clear reason).

In Solidity, this is implemented as a default case in conditional logic or a `require` statement that checks for the completeness and validity of input data. If an oracle provides a stale or outlier value, instead of reverting the transaction or proceeding with bad data, the function triggers a transition to the Epistemic Hold state. The system remains in a safe, non-committal state until the ambiguity can be resolved through a defined process.

The three properties of the Goukassian Principle are:
- **Lantern** — the system's purpose and decision logic must be visible and auditable at all times
- **Signature** — every decision carries an immutable record of the authorizing agent
- **License** — the system operates only within constitutionally defined boundaries

#### 1.2.4. Pillar 4: Decision Logs

The **Decision Logs** pillar mandates that every state change within the system must be accompanied by a corresponding log entry. This is a strict requirement that ensures complete transparency and traceability of all actions. The **No Log = No Action** invariant enforces this pillar: `G(execute implies P(escrow_recorded and auditable))`.

In the V2.0 implementation, Decision Log entries are stored in `TL_Evidence_Vault.sol` via `archiveEvidence()`. Each entry captures: transaction hash, evidence URI, submitter address, final state (int8), Merkle root, lane origin hash, PermissionToken ID, trace ID, and escrow record ID. This creates a rich, queryable history of all decisions usable for auditing, dispute resolution, and analysis.

#### 1.2.5. Pillar 5: Economic Rights and Transparency

The **Economic Rights and Transparency** pillar is implemented through a set of public `view` functions that provide unrestricted access to the smart contract's state and financial data. This ensures that all stakeholders can independently verify the system's operations and audit the flow of assets. These functions do not modify the state of the contract and can be called without incurring gas costs.

In `TL_Evidence_Vault.sol`, `getEvidence()`, `evidenceExists()`, `getTransactionState()`, and `isMerkleRootAnchored()` are all public view functions providing open access to the governance record.

#### 1.2.6. Pillar 6: Sustainable Capital Allocation

The **Sustainable Capital Allocation** pillar is designed to prevent the drainage of a treasury or the depletion of a shared resource. This is achieved through smart contract constraints that limit the rate and amount of withdrawals.

In the V2.0 implementation, the Smart Contract Treasury accumulates TL service fees. All disbursements require Tri-Cameral Joint-Approval: a 75% supermajority independently in both the Technical Council and the Stewardship Custodians. The `proposeDisbursement()` / `approveDisbursement()` / `vetoDisbursement()` pathway in `TL_Ledger_Core.sol` enforces this constraint. No individual can withdraw from the Treasury directly. No admin key exists.

#### 1.2.7. Pillar 7: Hybrid Shield

The **Hybrid Shield** pillar provides a multi-layered defense against corruption and unauthorized control. It combines cryptographic security with institutional oversight through the Tri-Cameral governance model.

The Stewardship Custodians (11 members, 75% quorum — 9 votes) hold binding constitutional veto authority. Their multi-signature requirement ensures that no single custodian can unilaterally make critical decisions. The Technical Council (9 members, 75% quorum — 7 votes) holds exclusive proposal rights but cannot exercise veto authority. The Smart Contract Treasury executes automatically on verified milestones with no admin key.

In `TL_Ledger_Core.sol`, all state-mutating operations require `CustodianAttestation[]` arrays meeting the `CUSTODIAN_THRESHOLD` of 9. Any operation with fewer attestations reverts `QuorumNotMet`.

#### 1.2.8. Pillar 8: Anchors

The **Anchors** pillar connects the TL system's on-chain decisions to real-world events and data, and to the external cryptographic verification infrastructure. Anchors are implemented using Merkle hash chains, OpenTimestamps proofs, and multi-chain anchoring across Bitcoin, Ethereum, and Polygon.

In the V2.0 implementation, `TL_Evidence_Vault.sol` stores anchored Merkle roots via `anchorMerkleRoot()`. `verifyMerkleInclusion()` provides pure on-chain verification of log entry inclusion in any anchored root. The NL=NA Layer 5 gate in `TL_Ledger_Core.registerPermissionToken()` reverts `NLNAViolation` if `logHash` is not provably included in an anchored Merkle root — making the Anchor pillar a constitutional precondition of every Proceed authorization.

### 1.3. The Governance Trinity

The governance of the Ternary Logic system is structured around a **Governance Trinity**, a tripartite model designed to distribute power and prevent any single entity from gaining unilateral control. This model consists of three distinct bodies: the Technical Council, the Stewardship Custodians, and the Smart Contract Treasury.

#### 1.3.1. Technical Council

The **Technical Council** is responsible for the technical maintenance and evolution of the TL framework. It consists of 9 members operating with a 75% quorum (7 votes). The Council holds exclusive proposal rights — it is the only body authorized to originate governance proposals. It cannot exercise veto authority over anything it proposes.

Key responsibilities: preserving and updating core specifications and cryptographic standards; proposing and implementing code upgrades; commissioning external security audits; ensuring interoperability with other platforms. Any upgrades proposed by the Council are subject to review and potential veto by the Stewardship Custodians before activation.

#### 1.3.2. Stewardship Custodians

The **Stewardship Custodians** are the ethical and legal guardians of the Ternary Logic framework. They consist of 11 members operating with a 75% quorum (9 votes). The Custodians hold binding constitutional veto authority over all Technical Council proposals. They cannot originate proposals.

Key responsibilities: enforcing the "No Spy" and "No Weapon" mandates; certifying compliant operators; revoking certification for violations; arbitrating escalated disputes; reviewing and vetoing Technical Council proposals; approving or vetoing disbursement proposals from the Treasury.

In `TL_Ledger_Core.sol`, Stewardship Custodian authority is enforced through `CustodianAttestation[]` arrays on all state-mutating operations. The veto in `vetoDisbursement()` is permanent and cannot be reversed.

#### 1.3.3. Smart Contract Treasury

The **Smart Contract Treasury** is the autonomous financial backbone of the Ternary Logic system. It is a smart contract that holds the funds for the project and is responsible for their allocation and disbursement. The Treasury operates without human intervention, ensuring that financial decisions are made in a predictable and impartial manner.

In the V2.0 implementation, the Treasury accumulates:
- `permissionTokenFee` — per State +1 PermissionToken registration
- `archiveEvidenceFee` — per governance action archived
- License revenue (off-chain, managed by the Goukassian Foundation)

Both fee parameters are governance parameters labeled **Nomination 2026** — set at deployment as initial values, subject to revision by Tri-Cameral Joint-Approval. Epistemic Hold activation and resolution carry no fee. No admin key exists.

### 1.4. The Four Mandates (Hard Constraints)

The Ternary Logic framework is governed by four hard constraints, or **Mandates**, that are enforced at the smart contract level.

#### 1.4.1. Mandate 1: No Spy

The **No Spy** mandate prohibits the system from engaging in any form of backdoor data collection or surveillance. No function within a TL-governed system may enable surveillance of participants. This mandate is enforced by the Stewardship Custodians and is constitutionally beyond the authority of any governance body to modify.

#### 1.4.2. Mandate 2: No Weapon

The **No Weapon** mandate prohibits the use of the Ternary Logic framework for any purpose designed to cause harm to individuals or society. The protocol and its implementation cannot be turned against any individual or group. The Stewardship Custodians hold authority to revoke the certification of any operator who violates this mandate.

#### 1.4.3. Mandate 3: No Log = No Action

The **No Log = No Action** mandate is the constitutional mechanism ensuring that every action is recorded and auditable before it occurs. Formally in Linear Temporal Logic: `G(execute implies P(escrow_recorded and auditable))`. Any execution that cannot satisfy this invariant does not occur.

In `TL_Ledger_Core.sol`, this is enforced at five independent layers:

| Layer | Location | Mechanism |
| :--- | :--- | :--- |
| Layer 1 | `tl_schema.json` | `StateEnvelope` if/then: State +1 requires `permissionToken` |
| Layer 2 | `PermissionToken.laneOrigin` | `const: "GOVERNANCE_LANE"` — any other value is schema-invalid |
| Layer 3 | `TGLF_StateP1` | `permissionToken` in required array; all Eight Pillars must be certified |
| Layer 4 | `GovernanceProof` | `logHash` and `merkleRoot` must match `PermissionToken` fields |
| Layer 5 | `TL_Ledger_Core.registerPermissionToken` | Reverts `NLNAViolation` if `logHash` not in anchored Merkle root |

Bypassing one layer does not bypass the others. Layer 5 is the terminal constitutional gate.

#### 1.4.4. Mandate 4: No Switch Off

The **No Switch Off** mandate is a commitment to the long-term resilience and decentralization of the Ternary Logic system. It prohibits the inclusion of any mechanism that would allow a single administrator or a small group of administrators to unilaterally terminate or disable the smart contract. This is implemented by the **absence of a `selfdestruct` function** and the absence of any admin key. The Smart Contract Treasury has no pause guardian and no emergency shutdown capability.

---

## 2. Smart Contract as Enforcement Layer

### 2.1. Role of the Smart Contract: The Executioner

In the Ternary Logic (TL) framework, the smart contract serves as the **Executioner** — a term that precisely defines its function within the broader system architecture. It is not an intelligent agent capable of independent thought or decision-making; rather, it is a deterministic and transparent mechanism for enforcing the rules and logic of the TL system. The contract's primary role is to receive a signed input from an external source — an oracle, an AI, or a human — and to execute the corresponding state transition logic (+1, 0, or -1) based on that input.

This clear separation of concerns ensures that the on-chain enforcement layer remains impartial, predictable, and verifiable. The contract's logic is immutable and publicly auditable, meaning that anyone can inspect the code to understand how it will behave in any given situation.

#### 2.1.1. Distinction from the Decision Layer

A critical aspect of the TL architecture is the clear distinction between the **Decision Layer** and the **Enforcement Layer**. The Decision Layer is responsible for gathering and analyzing data, evaluating risks, and ultimately making the decision to Proceed, hold, or Refuse a transaction. This layer can be composed of a variety of components, including off-chain AI models, human experts, or decentralized oracle networks.

The Enforcement Layer is the on-chain smart contract responsible for executing the decision made by the Decision Layer. The contract does not question the validity of the input it receives; it executes the corresponding state transition logic. This separation of concerns prevents the on-chain logic from being manipulated or corrupted by external factors.

In the V2.0 implementation, the Decision Layer is the TL API (Inference Lane + Governance Lane). The Enforcement Layer is `TL_Ledger_Core.sol` + `TL_Evidence_Vault.sol`. The `Data_Bridge.py` connects the two, routing every decision through the full API stack before any on-chain contract interaction.

#### 2.1.2. Handling Signed Inputs from Oracles, AI, or Humans

The TL smart contract is designed to accept signed inputs from a variety of sources, including oracles, AI models, and human users. The signature on the input serves as a cryptographic proof of its authenticity. In the V2.0 implementation, all Governance Lane outputs carry an HSM-signed `PermissionToken` with EIP-712 typed data signatures. The `signatureValue` field in `TL_Ledger_Core.registerPermissionToken()` carries this signature for on-chain verification.

The `NLNAGovernanceToken` security scheme in the API is cryptographically bound to the `X-TL-Trace-Id` of the originating Inference Lane request, preventing token substitution across unrelated decision vectors.

### 2.2. State Machine Architecture (FSM)

The Ternary Logic Smart Contract Execution Layer is fundamentally a deterministic, transaction-based state machine. In the context of TL, the state machine is not merely a ledger of balances but a sophisticated engine for enforcing economic and governance rules. It transitions between a finite set of states based on predefined logic and external inputs.

The core transition function is `f(S, I) -> S'`, where `S` is the current state, `I` is the input, and `S'` is the new state. This deterministic execution guarantees that all nodes processing the same block of transactions will compute the same resulting state, thereby maintaining the integrity and consistency of the distributed ledger.

The TL FSM is defined by three operational states: `Proceed` (+1), `EpistemicHold` (0), and `Refuse` (-1). Each state represents a specific condition of a transaction or proposal, and transitions between these states are governed by strict, immutable rules encoded in the smart contract.

#### 2.2.1. Conceptual FSM Graph

The conceptual FSM for the Ternary Logic system is defined by three primary states and a set of controlled transitions. The `EpistemicHold` (0) state is the most critical and unique aspect of the TL FSM. It acts as a suspension or escrow state, where a transaction is neither finalized nor rejected but is instead locked pending further input.

The `Proceed` (+1) state represents a finalized and successful transaction. The `Refuse` (-1) state signifies a reverted transaction. The `EpistemicHold` (0) state is temporary and resolvable — from this state, the system can transition to either `Proceed` or `Refuse` based on the outcome of the resolution process.

#### 2.2.2. State Transition Logic Table

| Current State | Action | Next State |
| :--- | :--- | :--- |
| `PROCEED` | `SUSPENDED` | `EPISTEMIC_HOLD` |
| `PROCEED` | `REJECTED` | `REFUSE` |
| `EPISTEMIC_HOLD` | `EVIDENCE_RECEIVED` | `PROCEED` |
| `EPISTEMIC_HOLD` | `REJECTED` | `REFUSE` |
| `EPISTEMIC_HOLD` | `TIMEOUT` | `REFUSE` |
| `REFUSE` | `NEW_PROPOSAL` | `PROCEED` |

Note: `EPISTEMIC_HOLD → EPISTEMIC_HOLD` is a forbidden transition. Re-resolution to the Epistemic Hold state is constitutionally prohibited. `resolveEpistemicHoldSystemWide()` in `TL_Ledger_Core.sol` reverts `InvalidResolutionState` for any value other than `uint8(0)` (Refuse encoding) or `uint8(1)` (Proceed encoding).

#### 2.2.3. Forbidden Transitions

The TL state machine is designed with a set of **forbidden transitions** to prevent the system from entering an invalid or unstable state:

1. **`Refuse` → `Proceed` (direct):** Forbidden. A refused transaction must be re-initiated as a new proposal.
2. **`Proceed` → `Refuse` (direct):** Forbidden. A Proceed state is considered final. Any subsequent action must go through the Epistemic Hold.
3. **`EpistemicHold` → `EpistemicHold`:** Forbidden. The Epistemic Hold is a temporary state that must resolve to either Proceed (+1) or Refuse (-1).

#### 2.2.4. Mechanics of the Epistemic Hold (0) State

The `EpistemicHold` (0) state is the cornerstone of the Ternary Logic system's ability to manage uncertainty and enforce a fail-secure posture. When a transaction enters the Epistemic Hold state, any associated assets are locked within the smart contract's escrow. They are neither transferred to the recipient nor returned to the sender — they are effectively frozen until a resolution is reached.

The trigger for entering this state is based on specific, pre-programmed conditions: oracle data quality failures, compliance check failures, Stewardship Custodian review requirements, or the absence of a valid PermissionToken from the Governance Lane.

In `TL_Evidence_Vault.sol`, `activateEpistemicHold()` sets `epistemicHoldActive = true` and records `activeEscrowRecordId` and `epistemicHoldResolutionDeadline`. All subsequent State +1 evidence writes are blocked via the `notUnderEpistemicHold` modifier until `resolveEpistemicHold()` is called with a valid resolution state.

Resolution requires a Tri-Cameral Stewardship Custodian quorum attestation (`CUSTODIAN_THRESHOLD = 9`). The resolution state must be `uint8(0)` (Refuse) or `uint8(1)` (Proceed). Any other value reverts `InvalidResolutionState`.

### 2.3. Failure Modes and the Fail-Secure Zero

The Ternary Logic system is designed with a **fail-secure** philosophy. The core principle is that in the face of uncertainty, ambiguity, or system stress, the default action is to transition to the `EpistemicHold` (0) state. Unlike systems that might fail open (allowing transactions to proceed in error) or fail closed (crashing in a way that could be exploited), the TL system defaults to a state of suspended animation — no irreversible actions are taken when the system's normal operating conditions are not met.

In `TL_Evidence_Vault.sol`, `getTransactionState()` returns `int8(0)` (Epistemic Hold) for any transaction hash with no archived evidence. This fail-closed default is structural, not configurable.

#### 2.3.1. Handling Oracle Failure

When a smart contract requires data from an external source and the oracle fails to deliver, delivers stale data, or delivers data outside expected parameters, the contract triggers a transition to the `EpistemicHold` (0) state. This immediately locks any assets involved, preventing movement or loss based on bad data.

Resolution can involve backup oracles, oracle network consensus, or Stewardship Custodian intervention via multi-signature authority to manually resolve the held transaction.

#### 2.3.2. Mitigating Flash Loan Attacks

Flash loan attacks exploit the atomicity of DeFi transactions to manipulate state within a single block. The TL system's fail-secure design, particularly the `EpistemicHold` state, provides a defense by introducing mandatory delays or external validation requirements that break the atomicity essential for a successful flash loan attack.

A TL-based lending protocol can place any large withdrawal or any transaction that significantly alters a key state variable into an `EpistemicHold` state for a short period. This delay prevents the attacker from completing their exploit within a single transaction. The Governance Lane 300ms ceiling combined with the Merkle anchoring requirement makes same-block manipulation impossible for any transaction routed through the full NL=NA stack.

#### 2.3.3. Defaulting to State 0 (Epistemic Hold) Under Stress

In the event of any type of failure or stress, the system defaults to the `EpistemicHold` state (0) rather than crashing or allowing unauthorized execution. This fail-secure approach ensures that the system always behaves in a predictable and reliable manner under adverse conditions. The Epistemic Hold provides a safe environment for the system to recover, as it prevents any transactions from being executed until the issue has been resolved.

---

## 3. Technical Implementation Specification

### 3.1. Solidity Implementation of Core States

#### 3.1.1. Defining States with `enum`

In Solidity, the three operational states of the Ternary Logic system are best represented using an `enum`. This provides a clean, type-safe, and gas-efficient way to manage the state of a transaction or proposal.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract TernaryLogicSystem {

    // Three operational states of the TL framework
    enum TernaryState {
        Refuse,         // int8(-1) — definitive rejection
        EpistemicHold,  // int8(0)  — constitutional pause, fail-closed default
        Proceed         // int8(+1) — authorized execution
    }

    // Constitutional mapping: enum to int8 TL encoding
    // EpistemicHold = 0, Proceed = 1, Refuse = -1
    // Note: in TL_Evidence_Vault.sol, int8 is used directly.

    // Struct to represent a transaction with a TL state
    struct Transaction {
        uint256 id;
        address initiator;
        uint256 amount;
        TernaryState state;
        bytes32 traceId;       // X-TL-Trace-Id from originating API request
        bytes32 permissionTokenId; // Required for Proceed state
    }

    // Mapping to store transactions by their ID
    mapping(uint256 => Transaction) public transactions;

    // Function to get the state of a transaction
    function getTransactionState(
        uint256 transactionId
    ) public view returns (TernaryState) {
        return transactions[transactionId].state;
    }
}
```

In the V2.0 `TL_Evidence_Vault.sol` implementation, states are stored as `int8` rather than `enum` to allow signed encoding (`-1`, `0`, `+1`). The fail-closed default — returning `int8(0)` (Epistemic Hold) for any unarchived transaction — is enforced in `getTransactionState()`.

#### 3.1.2. State Management and Storage

The management of states within the smart contract's storage is critical. In `TL_Evidence_Vault.sol`, the `EvidenceLog` struct captures the full constitutional record for each state transition:

```solidity
struct EvidenceLog {
    uint256 timestamp;         // block.timestamp at archival
    string  uri;               // IPFS or Arweave evidence link
    address submitter;         // Governance Lane operator address
    int8    finalState;        // TL triadic state: +1, 0, or -1
    bytes32 merkleRoot;        // Batch Merkle root this record belongs to
    bytes32 laneOrigin;        // Must equal keccak256("GOVERNANCE_LANE")
    bytes32 permissionTokenId; // Associated PermissionToken (zero for State 0/-1)
    bytes32 traceId;           // X-TL-Trace-Id UUID v4 from originating API request
    bytes32 escrowRecordId;    // EscrowRecord identifier for State 0 entries
}
```

Every `EvidenceLog` entry is write-once. Any overwrite attempt reverts `ImmutabilityViolation`. This is the Immutable Ledger pillar enforced at the storage layer.

#### 3.1.3. The NL=NA Interlock in Practice

The No-Log-No-Action invariant is enforced through the PermissionToken registration pathway. Before any Proceed authorization can be recognized on-chain, `TL_Ledger_Core.registerPermissionToken()` must be called successfully. This function enforces:

```solidity
// NL=NA Layer 2: Governance Lane origin check
if (laneOriginHash != GOVERNANCE_LANE_HASH) {
    revert NLNAViolation(tokenId, logHash, 1);
}

// NL=NA Layer 5: Merkle inclusion proof
bool included = evidenceVault.verifyMerkleInclusion(
    logHash, merkleRoot, merkleProof
);
if (!included) {
    revert NLNAViolation(tokenId, logHash, 0);
}

// Merkle root must be anchored on-chain
bool anchored = evidenceVault.isMerkleRootAnchored(merkleRoot);
if (!anchored) {
    revert NLNAViolation(tokenId, logHash, 0);
}
```

`NLNAViolation` reverts the entire transaction. No partial state update is possible. Ghost Governance — execution without immutable audit evidence — is structurally impossible once this gate is in place.

#### 3.1.4. The Epistemic Hold in Solidity

The system-wide Epistemic Hold is managed through coordinated state in both `TL_Ledger_Core.sol` and `TL_Evidence_Vault.sol`:

```solidity
// TL_Evidence_Vault.sol — storage
bool public epistemicHoldActive;
bytes32 public activeEscrowRecordId;
uint256 public epistemicHoldResolutionDeadline;

// Modifier blocking State +1 writes under system-wide hold
modifier notUnderEpistemicHold() {
    if (epistemicHoldActive) {
        revert SystemEpistemicHoldActive(activeEscrowRecordId);
    }
    _;
}
```

```solidity
// TL_Ledger_Core.sol — resolution enforcement
function resolveEpistemicHoldSystemWide(
    bytes32 escrowRecordId,
    uint8 resolvedState,   // uint8(1) = Proceed, uint8(0) = Refuse
    bytes32 resolutionRationaleHash,
    CustodianAttestation[] calldata quorumAttestations
) external onlyGovernanceLane
  quorumRequired(quorumAttestations, CUSTODIAN_THRESHOLD)
  returns (bool resolved)
{
    // Epistemic Hold re-resolution is constitutionally prohibited
    if (resolvedState != 0 && resolvedState != 1) {
        revert InvalidResolutionState(resolvedState);
    }
    // ... resolution logic
}
```

#### 3.1.5. Treasury Fee Collection

On-chain fee collection routes through the internal `_collectFee()` function in `TL_Ledger_Core.sol`:

```solidity
function _collectFee(
    bytes32 operationId,
    uint8 feeType,    // 1=PERMISSION_TOKEN, 2=ARCHIVE_EVIDENCE
    uint256 feeAmount
) internal {
    if (feeAmount > 0 && smartContractTreasury != address(0)) {
        require(msg.value >= feeAmount, "TL_Core: Insufficient fee");
        (bool sent,) = smartContractTreasury.call{value: feeAmount}("");
        require(sent, "TL_Core: Fee transfer to treasury failed");
        emit FeeCollected(
            operationId, feeType, feeAmount, msg.sender, block.timestamp
        );
    }
}
```

Fee parameters `permissionTokenFee` and `archiveEvidenceFee` are governance parameters (Nomination 2026), not constants. They are updated via `setFees()` which requires Tri-Cameral Stewardship Custodian quorum.

---

## 4. NL=NA: The Constitutional Enforcement Invariant

The No-Log-No-Action (NL=NA) invariant is the constitutional mechanism that connects the governance architecture to its smart contract implementation. Formally in Linear Temporal Logic:

`G(execute implies P(escrow_recorded and auditable))`

Globally, every execution event was preceded by an escrow-recorded and auditable event. This formulation admits no exceptions. It applies to every execution event without regard for urgency, identity of the authorizing agent, claimed legal authority, or classification level of the environment.

The five enforcement layers work independently. Bypassing one does not bypass the others. The hardware layer (if DITL is deployed) is the terminal gate below Layer 5. See the Constitutional Hardware folder for the full DITL specification.

---

## 5. Immutable Mandates

Three constitutional prohibitions beyond the authority of any governance body created by the TL framework:

- **No Spy** — no function within a TL-governed system may enable surveillance of participants
- **No Weapon** — the protocol and its implementation cannot be turned against any individual or group
- **No Switch Off** — the TL protocol may evolve but cannot be extinguished

Any proposal attempting to modify, suspend, or reinterpret any Immutable Mandate is void from the beginning as if it had never been made, regardless of the governance body from which it originates and regardless of the supermajority that purports to authorize it.
