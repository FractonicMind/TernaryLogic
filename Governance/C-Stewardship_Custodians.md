# Stewardship_Custodians.md
## Ternary Logic Constitutional Governance Research - Section 2
**Framework:** Ternary Logic (TL) by Lev Goukassian
**ORCID:** 0009-0006-5966-1243
**Research Date:** Q2 2026
**Status:** Standalone Report - Section 2 of 4

---

## Executive summary and verdict preview

The Stewardship Custodians, as specified in Governance.md, are a credible but fragile institution. **Their binding veto survives human-only adversaries with high probability over 10-year horizons and degrading probability over 20-30 year horizons [HIGH].** Their mandatory veto obligation, anti-capture review duty, and publication-of-reasons requirement are enforceable only as social and legal commitments, not as on-chain code [VERIFIED]. The 9-of-11 quorum requirement is a defined adversarial target: three disabled, compromised, or legally compelled Custodians are sufficient to freeze Type 2 and Type 3 governance [HIGH]. **Against the Q2 2026 threat frontier - synthetic video and audio forgery at chance-detection levels for untrained humans, automated agents probing procedural windows, and state-level harvest-now-decrypt-later posture - several Custodian provisions are effectively unenforceable at the software layer [NOVEL].**

The core honest tension for this section: any software-layer governance architecture, including the Custodians' on-chain voting contracts, is modifiable by any adversary with sufficient access to the execution substrate. Constitutional governance written in smart contract code is only as strong as the hardware beneath it. The Stewardship Custodians provide accountability, auditability, and coordination; they do not, and cannot, provide physical enforcement. Physical enforcement of the Immutable Mandates belongs to DITL hardware, where Epistemic Hold is instantiated as a dual-rail NULL voltage state that cannot be overridden by software, root access, kernel compromise, or firmware manipulation [VERIFIED from Atomic Auditability paper]. Both layers are necessary. Neither alone is sufficient.

---

## 2.1 Stewardship Custodians vote rights architecture

The Custodians' vote rights implement what Tsebelis veto-player theory recognizes as an **asymmetric proposer-blocker architecture**: one body (the Technical Council) holds monopoly on origination of technical and treasury proposals; the other (the Custodians) holds binding constitutional veto but cannot itself originate. This asymmetry is the structural counterweight. It has precedent, but the precedents are cautionary.

### The asymmetry under historical pressure

Four constitutional analogs provide the calibration set. The **US Senate advice-and-consent power** (Article II §2) cannot originate treaties or nominations but has, over two centuries, developed de facto agenda-shaping via blue slips, committee holds, and informal pre-consultation. The **UK House of Lords** held absolute veto on legislation until the 1909 budget crisis forced the Parliament Act 1911, which reduced it to a two-year delaying power (further reduced to one year by the Parliament Act 1949). The **Canadian Senate** retains formal absolute veto over ordinary legislation but has applied it sparingly; the 1988 free-trade and 1990 GST disputes required Prime Minister Mulroney to invoke the never-previously-used Section 26 of the Constitution Act to appoint eight extra senators to break Senate blockade. The **German Bundesrat** distinguishes Zustimmungsgesetze (absolute consent required) from Einspruchsgesetze (suspensive veto only, overridable by the Bundestag), and uniquely retains a legislative-initiative right under Article 76(1).

The cross-case pattern is consistent and load-bearing for this analysis: **pure veto-only bodies tend to develop de facto proposal power over time through procedural innovation, unless restrained by explicit constitutional lock-in or a durable legitimacy gap** [HIGH, based on Tsebelis 2002 and Hirsch-Shotts 2022]. The Custodians face exactly this drift risk. The Governance.md prohibition on Custodian-initiated technical proposals, treasury proposals, or node certification changes is textually explicit, but **every analogous body has found ways around such prohibitions over multi-decade horizons** [HIGH]. Without an on-chain enforcement mechanism for the proposal prohibition itself, sustained pressure during a Technical Council stalemate will likely produce procedural innovations (drafted "advisory white papers," informal pre-negotiation, public publication of proposed alternatives) that functionally re-introduce proposal authority. [CONSTITUTIONAL TENSION]: the textual scope restriction is durable; the functional scope restriction is not.

The closest mission-critical analog is the **nuclear Two-Man Rule combined with Permissive Action Links**, operational across the US arsenal from 1962 to present. Two independent authorized individuals must affirmatively act to arm or launch; either can veto. Cryptographic code gates enforce the separation in hardware. This architecture has not failed catastrophically in 63 years [VERIFIED]. It is the most durable observed asymmetric-veto design. Its durability comes from **physical enforcement of the separation, not procedural enforcement** - which is precisely the move the Atomic Auditability paper proposes for Epistemic Hold.

### The mandatory veto obligation

Governance.md states: Custodians "must veto any proposal creating credible risk of violating any Immutable Mandate (No Spy, No Weapon, No Switch Off). Failure to veto is itself a constitutional violation."

This obligation is **enforceable only at the social and legal layer, not on-chain** [VERIFIED]. Smart contract voting logic cannot distinguish between a Custodian who votes to approve because they believe the proposal does not violate a Mandate and a Custodian who votes to approve despite believing that it does. The mandatory veto reduces in practice to an evidentiary standard: after the fact, can analysts prove the vote was a constitutional violation? The publication requirement (below) partially addresses this but introduces separate risks.

**What happens when a Custodian majority disagrees about whether a proposal violates a Mandate?** The Custodians' constitutional role requires them to adjudicate the edges of the Mandates themselves - No Spy does not come with a precise operational definition, and adversaries will probe the edges. The governance document provides no tie-breaker and no external arbiter. Under Governance.md's 9-of-11 quorum and 75% veto threshold, **a 3-member minority can effectively force a veto by withholding consent**, because the absence of a 75% supermajority on the Type 3 Joint-Approval defaults to rejection. This is structurally sound for the "defend the Mandates" case but creates a parallel vulnerability: a 3-member captured minority can veto legitimate Technical Council proposals indefinitely [HIGH]. The OPCW Douma dispute (2018-2020), with its contested whistleblower claims and DG-level suppression allegations, illustrates what happens when a technical body must adjudicate its own edge cases under political pressure - outcome quality degrades and institutional trust collapses regardless of which side was factually correct [VERIFIED].

### The publication requirement on veto

Governance.md requires Custodians to publish a report detailing constitutional and ethical grounds for any veto. **Under adversarial conditions this requirement cuts both ways** [NOVEL].

Strengthening effects: public reasoning creates legal record; invites external scholarly and civil-society scrutiny; raises the reputational cost of sham vetoes or sham non-vetoes; and creates an audit trail for detecting capture (a pattern of vetoes whose reasoning consistently favors one nation-state or corporate interest is detectable).

Weakening effects: **published veto justifications are a training corpus for adversarial circumvention** [SPECULATIVE, but directly supported by documented offensive-AI practice as of Q2 2026]. The documented use of LLM-assisted reconnaissance by state actors (Google Threat Intelligence Group, November 2025) and the 2025 maturation of illicit AI tool marketplaces imply that an adversary can automatically ingest all public Custodian veto reports and generate proposals optimized to avoid the stated grounds while preserving the underlying harmful behavior. This is a form of "reasoning leakage." The published reports become the specification against which hostile proposals are optimized. [CONSTITUTIONAL TENSION]: transparency is constitutionally required and ethically correct, yet provides operational intelligence to patient adversaries.

