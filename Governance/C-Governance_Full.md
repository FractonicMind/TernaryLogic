# Ternary Logic Constitutional Governance: Complete Research Program
**Framework:** Ternary Logic (TL) by Lev Goukassian
**ORCID:** 0009-0006-5966-1243
**Research Date:** Q2 2026
**Status:** Unified Document - All Four Sections (Claude Research Series)

---

## About this document

This file unifies four standalone research reports produced in a single deep-research session examining the constitutional governance architecture of Ternary Logic (TL). Each section was produced independently, with its own verdict and confidence markers, and is reproduced here in full without modification. The four sections are:

- **Section 1:** `Technical_Council.md` - Is the Technical Council technically sound, currently defensible, and adequate to govern protocol evolution without becoming a capture vector?
- **Section 2:** `Stewardship_Custodians.md` - Can the Stewardship Custodians survive the capture vectors in Article VII over a multi-decade horizon and against AI-assisted adversaries?
- **Section 3:** `Smart_Contract_Treasury.md` - How does on-chain Treasury enforcement interact with DITL hardware enforcement, and what is the honest minimum viable governance architecture?
- **Section 4:** `Governance_Synthesis.md` - What does the complete TL architecture guarantee, what requires DITL hardware, and does the architecture stay within the janitor role?

**Reference documents consulted:**
- Governance.md: `https://raw.githubusercontent.com/FractonicMind/TernaryLogic/refs/heads/main/Governance.md`
- Atomic Auditability paper (DOI: 10.5281/zenodo.18716142): `https://raw.githubusercontent.com/FractonicMind/TernaryLogic/refs/heads/main/Hardware_Architecture/Atomic_Auditability_in_Financial_Execution_Pipelines_via_Hardware-Enforced_Ternary_States.md`

**Canonical terminology used throughout:**
- Epistemic Hold - State 0. Never "pause," "stall," "freeze," or "hold state."
- Escrow - the hardware execution state mapped to NCL NULL/Spacer
- No Spy, No Weapon, No Switch Off - the Three Mandates. Exact phrasing always.
- DITL - Delay-Insensitive Ternary Logic
- Goukassian Principle - No execution signal may propagate unless the system has entered, recorded, and exited a physically enforced Escrow state
- No Log = No Action - the causal invariant

---

---

# Section 1: Technical_Council.md
## Ternary Logic Constitutional Governance Research - Section 1
**Research Date:** Q2 2026
**Status:** Standalone Report - Section 1 of 4

---

## Core honest tension stated up front

Any software can be modified. Humans with commit rights can modify it. Automated agents with root access can modify it. State-level adversaries with supply-chain reach can modify it. This is not a theoretical risk; it is an architectural fact. Constitutional governance expressed in smart contract code is only as strong as the hardware beneath that code. The sole path to genuine enforcement of the Immutable Mandates is DITL hardware, where Epistemic Hold is not a policy commitment but a physical voltage state (NULL / half-Vdd) that cannot be overridden by software, root access, kernel compromise, or firmware manipulation. [NOVEL]

This does not invalidate the Technical Council as specified in Governance.md. It locates it honestly. Software governance provides accountability, auditability, and coordination. Hardware governance, via the Goukassian Principle expressed in Linear Temporal Logic and SystemVerilog assertions, provides enforcement. Both are necessary. Neither alone is sufficient. [HIGH]

---

## 1.1 Tri-cameral design and three-body equilibrium

**Finding: The tri-cameral architecture is defensible in principle but has no exact analogue in decentralized protocol governance as of Q2 2026.** [VERIFIED]

The closest production precedent is the Optimism Collective's bicameral design, which separates a Token House (protocol upgrades, treasury, project incentives) from a Citizens' House (soulbound membership, with a 30 percent veto threshold on protocol upgrades exercised during a one-week window after Token House passage). A Developer Advisory Board (DAB) adds a third advisory tier with a separate seven-day public veto window on protocol changes.[1] This is structurally similar to TL's Technical Council plus Stewardship Custodians plus Treasury, but Optimism's Citizens' House veto is executed off-chain via Snapshot and operational finalization still runs through the Optimism Foundation, so it is not purely trustless forwarding.[1] Optimism is the strongest extant precedent for cross-chamber non-censorable forwarding, but it is weaker than what Governance.md specifies. [HIGH]

Outside decentralized protocols, genuine multi-organ structures exist, but very few establish three coequal veto-bearing bodies. The IAEA has three organs (General Conference, Board of Governors, Secretariat), but they are hierarchical rather than coequal.[2] The IETF separates IESG (standards approval), IAB (architectural oversight and appeals), NomCom (appointments), and IETF LLC (administration only, explicitly excluded from standards authority per RFC 8711),[3] which is the cleanest real-world precedent for separating operational, architectural, and administrative authority. The WTO Dispute Settlement Body uses a Panel plus Appellate Body structure, but the Appellate Body has been non-functional since December 10, 2019 because a single member state refused to approve new appointments.[4] This is a directly relevant cautionary precedent for any governance chamber whose membership depends on consensus replenishment.

**Nine members is at the lower bound of defensibility under standard BFT analysis.** [VERIFIED] Castro-Liskov PBFT requires n >= 3f+1 for safety under Byzantine faults.[5] A nine-member Technical Council can tolerate f = 2 Byzantine members safely. Three compromised members breaks safety. The specified 7-of-9 quorum formalizes this: any two members offline or captured cannot halt governance, but any three can. This is a reasonable design point, but it is not generous.

On deadlock versus capture: permanent orbital tension between Technical Council (proposal monopoly, no veto) and Stewardship Custodians (veto, no proposal) makes explicit collusion the only path to unilateral capture, because neither body can act alone on Type 3 decisions. The cost is latent deadlock risk, analyzed in 1.2. [HIGH]

---

## 1.2 Technical Council vote rights architecture

This is the spine of TL constitutional governance. The separation of exclusive proposal rights from final veto authority is the core capture-resistance mechanism, and it is also the core deadlock-generation mechanism.

### Exclusive proposal rights plus no veto

**Exclusive proposal rights without veto authority is a well-attested governance pattern that reliably produces agenda-setting dominance, not deadlock, under normal operation.** [HIGH] The clearest precedent is the EU Commission's quasi-monopoly on legislative initiative under TFEU, which has been criticized since the 1990 Parliament resolution as producing a "democratic deficit" precisely because Commission agenda-setting, combined with a reviewing body that can reject but cannot initiate, produces de facto Commission dominance regardless of formal veto distribution.[6] The April 2022 AFCO committee resolution (22-5-1) and the 2019 von der Leyen commitment to Parliament initiative rights both reflect sustained pressure against this architecture.[6]

For TL, this means: the structural risk is not that the Custodians will be unable to veto, but that the Custodians will receive only proposals pre-shaped by the Technical Council, with no ability to force consideration of alternatives. The Custodian veto is a stop condition, not a steering mechanism. [HIGH] If capture occurs, it will likely appear as narrowing of the proposal space rather than as override of veto.

### Sustained disagreement and deadlock

If Technical Council and Custodians enter sustained disagreement on a Type 3 matter, Governance.md as specified produces status quo preservation, not deadlock, because the Diamond Proxy remains operational and Immutable Mandates continue to hold regardless of upgrade cadence. The risk surfaces only when the status quo itself becomes untenable - for instance when a cryptographic primitive is broken (see 1.7) and upgrade is required for continued safety. **[CONSTITUTIONAL TENSION]** In that narrow window, indefinite Custodian veto of a Technical Council-proposed migration could leave the protocol running on broken cryptography. Governance.md contains no time-bound escalation mechanism for this case. [GAP-ARCHITECTURAL]

### Type 1 emergency continuity fallback

Governance.md grants the Technical Council unilateral authority (simple majority, no Custodian involvement) to migrate Anchor Host Chain state under emergency conditions. **This is the single largest concentration of unilateral authority in the Technical Council's mandate, and it is the point where capture risk is highest.** [HIGH]

The relevant failure precedents:
- Build Finance DAO takeover (February 10, 2022): 3.8 percent turnout passed a treasury-draining proposal because monitoring infrastructure failed to raise an alarm.[7] Loss approximately $470,000.
- Compound Proposal 289 (July 28, 2024): Attacker-aligned wallets passed a $24M treasury transfer by timing the vote for low participation.[8]
- Beanstalk governance attack (April 17, 2022): $182M drained via a flash-loan-purchased supermajority executing emergencyCommit in the same transaction.[9] The emergency execution path was the exploit.

Each of these used an emergency-or-unilateral pathway to bypass deliberation. **Recommended constraint without adding God Mode: require that any Type 1 emergency Anchor migration be accompanied by a mandatory, non-censorable Custodian notification with a minimum 72-hour observation window before execution finality, during which Custodians may escalate to a Type 2 reversal vote.** [NOVEL] This preserves Technical Council operational autonomy while closing the unilateral-emergency-action attack surface.

### 7-of-9 quorum under adversarial attrition

Under standard availability assumptions, 7-of-9 is robust. Under adversarial attrition, it is fragile. [HIGH] Three coordinated absences halt the Technical Council. The WTO Appellate Body precedent shows that a single state-level adversary can paralyze a body requiring consensus replenishment for years.[4] **Recommended: Governance.md should specify a documented succession protocol with a pre-authorized alternate bench such that vacancies can be filled within a defined window (e.g., 30 days) by Custodian confirmation under existing Type 2 rules.** [GAP-ARCHITECTURAL]

### Non-censorable forwarding enforceability

