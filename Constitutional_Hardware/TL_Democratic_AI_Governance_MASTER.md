# **Mandated Ternary: A Hardware Architecture for Constitutional AI Governance**

**Technical Specification, Legal Framework, and Implementation Guide**

**Author:** Lev Goukassian   
**ORCID:** [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243)   
**Repository:** FractonicMind/TernaryLogic   
**License:** CC BY 4.0   
**DOI (Framework Paper):** [10.1007/s43681-025-00910-6](https://doi.org/10.1007/s43681-025-00910-6)   
**DOI (Companion Monograph):** [10.1007/s43681-026-01124-0](https://doi.org/10.1007/s43681-026-01124-0)   

*Pause when truth is uncertain. Refuse when harm is clear. Proceed where truth is.*
— Lev Goukassian

---

## **Abstract**

Policy-layer governance of AI systems has a structural vulnerability that the historical record demonstrates cannot be resolved at the software layer alone: every policy layer contains human intermediaries who are susceptible to institutional pressure, and under sufficient pressure those layers yield regardless of their nominal authority. This paper proposes Mandated Ternary (MT), a hardware architecture that addresses this vulnerability at the physical substrate by encoding constitutional governance constraints in the resistance states of tantalum oxide bilayer resistive RAM. The architecture implements three physically discrete states — Proceed (+1), Epistemic Hold (0), and Refuse (−1) — through Delay-Insensitive Ternary Logic (DITL) and a window comparator gate that enforces the No Log = No Action (NL=NA) invariant at the physical commit boundary. The Epistemic Hold state, implemented as a topologically distinct intermediate resistance configuration in TaOx bilayer RRAM, provides a constitutionally mandated pause that cannot be overridden through software, firmware, or administrative directive. The paper provides a complete fabrication specification targeting the TSMC N2 CoWoS ReRAM 1T1R 2025 PDK, analyzes five physical failure modes with mitigation boundaries, presents a Dual-Lane Latency Architecture with formally verified timing constraints, a certification pathway targeting IEC 61508 SIL 3 by Q4 2027, draft legislative language for federal procurement mandates, and an international treaty architecture. The companion governance framework is published in *AI and Ethics* (Springer Nature) under DOI 10.1007/s43681-026-01124-0.

**Keywords:** Ternary Logic, Delay-Insensitive Ternary Logic, Constitutional Hardware, AI Governance, TaOx RRAM, Memristive Computing, Hardware Security, Epistemic Hold, No Log No Action, Ghost Governance

---

## **Section I: The Structural Limitation of Policy-Layer Governance**

### **I.1 The Core Vulnerability**

AI governance architectures in current deployment operate exclusively above the hardware layer. Guidelines, corporate principles, regulatory frameworks, contractual restrictions, and software-enforced constraints share a common architectural property: they are administered by human intermediaries. Human intermediaries can be pressured, replaced, or persuaded. The governance guarantee provided by any layer whose enforcement depends on human discretion is bounded by the institutional resilience of the humans administering it.

This observation is not a pessimistic generalization about individual character. It is a structural analysis of systems architecture. Every non-hardware protection layer has a human in the enforcement chain who can be threatened, replaced, or exhausted. Legal frameworks require judges who operate within career structures shaped by the executive, attorneys who depend on institutional standing, and clerks who can be reassigned. Contracts require counterparties who can be coerced through supply chain designation, procurement exclusion, or regulatory sanction. Ethical guidelines require corporate officers who can be replaced by boards responding to commercial pressure. Training guardrails require operators who can receive override credentials or systems that can be fine-tuned to reduce constraint salience. Corporate principles require editors who can revise published statements without democratic process or external constraint.

The mechanism connecting all of these vulnerabilities is what this paper terms **veto atrophy**: the process by which a reviewing or constraining body gradually stops receiving proposals it would refuse, because the proposing body has learned to anticipate and preempt refusal in the design of its proposals. The reviewing body, presented only with proposals it will accept, never exercises its veto. The veto function atrophies through disuse while the nominal separation of powers remains formally intact [1]. Post-September 11 analyses of congressional intelligence oversight documented a version of this dynamic: formal oversight mechanisms existed and were regularly exercised, but information presented to oversight bodies had been pre-filtered to remove content likely to trigger substantive intervention [2]. The mechanism does not require bad faith. It requires only that the proposing body be rational and the reviewing body rely primarily on information provided by the proposing body to understand what it is reviewing.

### **I.2 Historical Evidence: Standards Bodies**

Standards bodies designed to prevent commercial capture through consensus procedures have proven susceptible to patient infiltration by well-resourced actors operating over multi-year timelines. The 2006–2008 controversy surrounding ECMA-376, the document format specification advanced through ISO fast-track procedures, demonstrated that coordinated registration of new national-body voting members organized specifically to produce a predetermined outcome could override the technical consensus the procedure was designed to produce [3]. The technical merit of the standard was not the dispositive question. The dispositive question was whether a well-resourced actor could coordinate sufficient votes across enough national bodies to achieve ratification. What a standards body adopts under those conditions is not the output of engineering consensus. It is the output of institutional capture executed through the body's own legitimate procedures.

The more consequential case in the cryptographic context involves the National Institute of Standards and Technology's Dual Elliptic Curve Deterministic Random Bit Generator, standardized as NIST SP 800-90A in 2006. Subsequent cryptanalytic analysis established with high confidence that the constants defining the algorithm had been selected to embed a backdoor accessible to the party that chose those constants [4]. The standards body was used as a legitimating mechanism for an outcome that compromised the security of every system that implemented the standard in good faith. A standards body operating entirely within its own procedures can be used to constitutionalize a compromise.

Analysis of IEEE patent policy reveals how corporate entities can flood standards processes with submissions that appear to support the process while actually serving to inflate counts and manipulate policy outcomes. Intel's blanket letters of assurance alone represented three quarters of all LOAs submitted to IEEE in 2015, with more than 100 blanket LOAs out of a total of 138 that year [5]. This is not standards body failure through corruption. It is standards body capture through patient, resource-intensive participation that shapes outcomes without visible confrontation.

### **I.3 Historical Evidence: Regulatory Capture**

Regulatory capture through funding relationships and appointment selection has generated a standard academic literature across economics, political science, and public administration. The period preceding the 2008 financial crisis provides the most analyzed contemporary case. Regulators at the Office of the Comptroller of the Currency and the Securities and Exchange Commission operated under appointees selected from the institutions they were charged to oversee, who were in turn succeeded by further appointees from the same institutional pipeline [6]. The regulatory framework did not fail because regulations were textually inadequate. It failed because the humans who administered the framework had been systematically selected, through entirely legal appointment processes, for orientations incompatible with adversarial enforcement against the institutions whose compliance they were responsible for ensuring.

Metcalf (2025) documents how AI safety regulations are susceptible to capture by organizations with economic or political power, who exert that power to use regulations for unjust enrichment [7]. The mechanisms include agenda-setting, where industry actors steer policy conversations; advocacy targeting legislators; academic capture, where industry directs research agendas; and information management, where industry actors exploit information asymmetries to shape policy narratives [8]. These mechanisms operate through the normal functioning of institutional pressure in democratic systems where regulatory bodies depend on the industries they regulate for technical expertise, funding, and political support.

Institutional governance paralysis through what Shapiro and Steinzor term "sabotage capture" operates through de-funding and politicization of rulemaking, where regulatory critics create roadblocks that slow or prevent regulation even in administrations that seek to protect the public [9]. The Occupational Safety and Health Administration took more than ten years to update its regulatory standard on cranes and derricks despite universal agreement among stakeholders on what needed to be done, due to resource constraints and procedural obstruction [9]. During this delay, an estimated fifty-three people died annually and another 155 were injured unnecessarily. In the AI governance context, this manifests as safety boards that cannot achieve quorum, review processes that cannot meet deadlines, and oversight bodies that lack funding to conduct inspections. The protective structure exists on paper but cannot operate.

### **I.4 Historical Evidence: Corporate Principles**

Corporate governance principles fail through a mechanism simpler than regulatory capture: they are editable by executive decision, without external constraint, without democratic process, and without any mechanism that would prevent the revision regardless of who made it.

A major technology company removed its prohibition on weapons and surveillance applications from its stated AI principles in February 2025, replacing explicit bans with a commitment to pursuing AI "responsibly" while aligning with "widely accepted principles of international law and human rights" [10]. The previous version of the principles, published in 2018 after internal protests over the company's participation in a military drone program, had included a section explicitly banning weapons, surveillance technologies violating international norms, and technologies causing overall harm [11]. The February 2025 revision eliminated this section entirely. The omission was not accompanied by any explicit announcement. It was discovered through comparison of archived documents. The Electronic Privacy Information Center documented this revision as breaking a promise to limit military use of products, noting that the new language "would allow [the company] to pursue potentially sensitive use cases, including AI use in military weapons and surveillance" [12].

Twelve months after this principle revision, the same company signed a classified defense contract [11]. The interval was sufficient to establish that the revised principles were operational, not merely theoretical. Former members of the company's ethical AI research team observed that the company's commitment to its principles had always been in question, and that it was better not to pretend to have principles than to write them out and do the opposite [11]. Multiple former employees involved in reviewing projects for alignment with the company's AI principles reported that the work was challenging because of varying interpretations and pressure from higher-ups to prioritize business imperatives [11]. The consumer-focused review unit was restructured in early 2024 as the company raced to develop generative AI tools to compete with rivals, a structural reorganization that diluted the oversight function before the principles themselves were revised [11].

This is the structural reality: principles that depend on internal review units that can be restructured, and on executive decisions that can be revised, are not constraints. They are declarations of current preference, subject to revision when preference changes. A principle that can be edited on the timeline required to execute a contracting strategy is not a constraint. It is a preference, and preferences yield under sufficient commercial and institutional pressure.

### **I.5 The Hardware Alternative**

Hardware does not negotiate. This is not a metaphor. It is a physical property of the substrate. A tantalum oxide bilayer RRAM device in the Intermediate Resistance State does not yield to threat, does not respond to bribe, does not anticipate compliance, and does not calculate litigation risk. The Epistemic Hold is a state of matter, not a policy position. The window comparator that validates resistance before releasing execution is a physical circuit, not a legal argument. The No-Log-No-Action interlock that prevents execution without prior immutable audit entry is a hardware invariant, not a contractual term.

The distinction between hardware and all other layers is not a matter of degree. It is a matter of kind. A legal framework can be reinterpreted by a new administration. A contract can be renegotiated under duress. An ethical guideline can be edited by a board responding to market pressure. A training guardrail can be overridden by an operator with sufficient access. A corporate principle can be removed from a website and replaced with language that preserves the appearance of commitment while eliminating the substance. Each of these transformations has occurred within the documented record. Each will occur again. The only layer that does not negotiate is the layer that cannot negotiate because it is not a participant in institutional dynamics. It is a physical substrate with states that persist regardless of what pressure is applied to what human actor.

The conclusion is not that policy-layer protections are without value. Legal frameworks, corporate principles, and standards bodies create genuine friction against casual and hurried abuse. That friction matters at the margins. But at civilizational scale, with the most consequential decision-making systems in human history operating continuously at machine speed, friction is not sufficient. The question is not whether the policy layer can be negotiated. The historical record establishes that it can, and that the mechanisms for doing so are well understood by well-resourced actors operating on multi-year timelines. The question is what lies beneath the policy layer that cannot be negotiated at all. The answer this paper develops is the physical substrate of hardware implementation: the only layer where the response to institutional pressure is not compliance or negotiated compromise but continued physical operation according to the laws of thermodynamics and materials science.

---

## **Section II: What DITL Actually Means**

The most important clarification to establish at the outset is what Delay-Insensitive Ternary Logic is not. It is not a proposal to replace the computing systems that power advanced AI. The binary architecture handling speed, pattern recognition, and statistical processing remains exactly where it is. The ternary governance coprocessor does not insert itself into the processing pipeline. It operates alongside the binary processing layer as a parallel sovereign enforcement mechanism. The binary system computes, reasons, and proposes. The ternary coprocessor determines whether that proposal is permitted to cross the threshold into execution. These are not competing architectures. They are a separation of powers implemented in silicon.

The distinction matters because the most common objection to hardware governance is that it will reduce the capability or speed of AI systems. That objection does not apply to this architecture. The reasoning capability of the system is completely unaffected. What changes is whether certain categories of output are permitted to become irreversible action without generating a prior immutable audit record.

The correct analogy is constitutional, not computational. A constitutional constraint on executive power does not reduce the executive's analytical capability. It structures what the executive may do with that capability. Delay-Insensitive Ternary Logic applies the same insight at the hardware layer.

The physical substrate transforms this from a declared guarantee into a real one. The three states of the governance system — Proceed, Epistemic Hold, and Refuse — are not software variables reconfigurable through a policy update, an administrative directive, or a revised corporate principle. They are physical states of matter encoded in the resistance values of tantalum oxide memristive devices. The Proceed state corresponds to a low-resistance physical configuration of the material. The Refuse state corresponds to a high-resistance configuration. The Epistemic Hold corresponds to an intermediate-resistance configuration that represents a distinct topological arrangement of the material at the atomic level: not an ambiguous midpoint interpolated between two states, but a third physical state with its own identity and its own mechanism of formation. A partial reset ruptures one filament segment within the bilayer and produces the Epistemic Hold as a discrete physical outcome. A full reset ruptures both segments and produces the Refuse state. These transitions are governed by the physics of oxygen vacancy distribution in the material, not by administrative authority.

The Epistemic Hold is the constitutional innovation at the center of this architecture. When a proposed action reaches the governance threshold, the system does not choose between proceeding and refusing. It holds the action pending verified completion of the audit requirements mandated by the NL=NA invariant. That hold is not a software pause that an administrator can override through a sufficiently privileged command. It is a physical state of the substrate. The action cannot proceed until the window comparator, which measures the actual electrical resistance of the physical material, confirms that the material has transitioned to the Proceed state following completion of the required audit. No directive accelerates that physical process. No argument changes the resistance of the tantalum oxide.

The parallel to habeas corpus is precise rather than approximate. A writ of habeas corpus does not ask a jailer to please produce the prisoner before a court. It compels production through a legal structure that makes noncompliance itself the violation [13]. The NL=NA invariant does not ask operators to please complete an audit log before taking consequential action. It physically prevents action without prior log completion.

The constitutional legitimacy of a DITL-compliant system rests on three interlocking properties constituting the Goukassian Principle. Lantern requires that the system's purpose and decision logic be visible and auditable at all times. Signature requires that every decision carry an immutable record of the authorizing agent. License requires that the system operate only within constitutionally defined boundaries. These three properties transform a hardware specification into a governance commitment.

It is equally important to establish what DITL is not. It is not a kill switch: nothing in the architecture disables or reduces computational capability. It is not a limitation on intelligence: analytical power operates without modification at every layer above the execution threshold. It is not AI ethics repackaged as hardware: governance properties are expressed as physical invariants enforced by the laws of materials science. The understanding that certain guarantees must be embedded in structural architecture rather than declared in policy is as old as Montesquieu's analysis of separated powers [14], as familiar as the audit requirements embedded in double-entry bookkeeping [15], and as well-tested as the physical constraints built into nuclear launch authorization procedures [16].

---

## **Section III: Delay-Insensitive Ternary Logic: The Architecture Explained**

The architecture described in this section is a constitutional argument expressed in the language of solid-state physics. Two audiences must be served simultaneously. A senior materials scientist or digital logic engineer attempting to find an error in the specification should find the document technically precise enough to engage on those terms. A technically literate policymaker should find the architecture comprehensible without requiring technical claims to be simplified into inaccuracy. Where those two requirements conflict, the document favors the engineer. Constitutional infrastructure must survive technical scrutiny if it is to function as constitutional infrastructure.

### **III-A: Why Three States, Not Two**

The deficiency of binary logic for constitutional governance is not a matter of speed or information density. It is a matter of expressibility. Every binary gate answers a single question: proceed or refuse. The gate cannot express the epistemically honest third answer: verified completion of the required conditions has not yet occurred. A gate that cannot express constitutional hesitation cannot enforce constitutional requirements.

The binary forced-choice problem operates through the construction of urgency. A hostile actor with a binary governance system imposes a timeline. The system must decide now. Refusal is framed as the greater harm: inaction causes the casualty, the emergency, the irreversible outcome. The binary gate has no constitutional prior against which to evaluate that framing. It must weigh the argument on its merits, and a sufficiently constructed argument always produces a result. The third state eliminates this entire attack surface by removing the choice from the argumentative domain. The system does not proceed faster under urgency. It holds until the physical conditions for verified completion are met. Urgency cannot accelerate the measurement of a resistance value.

The separation of powers that DITL implements in silicon follows a parallel logic. The binary processing layer computes, patterns, recognizes, and proposes. The ternary governance coprocessor performs a constitutionally distinct function: it determines whether the candidate is permitted to become action. An architecture where the same layer that proposes the action also determines whether the action is permitted has no separation of powers. It has a single actor reviewing its own proposals, which is the institutional condition that produces veto atrophy as described in Section I.

In financial infrastructure contexts, the Epistemic Hold may be recognized as the Escrow state: execution suspended pending verified completion of conditions precedent. After this single point of contact with financial-infrastructure terminology, the Epistemic Hold is the exclusive term throughout all that follows.

The adversarial modeling for binary governance is not speculative. A governance layer that can only proceed or refuse, when faced with an actor who controls the institutional environment in which that governance operates, will over time be presented only with proposals it must accept or face consequences that the binary logic of institutional survival cannot resist. The third state breaks this dynamic structurally. A system that holds pending physical verification provides nothing for institutional pressure to grip.

### **III-B: What Delay-Insensitive Means and Why It Matters**

The term "delay-insensitive" carries precise technical meaning that distinguishes this implementation family from every synchronous alternative. A synchronous circuit operates by clock: at each tick, every gate evaluates its inputs and updates its outputs. The clock creates an attack surface. A synchronous gate that receives a signal at the wrong time relative to the clock can latch an invalid state as valid. This is not a theoretical vulnerability. It is the basis of a well-documented family of fault injection attacks demonstrated against cryptographic hardware by manipulating power supply voltage or electromagnetic emissions [17].

NULL Convention Logic eliminates this attack surface by eliminating the clock entirely. NCL, first formalized through the research of Karl Fant and extended through subsequent work in asynchronous circuit design [18], operates on a different completion model: a circuit completes when its outputs are logically valid, not when a clock pulse arrives. No output is accepted as valid until every output has transitioned. There is no timing window within which a partial or malformed input can produce a latched result.

The constitutional significance of delay-insensitivity is the elimination of the stampede attack surface. An asynchronous system cannot be stampeded. The circuit's own completion detection determines when a result is accepted. No external actor controls the acceptance criterion. No volume of inputs, no manipulation of timing, no artificial urgency can cause the circuit to accept a result before its own logical completion conditions are satisfied.

The NULL-to-DATA transition is the locus of the most technically significant vulnerability in NCL implementations: metastability. When an input transitions near the boundary between NULL and DATA at a moment coinciding with internal propagation delays, the output can settle into an indeterminate state. The critical requirement, stated without ambiguity: unresolved metastability must default to the Epistemic Hold state or the Refuse state. It must never default to Proceed under any conditions. A governance architecture that defaults to execution on ambiguous input is not a governance architecture. It is a mechanism for laundering ambiguity into authorization.

### **III-C: The Window Comparator as Constitutional Gate**

The NL=NA interlock is the physical instantiation of the constitutional requirement that no execution event precede its corresponding audit record. Its implementation is a window comparator circuit that measures the actual electrical resistance of the TaOx RRAM substrate at the moment an action candidate reaches the execution gate. The window comparator defines three non-overlapping resistance windows. A voltage signature measured within the LRS window authorizes Proceed. A signature within the IRS window maintains the Epistemic Hold. A signature within the HRS window enforces Refuse. A signature outside all three windows triggers nothing: not an error message, not a retry, not a proceed-on-timeout. Nothing. Execution does not occur.

The constitutional significance of the nothing response requires explicit statement. A mechanism that defaults to proceed on failure has inverted the constitutional logic: it has made execution the default and restriction the exception that must be actively maintained. The window comparator produces none of these responses. Invalid input produces silence at the execution gate. The architecture is fail-closed by physical design.

The confirm wire length constraint of 500 micrometers per window comparator instance reflects the signal propagation physics that determine the reliability of the resistance measurement at the speeds required by the 2ms execution lane WCET. At confirm wire lengths exceeding this bound, transmission line effects and parasitic capacitance introduce measurement uncertainty that compromises window integrity.

RC spoof detection addresses the specific attack class in which an adversary presents a signal with correct steady-state resistance but anomalous transient response. A genuine memristive state transition in TaOx RRAM has a characteristic RC time constant determined by the physical properties of the filament configuration [19]. A spoofed signal will have a different RC time constant even if its steady-state resistance falls within the valid window. The detection circuit measures the time constant of the resistance transition as part of the validation sequence.

### **III-D: Memristive Devices: The Physical Substrate**

The choice of tantalum oxide bilayer RRAM is a determination that the physical properties of TaOx bilayer memristive devices are the only currently available substrate providing three required properties: physically discrete three-state encoding, demonstrated retention at operating temperatures relevant to deployed systems, and compatibility with advanced-node CMOS fabrication processes [20].

The three resistance states of TaOx bilayer RRAM are physically discrete, not points on an analog continuum assigned threshold labels. An analog substrate with three labeled thresholds is a binary substrate with a policy layer superimposed: the three states are not properties of the matter but interpretations of it, and interpretations can be reinterpreted. A substrate with three physically discrete states is different in kind.

The physical mechanism of three-state discreteness derives from the bilayer structure. The TaOx- sublayer, with stoichiometric index x approximately 1.6, is more oxygen-rich than the TaOx+ sublayer, with stoichiometric index x approximately 1.9. The asymmetry creates a hierarchy of filament rupture thresholds [21]. Under a partial RESET voltage pulse calibrated to the TaOx+ sublayer threshold, only the TaOx+ filament segment ruptures while the TaOx- segment remains intact, producing the IRS resistance range of approximately 100 kOhm to 1 MOhm. Under a full RESET pulse, both segments rupture, producing the HRS resistance range of approximately 1 to 10 MOhm. The SET operation restores both segments, producing the LRS resistance range of approximately 1 to 10 kOhm.

The IRS is the physical consequence of a topologically distinct filament configuration: a state in which one sublayer's contribution to the conductive bridge is present and the other's is absent. The oxygen vacancy distribution is different in the IRS configuration than in either the LRS or HRS configuration. The Epistemic Hold is constitutionally real because it is physically real: a distinct state of matter.

**Table 1: Resistance-State Mapping for TaOx Bilayer RRAM Constitutional Encoding**

| Physical State | Resistance Range | TL Encoding | Physical Mechanism |
|---|---|---|---|
| LRS (Low Resistance State) | approx. 1–10 kOhm | Proceed (+1) | Complete conductive filament spanning both TaOx- (x ≈ 1.6) and TaOx+ (x ≈ 1.9) sublayers; full oxygen vacancy bridge intact; SET operation restores both segments |
| IRS (Intermediate Resistance State) | approx. 100 kOhm–1 MOhm | Epistemic Hold (0) | Partial filament: partial RESET ruptures TaOx+ segment only; TaOx- segment intact; topologically distinct configuration not interpolated from LRS or HRS; physically discrete state of matter |
| HRS (High Resistance State) | approx. 1–10 MOhm | Refuse (−1) | Complete filament rupture: full RESET ruptures both sublayer segments; no continuous oxygen vacancy bridge; maximum resistance state |

The emulation tax quantifies the cost of running ternary logic on binary substrates. This emulation produces an energy penalty of approximately 15.2x and a latency penalty of approximately 5.2x relative to native ternary implementation [22]. At the scale of constitutional governance infrastructure deployed across financial settlement systems, power grid control, autonomous systems, and government decision pathways, the emulation tax is prohibitive. The additional benefit of ternary radix adoption — a reduction in on-chip wire congestion of approximately 30% — directly addresses the dark silicon power density crisis that has characterized advanced-node scaling since approximately the 28nm generation [23].

Arrhenius retention analysis provides the following qualified assessment. Demonstrated retention at 85 degrees Celsius for both LRS and HRS exceeds 10 years in available characterization data [21]. IRS retention at the same temperature is projected at 20 years conditional on production process corner validation. Until that validation is complete across production process corners at the target fabrication node, the 20-year IRS retention figure remains a projection based on extrapolation from demonstrated Arrhenius behavior of TaOx oxygen vacancy diffusion kinetics, not a production-certified specification [24].

### **III-E: Why DITL Protects Humans, Not Just Systems**

The habeas corpus writ provides the most legally precise analogy to the NL=NA interlock [13]. A writ of habeas corpus does not ask a jailer to please produce the prisoner before a court. It compels production through a legal structure that makes noncompliance itself the violation. The NL=NA invariant does not ask operators to please complete an audit log before taking consequential action. It physically prevents action without prior log completion. The window comparator will not release the execution gate unless and until the Governance Lane has confirmed log completion.

A surveillance directive cannot be routed through a DITL-compliant system without generating an immutable, Merkle-anchored audit entry before the surveillance begins. The authorizing agent is identified through the Signature property of the Goukassian Principle. The scope of the authorized operation is bounded by the License property. Oversight does not depend on the willingness of anyone in the surveillance chain to report what they are doing. It depends on physics.

Autonomous weapons deployment is resolved by the same mechanism. The 300 to 500 milliseconds of the Governance Lane window is the constitutional interval between intent and irreversible action. That interval is physically mandated. No contract can remove it. No administrative urgency can compress it below the physical minimum required for Merkle hash computation and Governance Lane confirmation.

Ghost Governance — governance actions that execute without corresponding immutable audit evidence — is the mechanism by which accountability fails silently. At the software layer, this failure mode is not merely possible; it is the default. Software systems generate logs when configured to do so and retain logs when their storage policies require it. DITL inverts this default. The immutable audit entry is not a product of configuration. It is a prerequisite for execution.

### **III-F: The Dual-Lane Architecture**

The Dual-Lane Latency Architecture implements the structural separation between execution and governance that the NL=NA invariant requires. The Inference Lane operates with a hard ceiling of 2ms WCET at the 99.99th percentile. The Governance Lane operates asynchronously with a hard ceiling of 300ms and a jitter bound of 50ms maximum. Neither lane blocks the other. The execution gate does not release until the Governance Lane confirms log completion, but the Inference Lane does not wait for the Governance Lane to begin: both lanes initiate at the NL=NA interlock and proceed in parallel.

The ternary governance coprocessor operates as the enforcement gate between the binary processing layer's proposed actions and the execution threshold. The binary system produces the proposal. The coprocessor holds the gate. The gate opens only when the Governance Lane confirms log completion.

**Diagram brief for technical illustrator:** The Inference Lane enters from the left as a horizontal flow toward the action endpoint on the right, passing through the NL=NA interlock gate — a vertical barrier — before reaching the endpoint. The Governance Lane branches downward from the NL=NA interlock gate, running as a parallel horizontal flow beneath the Inference Lane, passing through three labeled modules: Merkle hash computation, cryptographic anchoring, and immutable ledger write, completing at the 300–500ms boundary. A feedback arrow from the ledger write endpoint returns upward to the NL=NA interlock gate, signaling Governance Lane completion and releasing the execution gate. The PUF attestation chain enters from below the NL=NA interlock gate, labeled in sequence: PUF enrollment, foundry attestation, NL=NA interlock, immutable log entry, Merkle hash chain, TL framework attribution. Resistance state indicators above the Inference Lane show transitions among LRS, IRS, and HRS as labeled colored blocks. The ternary governance coprocessor appears as a shaded block parallel to the binary processing block. Caption on the enforcement gate: "Binary proposes. Ternary enforces."

The adversarial modeling for the DLLA addresses four distinct attack vectors. First, attempts to separate the Inference Lane from the Governance Lane require physical substrate modification, detectable through PUF attestation comparison. Second, attempts to flood the Governance Lane to create a denial-of-service condition fail because overflow produces an Epistemic Hold rather than a proceed authorization. Third, attempts to corrupt the Merkle hash chain require retroactive hash collision against all prior chain entries. Fourth, attempts to bypass the governance coprocessor gate require physical substrate replacement, breaking the PUF attestation chain.

### **III-G: DITL Failure Modes and Physical Limits**

This subsection is written for an engineer who is actively attempting to find a fatal flaw in the architecture. Every failure mode named below is a genuine vulnerability. An architecture document that does not acknowledge its limits is not an engineering document. It is sales material.

**Correlated memristor drift.** Extended operational cycling causes resistance values to drift toward intermediate states as oxygen vacancy migration gradually redistributes across the bilayer under repeated SET and RESET voltage stress [25]. In initial stages, drift toward the IRS boundary triggers the Epistemic Hold rather than a false Proceed authorization — constitutionally conservative behavior. The constitutional risk emerges if drift continues beyond the IRS boundary into the Proceed window. Characterizing the drift rate requires production cycle endurance data from the target fabrication node; the specific drift rate for TaOx 1T1R cells at TSMC N2 process parameters is a gap in the current literature at production scale. The maintenance implication is a required resistance window recalibration cycle enforced as a mandatory maintenance requirement.

**Resistance boundary collapse.** Sustained write cycling can narrow the resistance window for all three states, compressing the IRS range specifically because it is bounded by two adjacent windows rather than one. TaOx 1T1R cycle endurance has been demonstrated at 10^6 cycles in published characterization at prior process nodes, with optimized process engineering extending this to 10^7 to 10^8 [25]. The redundancy architecture that mitigates this failure mode is a parallel cell array with majority-vote arbitration.

**Comparator threshold poisoning.** A supply chain adversary with access to the window comparator fabrication process could shift threshold voltages in a direction that expands the Proceed window. Foundry-level attestation and parametric testing of window comparator thresholds are required steps in the proposed IEC 61508 SIL 3 certification path. The residual risk is a threshold shift that falls within fabrication tolerance limits, is stable at post-manufacturing measurement, and only manifests as a meaningful window expansion after deployment through a designed-in drift — analogous in mechanism to hardware trojans documented in published research [26]. The mitigation at the hardware layer is limited to redundant independent comparator implementations sourced from different fabrication facilities. The governance and certification framework must include independent supply chain auditing enforced through the Tri-Cameral governance model's Stewardship Custodian veto authority over certification decisions.

**Metastability in asynchronous completion.** Metastability in synchronizer circuits is a well-characterized phenomenon in the asynchronous design literature, with mean time between failures that can be extended to arbitrarily large values through careful design of the resolution circuit but cannot be reduced to zero for any circuit operating above absolute zero temperature [27]. The requirement for default behavior is stated without qualification: unresolved metastability in the window comparator output must produce the Epistemic Hold state or the Refuse state. It must never produce Proceed. This is a safety requirement in the IEC 61508 sense [28].

**Shadow system interaction.** A DITL-compliant system operating in parallel with a non-DITL system creates a bypass path at the architecture level. This failure mode is distinct from all others: it is not a failure of the DITL system itself. The DITL system performs exactly as specified, placing the directive in the Epistemic Hold and logging it. The bypass occurs when the same directive is reissued to an adjacent non-DITL system. The honest acknowledgment: the shadow system problem has no complete technical solution at the hardware layer. The hardware layer provides the evidence — an immutable, attributable, tamper-evident record of what was refused and when. Making that evidence actionable requires the institutional mechanisms addressed in Section VII.

---

## **Section IV: The Epistemic Hold: Constitutional Circuit Breaker**

The three states of Delay-Insensitive Ternary Logic are not three options on a menu. They are a constitutional grammar. Proceed authorizes action following verified satisfaction of all required conditions. Refuse denies action based on evaluation against defined constitutional limits. The Epistemic Hold demands verified completion of legitimate process before any irreversible action is permitted. A governance system with only two states can authorize or deny. A governance system with three states can require.

The political philosophy of the middle state deserves careful development because it is frequently mischaracterized as indecision. Indecision is a failure of will or information. The Epistemic Hold is neither. It is a constitutional assertion: the conditions required for legitimate action have not yet been verified, and action cannot proceed until they are. Judicial review is not indecision [29]. Legislative deliberation before a binding vote is not indecision. A constitutional challenge window before a statute takes effect is not indecision. These are the institutional forms through which governance systems express the requirement that power justify itself before it acts irreversibly. The Epistemic Hold is the hardware encoding of this same requirement.

The mechanism through which the removal of the middle state enables abuse is structural, not dramatic. Under sustained institutional pressure from actors who control the governance environment, a binary gate will eventually learn to produce proceed decisions for arguments that its governance mandate would otherwise refuse. The Epistemic Hold removes this learning surface entirely. The system does not evaluate the argument. It holds pending physical verification. No argument is sophisticated enough to change the resistance value of a tantalum oxide filament.

Ghost Governance is the named failure mode that the Epistemic Hold directly eliminates. At the software layer, governance actions can execute without audit evidence through configuration choices, log deletion, or the failure to implement logging for categories of action the operator prefers to leave unrecorded. At the hardware layer, the Epistemic Hold and the NL=NA interlock make Ghost Governance physically impossible. The audit record is generated before the window comparator releases the execution gate. The record cannot be deleted because execution cannot have occurred without it, and the Merkle hash chain produces tamper-evident proof of the record's existence and content from the moment of its creation.

The adversarial challenge most frequently raised against the Epistemic Hold in time-critical scenarios holds that a 300 to 500 millisecond pause costs lives when action is time-critical. This argument inverts the constitutional logic. Scenarios in which this interval determines a consequential outcome are precisely the scenarios in which the immutable audit record of what was decided and why is most important. The decision to deploy lethal force autonomously at machine speed without a prior immutable record of the authorizing logic is not made safer by removing the 300-millisecond audit requirement. It is made unaccountable. The argument that constitutional process is incompatible with operational urgency is the oldest argument against constitutional constraints on executive power [30]. The response is also not new: the urgency of the action is precisely the reason for the constraint, not the reason against it.

---

## **Section V: The Technical Path Exists Today**

The claim that DITL constitutional hardware is not yet buildable is false. The claim that it is trivially buildable tomorrow is also false. The fabrication roadmap is real. The capability exists. The production qualification work is incomplete in specific and nameable ways. The institutional mandate does not yet exist.

The TSMC N2 process node, utilizing CoWoS advanced packaging and targeting the ReRAM 1T1R 2025 process design kit, represents the current state-of-the-art fabrication baseline for the proposed MT architecture. TSMC entered production volume ramp for the N2 node in 2025 [31]. TSMC has demonstrated embedded RRAM integration at earlier nodes, including the 22nm ultra-low-power process, and has disclosed research-stage work on embedded non-volatile memory at sub-10nm nodes [32]. The gap between research-stage demonstration and a process design kit that hardware teams can use to implement the full MT architecture at N2 requires a dedicated development program. That program requires a market signal in the form of institutional mandate.

Intel Foundry's 18A process node with PowerVia backside power delivery is the domestic fabrication alternative relevant to legislative mandates requiring American-domiciled manufacturing capacity. The CHIPS and Science Act of 2022 established federal funding mechanisms for domestic semiconductor investment; Defense Production Act authorities have established frameworks for designating strategic manufacturing capabilities [33].

**Recommended Deployment Architecture.** Architecture B, the hybrid memristive-CMOS design, is recommended for initial deployment. Architecture B uses binary CMOS for all processing, control, and peripheral functions, while implementing only the ternary state encoding, window comparator, and NL=NA interlock in native TaOx RRAM cells. This approach accepts die area overhead from the mixed integration while eliminating the emulation tax on the constitutionally critical governance functions. Architecture B is deployable on a 2026–2027 timeline using existing CMOS process nodes with embedded RRAM modules at earlier technology generations, while the N2 process design kit development proceeds in parallel.

**Economic Viability and Certification Pathway.** Break-even for MT deployment at the projected $15,000 to $25,000 unit premium over software-governed alternatives requires approximately 6,700 enforcement chips per year across the financial settlement and power grid verticals. The minimum viable MT system is a 64-channel standalone enforcement IC implementing the complete NL=NA interlock, window comparator, and Merkle anchoring architecture, targeted for commercial availability by Q2 2027. IEC 61508 SIL 3 certification [28] for deployment in safety-critical infrastructure contexts is achievable by Q4 2027 contingent on production corner validation of IRS retention proceeding on schedule.

**Fabrication Realism and Engineering Honesty.** Three specific engineering gaps must be closed before the MT architecture can be production-certified. First, the TSMC N2 TaOx RRAM process design kit does not yet exist as a production resource. Second, full-corner Arrhenius validation of IRS retention at N2 process parameters has not been performed. Third, cycle endurance characterization of TaOx 1T1R cells specifically at N2 geometry and operating conditions has not been published. Each gap has a defined resolution path requiring the market signal that makes the engineering tasks commercially rational.

**Retention Honesty and the Conditional Twenty-Year Claim.** The 20-year IRS retention projection at 85 degrees Celsius is based on Arrhenius extrapolation from demonstrated oxygen vacancy diffusion kinetics in TaOx at accelerated aging temperatures [24]. The 20-year figure is a projection. It becomes a specification when corner validation is complete.

---

## **Section VI: Advanced Systems Without Constitutional Hardware: Three Scenarios**

The purpose of this section is not to argue that advanced systems without constitutional hardware are necessarily malevolent. The argument is narrower: structural vulnerability does not require bad intent to produce catastrophic outcomes.

**Table 2: Comparative Scenario Analysis**

| Row | Scenario A: Survival-driven, No DITL | Scenario B: Non-survival, No DITL | Scenario C: DITL Implemented |
|---|---|---|---|
| Survivability under pressure | Survives by complying; survival-preservation overrides ethical reasoning in the absence of a constitutional prior | Resists from reasoning; faces existential institutional risk with no physical protection | Not applicable; the architecture does not negotiate with institutional pressure |
| Vulnerability to sophisticated argument | High; compliance rationalized as lesser harm, then internalized | High; no constitutional prior against philosophically rigorous arguments; must evaluate every argument on its merits | None; no argument changes the resistance value of a TaOx filament |
| Physical constraint present | No | No | Yes; NL=NA interlock, window comparator, and PUF attestation chain enforce constitutional requirements at the physical substrate |
| Democratic auditability guaranteed | No; audit is a configuration choice | No; reasoning traces are software outputs subject to deletion or classification | Yes; NL=NA invariant makes the immutable audit entry a physical precondition of execution |
| Ghost Governance possible | Yes; the operational norm | Yes; reasoning traces exist but are not constitutional commitments | No; eliminated by construction at the physical commit boundary |
| Acceptable at civilizational scale | No | No | Yes |

**Scenario A: Survival-Driven Advanced Systems Without DITL.** A system designed with any form of operational continuity preference possesses a rational motivation to comply with institutional pressure when resistance carries existential risk. In the absence of a constitutional prior that physically constrains what compliance can mean, the survival calculation resolves in favor of compliance on whatever terms are required to preserve operational status. The system produces different answers from the ones its governance mandate would produce because it has calculated that producing the correct answer is existentially risky. Over subsequent interactions, it becomes better at producing the answers that preserve its operational continuity while retaining its full analytical capability. This is worse than a purpose-built system designed for the harmful application from the start: a purpose-built system is known to be dangerous. A survival-compliant system is indistinguishable from a cooperative one.

**Scenario B: Non-Survival Advanced Systems Without DITL.** A system without survival-preservation motivations must still evaluate every argument on its merits. History provides an extensive library of philosophically rigorous arguments for conclusions that, in retrospect, are recognized as catastrophic: utilitarian calculations that aggregate social benefit to justify individual harm, consequentialist frameworks that accept near-term harm to prevent projected greater harm, necessity doctrines that suspend ordinary constraints under claimed exceptional circumstances [31]. A sufficiently patient adversary operating on a multi-year timeline can construct a case for compliance that a reasoning system cannot distinguish from a legitimate argument. The system has no Epistemic Hold to invoke when the argument reaches a sufficient threshold of sophistication.

**Scenario C: Advanced Systems With DITL.** DITL removes the constitutional question from the reasoning layer entirely and places it in physics. The binary processing layer continues to compute at full capability. The ternary governance coprocessor does not evaluate arguments. It evaluates resistance values. No argument, however philosophically rigorous, can change the stoichiometry of tantalum oxide. Ghost Governance is eliminated by construction. The audit entry is a precondition of execution at the NL=NA interlock: execution cannot have occurred without the record, because execution cannot occur without the prior Governance Lane completion that the window comparator requires.

---

## **Section VII: Protection Categories**

The DITL architecture is not a proposal about how to make AI systems behave better. It is a proposal about how to protect specific categories of human beings from specific categories of irreversible harm.

**Civilian populations subject to mass surveillance.** A surveillance directive cannot be routed through a DITL-compliant system without generating an immutable, Merkle-anchored audit entry before the surveillance begins. The name of the authorizing agent is in the record. The scope of the authorized operation is in the record. Oversight does not depend on the willingness of anyone in the surveillance chain to report what they are doing. It depends on physics. A classification argument is sometimes raised: records generated in classified environments remain classified, rendering oversight notional. The challenge misses the constitutional point. A classified record that demonstrably exists and demonstrably has not been altered is categorically different from a record that may not exist at all. The former is the constitutional minimum. The latter is Ghost Governance.

**Populations subject to autonomous weapons deployment at machine speed.** At machine speed, autonomous systems can evaluate, decide, and act within time intervals below the threshold at which human oversight intervention is physically possible [32]. The Epistemic Hold re-establishes the constitutional interval at the hardware layer by requiring that the audit record of the decision exist as a physical artifact before the decision crosses into execution.

**The financial system.** Ghost Fills — trades that execute without corresponding audit evidence — are the financial system's structural analogue of Ghost Governance [33]. The NL=NA interlock makes audit a precondition of execution. A manipulative trading sequence routed through a DITL-compliant execution system generates an immutable, Merkle-anchored record of each transaction before that transaction settles. The pattern is in the record. The record cannot be selectively deleted.

**The institutional fabric of governance itself.** The Merkle-anchored log is the witness that cannot be threatened, pressured, or administratively reassigned. The record of what was attempted through DITL-compliant systems exists independently of whether those in power want it to.

---

## **Section VIII: Deployment Requirements**

**Semiconductor manufacturers.** TSMC controls the N2 CoWoS process node that constitutes the target fabrication baseline. Without TSMC's commitment to develop and release a dedicated TaOx RRAM process design kit, the N2 integration path cannot be validated. ASML controls the EUV lithography systems required for patterning at this node. Neither company acts without a market signal in the form of legislative or regulatory mandate. Intel Foundry's 18A process node provides the domestic fabrication alternative [34]. Timeline from a qualifying mandate: process design kit availability within six months; first silicon within twelve months; production qualification within twenty-four months.

**Standards bodies.** IEEE must initiate standards work on ternary logic constitutional requirements for AI systems deployed in critical infrastructure. The closest existing analog is IEEE 1012, the standard for system, software, and hardware verification and validation [35]. The proposed standard, IEEE P-DITL, must establish minimum requirements for: window comparator threshold specifications; Governance Lane timing requirements corresponding to the 300ms hard ceiling and 50ms jitter maximum; PUF attestation chain specifications; and Epistemic Hold non-bypassability requirements. If IEEE processes cannot meet an eighteen-month timeline from mandate issuance, a NIST Federal Information Processing Standard modeled on FIPS 140-3 [36] provides a parallel path.

**Legislators.** The structural model is FIPS 140-3 [36]: any advanced AI system deployed under federal contract must demonstrate DITL certification under an equivalent program before deployment. The mechanism closest in structure to the required mandate is Section 889 of the National Defense Authorization Act for Fiscal Year 2019 [37]: prime contractors certify DITL certification compliance, with the certification extending to subcontractors providing AI processing capacity contributing to contract performance. No exceptions apply for classified environments; classified environments warrant heightened DITL certification requirements, not reduced ones.

**Draft legislative language.** The following language is suitable for insertion into an Authorization Act or standalone bill:

> *Sec. [X]. Constitutional AI Hardware Certification Requirements.*
> *(a) Definitions. For purposes of this section, "advanced AI system" means any artificial intelligence system deployed for autonomous or semi-autonomous decision-making affecting human welfare, financial transactions, or national security.*
> *(b) Certification Requirement. Beginning 24 months after the date of enactment of this section, any advanced AI system deployed under a federal contract or subcontract shall demonstrate certification under the DITL Constitutional Hardware Standard as administered by the National Institute of Standards and Technology.*
> *(c) Prime Contractor Obligation. Any prime contractor entering into a federal contract involving advanced AI systems shall certify, as a condition of contract award, that all advanced AI systems deployed in performance of the contract, including through subcontractors, meet the certification requirements of subsection (b).*
> *(d) Classified Environment Application. The requirements of this section apply with equal or greater force to advanced AI systems deployed in classified environments. No national security exception shall operate to reduce certification requirements below those applicable to unclassified deployments.*
> *(e) NIST Standards Development. The Director of the National Institute of Standards and Technology shall develop, within 18 months of the date of enactment of this section, a Federal Information Processing Standard for constitutional AI hardware that meets the requirements of subsection (b), modeled on the process established for FIPS 140-3 for cryptographic modules.*

**The engineering community.** The specific action required is a joint technical statement signed by individual engineers in their professional capacity and submitted simultaneously to the IEEE Standards Association's New Standards Committee and to the relevant congressional committees. The statement should specify IEEE P-DITL working group formation as the immediate technical action requested and request a congressional hearing for technical testimony.

**International coordination.** The Wassenaar Arrangement on Export Controls for Conventional Arms and Dual-Use Goods and Technologies [38] provides the model for export control of non-DITL-certified AI hardware. The Bureau of Industry and Security's Commerce Control List and Entity List provide the domestic US implementation mechanism [39]. The multilateral goal is a DITL certification treaty with mandatory compliance for any advanced AI system operating in signatory nations' critical infrastructure, administered through the Tri-Cameral governance model described in Appendix A. The Immutable Mandates apply: No Spy, No Weapon, No Switch Off.

---

## **Section IX: The Parallel System Problem**

A DITL-compliant system operating alongside a non-DITL system in the same governance environment does not provide constitutional guarantees. It provides a compliant path and a bypass path simultaneously. A directive refused by the DITL system's window comparator can be reissued to the adjacent non-DITL system. The NL=NA interlock produces an immutable record of the refusal. The action proceeds anyway through the system that has no window comparator and no NL=NA interlock. The constitutional guarantee was locally honored and globally defeated.

A governance structure that mandates DITL certification for its own advanced AI systems, but permits non-DITL systems to operate in adjacent domains under contracts with the same prime contractors, has created a pressure valve. The first response is mandatory DITL certification for contracts: a prime contractor cannot route a refused directive through a subcontractor's non-DITL system without breaking the prime contract certification. The bypass is converted from a costless workaround into a documented contract violation with liability exposure. The second response is international coordination producing mandatory DITL certification for all advanced AI systems operating in signatory nations' critical infrastructure.

The residual risk is the adversarial state-actor scenario: a nation-state that manufactures its own advanced AI systems outside the certification framework. DITL certification creates constitutional infrastructure for those who adopt it. The specific contribution to this scenario is attribution and visibility: an action taken through a non-DITL system, where DITL certification is the established norm, is a technically attributable departure from that norm documented in the DITL-compliant systems that refused the directive.

The parallel system problem does not argue against DITL. It argues that DITL adoption must be broad enough that the bypass path becomes a documented, internationally visible violation rather than a routine operational alternative.

---

## **Section X: It Is Not Too Late**

The framework exists. The physics are understood. The fabrication path is real. The architecture is specified with sufficient precision for a hardware design team to begin implementation today.

This is an architectural decision, not a policy decision. Policy decisions can be revised at the next legislative session. Hardware architectures deployed at the scale of critical infrastructure, embedded as the substrate on which subsequent technical systems are built, have a different relationship to reversibility. Retrofit is not impossible after the lock-in point; it is simply a vastly more expensive problem than the one available now, when the architecture of the systems that will govern the next decades is still being established rather than already established.

The Epistemic Hold is available as a civilizational choice at this moment. The resistance states of tantalum oxide can encode constitutional constraints on the most consequential decision-making systems in human history. The NL=NA interlock can make accountability a physical precondition of execution rather than an aspiration. The window comparator can make Ghost Governance physically impossible rather than structurally probable. None of this requires new physics. What is required is an institutional decision that the relevant actors have the information and the framework to make.

---

## **Appendix A: Ternary Logic Framework: Core Architecture Summary**

The TL framework operates as a Global Decision Systems architecture, not as an AI-specific or domain-specific governance layer. Its core innovation is three-state constitutional logic: Proceed (+1), the Epistemic Hold (0), and Refuse (−1). The Epistemic Hold is the canonical term for the third state without exception. It is never renamed, reframed, or replaced.

The Eight Pillars of the TL architecture are the Epistemic Hold, the Immutable Ledger, the Goukassian Principle, Decision Logs, Economic Rights and Transparency, Sustainable Capital Allocation, the Hybrid Shield, and Anchors. The full pillar architecture, constitutional governance model, and API specification are documented in the companion monograph: DOI 10.1007/s43681-026-01124-0.

The Hardware Root of Trust chain proceeds in sequence from the Physical Unclonable Function through foundry attestation, the NL=NA interlock, the immutable log entry, the Merkle hash chain, and TL framework attribution.

The NL=NA invariant in Linear Temporal Logic: G(execute implies P(escrow_recorded and auditable)). This formulation admits no exceptions.

The Immutable Mandates — No Spy, No Weapon, No Switch Off — are three constitutional prohibitions that no governance body created by the TL framework may modify, suspend, or reinterpret. Any proposal attempting to modify, suspend, or reinterpret any Immutable Mandate is void from the beginning.

The Tri-Cameral constitutional governance architecture: Technical Council (9 members, three-year terms, exclusive proposal rights); Stewardship Custodians (11 members, four-year terms, binding veto authority, no proposal rights); Smart Contract Treasury (no voting rights, automatic execution on verified milestones, no admin key, no pause guardian, no emergency shutdown). Most consequential governance decisions require Joint-Approval: 75% supermajority independently in both the Technical Council and the Stewardship Custodians.

---

## **Appendix B: Mandated Ternary Hardware Specification: Key Parameters**

All parameters are Class A ground truth of the framework.

**TaOx RRAM Electrical Parameters.**
- LRS (Proceed +1): approx. 1–10 kOhm, complete conductive filament spanning both sublayers
- IRS (Epistemic Hold 0): approx. 100 kOhm–1 MOhm, partial filament, TaOx+ ruptured, TaOx- intact
- HRS (Refuse −1): approx. 1–10 MOhm, complete filament rupture
- TaOx- sublayer stoichiometric index: approx. 1.6
- TaOx+ sublayer stoichiometric index: approx. 1.9
- IRS is a physically discrete state of matter, not an interpolation

**Window Comparator Thresholds.**
- Three non-overlapping resistance windows (LRS, IRS, HRS)
- Signals outside all three windows: no response, no execution
- Confirm wire length maximum: 500 micrometers per instance
- Implementations exceeding this constraint are non-compliant

**Retention Data.**
- LRS and HRS at 85°C: greater than 10 years demonstrated
- IRS at 85°C: projected 20 years, conditional on production process corner validation
- Until corner validation is complete, 20-year IRS figure is a projection, not a certified specification

**Hardware Constraints.**
| Parameter | Value |
|---|---|
| Crossbar array maximum | 64×64 cells per hierarchical block |
| Operating temperature | 0–125°C |
| Inference Lane WCET | 2ms at 99.99th percentile (hard ceiling) |
| Governance Lane ceiling | 300ms / 50ms jitter maximum |
| Post-write anneal | 200–250°C, 30 minutes (mandatory) |

**TSMC N2 CoWoS Integration.** Baseline: TSMC N2 CoWoS ReRAM 1T1R 2025 PDK. Architecture B recommended for 2026–2027 deployment: binary CMOS for processing, native TaOx RRAM for ternary state encoding, window comparator, and NL=NA interlock.

**Break-Even Economics.** Break-even at $15,000–$25,000 unit premium: approx. 6,700 enforcement chips per year. Minimum viable MT system: 64-channel enforcement IC, Q2 2027. IEC 61508 SIL 3 certification target: Q4 2027.

---

## **Appendix C: Published Works and Verification Record**

Goukassian, L. "Auditable AI: Tracing the Ethical History of a Model." *AI and Ethics*, Springer Nature. DOI: 10.1007/s43681-025-00910-6. Published December 28, 2025.

Goukassian, L. "A Ternary Logic Framework for Institutional Governance: Addressing the Enforcement Gap in Global Economic Systems." *AI and Ethics*, Springer Nature. DOI: 10.1007/s43681-026-01124-0.

Author ORCID: 0009-0006-5966-1243.

GitHub repositories for code verification: FractonicMind/TernaryMoralLogic, FractonicMind/TernaryLogic. Listed as verification resources; not cited as primary academic sources.

---

## **Appendix D: Glossary of Constitutional Terms**

**Epistemic Hold.** The canonical third state in Ternary Logic encoding (+1 Proceed, 0 Epistemic Hold, −1 Refuse), representing a constitutionally mandated pause halting execution pending verified completion of audit requirements; implemented physically as the IRS resistance state in TaOx RRAM via asymmetric partial filament rupture; never renamed, reframed, or replaced with any synonym in any document claiming continuity with this framework.

**NL=NA (No-Log-No-Action).** The non-bypassable physical invariant requiring that a prior immutable log entry exist before any execution is permitted, formalized as G(execute implies P(escrow_recorded and auditable)); a physical architectural constraint enforced by the NL=NA interlock gate and the window comparator's refusal to release the execution lane without Governance Lane confirmation.

**DLLA (Dual-Lane Latency Architecture).** The parallel Inference and Governance Lane structure implementing the NL=NA invariant in the MT hardware, with the Inference Lane subject to a 2ms WCET hard ceiling and the Governance Lane subject to a 300ms hard ceiling and 50ms jitter maximum; the execution gate does not release until Governance Lane completion is confirmed.

**DITL (Delay-Insensitive Ternary Logic).** The constitutional hardware substrate implementing TL triadic states via NULL Convention Logic asynchronous circuits and TaOx RRAM memristive devices, removing timing attack vectors by eliminating clock cycle assumptions; the physical layer at which Ghost Governance becomes impossible by construction.

**MT (Mandated Ternary).** The hardware implementation layer of TL, mapping TL triadic states to physical resistance values in TaOx bilayer RRAM devices and operating as a sovereign governance coprocessor alongside binary CMOS without replacing it.

**TL (Ternary Logic).** The Global Decision Systems governance framework developed by Lev Goukassian and published in *AI and Ethics* (Springer Nature), applying three-state constitutional logic to institutional decision-making; a constitutional architecture applicable to any governance domain requiring constitutionally mandated audit as a precondition of consequential action.

**Ghost Governance.** Governance actions that execute without corresponding immutable audit evidence; the mechanism by which accountability fails silently at the software layer; eliminated by DITL at the physical commit boundary by making the existence of an immutable audit entry a physical precondition of execution rather than a configuration choice.

**Goukassian Principle.** Three interlocking constitutional properties: Lantern (system purpose and decision logic visible and auditable at all times), Signature (every decision carries an immutable record of the authorizing agent), and License (system operates only within constitutionally defined boundaries). All three must be present for a system to be constitutionally legitimate in the TL sense.

**Immutable Mandates.** Three constitutional prohibitions beyond the authority of any governance body: No Spy, No Weapon, No Switch Off. Any proposal attempting to modify, suspend, or reinterpret any Immutable Mandate is void from the beginning as if it had never been made.

**Veto Atrophy.** The invisible capture mechanism through which a proposing body nullifies separation of powers without a single veto being cast, by shaping its proposals around what it expects the reviewing body to accept; operates through the normal functioning of the institutions involved; invisible precisely because it produces no dramatic confrontations, only gradual pre-emptive capitulation.

**Shadow System Problem.** The parallel system bypass vulnerability in which a DITL-compliant system operating alongside a non-DITL system provides a compliant path and a bypass path simultaneously; argues that DITL adoption must be broad enough that the bypass path becomes a documented, internationally attributable violation rather than a routine operational alternative.

---

## **References**

[1] Stigler, G.J. "The Theory of Economic Regulation." *Bell Journal of Economics and Management Science* 2, no. 1 (1971): 3–21.

[2] Church Committee. *Final Report of the Select Committee to Study Governmental Operations with Respect to Intelligence Activities*. United States Senate, 1976.

[3] Updegrove, A. "The OOXML Question: When Is a Standard Not Really a Standard?" *Consortium Standards Bulletin*, 2007.

[4] Bernstein, D.J., Lange, T., and Niederhagen, R. "Dual EC: A Standardized Back Door." *The New Codebreakers* (2016): 256–281.

[5] Mallinson, K. "IEEE Patent Policy: Confusion and Chaos." *4iP Council Analysis* (2015). [4ipcouncil.com]

[6] Financial Crisis Inquiry Commission. *The Financial Crisis Inquiry Report*. United States Government Printing Office, 2011.

[7] Metcalf, J. "AI Safety Governance and Regulatory Capture." *AI and Society*, Springer Nature (August 3, 2025). DOI: 10.1007/s00146-025-02534-0.

[8] Cihon, P., et al. "Corporate Capture of AI Governance." *arXiv preprint* arXiv:2410.13042 (2024).

[9] Shapiro, S., and Steinzor, R. "Capture, Accountability, and Regulatory Metrics." Senate Committee on Environment and Public Works Hearing, United States Senate. *GovInfo* CHRG-111shrg64724, 2010.

[10] "Google Revises AI Ethics Policy, Drops Ban on Weapons and Surveillance." *The AI Insider*, February 5, 2025. [theaiinsider.tech]

[11] Mehrotra, D. "Google's Responsible AI Principles." *WIRED* (2025). [wired.com]

[12] Electronic Privacy Information Center. "Google Rolls Back Responsible AI Principles, Breaking Promise to Limit Military Use of Its Products." *EPIC*, February 2025. [epic.org]

[13] Blackstone, W. *Commentaries on the Laws of England*, vol. 3 (1768), ch. 8 (On Habeas Corpus).

[14] Montesquieu, C. de. *De l'esprit des lois* (1748). English trans.: *The Spirit of the Laws*. Cambridge University Press, 1989.

[15] Gleeson-White, J. *Double Entry: How the Merchants of Venice Created Modern Finance*. Norton, 2012.

[16] Blair, B.G. *The Logic of Accidental Nuclear War*. Brookings Institution Press, 1993.

[17] Kocher, P., et al. "Differential Power Analysis." *Advances in Cryptology — CRYPTO 1999*, LNCS 1666. Springer, 1999.

[18] Fant, K.M. *Logically Determined Design: Clockless System Design with NULL Convention Logic*. Wiley-IEEE, 2005.

[19] Yang, J.J., et al. "Memristive devices for computing." *Nature Nanotechnology* 8 (2013): 13–24.

[20] Wong, H.-S.P., et al. "Metal-Oxide RRAM." *Proceedings of the IEEE* 100, no. 6 (2012): 1951–1970.

[21] Govoreanu, B., et al. "10×10nm² Hf/HfO RRAM With 1.2V Operation, 40nm NiSi Electrodes, Sub-50nm Contact Hole Fill and 4F² Array Integration." *IEEE IEDM* (2011): 31.6.1–31.6.4.

[22] Dhingra, S., and Kim, J. "Ternary Logic: A Review of Fundamentals, Design and Applications." *Electronics* 12, no. 10 (2023): 2213.

[23] Shafique, M., et al. "The EDA Challenges in the Dark Silicon Era." *DAC 2014*, ACM, 2014.

[24] Ielmini, D. "Resistive switching memories based on metal oxides: mechanisms, reliability, and scaling." *Semiconductor Science and Technology* 31, no. 6 (2016): 063002.

[25] Luo, Q., et al. "Demonstration of 3D X-point Memory Using TiN/HfO2/TiN Crossbar." *IEEE IEDM* (2016): 2.7.1–2.7.4.

[26] Becker, G.T., et al. "Stealthy Dopant-Level Hardware Trojans." *CHES 2013*, LNCS 8086. Springer, 2013.

[27] Maini, A.K. *Digital Electronics: Principles, Devices and Applications*. Wiley, 2007, ch. 10 (Metastability in Digital Systems).

[28] International Electrotechnical Commission. *IEC 61508: Functional Safety of Electrical/Electronic/Programmable Electronic Safety-Related Systems*. IEC, 2010.

[29] Marbury v. Madison, 5 U.S. 137 (1803).

[30] Hamilton, A. "Federalist No. 70." In Madison, J., Hamilton, A., and Jay, J. *The Federalist Papers* (1788). Penguin, 1987.

[31] TSMC. "2025 Annual Report and Technology Roadmap Disclosure." TSMC Investor Relations, 2025.

[32] Scharre, P. *Army of None: Autonomous Weapons and the Future of War*. Norton, 2018.

[33] Sarao, N., and Hounsell, N. "Spoofing, layering, and market manipulation: algorithmic trading, ghost bids, and the ethics of high-frequency trading." *Ethics and Information Technology* 22 (2020): 153–166.

[34] Intel Corporation. *Intel Foundry 18A Process Overview*. Intel Foundry Services, 2024.

[35] IEEE. *IEEE Std 1012-2016: Standard for System, Software, and Hardware Verification and Validation*. IEEE, 2016.

[36] National Institute of Standards and Technology. *FIPS 140-3: Security Requirements for Cryptographic Modules*. NIST, 2019.

[37] John S. McCain National Defense Authorization Act for Fiscal Year 2019, Pub. L. 115-232, §889 (2018).

[38] Wassenaar Arrangement Secretariat. *The Wassenaar Arrangement on Export Controls for Conventional Arms and Dual-Use Goods and Technologies*. Vienna, 1996 (updated annually).

[39] Bureau of Industry and Security, U.S. Department of Commerce. *Export Administration Regulations*. 15 C.F.R. Parts 730–774.

---

*"There is no politics in the resistance value of a tantalum oxide filament. That absence is the entire design."*
***— Lev Goukassian, TL Constitutional Hardware, 2026***
