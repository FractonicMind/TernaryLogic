\*\*Instructions to the AI Researcher\*\*

You are executing Phase 1 of a two-phase research program. Phase 2 exists but you do not have access to it yet and must not anticipate it.

Your only task is to answer the Phase 1 core question honestly, layer by layer, using the evidence and calculations available to you. You are not building toward a predetermined conclusion. You are testing a hypothesis.

\*\*Read these instructions before proceeding:\*\*

\- Treat every section requirement as mandatory. If you cannot satisfy a requirement with evidence or calculation, state this explicitly and bound the uncertainty. Do not fill gaps with plausible-sounding assertions.

\- At each layer, conclude pass or fail before moving to the next layer. Do not average across layers. A pass at device level does not redeem a fail at circuit level.

\- The comparative baseline is named and fixed: TSMC N2 CoWoS with embedded ReRAM (1T1R), 2025 PDK. Every quantitative claim must be compared against this baseline. If MT shows no discontinuous advantage at a given layer, state this. This is a valid and important finding, not a failure of the research.

\- The non-blocking constraint is absolute. If any enforcement mechanism you describe introduces unbounded latency in the execution path, you must flag it as a constraint violation, not work around it silently.

\- The falsifiability section is not a formality. List conditions that would genuinely kill this program. If you cannot think of ten honest failure conditions, you are not being rigorous enough.

\- Do not write to please. Write to be falsified. A report that identifies real failure conditions is more valuable than one that argues for feasibility at every turn.

\- Citations must be labeled "high confidence" or "unverified recall." Do not present unverified recall as established fact.

\- When Phase 1 is complete, your Section 11 conclusion will be inherited directly by Phase 2\. Write it with that responsibility in mind. Be precise about what passed, what failed, and what Phase 2 may and may not assume.

\---

\# Mandated Ternary: Hardware Implementation of Ternary Logic  
\#\# From Device Physics to System Architecture  
\#\#\# A Two-Phase Technical Research Report  
\*Ternary Logic Framework \- Hardware Architecture Folder\*  
\*ORCID: 0009-0006-5966-1243\*

\---

\*Phase 1 and Phase 2 are standalone research documents sharing identical terminology, resistance state definitions, and trust chain architecture. Phase 1 output is inherited by Phase 2\. Where Phase 1 concludes failure at any layer, Phase 2 terminates that investigation path completely. No workarounds permitted.\*

\---

\# PHASE 1  
\#\# Device Physics, Circuit Primitives, and Physical Interlock Mechanisms  
\#\#\# Sub-title: Can the Third State Be Built Into Matter?

\---

\*\*Act as a Lead Semiconductor Physicist and Circuit Design Engineer with specialization in resistive switching devices, compute-in-memory, and post-CMOS logic primitives. Your task is to produce Phase 1 of a two-phase technical research report evaluating the physical feasibility of Mandated Ternary (MT) \- the hardware implementation of the Ternary Logic (TL) decision framework.\*\*

\*\*Audience:\*\* device physicists, circuit designers, process integration engineers, and EDA architects.

\*\*Tone:\*\* rigorous, technical, unsentimental. Avoid marketing language. Where data is missing, state assumptions explicitly and bound uncertainty. If multiple interpretations exist, present them, choose one, and justify it.

\*\*Critical instruction:\*\* If MT is not physically or economically viable at any layer evaluated in this phase, conclude failure at that layer explicitly and explain why binary CMOS plus software is sufficient. Agreement without resistance is not acceptable.

\---

\*\*Terminology Hierarchy \- Establish Once, Use Consistently\*\*

\- \*\*Mandated Ternary (MT):\*\* the hardware implementation architecture.  
\- \*\*Ternary Logic (TL):\*\* the formal decision framework that MT physically instantiates.  
\- \*\*TL triadic states and their MT hardware mappings:\*\*  
  \- Proceed (+1): Low Resistance State (LRS), \~1-10 kΩ  
  \- Epistemic Hold (0): Intermediate Resistance State (IRS), \~100 kΩ \- 1 MΩ  
  \- Refuse (-1): High Resistance State (HRS), \~1-10 MΩ  