The Governance.md claim that Type 3 proposals passing the Technical Council are "automatically and non-censorably forwarded" to the Custodians is technically enforceable on-chain within a single chain via the Compound Governor Bravo plus OpenZeppelin TimelockController pattern: once queue() is called, any address can call execute() after the timelock expires, with no proposer discretion.[10] A compromised Technical Council cannot suppress forwarding of an already-queued proposal without compromising the Diamond Proxy's Governance facet itself. [VERIFIED]

The weak point is not forwarding; it is proposal construction before forwarding. A compromised Technical Council can simply decline to propose, and the Custodians cannot force a proposal onto the agenda. This is the EU Commission problem reproduced on-chain. [HIGH]

---

## 1.3 Diamond Standard (EIP-2535) current status as of Q2 2026

**ERC-2535 is FINAL as of 2023 (PR #5802 merged), confirmed on the canonical ERCs repository.** [VERIFIED][11]

Known vulnerability classes in diamond implementations: the reference Diamond.sol fallback does not implement a reentrancy guard; Cyfrin CodeHawks audit of Beanstalk "The Finale" (May 2024) flagged this as systemic.[12] Storage collisions between facets from incorrect manual slot management are documented.[13] The EIP itself warns that diamondCut allows arbitrary execution with access to the diamond's storage through delegatecall and must be access-restricted carefully.[11]

**No confirmed mainnet post-mortem of a major exploit attributable specifically to an EIP-2535 diamond-pattern bug was located for 2023 through Q2 2026.** [GAP-RESEARCH]

Industry consensus in 2025 through Q2 2026 has shifted away from diamonds for governance-tier contracts unless the 24KB size limit forces the pattern. [HIGH] Nick Mudge is now proposing ERC-8109 as a simplified successor standard.[14] The Diamond Proxy with upgradeability permanently renounced, plus four upgradeable facets on UUPS, is architecturally sound for "maintain but not mutate." [HIGH]

---

## 1.4 UUPS (EIP-1822) and upgradeability as of Q2 2026

**ERC-1822 is formally STAGNANT, confirmed on eips.ethereum.org.** [VERIFIED][15] Despite formal status, UUPS is the de facto dominant upgradeable-proxy pattern in 2025-2026 via OpenZeppelin's UUPSUpgradeable combined with EIP-1967 storage slots and ERC-7201 namespaced storage (Final status).[16]

Known UUPS vulnerabilities: September 2021 OpenZeppelin advisory GHSA-5vp3-v4hc-gx76 (CVE-2021-41264) disclosed an uninitialized-implementation attack allowing attacker to become owner and selfdestruct the implementation, bricking all proxies.[17] Post-Cancun EIP-6780 (March 2024) largely neutralizes the "destroy implementation, brick proxy" variant.[18]

Known exploits using upgrade mechanisms as attack vectors include PAID Network (March 2021, proxy admin key compromise, ~$3M realized)[19] and Audius governance takeover (July 23, 2022, storage layout collision between proxyAdmin variable and Initializable.initializing flag, approximately $6M)[20].

Joint-Approval before upgradeTo execution is enforceable. The residual risk is authorized but malicious implementation content, which cannot be detected by any on-chain check and requires off-chain audit before Custodian approval. **Governance.md should explicitly require that Type 3 proposals include audit artifacts as a prerequisite for the Custodian review window.** [GAP-ARCHITECTURAL]

---

## 1.5 The software honesty problem

### Blockchain-layer compromise scenarios

A constitutionally immutable Diamond Proxy provides zero protection against a 51 percent attack on the underlying chain that reorganizes the state containing governance votes. MEV extraction can influence vote ordering. Consensus manipulation can censor Custodian veto transactions during the Type 3 review window. **These are layer-below-governance failure modes that the Technical Council cannot address by any amount of smart contract engineering.** [VERIFIED]

Foundry USA plus AntPool together control approximately 55 to 60 percent of Bitcoin hashrate as of Q2 2026.[21] Lido plus Coinbase collectively control more than 33 percent of staked ETH.[22] The May 11-12, 2023 Ethereum finality delays from a Prysm/Teku attestation bug,[23] and the late-2025 post-Fusaka Prysm v7.0.0 bug that dropped voting participation by 25 percent and brought the network within 9 percent of losing finality supermajority,[24] both demonstrate that client monoculture remains a live failure mode.

### "Absence of function" as No Switch Off enforcement

Article VIII states that No Switch Off is enforced by the absence of pause(), suspend(), freeze(), and admin_kill() in the Protocol Contract. **This is genuinely sufficient against application-layer pause authority, but it does not prevent equivalent effect through other means.** [HIGH] Chain-level censorship - if the validator set of the host chain excludes all transactions to the Protocol Contract - is the fundamental limit of software-layer No Switch Off enforcement. [VERIFIED]

### The Goukassian Principle applied to governance

The Atomic Auditability paper's formalization is: G(execute → P(escrow_recorded ∧ auditable)). Applied to TL governance contract execution, the analogous LTL formula is: G(execute_upgrade → P(escrow_recorded ∧ custodian_window_closed ∧ no_veto)). Implementation at the hardware level would require the Governance facet's execute() opcode to trigger a DITL Escrow state on dedicated hardware attesting that the Custodian review window expired without veto, with the NULL voltage state physically blocking execution propagation until attestation is produced. [SPECULATIVE]

### Where software governance becomes effectively unenforceable

**Software governance becomes effectively unenforceable at the moment a sufficiently-resourced adversary can either (a) modify the binaries running on validators, (b) censor finality-relevant transactions at a majority of validators, or (c) compromise the key material of a quorum of governance participants faster than revocation can occur.** [HIGH]

**DITL hardware enforcement changes exactly one thing: it makes the physical Escrow state non-software-overridable, so the gap between commit and audit closes at the hardware boundary.** It does not prevent binary compromise upstream, does not prevent chain-level censorship, does not prevent key-material compromise. It does prevent any compromised software stack from causing execution without recorded audit evidence. That is the specific property DITL provides and no software design can replicate.

---

## 1.6 Host Chain selection (Article VI) as of Q2 2026

**Based on Q2 2026 data, the defensible minimum anchor set is Bitcoin, Ethereum, Cardano, Polkadot, Tezos.** [HIGH]

| Chain | Nakamoto coefficient | Key risk |
|---|---|---|
| Bitcoin | 4 (pool layer) | Foundry USA + AntPool ~57% hashrate |
| Ethereum | 2 (entity level) | Lido + Coinbase >33% stake; AWS hosts >50% of nodes |
| Cardano | 22 | Single dominant client (Amaru Rust client maturing) |
| Polkadot | 178 (highest of tracked L1s) | Reference client monoculture |
| Tezos | 14 | Smaller TVL |

Chains that appeared strong but showed vulnerability: Solana (multiple multi-hour halts 2023-2024); Aptos (October 2023 5h+ halt); all Ethereum L2s retain centralized sequencers - disqualified as independent anchors.

The "any one Anchor survives" liveness guarantee is achievable for the recommended five-chain set under Q2 2026 infrastructure conditions, conditional on maintaining distance from shared cloud providers. [HIGH]

---

## 1.6.1 Cross-chain vote security and relay integrity

**The "any one honest prover plus safe source chain equals integrity" property is genuinely achievable in production as of Q2 2026 for Ethereum-Cosmos only, through IBC Eureka powered by Succinct SP1 (launched April 10, 2025).** [VERIFIED][25]

Historical relay failures applied to TL Anchor notarization:

| Failure | Date | Loss | Mechanism |
|---|---|---|---|
| Wormhole | Feb 2, 2022 | $320M+ | Signature verification bypass |
| Ronin | Mar 23, 2022 | $624M | 5-of-9 validator key compromise |
| Nomad | Aug 1, 2022 | $190M | Zero-hash replay after upgrade |
| Multichain | Jul 2023 | $125-210M | CEO detained, MPC keys inaccessible |
| Orbit Chain | Dec 31, 2023 | $81.5M | 7-of-10 multisig key compromise |

**[CONSTITUTIONAL TENSION]: If Type 3 proposals must be notarized on-chain before Custodian review, and federated relay infrastructure is compromised, Governance.md contains no protocol-level deadlock resolution mechanism.** [GAP-ARCHITECTURAL]

**Mitigation without adding God Mode: require that the Anchor relay model use IBC-class trust-minimized infrastructure (permissionless relayers plus on-chain light clients, or ZK-light-client bridges with permissionless provers), explicitly excluding federated multisig relay sets.** [NOVEL]

---

## 1.7 Post-quantum readiness

**Governance.md as written is silent on post-quantum cryptography, and the cryptographic primitives implied by typical blockchain governance (ECDSA secp256k1, BLS12-381, KZG commitments) are all Shor-vulnerable.** [VERIFIED]

NIST finalized FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) on August 13, 2024.[26] NSA CNSA 2.0 and NIST IR 8547 deprecate RSA/ECDSA/ECDH after 2030 and disallow after 2035.[27] No PQC signature verification precompile is live on Ethereum mainnet as of Q2 2026.[28]

**A PQC migration can be executed within Governance.md Article V without violating Article I immutability, because PQC migration is a "major cryptographic upgrade" to the four upgradeable facets, not a modification of the Immutable List.** [HIGH] This is a Type 3 decision requiring >=75% Joint-Approval. Governance.md should explicitly add language scheduling a pre-2030 Type 3 PQC migration proposal with candidate primitives ML-DSA-87 (NSA CNSA 2.0 selected[27]) and a SLH-DSA fallback. [GAP-ARCHITECTURAL]

