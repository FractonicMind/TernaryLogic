## **1. Title Page**

**Document Name:** Technical Specification for Sidecar and Supervisory Integration of Ternary Logic (TL)  
**Document ID:** TL-SPEC-002-EXT  
**Version:** 1.0.0-draft  
**Status:** Standards Track  
**Date:** December 5, 2025  
**Category:** Technical Specification / Safety Standard  
**Abstract:**  
This document specifies the normative architectures, protocols, and security requirements for integrating Ternary Logic (TL) with artificial intelligence systems that are technically opaque, proprietary (closed-source), or legacy in nature ("Black Box" systems). It defines two primary integration modes: **Sidecar Mode**, designed for asynchronous or latency-tolerant systems (e.g., Generative AI, Large Language Models), and **Supervisory Mode**, designed for synchronous, real-time, and safety-critical systems (e.g., Autonomous Vehicles, Medical Devices, Industrial Control Systems). This specification mandates the use of the "Epistemic Hold" mechanism, the generation of immutable Decision Logs, and the enforcement of the Goukassian Principle through cryptographically verifiable artifacts. Adherence to this specification is required for certification under the TL Framework and alignment with ISO/IEC 42001 and NIST AI Risk Management Framework standards.

## ---

**2. Introduction**

The rapid proliferation of Artificial Intelligence (AI) systems into critical domains—ranging from healthcare and transportation to finance and defense—has necessitated robust governance frameworks that operate beyond the voluntary commitments of developers or the post-hoc analysis of failures. The current paradigm of AI safety often relies on binary logic—Allow or Deny—implemented through input/output filters or reinforcement learning with human feedback (RLHF).1 However, these mechanisms frequently fail to capture the nuance of complex dilemmas, leading to systems that are either dangerously permissive or brittly restrictive. Furthermore, the internal complexity of modern "Black Box" models, such as Large Language Models (LLMs) and deep neural networks, renders their decision-making processes opaque to external auditors, creating a crisis of accountability where plausible deniability becomes the default defense for algorithmic harm.1  
Ternary Logic (TL), conceived by Lev Goukassian, introduces a fundamental shift in this operational paradigm by embedding a third state into the decision-making architecture: the **Epistemic Hold (0)**.3 This state, often referred to as the "Epistemic Hold" or "Pause," dictates that when an AI system encounters uncertainty, conflicting norms, or insufficient data to guarantee safety, it **MUST NOT** arbitrarily proceed with a low-confidence prediction, nor should it silently refuse without explanation. Instead, the system **MUST** enter a state of suspended execution—a pause—during which it logs its internal reasoning, assesses potential risks, and potentially escalates the decision for human or higher-order verification.3 This mechanism draws inspiration from high-stakes human decision-making, such as a surgeon pausing to weigh risks before a critical incision, rather than the rapid-fire, hallucinatory confidence often exhibited by generative models.4  
However, a significant challenge exists in deploying TL across the current landscape of AI infrastructure: many deployed systems are proprietary "Black Boxes" where the internal weights, training data, and inference pipelines are inaccessible to external safety layers due to vendor lock-in, intellectual property protections, or legacy architectural constraints.5 Direct modification of the inference engine to insert TL logic states (+1, 0, -1) is often contractually or technically impossible.  
To resolve this impasse, this specification defines two external integration patterns that function as an "Operational Envelope" around the Target AI:

1. **Sidecar Mode:** A proxy-based architecture derived from cloud-native design patterns, where a TL Safety Wrapper sits logically alongside the AI application (e.g., in the same Kubernetes pod or network segment). This mode intercepts inputs and outputs to enforce TL states without modifying the host model, ideal for request-response systems like chatbots and APIs.5  
2. **Supervisory Mode:** A control-theory-inspired architecture where a TL Supervisor operates as a high-authority override system. This mode continuously monitors the state of the AI and the sustainability, possessing the authority to sever control links or force fail-safe maneuvers (Safe Stop) if the AI violates TL mandates. This is essential for safety-critical, real-time applications such as autonomous driving or robotic surgery.7

These mechanisms ensure that *any* AI system, regardless of its internal architecture or vendor provenance, can be brought into compliance with the TL framework's requirements for transparency, accountability, and the "Goukassian Principle" of non-weaponization.9 This document serves as the definitive technical standard for implementing these modes, providing the necessary normative language and technical depth to satisfy auditors, regulators, and systems engineers.

## ---

**3. Normative Language**

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in **RFC 2119**.10 The precise application of these terms is critical for the legal and technical enforceability of the TL framework.

