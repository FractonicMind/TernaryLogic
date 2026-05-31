# TL Core Doctrine: No Log = No Action — Execution Integrity Specification

> 🌐 **Interactive Web Version:** [No_Log-No_Action_Execution_Integrity_Specification.html](https://fractonicmind.github.io/TernaryLogic/No_Log-No_Action/No_Log-No_Action_Execution_Integrity_Specification.html)

> 🎧 **Audio Overview (6 min):** [No_Log-No_Action_Execution_Integrity_Specification.mp3](https://fractonicmind.github.io/TernaryLogic/No_Log-No_Action/No_Log-No_Action_Execution_Integrity_Specification.mp3)

---

## I. Problem Definition: Optional Logging Failure

### I.1 Asynchronous Telemetry and Non-Determinism

#### I.1.1 Execution-Persistence Decoupling in Traditional Systems

Traditional computing systems fundamentally rely upon asynchronous telemetry mechanisms for observability, creating an inherent architectural decoupling between the execution of operations and the persistence of their corresponding audit records. This decoupling manifests as a temporal gap between the moment an action completes and the moment its corresponding log entry becomes durable, during which any number of failure modes may intervene to prevent successful persistence. The core architectural pattern involves application code executing business logic, emitting log events through asynchronous channels such as message queues, network sockets, or buffered file descriptors, and then proceeding without confirmation that those events have reached durable storage. This pattern, while offering performance advantages through reduced latency and increased throughput, fundamentally undermines the evidentiary value of the logging system by permitting execution to advance while the audit state remains provisional or incomplete.

The execution-persistence decoupling creates what this specification terms "evidentiary debt": a cumulative gap between the actual state of the system and the explainable state derived from audit records, which grows without bound in the presence of logging failures and can never be fully repaid. The non-determinism introduced by this architecture is not merely a performance artifact but a fundamental source of systemic risk, as it enables scenarios where actions have irreversible consequences while their documentation remains subject to loss through buffer overflow, network partition, process crash, or power failure. The telemetry approach provides observability without enforcement: systems may generate voluminous log data without any guarantee that this data comprehensively represents system behavior, creating conditions under which post-hoc reconstruction of system behavior becomes an exercise in approximation rather than determination.

#### I.1.2 Log Loss, Reordering, and Silent Failures

The asynchronous logging pipeline creates multiple vectors for log loss, reordering, and silent failures that remain invisible to conventional monitoring. Buffering strategies designed to optimize I/O performance may discard entries under load, with replacement policies that prioritize recency or frequency over criticality, and without any notification to the generating application that its actions are proceeding unrecorded. Network transmission protocols may acknowledge receipt at intermediate hops without guaranteeing end-to-end delivery, creating false confidence in persistence while the actual log entry remains in a network queue subject to timeout and discard. Storage systems may report write completion from volatile caches prior to physical media commitment, exposing recorded state to power loss or system crash with no recovery mechanism.

The silent nature of these failures is particularly pernicious: the absence of a log entry cannot be distinguished from the absence of an action without independent verification mechanisms that the architecture itself fails to provide. When logs are dropped due to buffer exhaustion, the resulting gaps are typically undetectable from the remaining records, as there is no marker indicating that something should have been present. This creates a false sense of completeness that is more dangerous than acknowledged absence, as investigators may proceed with confidence in their analysis while remaining unaware of the missing evidence. The problem compounds with log rotation and archival, where the temporal distribution of retained records may not match the distribution of actual events, creating systematic biases in any analysis based on the surviving data.

#### I.1.3 Observability Without Enforcement

The fundamental limitation of traditional logging architectures is their provision of observability without enforcement. Observability permits inference about system state from available data when the logging infrastructure functions correctly, but it provides no mechanism to prevent or detect violations of the expected logging behavior. Enforcement, by contrast, guarantees that system state transitions are bound to observable, verifiable records through architectural constraints that cannot be circumvented by configuration, load conditions, or software defects. The distinction is critical for systems requiring forensic reconstruction, regulatory compliance, or adversarial resilience, as the absence of guaranteed persistence creates exploitable gaps in the evidentiary chain.

The enforcement gap in traditional systems appears at multiple levels: there is no guarantee that logging code is executed for all actions, no guarantee that executed logging code successfully persists its output, and no guarantee that persisted output accurately represents the action that was executed. Each of these guarantees must be provided through architectural mechanisms rather than procedural adherence, as procedural mechanisms are themselves subject to the same failure modes they attempt to prevent. The transformation from observability to enforcement requires synchronous, hardware-verified persistence that fundamentally alters system latency and throughput characteristics, accepting these costs as necessary for deterministic state integrity.

### I.2 Post-Hoc Reconstruction Limitations

#### I.2.1 Partial Data Loss and Evidence Gaps

The limitations of post-hoc reconstruction become apparent when systems attempt to establish behavioral provenance from incomplete or inconsistent log data, a condition that arises predictably under partial data loss. When log entries are missing due to buffer overflow, network congestion, or storage exhaustion, reconstruction algorithms must operate upon an incomplete evidentiary substrate, producing outputs that may be technically consistent with available data yet factually incorrect regarding actual system behavior. The evidence gaps created by missing entries are fundamentally unbridgeable: no algorithmic technique can recover information that was never recorded, and the reconstruction process cannot distinguish between "no event occurred" and "event occurred but was not recorded."

The degradation of evidentiary value is non-linear with data loss percentage, as missing entries disproportionately impact the ability to establish causal chains and temporal dependencies. A system experiencing even modest log loss rates may produce reconstructions that are technically incomplete but functionally unusable for accountability purposes, as critical decision points, authorization events, or state transitions fall within gaps that cannot be bridged through inference. The reconstruction algorithms, whether based on state machine inference, constraint satisfaction, or probabilistic estimation, all share the characteristic that their output certainty is bounded by their input completeness, with no mechanism for quantifying confidence in the absence of knowledge about what is missing.

#### I.2.2 Adversarial Conditions and Timing Inconsistencies

Adversarial conditions amplify reconstruction limitations dramatically. An attacker with knowledge of the logging architecture can deliberately trigger conditions that cause log loss or corruption while executing malicious actions, creating a forensic environment where the available evidence points away from rather than toward the true sequence of events. The attack surface encompasses not merely the log storage subsystem but the entire pipeline from event generation through buffering, transmission, aggregation, and archival, with each stage operating under different trust assumptions and vulnerability profiles. Selective suppression, where an attacker removes incriminating entries while preserving benign ones, or injection attacks, where fabricated entries create false narratives, render reconstruction systematically misleading rather than merely uncertain.

Timing inconsistencies in distributed systems create additional reconstruction challenges that resist algorithmic resolution. Clock synchronization protocols, even when operating within nominal parameters, provide only bounded uncertainty in timestamp comparison, with the bound potentially exceeding the inter-event latency for high-frequency operations. Network latency variation and processing delay jitter create fundamental ambiguity in the mapping from physical event occurrence to logical record ordering. The happens-before relationship, central to causal reasoning about distributed computations, cannot be reliably established from timestamps alone, and logical clock schemes impose substantial overhead that limits their deployment in performance-critical contexts. The result is that distributed traces, even when complete, may admit multiple consistent interpretations of event causality, with no principled basis for selection among them.

#### I.2.3 Forensic Uncertainty in Distributed Traces

The forensic uncertainty arising from partial data loss, adversarial manipulation, and timing uncertainty creates a reconstruction problem that is computationally intractable in the general case. Investigators of system failures, security breaches, or regulatory violations frequently encounter scenarios where the evidentiary record is insufficient to determine what actually occurred, who was responsible, or whether proper procedures were followed. The traditional response of increasing log verbosity, improving network reliability, or adding redundant logging channels addresses symptoms rather than causes, as the fundamental architectural decoupling between execution and persistence remains intact.

The evidentiary value of reconstructed traces is further compromised by their lack of cryptographic binding to the original system state. Reconstruction processes operate upon log copies rather than authenticated originals, with no technical mechanism preventing modification of source data prior to reconstruction or of reconstruction outputs subsequent to generation. Legal and regulatory frameworks that admit reconstructed evidence typically impose procedural controls and expert testimony requirements that acknowledge these limitations, but such frameworks represent risk management rather than technical assurance, accepting reduced evidentiary quality as a practical necessity rather than solving the underlying architectural defects.

### I.3 Bypass Vectors in Emergency and Hardware Paths

#### I.3.1 Emergency Shutdown Sequences Circumventing Logging Stacks

Emergency shutdown sequences in traditional systems frequently implement direct hardware manipulation paths that circumvent normal software logging stacks, creating privileged execution channels that are inherently unlogged and therefore unaccountable. These sequences, designed for rapid response to critical conditions, prioritize speed over comprehensiveness, with hard-coded paths that write directly to hardware registers or trigger physical mechanisms without software mediation. While this design choice optimizes for availability and safety in the immediate sense, it creates a systematic exemption from logging requirements precisely at the moments when such requirements are most critical for subsequent accident investigation and liability determination.

The emergency shutdown path typically proceeds from hardware fault detection through direct processor interrupt to execution of ROM-resident firmware, circumventing the operating system, file systems, and logging daemons that would normally record system events. The state changes produced by emergency shutdown, including data loss, transaction aborts, and physical system reconfiguration, may therefore lack documentary evidence, creating forensic gaps precisely where accountability is most needed. The classification of conditions as "emergency" itself becomes a security-critical decision point, with insufficiently protected emergency triggers serving as covert action channels that adversaries may deliberately exploit to execute actions within the resulting logging gap.

#### I.3.2 Direct Memory Access Without Software Mediation

Direct memory access (DMA) mechanisms provide a fundamental bypass vector by enabling hardware subsystems to read from and write to system memory without processor involvement or software visibility. DMA-enabled devices, including network interfaces, storage controllers, graphics processors, and specialized accelerators, can modify system state, transfer data to external networks, and trigger physical actuations while the main processor and its logging infrastructure remain unaware of these operations. The DMA path represents a complete circumvention of software-based logging, as the device driver model that would normally intercept and record I/O operations is bypassed at the hardware level.

The security implications of DMA are substantial and well-documented: DMA attacks enable memory extraction, code injection, and privilege escalation through peripheral compromise, with the attack execution occurring entirely through hardware pathways that generate no audit records within the compromised system's logging infrastructure. Defense mechanisms including IOMMU-based DMA protection provide partial mitigation but introduce complexity and performance overhead, with implementation gaps and configuration errors common in production deployments. The fundamental architectural challenge is that hardware-level access pathways are designed for performance and functionality rather than evidentiary completeness, with logging as an afterthought rather than core requirement.

Documented IOMMU insufficiency vectors include: early boot gaps where IOMMU translation tables are not yet enabled; deferred DMA attacks exploiting stale mappings after virtual machine destruction; and message-signaled interrupt (MSI) forgery that bypasses IOMMU enforcement entirely. None of these vectors are addressable through software policy alone. They require hardware-layer enforcement at the physical actuation boundary — exactly what the DITL/MT substrate described in Section IV provides.

#### I.3.3 Memory-Mapped I/O Reaching Physical Interfaces

Memory-mapped I/O (MMIO) extends the DMA bypass capability by presenting hardware device registers as addressable memory locations, allowing direct manipulation of physical interfaces through simple load and store operations that may not trigger any software interception points. A malicious or compromised process with appropriate page table mappings can manipulate physical actuators, network ports, and storage devices directly, with no evidence of such manipulation appearing in system call logs, network traces, or application audit records. The architectural separation between memory and I/O, historically a performance optimization, becomes a security vulnerability when evidentiary requirements are considered, as it enables action without observation by design.

The combination of emergency shutdown bypasses, DMA transfers, and memory-mapped I/O operations creates a comprehensive set of vectors through which actions can be executed without traversing software logging stacks. These vectors are not implementation defects but architectural features of conventional computing, and their elimination requires fundamental restructuring of the execution-logging relationship that only hardware-enforced invariants can provide. The No Log = No Action specification addresses these bypass vectors through mandatory hardware logging interfaces at all physical effector boundaries, with mechanical or electrical interlocks that prevent actuation energization pending log commitment verification.

---

## II. The Invariant: No Log = No Action

### II.1 Formal Predicate Logic Definition

#### II.1.1 Universal Quantification Over All Actions

The No Log = No Action invariant is formally defined as a universal constraint over all possible system executions, establishing that the existence of a committed log entry is a necessary precondition for any action release. Let A denote the set of all actions within the system scope, where each action a ∈ A represents a potential state transition, transaction, API invocation, or physical actuation. Let L denote the set of all log entries, with l_a ∈ L representing the entry corresponding to action a. The predicate LogCommitted(l_a) evaluates to true precisely when l_a has satisfied all completeness criteria defined subsequently: canonical serialization, cryptographic hashing, physical persistence in a hardware-backed non-volatile accumulator, and successful read-back verification with integrity confirmation. The predicate ActionReleased(a) evaluates to true when a has been permitted to produce externally observable effects, persistent state mutations, or physical actuations at cyber-physical boundaries.

The universal quantification ensures that no action category, regardless of urgency, privilege level, operational context, or perceived criticality, is exempt from the invariant. This absoluteness is essential to the invariant's function as a hard architectural constraint; any qualified or conditional formulation would create exploitable edge cases that could be systematically leveraged to circumvent evidentiary requirements. The quantification extends to actions initiated through emergency procedures, hardware interrupts, diagnostic modes, and maintenance interfaces, eliminating the category of "unlogged operations" that plague traditional systems.

#### II.1.2 Log Commitment as Necessary Precondition

The material implication structure of the invariant, ActionReleased(a) → LogCommitted(l_a), establishes log commitment as a necessary precondition for action release in the logical sense: ActionReleased(a) cannot be true in any model where LogCommitted(l_a) is false, regardless of what other conditions may obtain. This is not merely a correlation or best practice but a strict dependency that is enforced through hardware mechanisms rather than software convention. The contrapositive, ¬LogCommitted(l_a) → ¬ActionReleased(a), makes explicit the enforcement interpretation: absence of log commitment guarantees prevention of action release.

The necessary precondition status has profound architectural implications. It means that no optimization, configuration change, or operational expedient can legitimately bypass the logging requirement; that all execution paths, including error handling, recovery, and shutdown sequences, must satisfy the invariant; and that any violation represents a catastrophic system failure rather than a tolerable degradation. The precondition is evaluated through hardware mechanisms that are not subject to software override, ensuring that the enforcement persists even under total software compromise.

In the DITL/MT hardware substrate described in Section IV, this precondition is not a software check but a physical voltage condition. The Commit Gate — a memristive-gated pass transistor — is pre-set to Low Resistance State (LRS) only when TL authorization is confirmed. In High Resistance State (HRS), the gate blocks execution physically. No software path, privilege escalation, or firmware override can change this: the gate state is set by the NL=NA write pulse, a dedicated voltage pulse on a hardware wire that is entirely outside the processor's instruction set architecture.

#### II.1.3 Action Release as Consequent Condition

The consequent condition ActionReleased(a) is defined comprehensively to encompass all mechanisms by which a system produces effects upon its environment. This includes externally observable effects such as API responses, network transmissions, display updates, and side-channel emissions; persistent state mutations including database writes, file system modifications, configuration changes, and firmware updates; and cyber-physical boundary actuations comprising motor commands, valve positions, heating element activation, and any other conversion of computational state to physical energy or material transformation. The scope explicitly includes implicit actions such as cache line evictions that reveal memory contents, speculative execution results that affect timing, and power state transitions that modify availability.

The comprehensive definition ensures that no execution pathway produces external effects while evading logging requirements. Actions that are purely internal, producing no observable effect and no persistent state change, are excluded from the consequent condition, allowing optimization of logging overhead for computational intensive but effect-free operations. However, any operation whose result may influence subsequent action decisions must be logged to ensure complete traceability of decision chains, with the logging requirement propagating through data dependencies to capture all relevant computation.

### II.2 Linear Temporal Logic Specification

#### II.2.1 Strict Until Operator Semantics

The temporal dynamics of the invariant are formally specified using Linear Temporal Logic (LTL) with strict Until operator semantics, capturing the requirement that log commitment must precede action release in all possible execution traces. The Until operator U is defined such that φ U ψ holds at position i in a trace if ψ holds at some position j > i and φ holds at all positions k with i ≤ k < j. The strictness of this definition, requiring j > i rather than j ≥ i, is essential: it ensures that log commitment must actually occur at a strictly later time than action request, preventing scenarios where action release and log commitment are claimed to occur simultaneously through logical sleight of hand.

The strict Until semantics enforce genuine temporal precedence rather than definitional coincidence. In hardware implementation, this translates to a physical sequencing requirement: the electrical or logical signal enabling action release cannot be generated until hardware verification of log commitment has completed, with no race condition or pipelining ambiguity that might permit release based on anticipated rather than confirmed commitment. The strictness also supports inductive reasoning about system behavior, as each state transition can be analyzed with clear precedence relationships that enable compositional verification.

#### II.2.2 Globally Enforced Temporal Ordering

The globally operator G in the LTL specification ensures that the temporal constraint applies at all positions in all execution traces, not merely at initialization or during specific operational modes. The formula G(φ) holds if φ holds at every position in every trace, capturing the architectural requirement that the invariant is not a one-time initialization property but a continuous enforcement mechanism that applies to every action throughout system operation. This global enforcement extends through system states including normal operation, error recovery, degraded mode, and shutdown, with no state transition that violates the invariant being permissible.

The temporal ordering enforced by the LTL specification is total and strict: for any action request, there exists a unique sequence of states where the action is blocked pending commitment, followed by commitment achievement, followed by release authorization. This ordering is observable and verifiable through hardware state machine analysis, with each transition generating evidence that can be audited post-hoc. The global enforcement ensures that no execution trace exists where the ordering is violated, a property that can be verified through model checking of finite-state system abstractions.

#### II.2.3 Formal Formula

The complete LTL specification of the invariant is:

```
G(ActionRequested(a) → (¬ActionReleased(a) U LogCommitted(l_a)))
```

This formula applies the globally operator to an implication whose consequent is a strict Until formula. The antecedent ActionRequested(a) identifies positions in the execution trace where action a has been initiated and awaits release authorization. The consequent (¬ActionReleased(a) U LogCommitted(l_a)) enforces that from such positions, ActionReleased(a) remains false continuously until LogCommitted(l_a) becomes true, with LogCommitted(l_a) required to actually occur. The negation of ActionReleased(a) before the Until ensures that the action cannot be released at the same instant that log commitment is achieved; there must be a strict temporal separation with log commitment preceding action release, even if that separation is measured in hardware clock cycles.

An equivalent formulation using the Before operator, available in some LTL variants and in Computation Tree Logic (CTL), emphasizes the precedence relationship more directly:

```
G(ActionRequested(a) → (LogCommitted(l_a) B ActionReleased(a)))
```

where φ B ψ ("φ before ψ") is defined as ¬(¬φ U ψ) ∧ Fφ, ensuring that φ occurs strictly before ψ and that φ eventually occurs. Both formulations are logically equivalent and satisfy the requirement for strict temporal operator semantics; the Until formulation is preferred in this specification for direct compatibility with standard LTL model checking tools such as NuSMV and SPIN. The CTL variant, A G(ActionRequested(a) → A (LogCommitted(l_a) B ActionReleased(a))), adds explicit universal path quantification that may assist in model checking implementations for non-deterministic systems.

### II.3 The Five-Layer NL=NA Enforcement Stack

The invariant is enforced through five independent layers. Bypassing one layer does not bypass the others. Every Proceed (+1) authorization must pass all five. Layer 5 is the terminal constitutional gate.

**Layer 1 (Schema):** State Envelope if/then constraint. The permissionToken field is REQUIRED whenever currentState equals +1 (Proceed). No schema-valid Proceed response can exist without a permission token.

**Layer 2 (Schema):** PermissionToken.laneOrigin carries the constant value "GOVERNANCE_LANE". Inference Lane tokens are schema-invalid by construction. No token originating from the Inference Lane can authorize execution.

**Layer 3 (Schema):** TGLF-StateP1.permissionToken is in the required array. A Proceed log entry that omits the permission token fails schema validation before it reaches any downstream consumer.

**Layer 4 (Schema):** AuditProof cross-reference. The logHash and merkleRoot fields in the AuditProof must match the logHash and merkleRoot in the PermissionToken. Mismatched values indicate either forgery or accumulator divergence and are rejected.

**Layer 5 (On-chain ABI):** TL_Ledger_Core.registerPermissionToken reverts with NLNAViolation if logHash is not provably contained in the anchored Merkle root. This is the terminal constitutional gate — enforcement in silicon and on-chain, not in software policy.

In deployments where DITL/MT silicon is present, Layer 5 is reinforced at the physical level by the Commit Gate and Window Comparator described in Section IV. In Architecture B deployments (software enforcement where DITL/MT silicon is not yet deployed), Layers 1-4 carry the enforcement load and the NULL_PUF_DEPLOYMENT sentinel is set in the NLNAAuditToken to record the deployment mode honestly.

### II.4 Log Completeness Criteria

#### II.4.1 Canonical Serialization Requirements

Canonical serialization transforms the semantic content of a log entry into a deterministic byte sequence with unambiguous interpretation, eliminating representation variability that could enable equivocation attacks or verification failures. The serialization protocol specifies explicit byte-level field ordering, with all semantic content arranged in a defined sequence that preserves structural relationships while enabling byte-level comparison and hashing. Fixed-width encoding for numeric types eliminates implementation-dependent variations in integer and floating-point representation; length-prefixed encoding for variable-length data replaces delimiter-based termination that could be exploited for injection attacks; and normalized string representations with explicit character encoding and Unicode normalization form ensure consistent text processing across platforms.

The canonicalization protocol is versioned, with version identifiers included in every serialized structure to enable format evolution while maintaining backward verifiability of historical entries. Version negotiation occurs at system initialization, with agreement on the maximum mutually supported version and fallback to earlier versions where necessary for interoperability. The deterministic property of canonicalization ensures that identical actions produce identical byte sequences, enabling hash-based deduplication and integrity verification, while the explicit specification of every encoding decision eliminates the class of attacks that exploit implementation-dependent behavior.

#### II.4.2 Cryptographic Hashing and Integrity Verification

Cryptographic hashing applies a collision-resistant hash function to the canonical serialized log entry, producing a fixed-size digest that serves as the entry's cryptographic identifier and integrity anchor. The hash function must satisfy preimage resistance, preventing derivation of log content from its hash; second-preimage resistance, preventing construction of alternative valid logs with identical hashes; and collision resistance, preventing generation of any two distinct entries with identical hashes. SHA-3-256 or equivalent post-quantum candidates are required for new deployments, with SHA-256 permitted for legacy interoperability through documented transition procedures.

The PUF binding hash, computed as SHA3-256(K_PUF ∥ device_serial_OTP ∥ log_session_nonce), binds every log session to the specific physical silicon instance. This binding ensures that logs produced on one device cannot be replayed as if produced on another, and that physical substitution of the DITL/MT die is detectable through attestation failure.

#### II.4.3 Physical Persistence Through Read-Back Confirmation

Physical persistence verification requires read-back confirmation from the non-volatile accumulator before commitment is acknowledged, ensuring that the log entry has been durably recorded with properties that survive power loss and system restart. The storage medium must provide write atomicity at the granularity of the hash value, ensuring that partial writes produce detectably invalid results rather than plausible corruptions; read-after-write verification, with the stored value read back and compared to the original before acknowledgment of persistence; and resistance to remanence attacks, with explicit overwrite of previous values rather than simple marking as invalid.

On the TSMC N2 CoWoS baseline with embedded TaOx 1T1R ReRAM, Arrhenius-model retention is rated at 20 years at 85 degrees C. The IRS (Intermediate Resistance State, ~100 kΩ to 1 MΩ) retention confidence interval is narrower than LRS/HRS by approximately 2x, requiring differential sensing margins wider than conventional NVRAM practice. Only upon successful read-back confirmation does LogCommitted(l_a) evaluate to true, enabling the temporal constraint in the LTL specification to be satisfied and action release to proceed.

### II.5 Action Definition and Scope

#### II.5.1 Externally Observable Effects

Externally observable effects include any system behavior that reveals information about internal state to external observers, regardless of whether such detection is intended or routine. This category encompasses API responses that return computation results or status indicators; network transmissions that cross organizational or trust boundaries; display updates and audio generation that present information to human users; and side-channel emissions including timing variation, power consumption patterns, and electromagnetic radiation that could be monitored by sophisticated adversaries. The observability criterion is epistemic rather than operational: if an effect could be detected by a sufficiently instrumented observer, it qualifies as an action requiring prior logging.

The invariant requires logging of the decision to produce such effects, not merely the effects themselves, ensuring that the system's reasoning is captured regardless of whether the effect is successfully produced.

#### II.5.2 Persistent State Mutations

Persistent state mutations include any modification to storage that survives the transaction or operation that produced it, encompassing database updates, file system writes, registry modifications, and configuration changes that affect system behavior across restarts. The log entry for a state mutation must be committed before the mutation itself is acknowledged as complete, with the acknowledgment to the requesting component withheld pending commitment verification, creating observable latency that must be accounted for in system design.

#### II.5.3 Cyber-Physical Boundary Actuations

Cyber-physical boundary actuations represent the most safety-critical action category, as they directly modify the material world through physical interfaces and are frequently irreversible in ways that computational state changes are not. Actuation commands to motors, valves, switches, heating elements, and other effectors must be logged with: the computed command value, with full precision and units; the sensor readings and state estimates that informed the command computation; the safety envelope constraints that the command is required to satisfy; and the identity of the control algorithm or decision module that generated the command.

The physical actuation is gated by log commitment through hardware interlock mechanisms. In DITL/MT deployments, this gate is the Commit Gate: a memristive-gated pass transistor that is physically in-line on the actuation path. No signal can reach the effector driver until the Commit Gate transitions from HRS to LRS, and that transition is triggered only by the NL=NA write pulse — a dedicated voltage pulse on a hardware wire, not a software flag.

### II.6 Physical Existence Gating

#### II.6.1 Hardware-Backed Non-Volatile Accumulator as Gate

The enforcement mechanism for the No Log = No Action invariant operates through physical existence gating, where the presence of a valid log entry in hardware-backed non-volatile storage is a necessary electrical or logical condition for action release. The gate is implemented through dedicated hardware pathways that are isolated from general-purpose computation and cannot be overridden through software means, with the gating element combining the log commitment confirmation signal with action request signals to produce release authorization.

In the DITL/MT hardware substrate, this gating is not metaphorical. The Commit Gate is a literal memristive-gated pass transistor whose resistance state determines whether the actuation signal propagates. Its resistance state is set by measuring the TaOx ReRAM cell through the Window Comparator. The Window Comparator enforces the three TL states through resistance thresholds: LRS (~1-10 kΩ) maps to Proceed (+1); IRS (~100 kΩ to 1 MΩ) maps to Epistemic Hold (0); HRS (~1-10 MΩ) maps to Refuse (-1). RC spoof detection with a 5 ns threshold prevents analog attacks on the voltage sensing path.

#### II.6.2 Rejection of Probabilistic Guarantees

The rejection of probabilistic guarantees is fundamental to the invariant's design philosophy. Traditional systems often employ checksums, parity bits, or error-correcting codes that provide high probability of fault detection without absolute certainty, accepting the residual undetected error rate as negligible for practical purposes. The No Log = No Action invariant explicitly excludes such probabilistic mechanisms from the critical path of enforcement, requiring instead cryptographic verification with security parameters chosen such that the probability of successful attack or undetected fault is below any physically realizable threshold.

The physical existence gate thus embodies a deterministic security property: given correct hardware implementation, the gate state is a strict function of the log entry state, with no probabilistic or computational approximations that could be exploited to achieve bypass. The only failures permitted are detectable failures that trigger safe harbor transition, never silent failures that permit unlogged execution.

#### II.6.3 Inductive Proof Obligations for State Transitions

Inductive proof obligations establish that the No Log = No Action invariant is preserved across all possible system evolutions. The base case requires that the initial system state satisfies the invariant, with no actions released at system initialization and empty log state trivially satisfying the implication. The inductive step requires that for any state satisfying the invariant, all possible successor states similarly satisfy the invariant, considering the effects of logging operations, action releases, and concurrent system activities.

The proof proceeds by case analysis on transition types. For logging transitions that add entries to the accumulator, the invariant is preserved by construction as the new committed state enables subsequent action release. For action release transitions, the transition is only permitted when the invariant's precondition is satisfied, with the hardware gating logic enforcing this check. For all other transitions including internal computation, state queries, and error handling, the invariant is preserved trivially as the truth values of relevant predicates remain unchanged.

---

## III. Cryptographic Actuator Interlock and Execution Coupling

### III.1 Protocol-Level Execution Gating

#### III.1.1 Write-Before-Release Model Embedding

The transformation of logging from observability mechanism to protocol-level execution gate represents the central architectural innovation of the No Log = No Action invariant. In this architecture, the logging subsystem is not merely a consumer of execution events but an active participant in the execution authorization protocol, with the ability to permit or deny action release based on the state of log persistence. The write-before-release model embeds this participation directly into the execution path, such that the attempt to release an action necessarily traverses the logging verification logic, with no alternative pathway that could circumvent this traversal.

This embedding is architectural rather than merely procedural. The hardware and software interfaces are designed such that there is no execution path that bypasses the logging gate. This stands in contrast to systems where logging calls are inserted at strategic points but could be omitted or circumvented through alternative code paths. The protocol-level nature of the gate means that it operates on the same data structures and control flows as the execution logic itself, with the logging subsystem participating in transaction coordination and failure handling.

#### III.1.2 Log Subsystem as Execution Gatekeeper

The logging subsystem functions as the execution gatekeeper through its exclusive control over the capability token required for action release. This gatekeeper role is enforced by hardware access controls rather than software convention, with the logging subsystem's hardware state machines being the only entities capable of generating valid capability tokens. The gatekeeper function encompasses: validation of log entry completeness against the canonical serialization, hashing, and persistence criteria; Merkle accumulator update to incorporate the new entry with cryptographic binding to prior history; and capability token issuance in the form of the updated accumulator root that enables action release.

The gatekeeper's denial capability is as important as its issuance capability: any attempt to execute an action without presenting a valid capability token, or with a token that fails verification, triggers immediate fault generation and safe harbor transition. This denial is non-negotiable and non-overrideable, with no administrative procedure, emergency protocol, or maintenance mode that can force action release without valid logging.

#### III.1.3 Merkle Accumulator Root as Capability Token

The Merkle accumulator root serves as the execution capability token that materializes the abstract LogCommitted predicate in a form that can be efficiently verified by hardware interlock mechanisms. The Merkle accumulator is a cryptographic commitment structure that enables compact representation of a set of log entries with efficient membership verification, constructed as a balanced binary tree where each internal node contains the hash of its children and the root contains a commitment to the entire set. For each log entry created, the entry is inserted into the accumulator through a defined update procedure that recomputes the path from leaf to root, with the new root value representing the updated set commitment.

The root value is maintained in hardware-protected registers that are readable by the interlock logic but modifiable only by the logging subsystem through authenticated update operations. The execution gate verifies that the presented log entry identifier corresponds to a valid inclusion proof against the current accumulator root, with verification failure triggering immediate fault and safe harbor transition.

### III.2 Hardware-Protected Register Architecture

#### III.2.1 Logging-Exclusive Modification Rights

The registers maintaining the Merkle accumulator root and related capability state are implemented as hardware-protected structures with access controls that enforce logging-subsystem exclusivity. These registers are readable by the execution gating logic for verification purposes but modifiable only by the logging subsystem's hardware state machines, with no processor instruction, DMA transfer, or debug interface capable of direct modification. The protection mechanisms include: physical isolation of register files from processor memory maps; dedicated clock domains that prevent timing attacks; and tamper detection that triggers register clearing and system halt upon physical intrusion attempts.

#### III.2.2 Invalid Token Detection and Fault Generation

Invalid token detection occurs on every action execution attempt, with the hardware comparing the current capability register value against the expected range for valid states. Detection encompasses: stale tokens that reference accumulator states superseded by subsequent updates; forged tokens that fail cryptographic verification against the logging subsystem's public key; malformed tokens that do not parse as valid Merkle inclusion proofs; and absent tokens where no capability is presented for verification. Any of these conditions triggers immediate non-maskable interrupt, transferring control to the safe harbor handler without completing the attempted action.

#### III.2.3 Immediate Safe Harbor Transition on Violation

The safe harbor transition on capability token violation is immediate and unconditional, with no software or firmware path that could delay or prevent the transition once detection occurs. The safe harbor state is defined by application domain: for cyber-physical systems, it comprises kinetic energy minimization with bounded convergence time, controlled deceleration with bounded jerk and acceleration profiles, and passive stability achievement without active control; for financial systems, it comprises immediate transaction halting and liquidity preservation protocols that prevent new obligation creation while maintaining asset availability.

### III.3 Triple Cryptographic Requirements for Release

Actuator release requires the simultaneous satisfaction of three independent cryptographic requirements.

First, valid log hash with preimage resistance and collision resistance: the hash must correspond to a canonicalized log entry whose preimage is available for verification, providing at minimum 128-bit collision resistance.

Second, hardware-generated attestation quote: a TPM-generated or enclave-generated signed statement binding the current Merkle root, a monotonic counter value, and a freshness nonce, signed by a key resident within the hardware trust boundary. For DITL/MT deployments, the PUF binding hash SHA3-256(K_PUF ∥ device_serial_OTP ∥ log_session_nonce) is included in the attestation quote, binding the quote to the specific silicon instance.

Third, inference containment verification: for systems operating within the Ternary Logic decision framework, the log entry must include the complete decision vector, the TL state reached (Proceed +1, Epistemic Hold 0, or Refuse -1), and the confidence metrics that determined the state, ensuring that the decision process is fully captured before its result is released.

### III.4 Non-Bypassability Guarantees

#### III.4.1 Administrative Privilege Exclusion

The architectural design explicitly excludes administrative privilege as a mechanism for bypassing execution gating. Traditional superuser or root privileges that enable unrestricted system access do not extend to the capability token registers or the execution release gate. This exclusion is implemented through hardware access controls that are not subject to software configuration, with physical isolation preventing any software-privileged operation from affecting the gate state.

#### III.4.2 Hypervisor and System Management Mode Prohibition

Hypervisor code, including type-1 and type-2 hypervisors with full system visibility and control, is similarly constrained by the hardware-enforced gating mechanism. System management mode (SMM) firmware, which on x86 platforms operates with processor privileges exceeding even the hypervisor, is explicitly prohibited from bypassing execution gating. These comprehensive exclusions ensure that the invariant is enforced through hardware rather than policy, eliminating the gap between intended and actual enforcement that characterizes software-based security controls.

#### III.4.3 Firmware-Level Override Prevention

Firmware updates must themselves satisfy the invariant, with update images logged and verified before activation. The boot ROM measurement chain extends to firmware logging initialization, with the logging subsystem firmware explicitly measured and attested before activation. Any attempt to modify firmware to bypass logging requirements is detectable through measurement mismatch and prevents system initialization.

### III.5 Transactional Commit Semantics

The logging and execution operations are structured as a distributed transaction with atomic commit semantics. The transaction scope encompasses: log entry generation and serialization; hash computation and accumulator update; physical persistence and read-back verification; capability token issuance; and action release signal generation. All stages must complete successfully for the transaction to commit; any failure at any stage triggers complete rollback with no external effects.

The critical property is that the failure of any component of the logging obligation prevents any component of the action from executing. This all-or-nothing semantics eliminates the hazard conditions that plague non-atomic logging systems, where crashes or faults during log flush may leave actions executed but unlogged.

---

## IV. DITL/MT Hardware Substrate

### IV.1 Architecture Overview

The Delay-Insensitive Ternary Logic (DITL) substrate is the asynchronous circuit layer that physically implements NL=NA enforcement. Mandated Ternary (MT) is the hardware implementation layer above DITL, mapping the three TL governance states to silicon-level voltage and resistance conditions. Together, DITL/MT constitutes the hardware substrate that transforms the NL=NA invariant from a formal specification into a physical constraint enforced by the laws of semiconductor physics.

The named baseline is TSMC N2 CoWoS with embedded TaOx 1T1R ReRAM, 2025 PDK. Arrhenius-model retention is rated at 20 years at 85 degrees C. The voltage domain is: 3.3V for Proceed (+1), 1.65V for Epistemic Hold (0), and 0V for Refuse (-1). These are not software-assigned values; they are physical voltage levels on dedicated wires.

### IV.2 TL State to MT Hardware Mapping

The three constitutional states of Ternary Logic map to measurable physical conditions in TaOx ReRAM:

| TL State | Value | Resistance State | Resistance Range | Voltage |
|----------|-------|-----------------|-----------------|---------|
| Proceed | +1 | LRS (Low Resistance State) | ~1-10 kΩ | 3.3V |
| Epistemic Hold | 0 | IRS (Intermediate Resistance State) | ~100 kΩ - 1 MΩ | 1.65V |
| Refuse | -1 | HRS (High Resistance State) | ~1-10 MΩ | 0V |

The significance of this mapping is categorical: governance states are not software variables that can be overwritten. They are resistance conditions in silicon that can only be changed through physical write pulses within defined operating parameters.

### IV.3 DITL Circuit Architecture

The fundamental gate primitive of DITL is the Muller C-element. The Muller C-element cannot generate an output without complete, verified input from all input channels. There is no equivalent of a software "default" or "fallback value" at this layer: if inputs are incomplete, the output does not appear. This property enforces the NL=NA invariant at the gate level, making it impossible for the circuit to proceed without all required log commitment signals being asserted.

Three-voltage single-wire encoding carries all TL state information: Vdd for +1, Vdd/2 for 0, and GND for -1. The circuit operates asynchronously with no global clock, using request/acknowledge handshake signaling between stages. Genuine delay-insensitivity means that no timing assumption about wire delays is required; correctness is maintained regardless of propagation delays across the die.

The topology requirement is inline (series), not sidecar (parallel). A sidecar implementation would allow the actuation path to exist independently of the logging path, with the logging verification running in parallel. In an inline topology, the actuation path physically passes through the verification gate. There is no alternate route. This is the topological expression of the NL=NA invariant.

### IV.4 Physical Enforcement Mechanisms

#### IV.4.1 Window Comparator

The Window Comparator measures TaOx ReRAM resistance to enforce TLState transitions. It is a fail-closed design: any resistance reading outside the valid window for a claimed state causes the gate to default to Refuse (-1). RC spoof detection operates at a 5 ns threshold, detecting attempts to forge a valid resistance reading through capacitive manipulation of the sensing line. The independent bandgap reference ensures that comparison thresholds remain stable across the operating temperature range of 0-125 degrees C and supply voltage variation of ±10%.

#### IV.4.2 Commit Gate

The Commit Gate is a memristive-gated pass transistor. Its function is to stand physically in-line on the actuation signal path. When the TaOx cell is in HRS, the Commit Gate blocks the actuation signal. When the TaOx cell is in LRS — and only when it is in LRS, as confirmed by the Window Comparator — the Commit Gate allows the actuation signal to propagate. There is no software path to the Commit Gate. Its state is determined solely by the resistance of the associated ReRAM cell as measured through the Window Comparator.

#### IV.4.3 NL=NA Write Pulse

The NL=NA write pulse is the mechanism by which TLState transitions are recorded in silicon. It is a voltage pulse on a dedicated wire. It is not a software flag, a register write, or a firmware call. When the Governance Lane evaluates an action and reaches a decision, the result is physically written to the TaOx cell through a calibrated voltage pulse that sets the cell to the appropriate resistance state: LRS for Proceed, IRS for Epistemic Hold, or HRS for Refuse. Without this pulse, no state transition occurs. The circuit cannot be advanced by any instruction in the processor's ISA.

#### IV.4.4 Physical Unclonable Function

The PUF generates device-unique identity from post-manufacturing entropy: SRAM power-up states or Ring Oscillator frequency differences on the TSMC N2 die. The PUF output is a 128-bit fuzzy-extractor value. It is not factory-programmed. It cannot be extracted from a powered-off device, since no stored key material exists when the device is unpowered. The PUF-derived key binds every attestation quote and every log session to the specific physical silicon instance. PUF inter-die Hamming distance of approximately 49-51% has been experimentally demonstrated.

### IV.5 Dual-Lane Latency Architecture (DLLA)

The DLLA defines the latency bounds for the two-lane enforcement architecture:

| Lane | Function | Latency Bound |
|------|----------|--------------|
| Inference Lane | Binary computation; proposes actions; never authorizes | ≤2 ms WCET at 99.99th percentile |
| Governance Lane | Ternary constitutional evaluation; authorizes or blocks | ≤300 ms ceiling, 50 ms jitter max |
| Commit Gate | Authorization path overhead | 100-200 ns |

WCET stability requirement: sigma/mu < 10% across temperature 0-125 degrees C, voltage ±10%, and all process corners. The non-blocking constraint is absolute: Epistemic Hold runs parallel to the Inference Lane; it never serially stalls execution. The Inference Lane continues computing its proposal. The Governance Lane evaluates independently. The Commit Gate resolves them. This architecture prevents the Governance Lane from becoming a latency bottleneck while preserving constitutional authority.

### IV.6 Implementation Gap: Architecture B

DITL/MT has been demonstrated at transistor simulation level using IBM PDK 1.2V 130nm CMOS. No fabricated DITL chip exists as of the date of this specification. The gap between simulation and production silicon is a real constraint acknowledged here explicitly.

In deployments where DITL/MT silicon is not yet present, Architecture B is the SHIPPING baseline:

- Software enforcement is active for Layers 1-4 of the five-layer NL=NA stack
- The NULL_PUF_DEPLOYMENT sentinel is set in the NLNAAuditToken, recording the deployment mode honestly in every audit log
- TLCapabilityFlags.pufAttestationMode is set to "ARCHITECTURE_B"
- Layer 5 (TL_Ledger_Core on-chain enforcement) remains active and unchanged

Architecture B does not reduce the constitutional authority of NL=NA. It records honestly that the physical enforcement layer is pending fabrication. When DITL/MT silicon becomes available, the transition from Architecture B to full silicon enforcement requires no changes to Layers 1-4 or Layer 5; only the hardware attestation mode changes, and the NULL_PUF_DEPLOYMENT sentinel is retired.

### IV.7 Adversarial Considerations

Three black-swan adversarial scenarios specific to the DITL/MT substrate are documented for transparency:

**Correlated DITL Hardware Failure Cascade.** If a manufacturing defect or environmental stressor causes correlated failure across multiple DITL gates on the same die, the fail-closed design defaults all affected gates to HRS (Refuse -1). The system halts rather than proceeding with degraded enforcement. This is the correct behavior.

**Foundry Compromise.** Nation-state actors with access to the fabrication mask at the foundry level could in principle introduce backdoors at the silicon level that are undetectable through post-fabrication inspection. PUF attestation and boot ROM measurement chains provide detection capabilities but cannot prevent a mask-level insertion. This risk is acknowledged as a residual structural constraint.

**Side-Channel Extraction.** DITL delay-insensitivity resists timing attacks by design. However, power and electromagnetic side channels remain active and are not addressed by DITL architecture alone. Standard power analysis countermeasures (dual-rail pre-charge logic, power analysis masking) are required in high-threat deployments and are not intrinsic to the DITL circuit.

---

## V. Hardware Root of Trust

### V.1 Secure Enclave Integration

Secure enclaves provide isolated execution environments where the logging subsystem and execution gate logic operate with protection from observation and modification by software outside the enclave boundary. The enclave boundary encompasses the processors, memory, and hardware accelerators dedicated to log processing, with cryptographic mechanisms ensuring that code and data within the enclave cannot be accessed by software outside, including the operating system, hypervisor, and firmware.

Within an SGX enclave, the logging subsystem's hash computation, Merkle accumulator update, and attestation quote generation execute in hardware-protected memory. ARM TrustZone partitions the system into Secure World and Normal World, with the logging subsystem and execution gate operating in Secure World where Normal World software, regardless of privilege level, cannot access secure memory or registers.

### V.2 Trusted Platform Module Functions

#### V.2.1 Platform Integrity Measurement and Reporting

The TPM 2.0 module conforming to ISO/IEC 11889 provides foundational platform integrity measurement. Platform Configuration Registers (PCRs) capture the state of system software from boot ROM through firmware to operating system in a chain of hash computations. The extend operation PCR_new = Hash(PCR_old ∥ measurement) is irreversible: PCR values cannot be rolled back or set to arbitrary values. Each subsequent boot stage is measured and extended into designated PCRs before execution, creating a measurement chain that can be remotely verified through TPM attestation quotes.

#### V.2.2 Secure Key Storage and Cryptographic Operations

The TPM's secure key storage protects signing keys used for log entry authentication and attestation keys used for quote generation, with keys marked as non-migratable and non-exportable. Key usage for signing operations is restricted through authorization policies that may require specific PCR values, authorization values, or physical presence indicators. The monotonic counters provide hardware-protected sequence numbers that prevent replay attacks on log entries.

#### V.2.3 Attestation Quote Generation for Local Commit

Attestation quote generation by the TPM provides the hardware-generated evidence required for local commit acknowledgment. A quote includes: the current PCR values representing platform state at quote generation time; a nonce provided by the verifier to prevent replay; and a timestamp from the TPM's protected clock. For DITL/MT deployments, the log entry hash is incorporated into the quote through PCR extension prior to generation, and the PUF binding hash is included, binding the quote to both the specific log entry and the specific silicon instance.

### V.3 Hardware Security Module Backing

HSMs conforming to FIPS 140-3 Level 3 provide tamper-resistant key storage and cryptographic operations. Level 3 modules incorporate tamper-detection circuitry, including conductive mesh layers, light sensors, voltage monitors, and temperature sensors, that triggers immediate zeroization of all plaintext Critical Security Parameters upon detection of physical intrusion. The named baseline is Thales Luna 7 HSM. Keys generated within the HSM boundary never leave that boundary in plaintext.

The RISC-V Keystone TEE provides an open-source verified execution environment for deployments where vendor-controlled enclaves (Intel SGX, ARM TrustZone) are not acceptable from a trust perspective.

### V.4 Full Trust Chain Construction

The trust chain begins in immutable boot ROM and extends through UEFI firmware, bootloader, operating system kernel, logging subsystem initialization, and into the DITL/MT hardware layer. The PUF binding provides device-unique identity at the silicon layer. The boot ROM measurement chain provides software-layer integrity. The TPM attestation chain provides verifiable proof of the complete sequence to any remote verifier. The logging subsystem's initialization is itself the first log entry in the accumulator, creating a self-referential attestation that binds all subsequent logging to the initialization integrity.

Runtime continuous attestation re-measures critical code and data structures during operation, with unexpected measurement changes triggering safe harbor transition.

### V.5 Software-Only Enforcement Insufficiency

Software-only enforcement fails against four documented attack vectors: kernel compromise (full physical memory access, no execution constraint); hypervisor escape (documented vulnerabilities enable host memory access from guest VM); SMM subversion (SMM callout vulnerabilities allow OS-level code to execute at SMM privilege and modify SPI flash); and supply chain substitution (compromised firmware subverts the entire software stack from before OS load).

Only hardware enforcement, where the electrical path to the actuator physically traverses a verification gate independent of the CPU's software execution environment, eliminates these classes of bypass.

---

## VI. Ternary Logic Mapping and Epistemic Hold / Solvency Protocol

### VI.1 Triadic Decision Space Definition

#### VI.1.1 Proceed State (+1): Committed Execution

The Proceed state (+1) represents committed execution where confidence thresholds are satisfied, inputs are consistent and complete, and all preconditions for action are verified. In the MT hardware substrate, Proceed corresponds to LRS (~1-10 kΩ). The NL=NA write pulse sets the TaOx cell to LRS. The Window Comparator confirms the resistance reading. The Commit Gate transitions from blocking to conducting. The actuation signal propagates. The transition to Proceed is itself a logged event, with the complete justification record committed before the Commit Gate opens.

#### VI.1.2 Refuse State (-1): Definitive Rejection

The Refuse state (-1) represents definitive rejection where the system has determined that action is inappropriate, unsafe, or unauthorized. In the MT hardware substrate, Refuse corresponds to HRS (~1-10 MΩ). The Commit Gate in HRS blocks all actuation signals regardless of any software or firmware instruction. Refuse transitions require the same logging completeness as Proceed, with the rejection rationale fully documented.

The explicit representation of refusal as a distinct hardware state, rather than simple inaction or error return, closes accountability gaps that plague traditional systems where the absence of action is difficult to distinguish from failure to consider action.

#### VI.1.3 Epistemic Hold State (0): Suspended Deliberation

The Epistemic Hold state (0) represents suspended deliberation when confidence is insufficient for reliable classification into Proceed or Refuse. In the MT hardware substrate, Epistemic Hold corresponds to IRS (~100 kΩ to 1 MΩ). The Commit Gate in IRS neither fully conducts nor fully blocks: it holds the system in a physically indeterminate state that mirrors the semantic indeterminacy of the decision. No action can be released from an Epistemic Hold state without explicit resolution.

Epistemic Hold is not a failure mode. It is a deliberate, architecturally supported outcome that preserves optionality while preventing premature commitment. The Epistemic Hold state persists across power cycles without software reinitialization — this is one of MT's two discontinuous advantages over conventional NVRAM: the hardware-semantic persistence of the Epistemic Hold state in silicon, not in volatile memory.

### VI.2 Solvency Protocol in Financial Contexts

In financial and economic decision-making contexts, the Epistemic Hold state implements the Solvency Protocol. When an algorithmic trading system, credit assessment engine, or settlement processor encounters ambiguous market conditions, conflicting signals, or data quality degradation, the system enters the Solvency Protocol state, which halts all pending transactions, preserves current positions without modification, and logs the complete market state snapshot, the pending transaction queue, and the specific conditions that triggered the hold.

The Solvency Protocol recognizes that financial actions, once executed, may create irreversible obligations and propagate instability through interconnected networks. Epistemic Hold enforcement prevents such commitment under uncertainty, maintaining capital and contractual capacity that would be consumed by premature action.

### VI.3 Epistemic Hold Trigger Conditions

Epistemic Hold is mandatory under four conditions:

**Insufficient confidence metrics.** Calculated confidence in decision outcomes falls below configured thresholds, whether due to model uncertainty, input quality degradation, or out-of-distribution conditions. The confidence threshold calibration is subject to ongoing validation, with historical performance compared against actual outcomes to detect miscalibration.

**Conflicting input detection.** Multiple information sources provide mutually inconsistent data that cannot be reconciled within the decision cycle's time budget. Conflicting inputs are preserved in the suspension log with full content of each source, provenance documentation, conflict metrics, and resolution algorithm applied.

**Incomplete data states.** Required information is missing, delayed beyond timeout thresholds, or fails quality checks. The system maintains explicit schemas of data requirements for each decision type, with Epistemic Hold triggered by any schema violation.

**Outlier detection beyond validated distribution envelopes.** Inputs exceed configured standard deviations from trained distribution envelopes, or violate topological data analysis constraints indicating manifold structure disruption. Detection employs Mahalanobis distance, local outlier factor scores, or isolation forest path lengths depending on feature space dimensionality. Complete feature vectors, nearest neighbor references, and reconstruction error from autoencoder models are logged for post-hoc determination of whether the outlier represented genuine novel conditions or adversarial inputs.

### VI.4 Forced Continuation Prevention

Forced continuation prevention from Epistemic Hold is enforced through three mechanisms.

First, cryptographic time-lock mechanisms using the Wesolowski VDF construction require that a minimum wall-clock time must elapse between hold entry and any subsequent state transition. The VDF output cannot be accelerated by parallel computation.

Second, external pressure detection through timing analysis monitors attempted override patterns. Command arrival rates exceeding human interaction capabilities, or synchronization anomalies suggesting coordinated external manipulation, trigger automatic audit events.

Third, a complete audit trail of all override attempts is maintained: every request to exit Epistemic Hold is logged with the identity of the requestor, the justification provided, the timestamp, and the current system state, with this log entry committed before the override can be evaluated.

### VI.5 Mandatory Logging of All Three State Outcomes

The mandatory logging of all three state outcomes, Proceed, Refuse, and Epistemic Hold, creates a complete record of system deliberation. The No Log = No Action invariant applies to all three states equally: a Proceed decision that is not logged cannot release the action; a Refuse decision that is not logged cannot release the refusal notification; an Epistemic Hold that is not logged cannot release the hold signal or initiate escalation procedures. The logging format for state outcomes is standardized across decision types, with cryptographic protection through the Merkle accumulator ensuring tamper-evidence and non-repudiation.

---

## VII. Cryptographic Non-Repudiation of Action

Every action under this specification generates verifiable prior log requirements establishing complete chains of proof from system initialization through current operational states. These chains utilize Merkle proof techniques providing logarithmic-size evidence of entry inclusion and chronological ordering, enabling efficient verification that any specific action was preceded by its complete documentary precedent without requiring transmission of entire log histories.

Digital signature binding connects actor identity to action commitments through asymmetric cryptographic mechanisms. In DITL/MT deployments, the signature covers the canonical serialization of the log entry, the TL state reached, the decision vector, the timestamp, the monotonic counter value, the hash of the preceding log entry, and the PUF binding hash. This binding ensures that the log entry is non-separable from the specific physical device on which it was generated.

The identity-integrity-logging triad defines the three inseparable components of every auditable action. Identity establishes who authorized the action. Integrity establishes that the log entry has not been modified since commitment. Logging establishes that the action was recorded before it occurred. No component of this triad can be satisfied without the other two.

Invalid execution states and their mandatory responses: an orphaned action triggers immediate safe harbor transition, key rotation for all signing keys that may have been compromised, and quarantine of the affected log segment. A hash mismatch triggers safe harbor transition, isolation of the affected segment, and forensic investigation. A signature verification failure triggers safe harbor transition, revocation of the associated signing key, and notification to all relying parties.

---

## VIII. Cryptographic Primitives and Adversarial Resistance

Canonicalization eliminates representation ambiguity through deterministic serialization conforming to RFC 8785 (JSON Canonicalization Scheme) for text-format logs or deterministic CBOR (dCBOR) for binary-format logs. Append-only structures including Merkle accumulators conforming to RFC 9162 (Certificate Transparency v2) ensure tamper evidence through avalanche sensitivity where single-bit modifications propagate through entire subsequent chains.

Replay protection deploys nonce inclusion from hardware random number generators combined with monotonic counters maintained in hardware-backed non-volatile storage, preventing rollback or reuse. In DITL/MT deployments, the monotonic counter increment is hardware-atomic: it occurs simultaneously with the NL=NA write pulse, ensuring that counter and resistance state are always consistent.

Logging suppression countermeasures utilize redundant channels with Byzantine fault tolerance following the PBFT protocol of Castro and Liskov, with the Logres protocol providing formally verified (in Isabelle/HOL) guarantees of agreement, completeness, and liveness. Cross-verification between independent log instances, following the Certificate Transparency model of monitors and auditors, detects split-world attacks.

Insider threat mitigation requires M-of-N authorization for all operations that could affect log integrity. No single individual or credential can modify log retention policies, access raw log storage, rotate signing keys, or approve manual overrides.

Silent action prevention leverages power consumption correlation: power consumption during periods logged as idle that exceeds the baseline profile indicates unlogged computation. This physical-layer tamper detection is independent of and complementary to all software-layer mechanisms.

Post-commit immutability is enforced through WORM (Write Once Read Many) storage at hardware level, combined with software-layer enforcement through systems such as SealFS implementing transparent tamper-evident logging with HMAC ratchet chains.

---

## IX. Failure Modes and Cyber-Physical and Financial Safe Harbor States

This specification requires fail-closed behavior across all critical failure modes. Storage failure, hashing inconsistency, buffer exhaustion, HSM communication loss, key rotation failure, and certificate expiration all trigger immediate cessation of action execution rather than degraded or unlogged operation.

In DITL/MT deployments, the fail-closed property is physically enforced: the Commit Gate defaults to HRS (Refuse -1) in any undefined or error state. The Window Comparator's fail-closed design means that any resistance reading outside valid windows causes the gate to default to HRS. There is no "fail-open" mode in the silicon.

For cyber-physical systems, the safe harbor state comprises kinetic energy minimization with bounded convergence time established through Lyapunov stability analysis, with a Control Lyapunov Function V(x) such that V_dot(x) ≤ -αV(x) for some α > 0 along all trajectories; controlled deceleration with bounded jerk and acceleration following a seven-segment S-curve profile; and stable equilibrium verified through Lyapunov stability criteria. For financial systems, the safe harbor state comprises immediate transaction halting and liquidity preservation preventing new obligation creation while maintaining reserve levels.

The specification enforces clear separation between high-level decision authority denial and low-level control stability preservation. When the logging subsystem fails and execution is halted, low-level stabilizing controllers continue to operate within pre-defined safe harbor parameters. These controllers do not require high-level decision authority; they execute fixed, pre-validated control laws logged at system initialization.

State machines governing failure mode transitions are model-checked to verify that all transitions lead to safe states. The safety property AG(state ∈ {Normal, Degraded, Safe_Harbor_Transition, Safe_Harbor_Steady, Recovery}) and the liveness property AG(Logging_Failure → AF(Safe_Harbor_Steady)) are both verified.

Manual override procedures require: physical presence verified through local authentication that cannot be satisfied remotely; multi-party authorization with M ≥ 2 from organizationally independent roles; and complete logging of all override actions through a secondary battery-backed recording channel if the primary logging subsystem is inoperative.

---

## X. Integration with Dual-Lane Architecture

### X.1 Inference Lane: Local Hardware-Backed Commitment

The Inference Lane is the binary computation layer that proposes actions. It never authorizes them. The Inference Lane executes within a strict WCET bound of ≤2 ms at the 99.99th percentile, implemented through dedicated FPGA or ASIC hardware pipelines that execute canonical serialization, SHA-3-256 hashing, Merkle accumulator update, monotonic counter increment, ReRAM write, and read-back verification entirely within programmable logic without dependency on a general-purpose CPU or operating system scheduler. Battery-backed non-volatile accumulators ensure that committed log entries survive power interruption without explicit flush operations.

The Inference Lane satisfies the NL=NA invariant for its own operations: the actuator interlock verifies commitment against the Inference Lane accumulator, and action release occurs only after Inference Lane commitment is complete. The formal property is AG(exec(a) → inference_committed(a)).

### X.2 Governance Lane: Constitutional Evaluation Layer

The Governance Lane is the ternary constitutional evaluation layer that authorizes or blocks every action proposed by the Inference Lane. The Governance Lane operates within a ≤300 ms ceiling with 50 ms jitter maximum. It evaluates the complete TL decision framework: confidence metrics, pillar certifications, regulatory compliance, and constitutional constraints. Its output is the PermissionToken with laneOrigin const "GOVERNANCE_LANE", which is the only token that can authorize execution through Layer 2 of the five-layer NL=NA stack.

The Governance Lane runs parallel to the Inference Lane. It does not stall the Inference Lane while evaluating. The Commit Gate resolves the two lanes: if the Governance Lane reaches Proceed (+1), the Commit Gate transitions to LRS and the actuation signal propagates; if the Governance Lane reaches Refuse (-1) or Epistemic Hold (0), the Commit Gate remains in HRS and the Inference Lane's proposal is blocked regardless of its own computational result.

### X.3 Asynchronous Anchoring and Gap Tolerance

The Governance Lane provides asynchronous anchoring to distributed ledgers, timestamp authority services conforming to RFC 3161, and multi-party transparency logs conforming to RFC 9162 for external auditability. This anchoring batches committed entries into Merkle trees and anchors batch roots to external verifiable data structures.

Delayed anchoring does not violate the NL=NA invariant. The invariant requires that a log entry be committed to local hardware-backed non-volatile storage before action release. This requirement is satisfied entirely by the Inference Lane and Governance Lane local commitment. Anchoring provides supplementary external auditability and global temporal ordering.

Governance Lane failures, including network partition, ledger congestion, or timestamp service unavailability, do not block Inference Lane operation. The gap tolerance between local commitment and external anchoring is bounded by application-domain safety constants and monitored in real time.

The formal property bounding the gap is: AG(inference_committed(a) → A[¬gap_exceeded U governance_anchored(a)]), stating that from any state where a is committed in the Inference Lane, the gap tolerance is never exceeded before a is anchored in the Governance Lane, on all paths where anchoring eventually succeeds.

---

*No Log = No Action. The right to act is derived from the act of remembering.*
