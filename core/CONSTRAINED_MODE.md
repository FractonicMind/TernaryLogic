# Constrained Mode

## "Ternary Logic" (TL) Degraded Operational Specification

**Framework:** "Ternary Logic" (TL) by Lev Goukassian
**ORCID:** 0009-0006-5966-1243
**Repository:** FractonicMind/TernaryLogic
**Spec Version:** 1.0.0-tl-monograph-2026

---

## Section 1: Overview

Constrained Mode is the operational posture of a TL deployment when one or more enforcement layers are operating below their full constitutional specification. It is not a failure state. It is a documented, honest, and governance-logged condition in which the system continues to operate within its constitutional boundaries while recording exactly which enforcement mechanisms are active and which are pending.

Constrained Mode has two distinct forms:

**Architecture B (Software Enforcement):** The SHIPPING baseline for all current TL deployments. DITL/MT silicon is not yet fabricated. The five-layer NL=NA enforcement stack operates fully via software. The `NULL_PUF_DEPLOYMENT` sentinel records this posture in every audit log.

**Epistemic Hold (State 0):** The constitutional state triggered when uncertainty, conflicting data, or constitutional conditions prevent a definitive Proceed or Refuse determination. The system enters a mandatory governance pause. All actuation is suspended. No assets move.

Both forms are first-class constitutional conditions. Neither is an error. Both are fully logged before any downstream action is permitted.

---

## Section 2: Architecture B, Current SHIPPING Baseline

### 2.1 What Architecture B Is

Architecture B is software enforcement with DITL attestation where available. It is the honest deployment posture for all TL instances where DITL/MT physical silicon has not yet been fabricated and installed.

DITL/MT has been demonstrated at transistor simulation level (IBM PDK 1.2V 130nm CMOS). No fabricated DITL chip exists as of the current specification version. Architecture B records this gap honestly rather than pretending it does not exist.

The following `TLCapabilityFlags` are set in all Architecture B deployments:

```json
{
  "pufAttestationMode": "ARCHITECTURE_B",
  "ditlIntegrated": false,
  "custodianQuorumAttestationEnabled": false
}
```

### 2.2 What Is and Is Not Operative in Architecture B

**Fully operative (Layers 1 through 4 of the five-layer NL=NA stack):**

Layer 1: `StateEnvelope` if/then constraint enforcing `permissionToken` when `currentState` equals 1.
Layer 2: `PermissionToken.laneOrigin` const `"GOVERNANCE_LANE"` enforced at schema level.
Layer 3: `TGLF_StateP1.permissionToken` in required array, `pillarsCertified` minItems 8.
Layer 4: `GovernanceProof.logHash` and `merkleRoot` cross-reference with `PermissionToken` enforced at request handler.

**Fully operative (Layer 5):**

Layer 5: `TL_Ledger_Core.registerPermissionToken` on-chain enforcement is unchanged. `NLNAViolation` revert is active.

**Fully operative (PUF Attestation Chain elements 3 through 5):**

Element 3: NL=NA interlock verification via software enforcement.
Element 4: Immutable log entry with `NULL_PUF_DEPLOYMENT` sentinel.
Element 5: Merkle hash chain construction and anchoring.

**Pending fabrication (Architecture B compensating controls active):**

Physical Window Comparator: replaced by `windowComparatorReading.softwareEnforcementActive: true` in `EscrowRecord`.
Physical Commit Gate (TaOx ReRAM pass transistor): replaced by software-layer actuation gate.
NL=NA write pulse (dedicated hardware wire): replaced by software-layer enforcement path.
PUF attestation chain elements 1 and 2: replaced by `NULL_PUF_DEPLOYMENT` sentinel.

### 2.3 NLNAGovernanceToken in Architecture B

Every `NLNAGovernanceToken` issued in an Architecture B deployment MUST carry:

```json
{
  "pufAttestation": "NULL_PUF_DEPLOYMENT",
  "laneStatus": "committed"
}
```

The sentinel value `"NULL_PUF_DEPLOYMENT"` is not a placeholder or an error code. It is a constitutional declaration that the deployment is operating in Architecture B and that PUF-bound hardware attestation is not yet available. This sentinel maintains schema integrity without silently omitting the field.

### 2.4 EscrowRecord in Architecture B

Every `EscrowRecord` generated during Epistemic Hold in an Architecture B deployment MUST carry:

```json
{
  "windowComparatorReading": {
    "readingAvailable": false,
    "softwareEnforcementActive": true
  }
}
```

