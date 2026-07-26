# PPT Lifecycle
### Ternary Logic — Dual-Lane Latency Architecture | 01_Architecture_Specs
**Author:** Lev Goukassian | FractonicMind  
**Parent directory:** `PPT/01_Architecture_Specs/`

---

## Overview

The PPT lifecycle is the complete sequence of events from authorization request to final confirmed execution — or to hardware snapback if finality does not arrive in time. It spans two lanes, three states, and two tokens. Every transition in the lifecycle is either hardware-enforced or cryptographically-gated. No transition is software-policy alone.

---

## The Five Phases

### Phase 1 — Request, Reversibility Classification, and State 0 Hold

The system begins in **State 0 (Epistemic Hold)**. No execution is permitted. The C-element's output is held low by its pull-down network. The execution gate is physically closed.

Before any authorization request enters the pipeline, every action the proposal intends to take must be classified against the **Reversibility Boundary** — TL's constitutional primitive that divides execution into two classes. This classification is **fixed at hardware deployment**. It is expressed in silicon topology, not software labels. It cannot be changed at runtime. It cannot be overridden by software.

**Class R — Reversible (Provisional Computation):**
ALU operations, volatile register writes, internal state changes, mathematical calculations, in-memory transformations, queue preparation, shadow buffer population. These connect directly to the ALU and volatile memory. The PPT authorizes their execution during State 1. The C-element destroys them entirely on `provisionalExpiry` — the volatile buffer is grounded, the pipeline is flushed, and no trace remains.

**Class I — Irreversible (External Actuation):**
Network transmissions (NIC), financial wire transfers (outbound bus), physical actuator commands, external API calls, database commits to external systems. These are physically wired through the Shadow Buffer Gate (`Shadow_Buffer_Gate.v`). The PPT authorizes their **computation and staging** during State 1 — the ALU may calculate the payload and place it in the shadow buffer. The physical port remains **CLOSED**. Only the State 2 output rail of the C-element — asserted when a valid FPT arrives — opens the Shadow Buffer Gate and releases Class I actions to the world.

**The constitutional consequence:** An adversary who suppresses FPT delivery to force `provisionalExpiry` gains nothing. Class R actions are destroyed by the volatile buffer clear. Class I actions are discarded from the shadow buffer. The physical port was never opened. No action entered the world. The adversary has caused a localized waste of electricity.

An authorization request arrives carrying:
- Operation identifier
- Session context
- Monotonic counter (nonce — hardware-incremented, non-reusable)
- Requesting principal identity
- Action manifest — the declared list of Class R and Class I actions the proposal will take, verified against the physical topology at admission

The request enters the Lane 1 hardware pipeline. The system remains in State 0 until the pipeline completes. There is no provisional execution during pipeline processing. State 0 is the default and the fallback.

---

### Phase 2 — PPT Minting (The Hardware Pipeline)

The four-stage cryptographic pipeline executes entirely within Lane 1:

**Stage 1 — SHA-256 Hash** (~1 μs, warm path)  
The hardware SHA-256 accelerator computes a hash over the operation identifier, session context, and monotonic counter. This produces the cryptographic commitment to the specific authorized operation. The nonce ensures that no two PPTs for the same operation are identical — replay prevention at the hardware level.

**Stage 2 — Merkle Pre-computation** (~16 μs, warm path)  
Sixteen parallel SHA-256 cores construct a Merkle tree over the current audit leaf set, producing an authenticated root that anchors the PPT in the immutable audit log. The Merkle root binds the PPT to the full audit context of the authorization request — not just the operation, but the complete evidence trail that justifies it.

**Stage 3 — HSM Signing** (~5–10 ms, warm path)  
A FIPS 140-3 Level 3 certified Hardware Security Module signs the SHA-256 hash and Merkle root using ECDSA P-256 (or a post-quantum successor per FIPS 204/205). The HSM's private key never leaves the HSM boundary. The output is the PPT's cryptographic authorization token — unforgeable without HSM access.

