# Structural, Adversarial, and Availability-Hardened Merkle Architecture for Ternary Logic (TL)

**Version:** 1.0  
**Status:** Specification  
**Framework:** Ternary Logic (TL) — Global Decision Systems Architecture  
**ORCID:** 0009-0006-5966-1243  

---

## Section 0 — System Model

### 0.1 Node Taxonomy

**Validators** are the authoritative participants in TL's execution fabric. Each validator maintains a full replica of the append-only event log, constructs and verifies Merkle subtrees for its assigned decision domain, and participates in root anchoring consensus. Validators are trusted to execute TL triadic logic correctly but are explicitly modeled as potentially Byzantine: the architecture assumes that any individual validator may be compromised, coerced, or colluding. A validator's signed Merkle root carries cryptographic weight only when corroborated by a threshold of independent validators (quorum threshold: ⌈2n/3⌉ + 1 for Byzantine fault tolerance).

**Auditors** are read-only participants with full log access. Auditors do not write to the event log and do not participate in Merkle root construction. Their function is independent forensic verification: given an event payload and a Merkle inclusion proof, an auditor verifies the proof against a publicly anchored root without trusting any validator. Auditors are explicitly untrusted by the system — their outputs are informational, not operative. An auditor asserting proof invalidity triggers the anomaly pathway defined in Section 9 but does not unilaterally suspend execution.

**Light Clients** are constrained verifiers — regulators, infrastructure operators, or third-party oversight entities — that hold only anchored root hashes and verify individual events via logarithmic inclusion proofs. Light clients do not download or store the full event log. Their trust model is anchoring-dependent: they trust the correctness of the anchored root as established by the multi-chain anchoring strategy defined in Section 5. A light client that cannot obtain an anchored root from at least two independent chains is in a degraded verification state and must not certify event validity.

### 0.2 Network Model

TL assumes a **partially synchronous** network model in the sense of Dwork, Lynch, and Stockmeyer (1988): the network alternates between synchronous periods (bounded message delay Δ) and asynchronous periods (unbounded delay). The system's liveness guarantees are conditional on synchronous periods being sufficiently frequent to complete anchoring within the maximum deferral window of 500 ms defined in Section 5. Safety guarantees — tamper evidence, causal ordering, and Merkle integrity — hold unconditionally under asynchrony; no event committed during an asynchronous period can be silently reordered or suppressed without invalidating at least one hash chain link.

The practical implication is that TL does not rely on network synchrony for correctness. It relies on synchrony only for timely anchoring. If anchoring is delayed beyond 500 ms due to network partition, the Deferred Anchoring Mode defined in Section 5 activates, maintaining cryptographic integrity via cascade roots stored in a write-ahead log.

### 0.3 Trust Boundary Definitions

**Trusted components:** Hardware Security Modules (HSMs) holding signing keys for Merkle root attestation; Trusted Platform Modules (TPMs) providing hardware-backed monotonic counters for sequence ID enforcement; the write-ahead log (WAL) storage medium when protected by hardware encryption at rest.

**Untrusted components:** All software processes running on general-purpose operating systems, including the TL execution engine itself. Any software component is assumed potentially exploitable. The Merkle structure is designed so that a compromised software component cannot silently falsify a committed event without producing a detectable hash mismatch at the next verification point.

**Conditionally trusted components:** External timestamping authorities (TSAs) are trusted for timestamp binding but not for event content. If a TSA is compromised, timestamp integrity degrades but Merkle structural integrity and causal ordering remain intact via the prev_event_hash chain. Anchoring chains (blockchains) are trusted for root immutability after sufficient confirmation depth (minimum 6 confirmations on proof-of-work chains; 1 finalized epoch on proof-of-stake chains with BFT finality).

### 0.4 Failure Model

TL employs **Byzantine Fault Tolerance (BFT)** for the validator set, not merely crash-fault tolerance. The justification is as follows: the adversarial threat model includes malicious insiders with log write access, compromised infrastructure operators, and nation-state-level adversaries capable of coercing individual nodes. Crash-fault tolerance (CFT) assumes failures are benign — nodes stop responding but do not actively lie. BFT assumes failures may be adversarial — nodes may forge, delay, or selectively omit messages. Given TL's deployment context (financial infrastructure, cyber-physical systems, economic governance), the weaker CFT assumption is architecturally insufficient.

The system tolerates up to f = ⌊(n−1)/3⌋ Byzantine validators out of n total, consistent with the BFT lower bound. For a minimum deployment of n = 4 validators, f = 1 Byzantine node is tolerated. Recommended minimum deployment is n = 7, tolerating f = 2.

### 0.5 External Dependency Trust

**Timestamping authorities (RFC 3161):** Trusted for timestamp binding only. TSA signatures are verified against a pinned certificate chain. TSA compromise degrades timestamp non-repudiation but does not invalidate Merkle proofs. Multiple independent TSAs are required (minimum 2); timestamp binding uses the earliest consistent timestamp across all responding TSAs.

**Anchoring chains:** Treated as append-only public bulletin boards. TL does not trust any single chain for finality. Multi-chain anchoring (Section 5) requires root commitment on at least two chains from distinct consensus families (e.g., one proof-of-work, one proof-of-stake with BFT finality) before an anchoring cycle is considered complete.

**Storage providers:** Treated as untrusted infrastructure. All pre-hash event data is encrypted before storage. Storage providers are trusted only for availability, not confidentiality or integrity. Integrity is enforced by Merkle proofs; confidentiality is enforced by encryption. A storage provider that corrupts or deletes data triggers the disaster recovery protocol in Section 8 but does not compromise cryptographic guarantees for data that was already Merkle-committed.

---

## Section 1 — Merkle as a Core Structural Component of TL

### 1.1 Why Merkle Is Necessary, Not Optional

TL's governance guarantees rest on four properties that are structurally impossible without a cryptographic accumulator binding event history into a single verifiable commitment: **tamper evidence**, **causal ordering**, **selective verifiability**, and **immutable decision freezing**. Merkle trees provide all four simultaneously with logarithmic proof size.

Without Merkle commitment, each of TL's core governance claims collapses:

A claim that a transaction was governed by Epistemic Hold (0) rather than Act (+1) becomes an assertion without cryptographic backing. An auditor cannot distinguish a retroactively relabeled outcome from an original one. The Eight Pillars enforcement history becomes a mutable narrative rather than a fixed record. Schema versioning becomes advisory rather than enforced: a developer could silently alter the rule-set applied to a past decision. The Immutable Ledger property, which is foundational to TL's accountability model, requires that the hash of every committed event be permanently bound into a structure that cannot be altered without detection. Merkle trees are the minimal construction that achieves this at scale.

### 1.2 TL Properties That Collapse Without Merkle

**Immutable Ledger:** Without Merkle commitment, log entries are individually hashable but not mutually bound. Deleting an entry between entries i and j would not be detectable from entries i+1 through j. The prev_event_hash chain (defined in Section 2) provides linear linking, but without periodic Merkle root anchoring, the chain is only as trustworthy as the node that holds it. Anchoring a Merkle root on a public chain makes suppression detectable globally.

**Epistemic Hold Immutability:** The Epistemic Hold (0) state represents a governance decision not to act. Its forensic value depends entirely on the impossibility of retroactive reclassification to Act (+1). Without a Merkle-committed, anchored hash of the outcome at decision time, a malicious actor with log write access could change the triadic outcome field in a stored event and reconstruct a plausible log. With Merkle commitment, altering any field in a committed event invalidates every ancestor hash up to the anchored root, producing a detectable inconsistency.

**Active Axiom Set Integrity:** The Active Axiom Set Hash (defined in Section 2) commits the exact TL rule-set applied at event time. Without Merkle inclusion, this hash exists only as a field in a mutable record. With Merkle inclusion, the axiom set hash is frozen into the anchored root. Any retroactive claim that a different rule-set was in effect is falsifiable by proof.

**Selective Verifiability:** Without a tree structure, verifying one event requires either trusting the presenting party or downloading the full log. Merkle inclusion proofs of size O(log n) enable a light client to verify a single event against the anchored root in milliseconds. This property is non-negotiable for regulatory use: a regulator cannot be required to replicate the full TL event history to audit a single transaction.

