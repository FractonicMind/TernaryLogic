## Ternary Logic Constitutional Governance Research - Section 1
**Framework:** Ternary Logic (TL) by Lev Goukassian   
**ORCID:** 0009-0006-5966-1243   
**Research Date:** Q2 2026   
**Status:** Standalone Report - Section 1 of 4   

---

## Core honest tension stated up front

Any software can be modified. Humans with commit rights can modify it. Automated agents with root access can modify it. State-level adversaries with supply-chain reach can modify it. This is not a theoretical risk; it is an architectural fact. Constitutional governance expressed in smart contract code is only as strong as the hardware beneath that code. The sole path to genuine enforcement of the Immutable Mandates is DITL hardware, where Epistemic Hold is not a policy commitment but a physical voltage state (NULL / half-Vdd) that cannot be overridden by software, root access, kernel compromise, or firmware manipulation. [NOVEL]

This does not invalidate the Technical Council as specified in Governance.md. It locates it honestly. Software governance provides accountability, auditability, and coordination. Hardware governance, via the Goukassian Principle expressed in Linear Temporal Logic and SystemVerilog assertions [1], provides enforcement. Both are necessary. Neither alone is sufficient. [HIGH]

---

## 1.1 Tri-cameral design and three-body equilibrium

**Finding: The tri-cameral architecture is defensible in principle but has no exact analogue in decentralized protocol governance as of Q2 2026.** [VERIFIED]

The closest production precedent is the Optimism Collective's **bicameral** design, which separates a Token House (protocol upgrades, treasury, project incentives) from a Citizens' House (soulbound membership, with a 30 percent veto threshold on protocol upgrades exercised during a one-week window after Token House passage) [2]. A Developer Advisory Board (DAB) adds a third advisory tier with a separate seven-day public veto window on protocol changes [2]. This is structurally similar to TL's Technical Council plus Stewardship Custodians plus Treasury, but Optimism's Citizens' House veto is executed off-chain via Snapshot and operational finalization still runs through the Optimism Foundation, so it is not purely trustless forwarding [2]. **Optimism is the strongest extant precedent for cross-chamber non-censorable forwarding, but it is weaker than what Governance.md specifies.** [HIGH]

Outside decentralized protocols, genuine multi-organ structures exist, but very few establish three coequal veto-bearing bodies. The **IAEA** has three organs (General Conference, Board of Governors, Secretariat), but they are hierarchical rather than coequal [3]. The **US Nuclear Regulatory Commission** is a unitary five-Commissioner body with staggered terms and partisan balance requirements, not tri-cameral [4]. The **IETF** separates IESG (standards approval), IAB (architectural oversight and appeals), NomCom (appointments), and IETF LLC (administration only, explicitly excluded from standards authority per RFC 8711) [5], which is the cleanest real-world precedent for separating operational, architectural, and administrative authority. The **Python PEP 13 Steering Council** is recallable by the Core Team via no-confidence vote [6]. The **WTO Dispute Settlement Body** uses a Panel plus Appellate Body structure, but the Appellate Body has been **non-functional since December 10, 2019** because a single member state refused to approve new appointments, allowing all terms to expire by November 30, 2020 [7]. This is a directly relevant cautionary precedent for any governance chamber whose membership depends on consensus replenishment.

**Nine members is at the lower bound of defensibility under standard BFT analysis.** [VERIFIED] Castro-Liskov PBFT requires `n ≥ 3f+1` for safety under Byzantine faults [8]. A nine-member Technical Council can tolerate `f = 2` Byzantine members safely. Three compromised members breaks safety. Fast two-step BFT protocols require `5f - 1` replicas, meaning nine is exactly at the boundary for `f = 2` with zero margin [9]. The specified 7-of-9 quorum formalizes this: it means any two members offline or captured cannot halt governance, but any three can. This is a reasonable design point, but it is not generous.

On deadlock versus capture: permanent orbital tension between Technical Council (proposal monopoly, no veto) and Stewardship Custodians (veto, no proposal) makes explicit collusion the only path to unilateral capture, because neither body can act alone on Type 3 decisions. That is the correct design inversion. The cost is latent deadlock risk, analyzed in 1.2. [HIGH]

---

## 1.2 Technical Council vote rights architecture

This is the spine of TL constitutional governance. The separation of exclusive proposal rights from final veto authority is the core capture-resistance mechanism, and it is also the core deadlock-generation mechanism.

### Exclusive proposal rights plus no veto

**Exclusive proposal rights without veto authority is a well-attested governance pattern that reliably produces agenda-setting dominance, not deadlock, under normal operation.** [HIGH] The clearest precedent is the **EU Commission's quasi-monopoly on legislative initiative under TFEU**, which has been criticized since the 1990 Parliament resolution as producing a "democratic deficit" precisely because Commission agenda-setting, combined with a reviewing body that can reject but cannot initiate, produces de facto Commission dominance regardless of formal veto distribution [10]. The April 2022 AFCO committee resolution (22-5-1) and the 2019 von der Leyen commitment to Parliament initiative rights both reflect sustained pressure against this architecture [10]. The US House Speaker's agenda control under the informal "Hastert rule" exhibits the same pattern.

For TL, this means: the structural risk is not that the Custodians will be unable to veto, but that the Custodians will receive only proposals pre-shaped by the Technical Council, with no ability to force consideration of alternatives. **The Custodian veto is a stop condition, not a steering mechanism.** [HIGH] If capture occurs, it will likely appear as narrowing of the proposal space rather than as override of veto.

### Sustained disagreement and deadlock

If Technical Council and Custodians enter sustained disagreement on a Type 3 matter, Governance.md as specified produces **status quo preservation, not deadlock**, because the Diamond Proxy remains operational and Immutable Mandates continue to hold regardless of upgrade cadence. The risk surfaces only when the status quo itself becomes untenable, for instance when a cryptographic primitive is broken (see 1.7) and upgrade is required for continued safety. **[CONSTITUTIONAL TENSION]** In that narrow window, indefinite Custodian veto of a Technical Council-proposed migration could leave the protocol running on broken cryptography. Governance.md contains no time-bound escalation mechanism for this case. [GAP-ARCHITECTURAL]