The mitigation is not secrecy. The mitigation is that **the Immutable Mandates must be enforceable at a layer below the proposal specification** - which is exactly what DITL hardware provides. A hardware Epistemic Hold does not care how the harmful intent was laundered through clever proposal language; it blocks on physical attestation of the Escrow state [VERIFIED from Atomic Auditability].

### The absence of Custodian proposal rights - governance gap

Governance.md denies Custodians the right to initiate technical upgrades, propose Treasury disbursement rules, or submit node certification changes. This is doctrinally correct: proposal rights in a Custodian body would collapse the tri-cameral separation and convert Custodians from janitors into architects. [CONSTITUTIONAL VIOLATION risk flagged if this is ever relaxed.] Recall the constitutional hard boundary: **governance is the janitor of eternity, not the architect of tomorrow**. The Custodians must remain at janitor scope.

But this creates a defined gap: **what happens when the Custodians identify a problem - an emerging capture vector, a Mandate-edge ambiguity, a technical drift - that the Technical Council refuses to address?** Governance.md's Time-Bound Epistemic Hold mechanism (Section 2.6 below) handles the stalemate case within a proposal lifecycle. It does not handle the no-proposal case, where the Council simply refuses to propose remediation.

The least-harm design response, without crossing into architectural authority, is: **the Custodians may publish findings identifying a problem and may veto any Technical Council proposal that fails to address it, but they cannot compel the Council to propose remediation.** This is the structure Governance.md implies. The cost is real: in the worst case, a captured Technical Council that simply stops proposing can freeze system evolution while the Custodians watch. The mitigation is that the Smart Contract Treasury continues autonomous operation during such a freeze (Section 2.7), which is a feature, not a bug - the janitor role does not require constant action.

### The 9-of-11 quorum as adversarial target

Any Type 2 or Type 3 vote requires 9 of 11 active Custodians. **Removing 3 Custodians - by death, incapacitation, resignation, legal compulsion, or coordinated non-appearance - paralyzes all Type 2 and Type 3 governance** [VERIFIED from Governance.md text]. This is a known attack vector in comparable bodies.

The canonical precedent is the **WTO Appellate Body quorum collapse of December 2019**. The Body had 7 seats and a 3-member quorum to decide appeals. The United States blocked the reappointment of South Korean member Seung Wha Chang in May 2016 and systematically blocked all further appointments. On 10 December 2019 the terms of Ujal Singh Bhatia and Thomas R. Graham expired, leaving only Hong Zhao; by 11 December 2019 the Body lost quorum, and by December 2020 all seven seats were vacant [VERIFIED via CRS LSB10385]. A single state with negative-consensus blocking power produced full collapse through inaction alone, with no formal rule change required. The Body has remained non-functional for six years as of this writing.

The Custodians differ from the Appellate Body in that their members are not confirmed by a single adversarial state. But the structural lesson applies: **a body requiring affirmative appointment to maintain quorum is a body vulnerable to attrition-based collapse** [HIGH]. Three Custodians can be removed via:

- Death or incapacitation (base-rate actuarial risk over 20 years is meaningful for an 11-member body whose members are senior experts)
- Targeted legal compulsion across jurisdictions (the APGT scenario, Section 2.5.1)
- Coordinated resignation under duress
- LLM-assisted personalized pressure campaigns (the $25M Arup deepfake CFO fraud of January 2024 demonstrates that individualized video-and-voice manipulation at scale is now operational [VERIFIED])

The Nominating Committee provision (Section 2.3) is the designed backstop, but it is slow and itself vulnerable. During the interval between loss of quorum and replacement confirmation, the system is effectively frozen at the governance layer. Whether this freeze is acceptable depends on whether the Smart Contract Treasury can sustain operation - which it can, but without human course-correction (Section 2.7).

**Specific recommended strengthening without God Mode:** (a) consider pre-confirmed alternates - individuals vetted and pre-approved but not seated unless a primary departs, reducing the quorum-replacement window from months to hours; (b) require geographic distribution of quorum such that no single jurisdiction's legal compulsion can drop more than 2 members; (c) permit verifiable remote attestation of presence so that incapacitation by physical detention is distinguishable from resignation. None of these require architectural authority. All are janitorial.

---

## 2.2 Capture vector analysis

Article VII of Governance.md identifies three capture vectors: state, corporate, and insider. The tri-cameral three-body equilibrium requires simultaneous capture of both the Technical Council and the Stewardship Custodians for any Type 3 action. This is sound in principle. The historical record shows the mechanisms by which, despite such protections, capture nonetheless succeeds.

### State capture - precedents and pattern

**The NIST / Dual_EC_DRBG episode (2004-2014)** is the canonical state-capture-of-a-standards-body precedent [VERIFIED]. The ANSI X9F1 committee that originated Dual_EC included three NSA employees and three RSA Security employees. NIST published SP 800-90A in 2006. Shumow and Ferguson (CRYPTO 2007 rump session) demonstrated the backdoor structure. The Snowden 2013 Bullrun disclosures, combined with December 2013 Reuters reporting of a $10 million NSA payment to RSA to make Dual_EC the default PRNG in BSAFE, triggered NIST's revised SP 800-90A Rev.1 in April 2014 removing the algorithm. The NIST VCAT review found that the standards process had been compromised by reliance on agency expertise without independent review. Time horizon: approximately 9 years from standardization to retraction.

**Layer of failure:** cryptographic (algorithm choice), social (agency authorship of standard), economic (RSA contract). **Would the Custodians' structure have prevented this?** Partially. A supermajority veto requirement would raise the bar for adoption of an algorithm with visible backdoor structure, and an anti-capture review obligation should surface the authorship concentration. The external-reviewer path (Shumow and Ferguson were private-sector researchers) is the detection mechanism that actually worked. Structural diversity in the Custodians helps only if at least one member has the technical depth and political freedom to raise objection on cryptographic rather than political grounds. **A captured Custodian majority that collectively defers to state technical expertise would not have prevented Dual_EC** [HIGH].

**The UN Security Council veto pattern** provides the other end of the state-capture spectrum. 2024 saw seven vetoed draft resolutions with eight total vetoes (four Russia, three US, one China) - the most since 1986 [VERIFIED via Security Council Report]. The NPT Review Conferences show consensus-capture: in 2015 the US, UK, and Canada blocked consensus over Middle East WMD-Free Zone language; in 2022 Russia alone blocked consensus over Ukraine-related paragraphs [VERIFIED via UN press release DC/3850]. **Single-state blocking in consensus bodies generalizes to single-bloc blocking in supermajority bodies**: a Custodian body with a 75% veto threshold can be blocked by a coordinated bloc of 3, which is achievable by any state with legal or economic leverage over 3 jurisdictions.

### Corporate capture - the Basel and OOXML precedents