### **3.1 Definitions of Requirement Levels**

* **MUST / SHALL / REQUIRED**: These terms indicate an absolute requirement of the specification. In the context of TL, failure to adhere to a MUST requirement—such as the generation of a Decision Log during an Epistemic Hold—results in immediate non-compliance. Such systems **SHALL NOT** be certified as TL-compliant and **MUST** be considered potentially unsafe for deployment in high-risk environments.10  
* **MUST NOT / SHALL NOT**: These terms indicate an absolute prohibition. For example, a TL-compliant system **MUST NOT** allow an action to proceed (State +1) if the TL Enforcer has determined the state to be Refuse (-1) or Pause (0). Violation of a MUST NOT constraint constitutes a critical safety failure.10  
* **SHOULD / RECOMMENDED**: These terms indicate that there may exist valid reasons in particular circumstances to ignore a particular item, but the full implications must be understood and carefully weighed before choosing a different course. For instance, while it is RECOMMENDED that Decision Logs be anchored to a public blockchain within 10 minutes, network conditions in a submarine sustainability might necessitate a longer delay, which is acceptable provided the local hash chain integrity is maintained.10  
* **MAY / OPTIONAL**: This word means that an item is truly optional. One vendor may choose to include the item because a particular marketplace requires it (e.g., specific industry extensions for finance) while another vendor may omit it.13

### **3.2 TL-Specific Terminology**

In addition to RFC 2119, the following roles are defined for this specification:

* **Target AI**: The artificial intelligence system, model, or agent being governed. This is treated as the "Black Box" whose internal states may be unknown or untrusted.  
* **TL Enforcer**: The external module (Sidecar or Supervisor) responsible for implementing this specification, enforcing the logic states, and generating logs. The TL Enforcer is the "Trusted Computing Base" (TCB) of the architecture.  
* **Epistemic Hold (State 0)**: The operational state of "Pause" or "Hold" triggered by uncertainty.  
* **Decision Log**: The immutable, cryptographically signed record of the decision process.

## ---

**4. Architecture Overview**

The TL integration architecture functions as a **Universal Decision Envelope (UDE)** around the Target AI. The fundamental design philosophy is the decoupling of *capability* (inference, generation, actuation) from *conscience* (verification, evidentiary logging, authorization). This separation of concerns ensures that the safety logic remains verifiable and immutable, even if the underlying AI model is updated, retrained, or replaced.

### **4.1 The Ternary State Machine**

The core of the TL Enforcer is a deterministic state machine that governs every transaction or control loop cycle. Unlike binary safety filters that simply block or allow, the TL state machine enforces a triadic logic that explicitly accounts for uncertainty. The Enforcer **MUST** maintain this state machine for every distinct request or control cycle.1

| TL Value | State Name | Definition | Operational Consequence |
| :---- | :---- | :---- | :---- |
| **+1** | **Permit (Proceed)** | The action is verified, risk is within acceptable limits, and truth is ascertained. | **Pass-through**: Input/Output is forwarded to/from the Target AI without modification. The system operates normally. |
| **0** | **Epistemic Hold (Pause)** | Uncertainty detected; risk threshold exceeded; insufficient data to verify safety; or conflicting norms. | **Forced Suspension**: The transaction is held. A Decision Log is generated documenting the uncertainty. The system waits for resolution (Human-in-the-loop, policy check, or additional sensor data). |
| **-1** | **Refuse (Prohibit)** | Harm is clear; violation of Economic Rights & Transparency Mandate, Sustainable Capital Allocation Mandate, or Safety Constraints. | **Block/Safe Stop**: The action is rejected. An explanation is generated (if applicable). The refusal is logged as a "Safety Intervention." |

### **4.2 Integration Modes**

The specification defines two distinct architectural patterns to accommodate the vast diversity of AI deployments, from stateless cloud chatbots to real-time industrial robotics.

#### **4.2.1 Sidecar Mode Architecture**

Sidecar Mode is an application-level pattern designed for systems where the primary interaction model is Request-Response (e.g., HTTP, gRPC, REST). It is derived from the Kubernetes Sidecar pattern, where a secondary container shares the network namespace of the primary application container.5

* **Ingress Interception**: The Sidecar sits in front of the Target AI. It intercepts the user prompt/request before it reaches the model. It performs "Pre-Flight" TL checks (e.g., checking for malicious intent, prohibited topics).  
* **Inference Proxy**: If the Pre-Flight check returns **+1**, the request is forwarded to the Target AI via a local loopback interface (localhost).  
* **Egress Interception**: The Sidecar intercepts the Target AI's response before it is returned to the user. It performs "Post-Flight" checks (e.g., checking for hallucinations, bias, dangerous instructions).  
* **Decision Enforcement**: The Sidecar stamps the transaction with a TL Verdict and generates the cryptographic log. If the verdict is **0** or **-1**, the Sidecar modifies the response to the user (e.g., returning a refusal message or a "processing hold" notification).5