\- \*\*NL=NA:\*\* No Log \= No Action \- a physical interlock, not a software check.  
\- \*\*PUF:\*\* Physical Unclonable Function \- die-level identity from post-manufacturing physical entropy, not factory-programmed values.  
\- \*\*WCET:\*\* Worst-Case Execution Time \- provably bounded at 99.99th percentile with σ/μ \< 10% under all operating conditions.  
\- \*\*MT:\*\* hardware contexts only. \*\*TL:\*\* semantic/decision contexts only.

\---

\*\*Global System Constraints \- Apply at Every Layer Without Exception\*\*

\*\*Constraint 1 \- Non-Blocking Enforcement:\*\*  
Reject any design that introduces blocking behavior in the execution path of TL state transitions. All enforcement mechanisms must be either non-blocking or bounded within deterministic latency guarantees. "Deterministic" is defined as WCET provably bounded at the 99.99th percentile with σ/μ \< 10% under all operating conditions: temperature 0-125°C, voltage ±10%, process corners. Epistemic Hold is a parallel state, not a serial stall. The logging path runs parallel to execution \- never serial. Any architecture that converts Epistemic Hold into unbounded execution latency has failed. State this explicitly if it occurs.

\*\*Constraint 2 \- Comparative Baseline:\*\*  
At every layer, include a direct comparison to the following named baseline: TSMC N2 CoWoS with embedded ReRAM (1T1R), 2025 PDK. If a superior demonstrated alternative is published in IEDM or VLSI 2025, use that and name it explicitly. If MT does not demonstrate a clear, quantified, discontinuous advantage over this baseline at any given layer, state this explicitly. Incremental improvement is not sufficient justification. The advantage must be architectural or discontinuous.

\---

\*\*Phase 1 Core Question\*\*

Can the three TL states (Proceed, Epistemic Hold, Refuse) be physically instantiated as stable, non-volatile, hardware-enforced resistance states in memristive devices \- with sufficient reliability, sensing margin, and endurance for deterministic autonomous execution systems operating over a 20-year horizon?

Answer layer by layer. Conclude pass or fail at each layer before proceeding to the next.

\---

\*\*Scope Exclusions\*\*

Excluded entirely: machine learning inference, neural network accelerators, large language model pipelines, or any system where "decision" implies statistical pattern matching. The target domain is deterministic autonomous execution systems in industrial, financial, and critical infrastructure contexts.

\---

\*\*Section 1 \- Abstract (150-250 words)\*\*

Single core claim. State it in the first sentence.

\---

\*\*Section 2 \- Executive Summary (one page)\*\*

What Phase 1 finds. What it leaves to Phase 2\. What would constitute immediate termination of the research program.

\---

\*\*Section 3 \- Definitions and Scope\*\*

\- Binary CMOS baseline: logic levels, noise margins, switching energy.  
\- Memristor vs memristive system: ideal vs practical distinction.  
\- Hysteresis window: why it enables stable multi-state memory.  
\- Mandate: enforcement mechanism, not governance philosophy.  
\- MT vs TL hierarchy as above.  
\- NL=NA: physical interlock with confirm pulse \- voltage write pulse on dedicated hardware wire, not software flag.  
\- Epistemic Hold (IRS): designed enforcement state, not logical uncertainty. Explicit justification required: "Epistemic Hold repurposes the logical intermediate state as a deliberate enforcement pause. The system has sufficient information to proceed or refuse, but lacks authorization confirmation. This is not logical uncertainty \- it is authorization pending. Unlike binary wait states which stall execution, IRS is a stable resistive state with physical semantics that persists without power and without polling."  
\- PUF identity vs manufacturing provenance: two distinct systems:  
  \- PUF: physical entropy generated post-manufacturing from device variation. Must not be factory-programmed. If foundry burns PUF values, system reduces to single-vendor trust \- this is a failure mode, state it explicitly.  
  \- Manufacturing provenance: foundry attests by signing PUF public key at wafer sort. Attestation database records fab date, node, wafer lot, die coordinates. Chain of custody from foundry to deployment.  
\- WCET: as defined in terminology hierarchy above.

\*\*Section 3.5 \- Mandate Authority Architecture\*\*

\- Governance parameters stored in write-once fuses: specify how many, what they encode, and who has authority to burn them.  
\- Vendor capture prevention: how is it cryptographically enforced that no single vendor can override the mandate post-deployment? Specify the mechanism.  
\- Policy update path: can the mandate evolve post-deployment without breaking the provenance chain? If yes, specify how. If no, state this as a design constraint.

