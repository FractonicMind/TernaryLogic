# Specification Architecture

## "Ternary Logic" (TL) Governance API

**Framework:** "Ternary Logic" (TL) by Lev Goukassian   
**ORCID:** 0009-0006-5966-1243   
**Repository:** FractonicMind/TernaryLogic   
**Spec Version:** 1.0.0-tl-monograph-2026   
**DOI 1:** 10.1007/s43681-025-00910-6 — "Auditable AI: Tracing the Ethical History of a Model"   
**DOI 2:** 10.1007/s43681-026-01124-0 — "A Ternary Logic Framework for Institutional Governance"   

---

## Section 1 [CONSTITUTIONAL]: The Goukassian Vow as Foundational Architecture

Every schema property, endpoint path, error code, and webhook payload in this specification derives from a single constitutional foundation: the Goukassian Vow.

    "Pause when truth is uncertain"  ->  State  0  (Epistemic Hold)
    "Refuse when harm is clear"      ->  State -1  (Refuse)
    "Proceed where truth is"         ->  State +1  (Proceed)

This is not a design preference. It is the constitutional logic that makes the entire "Ternary Logic" (TL) framework coherent. Every state transition is an expression of one of these three lines.

The first line mandates `EscrowRecord` creation, `TGLF_State0` log emission, and the `epistemicHold.escalation` webhook. The word "uncertain" is the constitutional basis for State 0 never being an error, null, timeout, or retry. It is a first-class determination that truth has not yet been established. Uncertainty is not failure; it is constitutional information.

The second line mandates `TGLF_StateNeg1` log emission, no Permission Token issuance, and `refusalIsPermanent: true` by default. "Harm is clear" is the constitutional basis for Refuse being permanent by default. The ABI's `InvalidResolutionState` revert enforces this at the on-chain layer.

The third line mandates the Permission Token as the cryptographic expression of verified truth. "Where truth is" is the constitutional basis for NL=NA: truth cannot be claimed without prior immutable evidence. The five-layer NL=NA enforcement architecture is the engineering expression of this single phrase.

The Goukassian Vow appears in `tl_openapi.yaml` in both `info.description` and `x-tl-constitutional-preamble`. It governs every state machine branch in `StateEnvelope_v1_0_0`, every TGLF schema const value, and every ABI revert condition in `TL_Ledger_Core`.

---

## Section 2 [INFORMATIVE]: Binary and Ternary in Parallel

The "Ternary Logic" framework does not replace binary inference. It governs it.

The binary inference engine provides speed, pattern recognition, and statistical throughput. It proposes a state. It cannot authorize actuation. This distinction is architectural and constitutional: the Inference Lane produces `TLResult` objects that carry a proposed `state` field. That field is advisory.

The ternary governance coprocessor operates in parallel, receiving the same decision vector through the Governance Lane. It verifies, logs, and either issues or withholds a Permission Token. Only a valid Permission Token from the Governance Lane authorizes the actuation layer to fire.

This is why `POST /decisions` and `POST /governance-logs` are separate endpoints on separate security schemes. The Inference Lane uses `TLGovernanceJWT`. The Governance Lane uses `HSMSignedJWT` and `NLNAGovernanceToken`. A client that has only `TLGovernanceJWT` can propose actions. It cannot authorize them.

The `X-TL-Trace-Id` UUID v4 header is the cryptographic thread that connects both lanes. It is required on every request and echoed in every response, webhook event, and downstream regulator export. The `NLNAGovernanceToken` security scheme is cryptographically bound to the `X-TL-Trace-Id` of the originating Inference Lane request, preventing token substitution across unrelated decision vectors.

---

## Section 3 [NORMATIVE]: Dual-Lane Architecture in OpenAPI Paths

### 3.1 Inference Lane Path Group

The Inference Lane endpoints are `POST /decisions` and `GET /decisions/{decisionId}`. These paths are the binary proposal surface. Security: `TLGovernanceJWT`.