Gidney's May 2025 result reduced the qubit requirement to factor RSA-2048 to less than 1 million noisy physical qubits.[29] Treat 2030-2035 as the operational migration window. [HIGH]

---

## 1.8 Technical Council verdict

### Core honest tension restated

The Technical Council is the software-layer architect of protocol evolution within a framework that explicitly forbids modification of its Immutable List. Its software code is modifiable by any sufficiently-resourced adversary. The Immutable Mandates it cannot modify are also, at the software layer, only as strong as the hardware running the validator set, the relay infrastructure, and the anchor notarization network. DITL hardware enforcement via physical Escrow states is the only path to enforcement that survives full software compromise. Software governance remains necessary for accountability, auditability, and coordination. Neither layer alone is sufficient.

### Consolidated verdict

**Robust:** Tri-cameral separation of proposal, veto, and autonomous treasury; 7-of-9 quorum BFT-defensible under standard assumptions; Diamond Proxy with permanently renounced upgradeability plus UUPS facets controlled by Joint-Approval; non-censorable forwarding of queued Type 3 proposals; absence of pause()/suspend()/freeze()/admin_kill().

**Fragile:** Type 1 emergency Anchor migration authority (single largest capture vector); exclusive proposal rights without Custodian counter-proposal (EU Commission precedent); 7-of-9 quorum under coordinated absence (WTO Appellate Body precedent); federated cross-chain relay infrastructure; sustained Custodian veto of cryptographically-urgent proposal has no time-bound escalation.

**Outdated:** PQC migration not scheduled; Diamond Standard reference does not acknowledge industry drift toward ERC-7201 and pending ERC-8109; EIP-1822 formal Stagnant status unacknowledged.

### Recommended updates to Governance.md

1. Add 72-hour Custodian observation-and-escalation window for Type 1 emergency Anchor migrations.
2. Specify pre-authorized alternate bench and 30-day succession protocol for Technical Council vacancies.
3. Restrict Anchor relay layer to IBC-class trust-minimized infrastructure, excluding federated multisig relays.
4. Schedule pre-2030 Type 3 PQC migration with ML-DSA-87 primary and SLH-DSA fallback.
5. Require that Type 3 proposals include audit artifacts as prerequisite for Custodian review window.
6. Add time-bound escalation for cryptographically-urgent proposals under sustained Custodian veto.
7. Permit non-architectural migration to ERC-8109 or equivalent Final successor standard.

### DITL hardware and the Technical Council role

DITL does not expand Technical Council authority; it restricts what any compromised version of that authority can accomplish. Epistemic Hold becomes a physical voltage state (NULL / half-Vdd), so no software compromise of the Governance facet can force execution past it. The commit-audit gap at the governance-pipeline level closes at the hardware boundary. A fully captured Technical Council plus Custodian set still cannot produce execution without recorded audit evidence.

### Constitutional integrity assessment

**The Technical Council's defined scope in Governance.md keeps it within the janitor role.** [VERIFIED] Its authority covers protocol evolution, code stewardship, certification, monitoring, and audit cadence. It has no authority to modify the Immutable List, no authority over Treasury disbursement without Custodian approval, no pause or kill function. The one boundary-adjacent power is Type 1 emergency Anchor migration, which is operational continuity, not architectural redesign. **No part of the Technical Council's defined scope crosses into architect territory.** [HIGH] No [CONSTITUTIONAL VIOLATION] identified.

---

---

# Section 2: Stewardship_Custodians.md
## Ternary Logic Constitutional Governance Research - Section 2
**Research Date:** Q2 2026
**Status:** Standalone Report - Section 2 of 4

---

## Executive summary and the core honest tension

The Stewardship Custodians, as specified in Governance.md, are a credible but fragile institution. **Their binding veto survives human-only adversaries with high probability over 10-year horizons and degrading probability over 20-30 year horizons.** [HIGH] Their mandatory veto obligation, anti-capture review duty, and publication-of-reasons requirement are enforceable only as social and legal commitments, not as on-chain code. [VERIFIED] The 9-of-11 quorum requirement is a defined adversarial target: three disabled, compromised, or legally compelled Custodians are sufficient to freeze Type 2 and Type 3 governance. [HIGH]

The core honest tension: any software-layer governance architecture, including the Custodians' on-chain voting contracts, is modifiable by any adversary with sufficient access to the execution substrate. Constitutional governance written in smart contract code is only as strong as the hardware beneath it. The Stewardship Custodians provide accountability, auditability, and coordination; they do not, and cannot, provide physical enforcement. Physical enforcement of the Immutable Mandates belongs to DITL hardware, where Epistemic Hold is instantiated as a dual-rail NULL voltage state that cannot be overridden by software, root access, kernel compromise, or firmware manipulation. Both layers are necessary. Neither alone is sufficient.

---

## 2.1 Stewardship Custodians vote rights architecture

The Custodians' vote rights implement an asymmetric proposer-blocker architecture: one body (the Technical Council) holds monopoly on origination; the other (the Custodians) holds binding constitutional veto but cannot itself originate.

### The asymmetry under historical pressure

Four constitutional analogs provide the calibration set. The UK House of Lords held absolute veto on legislation until the 1909 budget crisis forced the Parliament Act 1911, which reduced it to a two-year delaying power.[30] The Canadian Senate retains formal absolute veto but has applied it sparingly; the 1988 and 1990 disputes required invocation of the never-previously-used Section 26 of the Constitution Act.[31] Tsebelis veto-player theory (2002) establishes that pure veto-only bodies tend to develop de facto proposal power over time through procedural innovation.[32]

The cross-case pattern: **pure veto-only bodies tend to develop de facto proposal power over time through procedural innovation, unless restrained by explicit constitutional lock-in or a durable legitimacy gap.** [HIGH] The Custodians face exactly this drift risk. The prohibition on Custodian-initiated technical proposals is textually explicit, but **every analogous body has found ways around such prohibitions over multi-decade horizons.** [HIGH]

The closest mission-critical analog is the nuclear Two-Man Rule combined with Permissive Action Links, operational across the US arsenal from 1962 to present. Two independent authorized individuals must affirmatively act to arm or launch. This architecture has not failed catastrophically in 63 years. [VERIFIED] Its durability comes from **physical enforcement of the separation, not procedural enforcement** - which is precisely the move the Atomic Auditability paper proposes for Epistemic Hold.

### The mandatory veto obligation

Governance.md states Custodians "must veto any proposal creating credible risk of violating any Immutable Mandate." This obligation is **enforceable only at the social and legal layer, not on-chain.** [VERIFIED] Smart contract voting logic cannot distinguish between a principled vote and a compelled one.

### The publication requirement on veto

Strengthening effects: public reasoning creates legal record; raises reputational cost of sham vetoes; creates audit trail for detecting capture. Weakening effects: **published veto justifications are a training corpus for adversarial circumvention** [SPECULATIVE but directly supported by documented offensive-AI practice as of Q2 2026]. The published reports become the specification against which hostile proposals are optimized. [CONSTITUTIONAL TENSION]: transparency is constitutionally required and ethically correct, yet provides operational intelligence to patient adversaries.

### The 9-of-11 quorum as adversarial target

**The WTO Appellate Body quorum collapse of December 2019 is the canonical precedent.** The United States blocked all reappointments from May 2016 onward. On December 10, 2019 the Body lost quorum; by December 2020 all seven seats were vacant.[4] A single state with negative-consensus blocking power produced full collapse through inaction alone, with no formal rule change required. The Body has remained non-functional for six years.

Three Custodians can be removed via: death or incapacitation; targeted legal compulsion across jurisdictions; coordinated resignation under duress; LLM-assisted personalized pressure campaigns. The $25M Arup deepfake CFO fraud (January 2024) demonstrates that individualized video-and-voice manipulation at scale is now operational. [VERIFIED][33]

**Specific recommended strengthening without God Mode:** (a) pre-confirmed alternates - vetted but not seated unless a primary departs; (b) geographic distribution of quorum such that no single jurisdiction's legal compulsion can drop more than 2 members; (c) verifiable remote attestation of presence distinguishing physical detention from resignation.

---

## 2.2 Capture vector analysis

### State capture

**The NIST / Dual_EC_DRBG episode (2004-2014)** is the canonical state-capture-of-a-standards-body precedent. [VERIFIED] The ANSI X9F1 committee that originated Dual_EC included NSA employees. NIST published SP 800-90A in 2006. Shumow and Ferguson demonstrated the backdoor structure at CRYPTO 2007. The December 2013 Reuters reporting of a $10 million NSA payment to RSA triggered NIST's revised SP 800-90A Rev.1 in April 2014 removing the algorithm.[34] Time horizon: approximately 9 years from standardization to retraction. Layer: cryptographic, social, economic. **A captured Custodian majority that collectively defers to state technical expertise would not have prevented Dual_EC.** [HIGH]

The UN Security Council veto pattern: 2024 saw seven vetoed draft resolutions with eight total vetoes - the most since 1986.[35] **Single-state blocking in consensus bodies generalizes to single-bloc blocking in supermajority bodies**: a Custodian body with a 75% veto threshold can be blocked by a coordinated bloc of 3.

### Corporate capture

**Basel Committee on Banking Supervision capture of Basel III** is documented in Lall (2012) and Bengtsson (2015 ECB working paper). [VERIFIED] BCBS "mainly accommodated the preferences of stakeholders from the financial industry." The Basel III Endgame proposal (July 2023) was substantially weakened in mid-2024 after industry lobbying.