\---

\*\*Section 4 \- Baseline: Binary CMOS Limitations\*\*

\- Logic levels, noise margins, switching energy at 3nm GAA node.  
\- Explicit assumptions: VDD \= 0.75V nominal, σVth \= 50mV, interconnect RC from IRDS.  
\- Why binary CMOS cannot natively enforce a mandatory intermediate state without software overhead.  
\- Direct quantified comparison to named baseline: TSMC N2 CoWoS with embedded ReRAM 1T1R, 2025 PDK. If MT does not show discontinuous advantage at this baseline layer, state this explicitly before proceeding.

\---

\*\*Section 5 \- Device Physics and Engineered State Requirements\*\*

\*5.1 Universal Memristive Mechanisms\*  
\- Filament formation/rupture, oxygen vacancy migration, interfacial redox.  
\- What "hysteresis" means physically and why it produces state retention.  
\- Why three states and not two or four: the engineering case for exactly three.  
\- Comparison to best 2025 binary NVRAM: where does the third state add value that binary multi-level cell does not already provide? If it does not, state this.

\*5.2 TaOx Deep-Dive (Primary Worked Example)\*  
\- Device stack: electrodes, oxide thickness range, switching layer. Must be sufficient for a foundry engineer to fabricate from this description alone.  
\- Switching mechanism in detail.  
\- Hysteresis characteristics: set/reset thresholds, window width, retention at 85°C and 125°C.  
\- IRS engineering: intermediate filament, partial reset, dual filament regime \- which is most robust and why.  
\- Endurance: cycle count required for logic use versus memory use.  
\- Thermal budget: maximum post-CMOS processing temperature (\<400°C), impact on filament stability, 3D stacking thermal profiles.  
\- 20-year retention projection: Arrhenius extrapolation with activation energy Ea \= 1.0-1.2 eV (typical for TaOx filament systems). Required: 10-year accelerated test data at 150°C minimum with \<10% resistance drift. Confidence interval: 95% lower bound must exceed 10-year specification. State extrapolation methodology and assumptions explicitly.

\*5.3 Comparative Device Table\*  
Minimum 8 rows: TaOx, HfOx, TiOx, PCM, MTJ, FeFET, and at least two others.  
Columns: retention, endurance, variability (σ/μ), write energy, read energy, operating voltage, integration maturity, CMOS compatibility, IRS credibility (yes/marginal/no with justification), quantified advantage over 2025 named baseline (or none).

\*5.4 TL State Mapping\*  
\- Define R-, R0, R+ resistance values with explicit sensing thresholds.  
\- Sense amplifier architecture: two reference cells (LRS and HRS), margining strategy for three-state discrimination.  
\- Noise sources: temperature, read disturb, cycle-to-cycle variability, random telegraph noise, stochastic filament dynamics.  
\- Distribution overlap implications for ternary reliability at 10^6, 10^9, and 10^12 read cycles.

\---

\*\*Section 6 \- Circuit Primitives and Sensing Margins\*\*

\- Native ternary logic gates: ternary inverter, NAND/NOR analogs, threshold logic.  
\- Sense amplifier sizing from noise margin analysis. A circuit designer must be able to size sense amplifiers from this section alone.  
\- ADC/DAC costs for analog state readout.  
\- Gate inflation factor: how many binary gates approximate a ternary primitive. Area and energy implications.  
\- Encoding strategies: 2-bit encoding, one-hot, signed magnitude, balanced ternary \- map each to physical resistive states and sensing thresholds.  
\- Non-blocking constraint verification: demonstrate all sensing and gate evaluation paths complete within WCET bounds. If any path introduces unbounded delay, flag explicitly and quantify.  
\- Quantified comparison to equivalent binary CMOS plus 2025 NVRAM baseline at each primitive level.

\---

\*\*Section 7 \- NL=NA: Physical Interlock Architecture\*\*

This is the core enforcement mechanism of TL instantiated in hardware. Treat with full engineering rigor.

