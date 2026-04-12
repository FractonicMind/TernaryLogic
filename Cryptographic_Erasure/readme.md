# Cryptographic Erasure in Ternary Logic

*How do you delete data from a ledger that was designed never to forget?*

This is the structural paradox at the heart of Ternary Logic (TL): the same immutable, tamper-evident ledger that guarantees accountability becomes an obstacle when a data subject invokes the right to erasure, or when trade secrets embedded in decision justifications must be protected from patient adversaries with archive access.

The answer is not deletion. It is **key destruction**. When the encryption key is gone, the ciphertext remains - structurally intact, Merkle-verified, blockchain-anchored - but computationally unrecoverable. The ledger keeps its promise of immutability. The data subject gets their erasure. The trade secret disappears from any adversary without the key.

This specification documents TL's unified **Cryptographic Erasure** architecture, covering two trigger paths against a shared key destruction substrate.

---

## The Core Idea

Every Decision Log entry in TL is encrypted under an epoch key derived from three coupled sources: a hardware-attested monotonic counter, a heartbeat entropy source, and the previous epoch's Merkle root. This derivation chain provides **forward secrecy**: compromise of one epoch's key cannot reach any prior epoch.

When a data subject requests erasure, TL does not touch the ledger. Instead, it destroys the subject-specific derivation mapping in hardware-protected memory. Without that mapping, no one - not even an authorized auditor with the epoch key - can re-derive the subject's encryption key or recover their data.

Two trigger paths, one zeroization primitive:

- **Ephemeral Key Rotation (EKR)** - scheduled, automated, epoch-driven. Destroys the entire epoch key at each rotation boundary, providing forward secrecy across time.
- **Commanded Destruction** - custodian-authorized, per-subject, legally governed. Destroys only the derivation path for a specific data subject, satisfying GDPR Article 17 without affecting any other subject's data or any trade-secret content in the same epoch.

Both paths require a Destruction Event log entry to be committed to the Immutable Ledger before any zeroization executes. The No Log = No Action invariant applies unconditionally to destruction itself.

---

## Audio Introduction

