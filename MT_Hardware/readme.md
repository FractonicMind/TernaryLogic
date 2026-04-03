# MT Hardware Architecture — Ternary Logic (TL)

**Author:** Lev Goukassian
**ORCID:** [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243)
**Framework:** Ternary Logic (TL) — Global Decision Systems Architecture
**Status:** Specification Complete

---

## Overview

This folder defines the hardware implementation of Mandated Ternary (MT) — the physical instantiation of the Ternary Logic (TL) triadic decision framework in silicon. MT is not a software architecture. It is the engineering of matter itself to enforce the three TL states as stable, non-volatile, hardware-mandated resistance conditions in memristive devices.

> **Core Guarantee:** The Epistemic Hold state (IRS) persists without power, without polling, and without software mediation. No software path can substitute for the physical confirm pulse required to release it. The hold is enforced by matter, not by code.

The architecture targets deterministic autonomous execution systems in industrial control, financial settlement finality, and critical infrastructure dispatch — contexts where "software said so" is no longer a sufficient audit statement.

---

## TL Triadic States — MT Hardware Mapping

| TL Semantic State | TL Symbol | MT Resistance State | Target Resistance |
|---|---|---|---|
| Proceed | +1 | Low Resistance State (LRS) | 1–10 kΩ |
| Epistemic Hold | 0 | Intermediate Resistance State (IRS) | 100 kΩ – 1 MΩ |
| Refuse | −1 | High Resistance State (HRS) | 1–10 MΩ |

---

## Device Architecture

![MT Triadic State Mapping](https://fractonicmind.github.io/TernaryLogic/MT_Hardware/Q-1.png)

Three physically distinct resistance states implemented in bilayer TaOx memristive 1T1R cells. The IRS is not an analog interpolation — it corresponds to a distinct topological filament configuration engineered via asymmetric oxygen vacancy distribution (TaOx⁻ sublayer x≈1.6 / TaOx⁺ sublayer x≈1.9).

![TaOx Device Stack](https://fractonicmind.github.io/TernaryLogic/MT_Hardware/Q-2.png)

The bilayer stack enables sequential switching: partial RESET ruptures only the TaOx⁺ filament segment (LRS → IRS), full RESET ruptures both segments (LRS → HRS). Each state corresponds to a distinct physical configuration, not a software label.

---

## Audio

🎧 [MT Hardware Architecture — Audio Overview](https://fractonicmind.github.io/TernaryLogic/MT_Hardware/Hardware_Implementation.mp3)

---

## Specification Documents

### Primary Specifications

| Document | Format |
|---|---|
| MT Device Physics and Circuit Primitives | [Markdown](https://github.com/FractonicMind/TernaryLogic/blob/main/MT_Hardware/MT_Device_Physics_and_Circuit_Primitives.md) |
| MT System Architecture and Economics | [Markdown](https://github.com/FractonicMind/TernaryLogic/blob/main/MT_Hardware/MT_System_Architecture_and_Economics.md) |

### Interactive Reference

| Document | Format |
|---|---|
| Hardware Implementation — Phase 1 | [HTML](https://fractonicmind.github.io/TernaryLogic/MT_Hardware/Hardware_Implementation.html) |

---

## Phase 1 Core Finding

TaOx bilayer memristive devices physically instantiate all three TL states with demonstrated 10-year retention at 85°C for LRS and HRS, and conditional 20-year retention for IRS pending production process corner validation. The discontinuous advantage over the binary CMOS baseline is specific and confined:

- **Non-volatile enforcement** of authorization-pending states without software polling
- **Power-loss persistence** of Epistemic Hold across power cycles without reinitialization
- **Hardware-enforced NL=NA** — No Log = No Action — the IRS cannot transition to LRS without a verified physical confirm pulse from the logging path

No discontinuous advantage is claimed at the binary logic switching layer. MT does not compete on speed or density. It competes on enforceability.

---

## Phase 2 Core Finding

Architecture B (hybrid memristive-CMOS) is the recommended implementation for the 2026–2027 commercialization window. Break-even requires approximately 6,700 enforcement chips per year across financial settlement and power grid verticals at a $15,000–$25,000 unit premium. IEC 61508 SIL 3 certification path is achievable by Q4 2027.

The minimum viable MT system: a 64-channel standalone enforcement IC on a mature process node, commercially available by Q2 2027.

---

## Key Constraints

- Crossbar arrays: ≤ 64×64 per hierarchical block (IR drop limit)
- Confirm wire length: ≤ 500 μm per window comparator instance
- Operating temperature: 0–125°C
- Execution lane WCET: ≤ 2 ms at 99.99th percentile
- Logging lane hard ceiling: 300 ms maximum, jitter ≤ 50 ms
- Post-write anneal: 200–250°C, 30 min (mandatory manufacturing step)

---

## Related TL Folders

- [Merkle Tree Architecture](https://github.com/FractonicMind/TernaryLogic/blob/main/Merkle_Architecture/readme.md)
- [No Log = No Action](https://github.com/FractonicMind/TernaryLogic/blob/main/No_Log-No_Action/readme.md)
- [No Spy = No Weapon](https://github.com/FractonicMind/TernaryLogic/blob/main/No_Spy-No_Weapon/readme.md)
- [Hardware Architecture — Published Papers](https://github.com/FractonicMind/TernaryLogic/tree/main/Hardware_Architecture)
- [Triadic Decision Pipelines](https://github.com/FractonicMind/Triadic_Decision_Pipelines)

---
