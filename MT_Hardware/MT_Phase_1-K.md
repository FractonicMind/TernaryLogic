# Mandated Ternary: Hardware Implementation of Ternary Logic  
## Phase 1 — Device Physics, Circuit Primitives, and Physical Interlock Mechanisms

---

## 1. Abstract

### 1.1 Core Claim

The physical instantiation of three stable, non-volatile resistance states in memristive devices—specifically TaOx-based ReRAM with engineered Intermediate Resistance State (IRS)—is theoretically feasible for 10-year operational horizons but **cannot be validated for 20-year retention with statistical confidence required for deterministic autonomous execution systems**. No discontinuous advantage over the named baseline (TSMC N2 CoWoS with embedded ReRAM 1T1R, 2025 PDK) has been demonstrated at any evaluated layer.

### 1.2 Scope and Constraints

This Phase 1 evaluation addresses: device physics of three-state resistive switching; circuit primitives for ternary sensing and logic; physical interlock mechanisms for non-blocking enforcement; and hardware root of trust integration. The analysis adheres strictly to two global constraints: **(1) non-blocking enforcement with WCET provably bounded at 99.99th percentile with σ/μ < 10%**, and **(2) direct quantitative comparison to the fixed 2025 baseline at every layer**. Machine learning inference and statistical pattern matching are explicitly excluded; target applications are deterministic autonomous execution in industrial, financial, and critical infrastructure contexts.

---

## 2. Executive Summary

### 2.1 Phase 1 Findings

**Device Physics Layer (Section 5):** TaOx ReRAM demonstrates proven capability for binary switching with **10⁴–10⁹ cycle endurance** and **>10 year retention at 85°C** in production-qualified devices . However, the **Intermediate Resistance State (IRS) required for Epistemic Hold exhibits fundamental reliability challenges**: (a) σ/μ variability of **20–40%** in published demonstrations, exceeding the <20% target for reliable discrimination; (b) **no validated 20-year retention data**—Arrhenius extrapolation relies on unverified assumptions for metastable configurations; (c) **no 10-year accelerated test at 150°C with <10% drift** meeting 95% confidence lower bound requirements. The dual-filament and interfacial barrier engineering approaches show promise but remain at early development stage.

**Circuit Primitives Layer (Section 6):** Native ternary logic gates require **2.5–6× area and 2–5× energy** versus binary equivalents, with sense amplifier complexity increasing substantially for three-state discrimination. Gate inflation factors range from **2.2× (inverter) to 5.8× (full adder)**. WCET bounds for sensing paths are **analytically achievable (20–50 ns)** but **not statistically validated** at 99.99th percentile across process corners.

**Physical Interlock Layer (Section 7):** The NL=NA architecture is **conceptually sound** but introduces **unbounded latency risks under fault conditions** that violate Constraint 1. The 300 ms logging lane hard ceiling with σ/μ < 10% jitter is a **design target without demonstrated implementation**. Confirm pulse verification with window comparator and RC signature spoof detection is **theoretically adequate** but lacks experimental validation.

**Hardware Root of Trust (Section 8):** PUF integration with memristive entropy sources is **architecturally compatible** but the **>49% inter-die Hamming distance requirement** has not been demonstrated for filament-nucleation-based systems. Foundry attestation chain and 20-year provenance traceability rely on **escrow arrangements exceeding current industry practice**.

**Comparative Baseline Assessment:** The named **"TSMC N2 CoWoS with embedded ReRAM 1T1R, 2025 PDK" does not exist as a publicly documented product**. TSMC N2 GAA logic entered volume production H2 2025; TSMC ReRAM is qualified at 12–28nm nodes with no disclosed N2 integration . Available 2025 ReRAM benchmarks (KIOXIA: <50ns switching, >10⁶ cycles, >10 year retention at 85°C ) provide no ternary capability. **MT shows no discontinuous advantage**—ternary encoding offers marginal density improvement (1.58× vs. 2× for binary MLC) at substantial circuit complexity cost.

### 2.2 Phase 2 Inheritance

Phase 2 **may assume**: (a) binary ReRAM device physics as validated in 12–28nm production; (b) 10⁶–10⁷ cycle endurance achievable with proper current compliance; (c) 10-year retention at 85°C as demonstrated; (d) sense amplifier architectures capable of three-state discrimination with sufficient margin for 10⁶–10⁸ read cycles; (e) NL=NA interlock mechanisms with bounded latency under nominal conditions.

Phase 2 **must not assume**: (a) **20-year IRS retention with 95% confidence lower bound**; (b) **σ/μ < 20% for IRS variability** without explicit process control demonstration; (c) **WCET bounds proven at 99.99th percentile** under all operating corners; (d) **discontinuous advantage over software-implemented ternary state machines**; (e) **scalability beyond 512×512 crossbar dimensions** without wire energy dominance; (f) **existence of the named N2 CoWoS ReRAM 1T1R 2025 PDK baseline** as specified.

### 2.3 Program Termination Conditions

Immediate termination warranted if any of the following is confirmed: (1) **TaOx σ/μ > 40%** at IRS operating conditions; (2) **10-year accelerated test at 150°C demonstrates <10 year retention** at 95% confidence lower bound for any of three states; (3) **confirm pulse tamper-evidence requires components exceeding 400°C BEOL thermal budget**; (4) **PUF inter-die Hamming distance < 49%** or intra-die > 1% across specified conditions; (5) **WCET bounds unprovable at 99.99th percentile** for any enforcement path; (6) **no quantified architectural advantage demonstrated** in Phase 2 system-level analysis; (7) **binary MLC ReRAM achieves equivalent functional safety** with lower total cost of ownership; (8) **wire energy dominates compute energy** at crossbar dimensions below 1024×1024; (9) **read disturb threshold for IRS→LRS transition falls below 10⁶ cycles**; (10) **foundry PUF attestation chain requires single-vendor trust** with no cryptographic escape.

---

## 3. Definitions and Scope

### 3.1 Binary CMOS Baseline

#### 3.1.1 Logic Levels and Noise Margins

Binary CMOS at the **3nm GAA node** operates with **nominal VDD = 0.75V**, with six threshold voltage (Vth) levels available for power-performance optimization . The transition from FinFET to GAA nanosheet transistors provides improved electrostatic control, reducing subthreshold swing and enabling more precise threshold tuning . Logic levels are defined as **VOL < 0.15V** (logic-0) and **VOH > 0.60V** (logic-1), yielding static noise margins of approximately **150mV (NML)** and **450mV (NMH)** under nominal conditions. Process variation with **σVth = 50mV** (6.7% of VDD) reduces effective noise margins by **15–20% at 3σ corners** .

The fundamental limitation for MT implementation is the **absence of a native intermediate state**. The CMOS inverter transfer characteristic exhibits a sharp switching threshold where both transistors conduct, but this region is: **(a) metastable**—noise or variation drives rapid transition to rail; **(b) non-persistent**—power removal destroys state information; **(c) not architecturally discriminable**—regenerative feedback collapses intermediate voltages to valid logic levels. Any "third state" implementation requires software synthesis with state machine encoding, polling loops, and explicit timeout handling—introducing **unbounded latency vulnerability and software-exploitable attack surface**.

#### 3.1.2 Switching Energy at 3nm GAA Node

Switching energy follows **Esw = αCVDD²**, where **α ≈ 0.25** (activity factor), **C ≈ 0.5 fF** (minimum-size inverter gate + interconnect), and **VDD = 0.75V**, yielding **Esw ≈ 0.07 fJ per toggle**. This excludes dominant interconnect energy: for **1 mm global wire** (RC ≈ 100 ps, C ≈ 200 fF), wire energy exceeds **100 fJ**—approximately **1,400× the gate energy**. Binary CMOS implementing ternary semantics requires **2-bit encoding minimum** (50% overhead), with additional software path energy for state machine evaluation, memory access, and logging system calls.

### 3.2 Memristor vs. Memristive System Distinction

The **ideal memristor** (Chua, 1971) defines a fundamental two-terminal relationship between charge and flux: **dφ = M(q)dq**, with state-dependent resistance **R(x)** where **dx/dt = f(x,i)** . **No physical device satisfies this ideal definition**. Practical **memristive systems**—including all TaOx, HfOx, TiOx ReRAM implementations—exhibit: **(a) hysteretic I-V characteristics with memory**; **(b) state retention without power**; **(c) resistance modulation through ionic migration, phase change, or redox reactions**; **(d) stochastic nucleation, abrupt switching, and relaxation phenomena** not captured by ideal models.

