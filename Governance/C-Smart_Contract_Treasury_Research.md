## Ternary Logic Constitutional Governance Research - Section 3
**Framework:** Ternary Logic (TL) by Lev Goukassian
**ORCID:** 0009-0006-5966-1243
**Research Date:** Q2 2026
**Status:** Standalone Report - Section 3 of 4

---

## Executive summary and the core honest tension

The Smart Contract Treasury is the only body in the TL constitutional architecture with zero vote rights and zero discretionary authority. It is a financial state machine that executes Joint-Approved rules and nothing else. That is its strongest property and its most dangerous one. **Any software can be modified - by humans with root access, by advanced machine learning agents with supply-chain reach, or by state-level adversaries with firmware-level access. This is not theoretical. It is an architectural fact.** [VERIFIED]

Constitutional guarantees written in smart contract code are only as strong as the hardware beneath them. The sole path to genuine enforcement of the Immutable Mandates is Delay-Insensitive Ternary Logic (DITL) hardware, where Epistemic Hold is not a policy commitment but a physical voltage state at half-Vdd that no software call, root account, kernel compromise, or firmware flash can override. The Atomic Auditability paper formalizes this as the Goukassian Principle in Linear Temporal Logic and specifies it in SystemVerilog assertions. [VERIFIED per source documents]

This does not invalidate the smart contract architecture. It locates it honestly. **Software governance provides accountability, auditability, and coordination. Hardware governance provides enforcement. Both are necessary. Neither alone is sufficient.** [NOVEL]

The verdict up front: the Treasury's vote-right absence is constitutionally robust in design and empirically unprecedented in production. No comparable autonomous fiduciary with no admin key, no pause guardian, no emergency shutdown, and no discretionary milestone verifier has been deployed and survived adversarial testing as of Q2 2026. [HIGH] Every production DeFi recovery at scale has relied on god-mode authority or off-chain social coordination. [VERIFIED] Without DITL hardware beneath it, the Treasury's guarantees reduce to social-layer trust in whoever controls the compiler, the deployer key, and the node infrastructure. With DITL, those guarantees become physics. [NOVEL]

---

## 3.1 Smart contract treasury vote rights architecture

The Treasury's complete absence of vote rights is the architecturally distinctive claim. Nothing comparable exists in production as of Q2 2026. Every major on-chain treasury surveyed retains some form of privileged override: a pause guardian, an emergency shutdown, a multisig with admin authority, or a governance body that can rewrite the executor.

### The autonomy gap in comparable systems

**MakerDAO's Emergency Shutdown Module (ESM)** is the canonical counter-example of what TL explicitly forbids. Any address may burn MKR into the ESM contract; when burned MKR crosses the threshold (raised from 50,000 in the original design to 75,000, then 100,000 in February 2022, then **300,000 MKR by executive vote on July 25, 2024**), any caller can invoke `fire()` to halt the entire protocol and trigger collateral auction settlement. [VERIFIED][1] This is a full god-mode mechanism. Under TL's Article VIII ("No Switch Off"), an equivalent would be a [CONSTITUTIONAL VIOLATION] of the absolute mandate. Maker governance can also disarm the ESM by deauthorizing `End.cage()`, meaning honest governance retains override of the override - a layered god-mode that TL architecturally rejects.

**Compound Finance** retains a Pause Guardian multisig that can halt `supply`, `transfer`, `withdraw`, `absorb`, and `buyCollateral` per-market, though asymmetrically it cannot unpause (only governance can). [VERIFIED][2] Compound's proposal threshold is 25,000 COMP delegated (reduced from 100,000); quorum is 400,000 votes. Cycle time from proposal to execution is minimum 7 days: 2-day review, 3-day voting, 2-day timelock, with major risk-system upgrades typically using the 14-day delay. [VERIFIED][3]

**Aave v3** maintains two separate 5-of-9 emergency multisigs: a Protocol Emergency Guardian holding the `EMERGENCY_ADMIN` role that can freeze or pause supply/borrow/liquidation per-asset or globally, and a Governance Emergency Guardian authorized to veto malicious on-chain governance payloads based on Certora formal verification findings. [VERIFIED][4] The Aave Umbrella upgrade (2024-2025) introduced automated bad-debt coverage that burns staked aTokens without governance intervention, but only within the narrow on-chain-solvency domain - not for arbitrary milestone-triggered disbursement.

**Uniswap's governance treasury** is controlled by UNI token voting with a minimum cycle of approximately 16 days: 7-day RFC, 5-day temperature check on Snapshot, 2-day voting delay, 7-day on-chain vote, and 2-day timelock. [VERIFIED][5] The treasury is wallet-plus-committee, not autonomous.

**Nouns DAO** offers the closest comparable pattern to TL's philosophy, not through treasury autonomy but through its **fork mechanism** (V3 upgrade, August 2023). Any Noun holder may escrow tokens during a fork period; if the escrow threshold (originally 20%, later raised to 30%) is met, a new Fork DAO is deployed via `ForkDAODeployer` and forkers receive a pro-rata share of treasury ETH. Three forks executed September-October 2023: Fork 1 saw approximately 56% of Nouns (472 of 846) exit with ~16,757 ETH ($27M at the time); Fork 2 saw approximately 20% exit with ~2,035 ETH. [VERIFIED][6] The fork pattern converts governance disagreement into value-preserving exit rather than protocol intervention. It is the strongest published "exit without god-mode" pattern, but it is exit, not repair, and it applies to fractional-ownership tokens rather than to a rule-bound treasury.

**Protocol Guild Vesting Contract** vests to a curated membership but retains membership-management authority in the Pilot multisig. Not truly autonomous. [HIGH]

**Three-party autonomous fiduciary as specified by TL (Technical Council proposes, Custodians approve, Treasury autonomously executes) has no production precedent.** [HIGH] The closest production topology is the oSnap pattern: Snapshot off-chain vote plus UMA Optimistic Oracle verification plus a Gnosis Safe module that auto-executes payload data after liveness expires, with no multisig signature required. CoW DAO, Across Protocol, Connext, Gitcoin DAO (passed with 98.67% approval), and Developer DAO have adopted this pattern, with oSnap securing approximately $689M by end of 2024. [VERIFIED][7] But oSnap's "third party" is still human voters, not a second independent body with constitutional duties.

### The milestone verification problem

The Treasury disburses on "verifiable on-chain milestones" such as "protocol upgrade vX.Y is deployed and verified" or "audit report Z is published to IPFS." The unavoidable question: who verifies?

Four categories of verification exist, and each relocates trust rather than eliminating it:

1. **EXTCODEHASH-based code deployment verification** is trustless for the statement "bytecode hash X is deployed at address Y." It is not trustless for the statement "hash X is the correct, audited, intended version for milestone M." The latter requires off-chain attestation. [VERIFIED]

2. **Ethereum Attestation Service (EAS)** permits tokenless schema-based attestations on-chain or off-chain with IPFS pinning. [VERIFIED][8] EAS does not eliminate trust; it concentrates it in the attester's signing key. Without dispute mechanism, EAS reduces to "whoever holds the signing key decides milestones" - a functional god-mode held by the attester set. [HIGH]

3. **UMA Optimistic Oracle v3** accepts asserted claims under a configurable bond and default 2-hour liveness window; disputes escalate to UMA's DVM token-holder vote with multi-day resolution. [VERIFIED][9] This is the strongest production pattern for milestone claims that are human-adjudicable. It is not trustless; it is economically secured dispute-game adjudication.