`POST /decisions` accepts a `decisionVector`, `proposedAction`, `GoukassianPrincipleBlock`, optional `RegulatoryContext`, and optional `domain`. It returns a `TLResult` with a `decisionId`. The `TLResult.state` field is the binary engine's proposed state. It is not authorization.

`GET /decisions/{decisionId}` returns the `StateEnvelope` reflecting the current governance state of a decision, including any `PermissionToken` issued by the Governance Lane.

### 3.2 Governance Lane Path Group

The Governance Lane endpoints are `POST /governance-logs` and `GET /governance-logs/{logId}`. These paths are the ternary governance surface. Security: `HSMSignedJWT` and `NLNAGovernanceToken`.

`POST /governance-logs` is the central NL=NA enforcement point. It accepts a `decisionId`, a `tglfRecord`, a `GoukassianPrincipleBlock`, and a `GovernanceProof` object. The `GovernanceProof.logHash` and `GovernanceProof.merkleRoot` fields must match the `PermissionToken.logHash` and `PermissionToken.merkleRoot` fields respectively (NL=NA Layer 4). On State +1, a `PermissionToken` is returned inside a `StateEnvelope`. On State 0, an `EscrowRecord` is returned and the `epistemicHold.escalation` webhook fires. On State -1, a `StateEnvelope` with `stateLabel: "Refuse"` is returned and no `PermissionToken` is issued.

### 3.3 Gateway Fail-Closed Behavior

`GET /gateway/status` and `POST /gateway/lane-assignment` expose the TL Gateway routing state. The Gateway is fail-closed by design: if it cannot route to the Governance Lane, it defaults to `EPISTEMIC_HOLD` and activates `epistemicHoldOverride: true`. The `GatewayRoutingStatus.operationalStatus` enum includes `EPISTEMIC_HOLD_OVERRIDE_ACTIVE` to signal this condition.

Fail-open is constitutionally prohibited. This means a Gateway that loses connectivity to the Governance Lane does not pass traffic to the actuation layer. It holds all pending decisions in Epistemic Hold until the Governance Lane is restored.

The `epistemicHoldOverride` boolean flag in `POST /gateway/lane-assignment` signals that the client is requesting fail-closed activation explicitly. This is not an override of Epistemic Hold; it is a signal that the fail-closed mode should activate now rather than waiting for automatic detection.

---

## Section 4 [NORMATIVE]: NL=NA Schema-Level Enforcement

NL=NA (No Log = No Action) is enforced at five independent layers. Bypassing one layer does not bypass the others.

**Layer 1** is in `StateEnvelope_v1_0_0` in `tl_schema.json`. The `if/then` constraint makes `permissionToken` a required property when `currentState` equals 1. The `unevaluatedProperties: false` keyword prevents bypass by additional properties. This layer is evaluated on every response object returned by any endpoint that produces a `StateEnvelope`.

**Layer 2** is in `PermissionToken_v1_0_0` in `tl_schema.json`. The `laneOrigin` field carries a `const: "GOVERNANCE_LANE"` constraint. Any `PermissionToken` object with `laneOrigin` set to any other value is schema-invalid. In `tl_abi.json`, `TL_Ledger_Core.registerPermissionToken` accepts a `laneOriginHash` parameter that must equal `keccak256("GOVERNANCE_LANE")`. Mismatch reverts `NLNAViolation`.

**Layer 3** is in `TGLF_StateP1_v1_0_0` in `tl_schema.json`. The `permissionToken` field is in the `required` array. The `pillarsCertified` array carries `minItems: 8, maxItems: 8`. A `TGLF_StateP1` record without a `permissionToken` is schema-invalid. A record with fewer than 8 certified pillars is schema-invalid.

**Layer 4** is in `GovernanceProof_v1_0_0` in `tl_schema.json`. The `GovernanceProof.logHash` field must match `PermissionToken.logHash`. The `GovernanceProof.merkleRoot` field must match `PermissionToken.merkleRoot`. This cross-reference is described in both field descriptions and enforced by the `POST /governance-logs` request handler.

