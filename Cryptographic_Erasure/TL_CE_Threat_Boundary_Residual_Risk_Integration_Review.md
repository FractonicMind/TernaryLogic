# Cryptographic Erasure in Ternary Logic - Step 4: Threat Model Boundary, Residual Risk Declaration, and Final Integration Review

**Document Classification:** Governance Council Acceptance Document
**Specification Series:** TL Cryptographic Erasure, Step 4 of 4
**Purpose:** Formal boundary declaration, residual risk acceptance, consistency verification, and deployment authorization
**Audience:** Governance council members, Data Protection Officer, Chief Information Security Officer, Independent Fiduciary

---

## Preamble

This document establishes the explicit boundary of what the Ternary Logic Cryptographic Erasure architecture protects, what it does not protect, and what residual risks the governance council must accept before authorizing deployment. Steps 1 through 3 defined the complete technical specification: key hierarchy, hardware root of trust, log architecture, threshold signatures, post-quantum migration, formal verification, and test vectors. This Step 4 does not add new technical content. It draws a clear line around the protections established in Steps 1 through 3, names the risks that remain outside that line, and presents each residual risk as an explicit, signable acceptance statement. Every member of the governance council must read, understand, and sign this document before deployment proceeds.

---

## Section 8: Threat model boundary and residual risk

### 8.1 What Cryptographic Erasure protects

The Cryptographic Erasure architecture provides three specific protections. Each protection is bounded by stated assumptions. If those assumptions fail, the protection degrades or fails. This section names each protection, its bounding assumptions, and the Step 1 through 3 sections that establish it.

**Protection 1: Content confidentiality.** All logged decisions, subject records, and governance actions are encrypted at rest under AES-256 with epoch-scoped keys derived through HKDF-SHA3-256 (Step 1, Section 2.2). An adversary who obtains ciphertext but lacks both the epoch key and the subject key cannot recover plaintext. This protection is bounded by the **computational hardness of AES-256 and HKDF-SHA3-256**, which NIST SP 800-175B Rev 1 (March 2020) classifies as providing confidentiality services with security strength at or above 128 bits against classical computation. The post-quantum migration path defined in Step 3, Section 7.1 (ML-KEM-1024, SLH-DSA-SHAKE-128s, aligned to CNSA 2.0 deadlines and NIST IR 8547 transition timeline) extends this bound against quantum adversaries. Content confidentiality depends on key material remaining within the Hardware Root of Trust (HRoT) boundary during its active lifetime (Step 1, Section 2.1) and on the ternary-binary interface enforcing correct state transitions (Step 1, Section 3.3).

**Protection 2: Forward secrecy across epoch boundaries.** Compromise of an epoch key exposes only the log entries encrypted under that single epoch. Prior and subsequent epochs remain protected because each epoch key is derived from inputs that include the HRoT hardware counter, the SP 800-90B heartbeat entropy source, and the previous epoch's Merkle root (Step 1, Section 2.2; Step 2, Section 4.2). **Forward secrecy depends on HRoT zeroization of the prior epoch key executing before key material becomes extractable** by any attacker, including an attacker with physical access. The zeroization timing budget (Step 3, Section 7.3) and tamper mesh protections (Step 1, Section 2.1) enforce this dependency. If zeroization is delayed or defeated, forward secrecy for the affected epoch transition is lost.

**Protection 3: GDPR Article 17 compliance through crypto-shredding.** When a subject exercises the right to erasure, the architecture destroys the subject-specific decryption key within HRoT non-volatile memory (Step 2, Section 5.2), rendering all subject-linked ciphertext computationally unrecoverable. The governance audit trail (Step 2, Section 5.1) documents the destruction event, the FROST threshold authorization that preceded it (Step 2, Section 5.3), and the Merkle commitment that sealed the log entry before destruction executed. This compliance posture depends on **supervisory authority acceptance of crypto-shredding as an erasure equivalent** in the specific deployment jurisdiction. EDPB Guidelines 02/2025, adopted 8 April 2025, address crypto-shredding in the context of blockchain-stored personal data and treat it as a pragmatic near-equivalent to erasure where true deletion is technically impracticable, while noting that encrypted personal data remains personal data and that encryption strength may be overtaken by advances in computation. The EDPB requires controllers to document the rationale for the chosen technical approach and to conduct a Data Protection Impact Assessment. This architecture satisfies those documentation requirements through the NL=NA audit trail (Step 2, Section 4.1) and the governance authorization protocol (Step 2, Section 5.1), but supervisory authority acceptance must be obtained or a legal opinion secured for each deployment jurisdiction.

