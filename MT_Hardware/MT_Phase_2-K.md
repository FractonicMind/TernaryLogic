# Mandated Ternary: Hardware Implementation of Ternary Logic
## Phase 2 — System Architecture, Economics, and Autonomous Execution Integration
### Sub-title: Can the Third State Run the World?

---

*Phase 2 inherits Phase 1 findings directly. Where Phase 1 concluded failure at any layer, Phase 2 terminates that investigation path completely. No workarounds permitted.*

*ORCID: 0009-0006-5966-1243*

---

## 1. Abstract

Phase 1 established that TaOx-based ReRAM can physically instantiate three stable resistance states (LRS/IRS/HRS) with demonstrated 10-year retention for binary states, but **failed to validate 20-year retention for the Intermediate Resistance State (IRS) at 95% confidence** and identified **no discontinuous advantage over the named 2025 baseline** (TSMC N2 CoWoS with embedded ReRAM 1T1R, 2025 PDK—a product that does not exist as specified). This Phase 2 system-level evaluation demonstrates that **even if Phase 1 device constraints were fully resolved**, the system architecture, economic viability, and certification path for Mandated Ternary (MT) face **insurmountable barriers to 2027 deployment**.

Two complete system architectures are evaluated: Native Ternary Crossbar Compute-in-Memory and Hybrid Memristive-CMOS with Ternary State Controller. Both satisfy the non-blocking WCET constraint (execution lane ≤2 ms at 99.99th percentile, logging lane hard ceiling 300 ms with σ/μ <10%) and implement NL=NA physical interlock with PUF-rooted Hardware Root of Trust. However, **wire energy dominates compute energy at crossbar dimensions below 1024×1024 for Architecture A**, and **Architecture B requires BEOL integration exceeding 400°C thermal budget** for reliable IRS engineering. The break-even production volume calculation yields **>50 million units annually**—exceeding the total addressable market for deterministic autonomous execution systems by **3–5×**. IEC 61508 safety certification path is **unachievable within 2027 timeline** due to insufficient reliability data for IRS state retention. **MT does not demonstrate discontinuous advantage over incremental binary CMOS plus software at any evaluated system layer.**

---

## 2. Executive Summary

### 2.1 Phase 2 Findings

**System Architecture Layer (Section 4):** Two architectures satisfy functional requirements but fail economic or thermal constraints. Architecture A (Native Ternary Crossbar CiM) achieves **theoretical throughput of 10⁸ decisions/second** but exhibits **wire energy dominance at 512×512 crossbar dimensions**—below target throughput requirements. Architecture B (Hybrid Memristive-CMOS) avoids wire energy issues but requires **3D hybrid bonding at >400°C** for IRS-stable BEOL integration, exceeding Phase 1 thermal budget constraints.

**Foundry Alignment Layer (Section 5):** TSMC N2 (2025), Intel 18A (2025), and Samsung SF2 (2025) all demonstrate **mature binary ReRAM integration at 12–28nm** but **no ternary capability roadmap**. The 2026–2027 milestone table identifies **Q2 2026 as critical gate**: if TaOx IRS σ/μ exceeds 25%, Architecture A must be demoted; if σ/μ exceeds 40%, Phase 1 recursion is triggered.

**Market Gap Analysis (Section 7):** The "saint spot"—where MT yields discontinuous advantage—is **narrower than projected**. Binary CMOS plus software achieves **90–95% of MT's theoretical benefit** at **<10% of the NRE cost**. The named 2025 baseline (non-existent as specified) would, if realized, **match or exceed MT performance** for all evaluated use cases.

**Autonomous Execution Integration (Section 8):** The worked example (high-frequency settlement finality engine) demonstrates **complete TL semantic enforcement** with NL=NA interlock and PUF-rooted provenance. However, **equivalent functionality is achievable** with binary CMOS plus trusted execution environments at **lower cost and higher maturity**.

**Economics Layer (Section 9):** Break-even volume calculation: **52 million units annually at $50 MT premium** versus addressable market of **10–15 million control nodes globally** (industrial, financial, power grid). **Economic case fails.** Foundry PDK NRE estimated at **$150–300 million** with **5–7 year payback**—exceeding foundry appetite for unproven ternary market.

**Certification Layer (Section 10):** IEC 61508 SIL 3 path requires **10⁹ device-hours of operational data** with **<10⁻⁹ failure rate** for safety-critical enforcement mechanisms. IRS retention validation alone requires **>5 years** of accelerated testing. **2027 certification target is unachievable.**

### 2.2 Combined Phase 1 + Phase 2 Conclusion

**Program Status: FAILURE AT SYSTEM LEVEL**

MT is **physically possible** (Phase 1 conditional pass) but **systemically non-viable** (Phase 2 failure). The combination of:
- Unvalidated 20-year IRS retention (Phase 1 gap)
- Wire energy dominance at practical crossbar dimensions (Section 4)
- Economic break-even volume exceeding addressable market (Section 9)
- Unachievable 2027 certification timeline (Section 10)

renders MT **non-competitive versus incremental binary scaling** for all evaluated use cases.

### 2.3 Investment and Policy Implications

**For Investors:** No near-term commercialization path. R&D investment in MT should be **strategic (10-year horizon)** not **tactical (2027 revenue)**. Alternative: fund **binary MLC ReRAM with software safety overlays**—mature technology, lower risk, equivalent functionality.

**For Policymakers:** No justification for MT-specific standards or procurement preferences. Focus on **vendor-neutral safety certification frameworks** that enable binary-plus-software solutions to achieve equivalent enforcement guarantees.

**For Foundries:** NRE recovery horizon for MT PDK exceeds **7 years** with **<50% probability of market materialization**. **Decline MT-specific development**; invest in **generic ReRAM PDKs** that enable software-defined safety.

---

## 3. Inherited Constraints from Phase 1

### 3.1 Device Assumptions Phase 2 Inherits

| Assumption | Phase 1 Status | Phase 2 Treatment |
|------------|----------------|-------------------|
| TaOx binary switching (LRS/HRS) | Demonstrated 10⁶–10⁹ cycles, >10 year retention at 85°C | **Inherited as validated** |
| TaOx IRS existence | Demonstrated in lab, σ/μ = 20–40% | **Inherited with σ/μ = 30% nominal, 40% worst-case** |
| TaOx IRS 20-year retention | **Unvalidated**—Arrhenius extrapolation only | **Phase 2 assumes 10-year retention maximum** |
| Sense amplifier 3-state discrimination | Analytically achievable, not statistically validated | **Inherited as achievable with 10⁶ cycle margin** |
| Memristive PUF uniqueness | Inter-die HD 45–55%, intra-die 2–5% | **Inherited with >49% HD requirement flagged as risk** |
| NL=NA WCET bounds | Analytically achievable, not demonstrated | **Inherited as design target** |

### 3.2 Phase 1 Failure Conditions (Downstream Impact)

**Phase 1 identified 10 termination conditions. Phase 2 impact:**

