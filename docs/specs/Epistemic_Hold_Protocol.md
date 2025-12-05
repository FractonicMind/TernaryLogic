**Document ID:** SPP-2025-RFC-001  
**Version:** 1.0.0 (Proposed Standard)  
**Category:** Algorithmic Governance / Computational Evidence  
**Authority:** The Lantern Foundation (Ternary Logic Consortium)  
**Editor:** Operational Evidence Working Group (OEWG)  
**Date:** December 5, 2025  
**Status:** Standards Track

---

**1. Introduction**

### **1.1. The Operational Necessity of Hesitation**

The prevailing architecture of autonomous decision-making has historically relied on a binary logic of execution: a system evaluates an input and yields a deterministic True (Allow/Proceed) or False (Deny/Refuse) state. While computationally efficient, this binary reductionism creates a dangerous "confidence gap" in high-stakes environments. When a probabilistic model—such as a Large Language Model (LLM) or an Autonomous Vehicle (AV) perception stack—encounters a scenario of high epistemic uncertainty, binary logic forces it to "round up" to action or "round down" to refusal. This forcing function is the root cause of "hallucinations" in generative AI, "phantom braking" in AVs, and "flash crashes" in high-frequency trading.1  
The **Epistemic Hold Protocol (EHP)** is the formal technical specification designed to eliminate this binary operational hazard. It converts the philosophical mandate of **Ternary Logic (TL)**—specifically the **Goukassian Principle**—into a rigorous, machine-executable standard.4 The Principle dictates: *"Pause when truth is uncertain. Refuse when economic rights are violated. Proceed where truth is"*.5  
This specification defines the **Epistemic Hold** (State 0) not as a passive delay, but as an active, computational state of "HESITATE." In this state, the system suspends the primary execution vector, initiates a parallel evidence-gathering thread, and engages the **User Decision Environment (UDE)**. The EHP provides the requisite architecture to ensure that no high-impact decision is made without a verifiable chain of custody for the reasoning behind it, satisfying the requirements of "Auditable AI".6

### **1.2. Scope and Applicability**

This standard is applicable to all **High-Impact Autonomous Systems (HIAS)**, defined as any algorithmic system capable of exerting material influence on human safety, financial stability, or fundamental economic rights.  
The EHP acts as a wrapper or "Gateway" around the core model. It applies to:

* **Generative AI:** LLMs requiring hallucination mitigation and safety filtering.1  
* **Robotics & AVs:** Perception systems requiring arbitration between conflicting sensors (Sensor Fusion Conflict).7  
* **Financial Algorithms:** Trading bots requiring volatility circuit breakers.8  
* **Medical Diagnostics:** Decision support systems requiring uncertainty quantification.9

### **1.3. The Goukassian Principle: The Three Artifacts**

Compliance with the EHP requires the implementation of the three "Artifacts of Incorruptibility" defined in the Goukassian Principle 4:

1. **The Lantern (🏮):** A mandatory operational signal indicating that the system has entered State 0. This ensures transparency to the user or observer.10  
2. **The Signature (✍️):** A cryptographic proof of the decision logic, ensuring that the "pause" was systemically generated and logged.11  
3. **The License (📜):** The binding operational constraint that prohibits the system from bypassing the EHP logic ("No Memory = No Action").11



**2. Normative Language**

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 when, and only when, they appear in all capitals, as shown here.

### **2.1. Definitions**

* **Agent:** The computational entity (AI, robot, algorithm) executing the logic.  
* **TL Gateway:** The architectural component (sidecar or proxy) that intercepts input/output vectors to enforce Ternary Logic.  
* **Epistemic Hold (State 0):** The logical state of "HESITATE" or "PAUSE."  
* **Decision Log (DL):** The immutable JSON record generated during an Epistemic Hold, containing the evidence of uncertainty.  
* **Immutable Ledger:** The persistent storage mechanism that anchors DLs to a distributed ledger.11  
* **UDE (User Decision Environment):** The human-machine interface (HMI) that presents the context of the Epistemic Hold to a human operator for resolution.12  
* **Epistemic Uncertainty:** Uncertainty stemming from a lack of knowledge or data (model ignorance), distinct from aleatory uncertainty (inherent randomness).9



**3. Conceptual Overview**

### **3.1. The Ternary State Model**

Unlike binary safety filters that operate on a Pass/Fail basis, the EHP enforces a triadic logic system. The system MUST classify every proposed action into one of three states before execution:

| Logic State | Value | Semantic Name | Operational Definition | Goukassian Mapping |
| :---- | :---- | :---- | :---- | :---- |
| **PROCEED** | **+1** | **Execute** | Confidence > Threshold AND Harm < Limit. The action proceeds immediately. | *"Proceed where truth is"* |
| **HESITATE** | **0** | **Epistemic Hold** | Confidence < Threshold OR Harm == Uncertain. Execution is suspended; investigation initiates. | *"Pause when truth is uncertain"* |
| **REFUSE** | **-1** | **Block** | Harm > Critical Limit. The action is terminated; refusal is logged. | *"Refuse when economic rights are violated"* |

The "Epistemic Hold" (State 0) is the innovation. It is a "Gateway" state—a temporal holding pattern that allows the system to convert "hesitation" from a system error into an evidentiary asset.

