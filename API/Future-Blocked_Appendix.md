# Future-Blocked Features Appendix

## "Ternary Logic" (TL) Governance API

**Framework:** "Ternary Logic" (TL) by Lev Goukassian   
**ORCID:** 0009-0006-5966-1243   
**Repository:** FractonicMind/TernaryLogic   
**Spec Version:** 1.0.0-tl-monograph-2026   
**DOI 1:** 10.1007/s43681-025-00910-6 — "Auditable AI: Tracing the Ethical History of a Model"   
**DOI 2:** 10.1007/s43681-026-01124-0 — "A Ternary Logic Framework for Institutional Governance"   

This appendix documents all features that are architecturally desirable and constitutionally required but not buildable with 2026 production infrastructure. For each feature: the blocking monograph constraint is cited verbatim, the SHIPPING mitigation is described, the remaining unbuildable gap is explained, the `x-tl-migration-path` value is named, and all affected specification artifacts are listed.

---

## Feature 1: Real-Time Per-Trade Blockchain Anchoring

### Blocking Constraint

`x-tl-blocking-constraint: "Constitutional Hardware Monograph, Section X"`

The throughput asymmetry between institutional financial transaction volume (millions of trades per second at peak) and public blockchain confirmation latency (seconds to minutes per block, even with Layer 2 solutions) makes per-trade on-chain anchoring architecturally infeasible at the required scale without introducing confirmation latency that would breach the DLLA Governance Lane 300ms hard ceiling.

### SHIPPING Mitigation

Batch Merkle root anchoring via `TL_Ledger_Core.anchorMerkleRoot`. Multiple TGLF records are aggregated into a Merkle tree. The root of that tree is anchored on-chain in a single transaction. Any individual record can be proven included via `TL_Ledger_Core.verifyMerkleInclusion` and the API endpoint `GET /governance/verifications/inclusion/{logId}`. The batch frequency is deployment-configurable but must satisfy the requirement that any `PermissionToken.logHash` is verifiable against an on-chain Merkle root before token expiration.

### Remaining Gap After Mitigation

The SHIPPING mitigation creates a window between TGLF record commitment and on-chain anchoring. During this window, a record exists in the immutable off-chain ledger but has not yet been anchored. An adversary with access to the off-chain ledger during this window could theoretically observe unanchored records. Per-trade instant anchoring would eliminate this window entirely.

### Migration Path

`x-tl-migration-path: "Constitutional Hardware Monograph, Section X"`

Resolution depends on sufficiently low-latency, high-throughput Layer 2 or application-specific blockchain infrastructure achieving sub-100ms finality at institutional transaction volumes.

### Affected Specification Artifacts

- `tl_openapi.yaml`: `POST /governance-logs` (anchoring is batch, not per-trade)
- `tl_openapi.yaml`: `GET /governance/verifications/merkle/{merkleRoot}` (batch anchor verification)
- `tl_abi.json`: `TL_Ledger_Core.anchorMerkleRoot` (batch anchor function)
- `tl_abi.json`: `TL_Ledger_Core.registerPermissionToken` (requires prior batch anchor)
- `constitutional_compliance_matrix.md`: Implementation Gap row for this feature

---

## Feature 2: Quantum-Proof Signature Migration

### Blocking Constraint

`x-tl-blocking-constraint: "Constitutional Hardware Monograph, Section X"`

SLH-DSA-SHAKE-128s and ML-KEM-1024 are not yet available in production HSM firmware for the signing operations required by the TL governance stack. NIST finalized these algorithms but production-grade HSM support, ecosystem tooling, and regulatory acceptance for use in financial governance contexts remain in progress as of the specification date.

### SHIPPING Mitigation

ES256 (default) and Ed25519 are the SHIPPING signature algorithms. Both are present in `SignatureBlock_v1_0_0.signatureAlgorithm` enum. PQC slots are reserved: SLH-DSA-SHAKE-128s carries id 6, ML-KEM-1024 carries id 7, in both `SignatureBlock_v1_0_0` and `GoukassianSignatureAttestation.signatureAlgorithmId` in `eip712_typed_data.json`. SHIPPING implementations MUST use values 0 (ES256) or 1 (Ed25519) and MUST NOT emit reserved values 6 or 7.

### Remaining Gap After Mitigation