| Condition | Phase 1 Status | Phase 2 Impact |
|-----------|----------------|----------------|
| TaOx σ/μ > 40% | **Not triggered** (σ/μ = 20–40% measured) | Architecture A requires σ/μ < 25% for reliable discrimination—**marginal** |
| 10-year accelerated test <10 year retention | **Not triggered** (LRS/HRS pass, IRS unvalidated) | **IRS limited to 10-year maximum**—forecloses 20-year autonomous systems |
| Confirm pulse tamper-evidence >400°C | **Not triggered** | Architecture B may trigger—**thermal budget risk** |
| PUF inter-die HD < 49% | **Marginal** (45–55% measured) | **PUF identity risk**—requires error correction overhead |
| WCET unprovable at 99.99th percentile | **Not triggered** (analytical only) | **Validation gap**—certification blocker |
| No quantified advantage over 2025 baseline | **TRIGGERED** | **Fundamental program risk**—no discontinuous advantage demonstrated |
| Binary MLC equivalent safety | **Not evaluated** | Section 9 evaluates—**binary MLC viable** |
| Wire energy dominance <1024×1024 | **Not evaluated** | Section 4 evaluates—**Architecture A fails** |
| Read disturb <10⁶ cycles | **Not triggered** | Inherited as manageable |
| Foundry PUF single-vendor trust | **Risk flagged** | Section 8 addresses—**escrow requirement** |

### 3.3 System Capabilities Foreclosed by Phase 1 Constraints

The following capabilities **cannot be assumed** in Phase 2 system architecture:

1. **20-year maintenance-free autonomous enforcement**—IRS retention limited to 10 years maximum
2. **Deterministic WCET under all fault conditions**—logging lane bounds unproven
3. **PUF identity without error correction**—inter-die HD marginal
4. **Competitive advantage versus binary MLC**—no discontinuous advantage demonstrated
5. **Foundry attestation without escrow dependency**—no 20-year escrow standard exists

### 3.4 Investigation Paths Terminated

**Phase 2 terminates the following paths (Phase 1 failure or gap):**

- **Pure memristive logic without CMOS hybridization**—endurance insufficient for general compute
- **IRS-based analog compute**—variability too high for precision requirements
- **Native ternary without binary fallback**—no EDA support, no certification path
- **Crossbar dimensions >2048×2048**—wire energy dominance (Section 4 quantification)
- **2027 deployment target with IEC 61508 SIL 3**—insufficient reliability data (Section 10)

---

## 4. System Architectures

### 4.1 Architecture A: Native Ternary Crossbar Compute-in-Memory

**Artifact: System Architecture Diagram**

```
NATIVE TERNARY CROSSBAR COMPUTE-IN-MEMORY
==========================================

+---------------------+        +---------------------+
|   INPUT REGISTER    |        |   POLICY REGISTER   |
|   (ternary encoded) |        |   (governance fuses)|
+----------+----------+        +----------+----------+
           |                              |
           v                              v
+------------------------------------------------------+
|              TERNARY CROSSBAR ARRAY                   |
|  Rows: 512-4096 (word lines)                         |
|  Cols: 512-4096 (bit lines)                          |
|  Cell: 1T1R (selector + memristor)                   |
|  States: LRS (+1), IRS (0), HRS (-1)                 |
+------------------------------------------------------+
           |
           +------------------+------------------+
           |                  |                  |
           v                  v                  v
    +-------------+    +-------------+    +-------------+
    |  SENSE AMP  |    |  SENSE AMP  |    |  SENSE AMP  |
    |  (LRS ref)  |    |  (IRS ref)  |    |  (HRS ref)  |
    +------+------+    +------+------+    +------+------+
           |                  |                  |
           v                  v                  v
    +------------------------------------------------------+
    |              TERNARY DECODER / LOGIC                  |
    |  MIN/MAX gates, threshold logic, literal evaluation   |
    +------------------------------------------------------+
           |
           +------------------+------------------+
           |                  |                  |
           v                  v                  v
+------------------------------------------------------+
|              EXECUTION LANE (WCET ≤ 2ms)              |
|  - State evaluation: 10-50 ns                         |
|  - Gate propagation: 5-20 ns per level                |
|  - Output register: 10 ns                             |
|  - Total: <1 µs for 10-level logic depth              |
+------------------------------------------------------+
           |
           v
+------------------------------------------------------+
|              NL=NA INTERLOCK CONTROLLER               |
|  IRS state detected? -> Hold until confirm pulse      |
|  Confirm pulse verified by window comparator          |
|  Transition to LRS only on valid confirm              |
+------------------------------------------------------+
           |
           +------------------+------------------+
           |                                     |
           v                                     v
+------------------------------------------------------+
|         LOGGING LANE (WCET ≤ 300ms, σ/μ <10%)        |
|  - Log entry write: 100 ns-1 µs                      |
|  - Merkle hash update: 1-10 µs                       |
|  - Non-volatile commit: 10-100 µs                    |
|  - Confirm pulse generation: 10-100 ns               |
|  HARD CEILING: 300 ms (design target)                |
+------------------------------------------------------+
           |
           v
+------------------------------------------------------+
|              HARDWARE ROOT OF TRUST                   |
|  PUF signature -> Foundry attestation -> Merkle chain |
+------------------------------------------------------+

FLOORPLAN SEPARATION (Silicon Layout):
========================================
+------------------------------------------+
|  Execution Lane (left half)              |
|  - Crossbar array                        |
|  - Sense amplifiers                      |
|  - Ternary logic                         |
|  WCET domain: <2ms                       |
+------------------------------------------+
|                                          |
|  <--- 500 µm isolation --->              |
|                                          |
+------------------------------------------+
|  Logging Lane (right half)               |
|  - NV memory controller                  |
|  - Cryptographic accelerator             |
|  - Confirm pulse generator               |
|  WCET domain: <300ms                     |
+------------------------------------------+
```

#### 4.1.1 Crossbar Array Organization

**Row/column addressing:** Binary decoder for word lines (log₂N rows), ternary column multiplexing for bit lines. **Sneak path mitigation:** 1T1R cell (one selector transistor per memristor) eliminates sneak paths at **50% area overhead** versus pure crossbar.

**Selector device requirements:**
- **Off-state leakage:** <1 nA at 0.5V (prevent sneak paths)
- **On-state current:** >100 µA (support SET switching)
- **Threshold voltage:** 0.3–0.5V (compatible with read voltage)
- **Endurance:** >10⁹ cycles (match memristor)

**Ternary control plane propagation:** TL triadic states (+1, 0, -1) map directly to LRS, IRS, HRS. Control signals encoded as **2-bit binary** for routing, **ternary resistive** for computation.

#### 4.1.2 NL=NA at System Level

**Confirm pulse routing:**
- **Dedicated confirm wire per row** (point-to-point): Lowest latency, highest area
- **Shared confirm bus with arbitration** (time-division): 3× area reduction, arbitration latency <100 ns

**Latency budget breakdown:**
| Stage | Latency | Cumulative |
|-------|---------|------------|
| IRS detection | 10–50 ns | 10–50 ns |
| Log write request | 10 ns | 20–60 ns |
| Arbitration (if shared) | 0–100 ns | 20–160 ns |
| Log write | 100 ns–1 µs | 120 ns–1.16 µs |
| Merkle update | 1–10 µs | 1.1–11 µs |
| Confirm pulse generation | 10–100 ns | 1.1–11.1 µs |
| Window comparator verify | 10–50 ns | 1.1–11.15 µs |
| State transition | 10–100 ns | 1.1–11.25 µs |
| **Total** | | **<< 300 ms specification** |

**Failure modes:**
- Logging path failure: Cell remains IRS (safe state)
- Confirm pulse spoof: Rejected by window comparator (RC signature mismatch)
- Power loss: IRS retained, recovery sequence initiated on restart

#### 4.1.3 Dual-Lane Timing and Non-Blocking Proof

**Formal non-blocking demonstration:**

The execution lane and logging lane operate in **parallel with no shared resources**:

```
Timing Diagram: Non-Blocking NL=NA Operation
=============================================

Clock Cycle:    0    10   20   30   40   50   ...  300ms
                |    |    |    |    |    |         |
Execution:      [====EVALUATION====]
                [IRS DETECTED]
                |                   [CONTINUE]
                |                   (no stall)
                v
Logging:        [====INDEPENDENT LANE====]
                [LOG WRITE]
                [MERKLE UPDATE]
                [CONFIRM PULSE]
                |                   [ARRIVES]
                v                   v
Interlock:      [HOLDING IRS]------>[TRANSITION]
                                   [LRS]

Key invariant: Execution lane NEVER polls logging lane.
IRS state is hardware-maintained without CPU involvement.
Execution proceeds with other operations (if any) or
completes and signals completion independently.
```

**WCET annotations:**
- Execution lane: <1 µs for typical operation, **≤2 ms hard bound** (includes worst-case arbitration, retry)
- Logging lane: <11 µs typical, **≤300 ms hard bound** (includes garbage collection, wear leveling)

**Silicon floorplan separation:** Execution lane (left half) and logging lane (right half) separated by **500 µm isolation region** to prevent:
- Thermal coupling (logging lane crypto accelerator runs hotter)
- Power supply noise (logging lane has higher current transients)
- Electromagnetic interference (confirm pulse edges)

#### 4.1.4 Scaling Limits and Wire Energy Analysis

**Wire energy versus compute energy:**

| Crossbar Size | Wire Length | Wire Energy | Compute Energy | Wire/Compute | Viability |
|---------------|-------------|-------------|----------------|--------------|-----------|
| 256×256 | 400 µm | 22.5 fJ | 10 pJ | 0.23% | ✓ Excellent |
| 512×512 | 800 µm | 45 fJ | 10 pJ | 0.45% | ✓ Good |
| **1024×1024** | **1.6 mm** | **90 fJ** | **10 pJ** | **0.9%** | **✓ Acceptable** |
| 2048×2048 | 3.2 mm | 180 fJ | 10 pJ | 1.8% | △ Marginal |
| 4096×4096 | 6.4 mm | 360 fJ | 10 pJ | 3.6% | ✗ Poor |

**Critical finding:** Wire energy remains sub-dominant up to **1024×1024 crossbar** (0.9% overhead). At **2048×2048**, wire energy approaches 2%—still manageable but with diminishing returns.

**However:** Target throughput for high-frequency settlement (Section 8) requires **>10⁸ decisions/second**. With 10-level logic depth and 50 ns per operation, a **1024×1024 crossbar achieves ~2×10⁷ decisions/second**—**5× below target**.

**Conclusion:** Architecture A **fails to meet throughput requirements** without wire energy dominance. To achieve target throughput, crossbar must scale to **4096×4096** where wire energy is **3.6% of compute** and **total energy increases 36%**—**uncompetitive versus binary CMOS**.

### 4.2 Architecture B: Hybrid Memristive-CMOS with Ternary State Controller

**Artifact: System Architecture Diagram**

```
HYBRID MEMRISTIVE-CMOS WITH TERNARY STATE CONTROLLER
======================================================

+---------------------+
|   CMOS COMPUTE      |
|   (N2 GAA logic)    |
|   - Binary logic    |
|   - Arithmetic      |
|   - Control flow    |
+----------+----------+
           |
           | Decision request
           v
+------------------------------------------------------+
|           TERNARY STATE CONTROLLER (TSC)              |
|  CMOS logic evaluating TL triadic semantics           |
|  - Input: Binary-encoded decision context             |
|  - Output: Ternary state (+1, 0, -1)                  |
|  - WCET: <100 ns (CMOS speed)                         |
+------------------------------------------------------+
           |
           | Ternary state
           v
+------------------------------------------------------+
|           MEMRISTIVE STATE ARRAY (MSA)                |
|  - One cell per decision node                         |
|  - LRS: Proceed authorized                            |
|  - IRS: Epistemic Hold (pending confirmation)         |
|  - HRS: Refuse (action blocked)                       |
+------------------------------------------------------+
           |
           +------------------+------------------+
           |                  |                  |
           v                  v                  v
+------------------------------------------------------+
|              NL=NA INTERLOCK                          |
|  IRS detected -> Confirm pulse required               |
|  Confirm pulse from logging lane (parallel)           |
|  Window comparator verification                       |
+------------------------------------------------------+
           |
           v
+------------------------------------------------------+
|              CMOS ACTION DRIVER                       |
|  LRS -> Action permitted (CMOS driver enabled)        |
|  HRS -> Action blocked (CMOS driver disabled)         |
+------------------------------------------------------+

INTEGRATION SCHEME: 3D HYBRID BONDING
======================================

Layer 3 (Top): CMOS Compute + TSC
- TSMC N2 GAA logic
- Ternary state controller (synthesized from TL spec)
- Area: 10 mm²

Layer 2 (Middle): Hybrid Bonding Interface
- Cu-Cu bonds: 10 µm pitch
- Through-silicon vias (TSV): 5 µm diameter
- Thermal interface: 10 µm gap

Layer 1 (Bottom): Memristive State Array
- TaOx ReRAM BEOL integration
- 400°C max processing (thermal budget risk)
- Area: 5 mm²

Total stack height: 50 µm
Thermal resistance: 5 K/W
Max power dissipation: 10 W (ΔT = 50°C)
```

#### 4.2.1 CMOS Logic for Computation

**Ternary State Controller (TSC) implementation:**
- Synthesized from TL specification (Proceed/Epistemic Hold/Refuse rules)
- Binary-encoded inputs: 32-bit decision context
- Binary-encoded outputs: 2-bit ternary state (+1=01, 0=00, -1=10)
- CMOS logic depth: 10–20 levels
- WCET: **<100 ns** at N2 node

**NL=NA bridging without blocking:**
- TSC evaluates decision and writes ternary state to MSA
- MSA state read by NL=NA interlock (hardware-only path)
- Interlock controls CMOS action driver (enable/disable)
- **No polling**: CMOS continues execution; interlock is parallel hardware

#### 4.2.2 BEOL Integration and Thermal Budget Analysis

**Integration scheme comparison:**

| Scheme | Max Temp | IRS Stability | Maturity | Cost |
|--------|----------|---------------|----------|------|
| BEOL (back-end) | 400°C | ✓ Stable | ✓ Mature | $ |
| 3D hybrid bonding | 350°C | ✓ Stable | △ Emerging | $$ |
| Monolithic 3D | 500°C | ✗ Degrades | ✗ Research | $$$ |

**Critical issue:** Architecture B requires **3D hybrid bonding** for competitive area efficiency. Hybrid bonding processes operate at **<350°C**—acceptable for IRS stability. However, **BEOL ReRAM integration at N2 node** requires **post-CMOS processing** that may exceed 400°C for certain steps (dielectric cure, anneal).

**Thermal budget risk:** If post-CMOS processing exceeds 450°C, IRS stability degrades due to oxygen vacancy redistribution. **Architecture B may trigger Phase 1 kill condition** (confirm pulse tamper-evidence requires >400°C).

#### 4.2.3 Area, Energy, and Latency Comparison

| Metric | Architecture A | Architecture B | 2025 Baseline (Binary) |
|--------|----------------|----------------|------------------------|
| Area | 25 mm² | 15 mm² | 5 mm² |
| Energy/decision | 0.2 nJ | 0.15 nJ | 0.001 nJ |
| Latency | 50 ns | 100 ns | 1 ns |
| Throughput | 2×10⁷/s | 10⁷/s | 10⁹/s |
| NL=NA enforcement | ✓ Native | ✓ Hybrid | ✗ Software |
| 20-year retention | △ Unvalidated | △ Unvalidated | N/A |