**Basel Committee on Banking Supervision capture of Basel II and Basel III** is documented in Lall (2012, RIPE 19:4) and Bengtsson (2015 ECB working paper) [VERIFIED]. The Internal Ratings-Based approach in Basel II reflected industry preferences channeled through the Institute of International Finance consultations. Bengtsson found that BCBS "mainly accommodated the preferences of stakeholders from the financial industry and advanced economies in finalising Basel III." The Basel III Endgame proposal (July 2023) was substantially weakened in mid-2024 after industry lobbying. Time horizon: decades, with each consultation round producing incremental concessions. Layer: economic (lobbying) plus legal (the Committee's soft-law status).

**The ISO/IEC OOXML fast-track (2006-2008)** demonstrates corporate capture of a standards body via mass-accession [VERIFIED]. Martin Bryan, convenor of ISO/IEC JTC1/SC34/WG1, resigned in 2008 citing capture: "The influx of P members whose only interest is the fast-tracking of ECMA 376 as ISO 29500 has led to the failure of a number of key ballots." Sweden's national vote was invalidated after a Microsoft partner admitted paying for votes. Capture worked by finding sympathetic local actors in each national body - **diversity requirements did not prevent capture; they facilitated it, because the adversary simply populated each diversity category with aligned members** [VERIFIED]. Time horizon: approximately 18 months of concentrated effort.

**Would the Custodians' "no more than 2 from the same entity" rule prevent this?** Partially, but entity is a slippery category. Modern corporate acquisition patterns (where a Custodian's employer is acquired after appointment, or where multiple ostensibly independent foundations share backing) defeat textual interpretations of the rule. The Leonard Leo / Federalist Society pipeline for US federal judicial nominations (2017-2020) produced 86% FedSoc affiliation in Trump circuit and Supreme Court appointees without any formal entity overlap - **ideological capture operates through a different coordination mechanism than institutional capture, and diversity rules addressed to institutions do not bind ideology** [VERIFIED via ProPublica and Yale Daily News 2024 reporting].

### Insider collusion - XZ Utils is the precedent

The **XZ Utils / "Jia Tan" backdoor (2021-2024)** is the canonical multi-year insider-grooming precedent [VERIFIED via Russ Cox timeline, Kaspersky Securelist, and Linux Foundation 2024 post-mortem]. The sequence:

- January 26, 2021: GitHub account JiaT75 created
- October 29, 2021: first innocuous patch to xz-devel
- April 2022: sockpuppet "Jigar Kumar" begins pressuring sole maintainer Lasse Collin to add a co-maintainer, citing Collin's publicly stated mental health struggles
- June 2022: second sockpuppet "Dennis Ens" joins pressure campaign
- January 7, 2023: first direct commit by JiaT75; oss-fuzz contact transferred from Collin
- July 2023: IFUNC disabled in oss-fuzz to conceal backdoor from fuzzing
- January 19, 2024: JiaT75 moves xz.tukaani.org to GitHub Pages
- February 23-24, 2024: backdoor binary inserted as "test corpus" in releases 5.6.0 and 5.6.1
- March 28-29, 2024: Andres Freund, a Microsoft PostgreSQL engineer, notices 500ms sshd latency, reverse-engineers the backdoor, and discloses. CVE-2024-3094 assigned (CVSS 10.0)

Total operation: approximately 2.6 years; only 8 of hundreds of commits were malicious.

**Mechanism, layer, and TL architecture response:**

1. *Mechanism of failure:* patient multi-year social engineering of a sole maintainer suffering from burnout, combined with sockpuppet pressure campaigns creating artificial demand for co-maintainer privileges.
2. *Layer:* social (grooming) plus identity (fabricated persona, attributed by Kaspersky to APT-consistent tradecraft) plus software (build-process injection).
3. *Would TL's architecture have prevented this?* The Custodians' institutional diversity requirements and quorum thresholds would have **helped substantially** because TL governance has no single-maintainer node. Any release-critical action requires quorum and supermajority. The XZ attacker would have needed to compromise multiple Custodians simultaneously, which moves the attack from "patient grooming of one burned-out maintainer" to "multi-year coordinated grooming of several senior policy professionals." This is harder but not impossible - Hanssen (FBI, 22 years) and Ames (CIA, 9 years) demonstrate that patient grooming of multiple senior professionals is achievable over decade-plus horizons [VERIFIED].
4. *Additional constraint without God Mode:* pre-commitment of signing keys to hardware security modules with dual-control attestation; mandatory co-signing of critical actions by at least two geographically separated Custodians; public logging of all Custodian action-signing events to a tamper-evident ledger. All janitorial.

**The solo insider threat specifically.** Governance.md's quorum and supermajority thresholds address unilateral action by design - no single Custodian can act alone on any Type 2 or Type 3 matter. The residual solo-insider risk is different and narrower: (a) confidentiality breach of deliberations (the Snowden/Manning/Winner pattern, weeks-to-months horizon); (b) key-compromise exfiltration in which an insider's signing credentials are used by an external attacker; (c) individual refusal to vote, which contributes to quorum attrition. None of these can be fully prevented at the software layer. **Hardware-enforced dual-control signing closes (b); it does not close (a) or (c)** [HIGH].

### The 75% supermajority under sustained pressure

A 75% supermajority of 11 Custodians is 9. The blocking minority is 3. **Sustained adversarial pressure to reach either 9 aligned or 3 aligned members is a multi-year project against a rotating body with 4-year staggered terms and an 8-year cap.** Two decades is sufficient time to appoint or influence a majority of seats through legitimate Nominating Committee channels if the Committee is itself compromised (Section 2.3). The FSOC designation regime - which shifted from aggressive (Obama era) to retreat (Trump I) to re-strengthening (Biden) to reverting (Trump II 2026) - illustrates how a body with 2/3 supermajority designations oscillates across multi-decade political cycles, with each administration eroding prior framework [VERIFIED via GAO-23-105708 and CRS R48739]. Supermajority thresholds slow but do not halt such oscillation.

---

## 2.3 Nominating Committee integrity

The Nominating Committee as specified: 7 members - 2 outgoing Technical Council, 2 outgoing Custodians, 3 external domain experts selected and approved by existing Custodians. The receiving body confirms by 2/3 qualified majority.

### The external-expert selection path is the capture entry point

**The three external experts are selected and approved by existing Custodians.** This creates a direct self-reproduction channel: a Custodian majority inclined toward a given ideology can select external experts aligned with that ideology, who then tilt nominations toward replacements who preserve the majority. The ICANN Nominating Committee is the closest operational analog, and it has been publicly contested on precisely this ground. **Outgoing ICANN CEO Rod Beckstrom at ICANN 43 (San Jose, 2012) publicly called for the NomCom to be "free of conflicts" and "financially independent of the domain name industry"** [VERIFIED]. In June 2025 ICANN formally intervened in AFRINIC Board elections after two NomCom members were appointed who had previously supported a disputed company's AFRINIC membership registration - a textbook NomCom capture case [VERIFIED].

The Federalist Society pipeline provides the upper bound on what a concerted multi-decade selection strategy can achieve. Leonard Leo's network produced 86% FedSoc affiliation in Trump circuit and Supreme Court appointees over four years; by 2024 six of nine Supreme Court Justices self-identified as FedSoc affiliates, and a 2023 study found FedSoc affiliation raised Senate-confirmation probability by approximately 20 percentage points [VERIFIED via ProPublica and TIME]. **The Custodian external-expert selection mechanism is structurally similar to the Federalist Society short-list mechanism: curated external expertise provided to the decision body, which then ratifies without independent recruitment** [HIGH].

### Does the 2/3 qualified-majority confirmation compensate?

Partially. A 2/3 confirmation threshold protects against overt partisan capture but does not protect against **ideological convergence within the expert class itself** - the phenomenon Dumbrovský, Petkova and Van der Sluis (Common Market Law Review 51:2, 2014) identified in their analysis of the European Court of Justice Article 255 panel, where opening scrutiny produced "a subtle move in the direction of judicial self-government" rather than industry capture [VERIFIED]. The risk is not that the Custodians become tools of a state or corporation; it is that they become a self-reproducing professional class whose members share assumptions that adversaries can identify and exploit.