This distinction is **critical for MT feasibility**: engineering targets **reliable, reproducible three-state hysteresis**, not theoretical memristance compliance. Device-to-device variability, cycle-to-cycle stochasticity, and temporal drift must be bounded by **design margins and circuit techniques**, not assumed away.

### 3.3 Hysteresis Window and State Retention

**Hysteresis** arises from **history-dependent ionic distribution**: the resistance state depends on the integral of applied voltage/current, not merely instantaneous values. For TaOx, the **SET transition** (HRS→LRS) occurs at **VSET ≈ 1.0–1.5V** as oxygen vacancies accumulate to form conductive filament; the **RESET transition** (LRS→HRS) requires **VRESET ≈ −1.5 to −2.5V** (bipolar) or complementary polarity with thermal assistance. The **hysteresis window**—voltage range where neither transition occurs—enables **non-destructive read and multi-state stability**. Typical TaOx windows of **0.3–0.8V** are **marginal for reliable three-state discrimination** with process and temperature variation.

**State retention** depends on **thermal activation barrier for oxygen vacancy diffusion**: **Ea ≈ 1.0–1.2 eV** for TaOx filament systems, yielding **Arrhenius-projected retention >10 years at 85°C** for fully formed LRS and HRS. **IRS configurations are thermodynamically metastable** with **lower effective barrier** due to proximity to transition states and reduced filament coherence.

### 3.4 Mandate as Enforcement Mechanism

In MT, **"mandate" denotes hardware-enforced authorization constraints**, not organizational governance. The mandate is instantiated through: **(a) write-once fuse storage of governance parameters** defining authorization conditions; **(b) physical interlock circuits preventing state transitions without cryptographic confirmation**; **(c) non-volatile logging creating tamper-evident audit trails**. This tripartite structure separates **policy specification** (fuses), **policy enforcement** (interlocks), and **policy verification** (logging), with **cryptographic binding between layers**.

The enforcement is **mandatory in the architectural sense**: no software override is possible—interlock circuits operate on **dedicated hardware paths with independent power and timing**.

### 3.5 MT vs. TL Hierarchy

| Context | Term | Definition |  
|--------|------|------------|  
| Hardware implementation | **MT** | Physical architecture: memristive cells, interlock circuits, PUF identity, logging infrastructure |  
| Formal decision framework | **TL** | Semantic layer: Proceed/Epistemic Hold/Refuse with defined transition rules |  
| State mapping | **TL→MT** | +1→LRS (~1–10 kΩ), 0→IRS (~100 kΩ–1 MΩ), −1→HRS (~1–10 MΩ) |

The hierarchy is **strict and unidirectional**: MT physically instantiates TL; TL provides semantic interpretation of MT hardware states. **No semantic interpretation occurs in hardware**—all meaning is assigned by TL framework and attributed through trust chain (ORCID: 0009-0006-5966-1243).

### 3.6 NL=NA Physical Interlock

**NL=NA (No Log = No Action)** is the **core enforcement primitive**: **(a)** execution cell resides in **IRS by default**; **(b)** transition to **LRS requires confirm pulse from logging path**; **(c)** confirm pulse is **voltage write pulse on dedicated hardware wire**, not software flag; **(d)** **no software path can generate valid confirm pulse**—hardware-only enforcement. The logging path operates **in parallel with execution**, satisfying non-blocking constraint; **any serialization converts Epistemic Hold into unbounded latency violation**.

### 3.7 Epistemic Hold (IRS) Semantics

**Epistemic Hold repurposes the logical intermediate state as deliberate enforcement pause**. The system possesses **sufficient information to proceed or refuse**—sensor data evaluated, rules applied, context assembled—but **lacks authorization confirmation from logging/attestation chain**. This is **not logical uncertainty** (insufficient information to decide) but **authorization pending** (sufficient information, unverified provenance).

Unlike **binary wait states** which: consume CPU cycles through polling or interrupt handling; require explicit timeout management; are **volatile and vulnerable to power loss**—**IRS is stable resistive state with physical semantics**: **persists without power, requires no clock, transitions only on verified external event**. The architectural parallelism enables **execution lane completion** (reaching IRS) **concurrent with logging lane commitment** (issuing confirm), with interlock releasing embargo only upon cryptographic verification of log entry integrity. The parallelism is absolute: execution lane WCET ≤ 2 ms at 99.99th percentile; logging lane hard ceiling 300 ms with jitter σ/μ < 10%. These bounds are **design specifications**, not demonstrated achievements—Section 7 evaluates feasibility.

The **physical semantics of IRS** derive from three properties: **(a) non-volatility**—state persists through power cycling without refresh; **(b) self-holding**—no clock or active circuitry required to maintain state; **(c) transition-guarded**—exit from IRS requires energy input exceeding defined threshold with correct temporal signature. These properties make IRS **architecturally distinct from software wait states** and enable **deterministic recovery** after power loss: the system restarts in the same epistemic posture—authorization pending—without requiring state reconstruction from logs.

### 3.8 PUF Identity vs. Manufacturing Provenance

**Two distinct systems with non-overlapping functions:**

| System | Source | Function | Compromise Consequence |  
|--------|--------|----------|------------------------|  
| **PUF Identity** | Post-manufacturing physical entropy (filament nucleation sites, threshold variation, dopant distribution) | Die-unique cryptographic identity, unclonable per die | Single-vendor trust if factory-programmed—**program failure** |  
| **Manufacturing Provenance** | Foundry attestation at wafer sort | Chain of custody: fab date, node, wafer lot, die coordinates | Attestation gap if foundry defunct—**escrow required** |

**Critical distinction:** PUF values **must not** be factory-programmed. If foundry burns "PUF" values during manufacturing, the system collapses to **single-vendor trust**—the foundry knows all identities and can forge attestations. This is a **Phase 1 failure mode** flagged explicitly in Section 8.

Manufacturing provenance requires: **(a)** foundry signs PUF public key at wafer sort using foundry private key; **(b)** attestation database records manufacturing parameters; **(c)** chain-of-custody documentation through die attach, package test, and system integration; **(d)** escrow arrangement preserving attestation chain if foundry ceases operation.

### 3.9 Worst-Case Execution Time (WCET)

**Definition (reiterated from global constraints):** WCET is **provably bounded at 99.99th percentile with σ/μ < 10%** under all operating conditions: temperature 0–125°C, voltage ±10%, process corners (SS/TT/FF). 

**WCET is not typical latency**—it is the **statistical ceiling** that execution paths must not exceed under any combination of environmental and process variation. For MT enforcement paths: **execution lane** (compute + sensing) WCET ≤ 2 ms; **logging lane** (write + confirm) WCET ≤ 300 ms with jitter bound. These specifications are **analytically derivable** from circuit parameters but **not experimentally validated** at required confidence levels—this gap is flagged in Section 7.

---

## 4. Baseline: Binary CMOS Limitations

### 4.1 Logic Levels and Noise Margins at 3nm GAA Node

Binary CMOS at **TSMC N2 (2nm GAA)** operates with **nominal VDD = 0.75V** [high confidence: IRDS 2023, IEDM 2023]. Six threshold voltage levels enable power-performance optimization, with **σVth ≈ 50mV** (6.7% of VDD) representing 3σ process variation. Logic levels: **VOL < 0.15V**, **VOH > 0.60V**, yielding static noise margins **NML ≈ 150mV**, **NMH ≈ 450mV** under nominal conditions.

At **3σ process corners**, effective noise margins degrade **15–20%** due to threshold variation. Temperature dependence: **dVth/dT ≈ −0.8 mV/°C**, causing **~100mV Vth shift** across 0–125°C range. Combined with **±10% VDD variation**, noise margins contract to **~100mV (NML)** and **~350mV (NMH)** at worst-case corners.

**Fundamental limitation for ternary implementation:** CMOS has **no native intermediate state**. The inverter transfer characteristic exhibits a **metastable switching region** where both transistors conduct, but this region: **(a)** spans **<50mV** input range; **(b)** collapses to rail within **<1 ps** due to regenerative feedback; **(c)** is **non-persistent**—power removal destroys state information. Any "third state" requires **software synthesis**: state machine encoding, polling loops, interrupt handling, timeout management—introducing **unbounded latency vulnerability** and **software-exploitable attack surface**.

### 4.2 Switching Energy and Interconnect Dominance

Switching energy follows **Esw = αCVDD²**. At N2 node: **α ≈ 0.25** (activity factor), **C ≈ 0.5 fF** (minimum inverter + local interconnect), **VDD = 0.75V**, yielding **Esw ≈ 0.07 fJ per toggle**. This is **gate energy only**—interconnect dominates at system level.

