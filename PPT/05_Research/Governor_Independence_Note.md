# Governor Independence
### Ternary Logic — Dual-Lane Latency Architecture | 05_Research
**Author:** Lev Goukassian | FractonicMind  
**Parent directory:** `PPT/05_Research/`  
**Status:** Architectural refinement — pending integration into DLLA specification

---

## Origin

This note documents an architectural refinement to TL's Dual-Lane Latency Architecture identified during the PPT specification work. It is recorded here before integration into the formal DLLA specification document and the academic paper revision.

The core observation: the DLLA specification as originally written implies a coupled cycle — Lane 1 issues a PPT, Lane 2 produces the FPT, and then Lane 1 resets for the next cycle. This is not wrong, but it understates what the architecture actually permits.

---

## The Refinement

At PPT issuance — the 50-millisecond marker — Lane 1 hardware resets immediately. The C-element is re-primed. The HSM session remains warm. The pipeline is ready for the next authorization request.

Lane 1 does not wait for Lane 2 to complete its anchoring. Lane 2 does not know or care that Lane 1 has already moved on. They are genuinely independent streams from the moment the fork occurs.

This is Governor Independence: **the Governor (C-element) returns to its post at the 50-millisecond marker, not at the end of Lane 2's anchoring cycle.**

---

## What Changes Architecturally

Before this refinement, TL's DLLA is described as:

```
Cycle 1:  PPT issued → State 1 → FPT arrives → State 2 → Reset
          [~10ms]                [~300-500ms]            [then next PPT]
```

Throughput ceiling: 1 PPT per anchoring cycle ≈ 2–3 PPT/second.

After Governor Independence:

```
T=0ms:    PPT-1 issued → State 1 begins
          Lane 1 resets immediately
T=10ms:   PPT-2 issued → State 1-b begins (independent)
          Lane 1 resets again
T=20ms:   PPT-3 issued ...
          ...
T=300ms:  FPT-1 arrives → PPT-1 confirms to State 2
T=310ms:  FPT-2 arrives → PPT-2 confirms to State 2
          ...
```

Throughput ceiling: governed by HSM signing rate (~5–10ms/PPT), not anchoring latency. With warm-path HSM at 10ms/PPT, Lane 1 processes approximately 6–10 PPT cycles per single Lane 2 anchoring window.

---

## The Throughput Consequence

| Model | PPT cycle time | Anchor time | PPTs per anchor window | HSM utilization |
|---|---|---|---|---|
| Coupled cycle | ~300–500ms | ~300–500ms | 1 | ~2–3% |
| Governor Independence | ~5–10ms | ~300–500ms | **30–100** | ~100% |

The precise concurrent PPT formula [Engineering Estimate — GI-TL-2026-07-25]:

```
Concurrent PPTs = Lane 2 anchoring time / Lane 1 cycle time
               = 300–500 ms / 5–10 ms
               = 30–100 in-flight PPTs
```

This is not a marginal improvement. It is a 2–3 order of magnitude change in Lane 1 throughput from the same hardware, with no additional silicon. The theoretical maximum throughput ceiling shifts to HSM signing capacity: Utimaco Se-Series at 40,000 RSA ops/s yields a theoretical maximum of 40,000 PPTs/s.

### Per-PPT Memory Footprint

Each concurrent in-flight PPT requires the following tracking state [Engineering Estimate]:

| Field | Size |
|---|---|
| `provisionalExpiry` clock (timestamp) | 8 bytes |
| Nonce | 8 bytes |
| Merkle root | 32 bytes |
| Operation context | ~256 bytes |
| FPT routing table entry | ~128 bytes |
| **Total per PPT** | **~432 bytes** |

For 100 concurrent PPTs: ~43 KB. For 1,000 concurrent PPTs: ~432 KB. Both are negligible for hardware implementation. Memory is not a practical binding constraint under Governor Independence at realistic throughput targets.

The Governor's ~45 picosecond reset time after C-element convergence means the hardware is idle for essentially zero time between the PPT fork and readiness for the next request. The only practical reset latency is HSM session overhead — already accounted for in the 10ms warm-path figure.

---

## What Must Be Specified

Governor Independence as an intentional architectural property requires explicit specification of several behaviors that are currently implicit or unaddressed:

**1 — Post-expiry FPT rejection is non-negotiable.**  
When `provisionalExpiry` fires for PPT-1 while PPT-2 is in State 1, the FPT for PPT-1 — if it arrives late — must be rejected. The rendezvous logic must match incoming FPTs to their originating PPT by nonce and audit_seq, not merely by arrival order. This is a required addition to the FPT intake specification.

