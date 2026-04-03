# **PHASE 2**

## **System Architecture, Economics, and Autonomous Execution Integration**

### **Sub-title: Can the Third State Run the World?**

---

## **Section 1 \- Abstract**

The system-level implementation and economic commercialization of Mandated Ternary (MT) utilizing transition metal oxide memristors fails, permanently terminating the research program. Phase 2 confirms that the fatal architectural tension identified in Phase 1—interfacing a 0.75V TSMC N2 advanced logic baseline with the 1-3V analog confirm pulse required for physical state enforcement—cannot be resolved at the system level without violating strict Worst-Case Execution Time (WCET) deterministic constraints. While heterogeneous integration (CoWoS) can physically isolate the voltage domains, the interconnect latency, thick-oxide level-shifter area overhead, and verification complexity strictly preclude compliance with the IEC 61508 safety certification path by 2027\. Furthermore, the addressable market for ultra-high reliability autonomous execution nodes is insufficient to amortize the estimated $150M+ Non-Recurring Engineering (NRE) costs required to develop a custom mixed-signal ternary Process Design Kit (PDK) at the 2nm node. Incremental binary CMOS scaling, combined with software-enforced state machines and standardized secure enclaves, remains the only viable path for deterministic execution systems.

## **Section 2 \- Executive Summary**

Phase 2 evaluates the composition of MT device primitives into viable, scale-out system architectures for autonomous deterministic execution. The investigation strictly enforces the TSMC N2 CoWoS 1T1R 2025 baseline.

**Phase 2 Findings:**

1. **Architecture:** Native ternary crossbars fail at the system level due to interconnect IR drop and dominant wire energy at necessary scaling dimensions. Hybrid CoWoS integration solves thermal and density constraints but inherently fails the WCET non-blocking constraint due to cross-domain level-shifting latency.  
2. **Economics:** The "Saint Spot" market size for deterministic, non-ML execution systems (high-frequency trading, power grid dispatch) is estimated at 125,000 units globally. The break-even arithmetic definitively shows that NRE costs cannot be recovered at any acceptable market premium.  
3. **Certification:** The analog variability of the No Log \= No Action (NL=NA) window comparator under ±10% voltage and 0-125°C temperature fluctuations prevents the generation of a deterministic Failure Mode, Effects, and Diagnostic Analysis (FMEDA) required for IEC 61508 SIL-3 certification.

**Combined Program Conclusion:**

The Mandated Ternary hardware hypothesis is falsified. The physical interlock mechanisms required to strictly enforce Ternary Logic (TL) semantics in hardware introduce unacceptable latency and cost penalties that negate the system-level benefits.

## **Section 3 \- Inherited Constraints from Phase 1**

Phase 2 inherits the following device physics realities and constraints from Phase 1:

* **Assumptions Inherited:** TaOx ReRAM successfully retains three stable resistance states (LRS, IRS, HRS) with a \>20-year retention horizon extrapolated via the Arrhenius equation ($E\_a \= 1.1$ eV). Memristor Physical Unclonable Functions (MR-PUFs) provide cryptographically secure die-level identity with $\\sim$49% inter-die Hamming distance, provided spatial majority voting is applied.  
* **Phase 1 Failure Condition:** There is a catastrophic voltage domain crossing tension between the 0.75V TSMC N2 Gate-All-Around (GAA) logic and the 1-3V required to clear the Epistemic Hold (IRS) state via the confirm pulse.  
* **Foreclosed Capabilities:** Monolithic integration of the MT NL=NA enforcement loop directly into the 0.75V core logic path is foreclosed. The generation, routing, and verification of 1-3V analog pulses using on-chip charge pumps breaks the 99.99th percentile WCET bounds. Phase 2 must terminate any investigation into monolithic, single-die advanced logic integration of the interlock.

## **Section 4 \- System Architectures**

To bypass the foreclosed monolithic integration, two architectures are evaluated. Both attempt to isolate the voltage domain tension.

### **Architecture A: Native Ternary Crossbar Compute-in-Memory**

This architecture utilizes a passive 1S1R (one selector, one memristor) TaOx crossbar for both state enforcement and computation.