### Type 1 emergency continuity fallback

Governance.md grants the Technical Council unilateral authority (simple majority, no Custodian involvement) to migrate Anchor Host Chain state under emergency conditions. **This is the single largest concentration of unilateral authority in the Technical Council's mandate, and it is the point where capture risk is highest.** [HIGH]

The relevant failure precedents:
- **Build Finance DAO takeover (February 10, 2022)**: 5,000 yes votes out of 130,000 token supply (3.8 percent turnout) passed a treasury-draining proposal because monitoring infrastructure failed to raise an alarm [11]. Loss approximately $470,000. This is the canonical case of low-quorum emergency action being exploited.
- **Compound Proposal 289 (July 28, 2024)**: Attacker-aligned "Humpy" wallets passed a $24M treasury transfer 682,191 to 633,636 by timing the vote for a weekend when "participation is low enough for the proposal to pass" [12].
- **Beanstalk governance attack (April 17, 2022)**: $182M drained via a flash-loan-purchased supermajority executing `emergencyCommit` in the same transaction [13]. The emergency execution path was the exploit.

Each of these used an emergency-or-unilateral pathway to bypass deliberation. A Technical Council emergency Anchor migration authority, triggered by 5 of 9 members on simple majority, reproduces the core vulnerability pattern. **Recommended constraint without adding God Mode: require that any Type 1 emergency Anchor migration be accompanied by a mandatory, non-censorable Custodian notification with a minimum 72-hour observation window before execution finality, during which Custodians may escalate to a Type 2 reversal vote.** [NOVEL] This preserves Technical Council operational autonomy while closing the unilateral-emergency-action attack surface. Crucially, this does not grant the Custodians architectural authority; they only gain an observation-and-escalation trigger.

### 7-of-9 quorum under adversarial attrition

Under standard availability assumptions, 7-of-9 is robust. Under adversarial attrition, it is fragile. [HIGH] Three coordinated absences (sickness, coercion, compromise, travel embargo, legal injunction) halt the Technical Council. The WTO Appellate Body precedent shows that a single state-level adversary can paralyze a body requiring consensus replenishment for years [7]. For a nine-member council, the adversarial f-threshold for liveness is `f = 3`, which is one member below the safety bound. **Recommended: Governance.md should specify a documented succession protocol with a pre-authorized alternate bench such that vacancies can be filled within a defined window (e.g., 30 days) by Custodian confirmation under existing Type 2 rules.** [GAP-ARCHITECTURAL]

### Non-censorable forwarding enforceability

The Governance.md claim that Type 3 proposals passing the Technical Council are "automatically and non-censorably forwarded" to the Custodians is technically enforceable on-chain within a single chain via the Compound Governor Bravo plus OpenZeppelin TimelockController pattern: once `queue()` is called, any address can call `execute()` after the timelock expires, with no proposer discretion [14]. The OpenZeppelin Governor family of contracts implements this today. A compromised Technical Council cannot suppress forwarding of an already-queued proposal without compromising the Diamond Proxy's Governance facet itself, which requires a Joint-Approval vote (circular dependency that blocks the attack). [VERIFIED]

The weak point is not forwarding; it is **proposal construction before forwarding**. A compromised Technical Council can simply decline to propose, and the Custodians cannot force a proposal onto the agenda. This is the EU Commission problem reproduced on-chain. [HIGH] The mitigation without adding God Mode is for the Custodians to retain their revocation proposal right, which Governance.md preserves, effectively allowing the Custodians to remove captured members and force replacement. This is sufficient but slow.

---

## 1.3 Diamond Standard (EIP-2535) current status as of Q2 2026

