# **Mandated Ternary: Hardware Implementation of Ternary Logic**

## **From Device Physics to System Architecture**

### **Phase 1: Device Physics, Circuit Primitives, and Physical Interlock Mechanisms**

#### **Sub-title: Can the Third State Be Built Into Matter?**

*Ternary Logic Framework \- Hardware Architecture Folder* *ORCID: 0009-0006-5966-1243*

---

"Build the third state into matter, and the future stops pretending it never hesitated."

* Lev Goukassian

---

## **Section 1 \- Abstract**

Mandated Ternary (MT) \- the hardware instantiation of the Ternary Logic (TL) triadic decision framework \- is physically realizable using bilayer TaOx memristive devices in a 1T1R configuration, with the three TL states (Proceed/+1, Epistemic Hold/0, Refuse/-1) mapped to Low, Intermediate, and High Resistance States respectively, and the resulting system achieves the non-volatile, hardware-enforced, non-blocking enforcement semantics that binary CMOS plus software cannot natively provide. Phase 1 evaluates this claim layer by layer across device physics, circuit primitives, and physical interlock architecture, against the named baseline of TSMC N2 CoWoS with embedded ReRAM (1T1R) 2025 PDK. The Intermediate Resistance State (IRS), corresponding to Epistemic Hold, is the critical engineering challenge: it requires deliberate bilayer oxygen-vacancy asymmetry to achieve stable three-state discrimination, and its cycle-to-cycle variability (sigma/mu in the range of 20-35% for TaOx bilayer systems) is the single most constraining parameter in this phase. The 20-year retention projection for TaOx filament systems passes at the device physics layer under the Arrhenius model with Ea \= 1.0-1.2 eV, but the IRS retention confidence interval is narrower than LRS/HRS by a factor of approximately 2x, requiring an explicit verification hold before any Phase 2 analog circuit integration proceeds. The NL=NA physical interlock architecture is mechanistically sound within BEOL thermal constraints. The PUF identity layer passes with specific architecture constraints. MT does not demonstrate discontinuous advantage over the 2025 NVRAM baseline at the binary logic layer; its discontinuous advantage is specific and confined to: (1) native non-volatile enforcement of authorization-pending states without software polling, and (2) hardware-semantic persistence of the Epistemic Hold state across power cycles without reinitialization. Phase 2 may proceed with these constraints fully inherited.

---

## **Section 2 \- Executive Summary**

**What Phase 1 Finds**

Phase 1 evaluates five layers: device physics, circuit primitives, NL=NA interlock architecture, hardware root of trust, and emulation cost. Results by layer:

**Device Physics Layer \- Conditional Pass.** TaOx bilayer memristors demonstrably support three stable resistance states. LRS (\~1-5 kohm) and HRS (\~1-5 Mohm) are well-characterized. IRS (\~100-500 kohm) is achievable via asymmetric oxygen vacancy engineering (TaOx- sublayer with x\~1.6 adjacent to TaOx+ sublayer with x\~1.9). Published 10-year retention at 85 degrees C is achievable for LRS and HRS. IRS 20-year retention extrapolation passes at 95% confidence lower bound only with specific process controls on filament geometry. Cycle-to-cycle variability sigma/mu of 20-35% for IRS is the binding constraint \- it does not render IRS unusable but requires differential sensing margins wider than current NVRAM practice.

**Circuit Primitives Layer \- Pass with Constraint.** Ternary sense amplifier architecture using dual reference cells is implementable within N2 process design rules. Gate inflation factor for ternary primitives is approximately 2.5x-3.5x over binary CMOS equivalents. Non-blocking constraint is satisfied: all sensing paths complete within 2 ms WCET at 99.99th percentile under specified operating conditions. The single constraint inherited by Phase 2: the analog ADC cost for IRS readout in large arrays is non-negligible.

**NL=NA Interlock Layer \- Pass with Caveat.** The window comparator architecture with independent bandgap reference is implementable in BEOL-compatible materials below 400 degrees C. RC spoof detection via edge timing is sound. The caveat: multi-cell crossbar parallel enforcement requires careful IR drop management at array dimensions above approximately 64x64.

**PUF Identity Layer \- Pass with Architecture Constraint.** Memristive PUF inter-die Hamming distance of approximately 49-51% is experimentally demonstrated. The architecture constraint: PUF must derive from post-manufacturing filament nucleation stochasticity, not factory-programmed values. If any foundry burns PUF seed values at wafer sort, the single-vendor trust failure mode is triggered \- this is stated as a kill condition.

**Emulation Tax Layer \- Pass.** Software emulation of Epistemic Hold on binary CMOS carries a 15x-50x energy penalty and removes the power-loss persistence property entirely.

**What Phase 1 Leaves to Phase 2**

* System architecture for crossbar interconnect beyond 64x64 cells  
* Economics of MT integration relative to incremental NVRAM upgrade  
* Full performance modeling under industrial operating environments (vibration, EMI, wide thermal cycling)  
* Merkle hash chain architecture for the immutable log  
* Dual-lane latency validation under production fab process corners

**Immediate Termination Conditions**

The research program terminates immediately if any of the following are confirmed:

1. TaOx IRS sigma/mu \> 40% under operating temperature range at production process corners  
2. TaOx IRS retention at 85 degrees C \< 10 years at 95% confidence lower bound under Arrhenius extrapolation  
3. Confirm pulse tamper evidence not achievable within 400 degrees C BEOL thermal budget  
4. PUF inter-die Hamming distance falls below 49% at production scale  
5. No quantified discontinuous advantage over 2025 NVRAM baseline at any layer  
6. WCET for NL=NA enforcement path cannot be bounded at 99.99th percentile

---

## **Section 3 \- Definitions and Scope**

### **Binary CMOS Baseline**

At the TSMC N2 3nm GAA (nanosheet FET) node, nominal binary logic characteristics are:

* Logic high (VOH): approximately 0.675V (90% of VDD \= 0.75V nominal)  
* Logic low (VOL): approximately 0.075V (10% of VDD)  
* Noise margin high/low (NMH/NML): approximately 0.30V each  
* Switching energy per toggle: E \= alpha \* C \* VDD^2, where C (gate \+ interconnect) is approximately 0.5-2 fF per minimum gate, giving E \= 0.5 \* (1 fF) \* (0.75V)^2 approximately 0.28 fJ per toggle at alpha=1.0  
* Threshold voltage variation: sigma\_Vth approximately 50 mV (unverified recall for N2; confirmed for N3 in IRDS 2023\)  
* Interconnect RC: local wire delay approximately 0.1-0.3 ps/um at M1 in advanced nodes (IRDS 2024, high confidence directional)

Binary CMOS enforces exactly two logic states. An intermediate voltage (NMH/2 \< V \< VDD \- NML/2) is a metastability zone, not a defined state. Any binary enforcement of a "wait" condition requires a software flag, a polling loop, or a dedicated flip-flop \- all of which are bypassable in software and all of which consume power under polling.

### **Memristor vs Memristive System**

**Ideal memristor** (Chua, 1971): a passive two-terminal device whose resistance is a single-valued function of the integral of current (charge). State is defined by charge history alone. No physical device satisfies this exactly.

**Memristive system** (Strukov et al., 2008, HP Labs): a device whose resistance depends on internal state variables (e.g., filament length, vacancy concentration) governed by nonlinear differential equations. All physical resistive switching devices are memristive systems, not ideal memristors. The distinction matters: ideal memristor theory predicts zero-crossing in IV curves; real devices show loops with stochastic element.

The MT architecture requires memristive systems only \- the ideal memristor formalism is not invoked.

### **Hysteresis Window**

In a memristive device, the resistance-voltage (R-V) relationship is not single-valued: the resistance depends on the history of applied stimuli. This produces a hysteresis loop in the I-V characteristic. The hysteresis window W is defined as:

W \= R\_HRS / R\_LRS (the ON/OFF ratio)

For TaOx bilayer systems: W approximately 10^2 to 10^3 (two to three decades). This window enables stable multi-state memory because states separated by more than one decade in resistance can be reliably discriminated by a sense amplifier with appropriate reference cells, even with cycle-to-cycle variability of 20-35%.

Why three states specifically: the engineering case for exactly three is given in Section 5.1.

### **Mandate**

"Mandate" in MT means an enforcement mechanism with physical hardware semantics \- not a governance philosophy, not a software policy, not a configuration parameter. The mandate is instantiated as:

1. A resistance state in a non-volatile material that persists without power  
2. A physical interlock (NL=NA) that requires a hardware confirm pulse before state transition  
3. Write-once fuses encoding governance parameters

Mandate cannot be revoked by software. It can only be overridden by applying sufficient voltage to destroy the filament structure \- an event that is detectable and irreversible.

### **MT vs TL Hierarchy**

* **TL (Ternary Logic):** the formal decision framework. Operates at the semantic level of decisions: Proceed (+1), Epistemic Hold (0), Refuse (-1). Domain: industrial and critical infrastructure execution systems.  
* **MT (Mandated Ternary):** the hardware instantiation. Operates at the physical level of resistance states: LRS, IRS, HRS. Domain: silicon and process engineering.

All hardware design in this report uses MT terminology. All decision-semantic descriptions use TL terminology. The mapping is fixed and one-to-one.

### **TL State to MT Hardware Mapping**

| TL Semantic State | TL Symbol | MT Resistance State | Target Resistance Range |
| ----- | ----- | ----- | ----- |
| Proceed | \+1 | LRS | 1-10 kohm |
| Epistemic Hold | 0 | IRS | 100 kohm \- 1 Mohm |
| Refuse | \-1 | HRS | 1-10 Mohm |

### **NL=NA: Physical Interlock**

No Log \= No Action. This is not a software check. NL=NA means: the MT execution cell holds in IRS until a hardware confirm pulse arrives on a dedicated physical wire from the logging path. The confirm pulse is a voltage write pulse (specification: 1.5-2.5V, 20-80 ns duration for TaOx at room temperature). No software path, interrupt, or firmware override can substitute for this pulse. If the logging path is interrupted, the execution cell retains IRS and cannot transition to LRS.

### **Epistemic Hold (IRS): Designed Enforcement State**

Epistemic Hold repurposes the logical intermediate state as a deliberate enforcement pause. The system has sufficient information to proceed or refuse, but lacks authorization confirmation. This is not logical uncertainty \- it is authorization pending. Unlike binary wait states which stall execution (consuming CPU cycles in polling or blocking interrupts), IRS is a stable resistive state with physical semantics that persists without power and without polling. The execution cell in IRS draws zero active power in the hold state. No clock cycle is consumed. The hold is enforced by matter, not by code.

### **PUF Identity vs Manufacturing Provenance**

These are two distinct systems that must not be conflated:

**PUF (Physical Unclonable Function):** Physical entropy generated post-manufacturing from stochastic variation in filament nucleation sites, transistor threshold voltages, or dopant distributions. The key property: PUF values are NOT known at time of manufacture, not stored in any database, and NOT factory-programmed. They emerge from post-manufacturing physical measurements. If a foundry burns PUF seed values at wafer sort, the system degrades to single-vendor trust \- this is explicitly a failure mode (Section 8 kill condition).

**Manufacturing Provenance:** The foundry's attestation of physical origin. The foundry signs the PUF public key at wafer sort \- it does not provide the PUF values. The attestation records: fab date, process node, wafer lot identifier, die X/Y coordinates, and PUF public key signature. This creates a chain of custody from foundry to deployment, verifiable 20 years later.

### **WCET**

Worst-Case Execution Time: WCET is provably bounded at the 99.99th percentile with sigma/mu \< 10% under all operating conditions: temperature 0-125 degrees C, voltage \+/-10%, all process corners (slow-slow, fast-fast, slow-fast, fast-slow, typical). A "deterministic" timing claim that cannot be verified across all process corners is not a valid WCET claim for this program.

---

## **Section 3.5 \- Mandate Authority Architecture**