**Stage 4 — C-Element Convergence** (~45 ps)  
The HSM signing output drives one input of the Muller C-element. The hardware authorization signal drives the second input. When both inputs are electrically high, the C-element output goes high — releasing State 0 and permitting transition to State 1. This is the physical gate. It is not configurable and has no software override path.

**Total pipeline latency:**

| Path | Mean | p99 | Classification |
|---|---|---|---|
| Warm path (operational steady state) | ~5–10 ms | ~17 ms | [Engineering Estimate] |
| Cold path (first issuance, session startup) | ~20–40 ms | ~60 ms | [Engineering Estimate] |

The cold-path p99 of approximately 60 ms exceeds TL's 50 ms specification. Mandatory HSM session pre-warming at system startup mitigates this. The 50 ms SLA applies to the warm-path operational steady state, not to first-issuance startup transients.

---

### Phase 3 — The 50-Millisecond Fork (Governor Independence)

At PPT issuance, the DLLA executes a simultaneous fork:

**Lane 1 — Execution thread released:**
The system transitions to **State 1 (Provisional Execution)**. The execution thread proceeds under the Reversibility Boundary:
- **Class R actions** execute immediately against the ALU and volatile registers
- **Class I actions** are computed, their payloads staged in the Shadow Buffer Gate, physical port CLOSED

The `provisionalExpiry` hardware watchdog counter begins counting from zero. Lane 1 hardware resets — the C-element is primed for the next authorization request. Lane 1 does not wait for Lane 2 to complete.

**Lane 2 — Logging thread dispatched:**
The logging payload (PPT token, Merkle root, operation context, audit leaf set) is dispatched to the external anchoring infrastructure. Lane 2 operates at infrastructure speed — 300 to 500 ms, operator-configured. Lane 2 runs as an independent stream. Its completion is not required for Lane 1 to accept the next PPT request.

This is TL's **Governor Independence** principle: the moment the fork occurs at the 50-millisecond marker, Lane 1 and Lane 2 are autonomous. Lane 1 throughput is no longer coupled to Lane 2 anchoring latency. Multiple PPT cycles can complete within a single Lane 2 anchoring window.

```
PPT Issued at T=0
        │
        ├──── Lane 1 ────────────────────────────────────────────────►
        │     T=0:   State 1 active.
        │            Class R → executes in volatile registers
        │            Class I → staged in shadow buffer, port CLOSED
        │     T=0:   C-element resets. Next PPT accepted.
        │     T=50ms: provisionalExpiry countdown active.
        │
        └──── Lane 2 ────────────────────────────────────────────────►
              T=0:   Logging payload dispatched.
              T=300–500ms: FPT issued on anchoring completion.
              T=300–500ms: FPT delivered to Lane 1 rendezvous point.
```

---

### Phase 4 — The Rendezvous Window

During the provisional window, the system holds **State 1**. Two outcomes are possible:

**Outcome A — FPT arrives before `provisionalExpiry`:**
The FPT is verified (signature check, Merkle root cross-validation, nonce confirmation). On successful verification, the C-element achieves State 2 consensus. The **State 2 output rail goes high**. This rail is hardwired to the Shadow Buffer Gate's enable pin. The physical port opens. All staged Class I payloads are released to the world in sequence. The system has reached **State 2 (Final Confirmed Execution)**. Execution is now irreversible. The `provisionalExpiry` watchdog is cleared.

**Outcome B — `provisionalExpiry` fires before FPT arrives:**
The hardware watchdog counter reaches its configured bound. The watchdog output signal goes high, pulling the PPT-valid line low, which collapses the C-element output, which asserts State 0. The State 2 rail never went high. The Shadow Buffer Gate's enable pin was never asserted. The physical port was never opened. Class I payloads in the shadow buffer are cleared and discarded. The system returns to **State 0 (Epistemic Hold)** unconditionally. No action entered the world during the provisional window except Class R computation which is now destroyed.

Any Lane 2 FPT that arrives after `provisionalExpiry` has fired must be rejected. A post-expiry FPT does not re-authorize execution. A fresh authorization cycle is required.

---

### Phase 5 — Terminal States