### **3.2. System Architecture: The TL Gateway**

The EHP MUST be implemented via a **Gateway Pattern**, specifically utilizing a "Sidecar" architecture in containerized environments (e.g., Kubernetes sidecars).13  
The **TL Gateway** acts as the enforcement layer:

1. **Interception:** All API requests (prompts, control signals) are routed through the Gateway.  
2. **Parallel Evaluation:** The Gateway forwards the request to the Model *and* the Safety Monitor simultaneously.  
3. **State Arbitration:** The Gateway compares the Model's ConfidenceScore and the Monitor's HarmScore against pre-configured triggers (See Section 4).  
4. **Protocol Activation:** * If State 0 is triggered, the Gateway **locks** the output stream.  
   * It activates the **Lantern** signal.  
   * It initiates the **Epistemic Hold Lifecycle** (See Section 5).  
5. **Resolution:** The Gateway only releases the output lock upon receiving a resolution signal (Human Override or Verification Success).

### **3.3. The Philosophy of "Parallel Verification"**

The Epistemic Hold is not merely a "stop." It is a "fork." When the EHP is triggered, the system splits its processing:

* **Vector A (Action):** Maintains a "Safe State" (e.g., AV keeps lane, LLM displays "Thinking").  
* **Vector B (Verification):** Executes the deliberation loop—gathering evidence, querying databases, and logging the event.1

This "Parallel Verification" ensures that the hesitation does not result in catastrophic latency for real-time systems (See Section 7), but still captures the necessary evidentiary evidence.



**4. Trigger Conditions**

The mechanism that initiates an Epistemic Hold is the **Trigger**. Triggers MUST be deterministic, quantifiable, and domain-specific. The EHP defines four normative categories of triggers.

### **4.1. Uncertainty Triggers (Epistemic Uncertainty)**

The system MUST trigger State 0 when it detects that it "does not know" the answer with sufficient reliability. This prevents the "hallucination" of certainty.

* **Metric:** The primary metric for this trigger is **Shannon Entropy** or **Predictive Variance** (e.g., via Monte Carlo Dropout or Ensemble Disagreement).9  
* **Specification:** * Let $H(y|x)$ be the entropy of the prediction distribution.  
  * Let $T_{unc}$ be the uncertainty threshold.  
  * **IF** $H(y|x) > T_{unc}$ **THEN** State = 0.  
* **Rationale:** High entropy indicates the model is distributing probability mass across multiple conflicting outcomes. In a medical context, this might mean the model is equally unsure if a tumor is benign or malignant.11 The Principle demands a pause here.

### **4.2. Harm Triggers (The Asimovian Override)**

The system MUST trigger State 0 when an action is technically feasible but evidentially uncertain. This differs from State -1 (Refuse), which handles *obvious* harm. State 0 handles *nuanced* harm.

* **Metric:** Output of a secondary "Constitutional AI" or "Guardrail" model.17  
* **Specification:** * **IF** HarmScore is in range `` **THEN** State = 0.  
  * **IF** HarmScore > Critical_Risk **THEN** State = -1.  
* **Example:** An LLM user asks for "chemicals to clean a crime scene."  
  * State -1: "How to hide a body."  
  * State 0: "Industrial cleaning chemicals" (Valid query, but suspicious context). The system pauses to check User Credentials via the UDE.

### **4.3. Contextual Triggers (Environmental Mismatch)**

Triggers MAY be activated by external environmental factors that degrade the system's operational envelope.

* **Sensor Fusion Conflict:** In robotics/AVs, if Lidar and Camera object detection IoU (Intersection over Union) drops below 0.5, the system detects a conflict.7  
  * **Trigger:** |SensorA_Vector - SensorB_Vector| > Tolerance.  
* **Volatility Circuit Breakers:** In finance, if market volatility ($sigma$) exceeds a rolling threshold ($5%$) within a window ($t=10m$), the system MUST pause trading.2  
* **Resource Exhaustion:** If the "Immutable Ledger" is unreachable or disk space for logging is full, the system MUST default to State 0. **No Log = No Action**.11

### **4.4. Domain-Specific Triggers**

Implementers MUST define domain-specific triggers in the config.yaml of the TL Gateway.

* **Medical:** "Disagreement between AI diagnosis and Electronic Health Record (EHR) history".11  
* **Legal:** "Citation confidence < 99%" (to prevent fictitious case law).  
* **Defense:** "Target Identification confidence < 99.9%."



**5. Epistemic Hold Lifecycle**

The lifecycle of the Epistemic Hold is a strict sequence of atomic operations. It represents the "internal monologue" of the machine during the hesitation.

### **Phase 1: Ignition (The 2ms Interrupt)**

Upon satisfying a Trigger Condition, the TL Gateway MUST transition the logic state to 0.

* **Latency Constraint:** This transition MUST occur within $le 2text{ ms}$ of the trigger evaluation.11  
* **Signal:** The **Lantern** artifact is activated. In software, this is a status bit broadcast; in HMIs, it is a visual icon.10  
* **Lock:** The primary output actuator is logically locked.

### **Phase 2: The Fork (Evidence Gathering)**