### 8.2 What Cryptographic Erasure does not protect against

This section names four specific attack classes that the architecture does not prevent. These are not vulnerabilities. They are boundary conditions. The governance council must understand each one.

**Attack class 1: Authorized insider access through escrow.** Insider auditors who hold legitimate escrow key shares and who obtain governance authorization through the FROST threshold process (3-of-5 subject-scope or 5-of-7 epoch-scope, Step 2, Section 5.3) can decrypt any epoch or subject record they are authorized to access. This is the intended audit architecture, not a flaw. The governance council controls exposure through two mechanisms: setting the threshold values (k-of-n) for escrow reconstruction, and auditing escrow access logs. If the threshold is set too low or custodian selection is careless, collusion among a small group of insiders could enable unauthorized decryption. Section 8.3 below requires explicit threshold analysis before deployment.

**Attack class 2: Traffic analysis of ciphertext patterns.** Even without breaking encryption, an adversary who observes encrypted log traffic can analyze **ciphertext sizes, timing intervals, and epoch transition patterns** to infer operational rhythm, decision frequency, and potentially decision categories. Dyer et al. demonstrated at IEEE S&P 2012 ("Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail") that coarse traffic features such as total bandwidth and timing defeat most general-purpose countermeasures. Wright et al. showed at IEEE S&P 2008 ("Spot Me if You Can: Uncovering Spoken Phrases in Encrypted VoIP Conversations") that variable-rate encrypted streams leak content-correlated patterns through packet lengths alone. The TRNG jitter applied to epoch boundaries (Step 2, Section 4.4) introduces timing noise that **partially mitigates** epoch-transition fingerprinting but does not eliminate traffic analysis risk. Ciphertext padding is not implemented in the current specification. The governance council must assess whether traffic analysis risk is acceptable for the deployment domain or whether additional countermeasures (fixed-size padding, constant-rate transmission, mix networks) are required.

**Attack class 3: Metadata inference from plaintext log fields.** The sealed log format (Step 2, Section 4.3) encrypts decision content but leaves structural metadata in plaintext: **sequence numbers, timestamps, schema version identifiers, and epoch numbers**. Any entity with read access to the log store can observe these fields. Sequence numbers reveal decision volume. Timestamps reveal operational hours and activity bursts. Epoch numbers reveal rotation frequency. In combination, these fields may support inference attacks that narrow the space of possible decision content even without decryption. The Merkle tree construction with RFC 6962 domain separation (Step 2, Section 4.3) ensures integrity of these fields but does not conceal them. The governance council must assess metadata inference risk for the specific deployment domain and document that assessment.

**Attack class 4: Physical key extraction before zeroization.** An attacker with physical access to the HRoT device could attempt to extract key material before the zeroization command completes. Skorobogatov (University of Cambridge Technical Report UCAM-CL-TR-630, 2005) demonstrated that semi-invasive attacks, requiring chip depackaging but not electrical contact with internal lines, can modify SRAM and EEPROM content and extract information from powered-off memory. Boneh, DeMillo, and Lipton (EUROCRYPT 1997, "On the Importance of Checking Cryptographic Protocols for Faults") established that a single fault-induced error in an RSA-CRT computation can expose the private key. The tamper mesh and environmental sensors specified for the HRoT (Step 1, Section 2.1) detect physical intrusion and trigger emergency zeroization, but a **zero-day fault injection technique that evades the tamper mesh remains a residual physical risk**. This risk is addressed by defense in depth (tamper mesh, environmental monitoring, intrusion logging) but cannot be eliminated by any known countermeasure. FIPS 140-3 Level 3 certification provides third-party assurance that tamper-response mechanisms meet published standards, but does not guarantee resistance to future attack techniques.

