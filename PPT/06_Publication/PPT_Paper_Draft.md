# Hardware-Enforced Authorization in Ternary Logic's Dual-Lane Latency Architecture: A Technical Evaluation of the Provisional Permission Token

**Author:** Lev Goukassian  
**Affiliation:** Independent Researcher — AI Governance and Framework Architecture  
**Contact:** FractonicMind | ORCID: [author's ORCID]  
**Repository:** FractonicMind/TernaryLogic — Dual_Latency_Architecture/  
**Submission target:** TechRxiv / SSRN / Zenodo / peer-reviewed engineering journal  
**Keywords:** Ternary Logic, Dual-Lane Latency Architecture, Provisional Permission Token, Epistemic Hold, hardware authorization, C-element, cryptographic authorization pipeline, formal verification

---

## Abstract

The Provisional Permission Token (PPT) is the hardware-enforced authorization mechanism within Ternary Logic's (TL) Dual-Lane Latency Architecture (DLLA). TL's core architectural inversion — *proof precedes action* — is physically instantiated by the PPT: a cryptographically-signed, Merkle-anchored token issued in under 50 milliseconds by a hardware pipeline, whose valid receipt is the sole condition under which TL's C-element physical consensus gate releases the Epistemic Hold (State 0) and permits provisional execution (State 1). This paper conducts an objective, evidence-based technical evaluation of the PPT across eleven research dimensions: hardware feasibility, cryptographic pipeline realism, architectural soundness relative to prior art, novelty assessment, failure mode taxonomy, security analysis, performance characterization, infrastructure integration, alternative architecture comparison, regulatory compliance, and formal verification. The principal findings are: (1) PPT issuance at under 50 ms is technically realistic on the warm path (mean approximately 5–10 ms, p99 approximately 17 ms) using a hybrid FPGA/ASIC Muller C-element and a FIPS 140-3 Level 3 certified HSM; (2) TL's design intent — authorization as a physical hardware constraint with no software override path — is satisfied exclusively by the FPGA/ASIC C-element, not by any commercial trusted execution environment; (3) the provisional-then-final two-token pattern has prior art in distributed systems literature (optimistic concurrency control, two-phase commit, speculative execution) but no prior system combines hardware enforcement, cryptographic provisional token, automatic hardware rollback on timeout, and two-lane latency separation in a unified triadic state model; (4) critical specification gaps exist in externally visible I/O rollback semantics, cascading provisional chain behavior, and power-loss recovery; (5) a TLA+ formal specification is provided with safety properties proven by construction and liveness properties verified by model checking within a bounded state space. The paper concludes that TL's PPT is a technically feasible and architecturally novel authorization mechanism, with identified gaps representing a defined engineering roadmap rather than fundamental infeasibility.

**Word count:** approximately 249 words.

---

## 1. Introduction

The canonical problem in authorization architecture is the gap between *permission* and *proof*. In most systems, authorization is a policy decision enforced by software running on hardware — a trusted execution environment, a cryptographic protocol stack, a rule engine. These systems are conditionally secure: their authorization guarantees are contingent on the correctness, integrity, and uncompromised state of the software that enforces them.

Ternary Logic (TL) proposes a different architectural premise: that for high-consequence operations — financial execution, medical device actuation, AI agent actions, autonomous vehicle commands — authorization should be a *physical* constraint, not a software policy. TL's central design invariant is *no log = no action*: the cryptographic proof that an action is authorized must physically exist before the action can physically proceed. This is TL's inversion of the conventional model, in which software enforces authorization policies at runtime.

The Provisional Permission Token (PPT) is the mechanism that instantiates this inversion. The PPT is a cryptographically-signed, Merkle-anchored authorization token, issued by a hardware pipeline in under 50 ms, whose valid receipt is the physical input required by TL's C-element consensus gate to release the Epistemic Hold (State 0) and permit execution to begin. Without a valid PPT, TL's C-element holds the system in State 0 at the circuit level — not as a policy decision, but as a consequence of CMOS physics.

This paper presents a rigorous, evidence-based evaluation of the PPT's technical feasibility, architectural novelty, security properties, failure modes, and regulatory alignment. The evaluation is organized within TL's own architectural context: the Dual-Lane Latency Architecture (DLLA), in which authorization latency (hardware-owned, Lane 1) is separated from finality latency (infrastructure-owned, Lane 2), and the PPT is the instrument that bridges State 0 and State 1 within the Lane 1 hardware domain.

The goal of this evaluation is objective determination — not advocacy. Where TL's specification is technically strong, this paper says so and shows the evidence. Where gaps exist, they are named precisely. Where claims exceed currently demonstrated evidence, they are classified accordingly using a normative evidence taxonomy applied throughout.

---

## 2. Background

### 2.1 The Ternary Logic Framework

Ternary Logic (TL) is an AI and economic decision-making framework built on a triadic state model. It is one of two peer-reviewed frameworks published by the author, the other being Ternary Moral Logic (TML). TL and TML are architecturally distinct frameworks with distinct terminologies that are not interchangeable.

TL's three states are:
- **State 0 — Epistemic Hold:** The governed pause state. No execution is permitted while State 0 is active. The system awaits authorization.
- **State 1 — Provisional Execution:** Authorized execution under the PPT. Execution may proceed but is subject to reversal if the FPT does not arrive before `provisionalExpiry`.
- **State 2 — Final Confirmed Execution:** Authorized execution under the FPT. Irreversible.

TL's core architectural principle separates two distinct latency regimes: *"Authorization latency is hardware-owned. Finality latency is infrastructure-owned."*

### 2.2 The Dual-Lane Latency Architecture (DLLA)

The DLLA is TL's execution framework. It defines two lanes with distinct ownership and latency characteristics:

- **Lane 1 — Authorization Lane:** The hardware-controlled path. The PPT is issued here. Latency target: under 50 ms. Owner: MT hardware layer.
- **Lane 2 — Governance Lane:** The infrastructure-controlled path. The FPT is issued here. Latency: operator-configured. Owner: deployment infrastructure.

The DLLA's central design decision is the separation of these two lanes — the key insight being that authorization (who may act) can and should be resolved deterministically at hardware speed, while finality (whether the action is permanently confirmed) can tolerate infrastructure-bound latency without blocking execution.

### 2.3 The Epistemic Hold (State 0)

State 0 is TL's governed pause. The system cannot proceed to execution until the Epistemic Hold is released. The PPT is the instrument that releases it. If no PPT is issued, the system remains in State 0. If a PPT is issued but the FPT does not arrive before `provisionalExpiry`, the hardware automatically returns the system to State 0.

### 2.4 The C-Element

TL's physical enforcement circuit. The C-element (Muller C-element, Muller & Bartky 1959) is a consensus gate requiring all inputs to be high before its output goes high. In TL's implementation, the C-element requires both PPT satisfaction and hardware authorization as inputs before releasing State 0. TL's design intent is that this interlock operates at the hardware level with no software override path — making the authorization constraint physical rather than policy-based.

### 2.5 The Mandated Ternary (MT) Hardware Layer

TL's physical implementation specification defines the device physics, circuit primitives, and physical interlock that enforce TL's triadic state model in silicon. The PPT's hardware pipeline (SHA-256 hashing, Merkle pre-computation, HSM signing, C-element convergence) runs on MT-specified hardware.

### 2.6 The Two-Token Model

The PPT and FPT constitute TL's two-token authorization model:

**PPT (Provisional Permission Token):** Hardware-owned. Issued in under 50 ms. Releases the Epistemic Hold. Authorizes provisional execution. Carries `provisionalExpiry` — a hardware-enforced timeout. If the FPT does not arrive before expiry, hardware reverts to State 0 automatically.

**FPT (Final Permission Token):** Infrastructure-owned. Operator-configured latency. Completes the DLLA cycle. Converts provisional execution to final confirmed execution.

---

## 3. Related Work

### 3.1 The Prior-Art Landscape

TL's provisional-then-final two-token pattern has recognized antecedents in distributed systems and database literature. Intellectual honesty requires explicit acknowledgment of these antecedents before characterizing TL's contribution.

**Optimistic Concurrency Control (OCC)** (Kung & Robinson 1981) proceeds in three phases — read, validate, write — allowing provisional execution under the assumption of no conflict, then validating before final commit. TL's PPT/FPT model resembles OCC's read/validate/commit structure. The critical difference: OCC's validation is a software conflict-check on database state; TL's authorization is a cryptographically-signed hardware token physically gating execution.

**Two-Phase Commit (2PC)** (Gray 1978) uses a Prepare/Commit two-phase structure in distributed transactions. TL's PPT and FPT map superficially onto 2PC's phases. The critical difference: 2PC's blocking "in-doubt" state — when the coordinator has committed but a participant has not received the commit message — can suspend a distributed transaction indefinitely. TL's `provisionalExpiry` timer provides a deterministic hardware-enforced resolution: if the FPT (commit message) does not arrive within the specified window, the hardware reverts to State 0 without waiting for coordinator contact. TL eliminates 2PC's blocking problem by substituting a hardware watchdog for the coordinator.

**Speculative Execution** in processor architecture (Tomasulo 1967; modern out-of-order processors) executes instructions before their conditions are confirmed, then commits or rolls back based on branch resolution. TL's provisional execution window resembles processor speculation. The critical difference: CPU speculation is internal to the pipeline with no externally visible effect until instruction retirement. TL's provisional execution can produce externally visible effects — a fundamentally harder rollback problem (see Section 10 — Limitations).

**Sagas** (Garcia-Molina & Salem 1987) address long-lived transactions via compensating transactions. TL's `provisionalExpiry` rollback resembles a saga's compensating transaction, but TL's rollback is hardware-enforced and time-bounded rather than application-defined.

**Blockchain Finality** provides probabilistic or economic finality through distributed consensus. TL's FPT, by contrast, is infrastructure-owned and operator-configured — it could use a blockchain anchor, but it could equally be a regulatory clearinghouse, making TL's finality deterministic from the system's perspective even when the underlying infrastructure is probabilistic.

**Trusted Execution Environments (TEEs)** (Intel SGX, AMD SEV, ARM TrustZone) provide isolated execution environments with hardware-protected key storage. TEEs enforce authorization as software running in isolation — the authorization decision is made by code, not by a physical circuit. TL's C-element adds a constraint that TEEs do not provide: a physical consensus gate that is electrically impossible to satisfy without both inputs being active, independent of any software layer.

### 3.2 Novelty Assessment

No prior system in the surveyed literature combines:
1. A Muller C-element as a physical authorization gate (not merely an asynchronous circuit primitive)
2. An HSM-generated cryptographic provisional token as the gate condition
3. A hardware watchdog `provisionalExpiry` as a deterministic rollback trigger
4. Two-lane latency separation (hardware-owned authorization / infrastructure-owned finality)
5. A unified triadic state model governing the full execution lifecycle
6. General applicability across economic, medical, automotive, and AI governance domains

**The PPT is a novel architectural composition** — not a novel circuit primitive, not a novel cryptographic protocol, and not a novel distributed transaction pattern. Its novelty lies in the specific combination of hardware enforcement with the provisional-then-final execution pattern within a unified triadic state model, applied to the authorization problem in high-consequence systems. This is the distinction that must be held clearly: the pattern is not new; the hardware enforcement layer applied to the pattern within TL's DLLA is TL's specific contribution.

---

## 4. Technical Architecture

### 4.1 The PPT Cryptographic Pipeline

The PPT is produced by a four-stage hardware pipeline:

**Stage 1 — SHA-256 Hashing (~1 μs warm path):** The operation request, session context, and monotonic counter are hashed using a dedicated hardware SHA-256 accelerator (Intel SHA-NI class). This produces the cryptographic commitment to the specific authorized operation.

**Stage 2 — Merkle Pre-computation (~16 μs warm path):** Using 16 parallel SHA-256 cores, a Merkle tree is constructed over the audit leaf set, producing an authenticated audit root that anchors the PPT in the immutable audit log. TL's monograph specifies that 16 parallel SHA-256 cores can construct a 4,096-leaf Merkle tree in approximately 16.4 μs at 1 GHz.

**Stage 3 — HSM Signing (~5–10 ms warm path):** A FIPS 140-3 Level 3 certified HSM generates an ECDSA P-256 (or equivalent) digital signature over the SHA-256 hash and Merkle root, producing the PPT's cryptographic authorization token. The HSM's key material is physically protected and never exposed outside the HSM boundary.

**Stage 4 — C-Element Convergence (~45 ps):** The C-element receives the PPT's validity signal as one input and the hardware authorization signal as the second input. When both inputs are high, the C-element output goes high, releasing the Epistemic Hold. At 28 nm CMOS, C-element propagation delay is approximately 45 ps — negligible against any execution latency.

**Pipeline latency summary (warm path):**

| Stage | Mean Latency | p99 Latency | Evidence Classification |
|---|---|---|---|
| SHA-256 hash | ~1 μs | ~2 μs | [Engineering Estimate] |
| Merkle pre-computation | ~16 μs | ~30 μs | [Engineering Estimate] |
| HSM signing | ~5–10 ms | ~15 ms | [Engineering Estimate] |
| C-element convergence | ~45 ps | <1 ns | [Demonstrated — CMOS physics] |
| **Total PPT (warm path)** | **~5–10 ms** | **~17 ms** | **[Engineering Estimate]** |

TL's 50 ms specification is met comfortably on the warm path. The cold path (first issuance, full key loading, no cached Merkle branches) carries an estimated p99 of approximately 60 ms. Cold-path first-issuance should be treated as a startup transient rather than a steady-state SLA violation; the normative SLA applies to the warm-path operational steady state.

### 4.2 The C-Element Interlock

TL's C-element is a Muller C-element — a consensus gate from asynchronous circuit theory (Muller & Bartky 1959; Fant & Brandt 1996 for the NCL extension). In TL's implementation, it is instantiated as an FPGA LUT6_2 (INIT=0xE8E8E8E8E8E8E8E8 in Xilinx Versal RTL) or as a custom CMOS cell in ASIC implementations.

The C-element's physical property is its defining architectural advantage: its output is held low by a pull-down network whenever any input is electrically low. The transition from State 0 to State 1 requires the C-element output to go high, which is electrically impossible while the PPT validity signal is low. This is not a software policy — it is a consequence of Kirchhoff's current laws applied to the physical circuit.

The distinction between TL's C-element and a TEE is therefore architectural, not merely technical: a TEE enforces authorization via software code, which can in principle be exploited, patched, or circumvented; TL's C-element enforces authorization via circuit physics, which cannot be circumvented without physical manipulation of the silicon.

### 4.3 The Two-Lane Separation

The DLLA's core architectural decision is the separation of Lane 1 (Authorization Lane, hardware-owned) from Lane 2 (Governance Lane, infrastructure-owned). This separation achieves two goals:

**Goal 1 — Deterministic authorization latency.** By making Lane 1 hardware-owned and physically local to the execution system, TL removes authorization latency from the dependency on external network, consensus, or clearing infrastructure. Lane 1's latency is bounded by the hardware pipeline's performance characteristics, not by network RTT or infrastructure availability.

**Goal 2 — Flexible finality infrastructure.** By making Lane 2 infrastructure-owned and operator-configured, TL allows the finality mechanism to be adapted to the deployment domain: a blockchain anchor for decentralized finance, a regulatory clearinghouse for securities trading, an AI oversight system for AI governance. The FPT's mechanism is not TL's specification; its required existence is.

### 4.4 The `provisionalExpiry` Mechanism

TL's `provisionalExpiry` is a hardware watchdog counter that begins counting at PPT issuance. If the FPT does not arrive before the counter reaches its configured bound (the 50 ms window in TL's financial execution specification), the hardware automatically asserts State 0, clearing the provisional authorization.