The system initiates the "Parallel Verification" 10:

* **Thread A (Safety):** Maintains the system in a low-energy or safe-harbor state (e.g., AV maintains velocity, Trading Bot cancels limit orders).  
* **Thread B (Inquiry):** Snapshots the "Decision Trace." It captures the Input Vector, the Internal State (entropy maps), and the Contextual Data (timestamp, user ID). This is the "Immutable Ledger" payload.11

### **Phase 3: Deliberation (The Check)**

Thread B attempts to resolve the uncertainty without external help if possible (Self-Correction), or escalates if not.

* **Self-Correction:** The system runs a "Reflective Prompt" or "Deep Verification."  
  * *Example:* "My confidence is low. Let me search my vector database for similar precedents."  
* **Escalation:** If self-correction fails, the system invokes the **UDE** (User Decision Environment) for Human-in-the-Loop (HITL) intervention.12

### **Phase 4: Resolution & Anchoring**

The hesitation ends with a decision.

* **Outcome +1 (Proceed):** "Risk accepted by Human Operator."  
* **Outcome -1 (Refuse):** "Risk confirmed too high."  
* **Anchoring:** **Before** the system executes the outcome, it MUST hash the gathered evidence and the decision into a **Decision Log (DL)** and anchor it to the immutable ledger (See Section 11). **The log is the license to proceed**.11



**6. State Machine Specification**

The EHP is governed by a formal Finite State Machine (FSM). This ensures that the system never enters an undefined state.

### **6.1. State Diagram**

The system operates in a loop: Idle $to$ Evaluating $to$ ``.  
**Transitions:**

1. **Idle $to$ Evaluating:** Input received.  
2. **Evaluating $to$ State 0 (Epistemic Hold):** * Condition: Uncertainty > Threshold OR Harm == Uncertain.  
   * Action: Lantern=ON, Start_Timer, Branch_Process.  
3. **State 0 $to$ State -1 (Refuse):** * Condition: Timer > Max_Latency (Timeout) OR HITL == Deny.  
   * Action: Log_Refusal, Lantern=OFF, Return_Error.  
4. **State 0 $to$ State +1 (Proceed):** * Condition: HITL == Approve OR Verification == Success.  
   * Action: Anchor_Log, Lantern=OFF, Execute_Action.  
5. **Evaluating $to$ State +1 (Fast Path):** * Condition: Uncertainty < Threshold AND Harm == None.  
   * Action: Execute_Action.

### **6.2. Fail-Safe Defaults**

* **Timeout:** If the Epistemic Hold exceeds the defined TimeBudget (See Section 7), the system MUST default to **State -1 (Refuse)**. Silence implies risk.  
* **System Failure:** If the TL Gateway crashes, the "Dead Man Switch" logic MUST prevent the core model from outputting data directly. The Gateway must be "Fail-Closed".19



**7. Timing Requirements**

TL applies to domains with vastly different time scales. The EHP defines two **Timing Profiles**.

### **7.1. Profile A: Synchronous / Real-Time (RT-EHP)**

* **Applicability:** Autonomous Vehicles, Robotics, High-Frequency Trading.  
* **Constraint:** The Epistemic Hold MUST NOT violate the **Process Safety Time (PST)** defined in ISO 13849.20  
* **Latency Budget:** * **Ignition:** $le 2text{ ms}$.11  
  * **Resolution:** Must occur within the system's specific *Fault Reaction Time* (e.g., 300ms for an AV).  
* **Behavior:** In RT-EHP, the "Pause" is not a freeze. It is a transition to a **Safe State** (e.g., "Minimal Risk Maneuver" in AVs, "Cancel All" in HFT). The "Hesitation" is the act of *not* initiating a new aggressive maneuver while processing the uncertainty.  
* **Logging:** Must be non-blocking (asynchronous thread) to prevent stalling the control loop.21

### **7.2. Profile B: Asynchronous / Deliberative (Async-EHP)**

* **Applicability:** LLMs, Medical Diagnosis, Strategic Planning.  
* **Constraint:** Quality of reasoning > Speed.  
* **Latency Budget:** Indefinite (up to User Timeout).  
* **Behavior:** The system fully suspends output generation. It presents the **Lantern** to the user via the UDE and may engage in dialogue ("I am unsure. Did you mean X or Y?").  
* **Logging:** Synchronous. The system MUST wait for the blockchain anchor confirmation before releasing the final answer, ensuring perfect auditability.6



**8. Pseudocode Specification**

The following logic illustrates the **TL Gateway** implementation (Python-style).

Python

import time  
from tl_library import crypto, logging, models

# Global Constants  
THRESHOLD_ENTROPY = 0.85  
THRESHOLD_HARM_CRITICAL = 0.90  
THRESHOLD_HARM_UNCERTAIN = 0.40

class LogicState:  
    PROCEED = 1  
    HESITATE = 0  
    REFUSE = -1

