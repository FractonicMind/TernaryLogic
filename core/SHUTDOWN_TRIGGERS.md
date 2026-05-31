# Shutdown Triggers

## "Ternary Logic" (TL) Constitutional Freeze Trigger Catalog

**Framework:** "Ternary Logic" (TL) by Lev Goukassian
**ORCID:** 0009-0006-5966-1243
**Repository:** FractonicMind/TernaryLogic
**Spec Version:** 1.0.0-tl-monograph-2026
**Enforcement Level:** Governance Lane constitutional gate and, in DITL/MT deployments, Kernel Ring 0 / FPGA Hardware Gate

---

## Section 1: Abstract

This document defines the events that mandate an immediate transition to the FREEZE (S3) state. In a TL deployment, these triggers prevent unconstitutional state transitions from propagating to the actuation layer. Every trigger results in a `SHUTDOWN_RECORD_SCHEMA` record committed to the Immutable Ledger before the freeze propagates. The NL=NA invariant applies to the freeze itself: the evidence of the freeze must exist before the freeze executes.

Three trigger series are defined:

**H-Series (Hardware Integrity):** Govern the physical enforcement substrate. In DITL/MT deployments, these triggers operate at the silicon level via the Window Comparator, Commit Gate, and NL=NA write pulse. In Architecture B deployments, software enforcement is substituted and `windowComparatorReading.softwareEnforcementActive: true` is recorded.

**C-Series (Constitutional Financial Violations):** Enforce the TL constitutional axioms at the governance logic level. These are TL-specific and enforce the Goukassian Vow, the Iron Law (NL=NA), and the framework's financial integrity requirements.

**D-Series (Cryptographic and Data Integrity):** Enforce the cryptographic substrate that underlies all governance evidence. These triggers protect the Immutable Ledger, the Merkle accumulator, and the timestamp integrity of the governance chain.

---

## Section 2: H-Series, Hardware Integrity Triggers

H-series triggers govern the physical and firmware enforcement substrate. The voltage domain mappings reference the DITL/MT hardware architecture: 3.3V for Proceed (+1), 1.65V for Epistemic Hold (0), and 0V for Refuse (-1), encoded in TaOx 1T1R ReRAM on the TSMC N2 CoWoS baseline.

In Architecture B deployments where DITL/MT silicon is not yet fabricated, H-series triggers that reference voltage rails or Window Comparator readings use software enforcement substitutes. The `SHUTDOWN_RECORD_SCHEMA.hardwareContext.windowComparatorReading.softwareEnforcementActive` field confirms the enforcement posture for each H-series event.

| Trigger ID | Trigger Name | Threshold / Condition | Latency | Severity | Architecture B Behavior |
|------------|-------------|----------------------|---------|----------|------------------------|
| **H-001** | Rail Voltage Deviation (Pos) | Positive voltage rail variance greater than 1.5% for more than 3 clock cycles. In DITL/MT: 3.3V (Proceed) rail. | Instant | CRITICAL | Software voltage monitor substitutes; threshold enforced via OS-level sensor |
| **H-002** | Rail Voltage Deviation (Neg) | Negative voltage rail variance greater than 1.5% for more than 3 clock cycles. In DITL/MT: 0V (Refuse) rail. | Instant | CRITICAL | Software voltage monitor substitutes; threshold enforced via OS-level sensor |
| **H-003** | Zero Plane Drift | Epistemic Hold voltage plane (1.65V in DITL/MT; IRS in TaOx ReRAM) registers potential outside the Window Comparator valid window for the IRS range (~100 kΩ to 1 MΩ). RC spoof detection threshold: 5 ns. | Instant | CRITICAL | `windowComparatorReading.softwareEnforcementActive: true`; resistance reading unavailable; software state consistency check substitutes |
| **H-007** | Physical Tamper Mesh | Continuity loss on chassis intrusion detection mesh. HSM FIPS 140-3 tamper-reactive shielding triggers key zeroization. | Instant | CRITICAL | Software tamper detection via OS integrity monitoring; HSM tamper response identical |
| **H-008** | Hardware Anchor Timeout | Failure to receive heartbeat from HSM / TPM within configured interval. TPM 2.0 baseline (ISO/IEC 11889); Thales Luna 7 HSM named baseline. | 10ms | CRITICAL | Identical in Architecture B; HSM heartbeat monitoring is software-equivalent |

### H-Series Technical Notes

**H-003 Window Comparator context:** In DITL/MT deployments, the Window Comparator measures TaOx cell resistance using an independent bandgap reference stable across 0-125 degrees C and supply voltage variation of plus or minus 10 percent. The IRS range for Epistemic Hold (0) is approximately 100 kΩ to 1 MΩ. Any resistance reading outside this window when the system is in State 0 triggers H-003. In Architecture B, the analogous software check is a state consistency verification: the `EscrowRecord.heldState` const of 0 is verified against the governance log at each decision cycle.