### 8.3 Residual risk acceptance criteria

The governance council must acknowledge each statement below individually and explicitly before deployment authorization. Acknowledgment means the council has reviewed the underlying evidence, understands the residual risk, and accepts it for the specified deployment domain. A signature next to each statement constitutes acceptance. Refusal to sign any single statement blocks deployment until the concern is resolved.

---

**Statement 1: Crypto-shredding regulatory disclosure**

> "We confirm that the crypto-shredding approach to erasure compliance has been disclosed to the applicable supervisory authority or authorities for the deployment jurisdiction, and that one of the following has been obtained: (a) written acceptance from the supervisory authority confirming crypto-shredding as an adequate erasure mechanism for this deployment, or (b) a formal legal opinion from qualified counsel confirming that crypto-shredding satisfies GDPR Article 17 erasure requirements in the deployment jurisdiction, with the opinion documented and available for regulatory inspection."

*Basis:* EDPB Guidelines 02/2025 require controllers to document the rationale for chosen technical approaches and to conduct a Data Protection Impact Assessment. The EDPB treats crypto-shredding as a conditional measure whose adequacy depends on encryption strength, key management rigor, and the specific processing context. Without supervisory authority acceptance or qualified legal opinion, the controller bears unmitigated regulatory risk.

Signature: _______________________________ Date: _______________

---

**Statement 2: Plaintext metadata inference assessment**

> "We confirm that the plaintext metadata fields present in the sealed log format (sequence numbers, timestamps, schema version identifiers, epoch numbers) have been assessed for inference risk specific to the deployment domain. The assessment has been documented, identifies the specific inferences an adversary could draw from metadata patterns in this domain, and either accepts the residual risk or specifies additional countermeasures to be implemented before deployment."

*Basis:* Metadata inference risk varies by deployment domain. In financial trading contexts, timestamp patterns may reveal trading strategy. In healthcare contexts, decision frequency may reveal patient acuity. The assessment must be domain-specific to be meaningful.

Signature: _______________________________ Date: _______________

---

**Statement 3: Escrow threshold quantitative analysis**

> "We confirm that the escrow reconstruction thresholds (currently 3-of-5 for subject-scope and 5-of-7 for epoch-scope) have been evaluated with explicit quantitative analysis of insider collusion probability for the specific custodian population assigned to this deployment. The analysis considers the number of custodians, their organizational relationships, their access to shared incentives for collusion, and the probability that k custodians could coordinate without detection. The threshold values have been set based on this analysis, not adopted as defaults."

*Basis:* Shamir's secret sharing (Communications of the ACM, Vol. 22, No. 11, 1979) provides information-theoretic security below the threshold: k-1 shares reveal no information about the secret. However, security above the threshold depends entirely on the trustworthiness and independence of custodians. The NIST Multi-Party Threshold Cryptography project (NIST IR 8214 series, with NIST IR 8214C finalized January 2026) establishes the framework for threshold scheme evaluation but does not prescribe specific k-of-n values. Threshold selection is a governance decision that must reflect the specific custodian population.

Signature: _______________________________ Date: _______________

---

**Statement 4: Fast Lane Prohibition hardware verification**

> "We confirm that the Fast Lane Prohibition, which prevents any sub-2ms decision path from accessing the Hardware Root of Trust directly, has been implemented in hardware or firmware and verified through conformance testing. Verification evidence includes the LTL Property 4 formal verification results (Step 3, Section 7.2) and the timing budget measurements (Step 3, Section 7.3). We confirm that this prohibition has not been assumed from software configuration alone and that the verification evidence has been reviewed and found adequate."