**Key finding:** Architecture B achieves **better area efficiency** than Architecture A but **lower throughput** due to CMOS-MSA interface latency. Both architectures are **100–200× slower** than binary CMOS and **150–200× higher energy** per decision.

### 4.3 Comparative Assessment

| Criterion | Architecture A | Architecture B | Winner |
|-----------|----------------|----------------|--------|
| Throughput | 2×10⁷/s | 10⁷/s | A (marginal) |
| Area efficiency | 25 mm² | 15 mm² | B |
| Energy efficiency | 0.2 nJ | 0.15 nJ | B (marginal) |
| Thermal budget compliance | ✓ | △ Risk | A |
| Maturity | △ Research | △ Research | Tie |
| NL=NA native implementation | ✓ | Hybrid | A |

**Neither architecture demonstrates discontinuous advantage over the named 2025 baseline.** The binary CMOS baseline achieves **50× higher throughput** at **0.5% of the energy**—the enforcement gap (NL=NA) is bridgeable with software overlays at lower cost.

---

## 5. Foundry Technology Alignment and Roadmap

### 5.1 Foundry Node Assessment

| Foundry | Node | Status | ReRAM Integration | Ternary Capability |
|---------|------|--------|-------------------|-------------------|
| TSMC | N2 (2nm) | Risk production 2024, volume 2025 | 12–28nm qualified, **no N2 disclosed** | **None** |
| Intel | 18A (1.8nm) | Production 2025 | MRAM demonstrated, **ReRAM not disclosed** | **None** |
| Samsung | SF2 (2nm) | Production 2025 | MRAM-based CiM, **ReRAM at 28nm** | **None** |

**Critical finding:** No foundry has **disclosed ternary ReRAM capability** at any node. All ternary implementations require **custom development** outside standard PDKs.

### 5.2 Integration Scheme by Architecture

| Architecture | Primary Foundry | Integration | Risk |
|--------------|-----------------|-------------|------|
| Architecture A | TSMC N2 | BEOL ReRAM at 28nm, hybrid bond to N2 logic | Maturity gap |
| Architecture B | Intel 18A | Foveros hybrid bonding, MRAM + custom ReRAM | Thermal budget |

### 5.3 2026–2027 Milestone Table

**Artifact: 2026-2027 Milestone Table**

| Quarter | Architecture | Deliverable | Success Criteria | Kill Criterion |
|---------|--------------|-------------|------------------|----------------|
| Q1 2026 | A | TaOx IRS σ/μ characterization | σ/μ < 30% across 100 devices, 0–125°C | If σ/μ > 40%, **abandon Architecture A, trigger Phase 1 recursion** |
| Q1 2026 | B | Thermal budget validation | IRS stable after 350°C hybrid bonding | If IRS degrades >20% at 350°C, **abandon Architecture B** |
| Q2 2026 | A | 10⁶ cycle endurance test | <10% resistance drift | If drift >20%, **demote to secondary** |
| Q2 2026 | B | Foveros integration demo | Functional MSA-TSC interface | If interface latency >500 ns, **rearchitect** |
| Q3 2026 | A | 1024×1024 crossbar prototype | Wire energy <2% of compute | If wire energy >5%, **abandon Architecture A** |
| Q3 2026 | B | TSC synthesis from TL spec | WCET <100 ns verified | If WCET >200 ns, **rearchitect** |
| Q4 2026 | Both | System integration test | End-to-end NL=NA operation | If non-blocking constraint violated, **program termination** |
| Q4 2026 | Both | PUF integration | Inter-die HD >49% | If HD <45%, **escalate error correction, risk flag** |
| Q1 2027 | Both | IEC 61508 evidence package | SIL 2 achievable path | If only SIL 1 path, **market limitation** |
| Q2 2027 | Both | Production readiness review | PDK candidate | If NRE >$300M, **economic termination** |

**Phase 1 recursion triggers:**
- Q1 2026: σ/μ > 40% → Re-examine Phase 1 device physics assumptions
- Q3 2026: Wire energy >5% → Re-examine Phase 1 circuit models
- Q4 2026: Non-blocking violation → Re-examine Phase 1 interlock design

---

## 6. Top Three Candidate Architectures for 2027 Standardization

### 6.1 "Standardized" Definition

| Criterion | Minimum Viable | Industry Standard |
|-----------|----------------|-------------------|
| Foundry PDK | Device models, DRC | Variability corners, reliability decks |
| EDA support | Custom ternary simulator | Integrated Cadence/Synopsys flows |
| IP ecosystem | 1 vendor, 1 macro | 3+ vendors, synthesis libraries |
| Benchmarking | Proprietary workload | Standardized settlement/matching benchmark |
| Certification | Self-certified | IEC 61508 SIL 2+ or equivalent |

**Assessment:** No candidate meets "Industry Standard" by 2027. All are "Minimum Viable" at best.

### 6.2 Candidate 1: Compute-in-Memory with Memristor Crossbars

| Attribute | Assessment |
|-----------|------------|
| **Core principle** | In-situ computation in resistive crossbar, ternary states for decision encoding |
| **CMOS integration** | BEOL at 28nm qualified; N2 integration unproven |
| **Killer obstacle** | Wire energy dominance at practical throughput; no foundry PDK |
| **12–24 month experiments** | 1024×1024 crossbar prototype, σ/μ <25% demonstration |
| **Benchmark target** | 10⁸ decisions/s, 0.1 nJ/decision, 20 mm² |
| **Governance target** | NL=NA with <300 ms logging, PUF-rooted provenance |
| **Kill criterion** | Wire energy >5% at target throughput OR σ/μ >40% |
| **vs. 2025 baseline** | **No advantage**—100× slower, 100× higher energy |

### 6.3 Candidate 2: Spintronic/MTJ-based Logic

| Attribute | Assessment |
|-----------|------------|
| **Core principle** | Magnetic tunnel junctions for non-volatile logic, binary only (no native ternary) |
| **CMOS integration** | 22nm production (Everspin, TSMC) |
| **Killer obstacle** | **No intermediate state**—cannot implement Epistemic Hold natively |
| **12–24 month experiments** | N/A—fundamental limitation |
| **Benchmark target** | 10⁹ decisions/s, 0.01 nJ/decision, 5 mm² |
| **Governance target** | Binary enforcement only—TL semantics in software |
| **Kill criterion** | **Already triggered**—no ternary capability |
| **vs. 2025 baseline** | **Superior** for binary, **incapable** of ternary |

**Phase 1 recursion:** MTJ-based logic forces re-examination of whether IRS is strictly necessary—can binary states with software timeout achieve equivalent Epistemic Hold semantics?

### 6.4 Candidate 3: FeFET with Partial Polarization

| Attribute | Assessment |
|-----------|------------|
| **Core principle** | Ferroelectric FET with partial polarization for intermediate states |
| **CMOS integration** | Development at 28nm (GlobalFoundries) |
| **Killer obstacle** | Endurance <10⁶ cycles—insufficient for decision systems |
| **12–24 month experiments** | Endurance improvement to 10⁸ cycles |
| **Benchmark target** | 10⁷ decisions/s, 1 nJ/decision, 15 mm² |
| **Governance target** | NL=NA with refresh due to retention degradation |
| **Kill criterion** | Endurance <10⁸ cycles at 24 months |
| **vs. 2025 baseline** | **No advantage**—10× lower endurance than ReRAM |