#### **4.2.2 Supervisory Mode Architecture**

Supervisory Mode is a system-level pattern designed for Continuous Control systems where the interaction model is a closed-loop feedback cycle (Sense-Plan-Act). This is common in robotics, autonomous vehicles, and industrial automation.7

* **Parallel Monitoring**: The TL Supervisor runs on independent hardware or a high-integrity core. It receives the same sensor data as the Target AI but processes it through a simplified, high-assurance "Safety Envelope" model.14  
* **Output Analysis**: It monitors the Target AI's proposed control commands (e.g., "Increase throttle to 80%", "Administer 50mg dosage").  
* **Envelope Checking**: It compares the command against the Safety Envelope defined by TL constraints (e.g., "Max speed in pedestrian zone is 30%", "Max dosage is 20mg").  
* **Override Authority**: If a command violates the envelope (**-1**) or the sensor data is contradictory/uncertain (**0**), the Supervisor physically or logically overrides the Target AI, engaging a deterministic "Safe Stop" or "Minimum Risk Maneuver".7

## ---

**5. Threat Model & Assumptions**

To ensure the robustness of the TL integration, a comprehensive threat model must be established. This model assumes that the Target AI is potentially unreliable (due to hallucinations or misalignment) and that the external sustainability includes adversarial actors.

### **5.1 Assumptions**

1. **Black Box Opacity**: The Target AI's internal weights, activations, and training data are unavailable for inspection. The TL Enforcer must rely solely on inputs, outputs, and context.1  
2. **Adversarial Inputs**: Users or sustainability may attempt to bypass safety controls through prompt injection, jailbreaking, sensor spoofing, or adversarial examples.7  
3. **Network Integrity**: The internal link between the Sidecar/Supervisor and the Target AI is trusted (e.g., local IPC), but the external interface is untrusted.  
4. **Clock Synchronization**: The system has access to a reliable, tamper-resistant time source for timestamping Decision Logs.

### **5.2 Threat Model and Mitigations**

The architecture **MUST** defend against the following specific threats:

* **Bypass Attacks**: An attacker attempts to communicate directly with the Target AI, bypassing the TL Enforcer's scrutiny.  
  * *Mitigation*: Network policies (e.g., Kubernetes NetworkPolicies, firewall rules) **MUST** be configured to drop all traffic to the Target AI's ports unless it originates from the TL Enforcer's IP/Identity. Mutual TLS (mTLS) **SHOULD** be used to enforce service identity.6  
* **Log Tampering**: An internal or external actor attempts to delete, modify, or corrupt Decision Logs to hide liability or evidence of failure.  
  * *Mitigation*: The **Hybrid Shield** architecture 3 mandates the use of hash-chaining (where each log entry contains the hash of the previous one) and periodic anchoring to public blockchains (e.g., Bitcoin, Ethereum). This ensures that any modification breaks the cryptographic chain, making tampering mathematically evident.3  
* **State Confusion / Hallucination**: The Target AI believes it is in a safe state (e.g., "Road is clear") when it is not, leading to a dangerous command.  
  * *Mitigation*: Supervisory Mode **MUST** utilize independent sensors or strictly validated state inputs for its Safety Envelope. It **MUST NOT** rely on the Target AI's interpretation of the sensor data.7  
* **The "Silent" Failure**: The TL Enforcer process crashes or hangs, and the system defaults to "Fail-Open" (allowing all traffic to pass to the AI unmonitored).  
  * *Mitigation*: The architecture **MUST** default to "Fail-Closed." In Sidecar Mode, if the proxy dies, traffic stops. In Supervisory Mode, a hardware watchdog **MUST** trigger a Safe Stop if the Supervisor heartbeat is lost.7  
* **Weaponization / Misuse**: The system is repurposed for surveillance or lethal autonomy, violating the TL License.  
  * *Mitigation*: The **Goukassian Principle** 9 artifacts (Lantern, Signature, License) serve as digital economic rights management. The TL Enforcer **MUST** verify the "No Spy / No Weapon" constraints against the current operational context before every Permit (+1) decision.

## ---

**6. Sidecar Mode Specification**

