# System State Machine

## "Ternary Logic" (TL) Constitutional State Automaton

**Framework:** "Ternary Logic" (TL) by Lev Goukassian
**ORCID:** 0009-0006-5966-1243
**Repository:** FractonicMind/TernaryLogic
**Spec Version:** 1.0.0-tl-monograph-2026
**Model:** TL Financial and Cyber-Physical State Automaton

---

## Section 1: Overview

The TL System State Machine is the constitutional state automaton governing every operational mode of a TL deployment. It defines five states, the permitted transitions between them, the enforcement actions associated with each transition, and the governance requirements for recovery.

The state machine is constitutional in the strict sense: no transition can occur that violates the Goukassian Vow, the Iron Law (NL=NA), or the Three Immutable Mandates. Every transition is logged before it executes. The NL=NA invariant applies to state transitions themselves: the record of the transition must be committed to the Immutable Ledger before the transition propagates to the actuation layer.

The three core TL states (+1, 0, -1) map to three of the five operational states. The other two states (S0 and S4) are infrastructure states that exist outside the triadic decision space but are governed by the same constitutional constraints.

---

## Section 2: State Definitions

### S0: Boot Integrity Check

**Description:** The system initialization and trust chain verification state. No governance decisions are processed. No actuation is authorized. The system establishes the hardware root of trust, verifies firmware integrity, and confirms the Governance Lane is reachable before entering normal operation.

**Actions:**
- Verify HSM connection (Thales Luna 7 or equivalent, FIPS 140-3 Level 3)
- Extend TPM 2.0 PCRs with firmware measurements (ISO/IEC 11889)
- Verify PUF attestation chain elements 1 and 2 in MT deployments; record `NULL_PUF_DEPLOYMENT` sentinel in Architecture B
- Confirm `TLCapabilityFlags` posture: `pufAttestationMode`, `ditlIntegrated`, `custodianQuorumAttestationEnabled`
- Verify the Goukassian Principle artifacts (lantern, signature, license) are present and valid
- Confirm Governance Lane connectivity; if unavailable, hold in S0 until available or transition to S2 with `GOVERNANCE_LANE_DEGRADED` status
- Commit the initialization log entry (first entry in Merkle accumulator) before transitioning to S1

**Exit condition:** All integrity checks pass and initialization log is committed. Transition to S1 (Active Governance).

**Architecture B behavior:** PUF attestation elements 1 and 2 are replaced by `NULL_PUF_DEPLOYMENT` sentinel. Software enforcement active. All other S0 checks are identical.

---

### S1: Active Governance (The Triad)

**Description:** Normal constitutional operation. The Inference Lane proposes actions through the triadic decision framework. The Governance Lane evaluates, logs, and issues or withholds Permission Tokens. The Commit Gate resolves the two lanes.

**Allowed decisions:**
- Proceed (+1): `stateLabel: "Proceed"`, `processActive: "ProceedAuthorized"`. Requires valid `PermissionToken` with `laneOrigin: "GOVERNANCE_LANE"`. All Eight Pillars certified. Actuation authorized.
- Epistemic Hold (0): `stateLabel: "EpistemicHold"`, `processActive: "GovernancePause"`. Requires `EscrowRecord`. Trade Lock active. Oracle Scan initiated.
- Refuse (-1): `stateLabel: "Refuse"`, `processActive: "RefusalPermanent"`. No `PermissionToken` issued. `refusalIsPermanent: true` by default.

**Dual-Lane Architecture in S1:**

The Inference Lane operates at no more than 2ms WCET (Worst-Case Execution Time) at the 99.99th percentile. It proposes actions through `POST /decisions`. It cannot authorize actuation. The `TLResult.state` field from the Inference Lane is advisory, not authoritative.

The Governance Lane operates at no more than 300ms ceiling with 50ms jitter maximum. It receives the decision vector through `POST /governance-logs`. It verifies, logs, and either issues a `PermissionToken` (Proceed) or records an `EscrowRecord` (Epistemic Hold) or a `TGLF_StateNeg1` record (Refuse). Only a valid `PermissionToken` from the Governance Lane with `laneOrigin: "GOVERNANCE_LANE"` authorizes the actuation layer to fire.

