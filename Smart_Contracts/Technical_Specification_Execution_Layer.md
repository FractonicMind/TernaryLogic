\# Specification: The Ternary Logic (TL) Smart Contract Execution Layer

\#\# 1\. Core Architectural Principles

The Ternary Logic (TL) framework is an operational governance and economic system designed to enforce accountability and transparency through a set of core architectural principles. These principles are instantiated in smart contracts to create a robust and verifiable system for managing value and state transitions. The framework is built upon three operational states, eight architectural pillars, a governance trinity, and four hard constraints, collectively forming a comprehensive system that moves from trust-based promises to cryptographic verification. This section provides a detailed specification of these foundational components, treating TL strictly as a technical and economic protocol rather than a moral philosophy. The design prioritizes value management and state enforcement, ensuring that every action is recorded, auditable, and governed by a clear set of rules. The system's architecture is intended to be platform-agnostic, with a primary focus on Ethereum and its ecosystem, but with considerations for adaptation to other blockchain platforms like Bitcoin and Polygon. The ultimate goal is to create a "constitutional code" where the rules of economic interaction are embedded in immutable and transparent smart contracts, making them harder to break than traditional legal agreements.

\#\#\# 1.1. The Three Operational States

The Ternary Logic system is fundamentally defined by three distinct operational states that govern the flow of assets and the finality of transactions. These states—\*\*Proceed\*\*, \*\*Epistemic Hold\*\*, and \*\*Refuse\*\*—provide a more nuanced and secure model for transaction processing compared to the binary success/failure outcomes of traditional smart contracts. Each state has a clear financial definition and is instantiated in the smart contract's ledger, providing a transparent and auditable record of all economic activities. The introduction of the \*\*"Epistemic Hold"\*\* state is a key innovation, creating a deliberate pause in execution to allow for verification and dispute resolution, thereby mitigating risks associated with uncertainty and incomplete information. This ternary model ensures that the system does not default to a potentially harmful "fail-open" or "fail-closed" state in the face of ambiguity, but instead enters a controlled, escrow-like state pending further input. The following subsections detail the specific mechanics and financial implications of each of these three core states.

\#\#\#\# 1.1.1. State (+1): Proceed

The \*\*"Proceed"\*\* state, represented numerically as \*\*(+1)\*\* , signifies the successful and final confirmation of a transaction. When a transaction enters this state, it indicates that all predefined conditions have been met, all necessary verifications have been completed, and the system has reached a state of cryptographic certainty. In financial terms, this state corresponds to the finalization of an asset transfer. For a token transfer, this means the credit and debit entries are confirmed and updated on the ledger. For a more complex operation, such as the execution of a governance proposal or the settlement of a financial derivative, the "Proceed" state indicates that the outcome has been enacted and is irreversible. The transition to this state is typically triggered by a definitive input from an authorized oracle, a successful vote by a governance body, or the fulfillment of a set of programmatic conditions. The "Proceed" state is the desired end-state for most legitimate transactions, representing the successful completion of the intended economic action. The system's design ensures that reaching this state requires clear, verifiable evidence, preventing premature finalization and protecting the integrity of the ledger.

\#\#\#\# 1.1.2. State (0): Epistemic Hold

The \*\*"Epistemic Hold"\*\* state, represented as \*\*(0)\*\* , is a cornerstone of the Ternary Logic framework, designed to address uncertainty and ambiguity in a systematic and secure manner. This state functions as a computational pause or an escrow mechanism, where a transaction is suspended and any associated assets are locked, pending the resolution of an epistemic issue. An issue may arise from various sources, such as conflicting data from oracles, a detected anomaly in a supply chain, a dispute raised by a stakeholder, or the simple lack of sufficient information to make a definitive decision. When the system encounters such a situation, it does not default to a binary "success" or "failure" but instead transitions to the "Epistemic Hold" state. This state requires additional inputs, such as an audit report, a manual review by a governance body (like the Stewardship Custodians), or a new data feed from a trusted oracle, to resolve the uncertainty and determine the next course of action. The mechanics of this state can involve a time-lock, a voting period, or a direct oracle request, depending on the specific implementation and the nature of the transaction. By design, the "Epistemic Hold" state embodies the Goukassian Principle of defaulting to a secure, non-committal state in the face of ambiguity, preventing the system from making potentially harmful decisions based on incomplete or unreliable information .

\#\#\#\# 1.1.3. State (-1): Refuse

The \*\*"Refuse"\*\* state, represented as \*\*(-1)\*\* , is the definitive rejection of a transaction. This state is reached when the conditions for proceeding are not met, a dispute is resolved against the transaction's initiator, or a critical failure occurs that prevents the transaction from being completed safely. In financial terms, the "Refuse" state results in the reversion of the transaction, with any assets that were to be transferred being returned to their original owners. Depending on the system's design and the reason for refusal, gas fees or other penalties may be applied to the party responsible for the failed transaction, providing a disincentive for spam or malicious activity. The transition to the "Refuse" state can be triggered by a variety of events, such as a "REJECTED" action from a governance vote, a "TIMEOUT" in the "Epistemic Hold" state without a resolution, or the detection of a violation of the system's mandates (e.g., an attempt to execute a forbidden function call). The "Refuse" state provides a clear and final negative outcome, ensuring that the ledger remains clean of incomplete or invalid transactions. It is a critical component of the system's security model, providing a mechanism to halt and reverse actions that are deemed invalid, unsafe, or non-compliant with the established rules.

\#\#\# 1.2. The Eight Architectural Pillars

The Ternary Logic framework is constructed upon eight foundational pillars that collectively define its technical implementation and operational characteristics. These pillars are not merely abstract principles but are intended to be implemented as concrete logic within the smart contract code, providing a robust and verifiable architecture for governance and economic management. Each pillar addresses a specific aspect of the system's design, from handling uncertainty and ensuring immutability to promoting transparency and enabling secure governance. The pillars work in concert to create a system that is resilient, auditable, and resistant to both technical failures and malicious manipulation. The following subsections provide a detailed explanation of the Solidity or Chaincode implementation for each of the eight pillars, translating the high-level architectural concepts into specific technical requirements and design patterns. This detailed specification is crucial for developers seeking to build compliant and secure TL-based applications.

\#\#\#\# 1.2.1. Pillar 1: Epistemic Hold

The \*\*"Epistemic Hold"\*\* pillar is the technical implementation of the system's ability to pause execution in the face of uncertainty. This is not an administrative \`pause()\` function controlled by a central authority, but rather a logic gate that is automatically triggered by specific, predefined conditions related to data quality, risk, or ambiguity. The implementation involves a systematic evaluation process that quantifies uncertainty and assesses the complexity of a given decision . For example, a smart contract managing a supply chain might enter an "Epistemic Hold" if an IoT sensor reports a temperature deviation for a shipment of perishable goods. The contract would then lock the payment for that shipment and await further input, such as a signed report from a third-party inspector or a consensus from a network of oracles. The logic for this pillar would be implemented as a set of conditional checks within the contract's functions. If the input data falls outside of acceptable parameters or if there is a conflict between different data sources, the contract's state machine would be triggered to transition to the "Epistemic Hold" state. This ensures that the system does not proceed with a transaction based on potentially flawed or incomplete information, thereby mitigating risk and enforcing a higher standard of verification.

\#\#\#\# 1.2.2. Pillar 2: Immutable Ledger

