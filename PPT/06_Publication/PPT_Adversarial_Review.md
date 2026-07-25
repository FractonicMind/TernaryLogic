# Session 4 — Adversarial Peer Review
## Provisional Permission Token in TL's DLLA: Three Independent Reviewer Challenges

**Review target:** Session 3 academic paper — *"Hardware-Enforced Authorization in Ternary Logic's Dual-Lane Latency Architecture: A Technical Evaluation of the Provisional Permission Token"*

**Review protocol:** Three disciplinary reviewers with distinct challenges. Each reviewer operates independently and reaches an independent verdict. Verdicts are not reconciled. The purpose is adversarial stress-testing before a real peer reviewer reads the manuscript.

---

## REVIEWER 1: Hardware Architect

*Disciplinary perspective: semiconductor design, ASIC/FPGA implementation, physical hardware security, real-world deployment of cryptographic hardware at scale.*

---

### Challenge 1.1 — The C-Element Novelty Problem

The paper claims that TL's Muller C-element is the sole mechanism satisfying TL's hardware-constraint design intent. This claim requires careful unpacking.

The Muller C-element was described in 1959. Its use as a consensus gate in asynchronous circuit design is a textbook technique. NULL Convention Logic (Fant & Brandt, 1996) extended it into a complete logic family. The C-element's physical properties — output held low until all inputs are high — are elementary CMOS behavior. None of this is new.

**What the paper must clarify, and does not sufficiently clarify:** Is TL's novelty claim the *use* of the C-element in an authorization context, or is it the C-element's *integration* with the specific PPT pipeline (SHA-256 → Merkle → HSM signing) as a unified authorization system? The paper gestures at this distinction in the Related Work section but does not state it with the precision a hardware architect requires.

Specifically: an FPGA LUT configured as a C-element (INIT=0xE8E8E8E8E8E8E8E8 in Xilinx RTL) is a trivial, one-line configuration. The C-element itself is not an engineering contribution. The engineering contribution — if it exists — is the *architectural decision* to use it as the physical release gate for authorization, with the HSM signing output as one input and the hardware authorization signal as the other, operating without any software override path. The paper must make this contribution explicit and precise: *the contribution is the integration decision and the resulting architectural property, not the C-element circuit per se*.

**Assessment of this challenge:** If the paper is read by a hardware architect who misses this distinction, it risks being dismissed with the observation "C-elements are 65 years old." The paper needs a crisp one-paragraph statement that preempts this reading. The statement should be: "The Muller C-element is a well-established circuit primitive. TL's contribution is not the primitive itself but its application as a physical authorization gate within the DLLA, with the effect that execution is physically blocked at the circuit level — not at the software policy level — by the absence of a valid PPT. No prior authorization architecture applies this primitive in this way for this purpose."

---

### Challenge 1.2 — The MT Hardware Layer: Specification vs. Silicon

The paper references TL's Mandated Ternary (MT) hardware layer as the physical implementation substrate for the C-element. Section 5 (Hardware Feasibility) presents the MT layer as an architectural specification.

**The challenge:** The paper conflates specification and silicon. The FPGA implementation (Xilinx Versal LUT configuration) is described as demonstrating C-element implementability. But there is a gap between "this LUT configuration instantiates a C-element" and "an MT-compliant hardware layer exists and has been fabricated."

An FPGA-hosted C-element is a *proof of concept* instantiation. It demonstrates that the circuit is realizable in FPGA fabric. It does not demonstrate that the MT hardware layer — as TL specifies it, including dual-rail encoding, hardware watchdog, HSM co-integration, and the full circuit hierarchy — has been manufactured, tested, and validated.

**What the paper must do:** Clearly distinguish between (a) the FPGA LUT configuration, which demonstrates C-element circuit realizability [Demonstrated], and (b) the full MT hardware layer specification, which is an engineering model of how these components would be integrated [Theoretical/Engineering Estimate], and has not been fabricated as an integrated silicon product. Currently, the paper blurs this distinction in ways that could mislead a hardware architect reader into believing more of the MT layer has been physically realized than is the case.

