# C-Element Rollback
### Ternary Logic — Dual-Lane Latency Architecture | 01_Architecture_Specs
**Author:** Lev Goukassian | FractonicMind  
**Parent directory:** `PPT/01_Architecture_Specs/`

---

## Overview

This document specifies what happens physically when TL's C-element reverts the system from State 1 (Provisional Execution) back to State 0 (Epistemic Hold). The rollback is not a software event. It is a circuit event — a cascade of electrical state changes that physically closes the execution gate without requiring software permission, coordinator contact, or external signal.

---

## What Triggers the Rollback

Two conditions trigger C-element collapse:

**Condition A — `provisionalExpiry` fires:**  
The hardware watchdog counter reaches its configured bound before the FPT arrives. The watchdog output signal transitions from low to high. This signal is wired to the PPT-validity input of the C-element through an inverter — when the watchdog fires, the PPT-validity line is pulled low.

**Condition B — HSM or pipeline failure during State 1:**  
If a hardware component in the signing pipeline asserts a fault signal after PPT issuance, the fault line is wired to pull the PPT-validity input low, triggering the same collapse sequence.

Both conditions produce identical electrical behavior in the C-element.

---

## The Collapse Sequence

The C-element rollback proceeds in four electrical stages:

### Stage 1 — Input Deassertion (~0 ns to ~1 ns)

The PPT-validity input to the C-element transitions from high (1) to low (0).

The C-element is a consensus gate. Its output is defined by the following truth table:

| Input A (PPT valid) | Input B (HW auth) | Output (State release) |
|---|---|---|
| 1 | 1 | 1 — State 1 active |
| 1 | 0 | 0 — State 0 held |
| 0 | 1 | **0 — State 0 asserted** |
| 0 | 0 | 0 — State 0 held |

When Input A goes low, the pull-down network in the C-element's CMOS topology activates. The output is pulled toward ground regardless of Input B's state.

### Stage 2 — C-Element Output Collapse (~45 ps propagation)

The C-element output transitions from high (1) to low (0) within approximately 45 ps at 28 nm CMOS process. This is the physical moment of State 0 assertion — the execution gate closes at the circuit level.

The output going low simultaneously:
- Deasserts the State 1 enable signal to the execution pipeline
- Asserts the State 0 hold signal to the execution gate
- Triggers the volatile buffer invalidation sequence (see Stage 3)

### Stage 3 — Volatile Buffer Invalidation (~1–5 ns)

The execution pipeline's volatile buffer — holding the in-progress provisional computation — receives the buffer-clear signal derived from the C-element output going low. The buffer invalidation logic (specified in `02_Hardware_Primitives/Volatile_Memory_Clear.v`) sets validity bits to zero for all uncommitted provisional data.

**What buffer invalidation does:**  
Marks all data written during the provisional window as invalid. Subsequent reads from these addresses return an invalid-data signal rather than the uncommitted values.

**What buffer invalidation does not do:**  
It does not automatically reverse externally visible effects — transmitted network packets, engaged actuators, or writes committed to persistent storage outside the volatile buffer. These require application-layer compensating logic triggered by the State 0 snapback event. This is a fundamental boundary of TL's hardware rollback guarantee.

TL's hardware rollback is an **authorization state rollback** — the system returns to State 0 and all uncommitted volatile state is invalidated. It is not an **execution state rollback** — effects that have left the system boundary during the provisional window are not automatically undone by the circuit.

### Stage 4 — Hardware Reset and Lane 1 Re-priming (~5–10 ms)

Following buffer invalidation, Lane 1 hardware enters its reset sequence:
- The `provisionalExpiry` watchdog counter is cleared
- The PPT-validity line is held low pending the next valid PPT
- The Merkle engine pre-computes the next audit branch (warm-path preparation)
- The HSM session remains warm for the next signing request
- The C-element awaits its next valid input pair

Lane 1 is ready to accept the next authorization request. Lane 2 — if still processing its anchoring — continues independently. Lane 2's in-progress anchoring is abandoned; any FPT that arrives after State 0 has been asserted must be rejected.

---

## The Rollback Is Not a Software Event

This distinction is the C-element's defining architectural property.

In a software-enforced authorization system, rollback means: a software process detects a timeout condition, sets a flag, and the execution pipeline checks the flag before proceeding. The execution pipeline can proceed between the timeout and the flag check. The rollback is contingent on the software executing correctly.

In TL's C-element architecture, rollback means: the watchdog output pulls the C-element input low, which collapses the C-element output, which physically deasserts the execution enable signal. There is no software in this path. The execution gate closes because of Kirchhoff's current laws, not because of code.

The execution pipeline cannot proceed after C-element collapse because the enable signal is electrically low. There is no software flag to check, no race condition between detection and enforcement, no window between rollback trigger and rollback effect.