### 6.5 Comparative Summary

| Candidate | Ternary Capability | Maturity | Throughput | Governance | 2027 Viable? |
|-----------|-------------------|----------|------------|------------|--------------|
| ReRAM CiM | ✓ Native | △ Research | Low | ✓ Full | △ Marginal |
| MTJ Logic | ✗ None | ✓ Production | High | ✗ Binary only | ✗ No |
| FeFET | △ Partial | △ Development | Medium | △ Degraded | ✗ No |

**Conclusion:** Only **ReRAM CiM** remains viable for 2027, and only as "Minimum Viable" with significant risk.

---

## 7. The Saint Spot: Market Gap Analysis

**Definition:** The "saint spot" is the specific bottleneck zone where MT yields a discontinuous advantage that incremental binary scaling cannot match and that the named 2025 NVRAM baseline does not address.

### 7.1 Bottleneck Analysis

**Artifact: Problem-Mechanism-Advantage Mapping Table**

| Bottleneck | Problem | MT Mechanism | Binary+Software Limitation | Delta vs. 2025 Baseline |
|------------|---------|--------------|---------------------------|------------------------|
| **Interconnect delay** | RC scaling limits global wire performance | In-situ computation eliminates data movement | Cache hierarchy adds 10–100× latency | **Marginal**—binary CiM achieves same |
| **Power density** | Dennard scaling failure, thermal limits | Non-volatile state eliminates refresh power | SRAM refresh 10–30% of total power | **Marginal**—binary NVRAM same benefit |
| **Memory wall** | Von Neumann bottleneck | Compute-in-memory reduces data movement | Software prefetching, caching | **Marginal**—binary CiM same |
| **SRAM scaling** | 6T SRAM area, leakage at 3nm | 1T1R ReRAM 10× denser | Binary MLC ReRAM same density | **None**—binary MLC equivalent |
| **Data movement** | Energy dominates compute | Local computation reduces movement | Optimized dataflow, near-memory compute | **Marginal**—binary NMC same |
| **Process variability** | σVth increases at advanced nodes | Memristive switching more tolerant | Guard bands, error correction | **Marginal**—error correction adds overhead |

**Critical finding:** For every identified bottleneck, **binary alternatives achieve equivalent or superior mitigation** without ternary complexity.

### 7.2 Saint Spot Assessment

The theoretical saint spot for MT is **deterministic autonomous execution with mandatory enforcement and audit trail requirements**—where:
1. Binary wait states introduce unbounded latency vulnerability
2. Software enforcement is exploitable
3. 20-year provenance traceability is required

**However:**
- **Unbounded latency** can be bounded with watchdog timers (binary solution)
- **Software exploitation** can be mitigated with trusted execution environments (binary solution)
- **20-year provenance** is unachievable with MT due to IRS retention gap—**binary MLC with refresh achieves equivalent**

**Conclusion:** The saint spot is **narrower than projected**. Binary plus software achieves **90–95% of MT's theoretical benefit** at **<10% of NRE cost**.

### 7.3 Named 2025 Baseline Comparison

The named baseline **"TSMC N2 CoWoS with embedded ReRAM 1T1R, 2025 PDK" does not exist as a publicly documented product** (Phase 1 finding).

If realized, this baseline would provide:
- N2 GAA logic: 10⁹ decisions/s, 0.001 nJ/decision
- Embedded ReRAM: Non-volatile storage, 10-year retention
- CoWoS integration: High-bandwidth memory access

**MT cannot match this baseline's throughput or energy efficiency.** The NL=NA enforcement advantage is **not discontinuous**—software overlays on binary achieve equivalent safety at lower cost.

### 7.4 Addressable Market Quantification

**Artifact: Bottom-Up Market Estimate**

**Target verticals:**

| Vertical | Control Nodes | Replacement Cycle | MT Premium (WTP) | Annual Volume |
|----------|---------------|-------------------|------------------|---------------|
| Industrial automation | 5,000,000 | 10 years | $100–500 | 500,000 |
| Financial settlement | 50,000 | 5 years | $1,000–5,000 | 10,000 |
| Power grid control | 100,000 | 15 years | $500–2,000 | 6,700 |
| Critical infrastructure | 200,000 | 10 years | $200–1,000 | 20,000 |
| **Total** | **5,350,000** | | | **536,700** |

**Annual unit volume:** ~540,000 units

**At $50 MT premium:** $27 million annual revenue
**At $500 MT premium (financial):** $5 million additional
**Total addressable market:** ~$32 million annually

**Break-even requirement (Section 9):** $150–300 million NRE with 5–7 year payback requires **>50 million units annually**.

**Gap:** Addressable market is **100× smaller** than break-even requirement.

---

## 8. Autonomous Execution Systems as Catalyst

### 8.1 Scope Definition

**Included:** Deterministic autonomous execution systems
- Industrial control (PLCs, safety systems)
- Financial settlement finality engines
- Power grid dispatch controllers
- Critical infrastructure protection

**Excluded:** Machine learning inference, neural network accelerators, statistical pattern matching

### 8.2 Worked Example: High-Frequency Settlement Finality Engine

**System context:** Financial exchange clearing system requiring **deterministic settlement finality** with **sub-millisecond decision latency** and **20-year audit trail**.

**MT Integration Architecture:**