The paper's own evidence taxonomy should enforce this. The C-element RTL is [Demonstrated] for the LUT-level instantiation. The MT hardware layer as a complete integrated system is [Theoretical] / [Engineering Estimate] pending actual silicon fabrication. The paper must enforce this distinction consistently throughout Section 5.

---

### Challenge 1.3 — The Consumer Deployment Path Is Not Credible Without Custom Silicon

The paper states that TL's 10–20 ms consumer PPT target is achievable on Apple Secure Enclave via ECC P-256 signing at approximately 1–5 ms. Then the paper acknowledges that the Secure Enclave is a TEE-based "weaker instantiation" deployment.

**The challenge:** The paper simultaneously claims consumer deployment viability and acknowledges that consumer hardware cannot satisfy TL's hardware-constraint design intent. These two claims, presented together without explicit resolution, create a misleading impression.

A hardware architect reads this as follows: either TL's hardware-constraint design intent is TL's essential contribution (in which case consumer devices cannot implement TL, only a weakened approximation), or TL's essential contribution is accessible without the C-element (in which case the C-element is not essential). The paper must resolve this tension explicitly.

The resolution I recommend: explicitly state that TL defines two implementation tiers. Tier 1 (Full Hardware Constraint): FPGA/ASIC C-element + FIPS HSM; satisfies TL's design intent completely. Tier 2 (Software-Policy-on-Hardware): TEE-based implementations (Secure Enclave, TrustZone, SGX); achieves TL's latency and cryptographic pipeline targets but not the physical authorization gate guarantee. Tier 2 deployments carry the label "weaker instantiation" and must be presented with an explicit security downgrade notice. This two-tier structure needs to be a formal part of TL's specification, not an informal footnote.

---

### Challenge 1.4 — FPGA C-Element SEU Vulnerability Is Under-Specified

Section 7 (Security Analysis) addresses FPGA Single-Event Upset vulnerability in Challenge 6.8 and identifies it as a gap. The paper correctly notes that SRAM-based FPGAs are vulnerable and lists mitigations (scrubbing, TMR, flash-based FPGAs, ASIC).

**The challenge:** For a hardware architect evaluating this paper, the SEU vulnerability in an SRAM-based FPGA C-element is not merely a "gap" — it is potentially a systemic safety failure for any application with safety-critical authorization requirements. An SEU that flips the C-element's LUT configuration could cause the C-element to output high regardless of its inputs, bypassing the authorization gate entirely. This is not a marginal risk; it is a categorical failure mode.

The paper must be more explicit about the severity here: for safety-critical deployments (medical devices, autonomous vehicles, industrial control), an SRAM-based FPGA C-element is not an acceptable implementation without demonstrated SEU protection. Flash-based FPGA (Microchip PolarFire) or ASIC implementation should be specified as *mandatory* for safety-critical deployments, not merely *recommended*.

This is not a minor spec gap. A hardware architect reviewing this for ISO 26262 ASIL-D or IEC 62304 Class C compliance will flag this immediately. The paper should preempt this by specifying it explicitly.

---

### Verdict — Reviewer 1

**Verdict: Major Revision Required before publication.**

The paper makes a technically sound and defensible case for PPT feasibility within TL's architecture. The hybrid FPGA/ASIC C-element + FIPS HSM architecture is realizable today. The warm-path latency figures are credible and consistent with known hardware characteristics. The failure mode taxonomy is thorough.

However, the following revisions are required:

**R1.1** — Add a crisp, explicit statement in Section 4.2 distinguishing the C-element as a known primitive from TL's contribution as the architectural integration decision that applies it as a physical authorization gate. Preempt the "C-elements are old" objection before a reviewer raises it.

**R1.2** — Section 5 must consistently apply the evidence taxonomy to distinguish FPGA LUT-level instantiation [Demonstrated] from the full MT hardware layer as an integrated manufactured system [Theoretical/Engineering Estimate]. The current text is insufficiently precise on this point.

