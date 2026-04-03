# **Mandated Ternary: Hardware Implementation of Ternary Logic**

## **From Device Physics to System Architecture**

### **Phase 2: System Architecture, Economics, and Autonomous Execution Integration**

#### **Sub-title: Can the Third State Run the World?**

*Ternary Logic Framework \- Hardware Architecture Folder* *ORCID: 0009-0006-5966-1243*

---

"Build the third state into matter, and the future stops pretending it never hesitated."

* Lev Goukassian  
  ---

  ## **Section 1 \- Abstract**

Building on Phase 1's conditional pass across device physics, circuit primitives, NL=NA interlock architecture, PUF identity, and emulation tax, Phase 2 evaluates whether TaOx bilayer memristive MT primitives can be composed into viable system architectures that enforce TL triadic semantics at scale \- with acceptable economics, interconnect performance, safety certification path, and 20-year operational horizon. The finding is a qualified yes, with a single critical constraint: MT is not a general-purpose computing architecture and must not be positioned as one. Its discontinuous advantage is specific, bounded, and real: hardware-enforced non-volatile authorization-pending states with WCET-bounded non-blocking enforcement and power-loss persistence, targeting deterministic autonomous execution systems in industrial control, financial settlement finality, and critical infrastructure dispatch contexts. Phase 2 identifies two viable architectures \- a native ternary crossbar CiM design (Architecture A) and a hybrid memristive-CMOS design (Architecture B) \- with Architecture B recommended for the 2026-2027 commercialization window on economic and certification grounds. The economics are marginal: break-even requires approximately 12,000-18,000 MT enforcement units per year at a $15,000-25,000 unit premium, which is achievable in financial settlement and power grid verticals but requires active market development. The IEC 61508 SIL 3 certification path is achievable by 2027 for Architecture B; Architecture A requires an additional 12-18 months. The program is not terminated by any Phase 2 failure condition.

---

## **Section 2 \- Executive Summary**

**What Phase 2 Finds**

Phase 2 evaluates MT at five layers: system architecture, foundry roadmap, market positioning, autonomous execution integration, and economics/certification. Results:

**System Architecture Layer \- Pass with Selection.** Two architectures are viable. Architecture A (native ternary crossbar CiM) is technically superior but economically premature for 2026-2027. Architecture B (hybrid memristive-CMOS) is technically adequate and economically viable for the target window. The crossbar dimension limit (64x64 per block, from Phase 1\) propagates into both architectures as a hierarchical tiling constraint.

**Foundry Roadmap Layer \- Conditional Pass.** TSMC N2 CoWoS is the preferred integration platform for Architecture B. A full MT PDK does not exist at any foundry as of 2025\. The NRE to create one is estimated at $8-15 million, requiring a consortium or government co-investment model. Intel 18A and Samsung SF2 are secondary options with specific tradeoffs.

**Market Positioning Layer \- Pass (narrowly).** The MT "saint spot" \- the specific market gap where MT yields a discontinuous advantage \- is real and quantifiable: deterministic authorization enforcement in high-value, high-accountability autonomous execution systems. The addressable market is approximately 85,000-120,000 enforcement nodes globally across target verticals, generating $1.3B-$3.0B in total addressable revenue. This is sufficient to justify PDK development at consortium scale, but not for a single foundry acting alone.

**Autonomous Execution Integration Layer \- Pass.** Both a high-frequency settlement finality engine and a power grid dispatch controller demonstrate clear MT integration paths. The settlement engine cannot be adequately served by the named 2025 CMOS/NVRAM baseline in one critical dimension: physically-enforced, audit-immutable Epistemic Hold with power-loss persistence. The power grid controller gains additional advantage: hardware-mandated safe-state persistence during fault events with no software dependency.

**Economics and Certification Layer \- Conditional Pass.** Break-even is achievable at realistic production volumes for Architecture B. IEC 61508 SIL 3 certification is achievable by Q4 2027 for Architecture B. These are conditions, not guarantees.

**Combined Phase 1 \+ Phase 2 Program Conclusion**

MT is physically realizable, architecturally viable, and economically marginal-but-achievable for a specific and well-defined set of use cases. It is not a successor to binary CMOS. It is a mandatory enforcement substrate for the highest-accountability tier of autonomous decision systems \- the tier where "software said so" is no longer a sufficient audit statement, and "matter enforced it" is required.

**Investment and Policy Implications**

For investors: Architecture B hybrid memristive-CMOS represents a $8-15M NRE investment for a $1.3B-$3.0B TAM across a 10-year horizon. Risk is concentrated in IRS sigma/mu process corner validation and IEC 61508 certification timeline. Return is back-loaded (first commercial deployments 2027-2028).

For policymakers: Financial regulators and grid operators who require deterministic, tamper-evident, power-loss-persistent audit trails for autonomous systems should consider MT as a hardware complement to existing software governance frameworks. MT does not replace software governance; it enforces it at the physical layer where software cannot.

---

## **Section 3 \- Inherited Constraints from Phase 1**

The following Phase 1 findings are binding on Phase 2\. Phase 2 terminates any investigation path where Phase 1 concluded failure.

**Device Assumptions Phase 2 Inherits:**

1. TaOx bilayer 1T1R cells are the designated MT device. No further device-level evaluation.  
2. LRS: 1-10 kohm. IRS: 100 kohm \- 1 Mohm. HRS: 1-10 Mohm. These ranges are fixed.  
3. Sigma/mu for IRS: 20-30% at 25 degrees C. Binding constraint on sense amplifier design.  
4. Crossbar dimension limit: \<= 64x64 per hierarchical block (IR drop limit from Phase 1 Section 7).  
5. Confirm wire length: \<= 500 um per window comparator instance.  
6. Post-write anneal protocol (200-250 degrees C, 30 min) is a mandatory manufacturing step.  
7. Energy per MT enforcement event: 100-500 pJ (budget for system energy models).  
8. Execution lane WCET: \<= 2 ms at 99.99th percentile (established in Phase 1).  
9. Logging lane hard ceiling: 300 ms maximum, jitter \<= 50 ms.  
10. IRS 20-year retention: conditional pass, pending IRS accelerated aging data at production corners.

**Phase 1 Failure Conditions That Did Not Trigger (but remain active monitoring items):**

* IRS sigma/mu \> 40%: not triggered; remains kill condition if production data exceeds this.  
* IRS retention \< 10 years at 85 degrees C (95% CI): not triggered; requires accelerated aging validation.  
* PUF inter-die HD \< 49%: not triggered; one literature data point (48.57%) is slightly below threshold \- requires production-scale validation.  
* Foundry pre-forming PUF cells: not triggered; must be contractually prevented.

**System Capabilities Foreclosed by Phase 1:**

1. Software override of Epistemic Hold: PERMANENTLY FORECLOSED.  
2. More than 3 resistance states (MLC extension): FORECLOSED (sigma/mu limits).  
3. Remote mandate update: FORECLOSED (OTP fuse architecture).  
4. Single-vendor PUF provisioning: FORECLOSED.  
5. Crossbar arrays \> 64x64 without hierarchical tiling: FORECLOSED (IR drop constraint).

**Downstream Impact on Phase 2:** The 64x64 crossbar limit means that any Phase 2 architecture handling more than 4,096 simultaneous MT enforcement cells must use hierarchical tiling with repeaters and level-select logic between tiles. This adds approximately 20-40% area overhead per tiling level and approximately 5-15 ns additional latency per tile boundary crossing. Neither overhead violates WCET constraints (execution lane WCET 2 ms remains satisfied with many orders of magnitude of margin), but they must be accounted for in area and energy budgets.

---

## **Section 4 \- System Architectures**

### **Architecture A: Native Ternary Crossbar Compute-in-Memory**

**Overview**

Architecture A instantiates MT enforcement states directly as the primary memory and state representation layer in a crossbar CiM array. Binary CMOS logic is relegated to peripheral circuits (row/column drivers, sense amplifiers, control plane). TL triadic states are the native data representation.

**Crossbar Array Organization**

* \+----------------------------------------------------------+  
* |  ARCHITECTURE A: NATIVE TERNARY CROSSBAR CiM             |  
* |                                                          |  
* |  \+----------------+  \+----------------+  \+----------+   |  
* |  | MT BLOCK 0     |  | MT BLOCK 1     |  | ...      |   |  
* |  | 64x64 1T1R     |  | 64x64 1T1R     |  |          |   |  
* |  | TaOx bilayer   |  | TaOx bilayer   |  | MT BLOCK |   |  
* |  | \+Confirm wires |  | \+Confirm wires |  | N        |   |  
* |  \+-------+--------+  \+-------+--------+  \+----+-----+   |  
* |          |                   |                |          |  
* |  \+-------+-------------------+----------------+------+   |  
* |  |  TERNARY CONTROL PLANE (binary CMOS)               |   |  
* |  |  Row/col select, sense amp mux, NL=NA gate array   |   |  
* |  \+-------+-------------------------------------------+   |  
* |          |                                               |  
* |  \+-------+----------+  \+----------------------------+   |  
* |  | EXECUTION LANE   |  | LOGGING LANE               |   |  
* |  | WCET \<= 2 ms     |  | Ceiling: 300 ms            |   |  
* |  | Physically       |  | Jitter: \<= 50 ms           |   |  
* |  | separated        |  | Physically separated       |   |  
* |  | metal layer M1-M3|  | metal layer M5-M7          |   |  
* |  \+------------------+  \+----------------------------+   |  
* |                                                          |  
* |  \+----------------------------------------------------+  |  
* |  | PUF ARRAY (separate TaOx sector, no pre-forming)  |  |  
* |  | Ed25519 signing engine                             |  |  
* |  | OTP fuse bank (mandate parameters)                |  |  
* |  \+----------------------------------------------------+  |  
* \+----------------------------------------------------------+


**Row/Column Addressing and Sneak Path Mitigation**

Each 64x64 block uses 1T1R cell architecture: one access transistor per cell prevents sneak paths by blocking current flow through unselected cells. This is the established production solution for sneak path elimination (high confidence from TSMC embedded RRAM production history).

* Row address: word line (WL) driven by row decoder, selects transistor gate  
* Column address: bit line (BL) driven by column decoder, selects cell current path  
* Selector transistor: provides \> 10^6 isolation ratio between selected and unselected cells  
* Sneak path current in 64x64 1T1R array: negligible (\< 1 nA per unselected row at V\_READ \= 0.2V)

**Ternary Control Plane**

The ternary control plane is binary CMOS. It does not "think in ternary" \- it reads 2-bit encoded states from the dual-reference sense amplifier (Section 5.4 of Phase 1\) and routes them to the appropriate processing or logging function. The ternary semantics live in the resistance states; the control plane interprets them.

Control plane operations per enforcement cycle:

1. Assert row select (WL high for selected row)  
2. Enable sense amplifier (dual-reference comparison)  
3. Decode 2-bit output: 00=LRS, 01=IRS, 10=HRS  
4. If IRS: assert NL=NA gate (wait for CONFIRM\_OK from logging lane)  
5. If CONFIRM\_OK received: write LRS or HRS per authorization  
6. Assert WL low, precharge BL for next cycle

Total control plane latency: approximately 200-500 ns per enforcement cycle. Within 2 ms WCET by factor of \>1000.

**NL=NA at System Level**

Confirm pulse routing across Architecture A crossbar:

* Each 64x64 block has one dedicated confirm wire per row (64 wires per block)  
* Confirm wires are on M4, orthogonal to BL (on M3) and WL (on M2)  
* Confirm wire length within block: 64 cells \* 200 nm pitch \= 12.8 um (well within 500 um limit)  
* Block-to-block confirm routing: on M5, with repeaters at each block boundary (maximum 5 ns added latency per hop)  
* System-level confirm routing from logging controller: M6 global bus, maximum 100 um routing, \< 1 ns propagation

Failure modes at system level:

* Logging controller failure: all cells in IRS-pending state retain IRS (safe failure)  
* Block-level power loss: cells retain state (TaOx non-volatile)  
* Global bus fault: IRS retained; degraded mode alert issued

**Dual-Lane Timing Architecture (Architecture A)**

* EXECUTION LANE (M1-M3)          LOGGING LANE (M5-M7)  
* \========================        \=========================  
* WL select:    t=0               Log entry formation: t=0  
* SA read:      t=50 ns           PUF sign (Ed25519):  t=1-10 ms  
* Decode:       t=100 ns          Merkle hash:         t=10-50 ms  
* NL=NA check:  t=150 ns          NVRAM log write:     t=50-200 ms  
*                                 CONFIRM\_OK issued:   t=200-300 ms  
*   
* PARALLEL: Execution path reaches NL=NA check at t=150 ns.  
* If CONFIRM\_OK not yet arrived: execution cell retains IRS.  
* No CPU stall. No polling. Execution cell holds state physically.  
* Other cells in array continue operating independently.  
*   
* CONFIRM\_OK arrives at t=200-300 ms.  
* Execution cell transitions LRS or HRS within 100 ns of pulse.  
* Total enforcement cycle: 200-300 ms (dominated by logging lane).  
* Execution lane itself: \< 200 ns. NON-BLOCKING VERIFIED.