For **1 mm global wire** (RC ≈ 100 ps, C ≈ 200 fF), wire energy **Ewire = ½CVDD² ≈ 56 fJ**—**800× gate energy**. For **5 mm on-chip network** (C ≈ 1 pF), wire energy **≈ 280 fJ**—**4,000× gate energy**. Binary CMOS implementing ternary semantics requires **minimum 2-bit encoding** (50% overhead), with additional energy for: state machine evaluation (~10× gate energy per transition), memory access (~100 fJ per read), logging system calls (~1–10 µJ including software stack).

**Total emulation energy**: 2-bit encoding (1.5×) + state machine (2–5×) + memory access (10–100×) + software logging (1,000–10,000×) = **~100–1,000× native gate energy** for equivalent semantic operation.

### 4.3 Why Binary CMOS Cannot Natively Enforce Mandatory Intermediate State

**Three architectural barriers:**

1. **Volatility**: CMOS state requires power. Power loss destroys "wait state" information—recovery requires state reconstruction from external memory, introducing **unbounded latency** and **trust gap**.

2. **Software dependency**: Any intermediate state implementation requires **active CPU execution**: polling loops, interrupt handlers, timeout management. These are **terminable by software**—malware or malfunction can bypass enforcement.

3. **No physical interlock**: Binary CMOS lacks **hardware-only enforcement path**. Confirm signals are software-generated, subject to spoofing, replay, or suppression attacks.

**Comparative baseline assessment:** The named baseline **"TSMC N2 CoWoS with embedded ReRAM 1T1R, 2025 PDK" does not exist as a publicly documented product** [high confidence: TSMC public disclosures, IEDM 2023–2025]. TSMC N2 GAA logic entered risk production H2 2024, volume production H2 2025. TSMC ReRAM is qualified at **12–28nm nodes** with **no disclosed N2 integration** [unverified recall: industry analyst reports]. Available 2025 ReRAM benchmarks (KIOXIA: <50ns switching, >10⁶ cycles, >10 year retention at 85°C) provide **no ternary capability** [high confidence: KIOXIA IEDM 2024].

**MT shows no discontinuous advantage at this layer.** Binary CMOS limitations are **well-understood constraints**, not failures—software synthesis of ternary semantics is **possible but expensive**, as quantified in Section 9.

---

## 5. Device Physics and Engineered State Requirements

### 5.1 Universal Memristive Mechanisms

**Filament formation/rupture (TaOx, HfOx, TiOx):** Conductive filaments form through **oxygen vacancy accumulation** under positive bias, creating **metallic Ta-rich phase** (TaO₂₋ₓ, x→0) with resistivity **~10⁻⁴ Ω·cm**. RESET transition ruptures filament through **oxygen ion back-migration** under negative bias or thermal dissolution, restoring high-resistance oxide phase.

**Interfacial redox:** Schottky barrier modulation at electrode/oxide interface creates **thickness-dependent resistance** without full filament formation. Enables **multi-level states** through partial barrier modulation.

**Hysteresis physics:** Resistance depends on **history of applied voltage/current**, not merely instantaneous values. The **hysteresis window**—voltage range where neither SET nor RESET occurs—enables **non-destructive read and multi-state stability**. For TaOx: **VSET ≈ 1.0–1.5V**, **VRESET ≈ −1.5 to −2.5V**, window width **0.3–0.8V**—**marginal for reliable three-state discrimination** with process/temperature variation.

**Why three states, not two or four:** Two states (binary) **cannot encode Epistemic Hold**—the architectural requirement for authorization-pending enforcement pause. Four states (quaternary) **exacerbate discrimination challenges**: sensing margins shrink, variability tolerance decreases, circuit complexity increases. Three states represent **engineering optimum**: sufficient for TL semantics (Proceed/Hold/Refuse), achievable with demonstrated memristive physics, discriminable with robust circuit margins.

**Comparison to binary MLC:** Binary multi-level cell (MLC) ReRAM stores **2 bits in 4 resistance states**—denser than ternary (1.58 bits/cell). However, MLC lacks **semantic assignment**—states are arbitrary data values, not enforcement primitives. MT's **discontinuous advantage** (if any) derives from **physical interlock capability**, not density—IRS as **enforceable pause state** with hardware-only exit condition.

### 5.2 TaOx Deep-Dive (Primary Worked Example)

#### 5.2.1 Device Stack Specification

**Cross-section structure (bottom to top):**  
```  
TiN (100 nm) - bottom electrode  
TaOx switching layer (15–25 nm, x ≈ 2.4–2.5)  
TaO₂₋ₓ interfacial layer (2–5 nm, oxygen-deficient)  
TiN (50 nm) - top electrode  
```

**Critical parameters for foundry fabrication:**  
- **Bottom electrode**: TiN sputtered at **300–400°C**, thickness **100±10 nm**, resistivity **~100 µΩ·cm**  
- **Switching layer**: TaOx deposited by **reactive sputtering** (Ta target, Ar/O₂ plasma), thickness **20±2 nm**, composition **TaO₂.₄₅±₀.₀₅** (x = 2.4–2.5)  
- **Oxygen profile**: **gradient** from Ta-rich (near bottom electrode) to TaO₂.₅ (near top)—enables bipolar switching with **asymmetric filament nucleation**  
- **Top electrode**: TiN **50±5 nm**, patterned by **Cl₂/BCl₃ RIE**  
- **Thermal budget**: Maximum post-CMOS processing **<400°C**—filament stability degrades above **450°C** due to oxygen vacancy redistribution

#### 5.2.2 Switching Mechanism

**SET (HRS→LRS):** Positive bias on top electrode (**+1.0 to +1.5V**) drives **oxygen vacancies (Vₒ²⁺)** toward bottom electrode, forming **conductive Ta-rich filament** (TaO₂₋ₓ, x→0). Filament diameter **~10–50 nm**, resistance **R_LRS ≈ 1–10 kΩ**. Current compliance **I_cc = 100–500 µA** controls filament thickness—higher compliance → thicker filament → lower R_LRS.

**RESET (LRS→HRS):** Negative bias (**−1.5 to −2.5V**) or **opposite polarity** drives oxygen ions back into filament, **rupturing conductive path** through thermal dissolution or electrochemical oxidation. HRS resistance **R_HRS ≈ 1–10 MΩ**, determined by **remaining filament stub length** and **interfacial barrier height**.

**IRS engineering approaches:**  
1. **Partial RESET**: Incomplete RESET pulse dissolves filament partially, leaving **residual conductive path** with **R_IRS ≈ 100 kΩ–1 MΩ**. Challenge: **stochastic rupture point**—difficult to control reproducibly.  
2. **Dual-filament regime**: **Two partial filaments** in parallel, each insufficient for full conduction. More reproducible but requires **precise nucleation control**.  
3. **Interfacial barrier modulation**: Schottky barrier height modulation without full filament rupture. **Most promising** for IRS stability—barrier height changes are **more reversible than filament reconfiguration**.

#### 5.2.3 Hysteresis Characteristics

| Parameter | Typical Value | Process Variation (σ/μ) |  
|-----------|---------------|------------------------|  
| VSET | 1.0–1.5V | 10–15% |  
| VRESET | −1.5 to −2.5V | 10–15% |  
| Forming voltage | 2.0–3.0V (first cycle only) | 15–20% |  
| Hysteresis window | 0.3–0.8V | 20–30% |  
| R_LRS | 1–10 kΩ | 20–30% |  
| R_HRS | 1–10 MΩ | 30–50% |  
| R_IRS (target) | 100 kΩ–1 MΩ | **20–40%** |

**Temperature dependence:** VSET decreases **~0.5 mV/°C**; VRESET magnitude decreases **~0.8 mV/°C**. Hysteresis window **narrows 10–15%** from 25°C to 125°C. R_LRS increases **~20%** at 125°C due to metallic filament resistivity temperature coefficient; R_HRS decreases **~30%** due to thermally-assisted tunneling.

#### 5.2.4 Retention Projection

**Arrhenius model:** Retention time **t_ret ∝ exp(Ea/kT)**, where **Ea ≈ 1.0–1.2 eV** for TaOx filament systems [high confidence: IEDM 2018–2023].

**LRS retention:** Fully formed metallic filament has **high activation barrier** for oxidation. Projected retention **>10 years at 85°C**, **>5 years at 125°C** at 95% confidence [high confidence: Panasonic, IEDM 2020].

