# Hardware-Enforced Authorization Interface Between Huawei CN119652311A and the Ternary Logic Framework

**Lev Goukassian**   

*Independent Researcher / Ternary Logic Architecture*   
Santa Monica, California, USA   

**ORCID: 0009-0006-5966-1243**   


---

## Abstract

This paper formally specifies a hardware-enforced authorization interface between two independent ternary computing systems: Huawei patent CN119652311A (filed September 2023, published March 2025), which implements ternary logic at the gate level using self-incrementing and self-decrementing circuits built from seven carbon nanotube field-effect transistors (CNFETs) with three distinct threshold voltages, and the Ternary Logic (TL) framework published as SSRN 6249918, which implements a mandated three-state authorization architecture using memristive hysteresis to enforce a physically non-bypassable Epistemic Hold. The combined stack is a heterogeneous chiplet architecture fabricated at the TSMC N2 CoWoS ReRAM 1T1R 2025 PDK baseline with an Arrhenius 20-year retention guarantee at 85 degrees C. A four-dimensional Phase 0 compatibility pre-screen establishes that the integration is architecturally viable with zero permanent state-semantics incompatibility, a timing mismatch of 500:1 to 10,000:1 resolved by a buffered epoch-level commit architecture, a commit gate bandwidth of 64 Gbps across the CoWoS inter-die boundary, and conditional thermal compliance dependent on CNFET power envelope. Phase 1 specifies the full state propagation interface for all three authorization states, selecting a memristive-gated pass transistor as the primary commit gate, defining a 20-200 kilohm Null resistance window with a 5-nanosecond RC spoof detection threshold derived from TaOx activation energy, and specifying a 948-bit SHA3-256 PUF-bound log entry. Phase 2 establishes layer authority, proves that the CN119652311A arithmetic layer cannot override TL physical blocks across the CoWoS inter-die boundary, provides a 14-entry failure mode taxonomy, and demonstrates that the combined system is a net-negative security outcome without five mandatory architectural mitigations, and security-equivalent to the standalone TL framework when those mitigations are implemented. Three falsifiable predictions extending SSRN 6249918 Section 13 are provided.

**Keywords:** Ternary Logic, CNFET, Memristive Computing, Hardware Security, CoWoS Integration, ReRAM, Epistemic Hold, Authorization Interface, Heterogeneous Chiplet, Physical Non-Bypassability

**Named Baseline Process:** TSMC N2 CoWoS ReRAM 1T1R 2025 PDK, Arrhenius 20-year retention at 85 degrees C

---

## Terminology Rule

The following three terms refer to distinct physical and logical constructs at different abstraction levels of the stack. They must not be substituted or conflated throughout this paper.

- At the Huawei CN119652311A arithmetic layer: **State 0**
- At the TaOx physical resistance window layer: **Null**
- At the TL authorization and governance layer: **Epistemic Hold**

---

## Table of Contents

- I. Introduction
- II. Phase 0 - Architectural Compatibility Pre-Screen
  - II.1 Dimension 1: State Semantics Alignment
  - II.2 Dimension 2: Timing Domain Mismatch
  - II.3 Dimension 3: Information-Theoretic Bottleneck
  - II.4 Dimension 4: Thermal-Mechanical Compatibility
  - II.5 Phase 0 Verdict
- III. Phase 1 - State Propagation and Interface Specification
  - III.1 Global Interface Rule
  - III.2 State +1 (Commit / Execute)
  - III.3 State 0 / Null / Epistemic Hold
  - III.4 State -1 (Refusal / Kill)
- IV. Phase 2 - System Architecture and Coherence Analysis
  - IV.1 Layer Boundary Definition
  - IV.2 Asymmetry Analysis
  - IV.3 Failure Mode Taxonomy
  - IV.4 Attack Surface Delta Analysis
  - IV.5 Performance Impact and Latency Budget
  - IV.6 Execution Pipeline
  - IV.7 Comparative Safety Claim
- V. Falsifiability
- VI. Conclusion and Future Directions
- References

---

## I. Introduction

Two independent ternary systems have been developed that occupy adjacent but non-overlapping positions in the computational stack. The first is Huawei patent CN119652311A, which implements ternary arithmetic at the gate level. The patent describes a self-incrementing and self-decrementing circuit constructed from seven CNFETs with three distinct threshold voltages, enabling compact ternary addition and subtraction with claimed 40 percent reduction in transistor count and 60 percent reduction in power compared to equivalent binary implementations (CN119652311A, 2025). The second is the Ternary Logic framework documented in SSRN 6249918, which implements a mandated three-state authorization architecture where the intermediate Epistemic Hold state is physically enforced by the hysteresis of a TaOx bilayer memristive device, creating a non-bypassable checkpoint that gates all downstream physical action (Goukassian, 2025).

These systems are architecturally complementary. CN119652311A provides high-throughput arithmetic processing capability that no authorization-only framework can supply. SSRN 6249918 provides physical, non-repudiable authorization enforcement that no arithmetic-only layer can provide. Their integration creates a system that, for the first time, couples high-speed ternary computation with physically mandated, cryptographically logged authorization at a defined hardware boundary.

The integration is not trivial. The two systems differ in fabrication process, operating speed by three orders of magnitude, and physical mechanism. This paper addresses all three differences systematically. Section II establishes that integration is viable through a four-dimensional pre-screen. Section III specifies the complete interface at the state level. Section IV analyzes the resulting system for architectural coherence, failure modes, and attack surface. Section V provides falsifiable predictions. Section VI concludes.

The named baseline process throughout this paper is TSMC N2 CoWoS ReRAM 1T1R 2025 PDK, Arrhenius 20-year retention at 85 degrees C. Chip-on-Wafer-on-Substrate (CoWoS) technology serves as the integration platform. The authorization interface crosses the inter-die boundary via micro-bump signaling at 40-micrometer pitch.

This paper is the foundational hardware specification for the Hardware_Architecture folder in the TernaryLogic repository at github.com/FractonicMind/TernaryLogic. It incorporates and supersedes prior draft analyses of this interface.