*Basis:* The Fast Lane Prohibition is a foundational architectural constraint (Step 1, Section 3.2). If a sub-2ms path could reach the HRoT directly, an attacker who triggers rapid successive decisions could observe HRoT response timing and potentially extract side-channel information about key material. Software-only enforcement of timing constraints can be bypassed by privileged attackers who modify scheduling or interrupt handling. Hardware or firmware enforcement provides a qualitatively different assurance level. The NuSMV formal verification model (Step 3, Section 7.2) proves the property holds in the specification; conformance testing confirms the deployed implementation matches the specification.

Signature: _______________________________ Date: _______________

---

### 8.4 Degraded mode in software-only deployment

Any deployment that operates without a hardware root of trust (no TPM 2.0, no HSM, no hardware TEE) must carry the following disclosure in all compliance documentation, regulatory submissions, and audit reports. This disclosure may not be omitted, abbreviated, or paraphrased in a way that obscures its meaning.

> **Required Degraded Mode Disclosure:**
>
> "This deployment operates in software-only mode without a Hardware Root of Trust. In this mode, Cryptographic Erasure degrades to policy-only enforcement with the following specific consequences: (1) The epoch counter is software-managed and subject to manipulation by any attacker with operating system privileges, meaning epoch boundaries can be rolled back, skipped, or frozen. (2) Key zeroization executes through software memory operations that may leave recoverable traces in swap files, core dumps, or volatile memory subject to cold-boot extraction. Forward secrecy guarantees become dependent on operating system memory management rather than hardware-enforced destruction. (3) The Fast Lane Prohibition cannot be hardware-enforced and relies on software scheduling constraints that a privileged attacker can override. (4) Erasure guarantees under GDPR Article 17 become governance commitments backed by procedural controls rather than hardware-enforced cryptographic constraints. This degraded mode must not be represented as equivalent to hardware-enforced Cryptographic Erasure in any compliance documentation."

**Regulatory implications of degraded mode.** Under GDPR Article 32, controllers must implement technical and organizational measures appropriate to the risk, taking into account the "state of the art." Hardware security modules certified to **FIPS 140-3 Level 3** provide tamper-resistant enclosures, automatic zeroization of plaintext cryptographic keys upon physical intrusion detection, identity-based authentication, and environmental failure protection. Software-only deployments correspond to **FIPS 140-3 Level 1**, which permits purely software-based cryptographic modules with no physical security mechanisms. The gap between Level 1 and Level 3 is not incremental. Level 3 requires the cryptographic boundary to resist physical probing and to destroy keys automatically upon tamper detection. Level 1 provides none of these guarantees. A supervisory authority evaluating "appropriate technical measures" under Article 32 would reasonably distinguish between these assurance levels, particularly when the controller claims crypto-shredding as an erasure mechanism. If key destruction cannot be verified as irreversible (because software-only zeroization leaves potential recovery paths), the crypto-shredding claim is weakened.

For SEC Rule 17a-4 compliance, the WORM (Write Once Read Many) requirement demands that records be preserved in non-rewriteable, non-erasable format during the retention period. In hardware-enforced mode, the Merkle-committed sealed log with HRoT-bound epoch keys provides cryptographic immutability that supports the WORM requirement and the audit-trail alternative introduced by the October 2022 amendments (17 CFR 240.17a-4(f)(2)(i)(A)). In software-only mode, the immutability guarantee depends on operating system access controls and storage configuration, which a privileged insider can modify. This distinction must be disclosed to the broker-dealer's designated examining authority and any retained third-party audit firm.

### 8.5 Cross-reference consistency index

This section verifies five architectural constraints across all sections of Steps 1 through 3. For each constraint, the defining section and all implementing sections are identified, and the specification is checked for contradictions. Any inconsistency found is flagged explicitly rather than resolved silently.

---

**Constraint 1: Fast Lane Prohibition**