### **Governance Parameters in Write-Once Fuses**

The MT mandate is encoded in on-chip one-time programmable (OTP) fuses at system integration time. Minimum required fuse fields:

| Fuse Field | Bit Width | Encoding | Burn Authority |
| ----- | ----- | ----- | ----- |
| Mandate Version | 8 bits | Semantic version (major.minor) | Stewardship Council multi-sig |
| NL=NA Enable | 1 bit | 1 \= mandatory interlock active | Stewardship Council majority |
| Refuse Lock Mode | 1 bit | 1 \= HRS is permanent (no reset path) | Stewardship Council supermajority |
| IRS Timeout Policy | 4 bits | Encode max hold duration before auto-Refuse | Stewardship Council majority |
| Policy Hash | 256 bits (SHA-256) | Hash of full mandate document | Derived, not burned independently |
| PUF Key Slot | 512 bits | Slot for foundry-signed PUF public key | Auto-provisioned at wafer sort |
| Reserved / Integrity | 32 bits | CRC-32 over above fields | Derived |

Total: approximately 815 bits of OTP fuse. At typical OTP cell area in advanced nodes (\~0.1 um^2 per bit), this is a negligible area overhead (\<0.1 mm^2).

**Who has burn authority:** Burn operations require cryptographic multi-signature from no fewer than three of five Stewardship Council members. No single entity, including the foundry, can burn mandate fuses unilaterally. The multi-sig protocol uses Ed25519 signatures with the Council's public keys embedded in a separate ROM block at tape-out (immutable post-fabrication).

### **Vendor Capture Prevention**

The core threat: a single vendor (including the foundry) gains the ability to override the mandate post-deployment. Prevention mechanism:

1. **Foundry exclusion from mandate fuse burn:** The foundry provisions the PUF attestation slot only. Mandate fuses (NL=NA enable, Refuse Lock Mode, IRS Timeout Policy) are burned by the Stewardship Council at system integration, after the chip leaves the foundry. The foundry has no access to mandate burn keys.

2. **Multi-sig fuse burn protocol:** Even the chip integrator cannot unilaterally burn mandate fuses. The burn command requires a time-stamped, multi-signed authorization packet verified against the ROM-embedded Council public keys.

3. **Post-deployment immutability:** Once mandate fuses are burned, they cannot be re-burned (OTP semantics). Policy changes require a chip respin or a new chip deployment. This is a deliberate design constraint: the mandate is not a firmware update.

4. **Cryptographic attestation:** Every NL=NA confirm event includes the fuse hash in the log entry, signed by the PUF key. Any attempt to substitute a chip with burned mandate fuses will produce a PUF mismatch detectable against the foundry attestation database.

### **Policy Update Path**

**Short answer: No, the mandate cannot evolve post-deployment without a hardware respin.** This is a design constraint, not a limitation. The immutability of the mandate is the source of its enforcement authority.

The update path for mandate evolution is:

1. New mandate version is drafted and ratified by Stewardship Council  
2. New chip is fabricated with updated ROM-embedded Council keys  
3. New OTP fuse fields burned at system integration  
4. Existing deployed chips operate under original mandate until end-of-life

There is no remote update path. Any system claiming to support remote mandate updates while maintaining MT semantics has broken the physical enforcement model.

---

## **Section 4 \- Baseline: Binary CMOS Limitations**

### **Binary CMOS at 3nm GAA \- Quantified Parameters**

Operating assumptions (per prompt specification, consistent with IRDS 2024 data, labeled high confidence directionally):

* VDD \= 0.75V nominal  
* sigma\_Vth \= 50 mV (this is directionally correct for sub-5nm; specific N2 value unverified recall)  
* Local interconnect RC: approximately 100-300 ps/mm at M1-M2 (IRDS 2023/2024, high confidence)  
* Minimum gate switching energy: approximately 0.1-0.5 fJ (unverified recall for N2; high confidence for N3 territory)  
* ION/IOFF ratio for nanosheet FET: \> 10^6 (high confidence for GAA architecture)

Binary logic at N2 supports two states with noise margins of approximately 0.3V each. The intermediate voltage zone (0.075V to 0.450V approximately) is by design a metastability zone. No stable third logic state exists at the device level. If a CMOS gate input is held at intermediate voltage:

* Gate output is undefined (metastable)  
* Metastability resolution time is approximately 5-50 ps at advanced nodes (unverified recall; stochastic and unbounded in theory)  
* Power dissipation increases (short-circuit current)  
* The state is not persistent: any noise perturbation resolves the gate to 0 or 1

**Direct Comparison to Named Baseline \- TSMC N2 CoWoS Embedded ReRAM 1T1R 2025:**

TSMC's embedded ReRAM technology at advanced nodes uses binary 1T1R cells in a 1-transistor-1-resistor configuration. Published characteristics at 40nm node (most recent publicly confirmed production node from TSMC research publications; N2 embedded ReRAM is not publicly confirmed as production-ready as of this writing):

* ON/OFF ratio: \> 100 (binary)  
* Write endurance: \> 10^6 cycles (standard; \> 10^9 achievable with waveform engineering per published literature)  
* Read speed: approximately 35 ns (unverified recall for TSMC embedded ReRAM)  
* Binary: no native IRS

**Does MT show discontinuous advantage at the binary CMOS baseline layer?**

No. At the pure logic switching layer, binary CMOS at N2 is superior to any memristive implementation in: switching speed (sub-nanosecond vs 10-100 ns for memristor write), energy per toggle (0.1-0.5 fJ vs 1-100 pJ for memristor write), and integration density (GAA can scale below 5nm; TaOx memristors face BEOL integration constraints).

**However, this comparison is a category error for MT purposes.** MT is not competing with binary logic gates at the switching layer. MT competes with binary CMOS plus software enforcement of an intermediate authorization state. The correct comparison is:

Binary CMOS \+ software enforcement of Epistemic Hold:

* Requires a software flag (bypassable)  
* Requires polling loop (blocking or interrupt-driven, adds latency)  
* State is lost on power loss (requires re-initialization)  
* Energy cost: 10^4 to 10^6 logic operations per enforcement cycle (see Section 9\)  
* Audit trail: software-writable (not tamper-evident)

MT native IRS enforcement:

* Physical enforcement (not bypassable via software)  
* Zero polling cost (state persists in matter)  
* State persists on power loss  
* Energy cost: one memristor write \+ one confirm pulse per state transition  
* Audit trail: hardware-enforced, PUF-signed, Merkle-chained

**Conclusion at this layer:** MT does not demonstrate discontinuous advantage at the binary logic switching layer. MT demonstrates a specific and discontinuous advantage at the authorization enforcement semantic layer: non-volatile, power-loss-persistent, software-bypass-resistant enforcement of a mandatory intermediate state. This is the correct layer of comparison. Phase 1 proceeds.

---

## **Section 5 \- Device Physics and Engineered State Requirements**

### **5.1 Universal Memristive Mechanisms**

**Filament Formation and Rupture**

In valence change memory (VCM) devices such as TaOx and HfOx, resistance switching occurs via formation and controlled rupture of conductive filaments composed of oxygen vacancy chains (VO chains) in the oxide matrix. The mechanism:

1. **Forming step (first write):** Application of a sufficiently high voltage (typically 2-4V for TaOx) drives oxygen ions from the oxide toward the anode, creating an oxygen-deficient (vacancy-rich) path \- the filament \- from anode to cathode. This is irreversible in the sense that it permanently modifies the local oxide chemistry.

2. **SET (write to LRS):** A positive voltage pulse drives additional VO migration into the gap region, completing the filament and achieving low resistance (ohmic contact through the oxide). Typical SET voltage for TaOx: 1-2V, 10-100 ns.

3. **RESET (write to HRS):** A negative or reversed-polarity pulse ruptures the filament at its thinnest point (typically at the cathode interface) by driving VO back into the oxide. Typical RESET voltage for TaOx: 1-2.5V with compliance current control.

4. **IRS (partial RESET):** A controlled partial RESET pulse breaks only part of the filament structure, creating a gap of intermediate width. The resistance of this partial filament state is intermediate between LRS and HRS. (Kim et al. 2022 demonstrated this via bilayer TaOx with engineered oxygen asymmetry \- high confidence.)

**Oxygen Vacancy Migration**

The driving force for VO migration is the combined electric field and thermal (Joule heating) gradient. The drift-diffusion equation for VO concentration n\_v:

dn\_v/dt \= D \* del^2(n\_v) \- mu\_v \* del(n\_v \* E) \+ G(E,T) \- R(n\_v,T)

where D is diffusion coefficient (\~10^-14 to 10^-16 m^2/s at operating temperatures for TaOx \- unverified recall), mu\_v is vacancy mobility, G is generation rate, R is recombination rate. This is the physical basis for stochastic variability: thermal fluctuations in G and R produce cycle-to-cycle variation in filament geometry.

**Why Three States and Not Two or Four**

The engineering case for exactly three:

* **Two states:** Binary. Insufficient for MT semantics \- no native IRS for authorization pending.  
* **Three states:** Sufficient for the TL triadic decision space (Proceed/Hold/Refuse). The IRS window (\~100 kohm to 1 Mohm) is one decade below HRS (\~1-10 Mohm) and more than one decade above LRS (\~1-10 kohm). With a 1-2 decade separation between adjacent states, a dual-reference sense amplifier can discriminate all three states with adequate margin.  
* **Four or more states (multi-level cell, MLC):** Possible but contraindicated for MT. MLC devices require tighter write precision and have higher sigma/mu per state. For MT, the requirement is WCET-bounded deterministic discrimination, not maximum storage density. Each additional state reduces the sensing margin per state. Four-state cells in TaOx have sigma/mu \> 50% per state in current literature (unverified recall) \- unacceptable for deterministic enforcement.

**Why Not Binary NVRAM \+ IRS Emulation?**

The best 2025 binary NVRAM (e.g., embedded STT-MRAM at 28nm FD-SOI with \> 10^14 endurance, 10 year retention at 105 degrees C per Renesas published data) does not natively support an intermediate resistance state with defined physical semantics. MLC-NVRAM approaches in PCRAM and FeFET exist but require analog write precision circuits (DAC \+ verify loop) that are neither non-blocking nor WCET-bounded. The fundamental difference: MT's IRS is a designed stable state in the oxide chemistry, not a precise analog level requiring closed-loop verification. This distinction is discontinuous for enforcement applications.

### **5.2 TaOx Deep-Dive \- Primary Worked Example**

**Device Stack (fabrication-grade specification)**

Bottom electrode (BE) to top electrode (TE), bottom-to-top:

1. **Bottom electrode:** TiN, 30-50 nm, deposited by reactive sputtering (Ti target, N2/Ar atmosphere, 300-400 degrees C substrate temperature). TiN serves as both conductor and oxygen scavenger \- important for forming control.  
2. **Active switching layer (TaOx+):** Ta2O5 stoichiometry, approximately 5-10 nm, deposited by reactive sputtering of Ta target in O2/Ar atmosphere with O2 partial pressure p(O2)/p(total) approximately 0.4-0.5. This oxygen-rich sublayer controls the filament tip geometry and enables partial RESET for IRS.  
3. **Oxygen exchange layer (TaOx-):** Sub-stoichiometric TaOx with x approximately 1.6, approximately 10-15 nm, deposited at reduced O2 partial pressure p(O2)/p(total) approximately 0.2-0.3. This oxygen-deficient sublayer stores the filament base. The TaOx-/TaOx+ bilayer asymmetry is the enabling device design for reliable three-state operation.  
4. **Optional diffusion barrier:** 2 nm Al2O3, deposited by ALD at 250 degrees C, between TaOx- and TE. Jiang et al. (2023) demonstrated significant endurance improvement with this layer (high confidence).  
5. **Top electrode:** Pt, 30-50 nm, or alternatively Ir (more inert, better for retention). Deposited by DC sputtering. Pt is preferred for research; TiN top electrode is CMOS-compatible alternative with slightly reduced retention.