* **Organization:** Wordline/Bitline routing with threshold-based selectors to mitigate sneak-path currents.  
* **Ternary Control Plane:** Triadic states are propagated via multi-level voltage pulses, requiring high-precision digital-to-analog converters (DACs) at the edge of the array.  
* **NL=NA System Level:** The confirm pulse is driven down the wordline.  
* **Scaling Limits & Baseline Comparison:** Due to the 1-3V requirement, interconnect resistance (Cu/Ru at 2nm geometries) causes severe IR drop. Wire energy dominates compute energy past a $256 \\times 256$ crossbar dimension. TSMC N2 1T1R embedded ReRAM baseline easily scales to macro sizes of 2Mb without these routing limitations.  
* **Conclusion:** **FAILS.** Does not satisfy WCET latency bounds and scales poorly compared to the baseline.

\+---------------------------------------------------+

| Architecture A: Native Ternary Crossbar (FAILED) |

| |

| \--\> |

| | |

| |

| | |

| |

| | |

| \*\* FATAL IR DROP AT \>256x256 \*\* |

\+---------------------------------------------------+

### **Architecture B: Hybrid Memristive-CMOS with Ternary State Controller**

This architecture leverages 2.5D/3D heterogeneous integration. Computation executes on a 0.75V TSMC N2 logic die. The MT enforcement states and NL=NA interlock are pushed to a separate mature-node die (e.g., 28nm or 40nm) utilizing TSMC CoWoS-S (Silicon Interposer).

* **Integration Scheme:** CoWoS isolates the 0.75V and 3.0V domains into separate chiplets. The execution lane runs on the 2nm die; the logging lane and window comparators run on the 40nm die.  
* **NL=NA Interlock:** The decision is passed across the interposer. The 40nm die handles the 3V confirm pulse and RC signature verification.  
* **WCET Satisfaction Check:** Driving a signal off the 2nm logic die, across the interposer, into the 40nm analog die, verifying the window, and returning the Proceed signal introduces $\\sim$40-60 ns of round-trip latency. While deterministic, it creates a pipeline stall. The execution path blocks waiting for the interposer round-trip.  
* **Conclusion:** **FAILS.** While physically viable and bypassing the thermal budget constraints of monolithic BEOL integration, it strictly violates Global Constraint 1 (Non-Blocking). The execution path must halt to wait for the off-chiplet confirm pulse.

\+-------------------------------------------------------+

| Architecture B: Hybrid CoWoS Integration (FAILED) |

| |

| |

| |

| \[ Execution Lane \] \[ NL=NA Interlock \] |

| | | |

| \---\> \<---/ |

| WCET Penalty \> 50ns |

| \*\* VIOLATES NON-BLOCKING \*\* |

\+-------------------------------------------------------+

## **Section 5 \- Foundry Technology Alignment and Roadmap**

The architectures map against TSMC N2 (GAA, CoWoS), Intel 18A (PowerVia), and Samsung SF2.

**2026-2027 Milestone Table**

| Quarter | Architecture | Deliverable | Success Criteria | Kill Criterion |
| :---- | :---- | :---- | :---- | :---- |
| Q1 2026 | Arch B (Hybrid) | Multi-die interface spec | Interposer RC delay \< 10ns | If interposer delay \> 25ns, abandon Arch B. |
| Q2 2026 | Arch A (Crossbar) | 512x512 array tapeout | Read margin \> 150mV at edge | If IR drop collapses window comparator margins to \< 5%, abandon Arch A. |
| Q3 2026 | Arch B (Hybrid) | Window Comparator IP | Tamper detection \> 99.9% | If RC spoofing falls inside $\\pm$5% comparator tolerance, abandon program. |
| Q4 2026 | System Level | WCET bound simulation | Execution lane WCET $\\le$ 2ms | If execution stalls on 300ms logging lane, trigger Phase 1 recursion. |
| Q1 2027 | Root of Trust | MR-PUF integration | Inter-die HD \> 48% at 125°C | If SMV overhead increases power by \> 20%, fail security architecture. |
| Q2 2027 | Standardization | IEC 61508 pre-audit | FMEDA report finalized | If analog jitter prevents SIL-3 target achievement, abandon program. |