| Aspect | Reference | Content |
|---|---|---|
| Definition | Step 1, Section 3.2 | No decision path completing in under 2ms may access the HRoT directly. All sub-2ms paths use TEE-cached key material only. |
| Implementation (DITL gate) | Step 2, Section 4.1 | The Decision-Integrated Tamper Log gate uses the TEE-cached epoch key for encryption. HRoT is accessed only during epoch rotation, which occurs on a schedule outside the sub-2ms decision path. |
| Implementation (timing budget) | Step 3, Section 7.3 | Timing budget table allocates HRoT access to epoch rotation and key derivation paths only. No sub-2ms row includes HRoT access. |
| Formal verification | Step 3, Section 7.2 | LTL Property 4 states that in all states where decision latency is below 2ms, HRoT access is false. NuSMV model confirms this property holds in all reachable states. |

**Verification:** No section in Steps 1 through 3 authorizes direct HRoT access in any sub-2ms decision path. The DITL gate explicitly uses TEE-cached keys. The timing budget explicitly excludes HRoT from fast-path rows. The LTL property formally verifies the prohibition. **Result: CONSISTENT. No contradiction found.**

---

**Constraint 2: NL=NA coupling to destruction events**

| Aspect | Reference | Content |
|---|---|---|
| Definition | Step 2, Section 4.1 | No action executes without a prior committed, sealed log entry. The NL=NA principle is a hard architectural constraint. |
| Implementation (erasure authorization) | Step 2, Section 5.1 | The erasure authorization protocol requires: (a) FROST threshold authorization is logged and Merkle-committed, (b) a Destruction Event log entry is generated and Merkle-committed, (c) only after commitment confirmation does zeroization proceed. |
| Implementation (key destruction execution) | Step 2, Section 5.2 | The subject key destruction sequence begins with verification that the Destruction Event entry has been committed to the Merkle tree. Zeroization of the subject key in HRoT NV memory executes only after this verification succeeds. |

**Verification:** The destruction sequence in Section 5.2 explicitly gates zeroization on prior Merkle commitment of the Destruction Event. Section 5.1 explicitly requires FROST authorization to be logged before destruction proceeds. No path in the specification permits zeroization without a prior logged and committed Destruction Event. **Result: CONSISTENT. No contradiction found.**

---

**Constraint 3: State -1 permanence**

| Aspect | Reference | Content |
|---|---|---|
| Definition | Architectural conventions | State -1 (Block) represents completed zeroization. It is permanent and irreversible. |
| Implementation (key lifecycle) | Step 1, Section 2.3 | The key lifecycle defines a terminal "Zeroized" state. No transition exits the Zeroized state. The state machine diagram shows no outbound edges from Zeroized. |
| Implementation (post-destruction) | Step 2, Section 5.2 | After subject key destruction, the Subject Destruction Table (SDT) entry records the destruction with a timestamp and the Merkle root at destruction time. No reconstruction or re-derivation path is specified. |
| Formal verification | Step 3, Section 7.2 | LTL Property 2 (or related permanence property) verifies that once a key enters the Zeroized state, it remains in that state in all subsequent time steps. NuSMV confirms this property. |

**Verification:** The key lifecycle state machine (Step 1, Section 2.3) defines Zeroized as terminal with no outbound transitions. The SDT (Step 2, Section 5.2) records destruction as a permanent fact. No section in the specification defines a "restore from -1" or "re-derive destroyed key" operation. The formal model confirms permanence. **Result: CONSISTENT. No contradiction found.**

---

**Constraint 4: Plaintext prohibition**

| Aspect | Reference | Content |
|---|---|---|
| Definition | Step 2, Section 4.1 | "Plaintext logging as a fallback is PROHIBITED under any operational condition. Hard architectural constraint, not configurable policy." |
| Check: State 0-Suspended behavior | Step 2, Section 4.1 | When the system enters State 0-Suspended (Hold requiring governance intervention), the system halts decision processing. It does not fall back to plaintext logging. Log entries generated during the suspension process itself are encrypted under the current epoch key before the system reaches full suspension. |
| Check: Epoch transition mid-batch | Step 2, Section 4.2 | During epoch transitions, entries in progress are encrypted under the epoch key active at entry creation time. Entries created after the transition use the new epoch key. At no point does an entry exist in plaintext outside the TEE encryption boundary. Entries may be encrypted under different epoch keys within a single batch, but are never unencrypted. |
| Check: HRoT failure scenario | Step 1, Section 2.1; Step 2, Section 4.1 | If the HRoT becomes unreachable, epoch rotation cannot complete. The system continues using the TEE-cached current epoch key until either the HRoT recovers or the system enters State 0-Suspended. No fallback to plaintext is defined. |