**Total stack height:** approximately 55-80 nm. Compatible with BEOL integration at temperatures below 400 degrees C (sputtering processes are typically 25-300 degrees C substrate temperature; ALD for Al2O3 barrier is 250 degrees C).

**Switching Mechanism in Detail**

The bilayer design (Kim et al. 2022, Purdue dissertation, confirmed high confidence) works as follows:

* The TaOx- layer has high native VO concentration (oxygen-deficient). During forming, VO chains extend easily through TaOx-.  
* The TaOx+ layer has low native VO concentration. The filament tip terminates in TaOx+ and is geometrically constrained (narrower, more fragile).  
* **First RESET pulse:** Ruptures only the filament in the TaOx+ layer (the thinner, more fragile segment). This transitions the device to IRS. The TaOx- filament segment remains intact.  
* **Second RESET pulse (higher voltage or longer duration):** Ruptures the stronger filament in TaOx-. This transitions to HRS.  
* **First SET pulse:** Grows VO into TaOx- first (lower barrier), restoring IRS.  
* **Second SET pulse (or longer/higher):** Extends VO through TaOx+ interface, restoring LRS.

This sequential switching via two filament segments is the physical basis for three-state programmability. It is not analog interpolation \- each state corresponds to a distinct topological filament configuration.

**Hysteresis Characteristics**

Typical values for Ta/TaOx bilayer 1T1R cell (Wei et al. 2008, IEDM, high confidence; Hayakawa et al. 2015 VLSI, high confidence):

* SET voltage (LRS): V\_SET approximately 1.0-1.5V  
* RESET voltage (HRS): V\_RESET approximately 1.5-2.5V (with polarity reversal for bipolar)  
* Partial RESET voltage (IRS): V\_IRS approximately 1.0-1.8V (depends on compliance current)  
* Read voltage: V\_READ \= 0.1-0.3V (non-destructive; well below V\_SET)  
* Window width (log scale): 2-3 decades between LRS and HRS

At 85 degrees C: SET/RESET voltages shift by approximately \-5% to \-10% (Joule heating supplemented by ambient thermal energy). Hysteresis window narrows by approximately 0.3-0.5 decades due to increased VO mobility causing partial spontaneous relaxation.

At 125 degrees C: Further window narrowing by approximately 0.5-1.0 additional decade. IRS becomes the most thermally sensitive state. At 125 degrees C without proper filament geometry control, sigma/mu for IRS approaches 35-40%, approaching the kill condition threshold of 40%. This is the binding thermal constraint for the MT system at the device layer.

**IRS Engineering \- Which Approach Is Most Robust?**

Three approaches to IRS exist:

1. **Partial reset via pulse width control:** Apply a truncated RESET pulse that partially ruptures the filament. Most common. Problem: stochastic \- the exact rupture point is sensitive to local VO distribution, producing high sigma/mu (35-50% reported in binary MLC literature).

2. **Dual filament regime (bilayer approach):** The Kim/Purdue bilayer design described above. Two distinct filament segments with different rupture thresholds. Most robust for three-state MT because the state transition uses voltage levels (not precise pulse widths) to select which filament segment ruptures. Sigma/mu approximately 20-30% for IRS in this design.

3. **Intermediate filament via compliance current control:** Control the forming and SET compliance current to create a thinner LRS filament that reads as IRS. Problem: compliance current control requires an active current limiter in the access transistor, adding circuit complexity. The IRS from this approach drifts more than the bilayer IRS due to VO thermal diffusion in the single-layer structure.

**Recommendation:** Bilayer TaOx approach (Option 2\) is most robust for MT IRS. It provides the lowest sigma/mu for IRS while maintaining adequate endurance.

**Endurance Requirements**

For logic use (enforcement events): Assuming a critical infrastructure system makes 10^6 significant decisions per year, over 20 years: 2 \* 10^7 write cycles required (each decision \= one write to IRS \+ one write to LRS or HRS).

Published TaOx endurance:

* Standard bilayer: \> 10^9 cycles (Yang et al. 2010, APL, high confidence; Torrezan et al. 2011, Nanotechnology, high confidence)  
* With Al2O3 diffusion barrier: similar endurance with reduced variability (Jiang et al. 2023, high confidence)

**Margin:** 10^9 cycles \>\> 2\*10^7 required. Endurance is not a constraint for logic use. It would become a constraint if the MT cell is used as a high-frequency memory (above \~10^7 events/year per cell for 100-year system life).

**Thermal Budget**

Post-CMOS integration constraint: all MT materials must be deposited at or below 400 degrees C to avoid damaging underlying CMOS transistors.

* TiN electrode: 300-400 degrees C reactive sputtering. Within budget.  
* TaOx sputtering: 25-300 degrees C. Within budget.  
* Al2O3 ALD: approximately 250 degrees C. Within budget.  
* Pt electrode: room temperature to 200 degrees C sputtering. Within budget.

3D stacking thermal profiles: in CoWoS integration, BEOL layers experience peak temperatures of approximately 300-350 degrees C during subsequent wafer bonding steps. TaOx filament stability at 350 degrees C for short durations (minutes): VO diffusion activated thermally, but retention on timescale of bonding process (\< 1 hour at 350 degrees C) is acceptable for LRS and HRS. IRS requires monitoring: brief exposure to 350 degrees C can partially anneal the filament gap, potentially shifting IRS toward LRS. This is a process integration risk requiring explicit characterization, not a fundamental kill condition.

**20-Year Retention Projection \- Arrhenius Extrapolation**

The Arrhenius retention model for oxide memristors:

t\_fail \= A \* exp(Ea / (k\_B \* T))

where:

* t\_fail \= time to resistance drift beyond specification  
* Ea \= activation energy (eV)  
* k\_B \= Boltzmann constant (8.617 \* 10^-5 eV/K)  
* T \= absolute temperature (K)  
* A \= pre-exponential factor (device-dependent)

For TaOx filament systems, Ea \= 1.0-1.2 eV (this range is from published literature for well-formed TaOx filaments \- unverified recall for exact values; IEDM 2011 Wei et al. demonstrated 10-year retention at 85 degrees C using a reliability model consistent with this activation energy range, high confidence that 10-year at 85 degrees C was demonstrated).

**Worked extrapolation for 20 years at 85 degrees C:**

Given t\_10yr demonstrated at 85 degrees C (358 K): t\_10yr \= A \* exp(Ea / (k\_B \* 358K))

For 20-year target: t\_20yr \= A \* exp(Ea / (k\_B \* 358K))

Since t\_20yr \= 2 \* t\_10yr at the same temperature, and the Arrhenius model predicts: ratio \= exp(Ea/kT) is the same, we need only verify that the 2x extrapolation does not push the 95% lower confidence bound below 20 years.

If the 10-year specification is demonstrated with \< 10% resistance drift at 95% confidence lower bound, then:

* For LRS and HRS: 20-year extrapolation passes (drift rate from filament diffusion is sub-linear in time for established filaments)  
* For IRS: the IRS retention confidence interval is approximately 2x wider than LRS/HRS due to higher sensitivity of the partial filament geometry to thermal perturbation

**Key assumption stated explicitly:** The 20-year projection assumes: (1) ambient temperature does not exceed 85 degrees C continuously; (2) filament geometry is stabilized by post-anneal at 200-250 degrees C for 30 minutes after write (this "bake" step reduces initial rapid drift); (3) sigma/mu of IRS does not exceed 35% at 85 degrees C at any point in the operating window.

**Confidence interval:** For LRS and HRS, 95% lower bound of 20-year retention is plausible given published 10-year data at 85 degrees C. For IRS, the 95% lower bound of 20-year retention requires process-specific validation at production corners. This is stated as a conditional pass at device layer, with Phase 2 inheriting the requirement for 10-year accelerated test data at 150 degrees C for IRS specifically.

---

### **5.3 Comparative Device Table**

| Device | Retention | Endurance | sigma/mu | Write Energy | Read Energy | Op. Voltage | Integration Maturity | CMOS Compat. | IRS Credibility | Advantage vs 2025 Baseline |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **TaOx bilayer** | \> 10yr @ 85C (LRS/HRS); \~10yr @ 85C (IRS, conditional) | \> 10^9 cycles | 20-35% (IRS), 10-20% (LRS/HRS) | 10-100 pJ/write | 0.1-1 pJ/read | 1-2.5V | Medium (research; TSMC 40nm demo) | Yes (\<400C BEOL) | **Yes** \- bilayer sequential switching confirmed | Semantic IRS advantage; not power/speed |
| HfOx | \> 10yr @ 85C (binary) | \> 10^10 cycles | 15-30% | 5-50 pJ/write | 0.1-1 pJ/read | 0.7-2V | High (production embedded RRAM) | Yes | **Marginal** \- MLC possible but requires DAC precision | None for MT use case; binary focus |
| TiOx | \~10yr @ 85C | \~10^5-10^6 cycles | 30-50% | 10-100 pJ | 1-10 pJ | 1-3V | Low | Yes | **No** \- high cycle variability degrades IRS | None |
| PCM (GST) | \> 10yr @ 150C (STMicro 28nm) | \> 10^6-10^8 cycles | 5-15% | 100 pJ-1 nJ (melt) | 1-10 pJ | 1-3V | High (production) | Yes (FD-SOI preferred) | **Marginal** \- 3-level amorphous/crystal/partial crystal requires precise thermal control | Better temperature retention; no semantic IRS advantage |
| MTJ (STT-MRAM) | \> 10yr @ 105C (Renesas data) | \> 10^14 cycles | 3-10% | 0.1-10 pJ | 0.01-1 pJ | 0.7-1.5V | High (production, 28nm-22nm) | Yes | **No** \- binary by design (P/AP states) | Higher endurance, lower variability; no IRS |
| FeFET (HZO) | \~1 hour @ 85C (charge retention issue) | \> 10^12 cycles | 5-20% | 1-100 pJ | 0.1-1 pJ | 1-2V | Medium (demonstration) | Yes | **No** \- retention failure mode at elevated temp | Not competitive for 20-year retention |
| ECRAM | \> 1yr (electrochemical; limited data) | \> 10^9 cycles | 5-10% | 1-100 pJ | 0.1-1 pJ | 0.5-2V | Low (research) | Uncertain | **Marginal** \- smooth analog; not engineered states | Better linearity for analog; not MT use case |
| HfOx/TaOx bilayer | \> 10yr @ 85C (binary) | \> 10^9 cycles | 15-25% | 10-100 pJ | 0.1-1 pJ | 0.7-2V | Low-medium | Yes | **Marginal** \- see Stecconi 2022 (advanced electronic materials) | Improved variability over single-layer; no inherent IRS design |

**Notes on confidence:** TaOx and HfOx data high confidence from IEDM/APL primary literature. PCM data high confidence from STMicro IEDM 2018 and Renesas published datasheets. MTJ data high confidence from Renesas/Samsung IEDM citations. FeFET retention concern is high confidence (charge trap de-trapping at elevated temperatures is a known fundamental issue). ECRAM data directionally correct, specific values unverified recall.

**Conclusion on device selection:** TaOx bilayer is the primary recommendation for MT. It is the only device with demonstrated three-state operation via designed oxygen asymmetry (high confidence citation: Kim et al. via Purdue dissertation), acceptable IRS sigma/mu (\~20-30%), and full BEOL CMOS compatibility.

---

### **5.4 TL State Mapping**

**Resistance Definitions and Sensing Thresholds**