**H-007 HSM key zeroization:** Upon physical tamper detection, the HSM immediately zeroizes all Critical Security Parameters. This includes the signing keys for governance log entries and attestation quotes. After zeroization, no new governance log entries can be signed and therefore no new actuation is authorized. The system is constitutionally frozen by the absence of the signing capability, not by a software command.

---

## Section 3: C-Series, Constitutional Financial Violation Triggers

C-series triggers enforce the TL constitutional axioms. The governing axioms are:

- "No Log = No Action" (Iron Law): no actuation without prior committed log entry
- "No Anchor, No Liquidity": no financial execution without cryptographic proof of reserve
- "No Provenance, No Trade": no asset transaction without verified Merkle chain of custody

These triggers are TL-specific and have no equivalent in standard financial risk systems. They represent the constitutional boundaries of the framework.

| Trigger ID | Trigger Name | Threshold / Condition | Latency | Severity | NL=NA Layer |
|------------|-------------|----------------------|---------|----------|-------------|
| **C-001** | Decision Log Bypass | Attempt to execute Proceed (+1) or Refuse (-1) without a committed TGLF log entry with valid `permissionToken` (Proceed) or `TGLF_StateNeg1` record (Refuse). Enforced by Layer 1 StateEnvelope if/then and Layer 5 `TL_Ledger_Core.registerPermissionToken`. | Pre-actuation | FATAL | Layers 1, 3, 5 |
| **C-002** | Provenance Gap (AML) | Asset introduced into a transaction with a broken or missing Merkle chain of custody. `GovernanceProof.merkleProofPath` cannot be verified. Enforced by Layer 4 GovernanceProof cross-reference and Layer 5 `verifyMerkleInclusion`. | Pre-processing | FATAL | Layers 4, 5 |
| **C-003** | Solvency Illusion | Account claims a balance that is unanchored by external Treasury or chain oracle. The Anchor Oracle query returns no valid cryptographic proof of reserve, or the returned timestamp matches a known replay attack pattern. Prevents trading with non-existent money. | Pre-trade | FATAL | Layers 4, 5 |
| **C-004** | Hold Violation | Attempt to force Proceed (+1) or Refuse (-1) execution while the system is in Epistemic Hold (State 0). Any bypass attempt against `GovernancePause` constitutes a constitutional violation. The `EmergencyOverrideRequest.forcedState` enum prohibits +1; only -1 and 0 are permitted. | Instant | FATAL | All layers |
| **C-005** | Regulatory Bypass | Outbound transaction packet lacks a required Regulator View Key, or a mandatory regulatory notification (SAR, FATF report, Basel III disclosure) has not been submitted. Enforced under Pillar V (EconomicRightsAndTransparencyMandate). | Network layer | FATAL | Layer 3 (pillarsCertified) |
| **C-006** | Flash Crash Resonance | Market volatility metrics exceed the safe-harbor limits configured in `ThresholdProfile.haltThreshold` for the active domain. Circuit breaker activates. System enters Epistemic Hold pending human review. Final state: 0 (Epistemic Hold), not -1 (Refuse), unless Hold Violation subsequently occurs. | Less than 1ms | HIGH | Layer 1 (EscrowRecord required) |
| **C-007** | Double-Spend Detect | Asset ID detected in two concurrent state transitions. Pre-commit check in the Governance Lane identifies the collision before either transaction commits. Both transactions are refused. | Pre-commit | CRITICAL | Layers 4, 5 |

### C-Series Detailed Analysis

**C-001 (Decision Log Bypass):** This trigger fires when any attempt is made to produce an externally observable effect without prior committed governance log entry. It is the most fundamental constitutional violation: it is the negation of the NL=NA Iron Law. The trigger operates across all five enforcement layers simultaneously. Any single layer detecting the bypass is sufficient to prevent actuation.

**C-003 (Solvency Illusion):** TL explicitly forbids phantom liquidity. The Governance Lane queries the external Anchor Oracle before authorizing any transaction that claims a specific balance. If the cryptographic proof of reserve is missing, the `GovernanceProof.merkleRoot` cannot be verified, and the `PermissionToken` is not issued. If the timestamp of the returned proof matches a known replay attack pattern (D-003 Time Travel Detect overlap), both triggers fire simultaneously. The `SHUTDOWN_RECORD_SCHEMA.financialContext.replayAttackDetected: true` field records this condition.

**C-004 (Hold Violation):** The Epistemic Hold (State 0) is a mandatory constitutional pause. Any attempt by an automated trading algorithm, administrative override, or external pressure to force continuation from State 0 to State +1 constitutes a C-004 violation. The `EmergencyOverrideRequest` schema enforces this at the schema level: `forcedState` accepts only -1 and 0. Any request carrying `forcedState: 1` is rejected by schema validation before it reaches the enforcement layer. If bypass is attempted through non-schema means, C-004 fires and triggers immediate freeze.

