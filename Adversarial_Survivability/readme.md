# Constitutional Hardware

## "Ternary Logic" (TL) Framework — Hardware Specification Folder   

**Author:** Lev Goukassian   
**ORCID:** [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243)   
**Repository:** FractonicMind/TernaryLogic   
**License:** CC BY 4.0

---

## What This Folder Contains

This folder contains the hardware specification for **Mandated Ternary (MT)**: the physical implementation layer of the "Ternary Logic" (TL) governance framework. MT encodes constitutional governance constraints in the resistance states of tantalum oxide bilayer resistive RAM, implementing three physically discrete states -- Proceed (+1), Epistemic Hold (0), and Refuse (-1) -- at the hardware substrate.

The architecture operates as a sovereign governance coprocessor alongside binary processing systems without replacing them. The binary layer proposes. The ternary layer enforces. The execution gate does not open without a prior immutable audit record.

---

## The Core Argument

Every governance layer above hardware is administered by human intermediaries who can be pressured, replaced, or persuaded. The historical record -- from standards body capture to regulatory failure to corporate principle revision -- demonstrates that policy-layer governance yields under sufficient institutional pressure regardless of its nominal authority. Hardware does not negotiate. A tantalum oxide filament in the Intermediate Resistance State does not respond to threat, bribe, or administrative directive. The Epistemic Hold is a state of matter, not a policy position.

---

## Documents

### Primary Specifications

**[Mandated Ternary: A Hardware Architecture for Constitutional AI Governance -- TECHSPEC](https://github.com/FractonicMind/TernaryLogic/blob/main/Constitutional_Hardware/TL_Democratic_AI_Governance_TECHSPEC.md)**
Pure engineering specification. Abstract, architecture, physical substrate, failure modes, deployment roadmap. No inline citations -- the document is self-contained. Target audience: engineers, materials scientists, standards bodies, hardware design teams.
→ [View HTML](https://fractonicmind.github.io/TernaryLogic/Constitutional_Hardware/TL_Democratic_AI_Governance_TECHSPEC.html)

**[Mandated Ternary: A Hardware Architecture for Constitutional AI Governance -- MASTER](https://github.com/FractonicMind/TernaryLogic/blob/main/Constitutional_Hardware/TL_Democratic_AI_Governance_MASTER.md)**
Full document with 39 inline citations and complete reference list. Includes draft federal legislative language for a DITL certification mandate, and international treaty architecture (Wassenaar Arrangement, BIS export control). Target audience: policymakers, legislators, congressional staff, academic reviewers, legal scholars.
→ [View HTML](https://fractonicmind.github.io/TernaryLogic/Constitutional_Hardware/TL_Democratic_AI_Governance_MASTER.html)

### Engineering Gap Acknowledgment

**[Fabrication Gaps and Resolution Paths](https://github.com/FractonicMind/TernaryLogic/blob/main/Constitutional_Hardware/FABRICATION_GAPS_AND_RESOLUTION_PATHS.md)**
Formal acknowledgment of the three fabrication gaps the specification names itself: the TSMC N2 TaOx RRAM PDK does not yet exist, the 20-year IRS retention figure is a projection not a certification, and cycle endurance at N2 geometry has not been published. Each gap is assigned a resolution path, a trigger condition, and closure criteria. A specification that names its own limits is a specification that can be trusted.

### Companion Narrative

**[I Read Lev Goukassian's Document So You Don't Have To](https://github.com/FractonicMind/TernaryLogic/blob/main/Constitutional_Hardware/I_Read_Lev_Goukassians_Document_So_You_Dont_Have_To.md)**
Accessible narrative for general readers. Explains the constitutional hardware argument without requiring technical background.

### Audio

**[Hardwiring AI Safety into Ternary Logic](https://fractonicmind.github.io/TernaryLogic/Constitutional_Hardware/Hardwiring%20AI%20Safety%20into%20Ternary%20Logic.mp3)**
AI-generated deep-research audio companion.

---

## The Three States

| State | Integer | Physical Implementation | Constitutional Function |
|---|---|---|---|
| Proceed | +1 | LRS: ~1-10 kΩ, complete TaOx filament | Authorizes execution after verified audit completion |
| Epistemic Hold | 0 | IRS: ~100 kΩ-1 MΩ, partial filament (TaOx+ ruptured, TaOx- intact) | Mandates pause pending verified completion of required process |
| Refuse | -1 | HRS: ~1-10 MΩ, complete filament rupture | Denies execution; permanent by default |

The Epistemic Hold is not a timeout. It is not a software flag. It is a topologically distinct arrangement of oxygen vacancies at the atomic level in the bilayer substrate -- a physically discrete state of matter that no administrative directive can override.

---

## Key Hardware Parameters

| Parameter | Value |
|---|---|
| Substrate | TaOx bilayer RRAM, TSMC N2 CoWoS ReRAM 1T1R 2025 PDK |
| Inference Lane WCET | 2ms hard ceiling at 99.99th percentile |
| Governance Lane ceiling | 300ms / 50ms jitter maximum |
| Crossbar array maximum | 64x64 cells per hierarchical block |
| Confirm wire length maximum | 500 μm per window comparator instance |
| Operating temperature | 0-125°C |
| Post-write anneal | 200-250°C, 30 minutes (mandatory) |
| LRS / HRS retention at 85°C | >10 years (demonstrated) |
| IRS retention at 85°C | 20 years (projected -- see Fabrication Gaps) |
| IEC 61508 SIL 3 target | Q4 2027 |
| Recommended deployment | Architecture B (hybrid memristive-CMOS) |

---

## NL=NA: The Constitutional Invariant

**No Log = No Action**

Formally in Linear Temporal Logic: `G(execute implies P(escrow_recorded and auditable))`

Globally, every execution event was preceded by an escrow-recorded and auditable event. This formulation admits no exceptions. It is enforced simultaneously at five independent layers: schema, API contract, EIP-712 signing, on-chain ABI, and hardware substrate. Bypassing one layer does not bypass the others. The hardware layer is terminal.

---

## Published Framework

The companion governance framework -- Eight Pillars, Tri-Cameral Governance, API specification, and economic institution architecture -- is published in *AI and Ethics* (Springer Nature):

- DOI [10.1007/s43681-025-00910-6](https://doi.org/10.1007/s43681-025-00910-6) -- "Auditable AI: Tracing the Ethical History of a Model"
- DOI [10.1007/s43681-026-01124-0](https://doi.org/10.1007/s43681-026-01124-0) -- "A Ternary Logic Framework for Institutional Governance"

---

## Immutable Mandates

Three constitutional prohibitions beyond the authority of any governance body created by the TL framework:

- **No Spy** -- no function within a TL-governed system may enable surveillance of participants
- **No Weapon** -- the protocol and its implementation cannot be turned against any individual or group
- **No Switch Off** -- the TL protocol may evolve but cannot be extinguished

Any proposal attempting to modify, suspend, or reinterpret any Immutable Mandate is void from the beginning as if it had never been made.

---

*"There is no politics in the resistance value of a tantalum oxide filament. That absence is the entire design."*
-- Lev Goukassian