4. **zkVMs (SP1, RISC Zero)** prove that computation C on input I produced output O. R0VM 2.0 (April 2025) reduced Ethereum block proving from 35 minutes to 44 seconds. [VERIFIED][10] zkVMs solve verification only for milestones expressible as pure functions of on-chain-verifiable inputs - for example, "this bytecode compiles deterministically from this source tree" or "all tests pass on this committed git hash." They do not solve "did the grantee deliver real-world milestone M."

**No production protocol performs fully autonomous, off-chain-milestone-based, non-oracle-dependent treasury disbursement at scale.** [HIGH] Every production system reduces to one of: trust an oracle, trust an attester set, or trust a dispute-game of humans. The TL Treasury inherits this constraint. The Joint-Approval rule-encoding step is where trust is actually imposed: the two bodies encode, at rule-definition time, which oracle, attester, or dispute game is authoritative for each milestone category.

### Joint-Approval cycle time and governance paralysis risk

The 75%+75% threshold across two bodies is stringent. If comparable production cycle times are a guide - Compound approximately 7 days, Aave short-executor 5 days, Uniswap 16 days, L2BEAT Stage 2 exit window ≥30 days [VERIFIED][3][5][11] - then TL Joint-Approval for routine budget adjustments plausibly takes 2-4 weeks including both bodies' deliberation. This is appropriate for constitutional rule changes and dangerous for operational tempo. [HIGH]

The constitutional answer is that this is a feature, not a bug. The Treasury's encoded rules must be stable enough that annual cycles suffice. If operations require frequent rule changes, the rules are insufficiently abstract. [NOVEL]

### The economic denial-of-service vector

If an adversary captures one body sufficiently to deny 75% supermajority, the Treasury continues collecting fees autonomously but cannot encode new disbursement rules. Fees accumulate. Operational funding starves. The adversary does not need to attack the Treasury directly; attacking Joint-Approval is sufficient.

The Compound "Humpy" / Golden Boys attack (Proposal 289, July 2024) demonstrated spot-market accumulation capture: a whale coalition acquired COMP on the open market and passed a proposal transferring approximately 499,000 COMP ($24M, about 5% of treasury) to a yield vault they controlled. [VERIFIED][12] The proposal was withdrawn only after social pressure. This was quorum capture by accumulation, not spam. TL's two-body structure with no token-weighted voting is not directly vulnerable to this vector, but capture of membership selection in either body is the equivalent vector. [HIGH]

The **Tribe DAO dissolution** provides the clearest fee-accumulation precedent. After the April 30, 2022 Fei-Fuse reentrancy exploit drained approximately $80M, Tribe DAO voted to reimburse victims from treasury; a minority faction of FEI insiders subsequently vetoed on-chain execution through governance. TIP-121 wound down the DAO on August 19, 2022, converting PCV to DAI. As of 2024-2026, TRIBE still traded on major exchanges and autonomous contract roles remained listed while the treasury was effectively empty. [VERIFIED][13] This is the canonical "zombie governance" precedent - autonomous contracts continuing to operate while governance is dead.

### Adversarial failure analysis

| Precedent | Mechanism | Layer | TL Treasury outcome | Additional constraint (no god-mode) |
|---|---|---|---|---|
| Beanstalk flash-loan governance (April 2022, ~$77M) | Flash-loan voting power, `emergencyCommit()` passed malicious BIP18 in one block; no delegation checkpointing | Software (protocol) | Prevented: no token-weighted voting; two-body approval; no `emergencyCommit()` function | Require attestation that no voting weight was acquired within N blocks of vote |
| Compound Proposal 62 bug (Sept 2021, ~$62M unrecovered) | Distribution bug; 7-day timelock prevented fast fix; `drip()` remained permissionless during delay | Software | Equally vulnerable: rule-bug in encoded Treasury rule would execute identically; timelock cannot be accelerated without god-mode | Require rules to include circuit-breaker clauses (per-epoch max disbursement) that are themselves encoded rules, not overrides |
| Compound "Humpy" Prop 289 (July 2024, $24M) | Open-market accumulation of voting power | Social/economic | Partially mitigated: no token voting in TL; attack surface shifts to body-membership capture | Membership renewal with staggered terms and cross-body nomination (covered in other sections) |
| Tribe DAO dissolution (May-Aug 2022) | Governance deadlock; contracts continued operating after DAO dead | Social | Directly applicable: Treasury cannot be shut down under Article VIII; fees continue to accumulate | Rule encoding must include terminal-state clauses - what Treasury does when Joint-Approval is permanently unreachable |
| Mango Markets oracle manipulation (Oct 2022, ~$110-117M) | Manipulated MNGO spot price fed into collateral oracle | Oracle | Vulnerable if Treasury milestone verification uses manipulable price feed | Use multi-source oracle aggregation with dispute window for any milestone involving price data |
| Tornado Cash governance takeover (May 2023) | Malicious proposal containing hidden `selfdestruct` in `emergencyStop` function; attackers minted 1.2M votes | Software/social | Partially mitigated: two-body structure forces malicious payload to pass two independent reviews; but equally vulnerable if Custodian review is not technical | Mandate that every Joint-Approval proposal pass formal verification on the payload bytecode, not only the English description |

### Verdict on vote-right architecture

The Treasury's absence of vote rights is constitutionally coherent and empirically unprecedented. [HIGH] The architectural question is whether the Joint-Approval rule-encoding layer adequately replaces the discretionary authority that production treasuries rely on. The honest answer: **only if the rules themselves are sufficiently expressive to encode circuit-breakers, terminal-state behavior, and oracle-dispute escalation without requiring god-mode overrides.** [NOVEL] The Compound Prop 62 case is the empirical proof that rule-bound autonomy without fast-override can amplify losses. TL must confront this directly: rule expressiveness is the load-bearing design constraint.

---

## 3.2 On-chain governance current state (Q2 2026)

As of Q2 2026, the most sophisticated on-chain governance implementations have converged on a pattern: off-chain discussion plus Snapshot temperature check plus on-chain vote plus timelock plus selective guardian veto. None has eliminated the guardian role without either (a) restricting the governance scope to narrow on-chain parameters or (b) retaining an upgrade path controlled by a small multisig.

### The immutability-upgradeability tension

Optimism operates a bicameral design with the Token House (OP token holders voting on protocol upgrades, treasury appropriations, and inflation) and the Citizens House (identity-based Retroactive Public Goods Funding). [HIGH] Citizens are selected via RetroPGF rounds. The two houses have different scopes rather than co-equal veto. This is not genuinely analogous to TL's two-body Joint-Approval where both must approve the same action.

L2 maturity frameworks provide the clearest public honest-disclosure language. Vitalik Buterin's November 2022 proposal and L2BEAT's June 2023 Stages Framework define Stage 0 (fully controlled), Stage 1 (limited training wheels; upgrades outside a Security Council require ≥7-day exit window; compromising ≥75% of Security Council required to block withdrawals), and Stage 2 (permissionless fraud proofs, ≥30-day exit window, Security Council restricted to adjudicable on-chain bugs only). [VERIFIED][11] As of January 2025, per Buterin's own statement, three Stage 1 rollups existed (Optimism, Arbitrum, Ink) and three Stage 2 rollups (DeGate, zk.money, Fuel). [VERIFIED][14] By late 2025, Arbitrum One, OP Mainnet, and Base operated Stage-1-class fraud proofs. L2BEAT explicitly states its stages "do not reflect rollup security" but rather "maturity of decentralization" - a distinction TL's constitutional framework should explicitly adopt.