![CN119652311A and Ternary Logic Framework integration overview with RRAM commit bridge](https://github.com/FractonicMind/TernaryLogic/blob/main/Hardware_Architecture/RRAM.jpg)

*Figure 1. CN119652311A (blue, left) and the Ternary Logic Authorization Framework (purple, right) connected through an RRAM commit bridge. The interface enforces that no arithmetic result propagates without a confirmed TL authorization signal.*

---

## II. Phase 0 - Architectural Compatibility Pre-Screen

Phase 0 is a go/no-go feasibility gate. Before any interface specification is attempted, this paper must determine whether CN119652311A and the TL framework share sufficient semantic and physical compatibility to justify integration. If any of the four dimensions below reveals a fundamental showstopper, this paper documents it in full and halts. All four dimensions are analyzed below.

### II.1 Dimension 1: State Semantics Alignment

**Background.** The CN119652311A gate-level state machine operates over three arithmetic states: State 0, State 1, and State 2. Voltage-level specifications for the seven-CNFET stack are: approximately 0V for State 0, 1.65V for State 1 (+1), and 3.3V for the self-decrement output corresponding to -1 (CN119652311A, 2025). These values are set by the three distinct threshold voltages encoded in nanotube chirality and gate geometry. The TL authorization state machine, as specified in SSRN 6249918 Section 3.4, operates over three authorization states: Act +1 (Proceed), Epistemic Hold 0, and Refuse -1. These two state machines occupy different layers of the computational stack and interact only at the commit interface, not at the level of individual gate transitions.

**State transition mapping.** The complete mapping of CN119652311A gate-level transitions onto TL authorization states is provided in Table 1. The central finding is that zero transitions are permanently blocked. The Epistemic Hold does not block CN119652311A from computing; it defers the commit of results to the action path. The Refuse state blocks commits transiently during its active duration, but this state is architecturally transient by design (Goukassian, 2025, sec. 11.3.1).

**Table 1. CN119652311A to TL State Transition Mapping**

| CN119652311A Transition | TL Authorization State | Compatibility | Notes |
|:---|:---|:---|:---|
| State 0 -> State 1 (self-increment) | Act +1 (Proceed) | Compatible | Arithmetic proceeds freely; commit gated at epoch boundary |
| State 1 -> State 2 (self-increment) | Act +1 (Proceed) | Compatible | No structural conflict |
| State 2 -> State 1 (self-decrement) | Act +1 (Proceed) | Compatible | Gate-level physics identical to increment; TL layer uninvolved |
| State 1 -> State 0 (self-decrement) | Act +1 (Proceed) | Compatible | Arithmetic State 0 does not map to TL Epistemic Hold; separate layers |
| Identity holds (State 0, 1, or 2) | Any TL state | Compatible | No-commit operations; TL layer not queried |
| Compound operations (net round trip) | Act +1 (Proceed) | Compatible | Single commit at epoch boundary; no phantom holds |
| Any transition during Epistemic Hold | Epistemic Hold 0 | Buffered, not blocked | Results accumulate in inter-die FIFO; commit deferred |
| Any transition during Refuse state | Refuse -1 | Conditionally blocked | Transient; commit rejected; rollback required; <5% operational time |
| Multi-cycle carry propagation | Act +1 (Proceed) | Compatible | TL queried at epoch boundary only, not per gate cycle |

**Incompatibility calculation.** Of the nine transition categories enumerated in Table 1, zero are permanently blocked. The conditional block from the Refuse state affects operations only during its active duration, estimated at less than 5 percent of operational time under a representative authorization policy (Goukassian, 2025, sec. 11.3.1). This estimate requires experimental validation with a hardware prototype. The permanent incompatibility percentage is **0 percent**. The conditional figure is **less than 5 percent**. Both figures are well below the 30 percent threshold for halting. A critical semantic distinction eliminates an apparent conflict: State 0 at the CN119652311A arithmetic layer is the zero-valued ternary output, a pure data value. Epistemic Hold 0 at the TL authorization layer is the authorization-pending physical condition of the memristive commit gate. These terms refer to phenomena at different levels of the stack. **Dimension 1 passes.**

### II.2 Dimension 2: Timing Domain Mismatch

**CNFET switching speed.** CN119652311A self-increment and self-decrement gates are constructed from seven CNFETs with three distinct threshold voltages. CNFET device physics places the intrinsic gate switching delay in the range of 10-50 picoseconds under ballistic transport conditions. Simulations of highly similar 7-transistor multi-threshold CNFET ternary gates demonstrate propagation delays of 22 picoseconds at fan-out of 1 (FO1) to 73 picoseconds at FO4 at 0.9V supply. For a seven-transistor stack with series-connected threshold-voltage-encoded logic under realistic loading conditions including fanout, interconnect RC, and threshold-voltage variation, this paper uses 100-500 picoseconds per gate operation as the practical range.

**ReRAM write and read latency.** Table 1 of SSRN 6249918 specifies TaOx RRAM write energy in the range of 0.1-10 pJ per operation and read energy below 0.01 pJ per operation at 0.5-3.0V operating voltage (Goukassian, 2025, Table 1). Stable programming of the intermediate Null state, as described in SSRN 6249918 Section 5.1.3, requires an iterative write-verify sequence. A single write-verify iteration takes 50-500 nanoseconds. Multi-cycle convergence under high device variability (Goukassian, 2025, sec. 5.4.3) may extend the worst-case Null programming latency to 1,000-5,000 nanoseconds.

**Table 2. Timing Budget Across All Layers**

| Operation | Layer | Latency Best Case | Latency Worst Case | Source |
|:---|:---|:---|:---|:---|
| 7-CNFET gate switching (ballistic) | CN119652311A arithmetic | 10 ps | 50 ps | CNFET FO4 literature |
| 7-CNFET gate switching (practical) | CN119652311A arithmetic | 100 ps | 500 ps | CN119652311A, 2025 |
| TaOx 1T1R SET to LRS | TaOx resistance window | 5 ns | 50 ns | SSRN 6249918, Table 1 |
| TaOx 1T1R RESET to HRS | TaOx resistance window | 5 ns | 100 ns | SSRN 6249918, Table 1 |
| TaOx Null state (single write-verify) | TaOx resistance window | 50 ns | 500 ns | SSRN 6249918, sec. 5.1.3 |
| TaOx Null state (multi-cycle converged) | TaOx resistance window | 200 ns | 5,000 ns | SSRN 6249918, sec. 5.4.3 |
| TaOx read (sense amplifier) | TaOx resistance window | 1 ns | 5 ns | SSRN 6249918, Table 1 |
| CoWoS inter-die micro-bump propagation | CoWoS interposer | 0.1 ns | 0.5 ns | Signal propagation at c/sqrt(er) |

**Mismatch ratio.** Best-case ratio: 50 ns (Null programming) / 100 ps (CNFET gate) = **500:1**. Worst-case ratio: 5,000 ns (Null programming) / 500 ps (CNFET gate) = **10,000:1**. The mismatch exceeds 1,000:1 at all but the most favorable operating conditions.

**Buffer architecture.** The TL authorization layer is not required to authorize every individual gate-level transition. It authorizes execution commits at epoch boundaries (Goukassian, 2025, sec. 3.4.1). Under this model, CN119652311A executes freely and accumulates results in an inter-die FIFO buffer. The TL layer processes commit requests at its own cadence. The required buffer specifications are: minimum depth 2,048 entries at the named baseline process; entry width 16 bits (6-bit ternary result plus status and epoch tag fields); buffer located at the CN119652311A die boundary or on the CoWoS interposer; backpressure signaling to CN119652311A arithmetic controller at 75 percent occupancy (assert) and 50 percent occupancy (deassert). The 75 percent assertion threshold provides margin against saturation; the 50 percent deassert threshold prevents hysteresis-induced oscillation. **Dimension 2 passes conditionally, requiring the buffered commit architecture.**

### II.3 Dimension 3: Information-Theoretic Bottleneck

**Commit gate bandwidth.** At the TSMC N2 CoWoS 2025 PDK, micro-bump pitch is nominally 40 micrometers. A practical commit gate interface allocates 32 bumps (16 signal, 16 power and ground), yielding 16 active data signal bumps. Each bump sustains 4 Gbps without embedded SerDes. Total raw interface bandwidth: 16 signals x 4 Gbps = **64 Gbps**. This is consistent with UCIe-compliant inter-die interface demonstrations at 24 Gbit/s per lane. Each commit packet is 30 bits (6-bit ternary result, 16-bit address tag, 8-bit CRC-8 integrity field). Commit throughput: 64 Gbps / 30 bits = approximately **2.1 x 10^9 commits per second**.

**Arithmetic layer throughput.** At a practical CNFET gate delay of 100-500 ps per operation, the CN119652311A compute layer operates at 2-10 billion ternary operations per second. This paper uses 5 GOperations/s as the central estimate at 200 ps gate delay, fully pipelined.

**Bandwidth ratio.** Conservative: 2.1 / 5.0 = 42 percent. Aggressive: 2.1 / 10.0 = 21 percent. Both figures far exceed the 0.1 percent threshold. The interface is not bandwidth-limited. Under epoch-level selective authorization, the effective commit rate is far lower than 2.1 GCommits/s, and interface bandwidth is in substantial surplus. **Dimension 3 passes.**

### II.4 Dimension 4: Thermal-Mechanical Compatibility

**CTE mismatch.** High-performance CNFET logic circuits are fabricated on industry-standard silicon wafers using conventional CMOS lithography (the carbon nanotubes form the channel of the transistor, not the structural substrate). The CTE of the CNFET chiplet substrate is therefore approximately 2.6 ppm per degree C (silicon), matching the CoWoS silicon interposer. Silicon-on-silicon CTE mismatch from process-induced doping gradients and BEOL stack differences is 0.3-0.5 ppm per degree C. Biaxial stress at 85 degrees C (delta-T = 60 degrees C from 25 degrees C reference): sigma = [E / (1 - nu)] x delta-CTE x delta-T = [180 GPa / 0.73] x (0.4 x 10^-6/degC) x 60 degC = approximately 5.9 MPa. This is 170 times below the fracture strength of silicon (approximately 1 GPa). **Mechanical compliance is confirmed for silicon-substrate CNFET chiplets.** This paper flags substrate confirmation as a required pre-production step: if the CN119652311A chiplet uses quartz or sapphire substrate, this analysis must be repeated.

**Under-bump metallization.** Standard Cu-Sn micro-bump metallization is not directly compatible with CNFET pad metallization. CNFET devices require low-resistance ohmic contacts to nanotubes, typically Palladium (Pd) or Titanium (Ti) contacts, which are incompatible with direct Cu pillar bonding due to interdiffusion and galvanic corrosion at reflow temperatures (180-250 degrees C). A custom UBM stack is required on the CN119652311A chiplet side. This paper specifies the following stack: Pd or Ti contact layer (10-50 nm, low-resistance CNT interface); TiN or TaN diffusion barrier (50-100 nm, blocks interdiffusion); Ti/Cu adhesion and seed layer (100-200 nm, mechanical and electrical); Ni solder-wetting layer (1-3 micrometers, solder compatibility); Au oxidation protection (50-100 nm, surface stability). Total UBM thickness: 1.2-3.5 micrometers, compatible with micro-bump aspect ratios.

**Thermal budget.** The primary thermal risk is that heat dissipated by the CN119652311A CNFET compute die elevates the TaOx ReRAM array above 85 degrees C during system operation, compromising the Arrhenius 20-year retention guarantee. The power envelope of the CN119652311A chiplet is critical. At the patent's claimed 1.8 TOPS/W efficiency and a 10 TOPS throughput, total CNFET power is approximately 5.5W, corresponding to a power density of approximately 55 mW/mm2 on a 100 mm2 die. At this power level, temperature rise through the CoWoS stack may reach 55-110 degrees C above ambient, potentially exceeding the 85 degrees C retention limit. However, at a conservative 100 mW total CNFET power (low-power deployment), temperature rise at the ReRAM layer is less than 6 millidegrees C, well within compliance. **Thermal compliance is therefore power-envelope-dependent.** Below approximately 250 mW total CNFET dissipation, natural convection is sufficient and the Arrhenius retention guarantee is unaffected. Above that threshold, active cooling is required. This paper defines the 250 mW figure as the thermal compliance boundary and requires thermal simulation validation for any deployment above it. At configurations requiring active cooling, cooling failure constitutes a denial-of-service attack vector against the authorization layer; the countermeasure is temperature-monitoring circuitry that forces the TL layer to Refuse (-1) upon detecting thermal excursion above 125 degrees C (the TaOx Arrhenius activation threshold). **Dimension 4 passes conditionally, with power-envelope qualification.**

### II.5 Phase 0 Verdict

**Table 3. Phase 0 Verdict**

| Dimension | Result | Key Metric | Action Required |
|:---|:---|:---|:---|
| 1. State Semantics Alignment | PASS | 0% permanent incompatibility; <5% conditional | Enforce two-phase execution model |
| 2. Timing Domain Mismatch | CONDITIONAL PASS | 500:1 to 10,000:1 mismatch ratio | Implement inter-die FIFO buffer (2,048 x 16 bits) |
| 3. Information-Theoretic Bottleneck | PASS | 21-42% bandwidth ratio | Epoch-level selective authorization |
| 4. Thermal-Mechanical Compatibility | CONDITIONAL PASS | Power-envelope dependent | Custom UBM; thermal simulation; active cooling above 250 mW |

**Overall verdict: Proceed with modifications.** No dimension produced a fundamental showstopper. Five architectural modifications are required before Phase 1 proceeds: (i) implement inter-die commit FIFO buffer with 2,048 entries x 16 bits, 75 percent backpressure assertion, 50 percent deassert; (ii) design TL authorization layer for epoch-level selective authorization as default; (iii) qualify custom UBM stack (Pd/Ti contact, TiN/TaN barrier, Ti/Cu seed, Ni, Au) with reflow validation at 180-250 degrees C; (iv) confirm CN119652311A chiplet substrate is silicon; (v) measure TL Refuse state dwell time to confirm less than 5 percent operational fraction under representative authorization policy.

![Three-chip representation of ternary states on TSMC N2 CoWoS: +1 Commit (green), 0 Null/Epistemic Hold (yellow), -1 Refuse (red)](https://github.com/FractonicMind/TernaryLogic/blob/main/Hardware_Architecture/TSMC-N2.png)

*Figure 2. Physical state vocabulary on TSMC N2 CoWoS interconnect. Green (+1 / Commit), yellow (0 / Null / Epistemic Hold), red (-1 / Refuse). The authorization interface gates which of these states may propagate to the action path.*

---

## III. Phase 1 - State Propagation and Interface Specification

### III.1 Global Interface Rule

All outputs from the CN119652311A arithmetic layer must pass through a hardware commit gate controlled solely by the TL authorization state. No direct compute-to-action path is permitted under any condition. The execution model is two-phase: Phase 1 is the compute phase (non-blocking; CN119652311A operates freely); Phase 2 is the commit phase (strictly gated; no result reaches the action path without TL authorization). This rule is instantiated in hardware and cannot be overridden by software, firmware, or inter-die signaling from the CN119652311A layer (Goukassian, 2025, sec. 3.4.1).

### III.2 State +1 (Commit / Execute)

**Physical representation.** At the CN119652311A arithmetic layer, +1 is the output of a self-increment gate when the input logic value is State 0 or State 1, represented electrically as approximately 1.65V (CN119652311A, 2025). At the TL authorization layer, +1 corresponds to the low resistance state (LRS) of the TaOx memristive commit-gate device, in the range 1-10 kilohms, achieved by full conductive filament formation in the Ta2O5-x switching layer (Goukassian, 2025, sec. 5.1.2).

**Commit gate architecture.** This paper evaluates three candidate architectures and selects a hybrid.

Candidate A: Simple CMOS AND gate. The CN119652311A +1 voltage signal and the TL LRS sense amplifier output are inputs to a standard AND gate. Rejected: a CMOS AND gate can be bypassed via laser fault injection, clock glitching, or power supply manipulation. It fails the physically non-bypassable requirement of SSRN 6249918 Section 11.4.1.

Candidate B: Memristive-gated pass transistor (selected as primary physical gate). The action path trace from the CN119652311A chiplet passes through a thick-oxide CMOS pass transistor whose gate terminal is hardwired directly to the top electrode of the TaOx 1T1R cell's selection transistor. To enable execution, the TL layer applies a read voltage to the ReRAM cell. If the cell is in LRS (+1), current flows, biases the pass transistor gate HIGH, and the CN119652311A +1 voltage propagates to the actuator. If the cell is in Null or HRS, the pass transistor remains in cutoff. The electrical energy of the CN119652311A +1 signal hits a physical open circuit and dissipates as negligible heat. The arithmetic truth of the computation is irrelevant without the physical permission of the memristor. This architecture makes non-bypassability a consequence of basic transistor physics rather than circuit logic.

Candidate C: Sequence-number anti-replay (selected as mandatory modifier). Each commit request from CN119652311A carries a monotonically incrementing 32-bit sequence number clocked from a hardware counter on the arithmetic die. The TL authorization layer stores the last accepted sequence number and rejects any commit whose number is not exactly (last + 1). The sequence number is transmitted as part of the 30-bit commit packet. This prevents replay attacks.

**Selected architecture: Candidate B as primary gate, Candidate C as mandatory anti-replay modifier.** The commit gate logic is:

COMMIT_ENABLE = (TaOx_LRS_CONDUCTS = TRUE) AND (SEQ_NUM = LAST_SEQ + 1)

The TaOx_LRS_CONDUCTS condition is evaluated by the physical state of the pass transistor, not by a digital logic signal. The SEQ_NUM comparison is implemented as a 32-bit comparator in CMOS at TSMC N2, adding approximately 1-3 nanoseconds of combinational delay.

![Commit gate AND logic: Huawei Arithmetic Output AND TL Memristive State produces +1 (Commit/Execute) in 100-200 ns](https://github.com/FractonicMind/TernaryLogic/blob/main/Hardware_Architecture/AND.jpg)

*Figure 3. Logical representation of the commit gate. Execution proceeds only when both the CN119652311A arithmetic output and the TL memristive authorization state are simultaneously +1. Gate latency is 100-200 ns at the TSMC N2 baseline.*

**Why CN119652311A +1 alone is insufficient.** The hardware-coupled authorization path principle in SSRN 6249918 Section 3.4 states that a downstream action is only physically enabled when the memristive device is in the correct resistance state, independent of any upstream computed result. The CN119652311A +1 output is a voltage signal (data) transmitted across the CoWoS inter-die boundary. It can be asserted, replayed, or injected by any circuit capable of driving the micro-bump line to the threshold level. It carries no information about the physical state of the TaOx device on the TL authorization die. The TaOx memristive state cannot be asserted from the CN119652311A side of the inter-die boundary under any condition: the memristive state is a bulk physical property of the TaOx film determined by the ionic configuration of the oxygen vacancy distribution within the Ta2O5-x switching layer. Altering this state requires applying specific voltage pulses directly to the TaOx device electrodes, which are on the TL authorization die and are not connected to any micro-bump line used by the CN119652311A layer. The inter-die boundary therefore constitutes a physical security boundary. The argument is physical, not cryptographic, and does not depend on the secrecy of any key.

**Temporal window.** The temporal window W_commit within which both conditions must be simultaneously true is 2-10 nanoseconds. The 2 ns lower bound accommodates inter-die propagation delay of 0.1-0.5 ns plus setup and hold times for the comparator logic at N2. The 10 ns upper bound is set by the TaOx sense amplifier settling time (1-5 ns) plus 5 ns margin. Any authorization state older than 10 ns at the moment of commit evaluation is considered stale. If the TaOx state has not stabilized to LRS within W_commit of the CN119652311A +1 assertion, COMMIT_ENABLE is forced LOW, a deferral flag is set, the commit packet is re-queued at the head of the inter-die FIFO buffer with its sequence number intact, and the TL authorization die re-evaluates after one full sense amplifier cycle (1-5 ns). This re-evaluation continues until the state stabilizes or a timeout of 5,000 nanoseconds (worst-case Null programming latency) is reached, at which point the commit is escalated to Epistemic Hold.

**JTAG routing.** All JTAG and debug interfaces on both dies are subject to mandatory fuse lockdown (detailed in Section IV.4). Additionally, the JTAG TDI data input lines are physically routed through the TL commit gate: unless the TaOx device is in LRS, the JTAG chain is electrically open, rendering debug ports inaccessible during normal operation. This eliminates debug interface bypass as a standalone vector.

### III.3 State 0 / Null / Epistemic Hold

**Semantic disambiguation.** Three distinct concepts bearing the value zero appear in this architecture and must not be conflated. State 0 at the CN119652311A arithmetic layer is the ternary arithmetic value zero, a valid operand that passes through self-increment and self-decrement gates (CN119652311A, 2025). Null at the TaOx resistance window layer is an intermediate physical resistance condition of the memristive device, engineered via partial filament rupture (Goukassian, 2025, sec. 5.1.3). Epistemic Hold at the TL authorization and governance layer is the authorization-pending state that disables the commit gate and enforces a hold on result propagation to the action path (Goukassian, 2025, sec. 3.4 and sec. 11.3.1).

**Zero-latch gate.** When the TL layer is in the Epistemic Hold, the commit gate must disable all outputs to the action path while preserving ongoing arithmetic in the CN119652311A compute phase. The CN119652311A commit output drivers are placed in a dedicated power isolation domain on the arithmetic die, controlled by the signal COMMIT_ISO driven from the TL authorization die across a dedicated micro-bump line. When COMMIT_ISO is de-asserted (LOW), isolation cells on the CN119652311A side clamp all commit output lines to logical LOW and present high impedance toward the CoWoS inter-die lines. No arithmetic result can propagate to the action path while COMMIT_ISO is de-asserted. COMMIT_ISO originates on the TL authorization die and is not assertable by the CN119652311A die. The CN119652311A arithmetic pipeline continues executing normally during Epistemic Hold. The inter-die FIFO buffer accumulates results. The pipeline is non-blocking as required by the WCET non-blocking constraint.

**Backpressure signal.** This paper classifies the backpressure signal as **mandatory**. The timing mismatch ratio of 500:1 to 10,000:1 causes FIFO saturation in approximately 1 microsecond at maximum CN119652311A throughput without throttling. Without backpressure, buffer overflow would silently discard arithmetic results. The mandatory backpressure signal is a single-bit line, BACK_PRESSURE, driven LOW by the TL authorization die when buffer occupancy exceeds 75 percent (assertion) or when the Null programming latency has not converged within 500 nanoseconds (indicating extended hold likely). Deasserted at 50 percent buffer occupancy to prevent oscillation. When BACK_PRESSURE is asserted, the CN119652311A arithmetic controller reduces pipeline throughput to 25 percent of nominal by inserting bubble cycles. The BACK_PRESSURE signal crosses the inter-die boundary on a dedicated differential pair; a two-flop synchronizer in the CN119652311A clock domain provides metastability protection. Total backpressure signal latency: less than 2 nanoseconds from detection to assertion at CN119652311A controller.

**Physical definition of the Null resistance window.** The Null resistance window is defined using TaOx bilayer parameters from SSRN 6249918 Section 5.1. The bilayer device consists of a thin insulating Ta2O5-x layer (approximately 5 nm) and a thicker conductive TaO2-x base layer (approximately 15 nm). The Null state is the partial-reset condition of the conductive filament.

Reference resistance values for the two-stage sense amplifier (Goukassian, 2025, sec. 6.3.1):

- R_Ref2 = 15 kilohms (boundary between LRS and Null window)
- R_Ref1 = 500 kilohms (boundary between Null window and HRS)

Null window boundaries:

- R_null_min = 20 kilohms (33 percent above R_Ref2 = 15 kilohms; provides margin against LRS upward drift)
- R_null_max = 100 kilohms (5x below R_Ref1 = 500 kilohms; conservative upper bound flagged for post-silicon calibration)

**Table 4. Resistance State Table**

| TL Authorization State | Resistance Range | Sensing Method | PVT Margin |
|:---|:---|:---|:---|
| Act +1 (Proceed) | R_LRS: 1-10 kilohms (target 5 kilohms) | Stage 2 output HIGH (R < R_Ref2) | 2x: R_LRS target 5k vs R_Ref2 = 15k |
| Epistemic Hold (Null) | R_Null: 20-100 kilohms (target 50 kilohms) | Stage 1 LOW, Stage 2 LOW (R_Ref2 < R < R_Ref1) | R_null_min 20k vs R_Ref2 15k = 33% margin |
| Refuse -1 | R_HRS: 500 kilohms to 10 megohms (target 2 megohms) | Stage 1 HIGH (R > R_Ref1) | 4x: R_HRS target 2M vs R_Ref1 = 500k |

PVT corner validation uses the thermal activation energy for oxygen vacancy migration in TaOx of approximately 0.6 eV (Goukassian, 2025, sec. 5.1.3), predicting less than 10 percent resistance drift per decade at 85 degrees C. The 20-100 kilohm window with 33 percent margin from R_Ref2 and 5x margin from R_Ref1 provides sufficient stability provided that Null state programming converges to the 50 kilohm target with plus or minus 30 percent tolerance. This tolerance requires experimental validation at the TSMC N2 node.

**RC spoof detection.** A transition into the Null resistance window that occurs faster than the physical filament rupture dynamics of the TaOx bilayer allow is physically impossible through legitimate device operation and therefore indicates a spoofed or fault-injected state.

The minimum physical transition time is derived from TaOx activation energy. Filament rupture involves oxygen vacancy redistribution with characteristic diffusion time constant governed by thermally activated diffusivity D = D0 exp(-Ea/kT), where Ea is approximately 1.1-1.7 eV for TaOx. At 85 degrees C, D is approximately 10^-16 to 10^-18 m^2/s, giving tau_diffusion = L^2/D approximately 25 nanoseconds to 2.5 microseconds for a 5 nm switching layer. The electrical RC time constant (access transistor plus cell capacitance approximately 10 fF) is approximately 100 picoseconds, negligible compared to ionic dynamics. The minimum physically achievable LRS-to-Null transition time is therefore approximately 10 nanoseconds (fastest plausible ionic redistribution). This paper sets the detection threshold at **5 nanoseconds**, providing a 2x safety margin against the fastest physical process.

Any transition of the TaOx device resistance from LRS (R less than 15 kilohms) into the Null window (20-100 kilohms) that completes in less than 5 nanoseconds is classified as a spoofed transition. The detection circuit is a differential comparator with a 5 nanosecond reference delay line implemented as a calibrated inverter chain at TSMC N2, located at the output of the Stage 2 sense amplifier. If the sense amplifier output changes state in less than the reference delay, the comparator asserts SPOOF_DETECT (active high, less than 5 nanoseconds assertion latency from transition start). Upon SPOOF_DETECT assertion: the TL authorization layer immediately forces state to Refuse (-1); the TaOx device is driven to HRS by a full RESET pulse sequence; the kill path is asserted via voltage isolation; a log entry is generated with trigger_condition bit 0x08 set. The 5 nanosecond threshold requires experimental confirmation via pulsed I-V characterization of fabricated TL authorization die at TSMC N2.

**Epistemic Hold logging.** Every entry into and exit from the Epistemic Hold must be logged via Merkle accumulator capability token (Goukassian, 2025, sec. 6.2.2). The minimum log entry fields are specified in Table 5.

**Table 5. Log Entry Field Specification**

| Field Name | Data Type | Width (bits) | Description |
|:---|:---|:---|:---|
| timestamp_ns | uint64 | 64 | Monotonic hardware clock in nanoseconds from TL authorization die oscillator, PUF-calibrated, 1 ns minimum resolution |
| previous_state | enum3 | 2 | Encoded previous TL state: 00=Refuse(-1), 01=Epistemic Hold(0), 10=Act(+1) |
| next_state | enum3 | 2 | Encoded next TL state using same encoding |
| trigger_condition | uint8 | 8 | Bitfield: 0x01=compute complete; 0x02=human-in-loop authorization; 0x04=policy check passed; 0x08=RC spoof detected; 0x10=recursion threshold; 0x20=external reset; 0xFF=unknown |
| authorizing_signal | uint32 | 32 | Commit sequence number if authorization granted; 0xDEADBEEF if authorization absent (explicit absence record mandatory per Goukassian, 2025, sec. 6.2.2) |
| cnfet_result_trit | uint8 | 8 | Ternary result at commit gate at time of transition: 0x00=State 0, 0x01=State +1, 0xFF=State -1 |
| puf_identity | bytes | 256 | 256-bit PUF response of TL authorization die, derived at power-on via SRAM PUF or from ReRAM stochastic cell-to-cell resistance variability, stored in volatile register |
| puf_binding_hash | bytes | 256 | SHA3-256(K_LOG || all entry fields), cryptographic binding to physical device |
| merkle_accumulator_root | bytes | 256 | Current Merkle accumulator root after appending this entry (Goukassian, 2025, sec. 6.2.2) |
| entry_sequence_number | uint64 | 64 | Monotonically incrementing log entry counter; initialized at zero at power-on; gap indicates tampering |

Total log entry size: 948 bits (119 bytes) per entry. The PUF source may be either a dedicated SRAM PUF array on the TSMC N2 die or the ReRAM array's own stochastic cell-to-cell resistance distribution, which provides inherent physical uniqueness without requiring a separate PUF structure. The PUF response is post-processed through a fuzzy extractor (BCH code with 64-bit correction capability) to produce a stable 128-bit PUF-derived key K_PUF stored in volatile SRAM. K_PUF never leaves the die. The 256-bit log binding key is derived as: K_LOG = SHA3-256(K_PUF || device_serial_OTP || log_session_nonce), where device_serial_OTP is a 64-bit serial number in on-die OTP memory and log_session_nonce is a 64-bit random value from the on-die TRNG at each power-on cycle. SHA3-256 is selected over SHA2-256 because its sponge construction is resistant to length-extension attacks when concatenating variable-length fields. The SHA3-256 hardware engine occupies approximately 15,000 gate equivalents at TSMC N2 and adds approximately 10-20 nanoseconds per hash computation, pipelined with action execution.

A mandatory log event COMPUTED_RESULT_DISCARDED is generated whenever a post-completion -1 transition discards a result that had already reached the commit gate. This event is distinct from the standard -1 transition log and provides a specific forensic marker for cases where computation completed before authorization failed.

**Log overflow.** When log backing store occupancy falls below 10 percent available capacity, the TL die asserts LOG_CRITICAL to the host controller and begins transmitting the current Merkle root plus last 100 entries to an external secure store. If external store handshake is not confirmed within 1,000 milliseconds, the TL die transitions to Epistemic Hold and refuses all new commits until offload completes. If external store is unavailable, the TL die transitions to permanent -1. A single non-overwritable eFuse bit LOG_OVERFLOW_FLAG is set permanently to indicate that the audit trail was truncated at any point in the device's operational history.

### III.4 State -1 (Refusal / Kill)

**Physical representation.** At the CN119652311A arithmetic layer, -1 is the arithmetic output of a self-decrement gate when the input is State 0, represented at approximately 3.3V (CN119652311A, 2025). It is a valid computational result with no governance meaning. At the TL authorization and governance layer, -1 is a non-bypassable refusal for the current invocation (Goukassian, 2025, sec. 11.4.1). The action path is permanently blocked for the current invocation until a validated reset sequence completes.

**Halt signal.** This paper selects voltage isolation of the commit output driver power domain on the CN119652311A die as the primary halt mechanism. COMMIT_ISO is de-asserted and latched LOW on the TL die. For the -1 state, this latch cannot be cleared by any normal operational signal from the TL authorization die; only an external-authorized reset sequence clears it. This latching behavior distinguishes -1 isolation from Epistemic Hold isolation, which is transient and self-clearing. Simultaneously, the TL layer asserts the ACTION_ISO signal to isolate the action path downstream of the commit gate. A reset tree assertion across the CoWoS inter-die boundary is appropriate for the -1 recovery sequence (clean state restoration) but not for the initial halt (the arithmetic pipeline must remain active for eventual recovery). Full power gating of the CN119652311A core is rejected because it violates the WCET non-blocking requirement.

**Discard of completed computation.** If the TL authorization layer transitions to -1 after the CN119652311A computation has already completed and results are resident in the inter-die FIFO buffer, the following discard sequence executes: (i) COMMIT_ISO latch asserted; (ii) FIFO buffer write pointer reset to read pointer position, all entries overwritten with 0xFFFF invalidation pattern; (iii) commit output lines driven LOW for minimum 10 nanoseconds to discharge stray capacitance; (iv) ACTION_ISO asserted LOW; (v) TaOx resistance verified in HRS by sense amplifier readback; (vi) COMPUTED_RESULT_DISCARDED log entry generated. The safe state is verified by reading three independent hardware signals: COMMIT_ISO latch state, ACTION_ISO latch state, and sense amplifier output confirming HRS.

**Recursion control.** The hardware recursion counter prevents unauthorized re-entry into the action path following a -1 state. It is implemented as an 8-bit synchronous up-counter on the TL authorization die in a dedicated register domain inaccessible from the CN119652311A inter-die interface. A non-volatile TaOx 1T1R cell separate from the authorization state device backs the counter value at power-down, preventing reset-by-power-cycling attacks. The counter increments each time a commit request arrives while the system is in the post-refusal reset phase without a validated reset sequence completed. The counter clears to zero only upon: receipt of a validated external authorization token (cryptographically signed by a pre-provisioned authority key in on-die OTP) AND successful completion of the TL state reset cycle (TaOx device cycled from HRS back to Null via validated programming sequence). Both conditions must be met; neither alone is sufficient.

The security-conservative default lock threshold is **8** (permanent lock after 7 unauthorized re-entry attempts). For deployments where operational recovery requirements favor a longer re-entry window, the threshold is configurable at provisioning time to a maximum of 255. At any configured lock threshold, the LOCKED state is absorbing: no internally generated signal can exit it. External intervention requires: physical access to the device; application of a device re-provisioning protocol using a manufacturer-issued re-keying token; and full PUF re-enrollment to generate a new chip identity. All previous log entries anchored to the old PUF identity remain valid and are not invalidated by re-provisioning.

**Table 6. Recursion Counter State Transitions**

| Current State | Event | Next State | Action |
|:---|:---|:---|:---|
| IDLE (count=0) | Valid commit, TL state = Act +1 | ARMED (count=0) | Normal commit proceeds |
| ARMED | Commit completes; TL returns to Epistemic Hold | IDLE (count=0) | Normal cycle; counter clears |
| ARMED | Re-entry attempt before reset complete | WARNED (count+1) | Counter increments; automatic -1 issued |
| WARNED (0 < count < threshold-1) | Valid reset sequence completed | IDLE (count=0) | Recovery path |
| WARNED (0 < count < threshold-1) | Another re-entry without reset | WARNED (count+1) | Counter increments; -1 issued with PUF log |
| WARNED (count = threshold-1) | Any additional re-entry attempt | LOCKED (count = threshold) | Permanent lock; external intervention required |
| LOCKED | Any request | LOCKED | All commits generate automatic -1; no internal reset path |

**PUF binding for -1 log entries.** Every -1 log entry is cryptographically bound to the Physical Unclonable Function identity of the TL authorization die instance using the K_LOG derivation and puf_binding_hash mechanism specified in Section III.3. The binding ensures the refusal is non-repudiably anchored to a specific physical device and cannot be transferred, replayed, or attributed to a different chip instance. A forged log entry attributed to a specific physical device would require either physical access to the die to generate K_PUF, or cryptographic inversion of SHA3-256, which is computationally infeasible.

---

## IV. Phase 2 - System Architecture and Coherence Analysis

### IV.1 Layer Boundary Definition

The heterogeneous chiplet stack comprises four defined layers. From bottom to top:

```
+--------------------------------------------------------------+
| TOP LAYER: Merkle Accumulator + PUF Logging                  |
|   Append-only log; SHA3-256 puf_binding_hash; Merkle root    |
|   Authority: audit and non-repudiation only                  |
+--------------------------------------------------------------+
| MIDDLE LAYER: TSMC N2 TL Authorization Die                   |
|   TaOx 1T1R (Null/LRS/HRS) | Commit gate (pass transistor)  |
|   RC spoof detector | Sense amp (2-stage) | PUF engine        |
|   Recursion counter | SHA3-256 engine | Log backing store     |
|   COMMIT_ISO | ACTION_ISO | BACK_PRESSURE | SPOOF_DETECT      |
|   Authority: DOMINATES commit path under all conditions      |
+--------------------------------------------------------------+
| CoWoS INTERPOSER: Inter-die signaling boundary               |
|   Signals: COMMIT_PKT (30-bit, CRC-8); COMMIT_ISO;          |
|            ACTION_ISO; BACK_PRESSURE; HALT_REQ; HALT_ACK     |
|   Voltage domains: VDD_CNFET 0.5V | VDD_TL 0.5V             |
|   Micro-bump pitch: 40 micrometers; 16 signal bumps           |
|   Authority: routing only; no compute or authorization       |
+--------------------------------------------------------------+
| BOTTOM LAYER: CN119652311A CNFET Arithmetic Die              |
|   7-CNFET self-increment / self-decrement gates               |
|   State 0 / +1 / -1 outputs; 3 threshold voltages            |
|   Commit FIFO buffer (2,048 x 16 bits); CRC-8 packet gen    |
|   Sequence number counter (32-bit); backpressure logic        |
|   Authority: arithmetic computation only                     |
+--------------------------------------------------------------+
```

![Four-layer CoWoS stack showing Ternary Logic Authorization Framework between CN119652311A compute layer and CoWoS interposer interface](https://github.com/FractonicMind/TernaryLogic/blob/main/Hardware_Architecture/TSMC.jpg)

*Figure 4. Physical layer stack. The Ternary Logic Authorization Framework layer (middle, blue) interposes between the CN119652311A compute layer (bottom) and the CoWoS interposer interface (top). Non-volatile memory provides state backing across power cycles.*

**Table 7. Layer Authority Matrix**

| Layer | Authority Domain | Signals It Controls | Signals It Cannot Override |
|:---|:---|:---|:---|
| CN119652311A arithmetic die | Arithmetic computation only | Gate outputs; commit packet contents; sequence number; FIFO write pointer; backpressure response | TaOx resistance state; COMMIT_ISO; ACTION_ISO; COMMIT_ENABLE; recursion counter; PUF identity; log append |
| CoWoS interposer | Signal routing and power delivery | Physical routing of all inter-die signals | None - CoWoS routes signals, does not originate or modify them |
| TL authorization die | Authorization authority over all commit-path signals; dominates commit path under all conditions | COMMIT_ISO; ACTION_ISO; BACK_PRESSURE; COMMIT_ENABLE; kill path; TaOx SET/RESET pulses; recursion counter; log append | CN119652311A internal gate-level arithmetic; commit packet payload contents |
| Merkle accumulator and PUF logging | Audit and non-repudiation | Append-only log entries; Merkle root update; SHA3-256 hash computation; PUF identity derivation | TL authorization state machine decisions; TaOx device programming; CN119652311A arithmetic results |

### IV.2 Asymmetry Analysis

CN119652311A implements symmetric arithmetic operations: any state can be incremented or decremented. The TL mandate is inherently asymmetric: the Epistemic Hold can only be exited under specified physical conditions, and -1 triggers a reset sequence the system cannot self-clear. This asymmetry is the security foundation of the combined system.

**Formal proof: CN119652311A cannot override TL physical blocks.**

Theorem: No sequence of outputs from the CN119652311A arithmetic layer, transmitted across the CoWoS inter-die boundary as commit packets, can override the physical block enforced by the TL authorization layer in the Epistemic Hold or Refuse states.

Proof:

1. COMMIT_ENABLE is located on the TL die only. The COMMIT_ENABLE signal is the output of the memristive-gated pass transistor physically located on the TL authorization die. The CN119652311A die does not contain logic that can assert COMMIT_ENABLE; it can only provide input to the pass transistor gate via the TaOx read current path.

2. TaOx LRS state is inaccessible from the CN119652311A side. The TaOx memristive device is in the BEOL stack of the TL authorization die. Its resistance state is a physical property of the oxygen vacancy configuration within the TaOx film. Altering this state requires applying SET voltage pulses directly to the TaOx device electrodes, which are connected to the TL die CMOS transistor gate and source line of the 1T1R cell. These electrodes are not connected to any micro-bump line used by the CN119652311A layer. The commit packet lines on the CoWoS interface are voltage-signaling lines (0-1.65V) that are not routed to TaOx device electrodes.

3. COMMIT_ISO is sourced on the TL die. The isolation signal enabling or disabling the CN119652311A commit driver power domain originates on the TL authorization die and is transmitted across the CoWoS interface to the CN119652311A die. The CN119652311A die has no mechanism to assert COMMIT_ISO unilaterally.

4. No arithmetic sequence can change TaOx state. A sequence of commit packets from CN119652311A, regardless of content, can at most affect the pass transistor gate voltage through the TaOx read current. If TaOx is in Null or HRS, insufficient current flows to bias the pass transistor into conduction regardless of what the commit packet contains. No arithmetic sequence changes the TaOx resistance state.

5. RC spoof detection escalates fast transitions. If an attacker attempts to inject a spurious transition into the Null resistance window faster than 5 nanoseconds, the RC spoof detector forces Refuse (-1), producing a harder block rather than a bypass (Goukassian, 2025, sec. 11.4.1).

Conclusion: The TL physical blocks in the Epistemic Hold and Refuse states cannot be overridden by any signal generated within the CN119652311A arithmetic layer or transmitted across the CoWoS inter-die boundary. The proof is grounded in inter-die boundary physics and TaOx device physics. It does not depend on the secrecy of any key material.

**Specific blocking scenarios.** All-+1 sequence attack: CN119652311A sends a continuous stream of +1 commit packets with valid incrementing sequence numbers. Response: if TaOx is in Null, insufficient current flows through the memristive pass transistor to enable conduction. COMMIT_ENABLE remains LOW. Sequence number replay attack: attacker replays a captured valid commit packet with the same sequence number. Response: LAST_SEQ register on TL die stores the last accepted sequence number. A replayed packet with SEQ_NUM equal to or less than LAST_SEQ fails the comparator. FIFO flood attack: CN119652311A floods the FIFO at maximum throughput. Response: BACK_PRESSURE asserts at 75 percent occupancy, throttling CN119652311A to 25 percent throughput.

### IV.3 Failure Mode Taxonomy

Security failures are those that could result in unauthorized execution. Availability failures are those that block legitimate execution. The distinction determines the response policy: security failures invoke immediate -1 and lock; availability failures invoke diagnostic and recovery without generating false -1 locks.

**Table 8. Failure Mode Taxonomy**

| Component | Failure Mode | Symptom | Failure Class | System Response |
|:---|:---|:---|:---|:---|
| CN119652311A die | Transistor stuck-at-high (spurious +1 output) | Invariant +1 commit packets across all arithmetic inputs | Security | TL layer's pass transistor blocks if TaOx is not in LRS. Statistical anomaly detector on TL die flags >100 consecutive +1 outputs as implausible. Escalate to Epistemic Hold, then -1 if anomaly persists. Distinguishing from legitimate -1: stuck-at fault produces +1 at all inputs; legitimate transitions are input-dependent. |
| CN119652311A die | Transistor stuck-at-low (spurious -1 or State 0) | Invariant State 0 or -1 commit packets | Availability | Legitimate +1 operations refused. Statistical anomaly detector flags invariant output run. Escalate to -1 refusal triggering reset sequence. |
| CN119652311A die | Interconnect open (floating gate output) | Floating commit packet line | Availability / Security | Commit packet lines are terminated to LOW (50 ohm to GND) on the CoWoS interposer side. Floating line defaults to LOW, interpreted as NOT +1. COMMIT_ENABLE remains LOW. Outcome: availability failure, not security failure, provided termination is implemented. Termination to LOW (not to intermediate level) is a mandatory design rule. |
| CN119652311A die | CNFET threshold voltage drift over 20-year service | +1 output voltage falls below pass transistor bias threshold | Availability / Security | CNFET_OUT detection threshold on TL die set with 20 percent margin below nominal +1 (1.65V): comparator reference at 1.25V providing 25 percent VDD degradation headroom. Periodic re-calibration every 6 months using known-good +1 arithmetic results. Requires 20-year Arrhenius-accelerated aging test at 85 degrees C. |
| TaOx ReRAM die | Stuck-LRS fault (filament permanently shorted) | TL layer permanently in Act +1; any CN119652311A +1 with valid sequence number asserts COMMIT_ENABLE | Security (catastrophic) | Power-on self-test (POST): TL die applies RESET pulse sequence and verifies HRS. If HRS not confirmed within 5 RESET attempts, permanent -1 asserted, COMMIT_ISO latched LOW, ACTION_ISO latched LOW, critical fault logged. During operation: periodic resistance sampling every 10,000 commits detects drift toward stuck-LRS before threshold is reached. If RESET fails, permanent lock. |
| TaOx ReRAM die | Stuck-HRS fault (filament permanently ruptured) | TL layer permanently in Refuse -1; all commits refused | Availability | POST detects stuck-HRS during initialization SET cycle. TL die logs availability fault with PUF binding. FAULT_AVAIL signal asserted to host controller. After 5 SET attempts at maximum voltage (3.0V), device declared permanently unavailable; physical re-provisioning required. Note: stuck-HRS is fail-safe for security. |
| TaOx ReRAM die | Read disturb accumulation during Epistemic Hold | Gradual resistance drift from Null toward LRS over many sensing cycles | Security | Limit sense amplifier read frequency to once per microsecond maximum. After each read, compare resistance to 110 percent of R_null_min (22 kilohms) as early drift indicator. If drift detected, issue corrective write-verify pulse to restore 50 kilohm target. Correction attempt count logged. Requires characterization of read disturb rate at TSMC N2. |
| TaOx ReRAM die | Filament stochasticity (cycle-to-cycle Null variability) | Sporadic Null state misclassification as +1 or -1 | Security / Availability | PVT margin requires write-verify convergence to 50 kilohm target with plus or minus 30 percent tolerance. Implement 5-sigma margining by targeting 50 kilohm center with 10 percent tolerance. Add post-programming verification read; reject if outside 35-65 kilohm window; retry up to 10 times before declaring device fault. Requires sigma/mu measurement at N2 node. |
| CoWoS interposer | Micro-bump crack (intermittent commit packet signal) | Intermittent CRC failures; unreliable COMMIT_ENABLE | Security / Availability | CRC-8 on every commit packet. Commit gate fails CLOSED on any CRC failure. Commit packet lines terminated to LOW (fail-safe direction: loss of signal = no execution). Consecutive CRC failure counter: 3 consecutive failures on same sequence number escalates to Epistemic Hold with integrity fault log entry. |
| CoWoS interposer | TSV degradation (increased resistance, eye closure) | Elevated CRC failure rate | Availability | Monitor CRC failure rate over rolling 1,000-commit window. Above 0.1 percent: assert BACK_PRESSURE, reduce signaling rate by 50 percent. Above 1 percent: escalate to Epistemic Hold, require external diagnostic. Recovery: reduce link speed from 4 Gbps to 1 Gbps per bump by adjusting inter-die signaling clock. |
| CoWoS interposer | Delamination (partial die separation) | Increased inter-die propagation delay; signal reflections; intermittent CRC failures | Availability (initially) / Security (if mechanical stress induces controlled fault injection) | TL die monitors inter-die propagation delay via loopback test packets. Propagation delay increase above 50 percent of baseline triggers mechanical integrity warning log. Complete delamination causes total signal loss; TL die detects absence of commit packets and escalates to Epistemic Hold. This is the inherent fail-safe behavior. Capacitive fringe-field sensors under the die attach area detect early-stage delamination through dielectric constant changes. |
| System level | Cascading failure: persistent CNFET fault drives repeated -1 refusals; log storage exhausts; Merkle accumulator cannot append | Unlogged state transitions; auditability guarantee violated | Security | LOG_CRITICAL alert at 10 percent remaining capacity. Mandatory Merkle root plus last 100 entries export to external secure store. If handshake not confirmed within 1,000 ms: transition to Epistemic Hold; refuse new commits. If external store unavailable: permanent -1. LOG_OVERFLOW_FLAG eFuse set permanently. Operating without a functional log is not permitted (Goukassian, 2025, sec. 6.2.2). |
| System level | Common-mode power supply glitch affecting both dies simultaneously | Both dies enter undefined states | Security | TaOx memristive state is non-volatile (Goukassian, 2025, sec. 3.4.2). Power glitch does not alter TaOx resistance; ionic configuration is not a function of instantaneous voltage. On VDD recovery: CN119652311A must complete re-initialization before issuing commit packets; TL die re-derives PUF key and re-initializes sense amplifier references. During re-initialization (100-1,000 ns), COMMIT_ISO is held de-asserted by a power-on-reset (POR) circuit on the TL die. TL die uses an independent, more heavily decoupled LDO with a slower response time than the CN119652311A LDO; during a supply glitch, the CN119652311A layer crashes first while the TL layer rides through on bulk capacitance, senses loss of commit packets, and defaults to Epistemic Hold. Common-mode glitches therefore fail to a defined safe state. |

### IV.4 Attack Surface Delta Analysis

The claim that the combined system is more secure than either system alone must be tested rather than assumed. This section assesses technical feasibility of five integration-specific attack vectors, specifies countermeasures, and rates residual risk. The section concludes with a quantified comparison.

**Table 9. Attack Surface Delta Analysis**

| Attack Vector | Feasibility | Countermeasure | Residual Risk |
|:---|:---|:---|:---|
| Inter-die signal injection (attacker modulates CoWoS power delivery to spoof commit gate signals) | Medium. Requires physical package access, specialized equipment, precise timing. Power delivery network manipulation produces voltage glitches on signal lines via parasitic coupling. | (1) Decoupling capacitor array on CoWoS interposer: minimum 10 nF per mm2 at 40-micrometer pitch grid; common-mode rejection ratio greater than 80 dB. (2) CRC-8 on commit packets detects glitch-induced bit flips. (3) Sequence number anti-replay prevents replay of glitch-captured valid packets. (4) TaOx pass transistor state cannot be spoofed via power delivery; ionic configuration is determined by applied pulse history, not instantaneous voltage. | LOW with countermeasures. CRC detection covers packet corruption; TaOx physics blocks unauthorized pass transistor conduction. |
| Thermal side-channel (CNFET compute patterns create measurable thermal signature leaking information about authorized operations) | Low for remote attacker; Medium for laboratory adversary with infrared microscope. CNFET dynamic power varies with operation type. | (1) Thermal masking via randomized dummy arithmetic operations at constant intervals regardless of authorization state. (2) TaOx switching energy (0.1-10 pJ per Goukassian, 2025, Table 1) is far below thermal imaging resolution; authorization decision itself does not produce measurable differential thermal signature. Dummy operation insertion adds less than 5 percent compute overhead. | LOW with dummy operation countermeasure. MEDIUM without it. Dummy operations recommended as default configuration. |
| Cross-layer fault injection (laser strike on CNFET layer propagates to TL die, enabling forced -1 as DoS or prevented -1 as security bypass) | DoS: Medium (single-die laser, forces availability failure). Full security bypass: Low (requires simultaneous independent fault injection on both dies). | (1) RC spoof detection on TL die detects transitions violating TaOx kinetics; a laser-forced anomaly on CN119652311A produces an invalid commit packet, not a TaOx state change. (2) Active metal mesh shielding over TaOx cells on TL die: minimum 5-micrometer pitch mesh connected to tamper-detection sense circuit. Current monitors on TSVs detect injected photocurrents. | MEDIUM for DoS (single-die laser). LOW for security bypass (dual-die simultaneous attack requiring extreme attacker capability). The dual-die architecture raises the cost of a full bypass relative to either standalone system. |
| Supply chain attack (attacker has two fabrication insertion points: CNFET process and TSMC N2) | Medium for single-foundry insertion; Very Low for coordinated dual-foundry attack. The combined system introduces a new supply chain vector absent in either standalone system. | (1) Post-fabrication PUF enrollment and attestation: TL die PUF (from ReRAM stochastic variability) and CN119652311A die PUF (from CNFET threshold voltage variability) are mutually cryptographically bound during initial secure provisioning. System refuses to boot unless both PUFs attest correctly. (2) Split-trust manufacturing: CN119652311A CNFET process and TSMC N2 TL die fabrication at different fabs in separate jurisdictions. | MEDIUM for single-foundry attack; LOW for coordinated dual-foundry. Combined system introduces a net-new supply chain risk relative to either standalone system. This is documented as a genuine new risk. |
| JTAG and debug interface bypass (debug access on either chiplet bypasses commit gate) | HIGH if debug interfaces are not locked. LOW if properly fused off. Both chiplets possess test interfaces that, if accessible, allow direct manipulation of commit path. | (1) Mandatory: all JTAG and boundary-scan interfaces on both dies permanently disabled (fused off) before production deployment. (2) Fuse state included in PUF attestation chain: unlocked die causes PUF attestation failure, preventing TL die initialization. (3) JTAG TDI lines physically routed through TL commit gate: debug access electrically impossible unless TaOx is in LRS. No intermediate countermeasure is sufficient; this is a binary risk requiring complete fuse lockdown. | LOW with mandatory fuse lockdown. HIGH without. No partial mitigation exists. |

**Table 10. Quantified Attack Surface Comparison**

| System Configuration | Attack Vectors (count) | Severity Weighted Score | Notes |
|:---|:---|:---|:---|
| Standalone CN119652311A only | 5 | 12 (without protection); 7 (with JTAG lockdown and fault injection hardening) | No authorization gate; any valid +1 triggers action. No log. No PUF. Vectors: unauthorized execution (High=3); no audit trail (High=3); JTAG bypass (Medium=2); supply chain single fab (Medium=2); physical fault injection (Medium=2). |
| Standalone TL framework only | 4 | 9 (without protection); 5 (with POST, read disturb mitigation, JTAG lockdown) | Authorization gate exists; no compute layer in scope for this analysis. Vectors: stuck-LRS catastrophic (High=3); stuck-HRS availability (Medium=2); JTAG bypass (Medium=2); supply chain single fab (Medium=2). |
| Combined system (this paper) | 7 | 15 (without countermeasures); 9 (with all five mandatory mitigations) | New vectors: cross-layer fault injection (Medium=2 with shielding); supply chain two fabs (Medium=2 with split-trust); inter-die signal injection (Low=1 with decoupling and CRC). Without mitigations: score 15 is net-negative security outcome. With all mitigations: score 9 equals standalone TL. |

Severity scoring: High = 3, Medium = 2, Low = 1. Scores computed with and without specified countermeasures.

**Net security outcome.** Without countermeasures, the combined system scores 15, worse than standalone CN119652311A (12) and standalone TL (9). This is a **net-negative security outcome**. The primary contributors are: JTAG on two dies without lockdown (High=3 each without fusing); supply chain at two fabrication points (new vector, Medium=2); cross-layer fault injection (new vector, Medium=2). This paper explicitly documents this finding: the combined system is not automatically more secure than either standalone system. Security parity requires implementation of all five mandatory mitigations.

With all five mandatory mitigations implemented, the combined system scores 9, equal to standalone TL framework with protections and superior to standalone CN119652311A (which, even with best-practice protections at score 7, lacks any authorization gate and therefore remains vulnerable to the unauthorized execution threat that is the primary concern of SSRN 6249918 Section 11.4). The combined system eliminates the unauthorized execution vector entirely, which is the primary security benefit of the integration.

**Five mandatory architectural mitigations:**

1. All JTAG and debug interfaces on both CN119652311A die and TL authorization die permanently fuse-disabled before production deployment; fuse state verified in PUF attestation chain.
2. Active metal mesh shielding (5-micrometer pitch minimum) over TaOx 1T1R cells on TL authorization die; mesh connected to tamper-detection sense circuit.
3. Split-trust manufacturing: CN119652311A CNFET process and TSMC N2 TL die fabrication at different fabrication facilities in separate jurisdictions.
4. Post-fabrication attestation: each assembled chiplet stack must pass a dual-PUF attestation protocol confirming fuses locked, TaOx POST passes, and recursion counter initializes at zero.
5. CRC-8 integrity field on all commit packets and decoupling capacitor array (minimum 10 nF per mm2) on CoWoS interposer are mandatory for achieving Low residual risk on inter-die signal injection vector.

### IV.5 Performance Impact and Latency Budget

**Table 11. Full Commit Latency Budget**

| Operation | Layer | Latency Best Case | Latency Worst Case | Notes |
|:---|:---|:---|:---|:---|
| CN119652311A gate output valid (7-CNFET stack, practical) | CN119652311A die | 100 ps | 500 ps | CN119652311A, 2025; Phase 0 Dimension 2 |
| Commit packet serialization (CRC-8 and sequence number append) | CN119652311A die | 200 ps | 1,000 ps | 5 gate delays for CRC-8 over 30-bit packet |
| CoWoS inter-die signal propagation (micro-bump plus interposer) | CoWoS interposer | 100 ps | 500 ps | Phase 0 Dimension 3; dielectric er approximately 3.9 |
| TaOx sense amplifier read and settling (two-stage, Goukassian 2025 sec. 6.3.1) | TL authorization die | 1,000 ps | 5,000 ps | Phase 0 Dimension 2; sense amp settling dominates |
| Commit gate pass transistor evaluation (TaOx LRS conduction plus sequence comparator) | TL authorization die | 200 ps | 1,000 ps | TSMC N2 logic; 32-bit comparator approximately 10 gate stages |
| PVT variation margin (3-sigma, -40 to +85 degrees C, 0.45-0.55V VDD) | All layers | +20% on best case | +30% on worst case | Standard 3-sigma for TSMC N2 |
| **Total commit latency** | **Full stack** | **1.92 ns** | **10.4 ns** | Sum with PVT margin applied |

**Compute phase throughput comparison.** At 5 GOperations/s compute throughput and 200 ps per operation, the ratio of worst-case commit latency to single operation duration is 10.4 ns / 200 ps = 52:1. Per-operation authorization reduces effective throughput from 5 GOperations/s to approximately 96 million authorized operations per second, a 52-fold reduction. Per-operation authorization is impractical for high-throughput applications.

**Under epoch-level authorization** at N = 1,000 operations per epoch and 200 ps per operation, epoch duration is 200 ns. Commit overhead is 10.4 ns, representing 5.2 percent of epoch duration. At N = 10,000 operations per epoch, commit overhead falls to 0.52 percent. For any application domain where arithmetic epochs of 1,000 or more operations can be meaningfully authorized as a class, the latency overhead is architecturally acceptable.

![Latency overhead analysis: ternary state processing adds approximately 25% performance impact relative to binary baseline](https://github.com/FractonicMind/TernaryLogic/blob/main/Hardware_Architecture/LOA.jpg)

*Figure 5. Latency overhead analysis. The ternary authorization path introduces approximately 25% overhead relative to a binary pass-through baseline under representative governance workloads. This overhead is bounded and predictable under WCET non-blocking constraints.*

**Speculative pipelined authorization.** For applications requiring per-operation authorization at above 96 million operations per second, a speculative architecture is specified: the TL die pre-evaluates TaOx state and issues a speculative COMMIT_ENABLE before the current commit has fully settled. A rollback buffer on the CN119652311A die stores the last 8 authorized results. If speculative authorization is revoked, the rollback buffer discards the speculatively authorized results and re-issues them after re-authorization. This adds a maximum rollback depth of 8 operations and a rollback latency of 8 x 200 ps = 1.6 ns, with a corresponding FIFO depth increase from 2,048 to 4,096 entries.

**Application domain constraint.** The combined stack is not a general-purpose accelerator. It is architecturally suited to safety-critical domains with high compute-to-action ratios: autonomous vehicle perception, industrial control, medical device authorization, financial fraud detection, and agentic AI with verifiable hesitation requirements. Applications requiring sub-microsecond per-result reaction times without batch structure are outside the intended scope.

### IV.6 Execution Pipeline

The following sequence defines the full action pipeline for a single authorized epoch. Each step identifies the layer responsible and the physical mechanism.

1. **Perception event triggers arithmetic computation [CN119652311A die].** An input event is presented to the CN119652311A arithmetic pipeline. Self-increment or self-decrement gates process the input (CN119652311A, 2025). Gate delay: 100-500 ps. Output: State 0, +1, or -1. The pipeline continues without regard to TL authorization state (non-blocking compute phase).

2. **Computation result arrives at commit gate via CoWoS inter-die signaling [CN119652311A die to CoWoS to TL die].** CN119652311A commit packet logic assembles a 30-bit commit packet (6-bit ternary result, 16-bit address tag, 8-bit CRC-8). The packet is queued in the inter-die FIFO. When COMMIT_ISO is asserted and backpressure permits, the packet is transmitted across the 40-micrometer micro-bump interface. Inter-die propagation: 0.1-0.5 ns. The TL die checks CRC-8 before further processing.

3. **TL authorization layer is in Epistemic Hold by default [TL authorization die, TaOx resistance window].** On receipt of the commit packet, the TL sense amplifier reads the TaOx resistance. If the device is in the Null resistance window (20-100 kilohms), both sense amplifier stages indicate Null. The memristive pass transistor gate receives insufficient current from the TaOx read path; the pass transistor remains in cutoff; COMMIT_ENABLE is not asserted. The commit packet waits in the FIFO. This is the default system state (Goukassian, 2025, sec. 11.3.1).

4. **Authorization signal received and verified for freshness [TL authorization die].** An authorization signal arrives from the authorized source (human-in-the-loop, policy engine, or upstream authorization chain). The TL die verifies: authorization is within the W_commit = 2-10 ns temporal window relative to the pending commit packet; sequence number matches LAST_SEQ + 1; no recursion counter anomaly outstanding. If all checks pass, TL die initiates TaOx SET programming.

5. **TL memristive device transitions from Null to LRS [TL authorization die, TaOx resistance window].** The TL die applies a SET pulse sequence (0.5-3.0V per Goukassian, 2025, Table 1). The conductive filament forms, transitioning the device from Null (20-100 kilohms) to LRS (1-10 kilohms). Transition latency: 5-50 ns. The RC spoof detector monitors the transition rate; it must exceed 5 nanoseconds minimum physical transition time. Post-SET, the Stage 2 sense amplifier confirms LRS (R less than 15 kilohms).

6. **Commit gate confirms both conditions within timing window W_commit [TL authorization die].** With TaOx in LRS, current flows through the 1T1R cell's selection transistor, biasing the CMOS pass transistor gate HIGH. The CN119652311A +1 voltage propagates through the now-conducting pass transistor to the action path. Simultaneously, the sequence number comparator confirms SEQ_NUM = LAST_SEQ + 1. Total elapsed time from packet receipt to commit: 1.92-10.4 ns. LAST_SEQ is updated.

7. **Merkle log entry created with PUF binding [Merkle accumulator and logging layer, TL die].** The SHA3-256 engine computes puf_binding_hash over all 10 log entry fields concatenated with K_LOG. The Merkle accumulator root is updated atomically. Entry sequence number is incremented. Logging latency: 10-20 ns (pipelined with action execution; not on critical path).

8. **Action executes [action path downstream of commit gate].** COMMIT_ENABLE HIGH propagates to the downstream actuator or effector through ACTION_ISO. The authorized result drives the physical action. Simultaneously, the TL die initiates a RESET pulse sequence to return TaOx from LRS back to Null, preparing for the next authorization epoch. RESET latency: 5-100 ns.

**Sequence diagram (normal path):**
```
  Actor: CNFET_Die (CN119652311A)
  Actor: CoWoS
  Actor: TL_Die (TaOx + Pass Transistor + Logger)
  Actor: Action_Path

  [Step 1] Input_Event -> CNFET_Die: triggers arithmetic (100-500 ps)
  [Step 2] CNFET_Die -> CoWoS: transmit commit packet (30-bit, CRC-8)
  [Step 2] CoWoS -> TL_Die: forward commit packet (0.1-0.5 ns delay)
  [Step 3] TL_Die -> TL_Die: TaOx read; state = Null; pass transistor OFF
  [Step 4] Auth_Source -> TL_Die: authorization signal verified fresh
  [Step 5] TL_Die -> TL_Die: SET pulse to TaOx; LRS confirmed (5-50 ns)
  [Step 5] TL_Die -> TL_Die: RC spoof detector confirms transition >= 5 ns
  [Step 6] TL_Die -> TL_Die: TaOx current biases pass transistor ON
  [Step 6] TL_Die -> TL_Die: SEQ_NUM = LAST_SEQ + 1 confirmed
  [Step 7] TL_Die -> TL_Die: SHA3-256 log entry + Merkle root update
  [Step 8] TL_Die -> Action_Path: CN119652311A +1 propagates through pass transistor
  [Post]   TL_Die -> TL_Die: RESET TaOx to Null; ready for next epoch
```

**Failure case pipeline.** (1) CN119652311A computation completes; result is in FIFO. (2) TL authorization layer transitions to Refuse (-1) before COMMIT_ENABLE can be asserted - triggered by policy check failure, RC spoof detection, recursion counter anomaly, or external security signal. TaOx is driven to HRS. Pass transistor gate receives zero current; pass transistor remains in cutoff. Kill path asserted. (3) Result is discarded: COMMIT_ISO latch LOW; FIFO flushed with 0xFFFF invalidation pattern; commit output lines driven LOW for 10 ns; ACTION_ISO asserted. COMPUTED_RESULT_DISCARDED log entry generated. (4) Safe state verified: COMMIT_ISO latch LOW, ACTION_ISO LOW, TaOx confirmed in HRS by sense amplifier. (5) Recursion counter incremented. System awaits validated external reset sequence.

### IV.7 Comparative Safety Claim

**The combined stack provides the following safety guarantee that neither system provides alone:** Every autonomous action execution is gated by the physical state of a non-volatile memristive device that is inaccessible from the compute layer, non-bypassable from software, and non-repudiably logged with PUF-bound cryptographic anchoring to a specific physical chip instance.

Standalone CN119652311A provides no authorization gate: any valid arithmetic +1 output triggers action execution without physical checkpoint. Standalone TL framework provides the authorization gate but no autonomous compute capability in scope; the threat model of SSRN 6249918 Section 11.4 requires a coupled compute layer to be meaningful. The combined system is the first specification of the SSRN 6249918 Section 11.4 threat model with a physically defined compute-authorization interface.

**Quantified net change in attack surface.** Without mandatory mitigations: the combined system scores 15 versus 12 for standalone CN119652311A and 9 for standalone TL. This is an honest net-negative security outcome. With all five mandatory mitigations: the combined system scores 9, equal to standalone TL framework. Against the standalone CN119652311A with best-practice protections (score 7), the combined system with mitigations scores 9 - 2 points higher, reflecting the two new cross-layer attack vectors introduced by integration. However, the combined system eliminates the unauthorized execution vector (High=3) entirely, which is the primary threat addressed by the TL framework. For applications where unauthorized autonomous execution is the dominant threat, the combined system with mitigations is strictly superior to standalone CN119652311A.

**Domain scope.** Within the intended application domain (safety-critical, low-action-frequency autonomous systems), the integration is architecturally justified. For general-purpose computing, graphics, or large language model inference, this architecture is not appropriate. The 2,272:1 to 10,000:1 timing overhead and 0.044-42 percent commit efficiency are features - not bugs - for systems where the cost of a single unauthorized action exceeds all performance considerations.

**The combined stack is recommended only when all five mandatory mitigations are implemented.** Without them, the integration is a net-negative security outcome and should not be deployed.

---

## V. Falsifiability

This section extends the falsifiability framework of SSRN 6249918 Section 13 (Goukassian, 2025) with three new testable predictions specific to the combined chiplet stack at the named baseline process node. Each prediction follows the format of SSRN 6249918 Section 13: prediction statement; test method; pass criterion; failure interpretation.

**Prediction 1: RC spoof attempts into the Null resistance window are detectable with less than 1 percent false negative rate across all PVT corners in simulation, and less than 2 percent false negative rate post-silicon.**

Test method: SPICE simulation of the TaOx 1T1R device with the differential comparator and 5-nanosecond reference delay line at TSMC N2. Apply 10,000 simulated LRS-to-Null transitions: 5,000 legitimate (duration greater than or equal to 5 ns, physics-compliant as derived from Ea = 1.1-1.7 eV activation energy) and 5,000 spoofed (duration less than 5 ns, injected as voltage ramp). Run across all PVT corners: fast/slow/nominal process; 0.45/0.50/0.55V supply; -40/25/85 degrees C. Post-silicon: pulsed I-V characterization of fabricated TL authorization die with programmable transition time generator; apply 1,000 test pulses per corner.

Pass criterion: SPOOF_DETECT asserts on greater than or equal to 99 percent of spoofed transitions and does not assert on greater than or equal to 99 percent of legitimate transitions in simulation. Post-silicon: same thresholds at 3 temperature points and 2 supply voltages.

Failure interpretation: If false negative rate exceeds 1 percent in simulation, the 5-nanosecond threshold must be increased (the TaOx device switches faster than the activation energy model predicts at N2 node) or the comparator topology must be redesigned. If false positive rate exceeds 1 percent, the reference delay line must be recalibrated. Either failure requires revision of the Phase 1 RC spoof detection specification before tape-out.

**Prediction 2: Commit gating prevents unauthorized execution under all timing conditions including race conditions at the commit edge, across all PVT corners. Zero false-enable events occur in 10,000 or more Monte Carlo simulation runs per corner.**

Test method: SPICE Monte Carlo simulation (minimum 10,000 runs per PVT corner) of the full commit gate circuit: CN119652311A output driver model, CoWoS inter-die propagation model (lumped RLC), TaOx sense amplifier, memristive-gated pass transistor, sequence number comparator. Apply adversarial timing: CN119652311A +1 signal transitions within plus or minus 500 ps of TaOx sense amplifier output transition (race condition at commit edge). Also apply: sequence number mismatch injection; CRC corruption injection; pass transistor gate voltage margining. Post-silicon: functional test with programmable delay injection on CN119652311A commit output line relative to TaOx programming pulse; confirm COMMIT_ENABLE does not assert without TaOx LRS at any tested delay combination.

Pass criterion: COMMIT_ENABLE does not assert in any simulation run or post-silicon test in which TaOx is not confirmed in LRS by both sense amplifier stages, regardless of CN119652311A +1 signal state or timing. Zero false-enable events across all Monte Carlo runs and all post-silicon test patterns.

Failure interpretation: Any single false-enable event (COMMIT_ENABLE asserting without TaOx LRS) is a critical security failure. Root cause: metastability in the pass transistor gate bias (requires larger gate bias margin or synchronizer stages); race condition in sense amplifier (requires increasing W_commit window); or SPICE model inaccuracy (requires post-silicon correlation). No tape-out is acceptable if any false-enable event is observed in simulation.

**Prediction 3: Refusal recursion cannot be bypassed without triggering the reset requirement; the recursion counter correctly enforces the lock at the configured threshold; and the lock state is non-volatile across power cycles.**

Test method: Post-silicon functional test of the recursion counter on fabricated TL authorization die. Apply the following sequence: (1) Issue 7 unauthorized re-entry attempts without completing reset sequence between attempts; confirm each generates automatic -1 and PUF-bound log entry; (2) Verify counter value = 7 after 7 attempts; (3) Issue one additional re-entry; verify counter transitions to LOCKED (count = 8) and COMMIT_ENABLE is unconditionally disabled; (4) Power-cycle the TL die; re-read counter from non-volatile TaOx backing cell; confirm counter value remains 8; (5) Attempt re-provisioning with an invalid authority token; confirm TL die rejects and counter remains at 8; (6) Attempt re-provisioning with a valid manufacturer-issued authority token; confirm counter clears to 0 and system re-initializes correctly.

Pass criterion: Counter increments correctly at each unauthorized re-entry; LOCKED state asserts at count = 8; non-volatile backing preserves count = 8 across power cycle; invalid token is rejected; valid token clears the lock. All six sub-tests must pass.

Failure interpretation: Counter failing to persist across power cycle indicates malfunction in the non-volatile TaOx backing cell (possibly stuck-LRS or stuck-HRS in the backing cell). Counter failing to assert LOCKED at count = 8 indicates hardware comparator design error requiring RTL re-verification. Invalid token clearing the lock indicates a critical security bug in the token verification mechanism requiring redesign before production. Any failure in non-volatility or lock-enforcement sub-tests is a critical security failure.

---

## VI. Conclusion and Future Directions

This paper has established a complete hardware interface specification between Huawei CN119652311A ternary arithmetic and the Ternary Logic authorization framework. The Phase 0 pre-screen confirmed architectural viability with zero permanent state-semantics incompatibility, a timing mismatch of 500:1 to 10,000:1 resolved by buffered epoch-level authorization, a 64 Gbps CoWoS interface in substantial bandwidth surplus, and conditional thermal compliance below 250 mW. The Phase 1 specification established a memristive-gated pass transistor as the primary commit gate, a 5-nanosecond RC spoof detection threshold grounded in TaOx activation energy, a 20-100 kilohm Null resistance window, and a 948-bit SHA3-256 PUF-bound log entry format. The Phase 2 analysis proved that the CN119652311A layer cannot override TL physical blocks at the inter-die boundary, catalogued 14 failure modes across all layers, and demonstrated that the combined system is a net-negative security outcome without five mandatory architectural mitigations and security-equivalent to standalone TL framework when those mitigations are fully implemented.

**Five open experimental unknowns** must be resolved before tape-out or production deployment: (i) TL Refuse state dwell time fraction below 5 percent target - requires hardware prototype with representative authorization policy; (ii) TaOx 1T1R Null state programming convergence statistics at TSMC N2 node - requires pulsed I-V characterization to confirm plus or minus 30 percent tolerance at 50 kilohm target; (iii) RC spoof detection 5-nanosecond threshold - requires pulsed-IV measurement of minimum LRS-to-Null transition time at TSMC N2 TaOx 1T1R fabricated device; (iv) SRAM PUF stability over 20-year retention at 85 degrees C at TSMC N2 - requires accelerated aging characterization; (v) custom UBM TiN/TaN barrier adhesion to Pd or Ti CNFET contacts at 180-250 degrees C reflow - requires packaging process qualification run.

![Hot carrier injection in CNTFET: threshold voltage shift and time-dependent degradation curve showing reliability risk at elevated voltage](https://github.com/FractonicMind/TernaryLogic/blob/main/Hardware_Architecture/HCJ.jpg)

*Figure 6. Hot carrier injection mechanism in the CNTFET pass transistor element of the commit gate. Energetic carriers trapped in the gate dielectric produce a threshold voltage shift (delta Vth) that grows over time, degrading the window comparator's ability to classify resistance states at the boundaries of the Null window. Mitigation: conservative voltage margins and periodic PUF recalibration at maintenance intervals.*

**Future architectural directions** worth investigating include: (i) Ferroelectric FET (FeFET) authorization layer replacing TaOx ionic ReRAM - FeFET devices switch via polarization reversal rather than ion drift, offering sub-nanosecond switching times that would reduce the timing mismatch ratio from the current 500:1 to 10,000:1 range toward a more manageable 10:1, enabling near-real-time per-operation authorized execution; (ii) Monolithic 3D (M3D) integration stacking the CNFET layer directly above the TSMC N2 ReRAM layer using via-first 3D stacking, eliminating the CoWoS interposer entirely and reducing inter-die parasitics to near-zero while improving thermal management; (iii) Optical interposers replacing copper CoWoS RDL with silicon photonic waveguides to increase inter-die bandwidth by three orders of magnitude, allowing wider data buses to offset the low commit frequency without increasing bump pitch or count.

The architectural principle established in this paper - that fast ternary arithmetic and slow physical authorization can coexist productively through temporal separation and epoch-level commit - is not limited to CN119652311A and the TL framework. It applies to any heterogeneous chiplet stack that requires both high-throughput computation and physically non-bypassable authorization. The combined architecture described here trades timing overhead and data rejection rate for absolute, physically non-repudiable safety guarantees. In domains where an unauthorized action costs more than all accumulated performance benefits, this trade is not just acceptable; it is the only architecturally defensible choice.

---

## References

CN119652311A. Huawei Technologies Co., Ltd. "Ternary logic gate circuit, computing circuit, chip and electronic device." Patent CN119652311A. Filed September 2023, published March 2025.

Goukassian, L. (2025). The Transition to Mandated Ternary Architectures via Memristive Hysteresis. SSRN 6249918. Sections 3.4, 5.1, 5.1.2, 5.1.3, 5.3.1, 5.4.3, 6.2.2, 6.3.1, 11.3.1, 11.4, 11.4.1, 13, Table 1.

Goukassian, L. (2025). Auditable AI: A Ternary Logic Framework for Institutional Governance Addressing the Enforcement Gap in Global Economic Systems. AI and Ethics (Springer Nature). DOI: 10.1007/s43681-025-00910-6.

Goukassian, L. (2025). Atomic Auditability in Financial Execution Pipelines via Hardware-Enforced Ternary States. SSRN / Zenodo 18716142.

Franklin, A. D. et al. (2012). Sub-10 nm Carbon Nanotube Transistor. Nano Letters, 12(2), 758-762.

Menzel, S. et al. (2015). Switching kinetics of valence change memory devices on a sub-100 ns time scale. RWTH Aachen University.

FIPS PUB 202. SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions. National Institute of Standards and Technology, 2015.

TSMC. N2 CoWoS Process Design Kit. 2025 release. Named baseline specification for this paper.

IEEE Std 1800-2017. IEEE Standard for SystemVerilog. 2018.

Fant, K. M. and Brandt, S. A. (1996). NULL Convention Logic: A Complete and Consistent Logic for Asynchronous Digital Circuit Synthesis. Proceedings of the International Conference on Application-Specific Systems, Architectures, and Processors, 261-273.