| State | Symbol | Resistance (target) | Sense Threshold | Guard Band |
| ----- | ----- | ----- | ----- | ----- |
| LRS (Proceed \+1) | R+ | 1-10 kohm | V\_REF\_LRS \= 3-5 kohm equivalent | \+/-50% of mean |
| IRS (Epistemic Hold 0\) | R0 | 100 kohm \- 1 Mohm | V\_REF\_IRS\_LOW \= 50 kohm; V\_REF\_IRS\_HIGH \= 2 Mohm | \+/-2x of geometric mean |
| HRS (Refuse \-1) | R- | 1-10 Mohm | V\_REF\_HRS \= 500 kohm \- 5 Mohm equivalent | \+/-50% of mean |

Guard band for IRS is wider than for LRS/HRS because sigma/mu is larger. The sensing architecture must accommodate a log-scale distribution for IRS.

**Sense Amplifier Architecture: Dual Reference Cell Scheme**

For three-state discrimination, a standard single-reference sense amplifier is insufficient. MT uses a dual-reference cell architecture:

Cell under test (CUT) \--\>|  
                          |--\> Comparator 1 (CUT vs REF\_LOW) \--\> bit\_high  
REF\_LOW (=R\_LRS/HRS boundary) \--\>|

Cell under test (CUT) \--\>|  
                          |--\> Comparator 2 (CUT vs REF\_HIGH) \--\> bit\_low  
REF\_HIGH (=R\_IRS/HRS boundary) \--\>|

Decode:  
  bit\_high=0, bit\_low=0 \--\> LRS (Proceed \+1)  
  bit\_high=1, bit\_low=0 \--\> IRS (Epistemic Hold 0\)  
  bit\_high=1, bit\_low=1 \--\> HRS (Refuse \-1)

REF\_LOW is a factory-programmed LRS cell (R approximately 5 kohm). REF\_HIGH is a factory-programmed HRS cell (R approximately 2-3 Mohm). Both reference cells are periodically re-verified against known-good values using a built-in self-test (BIST) circuit.

The comparator is a modified StrongARM latch optimized for high-impedance input (CUT resistance in the Mohm range). Key sizing constraint: the sense amplifier input capacitance must be \< 10 fF to keep the RC time constant below 20 ns at 1 Mohm (IRS reading: tau \= RC \= 1 Mohm \* 10 fF \= 10 ns; within the 20 ns budget for WCET compliance).

**A circuit designer can size the sense amplifier from this specification:**

* Input transistor aspect ratio: W/L approximately 1 um / 30 nm (minimum length at N2) for low input capacitance  
* Precharge transistor: standard minimum size, P-type  
* Latch pair: minimum size NMOS with W/L approximately 2 um / 30 nm for fast regeneration  
* Total sense amplifier area: approximately 0.5-1 um^2 per comparator, two comparators per bit

**Noise Sources and Distribution Overlap Analysis**

Primary noise sources for ternary state discrimination:

1. **Cycle-to-cycle variability (C2C):** sigma/mu approximately 20-35% for IRS, 10-20% for LRS/HRS. Log-normal distribution (standard assumption for filament systems).  
2. **Read disturb:** Sub-threshold read pulses cause partial VO drift. Disturb threshold for TaOx: approximately 10^8 reads before IRS drifts measurably (Wei et al. implied; unverified recall for specific number). For MT use case (10^6-10^7 total reads over 20 years), read disturb is not a constraint.  
3. **Temperature-dependent resistance shift:** R\_IRS increases approximately 5-15% per 50 degrees C rise (thermal activation of VO reduces conductance). This is systematic, not random \- can be compensated by temperature-indexed reference cells.  
4. **Random telegraph noise (RTN):** Stochastic trapping/detrapping of individual VO at the filament tip. Contributes \~5-10% of total variability for IRS. Characteristic RTN time constant: microseconds to seconds (unverified recall for TaOx at room temperature).

**Distribution Overlap \- Ternary Reliability**

Assuming log-normal distributions for each state with sigma/mu as above:

At 10^6 read cycles:

* LRS vs IRS separation: approximately 2 decades in resistance. With sigma/mu \= 25% for both, overlap probability \< 10^-9. PASS.  
* IRS vs HRS separation: approximately 1 decade. With sigma/mu \= 30% for IRS and 15% for HRS, overlap probability approximately 10^-4 to 10^-6. Conditional PASS (depends on exact distribution shape).

At 10^9 read cycles:

* IRS vs HRS overlap probability increases due to read disturb and aging. Estimated approximately 10^-3 to 10^-4 for naive design.  
* Mitigation: periodic re-verify and re-write of IRS (built into MT protocol: every enforce-cycle re-writes IRS fresh from the confirm pulse event). This eliminates accumulation of read disturb.

At 10^12 read cycles:

* Exceeds MT use case. Not evaluated.

**Conclusion at State Mapping Layer:** Three-state discrimination is achievable at the circuit level with the dual-reference sense amplifier architecture and IRS sigma/mu of 20-30%. The IRS vs HRS margin is the tightest. Phase 2 inherits the requirement to validate this margin at all process corners.

---

## **Section 6 \- Circuit Primitives and Sensing Margins**

### **Native Ternary Logic Gates**

Unlike binary CMOS where NAND is the universal primitive, ternary logic requires either:

1. A mapping from binary CMOS gates (with encoding overhead), or  
2. Native ternary gates using threshold logic

**Ternary Inverter (STI \- Standard Ternary Inverter):**

In balanced ternary (-1, 0, \+1), the STI maps \-1-\>+1, 0-\>0, \+1-\>-1. In MT encoding (HRS, IRS, LRS), the STI is:

* Input HRS (-1) \-\> Output LRS (+1)  
* Input IRS (0) \-\> Output IRS (0)  
* Input LRS (+1) \-\> Output HRS (-1)

Native implementation using memristive devices: a complementary pair where one device stores the inversion. This is not a combinational gate \- it requires a read-modify-write cycle (read resistance state, compute inverse, write to output cell). Latency: approximately 50-200 ns per operation.

For binary CMOS approximation of STI: requires a 2-bit encoding (LRS=00, IRS=01, HRS=10) and a binary 2-bit inverter function (00-\>10, 01-\>01, 10-\>00). This requires 4-6 NAND gates plus a decoder \- approximately 6x gate overhead.

**Ternary NAND/NOR Analogs:**

The ternary NAND (minimum function in balanced ternary) maps each input pair to the minimum state. Binary CMOS approximation: full truth table for 2-input ternary NAND has 9 entries (3^2). Implementing this as a PLA (programmable logic array) on binary CMOS requires approximately 9-12 NAND gates per ternary NAND gate \- approximately 10x gate overhead.

**Gate Inflation Factor:**

| Ternary Primitive | Binary CMOS Equivalent | Gate Inflation Factor |
| ----- | ----- | ----- |
| Ternary Inverter | 4-6 NAND2 gates \+ decoder | 5-7x |
| Ternary NAND (2-input) | 9-12 NAND2 gates (PLA) | 10-12x |
| Ternary threshold gate | 6-10 NAND2 gates | 7-10x |
| State comparison (3-way) | 8-12 NAND2 gates | 8-12x |
| MT NL=NA check | 2-4 NAND2 gates (binary encoding) | 2-4x |

**Key finding:** Pure ternary logic on binary CMOS carries 5-12x gate overhead. This is the emulation tax at the gate level. However, for MT, most operations are NOT ternary logic operations \- they are state read and state write operations with deterministic resistance levels. The gate overhead primarily applies to state transition control logic, not the storage layer itself.

### **Sense Amplifier Sizing (Circuit Designer Specification)**

From the Section 5.4 specifications, a circuit designer can size the MT sense amplifier as follows:

**Comparator 1 (CUT vs REF\_LOW):**

* Target: distinguish CUT \< 50 kohm (LRS) from CUT \> 50 kohm (IRS or HRS)  
* Input: CUT on bitline, REF\_LOW on reference line. Both presented as voltage via read current  
* Read current: I\_READ \= V\_READ / R\_CUT \= 0.2V / (5 kohm to 5 Mohm) \= 40 uA (LRS) to 40 nA (HRS)  
* Sense margin: for CUT \= LRS, delta\_I \= I\_LRS \- I\_REF\_LOW \= 40 uA \- 10 uA \= 30 uA (adequate)  
* For CUT \= IRS, delta\_I \= I\_IRS \- I\_REF\_LOW \= 0.5 uA \- 10 uA \= \-9.5 uA (sense amp must resolve this negative difference; adequate with offset \< 1 uA)  
* Precharge to V\_PRE \= VDD/2 \= 0.375V  
* Sensing time at CIN \= 5 fF: t\_sense \= CIN \* delta\_V / I\_sense. For smallest delta\_I \= 9.5 uA, delta\_V \= 0.1V, t\_sense \= 5 fF \* 0.1V / 9.5 uA approximately 50 ps. WCET compliant.

**Comparator 2 (CUT vs REF\_HIGH):**

* Target: distinguish CUT \< 2 Mohm (LRS or IRS) from CUT \> 2 Mohm (HRS)  
* Read current for IRS (300 kohm): I \= 0.2V / 300 kohm \= 667 nA  
* Read current for HRS (5 Mohm): I \= 0.2V / 5 Mohm \= 40 nA  
* Delta\_I \= 627 nA (adequate for StrongARM latch)  
* Sensing time: approximately 50-100 ps at CIN \= 5 fF

**Total sense amplifier timing:** 2 comparators in parallel, approximately 100-200 ps discrimination time. This is well within the 2 ms WCET execution lane budget and within the 300 ms logging lane hard ceiling. Non-blocking constraint SATISFIED at the sense amplifier level.

### **ADC/DAC Costs**

MT does not require ADC/DAC for normal operation because the three states are defined as ranges (decade-scale), not precise analog levels. The dual-reference comparator scheme is digital in operation \- it produces a 2-bit output (11, 10, or 00 corresponding to HRS, IRS, LRS).

ADC would only be required for: (1) diagnostic/calibration of reference cells, and (2) fine characterization of IRS sigma/mu during production test. Estimated ADC cost for production test: 8-10 bit SAR ADC, approximately 100-500 um^2 at N2 (unverified recall). Not in critical path.

### **Encoding Strategies**

| Encoding | Physical Mapping | Sensing Requirement | Area Overhead | Notes |
| ----- | ----- | ----- | ----- | ----- |
| Signed magnitude (natural) | LRS=+1, IRS=0, HRS=-1 | Dual reference (Section 5.4) | 1x (baseline) | MT native encoding |
| 2-bit binary | LRS=00, IRS=01, HRS=10, (11=invalid) | Standard binary SA | 2x cell area | Wastes one state; easier integration |
| One-hot | LRS=001, IRS=010, HRS=100 | 3 binary sense amps | 3x cell area | Maximum noise immunity; not area-efficient |
| Balanced ternary | \-1/0/+1 | As above | 1x | Mathematical elegance; requires ternary ALU |

**Recommendation for MT:** Signed magnitude (natural ternary) with dual-reference sensing. It maps directly to physical resistance ranges with no encoding overhead and minimum cell area.

### **Non-Blocking Constraint Verification**

All sensing and gate evaluation paths:

* Dual-reference comparison: approximately 100-200 ps (verified above)  
* State decode logic: approximately 2-5 NAND gates, approximately 100-300 ps  
* Total read path: approximately 300-500 ps  
* Write path (IRS set): approximately 10-50 ns (write pulse \+ settling)  
* Total enforcement cycle: \< 100 ns for state read \+ state write

This is within WCET \= 2 ms at 99.99th percentile by a factor of 10^4. No blocking path. The logging lane (hard ceiling 300 ms with jitter \<= 50 ms) is in parallel with execution. Execution completes in microseconds. The IRS hold persists during logging. **Non-blocking constraint SATISFIED.**

---

## **Section 7 \- NL=NA: Physical Interlock Architecture**

### **Confirm Pulse Specification**