**Layer 5** is in `TL_Ledger_Core.registerPermissionToken` in `tl_abi.json`. This function reverts `NLNAViolation` if the supplied `logHash` is not provably included in an anchored Merkle root via `verifyMerkleInclusion`. This is the terminal on-chain enforcement gate.

The fail-closed default applies to all five layers: any Governance Lane failure, timeout, or ambiguity defaults to `EPISTEMIC_HOLD` or `REFUSE`, never to `PROCEED`. NL=NA applies to Emergency Override without exception.

---

## Section 5 [NORMATIVE]: Epistemic Hold

### 5.1 State versus Workflow Distinction

Epistemic Hold is a TL constitutional state. Its integer value is 0. Its `stateLabel` is `"EpistemicHold"`. These are state identifiers.

`GovernancePause` is the workflow process name that activates when Epistemic Hold is declared. It appears in `StateEnvelope.processActive` as `const: "GovernancePause"` and in `TGLF_State0.processActive` as `const: "GovernancePause"`. It is a workflow name, not a state synonym.

The distinction matters for auditability: an auditor reading a `TGLF_State0` record can distinguish between the constitutional state (Epistemic Hold, State 0) and the governance workflow activated by that state (GovernancePause). Conflating the two would create ambiguity in records that must remain unambiguous for decades.

### 5.2 EscrowRecord as Single Schema Source

`EscrowRecord_v1_0_0` in `tl_schema.json` is the single authoritative definition of all Epistemic Hold response fields. The behavioral description in Section 4.4 of the specification prompt lists the required fields; all of them are defined exclusively in `EscrowRecord_v1_0_0`. No other schema duplicates these definitions.

The fields are: `escrowId`, `heldState` (const 0), `initiatedAt`, `initiatingDecisionId`, `holdRationale` (with `rationale`, `uncertaintyScore`, `pillarImplicated`), `resolutionDeadline`, `immutableLogHash`, `holdDurationMs`, `governanceLaneStatus` (with `stage` and `percentComplete`), `requiredConditions`, and `windowComparatorReading`.

### 5.3 Resolution Constraints

Resolution of Epistemic Hold must specify a terminal state: +1 (Proceed) or -1 (Refuse). State 0 is not a valid resolution. This constraint is enforced at three layers:

`PATCH /epistemic-hold/escalations/{escalationId}` accepts `resolvedState` with enum `[1, -1]`. The schema rejects State 0 at the HTTP layer.

`TL_Ledger_Core.resolveEpistemicHoldSystemWide` reverts `InvalidResolutionState` for any `resolvedState` value other than 0 (encoding REFUSE) or 1 (encoding PROCEED). The uint8 encoding in this ABI function uses 0 to mean REFUSE and 1 to mean PROCEED; this is a function-local encoding to work within uint8 constraints and does not affect the triadic integer semantics elsewhere in the specification.

Tri-Cameral governance bodies may not indefinitely defer resolution. The `resolutionDeadline` field in `EscrowRecord` and `TGLF_State0.resolutionRequest.resolutionDeadline` establish a constitutional deadline.

---

## Section 6 [NORMATIVE]: Goukassian Principle as API Resources

The Goukassian Principle has three properties. Each is modeled as a canonical lowercase string artifact name and exposed as a dedicated API resource.

`lantern` (artifactName const `"lantern"`) is exposed at `GET /epistemic-hold/lantern`. The Lantern broadcasts the current governance transparency posture. Its `compliancePosture` enum includes `EPISTEMIC_HOLD_ACTIVE`, which reflects the constitutional state, not an error. The `pillarStatuses` array reflects all 8 pillars.

`signature` (artifactName const `"signature"`) is exposed at `GET /goukassian/signature`. The Signature Block carries the current Ed25519 or ES256 attestation and the `attestationChainStatus`. PQC migration slots 6 (SLH-DSA-SHAKE-128s) and 7 (ML-KEM-1024) are reserved in `SignatureBlock_v1_0_0.signatureAlgorithm`.