**R1.3** — The two-tier architecture (Tier 1 physical constraint / Tier 2 software-policy weaker instantiation) must be formally defined in the specification and explicitly applied throughout Section 5 and Section 8. Currently, the tiers are acknowledged but not formally structured.

**R1.4** — Section 7 (Security Analysis, hardware fault injection) must be strengthened to state explicitly that SRAM-based FPGA C-element is contraindicated for safety-critical deployments without demonstrated SEU protection. Flash-based FPGA or ASIC must be specified as mandatory (not optional) for ASIL-D and IEC 62304 Class C contexts.

With these revisions, the paper is ready for TechRxiv/SSRN submission.

---

## REVIEWER 2: Cryptographer

*Disciplinary perspective: applied cryptography, side-channel analysis, protocol security, HSM certification standards, post-quantum cryptography.*

---

### Challenge 2.1 — The 50 ms Headline Is a Warm-Path Figure Presented as a General Claim

Section 6.2 of the paper correctly identifies the warm-path/cold-path distinction and states that "TL's 50 ms claim assumes the warm path." However, the Abstract, the Introduction, and the section headings consistently present "under 50 ms" as the PPT latency without qualification.

**The challenge:** A cryptographer or systems engineer reading only the Abstract, Introduction, and conclusions — the parts most likely to be read and cited — receives the impression that TL's PPT can be issued in under 50 ms. The qualification (warm path only; cold path may reach p99 approximately 60 ms) is present in the body but not in the places where it needs to be.

This is an engineering honesty problem, not merely a presentation problem. A 50 ms claim without variance characterization is not an engineering claim — it is a marketing claim. The paper explicitly states in the research protocol that "a headline figure of 'under 50ms' is an engineering claim only when variance is characterized." By that standard, the paper should report the headline figure as "under 50 ms on the warm operational path (mean approximately 5–10 ms, p99 approximately 17 ms); cold-path first-issuance approximately 20–40 ms mean, p99 approximately 60 ms."

**Required revision:** The Abstract must report both warm-path and cold-path figures. The headline "under 50 ms" must be qualified "on the warm path" in every occurrence in the paper's key locations (title, abstract, introduction, conclusions).

---

### Challenge 2.2 — p99 Figures Are Derived Estimates, Not Measured Values

The paper presents p99 latency figures: p99 approximately 17 ms for warm path, p99 approximately 60 ms for cold path. These figures appear in the paper's main latency table without adequate qualification of how they were derived.

**The challenge:** There are no measured HSM latency-vs-throughput curves in this paper. The p99 figures are derived from engineering reasoning applied to published throughput specifications — the paper even acknowledges this in the body ("Published HSM latency-vs-throughput curves at 50%, 80%, and 95% utilization could not be obtained this session"). A cryptographer will note that "p99 ~17 ms" derived from throughput specification arithmetic is not the same as "p99 ~17 ms" measured under operational load on a specific hardware configuration.

The paper's evidence taxonomy should classify these p99 figures as [Engineering Estimate], and this classification must be visible in the table itself, not only in the body text. Moreover, the paper should explicitly state that the p99 figures have not been empirically measured and are subject to revision based on direct hardware testing.

For a cryptographic hardware paper, operational p99 latency is a critical claim. HSMs under load behave differently than their throughput specifications suggest — queuing dynamics, thermal throttling, network congestion, and key management operations can all inflate p99 in ways that pure throughput arithmetic does not capture. The paper must be explicit that the p99 figures are engineering estimates requiring hardware validation.

---

### Challenge 2.3 — The HSM Compromise Analysis Understates the Severity

Section 7.3 correctly identifies HSM compromise as TL's most severe single-point security failure and correctly states that the C-element provides no residual protection against a Byzantine-faulty HSM. The mitigations listed (anomaly detection, key ceremony requirements, dual-HSM cross-validation, hardware attestation chaining) are appropriate.

**The challenge:** The severity framing is understated for the implications it carries. A compromised HSM in TL's architecture does not merely "defeat the cryptographic chain" — it converts TL's physical authorization gate into a credential for a supply chain attacker. An adversary who controls the HSM firmware can issue valid PPTs for any operation, bypassing TL's entire security model silently. The C-element, which is the component most prominently marketed as TL's novel security property, provides zero defense against this.