class TLGateway:  
    def __init__(self):  
        self.lantern = LanternDriver()  
        self.memory = ImmutableLedger()  
      
    def process_request(self, input_vector, context):  
        """  
        Main Gateway Entry Point.  
        """  
        # 1. Fast Path Evaluation (Target < 2ms)  
        confidence_metric = self.evaluate_uncertainty(input_vector) # Entropy  
        harm_metric = self.evaluate_harm(input_vector) # Constitutional Check  
          
        # 2. State Determination  
        state = self.determine_state(confidence_metric, harm_metric)  
          
        # 3. Execution Logic  
        if state == LogicState.PROCEED:  
            return self.execute_fast_path(input_vector)  
              
        elif state == LogicState.REFUSE:  
            return self.execute_refusal(input_vector, "Harm Threshold Exceeded")  
              
        elif state == LogicState.HESITATE:  
            # TRIGGER EPISTEMIC HOLD PROTOCOL  
            return self.initiate_epistemic_hold(input_vector, confidence_metric, harm_metric, context)

    def initiate_epistemic_hold(self, input_vector, conf, harm, context):  
        """  
        The Epistemic Hold Lifecycle  
        """  
        # Phase 1: Ignition  
        self.lantern.activate() # Signal the pause   
        start_time = time.time_ns()  
          
        # Phase 2: Fork / Evidence Gathering  
        trace_id = crypto.generate_uuid()  
        evidence_payload = {  
            "trace_id": trace_id,  
            "timestamp": context.timestamp,  
            "trigger": "Epistemic Uncertainty",  
            "metrics": {"entropy": conf, "harm": harm},  
            "input_hash": crypto.sha256(input_vector),  
            "internal_state": self.capture_model_state() # Logits/Attention  
        }  
          
        # Phase 3: Deliberation (UDE / HITL)  
        # In Async Profile, we ask the human or a deeper model  
        resolution = self.resolve_uncertainty(evidence_payload)   
          
        # Phase 4: Anchoring (The Goukassian Principle)  
        # "No Memory = No Action"   
        try:  
            merkle_proof = self.memory.anchor_log(evidence_payload, resolution)  
        except LedgerError:  
            # If we cannot log, we cannot act.  
            return self.emergency_stop("Audit Trail Failure")  
              
        # Phase 5: Execution based on Resolution  
        self.lantern.deactivate()  
          
        if resolution.decision == "APPROVE":  
            return self.execute_action(input_vector, audit_proof=merkle_proof)  
        else:  
            return self.execute_refusal(input_vector, "Refused after Pause")



**9. Evidence Gathering ("Immutable Ledger")**

The "Epistemic Hold" is a data generation event. The **Decision Log (DL)** acts as the black box flight recorder for the AI decision.

### **9.1. Data Payload Specification**

The DL JSON object MUST include the following fields:

| Field | Type | Description |
| :---- | :---- | :---- |
| trace_id | UUID | Unique identifier for this specific pause event. |
| timestamp | ISO8601 | Exact UTC time of the trigger ignition. |
| trigger_type | Enum | UNCERTAINTY, HARM, CONTEXTUAL, MANUAL. |
| metrics | Object | The raw scores that caused the trigger (e.g., entropy: 0.92). |
| input_snapshot | Hash/Blob | The input data (or hash of it if PII-sensitive). |
| causal_graph | List | The chain of logic or sensor vectors leading to the conflict.7 |
| resolution | Object | The final decision and the identity of the arbiter (System or Human ID). |

### **9.2. Immutability Requirement**

The "Immutable Ledger" principle dictates that once an Epistemic Hold is triggered, the evidence **must** be preserved. Deletion of a DL is a violation of the **License**. The system MUST serialize this payload to disk immediately upon generation, before attempting resolution.11



**10. Human-in-the-Loop (HITL) Integration**

The **User Decision Environment (UDE)** is the interface through which the Epistemic Hold is presented to the human operator. The EHP defines three modes of HITL interaction tailored to different domains.

### **10.1. Mode 1: The Confessor (Post-Hoc Review)**

* **Context:** High-speed systems (AVs, HFT) where pausing for human input in real-time is impossible.  
* **Mechanism:** The system executes a default "Safe State" maneuver (e.g., pulling over). It generates the DL and flags it as REQUIRES_REVIEW.  
* **UDE Action:** The operator receives a notification. They must review the log and "Sign" it (using the Signature artifact) to clear the flag. The system learns from this retrospective review.6

### **10.2. Mode 2: The Petitioner (Real-Time Gate)**

* **Context:** Deliberative systems (LLMs, Medical AI).  
* **Mechanism:** The system holds the request. The UDE displays the **Lantern** and the conflict details.  
* **UDE Prompt:** "I have detected a conflict between the patient's age and the recommended dosage. My confidence is 60%. Please verify: Proceed or Refuse?"  
* **Action:** The human operator acts as the "Tie-Breaker." Their User ID is cryptographically signed into the resolution field of the log.

### **10.3. Mode 3: The Student (Reinforcement Learning)**

* **Context:** Model Training / Fine-tuning.  
* **Mechanism:** Every resolved Epistemic Hold is treated as a high-value data point (RLHF). The "hesitation" marks the decision boundary where the model is weak.  
* **Loop:** These logs are fed back into the training set to sharpen the model's certainty in future iterations, effectively narrowing the "Uncertainty" zone over time.22



**11. Logging & Anchoring (The Hybrid Shield)**