ES256 and Ed25519 are vulnerable to sufficiently capable quantum computers running Shor's algorithm. The time horizon for this threat is uncertain but the reservation of PQC slots enables a schema-compatible migration without a breaking change to the specification.

### Migration Path

`x-tl-migration-path: "Constitutional Hardware Monograph, Section X"`

When production HSM support for SLH-DSA-SHAKE-128s and ML-KEM-1024 is available and regulatory frameworks accept their use, SHIPPING implementations may begin emitting `signatureAlgorithmId: 6` or `signatureAlgorithmId: 7`. The schema is ready; only the implementation gate remains.

### Affected Specification Artifacts

- `tl_schema.json`: `SignatureBlock_v1_0_0.signatureAlgorithm` (PQC slots reserved)
- `eip712_typed_data.json`: `GoukassianSignatureAttestation.signatureAlgorithmId` (slots 6-7 reserved)
- `tl_openapi.yaml`: `SignatureBlock` component schema (same reservation)
- `specification_architecture.md`: Section 6 (Goukassian Principle signature algorithm note)

---

## Feature 3: Hardware Ternary Enforcement Units (TEUs) and Full DITL Deployment

### Blocking Constraint

`x-tl-blocking-constraint: "Constitutional Hardware Monograph, Section X"`

Full DITL (Delay-Insensitive Ternary Logic) deployment at TSMC N2 or Intel 18A process nodes with TaOx RRAM physical state enforcement via Window Comparator is not available in production silicon as of the specification date. The Mandated Ternary (MT) hardware layer that maps TL states to TaOx bilayer RRAM resistance values (Proceed, Epistemic Hold, Refuse encoded as distinct resistance ranges) requires foundry fabrication at advanced nodes that are not yet accessible for governance-specific ASIC deployment.

### SHIPPING Mitigation

Architecture B hybrid model: software enforcement with DITL attestation where available. The `TLCapabilityFlags.pufAttestationMode: "ARCHITECTURE_B"` flag signals this deployment posture. The `NLNAGovernanceToken.pufAttestation` field uses the sentinel value `"NULL_PUF_DEPLOYMENT"` for non-MT deployments. The `EscrowRecord.windowComparatorReading.softwareEnforcementActive: true` field confirms that software-layer enforcement is substituting for physical DITL gate enforcement.

The two DITL endpoints `POST /ditl/state-transition` and `GET /ditl/puf-attestation/{deviceId}` are defined in `tl_openapi.yaml` with `x-tl-implementation-status: FUTURE`. They are present in the specification to define the contractual interface for when MT hardware becomes available, and to enable partial deployments where some nodes have MT hardware.

### Remaining Gap After Mitigation

Software enforcement can be bypassed by a sufficiently privileged attacker with access to the runtime. Physical DITL enforcement via Window Comparator and TaOx RRAM is tamper-proof at the hardware level: the resistance values cannot be spoofed in software because the measurement is physical. Architecture B provides strong but not hardware-rooted guarantees.

The PUF Attestation Chain (enrollment, foundry attestation, NL=NA interlock verification, immutable log entry, Merkle hash chain) is fully operative only when physical PUF hardware is present. The SHIPPING compensating controls cover elements 3, 4, and 5; elements 1 and 2 require physical MT silicon.

### Migration Path

`x-tl-migration-path: "Constitutional Hardware Monograph, Section X"`

When MT silicon is available from TSMC N2 or Intel 18A, the `pufAttestationMode` flag transitions from `ARCHITECTURE_B` to `FULL_PUF`. The `NULL_PUF_DEPLOYMENT` sentinel is replaced with an actual PUF attestation hex256 value. The DITL endpoints transition from `FUTURE` to `SHIPPING`.

### Affected Specification Artifacts

- `tl_openapi.yaml`: `POST /ditl/state-transition`, `GET /ditl/puf-attestation/{deviceId}` (FUTURE)
- `tl_schema.json`: `NLNAGovernanceToken_v1_0_0.pufAttestation` (NULL_PUF_DEPLOYMENT sentinel)
- `tl_schema.json`: `EscrowRecord_v1_0_0.windowComparatorReading` (softwareEnforcementActive flag)
- `tl_schema.json`: `TLCapabilityFlags_v1_0_0.pufAttestationMode` (ARCHITECTURE_B default)
- `specification_architecture.md`: Section 11 (DITL Hardware Interface)