`license` (artifactName const `"license"`) is exposed at `POST /goukassian/license/validate`. Any proposed action exceeding the `licenseScope` array triggers automatic Refuse (State -1). The `LicenseValidationRequest_v1_0_0` schema enforces `artifactName: const "license"` as a required field.

In `GoukassianPrincipleBlock_v1_0_0`, the three artifacts are nested objects. Each carries `artifactName` as a const-constrained property. In `eip712_typed_data.json`, `GoukassianSignatureAttestation.artifactName` is typed as `bytes32` with canonical value `keccak256("signature")`. The `canonicalArtifactNameHashes` section records the pre-images for all three artifact names.

---

## Section 7 [NORMATIVE]: Eight Pillars

The Eight Pillars are the governance architecture of the "Ternary Logic" framework. Their canonical identifiers are used in `x-tl-pillar` annotations on every endpoint and in `PillarIdentifier_v1_0_0` as the exclusive vocabulary for pillar references.

**Pillar I (EpistemicHold):** Expressed through `POST /decisions`, `POST /governance-logs`, `GET/PATCH /epistemic-hold/escalations/*`, and `GET /epistemic-hold/lantern`. Schema anchor: `EscrowRecord_v1_0_0`, `TGLF_State0_v1_0_0`. Gateway fail-closed behavior is a Pillar I enforcement mechanism.

**Pillar II (ImmutableLedger):** Expressed through `POST /governance-logs`, `GET /governance-logs/{logId}`, `POST /refusals`, `GET /regulator/timestamp-verification/{logId}`, and the `GovernanceProof_v1_0_0` schema. The `ghostGovernanceDetectionRate` metric in `GET /metrics/summary` quantifies Ghost Governance prevention at the NL=NA physical commit boundary.

**Pillar III (GoukassianPrinciple):** Expressed through `GET /goukassian/signature`, `POST /goukassian/license/validate`, `GET /epistemic-hold/lantern`, `GET /gateway/status`, and the `GoukassianPrincipleBlock_v1_0_0` schema. Required on every `POST /decisions`, `POST /governance-logs`, and `POST /evaluate/*` request body.

**Pillar IV (DecisionLogs):** Expressed through `GET /decisions/{decisionId}`, `GET /thresholds/{domain}`, `PUT /thresholds/{domain}`, and `GET /metrics/summary`. Schema anchor: `JustificationObject_v1_0_0`, `ThresholdProfile_v1_0_0`.

**Pillar V (EconomicRightsAndTransparencyMandate):** Expressed through `POST /evaluate/trade`, `POST /redress/*`, `GET /regulator/basel-iii/attestation`, `POST /regulator/fatf/compliance-export`, `GET /regulator/iosco/principle-mapping`, and `POST /regulator/evidence-export`. Regulatory vectors: Basel III, FATF, IOSCO, CFPB, SEC, FINRA.

**Pillar VI (SustainableCapitalAllocationMandate):** Expressed through `POST /evaluate/policy`, `POST /evaluate/supply-chain`. Regulatory vectors: Paris Agreement (carbon footprint, green bond eligibility, ESG score), climate-aligned capital flow validation.

**Pillar VII (HybridShield):** Expressed through `POST /emergency/override`, `GET /emergency/status`, `GET /governance/custodians/{custodianId}/heartbeat`, `GET /regulator/custodian-quorum`, and `POST /pillars/{pillarId}/configure`. Schema anchor: `TriCameralApproval_v1_0_0`, `EmergencyOverrideRequest_v1_0_0`, `EKRRecord_v1_0_0`.

**Pillar VIII (Anchors):** Expressed through `GET /governance/verifications/merkle/{merkleRoot}`, `GET /governance/verifications/inclusion/{logId}`, and the `SuccessionDeclaration_v1_0_0` schema. The `canonicalArtifactNameHashes` and `canonicalMandateHashes` sections of `eip712_typed_data.json` are Pillar VIII artifacts.