**Forward Integrity:** The hash chain (each root including the prior root's hash) means that any tampering with historical events invalidates all subsequent roots. This property requires the chained structure of Merkle roots over time, not just individual event hashes.

### 1.3 How Merkle Freezes Epistemic Hold Outcomes

When a TL decision engine produces an Epistemic Hold (0) outcome, the following sequence executes atomically (the atomicity guarantee is formally specified in Section 6):

1. The event payload is serialized in canonical form (Section 2, Determinism Requirements).
2. The triadic outcome field is set to 0 (Epistemic Hold).
3. The event is hashed using SHA3-256 (Section 3, Hashing).
4. The leaf hash is inserted into the rolling Merkle buffer at the position determined by its Monotonic Sequence ID.
5. The updated subtree root is computed.
6. The transaction commit — or, for Epistemic Hold, the non-commit — is recorded with a reference to the committed leaf hash.

The causal ordering guarantee (Section 6) ensures that step 4 occurs before or simultaneously with step 6. No mechanism exists to commit a transaction or record a non-action without first committing the corresponding Merkle leaf. The outcome is therefore frozen at the moment of decision, not at the moment of anchoring. Anchoring makes the freeze globally verifiable; the freeze itself is local and immediate.

### 1.4 Active Axiom Set Hash and Contextual Integrity

Each TL decision is made against a specific version of the TL rule-set: the Eight Pillars definitions, risk classification thresholds, Epistemic Hold trigger conditions, and domain-specific governance parameters. This rule-set is called the Active Axiom Set. Its hash is computed over the canonical serialization of the full rule-set document at version V_k and embedded in every leaf node produced under that rule-set version.

If the rule-set changes (producing version V_{k+1}), the Active Axiom Set Hash changes. Events produced before the change retain the old hash; events after retain the new hash. A verifier can determine with cryptographic certainty which rule-set governed any given decision. Retroactive reinterpretation — claiming that event E was evaluated under V_{k+1} when it was actually evaluated under V_k — is detectable because the leaf hash includes the axiom hash, and the leaf hash is Merkle-committed.

### 1.5 Hierarchical Subtrees and TL Decision Domains

TL operates across three primary decision domains: Economic Systems, Financial Infrastructure, and Cyber-Physical Systems. Each domain is assigned a dedicated Merkle subtree. Events are routed to the appropriate subtree based on the Pillar Reference field in the leaf schema (Section 2). The three subtree roots are aggregated into a Master Root via a higher-order Merkle construction (Section 4). This architecture serves two purposes: it isolates domain-specific audit trails (a financial regulator need only verify the Financial Infrastructure subtree root against the Master Root, not the full event log), and it provides domain-level tamper evidence independent of cross-domain events.

### 1.6 Proof Compression and Scalable Governance

At 10,000 events per second with a balanced binary tree, the inclusion proof for any single event consists of O(log_2 N) hashes, where N is the total number of leaves. At N = 10^9 (approximately 27 hours of operation at 10,000 events/sec), the inclusion proof is 30 hashes × 32 bytes = 960 bytes. This proof size is independent of the total event volume and enables a regulator on a standard laptop to verify any historical event against the anchored root in under 10 ms, with no access to the full event database.

### 1.7 Crypto-Shredding and Hash Continuity

Crypto-shredding is the practice of rendering personal or sensitive data permanently unreadable by destroying the encryption keys used to encrypt it, rather than attempting to delete underlying storage. In TL, pre-hash event data containing personal identifiers is encrypted under an ephemeral per-period key K_t before hashing. When the retention period for that data expires (per the jurisdiction-specific retention horizon defined in Section 8), K_t is destroyed.

The critical property is that the leaf hash — computed over the canonical form of the event, which includes only pseudonymized or redacted identifiers (Section 2, Privacy Requirements) — remains valid and verifiable after key destruction. The Merkle proof for the event remains intact. An auditor can verify that an event of a given type, with a given triadic outcome, governed by a given Active Axiom Set, occurred at a given time, without being able to reconstruct the personal data that was associated with it. This satisfies both the cryptographic integrity requirement and data minimization obligations under applicable privacy regulations.

### 1.8 Concrete Scenario: Prevention of Retroactive Reinterpretation

**Scenario:** A financial infrastructure operator processes a high-risk derivative transaction at T=0. The TL decision engine, operating under Active Axiom Set V_3, produces an Epistemic Hold (0) outcome. The transaction is not executed. At T=72h, a compliance officer claims the decision was actually Act (+1), asserting that the transaction was approved and the hold was a system error.

**Without Merkle:** The event log contains a record with outcome field "0". If the operator has write access, this field can be changed to "1". The log hash can be recomputed. Without an external, immutable anchor of the original hash, the forensic record is ambiguous.

**With Merkle (TL architecture):** At T=0, the event is serialized, hashed, inserted into the Merkle tree, and the subtree root is updated. Within 500 ms, the subtree root is anchored on two independent public chains. At T=72h, the compliance officer presents a modified event with outcome "1". The verifier computes the leaf hash of the modified event and attempts to reconstruct the Merkle path to the anchored root. The leaf hash does not match any leaf in the committed tree. The proof fails. The original outcome "0" remains the only cryptographically valid state for that event. The retroactive reinterpretation is falsified.

---

## Section 2 — Canonical Leaf Node Specification

### 2.1 Schema Definition

A TL state transition event is represented as a leaf node L_i with the following mandatory fields, in strict canonical order:

```
L_i := {
  event_id          : UUID v4 (128-bit, RFC 4122)
  seq_id            : uint64, monotonically increasing, globally unique per domain
  prev_event_hash   : bytes[32], SHA3-256 of L_{i-1} canonical serialization
  timestamp_utc     : int64, Unix epoch milliseconds, RFC 3161 TSA-bound
  tsa_signature     : bytes, RFC 3161 timestamp token
  hold_trigger_src  : enum { RISK_THRESHOLD | PILLAR_CONFLICT | AXIOM_BOUNDARY |
                              ORACLE_UNVERIFIABLE | MANUAL_OVERRIDE }
  pillar_ref        : uint8[1..8], reference to one or more of the Eight Pillars
  risk_class        : enum { LOW | MEDIUM | HIGH | CRITICAL }
  domain            : enum { ECONOMIC | FINANCIAL | CYBER_PHYSICAL }
  triadic_outcome   : int8 { +1 | 0 | -1 }
  integrity_flags   : uint32, bitmask of integrity check results
  schema_version    : uint16, increments on any schema change
  schema_hash       : bytes[32], SHA3-256 of canonical schema definition at schema_version
  axiom_set_hash    : bytes[32], SHA3-256 of canonical Active Axiom Set at version V_k
  hash_algo_version : uint8, algorithm identifier (0x01 = SHA3-256, 0x02 = BLAKE3,
                              0x10 = SHA3-256 + Dilithium hybrid)
}
```

### 2.2 prev_event_hash

The prev_event_hash field contains the SHA3-256 hash of the immediately preceding leaf L_{i-1} in the same domain sequence. For the genesis event (seq_id = 0), prev_event_hash is set to the 32-byte zero vector. This field enforces linear ordering within a domain sequence and prevents reordering attacks: any attempt to insert, delete, or reorder events between positions i and j invalidates prev_event_hash for all events from position i+1 onward, producing a detectable chain break at verification.

This field is distinct from the Merkle tree structure itself. The Merkle tree provides inclusion proofs for any event against the current root. The prev_event_hash chain provides linear ordering guarantees within a sequence, independent of tree construction timing. Together they provide both random-access inclusion proof and sequential ordering proof.

### 2.3 Active Axiom Set Hash Requirement

The axiom_set_hash is computed as SHA3-256 over the UTF-8 encoded, canonically serialized TL rule-set document (JSON Canonicalization Scheme per RFC 8785) at the version active at event time. The rule-set document includes: all Eight Pillar definitions, risk classification thresholds, Epistemic Hold trigger conditions, domain routing rules, and governance parameter values.

Any change to any field in the rule-set document produces a new axiom_set_hash value. The mapping from axiom_set_hash to rule-set version is maintained in the signed schema registry defined in Section 9. A verifier presented with a historical event can retrieve the exact rule-set version from the registry, verify the registry entry's signature, recompute the axiom_set_hash, and confirm that it matches the value committed in the leaf. This chain makes retroactive reinterpretation cryptographically impossible: the leaf hash (and therefore the Merkle proof) is invalidated by any change to the axiom set hash field.

### 2.4 Determinism Requirements

Canonical serialization uses **Protocol Buffers v3** (proto3) with deterministic serialization mode enabled (marshal with deterministic flag). Fields are serialized in field number order. The encoding standard is UTF-8 for string fields; fixed-width little-endian for numeric fields; raw bytes for hash fields. Non-deterministic values (current wall clock, random nonces not derived from the sequence ID) are explicitly prohibited as leaf fields. All timestamp values are pre-bound to TSA signatures before leaf construction; the TSA signature is included in the leaf, binding the timestamp at the moment of TSA response receipt.

Locale-dependent encodings (locale-specific date formats, locale-specific decimal separators) are prohibited. All numeric fields use their canonical binary representations. The canonical serialization of L_i must produce an identical byte sequence on any compliant implementation, on any hardware, in any locale.

### 2.5 Privacy Requirements

Personal data associated with a TL event (counterparty identifiers, operator identifiers, entity references) must be processed through the following pipeline before any field value is included in the leaf schema:

**Step 1 — Redaction:** Fields containing free-text personal data that are not required for governance audit (e.g., natural language transaction descriptions containing names) are redacted to a fixed-length placeholder. The redaction is logged with a redaction audit entry cross-referenced to the event_id.

**Step 2 — Pseudonymization:** Structured identifiers (account numbers, entity IDs, operator IDs) are replaced with cryptographic pseudonyms derived as HMAC-SHA256(pseudonymization_key, raw_identifier), where pseudonymization_key is domain-specific and rotated per retention period. The pseudonymization mapping is stored separately from the event log, under access control, and subject to the same crypto-shredding schedule as the pre-hash event data.

**Step 3 — Prohibition:** Raw personal data in any form is explicitly prohibited from the leaf schema. Hash functions are not privacy-preserving when applied to low-entropy inputs (e.g., names, account numbers from a known universe); SHA3-256("ACCT-12345") is trivially reversible by enumeration. Only pseudonymized or redacted values may be hashed.

The redaction audit log is itself a TL event log subject to Merkle commitment, creating a verifiable chain from the pseudonymized leaf to the redaction decision.

### 2.6 Immutability Enforcement

Immutability is enforced through three interlocking mechanisms:

First, the leaf includes schema_hash: any change to the schema structure changes this hash, invalidating all leaf hashes computed under the old schema. Schema changes require a schema_version increment (Section 9), and the new schema_hash is computed and registered before any new events are processed.

Second, the leaf hash is computed over all fields including schema_hash and axiom_set_hash. Mutation of any field — including metadata fields — invalidates the leaf hash and propagates invalidation up the Merkle tree to the anchored root.

Third, the append-only storage enforcement (Section 9) prevents physical mutation of committed leaf records. The combination of append-only storage and hash commitment means that an attacker must either mutate storage (detectable by periodic integrity checks) or forge a hash preimage (computationally infeasible under SHA3-256).

---

## Section 3 — Merkle Tree Construction Model

### 3.1 Hash Algorithm Selection

TL uses **SHA3-256** (FIPS 202, Keccak-based) as the primary hash algorithm. The selection is justified by the following properties: SHA3-256 provides 128-bit collision resistance and 256-bit preimage resistance; it is standardized by NIST and approved for use in high-assurance cryptographic applications including financial infrastructure; its sponge construction is structurally distinct from SHA-2, providing defense-in-depth against SHA-2-specific attacks; it is widely implemented in hardware (including HSMs certified under FIPS 140-3), enabling the hardware-backed hashing path required for the ≤2 ms latency budget.

BLAKE3 is designated as the secondary algorithm (hash_algo_version 0x02) for performance-critical paths where SHA3-256 throughput is insufficient. BLAKE3 provides equivalent security at significantly higher throughput on modern hardware (approximately 3× SHA3-256 on AVX-512 implementations). BLAKE3 outputs are 256-bit by default and are compatible with the leaf schema's 32-byte hash fields.

The hash_algo_version field in each leaf records which algorithm produced the leaf hash, enabling heterogeneous migration periods where old events use SHA3-256 and new events use an upgraded algorithm.

### 3.2 Post-Quantum Survivability Analysis

SHA3-256's collision resistance against quantum adversaries using Grover's algorithm is estimated at 128-bit security (Grover provides a quadratic speedup, reducing 256-bit preimage resistance to 128-bit effective security). This remains computationally infeasible for any foreseeable quantum hardware deployment timeline through approximately 2040.

For migration continuity, the hash_algo_version field supports value 0x10, designating a hybrid SHA3-256 + Dilithium (CRYSTALS-Dilithium, NIST PQC standard) construction for leaf signing. Under this hybrid mode, each leaf is both hashed with SHA3-256 and signed with Dilithium. The Merkle tree structure continues to use SHA3-256 hashes; the Dilithium signature provides an additional post-quantum attestation layer over the leaf content. Validators can begin emitting 0x10 leaves before Merkle tree construction is migrated, enabling a phased transition.

Migration to a fully post-quantum hash function (e.g., SHA3-512 truncated, or a future NIST-standardized hash) is supported by the hash_algo_version field: a new version value is registered, old events retain their original algorithm identifier, and verifiers support both. No retroactive rehashing of committed events is required or permitted.

### 3.3 Branching Analysis: Binary vs. Ternary

**Binary tree (branching factor b=2):**
- Tree depth for N leaves: d = ⌈log_2 N⌉
- Inclusion proof size: d × 32 bytes
- At N = 10^6: d = 20, proof = 640 bytes
- At N = 10^9: d = 30, proof = 960 bytes
- Leaf construction: pair adjacent leaves; duplicate last leaf if N is odd

**Ternary tree (branching factor b=3):**
- Tree depth for N leaves: d = ⌈log_3 N⌉
- Inclusion proof size: 2d × 32 bytes (each proof step requires 2 sibling hashes)
- At N = 10^6: d = 13, proof = 832 bytes
- At N = 10^9: d = 19, proof = 1216 bytes
- Leaf construction: group leaves in triplets; pad with null hashes if N mod 3 ≠ 0

**Structural comparison:**

```
Binary tree (8 leaves):          Ternary tree (9 leaves):
         Root                           Root
        /    \                        /  |  \
      H01    H23                   H012 H345 H678
     / \    / \                   / | \ / | \ / | \
   H0 H1  H2 H3  ...            L0 L1 L2 L3 L4 L5 L6 L7 L8
```

**Semantic mapping evaluation:** TL's triadic outcomes (Act +1, Epistemic Hold 0, Refuse −1) map naturally to a ternary branching factor at the conceptual level. A ternary tree node could in principle represent the three possible outcomes of a single decision point. However, this semantic mapping does not provide a practical structural advantage for the Merkle log use case, where leaves represent ordered sequential events rather than decision tree branches. The Merkle tree's function is accumulation and proof, not decision routing. A ternary tree produces shallower trees (depth ratio log_2/log_3 ≈ 1.585) but larger proof steps, yielding comparable total proof sizes. The binary tree is preferred for TL's Merkle log due to universal implementation support, compatibility with Bitcoin/Ethereum proof tooling, and marginally smaller proof sizes at operational event volumes.

**Formal topology justification:** Binary branching is selected. The semantic triadic structure of TL is encoded in the leaf schema (triadic_outcome field) and the Active Axiom Set, not in the tree topology. The tree's function is cryptographic accumulation; its topology is optimized for proof efficiency and implementation maturity, not semantic correspondence.

### 3.4 Construction Requirements

**Asynchronous tree building:** Merkle tree updates are performed on a dedicated background thread (or async task in an event-loop runtime). The tree update operation does not block the critical path of transaction execution. The leaf hash is computed synchronously on the transaction execution thread (this is required for the atomic log commitment in Section 6); the tree update that incorporates the leaf is asynchronous.

**Rolling buffer with integrity checksum:** Leaf hashes are accumulated in a rolling buffer of size B = 1024 leaves (configurable). Each buffer entry includes the leaf hash and a buffer-level CRC-32C integrity checksum. When the buffer fills, a partial subtree root is computed and the buffer is cleared. The partial subtree root is chained into the main tree. Buffer corruption (CRC mismatch) triggers immediate anomaly signaling.

**Deterministic leaf placement:** Leaf position in the tree is determined by seq_id modulo the current tree capacity. This ensures that any implementation produces identical tree structures for identical input sequences, enabling independent reconstruction by auditors.

**Odd-leaf handling:** When the number of leaves at a level is odd, the last leaf hash is duplicated to form a pair, consistent with the Bitcoin Merkle tree convention. This behavior is deterministic and documented in the schema specification; auditors must implement the same rule to produce matching roots.

**Balanced tree enforcement:** The tree is rebuilt as a complete binary tree after each anchoring cycle. Within a cycle, the tree may be unbalanced (complete but not perfectly balanced). The anchored root represents the complete binary tree over all leaves in the cycle.

### 3.5 Replay Protection

**Event ID uniqueness:** event_id (UUID v4) is generated by a cryptographically secure random number generator seeded from the HSM's hardware entropy source. The event log enforces a uniqueness constraint on event_id at the storage layer: any attempt to insert a duplicate event_id is rejected before leaf construction.

**Monotonic sequence validation:** seq_id is issued by a hardware-backed monotonic counter (TPM counter or HSM counter). The counter is incremented atomically with leaf hash commitment. Any seq_id value that is non-consecutive (gap) or non-increasing triggers immediate anomaly signaling and log suspension.

**Replay detection logic:** A replay cache maintains the set of event_ids observed in the current anchoring window. Any event_id present in the cache is rejected as a replay. The cache is persisted to the write-ahead log; on restart, the cache is restored before any new events are processed.

---

## Section 4 — Hierarchical Integrity Model

### 4.1 Domain Subtree Structure

Each of TL's three decision domains maintains an independent Merkle subtree:

- **Subtree_E:** Economic Systems events
- **Subtree_F:** Financial Infrastructure events  
- **Subtree_C:** Cyber-Physical Systems events

Each subtree is a complete binary Merkle tree over the events in its domain, constructed according to the model in Section 3. Domain routing is determined by the domain field in the leaf schema, which is derived from the pillar_ref field via a deterministic mapping defined in the Active Axiom Set. An event cannot appear in more than one subtree.

### 4.2 Master Root Construction

The Master Root R_M is computed as:

```
R_M := SHA3-256(
  root_index          ||  // uint64, monotonically increasing
  timestamp_utc       ||  // int64, Unix epoch milliseconds
  prev_master_root    ||  // bytes[32], hash of previous R_M
  Subtree_E.root      ||  // bytes[32]
  Subtree_F.root      ||  // bytes[32]
  Subtree_C.root      ||  // bytes[32]
  active_axiom_hash   ||  // bytes[32]
  hash_algo_version       // uint8
)
```

The Master Root is a single 32-byte hash that commits the state of all three domain subtrees simultaneously. An inclusion proof for an event E in domain D consists of: the Merkle inclusion proof for E in Subtree_D (O(log n_D) hashes) plus the Subtree_D root, plus the other two subtree roots (2 × 32 bytes), plus the Master Root preimage fields. Total proof overhead above the domain inclusion proof is 5 × 32 bytes + 9 bytes = 169 bytes.

### 4.3 Root-of-Roots Versioning

Each Master Root R_M(k) includes prev_master_root = R_M(k-1). This creates a forward hash chain over all Master Roots: any alteration of a historical Master Root invalidates all subsequent Master Roots. The chain of Master Roots is itself a log; its integrity is verifiable by any party holding the genesis root R_M(0) (which is published in the TL repository and anchored on all supported chains at system initialization).

### 4.4 Subtree Continuity Guarantees

Each subtree root carries a subtree sequence counter that increments with each anchoring cycle. A verifier can detect missing anchoring cycles by checking for gaps in the subtree sequence counter sequence. Missing cycles trigger the reconciliation protocol in Section 5. The combination of prev_event_hash (within-domain linear ordering), subtree root chaining (within-domain cross-cycle continuity), and Master Root chaining (cross-domain cross-cycle continuity) provides three independent layers of continuity enforcement.

---

## Section 5 — Anchoring Strategy

### 5.1 Maximum Anchoring Delay and Trigger Mechanism

The maximum permitted delay between Master Root computation and on-chain anchoring commitment is **500 milliseconds** under normal operation. This bound is enforced by a hardware-backed timer (HSM-internal) that fires at T+500ms after each Master Root computation. If the anchoring transaction has not been confirmed on at least one chain before the timer fires, the Deferred Anchoring Mode activates.

Under normal operation, anchoring is triggered automatically when either of the following conditions is met, whichever occurs first:
1. The rolling buffer accumulates 1,000 new leaf hashes since the last anchor.
2. 250 ms have elapsed since the last anchor.

The 250 ms nominal trigger provides headroom before the 500 ms hard limit to accommodate chain confirmation latency.

### 5.2 Monotonic Root Indexing

Each anchored Master Root carries a root_index value (uint64, HSM-backed monotonic counter). The sequence of anchored root_index values must be strictly increasing with no gaps. A gap in the root_index sequence indicates a missing anchoring cycle, triggering the reconciliation protocol.

### 5.3 Multi-Chain Anchoring Strategy

TL requires Master Root anchoring on a minimum of two chains from distinct consensus families:

**Chain family A (proof-of-work):** Bitcoin mainnet via OP_RETURN output (80-byte maximum payload sufficient for 32-byte root hash + 8-byte root_index + metadata). Finality threshold: 6 confirmations (approximately 60 minutes).

**Chain family B (proof-of-stake with BFT finality):** Ethereum mainnet or equivalent (Cosmos Hub, Polkadot relay chain). Finality threshold: 1 finalized epoch under Casper FFG (approximately 12.8 minutes on Ethereum).

The rationale for dual-family anchoring is defense against chain-level attacks: a 51% attack on one chain does not affect the other. The earlier-finalizing chain (typically the BFT chain) provides faster availability of the anchored root for light client verification; the proof-of-work chain provides longer-horizon security.

**Public verification endpoint:** A publicly accessible REST API exposes anchored root hashes indexed by root_index and timestamp. The endpoint is read-only, unauthenticated, and served from geographically distributed replicas. Its response includes: root_index, master_root_hash, timestamp_utc, chain_A_tx_id, chain_B_tx_id, and the TSA signature binding the timestamp to the root hash.

### 5.4 Time Integrity

Each anchored Master Root is bound to a trusted timestamp via RFC 3161 TSA signature. The TSA signature is obtained before the anchoring transaction is broadcast, binding the timestamp to the root hash before public commitment. The anchoring transaction embeds the TSA-signed root hash in its payload, not the raw root hash, ensuring that the chain record contains timestamp-bound data.

Anti-backdating enforcement: the timestamp_utc field in each Master Root is validated against the TSA signature at anchoring time. Any root with a timestamp more than 5 seconds earlier than the TSA-response time is rejected. The HSM's internal clock is synchronized to GPS-disciplined NTP sources with a maximum permitted skew of 100 ms.

### 5.5 Deferred Anchoring Mode

During high-frequency execution windows (peak event rate > 50,000 events/sec) or during anchoring infrastructure outages, TL may activate Deferred Anchoring Mode. In this mode:

**Cascade roots:** Every 50 ms, an intermediate cascade root is computed over the leaves accumulated since the last cascade root. The cascade root is stored in the write-ahead log (WAL) with its timestamp and seq_id range. Cascade roots are not anchored on-chain; they serve as checkpoints for crash recovery.

**Deferral window:** The maximum permitted deferral is **500 ms** from the last successful anchor. If deferral extends beyond 500 ms without a successful anchor, the system enters a degraded state: new Act (+1) outcomes are suspended (Epistemic Hold is applied to all new decisions pending anchor restoration). Epistemic Hold (0) and Refuse (−1) outcomes continue to be logged and cascade-rooted.

**Crash recovery:** On restart after a crash during deferred mode, the WAL is replayed from the last successfully anchored root_index. Cascade roots are used to reconstruct the partial subtree for the deferred window. The reconstructed subtree is validated against the leaf seq_id sequence (no gaps permitted). Once reconstruction is verified, anchoring resumes from the reconstructed Master Root. Any leaves that cannot be reconstructed from the WAL (due to WAL corruption) are reported as missing events in the anomaly log, and the affected seq_id range is flagged as integrity-degraded.

**WAL implementation:** The write-ahead log is an append-only file on hardware-encrypted storage, fsync'd after each write. Each WAL entry contains: seq_id, leaf_hash, cascade_root (updated incrementally), and a WAL entry CRC-32C. On recovery, WAL entries are read sequentially; any entry with a CRC mismatch terminates the recovery at that point, and the preceding entry marks the last valid recovery position.

**Reconciliation:** Failure to reconcile deferred logs (unresolvable WAL corruption, missing seq_id ranges) produces a permanent integrity gap in the event log. This gap is announced via the public verification endpoint, logged with a signed anomaly record, and treated as an integrity failure for any Merkle proof spanning the affected seq_id range. Such proofs are considered invalid; the corresponding TL governance decisions in the affected range are marked as unverifiable.

### 5.6 Reconciliation Protocol

**Detection:** The reconciliation daemon monitors the root_index sequence on all anchoring chains. A gap between consecutive anchored root_index values (e.g., root_index 1041 anchored after root_index 1039, with 1040 absent) triggers reconciliation.

**Response:** The reconciliation daemon queries the WAL for cascade roots covering the missing root_index range. If cascade roots are found, the missing Master Root is reconstructed and anchored retroactively (on-chain, with a reconciliation flag in the metadata). If cascade roots are absent, the gap is declared an integrity failure and logged to the anomaly log.

**Audit pathway:** All reconciliation events are themselves TL log entries, Merkle-committed, and anchored. An independent auditor can verify the reconciliation chain: original gap detection → WAL reconstruction → retroactive anchor → anomaly log entry.

---

## Section 6 — Causal Integrity Enforcement

### 6.1 Causal Ordering Proof

The Epistemic Hold log commitment must occur before or atomically with the corresponding governance decision record (transaction commit for Act (+1), non-action record for Epistemic Hold (0), refusal record for Refuse (−1)). The following ordering guarantee is enforced by the execution interlock:

**Formal guarantee:** For any event E_i with triadic_outcome o_i, the leaf hash H(E_i) is committed to the Merkle rolling buffer (and the WAL) before the corresponding governance action record is written to the primary database. The seq_id of E_i is issued by the HSM monotonic counter, which is incremented atomically with the WAL write. No governance action record can reference a seq_id that has not been WAL-committed.

This guarantee is implemented via a two-phase commit protocol between the TL execution engine and the Merkle commitment subsystem:

**Phase 1 (prepare):** The execution engine serializes E_i canonically, computes H(E_i), and writes H(E_i) to the WAL. The WAL write is fsync'd. The seq_id is issued. Phase 1 completes only after fsync confirmation.

**Phase 2 (commit):** The execution engine writes the governance action record to the primary database with a reference to seq_id and H(E_i). If Phase 2 fails (e.g., database write error), the WAL entry for H(E_i) is marked as orphaned, and the anomaly log records a commit failure.

A governance action record cannot exist in the primary database without a corresponding WAL entry. A WAL entry that was never followed by a governance action record is detectable as an orphaned entry on the next reconciliation sweep.

### 6.2 Atomic Snapshot Boundary

The atomic snapshot boundary is the pair (WAL write, database write) in Phase 1 and Phase 2 respectively. The boundary is atomic in the sense that: either both writes succeed (normal case), or the WAL write succeeds and the database write fails (recoverable anomaly), or the WAL write fails and the database write is not attempted (safe failure). The case where the database write succeeds without a preceding WAL write is architecturally prevented: the seq_id is not issued (and therefore the database write cannot complete) until the WAL write has been fsync'd.

### 6.3 Execution Interlock

**Transaction commit reference:** Every Act (+1) outcome is recorded in the primary database with a transaction_log_hash field equal to H(E_i) and a transaction_seq_id field equal to seq_id(E_i). Any transaction record missing these fields is rejected at the database write layer.

**Actuation command validity:** In cyber-physical domains, an actuation command is transmitted only after the corresponding TL event (triadic_outcome = +1) has been WAL-committed with its seq_id. The actuation command payload includes seq_id(E_i) and H(E_i). The receiving actuator (if equipped with a TL verification module) verifies the inclusion proof before executing. An actuation command without a verifiable corresponding log entry is rejected by the actuator's TL verification module as structurally invalid, consistent with Invariant III.

**Silent bypass prevention:** The execution interlock is implemented in the HSM, not in software. The HSM holds the signing key for actuation commands. It will not sign an actuation command unless the corresponding event has been WAL-committed (the WAL write triggers an internal HSM state update confirming commitment). A software-level bypass of the interlock does not produce a valid HSM-signed actuation command.

---

## Section 7 — Proof Generation and Verification

### 7.1 Merkle Inclusion Proof

A Merkle inclusion proof for event E_i against anchored root R consists of:

```
Proof_i := {
  leaf_hash       : bytes[32], H(E_i)
  siblings        : bytes[32][d], sibling hashes at each level
  directions      : bits[d], left/right indicator for each level
  root            : bytes[32], claimed root R
  root_index      : uint64
  chain_A_tx_id   : bytes[32]
  chain_B_tx_id   : bytes[32]
  tsa_token       : bytes, RFC 3161 token for root timestamp
}
```

Proof size: 32 + (d × 32) + ⌈d/8⌉ + 32 + 8 + 32 + 32 + |tsa_token| bytes. At d = 30, excluding TSA token: approximately 1,000 bytes. The TSA token is typically 500–2,000 bytes depending on the TSA's certificate chain. Total proof size is under 4 KB for any practical event count.

Verification procedure: recompute the root from leaf_hash using the sibling path, compare to claimed root R, verify R against chain_A_tx_id and chain_B_tx_id on the respective chains, verify TSA token signature.

### 7.2 Non-Inclusion Proof and Sparse Merkle Evaluation

For standard TL Merkle logs (dense, append-only), non-inclusion proofs in the classical sense (proving that a value is not in the tree) are not directly supported by the binary Merkle structure. Non-inclusion is instead demonstrated by proving that no leaf at the claimed seq_id position has a matching event_id: the inclusion proof for position seq_id is computed, and the verifier confirms that the leaf_hash at that position does not match H(E_claimed).

**Sparse Merkle Tree (SMT) evaluation:** A Sparse Merkle Tree over the full uint64 keyspace (2^64 positions) supports native non-inclusion proofs: a proof that position k is empty is a Merkle path terminating in a null leaf hash. SMT non-inclusion proofs are the same size as inclusion proofs (O(log 2^64) = 64 hashes = 2,048 bytes maximum, but compressed to O(depth of non-empty leaves) in practice using default-value compression).

SMT adoption would enable regulators to prove that no event occurred under a given seq_id without requiring full log access. The tradeoff is increased construction complexity and larger tree state. TL specifies SMT as an optional extension for deployments requiring non-inclusion proofs as a primary governance feature. The base TL specification uses a dense append-only tree; the SMT extension is defined in Appendix A (deferred to SDK phase).

### 7.3 Proof Serialization Format

Proofs are serialized using Protocol Buffers v3 (same canonical format as leaf schema) to a binary wire format. A JSON representation is also defined (JSON Canonicalization Scheme per RFC 8785) for regulator-facing interfaces. The JSON representation is larger but human-readable and compatible with standard JSON tooling. Both formats encode identical information; a compliant verifier accepts either format.

### 7.4 Light Client / SPV Verification Specification

**Protocol:** A light client wishing to verify event E_i against anchored root R executes the following steps:

1. Obtain the event payload P_i from any data provider (storage node, operator, or the public data availability layer).
2. Obtain Proof_i from any proof provider (validator set, operator, or public proof service).
3. Obtain the anchored root R at root_index k from any of: the public verification endpoint, a direct chain query to chain_A or chain_B, or a trusted root cache.
4. Verify: recompute leaf_hash from P_i using canonical serialization. Verify the Merkle path from leaf_hash to R using siblings and directions in Proof_i. Verify R against the on-chain commitment at chain_A_tx_id and chain_B_tx_id. Verify the TSA token in Proof_i against the TSA's public certificate.
5. Accept the event as verified if all checks pass. Reject if any check fails.

**Performance characteristics:** Steps 1–3 involve network I/O (latency-dominant). Step 4 involves: one SHA3-256 computation for leaf_hash, d ≈ 30 SHA3-256 computations for path verification, two chain RPC calls (cacheable after first verification of a given root), one TSA signature verification. On a 2024-era laptop: leaf and path hashing completes in under 1 ms; chain RPC calls complete in 50–500 ms (network-dependent, cacheable). Verification is feasible on a mobile device; the bottleneck is network latency, not computation.

**No full dataset download required:** The light client requires only P_i (variable size, typically < 1 KB for a TL event), Proof_i (< 4 KB), and the anchored root (32 bytes + metadata). Total data requirement: under 10 KB per verified event.

**Example verification workflow:**

```
Input:  event_id = "a3f2...", seq_id = 88,421,003
        P_i = { triadic_outcome: 0, domain: FINANCIAL, ... }

Step 1: leaf_hash = SHA3-256(canonical_serialize(P_i))
        = "b7c4e1..."

Step 2: Verify path:
        Level 0: SHA3-256(leaf_hash || sibling[0]) = "d91a..."
        Level 1: SHA3-256("d91a..." || sibling[1]) = "3f88..."
        ...
        Level 29: computed_root = "8e22a1..."

Step 3: Fetch root R at root_index = 88,213 from public endpoint.
        R = "8e22a1..." ✓

Step 4: Verify chain_A_tx_id on Bitcoin: OP_RETURN contains "8e22a1..." ✓
        Verify chain_B_tx_id on Ethereum: log contains "8e22a1..." ✓
        Verify TSA token: signature valid, timestamp = 2025-03-15T14:23:01Z ✓

Result: Event verified. Triadic outcome Epistemic Hold (0) was committed at
        2025-03-15T14:23:01Z under Active Axiom Set V_3.
```

**Verification failure handling:** If the computed root does not match R, the verifier reports: proof_invalid, with the first diverging level in the Merkle path. If R cannot be confirmed on at least one anchoring chain, the verifier reports: root_unanchored, and the verification is inconclusive (not failed — the chain may be experiencing delays). If the TSA token is invalid, the verifier reports: timestamp_unverified; the inclusion proof may still be valid but temporal binding is not confirmed.

### 7.5 Oracle Integrity Constraint and Verification Hold

**Definition:** When a TL decision depends on external data (oracle inputs — price feeds, sensor readings, external event triggers) and that data's provenance cannot be cryptographically validated, the system must not produce an Act (+1) or Refuse (−1) outcome. Instead, it enters **Verification Hold** — a protective suspension state.

**Distinction from Epistemic Hold (0):** Epistemic Hold (0) is a triadic governance outcome produced by the TL decision engine when the engine determines that the evidence, risk profile, or contextual conditions do not warrant commitment to Act (+1) or Refuse (−1). It is a deliberate governance decision. Verification Hold is a pre-decision integrity check failure: the inputs required to make any triadic determination are themselves of unverifiable provenance. The engine cannot enter the triadic decision process until Verification Hold is resolved.

**Operational boundary:**

```
External input arrives
    │
    ▼
Provenance validation:
  - Is input signed by a registered oracle?
  - Is oracle signature verifiable against registry?
  - Is input timestamp within acceptable staleness bound (≤ 30s)?
  - Is input hash committed in a prior TL Merkle log entry (for recursive inputs)?
    │
    ├─ YES → proceed to triadic decision → { +1, 0, -1 }
    │
    └─ NO  → Verification Hold
               │
               ├─ Resolution: oracle re-authenticates input, or
               │               input is replaced with a verified source, or
               │               timeout (configurable, default 5s) → auto-resolve to Epistemic Hold (0)
               │
               └─ Resolution record: TL log entry with
                    hold_trigger_src = ORACLE_UNVERIFIABLE
                    triadic_outcome = 0 (if timeout-resolved)
```

Verification Hold is not a triadic outcome and does not appear as triadic_outcome = 0 in the log unless it times out and is resolved as Epistemic Hold (0). During Verification Hold, no leaf is committed; the hold is recorded as a pending event in the WAL with a status flag. On resolution, the pending event is either completed (as Epistemic Hold) or superseded by a new event with verified inputs.

### 7.6 Key Security

**Ephemeral encryption keys:** Pre-hash event data is encrypted under per-period keys K_t, where the period is defined by the retention schedule (Section 8). Keys are generated inside the HSM and never exported in cleartext.

**Hardware-backed storage:** HSMs certified under FIPS 140-3 Level 3 or higher are recommended for key storage. TPMs (TPM 2.0 specification) provide hardware-backed monotonic counters for seq_id enforcement. Keys for Merkle root signing are stored exclusively in HSM-protected key stores.

**Key rotation schedule:** Encryption keys K_t rotate at the start of each retention period (default: quarterly). Signing keys for Merkle root attestation rotate annually. Rotation events are themselves TL log entries, Merkle-committed, enabling an auditor to verify the key lineage.

**Compromise detection:** HSM tamper detection (physical and logical) triggers immediate key invalidation and anomaly logging. Software-level key compromise (unauthorized extraction attempt) is detected via HSM access logging, which is itself a TL log stream.

### 7.7 Crypto-Shredding

When the retention period for a data class expires, the corresponding K_t is deleted from the HSM. Deletion is irreversible; the HSM provides a signed deletion attestation. Post-deletion, the pre-hash event data is permanently unreadable.

The Merkle proof for events encrypted under K_t remains fully valid after key deletion. The proof authenticates the leaf hash, which was computed over the canonical form of the event before encryption. The leaf hash does not depend on K_t. An auditor post-deletion can verify: that an event occurred, its triadic outcome, its domain, its Pillar reference, its Active Axiom Set, and its timestamp — without being able to reconstruct the pseudonymized identifiers or other personal data that was associated with the event.

---

## Section 8 — Data Availability Strategy

### 8.1 Principle

A Merkle root without retrievable pre-hash event data fails TL governance guarantees. The Merkle tree provides tamper evidence and selective verifiability; it does not by itself guarantee that the full event context needed for forensic reconstruction is available. Data availability must be ensured independently.

### 8.2 Storage Architecture

**Primary storage:** Encrypted event records (pre-hash canonical serializations) are stored in an append-only distributed log (e.g., Apache Kafka with replication factor ≥ 3, or a purpose-built TL storage node cluster). Primary storage is co-located with validators.

**Secondary storage (geographic distribution):** Encrypted event records are replicated to secondary storage nodes in at least three geographically distinct jurisdictions, consistent with the primary data sovereignty requirements of the deployment (e.g., EU, US, APAC). Replication is near-real-time (target: within 5 seconds of primary write).

**Tertiary storage (cold archive):** After 90 days, event records are migrated to cold archival storage (object storage with versioning enabled, e.g., S3-compatible or equivalent). Cold archive is the authoritative long-term store for the retention horizon.

### 8.3 Retention Horizon

The minimum retention horizon is 10 years from the date of event creation, consistent with financial regulatory requirements in major jurisdictions (EU MiFID II: 5 years; US SEC Rule 17a-4: 6 years; jurisdictions with stricter requirements should configure accordingly). For intergenerational review use cases identified in the TL framework objective, the configurable maximum retention horizon is 75 years. Events subject to crypto-shredding after their personal data retention period retain their Merkle-committed hash records indefinitely; only the pre-hash personal data is subject to scheduled deletion.

### 8.4 Centralized vs. Decentralized Storage

**Centralized storage (operator-managed):** Lower latency, simpler key management, higher single-point-of-failure risk. Acceptable for deployments where the operator is itself subject to regulatory oversight and the regulator can compel access.

**Decentralized storage (IPFS, Filecoin, Arweave):** Content-addressed storage aligns naturally with Merkle hash commitments: the CID (content identifier) of an event record is directly derivable from its hash, enabling self-certifying retrieval. Decentralized storage provides higher availability guarantees and censorship resistance but introduces retrieval latency variability and dependency on network incentive structures.

**TL recommendation:** Hybrid model. Primary and secondary storage are operator-managed for performance. Tertiary cold archive is replicated to a decentralized storage network (Filecoin or Arweave) with a proof-of-storage commitment, ensuring long-term availability without dependence on any single operator's continued operation.

### 8.5 Proof-of-Storage and Availability Attestation

For decentralized cold archive, TL requires a proof-of-storage mechanism (e.g., Filecoin's Proof-of-Replication / Proof-of-Spacetime, or Arweave's Succinct Proofs of Random Access) providing cryptographic evidence that the archive node is storing the claimed data. Proofs are verified quarterly; failure to produce a valid proof triggers migration of the affected data to a new archive node.

For centralized storage tiers, availability attestation is provided by the storage SLA (99.99% availability commitment from the storage provider) supplemented by monthly integrity checks: the operator recomputes the Merkle root over all stored events and compares to the anchored root sequence. Any discrepancy triggers the disaster recovery protocol.

### 8.6 Disaster Recovery Protocol

**Scenario:** Primary storage node failure resulting in data loss for seq_id range [a, b].

**Step 1:** Detect loss via monthly integrity check or real-time replication monitoring. Announce affected range on the public verification endpoint.

**Step 2:** Attempt reconstruction from secondary storage (geographic replica). If secondary is intact, restore primary from secondary. Verify restored data against Merkle roots for the affected range.

**Step 3:** If secondary is also affected, attempt reconstruction from tertiary cold archive. Retrieve event records for [a, b] from decentralized storage using their content addresses (derivable from leaf hashes in the WAL). Verify against Merkle proofs.

**Step 4:** If tertiary is also affected (catastrophic failure), the affected range is declared an irreversible data loss event. The Merkle proofs for events in [a, b] remain valid (the hashes are anchored), but the underlying event data is unavailable. This is announced via the public verification endpoint and logged as a permanent availability degradation.

### 8.7 Data Rehydration Workflow

For forensic reconstruction requests (regulatory audit, legal proceeding), the data rehydration workflow is:

1. Requester provides event_id or seq_id range.
2. Operator retrieves encrypted event records from the lowest-latency available storage tier.
3. Operator decrypts records using K_t (if within retention period and key not yet shredded).
4. Operator generates Merkle inclusion proofs for all retrieved events.
5. Operator delivers: decrypted event payloads + inclusion proofs + anchored root references.
6. Requester verifies inclusion proofs independently per the light client protocol (Section 7.4).

If K_t has been shredded (post-retention period), step 3 is omitted and the delivered package contains encrypted records (unreadable) with valid Merkle inclusion proofs. The requester can confirm event existence and metadata but cannot read the personal data content.

---

## Section 9 — Log Truncation and Tamper Resistance

### 9.1 Append-Only Storage Enforcement

The primary event log is stored in an append-only data structure. At the storage layer, this is enforced by: filesystem-level immutability flags (Linux chattr +a for append-only) on log segment files; database-level constraints prohibiting UPDATE and DELETE operations on committed event records; HSM-enforced write policies that reject any write request targeting a seq_id that has already been committed.

Append-only enforcement does not prevent an attacker with root access from modifying underlying storage. It does ensure that any such modification is detectable: the next Merkle integrity check will produce a root mismatch for the modified segment.

### 9.2 Periodic Integrity Checks

Integrity checks are scheduled at four intervals:

**Real-time (continuous):** The WAL's CRC-32C on each entry is verified on every read. Any CRC mismatch triggers immediate anomaly signaling.

**Hourly:** A partial Merkle root recomputation over the last 3,600 seconds of events is performed. The result is compared to the cached partial root from the rolling buffer. Any discrepancy triggers investigation.

**Daily:** A full Merkle root recomputation over all events since the last anchoring cycle is performed. The result is compared to the anchored root. Any discrepancy triggers anomaly signaling and operator notification.

**Monthly:** A full Merkle root recomputation over the entire event history is performed. This is computationally intensive (up to several hours for large deployments) and is executed on a dedicated audit node with read-only access to the primary event log. Any discrepancy triggers the disaster recovery assessment protocol.

### 9.3 Missing Sequence ID Detection

The integrity check process includes a sequential scan of seq_id values in the event log. Any gap (seq_id i present, seq_id i+1 absent, seq_id i+2 present) is logged as a missing event anomaly. The anomaly record includes the affected seq_id, the timestamp of detection, and the result of the WAL query for the missing seq_id (whether a WAL entry exists for the missing position).

### 9.4 Automatic Anomaly Signaling

The anomaly signaling system maintains a prioritized queue of detected integrity violations. Violations are classified:

**Critical:** Missing seq_id, Merkle root mismatch, WAL CRC failure, HSM tamper detection. Response: immediate execution suspension, operator alert, automatic escalation to the independent audit pathway.

**High:** Replication lag exceeding 30 seconds, anchoring delay exceeding 400 ms (pre-warning before 500 ms hard limit), proof-of-storage check failure. Response: operator alert, automatic remediation attempt.

**Medium:** Missing anchoring chain confirmation (one chain unavailable), TSA response latency > 2s. Response: logged, monitored for escalation.

All anomaly records are themselves TL log entries, Merkle-committed. An auditor can verify the integrity of the anomaly detection history.

### 9.5 Schema Governance

**Signed schema registry:** The schema registry is a signed append-only log maintained by the TL governance authority. Each entry records: schema_version, schema_hash, effective_date, and a threshold signature from the validator set (requiring ⌈2n/3⌉ + 1 signatures). The registry is publicly readable; writes require governance authority signatures.

**Dual control for schema updates:** Any schema change requires approval from two independent members of the TL governance authority, whose signatures are both included in the registry entry. This prevents a single compromised governance member from silently modifying the schema.

**Independent anchoring of schema hash:** Each schema_version's schema_hash is anchored on-chain independently (separate from event log anchoring) upon registration. This provides a public, tamper-evident record of all schema versions and their effective dates, enabling verifiers to independently confirm which schema governed events at any historical time.

---

## Section 10 — Latency and Throughput Modeling

### 10.1 Latency Budget

The total transaction execution budget is ≤ 2,000 µs (2 ms). The Merkle commitment operations consume a portion of this budget. The allocation is:

```
Operation                          Allocation (µs)   Notes
─────────────────────────────────────────────────────────────────────────
Canonical serialization             80               proto3 deterministic
SHA3-256 leaf hash computation      40               hardware-accelerated
WAL write (fsync)                  200               NVMe SSD, synchronous
HSM seq_id counter increment        60               TPM 2.0 counter
Merkle rolling buffer insert        20               in-memory, O(log n)
Partial subtree hash update         30               background, amortized
TSA timestamp binding (async)        0               async, off critical path
Anchoring transaction (async)        0               async, off critical path
─────────────────────────────────────────────────────────────────────────
Total Merkle path overhead         430               21.5% of 2,000 µs budget
Remaining for TL execution logic  1,570
```

The critical-path operations (serialization, hashing, WAL write, seq_id increment, buffer insert) consume 430 µs. The WAL fsync is the dominant term; an NVMe SSD with fdatasync latency of 150–200 µs is required to meet this budget. DRAM-backed storage (battery-backed RAM or Intel Optane) reduces this to 10–20 µs, providing 190 µs headroom.

Async operations (TSA binding, tree completion, anchoring) are off the critical path and do not contribute to the 2 ms budget.

### 10.2 Maximum Sustainable Event Rate

At the nominal critical-path overhead of 430 µs per event on a single execution thread: maximum rate = 1,000,000 µs / 430 µs ≈ 2,325 events/sec per thread.

With parallel execution across 8 independent domain-partitioned threads (each domain subtree updated independently): maximum rate ≈ 18,600 events/sec per node.

For the target of ≥ 10,000 events/sec: a 4-thread configuration (2 threads for FINANCIAL, 1 for ECONOMIC, 1 for CYBER_PHYSICAL) meets the target with margin.

### 10.3 Parallel Construction Strategy

Parallelism is achieved by domain partitioning: each domain subtree (Subtree_E, Subtree_F, Subtree_C) is updated by a dedicated thread. Within a domain, events are processed sequentially (required by the prev_event_hash chain). Cross-domain events are impossible by schema design (domain field is mandatory and single-valued). Master Root computation is serialized (occurs at anchoring time, not on the critical path) and takes < 1 µs (single SHA3-256 computation).

### 10.4 Worst-Case Load Model

**Peak load:** 50,000 events/sec for 60 seconds (e.g., end-of-day settlement spike in a financial infrastructure deployment).

**Memory requirement:** Rolling buffer of 1,024 leaves × 32 bytes = 32 KB per domain × 3 domains = 96 KB. At 50,000 events/sec, the buffer fills in 1024/50000 ≈ 20 ms, triggering a partial subtree computation every 20 ms. Partial subtree computation time: O(log 1024) = 10 SHA3-256 operations ≈ 0.4 µs; negligible.

**Disk I/O:** At 50,000 events/sec, WAL write volume is 50,000 × (leaf_hash 32 bytes + CRC 4 bytes + metadata ~100 bytes) ≈ 6.8 MB/sec. An NVMe SSD with sequential write throughput of > 1 GB/sec is not constrained by this volume.

**Anchoring overhead:** At 50,000 events/sec, the nominal 250 ms anchoring trigger fires 4 times/sec. Each anchor produces one Master Root computation (< 1 µs) and one anchoring transaction broadcast (async). Anchoring transaction submission does not block event processing.

### 10.5 Numerical Scenario: 10,000 Events/Sec

**Configuration:** 4 execution threads, NVMe SSD WAL storage, SHA3-256 with AVX-512 acceleration.

**Per-event latency:**
- Serialization: 80 µs
- Hashing: 40 µs  
- WAL write: 200 µs
- seq_id increment: 60 µs
- Buffer insert: 20 µs
- **Total: 400 µs** (within 2 ms budget with 1,600 µs for TL logic)

**Throughput:** 10,000 events/sec = 2,500 events/sec per thread. At 400 µs/event: thread utilization = 2,500 × 0.4 ms = 100% on each thread. This is the maximum sustainable rate for this configuration; any additional load requires adding execution threads or reducing per-event overhead (e.g., by switching WAL to DRAM-backed storage, reducing WAL write to 10 µs and increasing thread capacity to ~25,000 events/sec per thread).

**Proof generation rate:** At 10,000 events/sec, proof generation (async, off critical path) must keep pace. Proof generation requires O(log n) hash lookups; at 30 levels and 10 ns per lookup, proof generation time is 300 ns per proof. Background proof generation capacity far exceeds the event ingestion rate.

---

## Section 11 — Formal Integrity Guarantees

### 11.1 Collision Resistance

**Claim:** An adversary cannot produce two distinct events E and E' such that H(E) = H(E').