## **Section 6 \- Top Three Candidate Architectures for 2027 Standardization**

"Standardized" is operationally defined as possessing a foundry-supported PDK with comprehensive variability corners and reliability decks, integration with Synopsys/Cadence EDA synthesis flows, and a clear, documented path to IEC 61508 SIL-3 certification.

| Criterion | Minimum Viable | Industry Standard |
| :---- | :---- | :---- |
| Foundry PDK | Device models, DRC | Variability corners, reliability decks |
| EDA support | Custom ternary simulator | Integrated Cadence/Synopsys flows |
| IP ecosystem | 1 vendor, 1 macro | 3+ vendors, synthesis libraries |
| Benchmarking | Proprietary workload | Standardized settlement/matching benchmark |
| Certification | Self-certified | IEC 61508 or equivalent path |

**Candidate Families:**

1. **Compute-in-Memory with TaOx Memristor Crossbars:**  
   * *Core Principle:* VCM-driven triadic state manipulation.  
   * *CMOS Status:* Demonstrated at 40nm. Unproven monolithically at 2nm.  
   * *Killer Obstacle:* IR drop and high write energy.  
   * *Benchmark Target:* 1 TOPS/W.  
   * *Governance Target:* TL triadic enforcement via NL=NA.  
   * *Kill Criterion:* Wire energy dominates at required throughput.  
   * *Comparison to Baseline:* Severely trails N2 1T1R in write speed and energy efficiency.  
2. **Spintronic / STT-MRAM:**  
   * *Core Principle:* Magnetic tunnel junction (MTJ) state switching via spin-polarized current.  
   * *CMOS Status:* High maturity. Embedded in 22nm and scaled to 16nm/14nm.  
   * *Killer Obstacle:* STT-MRAM is intrinsically binary (parallel/anti-parallel magnetization). Engineering a stable ternary "Hold" state is highly stochastic and prone to thermal flipping.  
   * *Benchmark Target:* 10 TOPS/W.  
   * *Kill Criterion:* Inability to retain a stable intermediate magnetic state for \>10 years. (Phase 1 recursion trigger).  
   * *Comparison to Baseline:* Excellent binary alternative, completely fails ternary requirements.  
3. **Ferroelectric FET (FeFET):**  
   * *Core Principle:* Polarization of HfO2 dielectrics shifting transistor threshold voltages.  
   * *CMOS Status:* Demonstrated at 3nm/2nm scale in research.  
   * *Killer Obstacle:* Severe endurance limitations ($10^{10}$ cycles) and "wake-up" effects that alter the state boundaries over time, ruining the sensing margins for an intermediate state.  
   * *Kill Criterion:* Cycle-to-cycle threshold drift destroys the Epistemic Hold sensing margin.  
   * *Comparison to Baseline:* Trails N2 1T1R baseline in endurance.

## **Section 7 \- The Saint Spot: Market Gap Analysis**

The "saint spot" is defined as the specific bottleneck zone where MT yields a discontinuous advantage that incremental binary scaling cannot match, specifically: the requirement for zero-power, cryptographically bound, immutable hardware state enforcement that is physically impervious to software override.

Unfortunately, compared to the 2025 TSMC N2 NVRAM baseline, this spot is narrow, as modern secure enclaves emulate this satisfactorily for most threat models.

**Problem-Mechanism-Advantage Mapping Table**

| Problem Bottleneck | MT Mechanism | Why Binary \+ Software Cannot Match | Quantified Delta vs 2025 N2 Baseline |
| :---- | :---- | :---- | :---- |
| Malicious Software Override | NL=NA physical interlock | Binary state machines reside in volatile flip-flops subject to OS-level attacks. | 100% reduction in software state-tampering vectors; \>10,000x latency penalty. |
| Power Loss State Corruption | Non-volatile Epistemic Hold (IRS) | Binary logic loses state without power unless checkpointed to bulk NVRAM. | 0 fJ static retention power vs active SRAM leakage (\~10-50 pW/cell). |
| Provenance Spoofing | MR-PUF Identity | Factory-burned eFuses represent centralized, single-vendor trust vectors. | Unclonable physical entropy; 49% Hamming distance vs 0% (known factory keys). |