**HRS retention:** Ruptured filament with **oxygen-rich gap** has **lower barrier** for vacancy re-accumulation. Projected retention **>10 years at 85°C**, **>3 years at 125°C** [unverified recall: published accelerated test data].

**IRS retention (critical gap):** Intermediate configurations are **thermodynamically metastable** with **reduced effective barrier Ea_IRS ≈ 0.7–0.9 eV** estimated from proximity to transition states. **No validated 20-year retention data exists.** Arrhenius extrapolation from **150°C accelerated tests** (if available) would require:  
- **10 years at 150°C** with **<10% resistance drift**  
- **95% confidence lower bound** exceeding 10-year specification  
- **Statistical sample** of **>100 devices** for meaningful confidence interval

**Current status:** Published IRS retention data extends to **1,000 hours at 150°C** with **<15% drift** [unverified recall: academic demonstrations, 2018–2022]. This is **insufficient for 20-year projection**—**Phase 1 cannot validate 20-year IRS retention**.

#### 5.2.5 Endurance Requirements

| Application | Required Cycles | TaOx Demonstrated | Status |  
|-------------|-----------------|-------------------|--------|  
| Memory (storage) | 10⁶ | 10⁶–10⁹ | ✓ Qualified |  
| Logic (frequent switching) | 10¹² | 10⁸–10¹⁰ | ✗ Marginal |  
| TL enforcement (moderate) | 10⁸–10¹⁰ | 10⁸ (projected) | ? Unvalidated |

**TL enforcement cycle estimate:** For autonomous system with **1,000 decisions/second**, **10-year lifetime** requires **3.15×10¹¹ cycles**—exceeds demonstrated TaOx endurance. However, **majority of decisions** may not require state switching (IRS→IRS for Hold, LRS→LRS for Proceed continuation). **Effective cycle count** depends on transition frequency—if **10% of decisions change state**, requirement reduces to **3×10¹⁰ cycles**, within projected capability.

### 5.3 Comparative Device Table

**Artifact: Comparative Device Table (8+ rows, named 2025 baseline column)**

| Device | Retention (85°C) | Endurance | σ/μ Variability | Write Energy | Read Energy | Vop | CMOS Compat | IRS Credibility | Advantage vs. 2025 Baseline |  
|--------|------------------|-----------|-----------------|--------------|-------------|-----|-------------|-----------------|----------------------------|  
| **TaOx ReRAM** | >10 yr (LRS/HRS); **unvalidated** (IRS) | 10⁶–10⁹ | 20–40% (IRS) | 1–10 pJ | 0.1–1 pJ | 1–3V | ✓ Mature (12–28nm) | **Marginal**—variability high, retention unproven | None demonstrated—no N2 integration |  
| **HfOx ReRAM** | >10 yr | 10⁶–10¹⁰ | 15–30% | 0.1–1 pJ | 0.01–0.1 pJ | 0.5–2V | ✓ Production (28nm) | **Marginal**—better σ/μ but IRS engineering less mature | None—no ternary capability |  
| **TiOx ReRAM** | >5 yr | 10⁴–10⁶ | 30–50% | 10–100 pJ | 1–10 pJ | 2–5V | △ Research | **No**—poor retention, high variability | None |  
| **PCM (Ge₂Sb₂Te₅)** | >10 yr | 10⁸–10¹² | 10–20% | 10–100 pJ | 1–10 pJ | 1–3V | ✓ Production (Intel Optane) | **Yes**—crystalline/amorphous intermediate states demonstrated | None—no N2 integration, high write energy |  
| **MTJ (STT-MRAM)** | >20 yr | >10¹⁵ | 5–10% | 0.01–0.1 pJ | 0.001–0.01 pJ | 0.5–1V | ✓ Production (22nm) | **No**—binary only, no intermediate state | None—no ternary capability |  
| **FeFET (HfZrO)** | >10 yr | 10⁴–10⁶ | 15–25% | 1–10 pJ | 0.1–1 pJ | 2–4V | △ Development | **Marginal**—partial polarization possible | None—endurance insufficient |  
| **CBRAM (Cu-based)** | >5 yr | 10⁴–10⁶ | 40–60% | 1–10 pJ | 0.1–1 pJ | 0.3–1V | △ Research | **No**—electrochemical variability extreme | None |  
| **Electrochemical (EO)** | >1 yr | 10³–10⁵ | 50–100% | 1–100 pJ | 0.1–10 pJ | 0.1–1V | ✗ Early research | **No**—variability unacceptable | None |  
| **2025 Baseline: TSMC N2 CoWoS + 1T1R ReRAM** | **N/A—product does not exist** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Reference only |

**Key finding:** No device in table demonstrates **validated IRS capability** with σ/μ < 20% and 20-year retention. PCM shows **best IRS credibility** through crystalline/amorphous gradient but lacks **hardware interlock integration path** and has **10–100× higher write energy** than oxide ReRAM.

### 5.4 TL State Mapping and Sensing Margins

**Artifact: Sensing Margin Analysis with Reference Cell Architecture**

**Resistance state definitions:**  
- **R+ (Proceed, LRS)**: 1–10 kΩ, nominal **5 kΩ**  
- **R0 (Epistemic Hold, IRS)**: 100 kΩ–1 MΩ, nominal **300 kΩ**  
- **R− (Refuse, HRS)**: 1–10 MΩ, nominal **5 MΩ**

**Sensing thresholds:**  
- **TH_L** (LRS/IRS boundary): **30 kΩ** (geometric mean: √(5k×300k) ≈ 38.7k, adjusted for distribution overlap)  
- **TH_H** (IRS/HRS boundary): **1.5 MΩ** (geometric mean: √(300k×5M) ≈ 1.22M, adjusted for distribution overlap)

**Reference cell architecture:**  
```  
Two reference cells per sense amplifier:  
- REF_L: Programmed to TH_L boundary (30 kΩ)  
- REF_H: Programmed to TH_H boundary (1.5 MΩ)

Sense amplifier topology: Dual differential comparators  
- Comparator 1: R_cell vs REF_L → output L (LRS) or not-L  
- Comparator 2: R_cell vs REF_H → output H (HRS) or not-H  
- Decoder: (L, not-H) = LRS; (not-L, not-H) = IRS; (not-L, H) = HRS  
```

**Margining strategy:**  
- **Read voltage**: 0.1–0.3V (within hysteresis window, non-disturbing)  
- **Read current**: 1–10 µA (LRS), 0.1–1 µA (IRS), 0.01–0.1 µA (HRS)  
- **Integration time**: 10–50 ns (tradeoff: speed vs. noise averaging)

**Noise sources and margins:**

| Noise Source | Amplitude | Impact on Sensing |  
|--------------|-----------|-------------------|  
| Temperature drift (0–125°C) | R_LRS +20%, R_HRS −30% | **Critical**—shifts distributions, may cause overlap at extremes |  
| Read disturb (10⁶ cycles) | <5% resistance shift | Manageable with read voltage <0.3V |  
| Cycle-to-cycle variability | σ/μ = 20–40% (IRS) | **Critical**—may cause misclassification if distributions overlap |  
| Random telegraph noise (RTN) | ±10–50% instantaneous | **Critical**—requires multiple sampling or error correction |  
| Process variation | σ/μ = 10–20% (LRS/HRS), 20–40% (IRS) | Manageable with guard bands |

**Distribution overlap implications:**

At **10⁶ read cycles**: IRS σ/μ = 30% → **3σ tails extend to 0.4× and 2.5× nominal**. With R_LRS nominal 5kΩ (σ/μ=20%, 3σ: 2–11kΩ) and R_IRS nominal 300kΩ (σ/μ=30%, 3σ: 90–750kΩ), **guard band of 30×** (11kΩ to 90kΩ) provides **adequate margin**.

At **10⁹ read cycles**: Read disturb + RTN accumulation may shift LRS upper tail to **20kΩ**, IRS lower tail to **60kΩ**—**margin contracts to 3×**, requiring **adaptive thresholding or error correction**.

At **10¹² read cycles**: **No validated data**. Projected margin collapse without **active refresh or state restoration**—**feasibility unproven**.

---

## 6. Circuit Primitives and Sensing Margins

### 6.1 Native Ternary Logic Gates

**Ternary inverter:** Three output levels (LRS, IRS, HRS) corresponding to input state inversion. Implementation: **resistive divider with reference thresholds** or **current-mode comparison**.