The \*\*"Immutable Ledger"\*\* pillar ensures that the history of all decisions and state changes is permanently and transparently recorded. This is achieved through a carefully designed \`Log\` event structure within the smart contract. Every significant action, particularly state transitions between (+1), (0), and (-1), must be accompanied by a corresponding event emission. These events are not just simple notifications; they are structured data records that capture the context of the decision, including the timestamp, the parties involved, the input data that triggered the change, and the resulting state. For example, a \`Decision\` event might be defined with parameters such as \`decisionId\`, \`previousState\`, \`newState\`, \`initiator\`, \`justificationHash\`, and \`timestamp\`. This creates a detailed and cryptographically secured audit trail that is readable by anyone but cannot be altered or deleted. The immutability of the blockchain ensures that this ledger of events is tamper-proof, providing a permanent record for regulatory compliance, forensic analysis, and public accountability. The design of these events is critical, as they serve as the primary source of truth for the entire system's history .

\#\#\#\# 1.2.3. Pillar 3: Goukassian Principle

The \*\*"Goukassian Principle"\*\* is a core safety mechanism that dictates the system's behavior in the presence of ambiguity or uncertainty. It is a logic gate that defaults to the \*\*"Hold" (0) state\*\* rather than allowing the system to "Fail Open" (proceed with a potentially risky transaction) or "Fail Closed" (revert without a clear reason). This principle is a direct implementation of the "Sacred Zero" concept, which prioritizes caution and verification over speed or automation . In Solidity, this would be implemented as a default case in conditional logic or a \`require\` statement that checks for the completeness and validity of input data. For example, if a function expects a price feed from an oracle but receives a stale or outlier value, instead of reverting the transaction (which could be exploited) or proceeding with the bad data (which could cause financial loss), the function would trigger a transition to the "Epistemic Hold" state. This ensures that the system remains in a safe, non-committal state until the ambiguity can be resolved through a defined process, such as a governance vote or a manual audit. This principle is fundamental to the system's resilience, as it prevents it from being forced into an incorrect state by unexpected or malicious inputs.

\#\#\#\# 1.2.4. Pillar 4: Decision Logs

The \*\*"Decision Logs"\*\* pillar mandates that every state change within the system must be accompanied by a corresponding log entry. This is a strict requirement that ensures complete transparency and traceability of all actions. The implementation involves the use of Solidity's \`emit\` keyword to trigger a \`Decision(...)\` event for every transition between the (+1), (0), and (-1) states. This event serves as a formal record of the decision, capturing not just the outcome but also the context and justification. The structure of the \`Decision\` event is critical and should be designed to include all relevant information, such as the unique identifier for the decision, the addresses of the parties involved, the previous and new states, a hash of the justification or evidence that supported the decision, and a timestamp. This creates a rich, queryable history of all decisions, which can be used for auditing, dispute resolution, and analysis. The \*\*"No Log \= No Action"\*\* mandate (discussed later) enforces this pillar by reverting any transaction that fails to emit the required log, making it a non-negotiable part of the system's operation.

\#\#\#\# 1.2.5. Pillar 5: Economic Rights & Transparency

The \*\*"Economic Rights & Transparency"\*\* pillar is implemented through a set of public \`view\` functions that provide unrestricted access to the smart contract's state and financial data. This ensures that all stakeholders can independently verify the system's operations and audit the flow of assets. For a treasury contract, this would include functions to view the total balance, the allocation of funds to different categories, the history of withdrawals, and the current spending limits. For a governance contract, it would include functions to view the status of proposals, the results of votes, and the membership of the governing bodies. These functions do not modify the state of the contract and can be called without incurring gas costs, making them accessible to anyone with a blockchain connection. This transparency is a key feature of the TL framework, as it allows for public oversight and helps to build trust in the system. It also serves as a deterrent to corruption and mismanagement, as all actions are visible and can be scrutinized by the community.

\#\#\#\# 1.2.6. Pillar 6: Sustainable Capital Allocation

The \*\*"Sustainable Capital Allocation"\*\* pillar is designed to prevent the drainage of a treasury or the depletion of a shared resource. This is achieved through smart contract constraints that limit the rate and amount of withdrawals. For example, a treasury contract might be programmed to only allow a certain percentage of its total funds to be withdrawn within a specific time period (e.g., a month or a year). These limits could be hard-coded into the contract or, for more flexibility, be subject to change through a governance process. The implementation would involve state variables to track the total allocated funds, the amount withdrawn in the current period, and the time of the last withdrawal. A \`withdraw\` function would then include logic to check these variables and ensure that any new withdrawal does not exceed the predefined limits. This prevents a single actor or a small group from draining the treasury, ensuring the long-term financial sustainability of the project or organization. This pillar is particularly important for DAOs and other decentralized organizations that manage a shared pool of capital.

\#\#\#\# 1.2.7. Pillar 7: Hybrid Shield

The \*\*"Hybrid Shield"\*\* pillar provides a multi-layered defense against corruption and unauthorized control. It combines cryptographic security with institutional oversight, typically through the use of multi-signature (multi-sig) wallets or a Decentralized Autonomous Organization (DAO) interface for the \*\*"Stewardship Custodians."\*\* The Stewardship Custodians are a group of trusted individuals or entities responsible for overseeing the system, resolving disputes, and ensuring compliance with the established principles . The multi-sig requirement ensures that no single custodian can unilaterally make critical decisions, such as draining a treasury or changing the system's rules. Instead, a predefined number of signatures from the group (e.g., 6 out of 11\) are required to authorize a transaction. This distributes power and reduces the risk of a single point of failure or a malicious insider. The "Hybrid" nature of the shield refers to the combination of this technical mechanism (multi-sig) with the legal and ethical responsibilities of the custodians, creating a robust system of checks and balances.

\#\#\#\# 1.2.8. Pillar 8: Anchors

The \*\*"Anchors"\*\* pillar is the mechanism by which the TL system connects its on-chain decisions to real-world events and data. This is crucial for applications that rely on external information, such as supply chain management, insurance, or financial derivatives. Anchors are implemented using \`block.timestamp\` to record the time of a decision on-chain, or by using cryptographic hashes of external data to prove its existence and integrity. For example, a supply chain contract might anchor a shipment by recording the cryptographic hash of the bill of lading on the blockchain. This creates a tamper-proof record of the document's state at a specific point in time, which can be used to verify the shipment's authenticity and track its progress. Similarly, an oracle can provide a data feed (e.g., the price of a commodity) along with a cryptographic proof of its origin, which the smart contract can verify before using the data in its logic. These anchors provide a \*\*"proof of reality,"\*\* ensuring that the system's on-chain state accurately reflects the off-chain world .

\#\#\# 1.3. The Governance Trinity

The governance of the Ternary Logic system is structured around a \*\*"Governance Trinity,"\*\* a tripartite model designed to distribute power and prevent any single entity from gaining unilateral control. This model consists of three distinct bodies: the Technical Council, the Stewardship Custodians, and the Smart Contract Treasury. Each body has a specific set of responsibilities and permissions, and their interactions are governed by a set of transparent rules encoded in the smart contracts. This separation of powers is a core tenet of the TL framework, ensuring that the system remains decentralized, resilient, and aligned with its intended purpose. The following subsections define the specific permission sets and roles for each of the three governance bodies, outlining how they work together to maintain and evolve the system.

\#\#\#\# 1.3.1. Technical Council

The \*\*Technical Council\*\* is responsible for the technical maintenance and evolution of the TL framework. Its primary role is to preserve and update the core specifications, cryptographic standards, and protocol-level improvements . The council is typically composed of a small group of technical experts (e.g., 9 members) who are elected or appointed based on their expertise and contributions to the project. Their powers are strictly limited to technical matters; they do not have the authority to change the fundamental principles of the system or to make decisions on ethical or legal issues. Key responsibilities of the Technical Council include proposing and implementing code upgrades, commissioning external security audits, and ensuring the interoperability of the system with other platforms. To prevent unilateral changes, any upgrades or modifications proposed by the council are typically subject to a \*\*time-lock\*\*, which introduces a delay before the changes can be activated. This delay allows other stakeholders, such as the Stewardship Custodians, to review the proposals and intervene if necessary.

\#\#\#\# 1.3.2. Stewardship Custodians

The \*\*Stewardship Custodians\*\* are the ethical and legal guardians of the Ternary Logic framework. Their primary role is to ensure that the system is not captured, misused, or bent toward secrecy or harm . They are responsible for enforcing the "No Spy" and "No Weapon" mandates, certifying compliant operators, and arbitrating disputes that may arise, particularly those related to transactions in the "Epistemic Hold" state. The Custodians are typically a larger and more diverse group than the Technical Council (e.g., 11 members), representing a wider range of stakeholders and perspectives. Their decisions are often implemented through a multi-signature wallet, requiring a supermajority (e.g., 9 out of 11 votes) to authorize an action. This ensures that their power is not concentrated in the hands of a few and that their decisions reflect a broad consensus. The Custodians play a critical role in maintaining the integrity and trustworthiness of the system, providing a human layer of oversight to complement the automated logic of the smart contracts.

\#\#\#\# 1.3.3. Smart Contract Treasury

The \*\*Smart Contract Treasury\*\* is the autonomous financial backbone of the Ternary Logic system. It is a smart contract that holds the funds for the project and is responsible for their allocation and disbursement. The Treasury is designed to be incorruptible and transparent, with its rules and operations encoded directly in the smart contract logic. It receives funds from various sources, such as ecosystem revenue, endowments, or transaction fees, and releases them only when specific, predefined conditions are met. For example, a withdrawal from the Treasury might require a proposal from the Technical Council, ratification by the Stewardship Custodians, and a successful vote by the community. The Treasury's logic is designed to ensure the perpetual financial continuity of the project, preventing the misallocation or depletion of funds. It is a key component of the system's sustainability, providing the resources needed for ongoing maintenance, development, and governance.

\#\#\# 1.4. The Four Mandates (Hard Constraints)

The Ternary Logic framework is governed by four hard constraints, or \*\*"Mandates,"\*\* that are designed to protect the system and its users from specific types of harm. These mandates are not merely guidelines but are enforced at the smart contract level, making them an integral part of the system's architecture. They are intended to prevent the system from being used for malicious purposes, to protect the privacy of its users, and to ensure its long-term stability and resilience. The following subsections detail each of the four mandates and explain how they are implemented in the smart contract code.

\#\#\#\# 1.4.1. Mandate 1: No Spy

The \*\*"No Spy"\*\* mandate is a commitment to user privacy and data protection. It prohibits the system from engaging in any form of backdoor data collection or surveillance. This is particularly important in applications where sensitive information is involved, such as personal identity, financial transactions, or proprietary business data. The implementation of this mandate can involve the use of \*\*Zero-Knowledge (ZK) proofs\*\*, which allow a user to prove that they possess certain information without revealing the information itself. For example, a user could prove that they are over 18 years old without revealing their actual date of birth. The "No Spy" mandate also requires that all data collection is transparent and consensual, with clear policies on what data is collected, how it is used, and who has access to it. This mandate is a key differentiator for the TL framework, as it provides a strong guarantee of privacy and helps to build trust with users.

\#\#\#\# 1.4.2. Mandate 2: No Weapon

The \*\*"No Weapon"\*\* mandate prohibits the use of the Ternary Logic framework for any purpose that is designed to cause harm to individuals or society. This includes the development or deployment of autonomous weapons systems, the facilitation of illegal activities, or the creation of systems that are designed to manipulate or exploit users. The implementation of this mandate involves the creation of an \*\*exclusion list of forbidden function calls\*\* and a set of ethical guidelines that all developers and users must adhere to. The Stewardship Custodians are responsible for enforcing this mandate, with the power to revoke the certification of any operator who violates the rules. This mandate is a critical safeguard, ensuring that the powerful capabilities of the TL framework are used for beneficial purposes and not for malicious ends.

\#\#\#\# 1.4.3. Mandate 3: No Log \= No Action

The \*\*"No Log \= No Action"\*\* mandate is a core principle of the Ternary Logic framework, ensuring that every action is recorded and auditable. It states that any transaction that fails to emit a required log entry will be automatically reverted. This is implemented through a modifier in the Solidity code that wraps all state-changing functions. This modifier would check to ensure that the function has successfully emitted the required event (e.g., a \`Decision\` event) before allowing the transaction to be finalized. If the event is not emitted, the modifier will trigger a \`revert\`, causing the transaction to fail and any state changes to be rolled back. This mandate is a powerful tool for ensuring transparency and accountability, as it makes it impossible for any action to be taken without a corresponding record being created. It is a key component of the "Immutable Ledger" pillar and is essential for the system's auditability and trustworthiness.

\#\#\#\# 1.4.4. Mandate 4: No Switch Off

The \*\*"No Switch Off"\*\* mandate is a commitment to the long-term resilience and decentralization of the Ternary Logic system. It prohibits the inclusion of any mechanism that would allow a single administrator or a small group of administrators to unilaterally terminate or "kill" the smart contract. This is implemented by the \*\*absence of a \`selfdestruct\` function\*\* or any other administrative function that could disable the contract. The system's governance is designed to be distributed among the three bodies of the Governance Trinity, with no single entity having the power to shut down the system. This mandate ensures that the system is resistant to censorship and external pressure, and that it will continue to operate as long as there is a community of users who support it. It is a key feature of the system's design, providing a strong guarantee of its long-term viability and independence.

\#\# 2\. Smart Contract as Enforcement Layer

\#\#\# 2.1. Role of the Smart Contract: The Executioner

In the Ternary Logic (TL) framework, the smart contract serves as the \*\*"Executioner,"\*\* a term that precisely defines its function within the broader system architecture. It is not an intelligent agent capable of independent thought or decision-making; rather, it is a deterministic and transparent mechanism for enforcing the rules and logic of the TL system. The contract's primary role is to receive a signed input from an external source—be it an Oracle, an AI, or a human—and to execute the corresponding state transition logic (+1, 0, or \-1) based on that input. This clear separation of concerns is fundamental to the TL design, as it ensures that the on-chain enforcement layer remains impartial, predictable, and verifiable. The contract's logic is immutable and publicly auditable, meaning that anyone can inspect the code to understand how it will behave in any given situation. This transparency is a key feature of the TL framework, as it provides a high degree of certainty and trust in the system's operation.

\#\#\#\# 2.1.1. Distinction from the Decision Layer

![][image1]

A critical aspect of the TL architecture is the clear distinction between the \*\*Decision Layer\*\* and the \*\*Enforcement Layer\*\*. The Decision Layer is responsible for gathering and analyzing data, evaluating risks, and ultimately making the decision to proceed, hold, or refuse a transaction. This layer can be composed of a variety of components, including off-chain AI models, human experts, or decentralized oracle networks. The Decision Layer is where the "intelligence" of the system resides, as it is responsible for interpreting the complex and often ambiguous data of the real world. The Enforcement Layer, on the other hand, is the on-chain smart contract that is responsible for executing the decision made by the Decision Layer. The contract does not question the validity of the input it receives; it simply executes the corresponding state transition logic. This separation of concerns is crucial for maintaining the security and integrity of the system, as it prevents the on-chain logic from being manipulated or corrupted by external factors.

\#\#\#\# 2.1.2. Handling Signed Inputs from Oracles, AI, or Humans

The TL smart contract is designed to accept signed inputs from a variety of sources, including Oracles, AI models, and human users. The signature on the input serves as a cryptographic proof of its authenticity, ensuring that it has not been tampered with in transit. The contract verifies the signature before executing any state transition, providing a high degree of security and trust in the system. The ability to accept inputs from a variety of sources is a key feature of the TL framework, as it allows the system to be flexible and adaptable to a wide range of use cases. For example, in a DeFi application, the input might come from a decentralized oracle network that is providing real-time price data. In a supply chain application, the input might come from an IoT sensor that is tracking the location and condition of a shipment. In a governance application, the input might come from a human user who is casting a vote on a proposal.

\#\#\# 2.2. State Machine Architecture (FSM)

The Ternary Logic (TL) Smart Contract Execution Layer is fundamentally a deterministic, transaction-based state machine. This model, which underpins most modern smart contract platforms like Ethereum, ensures that given a specific initial state and a sequence of transactions, all network participants will arrive at the same final state . In the context of TL, the state machine is not merely a ledger of balances but a sophisticated engine for enforcing economic and governance rules. It transitions between a finite set of states based on predefined logic and external inputs, providing a predictable and verifiable framework for value management. The core of this architecture is the transition function, \`f(S, I) \-\> S'\`, where \`S\` is the current state, \`I\` is the input (a transaction or message), and \`S'\` is the new state . This deterministic execution is critical for consensus, as it guarantees that all nodes processing the same block of transactions will compute the same resulting state, thereby maintaining the integrity and consistency of the distributed ledger . The TL state machine extends this fundamental concept by embedding complex governance and economic logic directly into the state transition rules, moving beyond simple value transfers to a system of conditional execution and multi-party consensus.

The design of the TL state machine is heavily influenced by established patterns in smart contract development, particularly the use of Finite State Machines (FSMs) to model complex processes. FSMs are ideal for representing systems that move through distinct, sequential stages, such as an auction (\`Started\`, \`InProgress\`, \`Ended\`) or a multi-step governance proposal . In the case of TL, the FSM is defined by the three operational states: \`Proceed\` (+1), \`Epistemic Hold\` (0), and \`Refuse\` (-1). Each state represents a specific condition of a transaction or a proposal, and transitions between these states are governed by strict, immutable rules encoded in the smart contract. For instance, a transaction cannot simply jump from a \`Refuse\` state to a \`Proceed\` state without a new, valid proposal being submitted and passing through the necessary checks. This structured approach ensures that the system's behavior is predictable and secure, preventing unauthorized state changes and ensuring that all actions are accounted for. The use of an FSM also simplifies the auditing and verification process, as the entire lifecycle of a transaction can be formally modeled and its properties proven, a practice that is becoming increasingly important in the security-conscious DeFi space .

\#\#\#\# 2.2.1. Conceptual FSM Graph

The conceptual Finite State Machine (FSM) for the Ternary Logic system is defined by three primary states and a set of controlled transitions between them. The states are \`Proceed\` (+1), \`Epistemic Hold\` (0), and \`Refuse\` (-1). The system begins in a neutral or initial state, from which a transaction or proposal is initiated. Upon initiation, the system transitions into one of the three operational states based on the initial validation logic. The \`Epistemic Hold\` (0) state is the most critical and unique aspect of the TL FSM. It acts as a suspension or escrow state, where a transaction is neither finalized nor rejected but is instead locked pending further input. This state is triggered by ambiguity, uncertainty, or a requirement for external validation, such as an oracle feed or a decision from the Stewardship Custodians. This is a significant departure from traditional binary systems that only offer "success" or "failure" outcomes. The \`Proceed\` (+1) state represents a finalized and successful transaction, where assets are transferred, and the ledger is updated. Conversely, the \`Refuse\` (-1) state signifies a reverted transaction, where assets are returned to their original owners, and any associated fees or penalties are applied.

The transitions between these states are strictly controlled to ensure system integrity and prevent logical inconsistencies. A key feature of the TL FSM is the set of \*\*"forbidden transitions."\*\* For example, a transaction cannot move directly from the \`Refuse\` (-1) state to the \`Proceed\` (+1) state. Any transaction that has been formally rejected must be re-initiated as a new proposal, which will then follow the standard state transition path. This prevents the system from being manipulated by repeatedly attempting to push through a previously denied transaction. Similarly, a transaction in the \`Proceed\` (+1) state is considered final and cannot be reverted to a \`Hold\` or \`Refuse\` state, ensuring the immutability of finalized transactions. The \`Epistemic Hold\` (0) state is designed to be a temporary and resolvable state. From this state, the system can transition to either \`Proceed\` or \`Refuse\` based on the outcome of the resolution process, which could involve a multi-signature vote from custodians, a timeout period, or a definitive signal from an external oracle. This structured, rule-based approach to state transitions is what gives the TL system its robustness and makes it suitable for complex governance and economic applications where certainty and auditability are paramount.

\#\#\#\# 2.2.2. State Transition Logic Table

The state transition logic table for the TL smart contract is a formal specification of the system's state transitions. The table is composed of three columns: "Current State," "Action," and "Next State." The "Current State" column lists the three operational states of the TL framework. The "Action" column lists the events that can trigger a state transition, such as "Evidence Received" or "Timeout." The "Next State" column lists the state that the system will transition to when the corresponding action is taken in the current state. The table is designed to be exhaustive, meaning that it specifies the next state for every possible combination of current state and action. This exhaustiveness is a key feature of the TL framework, as it provides a complete and unambiguous specification of the system's behavior.

The following table provides a partial representation of the state transition logic for the TL smart contract, based on the Python code generated in the research phase :

| Current State | Action | Next State |  
| \--- | \--- | \--- |  
| \`PROCEED\` | \`SUSPENDED\` | \`EPISTEMIC\_HOLD\` |  
| \`PROCEED\` | \`REJECTED\` | \`REFUSE\` |  
| \`EPISTEMIC\_HOLD\` | \`EVIDENCE\_RECEIVED\` | \`PROCEED\` |  
| \`EPISTEMIC\_HOLD\` | \`REJECTED\` | \`REFUSE\` |  
| \`EPISTEMIC\_HOLD\` | \`TIMEOUT\` | \`REFUSE\` |  
| \`REFUSE\` | \`NEW\_PROPOSAL\` | \`PROCEED\` |

This table illustrates the core logic of the state machine, showing how the system transitions between the three operational states in response to different events. For example, it shows that a transaction in the \`PROCEED\` state can be suspended, moving it to the \`EPISTEMIC\_HOLD\` state, or it can be rejected, moving it to the \`REFUSE\` state. It also shows that a transaction in the \`EPISTEMIC\_HOLD\` state can be resolved by receiving evidence, which moves it to the \`PROCEED\` state, or by being rejected or timing out, which moves it to the \`REFUSE\` state. Finally, it shows that a transaction in the \`REFUSE\` state can be re-proposed, which moves it back to the \`PROCEED\` state.

\#\#\#\# 2.2.3. Forbidden Transitions

The TL state machine is designed with a set of \*\*forbidden transitions\*\* that are intended to prevent the system from entering an invalid or unstable state. These forbidden transitions are a critical component of the system's security and integrity, as they ensure that the system always behaves in a predictable and reliable manner. One of the most important forbidden transitions is the direct transition from the \`Refuse\` state to the \`Proceed\` state. This transition is forbidden because it would allow a transaction to be approved without going through the proper validation process. Instead, a transaction in the \`Refuse\` state must first be re-proposed, which triggers a new validation cycle. Another important forbidden transition is the direct transition from the \`Proceed\` state to the \`Refuse\` state. This transition is forbidden because it would allow a transaction to be reversed without a clear and documented reason. Instead, a transaction in the \`Proceed\` state must first be suspended, which moves it to the \`Epistemic Hold\` state, where it can be reviewed and either approved or rejected.

\#\#\#\# 2.2.4. Mechanics of the Epistemic Hold (0) State

The \`Epistemic Hold\` (0) state is the cornerstone of the Ternary Logic system's ability to manage uncertainty and enforce a "fail-secure" posture. This state is not merely a pause button but a sophisticated mechanism for suspending a transaction or proposal when the system encounters ambiguity, a lack of sufficient information, or a predefined condition for manual review. When a transaction enters the \`Epistemic Hold\` state, any associated assets are locked within the smart contract's escrow. They are neither transferred to the recipient nor returned to the sender; they are effectively frozen until a resolution is reached. This prevents any party from unilaterally moving funds while a dispute or uncertainty is being resolved, which is a critical feature for building trust in a decentralized system. The trigger for entering this state is not arbitrary but is based on specific, pre-programmed conditions. These conditions can range from a simple time-lock, where a transaction is held for a certain period to allow for public scrutiny, to more complex scenarios involving external data feeds from oracles. For example, a DeFi lending contract using TL logic might place a large loan request into an \`Epistemic Hold\` if the collateral's price, as reported by an oracle, becomes highly volatile or if the oracle feed itself becomes unreliable.

The resolution of the \`Epistemic Hold\` state is a structured process designed to re-establish certainty and allow the system to transition to a definitive \`Proceed\` (+1) or \`Refuse\` (-1) state. The specific mechanics of this resolution are defined by the contract's logic and can be tailored to the application's needs. One common pattern is to use a multi-signature (multi-sig) wallet controlled by the Stewardship Custodians. When a transaction is in the \`Hold\` state, the custodians can review the evidence, deliberate off-chain, and then collectively sign a transaction to either approve (\`Proceed\`) or deny (\`Refuse\`) the held transaction. This introduces a human-in-the-loop element for handling complex or subjective cases that cannot be automated. Another approach is to rely on a decentralized oracle network. For instance, a supply chain contract might hold a payment until an IoT sensor confirms that a shipment has arrived at its destination and met all required conditions (e.g., temperature, humidity). Once the oracle provides this definitive proof, the contract can automatically transition from \`Hold\` to \`Proceed\`. The \`Epistemic Hold\` state thus acts as a crucial buffer, allowing the system to pause, gather more information, and make a more informed decision, thereby preventing irreversible errors and enhancing the overall security and reliability of the protocol.

\#\#\# 2.3. Failure Modes and the "Fail-Secure" Zero

The Ternary Logic (TL) system is designed with a \*\*"fail-secure"\*\* philosophy, which is most evident in its behavior under adverse conditions. The core principle is that in the face of uncertainty, ambiguity, or system stress, the default action is to transition to the \`Epistemic Hold\` (0) state. This is a deliberate design choice that prioritizes the security of assets and the integrity of the system over liveness or convenience. Unlike systems that might "fail open" (allowing transactions to proceed in error) or "fail closed" (crashing or reverting in a way that could be exploited), the TL system defaults to a state of suspended animation. This ensures that no irreversible actions are taken when the system's normal operating conditions are not met. This "fail-secure" approach is a critical feature for any system that handles significant value, as it provides a robust defense against a wide range of potential failure modes, from technical glitches to malicious attacks. The system's architecture is built to anticipate these failures and to handle them in a predictable and secure manner, ensuring that the "laws" of the economic constitution are upheld even in the most challenging circumstances.

The "fail-secure" zero is not just a passive fallback but an active security measure. It is enforced through a combination of careful smart contract logic, robust oracle integration, and a well-defined governance structure. The system's state machine is designed to recognize the signs of potential failure and to trigger the \`Epistemic Hold\` state as a protective measure. For example, if an oracle fails to provide a required data point, the contract does not assume a default value or proceed with the last known value; instead, it places the transaction on hold until the oracle is restored or an alternative resolution is found. This proactive approach to security is what makes the TL system resilient. It acknowledges that in a complex, decentralized world, failures are inevitable, and it provides a structured and secure way to manage them. By defaulting to the \`Epistemic Hold\` state, the system ensures that it can weather the storm, maintain the security of its assets, and resume normal operations once the underlying issues have been resolved. This makes the TL system a robust and trustworthy foundation for building complex economic and governance applications.

\#\#\#\# 2.3.1. Handling Oracle Failure

Oracle failure is a significant risk in any smart contract system that relies on external data. The TL system addresses this risk head-on with its "fail-secure" design. When a smart contract requires data from an external source to execute a state transition (e.g., a price feed for a DeFi swap or a sensor reading for a supply chain payment), it is programmed to expect this data within a certain timeframe and in a specific format. If the oracle fails to deliver the data, delivers it late, or delivers data that is clearly outside of expected parameters (e.g., a price that is an order of magnitude off), the contract does not attempt to proceed with a "best guess" or a stale value. Instead, the logic is designed to trigger a transition to the \`Epistemic Hold\` (0) state. This immediately locks any assets involved in the transaction, preventing them from being moved or lost due to a decision based on bad or missing data. This is a critical safeguard against a common failure mode that has been exploited in numerous DeFi hacks.

The resolution of an \`Epistemic Hold\` triggered by oracle failure is also a structured process. The system can be designed to handle this in several ways. One approach is to have a backup oracle or a network of multiple oracles. If the primary oracle fails, the contract can automatically query the backup or wait for a consensus to be reached among the oracle network. Once a reliable data point is obtained, the contract can then transition from \`Hold\` to either \`Proceed\` or \`Refuse\` based on the new information. Another approach is to involve the Stewardship Custodians. In the event of an oracle failure, the contract can emit a specific event alerting the custodians to the issue. The custodians can then investigate the failure, potentially using off-chain resources to determine the correct data, and then use their multi-signature authority to manually resolve the held transaction. This human-in-the-loop approach is particularly useful for complex or high-value transactions where the cost of an error is high. By defaulting to the \`Hold\` state and providing a clear path for resolution, the TL system ensures that oracle failures do not lead to catastrophic losses but are instead handled as manageable, albeit inconvenient, events.

\#\#\#\# 2.3.2. Mitigating Flash Loan Attacks

Flash loan attacks are a class of exploits that take advantage of the unique properties of DeFi protocols to manipulate prices or other state variables within a single transaction. The core of a flash loan attack is the ability to borrow a large amount of an asset without collateral, use that capital to manipulate the state of another contract (e.g., by skewing the price on a decentralized exchange), and then repay the loan, all within the same atomic transaction. The TL system's "fail-secure" design, particularly the \`Epistemic Hold\` (0) state, provides a powerful defense against these types of attacks. By introducing a mandatory delay or a requirement for external validation for certain types of transactions, the TL architecture can break the atomicity that is essential for a successful flash loan attack. For example, a TL-based lending protocol could be designed to place any large withdrawal or any transaction that significantly alters a key state variable (like a collateralization ratio) into an \`Epistemic Hold\` state for a short period, such as a few blocks.

This delay, even if only for a few minutes, is enough to thwart a flash loan attack. The attacker would not be able to complete their entire exploit within a single transaction because the state change they are trying to manipulate would be locked in the \`Epistemic Hold\` state. During this hold period, other network participants, such as arbitrageurs or the protocol's own security bots, would have an opportunity to observe the attempted manipulation and take corrective action. They could, for example, arbitrage the price back to its correct level or alert the Stewardship Custodians to the malicious activity. The custodians could then use their authority to revert the transaction, preventing the attacker from profiting. Furthermore, the TL system's reliance on oracles for price data, combined with the \`Epistemic Hold\` mechanism, adds another layer of defense. If a flash loan attack attempts to manipulate the price on a single DEX, the protocol's oracle, which should be pulling data from multiple sources, would not be immediately affected. Any transaction relying on that price would be held until the oracle confirms the price across its various sources, effectively ignoring the manipulated price on the single DEX. This multi-layered approach, combining time delays, external validation, and human oversight, makes the TL system significantly more resilient to flash loan attacks than protocols that rely solely on on-chain data.

\#\#\#\# 2.3.3. Defaulting to State 0 (Hold) Under Stress

The "fail-secure" design of the TL framework is a critical component of its security and integrity. In the event of any type of failure or stress, the system will default to the \`Epistemic Hold\` state (0) rather than crashing or allowing theft. This "fail-secure" approach is a key feature of the TL framework, as it ensures that the system always behaves in a predictable and reliable manner, even under the most adverse conditions. The \`Epistemic Hold\` state provides a safe and secure environment for the system to recover from a failure, as it prevents any transactions from being executed until the issue has been resolved. This "fail-secure" approach is a testament to the robustness and resilience of the TL framework, and it is a key reason why the system is well-suited for use in critical infrastructure applications.

\#\# 3\. Technical Implementation Specification

\#\#\# 3.1. Solidity Implementation of Core States

\#\#\#\# 3.1.1. Defining States with \`enum\`

In Solidity, the three operational states of the Ternary Logic system—\`Proceed\`, \`Epistemic Hold\`, and \`Refuse\`—are best represented using an \`enum\`. This provides a clean, type-safe, and gas-efficient way to manage the state of a transaction or proposal. An \`enum\` is a user-defined type that consists of a set of named constants, which are internally represented as unsigned integers starting from 0\. By defining the states in this way, the smart contract can easily track the current state of any given process and perform conditional logic based on that state.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
// Define the three operational states using an enum  
enum TernaryState {  
Proceed,        // Represents the (+1) state  
EpistemicHold,  // Represents the (0) state  
Refuse          // Represents the (-1) state  
}

// Example: A struct to represent a transaction with a state  

struct Transaction {  

    uint256 id;  

    address initiator;  

    uint256 amount;  

    TernaryState state; // The state is of type TernaryState  

    // ... other fields  

}

// Example: A mapping to store transactions by their ID  

mapping(uint256 \\=\\\> Transaction) public transactions;

// Function to get the state of a transaction  

function getTransactionState(uint256 transactionId) public view returns (TernaryState) {  

    return transactions\\\[transactionId\\\].state;  

}  

}  
\`\`\`

In this example, the \`TernaryState\` enum clearly defines the three possible states. The \`Transaction\` struct then uses this enum as the data type for its \`state\` field. This makes the code more readable and less error-prone than using raw integers (e.g., 0, 1, 2\) to represent the states. The \`getTransactionState\` function demonstrates how to retrieve the state of a specific transaction, returning a value of type \`TernaryState\`.

\#\#\#\# 3.1.2. State Management and Storage

The management of these states within the smart contract's storage is a critical aspect of the implementation. The state of each transaction, proposal, or other governed entity must be persistently stored on the blockchain so that it can be accessed and updated over time. This is typically achieved by including the state enum as a field within a struct that represents the entity, and then storing that struct in a mapping or an array.

The choice of data structure depends on the specific requirements of the application. A \`mapping\` is often the most efficient choice for storing a large number of entities, as it allows for O(1) lookups by a unique key (e.g., a transaction ID). An \`array\` might be used if the entities need to be iterated over or if they are processed in a sequential order.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
enum TernaryState { Proceed, EpistemicHold, Refuse }

struct Proposal {  

    uint256 id;  

    string description;  

    TernaryState state;  

    uint256 votesFor;  

    uint256 votesAgainst;  

    uint256 votingDeadline;  

    // ... other fields  

}

// Using a mapping for O(1) access to proposals by ID  

mapping(uint256 \\=\\\> Proposal) public proposals;  

uint256 public proposalCount;

// Function to create a new proposal, initializing it in the 'Proceed' state  

function createProposal(string memory description) public returns (uint256) {  

    proposalCount++;  

    uint256 newProposalId \\= proposalCount;  

    proposals\\\[newProposalId\\\] \\= Proposal({  

        id: newProposalId,  

        description: description,  

        state: TernaryState.Proceed, // Initial state  

        votesFor: 0,  

        votesAgainst: 0,  

        votingDeadline: block.timestamp \\+ 7 days // Example: 7-day voting period  

    });  

    return newProposalId;  

}

// Function to transition a proposal to the 'EpistemicHold' state  

function suspendProposal(uint256 proposalId) public {  

    Proposal storage prop \\= proposals\\\[proposalId\\\];  

    require(prop.state \\== TernaryState.Proceed, "Proposal not in Proceed state");  

    prop.state \\= TernaryState.EpistemicHold;  

    // Emit a DecisionLog event (see Pillar 4\\)  

}  

}  
\`\`\`

In this example, the \`Proposal\` struct contains a \`TernaryState\` field to track its current state. The \`proposals\` mapping stores all proposals by their ID. The \`createProposal\` function initializes a new proposal in the \`Proceed\` state, while the \`suspendProposal\` function demonstrates how to update the state of an existing proposal. This pattern of using a struct and a mapping is a common and effective way to manage the state of multiple entities within a Solidity smart contract.

\#\#\# 3.2. Implementing the Eight Pillars in Solidity

\#\#\#\# 3.2.1. Epistemic Hold: The \`pause()\` Logic

The \`Epistemic Hold\` logic is not a simple administrative \`pause()\` function but a sophisticated, condition-driven mechanism. It is implemented as a set of internal functions or modifiers that check for specific conditions of uncertainty or ambiguity before allowing a state transition to a final \`+1\` or \`-1\` state. If these conditions are met, the transaction is automatically placed into the \`0\` state.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
enum TernaryState { Proceed, EpistemicHold, Refuse }

struct Transaction {  

    uint256 id;  

    uint256 amount;  

    TernaryState state;  

    uint256 holdDeadline; // Timestamp for hold resolution  

}

mapping(uint256 \\=\\\> Transaction) public transactions;

// Example: Oracle price feed  

uint256 public lastKnownPrice;  

uint256 public lastPriceUpdateTime;  

uint256 public constant PRICE\\\_STALENESS\\\_THRESHOLD \\= 1 hours;  

uint256 public constant PRICE\\\_VOLATILITY\\\_THRESHOLD \\= 10; // 10%

// Modifier to check if a transaction should be placed on hold  

modifier checkForHold(uint256 transactionId) {  

    Transaction storage txn \\= transactions\\\[transactionId\\\];  

    require(txn.state \\== TernaryState.Proceed, "Transaction not active");

    // Example condition: Check for stale price data  

    if (block.timestamp \\- lastPriceUpdateTime \\\> PRICE\\\_STALENESS\\\_THRESHOLD) {  

        txn.state \\= TernaryState.EpistemicHold;  

        txn.holdDeadline \\= block.timestamp \\+ 1 days; // 1 day to resolve  

        emit Decision(transactionId, TernaryState.Proceed, TernaryState.EpistemicHold, "Stale price data");  

        return; // Exit the function, transaction is now on hold  

    }

    // Example condition: Check for high price volatility  

    uint256 priceChange \\= getPriceChangePercent();  

    if (priceChange \\\> PRICE\\\_VOLATILITY\\\_THRESHOLD) {  

        txn.state \\= TernaryState.EpistemicHold;  

        txn.holdDeadline \\= block.timestamp \\+ 1 hours; // 1 hour to resolve  

        emit Decision(transactionId, TernaryState.Proceed, TernaryState.EpistemicHold, "High price volatility");  

        return;  

    }  

    \\\_; // Continue with the original function if no hold is triggered  

}

function finalizeTransaction(uint256 transactionId) public checkForHold(transactionId) {  

    Transaction storage txn \\= transactions\\\[transactionId\\\];  

    // If we reach here, the transaction was not put on hold  

    txn.state \\= TernaryState.Proceed;  

    // ... logic to transfer assets  

    emit Decision(transactionId, TernaryState.Proceed, TernaryState.Proceed, "Transaction finalized");  

}

function getPriceChangePercent() internal view returns (uint256) {  

    // Simplified logic for demonstration  

    return 5; // Assume 5% change  

}

event Decision(uint256 indexed transactionId, TernaryState previousState, TernaryState newState, string reason);  

}  
\`\`\`

In this example, the \`checkForHold\` modifier encapsulates the logic for triggering an \`Epistemic Hold\`. It checks for conditions like stale price data or high volatility. If a condition is met, it updates the transaction's state to \`EpistemicHold\`, sets a deadline for resolution, emits a \`Decision\` event, and then exits the function, effectively pausing the transaction. If no hold condition is met, the modifier executes the original function (\`finalizeTransaction\`).

\#\#\#\# 3.2.2. Immutable Ledger: \`DecisionLog\` Event Structure

The \`Immutable Ledger\` is implemented through a structured \`DecisionLog\` event that is emitted for every significant state change. This event serves as the on-chain record of the decision, providing a permanent and auditable history.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
enum TernaryState { Proceed, EpistemicHold, Refuse }

// Define a structured event for decision logs  

event DecisionLog(  

    uint256 indexed decisionId,      // Unique ID for the decision/transaction  

    address indexed initiator,       // Address that initiated the action  

    TernaryState previousState,      // The state before the transition  

    TernaryState newState,           // The state after the transition  

    bytes32 justificationHash,       // Hash of the off-chain justification  

    uint256 timestamp,               // block.timestamp of the decision  

    string reason                    // Human-readable reason for the state change  

);

// Function to transition state and emit a log  

function transitionState(  

    uint256 decisionId,  

    TernaryState newState,  

    bytes32 justificationHash,  

    string memory reason  

) internal {  

    // Assume we have a way to get the current state and initiator  

    TernaryState previousState \\= getCurrentState(decisionId);  

    address initiator \\= getInitiator(decisionId);

    // Update the state (implementation not shown)  

    // ...

    // Emit the structured log event  

    emit DecisionLog(  

        decisionId,  

        initiator,  

        previousState,  

        newState,  

        justificationHash,  

        block.timestamp,  

        reason  

    );  

}

// Placeholder functions for demonstration  

function getCurrentState(uint256 decisionId) internal view returns (TernaryState) {  

    return TernaryState.Proceed; // Simplified  

}  

function getInitiator(uint256 decisionId) internal view returns (address) {  

    return msg.sender; // Simplified  

}  

}  
\`\`\`

The \`DecisionLog\` event is designed to capture all relevant information about a state transition. The \`indexed\` keyword on \`decisionId\` and \`initiator\` allows for efficient filtering of logs. The \`justificationHash\` provides a link to off-chain context, while the \`reason\` provides a human-readable explanation. This structured event is the foundation of the Immutable Ledger, creating a rich and queryable history of all system actions.

\#\#\#\# 3.2.3. Goukassian Principle: The Ambiguity Gate

The \`Goukassian Principle\` is implemented as a logic gate that defaults to the \`EpistemicHold\` state in the presence of ambiguity. This is typically done using conditional logic (\`if-else\` statements) or \`require\` statements that check for the validity and completeness of data.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
enum TernaryState { Proceed, EpistemicHold, Refuse }

// Function to process an oracle price update  

function processPriceUpdate(uint256 newPrice, uint256 timestamp) public {  

    // Check for ambiguity: Is the price stale?  

    if (block.timestamp \\- timestamp \\\> 1 hours) {  

        // Ambiguity detected. Default to Hold.  

        transitionState(0, TernaryState.EpistemicHold, keccak256("Stale price"), "Price data is stale");  

        return;  

    }

    // Check for ambiguity: Is the price an outlier?  

    uint256 currentPrice \\= getCurrentPrice();  

    if (newPrice \\\> currentPrice \\\* 110 / 100 || newPrice \\\< currentPrice \\\* 90 / 100\\) {  

        // Ambiguity detected. Default to Hold.  

        transitionState(0, TernaryState.EpistemicHold, keccak256("Outlier price"), "Price is an outlier");  

        return;  

    }

    // If no ambiguity, proceed with the update  

    updatePrice(newPrice);  

    // ... other logic  

}

function transitionState(uint256 id, TernaryState newState, bytes32 hash, string memory reason) internal {  

    // Implementation for state transition and logging  

}

function getCurrentPrice() internal view returns (uint256) {  

    return 100; // Simplified  

}  

function updatePrice(uint256 newPrice) internal {  

    // Simplified  

}  

}  
\`\`\`

In this example, the \`processPriceUpdate\` function acts as the ambiguity gate. It checks if the incoming price data is stale or an outlier. If either condition is true, it does not proceed with the update or revert the transaction. Instead, it calls \`transitionState\` to move the system to the \`EpistemicHold\` state, effectively pausing operations until the ambiguity is resolved. This is the core of the Goukassian Principle in action.

\#\#\#\# 3.2.4. Decision Logs: The \`emit Decision(...)\` Requirement

The \`emit Decision(...)\` requirement is enforced by a modifier that wraps all state-changing functions. This modifier ensures that the \`Decision\` event is emitted before the function's logic is executed. If the event emission fails, the entire transaction is reverted.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
enum TernaryState { Proceed, EpistemicHold, Refuse }

event Decision(  

    uint256 indexed transactionId,  

    TernaryState previousState,  

    TernaryState newState,  

    string reason  

);

// Modifier to enforce the "No Log \\= No Action" mandate  

modifier noLogNoAction(  

    uint256 transactionId,  

    TernaryState newState,  

    string memory reason  

) {  

    TernaryState previousState \\= getCurrentState(transactionId); // Get state before change  

    \\\_; // Execute the original function's logic  

    // After the logic is executed, emit the log  

    emit Decision(transactionId, previousState, newState, reason);  

    // If the emit fails (e.g., out of gas), the transaction will revert  

}

function approveTransaction(uint256 transactionId)  

    public  

    noLogNoAction(transactionId, TernaryState.Proceed, "Transaction approved by governance")  

{  

    // The modifier ensures the Decision event is emitted if this logic succeeds  

    // ... logic to approve the transaction  

}

function getCurrentState(uint256 transactionId) internal view returns (TernaryState) {  

    return TernaryState.EpistemicHold; // Simplified  

}  

}  
\`\`\`

This \`noLogNoAction\` modifier is a powerful pattern for enforcing the "No Log \= No Action" mandate. It separates the concern of logging from the core business logic of the function. By applying this modifier to all state-changing functions, the system guarantees that every action is accompanied by a corresponding log entry, creating a complete and auditable record.

\#\#\#\# 3.2.5. Economic Rights & Transparency: Public \`view\` Functions

The \`Economic Rights & Transparency\` pillar is implemented through public \`view\` functions that provide read-only access to the contract's data. These functions do not consume gas and allow anyone to audit the system's state.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicTreasury {  
uint256 public totalFunds;  
mapping(address \=\> uint256) public allocatedFunds;  
address public technicalCouncil;  
address public stewardshipCustodians;

// Public view function to get the total treasury balance  

function getTreasuryBalance() public view returns (uint256) {  

    return address(this).balance;  

}

// Public view function to get the allocated funds for a specific project  

function getAllocatedFunds(address projectAddress) public view returns (uint256) {  

    return allocatedFunds\\\[projectAddress\\\];  

}

// Public view function to get the current withdrawal limits  

function getWithdrawalLimit() public view returns (uint256) {  

    // Example: Limit is 1% of total funds per month  

    return totalFunds \\\* 1 / 100;  

}

// Public view function to check if an address is a member of the Technical Council  

function isTechnicalCouncil(address account) public view returns (bool) {  

    return account \\== technicalCouncil;  

}

// Public view function to check if an address is a Stewardship Custodian  

function isStewardshipCustodian(address account) public view returns (bool) {  

    // In a real implementation, this would check a list or a role  

    return account \\== stewardshipCustodians; // Simplified  

}  

}  
\`\`\`

These \`view\` functions provide a transparent window into the contract's operations. Anyone can call them to verify the treasury balance, check fund allocations, or confirm the roles of governance members. This transparency is essential for building trust and allowing stakeholders to hold the system accountable.

\#\#\#\# 3.2.6. Sustainable Capital Allocation: Withdrawal Constraints

The \`Sustainable Capital Allocation\` pillar is implemented through constraints within the withdrawal function. These constraints prevent the treasury from being drained by limiting the amount and frequency of withdrawals.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicTreasury {  
uint256 public totalFunds;  
uint256 public lastWithdrawalTimestamp;  
uint256 public constant WITHDRAWAL\_PERIOD \= 30 days;  
uint256 public constant MAX\_WITHDRAWAL\_PERCENT \= 5; // 5% per period

// Function to withdraw funds from the treasury with constraints  

function withdraw(uint256 amount) public {  

    require(amount \\\> 0, "Withdrawal amount must be greater than 0");

    // Constraint 1: Check if the withdrawal period has passed  

    require(  

        block.timestamp \\\>= lastWithdrawalTimestamp \\+ WITHDRAWAL\\\_PERIOD,  

        "Withdrawal period has not passed"  

    );

    // Constraint 2: Check if the amount is within the allowed limit  

    uint256 maxWithdrawal \\= (totalFunds \\\* MAX\\\_WITHDRAWAL\\\_PERCENT) / 100;  

    require(amount \\\<= maxWithdrawal, "Withdrawal amount exceeds limit");

    // Update state  

    lastWithdrawalTimestamp \\= block.timestamp;  

    totalFunds \\-= amount;

    // Transfer the funds (simplified)  

    (bool success, ) \\= msg.sender.call{value: amount}("");  

    require(success, "Transfer failed");  

}

receive() external payable {  

    totalFunds \\+= msg.value;  

}  

}  
\`\`\`

This \`withdraw\` function enforces two key constraints: a time-based lock (\`WITHDRAWAL\_PERIOD\`) and a percentage-based limit (\`MAX\_WITHDRAWAL\_PERCENT\`). These constraints ensure that funds are released in a controlled and sustainable manner, protecting the long-term financial health of the project.

\#\#\#\# 3.2.7. Hybrid Shield: Multi-Sig and DAO Interfaces

The \`Hybrid Shield\` is implemented by requiring that certain critical functions can only be called by a designated multi-signature wallet or DAO contract. This is achieved by storing the address of the multi-sig/DAO in the contract and checking \`msg.sender\` against it.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
address public stewardshipCustodians; // Address of the multi-sig wallet or DAO

// Modifier to restrict function calls to the Stewardship Custodians  

modifier onlyStewardshipCustodians() {  

    require(msg.sender \\== stewardshipCustodians, "Not authorized");  

    \\\_;  

}

// Function to resolve an Epistemic Hold, only callable by Custodians  

function resolveHold(uint256 transactionId, TernaryState finalState)  

    public  

    onlyStewardshipCustodians  

{  

    // ... logic to resolve the hold  

    // This function can only be executed if the caller is the multi-sig/DAO  

}

// Function to upgrade the contract, only callable by Custodians  

function upgradeContract(address newImplementation)  

    public  

    onlyStewardshipCustodians  

{  

    // ... upgrade logic (e.g., using a proxy pattern)  

}  

}  
\`\`\`

In this example, the \`onlyStewardshipCustodians\` modifier acts as the gatekeeper. Any function decorated with this modifier can only be executed if the transaction originates from the address stored in \`stewardshipCustodians\`. This address would be the multi-signature wallet or the DAO contract, ensuring that these critical actions require collective approval.

\#\#\#\# 3.2.8. Anchors: Using \`block.timestamp\` and Oracle Hashes

The \`Anchors\` pillar is implemented by using \`block.timestamp\` to record the time of an event and by storing cryptographic hashes of external data to prove its integrity.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
struct DocumentAnchor {  
bytes32 documentHash;  
uint256 anchoredTimestamp;  
}

mapping(uint256 \\=\\\> DocumentAnchor) public documentAnchors;

// Function to anchor a document's hash to the blockchain  

function anchorDocument(uint256 documentId, bytes32 documentHash) public {  

    documentAnchors\\\[documentId\\\] \\= DocumentAnchor({  

        documentHash: documentHash,  

        anchoredTimestamp: block.timestamp // Anchor to current block time  

    });  

    emit DocumentAnchored(documentId, documentHash, block.timestamp);  

}

// Function to verify a document against its anchor  

function verifyDocument(uint256 documentId, bytes32 providedHash)  

    public  

    view  

    returns (bool)  

{  

    return documentAnchors\\\[documentId\\\].documentHash \\== providedHash;  

}

event DocumentAnchored(  

    uint256 indexed documentId,  

    bytes32 documentHash,  

    uint256 timestamp  

);  

}  
\`\`\`

This example shows how to anchor a document's hash. The \`anchorDocument\` function stores the hash and the current \`block.timestamp\`. The \`verifyDocument\` function allows anyone to verify if a given document hash matches the one stored on-chain. This creates a tamper-proof record of the document's state at a specific point in time, providing a verifiable link to the off-chain world.

\#\#\# 3.3. Enforcing the Mandates

\#\#\#\# 3.3.1. The \`NoLogNoAction\` Modifier

The \`NoLogNoAction\` modifier is a critical component for enforcing the "No Log \= No Action" mandate. It ensures that a \`Decision\` event is emitted for every state change. If the event emission fails, the entire transaction is reverted.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
enum TernaryState { Proceed, EpistemicHold, Refuse }

event Decision(  

    uint256 indexed transactionId,  

    TernaryState previousState,  

    TernaryState newState,  

    string reason  

);

// Modifier to enforce "No Log \\= No Action"  

modifier noLogNoAction(  

    uint256 transactionId,  

    TernaryState newState,  

    string memory reason  

) {  

    TernaryState previousState \\= getCurrentState(transactionId);  

    \\\_; // Execute the function's logic first  

    // After the logic, emit the log. If this fails, the tx reverts.  

    emit Decision(transactionId, previousState, newState, reason);  

}

function approveTransaction(uint256 transactionId)  

    public  

    noLogNoAction(transactionId, TernaryState.Proceed, "Approved by governance")  

{  

    // This logic will only execute if the Decision event is successfully emitted  

}

function getCurrentState(uint256 transactionId) internal view returns (TernaryState) {  

    return TernaryState.EpistemicHold; // Simplified  

}  

}  
\`\`\`

This modifier is applied to all state-changing functions. It captures the state before the change, executes the function, and then attempts to emit the \`Decision\` event. This pattern guarantees that an action and its corresponding log are an atomic unit; one cannot exist without the other.

\#\#\#\# 3.3.2. Implementing the \`NoSwitchOff\` Constraint

The \`NoSwitchOff\` constraint is implemented by simply \*\*not including a \`selfdestruct\` function\*\* or any other administrative function that could disable the contract. This is a "security by design" principle.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
// This contract has NO selfdestruct function  
// This contract has NO unilateral kill switch

// The only way to "upgrade" is through a proxy pattern,  

// which would be controlled by the Governance Trinity (e.g., multi-sig)

// ... rest of the contract logic  

}  
\`\`\`

By omitting these functions, the contract is designed to be immutable and perpetual. Any necessary upgrades would have to be handled through a proxy pattern, where the logic contract can be replaced, but this process itself would be governed by the strict rules of the Governance Trinity (e.g., requiring multi-signature approval), not by a single administrator.

\#\#\#\# 3.3.3. Exclusion Lists for the \`NoWeapon\` Mandate

The \`NoWeapon\` mandate is enforced by maintaining an on-chain exclusion list of forbidden addresses or function signatures. Any transaction attempting to interact with an address on this list will be automatically reverted.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
// Mapping to store forbidden addresses (e.g., sanctioned addresses)  
mapping(address \=\> bool) public forbiddenAddresses;

// Event to log the addition of a forbidden address  

event AddressForbidden(address indexed account);  

event AddressUnforbidden(address indexed account);

// Function to add an address to the exclusion list (only by Custodians)  

function forbidAddress(address account) public onlyStewardshipCustodians {  

    forbiddenAddresses\\\[account\\\] \\= true;  

    emit AddressForbidden(account);  

}

// Function to remove an address from the exclusion list  

function unforbidAddress(address account) public onlyStewardshipCustodians {  

    forbiddenAddresses\\\[account\\\] \\= false;  

    emit AddressUnforbidden(account);  

}

// Modifier to check if an address is forbidden  

modifier notForbidden(address account) {  

    require(\\\!forbiddenAddresses\\\[account\\\], "Address is forbidden");  

    \\\_;  

}

// Apply the modifier to all external functions that involve transfers  

function transfer(address recipient, uint256 amount)  

    public  

    notForbidden(msg.sender)  

    notForbidden(recipient)  

{  

    // ... transfer logic  

}

// Modifier for Stewardship Custodians (simplified)  

modifier onlyStewardshipCustodians() {  

    require(msg.sender \\== address(0x123), "Not authorized"); // Replace with actual multi-sig address  

    \\\_;  

}  

}  
\`\`\`

This example shows how to implement an exclusion list. The \`forbiddenAddresses\` mapping stores the list of banned addresses. The \`notForbidden\` modifier is applied to all sensitive functions, such as \`transfer\`, to check if the involved parties are on the list. The \`forbidAddress\` and \`unforbidAddress\` functions allow the Stewardship Custodians to manage the list, ensuring that it is kept up-to-date.

\#\# 4\. The Triple-Entry Accounting Model

The Ternary Logic (TL) system introduces a novel approach to on-chain accounting by implementing a \*\*Triple-Entry Accounting (TEA)\*\* model. This model extends the traditional double-entry bookkeeping system, which has been the foundation of accounting for centuries, by adding a third, cryptographically secured entry for every transaction. In a standard double-entry system, each transaction is recorded with a debit in one account and a corresponding credit in another, ensuring that the books always balance. The TL system retains this fundamental principle but enhances it with a third entry that serves as an immutable, verifiable receipt of the transaction. This third entry is not just a simple record of the transfer; it contains a cryptographic hash of the transaction's context and justification, creating an auditable trail that links the on-chain event to its real-world or off-chain origins. This is a significant departure from standard token contracts like ERC-20, which only record the change in balances (the debit and credit) without any inherent record of \*why\* that change occurred.

The implementation of TEA within a smart contract has profound implications for transparency, auditability, and trust. By creating a tamper-proof, third-party-verifiable record of every transaction, the TEA model makes it extremely difficult to commit fraud or manipulate financial records. The third entry, being stored on a distributed ledger like a blockchain, is not controlled by any single entity and is visible to all participants in the network . This creates a system of "trust through verification," where the integrity of the financial records is guaranteed by the cryptographic properties of the blockchain rather than by the trustworthiness of a central authority. This is particularly valuable in complex, multi-party scenarios such as supply chain management, where goods and payments pass through many hands, or in decentralized governance, where it is crucial to have a clear and undisputed record of all treasury transactions and decisions. The TEA model, as implemented in the TL system, provides the technical foundation for a new generation of financial applications that are more transparent, secure, and accountable than their traditional counterparts.

\#\#\# 4.1. Comparison with Double-Entry (ERC-20)

The standard ERC-20 token contract, which is the most common type of fungible token on the Ethereum blockchain, operates on a double-entry accounting principle. Its core functionality is to maintain a ledger of balances for each address. When a transfer occurs, the contract debits the balance of the sender and credits the balance of the recipient. This is a simple and efficient model for tracking ownership of a fungible asset, and it has been the workhorse of the DeFi ecosystem. However, this model has significant limitations when it comes to providing a complete and auditable record of transactions. The ERC-20 standard defines a \`Transfer\` event that is emitted whenever a transfer occurs, which logs the sender, recipient, and amount. While this provides a basic record of the transaction, it does not include any information about the \*context\* or \*justification\* for the transfer. For example, if a DAO treasury sends 100 ETH to a contractor, the ERC-20 log will show the transfer, but it will not explain that the payment was for "completion of Milestone 3 of Project X."

This lack of context is a major limitation of the double-entry model in a decentralized environment. It makes it difficult to perform a comprehensive audit of a treasury's activities, as the on-chain records alone do not provide enough information to understand the purpose of each transaction. This can lead to a lack of transparency and accountability, as it is possible for malicious actors to hide fraudulent transactions among a sea of legitimate ones. The TL system's Triple-Entry Accounting (TEA) model addresses this limitation by adding a third entry to the ledger. This third entry, which is implemented as a cryptographic hash stored in the contract's state or emitted as part of a custom event, contains a reference to the off-chain justification for the transaction. This could be a link to a proposal on a governance forum, a hash of a legal contract, or any other piece of evidence that provides the necessary context. By linking the on-chain transaction to this off-chain justification, the TEA model creates a much richer and more auditable record of all financial activities, making it a superior choice for any application where transparency and accountability are paramount.

\#\#\#\# 4.1.1. Limitations of Standard Double-Entry

The standard double-entry accounting model, while foundational to modern finance, has inherent limitations when applied to decentralized systems. Its primary weakness is the lack of \*\*contextual information\*\*. A double-entry ledger can answer \*what\* happened (e.g., "Account A was debited, Account B was credited"), but it cannot answer \*why\* it happened. This "why" is the crucial piece of information that provides meaning and justification for a transaction. In a traditional, centralized organization, this context is often provided by off-chain records, such as invoices, contracts, and meeting minutes. However, in a decentralized system, where trust is distributed and there is no central authority, relying on off-chain records creates a significant gap in auditability and accountability.

This gap can be exploited in several ways. For example, a malicious actor could create a series of seemingly legitimate transactions on-chain, while the off-chain justifications are fraudulent or non-existent. Without a cryptographically secure link between the on-chain and off-chain records, it becomes difficult, if not impossible, to detect this type of fraud. Furthermore, the lack of on-chain context makes it challenging to automate complex business processes that require a clear understanding of the purpose of a transaction. For example, a smart contract that is designed to release funds based on the completion of a specific milestone would need to be able to verify that the milestone has been reached, which is difficult to do with a standard double-entry ledger alone.

\#\#\#\# 4.1.2. The Need for a Third Entry

The need for a third entry in the accounting model arises from the fundamental challenge of bridging the gap between the on-chain and off-chain worlds. While blockchains are excellent at providing a secure and immutable record of on-chain events, they are inherently limited in their ability to understand the real-world context in which those events occur. A standard double-entry system, like that used in ERC-20 tokens, can tell you \*what\* happened (e.g., 100 tokens were transferred from address A to address B), but it cannot tell you \*why\* it happened. This "why" is the crucial piece of information that is needed to build a truly transparent and trustworthy system. Without it, the on-chain ledger is just a collection of numbers, devoid of the narrative that gives them meaning. The third entry in the TEA model is designed to capture this narrative. It acts as a bridge, linking the on-chain transaction to the off-chain evidence that justifies it.

This third entry is not just a "nice-to-have" feature; it is a critical component for building robust governance and economic systems. In a DAO, for example, it is not enough to simply see that funds were transferred from the treasury. Stakeholders need to know that the transfer was authorized by a valid proposal, that the proposal was approved by the required quorum, and that the funds are being used for their intended purpose. The third entry provides this assurance by creating an immutable link between the on-chain transaction and the off-chain record of the governance process. This makes it possible to conduct a full and transparent audit of the DAO's activities, ensuring that the organization is being run in a responsible and accountable manner. Similarly, in a supply chain, the third entry can be used to link a payment to a delivery confirmation, a quality inspection report, or a customs declaration. This creates a single, unified record of the entire transaction, from the initial order to the final payment, providing all parties with a shared source of truth and reducing the potential for disputes. The third entry is therefore the key to unlocking the full potential of blockchain technology, transforming it from a simple ledger of transactions into a powerful tool for building trust and transparency in a wide range of applications.

\#\#\# 4.2. The "Third Column": Justification and Context

The "third column" in the TL Triple-Entry Accounting ledger is where the justification and context for each transaction are recorded. This is the most innovative and powerful feature of the TEA model. Instead of just recording the debit and credit, the TL system creates a third entry that contains a cryptographic hash of the data that justifies the transaction. This data can be anything from a simple text string explaining the purpose of the payment to a complex JSON object containing multiple fields of information, such as the ID of a related proposal, the timestamp of an off-chain event, or the hash of a legal document. The key is that this data is not stored directly on the blockchain, as this would be expensive and would bloat the chain. Instead, only the cryptographic hash is stored. The actual data is stored off-chain, in a decentralized storage system like IPFS or on a traditional server. The hash serves as a unique and tamper-proof fingerprint for the data. Anyone can retrieve the data from the off-chain storage, hash it, and compare it to the hash stored on the blockchain to verify its integrity.

This "third column" has profound implications for the auditability and transparency of the system. It creates an immutable and verifiable link between the on-chain transaction and its real-world context. This means that for every transaction, there is a clear and undisputed record of \*why\* it happened. This is a game-changer for applications like DAO governance, where it is crucial to be able to trace every treasury expenditure back to a specific, approved proposal. It is also a major benefit for supply chain management, where it can be used to create a complete and verifiable record of a product's journey from the factory to the consumer. The "third column" effectively transforms the blockchain from a simple ledger of value transfers into a rich and detailed audit trail, providing a level of transparency and accountability that is simply not possible with traditional accounting systems. It is the technical mechanism that underpins the TL system's goal of moving from "trust" to "verification," providing the cryptographic certainty that is needed to build a new generation of more secure and trustworthy economic systems.

\#\#\#\# 4.2.1. Recording the Causal Chain

The "third column" is instrumental in recording the \*\*causal chain\*\* of a transaction. It provides the "why" behind the "what," creating a complete and verifiable narrative of the decision-making process. This is particularly important in complex systems like DAOs, where a single on-chain transaction is often the final step in a long and complex off-chain process. For example, a treasury expenditure might be the result of a community discussion, a formal proposal, a voting period, and a final execution call. The "third column" can be used to link the on-chain transaction to each of these preceding events, creating a complete and auditable record of the entire causal chain.

This is achieved by including references to the off-chain events in the justification data. For example, the justification for a treasury expenditure might include the IPFS hash of the proposal document, the transaction hash of the voting results, and a timestamp of the community discussion. All of this data is then hashed together to create the final justification hash that is stored on-chain. This creates a cryptographically secure link between the on-chain transaction and the off-chain events that led to it. This level of detail is invaluable for auditors, regulators, and other stakeholders who need to understand the full context of a transaction. It provides a level of transparency and accountability that is simply not possible with traditional accounting systems, which often rely on fragmented and easily manipulated off-chain records.

\#\#\#\# 4.2.2. Storing Justification Hashes

The practical implementation of the "third column" involves storing a cryptographic hash of the transaction's justification data within the smart contract. This is typically done by adding a new field to the contract's state or by including the hash as a parameter in a custom event that is emitted whenever a transaction occurs. The choice of data structure for storing the justification hash depends on the specific requirements of the application. If the justification needs to be easily queryable on-chain, it might be stored in a mapping that links transaction IDs to their corresponding hashes. If the primary goal is to create an immutable audit log, then emitting the hash as part of an event might be sufficient. The key is that the hash is permanently and publicly recorded on the blockchain, creating a tamper-proof record of the transaction's context.

The process of creating and storing a justification hash is as follows. First, the off-chain justification data is collected. This could be a combination of various pieces of information, such as a proposal ID, a user ID, a timestamp, and a description of the transaction. This data is then serialized into a standard format, such as a JSON string. The serialized data is then passed through a cryptographic hash function, such as SHA-256, to produce a fixed-length hash. This hash is then passed to the smart contract function as a parameter. The contract function verifies that the transaction is valid and then records the hash in its state or emits it in an event. This process ensures that there is a one-to-one correspondence between the on-chain transaction and the off-chain justification. Any attempt to alter the justification data would result in a different hash, which would be immediately detectable by anyone auditing the system. This provides a powerful mechanism for ensuring the integrity and authenticity of the transaction's context, making the entire system more transparent and trustworthy.

\#\#\# 4.3. Implementation in a TL Smart Contract

\#\#\#\# 4.3.1. Extending Standard Token Contracts

The Triple-Entry Accounting (TEA) model can be implemented by extending a standard token contract, such as ERC-20. This involves overriding the \`transfer\` and \`transferFrom\` functions to include the logic for the third entry. The key is to add a new parameter to these functions for the justification hash and to ensure that this hash is recorded on-chain.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TernaryToken is ERC20 {  
// Event for the third entry (Triple-Entry Accounting)  
event TransferWithContext(  
address indexed from,  
address indexed to,  
uint256 value,  
bytes32 justificationHash,  
string context  
);

constructor(string memory name, string memory symbol) ERC20(name, symbol) {}

// Override the transfer function to include a justification hash  

function transferWithJustification(  

    address to,  

    uint256 amount,  

    bytes32 justificationHash,  

    string memory context  

) public returns (bool) {  

    // Perform the standard transfer  

    bool success \\= transfer(to, amount);  

    require(success, "Transfer failed");

    // Emit the event for the third entry  

    emit TransferWithContext(msg.sender, to, amount, justificationHash, context);  

    return true;  

}

// The standard transfer function can still be used, but it won't have the third entry  

// Alternatively, it could be disabled to force the use of the new function  

}  
\`\`\`

In this example, the \`transferWithJustification\` function extends the standard \`transfer\` function by adding the \`justificationHash\` and \`context\` parameters. It first performs the standard transfer and then emits a \`TransferWithContext\` event, which serves as the third entry in the ledger. This approach allows for backward compatibility with the ERC-20 standard while also providing the enhanced functionality of the TEA model.

\#\#\#\# 4.3.2. Event Structures for Triple-Entry

The event structure for the third entry is a critical component of the TEA model. It should be designed to capture all relevant information about the transaction's context, including the justification hash, a human-readable description, and any other relevant metadata.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicSystem {  
// A comprehensive event for the third entry  
event TripleEntryLog(  
uint256 indexed transactionId,  
address indexed initiator,  
address indexed recipient,  
uint256 amount,  
bytes32 justificationHash,  
string contextDescription,  
string proposalId, // Example: Link to a governance proposal  
uint256 timestamp,  
string category // Example: "Treasury", "Payroll", "Grant"  
);

function executeTransaction(  

    uint256 transactionId,  

    address recipient,  

    uint256 amount,  

    bytes32 justificationHash,  

    string memory contextDescription,  

    string memory proposalId,  

    string memory category  

) public {  

    // ... logic to execute the transaction

    // Emit the comprehensive event for the third entry  

    emit TripleEntryLog(  

        transactionId,  

        msg.sender,  

        recipient,  

        amount,  

        justificationHash,  

        contextDescription,  

        proposalId,  

        block.timestamp,  

        category  

    );  

}  

}  
\`\`\`

This \`TripleEntryLog\` event is a more comprehensive example of the third entry. It includes a wide range of fields that provide a rich and detailed record of the transaction's context. This level of detail is essential for creating a truly auditable and transparent system. The \`indexed\` keyword is used on key fields to allow for efficient filtering and querying of the logs.

\#\# 5\. Governance and Permissioning

\#\#\# 5.1. Role-Based Access Control (RBAC)

Role-Based Access Control (RBAC) is a fundamental security pattern for managing permissions in a smart contract system. It involves defining a set of roles, each with a specific set of permissions, and then assigning these roles to different accounts. This approach is more granular and secure than using a single "owner" account, as it allows for a more fine-grained control over who can perform what actions. In the context of the Ternary Logic framework, RBAC is used to implement the Governance Trinity, with each body having its own distinct role and set of permissions.

\#\#\#\# 5.1.1. Defining Roles for the Governance Trinity

The Governance Trinity consists of three distinct bodies: the Technical Council, the Stewardship Custodians, and the Smart Contract Treasury. Each of these bodies should have its own unique role in the RBAC system. For example, the Technical Council might have a role that allows it to propose code upgrades, the Stewardship Custodians might have a role that allows them to resolve disputes, and the Smart Contract Treasury might have a role that allows it to manage the project's funds. By defining these roles, the system can ensure that each body can only perform the actions that are within its remit, preventing any single entity from gaining too much power.

\#\#\#\# 5.1.2. Using OpenZeppelin's \`AccessControl\`

OpenZeppelin's \`AccessControl\` library is a popular and well-audited implementation of RBAC for Solidity. It provides a flexible and secure framework for managing roles and permissions in a smart contract. The library allows you to define roles as \`bytes32\` constants and then assign these roles to different accounts. It also provides a set of modifiers, such as \`onlyRole\`, that can be used to restrict access to functions based on the caller's role.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract TernaryLogicGovernance is AccessControl {  
// Define roles as bytes32 constants  
bytes32 public constant TECHNICAL\_COUNCIL\_ROLE \= keccak256("TECHNICAL\_COUNCIL\_ROLE");  
bytes32 public constant STEWARDSHIP\_CUSTODIANS\_ROLE \= keccak256("STEWARDSHIP\_CUSTODIANS\_ROLE");  
bytes32 public constant TREASURY\_ROLE \= keccak256("TREASURY\_ROLE");

constructor() {  

    // Grant the default admin role to the deployer (can be transferred later)  

    \\\_grantRole(DEFAULT\\\_ADMIN\\\_ROLE, msg.sender);  

}

// Function to grant a role to an account (only by an admin)  

function grantTechnicalCouncilRole(address account) public onlyRole(DEFAULT\\\_ADMIN\\\_ROLE) {  

    \\\_grantRole(TECHNICAL\\\_COUNCIL\\\_ROLE, account);  

}

// Function to revoke a role from an account (only by an admin)  

function revokeTechnicalCouncilRole(address account) public onlyRole(DEFAULT\\\_ADMIN\\\_ROLE) {  

    \\\_revokeRole(TECHNICAL\\\_COUNCIL\\\_ROLE, account);  

}

// Function that can only be called by the Technical Council  

function proposeUpgrade() public onlyRole(TECHNICAL\\\_COUNCIL\\\_ROLE) {  

    // ... logic for proposing an upgrade  

}

// Function that can only be called by the Stewardship Custodians  

function resolveDispute() public onlyRole(STEWARDSHIP\\\_CUSTODIANS\\\_ROLE) {  

    // ... logic for resolving a dispute  

}  

}  
\`\`\`

In this example, the \`TernaryLogicGovernance\` contract inherits from \`AccessControl\`. It defines three roles for the Governance Trinity. The \`onlyRole\` modifier is used to restrict access to the \`proposeUpgrade\` and \`resolveDispute\` functions, ensuring that they can only be called by accounts with the appropriate role.

\#\#\# 5.2. Technical Council Implementation

\#\#\#\# 5.2.1. Time-Locked Functions for Upgrades

Time-locks are a critical security feature for smart contract upgrades. They introduce a mandatory delay between the proposal of an upgrade and its execution, giving the community time to review the changes and react if necessary. This is typically implemented by storing the timestamp of the proposal and then checking that the required delay has passed before allowing the upgrade to be executed.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract TernaryLogicUpgrades is AccessControl {  
bytes32 public constant TECHNICAL\_COUNCIL\_ROLE \= keccak256("TECHNICAL\_COUNCIL\_ROLE");  
uint256 public constant UPGRADE\_DELAY \= 2 days; // 2-day delay

struct UpgradeProposal {  

    address newImplementation;  

    uint256 proposedAt;  

    bool executed;  

}

UpgradeProposal public pendingUpgrade;

function proposeUpgrade(address newImplementation) public onlyRole(TECHNICAL\\\_COUNCIL\\\_ROLE) {  

    pendingUpgrade \\= UpgradeProposal({  

        newImplementation: newImplementation,  

        proposedAt: block.timestamp,  

        executed: false  

    });  

    emit UpgradeProposed(newImplementation, block.timestamp);  

}

function executeUpgrade() public onlyRole(TECHNICAL\\\_COUNCIL\\\_ROLE) {  

    require(pendingUpgrade.newImplementation \\\!= address(0), "No pending upgrade");  

    require(\\\!pendingUpgrade.executed, "Upgrade already executed");  

    require(block.timestamp \\\>= pendingUpgrade.proposedAt \\+ UPGRADE\\\_DELAY, "Delay not passed");

    // Logic to perform the upgrade (e.g., using a proxy)  

    // ...

    pendingUpgrade.executed \\= true;  

    emit UpgradeExecuted(pendingUpgrade.newImplementation);  

}

event UpgradeProposed(address newImplementation, uint256 timestamp);  

event UpgradeExecuted(address newImplementation);  

}  
\`\`\`

In this example, the \`proposeUpgrade\` function sets the \`proposedAt\` timestamp. The \`executeUpgrade\` function then checks that the \`UPGRADE\_DELAY\` has passed before allowing the upgrade to be executed. This ensures that there is a mandatory waiting period for all upgrades.

\#\#\#\# 5.2.2. Proposal and Voting Mechanisms

The Technical Council's decision-making process can be implemented using an on-chain proposal and voting mechanism. This allows for a transparent and auditable record of all proposals and votes. A simple implementation might involve a struct to represent a proposal and a mapping to store the votes of each council member.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract TernaryLogicCouncilVoting is AccessControl {  
bytes32 public constant TECHNICAL\_COUNCIL\_ROLE \= keccak256("TECHNICAL\_COUNCIL\_ROLE");

struct Proposal {  

    string description;  

    uint256 votesFor;  

    uint256 votesAgainst;  

    mapping(address \\=\\\> bool) hasVoted;  

    bool executed;  

}

Proposal\\\[\\\] public proposals;

function createProposal(string memory description) public onlyRole(TECHNICAL\\\_COUNCIL\\\_ROLE) {  

    proposals.push();  

    Proposal storage p \\= proposals\\\[proposals.length \\- 1\\\];  

    p.description \\= description;  

    emit ProposalCreated(proposals.length \\- 1, description);  

}

function vote(uint256 proposalId, bool support) public onlyRole(TECHNICAL\\\_COUNCIL\\\_ROLE) {  

    Proposal storage p \\= proposals\\\[proposalId\\\];  

    require(\\\!p.hasVoted\\\[msg.sender\\\], "Already voted");  

    require(\\\!p.executed, "Proposal already executed");

    p.hasVoted\\\[msg.sender\\\] \\= true;  

    if (support) {  

        p.votesFor++;  

    } else {  

        p.votesAgainst++;  

    }  

    emit VoteCast(proposalId, msg.sender, support);  

}

function executeProposal(uint256 proposalId) public onlyRole(TECHNICAL\\\_COUNCIL\\\_ROLE) {  

    Proposal storage p \\= proposals\\\[proposalId\\\];  

    require(\\\!p.executed, "Proposal already executed");  

    require(p.votesFor \\\> p.votesAgainst, "Proposal not approved");

    p.executed \\= true;  

    // ... logic to execute the proposal  

    emit ProposalExecuted(proposalId);  

}

event ProposalCreated(uint256 proposalId, string description);  

event VoteCast(uint256 proposalId, address voter, bool support);  

event ProposalExecuted(uint256 proposalId);  

}  
\`\`\`

This example shows a simple on-chain voting system for the Technical Council. It allows council members to create proposals, vote on them, and execute them if they are approved. This provides a transparent and auditable record of the council's decision-making process.

\#\#\# 5.3. Stewardship Custodians Implementation

\#\#\#\# 5.3.1. Multi-Signature Wallet Integration

The Stewardship Custodians' authority is best implemented through a multi-signature (multi-sig) wallet. A multi-sig wallet is a smart contract that requires a predefined number of signatures from a group of owners to authorize a transaction. This distributes power and prevents any single custodian from acting unilaterally. The TL smart contract would then delegate its critical functions to the multi-sig wallet.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicCustodianActions {  
address public stewardshipCustodians; // Address of the multi-sig wallet

// Modifier to restrict function calls to the multi-sig wallet  

modifier onlyCustodians() {  

    require(msg.sender \\== stewardshipCustodians, "Not authorized by Custodians");  

    \\\_;  

}

function resolveEpistemicHold(uint256 transactionId, bool approve)  

    public  

    onlyCustodians  

{  

    // ... logic to resolve the hold  

    if (approve) {  

        // Transition to Proceed  

    } else {  

        // Transition to Refuse  

    }  

}

function vetoUpgrade(address newImplementation) public onlyCustodians {  

    // ... logic to veto a proposed upgrade  

}  

}  
\`\`\`

In this example, the \`stewardshipCustodians\` variable stores the address of the multi-sig wallet. The \`onlyCustodians\` modifier checks that the caller is the multi-sig wallet, ensuring that only the collective decision of the custodians can authorize the action. The actual multi-sig wallet contract (e.g., a Gnosis Safe) would be a separate contract that manages the list of custodians and the signature threshold.

\#\#\#\# 5.3.2. Dispute Resolution Workflow for State (0)

The dispute resolution workflow for transactions in the \`Epistemic Hold\` (0) state is a key responsibility of the Stewardship Custodians. The workflow would typically involve an off-chain deliberation process, followed by an on-chain action to resolve the hold.

1\.  \*\*Detection of Hold\*\*: A transaction enters the \`Epistemic Hold\` state due to a detected ambiguity or dispute.  
2\.  \*\*Notification\*\*: The smart contract emits an event to notify the custodians that a transaction is on hold.  
3\.  \*\*Off-Chain Deliberation\*\*: The custodians review the evidence and deliberate off-chain (e.g., on a forum, in a video call).  
4\.  \*\*On-Chain Resolution\*\*: Once a decision is reached, the custodians use their multi-sig wallet to call a function on the TL smart contract to resolve the hold.  
5\.  \*\*State Transition\*\*: The smart contract transitions the transaction to either the \`Proceed\` (+1) or \`Refuse\` (-1) state based on the custodians' decision.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicDisputeResolution {  
enum TernaryState { Proceed, EpistemicHold, Refuse }

struct Transaction {  

    uint256 id;  

    TernaryState state;  

    string disputeReason;  

}

mapping(uint256 \\=\\\> Transaction) public transactions;  

address public stewardshipCustodians; // Multi-sig address

event HoldTriggered(uint256 transactionId, string reason);  

event HoldResolved(uint256 transactionId, TernaryState finalState, string resolution);

function triggerHold(uint256 transactionId, string memory reason) public {  

    transactions\\\[transactionId\\\].state \\= TernaryState.EpistemicHold;  

    transactions\\\[transactionId\\\].disputeReason \\= reason;  

    emit HoldTriggered(transactionId, reason);  

}

function resolveHold(uint256 transactionId, bool approve, string memory resolution)  

    public  

{  

    require(msg.sender \\== stewardshipCustodians, "Not authorized");  

    Transaction storage txn \\= transactions\\\[transactionId\\\];  

    require(txn.state \\== TernaryState.EpistemicHold, "Not on hold");

    if (approve) {  

        txn.state \\= TernaryState.Proceed;  

    } else {  

        txn.state \\= TernaryState.Refuse;  

    }

    emit HoldResolved(transactionId, txn.state, resolution);  

}  

}  
\`\`\`

This simplified example illustrates the core logic of the dispute resolution workflow. The \`triggerHold\` function places a transaction on hold, and the \`resolveHold\` function, which is only callable by the multi-sig wallet, resolves it.

\#\#\# 5.4. Smart Contract Treasury

\#\#\#\# 5.4.1. Autonomous Vault Design

The Smart Contract Treasury is designed as an autonomous vault, meaning it is controlled by its own internal logic rather than by a human administrator. This is achieved by encoding the rules for fund allocation and release directly into the smart contract. The treasury contract would hold the project's funds and would only release them when specific, predefined conditions are met.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicTreasury {  
uint256 public totalFunds;  
address public technicalCouncil;  
address public stewardshipCustodians;

// ... other state variables

receive() external payable {  

    totalFunds \\+= msg.value;  

}

// Function to request funds, which can only be called by authorized contracts  

function requestFunds(uint256 amount, string memory justification)  

    public  

    returns (uint256 requestId)  

{  

    // ... logic to create a funding request  

    // This would typically involve a proposal and voting process  

}

// Function to release funds, which is called by the governance logic  

function releaseFunds(address payable recipient, uint256 amount) internal {  

    require(amount \\\<= address(this).balance, "Insufficient funds");  

    totalFunds \\-= amount;  

    (bool success, ) \\= recipient.call{value: amount}("");  

    require(success, "Transfer failed");  

}  

}  
\`\`\`

This example shows the basic structure of an autonomous treasury. It can receive funds and has internal functions to manage the release of those funds. The key is that the \`releaseFunds\` function is \`internal\`, meaning it can only be called by other functions within the contract, which would be governed by the rules of the Governance Trinity.

\#\#\#\# 5.4.2. Programmed Fund Allocation and Release

The allocation and release of funds from the treasury are programmed into the smart contract's logic. This can involve a variety of mechanisms, such as vesting schedules, milestone-based payments, and budget allocations.

\`\`\`solidity  
// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;

contract TernaryLogicTreasury {  
struct FundingAllocation {  
address recipient;  
uint256 totalAmount;  
uint256 releasedAmount;  
uint256 startTime;  
uint256 duration; // Vesting duration  
}

mapping(uint256 \\=\\\> FundingAllocation) public allocations;  

uint256 public allocationCount;

function createAllocation(  

    address recipient,  

    uint256 totalAmount,  

    uint256 duration  

) public {  

    // ... authorization checks (e.g., only by governance)

    allocationCount++;  

    allocations\\\[allocationCount\\\] \\= FundingAllocation({  

        recipient: recipient,  

        totalAmount: totalAmount,  

        releasedAmount: 0,  

        startTime: block.timestamp,  

        duration: duration  

    });  

}

function releaseVestedFunds(uint256 allocationId) public {  

    FundingAllocation storage allocation \\= allocations\\\[allocationId\\\];  

    require(allocation.recipient \\== msg.sender, "Not the recipient");

    uint256 releasableAmount \\= calculateReleasableAmount(allocation);  

    require(releasableAmount \\\> 0, "No funds to release");

    allocation.releasedAmount \\+= releasableAmount;  

    (bool success, ) \\= allocation.recipient.call{value: releasableAmount}("");  

    require(success, "Transfer failed");  

}

function calculateReleasableAmount(FundingAllocation memory allocation)  

    internal  

    view  

    returns (uint256)  

{  

    if (block.timestamp \\\>= allocation.startTime \\+ allocation.duration) {  

        return allocation.totalAmount \\- allocation.releasedAmount;  

    } else {  

        uint256 elapsedTime \\= block.timestamp \\- allocation.startTime;  

        uint256 vestedAmount \\= (allocation.totalAmount \\\* elapsedTime) / allocation.duration;  

        return vestedAmount \\- allocation.releasedAmount;  

    }  

}  

}  
\`\`\`

This example shows a simple vesting schedule implementation. The \`createAllocation\` function sets up a new vesting schedule, and the \`releaseVestedFunds\` function allows the recipient to claim their vested funds over time. This is a powerful mechanism for ensuring that funds are released in a controlled and responsible manner, in line with the long-term goals of the project.

\#\# 6\. Cross-Domain Applicability and Case Studies

The Ternary Logic (TL) Smart Contract Execution Layer, with its unique blend of a three-state system, Triple-Entry Accounting, and robust governance mechanisms, is not limited to a single use case. Its design principles are broadly applicable across a wide range of domains where trust, transparency, and secure value management are critical. While the primary use case is envisioned to be in the realm of decentralized governance, the underlying architecture is flexible enough to be adapted to other complex systems, such as Decentralized Finance (DeFi) and supply chain management. The core value proposition of the TL system—its ability to handle uncertainty, enforce rules, and provide a verifiable audit trail—makes it a powerful tool for any application that involves multiple parties, conditional payments, and the need for a shared source of truth. The following sections will explore how the TL system can be applied in these different domains, providing concrete examples and case studies to illustrate its versatility and power.

The adaptability of the TL system stems from its modular and principle-driven design. The three operational states (\`Proceed\`, \`Epistemic Hold\`, \`Refuse\`) can be mapped to a wide variety of real-world processes. In a governance context, they might represent the lifecycle of a proposal. In a DeFi context, they could represent the states of a conditional escrow. In a supply chain, they could represent the status of a shipment. The Eight Pillars, which define the technical implementation of the system, provide a consistent and secure framework for building these applications, regardless of the specific domain. The \`Epistemic Hold\` state, in particular, is a key enabler of cross-domain applicability. It provides a generic mechanism for handling uncertainty and disputes, which is a common challenge in almost any complex system. By providing a structured way to pause, investigate, and resolve issues, the TL system can help to build more resilient and trustworthy applications across a wide range of industries.

\#\#\# 6.1. Primary Use Case: Governance

The primary use case for the Ternary Logic framework is in the realm of decentralized governance, particularly for Decentralized Autonomous Organizations (DAOs). DAOs are organizations that are governed by smart contracts and managed by a community of stakeholders. They often have a treasury of funds that needs to be managed in a transparent and accountable way. The TL system is ideally suited for this purpose, as it provides a robust framework for on-chain voting, treasury management, and dispute resolution.

\#\#\#\# 6.1.1. On-Chain Voting and Proposal Systems

The TL system can be used to create a more secure and transparent on-chain voting system. A proposal can be created in the \`Proceed\` state, and then community members can vote on it. If the vote is successful, the proposal can be executed. If there is a dispute or a lack of consensus, the proposal can be placed in the \`Epistemic Hold\` state for further review by the Stewardship Custodians. This provides a structured way to handle contentious proposals and to ensure that all decisions are made in a fair and equitable manner.

\#\#\#\# 6.1.2. Treasury Management for DAOs

The TL system is particularly well-suited for managing a DAO's treasury. The \`Sustainable Capital Allocation\` pillar provides a mechanism for preventing the treasury from being drained, while the \`Economic Rights & Transparency\` pillar provides a way for stakeholders to audit the flow of funds. The \`Epistemic Hold\` state can be used to pause any large or controversial expenditures, giving the community time to review and debate them. This provides a much-needed layer of security and accountability for DAO treasuries, which are often targeted by malicious actors.

\#\#\# 6.2. Decentralized Finance (DeFi)

The DeFi ecosystem, with its complex protocols for lending, borrowing, trading, and derivatives, is a natural fit for the Ternary Logic system. The current DeFi landscape is largely built on smart contracts that operate in a binary fashion: a transaction either succeeds or fails. While this is efficient for simple swaps, it can be problematic for more complex financial instruments that involve significant risk and uncertainty. The TL system's \`Epistemic Hold\` state provides a much-needed third option, allowing for the creation of more sophisticated and risk-managed DeFi products. For example, a decentralized lending protocol could use the TL system to manage large loans. Instead of simply liquidating a borrower's collateral if its value drops below a certain threshold, the protocol could place the loan into an \`Epistemic Hold\` state. This would give the borrower an opportunity to add more collateral or negotiate a new repayment plan, while also giving the protocol time to assess the situation and avoid a potentially disruptive liquidation.

Another key application of the TL system in DeFi is in the area of conditional escrow and settlement. Many DeFi applications, such as decentralized exchanges and derivatives platforms, rely on escrow contracts to hold funds until certain conditions are met. The TL system can enhance these contracts by providing a more flexible and secure framework for managing the escrow process. For example, a decentralized options contract could use the TL system to manage the settlement process. When an option expires, the contract could place the settlement into an \`Epistemic Hold\` state while it waits for a definitive price feed from an oracle. This would prevent any disputes or manipulation of the settlement price, ensuring a fair and transparent process for all parties. The Triple-Entry Accounting model is also highly relevant to DeFi. By creating an immutable and verifiable record of every transaction, the TEA model can help to improve the transparency and auditability of DeFi protocols, making it easier for users to understand the risks they are taking and for regulators to oversee the market.

\#\#\#\# 6.2.1. Conditional Escrow and Settlement

Conditional escrow and settlement are fundamental building blocks of the DeFi ecosystem. They are used in a wide range of applications, from decentralized exchanges to cross-chain bridges. The TL system provides a powerful framework for implementing these features in a more secure and flexible way. A conditional escrow contract using TL logic would hold funds in the \`Epistemic Hold\` state until a specific condition is met. For example, a cross-chain bridge could hold a user's funds in escrow until it receives a confirmation from the destination chain. This would prevent the loss of funds in the event of a technical failure or a malicious attack.

\#\#\#\# 6.2.2. Oracle-Based Derivatives

Oracle-based derivatives are another key application of the TL system. These are financial instruments whose value is derived from the price of an underlying asset, as reported by an oracle. The TL system can be used to create more secure and reliable oracle-based derivatives by using the \`Epistemic Hold\` state to pause settlement in the event of an oracle failure or a price manipulation attack. This would protect users from the risks associated with unreliable or malicious oracles, which are a common attack vector in the DeFi space.

\#\#\# 6.3. Supply Chain Management

The Ternary Logic system can also be applied to supply chain management to create a more transparent and efficient system for tracking goods and managing payments. The \`Epistemic Hold\` state can be used to pause a payment until a shipment has been confirmed to have arrived at its destination and met all required quality standards. This would reduce the risk of fraud and disputes, and would provide a more secure and reliable way to manage international trade.

\#\#\#\# 6.3.1. Tracking Goods with Verifiable States

The TL system can be used to track the movement of goods through a supply chain, with each stage of the journey being represented by a state in the smart contract. For example, a shipment could start in the \`Proceed\` state, then move to the \`Epistemic Hold\` state for customs clearance, and then back to the \`Proceed\` state for final delivery. This would create a transparent and auditable record of the entire journey, providing all parties with a shared source of truth.

\#\#\#\# 6.3.2. Automated Payments on Delivery Confirmation

The TL system can be used to automate payments on delivery confirmation. A smart contract could be programmed to release a payment to a supplier only when it receives a confirmation from a trusted oracle that the goods have been delivered and have passed a quality inspection. This would reduce the need for manual intervention and would provide a more efficient and secure way to manage payments in a supply chain.

\#\#\# 6.4. Real-World Case Study: A Governance Proposal

Let's consider a real-world case study of a governance proposal in a DAO that uses the Ternary Logic framework. The DAO has a treasury of 1,000 ETH and is considering a proposal to fund a new marketing campaign for 100 ETH.

![][image2]

\#\#\#\# 6.4.1. Initial Proposal and State (+1)

A community member creates a proposal on the DAO's forum, outlining the details of the marketing campaign and requesting 100 ETH from the treasury. The proposal is then submitted to the on-chain voting system, where it enters the \`Proceed\` state. Community members then have a period of time to vote on the proposal.

\#\#\#\# 6.4.2. Triggering an Epistemic Hold (State 0\)

During the voting period, a community member raises a concern that the proposal is too vague and does not provide enough detail about how the funds will be used. The community is split on the issue, and the vote is too close to call. As a result, the proposal is placed in the \`Epistemic Hold\` state for further review.

\#\#\#\# 6.4.3. Custodian Intervention and Final State Resolution

The Stewardship Custodians are notified of the hold and they begin an off-chain review of the proposal. They request more information from the proposal's creator and they consult with marketing experts to assess the feasibility of the campaign. After a week of deliberation, the custodians decide that the proposal is not in the best interests of the DAO. They use their multi-signature wallet to call a function on the TL smart contract to resolve the hold and transition the proposal to the \`Refuse\` state. The proposal is rejected, and the 100 ETH remains in the treasury.

\#\# 7\. Platform Considerations and Future-Proofing

\#\#\# 7.1. Ethereum as the Primary Target

\#\#\#\# 7.1.1. Leveraging the EVM and Solidity

The primary target for the Ternary Logic Smart Contract Execution Layer is the Ethereum blockchain. This is due to its mature ecosystem, large developer community, and the widespread adoption of the Ethereum Virtual Machine (EVM) and the Solidity programming language. By targeting Ethereum, the TL framework can leverage a rich set of existing tools, libraries, and infrastructure, such as OpenZeppelin's contract libraries, Hardhat and Foundry development environments, and a wide range of oracles and other services. The EVM's Turing-completeness and the expressiveness of Solidity make it well-suited for implementing the complex logic of the TL system, including the three-state model, the Eight Pillars, and the Governance Trinity.

\#\#\#\# 7.1.2. Integration with Layer 2 Solutions (Polygon)

To address the scalability and cost challenges of the Ethereum mainnet, the TL framework should be designed to be compatible with Layer 2 (L2) scaling solutions, such as Polygon. L2 solutions offer lower transaction fees and higher throughput, making them an attractive option for applications that require a high volume of transactions. The TL framework can be deployed on an L2 network with minimal changes to the core logic, as most L2 solutions are EVM-compatible. This would allow the TL system to benefit from the security of the Ethereum mainnet while also enjoying the scalability and cost-effectiveness of an L2 network.

\#\#\# 7.2. Adaptation for Other Platforms

\#\#\#\# 7.2.1. Bitcoin via Script or RSK

While Bitcoin's scripting language is not Turing-complete, it is possible to implement a simplified version of the TL framework on Bitcoin. This would involve using Bitcoin's native multi-signature capabilities to create a multi-sig wallet for the Stewardship Custodians and using the \`OP\_CHECKLOCKTIMEVERIFY\` opcode to implement time-locks. However, the full functionality of the TL system, including the \`Epistemic Hold\` state and the Triple-Entry Accounting model, would be difficult to implement on Bitcoin's base layer. A more promising approach would be to use a sidechain or a Layer 2 solution like RSK, which is a smart contract platform that is pegged to the Bitcoin blockchain. RSK is EVM-compatible, which would allow for a direct port of the Solidity-based TL smart contracts to the Bitcoin ecosystem.

\#\#\#\# 7.2.2. Considerations for Non-EVM Chains

Adapting the TL framework for non-EVM chains, such as Solana or Polkadot, would require a more significant effort. These platforms use different programming languages (e.g., Rust for Solana, Ink\! for Polkadot) and have different execution models than the EVM. However, the core principles of the TL framework are platform-agnostic and could be implemented on any smart contract platform that supports a Turing-complete programming language. The key would be to translate the Solidity-based logic of the TL system into the native language of the target platform, while also taking into account the unique features and constraints of that platform.

\#\#\# 7.3. Upgradeability and Extensibility

\#\#\#\# 7.3.1. Proxy Pattern for Logic Upgrades

To ensure the long-term viability of the TL framework, it is important to design the system to be upgradeable. This is typically achieved through the use of a proxy pattern, such as the OpenZeppelin Proxy Pattern. A proxy pattern separates the logic of the smart contract from its storage. The logic is stored in a separate "implementation" contract, while the storage is stored in a "proxy" contract. The proxy contract delegates all calls to the implementation contract, but it retains control over the storage. This allows the logic of the system to be upgraded by deploying a new implementation contract and then updating the proxy to point to the new contract. This is a powerful pattern for ensuring that the TL system can evolve and adapt to new challenges over time.

\#\#\#\# 7.3.2. Versioning and Migration Strategies

When upgrading a smart contract, it is important to have a clear versioning and migration strategy. This involves carefully planning the upgrade process to ensure that it is executed smoothly and without any loss of data or functionality. A versioning strategy might involve using semantic versioning (e.g., v1.0.0, v1.1.0) to track the different versions of the contract. A migration strategy might involve creating a migration contract that is responsible for transferring the state from the old version of the contract to the new version. This is a complex process that requires careful planning and testing, but it is essential for ensuring the long-term success of the TL framework.

\#\# 8\. Conclusion: The Constitutional Code

\#\#\# 8.1. Summary of the TL Execution Layer

The Ternary Logic (TL) Smart Contract Execution Layer is a novel and robust framework for building secure, transparent, and accountable economic and governance systems. It introduces a third, intermediate state—\*\*Epistemic Hold (0)\*\*—to manage uncertainty and enforce verifiable prudence. This is achieved through a combination of eight core architectural pillars, a tripartite governance model, and four non-negotiable hard constraints. The system is designed to move from a model of "Trust" to one of "Verification," embedding the rules of economic interaction directly into immutable and transparent smart contracts. The TL framework is not just a theoretical concept; it is a practical and implementable specification that can be used to build a new generation of more secure and trustworthy decentralized applications.

\#\#\# 8.2. The "Economic Constitution" Analogy

The TL framework can be thought of as an \*\*"Economic Constitution."\*\* Just as a political constitution sets out the fundamental principles and rules by which a state is governed, the TL framework sets out the fundamental principles and rules by which an economic system is governed. The four mandates—\*\*No Spy\*\*, \*\*No Weapon\*\*, \*\*No Log \= No Action\*\*, and \*\*No Switch Off\*\*—are the constitutional rights of the system, protecting it from specific types of harm. The Governance Trinity is the separation of powers, ensuring that no single entity has too much control. The Eight Pillars are the institutional structures that support the system and ensure its smooth operation. And the Triple-Entry Accounting model is the evidentiary record, providing a complete and auditable history of all actions. By encoding these constitutional principles into smart contract code, the TL framework creates a system where the rules of money are harder to break than the laws of men.

\#\#\# 8.3. Final Remarks on Trust and Verification

The Ternary Logic framework represents a significant step forward in the evolution of decentralized systems. It provides a practical and implementable solution to the challenge of building trust in a trustless environment. By moving from a model of "Trust" to one of "Verification," the TL framework creates a system where the integrity of the system is guaranteed by the cryptographic properties of the blockchain, rather than by the trustworthiness of a central authority. This is a powerful concept that has the potential to transform a wide range of industries, from finance and governance to supply chain management and beyond. The TL framework is not a panacea, and it is not without its challenges. However, it provides a solid foundation for building a new generation of more secure, transparent, and accountable decentralized systems.

\#\# 9\. Glossary of Terms

\*   \*\*Anchors\*\*: The mechanism by which the TL system connects its on-chain decisions to real-world events and data, typically using \`block.timestamp\` or cryptographic hashes of external data.  
\*   \*\*Decision Layer\*\*: The off-chain component of the TL system that is responsible for gathering information, evaluating evidence, and making a determination as to whether a transaction or proposal should proceed, be held, or be refused.  
\*   \*\*Economic Constitution\*\*: An analogy used to describe the TL framework, where the rules of economic interaction are embedded in immutable and transparent smart contracts, making them harder to break than traditional legal agreements.  
\*   \*\*Enforcement Layer\*\*: The on-chain smart contract that is responsible for executing the decisions made by the Decision Layer.  
\*   \*\*Epistemic Hold (0)\*\*: The intermediate state in the TL system, which represents a pause in execution due to uncertainty, ambiguity, or a need for further verification.  
\*   \*\*Fail-Secure\*\*: A design principle where the system defaults to a secure state (in this case, the \`Epistemic Hold\` state) in the face of failure or ambiguity.  
\*   \*\*Finite State Machine (FSM)\*\*: A computational model that is used to represent the state transitions of the TL system.  
\*   \*\*Governance Trinity\*\*: The tripartite governance model of the TL system, which consists of the Technical Council, the Stewardship Custodians, and the Smart Contract Treasury.  
\*   \*\*Goukassian Principle\*\*: The core safety mechanism of the TL system, which dictates that the system should default to the \`Hold\` (0) state in the presence of ambiguity.  
\*   \*\*Hybrid Shield\*\*: A multi-layered defense mechanism that combines cryptographic security with institutional oversight, typically through the use of a multi-signature wallet for the Stewardship Custodians.  
\*   \*\*Immutable Ledger\*\*: The on-chain record of all decisions and state changes, which is implemented through a structured \`Log\` event structure.  
\*   \*\*Mandates\*\*: The four hard constraints of the TL system: \*\*No Spy\*\*, \*\*No Weapon\*\*, \*\*No Log \= No Action\*\*, and \*\*No Switch Off\*\*.  
\*   \*\*No Log \= No Action\*\*: A mandate that requires every state change to be accompanied by a corresponding log entry.  
\*   \*\*No Spy\*\*: A mandate that prohibits the system from engaging in any form of backdoor data collection or surveillance.  
\*   \*\*No Switch Off\*\*: A mandate that prohibits the inclusion of a \`selfdestruct\` function or any other unilateral kill switch in the smart contract.  
\*   \*\*No Weapon\*\*: A mandate that prohibits the use of the TL framework for any purpose that is designed to cause harm.  
\*   \*\*Pillars\*\*: The eight foundational components of the TL system: \*\*Epistemic Hold\*\*, \*\*Immutable Ledger\*\*, \*\*Goukassian Principle\*\*, \*\*Decision Logs\*\*, \*\*Economic Rights & Transparency\*\*, \*\*Sustainable Capital Allocation\*\*, \*\*Hybrid Shield\*\*, and \*\*Anchors\*\*.  
\*   \*\*Proceed (+1)\*\* : The final state in the TL system, which represents the successful and irreversible confirmation of a transaction.  
\*   \*\*Refuse (-1)\*\* : The final state in the TL system, which represents the rejection and reversion of a transaction.  
\*   \*\*Role-Based Access Control (RBAC)\*\* : A security pattern for managing permissions in a smart contract system by defining roles and assigning them to different accounts.  
\*   \*\*Stewardship Custodians\*\*: The ethical and legal guardians of the TL framework, who are responsible for resolving disputes and ensuring compliance with the established principles.  
\*   \*\*Sustainable Capital Allocation\*\*: A pillar that introduces smart contract constraints to prevent the drainage of a treasury and ensure the long-term sustainability of the project.  
\*   \*\*Technical Council\*\*: The body responsible for the technical maintenance and evolution of the TL framework.  
\*   \*\*Ternary Logic (TL)\*\* : The three-state computational model that is the foundation of the TL framework.  
\*   \*\*Third Column\*\*: The part of the Triple-Entry Accounting ledger that records the justification and context for each transaction.  
\*   \*\*Triple-Entry Accounting (TEA)\*\* : An accounting model that extends the traditional double-entry system by adding a third, cryptographically secured entry for every transaction.  
\*   \*\*Trust to Verification\*\*: The core paradigm shift of the TL framework, moving from a system based on trust in human promises to one based on cryptographic verification.  
\*   \*\*Zero-Knowledge (ZK) Proofs\*\*: A cryptographic technique that allows a user to prove that they possess certain information without revealing the information itself.  


[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>