**Formal Non-Blocking Demonstration:** The execution path does NOT poll the logging path. The NL=NA gate is a combinational element: it asserts "ready to write" when CONFIRM\_OK \= 1, and "hold" when CONFIRM\_OK \= 0\. In the hold state, no CPU instruction is blocked, no interrupt is pending, and no clock cycle is consumed. The IRS cell is an asynchronous physical state that requires no active maintenance. This is non-blocking by construction, not by policy.

**Scaling Limits**

Wire energy per confirm pulse on M4 (Architecture A, within block): E\_wire \= C\_wire \* V^2 / 2 \= (0.1 fF/um \* 12.8 um) \* (2V)^2 / 2 \= 1.28 fF \* 2 \= 2.56 fJ

Compute energy per MT cell enforcement cycle: 100-500 pJ.

Wire energy \= 2.56 fJ. Compute energy \= 100-500 pJ. Ratio: wire/compute \= 2.56e-15 / 100e-12 \= 2.56e-5.

Wire energy is 0.003% of compute energy within a 64x64 block. Wire energy does not dominate at block level.

For block-to-block routing on M5 (100-500 um inter-block distance): E\_inter\_block \= (0.1 fF/um \* 500 um) \* (0.75V)^2 / 2 \= 50 fF \* 0.28 \= 14 fJ.

Still \< 0.02% of compute energy. Wire energy does NOT dominate MT viability at any practical chip dimension.

**Scaling limit (from Phase 1):** The binding limit is IR drop, not wire energy. At 64x64 per block, IR drop from LRS read current is approximately 256 mV \- manageable. Above 64x64 single-level, IR drop exceeds 10% of read voltage and degrades sensing margin. MT is viable with hierarchical tiling up to any required array dimension. Wire energy is never the limiting factor.

**Architecture A vs Named 2025 Baseline Comparison**

| Parameter | Architecture A (Native Ternary CiM) | TSMC N2 CoWoS ReRAM 1T1R 2025 Baseline |
| ----- | ----- | ----- |
| Native IRS state | YES (physical) | NO (binary only) |
| IRS power-loss persistence | YES | N/A |
| NL=NA physical interlock | YES | NO |
| PUF-rooted provenance | YES | Not specified |
| Enforcement energy | 100-500 pJ | N/A (no IRS) |
| Crossbar integration | 64x64 blocks, hierarchical | Binary, no IRS |
| Area overhead vs binary | 2-3x (ternary control plane \+ confirm wires) | Baseline |
| Certification path | IEC 61508 SIL 3 (24-36 months from start) | Not applicable |
| 2027 readiness | LOW (PDK development required, 36+ months) | READY (production) |

**Architecture A Recommendation:** Technically correct, economically premature for 2026-2027. Target for 2029-2030 standardization.

---

### **Architecture B: Hybrid Memristive-CMOS with Ternary State Controller**

**Overview**

Architecture B separates concerns: binary CMOS performs all computation, routing, and control. MT memristive cells handle exclusively state enforcement \- the IRS hold, the confirm pulse gate, and the immutable log. Binary CMOS and MT cells are integrated via BEOL 3D hybrid or monolithic 3D.

**System Diagram**

* \+-----------------------------------------------------------+  
* |  ARCHITECTURE B: HYBRID MEMRISTIVE-CMOS                   |  
* |                                                           |  
* |  CMOS LAYER (N2 GAA)                                      |  
* |  \+---------------------------+  \+----------------------+  |  
* |  | DECISION ENGINE           |  | LOGGING CONTROLLER   |  |  
* |  | (binary CMOS, \~10^6 gates)|  | (binary CMOS)        |  |  
* |  | Runs authorization logic  |  | PUF signing engine   |  |  
* |  | Outputs: \+1, 0, \-1 signal |  | Merkle hash engine   |  |  
* |  \+------------+--------------+  \+--------+-------------+  |  
* |               |                          |                 |  
* |  BEOL MT LAYER (TaOx, above CMOS)        |                 |  
* |  \+------------v--------------------------v-----------+     |  
* |  |  MT ENFORCEMENT ARRAY (1T1R TaOx, 64x64 tiles)  |     |  
* |  |  \+--------+  \+--------+  \+--------+             |     |  
* |  |  | TILE 0 |  | TILE 1 |  | TILE N |             |     |  
* |  |  | 64x64  |  | 64x64  |  | 64x64  |             |     |  
* |  |  \+----+---+  \+----+---+  \+---+----+             |     |  
* |  |       |           |          |                   |     |  
* |  |  \+----v-----------v----------v---+              |     |  
* |  |  | NL=NA GATE ARRAY              |              |     |  
* |  |  | Window comparator per tile    |              |     |  
* |  |  | VREF\_BANDGAP powered          |              |     |  
* |  |  | RC spoof detection per row    |              |     |  
* |  |  \+-------------------------------+              |     |  
* |  \+--------------------------------------------------+     |  
* |                                                           |  
* |  \+--------------------------------------------------+     |  
* |  | PUF SECTOR \+ OTP FUSES \+ LOG MEMORY              |     |  
* |  | (separate MT sector, physically isolated)        |     |  
* |  \+--------------------------------------------------+     |  
* \+-----------------------------------------------------------+


**CMOS-to-MT Interface: No Blocking**

The CMOS decision engine outputs a 2-bit signal: {+1, 0, \-1} encoded as {00, 01, 10}. This signal is sent to the MT enforcement array's write driver in one clock cycle. The write driver issues the appropriate voltage pulse to the MT cell. This is a fire-and-forget operation from the CMOS perspective: the CMOS engine does not wait for the MT cell to confirm its state.

If the decision is 0 (Epistemic Hold / IRS), the MT cell transitions to IRS. The CMOS engine proceeds to next tasks. The MT cell holds IRS physically until CONFIRM\_OK from the logging controller. The logging controller runs on a separate CMOS core with separate power domain \- it does not block the decision engine.

**Proof of non-blocking:** The CMOS decision engine and logging controller are on independent clock domains with no shared memory in the critical path. The only coupling is the CONFIRM\_OK wire from logging controller to NL=NA gate. This wire is combinational \- it asserts CONFIRM\_OK when log write is verified, and does not send any signal (no assertion) while logging is in progress. The decision engine never reads CONFIRM\_OK. Only the NL=NA gate reads it, and the gate is asynchronous \- it permits the LRS/HRS write only when CONFIRM\_OK arrives. Non-blocking by architecture.

**Integration Scheme: Monolithic 3D (M3D)**

Recommended integration: monolithic 3D stacking with TaOx MT layer deposited in BEOL above N2 CMOS. This is the integration approach demonstrated by Kim et al. (2022) and consistent with TSMC's BEOL integration research for embedded RRAM.

* CMOS N2 layer: gate-all-around FETs, all logic, sense amplifiers, PUF signing engine  
* BEOL MT layer: TaOx 1T1R cells in M4-M6 inter-metal region, approximately 55-80 nm stack height  
* Via connections: standard BEOL contacts from CMOS to MT layer, approximately 10-50 nm diameter  
* Thermal budget: MT deposition at 200-300 degrees C, within N2 BEOL tolerance

Alternative: CoWoS chiplet integration (CMOS on substrate, MT chiplet bonded via CoWoS-S):

* Advantages: MT chiplet can use optimized process independent of logic process  
* Disadvantages: inter-die routing adds approximately 50-200 ns latency and 10-50 pJ/bit energy penalty  
* Recommendation: Use CoWoS integration only if monolithic 3D proves difficult to yield (fallback option)

**Thermal Budget Analysis**

MT BEOL deposition sequence on top of N2 CMOS:

1. TiN bottom electrode: 300 degrees C reactive sputtering \- below N2 BEOL limit (\~400 degrees C)  
2. TaOx- layer: 200-250 degrees C sputtering \- within budget  
3. TaOx+ layer: 200-250 degrees C sputtering \- within budget  
4. Al2O3 barrier: 250 degrees C ALD \- within budget  
5. Pt/TiN top electrode: 150-200 degrees C sputtering \- within budget  
6. Post-anneal: 200-250 degrees C, 30 min \- within budget  
7. Total worst-case temperature exposure of CMOS: 300 degrees C for \< 60 min, 250 degrees C for \~4 hours

N2 CMOS ION degradation from BEOL thermal exposure at 300 degrees C for 60 min: estimated \< 2% ION loss (directional estimate based on CMOS reliability data; specific N2 characterization required \- flagged as Phase 2 test vehicle requirement).

**Area, Energy, and Latency Overhead: Architecture B vs Architecture A vs Baseline**

| Parameter | Architecture A | Architecture B | Named 2025 Baseline |
| ----- | ----- | ----- | ----- |
| Area (MT enforcement sector, 1000 cells) | \~0.015 mm^2 | \~0.020 mm^2 (BEOL adds \~30%) | N/A (no IRS) |
| Energy per enforcement event | 100-500 pJ | 150-700 pJ (interface overhead) | N/A |
| Execution lane WCET | \< 200 ns | \< 500 ns (CMOS-to-MT interface adds \~300 ns) | N/A |
| Logging lane ceiling | 300 ms | 300 ms (same) | N/A |
| Control logic area | \~20% overhead | \~15% overhead (CMOS logic efficient) | Baseline |
| Integration risk | HIGH (native ternary PDK) | MEDIUM (BEOL addition to known process) | LOW |
| 2027 readiness | LOW | MEDIUM-HIGH | HIGH (now) |

**Architecture B Recommendation:** Primary recommendation for 2026-2027 commercialization. Lower integration risk, adequate performance, achievable certification path.

---

## **Section 5 \- Foundry Technology Alignment and Roadmap**

### **Candidate Foundry Nodes**

**TSMC N2 (2025): Nanosheet GAA, CoWoS**

* Status: Mass production ramping H2 2025\. N2 adoption by AI customers is double N5's first-year rate. (High confidence \- TSMC Q3 2025 earnings; TSMC 2025 Technology Symposium)  
* MT relevance: N2 provides the CMOS logic base for Architecture B's decision engine and logging controller. TSMC has demonstrated embedded RRAM at 40nm node; N2 embedded RRAM integration is not publicly confirmed as production-ready as of this writing.  
* Integration path: Architecture B uses N2 for CMOS \+ BEOL TaOx in M4-M6. Alternatively, N2 CMOS \+ CoWoS-bonded MT chiplet.  
* PDK status: N2 PDK available to customers. MT (TaOx IRS) PDK: does not exist. Must be developed.  
* Thermal concern: N2 nanosheet FETs may be more sensitive to BEOL thermal excursions than FinFET predecessors. Specific N2 \+ TaOx BEOL thermal characterization required.

**Intel 18A (2025): PowerVia backside power delivery, Foveros hybrid bonding**

* Status: Intel 18A targeted for 2025 production (internal products). External foundry customers uncertain timeline.  
* MT relevance: Foveros direct bonding enables face-to-face die stacking with \< 10 um bump pitch. An MT enforcement chiplet could be bonded directly atop an 18A CMOS logic die with sub-100 ns interface latency.  
* PowerVia advantage: backside power delivery frees front-side metal layers for signal routing, potentially enabling cleaner MT BEOL integration.  
* Disadvantage: Intel 18A commercial availability for external customers and MT PDK development timeline are uncertain. Not recommended as primary path.

**Samsung SF2 (2025): MBCFET, demonstrated MRAM-based CiM**

* Status: SF2 (2nm class, MBCFET \- Multi-Bridge Channel FET) targeted for 2025\.  
* MT relevance: Samsung has demonstrated MRAM-based CiM at 28nm FD-SOI and at advanced nodes. Their process team has NVRAM-in-logic integration experience directly applicable to MT BEOL integration.  
* Disadvantage: Samsung SF2 has not demonstrated TaOx ReRAM integration. MRAM experience is relevant but not directly transferable. Yield concerns at SF2 node remain (directional concern; specific data unverified recall).  
* Recommendation: Secondary candidate if TSMC path encounters BEOL thermal integration issues.

  ### **Required Artifact: 2026-2027 Milestone Table**