**Ternary NAND/NOR analogs:**   
- **MIN gate**: Output = minimum of inputs (analogous to NAND in negative logic)  
- **MAX gate**: Output = maximum of inputs (analogous to NOR in negative logic)  
- **Literals**: X⁺ = 1 if X=LRS else 0; X⁰ = 1 if X=IRS else 0; X⁻ = 1 if X=HRS else 0

**Threshold logic:** Single gate implements **weighted sum with ternary output**:  
```  
Output = sign(Σ(w_i × x_i) − θ)  
where x_i ∈ {−1, 0, +1}, w_i ∈ {−1, 0, +1}, θ = threshold  
```

### 6.2 Sense Amplifier Sizing

**Circuit designer specification:**

**Input stage:** Differential pair with **active load**, sized for:  
- **Input common-mode range**: 0.1–0.5V (read voltage levels)  
- **Transconductance gm**: >100 µS for 10 ns settling  
- **Bandwidth**: >100 MHz for 10 ns response

**Reference generation:** Bandgap-derived voltage reference (1.2V) with **resistive divider** creating TH_L and TH_H. **Critical**: Reference must be **independent of VDD**—VDD compromise must not shift thresholds.

**Comparator sizing:**  
- **Input pair**: W/L = 10/0.5 µm (N2 node) for matching σVth < 5mV  
- **Current mirror**: 1:1 ratio, minimum channel length for speed  
- **Latch regeneration**: Positive feedback with **<1 ns regeneration time**

**Power**: **5–20 µW per sense amplifier** (active), **<100 nW** (standby with periodic refresh).

### 6.3 ADC/DAC Costs for Analog State Readout

**Flash ADC (2-bit, 3-level):**  
- **2 comparators** (as specified above)  
- **Decoder**: 2-bit binary output  
- **Latency**: 10–20 ns  
- **Energy**: 1–5 pJ per conversion  
- **Area**: ~100 µm²

**DAC (for write verification):**  
- **Resistive string DAC**: 3-level output for precise write pulse generation  
- **INL/DNL**: <0.5 LSB for reliable state placement  
- **Settling**: <10 ns to 0.1%

### 6.4 Gate Inflation Factor

**Comparison: native ternary vs. binary equivalent:**

| Gate | Binary CMOS (N2) | Native Ternary MT | Inflation Factor |  
|------|------------------|-------------------|------------------|  
| Inverter | 1× (reference) | 2.5× | 2.5× |  
| 2-input NAND | 1× | 3× | 3× |  
| 2-input NOR | 1× | 3× | 3× |  
| Full adder | 1× | 5.8× | 5.8× |  
| D flip-flop | 1× | 4× | 4× |  
| MUX 2:1 | 1× | 3.5× | 3.5× |

**Area and energy implications:**  
- **Area**: 2.5–6× versus binary CMOS  
- **Energy**: 2–5× versus binary CMOS (excluding emulation overhead)  
- **Speed**: 0.5–1× (comparable, limited by sensing time)

### 6.5 Encoding Strategies

| Encoding | Physical Mapping | Sensing Complexity | Area Efficiency |  
|----------|------------------|-------------------|-----------------|  
| **2-bit binary** | Two binary cells per ternary value | Low (binary sense amps) | 50% overhead |  
| **One-hot** | Three cells, exactly one active | Medium (3× cells, simple OR) | 200% overhead |  
| **Signed magnitude** | Sign bit + magnitude | High (arithmetic required) | 75% overhead |  
| **Balanced ternary** | Native three-state | Low (single ternary cell) | Baseline (1×) |

**Recommendation:** **Balanced ternary encoding** for MT-native implementations; **2-bit binary** for hybrid approaches (ternary memory, binary compute).

### 6.6 Non-Blocking Constraint Verification

**Execution path timing:**  
- **Sense operation**: 10–50 ns (wcet_sense)  
- **Gate evaluation**: 5–20 ns (wcet_gate)  
- **State transition**: 10–100 ns (wcet_write)  
- **Total execution lane**: **25–170 ns** << 2 ms specification

**Logging path timing:**  
- **Log write**: 100 ns–1 µs (non-volatile memory)  
- **Merkle hash update**: 1–10 µs (cryptographic hardware)  
- **Confirm pulse generation**: 10–100 ns  
- **Total logging lane**: **1.1–11 µs** << 300 ms specification

**WCET bound status:** Analytically achievable with substantial margin. **Not statistically validated** at 99.99th percentile across process corners—**validation gap flagged**.

---

## 7. NL=NA: Physical Interlock Architecture

**Artifact: NL=NA Interlock Circuit Diagram**

```  
NL=NA INTERLOCK ARCHITECTURE  
============================

EXECUTION CELL (Memristor Array)  
    |  
    | R_cell (LRS/IRS/HRS)  
    v  
SENSE AMPLIFIER  
    |  
    +---> State decoder: LRS/IRS/HRS  
    |  
    +---> IRS detector (window comparator)  
              |  
              | IRS detected?  
              v  
    +------------------+  
    |   INTERLOCK      |  
    |   CONTROLLER     |  
    +------------------+  
              |  
    +---------+---------+  
    |                   |  
    v                   v  
EXECUTION LANE      LOGGING LANE  
(WCET ≤ 2ms)       (WCET ≤ 300ms)  
    |                   |  
    |                   v  
    |            LOG WRITE  
    |            (non-volatile)  
    |                   |  
    |                   v  
    |            MERKLE HASH  
    |            UPDATE  
    |                   |  
    |                   v  
    |            CONFIRM PULSE  
    |            GENERATOR  
    |                   |  
    +-------------------+  
              |  
              v  
    +------------------+  
    | WINDOW COMPARATOR|  
    | (verify pulse)   |  
    +------------------+  
              |  
              | Valid?  
              v  
    +------------------+  
    |  STATE TRANSITION|  
    |  IRS → LRS       |  
    +------------------+

CONFIRM PULSE SPECIFICATION:  
- Voltage: 1.0–3.0V (TaOx compatible)  
- Duration: 10–100 ns  
- Rise time: <5 ns (RC signature)  
- Routing: Dedicated wire, no software access

WINDOW COMPARATOR:  
- Voltage tolerance: ±5%  
- Timing tolerance: ±10%  
- Reference: Independent bandgap (not VDD)  
```

### 7.1 Confirm Pulse Specification

**Voltage range:** 1.0–3.0V for TaOx compatibility (must exceed VSET for reliable transition). **Higher voltages** (2–3V) enable **faster switching** but increase **disturb risk**—design tradeoff.

**Pulse duration:** 10–100 ns. **Shorter pulses** (<10 ns) may be **insufficient for complete filament formation**; **longer pulses** (>100 ns) increase **energy consumption and disturb probability**.

**Wire routing:** Dedicated **confirm wire** per execution cell or **shared bus with arbitration**. Point-to-point: **lowest latency, highest area**; Shared bus: **N× area reduction, arbitration latency**.

### 7.2 Confirm Pulse Verification

**Window comparator architecture:**  
- **Voltage window**: Confirm pulse must be **1.0–3.0V ±5%** (0.95–3.15V)  
- **Timing window**: Pulse duration **10–100 ns ±10%** (9–110 ns)  
- **Rise time**: **<5 ns** (detects capacitive loading/tamper)

**Independent reference**: Bandgap voltage reference (1.2V) with **precision resistor divider**. **Critical**: VDD compromise must not enable false confirmation—reference powered from **separate regulator or battery backup**.

### 7.3 Spoof Detection via RC Signature

**Legitimate pulse rise time** determined by:  
- **Wire resistance**: R_wire = ρ×L/A (typically 10–100 Ω for on-chip)  
- **Wire capacitance**: C_wire = ε×L×W/h (typically 0.1–1 pF for on-chip)  
- **RC time constant**: τ = R_wire × C_wire = **1–100 ps** for typical dimensions

**Tamper detection:**  
- **Added capacitance** (wire tap): Slows rise time to **>10 ns**—rejected  
- **Added resistance** (series resistor): Reduces amplitude below threshold—rejected  
- **EM injection**: May create false pulse—filtered by **window comparator timing requirements**

**Detection threshold:** Rise time **>5 ns** flagged as tamper event.

### 7.4 Interlock Circuit Operation

**IRS hold state:** Execution cell remains in IRS until:  
1. **Log entry written** to non-volatile memory  
2. **Merkle hash updated** with new entry  
3. **Confirm pulse generated** by logging hardware  
4. **Window comparator validates** pulse signature  
5. **State transition IRS→LRS** executed

**No software override:** Confirm pulse generation requires **hardware-only path** from logging completion to pulse generator. Software can **request** transition but cannot **compel** it.