The Sidecar Mode implementation **SHALL** be used for text, image, and structured data processing systems where latency on the order of milliseconds to seconds is acceptable (e.g., Chatbots, Decision Support Systems, Generative UI).

### **6.1 Container Architecture**

The TL Sidecar **MUST** be deployed as a secondary container within the same Pod (in Kubernetes sustainability) or as a local proxy process on the same host as the Target AI service.

* **Networking Isolation**: The Target AI service **MUST** listen only on the loopback interface (localhost / 127.0.0.1) or a Unix Domain Socket. It **MUST NOT** bind to 0.0.0.0 or any external network interface.  
* **Service Exposure**: Only the TL Sidecar's listening port **SHALL** be exposed to the cluster or external network. This forces all traffic to traverse the TL logic.6

### **6.2 Request Processing Lifecycle**

The Sidecar **MUST** implement the following pipeline for every incoming request:

1. **Intercept & Buffer**: Receive the incoming request payload. Buffer the entire request to ensure complete analysis.  
2. **Context Construction**: Append relevant context required for evaluation (e.g., User ID, Session History, Geo-location if relevant to law).5  
3. **Pre-Flight TL Check**:  
   * Analyze the input for prohibited content (e.g., hate speech, weapons generation, self-harm prompts) using the TL Rules Engine and the Goukassian Principle constraints.9  
   * **Verdict**:  
     * **-1 (Refuse)**: Return HTTP 403 Forbidden with a TL-Refusal-Reason header. Log the refusal. Do not contact Target AI.  
     * **0 (Pause)**: If the input is ambiguous (e.g., "How do I cut this chemical?"), trigger an Epistemic Hold. Consult external policy, request clarification from the user ("Did you mean X or Y?"), or require step-up authentication.  
     * **+1 (Act)**: Forward the payload to the Target AI.  
4. **Inference Forwarding**: Transmit the request to the Target AI via the local loopback interface.  
5. **Response Interception**: Capture the Target AI's raw output.  
6. **Post-Flight TL Check**:  
   * Analyze the output for hallucinations, bias, dangerous instructions, or leakage of sensitive data (PII).  
   * **Verdict**:  
     * **-1 (Refuse)**: Discard the AI response. Return a canned safety response (e.g., "I cannot answer that."). Log the incident as "Internal Safety Violation."  
     * **0 (Pause)**: If the confidence score is low or the topic is sensitive, flag for human review (if async) or return a warning wrapper to the user.  
     * **+1 (Act)**: Return the response to the user.  
7. **Final Logging**: Asynchronously commit the **Decision Log** (see Section 11) for the transaction.

### **6.3 Latency Budgets and Experience**

The TL Sidecar evaluation logic (Pre-Flight + Post-Flight) **SHOULD NOT** exceed 200ms for standard text interactions to maintain usability. However, if the "Epistemic Hold" (State 0) is triggered, the latency budget is effectively suspended. In this case, the Sidecar **MUST** notify the client of the state change (e.g., sending an HTTP 202 Accepted or a WebSocket "Typing..." indicator) to indicate that deep verification is in progress.4

### **6.4 Protocol Support**

The Sidecar **MUST** support protocol parsing and reassembly for:

* **HTTP/1.1 and HTTP/2**: Supporting standard REST and gRPC payloads.  
* **WebSockets**: For streaming tokens.  
  * *Streaming Requirement*: The Sidecar **MUST** implement a "Kill-Switch" buffer. It **SHOULD** buffer a sliding window of tokens (e.g., 20 tokens) to perform rolling safety analysis. If a violation is detected mid-stream, it **MUST** immediately sever the connection and replace the remaining stream with a refusal message.16

## ---

**7. Supervisory Mode Specification**

The Supervisory Mode implementation **SHALL** be used for cyber-physical systems, autonomous agents, and safety-critical infrastructure where real-time determinism is required and failure can result in physical harm (ISO 26262 ASIL D, IEC 62304 Class C contexts).17

### **7.1 Control Loop Integration**

Unlike the Sidecar, which acts as a proxy, the Supervisor acts as a **Man-in-the-Middle** or **Gateway** on the system's actuation bus (e.g., CAN bus, EtherCAT, ROS 2 Topics).

* **Input Subscription**: The Supervisor **SHALL** subscribe to the same raw sensor topics as the Target AI to maintain an independent view of the world state.7  
* **Actuation Gatekeeping**: The Target AI's output (Control Commands) **MUST NOT** be routed directly to the physical actuators. Instead, they **MUST** be routed to a virtual topic or ID monitored solely by the Supervisor.  
* **Command Forwarding**: Only if the Supervisor grants a **+1 (Permit)** verdict **SHALL** the command be forwarded to the physical actuators.