The `readingAvailable: false` field confirms that physical TaOx ReRAM resistance measurement is not available. The `softwareEnforcementActive: true` field confirms that software-layer enforcement is substituting. Both fields together constitute an honest and auditable record of the deployment posture at the moment of Epistemic Hold entry.

### 2.5 Transition from Architecture B to Full Silicon Enforcement

When DITL/MT silicon becomes available, the transition from Architecture B to full silicon enforcement requires:

- `TLCapabilityFlags.pufAttestationMode` updated from `"ARCHITECTURE_B"` to `"FULL_PUF"`
- `TLCapabilityFlags.ditlIntegrated` updated to `true`
- `NLNAGovernanceToken.pufAttestation` populated with actual PUF binding hash: `SHA3-256(K_PUF || device_serial_OTP || log_session_nonce)`
- `EscrowRecord.windowComparatorReading.readingAvailable` updated to `true` with `resistanceRangeOhm` populated

No changes to Layers 1 through 5 of the NL=NA stack are required. The constitutional enforcement architecture is identical. Only the hardware attestation layer changes.

This transition is a governance event requiring Technical Council proposal and Stewardship Custodian ratification per the standard upgrade workflow.

---

## Section 3: Epistemic Hold (State 0), Constitutional Pause

### 3.1 What Epistemic Hold Is

Epistemic Hold is the TL constitutional State 0. It represents the system's honest determination that truth has not yet been established. The Goukassian Vow line "Pause when truth is uncertain" is the constitutional basis for State 0. Uncertainty is not failure; it is constitutional information.

Epistemic Hold is:
- A first-class constitutional state with `stateLabel: "EpistemicHold"`
- Never null, error, false, timeout, pending, or retry
- A mandatory determination, not an optional fallback
- Activating the `GovernancePause` workflow process (`processActive: "GovernancePause"`)
- Persisting across power cycles in MT hardware deployments without software reinitialization

Epistemic Hold is not:
- A synonym for `GovernancePause` (which is the workflow name, not the state name)
- A degraded or broken condition
- Bypassable by any administrative privilege, software override, or Emergency Override

### 3.2 Operational Limits During Epistemic Hold

When the system enters Epistemic Hold, the following operational limits apply immediately and without exception:

**Trade Lock:** No actuation fires. No assets move. No transactions settle. The actuation layer is suspended pending Governance Lane resolution. The Inference Lane may continue computing proposals, but no Proceed authorization is issued until the Governance Lane resolves the hold.

**EscrowRecord Creation:** An `EscrowRecord` is created at hold initiation and is immutable. It carries:
- `escrowId`: UUID v4 identifying this specific hold instance
- `heldState: 0`: const confirming the constitutional state
- `initiatedAt`: ISO 8601 timestamp of hold entry
- `initiatingDecisionId`: UUID linking to the decision that triggered the hold
- `holdRationale`: rationale string, `uncertaintyScore`, and `pillarImplicated`
- `resolutionDeadline`: constitutional deadline; Tri-Cameral governance bodies may not indefinitely defer
- `immutableLogHash`: SHA-256 hash of the committed log entry
- `holdDurationMs`: elapsed duration since initiation
- `governanceLaneStatus`: stage and percentComplete of Governance Lane processing
- `requiredConditions`: array of conditions that must be met before resolution
- `windowComparatorReading`: hardware or software enforcement posture at hold initiation

**Oracle Scan:** The system queries secondary and tertiary oracles to resolve the data conflict that triggered the hold. Specific missing data or conflicting signals are recorded in the `holdRationale` field and in `requiredConditions`.

**Transparency (Proof of Hold):** The system publishes a `TGLF_State0` record to the Immutable Ledger citing the specific triggering condition, the `pillarImplicated`, the `uncertaintyScore`, and the `resolutionDeadline`. This record is cryptographically sealed, Merkle-anchored, and admissible as governance evidence. The `Lantern.compliancePosture` transitions to `"EPISTEMIC_HOLD_ACTIVE"` and all eight `pillarStatuses` are updated.

**Gateway Behavior:** The TL Gateway enters `EPISTEMIC_HOLD_OVERRIDE_ACTIVE` status. `epistemicHoldOverride: true` is set. The Gateway is fail-closed: it does not pass traffic to the actuation layer. All pending decisions are held in Epistemic Hold until the Governance Lane restores.

### 3.3 Trigger Conditions

Epistemic Hold is mandatory under any of the following conditions:

**Insufficient confidence:** The Inference Lane's `TLResult.confidence` score falls below the configured `ThresholdProfile.holdThreshold` for the active domain (trade, policy, supply-chain, or general).

**Conflicting inputs:** Two or more input signals provide mutually inconsistent data that cannot be reconciled within the Governance Lane's 300ms ceiling. The conflict is quantified and recorded in `holdRationale`.

**Incomplete data:** Required input fields are missing, corrupted, or stale beyond the configured freshness bound. The schema violation is recorded in `holdRationale.pillarImplicated`.

**Regulatory flag:** Any `RegulatoryFlags` entry with `severityLevel: "CRITICAL"` that does not rise to `REFUSE_TRIGGER` level triggers Epistemic Hold pending review.

**Governance Lane unavailability:** If the Governance Lane cannot be reached, the Gateway defaults to Epistemic Hold. Fail-open is constitutionally prohibited.

**C-004 Hold Violation attempt:** Any attempt to force execution while in Epistemic Hold immediately escalates the hold to a C-004 shutdown trigger and transitions the system toward Refuse.

### 3.4 Epistemic Hold Resolution

Resolution of Epistemic Hold requires a terminal state declaration of either +1 (Proceed) or -1 (Refuse). State 0 is not a valid resolution. This constraint is enforced at three layers:

`PATCH /epistemic-hold/escalations/{escalationId}` accepts `resolvedState` with enum `[1, -1]`. State 0 is rejected at the HTTP layer.

`TL_Ledger_Core.resolveEpistemicHoldSystemWide` reverts `InvalidResolutionState` for any value other than REFUSE (0 in uint8 ABI encoding) or PROCEED (1 in uint8 ABI encoding).

`resolutionDeadline` in `EscrowRecord` enforces a constitutional deadline. Tri-Cameral governance bodies may not indefinitely defer.

### 3.5 Forced Continuation Prevention

No administrative privilege, software override, Emergency Override, or external timing pressure can force continuation from Epistemic Hold to Proceed without a valid `PermissionToken` issued by the Governance Lane. Any attempt to bypass Epistemic Hold constitutes a C-004 Hold Violation and triggers immediate system freeze.

The Emergency Override mechanism (`POST /emergency/override`) accepts `forcedState` values of `-1` or `0` only. `forcedState: 1` (forced Proceed) is constitutionally blocked and will be rejected by schema validation.

---

## Section 4: Constrained Mode Governance Logging

All Constrained Mode conditions are logged before any downstream action is permitted. This is the NL=NA invariant applied to the constrained condition itself: the system's honest declaration that it is in a degraded or hold state must be committed to the Immutable Ledger before any governance action proceeds from that state.

**Architecture B deployment logging:** Every governance log entry carries `NULL_PUF_DEPLOYMENT` in `pufAttestation` and `ARCHITECTURE_B` in capability flags. This creates a complete, honest, auditable record of every decision made under software-only enforcement.

**Epistemic Hold logging:** Every `TGLF_State0` record is committed to the Immutable Ledger before the `GovernancePause` workflow initiates any escalation. The `immutableLogHash` in the `EscrowRecord` is the cryptographic proof of prior commitment.

**Recovery logging:** When Architecture B transitions to full DITL/MT enforcement, the transition is itself a governance event that is logged to the Immutable Ledger with a `TriCameralApproval` record, before the new enforcement posture is activated.

---

## Section 5: Constrained Mode Error Codes

The following `tlErrorCode` values from `TLProblemDetail` are associated with Constrained Mode conditions:

| Error Code | Condition | Default State |
|------------|-----------|---------------|
| `WINDOW_COMPARATOR_FAILURE_ERROR` | Physical Window Comparator unavailable (Architecture B) | Epistemic Hold |
| `EPISTEMIC_HOLD_TIMEOUT_ERROR` | Resolution deadline passed without Tri-Cameral action | Refuse |
| `NLNA_VIOLATION_ERROR` | Actuation attempted without valid PermissionToken | Refuse |
| `GHOST_GOVERNANCE_DETECTED_ERROR` | Governance action without immutable evidence | Refuse or Epistemic Hold |
| `PILLAR_VIOLATION_ERROR` | One or more Pillars not certified in TGLF_StateP1 | Refuse |
| `QUORUM_NOT_MET_ERROR` | Governance resolution attempted without quorum | Epistemic Hold |

All error responses carry `x-tl-state` (never omitted), `x-tl-pillar`, and `x-tl-trace-id` as mandatory fields per RFC 7807 with TL extensions.