**ERC-2535 is FINAL as of 2023 (PR #5802 merged), confirmed on the canonical ERCs repository with `status: Final`.** [VERIFIED] [15] The EIP was moved from the EIPs repo to the ERCs repo; the old EIPs copy shows `status: Moved`.

### Known vulnerability classes in diamond implementations

The reference `Diamond.sol` fallback does not implement a reentrancy guard; Cyfrin CodeHawks audit of Beanstalk "The Finale" (May 2024) flagged this as systemic, requiring each facet to implement its own guards [16]. Storage collisions between facets from incorrect manual slot management are documented [17]. The EIP itself warns that `diamondCut` "allows arbitrary execution with access to the diamond's storage (through `delegatecall`)" and must be access-restricted carefully [15]. Function selector clash prevention is spec-mandated but implementation-dependent.

**No confirmed mainnet post-mortem of a major exploit attributable specifically to an EIP-2535 diamond-pattern bug was located for 2023 through Q2 2026.** [GAP-RESEARCH] Beanstalk's 2022 $182M loss used EIP-2535 but the exploit was a flash-loan governance attack, not a diamond pattern flaw. Absence of finding is not proof of absence.

### Is EIP-2535 still best practice for upgradeable governance?

**Industry consensus in 2025 through Q2 2026 has shifted away from diamonds for governance-tier contracts unless the 24KB size limit forces the pattern.** [HIGH] Zealynx (January 2026) classifies diamonds as "moderate risk, high audit complexity" with typical audit cost of $100K to $200K versus $65K to $130K for UUPS DeFi protocols [18]. OpenZeppelin Contracts v5 (2024) adopted ERC-7201 namespaced storage but never shipped an official Diamond implementation (long-standing request GitHub issue #2793 remains unimplemented) [19]. Nick Mudge himself is now proposing **ERC-8109** as a simplified successor standard while stating he is not changing ERC-2535 [20]. This is a strong signal that the original standard's complexity is viewed as excessive for most applications.

**Assessment for TL:** The Diamond Proxy with upgradeability permanently renounced, plus four upgradeable facets on UUPS, is architecturally sound for "maintain but not mutate" because the immutable outer proxy contains no `diamondCut` function on itself (only on the facets, which are governed). **The pattern works as specified in Governance.md Article V.** [HIGH] However, given maintainer signal toward ERC-8109 and industry drift toward simpler patterns plus namespaced storage, Governance.md should add language permitting non-architectural migration to a successor diamond standard if that standard becomes Final and is endorsed by the original maintainer, subject to full Type 3 Joint-Approval. [GAP-RESEARCH]

---

## 1.4 UUPS (EIP-1822) and upgradeability as of Q2 2026

**ERC-1822 is formally STAGNANT, confirmed on eips.ethereum.org with the Stagnant banner and on the ERCs repository.** [VERIFIED] [21] Despite formal status, UUPS is the de facto dominant upgradeable-proxy pattern in 2025-2026 via OpenZeppelin's `UUPSUpgradeable` combined with EIP-1967 storage slots (not the original ERC-1822 `keccak256("PROXIABLE")` slot) [22].

**ERC-7201 namespaced storage is FINAL** and is the current recommended storage pattern for upgradeable contracts, adopted throughout OpenZeppelin Contracts v5 [23].

### Known UUPS vulnerabilities

The September 2021 OpenZeppelin advisory GHSA-5vp3-v4hc-gx76 (CVE-2021-41264) disclosed an uninitialized-implementation attack allowing an attacker to become owner, call `upgradeToAndCall`, delegatecall to attacker code, and `selfdestruct` the implementation, bricking all proxies [24]. Iosiro disclosed one related instance with $44M at risk (HidingVaultNFTProxy, not exploited) [25]. Fix: `_disableInitializers()` in implementation constructor, now standard.

**Post-Cancun EIP-6780 (March 2024) largely neutralizes the "destroy implementation, brick proxy" variant for contracts not created in the same transaction as the destroy call** [26]. It does not eliminate the broader uninitialized-implementation takeover. [VERIFIED]

Known exploits using upgrade mechanisms as attack vectors:
- **PAID Network (March 2021)**: proxy admin key compromise, attacker called upgrade, minted tokens; approximately $180M notional, $3M realized [27].
- **Audius governance takeover (July 23, 2022)**: storage layout collision between `proxyAdmin` variable and `Initializable.initializing` flag allowed re-calling `initialize` on governance, staking, and delegation contracts; approximately 18M AUDIO (about $6M at time) stolen, sold for about $1M [28].
- **AllianceBlock (2024)**: re-initialization bug in upgradeable contract [18].
- **Yearn yETH (December 2025)**: "ghost state" upgrade bug, V1 `packed_vbs` not cleared during V2 upgrade [18]. Primary post-mortem not verified in this research. [GAP-RESEARCH]

### upgradeTo ownership by Governance Contract

**Multi-party authorization (timelock plus multisig plus role-gate) controlling `_authorizeUpgrade` is technically enforceable in Solidity.** [VERIFIED] OpenZeppelin TimelockController plus a Safe multisig is the canonical stack. Known limitations:

1. Storage collision during upgrade can create unrecoverable deadlock (OpenZeppelin issue #6362, upgrading v4 sequential storage to v5 namespaced storage) [29].
2. `upgradeToAndCall` performs a `delegatecall` to the new implementation's initializer before any further authorization check, so a malicious new implementation executes with full proxy storage access if authorization was granted on a compromised basis.
3. Signer compromise of the multisig is always a vector independent of the proxy pattern. The Ronin Bridge March 2022 hack ($624M, 5-of-9 validator keys, attributed to state-level spear-phishing) [30] is the cardinal precedent.

**Assessment for TL:** Joint-Approval before `upgradeTo` execution is enforceable. The residual risk is **authorized but malicious implementation content**, which cannot be detected by any on-chain check and requires off-chain audit before Custodian approval. Governance.md should explicitly require that Type 3 proposals include audit artifacts as a prerequisite for the Custodian review window. [GAP-ARCHITECTURAL]

---

## 1.5 The software honesty problem

This section applies the Core Honest Tension directly to the Technical Council's mandate.

### Blockchain-layer compromise scenarios

A constitutionally immutable Diamond Proxy provides zero protection against a 51 percent attack on the underlying chain that reorganizes the state containing governance votes. MEV extraction can influence vote ordering. Consensus manipulation can censor Custodian veto transactions during the Type 3 review window. **These are layer-below-governance failure modes that the Technical Council cannot address by any amount of smart contract engineering.** [VERIFIED] The only mitigation available at the software layer is multi-chain anchoring, which is why Article VI exists.

Empirical weight of this risk: Foundry USA plus AntPool together control approximately 55 to 60 percent of Bitcoin hashrate as of Q2 2026 [31]. Lido plus Coinbase collectively control more than 33 percent of staked ETH [32]. MEV-Boost censorship of OFAC-sanctioned transactions peaked at 79 percent of Ethereum blocks in November 2022 and remained elevated through 2024-2026 before non-censoring relays regained share [33]. The May 11-12, 2023 Ethereum finality delays (25 minutes and 64 minutes) from a Prysm/Teku attestation bug [34], and the late-2025 post-Fusaka Prysm v7.0.0 bug that dropped voting participation by 25 percent and brought the network within 9 percent of losing finality supermajority [35], both demonstrate that client monoculture remains a live failure mode.

### "Absence of function" as No Switch Off enforcement

Article VIII states that No Switch Off is enforced by the absence of `pause()`, `suspend()`, `freeze()`, and `admin_kill()` in the Protocol Contract. **This is genuinely sufficient against application-layer pause authority, but it does not prevent equivalent effect through other means.** [HIGH]

- **`selfdestruct` in the Protocol Contract itself**: post-EIP-6780 (Cancun, March 2024), `selfdestruct` no longer destroys contracts not created in the same transaction [26]. This substantially mitigates but does not fully eliminate the vector. An implementation-facet `selfdestruct` would still be possible if the facet is created and destroyed in the same transaction during an upgrade, though the immutable outer Diamond Proxy is protected.
- **Proxy pointer manipulation**: the EIP-1967 implementation slot is only writable by functions that have permission to write it. If the Governance facet is compromised, the attacker can write a new implementation pointer. This is not a No Switch Off vector per se; it is an upgrade hijack.
- **Chain-level censorship**: if the validator set of the host chain excludes all transactions to the Protocol Contract, the protocol is effectively paused without any contract modification. This is the fundamental limit of software-layer No Switch Off enforcement. [VERIFIED]

### The commit-audit gap applied to governance state

The Atomic Auditability paper identifies the vulnerability window between commit and audit as the surface where execution can occur without prior recorded audit evidence [1]. **This window applies to governance contract state as well as to financial execution pipelines.** [NOVEL] A Type 3 vote that is committed (passed on Technical Council), queued, and executed is a sequence of state transitions, each of which could be reordered, censored, or subjected to MEV extraction during the transition window. The DITL four-phase handshake would apply natively: no `execute()` may propagate unless the system has entered, recorded, and exited a physically enforced Escrow state attesting that the Custodian review window completed without veto.

Expressed in LTL terms, the Goukassian Principle generalized to governance: `G(execute_upgrade → P(escrow_recorded ∧ custodian_window_closed ∧ no_veto))`. Implementation at the hardware level would require that the Governance facet's `execute()` opcode trigger a DITL Escrow state on dedicated hardware attesting that the Custodian review window expired without veto, with the NULL voltage state physically blocking execution propagation until attestation is produced. This is consistent with the paper's SystemVerilog assertion pattern, applied to a different pipeline. [SPECULATIVE]

### Where software governance becomes effectively unenforceable

**Software governance becomes effectively unenforceable at the moment a sufficiently-resourced adversary (state-level, advanced automated agent supply chain, or coordinated multi-validator cartel) can either (a) modify the binaries running on validators, (b) censor finality-relevant transactions at a majority of validators, or (c) compromise the key material of a quorum of governance participants faster than revocation can occur.** [HIGH]

**DITL hardware enforcement changes exactly one thing: it makes the physical Escrow state non-software-overridable, so the gap between commit and audit closes at the hardware boundary.** It does not prevent binary compromise upstream, does not prevent chain-level censorship, does not prevent key-material compromise. **It does prevent any compromised software stack, including a fully captured Technical Council and fully captured Custodian set, from causing execution without recorded audit evidence.** That is the specific property DITL provides and no software design can replicate.

---

## 1.6 Host Chain selection (Article VI) as of Q2 2026

Article VI requires minimum 5 Anchor Host Chains satisfying verifiable decentralization, cryptographic security, long-term liveness, and jurisdictional diversity, with an "any one Anchor survives" liveness guarantee.

### Recommended 5-chain anchor set

**Based on Q2 2026 data, the defensible minimum anchor set is Bitcoin, Ethereum, Cardano, Polkadot, Tezos.** [HIGH]

| Chain | Nakamoto coefficient | Halts 2023-2026 | Key risk |
|---|---|---|---|
| Bitcoin | 4 (pool layer) | None | Foundry USA + AntPool ~57% hashrate [31] |
| Ethereum | 2 (entity level) | Finality delays May 2023, late 2025 [34][35] | Lido + Coinbase >33% stake; AWS hosts >50% of nodes [32] |
| Cardano | 22 | None in 8+ years (2,923 days as of Sept 2025) [36] | Single dominant client (Amaru Rust client maturing) |
| Polkadot | 178 (highest of tracked L1s) [37] | None | Reference client monoculture; smaller economic value |
| Tezos | 14 | None; 15+ successful on-chain upgrades | Smaller TVL |

This set delivers four distinct consensus families, four or more distinct client codebases, Swiss-plus-global foundation dispersion, cloud-independence via Cardano's 17.5 percent self-hosted validators across 183 ISPs and Bitcoin PoW mining [38], and zero cross-chain cascade risk via restaking (only Ethereum is exposed to EigenLayer with approximately $17.6B to $19.7B TVL).

### Chains that appeared strong but showed vulnerability

- **Solana**: multiple multi-hour halts (Feb 2023 approximately 19h, Feb 2024 approximately 5h) [39]. Fails long-term liveness criterion. Firedancer multi-client maturing in 2026 but not yet default.
- **Aptos**: October 2023 5h+ halt [40]. The task prompt referenced an October 2024 halt; this **appears to be a factual error in the source question**, and no verifiable Aptos consensus halt in October 2024 was located. [GAP-RESEARCH]
- **Polygon PoS**: Nakamoto coefficient 4, historical deep reorgs pre-Heimdall v2 (July 10, 2025) [41], Lido ceased support December 2024. Not recommended as anchor.
- **Avalanche**: validator set declined 55.2 percent year-over-year to 656 in Q4 2025 [42]. Trajectory unfavorable.
- **All Ethereum L2s** (Arbitrum, Optimism, Base, zkSync Era, Starknet): all retain centralized sequencers with multi-hour outages; disqualified as independent anchors. **Base specifically failed the October 20, 2025 AWS us-east-1 test**, suffering approximately 25 percent throughput loss during the outage while Arbitrum and Optimism (multi-cloud) maintained 100 percent uptime [43].

### "Any one Anchor survives" achievability

**The liveness guarantee is achievable for the recommended five-chain set under Q2 2026 infrastructure conditions, conditional on maintaining distance from shared cloud providers and from cross-chain restaking exposure.** [HIGH] The October 2025 AWS us-east-1 outage is the canonical live-fire test: Base and some Ethereum operator cohorts degraded, Bitcoin, Cardano, Cosmos Hub, Polkadot, and Tezos showed no observable impact [43]. The guarantee is robust for this anchor composition but would be fragile if anchors were chosen with shared AWS dependencies or shared CometBFT or Substrate codebases.

---

## 1.6.1 Cross-chain vote security and relay integrity

**The "any one honest prover plus safe source chain equals integrity" property is genuinely achievable in production as of Q2 2026 for Ethereum-Cosmos, and only for that pair through IBC Eureka powered by Succinct SP1 (launched April 10, 2025).** [VERIFIED] [44] Cosmos IBC between Cosmos chains satisfies it trivially via permissionless relayers and on-chain light clients. Canonical Ethereum L1-L2 bridges satisfy it within the Ethereum-centric stack. Every other major cross-chain option (CCIP, default LayerZero, Wormhole, Axelar, Hyperlane default) relies on a permissioned validator quorum that could in principle censor or forge [44].

### Historical failure modes applied to Anchor notarization

| Failure | Date | Loss | Mechanism | Layer |
|---|---|---|---|---|
| Poly Network | Aug 10, 2021 | $611M (largely returned) | Access rights mismanagement | Smart contract |
| Wormhole | Feb 2, 2022 | $320M+ | Signature verification bypass on Solana | Smart contract / cryptographic |
| Ronin | Mar 23, 2022 | $624M | 5-of-9 validator key compromise | Operator/social |
| Harmony Horizon | Jun 23, 2022 | $100M | 2-of-5 multisig compromise | Operator/social |
| Nomad | Aug 1, 2022 | $190M | Zero-hash replay after upgrade | Smart contract (init) |
| Multichain | Jul 6-14, 2023 | $125M-$210M | CEO detained May 2023, MPC keys inaccessible | Operator/social |
| Orbit Chain | Dec 31, 2023 | $81.5M | 7-of-10 multisig key compromise | Operator/social |
| Ronin v2 | Aug 6, 2024 | $12M (returned) | Uninitialized `minimumVoteWeight` after upgrade | Smart contract |

**Private key compromise accounted for 88 percent of stolen funds in Q1 2025 per Chainlink/The Block aggregation** [44]. Operator compromise is the dominant failure mode by both frequency and dollar loss. This directly bears on any Anchor notarization model that depends on a federated relay: a Ronin-pattern compromise of relay operators would allow forging of Anchor state.

**[CONSTITUTIONAL TENSION]: If Type 3 proposals must be notarized on-chain across the Anchor network before Custodian review, and a federated relay infrastructure is compromised, Governance.md as specified contains no protocol-level deadlock resolution mechanism.** The Multichain precedent (resolved only via Singapore High Court default judgment of $2.18M to Fantom, January 2024) demonstrates that legal resolution is the realistic fallback when protocol-level recovery does not exist [44]. Ronin March 2022 was resolved by Sky Mavis plus Binance raising replacement funds and Wormhole February 2022 by Jump Crypto treasury replacement. None of these are protocol-level mechanisms.

**Mitigation without adding God Mode**: specify in Governance.md that the Anchor relay model must use IBC-class trust-minimized infrastructure (permissionless relayers plus on-chain light clients, or ZK-light-client bridges with permissionless provers such as Succinct SP1 for Ethereum-Cosmos pairs), explicitly excluding federated multisig relay sets. This preserves the Technical Council's exclusive proposal right on Anchor rotation (Type 2) and does not grant architectural authority. [NOVEL]

---

## 1.7 Post-quantum readiness

**Governance.md as written is silent on post-quantum cryptography, and the cryptographic primitives implied by typical blockchain governance (ECDSA secp256k1, BLS12-381, KZG commitments) are all Shor-vulnerable.** [VERIFIED]

### NIST PQC standards status

**Finalized August 13, 2024** [45]:
- FIPS 203 ML-KEM (formerly Kyber), parameter sets ML-KEM-512/768/1024
- FIPS 204 ML-DSA (formerly Dilithium), parameter sets ML-DSA-44/65/87
- FIPS 205 SLH-DSA (formerly SPHINCS+), 12 parameter sets

**Not yet finalized as of Q2 2026**:
- FIPS 206 FN-DSA (Falcon): draft submitted August 28, 2025; final expected late 2026 or early 2027 [46]
- HQC: selected March 11, 2025; draft expected 2026, final 2027 [47]

**Deprecation timeline** (NIST IR 8547 IPD, NSA CNSA 2.0): RSA/ECDSA/ECDH **deprecated after 2030, disallowed after 2035** [48][49]. UK NCSC (March 2025) endorses this timeline and sets 2028 for migration planning complete, 2031 for high-priority upgrades, 2035 for full migration [50].

### Relevance to governance contract cryptography

For TL governance, ML-DSA (FIPS 204) is the primary signature standard, SLH-DSA (FIPS 205) a conservative hash-based backup. ML-KEM is less immediately relevant to governance (signatures, not key encapsulation, dominate). **No PQC signature verification precompile is live on Ethereum mainnet as of Q2 2026.** [VERIFIED] EIP-8051 (ML-DSA precompile) and EIP-8052 (Falcon precompile) are both **Draft** [51]. EIP-7619 (Falcon-512) is Draft. EIP-7702 (EOA-to-smart-account delegation) went live at Pectra in May 2025 and provides the substrate for opt-in PQC signatures via account abstraction [52].

Vitalik Buterin's February 26, 2026 "Quantum Roadmap" post identified four vulnerable areas: consensus-layer BLS, KZG-based data availability, ECDSA EOAs, and application-layer ZK proofs, proposing hash-based signatures (leanXMSS, Winternitz variants) plus STARK aggregation as the replacement stack [53]. The Ethereum Foundation's January 2026 PQC strategic priority declaration and the `pq.ethereum.org` roadmap target L1 protocol upgrades by approximately 2029 [54].

### Migration path within Article I immutability constraints

**A PQC migration can be executed within Governance.md Article V without violating Article I immutability, because PQC migration is a "major cryptographic upgrade" to the four upgradeable facets, not a modification of the Immutable List.** [HIGH] The immutable Protocol Contract (Diamond Proxy) address does not change. The Eight Pillars, triadic logic structure, Three Mandates, evidentiary requirements, Anchors as a concept, and the Goukassian Principle all remain untouched. What changes is the signature verification logic within the Governance, Treasury, Anchor Registry, and Revocation facets.

**This is a Type 3 decision requiring ≥75% Joint-Approval and falls squarely within the existing governance scope.** [VERIFIED] Governance.md should explicitly add language scheduling a pre-2030 Type 3 PQC migration proposal to the Technical Council mandate, with candidate primitives ML-DSA-87 (aligned with NSA CNSA 2.0 selection [49]) and a SLH-DSA fallback, and requiring Custodian review of audit artifacts prior to `upgradeTo` authorization. [GAP-ARCHITECTURAL]

### Quantum threat timeline caveat

Gidney's May 2025 result reduced the qubit requirement to factor RSA-2048 by approximately 20× (now less than 1 million noisy physical qubits, roughly 1,000 to 1,400 logical qubits) [55]. IBM's Starling roadmap targets 200 logical qubits by 2029 [56]. Vitalik Buterin estimated approximately 20 percent probability that quantum computers break modern encryption before 2030 [53]. **The 2026 expert consensus has contracted by approximately 5 years relative to 2023 estimates.** [HIGH] Treat 2030-2035 as the operational migration window, not the comfortable one.

---

## 1.8 Technical Council verdict

### Core honest tension restated for the Technical Council

The Technical Council is the software-layer architect of protocol evolution within a framework that explicitly forbids modification of its Immutable List. Its authority is bounded by Article I on one side and by the Stewardship Custodians' veto on the other. **Within those bounds, its scope is the janitor role: maintaining, rotating, certifying, and upgrading, but never architecting foundational structure.** [HIGH] The software code that implements its authority is modifiable by any sufficiently-resourced adversary. The Immutable Mandates it cannot modify are also, at the software layer, only as strong as the hardware running the validator set, the relay infrastructure, and the anchor notarization network. DITL hardware enforcement via physical Escrow states is the only path to enforcement that survives full software compromise. Software governance remains necessary for accountability, auditability, and coordination. Neither layer alone is sufficient.

### Consolidated verdict

**Robust**:
- The tri-cameral separation of proposal, veto, and autonomous treasury is a correct design inversion against capture. [HIGH]
- 7-of-9 quorum with 9-member Technical Council is BFT-defensible under standard assumptions (`f = 2` tolerated). [VERIFIED]
- Diamond Proxy with permanently renounced upgradeability plus UUPS facets controlled by Joint-Approval is technically enforceable. [VERIFIED]
- Non-censorable forwarding of queued Type 3 proposals is technically enforceable via Governor-plus-Timelock patterns. [VERIFIED]
- Absence of `pause()` / `suspend()` / `freeze()` / `admin_kill()` is a defensible No Switch Off posture at the application layer. [HIGH]

**Fragile**:
- Type 1 emergency Anchor migration authority concentrated in Technical Council is the single largest capture vector. [HIGH]
- Exclusive proposal rights without a Custodian counter-proposal mechanism reproduces the EU Commission agenda-setting dominance pattern. [HIGH]
- 7-of-9 quorum under coordinated absence (WTO Appellate Body precedent) leaves `f = 3` liveness attack surface with no documented succession protocol. [GAP-ARCHITECTURAL]
- Cross-chain Anchor notarization via federated relay sets would reproduce the Ronin/Multichain/Orbit failure mode at the constitutional layer. [HIGH]
- Sustained Custodian veto of a cryptographically-urgent Technical Council proposal has no time-bound escalation. [CONSTITUTIONAL TENSION]

**Outdated**:
- Governance.md as implied does not specify PQC migration scheduling, despite NIST 2030 deprecation and 2035 disallow timelines [48][49]. [GAP-ARCHITECTURAL]
- The Diamond Standard reference in Article V does not acknowledge industry drift toward ERC-7201 namespaced storage (Final) and the pending ERC-8109 simplified diamond standard [20][23]. [GAP-RESEARCH]
- EIP-1822 formal Stagnant status [21] warrants explicit Governance.md acknowledgement that the UUPS implementation relies on OpenZeppelin's production patterns with EIP-1967 storage slots and EIP-7201 namespaced storage, not the original 1822 specification.

### Recommended updates to Governance.md

1. Add a 72-hour Custodian observation-and-escalation window for Type 1 emergency Anchor migrations, preserving Technical Council operational autonomy while closing the unilateral-emergency surface. [NOVEL]
2. Specify a pre-authorized alternate bench and 30-day succession protocol for Technical Council vacancies, filled by Custodian confirmation under existing Type 2 rules. [GAP-ARCHITECTURAL]
3. Restrict the Anchor relay layer to IBC-class trust-minimized infrastructure (permissionless relayers plus on-chain light clients, or ZK-light-client bridges with permissionless provers), excluding federated multisig relays. [NOVEL]
4. Schedule a pre-2030 Type 3 PQC migration with ML-DSA-87 primary and SLH-DSA fallback, explicitly scoped as a major cryptographic upgrade within existing Article V authority. [GAP-ARCHITECTURAL]
5. Require that Type 3 proposals include audit artifacts for new implementation content as a prerequisite for Custodian review window opening. [GAP-ARCHITECTURAL]
6. Add time-bound escalation language for the specific case where Custodian veto blocks a cryptographically-urgent Technical Council proposal, defaulting to a second Technical Council supermajority (≥75%) triggering a mandatory 14-day public comment period and a re-vote. [NOVEL]
7. Permit non-architectural migration to a successor diamond standard (ERC-8109 or equivalent Final status) subject to full Type 3 approval, without treating such migration as Article I modification. [GAP-RESEARCH]

### Where DITL hardware enforcement changes the Technical Council's role

DITL hardware does not expand Technical Council authority; it restricts what any compromised version of that authority can accomplish. [HIGH] Specifically:

- Epistemic Hold becomes a physical voltage state (NULL / half-Vdd) [1], so no software compromise of the Governance facet can force execution past it.
- The commit-audit gap at the governance-pipeline level closes at the hardware boundary: `execute_upgrade` cannot propagate unless the Escrow state attests that the Custodian review window closed without veto. [NOVEL]
- A fully captured Technical Council plus fully captured Custodian set still cannot produce execution without recorded audit evidence, because the Escrow state is dual-rail `{0,0}` NULL and is not software-addressable.
- Residual vulnerabilities (C-element hysteresis drift, dual-rail crosstalk, completion detection metastability [1]) remain physical-layer concerns and are outside the Technical Council's governance mandate. They belong to the hardware certification process.

### Constitutional integrity assessment

**The Technical Council's defined scope in Governance.md keeps it within the janitor role.** [VERIFIED] Its authority covers protocol evolution, code stewardship, certification, monitoring, and audit cadence. It has no authority to modify the Immutable List, no authority over Treasury disbursement without Custodian approval, no pause or kill function. Its exclusive proposal right is agenda-setting, not architectural. The one boundary-adjacent power is Type 1 emergency Anchor migration, which is an operational continuity action on a set that Article VI already authorizes in principle; this remains within janitor scope because the Anchor network is defined by criteria, not specific chains, and migration preserves the constitutional function rather than redesigning it.

**No part of the Technical Council's defined scope crosses into architect territory.** [HIGH] No **[CONSTITUTIONAL VIOLATION]** is identified. The architectural boundary holds. Governance is the janitor of eternity, not the architect of tomorrow, and Governance.md enforces this at the text level. Hardware enforcement via DITL is what makes the text durable against adversarial modification.

---

## Footnotes

[1] Goukassian, L., "Atomic Auditability via Delay-Insensitive Ternary Logic," DOI: 10.5281/zenodo.18716142. Introduces DITL hardware enforcement, dual-rail NCL NULL/Spacer Escrow state, four-phase handshake, Goukassian Principle in LTL, SystemVerilog assertion implementation, and residual vulnerabilities (Section VIII: C-element hysteresis drift, dual-rail crosstalk, completion detection metastability).

[2] Optimism Collective. OPerating Manual, https://github.com/ethereum-optimism/OPerating-manual/blob/main/manual.md; "The Future of Optimism Governance," https://www.optimism.io/blog/the-future-of-optimism-governance.

[3] International Atomic Energy Agency. Governance structure, https://www.iaea.org/about/governance.

[4] US Nuclear Regulatory Commission. Commission functions and organization, https://www.nrc.gov/about-nrc/organization/commfuncdesc.

[5] IETF. RFC 8711 IASA 2.0, https://www.rfc-editor.org/rfc/rfc8711.html; RFC 4089.

[6] Python. PEP 13, https://peps.python.org/pep-0013/; PEP 8016, https://peps.python.org/pep-8016/.

[7] International Institute for Sustainable Development, "WTO Dispute Settlement Without the Appellate Body," https://www.iisd.org/articles/policy-analysis/wto-dispute-settlement-without-appellate-body. Appellate Body non-functional since December 10, 2019; all terms expired November 30, 2020.

[8] Castro, M. and Liskov, B., "Practical Byzantine Fault Tolerance," 1999. `n ≥ 3f+1` safety bound, https://www.comp.nus.edu.sg/~rahul/allfiles/cs6234-16-pbft.pdf.

[9] Abraham et al., unified BFT view, https://www.usenix.org/system/files/nsdi24-amiri.pdf. Fast two-step BFT `5f - 1` lower bound.

[10] European Parliament, "Parliament's right of initiative," https://www.europarl.europa.eu/RegData/etudes/BRIE/2025/767211/EPRS_BRI(2025)767211_EN.pdf; AFCO resolution 22-5-1 adopted April 2022.

[11] The Block, "Build Finance DAO suffers hostile governance takeover," February 14, 2022, https://www.theblock.co/post/134180/build-finance-dao-suffers-hostile-governance-takeover-loses-470000.

[12] rekt.news, "The Humpy Dance," https://rekt.news/the-humpy-dance; CoinDesk, July 29, 2024, https://www.coindesk.com/markets/2024/07/29/comp-down-67-after-supposed-governance-attack-on-compound-dao.

[13] Immunefi, "Hack Analysis: Beanstalk Governance Attack April 2022," https://medium.com/immunefi/hack-analysis-beanstalk-governance-attack-april-2022-f42788fc821e; Halborn.

[14] OpenZeppelin, Governor and TimelockController documentation, https://docs.openzeppelin.com/contracts/4.x/governance; Compound Governance, https://docs.compound.finance/v2/governance/.

[15] ERC-2535 Diamond Standard, Final status, https://github.com/ethereum/ercs/blob/master/ERCS/erc-2535.md; PR #5802, https://github.com/ethereum/EIPs/pull/5802.

[16] Cyfrin CodeHawks, Beanstalk "The Finale" contest findings, May 2024, https://codehawks.cyfrin.io/c/2024-05-beanstalk-the-finale/s/5.

[17] ChainScore Labs, upgradable contract design guidance, https://www.chainscorelabs.com/en/blog/smart-contract-auditing-and-best-practices/upgradable-contract-design/why-your-diamond-pattern-implementation-is-insecure.

[18] Zealynx, "The Dark Side of Upgrades," January 29, 2026, https://www.zealynx.io/blogs/upgrade-patterns-security.

[19] OpenZeppelin Contracts GitHub, issue #2793 (Diamond implementation request, unimplemented).

[20] Mudge, N., Ethereum Magicians forum, "Revising ERC-2535 Diamonds to simplify and improve the terminology," https://ethereum-magicians.org/t/revising-erc-2535-diamonds-to-simplify-and-improve-the-terminology/26973/20.

[21] EIP-1822 UUPS, Stagnant status, https://eips.ethereum.org/EIPS/eip-1822; ERCs repo confirmation.

[22] OpenZeppelin proxy documentation and `UUPSUpgradeable` pattern using EIP-1967 slots.

[23] ERC-7201 Namespaced Storage Layout, Final status, https://eips.ethereum.org/EIPS/eip-7201.

[24] OpenZeppelin Security Advisory GHSA-5vp3-v4hc-gx76 / CVE-2021-41264, https://github.com/OpenZeppelin/openzeppelin-contracts/security/advisories/GHSA-5vp3-v4hc-gx76; post-mortem https://forum.openzeppelin.com/t/uupsupgradeable-vulnerability-post-mortem/15680.

[25] Iosiro, UUPS proxy disclosure, https://www.iosiro.com/blog/openzeppelin-uups-proxy-vulnerability-disclosure.

[26] EIP-6780 SELFDESTRUCT changes in Cancun, March 2024; ConsenSys Dencun analysis, https://consensys.io/blog/ethereum-dencun-upgrade-explained-part-1.

[27] CertiK, upgradeable proxy security best practices; Three Sigma, upgradeable contract risks, https://threesigma.xyz/blog/web3-security/upgradeable-contract-security-risks-vulnerabilities.

[28] Audius governance takeover post-mortem, July 23, 2022, https://blog.audius.co/article/audius-governance-takeover-post-mortem-7-23-22; technical analysis https://jordaniza.com/posts/technical-overview-of-the-audius-exploit/.

[29] OpenZeppelin Contracts issue #6362 (v4 to v5 storage migration deadlock).

[30] Halborn, Ronin hack analysis, https://www.halborn.com/blog/post/explained-the-ronin-hack-march-2022; CoinDesk, March 29, 2022.

[31] b10c Mining Centralization Index, https://b10c.me/blog/015-bitcoin-mining-centralization/; March 2025 Foundry seven-consecutive-block incident.

[32] ethernodes.org; Messari validator decentralization report; Dune staking dashboards 2025.

[33] mevwatch.info; CoinDesk, "Ethereum's censorship problem is getting worse," December 2023, https://www.coindesk.com/tech/2023/12/06/ethereums-censorship-problem-is-getting-worse.

[34] Offchain Labs, Ethereum mainnet finality post-mortem May 11-12, 2023, https://medium.com/offchainlabs/post-mortem-report-ethereum-mainnet-finality-05-11-2023-95e271dfd8b2.

[35] Cointelegraph, Ethereum Fusaka / Prysm v7.0.0 participation incident, late 2025.

[36] Phemex, Cardano 8th anniversary; DailyCoin Cardano uptime; 2,923 days of continuous operation as of September 23, 2025.

[37] Chainspect dashboard, April 2026 snapshot, https://chainspect.app/dashboard/decentralization; Polkadot key metrics, https://polkadot.com/key-metrics.

[38] Messari, "Evaluating Validator Decentralization," https://messari.io/report/evaluating-validator-decentralization-geographic-and-infrastructure-distribution-in-proof-of-stake-networks.

[39] Helius, Solana outage history, https://helius.dev/blog/solana-outages-complete-history; StatusGator.

[40] Messari, State of Aptos Q4 2023, https://messari.io/report/state-of-aptos-q4-2023.

[41] Polygon Heimdall v2 hard fork, July 10, 2025, https://polygon.technology/docs; Stakin Polygon analysis.

[42] Messari, State of Avalanche Q4 2025, https://messari.io/report/state-of-avalanche-q4-2025.

[43] Metrika, "Post-mortem: AWS Outage October 2025," https://metrika.co/blog/post-mortem-aws-outage-10-2025; Stellar policy blog.

[44] IBC Protocol, IBC v2 announcement, https://ibcprotocol.dev/blog/ibc-v2-announcement; Succinct SP1 IBC Eureka, https://blog.succinct.xyz/ibc/; CoinDesk IBC Eureka launch April 10, 2025; Chainlink CCIP architecture, https://docs.chain.link/ccip/concepts/architecture/offchain/overview; LayerZero v2 DVN documentation, https://docs.layerzero.network/v2/deployments/dvn-addresses; Halborn bridge post-mortems; Chainalysis Q1 2025 report.

[45] NIST, "NIST Releases First 3 Finalized Post-Quantum Encryption Standards," August 13, 2024, https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards.

[46] NIST FIPS 206 FN-DSA status presentation, https://csrc.nist.gov/csrc/media/presentations/2025/fips-206-fn-dsa-(falcon)/images-media/fips_206-perlner_2.1.pdf.

[47] NIST, "NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption," March 11, 2025, https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption; NIST IR 8545.

[48] NIST IR 8547 Initial Public Draft, https://csrc.nist.gov/pubs/ir/8547/ipd; SP 800-131A Rev 3 IPD.

[49] NSA CNSA 2.0 Algorithms, May 30, 2025, https://media.defense.gov/2025/May/30/2003728741/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS.PDF. ML-KEM-1024, ML-DSA-87, AES-256, SHA-384/512, LMS, XMSS.

[50] UK NCSC, PQC migration timelines, March 2025, https://www.ncsc.gov.uk/guidance/pqc-migration-timelines.

[51] EIP-8051 ML-DSA precompile, https://eips.ethereum.org/EIPS/eip-8051; EIP-7619 Falcon-512, https://eips.ethereum.org/EIPS/eip-7619; EIP-8052.

[52] EIP-7702 live on Pectra hardfork, May 2025.

[53] Ethereum Foundation "Quantum Roadmap" post, February 26, 2026; CoinDesk, DL News, CryptoPotato coverage.

[54] pq.ethereum.org roadmap; Ethereum Foundation January 2026 PQC strategic priority declaration; leanSig paper, https://eprint.iacr.org/2025/055.pdf.

[55] Gidney, C., "How to factor 2048 bit RSA integers with less than a million noisy qubits," May 2025, https://arxiv.org/abs/2505.15917.

[56] IBM Quantum, "Large-scale fault-tolerant quantum computing roadmap," June 10, 2025, https://www.ibm.com/quantum/blog/large-scale-ftqc.