🎧 [Shredding Immutable Data with Ternary Logic](https://fractonicmind.github.io/TernaryLogic/Cryptographic_Erasure/Shredding_Immutable_Data_with_Ternary_Logic.mp3)

---

## Architecture Overview

### Dual-Horizon Threat Model

![Dual-Horizon Threat Model](https://raw.githubusercontent.com/FractonicMind/TernaryLogic/main/Cryptographic_Erasure/DHTM.png)

The threat model operates on two horizons simultaneously. The first is the present-day regulatory adversary: a supervisory authority acting on behalf of a data subject under GDPR Article 17, or a passive archive reader accumulating ciphertext for later analysis. The second is the forward-looking quantum adversary: a system running Shor's algorithm against the public-key components of the architecture within the next decade.

AES-256-GCM requires no post-quantum migration - Grover's algorithm reduces 256-bit symmetric security to 128 bits, which remains computationally infeasible. Migration effort concentrates on key encapsulation (ML-KEM-1024, NIST FIPS 203) and epoch attestation signatures (SLH-DSA-SHAKE-128s, NIST FIPS 205).

---

### Hardware Root of Trust

![Hardware Root of Trust Platform Architecture](https://raw.githubusercontent.com/FractonicMind/TernaryLogic/main/Cryptographic_Erasure/Luna7.png)

The epoch counter, entropy source, and zeroization primitive are all anchored in a Hardware Root of Trust. TPM 2.0 is the named baseline - NV Index with TPMA_NV_COUNTER attribute, TPM2_NV_Increment for counter advance, TPM2_NV_Certify for attestation. Thales Luna 7 HSM and RISC-V Keystone TEE are secondary compatibility targets.

A critical constraint governs all deployments: **direct HRoT NV access is prohibited in the Fast Lane path** (sub-2ms decisions). Fast Lane operations use TEE-cached epoch keys only. HRoT attestation occurs asynchronously in the Governance Lane, once per 30-second Merkle batch. This Fast Lane Prohibition resolves the fundamental latency conflict between TPM 2.0's 5-15ms NV operation latency and the 2ms decision budget.

---

### Post-Quantum Key Architecture

![Root of Trust Post-Quantum Integration](https://raw.githubusercontent.com/FractonicMind/TernaryLogic/main/Cryptographic_Erasure/RoT.png)

The key hierarchy is built on HKDF-SHA3-256. Each epoch key derives from: the HRoT counter attestation quote, 256 bits of TRNG heartbeat entropy validated per NIST SP 800-90B, and the previous epoch's Merkle root. This three-input construction ensures epoch key independence: no single compromised input can reproduce any other epoch's key.

Per-subject keys derive from the epoch key via HMAC-SHA3-512 over the subject pseudonym and epoch number. They are never stored - re-derived on demand and destroyed after use. A separate audit key branch derives from a master audit secret under distinct key material, ensuring auditors can access specific epochs without ever holding the epoch encryption key itself.

---

## Interactive Specification

[TL Cryptographic Erasure - Full Interactive Specification](https://fractonicmind.github.io/TernaryLogic/Cryptographic_Erasure/TL_Cryptographic_Erasure.html)

The interactive specification covers all eight sections of the architecture with navigable sidebar, dark-navy styling, and cross-referenced subsections.

---

## Specification Documents

The full specification is produced as a dual-spec: two independent research runs generating parallel documents that are compared rather than merged. Citation provenance is kept clean within each specification.

### Primary Specification (Spec A)

**Step 1 - Threat Models, Key Hierarchy, and Hardware Root of Trust**   
[TL_CE_Threat_Models_Key_Hierarchy_HRoT.md](https://github.com/FractonicMind/TernaryLogic/blob/main/Cryptographic_Erasure/TL_CE_Threat_Models_Key_Hierarchy_HRoT.md)

Establishes the three-class trade-secret threat model, the GDPR erasure threat model with EDPB Guidelines 02/2025 and CNIL blockchain guidance, the unified destruction guarantee, the HKDF-SHA3-256 epoch key derivation construction, the PRF-based subject-derived key hierarchy, the five-state key lifecycle mapped to TL ternary states, the Fast Lane Prohibition with benchmark-cited timing budget, and the SP 800-90B heartbeat entropy specification.

**Step 2 - NL=NA Integration, Merkle Architecture, and Commanded Destruction**   
[TL_CE_NL_NA_Merkle_Integration_Commanded_Destruction.md](https://github.com/FractonicMind/TernaryLogic/blob/main/Cryptographic_Erasure/TL_CE_NL_NA_Merkle_Integration_Commanded_Destruction.md)

Specifies the DITL gate interaction with epoch key availability, the RFC 6962 domain-separated Merkle leaf construction, the epoch map mechanism preventing epoch substitution attacks, Hybrid Shield operation ordering, anchor timing decoupling with TRNG jitter, the FROST 3-of-5 and 5-of-7 threshold erasure authorization protocol, Subject Derivation Table zeroization with random-data overwrite, and the dual-regime SEC Rule 17a-4 and GDPR Article 17 compliance framework.

**Step 3 - Post-Quantum Migration, Formal Verification, Test Vectors, and Diagrams**   
[TL_CE_Post_Quantum_Formal_Verification_Test_Vectors_Diagrams.md](https://github.com/FractonicMind/TernaryLogic/blob/main/Cryptographic_Erasure/TL_CE_Post_Quantum_Formal_Verification_Test_Vectors_Diagrams.md)

Covers ML-KEM-1024 and SLH-DSA-SHAKE-128s migration paths with CNSA 2.0 deadlines, the three-phase epoch chain migration protocol, four NuSMV-verified LTL properties with complete model code, the full attack surface control table with seven vectors, five NIST CAVP-style test vectors including avalanche and dependency chain negative cases, and four mandatory Mermaid diagrams covering epoch boundary atomicity, key lifecycle state machine, Fast Lane timing separation, and commanded destruction governance flow.

**Step 4 - Threat Boundary, Residual Risk, and Integration Review**   
[TL_CE_Threat_Boundary_Residual_Risk_Integration_Review.md](https://github.com/FractonicMind/TernaryLogic/blob/main/Cryptographic_Erasure/TL_CE_Threat_Boundary_Residual_Risk_Integration_Review.md)

The governance council acceptance document. Names the three explicit protections (content confidentiality, forward secrecy, GDPR compliance), the four non-protection boundaries (authorized insider access, traffic analysis, metadata inference, physical key extraction), four signable residual risk acceptance statements, the degraded mode disclosure required for software-only deployments, and a five-constraint cross-reference consistency index verifying the specification is internally contradiction-free.

---

### Parallel Specification (Spec B)

**Step 1 - Architectural Blueprint: Threat Model, Key Hierarchy, and Hardware Root of Trust**   
[TL_CE_Architectural_Blueprint_Threat_Model_Key_Hierarchy_HRoT.md](https://github.com/FractonicMind/TernaryLogic/blob/main/Cryptographic_Erasure/TL_CE_Architectural_Blueprint_Threat_Model_Key_Hierarchy_HRoT.md)

A dual-horizon threat model treating current regulatory adversaries and quantum adversaries as simultaneous planning horizons. Produces pseudocode for all three derivation functions (epoch key, subject key, audit key) alongside state transition tables, and includes an explicit platform divergence analysis comparing TPM 2.0, Thales Luna 7 HSM, and RISC-V Keystone TEE on attestation latency and Fast Lane enforcement requirements.

**Step 2 - Architecting Contradiction: GDPR Erasure and SEC Recordkeeping in Ternary Logic**   
[TL_CE_Architecting_Contradiction_GDPR_SEC_Compliance.md](https://github.com/FractonicMind/TernaryLogic/blob/main/Cryptographic_Erasure/TL_CE_Architecting_Contradiction_GDPR_SEC_Compliance.md)

Addresses the apparent conflict between GDPR Article 17 (erasure) and SEC Rule 17a-4 (mandatory retention) and resolves it architecturally: the Destruction Event log entry is proof of erasure, not the erased content, so its retention does not contradict the erasure it documents. Specifies auditor verification procedures for structural integrity confirmation without epoch key access, using Merkle inclusion proofs, consistency proofs, and epoch map validation.

**Step 3 - Post-Quantum Migration, Formal Verification, Attack Surface, and Diagrams**   
[TL_CE_Post_Quantum_Verification_Attack_Surface_Diagrams.md](https://github.com/FractonicMind/TernaryLogic/blob/main/Cryptographic_Erasure/TL_CE_Post_Quantum_Verification_Attack_Surface_Diagrams.md)

Parallel coverage of ML-KEM-1024 and SLH-DSA migration, four LTL formal properties, seven-row attack surface control matrix, five NIST CAVP-style test vectors, and four Mermaid diagrams. Notable contribution: the platform divergence table carried forward from Step 1 clarifying that low-latency HSM and TEE platforms must enforce the Fast Lane Prohibition logically even when hardware latency would physically permit HRoT access in the sub-2ms window.

**Step 4 - Defining the Guardrails: A Governance Framework for Ternary Logic Cryptographic Erasure**   
[TL_CE_Defining_the_Guardrails.md](https://github.com/FractonicMind/TernaryLogic/blob/main/Cryptographic_Erasure/TL_CE_Defining_the_Guardrails.md)

Governance framework covering deployment checklist, custodian ceremony runbooks for epoch rotation and subject-scope erasure, incident response procedures mapped to TL states, and a consolidated cross-reference index linking every requirement to its originating standard across FIPS 140-3, FIPS 203, FIPS 205, SP 800-38D, SP 800-90B, SEC 17a-4, FINRA 4511, and GDPR Articles 17 and 5(2).

---

## Where This Fits in Ternary Logic

Cryptographic Erasure is the confidentiality and rights layer of TL's accountability stack. It operates above the Merkle_Architecture (which provides structural integrity) and the No_Log-No_Action invariant (which enforces evidentiary sequencing), and below the Adversarial_Survivability analysis (which stress-tests all pillars under determined attack).

The Ephemeral Key Rotation mechanism was identified in the Constitutional Survivability analysis as a specified but not fully developed component of the Hybrid Shield pillar. This folder constitutes its complete specification.

---

## Published Research

**First Paper:** Goukassian, L. (2025). Auditable AI: Tracing the Ethical History of a Model. *AI and Ethics*, Springer Nature.   
[https://doi.org/10.1007/s43681-025-00910-6](https://doi.org/10.1007/s43681-025-00910-6)

**Second Paper:** Accepted April 1, 2026. A Ternary Logic Framework for Institutional Governance. *AI and Ethics*, Springer Nature.

**SSRN Working Paper:** Atomic Auditability in Financial Execution Pipelines via Hardware-Enforced Ternary States.    
[https://doi.org/10.5281/zenodo.18716142](https://doi.org/10.5281/zenodo.18716142)

---

*Ternary Logic is a Global Decision Systems architecture. ORCID: 0009-0006-5966-1243*