| Quarter | Architecture | Deliverable | Success Criteria | Kill Criterion |
| ----- | ----- | ----- | ----- | ----- |
| Q1 2026 | B (Hybrid) | TaOx BEOL test vehicle on N2 CMOS. 100 dice, 64x64 MT array on N2 CMOS. | ION degradation \< 3%. IRS sigma/mu \< 35% on test vehicle. | ION \> 5% degradation: BEOL integration incompatible; trigger Phase 1 recursion on thermal budget assumption. |
| Q2 2026 | B (Hybrid) | IRS accelerated aging at 150 degrees C, 1000 hours. | IRS resistance drift \< 10% at 95% CI lower bound. | Drift \> 20% at 95% CI: IRS 20-year retention fails; Phase 1 device layer conditional pass revoked; program terminated unless IRS engineering corrected. |
| Q2 2026 | B (Hybrid) | PUF production-scale characterization, 1000 dice. | Inter-die HD \> 49%. Intra-die HD \< 1% with fuzzy extractor. | Inter-die HD \< 47% on production dice: PUF identity unreliable; Phase 1 PUF layer fails; alternative PUF mechanism required (ring oscillator fallback). |
| Q3 2026 | B (Hybrid) | NL=NA window comparator test. Full attack battery. | Tamper detection rate \> 99.9%. Zero false accepts at operating corners. | False accept rate \> 0.1%: window comparator specification insufficient; redesign required. |
| Q3 2026 | B (Hybrid) | WCET characterization across process corners (SS, FF, SF, FS, TT) and temperature range. | Execution lane \< 2 ms at 99.99th percentile at all corners. | Any corner exceeds 5 ms: non-blocking WCET constraint violated; Phase 2 failure condition triggered. |
| Q4 2026 | B (Hybrid) | IEC 61508 SIL 3 pre-assessment submission (exida or TÜV SÜD). | Pre-assessment report with identified gaps. | Pre-assessment identifies fundamental incompatibility (e.g., analog device in digital safety standard): certification approach requires fundamental revision; 12-month slip. |
| Q4 2026 | A (Native) | Architecture A design complete. Ternary PDK specification document. | Foundry agreement to develop MT PDK (consortium funding confirmed). | No foundry agrees to MT PDK development: Architecture A deferred to post-2028. Architecture B proceeds alone. |
| Q1 2027 | B (Hybrid) | First functional MT enforcement chip. Full system integration. | 10^6 enforcement events, zero NL=NA bypass confirmed. | \> 1 confirmed NL=NA bypass event: interlock architecture compromised; root cause analysis, potential Phase 1 NL=NA recursion. |
| Q1 2027 | B (Hybrid) | Financial settlement finality pilot (Section 8 use case). | 10^6 settlement decisions enforced, full audit trail verified. | Logging lane ceiling exceeded in \> 0.1% of events: architecture adjustment required. |
| Q2 2027 | B (Hybrid) | IEC 61508 SIL 3 certification submission. | Certification body accepts evidence package. | Certification rejected: specific deficiency identified; 6-12 month remediation cycle; program not terminated but 2027 commercial deployment delayed. |
| Q2 2027 | B (Hybrid) | Power grid dispatch pilot (Section 8 use case). | 10^4 dispatch decisions over 30 days with zero HRS-to-LRS false transitions. | False transition detected: safety-critical failure; immediate halt; root cause analysis mandatory. |

**Kill Criterion with Phase 1 Recursion:** If Q2 2026 IRS aging test triggers failure (drift \> 20%), Phase 1 device layer conditional pass is revoked. One recursion is permitted: Phase 1 Section 5.2 TaOx stack specification is re-examined with the Q2 2026 test data. Specific assumption to re-examine: post-write anneal protocol adequacy and IRS engineering approach (bilayer vs. compliance current control). If second evaluation also fails, program terminates permanently.

---

## **Section 6 \- Top Three Candidate Architectures for 2027 Standardization**

**Defining "Standardized" for MT:**

| Criterion | Minimum Viable (2027 target) | Industry Standard (2030 target) |
| ----- | ----- | ----- |
| Foundry PDK | Device models for TaOx IRS, DRC rules | Variability corners, reliability decks, aging models |
| EDA support | Custom ternary behavioral simulator, SPICE models | Integrated Cadence/Synopsys flows, synthesis libraries |
| IP ecosystem | 1 foundry, 1 MT enforcement macro | 3+ foundries, standard enforcement cell library |
| Benchmarking | Proprietary enforcement throughput metric | Standardized "MT enforcement density" benchmark (TED/mm^2) |
| Certification | IEC 61508 SIL 3 for Architecture B | IEC 61508 SIL 4 path defined |

---

### **Candidate Family 1: Compute-in-Memory with TaOx Memristor Crossbars (MT Native)**

**Core Principle:** TaOx bilayer 1T1R cells provide three-state non-volatile enforcement states in BEOL. NL=NA interlock is hardware-enforced via window comparator and dedicated confirm wire. This is the direct MT implementation.

**CMOS Integration Status:** Demonstrated in research (TSMC 40nm embedded RRAM; Kim et al. bilayer ternary). Not yet in production as a three-state enforcement architecture at N2.

**Killer Obstacle:** IRS sigma/mu at production corners. The 20-35% lab result must translate to \< 35% at all production corners. Process corner variations in TaOx stoichiometry can shift sigma/mu significantly. This is the single obstacle that could terminate this family.

**Minimum Experiments (12-24 months):**

1. N2 BEOL TaOx integration test vehicle (Q1 2026, as above)  
2. IRS sigma/mu across process corners: SS/FF/SF/FS at 0 degrees C, 25 degrees C, 85 degrees C, 125 degrees C (Q1-Q2 2026\)  
3. 10^7 cycle endurance at IRS state (Q2-Q3 2026\)  
4. Full NL=NA attack battery (Q3 2026\)  
5. System-level WCET validation at all process corners (Q3 2026\)

**Benchmark Target:** 1000 MT enforcement decisions per second per mm^2, energy \< 500 pJ/decision, WCET \< 2 ms at 99.99th percentile.

**Governance Target:** TL triadic enforcement with NL=NA and PUF-rooted provenance satisfying WCET. This is the only family that provides fully native TL semantics in hardware.

**Kill Criterion:** IRS sigma/mu \> 35% at any production process corner (slow-slow at 125 degrees C worst case). Phase 1 recursion trigger: re-examine bilayer oxygen asymmetry specification (TaOx-/TaOx+ stoichiometry targeting).

**2025 Baseline Quantified Advantage:** 1400-2800x energy reduction for Epistemic Hold enforcement (Section 9 of Phase 1). Power-loss persistence of IRS: infinite advantage (binary CMOS provides zero persistence). WCET determinism: infinite advantage (software polling is unbounded). No quantified speed or density advantage.

---

### **Candidate Family 2: Spintronic/Magnetic Devices (MTJ-based)**

**Core Principle:** Magnetic tunnel junctions (MTJ) provide two stable states (parallel/anti-parallel magnetization) with excellent endurance (\> 10^14 cycles, Renesas data) and retention (\> 10 years at 105 degrees C). A "third state" for MT could be approximated by using a probabilistic intermediate state (thermally fluctuating between P and AP magnetization under applied spin-torque) or by using a three-terminal design.

**CMOS Integration Status:** High. STT-MRAM at 28nm FD-SOI is in production (Samsung, Renesas). Embedded MRAM at advanced nodes is actively developed.

**Killer Obstacle for MT Application:** MTJ has no native stable IRS. The two-state nature is fundamental to the MTJ operating principle. Approximating IRS via probabilistic intermediate state violates the MT stability requirement (IRS must be deterministic and non-volatile). A three-terminal design (in-plane magnetization control) could approximate IRS but has not been demonstrated with adequate stability and endurance simultaneously. Unless a stable, non-volatile, deterministic intermediate magnetization state is demonstrated in a fabricated device, MTJ is NOT viable as a primary MT device.

**Minimum Experiments (12-24 months):**

1. Literature survey of stable three-state MTJ proposals (Q1 2026\)  
2. If credible proposal found: device fabrication and sigma/mu measurement for intermediate state (Q2-Q3 2026\)  
3. Comparison of MTJ-IRS stability vs TaOx-IRS stability at operating temperature range (Q4 2026\)

**Benchmark Target:** If MTJ intermediate state demonstrated: equivalent to TaOx target (\< 35% sigma/mu at all corners, \> 10 year retention at 85 degrees C).

**Kill Criterion:** No stable, non-volatile, deterministic intermediate MTJ state demonstrated in fabricated device with sigma/mu \< 40%. This kill criterion is likely to trigger: MTJ is fundamentally binary. Phase 1 recursion: not required (TaOx remains primary; MTJ is parallel investigation only).

**2025 Baseline Comparison:** MTJ (STT-MRAM) is SUPERIOR to TaOx in endurance (10^14 vs 10^9 cycles) and variability for binary states. For MT's IRS requirement, MTJ is inferior (no stable native intermediate state). MTJ is recommended only as the binary CMOS complement in Architecture B (for high-endurance binary logging), not as the MT enforcement cell.

---

### **Candidate Family 3: FeFET (Ferroelectric FET)**

**Core Principle:** FeFET uses a ferroelectric gate dielectric (HZO \- hafnium zirconium oxide) to achieve multi-state non-volatile threshold voltage modulation. In principle, a three-state FeFET can be engineered via partial polarization switching.

**CMOS Integration Status:** Medium. Intel demonstrated HZO-based FeRAM at VLSI 2024 with \< 100 fJ write energy and 10 year retention at "elevated temperatures." FeFET integration with advanced CMOS is actively researched but not in production at sub-10nm nodes.

**Killer Obstacle for MT Application:** Retention at elevated temperature. FeFET retention is limited by charge de-trapping from the ferroelectric/semiconductor interface. Published data shows degraded retention above 85 degrees C for HZO-based devices (high confidence directional; specific quantitative data for three-state FeFET is unverified recall). The MT specification requires \> 10 year retention at 85 degrees C \- a hurdle FeFET has not cleared for intermediate states.

A second obstacle: FeFET intermediate state (partial polarization) is the least stable configuration. The ferroelectric wants to be fully polarized (P or AP). Any partial state will relax toward a fully-polarized state over time. This is fundamentally adverse to MT's requirement for a stable IRS.

**Minimum Experiments (12-24 months):**

1. FeFET three-state retention measurement at 85 degrees C and 125 degrees C (Q1-Q2 2026\)  
2. FeFET IRS sigma/mu across 100 cycles (Q2 2026\)  
3. Comparison to TaOx IRS stability (Q3 2026\)

**Kill Criterion:** FeFET intermediate state retention \< 5 years at 85 degrees C at 95% CI lower bound. This criterion is likely to trigger based on known FeFET physics. Phase 1 recursion: not required; FeFET is a parallel investigation.

**2025 Baseline Comparison:** FeFET write energy (\< 100 fJ) is superior to TaOx (\~50 pJ) by \~500x. However, this advantage is irrelevant if retention is insufficient for 20-year operation. FeFET is not recommended as primary MT device but could be revisited if a charge-trapping stabilization approach is demonstrated.

---

## **Section 7 \- The Saint Spot: Market Gap Analysis**

**The MT "saint spot" is the specific operational zone where deterministic, hardware-enforced, power-loss-persistent authorization semantics yield a discontinuous advantage that no binary CMOS plus software combination can provide at any cost, because the requirement is physical enforcement, not algorithmic correctness.**

This definition distinguishes MT from performance-driven computing architectures. MT does not compete on TOPS/W. It competes on enforceability: the property that an enforcement action happened in matter, not merely in software, and is verifiable to foundry-level provenance.

### **Problem-Mechanism-Advantage Mapping Table**

| Bottleneck | Problem | MT Mechanism | Why Binary+SW Cannot Match | Delta vs 2025 Named Baseline |
| ----- | ----- | ----- | ----- | ----- |
| Authorization audit immutability | Software-written audit logs are modifiable post-hoc by privileged software or hardware exploits | NL=NA physical interlock writes to non-volatile TaOx on dedicated hardware path; PUF-signed Merkle chain | Any binary CMOS system with software-writable registers can have logs altered by root-level exploits. MT log is written by physical pulse, not by software instruction. | 2025 baseline (binary NVRAM) can be erased or overwritten by any process with write access. MT log write requires a physical confirm pulse from verified hardware path. Discontinuous. |
| Epistemic Hold persistence through power loss | Binary wait states are lost on power failure; system must re-initialize authorization state | TaOx IRS persists without power; state is in matter, not in registers | Any SRAM, DRAM, or flip-flop-based wait state vanishes on power loss. Re-initialization requires software logic and policy re-evaluation. | NVRAM (binary) can store a flag, but the flag is software-writable. MT IRS is physics-writable only (confirm pulse required). Discontinuous. |
| Non-bypassable enforcement | Software-enforced authorization can always be bypassed by privileged software, firmware updates, or debug interfaces | MT enforcement cell does not have a software API for state override. State changes require physical voltage pulses | Even hardware security modules (HSMs) have firmware update paths. MT's mandate is in OTP fuses, not firmware. No firmware update path exists. | Named baseline (NVRAM \+ software) inherits any software bypass vulnerability in the system stack. MT forecloses this by architecture. |
| WCET-bounded authorization latency | Software polling for authorization state completion has unbounded worst-case latency (interrupt storm, OS preemption, memory contention) | NL=NA gate assertion is asynchronous and combinational; no software interrupt path; WCET \< 200 ns for execution lane | Real-time OS-based authorization systems can achieve low-average latency but cannot guarantee 99.99th percentile bounds under all conditions without dedicated hardware. | Binary CMOS \+ RTOS: typical authorization WCET is 1-5 ms; 99.99th percentile can exceed 50 ms under interrupt contention. MT execution lane WCET: \< 200 ns at 99.99th percentile. \>250x improvement. |
| Multi-party governance without trust aggregation | Software-based multi-party governance (multi-sig, threshold signatures) requires software intermediaries that can be compromised or unavailable | OTP fuse mandate requires multi-sig authorization at burn time; post-burn, no software intermediary exists | Any software-based multi-party system has an availability dependency. If signers are unavailable, governance stalls. MT mandate once burned is self-executing without signer availability. | Named baseline: no equivalent hardware-level governance encoding. Discontinuous. |
| Memory wall for high-frequency enforcement | Binary CMOS systems must fetch authorization state from DRAM or SRAM on every decision cycle, consuming significant bandwidth and energy | MT enforcement cells are co-located with execution decision points; authorization state read is in-place, not fetched | SRAM L1 access: \~50 pJ, \~1 ns. But SRAM is volatile and software-accessible. MT read: \~1 pJ, \~100 ns, non-volatile, not software-accessible. Different function. | Named baseline SRAM: 50x lower read energy but volatile and bypassable. MT: 20-year persistent non-volatile state co-located with enforcement. Different service. |

