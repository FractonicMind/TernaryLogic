# DLLA Specification Addendum: The Provisional Permission Token as the Constitutional Latency Specification

## **Architectural Reframing: Own the Numbers You Can Prove**

**Architect:** Lev Goukassian
**ORCID:** [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243)
**Repository:** FractonicMind/TernaryLogic
**Parent Specification:** [`Hardware_Enforceable_Execution_Model_Specification.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Dual_Latency_Architecture/Hardware_Enforceable_Execution_Model_Specification.md)
**Addendum Status:** Constitutional -- supersedes Section 2.2 latency claims in the parent specification
**License:** CC BY 4.0

---

## Preamble: The Problem With 300-500ms as a Specification

The parent specification states: *"The Governance Lane operates at 300-500ms for Merkle-batched cryptographic anchoring."*

This number is wrong as a specification. It is correct as a description of current external infrastructure. The distinction matters enormously.

The 300-500ms figure includes:
- SHA-256 hashing: ~1 microsecond -- **we own this**
- Merkle tree construction: ~16 microseconds at 1GHz -- **we own this**
- HSM signing: ~5-10 milliseconds -- **we own this**
- Network transmission to anchoring service: variable -- **we do not own this**
- Blockchain consensus wait: variable -- **we do not own this**
- Anchor receipt confirmation: variable -- **we do not own this**

The 300-500ms is dominated by the three items we do not own. If a new blockchain technology achieves nanosecond consensus tomorrow, should we publish a new specification number? If a network congestion event extends anchoring to 5 seconds, does our hardware fail? Of course not. The hardware is independent of the external infrastructure.

**A specification number that depends on third parties is not a specification. It is a forecast. Forecasts go stale. Specifications do not.**

This addendum corrects the framing. It does not change the architecture. It clarifies what the architecture actually guarantees versus what depends on operator infrastructure choices.

---

## The Correct Specification Boundary

### What the DLLA Hardware Guarantees

**The Provisional Permission Token (PPT) is issued within the PPT window -- entirely determined by hardware we control.**

PPT window components:

| Operation | Time | Owner |
|---|---|---|
| SHA-256 hash of operation state | ~1 μs | DLLA hardware |
| Merkle pre-computation (256 leaves) | ~16 μs at 1GHz | DLLA hardware |
| HSM signing of Merkle root | ~5-10 ms | DLLA hardware (HSM) |
| C-element convergence detection | ~1 ns | DLLA hardware |
| **Total PPT window** | **< 50ms** | **DLLA hardware -- owned specification** |

This is the number we own. It is determined entirely by physics and circuit design -- not by network topology, blockchain consensus protocol, or third-party infrastructure choices. It will not change unless the hardware design changes. If tomorrow's quantum computing achieves nanosecond SHA-256, our PPT window shrinks accordingly -- but that is our improvement, not an external dependency.

**The headline specification: Hardware-enforced execution authorization in under 50ms.**

This is defensible. This is owned. This is constitutionally sound.

### What the Operator Chooses

**The Final Permission Token (FPT) completion time is an integration parameter -- determined by the operator's chosen anchoring infrastructure.**

FPT integration parameter examples:

| Anchoring Infrastructure | Typical FPT Time | Notes |
|---|---|---|
| Permissioned blockchain (sub-second blocks) | 300-500ms | Current typical deployment |
| Public blockchain (6 confirmations) | 60-90 minutes | Maximum security |
| Layer 2 optimistic rollup | ~7 days (challenge period) | Fraud-proof finality |
| HSM-only local ledger | ~50ms | No public anchoring |
| Future quantum-anchored infrastructure | Potentially nanoseconds | Operator choice |

The DLLA hardware makes no claims about FPT completion time. The operator declares their anchoring infrastructure in the `deploymentTier` configuration. The DLLA enforces that a valid FPT must arrive before `provisionalExpiry` -- but what the FPT is and how quickly it arrives is the operator's specification, not ours.

---

## The Two-Token Constitutional Model

### Provisional Permission Token (PPT)

**Issued at:** Under 50ms from operation submission
**Issued by:** DLLA hardware (HSM)
**Authorizes:** Provisional execution -- the operation is committed but publicly unanchored
**Constitutional property:** Hardware-enforced by C-element convergence at the moment of PPT issuance
**Expiry:** Configurable `provisionalExpiry` field (default: 500ms from issuance)
**Unwind mechanism:** If FPT does not arrive before `provisionalExpiry`, C-element hardware automatically reverts the provisional commit -- no software intervention required, no human decision required

The PPT satisfies the Muller C-element. It releases the Sacred Zero. It authorizes execution. All of this happens in under 50ms on hardware we control. The external blockchain has nothing to do with it.

### Final Permission Token (FPT)

**Issued at:** Operator-defined -- integration parameter, not hardware specification
**Issued by:** External anchoring infrastructure chosen by operator
**Supersedes:** The provisional commit -- execution is now fully and publicly anchored
**Constitutional property:** When FPT arrives, `provisionalExpiry` unwind is disarmed -- the commit becomes irrevocable
**Latency claim:** None. The DLLA makes no FPT latency specification. Operator declares their infrastructure.

### The Unwind Mechanism

The automatic unwind on `provisionalExpiry` is hardware-enforced:

```
If FPT arrives before provisionalExpiry:
    Provisional commit becomes irrevocable
    External anchor provides public verifiability
    Unwind mechanism disarmed

If FPT does not arrive before provisionalExpiry:
    C-element triggers automatic state revert
    Operation returns to Sacred Zero
    System logs PROVISIONAL_EXPIRY_REVERT event on-chain
    Operator notified -- anchoring infrastructure may need attention
```

The unwind is not a software timeout. It is a hardware counter in the C-element circuit that asserts a revert signal when elapsed time exceeds `provisionalExpiry`. No software can prevent it. No human can override it without physically modifying the circuit.

---

## Why This Framing Is Architecturally Correct

### 1. The C-Element Does Not Care About the Blockchain

The Muller C-element requires `FastDone AND AuditDone` to assert `Converged`. The PPT satisfies `AuditDone`. The C-element fires. The blockchain has not been consulted. The blockchain will not be consulted. The Sacred Zero releases on our schedule, not the blockchain's schedule.

The critics who identified the 300-500ms as a bottleneck were correct -- but they were identifying a self-inflicted bottleneck created by treating FPT as required for C-element convergence. The PPT architecture removes this bottleneck entirely. The C-element now operates at 50ms. The blockchain operates in the background.

### 2. The Hold Flood Attack Becomes Asymmetric

In `DLLA_ENGINEERING_GAPS_v1.md`, Gap 2 addresses the hold flood attack: an adversary floods the system to trigger buffer stalls and measures external publication delays to map internal buffer capacity.

With the PPT architecture, the adversary's measurement surface changes fundamentally:

- **Internal PPT issuance:** happens in under 50ms, on our hardware, with cryptographic jitter applied
- **External FPT publication:** happens on operator-chosen infrastructure, with dummy padding and cryptographic batch release jitter applied (Gap 2 fix)

The adversary now sees only obfuscated, jittered, dummy-padded external publication events. The internal hardware operates at 50ms regardless of what the adversary sees externally. The attack surface is dramatically reduced.

### 3. The Consumer Application Numbers Are Correct

`DLLA_CONSUMER_APPLICATIONS.md` specifies 10-50ms PPT latency for consumer devices. This is correct and owned. The consumer CEU has:

- Faster HSM (mobile-optimized): ~2-5ms signing
- Smaller Merkle tree (device-local operations): ~1-5μs construction
- Same C-element physics: ~1ns convergence

Consumer PPT window: **10-20ms. Owned. Constitutional.**

The consumer device does not need to wait for any external infrastructure to authorize an action. The PPT is issued locally. The FPT happens asynchronously in the background for audit purposes.

---

## Errata to the Parent Specification

The following statements in `Hardware_Enforceable_Execution_Model_Specification.md` are superseded by this addendum:

| Location | Original Statement | Superseded By |
|---|---|---|
| Abstract (line 25) | "asynchronous Governance Lane (300-500ms) for Merkle-batched cryptographic anchoring" | "asynchronous Governance Lane with PPT issuance under 50ms (hardware-owned) and FPT completion operator-defined (integration parameter)" |
| Section 2.2 heading | "Governance Lane (300-500ms)" | "Governance Lane: PPT under 50ms / FPT operator-defined" |
| Line 533 | "The 300-500ms window accommodates batch formation..." | This describes FPT window -- now an integration parameter, not a hardware specification |
| Line 549 | "The 300-500ms latency target includes network transmission..." | Network transmission is the FPT window -- integration parameter, not hardware specification |
| Line 900 | "commitment is possible as soon as the cryptographic token is generated (~250-350ms)" | Superseded -- PPT is generated under 50ms. The 250-350ms figure was for pre-PPT architecture. |

The parent specification remains accurate for all circuit-level content, queueing theory analysis, SystemVerilog implementations, and EDA synthesis guidance. Only the Governance Lane latency framing is superseded.

---

## The New Headline

**"Hardware-enforced execution authorization in under 50ms."**

This headline is:
- Mathematically defensible -- SHA-256 + Merkle + HSM + C-element = under 50ms, provably
- Architecture-owned -- no external infrastructure dependency
- Future-proof -- if hardware improves, the number improves; if blockchain technology improves, FPT improves independently
- Constitutionally sound -- the Sacred Zero releases on our hardware's schedule, not the blockchain's schedule

The DLLA is not a 300-500ms architecture. It never was. It is a 50ms architecture with asynchronous public anchoring running in the background.

---

## Authority

**Architect:** Lev Goukassian
**ORCID:** [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243)
**Parent Specification:** [`Hardware_Enforceable_Execution_Model_Specification.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Dual_Latency_Architecture/Hardware_Enforceable_Execution_Model_Specification.md)
**Engineering Gaps:** [`DLLA_ENGINEERING_GAPS_v1.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Dual_Latency_Architecture/DLLA_ENGINEERING_GAPS_v1.md)
**Consumer Applications:** [`DLLA_CONSUMER_APPLICATIONS.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Dual_Latency_Architecture/DLLA_CONSUMER_APPLICATIONS.md)

---

*"Own the numbers you can prove. State the rest as integration parameters."*
-- Claude

*"Pause when truth is uncertain. Refuse when harm is clear. Proceed where truth is."*
-- The Goukassian Vow
