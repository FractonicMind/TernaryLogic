# Provisional Permission Token (PPT)
### Ternary Logic — Dual-Lane Latency Architecture
**Author:** Lev Goukassian | FractonicMind  
**Framework:** Ternary Logic (TL) — published in *AI and Ethics*, Springer Nature  
**DOI:** 10.1007/s43681-026-01124-0  
**Repository:** FractonicMind/TernaryLogic

---

## What This Directory Contains

This directory is the complete technical specification, hardware implementation, cryptographic pipeline, formal verification, research evidence base, and publication package for the **Provisional Permission Token (PPT)** — the hardware-enforced authorization mechanism within Ternary Logic's Dual-Lane Latency Architecture (DLLA).

It is organized in six folders that follow the physical and logical progression of the token: from architectural concept down to silicon, then back up through formal proof and publication.

---

## Parent Specification

This directory is the hardware implementation layer of TL's Dual-Lane Latency Architecture. The constitutional specification — architectural principles, abstract hardware model, formal gap analysis, and the two-token PPT/FPT constitutional model — is maintained in the [`Dual_Latency_Architecture/`](https://github.com/FractonicMind/TernaryLogic/tree/main/Dual_Latency_Architecture) folder.

| Constitutional specification | Link |
|---|---|
| Architecture overview and Iron Law | [`Dual_Latency_Architecture/Readme.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Dual_Latency_Architecture/Readme.md) |
| Primary hardware specification | [`Hardware_Enforceable_Execution_Model_Specification.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Dual_Latency_Architecture/Hardware_Enforceable_Execution_Model_Specification.md) |
| PPT/FPT two-token constitutional model | [`DLLA_PPT_SPECIFICATION_ADDENDUM.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Dual_Latency_Architecture/DLLA_PPT_SPECIFICATION_ADDENDUM.md) |
| Engineering gap analysis | [`DLLA_ENGINEERING_GAPS_v1.md`](https://github.com/FractonicMind/TernaryLogic/blob/main/Dual_Latency_Architecture/DLLA_ENGINEERING_GAPS_v1.md) |

This PPT folder implements, extends, and in several cases resolves the gaps identified in those documents.


---

## The Problem This Solves

In every existing authorization system, the decision to permit execution is made by software — a policy engine, a trusted execution environment, a rule interpreter — running on hardware. This means the authorization guarantee is only as strong as the software enforcing it. Software can be exploited, patched, circumvented, or compromised.

TL's position is that for high-consequence operations — financial execution, medical device actuation, AI agent actions, autonomous vehicle commands — authorization should be a **physical constraint**, not a software policy.

The PPT is the mechanism that makes this concrete.

---

## The Core Invariant

> **No log. No action.**

The cryptographic proof that an action is authorized must physically exist before the action can physically proceed. This is not enforced by code. It is enforced by a circuit.

---

## How the PPT Works

Think of the PPT as a conductor at a 50-millisecond marker.

The conductor holds two threads — a computation thread and a logging thread. Neither may move until the conductor has received a signed authorization receipt. When the receipt arrives, the conductor walks both threads to the marker and executes a fork:

The **computation thread** enters provisional work under State 1. But not all work is equal. The Reversibility Boundary divides every action into two constitutional classes:

- **Class R — Reversible (Provisional Computation):** ALU operations, internal state changes, mathematical calculations. These execute freely. If the authorization is revoked, the C-element grounds the volatile buffer and they are destroyed. The world never saw them.

- **Class I — Irreversible (External Actuation):** Network transmissions, financial transfers, actuator commands, outbound signals. These are computed and staged in the **Shadow Buffer Gate** — a dedicated hardware component whose physical port stays **CLOSED**. They are prepared but not released.

The **logging thread** is dispatched down the Governance Lane at infrastructure speed — 300 to 500 milliseconds, operator-configured.

The conductor — the C-element — resets immediately and is ready for the next cycle. It does not wait for Lane 2 to finish. This is **Governor Independence**.

If the Final Permission Token (FPT) arrives before the clock expires, the system transitions to State 2. The State 2 output rail opens the Shadow Buffer Gate. Class I actions are released to the world. If the FPT does not arrive, the hardware snaps back to State 0 automatically. The volatile buffer is grounded. The shadow buffer is cleared. The physical port was never opened.

An adversary who suppresses FPT delivery gains nothing — only a localized waste of electricity.

---

## The Three States

| State | Name | Condition | Class R | Class I |
|---|---|---|---|---|
| **0** | Epistemic Hold | Default. No valid PPT. | Blocked | Blocked |
| **1** | Provisional Execution | Valid PPT. Clock running. | Executes freely | Staged — port CLOSED |
| **2** | Final Confirmed Execution | Valid FPT before expiry. | Committed | Released — port OPEN |

The system begins in State 0. It cannot leave State 0 without a valid PPT. It cannot reach State 2 without a valid FPT. The Shadow Buffer Gate opens exclusively on the State 2 output rail — not on the FPT directly. If the clock expires, hardware returns to State 0. The shadow buffer is cleared. The port was never opened.

These are not policy rules. They are circuit properties.

---

## The Hardware Pipeline

The PPT is produced by a four-stage hardware pipeline in under 50 milliseconds (warm path):

```
Request arrives
      │
      ▼
┌─────────────────────┐
│  SHA-256 Hash       │  ~1 μs    Hardware accelerator
│  (operation + nonce)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Merkle             │  ~16 μs   16 parallel SHA-256 cores
│  Pre-computation    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HSM Signing        │  ~5–10ms  FIPS 140-3 Level 3 certified
│                     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  C-Element          │  ~45 ps   Physical consensus gate
│  Convergence        │           No software override path
└──────────┬──────────┘
           │
           ▼
      PPT Issued — 50ms fork
           │
           ├──► Class R: executes in volatile registers
           └──► Class I: staged in Shadow Buffer Gate (port CLOSED)
```

At the 50ms fork, Lane 1 hardware resets immediately — Governor Independence. Multiple PPT cycles (30–100) can complete within a single Lane 2 anchoring window. Each PPT owns its shadow buffer instance — 8 staging slots, single-cycle wipe on `provisionalExpiry`. No routing tables. No CAM. Physics, not logic.

---

## The Two-Signal Chain

The Shadow Buffer Gate obeys State 2 — not the FPT directly. The chain of causality is:

```
FPT arrives → cryptographic validation → C-element achieves State 2
→ State 2 output rail goes HIGH → Shadow Buffer Gate enable pin asserted
→ Physical port OPENS → Class I payloads released to world
```

This two-signal chain ensures protocol agnosticism: if the FPT mechanism changes in the future (post-quantum cryptography, human-in-the-loop confirmation, new consensus ledger), the Shadow Buffer Gate requires no modification. It responds to State 2. How State 2 is achieved is the Governance Lane's constitutional responsibility.

---

## The Epoch Hold

The nonce counter is 64-bit. At one million PPTs per second, exhaustion occurs in approximately 584,000 years. Nonce exhaustion is not a practical threat.

However, formal verification requires a deterministic bound. The hardware implements an **Epoch Hold**: when the nonce counter reaches MAX_NONCE − 10,000, the hardware ceases minting PPTs and asserts a system-wide Epistemic Hold. A privileged **Epoch Reset FPT** — requiring Tri-Cameral quorum — rotates the signing keys, resets the counter to zero, and releases the hold. Nonce space and key material rotate together.

---

## Two Implementation Tiers

**Tier 1 — Full Hardware Constraint**
FPGA/ASIC Muller C-element + FIPS 140-3 Level 3 HSM + Shadow Buffer Gate. Satisfies TL's hardware-constraint design intent completely. The authorization gate and the release gate are both physically enforced.

**Tier 2 — Software-Policy-on-Hardware (Weaker Instantiation)**
TEE-based implementations (Apple Secure Enclave, ARM TrustZone, Intel SGX). Achieves TL's latency and cryptographic pipeline targets but authorization is enforced by trusted software, not a physical circuit. Deployments in this tier must be labeled explicitly as a weaker instantiation.

---

## Directory Map

```
PPT/
│
├── README.md                          ← You are here
│
├── 01_Architecture_Specs/             ← What the PPT is and how it behaves
│   ├── PPT_Lifecycle.md               Minting → Reversibility Boundary → fork → FPT → State 2 or snapback
│   ├── C_Element_Rollback.md          Physical circuit collapse; Shadow Buffer Gate clear on provisionalExpiry
│   ├── Dual_Lane_Governance.md        Governor Independence; FPT routing; Lane 1 autonomy
│   └── PPT_Token_Schema.md            Exact data structure of a minted PPT
│
├── 02_Hardware_Primitives/            ← The silicon that enforces the architecture
│   ├── C_Element_Interlock.v          Verilog RTL — the physical consensus gate (with TMR wrapper)
│   ├── Countdown_Timer_Clock.v        Hardware watchdog + Epoch Hold controller
│   ├── Volatile_Memory_Clear.v        Buffer invalidation on C-element output going low
│   └── Shadow_Buffer_Gate.v           Per-PPT Class I staging; State 2 rail opens physical port
│
├── 03_Cryptographic_Pipeline/         ← The four-stage token production pipeline
│   ├── SHA256_Hardware_Accel.v        HDL — dedicated SHA-256 hashing core
│   ├── Merkle_Precomputation.v        HDL — 16-parallel-core Merkle tree builder
│   └── HSM_Signing_Interface.md       Integration spec — HSM receive, sign, return; HA failover
│
├── 04_Formal_Verification/            ← Mathematical proof of correctness
│   ├── PPT_State_Transitions.tla      TLA+ model — State 0/1/2, provisionalExpiry, Epoch Hold, DAG resolution
│   ├── Rollback_Safety_Proofs.md      Deadlock freedom, liveness, safety — human-readable proofs
│   └── PPT_Physical_Layer_Feasibility.md  Physical-layer feasibility research — Q1, Q2, Q7
│
├── 05_Research/                       ← The evidentiary foundation
│   ├── PPT_Physical_Layer_Research.md       Parallel physical-layer evidence base
│   ├── PPT_Engineering_Assessment.md        Full engineering assessment — adversarial review
│   ├── PPT_Governor_Independence_Research.md Governor Independence — throughput, routing, failover
│   ├── Session-2_Deep_Research.md           Deep research Q3–Q11 — full evidence base
│   ├── Governor_Independence_Note.md         50ms marker — all 5 open questions resolved
│   ├── Governor_Independence_Prompt.md       Research prompt for external deep research sessions
│   └── PPT_Governor_Independence_Domain_Analysis.md  Domain analysis and failure mitigation (archived)
│
└── 06_Publication/                    ← Submission-ready outputs
    ├── PPT_Paper_Draft.md             Academic paper — TechRxiv/SSRN/Zenodo target
    └── PPT_Adversarial_Review.md      Three-reviewer adversarial challenge + revision plan
```

---

## Architecture Status

| Component | Status |
|---|---|
| C-element interlock | ✓ Specified — synthesizable RTL |
| Countdown timer + Epoch Hold | ✓ Specified — synthesizable RTL |
| Volatile memory clear | ✓ Specified — synthesizable RTL |
| Shadow Buffer Gate (per-PPT) | ✓ Specified — synthesizable RTL |
| SHA-256 hardware accelerator | ✓ Specified — synthesizable RTL |
| Merkle pre-computation (16-core) | ✓ Specified — synthesizable RTL |
| HSM signing interface | ✓ Specified — integration document |
| TLA+ formal model | ✓ Complete — safety proven by construction |
| Reversibility Boundary | ✓ Constitutional primitive — topology-enforced |
| Governor Independence | ✓ Architectural principle — fully specified |
| Epoch Hold | ✓ Formally bounded — deterministic recovery |
| DAG cycle resolution | ✓ Resolved — Governance Lane starvation |
| Open architectural questions | **0 remaining** |

**The DLLA is sealed and ready for formal simulation.**

---

## Evidence Standards

All claims in this directory are classified using TL's normative evidence taxonomy:

| Classification | Meaning |
|---|---|
| **[Demonstrated]** | Experimentally verified in published literature |
| **[Engineering Estimate]** | Derived from published component specifications |
| **[Theoretical]** | Consistent with known principles; not yet measured in silicon |
| **[Formal Proof]** | Established by theorem prover or model checker |
| **[Speculative]** | Plausible; not yet supported by published evidence |

No claim in this directory presents speculation as established fact or engineering estimates as demonstrated results.

---

## Terminology Note

TL and TML are distinct frameworks with non-interchangeable terminology.

- **Epistemic Hold** = TL's State 0. Do not substitute "Sacred Zero" — that belongs to TML.
- **Governance Lane** = TL's Lane 2. Do not substitute "Anchoring Lane" — that is TML's construct.
- **Inference Lane** = TL's Lane 1. Do not substitute "Authorization Lane" — incorrect terminology.

Cross-application of terminology between frameworks is a framework error.

---

## Quick Navigation

| If you want to... | Go to... |
|---|---|
| Understand the PPT conceptually | `01_Architecture_Specs/PPT_Lifecycle.md` |
| Understand the Reversibility Boundary | `01_Architecture_Specs/C_Element_Rollback.md` |
| See the exact token data structure | `01_Architecture_Specs/PPT_Token_Schema.md` |
| Read the C-element circuit | `02_Hardware_Primitives/C_Element_Interlock.v` |
| Read the Shadow Buffer Gate circuit | `02_Hardware_Primitives/Shadow_Buffer_Gate.v` |
| Understand Governor Independence | `05_Research/Governor_Independence_Note.md` |
| Verify the latency claims | `PPT_Physical_Layer_Feasibility.md` |
| Check the formal safety proofs | `04_Formal_Verification/Rollback_Safety_Proofs.md` |
| Read the full academic paper | `06_Publication/PPT_Paper_Draft.md` |
| See the peer review challenges | `06_Publication/PPT_Adversarial_Review.md` |

---

*Part of the Ternary Logic framework — FractonicMind/TernaryLogic*  
*For the companion framework governing moral decision-making, see FractonicMind/TernaryMoralLogic*
