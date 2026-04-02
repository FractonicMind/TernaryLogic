# **Structural, Adversarial, and Availability-Hardened Merkle Architecture for Ternary Logic (TL)**

# **Structural, Adversarial, and Availability-Hardened Merkle Architecture for Ternary Logic (TL)**

**Author:** Lev Goukassian 

**Document Classification:** Technical Specification 

**Version:** 1.0 **Date:** 2026-03-31

---

## **Executive Summary**

This report provides a comprehensive technical specification for the Merkle tree architecture underlying Ternary Logic (TL), a governance framework operating with a strict ≤2 millisecond transaction execution latency requirement. The Merkle structure is not an optional component of TL but rather its foundational structural substrate, providing tamper-evident commitment, causal ordering, and cryptographically enforceable contextual integrity for triadic state transitions.

The architecture addresses a sophisticated threat model encompassing malicious insiders, external attackers, infrastructure compromise, and systemic failure modes including cryptographic degradation and data loss events. The design enforces Invariant III — the Execution Legitimacy Constraint — which mandates that no transaction commit or actuation command is valid absent a corresponding Merkle-committed log entry.

Key architectural decisions include: ternary branching topology natively aligned with TL’s triadic logic (Act \+1, Epistemic Hold 0, Refuse −1); hierarchical integrity domains separating Economic Systems, Financial Infrastructure, and Cyber-Physical Systems; a maximum 500-millisecond deferred anchoring window with cryptographic cascade binding; and a data availability strategy ensuring no Merkle root exists without retrievable backing data. The system supports logarithmic-size SPV proofs verifiable on commodity hardware, enabling regulators and independent auditors to inspect specific events without full system replication.

Formal integrity guarantees are established under standard cryptographic assumptions (collision resistance, preimage resistance, second-preimage resistance) with explicit degradation conditions and post-quantum migration pathways. Comparative analysis against Bitcoin Merkle trees, Ethereum’s state trie, Certificate Transparency logs, and Sparse Merkle Trees demonstrates TL’s specialized positioning for governance-critical, high-frequency, causally ordered decision recording.

---

## **Table of Contents**