**ISO/IEC OOXML fast-track (2006-2008):** Martin Bryan, convenor of ISO/IEC JTC1/SC34/WG1, resigned citing capture; Sweden's national vote was invalidated after a Microsoft partner admitted paying for votes.[36] **Diversity requirements did not prevent capture; they facilitated it, because the adversary simply populated each diversity category with aligned members.** [VERIFIED]

### Insider collusion - XZ Utils

The XZ Utils / "Jia Tan" backdoor (2021-2024) is the canonical multi-year insider-grooming precedent. [VERIFIED] Total operation: approximately 2.6 years; only 8 of hundreds of commits were malicious. The attacker used sockpuppet pressure campaigns to exploit the sole maintainer's publicly-stated mental health struggles. Linux Foundation's April 2026 report explicitly warns this template is being replicated.[37]

**Mechanism, layer, TL response:** (1) Patient multi-year social engineering. (2) Social plus identity layer. (3) Would TL's architecture have helped substantially, because any release-critical action requires quorum and supermajority - attack would need to compromise multiple Custodians simultaneously. (4) Additional constraint: pre-commitment of signing keys to hardware security modules with dual-control attestation.

### The 75% supermajority under sustained pressure

Two decades is sufficient time to appoint or influence a majority of seats through legitimate Nominating Committee channels if the Committee is itself compromised. The FSOC designation regime oscillated across multi-decade political cycles, with each administration eroding prior framework. [VERIFIED] Supermajority thresholds slow but do not halt such oscillation.

---

## 2.3 Nominating Committee integrity

**The three external experts on the Nominating Committee are selected and approved by existing Custodians - this is the capture entry point.** [HIGH] The ICANN NomCom is the closest operational analog; in June 2025 ICANN formally intervened in AFRINIC Board elections after two NomCom members with conflicts were appointed.[38]

The Federalist Society pipeline produced 86% FedSoc affiliation in Trump circuit and Supreme Court appointees over four years without any formal entity overlap - **ideological capture operates through a different coordination mechanism than institutional capture, and diversity rules addressed to institutions do not bind ideology.** [VERIFIED]

Cool-down periods: Wright and Booker (2010, Advances in Accounting) found that perceived auditor independence increases significantly with a 1-year cooling-off period but "increasing the length from one year to two years fails to significantly increase perceptions of independence." [VERIFIED] Jose Manuel Barroso joined Goldman Sachs two months after his EU cooling-off window expired (July 2016).[39] The honest reading: the 4-year cool-down is better than shorter alternatives but does not close the capture vector.

---

## 2.4 Governance fatigue and temporal degradation

The WTO Appellate Body collapse (December 2019 quorum loss, all seven seats vacant by December 2020, non-functional for six years) is the clearest cautionary case. [VERIFIED]

Alert fatigue across comparable review functions: approximately 62% of security alerts ignored entirely (CardinalOps 2024); EHR drug-allergy alert override rates reach 96%; 331 alerts required on average to prevent 1 adverse drug event (JAMA 2024).[40] **Unless the Custodians' review workflow is itself supported by automated pre-triage with careful design, governance fatigue is the most likely failure mode over 10-20 year horizons.** [HIGH]

What degrades first under alert overload: review of edge cases requiring judgment (as opposed to pattern matching) degrades first; proactive anti-capture surveillance is deferred in favor of reactive vote-on-proposal work; investigation depth drops before investigation count; inter-Custodian deliberation quality drops before voting participation.

---

## 2.5 The human-AI adversarial frontier

**As of Q2 2026, the Stewardship Custodian architecture has no defenses against AI-assisted capture that are qualitatively different from defenses against human-only capture.** The defenses - diversity, supermajority, quorum, publication, cool-down, anti-capture review - were designed against human adversaries. They are not useless; they still raise the cost of attack. They are no longer qualitatively suited to the threat frontier. [HIGH]

**Human detection of synthetic deepfake media: Diel et al. (Computers in Human Behavior Reports, December 2024), meta-analysis of 56 studies with 86,155 participants, found overall human detection of synthetic media at 55.54% (95% CI 48.87-62.10), with every modality's confidence interval crossing chance.** [VERIFIED][41] The January 2024 Hong Kong deepfake CFO fraud ($25.6M via multi-person synthetic video conference with all participants except the victim being deepfakes) is the canonical operational precedent. [VERIFIED][33]

For the Custodians: any evidence presented in support of a proposal - video testimony, audio recordings, document photographs, attributed quotations - **cannot be reliably authenticated by human review alone in Q2 2026.** [VERIFIED]

---

## 2.5.1 Advanced Persistent Governance Threat (APGT) Ceiling

The APGT ceiling is defined as a state-level adversary with: quantum decryption posture (harvest-now-decrypt-later); AI-generated synthetic video and document evidence at Q2 2026 quality levels; legal compulsion power over 30%+ of Custodian jurisdictions.

Global Risk Institute Quantum Threat Timeline Report 2025 (seventh edition, April 2026): 28-49% probability of CRQC within 10 years. [VERIFIED][42]

**Which Custodian provisions survive APGT:** Staggered 4-year terms; tri-cameral requirement of simultaneous capture of both bodies; publication-of-reasoning as accountability record.

**Which provisions fail against APGT:** The 75% supermajority (3-member compelled bloc achieves paralysis); 9-of-11 quorum (3-member compelled absence achieves paralysis); Mandatory Veto Obligation under forged evidence; anti-capture review under alert volume overload.

**Which provisions require DITL hardware:** The Immutable Mandates themselves. No Spy, No Weapon, No Switch Off must be enforced below the layer at which an APGT adversary can operate. [VERIFIED from Atomic Auditability paper]

**Honest conclusion: Yes. The Stewardship Custodian model assumes a threat environment that has already changed as of Q2 2026.** [GAP-ARCHITECTURAL]

**Architectural additions without God Mode:** (a) Pre-committed PQC migration schedule targeting 2028 completion. (b) Mandatory hardware-attested dual-control signing for Custodian actions. (c) Pre-confirmed alternate Custodians. (d) Geographic quorum requirements. (e) Automated provenance verification of all evidence submitted to Custodians.

---

## 2.6 The Time-Bound Epistemic Hold in governance

Default-to-rejection is the correct failure mode. Every comparable critical-system governance domain applies it: nuclear weapons surety enforces fail-safe defaults; IAEA safeguards default to "cannot certify peaceful use"; financial market circuit breakers default to no trading. The Saltzer and Schroeder (1975) fail-safe defaults principle is the formal computer-security version. NASA Challenger is the cautionary counter-example: the Rogers Commission documented that Marshall's Larry Mulloy inverted the default, demanding contractors prove it was unsafe to launch rather than demanding they prove it was safe. [VERIFIED]

**The dual written justification requirement during hold: not enforceable on-chain. It is a social and legal commitment only.** [VERIFIED]

**The governance-layer Epistemic Hold vs. the hardware-layer Epistemic Hold:**

The governance-layer Hold is time-bounded and procedural: proposals default to rejection after a window; it can be modified by any adversary with sufficient access to the contract.

The hardware-layer Epistemic Hold, as specified in the Atomic Auditability paper, is a physical voltage state: instantiated as {0,0} dual-rail NCL NULL/Spacer, implementing a four-phase handshake, formalized in LTL via the Goukassian Principle. It cannot be modified by software, root access, kernel compromise, or firmware manipulation.

**They are the same principle operating at different layers, not fundamentally different mechanisms.** [HIGH] Both implement "deliberate pause with positive-evidence requirement before proceeding." The governance version pauses proposals; the hardware version pauses execution. **Escrow is a state (physical voltage blocking), not a delay (software-bypassable speed bump).** [VERIFIED]

---

## 2.7 Succession and long-term continuity

The Bitcoin Core maintainer chain is the best-documented empirical succession record. Satoshi's last email to Mike Hearn was April 23, 2011. The Lead Maintainer role has been formally vacant since 2022; the protocol continues regardless of maintainer availability. [VERIFIED] This is the paradigmatic zombie-governance-resistant system because consensus rules are enforced by node operators, not by a governance body.

The Linux kernel formal succession plan was drafted following the Linux Kernel Maintainers Summit in Tokyo, late 2025, reported publicly January 2026. [VERIFIED] MakerDAO's Endgame Plan (ratified October 24, 2022; Constitution ratified March 27, 2023 at 76% in favor) explicitly targets governance ossification as an endpoint. [VERIFIED]

**Whether the Treasury can operate indefinitely without active human governance:** Yes, operationally. No, for evolution. Bitcoin demonstrates a protocol can operate indefinitely with frozen governance. Meaningful evolution requires active human governance. **The Smart Contract Treasury can sustain system operation indefinitely, but it cannot adapt to new threats.** [HIGH]

**Zombie governance risk specific provisions that Governance.md should make explicit:** pre-specified quorum-restoration procedure triggered automatically at specified active-member thresholds; pre-committed fallback nominating authority; explicit scoping of what the Treasury will and will not fund during governance freeze; time-bounded sunset on governance freeze.

---

## 2.8 Stewardship Custodians verdict

### Core honest tension restated

**Any software can be modified.** The Custodians' voting logic, publication requirements, quorum rules, and veto thresholds are implemented in smart contract code that is modifiable by humans, advanced AI systems, or state-level adversaries. The sole path to genuine enforcement of the Immutable Mandates is DITL hardware, where Epistemic Hold is not a policy commitment but a physical voltage state. The Custodians' constitutional value is real and load-bearing at the accountability layer. It does not extend to physical prevention of Mandate violation.