### Cool-down periods - do they prevent or delay revolving-door capture?

The Governance.md four-year cool-down for Custodians after two consecutive terms is substantially longer than most real-world comparators. The empirical evidence is sobering.

**Wright and Booker (2010, Advances in Accounting), the most-cited direct empirical study, found that perceived auditor independence increases significantly with a 1-year cooling-off period but "increasing the length from one year to two years fails to significantly increase perceptions of independence"** [VERIFIED]. The finding is consistent with diminishing returns: the signal value of a cool-down peaks early and flattens. It does not follow that 4-year cool-downs are no better than 2-year, but the empirical base for claiming strong incremental benefit is thin.

Specific breach cases confirm the "delay not prevent" reading:

- **José Manuel Barroso** (European Commission President 2004-2014) joined Goldman Sachs as non-executive chair two months after the 18-month cooling-off window expired, July 2016 [VERIFIED]. The ad-hoc ethics committee cleared him of formal violation but criticized his judgment.
- **FDA revolving door:** Bien and Prasad (BMJ, September 2016) found that more than half of 55 FDA hematology-oncology reviewers 2001-2010 subsequently worked for the biopharmaceutical industry [VERIFIED]. In April 2025 former FDA commissioner Scott Gottlieb publicly told CNBC that as many as 600 drug reviewers had recused themselves from approvals because they were interviewing with pharma companies [VERIFIED via STAT].
- **SEC revolving door:** between 2001 and 2010, more than 400 former SEC employees filed almost 2,000 disclosure forms stating they planned to represent a client before the SEC [VERIFIED via POGO 2013].

**Adolph (2013, Bankers, Bureaucrats, and Central Bank Politics) - the seminal quantitative study of ~600 central bankers across 20 economies 1950-2000 - showed that prior private-sector banking experience predicts tighter monetary policy and prior bureaucratic or academic careers predict looser policy** [VERIFIED]. Career paths themselves are the capture mechanism; cool-down periods address only the window, not the upstream pipeline.

**The honest reading:** the 4-year cool-down is better than shorter alternatives and signals seriousness, but it does not close the capture vector. What closes it is the combination of cool-down plus transparent career-path publication plus public anti-capture review obligation plus ideologically non-homogeneous nomination sourcing. Governance.md specifies the first and third; it underspecifies the fourth.

### Specific recommended strengthening without God Mode

(a) Require that the three external experts on the Nominating Committee be drawn from a pre-committed public registry of candidates who have declared their interest years in advance, with their career paths publicly visible - this does not restrict Custodian discretion but shifts the selection corpus from private networks to public ones. (b) Publish detailed Nominating Committee deliberation records with a delay (e.g., 10 years) to enable retrospective audit without chilling current deliberation. (c) Require Nominating Committee members to disclose all prior affiliations of candidates and their own relationships to candidates, with a rebuttable presumption of recusal. All janitorial, none architectural.

---

## 2.4 Governance fatigue and temporal degradation

Over 10, 20, and 30 year horizons, the Custodians face three distinct degradation pressures: institutional-memory attrition, alert-volume overload, and quorum-cascade risk. The historical evidence across comparable bodies is consistent: **governance bodies do not degrade gracefully; they degrade suddenly at identifiable stress points** [HIGH].

### Longitudinal effectiveness of comparable bodies

The **Federal Reserve Board of Governors**, with 14-year staggered terms, is the most durable comparator. Drechsel (NBER Working Paper 32461, 2024) documented via narrative approach that Nixon-era political pressure on Arthur Burns ahead of the 1972 election produced non-systematic monetary easing [VERIFIED]. The 2025-2026 Trump-administration executive orders asserting presidential supervision of independent agencies, public pressure to lower rates, and DOJ criminal investigation of Chair Powell mark the sharpest stress on Fed independence in half a century [VERIFIED via MSU Today and CFR]. The institution has not failed, but independence is measurably trending down from a historical peak.

The **US Supreme Court** legitimacy trajectory is the clearest quantitative warning. Gallup trust fell from roughly two-thirds historically to 53% in 2023, the lowest level in the poll's 50-year history; Pew found a 26-point drop in favorable views 2021-2023 [VERIFIED via Judicature]. Krewson et al. (Science Advances 2024) documented that polarized partisan decisions tripled from 9% of 2018-19 cases to 29% in 2021-22 [VERIFIED]. **A governance body with 8-year Custodian terms and a 4-year cool-down faces analogous legitimacy erosion pressures over 20-30 year horizons** [HIGH].

The **WTO Appellate Body collapse** (December 2019 quorum loss, all seven seats vacant by December 2020, non-functional for six years) is the clearest cautionary case. One state's refusal to confirm appointments collapsed a body that had functioned for 24 years [VERIFIED via CRS LSB10385]. The lesson generalizes: **bodies requiring affirmative appointment to sustain quorum are vulnerable to attritional collapse that requires no rule change** [VERIFIED].

### Alert fatigue as documented failure mode

Volume overload is the most empirically measured failure mode across comparable review functions. The numbers are stark.

- **SOC analyst alert fatigue:** multiple 2024 studies converge on roughly 62% of security alerts ignored entirely; CardinalOps 2024 found 20-30% of alerts never properly investigated; typical enterprise SOC receives approximately 3,832 alerts per day; Tines 2022 and a 2023 industry study found approximately 83% of alerts are false positives and 67% get ignored because analysts cannot keep up [VERIFIED via multiple vendor-and-academic studies, with the caveat that aggregate headline percentages come from vendor-published surveys].
- **Medical alert fatigue:** EHR override rates reach 96% for drug-allergy alerts; average physician receives 180+ alerts per day; more than 95% override rate for low-priority notifications; **331 alerts are required on average to prevent 1 adverse drug event** [VERIFIED via JAMA 2024 and Ridgeway et al., PMC5058605].
- **PCI-DSS compliance drift:** Verizon Payment Security Reports document continuous decline from 55.4% full compliance (2016 data) to 27.9% (2019 data), a 27.5 percentage point drop over four years [VERIFIED via Verizon PSR series].
- **SEC enforcement volume under constraint:** FY2024 saw 431 standalone enforcement actions, down 14% from 501 in FY2023; investment-adviser enforcements were down 49% from the 2019 peak of 191 [VERIFIED via Morgan Lewis 2025 white paper].
- **Bank Secrecy Act SAR overload:** in 2019, 12,148 financial institutions filed 2,751,694 SARs, with 10 filers accounting for 49% of all filings - a roughly 4x increase over two decades while law enforcement capacity did not scale. FinCEN's 2025 guidance explicitly acknowledged "duplicative work and information overload for both financial institutions and law enforcement" [VERIFIED].

**For the Custodians, the direct analog is the anti-capture review obligation**, which requires continuous monitoring of a growing corpus of proposals, system events, and public reports. The base rate of review failure in analogous functions is 60-96% override or ignoring. **Unless the Custodians' review workflow is itself supported by automated pre-triage with careful design, governance fatigue is the most likely failure mode over 10-20 year horizons** [HIGH].

The cruel irony is that the automated pre-triage pushed by fatigue pressure creates its own capture vector: **the triage tools become the target.** If an adversary can shape what alerts rise to Custodian attention, the Custodians' binding veto power is disarmed at the upstream filter. This is the PCI-DSS compliance drift pattern applied to governance.