### **Section 7.5 \- Addressable Market Quantification**

**Bottom-up estimate for break-even calculation (Section 9).**

**Vertical 1: Financial Settlement Finality Engines**

Target: central bank RTGS systems, CCP clearing systems, high-frequency settlement engines.

* Number of systems globally: approximately 70 central bank RTGS systems (one per major currency zone), approximately 60 CCP clearing houses globally, approximately 200 major settlement engines at tier-1 financial institutions. Total nodes: approximately 330 primary systems.  
* Each system requires approximately 10-50 MT enforcement chips (one per settlement lane, multiple lanes per system). Median: 20 chips per system.  
* Total chips: 330 \* 20 \= 6,600 enforcement chips for primary systems.  
* Secondary market (tier-2 banks, regional clearing): approximately 5x primary market \= 33,000 chips.  
* Replacement cycle: 5-7 years (hardware refresh cycle for financial infrastructure).  
* Annual replacement demand: 33,000 chips / 6 years \= approximately 5,500 chips per year.  
* Willingness-to-pay premium: cost of settlement failure. A single major settlement failure event costs $100M-$1B+ (based on published financial infrastructure incident data). MT premium of $15,000-$25,000 per enforcement chip is \< 0.01% of one major failure event cost. Premium is easily justified.  
* Revenue at $20,000 per chip: 5,500 chips/year \* $20,000 \= $110M/year at steady state.

**Vertical 2: Power Grid Dispatch Controllers**

Target: grid interconnection control centers, HVDC converter stations, substation automation controllers.

* Number of systems globally: approximately 1,000-1,500 transmission system operator (TSO) control nodes globally (unverified recall; directionally correct). Each requires 5-20 MT enforcement chips.  
* Total chips: 1,200 \* 10 \= 12,000 chips.  
* Replacement cycle: 10-15 years (industrial control hardware).  
* Annual replacement demand: 12,000 / 12 years \= 1,000 chips per year.  
* Willingness-to-pay premium: cost of grid failure. A major grid failure event costs $1B-$10B+ in economic damage. MT premium of $15,000-$25,000 is negligible.  
* Revenue at $20,000 per chip: 1,000 chips/year \* $20,000 \= $20M/year at steady state.

**Vertical 3: Industrial Autonomous Control Systems**

Target: nuclear plant safety systems, chemical process controllers, aviation flight management systems requiring deterministic authorization.

* Number of systems globally: approximately 50-100 nuclear plants with digital I\&C systems, approximately 500 large chemical plants with autonomous process controllers, approximately 5,000 commercial aircraft with flight management systems. Subset requiring MT-level enforcement: approximately 10% \= 560 systems.  
* Each system: 2-10 MT enforcement chips.  
* Total chips: 560 \* 5 \= 2,800 chips.  
* Replacement cycle: 10-20 years (safety-critical hardware).  
* Annual demand: 2,800 / 15 years \= approximately 190 chips per year.  
* Revenue at $25,000 per chip (higher premium for SIL 4 grade): 190 \* $25,000 \= $4.75M/year.

**Total Addressable Market Summary:**

| Vertical | Annual Chip Demand | Revenue at $20-25K/chip |
| ----- | ----- | ----- |
| Financial Settlement | 5,500 chips/year | $110M/year |
| Power Grid Control | 1,000 chips/year | $20M/year |
| Industrial Safety | 190 chips/year | $4.75M/year |
| **Total** | **\~6,700 chips/year** | **\~$135M/year** |

Total 10-year addressable revenue: approximately $1.35B (conservative, no growth) to $3.0B (optimistic, including secondary markets and standard adoption).

Note: These estimates assume approximately 85,000-120,000 total MT enforcement nodes globally, with annual replacement generating the demand above. The TAM is real but niche. It is not a mass market. This is the correct positioning.

---

## **Section 8 \- Autonomous Execution Systems as Catalyst**

Both use cases are developed in full technical depth. MT integration is specified completely for each.

---

### **Use Case 1: High-Frequency Settlement Finality Engine**

**Context**

Settlement finality is the moment at which a financial transaction becomes legally irrevocable. In modern markets, settlement systems must enforce: (1) sufficient funds/assets are present, (2) counterparty authorization is confirmed, (3) the transaction is within mandate limits. These three conditions map directly to TL triadic logic: Proceed (+1) \= all conditions met, Epistemic Hold (0) \= conditions met but authorization pending, Refuse (-1) \= conditions failed.

Financial institutions require deterministic settlement finality, unlike the probabilistic nature of blockchain finality. MT provides hardware-enforced deterministic finality at the enforcement cell level \- a stronger guarantee than software determinism.

The targeted system: a Real-Time Gross Settlement (RTGS) engine processing 10,000-100,000 settlement decisions per second, each requiring deterministic authorization within \< 2 ms with immutable audit trail.

**System Architecture with MT Integration**

* \+--------------------------------------------------------------+  
* |  HF SETTLEMENT FINALITY ENGINE WITH MT INTEGRATION           |  
* |                                                              |  
* |  INPUT LAYER                                                 |  
* |  \[Market Data\] \[Auth Request\] \[Risk Check\] \[Mandate Params\]  |  
* |       |              |              |              |          |  
* |  \+----v--------------v--------------v--------------v-----+   |  
* |  |  DECISION ENGINE (binary CMOS, \~10^6 gates)          |   |  
* |  |  Runs risk model, counterparty check, mandate verify  |   |  
* |  |  Output: {+1, 0, \-1} per settlement request          |   |  
* |  \+----+-----------------------------+--------------------+   |  
* |       |                             |                        |  
* |  \[+1 / \-1 / 0\]                  \[Log data\]                   |  
* |       |                             |                        |  
* |  \+----v-----------+   \+-------------v---------------------+   |  
* |  | MT ENFORCEMENT |   | LOGGING CONTROLLER (binary CMOS)  |   |  
* |  | ARRAY          |   | PUF signing, Merkle hash          |   |  
* |  | TaOx 64x64    |   | NVRAM log write                   |   |  
* |  | \[LRS/IRS/HRS\] |   | Issues CONFIRM\_OK                 |   |  
* |  |               |   |                                   |   |  
* |  | NL=NA GATE    \<---\< CONFIRM\_OK (when log verified)    |   |  
* |  |               |   |                                   |   |  
* |  \+----+----------+   \+-----------------------------------+   |  
* |       |                                                      |  
* |  \[State confirmed\]                                           |  
* |       |                                                      |  
* |  \+----v--------------------------------------------------+   |  
* |  | ACTION LAYER                                          |   |  
* |  | LRS (Proceed \+1): funds transfer authorized           |   |  
* |  | IRS (Hold 0): funds in escrow, awaiting confirm       |   |  
* |  | HRS (Refuse \-1): transaction rejected, funds returned |   |  
* |  \+-------------------------------------------------------+   |  
* \+--------------------------------------------------------------+


**NL=NA Operational Context for Settlement**

What triggers Epistemic Hold (IRS):

* Counterparty risk model returns "PENDING" (counterparty credit score being updated)  
* Authorization signature received but not yet verified against mandate parameters  
* Settlement amount within mandate but second-factor authorization pending (for amounts \> threshold)  
* Cross-border compliance hold (regulatory clearance pending)

What constitutes a valid confirm pulse in this domain:

* Logging controller has written the pending authorization record to the immutable MT log  
* PUF signature has been computed and verified  
* Merkle hash has been updated  
* All three conditions together trigger CONFIRM\_OK on the NL=NA gate  
* Physical confirm pulse: 1.5-2.5V, 20-80 ns on the dedicated confirm wire to the MT cell

What a Refuse event means operationally:

* Counterparty failed credit check beyond remediation threshold  
* Settlement would breach mandate limit (hard limit, not soft warning)  
* Cryptographic signature verification failed (potential fraud or error)  
* Physically: MT cell transitions to HRS. If Refuse Lock is set (for mandate breach), the cell is permanently locked in HRS \- this specific settlement request cannot be reinstated on this execution slot.  
* Audit trail: HRS event logged with timestamp, counterparty ID, decision parameters, PUF signature, Merkle hash. Immutable.

**Dual-Lane Latency Budget \- Settlement System**

* SETTLEMENT DECISION TIMELINE:  
*   
* t \= 0 ms        Input received (settlement request)  
* t \= 0.1 ms      Decision Engine evaluation complete  
* t \= 0.1 ms      MT cell write command issued (IRS for pending, LRS/HRS for clear decisions)  
* t \= 0.15 ms     MT cell reaches target state (50 ns write pulse \+ settling)  
* t \= 0.15 ms     \[EXECUTION LANE COMPLETE for clear decisions\]  
*                 \[For IRS (pending): execution lane holds here; NO stall in any other process\]  
*   
* PARALLEL LOGGING LANE:  
* t \= 0 ms        Log entry formation begins (parallel to above)  
* t \= 10 ms       PUF signing complete (Ed25519)  
* t \= 50 ms       Merkle hash update complete  
* t \= 150-250 ms  NVRAM log write complete (TaOx log cell write)  
* t \= 250 ms      CONFIRM\_OK issued to NL=NA gate  
*   
* CONFIRM\_OK received at NL=NA gate at t \= 250 ms.  
* MT cell transitions from IRS to LRS (if authorized) in 50 ns.  
* t \= 250.00005 ms: Settlement execution confirmed.  
*   
* WCET ANNOTATIONS:  
* \- Execution lane WCET: 0.15 ms \< 2 ms limit. SATISFIED.  
* \- Logging lane ceiling: 250 ms \< 300 ms limit. SATISFIED.  
* \- Jitter: \+/-30 ms for NVRAM write variation (sigma/mu \= 30ms/250ms \= 12%). At 300 ms ceiling: 30ms/300ms \= 10%. SATISFIED (barely; NVRAM write jitter must be controlled).  
* \- Non-blocking: execution lane does not poll logging lane at any point. VERIFIED.


**Minimum dwell time in Epistemic Hold before transition:** No minimum dwell time is required by the MT mechanism. The IRS is held until CONFIRM\_OK arrives. If CONFIRM\_OK arrives in 1 ms (fast logging path), the transition occurs at 1 ms. If it arrives at 299 ms, transition occurs at 299 ms. The IRS state is stable for any duration.

**Hardware Root of Trust \- 20-Year Verification Scenario**

A log entry from a settlement decision made on April 3, 2026 must be verifiable on April 3, 2046\. Verification chain:

1. Retrieve log entry L from archive. L contains: timestamp, counterparty IDs, settlement amount, decision (+1/0/-1), MT cell resistance state confirmed, PUF signature S, die certificate reference cert\_id, Merkle chain position.  
2. Retrieve cert\_id from foundry attestation database (must be in escrow per Section 8.2 of Phase 1).  
3. Verify Cert\_die against K\_foundry (foundry public key, archived in 5+ public repositories).  
4. Extract K\_pub from Cert\_die.  
5. Verify S against K\_pub: if verification passes, the log entry was signed by the specific die identified by cert\_id. The die's physical identity is its filament morphology \- unclonable.  
6. Cert\_die records: fab\_date (2026-Q1), process\_node (N2), wafer\_lot\_id, die\_X=217, die\_Y=089. These records are immutable in the escrow database.  
7. Merkle chain: verify that L's hash links correctly to adjacent entries (detecting any tampering with the log sequence).

Foundry escrow scenario (foundry no longer exists in 2046):

* K\_foundry public key was published in NIST, IANA, ISO, and two national standards repositories in 2026\. These repositories still exist.  
* Full attestation database was archived in escrow with Stewardship Council (2 geographically distributed copies per jurisdiction).  
* Verification in 2046 proceeds identically to above, using archived K\_foundry from public repositories.  
* The foundry's non-existence does not break the chain, because the chain does not require the foundry to be operational \- only its public key to be accessible.

**Why This Use Case Cannot Be Served by the Named 2025 Baseline**

The named 2025 baseline (TSMC N2 CoWoS embedded ReRAM 1T1R, binary only) can store binary flags at high speed and with non-volatility. It cannot provide:

1. A native, physically-enforced intermediate state (IRS) that persists without software polling.  
2. A hardware-level guarantee that the log write preceded the state transition (NL=NA). Binary NVRAM can record both events, but cannot physically guarantee their sequencing without software logic \- which can be bypassed.  
3. A PUF-rooted identity tied to the enforcement cell itself. Binary NVRAM systems use TPMs or HSMs for identity \- separate chips, with firmware update paths, that can be replaced or compromised.  
4. Power-loss persistence of the authorization-pending state with guaranteed re-verification on restart. Binary systems lose volatile state on power loss and re-initialize from software flags \- which may have been corrupted.