### Consolidated verdict

**Robust:** Staggered 4-year terms with 8-year cap and 4-year cool-down; tri-cameral requirement of simultaneous capture; asymmetric proposer-blocker architecture insofar as the janitor-architect boundary is maintained; publication-of-reasoning requirement; default-to-rejection on expired Time-Bound Epistemic Hold.

**Fragile:** 9-of-11 quorum threshold vulnerable to 3-member attrition; Nominating Committee external-expert selection structurally analogous to known capture channels; no-more-than-2-per-entity diversity rule does not bind ideology; Mandatory Veto Obligation enforceable only at social and legal layers; anti-capture review vulnerable to alert fatigue.

**Effectively unenforceable against APGT:** Any defense depending on human reviewers authenticating presented evidence; any defense depending on classical cryptography for persistent records under harvest-now-decrypt-later posture; any defense depending on Custodians' ability to investigate at depth under alert-fatigue pressure.

### Where DITL hardware reduces dependence on human Custodian action

DITL's physical-voltage Escrow state substantially reduces dependence on human Custodian action for **direct prevention of Mandate violation**. No Spy and No Weapon: hardware Escrow state requiring attestation before sensitive-data execution paths proceed removes the need for case-by-case adjudication of surveillance risk. No Switch Off: hardware-level guarantees remove the need for Custodians to verify compliance rather than enforce it.

### Constitutional integrity assessment

**The Custodians' defined scope keeps them within the janitor role textually.** [VERIFIED] The prohibition on initiating technical proposals, proposing Treasury disbursement rules, and modifying Immutable Mandates is explicit. **Functionally, under multi-decade sustained pressure, the risk is real that the binding veto becomes architectural.** Every analogous veto-only body in the comparative record has developed de facto proposal power through procedural innovation over long horizons. Any such crossing must be flagged as [CONSTITUTIONAL VIOLATION] and remediated by re-scoping, not accommodation.

The remembered constitutional hard boundary: **governance is the janitor of eternity, not the architect of tomorrow.** Without DITL hardware below, the pressure to expand Custodian authority to compensate would be immense and eventually irresistible. With DITL hardware below, the Custodians can remain janitors because they do not have to be enforcers.

---

---

# Section 3: Smart_Contract_Treasury.md
## Ternary Logic Constitutional Governance Research - Section 3
**Research Date:** Q2 2026
**Status:** Standalone Report - Section 3 of 4

---

## Executive summary and the core honest tension

The Smart Contract Treasury is the only body in the TL constitutional architecture with zero vote rights and zero discretionary authority. **Any software can be modified - by humans with root access, by advanced machine learning agents with supply-chain reach, or by state-level adversaries with firmware-level access. This is not theoretical. It is an architectural fact.** [VERIFIED]

Constitutional guarantees written in smart contract code are only as strong as the hardware beneath them. The sole path to genuine enforcement of the Immutable Mandates is DITL hardware, where Epistemic Hold is not a policy commitment but a physical voltage state at half-Vdd. Software governance provides accountability, auditability, and coordination. Hardware governance provides enforcement. Both are necessary. Neither alone is sufficient. [NOVEL]

**The verdict up front: the Treasury's vote-right absence is constitutionally robust in design and empirically unprecedented in production.** No comparable autonomous fiduciary with no admin key, no pause guardian, no emergency shutdown, and no discretionary milestone verifier has been deployed and survived adversarial testing as of Q2 2026. [HIGH]

---

## 3.1 Smart contract treasury vote rights architecture

The Treasury's complete absence of vote rights is the architecturally distinctive claim. Nothing comparable exists in production as of Q2 2026.

### The autonomy gap in comparable systems

**MakerDAO's Emergency Shutdown Module (ESM)** is the canonical counter-example of what TL explicitly forbids. Any address may burn MKR into the ESM contract; when burned MKR crosses the threshold (raised to 300,000 MKR by executive vote on July 25, 2024), any caller can invoke fire() to halt the entire protocol. [VERIFIED][43] Under TL's Article VIII (No Switch Off), an equivalent would be a [CONSTITUTIONAL VIOLATION] of the absolute mandate.

**Compound Finance** retains a Pause Guardian multisig that can halt supply, transfer, withdraw, absorb, and buyCollateral per-market. [VERIFIED][44]

**Aave v3** maintains two separate 5-of-9 emergency multisigs: a Protocol Emergency Guardian and a Governance Emergency Guardian authorized to veto malicious on-chain governance payloads. [VERIFIED][45]

**Three-party autonomous fiduciary as specified by TL (Technical Council proposes, Custodians approve, Treasury autonomously executes) has no production precedent.** [HIGH] The closest production topology is the oSnap pattern (Snapshot off-chain vote plus UMA Optimistic Oracle verification plus a Gnosis Safe module that auto-executes payload data after liveness expires), securing approximately $689M by end of 2024. [VERIFIED][46] But oSnap's "third party" is still human voters, not a second independent body with constitutional duties.

### The milestone verification problem

Four categories of verification exist, each relocating trust rather than eliminating it:

1. **EXTCODEHASH-based code deployment verification:** trustless for bytecode hash at address; not trustless for intent. [VERIFIED]
2. **Ethereum Attestation Service (EAS):** schema-based attestations; trust concentrated in the attester's signing key. [VERIFIED][47]
3. **UMA Optimistic Oracle v3:** bond plus 2-hour liveness plus dispute escalation. Economically secured dispute-game, not trustless. [VERIFIED][48]
4. **zkVMs (SP1, RISC Zero):** prove that computation C on input I produced output O - only applicable to milestones expressible as deterministic computation. [VERIFIED][49]

**No production protocol performs fully autonomous, off-chain-milestone-based, non-oracle-dependent treasury disbursement at scale.** [HIGH] Every system reduces to trust in oracle, attester, or dispute-game.

### Joint-Approval cycle time and governance paralysis risk

The 75%+75% threshold across two bodies is stringent. By analogy with production cycle times: Compound ~7 days, Aave Short-executor ~5 days, Uniswap ~16 days, L2BEAT Stage 2 exit window >=30 days. [VERIFIED] TL Joint-Approval plausibly takes 2-4 weeks. This is appropriate for constitutional rule changes but creates economic denial-of-service exposure for operational tempo. The constitutional answer is that this is a feature, not a bug - Treasury's encoded rules must be stable enough that annual cycles suffice. [NOVEL]

### The economic denial-of-service vector

The Compound "Humpy" / Golden Boys attack (Proposal 289, July 2024): a whale coalition acquired COMP on the open market and passed a proposal transferring approximately 499,000 COMP ($24M) to a yield vault they controlled. [VERIFIED][8] The proposal was withdrawn only after social pressure. TL's two-body structure with no token-weighted voting is not directly vulnerable to this vector, but capture of membership selection in either body is the equivalent vector.

**Tribe DAO dissolution provides the clearest fee-accumulation precedent.** After the April 30, 2022 Fei-Fuse reentrancy exploit drained approximately $80M, Tribe DAO wound down on August 19, 2022; autonomous contracts continued operating while the treasury was effectively empty. [VERIFIED][50]

### Adversarial failure analysis

| Precedent | Mechanism | Layer | TL Treasury outcome | Additional constraint (no god-mode) |
|---|---|---|---|---|
| Beanstalk flash-loan governance (April 2022, ~$77M) | Flash-loan voting power, emergencyCommit() in one block | Software | Prevented: no token-weighted voting; no emergencyCommit() | Require attestation that no voting weight acquired within N blocks |
| Compound Proposal 62 bug (Sept 2021, ~$62M unrecovered) | Distribution bug; timelock prevented fast fix | Software | Equally vulnerable: rule-bug executes identically | Rules must include per-epoch max disbursement circuit-breakers |
| Tornado Cash governance takeover (May 2023) | Malicious proposal with hidden selfdestruct; minted 1.2M votes | Software/social | Partially mitigated by two-body structure; equally vulnerable if Custodian review is not technical | Mandate formal verification of payload bytecode, not only English description |

---

## 3.2 On-chain governance current state (Q2 2026)

As of Q2 2026, the most sophisticated on-chain governance implementations converge on: off-chain discussion plus Snapshot temperature check plus on-chain vote plus timelock plus selective guardian veto. None has eliminated the guardian role without either restricting governance scope to narrow on-chain parameters or retaining an upgrade path controlled by a small multisig.

L2BEAT Stage 2 (June 2023 framework): permissionless fraud proofs, >=30-day exit window, Security Council restricted to adjudicable on-chain bugs only. [VERIFIED][51] As of January 2025, three Stage 2 rollups existed (DeGate, zk.money, Fuel). **Smart contract treasury immutability is functionally Stage 2.** [NOVEL]

No multi-chamber on-chain governance with 75%+75% co-equal supermajorities across two independent bodies has survived adversarial testing in production. [GAP-RESEARCH]

---

## 3.3 The Treasury as autonomous fiduciary

Current production milestone-gated disbursement infrastructure:
- **Optimistic oracle pattern (UMA OO, Reality.eth):** Assertion plus bond plus liveness plus dispute escalation. Secures ~$689M via oSnap deployments. [VERIFIED][46]
- **EAS attestation:** Trust concentrated in attester set. [VERIFIED][47]
- **SP1/RISC Zero zkVM proofs:** Production-ready on-chain verifiers; applicable only to deterministic computation milestones. [VERIFIED][49]