This means that TL's physical-hardware-enforcement guarantee is contingent on the HSM's software and firmware integrity — which is precisely the kind of software dependency that TL's C-element is architecturally intended to eliminate for the execution gate. The irony deserves explicit acknowledgment: TL's physical hardware gate (C-element) depends for its effective security on the integrity of the HSM's software stack. A compromised HSM renders the physical gate security theater.

**Required statement:** The paper should explicitly acknowledge this architectural dependency: "TL's physical authorization guarantee is a property of the complete system, not of the C-element alone. The C-element's security guarantee is conditioned on the HSM's software and firmware integrity. A Byzantine-faulty HSM converts TL's physical gate into an authorized-execution pathway for any attacker who controls HSM behavior. Dual-HSM cross-validation and multi-party key ceremonies are therefore not merely operational best practices — they are architectural requirements for deployments where the HSM compromise threat model is considered."

---

### Challenge 2.4 — The Post-Quantum Section Is Too Brief

Section 7.2 correctly identifies that ECDSA P-256 has approximately 64-bit quantum security against Shor's algorithm and recommends NIST PQC migration (CRYSTALS-Dilithium / FIPS 204; SPHINCS+ / FIPS 205). This is accurate but handled in three sentences.

**The challenge:** For a paper claiming applicability in high-consequence domains with potentially decades-long operational lifetimes (medical devices, financial infrastructure, autonomous vehicle infrastructure), the post-quantum transition is not a footnote. A deployed TL infrastructure that signs PPTs with ECDSA P-256 today may be expected to remain operational until cryptographically relevant quantum computers exist — a timeline that is contested but not implausible within a 15–20 year horizon.

**Required additions:**
- A statement of the threat timeline: current NIST estimates place cryptographically relevant quantum computers (CRQC) as possible within 10–20 years.
- An assessment of *harvest-now-decrypt-later* risk: an adversary who records TL PPT traffic today could decrypt it retroactively with a future CRQC, undermining the immutability of the audit record.
- A concrete migration path: CRYSTALS-Dilithium (FIPS 204) signatures are approximately 2,420 bytes vs. ECDSA P-256's 64 bytes — a 38× increase in signature size. The HSM pipeline's latency for Dilithium signing (estimated several milliseconds) versus ECDSA is relevant to TL's 50 ms specification. The paper should assess whether the Dilithium signature size and latency are compatible with TL's PPT pipeline.
- A recommendation: TL's specification should include a PQC migration plan as a normative document.

---

### Verdict — Reviewer 2

**Verdict: Major Revision Required before publication.**

The cryptographic analysis is broadly correct — the pipeline claims are consistent with known hardware performance, the attack vectors are appropriately identified, and the security mitigations are consistent with published literature. However, four revisions are required:

**R2.1** — The Abstract and all headline locations must qualify the 50 ms figure as a warm-path figure with explicit p99 characterization. The current presentation does not meet the paper's own engineering claim standard.

**R2.2** — The latency table in Section 6 must display evidence classification ([Engineering Estimate]) inline for p99 figures, with an explicit note that these figures are derived estimates not yet empirically validated against hardware under operational load.

**R2.3** — Section 7.3 (HSM Compromise) must explicitly acknowledge the architectural dependency: TL's physical gate security is conditioned on HSM software/firmware integrity. The phrase "dual-HSM cross-validation is an architectural requirement, not merely an operational best practice" should appear in the paper with appropriate emphasis.

**R2.4** — Section 7.2 (Token Forgery / Post-Quantum) must be expanded to address harvest-now-decrypt-later risk, Dilithium/SPHINCS+ latency and size implications for the PPT pipeline, and a normative PQC migration plan recommendation. Three sentences is insufficient for a paper claiming decade-scale deployment relevance.

With these revisions, the paper is publishable in a peer-reviewed engineering venue.

---

## REVIEWER 3: Distributed Systems Theorist