**Cross-pillar dependency notes:** Pillar V regulatory failures feed Pillar VII (HybridShield governance escalation). Pillar I (EpistemicHold) activation degrades all eight Pillar statuses in `LanternStatus.pillarStatuses`. Pillar VIII (Anchors) provides the cryptographic substrate on which Pillar II (ImmutableLedger) depends.

---

## Section 8 [NORMATIVE]: Regulatory Nexus

Regulatory compliance checks are the detection and refusal layer before a Permission Token is requested. They are not synonymous with NL=NA. NL=NA applies universally; regulatory checks apply domain-specifically under Pillars V and VI.

**Basel III** is expressed in `RegulatoryContext.baselIii` (lcr, nsfr, capitalRatio, stressTestRequired, counterpartyExposureWithinLimits), `GET /regulator/basel-iii/attestation`, `ITL_Validator.verifyEconomicRightsCompliance` (baselIiiVector), and `RegulatoryFlags.baselIiiFlags`. The LCR >= 1.0 and NSFR >= 1.0 constraints are encoded as threshold values in `baselIiiVector.lcr` and `baselIiiVector.nsfr` (scaled to 1e18 in the ABI).

**FATF** is expressed in `RegulatoryContext.fatf` (amlCheckRequired, sanctionsScreened, pepInvolved, sarGenerated), `POST /regulator/fatf/compliance-export`, `ITL_Validator.verifyEconomicRightsCompliance` (fatfVector), and `RegulatoryFlags.fatfFlags`. The `EconomicRightsMandateViolationDetected` event carries the `violationCode` bytes32 for programmatic downstream handling.

**IOSCO** is expressed in `RegulatoryContext.iosco` (layeringDetected, spoofingDetected, washTradingDetected, crossMarketManipulationDetected), `GET /regulator/iosco/principle-mapping`, and `ITL_Validator.verifyEconomicRightsCompliance` (ioscoVector).

**GDPR** is expressed in `RegulatoryContext.gdpr` (jurisdiction, consentAttestation, erasureEligible). The `erasureEligible` field reflects whether GDPR Article 17 applies. TL uses cryptographic erasure via HKDF-SHA3-256 key destruction (not pseudonymization under Article 4(5)) as the SHIPPING mitigation. This is captured in `EKRRecord_v1_0_0.hkdfSha3256Confirmed`.

**Paris Agreement** is expressed in `RegulatoryContext.parisAgreement` (carbonFootprintVerified, greenBondEligibility, esgScore), `POST /evaluate/policy` (policyMetadata.greenBondEligibility), `POST /evaluate/supply-chain` (chainMetadata.carbonFootprintVerified), and `ITL_Validator.verifySustainableCapitalCompliance`.

All five regulatory frameworks carry versioning through `RegulatoryContext.regulatoryFrameworkVersion` (baselVersion, fatfVersion, ioscoVersion, gdprVersion).

---

## Section 9 [NORMATIVE]: Domain Evaluation Endpoints

The three domain evaluation endpoints represent "Ternary Logic" (TL) governance at institutional scale.

`POST /evaluate/trade` is the financial trading governance surface. It accepts a `tradeVector`, `RegulatoryContext` (with Basel III, FATF, and IOSCO sub-objects populated), and a `GoukassianPrincipleBlock`. It returns a `TLResult` with `tradingMetadata` containing `fillProbability`, `marketImpactEstimate`, and `amlClearanceStatus` (CLEARED, PENDING_REVIEW, or REFUSED). The `amlClearanceStatus` enum maps to the Goukassian Vow: CLEARED is Proceed-eligible, PENDING_REVIEW triggers Epistemic Hold, REFUSED triggers Refuse.

`POST /evaluate/policy` is the central banking and monetary policy governance surface. It returns `policyMetadata` with `inflationImpact`, `unemploymentDelta`, and `greenBondEligibility`. The `greenBondEligibility` boolean is the direct expression of Pillar VI (SustainableCapitalAllocationMandate) in monetary policy decisions.