**Smart contract treasury immutability is functionally Stage 2.** [NOVEL] TL's No Switch Off mandate aligns with Stage 2's restriction of Security Council authority to adjudicable on-chain bugs. The difference: TL has no Security Council at all.

### Known governance attacks 2023-2026

**Tornado Cash governance takeover (May 20, 2023):** Attackers submitted a proposal appearing to duplicate a prior legitimate proposal but containing a malicious `emergencyStop` function invocation. Upon passage and execution, the payload minted 1.2M votes to the attacker, granting full governance control. Attacker eventually returned voting power after extracting approximately $1M in TORN. [VERIFIED][15] Lesson: the two-body structure is only as strong as the technical review of the proposal payload, not only its English description.

**Compound Proposal 289 / Humpy attack (July 2024):** Open-market voting-power accumulation; 499,000 COMP (~$24M, 5% of treasury) proposed for transfer to attacker-controlled vault. Eventually withdrawn under social pressure. [VERIFIED][12]

**Arbitrum AIP-1 controversy (March 2023):** Foundation pre-allocated 750M ARB tokens before the community ratification vote; disclosure triggered significant community backlash. Demonstrates that governance token pre-allocations made before on-chain mechanisms activate are a pre-constitutional vulnerability TL should foreclose explicitly. [VERIFIED][16]

**Beanstalk (April 2022, $182M)** remains the canonical flash-loan governance attack baseline. One-block voting plus insufficient delegation checkpointing. [VERIFIED][17] No direct 2023-2026 successor of equivalent scale was located in public reporting; the pattern appears to have been closed by minimum-hold-time and checkpoint requirements in subsequent Governor implementations.

### Joint-Approval as bicameral on-chain governance

No multi-chamber on-chain governance design has survived adversarial testing in a form directly analogous to TL's 75%+75% across two independent bodies. [GAP-RESEARCH] Optimism's Token House plus Citizens House is the closest production instance but operates scope-separated rather than co-equal. The oSnap pattern is closer in topology (Snapshot vote plus UMA OO plus Safe executor) but is a sequential dispute-game rather than two independent supermajorities.

### Gas economics under adversarial conditions

Ethereum L1 gas has spiked during historical congestion events (NFT mints, market crashes, DEX arbitrage on depeg events). EIP-4844 (Dencun upgrade, March 13, 2024) introduced blob transactions that dramatically reduced L2 data-availability posting costs. [VERIFIED][18] For governance transactions posted on L1, gas-price spikes during peak congestion have historically priced out small holders from voting; Compound's 25,000 COMP proposal threshold already gates spam. MEV extraction of governance votes has not been documented as a successful attack in production, but frontrunning of governance-timed actions (e.g. liquidations triggered by a governance-adjusted parameter) is a documented pattern in Flashbots analyses. [HIGH]

For TL, the implication is that Joint-Approval transactions on L1 must budget for peak-congestion gas costs, and that the Treasury's disbursement transactions should be priority-fee-insensitive (executable by anyone willing to pay gas) to prevent operational griefing. [NOVEL]

---

## 3.3 The Treasury as autonomous fiduciary

### Best practice for milestone-gated disbursement

Current production milestone-gated disbursement infrastructure has three categories:

**Optimistic oracle pattern (UMA OO, Reality.eth):** Assertion-plus-bond-plus-liveness-plus-dispute-escalation. UMA OO v3 uses configurable bonds (minimum = `finalFee`) and default 2-hour liveness; disputes escalate to DVM token-holder vote with multi-day resolution. Reality.eth uses escalating bonds with an arbitrator (often Kleros) for terminal resolution. [VERIFIED][9][19] This pattern secures approximately $689M via oSnap deployments as of 2024 year-end.

**Attestation pattern (EAS):** On-chain and IPFS-pinned signed attestations from whitelisted attesters. Permissionless schema registry plus free attestation. [VERIFIED][8] Trust is concentrated in the attester set.

**Cryptographic proof pattern (SP1, RISC Zero):** zkVM proofs of deterministic computation. Production-ready on-chain verifiers on multiple chains. Not applicable to real-world milestone verification. [VERIFIED][10]

For TL, the honest architectural choice at rule-encoding time is: which milestone category maps to which verification pattern? A "protocol upgrade deployed and verified" milestone maps cleanly to EXTCODEHASH plus zkVM reproducible-build proof. A "published audit report matches specification" milestone requires EAS attestation or UMA OO adjudication. A "grantee delivered deliverable D" milestone requires optimistic oracle with dispute.

### Can autonomy be a security feature when rules produce wrong outcomes?

The Compound Proposal 62 case is the empirical answer: **no, not without rule-level circuit-breakers.** When the distribution bug was identified, the 7-day governance delay permitted continued permissionless `drip()` calls that moved an additional $68.8M into drainable state. Approximately 163,000 COMP was voluntarily returned; approximately 200,000 COMP ($62M) was never recovered. [VERIFIED][20] Timelock amplified the loss.

The Nouns fork mechanism demonstrates the alternative recovery path: **value-preserving exit rather than protocol intervention.** [HIGH] TL does not have tokens to fork, but the pattern suggests a constitutional primitive: if Joint-Approval produces a rule the dissenting party considers catastrophically wrong, the recovery path is not override but *rule-level exit clauses* encoded at Joint-Approval time. This is architecturally different from god-mode pause.

The **MakerDAO Emergency Shutdown Module is explicitly what TL cannot have.** [CONSTITUTIONAL VIOLATION if adopted] The ESM halts the protocol via MKR burn. The TL Treasury cannot be halted under any circumstance by any mechanism. This is absolute under Article VIII.

### Three-party autonomous fiduciary track record

**No production deployment of a three-party autonomous fiduciary, where two independent bodies approve and a third autonomously executes without human-veto path, has survived adversarial conditions.** [HIGH] The Aave Umbrella automated bad-debt coverage is the closest fully-automated production mechanism but operates only in the narrow on-chain-solvency domain. [VERIFIED][4] Every adjacent pattern (oSnap, Reality Module, Compound Timelock) retains human voters as one of the parties.

The Mirror Protocol collapse and Euler Finance hack are instructive inverse cases. Mirror's contracts remained on-chain but rendered inert by Band Protocol's August 11, 2022 cessation of price-feed support, demonstrating autonomous-contract brittleness to oracle withdrawal. [VERIFIED][21] Euler's $197M hack (March 13, 2023) was recovered entirely through social/off-chain negotiation plus law-enforcement pressure; the attacker returned funds in tranches through April 3, 2023. [VERIFIED][22] No autonomous mechanism executed the recovery.

### Gas-price spike exposure

Historical Ethereum congestion events have priced governance actions above small-holder participation thresholds but have not permanently blocked critical governance. EIP-4844 reduced L2 costs but did not fundamentally change L1 congestion dynamics. [VERIFIED][18] TL's exposure is moderate: Joint-Approval transactions are infrequent by design, so occasional cost spikes are tolerable; Treasury disbursement transactions are frequent and should be gas-priority-insensitive. The residual risk is targeted denial-of-service timed to coincide with Joint-Approval windows.

