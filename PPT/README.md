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

The conductor holds two threads — an execution thread and a logging thread. Neither may move until the conductor has received a signed authorization receipt. When the receipt arrives, the conductor walks both threads to the marker, releases the execution thread into provisional work, dispatches the logging thread down the Governance Lane to complete its anchoring — and instantly resets to accept the next authorization request.

The execution thread proceeds under State 1 (Provisional Execution). The logging thread completes its anchoring in Lane 2 at infrastructure speed — 300 to 500 milliseconds, operator-configured. If the Final Permission Token (FPT) arrives before the clock expires, the system transitions to State 2 (Final Confirmed Execution). If it does not, the hardware snaps the execution thread back to State 0 (Epistemic Hold) automatically. No software permission required. No coordinator contact required.

The conductor — the C-element — is already back at the gate, primed for the next cycle. It does not wait for Lane 2 to finish.

This is the **50-millisecond marker**: the point at which Lane 1 (hardware-owned) and Lane 2 (infrastructure-owned) become genuinely independent streams. It is what makes TL's authorization throughput independent of anchoring latency.

---

## The Three States

| State | Name | Condition | Execution Permitted |
|---|---|---|---|
| **0** | Epistemic Hold | Default. No valid PPT held. | No |
| **1** | Provisional Execution | Valid PPT issued. Clock running. | Yes — reversible |
| **2** | Final Confirmed Execution | Valid FPT arrived before expiry. | Yes — irreversible |

The system begins in State 0. It cannot leave State 0 without a valid PPT. It cannot reach State 2 without a valid FPT. If the clock expires before the FPT arrives, hardware returns to State 0 unconditionally.

These are not policy rules. They are circuit properties.

---

## The Hardware Pipeline

The PPT is produced by a four-stage hardware pipeline operating entirely within Lane 1:

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
      PPT Issued
      (< 50ms total, warm path)
```

The C-element is the only stage that is a physical constraint rather than a computation. Its output is held low by a pull-down network until both inputs — PPT validity and hardware authorization — are electrically high. This is not configurable. It is a consequence of CMOS physics.

---

## Two Implementation Tiers

Not every deployment context can host a physical FPGA/ASIC C-element. TL therefore defines two implementation tiers:

**Tier 1 — Full Hardware Constraint**  
FPGA/ASIC Muller C-element + FIPS 140-3 Level 3 HSM. Satisfies TL's hardware-constraint design intent completely. The authorization gate is physically enforced.

**Tier 2 — Software-Policy-on-Hardware (Weaker Instantiation)**  
TEE-based implementations (Apple Secure Enclave, ARM TrustZone, Intel SGX). Achieves TL's latency and cryptographic pipeline targets but the authorization gate is enforced by trusted software, not a physical circuit. Deployments in this tier must be labeled explicitly as a weaker instantiation.

---

## Directory Map

```
PPT/
│
├── README.md                          ← You are here
│
├── 01_Architecture_Specs/             ← What the PPT is and how it behaves
│   ├── PPT_Lifecycle.md               Minting → provisional release → FPT → State 2 or snapback
│   ├── C_Element_Rollback.md          Physical circuit collapse on provisionalExpiry
│   ├── Dual_Lane_Governance.md        Lane 1 autonomy; Lane 2 as independent anchoring stream
│   └── PPT_Token_Schema.md            Exact data structure of a minted PPT
│
├── 02_Hardware_Primitives/            ← The silicon that enforces the architecture
│   ├── C_Element_Interlock.v          Verilog RTL — the physical consensus gate
│   ├── Countdown_Timer_Clock.v        Hardware watchdog — fires provisionalExpiry on timeout
│   └── Volatile_Memory_Clear.v        Buffer invalidation on C-element output going low
│
├── 03_Cryptographic_Pipeline/         ← The four-stage token production pipeline
│   ├── SHA256_Hardware_Accel.v        HDL — dedicated SHA-256 hashing core
│   ├── Merkle_Precomputation.v        HDL — 16-parallel-core Merkle tree builder
│   └── HSM_Signing_Interface.md       Integration spec — HSM receive, sign, return
│
├── 04_Formal_Verification/            ← Mathematical proof of correctness
│   ├── PPT_State_Transitions.tla      TLA+ model — State 0/1/2, provisionalExpiry, invariants
│   ├── Rollback_Safety_Proofs.md      Deadlock freedom, liveness, safety — human-readable
│   └── Session-1.md                   Physical-layer feasibility research — Q1, Q2, Q7
│
├── 05_Research/                       ← The evidentiary foundation
│   ├── Session-2_Deep_Research.md     Deep research Q3–Q11 — full evidence base
│   ├── Governor_Independence_Note.md  50ms marker as Lane 1 autonomy — architectural note
│   ├── Governor_Independence_Prompt.md Research prompt for external deep research sessions
│   └── PPT_Governor_Independence_Domain_Analysis.md  Governor Independence domain analysis and failure mitigation (archived)
│
└── 06_Publication/                    ← Submission-ready outputs
    ├── PPT_Paper_Draft.md             Academic paper — TechRxiv/SSRN/Zenodo target
    └── PPT_Adversarial_Review.md      Three-reviewer adversarial challenge + revision plan
```

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

Cross-application of terminology between frameworks is a framework error.

---

## Quick Navigation

| If you want to... | Go to... |
|---|---|
| Understand the PPT conceptually | `01_Architecture_Specs/PPT_Lifecycle.md` |
| See the exact token data structure | `01_Architecture_Specs/PPT_Token_Schema.md` |
| Read the C-element circuit | `02_Hardware_Primitives/C_Element_Interlock.v` |
| Verify the latency claims | `Session-1.md` |
| Check the formal safety proofs | `04_Formal_Verification/Rollback_Safety_Proofs.md` |
| Read the full academic paper | `06_Publication/PPT_Paper_Draft.md` |
| See the peer review challenges | `06_Publication/PPT_Adversarial_Review.md` |

---

*Part of the Ternary Logic framework — FractonicMind/TernaryLogic*  
*For the companion framework governing moral decision-making, see FractonicMind/TernaryMoralLogic*