`POST /evaluate/supply-chain` is the supply chain governance surface. It returns `chainMetadata` with `carbonFootprintVerified` and `laborStandardCompliance`. These fields are the direct expression of Paris Agreement compliance at the supply chain level.

All three domain endpoints require `GoukassianPrincipleBlock` in the request body. All three are tagged `Regulatory Compliance` and `Decision Engine`. All three are on the Inference Lane path group and return `TLResult` objects, not `StateEnvelope` objects. The `POST /governance-logs` step is required before any Proceed determination from these endpoints may authorize actuation.

---

## Section 10 [NORMATIVE]: Governance and Regulator Surface

The following 6-step workflow describes a complete compliance verification using only endpoints defined in `tl_openapi.yaml`.

**Step 1: Verify the Merkle anchor.** `GET /governance/verifications/merkle/{merkleRoot}`. The auditor supplies the Merkle root from a log record under review. The response confirms `verified: true`, `anchoredAt`, and `blockchainTxHash`. This step confirms that the Merkle batch containing the log under review is on-chain.

**Step 2: Verify log inclusion.** `GET /governance/verifications/inclusion/{logId}`. The auditor supplies the `logId`. The response provides the full Merkle inclusion proof path (`merklePath`), `leafHash`, and `merkleRoot`. The auditor can independently verify the proof offline.

**Step 3: Retrieve the anchored TGLF record.** `GET /governance-logs/{logId}`. The auditor retrieves the full TGLF record and the embedded `StateEnvelope`. For State +1 records, the `permissionToken` field is present and can be verified against the Merkle root from Step 1.

**Step 4: Verify the RFC 3161 timestamp.** `GET /regulator/timestamp-verification/{logId}`. The auditor verifies the qualified timestamp of the log entry. The response carries the `rfc3161Token` bytes and `tsaIssuer`.

**Step 5: Pull the Eight Pillar compliance attestation.** `GET /governance/compliance/attestation`. The auditor retrieves the signed attestation covering all 8 Pillars, with per-pillar `complianceStatus` and `attestationHash`.

**Step 6: Export regulatory evidence.** `POST /regulator/evidence-export`. For bulk governance requirements, the auditor requests a signed, Merkle-verified archive. The asynchronous response provides an `exportJobId` for status tracking.

### Monograph Reference Index

The following is a machine-readable list of all `x-tl-monograph-ref` values used across `tl_openapi.yaml` endpoints:

- `"Constitutional Hardware Monograph, Section I"` - Core TLState definitions; Inference Lane; Refusal State
- `"Constitutional Hardware Monograph, Section II"` - Governance Lane; Epistemic Hold; Gateway; DLLA; Permission Token; EscrowRecord
- `"Constitutional Hardware Monograph, Section III"` - Goukassian Principle; Eight Pillars; Regulatory Nexus; Tri-Cameral; EKR; Succession Declaration
- `"Constitutional Hardware Monograph, Section IX.3"` - Emergency Override
- `"Constitutional Hardware Monograph, Section X"` - DITL Hardware Interface; Implementation Gap; custodian quorum latency

---

## Section 11 [NORMATIVE]: DITL Hardware Interface

### 11.1 Architecture B Hybrid Model (SHIPPING Baseline)

The SHIPPING baseline for this specification is Architecture B: software enforcement with DITL attestation where available. This model uses the `NULL_PUF_DEPLOYMENT` sentinel value in `NLNAGovernanceToken.pufAttestation` for non-MT deployments.

Architecture B compensating controls: the `windowComparatorReading.softwareEnforcementActive: true` field in `EscrowRecord` signals that software-layer enforcement is active in place of physical DITL gate enforcement. The `TLCapabilityFlags.pufAttestationMode: "ARCHITECTURE_B"` capability flag in `tl_openapi.yaml` informs consumers of the deployment posture.

`NLNAGovernanceToken.pufAttestation` must be set to the string `"NULL_PUF_DEPLOYMENT"` for all non-MT deployments. This sentinel value maintains schema integrity without silently omitting the field.

### 11.2 MT Integration (FUTURE)