---

## 3.4 The Revocation Contract and automated slashing

### The canonical automated-slashing false-positive precedent

The widely-cited "approximately 1,700 Lido validators slashed in early 2023" claim **does not match primary sources.** [VERIFIED] The actual incident is:

**RockLogic GmbH / Lido slashing (April 13, 2023):** Eleven validators slashed, beginning at 12:50 UTC and resolved by 15:30 UTC (epochs 194182-194183). Root cause: a Prysm consensus client bug (issue #12281) in which previously-deleted validator keys were unexpectedly re-imported after a BN+VC client update, causing duplicate attestations alongside their active counterparts elsewhere. Fixed in Prysm v4.0.3 (April 21, 2023). Total penalties approximately 11.19 ETH per the Lido post-mortem. Lido DAO and RockLogic reimbursed the impacted staker pool via a "slashing-burn omnibus" beginning June 20, 2023. [VERIFIED][23]

Larger-scale precedents that establish the automated-slashing false-positive pattern:

**Medalla testnet incident (August 14-19, 2020):** Cloudflare Roughtime servers returned incorrect time (one server jumped approximately 24 hours ahead); the Prysm client did not properly fall back to alternate time sources. Nodes exhibited ~4-hour clock skew, signing attestations for future slots. A rushed Prysmatic Labs hotfix contained a critical flaw removing necessary features; when clocks re-synced, all future-dated Prysm attestations became valid, and validators attempted to get slashed en masse. **Over 3,000 slashing events** broadcast in a short period; validator participation dropped from ~80% to ~5%. Prysmatic Labs' own internal validators were slashed because they had not configured local slashing protection. [VERIFIED][24]

**SSV Network mass slashing (September 10, 2025):** One validator slashed at 11:51 UTC; 39 more approximately 90 minutes later. Total of 40 validators. Root cause: Ankr maintenance misconfiguration left validator keys active in two infrastructures simultaneously, causing parallel signing; Allnodes had a similar stale-migration issue. Per-validator loss approximately 0.3 ETH. SSV Protocol itself was not compromised; failure was in off-SSV key handling. [VERIFIED][25]

These are the empirical proof that **sensor/oracle/monitoring data feeding automated slashing contracts malfunctions at scale, in production, multiple times.** [VERIFIED] The failure mode is not malicious attack on the slashing contract - it is infrastructure misconfiguration producing false attestations that the contract correctly interprets as slashable offenses.

### Current automated slashing state

**Ethereum Beacon Chain post-Pectra (live May 7, 2025):** Three slashable offenses (proposer double-proposal, attester double-vote, attester surround-vote). Initial slashing penalty scales with effective balance: `effective_balance / MIN_SLASHING_PENALTY_QUOTIENT` where quotient = 4096 post-Pectra (previously 32). A 32 ETH validator faces approximately 0.0078 ETH initial penalty; a 2,048 ETH validator approximately 0.5 ETH. Correlation penalty is applied on day 18 of the 36-day exit queue based on summed effective balances of validators slashed in the surrounding 18-day window. **Slashing is entirely algorithmic and cannot be reversed by governance.** [VERIFIED][26]

**Cosmos SDK:** `SlashFractionDoubleSign` = 5% plus tombstoning; `SlashFractionDowntime` = 1% SDK default (Cosmos Hub uses 0.01%). [VERIFIED][27]

**Polkadot** is uniquely relevant to TL: its slashing mechanism has a **built-in 27-day grace period** during which governance can reverse a slash before application. Slashed DOT is frozen for 256 eras (~9 months), then split 50/50 between burn and treasury. This is a direct production precedent for TL's "revocation stands unless overturned" design. [VERIFIED][28]

**EigenLayer slashing** went live on mainnet April 17, 2025, opt-in by AVS, defined in ELIP-002. [VERIFIED][29] Too recent for meaningful false-positive dataset.

### Minimum overturn cycle times

| Protocol | Fastest overturn | Realistic with forum discussion |
|---|---|---|
| Compound-style | ~7 days | 10-14 days |
| Aave Short Executor | ~5 days | ~8-11 days plus 3d Snapshot plus forum |
| Uniswap-style | ~16 days | 3+ weeks |
| Polkadot slash grace (built-in) | 27 days | 27 days |

If TL governance cycle time approximates Compound or Aave Short Executor, an incorrect automated revocation deplatforms an honest operator for 5-14 days before overturn. [HIGH] This is the denial-of-service vector against honest node operators: **the revocation stands is the weapon, not the slashing itself.** [NOVEL]

### Oracle compromise vector

Oracle/monitoring-data manipulation analogues from DeFi are severe and relevant. The Mango Markets attack (October 11, 2022, Avraham Eisenberg, approximately $110-117M drained in 30-40 minutes by pumping MNGO spot 1,000-2,300% to inflate collateral value) demonstrates that manipulable data feeds produce catastrophic autonomous-contract outcomes. [VERIFIED][30] bZx (February 2020, ~$954K combined), Cream Finance (October 27, 2021, ~$130M), Inverse Finance ($15.6M April 2022 plus $1.26M June 2022), and Chainalysis' 2022 estimate of $403.2M across 41 oracle manipulation attacks establish the pattern. [VERIFIED][31] No successful compromise of Chainlink's decentralized price feeds has been documented; attacks target protocols using single-DEX spot prices.

**If the on-chain monitoring service feeding the Revocation Contract is compromised or manipulated, it will trigger mass false-positive revocations that automated slashing will execute correctly and that governance will take 5-14+ days to overturn.** [HIGH] This is a [CONSTITUTIONAL TENSION] with the No Switch Off mandate: the Revocation Contract cannot itself be paused during an oracle-compromise event under Article VIII.

The mitigation that does not require god-mode is **Polkadot's built-in grace period pattern:** slashing conditions enter an "unapplied state transition" for a fixed pre-enforcement delay during which the governance vote can reverse. This is rule-level, not override. TL should encode a minimum 7-day pre-enforcement delay on all revocations with the rule itself, not as a pause. [NOVEL]

---

## 3.5 DITL as the honest constitutional floor

### Fabrication status verification (Q2 2026)

**[GAP-ARCHITECTURAL]** As of Q2 2026, no production deployment of DITL or NULL Convention Logic (NCL) governance/safety hardware has been located. The paradigm is real and peer-reviewed but remains at design specification, transistor-level simulation, FPGA demonstration, and small research-ASIC stages. The specific Zenodo record 10.5281/zenodo.18716142 ("Atomic Auditability") is referenced in the TL framework materials as the primary source for DITL specifications; it was not independently corroborated via external search in this research session and should be verified directly via the Zenodo DOI resolver.

Verifiable academic lineage of DITL and NCL:

- Parameswaran Nair, R.S. (MS thesis, Missouri S&T, advisor Scott C. Smith, 2007): origin of the "DITL" term; transistor-level simulation in IBM 130nm PDK. [VERIFIED][32]
- Smith et al., "Delay Insensitive Ternary CMOS Logic for Secure Hardware" (J. Low Power Electron. Appl. 5(3):183, 2015): DITL Adder plus 8051 ALU, transistor-level simulation, not taped out. [VERIFIED][33]
- IEEE, "Design and Analysis of 4-Bit Adder Using DITL" (2020): 90nm CMOS simulation, 1.1V, 128.3µW, 258.9ns propagation delay. Simulation only. [VERIFIED][34]
- Cole Sherrill (Univ. of Arkansas, 2024): automated design flow from synchronous RTL to optimized layout using commercial EDA tools for Multi-Threshold NCL circuits; 64-bit adders, Montgomery multipliers, AES-256 cores in TSMC 65nm - a synthesis-flow paper, not a fabricated governance chip. [VERIFIED][35]

Commercial lineage: **Theseus Logic Inc.** (Karl Fant, founded 1996) was the canonical NCL commercialization vehicle; listed as defunct on Tracxn. [VERIFIED][36] IP transferred through Camgian Microsystems to Wave Semiconductor Inc. (2014-2015), which subsequently pivoted to machine learning accelerators without shipping an NCL product line. [VERIFIED][37] No evidence of governance/safety silicon based on NCL dual-rail {0,0} at half-Vdd, a hysteretic C-element Epistemic Hold, or any "Goukassian signature"-embedded chip having been fabricated, taped out, or deployed. [HIGH]

**The honest statement: the constitutional hardware floor described in the Atomic Auditability paper is an architectural specification, not a deployed artifact, as of Q2 2026.** [VERIFIED][GAP-ARCHITECTURAL]

### Why the Escrow state cannot be overridden by software

Per the Atomic Auditability paper, the Escrow state is instantiated as the NULL/Spacer encoding at dual-rail {0,0} at half-Vdd. The four-phase handshake protocol is: Phase 1 Data Propagation (DATA encoding, {0,1} or {1,0}), Phase 2 Completion Detection, Phase 3 Spacer Propagation (Escrow entry via {0,0}), Phase 4 Spacer Completion (Escrow exit requiring explicit new data with audit token). [per source]

The hysteretic C-element has three stable states: Escrow {0,0}, Executed {0,1}, Refused {1,0}. Transition to Executed requires `set ∧ audit_valid ∧ ¬reset`. The paper's critical claim is that this is a **state, not a delay.** [per source] Unlike IEX's 350μs fiber delay (software-bypassable via alternative paths), the DITL Escrow physically blocks execution because the downstream stage's completion detector will not fire until the upstream stage produces valid DATA - and valid DATA requires the audit token. There is no software call that can override the physical voltage configuration of a CMOS transistor pair forced to {0,0}; the bypass would require physical probe access to the die. [HIGH]

### The Goukassian Principle in LTL applied to governance

The paper's formalization is: `G(execute → P(escrow_recorded ∧ auditable))`. "No execution signal may propagate unless the system has entered, recorded, and exited a physically enforced Escrow state." [per source]

Applied to TL governance contract execution, the analogous LTL formula is:

`G(execute_upgrade → P(escrow_recorded ∧ custodian_window_closed ∧ no_veto))`

For a governance upgrade to propagate, the hardware must have (1) entered the Escrow state, (2) recorded the Joint-Approval event with the audit token, (3) closed the Custodian review window, and (4) confirmed no veto. Implementing this at hardware level for governance rather than financial pipelines requires the signals "custodian_window_closed" and "no_veto" to be physical inputs to the hysteretic C-element governing upgrade execution, not software states. [NOVEL] This implies a governance-specific hardware module co-located with the protocol's execution environment - currently undesigned and unfabricated. [GAP-ARCHITECTURAL]

### Ghost Governance derived from Atomic Auditability

The Atomic Auditability definition is `Executed(T) → Auditable(T)` with temporal overlap on the same physical commit boundary. Ghost Fills in trading systems are execution-audit mismatches from binary commit semantics. [per source]

**Ghost Governance is the direct analogue: governance actions that execute without corresponding immutable audit evidence.** [NOVEL] At the software layer, a compromised node that processes a governance transaction but manipulates the audit log produces execution without faithful audit. At the DITL hardware layer, Ghost Governance is eliminated by construction: the physical commit boundary is shared between execute and audit - no execute signal propagates unless audit_valid is asserted at the same C-element transition. [HIGH, derived from source]

### Honest residual vulnerabilities from Section VIII of the Atomic Auditability paper

These must be stated without minimization:

1. **C-element hysteresis drift.** Threshold voltage drift from transistor aging (negative bias temperature instability, hot carrier injection), temperature swings, and ionizing radiation can shift the hysteretic switching thresholds over device lifetime. A sufficiently drifted C-element may transition to Executed before audit_valid stabilizes. [per source]

2. **Dual-rail crosstalk.** Wire spacing, fast-swinging adjacent signals, and coupling capacitance can induce false transitions on the dual-rail lines. This is a physical vulnerability to hardware supply-chain adversaries who influence die layout. [per source]

3. **Completion detection metastability.** Near-simultaneous input arrival at completion detectors can induce synchronizer failure with non-zero probability per transition. At scale, this produces low-rate but non-zero false completion events. [per source]

These are real and do not admit software mitigation. They require physical-design countermeasures (guardbanding, layout verification, radiation-hardened processes, synchronizer chains with adequate mean-time-between-failures). The paper is honest that DITL eliminates software-layer Ghost Fills by construction but does not eliminate physical-layer hardware faults.

### The two-layer architecture

Software governance sits above the DITL hardware floor. Software can be upgraded through Joint-Approval; hardware floor cannot be overridden by software-layer actions. **This is the honest division of labor:** [NOVEL]

- Software provides accountability (who proposed, who approved, who dissented), auditability (searchable records, attestations), and coordination (meeting cadence, deliberation workflows).
- Hardware provides enforcement (the Escrow state that no software call can bypass).

Without DITL deployed, the software layer is the only layer, and its guarantees reduce to trust in whoever controls the build toolchain, the deployment key, and the node operators. [HIGH]

---

## 3.6 Transitional governance (pre-DITL deployment)

### The current enforceability gap

In the absence of deployed DITL hardware, the No Log = No Action invariant is bypassable at the software layer by any adversary with root access to the node infrastructure, the build pipeline, or the firmware of the execution hardware. [HIGH] This is not a hypothetical: every production DeFi recovery at scale has relied on this exact bypass path (administrator action), and every governance attack has exploited some variant of it. During the transitional period, constitutional governance is aspirational, not enforceable. [NOVEL]

### Software-layer approximations and their honest characterization

Multi-sig with timelock is the closest software-layer pattern to an Escrow state. Production reference values:

- Compound v2/v3 Timelock: 2-day minimum, 30-day maximum, 14-day grace period. [VERIFIED][3]
- Uniswap: 2-day timelock after 7-day vote. [VERIFIED][5]
- MakerDAO GSM Pause Delay: 48-72 hours historically, raised during crises. [HIGH]
- L2BEAT Stage 2 exit window: ≥30 days. [VERIFIED][11]
- Arbitrum/Optimism Stage 1 Security Council exit: ≥7 days. [VERIFIED][11]

**Per the Atomic Auditability paper's distinction, every one of these is explicitly a speed bump, not an Escrow state.** [per source] A speed bump imposes delay in the primary execution path; it can be bypassed via alternative paths (multisig compromise at ≥75% under L2BEAT's own stated assumption; direct call to a privileged function; upgrade to a new implementation that removes the check). The IEX 350μs fiber delay is the archetype: it added time to one path but did not physically block the action.