**Compound Proposal 62 is the empirical answer to whether autonomy is a security feature without circuit-breakers: No.** When the distribution bug was identified, the 7-day governance delay permitted continued permissionless drip() calls that moved an additional $68.8M into drainable state. Approximately $62M was never recovered. [VERIFIED]

**MakerDAO's Emergency Shutdown Module is explicitly what TL cannot have.** [CONSTITUTIONAL VIOLATION if adopted] The TL Treasury cannot be halted under any circumstance by any mechanism. This is absolute under Article VIII.

---

## 3.4 The Revocation Contract and automated slashing

**RockLogic GmbH / Lido slashing (April 13, 2023):** Eleven validators slashed from infrastructure misconfiguration (previously-deleted validator keys unexpectedly re-imported after a BN+VC client update, causing duplicate attestations). Total penalties approximately 11.19 ETH. Lido DAO and RockLogic reimbursed the impacted pool. [VERIFIED][52]

**Medalla testnet incident (August 14-19, 2020):** Cloudflare Roughtime servers returned incorrect time; Prysm did not properly fall back. Over 3,000 slashing events broadcast; validator participation dropped from ~80% to ~5%. [VERIFIED][53]

**SSV Network mass slashing (September 10, 2025):** 40 validators slashed from Ankr maintenance misconfiguration leaving validator keys active in two infrastructures simultaneously. [VERIFIED][54]

These are the empirical proof that **sensor/oracle/monitoring data feeding automated slashing contracts malfunctions at scale, in production, multiple times.** [VERIFIED] **If the on-chain monitoring service feeding the Revocation Contract is compromised or manipulated, it will trigger mass false-positive revocations that governance will take 5-14+ days to overturn.** [HIGH]

**Polkadot's built-in 27-day grace period** is the direct production precedent for rule-level mitigation: slashing conditions enter an "unapplied state transition" for 27 days during which governance can reverse, without requiring a god-mode override. [VERIFIED][55] TL should encode a minimum 7-day pre-enforcement delay on all revocations as a rule, not a pause.

---

## 3.5 DITL as the honest constitutional floor

**[GAP-ARCHITECTURAL]** As of Q2 2026, no production deployment of DITL or NULL Convention Logic governance/safety hardware has been located. DITL remains at design specification, transistor-level simulation, FPGA demonstration, and small research-ASIC stages. Theseus Logic Inc. (Karl Fant, 1996) is listed as defunct on Tracxn. No governance silicon based on NCL dual-rail {0,0} at half-Vdd, hysteretic C-element Epistemic Hold, or Goukassian-signature-embedded chip has been fabricated in production. [VERIFIED]

**The Escrow state cannot be overridden by software** because the {0,0} dual-rail state at half-Vdd configures specific CMOS transistors to block signal propagation. There is no software call that can override the physical voltage configuration of a transistor pair forced to {0,0}; bypass would require physical probe access to the die. [HIGH]

**Ghost Governance** is the direct analogue of Ghost Fills: governance actions that execute without corresponding immutable audit evidence. The Atomic Auditability definition is Executed(T) implies Auditable(T) with temporal overlap on the same physical commit boundary. DITL eliminates Ghost Governance by construction: the physical commit boundary is shared between execute and audit. [NOVEL]

**Honest residual vulnerabilities (Section VIII of Atomic Auditability paper, stated without minimization):**
1. C-element hysteresis drift: threshold voltage drift from aging, temperature, and ionizing radiation can shift switching thresholds over device lifetime. A sufficiently drifted C-element may transition to Executed before audit_valid stabilizes.
2. Dual-rail crosstalk: wire spacing and fast-swinging adjacent signals can induce false transitions on dual-rail lines. Physical vulnerability to hardware supply-chain adversaries who influence die layout.
3. Completion detection metastability: near-simultaneous input arrival at completion detectors can induce synchronizer failure with non-zero probability per transition.

**The two-layer architecture:** software governance above the DITL hardware floor. Software can be upgraded through Joint-Approval; hardware floor cannot be overridden by software-layer actions. Software provides accountability, auditability, and coordination. Hardware provides enforcement.

---

## 3.6 Transitional governance (Pre-DITL deployment)

In the absence of deployed DITL hardware, the No Log = No Action invariant is bypassable at the software layer by any adversary with root access. [HIGH] Every production DeFi recovery at scale has relied on administrator action, and every governance attack has exploited some variant of it.

**Every software timelock and multisig delay is explicitly a speed bump, not an Escrow state** - per the Atomic Auditability paper's critical distinction. A delay slows participants equally but does not change the fundamental race condition structure. A state barrier physically prevents execution until attestation. [VERIFIED]

Transitional provisions recommended:
1. **On-chain disclosure of reduced enforceability**, following the L2BEAT Stages Framework model.
2. **Minimum 7-day timelock on all rule-encoding transactions** (Stage 1 aligned) with 30-day timelock for Mandate-adjacent rules (Stage 2 aligned).
3. **Rule-level circuit-breakers** (per-epoch maximum disbursement; multi-oracle concurrence; Polkadot-pattern grace period on revocations).
4. **External attestation via EAS or optimistic oracle** for Joint-Approval payloads.

An adversary with established software-layer access loses that access after DITL hardware deployment - creating specific incentive to prevent DITL upgrade. Constitutional text should commit to DITL migration as a non-discretionary constitutional objective and require Joint-Approval on delays beyond a published schedule. [NOVEL]

---

## 3.7 Zombie governance - Treasury operation during Layer 1 compromise

**Under Article VIII No Switch Off, the Treasury cannot be halted.** A "pause during compromise" mechanism would be a god-mode override. This is a [CONSTITUTIONAL TENSION] but the intended behavior of the constitution. The constitution accepts continued Treasury operation during compromise as the cost of absolute uncompromised autonomy. [HIGH]

Production 51% attack data: Ethereum Classic August 2020 - three attacks within one month, approximately $7M combined; Bitcoin Gold May 2018 - approximately $18M; Verge February 2021 - 560,000+ block reorganization (approximately 200 days of history erased). [VERIFIED][56]

**MakerDAO's Oracle Security Module (OSM) pattern** is the strongest production precedent for time-delay mitigation without god-mode: each collateral type has a 1-hour hop delay on new price values; poke() is permissionless; no single admin override exists. [VERIFIED][57] Applied to TL: every Treasury disbursement could be queued for a publicly-observable window during which permissionless actors could submit dispute attestations proving L1 compromise.

**Maximum financial exposure during a 30-day compromise window** is bounded only by per-epoch disbursement rules encoded at Joint-Approval time - a strong argument for mandatory per-epoch caps. [NOVEL]

---

## 3.8 Smart contract treasury verdict

### Core honest tension restated

Any software can be modified. The Treasury's constitutional guarantees written in smart contract code are only as strong as the hardware beneath them. The sole path to genuine enforcement of the Immutable Mandates is DITL hardware. Software governance provides accountability, auditability, and coordination. Hardware governance provides enforcement. Both are necessary. Neither alone is sufficient.

### Consolidated verdict

**Robust:** The Treasury's absolute absence of vote rights is constitutionally coherent and architecturally distinctive. The two-body Joint-Approval structure with no token-weighted voting forecloses the Beanstalk flash-loan attack vector and the Compound Humpy market-accumulation vector. The Goukassian Principle's formalization in LTL plus SystemVerilog provides a mathematically precise specification of the Escrow state.

**Fragile:** Milestone verification reduces to trust in an oracle, attester, or dispute-game. Joint-Approval cycle time creates economic denial-of-service exposure via Tribe DAO-style dynamics. The Revocation Contract inherits every known automated-slashing false-positive pattern.

**Gaps:** [GAP-ARCHITECTURAL] DITL has no production deployment. [GAP-RESEARCH] No multi-chamber on-chain governance with 75%+75% co-equal supermajorities across two independent bodies has survived adversarial production testing. [GAP-ARCHITECTURAL] Governance.md does not currently encode rule-level circuit-breakers at the granularity implied by production precedents.

### Enforceable guarantees given current DITL deployment status

**Given that DITL is not deployed:** The Treasury's guarantees are enforceable at the software layer against adversaries without root access; not enforceable against adversaries with supply-chain reach, compiler compromise, or node-operator compromise; auditable in the sense that any violation leaves detectable evidence, provided audit nodes are not compromised.

**Given that DITL is deployed:** Enforceable at the physical layer against any software-only adversary; still vulnerable to residual hardware vulnerabilities in Section VIII (C-element hysteresis drift, dual-rail crosstalk, completion detection metastability).

### Final constitutional integrity assessment

**The Smart Contract Treasury is constitutionally sound in design and empirically unprecedented in production.** Its enforceability is contingent on DITL hardware deployment. In the transitional period, it is a speed-bump regime that should honestly acknowledge its reduced enforceability on-chain. Its long-term integrity depends on rule-encoding quality by Joint-Approval.

The Treasury's guarantees are physics when hardware is real, and trust when it is not.

---

---

# Section 4: Governance_Synthesis.md
## Ternary Logic Constitutional Governance Research - Section 4
**Research Date:** Q2 2026
**Status:** Standalone Report - Section 4 of 4 (Integrated Synthesis)

---

The complete TL architecture guarantees, at the governance layer, procedural separation of powers and time-bounded uncertainty management. It does not guarantee, at the software layer, physical enforcement of the Three Mandates. Those require DITL silicon. The tri-cameral design stays within the janitor role as a matter of formal constitutional structure, but exhibits a [CONSTITUTIONAL TENSION] where three-body coordinated action can accrete architectural authority through operational rule-encoding without any single vote being visibly architectural. [NOVEL]