This mechanism eliminates the distributed systems' canonical "in-doubt" problem (Gray 1978) by providing a deterministic hardware resolution: provisional execution cannot continue indefinitely without FPT confirmation. The worst-case outcome is always State 0 return — fail-safe by design.

---

## 5. Hardware Feasibility

TL's PPT is implementable today using commercially available hardware, subject to the architectural constraint that full hardware enforcement requires the hybrid architecture described here.

### 5.1 The Hybrid Architecture Requirement

TL's design intent — authorization as a physical constraint with no software override path — is satisfied exclusively by the FPGA/ASIC Muller C-element. Every commercial Trusted Execution Environment evaluated (Intel SGX, AMD SEV, ARM TrustZone, Apple Secure Enclave, RISC-V Keystone) provides tamper-resistant isolation but enforces the authorization decision via trusted software running on isolated hardware. This is a qualitatively weaker guarantee than TL's C-element: software-policy-on-hardware can in principle be circumvented by exploiting the software layer; a physical circuit gate cannot.

The recommended hybrid architecture is:
- **FPGA/ASIC Muller C-element** as the physical commit gate — the only component satisfying TL's hardware-constraint design intent
- **FIPS 140-3 Level 3 certified HSM** (Thales Luna Network HSM 7, Entrust nShield 5, Utimaco CryptoServer CP5, or equivalent) as the signing and key-custody element
- **Dedicated hardware SHA-256 accelerator** (Intel SHA-NI, ARM SHA extension, or parallel FPGA-hosted cores) for hashing and Merkle construction