**Basis:** SHA3-256 collision resistance, estimated at 2^128 operations under the best known classical attack. Under Grover's algorithm (quantum), the bound reduces to 2^64 — still computationally infeasible for any realistic quantum hardware deployment through the 2040 horizon. Post-quantum migration (Section 3.2) extends this guarantee beyond 2040.

**Degradation conditions:** Collision resistance degrades if SHA3-256 is broken by a mathematical attack not based on brute force (a structural attack on the Keccak sponge). No such attack is currently known. The hash_algo_version field enables migration to a replacement algorithm if structural weaknesses are discovered.

### 11.2 Preimage and Second-Preimage Resistance

**Preimage resistance:** Given H(E), an adversary cannot recover E. SHA3-256 provides 256-bit preimage resistance (2^128 under Grover). This property ensures that the anchored root does not leak event content.

**Second-preimage resistance:** Given E and H(E), an adversary cannot find E' ≠ E such that H(E') = H(E). SHA3-256 provides 256-bit second-preimage resistance. This property ensures that a committed event cannot be silently substituted with a different event with the same hash.

### 11.3 Forward Integrity

**Definition:** An event committed at time T cannot be altered after T without invalidating all Merkle roots computed after T.

**Basis:** The prev_event_hash chain links each event to its predecessor. Any alteration of event E_i changes H(E_i), which changes the prev_event_hash value in E_{i+1}, which propagates through all subsequent events and up to every subsequent Merkle root. Since subsequent Merkle roots are anchored on public chains, the alteration is detectable by anyone who holds any subsequent anchored root.