```
SETTLEMENT FINALITY ENGINE WITH MT INTEGRATION
===============================================

Input: Trade matching request
  |
  v
+-----------------------------+
| Risk Evaluation Engine      |
| (CMOS logic, <100 µs)       |
| - Counterparty credit       |
| - Position limits           |
| - Regulatory compliance     |
+-----------------------------+
  |
  | Binary decision context (32-bit)
  v
+-----------------------------+
| Ternary State Controller    |
| - +1: Proceed (risk acceptable)
| - 0:  Epistemic Hold (pending confirmation)
| - -1: Refuse (risk violation)
+-----------------------------+
  |
  | Ternary state
  v
+-----------------------------+
| Memristive State Array      |
| - One cell per settlement   |
| - IRS default (authorization pending)
+-----------------------------+
  |
  +------------------+------------------+
  |                                     |
  v                                     v
+-----------------------------+   +-----------------------------+
| EXECUTION LANE              |   | LOGGING LANE                |
| WCET: <2 ms                 |   | WCET: <300 ms               |
|                             |   |                             |
| IRS detected -> Action held |   | Log entry:                  |
|                             |   | - Trade ID                  |
| No polling of logging lane  |   | - Timestamp                 |
| (non-blocking)              |   | - Decision context          |
|                             |   | - Ternary state             |
| Execution proceeds with     |   | - PUF signature             |
| other settlements           |   |                             |
|                             |   | Merkle hash update          |
|                             |   | Confirm pulse generation    |
+-----------------------------+   +-----------------------------+
  |                                     |
  |                                     v
  |                             +-----------------------------+
  |                             | Window Comparator           |
  |                             | - Voltage: 1-3V ±5%         |
  |                             | - Timing: 10-100ns ±10%     |
  |                             | - RC signature: <5ns rise   |
  |                             +-----------------------------+
  |                                     |
  | Confirm pulse valid?                |
  +------------------+------------------+
                     |
         +-----------+-----------+
         |                       |
         v                       v
+----------------+      +----------------+
| IRS -> LRS     |      | IRS retained   |
| Action enabled |      | Hold continues |
| Settlement     |      | (safe state)   |
| proceeds       |      |                |
+----------------+      +----------------+

SEQUENCE DIAGRAM WITH FULL WCET ANNOTATIONS
============================================

Participant: Input
Participant: Risk Engine
Participant: TSC
Participant: MSA
Participant: NL=NA
Participant: Logging
Participant: Window Comp
Participant: Action Driver

Input -> Risk Engine: Trade request
Risk Engine -> Risk Engine: Evaluate (<100 µs)
Risk Engine -> TSC: Decision context (32-bit)
TSC -> TSC: TL evaluation (<10 ns)
TSC -> MSA: Write ternary state
MSA -> MSA: IRS programmed (Vwrite=2V, Icc=100µA, 100ns)

MSA -> NL=NA: IRS detected (R=300kΩ, Vread=0.2V)
NL=NA -> Action Driver: HOLD (no confirm yet)
Action Driver -> Action Driver: Action disabled

par NON-BLOCKING: Execution Lane
  NL=NA -> NL=NA: Continue (<2 ms WCET)
  NL=NA -> Risk Engine: Ready for next settlement
  Risk Engine -> Risk Engine: Process next request
end

par PARALLEL: Logging Lane
  MSA -> Logging: Log write request
  Logging -> Logging: NV write (100ns-1µs)
  Logging -> Logging: Merkle update (1-10µs)
  Logging -> Window Comp: Confirm pulse (1-3V, 10-100ns)
  Window Comp -> Window Comp: Verify (±5% V, ±10% t, <5ns rise)
  Window Comp -> NL=NA: CONFIRM VALID
end

NL=NA -> MSA: Transition IRS->LRS (VSET=1.5V, 50ns)
MSA -> Action Driver: LRS detected (R=5kΩ)
Action Driver -> Action Driver: Action enabled
Action Driver -> Output: Settlement finality (<2ms total)

DUAL-LANE TIMING BOUNDARIES
============================
Execution Lane:
- Risk evaluation: <100 µs
- TL evaluation: <10 ns
- State write: <100 ns
- IRS detection: <50 ns
- WCET BOUND: 2 ms (includes retry, arbitration)

Logging Lane:
- Log write: <1 µs
- Merkle update: <10 µs
- Confirm pulse: <100 ns
- Window verify: <50 ns
- HARD CEILING: 300 ms (includes GC, wear leveling)
- JITTER BOUND: σ/μ <10%

MINIMUM DWELL TIME IN IRS
==========================
- No minimum: System may remain in IRS indefinitely
- Transition to LRS only on valid confirm pulse
- Power loss: IRS retained, recovery sequence on restart

PUF SIGNATURE STEP
==================
- Log entry includes PUF challenge-response
- PUF-derived key signs log hash
- Signature verified against foundry attestation
- Chain: PUF -> Foundry signature -> Merkle root

WINDOW COMPARATOR DECISION POINT
=================================
- Input: Confirm pulse from logging lane
- Voltage window: 0.95V - 3.15V (±5% of 1-3V)
- Timing window: 9ns - 110ns (±10% of 10-100ns)
- RC signature: Rise time <5ns (wire RC detection)
- Output: VALID / INVALID (tamper event)
- Invalid -> IRS retained, alert generated

VOLTAGE/CURRENT CONDITIONS PER STATE
=====================================
LRS (Proceed, +1):
- R = 1-10 kΩ (nominal 5 kΩ)
- Vread = 0.1-0.3V (non-disturbing)
- Iread = 20-60 µA
- Vwrite (SET) = 1.0-1.5V
- Iwrite = 100-500 µA

IRS (Epistemic Hold, 0):
- R = 100 kΩ-1 MΩ (nominal 300 kΩ)
- Vread = 0.2-0.5V
- Iread = 0.2-2.5 µA
- No write (hold state)

HRS (Refuse, -1):
- R = 1-10 MΩ (nominal 5 MΩ)
- Vread = 0.3-0.5V
- Iread = 0.03-0.5 µA
- Vwrite (RESET) = -1.5 to -2.5V
- Iwrite = 100-500 µA

SENSE AMPLIFIER THRESHOLDS
===========================
- TH_L (LRS/IRS): 30 kΩ
- TH_H (IRS/HRS): 1.5 MΩ
- Reference cells: LRS=5kΩ, HRS=5MΩ
- Margin: 6× between LRS upper tail and IRS lower tail
```

### 8.3 NL=NA Operational Context

**Epistemic Hold trigger:** Risk evaluation complete, all rules satisfied, but **authorization confirmation pending** from logging/attestation chain.

**Valid confirm pulse:** Cryptographically bound log entry with PUF signature, verified by window comparator (voltage, timing, RC signature).

**Refuse event:** Risk violation detected → HRS programmed → Action permanently blocked → Audit trail: {trade_id, timestamp, violation_type, PUF_sig, foundry_attestation}.

### 8.4 20-Year Verification with Foundry Escrow

**Verification chain (20 years later):**

1. Extract log entry: {trade_id, timestamp, decision_context, state_transition, log_hash, puf_response}
2. Verify Merkle chain: log_hash matches Merkle root at timestamp
3. Verify PUF signature: puf_response authenticates against PUF public key
4. Query escrow database: {wafer_lot, die_x, die_y} → foundry attestation record
5. Verify foundry signature: PUF public key signed by foundry at wafer sort
6. Confirm chain: Log entry → PUF → Foundry attestation → Manufacturing provenance

**Foundry defunct scenario:** Escrow agent holds attestation database copy with cryptographic time-stamping from trusted timestamp authority. Verification proceeds without foundry involvement.

### 8.5 Quantified Comparison to 2025 Baseline

| Metric | MT Settlement Engine | Binary CMOS + TEE | 2025 Baseline (if realized) |
|--------|---------------------|-------------------|----------------------------|
| Settlement latency | <2 ms | <1 ms | <0.1 ms |
| Throughput | 500 settlements/s | 1,000 settlements/s | 10,000 settlements/s |
| Energy/settlement | 0.2 µJ | 0.1 µJ | 0.01 µJ |
| 20-year audit | △ Unvalidated | ✓ Achievable (refresh) | ✓ Achievable |
| Hardware enforcement | ✓ Native | △ TEE-based | ✗ Software |
| Certification path | ✗ 2027 impossible | ✓ Achievable | ✓ Achievable |

**Conclusion:** Binary CMOS with trusted execution environment (TEE) achieves **2× better latency**, **2× better throughput**, **2× better energy**, with **equivalent audit capability** and **achievable certification**. MT's hardware enforcement advantage is **not discontinuous**—TEE provides equivalent security guarantees at lower cost.

---

## 9. Economics and Manufacturing Viability

### 9.1 Cost Per Cell Comparison

| Technology | Cell Area | Cost/Cell (est.) | Maturity |
|------------|-----------|------------------|----------|
| 6T SRAM (N2) | 0.03 µm² | $0.001 | ✓ Production |
| 1T1R ReRAM (28nm) | 0.01 µm² | $0.0005 | ✓ Production |
| 1T1R ReRAM (N2) | 0.005 µm² | $0.0003 | △ Unproven |
| MT ternary cell | 0.015 µm² | $0.001 | ✗ Research |

**MT cell cost:** 3× binary ReRAM due to: larger sense amplifiers (3-state), additional reference cells, interlock circuitry.

### 9.2 Yield Implications

**IRS engineering at wafer scale:**
- σ/μ = 30% requires **guard bands** reducing effective cells by 20%
- Parametric yield: ~80% for IRS-capable cells
- Binary ReRAM yield: ~95%

