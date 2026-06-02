# Threshold Calibration and Trigger Mechanisms

**Ternary Logic Framework - Technical Documentation**

---

## Executive Summary

This document explains how the Ternary Logic Framework determines when to trigger the Epistemic Hold (State 0), how confidence thresholds are established through institutional governance, and how the eight architectural pillars work together to create a resilient decision-making system.

**The central principle of threshold governance:**

The TL framework does not ship universal threshold values. There is no number that is correct for all systems. A central bank monetary policy engine, a high-frequency equity trading system, an ESG green bond verifier, and an emergency response coordinator each operate under fundamentally different uncertainty profiles. The same confidence score that justifies Proceed in one domain may require Epistemic Hold in another.

The framework enforces that thresholds exist, are institutionally calibrated, are documented, and are anchored to the governance ledger. What those thresholds are belongs entirely to the governed institution. TLEngine raises a ValueError if instantiated without explicit threshold values. This is intentional.

**Critical Question Answered:** *Who decides trigger levels, how, and when does TL know Decision Logs have hit complexity requiring intervention?*

---

## Table of Contents

1. [Overview of TL States](#overview-of-tl-states)
2. [The Eight Architectural Pillars](#the-eight-architectural-pillars)
3. [Threshold Governance Methods](#threshold-governance-methods)
4. [Composite Confidence Calculation](#composite-confidence-calculation)
5. [Automatic Trigger Mechanisms](#automatic-trigger-mechanisms)
6. [Pillar Integration](#pillar-integration)
7. [Practical Implementation](#practical-implementation)

---

## Overview of TL States

The Ternary Logic Framework operates with three distinct states:

| State | Value | Trigger Condition | Action |
|-------|-------|-------------------|--------|
| **PROCEED** | +1 | Confidence >= proceed_threshold (institution-defined) | Execute transaction |
| **EPISTEMIC_HOLD** | 0 | hold_threshold <= Confidence < proceed_threshold | Pause for deliberation |
| **REFUSE** | -1 | Confidence < hold_threshold (institution-defined) | Reject transaction |

The specific threshold values in this table are blank by design. They are institution-specific governed parameters, not framework constants. See Section 3 for calibration methodology.

**Target Epistemic Hold Rate:** 15-25% of all decisions is optimal for balancing deliberation quality against operational speed. This target should be monitored and reported. Consistent deviation from this range is a signal that thresholds need recalibration, not that the framework is malfunctioning.

---

## The Eight Architectural Pillars

### 1. Epistemic Hold (Pillar I)

**Purpose:** Codifies uncertainty as an active, intelligent pause before execution.

**Mechanism:**
- Triggered when confidence falls below the institution-calibrated proceed_threshold
- Triggered by mandate failures regardless of confidence score
- Analyzes economic confidence, signal conflicts, information completeness
- Creates mandatory, auditable pause for deliberation

**Integration with Thresholds:**
- When confidence falls into the hold zone between hold_threshold and proceed_threshold
- When mandatory verification checks fail (Economic Rights, Sustainable Capital)
- When model conflict exceeds 30% disagreement
- When data is missing, stale (>24 hours), or unverifiable

### 2. Immutable Ledger (Pillar II)

**Purpose:** Creates tamper-evident, chronologically sound record of all transactions.

**Mechanism:**
- Distributed ledger technology with cryptographic hashing
- Each block contains hash of previous block
- Single source of truth for all network participants

**Integration with Thresholds:**
- Records the complete decision process: +1 intent, 0 Hold, final +1 or -1 outcome
- Stores the institution-calibrated threshold values used at time of each decision
- Provides cryptographic proof of when thresholds were crossed
- Enables post-hoc analysis for threshold recalibration with full audit trail

### 3. Goukassian Principle (Pillar III)

**Purpose:** Engineers ethical accountability through decision trace logs during deliberation.

**Mechanism:**
- Creates Decision Logs during Epistemic Hold
- Documents reasoning, alternatives considered, risk assessments
- Cryptographically sealed and immutable

**Integration with Thresholds:**
- Activated automatically when Epistemic Hold is triggered
- Documents why threshold was crossed (data quality issue, model conflict, mandate failure)
- Creates legal evidence for reverse burden of proof
- Enables system designers to prove standard of care

### 4. Decision Logs (Pillar IV)

**Purpose:** Comprehensive audit trails capturing complete context of every material action.

**Mechanism:**
- Records: identities, timestamps, inputs, models, confidence scores, state transitions
- Creates intellectual history for every transaction
- Immutably linked to Immutable Ledger

**Integration with Thresholds:**
- Logs the institution-calibrated threshold values active at decision time
- Records which threshold was crossed and why
- Records all input data used in confidence calculation
- Tracks model outputs and disagreements
- Provides data for backtesting and threshold recalibration over time
- This is how TL knows complexity has been reached: Decision Logs capture all signals that feed into confidence calculation in real time

### 5. Economic Rights and Transparency Mandate (Pillar V)

**Purpose:** Ensures ownership, consent, data provenance, and regulatory access.

**Mechanism (Automatic Trigger):**
```
Checks Required:
- Beneficial ownership verified?
- Consent obtained from all parties?
- Data provenance cryptographically signed?
- Regulatory access granted?

IF ANY CHECK FAILS:
    State = EPISTEMIC_HOLD (forced, confidence = 0.0)
    Log failure reason in Decision Logs
    Create Goukassian Principle trace
    Record on Immutable Ledger
```

**Integration with Thresholds:**
- Overrides confidence-based thresholds entirely
- Even if calculated confidence = 1.0, mandate failure triggers Epistemic Hold
- Binary pass/fail; no gradual confidence score
- Creates audit trail showing which specific check failed

### 6. Sustainable Capital Allocation Mandate (Pillar VI)

**Purpose:** Combat greenwashing with verifiable sustainability credentials.

**Mechanism (Automatic Trigger):**
```
Checks Required:
- ESG data verified by certified third party?
- Emissions report cryptographically anchored?
- Use of proceeds tracked via smart contract?

IF ANY CHECK FAILS:
    State = EPISTEMIC_HOLD (forced, confidence = 0.0)
    Log which sustainability claim failed
    Create verification trace
    Record failure on Immutable Ledger
```

**Integration with Thresholds:**
- Overrides confidence-based thresholds entirely
- Mandatory for green bonds and ESG-linked instruments
- Binary verification; pass or fail
- Prevents execution even with maximum confidence if ESG unverified

### 7. Hybrid Shield (Pillar VII)

**Purpose:** Balance institutional privacy with public transparency.

**Mechanism:**
- Private permissioned layer: confidential transaction details
- Public permissionless layer: cryptographic proofs anchored

**Integration with Thresholds:**
- Threshold decisions recorded on private layer (confidential)
- Cryptographic hash of decision anchored to public layer
- Public can verify integrity without seeing details
- Regulators have permissioned access to full Decision Logs

### 8. Anchors (Pillar VIII)

**Purpose:** Ground the digital system in real-world governance, interoperability, and veracity.

**Types:**
- Governance Anchors: hybrid on/off-chain governance model
- Interoperability Anchors: cross-chain bridges, multi-chain support
- Veracity Anchors: blockchain notarization of real-world evidence

**Integration with Thresholds:**
- Governance Anchors record who set or adjusted thresholds (consortium board, Technical Council) and when
- Threshold modifications require TriCameralApproval per governance specification
- Interoperability Anchors: threshold decisions portable across jurisdictions
- Veracity Anchors: real-world documents (audit reports, regulatory filings) factored into confidence score

---

## Threshold Governance Methods

Thresholds are not arbitrary. They are derived from a combination of five governed inputs. Every deployment must document which methods were used and preserve that documentation in the governance ledger.

### Method 1: Historical Backtesting (Primary)

**Process:**
1. Collect 20+ years of historical decisions and outcomes for your specific domain
2. Test candidate threshold pairs across your actual decision history
3. Simulate decisions using each candidate pair
4. Measure performance metrics: false positives (bad decisions executed), false negatives (good opportunities missed), and total cost
5. Select thresholds that minimize total cost for your domain and risk tolerance

**Example structure (not prescriptive values):**
```
Threshold Pair          | False Positives | False Negatives | Total Cost
proceed=A / hold=B      | ...             | ...             | $...
proceed=C / hold=D      | ...             | ...             | $...  <- your optimum
proceed=E / hold=F      | ...             | ...             | $...
```

The optimum is domain-specific and institution-specific. It cannot be computed from first principles. It requires your data.

**Who decides:** Technical Committee (data scientists, risk managers) proposes thresholds based on backtesting. Governance Anchor (board/consortium/Technical Council) approves. The approved values are anchored to the governance ledger via TriCameralApproval before activation.

### Method 2: Regulatory Requirements (Constraints)

Certain regulatory frameworks impose confidence constraints that function as floor thresholds. Your institution's calibrated thresholds must be equal to or stricter than any applicable regulatory minimum.

**Examples of regulatory constraint structure:**
- Basel III Liquidity Coverage Ratio: defines a minimum confidence level below which a hold or refuse is mandatory
- FATF AML/CFT screening: defines certainty thresholds for clear/review/block determinations
- IOSCO market integrity standards: define manipulation detection sensitivity requirements

**Who decides:** Regulators (BIS, FSB, national central banks, securities commissions) set minimum thresholds. Institutions may use stricter thresholds but not looser. Regulatory floor thresholds are incorporated as constraints in the backtesting process.

### Method 3: Institutional Risk Tolerance (Policy)

**Board-approved risk appetite translated to threshold ranges:**

Different risk postures produce different threshold profiles. The framework does not assign labels to these postures. Your board determines your risk appetite; your Technical Committee translates that appetite into threshold values; the governance body approves.

The relationship is directional, not numerical:
- More conservative posture: higher proceed threshold, higher hold threshold
- More aggressive posture: lower proceed threshold, lower hold threshold
- The specific values depend on your domain, your historical data, and your regulatory constraints

**Who decides:** Board of Directors approves risk appetite. Chief Risk Officer translates into threshold constraints. Technical Committee derives candidate values via backtesting within those constraints. Governance Anchor approves final values.

### Method 4: Market Regime Adaptation (Dynamic)

Thresholds may be adapted dynamically based on pre-approved volatility bands. The activation rules for dynamic adjustment are themselves governed parameters that require board approval and ledger anchoring before deployment.

**Example structure (not prescriptive values):**
```
Regime         | Volatility Indicator Range | Threshold Adjustment
Normal         | Indicator < lower bound    | Base calibrated thresholds
Elevated       | Lower bound <= Indicator   | More conservative thresholds
               | < upper bound              |
Crisis         | Indicator >= upper bound   | Most conservative thresholds
```

The specific volatility indicator, the band boundaries, and the threshold adjustments are all institution-specific governed parameters.

**Who decides:** Automated adjustment based on pre-approved volatility bands. Technical Committee defines bands. Governance body approves activation rules. All dynamic adjustments are logged to the Immutable Ledger with the triggering indicator value.

### Method 5: Mandate Verification (Binary Override)

Mandate verification triggers are not thresholds in the confidence sense. They are binary constitutional checks that override confidence-based state determination entirely.

**Economic Rights and Transparency mandate:** Any verification failure forces Epistemic Hold regardless of confidence score.

**Sustainable Capital Allocation mandate:** Any ESG verification failure forces Epistemic Hold regardless of confidence score.

**Who decides:** These are framework mandates, non-negotiable and not subject to institutional calibration. The checks themselves are defined in the protocol specification. Individual institutions cannot override them.

---

## Composite Confidence Calculation

**How TL knows complexity has been reached:**

The confidence score is calculated from four equally weighted factors (25% each). When any factor scores low, it reduces the composite confidence, potentially triggering Epistemic Hold. Decision Logs capture all four component scores in real time, providing the complete forensic record of why the system determined complexity warranted a pause.

### 1. Data Quality Score (25%)

**Checks:**
- Completeness: all required fields present
- Freshness: data age within acceptable bounds
- Verification: cryptographic signature confirmed
- Source Reputation: historical reliability of data provider

**Formula:**
```python
data_quality = (completeness + freshness + verification + reputation) / 4
```

**Recorded in Decision Logs:**
- Which fields were missing
- Age of each data source
- Which signatures failed verification
- Provider reliability scores

### 2. Model Agreement Score (25%)

**Checks:**
- Consensus: do multiple models agree
- Variance: how much do outputs differ
- Confidence Distribution: are models certain or uncertain

**Formula:**
```python
mean_output = sum(model_outputs) / num_models
variance = sum((output - mean_output)**2 for output in outputs) / num_models
model_agreement = max(0.0, 1.0 - variance)
```

**Recorded in Decision Logs:**
- Output from each model
- Variance calculation
- Which models disagreed and by how much
- If variance exceeds 30%: model conflict triggers automatic Epistemic Hold

### 3. Historical Accuracy Score (25%)

**Checks:**
- Recent performance: model accuracy over last 90 days
- Weighted recency: more recent predictions weighted higher
- Regime stability: has market regime changed

**Recorded in Decision Logs:**
- 90-day accuracy history
- Recent prediction outcomes
- Regime change indicators

### 4. Signal Strength Score (25%)

**Checks:**
- Directional clarity: clear signal or mixed
- Noise level: signal-to-noise ratio
- Indicator alignment: do technical indicators agree

**Recorded in Decision Logs:**
- Each indicator value
- Signal-to-noise calculation
- Which indicators conflicted

### Final Confidence Calculation

```python
confidence = (
    0.25 * data_quality +
    0.25 * model_agreement +
    0.25 * historical_accuracy +
    0.25 * signal_strength
)
confidence = max(0.0, min(1.0, confidence))
```

This composite score is then evaluated against the institution-calibrated thresholds in TLEngine. The calculation itself is domain-agnostic. The thresholds applied to the result are domain-specific and institution-specific.

---

## Automatic Trigger Mechanisms

### Trigger Type 1: Confidence-Based (Continuous)

**Mechanism:**
```python
if confidence >= institution_proceed_threshold:
    state = TLState.PROCEED
elif confidence < institution_hold_threshold:
    state = TLState.REFUSE
else:
    state = TLState.EPISTEMIC_HOLD
```

**Logged in Decision Logs:**
- Exact confidence score
- Institution-calibrated threshold values active at decision time
- Which threshold was crossed
- Component breakdown showing why

### Trigger Type 2: Mandate-Based (Binary Override)

**Mechanism:**
```python
# Check Economic Rights
if not all([ownership_verified, consent_obtained, provenance_signed, regulatory_access]):
    state = TLState.EPISTEMIC_HOLD  # FORCED regardless of confidence
    confidence = 0.0
    reason = f"Economic Rights mandate failed: {failed_checks}"

# Check Sustainable Capital
if not all([esg_verified, emissions_anchored, use_of_proceeds_tracked]):
    state = TLState.EPISTEMIC_HOLD  # FORCED regardless of confidence
    confidence = 0.0
    reason = f"Sustainable Capital mandate failed: {failed_checks}"
```

**Logged in Decision Logs:**
- Which mandate failed
- Which specific checks failed
- Evidence of verification attempts
- Note: even if confidence would be 1.0, mandate failure overrides

### Trigger Type 3: Model Conflict (Threshold-Based)

**Mechanism:**
```python
max_deviation = max(abs(output - mean) for output in model_outputs)
if max_deviation > 0.30:  # 30% disagreement threshold
    state = TLState.EPISTEMIC_HOLD
    reason = "Significant model disagreement detected"
```

**Logged in Decision Logs:**
- Output from each model
- Deviation calculation
- Which models disagreed most

### Trigger Type 4: Data Staleness (Time-Based)

**Mechanism:**
```python
for data_source in data_sources:
    age_hours = (now - data_source.timestamp).total_seconds() / 3600
    if age_hours > 24:
        state = TLState.EPISTEMIC_HOLD
        reason = f"Data source {data_source.name} is {age_hours:.1f} hours old"
        break
```

**Logged in Decision Logs:**
- Age of each data source
- Which source triggered staleness alert
- Last successful update timestamp

---

## Pillar Integration: How They Work Together

### Example Transaction Flow

**Scenario:** Bank wants to approve $10M trade financing for a renewable energy project.

#### Step 1: Initial Intent (+1)
- Transaction submitted to TL system
- Recorded on Immutable Ledger with timestamp
- Decision Logs begin recording

#### Step 2: Mandate Verification (Pillars V and VI)
```python
# Pillar V: Economic Rights and Transparency
ownership_check = verify_beneficial_ownership()    # Pass
consent_check = verify_all_party_consent()         # Pass
provenance_check = verify_data_provenance()        # Pass
regulatory_check = verify_regulator_access()       # Pass

# Pillar VI: Sustainable Capital Allocation
esg_check = verify_esg_data()                      # FAIL - ESG report not verified
emissions_check = verify_emissions_anchor()        # Pass
proceeds_check = verify_smart_contract_track()     # Pass

# RESULT: Sustainable Capital mandate FAILED
# State = EPISTEMIC_HOLD (forced, regardless of any confidence score)
```

**What happens:**
- Pillar I (Epistemic Hold): activated automatically
- Pillar III (Goukassian Principle): creates Decision Log documenting intent, deliberation, options considered, risk assessment
- Pillar IV (Decision Logs): records complete audit trail with all verification results
- Pillar II (Immutable Ledger): writes +1 intent to 0 Hold (ESG failure) to pending resolution
- Pillar VII (Hybrid Shield): private layer records full details; public layer records hash proving Hold occurred
- Pillar VIII (Anchors): Veracity Anchor records ESG verification attempt and failure

#### Step 3: Resolution Process

**Bank obtains verified ESG audit (4 hours later):**

```python
# Re-check Sustainable Capital mandate
esg_check = verify_esg_data()  # Now passes

# All mandates pass. Calculate composite confidence.
data_quality = ...      # institution-specific inputs
model_agreement = ...
historical_accuracy = ...
signal_strength = ...

confidence = calculate_confidence(data_sources, models)

# Engine evaluates against institution-calibrated thresholds
decision = engine.evaluate(confidence, reasoning, metadata)
# If confidence >= institution's proceed_threshold -> PROCEED
```

**What happens:**
- Pillar I: Epistemic Hold resolved with PROCEED or REFUSE depending on confidence vs thresholds
- Pillar III: updates Decision Log with resolution, final decision, justification
- Pillar IV: records complete resolution with Hold duration, resolution action, final state
- Pillar II: writes final entry
- Pillars VII and VIII: updated with resolution record

### Why This Integration Matters

The pillars create a complete evidentiary chain. Every action becomes a complete narrative with intent, justification, verification, and immutable proof:

1. Epistemic Hold (Pillar I) detects complexity and triggers pause
2. Goukassian Principle (Pillar III) documents reasoning and creates accountability
3. Decision Logs (Pillar IV) records everything and enables audit
4. Immutable Ledger (Pillar II) stores permanently and prevents tampering
5. Mandates (Pillars V and VI) enforce standards and ensure compliance
6. Hybrid Shield (Pillar VII) balances privacy and maintains transparency
7. Anchors (Pillar VIII) grounds the record in reality and provides decentralized proof

---

## Practical Implementation

### Code Example: Full Integration

```python
from ternary_logic import TLEngine, TLState, verify_mandate, calculate_confidence

# STEP 1: Establish institutionally calibrated thresholds.
# These values must come from your calibration process.
# Do not use sample values from documentation in production.
# See Section 3 of this document for calibration methodology.
MY_PROCEED_THRESHOLD = YOUR_BACKTESTED_PROCEED_VALUE
MY_HOLD_THRESHOLD = YOUR_BACKTESTED_HOLD_VALUE

engine = TLEngine(
    proceed_threshold=MY_PROCEED_THRESHOLD,
    hold_threshold=MY_HOLD_THRESHOLD,
    epistemic_hold_rate_target=0.20
)

# Transaction data
transaction = {
    'amount': 10_000_000,
    'type': 'trade_financing',

    # Pillar V: Economic Rights data
    'ownership_verified': True,
    'consent_obtained': True,
    'provenance_signed': True,
    'regulatory_access': True,

    # Pillar VI: Sustainable Capital data
    'esg_verified': False,  # Will trigger mandate hold
    'emissions_anchored': True,
    'use_of_proceeds_tracked': True,

    'data_sources': [...],
    'models': [...]
}

# Check Economic Rights mandate (Pillar V)
rights_result = verify_mandate('economic_rights', transaction)
if rights_result.state == TLState.EPISTEMIC_HOLD:
    # Log to Pillars II and IV, create Pillar III trace
    handle_mandate_hold(rights_result)

# Check Sustainable Capital mandate (Pillar VI)
sustainability_result = verify_mandate('sustainable_capital', transaction)
if sustainability_result.state == TLState.EPISTEMIC_HOLD:
    # esg_verified = False triggers this path
    handle_mandate_hold(sustainability_result)

# Calculate composite confidence
confidence = calculate_confidence(
    transaction['data_sources'],
    transaction['models']
)

# Evaluate with TL engine using institution-calibrated thresholds
decision = engine.evaluate(
    confidence=confidence,
    reasoning=f"Trade financing decision",
    metadata=transaction
)

# Act on decision
if decision.state == TLState.PROCEED:
    execute_transaction()
elif decision.state == TLState.EPISTEMIC_HOLD:
    pause_for_review(decision)
else:  # TLState.REFUSE
    reject_transaction(decision)

# Export audit trail
engine.export_audit_trail('/ledger/transaction_audit.json')
```

---

## Summary: Answering the Critical Questions

### Q1: Who decides trigger levels?

1. **Technical Committee** (data scientists, risk managers) proposes thresholds via backtesting against domain-specific historical data
2. **Governance body** (board/consortium/Technical Council) approves institutional risk appetite and threshold values
3. **Regulators** set minimum mandatory thresholds that act as constraints on institutional calibration
4. **Framework protocol** defines non-negotiable mandate triggers that operate independently of confidence thresholds

### Q2: How are thresholds established?

1. **Historical backtesting:** optimize for minimum total cost using domain-specific data
2. **Regulatory constraints:** comply with applicable minimum thresholds
3. **Institutional policy:** board-approved risk tolerance translated to threshold bounds
4. **Market adaptation:** dynamic adjustment within pre-approved volatility bands
5. **Mandate enforcement:** binary pass/fail checks that override all confidence-based determination

There is no universal value appropriate for all systems. The framework ships no defaults.

### Q3: When does TL know Decision Logs have hit complexity?

Decision Logs capture all inputs to confidence calculation in real time:

- **Data Quality Score:** missing, stale, or unverified data logged with specifics
- **Model Agreement Score:** high variance (>30%) logged with disagreement details
- **Historical Accuracy:** recent poor performance logged with prediction outcomes
- **Signal Strength:** mixed or unclear signals logged with indicator conflicts
- **Mandate Failures:** binary check failures logged with specific failed condition

Complexity detection is automatic and real time through continuous monitoring of these factors. When composite confidence falls below the institution-calibrated proceed_threshold or a mandate check fails, Epistemic Hold triggers immediately and the complete evidence record is committed to the Immutable Ledger.

### Q4: How do the eight pillars work together?

1. **Epistemic Hold (I):** detects and enforces pause
2. **Immutable Ledger (II):** records complete transaction history including threshold values at decision time
3. **Goukassian Principle (III):** documents reasoning during pause
4. **Decision Logs (IV):** captures all signals and calculations
5. **Economic Rights (V):** mandates ownership verification (auto-trigger overriding confidence)
6. **Sustainable Capital (VI):** mandates ESG verification (auto-trigger overriding confidence)
7. **Hybrid Shield (VII):** balances privacy with transparency
8. **Anchors (VIII):** provides governance, interoperability, and real-world grounding

Together they create a complete, verifiable, auditable decision chain from intent (+1) through deliberation (0) to outcome (+1 or -1).

---

## Conclusion

The Ternary Logic Framework transforms financial decision-making from binary execution into thoughtful, verifiable, accountable processes. Thresholds are not arbitrary. They are derived from rigorous backtesting, regulatory requirements, and institutional risk tolerance. They are also not universal. The framework's role is to enforce the governance of thresholds, not to prescribe what those thresholds must be.

**The system knows when complexity has been reached because Decision Logs capture every signal in real time.** When confidence falls or mandates fail, Epistemic Hold triggers automatically, creating space for human wisdom in a world of algorithmic speed.

---

**Document Version:** 2.0
**Last Updated:** June 2026
**Created by:** Lev Goukassian (ORCID: 0009-0006-5966-1243)
**Email:** leogouk@gmail.com
**Repository:** https://github.com/FractonicMind/TernaryLogic
**Support:** support@tl-goukassian.org