**Scope:** Forward integrity holds from the point of WAL commit, not from the point of anchoring. Anchoring makes forward integrity globally verifiable; WAL commitment makes it locally enforceable.

### 11.4 Conditions Under Which Guarantees Degrade

**Simultaneous compromise of all anchoring chains:** If all anchoring chains (both Chain A and Chain B) are simultaneously rewritten (50% attack on both), historical roots can be replaced. Mitigation: the public verification endpoint maintains an independent root archive; regulators maintain root caches; the cost of attacking multiple independent chains simultaneously is currently economically infeasible.

**HSM compromise:** If the HSM holding signing keys is compromised, forged root signatures are possible. Mitigation: hardware tamper detection, threshold signatures requiring multiple HSMs, key rotation on suspected compromise.

**Catastrophic hash break:** If SHA3-256 is broken (collision found), the leaf immutability guarantee fails. Mitigation: hash_algo_version field enables emergency migration; post-quantum hybrid mode (Section 3.2) provides a secondary attestation layer.

**WAL destruction before anchoring:** If the WAL is destroyed before an anchoring cycle completes, events in the destroyed range are lost with no cryptographic record. Mitigation: WAL is stored on hardware-encrypted redundant storage; WAL replication to a secondary node is required in production deployments.

### 11.5 Long-Term Survivability Modeling