### **7.5 Addressable Market Quantification**

Bottom-up estimate for critical infrastructure control nodes requiring strict deterministic state binding:

* **Target Verticals:** High-frequency financial settlement engines, national power grid dispatch controllers, nuclear SCADA.  
* **Number of Nodes:**  
  * Financial settlement: $\\sim$25,000 global matching engines and institutional gateways.  
  * Power grid / SCADA: $\\sim$100,000 critical transmission/distribution substations.  
* **Total Units:** 125,000 nodes.  
* **Replacement Cycle:** 5 to 7 years.  
* **Willingness to Pay (Premium):** Due to the catastrophic cost of failure (e.g., flash crashes, grid blackouts), institutions will pay an estimated $1,000 premium per MT-enabled trusted processor.  
* **Total Addressable Market (TAM):** 125,000 units $\\times$ $1,000 \= $125,000,000 revenue.

## **Section 8 \- Autonomous Execution Systems as Catalyst**

**Worked Example: High-Frequency Settlement Finality Engine**

High-frequency trading (HFT) and settlement environments require execution within microseconds and demand absolute deterministic finality to eliminate counterparty risk.

* **System Architecture:** The matching engine runs on the TSMC N2 0.75V logic execution lane. When a trade meets clearing conditions, the system transitions to Epistemic Hold (0).  
* **NL=NA Context:** The Hold state is triggered by the settlement request. A valid confirm pulse (2.0V) is routed from the logging hardware only after the trade details (price, volume, cryptographic signatures) are written to the immutable ledger.  
* **Refuse (-1) Event:** If the account lacks funds or a kill-switch is activated, the hardware drops to HRS. No further trading on that specific context can occur. The audit trail locks the failed state into the Merkle tree.  
* **Root of Trust:** A log entry is signed by the die's MR-PUF. The foundry attests this public key at wafer sort. If the foundry ceases to exist, public keys are escrowed in a decentralized, mathematically verifiable ledger.  
* **Baseline Comparison:** The 2025 N2 baseline utilizes software state machines to achieve this. Software is significantly faster but lacks the absolute hardware lock. Because MT requires analog pulse generation and verification, it breaks the deterministic latency requirement.

**Sequence Diagram**

Input

\-\> Decision Engine (0.75V Logic Domain)

\-\> Ternary Decision State \[+1 / 0 / \-1\] Evaluated

\-\> Mandate Check (NL=NA interlock, hardware-coupled)

\-\> No confirm pulse \-\> IRS retained \-\> Epistemic Hold

(non-blocking: execution path must NOT poll logging path)

\*\*\*\*

\-\> Immutable Log Write (parallel lane, hard ceiling 300 ms)

\-\> Merkle Hash Calculated

\-\> PUF-signed entry (post-manufacturing entropy applied)

\-\> Foundry Attestation verified (Key from Wafer Sort Escrow)

\-\> \[+1\] Confirm pulse verified \-\> LRS \-\> Action permitted

(WCET \<= 2 ms boundary)

\-\> \[-1\] HRS \-\> Refuse, log entry written, no action permitted

\-\> Hardware Root of Trust chain updated

## **Section 9 \- Economics and Manufacturing Viability**

To bring MT to standard manufacturing, massive NRE costs are incurred.

* **Cost per Cell:** The physical TaOx cell is marginally cheap (comparable to standard BEOL ReRAM), but the area overhead of the 3.0V level shifters inflates the effective macro area by $50\\times$ to $100\\times$.  
* **NRE Costs:** Developing a custom 2nm PDK with comprehensive analog models, DRC decks, and specific window comparator macros for a novel voltage domain crossing requires an estimated $150,000,000.  
* **Time-to-Market:** Incremental binary scaling is available today. MT requires a minimum 4-year development cycle.  
* **Break-Even Production Volume Calculation:**  
  * $NRE \= \\$150,000,000$.  
  * Premium per unit \= $1,000.  
  * Required units to break even \= $NRE / Premium \= 150,000$ units.  
  * *Result:* The required break-even volume (150,000) exceeds the total realistically addressable market for critical nodes (125,000).  