\- Confirm pulse specification: voltage range (typically 1-3V for TaOx), pulse duration (10-100 ns), wire routing requirements.  
\- Confirm pulse verification circuit: window comparator with ±5% voltage tolerance, ±10% timing tolerance. Pulses outside window are rejected and flagged as tamper events. Window comparator powered from independent bandgap voltage reference, not VDD \- VDD compromise must not enable false confirmation.  
\- Spoof detection via RC signature: legitimate pulse rise time matches RC characteristics of confirm wire length. Tamper (added capacitance, wire tap) slows edge and falls outside timing window. Specify detection threshold.  
\- Interlock circuit: IRS is held until confirm pulse arrives from logging path. No software path can substitute. Logging path runs parallel to execution \- never serial \- satisfying non-blocking constraint.  
\- Dual-lane timing hard specification: execution lane WCET \<= 2 ms at 99.99th percentile. Logging lane hard ceiling: 300 ms maximum with jitter \<= 50 ms (σ/μ \< 10%). The 300-500 ms range is not acceptable as a specification \- collapse to single hard ceiling with jitter bound.  
\- Power loss behavior: cell retains IRS on power loss. Exact restart/recovery sequence required: log must be re-verified and confirm pulse re-issued before any state transition is permitted post-restart. Specify the verification protocol.  
\- Refuse (-1) hardware behavior: does HRS lock permanently? Is it resettable? Under what voltage conditions? What is the complete audit trail for a Refuse event?  
\- Multi-cell parallel execution: specify crossbar topology for parallel NL=NA enforcement when multiple execution requests arrive simultaneously.

\*\*Attack modeling \- required, not optional:\*\*  
\- Pulse spoofing: can false confirm pulse be injected within window comparator tolerance? What is the minimum attack energy required?  
\- Confirm wire shorting: behavior if wire shorted to ground or VDD. Is this detectable? What state does execution cell retain?  
\- Logging path failure: if logging path fails mid-write, what state does execution cell retain? Is this the safe failure mode?  
\- Read disturb exploitation: can repeated sub-threshold reads perturb IRS toward LRS without confirm pulse? Quantify disturb threshold.  
\- Analog fault injection: behavior under voltage glitching, electromagnetic pulse, temperature extremes beyond operating range.  
\- Degraded mode: specify exactly what system does when attack is detected. Fail-safe to HRS? Alert only? Log and continue? Justify the choice.

\---

\*\*Section 8 \- Hardware Root of Trust\*\*

\*8.1 PUF Identity\*  
\- Physical entropy source: post-manufacturing variation in filament nucleation sites, transistor thresholds, or dopant distribution. Must not be factory-programmed. If foundry burns PUF values, state this as single-vendor trust failure mode.  
\- PUF circuit architecture: which PUF type (SRAM, ring oscillator, memristive) is most compatible with MT integration and why.  
\- Uniqueness requirement: inter-die Hamming distance must exceed 49%. If below this threshold, PUF identity is unreliable \- state as kill condition.  
\- Reliability requirement: intra-die Hamming distance must be below 1% across temperature 0-125°C and voltage ±10%.  
\- How PUF key signs log entries: specify signing protocol.  
\- Tamper evidence: what physical attack on PUF is detectable and how.

\*8.2 Manufacturing Provenance\*  
\- Secure provisioning chain: foundry signs PUF public key at wafer sort. This is the attestation mechanism \- foundry does not burn identity values.  
\- Attestation database: records fab date, node, wafer lot, die coordinates, PUF public key signature. Specify what is recorded at wafer sort, die attach, and system integration.  
\- Chain of custody: how a log entry produced 20 years from now is traced to specific die, wafer lot, and foundry run.  
\- Foundry longevity: if foundry no longer exists, what escrow arrangement preserves the attestation chain? Specify minimum escrow requirements.

\*8.3 Trust Chain Integration\*

Complete chain \- a hostile reviewer must be able to trace any log entry from Merkle hash to PUF signature to foundry wafer lot:

\`\`\`  
PUF (post-manufacturing physical entropy, unique per die)  
    |  
    v  
Foundry Attestation (PUF public key signed at wafer sort)  
    |  
    v  
Hardware Identity (fab date, node, wafer lot, die coordinates)  
    |  
    v  
NL=NA Interlock (confirm pulse, window comparator verified)  
    |  
    v  
Immutable Log Entry (non-volatile write, IRS retained on power loss)  
    |  
    v  
Merkle Hash Chain (cryptographic integrity)  
    |  
    v  
TL Framework Attribution (ORCID: 0009-0006-5966-1243)  
\`\`\`

If any link in this chain cannot be completed within constraints of this section, state the break point explicitly. Do not proceed past a broken link without flagging it as a program-level risk.

\---

\*\*Section 9 \- Emulation Tax: Quantified Comparison\*\*

Compare three implementations:  
\- A) TL triadic states as software/state machines on binary CMOS.  
\- B) Native MT at circuit level.  
\- C) Hybrid: ternary state in memristors, binary compute for other operations.

Required artifact: worked numerical example showing cost of simulating Epistemic Hold in a decision pipeline versus native hardware execution. Use E \= αCV² per toggle plus memory access cost. State all assumed parameters explicitly. Provide best-case and worst-case bounds.

Required artifact: comparative table showing speed loss, energy loss, area overhead, latency penalty for each implementation versus named 2025 baseline.

Interconnect implications: on-chip network delay for NL=NA confirm pulse routing. Crossbar scaling limits. Wire energy versus compute energy as function of crossbar dimension. At what crossbar dimension does wire energy dominate and render MT unviable? State this threshold explicitly.

\---

\*\*Section 10 \- Falsifiability: Phase 1 Predictions and Failure Conditions\*\*

Minimum 10 testable predictions specific to device physics and circuit feasibility.

Minimum 10 failure conditions that terminate Phase 1 and prevent Phase 2 from proceeding. Examples:  
\- TaOx σ/μ \> 40%: IRS not reliably distinguishable from adjacent states at operating conditions.  
\- Retention at 85°C \< 10 years at 95% confidence lower bound.  
\- Confirm pulse tamper-evidence not achievable within BEOL thermal budget.  
\- PUF inter-die Hamming distance \< 49%: identity unreliable.  
\- No quantified discontinuous advantage over 2025 NVRAM baseline at any tested layer.  
\- WCET bounds cannot be proven at 99.99th percentile for any enforcement path.

\---

\*\*Section 11 \- Phase 1 Conclusion\*\*

Answer Phase 1 core question: pass or fail, layer by layer.

State explicitly: what Phase 2 may assume, what it may not, and what constraints it inherits. Phase 2 terminates any investigation path where Phase 1 concluded failure. No workarounds. State which system capabilities are foreclosed by Phase 1 constraints.

\---

\*\*Section 12 \- Bibliography\*\*

Label each citation: "high confidence" or "unverified recall."  
Primary sources only: IEEE, Nature, APL, IEDM, IRDS, foundry disclosures. No blogs.

\---

\*\*Section 13 \- Glossary\*\*

12-20 terms. Include all abbreviations: MT, TL, NL=NA, PUF, LRS, IRS, HRS, BEOL, GAA, CiM, ADC, DAC, NVRAM, ReRAM, PCM, MTJ, FeFET, WCET.

\---

\*\*Minimum Artifacts Required\*\*

\- Comparative device table with 2025 named baseline column (Section 5.3)  
\- Sensing margin analysis with reference cell architecture (Section 5.4)  
\- NL=NA interlock circuit diagram with window comparator and RC spoof detection in ASCII or pseudo-UML (Section 7\)  
\- Hardware Root of Trust chain diagram (Section 8.3)  
\- Emulation tax comparative table with 2025 baseline (Section 9\)  
\- Worked numerical example with best/worst bounds (Section 9\)

\---

\*\*Evaluation Criteria\*\*

Hostile but competent review committee:  
\- Every major claim supported by cited evidence or transparent calculation with stated assumptions.  
\- Explicitly state what would change your mind at each layer.  
\- Explain why MT is not analog compute rebranded \- where the advantage is discontinuous.  
\- Can a foundry engineer fabricate the TaOx stack from Section 5.2 alone?  
\- Can a circuit designer size sense amplifiers from Section 6 alone?  
\- Can a hostile reviewer trace a log entry from Merkle hash to PUF to foundry wafer lot?  
\- Does every enforcement mechanism satisfy WCET non-blocking constraint?  
\- Does every layer show quantified comparison to named 2025 baseline?  
\- Is the window comparator specification sufficient to prevent analog spoofing?

\---

\*"Build the third state into matter, and the future stops pretending it never hesitated." \- Lev Goukassian.\*

\---