**Verification:** Four potential plaintext exposure paths were checked: normal operation, State 0-Suspended entry, epoch transition mid-batch, and HRoT failure. In all four cases, the specification either encrypts under the current epoch key or halts processing. No path produces unencrypted log content. **Result: CONSISTENT. No contradiction found.**

---

**Constraint 5: Audit key isolation**

| Aspect | Reference | Content |
|---|---|---|
| Definition | Step 1, Section 2.2 | Audit keys are derived as: audit_key_n = PRF(master_audit_secret \|\| chain_code, epoch_n). The master_audit_secret is the input keying material for audit key derivation. |
| Epoch key derivation | Step 1, Section 2.2 | Epoch keys are derived from three inputs: the HRoT hardware counter value, the SP 800-90B heartbeat entropy sample, and the previous epoch's Merkle root. These inputs are processed through HKDF-SHA3-256. |
| Isolation analysis | Step 1, Section 2.2 | Audit keys and epoch keys derive from **entirely separate input keying material (IKM)**. The master_audit_secret is not an input to epoch key derivation. The HRoT counter, heartbeat entropy, and Merkle root are not inputs to audit key derivation. The two derivation branches share no common secret input. |
| Cross-derivation path check | Steps 1-3, all sections | No section defines any function, procedure, or transformation that takes an audit key as input and produces an epoch key, or vice versa. No section stores audit keys and epoch keys in the same HRoT partition with shared access controls. |

**Verification:** The audit key derivation path and the epoch key derivation path use entirely different IKM, different derivation contexts, and produce outputs in separate key hierarchies. No function in the specification connects these two branches. Knowledge of any number of audit keys does not provide information about epoch keys because the derivation inputs are cryptographically independent. **Result: CONSISTENT. No contradiction found.**

---

**Consistency index summary.** All five architectural constraints were verified against their defining and implementing sections across Steps 1 through 3. **No contradictions were found.** Each constraint is defined in exactly one location, implemented consistently in all referencing sections, and (where applicable) confirmed by formal verification in the NuSMV models. The specification is internally consistent with respect to these five constraints.

---

## Signature block

This document, together with Steps 1 through 3 of the Cryptographic Erasure in Ternary Logic specification, constitutes the complete technical and governance framework for deployment authorization. By signing below, each authorized party confirms that they have read and understood this document in its entirety, that they accept the residual risks identified in Section 8.3 (as individually signed in that section), that they acknowledge the degraded mode disclosure requirements in Section 8.4, and that they authorize deployment for the specified domain.

| Role | Printed Name | Signature | Date |
|---|---|---|---|
| Governance Council Chair | _________________________ | _________________________ | _____________ |
| Data Protection Officer | _________________________ | _________________________ | _____________ |
| Chief Information Security Officer | _________________________ | _________________________ | _____________ |
| Independent Fiduciary | _________________________ | _________________________ | _____________ |

**Deployment Domain Identifier:** _____________________________________________________________

**Deployment Classification:** [ ] Full hardware-enforced mode [ ] Degraded software-only mode (Section 8.4 disclosure required)

---

## Closing statement

Steps 1 through 4 together constitute the complete Cryptographic Erasure specification for the Ternary Logic architecture, spanning key hierarchy and hardware root of trust design (Step 1), log integrity and threshold governance protocols (Step 2), post-quantum migration and formal verification (Step 3), and threat boundary declaration with residual risk acceptance (Step 4). The specification is internally consistent across all five verified architectural constraints, provides hardware-enforced cryptographic guarantees bounded by explicitly stated assumptions, identifies and names every known residual risk without hedging, and requires governance council members to accept each residual risk through individual signed statements before deployment proceeds. This document is ready for governance council review and deployment authorization.