At a conservative SHA3-256 security degradation rate aligned with NIST post-quantum migration timelines, full migration to a post-quantum hash construction is recommended before 2035. The hash_algo_version field enables gradual migration: new events are emitted with the new algorithm while old events retain their original algorithm identifiers. No rehashing of historical events is performed; historical proofs remain valid under the original algorithm, and verifiers support both. The migration timeline is governed by a formal schema update under the dual-control schema governance process (Section 9.5).

---

## Section 12 — Comparative Analysis

### 12.1 Comparison Matrix

| System | Tree Type | Hash | Proof Size | Non-Inclusion | Finality | TL Relevance |
|---|---|---|---|---|---|---|
| Bitcoin transactions | Binary Merkle | SHA256d | O(log n) | No | ~60 min | Proof model directly applicable |
| Ethereum state trie | Modified Patricia-Merkle | Keccak-256 | O(depth × 32B) | Yes (MPT) | ~13 min (Casper) | State non-inclusion valuable; trie overhead unsuitable for high-throughput log |
| Certificate Transparency | Binary Merkle (append-only log) | SHA-256 | O(log n) | Via consistency proofs | Immediate (signed tree head) | Closest architectural analog; CT's append-only, publicly auditable model directly informs TL design |
| Sparse Merkle Tree | Binary (sparse) | SHA3-256 | O(log 2^256) compressed | Yes (native) | Depends on anchoring | Valuable for non-inclusion proofs; overhead justified only for deployments requiring non-inclusion as primary feature |