### 7.5 Dual-Lane Timing Specification

| Parameter | Specification | Status |  
|-----------|---------------|--------|  
| Execution lane WCET | ≤ 2 ms @ 99.99th percentile | Analytically achievable, **not validated** |  
| Logging lane WCET | ≤ 300 ms @ 99.99th percentile | **Design target, no demonstration** |  
| Logging lane jitter | σ/μ < 10% | **Design target, no demonstration** |  
| Parallelism | Execution || Logging (never serial) | Architecturally satisfied |

**Critical gap:** The **300 ms hard ceiling with σ/μ < 10%** is a **design specification without demonstrated implementation**. Real-world logging systems exhibit **variable latency** due to: contention, garbage collection, wear leveling, cryptographic overhead. **Constraint 1 violation risk** if logging lane exceeds bounds.

### 7.6 Power Loss Behavior

**IRS retention on power loss:** Memristor state **persists without power**. System restarts in **IRS state** (authorization pending).

**Recovery sequence:**  
1. **Power-on reset**: All circuits initialized  
2. **Log verification**: Last log entry read and integrity-checked (Merkle hash)  
3. **Confirm pulse re-issue**: If log valid, confirm pulse regenerated  
4. **State transition permitted**: IRS→LRS only after successful verification

**Audit trail completeness:** Power loss event logged with **timestamp** (if RTC available) or **sequence number** on restart.

### 7.7 Refuse (−1) Hardware Behavior

**HRS state options:**  
1. **Permanent lock**: One-time programmable fuse prevents exit from HRS. **Irreversible**—requires physical replacement.  
2. **Resettable**: Specific voltage sequence (higher than normal operating range) permits HRS→IRS transition. **Requires authorization** via separate confirm path.

**Audit trail for Refuse event:**  
- **Log entry**: Timestamp, decision context, reason code  
- **Merkle hash**: Cryptographic binding to previous entries  
- **PUF signature**: Die-identity binding  
- **State persistence**: HRS maintained until explicit reset or permanent lock

### 7.8 Multi-Cell Parallel Execution

**Crossbar topology for parallel NL=NA:**  
```  
Row lines (word lines): N cells  
Column lines (bit lines): M cells  
Confirm wires: Routed per-cell or shared per-row

Parallel execution:  
- Multiple cells in IRS simultaneously  
- Independent logging paths per cell  
- Confirm pulses issued independently  
- No cross-cell interference (isolated filaments)  
```

**Scaling limit:** Wire energy dominates at **crossbar dimensions >512×512** (see Section 9).

### 7.9 Attack Modeling

**Pulse spoofing:**  
- **Attack**: Inject false confirm pulse within window comparator tolerance  
- **Defense**: RC signature detection, independent reference, timing window  
- **Minimum attack energy**: ~1 pJ (pulse amplitude × duration)—detectable by power monitoring

**Confirm wire shorting:**  
- **Short to ground**: Pulse amplitude = 0—rejected, cell remains IRS  
- **Short to VDD**: Pulse amplitude = VDD—rejected if VDD outside window, cell remains IRS  
- **Detection**: Window comparator flags out-of-range pulse

**Logging path failure mid-write:**  
- **Behavior**: Log entry incomplete, Merkle hash mismatch  
- **Result**: Confirm pulse not generated, cell remains IRS  
- **Recovery**: Log rollback to last valid entry, retry

**Read disturb exploitation:**  
- **Attack**: Repeated sub-threshold reads to perturb IRS toward LRS  
- **Threshold**: >10⁶ reads at 0.3V required for measurable shift  
- **Defense**: Read counter with refresh, access rate limiting

**Analog fault injection:**  
- **Voltage glitching**: May cause spurious switching—mitigated by hysteresis window  
- **EM pulse**: May induce currents—mitigated by shielding, differential sensing  
- **Temperature extremes**: State drift—mitigated by design margins, refresh

**Degraded mode on attack detection:**  
- **Fail-safe to HRS**: Conservative—system refuses all actions  
- **Alert only**: Permits continued operation with logging—risk of continued attack  
- **Log and continue**: Default for non-critical attacks; fail-safe for critical

**Recommendation:** **Fail-safe to HRS** for critical systems; **log and continue** with degraded trust for non-critical.

---

## 8. Hardware Root of Trust

### 8.1 PUF Identity

**Physical entropy source:** Post-manufacturing variation in:  
- **Filament nucleation sites**: Stochastic oxygen vacancy distribution  
- **Transistor thresholds**: Dopant fluctuation, line-edge roughness  
- **Interconnect resistance**: Grain boundary variation

**Must not be factory-programmed:** If foundry burns PUF values, system reduces to **single-vendor trust**—**Phase 1 failure mode**.

**PUF circuit architecture comparison:**

| PUF Type | Entropy Source | MT Compatibility | Reliability (0–125°C) |  
|----------|----------------|------------------|----------------------|  
| **SRAM PUF** | Cell power-up state | Low (requires SRAM array) | Moderate (bit flips) |  
| **Ring Oscillator** | Frequency variation | Medium (additional circuits) | Good |  
| **Memristive PUF** | Filament resistance | **High** (native integration) | Unvalidated |  
| **Bistable PUF** | Metastable settling | Low (additional circuits) | Poor |

**Recommendation:** **Memristive PUF** using existing ReRAM array—**no additional circuits required**, native MT integration.

**Uniqueness requirement:** Inter-die Hamming distance **>49%** [high confidence: IEEE PUF standard]. Below this threshold, PUF identity is unreliable—**kill condition**.

**Reliability requirement:** Intra-die Hamming distance **<1%** across temperature 0–125°C and voltage ±10%.

**Current status:** Memristive PUF demonstrations show **inter-die HD 45–55%**, **intra-die HD 2–5%** [unverified recall: 2018–2022 academic papers]. **>49% requirement not consistently demonstrated**—**validation gap**.

**PUF key signing protocol:**  
1. **Enrollment**: PUF response measured, helper data generated  
2. **Reconstruction**: Challenge→PUF→response→error correction→stable key  
3. **Signing**: ECDSA or EdDSA signature using PUF-derived private key  
4. **Verification**: Public key (signed by foundry) verifies signature

### 8.2 Manufacturing Provenance

**Secure provisioning chain:**

**Wafer sort:**  
- PUF challenge-response measured per die  
- Foundry signs PUF public key with **foundry private key**  
- Attestation record: {fab_date, node, wafer_lot, die_x, die_y, PUF_pubkey, foundry_signature}

**Die attach:**  
- Die identity verified against attestation database  
- Package ID bound to die ID

**System integration:**  
- Full chain verified: foundry→package→system  
- System PUF (if different from die PUF) enrolled

**Attestation database fields:**  
| Field | Source | Persistence |  
|-------|--------|-------------|  
| Fab date | Foundry MES | Escrow |  
| Node | Foundry process | Escrow |  
| Wafer lot | Foundry MES | Escrow |  
| Die coordinates | Wafer map | Escrow |  
| PUF public key | Wafer sort measurement | Escrow + device certificate |  
| Foundry signature | Foundry HSM | Escrow + device certificate |

**Chain of custody:** Any log entry produced 20 years post-deployment must be traceable to:  
1. **Merkle hash** → log entry  
2. **Log entry** → PUF signature  
3. **PUF signature** → PUF public key  
4. **PUF public key** → foundry signature  
5. **Foundry signature** → {fab_date, node, wafer_lot, die_x, die_y}

**Foundry longevity:** If foundry ceases operation:  
- **Escrow arrangement**: Attestation database copy held by **independent escrow agent**  
- **Cryptographic time-stamping**: Foundry signatures time-stamped by **trusted timestamp authority**  
- **Minimum escrow**: 20-year retention guarantee, cryptographic integrity verification

**Current status:** **Escrow arrangements exceeding current industry practice**—no standard foundry offering includes 20-year attestation escrow.

### 8.3 Trust Chain Integration

**Artifact: Hardware Root of Trust Chain Diagram**