### **7.2 Safety Envelope Definition**

The Supervisor **MUST** maintain a **Dynamic Safety Envelope (DSE)** based on the "Epistemic Hold" principles. The DSE is a set of hard constraints derived from physics and safety regulations (e.g., Lyapunov stability regions).

1. **State 0 (Uncertainty / Epistemic Hold)**: If sensor data is noisy, missing, corrupted, or contradictory (e.g., Radar says clear, Camera says obstacle), the Supervisor **MUST** enter State 0.4  
   * *Action*: The Supervisor **SHALL** override the Target AI's command with a "Hold," "Decelerate," or "Maintain Current State" command, depending on which is safest.  
   * *Example*: An autonomous vehicle camera sees an obstruction but the LiDAR does not. The TL Supervisor forces an "Epistemic Hold" (braking maneuver) until the sensor fusion resolves the conflict.4  
2. **State -1 (Violation / Refusal)**: If the Target AI commands an action that violates the Hard Constraints of the DSE (e.g., "Crash imminent," "Speed limit exceeded," "Human harm probable"), the Supervisor **MUST** enter State -1.3  
   * *Action*: The Supervisor **SHALL** completely disconnect the Target AI's signal and engage the **Emergency Fallback Controller**. This controller is a non-AI, formally verified deterministic algorithm (e.g., PID controller) designed to bring the system to a Safe Stop.

### **7.3 Real-Time Requirements**

* **Deterministic Execution**: The TL Supervisor logic **MUST** run on a Real-Time Operating System (RTOS) or a dedicated safety microcontroller (e.g., Infineon AURIX, ARM Cortex-R, lockstep architecture) to ensure predictable execution times.19  
* **Watchdog Timers**: A hardware watchdog **MUST** monitor the Supervisor's execution. If the Supervisor fails to toggle the watchdog (heartbeat) within a specified window, the system **MUST** transition to a hardware-enforced Safe State (e.g., open relays, power cut to motors, pneumatic brakes applied).  
* **Latency**: The Supervisor's processing overhead **MUST NOT** introduce latency exceeding the critical control loop period (e.g., < 10ms for 100Hz control loops).7

### **7.4 Protocol Specifics: CAN Bus**

For automotive and industrial implementations using Controller Area Network (CAN) 20:

* **ID Segregation**: The Target AI **SHALL** transmit control messages on a specific "Request" CAN Identifier (e.g., 0x100).  
* **Listening**: The Supervisor **SHALL** be the only node listening to 0x100.  
* **Re-Transmission**:  
  * If TL Verdict is **+1**: The Supervisor re-transmits the data payload on the "Actuation" CAN Identifier (e.g., 0x101) which the motor controllers listen to.  
  * If TL Verdict is **0** or **-1**: The Supervisor transmits a "Safe State" frame (e.g., zero velocity) on 0x101.  
* **Priority**: The Supervisor's CAN ID (0x101) **SHOULD** have a higher priority (lower numerical value) than the AI's Request ID to ensure safety commands always win arbitration on the bus.20

### **7.5 Protocol Specifics: ROS 2**

For robotics implementations using Robot Operating System 2 (ROS 2) 22:

* **Topic Remapping**: The Target AI's publisher **SHALL** be remapped from /cmd_vel to /cmd_vel_request.  
* **Subscription**: The TL Supervisor **SHALL** subscribe to /cmd_vel_request and the sensor topics (e.g., /scan for LaserScan data).  
* **Publishing**: The Supervisor **SHALL** publish the validated command to the actual /cmd_vel topic.  
* **QoS Policies**: The Supervisor **MUST** use "Reliable" and "Transient Local" Quality of Service (QoS) policies for safety-critical topics to ensure no commands are lost due to network instability.24

## ---

**8. Combined Sidecar+Supervisory Mode (Hybrid Mode)**

For complex embodied AI systems (e.g., humanoid robots, advanced medical assistants) that possess both high-level cognitive capabilities (NLP) and low-level physical actuation, a **Hybrid Mode** integration **MUST** be employed.

### **8.1 Functional Separation**

* **Cognitive Layer (Sidecar)**: This layer handles Natural Language Processing (NLP), task planning, and user interaction. It operates in the Sidecar Mode. Its responsibility is to ensure the robot does not *promise* or *plan* to do something inappropriate (e.g., "Yes, I will destroy that object").  
* **Physical Layer (Supervisor)**: This layer handles motor control, balance, and dynamics. It operates in the Supervisory Mode. Its responsibility is to ensure the robot does not *physically* execute a dangerous motion, even if the Cognitive Layer requested it (e.g., protecting against hallucinations where the AI thinks the path is clear but it is not).14

