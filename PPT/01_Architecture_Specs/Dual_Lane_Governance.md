# Dual-Lane Governance
### Ternary Logic — Dual-Lane Latency Architecture | 01_Architecture_Specs
**Author:** Lev Goukassian | FractonicMind  
**Parent directory:** `PPT/01_Architecture_Specs/`

---

## Overview

TL's Dual-Lane Latency Architecture separates two operations that every prior authorization system conflates: *authorization* and *finality*. This document specifies how the two lanes are structured, how they interact at the 50-millisecond fork, and why their independence — Governor Independence — is an architectural property rather than an implementation detail.

---

## The Core Separation

> **Authorization latency is hardware-owned.**  
> **Finality latency is infrastructure-owned.**

These are not descriptions of two phases in the same process. They are descriptions of two independent processes with different owners, different latency envelopes, and different failure modes — operating in parallel after the fork.

Most authorization systems treat authorization and finality as a sequential pipeline: authorize, then confirm, then permit execution. The system waits for each step before proceeding to the next. Finality latency adds directly to execution latency.

TL's position is that this is wrong for high-throughput, high-consequence systems. Authorization can be resolved deterministically in hardware in under 50 milliseconds. Finality — anchoring to an external ledger, regulatory clearinghouse, or consensus infrastructure — takes 300 to 500 milliseconds, is network-dependent, and is not TL's specification. Coupling these two latencies forces hardware to run at infrastructure speed.

The DLLA decouples them.

---

## Lane 1 — The Inference Lane

**Owner:** MT hardware layer  
**Latency:** Under 50 ms (warm path, operational steady state)  
**Content:** SHA-256 hash → Merkle pre-computation → HSM signing → C-element convergence → PPT issuance  
**Lifecycle:** State 0 → State 1 → (reset at fork)  
**Governed by:** C-element physical consensus gate  

Lane 1 is the hardware domain. Everything in Lane 1 operates without external network dependency. The SHA-256 accelerator, Merkle engine, HSM, and C-element are all physically local to the execution system. Lane 1's latency is bounded by the hardware pipeline's performance characteristics — not by network RTT, consensus rounds, or infrastructure availability.

**Governor Independence:**  
At the 50-millisecond fork — the moment the PPT is issued — Lane 1 resets immediately. The C-element is re-primed. The hardware pipeline is ready for the next authorization request. Lane 1 does not wait for Lane 2 to complete its anchoring cycle. Lane 1's throughput is governed purely by HSM signing capacity and C-element reset speed.

This is the key throughput consequence: multiple Lane 1 PPT cycles can complete within a single Lane 2 anchoring window. If the warm-path PPT cycle is approximately 10 ms and Lane 2 anchoring is 300–500 ms, Lane 1 can process 6–10 authorization cycles per anchoring window. Same hardware. Same HSM. Throughput multiplied without architectural change.

---

## Lane 2 — The Governance Lane

