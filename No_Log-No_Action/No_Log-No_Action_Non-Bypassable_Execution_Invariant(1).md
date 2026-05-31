# No Log = No Action: Non-Bypassable Execution Invariant Specification for Ternary Logic

> 🌐 **Interactive Web Version:** [No_Log-No_Action_Non-Bypassable_Execution_Invariant.html](https://fractonicmind.github.io/TernaryLogic/No_Log-No_Action/No_Log-No_Action_Non-Bypassable_Execution_Invariant.html)

---

## I. Problem Definition: Optional Logging Failure

Traditional computing and control architectures treat logging as a telemetry concern, decoupled from execution by asynchronous buffering, deferred writes, and best-effort delivery semantics. In such systems, the execution path and the persistence path are independent: an action completes on the main processor pipeline while a log entry is enqueued in a memory buffer, forwarded through a network stack, and eventually written to a storage backend. This architectural separation introduces non-determinism between execution and persistence, because the temporal ordering of action completion and log commitment is not enforced by any structural constraint. Actions routinely complete while their corresponding log entries remain in volatile buffers, transit queues, or write-back caches, any of which may be lost to power interruption, process termination, memory pressure eviction, or network partition. The result is that the observability layer provides a probabilistic, best-effort record of system behavior rather than a deterministic, complete, and tamper-evident proof of every externally visible effect.

The failure modes of optional logging are numerous and well-characterized. Log entries may be dropped silently when buffer capacity is exhausted under sustained load, producing gaps in the record that are indistinguishable from periods of legitimate inactivity. Log entries may be reordered when multiple producers write concurrently to shared aggregation points without enforced serialization, destroying the causal ordering that reconstruction requires. Log entries may never be written at all if the logging subsystem crashes, is deliberately suppressed by an adversary with kernel-level or hypervisor-level privilege, or is bypassed by execution paths that were never instrumented. In each of these cases, the system has acted, the external world has been affected, and no corresponding record exists to prove, reconstruct, or audit what occurred.

Post-hoc reconstruction, the standard forensic technique applied when logs are incomplete, is fundamentally unreliable under these conditions. Reconstruction depends on correlating timestamps across distributed components, but clock skew, NTP drift, and deliberate clock manipulation introduce timing inconsistencies that make causal ordering ambiguous. Reconstruction depends on cross-referencing partial records from multiple sources, but partial data loss means that the very entries needed to disambiguate conflicting evidence are the ones most likely to be missing. Under adversarial conditions, an attacker with sufficient privilege can selectively delete, modify, or forge log entries, rendering post-hoc analysis not merely incomplete but actively misleading.

Two classes of execution path are particularly dangerous because they reach physical interfaces without traversing any software logging stack. Emergency shutdown sequences in industrial control systems and safety instrumented systems are designed to bypass normal software layers entirely, driving actuators through dedicated hardware circuits to achieve minimum-latency response to hazardous conditions. While this bypass is justified by safety requirements, it creates an unlogged action window during which the system transitions through states that leave no record. Direct hardware manipulation paths, including Direct Memory Access (DMA) and memory-mapped I/O (MMIO), present an even more severe threat. DMA-capable peripherals, including network interface controllers, GPUs, storage controllers, and any device connected via Thunderbolt, PCI Express, or USB4, can read and write physical memory without CPU intervention or software mediation. A compromised or malicious DMA-capable device can directly write to actuator control registers mapped into the physical address space, triggering externally observable effects with no software-layer awareness and therefore no logging.

IOMMU protections are insufficient for three documented reasons: early boot gaps where IOMMU translation tables are not yet enabled allow DMA before the protection is active; deferred DMA attacks exploit stale mappings that persist after virtual machine destruction; and message-signaled interrupt (MSI) forgery bypasses IOMMU enforcement entirely by forging interrupt signals that trigger processor actions without any DMA transaction appearing in the IOMMU's translation tables. The conclusion is inescapable: telemetry-grade logging provides observability but not enforcement, and any architecture that permits action without structurally guaranteed prior log commitment cannot provide the evidentiary integrity that Ternary Logic demands.

---

## II. The Invariant: No Log = No Action

This specification defines the No Log = No Action invariant as a structural execution constraint within the Ternary Logic framework, requiring that no state transition, transaction, API call, or physical actuation may be released unless a corresponding log entry has been fully committed to a local hardware-backed non-volatile accumulator. The invariant is not a policy, a configuration parameter, or a software check; it is an architectural coupling enforced through the physical topology of the execution path, such that the electrical and logical prerequisites for action release include cryptographic proof of prior log persistence.

In the DITL/MT hardware substrate, this coupling is material. The Commit Gate stands physically in-line on the actuation path. Its resistance state, determined by the TaOx ReRAM cell through the Window Comparator, determines whether the actuation signal propagates. The NL=NA write pulse, a voltage pulse on a dedicated hardware wire, is the only mechanism that can transition the Commit Gate to Low Resistance State (LRS, Proceed). No instruction in the processor's ISA, no DMA transfer, no firmware call, and no software privilege level has access to this wire.

### II.1 Formal Transition System Definition

The invariant is defined over a transition system TS = (S, Act, T, I, AP, L) where S is the set of system states, Act is the set of actions, T ⊆ S × Act × S is the transition relation, I ⊆ S is the set of initial states, AP is the set of atomic propositions, and L : S → 2^AP is the labeling function. Two atomic propositions are distinguished: log(a), which holds when a log entry for action a has been fully committed to durable storage with integrity verified, and exec(a), which holds when action a has produced an externally observable effect or state mutation.

### II.2 LTL Specification

The primary invariant in Linear Temporal Logic, using the precedence pattern with strict Until operator semantics as formalized by Dwyer, Avrunin, and Corbett, is:

```
For all actions a: ◇exec(a) → (¬exec(a) U (log(a) ∧ ¬exec(a)))
```

This formula states that if exec(a) ever occurs on any execution trace, then exec(a) must not hold until log(a) holds, and at the moment log(a) first holds, exec(a) must still be false. The Until operator is strict: it requires that log(a) eventually becomes true and that exec(a) remains false at every position strictly before and including the position where log(a) is first satisfied.

In past-time LTL, the equivalent formulation is:

```
□(exec(a) → O(log(a)))
```

stating that at every point in every trace, if exec(a) holds then log(a) must have held at some strictly earlier position, where O is the Once operator with standard past-time semantics.

### II.3 CTL Specification

In Computation Tree Logic, the invariant is expressed over all paths from all reachable states:

```
¬E[¬log(a) U exec(a)]
```

asserting that there exists no computation path on which exec(a) occurs while log(a) has not yet held. Equivalently:

```
A[¬exec(a) W log(a)]
```

states that on all paths, exec(a) does not occur until log(a) has occurred, where the Weak Until operator W permits the possibility that log(a) never occurs, in which case exec(a) never occurs either, which is the correct fail-closed behavior. The strongest formulation combines universal path quantification with the state predicate:

```
AG(∀a ∈ Act : exec(a) → logged(a))
```

where logged(a) is a state predicate asserting that a complete, hash-verified, integrity-confirmed log entry for a exists in the committed log store.

### II.4 Log Completeness Definition

Log completeness is defined as the conjunction of four conditions.

**Canonical serialization:** the log entry is produced through deterministic serialization conforming to a fixed canonical form such as JCS (RFC 8785) or deterministic CBOR, ensuring that semantically identical records always produce identical byte sequences.

**Cryptographic hashing:** the canonicalized byte sequence is processed through a collision-resistant hash function, producing a digest included in the Merkle accumulator and linked to the preceding entry via hash chain. In DITL/MT deployments, the PUF binding hash SHA3-256(K_PUF ∥ device_serial_OTP ∥ log_session_nonce) is appended, binding every log entry to the specific physical silicon instance.

**Physical persistence:** the entry and its hash are written to a hardware-backed non-volatile storage element (TaOx 1T1R ReRAM on the TSMC N2 CoWoS baseline, MRAM, nvSRAM, or battery-backed SRAM in other configurations) that retains data across power loss without depending on any software-controlled write-back mechanism. Arrhenius-model retention on the named baseline is 20 years at 85 degrees C.

**Read-back confirmation with integrity check:** after the write completes, the storage subsystem reads back the written data, recomputes the hash, and confirms that the read-back hash matches the originally computed hash, verifying that the data was physically persisted correctly. Only after all four conditions are satisfied does log(a) evaluate to true.

### II.5 Action Definition

Action is defined as any externally observable effect or state mutation, encompassing network packet transmission, actuator signal assertion, database write commitment, API response delivery, financial transaction settlement, sensor reading publication, and any modification to shared state visible to processes or systems outside the logging boundary. Internal intermediate computations that produce no externally observable effect are not actions under this definition.

### II.6 Inductive Proof Obligations

Let Inv(s) ≡ ∀a ∈ Act : executing(a, s) → ∃e ∈ Log(s) : (e.action = a) ∧ (e.timestamp < exec_time(a, s)) ∧ verified(e.hash, s).

The base case requires that for all initial states s₀ ∈ I, Inv(s₀) holds; this is satisfied because no actions are executing in any initial state.

The inductive step requires that for all states s and s' such that Inv(s) holds and T(s, a, s') is a valid transition, Inv(s') holds; this is established by the structural constraint that the transition relation T is physically gated such that no transition producing exec(a) in s' can fire unless log(a) is committed in s before the transition.

The strengthening condition requires that Inv(s) implies the safety property AG(∀a : exec(a) → logged(a)), which follows directly from the definition of Inv. These obligations can be discharged through symbolic model checking using BDD-based or SAT-based bounded model checking, with the transition system encoding the hardware gate logic, the logging subsystem state machine, and the actuator release mechanism.

### II.7 The Five-Layer NL=NA Enforcement Stack

The invariant is enforced through five independent layers. Bypassing one layer does not bypass the others. Every Proceed (+1) authorization must pass all five. Layer 5 is the terminal constitutional gate.

**Layer 1 (Schema):** State Envelope if/then constraint. The permissionToken field is REQUIRED whenever currentState equals +1 (Proceed). No schema-valid Proceed response exists without a permission token.

**Layer 2 (Schema):** PermissionToken.laneOrigin carries the constant value "GOVERNANCE_LANE". Inference Lane tokens are schema-invalid by construction. No token originating outside the Governance Lane can authorize execution.

**Layer 3 (Schema):** TGLF-StateP1.permissionToken is in the required array, with pillarsCertified at minItems 8 and maxItems 8. A Proceed log entry that omits the permission token or carries incomplete pillar certification fails schema validation.

**Layer 4 (Schema):** AuditProof cross-reference. AuditProof.logHash and AuditProof.merkleRoot must match PermissionToken.logHash and PermissionToken.merkleRoot. Mismatched values indicate forgery or accumulator divergence.

**Layer 5 (On-chain ABI):** TL_Ledger_Core.registerPermissionToken reverts with NLNAViolation if logHash is not provably contained in the anchored Merkle root. This is the terminal constitutional gate in silicon and on-chain.

In DITL/MT deployments, Layer 5 is reinforced at the physical level: the Commit Gate and Window Comparator enforce the same constraint in silicon independently of Layer 5's on-chain check. In Architecture B deployments, the NULL_PUF_DEPLOYMENT sentinel in the NLNAAuditToken and TLCapabilityFlags.pufAttestationMode: "ARCHITECTURE_B" record the deployment mode honestly in every audit log.

---

## III. Cryptographic Actuator Interlock and Execution Coupling

The No Log = No Action invariant transforms logging from an observability mechanism into a protocol-level gate embedded directly in the execution path, enforcing a strict write-before-release model in which no externally observable effect can occur without prior cryptographic proof of log commitment. This enforcement is achieved through a cryptographic actuator interlock that couples the physical or logical release of every action to the presentation and verification of a valid execution capability token derived from the committed log state.

### III.1 Merkle Accumulator Root as Capability Token

The core mechanism is a Merkle accumulator whose root hash serves as the current execution capability token. The Merkle accumulator is an append-only binary hash tree in which each leaf corresponds to a committed log entry, and internal nodes are computed as the hash of their children's concatenation. The root hash of this accumulator is stored in a hardware-protected register, accessible only to the logging subsystem and readable by the actuator interlock, but not writable by any other component regardless of privilege level.

This register resides within a hardware trust boundary, implemented through a secure enclave, a dedicated FPGA fabric region, or an ASIC-embedded register file with hardware-enforced access control. Modification of the Merkle root register requires presentation of a valid new root derived from appending a verified log entry to the accumulator, computed and verified entirely within the logging subsystem's trust boundary. Any attempt to execute an action without presenting a valid capability token that matches the current Merkle root triggers an immediate fault condition, halting the action and initiating a safe harbor transition.

### III.2 Triple Cryptographic Requirements for Release

Actuator release requires the simultaneous satisfaction of three independent cryptographic requirements.

**First:** valid log hash with demonstrated preimage resistance and collision resistance; the hash must correspond to a canonicalized log entry whose preimage is available for verification, and the hash function must provide at minimum 128-bit collision resistance.

**Second:** hardware-generated attestation quote; a TPM-generated or enclave-generated signed statement binding the current Merkle root, a monotonic counter value, and a freshness nonce, signed by a key that is resident within the hardware trust boundary and has never been exposed in plaintext outside that boundary. In DITL/MT deployments, the PUF binding hash is included, binding the quote to the specific silicon instance.

**Third:** inference containment verification; for systems operating within the Ternary Logic decision framework, the log entry must include the complete decision vector, the TL state reached (Proceed +1, Epistemic Hold 0, or Refuse -1), and the confidence metrics that determined the state, ensuring that the decision process is fully captured before its result is released.

### III.3 Non-Bypassability: Software and Firmware

This specification states explicitly that no administrative privilege, software override, hypervisor code, or System Management Mode firmware can bypass execution gating. The actuator interlock operates at a layer below all software privilege levels: the electrical path from the decision logic to the external actuator or output interface physically traverses the interlock hardware, and there is no alternate routing that circumvents it.

A compromised kernel cannot bypass the interlock because the kernel has no write access to the Merkle root register. A compromised hypervisor cannot bypass the interlock because the interlock's trust boundary is independent of the hypervisor's memory management. SMM code cannot bypass the interlock because the interlock is implemented in dedicated hardware, such as an FPGA fabric or ASIC gate, that is not addressable from the SMM address space.

### III.4 Non-Bypassability: DITL/MT Physical Layer

In DITL/MT deployments, non-bypassability extends to the silicon layer. The Muller C-element, the fundamental gate primitive of DITL, cannot generate an output without complete verified input from all input channels. If any required log commitment signal is absent, the Muller C-element does not produce output; it holds indefinitely. No timing assumption, clock manipulation, or voltage glitch can advance it past an incomplete input state.

The Commit Gate stands in-line on the actuation path. Its state is determined by the TaOx ReRAM resistance as measured by the Window Comparator. The Window Comparator is fail-closed: any resistance reading outside valid windows causes it to assert HRS (Refuse -1). The NL=NA write pulse is the only mechanism that sets the TaOx cell, and it is a voltage pulse on a dedicated wire outside the processor's ISA. The topology is series, not parallel: the actuation signal physically cannot bypass the Commit Gate.

### III.5 Transactional Commit Semantics

Each action proposal initiates a transaction that proceeds through a deterministic state sequence: Idle → Proposed → Logging → Committed → Executing → Complete. The transition from Logging to Committed occurs only when all four log completeness conditions are satisfied. The transition from Committed to Executing occurs only when the three cryptographic requirements are simultaneously verified. If any condition fails at any stage, the transaction aborts and the system returns to Idle; partial completion is not possible, and no externally observable effect occurs.

---

## IV. DITL/MT Hardware Substrate

### IV.1 Architecture and Terminology

Two terms govern the hardware layer. DITL (Delay-Insensitive Ternary Logic) is the asynchronous circuit substrate. MT (Mandated Ternary) is the hardware implementation layer that maps TL governance states to silicon-level conditions. These are not synonyms: DITL names the circuit architecture; MT names the governance-to-silicon mapping.

The named hardware baseline is TSMC N2 CoWoS with embedded TaOx 1T1R ReRAM, 2025 PDK, with Arrhenius-model 20-year retention at 85 degrees C.

### IV.2 Voltage Domain and Resistance State Mapping

The three TL constitutional states are physically encoded:

| TL State | Value | Resistance State | Resistance Range | Voltage |
|----------|-------|-----------------|-----------------|---------|
| Proceed | +1 | LRS | ~1-10 kΩ | 3.3V |
| Epistemic Hold | 0 | IRS | ~100 kΩ - 1 MΩ | 1.65V |
| Refuse | -1 | HRS | ~1-10 MΩ | 0V |

These are physical conditions in silicon, not software-assigned values. The significance is categorical: governance states cannot be overwritten by any instruction in any privilege ring. They can only be changed by the NL=NA write pulse, which applies a calibrated voltage pulse to the TaOx cell through the dedicated hardware wire.

IRS variability (sigma/mu of 20-35% cycle-to-cycle) is the binding constraint for this resistance layer. It does not render IRS unusable, but it requires differential sensing margins wider than conventional NVRAM practice, implemented through the Window Comparator's dual reference cell architecture.

### IV.3 DITL Circuit Architecture

The Muller C-element is the fundamental gate primitive. Its behavioral property is the enforcement primitive: output cannot be generated without complete, verified input from all channels. This property implements NL=NA at the gate level.

Three-voltage single-wire encoding: Vdd (+1), Vdd/2 (0), GND (-1). No global clock; the circuit is genuinely asynchronous. Request/acknowledge handshake signaling between stages. Inline (series) topology required: any parallel (sidecar) topology creates an alternate path around the enforcement gate and is constitutionally insufficient.

### IV.4 Physical Enforcement Mechanisms

#### IV.4.1 Window Comparator

The Window Comparator measures TaOx cell resistance using an independent bandgap reference stable across 0-125 degrees C and ±10% supply voltage variation. It enforces TLState transitions through resistance thresholds corresponding to LRS, IRS, and HRS ranges. Fail-closed design: any out-of-window reading asserts Refuse (-1). RC spoof detection at 5 ns threshold prevents capacitive attacks on the voltage sensing path.

#### IV.4.2 Commit Gate

A memristive-gated pass transistor physically in-line on the actuation path. HRS blocks all actuation signals. LRS permits propagation. The Commit Gate's state is set exclusively by the TaOx cell resistance as measured by the Window Comparator. No software path reaches the Commit Gate. The 100-200 ns propagation overhead on the authorization path is the only latency added by physical enforcement.

#### IV.4.3 NL=NA Write Pulse

A voltage pulse on a dedicated hardware wire. Not a software flag. Not a register write. Not a firmware call. When the Governance Lane reaches a decision, the result is physically written to the TaOx cell through this pulse: the pulse amplitude and duration are calibrated to achieve the target resistance state (LRS, IRS, or HRS) reliably within the IRS variability constraint. Without the pulse, no TLState transition occurs regardless of any software state.

#### IV.4.4 Physical Unclonable Function

Post-manufacturing entropy from SRAM power-up states or Ring Oscillator frequency differences on the TSMC N2 die. 128-bit fuzzy-extractor output. Not factory-programmed. No key material exists on a powered-off device; the PUF derives identity from physical silicon characteristics reconstructed on power-up. Invasive probing disrupts the physical characteristics and renders the PUF invalid, ensuring that physical attack destroys the identity being extracted. PUF inter-die Hamming distance approximately 49-51% (experimentally demonstrated). PUF binding: SHA3-256(K_PUF ∥ device_serial_OTP ∥ log_session_nonce).

### IV.5 Dual-Lane Latency Architecture (DLLA)

The DLLA governs latency bounds for the two-lane enforcement architecture:

| Lane | Latency Bound | Role |
|------|--------------|------|
| Inference Lane | ≤2 ms WCET at 99.99th percentile | Proposes actions; never authorizes |
| Governance Lane | ≤300 ms ceiling, 50 ms jitter max | Evaluates constitutionally; authorizes or blocks |
| Commit Gate overhead | 100-200 ns | Authorization path only |

WCET stability requirement: sigma/mu < 10% across temperature 0-125 degrees C, voltage ±10%, and all process corners. The non-blocking constraint is absolute: the Governance Lane runs parallel to the Inference Lane and never serially stalls it. The Inference Lane continues computing during Governance Lane evaluation. The Commit Gate is the resolution point.

### IV.6 Architecture B: SHIPPING Baseline

DITL/MT has been demonstrated at transistor simulation level (IBM PDK 1.2V 130nm CMOS). No fabricated DITL chip exists. The gap between simulation and production silicon is acknowledged here explicitly as a real constraint.

Architecture B is the SHIPPING baseline for deployments without DITL/MT silicon:

- Software enforcement is active for Layers 1-4 of the five-layer NL=NA stack
- NULL_PUF_DEPLOYMENT sentinel in the NLNAAuditToken records deployment mode in every audit log
- TLCapabilityFlags.pufAttestationMode: "ARCHITECTURE_B"
- Layer 5 on-chain enforcement is active and unchanged

Architecture B does not reduce constitutional authority. It records honestly that physical silicon enforcement is pending fabrication. The transition from Architecture B to full silicon enforcement requires no changes to Layers 1-5; only the hardware attestation mode and NULL_PUF_DEPLOYMENT sentinel change.

### IV.7 Adversarial Considerations for DITL/MT

Three black-swan adversarial scenarios specific to the DITL/MT layer are documented:

**Correlated DITL Hardware Failure Cascade.** Manufacturing defects or environmental stressors causing correlated failure across multiple DITL gates on the same die. Fail-closed design defaults all affected gates to HRS (Refuse -1). The system halts. This is the correct behavior, and it is structurally guaranteed.

**Foundry Compromise.** Nation-state actors with access to fabrication masks at the foundry could introduce silicon-level backdoors undetectable through post-fabrication inspection. PUF attestation and boot ROM measurement chains provide detection capability but cannot prevent a mask-level insertion. This risk is acknowledged as a residual structural constraint on the entire field of custom silicon, not specific to DITL/MT.

**Side-Channel Extraction.** DITL delay-insensitivity resists timing attacks by design. Power and electromagnetic side channels are not addressed by DITL architecture alone and require standard countermeasures (dual-rail pre-charge logic, power analysis masking) in high-threat deployments.

---

## V. Hardware Root of Trust

### V.1 Trust Chain Architecture

The trust chain extends from immutable boot ROM through measured firmware stages to the execution gate hardware. The Boot ROM Root of Trust for Measurement, implemented in mask ROM or OTP memory, contains the first measurement code, which hashes the next firmware stage and extends the measurement into PCR 0 of a TPM 2.0 module conforming to ISO/IEC 11889. The extend operation PCR_new = Hash(PCR_old ∥ measurement) is irreversible.

Each subsequent boot stage, including UEFI firmware, bootloader, kernel, and logging subsystem initialization, is measured and extended into designated PCRs before execution. The TPM signs the current PCR values along with a verifier-supplied nonce using an Attestation Key certified through the TPM's Endorsement Key, burned at manufacture and uniquely identifying the physical TPM device.

In DITL/MT deployments, the logging subsystem's initialization is the first log entry in the accumulator, and the NL=NA write pulse that records it is the first pulse on the dedicated hardware wire. This creates a chain from boot ROM measurement through TPM attestation through PUF identity through the first NL=NA pulse to every subsequent log entry.

### V.2 Secure Enclaves

Intel SGX enclaves execute logging subsystem hash computation, Merkle accumulator update, and attestation quote generation in hardware-protected memory inaccessible to the operating system and hypervisor. The enclave measurement hash (MRENCLAVE) is included in remote attestation reports, allowing external verifiers to confirm that the exact expected logging code is executing on genuine hardware.

ARM TrustZone partitions the SoC into Secure World and Normal World. The TrustZone Address Space Controller enforces memory access control based on the Non-Secure bit on every bus transaction: the logging subsystem and execution gate operate in Secure World, where Normal World software at any privilege level cannot access secure memory or registers.

The RISC-V Keystone TEE provides an open-source verified execution environment for deployments where vendor-controlled enclaves are unacceptable from a trust perspective.

### V.3 Hardware Security Module

HSMs conforming to FIPS 140-3 Level 3, with the Thales Luna 7 as named baseline, provide tamper-resistant key storage and cryptographic operations. Level 3 modules incorporate conductive mesh layers, light sensors, voltage monitors, and temperature sensors that trigger immediate zeroization of all plaintext Critical Security Parameters upon detection of physical intrusion. Keys generated within the HSM boundary never leave in plaintext.

### V.4 Physical Unclonable Function Chain

The PUF provides device-unique identity that cannot be cloned, extracted, or transferred. PUF-derived keys bind the device's signing key through a certificate chain, ensuring that attestation quotes and log signatures are attributable to a specific physical device. Physical attack on the device destroys the identity being extracted because invasive probing disrupts the physical characteristics from which the PUF derives its response.

### V.5 Software-Only Enforcement Insufficiency

Software-only enforcement fails against four documented attack classes:

**Kernel compromise:** full physical memory access allows modification of logging code, suppression of log writes, or forgery of entries without detection by any software-layer monitor.

**Hypervisor escape:** documented vulnerabilities enable guest VM escape to host memory, where any software-based logging mechanism can be disabled.

**SMM subversion:** SMM callout vulnerabilities allow OS-level attackers to execute arbitrary code at SMM privilege and modify SPI flash, concealing all activities from OS detection.

**Supply chain substitution:** compromised firmware subverts the entire software stack before the operating system loads.

Hardware enforcement, where the electrical path to the actuator physically traverses a verification gate independent of the CPU's software execution environment, eliminates all four classes.

---

## VI. Ternary Logic Mapping and Epistemic Hold / Solvency Protocol

### VI.1 Triadic Decision Space

The Ternary Logic framework defines a triadic decision space T = {+1, 0, -1} that governs every decision cycle.

**Proceed (+1):** clear affirmative; confidence thresholds satisfied, inputs consistent and complete, preconditions verified. In the MT hardware substrate, Proceed corresponds to LRS. The NL=NA write pulse sets LRS. The Window Comparator confirms. The Commit Gate conducts. The actuation signal propagates. The transition to Proceed is itself a logged event, committed before the Commit Gate opens.

**Refuse (-1):** definitive negative; the proposed action violates a hard constraint, exceeds a risk boundary, or fails a validity check. In the MT hardware substrate, Refuse corresponds to HRS. The Commit Gate in HRS blocks all actuation signals. Refuse transitions require the same logging completeness as Proceed. The explicit representation of refusal as a distinct hardware state closes accountability gaps where absence of action is indistinguishable from failure to consider action.

**Epistemic Hold (0):** the system has determined that it cannot determine; confidence is insufficient, inputs are conflicting, data is incomplete, or the input distribution falls outside the domain for which the decision model was trained or validated. In the MT hardware substrate, Epistemic Hold corresponds to IRS. The Commit Gate in IRS neither fully conducts nor fully blocks, holding the system in a physically indeterminate state that mirrors the semantic indeterminacy of the decision.

Epistemic Hold is not a failure mode. It is a deliberate, architecturally supported outcome. It persists across power cycles without software reinitialization; hardware-semantic persistence of Epistemic Hold in silicon, not in volatile memory, is one of MT's two discontinuous advantages over conventional NVRAM.

This specification requires that every decision cycle produce a log entry recording which of these three states was reached, along with the complete decision vector, the confidence metrics, the raw input data, and the specific trigger condition. The log entry must be committed before the decision result is released to any downstream consumer. The NL=NA invariant applies to all three states equally.

### VI.2 Solvency Protocol in Financial Contexts

In financial and economic contexts, Epistemic Hold implements the Solvency Protocol. When an algorithmic trading system, credit assessment engine, or settlement processor encounters ambiguous market conditions, conflicting signals, or data quality degradation, the system enters the Solvency Protocol state: all pending transactions are halted, current positions are preserved without modification, and a complete market state snapshot with the pending transaction queue and triggering conditions is committed to the log.

The Solvency Protocol recognizes that financial actions create irreversible obligations that may propagate instability through interconnected networks. Epistemic Hold enforcement prevents commitment under uncertainty, maintaining capital and contractual capacity that would be consumed by premature action. The protocol persists until the triggering conditions are resolved through arrival of additional data, human review with explicit authorized continuation, or expiration of a safety timeout that triggers orderly position unwinding.

### VI.3 Epistemic Hold Trigger Conditions

Epistemic Hold is mandatory under four conditions:

**Confidence below calibrated threshold.** Confidence in decision outcomes falls below configured per-domain thresholds, whether due to model uncertainty, input quality degradation, or out-of-distribution conditions that invalidate model assumptions. The confidence calculation includes aleatory uncertainty from inherent randomness, epistemic uncertainty from model and data limitations, and aggregation uncertainty from combining multiple sources.

**Conflicting input detection.** Multiple information sources provide mutually inconsistent data that cannot be reconciled within the decision cycle's time budget. The conflict magnitude is quantified and compared against thresholds that distinguish resolvable disagreement from fundamental contradiction. Full content of each conflicting source, provenance and transmission path documentation, conflict metrics, and resolution algorithm applied are preserved in the suspension log.

**Incomplete data states.** Required input fields are missing, corrupted, or stale beyond a defined freshness bound. The system maintains explicit schemas of data requirements for each decision type. Epistemic Hold is triggered by any schema violation. The incompleteness characterization identifies specifically which required elements are missing, expected availability based on source characteristics, and the impact of incompleteness on decision quality.

**Out-of-distribution inputs.** The input vector falls outside the convex hull or statistical boundary of the training or validation distribution, as detected by distance metrics, anomaly scores, or distribution shift detectors. Mahalanobis distance, local outlier factor scores, or isolation forest path lengths are applied depending on feature space dimensionality. The distribution envelope is validated continuously through goodness-of-fit testing, with the envelope updating to accommodate legitimate concept drift while flagging abrupt distributional shifts indicative of sensor malfunction, adversarial poisoning, or environmental regime changes. The complete log entry includes the anomalous feature vector, nearest neighbor references in the training distribution, projection onto principal components, and reconstruction error from autoencoder models.

### VI.4 Forced Continuation Prevention

Three mechanisms prevent forced continuation from Epistemic Hold.

**Cryptographic time-lock.** The Wesolowski VDF construction requires sequential squaring in a group of unknown order, providing cryptographic proof that a minimum wall-clock time has elapsed between hold entry and any subsequent state transition. The proof cannot be accelerated by parallel computation.

**External pressure detection.** Timing analysis monitors the statistical distribution of decision latencies. Command arrival rates exceeding human interaction capabilities, or synchronization anomalies suggesting coordinated external manipulation, trigger automatic audit events and flag potential coercion.

**Complete audit trail of override attempts.** Every request to exit Epistemic Hold, whether automated or human-initiated, is logged with the identity of the requestor, the justification provided, the timestamp, and the current system state. This log entry must be committed before the override can be evaluated.

---

## VII. Cryptographic Non-Repudiation of Action

Every action committed under the No Log = No Action invariant satisfies verifiable prior log requirements that establish an unbroken chain of cryptographic proof from system initialization through the current state.

The chain begins at the boot measurement sequence, where TPM PCR values record the identity of every firmware and software component loaded, and extends through every logged decision and action to the present moment. For any action a executed at time t, a Merkle inclusion proof of O(log n) hash values demonstrates that the log entry for a is a leaf in the accumulator whose root was the active capability token at time t. A Merkle consistency proof of O(log n) hash values demonstrates that the accumulator state at any earlier time t' is a prefix of the accumulator state at t, confirming that no entries were deleted, modified, or reordered.

### VII.1 Digital Signature Binding

Each log entry is signed by the actor's private key held within a TPM, HSM, or secure enclave, never exposed in plaintext outside the hardware trust boundary. In DITL/MT deployments, the signature covers the canonical serialization of the log entry, the TL state reached, the decision vector, the timestamp, the monotonic counter value, the hash of the preceding log entry, and the PUF binding hash. The signed log entry constitutes a cryptographic commitment that the identified actor authorized the specific action at the specific time in the specific system state, binding the commitment to the specific physical silicon instance.

### VII.2 Identity-Integrity-Logging Triad

The three inseparable components of every auditable action are:

**Identity:** who authorized the action, through digital signature verified against a certificate chain rooted in the device's PUF-derived identity and the actor's credential.

**Integrity:** that the log entry has not been modified since commitment, through Merkle inclusion proof and hash chain verification.

**Logging:** that the action was recorded before it occurred, through the temporal ordering enforced by the cryptographic actuator interlock and, in DITL/MT deployments, by the physical Commit Gate.

No component of this triad can be satisfied without the other two.

### VII.3 Invalid Execution States

**Orphaned action:** an externally observable effect for which no committed log entry exists in the accumulator. Detection triggers immediate safe harbor transition, key rotation for all potentially compromised signing keys, and quarantine of the log segment spanning the time window in which the orphan was detected.

**Hash mismatch:** a log entry's stored hash does not match the hash recomputed from the entry's canonical serialization. Triggers safe harbor transition, isolation of the affected log segment, and forensic investigation to determine whether the mismatch resulted from storage corruption or adversarial tampering.

**Signature verification failure:** a log entry's digital signature cannot be verified against the expected public key. Triggers safe harbor transition, revocation of the associated signing key, and notification to all relying parties that log entries signed by that key after the last verified entry require independent corroboration.

---

## VIII. Cryptographic Primitives and Adversarial Resistance

Canonicalization follows RFC 8785 (JSON Canonicalization Scheme) for text-format logs or deterministic CBOR (dCBOR) for binary-format logs. Without canonicalization, an adversary could construct log entries that are semantically identical to legitimate entries but produce different hashes, enabling substitution attacks undetectable through hash chain verification.

Append-only structures conform to RFC 9162 (Certificate Transparency v2). Merkle inclusion proofs (O(log n)) demonstrate that a specific entry exists as a leaf in the tree. Merkle consistency proofs (O(log n)) demonstrate that the tree at an earlier size is a strict prefix of the current tree, confirming that no entries were deleted, modified, or inserted before existing entries.

Replay protection uses two complementary mechanisms. Nonce inclusion: every log entry contains a cryptographically random nonce from a hardware true random number generator within the trust boundary, ensuring that replaying an earlier entry produces a duplicate nonce detected by the accumulator's uniqueness constraint. Monotonic counters: implemented in TPM non-volatile memory, each log entry includes the current counter value, the counter is incremented atomically with each commitment, and counters can never be decremented or reset. In DITL/MT deployments, the counter increment is hardware-atomic with the NL=NA write pulse.

Logging suppression countermeasures implement redundant channels with Byzantine fault tolerance following the PBFT protocol of Castro and Liskov, requiring a minimum of 3f + 1 logging nodes to tolerate f Byzantine faults. The Logres protocol of Wanner, Chuat, and Perrig provides formally verified (in Isabelle/HOL) guarantees of agreement (all valid logs produced during a protocol run are equal), completeness (every entry submitted by a client to a correct node is included), and liveness (the protocol always produces a new valid log).

Insider threat mitigation requires M-of-N authorization, with M ≥ 2 and authorities drawn from organizationally independent roles, for all operations that could affect log integrity. The logging subsystem, key management subsystem, audit verification subsystem, and override authorization subsystem operate in distinct trust domains with hardware-enforced isolation.

Silent action prevention leverages observable energy consumption correlation with logged activity. Power consumption during periods logged as idle that exceeds the baseline profile indicates unlogged computation; characteristic operation signatures can be matched against a reference library. This physical-layer tamper detection is independent of all software-layer mechanisms.

Post-commit immutability is enforced through WORM (Write Once Read Many) storage at hardware level, combined with software-layer enforcement through systems such as SealFS (a Linux kernel module implementing transparent tamper-evident logging with HMAC ratchet chains), ensuring that even root-level access to the logging host cannot modify committed log data without cryptographic detection.

---

## IX. Failure Modes and Cyber-Physical and Financial Safe Harbor States

This specification requires fail-closed behavior across all critical failure modes: storage failure, hashing inconsistency, buffer exhaustion, HSM communication loss, key rotation failure, and certificate expiration all trigger immediate cessation of action execution rather than degraded or unlogged operation.

In DITL/MT deployments, fail-closed is physically guaranteed: the Commit Gate defaults to HRS (Refuse -1) in any undefined or error state. The Window Comparator's fail-closed design means that any out-of-window resistance reading asserts HRS. There is no fail-open mode in the silicon.

For cyber-physical systems, the safe harbor state comprises three interlocking requirements. Kinetic energy minimization with bounded convergence time: a Control Lyapunov Function V(x) exists such that V_dot(x) ≤ -αV(x) for some α > 0 along all trajectories within the safe harbor controller's domain, yielding exponential convergence. Controlled deceleration with bounded jerk and acceleration: the deceleration trajectory follows a seven-segment S-curve profile with jerk bounded by j_max, preventing impulsive loads and vibration. Stable equilibrium: the final state is a stable equilibrium point verified through Lyapunov stability criteria such that small perturbations do not cause departure.

For financial systems, the safe harbor state comprises immediate transaction halting and liquidity preservation. All pending transactions are frozen; no new transactions are initiated; no settlements are completed; no position modifications are permitted; all outbound transfers are halted; current reserve levels are maintained.

The specification enforces clear separation between high-level decision authority denial and low-level control stability preservation. When the logging subsystem fails and execution is halted, stabilizing controllers continue to operate within pre-defined safe harbor parameters logged at system initialization. These controllers do not require high-level decision authority.

State machines governing failure mode transitions are model-checked to verify the safety property AG(state ∈ {Normal, Degraded, Safe_Harbor_Transition, Safe_Harbor_Steady, Recovery}) and the liveness property AG(Logging_Failure → AF(Safe_Harbor_Steady)).

Manual override procedures require: physical presence verified through local authentication that cannot be satisfied remotely; multi-party authorization with M ≥ 2 from organizationally independent roles; and complete logging of all override actions through a secondary battery-backed recording channel if the primary logging subsystem is inoperative. All override records must be integrated into the primary log upon restoration.

---

## X. Integration with Dual-Lane Architecture

### X.1 Architecture Overview

The dual-lane architecture separates log commitment into two concurrent but independent lanes, each with distinct latency characteristics, durability guarantees, and failure domains. This architecture resolves the tension between real-time latency requirements and global auditability requirements without compromising the NL=NA invariant.

### X.2 Inference Lane: Proposal Without Authorization

The Inference Lane is the binary computation layer. It proposes actions. It never authorizes them. Its latency bound is a strict ≤2 ms WCET at the 99.99th percentile, implemented through dedicated FPGA or ASIC hardware pipelines executing the complete log commitment sequence, comprising canonical serialization, SHA-3-256 hashing, Merkle accumulator update, monotonic counter increment, ReRAM write, and read-back verification, entirely within programmable logic without dependency on a general-purpose CPU or operating system scheduler.

The formal property is AG(exec(a) → inference_committed(a)): on all paths, execution of action a implies that a has been committed in the Inference Lane accumulator.

### X.3 Governance Lane: Constitutional Authorization

The Governance Lane is the ternary constitutional evaluation layer. It authorizes or blocks every action proposed by the Inference Lane. Its ceiling is ≤300 ms with 50 ms jitter maximum. It evaluates confidence metrics, pillar certifications, regulatory compliance, and all constitutional constraints. Its output is the PermissionToken with laneOrigin const "GOVERNANCE_LANE", the only token that can authorize execution through Layer 2 of the five-layer NL=NA stack.

The Governance Lane runs parallel to the Inference Lane without stalling it. The Commit Gate is the resolution point: Proceed (+1) from the Governance Lane opens the Commit Gate; Refuse (-1) or Epistemic Hold (0) keeps it closed regardless of the Inference Lane's computational result.

Governance Lane failures, including network partition, ledger congestion, and timestamp service unavailability, do not block Inference Lane operation. The two lanes operate in separate failure domains with no shared dependencies.

### X.4 Anchoring and Gap Tolerance

The Governance Lane provides asynchronous anchoring to distributed ledgers, timestamp authorities conforming to RFC 3161, and transparency logs conforming to RFC 9162. Delayed anchoring does not violate the NL=NA invariant: the invariant requires commitment to local hardware-backed non-volatile storage before action release, satisfied entirely by the Inference Lane and Governance Lane local commitment.

The gap tolerance between local commitment and external anchoring is bounded by application-domain safety constants, monitored in real time, and enforced through the formal property:

```
AG(inference_committed(a) → A[¬gap_exceeded U governance_anchored(a)])
```

stating that from any state where a is committed in the Inference Lane, the gap tolerance is never exceeded before a is anchored in the Governance Lane, on all paths where anchoring eventually succeeds.

The formal property combining both lanes is:

```
□(exec(a) → inference_committed(a)) ∧ ◇(inference_committed(a) → governance_anchored(a))
```

stating that execution always requires prior Inference Lane commitment, and every Inference Lane commitment is eventually anchored in the Governance Lane.

---

## Conclusion

The No Log = No Action invariant, as specified across these ten sections, constitutes a binding architectural constraint that transforms logging from an optional telemetry service into a structurally enforced prerequisite for every externally observable effect in a Ternary Logic system. The invariant's enforcement rests on four interlocking pillars.

The first is formal temporal logic: LTL and CTL properties defining the required ordering between log commitment and action release, dischargeable through model checking against the system's complete state space.

The second is the five-layer NL=NA enforcement stack: independent schema-level and on-chain layers that independently prevent any Proceed authorization without cryptographic log commitment, such that bypassing one layer does not bypass the others.

The third is cryptographic coupling: Merkle accumulators, digital signatures, PUF binding, and hardware attestation quotes making log entries unforgeable, log sequences tamper-evident, and actor identity non-repudiable, with every log session bound to the specific physical silicon instance that produced it.

The fourth is the DITL/MT hardware substrate: Muller C-elements that cannot generate output without complete verified input; a Window Comparator that enforces TLState transitions through physical resistance measurement; a Commit Gate standing in-line on the actuation path in silicon; and an NL=NA write pulse that is a voltage pulse on a dedicated wire, not a software flag, not a register write, not a privilege-level operation. This substrate enforces the invariant at a layer that no software, firmware, hypervisor, or operating system can reach.

The integration of Ternary Logic's triadic decision space into this enforcement framework ensures that the critical third state, Epistemic Hold, receives the same structural protection as Proceed and Refuse. The system's admission that it does not know is logged, hardware-committed, and auditable with exactly the same rigor as its decisions to act or refuse. The dual-lane architecture provides sub-2 ms Inference Lane commitment for real-time operation and asynchronous Governance Lane anchoring for global verification. Architecture B records honestly the current deployment status of the hardware layer while maintaining full constitutional authority through Layers 1-5.

The resulting system does not trust its operators, its software, or its firmware to maintain log integrity. It structurally prevents any of them from violating it.

---

*No Log = No Action. The right to act is derived from the act of remembering.*