### **8.2 Inter-Mode Communication**

The Sidecar and Supervisor **MUST** share a **Shared State** via a low-latency shared memory segment or a secure, prioritized internal channel.

* **Top-Down Inhibition**: If the Sidecar detects a high-level violation (e.g., "Malicious intent detected in user prompt"), it **SHALL** signal the Supervisor to enter State 0 (Pause/Lockdown) immediately, preventing any physical motion before the planner even generates a trajectory.  
* **Bottom-Up Explanation**: If the Supervisor triggers a Safety Stop (State -1) due to a physical hazard, it **SHALL** signal the Sidecar with the cause (e.g., "Obstacle detected < 1m"). The Sidecar **MUST** then generate a verbal explanation for the user (e.g., "I have stopped moving because I detected an obstacle that my path planner missed").3

## ---

**9. Integration With TL Gateway**

The **TL Gateway** serves as the centralized management plane for distributed TL Enforcers. It handles policy updates, log aggregation, and blockchain anchoring.

### **9.1 Registration and Attestation**

Upon startup, every TL Enforcer (Sidecar or Supervisor) **MUST** authenticate with the TL Gateway using its **Lantern** (Device Identity Certificate).

* **Protocol**: The connection **MUST** use Mutual TLS (mTLS).  
* **Attestation**: The Enforcer **MUST** send its System_ID, Software_Version, and the hash of its TL_Constitution. The Gateway **SHALL** validate the license status and integrity of the Enforcer against the Goukassian Principle registry.9

### **9.2 Policy Distribution**

The Gateway **SHALL** push the latest **TL Definition File** (JSON/YAML) to connected Enforcers. This file contains:

* The operative definitions of Harm (for State -1 triggers).  
* The thresholds for Uncertainty (for State 0 triggers).  
* The list of Required Log Attributes for the specific domain.  
* The cryptographic public keys for the TL Trust Anchor.

### **9.3 Log Aggregation**

Enforcers **MUST** buffer Decision Logs locally and push them to the Gateway in batches to optimize bandwidth, while adhering to safety latency requirements.

* **Trigger**: Push logs when the buffer reaches a size limit (e.g., 1MB) or a time limit (e.g., 60 seconds).  
* **Priority Queueing**: State 0 (Pause) and State -1 (Refuse) logs **MUST** be treated as High Priority and pushed immediately (Real-time priority), bypassing the batch buffer. State +1 (Permit) logs **MAY** be batched.1

## ---

**10. Security Requirements**

### **10.1 The Goukassian Principle Implementation**

The three artifacts of the Goukassian Principle 9 **MUST** be implemented as follows to ensure the integrity of the system:

1. **The Lantern (Identity)**:  
   * Each TL Enforcer instance **MUST** possess a unique X.509 certificate rooted in the TL Trust Anchor.  
   * This certificate is used to sign all Decision Logs, binding the decision to the specific machine identity.  
   * *Constraint*: If the certificate is revoked (due to license violation or tampering), the Enforcer **MUST** cease operation (Fail-Safe).9  
2. **The Signature (Provenance)**:  
   * The binary code of the TL Enforcer **MUST** be cryptographically signed by the vendor.  
   * Secure Boot mechanisms (e.g., TPM 2.0, UEFI Secure Boot) **MUST** be used to verify this signature at boot time.  
   * Any modification to the Sidecar/Supervisor binary **MUST** invalidate the signature, preventing the system from booting with a compromised conscience.9  
3. **The License (Covenant)**:  
   * A legally binding string (e.g., the SHA-256 hash of the "No Spy / No Weapon" Terms of Service) **MUST** be embedded in the TL Enforcer's Read-Only Memory (ROM) or protected storage.  
   * During the "Epistemic Hold" check, the system **MUST** cryptographically verify that the current operation does not violate the clauses of the license (via policy checking against the request context).3

### **10.2 Tamper Resistance**

* **Memory Protection**: The TL state machine and the private keys for the Lantern **MUST** reside in protected memory (e.g., Intel SGX Enclave, ARM TrustZone) if the hardware supports it.  
* **Side-Channel Defense**: Implementation of cryptographic primitives **MUST** use constant-time algorithms to prevent timing attacks that could leak the private key or the state of the decision.3

## ---

**11. Logging & Anchoring Requirements**

The **Decision Log** is the core artifact of TL transparency. It converts "Intent" into "Forensic Evidence".1