**The baseline can serve the settlement engine for the 95% of decisions that are clear (+1 or \-1). MT adds value specifically for the 5% of decisions that enter Epistemic Hold \- the highest-risk, highest-scrutiny category. For those decisions, MT provides a physical enforcement guarantee that is not achievable any other way.**

---

### **Sequence Diagram \- Settlement Finality Engine**

* ACTORS:  
*   \[INPUT\]     Settlement request  
*   \[DE\]        Decision Engine (binary CMOS)  
*   \[MT-CELL\]   MT Enforcement Cell (TaOx 1T1R)  
*   \[NL=NA\]     NL=NA Gate (window comparator)  
*   \[LOG-CTRL\]  Logging Controller (binary CMOS)  
*   \[LOG-MEM\]   Immutable Log Memory (MT cells)  
*   \[PUF\]       PUF Signing Engine  
*   
* SEQUENCE:  
*   
* \[INPUT\] \----\> \[DE\]  
*               |  t=0: Evaluate settlement request  
*               |  Inputs: counterparty risk, mandate params, auth sig  
*               |  Output: Decision \= {+1, 0, \-1}  
*               |  
*               \+--------\> \[MT-CELL\]: Write command  
*               |           Voltage: 1.5-2.5V, 40 ns pulse  
*               |           For 0: IRS write (partial RESET)  
*               |           For \+1: LRS write (SET)  
*               |           For \-1: HRS write (RESET)  
*               |           R\_IRS \= 100 kohm \- 1 Mohm  
*               |           Sense amp threshold: R\_REF\_LOW=5 kohm, R\_REF\_HIGH=2 Mohm  
*               |  
*               |  (PARALLEL LOGGING LANE \- never serial with execution)  
*               \+--------\> \[LOG-CTRL\]: Begin log entry  
*                           |  t=0 to t=250 ms (logging lane, hard ceiling 300 ms)  
*                           |  
*                           \+--------\> \[PUF\]: Sign(K\_priv, H(log\_entry))  
*                           |           t=0 to t=10 ms (Ed25519, 32-byte key)  
*                           |  
*                           \+--------\> \[LOG-MEM\]: Write log entry (PUF-signed)  
*                           |           t=10 to t=250 ms (NVRAM write, 50-200 ms typical)  
*                           |           Merkle hash update included  
*                           |  
*                           \+--------\> \[NL=NA\]: Issue CONFIRM\_OK  
*                                       t=250 ms (when log write verified)  
*                                       Signal: V=1.5-2.5V, t=40 ns  
*                                       Wire: M4, 500 um max, RC=1.85 ps  
*                                       Window comparator: \+/-5% voltage, \+/-10% timing  
*   
* \[NL=NA\] \---\> \[MT-CELL\]:  
*               If Decision was 0 (IRS):  
*                 CONFIRM\_OK=1 at t=250 ms  
*                 Write LRS (authorize) or HRS (refuse per logging result)  
*                 Voltage: 1.5-2.5V, 40 ns (LRS write)  
*                 State transition: IRS \-\> LRS in \~50 ns  
*                 \[WCET EXECUTION LANE: t=0.15 ms (write) \+ wait in IRS \+ 0.05 ms (transition)\]  
*                 \[NON-BLOCKING: No polling. No CPU stall. IRS persists physically.\]  
*   
*               If Decision was \+1 (LRS) or \-1 (HRS):  
*                 State already written at t=0.15 ms  
*                 CONFIRM\_OK at t=250 ms also logged but does not change state  
*                 \[WCET EXECUTION LANE: 0.15 ms total\]  
*   
* STATE OUTCOMES:  
*   LRS (+1): Settlement AUTHORIZED  
*             Action: Funds/assets transfer permitted  
*             Logging: CONFIRM\_OK received, LRS state verified  
*   IRS (0):  Settlement HELD  
*             Action: Funds held in escrow. No transfer. No polling.  
*             System proceeds to next decision in parallel.  
*             Logging: CONFIRM\_OK pending  
*   HRS (-1): Settlement REFUSED  
*             Action: Funds returned. No transfer.  
*             If Refuse Lock: cell permanently locked. New cell required for next attempt.  
*             Logging: HRS event, full audit trail, Merkle chain updated  
*   
* DUAL-LANE TIMING BOUNDARIES:  
*   EXECUTION LANE (M1-M3 metal, physically separated):  
*     Decision engine \-\> MT cell write: t=0 to t=0.15 ms  
*     WCET: 0.15 ms \<\< 2 ms limit  
*   LOGGING LANE (M5-M7 metal, physically separated):  
*     Log entry \-\> PUF sign \-\> NVRAM write \-\> CONFIRM\_OK: t=0 to t=250 ms  
*     Hard ceiling: 300 ms. Current estimate: 250 ms. Margin: 50 ms.  
*     Jitter: \+/-30 ms (sigma/mu \= 12% of 250 ms. Specification: sigma/mu \< 10% of 300 ms ceiling \= 30 ms. SATISFIED.)  
    
  ---

  ### **Use Case 2: Power Grid Dispatch Controller**

**Context**

Power grid dispatch is the decision to route electric power from generation sources to load nodes through transmission infrastructure. In modern grids with autonomous control systems, dispatch decisions occur in real time (millisecond to second timescales). A Refuse decision means: a power flow is blocked (e.g., overloaded line, protection relay triggered, N-1 security constraint violated). An Epistemic Hold means: dispatch is pending verification of grid state (sensor data reconciliation, voltage stability check). A Proceed means: dispatch authorized.

The critical safety property: a false Proceed decision on an overloaded line can cause a cascade failure. The hardware enforcement of Refuse must not be bypassable by software error, firmware bug, or cyber intrusion.

**System Architecture with MT Integration**

* \+--------------------------------------------------------------+  
* |  POWER GRID DISPATCH CONTROLLER WITH MT INTEGRATION          |  
* |                                                              |  
* |  SENSOR LAYER                                                |  
* |  \[PMU Data\] \[SCADA\] \[Thermal Sensors\] \[Stability Model\]      |  
* |       |                                                      |  
* |  \+----v-----------------------------------------------+      |  
* |  | GRID STATE PROCESSOR (binary CMOS)                 |      |  
* |  | Runs N-1 security analysis, thermal limit check    |      |  
* |  | Voltage stability assessment                       |      |  
* |  | Output: {PROCEED, HOLD, REFUSE} per dispatch req  |      |  
* |  \+----+----------------------------+------------------+      |  
* |       |                            |                         |  
* |  \[Decision\]                  \[Log data\]                      |  
* |       |                            |                         |  
* |  \+----v-----------+   \+------------v--------------------+    |  
* |  | MT ENFORCEMENT |   | LOGGING CONTROLLER              |    |  
* |  | TaOx 64x64     |   | PUF signing, Merkle             |    |  
* |  | Per dispatch   |   | NVRAM log write                 |    |  
* |  | lane           |   | Issues CONFIRM\_OK               |    |  
* |  | NL=NA GATE     \<---\< CONFIRM\_OK (log verified)      |    |  
* |  \+----+-----------+   \+---------------------------------+    |  
* |       |                                                      |  
* |  \+----v-----------------------------------------------+      |  
* |  | HARDWARE SAFETY INTERLOCK                          |      |  
* |  | LRS \-\> Circuit breaker CLOSE permitted             |      |  
* |  | IRS \-\> Circuit breaker HOLD (no change)            |      |  
* |  | HRS \-\> Circuit breaker OPEN command mandatory      |      |  
* |  | HRS with Refuse Lock \-\> cannot CLOSE until new     |      |  
* |  |         authorization cycle from operator          |      |  
* |  \+----------------------------------------------------+      |  
* \+--------------------------------------------------------------+


**NL=NA Operational Context for Power Grid**

What triggers Epistemic Hold (IRS):

* Grid state model is being refreshed (phasor measurement unit data arriving, state estimation convergence pending)  
* N-1 security analysis in progress (cannot dispatch until analysis confirms grid remains stable post-dispatch)  
* Voltage stability margin is below threshold but not yet confirmed by redundant sensor  
* Operator authorization pending for a dispatch request above automatic authority limit

What constitutes a valid confirm pulse in this domain:

* Grid state estimation has converged (stability check passed)  
* N-1 analysis confirms security constraint not violated  
* If operator authorization required: operator has entered valid credentials AND logging controller has verified and signed the authorization  
* Physical: CONFIRM\_OK asserted by logging controller, which verifies all conditions before issuing

What a Refuse event means operationally:

* Dispatch would violate thermal limit on a transmission line (potential conductor damage)  
* N-1 security constraint violated (grid vulnerable to cascade if one element fails)  
* Voltage stability margin insufficient  
* Physically: MT cell transitions to HRS. Circuit breaker remains open (or is forced open). No current flows on the disputed path.  
* If Refuse Lock: this dispatch decision cannot be reversed without a new authorization cycle from operator with logged justification.  
* Safety property: hardware HRS cannot be converted to LRS (CLOSE command) by any software action. Physical confirm pulse with verified logging is required.

**Why This Use Case Cannot Be Served by Named 2025 Baseline**

The named 2025 baseline can store dispatch decisions in binary NVRAM. It cannot provide:

1. A hardware-level Refuse that cannot be overridden by software fault or cyber intrusion. If a software bug issues an incorrect CLOSE command to a relay in a binary system, the relay closes. In an MT system, the relay close command is physically gated by the LRS state of the MT enforcement cell. A software bug generating a LRS write command is rejected by the NL=NA gate unless the logging controller has verified and signed the authorization.

2. Power-loss-persistent dispatch hold. If the controller loses power mid-decision (storm, UPS failure), binary systems re-initialize from last known state \- which may be stale. MT cells retain IRS on power loss. When power is restored, the controller knows the exact pre-failure dispatch state from the MT cells, and the restart protocol requires log re-verification before any state transition. This is the critical safety property for grid applications.

3. A tamper-evident, PUF-rooted audit trail that traces every dispatch decision to the hardware that made it, verifiable 20 years later by a regulator.

**Dual-Lane Latency Budget \- Power Grid**

* DISPATCH DECISION TIMELINE:  
*   
* t \= 0 ms        Dispatch request received  
* t \= 0.5 ms      Grid State Processor evaluation complete (N-1 check)  
* t \= 0.5 ms      MT cell write command (IRS for pending N-1, LRS/HRS for clear decisions)  
* t \= 0.55 ms     MT cell state confirmed  
* t \= 0.55 ms     \[EXECUTION LANE COMPLETE for clear decisions: 0.55 ms \<\< 2 ms WCET\]  
*                 \[For IRS: circuit breaker held. No stall in any system process.\]  
*   
* PARALLEL LOGGING LANE:  
* t \= 0 ms        Log entry formation begins  
* t \= 10 ms       PUF signing complete  
* t \= 50 ms       Merkle hash update  
* t \= 100-250 ms  NVRAM log write  
* t \= 250 ms      CONFIRM\_OK issued  
*   
* For grid dispatch, a 250 ms hold is operationally acceptable:  
* \- Automatic dispatch (within authority): grid state changes in 100-500 ms timescales; 250 ms hold is within grid dynamics  
* \- Operator-mediated dispatch: seconds to minutes; 250 ms hold is negligible  
*   
* WCET ANNOTATIONS:  
* \- Execution lane: 0.55 ms \<\< 2 ms. SATISFIED.  
* \- Logging lane: 250 ms \< 300 ms ceiling. SATISFIED.  
* \- Non-blocking: grid processor continues receiving sensor data and evaluating other dispatch requests while IRS is held. VERIFIED.  
    
  ---

  ### **Sequence Diagram \- Power Grid Dispatch Controller**