**Owner:** Deployment infrastructure (operator-configured)  
**Latency:** 300–500 ms (illustrative; operator-configured, not TL's specification)  
**Content:** Logging payload → external anchoring infrastructure → FPT issuance → FPT delivery  
**Lifecycle:** Dispatch at fork → anchor → FPT → rendezvous  
**Governed by:** Operator infrastructure  

Lane 2 is the infrastructure domain. Its latency is explicitly not TL's specification — TL specifies that Lane 2 must exist and that the FPT must be cryptographically verifiable, but the mechanism and latency of Lane 2 are operator choices.

Lane 2 options include:
- Blockchain anchor (public or permissioned ledger)
- Regulatory clearinghouse submission
- Internal audit ledger with cryptographic sealing
- Multi-party consensus infrastructure
- Write-once hardware medium (OTP, WORM) — no network anchoring required

The choice of Lane 2 infrastructure determines the FPT's latency, its decentralization properties, and its regulatory alignment. TL does not prescribe which is correct — it prescribes only that the FPT must be cryptographically signed and verifiable before it can transition the system to State 2.

---

## The Fork — Where the Lanes Separate

At PPT issuance (T=0), two things happen simultaneously:

```
T = 0 ms: PPT issued
          │
          ├──── Lane 1 fork ───────────────────────────────────────►
          │     Execution thread released → State 1
          │     Lane 1 hardware resets → next PPT accepted
          │     provisionalExpiry watchdog begins counting
          │
          └──── Lane 2 fork ───────────────────────────────────────►
                Logging payload dispatched to external infrastructure
                Anchoring proceeds at infrastructure speed
                FPT issued on anchoring completion
                FPT delivered to Lane 1 rendezvous point
```

The fork is not a handoff — it is a split. Lane 1 and Lane 2 run concurrently from T=0. Neither waits for the other after the fork.

---

## The Rendezvous

The FPT is Lane 2's output. It is delivered to Lane 1's rendezvous point — a hardware-verified FPT intake that accepts the token, verifies its signature and Merkle root, confirms the nonce, and if valid, transitions the system from State 1 to State 2.

The rendezvous has a hard deadline: `provisionalExpiry`. If the FPT arrives before the deadline, State 2 is reached. If it does not, the watchdog fires, the C-element collapses, and State 0 is asserted. The FPT that arrives after the deadline must be rejected.

The rendezvous point is Lane 1 hardware. FPT verification is not software-mediated — the cryptographic check runs on the same hardware pipeline that produced the PPT.

---

## Governor Independence — The Architectural Principle

Governor Independence is TL's name for the property that Lane 1's operational cadence is decoupled from Lane 2's completion.

Before Governor Independence is explicit in the specification, a naive reading of the DLLA suggests that Lane 1 waits for Lane 2 before accepting the next request — a coupled sequential model. Governor Independence clarifies that this is not TL's architecture.

The Governor (C-element) resets at the fork. It does not wait for Lane 2. It does not track Lane 2's progress. It does not receive signals from Lane 2 except the FPT delivery at the rendezvous point. Lane 2 is invisible to Lane 1 except at the rendezvous.

**Consequences of Governor Independence:**

| Property | Without Governor Independence | With Governor Independence |
|---|---|---|
| Lane 1 throughput ceiling | Coupled to Lane 2 latency (~300–500 ms/cycle) | Coupled to HSM signing rate (~5–10 ms/cycle) |
| Lane 1 idle time | ~97% (waiting for Lane 2) | Near zero |
| PPT cycles per Lane 2 window | 1 | 6–10 |
| Hardware utilization | Low | High |
| Lane 2 failure impact on Lane 1 | Blocks Lane 1 | Does not block Lane 1 — `provisionalExpiry` handles resolution |

---

## Multi-PPT Pipeline Behavior

With Governor Independence, multiple PPTs can be in-flight simultaneously — each in its own provisional window, each with its own `provisionalExpiry` clock, each awaiting its own FPT.

This introduces the **cascading provisional chain** consideration: if PPT-2 is issued while PPT-1's FPT is still in flight, and FPT-1 subsequently fails to arrive, does PPT-2's authorization remain valid?

TL's answer depends on whether PPT-2's execution carries a logical dependency on PPT-1's finality:

**Independent PPTs (no logical dependency):**  
PPT-1's failure to finalize does not affect PPT-2. Each PPT is an independent authorization for an independent operation. PPT-2 proceeds to State 2 on its own FPT regardless of PPT-1's outcome.

**Dependent PPTs (logical dependency):**  
If PPT-2's execution is logically contingent on PPT-1 having reached State 2, then PPT-1's failure triggers a cascade. The application layer must implement dependency tracking — TL's hardware provides the `provisionalExpiry` event as the trigger, but the cascade propagation is an application responsibility.

**Current specification status:** Cascade-revocation protocol for dependent PPT chains is [Gap] — identified as engineering task FW5 in the publication package. Independent PPT pipelines are fully specified.

---

## Lane 2 Infrastructure Requirements

TL specifies the following normative requirements for Lane 2 infrastructure, regardless of the anchoring mechanism chosen:

**Security requirements:**
- FPT must be cryptographically signed by an infrastructure key distinct from the Lane 1 HSM signing key
- FPT delivery channel must use mutual authentication (TLS 1.3 minimum)
- FPT delivery channel must be integrity-protected
- Post-`provisionalExpiry` FPTs must be rejected at the Lane 1 rendezvous point

**Availability requirements:**
- Lane 2 unavailability does not block Lane 1 — it triggers `provisionalExpiry` on active provisional windows
- Lane 2 infrastructure must be provisioned for the expected FPT delivery rate, accounting for multiple concurrent in-flight PPTs under Governor Independence
- Lane 2 SLA must be configured such that FPT delivery latency is reliably within `provisionalExpiry` bounds

**Audit requirements:**
- Lane 2 must produce an immutable, tamper-evident record of all FPT issuances
- The Merkle root in each PPT must be cross-validated by the Lane 2 infrastructure at FPT issuance
- FPT issuance records must be retainable for the regulatory retention period of the deployment domain

---

## Domain-Specific Lane 2 Configurations

| Domain | Lane 2 Mechanism | FPT Latency Target | Notes |
|---|---|---|---|
| Financial execution | Regulatory clearinghouse or permissioned ledger | 300–500 ms | Compatible with ISO 20022, SWIFT |
| Medical devices (strict mode) | Internal cryptographic ledger | < actuation window | FPT required before actuation |
| AI governance | Human reviewer or AI oversight system | Operator-configured | FPT = human-in-the-loop confirmation |
| Industrial control | Internal audit ledger | < control loop period | SCADA zone boundary integration |
| High-frequency trading | On-premises permissioned ledger | < 100 ms | Pre-trade authorization context |

---

## FPT Routing Under Governor Independence

With multiple PPTs in-flight simultaneously, the Lane 1 rendezvous point must unambiguously match each arriving FPT to its originating provisional window.

### Routing Key

The routing key is constructed as:

```
routing_key = SHA-256(issuer_id || nonce || audit_seq)
```

These three fields from the PPT token schema (see `PPT_Token_Schema.md`) are sufficient to guarantee unambiguous matching:
- `issuer_id` — identifies the Lane 1 hardware instance
- `nonce` — 64-bit hardware monotonic counter, unique per PPT per issuer
- `audit_seq` — sequential audit counter, eliminates any nonce collision across reset boundaries

### Lane 1 Routing Table

Each in-flight PPT occupies one entry in a hardware routing table:

| Field | Size | Description |
|---|---|---|
| routing_key | 256 bits | SHA-256(issuer_id \|\| nonce \|\| audit_seq) |
| ppt_timestamp | 64 bits | Time of PPT issuance |
| state | 2 bits | PENDING / FINALIZED / EXPIRED |
| operation_context | 256 bits | Pointer to operation state |

**Memory footprint:** ~84 bytes per in-flight PPT. For 100 concurrent PPTs: ~8.4 KB — negligible for hardware implementation. [Engineering Estimate]

### Routing Rules

**Out-of-order FPT arrival:** The routing table accepts FPTs in any order. Each FPT is matched by routing key; if the entry exists and state is PENDING, the transition to State 2 proceeds. FPT-2 may be confirmed before FPT-1 when the two are independent operations.

**Duplicate FPT delivery:** If the same routing key arrives twice (network retry), the second FPT is rejected — the entry state is already FINALIZED.

**Post-expiry FPT rejection:** If a FPT arrives after `provisionalExpiry` has fired for that routing key, the entry state is EXPIRED and the FPT is rejected unconditionally. It does not re-authorize execution.

### Sequencing Guarantee

TL does not require strict FIFO sequencing of FPT confirmations. Out-of-order confirmation is permitted for independent operations. Deployments where ordering matters (financial transactions, industrial control command sequences) must implement application-layer sequencing using the `audit_seq` field as a sequence discriminator.

**Unsafe conditions for out-of-order confirmation:**
- Operations with data dependencies (PPT-2 depends on PPT-1's result)
- Operations sharing mutable state (double-spend scenarios)
- Regulatory requirements mandating strict ordering (some financial message standards)

[Engineering Estimate] for routing table design; [Theoretical] for ordering semantics.

### Cascade-Revocation for Dependency Chains

When PPT-3 depends on PPT-2 which depends on PPT-1, and PPT-1's `provisionalExpiry` fires:

1. **Detection:** Watchdog fires for PPT-1; routing table entry transitions to EXPIRED
2. **Propagation:** Hardware generates `DEPENDENCY_FAILURE` signal for all routing entries with `depends_on` = PPT-1's routing key
3. **Revocation:** PPT-2 and PPT-3 are immediately rolled back to State 0, independent of their individual expiry timers
4. **Audit:** All rolled-back operations are logged with reason `DEPENDENCY_CHAIN_BREAK`

Propagation is hardware-level; revocation completes within one clock cycle of expiry detection. [Theoretical — Gap: not yet specified in MT hardware layer]

---

## Related Files

| File | Relationship |
|---|---|
| `PPT_Lifecycle.md` | Full lifecycle — Phase 3 is the fork described here |
| `C_Element_Rollback.md` | What happens when Lane 2 fails to deliver FPT in time |
| `PPT_Token_Schema.md` | The logging payload dispatched to Lane 2 at the fork; routing key fields defined here |
| `05_Research/Governor_Independence_Note.md` | Extended architectural treatment of the 50ms autonomy principle |
| `PPT_Governor_Independence_Research.md` | Governor Independence research — routing key and memory footprint analysis |
| `05_Research/Session-2_Deep_Research.md` | Q3 architectural soundness analysis; Q8 domain integration |

---

*Ternary Logic — FractonicMind/TernaryLogic/PPT/01_Architecture_Specs*