*Disciplinary perspective: distributed systems theory, formal verification, rollback semantics, transaction processing, prior-art analysis, architectural soundness of claims about novel distributed protocols.*

---

### Challenge 3.1 — "Hardware-Enforced Rollback" Is an Incomplete Claim

The paper consistently refers to TL's "hardware-enforced rollback" as a property of the DLLA architecture. Section 10 (Limitations) acknowledges the externally visible I/O and non-idempotent partial write problems. However, the framing of these as "limitations" understates what is actually a fundamental boundary on the rollback claim.

**The challenge:** TL's hardware-enforced rollback reverts *authorization state* — it moves the system from State 1 back to State 0. This is not the same as reverting *execution state*. The paper uses "rollback" in a way that conflates these two distinct concepts.

In distributed systems, rollback means one of two things: (a) returning to a prior consistent global state (the classic Chandy-Lamport snapshot problem), or (b) executing compensating transactions that undo the logical effects of the rolled-back operations (the Sagas model). TL's hardware `provisionalExpiry` does neither of these. It reverts *authorization*, which is a necessary but not sufficient condition for reverting execution.

**The paper must clarify:** TL's rollback guarantee is an *authorization state rollback*, not an *execution state rollback*. The distinction matters for every application domain. A financial execution that debited an account during the provisional window has debited that account; returning the authorization system to State 0 does not automatically undo the debit. The debit requires a compensating transaction (credit) executed by the application layer. TL's hardware provides the trigger for that compensating transaction (the `provisionalExpiry` event) but not the compensating transaction itself.

This is not merely a limitation to enumerate — it is a fundamental characterization of what TL's rollback guarantee actually is. The paper's core claim that TL provides "hardware-enforced rollback" is misleading unless it is qualified as "hardware-enforced authorization state rollback, triggering application-layer compensation for execution state."

---

### Challenge 3.2 — The Two-Token Pattern Prior Art Case Is Undersold, Then Overclaimed

The paper correctly identifies the prior art for the provisional-then-final two-token pattern (OCC, 2PC, Sagas, Paxos). It correctly frames TL's novelty as the hardware enforcement layer applied to this pattern. 

**The challenge:** The novelty argument then overreaches. The paper states that no prior system combines "A Muller C-element as a physical authorization gate (not merely an asynchronous circuit primitive), an HSM-generated cryptographic provisional token as the gate condition, a hardware watchdog `provisionalExpiry` as a deterministic rollback trigger," etc. This enumeration of five combined properties is then presented as TL's novelty.

But a distributed systems theorist will observe: this list conflates architectural decisions (two-lane separation, unified triadic state model) with implementation choices (Muller C-element, HSM, SHA-256). It is not obvious that the specific choice of a Muller C-element versus any other hardware gate (a simple D flip-flop controlled by the HSM output, for instance) constitutes a fundamental architectural distinction. The paper does not justify why the C-element specifically — as opposed to any hardware-level authorization gate — is the architecturally essential component.

**Required clarification:** The novelty claim should be separated into two claims:
- **Architectural novelty claim:** TL is novel in applying hardware-enforced authorization gating to the provisional-then-final execution pattern within a unified triadic state model, separating authorization latency from finality latency in a single coherent architecture. This claim is defensible.
- **Implementation specificity claim:** TL implements the authorization gate using a Muller C-element because of its specific electrical properties (output held low by pull-down network, no software override path). The Muller C-element is the *best available* implementation of TL's architectural requirement — but the architectural requirement itself is what is novel, not the specific circuit chosen to meet it.

This distinction protects TL's novelty claim from the objection: "You could achieve the same architectural property with a different gate." Yes, you could — and the architectural contribution (separation of authorization latency from finality latency via a hardware gate with no software override) would be equally present. TL's use of the C-element is the implementation choice, not the novelty claim.

---

### Challenge 3.3 — The Governance Lane After Forced State 0 Return Is Unspecified

The formal specification in the Appendix models the C-element state transitions with precision. The TLA+ specification captures the main lifecycle correctly. However, a distributed systems theorist reading the formal model immediately asks: *what happens in Lane 2 (the Governance Lane) when `provisionalExpiry` fires and forces State 0 return?*