* [Section 0 — System Model](#bookmark=id.y7yp8vb53547)

* [Section 1 — Merkle as a Core Structural Component of TL](#bookmark=id.iors8qlfrjc4)

* [Section 2 — Canonical Leaf Node Specification](#bookmark=id.bhp0ayvuf2y4)

* [Section 3 — Merkle Tree Construction Model](#bookmark=id.ac0hp4hvnti9)

* [Section 4 — Hierarchical Integrity Model](#bookmark=id.zbe1ivu8d011)

* [Section 5 — Anchoring Strategy (Time-Bound Enforcement)](#bookmark=id.dn50ks35kmgs)

* [Section 6 — Causal Integrity Enforcement (Epistemic Hold Protection)](#bookmark=id.352xoslp3z27)

* [Section 7 — Proof Generation and Verification](#bookmark=id.50gc3wybprce)

* [Section 8 — Data Availability (DA) Strategy](#bookmark=id.aauexgqawdlt)

* [Section 9 — Log Truncation and Tamper Resistance](#bookmark=id.3nrt4p3gaqav)

* [Section 10 — Latency and Throughput Modeling](#bookmark=id.ik0dy4oav26s)

* [Section 11 — Formal Integrity Guarantees](#bookmark=id.di3js8iahmnr)

* [Section 12 — Comparative Analysis](#bookmark=id.hxtdy0wy4vai)

* [Section 13 — Failure Mode Disclosure](#bookmark=id.9qk42ln7lu5q)

* [Glossary](#bookmark=id.r89w4yn7b46f)

* [References](#bookmark=id.93ejip34sp07)

---

## **Section 0 — System Model**

### **0.1 Node Taxonomy and Trust Levels**

The TL architecture defines three primary node classes, each with distinct trust assumptions, operational permissions, and adversarial exposure profiles.

**Validators** constitute the trust-anchored core of the TL system. Validators possess full write access to the append-only event log, participate in Merkle tree construction, and hold signing keys for root aggregation and anchoring operations. The validator set implements Byzantine-fault tolerance (BFT), requiring a minimum of 3f+1 nodes to tolerate f malicious participants. Validators are trusted to: correctly compute hash commitments, enforce causal ordering constraints, execute the anchoring protocol without unauthorized delay, and maintain key material according to specified rotation schedules. Validator trust assumes that fewer than one-third of the validator set acts maliciously simultaneously and that hardware security modules (HSMs) protect signing keys from exfiltration.

**Auditors** operate in a read-only trust posture. Auditors maintain full or partial replica of the event log and Merkle tree structure, enabling independent verification of inclusion proofs, root continuity, and causal ordering. Auditors cannot modify the log or influence consensus. The auditor role is designed for: regulatory bodies requiring forensic reconstruction capability, independent third parties performing compliance verification, and internal security teams conducting anomaly detection. Auditors are untrusted for write operations but trusted to correctly report verification results (byzantine behavior by auditors does not compromise system integrity, as their outputs are non-binding).

**Light Clients** represent the minimal verification endpoint. Light clients operate in SPV (Simplified Payment Verification) mode, maintaining only the current master root, block anchors, and a small verification cache. Light clients can verify individual event inclusions against anchored roots without downloading the full dataset. The light client trust model assumes: the anchoring chain remains consistent, the hash algorithm remains unbroken, and the initial root bootstrap was performed correctly. Light clients are untrusted for any write or consensus operations.

### **0.2 Network Model**

TL operates under a **partially synchronous communication model** as defined by Dwork, Lynch, and Stockmeyer (1988). This model assumes that the network may experience periods of asynchronous operation (where message delivery is unbounded), but eventually delivers all messages within some unknown but finite time bound Delta. This choice is deliberate: TL requires BFT consensus properties but cannot assume synchronous communication in wide-area deployments spanning geographically distributed infrastructure.

The system tolerates message delays up to 500 milliseconds for anchoring operations and up to 2 milliseconds for transaction execution within the hot path. If the network exceeds these bounds, the deferred anchoring mechanism activates (see Section 5), maintaining cryptographic continuity through cascade micro-roots while preventing execution liveness degradation.

### **0.3 Trust Boundary Definitions**

**Trusted Components:**

* Cryptographic primitives (hash functions, digital signatures, MACs) — trusted to satisfy standard security definitions

* Hardware Security Modules (HSMs) at validator nodes — trusted to protect key material

* Timestamp attestation services (when used) — trusted to provide accurate time within documented drift bounds

* Schema registry signing keys — trusted to correctly authenticate schema version increments

**Untrusted Components:**

* Individual validator execution (byzantine tolerance applies)

* Network paths between nodes (subject to interception, delay, injection)

* Storage providers (assumed potentially malicious or compromised)

* Light client implementations (assumed potentially incorrect but non-byzantine)

* External data oracle outputs (subject to Verification Hold constraints, see Section 7\)

### **0.4 Failure Model**

TL implements **Byzantine-Fault Tolerance (BFT)** for validator operations, specifically a BFT consensus protocol based on a variant of PBFT (Practical Byzantine Fault Tolerance) adapted for high-frequency event processing. The BFT assumption is essential because:

1. Validators possess write access to the append-only log, making byzantine behavior potentially catastrophic

2. The system operates in adversarial environments where infrastructure operators may be compromised

3. Regulatory and legal accountability requires that the system function correctly even when some participants behave maliciously

The minimum validator configuration tolerating f byzantine nodes requires 3f+1 total validators. For high-value deployments, a configuration of f=1 (4 validators minimum) is recommended; for critical infrastructure, f=2 (7 validators) provides enhanced protection.

Crash-fault tolerance (CFT) applies to: auditor node replication, light client verification caching, and storage provider availability attestation. CFT assumptions acknowledge that crash failures are more common than byzantine failures and that different operational responses (restart, failover) apply.

### **0.5 External Dependency Trust**

**Timestamping Authorities:** When external timestamp attestation is employed, TL assumes the authority operates within a documented time-drift bound (typically ±1 second per RFC 3161). Timestamp assertions are combined with internal validator timestamps to establish root timestamp binding. Trust in the timestamp authority is bounded: a compromised authority cannot forge inclusion proofs but can provide inaccurate time metadata.

**Anchoring Chains:** TL supports multi-chain anchoring to Bitcoin, Ethereum, or purpose-built anchoring networks. Anchoring chain trust assumptions: the anchoring chain’s consensus mechanism remains secure, the anchoring transaction achieves sufficient confirmations, and the anchoring network’s hash continuity is maintained. A compromised anchoring chain cannot retroactively modify TL’s historical commitments but can delay new anchor publications.

**Storage Providers:** Storage providers are explicitly untrusted for data integrity. All stored data includes cryptographic integrity checks (Merkle proofs, checksums) verifiable independently of the storage provider. Storage providers may experience availability failures; the architecture implements redundant, geographically distributed storage to maintain accessibility.

---

## **Threat Model**

The following adversarial conditions guide all architectural decisions in this report.

**T1: Malicious Insider with Log Write Access.** An authorized validator or operator attempts to insert, modify, or delete log entries. Countermeasure: append-only enforcement, dual-control requirements, Merkle hash chaining, and independent auditor replication.

**T2: Insider with Partial Encryption Key Access.** An actor possesses decryption keys for a subset of event data but lacks complete key material. Countermeasure: multi-party key derivation, crypto-shredding with preserved hash continuity, and separation between encryption (confidentiality) and hashing (integrity).

**T3: Developer Attempting Silent Schema Modification.** A developer modifies the event schema without proper versioning or authorization. Countermeasure: schema hash commitment in every leaf, signed schema registry, dual-control schema updates, and independent schema anchoring.

**T4: Infrastructure Operator Delaying Anchoring.** An operator with infrastructure access intentionally delays anchoring operations to create temporal ambiguity. Countermeasure: maximum anchoring delay bounds (500ms), automatic anchor triggering, monotonic root indexing, and anomaly logging on delay detection.

**T5: External Attacker with Storage Compromise.** An attacker gains access to storage infrastructure and attempts to modify or delete historical events. Countermeasure: geographic distribution, append-only enforcement, periodic integrity checks, and availability attestations.

**T6: Network-Level Interception Attacker.** An attacker intercepts, modifies, or delays network communications between nodes. Countermeasure: authenticated encryption, Merkle proof verification, and anchoring-based settlement.

**T7: Regulator Requesting Forensic Reconstruction.** A legitimate regulator requires access to historical events for audit purposes. Countermeasure: SPV proof generation, auditor node access, privacy-preserving pseudonymization, and redaction workflows.

**T8: Attempted Replay, Truncation, or Retroactive Reinterpretation.** An actor attempts to re-submit old events, truncate the log, or reinterpret past decisions under modified rule sets. Countermeasure: Event ID uniqueness, monotonic sequence validation, Active Axiom Set Hash binding, and forward integrity hash chaining.

**T9: Data Loss Event or Storage Failure.** Catastrophic storage failure results in loss of event data. Countermeasure: redundant replication, geographic distribution, disaster recovery protocols, and explicit data availability requirements (no root without retrievable data).

**T10: Long-Term Cryptographic Degradation.** Advances in cryptography (quantum computing, cryptanalytic breakthroughs) weaken hash function security over time. Countermeasure: hash versioning in leaf schema, explicit migration paths, and post-quantum algorithm preparation.

---

## **Section 1 — Merkle as a Core Structural Component of TL**

### **1.1 Architectural Necessity**

The Merkle tree is not an optional add-on to Ternary Logic but rather its **constitutive structural substrate**. Removal of the Merkle component collapses the following TL properties:

**Tamper-Evidence Collapse:** Without Merkle hash chaining, there exists no cryptographic evidence of log modification. An attacker who gains write access can alter historical events without detection. The append-only property of the Merkle structure ensures that any mutation invalidates all subsequent hash chains.

**Causal Ordering Collapse:** Without the prev\_event\_hash field anchored in Merkle commitments, events can be reordered after the fact without detection. The causal ordering guarantee — that event B referencing event A’s hash implies B occurred after A — depends entirely on the Merkle structure’s hash chaining.

**Contextual Integrity Collapse:** Without the Active Axiom Set Hash embedded in each leaf, rule changes could be retroactively applied to past events. The TL governance guarantee that decisions were made under the rule set active at decision time requires that each leaf bind to the exact axiom set in effect.

**Provable Commit Ordering Collapse:** Invariant III — the Execution Legitimacy Constraint — requires that transaction commits reference committed log hashes. Without Merkle proofs, there exists no mechanism to demonstrate that a commit reference corresponds to an actual committed event.

**Governance Auditability Collapse:** Without hierarchical Merkle subtrees aligned with decision domains (Economic Systems, Financial Infrastructure, Cyber-Physical Systems), auditors cannot selectively verify subsets of the decision space without downloading and verifying the entire log.

### **1.2 Epistemic Hold (0) Immutability via Merkle**

When TL reaches an Epistemic Hold (0) outcome — a decision to pause and await additional information or consensus — the Merkle structure freezes this outcome as immutable decision state. The Epistemic Hold event is committed to the Merkle tree with a triadic outcome field set to 0, binding the hold decision to a specific leaf in the hash chain. Once anchored, the Epistemic Hold cannot be retroactively changed to Act (+1) or Refuse (−1) without invalidating the entire subsequent hash chain. This provides cryptographic immutability for hold decisions, preventing ex-post rationalization or pressure-based reinterpretation of governance pauses.

The binding mechanism operates as follows: the Epistemic Hold leaf includes the complete decision context (trigger source, pillar reference, risk classification, active axiom set), and the leaf’s hash becomes an input to subsequent event hashes via the prev\_event\_hash chain. Any attempt to modify the hold outcome would require regenerating all subsequent hashes, which is computationally infeasible and cryptographically detectable.

### **1.3 Active Axiom Set Hash and Contextual Integrity**

The Active Axiom Set Hash enforces **contextual integrity** — the requirement that each decision be interpreted only under the rule set that was active when the decision was made. This hash is computed as:

AxiomSetHash \= H(rule\_set\_id || rule\_version || rule\_content\_hash)

Where H is the configured hash function, rule\_set\_id identifies the rule domain, rule\_version is the monotonically increasing version counter, and rule\_content\_hash is a Merkle root of the complete rule set content.

Each leaf contains the AxiomSetHash value active at event time. If governance rules change, a new AxiomSetHash is computed. Events committed after the change bind to the new hash; events committed before bind to the old hash. The system thus maintains a cryptographic record of which rule set governed each decision, making retroactive reinterpretation under altered rules cryptographically impossible without breaking hash continuity.

### **1.4 Hierarchical Subtrees and Decision Domains**

TL’s decision space is partitioned into three primary domains, each represented by a dedicated Merkle subtree:

**Economic Systems Subtree (ESS):** Contains events related to resource allocation, economic policy decisions, market mechanism governance, and allocation priority decisions. The ESS subtree root aggregates all economic decision events.

**Financial Infrastructure Subtree (FIS):** Contains events related to payment system integrity, settlement finality, counterparty risk management, and financial regulatory compliance. The FIS subtree root aggregates all financial infrastructure events.

**Cyber-Physical Systems Subtree (CPS):** Contains events related to operational technology, IoT governance, critical infrastructure control decisions, and physical-world actuation commands. The CPS subtree root aggregates all cyber-physical events.

The **Master Root** aggregates the three domain subtree roots:

MasterRoot \= H(ESS\_Root || FIS\_Root || CPS\_Root || metadata)

This hierarchy enables domain-selective auditing: a regulator concerned only with financial infrastructure can verify FIS subtree inclusion proofs without processing economic or cyber-physical events.

### **1.5 Proof Compression and Scalable Governance**

The Merkle structure enables scalable governance through proof compression. Rather than requiring verifiers to process the entire event history to validate a single decision, Merkle proofs provide logarithmic-size witnesses. For a tree with N events, a proof contains O(log N) hashes, enabling verification of any event’s inclusion and ordering in O(log N) time.

This compression is essential for regulatory compliance: a regulator can verify a specific transaction’s legitimacy by receiving only the event payload, its Merkle inclusion proof, and the anchored root reference — without downloading terabytes of historical data.

### **1.6 Crypto-Shredding and Hash Continuity**

When data must be erased for privacy compliance (crypto-shredding), the system destroys decryption keys while preserving hash commitments. The event leaf remains in the Merkle tree with all its hash chain bindings intact; only the plaintext payload becomes unrecoverable. Any verifier can still confirm that: (a) an event existed at a specific position in the sequence, (b) the event bound to a specific AxiomSetHash, (c) the event achieved a specific triadic outcome, and (d) the event was committed at a specific time. The loss of plaintext does not compromise the hash chain’s integrity or the decision’s provenance.

### **1.7 Retroactive Reinterpretation Prevention: Concrete Scenario**

Consider a TL system governing an automated trading venue with the following sequence:

**Event 1 (SeqID: 100):** A market participant submits a large sell order for asset X. The TL engine, evaluating risk classification and pillar compliance, reaches an **Epistemic Hold (0)** decision, pausing the order’s execution pending additional liquidity assessment. The event is committed to the Merkle tree with outcome=0, AxiomSetHash=ASH\_v2.1, and prev\_event\_hash referencing Event 99\.

**Event 2 (SeqID: 101):** Liquidity conditions improve. The TL engine evaluates the pending order under the same ASH\_v2.1 (no rule change has occurred) and reaches an **Act (+1)** decision, executing the order.

**An Attack Scenario:** A malicious insider attempts to retroactively reinterpret Event 1 as an **Act (+1)** decision, claiming the order was executed immediately without the Epistemic Hold pause.

**Merkle Protection:** The attacker would need to: (a) modify Event 1’s outcome field from 0 to \+1, (b) regenerate Event 1’s hash, (c) regenerate Event 2’s hash (since it references prev\_event\_hash=Event1\_hash), (d) regenerate all subsequent event hashes in the chain, (e) regenerate all subtree roots affected, (f) regenerate the Master Root, and (g) provide a valid anchoring proof for the modified chain on the anchoring chain. This is computationally infeasible and cryptographically detectable by any auditor with access to the original anchored root.

Furthermore, the AxiomSetHash binding ensures that even if the attacker controlled rule interpretation, they cannot claim Event 1 was evaluated under a different rule set than the one recorded.

---

## **Section 2 — Canonical Leaf Node Specification**

### **2.1 Mandatory Field Schema**

Every TL state transition event is encoded as a Merkle tree leaf with the following canonical schema:

TL\_Event\_Leaf {  
    event\_id:        UUIDv7        // Globally unique identifier  
    seq\_id:          uint64        // Monotonically increasing sequence number  
    prev\_event\_hash: HashDigest    // Hash of immediately preceding leaf  
    trusted\_ts:      uint64        // Unix timestamp in milliseconds  
    hold\_trigger:     utf8\_string  // Epistemic Hold trigger source identifier  
    pillar\_ref:      uint8         // Eight Pillars reference (0-7)  
    risk\_class:      uint8         // Risk classification level (0-255)  
    outcome:         int8          // Triadic outcome: \+1, 0, or \-1  
    integrity\_flags: uint16        // Bitfield for integrity extensions  
    schema\_ver:      uint32        // Schema version identifier  
    schema\_hash:     HashDigest    // Hash of schema definition  
    axiom\_hash:      HashDigest    // Active Axiom Set Hash at event time  
    hash\_algo\_ver:   uint16       // Hash algorithm version identifier  
    payload\_digest:  HashDigest    // Hash of encrypted event payload  
    extension:       bytes         // Optional extension data  
}

**Field Definitions:**

* **event\_id (UUIDv7):** A temporally ordered UUID providing global uniqueness without coordination. UUIDv7 encodes timestamp in the most significant 48 bits, ensuring sortability by event\_id as a secondary ordering guarantee.

* **seq\_id (uint64):** A monotonically increasing 64-bit integer assigned by the validator set consensus. Sequence IDs are gapless under correct operation; sequence gaps indicate potential tampering or failure.

* **prev\_event\_hash (HashDigest):** The hash of the immediately preceding leaf in the sequence, computed as H(prev\_leaf\_bytes). This field enforces linear ordering and prevents reordering attacks within a sequence. The hash includes the complete serialized preceding leaf, ensuring that any modification propagates forward.

* **trusted\_ts (uint64):** Unix timestamp in milliseconds from a trusted time source (validator-set consensus time or hardware RTC with attestation). Must be monotonically non-decreasing across the sequence.

* **hold\_trigger (utf8\_string):** Human-readable identifier of the trigger that caused an Epistemic Hold (0) outcome. Empty string if outcome is not 0\. Format: domain.trigger\_subtype.variant (e.g., economics.liquidity.insufficient).

* **pillar\_ref (uint8):** Numeric reference to the Eight Pillars framework element used for decision evaluation. Values 0-7 map to the eight defined pillars.

* **risk\_class (uint8):** Numeric risk classification level assigned during decision evaluation. Higher values indicate higher risk classification.

* **outcome (int8):** The triadic decision outcome. Permitted values: \+1 (Act), 0 (Epistemic Hold), \-1 (Refuse). No other values permitted.

* **integrity\_flags (uint16):** Bitfield for future integrity extension flags. Currently defined bits: bit 0 \= payload contains extensions, bit 1 \= event is part of deferred sequence, bit 2 \= event awaits oracle resolution.

* **schema\_ver (uint32):** The schema version identifier used to serialize this leaf. Enables schema evolution while maintaining backward compatibility for verification.

* **schema\_hash (HashDigest):** Hash of the complete schema definition document used to serialize this leaf. Changing the schema produces a new schema\_hash, enabling detection of schema version mismatches.

* **axiom\_hash (HashDigest):** The Active Axiom Set Hash — hash of the exact TL rule-set active at event time. This is the contextual integrity binding that prevents retroactive reinterpretation.

* **hash\_algo\_ver (uint16):** Identifier of the hash algorithm used for this leaf. Enables algorithm migration without breaking continuity. Currently assigned: 1 \= SHA-256, 2 \= SHA-384, 3 \= SHA-512, 4 \= BLAKE3, 5 \= SHA3-256.

* **payload\_digest (HashDigest):** Hash of the encrypted event payload (containing event-specific data beyond the commitment fields). The payload is encrypted separately; this digest enables integrity verification of the encrypted payload without decryption.

* **extension (bytes):** Optional DER-encoded ASN.1 structure for future extensions. Must be ignored by implementations that do not understand the extension’s OID.

### **2.2 Active Axiom Set Hash Specification**

The Active Axiom Set Hash binds each event to the governance rules active at its decision time. The hash is computed as:

AxiomSetHash \= HashFn(  
    "TL\_AXIOM\_SET\_V1" ||  
    rule\_set\_id ||  
    rule\_version ||  
    MerkleRoot(rule\_content)  
)

Where:

* HashFn is the configured hash function for this leaf

* "TL\_AXIOM\_SET\_V1" is a domain separation constant

* rule\_set\_id is a 256-bit identifier of the rule set

* rule\_version is a monotonically increasing version counter

* MerkleRoot(rule\_content) is a Merkle root of the complete rule set document

Rule changes require: (a) incrementing rule\_version, (b) updating the rule content, (c) recomputing the Merkle root, and (d) publishing the new AxiomSetHash. Events committed after the change automatically bind to the new hash. Events committed before retain the old hash. The two rule sets coexist as distinct hash values, enabling unambiguous historical interpretation.

### **2.3 Determinism Requirements**

Canonical serialization enforces deterministic encoding to prevent ambiguous representations:

**Canonical Serialization Format:** All leaves are serialized using a single, specified encoding standard (CBOR with deterministic tag mapping, RFC 8949). No field may be serialized in multiple ways.

**Strict Field Ordering:** Fields are serialized in ascending numeric tag order. No exceptions. Field ordering is part of the schema contract.

**Rejection of Non-Deterministic Values:** Floating-point values must not appear in commitment fields. Timestamps must use UTC. Locale-dependent string comparisons must not affect serialization.

**Locale Independence:** All string comparisons use Unicode NFC normalization. Timestamp formatting uses ISO 8601 / RFC 3339\.

**Explicit Encoding Standard:** CBOR with the following constraints: no indefinite-length arrays or maps, no tags beyond the defined set, no packed CBOR representations.

### **2.4 Privacy Requirements**

**Redaction Before Hashing:** Sensitive fields (personal identifiers, proprietary business data) are redacted before leaf construction. The redaction process produces a sanitized payload whose hash is recorded in payload\_digest; the original payload is encrypted and stored separately.

**Irreversible Pseudonymization:** Where personal data must be preserved, irreversible pseudonyms (HMAC-based one-way mapping) are used. The pseudonym cannot be reversed without the pseudonymization key, which is stored separately and destroyed on crypto-shredding.

**Raw Personal Data Prohibition:** Explicit encoding: personal data fields are never hashed directly. The system rejects leaves that contain obvious personal identifiers (names, ID numbers) in commitment fields.

**Audit Trail of Redaction:** Every redaction operation records: (a) the redaction rule applied, (b) the operator or system component that performed redaction, (c) the timestamp, and (d) the hash of the pre-redaction payload. This audit trail is itself committed to the append-only log.

### **2.5 Immutability Enforcement**

The schema hash field provides immutability enforcement: every leaf contains a hash of the schema definition used to serialize it. When the schema changes, a new schema\_hash is computed and distributed. Implementations must:

1. Reject leaves whose schema\_hash does not match a known schema version

2. Maintain a signed registry of schema versions with their corresponding hashes

3. Ensure that schema changes require dual-control authorization (two independent operators)

4. Anchor schema hashes independently on the anchoring chain to prevent retroactive schema replacement

---

## **Section 3 — Merkle Tree Construction Model**

### **3.1 Hash Algorithm Selection**

The primary hash algorithm is **SHA-256** for the initial deployment, providing 128-bit collision resistance (equivalent to 256-bit output). The choice is based on:

* **Widespread Cryptographic Scrutiny:** SHA-256 has undergone extensive public analysis since its specification in 2001\.

* **Hardware Acceleration:** SHA-256 is supported by hardware instructions (Intel SHA Extensions, ARM SHA instructions) enabling high-throughput computation.

* **Conservative Security Parameters:** 128-bit collision resistance exceeds the typically quoted 112-bit security threshold for government applications.

**Hash Versioning:** Each leaf embeds a hash\_algo\_ver field enabling algorithm migration. The migration path is: 1\. Add new hash algorithm identifier to the hash\_algo\_ver registry 2\. Run new algorithm in parallel with existing algorithm during transition 3\. After transition period, deprecate old algorithm 4\. Maintain backward compatibility for proof verification

**Post-Quantum Survivability:** SHA-256 provides approximately 128-bit classical collision resistance but only 64-bit quantum collision resistance (Grover’s algorithm reduces effective security by half). For post-quantum resilience, the architecture supports hash algorithm migration to SHA-384, SHA-512, or the BLAKE3 family. A hybrid mode during transition computes both classical and quantum-resistant hashes, embedding both in leaf metadata.

### **3.2 Binary vs. Ternary Branching Analysis**

**Binary Merkle Tree (Conventional):**

Depth calculation: D \= ceil(log\_2(N))  
Proof size: D hashes (each hash is 32 bytes for SHA-256)

**Ternary Merkle Tree (TL Architecture):**

Depth calculation: D \= ceil(log\_3(N))  
Proof size: D \* 2 hashes (two sibling hashes per level, 64 bytes total)

**Comparative Analysis Table:**

| Parameter | Binary Tree | Ternary Tree | Advantage |
| :---- | :---- | :---- | :---- |
| Depth for N=1M events | 20 | 13 | Ternary: 35% shallower |
| Proof size (32-byte hashes) | 640 bytes (20 hashes) | 832 bytes (13 levels × 2 × 32\) | Binary: 23% smaller |
| Hashes per node | 2 | 3 | Binary: simpler |
| Native TL outcome encoding | No | Yes (+1, 0, \-1 map to 3 children) | Ternary |
| CPU per proof verification | Lower | Higher | Binary |
| Memory for tree structure | Higher | Lower | Ternary |

**Ternary Topology Justification:** The ternary branching structure natively encodes TL’s triadic logic. Each internal node conceptually represents a decision point with three possible outcomes (Act, Hold, Refuse), creating a direct topological mapping between tree geometry and decision semantics. While this mapping is conceptual rather than enforced, it provides structural alignment between the Merkle architecture and the governance logic it secures.

Mathematically, ternary trees achieve O(log\_3 N) depth versus binary tree O(log\_2 N), reducing the number of hash computations required for proof generation at the cost of larger per-level proofs (two sibling hashes rather than one).

### **3.3 Ternary Geometry Visualization**

**Binary Merkle Tree (4 leaves):**

                    \[Root\]  
                   /      \\  
            \[NodeAB\]      \[NodeCD\]  
            /    \\        /    \\  
         \[A\]    \[B\]    \[C\]    \[D\]

Depth: 2 (for 4 leaves) Proof for leaf A: \[B, NodeCD, Root\] \= 3 hashes

**Ternary Merkle Tree (4 leaves, one padding):**

                 \[Root\]  
              /    |    \\  
       \[NodeABC\] \[NodeD\]  \[Padding\]  
       /    \\    \\  
    \[A\]    \[B\]  \[C\]

Depth: 2 (for 4 leaves, base-3 logarithm) Proof for leaf A: \[B, C, NodeD, Root\] \= 4 hashes (but 2 levels vs. 3)

**Semantic Encoding:**

The ternary node’s three children can be semantically mapped to TL outcomes:

        \[Node\]  
       /  |  \\  
    \[Act\] \[Hold\] \[Refuse\]  
     \+1     0      \-1

This mapping is conceptual: the hash computation does not depend on outcome values; the geometry simply provides a structurally aligned topology.

### **3.4 Construction Requirements**

**Asynchronous Tree Building:** Tree construction operates asynchronously to prevent blocking the transaction hot path. Events are accumulated in a rolling buffer; tree updates occur in background threads. The buffer implements a lock-free ring structure with per-slot checksums enabling crash detection.

**Rolling Buffer with Integrity Checksum:** The rolling buffer maintains the most recent B leaves in a pre-commitment state. Each buffer slot contains the serialized leaf and a 32-bit CRC checksum for corruption detection. On buffer overflow, the oldest slot is committed to the tree structure.

**Deterministic Leaf Placement:** Leaf position in the tree is determined solely by seq\_id modulo the tree size, ensuring that any validator or auditor can independently compute leaf positions and verify tree structure.

**Odd-Leaf Handling:** When the number of leaves is not a power of 3, the final incomplete node is padded with a deterministic padding leaf (hash \= SHA-256(“TL\_PADDING\_LEAF\_v1” || position)). The padding leaf is defined by the protocol and produces a fixed hash, ensuring reproducibility across implementations.

**Balanced Tree Enforcement:** Tree rebalancing occurs when the depth would increase (at 3^k leaves for integer k). Rebalancing reconstructs the tree at the new depth; no structural invariants are violated.

### **3.5 Replay Protection**

**Event ID Uniqueness:** The event\_id field uses UUIDv7, which encodes timestamp and randomness. Duplicate event\_id generation is prevented by consensus-level uniqueness checking before commitment.

**Monotonic Sequence Validation:** The seq\_id field must be strictly increasing. Validators reject events with seq\_id less than or equal to the last committed seq\_id.

**Replay Detection Logic:** Upon receiving an event with seq\_id equal to a previously committed seq\_id, validators compare event\_id. If event\_id differs, this indicates a potential fork attempt or duplicate submission attack; the event is rejected and an anomaly alert is logged. If event\_id matches, the event is recognized as a duplicate and rejected without penalty.

---

## **Section 4 — Hierarchical Integrity Model**

### **4.1 Domain Subtree Architecture**

The TL hierarchy implements four levels of Merkle aggregation:

**Level 0 — Individual Event Leaves:** Each event is serialized and hashed according to the canonical leaf schema (Section 2).

**Level 1 — Domain Subtree Roots:** Events are partitioned into three domain subtrees:

ESS\_Node\_h \= H(leaf\_h1 || leaf\_h2 || ... || leaf\_hk)  
FIS\_Node\_h \= H(leaf\_i1 || leaf\_i2 || ... || leaf\_ik)  
CPS\_Node\_h \= H(leaf\_j1 || leaf\_j2 || ... || leaf\_jk)

**Level 2 — Master Root:** The Master Root aggregates the three domain subtree roots:

MasterRoot\_h \= H(ESS\_Node\_h || FIS\_Node\_h || CPS\_Node\_h || metadata\_h)

**Level 3 — Root-of-Roots:** Periodic Master Roots are aggregated into a root-of-roots structure, providing long-term historical anchoring:

RootOfRoots\_h \= H(RootOfRoots\_{h-1} || MasterRoot\_h || timestamp\_h)

### **4.2 Subtree Continuity Guarantees**

Each subtree maintains independent continuity:

* Domain subtrees append events independently; cross-domain ordering is established at Master Root aggregation

* Subtree roots are immutable once included in a Master Root

* A Master Root cannot be modified without recomputing the RootOfRoots

### **4.3 Forward Integrity Safeguards**

**Strictly Increasing Root Index:** Every root in the chain (Master Root and Root-of-Roots) carries a monotonically increasing index counter. No root may be inserted retroactively between existing roots.

**Prior Root Hash Inclusion:** Each root contains the hash of its predecessor:

MasterRoot\_h \= H(ESS\_Node\_h || FIS\_Node\_h || CPS\_Node\_h || metadata\_h || MasterRoot\_{h-1})  
RootOfRoots\_h \= H(RootOfRoots\_{h-1} || MasterRoot\_h || timestamp\_h)

This creates an unbroken hash chain from any current root back to the genesis root, preventing insertion of fake historical roots.

---

## **Section 5 — Anchoring Strategy (Time-Bound Enforcement)**

### **5.1 Maximum Anchoring Delay**

The maximum anchoring delay is **500 milliseconds** from event commitment. This bound is architecturally enforced: if a root is not anchored within 500ms of its first event commitment, the system enters deferred anchoring mode with enhanced logging and reduced transaction throughput.

### **5.2 Automatic Anchoring Trigger**

Anchoring triggers automatically when any of the following conditions is met:

1. **Time-based:** 500ms has elapsed since the last anchor (maximum delay bound)

2. **Count-based:** 1,000 events have accumulated since the last anchor

3. **Size-based:** The unanchored event payload size exceeds 10 MB

4. **Manual:** An administrator explicitly triggers anchoring (used for disaster recovery)

### **5.3 Monotonic Root Indexing**

Every anchored root carries a globally unique, monotonically increasing anchor index. The anchor index is recorded in the anchoring transaction metadata, enabling ordering of anchors on the anchoring chain.

### **5.4 Multi-Chain Anchoring Strategy**

TL supports simultaneous anchoring to multiple chains to prevent single-chain dependency risk:

**Primary Anchor:** Bitcoin mainnet (highest security, highest cost) **Secondary Anchor:** Ethereum (good security, moderate cost) **Tertiary Anchor:** Purpose-built anchoring chain or公证链 (high availability, low cost)

Each anchor provides independent confirmation of the anchored root’s existence at a specific timestamp. Multi-chain anchoring prevents an attacker from reorganizing a single anchoring chain to alter history.

### **5.5 Public Verification Endpoint**

Anchored roots are published to a public verification endpoint (HTTPS API) enabling third-party verification of anchor existence and consistency. The endpoint provides:

* Latest anchored root and its anchoring transaction references

* Merkle proof of any specific event against the latest anchored root

* Historical anchor audit trail

* Anchor consistency verification (proving no anchor was removed or reordered)

### **5.6 Time Integrity Requirements**

**Trusted Timestamp Integration:** Anchors include timestamps from two sources: the validator-set consensus timestamp (internal) and the anchoring chain block timestamp (external). Discrepancies exceeding 60 seconds trigger an anomaly alert.

**Root Timestamp Binding:** The anchored root includes a timestamp field frozen at anchor time. This timestamp cannot be modified after anchoring.

**Anti-Backdating Enforcement:** Anchoring nodes reject anchor attempts whose timestamp is earlier than the last anchored timestamp. Backdating is cryptographically prevented by the anchoring chain’s timestamp enforcement.

### **5.7 Deferred Anchoring Mode**

During high-frequency execution windows, TL may defer full anchoring while maintaining cryptographic commitments through **cascade micro-roots**.

**Cascade Micro-Root Mechanism:**

MicroRoot\_t \= H(MicroRoot\_{t-1} || Event\_{t} || buffer\_checksum)

Every micro-root binds to the previous micro-root, creating an unbroken chain. The micro-root chain is committed to the rolling buffer and included in the next full anchor.

**Maximum Deferral Window:** 500 milliseconds. No event may remain unanchored beyond this bound under normal operation.

**Crash Failure Protection:**

* Rolling buffer is persisted to write-ahead log (WAL) before micro-root update

* On restart, the system reads WAL to recover the last consistent micro-root state

* Events in volatile buffer at crash time are recovered from WAL and reprocessed

* If WAL recovery reveals missing events, the system enters recovery mode and requests事件 from auditors

**Reconciliation Protocol:**

1. After restart, the system compares its recovered micro-root chain against auditor copies

2. Any discrepancy triggers anomaly logging and halts new event processing

3. Discrepancies are resolved by majority vote among validator set

4. A missed anchor interval triggers an automatic audit request to all auditor nodes

---

## **Section 6 — Causal Integrity Enforcement (Epistemic Hold Protection)**

### **6.1 Causal Ordering Proof Requirement**

The Epistemic Hold (0) outcome requires cryptographic enforcement of causal ordering. The system guarantees:

**Commitment Ordering:** For any event E with outcome=0 (Epistemic Hold), the event’s Merkle commitment must be established before or atomically with any subsequent event that depends on E’s hold state.

**Atomic Snapshot Boundary:** The atomic snapshot encompasses the Epistemic Hold event and all events committed in the same Merkle batch. The batch’s root hash atomically commits all included events.

**Formal Ordering Guarantee:**

∀ event B with seq\_id \> event A seq\_id:  
    H(A) is included in B's prev\_event\_hash chain  
    ∴ timestamp(B) ≥ timestamp(A)  
    ∴ causal\_order(B) \> causal\_order(A)

### **6.2 Execution Interlock**

Invariant III — the Execution Legitimacy Constraint — enforces a strict execution interlock:

**Precondition for Transaction Commit:** A transaction commit request must include a Merkle proof demonstrating that the corresponding event has been committed to the log and the commit references the committed log hash.

**Precondition for Actuation Command:** An actuation command (to external systems) is valid only if it references a committed log hash corresponding to an event with outcome=+1 (Act). Any actuation without a corresponding committed log hash is structurally invalid and must be rejected by the actuator.

**Epistemic Hold Bypass Prevention:** Events with outcome=0 (Epistemic Hold) must not produce actuation commands. This is enforced by the validator set consensus: the commit protocol rejects any attempt to commit an Act outcome for an event that was previously placed in Epistemic Hold without subsequent resolution.

**Silent Bypass Prevention:** The system monitors for any actuation command that does not have a corresponding committed log hash. Detected bypass attempts trigger immediate suspension of the offending validator and an anomaly alert.

---

## **Section 7 — Proof Generation and Verification**

### **7.1 Standardized Merkle Inclusion Proof**

A Merkle inclusion proof demonstrates that a specific leaf is contained in a Merkle tree with a given root. The proof consists of:

MerkleProof {  
    leaf:          bytes      // Serialized leaf data  
    leaf\_hash:    HashDigest // Hash of the leaf  
    proof\_hashes: \[\]HashDigest // Sibling hashes at each level  
    root\_hash:    HashDigest // The claimed root  
    tree\_config:  TreeConfig // Tree parameters (branching factor, hash algo)  
}

**Proof Generation Algorithm:**

function generate\_proof(leaf, seq\_id, tree):  
    position \= compute\_position(seq\_id, tree.size)  
    proof \= \[\]  
    current\_hash \= leaf.hash  
    for level in 0..tree.depth:  
        sibling\_position \= position ^ 1  // sibling index  
        sibling\_hash \= tree.get\_node(level, sibling\_position)  
        proof.append(sibling\_hash)  
        current\_hash \= hash(current\_hash, sibling\_hash)  // parent  
        position \= position // branching\_factor  
    return MerkleProof(leaf, proof, tree.root)

**Proof Size:** For a ternary tree with N leaves, proof size is O(log\_3 N) × (branching\_factor \- 1\) hashes. With 32-byte hashes and ternary branching, a tree with 1 million leaves requires proofs of approximately 832 bytes (13 levels × 2 siblings × 32 bytes).

### **7.2 Non-Inclusion Proof (Sparse Merkle Evaluation)**

For proving that an event does NOT exist in a tree, the system employs a Sparse Merkle Tree (SMT) structure for the lookup index. An SMT maps seq\_ids to event hashes; empty positions are assigned a predetermined null hash.

**Non-Inclusion Proof:** To prove seq\_id X does not exist, the verifier demonstrates: (a) the leaf at position X has the null hash, and (b) all ancestor nodes on the path from position X to the root have exactly one non-null child (the null branch) and one or two null branches. This proves that no non-null leaf exists at position X.

**Sparse Merkle Evaluation:** The SMT lookup index is maintained separately from the main event tree. The SMT root is included in each Master Root, binding the lookup index to the main tree.

### **7.3 Proof Serialization Format**

Proofs are serialized using CBOR (RFC 8949\) with the following schema:

MerkleProofSchema {  
    1: bytes,   // leaf\_bytes  
    2: bytes,   // leaf\_hash (32 bytes)  
    3: \[\]bytes, // proof\_hashes  
    4: bytes,   // root\_hash (32 bytes)  
    5: uint8,   // tree\_type (1=ternary\_event, 2=sparse\_lookup)  
    6: uint16,  // hash\_algo\_version  
}

### **7.4 Light Client / SPV Specification**

**Verification Protocol for a Single Event:**

1. **Input Received:** Event payload, Merkle inclusion proof, anchored root reference, anchor transaction ID on anchoring chain

2. **Anchor Verification:** Verify the anchor transaction exists and has sufficient confirmations on the anchoring chain

3. **Root Verification:** Verify the root matches the anchored root

4. **Proof Verification:** Compute hash(leaf) and iteratively combine with proof\_hashes to recompute root; verify computed root equals claimed root

5. **Output:** TRUE if all verifications succeed; FALSE otherwise

**Proof Size Guarantee:** For N=10^9 events, ternary tree depth is ceil(log\_3(10^9)) ≈ 19\. Proof size is 19 × 2 × 32 \= 1,216 bytes. This is logarithmically bounded and easily fits in a single network packet.

**Commodity Hardware Requirement:** SHA-256 computation of 1,216 bytes (38 hash invocations) completes in under 1 microsecond on modern commodity CPUs. The proof verification fits well within the ≤2ms latency budget.

**No Full Dataset Requirement:** The light client requires only: the anchored root, the proof for the requested event, and the anchor reference. Total data transfer is approximately 1.5 KB per verification.

**Verification Failure Handling:**

* **Network Failure:** Retry with exponential backoff; alert if failure persists

* **Invalid Proof:** Reject; log attempt; do not fall back to trusting the event

* **Anchor Not Found:** Query verification endpoint for current anchored root; do not trust unanchored claims

### **7.5 Oracle Integrity and Verification Hold**

**Verification Hold vs. Epistemic Hold (0):**

| Property | Verification Hold | Epistemic Hold (0) |
| :---- | :---- | :---- |
| Trigger | Unverifiable external input | TL governance decision |
| Outcome | Protective suspension | Governance pause |
| Resolution | Oracle data validation | Additional information or consensus |
| Duration | Until verification succeeds or timeout | Until governance conditions met |
| Event recorded in log? | Yes (with special flag) | Yes (outcome=0) |

**Boundary Definition:** Verification Hold applies exclusively to external data provenance (oracles, data feeds). Epistemic Hold applies to TL’s internal governance decision process. An event with outcome=0 may be in Verification Hold or Epistemic Hold depending on whether external data or internal deliberation triggered the hold.

**Resolution Pathway for Verification Hold:**

1. Oracle provides cryptographically signed data with proof of provenance

2. Validator set verifies signature and proof

3. If verification succeeds: event transitions to actionable state, original outcome is preserved

4. If verification fails after timeout (configurable, default 60 seconds): event transitions to Refuse (-1) by default; alternative resolution policies configurable

**Resolution Pathway for Epistemic Hold (0):**

1. Additional information becomes available or consensus is reached

2. Validator set re-evaluates the pending event

3. New outcome (+1 or \-1) is committed as a new event referencing the original hold event

4. Original hold event remains immutable in the log

### **7.6 Key Security**

**Ephemeral Encryption Keys:** Event payload encryption uses ephemeral keys generated per-event or per-batch. Ephemeral keys are encrypted with the validator set’s collective public key and stored with the encrypted payload. Key destruction (crypto-shredding) destroys only the ephemeral key, leaving the hash commitment intact.

**Hardware-Backed Storage:** Validator signing keys are stored in FIPS 140-2 Level 3 HSMs. Hardware recommendations: Cloud HSM (AWS CloudHSM, Azure Dedicated HSM) or dedicated HSM appliances (Thales Luna, Utvik).

**Key Rotation Schedule:**

* Signing keys: 90-day rotation

* Encryption keys: 30-day rotation

* Pseudonymization keys: Annual rotation (with crypto-shredding capability)

* Hash algorithm: Event-driven (when security parameters degrade)

**Compromise Detection Protocol:**

1. HSM logs all key usage with timestamps

2. Anomalous usage patterns (unusual hours, unusual operation types) trigger alerts

3. On suspected compromise: emergency key revocation, chain fork detection, audit of affected events

### **7.7 Crypto-Shredding**

**Destruction Process:**

1. Identify the pseudonymization or encryption key to destroy

2. Apply key destruction仪式 (cryptographic erasure, physical destruction)

3. Record destruction in the key destruction log (append-only, HSM-backed)

4. Publish key destruction attestation (optional, depending on policy)

**Hash Continuity Preservation:**

* The key destruction log is itself committed to the Merkle tree

* Event hashes remain verifiable; only the encrypted payload becomes unreadable

* Any verifier can confirm that a specific event existed and had a specific outcome without accessing the plaintext

**Continued Proof Validity:**

* Merkle proofs remain valid after crypto-shredding

* Proof verification does not require decryption

* The leaf\_hash and all chain hashes remain computationally indistinguishable from pre-shredding values

---

## **Section 8 — Data Availability (DA) Strategy**

### **8.1 Storage Architecture**

The encrypted pre-hash event data is stored in a **redundant, geographically distributed storage architecture** designed to maintain accessibility even under partial infrastructure failure.

**Storage Layers:**

1. **Validator Local Storage:** Each validator maintains a full replica of the encrypted event log on HSM-backed encrypted storage. Primary durability mechanism.

2. **Auditor Distributed Storage:** Auditor nodes maintain full replicas on geographically distributed storage clusters. Secondary durability mechanism.

3. **Archive Storage:** Long-term archive on geographically distributed cold storage (AWS S3 Glacier, Azure Archive Blob Storage). Tertiary durability for events older than 90 days.

### **8.2 Redundancy Model**

**Replication Factor:** 3 replicas for active storage (validator and auditor layers). 2 replicas for archive storage.

**Geographic Distribution:** Minimum 3 distinct geographic regions for active storage. Recommended: US-East, EU-West, AP-Southeast.

**Failure Tolerance:**

* 1 replica failure: Transparent operation continues

* 2 replica failure: Degraded operation (increased latency) continues

* 3 replica failure: System halts new event commitment until replica restoration

### **8.3 Retention Horizon**

* **Active Period (0-90 days):** All events stored in active storage with full redundancy

* **Archive Period (90 days \- indefinite):** Events migrated to cold storage with reduced redundancy; availability SLA reduced to best-effort with 99.9% annual availability target

### **8.4 Centralized vs. Decentralized Storage Comparison**

| Property | Centralized Storage | Decentralized Storage (TL Default) |
| :---- | :---- | :---- |
| Availability | Single-region, single-provider risk | Multi-region, multi-provider resilience |
| Latency | Lower (no consensus overhead) | Higher (geographic distribution adds latency) |
| Integrity | Provider-dependent | Cryptographically self-verifying |
| Cost | Lower for low volumes | Higher but predictable scaling |
| Censorship Resistance | Lower | Higher |
| Compliance | Easier to enforce | More complex |

TL defaults to a **hybrid model**: centralized storage clusters managed by validator set (centralized control, decentralized geographic distribution) with decentralized availability attestation for transparency.

### **8.5 Proof-of-Storage Mechanism**

Validator and auditor nodes periodically (every 1,000 events or 60 seconds, whichever is earlier) compute and sign an **availability attestation**:

AvailabilityAttestation {  
    node\_id: bytes,  
    root\_hash: HashDigest,  
    event\_range: (first\_seq\_id, last\_seq\_id),  
    timestamp: uint64,  
    signature: bytes  
}

Attestations are collected by the auditor set and aggregated into a **Storage Consensus Proof** demonstrating that a threshold of storage nodes have accessible data for a specific root.

### **8.6 Disaster Recovery Protocol**

**Scenario: Catastrophic Data Loss**

1. **Detection:** Storage monitoring detects unrecoverable replica loss

2. **Alert:** Immediate alert to all validators and auditors

3. **Recovery Initiation:** Validator set initiates recovery protocol

4. **Reconstruction:** Data reconstructed from remaining replicas (auditor nodes, archive storage)

5. **Integrity Verification:** Reconstructed data verified against Merkle roots

6. **Service Restoration:** Normal operation resumes when threshold replicas are restored

**Data Rehydration Workflow:** Cold-archived events are rehydrated to active storage on-demand when verification is required. Rehydration latency: approximately 4-12 hours for Glacier-class storage; approximately 1-5 minutes for archive blob storage.

### **8.7 Explicit Data Availability Requirement**

**Critical Invariant:** A Merkle root MUST NOT be considered committed if the corresponding event data is not retrievable. The anchoring protocol MUST verify data availability before anchor publication.

If a validator attempts to anchor a root for which it cannot provide data availability proof, the anchor is rejected by the validator set consensus. This prevents the dangerous state of a system that has committed to hashes without the ability to produce the underlying data.

---

## **Section 9 — Log Truncation and Tamper Resistance**

### **9.1 Append-Only Enforcement**

The Merkle tree structure inherently enforces append-only semantics at the integrity layer. Additional enforcement mechanisms:

**Storage-Level Enforcement:** Storage systems are configured in WORM (Write-Once, Read-Many) mode or equivalent append-only semantics. Operating system-level: filesystem mounted read-only after initial write; hardware-level: WORM-capable storage devices.

**Consensus-Level Enforcement:** Validator consensus explicitly rejects any attempt to modify or delete committed events. The consensus protocol only accepts new event commitments; modification and deletion are not valid consensus operations.

**Audit-Level Monitoring:** Auditor nodes continuously verify that the committed log matches the append-only expectation. Any detected truncation or modification triggers an immediate anomaly alert.

### **9.2 Periodic Integrity Checks**

The system performs continuous integrity verification:

* **Local Checksum Verification:** Every 10,000 events or 60 seconds, validators compute a rolling checksum of stored data and compare against the recorded checksum.

* **Cross-Node Consistency Check:** Every 100,000 events or 1 hour, validators exchange integrity digests and verify consistency. Divergence triggers anomaly alert.

* **Full Tree Rehash:** Weekly, validators recompute all leaf hashes and verify against stored roots. Any discrepancy indicates storage corruption or tampering.

### **9.3 Missing Sequence ID Detection**

The monotonically increasing seq\_id field enables gap detection. The integrity verification process:

1. Maintains the last verified seq\_id

2. On reading new events, verifies seq\_ids are contiguous

3. Reports missing seq\_ids as potential tampering or data loss

4. Triggers reconciliation protocol with auditor nodes

### **9.4 Automatic Anomaly Signaling**

Detected anomalies are logged to:

1. **Validator Local Alert System:** Immediate on-console alert

2. **Auditor Network Alert:** Anomaly propagated to all auditor nodes

3. **Independent Audit Trail:** Anomaly logged to separate, append-only audit system with independent storage

Anomaly categories:

* **SEVERITY 1 (Critical):** Missing seq\_ids, hash chain breaks, anchor delay exceeded — immediate halts of new event commitment pending resolution

* **SEVERITY 2 (High):** Cross-node consistency divergence, integrity checksum failures — degraded operation with enhanced monitoring

* **SEVERITY 3 (Medium):** Latency anomalies, storage availability degradation — operational monitoring and potential intervention

### **9.5 Schema Governance**

**Signed Schema Registry:** All authorized schema versions are recorded in a signed registry maintained by the validator set. The registry maps schema version ID to schema hash and includes a digital signature from the validator set.

**Dual Control for Schema Updates:** Schema modifications require: (a) proposed change submitted by developer, (b) independent review and approval by second developer, (c) validator set multi-signature authorization, (d) publication of new schema version with new schema\_hash.

**Independent Schema Anchoring:** Schema version changes are anchored independently on the anchoring chain, providing an immutable record of schema evolution separate from event data.

---

## **Section 10 — Latency and Throughput Modeling**

### **10.1 Latency Budget Allocation**

The total transaction execution latency budget is ≤2,000 microseconds (2 milliseconds). This budget is allocated as follows:

| Component | Latency Budget (μs) | Percentage |
| :---- | :---- | :---- |
| Event validation and preprocessing | 100 | 5.0% |
| Leaf serialization and hash computation | 150 | 7.5% |
| Rolling buffer write and checksum | 50 | 2.5% |
| Tree update (cascade hash computation) | 300 | 15.0% |
| Consensus round-trip (intra-datacenter) | 800 | 40.0% |
| Proof generation | 100 | 5.0% |
| Log commitment write | 200 | 10.0% |
| Response transmission | 100 | 5.0% |
| **Reserved contingency** | 200 | 10.0% |
| **Total** | **2,000** | **100%** |

**Notes:**

* Tree update computation assumes parallel hash computation across levels using SIMD instructions (AVX2/AVX-512)

* Consensus round-trip assumes intra-datacenter deployment (sub-millisecond RTT); wide-area deployments require geographic colocation of validators

* Reserved contingency enables handling of transient load spikes without exceeding the hard latency bound

### **10.2 Maximum Sustainable Event Rate**

**Single-Threaded Throughput (per validator core):**

* Leaf hash computation: \~500 ns per leaf (SHA-256 hardware)

* Tree level updates: \~100 ns per level per leaf

* For depth D=13 (ternary tree, 1M leaves): \~1.3 μs per leaf for tree update

* **Single-core sustainable rate: \~400,000 events/second**

**Parallel Construction Strategy:** Multi-core validators distribute leaf processing across cores. With C cores and perfect load balancing:

Maximum sustainable event rate \= 400,000 × C events/second

For an 8-core validator: \~3.2 million events/second sustained throughput.

**Bottleneck Analysis:** At high event rates, the bottleneck shifts from computation to consensus. PBFT consensus scales approximately linearly with validator set size up to 50 validators, providing throughput of 50,000-100,000 transactions/second per validator in the common case.

### **10.3 Worst-Case Load Model**

**Burst Load:** TL handles event bursts by:

1. Accepting events into the rolling buffer (up to 10,000 events capacity)

2. Processing buffer in parallel batches

3. Distributing tree updates across available cores

4. Deferring anchoring if buffer overflows

**Sustained Overload:** If event rate exceeds processing capacity:

1. System enters congestion mode: new event acceptance is rate-limited

2. Deferred anchoring mode activates (up to 500ms accumulation before forced anchor)

3. Backpressure signals sent to event sources

4. Recovery when rate falls below capacity

### **10.4 Numerical Scenario (≥10,000 events/sec)**

**Scenario:** A financial exchange using TL for trade decision governance processes 15,000 events per second during peak trading hours.

**Validator Configuration:** 4 validators, each with 8 cores, co-located in a single data center.

**Latency Analysis:**

* Per-event leaf processing: 200 μs (parallel batch processing)

* Tree update (13 levels): 300 μs (parallel across cores)

* Consensus (4 validators, single datacenter RTT \~0.5ms): 800 μs

* Total per-event latency: \~1,300 μs (well within 2ms budget)

**Throughput Verification:**

* Per-core throughput: 400,000 events/sec

* Per-validator throughput: 3,200,000 events/sec (8 cores)

* Validator set throughput: 12,800,000 events/sec (4 validators)

* **Sustained capacity: 15,000 events/sec \= 0.12% of capacity** ✓

**Headroom:** System can sustain 8.5x current load before approaching limits, providing substantial margin for growth and load spikes.

---

## **Section 11 — Formal Integrity Guarantees**

### **11.1 Collision Resistance**

**Definition:** A hash function H offers collision resistance if it is computationally infeasible to find two distinct inputs x and y such that H(x) \= H(y).

**TL Hash Function Assumptions:**

* SHA-256: Provides 128-bit collision resistance against classical adversaries (2^128 operations to find collision)

* Assessment: Adequate for TL’s integrity requirements through 2030; plan for SHA-384 migration thereafter

**Impact of Collision:** If a collision is found between two leaves with different outcomes, an attacker could potentially substitute one leaf for another while maintaining hash chain validity. The Active Axiom Set Hash and seq\_id uniqueness provide secondary protection; a collision would require finding a second-preimage attack rather than a mere collision.

### **11.2 Preimage and Second-Preimage Resistance**

**Preimage Resistance:** Given a hash output h, it is computationally infeasible to find any input x such that H(x) \= h. TL relies on preimage resistance to ensure that knowing a leaf hash does not enable recovery of the leaf content.

**Second-Preimage Resistance:** Given an input x, it is computationally infeasible to find a different input y such that H(x) \= H(y). TL relies on second-preimage resistance to ensure that an attacker cannot produce an alternative leaf that hashes to the same value as a legitimate leaf.

**Strengths:** SHA-256 provides 256-bit second-preimage resistance (equivalent to output size). This is considered computationally infeasible against any classical or near-term quantum adversary.

### **11.3 Forward Integrity Definition**

**Forward Integrity:** If an attacker compromises the system at time T, they cannot modify or forge events committed before time T. The hash chain structure ensures that pre-compromise events are frozen in the hash chain; compromising current keys does not provide the ability to regenerate historical hashes without detection.

**Formal Statement:** Let C be the set of events committed at time t \< T. For any event e ∈ C, the Merkle proof verifying e’s inclusion in MasterRoot\_t remains verifiable using only publicly available information (roots, proofs). Compromise of private keys at time T does not enable generation of valid proofs for modified versions of e.

### **11.4 Conditions Under Which Guarantees Degrade**

**Hash Algorithm Compromise:** If the hash function H is broken (collision found), collision resistance degrades to zero. Preimage and second-preimage resistance may remain partially intact depending on the nature of the break. Mitigation: hash algorithm migration protocol (Section 3.1).

**Consensus Failure:** If more than (n-1)/3 validators are byzantine, the consensus mechanism may accept invalid events. Forward integrity of previously committed events is preserved, but post-compromise events may be invalid. Mitigation: validator set monitoring, slashing conditions.

**Storage Failure:** If all replicas of event data are lost, the Merkle root remains committed but becomes unverifiable without data reconstruction. Data availability guarantees are lost. Mitigation: geographic distribution, redundancy, disaster recovery.

### **11.5 Long-Term Survivability Modeling**

**Cryptographic Aging Model:**

| Year | SHA-256 Classical Security | SHA-256 Quantum Security | Recommended Action |
| :---- | :---- | :---- | :---- |
| 2026 | 256 bits | 128 bits | Monitor quantum computing advances |
| 2030 | 256 bits | 128 bits | Begin SHA-384 migration planning |
| 2035 | 256 bits | 85 bits | SHA-384 deployment |
| 2040 | 256 bits | 64 bits | Evaluate post-quantum algorithms |

**Post-Quantum Migration Continuity:** The hash versioning mechanism (hash\_algo\_ver field) enables algorithm migration without breaking existing proofs or anchors. Migration procedure:

1. Introduce new hash algorithm identifier (e.g., SHA3-256 or BLAKE3)

2. Run hybrid mode: new events include both SHA-256 and new algorithm hashes

3. Validators and auditors update to support new algorithm

4. After transition period, deprecate SHA-256 for new events

5. Historical anchors remain verifiable under SHA-256

---

## **Section 12 — Comparative Analysis**

### **12.1 Bitcoin Transaction Merkle Trees**

**Architecture:** Binary Merkle tree aggregating transactions into a block header. The block header contains the Merkle root, which is committed to the Bitcoin blockchain via PoW.

**TL Comparison:**

| Property | Bitcoin | TL |
| :---- | :---- | :---- |
| Branching Factor | 2 (binary) | 3 (ternary) |
| Leaf Content | Transactions | State transition events |
| Ordering | Block-based, within-block order by miner | Sequenced by consensus, gapless |
| Context Binding | No context hash | Active Axiom Set Hash |
| Hierarchical Domains | No | Yes (ESS, FIS, CPS) |
| Deferred Commitment | No (immediate) | Yes (up to 500ms) |
| Light Client Verification | SPV (log size proofs) | SPV (log size proofs, smaller depth) |
| Privacy Model | Pseudonymous | Pseudonymous \+ crypto-shredding |

**Key Differences:** Bitcoin’s Merkle tree is optimized for transaction inclusion proofs; TL’s Merkle architecture is optimized for governance decision verification with contextual integrity, causal ordering, and domain isolation.

### **12.2 Ethereum State Trie**

**Architecture:** Modified Merkle Patricia Trie (MPT) for state, transactions, and receipts. Each block header contains three roots: state root, transactions root, receipts root. The state trie maps account addresses to account states.

**TL Comparison:**

| Property | Ethereum | TL |
| :---- | :---- | :---- |
| Tree Structure | Merkle Patricia Trie (prefix-based) | Ternary Merkle tree (sequence-based) |
| Update Model | Incremental state updates | Append-only event log |
| Ordering | Transaction order within block | Global sequence ID |
| Context Binding | No | Active Axiom Set Hash |
| Balancing | Self-balancing via Patricia structure | Rebalancing on depth threshold |
| Light Client | Eth2 light sync (Casper FFG) | Custom SPV with anchoring |

**Key Differences:** Ethereum’s trie is a key-value store optimized for state queries; TL’s Merkle structure is an append-only log optimized for audit and verification of governance decisions.

### **12.3 Certificate Transparency Logs**

**Architecture:** Append-only Merkle tree of certificate logs. Monotonically growing tree; logs are monitored by monitors and auditors. CT logs use a binary Merkle tree with SKT (Signed Tree Head) commitments.

**TL Comparison:**

| Property | Certificate Transparency | TL |
| :---- | :---- | :---- |
| Purpose | Certificate issuance audit | Governance decision audit |
| Branching Factor | 2 (binary) | 3 (ternary) |
| Ordering | By log server receipt time | By consensus sequence ID |
| Domain Partitioning | No | Yes (ESS, FIS, CPS) |
| Latency | Minutes to hours | ≤2ms execution |
| Consistency Model | eventual | Strong (BFT consensus) |
| Public Verification | Yes (via audit proofs) | Yes (via SPV proofs) |

**Key Differences:** CT logs prioritize broad distribution and eventual consistency over low latency; TL prioritizes real-time execution with ≤2ms latency while maintaining strong consistency.

### **12.4 Sparse Merkle Trees (SMT)**

**Architecture:** A Merkle tree where the key space is much larger than the number of stored leaves. Unused positions are assigned a predefined null hash. SMTs support efficient non-membership proofs.

**TL Comparison:**

| Property | Sparse Merkle Tree | TL Merkle Tree |
| :---- | :---- | :---- |
| Key Space | 2^256 (or similar large space) | Sequence ID (up to 2^64) |
| Non-Inclusion Proof | Efficient (O(log keyspace)) | Requires SMT lookup index |
| Update Complexity | O(log keyspace) per update | O(log N) per update |
| Storage | Proportional to keyspace (with compression) | Proportional to leaf count |
| TL Use Case | Lookup index for seq\_id → event | Main event tree structure |

**Integration in TL:** TL uses an SMT for the seq\_id-to-event-hash lookup index, enabling efficient non-inclusion proofs when required.

### **12.5 Tradeoff Matrix**

| Property | Bitcoin | Ethereum | CT Logs | SMT | TL |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Scalability (N events) | O(N) storage, O(log N) proof | O(N) storage, O(log N) proof | O(N) storage, O(log N) proof | O(N) storage, O(log N) proof | O(N) storage, O(log N) proof |
| Audit Clarity | High | Medium | High | Medium | High (domain isolation) |
| Governance Robustness | N/A (no governance) | Low (no explicit governance) | N/A (no governance) | N/A (structure only) | High (explicit governance binding) |
| Low Latency (\<2ms) | No (10 min block) | Partial (PoW \~12s) | No (minutes) | Yes | Yes |
| Causal Ordering | Block-level | Block-level | Log-level | N/A | Strict (seq\_id \+ prev\_hash) |
| Contextual Integrity | No | No | No | No | Yes (Axiom Hash) |
| Domain Isolation | No | No | No | No | Yes (3 subtrees) |
| Crypto-Shredding | No | No | No | No | Yes |
| BFT Consensus | No (PoW) | Partial (PoS) | No | N/A | Yes (PBFT-derived) |

---

## **Section 13 — Failure Mode Disclosure**

### **13.1 Residual Risk Statement**

Despite the comprehensive hardening described in this architecture, TL’s Merkle-based integrity guarantees represent risk reduction, not absolute elimination. Residual risks remain in the following categories:

**Cryptographic Risk:** All integrity guarantees depend on the security of the underlying hash function. If SHA-256 is significantly weakened (by cryptanalytic breakthrough or quantum computing), the collision resistance and preimage resistance guarantees degrade. Migration to stronger algorithms mitigates but does not eliminate this risk.

**Consensus Risk:** The BFT consensus protocol assumes fewer than one-third of validators are byzantine. If this assumption is violated, the system may accept invalid events or suffer fork conditions. Validator set diversity and slashing conditions mitigate but do not eliminate this risk.

**Data Availability Risk:** If all storage replicas are simultaneously destroyed (correlated failure, catastrophic disaster), event data may be permanently lost even though hash commitments remain on the anchoring chain. Redundancy and geographic distribution reduce but cannot eliminate this risk.

**Key Management Risk:** Compromise of validator signing keys or HSMs could enable an attacker to forge new proofs or anchors. Hardware security and key rotation mitigate but do not eliminate this risk.

### **13.2 Conditions Where Guarantees Fail**

**Guarantee Failure Conditions:**

| Guarantee | Failure Condition |
| :---- | :---- |
| Tamper-Evidence | Hash function collision attack; storage layer modification bypass |
| Causal Ordering | Byzantine validators \> 1/3; network partition causing fork |
| Contextual Integrity | Schema hash or Axiom Hash not properly enforced; schema registry compromise |
| SPV Verifiability | Anchor chain reorganization; hash algorithm migration without backward compatibility |
| Data Availability | Total replica loss; prolonged network partition |
| Forward Integrity | Validator key compromise combined with historical data modification |

### **13.3 Cryptographic Dependency Transparency**

TL’s integrity model depends on:

1. **SHA-256 (or configured hash function):** Collision resistance, preimage resistance, second-preimage resistance

2. **ECDSA / Ed25519 (signing):** Existential unforgeability under chosen message attack (EUF-CMA)

3. **AES-256-GCM (encryption):** IND-CPA confidentiality, authenticated encryption

4. **PBFT Consensus:** liveness and safety properties under partial synchrony assumptions

5. **Anchoring Chains:** Their respective security assumptions (Bitcoin PoW, Ethereum PoS)

The system is designed to operate with algorithm agility: each cryptographic primitive can be replaced by a successor algorithm without rebuilding the entire system.

### **13.4 Data Loss Impact Assessment**

**Scenario: Total Storage Loss**

* **Impact:** Event data becomes unrecoverable; only hash commitments on anchoring chains remain

* **Recovery:** System cannot process verification requests requiring plaintext; can only verify hash chain continuity

* **Duration:** Permanent for archived events; recoverable from auditors/archives for recent events

**Scenario: Partial Storage Loss**

* **Impact:** Some events become unavailable; system operates in degraded mode; new anchoring pauses until threshold replicas restored

* **Recovery:** Reconstruct from remaining replicas; cross-verify against auditor copies

**Scenario: Anchor Chain Failure**

* **Impact:** New anchors cannot be published; system continues operating with unanchored micro-roots; settlement finality delayed

* **Recovery:** Anchor chain service restoration; replay of deferred anchoring

**Scenario: Catastrophic Validator Failure (≥1/3 byzantine)**

* **Impact:** Consensus may accept invalid events; hash chain integrity of newly committed events compromised

* **Recovery:** Validator set remediation; hard fork to clean state; historical events (pre-compromise) remain verifiable

---

## **Glossary**

**Act (+1):** TL triadic outcome indicating approval to proceed with a transaction or action.

**AxiomSetHash:** Cryptographic hash of the complete TL rule set active at a specific point in time, embedded in each event leaf to enforce contextual integrity.

**BFT (Byzantine-Fault Tolerance):** System property of tolerating arbitrary (byzantine) behavior by up to f faulty nodes in a system of 3f+1 total nodes.

**Cascade Micro-Root:** Intermediate Merkle root computed during deferred anchoring mode, binding events in the deferral buffer to an unbroken cryptographic chain.

**Crypto-Shredding:** Cryptographic data erasure technique involving destruction of encryption keys while preserving hash commitments.

**Deferred Anchoring Mode:** Operational mode during high-frequency execution where full anchoring is temporarily deferred while micro-root commitments maintain cryptographic continuity.

**Domain Subtree:** Merkle subtree dedicated to events within a specific TL decision domain (Economic Systems, Financial Infrastructure, Cyber-Physical Systems).

**Epistemic Hold (0):** TL triadic outcome indicating a decision to pause and await additional information or consensus.

**ESS (Economic Systems Subtree):** Merkle subtree containing events related to economic decision governance.

**Event ID:** Globally unique identifier for each TL event, using UUIDv7 format for temporal ordering.

**FIS (Financial Infrastructure Subtree):** Merkle subtree containing events related to financial infrastructure governance.

**Forward Integrity:** Security property ensuring that compromise at time T does not enable modification of events committed before time T.

**HSM (Hardware Security Module):** Tamper-resistant hardware device for secure key storage and cryptographic operations.

**Invariant III (Execution Legitimacy Constraint):** Fundamental TL invariant requiring that no transaction commit or actuation command is valid without a corresponding Merkle-committed log entry.

**Light Client:** Minimal verification endpoint maintaining only current root and verification data, enabling SPV-style verification without full data replication.

**Master Root:** Top-level Merkle root aggregating the three domain subtree roots.

**Merkle Proof:** Cryptographic witness demonstrating that a specific leaf is included in a Merkle tree with a given root.

**PBFT (Practical Byzantine Fault Tolerance):** Consensus protocol providing byzantine-fault tolerance in partially synchronous networks.

**prev\_event\_hash:** Hash of the immediately preceding leaf, providing causal ordering and preventing reordering attacks.

**Refuse (-1):** TL triadic outcome indicating rejection of a transaction or action.

**Root-of-Rooms:** Highest-level Merkle aggregation providing long-term historical anchoring of Master Roots.

**Schema Hash:** Hash of the schema definition used to serialize a leaf, enabling detection of schema version mismatches.

**seq\_id:** Monotonically increasing sequence number providing linear ordering of events.

**Sparse Merkle Tree (SMT):** Merkle tree over a large key space, enabling efficient key-value lookups and non-membership proofs.

**SPV (Simplified Payment Verification):** Method for verifying specific transactions without downloading the full blockchain.

**Ternary Logic (TL):** Governance framework using triadic logic (Act \+1, Epistemic Hold 0, Refuse \-1) for decision recording.

**Verification Hold:** Protective suspension state triggered when external data provenance cannot be cryptographically validated.

---

## **References**

\[1\] Merkle, R. (1987). “A Digital Signature Based on a Conventional Encryption Function.” Advances in Cryptology — CRYPTO ’87. Lecture Notes in Computer Science, vol. 293. Springer.

\[2\] Lamport, L., Shostak, R., Pease, M. (1982). “The Byzantine Generals Problem.” ACM Transactions on Programming Languages and Systems (TOPLAS), 4(3), 382-401.

\[3\] Castro, M., Liskov, B. (2002). “Practical Byzantine Fault Tolerance and Proactive Recovery.” ACM Transactions on Computer Systems, 20(4), 398-461.

\[4\] Nakamoto, S. (2009). “Bitcoin: A Peer-to-Peer Electronic Cash System.” Bitcoin.org.

\[5\] Buterin, V. (2013). “Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform.” Ethereum White Paper.

\[6\] Laurie, B., Langley, A., Kasper, E. (2013). “Certificate Transparency.” RFC 6962\. IETF.

\[7\] Mykletun, E., Narasimha, M., Tsudik, G. (2004). “Authentication and Integrity in Outsourced Databases.” ACM Transactions on Storage, 2(2), 107-138.

\[8\] Rivest, R., et al. (2012). “Keccak.” NIST SHA-3 Competition Finalist.

\[9\] Dwork, C., Lynch, N., Stockmeyer, L. (1988). “Consensus in the Presence of Partial Synchrony.” Journal of the ACM, 35(2), 288-323.

\[10\] IEEE (2021). “IEEE Standard for Permissible Hash Algorithms for Electronic Signature.” IEEE 1363a-2004.

\[11\] NIST (2022). “Post-Quantum Cryptography: Selected Algorithms 2022.” National Institute of Standards and Technology.

\[12\] RFC 8949 — CBOR (Concise Binary Object Representation) Deterministic Tag Encoding. IETF.

\[13\] RFC 7515 — JSON Web Signature (JWS). IETF.

\[14\] RFC 7519 — JSON Web Token (JWT). IETF.

\[15\] RFC 3161 — Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP). IETF.

\[16\] AWS CloudHSM Documentation. Amazon Web Services.

\[17\] Ethereum 2.0 Light Client Specification. Ethereum Foundation.

\[18\] Certificate Transparency: How CT Works. Chrome Platform Security.

\[19\] BLAKE3 Algorithm Specification. BLAKE3 Team, 2020\.

\[20\] UUID Version 7: Time-Based Orderable UUID Format. IETF Draft (draft-ietf-uuidrev).

---

## **Appendix A: ASCII Art — Ternary Tree Structure**

                    MASTER ROOT  
                   /     |      \\  
          ESS\_ROOT   FIS\_ROOT   CPS\_ROOT  
              |          |          |  
          \[ESS\_1\]     \[FIS\_1\]    \[CPS\_1\]  
         /  |  \\      / | \\      /  |  \\  
    \[E1\] \[E2\] \[E3\] \[F1\] \[F2\] \[F3\] \[C1\] \[C2\] \[C3\]

Legend:  
  E\# \= Economic System event  
  F\# \= Financial Infrastructure event  
  C\# \= Cyber-Physical System event

---

## **Appendix B: Event Flow Diagram**

  \+---------+    \+-----------+    \+----------+    \+----------+  
  | Event   | \-\> | Validator | \-\> | Merkle   | \-\> | Consensus|  
  | Payload |    | Preprocess|   | Leaf Hash|    |  Commit  |  
  \+---------+    \+-----------+    \+----------+    \+----------+  
                                                        |  
                                                        v  
  \+-----------+    \+----------+    \+------------+    \+--------+  
  | Auditor   | \<- | Anchor   | \<- | Deferred   | \<- | Micro  |  
  | Replicate |    | Publish  |   | Buffer     |    | Root   |  
  \+-----------+    \+----------+    \+------------+    \+--------+

---

## **Appendix C: Proof Verification Code (Pseudocode)**

function verify\_merkle\_inclusion(proof, root):  
    // Step 1: Verify leaf hash  
    computed\_leaf\_hash \= hash(proof.leaf\_bytes, proof.hash\_algo\_version)  
    if computed\_leaf\_hash \!= proof.leaf\_hash:  
        return FALSE

    // Step 2: Reconstruct root from proof  
    current\_hash \= proof.leaf\_hash  
    position \= compute\_position(proof.seq\_id)  
    branching\_factor \= 3  // ternary

    for i in range(len(proof.proof\_hashes) // 2):  
        sibling\_hash\_1 \= proof.proof\_hashes\[2\*i\]  
        sibling\_hash\_2 \= proof.proof\_hashes\[2\*i \+ 1\]

        // Combine hashes based on position parity  
        if position % 3 \== 0:  
            combined \= hash(current\_hash || sibling\_hash\_1 || sibling\_hash\_2)  
        elif position % 3 \== 1:  
            combined \= hash(sibling\_hash\_1 || current\_hash || sibling\_hash\_2)  
        else:  
            combined \= hash(sibling\_hash\_1 || sibling\_hash\_2 || current\_hash)

        current\_hash \= combined  
        position \= position // branching\_factor

    // Step 3: Verify computed root matches claimed root  
    return current\_hash \== root

---

*End of Report*

**Document Version:** 1.0 

**Author:** Lev Goukassoan

**Classification:** Technical Specification 

**Distribution:** Unlimited