| Terminal State | How reached | Reversible |
|---|---|---|
| **State 2** | Valid FPT before `provisionalExpiry` | No — execution is final |
| **State 0 (snapback)** | `provisionalExpiry` fires | Yes — fresh PPT cycle may begin |
| **State 0 (no PPT issued)** | Pipeline failure or request rejection | Yes — retry permitted |

State 2 is the only irreversible terminal state. Every path that does not reach State 2 returns to State 0 — the system's safe default.

---

## Lifecycle State Diagram

```
                    ┌─────────────────────────────────┐
                    │                                 │
                    ▼                                 │ provisionalExpiry fires
              ┌──────────┐                            │ (hardware snapback)
    ─────────►│ STATE 0  │                            │
    (default) │ Epistemic│                            │
              │   Hold   │                            │
              └────┬─────┘                            │
                   │                                  │
                   │ Valid PPT issued                 │
                   │ (C-element releases)             │
                   ▼                                  │
              ┌──────────┐                            │
              │ STATE 1  ├────────────────────────────┘
              │Provisional│
              │Execution  │
              └────┬──────┘
                   │
                   │ Valid FPT arrives
                   │ before provisionalExpiry
                   ▼
              ┌──────────┐
              │ STATE 2  │
              │  Final   │
              │Confirmed │ (irreversible)
              └──────────┘
```

---

## Prohibited Transitions

The following transitions are physically impossible in TL's C-element implementation:

| Prohibited Transition | Why impossible |
|---|---|
| State 0 → State 1 without valid PPT | C-element output cannot go high without HSM signing input |
| State 1 → State 2 without valid FPT | FPT verification gate prevents State 2 assertion |
| State 0 → State 2 directly | No direct path exists in the state machine |
| State 1 persisting after `provisionalExpiry` | Hardware watchdog collapse is unconditional |

These are not enforced by software checks. They are properties of the circuit topology and verified formally in `04_Formal_Verification/PPT_State_Transitions.tla`.

---

## Lifecycle Constraints for Specific Domains

TL's lifecycle has domain-specific operational modes:

**Financial execution and AI governance (standard mode):**  
Provisional execution permitted. PPT releases State 0; FPT confirms State 2. The provisional window is the operational norm.

**Medical devices and autonomous vehicle actuation (strict mode):**  
No provisional actuation permitted. Both PPT and FPT must be verified before the actuator command is released. The system holds in State 0 until FPT arrives, then transitions directly to State 2. This eliminates the provisional window for actuation-class operations.

The mode is operator-configured at deployment. It is not a runtime switch.

---

## Failure Behavior Summary

| Failure | System response | Safe? |
|---|---|---|
| SHA-256 accelerator crash-stop | Pipeline stalls. `provisionalExpiry` fires. State 0 maintained. | Yes |
| Merkle engine crash-stop | Same as above. | Yes |
| HSM crash-stop | PPT not issued. System remains in State 0. | Yes |
| C-element crash-stop (output stuck low) | Execution permanently blocked. State 0 maintained. | Yes |
| `provisionalExpiry` crash-stop (timer fails) | **Critical gap** — timer failure must assert State 0 by default. Fail-closed. | Specified as requirement |
| FPT delivery failure | `provisionalExpiry` fires. State 0 snapback. | Yes |
| Power loss during State 1 | C-element loses state. Output defaults low. State 0 on restart. | Yes |

All failure modes resolve to State 0 except `provisionalExpiry` timer failure, which requires explicit fail-closed specification in the MT hardware layer. See `01_Architecture_Specs/C_Element_Rollback.md` for the circuit-level treatment.

---

## Related Files

| File | Relationship |
|---|---|
| `PPT_Token_Schema.md` | Exact data structure produced by Phase 2 |
| `C_Element_Rollback.md` | Circuit-level detail of Phase 4 Outcome B |
| `Dual_Lane_Governance.md` | Phase 3 Governor Independence — full architectural treatment |
| `02_Hardware_Primitives/C_Element_Interlock.v` | RTL implementation of the Phase 2 physical gate |
| `04_Formal_Verification/PPT_State_Transitions.tla` | Formal proof of prohibited transitions |

---

*Ternary Logic — FractonicMind/TernaryLogic/PPT/01_Architecture_Specs*