The Appendix's TLA+ specification models only the Lane 1 state (system_state, ppt_valid, fpt_valid, timer state). It is a single-component model. In a full DLLA deployment, the FPT is being constructed in Lane 2 during the provisional window. When `provisionalExpiry` fires and Lane 1 returns to State 0:

- Is the in-progress FPT construction in Lane 2 also cancelled?
- If the FPT arrives at Lane 2 after the Lane 1 State 0 return, what is the expected behavior? (The paper specifies that a post-expiry FPT must be rejected — but this is in Section 6 body text, not in the formal model.)
- If Lane 2 is maintaining audit records or external commitments related to the provisional execution, are those records invalidated on State 0 return?

**Required addition to the formal model:** A two-component TLA+ specification modeling the interaction between Lane 1 (the C-element state machine) and Lane 2 (the FPT delivery process), with explicit specification of Lane 2 behavior on `provisionalExpiry` events. At minimum, the paper should explicitly state that the current TLA+ model is a single-component model of Lane 1 only, and that a multi-component model capturing Lane 1/Lane 2 interaction is identified as future work.

Without this, the formal specification is technically correct for what it models but does not cover the distributed system's actual behavior — and a distributed systems reviewer will notice this gap.

---

### Challenge 3.4 — Alternative Architecture Analysis: Were the Competitors Selected to Win or to Lose?

The three alternative architectures (HECA/ARM Morello, DTAS/Threshold ECDSA, PEHI/seL4) are genuine competitors — they are not strawmen. The paper's comparative table is honest about cases where alternatives are preferable (DTAS for multi-party governance, PEHI for cost/simplicity).

**The challenge:** However, the framing of the comparison systematically advantages TL by selecting evaluation dimensions on which TL is designed to excel:
- "Immutable audit trail" — TL has one; the alternatives do not. But is an immutable audit trail required for the core authorization problem, or is it a TL-specific design choice?
- "Finality lane separation" — TL has two-lane separation by definition. But is two-lane separation a *benefit* or a *complexity cost*? Alternatives that achieve equivalent security without the two-lane complexity could be characterized as having lower architectural overhead.
- "Hardware enforcement of gate" — TL's C-element is physical; PEHI's seL4 is software. But seL4 has a machine-checked formal proof of functional correctness — a *different quality* of assurance than TL's physical enforcement. The comparison table presents "Hardware (C-element)" vs. "Software (verified)" as if hardware is always preferable, but for a distributed systems theorist, a formally verified software gate and a physically enforced hardware gate are different assurance models, not a hierarchy.

**Required revision:** The comparison section should explicitly acknowledge that the evaluation dimensions favor TL because they correspond to TL's specific design goals. An alternative comparison dimension set — authorization latency at minimum (not warm-path mean), single-point-of-failure resistance, operational cost per year, time-to-deployment — would likely show PEHI and DTAS as preferable to TL on multiple dimensions. The paper should acknowledge this explicitly: "The dimensions selected for comparison reflect TL's design priorities. Deployments with different priorities may find alternative architectures preferable; the appropriate comparison dimensions are deployment-context-specific."

---

### Challenge 3.5 — Cascading Provisional Chain Gap Requires Formal Specification, Not Just Acknowledgment

The Limitations section identifies the cascading provisional chain revocation gap (L3): if a multi-system provisional chain loses one FPT, downstream PPTs lack a specified cascade-revocation mechanism. This is correctly identified as a gap.

**The challenge:** For a distributed systems theorist, this gap is not merely an engineering task for future work — it is a correctness problem for the formal specification. The TLA+ model in the Appendix models a single-system PPT lifecycle. In any multi-system deployment, the state machine is a network of interacting TLA+ instances. The safety properties proven in the Appendix do not compose automatically to the multi-system case.