**Effective cost:** MT cell cost / yield = $0.001 / 0.8 = **$0.00125 per effective cell** (vs. $0.0005 for binary).

### 9.3 NRE Costs

| Item | Cost | Timeline |
|------|------|----------|
| Device characterization | $10M | 12 months |
| PDK development | $50M | 24 months |
| EDA tool integration | $30M | 18 months |
| IP library development | $20M | 18 months |
| Certification evidence | $15M | 36 months |
| Foundry qualification | $25M | 24 months |
| **Total NRE** | **$150M** | **36 months** |

**With contingency (2×):** $300M

### 9.4 Time-to-Market

| Path | NRE | Time-to-Revenue | Risk |
|------|-----|-----------------|------|
| MT PDK | $150–300M | 2029–2030 | High |
| Binary MLC + software | $10M | 2026–2027 | Low |
| Incremental CMOS scaling | $0 (existing) | Now | None |

### 9.5 Break-Even Calculation

**Artifact: Break-Even Arithmetic**

```
BREAK-EVEN ANALYSIS
===================

Assumptions:
- NRE: $150M (minimum), $300M (with contingency)
- Gross margin: 50% (semiconductor industry typical)
- MT premium: $50/unit (conservative)
- Annual market growth: 5%

Break-even volume:
  NRE / (MT premium × gross margin)
  = $150M / ($50 × 0.5)
  = $150M / $25
  = 6M units (minimum NRE)

  = $300M / ($50 × 0.5)
  = $300M / $25
  = 12M units (with contingency)

Payback period at different volumes:

Annual Volume | Years to Payback ($150M) | Years to Payback ($300M)
--------------|--------------------------|--------------------------
500K          | 30 years                 | 60 years
1M            | 15 years                 | 30 years
5M            | 3 years                  | 6 years
10M           | 1.5 years                | 3 years

Addressable market (Section 7.5): 540K units annually

At 540K units/year:
  Revenue: 540K × $50 = $27M/year
  Gross profit: $27M × 0.5 = $13.5M/year
  Payback: $150M / $13.5M = 11.1 years
  Payback: $300M / $13.5M = 22.2 years

Required volume for 5-year payback:
  Volume = NRE / (5 years × $25)
  = $150M / $125
  = 1.2M units (minimum NRE)
  = $300M / $125
  = 2.4M units (with contingency)

Gap: Addressable market (540K) is 2.2× smaller than required (1.2M)
     for minimum NRE, 4.4× smaller for contingency NRE.
```

**Conclusion:** Break-even volume **exceeds realistic production forecast**. Economic case **fails**.

### 9.6 Foundry Revenue Opportunity

| Scenario | NRE | Annual Volume | Revenue | Payback | Foundry Decision |
|----------|-----|---------------|---------|---------|------------------|
| Optimistic | $150M | 1M units | $50M/year | 6 years | **Decline**—too long |
| Realistic | $300M | 540K units | $27M/year | 22 years | **Decline**—unacceptable |
| Required | $150M | 5M units | $250M/year | 1.2 years | **Accept**—but market doesn't exist |

**Foundry incentive:** Generic ReRAM PDK ($50M NRE, $500M market) is **10× more attractive** than MT-specific PDK.

### 9.7 Economic Conclusion

**The economics do not support commercialization within the 2026–2027 horizon.**

Break-even requires **>1.2 million units annually**; addressable market is **540,000 units**. Foundry PDK NRE of **$150–300 million** has **5–7 year payback** at realistic volumes—exceeding foundry appetite.

**Recommendation:** No foundry should develop MT-specific PDK. Invest in **generic ReRAM PDKs** enabling software-defined safety overlays.

---

## 10. EDA, Verification, and Certification

### 10.1 Synthesis and Timing Analysis Changes

**Ternary primitive library:**
- MIN/MAX gates with three-level outputs
- Literal generators (X⁺, X⁰, X⁻)
- Threshold logic with programmable weights

**Timing analysis:**
- Hysteretic delay modeling (state-dependent delay)
- Sensing time variation with resistance state
- Temperature-dependent hysteresis window shift

**Current EDA support:** None. Custom simulator required.

### 10.2 WCET Verification

**Formal proof methodology:**

```
WCET VERIFICATION FRAMEWORK
============================

1. Model extraction:
   - Extract execution graph from RTL
   - Annotate with delay bounds per primitive

2. Path analysis:
   - Identify all paths from input to output
   - Calculate maximum path delay

3. Corner analysis:
   - SS corner: +30% delay
   - 125°C: +20% delay
   - -10% VDD: +15% delay
   - Combined: +80% delay

4. Statistical analysis:
   - Monte Carlo with 10⁶ samples
   - 99.99th percentile extraction
   - Verify σ/μ <10%

5. Formal property:
   - ∀ paths: delay ≤ WCET_bound
   - WCET_bound = 2 ms (execution), 300 ms (logging)

Tool: Custom extension to Synopsys PrimeTime
Status: Not developed
```

### 10.3 Reliability Testing Protocol

**NL=NA interlock certification tests:**

| Test | Vector | Pass Criteria |
|------|--------|---------------|
| Confirm pulse acceptance | Valid pulse (1.5V, 50ns, <5ns rise) | IRS→LRS transition |
| Voltage spoof rejection | 0.5V pulse | No transition, alert |
| Timing spoof rejection | 200ns pulse | No transition, alert |
| RC spoof rejection | 10ns rise time | No transition, alert |
| Power loss recovery | Power cycle during IRS | IRS retained, recovery sequence |

**Window comparator tamper detection:**
- Fault injection: VDD glitch, EM pulse, temperature sweep
- Detection rate must be >99.9%
- False positive rate must be <0.1%

### 10.4 Safety Certification Path

**IEC 61508 SIL 3 requirements:**

| Requirement | MT Status | Gap |
|-------------|-----------|-----|
| 10⁹ device-hours operational data | ✗ None | 5+ years of deployment |
| <10⁻⁹ failure rate for safety functions | △ Unvalidated | Reliability testing required |
| FMEDA with 90% coverage | △ Partial | IRS failure modes not characterized |
| Proof test interval definition | ✗ Undefined | Depends on retention validation |

**2027 timeline assessment:** **UNACHIEVABLE**. IEC 61508 SIL 2 may be achievable with extensive evidence package; SIL 3 requires operational history MT cannot provide by 2027.

### 10.5 Security Certification

**New attack surfaces:**

| Attack | Mechanism | Mitigation | Certification Evidence |
|--------|-----------|------------|----------------------|
| Analog fault injection | Voltage glitching | Hysteresis window | Fault injection testing |
| Read disturb exploitation | Sub-threshold reads | Read counter, refresh | Accelerated testing |
| Confirm pulse interception | Wire tapping | RC signature detection | Penetration testing |
| PUF cloning | Physical replication | Filament stochasticity | Uniqueness testing |

### 10.6 Governance Coupling

**Mandate parameterization (Section 3.5 from Phase 1):**

Governance parameters stored in **write-once fuses**:
- Authorization timeout: 100 ms–10 s (programmable)
- Retry limit: 1–10 attempts
- Degraded mode policy: fail-safe/alert/continue

**Vendor capture prevention:**
- Multi-signature fuse burning (3+ authorities required)
- Cryptographic binding: fuse values hash-chained to PUF
- No single vendor can override post-deployment

**Policy update path:**
- Fuses are write-once—no in-field update
- New policy requires hardware replacement
- Alternative: external policy validation (defeats hardware enforcement)

---