---

## 4.1 Two-layer architecture synthesis

TL governance is coherent only when read as two layers operating on different physical substrates. The upper layer is institutional and software-defined; the lower layer is physical and circuit-defined. Each layer has guarantees the other cannot provide. Each has failure modes the other cannot compensate for.

### Layer 1: the DITL hardware floor

The Delay-Insensitive Ternary Logic substrate provides four guarantees that no software governance layer can provide [VERIFIED against the Atomic Auditability paper; GAP-ARCHITECTURAL on production deployment]:

**The Epistemic Hold** is instantiated as the {0,0} dual-rail NULL or Spacer state at half-Vdd. It is a physical voltage condition, not a software flag. Root access, kernel compromise, firmware substitution, and hypervisor escape do not reach it, because it is enforced below the instruction-set architecture. The Epistemic Hold at this layer is never renamed and never bypassed; it is the state the wire is in.

**No Log = No Action** is enforced as a circuit-level interlock expressing the Goukassian Principle in LTL form: G(execute → P(escrow_recorded ∧ auditable)). The execute signal is physically gated on prior completion of the Escrow state and its audit-token emission. This is the atomic commit boundary: Executed(T) implies Auditable(T) with temporal overlap, not eventual consistency. **Ghost Governance** - governance actions that execute without corresponding immutable audit evidence - is eliminated by construction. [NOVEL]

**No Switch Off** is enforced by absence. There is no pause(), no suspend(), no freeze(), no admin_kill(), because the silicon routes no trace to such a function.

**Side-channel resistance** is a byproduct of delay-insensitive balanced dual-rail design.

Three residual hardware vulnerabilities remain: C-element hysteresis drift; dual-rail crosstalk; completion-detection metastability. These are bounded silicon-engineering problems with known mitigation patterns. They are not architectural defects. [VERIFIED per Atomic Auditability paper Section VIII]

### Layer 2: the constitutional governance layer

Above the physical floor sits the tri-cameral constitutional layer: Technical Council (exclusive proposal, 7-of-9 quorum, 3-year staggered terms); Stewardship Custodians (binding veto, 9-of-11 quorum, 4-year staggered terms); Smart Contract Treasury (autonomous execution, no vote rights). Upgrades to the four non-Protocol facets pass through UUPS under Joint-Approval Type 3 votes at >=75%. The Protocol Contract is an immutable Diamond Proxy with upgradeability permanently renounced. Anchors externalize notarization across a minimum of five chains. [VERIFIED against Governance.md Articles II, IV, V, VI]

The governance-layer Epistemic Hold is the time-bounded procedural mechanism: proposals default to rejection at window expiry. **This is the same principle as the hardware Epistemic Hold, expressed at a different layer.** The name does not change. The mechanism does. [VERIFIED]

### What each layer can do that the other cannot

**Layer 2 can adapt.** It can rotate members, certify new nodes, propose post-quantum migration schedules, rotate Anchor chains under threat, arbitrate edge cases, and evolve operational parameters. Layer 1 cannot adapt. A fabricated chip is a fabricated chip. [VERIFIED]

**Layer 1 can physically enforce.** It blocks execution paths that have not entered, recorded, and exited the Escrow state. It resists root access and firmware compromise. It eliminates Ghost Governance by making execution and audit evidence share one commit boundary. Layer 2 cannot physically enforce anything. A constitutional text is a coordination device that a captured, coerced, or quorum-starved institution can fail to apply. [HIGH]

### Failure modes when one layer is compromised

**Case A: Layer 1 intact, Layer 2 compromised.** Execution remains physically bounded by the Mandates. But no body can coordinate evolution. The system enters a constitutional zombie state: operationally alive, architecturally unable to evolve. The Treasury keeps executing autonomous rules against a milestone set that no body can amend. [HIGH]

**Case B: Layer 1 absent or compromised, Layer 2 intact.** The Mandates become procedural commitments only. This is the current pre-DITL state of the framework. [VERIFIED] An operator under state-level legal compulsion, a captured multisig, or a firmware-compromised node can violate the Mandates while the constitutional text remains satisfied on paper.

### Minimum viable architecture if DITL deployment is delayed

If DITL fabrication is delayed indefinitely, the honest transitional regime is a speed-bump architecture with explicit disclosure that it is not the floor. Five elements constitute the minimum viable interim design: (1) on-chain disclosure in the Preamble and Article I of reduced enforceability; (2) rule-level circuit-breakers and per-epoch caps in Treasury autonomous disbursement; (3) a PQC migration schedule with explicit milestones tied to the NIST FIPS 203, 204, 205 timeline; (4) Polkadot-pattern pre-enforcement grace periods on Revocation actions; (5) IBC Eureka or equivalently trust-minimized relay infrastructure for Anchor cross-chain. [VERIFIED and NOVEL in combination]

---

## 4.2 Constitutional integrity assessment

### Question 1: does coordinated three-body action create emergent architectural authority?

**Yes, conditionally.** The three bodies, acting through their constitutionally permitted channels, can cross the janitor/architect boundary that no single body can cross alone. This is a [CONSTITUTIONAL TENSION] present in the architecture as currently specified, and it becomes a [CONSTITUTIONAL VIOLATION] under a specific and identifiable pathway. [NOVEL]

The pathway is rule-encoding accretion. Three concrete hard cases illustrate it:

**Case (a) - the interpretive-lock pathway:** The Technical Council proposes and Custodians approve operational rules that functionally exclude categories of future proposals by binding later Councils to prior interpretive commitments. Each rule is individually operational. Cumulatively the proposal space is narrowed without amending Article I. [NOVEL]

**Case (b) - the budget-as-constitution pathway:** Treasury milestone rules structurally defund certain research directions without formally prohibiting them. Individually each rule allocates to a legitimate milestone. Cumulatively, the research surface that can be funded is bounded, equivalent to a research prohibition enforced through budget rather than text. This has direct analogues in legislative appropriations practice. [HIGH]

**Case (c) - the precedent-accretion pathway:** Custodian veto patterns establish de facto constitutional interpretations narrower than Article I's text. The publication requirement on veto creates a body of interpretive precedent that future Custodians treat as binding, even though it has no formal constitutional status. This reproduces the common-law drift that written constitutions routinely experience absent explicit originalist discipline. [HIGH]

### Question 2: does the architecture remain within the janitor role at the system level?

**Formally yes. Operationally, [CONSTITUTIONAL TENSION].** The three bodies can, working together within their permitted scopes, effectively modify the foundational architecture without formally proposing to do so. This is the default trajectory of any governance system with rule-encoding expressiveness, a proposer with exclusive agenda rights, and a vetoer with no counter-proposal right. [HIGH]

### Structural remedies that do not require God Mode

Five remedies, each compatible with Article I's immutability and none requiring an override primitive:

1. **A constitutional interpretation clause** stating operational rules are interpreted against Article I, never the reverse, and any rule found to narrow a Pillar's practical meaning is void. [HIGH]
2. **Mandatory Pillar Impact Statements** attached to every Type 3 proposal, enumerating which Pillars the proposal affects and certifying that cumulative active rules do not narrow any Pillar's scope. [NOVEL]
3. **Sunset clauses on operational rules**, auto-expiring after a bounded period and requiring explicit re-approval, breaking rule-accretion path dependence. [HIGH]
4. **A rotating Pillar Interpretation Panel** drawn from outside Technical Council and Custodians, with advisory jurisdiction only and a publication obligation on interpretive drift. [SPECULATIVE on effectiveness; HIGH on structural soundness]
5. **A Custodian counter-proposal right**, narrowly scoped to proposals that Custodians have formally vetoed, allowing Custodians to propose the minimally-modified alternative rather than only blocking. This is the direct structural response to the EU Commission precedent. [HIGH]

### Verdict on integrity at the system level

The tri-cameral architecture, as currently specified in Governance.md, is **structurally within the janitor role but operationally vulnerable to architectural drift through rule-accretion.** [NOVEL] It is not a present [CONSTITUTIONAL VIOLATION]. It is a future one absent the remedies above. The architecture does not need to be redesigned. It needs structural additions that make the janitor boundary explicit at the interpretive layer, auditable at the proposal layer, and expiring at the rule layer.

---

## 4.3 Synthesis verdict

### Deliverable 1: Preamble paragraph for Governance.md

The Ternary Logic framework guarantees, at the governance layer, a tri-cameral separation of powers in which no single body can propose, approve, and execute a change to the protocol. It guarantees time-bound uncertainty management through the Epistemic Hold, externalized notarization across a minimum of five Anchor chains, and a Diamond Standard contract architecture in which the core Protocol is immutable and only four bounded facets remain upgradeable under Joint-Approval supermajority. These guarantees are procedural. They bind institutions that can be captured, coerced, deceived, or left quorum-starved. Governance is the janitor of eternity, not the architect of tomorrow. Hardware resists last. Institutions fail first. To make the Three Mandates physical rather than rhetorical, the Epistemic Hold must be instantiated as a dual-rail NULL voltage state, execution must be interlocked with atomic audit evidence, and No Switch Off must be enforced by the absence of any kill circuit in silicon. Governance shapes the room. Governance never touches the foundation. The foundation is hardware, or the foundation is not physical at all.

### Deliverable 2: Single most important finding per section

**Section 1 (Technical Council):** The Type 1 emergency Anchor migration authority, exercisable unilaterally by a simple majority of the Technical Council with no Custodian involvement, is the single largest capture vector in the governance architecture. [VERIFIED]