---

## Feature 4: Cross-Jurisdiction Custodian Quorum in Under 300ms

### Blocking Constraint

`x-tl-blocking-constraint: "Constitutional Hardware Monograph, Section X"`

Network physics and geographic distribution prevent achieving sub-300ms round-trip quorum confirmation across custodians distributed across multiple continents. The speed of light across a trans-Pacific round trip is approximately 100ms under ideal conditions. A quorum requiring acknowledgment from custodians in, for example, North America, Europe, and Asia-Pacific has a physical minimum latency floor that approaches or exceeds the DLLA Governance Lane 300ms hard ceiling, leaving no margin for processing, queuing, or jitter.

### SHIPPING Mitigation

The `GET /regulator/custodian-quorum` endpoint exposes `crossJurisdictionLatencyMs` as a monitoring field. Consumers can observe actual quorum latency and assess whether it meets their specific deployment requirements. HybridShield quorum is still required for all state-mutating `TL_Ledger_Core` operations; the SHIPPING deployment accepts that this quorum may take longer than 300ms for globally distributed custodians, and the `forcedStateExpiresAt` field on Emergency Override requests prevents indefinite constitutional suspension.

### Remaining Gap After Mitigation

The constitutional ideal is that HybridShield custodian quorum is confirmed within the Governance Lane DLLA 300ms ceiling. In globally distributed deployments, this ceiling cannot be met. Regional deployments (all custodians within a single continent) can meet the ceiling, but sacrifice geographic diversity of the HybridShield.

### Migration Path

`x-tl-migration-path: "Constitutional Hardware Monograph, Section X"`

Resolution depends on advances in low-latency global networking infrastructure or the acceptance of threshold signature schemes that allow custodians to pre-commit attestations, reducing real-time round-trip requirements.

### Affected Specification Artifacts

- `tl_openapi.yaml`: `GET /regulator/custodian-quorum` (crossJurisdictionLatencyMs field; sub-300ms marked FUTURE)
- `constitutional_compliance_matrix.md`: Implementation Gap table row for this feature

---

## Feature 5: Immutable Ledger with Native GDPR Article 17 Compliance (Erasure Paradox)

### Blocking Constraint

`x-tl-blocking-constraint: "Constitutional Hardware Monograph, Section X"`

The "Erasure Paradox" is the fundamental conflict between the ImmutableLedger pillar (all validated decisions stored as permanent tamper-proof records) and GDPR Article 17 (right to erasure). True immutability and true erasure are logically incompatible: a record that can be erased is not immutable, and a record that is immutable cannot be erased.

### SHIPPING Mitigation

Cryptographic erasure via HKDF-SHA3-256: the data is encrypted under keys derived using HKDF-SHA3-256. When erasure is required under GDPR Article 17, the encryption key is destroyed. The underlying ciphertext remains in the immutable ledger (preserving structural integrity) but becomes computationally irrecoverable (satisfying the functional requirement of erasure). The `EKRRecord_v1_0_0.hkdfSha3256Confirmed: true` field confirms this approach was used. The `RegulatoryContext.gdpr.erasureEligible` boolean triggers the EKR workflow.

### Three Remaining Sub-Gaps After Mitigation

**Sub-gap 1: Regulatory interpretation.** Some data protection authorities may not accept cryptographic erasure as equivalent to deletion under GDPR Article 17. The legal status of "computationally irrecoverable ciphertext" varies by jurisdiction and is subject to ongoing regulatory guidance.

**Sub-gap 2: Erasure key registry dependency.** The registry that maps data subjects to their encryption keys must itself be erasable when a data subject invokes Article 17. If the key registry is stored on an immutable ledger, the same paradox applies to the registry itself. A separate, non-immutable key management system is required, creating an architectural dependency outside the TL immutable ledger.

**Sub-gap 3: Metadata residue.** Even after key destruction, certain metadata may persist: log timestamps, access patterns, batch membership (which Merkle batch a log entry belonged to), and the `logId` itself. In some contexts, this metadata alone may constitute personal data under GDPR Article 4(1).

### Migration Path

`x-tl-migration-path: "Constitutional Hardware Monograph, Section X"`