An Escrow state, by contrast, physically blocks signal propagation. No alternative path exists because the voltage state of the transistor pair cannot be circumvented by software. **This distinction must be on-chain and in the Governance.md constitutional text, not merely acknowledged externally.** [NOVEL]

### Recommended transitional provisions

1. **On-chain disclosure of reduced enforceability.** Following the L2BEAT Stages Framework's honest-disclosure model, the TL constitution should publish an on-chain attestation of its current maturity stage, explicitly stating that pre-DITL governance is a speed-bump regime, not an Escrow regime. The Optimism "training wheels" language is a direct precedent. [VERIFIED][11]

2. **Minimum 7-day timelock on all rule-encoding transactions** (aligned with L2BEAT Stage 1) with a 30-day timelock for rules affecting the Immutable Mandates (aligned with Stage 2 exit window). [HIGH]

3. **Rule-level circuit-breakers** (per-epoch maximum disbursement; required multi-oracle concurrence on milestone attestations; mandatory dispute window before revocation enforcement per Polkadot's 27-day grace pattern). These are encoded rules, not overrides. [NOVEL]

4. **External attestation via EAS or optimistic oracle** for Joint-Approval payloads, so that post-hoc payload substitution is cryptographically detectable even if not preventable at the software layer.

### Adversary incentives to prevent DITL upgrade

An adversary with established software-layer access loses that access after DITL hardware deployment. This creates a specific incentive structure: **any established software-layer adversary has strong motive to prevent DITL upgrade.** [HIGH] The mechanisms available to such an adversary include (a) influencing Joint-Approval to delay indefinitely, (b) introducing "safer" alternatives that are software-only, (c) attacking the hardware supply chain for DITL components, and (d) capturing the body or bodies that authorize the hardware migration.

Counter-mechanisms compatible with No Switch Off: the constitutional text should (a) explicitly commit to DITL migration as a non-discretionary constitutional objective with specific triggering conditions (e.g., completion of third-party audit of the Atomic Auditability specification), (b) require Joint-Approval on *delays* beyond a published schedule, not only on actions, and (c) publicly enumerate the supply-chain actors involved in DITL fabrication. None of these is a god-mode override; all are rule-level commitments. [NOVEL]

---

## 3.7 Zombie governance - Treasury operation during Layer 1 compromise

### The inverse of No Switch Off

No Switch Off guarantees that the Treasury cannot be halted by an adversary claiming authority. Its inverse: the Treasury cannot be halted by a legitimate party observing a confirmed attack. **Both are consequences of the same absolute mandate.** [HIGH]

### 51% attack quantification

Production 51% attack data points:

- **Bitcoin Gold, May 16-18, 2018:** 388,201 BTG double-spent, approximately $17.8-18.6M. Delisted from Bittrex. [VERIFIED][38]
- **Bitcoin Gold, January 23-24, 2020:** Two deep reorganizations (14-block, 16-block class); approximately 7,167 BTG ($72,000) double-spent. NiceHash rental cost per reorg approximately $1,200. [VERIFIED][39]
- **Ethereum Classic, January 5-7, 2019:** Approximately 88,500 ETC ($1.1M) double-spent. [VERIFIED][40]
- **Ethereum Classic, August 1, 2020:** 3,693-block reorganization. 807,260 ETC double-spent (~$5.6M) plus ~13,000 ETC in mining rewards. Hash rental cost approximately 17.5 BTC (~$192,000). Originated against OKEx. [VERIFIED][41]
- **Ethereum Classic, August 6, 2020:** 4,000-block reorganization; approximately $1.68M additional loss. [VERIFIED][42]
- **Ethereum Classic, August 29, 2020:** ~7,000-block reorganization (two days of history); amount not fully disclosed. [VERIFIED][43]
- **Verge, April 4-9, 2018:** timestamp-bug exploit; 250,000 XVG (~$1.1-1.75M). [VERIFIED][44]
- **Verge, May 22, 2018:** 35M XVG (~$1.7M) over several hours. [VERIFIED][45]
- **Verge, February 15, 2021:** 560,000+ block reorganization - approximately 200 days of history erased; characterized by Coin Metrics as the deepest reorg in any top-100 cryptocurrency. [VERIFIED][46]

Aggregate Ethereum Classic August 2020 losses: approximately $7M across three attacks within one month. [VERIFIED] Academic survey data indicate 85% of successful 51% attacks (2018-2024) targeted chains <3 years old with <$100M market cap. [VERIFIED][47] No major named 51% attack on a production L1 during 2023-2026 was located in public reporting; this is absence of evidence, not confirmed absence.

### Does the Treasury pause during confirmed compromise?

**Under Article VIII No Switch Off, no.** A "pause during compromise" mechanism would be a god-mode override. Even if the pause triggers on a widely-agreed observation (e.g., L2BEAT flags "consensus failure" for the underlying chain), the mechanism itself is authority to halt the Treasury - and once that authority exists, the question of who holds the trigger becomes a god-mode question regardless of framing. This is a [CONSTITUTIONAL TENSION] but it is the intended behavior of the constitution, not a bug. The constitution accepts continued Treasury operation during compromise as the cost of absolute uncompromised autonomy. [HIGH]

### Distinguishing correct operation under adversarial pressure from exploitation

The question is whether cryptographic attestation can distinguish "Treasury operating correctly under adversarial pressure" from "Treasury being exploited during network compromise" without introducing god-mode.

Candidate mechanisms:

- **Proof-of-honest-operation via Merkle proofs**: periodic commitments to the Treasury's state root, cross-posted to multiple chains. An observer comparing commitments across chains can detect state forks. The L2BEAT Data Availability Risk Framework evaluates exactly this pattern. [VERIFIED][48] Detection is not prevention.
- **Cross-chain attestation**: a companion contract on a second L1 posting hashes of TL Treasury state transitions. If the second L1 is also compromised, detection fails; if not, fork detection is robust.
- **MakerDAO's Oracle Security Module (OSM) pattern**: each collateral type has a 1-hour `hop` delay on new price values. `poke()` is permissionless. MKR holders can `stop()` or `void()` queued values if an attack is detected. **No single admin override exists; mitigation is time-delay plus permissionless detection plus permissionless dispute.** [VERIFIED][49] Direct demonstration: March 30, 2024, ETH dropped to ~$1,786 on spot while Maker's OSM system-price remained $1,831.25 for an hour, preventing liquidation cascades.

The MakerDAO OSM pattern is the strongest production precedent for time-delay mitigation of Zombie Governance without god-mode. Applied to TL: every Treasury disbursement could be queued for a publicly-observable window (e.g., 1-24 hours) during which permissionless actors could submit dispute attestations proving L1 compromise; the dispute itself does not pause the Treasury, but it creates public notice, enabling counterparties to refuse receipt of potentially compromised disbursements. [NOVEL]

### Maximum exposure during sustained compromise

Theoretical maximum disbursement exposure during a 30-day L1 compromise window is bounded only by the Treasury's per-epoch disbursement rules, which are set at Joint-Approval time. If annual budget authorization is approximately uniform across the year, 30-day exposure is approximately 1/12 of annual disbursement authority. This is a strong argument for **rule-level per-epoch disbursement caps** being mandatory encoded provisions. [NOVEL][HIGH]

The Ethereum Classic August 2020 data point is instructive: three 51% attacks within one month extracted approximately $7M combined. A Treasury operating during that window with no per-epoch cap could have disbursed orders of magnitude more if milestone-attestation oracles were manipulated during the compromise period.

---

## 3.8 Smart contract treasury verdict

### Condensed core honest tension

Any software can be modified by humans with sufficient access, by advanced machine learning agents with supply-chain reach, or by state-level adversaries. The Treasury's constitutional guarantees written in smart contract code are only as strong as the hardware beneath them. The sole path to genuine enforcement of the Immutable Mandates is DITL hardware, where Epistemic Hold is a physical voltage state at half-Vdd, not a policy commitment. Software governance provides accountability, auditability, and coordination. Hardware governance provides enforcement. Both are necessary. Neither alone is sufficient.

### Consolidated verdict

**Robust:**
- The Treasury's absolute absence of vote rights is constitutionally coherent and architecturally distinctive; no production counter-example of autonomous disbursement without admin key or pause guardian has survived adversarial testing. [HIGH]
- The two-body Joint-Approval structure with no token-weighted voting forecloses the Beanstalk flash-loan attack vector and the Compound Humpy market-accumulation vector, though it introduces a membership-capture vector requiring separate remedies. [HIGH]
- The Goukassian Principle's formalization in LTL plus SystemVerilog provides a mathematically precise specification of the Escrow state that admits formal verification. [VERIFIED per source]

**Fragile:**
- Milestone verification reduces to trust in an oracle, an attester, or a dispute-game of humans. No production system has eliminated this trust. TL must make its trust-relocation explicit at rule-encoding time. [HIGH]
- The Joint-Approval cycle time (plausibly 2-4 weeks by analogy) creates economic denial-of-service exposure via Tribe DAO-style dissolution dynamics. [HIGH]
- The Revocation Contract inherits every known automated-slashing false-positive pattern (Medalla 2020 - 3,000+ events; RockLogic 2023; SSV 2025). Polkadot's 27-day grace period is the direct precedent for the rule-level mitigation; this is not currently specified in Governance.md. [HIGH][GAP-ARCHITECTURAL]
- Zombie Governance during Layer 1 compromise is intentional under No Switch Off. Per-epoch disbursement caps and cross-chain Merkle commitments are the no-god-mode mitigations. [NOVEL]

**Gaps:**
- **[GAP-ARCHITECTURAL]** DITL has no production deployment. Current status is transistor-level simulation, FPGA demonstration, and small research-ASIC stages. Theseus Logic is defunct; IP-successor paths did not produce mainstream NCL silicon. Until DITL fabrication occurs, the constitutional hardware floor is a specification, not an artifact.
- **[GAP-RESEARCH]** No multi-chamber on-chain governance with 75%+75% co-equal supermajorities across two independent bodies has survived adversarial testing in production. Optimism's Token House plus Citizens House is scope-separated; oSnap is a sequential dispute-game. TL's Joint-Approval is novel.
- **[GAP-ARCHITECTURAL]** The Governance.md text does not currently encode rule-level circuit-breakers (per-epoch caps, pre-enforcement delay on revocations, cross-chain attestation for compromise detection) at the granularity implied by the production precedents above.
- **[GAP-CITATION]** The specific Zenodo DOI 10.5281/zenodo.18716142 for the Atomic Auditability paper was not independently corroborated via external search in this research session and should be verified directly via the Zenodo DOI resolver.

### Enforceable guarantees given current DITL deployment status

**Given that DITL is not deployed as of Q2 2026, the Treasury's guarantees are:**
- Enforceable at the software layer against adversaries without root access to the node infrastructure, build pipeline, or firmware.
- Not enforceable against adversaries with supply-chain reach, compiler compromise, or node-operator compromise.
- Auditable in the sense that any violation leaves detectable evidence in on-chain state, provided the audit nodes themselves are not compromised.

**Given that DITL is deployed, the Treasury's guarantees would be:**
- Enforceable at the physical layer against any software-only adversary.
- Enforceable against any adversary without physical die-level access to the hardware.
- Still vulnerable to the residual hardware vulnerabilities in Section VIII of the Atomic Auditability paper (C-element hysteresis drift, dual-rail crosstalk, completion detection metastability).

### Final constitutional integrity assessment

Does autonomous disbursement with no vote rights keep the Treasury within the janitor role, or does control over protocol funding create emergent architectural authority?

The honest answer: **control over funding does create de facto architectural pressure, but the TL design structurally minimizes it.** [HIGH] Because the Treasury has no discretion, cannot alter rules, and executes only what Joint-Approval has encoded, its "authority" is reducible to the authority of the rule-encoders. The architectural authority resides in the Joint-Approval process, not in the Treasury. The Treasury is a fiduciary state machine, not a body.

**This is within the janitor role as specified.** "Governance is the janitor of eternity, not the architect of tomorrow" is preserved: the Treasury cleans up the financial consequences of rules others have written and others have approved. It does not architect.

The constitutional violation risk is not in the Treasury itself. It is in the rule-encoding layer above it. **If rule-encoding insufficiently constrains the Treasury (no per-epoch caps, no pre-enforcement delays on revocations, no circuit-breakers on oracle compromise), the resulting emergent behavior can simulate architectural authority under adversarial conditions.** [NOVEL] The remedy is not pausing the Treasury - that would be a god-mode violation - but rather requiring that every Joint-Approval encoding include specific rule-level safety clauses as a constitutional prerequisite.

The final integrity assessment: **The Smart Contract Treasury is constitutionally sound in design and empirically unprecedented in production. Its enforceability is contingent on DITL hardware deployment. In the transitional period, it is a speed-bump regime that should honestly acknowledge its reduced enforceability on-chain, following the L2BEAT Stages Framework model. Its long-term integrity depends on the quality of rule-encoding by Joint-Approval, which is the actual architectural authority in the system.** [NOVEL]

The Treasury's guarantees are physics when hardware is real, and trust when it is not. The constitution must be written to be honest about which regime it is currently operating in.

---

## Footnotes

[1] MakerDAO Emergency Shutdown Module documentation: docs.makerdao.com/smart-contract-modules/shutdown; github.com/makerdao/esm; July 25, 2024 executive vote raising threshold to 300,000 MKR.

[2] Compound Pause Guardian: docs.compound.finance/governance; github.com/compound-finance/compound-protocol/blob/master/contracts/Comptroller.sol.

[3] Compound Timelock.sol parameters (MINIMUM_DELAY=2d, MAXIMUM_DELAY=30d, GRACE_PERIOD=14d): docs.compound.finance/v2/governance/.

[4] Aave v3 Guardian and Aave Umbrella: aave.com/docs/ecosystem/governance; aave.com/docs/developers/safety-module.

[5] Uniswap Governance process: docs.uniswap.org/concepts/governance/process.

[6] Nouns DAO V3 fork mechanism (August 2023); fork executions September-October 2023: github.com/code-423n4/2023-07-nounsdao; decrypt.co reporting of Fork 1 (472 of 846 Nouns, ~16,757 ETH).

[7] oSnap and UMA Optimistic Oracle v3: blog.uma.xyz/articles/what-is-umas-optimistic-oracle; uma.xyz/osnap. Production users include CoW DAO, Across Protocol, Connext, Gitcoin DAO (98.67% approval), Developer DAO.

[8] Ethereum Attestation Service: attest.org; docs.attest.org; github.com/ethereum-attestation-service/eas-contracts.

[9] UMA Optimistic Oracle v3 liveness and bond parameters: docs.uma.xyz/developers/setting-custom-bond-and-liveness-parameters.

[10] RISC Zero R0VM 1.0 and 2.0; Succinct SP1 ISP1Verifier: risczero.com/blog/hello-zkvm-1-0; docs.succinct.xyz/docs/sp1/verification/solidity-sdk.

[11] L2BEAT Stages Framework (June 2023, last updated July 23, 2025): l2beat.com/stages; original Buterin proposal November 2022 at Ethereum Magicians.

[12] Compound Proposal 289 / Humpy / Golden Boys, July 2024: unchainedcrypto.com/humpy-accused-of-governance-attack-on-compound-finance-dao; blocmates.com/news-posts/compound-governance-attack-whale-agrees-to-revoke-proposal.

[13] Fei Protocol/Tribe DAO: Fei-Fuse reentrancy April 30, 2022, ~$80M; TIP-121 wind-down August 19, 2022: members.delphidigital.io/reports/tribe-volume-and-price-spike-as-fei-protocol-winds-down.

[14] Vitalik Buterin, January 23, 2025: vitalik.eth.limo/general/2025/01/23/l1l2future.html on Stage 1 (Optimism, Arbitrum, Ink) and Stage 2 (DeGate, zk.money, Fuel).

[15] Tornado Cash governance takeover, May 20, 2023: public blockchain records; malicious proposal payload mintad 1.2M votes.

[16] Arbitrum AIP-1, March 2023: foundation pre-allocation controversy.

[17] Beanstalk flash-loan governance attack, April 17, 2022, $182M total impact: bean.money/blog/beanstalk-governance-exploit.

[18] EIP-4844 Dencun upgrade, March 13, 2024: eips.ethereum.org/EIPS/eip-4844.

[19] Reality.eth/Realitio and Zodiac Reality Module: realitio.github.io/docs/html; github.com/gnosisguild/zodiac-module-reality.

[20] Compound Proposal 62-65 COMP distribution bug, September-October 2021: compound.substack.com/p/compound-treasury-updates-comp-bug; cointelegraph.com reporting of Proposal 64 (1.037M COMP unanimous).

[21] Mirror Protocol/Terra collapse, May 2022; Band Protocol oracle support ended August 11, 2022.

[22] Euler Finance hack, March 13, 2023, $197M; attacker returned funds through April 3, 2023: euler.finance/blog/war-peace-behind-the-scenes-of-eulers-240m-exploit-recovery.

[23] RockLogic/Lido slashing, April 13, 2023, 11 validators, ~11.19 ETH penalties: blog.lido.fi/loe-rocklogic-gmbh-slashing-incident; research.lido.fi/t/slashing-incident-involving-rocklogic-gmbh-validators-april-13-2023/4399.

[24] Medalla testnet incident, August 14-19, 2020, 3,000+ slashing events: medium.com/prysmatic-labs/eth2-medalla-testnet-incident-f7fbc3cc934a; blog.ethereum.org/2020/08/21/validated-why-client-diversity-matters.

[25] SSV Network mass slashing, September 10, 2025, 40 validators (Ankr plus Allnodes misconfiguration): ssv.network/blog/slashing-post-mortem-september-2025.

[26] Ethereum Beacon Chain post-Pectra slashing (live May 7, 2025, MIN_SLASHING_PENALTY_QUOTIENT=4096): chorus.one/reports-research/ethereums-pectra-upgrade-slashing-explained; eth2book.info/latest/part2/incentives/slashing.

[27] Cosmos SDK slashing parameters: github.com/cosmos/cosmos-sdk/blob/main/x/slashing/types/params.go.

[28] Polkadot slashing tiers and 27-day grace period: docs.polkadot.com/infrastructure/staking-mechanics/offenses-and-slashes; research.web3.foundation/Polkadot/security/slashing/amounts.

[29] EigenLayer slashing mainnet activation, April 17, 2025, ELIP-002: coindesk.com/tech/2025/04/17/eigenlayer-adds-key-slashing-feature-completing-original-vision.

[30] Mango Markets oracle manipulation, October 11, 2022, Avraham Eisenberg, ~$110-117M: cftc.gov/PressRoom/PressReleases/8647-23; chainalysis.com/blog/oracle-manipulation-attacks-rising.

[31] bZx (February 2020, ~$954K), Cream Finance (October 27, 2021, ~$130M), Inverse Finance (April 2022 $15.6M plus June 2022 $1.26M), Chainalysis 2022 estimate $403.2M across 41 oracle manipulation attacks.

[32] Parameswaran Nair, R.S., MS thesis, Missouri S&T, 2007: scholarsmine.mst.edu/masters_theses/4568.

[33] Smith et al., J. Low Power Electron. Appl. 5(3):183, 2015: mdpi.com/2079-9268/5/3/183.

[34] IEEE, "Design and Analysis of 4-Bit Adder Using DITL," 2020: ieeexplore.ieee.org/document/9007281.

[35] Cole Sherrill, University of Arkansas, 2024: scholarworks.uark.edu/etd/5566.

[36] Theseus Logic Inc. status: tracxn.com/d/companies/theseus-logic.

[37] Camgian to Wave Semiconductor NCL IP transfer, 2014-2015: eetimes.com/startups-try-to-revive-null-convention-logic.

[38] Bitcoin Gold 51% attack, May 2018, 388,201 BTG (~$17.8-18.6M): en.wikipedia.org/wiki/Bitcoin_Gold; ccn.com/bitcoin-gold-hit-by-double-spend-attack-exchanges-lose-millions.

[39] Bitcoin Gold second 51% attack, January 23-24, 2020: James Lovejoy, MIT DCI analysis at gist.github.com/metalicjames/71321570a105940529e709651d0a9765.

[40] Ethereum Classic 51% attack, January 5-7, 2019, ~88,500 ETC (~$1.1M): en.wikipedia.org/wiki/Ethereum_Classic.

[41] Ethereum Classic, August 1, 2020, 807,260 ETC (~$5.6M): bitquery.io/blog/attacker-stole-807k-etc-in-ethereum-classic-51-attack.

[42] Ethereum Classic, August 6, 2020: coindesk.com/tech/2020/08/06/ethereum-classic-suffers-second-51-attack-in-a-week.

[43] Ethereum Classic, August 29, 2020: coindesk.com/markets/2020/08/29/ethereum-classic-hit-by-third-51-attack-in-a-month.

[44] Verge April 2018 attack: dn.institute/research/cyberattacks/incidents/2018-04-04-verge.

[45] Verge May 22, 2018 attack: ccn.com/privacy-coin-verge-succumbs-to-51-attack-again.

[46] Verge February 15, 2021 reorganization: cryptopotato.com/verge-xvg-goes-through-an-attempted-51-attack.

[47] Springer, Complex & Intelligent Systems survey on 51% attacks 2018-2024: link.springer.com/article/10.1007/s40747-026-02256-w.

[48] L2BEAT Data Availability Risk Framework: forum.l2beat.com/t/the-data-availability-risk-framework/318.

[49] MakerDAO Oracle Security Module (1-hour `hop`): docs.makerdao.com/smart-contract-modules/oracle-module/oracle-security-module-osm-detailed-documentation; github.com/makerdao/osm; March 30, 2024 ETH price delay demonstration.