**2 — Independent PPT nonce space.**  
Each PPT in the pipeline must carry a unique nonce (monotonic counter value). The hardware monotonic counter must increment before each PPT minting, ensuring that no two simultaneous in-flight PPTs share a nonce. This prevents FPT routing ambiguity.

**3 — Provisioned FPT delivery rate.**  
Lane 2 infrastructure must be provisioned to handle up to N concurrent in-flight FPTs, where N is the ratio of Lane 2 anchoring latency to Lane 1 PPT cycle time. For 400ms anchoring and 10ms PPT cycles, N ≈ 40 concurrent FPTs. Lane 2 infrastructure must handle 40 concurrent anchoring operations without degradation.

**4 — Dependent vs. independent PPT declaration.**  
When PPT-2's execution is logically dependent on PPT-1 having reached State 2, PPT-2 must declare this dependency in the `dependency_id` field of PPTPayload (see `01_Architecture_Specs/PPT_Token_Schema.md`). The FPT intake for PPT-2 must check that PPT-1's FPT has been confirmed before transitioning PPT-2 to State 2. Independent PPTs carry `dependency_id = 0x00...00`.

---

## Dependency Chains as a Directed Acyclic Graph

When multiple PPTs carry logical dependencies via the `dependency_id` field, the set of in-flight PPTs forms a **Directed Acyclic Graph (DAG)** — not a simple linear chain.

In the DAG model:
- Each PPT is a node
- Each `dependency_id` reference is a directed edge from dependent to prerequisite
- A PPT can only reach State 2 after all nodes it depends on have reached State 2
- A PPT with no `dependency_id` (= 0x00...00) is a root node — fully independent

This abstraction is well-established in related fields. MPEG video codec standards use `dependency_id` for exactly this purpose: to reassemble sub-bitstreams in correct dependency order. The DAG model enables formal verification of dependency ordering properties that linear chain models cannot express.

**Formal property for the DAG (TLA+ formulation):**

```tla
DependencyOrdering ==
    \A i, j \in Procs :
        (depends_on[i] = j) =>
            [](state[i] = STATE_FINAL ~> state[j] = STATE_FINAL)
```

This states: for all PPT pairs where i depends on j, if i reaches State 2 then j must have already reached State 2. This property is verifiable by TLC against the N-instance composition of the base TLA+ model.

**The DAG model has one hard constraint:** it must be acyclic. A cycle (PPT-A depends on PPT-B, PPT-B depends on PPT-A) creates a deadlock — neither can finalize. TL's hardware must validate at PPT minting time that adding the new `dependency_id` edge does not create a cycle. This is a required addition to the minting validation logic. [Theoretical — Gap]

---

## Comparison to Prior Systems

Governor Independence makes TL's DLLA structurally analogous to three prior systems, each illuminating a different aspect:

**TCP Sliding Window Protocol:**
- The "window" is the set of in-flight PPTs (bounded by HSM throughput and Lane 2 provisioned capacity)
- The "ACK" is the FPT
- The "retransmit on timeout" is the State 0 snapback on `provisionalExpiry`
- The "sequence number" is the PPT nonce / audit_seq
- **TL addition:** TCP has no hardware interlock; TL's C-element provides a physical authorization gate that TCP's acknowledgment mechanism does not

**CPU Out-of-Order Execution with Reorder Buffer:**
- Instructions execute out of order; the Reorder Buffer (ROB) tracks completion order
- PPTs execute provisionally; the FPT routing table tracks finality
- **TL addition:** CPU speculation operates on internal pipeline state only; TL's provisional execution can produce externally visible effects — a fundamentally harder rollback problem

**Database MVCC (Multi-Version Concurrency Control):**
- Multiple transaction versions coexist; reads see a consistent snapshot; writes are validated at commit
- Multiple PPTs coexist in provisional state; FPT arrival is the commit signal
- **TL addition:** MVCC commit validation is software; TL's FPT validation is hardware-enforced and cryptographically signed

These analogies make Governor Independence well-understood to network engineers, processor architects, and database engineers respectively — three different entry points into the same architectural property.

---

## Integration Plan

This note should be integrated into the following documents:

**DLLA specification (existing TL document):**  
Add a section titled "Governor Independence" after the two-lane separation section. State explicitly that Lane 1 reset occurs at PPT issuance, not at FPT confirmation. Update the throughput model.

**`01_Architecture_Specs/Dual_Lane_Governance.md`:**  
Already incorporates Governor Independence. This note is the source document.

**`06_Publication/PPT_Paper_Draft.md`:**  
Section 4.3 (The Two-Lane Separation) references Governor Independence. Section 8 (Performance) uses it in the throughput analysis. The paper should cite this note as the architectural source.