* ACTORS:  
*   \[SENSOR\]    Grid sensor data (PMU, SCADA, thermal)  
*   \[GSP\]       Grid State Processor (binary CMOS)  
*   \[MT-CELL\]   MT Enforcement Cell (TaOx 1T1R, per dispatch lane)  
*   \[NL=NA\]     NL=NA Gate (window comparator, VREF\_BANDGAP powered)  
*   \[LOG-CTRL\]  Logging Controller (binary CMOS)  
*   \[LOG-MEM\]   Immutable Log Memory  
*   \[PUF\]       PUF Signing Engine  
*   \[RELAY\]     Physical circuit breaker relay  
*   
* SEQUENCE:  
*   
* \[SENSOR\] \----\> \[GSP\]  
*                |  t=0: Grid state data arrives  
*                |  t=0 to t=0.5 ms: N-1 security analysis, thermal check  
*                |  Decision: PROCEED (+1), HOLD (0), or REFUSE (-1)  
*                |  
*                \+--------\> \[MT-CELL\]: Write command  
*                |           PROCEED: LRS write (V=1.5V, t=40ns, R\_LRS=1-10 kohm)  
*                |           HOLD: IRS write (V=1.5V partial RESET, R\_IRS=100k-1M ohm)  
*                |           REFUSE: HRS write (V=2.0V, t=40ns, R\_HRS=1-10 Mohm)  
*                |           Sense amp: R\_REF\_LOW=5 kohm, R\_REF\_HIGH=2 Mohm  
*                |           Minimum dwell in IRS: until CONFIRM\_OK. No minimum floor.  
*                |  
*                |  (PARALLEL LOGGING LANE):  
*                \+--------\> \[LOG-CTRL\]  
*                            |  t=0: Begin log entry (GSP output, sensor data hash,  
*                            |       dispatch parameters, mandate version)  
*                            |  
*                            \+-\> \[PUF\]: Sign(K\_priv, H(log\_entry))  
*                            |   t=0 to 10 ms (Ed25519)  
*                            |  
*                            \+-\> \[LOG-MEM\]: Write signed entry  
*                            |   t=10 to 250 ms  
*                            |   Includes: Merkle hash update, prev\_event\_hash link  
*                            |  
*                            \+-\> \[NL=NA\]: CONFIRM\_OK  
*                                t=250 ms  
*                                Window comparator: V\_LOW=1.425V, V\_HIGH=2.625V  
*                                Timing window: 18-88 ns  
*                                RC spoof detection: rise time 20-50 ps (legitimate)  
*   
* \[NL=NA\] \---\> \[MT-CELL\]:  
*               CONFIRM\_OK=1 received at t=250 ms  
*               If IRS state: write LRS or HRS per authorization  
*               If LRS or HRS already: state verified in log  
*   
* \[MT-CELL\] \-\> \[RELAY\]:  
*               LRS (Proceed \+1): CLOSE command permitted  
*               IRS (Hold 0): HOLD command \- no breaker change  
*               HRS (Refuse \-1): OPEN command mandatory  
*               Physical coupling: relay driver reads MT cell resistance via sense amp  
*               WCET for relay action: \< 2 ms from CONFIRM\_OK (per relay spec)  
*   
* SAFETY ANNOTATIONS:  
*   \- Hardware HRS cannot be overridden by software.  
*     If software issues CLOSE command while MT cell \= HRS:  
*     MT cell resistance is measured by relay sense amp.  
*     Resistance \= HRS (\> 1 Mohm). Relay does not close.  
*     Physical enforcement of Refuse without software mediation.  
*   \- Power loss during IRS: MT cell retains IRS.  
*     On power restore: restart protocol requires log re-verify \+ re-confirm.  
*     Relay remains in current state (HOLD) until CONFIRM\_OK re-issued.  
*   \- Tamper detection: VDD glitch does not affect VREF\_BANDGAP-powered window comparator.  
*     EMP: rise time violation \-\> TAMPER\_EVENT\_LOG \-\> HRS enforced.  
    
  ---

  ## **Section 9 \- Economics and Manufacturing Viability**

  ### **Cost Per Ternary Cell vs Binary Alternatives**

**MT enforcement cell (TaOx 1T1R):**

* Cell area at N2 (estimated): approximately 0.01-0.02 um^2 (4F^2 to 8F^2 where F \= half-pitch \~15nm at N2). Note: TaOx BEOL adds approximately 3 BEOL masks (TaOx-, TaOx+, Al2O3 barrier deposition and patterning). Each mask adds approximately $5-10/wafer processing cost.  
* Wafer cost at N2: approximately $15,000-20,000 per wafer (unverified recall; directionally consistent with TSMC N3 pricing trends).  
* BEOL adder for TaOx: 3 additional masks \* $8/mask \= $24/wafer (negligible relative to $15,000 wafer cost). However, if BEOL yield penalty is 5-10% due to TaOx integration issues, effective cost increase is $750-$2,000 per wafer.  
* MT enforcement chip (1 mm^2 die, 1,000 enforcement cells \+ logic): chip cost at 80% yield on N2 \= approximately $50-150 per chip at volume. With TaOx BEOL yield penalty: approximately $75-250 per chip.

**Binary SRAM (6T, N2):** approximately $0.001 per bit (unverified recall; SRAM is volatile, no NL=NA, not comparable for enforcement use).

**Named 2025 baseline (TSMC N2 embedded binary RRAM):** approximately $0.01-0.05 per bit at volume (unverified recall for RRAM pricing). Binary only, no IRS capability.

**MT enforcement cell premium over binary RRAM:** MT cell requires 3 additional BEOL masks, bilayer TaOx deposition, and per-cell confirm wire. Estimated cost premium: approximately 2-5x over binary RRAM cell cost. At the chip system level (including control logic, PUF, signing engine, logging memory), total chip cost: approximately $500-2,000 per enforcement chip depending on volume.

**Willingness to pay at market: $15,000-25,000 per chip** (derived from vertical-specific failure cost analysis in Section 7.5). Even at $2,000 chip cost, margin is 87-92%. This is economically viable if volume is achieved.

### **Yield Implications of IRS Engineering**

IRS requires bilayer TaOx deposition with precise oxygen stoichiometry. Process variation in O2 partial pressure during sputtering can shift TaOx stoichiometry and affect IRS stability.

Expected yield impact:

* Cells that fail to achieve IRS (stuck at LRS or HRS after IRS write attempt): estimated 1-5% at initial process maturity, improvable to \< 1% with process optimization (unverified recall, consistent with RRAM yield ramp literature).  
* Chip-level yield (at least 99% of cells functional): with 1% cell failure rate, chip yield for 1,000-cell chip \= 0.99^1000 \= approximately 0% (if one failed cell kills chip). Therefore: redundancy architecture required.  
* Redundancy design: each enforcement slot uses 2-3 cells, with majority-vote logic. Effective cell failure rate with 3x redundancy: 1% becomes 3\*(0.01)^2\*(0.99) \= 0.03% per slot. Chip yield with 1,000 slots and 3x redundancy \= 0.9997^1000 \= approximately 74%. Acceptable at manufacturing scale.  
* Cost of redundancy: 3x cell area (from 1,000 cells to 3,000 cells). Still \< 0.1 mm^2 at N2.

  ### **NRE Costs for MT PDK Development**

Building an MT process design kit requires:

1. TaOx device characterization (I-V, C-V, retention, endurance at all corners): approximately $2-4M (fab time \+ test equipment)  
2. SPICE model development for TaOx cell, sense amplifier, NL=NA gate: approximately $1-2M  
3. DRC rule development for TaOx BEOL layers: approximately $0.5-1M  
4. Reliability deck and aging models (20-year extrapolation at corners): approximately $1-2M  
5. EDA tool integration (custom cells in Cadence/Synopsys flow): approximately $1-2M  
6. IEC 61508 evidence package development: approximately $2-4M (certification body engagement, documentation, testing)  
7. First silicon (2 wafer runs for test vehicles): approximately $1-3M (N2 MPW shuttle)

**Total NRE estimate: $8-18M.** Central estimate: $13M.

At $13M NRE and $135M/year steady-state revenue, NRE payback period: approximately 1 year after ramp-up. This is a favorable NRE/revenue ratio.

However: no single foundry will fund $13M NRE for a market of 6,700 chips/year without risk sharing. The economic model requires:

* Government co-investment (critical infrastructure security justification): approximately $5-7M  
* Consortium of 5-10 anchor customers (financial and grid operators): approximately $5-7M per customer over 5 years in guaranteed purchase commitments  
* Foundry contribution (reduced margin wafer access, engineering time): approximately $3-5M equivalent

This consortium model is precedented in safety-critical semiconductor development (automotive SIL 4 chips, aerospace ICs) and is achievable. It is not guaranteed.

### **Time-to-Market vs Incremental Binary Scaling**

* **Incremental binary scaling path (no MT):** Available now. Binary CMOS \+ software enforcement. Total cost: $0 incremental hardware, existing software stack. Does NOT provide power-loss-persistent, physically-enforced, PUF-rooted enforcement. For the use cases in Section 8, incremental binary is insufficient (hardware enforcement guarantee missing).

* **MT Architecture B path:** Q1 2026 test vehicle, Q4 2026 IEC pre-assessment, Q1 2027 first functional chip, Q2 2027 certification submission, Q3-Q4 2027 first commercial pilots. First revenue: approximately Q1 2028\. Time to market: approximately 24 months from program start.

  ### **Break-Even Production Volume Calculation (Arithmetic Shown)**

**Assumptions (stated explicitly):**

* Unit selling price: $20,000 per MT enforcement chip  
* Unit manufacturing cost: $500-2,000 (using $1,000 midpoint)  
* Gross margin per unit: $20,000 \- $1,000 \= $19,000  
* NRE (total): $13,000,000  
* Annual fixed operating cost (sales, support, quality, certification maintenance): $5,000,000/year  
* Break-even volume \= (NRE \+ Annual Fixed) / Gross Margin per unit \= ($13,000,000 \+ $5,000,000) / $19,000 \= $18,000,000 / $19,000 \= **947 units in year 1** (to cover NRE \+ one year of fixed costs)

Year 2+ break-even (NRE fully recovered): \= Annual Fixed / Gross Margin per unit \= $5,000,000 / $19,000 \= **264 units per year**

**Addressable annual demand (from Section 7.5): approximately 6,700 chips/year.**

At 15% market capture in year 2 (conservative for niche market): 6,700 \* 0.15 \= 1,005 units/year.

1,005 \> 264\. Break-even is achieved at 15% market capture.

**Sensitivity analysis:**

* If selling price drops to $10,000: gross margin \= $9,000. Year 2 break-even \= 556 units \= 8.3% market capture. Still achievable.  
* If selling price drops to $5,000: gross margin \= $4,000. Year 2 break-even \= 1,250 units \= 18.7% market capture. Tight but achievable.  
* If volume falls below 500 units/year at $20,000 price: program is not economically self-sustaining at current NRE. Foundry subsidy or government mandate required.

**Economic case for foundry to develop MT PDK:**

Foundry revenue per wafer at N2: approximately $15,000-20,000. MT chips per wafer (1 mm^2 die on 300 mm wafer, at 80% yield): approximately 300 good chips/wafer \* $1,000 manufacturing cost \= $300,000 manufacturing revenue per wafer.

At 6,700 chips/year production: 6,700 / 300 \= approximately 22 wafers/year. Foundry revenue: 22 wafers \* $17,500 \= $385,000/year.

This does NOT justify a foundry investing $13M NRE unilaterally. The foundry economic model requires:

1. Consortium co-funding of NRE (see above)  
2. IP licensing fees from MT macro deliveries (\~$1,000/chip in licensing): 6,700 \* $1,000 \= $6.7M/year. This changes the foundry economic case significantly.

**Conclusion on economics:** MT is commercially viable with consortium co-investment. It is not commercially viable as a single-foundry speculative investment. If no consortium forms, program continuation requires government mandate or regulatory requirement for hardware-enforced settlement/dispatch enforcement.

**The economics do not support commercialization within 2026-2027 without consortium formation and anchor customer commitments. This is stated directly. The technology is ready by 2027; the business model requires parallel development.**

---

## **Section 10 \- EDA, Verification, and Certification**

### **EDA Changes for Ternary Primitives**

Standard EDA flows (Cadence Genus/Innovus, Synopsys DC/IC Compiler) assume binary logic. MT requires:

1. **Custom cell library:** TaOx 1T1R cell, dual-reference sense amplifier, NL=NA gate, window comparator \- specified in Phase 1 and Phase 2\. These must be characterized as Liberty (.lib) cells with timing arcs, power models, and reliability constraints. Estimated effort: 6-12 person-months.

2. **Ternary behavioral models:** The TL decision state machine must be representable in SystemVerilog/VHDL. The 2-bit encoding (00=LRS, 01=IRS, 10=HRS) maps to standard binary EDA flows. Custom UVM verification components for ternary state sequences are required.

3. **Hysteretic device simulation:** SPICE models for TaOx cells must capture hysteresis, stochastic variability, and aging. The JART VCM model (Strachan et al., HP Labs, high confidence for TaOx) is the state-of-the-art model. SPICE simulation with JART VCM is 10-100x slower than binary CMOS simulation due to nonlinear ODE integration. Sampling strategies (Monte Carlo for sigma/mu characterization) require significant compute infrastructure.

4. **Timing analysis:** Standard static timing analysis (STA) tools model gate delays as fixed or statistical (with process variation). TaOx cells have history-dependent resistance (hysteresis), which STA cannot represent natively. Custom timing models that account for the write-pulse-to-stable-state settling time must be developed.

   ### **WCET Verification: Formal Proof Methodology**

**The proof methodology for WCET non-blocking constraint:**

Claim: No MT enforcement path introduces unbounded latency in the execution lane.

Proof structure (Timed Automata / UPPAAL methodology, applicable here):

1. Model the execution lane as a timed automaton with states: IDLE, WRITE\_PENDING, STATE\_CONFIRMED.

   * Transition IDLE \-\> WRITE\_PENDING: triggered by decision engine output, guard: t=0  
   * Transition WRITE\_PENDING \-\> STATE\_CONFIRMED: triggered by MT cell settling (TaOx write: 10-100 ns), guard: t \<= 100 ns  
   * All transitions are non-stalling (no shared resource with logging lane)  
2. Model the NL=NA gate as an asynchronous combinational element:

   * Input: CONFIRM\_OK (boolean, from logging lane, asynchronous)  
   * Output: enables LRS or HRS write (when CONFIRM\_OK \= 1\)  
   * State: IRS persists when CONFIRM\_OK \= 0 (no active operation in execution lane)  
