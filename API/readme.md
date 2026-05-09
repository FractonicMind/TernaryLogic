# TL API Specification Suite: The "Ternary Logic" (TL) Framework

### Prologue: I Read This Document So You Don't Have To

Before diving into the specification files, we recommend reading **[I_Read_API_Documents_So_You_Don't_Have_To.md](https://github.com/FractonicMind/TernaryLogic/blob/main/API/I_Read_API_Documents_So_You_Don't_Have_To.md)** — a companion narrative that restores the constitutional thread inside schema constraints and ABI function signatures. Engineers, auditors, and policymakers who encounter a 14-file API specification suite can easily lose that thread. This companion piece restores it.

You can also listen to the full AI-generated deep-research interview: **[Preventing Financial Collapse With Ternary Hardware](https://fractonicmind.github.io/TernaryLogic/API/Preventing_Financial_Collapse_With_Ternary_Hardware.mp3)**

---

## Overview: The Constitution in Code

The TL API is not a conventional REST interface. It is the software expression of a constitutional enforcement architecture: a sovereign governance coprocessor that operates in parallel with a binary inference engine and holds absolute authority over whether any proposed action crosses the threshold into execution.

The binary system proposes. The ternary system decides. The **Permission Token** is the only key that opens the actuation gate. Without a cryptographically valid token issued by the **Audit Lane**, no proposed State +1 action may execute. This is the **No Log = No Action** (NL=NA) iron law, enforced simultaneously at the schema layer, the API contract layer, the on-chain ABI layer, and the EIP-712 signing layer. There is no software path around it in a conforming implementation.

The **Epistemic Hold** (State 0) is the most constitutionally significant state in the framework. It is not a null. It is not an error. It is not a timeout. It is a first-class governance state of mandatory hesitation that holds execution pending verified completion of legitimate process. It cannot be argued away. It can only be resolved by a human reviewer or a Tri-Cameral custodian quorum with a terminal state of +1 or -1. State 0 is constitutionally invalid as a resolution target.

### The Goukassian Vow

```
"Pause when truth is uncertain"  →  State  0  (Epistemic Hold)
"Refuse when harm is clear"      →  State -1  (Refuse)
"Proceed where truth is"         →  State +1  (Proceed)
```

---

## Architecture: The Dual-Lane System

![Dual-Lane Architecture](https://github.com/FractonicMind/TernaryLogic/blob/main/API/diagram_dual_lane_architecture.png?raw=true)

The entire API is organized around two structurally distinct lanes, each with its own security scheme, latency envelope, and constitutional function.

**Inference Lane:** The binary inference engine submits proposed decision vectors via `POST /decisions` and receives a `TLResult`. A `TLResult` returning State +1 from the Inference Lane does not authorize actuation. The Inference Lane cannot issue Permission Tokens. Security scheme: `TLGovernanceJWT`. This separation is enforced at the schema level by the `StateEnvelope` `if/then` constraint in `tl_schema.json`.

**Audit Lane:** The ternary governance layer receives the complete TGLF record via `POST /audit-logs`, performs its own independent evaluation, and — only when the audit lane confirms log completion and Merkle anchoring — issues a Permission Token. The token carries `laneOrigin: const "AUDIT_LANE"`. Security schemes: `HSMSignedJWT` and `NLNAAuditToken`. No token, no execution. No log, no token.

---

## Core Constitutional Enforcement

![NL=NA Five-Layer Stack](https://github.com/FractonicMind/TernaryLogic/blob/main/API/diagram_nlna_five_layer_stack.png?raw=true)

NL=NA is enforced at five independent layers. Bypassing one layer does not bypass the others.

`TL_Ledger_Core.sol` and `ITL_Validator.sol` are the on-chain enforcement layer. Even if a Permission Token were constructed that passed all off-chain schema validations, its registration on-chain would fail unless the authorizing TGLF record is already anchored in a previously committed Merkle root. The `NLNAViolation` custom error is the final constitutional backstop.

---

## The Three Triadic States

![Goukassian Vow State Machine](https://github.com/FractonicMind/TernaryLogic/blob/main/API/diagram_goukassian_vow_state_machine.png?raw=true)

Every object in this specification carries a `currentState` field drawn from exactly three values: `+1`, `0`, `-1`. These are signed integers, not enumerations of convenience. The `StateEnvelope` schema enforces the constitutional consequence of each value through `if/then` constraints: State +1 requires a `permissionToken`; States 0 and -1 prohibit one.

---

## TGLF: The Governance Log Variants

![Decision Lifecycle](https://github.com/FractonicMind/TernaryLogic/blob/main/API/diagram_decision_lifecycle.png?raw=true)

Every governance decision generates a Ternary Governance Log Format (TGLF) record. The discriminator on `currentState` routes to one of three forensic log variants. `TGLF_StateP1` carries the Permission Token, the Goukassian Principle Block, and the Merkle anchoring proof. `TGLF_State0` carries the uncertainty quantification, the deliberation matrix, and the Epistemic Hold escalation record. `TGLF_StateNeg1` carries the license violation record, the threat vector analysis, and the chain of custody. Every variant requires `committedAt` before the Audit Lane releases any authorization. The log precedes the action. Always.

---

## Tri-Cameral Governance

![Tri-Cameral Governance](https://github.com/FractonicMind/TernaryLogic/blob/main/API/diagram_tri_cameral_governance.png?raw=true)

State-mutating operations require `TriCameralApproval`. The Technical Council (9 members) holds proposal rights. The Stewardship Custodians (11 members) hold binding veto authority — `vetoExercised: true` blocks constitutionally. The Smart Contract Treasury executes automatically with no admin key and no human override path. Emergency overrides are logged before execution. `forcedState` enum is limited to [-1, 0]. Forced +1 is constitutionally blocked and will revert `UnauthorizedOverride`.

---

## Emergency Override

![Emergency Override](https://github.com/FractonicMind/TernaryLogic/blob/main/API/diagram_emergency_override.png?raw=true)

`POST /emergency/override` is the break-glass surface. Three override types: `BREAK_GLASS_SHUTDOWN`, `KILL_SWITCH`, `FORCED_STATE_TRANSITION`. NL=NA applies without exception. The audit log is written before the state change fires. This ordering is constitutional.

---

## Repository Artifacts and Documentation

### 1. OpenAPI Specification

The canonical, machine-parseable API contract. Defines all 40 endpoints across 12 path groups, 5 security schemes, request and response schemas, 2 webhook callbacks, and the dual-lane architectural separation. Import directly into Swagger UI, Postman, or any OpenAPI-compliant code generator.

- **Source:** [tl_openapi.yaml](https://github.com/FractonicMind/TernaryLogic/blob/main/API/tl_openapi.yaml)
- **Web:** [View HTML](https://fractonicmind.github.io/TernaryLogic/API/openapi.html)

### 2. TL JSON Schema Bundle

The canonical schema bundle for all data types in the framework. 22 schemas, all enforcing `unevaluatedProperties: false`. Contains `StateEnvelope`, `PermissionToken`, all three TGLF variants, `GoukassianPrincipleBlock`, `EscrowRecord`, `SignatureBlock`, `LanternStatus`, `AuditProof`, `TriCameralApproval`, `EKRRecord`, `SuccessionDeclaration`, `TLProblemDetail`, and all primitives. The `if/then` constraint on `StateEnvelope` is the schema-level enforcement of NL=NA.

- **Source:** [tl_schema.json](https://github.com/FractonicMind/TernaryLogic/blob/main/API/tl_schema.json)
- **Web:** [View HTML](https://fractonicmind.github.io/TernaryLogic/API/schema.html)

### 3. TL Smart Contract ABI Bundle

Application Binary Interface definitions for `TL_Ledger_Core.sol` and `ITL_Validator.sol`. Covers `anchorMerkleRoot`, `registerPermissionToken`, `verifyPermissionToken`, `verifyMerkleInclusion`, `activateEpistemicHoldSystemWide`, `resolveEpistemicHoldSystemWide`, `executeEmergencyOverride`, `revokePermissionToken`, mandate verification functions, and all custom errors. No Solidity source code. The on-chain layer is the final arbiter of token validity.

- **Source:** [tl_abi.json](https://github.com/FractonicMind/TernaryLogic/blob/main/API/tl_abi.json)
- **Web:** [View HTML](https://fractonicmind.github.io/TernaryLogic/API/abi_eip712.html)

### 4. EIP-712 Typed Data Schema Bundle

EIP-712 domain separator and typed data schema definitions for `GovernanceTraceLog`, `PermissionToken`, `EmergencyOverride`, and `GoukassianSignatureAttestation`. Enables off-chain structured data signing with on-chain verifiability. Binds signatures to a specific contract, chain, and monograph version, preventing cross-domain and cross-version replay attacks. `canonicalArtifactNameHashes` records keccak256 pre-images for all three Goukassian Principle artifact names.

- **Source:** [eip712_typed_data.json](https://github.com/FractonicMind/TernaryLogic/blob/main/API/eip712_typed_data.json)
- **Web:** [View HTML](https://fractonicmind.github.io/TernaryLogic/API/abi_eip712.html)

### 5. Specification Architecture

The canonical prose companion to `tl_openapi.yaml` and `tl_schema.json`. 14 sections covering the Goukassian Vow as foundational architecture, the Dual-Lane system, NL=NA five-layer enforcement, Epistemic Hold operationalization, the Goukassian Principle artifacts as API resources, all Eight Pillars mapped to API paths, the Regulatory Nexus (Basel III, FATF, IOSCO, GDPR, Paris Agreement), Domain Evaluation endpoints, the complete auditor verification workflow, DITL hardware interface, EKR and GDPR cryptographic erasure, error taxonomy, and trace propagation. Read this before reading the machine-readable files.

- **Text:** [Specification_Architecture.md](https://github.com/FractonicMind/TernaryLogic/blob/main/API/Specification_Architecture.md)
- **Web:** [View HTML](https://fractonicmind.github.io/TernaryLogic/API/Specification_Architecture.html)

### 6. Constitutional Compliance Matrix

Maps every OpenAPI path and every JSON Schema definition to its Monograph section, TL Pillar, Regulatory Nexus, Implementation Status (SHIPPING / BETA / FUTURE), and Pillar Interactions. Includes NL=NA five-layer checklist, Epistemic Hold integrity checkpoints, Goukassian Principle artifact name audit, implementation gap summary, and dangling reference audit. Sufficient for auditor verification without reading implementation code.

- **Text:** [Constitutional_Compliance_Matrix.md](https://github.com/FractonicMind/TernaryLogic/blob/main/API/Constitutional_Compliance_Matrix.md)
- **Web:** [View HTML](https://fractonicmind.github.io/TernaryLogic/API/Constitutional_Compliance_Matrix.html)

### 7. Future and Blocked Features Appendix

Explicit catalog of six features that are constitutionally desirable but not yet shipping due to named Section X constraints: real-time per-trade blockchain anchoring (throughput asymmetry), Post-Quantum Cryptography signature migration (SLH-DSA-SHAKE-128s and ML-KEM-1024, pending HSM readiness), full DITL/MT hardware deployment (pending TSMC N2 production silicon), sub-300ms cross-jurisdiction custodian quorum (network physics), full GDPR Article 17 native compliance (Erasure Paradox: three residual sub-gaps), and real-time cross-border Basel III monitoring at global volume. Every FUTURE feature has a defined SHIPPING mitigation already present in the specification.

- **Text:** [Future-Blocked_Appendix.md](https://github.com/FractonicMind/TernaryLogic/blob/main/API/Future-Blocked_Appendix.md)

### Audio Companion

Full AI-generated deep-research interview covering the relationship between ternary hardware, financial collapse prevention, and the TL governance architecture.

- **Listen:** [Preventing Financial Collapse With Ternary Hardware](https://fractonicmind.github.io/TernaryLogic/API/Preventing_Financial_Collapse_With_Ternary_Hardware.mp3)

---

## The Eight Pillars: API Coverage

| Pillar | Identifier | Primary Endpoints | Status |
|--------|-----------|-------------------|--------|
| I - Epistemic Hold | `EpistemicHold` | `POST /decisions`, `GET/PATCH /epistemic-hold/escalations/*`, `POST /gateway/lane-assignment` | SHIPPING |
| II - Immutable Ledger | `ImmutableLedger` | `POST /audit-logs`, `GET /audit-logs/{logId}`, `POST /refusals`, `GET /regulator/timestamp-verification/{logId}` | SHIPPING |
| III - Goukassian Principle | `GoukassianPrinciple` | `GET /epistemic-hold/lantern`, `GET /goukassian/signature`, `POST /goukassian/license/validate`, `POST /refusals/license-violations` | SHIPPING |
| IV - Decision Logs | `DecisionLogs` | `GET /decisions/{decisionId}`, `GET /thresholds/{domain}`, `PUT /thresholds/{domain}`, `GET /metrics/summary` | SHIPPING |
| V - Economic Rights and Transparency | `EconomicRightsAndTransparencyMandate` | `POST /evaluate/trade`, `POST /redress/*`, `GET /regulator/basel-iii/attestation`, `POST /regulator/fatf/compliance-export` | SHIPPING |
| VI - Sustainable Capital Allocation | `SustainableCapitalAllocationMandate` | `POST /evaluate/policy`, `POST /evaluate/supply-chain`, `GET /audit/compliance/attestation` | SHIPPING |
| VII - Hybrid Shield | `HybridShield` | `POST /emergency/override`, `GET /emergency/status`, `GET /audit/custodians/{id}/heartbeat`, `GET /regulator/custodian-quorum` | SHIPPING (sub-300ms cross-jurisdiction: FUTURE) |
| VIII - Anchors | `Anchors` | `GET /audit/verifications/merkle/{root}`, `GET /audit/verifications/inclusion/{logId}`, `POST /regulator/evidence-export` | SHIPPING (per-trade real-time anchoring: FUTURE) |

---

## Compliance and Regulatory Alignment

This specification operationalizes international financial and AI governance standards through machine-verifiable enforcement rather than policy declaration:

- **Basel III:** LCR >= 1.0, NSFR >= 1.0, capital adequacy, counterparty exposure, stress testing — enforced at `POST /evaluate/trade`, `GET /regulator/basel-iii/attestation`, and `RegulatoryContext.baselIii` schema fields.
- **FATF:** Recommendations 6 (targeted financial sanctions), 10, 11 (record keeping), 20 (SAR), 29 (financial intelligence) — enforced at `POST /evaluate/trade`, `POST /regulator/fatf/compliance-export`, and `RegulatoryFlags.fatfFlags` schema fields.
- **IOSCO:** Principles 34-38 (market integrity: layering, spoofing, wash trading, cross-market manipulation) — enforced at `POST /evaluate/trade`, `GET /regulator/iosco/principle-mapping`, and `RegulatoryFlags.ioscoFlags` schema fields.
- **GDPR Article 17:** The Erasure Paradox is mitigated through cryptographic erasure via HKDF-SHA3-256 key hierarchy (EKR workflow). Three residual sub-gaps documented in `Future-Blocked_Appendix.md`.
- **Paris Agreement:** Carbon footprint verification, green bond eligibility, ESG scoring — enforced at `POST /evaluate/policy`, `POST /evaluate/supply-chain`, and `RegulatoryContext.parisAgreement` schema fields.

---

## Hybrid Shield Status: Active

This specification is anchored to the TL framework's constitutional enforcement chain. The `PermissionToken.laneOrigin: const "AUDIT_LANE"` constraint means no token can claim to originate from the Inference Lane. The `unevaluatedProperties: false` constraint throughout `tl_schema.json` means no undeclared field can introduce ambiguity into the enforcement logic. The on-chain `NLNAViolation` custom error means the blockchain layer reverts any token registration attempt that lacks a previously anchored log.

| Enforcement Layer | Mechanism | File |
|-------------------|-----------|------|
| Schema | `StateEnvelope if/then` constraint | `tl_schema.json` |
| API Contract | `PermissionToken.laneOrigin: const "AUDIT_LANE"` | `tl_openapi.yaml` |
| EIP-712 | Domain separator binding to contract and chain | `eip712_typed_data.json` |
| On-Chain | `NLNAViolation` custom error in `TL_Ledger_Core` | `tl_abi.json` |
| Prose | Five-layer enforcement chain documented | `Specification_Architecture.md` |
| Audit | Full path-to-pillar-to-regulation mapping | `Constitutional_Compliance_Matrix.md` |

---

## Version and Authority

| Field | Value |
|-------|-------|
| Version | `1.0.0-tl-monograph-2026` |
| Authority | Constitutional Hardware Monograph 2026 |
| Author | Lev Goukassian - ORCID [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243) |
| Repository | [FractonicMind/TernaryLogic](https://github.com/FractonicMind/TernaryLogic) |
| Published | AI and Ethics, Springer Nature - DOI [10.1007/s43681-025-00910-6](https://doi.org/10.1007/s43681-025-00910-6) |
| Second Paper | AI and Ethics, Springer Nature - DOI [10.1007/s43681-026-01124-0](https://doi.org/10.1007/s43681-026-01124-0) |

---

### License

This work is licensed under a Creative Commons Attribution 4.0 International License (CC BY 4.0).

---

### *"If you cannot log it, you do not understand it. If you do not understand it, you have no authority to execute it."* - Lev Goukassian