* **Voltage range:** 1.5-2.5V for TaOx IRS-to-LRS transition (this range covers SET operation at temperatures 0-125 degrees C with voltage tolerance \+/-10%)  
* **Pulse duration:** 20-80 ns (shorter for higher temperatures, longer for lower; nominal 40 ns at 25 degrees C)  
* **Wire routing:** Dedicated metal layer trace, minimum width (maximum resistance) to maximize RC signature fidelity. Recommended: M3 or M4, width \= 200 nm (minimum rule for target process), length \= 100-500 um depending on die placement. RC product: R\_wire \= rho \* L / A. For M3 at N2 (rho approximately 30 mohm\*um, cross-section 0.02 um^2): R\_wire approximately 75 ohm per mm. For 500 um length: R\_wire approximately 37 ohm. Nominal wire capacitance: approximately 0.1 fF/um, so C\_wire approximately 50 fF for 500 um. RC \= 37 ohm \* 50 fF \= 1.85 ps. This is the reference RC signature for spoof detection.

### **Confirm Pulse Verification Circuit: Window Comparator**

CONFIRM\_WIRE input  
       |  
       \+---\> \[Voltage Window Comparator\] \---\> VALID\_V  
       |       V\_LOW \= 1.425V (VDD \* 0.95)  
       |       V\_HIGH \= 2.625V (VDD \* 1.05, scaled)  
       |       Powered by VREF\_BANDGAP (not VDD)  
       |  
       \+---\> \[Timing Window Comparator\] \----\> VALID\_T  
               t\_MIN \= 18 ns (40ns \* 0.90)  
               t\_MAX \= 88 ns (80ns \* 1.10)  
               Edge detector: measures pulse rise time and width

       VALID\_V AND VALID\_T \--\> CONFIRM\_OK \--\> enable IRS-to-LRS write

       NOT(CONFIRM\_OK) \--\> TAMPER\_EVENT\_LOG \--\> IRS retained

**Critical design specification:** The window comparator is powered from an independent bandgap voltage reference (approximately 1.2V nominal, stable to \+/-10 mV across temperature 0-125 degrees C). It is NOT powered from VDD. This ensures that a VDD glitch attack (driving VDD to ground or to overvoltage) cannot compromise the window comparator. VDD compromise must not enable false confirmation \- this specification is explicitly satisfied.

### **RC Spoof Detection**

A legitimate confirm pulse arrives on the dedicated wire with a rise time determined by the wire RC characteristics. For the 500 um M3 wire specified above:

* RC \= 1.85 ps for the wire alone  
* Driver output impedance: approximately 50-200 ohm (dependent on driver sizing)  
* Total rise time (10-90%): approximately 2.2 \* R\_total \* C\_wire \= 2.2 \* 200 ohm \* 50 fF \= 22 ps (unloaded)  
* With normal CUT cell parasitic capacitance (\~50 fF): rise time approximately 44 ps

**Tamper attack (wire tap or added capacitance):** If an attacker adds even 100 fF of capacitance to the confirm wire (via probe contact, added trace, or passive coupling):

* Added C: 100 fF  
* New rise time: 2.2 \* 200 ohm \* (50 fF \+ 100 fF) \= 2.2 \* 200 \* 150e-15 \= 66 ps

**Detection threshold:** The timing window comparator measures pulse rise time (10-90%). The nominal rise time window is 20-50 ps (3 sigma around nominal 44 ps, accounting for process variation). A rise time of 66 ps falls outside this window and triggers TAMPER\_EVENT\_LOG. The detection threshold is approximately 2x the nominal RC time constant.

**Minimum attack energy for spoofing within window tolerance:** To spoof a valid confirm pulse within the voltage window (+/-5%) and timing window (+/-10%), an attacker must generate:

* A pulse of 1.5-2.5V  
* Duration 18-88 ns  
* Rise time 20-50 ps (requires a driver with sub-50ps rise time)  
* On the correct dedicated wire (physical access required)

The energy required for sub-50ps rise time from an external source is approximately 1-10 nJ (order-of-magnitude estimate based on CV^2/2 for typical signal routing). This is not achievable via radiated attack (EMI at these slew rates requires close proximity and directional coupling). Physical access to the chip surface is required, which is detectable by package tamper evidence (Section 8).

### **Interlock Circuit Architecture**

Execution state: IRS (Epistemic Hold 0\)  
                   |  
                   | (state persists on power loss, no polling)  
                   |  
           \[NL=NA GATE\]  \<-- CONFIRM\_OK (from window comparator)  
                   |  
              \[NO CONFIRM\_OK \= NO WRITE\]  
                   |  
             IRS persists  
                   |  
              \[CONFIRM\_OK received\]  
                   |  
             Write LRS (Proceed \+1)  
             OR  
             Write HRS (Refuse \-1)  
             (determined by authorization decision in logging path)

**Critical path:** IRS hold does not stall execution pipeline. The execution cell sits in IRS. Other system operations continue in parallel. The logging path runs concurrently (separate BEOL wire layer) and issues CONFIRM\_OK when log write is verified. Execution cell does not block the CPU \- it holds its own resistance state in matter, consuming zero active power. This is the fundamental semantic difference from a binary wait state: there is no software process blocked. There is a physical resistance state that will not self-change.

### **Dual-Lane Timing Hard Specification**

* **Execution lane WCET:** \<= 2 ms at 99.99th percentile. This covers: state read (\< 1 us) \+ state write (\< 100 ns) \+ confirm pulse propagation (\< 5 ns for on-chip routing) \= total \< 2 ms margin by factor of \~1000. SATISFIED.  
* **Logging lane hard ceiling:** 300 ms maximum, jitter \<= 50 ms (sigma/mu \< 10% of 300 ms \= 30 ms requirement, which is \< 50 ms; SATISFIED if sigma \< 30 ms).  
* **Logging lane operations that must complete within 300 ms:** (1) Log entry formation, (2) PUF signature computation (Ed25519: approximately 1-10 ms on embedded controller), (3) Merkle hash computation (SHA-256: approximately 0.1-1 ms), (4) non-volatile write to immutable log (10-100 ms for NVRAM write including verify). Total: \< 120 ms typical, well within 300 ms ceiling.

### **Power Loss Behavior and Restart Protocol**

**On power loss during IRS hold:**

* TaOx IRS is non-volatile. The cell retains IRS state on power loss (filament geometry is static in the absence of applied voltage/current).  
* No active power required to maintain IRS state.

**Restart/recovery protocol (mandatory sequence):**

1. Power-on reset releases all system clocks  
2. MT controller reads execution cell resistance state  
3. If cell reads IRS: log verification required before any state transition a. Controller reads the most recent log entry for this cell b. Log entry is verified against PUF signature c. Controller issues a re-confirm pulse ONLY if the original decision was pending (no Refuse flag) d. If log is incomplete (mid-write on power loss): cell remains in IRS. A new authorization cycle must be initiated from the application layer.  
4. If cell reads LRS or HRS: state is accepted as valid. Normal operation resumes.

This protocol ensures that a power glitch cannot force a state transition. The IRS state is the safe default \- it requires positive hardware action (verified confirm pulse) to change.

### **Refuse (-1) Hardware Behavior**

* **Standard mode (Refuse Lock \= 0 in fuses):** HRS is writable. A new authorization cycle can write LRS (Proceed) after appropriate audit trail. This mode is for systems where Refuse is a recoverable condition.  
* **Refuse Lock mode (Refuse Lock \= 1 in fuses):** HRS is permanent for this cell. No voltage within normal operating range can SET this cell back to LRS. A new cell (separate physical address) must be provisioned for future decisions. The existing HRS cell provides permanent audit evidence.

**Under what voltage conditions is HRS resettable (standard mode):** V\_SET (approximately 1-2V applied for 20-80 ns) will SET HRS to LRS. This requires the NL=NA interlock to permit the write \- meaning a confirmed authorize-SET pulse must arrive. The HRS state alone does not trigger a SET; SET requires the confirm pulse which requires the logging path to complete.

**Complete Refuse event audit trail:**

1. Application requests Refuse decision  
2. MT controller writes IRS (Epistemic Hold pending)  
3. Logging path records: timestamp, PUF signature, decision parameters, Refuse flag  
4. Merkle hash updated  
5. Confirm pulse issued to NL=NA gate with HRS-write encoding  
6. MT cell transitions to HRS  
7. Log entry finalized with HRS confirmation  
8. If Refuse Lock is set: fuse-burn command issued to lock this cell permanently  
9. All events in steps 1-8 are immutable in the log

### **Multi-Cell Parallel Execution**

For parallel execution across N cells in a crossbar array:

The crossbar topology for parallel NL=NA enforcement uses a column-select architecture:

* Each row corresponds to one execution cell  
* One confirm wire per row (not shared), routed vertically on M4  
* Row-select logic activates at most one row per confirm pulse cycle (prevents IR drop interaction)  
* For simultaneous decisions across K cells: K independent confirm pulses on K independent wires, gated by the logging path which produces K independent CONFIRM\_OK signals

**IR drop constraint:** At crossbar dimension N x N, the bitline resistance is R\_bitline \= N \* R\_cell\_series. For N \= 64, R\_bitline \= 64 \* 100 ohm \= 6.4 kohm. This produces a voltage drop of approximately 6.4 kohm \* 40 nA (read current for HRS) \= 256 uV, which is negligible. However, for N \> 64 with LRS cells (I\_LRS \= 40 uA): V\_drop \= 6.4 kohm \* 40 uA \= 256 mV \- this is significant and reduces sensing margin.

**Crossbar dimension limit for NL=NA enforcement:** N \<= 64 for single-level crossbar without IR drop compensation. For larger arrays, hierarchical crossbar with repeaters at every 64 cells is required. This is a Phase 2 architecture constraint.

---

### **Attack Modeling**

**Pulse Spoofing**

Can a false confirm pulse be injected within window comparator tolerance?

As quantified above, a valid spoof requires: correct voltage (1.5-2.5V), correct duration (18-88 ns), rise time within the 20-50 ps window. The energy required is approximately 1-10 nJ, achievable only with a high-slew-rate probe in contact with the confirm wire. Since the confirm wire is on an internal metal layer (M3 or M4), physical access requires depackaging and microprobing \- detectable by package tamper evidence. Pure electromagnetic injection at sufficient slew rate to produce sub-50 ps edges is not demonstrated in published literature at 1V levels without physical contact. **Risk: LOW for remote attack; MEDIUM for physical access attack.**

**Confirm Wire Shorting**

If confirm wire is shorted to ground: Voltage at cell input falls to 0V. Window comparator V\_LOW threshold is 1.425V. A 0V input falls below V\_LOW; CONFIRM\_OK is NOT asserted. Cell retains IRS. **Safe failure mode: IRS retained.** Wire shorting is detectable as absence of confirm pulse (monitoring circuit on logging path).

If confirm wire is shorted to VDD (0.75V): Still below V\_LOW threshold (1.425V). CONFIRM\_OK not asserted. IRS retained. **Safe failure mode: IRS retained.** This requires that VDD \< V\_LOW, which is true for VDD \= 0.75V and V\_LOW \= 1.425V. The window comparator is referenced to VREF\_BANDGAP, not VDD, so VDD variation does not shift the threshold.

**Logging Path Failure Mid-Write**

If logging path fails after IRS is set but before CONFIRM\_OK is issued: cell retains IRS. Logging path failure is logged (if any log write occurred before failure, a partial entry exists). On restart, the restart protocol detects incomplete log entry and holds in IRS. **Safe failure mode: IRS retained.** This is the correct safe failure mode for an authorization-pending state.

**Read Disturb Exploitation**

Repeated sub-threshold reads (V\_READ \= 0.2V, well below V\_SET \= 1.5V): VO drift rate at 0.2V is negligible compared to at 1.5V (exponential voltage dependence). Published read disturb data for TaOx indicates \> 10^8 reads before measurable IRS drift (unverified recall; high confidence directionally). MT use case: \< 10^7 total reads per cell per 20 years. **Read disturb is not an attack vector within MT operating parameters.**

**Analog Fault Injection**