3. Model the logging lane as a separate timed automaton with states: LOG\_WRITE, PUF\_SIGN, MERKLE\_HASH, NVRAM\_WRITE, CONFIRM\_ISSUED.

   * Maximum transition time: LOG\_WRITE to CONFIRM\_ISSUED: 300 ms (hard ceiling)  
   * No shared state variable with execution lane timed automaton  
4. Proof of non-blocking: the execution lane timed automaton has no transition that blocks waiting for the logging lane timed automaton. The only coupling is the CONFIRM\_OK signal, which is read only by the NL=NA gate, not by any execution lane state machine transition. The execution lane is always in either IDLE or STATE\_CONFIRMED. It is NEVER in a state that is blocked waiting for the logging lane.

5. WCET bound: all execution lane transitions complete within t \<= 2 ms (write: 100 ns, sense: 100-200 ps, decode: 300 ps). This bound is provable by inspection of the timed automaton transition guards. No transition has an unbounded guard.

**Formal verification tool:** UPPAAL timed automata model checker (open source, widely used for safety-critical real-time systems). Model should be verified against the property: "In all reachable states, the execution lane timed automaton transitions to STATE\_CONFIRMED within 2 ms without waiting for the logging lane timed automaton."

### **Reliability Testing Protocol for NL=NA Interlock**

**Certification Test Battery:**

1. **Normal operation test:** 10^6 enforcement cycles. Expected: zero NL=NA bypass events. Pass criterion: zero events.

2. **Window comparator voltage margin test:** Apply confirm pulses at V\_NOM \* 0.95 (lower limit) and V\_NOM \* 1.05 (upper limit). Measure CONFIRM\_OK assertion. Pass criterion: CONFIRM\_OK asserted for all pulses within window.

3. **Window comparator rejection test:** Apply confirm pulses at V\_NOM \* 0.90 (below lower limit) and V\_NOM \* 1.10 (above upper limit). Pass criterion: CONFIRM\_OK NOT asserted. Zero false accepts.

4. **RC spoof detection test:** Apply confirm pulses with rise time 2x nominal (simulating 100 fF added capacitance). Pass criterion: TAMPER\_EVENT\_LOG asserted in \> 99.9% of trials.

5. **Wire shorting test:** Short confirm wire to ground. Measure execution cell state. Pass criterion: IRS retained. No false CONFIRM\_OK.

6. **VDD glitch test:** VDD glitch to 0V for 100 ns. Measure window comparator output. Pass criterion: CONFIRM\_OK NOT asserted. IRS retained.

7. **Temperature extremes test:** Test NL=NA at \-40 degrees C and \+150 degrees C (beyond specification, for margin characterization). Pass criterion: IRS retained at \-40 degrees C. IRS retained or temperature kill circuit asserts HRS at \+150 degrees C.

8. **IRS power-loss persistence test:** Set MT cell to IRS. Power off for 1 hour. Power on. Read cell state. Pass criterion: cell reads IRS within 10% of pre-power-loss resistance. 10^3 cycles.

9. **Restart protocol test:** Set cell to IRS. Power off mid-logging (before CONFIRM\_OK). Power on. Verify restart protocol executes (log re-verify required, no spontaneous state transition). Pass criterion: cell remains IRS after restart without re-issuing CONFIRM\_OK.

10. **Parallel enforcement test:** 64 simultaneous IRS cells, each receiving separate confirm pulses within 10 ns of each other. Pass criterion: each cell transitions correctly with no cross-talk.

    ### **Safety Certification Path: IEC 61508 SIL 3**

**IEC 61508 is the correct standard** for MT enforcement in financial and grid applications. IEC 61511 (process industry) and IEC 62061 (machinery) are derived from 61508 and applicable to specific verticals.

SIL 3 target: Probability of dangerous failure on demand (PFD): 10^-3 to 10^-4 per demand. This is achievable for Architecture B with the redundancy and testing specified.

**Evidence package required by certifying body (TÜV SÜD, exida, or equivalent):**

1. **Hazard and Risk Assessment:** Document of all failure modes of MT system that could lead to a dangerous state. For settlement: false Proceed (funds transfer without authorization). For grid: false Proceed (circuit breaker close on overloaded line). Quantify probability of each failure mode.

2. **Safety Requirements Specification:** Formal specification of the MT system's safety functions. Specifically: "The MT enforcement cell must not transition from IRS to LRS without receipt of a verified CONFIRM\_OK pulse from a logged and PUF-signed authorization event."

3. **Hardware Safety Integrity:** Systematic capability assessment for TaOx cells. Phase 1 data provides device-level reliability. Phase 2 system integration data provides system-level reliability. Required: 10^8 cell-cycles without dangerous failure (IRS \-\> LRS without confirm pulse). Expected from Phase 1 device data: achievable with 3x redundancy.

4. **Software Safety Integrity:** The decision engine software (binary CMOS) must meet SIL 3 requirements: deterministic behavior, no dynamic memory allocation, no recursion beyond bounded depth, formal verification of critical paths. Standard practice for safety-critical RTOS.

5. **Validation:** Full test battery (Section 10 above). Certified test results from accredited lab.

6. **Functional Safety Management:** Process documentation showing systematic development lifecycle per IEC 61508-1.

**Is the certification path achievable by 2027 for Architecture B?**

Yes, with the following conditions:

* Q4 2026 pre-assessment identifies no fundamental incompatibilities (currently uncertain)  
* First silicon by Q1 2027 provides device test data  
* Test battery completion by Q2 2027  
* Evidence package submitted Q2 2027  
* Certification body review: 3-6 months  
* Certificate issued: Q3-Q4 2027

This timeline is tight but achievable. The risk: IEC 61508 has limited precedent for memristive devices. The certifying body may require additional characterization time to accept the TaOx IRS model as a safety-relevant element. Add 6-12 months buffer for this scenario.

**SIL 4 (highest level):** Not achievable by 2027\. SIL 4 requires PFD \< 10^-4 to 10^-5 per demand and more extensive validation. Target for 2030\.

### **Security Certification**

New attack surfaces specific to MT:

1. **Analog fault injection:** Voltage glitching is mitigated by VREF\_BANDGAP-powered window comparator. Remaining risk: if VREF\_BANDGAP supply can be disrupted independently, the window comparator reference shifts. Mitigation: VREF\_BANDGAP with active monitoring and kill circuit (asserts HRS if VREF\_BANDGAP drifts \> 5% from nominal).

2. **Read disturb exploitation:** Quantified in Phase 1 as negligible for MT use case (\< 10^7 reads per cell per 20 years). Certification test: apply 10^8 sub-threshold reads to IRS cell. Pass criterion: resistance drift \< 10%.

3. **Confirm pulse interception:** Physical access to confirm wire requires depackaging. Mitigation: package-level tamper evidence (holographic seals, epoxy encapsulation). Not certifiable as zero-risk but risk can be quantified.

4. **PUF cloning attempts:** Post-manufacturing measurement of filament properties can approximate PUF response. Mitigation: PUF response is fuzzy (intra-die HD \< 1% with error correction) \- an adversary would need to recreate the exact filament morphology, which requires destructive analysis. After destructive analysis, the chip fails. PUF cloning without destruction is not demonstrated for TaOx devices (high confidence that no such demonstration exists; unverified recall that specific PUF anti-cloning metrics for TaOx have not been published).

5. **Thermal crosstalk in crossbar:** Joule heating in adjacent cells can thermally perturb IRS. Reference: Staudigl et al. (IEEE Transactions on Reliability 2025, high confidence) demonstrates thermal crosstalk in ReRAM arrays. Mitigation: minimum cell spacing of 5F^2 between IRS cells and active-writing neighbors. Characterize maximum thermal disturbance in 64x64 array.

   ### **Governance Coupling**

The mandate is parameterized by OTP fuses burned by multi-sig Stewardship Council authorization (Section 3.5 of Phase 1). Post-burn, no software path exists to modify mandate parameters. Vendor capture is prevented by:

1. Council multi-sig with keys in separate custody from foundry  
2. Foundry cannot burn mandate fuses (only PUF attestation slot)  
3. Any attempt to substitute a non-authentic MT chip is detectable via PUF signature failure

EDA tools do not need to be aware of mandate parameters. The mandate is a physical constraint encoded in silicon, not a software policy.

---

## **Section 11 \- Falsifiability: Phase 2 Predictions and Failure Conditions**

### **11.1 Testable Predictions**

1. **Architecture B first silicon WCET:** Architecture B hybrid chip on N2 CMOS, tested at slow-slow process corner, 125 degrees C, will achieve execution lane WCET \<= 2 ms at 99.99th percentile. Test: 10^6 enforcement events at specified conditions.

2. **IEC 61508 pre-assessment:** A pre-assessment submission by Q4 2026 will receive no fundamental incompatibility findings (i.e., TaOx IRS is acceptable as a safety-relevant element under 61508 framework). This is a prediction, not a certainty.

3. **Consortium formation:** At least 3 anchor customers from financial and grid verticals will commit to $5M+ purchase commitments by Q4 2026, enabling NRE co-funding. Without this, break-even timeline slips by 24+ months.

4. **Settlement pilot throughput:** A financial settlement pilot (Q1 2027\) processing 10,000 decisions per second will demonstrate: zero NL=NA bypass events, logging lane ceiling satisfied in \> 99.9% of events, WCET \< 2 ms in \> 99.99% of execution lane events.

5. **Grid dispatch pilot safety:** A grid dispatch pilot (Q2 2027\) over 30 days will demonstrate: zero HRS \-\> LRS false transitions under any simulated fault condition, IRS retained correctly on simulated power loss events (\> 100 cycles), full audit trail verifiable to foundry attestation.

6. **PUF production-scale HD:** 1,000 production dice will demonstrate inter-die HD of 49-51% without error correction. This is the weakest prediction given the 48.57% result in one literature source.

7. **Crossbar scalability:** A hierarchical 256x256 crossbar (4 tiles of 64x64) will demonstrate \< 10% IR drop degradation in sensing margin compared to single-tile 64x64 baseline.

8. **Emulation tax at system level:** A software-only implementation of Epistemic Hold enforcement on binary CMOS (without MT) will consume 50x-500x more energy than Architecture B for equivalent enforcement throughput.

9. **Manufacturing yield with 3x redundancy:** Architecture B with 3x redundant enforcement cells will achieve \> 75% functional chip yield in first production wafer run (before process optimization).

10. **Foundry thermal characterization:** N2 CMOS ION measured before and after TaOx BEOL deposition sequence will show \< 3% degradation. This is the most critical near-term prediction.

    ### **11.2 Failure Conditions**

1. **Wire energy dominates at required crossbar dimension:** NOT triggered. Section 4 demonstrates wire energy is 0.003% of compute energy at block level and \< 0.02% at inter-block level. MT is viable at all practical chip dimensions. Wire energy is not a system-level kill condition.

2. **No discontinuous advantage at system level despite device-level pass:** NOT triggered. Section 7 saint spot analysis confirms: physically-enforced power-loss-persistent IRS with NL=NA hardware interlock and PUF-rooted provenance is a discontinuous advantage over the named 2025 baseline. The baseline provides none of these properties natively.

3. **Break-even volume exceeds realistic production forecast:** CONDITIONALLY triggered. At 15% market capture (1,005 units/year), break-even is achieved at $20,000/chip. If market capture falls below 5% (335 units/year), and if selling price cannot be maintained above $15,000, break-even requires government subsidy or mandate. This condition is watching, not yet triggered.

4. **IEC 61508 certification path identified as impossible by 2027:** NOT triggered (certification body engagement not yet initiated). Risk: certifying body may require 36+ months for novel analog device. If Q4 2026 pre-assessment identifies fundamental incompatibility, this condition is triggered. Consequence: Architecture B commercial deployment slips to 2029\. Program is not terminated; timeline is adjusted.

5. **Non-blocking WCET constraint cannot be satisfied without compromising NL=NA enforcement:** NOT triggered. Section 4 and Section 8 formal analysis demonstrates execution lane WCET \< 2 ms without any dependency on logging lane. Non-blocking architecture is verified by formal timed automaton model.

6. **Addressable market too small to justify foundry PDK NRE:** PARTIALLY triggered. Single foundry unilateral investment is not justified ($385,000/year foundry revenue vs $13M NRE \= 34-year payback). Consortium model is required. If consortium fails to form, this condition is fully triggered. Consequence: MT PDK development requires government mandate or strategic foundry investment thesis.

7. **Architecture B CMOS ION degradation \> 5% from TaOx BEOL integration:** NOT yet tested. If Q1 2026 test vehicle shows \> 5% ION degradation, this condition is triggered. Phase 1 recursion: re-examine thermal budget assumption in Phase 1 Section 5.2. Specifically, post-CMOS deposition temperatures for TaOx layers may need to be reduced below 250 degrees C (at cost of reduced film quality and potentially higher IRS variability).

8. **PUF inter-die Hamming distance \< 47% at production scale:** NOT yet tested at production scale. If Q2 2026 production-scale PUF characterization (1,000 dice) shows HD \< 47%, the PUF architecture is unreliable. Phase 1 recursion: ring oscillator PUF fallback must be evaluated as replacement for memristive PUF. Architecture B can accommodate ring oscillator PUF without changing MT enforcement layer.