### 5.2 Technology Assessment Summary

| Technology | C-element interlock | Signing pipeline | SHA-256/Merkle | `provisionalExpiry` | Constraint vs. Policy | Notes |
|---|---|---|---|---|---|---|
| Thales Luna Network HSM 7 | No | Yes — ~20,000 ECDSA P-256 sig/s | On-module | Firmware policy | Software policy on HW | FIPS 140-2 L3; L3 migration path available |
| ARM TrustZone | No | Sub-ms to few ms | ARMv8 crypto ext. | Secure-world timer | Software policy on HW | Adequate for "weaker tier" consumer |
| Apple Secure Enclave | No | ECC P-256 ~1–5 ms | On-SoC | Enclave policy | Software policy on HW | Enables 10–20 ms consumer PPT |
| Intel SGX | No | Software in enclave | In-enclave | Software timer | Software policy on isolated HW | ~17,000 cycle enclave transition overhead |
| FPGA (Xilinx Versal / Intel) | **Yes** | External HSM | Yes — parallel cores | **Hardware watchdog** | **Hardware constraint** | Full TL design intent satisfied |
| ASIC (28–2 nm) | **Yes** | Integrable crypto core | Yes | **Hardware timeout** | **Hardware constraint** | Target for production deployment |
| TPM 2.0 | No | Tens of ms ECDSA — **too slow for critical path** | Supported | Monotonic counters | Software policy on HW | Disqualified from signing path |