* **Conclusion:** The economics do not support commercialization. The foundry revenue opportunity is negative. A minimum viable alternative is required: utilizing standard binary 1T1R arrays with software-defined secure enclaves (e.g., ARM TrustZone or RISC-V equivalent).

## **Section 10 \- EDA, Verification, and Certification**

* **EDA Changes:** Synthesis tools must account for multi-voltage domain crossings directly inside logic paths, which current Cadence/Synopsys digital flows do not natively support without heavy custom mixed-signal intervention.  
* **WCET Verification:** Proving bounded latency relies on Static Timing Analysis (STA). The analog nature of the charge pump generating the 2.0V confirm pulse introduces unacceptable jitter, making a formal proof of WCET at the 99.99th percentile impossible.  
* **Safety Certification (IEC 61508):** To achieve SIL-3, a complete FMEDA (Failure Mode, Effects, and Diagnostic Analysis) is required. The certifying body requires proof of deterministic failure containment. Because the MT system relies on stochastic filament dynamics and analog comparators subject to read-disturb and temperature drift, proving bounding limits to an IEC auditor by 2027 is impossible.  
* **Security Certification:** The RC signature of the confirm pulse provides excellent resistance to pulse spoofing. However, analog fault injection (e.g., glitching the bandgap reference of the window comparator) remains a critical attack surface.

## **Section 11 \- Falsifiability: Phase 2 Predictions and Failure Conditions**

**10 Testable Predictions:**

1. CoWoS integration of a 0.75V logic die and a 3.0V analog memristor die will introduce an interposer transit and level-shifting latency $\> 40$ ns.  
2. Wire energy for routing the 2.0V confirm pulse will exceed compute energy at array dimensions of $256 \\times 256$.  
3. NRE costs for a hybrid 2nm/40nm MT PDK will exceed $150 million.  
4. Total Addressable Market for MT-specific hardware nodes will not exceed 150,000 units by 2030\.  
5. MR-PUFs will require minimum SMV-3 (Spatial Majority Voting) logic to maintain Bit Error Rates (BER) $\< 10^{-6}$ across the 0-125°C temperature window.  
6. The window comparator $\\pm$5% tolerance will drift under continuous 125°C thermal stress, generating false-positive Refuse states.  
7. IEC 61508 SIL-3 certification will be denied due to the inability to bound analog charge pump jitter within the FMEDA.  
8. Standard EDA tools will fail to synthesize the NL=NA interlock without custom mixed-signal blocks.  
9. Area overhead for the 3V-tolerant transistors will penalize logic density by $\>20\\%$ relative to the N2 baseline.  
10. The deterministic high-frequency settlement engine will suffer a pipeline stall during the Epistemic Hold state evaluation.

**10 Kill Conditions (Failure Modes):**

1. **WCET Violation:** The non-blocking WCET constraint cannot be satisfied because the interposer and level-shifter delay introduces a hard pipeline stall. (TRIGGERED).  
2. **Economic Failure:** Break-even volume (150,000 units) exceeds the realistic TAM (125,000 units). (TRIGGERED).  
3. **Certification Blockage:** IEC 61508 certification path identified as impossible within the 2027 timeline due to analog variability. (TRIGGERED).  
4. **No System Advantage:** MT yields no discontinuous latency or energy advantage over the 2025 N2 SRAM/NVRAM baseline. (TRIGGERED).  
5. **Interconnect Dominance:** Wire energy dominates at the crossbar dimension required for target HFT throughput.  
6. **PUF Area Inflation:** Error correction (SMV) for the MR-PUF inflates logic area beyond viable SoC budgets.  
7. **Thermal Constraint Limit:** Hybrid bonding of the analog die creates thermal hotspots that degrade the 2nm logic layer.  
8. **Routing Congestion:** CoWoS interposer routing cannot handle the density of confirm pulses required for parallel multi-threading.  
9. **Security Failure:** Analog fault injection reliably bypasses the window comparator.  
10. **Market Rejection:** Institutional buyers prefer software-auditable enclaves over rigid hardware lock-outs.

**Recursion Trigger:**

Phase 2 triggers Phase 1 recursion based on Kill Condition 1 (WCET Violation).