In distributed systems, the composition of safety properties is non-trivial. A property that is invariant for each individual component may not be invariant for the composition (see: the dining philosophers problem, or the two-generals problem). TL's safety invariant "no execution without a valid PPT" may be violated at the system level even if each individual component maintains it, if a cascading chain executes component-B-PPT conditionally on component-A-State-1, and component-A's State-1 is subsequently revoked.

**Required statement:** The paper should explicitly state that the formal safety proofs in the Appendix apply to the single-system model only. Multi-system compositional correctness — safety under cascading provisional chain scenarios — is identified as an open problem requiring a compositional formal specification (e.g., TLA+ module composition or CCS/CSP process algebra treatment) before TL can claim safety guarantees in distributed multi-component deployments. This is not a minor footnote — it is a material limitation on the formal verification claim.

---

### Verdict — Reviewer 3

**Verdict: Major Revision Required before publication in a peer-reviewed venue, though suitable for SSRN preprint at current stage.**

The paper represents a technically serious and architecturally coherent contribution. The formal specification is a genuine addition to TL's documentation; the failure mode taxonomy is thorough; the comparison with prior art is honest. The paper is closer to publishable than it may appear from the challenge list above — most of the required revisions are clarifications and scope statements rather than fundamental architectural changes.

The following revisions are required:

**R3.1** — Recharacterize TL's rollback guarantee throughout the paper as "hardware-enforced authorization state rollback" (not execution state rollback). Add an explicit statement that execution state rollback requires application-layer compensating logic triggered by the `provisionalExpiry` event.