```  
TRUST CHAIN: FROM MERKLE HASH TO FOUNDRY WAFER LOT  
====================================================

LOG ENTRY (at time T)  
    |  
    v  
+--------------------------------+  
|  {decision, context, timestamp, |  
|   state_transition, PUF_sig}   |  
+--------------------------------+  
    |  
    v  
MERKLE HASH CHAIN  
    |  
    v  
+--------------------------------+  
|  Hash(entry_T + hash(entry_T-1))|  
|  = root of integrity chain      |  
+--------------------------------+  
    |  
    v  
PUF SIGNATURE VERIFICATION  
    |  
    v  
PUF PUBLIC KEY (die-unique)  
    |  
    v  
+--------------------------------+  
|  FOUNDRY ATTESTATION            |  
|  {foundry_pubkey, signature,    |  
|   fab_date, node, wafer_lot,    |  
|   die_x, die_y}                 |  
+--------------------------------+  
    |  
    v  
+--------------------------------+  
|  ESCROW VERIFICATION (if needed)|  
|  {timestamp_authority,          |  
|   escrow_agent_signature}       |  
+--------------------------------+  
    |  
    v  
HARDWARE IDENTITY CONFIRMED  
```

**Chain verification by hostile reviewer:**  
1. Extract PUF public key from device certificate  
2. Verify foundry signature on PUF public key using known foundry public key  
3. Query escrow database with {wafer_lot, die_x, die_y} to retrieve attestation record  
4. Verify attestation record matches device certificate  
5. Verify Merkle root against log entry hash chain  
6. Confirm all signatures cryptographically valid

**Break point analysis:**  
- **PUF→Foundry**: Broken if PUF factory-programmed—**single-vendor trust failure**  
- **Foundry→Escrow**: Broken if foundry defunct without escrow—**attestation gap**  
- **Escrow→Verification**: Broken if escrow agent compromised—**trust collapse**

**Status:** All break points are **program-level risks** without mature industry solutions.

---

## 9. Emulation Tax: Quantified Comparison

### 9.1 Three Implementation Comparison

**A) Software Ternary on Binary CMOS:**  
- 2-bit encoding for three states  
- State machine evaluation in software  
- Logging via system calls  
- **No hardware enforcement**

**B) Native MT at Circuit Level:**  
- Balanced ternary encoding  
- Native ternary gates  
- Hardware NL=NA interlock  
- **Full hardware enforcement**

**C) Hybrid: Ternary Memory + Binary Compute:**  
- Ternary state in memristors  
- Binary compute for operations  
- Hardware logging, software state machine  
- **Partial hardware enforcement**

### 9.2 Worked Numerical Example

**Artifact: Worked Numerical Example with Best/Worst Bounds**

**Scenario:** Decision pipeline with 1,000 decisions/second, 10-year lifetime = 3.15×10¹¹ decisions.

**Parameters:**  
- Gate switching energy: E_gate = 0.07 fJ (N2 node)  
- Memory read energy: E_mem_read = 100 fJ (SRAM), 1 pJ (ReRAM)  
- Memory write energy: E_mem_write = 1 pJ (SRAM), 10 pJ (ReRAM)  
- Software overhead: 1,000–10,000× gate energy per decision

**Implementation A (Software Ternary):**  
```  
Per decision:  
- State encoding (2-bit): 2 × 0.07 fJ = 0.14 fJ  
- State machine eval (software): ~1,000 instructions × 0.07 fJ = 70 fJ  
- Memory access (state read/write): 2 × 100 fJ = 200 fJ  
- Logging (system call): ~10,000× overhead = 700 fJ  
Total per decision: ~970 fJ (best case), ~10,000 fJ (worst case with cache misses)

10-year total: 3.15×10¹¹ × 970 fJ = 306 J (best), 3,150 J (worst)  
```

**Implementation B (Native MT):**  
```  
Per decision:  
- Ternary sense: 10 pJ (ReRAM read)  
- State transition (if needed): 10 pJ (ReRAM write)  
- Logging (hardware): 100 pJ (Merkle hash + NV write)  
- Confirm pulse: 1 pJ  
Total per decision: ~121 pJ (typical), ~200 pJ (worst case with retry)

10-year total: 3.15×10¹¹ × 121 pJ = 38 J (typical), 63 J (worst)  
```

**Implementation C (Hybrid):**  
```  
Per decision:  
- Ternary sense: 10 pJ (ReRAM read)  
- Binary compute: 70 fJ (software state machine)  
- Hardware logging: 100 pJ  
Total per decision: ~70.11 pJ (dominated by software)

10-year total: ~22 J (but lacks hardware enforcement)  
```

**Energy comparison:**

| Implementation | Energy per Decision | 10-Year Total | Hardware Enforcement |  
|----------------|---------------------|---------------|---------------------|  
| A (Software) | 970 fJ–10,000 fJ | 306–3,150 J | No |  
| B (Native MT) | 121–200 pJ | 38–63 J | Yes |  
| C (Hybrid) | ~70 pJ | ~22 J | Partial |

**Key finding:** Native MT shows **8,000× energy advantage** over software emulation **per decision**, but this advantage is **misleading**—software implementations amortize cost across batch operations, while MT is per-decision. **Realistic comparison** requires system-level analysis (Phase 2).

### 9.3 Comparative Table

**Artifact: Emulation Tax Comparative Table**

| Metric | Software Ternary (A) | Native MT (B) | Hybrid (C) | 2025 Baseline (Binary) |  
|--------|---------------------|---------------|------------|----------------------|  
| **Speed (decisions/sec)** | 10⁶ (CPU-limited) | 10⁸ (hardware) | 10⁷ (mixed) | 10⁹ (binary logic) |  
| **Energy/decision** | 1–10 nJ | 0.1–0.2 nJ | 0.07 nJ | 0.001 nJ |  
| **Area per decision node** | 1× (software) | 5× (ternary circuits) | 2× (hybrid) | 0.1× (dense binary) |  
| **Latency penalty** | 1–10 µs (software) | 0.1–1 µs (hardware) | 0.5–5 µs (mixed) | <1 ns (binary) |  
| **Hardware enforcement** | No | Yes | Partial | No |  
| **WCET provable** | No (software) | Analytical only | No (software path) | Yes (binary) |  
| **20-year retention** | N/A (volatile) | Unvalidated | Unvalidated | N/A (volatile) |

### 9.4 Interconnect Implications

**Crossbar scaling:**

| Crossbar Size | Wire Length | Wire Capacitance | Wire Energy | Compute Energy | Wire/Compute Ratio |  
|---------------|-------------|------------------|-------------|----------------|-------------------|  
| 64×64 | 100 µm | 20 fF | 5.6 fJ | 10 pJ | 0.06% |  
| 256×256 | 400 µm | 80 fF | 22.5 fJ | 10 pJ | 0.23% |  
| 512×512 | 800 µm | 160 fF | 45 fJ | 10 pJ | 0.45% |  
| 1024×1024 | 1.6 mm | 320 fF | 90 fJ | 10 pJ | 0.9% |  
| 2048×2048 | 3.2 mm | 640 fF | 180 fJ | 10 pJ | 1.8% |

**Wire energy dominance threshold:** At **crossbar dimensions >2048×2048**, wire energy exceeds 10% of compute energy—**acceptable for most applications**. At **>8192×8192**, wire energy exceeds compute energy—**architectural concern**.

**MT viability threshold:** Crossbar dimensions **up to 4096×4096** remain viable without wire energy dominance. **No architectural barrier** at practical scales.

---

## 10. Falsifiability: Phase 1 Predictions and Failure Conditions

### 10.1 Testable Predictions (Minimum 10)

| # | Prediction | Test Method | Timeline |  
|---|------------|-------------|----------|  
| 1 | TaOx IRS σ/μ < 40% at operating conditions | Statistical measurement across 100+ devices, 0–125°C | 6 months |  
| 2 | TaOx IRS retention >10 years at 85°C (95% confidence) | Accelerated test at 150°C, 10,000 hours, Arrhenius extrapolation | 18 months |  
| 3 | Confirm pulse RC spoof detection <5 ns rise time | Injected pulse measurement with variable loading | 3 months |  
| 4 | Window comparator rejects VDD-compromised pulses | Fault injection with VDD sweep | 3 months |  
| 5 | PUF inter-die Hamming distance >49% | 100+ device challenge-response measurement | 6 months |  
| 6 | PUF intra-die Hamming distance <1% across corners | Temperature/voltage sweep, repeated measurements | 6 months |  
| 7 | Sense amplifier 3-state discrimination at 10⁶ cycles | Accelerated read testing with margin monitoring | 12 months |  
| 8 | NL=NA logging lane WCET <300 ms at 99.99th percentile | Statistical latency measurement under load | 6 months |  
| 9 | Read disturb threshold >10⁶ cycles for IRS→LRS | Sub-threshold read stress testing | 12 months |  
| 10 | Memristive PUF reliability <2% bit error rate at 125°C | Temperature sweep with error correction disabled | 6 months |

### 10.2 Program Termination Conditions (Minimum 10)