### Cognitive overload and the Custodian review function

What degrades first under alert overload, based on the comparative literature: (a) review of edge cases that require judgment (as opposed to pattern matching) degrades first; (b) proactive anti-capture surveillance (which has no immediate deadline) is deferred in favor of reactive vote-on-proposal work (which has deadlines); (c) investigation depth drops before investigation count; (d) inter-Custodian deliberation quality drops before voting participation [HIGH, based on cross-domain alert-fatigue literature]. All four degradations weaken exactly the judgment work that the Mandatory Veto Obligation depends on.

### Quorum failure cascade

The 9-of-11 threshold is vulnerable to exactly the failure mode observed in the WTO Appellate Body and the **UN Commission on Human Rights (dissolved 2006 via GA Resolution 60/251 after composition-based delegitimization rather than formal quorum loss)** [VERIFIED]. For the Custodians over 20 years: actuarial base rate of death or incapacitation for 11 senior professionals is non-trivial; targeted legal compulsion against even a single jurisdiction's Custodians can remove 1-2 members (if the "no more than 2 per entity" rule is respected, 2 is the ceiling per jurisdiction); coordinated LLM-assisted social engineering campaigns (Section 2.5) can induce resignation under pressure. Loss of 3 members freezes governance. **The recommended mitigations are pre-confirmed alternates, geographic quorum distribution, and verifiable remote attestation of presence, as noted in Section 2.1** [NOVEL].

---

## 2.5 The human-AI adversarial frontier

The Stewardship Custodians' architecture was defensible against 2015-2020 threat models. **As of Q2 2026, several of its defenses are qualitatively weaker against adversaries equipped with current synthetic media generation, LLM-based spear phishing, and automated agent probing** [NOVEL].

### Defenses that are qualitatively different against AI-assisted capture

**There are none.** The Custodians' defenses - diversity, supermajority, quorum, publication, cool-down, anti-capture review - are all defenses against human adversaries. They assume the cost of coordinating synthetic personas across 2-5 year horizons is prohibitive and that human reviewers can detect manipulated evidence. Neither assumption holds in Q2 2026 [HIGH]. The defenses are not useless; they still raise the cost of attack. They are no longer qualitatively suited to the threat frontier.

### Can human Custodians reliably detect AI-generated evidence manipulation in Q2 2026?

The empirical answer is no for most modalities under adversarial conditions.

**Diel et al. (Computers in Human Behavior Reports, December 2024), meta-analysis of 56 studies with 86,155 participants,** found overall human detection of synthetic media at 55.54% (95% CI 48.87-62.10), with every modality's confidence interval crossing chance [VERIFIED]. Audio: 62.08% (38.23-83.18). Image: 53.16%. Text: 52.00%. Video: 57.31%. An arXiv:2501.15654 study (January 2025) found that annotators unfamiliar with LLM-generated text perform near random; only annotators who use large language models daily approach reliable detection, and even then only in careful A/B testing conditions [VERIFIED]. The Deepfake-Eval-2024 benchmark (arXiv:2503.02857, March 2025) showed top commercial detection systems after fine-tuning achieved only approximately 75% accuracy on video, 86% on audio, 69% on images - meaningfully below the roughly 90% inter-rater agreement for professional forensic analysts [VERIFIED].

The January 2024 Hong Kong deepfake CFO fraud is the most concrete operational precedent. A finance employee at the Hong Kong office of a UK engineering firm was tricked in a multi-party video conference in which every participant except the victim was a synthetic deepfake of the London-based CFO and colleagues; 15 transfers totaling approximately US$25.6 million were executed [VERIFIED via Hong Kong Police announcement 5 February 2024]. The operational lesson: **current synthetic video plus voice, under videoconference conditions, defeats unprepared human reviewers at executive level.**

C2PA content provenance adoption reached over 6,000 members/affiliates by January 2026 and is embedded in several camera models, but platforms still strip metadata on upload and transcoding, breaking the provenance chain for most end users; a September 2025 hardware key-management failure required revocation of all certificates from one camera model [VERIFIED]. C2PA is the most serious current mitigation; it is not sufficient alone. Watermarking schemes have been broken at 60-90% rates by specialized attacks (UnMarker at USENIX Security / IEEE S&P 2025) [VERIFIED].

**For the Custodians, the operational implication is that any evidence presented in support of a proposal - video testimony, audio recordings, document photographs, attributed quotations - cannot be reliably authenticated by human review alone in Q2 2026.** This is not a speculative claim; it is the documented finding of multiple 2024-2025 meta-analyses.

### Automated exploitation of procedural gaps

**CVE-Bench (ICML 2025 spotlight, arXiv:2503.17332) benchmarks LLM agents against 40 critical-severity real-world CVEs; state-of-the-art agents in 2025 exploited approximately 13% of critical-severity real-world web application CVEs in production environments** [VERIFIED]. AutoPenBench reports 21% fully autonomous success, rising to 64% with human assistance. Against known vulnerabilities with CVE descriptions, agent success rises to 85-87% in controlled conditions. The ARTEMIS framework (arXiv:2512.09882) placed second overall in a real-world penetration testing competition, outperforming 9 of 10 human participants. Google Threat Intelligence Group tracked 90 zero-days exploited in the wild in 2025 [VERIFIED].

For governance procedures, the analog is: **automated agents can systematically probe decision windows, deadline calendars, quorum thresholds, and publication schedules at machine speed, identifying procedural corners that human Custodians have not examined** [HIGH]. The Custodians' Time-Bound Epistemic Hold (Section 2.6) is specifically vulnerable - any window has boundaries, and any boundary has edge-case behavior, and edge-case behavior can be mapped by automated probing faster than a human body can adapt.

### Long-horizon social engineering

The human baseline is already multi-year:

- **Robert Hanssen (FBI, 1979-2001):** 22 years of active betrayal; total US intelligence losses and compromised assets characterized by DOJ as "possibly the worst intelligence disaster in U.S. history" [VERIFIED].
- **Aldrich Ames (CIA, 1985-1994):** 9 years; compromised more CIA assets than any prior insider [VERIFIED].
- **XZ Utils / "Jia Tan" (2021-2024):** 2.6 years of patient open-source grooming plus sockpuppet pressure campaigns.

No publicly confirmed case exists as of Q2 2026 of an AI-coordinated multi-year grooming operation against an open-source maintainer or regulatory figure [VERIFIED]. The Linux Foundation's April 2026 report explicitly warns that the XZ template is being replicated and that LLMs plausibly lower the cost of maintaining multiple convincing sockpuppet personas over multi-year timescales [VERIFIED]. **The threat class is not speculative; its AI-augmented instantiation is emerging but not yet documented at confirmed state-level scale.** The right reading: assume the cost of the XZ-pattern attack has dropped by at least an order of magnitude and plan Custodian defenses accordingly [SPECULATIVE but defensible].

---

## 2.5.1 Advanced Persistent Governance Threat (APGT) ceiling

Define the APGT ceiling as an adversary with:

1. **Quantum decryption posture:** harvest-now-decrypt-later collection against current classical cryptography, with credible 10-year probability of cryptographically relevant quantum computer availability. The Global Risk Institute Quantum Threat Timeline Report 2025 (seventh edition, published April 2026, survey of 26 international experts) gives 28-49% probability of CRQC within 10 years, the most optimistic in the survey's 7-year history; "quite possible" within 10, "likely" within 15 [VERIFIED]. NIST finalized FIPS 203 (ML-KEM), 204 (ML-DSA), and 205 (SLH-DSA) on 13 August 2024 [VERIFIED]. A 2025 Gidney theoretical result and 2026 whitepapers indicate secp256k1 and related curves may be vulnerable with approximately 1,200 logical qubits on sufficiently fault-tolerant systems.
2. **AI-generated synthetic video and document evidence** for social engineering at the quality levels documented in Section 2.5 - meaning current human detection at roughly chance without expert forensic analysis and proper tooling.
3. **Legal compulsion power over 30% or more of Custodian jurisdictions** - achievable by any large state against any Custodian body with members holding property, family ties, or citizenship in that jurisdiction. The no-more-than-2-per-entity rule does not bind jurisdiction; geographic diversity rules help but do not close the vector.

### Which Custodian provisions survive APGT?

- **Survive:** the publication-of-reasons requirement (hostile intent becomes part of the permanent record even if the vote is compelled); the staggered-term rotation (prevents any single APGT moment from controlling all seats); the Nominating Committee's mixed composition (prevents the simplest single-point capture) [HIGH].
- **Degrade meaningfully:** the 75% supermajority (3-member compelled bloc achieves paralysis); the 9-of-11 quorum (3-member compelled absence achieves paralysis); the Mandatory Veto Obligation (compelled Custodian can rationalize non-veto using forged evidence that passes human review); the anti-capture review obligation (volume overload degrades surveillance) [HIGH].
- **Fail:** any reliance on evidence authenticity in governance deliberation (given chance-level human detection); any reliance on long-lived classical cryptography for persistent governance records (given HNDL collection); any reliance on undetected covert coordination among a minority of Custodians (given the LLM-assisted sockpuppet pattern) [HIGH].

### Which provisions require DITL hardware to resist APGT?

**The Immutable Mandates themselves.** No Spy, No Weapon, No Switch Off must be enforced below the layer at which an APGT adversary can operate. Software-layer governance can record, deliberate, and certify; it cannot physically prevent execution when the adversary controls the substrate. **DITL's Epistemic Hold as a physical voltage NULL / half-Vdd state, formalized as the Goukassian Principle in Linear Temporal Logic and implemented in SystemVerilog assertions, is the sole currently-specified mechanism that blocks execution without attestation regardless of software, root access, kernel compromise, or firmware manipulation** [VERIFIED from Atomic Auditability paper]. [GAP-ARCHITECTURAL]: the paper presents FPGA and ASIC design specifications; no production deployment claim is made. The residual vulnerabilities identified in Section VIII of the paper - C-element hysteresis drift, dual-rail crosstalk, and completion detection metastability - remain the hardware-layer attack surface [VERIFIED].

### Honest conclusion on the threat environment

**Yes. The Stewardship Custodian model assumes a threat environment that has already changed as of Q2 2026.** The model's defensibility against the APGT ceiling is partial, not complete. The model remains correct in its fundamental architecture and should not be expanded to compensate, because any expansion of Custodian authority to address APGT directly crosses into the architect role - which would be [CONSTITUTIONAL VIOLATION]. The correct response is to locate the enforcement layer honestly: human governance at the software layer for accountability, coordination, and surveillance; DITL hardware at the physical layer for Mandate enforcement.

### Architectural additions without God Mode