---

## Rollback Timing

| Event | Latency | Classification |
|---|---|---|
| Watchdog fires → Input A goes low | ~1 ns (wire propagation) | [Engineering Estimate] |
| Input A low → C-element output low | ~45 ps | [Demonstrated — CMOS physics] |
| C-element output low → buffer invalidation asserted | ~1–5 ns | [Engineering Estimate] |
| Buffer invalidation complete | ~1–5 ns | [Engineering Estimate] |
| Lane 1 reset and re-priming | ~5–10 ms | [Engineering Estimate] |
| **Total rollback to Lane 1 ready** | **~5–10 ms** | **[Engineering Estimate]** |

The rollback-to-ready time is dominated by HSM re-priming, not by the circuit collapse itself. The circuit collapse completes in under 10 ns. The HSM is already warm; re-priming consists of confirming session state and pre-loading the next Merkle branch.

---

## Failure Modes of the Rollback Mechanism

### `provisionalExpiry` Timer Failure (Critical Gap)

If the hardware watchdog counter fails to fire — crash-stop, omission, or Byzantine fault — the system may remain in State 1 indefinitely without FPT arrival. This is the most severe failure mode of the rollback mechanism.

**Required specification (MT hardware layer):**  
The `provisionalExpiry` timer must be implemented with a fail-closed default: if the timer's operational status cannot be confirmed, State 0 must be asserted. A secondary independent timer (a watchdog-of-the-watchdog) should monitor the primary watchdog's heartbeat and assert State 0 if the heartbeat is absent.

**Current status:** [Gap] — not yet specified in TL's MT hardware layer. Identified as engineering task prior to ASIL-D certification.

### C-Element Byzantine Fault (Critical Gap)

If the C-element produces a high output when one or both inputs are low — due to radiation-induced SEU in SRAM-based FPGA implementations, laser fault injection, or manufacturing defect — the execution gate opens without authorization.

**Required specification:**  
- SRAM-based FPGA implementations must implement configuration scrubbing or Triple Modular Redundancy (TMR)
- Flash-based FPGA (Microchip PolarFire) or ASIC implementations are mandatory for ASIL-D and IEC 62304 Class C deployments
- Dual-rail encoding (specified in TL's MT layer) provides Byzantine fault detection at the output level — a detected fault must assert State 0 immediately

**Current status:** [Partially specified] — dual-rail encoding is in MT spec; scrubbing and TMR requirements are not yet normative.

### Power Loss During Rollback

If power fails during Stage 3 (buffer invalidation), the invalidation may be incomplete. On power restoration:
- The C-element loses state; output defaults low (State 0) by CMOS pull-down
- The buffer's validity bits are in an undefined state
- The system must perform a full buffer audit on restart before accepting new authorization requests

**Required specification (MT hardware layer):**  
Power-on reset sequence must include buffer-validity-bit zeroing before Lane 1 is declared ready. This should be a hardware-enforced startup check, not a software initialization routine.

---

## Rollback Scope Boundary

To be explicit about what TL's hardware rollback covers and what it does not:

| Scope | Covered by hardware rollback | Notes |
|---|---|---|
| Authorization state (State 1 → State 0) | **Yes** | C-element collapse |
| Volatile buffer contents | **Yes** | Buffer invalidation signal |
| In-flight Lane 1 pipeline state | **Yes** | Pipeline flush on enable deassertion |
| Writes to persistent storage (database, filesystem) | **No** | Requires transactional storage layer |
| Transmitted network packets | **No** | Requires application compensating logic |
| Engaged actuators (physical outputs) | **No** | Requires domain-specific reversal command |
| Lane 2 in-progress FPT construction | **No** | Lane 2 runs independently; post-expiry FPT must be rejected |

Applications operating in TL's provisional execution window must be designed with the understanding that hardware rollback covers volatile state only. Persistent and externally visible effects require application-layer compensation.

---

## Related Files

| File | Relationship |
|---|---|
| `PPT_Lifecycle.md` | Full lifecycle context for rollback Phase 4 |
| `02_Hardware_Primitives/C_Element_Interlock.v` | RTL implementation of the C-element |
| `02_Hardware_Primitives/Countdown_Timer_Clock.v` | Hardware watchdog that triggers rollback |
| `02_Hardware_Primitives/Volatile_Memory_Clear.v` | Buffer invalidation logic |
| `04_Formal_Verification/PPT_State_Transitions.tla` | Formal model of the rollback transition |
| `04_Formal_Verification/Rollback_Safety_Proofs.md` | Mathematical proof that rollback is unconditional |

---

*Ternary Logic — FractonicMind/TernaryLogic/PPT/01_Architecture_Specs*