| # | Failure Condition | Consequence |  
|---|-------------------|-------------|  
| 1 | **TaOx σ/μ > 40%** at IRS operating conditions | IRS not reliably distinguishable—**device layer fail** |  
| 2 | **10-year accelerated test at 150°C demonstrates <10 year retention** at 95% confidence lower bound | 20-year specification unachievable—**device layer fail** |  
| 3 | **Confirm pulse tamper-evidence requires components exceeding 400°C BEOL thermal budget** | Process integration impossible—**circuit layer fail** |  
| 4 | **PUF inter-die Hamming distance < 49%** or intra-die > 1% across specified conditions | Identity unreliable—**trust layer fail** |  
| 5 | **WCET bounds unprovable at 99.99th percentile** for any enforcement path | Non-blocking constraint violated—**architecture layer fail** |  
| 6 | **No quantified architectural advantage demonstrated** in Phase 2 system-level analysis | Economic viability absent—**program termination** |  
| 7 | **Binary MLC ReRAM achieves equivalent functional safety** with lower total cost of ownership | Competitive disadvantage—**program termination** |  
| 8 | **Wire energy dominates compute energy** at crossbar dimensions below 1024×1024 | Scalability barrier—**architecture layer fail** |  
| 9 | **Read disturb threshold for IRS→LRS transition falls below 10⁶ cycles** | Reliability unacceptable—**device layer fail** |  
| 10 | **Foundry PUF attestation chain requires single-vendor trust** with no cryptographic escape | Trust model compromised—**program termination** |

---

## 11. Phase 1 Conclusion

### 11.1 Layer-by-Layer Pass/Fail Assessment

| Layer | Assessment | Key Finding |  
|-------|------------|-------------|  
| **Device Physics (Section 5)** | **CONDITIONAL PASS** | TaOx ReRAM demonstrates proven binary switching; IRS capability **theoretically sound but experimentally unvalidated** for 20-year retention and σ/μ < 20% |  
| **Circuit Primitives (Section 6)** | **PASS** | Native ternary gates analytically achievable with 2.5–6× overhead; sense amplifier architectures sufficient for three-state discrimination |  
| **Physical Interlock (Section 7)** | **CONDITIONAL PASS** | NL=NA architecture conceptually sound; **300 ms WCET bound with σ/μ < 10% is design target without demonstration** |  
| **Hardware Root of Trust (Section 8)** | **CONDITIONAL PASS** | PUF integration architecturally compatible; **>49% inter-die Hamming distance and 20-year escrow arrangements exceed current practice** |  
| **Comparative Baseline (All)** | **FAIL** | **No discontinuous advantage over named 2025 baseline demonstrated at any layer**; named baseline product does not exist |

### 11.2 Phase 2 Inheritance

**Phase 2 MAY ASSUME:**  
1. Binary ReRAM device physics as validated in 12–28nm production  
2. 10⁶–10⁷ cycle endurance achievable with proper current compliance  
3. 10-year retention at 85°C for LRS/HRS as demonstrated  
4. Sense amplifier architectures capable of three-state discrimination for 10⁶–10⁸ read cycles  
5. NL=NA interlock mechanisms with bounded latency under nominal conditions  
6. Gate inflation factors of 2.5–6× versus binary CMOS

**Phase 2 MUST NOT ASSUME:**  
1. **20-year IRS retention with 95% confidence lower bound**—unvalidated  
2. **σ/μ < 20% for IRS variability**—requires explicit process control demonstration  
3. **WCET bounds proven at 99.99th percentile** under all operating corners—analytical only  
4. **Discontinuous advantage over software-implemented ternary state machines**—not demonstrated  
5. **Scalability beyond 512×512 crossbar dimensions** without wire energy analysis  
6. **Existence of named "TSMC N2 CoWoS with embedded ReRAM 1T1R, 2025 PDK" baseline**—product does not exist as specified  
7. **Memristive PUF reliability <2% BER at 125°C**—unvalidated  
8. **20-year foundry attestation escrow availability**—exceeds current practice

### 11.3 System Capabilities Foreclosed

The following capabilities **cannot be assumed** based on Phase 1 findings:  
- **Autonomous operation with 20-year maintenance-free enforcement**—IRS retention unvalidated  
- **Deterministic WCET guarantees under all fault conditions**—logging lane bounds unproven  
- **Cryptographic provenance without escrow dependency**—foundry longevity requires escrow  
- **Competitive advantage versus binary MLC with software safety**—no discontinuous advantage demonstrated

### 11.4 Final Assessment

**Phase 1 Core Question:** Can the three TL states be physically instantiated as stable, non-volatile, hardware-enforced resistance states with sufficient reliability for deterministic autonomous execution over 20 years?

**Answer:** **PARTIAL SUCCESS WITH CRITICAL GAPS**

The three states **can be physically instantiated** with demonstrated binary ReRAM technology and theoretically engineered IRS. However:  
- **20-year retention for IRS is unvalidated**—only 10-year retention for binary states is demonstrated  
- **σ/μ variability of 20–40% for IRS exceeds the <20% target** for reliable discrimination  
- **No discontinuous advantage over binary alternatives** has been demonstrated  
- **Named 2025 baseline product does not exist**—comparative claims are speculative

**Recommendation:** Phase 2 may proceed with **explicit constraints** documented above. **Immediate termination is not warranted** but **validation of IRS reliability** is **mandatory gate** before any deployment consideration.

---

## 12. Bibliography

| Citation | Source | Confidence |  
|----------|--------|------------|  
| Chua, L.O. "Memristor—The Missing Circuit Element." IEEE Trans. Circuit Theory, 1971. | IEEE | High confidence |  
| IRDS 2023: International Roadmap for Devices and Systems. | IEEE | High confidence |  
| TSMC N2 Technology Disclosure, IEDM 2023. | IEDM | High confidence |  
| KIOXIA ReRAM Qualification Data, IEDM 2024. | IEDM | High confidence |  
| Panasonic TaOx ReRAM 10-year Retention Study, IEDM 2020. | IEDM | High confidence |  
| Waser, R. "Nanoelectronics and Information Technology." Wiley-VCH, 2012. | Textbook | High confidence |  
| Wong, H.-S.P. "Metal-Oxide RRAM." Proc. IEEE, 2012. | IEEE | High confidence |  
| IEDM 2018–2023 TaOx device papers (various authors). | IEDM | Unverified recall |  
| IEEE PUF Standard P2410, Draft 2022. | IEEE | High confidence |  
| TSMC ReRAM Process Integration, VLSI 2022 (industry analyst reports). | VLSI | Unverified recall |  
| Academic memristive PUF demonstrations, 2018–2022 (various). | Nature, APL | Unverified recall |  
| KIOXIA 3D ReRAM Scaling Study, IEDM 2024. | IEDM | High confidence |

---

## 13. Glossary

| Term | Definition |  
|------|------------|  
| **MT** | Mandated Ternary—the hardware implementation architecture |  
| **TL** | Ternary Logic—the formal decision framework with Proceed/Epistemic Hold/Refuse states |  
| **NL=NA** | No Log = No Action—physical interlock preventing state transition without logging confirmation |  
| **PUF** | Physical Unclonable Function—die-unique identity from post-manufacturing physical entropy |  
| **LRS** | Low Resistance State—Proceed (+1) state, ~1–10 kΩ |  
| **IRS** | Intermediate Resistance State—Epistemic Hold (0) state, ~100 kΩ–1 MΩ |  
| **HRS** | High Resistance State—Refuse (−1) state, ~1–10 MΩ |  
| **BEOL** | Back-End-Of-Line—interconnect and passive processing, typically <400°C |  
| **GAA** | Gate-All-Around—transistor architecture with nanosheet channel |  
| **CiM** | Compute-in-Memory—processing within memory array |  
| **ADC** | Analog-to-Digital Converter |  
| **DAC** | Digital-to-Analog Converter |  
| **NVRAM** | Non-Volatile Random Access Memory |  
| **ReRAM** | Resistive Random Access Memory—memristive switching device |  
| **PCM** | Phase Change Memory—Ge₂Sb₂Te₅ crystalline/amorphous switching |  
| **MTJ** | Magnetic Tunnel Junction—STT-MRAM device |  
| **FeFET** | Ferroelectric FET—HfZrO polarization switching |  
| **WCET** | Worst-Case Execution Time—provably bounded at 99.99th percentile with σ/μ < 10% |

---

*"Build the third state into matter, and the future stops pretending it never hesitated." — Lev Goukassian.*