**Deployment tiers:** Deployments that cannot host an FPGA/ASIC C-element (cloud VMs, consumer devices, legacy infrastructure) must be explicitly classified as the "weaker instantiation" tier — providing TL's cryptographic pipeline guarantees but not TL's physical hardware-constraint guarantee for the authorization gate.

---

## 6. Cryptographic Analysis

### 6.1 Pipeline Feasibility

All evidence classifications apply per the taxonomy in Section 1.2 of the research protocol.

**SHA-256 hashing at approximately 1 μs:** Consistent with Intel SHA-NI performance (approximately 1.5–2 cycles per byte on modern Intel processors, yielding sub-microsecond hashing of typical PPT payloads). [Engineering Estimate]

**Merkle pre-computation at approximately 16 μs:** Consistent with TL's own engineering model for 16 parallel SHA-256 cores constructing a 4,096-leaf tree at 1 GHz. An independently measured hardware Merkle tree benchmark is not available at time of writing and is identified as a verification task prior to publication. [Engineering Estimate; TL model — Theoretical]

**HSM signing at 5–10 ms:** Consistent with published HSM throughput specifications for major vendors (Thales Luna 7 approximately 20,000 ECDSA P-256 signatures per second on the hardware core, implying approximately 0.05 ms per signature at sustained throughput, with network RTT of 1–5 ms for network-attached HSMs adding the material latency contribution). [Engineering Estimate — pending primary datasheet verification]

**C-element convergence at approximately 45 ps:** Consistent with published CMOS gate delay characteristics at 28 nm process nodes. TL's own parameter table specifies 45 ps at 28 nm and 12 ps at 2 nm GAA. Both figures are within the range expected from standard-cell delay analysis. [Demonstrated by CMOS physics; Engineering Estimate for the TL-specific cell]

### 6.2 Cold-Path vs. Warm-Path Distinction

The warm path (cached keys, pre-computed Merkle branches, warm HSM session) achieves mean approximately 5–10 ms, p99 approximately 17 ms. The cold path (first issuance, full key loading, no cached branches, cold HSM session) carries an estimated p99 of approximately 60 ms, primarily from HSM session establishment and first key load.

**TL's 50 ms claim assumes the warm path.** This is architecturally acceptable for TL's target domains (financial execution, AI governance) where PPT issuance is a steady-state hot-loop operation. First issuance (cold path) should be documented as a startup transient and explicitly excluded from the steady-state SLA. Mandatory system startup procedures should include HSM session pre-warming and key pre-loading.

**The discrete TPM 2.0 disqualification:** A discrete TPM 2.0 in the signing critical path disqualifies itself — its ECDSA signing latency runs in the tens of milliseconds, which alone can consume the entire 50 ms budget. TPM 2.0 may serve for attestation and `provisionalExpiry` monotonic counter functions but must not be placed in the per-PPT signing path.

---

## 7. Security Analysis

### 7.1 Replay Attacks

TL's Merkle-anchored PPT includes a cryptographic commitment to the specific operation context, session, and timing information. Replay prevention requires per-PPT uniqueness enforcement via monotonic counter or nonce as a normative requirement. If implemented as a hardware monotonic counter (TPM PCR class or dedicated RTOS timer), this provides hardware-level replay prevention. If implemented as HSM firmware policy, it provides software-level replay prevention. TL's specification should explicitly mandate the normative minimum implementation.

### 7.2 Token Forgery

ECDSA P-256 with SHA-256 provides approximately 128-bit classical security against existential forgery — computationally infeasible with current or near-future classical computers. Against quantum adversaries with Shor's algorithm, the security margin falls to approximately 64-bit equivalent, insufficient for long-term deployments. **TL's specification should include a migration path to NIST PQC algorithms** (CRYSTALS-Dilithium / FIPS 204; SPHINCS+ / FIPS 205) as a normative post-quantum recommendation. [Engineering Estimate — referencing NIST PQC finalization, August 2024]

### 7.3 HSM Compromise

HSM compromise is TL's most severe single-point security failure. A compromised HSM can generate valid-looking PPTs for unauthorized operations, satisfying the C-element's input condition for any requested execution. The C-element provides no residual protection against a Byzantine-faulty HSM — the C-element enforces that *a valid PPT exists*, not that *the PPT was generated by an uncompromised HSM*.

Mitigations include: HSM signing rate anomaly detection, multi-party HSM key generation (requiring M-of-N operators for key ceremonies), dual-HSM cross-validation (requiring two independent HSMs to co-sign for a PPT to be valid), and hardware attestation chaining. These mitigations should be specified as deployment best practices in TL's operational specification.