Full DITL deployment at TSMC N2 or Intel 18A nodes with physical Window Comparator enforcement is FUTURE status per Section X of the TL monograph. The two DITL endpoints are:

`POST /ditl/state-transition`: MT hardware state query with Window Comparator verification. `x-tl-implementation-status: FUTURE`. `x-tl-blocking-constraint: "Constitutional Hardware Monograph, Section X"`.

`GET /ditl/puf-attestation/{deviceId}`: PUF attestation chain verification. `x-tl-implementation-status: FUTURE`. `x-tl-blocking-constraint: "Constitutional Hardware Monograph, Section X"`.

### 11.3 PUF Attestation Chain

The PUF Attestation Chain consists of five elements: enrollment, foundry attestation, NL=NA interlock verification, immutable log entry, and Merkle hash chain. In SHIPPING deployments, elements 1 and 2 are replaced by the `NULL_PUF_DEPLOYMENT` sentinel. Elements 3, 4, and 5 are fully operative in Architecture B via software enforcement.

---

## Section 12 [NORMATIVE]: EKR, GDPR Cryptographic Erasure, and Succession Declaration

### 12.1 Ephemeral Key Rotation (EKR)

EKR is defined in `EKRRecord_v1_0_0` in `tl_schema.json`. Ephemeral keys protect proprietary information during the key's active lifetime while preserving auditability after expiration. The `governanceRetentionAnchor` SHA-256 field ensures that the governance trail survives key destruction.

The `hkdfSha3256Confirmed: true` field confirms that HKDF-SHA3-256 key derivation was used for this rotation event, which is the SHIPPING mitigation for GDPR Article 17 compliance. Key destruction via HKDF-SHA3-256 achieves cryptographic erasure: the underlying data becomes computationally irrecoverable while the governance record remains intact.

### 12.2 GDPR Cryptographic Erasure

TL uses cryptographic erasure (key destruction via HKDF-SHA3-256) to achieve GDPR-compliant anonymization post-retention. This is not pseudonymization in the Article 4(5) sense. The `RegulatoryContext.gdpr.erasureEligible` boolean field triggers the EKR workflow when true.

Three residual sub-gaps remain as FUTURE items: regulatory interpretation (some jurisdictions may not recognize cryptographic erasure as equivalent to deletion), erasure key registry dependency (the registry that maps data subjects to their encryption keys must itself be erasable), and metadata residue (log timestamps and access patterns may remain after key destruction). These gaps are documented in `future_blocked_appendix.md`.

### 12.3 Succession Declaration

The `SuccessionDeclaration_v1_0_0` schema defines a notarized, timestamped, anchored governance continuity instrument. It is referenced in Pillar VIII (Anchors) documentation and ensures TL governance permanence beyond any single actor or institution.

Fields: `declarationId` (UUID), `notarizedAt` (ISO8601), `notaryIdentifier` (string), `blockchainAnchor` (on-chain transaction hash), `successionScope` (array of covered governance domains), `validUntil` (ISO8601 expiration), and `merkleAnchorHash` (SHA-256 on-chain anchor).

Expiry of a Succession Declaration triggers `SUCCESSION_DECLARATION_EXPIRED_ERROR` in the `TLProblemDetail` error taxonomy. The `SUCCESSION_DECLARATION_REQUIRED_ERROR` code is emitted when a governance operation requires a valid Succession Declaration and none is present.

---

## Section 13 [NORMATIVE]: Error Handling

All error responses conform to RFC 7807 `application/problem+json` with mandatory TL extensions. The `TLProblemDetail_v1_0_0` schema defines the full structure.

Three fields are mandatory and never omitted on any error response:

`x-tl-state` (signed integer, enum [-1, 0, 1]): the ternary disposition of the error condition. Even errors carry a constitutional state. An error that occurs during an Epistemic Hold carries `x-tl-state: 0`. An error that indicates a constitutional violation carries `x-tl-state: -1`.

`x-tl-pillar` (PillarIdentifier enum): the canonical pillar implicated in this error.