*Re-examination required:* Phase 1 must re-evaluate whether a 1-3V confirm pulse is an absolute physical necessity for transition metal oxides. Can TaOx, or an alternative VCM material, be engineered to execute non-volatile triadic state switching reliably using exclusively 0.75V pulses to eliminate the level-shifting latency? If device physics dictates $V\_{set}/V\_{reset}$ strictly $\> 1.0$V, the MT program terminates permanently.

## **Section 12 \- Combined Conclusion: What Would Make This Inevitable**

Under current TSMC N2 paradigms, MT is economically and architecturally unviable. The fundamental physical requirement of moving a metal-oxide memristor across distinct resistance states requires voltages (1-3V) that are deeply hostile to the ultra-scaled, low-voltage (0.75V) environment of modern advanced logic. This voltage tension forces the use of level shifters, charge pumps, or heterogeneous CoWoS integration—all of which introduce non-deterministic latencies that break the core requirement of non-blocking autonomous execution.

Mandated Ternary only becomes the inevitable successor to binary CMOS if the voltage domain tension is resolved natively. The minimum viable MT system requires the discovery of a non-volatile, memristive material capable of distinct, reliable triadic state switching at $\\le 0.75$V, completely eliminating the need for analog level shifters.

**Falsification Threshold:** The publication of a peer-reviewed device demonstrating stable, 20-year retention, triadic resistance states (LRS, IRS, HRS) switchable at 0.75V with an activation energy $E\_a \\ge 1.1$ eV, natively integratable into the N2 BEOL. Until this specific device exists, binary CMOS with embedded ReRAM and software-defined secure enclaves remains the superior, necessary baseline.

## **Section 13 \- Bibliography**

* TSMC N2 Process Overview, GAAFET, BSPDN, and Performance Targets (High Confidence).  
* TSMC 40nm/22nm embedded ReRAM (1T1R) integration capabilities and specifications (High Confidence).  
* TSMC 3DFabric and CoWoS Interposer scaling capabilities (High Confidence).  
* IEC 61508 Functional Safety standard scope and hardware validation rules (High Confidence).  
* IEC 61508 FMEDA and Failure Mode analytical requirements (High Confidence).  
* MR-PUF normalized inter-die Hamming distances, voltage masking, and Spatial Majority Voting (High Confidence).  
* High-Frequency Trading latency, jitter, and deterministic architecture requirements (High Confidence).  
* Deterministic Event-Driven Sequencer architectures in HFT platforms (High Confidence).  
* Level shifter area, power, and delay overhead at ultra-scaled nodes (High Confidence).  
* Analog window comparator circuit design and RC response verification (High Confidence).  
* Foundry digital certificate generation and PUF public key attestation at Wafer Sort (High Confidence).

## **Section 14 \- Glossary**

* **BSPDN:** Backside Power Delivery Network; routes power below the transistor to reduce IR drop.  
* **CoWoS:** Chip-on-Wafer-on-Substrate; TSMC's advanced heterogeneous 2.5D/3D packaging technology.  
* **DRC:** Design Rule Check; automated verification that a layout meets foundry manufacturing capabilities.  
* **EDA:** Electronic Design Automation; the software tools used to design and verify integrated circuits.  
* **FMEDA:** Failure Modes, Effects, and Diagnostic Analysis; a systematic analysis technique required for safety certification.  
* **GAA:** Gate-All-Around; an advanced transistor architecture (nanosheet) replacing FinFETs at the 2nm node.  
* **HFT:** High-Frequency Trading; algorithmic financial execution requiring deterministic sub-millisecond latencies.  
* **IEC 61508:** The international standard for functional safety of electrical/electronic/programmable electronic safety-related systems.  
* **NRE:** Non-Recurring Engineering; the one-time cost to research, develop, and test a new product or PDK.  
* **PDK:** Process Design Kit; a set of files used within the semiconductor industry to model a fabrication process for the EDA tools.  
* **SIL:** Safety Integrity Level; a relative level of risk-reduction provided by a safety function (ranges from 1 to 4).  
* **SMV:** Spatial Majority Voting; an error-correction scheme used to stabilize PUF outputs against environmental noise.  
* **TOPS/W:** Tera Operations Per Second per Watt; a metric of energy efficiency in compute hardware.