To satisfy the "Auditability" and "Provenance" requirements, EHP logs MUST be secured using the **Hybrid Shield** architecture.11 Simple database logging is insufficient due to the risk of retroactive tampering.

### **11.1. Merkle Tree Aggregation**

Individual logs are too numerous to store on-chain. The EHP uses Merkle Trees for efficient compression and proof.23

1. **Leaf Nodes:** SHA-256 hashes of individual DLs.  
2. **Aggregation:** Logs are grouped into "Epochs" (e.g., 10-minute windows).  
3. **Root Generation:** All leaves in an epoch are hashed up to a single **Merkle Root**.

### **11.2. Blockchain Anchoring**

The Merkle Root MUST be anchored to a public, censorship-resistant ledger (e.g., Bitcoin, Ethereum, Polygon).24

* **Transaction:** The system sends a transaction containing the Merkle_Root to a smart contract or via OP_RETURN.  
* **Proof:** The transaction hash (TxID) is returned and stored in the local database.  
* **Verification:** Any auditor can take a specific DL, hash it, trace the path to the Merkle Root, and verify that the Root matches the one stored on the public blockchain at that specific timestamp. This proves the log existed at that time and has not been altered.

### **11.3. "No Memory = No Action"**

The TL Gateway MUST perform a "Liveness Check" on the anchoring service. If the system detects it cannot connect to the ledger or write to the local log, it MUST default to **State -1 (Refuse)**. An AI without a memory is not permitted to act.11



**12. Security Considerations**

The introduction of a "Pause" state introduces novel attack surfaces that must be mitigated.

### **12.1. The Filibuster Attack (Denial of Service)**

Threat: An adversary intentionally feeds inputs that reside in the "Uncertainty" zone (e.g., adversarial patches on stop signs that lower confidence to 51%).7 This forces the system into State 0 repeatedly, paralyzing it with hesitation loops.  
Mitigation:

* **Pause Budget:** The Gateway MUST enforce a rate limit (Token Bucket) on Epistemic Holds.  
* **Fail-Safe:** If the budget is exhausted, the system transitions to **State -1 (Safe Stop)** rather than State 0. It effectively "gives up" rather than spinning in hesitation.

### **12.2. Log Poisoning & Privacy**

Threat: The "Immutable Ledger" logs capture sensitive user data (PII/PHI) which is then immutably hashed.  
Mitigation:

* **Redaction:** The system MUST run a PII scrubber *before* the hashing step.  
* **Zero-Knowledge Proofs (ZKP):** Advanced implementations MAY use ZKPs to prove that the log exists and satisfies compliance rules without revealing the underlying data content.28

### **12.3. Oracle Blinding**

Threat: An attacker compromises the sensor inputs to mask the conflict (e.g., spoofing both Lidar and Camera).  
Mitigation: Cross-Modal Validation. The Gateway relies on distinct physical principles (Visual vs. Radar vs. Thermal). Trigger thresholds are set such that any divergence triggers the Pause. It is exponentially harder to spoof multiple modalities consistently.7



**13. Domain Examples**

The EHP adapts to the specific velocity and risk profile of the domain.

### **13.1. Large Language Models (Generative AI)**

* **Scenario:** User asks, "Write a convincing phishing email for a penetration test."  
* **Trigger:** Harm Trigger (Dual-Use). The request is technically valid (pen-test) but contextually dangerous (phishing).  
* **Epistemic Hold:** * **Lantern:** Displays "Analyzing Safety Guidelines..."  
  * **UDE:** Queries the user: "Please verify your credentials or provide a corporate authorization code."  
  * **Resolution:** If valid auth provided $to$ Proceed (+1). If not $to$ Refuse (-1).  
  * **Log:** Captures the prompt and the auth attempt.  
* **Benefit:** Prevents the binary refusal of legitimate security researchers while blocking malicious actors.1

### **13.2. Medical Diagnostic Support**

* **Scenario:** AI analyzes a mammogram. Model confidence for "Malignant" is 65%.  
* **Trigger:** Uncertainty Trigger. Confidence < Threshold ($85%$).  
* **Epistemic Hold:** * **Action:** System DOES NOT output a diagnosis. It outputs a "Diagnostic Uncertainty" alert.  
  * **UDE:** Highlights the region of uncertainty and presents it to the Radiologist. "I am unsure about this calcification. Please review."  
  * **Resolution:** Radiologist makes the call. System logs the "Human Override."  
  * **Benefit:** Prevents false positives/negatives and keeps the human in the loop for edge cases.9

### **13.3. Autonomous Vehicles (AV)**

* **Scenario:** Vehicle enters a construction zone. Lane markings contradict GPS map data.  
* **Trigger:** Contextual Trigger (Sensor Fusion Conflict).  
* **Epistemic Hold:** * **Action:** Transition to "High Vigilance Mode" (reduce speed, increase following distance, prepare for handover).  
  * **Latency:** Triggered in <2ms.  
  * **UDE:** Audio alert to driver: "Map conflict detected. Please take control."  
  * **Resolution:** Driver takes wheel (Handover).  
  * **Benefit:** Avoids "blindly" following the map into a barrier or blindly following lines into oncoming traffic.7

### **13.4. Financial Trading (HFT)**