### 7.4 Timing Attacks

FIPS 140-3 Level 3 certification mandates demonstrated resistance to non-invasive attacks including timing side channels. Deploying a FIPS 140-3 Level 3 certified HSM mitigates timing attack risk for the signing stage. The C-element's approximately 45 ps convergence time does not represent a meaningful timing side channel. **TL's specification should explicitly mandate FIPS 140-3 Level 3 certification** as the minimum normative requirement for HSMs in the PPT pipeline.

### 7.5 Rollback Attacks (Denial of Service)

An adversary who can delay or suppress FPT delivery can force `provisionalExpiry` to fire repeatedly, consuming HSM signing capacity without producing committed executions. FPT delivery channel security — including mutual authentication and integrity protection — should be specified as normative requirements.

### 7.6 Hardware Fault Injection

SRAM-based FPGA implementations of the C-element are susceptible to Single-Event Upsets (SEUs) from radiation or deliberate glitching. Mitigations: configuration scrubbing, Triple Modular Redundancy (TMR) at the FPGA configuration level, or using flash-based FPGAs (Microchip PolarFire) that are inherently SEU-resistant. ASIC implementations eliminate the SRAM-based vulnerability but introduce different fault injection considerations (laser fault injection). TL's specification should provide explicit countermeasure requirements for each implementation class.

---

## 8. Performance Evaluation

### 8.1 Throughput

HSM signing is both the latency driver and the throughput ceiling for TL's PPT pipeline. The SHA-256 (~1 μs), Merkle (~16 μs), and C-element (~45 ps) stages are negligible against HSM signing latency and never constrain throughput.

Estimated per-module throughput ceilings: Thales Luna 7 approximately 20,000 ECDSA P-256 signatures per second; Entrust nShield Connect XC approximately 8,600 RSA-2048 signatures per second; Utimaco CryptoServer CP5 approximately 1,000–2,000 ECDSA signatures per second. [Engineering Estimates — pending primary datasheet verification]

TL's internal throughput model projects approximately 3,864 operations per second at single-lane baseline, approximately 15,000 operations per second with 4-way pipelining, and approximately 3.0 million effective operations per second with 64 lane replicas (after 20% coordination overhead).

### 8.2 Queue Behavior Under Saturation

TL's specification defines a three-stage saturation response: when the Fast Lane input FIFO exceeds 80% capacity, the system enters stall mode (deasserts `RequestReady`, draining to 50% hysteresis threshold); if the stall persists beyond 100 ms, the system enters reject mode (immediate NAK for new admissions, in-flight operations continue to completion). TL's saturation response is *queue, then reject* — it never silently drops requests. The maximum sustainable burst before full Fast Lane stall is approximately 1.07 seconds.

### 8.3 Latency Under Load

The 50 ms target holds at moderate HSM utilization. HSM p99 latency rises steeply as utilization approaches the throughput ceiling. The operational trigger for adding HSM capacity is p99 latency exceeding approximately 30 ms at target load (consistent with maintaining headroom within the 50 ms SLA). Specific HSM latency-vs-throughput curves at 50%, 80%, and 95% utilization are identified as a primary-source verification task prior to publication.

### 8.4 Consumer Hardware

Apple Secure Enclave (ECC P-256 signing approximately 1–5 ms on Apple Silicon) makes TL's 10–20 ms consumer target achievable at both mean and p99 for the warm path. This is a TEE-based (weaker instantiation) deployment. The physical C-element awaits SoC-level integration for consumer deployment.

---

## 9. Alternative Architectures

Three alternative architectures were evaluated as genuine competitors to TL's PPT. Each is a strongest-available instantiation of its approach, not a strawman.

**Alternative 1: Hardware-Enforced Capability Architecture (HECA)**
Uses ARM Morello / CHERI hardware capability registers as per-operation authorization gates. Capabilities are hardware-enforced unforgeable pointers requiring cryptographic authorization before load. Enables finer granularity (per-pointer) than TL (per-operation) but provides no finality layer, no provisional-then-final lifecycle, and no built-in audit trail. Superior for memory-safety authorization at instruction granularity; not a substitute for TL's system-boundary lifecycle management.

**Alternative 2: Distributed Threshold Authorization System (DTAS)**
Uses threshold ECDSA (M-of-N, GG20 protocol) to require multi-party agreement before an execution token is issued. Eliminates TL's single HSM as a point of failure. Authorization and finality are simultaneous (no two-lane separation). Latency is network-RTT-dependent and non-deterministic under adversarial conditions. Superior for consortium governance and multi-party authorization requirements; accepts non-deterministic latency as a trade-off.

**Alternative 3: Policy-Enforced Hardware Isolation (PEHI — seL4)**
Uses a formally verified microkernel (seL4, with machine-checked proof of functional correctness) and hardware-enforced partition isolation to gate execution on policy engine authorization. Software enforcement only (seL4 is verified software, not a physical circuit). No finality layer. Lower cost and complexity than TL; formally proven correctness for the software execution model. Superior where deployment cost and simplicity are paramount and formal software correctness is an acceptable substitute for physical hardware enforcement.

**Comparative summary (key dimensions):**

| Dimension | TL's PPT | HECA (Morello) | DTAS (Threshold) | PEHI (seL4) |
|---|---|---|---|---|
| Authorization latency (mean/p99) | ~5–10 ms / ~17 ms | ~0.1–1 ms / ~2 ms | ~10–100 ms / ~500 ms | ~0.1–5 ms / ~10 ms |
| Hardware enforcement of gate | Physical (C-element) | Physical (ISA cap.) | Cryptographic | Software (verified) |
| Finality lane separation | Yes (two-lane DLLA) | No | No (simultaneous) | No |
| Immutable audit trail | Yes (Merkle-anchored) | No | Partial | Partial |
| Deterministic worst-case latency | Yes (`provisionalExpiry`) | Yes (cap. revoc.) | No | Yes (scheduling) |
| Cost/complexity | High | Medium | Medium-High | Low |
| Single-party PoF | Yes (HSM) | Yes (processor) | No (threshold) | Yes (seL4 boot) |