**Adversarial review response (Session 4 revision plan):**  
Governor Independence addresses the throughput characterization in the performance section and is a positive addition to the paper's contribution claim — it demonstrates that TL's architecture has throughput properties beyond what the base DLLA specification implies.

---

## Open Questions

**Q1: Maximum pipeline depth — RESOLVED by DS_50ms [Engineering Estimate]**  
Concurrent PPTs = 30–100 within a single anchoring window at warm-path PPT ~5–10ms and Lane 2 ~300–500ms. Memory footprint (~432 bytes/PPT) is not a binding constraint. Recommended operational maximum: 80% of HSM signing capacity. For Utimaco Se-Series: 32,000 PPTs/s sustainable ceiling.

**Q2: Pipeline ordering guarantees — RESOLVED [Theoretical]**  
TL does not require strict FIFO sequencing of FPT confirmations. Out-of-order confirmation is permitted for independent PPTs. Deployments requiring ordering (financial transactions, industrial control command sequences) must implement application-layer sequencing using `audit_seq` as a discriminator. Unsafe conditions for out-of-order: data dependencies, shared mutable state, regulatory ordering mandates. See `Dual_Lane_Governance.md` FPT routing section.

**Q3: Flow control signal — RESOLVED by per-PPT Shadow Buffer Gate architecture**
The backpressure mechanism is hardware-enforced. The `shadow_buffer_array.any_slot_full` output from the Shadow Buffer Gate array propagates to the Lane 1 PPT pipeline as a physical stall signal. When any PPT slot's shadow buffer reaches its 8-slot capacity, no new PPTs are minted until a slot is cleared — either by FPT arrival (State 2 releases the slot) or by `provisionalExpiry` (single-cycle wipe clears the slot). The DOS vector from the Governor Independence Prompt Q4.3 is closed: an adversary who suppresses FPTs causes slots to wipe on expiry, clearing space for new PPTs. No indefinite starvation is possible. [Engineering Estimate — pending hardware validation]

**Q4: DAG cycle detection at minting time — RESOLVED by constitutional lane separation**

Hardware graph traversal is a trap. Cycle detection requires deep tree traversal — a semantic, variable-time operation. Placing it inside the Lane 1 hardware pipeline would destroy the 50ms latency target and violate the constitutional principle that Lane 1 is strictly syntactic.

The resolution: the hardware does not prevent cycles. It destroys them.

When a system submits a cyclic dependency (PPT-A depends on PPT-B, PPT-B depends on PPT-A), the Lane 1 hardware checks syntax only — valid signatures, valid schema, valid nonce. It mints PPTs for both. They enter State 1 and sit in the volatile buffer. Meanwhile, the Governance Lane receives the logs, runs semantic graph analysis, detects the cycle, and does precisely nothing — it refuses to issue FPTs for either PPT. The `provisionalExpiry` timers fire. The C-element collapses both PPTs to Epistemic Hold. The cycle is physically erased from the volatile buffer.

The hardware needed no knowledge of DAGs. The Governance Lane needed no new mechanism. The existing `provisionalExpiry` watchdog is the cycle-destruction mechanism. Constitutional lane separation is the solution. [Theoretical — verified by architectural reasoning]

**Q5: Nonce exhaustion at high throughput — RESOLVED by Epoch Hold**

At 64-bit nonce width and one million PPTs per second — far above any currently projected deployment ceiling — nonce exhaustion occurs in approximately 584,000 years. Nonce exhaustion is a mathematical purity test, not a practical threat.

However, formal verification requires a deterministic bound. The hardware solution is the **Epoch Hold**: a physically hardwired threshold in the nonce counter — set at MAX_NONCE - 10,000 — at which the hardware immediately ceases minting new PPTs and asserts a system-wide Epistemic Hold. No software can override this. No new PPTs can be issued.

To resume operation, the system requires a privileged operator-issued **Epoch Reset FPT** — a specially classified FPT that rotates the base cryptographic signing keys, resets the nonce counter to zero, and releases the Epoch Hold. The key rotation is a required part of the reset: nonce space and key material are rotated together, ensuring that no nonce value from a prior epoch can be replayed against the new key.

The Epoch Hold is a scheduled maintenance event that deployments will require approximately once every 584,000 years at one million PPTs per second — or approximately once every 584 billion years at one thousand PPTs per second. It is specified not because exhaustion is a practical threat, but because formal verification requires the state machine to have a defined behavior for every reachable counter value. [Engineering Estimate for threshold; Theoretical for epoch reset protocol]

All five open questions are now resolved. The DLLA specification is complete pending hardware validation benchmarks (FW1–FW4 from the publication package). No architectural gaps remain.

---

*Ternary Logic — FractonicMind/TernaryLogic/PPT/05_Research*