`x-tl-trace-id` (UUID v4): echoed from the originating request `X-TL-Trace-Id` header.

**GhostGovernanceDetectedError** carries `x-tl-state: -1` or `x-tl-state: 0`, never omitted. Ghost Governance is governance actions executing without corresponding immutable governance evidence. It is eliminated by NL=NA at the physical commit boundary. When detected (e.g., an actuation attempt without a registered Permission Token), the error carries `tlErrorCode: "GHOST_GOVERNANCE_DETECTED_ERROR"`.

**SuccessionDeclarationExpiredError** carries `tlErrorCode: "SUCCESSION_DECLARATION_EXPIRED_ERROR"` and `x-tl-pillar: "Anchors"`. It signals that a required Succession Declaration has passed its `validUntil` timestamp.

**Fail-closed default:** any condition that cannot be resolved to a definitive `PROCEED` determination defaults to `EPISTEMIC_HOLD` or `REFUSE`. The error taxonomy includes `EPISTEMIC_HOLD_TIMEOUT_ERROR` for cases where the Epistemic Hold resolution deadline has been passed without Tri-Cameral action.

---

## Section 14 [NORMATIVE]: Trace Propagation

The `X-TL-Trace-Id` UUID v4 header is the constitutional thread connecting every layer of the governance stack. The following sequence describes its propagation.

```
Client                    Inference Lane              Governance Lane            Regulator
  |                            |                          |                          |
  |-- POST /decisions -------->|                          |                          |
  |   X-TL-Trace-Id: T1        |                          |                          |
  |<-- TLResult + decisionId --|                          |                          |
  |   X-TL-Trace-Id: T1        |                          |                          |
  |                            |                          |                          |
  |-- POST /governance-logs ---|------------------------->|                          |
  |   X-TL-Trace-Id: T1        |                          |                          |
  |   (bound to T1 by NLNAGovernanceToken)                |                          |
  |<-- StateEnvelope + PermissionToken ------------------|                          |
  |   X-TL-Trace-Id: T1        |                          |                          |
  |                            |                          |                          |
  |   (if State 0: webhook fires)                         |                          |
  |<-- epistemicHold.escalation webhook                   |                          |
  |   event_id: E1, x-tl-trace-id: T1                    |                          |
  |                            |                          |                          |
  |-- POST /regulator/evidence-export ------------------------------------------>|
  |   X-TL-Trace-Id: T1        |                          |                          |
  |<-- exportJobId -----------------------------------------------------------|
  |   (archive contains T1-linked TGLF records, PermissionTokens)             |
```

The `X-TL-Trace-Id` T1 appears in: the `POST /decisions` request and response, the `POST /governance-logs` request and response (cryptographically bound via `NLNAGovernanceToken`), any `StateEnvelope` returned by the Governance Lane, the `epistemicHold.escalation` webhook payload (`x-tl-trace-id` field), and the `POST /regulator/evidence-export` archive (linking all records to T1).

The `x-tl-idempotency` guarantee on all webhook payloads uses `event_id` (UUID v4) as the deduplication key. Receivers must deduplicate by `event_id`, not by `x-tl-trace-id`, since a single trace may produce multiple webhook events.

---

*Constitutional Uncertainty Register for Deliverable F*

| Item | Location | Issue | Assumption Made |
|---|---|---|---|
| `<MONOGRAPH_EXCERPT_MISSING>` | Section 11 - Architecture B exact compensating control specification | Monograph Section X not supplied as excerpt. | Architecture B described from Section 4.10 of the constitutional prompt (informative): "software enforcement with DITL attestation where available." NULL_PUF_DEPLOYMENT sentinel documented per Section 5B of the prompt. |
| `<MONOGRAPH_EXCERPT_MISSING>` | Section 12.2 - Three GDPR sub-gaps exact phrasing | Section X not supplied. | Sub-gaps derived from Section 5G of the constitutional prompt, which lists them verbatim: regulatory interpretation, erasure key registry dependency, metadata residue. |