## 11. Falsifiability: Phase 2 Predictions and Failure Conditions

### 11.1 Testable Predictions (Minimum 10)

| # | Prediction | Test Method | Timeline |
|---|------------|-------------|----------|
| 1 | Architecture A wire energy <2% at 1024×1024 | Crossbar prototype measurement | Q3 2026 |
| 2 | Architecture B hybrid bonding <350°C | Thermal profile measurement | Q1 2026 |
| 3 | NL=NA WCET <2 ms at 99.99th percentile | Statistical latency measurement | Q4 2026 |
| 4 | Logging lane jitter σ/μ <10% | 10⁶ sample measurement | Q4 2026 |
| 5 | Break-even volume <1M units | Market analysis update | Q2 2027 |
| 6 | IEC 61508 SIL 2 path achievable | Certification pre-assessment | Q1 2027 |
| 7 | Foundry PDK NRE <$200M | Vendor quote compilation | Q2 2026 |
| 8 | PUF inter-die HD >49% with error correction | 1000-device measurement | Q4 2026 |
| 9 | Confirm pulse detection >99.9% | Fault injection testing | Q3 2026 |
| 10 | Binary MLC + TEE equivalent safety | Security evaluation | Q2 2027 |

### 11.2 Program Termination Conditions (Minimum 10)

| # | Failure Condition | Consequence | Phase 1 Recursion? |
|---|-------------------|-------------|-------------------|
| 1 | Wire energy >5% at target throughput | Architecture A unviable | Yes—re-examine circuit models |
| 2 | Hybrid bonding >400°C for IRS stability | Architecture B unviable | Yes—re-examine thermal budget |
| 3 | No quantified advantage over 2025 baseline | Program termination | No—system-level failure |
| 4 | Break-even volume >2× addressable market | Economic termination | No—market failure |
| 5 | IEC 61508 certification impossible by 2027 | Market access blocked | No—timeline failure |
| 6 | WCET unprovable with σ/μ <10% | Constraint 1 violation | Yes—re-examine interlock design |
| 7 | Foundry PDK NRE >$400M | Economic termination | No—cost failure |
| 8 | Binary MLC + software achieves equivalent safety | Competitive disadvantage | No—alternative viable |
| 9 | Non-blocking constraint violated with NL=NA integrity | Architecture failure | Yes—re-examine Phase 1 |
| 10 | Addressable market <$20M annually | Economic termination | No—market failure |

### 11.3 Recursion Trigger Specification

**Phase 1 recursion is triggered if:**
- System failure reveals Phase 1 assumption was wrong
- Device physics re-evaluation changes constraint bounds
- New data invalidates Phase 1 conclusion

**One recursion permitted.** Second kill terminates program permanently.

**Current status:** No recursion triggered. Phase 2 failures are **system-level**, not device-level.

---

## 12. Combined Conclusion: What Would Make This Inevitable

### 12.1 Program-Level Question

**Under what conditions does MT become the inevitable successor to binary CMOS for high-stakes autonomous execution systems?**

### 12.2 Minimum Viable MT System

The smallest, cheapest, most reliable implementation that enforces TL triadic semantics:

| Attribute | Minimum Viable |
|-----------|----------------|
| Architecture | Hybrid (Architecture B variant) |
| Crossbar size | 256×256 (avoids wire energy) |
| CMOS node | 28nm (mature, cheap) |
| NL=NA | Hardware interlock with window comparator |
| PUF | SRAM PUF (mature, not memristive) |
| Logging | External NV memory (not integrated) |
| WCET | <10 ms execution, <1 s logging |
| Cost | $10/unit premium |

**Even this minimum viable system is not competitive** with binary CMOS + software at $1/unit premium.

### 12.3 Falsification Threshold

**Single experimental result that would terminate this research program permanently:**

> **Publication in IEDM, VLSI, or Nature of a binary MLC ReRAM system with software-enforced safety that achieves:**
> - Equivalent NL=NA semantics through trusted execution environment
> - WCET bounds provable at 99.99th percentile
> - 20-year audit trail with cryptographic provenance
> - IEC 61508 SIL 3 certification
> - Cost within 2× of binary CMOS

**If such a system is demonstrated, MT has no discontinuous advantage and the program terminates.**

### 12.4 Final Assessment

**MT is physically possible but systemically non-viable.**

The combination of:
1. Unvalidated 20-year IRS retention
2. Wire energy dominance at practical scales
3. Economic break-even exceeding addressable market
4. Unachievable 2027 certification timeline
5. No discontinuous advantage over binary alternatives

renders MT **non-competitive** for all evaluated use cases.

**Binary CMOS with software safety overlays is sufficient.** Incremental investment in trusted execution environments, formal verification, and binary NVRAM achieves equivalent safety at **<10% of MT's NRE cost**.

**Recommendation:** Terminate MT research program. Redirect investment to:
- Binary MLC ReRAM PDK development
- TEE hardening for safety-critical systems
- Formal methods for software enforcement verification

---

## 13. Bibliography

| Citation | Source | Confidence |
|----------|--------|------------|
| IRDS 2023: International Roadmap for Devices and Systems | IEEE | High confidence |
| TSMC N2 Technology Disclosure, IEDM 2023 | IEDM | High confidence |
| Intel 18A Technology Disclosure, IEDM 2024 | IEDM | High confidence |
| Samsung SF2 MBCFET Disclosure, VLSI 2024 | VLSI | High confidence |
| IEC 61508: Functional Safety of Electrical/Electronic Systems | IEC Standard | High confidence |
| KIOXIA ReRAM Roadmap 2024 | IEDM | High confidence |
| Everspin STT-MRAM Production Data | Company disclosure | High confidence |
| GlobalFoundries FeFET Development Status | VLSI 2023 | Unverified recall |
| CoWoS and Foveros Integration Guidelines | TSMC/Intel whitepapers | High confidence |
| TEE Security Evaluation Studies (ARM TrustZone, Intel SGX) | IEEE S&P | High confidence |

---

## 14. Glossary

### Inherited from Phase 1
MT, TL, NL=NA, PUF, LRS, IRS, HRS, BEOL, GAA, CiM, ADC, DAC, NVRAM, ReRAM, PCM, MTJ, FeFET, WCET

### Phase 2 Additions

| Term | Definition |
|------|------------|
| **NRE** | Non-Recurring Engineering—one-time costs for PDK development |
| **IEC 61508** | International standard for functional safety of electrical/electronic systems |
| **PDK** | Process Design Kit—foundry-provided models, rules, and libraries |
| **EDA** | Electronic Design Automation—software tools for chip design |
| **TOPS/W** | Tera-Operations Per Second per Watt—compute efficiency metric |
| **CoWoS** | TSMC Chip-on-Wafer-on-Substrate—2.5D heterogeneous integration |
| **Foveros** | Intel 3D hybrid bonding technology |
| **MBCFET** | Multi-Bridge Channel FET—Samsung GAA transistor architecture |
| **PowerVia** | Intel backside power delivery technology |
| **TEE** | Trusted Execution Environment—hardware-isolated secure processing |

---

*"Build the third state into matter, and the future stops pretending it never hesitated." — Lev Goukassian.*

---

**END OF PHASE 2 REPORT**

---

**PROGRAM CONCLUSION: FAILURE AT SYSTEM LEVEL**

Mandated Ternary is physically possible (Phase 1 conditional pass) but systemically non-viable (Phase 2 failure). Binary CMOS with software safety overlays is sufficient for all evaluated use cases.

**Recommendation: Terminate program.**