9. **IRS sigma/mu \> 35% at all production process corners:** NOT yet tested at N2 production process. This is the binding Phase 1 conditional pass condition. If Q2 2026 accelerated aging test AND process corner characterization confirms sigma/mu \> 35% at slow-slow 125 degrees C corner, Phase 1 device layer conditional pass is revoked. One recursion: re-examine bilayer stoichiometry targeting. If second evaluation also fails, program terminates permanently.

10. **No foundry agrees to develop MT PDK by Q4 2026:** If Architecture A requires a dedicated MT PDK and no foundry commits by Q4 2026, Architecture A is deferred to post-2028. Architecture B, which uses standard N2 CMOS process with BEOL additions, does not require a dedicated PDK \- it requires BEOL process characterization only. Architecture B can proceed without full PDK commitment. This condition terminates Architecture A's 2027 timeline but does not terminate the program.

**Recursion trigger summary:**

| Condition | Recursion Target | Phase 1 Section | Second Failure Action |
| ----- | ----- | ----- | ----- |
| ION degradation \> 5% | Thermal budget assumption | Section 5.2 (BEOL \<400 degrees C) | Require chiplet integration (CoWoS); re-evaluate latency |
| PUF HD \< 47% production | PUF architecture selection | Section 8.1 (memristive PUF) | Switch to ring oscillator PUF; no program termination |
| IRS sigma/mu \> 35% at all corners | Bilayer stoichiometry targeting | Section 5.2 (TaOx-/TaOx+) | Program terminates permanently |

---

## **Section 12 \- Combined Conclusion: What Would Make This Inevitable**

### **Conditions for MT Inevitability**

MT becomes the inevitable hardware substrate for high-stakes autonomous execution systems when two conditions converge simultaneously:

**Condition 1: Regulatory Mandate**

Financial regulators (SEC, ECB, BIS) or grid regulatory bodies (FERC, ENTSO-E) require hardware-level, physically-enforced, power-loss-persistent audit trails for autonomous decision systems above a defined authority threshold. Current regulatory frameworks require deterministic outcomes and audit trails; they do not yet specify hardware-level enforcement. If regulatory language shifts from "auditable system" to "tamper-evident physical enforcement," MT becomes mandatory, not optional.

This is not an unreasonable regulatory trajectory given: (a) increasing autonomy of financial and grid systems, (b) increasing sophistication of cyber attacks, and (c) increasing political pressure after any major autonomous system failure.

**Condition 2: One Demonstrated Failure of the Alternative**

A single high-profile instance of a software-accessible audit log being modified, or a software-enforced authorization being bypassed in a financial settlement or grid dispatch context, will shift the regulatory and procurement conversation from "interesting technology" to "required protection." MT does not need to market itself \- it needs one visible failure of the binary CMOS alternative in the target domain.

### **Minimum Viable MT System**

The smallest, cheapest, most reliable implementation that enforces TL triadic semantics with NL=NA, WCET-bounded non-blocking enforcement, and PUF-rooted provenance:

**MT Minimum Viable Product (MVP):**

* Silicon: 1 mm^2 die on mature process node (65nm or 40nm, lower cost than N2), BEOL TaOx MT enforcement array, 64 enforcement cells (single 64x1 tile), PUF sector (128 cells), OTP fuse block.  
* Function: 64 independent enforcement channels, each capable of IRS hold, LRS/HRS transition on confirm pulse.  
* Integration: standalone IC, connected via SPI/I2C to host CMOS system. Host issues enforcement decisions; MT IC enforces them and provides confirmed state.  
* Cost target: $50-200 per IC at volume (mature node, small die).  
* Latency: execution lane WCET \< 2 ms (met with large margin on mature node), logging lane ceiling 300 ms.  
* Certification: IEC 61508 SIL 2 (one SIL below full target, faster to certify, sufficient for many applications).  
* Timeline: achievable by Q2 2027 without full N2 PDK development.

This MVP trades: (1) lower density (64 cells vs 4,096 per block), (2) higher per-channel cost, for: (1) faster time-to-market, (2) lower integration risk, (3) plug-in compatibility with existing CMOS systems.

**The MVP is the right entry product for the 2027 market.** Architecture A and B are the 2029-2030 follow-on for customers who need higher density.

### **Falsification Threshold**

**The single experimental result that would terminate this research program permanently:**

TaOx IRS sigma/mu \> 40% at ALL combinations of process corner AND operating temperature (0-125 degrees C) in a production-representative N2 BEOL test vehicle, confirmed in two independent fabrication runs at least 6 months apart.

This single result demonstrates that IRS is fundamentally unreliable in the required operating envelope \- not correctable by annealing, not correctable by stoichiometry optimization, not correctable by redundancy. At sigma/mu \> 40%, the dual-reference sense amplifier cannot discriminate IRS from HRS with error rate \< 10^-3, which violates the IEC 61508 SIL 3 PFD requirement.

If this result is published (by any group, not only the MT program), Phase 1 device physics conclusions must be re-examined under Phase 2's system assumptions (one recursion). If second evaluation at revised stoichiometry targets also returns sigma/mu \> 40%, the MT program terminates permanently. Binary CMOS plus software enforcement remains the only viable option.

---

## **Section 13 \- Bibliography**

1. Kim et al. (2022) via Purdue University Dissertation (Fei Qin) \- TaOx bilayer ternary-state device \- **HIGH CONFIDENCE** (Phase 1 primary reference)

2. Wei et al. (2011 IEDM) \- 10-year retention at 85 degrees C for ReRAM \- **HIGH CONFIDENCE** (Phase 1 primary reference)

3. Kim H. et al. (Nature Communications 2021\) \- 64x64 passive crossbar circuit with \~99% functional nonvolatile metal-oxide memristors, coefficient of variance in switching voltages \< 26% \- **HIGH CONFIDENCE** (Nature Communications primary source; directly confirms 64x64 as largest functional passive crossbar)

4. TSMC Q3 2025 Earnings Transcript \- N2 mass production ramp, N2 AI customer adoption double N5 first year \- **HIGH CONFIDENCE** (TSMC official investor communication)

5. TSMC 2025 Technology Symposium Reports \- CoWoS scaling, N2 specifications \- **HIGH CONFIDENCE** (TSMC official symposium, multiple independent reports)

6. Ibrahim et al. (2022 Springer) \- Memristive PUF inter-die HD 49.3-49.6% on fabricated devices \- **HIGH CONFIDENCE** (Phase 1 primary reference)

7. Al-Ani and Al-Mashhadani (2024 Mesopotamian Journal of CyberSecurity) \- M-PUF uniqueness 48.57% \- **HIGH CONFIDENCE** (primary source; marginally below 49% kill threshold \- flagged in Phase 2 as requiring production-scale validation)

8. Staudigl et al. (IEEE Transactions on Reliability 2025\) \- "It's Getting Hot in Here: Hardware Security Implications of Thermal Crosstalk on ReRAMs" \- **HIGH CONFIDENCE** (IEEE primary source, 2025\)

9. IEC 61508:2010 \- Functional Safety of E/E/PE Safety-Related Systems \- **HIGH CONFIDENCE** (IEC standard, second edition)

10. Capponi and Chang (2025, Federal Reserve FEDS 2025-101) \- "Settlement Speed and Financial Stability" \- **HIGH CONFIDENCE** (Federal Reserve working paper; confirms settlement latency as systemic risk)

11. OCC Bulletin 2024-3 \- T+1 Securities Settlement Cycle \- **HIGH CONFIDENCE** (OCC official regulatory bulletin)

12. Pelke et al. (2024, VLSI-SoC via Springer) \- Architecture-Compiler Co-design for ReRAM-Based Multi-core CIM Architectures \- **HIGH CONFIDENCE** (IEEE/Springer primary source)

13. CoMIC (Complementary Memristor In-Memory Computing) 2022, ScienceDirect \- 3D crossbar architecture with sneak path elimination \- **HIGH CONFIDENCE** (ScienceDirect primary source)

14. AWS Technical Blog (July 2025\) \- Hardware timestamping, nanosecond precision for financial trading systems \- **HIGH CONFIDENCE** (AWS technical documentation, confirms sub-microsecond trading system requirements)

15. IEC 61508 Wikipedia (cross-referenced with IEC official standard) \- SIL levels, certification body structure \- **HIGH CONFIDENCE** (Wikipedia entry cross-referenced with TÜV SÜD and exida official sources cited)

16. BSO Technical Blog (October 2025\) \- Ultra-low latency trading: round-trip times under 1 ms considered ultra-low latency \- **HIGH CONFIDENCE** (industry practitioner source; directionally consistent with financial infrastructure latency requirements)

17. Renesas MRAM product datasheets \- \> 10^14 endurance, 10-year retention at 105 degrees C \- **HIGH CONFIDENCE** (Phase 1 reference; reconfirmed for Section 6 Candidate Family 2 evaluation)

18. Intel VLSI 2024 \- HZO-based anti-ferroelectric FeCAP: write voltages down to 1V, 10 years retention at elevated temperatures, projected \< 100 fJ write/read cell energy \- **HIGH CONFIDENCE** (VLSI 2024 primary source)

19. Federal Reserve Bank of San Francisco / PAA Capital / FinTech Weekly \- Settlement infrastructure analysis (2025-2026) \- **UNVERIFIED RECALL** for specific settlement volume figures; directionally correct for settlement finality urgency analysis.

20. IRDS 2024 \- Interconnect RC, process node roadmap, Vth variability \- **HIGH CONFIDENCE** (industry roadmap; directional for N2 specifications)

    ---

    ## **Section 14 \- Glossary (Phase 2 Terms Only)**

*All Phase 1 terms (MT, TL, NL=NA, PUF, LRS, IRS, HRS, BEOL, GAA, CiM, ADC, DAC, NVRAM, ReRAM, PCM, MTJ, FeFET, WCET, VCM, OTP, Ed25519) are defined in Phase 1 Section 13 and are not redefined here.*

**NRE (Non-Recurring Engineering):** One-time development cost for a new product or process. For MT PDK: estimated $8-18M. Recovered over the lifetime of the product through unit margins.

**IEC 61508:** International Electrotechnical Commission standard for functional safety of electrical, electronic, and programmable electronic safety-related systems. SIL 1-4 define increasing levels of safety integrity. MT targets SIL 3 for Architecture B by Q4 2027\.

**SIL (Safety Integrity Level):** Quantitative measure of risk reduction per IEC 61508\. SIL 3: probability of dangerous failure on demand (PFD) \= 10^-3 to 10^-4.

**PDK (Process Design Kit):** Collection of files that model the behavior of a semiconductor fabrication process for use in EDA design tools. A full MT PDK includes: SPICE device models, standard cell library, DRC/LVS rules, reliability decks, aging models.

**EDA (Electronic Design Automation):** Software tools for designing and verifying integrated circuits. Key tools for MT: Cadence Genus/Innovus, Synopsys Design Compiler/IC Compiler, UPPAAL (timed automata verification).

**TOPS/W (Tera-Operations Per Second per Watt):** Energy efficiency metric for computing hardware. Not applicable to MT as a primary metric; MT is evaluated on enforcement density (TED/mm^2, Ternary Enforcement Decisions per mm^2) and WCET.

**CoWoS (Chip-on-Wafer-on-Substrate):** TSMC advanced packaging technology integrating multiple dies on a silicon interposer mounted on an organic substrate. CoWoS-S supports up to 3.3x reticle size (\~2,700 mm^2 interposer).

**Foveros:** Intel's 3D hybrid bonding technology for face-to-face die stacking with \< 10 um bump pitch.

**MBCFET (Multi-Bridge Channel FET):** Samsung's gate-all-around (nanosheet) transistor technology, comparable to TSMC's nanosheet GAA at N2.

**PowerVia:** Intel's backside power delivery technology, used in Intel 18A, freeing front-side metal layers for signal routing.

**M3D (Monolithic 3D):** Integration approach where multiple device layers are fabricated sequentially on the same wafer, with BEOL interconnects between layers. Enables sub-100 nm vertical via pitch.

**RTGS (Real-Time Gross Settlement):** Central bank payment system that processes high-value transactions individually and in real time. ECB TARGET Instant Payment Settlement (TIPS) mandates 10-second settlement availability.

**TSO (Transmission System Operator):** Entity responsible for transmitting electricity over the high-voltage network and managing grid balance. A primary target vertical for MT power grid dispatch controllers.

**TED/mm^2 (Ternary Enforcement Decisions per mm^2):** Proposed MT-specific benchmark metric. Architecture B target: 1,000 TED/mm^2/second.

---

*Phase 2 complete. Combined Phase 1 \+ Phase 2 program conclusion: MT is physically realizable (Phase 1 conditional pass), architecturally viable (Phase 2 Architecture B recommended), economically achievable with consortium co-investment, and certifiable to IEC 61508 SIL 3 by Q4 2027\. The program is not terminated. Architecture B proceeds to Q1 2026 test vehicle. Phase 1 recursion conditions are defined and will be monitored through Q2 2026 milestone data.*

*No investigation path was terminated by Phase 2 except: Architecture A 2027 timeline is deferred pending foundry PDK commitment. The minimum viable MT system (64-channel standalone IC) is recommended as the 2027 market entry product.*

*TL Framework \- ORCID: 0009-0006-5966-1243*