Resolution of sub-gap 1 depends on regulatory guidance from EU data protection authorities. Resolution of sub-gap 2 requires a standardized approach to erasable key registries compatible with the TL governance architecture. Resolution of sub-gap 3 requires either differential privacy techniques applied to metadata or regulatory guidance that metadata residue does not constitute personal data in this context.

### Affected Specification Artifacts

- `tl_schema.json`: `EKRRecord_v1_0_0` (cryptographic erasure schema)
- `tl_schema.json`: `RegulatoryContext_v1_0_0.gdpr.erasureEligible` (trigger field)
- `tl_openapi.yaml`: `POST /redress/log-reevaluation` (original log immutable annotation)
- `specification_architecture.md`: Section 12 (EKR and GDPR Cryptographic Erasure)
- `constitutional_compliance_matrix.md`: EKRRecord rows (GDPR Article 17 nexus)

---

## Feature 6: Real-Time Cross-Border Basel III Capital Adequacy Monitoring at Global Transaction Volume

### Blocking Constraint

`x-tl-blocking-constraint: "Constitutional Hardware Monograph, Section X"`

Real-time aggregation of capital adequacy metrics (LCR, NSFR, capital ratios, counterparty exposure) across all active transactions at global financial system scale would require continuous streaming of position data from thousands of financial institutions simultaneously, aggregated and verified within the Governance Lane 300ms hard ceiling. Current data aggregation infrastructure for cross-border regulatory reporting operates on T+1 or end-of-day batches, not real-time streams.

### SHIPPING Mitigation

Periodic attestation via `GET /regulator/basel-iii/attestation`. This endpoint returns a signed attestation of the current Basel III compliance state (LCR, NSFR, capitalRatio, stressTestPassed, counterpartyExposureWithinLimits) at the time of the request. The attestation is signed via `SignatureBlock` and timestamped. Domain evaluation at `POST /evaluate/trade` carries a `RegulatoryContext.baselIii` sub-object that is evaluated per-transaction against the most recently available attestation.

The `regulatoryFrameworkVersion.baselVersion` field in `RegulatoryContext` captures which Basel III revision was applied, enabling auditors to verify that the correct standard version was in effect at decision time.

### Remaining Gap After Mitigation

The periodic attestation model creates a staleness window between attestation timestamps. A large transaction executed shortly after an attestation may reflect capital adequacy conditions that have since changed. Real-time monitoring would eliminate this window.

### Migration Path

`x-tl-migration-path: "Constitutional Hardware Monograph, Section X"`

Resolution depends on standardized real-time regulatory reporting APIs across financial institutions and sufficiently low-latency cross-border data aggregation infrastructure to satisfy the DLLA Governance Lane 300ms ceiling.

### Affected Specification Artifacts

- `tl_openapi.yaml`: `GET /regulator/basel-iii/attestation` (periodic, not real-time)
- `tl_openapi.yaml`: `POST /evaluate/trade` (RegulatoryContext.baselIii sub-object)
- `tl_schema.json`: `RegulatoryContext_v1_0_0.baselIii` (snapshot, not streaming)
- `constitutional_compliance_matrix.md`: Implementation Gap table row for this feature

---

## Constitutional Uncertainty Register - Deliverable G

| Item | Location | Issue | Assumption Made |
|---|---|---|---|
| `<MONOGRAPH_EXCERPT_MISSING>` | All six features: exact verbatim Section X blocking text | Section X of the TL Constitutional Hardware Monograph was not supplied as an excerpt. | All blocking constraints cite "Constitutional Hardware Monograph, Section X" per the constitutional prompt's explicit instruction in Section 5G: "cite the exact verbatim TL monograph section." The blocking description is derived from the functional descriptions in Section 5G of the constitutional prompt, which is the highest available authority per the source precedence hierarchy in Section 2.1. |
| `<MONOGRAPH_EXCERPT_MISSING>` | Feature 3: exact TaOx RRAM resistance values for each TLState | Specific resistance ranges not supplied as excerpts. | Resistance ranges described functionally (distinct ranges for Proceed, Epistemic Hold, Refuse) without specific ohm values. The `EscrowRecord.windowComparatorReading.resistanceRangeOhm` schema fields (minOhm, maxOhm) are present for MT deployments to populate. |