(a) Pre-committed PQC migration schedule for all Custodian signing keys and governance records, targeting 2028 completion. (b) Mandatory hardware-attested dual-control signing for Custodian actions. (c) Pre-confirmed alternate Custodians to shorten quorum-replacement windows. (d) Geographic quorum requirements (no single jurisdiction's legal compulsion can drop more than 2 members). (e) Automated provenance verification of all evidence submitted to Custodians, with mandatory disclosure when provenance chain is broken. None require architectural authority. All are janitorial.

---

## 2.6 The Time-Bound Epistemic Hold in governance

When a Type 2 or Type 3 proposal cannot reach the required majority within its decision window, Governance.md specifies that the proposal enters a Time-Bound Epistemic Hold: both bodies must provide written justifications, and at expiration the proposal defaults to rejection unless both bodies independently elevate it.

### Is default-to-rejection the correct failure mode?

Yes, unambiguously, in every comparable critical-system governance domain [VERIFIED].

- **Nuclear weapons surety** applies the "always/never" doctrine formalized in DOE Order 452.1D and DoD Directive 3150.02: weapons must always detonate when authorized and **never detonate in any other environment or for any other reason**. The architectural implementation - enhanced nuclear detonation safety enclosures with stronglinks and weaklinks - produces pure default-to-inactive state. Russia's Dead Hand (Perimeter, operational 1985) is the deliberate counter-example, a fail-deadly rather than fail-safe design, and it is widely regarded as an artifact of deterrence-credibility requirements that do not apply to governance systems [VERIFIED].
- **IAEA safeguards** default to "cannot verify, therefore cannot certify peaceful use" when states refuse Additional Protocol access. Iran's suspension of AP application in February 2021 triggered Board censure resolutions rather than automatic certification [VERIFIED].
- **FDA Emergency Use Authorization** defaults to no authorization absent affirmative findings under FD&C Act §564. A split VRBPAC vote does not produce automatic approval [VERIFIED].
- **Financial market circuit breakers** (Level 1 at -7% S&P 500, Level 2 at -13%, Level 3 at -20% any time) default to no trading during halt. The regime was triggered four times at Level 1 in March 2020 (9, 12, 16, 18 March) and worked as designed [VERIFIED via SIFMA 10th-anniversary retrospective].

**The Saltzer and Schroeder (1975) fail-safe defaults principle** is the formal computer-security version of the same doctrine. It holds that access decisions should be based on permission rather than exclusion - the default is lack of access, and the protection scheme must identify positive conditions under which access is granted. The Time-Bound Epistemic Hold is a direct expression of this principle applied to governance.

The NASA Challenger case is the cautionary counter-example. The Rogers Commission documented that in the 27 January 1986 teleconference, Marshall's Larry Mulloy **inverted the default** - demanding contractors prove it was unsafe to launch rather than demanding they prove it was safe [VERIFIED]. The burden-of-proof inversion produced the catastrophic loss of Challenger the next morning. **The Custodians' Time-Bound Epistemic Hold must never permit similar inversion** [CONSTITUTIONAL TENSION]: any procedural modification that shifts the burden from "proposal must achieve supermajority to proceed" to "proposal proceeds absent supermajority to reject" would cross the line. Governance.md's current formulation is correct. The risk is drift, not current text.

### Is the dual written justification requirement enforceable on-chain?

**No. It is a social and legal commitment only** [VERIFIED]. Smart contract logic can enforce the existence of a published document at a pre-specified content address; it cannot enforce the document's substantive quality or honesty. Enforcement relies on public scrutiny, peer review, and reputational cost. The publication-as-reasoning-leakage concern raised in Section 2.1 applies here as well: written justifications during hold become adversary training data.

### Governance-layer vs hardware-layer Epistemic Hold

This distinction must be stated precisely because confusing the two is the single most common category error in governance-architecture discussion.

**The governance-layer Epistemic Hold is a time-bounded procedural mechanism.** It operates at the level of proposal lifecycles. It is implemented in smart contract voting logic and human deliberation. Its failure mode is timeout-expiration-defaults-to-rejection. It can be modified by any adversary with sufficient access to the contract deployment or the governing bodies.

**The hardware-layer Epistemic Hold, as specified in the Atomic Auditability paper, is a physical voltage state.** It is instantiated as the {0,0} dual-rail NCL NULL/Spacer state in Delay-Insensitive Ternary Logic, implementing a four-phase handshake protocol. The Goukassian Principle in Linear Temporal Logic, formalized in SystemVerilog assertions, specifies that no execution signal may propagate unless the system has entered, recorded, and exited a physically enforced Escrow state [VERIFIED]. Its failure mode is physical: C-element hysteresis drift, dual-rail crosstalk, completion detection metastability. It cannot be modified by software, root access, kernel compromise, or firmware manipulation.

**They are the same principle operating at different layers, not fundamentally different mechanisms** [HIGH]. Both implement "deliberate pause with positive-evidence requirement before proceeding." The governance version pauses proposals; the hardware version pauses execution. The governance version defaults to rejection after a window; the hardware version physically blocks execution until attestation. **The two layers are complementary and mutually reinforcing. Neither replaces the other** [VERIFIED from Atomic Auditability paper structure and Governance.md scope].

The critical distinction the paper formalizes and this report must preserve: **Escrow is a state (physical voltage blocking), not a delay (software-bypassable speed bump)** [VERIFIED]. The governance-layer Hold is technically a delay because proposal re-submission is always possible; the hardware-layer Hold is a state because execution without attestation is physically impossible. This is why DITL hardware reduces but does not eliminate dependence on human Custodian action (Section 2.8).

---

## 2.7 Succession and long-term continuity

Governance.md references a Succession Charter without full specification. Comparable decentralized-protocol succession frameworks provide the calibration set.

### Comparable succession frameworks

The **Bitcoin Core** maintainer chain is the best-documented empirical succession record. Satoshi Nakamoto's last public forum post was 12 December 2010; final email to Mike Hearn 23 April 2011 ("I've moved on to other things. It's in good hands with Gavin and everyone") [VERIFIED]. Gavin Andresen held lead maintainer role until his 7 April 2014 Bitcoin Foundation blog post designating Wladimir van der Laan as successor. Van der Laan announced delegation in January 2021 ("The Widening Gyre") and removed his own merge privileges in February 2023 via PR #27054. The Lead Maintainer role has been formally vacant since 2022; current maintainers include Michael Ford, Andrew Chow, Russ Yanofsky, Gloria Zhao, and Hennadii Stepanov. The control architecture is a trusted-keys file in the repository with multi-sig by convention rather than cryptographic enforcement; maintainers merge locally using signing keys rather than GitHub's merge button to avoid trusting GitHub [VERIFIED]. **Bitcoin is the paradigmatic zombie-governance-resistant system because consensus rules are enforced by node operators, not by a governance body** [HIGH]. The protocol continues regardless of maintainer availability.

The **Linux kernel** formal succession plan was drafted by Intel principal engineer Dan Williams following the Linux Kernel Maintainers Summit in Tokyo, late 2025, and reported publicly in January 2026 [VERIFIED via BigGo News 28 January 2026]. Triggered by Torvalds's unforeseen absence or retirement; process initiation within 72 hours; decision within 2 weeks; decision body is Maintainers Summit invitees plus Linux Foundation Technical Advisory Board; Linux Foundation executes. **The plan emerged after Torvalds renewed his contract, prompting TAB to revisit long-term governance.** The document makes the *succession process* explicit, not the successor.

The **Ethereum Foundation** completed migration of its approximately 160,000 ETH treasury to a Safe multisig smart-account wallet on 22 October 2025 [VERIFIED]. No publicly documented Buterin-specific succession clause exists. Buterin advocates "decentralize your own security" and publicly stated in May 2024 he stores over 90% of personal crypto in multisig. Credible neutrality doctrine (Nakamoto.com, 3 January 2020) provides architectural guidance but not organizational succession. Control is dispersed across multisig signers and Swiss foundation council.

The **Apache Software Foundation** bylaws (adopted 1 June 1999; last material amendment 30 October 2002) distribute succession across Project Management Committees via lazy consensus; no single individual holds catastrophic succession risk at project level [VERIFIED].

**MakerDAO / Sky's Endgame Plan** (ratified 24 October 2022; Constitution ratified 27 March 2023 at 76% in favor) explicitly targets governance ossification as an endpoint: "Endgame State" is a state in which "the scope and complexity of Maker Core will no longer change" [VERIFIED]. This is the first major DeFi protocol to formally design for zombie-stable governance as the goal rather than the failure mode.

### Can the system operate without the founding architect?

Yes, architecturally. **But "operate" and "evolve" are different questions** [HIGH]. The Bitcoin precedent shows a protocol can operate indefinitely with frozen governance - Bitcoin has made only two significant post-2015 soft forks (SegWit in August 2017 and Taproot in November 2021), and consensus rules are enforced by node operators independent of any maintainer. The Smart Contract Treasury's autonomous disbursement, combined with the Custodians' veto-only architecture, means that absent active governance the system defaults to executing previously-approved rules. This is a feature, not a bug, aligned with the janitor-not-architect boundary.

Meaningful evolution, by contrast, requires active human governance. If the Custodians cannot reach quorum and the Technical Council cannot propose, the system is frozen at its current configuration. For an evolving threat landscape - specifically the Q2 2026 AI-assisted adversarial frontier - frozen configuration is not safe. **The Smart Contract Treasury can sustain system operation indefinitely, but it cannot adapt to new threats** [HIGH].

### Zombie governance risk

The specific failure case: mass incapacitation, catastrophic event, or legal prohibition reduces Custodian active members below 9. Type 2 and Type 3 governance freezes. Treasury continues disbursement according to its autonomous rules. Technical Council may continue proposing, but no proposal can receive Custodian approval. Over time, proposals expire via Time-Bound Epistemic Hold and default to rejection.

In this zombie state, **the system is robust against misuse (nothing new can happen) and vulnerable to drift (nothing can adapt)** [HIGH]. The research literature on DAO longevity (Meneguzzo et al., arXiv:2504.11341, April 2025) documents "recurring governance patterns, including low participation rates and high proposer concentration, which may undermine long-term viability" [VERIFIED]. Numerous forks of Compound, SushiSwap post-0xMaki departure (September 2020), and various stablecoin issuers continue paying yields and holding assets because smart contracts execute deterministically - empirical evidence that autonomous treasury operation survives governance failure.

The honest architectural position is that zombie governance is the failure mode the Smart Contract Treasury makes survivable. It is not a good outcome, but it is survivable. The specific Succession Charter provisions that Governance.md should make explicit, based on the comparative record:

- Pre-specified quorum-restoration procedure triggered automatically at specified active-member thresholds (8, 7, 6), without requiring the frozen body itself to act.
- Pre-committed fallback nominating authority if the standard Nominating Committee cannot be constituted (e.g., a standing pool of pre-confirmed external experts whose role activates automatically under specified conditions).
- Explicit scoping of what the Smart Contract Treasury will and will not fund during governance freeze (security patches yes; feature development no).
- Time-bounded sunset on governance freeze, after which the protocol transitions to a more restricted operating mode rather than continuing indefinitely.

None of these require God Mode. All are janitorial specifications of default behavior.

---

## 2.8 Stewardship Custodians verdict

### Core honest tension restated for the Custodian role

**Any software can be modified.** The Stewardship Custodians' voting logic, publication requirements, quorum rules, and veto thresholds are implemented in smart contract code that is modifiable by human developers, advanced AI systems coordinating with human proxies, or state-level adversaries with sufficient access. This is not a theoretical risk; it is an architectural fact. Constitutional governance written in smart contract code is only as strong as the hardware beneath it.

The sole path to genuine enforcement of the Immutable Mandates is DITL hardware, where Epistemic Hold is not a policy commitment but a physical voltage state that cannot be overridden by software, root access, kernel compromise, or firmware manipulation. The Custodians do not replace this requirement. They do not supplement it at the enforcement layer. They operate at a different layer entirely - accountability, auditability, coordination, and public reason-giving. The Custodians' constitutional value is real and load-bearing at that layer. It does not extend to physical prevention of Mandate violation, and any attempt to extend it there would cross from janitor scope into architect scope, which would be a [CONSTITUTIONAL VIOLATION].

### Consolidated verdict on provisions

**Robust provisions** (survive multi-decade horizon and AI-assisted human adversaries):
- The staggered 4-year terms with 8-year cap and 4-year cool-down - the slowest drift mechanism available without God Mode [HIGH]
- The tri-cameral requirement of simultaneous capture of both bodies for any Type 3 action - raises the coordination cost of successful capture substantially [HIGH]
- The asymmetric proposer-blocker architecture, insofar as the janitor-architect boundary is maintained and procedural innovation is constitutionally bounded [HIGH]
- The publication-of-reasoning requirement, as an accountability mechanism despite its reasoning-leakage cost [HIGH]
- Default-to-rejection on expired Time-Bound Epistemic Hold - aligned with every comparable critical-system governance default [VERIFIED]

**Fragile provisions** (degrade meaningfully under sustained adversarial pressure over 10-20 year horizons):
- The 9-of-11 quorum threshold, vulnerable to 3-member attrition via death, legal compulsion, incapacitation, or LLM-assisted pressure [HIGH]
- The Nominating Committee's external-expert selection path, structurally analogous to known capture channels (Federalist Society, ICANN NomCom precedents) [HIGH]
- The no-more-than-2-per-entity diversity rule, which does not bind ideology or upstream coordination mechanisms [HIGH]
- The Mandatory Veto Obligation, enforceable only at social and legal layers, vulnerable to forged evidence under Q2 2026 synthetic media detection rates [HIGH]
- The anti-capture review obligation, vulnerable to alert fatigue on the documented pattern (60-96% override rates across comparable review functions) [HIGH]

**Provisions effectively unenforceable against a sufficiently resourced adversary** (APGT ceiling):
- Any defense that depends on human reviewers authenticating presented evidence [VERIFIED from Diel et al. 2024 meta-analysis]
- Any defense that depends on undetected covert coordination among a minority of Custodians [SPECULATIVE but supported by LLM sockpuppet cost-reduction trajectory]
- Any defense that depends on long-lived classical cryptography for persistent governance records given harvest-now-decrypt-later posture [HIGH]
- Any defense that depends on Custodians' ability to investigate at depth rather than breadth, under alert-fatigue pressure over multi-decade horizons [HIGH]

### Specific recommended strengthening measures (none require God Mode)

1. Pre-confirmed alternate Custodians, vetted in advance but not seated unless a primary departs, to shorten quorum-replacement windows from months to hours.
2. Geographic quorum requirements such that no single jurisdiction's legal compulsion can drop more than 2 members from active count.
3. Verifiable remote attestation of Custodian presence, distinguishing physical detention from resignation.
4. Hardware-attested dual-control signing for all Custodian actions, with mandatory co-signing by at least two geographically separated Custodians.
5. Pre-committed PQC migration schedule for Custodian signing keys and governance records, targeting 2028 completion, aligned with NIST FIPS 203/204/205 finalized August 2024.
6. Mandatory automated provenance verification of all evidence submitted to Custodians, with disclosure when provenance chain is broken, and public logging of all evidence authentication outcomes.
7. Pre-committed Nominating Committee external-expert registry, with candidates declaring interest years in advance and career paths publicly visible, shifting selection corpus from private networks to public ones.
8. Explicit Succession Charter provisions for auto-triggered quorum-restoration procedures, fallback nominating authority, Treasury scoping during freeze, and time-bounded sunset on frozen governance.

### Where DITL hardware reduces or eliminates dependence on human Custodian action

DITL's physical-voltage Escrow state does not replace the Custodians' legitimation, coordination, or public-reasoning functions. It does, however, substantially reduce dependence on human Custodian action for **direct prevention of Mandate violation**. Specifically:

- No Spy: a hardware Escrow state that requires attestation before any sensitive-data execution path proceeds removes the need for Custodians to adjudicate, case-by-case, whether a given proposal creates surveillance risk. The hardware blocks execution regardless of how cleverly the proposal was drafted [VERIFIED from Atomic Auditability paper].
- No Weapon: the same logic applies to weaponization-adjacent execution paths. The Custodians' role becomes reviewing the hardware attestation regime, not adjudicating every proposal.
- No Switch Off: hardware-level guarantees that governance cannot physically disable the system reduce the Custodians' role to verifying compliance rather than enforcing it.

**Where DITL does not substitute:** accountability for which proposals were submitted and by whom; public reasoning about edge cases in Mandate interpretation; anti-capture surveillance of state, corporate, and insider pressure on either body; Nominating Committee integrity; succession. These remain human work at the governance layer [VERIFIED].

The honest reading: **software governance provides accountability, auditability, and coordination. Hardware governance provides enforcement. Both are necessary. Neither alone is sufficient** [VERIFIED as synthesis of Governance.md scope and Atomic Auditability paper scope].

### Constitutional integrity assessment

Does the Custodians' defined scope keep them within the janitor role under adversarial pressure?

**Textually, yes.** The prohibitions on initiating technical proposals, proposing Treasury disbursement rules, submitting node certification changes, defunding the system, modifying Immutable Mandates, and voting on Type 1 decisions are explicit and restrictive. The binding veto is a blocking power, not an origination power. This is janitorial.

**Functionally, under multi-decade sustained pressure, the risk is real that the binding veto becomes architectural.** Every analogous veto-only body in the comparative record has developed de facto proposal power through procedural innovation over long horizons (US Senate committees, UK Lords amendment culture pre-1911, Canadian Senate substantive reports). If the Custodians begin publishing white papers recommending technical directions, or if they begin using the veto prospectively to signal preferences rather than reactively to block violations, the line crosses. **Any such crossing must be flagged as [CONSTITUTIONAL VIOLATION]** and remediated by re-scoping, not by accommodation. The remedy is never to loosen the Technical Council's proposal monopoly; it is always to reaffirm the Custodians' blocking-only role.

The remembered constitutional hard boundary: **governance is the janitor of eternity, not the architect of tomorrow.** The Stewardship Custodians' provisions are strongest when they are most clearly janitorial. Under the Q2 2026 threat frontier, the honest locating of enforcement at the hardware layer is what makes the janitorial scope sustainable. Without DITL hardware below, the pressure to expand Custodian authority to compensate would be immense and eventually irresistible. With DITL hardware below, the Custodians can remain janitors because they do not have to be enforcers.

This is the architecture's deepest coherence, and it is the only coherence that survives sustained adversarial pressure over multi-decade horizons.

---

*End of Section 2.*