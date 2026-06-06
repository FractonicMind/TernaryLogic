## Governance Erosion Prevention Mechanisms for Tri-Cameral TL Framework

### The Threat Model (Adversarial Assumptions)

Before proposing countermeasures, I assume the erosion vector is **asymmetric patience**: a coordinated minority (30-40% of one chamber) acting over 8-12 years, exploiting:
- **Threshold fatigue** — successive 1-2% reductions in supermajority requirements
- **Schema scope creep** — `unevaluatedProperties: false` relaxations that begin as "backward-compatible additions"
- **Emergency precedent** — emergency overrides that expire but leave normative expectations
- **Quorum decay** — gradual absenteeism that lowers effective approval thresholds

---

## Mechanism 1: Constitutional Ratchet on Threshold Changes

**Problem:** Thresholds can be lowered incrementally (66% → 64% → 62%) without any single change triggering alarm.

**Solution:** Any vote that reduces a governance threshold (supermajority requirement, veto power, quorum minimum) must **simultaneously reduce the maximum allowable term length** for all sitting members of both chambers by the same proportion.

*Example:* Reducing the amendment threshold from 66% to 64% (a 3% relative reduction) triggers a 3% reduction in maximum consecutive terms: 9 years → 8.73 years (rounded down to 8 years, 8 months). This forces immediate, personal cost on the voters who benefit from the relaxation.

**Adversarial test:** A rational voter who expects to remain in power will hesitate to degrade their own term limits. A voter planning to exit will still face reputational cost (the public record of "voted for term reduction").

**Implementation:** Enforced at Layer 5 (on-chain). `TL_Ledger_Core.proposeThresholdChange` calculates the ratchet and reverts if the encoded term reduction is not present in the same transaction.

---

## Mechanism 2: Schema Version Fossilization with Sunset Clauses

**Problem:** Schema versions can be relaxed gradually — adding optional fields, then making them conditionally required, then removing `unevaluatedProperties: false` in isolated patches.

**Solution:** Every schema version must declare a **constitutionally frozen subset** of properties that cannot be removed, made optional, or conditionally bypassed in any future version. This subset is anchored as a Merkle root at version creation.

For `StateEnvelope_v1_0_0`, the frozen subset is:
- `currentState` enum `[-1, 0, 1]` (no additional states, no renaming)
- `permissionToken` required when `currentState == 1`
- `laneOrigin: "GOVERNANCE_LANE"` on PermissionToken

**Sunset clause addition:** Any schema version that relaxes a frozen property automatically expires 180 days after activation, returning all endpoints to the prior frozen version. This is not a vote; it is a **constitutional circuit breaker** encoded in the Gateway's `GET /gateway/status` fail-closed logic.

**Adversarial test:** A hostile amendment that passes all three chambers still faces automatic reversion after 180 days unless the frozen subset itself is modified — which requires a **constitutional change** (75% both chambers + 90-day comment period).

---

## Mechanism 3: Epistemic Hold Escalation Memory

**Problem:** Emergency overrides (Pillar VII, Section IX.3) are logged but not **aggregated**. After 50 legitimate emergencies, the 51st becomes "normalized" and faces less scrutiny.

**Solution:** The Lantern (`GET /epistemic-hold/lantern`) must expose a **cumulative erosion score**:

```
erosionScore = Σ(overrideCount_last_5_years × overrideSeverity) / (pillarComplianceAge_months)
```

When `erosionScore > 0.15`, the Lantern's `compliancePosture` shifts from `EPISTEMIC_HOLD_ACTIVE` to `CONSTITUTIONAL_DRIFT_WARNING`. At `> 0.30`, the Gateway enters **mandatory escalation mode**: any emergency override request automatically triggers a 72-hour public notice period before execution, regardless of Tri-Cameral approval.

**Adversarial test:** Score cannot be gamed by "minor" overrides because severity is weighted by the override's stated justification length (min 100 chars from `EmergencyOverrideRequest.justification`). Short justifications increase severity; long justifications are subject to NLP drift detection (change in vocabulary from historical patterns).

**Implementation:** `GET /metrics/summary` includes `erosionScore` field. Webhook `constitutionalDrift.warning` fires when score crosses 0.15.

---

## Mechanism 4: Negative Option Voting on Quorum Changes

**Problem:** Quorum decay (absenteeism) effectively reduces thresholds without any vote. A chamber that should have 9 members voting only receives 7; 66% of 7 is easier than 66% of 9.

**Solution:** Quorum is **dynamically adjusted upward** to compensate for absenteeism. The effective quorum is:

```
effectiveQuorum = constitutionalQuorum × (1 + absenteeRate_last_4_quarters)
```

If a 9-member chamber averages 2 absences per vote (22% absentee rate), the effective quorum becomes `9 × 1.22 = 11 members required` — impossible to achieve. This forces attendance or formal resignation.

**Negative option addition:** Any member who misses 3 consecutive votes without a pre-filed `GovernanceProof` (attesting to a verified external constraint) is automatically considered to have **voted against** the next 5 proposals. Their absence becomes a binding veto.

**Adversarial test:** A coordinated absentee campaign intended to lower thresholds instead produces automatic vetoes. The only escape is formal resignation (triggering a replacement election) or pre-filed attestation (which is itself logged and auditable).

