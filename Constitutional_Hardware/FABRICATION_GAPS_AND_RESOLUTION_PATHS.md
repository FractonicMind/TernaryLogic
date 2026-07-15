# Fabrication Gaps and Resolution Paths

## **Engineering Honesty: What Must Be Built Before MT Can Be Production-Certified**

**Architect:** Lev Goukassian
**ORCID:** [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243)
**Repository:** FractonicMind/TernaryLogic
**Parent Specification:** [`TL_Democratic_AI_Governance_TECHSPEC.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Constitutional_Hardware/TL_Democratic_AI_Governance_TECHSPEC.md)
**Document Type:** Engineering Roadmap -- companion to the technical specification
**License:** CC BY 4.0

---

## Preamble

The Mandated Ternary (MT) technical specification names its own fabrication gaps explicitly. This document exists because named gaps deserve named resolution paths. It does not rewrite the specification. It stands beside it as a public engineering roadmap -- the commitment that the gaps will be closed, the criteria by which closure will be confirmed, and the sequence in which the work must proceed.

As the specification states: *"The claim that Delay-Insensitive Ternary Logic constitutional hardware is not yet buildable is false. The claim that it is trivially buildable tomorrow is also false. The fabrication roadmap is real. The capability exists. The production qualification work is incomplete in specific and nameable ways."*

This document names them.

---

## Gap 1: The TSMC N2 TaOx RRAM Process Design Kit Does Not Yet Exist

### What the Gap Is

The MT architecture targets the TSMC N2 CoWoS ReRAM 1T1R process node as its primary fabrication baseline. TSMC entered production volume ramp for the N2 node in 2025. The integration of embedded TaOx bilayer resistive RAM into the N2 process flow -- specifically the bilayer stoichiometry control required to produce the three physically discrete resistance states (LRS: 1-10 kΩ, IRS: 100 kΩ-1 MΩ, HRS: 1-10 MΩ) -- requires a dedicated process design kit (PDK) that does not currently exist as a production resource.

Standard CMOS PDKs at N2 include transistor and interconnect design rules. They do not include the specialized design rules, SPICE models, and process corner specifications required to implement RRAM cells with the controlled bilayer stoichiometry that the IRS state requires. Without the PDK, hardware teams cannot implement the full MT architecture at N2.

### What Exists Today

- TaOx bilayer RRAM at prior process nodes (28nm, 22nm) has been demonstrated in research settings with the three-state behavior documented in the specification
- Architecture B (hybrid memristive-CMOS) is deployable on a 2026-2027 timeline using existing CMOS nodes with embedded RRAM modules at earlier technology generations
- The N2 node itself is in production; the gap is the RRAM integration layer, not the base CMOS process

### Resolution Path

**Trigger:** Legislative or regulatory mandate creating procurement demand for DITL-certified hardware. The commercial rationale for TSMC or Intel Foundry to invest in PDK development requires a market signal of sufficient scale.

**Timeline from qualifying mandate:**
- Process design kit availability: 6 months from mandate
- First silicon: 12 months from mandate
- Production qualification: 24 months from mandate

**Interim path:** Architecture B deployment on existing CMOS nodes with embedded RRAM proceeds in parallel. Architecture B implements the constitutionally critical functions -- ternary state encoding, window comparator, NL=NA interlock -- in native TaOx RRAM cells while using binary CMOS for all other functions. Architecture B is the recommended deployment architecture pending N2 PDK availability.

**Closure criteria:** PDK released by TSMC or Intel Foundry that includes TaOx bilayer RRAM design rules, SPICE models, and process corner specifications sufficient to implement the three-state resistance encoding specified in the TECHSPEC. Confirmed by successful first silicon implementing the complete NL=NA interlock at N2 geometry.

---

## Gap 2: Full-Corner Arrhenius Validation of IRS Retention at N2 Has Not Been Performed

### What the Gap Is

The specification states that 20-year IRS retention at 85°C is a projection based on Arrhenius extrapolation from demonstrated TaOx oxygen vacancy diffusion kinetics -- not a production-certified specification. The projection becomes a specification when corner validation is complete.

Corner validation requires measuring IRS retention across the full process corner space: worst-case oxygen stoichiometry variations, worst-case anneal temperature deviations within the 200-250°C, 30-minute specification, and worst-case cycling history prior to retention measurement. Until this validation is complete, the 20-year figure is an engineering-honest projection, not a certified claim.

### Why This Gap Is Constitutionally Significant

The IRS state -- the Epistemic Hold -- is the constitutional innovation at the center of the architecture. An IRS state that degrades toward LRS under long-term operational stress is the most serious failure mode the system faces: drift toward permanent Proceed authorization. An IRS state that degrades toward HRS develops drift toward permanent refusal -- less dangerous but still a constitutional failure.

The specification states this without ambiguity: *"Production corner validation of IRS retention is a constitutional requirement."* This document affirms that statement. The 20-year projection is honest. The validation is not yet done. Both are true simultaneously.

### What Exists Today

- LRS and HRS retention at 85°C exceeds 10 years in available characterization data -- demonstrated, not projected
- IRS retention Arrhenius extrapolation is based on demonstrated oxygen vacancy diffusion kinetics in TaOx at accelerated aging temperatures -- the physics are sound, the corner validation is incomplete
- Majority-vote parallel cell array arbitration provides operational mitigation against single-cell drift while validation proceeds

### Resolution Path

**Trigger:** N2 PDK availability (Gap 1 resolution) enables corner validation at the target process node. Corner validation at prior nodes can proceed in parallel as supporting evidence.

**Validation program:**
1. Fabricate TaOx bilayer RRAM test structures at the target process node
2. Accelerated aging at multiple temperatures (125°C, 150°C, 175°C) to establish Arrhenius parameters at N2 geometry
3. Cycle the test structures through the full operational range before retention measurement (worst-case cycling history)
4. Measure retention across process corners: stoichiometry variation ±5%, anneal temperature ±10°C
5. Extrapolate to 85°C operational temperature using validated Arrhenius parameters
6. Confirm against the 20-year projection within engineering tolerance

**Closure criteria:** Published corner validation data confirming IRS retention exceeds 20 years at 85°C across the full process corner space, with worst-case cycling history applied prior to measurement. IEC 61508 SIL 3 certification by Q4 2027 is contingent on this closure.

---

## Gap 3: Cycle Endurance Characterization at N2 Geometry and Operating Conditions Has Not Been Published

### What the Gap Is

TaOx 1T1R cycle endurance has been demonstrated at 10^6 cycles in published characterization at prior process nodes, with optimized process engineering extending this to the 10^7 to 10^8 range. Cycle endurance specifically for TaOx 1T1R cells at N2 geometry and N2 operating conditions has not been published.

This matters for two failure modes addressed in the specification:

**Correlated memristor drift:** Extended operational cycling causes resistance values to drift as oxygen vacancy migration redistributes across the bilayer under repeated SET/RESET voltage stress. The drift rate at N2 geometry determines the required recalibration cycle frequency. Without N2 endurance data, the recalibration schedule cannot be specified precisely.

**Resistance boundary collapse:** Sustained write cycling narrows the resistance windows for all three states, compressing the IRS window specifically because it is bounded by two adjacent windows. The cycle count at which IRS window compression becomes operationally significant at N2 geometry is not yet characterized.

### What Exists Today

- Published endurance data at prior nodes (28nm, 22nm) provides the baseline characterization
- Majority-vote parallel cell array arbitration mitigates single-cell boundary collapse
- The specification correctly identifies the recalibration requirement: resistance window recalibration through the PUF-attested governance pathway at a frequency determined by observed drift magnitude per cycle

### Resolution Path

**Trigger:** N2 PDK availability (Gap 1 resolution) enables endurance characterization at the target geometry. Prior-node characterization proceeds in parallel as supporting evidence.

**Characterization program:**
1. Fabricate TaOx bilayer RRAM test structures at N2 geometry
2. Cycle test structures through SET/RESET sequences to 10^6, 10^7, and 10^8 cycles at N2 operating voltages and temperatures
3. Measure resistance window positions (LRS, IRS, HRS center values and bounds) at each cycle milestone
4. Characterize IRS window compression rate: how many nanometers of window margin are lost per decade of cycles?
5. Establish the recalibration cycle frequency required to maintain constitutional IRS window integrity across the operational lifetime
6. Publish characterization data

**Closure criteria:** Published cycle endurance characterization for TaOx 1T1R at N2 geometry confirming endurance at or above 10^7 cycles with characterized IRS window compression rate and specified recalibration frequency. Recalibration schedule incorporated into the MT certification requirements.

---

## The Four Vulnerability Classes: Current Mitigation Status

The technical specification addresses five physical failure modes. The critics have highlighted four vulnerability classes drawn from that analysis. This section states the current mitigation status for each, without claiming the gaps above are closed.

### Substrate Degradation and Drift

**Status:** Mitigation specified, production validation pending.

Majority-vote parallel cell array arbitration is the specified mitigation for both correlated drift and resistance boundary collapse. The mitigation is architecturally sound. Its quantitative effectiveness at N2 geometry depends on Gap 3 closure (cycle endurance characterization at N2). Until that data exists, the recalibration schedule is specified in principle but not in production-validated frequency.

**Constitutional behavior of drift:** The specification notes that initial drift toward the IRS boundary is constitutionally protective -- the system becomes more cautious, not less, as it ages into early drift. The constitutional risk emerges only if drift continues beyond the IRS boundary into the LRS (Proceed) window. The recalibration requirement exists to prevent this progression.

### Circuit-Level and Timing Vulnerabilities

**Status:** Fully specified. No fabrication gap required for closure.

Metastability: The specification states without qualification that unresolved metastability must default to Epistemic Hold or Refuse -- never Proceed. This is a physical design requirement that must be verified in SIL 3 certification. The requirement is clear. The verification is part of the Q4 2027 certification path.

RC spoof detection: The circuit is specified. It measures the time constant of the resistance transition as part of the validation sequence. A signal with correct steady-state resistance and incorrect transient response fails before the window comparator measurement completes.

500-micrometer confirm wire length: This is a physical design constraint, not a gap. It is a constitutional specification: the boundary within which the resistance measurement is accurate enough to enforce the three-state distinction. No fabrication gap exists here -- it is a layout requirement.

### Supply Chain Comparator Poisoning

**Status:** Partial mitigation specified. Residual risk acknowledged.

Cross-foundry redundant independent comparators provide the hardware mitigation. The specification honestly acknowledges the residual risk: a threshold shift designed to fall within fabrication tolerance limits and manifest only post-deployment cannot be detected by post-manufacturing attestation alone. The governance mitigation is Tri-Cameral Stewardship Custodian veto authority over certification decisions, including independent supply chain auditing as a constitutional requirement.

This is an honest residual risk. It is not a fatal flaw. It is the attack surface that the most sophisticated adversary -- foundry-level access with long-horizon planning -- could theoretically exploit. The layered mitigation (cross-foundry comparators, PUF attestation, Tri-Cameral certification oversight) raises the cost of this attack to nation-state level. No single-point attack exists.

### Fabrication Realism

**Status:** Three gaps named, resolution paths defined, closure criteria specified.

This document. See Gaps 1, 2, and 3 above.

---

## Summary Table

| Gap | Description | Current Status | Trigger for Resolution | Closure Criteria |
|---|---|---|---|---|
| Gap 1 | TSMC N2 TaOx RRAM PDK does not exist | Architecture B deployable now; N2 pending mandate | Legislative or regulatory mandate | PDK released; first silicon confirmed |
| Gap 2 | IRS retention 20-year figure is a projection | Arrhenius extrapolation sound; corner validation pending | Gap 1 (N2 PDK availability) | Published corner validation data; IEC 61508 SIL 3 certification |
| Gap 3 | Cycle endurance at N2 geometry not published | Prior-node data provides baseline; N2 pending | Gap 1 (N2 PDK availability) | Published N2 endurance characterization; recalibration schedule specified |

---

## What This Document Does Not Concede

**The three-state physics are sound.** The IRS as a topologically distinct filament configuration -- partial RESET rupturing the TaOx+ sublayer segment only while the TaOx- segment remains intact -- is not an engineered abstraction. It is a distinct state of matter at the atomic level. The Epistemic Hold is constitutionally real because it is physically real.

**Architecture B is deployable now.** The fabrication gaps apply to the N2 full-native implementation. The hybrid memristive-CMOS architecture (Architecture B) is deployable on a 2026-2027 timeline using existing process nodes. The constitutional functions -- window comparator, NL=NA interlock, three-state encoding -- are implementable today. The gaps are about production certification at the target node, not about whether the architecture works.

**The specification's engineering honesty is not a weakness.** A specification that names its own limits is a specification that can be trusted. The critics' observations largely confirm what the document already states. That confirmation is the correct response to engineering honesty -- not a rebuttal, but a reading.

---

## Authority

**Architect:** Lev Goukassian
**ORCID:** [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243)
**Parent Specification:** [`TL_Democratic_AI_Governance_TECHSPEC.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Constitutional_Hardware/TL_Democratic_AI_Governance_TECHSPEC.md)
**Adversarial Response (TML):** [`API/ADVERSARIAL_RESPONSE_v1.md`](https://github.com/FractonicMind/TernaryMoralLogic/blob/main/API/ADVERSARIAL_RESPONSE_v1.md)
**Certification Target:** IEC 61508 SIL 3 by Q4 2027

---

*"The fabrication roadmap is real. The capability exists. The production qualification work is incomplete in specific and nameable ways. The institutional mandate does not yet exist."*
-- Lev Goukassian, TL_Democratic_AI_Governance_TECHSPEC.md