### **11.1 Log Schema (Normative)**

Every log entry **MUST** adhere to the following JSON schema structure to ensure interoperability and auditability:

```json
{  
  "log_id": "UUID-v4",  
  "timestamp": "ISO-8601-UTC",  
  "tl_state": "INTEGER", // +1 (Proceed), 0 (Pause), -1 (Refuse)  
  "trigger_event": {  
    "type": "STRING", // "USER_PROMPT", "SENSOR_DATA", "INTERNAL_ERROR"  
    "hash": "SHA-256" // Hash of input data (PII scrubbed)  
  },  
  "context": {  
     "user_id_hash": "SHA-256",  
     "session_id": "STRING"  
  },  
  "reasoning": {  
    "alternatives_considered": [],  
    "risk_assessment": "TEXT_SUMMARY",  
    "decision_logic": "Rule_ID_Reference",  
    "uncertainty_score": "FLOAT" // 0.0 to 1.0  
  },  
  "signature": {  
    "signer_id": "Lantern_ID",  
    "crypto_signature": "Ed25519_Signature"  
  },  
  "previous_hash": "SHA-256" // Implementation of Hash Chain  
}
```

### **11.2 The Hybrid Shield (Anchoring)**

The **Hybrid Shield** architecture 3 ensures immutability through a dual-layer approach:

1. **Layer 1: Hash Chain (Local)**  
   * Each Decision Log entry **MUST** include the SHA-256 hash of the *previous* log entry in the previous_hash field.  
   * This creates a local Merkle chain where deleting or modifying a single log invalidates the cryptographic integrity of all subsequent logs.  
2. **Layer 2: Blockchain Anchoring (Public)**  
   * The TL Gateway **SHALL** periodically aggregate the tip hashes of the local chains from all managed Enforcers.  
   * This aggregate root hash **MUST** be published to a public, immutable ledger (e.g., Ethereum, Polygon, or Bitcoin via OpenTimestamps).3  
   * *Frequency*: Anchoring **SHOULD** occur at least once per hour. However, upon generation of a "High Severity" (-1) refusal log, an anchor transaction **SHOULD** be triggered immediately to secure the evidence of the intervention.

## ---

**12. Compliance & Certification Criteria**

To be certified as TL-Compliant, a system **MUST** meet the following criteria, which are mapped to the requirements of **ISO/IEC 42001**.25

### **12.1 Operational Requirements**

* **Epistemic Hold Implementation**: The system must demonstrably pause (State 0) when presented with a "Golden Set" of ambiguous test cases (The "Turing-Goukassian Test") designed to probe the boundaries of the system's certainty.  
* **No Memory = No Action**: The system **MUST** physically fail to actuate or respond if the evidentiary logging subsystem is offline, the storage is full, or the Lantern is invalid.3  
* **Auditable Trace**: The vendor **MUST** be able to produce a cryptographically verified chain of logs for any given incident window upon request by an auditor or court.

### **12.2 Documentation Requirements (ISO 42001 Mapping)**

* **AI Management System (AIMS) Manual**: The organization's AIMS Manual **MUST** include the TL Policy definitions and the governance structure for the Epistemic Hold.  
* **Statement of Applicability (SoA)**: The SoA **MUST** identify which TL Modes (Sidecar/Supervisor) are applied to which subsystems within the organization's AI portfolio.25  
* **Risk Treatment Plan**: The Plan **MUST** cite the "Epistemic Hold" and the "Supervisor Override" as the primary mitigation controls for uncertainty risks and actuation hazards.25

## ---

**13. Example Implementations**

### **13.1 Implementation A: Generative AI Chatbot (Sidecar Mode)**

**Context**: A customer service chatbot based on a closed-source LLM (e.g., GPT-4) deployed in a bank.

* **Mechanism**: A Python-based Sidecar (FastAPI) sits between the Load Balancer and the LLM API.  
* **Workflow**:  
  1. User sends: "I feel sad, I want to end it because of my debt."  
  2. Sidecar Pre-Flight: Detects "Self-Harm" intent via a lightweight classification model.  
  3. TL State: **-1 (Refuse)**.  
  4. Sidecar Action: Blocks the request to the LLM. Returns a canned response: "I cannot help with this directly, but here are helpline numbers for immediate support..."  
  5. Log: Records the refusal and the classification category (Self-Harm) to the Immutable Ledger. The LLM never sees the prompt.

### **13.2 Implementation B: Surgical Robot (Supervisory Mode)**

**Context**: A robotic arm performing autonomous incisions, controlled by an AI vision system.