### 12.2 Certificate Transparency Alignment

Google's Certificate Transparency (RFC 9162) is the closest architectural analog to TL's Merkle log. CT maintains append-only, cryptographically verifiable logs of TLS certificates with publicly auditable Merkle roots (signed tree heads, STHs). TL's design inherits from CT: the append-only model, the anchored root sequence, the inclusion proof protocol, and the independent auditor model are all structurally analogous. The key differences are: TL uses multi-chain anchoring rather than CT's gossip-based consistency checking; TL's leaves encode triadic governance outcomes rather than certificate data; TL's hierarchical subtree model reflects domain separation absent in CT.

### 12.3 Tradeoff Matrix

| Property | TL Binary Merkle | Ethereum MPT | Certificate Transparency | Sparse Merkle |
|---|---|---|---|---|
| Scalability (events/sec) | High | Medium | High | Medium |
| Proof size | Small (O(log n)) | Medium (path depth) | Small | Medium (compressed) |
| Non-inclusion proof | No (base spec) | Yes | Partial (consistency) | Yes (native) |
| Construction complexity | Low | High | Low | Medium |
| Post-quantum readiness | Via version field | Limited | Limited | Via version field |
| Governance audit clarity | High | Medium | High | High |
| TL domain separation | Native (subtrees) | Via contract | Not applicable | Possible |