---

## Mechanism 5: Hysteresis Bands on Regulatory Context Drift

**Problem:** `RegulatoryContext` fields (Basel III LCR ≥ 1.0, NSFR ≥ 1.0) can be reinterpreted gradually — "1.0 means approximately 1.0" → "0.98 is acceptable with variance" → "0.95 in exceptional circumstances."

**Solution:** Enforce **hysteresis bands** at the ABI layer. `ITL_Validator.verifyEconomicRightsCompliance` must use a stateful comparator:

```
If lcr < 1.0:
    if lcr >= 0.98 and previous_lcr >= 1.0 and days_since_first_breach < 30:
        allow Epistemic Hold (State 0)
    else:
        Refuse (State -1)
```

A single breach below 1.0 triggers Epistemic Hold for 30 days, giving time for correction. A second breach within 90 days, or any breach below 0.98, triggers automatic Refuse with `refusalIsPermanent: true`.

**Adversarial test:** This prevents "slippery slope" regulatory erosion. The first breach is a warning; the second is permanent refusal. No committee can vote away a permanent refusal — it requires a constitutional change with 75% approval and 90-day comment.

**Implementation:** The `windowComparatorReading` field in `EscrowRecord` stores the hysteresis state (last known compliant value, breach count, cooldown remaining).

---

## Mechanism 6: Succession Declaration as Poison Pill

**Problem:** An eroded future governance body could simply ignore the Succession Declaration (`SuccessionDeclaration_v1_0_0`) or amend it out of existence.

**Solution:** The Succession Declaration includes a **cryptographic poison pill**: a pre-signed transaction that, if not renewed every 365 days, automatically transfers all `TL_Ledger_Core` admin capabilities to a **hard-coded emergency DAO** with a 10-year immutable charter.

The poison pill is anchored at Layer 8 (Pillar VIII) and embedded in the Genesis block of the ledger. Renewal requires a unanimous vote of all 20 members (Technical Council + Stewardship Custodians) and a Merkle proof of renewal anchored on-chain.

**Adversarial test:** An eroded body that wishes to ignore the Succession Declaration must either renew it (requiring unanimous consent — impossible if any dissenter remains) or allow the poison pill to trigger. The emergency DAO's charter explicitly forbids threshold reductions, schema relaxation, or emergency override normalization.

---

## Mechanism 7: Shadow Chamber with Retroactive Veto

**Problem:** All the above mechanisms are prospective. What detects erosion **after it has happened**?

**Solution:** A **Shadow Chamber** — 3 randomly selected former members (disqualified by term limits, cool-down periods, or voluntary exit) who hold no operational authority but possess **retroactive veto power** for 24 months after their departure.

The Shadow Chamber's authority:
- Can nullify any governance decision made in the 12 months preceding their departure if 2 of 3 agree that the decision constitutes "constitutional drift" (defined as: a change that would not have passed under the rules in effect 36 months prior)
- Nullification triggers automatic restoration of the prior state (schema version, threshold, or regulatory interpretation) and logs a `ConstitutionalDriftDetected` event
- Shadow Chamber members are bound by the same NL=NA logging requirements and must provide a `GovernanceProof` for their veto

**Adversarial test:** The Shadow Chamber cannot be captured because its members are randomly selected from the pool of **former** members who are legally barred from holding office again. Their incentive is reputational (historical vindication) rather than current power.

**Implementation:** `GET /governance/shadow-chamber/status` endpoint (not yet in `tl_openapi.yaml` — requires new endpoint) returns current Shadow Chamber roster and pending veto windows.

---

## Summary Table: Erosion Vectors vs. Mechanisms

| Erosion Vector | Mechanism | Enforcement Layer | Adversary Cost |
|---|---|---|---|
| Threshold creep (66% → 64%) | Constitutional Ratchet (term limits reduction) | Layer 5 (on-chain revert) | Personal term loss |
| Schema relaxation | Fossilization + Sunset Clause | Layer 1 (JSON Schema) + Gateway fail-closed | Automatic reversion after 180 days |
| Emergency normalization | Erosion Score + Lantern warning | Layer 3 (TGLF log) + Webhook | Public signaling + mandatory 72-hour delay |
| Quorum decay | Dynamic quorum + negative option | Layer 2 (PermissionToken lane validation) | Absence = veto |
| Regulatory reinterpretation (LCR drift) | Hysteresis bands | Layer 5 (ABI revert) | Permanent refusal after second breach |
| Succession Declaration nullification | Poison pill + unanimous renewal | Layer 8 (Merkle anchor) | Full admin transfer to emergency DAO |
| Post-hoc detection | Shadow Chamber retroactive veto | New endpoint (Layer 4 cross-reference) | 24-month window; 2/3 vote by disqualified former members |

---

**Constitutional note:** None of these mechanisms require trust in human judgment. Each is enforced at the schema, ABI, or Gateway layer with explicit revert conditions. The most adversarial scenario — a unanimous Tri-Cameral vote to disable all seven mechanisms — would itself constitute a constitutional change requiring 75% approval and 90-day public comment, during which the Shadow Chamber could exercise retroactive veto.