**C-006 (Flash Crash Resonance):** Unlike FATAL triggers that produce State -1 (Refuse), C-006 produces State 0 (Epistemic Hold). The rationale is that flash crash conditions may be transient. The system enters the `GovernancePause` workflow, creates an `EscrowRecord` with `holdRationale.pillarImplicated: "EpistemicHold"`, and awaits resolution from the Governance Lane. If the condition persists beyond `resolutionDeadline`, the system transitions to State -1 (Refuse) via `EPISTEMIC_HOLD_TIMEOUT_ERROR`.

---

## Section 4: D-Series, Cryptographic and Data Integrity Triggers

D-series triggers protect the cryptographic substrate underlying all governance evidence. They enforce the integrity of the Immutable Ledger, the Merkle accumulator, and the timestamp ordering of the governance chain.

| Trigger ID | Trigger Name | Threshold / Condition | Latency | Severity |
|------------|-------------|----------------------|---------|----------|
| **D-001** | Anchor Chain Break | Previous block hash in the Decision Log does not match the stored reference hash. Merkle chain integrity is broken. The `GovernanceProof.merkleProofPath` verification fails. | Instant | FATAL |
| **D-002** | Oracle Deviation | Price feed or time oracle deviates from consensus by more than the configured tolerance in `ThresholdProfile`. Triggers Epistemic Hold pending reconciliation. Final state: 0 (Epistemic Hold). | 1 second | MEDIUM |
| **D-003** | Time Travel Detect | System clock moves backward by more than 100ms. Indicates a settlement timing attack. The monotonic counter in the HSM / TPM provides the authoritative time reference. Backward movement relative to the monotonic counter triggers immediate freeze. | Instant | CRITICAL |

### D-Series Technical Notes

**D-001 (Anchor Chain Break):** Every TGLF log entry references the hash of its predecessor. This creates an unbreakable causal chain that reflects the sequence of governance actions. A break in this chain means either storage corruption or adversarial tampering. In either case, the downstream log entries cannot be trusted and the system must freeze. The `SHUTDOWN_RECORD_SCHEMA.cryptographicContext.previousBlockHash` and `storedReferenceHash` fields record the specific mismatch for forensic analysis.

**D-003 (Time Travel Detect):** The TPM 2.0 monotonic counter and the HSM's protected clock provide the authoritative time reference. These cannot be rolled back by software. If the system clock moves backward relative to these references, the most recent log timestamps become invalid, creating a potential window for replaying old governance decisions. C-003 (Solvency Illusion) may fire simultaneously if the clock reversal appears to enable a proof-of-reserve replay.

---

## Section 5: Architecture B Trigger Behavior Summary

In Architecture B deployments where DITL/MT silicon is not yet fabricated, the following trigger behaviors apply:

**H-001 and H-002:** Software voltage monitoring substitutes for hardware rail sensing. The Window Comparator physical gate does not exist; software consistency checks on governance state substitute.

**H-003:** The physical resistance measurement of the TaOx ReRAM cell is unavailable. `windowComparatorReading.readingAvailable: false` and `softwareEnforcementActive: true` are recorded. Software state consistency verification substitutes for physical IRS boundary enforcement.

**H-007:** The HSM tamper detection mesh and key zeroization are identical in both Architecture B and MT deployments. The HSM is a SHIPPING requirement; it is not deferred to DITL/MT.

**H-008:** Identical in both architectures. The HSM heartbeat monitoring is software-equivalent.

**C-series and D-series:** All C-series and D-series triggers are identical in Architecture B and MT deployments. They operate at the governance logic and cryptographic layers, which are fully operative in Architecture B via software enforcement.

**`SHUTDOWN_RECORD_SCHEMA` fields in Architecture B:**
- `pufAttestation`: `"NULL_PUF_DEPLOYMENT"`
- `architectureMode`: `"ARCHITECTURE_B"`
- `hardwareContext.windowComparatorReading.readingAvailable`: `false` for H-003 events
- `hardwareContext.windowComparatorReading.softwareEnforcementActive`: `true`

---

## Section 6: Trigger Severity Definitions

| Severity | Meaning | Final State | Recovery Path |
|----------|---------|-------------|---------------|
| FATAL | Constitutional violation. No recovery without Tri-Cameral review. | Refuse (-1) | CONSTITUTIONAL_REVIEW or UNFREEZE_TOKEN_REQUIRED |
| CRITICAL | Severe integrity breach. Immediate freeze. Forensic audit required before recovery. | Refuse (-1) | RECOVERY_AUDIT |
| HIGH | Significant threshold breach. Epistemic Hold pending human review. | Epistemic Hold (0) | UNFREEZE_TOKEN_REQUIRED |
| MEDIUM | Data quality issue. Epistemic Hold pending reconciliation. Auto-recovery possible. | Epistemic Hold (0) | RECOVERY_AUDIT (may auto-resolve) |