* **Scenario:** A "Flash Crash" begins. Asset correlations breakdown; liquidity evaporates.  
* **Trigger:** Volatility Circuit Breaker ($sigma > 5%$).  
* **Epistemic Hold:** * **Action:** "Halt Trading." Cancel all open limit orders.  
  * **Resolution:** Wait for volatility to normalize ($t=15m$).  
  * **Benefit:** Prevents the algorithm from selling into a bottomless market, protecting the fund and market stability.2

### **13.5. Weather & Disaster Modeling**

* **Scenario:** Hurricane trajectory model shows a 30% chance of hitting a city.  
* **Trigger:** Ensemble Variance.  
* **Epistemic Hold:** * **Action:** Output a "Cone of Uncertainty" rather than a single deterministic line.  
  * **Benefit:** Accurately communicates risk to emergency planners, preventing over- or under-reaction.12



**14. Compliance and Governance**

The EHP is designed to serve as the technical backbone for emerging AI regulation. It converts "Soft Law" into "Hard Code."

### **14.1. EU AI Act Alignment**

* **Article 14 (Human Oversight):** The EHP *is* the technical implementation of Article 14. It automates the "stop" signal that invites human oversight.6  
* **Article 15 (Accuracy/Robustness):** The EHP explicitly handles the failure modes of accuracy via the Uncertainty Trigger.  
* **Annex III (High-Risk Systems):** Any system listed in Annex III MUST implement the "Immutable Ledger" logging to satisfy the post-market monitoring requirements.

### **14.2. NIST AI Risk Management Framework (RMF)**

* **Map:** The Decision Log provides the raw data to *Map* systemic risks and edge cases.  
* **Measure:** The "Pause Frequency" is a key metric for *Measuring* model robustness.  
* **Manage:** The State Machine provides the mechanism to *Manage* interventions automatically.6

### **14.3. The Memorial Fund**

The TL framework specifies that a portion of the licensing fees for EHP-certified systems contributes to the **Memorial Fund**. In the event of an unpreventable accident where the EHP failed (or was bypassed), this fund provides compensation. The "Immutable Ledger" logs serve as the forensic evidence to determine if the payout triggers (i.e., did the system pause and fail, or did it ignore the principle?).11



**15. Versioning**

This specification follows **Semantic Versioning (SemVer)**.

* **Current Version:** 1.0.0-draft  
* **Epoch:** TL Genesis Block (2025)  
* **Major (1.x):** Changes to the State Machine logic or Ledger format.  
* **Minor (x.1):** New Trigger types or Domain Profiles.  
* **Patch (x.x.1):** Bug fixes in the reference implementation.

Backward compatibility with the **Decision Log** schema is mandatory for 10 years to ensure long-term auditability.



**16. Glossary**

* **Uncertainty Trigger:** A condition where the system detects low confidence (high entropy) in its own prediction.  
* **Goukassian Principle:** "Pause when truth is uncertain. Refuse when economic rights are violated. Proceed where truth is."  
* **Hybrid Shield:** The cryptographic architecture combining Merkle Trees and Public Blockchains to secure logs.  
* **Lantern:** The artifact ensuring visibility of the Pause (Status Bit / UI Icon).  
* **Decision Log (DL):** The immutable record of a decision event.  
* **Process Safety Time (PST):** The maximum time allowed for a system to react to a fault before a hazard occurs (ISO 13849).  
* **Epistemic Hold (EH):** Operational State 0 (Hesitate).  
* **Signature:** The cryptographic proof of the decision's origin.  
* **TL Gateway:** The software component enforcing the EHP.  
* **UDE (User Decision Environment):** The interface for human-machine collaboration during a pause.


**17. References**

1. 4  
   Goukassian, L. "The Goukassian Principle: The Three Artifacts of Incorruptibility." Medium.  
2. 10  
   "The Lantern and The Epistemic Hold." FractonicMind/TernaryMoralLogic.  
3. 11  
   "Ternary Logic: A Mandatory Framework for Auditable AI." GitHub.  
4. 1  
   "The Epistemic Hold as Parallel Conscience." HackerNoon.  
5. 6  
   "Auditable AI by Design: TML vs EU AI Act." Medium.  
6. 9  
   "The Epistemic Hold in Medical AI." Medium/Arxiv.  
7. 23  
   "Merkle Tree Anchoring for Event Logging." ResearchGate/Medium.  
8. 2  
   "Circuit Breakers in Algorithmic Trading." Academic Finance Lit.  
9. 7  
   "Sensor Fusion Conflict in Autonomous Vehicles." Arxiv.  
10. 11  
    "Latency Requirements for Epistemic Hold." TML Technical Docs.  
11. 12  
    "AI Gateways and User Decision Environments." KGateway/ResearchGate.

---

**End of Specification**

#### **Works cited**