In DITL/MT deployments, the Commit Gate (memristive-gated pass transistor physically in-line on the actuation path) is the physical resolution point. It transitions from HRS (blocking) to LRS (conducting) only when the Governance Lane issues a Proceed decision and the NL=NA write pulse sets the TaOx ReRAM cell to Low Resistance State. In Architecture B, software-layer enforcement substitutes.

The `X-TL-Trace-Id` UUID v4 header is the cryptographic thread connecting both lanes. Every request and response carries it. The `NLNAGovernanceToken` is cryptographically bound to the `X-TL-Trace-Id` of the originating Inference Lane request.

**NL=NA enforcement in S1:** All five layers of the NL=NA stack are active. Any actuation attempt without a valid `PermissionToken` triggers `NLNA_VIOLATION_ERROR` and `GHOST_GOVERNANCE_DETECTED_ERROR`, transitioning immediately to S3.

---

### S2: Epistemic Hold (State 0 / GovernancePause)

**Description:** The system has entered the constitutional State 0. The Goukassian Vow line "Pause when truth is uncertain" governs this state. Uncertainty is not failure; it is constitutional information.

**State identifiers:**
- `stateLabel`: `"EpistemicHold"` (constitutional state identifier)
- `processActive`: `"GovernancePause"` (workflow process name; not a state synonym)
- `currentState`: `0`

**Behavior:**

**Trade Lock:** All actuation is suspended. No assets move. No transactions settle. The Inference Lane may continue computing proposals but the Commit Gate remains in HRS (blocking) in DITL/MT deployments; software enforcement holds all actuation in Architecture B.

**EscrowRecord creation:** An immutable `EscrowRecord` is created with `heldState: 0`, `initiatedAt`, `initiatingDecisionId`, `holdRationale`, `resolutionDeadline`, `immutableLogHash`, `holdDurationMs`, `governanceLaneStatus`, `requiredConditions`, and `windowComparatorReading`. This record is committed to the Immutable Ledger before any escalation proceeds.

**Oracle Scan:** The system queries secondary and tertiary oracles to resolve the ambiguity that triggered the hold. The specific missing data is recorded in `holdRationale` and `requiredConditions`.

**Governance Lane status:** `governanceLaneStatus.stage` and `percentComplete` update as the Governance Lane processes the hold. The Lantern's `compliancePosture` is `"EPISTEMIC_HOLD_ACTIVE"`. All eight `pillarStatuses` are updated.

**Gateway behavior:** The TL Gateway enters `EPISTEMIC_HOLD_OVERRIDE_ACTIVE`. `epistemicHoldOverride: true`. Fail-closed: the Gateway does not pass traffic to the actuation layer.

**Forced continuation:** Constitutionally prohibited. Any attempt to force Proceed (+1) from S2 triggers C-004 (Hold Violation) and transitions to S3 (Freeze). The `EmergencyOverrideRequest.forcedState` enum prohibits +1; only -1 and 0 are accepted by schema validation.

**Visual indicator:** `Lantern.compliancePosture: "EPISTEMIC_HOLD_ACTIVE"`. This is the constitutional Lantern artifact (Goukassian Principle, `artifactName: "lantern"`), not a UI display element.

**Exit:** Requires resolution by the Governance Lane. Valid resolution states are +1 (Proceed) or -1 (Refuse). State 0 is not a valid resolution. Resolution must occur before `resolutionDeadline`. Timeout without resolution triggers `EPISTEMIC_HOLD_TIMEOUT_ERROR` and transitions to S3 or S1 with `stateLabel: "Refuse"` per governance policy.

---

### S3: Freeze (Constitutional Trap State)

**Description:** A shutdown trigger from the H-series, C-series, or D-series has fired. The system has detected a malicious action, systemic failure, hardware integrity breach, or constitutional violation. The system is constitutionally frozen.

**Properties:**

**Liquidity Cut:** All wallets, accounts, and settlement positions are locked. The Commit Gate transitions to HRS (blocking) in DITL/MT deployments and remains there until a valid `UNFREEZE_TOKEN_SCHEMA` record is presented to the Governance Lane. In Architecture B, software enforcement locks all actuation paths.