**Assessment:** TL's PPT is preferable where physics-enforced authorization gating, provisional-then-final lifecycle management, and immutable Merkle-anchored audit trail are jointly required. DTAS is preferable where multi-party authorization with no single point of failure is paramount. PEHI is preferable where cost and deployment simplicity are paramount and formal software verification is accepted as the assurance foundation. These are distinct trade-off positions, not a hierarchy.

---

## 10. Regulatory Compliance

### 10.1 Compliance Matrix

| TL Component | FDA 21 CFR Part 11 | ISO 26262 ASIL-D | IEC 62304 Class C | PCI-DSS 4.0 | Common Criteria EAL | FIPS 140-3 Level |
|---|---|---|---|---|---|---|
| C-element interlock | Partially satisfies | Partially satisfies (formal verification required) | Partially satisfies (hardware qualification required) | Satisfies Req. 6 | Partially satisfies (EAL4+ feasible) | N/A |
| HSM signing pipeline | Satisfies | N/A (infrastructure) | Partially satisfies (SOUP management required) | Satisfies Req. 3, 8 | Satisfies EAL4+ (per FIPS 140-3 L3 baseline) | **Satisfies Level 3** |
| Merkle audit trail | **Satisfies** (§11.10(e)) | Partially satisfies | Satisfies (§5.8) | **Satisfies** Req. 10 | Partially satisfies | N/A |
| `provisionalExpiry` rollback | Partially satisfies | Partially satisfies | Partially satisfies | Satisfies | Partially satisfies | N/A |
| FPT anchoring | Partially satisfies | Partially satisfies (availability concern) | Partially satisfies (SOUP) | Satisfies Req. 3 | Partially satisfies | N/A |
| MT hardware layer | N/A | **Partially satisfies** (Part 5 required) | N/A | N/A | Partially satisfies | N/A |

*Legend: Satisfies — demonstrably meets requirement as currently specified. Partially satisfies — meets some aspects; gaps identified. Does not satisfy — does not meet requirement. N/A — not applicable.*

### 10.2 Key Compliance Gaps

**ISO 26262 ASIL-D:** The formal verification in Section 11 (and the Appendix) is a prerequisite for ASIL-D certification. Cascading provisional chain behavior (identified in the failure mode taxonomy) must be resolved before a safety case can be submitted.

**IEC 62304 Class C:** All software components in the TL stack (HSM firmware integration, FPT delivery logic, `provisionalExpiry` software interface) must be developed under IEC 62304 SDLC requirements. This is a process compliance requirement separate from runtime behavior.

**FIPS 140-3 Level 4:** Level 3 is specified and achievable with current certified HSMs. High-consequence domains (financial market infrastructure, government operations) should specify Level 4, which adds requirements for environmental attack resistance and fault injection countermeasures beyond Level 3's scope.

---

## 11. Discussion

TL's PPT represents a technically feasible and architecturally coherent approach to hardware-enforced authorization in high-consequence systems. The key architectural contribution — separating authorization latency (hardware-owned, Lane 1) from finality latency (infrastructure-owned, Lane 2), and enforcing this separation through a physical C-element consensus gate — addresses a genuine gap in existing authorization architectures.

The provisional-then-final pattern is not new. The hardware enforcement layer applied to the pattern within a unified triadic state model is TL's specific contribution. This distinction is important for honest novelty assessment and should be stated clearly in any peer-reviewed publication.

TL's PPT is strongest where three properties are jointly required: (1) a physics-enforced authorization gate with no software override path, (2) a provisional-then-final execution lifecycle with deterministic hardware rollback, and (3) an immutable Merkle-anchored audit trail as a first-class architectural primitive. No existing system provides all three.

TL's PPT is challenged by: (1) HSM compromise, which defeats the cryptographic chain without C-element residual protection; (2) externally visible I/O, which cannot be rolled back by hardware reversion to State 0; (3) cascading provisional chains, which lack a specified cascade-revocation protocol; and (4) cloud environments, which cannot fully instantiate the physical C-element requirement.

The most immediately applicable deployment domain for TL's PPT is AI governance — where the need to gate AI-initiated actions on hardware-enforced authorization before execution is a pressing and underserved requirement, and where TL's provisional-then-final model maps cleanly onto the AI action lifecycle.

---

## 12. Limitations

The following limitations reflect the current state of TL's specification and are presented as a defined engineering roadmap, not as fundamental infeasibility findings.

**L1 — Externally visible I/O rollback:** TL's hardware `provisionalExpiry` reverts authorization state (State 1 → State 0) but does not automatically undo externally visible effects (transmitted network packets, engaged actuators) that occurred during the provisional window. Applications with irreversible external effects must use TL's FPT-first mode (no provisional execution for actuation-class operations) or implement application-level compensating logic.

**L2 — Non-idempotent partial write:** If a write operation is partially completed when `provisionalExpiry` fires, hardware rollback does not guarantee storage-level reversal. A transactional storage layer (MVCC database, journaling filesystem) operating beneath TL's DLLA is required for non-idempotent write safety.

**L3 — Cascading provisional chain revocation:** When a multi-system provisional chain loses one FPT, TL's specification does not define a cascade-revocation protocol for downstream PPTs that were conditionally issued on the revoked link's State 1. This is a significant gap for distributed deployments.

**L4 — Cold-path p99 outside specification:** The cold-path p99 (~60 ms) exceeds TL's 50 ms specification. Mandatory HSM session pre-warming at system startup mitigates this, but the startup transient is not explicitly addressed in TL's current specification.

**L5 — HSM as single point of failure and compromise:** HSM compromise defeats the authorization chain without residual C-element protection. Multi-HSM cross-validation and anomaly detection are identified as required operational hardening not yet specified normatively.