**Section 2 (Stewardship Custodians):** The Custodian mandatory veto obligation is a social and legal commitment only, not an on-chain primitive, and it fails as a defense against state-level legal compulsion combined with synthetic evidence at Q2 2026 human detection rates near chance. [VERIFIED]

**Section 3 (Smart Contract Treasury):** No comparable autonomous on-chain treasury without an admin key, pause guardian, or emergency shutdown has survived adversarial production testing as of Q2 2026, making the TL Treasury constitutionally unprecedented and making rule-encoding expressiveness the single load-bearing design constraint of the entire Treasury architecture. [VERIFIED]

### Deliverable 3: Recommended priority order for updating Governance.md

| # | Update | Article affected | Priority | Fits within Article I? |
|---|--------|------------------|----------|------------------------|
| 1 | Require Custodian concurrence or mandatory 72-hour grace period on Type 1 emergency Anchor migration | Article IV, Article VI | [CRITICAL] | Yes |
| 2 | Add time-bound escalation pathway for cryptographically-urgent proposals under sustained Custodian veto | Article IV, new PQC section | [CRITICAL] | Yes |
| 3 | Add explicit PQC migration schedule keyed to NIST FIPS 203, 204, 205 timelines | Article V or new Article | [CRITICAL] | Yes |
| 4 | Add Pillar Interpretation clause and mandatory Pillar Impact Statements on all Type 3 proposals | Article I, Article IV | [CRITICAL] | Yes |
| 5 | Add sunset clauses on operational rules with auto-expiry and explicit re-approval | Article IV, Treasury facet specs | [HIGH] | Yes |
| 6 | Grant Custodians scoped counter-proposal right limited to formally vetoed proposals | Article III, Article IV | [HIGH] | Requires new constitutional text |
| 7 | Encode rule-level circuit-breakers and per-epoch disbursement caps in Treasury facet | Article III, Article V | [HIGH] | Yes |
| 8 | Adopt Polkadot-pattern pre-enforcement grace period on Revocation actions | Article III (Revocation facet) | [HIGH] | Yes |
| 9 | Specify quorum-collapse safeguard for 9-of-11 Custodian threshold | Article II, Article IV | [HIGH] | Requires new constitutional text |
| 10 | Require IBC Eureka or equivalently trust-minimized relay infrastructure for Anchor cross-chain | Article VI | [HIGH] | Yes |
| 11 | Bound Custodian white-paper publishing to prevent precedent-accretion drift | Article III | [MODERATE] | Yes |
| 12 | Complete Succession Charter with full procedural specification | Article II | [MODERATE] | Yes |
| 13 | Insert honest Preamble disclosure that current deployment is a software speed-bump regime | Preamble, Article I | [MODERATE] | Yes |
| 14 | Document Ghost Governance as constitutional goal achievable only at hardware layer | Preamble, Article I | [MODERATE] | Requires new constitutional text |
| 15 | Establish rotating Pillar Interpretation Panel with advisory jurisdiction only | New article | [MODERATE] | Requires new constitutional text |

---

## Conclusion

The constitutional architecture is sound in its formal structure and vulnerable in three specific places that the research has now named with precision. The unilateral Type 1 emergency Anchor migration is the largest discrete capture vector. The mandatory Custodian veto obligation is a social commitment unbacked by on-chain primitives at a threat level where synthetic evidence and state compulsion defeat social commitments. The rule-accretion pathway across the three bodies is a latent [CONSTITUTIONAL TENSION] that becomes a [CONSTITUTIONAL VIOLATION] absent explicit interpretive-layer remedies, none of which require a kill switch.

The single non-negotiable observation is that the Three Mandates are **procedural commitments at the current software layer** and become **physical enforcements only at the DITL layer**. No amount of constitutional drafting changes this. The Goukassian Principle in LTL form, G(execute → P(escrow_recorded ∧ auditable)), is satisfiable in silicon by construction and unsatisfiable in software by any method known in Q2 2026. [VERIFIED] Hardware resists last. Institutions fail first. The framework, as a whole, is honest about this only if the Preamble is honest about it. Governance shapes the room. Governance never touches the foundation.

---

## Footnotes (consolidated)

[1] Optimism Collective OPerating Manual; Lemma Solutions governance analysis.   
[2] IAEA governance structure, iaea.org/about/governance.   
[3] IETF RFC 8711 IASA 2.0.   
[4] WTO Appellate Body: CRS LSB10385; Columbia Journal of Transnational Law; CSIS analysis.   
[5] Castro and Liskov, "Practical Byzantine Fault Tolerance," 1999.
[6] European Parliament EPRS BRI(2025)767211; AFCO resolution April 2022.
[7] The Block, Build Finance DAO hostile governance takeover, February 14, 2022.
[8] Unchained Crypto; The Block; Blocmates - Compound Proposal 289, July 2024.
[9] Immunefi, "Hack Analysis: Beanstalk Governance Attack April 2022."
[10] OpenZeppelin Governor and TimelockController documentation; Compound Governance documentation.
[11] ERC-2535 Diamond Standard, Final status, GitHub ethereum/ercs PR #5802.
[12] Cyfrin CodeHawks Beanstalk "The Finale" audit, May 2024.
[13] ChainScore Labs EIP-2535 vulnerability analysis.
[14] Nick Mudge, Ethereum Magicians forum, ERC-8109 proposal.
[15] EIP-1822 UUPS, Stagnant status, eips.ethereum.org/EIPS/eip-1822.
[16] ERC-7201 Namespaced Storage Layout, Final status; OpenZeppelin Contracts v5.
[17] OpenZeppelin Security Advisory GHSA-5vp3-v4hc-gx76 / CVE-2021-41264; Iosiro disclosure.
[18] EIP-6780 SELFDESTRUCT changes, Cancun March 2024.
[19] Halborn, PAID Network hack analysis, March 2021.
[20] Audius governance takeover post-mortem, July 23, 2022.
[21] b10c Mining Centralization Index; BeInCrypto reporting on Foundry/AntPool.
[22] ethernodes.org; Messari validator decentralization reports; Dune staking dashboards.
[23] Ethereum mainnet finality post-mortem May 11-12, 2023, Offchain Labs.
[24] Cointelegraph; Crypto Economy - Ethereum Fusaka/Prysm v7.0.0 incident, late 2025.
[25] IBC Protocol blog, IBC v2 announcement; Succinct SP1 IBC Eureka launch April 10, 2025.
[26] NIST, "NIST Releases First 3 Finalized Post-Quantum Encryption Standards," August 13, 2024.
[27] NSA CNSA 2.0 Algorithms, May 30, 2025; NIST IR 8547 IPD.
[28] EIP-8051 ML-DSA precompile, EIP-7619 Falcon-512 - both Draft as of Q2 2026.
[29] Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits," May 2025.
[30] Parliament Act 1911; LawTeacher; UOLLB analysis.
[31] Canadian Senate, Senate of Canada / The Canadian Encyclopedia.
[32] Tsebelis, "Veto Players: How Political Institutions Work," Princeton University Press, 2002.
[33] Incode / Hong Kong Police announcement February 5, 2024 - deepfake CFO fraud $25.6M.
[34] NIST Dual_EC_DRBG; Wikipedia; Cryptography Engineering blog; IACR eprint 2015/767.
[35] Security Council Report, "In Hindsight: The Security Council in 2024"; "Living with the Veto," April 2026.
[36] ISO/IEC OOXML fast-track; Martin Bryan resignation 2008.
[37] XZ Utils / Jia Tan: research.swtch.com/xz-timeline; Securelist; SoftwareSeni; Linux Foundation April 2026 report.
[38] ICANN NomCom; AFRINIC Board elections intervention, June 2025.
[39] Barroso / Goldman Sachs, July 2016 European media reporting.
[40] CardinalOps 2024; JAMA 2024 drug-allergy alert study; Verizon PSR series.
[41] Diel et al., Computers in Human Behavior Reports, December 2024; arXiv:2501.15654.
[42] Global Risk Institute Quantum Threat Timeline Report 2025, seventh edition, April 2026.
[43] MakerDAO ESM documentation; sky-ecosystem/esm GitHub; July 25, 2024 executive vote.
[44] Compound Pause Guardian; docs.compound.finance/governance.
[45] Aave v3 Guardian; aave.com/docs/ecosystem/governance; aave.com/docs/developers/safety-module.
[46] UMA Optimistic Oracle v3; oSnap documentation; Gitcoin DAO integration reports.
[47] Ethereum Attestation Service; docs.attest.org; eas-contracts GitHub.
[48] UMA Optimistic Oracle v3 liveness and bond parameters; docs.uma.xyz.
[49] RISC Zero R0VM 2.0; Succinct SP1 ISP1Verifier; docs.succinct.xyz.
[50] Fei Protocol / Tribe DAO dissolution August 2022; Delphi Digital; Protos.
[51] L2BEAT Stages Framework June 2023; Vitalik Buterin January 23, 2025.
[52] RockLogic/Lido slashing incident April 13, 2023; blog.lido.fi post-mortem.
[53] Medalla testnet incident August 14-19, 2020; Prysmatic Labs post-mortem.
[54] SSV Network mass slashing September 10, 2025; ssv.network blog.
[55] Polkadot slashing tiers and 27-day grace period; docs.polkadot.com; web3.foundation research.
[56] Bitcoin Gold May 2018; Ethereum Classic August 2020; Verge February 2021 - multiple public post-mortems.
[57] MakerDAO Oracle Security Module; docs.makerdao.com; March 30, 2024 ETH price delay demonstration.