**Death Gasp:** The complete governance state is dumped to WORM (Write-Once Read-Many) storage before the freeze propagates. The `SHUTDOWN_RECORD_SCHEMA` record is committed to the Immutable Ledger. `lastLogHash` and `merkleRootAtFreeze` ensure no governance history is lost at the freeze boundary.

**Beacon:** The system broadcasts `GHOST_GOVERNANCE_DETECTED_ERROR` or the relevant `tlErrorCode` to regulatory nodes if the trigger is C-series. For C-005 (Regulatory Bypass), mandatory regulatory notifications are sent and recorded in `SHUTDOWN_RECORD_SCHEMA.regulatoryNotifications`.

**Access constraint:** No local administrative action can unlock S3. The `UNFREEZE_TOKEN_SCHEMA` multi-party authorization token is required. Local admin credentials do not constitute a valid unfreeze mechanism. This constraint is enforced constitutionally, not by software policy alone.

**Governance logging:** The S3 entry event is itself logged as a `TGLF_StateNeg1` record (for FATAL triggers) or a `TGLF_State0` record (for HIGH triggers that produce Epistemic Hold before full freeze). The Immutable Ledger commitment occurs before S3 is fully entered.

---

### S4: Recovery Audit

**Description:** Restricted forensic accounting mode. The system has received a valid `UNFREEZE_TOKEN_SCHEMA` record from the required multi-party authorities. Read access to governance logs is enabled for forensic reconstruction. No new actuation is authorized. The system operates in the most restrictive constrained mode.

**Permitted operations:**
- `GET /governance-logs/{logId}`: Read governance log entries for audit
- `GET /governance/verifications/merkle/{merkleRoot}`: Verify Merkle anchors
- `GET /governance/verifications/inclusion/{logId}`: Verify log inclusion proofs
- `GET /regulator/timestamp-verification/{logId}`: Verify RFC 3161 timestamps
- `GET /governance/compliance/attestation`: Retrieve compliance attestation

**Prohibited operations:**
- All `POST` endpoints producing actuation or new governance decisions
- `POST /decisions`, `POST /governance-logs`, `POST /evaluate/*`

**Recovery path:** Depending on `SHUTDOWN_RECORD_SCHEMA.recoveryPath`:
- `RECOVERY_AUDIT`: S4 is the terminal state until Tri-Cameral governance votes to restore S1
- `UNFREEZE_TOKEN_REQUIRED`: A new `UNFREEZE_TOKEN_SCHEMA` record with the required authority signatures authorizes transition back to S0 (re-initialization)
- `CONSTITUTIONAL_REVIEW`: Full Tri-Cameral governance review required before any transition

---

## Section 3: Transition Logic

| From State | Event | To State | Governance Action |
|------------|-------|----------|-------------------|
| **S0** | All integrity checks pass; initialization log committed | **S1** | `TGLF_StateP1` initialization record committed; `TLCapabilityFlags` set |
| **S0** | Governance Lane unreachable at boot | **S2** | Epistemic Hold; `EscrowRecord` with `GOVERNANCE_LANE_DEGRADED`; Gateway fail-closed |
| **S0** | H-series trigger during boot (hardware integrity failure) | **S3** | `SHUTDOWN_RECORD_SCHEMA` committed; WORM dump; freeze |
| **S1** | `TLResult.confidence` below `ThresholdProfile.holdThreshold` | **S2** | `TGLF_State0` committed; `EscrowRecord` created; GovernancePause workflow |
| **S1** | Conflicting inputs; incomplete data; regulatory flag (non-FATAL) | **S2** | Same as above |
| **S1** | C-006 Flash Crash Resonance | **S2** | `EscrowRecord` with `holdRationale.pillarImplicated: "EpistemicHold"`; circuit breaker active |
| **S1** | Any FATAL or CRITICAL trigger (H, C, D series) | **S3** | `SHUTDOWN_RECORD_SCHEMA` committed; Liquidity Cut; Death Gasp; Beacon |
| **S2** | Governance Lane resolution: Proceed (+1) | **S1** | `TGLF_StateP1` committed; `PermissionToken` issued; Commit Gate opens |
| **S2** | Governance Lane resolution: Refuse (-1) | **S1** | `TGLF_StateNeg1` committed; `refusalIsPermanent: true`; no `PermissionToken` |
| **S2** | C-004 Hold Violation (forced continuation attempt) | **S3** | `SHUTDOWN_RECORD_SCHEMA` with `triggerId: "C-004"`; immediate freeze |
| **S2** | `EPISTEMIC_HOLD_TIMEOUT_ERROR` (resolutionDeadline passed) | **S3** | `SHUTDOWN_RECORD_SCHEMA` committed; timeout recorded |
| **S2** | Any FATAL or CRITICAL trigger (H, C, D series) | **S3** | Identical to S1 to S3 path |
| **S3** | Valid `UNFREEZE_TOKEN_SCHEMA` multi-party token presented | **S4** | Unfreeze record committed to Immutable Ledger; audit port enabled |
| **S4** | Tri-Cameral governance vote to restore operations | **S0** | Full re-initialization required; new boot integrity check |