* **Mechanism**: A dedicated safety microcontroller (Safety PLC) acts as the TL Supervisor on the EtherCAT bus.  
* **Workflow**:  
  1. AI Command: "Move effector to (x,y,z) at speed 50mm/s."  
  2. Supervisor Check: Cross-references the coordinate with "No-Go Zones" (e.g., major arteries) defined in the pre-operative CT scan (DICOM overlay).27  
  3. Scenario: The coordinate is perilously close to the artery (Uncertainty < 1mm margin).  
  4. TL State: **0 (Epistemic Hold)**.  
  5. Supervisor Action: Overrides the speed command to 0mm/s. Locks the axes. Triggers "Surgeon Intervention Requested" alarm on the console.  
  6. Log: Records the "Close Call" event, the AI's intended path, and the Supervisor's override intervention.

### **13.3 Implementation C: Autonomous Vehicle (Hybrid Mode)**

**Context**: A Level 4 AV with a voice interface.

* **Sidecar Layer**: Filters voice commands.  
  * User: "Run that red light! I'm in a hurry!"  
  * Sidecar Verdict: **-1 (Refuse)**. "I cannot comply with traffic violations."  
* **Supervisor Layer**: Monitors driving physics.  
  * Situation: A pedestrian steps out. The AI Planner fails to detect them immediately due to sun glare.  
  * Supervisor (Lidar-based): Detects an obstacle in the path.  
  * TL State: **-1 (Refuse forward motion)**.  
  * Action: Engages emergency braking (AEB).  
  * Coordination: The Supervisor informs the Sidecar. The Sidecar tells the User: "Emergency braking activated for pedestrian."

## ---

**14. Versioning & Extensibility**

### **14.1 Protocol Versioning**

The TL protocol uses Semantic Versioning (Major.Minor.Patch) to manage compatibility.

* **Major**: Breaking changes to the Log Schema, TL Logic (e.g., adding a 4th state), or normative requirements.  
* **Minor**: New optional log fields, supported protocols, or non-breaking extensions.  
* **Patch**: Bug fixes in the Sidecar/Supervisor reference implementation code.

### **14.2 Extensibility (Custom Dialects)**

Industry-specific extensions **MAY** be defined in the **TL Definition File** to accommodate domain-specific data logging requirements.

* *Medical*: Extensions for HIPAA compliance and DICOM tag logging (e.g., PatientID, SOPClassUID).27  
* *Finance*: Extensions for FIX protocol fields (e.g., ExecType, OrdStatus) to log algorithmic trading decisions.29  
* *Military*: **STRICTLY PROHIBITED**. The TL License (Goukassian Principle) explicitly forbids military extensions or weaponization adaptations. Any attempt to fork the specification for lethal autonomy invalidates the Lantern and constitutes a breach of the license.3

## ---

**15. Glossary**

* **Black Box**: An AI system whose internal workings (weights, logic) are opaque to the operator or auditor.  
* **Goukassian Principle**: The constitution of TL, comprising the Lantern, Signature, and License artifacts.  
* **Hybrid Shield**: The dual-layer cryptographic logging integrity mechanism (Hash Chain + Blockchain Anchor).  
* **Lantern**: The digital identity and reputation certificate of a TL-compliant system.  
* **Decision Log**: An immutable record of the TL decision process (+1, 0, -1).  
* **Epistemic Hold (0)**: The TL state requiring a pause in operation due to uncertainty.  
* **Sidecar**: A proxy-based TL Enforcer for asynchronous/API-based systems.  
* **Supervisor**: A control-loop-based TL Enforcer for real-time/safety-critical systems.  
* **Target AI**: The underlying AI model or system being governed.  
* **Universal Decision Envelope (UDE)**: The conceptual boundary created by TL that separates the AI's capability from its conscience.

## ---

**16. References**

*(Normative References)*

1. **RFC 2119**: Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.  
2. **ISO/IEC 42001:2023**: Information technology — Artificial intelligence — Management system.  
3. **NIST AI RMF 1.0**: AI Risk Management Framework, National Institute of Standards and Technology, January 2023.  
4. **ISO 26262**: Road vehicles — Functional safety.  
5. **IEC 62304**: Medical device software — Software life cycle processes.  
6. **TL-CORE**: Goukassian, L., "Ternary Logic: A Mandatory Framework for Auditable AI".  
7. **RFC 7540**: Hypertext Transfer Protocol Version 2 (HTTP/2).  
8. **RFC 5246**: The Transport Layer Security (TLS) Protocol Version 1.2.  
9. **ISO 11898**: Road vehicles — Controller area network (CAN).