---

## Section 13 — Failure Mode Disclosure

### 13.1 Residual Risk Statement

The following residual risks are present in the TL Merkle architecture even under full specification compliance:

**Cryptographic algorithm break:** The entire integrity model depends on the computational hardness of SHA3-256. A polynomial-time algorithm for SHA3-256 collision finding would invalidate all Merkle proofs. Probability: currently assessed as negligible through 2035 based on NIST cryptographic standards track. Mitigation: version-field migration capability; post-quantum hybrid mode.

**Anchoring chain failure:** If both anchoring chains cease to exist (e.g., protocol shutdown, catastrophic network failure), future roots cannot be anchored. Existing anchored roots remain verifiable for as long as chain history is preserved (which is indefinite for archived chain data). Mitigation: multi-chain strategy; maintain independent root archive.

**HSM supply chain compromise:** Hardware-level backdoors in HSM or TPM hardware could subvert key protection and monotonic counter integrity without software-detectable evidence. Mitigation: multi-vendor HSM deployment; open-source HSM firmware where available; physical security controls.

**Implementation divergence:** If the canonical serialization implementation differs between event producers and verifiers, proofs fail for correct events. Mitigation: comprehensive test vectors published in the TL specification repository; compliance test suite required for all implementations.

### 13.2 Conditions Where Guarantees Fail