**R3.2** — Separate the novelty claim into (a) architectural novelty (hardware enforcement of provisional-then-final pattern with two-lane latency separation — defensible) and (b) implementation specificity (C-element as the best available hardware gate for TL's architectural requirement — implementation rationale). Do not conflate these.

**R3.3** — Add an explicit scope statement to the TLA+ formal specification: "This model covers the single-system Lane 1 state machine. Multi-system compositional correctness, including cascading provisional chain revocation, requires a compositional formal specification and is identified as future work."

**R3.4** — Add a sentence to the alternative architecture comparison explicitly acknowledging that the evaluation dimensions reflect TL's design priorities. A deployment-context-specific dimension set may favor alternatives.

**R3.5** — Explicitly address the Governance Lane's state after forced State 0 return: specify that in-progress Lane 2 FPT construction should be cancelled on `provisionalExpiry`, and that a post-expiry FPT arriving at Lane 2 must be rejected. This should be added to the formal specification as an explicit axiom or constraint.

With revisions R3.1–R3.5, the paper is ready for TechRxiv/SSRN submission and has a viable path to peer-reviewed journal publication.

---

## Consolidated Revision Requirements

*This section lists all required revisions across the three reviewers for triage by the author. It does not reconcile the reviewers' verdicts — each stands independently.*

**Category A — Precision and Honesty (all reviewers agree these are required):**

| ID | Revision | Reviewer(s) |
|---|---|---|
| A1 | Qualify "under 50 ms" as warm-path figure with explicit p99 in Abstract and all headline locations | R2, R3 |
| A2 | Classify p99 latency figures as [Engineering Estimate] inline in the latency table | R2 |
| A3 | Recharacterize "hardware-enforced rollback" as "hardware-enforced authorization state rollback" with explicit explanation that execution state rollback requires application-layer compensation | R3 |
| A4 | Add explicit scope statement to TLA+ formal specification: single-system model only; multi-system compositional correctness is future work | R3 |

**Category B — Architecture and Specification:**

| ID | Revision | Reviewer(s) |
|---|---|---|
| B1 | Add crisp statement distinguishing C-element as known primitive from TL's contribution as architectural integration decision | R1 |
| B2 | Apply evidence taxonomy consistently in Section 5 to distinguish FPGA LUT-level [Demonstrated] from full MT hardware layer [Theoretical/Engineering Estimate] | R1 |
| B3 | Formalize two-tier architecture (Tier 1 physical constraint / Tier 2 software-policy weaker instantiation) as a formal structural distinction | R1, R3 |
| B4 | Separate novelty claim into architectural novelty vs. implementation specificity | R3 |
| B5 | Specify Governance Lane behavior on `provisionalExpiry` (FPT construction cancellation; post-expiry FPT rejection) | R3 |

**Category C — Security and Cryptography:**

| ID | Revision | Reviewer(s) |
|---|---|---|
| C1 | Strengthen HSM compromise analysis: state explicitly that TL's physical gate guarantee is conditioned on HSM software/firmware integrity; dual-HSM cross-validation is an architectural requirement, not a best practice | R2 |
| C2 | Expand post-quantum section: harvest-now-decrypt-later risk, Dilithium/SPHINCS+ latency/size implications for PPT pipeline, normative PQC migration plan | R2 |
| C3 | Strengthen hardware fault injection section: SRAM-based FPGA C-element is contraindicated (not merely non-recommended) for ASIL-D and IEC 62304 Class C deployments | R1 |

**Category D — Framing and Comparison:**

| ID | Revision | Reviewer(s) |
|---|---|---|
| D1 | Add statement to alternative architectures comparison acknowledging that evaluation dimensions reflect TL's design priorities | R3 |
| D2 | Add acknowledgment that seL4 formal verification and TL's physical enforcement represent different assurance models, not a hardware > software hierarchy | R3 |

---

## Post-Revision Projected Verdicts

*Note: These projections represent each reviewer's expected response to the revisions. They are not guaranteed outcomes and do not constitute commitments.*

**Reviewer 1 (Hardware Architect):** With revisions B1, B2, B3, C3 implemented, the hardware sections would meet the standard for TechRxiv publication and would withstand scrutiny from a semiconductor design audience. Projected verdict after revision: **Accept with minor revision**.

**Reviewer 2 (Cryptographer):** With revisions A1, A2, C1, C2 implemented, the cryptographic analysis would meet journal publication standard. The post-quantum section expansion is the most critical; without it, the paper is vulnerable in any venue where long-term deployment is relevant. Projected verdict after revision: **Accept with minor revision**.

**Reviewer 3 (Distributed Systems Theorist):** With revisions A3, A4, B4, B5, D1, D2 implemented, the formal methods and architectural soundness claims would be adequately scoped and defensible. The cascading chain gap is the most important — the formal specification must explicitly acknowledge its single-system scope. Projected verdict after revision: **Accept with minor revision**.

**Consensus path to publication:** Implementing all Category A revisions (A1–A4) is the highest-priority action, as these address honesty and precision concerns shared across reviewers. Categories B, C, and D address discipline-specific concerns and can be addressed in a structured revision. The paper is not fundamentally flawed; it requires precision improvements and scope clarifications consistent with the difference between an internal technical report and a publication-grade manuscript.

---

*End of Session 4 — Adversarial Review*

---

## Session Handoff Notes for Author

**What these four sessions have produced:**

- **Session 1** (fetched from GitHub): Evidence foundation for Q1, Q2, Q7 — hardware feasibility, cryptographic pipeline, performance. Status: complete research base, all figures [Engineering Estimate] pending primary-source verification.
- **Session 2** (this session): Deep research for Q3–Q6, Q8–Q11 — architectural soundness, novelty, failure modes, security, integration, alternatives, regulatory compliance, formal verification. Full traceability matrix complete.
- **Session 3** (this session): Publication-quality academic paper. All claims trace to Session 2 traceability matrix. Ready for revision per Session 4 findings.
- **Session 4** (this session): Three-reviewer adversarial challenge with specific revision requirements. Consolidated revision table provided.

**Recommended next steps:**
1. Implement all Category A revisions (A1–A4) — highest priority.
2. Primary-source verification of HSM latency/throughput figures and NIST CMVP certificate numbers (elevates [Engineering Estimate] to [Demonstrated] where confirmed).
3. Hardware measurement: Merkle tree benchmark, TPM 2.0 signing benchmark, HSM warm-path p99 under load.
4. Implement Category B–D revisions informed by the author's editorial judgment.
5. Full TLAPS-checked proof (Future Work FW7) — for completeness of the formal verification appendix.
6. Submit to TechRxiv for preprint; simultaneously prepare for peer-reviewed journal submission.