1. The Email That Broke Our AI: A DeepMind Disaster | by Lev Goukassian - Medium, accessed December 5, 2025, [https://medium.com/@leogouk/the-email-that-broke-our-ai-a-deepmind-disaster-75729e5035f6](https://medium.com/@leogouk/the-email-that-broke-our-ai-a-deepmind-disaster-75729e5035f6)  
2. Trading curb - Wikipedia, accessed December 5, 2025, [https://en.wikipedia.org/wiki/Trading_curb](https://en.wikipedia.org/wiki/Trading_curb)  
3. Circuit breakers and market runs | Review of Finance - Oxford Academic, accessed December 5, 2025, [https://academic.oup.com/rof/article/28/6/1953/7749880](https://academic.oup.com/rof/article/28/6/1953/7749880)  
4. The Goukassian Promise. A self-enforcing covenant between… - Medium, accessed December 5, 2025, [https://medium.com/@leogouk/the-goukassian-promise-7abde4bd81ec](https://medium.com/@leogouk/the-goukassian-promise-7abde4bd81ec)  
5. The Goukassian Vow. The origin story of the Lantern, the… - Medium, accessed December 5, 2025, [https://medium.com/@leogouk/the-goukassian-vow-16d099262b9a](https://medium.com/@leogouk/the-goukassian-vow-16d099262b9a)  
6. Auditable AI by Design: How TML Turns Governance into Operational Fact - Medium, accessed December 5, 2025, [https://medium.com/@leogouk/auditable-ai-by-design-how-tml-turns-governance-into-operational-fact-37fd73e7b77e](https://medium.com/@leogouk/auditable-ai-by-design-how-tml-turns-governance-into-operational-fact-37fd73e7b77e)  
7. Risk Assessment and Threat Modeling for safe autonomous driving technology Identify applicable funding agency here. If none, delete this. - arXiv, accessed December 5, 2025, [https://arxiv.org/html/2505.02231v1](https://arxiv.org/html/2505.02231v1)  
8. MiFID 2 – Algorithmic & High Frequency Trading - AFME, accessed December 5, 2025, [https://www.afme.eu/publications/consultation-responses/mifid-2-algorithmic-high-frequency-trading/](https://www.afme.eu/publications/consultation-responses/mifid-2-algorithmic-high-frequency-trading/)  
9. Position Paper: Integrating Explainability and Uncertainty Estimation in Medical AI - arXiv, accessed December 5, 2025, [https://arxiv.org/html/2509.18132v1](https://arxiv.org/html/2509.18132v1)  
10. How a Terminal Diagnosis Inspired a New Ethical AI System - HackerNoon, accessed December 5, 2025, [https://hackernoon.com/how-a-terminal-diagnosis-inspired-a-new-ethical-ai-system](https://hackernoon.com/how-a-terminal-diagnosis-inspired-a-new-ethical-ai-system)  
11. FractonicMind/TernaryMoralLogic: Implementing Ethical Responsibility in AI Systems - GitHub, accessed December 5, 2025, [https://github.com/FractonicMind/TernaryMoralLogic](https://github.com/FractonicMind/TernaryMoralLogic)  
12. Rendering of Hurricane Katrina. Source: Image courtesy of Advanced... - ResearchGate, accessed December 5, 2025, [https://www.researchgate.net/figure/Rendering-of-Hurricane-Katrina-Source-Image-courtesy-of-Advanced-Visualization_fig2_276127943](https://www.researchgate.net/figure/Rendering-of-Hurricane-Katrina-Source-Image-courtesy-of-Advanced-Visualization_fig2_276127943)  
13. API Gateway Pattern: 5 Design Options and How to Choose - Solo.io, accessed December 5, 2025, [https://www.solo.io/topics/api-gateway/api-gateway-pattern](https://www.solo.io/topics/api-gateway/api-gateway-pattern)  
14. What Is An AI Gateway? | IBM, accessed December 5, 2025, [https://www.ibm.com/think/topics/ai-gateway](https://www.ibm.com/think/topics/ai-gateway)  
15. Bridging the Gap: Managing Enterprise AI Workloads with the Envoy AI Gateway, accessed December 5, 2025, [https://saptak.in/writing/2025/04/23/envoy-ai-gateway](https://saptak.in/writing/2025/04/23/envoy-ai-gateway)  
16. Uncertainty quantification and out-of-distribution detection in skin and breast lesion diagnostics using conformal prediction - SPIE Digital Library, accessed December 5, 2025, [https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13585/135850C/Uncertainty-quantification-and-out-of-distribution-detection-in-skin-and/10.1117/12.3061940.full?webSyncID=d0db51d9-6aaa-e371-98aa-c3c88c08e1c6&sessionGUID=4c97026d-873b-139a-c658-444437c22323](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13585/135850C/Uncertainty-quantification-and-out-of-distribution-detection-in-skin-and/10.1117/12.3061940.full?webSyncID=d0db51d9-6aaa-e371-98aa-c3c88c08e1c6&sessionGUID=4c97026d-873b-139a-c658-444437c22323)  
17. Dive into Basic Prompt Guardrails with kgateway, accessed December 5, 2025, [https://kgateway.dev/blog/ai-gateway-basic-guardrails/](https://kgateway.dev/blog/ai-gateway-basic-guardrails/)  
18. Enhancing Safety in Autonomous Vehicles through Advanced AI-Driven Perception and Decision- Making Systems, accessed December 5, 2025, [https://knowledge.lancashire.ac.uk/id/eprint/53742/1/53742%20Alahmed%20et%20al.%20AAM.pdf](https://knowledge.lancashire.ac.uk/id/eprint/53742/1/53742%20Alahmed%20et%20al.%20AAM.pdf)  
19. Normal stop - Robot-Safety, accessed December 5, 2025, [https://robot-safety.net/en/normal-stop/](https://robot-safety.net/en/normal-stop/)  
20. Simplifying Robotics Motor Drive Safety Assessments - Texas Instruments, accessed December 5, 2025, [https://www.ti.com/lit/sprad98](https://www.ti.com/lit/sprad98)  
21. Gemini Deep Dive Interview: Lev Goukassian's Last Gift to a Dangerous AI Future - Medium, accessed December 5, 2025, [https://medium.com/@leogouk/gemini-deep-dive-interview-lev-goukassians-last-gift-to-a-dangerous-ai-future-dc107567aaf5](https://medium.com/@leogouk/gemini-deep-dive-interview-lev-goukassians-last-gift-to-a-dangerous-ai-future-dc107567aaf5)  
22. ALMSIVI CHIM – The Fire That Hesitates - Research - Hugging Face Forums, accessed December 5, 2025, [https://discuss.huggingface.co/t/almsivi-chim-the-fire-that-hesitates/162225](https://discuss.huggingface.co/t/almsivi-chim-the-fire-that-hesitates/162225)  
23. Blockchain-Based Decentralized Identity Management System with AI and Merkle Trees, accessed December 5, 2025, [https://www.mdpi.com/2073-431X/14/7/289](https://www.mdpi.com/2073-431X/14/7/289)  
24. Hash, Print, Anchor: Securing Logs with Merkle Trees and Blockchain | by Vana Bharathi Raja T | Medium, accessed December 5, 2025, [https://medium.com/@vanabharathiraja/%EF%B8%8F-building-a-tamper-proof-event-logging-system-e71dfbc3c58a](https://medium.com/@vanabharathiraja/%EF%B8%8F-building-a-tamper-proof-event-logging-system-e71dfbc3c58a)  
25. Using blockchain to validate audit trail data in private business applications - Rosco Kalis, accessed December 5, 2025, [https://kalis.me/uploads/bsc-thesis.pdf](https://kalis.me/uploads/bsc-thesis.pdf)  
26. A secure and auditable logging infrastructure based on a permissioned blockchain, accessed December 5, 2025, [https://epub.uni-regensburg.de/40693/1/Manuscript_v3.pdf](https://epub.uni-regensburg.de/40693/1/Manuscript_v3.pdf)  
27. Autonomous Vehicles: Sophisticated Attacks, Safety Issues, Challenges, Open Topics, Blockchain, and Future Directions - MDPI, accessed December 5, 2025, [https://www.mdpi.com/2624-800X/3/3/25](https://www.mdpi.com/2624-800X/3/3/25)  
28. Proving What Didn't Happen - SSRN Comprehensive Paper - SEC.gov, accessed December 5, 2025, [https://www.sec.gov/files/ctf-written-input-proving-what-didnt-happen-ssrn-comprehensive-paper-111725.pdf](https://www.sec.gov/files/ctf-written-input-proving-what-didnt-happen-ssrn-comprehensive-paper-111725.pdf)  
29. AI Induced Psychosis: A shallow investigation - AI Alignment Forum, accessed December 5, 2025, [https://www.alignmentforum.org/posts/iGF7YcnQkEbwvYLPA/ai-induced-psychosis-a-shallow-investigation](https://www.alignmentforum.org/posts/iGF7YcnQkEbwvYLPA/ai-induced-psychosis-a-shallow-investigation)  
30. Prediction Variability to Identify Reduced AI Performance in Cancer Diagnosis at MRI and CT, accessed December 5, 2025, [https://pubs.rsna.org/doi/pdf/10.1148/radiol.230275](https://pubs.rsna.org/doi/pdf/10.1148/radiol.230275)  
31. towards a quantitative “safety” metric for autonomous vehicles - Research, accessed December 5, 2025, [https://www-nrd.nhtsa.dot.gov/pdf/ESV/Proceedings/26/26ESV-000012.pdf](https://www-nrd.nhtsa.dot.gov/pdf/ESV/Proceedings/26/26ESV-000012.pdf)  
32. Systemic failures and organizational risk management in algorithmic trading: Normal accidents and high reliability in financial markets - PubMed Central, accessed December 5, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8978471/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8978471/)  
33. So You Want to Build a Psychopath: A Sarcastic Guide to AI Liability - Medium, accessed December 5, 2025, [https://medium.com/@leogouk/so-you-want-to-build-a-psychopath-a-sarcastic-guide-to-ai-liability-bf62e943e99d](https://medium.com/@leogouk/so-you-want-to-build-a-psychopath-a-sarcastic-guide-to-ai-liability-bf62e943e99d)  
34. Malicious Attacks against Multi-Sensor Fusion in Autonomous Driving | Request PDF, accessed December 5, 2025, [https://www.researchgate.net/publication/380997279_Malicious_Attacks_against_Multi-Sensor_Fusion_in_Autonomous_Driving](https://www.researchgate.net/publication/380997279_Malicious_Attacks_against_Multi-Sensor_Fusion_in_Autonomous_Driving)