---

## Section 4: Prohibited Transitions

The following transitions are constitutionally blocked and will be rejected at the schema, enforcement, or on-chain layer:

| Attempted Transition | Blocking Mechanism | Error Code |
|----------------------|-------------------|------------|
| S2 to S1 via forced Proceed (+1) | `EmergencyOverrideRequest.forcedState` enum rejects +1 at schema layer; C-004 fires | `NLNA_VIOLATION_ERROR` |
| S1 or S2 to S1 without PermissionToken | Layer 1 StateEnvelope if/then; Layer 5 `registerPermissionToken` revert | `NLNA_VIOLATION_ERROR` |
| S3 to S1 without valid UNFREEZE_TOKEN_SCHEMA | Actuation layer locked; no Permission Token issuable | `GHOST_GOVERNANCE_DETECTED_ERROR` |
| Any state to any state without committed log | NL=NA Iron Law; all five enforcement layers | `DECISION_LOG_VIOLATION_ERROR` |
| Any state: emitting `stateLabel: "Halt"` | Schema validation; `TLStateLabel` enum prohibits "Halt" | Schema validation error |

---

## Section 5: Architecture B State Machine Behavior

All five states operate identically in Architecture B with the following substitutions:

**S0:** PUF attestation elements 1 and 2 replaced by `NULL_PUF_DEPLOYMENT` sentinel. All other boot integrity checks identical.

**S1:** Commit Gate physical enforcement (TaOx ReRAM, Window Comparator) replaced by software-layer actuation gate. `EscrowRecord.windowComparatorReading.softwareEnforcementActive: true` in all S2 transitions.

**S2:** `EscrowRecord.windowComparatorReading.readingAvailable: false`. Software enforcement active. All other S2 behavior identical.

**S3:** H-series hardware triggers that reference voltage rails or Window Comparator readings use software enforcement substitutes. All C-series and D-series triggers are identical. `pufAttestation: "NULL_PUF_DEPLOYMENT"` in `SHUTDOWN_RECORD_SCHEMA`.

**S4:** Identical in both architectures.

---

## Section 6: State Machine Formal Properties

The following model-checked properties must hold for any correct TL deployment:

**Safety:** `AG(state IN {S0, S1, S2, S3, S4})`, No reachable state falls outside the defined set.

**Liveness:** `AG(trigger_detected IMPLIES AF(S3_entered))`, Every detected trigger eventually reaches S3 within its specified latency bound.

**NL=NA invariance:** `AG(actuation_authorized IMPLIES log_committed)`, On all paths, actuation authorization implies prior log commitment.

**Hold resolution:** `AG(S2_entered IMPLIES AF(S1_OR_S3))`, Every Epistemic Hold is eventually resolved to Active Governance or Freeze, never remaining in State 0 indefinitely.

**No forced Proceed:** `AG(NOT(forcedState_equals_plus1))`, The forcedState +1 transition never occurs in any reachable execution.