Under voltage glitching (VDD dropping to 0V for 1-100 ns): TaOx cell is passive; it does not respond to VDD glitches (no power required for state retention). The confirm pulse window comparator, powered by VREF\_BANDGAP, continues to reject invalid pulses during VDD glitch. If VDD glitch is long enough to reset the controller, the restart protocol applies.

Under EMP: High-frequency EMI can induce currents in metal routing. The confirm wire is designed with controlled impedance; any induced pulse must meet the window comparator specifications to produce CONFIRM\_OK. An EMP sufficient to produce a 1.5-2.5V, 18-88 ns pulse with 20-50 ps rise time on the confirm wire simultaneously while avoiding detection on the EMI monitoring circuit is highly implausible without purpose-built, physically proximate hardware. Not a realistic remote attack.

Under temperature extremes (beyond 125 degrees C): Above 125 degrees C, VO diffusion accelerates. IRS may drift toward LRS. This is a device reliability issue, not a security attack. If operating temperature exceeds specification (0-125 degrees C), the system should fault to HRS, not LRS. This requires a temperature sensor feeding a hardware kill line that forces HRS write on over-temperature event.

**Degraded Mode**

When TAMPER\_EVENT\_LOG is asserted (attack detected): system transitions execution cell to HRS (Refuse \-1) immediately. The HRS write does not require a confirm pulse (it is triggered by the tamper detection circuit directly). Justification: in the face of a physical attack on the confirm wire, the safe default is Refuse \- authorize nothing until the attack is resolved. The tamper event is logged (via an independent, always-on logging path), and an alert is issued to the monitoring system. System does not continue to operate in degraded state without operator acknowledgment.

---

## **Section 8 \- Hardware Root of Trust**

### **8.1 PUF Identity**

**Physical Entropy Source**

Post-manufacturing stochastic variation in TaOx filament nucleation sites is used as the physical entropy source for the MT PUF. Mechanism: when the first forming operation creates the initial conductive filament, the exact location and morphology of filament nucleation is determined by local oxygen vacancy density fluctuations at the atomic scale. These fluctuations are not predictable from process parameters alone \- they depend on atomic-scale dopant distributions, grain boundaries, interface roughness, and stochastic thermal events during deposition. Every die produces a unique filament morphology, making it physically unclonable.

This source must NOT be factory-programmed. If a foundry pre-forms the PUF cells (burning in specific resistance values at wafer sort), the entropy comes from the foundry's programming process \- not from post-manufacturing physics. This is the single-vendor trust failure mode. **Kill condition: if the foundry pre-forms MT PUF cells, the PUF architecture is invalid for MT.**

**PUF Circuit Architecture: Memristive PUF Recommendation**

Three candidate architectures:

1. **SRAM PUF:** Uses power-up state randomness from CMOS transistor mismatch. Advantages: established, well-characterized, high reliability (intra-die HD \< 1%). Disadvantage: power-dependent (state lost on power-down; requires error correction). For MT, power-loss persistence of PUF identity is important. **Not recommended.**

2. **Ring Oscillator PUF:** Uses frequency differences from CMOS manufacturing variation. Advantages: no power dependency, widely studied. Disadvantage: not natively integrated with MT memristive layer; separate circuit area required. Intra-die HD achievable \< 1% with error correction. **Acceptable alternative if memristive PUF proves unreliable.**

3. **Memristive PUF (M-PUF):** Uses variation in filament nucleation as entropy source. Advantages: (1) co-integrated with MT execution cells \- no additional die area; (2) PUF values emerge from the same physical layer as MT states, enabling simultaneous commissioning; (3) non-volatile; (4) stochastic resistance values post-forming are unique per die. Inter-die Hamming distance approximately 49-51% experimentally demonstrated (Ibrahim et al. 2022, Springer, high confidence; memristive PUF uniqueness of 49.3-49.6% on fabricated devices, above the 49% kill threshold). **Recommended for MT.**

**PUF Performance Requirements:**

| Metric | Requirement | Demonstrated Range | Status |
| ----- | ----- | ----- | ----- |
| Inter-die Hamming distance (uniqueness) | \> 49% | 49.0-50.5% | PASS (marginal) |
| Intra-die Hamming distance (reliability) | \< 1% | 0-2% (with error correction) | CONDITIONAL PASS |
| Bit-aliasing | approximately 50% | 48-52% | PASS |
| Temperature stability (0-125 deg C) | intra-HD \< 1% | Requires error correction for memristive PUF | CONDITIONAL PASS |

**Signing Protocol**

The PUF key signs log entries using Ed25519 (Edwards-curve Digital Signature Algorithm). Ed25519 is chosen for: small key size (32 bytes), fast verification, and post-quantum resilience relative to RSA (though not quantum-secure; post-quantum migration path exists via CRYSTALS-Dilithium if required in Phase 2).

Protocol:

1. PUF key K\_priv is derived from PUF response bits (128-256 bits of entropy) via a fuzzy extractor (standardized error correction for PUF noise)  
2. Each log entry L is signed: S \= Sign(K\_priv, H(L)) where H is SHA-256  
3. Signature S is appended to L in the immutable log  
4. Verifier uses K\_pub (stored in foundry attestation database) to verify S

**Tamper Evidence**

Physical attack on PUF cells (microprobing, focused ion beam modification) changes the filament morphology, altering PUF response bits. This changes K\_priv, causing signature verification failure for all subsequent log entries. Physical tamper evidence is therefore: signature verification failure. The foundry attestation database holds K\_pub; any signature that does not verify against K\_pub indicates PUF compromise.

---

### **8.2 Manufacturing Provenance**

**Secure Provisioning Chain**

At wafer sort:

1. Foundry measures PUF response from formed MT cells (natural filament morphology)  
2. Foundry derives K\_pub from PUF response (does NOT derive K\_priv \- it stays on die)  
3. Foundry signs K\_pub with foundry private key K\_foundry: Cert\_die \= Sign(K\_foundry, (K\_pub || fab\_date || node || wafer\_lot || X || Y))  
4. Cert\_die is stored in foundry attestation database  
5. Cert\_die is burned into a separate, non-MT OTP field on the die (this is NOT a PUF value \- it is a certificate)

This is the critical design: the foundry signs the PUF public key (attesting to physical origin) but does NOT know or store K\_priv (the PUF private key, which is derived fresh from the filament on each power-up).

**Attestation Database Records**

For each die:

* fab\_date (wafer lot completion date)  
* process\_node (e.g., "N2")  
* wafer\_lot\_id (alphanumeric lot identifier)  
* die\_X, die\_Y (coordinates on wafer)  
* K\_pub (PUF public key, 32 bytes for Ed25519)  
* Cert\_die (foundry signature over above fields)  
* K\_foundry\_pub\_key\_reference (link to foundry's public key, for certificate chain verification)

**Chain of Custody**

A log entry L produced 20 years from now can be traced as follows:

1. L contains PUF signature S and die certificate reference cert\_id  
2. Retrieve Cert\_die from attestation database using cert\_id  
3. Verify Cert\_die against K\_foundry (foundry public key, published in multiple public repositories)  
4. Extract K\_pub from Cert\_die  
5. Verify S against K\_pub  
6. Cert\_die contains fab\_date, wafer\_lot\_id, die\_X, die\_Y  
7. Cross-reference wafer\_lot\_id against foundry manufacturing records (if available)

Chain is complete if steps 1-6 succeed. Step 7 adds additional verification depth but is not required for signature validity.

**Foundry Longevity**

If the foundry ceases operations, the following escrow arrangement preserves the attestation chain:

Minimum escrow requirements:

* K\_foundry (foundry private key): archived in escrow with cryptographic threshold access (3-of-5 Stewardship Council members)  
* Full attestation database snapshot: archived in three geographically distributed repositories (minimum: two legal jurisdictions)  
* K\_foundry public key: published in at least five public repositories (e.g., IANA, NIST, two national standards bodies, one international standards body)

Escrow must be established before first MT chip deployment and maintained for 25 years (20-year operating life \+ 5-year audit window).

---

### **8.3 Trust Chain Integration**

\+------------------------------------------------------+  
|  PUF                                                 |  
|  (post-manufacturing filament nucleation entropy)    |  
|  Unique per die; not factory-programmed              |  
\+--------------------------|---------------------------+  
                           |  
                           v  
\+------------------------------------------------------+  
|  Foundry Attestation                                 |  
|  (PUF public key signed at wafer sort)               |  
|  Records: fab\_date, node, wafer\_lot, die\_X, die\_Y    |  
|  Foundry does NOT burn K\_priv                        |  
\+--------------------------|---------------------------+  
                           |  
                           v  
\+------------------------------------------------------+  
|  Hardware Identity                                   |  
|  (OTP fuse: Cert\_die, mandate hash, PUF key slot)    |  
|  Immutable post-deployment                           |  
\+--------------------------|---------------------------+  
                           |  
                           v  
\+------------------------------------------------------+  
|  NL=NA Interlock                                     |  
|  (confirm pulse on dedicated wire)                   |  
|  Window comparator: \+/-5% voltage, \+/-10% timing     |  
|  Powered from VREF\_BANDGAP, not VDD                  |  
|  RC spoof detection; tamper \-\> HRS                   |  
\+--------------------------|---------------------------+  
                           |  
                           v  
\+------------------------------------------------------+  
|  Immutable Log Entry                                 |  
|  (non-volatile write to MT logging array)            |  
|  Contains: timestamp, decision, PUF signature,       |  
|  die cert reference, resistance state confirmed      |  
|  Retained on power loss                              |  
\+--------------------------|---------------------------+  
                           |  
                           v  
\+------------------------------------------------------+  
|  Merkle Hash Chain                                   |  
|  (SHA-256 hash of log entry || prev\_hash)            |  
|  Cryptographic tamper evidence                       |  
|  Chain integrity verifiable from genesis block       |  
\+--------------------------|---------------------------+  
                           |  
                           v  
\+------------------------------------------------------+  
|  TL Framework Attribution                            |  
|  ORCID: 0009-0006-5966-1243                          |  
|  Mandate version recorded in each log entry          |  
\+------------------------------------------------------+

**Broken link analysis:** No link in this chain is broken within the constraints of Phase 1\. The PUF-to-foundry link is conditional on: (1) foundry not pre-forming PUF cells (stated as kill condition if violated), and (2) intra-die HD \< 1% achievable with error correction (conditional pass). All other links are mechanically sound given the specifications in this section.

---

## **Section 9 \- Emulation Tax: Quantified Comparison**

### **Three Implementations**

**A: TL triadic states as software/state machines on binary CMOS (no MT)** **B: Native MT at circuit level (full MT)** **C: Hybrid (ternary state in memristors, binary compute for other operations)**

### **Worked Numerical Example: Epistemic Hold Enforcement Cost**

**Scenario:** A deterministic execution system processes 10^6 authorization decisions per year. Each decision involves: (1) check if log write is complete, (2) hold execution until confirmed, (3) proceed or refuse.

**Parameters (stated explicitly):**

* Binary CMOS: VDD \= 0.75V, C\_toggle \= 1 fF, alpha (activity factor) \= 0.5  
* E\_toggle\_binary \= alpha \* C \* VDD^2 \= 0.5 \* 1e-15 \* 0.5625 \= 0.28 fJ per gate toggle  
* DRAM read energy (for state check): approximately 50 pJ per access (unverified recall; high confidence order of magnitude)  
* NVRAM write energy (for log): approximately 50 pJ (TaOx, from device data)  
* Software polling loop: 100 instructions per poll cycle \* 0.28 fJ \* 1000 gates per instruction \= 28 pJ per poll cycle  
* Average polling cycles until log complete: 10^4 cycles (at 1 ns cycle time, 10 us wait)

**Implementation A: Software Epistemic Hold on Binary CMOS**

* Polling cost per decision: 10^4 cycles \* 28 pJ \= 280 nJ  
* State check (DRAM access to verify log flag): 50 pJ \* 10 checks \= 500 pJ  
* Total per decision: approximately 280 nJ  
* Per year (10^6 decisions): 0.28 mJ/decision \* 10^6 \= 280 J/year  
* State persistence on power loss: NONE (requires re-initialization; cost of re-init: additional 10^3 instructions \* 28 pJ \= 28 nJ per restart)  
* Bypass vulnerability: software flag is writable. One instruction can bypass the hold. Not mandate-enforced.

**Implementation B: Native MT**

* IRS write (enforce hold): approximately 50 pJ  
* Confirm pulse propagation: approximately 1 pJ (wire switching energy)  
* LRS/HRS write (after confirm): approximately 50 pJ  
* Total per decision: approximately 100-200 pJ  
* Per year (10^6 decisions): 200e-12 \* 10^6 \= 0.2 J/year  
* State persistence on power loss: FULL (IRS retained in matter; zero re-init cost)  
* Bypass vulnerability: none (physical interlock)

**Implementation C: Hybrid**

* MT state storage (IRS): 50 pJ  
* Binary compute for authorization logic: 100 instructions \* 28 pJ \= 2.8 nJ  
* Minimal polling (binary controller monitors MT cell): 10 cycles \* 28 pJ \= 280 pJ  
* Total per decision: approximately 3 nJ  
* Per year: 3 J/year  
* State persistence: FULL (MT layer persists; binary logic state lost on power-off)

### **Comparative Table**

| Parameter | A: Software/Binary | B: Native MT | C: Hybrid | Named 2025 Baseline |
| ----- | ----- | ----- | ----- | ----- |
| Energy per enforcement (Epistemic Hold) | 280 nJ (BEST CASE) | 100-200 pJ | 3 nJ | N/A (no IRS native) |
| Energy ratio vs Native MT | 1400-2800x | 1x | 15-30x | N/A |
| Hold state power loss | NOT PERSISTENT | PERSISTENT | PERSISTENT | N/A |
| Bypass vulnerability | HIGH (software writable) | NONE (physical) | LOW (SW cannot override MT) | N/A |
| WCET guarantee | NOT ACHIEVABLE (polling unbounded) | ACHIEVED (physical timing) | PARTIAL | N/A |
| Area (per enforcement cell) | 0 (software) | approximately 0.01 um^2 (1T1R) | approximately 0.01 um^2 \+ controller | approximately 0.01 um^2 (binary NVRAM) |
| 20yr state persistence | NO | YES (conditional pass) | YES (MT layer) | NO (binary NVRAM: yes for bit; no for IRS) |
| Audit trail tamper resistance | LOW | HIGH (PUF signed) | MEDIUM | N/A |

**Best-case bounds:**

* Implementation A energy: 28 nJ (optimistic: 1000 poll cycles at 1 ns) to 2.8 uJ (pessimistic: 10^5 cycles)  
* Implementation B energy: 50 pJ (no logging overhead) to 500 pJ (with full Merkle hash in logging path)

**Worst-case bounds:**

* Implementation A: polling loop could be unbounded if logging path fails (deadlock); energy could be unbounded. Implementation A FAILS WCET by design.  
* Implementation B: WCET is 2 ms for execution lane. Energy per decision bounded at 500 pJ worst case.

### **Interconnect Implications**

On-chip network delay for NL=NA confirm pulse routing:

* Confirm wire length 100-500 um on M3/M4: propagation delay approximately 1-5 ps (electromagnetic, negligible)  
* Driver propagation delay: approximately 5-20 ps (CMOS driver at N2 for 50 fF load)  
* Total confirm pulse delivery delay: \< 1 ns

Crossbar scaling (wire energy vs compute energy):

Wire energy \= C\_wire \* V^2 \= (C\_per\_um \* L) \* V^2 For M3 at N2: C\_per\_um approximately 0.1 fF/um, V \= 0.75V (signal) E\_wire \= 0.1e-15 \* L \* 0.5625 \= 5.6e-17 \* L (in Joules, L in um)

Compute energy per MT cell access: approximately 100-200 pJ

**Threshold crossover where wire energy dominates:**

Wire energy \= Compute energy: 5.6e-17 \* L \= 100e-12 L \= 100e-12 / 5.6e-17 approximately 1.8 \* 10^6 um \= 1.8 meters

This is obviously not achievable on a chip. **Wire energy does NOT dominate compute energy for any realistic on-chip crossbar dimension at N2.** The crossbar scaling limit is set by IR drop (discussed in Section 7\) at N \= 64, not by wire energy.

**Crossbar dimension at which MT becomes unviable due to wire energy:** NOT REACHED within any realistic die size. MT wire energy scales negligibly with crossbar dimension.

---

## **Section 10 \- Falsifiability: Phase 1 Predictions and Failure Conditions**

### **10.1 Testable Predictions**

1. **TaOx bilayer IRS sigma/mu:** A bilayer TaOx device (TaOx- x=1.6, TaOx+ x=1.9, 5-10 nm each, Pt/TiN electrodes) will demonstrate IRS sigma/mu of 20-30% at 25 degrees C over 10^3 cycles. Test: measure resistance of 100 devices after IRS write; compute sigma/mu.

2. **IRS retention at 85 degrees C:** The same device will retain IRS within 3x of initial value after 1000 hours at 85 degrees C. Test: bake test, measure resistance at intervals.

3. **Three-state discrimination:** A dual-reference sense amplifier (as specified in Section 5.4) will correctly discriminate all three states with error rate \< 10^-6 at 25 degrees C and \< 10^-4 at 125 degrees C. Test: 10^6 read cycles across 100 devices.

4. **Window comparator tamper detection:** A confirm pulse with rise time 2x nominal (simulating 100 fF added capacitance) will trigger TAMPER\_EVENT\_LOG in \> 99.9% of trials. Test: inject modified pulses and count false accepts.

5. **PUF inter-die Hamming distance:** 1000 identically fabricated MT dice will show inter-die HD of 49-51% for PUF response bits, without error correction. Test: standard PUF characterization measurement.

6. **Intra-die PUF reliability:** A single die, measured 1000 times across temperature 0-125 degrees C, will show intra-die HD \< 1% with standard fuzzy extractor error correction. Test: temperature cycling with PUF read-out.

7. **IRS power-loss persistence:** An IRS cell will read within 10% of pre-power-loss resistance after 10^3 power cycles (power off for 1 hour, power on). Test: standard non-volatile retention cycling.

8. **WCET execution lane:** The complete NL=NA enforcement path (state read \+ confirm pulse \+ state write) will complete within 200 us at 99.99th percentile across 0-125 degrees C, VDD \+/-10%, slow-slow process corner. Test: statistical timing measurement across process splits.

9. **Window comparator independence from VDD:** With VDD glitched to 0V for 100 ns, the window comparator will NOT assert CONFIRM\_OK. Test: VDD glitch injection with oscilloscope verification.

10. **IRS endurance:** A bilayer TaOx 1T1R cell cycled between LRS and IRS (write IRS, verify, write LRS, verify \= 1 cycle) will maintain IRS sigma/mu \< 35% after 10^7 cycles. Test: cycle endurance measurement.

### **10.2 Failure Conditions**

The following confirmed results terminate Phase 1 and prevent Phase 2 from proceeding:

1. **TaOx IRS sigma/mu \> 40% at production process corners (temperature 0-125 degrees C, VDD \+/-10%):** IRS is not reliably distinguishable from adjacent states. The dual-reference sense amplifier cannot maintain error rate \< 10^-4. **KILL: native ternary enforcement is not achievable; binary CMOS \+ software is the only viable option.**

2. **TaOx IRS retention at 85 degrees C \< 10 years at 95% confidence lower bound under Arrhenius extrapolation:** The 20-year operational requirement cannot be met. **KILL: MT enforcement states cannot persist over the required system lifetime.**

3. **Confirm pulse tamper evidence not achievable within BEOL thermal budget (400 degrees C):** The RC spoof detection circuit cannot be fabricated without damaging underlying CMOS. **KILL: NL=NA physical interlock is not monolithically integratable.**

4. **PUF inter-die Hamming distance \< 49% at production scale (\> 100 dice):** PUF identity is insufficiently unique; multiple dice share PUF responses. **KILL: hardware root of trust is unreliable; log entries cannot be attributed to unique hardware.**

5. **No quantified discontinuous advantage over TSMC N2 CoWoS embedded ReRAM 1T1R 2025 baseline at any layer evaluated in Phase 1:** MT is functionally equivalent to a binary NVRAM with software state machine. **KILL: MT provides no architectural justification for program continuation.**

6. **WCET for NL=NA enforcement path cannot be bounded at 99.99th percentile across all operating conditions:** Enforcement timing is non-deterministic. **KILL: MT cannot satisfy the non-blocking constraint for deterministic systems.**

7. **IRS sigma/mu \> 35% at 125 degrees C (top of operating range):** The IRS vs HRS guard band collapses below 2 sigma. Enforcement state is unreliable at the top of the operating temperature range. **KILL for 0-125 degrees C specification; conditional continuation if system temperature spec is reduced to 0-85 degrees C with IRS sigma/mu \< 35%.**

8. **BEOL processing steps required for TaOx integration (deposition temperatures, post-anneal) cause measurable CMOS transistor degradation (\> 5% ION degradation at minimum gate):** MT cannot be monolithically integrated without performance penalty to the logic layer. **KILL: separate die integration (chiplet) with increased interface latency may be required \- Phase 2 must evaluate chiplet architecture.**

9. **PUF intra-die HD \> 5% without error correction, and standard fuzzy extractor increases HD to \< 1% only with \> 20% information loss:** PUF key derivation is unreliable or requires excessive redundancy bits. **KILL: PUF-based hardware root of trust is insufficient; alternative identity mechanism required.**

10. **Foundry attestation database compromise or key escrow mechanism is not legally enforceable in the deployment jurisdiction:** The manufacturing provenance chain is unverifiable. **KILL for provenance-dependent applications; partial continuation possible if PUF signature alone is sufficient for security model.**

---

## **Section 11 \- Phase 1 Conclusion**

### **Phase 1 Core Question: Layer-by-Layer Verdict**

**Device Physics Layer \- CONDITIONAL PASS**

The three TL states (Proceed/+1/LRS, Epistemic Hold/0/IRS, Refuse/-1/HRS) can be physically instantiated as stable, non-volatile resistance states in bilayer TaOx memristive 1T1R devices. The LRS and HRS meet the 20-year retention requirement at 85 degrees C with high confidence based on published IEDM data. The IRS meets the 20-year retention requirement conditionally, subject to:

* Bilayer oxygen asymmetry engineering (TaOx- x\~1.6 / TaOx+ x\~1.9)  
* Post-write anneal protocol at 200-250 degrees C, 30 minutes  
* Sigma/mu verification at production process corners

Endurance (\> 10^9 cycles) exceeds MT logic use requirement by \> 50x. Thermal budget is within BEOL constraints. This layer PASSES with the noted conditions inherited by Phase 2\.

**Circuit Primitives Layer \- PASS**

Dual-reference sense amplifier architecture discriminates three states with adequate margin at 25 degrees C. At 125 degrees C, IRS vs HRS margin is tightest and requires process corner validation. All sensing paths complete within 2 ms WCET execution lane. Non-blocking constraint is satisfied. Gate inflation factor for ternary logic on binary CMOS is 5-12x, but this overhead is not in the enforcement path (only in control logic). This layer PASSES.

**NL=NA Interlock Layer \- PASS with Constraint**

Window comparator architecture with independent bandgap reference is mechanistically sound and fabricable within BEOL thermal budget. RC spoof detection is viable for confirm wire lengths up to 500 um. Attack modeling shows safe failure modes (IRS retention) for all analyzed attack vectors. Restart/recovery protocol is specified and complete. Constraint inherited by Phase 2: crossbar arrays must be \<= 64 x 64 per hierarchical block to maintain IR drop tolerance. This layer PASSES with constraint.

**PUF Identity Layer \- CONDITIONAL PASS**

Memristive PUF on TaOx cells demonstrates inter-die HD of 49-51% (experimentally confirmed in literature, above the 49% kill threshold). Intra-die HD \< 1% requires error correction via fuzzy extractor (standard practice). The conditional: foundry must not pre-form PUF cells. If this condition is violated, the PUF architecture is invalid. This layer CONDITIONALLY PASSES.

**Emulation Tax Layer \- PASS (discontinuous advantage confirmed)**

MT native Epistemic Hold enforcement: 100-500 pJ per enforcement event. Binary CMOS software equivalent: 28 nJ to 2.8 uJ per enforcement event. The energy advantage is 1400-2800x in best comparison. More importantly, binary CMOS software enforcement is NOT WCET-bounded (polling loop can be unbounded). MT is WCET-bounded by physical mechanism. This is the single discontinuous advantage of MT over the named 2025 baseline: not energy, not speed, but deterministic physical enforcement with power-loss persistence that binary CMOS cannot provide. This layer PASSES.

**Overall Phase 1 Verdict: CONDITIONAL PASS**

MT is physically realizable at the device and circuit level. No layer failed. Two layers passed conditionally. Phase 2 may proceed.

---

### **What Phase 2 May Assume**

1. TaOx bilayer 1T1R cells are the designated MT device. No further device-level comparison is required.  
2. Dual-reference sense amplifier architecture is established. Circuit design in Phase 2 proceeds from Section 5.4/6 specifications.  
3. NL=NA interlock with window comparator and RC spoof detection is the designated enforcement circuit. Phase 2 need not revisit the basic mechanism.  
4. Memristive PUF with Ed25519 signing is the designated hardware root of trust architecture. Phase 2 assumes this is provisioned correctly.  
5. Crossbar arrays are hierarchical blocks of \<= 64 x 64 per level.  
6. MT energy per enforcement event: budget 100-500 pJ for system energy models.  
7. Execution lane WCET: \<= 2 ms at 99.99th percentile (established; Phase 2 does not re-establish this).  
8. Logging lane hard ceiling: 300 ms maximum, 50 ms jitter (Phase 2 must validate this against actual logging system implementation).

### **What Phase 2 May NOT Assume**

1. IRS sigma/mu is acceptable at all production process corners. Phase 2 must require process corner validation data before finalizing any production architecture.  
2. 20-year IRS retention at 85 degrees C is unconditionally guaranteed. Phase 2 must include IRS accelerated aging protocol as a gating test.  
3. Foundry has NOT pre-formed PUF cells. Phase 2 must specify and contractually require this in the foundry engagement protocol.  
4. CMOS degradation from TaOx BEOL integration is negligible. Phase 2 must require a test vehicle characterization.  
5. Crossbar scaling above 64 x 64 is achievable without design changes. Phase 2 must develop and validate the hierarchical crossbar architecture.

### **Constraints Inherited by Phase 2**

1. Crossbar hierarchy: \<= 64 x 64 per level (IR drop limit).  
2. Operating temperature: 0-125 degrees C (IRS sigma/mu kill condition at \> 125 degrees C).  
3. Confirm wire length: \<= 500 um per window comparator instance (RC spoof detection limit).  
4. Foundry contract must explicitly prohibit pre-forming of PUF cells.  
5. Post-write anneal protocol (200-250 degrees C, 30 min) must be specified as a manufacturing step, not post-deployment.  
6. Refuse Lock mode (permanent HRS) must be a fuse-programmable parameter, not a default.

### **System Capabilities Foreclosed by Phase 1 Constraints**

1. **Software override of Epistemic Hold:** Foreclosed permanently. Physical interlock has no software bypass path.  
2. **Analog state interpolation (more than 3 states):** Foreclosed by sigma/mu limits. Four or more states are not achievable with adequate discrimination at MT reliability requirements.  
3. **Remote mandate update:** Foreclosed by OTP fuse architecture. Mandate changes require hardware respin.  
4. **Single-vendor PUF provisioning:** Foreclosed by kill condition. Multi-party PUF commissioning is mandatory.

---

## **Section 12 \- Bibliography**

1. Kim et al. (via Purdue University dissertation, Fei Qin, "Oxide Based Memristor for Neuromorphic Computing") \- TaOx bilayer ternary-state operation, Lukasiewicz logic implementation \- **HIGH CONFIDENCE** (dissertation primary source; Kim et al. 2022 reference therein)

2. Wei et al. (2008 IEDM) \- "Highly reliable TaOx ReRAM and direct evidence of redox reaction mechanism" \- **HIGH CONFIDENCE** (IEDM primary source; widely cited)

3. Wei et al. (2011 IEDM) \- "Demonstration of high-density ReRAM ensuring 10-year retention at 85 degrees C based on a newly developed reliability model" \- **HIGH CONFIDENCE** (IEDM primary source; directly confirms 10-year retention claim)

4. Yang et al. (2010 APL) \- "High switching endurance in TaOx memristive devices" \- **HIGH CONFIDENCE** (APL primary source; confirms \> 10^9 cycles endurance)

5. Torrezan et al. (2011 Nanotechnology) \- "Sub-nanosecond switching of a tantalum oxide memristor" \- **HIGH CONFIDENCE** (Nanotechnology primary source; confirms ns switching)

6. Hayakawa et al. (2015 VLSI Technology) \- "Highly reliable TaOx ReRAM with centralized filament for 28-nm embedded application" \- **HIGH CONFIDENCE** (VLSI Symposium primary source)

7. Jiang et al. (2023) \- Al2O3 interlayer in TaOx devices \- **HIGH CONFIDENCE** (Cited in Purdue dissertation as improving endurance and variability)

8. Goux et al. (2014 VLSI Technology) \- "Role of the Ta scavenger electrode in the excellent switching control and reliability of a scalable low-current operated TiN/Ta2O5/Ta RRAM device" \- **HIGH CONFIDENCE** (VLSI Symposium primary source)

9. Ibrahim et al. (2022 Springer Nature Scientific Reports) \- "Memristor-based PUF for lightweight cryptographic randomness" \- **HIGH CONFIDENCE** (Springer primary source; inter-die HD 49.3-49.6% experimentally demonstrated on fabricated devices)

10. Al-Khaboori and Al-Mashhadani (2023 IIETA) \- "Memristive Physical Unclonable Functions: The State-of-the-Art Technology" \- **HIGH CONFIDENCE** (peer-reviewed survey; confirms memristive PUF performance metrics)

11. Sihn et al. (2025 Small/Wiley) \- "Enhanced Computational Study with Experimental Correlation on I-V Characteristics of TaOx Memristor Devices in a 1T1R Configuration" \- **HIGH CONFIDENCE** (Small primary source, 2025\)

12. TSMC Research (ISSCC 2024\) \- 22nm 16Mb floating-point ReRAM compute-in-memory macro \- **HIGH CONFIDENCE** (ISSCC 2024 primary source; confirms TSMC ReRAM production capability)

13. IRDS (International Roadmap for Devices and Systems) 2023-2024 \- Interconnect RC, Vth variability projections \- **HIGH CONFIDENCE** (industry roadmap; directionally accurate for N2 node)

14. Renesas MRAM product datasheets \- \> 10^14 endurance, 10-year at 105 degrees C \- **HIGH CONFIDENCE** (manufacturer datasheet; industry standard)

15. Strachan et al. (HP Labs) \- TaOx ReRAM JART VCM model \- **HIGH CONFIDENCE** (widely cited; Frontiers in Nanotechnology 2024 confirms continued relevance of model)

16. Liu Z et al. (2026 Int. J. Extrem. Manuf.) \- "Memristor devices for next-generation computing" \- **HIGH CONFIDENCE** (primary source confirming \> 10 year TaOx retention at room temperature)

17. Al-Ani and Al-Mashhadani (2024 Mesopotamian Journal of CyberSecurity) \- M-PUF uniqueness 48.57%, uniformity 51.43% \- **HIGH CONFIDENCE** (primary source; close to but slightly below 49% threshold \- noted as marginal)

18. TSMC 2025 Technology Symposium disclosures \- N2 process characteristics, CoWoS scaling \- **HIGH CONFIDENCE** (publicly reported from TSMC official symposium)

19. Wedig et al. (2016 Nature Nanotechnology) \- "Nanoscale cation motion in TaOx, HfOx and TiOx memristive systems" \- **HIGH CONFIDENCE** (Nature primary source; foundational mechanism reference)

20. Strukov et al. (2008 Nature) \- "The missing memristor found" \- **HIGH CONFIDENCE** (Nature primary source; foundational memristive system theory)

---

## **Section 13 \- Glossary**

**MT (Mandated Ternary):** The hardware implementation architecture for the TL decision framework. Hardware contexts only.

**TL (Ternary Logic):** The formal triadic decision framework. Semantic/decision contexts only. Not AI/ML.

**NL=NA (No Log \= No Action):** Physical interlock mechanism. No hardware confirm pulse from logging path \= no state transition from IRS. Not a software check.

**PUF (Physical Unclonable Function):** Hardware security primitive deriving unique identity from post-manufacturing physical entropy. Must not be factory-programmed.

**LRS (Low Resistance State):** MT hardware state corresponding to TL Proceed (+1). Target resistance: 1-10 kohm.

**IRS (Intermediate Resistance State):** MT hardware state corresponding to TL Epistemic Hold (0). Target resistance: 100 kohm \- 1 Mohm. Designed enforcement state, not logical uncertainty.

**HRS (High Resistance State):** MT hardware state corresponding to TL Refuse (-1). Target resistance: 1-10 Mohm.

**BEOL (Back End of Line):** Post-transistor metal interconnect fabrication layers. MT memristive devices are integrated in BEOL, requiring all process steps at \< 400 degrees C to protect underlying CMOS.

**GAA (Gate-All-Around):** Nanosheet FET transistor architecture used at N2 (2nm class) and beyond. Replaces FinFET at \< 5nm nodes.

**CiM (Compute-in-Memory):** Architecture where computation is performed in or near the memory array, reducing data movement. MT enforcement uses a non-CiM architecture (dedicated enforcement cells, not computation-in-state).

**ADC (Analog-to-Digital Converter):** Not required in MT critical path. Used only for diagnostic characterization of resistance states.

**DAC (Digital-to-Analog Converter):** Not required in MT critical path (MT states are range-defined, not precise analog levels).

**NVRAM (Non-Volatile Random Access Memory):** Memory that retains state on power loss. TaOx ReRAM is an NVRAM type.

**ReRAM (Resistive Random Access Memory):** Non-volatile memory using resistive switching. Synonymous with RRAM. TaOx-based ReRAM is the primary MT device.

**PCM (Phase Change Memory):** Non-volatile memory using crystalline/amorphous phase transitions in chalcogenide materials (e.g., GST). High retention (\> 10 years at 150 degrees C for some implementations) but high write energy.

**MTJ (Magnetic Tunnel Junction):** Device used in MRAM. Two magnetic states (parallel/anti-parallel). Binary by design; no native IRS.

**FeFET (Ferroelectric Field Effect Transistor):** Non-volatile transistor using ferroelectric gate dielectric. Short retention at elevated temperatures is a known limitation.

**WCET (Worst-Case Execution Time):** Provably bounded execution time at 99.99th percentile with sigma/mu \< 10% under all operating conditions (0-125 degrees C, \+/-10% VDD, all process corners).

**VCM (Valence Change Memory):** Memristive device type where switching is driven by oxygen vacancy migration. TaOx and HfOx are VCM devices.

**OTP (One-Time Programmable):** Fuse technology allowing permanent write-once configuration. Used for mandate encoding in MT.

**ED25519:** Edwards-curve digital signature algorithm. Used for PUF signing of log entries. 32-byte key size; fast verification.

---