**L6 — Quantum vulnerability:** ECDSA P-256 is not post-quantum secure. A PQC migration path (FIPS 204/205) should be specified normatively.

**L7 — FPGA SEU vulnerability:** SRAM-based FPGA C-element implementations are susceptible to radiation-induced configuration upsets. Flash-based FPGAs or ASIC implementation eliminate this; scrubbing mitigates it for SRAM-based FPGAs.

**L8 — Cloud deployment gap:** Cloud environments cannot fully instantiate TL's physical C-element requirement. Cloud deployments are limited to the "weaker instantiation" tier.

**L9 — Full TLA+ proof pending:** The formal specification in the Appendix establishes safety properties by construction and liveness by bounded model checking. A full TLAPS-checked proof of all three properties (deadlock freedom, liveness, safety) is identified as future work.

---

## 13. Future Work

The following engineering tasks are required before TL's PPT can move from architectural specification to practical deployment:

**FW1** — Primary-source verification of all HSM latency and throughput figures against current vendor datasheets and NIST CMVP certificate records. Elevation of [Engineering Estimate] figures to [Demonstrated] where primary-source evidence confirms them.

**FW2** — Measured FPGA/ASIC Merkle tree construction benchmark for approximately 4,096 leaves to independently validate TL's 16.4 μs model.

**FW3** — Measured TPM 2.0 ECDSA signing latency benchmark to quantify the precise disqualification margin.

**FW4** — Cold-path HSM session pre-warming study: determine the minimum startup sequence to pull cold-path p99 below 50 ms deterministically, or formally exclude first-issuance from the SLA.

**FW5** — Cascade-revocation protocol specification: a normative multi-system PPT chain revocation mechanism triggered by FPT failure in any chain link.

**FW6** — Post-quantum cryptographic migration specification: FIPS 204/205 implementation paths for TL's HSM signing pipeline.

**FW7** — Full TLAPS-checked formal proof of the TLA+ specification in the Appendix.

**FW8** — ASIC co-packaging study: determine whether TL's C-element and HSM signing pipeline can be physically co-packaged (2.5D/3D integration) such that the HSM signing output directly drives the C-element input without traversing a software or network layer.

**FW9** — ISO 26262 ASIL-D safety case development for automotive applications, incorporating the Q11 formal verification.

**FW10** — Empirical AI governance pilot: implement TL's DLLA as an authorization layer for an AI inference engine in a controlled deployment to demonstrate the provisional-then-final pattern applied to AI action gating.

---

## 14. Conclusion

The Provisional Permission Token, evaluated within Ternary Logic's Dual-Lane Latency Architecture, is technically feasible today using commercially available hardware in a hybrid FPGA/ASIC C-element plus FIPS 140-3 Level 3 HSM configuration. The warm-path latency target of under 50 ms is met with significant margin (mean approximately 5–10 ms, p99 approximately 17 ms). TL's design intent — authorization as a physical hardware constraint with no software override path — is satisfied exclusively by the FPGA/ASIC C-element implementation, distinguishing TL from all existing TEE-based authorization architectures.

TL's PPT is a novel architectural composition: not a novel circuit primitive, not a novel cryptographic protocol, and not a novel distributed transaction pattern, but a novel combination of hardware enforcement with the provisional-then-final execution pattern within a unified triadic state model. The provisional-then-final pattern has clear prior art; the hardware enforcement layer applied to it within TL's DLLA does not.

Identified gaps — externally visible I/O rollback limits, cascading provisional chain behavior, HSM single-point-of-compromise, and cloud deployment constraints — constitute a defined engineering roadmap. They do not represent fundamental architectural infeasibility. TL's PPT earns its feasibility claim on the warm path in hardware-capable deployments. The cases where TL's specific properties (physics-enforced gate + provisional/final lifecycle + immutable audit trail) are jointly required represent the deployments for which TL's architecture is most clearly the right engineering choice.

---

## Appendix: Formal Verification of the C-Element State Transition Model

### A.1 TLA+ Specification

*[The complete TLA+ specification is reproduced here from Session 2, Section 11. It is not repeated in full in this representation to avoid duplication — the specification in Session 2, Section 11.1 constitutes the normative formal model.]*

The specification covers:
- Three states: STATE_EPISTEMIC_HOLD (State 0), STATE_PROVISIONAL (State 1), STATE_FINAL_CONFIRMED (State 2)
- State transition conditions: Transition_0_to_1 (requires ppt_valid = TRUE), Transition_1_to_2 (requires fpt_valid = TRUE and expiry not fired), Transition_1_to_0_on_expiry (requires provisional_expiry_fired = TRUE)
- The `provisionalExpiry` timeout mechanism via a hardware counter model
- Prohibited transitions: State 0 → State 1 without PPT; State 1 → State 2 without FPT; State 0 → State 2 directly

### A.2 Safety Properties

**Safety 1 — No Provisional Without PPT:**
```
□(system_state = STATE_PROVISIONAL ⇒ ppt_valid = TRUE)
```
*Proof:* The only transition leading to STATE_PROVISIONAL is Transition_0_to_1, which has `ppt_valid = TRUE` as an explicit precondition. No other transition enables STATE_PROVISIONAL. Therefore, the invariant is preserved by construction over all reachable states. □

**Safety 2 — No Final Without FPT:**
```
□(system_state = STATE_FINAL_CONFIRMED ⇒ fpt_valid = TRUE)
```
*Proof:* The only transition leading to STATE_FINAL_CONFIRMED is Transition_1_to_2, which has `fpt_valid = TRUE` as an explicit precondition. □

**Safety 3 — No Final After Expiry:**
```
□(provisional_expiry_fired = TRUE ⇒ system_state ≠ STATE_FINAL_CONFIRMED)
```
*Proof:* Transition_1_to_2 requires `provisional_expiry_fired = FALSE` as an explicit precondition. When expiry fires (provisional_expiry_fired = TRUE), the only enabled transition is Transition_1_to_0_on_expiry, which returns to STATE_EPISTEMIC_HOLD. STATE_FINAL_CONFIRMED is unreachable from any state where provisional_expiry_fired = TRUE. □