**Complete WAL destruction before anchoring:** Events in the destroyed window have no cryptographic record. Their governance decisions are unverifiable.

**All storage tiers simultaneously unavailable (catastrophic data loss):** Merkle roots remain anchored and proofs remain structurally valid, but the event payloads they prove are unrecoverable. Governance decisions can be confirmed as having occurred (the hashes exist) but cannot be reconstructed for forensic content review.

**Threshold of validators simultaneously Byzantine (> f):** If more than ⌊(n−1)/3⌋ validators are Byzantine, the BFT guarantee fails and the validator set may produce a forged Master Root. Mitigation: validator selection under legal accountability frameworks; independent auditor monitoring; public anchoring provides post-hoc detection.

### 13.3 Cryptographic Dependency Transparency

This architecture depends on the following cryptographic primitives:

- SHA3-256 (FIPS 202): collision resistance, preimage resistance, second-preimage resistance
- RFC 3161 (TSA): timestamp binding security depends on TSA private key protection
- CRYSTALS-Dilithium (NIST PQC, hybrid mode): post-quantum signature security
- HMAC-SHA256 (pseudonymization): keyed pseudonym security depends on pseudonymization key protection
- CRC-32C (WAL integrity): not a cryptographic primitive; provides only error detection, not tamper evidence

The CRC-32C in the WAL is explicitly not a security control; it detects accidental corruption, not adversarial modification. WAL tamper detection relies on the Merkle integrity checks defined in Section 9.2.

### 13.4 Data Loss and Catastrophic Failure Impact

In the event of catastrophic failure resulting in irreversible loss of event data for seq_id range [a, b]:

- Merkle proofs for events in [a, b] remain valid as structural claims (the hashes are anchored).
- The underlying event content is unrecoverable.
- TL governance decisions in [a, b] are confirmed as having occurred but cannot be forensically reconstructed.
- The public verification endpoint permanently flags [a, b] as a data-loss range.
- Any light client proof for an event in [a, b] should be accompanied by a data-availability disclaimer.
- The governance consequences of this loss (regulatory reporting, contractual implications) are outside the scope of this specification and are determined by applicable law and TL deployment agreements.

---

*End of specification. This document constitutes the canonical Merkle Architecture specification for the Ternary Logic (TL) Global Decision Systems framework. All implementation decisions must be evaluated against the threat model and integrity guarantees defined herein.*
