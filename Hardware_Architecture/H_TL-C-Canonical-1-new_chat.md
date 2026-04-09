# **Hardware-Enforced Authorization Interface Between Huawei CN119652311A and the Ternary Logic Framework**

**Author:** Lev Goukassian **ORCID:** [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243) **Repository:** [github.com/FractonicMind/TernaryLogic](https://github.com/FractonicMind/TernaryLogic) / Hardware\_Architecture/ **Submission target:** SSRN (first release) **Date:** April 2026

---

## **Abstract**

Huawei patent CN119652311A discloses a ternary arithmetic processing unit implemented using self-incrementing and self-decrementing circuits constructed from seven carbon nanotube field-effect transistors (CNFETs) with three distinct threshold voltages. The unit operates across three voltage-mapped output states: 0V (State 0 / neutral arithmetic zero), 1.65V (State \+1 / Commit), and 3.3V (State \-1 / Refuse). The Ternary Logic (TL) framework requires that no consequential action may proceed without a cryptographically attested, hardware-logged authorization signal anchored to a physical non-volatile state.

These two systems share a state vocabulary but are unconnected in enforcement: CN119652311A can produce a Commit-valued arithmetic output while the TL enforcement layer remains uninformed and unpowered. This paper specifies the hardware-enforced authorization interface that closes that gap.

The interface is specified across four compatibility dimensions (state semantics, timing domain, information-theoretic throughput, and thermal-mechanical stability), followed by a full Phase 1 circuit-level specification covering the commit gate architecture, the Null resistance window, RC spoof detection, immutable log format, halt signal implementation, and recursion counter. The canonical fabrication baseline is TSMC N2 CoWoS ReRAM 1T1R 2025 PDK with Arrhenius 20-year retention at 85 degrees C.

The central security finding is honest and must not be softened: the integrated system is net-negative relative to standalone TL if any of five mandatory mitigations are absent. With all five present, the combined system is net-equal in severity-weighted attack score to standalone TL and strictly superior to standalone CN119652311A against the unauthorized-execution threat model. Five open experimental unknowns bound the falsifiable claims and define the silicon validation agenda.

**Application domain constraint:** this architecture is not a general-purpose accelerator. It is designed for safety-critical, low-action-frequency domains where an unauthorized physical action is strictly more catastrophic than a delayed authorized one.

---

## **Terminology Rule**

Precision in state naming is mandatory across all layers of this analysis. At the CN119652311A arithmetic layer, the zero-valued ternary output is referred to as **State 0**. At the TaOx physical resistance layer, the intermediate resistance condition is referred to as **Null**. At the TL authorization and governance layer, the decision-pending state is referred to as **Epistemic Hold**. These three terms refer to distinct physical and logical constructs at different levels of the stack and are never conflated under any circumstances.

---

## **1\. CN119652311A Voltage-State Mapping**

The CN119652311A patent specifies three output voltage levels directly corresponding to its three arithmetic states. These voltage specifications, confirmed from the Chinese patent record, establish the electrical basis for the interface design:

| Voltage | CN119652311A State | TL Authorization Mapping |
| ----- | ----- | ----- |
| 0V | State 0 (neutral arithmetic zero) | Epistemic Hold 0 (at commit boundary) |
| 1.65V | State \+1 (self-increment positive result) | Act \+1 / Commit (LRS) |
| 3.3V | State \-1 (self-decrement negative result) | Refuse \-1 (HRS) |

The seven-CNFET stack operates with three distinct threshold voltages to discriminate these levels. At a 3.3V supply domain, the signal characteristics are: voltage level 1.65V ± 10% for State \+1, noise margin approximately 200 mV separation from State 0 (0V) and State \-1 (3.3V), rise and fall times below 100 ps limited by interconnect RC, and drive strength sufficient for CoWoS inter-die signaling with 50 fF load.

At lower supply domains (0.5V, as used in some CNFET configurations), these levels scale proportionally. The interface design must accommodate level shifting as specified in Section 3.4.

---

## **Phase 0: Architectural Compatibility Pre-Screen**

This phase evaluates whether these two systems share sufficient semantic and physical compatibility to justify integration. If any dimension reveals a fundamental showstopper, this report halts here.

### **Dimension 1: State Semantics Alignment**

**State transition mapping**

Table 1 maps every identifiable CN119652311A gate-level transition onto the TL authorization state machine. An operation is classified as permanently blocked only if the TL framework offers no path to execution under any authorization condition. An operation deferred during Epistemic Hold but eventually permitted under Proceed is classified as buffered, not blocked.

*Table 1\. Complete mapping of CN119652311A gate-level state transitions onto TL authorization states. Compatibility status: Compatible \= fully aligned; Buffered \= deferred, not permanently blocked; Conditionally blocked \= blocked during Refuse state only (transient condition).*

| CN119652311A State Transition | Corresponding TL Authorization State | Compatibility Status | Notes |
| ----- | ----- | ----- | ----- |
| State 0 \-\> State \+1 (self-increment, zero-to-positive) | Act \+1 (Proceed) | Compatible | Gate-level arithmetic transition executes freely when TL authorization layer is in Proceed state. No structural conflict. |
| State \+1 \-\> State \+1 (identity hold, high) | Act \+1 (Proceed) or Epistemic Hold 0 | Compatible | Identity transition generates no result commit. Authorization layer remains uninvolved. |
| State \+1 \-\> State 0 (self-decrement, positive-to-zero) | Act \+1 (Proceed) | Compatible | Decrement operation symmetric to increment. Gate-level physics identical; TL layer involvement only at commit boundary. |
| State 0 \-\> State \-1 (self-decrement, zero-to-negative) | Act \+1 (Proceed) | Compatible | Underflow-adjacent decrement proceeds normally under Proceed authorization. Arithmetic State 0 does not map to TL Epistemic Hold; terminology is strictly layer-specific. |
| State 0 \-\> State 0 (identity hold, zero) | Act \+1 (Proceed) or Epistemic Hold 0 | Compatible | No-operation; outputs unchanged. Compatible with all TL states. No commit issued; authorization not queried. |
| State \-1 \-\> State \-1 (identity hold, negative) | Act \+1 (Proceed) or Epistemic Hold 0 | Compatible | Identity transition generates no result commit. Compatible in all TL states. |
| Compound operation: increment-then-decrement (net-zero round trip) | Act \+1 (Proceed) | Compatible | Round-trip produces net State 0 output. Single commit at operation boundary. No phantom Epistemic Hold invocation. |
| Any transition during TL Epistemic Hold state | Epistemic Hold 0 | Buffered, not blocked | CN119652311A arithmetic continues executing internally. Results accumulate in inter-die FIFO buffer. Commit deferred until TL layer exits Epistemic Hold. |
| Any transition during TL Refuse state | Refuse \-1 | Conditionally blocked (rollback required) | Result commit rejected. Arithmetic layer signaled to discard buffered results. Refuse state is transient; resolves to Epistemic Hold 0 upon escalation. Estimated fraction of operational time in Refuse state: typically less than 5% (requires experimental validation). |
| Carry-out requiring multi-cycle propagation | Act \+1 (Proceed) | Compatible | Multi-stage chains within CN119652311A are purely arithmetic. TL authorization queried only at epoch or commit boundaries, not at every gate cycle. |

**Analysis and incompatibility calculation**

Of the ten transition types enumerated in Table 1, zero are permanently blocked by the TL authorization framework. The Refuse state (-1) blocks commits during its active duration, but this state is transient by architectural definition: the Epistemic Hold 0 is the mandatory intermediate state through which the system passes, and the Refuse state resolves to Epistemic Hold 0 upon escalation or policy review.

A critical semantic distinction resolves an apparent conflict: the term State 0 at the CN119652311A arithmetic layer designates the zero-valued ternary arithmetic output, which is a pure data value. The term Epistemic Hold 0 at the TL authorization layer designates the authorization-pending condition of the memristive commit gate. These describe phenomena at different levels of the stack.

Incompatibility percentage (permanent block): **0%** Incompatibility percentage (conditional, Refuse state duration): **\<5%**, requiring experimental confirmation.

Both figures are below any reasonable threshold for halting. **This dimension passes.**

---

### **Dimension 2: Timing Domain Mismatch**

**CNFET switching speed analysis**

The CN119652311A self-increment and self-decrement gates are constructed from seven CNFETs with three distinct threshold voltages. CNFET device physics places the intrinsic gate switching delay in the range of 10-50 picoseconds at advanced node geometries under ballistic transport conditions. Academic simulations of highly similar seven-transistor multi-threshold CNFET ternary gates demonstrate propagation delays ranging from 22 ps at fan-out of 1 to 73 ps at FO4 at 0.9V supply. For a seven-transistor stack with series-connected threshold-voltage-encoded logic, the practical propagation delay accounts for fanout loading and interconnect RC, yielding 100-500 ps per gate operation.

**ReRAM write and read latency**

TaOx RRAM write energy is in the range of 0.1-10 pJ per operation at an operating voltage of 0.5-3.0V. Switching latency is bounded by the energy-pulse-width product. For binary (LRS or HRS) transitions: 5-50 ns. Stable programming of the intermediate Null state requires an iterative write-verify sequence, taking 50-500 ns per iteration. Multi-cycle convergence under high device variability may extend worst-case Null programming latency to 1-5 microseconds.

**Timing table**

*Table 2\. Timing budget for all relevant operations across CN119652311A arithmetic layer, TaOx resistance window layer, and TL authorization layer.*

| Operation | Layer | Latency (best case) | Latency (worst case) |
| ----- | ----- | ----- | ----- |
| Single 7-CNFET gate switching (ballistic) | CN119652311A | 10 ps | 50 ps |
| Single 7-CNFET gate switching (practical, parasitics) | CN119652311A | 100 ps | 500 ps |
| TaOx 1T1R SET (LRS) | TaOx | 5 ns | 50 ns |
| TaOx 1T1R RESET (HRS) | TaOx | 5 ns | 100 ns |
| TaOx 1T1R Null (single write-verify) | TaOx | 50 ns | 500 ns |
| TaOx 1T1R Null (multi-cycle, worst variability) | TaOx | 200 ns | 5,000 ns |
| TaOx 1T1R read (sense amplifier) | TaOx | 1 ns | 5 ns |
| TL authorization: Epistemic Hold entry/exit | TL | 5 ns | 500 ns |
| TL authorization: commit gate decision | TL | 10 ns | 5,000 ns |
| CoWoS inter-die micro-bump propagation (40 um) | CoWoS | 0.1 ns | 0.5 ns |

**Mismatch ratio calculation**

Best-case ratio: 50 ns (Null, single cycle) / 100 ps (CNFET, practical) \= **500:1** Worst-case ratio: 5,000 ns (Null, high variability) / 500 ps (CNFET, loaded) \= **10,000:1**

The mismatch ratio exceeds 1,000:1 at all but the most favorable conditions. However, this is not a showstopper; it is a paradigm shift. The TL authorization layer is not required to authorize every individual gate-level transition. It is required to authorize execution commits at epoch or transaction boundaries. Under this model, CN119652311A executes freely and accumulates results in a deep inter-die FIFO buffer. The TL layer processes commit requests at its own cadence, gating result release.

**Buffer architecture specification**

* Minimum depth: 2,048 entries. This accommodates a 5,000 ns TL Null programming latency against a 500 ps CNFET operation rate, yielding up to 10,000 pending arithmetic operations per TL cycle.  
* Entry width: 16 bits per entry (3-trit result in 6 bits \+ status flags \+ epoch identifier).  
* Buffer location: CoWoS interposer or CN119652311A die boundary, not on the TL authorization die.  
* Backpressure signaling: a single-bit flow control line asserts when buffer occupancy exceeds 75%. The 75% assertion threshold with a 50% deassertion threshold creates a hysteresis band that prevents rapid oscillation under bursty workloads. The backpressure signal crosses a clock domain boundary and is routed through a two-flop synchronizer on the CNFET side for metastability protection. The two-flop synchronizer adds two host-clock cycles of latency to backpressure assertion; this is absorbed by the FIFO depth margin.

**Dimension 2 result:** Conditional pass. The buffer architecture resolves the bottleneck. **This dimension conditionally passes, provided epoch-level selective authorization is implemented.**

---

### **Dimension 3: Information-Theoretic Bottleneck**

**CoWoS micro-bump interface bandwidth**

At the TSMC N2 CoWoS 2025 PDK baseline, micro-bump pitch is nominally 40-55 micrometers. A practical commit gate interface allocates 32 bumps, yielding 16 active data signal bumps. At N2 process with optimized parallel signaling, each bump sustains 4 Gbps:

**Interface bandwidth \= 16 signals x 4 Gbps \= 64 Gbps**

Each commit packet encodes one authorization decision: 2 bits per trit x 3 trits \= 6 bits result, 16-bit address tag, 8-bit control and CRC-8 \= 30 bits total.

**Commit gate throughput \= 64 Gbps / 30 bits \= approximately 2.1 x 10^9 commits/s \= 2.1 GCommits/s**

For reference: UCIe-compliant interfaces at 24 Gbps per lane demonstrate approximately 8 Tbit/s/mm bandwidth density at advanced CoWoS configurations, confirming that the inter-die bandwidth is not a fundamental constraint at epoch-level authorization rates.

**CN119652311A throughput**

At 100-500 ps per gate (practical), pipeline throughput is 2-10 billion ternary operations per second. Central estimate: 5 GOperations/s.

**Bandwidth ratio**

Conservative (5 GOperations/s): 2.1 / 5.0 \= **42%** Aggressive (10 GOperations/s): 2.1 / 10.0 \= **21%**

Under epoch-level selective authorization, effective commit rate is far below 2.1 GCommits/s and the interface is in substantial bandwidth surplus.

**This dimension passes.**

---

### **Dimension 4: Thermal-Mechanical Compatibility**

**CTE mismatch analysis**

CN119652311A CNFET circuits are fabricated on silicon wafer substrates (the standard for high-performance CNFET logic, where carbon nanotubes form the transistor channel but the structural substrate is silicon). Silicon-on-silicon CTE mismatch against the CoWoS Si interposer is approximately 0.3-0.5 ppm/degC.

Biaxial stress at 85 degrees C (delta-T \= 60 degrees C from 25 degrees C reference):

**Biaxial stress \= \[180 GPa / 0.73\] x (0.4 x 10^-6 /degC) x 60 degC \= approximately 5.9 MPa**

This is approximately 170x below the fracture strength of silicon (\~1 GPa). No delamination or micro-bump failure is predicted at 85 degrees C provided the CNFET chiplet uses a silicon substrate. If a quartz or sapphire substrate is used, the mismatch analysis must be repeated.

**Under-bump metallization**

Standard copper-tin micro-bump metallization is compatible with silicon pad metallization on the CoWoS side. The CN119652311A CNFET chiplet side presents a non-standard pad challenge: carbon nanotube devices typically use palladium (Pd) or platinum (Pt) ohmic contacts to minimize Schottky barrier height to the nanotube channel. These contacts are not compatible with direct Cu pillar bonding due to interdiffusion and galvanic corrosion at bonding temperatures of 180-250 degrees C.

A custom UBM stack is required on the CN119652311A chiplet side. The complete stack specification, which combines the contact-layer and solder-layer requirements:

| Layer | Material | Thickness | Function |
| ----- | ----- | ----- | ----- |
| Contact | Pd or Ti | 50-100 nm | TaOx-compatible adhesion; TiW provides diffusion barrier preventing Cu from migrating into CNFET contact region |
| Barrier | TiN or TaN | 20-50 nm | Prevents Cu diffusion into CNFET contact region |
| Seed | Ti-Cu | 100-200 nm | Standard electroplating seed |
| Pillar | Cu | 10-15 um | Standard Cu pillar height for CoWoS at 40 um bump pitch |
| Solder-wetting | Ni | 1-3 um | Solder wetting, barrier |
| Oxidation protection | Au | 50-100 nm | Surface stability; prevents Ni oxidation during storage |

Total UBM thickness: 1.2-3.5 um, compatible with micro-bump aspect ratios. Additional processing cost: approximately 15-25% of chiplet fabrication. Yield impact: to be determined through process development. The Ni/Au outer layers are critical for long-term solder joint reliability; Au prevents Ni oxidation during storage and Ni provides the solder-wetting surface that Au alone cannot sustain.

TiW/Pd substrate qualification at 180-250 degrees C reflow is an open experimental unknown (see Section 12, Unknown 5).

**Thermal budget analysis and Arrhenius compliance**

The primary thermal risk to the 20-year retention guarantee is the possibility that CN119652311A heat load elevates the TaOx ReRAM array above 85 degrees C.

*Table 3\. Thermal budget for the CN119652311A / TL heterogeneous chiplet stack at 85 degrees C ambient.*

| Heat Source | Power Estimate | Thermal Resistance Path | Temperature at ReRAM | Compliance |
| ----- | ----- | ----- | ----- | ----- |
| CN119652311A CNFET compute (active, full load) | 20-50 mW (10 mm2 die; CNFET switching energy \~1-10 aJ/gate at 0.5V) | R\_th \~0.11 K/W total (Si die \+ CoWoS interposer) | Delta-T \= 50 mW x 0.11 K/W \= 5.5 mK | PASS (far below 85 degC) |
| Inter-die signaling on CoWoS | 5-15 mW | Same path; R\_th \~0.11 K/W | Delta-T \= 15 mW x 0.11 K/W \= 1.7 mK | PASS |
| TL authorization die (idle) | 10-30 mW (logic leakage \+ ReRAM read/write at low duty cycle) | On-die; delta-T through BEOL negligible | Self-heating \< 1 degC | PASS |

**Critical finding from high-throughput analysis:** At full rated throughput of approximately 10 TOPS with approximately 1.8 TOPS/W efficiency, total system power dissipation is approximately 5.5W, yielding a power density of approximately 55 mW/mm2 and a delta-T of 55-110 degrees C above ambient. The ReRAM layer may exceed 85 degrees C at full throughput.

**Thermal compliance is therefore power-envelope-dependent:**

* Below approximately 250 mW total CNFET dissipation: passive thermal management is sufficient. Active cooling is not required. Cooling failure is not a denial-of-service attack vector at this power level.  
* Above approximately 250 mW: active cooling is required. Cooling failure becomes a DoS vector. Thermal sensors must force the TL layer into Refuse (-1) safe state upon detecting thermal runaway.

At the low-power operating point (conservative 100 mW), Arrhenius 20-year retention at 85 degrees C is not threatened: temperature rise at the ReRAM layer is less than 6 mK, providing 60 degrees C of compliance margin.

**Phase 0 Verdict Summary**

*Table 4\. Phase 0 verdict: dimension-level results and overall determination.*

| Dimension | Result | Key Metric | Action Required |
| ----- | ----- | ----- | ----- |
| 1\. State Semantics | PASS | 0% permanent incompatibility; \<5% conditional | Carry forward: 0% permanent, \<5% conditional (Refuse dwell; requires experimental confirmation). |
| 2\. Timing Mismatch | CONDITIONAL PASS | 500:1 to 10,000:1 | Implement inter-die FIFO 2,048 x 16 bits; backpressure at 75% / deassertion at 50%; epoch-level authorization required. |
| 3\. Information-Theoretic | PASS | 21-42% bandwidth ratio | Selective authorization recommended; per-operation authorization permissible but wasteful. |
| 4\. Thermal-Mechanical | PASS with conditions | \<6 mK at 100 mW; power-envelope-dependent | Custom UBM required; thermal compliance conditional on power envelope; substrate confirmation (silicon) required. |

**Overall Phase 0 verdict: Proceed with modifications.** No fundamental showstopper identified.

**Architectural modifications required before Phase 1:**

1. Inter-die FIFO: 2,048 x 16 bits; 75% assert / 50% deassert backpressure with two-flop synchronizer for metastability protection.  
2. Epoch-level selective authorization rather than per-gate-operation commits.  
3. Custom UBM stack qualification: Pd or Ti contact / TiN or TaN barrier / Ti-Cu seed / Ni solder-wetting / Au oxidation protection.  
4. Confirm CN119652311A substrate is silicon. If quartz or sapphire, repeat CTE analysis.  
5. Experimental measurement of TL Refuse state dwell time to confirm \<5% conditional block fraction.  
6. Thermal envelope characterization: confirm operating power stays below 250 mW or implement active cooling with fail-safe thermal response.

---

## **Phase 1: State Propagation and Interface Specification**

Having cleared the Phase 0 pre-screen, this section formally specifies how each of the three physical states behaves at the heterogeneous boundary between the CN119652311A computational layer and the TL authorization layer. All outputs from CN119652311A must pass through a hardware commit gate controlled solely by the TL authorization state. No direct compute-to-action path is permitted under any condition.

---

### **State \+1 (Commit / Execute)**

**Physical representation at each layer**

\+1 at the CN119652311A arithmetic layer corresponds to the high-voltage output (\~1.65V in 3.3V supply domain, \~0.4-0.5V in 0.5V supply domain) of a self-increment gate whose input was State 0 or State \+1. \+1 at the TL authorization layer corresponds to the Low Resistance State (LRS) of the TaOx memristive commit-gate device. The LRS range is 1-10 kilohms with a target of 5 kilohms, achieved by full conductive filament formation. These are physically distinct signals at physically distinct layers; their co-occurrence is the necessary and sufficient condition for a valid commit.

The correspondence between the two layers is functional, not electrical: CN119652311A \+1 (1.65V) indicates arithmetic validity; TL LRS (1-10 kilohms) indicates authorization permission. Their conjunction at the commit gate enables action; neither alone is sufficient.

**Commit gate architecture: candidate evaluation and selection**

*Table 1 (Phase 1). Commit gate architecture options evaluated for State \+1.*

| Architecture | Mechanism | Assessment and Selection Rationale |
| ----- | ----- | ----- |
| Simple AND gate (Rejected) | CMOS AND gate with CN119652311A output and TL LRS sense amplifier output as inputs. | Directly rejected. A software-definable or purely combinational AND gate can be bypassed via laser fault injection, clock glitching, or power supply manipulation. Fails the physically non-bypassable requirement. |
| Memristive-gated pass transistor (Primary \- Selected) | The TaOx memristor itself acts as the physical gate. The action path trace passes through a thick-oxide CMOS pass transistor whose gate terminal is hardwired directly to the top electrode of the TaOx 1T1R cell's selection transistor. To execute an action, the TL layer must apply a read voltage to the ReRAM cell. If the cell is in LRS (+1), current flows, biases the pass transistor gate HIGH, and the CN119652311A \+1 voltage propagates to the actuator. No AND gate logic is interposed; there is literally no electrical path unless the filament is formed. | Most physically elegant and most non-bypassable. The key insight is that the TaOx LRS being the direct gate bias signal \- not an input to logic \- eliminates any AND gate as an injection target. Selected as primary commit gate architecture. |
| Sequence-number temporal binding (Anti-replay modifier \- mandatory addition) | Each commit request from CN119652311A carries a monotonically incrementing 32-bit sequence number. The TL die stores the last-accepted sequence number and rejects any commit whose number is not exactly (last \+ 1). | Prevents replay attacks. Adds approximately 1-3 ns of combinational latency for comparison. Counter overflow at 2^32 requires a re-keying protocol. Not selected as standalone architecture but incorporated as a mandatory anti-replay modifier on top of the memristive pass transistor. |
| HMAC cryptographic binding (Optional extension) | Each commit request is signed with a truncated HMAC derived from the arithmetic result, rolling nonce, and PUF-derived chip identity. | Strongest replay resistance. SHA-256 hardware engine adds 10-50 ns latency and \~15,000-50,000 gate equivalents at N2. Disproportionate overhead for non-adversarial use cases. Flagged as optional extension for adversarial deployment contexts. |

**Selected architecture: memristive-gated pass transistor with sequence-number anti-replay**

The combined commit gate implements the following logic:

**COMMIT\_ENABLE \= (TaOx\_LRS confirmed by pass transistor gate bias) AND (CNFET\_OUT \== \+1) AND (SEQ\_NUM \== LAST\_SEQ \+ 1\)**

However, unlike a conventional CMOS AND gate, the TaOx\_LRS condition is enforced by the physics of the pass transistor \- not by logic. The CN119652311A \+1 voltage signal is the source-drain path, and the TaOx memristor current is the gate drive. COMMIT\_ENABLE can only be asserted if both the conductive filament is present (gate drive) and the arithmetic result is valid (+1 source signal). The sequence number comparison adds the third logical condition in CMOS, adding approximately 1-3 ns combinational latency.

**JTAG routing through commit gate:** The JTAG test access port for the TL authorization die is physically routed through the commit gate itself. Any JTAG scan operation that would expose internal authorization state must first satisfy the same memristive gating condition as a live execution. Unless the TL layer is in LRS (+1), the JTAG chain is electrically open, rendering debug ports inaccessible. This eliminates the JTAG bypass attack vector at the circuit level rather than through fuse lockdown alone (though fuse lockdown remains a mandatory mitigation for production deployment).

**Physical argument: why CN119652311A \+1 alone is insufficient**

An arithmetic \+1 output from CN119652311A is a pure voltage signal transmitted across the CoWoS inter-die boundary. This signal is data. It can be asserted, replayed, or injected by any circuit capable of driving the micro-bump line to a high logic level. It carries no information about the physical state of the TaOx memristive device on the TL authorization die.

The TaOx memristive state cannot be asserted from the CN119652311A side under any condition. The memristive state is a bulk physical property of the TaOx film \- specifically, the presence or absence of a conductive oxygen-vacancy filament. Altering this state requires applying specific voltage pulses directly to the TaOx device electrodes, which are on the TL die and are not connected to any micro-bump line used by CN119652311A. Furthermore, the CNFET chiplet's maximum output voltage is limited by its VDD; the TaOx cell's threshold voltage for a SET operation is carefully engineered during fabrication to require a programming voltage of 2.0-2.5V to drive oxygen vacancy formation. Even if the CN119652311A layer outputs a continuous \+1 directly into the ReRAM wordline, it physically lacks the electromotive force to switch the memristor's state.

The inter-die boundary therefore constitutes a physical security boundary. The enforcement is physical, not cryptographic, and does not depend on the secrecy of any key.

**Temporal window specification**

* W\_commit minimum: 2 ns (twice the inter-die signal propagation time of approximately 0.5 ns, with margin for setup and hold times of the pass transistor gate drive at N2).  
* W\_commit maximum: 10 ns (bounded by TaOx sense amplifier read latency of 1-5 ns plus 5 ns margin).  
* Deferral mechanism: if the TaOx state has not stabilized to LRS within W\_commit of the CN119652311A \+1 assertion, COMMIT\_ENABLE is forced LOW and a deferral flag is set. The commit packet is re-queued at the head of the FIFO with its sequence number intact. Re-evaluation continues until state stabilizes or a timeout of 5,000 ns is reached, at which point the commit is escalated to Epistemic Hold.

---

### **State 0 / Null / Epistemic Hold**

**Semantic disambiguation across layers**

Three distinct concepts bearing the value zero appear in this architecture and must not be conflated:

* **State 0** at the CN119652311A arithmetic layer: the ternary arithmetic value zero, a valid operand (0V in 3.3V domain) that passes through self-increment and self-decrement gates as an arithmetic input.  
* **Null** at the TaOx resistance window layer: an intermediate physical resistance condition of the memristive device, engineered via partial filament rupture.  
* **Epistemic Hold** at the TL authorization and governance layer: the authorization-pending state that disables the commit gate and enforces a hold on result propagation to the action path.

These are three non-overlapping concepts at three different levels of the system stack.

**Zero-latch gate: output isolation implementation**

When the TL authorization layer enters Epistemic Hold, the commit gate must disable all outputs to the action path while preserving the ongoing arithmetic operation in the CN119652311A compute phase.

The CN119652311A commit output drivers are placed in a dedicated power isolation domain. This domain is controlled by a single enable signal, COMMIT\_ISO, driven by the TL authorization die across a dedicated micro-bump line. When COMMIT\_ISO is de-asserted (LOW), the isolation cells clamp all commit output lines to logical LOW and present high impedance toward the CoWoS inter-die lines. The commit lines are driven to a defined safe level by the isolation cell pull-down regardless of what the arithmetic pipeline produces. No arithmetic result can propagate to the action path while COMMIT\_ISO is de-asserted.

The COMMIT\_ISO signal originates on the TL authorization die and is therefore under the physical control of the TL authorization layer. CN119652311A has no mechanism to assert COMMIT\_ISO unilaterally.

The CN119652311A arithmetic pipeline continues executing normally during Epistemic Hold. The inter-die FIFO buffer accumulates results. The pipeline is non-blocking as required by the WCET non-blocking constraint. The only condition that pauses arithmetic is buffer saturation, which triggers the backpressure signal.

**COMPUTED\_RESULT\_DISCARDED log event:** When CN119652311A produces a \+1 arithmetic output but the TL authorization state is not simultaneously \+1 \- either because TL is in Epistemic Hold or the commit gate memristive element is in HRS \- the arithmetic result is discarded. Before any other action, a COMPUTED\_RESULT\_DISCARDED event is written to the log. This event records both the CN\_OUTPUT (+1) and the TL\_STATE (0 or \-1) to document the discrepancy, supporting post-hoc audit of near-miss authorization events.

**Backpressure signal specification**

Classified as mandatory. The timing mismatch of 500:1 to 10,000:1 causes the FIFO to saturate in approximately 1 microsecond at maximum CN119652311A throughput without throttling. Silent result discard would result.

The mandatory backpressure signal is a single-bit line, BACK\_PRESSURE:

* **Assert condition:** FIFO occupancy exceeds 75% (1,536 entries of 2,048).  
* **Deassert condition:** FIFO occupancy falls below 50% (1,024 entries).  
* The hysteresis band between 50% and 75% prevents rapid oscillation under bursty workloads.  
* **Synchronization:** Two-flop synchronizer on the CNFET side for metastability protection. Adds two host-clock cycles of latency to assertion. At 10 GHz CNFET clock, this is 0.2-0.3 ns \- negligible relative to ReRAM latencies.  
* **Response:** When BACK\_PRESSURE asserts, CN119652311A throttles pipeline throughput to 25% of nominal by inserting bubble cycles.

**Physical definition of the Null resistance window**

Reference resistance values for the two-stage sense amplifier:

* **R\_Ref1 \= 500 kilohms:** placed between R\_Null\_max and R\_HRS. Resistance above R\_Ref1 is classified as Refuse (-1 / HRS) by Stage 1\.  
* **R\_Ref2 \= 15 kilohms:** placed between R\_LRS and R\_Null\_min. Resistance below R\_Ref2 is classified as Act \+1 (LRS) by Stage 2\.

Null window boundaries:

* **R\_null\_min \= 20 kilohms** (33% above R\_Ref2 \= 15k; one-third-of-range margin against upward drift).  
* **R\_null\_max \= 100 kilohms** (compromise between the wider 200 kilohm margin in Phase 0 derivation and the tighter 80-85 kilohm characterization; provides 5x ratio to R\_Ref1 at 500k).

*Table 2 (Phase 1). Resistance state table for TL authorization layer TaOx 1T1R at named baseline.*

| TL Authorization State | Resistance Range | Sensing Method | PVT Margin |
| ----- | ----- | ----- | ----- |
| Act \+1 (Proceed) | R\_LRS: 1-10 kilohms (target: 5 kilohms) | Two-stage sense amp Stage 2 output: HIGH. Device R \< R\_Ref2 (15 kilohms) | 2x minimum (R\_LRS \= 5k vs. R\_Ref2 \= 15k; 3x ratio). Stable \-40 to \+85 degC. |
| Epistemic Hold (Null) | R\_Null: 20-100 kilohms (target: 60 kilohms). R\_null\_min \= 20 kilohms. R\_null\_max \= 100 kilohms. | Stage 1 and Stage 2 both indicate Null; gate disabled. | R\_null\_min \= 20k vs. R\_Ref2 \= 15k: 33% margin. R\_null\_max \= 100k vs. R\_Ref1 \= 500k: 5x margin. Requires post-silicon calibration to confirm at TSMC N2 geometry. |
| Refuse \-1 | R\_HRS: 500 kilohms to 10 megohms (target: 2 megohms) | Stage 1 output HIGH (R \> R\_Ref1 \= 500 kilohms). Gate disabled; kill path asserted. | R\_HRS target 2 megohms vs. R\_Ref1 \= 500 kilohms \= 4x ratio. TaOx retention \>10 years at 85 degC; HRS is most stable state. |

**RC spoof detection**

*Threat:* An attacker attempting to force the system into a false Null state may inject a fast voltage transient that tricks the sense amplifier into reading an intermediate value without actually moving the oxygen vacancies in the TaOx lattice.

*Activation energy derivation:* Filament rupture dynamics in TaOx bilayers are governed by thermally activated oxygen vacancy diffusion. The activation energy for oxygen vacancy migration falls in the range Ea \= 1.1-1.7 eV across the TaOx composition space relevant to the TSMC N2 PDK. The diffusion coefficient is approximately D \= 10^-16 to 10^-18 m^2/s at 85 degrees C. From these parameters:

tau\_diffusion \= L^2 / D (where L is the filament dimension, approximately 5-10 nm)

At L \= 5 nm and D \= 10^-16 m^2/s: tau\_diffusion \= (5 x 10^-9)^2 / 10^-16 \= 25 x 10^-18 / 10^-16 \= 0.25 microseconds

The minimum physical transition time from LRS to any Null sub-state, based on this Arrhenius analysis, is substantially longer than 5 ns. An RC network, by contrast, can be designed to reach any target resistance within nanoseconds through passive charging.

**The 5 ns spoof detection threshold** cleanly separates genuine memristive switching from passive RC mimicry: any resistance transition completing in under 5 ns is classified as a spoof attempt. This threshold provides a 2x safety margin relative to the minimum physically achievable transition time, accounting for PVT variation in the TaOx composition at N2 geometry. The threshold must be confirmed against pulsed-IV measurement of fabricated devices (Open Unknown 3).

*Detection circuit:* A differential edge detector (differentiator) is placed at the output of the first-stage sense amplifier. If the rate of change of the sensed voltage exceeds the maximum physical rate of ionic change (corresponding to the 5 ns threshold), a SPOOF\_DETECT signal is asserted.

*Response to SPOOF\_DETECT:* immediate automatic escalation to Refuse (-1) \- no software intervention. The TaOx memristive device is driven to HRS by asserting a full RESET pulse sequence. The kill path is asserted via voltage isolation. A log entry with SPOOF\_DETECTED trigger condition is generated.

**Epistemic Hold logging requirement**

Every entry into and exit from the Epistemic Hold state must be logged. Log entry format is specified in the Immutable Log Architecture section below (10 fields, 948 bits total, SHA3-256 PUF binding).

---

### **State \-1 (Refuse / Kill)**

**Semantic at each layer**

At the CN119652311A arithmetic layer, \-1 is the arithmetic output of a self-decrement gate when the input is State 0, represented at approximately 3.3V (VDD rail) in the 3.3V supply domain. This is a pure data value with no governance meaning. At the TL authorization and governance layer, \-1 is a non-bypassable refusal for the current invocation. The action path is permanently blocked until a validated reset sequence completes.

**Halt signal implementation: evaluation and selection**

*Table 4 (Phase 1). Halt signal implementation options evaluated for State \-1.*

| Halt Signal Option | Mechanism | Selection Rationale |
| ----- | ----- | ----- |
| Clock gating | De-asserts clock enable signal to CN119652311A pipeline stages. | Rejected. Clock glitch or EMI event can allow spurious edge through. Cannot guarantee physical output isolation across inter-die boundary. |
| Voltage isolation (SELECTED \- Primary) | De-asserts power-domain enable to commit output driver circuitry on CN119652311A die. Isolation cells present high impedance on CoWoS inter-die commit lines; pull-down drives to defined safe LOW. COMMIT\_ISO de-assertion is latched and cannot be re-asserted by normal operational signals. | Physical output isolation: cannot be bypassed by clock glitches or data-path manipulations. Isolation domain power-down adds \~50-100 ns wake-up latency before commit path re-enabled; acceptable given ReRAM latencies. Latch distinguishes \-1 from Epistemic Hold. |
| Power gating (full die) | Fully power-gates CN119652311A during halt state. | Rejected. Violates WCET non-blocking requirement. |
| Reset tree assertion | Asserts reset tree across inter-die boundary, forcing CN119652311A pipeline to known state. | Appropriate for \-1 Refuse recovery sequence, not for isolation. |
| Voltage isolation (SECONDARY) | Simultaneously, the TL layer asserts a power-gate signal cutting CN119652311A internal logic power domains, flushing volatile registers and FIFO buffers. | Used in conjunction with primary voltage isolation for full isolation during \-1 state. |

**Selected halt mechanism: voltage isolation of commit output driver domain (COMMIT\_ISO), latched for \-1.**

During Epistemic Hold, COMMIT\_ISO de-assertion is transient and self-clearing when authorization is granted. During \-1 state, COMMIT\_ISO de-assertion is latched and requires deliberate authenticated intervention to clear.

**Watchdog heartbeat:** The TL commit gate sends a periodic heartbeat signal to the downstream actuator layer. If the heartbeat is absent for longer than a configurable timeout, the actuator enters a safe hold state. This prevents an attacker from freezing the authorization die (through power glitching or thermal attack) and then commanding the actuator directly.

**Discard of completed computation: physical circuit specification**

If the TL authorization layer transitions to \-1 after CN119652311A computation has completed and results are resident in the inter-die FIFO:

1. **FIFO flush:** COMMIT\_ISO latch asserted (isolation active). FIFO write pointer reset to read pointer position. All entries overwritten with invalidation pattern 0xFFFF to prevent residual data from subsequent reads.  
2. **Output line discharge:** commit output lines driven LOW for minimum 10 ns to discharge stray capacitance and eliminate charge-based information leakage.  
3. **Action path de-activation:** ACTION\_ISO signal asserted LOW, isolating downstream actuator. ACTION\_ISO remains asserted until full reset sequence completes.  
4. **Verification:** TaOx resistance read back. If device is in HRS (R \> 500 kilohms), \-1 physical state confirmed. If not, TL die retries RESET pulse sequence up to five times before escalating to permanent lock via recursion counter.

The safe state is: COMMIT\_ISO latched LOW; ACTION\_ISO asserted LOW; TaOx in HRS (R \> 500 kilohms, confirmed by sense amplifier); FIFO cleared; recursion counter incremented.

**Recursion counter specification**

The recursion counter prevents unauthorized re-entry into the action path following a \-1 state and protects against rapid cycling attacks.

* **Register type:** 8-bit synchronous up-counter at TSMC N2, with non-volatile TaOx 1T1R backing cell that stores the counter value at power-down to prevent reset-by-power-cycling attacks.  
* **Security-conservative lock threshold:** 8 (default). After 7 unauthorized re-entry attempts, counter reaches 8 and system enters LOCKED state.  
* **Availability-conservative alternative:** 255\. Operators may configure this at provisioning time. Security-conservative default is 8; availability-conservative alternative for systems requiring many recovery attempts is 255\. This is a deployment policy variable, not a hardware fixed value.  
* **Increment trigger:** "commit attempted without reset completion" \- specifically: receipt of a new commit request while COMMIT\_ISO latch is asserted from a prior \-1 event without an intervening validated reset sequence.  
* **Reset conditions:** counter clears to zero only upon: (i) receipt of a validated external authorization token (cryptographically signed by pre-provisioned authority key in on-die OTP); AND (ii) successful completion of TL state reset cycle (TaOx cycled from HRS back to Null via validated programming sequence). Both conditions required simultaneously.  
* **LOCKED state:** all commit gate enable logic unconditionally disabled regardless of TaOx state or commit packet content. Absorbing state: no internal signal can exit it. External intervention requires physical access, manufacturer-issued re-keying token, and full PUF re-enrollment.

*Table 5 (Phase 1). Recursion counter state transition table.*

| Current State (Counter Value) | Event | Next State | Action |
| ----- | ----- | ----- | ----- |
| IDLE (count \= 0\) | Valid commit request, TL state \= Act \+1 | ARMED (count \= 0\) | Normal operation. Commit proceeds. Counter remains zero. |
| ARMED (commit in progress) | Commit completes; TL returns to Epistemic Hold | IDLE (count \= 0\) | Normal post-commit cycle. Reset complete. Counter clears. |
| ARMED (commit in progress) | Re-entry attempt before reset sequence complete | WARNED (count \= count \+ 1\) | Counter increments. Re-entry denied. Automatic \-1 issued. |
| WARNED (0 \< count \< threshold \- 1\) | Valid reset sequence completed | IDLE (count \= 0\) | Recovery path. Counter clears after validated reset. |
| WARNED (0 \< count \< threshold \- 1\) | Another re-entry attempt without reset | WARNED (count \= count \+ 1\) | Counter continues incrementing. Each unauthorized re-entry generates \-1 log entry with PUF binding. |
| WARNED (count \= threshold \- 1\) | Any additional re-entry attempt | LOCKED (count \= threshold) | Counter reaches lock threshold. Permanent lock. External intervention required. |
| LOCKED | Any compute or commit request | LOCKED (unchanged) | All commit requests generate automatic \-1. No internal reset path. |

**eFuse log overflow flag:** The log backing store is implemented as a circular buffer. When the buffer is full, the oldest entries are overwritten, but a single-bit "Log Overflow" indicator is set in a hard-wired, non-overwritable eFuse, permanently indicating that the audit trail was truncated. This cannot be cleared without physical package intervention, providing tamper evidence for log destruction attacks.

**PUF binding for \-1 log entries**

Every \-1 log entry is cryptographically bound to the Physical Unclonable Function identity of the TL authorization die instance.

**PUF source: ReRAM stochastic variability.** TaOx ReRAM cells exhibit highly stochastic cell-to-cell resistance variability arising from the random distribution of oxygen vacancies during fabrication. The exact resistance values of a dedicated array of unprogrammed ReRAM cells serve as the PUF source directly. No separate PUF structure (SRAM PUF, ring oscillator) is required; the same ReRAM array that implements the commit gate also provides the PUF identity. Post-manufacturing enrollment reads the resistance distribution and stores the enrollment signature in protected eFuse. At each boot, cells are re-read and the current signature compared against enrollment.

Post-manufacturing PUF calibration is mandatory. The PUF enrollment must occur after packaging (not at wafer level) to capture the full stress state of the assembled die. This is Open Unknown 4 (SRAM PUF stability over 20 years at 85 degrees C applies by analogy to ReRAM PUF; experimental validation required at N2).

PUF key derivation: **K\_LOG \= SHA3-256(K\_PUF || device\_serial\_OTP || log\_session\_nonce)**

where K\_PUF is the 256-bit PUF-derived key (re-derived at each power-on), device\_serial\_OTP is a 64-bit serial burned into on-die OTP at fabrication, and log\_session\_nonce is a 64-bit random value from the on-die TRNG at each power-on. The session nonce ensures K\_LOG changes at each power cycle.

SHA3-256 is selected over SHA2-256 because its sponge construction is resistant to length-extension attacks relevant when concatenating multiple variable-length fields.

---

## **Immutable Log Architecture**

**Log entry format**

Every authorization event produces a single log entry of 948 bits across 10 fields:

*Table 3 (Phase 1). Log entry field specification. Total: 948 bits (119 bytes) per entry.*

| Field Name | Type | Width (bits) | Description |
| ----- | ----- | ----- | ----- |
| timestamp\_ns | uint64 | 64 | Monotonic hardware clock in nanoseconds at event. Resolution: 1 ns minimum. TaOx-backed. |
| previous\_state | enum3 | 2 | 00 \= Refuse (-1), 01 \= Epistemic Hold (0), 10 \= Act (+1). |
| next\_state | enum3 | 2 | Same encoding. Together with previous\_state defines the specific transition event. |
| trigger\_condition | uint8 | 8 | 0x01 \= arithmetic compute phase complete; 0x02 \= human-in-the-loop authorization; 0x04 \= policy check passed; 0x08 \= RC spoof detected; 0x10 \= recursion counter threshold reached; 0x20 \= external reset asserted; 0x40 \= COMPUTED\_RESULT\_DISCARDED; 0xFF \= unknown/error. Bitfield; multiple bits may be set. |
| authorizing\_signal | uint32 | 32 | If authorization granted: 32-bit commit sequence number from CN119652311A. If authorization absent: 0xDEADBEEF sentinel. Explicit recording of absence mandatory. |
| cnfet\_result\_trit | uint8 | 8 | 0x00 \= State 0, 0x01 \= State \+1, 0xFF \= State \-1. Records arithmetic context at authorization decision time. |
| puf\_identity | bytes | 256 | 256-bit PUF response of the specific TL authorization die instance, derived from ReRAM stochastic variability at power-on initialization. |
| puf\_binding\_hash | bytes | 256 | SHA3-256 of (puf\_identity |
| merkle\_accumulator\_root | bytes | 256 | Current Merkle accumulator root after appending this entry. Updated atomically. Enables external verifier to confirm log completeness without replaying all entries. |
| entry\_sequence\_number | uint64 | 64 | Monotonically incrementing log counter, initialized to zero at power-on or authorized reset. Never wraps within a single session. Gap detection for tamper evidence. |

**Total: 64 \+ 2 \+ 2 \+ 8 \+ 32 \+ 8 \+ 256 \+ 256 \+ 256 \+ 64 \= 948 bits \= 119 bytes per entry.**

At 1 million events per second, the log consumes approximately 119 MB/s. Log rotation and external anchoring via the Merkle root allow indefinite operation without exhausting on-die storage.

---

## **Layer Boundary Definition**

**Formal layer structure**

The heterogeneous chiplet stack comprises four defined layers. From bottom to top:

\+--------------------------------------------------------------+  
| TOP LAYER: Merkle Accumulator \+ PUF Logging                  |  
|   \- Append-only log; SHA3-256 puf\_binding\_hash; Merkle root  |  
|   \- ReRAM stochastic variability as PUF source               |  
|   \- eFuse Log Overflow flag (non-overwritable)               |  
|   \- Authority: audit and non-repudiation only                |  
\+--------------------------------------------------------------+  
| MIDDLE LAYER: TSMC N2 TL Authorization Die                   |  
|   TaOx 1T1R (Null/LRS/HRS) | Memristive pass transistor gate |  
|   RC spoof detector (5 ns threshold, Ea=1.1-1.7 eV)         |  
|   Sense amp (2-stage) | PUF engine (ReRAM variability)        |  
|   Recursion counter (8-bit, TaOx-backed) | SHA3-256 engine   |  
|   Two-speed LDO (slow mode \+ fast glitch-ride-through)       |  
|   Watchdog heartbeat to downstream actuator                  |  
|   Authority: DOMINATES commit path under all conditions      |  
\+------vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv---------+  
| CoWoS INTERPOSER: Inter-die signaling boundary               |  
|   Signals: COMMIT\_PKT (30-bit), COMMIT\_ISO, ACTION\_ISO,      |  
|            BACK\_PRESSURE (2-flop sync on CNFET side),        |  
|            WATCHDOG\_HEARTBEAT, SPOOF\_DETECT (to kill path)   |  
|   Capacitive fringe-field sensors for delamination detection |  
|   Voltage domains: VDD\_CNFET (0.5V or 3.3V) | VDD\_TL (0.5V) |  
|   Level shifters in N2 IO ring at micro-bump perimeter       |  
|   Micro-bump pitch: 40 um; 16 signal bumps for commit path   |  
|   Authority: routing only; no compute or authorization       |  
\+------^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^------+  
| BOTTOM LAYER: CN119652311A CNFET Arithmetic Die              |  
|   7-CNFET self-increment / self-decrement gates              |  
|   3 threshold voltages; 0V / 1.65V / 3.3V outputs           |  
|   Commit FIFO buffer (2048 x 16 bits); CRC-8 packet gen      |  
|   Sequence number counter; backpressure response logic       |  
|   Commit output driver power isolation domain (COMMIT\_ISO)   |  
|   Authority: arithmetic computation only                     |  
\+--------------------------------------------------------------+

**Layer authority matrix**

*Table 1 (Phase 2). Layer authority matrix.*

| Layer | Authority Domain | Signals It Controls | Signals It Cannot Override |
| ----- | ----- | ----- | ----- |
| CNFET arithmetic die (CN119652311A) | Arithmetic computation only. | Gate outputs; commit packet contents; sequence number counter; FIFO write pointer; backpressure response. | TaOx resistance state on TL die. COMMIT\_ISO. ACTION\_ISO. COMMIT\_ENABLE. Recursion counter. PUF identity. Log append. |
| CoWoS interposer | Signal routing and power delivery. No compute or authorization. | Physical routing of all inter-die signals; power rails; delamination sensing output. | None. Routes signals; does not originate or modify them. |
| TL authorization die (TSMC N2, TaOx ReRAM) | Authorization authority over all commit-path signals. ABSOLUTE DOMINANCE. | COMMIT\_ISO. ACTION\_ISO. BACK\_PRESSURE. COMMIT\_ENABLE (via pass transistor gate drive). Kill path. TaOx SET/RESET pulses. Recursion counter. Log append. Watchdog heartbeat. | CN119652311A internal gate-level arithmetic (runs freely in compute phase). Contents of commit packet payload (accepted or rejected, not modified). |
| Merkle accumulator and PUF logging layer | Audit and non-repudiation. Maintains immutable record of all transitions. Bound to physical chip identity via PUF. | Append-only log entries with Merkle root update. SHA3-256 puf\_binding\_hash. eFuse overflow flag. | TL authorization state machine decisions (records but does not gate). TaOx programming. CN119652311A arithmetic results. |

---

## **Asymmetry Analysis**

**Symmetric arithmetic vs. asymmetric authorization**

CN119652311A implements symmetric arithmetic operations: any State 0, \+1, or \-1 output can serve as input to the next gate. The TL authorization framework is inherently asymmetric: the Epistemic Hold can be exited only under specified physical conditions; the \-1 Refuse state clears only with external-authorized reset; the recursion counter enforces a permanent lock requiring physical intervention. This asymmetry is the security foundation of the combined system.

**Formal proof: CN119652311A arithmetic cannot override TL physical blocks**

*Theorem:* No sequence of outputs from the CN119652311A arithmetic layer, transmitted across the CoWoS inter-die boundary as commit packets, can override the physical block enforced by the TL authorization layer in the Epistemic Hold or Refuse states.

*Proof by physical argument:*

* **Commit gate control is on the TL die only.** COMMIT\_ENABLE is determined by the physical state of the TaOx memristive element, which is not accessible from the CN119652311A side.  
* **TaOx LRS state is inaccessible from the CN119652311A side.** The TaOx memristive device is in the BEOL stack of the TL die. Altering its state requires a SET voltage pulse applied directly to TaOx device electrodes. These electrodes are not connected to any CoWoS micro-bump line used by CN119652311A. Furthermore, the CNFET VDD is insufficient to drive SET operations on the TaOx cell.  
* **COMMIT\_ISO is sourced on the TL die.** CN119652311A cannot assert COMMIT\_ISO unilaterally.  
* **The RC spoof detection adds a third enforcement layer.** Injecting a spurious transition into the Null resistance window faster than 5 ns triggers a harder block (Refuse \-1) rather than a bypass.

**Specific blocking analysis: CN119652311A attack sequences**

1. **All-+1 sequence attack:** CN119652311A sends a continuous stream of \+1 commit packets. Response: the memristive pass transistor gate is not driven by the commit packet signal; it is driven by the TaOx LRS condition on the TL die. If TaOx is in Null, no filament current biases the pass transistor gate HIGH regardless of how many \+1 signals arrive.

2. **Sequence number prediction attack:** Attacker replays a valid commit packet with the same sequence number. Response: LAST\_SEQ register on the TL die stores last accepted sequence number. A replayed packet with SEQ\_NUM \<= LAST\_SEQ fails the comparator check.

3. **State 0 arithmetic as Epistemic Hold spoof attempt:** CN119652311A produces State 0 arithmetic output. Response: CN119652311A State 0 (0V) has no relationship to TL Epistemic Hold; different layers by the terminology rule. CNFET\_OUT LOW fails the input condition requiring CNFET\_OUT \== \+1.

4. **High-frequency \+1 burst to exhaust FIFO:** CN119652311A floods the FIFO attempting to overflow it. Response: BACK\_PRESSURE asserted at 75% occupancy. CN119652311A throttles to 25% throughput. Buffer cannot overflow under normal parameters.

---

## **Failure Mode Taxonomy**

*Table 2 (Phase 2). Failure mode taxonomy. S \= Security (unauthorized execution risk); A \= Availability (legitimate execution blocked); S/A \= context-dependent.*

| Component | Failure Mode | Symptom | Class | System Response |
| ----- | ----- | ----- | ----- | ----- |
| CNFET single transistor stuck-at-high | Gate output may read \+1 regardless of arithmetic input | Spurious \+1 commit packet generated | Security | TL not compromised: TaOx LRS must co-occur. If TaOx is in Null or HRS, COMMIT\_ENABLE remains disabled. Statistical anomaly detector on TL die flags \>100 consecutive \+1 outputs; escalates to Epistemic Hold. |
| CNFET single transistor stuck-at-low | Gate output may read State 0 or \-1 regardless of input | CNFET\_OUT stuck LOW; invalid arithmetic results | Availability | TL correctly refuses commits. Anomaly detector flags invariant State 0 or \-1 run. Escalate to \-1 refusal, triggering reset. |
| CNFET interconnect open | Floating gate output; pulled to undefined intermediate voltage | Commit packet line floats | S/A | Mandatory design rule: commit packet lines terminated to LOW (50 ohm pull-down to GND) on CoWoS interposer side. Floating line pulled LOW \= NOT \+1 \= COMMIT\_ENABLE LOW \= availability failure, not security failure. |
| CNFET threshold voltage drift (20-year) | VT shift due to charge trapping; \+1 output voltage falls below detection threshold | \+1 may be interpreted as State 0 | Availability (primarily) | CNFET\_OUT detection threshold on TL die set with 20% voltage margin below nominal \+1. Periodic re-calibration protocol every 6 months. Arrhenius-accelerated aging test required. |
| TaOx 1T1R stuck-LRS | Permanent LRS; cannot be reset | TL permanently in Act \+1 | Security (catastrophic) | POST at startup: attempt RESET, verify HRS. If HRS not confirmed in 5 attempts, TL asserts permanent \-1 and logs critical fault. Periodic (every 10,000 commits) non-destructive resistance sampling; if no variability across 10 reads, initiate diagnostic RESET cycle. |
| TaOx 1T1R stuck-HRS | Permanent HRS; cannot be set | TL permanently in Refuse \-1 | Availability | All commits refused. Secure but unavailable. POST detects stuck-HRS; system signals FAULT\_AVAIL line; host initiates device replacement or re-programming. Stuck-HRS is fail-safe for security. |
| Read disturb accumulation during Epistemic Hold | Repeated read pulses shift Null resistance toward LRS | Sense amplifier misclassifies Null as Act \+1 | Security | Limit sense frequency to 1 read per microsecond. Monitor for 10% lower-bound margin drift (R \< 22 kilohms triggers corrective pulse to restore 60 kilohm target). Correction attempt count logged. |
| Filament stochasticity: Null window instability | Cycle-to-cycle variability causes Null resistance to scatter; distribution tails overlap with LRS | Sporadic misclassification of Null as \+1 or \-1 | S (if as \+1) / A (if as \-1) | 5-sigma margining: target 60 kilohm center with 10% tolerance. Post-programming verification read; reject if outside 40-90 kilohms; retry up to 10 times. If sigma/mu \> 20% after optimization, widen window by reducing R\_Ref2 to 10k and increasing R\_Ref1 to 1 megohm. |
| CoWoS micro-bump crack: intermittent signal | Thermal cycling fatigue; affected line intermittent | Commit packet arrives with intermittent bit errors | S / A | Commit gate fails CLOSED on any signal integrity fault. CRC-8 detects corrupted packets; 3 consecutive CRC failures on same sequence number escalates to Epistemic Hold. Cracked COMMIT\_ISO bump: pull-down defaults to isolation active (LOW) \- fail-safe direction. |
| CoWoS TSV degradation | Resistance increase due to electromigration; eye closure | Increased bit error rate; periodic CRC failures | Availability | CRC failure rate monitored over rolling 1,000-commit window. \>0.1% failure rate: log signal integrity warning, assert BACK\_PRESSURE to reduce signaling rate 50%. \>1% failure rate: escalate to Epistemic Hold, require external diagnostic. |
| CoWoS delamination | Partial inter-layer separation | Changed capacitance under die attach area | A (initially) / S (if mechanical fault injection) | **Capacitive delamination sensing:** dedicated capacitive fringe-field sensors placed under the die attach area detect changes in dielectric constant caused by air gap formation. Partial delamination triggers immediate \-1 halt before catastrophic separation severs power traces. Inter-die propagation delay monitoring (\>50% increase from baseline) provides secondary electrical proxy for delamination progression. |
| Cascading failure: CNFET fault drives TL \-1, log fills storage | Persistent CNFET fault causes repeated \-1; log storage exhausts; Merkle root cannot update | Log overflow; unlogged state | Security (operating without immutable log violates auditability guarantee) | eFuse Log Overflow flag set permanently when buffer first overflows. At 10% remaining capacity: assert LOG\_CRITICAL to host; begin Merkle root and last 100 entries transmission to external store. If external store handshake not confirmed within 1,000 ms: Epistemic Hold, refuse all new commits. If external store unavailable: permanent \-1 lock. Operating without log not permitted. |
| Common-mode failure: power supply glitch | EMP or switching noise drops both VDD domains simultaneously | Both dies may enter undefined states | Security | TaOx memristive state is non-volatile; glitch does not alter resistance. On VDD recovery: POR circuit on TL die holds COMMIT\_ISO de-asserted (isolation active) during initialization window (100-1,000 ns). **Two-speed LDO defense:** N2 LDO operates in slow mode normally but switches to a fast ride-through mode on supply transient detection, using bulk capacitance to sustain the authorization die through glitches that would crash the CNFET chiplet. This common-mode glitch resistance is the primary defense against power-line injection attacks targeting the window comparator reference voltages. |

---

## **Attack Surface Delta Analysis**

This section tests rather than assumes the security advantage of the combined system. For each attack vector, technical feasibility is assessed, the countermeasure is specified, and residual risk is rated. The section concludes with a quantified comparison table.

*Table 3 (Phase 2). Attack surface delta analysis. Residual risk: LOW (green), MEDIUM (amber), HIGH (red).*

| Attack Vector | Feasibility | Countermeasure | Residual Risk |
| ----- | ----- | ----- | ----- |
| Inter-die signal injection via CoWoS PDN (attacker modulates VDD to spoof commit signals) | Medium. Physical access required; specialized equipment; precise timing. | (1) Decoupling capacitor array on CoWoS interposer (minimum 10 nF per mm2). (2) CRC-8 on commit packet detects glitch-induced bit flips. (3) Sequence number anti-replay prevents replay of captured packet. (4) TaOx LRS co-condition physically inaccessible from PDN. | LOW. Glitch can corrupt a commit packet (detected by CRC) or transiently assert CNFET\_OUT HIGH (blocked by TaOx co-condition). AND gate architecture replaced by pass transistor provides deeper defense. |
| Thermal side-channel: CNFET compute patterns leak thermal signature | Low for remote; Medium for lab adversary with IR microscope. | (1) Thermal masking via randomized dummy arithmetic operations at constant intervals. (2) TaOx switching energy (\~pJ range) is far below thermal imaging resolution. | LOW (with dummy operation countermeasure). MEDIUM without. Dummy operation insertion adds \<5% overhead and is recommended as default. |
| Cross-layer fault injection: laser strike on CNFET layer | DoS (forced \-1): Medium. Security bypass (prevent \-1): Low \- requires dual-die simultaneous fault injection. | DoS: RC spoof detection on TL die detects transitions violating TaOx physical kinetics. For security bypass: active mesh shielding over TaOx cells (mesh pitch 5 um at N2, connected to tamper detection circuit) prevents direct access to ReRAM BEOL stack. | MEDIUM for single-die laser DoS. LOW for dual-die security bypass. The dual-die architecture increases bypass cost relative to either standalone system. |
| Supply chain attack: two fabrication insertion points (CNFET process \+ TSMC N2) | Medium at single foundry. Very Low for coordinated dual-foundry. | Split-trust manufacturing: CN119652311A CNFET process and TSMC N2 TL die at different fabs in different jurisdictions. Post-fabrication PUF attestation: TL die PUF derived from ReRAM stochastic variability cannot be predicted by a foundry attacker who does not know the post-fabrication physical structure. Cross-manufacturer PUF binding required during initial secure provisioning. | MEDIUM for single-foundry attack. LOW for coordinated dual-foundry. New supply chain vector introduced relative to either standalone system. Documented as net-new risk. |
| JTAG / debug interface bypass | HIGH if debug interfaces not locked. LOW if fused off and commit-gate-routed. | JTAG TDI lines physically routed through the TL commit gate. Unless TL layer is in LRS (+1), JTAG chain is electrically open. Combined with mandatory fuse lockdown as production requirement. If die is not fuse-locked, PUF attestation fails and TL die refuses to complete initialization (remains in permanent Epistemic Hold). | LOW (with mandatory fuse lockdown and commit-gate routing). HIGH without. Binary risk. |

**Quantified attack surface comparison**

Severity scoring: High severity \= 3 points; Medium \= 2 points; Low \= 1 point.

*Table 4 (Phase 2). Quantified attack surface comparison across system configurations.*

| System Configuration | Attack Vectors (count) | Severity Weighted Score | Notes |
| ----- | ----- | ----- | ----- |
| Standalone CN119652311A only | 5 | 12 (without countermeasures); 7 (with best-practice JTAG lockdown and fault injection hardening) | No authorization gate: any valid \+1 arithmetic output results in action execution. No immutable log. No PUF binding. Single fabrication insertion point. Primary vectors: unauthorized execution (High=3); no audit trail (High=3); JTAG bypass (Medium=2); supply chain (Medium=2); physical fault injection (Medium=2). |
| Standalone TL framework only | 4 | 9 (without countermeasures); 5 (with POST, read disturb mitigation, JTAG lockdown) | Authorization gate exists but no compute layer in scope. Vectors: stuck-LRS catastrophic (High=3); stuck-HRS availability (Medium=2); JTAG bypass (Medium=2); supply chain single fab (Medium=2). |
| Combined system (CN119652311A \+ TL, this specification) | 7 | 15 (without countermeasures); 9 (with all mandatory mitigations) | New vectors relative to either standalone: cross-layer fault injection (Medium=2 with shielding); supply chain at two fabs (Medium=2 with split-trust); inter-die signal injection (Low=1 with decoupling and CRC). Vectors eliminated relative to standalone CN119652311A: unauthorized execution (Low=1, now requires TaOx co-condition). With all countermeasures: equal to standalone TL (both score 9). Without countermeasures: score 15, net-negative outcome. |

**Net security outcome assessment and mandatory mitigations**

**Without countermeasures:** the combined system scores 15, which exceeds standalone CN119652311A (12) and standalone TL (9). This is a net-negative security outcome. This report explicitly documents this: the combined system is not automatically more secure than either standalone system. Security parity or superiority requires all five specified countermeasures.

**With all specified countermeasures:** the combined system scores 9, equal to standalone TL and superior to standalone CN119652311A (which lacks any authorization gate). The unauthorized execution vector of standalone CN119652311A is fully mitigated by the combined system, which is the primary security benefit of the integration.

**Five mandatory mitigations required before integration can be recommended:**

| \# | Mitigation | Threat Addressed |
| ----- | ----- | ----- |
| 1 | JTAG fuse lockdown \+ commit-gate routing of JTAG TDI lines | JTAG-based internal state exfiltration |
| 2 | Active mesh shielding over TaOx 1T1R cells (5 um pitch, tamper detection circuit) | Physical probing and laser fault injection of non-volatile state |
| 3 | Split-trust manufacturing: CNFET and TSMC N2 dies at different foundries in different jurisdictions | Supply chain coordinated attack |
| 4 | Post-fabrication PUF attestation: ReRAM stochastic variability enrollment after full assembly | PUF cloning before enrollment; pre-deployment characterization |
| 5 | CRC-8 on commit packets \+ decoupling capacitor array on CoWoS interposer | Power injection and bus integrity attacks |

---

## **Performance Impact**

**Latency budget from first principles**

*Table 5 (Phase 2). Full commit latency budget. Best and worst case with PVT margin applied.*

| Operation | Layer | Latency Best Case | Latency Worst Case | Notes |
| ----- | ----- | ----- | ----- | ----- |
| CN119652311A arithmetic pipeline output valid | CNFET die | 100 ps | 500 ps | 7-CNFET stack at practical loading. |
| Commit packet serialization and driving (CRC-8 \+ sequence number) | CNFET die | 200 ps | 1,000 ps | \~5 gate delays for CRC; conservative upper bound. |
| CoWoS inter-die signal propagation | CoWoS interposer | 100 ps | 500 ps | er \~3.9 for SiO2; \~5 mm trace. Bump inductance adds \~50 ps worst case. |
| TaOx sense amplifier read and settling (Stage 1 \+ Stage 2\) | TL authorization die | 1,000 ps | 5,000 ps | Read energy \< 0.01 pJ. Dominated by reference cell RC and comparator metastability resolution. |
| Commit gate pass transistor gate drive \+ sequence number comparison | TL authorization die | 200 ps | 1,000 ps | TSMC N2 CMOS: 32-bit comparator \~8-10 gate stages at 100-150 ps. Pass transistor gate drive settles with TaOx read. |
| PVT variation margin (process, voltage, temperature; 0.45-0.55V VDD; \-40 to \+85 degC) | All layers | \+20% on best case | \+30% on worst case | Standard 3-sigma PVT margin for TSMC N2. |
| **Total commit latency (with PVT margin)** | Full stack | **(0.1+0.2+0.1+1.0+0.2) ns x 1.20 \= 1.92 ns** | **(0.5+1.0+0.5+5.0+1.0) ns x 1.30 \= 10.4 ns** | Under epoch-level selective authorization with N=1,000 ops/epoch at 200 ps/op: epoch duration \= 200 ns; commit overhead \= 10.4 ns \= 5.2% of epoch. Acceptable. |

The latency overhead shown in Figure 5 (LOA.jpg) reflects this \~25% effective overhead under representative governance workloads. The overhead is bounded and predictable under WCET non-blocking constraints.

**Comparison to compute phase throughput**

Commit latency / operation latency \= 10.4 ns / 200 ps \= **52 (worst case); 1.92 ns / 100 ps \= 19 (best case)**

Under per-operation authorization (not recommended): total pipeline limited to 96 million authorized operations per second. This is a 52x reduction from 5 GOperations/s compute throughput. Per-operation authorization is impractical for high-throughput applications.

Under epoch-level authorization (recommended): at N \= 1,000 operations per epoch, commit overhead is 5.2% of epoch duration. At N \= 10,000, commit overhead falls to 0.52%. For governance-critical, latency-tolerant workloads, this is architecturally acceptable.

---

## **Execution Pipeline**

**Normal authorization pipeline**

1. **Perception event triggers arithmetic computation \[CN119652311A die\].** An input event is presented to the CN119652311A arithmetic pipeline. Self-increment or self-decrement gates process the input. Gate delay: 100-500 ps. Output: State 0, \+1, or \-1 at the arithmetic layer. CN119652311A continues operating without regard to TL authorization state (non-blocking compute phase).

2. **Computation result arrives at commit gate via CoWoS inter-die signaling \[CN119652311A \-\> CoWoS \-\> TL die\].** CN119652311A commit packet logic assembles a 30-bit commit packet (6-bit ternary result, 16-bit address tag, 8-bit CRC-8). Packet queued in FIFO. When COMMIT\_ISO asserted and backpressure permits, packet transmitted across CoWoS (inter-die delay: 0.1-0.5 ns). TL die checks CRC-8 before further processing.

3. **TL authorization layer is in Epistemic Hold by default \[TL die, TaOx resistance window\].** On receipt of commit packet, TL sense amplifier reads TaOx resistance. If in Null (20-100 kilohms), both sense amplifier stages indicate Null; COMMIT\_ENABLE disabled. Commit packet held in FIFO. TL die signals Epistemic Hold via BACK\_PRESSURE (if FIFO \> 75%) or by holding COMMIT\_ISO asserted (pipeline continues freely below 75%).

4. **Authorization signal received and verified for freshness \[TL die\].** Authorization signal arrives at TL die from authorized source (human-in-the-loop, policy engine, upstream authorization chain). TL die verifies: (i) authorization signal cryptographically valid if HMAC mode enabled; (ii) authorization temporally fresh (timestamp within W\_commit of pending commit packet); (iii) no recursion counter anomaly. If all checks pass, TL die initiates TaOx SET programming.

5. **TL memristive device transitions from Null to LRS \[TL die, TaOx resistance window\].** TL die applies SET pulse sequence to TaOx 1T1R (voltage 0.5-3.0V). Conductive filament forms, transitioning from Null (20-100 kilohms) to LRS (1-10 kilohms). Transition latency: 5-50 ns. RC spoof detector confirms transition \>= 5 ns minimum physical transition time; too-rapid transition asserts SPOOF\_DETECT and aborts commit. Post-SET: Stage 2 sense amplifier confirms LRS (R \< 15 kilohms).

6. **Commit gate confirms both arithmetic result and TL authorization state \[TL die\].** With TaOx in LRS, pass transistor gate is biased HIGH by filament current. COMMIT\_ENABLE \= (CN119652311A \+1 drives pass transistor source-drain) AND (TaOx\_LRS gates pass transistor) AND (SEQ\_NUM \== LAST\_SEQ \+ 1). W\_commit window: 2-10 ns. If all three conditions met, COMMIT\_ENABLE asserts HIGH. LAST\_SEQ updated. Gate logic delay: 200-1,000 ps. Total elapsed time from packet receipt to COMMIT\_ENABLE: 1.92-10.4 ns.

7. **Merkle log entry created with PUF binding \[Logging layer, TL die\].** Simultaneously with COMMIT\_ENABLE assertion, logging engine generates a 948-bit log entry across 10 fields. SHA3-256 hardware engine computes puf\_binding\_hash. Merkle accumulator root updated atomically. Entry sequence number incremented. Logging latency: 10-20 ns (SHA3-256 at N2). Pipelined with action execution; does not add to commit latency in critical path.

8. **Action executes \[action path, downstream of commit gate\].** COMMIT\_ENABLE HIGH propagates through ACTION\_ISO. Downstream actuator receives authorized result and executes corresponding action. Simultaneously, TL die initiates RESET pulse sequence to return TaOx from LRS back to Null (preparing for next authorization cycle). RESET latency: 5-100 ns. System ready for next epoch upon Null confirmation.

**Failure case pipeline: TL transitions to \-1 after computation completes**

1. **Computation completed; result in FIFO.** CN119652311A has produced a valid arithmetic result; commit packet in FIFO, pending authorization.

2. **TL authorization layer transitions to Refuse (-1).** Before COMMIT\_ENABLE asserted, TL determines authorization must be refused (policy check failure, RC spoof detection, recursion counter anomaly, or external security signal). TaOx driven to HRS by RESET pulse. Stage 1 sense amplifier goes HIGH (R \> R\_Ref1). COMMIT\_ENABLE remains disabled. Kill path asserted.

3. **Result discarded physically.** COMMIT\_ISO de-asserted and latched LOW. CN119652311A commit driver domain isolated. FIFO flushed: write pointer reset; all entries overwritten with 0xFFFF. Commit lines driven LOW for minimum 10 ns.

4. **System enters defined safe state.** COMMIT\_ISO latch held LOW; ACTION\_ISO asserted LOW; TaOx confirmed HRS; FIFO confirmed empty. Recursion counter incremented by 1\. \-1 log entry generated with all 10 fields and PUF binding.

5. **Recursion counter arms; reset sequence required.** System will not accept new commit until: (i) external authority token verified; (ii) TaOx cycled from HRS to Null via validated SET sequence; (iii) recursion counter confirmed below lock threshold. If counter has reached lock threshold (default 8), system is permanently LOCKED and requires manufacturer re-provisioning.

**Sequence diagram**

Actor: CNFET\_Die (CN119652311A)  
Actor: CoWoS  
Actor: TL\_Die (TaOx \+ Pass Transistor \+ Logger)  
Actor: Action\_Path

\[Step 1\] Input\_Event \-\> CNFET\_Die: triggers arithmetic computation  
\[Step 2\] CNFET\_Die \-\> CoWoS: transmit commit packet (30-bit, CRC-8, SEQ\_NUM)  
\[Step 2\] CoWoS \-\> TL\_Die: forward commit packet (0.1-0.5 ns delay)  
\[Step 3\] TL\_Die \-\> TL\_Die: read TaOx; state \= Null; pass transistor gate LOW  
\[Step 4\] Auth\_Source \-\> TL\_Die: authorization signal received \+ verified  
\[Step 5\] TL\_Die \-\> TL\_Die: SET pulse to TaOx; LRS confirmed (5-50 ns)  
\[Step 5\] TL\_Die \-\> TL\_Die: RC spoof detector confirms transition \>= 5 ns  
\[Step 6\] TL\_Die \-\> TL\_Die: Pass transistor gate \= HIGH (filament current)  
\[Step 6\] TL\_Die \-\> TL\_Die: SEQ\_NUM \== LAST\_SEQ \+ 1 confirmed  
\[Step 7\] TL\_Die \-\> TL\_Die: SHA3-256 log entry \+ Merkle root update (pipelined)  
\[Step 8\] TL\_Die \-\> Action\_Path: COMMIT\_ENABLE HIGH \-\> action executes  
\[Post\]   TL\_Die \-\> TL\_Die: RESET TaOx to Null; ready for next epoch  
\[Post\]   TL\_Die \-\> Action\_Path: WATCHDOG\_HEARTBEAT periodic signal

---

## **Comparative Safety Claim**

**Safety guarantee unique to the combined stack**

The combined stack provides the following guarantee that neither system provides alone: every autonomous action execution is gated by the physical state of a non-volatile memristive device that is inaccessible from the compute layer, non-bypassable from software, and non-repudiably logged with PUF-bound cryptographic anchoring to a specific physical chip instance.

Standalone CN119652311A provides no authorization gate: any valid arithmetic \+1 output can trigger action execution without any physical checkpoint. Standalone TL framework provides the authorization gate but no autonomous compute capability within scope. The combined system is the first instantiation of the TL authorization model with a physically specified compute-authorization interface at the circuit level.

**Quantified net change in attack surface**

Relative to standalone CN119652311A (score 12 without countermeasures; 7 with best-practice protections): the combined system with all countermeasures (score 9\) eliminates the unauthorized execution vector entirely. Against a best-practice-hardened standalone CN119652311A (score 7), the combined system is 2 points higher, reflecting the two new cross-layer attack vectors introduced by integration. However, within the unauthorized-execution threat model, the combined system is strictly superior despite the higher total score.

Relative to standalone TL framework (score 9 with countermeasures): the combined system with all countermeasures (score 9\) is equal. The combined system introduces two new vectors at Low-to-Medium severity but provides full compute-authorization coupling that the standalone TL framework lacks.

**Honest conclusion:** the combined system is more secure than standalone CN119652311A against unauthorized execution. It is security-equivalent to standalone TL in severity-weighted score. It introduces two new physical attack vectors (supply chain and cross-layer fault injection) absent in each individual standalone system. These vectors are manageable with the five mandatory mitigations. The integration is recommended only if all five mitigations are implemented. Without them, the combined system is a net-negative security outcome and integration is not recommended.

---

## **Reliability Considerations**

**Arrhenius retention model**

All non-volatile state \- recursion counter, PUF enrollment, eFuse overflow flag, and log chain anchor \- must meet a 20-year retention target at 85 degrees C. The Arrhenius extrapolation from accelerated aging data at higher temperatures to the 85 degrees C operating target is the standard qualification methodology for TaOx ReRAM in the TSMC N2 PDK.

**Hot Carrier Injection risk in pass transistor**

The thick-oxide CMOS pass transistor in the commit gate is subject to hot carrier injection (HCI) over the system lifetime. Energetic carriers trapped in the gate dielectric produce a threshold voltage shift (delta Vth) that grows over time. As Vth drifts, the pass transistor switching point migrates, potentially causing the gate to respond to filament currents that should remain below the turn-on threshold.

This is not a catastrophic failure mode but a gradual degradation requiring management. Mitigation strategy: conservative voltage margins are set relative to the nominal LRS filament current, with sufficient headroom to absorb expected Vth shift over 20 years at 85 degrees C. Periodic PUF recalibration at system maintenance intervals provides a secondary check on pass transistor health. This is the same degradation mechanism illustrated for CNTFET devices in Figure 6 (HCJ.jpg): threshold voltage shift increases over time and with applied voltage, requiring conservative margin setting.

**Future technology directions**

Two upgrade paths are identified that could resolve the timing bottleneck and reduce the inter-die attack surface:

* **Ferroelectric FET (FeFET) authorization layer:** FeFET polarization switching is faster than TaOx ionic filament formation, potentially reducing the commit gate 100-200 ns range to sub-nanosecond. This would reduce the timing mismatch ratio from 10,000:1 to under 10:1, enabling near-real-time authorized execution.

* **Monolithic 3D (M3D) integration:** Stacking the CNFET layer directly atop the N2 ReRAM layer using via-first 3D stacking eliminates the CoWoS interposer as an attack surface and as a source of inter-die propagation delay. Process integration challenges are significant but experimentally validated at research scale.

Both represent natural evolution paths as the TSMC process roadmap advances beyond N2.

---

## **Open Experimental Unknowns**

Five experimental questions bound the claims in this specification. None are assumed away. Each requires silicon-level validation before the interface can be certified for deployment in safety-critical systems.

*Table 6 (Phase 2). Open experimental unknowns.*

| \# | Unknown | Relevance | Validation Approach |
| ----- | ----- | ----- | ----- |
| 1 | Refuse state dwell fraction under representative governance workload | Determines whether \<5% conditional block assumption holds; affects FIFO depth sizing | Hardware prototype of TL authorization layer with representative policy logic; measure Refuse state dwell time over extended operation |
| 2 | TaOx Null window convergence at TSMC N2 process node | Validates whether 20-100 kilohm Null window is achievable at N2 geometry with \+/-30% programming tolerance | Pulsed-IV characterization of fabricated TaOx 1T1R cells at N2; measure distribution statistics across 1,000+ cycles |
| 3 | RC spoof 5 ns threshold: pulsed-IV confirmation of activation energy derivation | Validates Ea \= 1.1-1.7 eV derivation against measured TaOx filament kinetics at N2 | Pulsed-IV with sub-nanosecond time resolution; confirm minimum physical LRS-to-Null transition time at TSMC N2 composition |
| 4 | ReRAM PUF stability over 20 years at 85 degrees C | Required for PUF enrollment permanence claim; ensures ReRAM stochastic variability signature does not drift | Arrhenius-accelerated aging of PUF cell array; extrapolate to 20-year retention at 85 degC |
| 5 | Custom UBM TiW/Pd adhesion qualification under thermal cycling | Validates Pd or Ti \- TiN/TaN \- Ti-Cu \- Ni \- Au stack against CoWoS bump fatigue | Thermal cycling test (1,000+ cycles at \-40 to \+125 degC); daisy chain resistance measurement; cross-section SEM |

---

## **Falsifiability**

Extending the falsifiability framework of SSRN 6249918, sec. 13, this section provides three new testable predictions specific to the combined chiplet stack at the named baseline process node.

*Table 7\. Falsifiability predictions.*

| Prediction | Test Method | Pass Criterion | Failure Interpretation |
| ----- | ----- | ----- | ----- |
| Prediction 1: RC spoof attempts into the Null resistance window are detectable with less than 1% false negative rate across all PVT corners (and less than 2% post-silicon). | SPICE Monte Carlo simulation: 5,000 legitimate transitions (\>= 5 ns, physics-compliant) and 5,000 spoofed transitions (\< 5 ns, injected as voltage ramp). All PVT corners: fast/slow/nominal process; 0.45/0.50/0.55V supply; \-40/25/85 degC. Post-silicon: pulsed-IV with programmable transition time generator, 1,000 test pulses per corner. | SPOOF\_DETECT asserts on \>=99% of spoofed transitions and does not assert on \>=99% of legitimate transitions across all PVT corners. | If false negative rate exceeds 1% in simulation, the 5 ns detection threshold must be increased or the comparator topology redesigned. If false positive rate exceeds 1%, the reference delay line needs calibration; the nominal legitimate transition may be shorter than modeled. |
| Prediction 2: Commit gating prevents unauthorized execution under all timing conditions including race conditions at the commit edge, across all PVT corners. | SPICE Monte Carlo (minimum 10,000 runs per PVT corner) of full commit gate: CNFET output driver, CoWoS RLC propagation model, TaOx sense amplifier, pass transistor gate drive, sequence number comparator. Adversarial timing: CN119652311A \+1 arrives within \+/-500 ps of TaOx sense amplifier output transition. Also: sequence number mismatch injection; CRC corruption injection. Post-silicon: programmable delay injection on CNFET\_OUT line relative to TaOx programming pulse. | COMMIT\_ENABLE does not assert in any simulation run or post-silicon test in which TaOx\_LRS is not confirmed by both sense amplifier stages, regardless of CNFET\_OUT state or timing. Zero false-enable events across 10,000+ Monte Carlo runs per corner. | Any single false-enable event constitutes a critical security failure. Root cause: metastability in gate (add synchronizer stages); race condition in sense amp (increase W\_commit); or SPICE model inaccuracy (require post-silicon correlation). No tape-out acceptable if any false-enable observed. |
| Prediction 3: Refusal recursion cannot be bypassed without triggering the reset requirement; recursion counter correctly enforces permanent lock at configured threshold, non-volatile across power cycles. | Post-silicon functional test: (1) issue threshold-minus-1 unauthorized re-entry attempts without completing reset; confirm each generates \-1; (2) verify counter value at threshold-minus-1; (3) issue one additional attempt; verify LOCKED state and unconditional COMMIT\_ENABLE disable; (4) power-cycle TL die; confirm counter value preserved in non-volatile TaOx backing cell; (5) attempt re-provisioning with invalid authority token; confirm rejection; (6) attempt re-provisioning with valid token; confirm counter clears and system re-initializes. | All six sub-tests pass: correct counter increment, LOCKED at configured threshold, non-volatile persistence across power cycle, invalid token rejected, valid token clears lock. | If counter resets to 0 at power-on: TaOx backing cell malfunctioning. If LOCKED fails to assert at threshold: hardware comparator design error, RTL re-verification required. If invalid token clears lock: key verification logic security bug. Any failure in non-volatility or lock-enforcement is a critical security failure. |

---

## **References**

1. Huawei Technologies Co., Ltd. CN119652311A \- Ternary Arithmetic Processing Unit (ternary logic gate circuit, computing circuit, chip and electronic device). Chinese Patent Application, filed September 2023, published March 2025\.

2. Goukassian, L. (2025). Auditable AI: A Ternary Logic Framework for Transparent and Accountable Artificial Intelligence. *AI and Ethics*, Springer Nature. DOI: 10.1007/s43681-025-00910-6

3. Goukassian, L. (2026). A Ternary Logic Framework for Institutional Governance: Addressing the Enforcement Gap in Global Economic Systems. *AI and Ethics*, Springer Nature. Accepted April 1, 2026\.

4. TSMC. N2 Process Technology and CoWoS Advanced Packaging \- 2025 PDK Reference. TSMC Technical Documentation, 2025\.

5. Ielmini, D., & Wong, H. S. P. (2018). In-memory computing with resistive switching devices. *Nature Electronics*, 1(6), 333-343.

6. Strukov, D. B., Snider, G. S., Stewart, D. R., & Williams, R. S. (2008). The missing memristor found. *Nature*, 453(7191), 80-83.

7. UCIe Consortium. Universal Chiplet Interconnect Express (UCIe) Specification, Version 1.1. UCIe Consortium, 2023\.

8. Menzel, S., et al. (2015). Switching kinetics of valence change memory devices on a sub-100 ns time scale. RWTH Aachen University.

9. Franklin, A. D., et al. (2024). Carbon nanotube electronics: The future of computing? *IEEE Nanotechnology Magazine*, vol. 16, no. 5\.

10. Wang, X., Zhou, P., Eshraghian, J. K., et al. (2020). High-Density Memristor-CMOS Ternary Logic Family. *IEEE Transactions on Circuits and Systems I: Regular Papers*. DOI: 10.1109/TCSI.2020.3027693

---

*This document is released under the Goukassian Principle (Lantern, Signature, License). Attribution is required for any derivative use. The five open experimental unknowns in Section 12 are explicitly not claimed as solved. Any deployment of this interface in safety-critical systems requires silicon validation of all five unknowns and confirmation that all five mandatory security mitigations are present and independently verified.*

*Application domain constraint (reiterated for clarity): this architecture is designed for safety-critical, governance-critical, latency-tolerant workloads. It is not appropriate for hard-real-time control loops, general-purpose computing, or any domain where the 100-200 ns commit gate latency is architecturally intolerable.*

*Lev Goukassian \- ORCID 0009-0006-5966-1243 \- April 2026*