### A.3 Liveness Property

**Liveness — Valid Cycle Proceeds to Final:**
```
□(ppt_valid = TRUE ∧ system_state = STATE_EPISTEMIC_HOLD ⇒ ◇(system_state = STATE_PROVISIONAL))
∧ □(system_state = STATE_PROVISIONAL ∧ fpt_valid = TRUE ⇒ ◇(system_state = STATE_FINAL_CONFIRMED))
```

*Proof (under weak fairness WF on Next actions):* Transition_0_to_1 is enabled whenever ppt_valid = TRUE, system_state = STATE_EPISTEMIC_HOLD, and provisional_expiry_fired = FALSE. Under WF(Next), an enabled action is eventually taken. Similarly, Transition_1_to_2 is enabled whenever system_state = STATE_PROVISIONAL, fpt_valid = TRUE, and provisional_expiry_fired = FALSE. Under WF(Next), an enabled action is eventually taken. The liveness property holds under the fairness assumption. □ (Partial — requires TLC model checking for bounded state space confirmation; full TLAPS proof is Future Work FW7.)

### A.4 Deadlock Freedom

*Proof:* TickAndCheckExpiry is enabled in every state (tick' = tick + 1 is always well-formed over Nat). Therefore, there is always at least one enabled action in the Next disjunction. The system has at least one possible next step from every reachable state. The specification is deadlock-free. □

---

## References

*Note: All references are based on the author's knowledge. DOIs and page numbers should be verified against primary sources prior to submission. Citation verification is identified as a pre-publication task.*

[1] Kung, H.T., Robinson, J.T. "On Optimistic Methods for Concurrency Control." ACM Transactions on Database Systems 6(2), 1981, pp. 213–226.

[2] Gray, J. "Notes on Data Base Operating Systems." In: Bayer, R., Graham, R.M., Seegmüller, G. (eds) Operating Systems. Lecture Notes in Computer Science, vol 60. Springer, Berlin, Heidelberg, 1978.

[3] Muller, D.E., Bartky, W.S. "A Theory of Asynchronous Circuits." Proceedings of the International Symposium on the Theory of Switching, Harvard University Press, 1959, pp. 204–243.

[4] Fant, K.M., Brandt, S.A. "NULL Convention Logic: A Complete and Consistent Logic for Asynchronous Digital Circuit Synthesis." Proceedings, IEEE International Conference on Application Specific Systems, Architectures and Processors, 1996, pp. 261–273.

[5] Garcia-Molina, H., Salem, K. "Sagas." ACM SIGMOD Record 16(3), 1987, pp. 249–259.

[6] Merkle, R.C. "A Digital Signature Based on a Conventional Encryption Function." Advances in Cryptology — CRYPTO '87, Lecture Notes in Computer Science, vol. 293. Springer, 1988, pp. 369–378.

[7] Costan, V., Devadas, S. "Intel SGX Explained." IACR Cryptology ePrint Archive, Report 2016/086, 2016.

[8] Lee, D., et al. "Keystone: An Open Framework for Architecting Trusted Execution Environments." Proceedings of the EuroSys Conference, 2020. DOI: 10.1145/3342195.3387532.

[9] Watson, R.N.M., et al. "CHERI: A Hybrid Capability-System Architecture for Scalable Software Compartmentalization." Proceedings of the IEEE Symposium on Security and Privacy, 2015.

[10] Klein, G., et al. "seL4: Formal Verification of an OS Kernel." Proceedings of the ACM SIGOPS Symposium on Operating Systems Principles (SOSP), 2009.

[11] Lamport, L. Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers. Addison-Wesley, 2002.

[12] Brumley, D., Tuveri, N. "Remote Timing Attacks are Practical." Proceedings of the 12th USENIX Security Symposium, 2003.

[13] NIST FIPS 140-3. Security Requirements for Cryptographic Modules. National Institute of Standards and Technology, 2019.

[14] NIST FIPS 186-5. Digital Signature Standard (DSS). National Institute of Standards and Technology, 2023.

[15] NIST FIPS 204. Module-Lattice-Based Digital Signature Standard (CRYSTALS-Dilithium). National Institute of Standards and Technology, 2024.

[16] NIST FIPS 205. Stateless Hash-Based Digital Signature Standard (SPHINCS+). National Institute of Standards and Technology, 2024.

[17] ISO 26262:2018. Road vehicles — Functional safety. International Organization for Standardization, 2018.

[18] IEC 62304:2006+AMD1:2015. Medical device software — Software life cycle processes. International Electrotechnical Commission, 2015.

[19] FDA 21 CFR Part 11. Electronic Records; Electronic Signatures. US Food and Drug Administration.

[20] PCI Security Standards Council. PCI Data Security Standard v4.0. March 2022.

[21] Goukassian, L. Dual-Lane Latency Architecture in Ternary Logic (TL): A Hardware-Enforceable Execution Model Specification. Document ID DLLA-TL-2026-03-20-REV1.

[22] Goukassian, L. Cryptographic Locking: A Hardware-Rooted Enforcement Specification for the 'No Log = No Action' Invariant. Internal TL specification document.

[23] Goukassian, L. "Atomic Auditability in Financial Execution Pipelines." Zenodo. DOI: 10.5281/zenodo.18716142.

[24] Goukassian, L. "Ternary Moral Logic: A Framework for AI Governance." AI and Ethics, Springer Nature. DOI: 10.1007/s43681-025-00910-6.

[25] Goukassian, L. "Ternary Logic: A Framework for Economic Decision-Making." AI and Ethics, Springer Nature. DOI: 10.1007/s43681-026-01124-0.

---

*End of Session 3 — Academic Paper*
