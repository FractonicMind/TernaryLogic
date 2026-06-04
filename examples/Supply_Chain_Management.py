"""
Ternary Logic Framework: Supply Chain Management
=================================================

Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com
Successor: support@tl-goukassian.org
Repository: https://github.com/FractonicMind/TernaryLogic

DOI 1: 10.1007/s43681-025-00910-6, Auditable AI: Tracing the Ethical History of a Model
DOI 2: 10.1007/s43681-026-01124-0, A Ternary Logic Framework for Institutional Governance

The Goukassian Vow:
    "Pause when truth is uncertain"  ->  State  0  (Epistemic Hold)
    "Refuse when harm is clear"      ->  State -1  (Refuse)
    "Proceed where truth is"         ->  State +1  (Proceed)

The Epistemic Hold prevents supply chain overreactions.

This example demonstrates TL applied to global supply chain management:
    - Disruption severity and duration assessment
    - Alternative route viability analysis
    - Inventory buffer evaluation (Solvency Protocol analog)
    - ESG mandate verification: no rerouting to non-compliant suppliers
    - Labor rights and sanctions screening (Pillar V)
    - Graduated response via Epistemic Hold vs immediate reroute
    - NL=NA write-before-act for every supply chain decision

THRESHOLD GOVERNANCE:
    Supply chain thresholds must be calibrated per industry, commodity,
    margin profile, and regulatory exposure. A pharmaceutical supply chain
    and a consumer electronics chain have fundamentally different uncertainty
    tolerances. No universal values exist.
    See docs/Threshold_Calibration.md.

WHY EPISTEMIC HOLD MATTERS IN SUPPLY CHAINS:
    Unlike financial trading where positions can be reversed in milliseconds,
    supply chain rerouting commits physical resources: shipping containers,
    warehouse space, customs filings, and supplier contracts. An incorrect
    reroute decision costs weeks and millions. The Epistemic Hold is not
    indecision. It is constitutional recognition that irreversible commitments
    demand verified truth before execution.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import numpy as np

# TL Framework imports
from ternary_logic import TLEngine, TLState, TLValue, verify_mandate


# =============================================================================
# SECTION 1: Governance Artifacts (consistent pattern)
# =============================================================================

def create_goukassian_principle_block(
    decision_payload: str,
    agent_id: str,
    license_scopes: list
) -> Dict[str, Any]:
    """Three Goukassian Principle artifacts. See Quickstart_Example.py."""
    payload_bytes = decision_payload.encode("utf-8")
    return {
        "lantern": {
            "artifactName": "lantern",
            "lanternHash": hashlib.sha256(payload_bytes).hexdigest()
        },
        "signature": {
            "artifactName": "signature",
            "agentSignature": hashlib.sha512(
                (agent_id + decision_payload).encode("utf-8")
            ).hexdigest()
        },
        "license": {
            "artifactName": "license",
            "licenseScope": license_scopes
        }
    }


def commit_log_entry(
    decision: TLValue,
    engine: TLEngine,
    goukassian_block: Dict[str, Any],
    previous_hash: str,
    extra_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Commit governance log entry. NL=NA: BEFORE any rerouting fires."""
    log_id = str(uuid.uuid4())
    committed_at = datetime.now(timezone.utc).isoformat()

    canonical = json.dumps({
        "logId": log_id,
        "state": decision.state.name,
        "stateValue": decision.state.value,
        "confidence": decision.confidence,
        "reasoning": decision.reasoning,
        "committedAt": committed_at
    }, sort_keys=True)

    log_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    merkle_root = hashlib.sha256(
        (previous_hash + log_hash).encode("utf-8")
    ).hexdigest()

    entry = {
        "logId": log_id,
        "currentState": decision.state.value,
        "stateLabel": decision.state.name,
        "processActive": {
            TLState.PROCEED: "ProceedAuthorized",
            TLState.EPISTEMIC_HOLD: "GovernancePause",
            TLState.REFUSE: "RefusalPermanent"
        }[decision.state],
        "confidence": decision.confidence,
        "reasoning": decision.reasoning,
        "logHash": log_hash,
        "merkleRoot": merkle_root,
        "previousHash": previous_hash,
        "committedAt": committed_at,
        "goukassianPrinciple": goukassian_block,
        "pufAttestation": "NULL_PUF_DEPLOYMENT",
        "architectureMode": "ARCHITECTURE_B",
        "engineConfig": {
            "proceedThreshold": engine.proceed_threshold,
            "holdThreshold": engine.hold_threshold
        }
    }
    if extra_context:
        entry["domainContext"] = extra_context
    return entry


def build_permission_token(log_entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """PermissionToken for PROCEED. laneOrigin const GOVERNANCE_LANE. NL=NA Layer 2."""
    if log_entry["currentState"] != TLState.PROCEED.value:
        return None

    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(milliseconds=300000)

    return {
        "tokenId": str(uuid.uuid4()),
        "logHash": log_entry["logHash"],
        "merkleRoot": log_entry["merkleRoot"],
        "laneOrigin": "GOVERNANCE_LANE",  # NL=NA Layer 2 const
        "issuedAt": issued_at.isoformat(),
        "expiresAt": expires_at.isoformat(),
        "maxLifetimeMs": 300000,
        "revocationStatus": "ACTIVE",
        "signerKeyId": "supply-chain-hsm-001",
        "epochTimestamp": int(issued_at.timestamp()),
        "signatureValue": hashlib.sha256(
            log_entry["logHash"].encode()
        ).hexdigest()
    }


class ImmutableLedger:
    """Pillar II: append-only hash chain. See Quickstart_Example.py."""

    def __init__(self):
        self._entries = []
        self._genesis_hash = hashlib.sha256(
            b"TL_SUPPLY_CHAIN_GENESIS"
        ).hexdigest()

    @property
    def previous_hash(self) -> str:
        return (
            self._entries[-1]["merkleRoot"]
            if self._entries else self._genesis_hash
        )

    def commit(self, entry: Dict[str, Any]) -> str:
        self._entries.append(entry)
        return entry["logHash"]

    @property
    def size(self) -> int:
        return len(self._entries)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "totalEntries": self.size,
            "latestMerkleRoot": self.previous_hash,
            "states": {
                "PROCEED": sum(
                    1 for e in self._entries if e["currentState"] == 1
                ),
                "EPISTEMIC_HOLD": sum(
                    1 for e in self._entries if e["currentState"] == 0
                ),
                "REFUSE": sum(
                    1 for e in self._entries if e["currentState"] == -1
                )
            }
        }


# =============================================================================
# SECTION 2: Supply Chain Signal Analysis
# =============================================================================

class DisruptionAnalyzer:
    """
    Analyze supply chain disruption signals.

    Supply chain signals differ from financial signals in one important way:
    they are often one-directional. A disruption signal of 0.9 (severe) does
    not become a buy signal when inverted. It means the current route is
    compromised. The question is whether the alternative is viable enough
    to commit to, not whether the disruption is real.

    Each signal returns a value in [0.0, 1.0] representing confidence that
    the proposed response (reroute, hold, maintain) is correct. Lower values
    indicate more uncertainty. Zero indicates data absence.
    """

    def assess_disruption_severity(
        self, severity_reports: List[Dict[str, Any]]
    ) -> Optional[float]:
        """
        Assess disruption severity from multiple source reports.

        High agreement on severity = higher confidence in the signal.
        Low agreement = uncertainty = lower confidence = Epistemic Hold.

        Returns confidence in the severity assessment [0.0, 1.0].
        """
        if not severity_reports:
            return None

        scores = [r.get("severity", 0.5) for r in severity_reports]
        if not scores:
            return None

        mean_severity = float(np.mean(scores))
        # Agreement: lower variance = higher confidence in the assessment
        variance = float(np.var(scores)) if len(scores) > 1 else 0.0
        agreement_confidence = max(0.0, 1.0 - variance * 4)

        # For rerouting: high severity with high agreement = PROCEED to reroute
        # High severity with low agreement = Epistemic Hold
        return float(np.clip(mean_severity * agreement_confidence, 0, 1))

    def assess_duration_confidence(
        self, duration_estimates: List[Dict[str, Any]]
    ) -> Optional[float]:
        """
        Assess confidence in disruption duration estimates.

        Wide spread in duration estimates = high uncertainty.
        Low confidence justifies Epistemic Hold over immediate rerouting.
        """
        if not duration_estimates:
            return None

        estimates = [e.get("days", 0) for e in duration_estimates if "days" in e]
        if not estimates:
            return None

        if len(estimates) == 1:
            return 0.6  # Single source: moderate confidence

        mean_days = float(np.mean(estimates))
        std_days = float(np.std(estimates))

        if mean_days == 0:
            return 0.5

        cv = std_days / mean_days  # Coefficient of variation
        # Low CV = consistent estimates = high confidence
        return float(np.clip(1.0 - cv, 0.1, 1.0))

    def assess_route_viability(
        self,
        alternative_routes: List[Dict[str, Any]],
        cost_comparisons: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[float]:
        """
        Assess viability of alternative routes.

        Combines reliability scores, capacity, and cost factors.
        No viable alternative = signal toward Epistemic Hold or Refuse.
        """
        if not alternative_routes:
            return 0.0  # No alternatives: low confidence in rerouting

        viable = [
            r for r in alternative_routes
            if r.get("capacity_available", 0) > 0.3
            and r.get("reliability_score", 0) > 0.5
        ]

        if not viable:
            return 0.1  # Alternatives exist but none viable

        best_reliability = max(
            r.get("reliability_score", 0) for r in viable
        )
        best_capacity = max(
            r.get("capacity_available", 0) for r in viable
        )

        base_score = (best_reliability * 0.6) + (best_capacity * 0.4)

        # Cost penalty: expensive rerouting reduces decision confidence
        if cost_comparisons:
            cost_ratios = [
                c.get("alternative_cost_ratio", 1.0) for c in cost_comparisons
            ]
            if cost_ratios:
                min_ratio = min(cost_ratios)
                if min_ratio > 2.0:
                    base_score *= 0.7  # More than 2x cost reduces confidence
                elif min_ratio > 1.5:
                    base_score *= 0.85

        return float(np.clip(base_score, 0, 1))

    def assess_inventory_buffer(
        self,
        current_inventory: Dict[str, float],
        demand_forecast: Optional[Dict[str, float]] = None
    ) -> Optional[float]:
        """
        Assess inventory buffer adequacy.

        This is the Solvency Protocol analog for supply chains:
        just as a financial system pauses when reserves are unclear,
        a supply chain pauses when inventory coverage is uncertain.

        Low inventory with uncertain forecast = Epistemic Hold.
        Low inventory with clear forecast = Refuse (do not reroute yet,
        immediate action on current route required).
        Adequate inventory = time to evaluate alternatives properly.
        """
        if not current_inventory:
            return None

        # Days of coverage per SKU
        coverage_days = []
        for sku, qty in current_inventory.items():
            if demand_forecast and sku in demand_forecast:
                daily_demand = demand_forecast[sku] / 30
                if daily_demand > 0:
                    coverage_days.append(qty / daily_demand)
                else:
                    coverage_days.append(90.0)  # No demand: ample coverage
            else:
                # No forecast: moderate confidence
                coverage_days.append(14.0)

        if not coverage_days:
            return None

        avg_coverage = float(np.mean(coverage_days))
        min_coverage = float(np.min(coverage_days))

        # Scale: 30+ days coverage = full confidence to deliberate
        # Under 7 days = urgency increases, reduces deliberation confidence
        coverage_score = min(avg_coverage / 30.0, 1.0)
        urgency_penalty = max(0.0, (7.0 - min_coverage) / 7.0) * 0.4

        return float(np.clip(coverage_score - urgency_penalty, 0, 1))

    def assess_supplier_flexibility(
        self, supplier_network: Dict[str, Any]
    ) -> Optional[float]:
        """
        Assess alternative supplier availability and qualification.

        Pre-qualified suppliers with available capacity score higher.
        Unqualified or capacity-constrained suppliers reduce confidence.
        """
        if not supplier_network:
            return None

        qualified = supplier_network.get("qualified_alternatives", 0)
        total = supplier_network.get("total_alternatives", 0)
        onboarding_weeks = supplier_network.get("avg_onboarding_weeks", 12)
        capacity_utilization = supplier_network.get("avg_utilization", 0.8)

        if total == 0:
            return 0.0

        qualification_ratio = qualified / total
        capacity_signal = 1.0 - capacity_utilization
        onboarding_penalty = min(onboarding_weeks / 16.0, 0.5)

        score = (
            qualification_ratio * 0.5
            + capacity_signal * 0.3
            - onboarding_penalty * 0.2
        )
        return float(np.clip(score, 0, 1))

    def assess_customer_impact(
        self,
        customer_commitments: List[Dict[str, Any]],
        disruption_timeline: Optional[Dict[str, Any]] = None
    ) -> Optional[float]:
        """
        Assess customer impact urgency.

        Critical commitments with near deadlines score lower confidence
        in the Epistemic Hold option: urgency may require faster action
        even under uncertainty.
        """
        if not customer_commitments:
            return 0.5  # No commitments: no urgency signal

        now = datetime.now(timezone.utc)
        critical_within_days = []

        for commitment in customer_commitments:
            deadline_str = commitment.get("deadline")
            criticality = commitment.get("criticality", "medium")
            if deadline_str and criticality == "critical":
                try:
                    deadline = datetime.fromisoformat(
                        deadline_str.replace("Z", "+00:00")
                    )
                    days_until = (deadline - now).days
                    critical_within_days.append(days_until)
                except (ValueError, TypeError):
                    pass

        if not critical_within_days:
            return 0.7  # No critical near-term: more time to deliberate

        min_days = min(critical_within_days)
        if min_days <= 3:
            return 0.2  # Critical deadline imminent: low confidence in holding
        elif min_days <= 7:
            return 0.4
        elif min_days <= 14:
            return 0.6
        else:
            return 0.8

    def assess_sustainability_compliance(
        self, sustainability_metrics: Dict[str, Any]
    ) -> Optional[float]:
        """
        Pillar VI: Assess sustainability of proposed alternative route.

        Returns a graded signal. Full mandate verification via
        verify_mandate() is binary and overrides this signal entirely.
        """
        if not sustainability_metrics:
            return None

        carbon_score = sustainability_metrics.get("carbon_intensity_score", 50) / 100
        labor_rights = sustainability_metrics.get("labor_rights_score", 50) / 100
        certifications = sustainability_metrics.get("certification_count", 0)

        cert_bonus = min(certifications / 5.0, 0.2)
        composite = (
            carbon_score * 0.4
            + labor_rights * 0.4
            + cert_bonus
        )
        return float(np.clip(composite, 0, 1))

    def analyze_all(
        self,
        disruption_event: Dict[str, Any],
        route_info: Dict[str, Any],
        market_conditions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run all signal analyses. Returns dict of signals."""
        signals = {}

        if "severity_reports" in disruption_event:
            signals["disruption_severity"] = self.assess_disruption_severity(
                disruption_event["severity_reports"]
            )

        if "duration_estimates" in disruption_event:
            signals["duration_confidence"] = self.assess_duration_confidence(
                disruption_event["duration_estimates"]
            )

        if "alternative_routes" in route_info:
            signals["route_viability"] = self.assess_route_viability(
                route_info["alternative_routes"],
                route_info.get("cost_comparisons")
            )

        if "current_inventory" in market_conditions:
            signals["inventory_buffer"] = self.assess_inventory_buffer(
                market_conditions["current_inventory"],
                market_conditions.get("demand_forecast")
            )

        if "supplier_network" in route_info:
            signals["supplier_flexibility"] = self.assess_supplier_flexibility(
                route_info["supplier_network"]
            )

        if "customer_commitments" in market_conditions:
            signals["customer_urgency"] = self.assess_customer_impact(
                market_conditions["customer_commitments"],
                disruption_event.get("timeline")
            )

        if "sustainability_metrics" in market_conditions:
            signals["sustainability"] = self.assess_sustainability_compliance(
                market_conditions["sustainability_metrics"]
            )

        return signals


# =============================================================================
# SECTION 3: Supply Chain Compliance (Pillars V and VI)
# =============================================================================

def check_supply_chain_compliance(
    disruption_event: Dict[str, Any],
    route_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Pillar V: Supply chain compliance checks.

    Covers FATF sanctions screening on alternative suppliers,
    labor rights violations (ILO conventions), and export controls.
    Any FATAL flag forces Refuse (-1).
    """
    failures = []
    warnings = []

    # Sanctions screening on proposed alternative suppliers
    if not disruption_event.get("alternative_suppliers_screened", False):
        failures.append("FATF: Alternative suppliers not sanctions-screened")

    # Labor rights: ILO conventions
    labor_violations = route_info.get("labor_violations_detected", False)
    if labor_violations:
        failures.append(
            "Pillar V: Labor rights violations detected on alternative route"
        )

    # Export controls
    restricted_goods = disruption_event.get("restricted_goods_involved", False)
    if restricted_goods and not disruption_event.get("export_license_verified", False):
        failures.append(
            "Pillar V: Export controls apply; license verification required"
        )

    # Child labor risk
    child_labor_risk = route_info.get("child_labor_risk_score", 0)
    if child_labor_risk > 0.6:
        failures.append(
            f"Pillar V: High child labor risk score "
            f"{child_labor_risk:.2f} on alternative route"
        )
    elif child_labor_risk > 0.3:
        warnings.append(
            f"Pillar V: Moderate child labor risk {child_labor_risk:.2f}; "
            "enhanced due diligence required"
        )

    return {
        "compliant": len(failures) == 0,
        "failures": failures,
        "warnings": warnings
    }


# =============================================================================
# SECTION 4: Supply Chain Response Engine
# =============================================================================

class GlobalSupplyChainManager:
    """
    Global Supply Chain Management using Ternary Logic.

    Implements sovereign-grade accountability for supply chain decisions:
        Pillar I:   Epistemic Hold (conflicting disruption reports, data gaps)
        Pillar II:  Immutable Ledger (every decision committed before rerouting)
        Pillar III: Goukassian Principle (lantern, signature, license)
        Pillar IV:  Decision Logs (complete audit trail)
        Pillar V:   Labor rights, sanctions, export controls
        Pillar VI:  ESG mandate verification on alternative routes
        Pillar VII: Hybrid Shield (privacy-preserving transparency)
        Pillar VIII:Anchors (Merkle root anchoring, RFC 3161 timestamps)

    The Epistemic Hold prevents supply chain overreactions.
    Rerouting is irreversible: containers move, contracts commit,
    customs filings trigger obligations. Wrong reroutes cost weeks
    and millions. Epistemic Hold is the constitutional mechanism for
    ensuring that irreversible commitments demand verified truth.

    The Solvency Protocol analog:
    Just as a financial system pauses when reserves are unclear,
    a supply chain pauses when inventory coverage is uncertain.
    The inventory_buffer signal is the reserve adequacy measure.

    THRESHOLD GOVERNANCE:
        proceed_threshold and hold_threshold must be calibrated per
        industry, commodity class, and regulatory exposure.
        See docs/Threshold_Calibration.md.
    """

    def __init__(
        self,
        proceed_threshold: float,
        hold_threshold: float,
        cost_sensitivity: float = 0.3,
        time_sensitivity: float = 0.4
    ):
        """
        Initialize Supply Chain Manager.

        Args:
            proceed_threshold: Institution-calibrated PROCEED threshold.
                               REQUIRED. No default.
            hold_threshold:    Institution-calibrated REFUSE threshold.
                               REQUIRED. No default.
            cost_sensitivity:  Weight given to cost signals [0-1].
            time_sensitivity:  Weight given to time/urgency signals [0-1].
        """
        self.engine = TLEngine(
            proceed_threshold=proceed_threshold,
            hold_threshold=hold_threshold,
            epistemic_hold_rate_target=0.25
        )
        self.analyzer = DisruptionAnalyzer()
        self.cost_sensitivity = cost_sensitivity
        self.time_sensitivity = time_sensitivity
        self.ledger = ImmutableLedger()
        self.license_scopes = [
            "supply_chain.rerouting",
            "regulatory.compliance",
            "audit.governance"
        ]
        self._decisions = []

    def make_supply_chain_decision(
        self,
        disruption_event: Dict[str, Any],
        route_info: Dict[str, Any],
        market_conditions: Dict[str, Any],
        scenario_label: str = "Supply Chain Decision"
    ) -> Dict[str, Any]:
        """
        Make a supply chain response decision under TL governance.

        Sequence (respecting NL=NA):
            1. Analyze disruption signals
            2. ESG mandate check (Pillar VI): binary, overrides confidence
            3. Compliance check (Pillar V): binary, may force Refuse
            4. Calculate composite confidence
            5. Evaluate with TLEngine
            6. Commit log entry (NL=NA: BEFORE any rerouting fires)
            7. Issue PermissionToken if PROCEED
            8. Return governance record with response plan

        The irreversibility of rerouting means the Epistemic Hold threshold
        is set deliberately higher than in reversible domains. Pausing to
        gather more data costs less than committing to a wrong route.
        """
        # Step 1: Analyze signals
        signals = self.analyzer.analyze_all(
            disruption_event, route_info, market_conditions
        )

        # Step 2: ESG mandate check on the alternative route (Pillar VI)
        sustainability_data = {
            "esg_verified": market_conditions.get("esg_verified", False),
            "emissions_anchored": market_conditions.get(
                "emissions_anchored", False
            ),
            "use_of_proceeds_tracked": market_conditions.get(
                "use_of_proceeds_tracked", True
            )
        }
        esg_result = verify_mandate("sustainable_capital", sustainability_data)
        esg_blocked = esg_result.state == TLState.EPISTEMIC_HOLD

        # Step 3: Compliance check (Pillar V)
        compliance = check_supply_chain_compliance(disruption_event, route_info)
        compliance_blocked = not compliance["compliant"]

        # Step 4: Determine state and confidence
        if compliance_blocked:
            forced_state = TLState.REFUSE
            confidence = 0.0
            reasoning = (
                f"Supply chain compliance failure prevents rerouting: "
                f"{'; '.join(compliance['failures'])}"
            )

        elif esg_blocked:
            forced_state = TLState.EPISTEMIC_HOLD
            confidence = 0.0
            reasoning = (
                f"Pillar VI ESG mandate failure on alternative route: "
                f"{'; '.join(esg_result.metadata.get('failed_checks', []))}. "
                "Cannot authorize rerouting to non-compliant supplier."
            )

        else:
            forced_state = None
            # Calculate weighted composite confidence
            numeric_signals = {
                k: v for k, v in signals.items()
                if isinstance(v, (int, float)) and v is not None
            }

            if not numeric_signals:
                forced_state = TLState.EPISTEMIC_HOLD
                confidence = 0.0
                reasoning = (
                    "Insufficient disruption data to assess rerouting "
                    "viability. Epistemic Hold: irreversible commitment "
                    "requires verified truth."
                )
            else:
                # Weight signals by domain priority
                weights = self._get_signal_weights(
                    numeric_signals, market_conditions
                )
                weighted_sum = sum(
                    numeric_signals.get(k, 0.5) * w
                    for k, w in weights.items()
                    if k in numeric_signals
                )
                weight_total = sum(
                    w for k, w in weights.items()
                    if k in numeric_signals
                )
                confidence = (
                    weighted_sum / weight_total
                    if weight_total > 0 else 0.5
                )
                reasoning = self._build_reasoning(
                    signals, disruption_event, market_conditions
                )

        # Step 5: Evaluate with TLEngine
        decision = self.engine.evaluate(
            confidence=confidence,
            reasoning=reasoning,
            metadata={
                "scenario": scenario_label,
                "eventType": disruption_event.get("event_type", "unknown"),
                "signalCount": len([
                    v for v in signals.values()
                    if isinstance(v, (int, float))
                ]),
                "esgBlocked": esg_blocked,
                "complianceBlocked": compliance_blocked,
                "pillarImplicated": (
                    "SustainableCapitalAllocationMandate"
                    if esg_blocked
                    else "EconomicRightsAndTransparencyMandate"
                    if compliance_blocked
                    else "EpistemicHold"
                )
            },
            force_state=forced_state
        )

        # Step 6: Commit log entry (NL=NA: BEFORE any rerouting fires)
        goukassian = create_goukassian_principle_block(
            decision_payload=decision.reasoning,
            agent_id="supply-chain-governance-001",
            license_scopes=self.license_scopes
        )
        log_entry = commit_log_entry(
            decision=decision,
            engine=self.engine,
            goukassian_block=goukassian,
            previous_hash=self.ledger.previous_hash,
            extra_context={
                "eventType": disruption_event.get("event_type", "unknown"),
                "signals": {
                    k: round(v, 4)
                    for k, v in signals.items()
                    if isinstance(v, (int, float))
                },
                "regulatoryCompliant": compliance["compliant"],
                "esgCompliant": not esg_blocked,
                "costSensitivity": self.cost_sensitivity,
                "timeSensitivity": self.time_sensitivity
            }
        )
        self.ledger.commit(log_entry)

        # Step 7: Permission Token (PROCEED only)
        token = build_permission_token(log_entry)

        # Step 8: Response plan based on state
        response_plan = self._build_response_plan(
            decision, disruption_event, route_info, signals
        )

        record = {
            "scenario": scenario_label,
            "eventType": disruption_event.get("event_type", "unknown"),
            "state": decision.state.name,
            "stateValue": decision.state.value,
            "processActive": log_entry["processActive"],
            "confidence": decision.confidence,
            "positionLabel": decision.position_label,
            "reasoning": decision.reasoning,
            "logHash": log_entry["logHash"][:16] + "...",
            "merkleRoot": log_entry["merkleRoot"][:16] + "...",
            "permissionToken": (
                token["tokenId"][:16] + "..." if token else None
            ),
            "laneOrigin": token["laneOrigin"] if token else "N/A",
            "responsePlan": response_plan,
            "regulatoryCompliant": compliance["compliant"],
            "regulatoryFailures": compliance["failures"],
            "regulatoryWarnings": compliance["warnings"],
            "esgCompliant": not esg_blocked,
            "nlNaStatus": "Log committed before rerouting authorized"
        }

        self._decisions.append(record)
        return record

    def _get_signal_weights(
        self,
        signals: Dict[str, float],
        market_conditions: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Compute signal weights based on business context.

        Weights are adjusted by cost_sensitivity and time_sensitivity
        configuration. In cost-sensitive industries, route viability
        and inventory buffer carry more weight. In time-sensitive
        industries, customer urgency and duration confidence dominate.
        """
        base_weights = {
            "disruption_severity": 0.25,
            "duration_confidence": 0.15,
            "route_viability": 0.20,
            "inventory_buffer": 0.15,
            "supplier_flexibility": 0.10,
            "customer_urgency": 0.10,
            "sustainability": 0.05
        }

        # Adjust for time sensitivity
        if self.time_sensitivity > 0.5:
            base_weights["customer_urgency"] = min(
                base_weights["customer_urgency"] + 0.10, 0.25
            )
            base_weights["inventory_buffer"] = min(
                base_weights["inventory_buffer"] + 0.05, 0.25
            )

        # Adjust for cost sensitivity
        if self.cost_sensitivity > 0.5:
            base_weights["route_viability"] = min(
                base_weights["route_viability"] + 0.05, 0.30
            )

        return base_weights

    def _build_reasoning(
        self,
        signals: Dict[str, Any],
        disruption_event: Dict[str, Any],
        market_conditions: Dict[str, Any]
    ) -> str:
        """Build human-readable reasoning from supply chain signals."""
        parts = []

        severity = signals.get("disruption_severity")
        if severity is not None:
            if severity > 0.7:
                parts.append("Disruption severity: high confidence in serious impact")
            elif severity < 0.4:
                parts.append(
                    "Disruption severity: conflicting reports, confidence low"
                )

        route = signals.get("route_viability")
        if route is not None:
            if route > 0.7:
                parts.append("Alternative route: viable with adequate capacity")
            elif route < 0.3:
                parts.append(
                    "Alternative route: limited viability, rerouting risky"
                )

        inventory = signals.get("inventory_buffer")
        if inventory is not None:
            if inventory > 0.7:
                parts.append(
                    "Inventory: adequate buffer for deliberate evaluation"
                )
            elif inventory < 0.3:
                parts.append(
                    "Inventory: low buffer; urgency increasing"
                )

        urgency = signals.get("customer_urgency")
        if urgency is not None and urgency < 0.3:
            parts.append("Customer urgency: critical commitments at risk")

        event_type = disruption_event.get("event_type", "")
        if event_type:
            parts.append(f"Event type: {event_type}")

        return ". ".join(parts) if parts else "Supply chain signal analysis"

    def _build_response_plan(
        self,
        decision: TLValue,
        disruption_event: Dict[str, Any],
        route_info: Dict[str, Any],
        signals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build concrete response plan based on TL state.

        PROCEED: implement major route change.
        EPISTEMIC_HOLD: graduated response with data gathering.
        REFUSE: maintain current operations with enhanced monitoring.
        """
        if decision.state == TLState.PROCEED:
            best_route = None
            alt_routes = route_info.get("alternative_routes", [])
            if alt_routes:
                best_route = max(
                    alt_routes,
                    key=lambda r: (
                        r.get("reliability_score", 0)
                        * r.get("capacity_available", 0)
                    )
                )

            return {
                "primaryAction": "IMPLEMENT_REROUTE",
                "selectedRoute": best_route.get("route_id") if best_route else None,
                "routeReliability": (
                    best_route.get("reliability_score")
                    if best_route else None
                ),
                "estimatedLeadTimeDays": disruption_event.get(
                    "estimated_resolution_days", 14
                ),
                "supplierNotificationRequired": True,
                "customerNotificationRequired": True,
                "complianceReportingRequired": True,
                "note": (
                    "Rerouting authorized by PermissionToken. "
                    "NL=NA: log committed before rerouting fired."
                )
            }

        elif decision.state == TLState.EPISTEMIC_HOLD:
            resolution_deadline = (
                datetime.now(timezone.utc) + timedelta(hours=24)
            ).isoformat()

            return {
                "primaryAction": "EPISTEMIC_HOLD_PROTOCOL",
                "holdDurationMs": 300,
                "resolutionDeadline": resolution_deadline,
                "immediateActions": [
                    "Activate secondary inventory reserves",
                    "Query tertiary oracle sources for disruption verification",
                    "Request updated severity assessments from field agents",
                    "Prepare contingency contracts with qualified alternatives"
                ],
                "dataRequirements": [
                    k for k, v in signals.items()
                    if v is None or (isinstance(v, float) and v < 0.3)
                ],
                "permittedResolutionStates": [1, -1],
                "note": (
                    "Epistemic Hold: irreversible rerouting commitment "
                    "requires verified truth. Gathering additional data "
                    "before authorizing route change."
                )
            }

        else:  # TLState.REFUSE
            return {
                "primaryAction": "MAINTAIN_CURRENT_OPERATIONS",
                "enhancedMonitoring": True,
                "monitoringIntervalHours": 4,
                "contingencyPreparation": [
                    "Pre-qualify alternative suppliers for rapid onboarding",
                    "Negotiate option contracts on alternative capacity",
                    "Brief customer success teams on potential delays"
                ],
                "escalationTriggers": [
                    "Disruption duration exceeds 14 days",
                    "Inventory buffer falls below 7 days coverage",
                    "Critical customer commitment within 5 days"
                ],
                "note": (
                    "Refuse: compliance or ESG failure prevents rerouting. "
                    "Maintain current route under enhanced monitoring. "
                    "refusalIsPermanent unless compliance resolved."
                )
            }

    def get_summary(self) -> Dict[str, Any]:
        """Return summary of all supply chain decisions."""
        stats = self.engine.get_statistics()
        ledger = self.ledger.get_summary()

        return {
            "totalDecisions": stats["total_decisions"],
            "proceedCount": stats["proceed_count"],
            "epistemicHoldCount": stats["hold_count"],
            "refuseCount": stats["refuse_count"],
            "epistemicHoldRate": stats["epistemic_hold_rate"],
            "targetHoldRate": stats["target_hold_rate"],
            "averageConfidence": stats["average_confidence"],
            "ledgerEntries": ledger["totalEntries"],
            "latestMerkleRoot": ledger["latestMerkleRoot"][:16] + "...",
            "architectureMode": "ARCHITECTURE_B",
            "pufAttestation": "NULL_PUF_DEPLOYMENT"
        }


# =============================================================================
# SECTION 5: Demonstration Scenarios
# =============================================================================

def run_supply_chain_demo():
    """
    Demonstrate TL supply chain management across five scenarios:
        1. Clear reroute: severe disruption, viable alternative, ESG compliant
        2. Epistemic Hold: conflicting disruption reports
        3. ESG mandate failure: alternative route not compliant (Pillar VI)
        4. Compliance failure: labor rights violations (Pillar V)
        5. Low inventory urgency: Solvency Protocol behavior

    DEMONSTRATION THRESHOLD VALUES: not for production use.
    Pharmaceutical, consumer electronics, and food supply chains each
    require different calibrations. See docs/Threshold_Calibration.md.
    """

    print()
    print("=" * 70)
    print("  TERNARY LOGIC: GLOBAL SUPPLY CHAIN MANAGEMENT")
    print("  Lev Goukassian (ORCID: 0009-0006-5966-1243)")
    print("  'The Epistemic Hold prevents supply chain overreactions.'")
    print("=" * 70)

    # DEMONSTRATION VALUES ONLY: not recommendations, not standards.
    # Supply chain thresholds are calibrated per industry and risk profile.
    DEMO_PROCEED = 0.68
    DEMO_HOLD = 0.28

    manager = GlobalSupplyChainManager(
        proceed_threshold=DEMO_PROCEED,
        hold_threshold=DEMO_HOLD,
        cost_sensitivity=0.3,
        time_sensitivity=0.4
    )

    print()
    print(f"  Engine initialized (demonstration thresholds: not for production)")
    print(f"  PROCEED >= {DEMO_PROCEED} | REFUSE < {DEMO_HOLD}")
    print(f"  Cost sensitivity: 0.3 | Time sensitivity: 0.4")

    # Shared dates for customer commitments
    soon = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()
    later = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()

    # ------------------------------------------------------------------
    # SCENARIO 1: Clear reroute decision
    # Severe disruption, high agreement on severity, viable alternative,
    # ESG compliant, all checks pass.
    # Expected: PROCEED with rerouting plan.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 1: Clear Reroute Decision")
    print("-" * 70)

    disruption_1 = {
        "event_type": "PORT_CLOSURE",
        "severity_reports": [
            {"source": "port_authority", "severity": 0.92},
            {"source": "shipping_company", "severity": 0.88},
            {"source": "logistics_partner", "severity": 0.90}
        ],
        "duration_estimates": [
            {"source": "port_authority", "days": 21},
            {"source": "industry_report", "days": 18},
            {"source": "insurance_assessment", "days": 24}
        ],
        "alternative_suppliers_screened": True,
        "restricted_goods_involved": False,
        "estimated_resolution_days": 21
    }

    route_1 = {
        "alternative_routes": [
            {
                "route_id": "CAPE_OF_GOOD_HOPE",
                "capacity_available": 0.82,
                "reliability_score": 0.88
            },
            {
                "route_id": "TRANS_PACIFIC_ALT",
                "capacity_available": 0.65,
                "reliability_score": 0.78
            }
        ],
        "cost_comparisons": [
            {"route_id": "CAPE_OF_GOOD_HOPE", "alternative_cost_ratio": 1.35}
        ],
        "supplier_network": {
            "qualified_alternatives": 4,
            "total_alternatives": 5,
            "avg_onboarding_weeks": 3,
            "avg_utilization": 0.62
        },
        "labor_violations_detected": False,
        "child_labor_risk_score": 0.08
    }

    conditions_1 = {
        "current_inventory": {
            "SKU-A": 4500,
            "SKU-B": 3200,
            "SKU-C": 5100
        },
        "demand_forecast": {
            "SKU-A": 2400,
            "SKU-B": 1800,
            "SKU-C": 2700
        },
        "customer_commitments": [
            {"id": "CUST-001", "criticality": "high", "deadline": later},
            {"id": "CUST-002", "criticality": "medium", "deadline": later}
        ],
        "sustainability_metrics": {
            "carbon_intensity_score": 72,
            "labor_rights_score": 85,
            "certification_count": 4
        },
        "esg_verified": True,
        "emissions_anchored": True,
        "use_of_proceeds_tracked": True
    }

    r1 = manager.make_supply_chain_decision(
        disruption_1, route_1, conditions_1, "Port Closure Reroute"
    )
    _print_supply_chain_result(r1)

    # ------------------------------------------------------------------
    # SCENARIO 2: Epistemic Hold via conflicting disruption reports
    # Wide disagreement on severity and duration.
    # Rerouting is irreversible; conflicting signals warrant pause.
    # Expected: EPISTEMIC_HOLD.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 2: Epistemic Hold via Conflicting Reports")
    print("-" * 70)

    disruption_2 = {
        "event_type": "WEATHER_EVENT",
        "severity_reports": [
            {"source": "local_agency", "severity": 0.85},
            {"source": "regional_authority", "severity": 0.30},
            {"source": "satellite_data", "severity": 0.55}
        ],
        "duration_estimates": [
            {"source": "meteorological", "days": 3},
            {"source": "local_operator", "days": 45},
            {"source": "insurance", "days": 14}
        ],
        "alternative_suppliers_screened": True,
        "restricted_goods_involved": False
    }

    route_2 = {
        "alternative_routes": [
            {
                "route_id": "NORTHERN_CORRIDOR",
                "capacity_available": 0.55,
                "reliability_score": 0.62
            }
        ],
        "cost_comparisons": [
            {"route_id": "NORTHERN_CORRIDOR", "alternative_cost_ratio": 1.85}
        ],
        "supplier_network": {
            "qualified_alternatives": 1,
            "total_alternatives": 3,
            "avg_onboarding_weeks": 8,
            "avg_utilization": 0.78
        },
        "labor_violations_detected": False,
        "child_labor_risk_score": 0.15
    }

    conditions_2 = {
        "current_inventory": {
            "SKU-A": 3800,
            "SKU-B": 2900
        },
        "demand_forecast": {"SKU-A": 2200, "SKU-B": 1600},
        "customer_commitments": [
            {"id": "CUST-003", "criticality": "medium", "deadline": later}
        ],
        "sustainability_metrics": {
            "carbon_intensity_score": 68,
            "labor_rights_score": 74,
            "certification_count": 2
        },
        "esg_verified": True,
        "emissions_anchored": True,
        "use_of_proceeds_tracked": True
    }

    r2 = manager.make_supply_chain_decision(
        disruption_2, route_2, conditions_2, "Conflicting Reports"
    )
    _print_supply_chain_result(r2)

    # ------------------------------------------------------------------
    # SCENARIO 3: ESG mandate failure (Pillar VI)
    # Alternative route not ESG verified.
    # Binary mandate override forces Epistemic Hold regardless of signals.
    # Expected: EPISTEMIC_HOLD (forced by Pillar VI).
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 3: ESG Mandate Failure (Pillar VI)")
    print("-" * 70)

    disruption_3 = {
        "event_type": "SUPPLIER_BANKRUPTCY",
        "severity_reports": [
            {"source": "financial_monitor", "severity": 0.95},
            {"source": "credit_agency", "severity": 0.93}
        ],
        "duration_estimates": [
            {"source": "legal_assessment", "days": 90},
            {"source": "industry_analyst", "days": 75}
        ],
        "alternative_suppliers_screened": True,
        "restricted_goods_involved": False,
        "estimated_resolution_days": 82
    }

    route_3 = {
        "alternative_routes": [
            {
                "route_id": "UNVERIFIED_SUPPLIER_X",
                "capacity_available": 0.90,
                "reliability_score": 0.85
            }
        ],
        "cost_comparisons": [
            {"route_id": "UNVERIFIED_SUPPLIER_X", "alternative_cost_ratio": 1.10}
        ],
        "supplier_network": {
            "qualified_alternatives": 2,
            "total_alternatives": 4,
            "avg_onboarding_weeks": 4,
            "avg_utilization": 0.55
        },
        "labor_violations_detected": False,
        "child_labor_risk_score": 0.12
    }

    conditions_3 = {
        "current_inventory": {"SKU-A": 5200, "SKU-B": 4100},
        "demand_forecast": {"SKU-A": 2800, "SKU-B": 2200},
        "customer_commitments": [
            {"id": "CUST-004", "criticality": "high", "deadline": later}
        ],
        "sustainability_metrics": {
            "carbon_intensity_score": 40,
            "labor_rights_score": 35,
            "certification_count": 0
        },
        "esg_verified": False,          # PILLAR VI FAILS
        "emissions_anchored": False,    # PILLAR VI FAILS
        "use_of_proceeds_tracked": True
    }

    r3 = manager.make_supply_chain_decision(
        disruption_3, route_3, conditions_3, "ESG Mandate Failure"
    )
    _print_supply_chain_result(r3)

    # ------------------------------------------------------------------
    # SCENARIO 4: Compliance failure via labor rights violation (Pillar V)
    # Alternative route has confirmed labor violations.
    # Forces Refuse (-1).
    # Expected: REFUSE.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 4: Labor Rights Violation (Pillar V: Refuse)")
    print("-" * 70)

    disruption_4 = {
        "event_type": "GEOPOLITICAL_DISRUPTION",
        "severity_reports": [
            {"source": "government_advisory", "severity": 0.88},
            {"source": "trade_association", "severity": 0.84}
        ],
        "duration_estimates": [
            {"source": "political_analyst", "days": 60},
            {"source": "trade_economist", "days": 45}
        ],
        "alternative_suppliers_screened": True,
        "restricted_goods_involved": False,
        "estimated_resolution_days": 52
    }

    route_4 = {
        "alternative_routes": [
            {
                "route_id": "ZONE-X-CORRIDOR",
                "capacity_available": 0.75,
                "reliability_score": 0.70
            }
        ],
        "cost_comparisons": [
            {"route_id": "ZONE-X-CORRIDOR", "alternative_cost_ratio": 1.20}
        ],
        "supplier_network": {
            "qualified_alternatives": 3,
            "total_alternatives": 5,
            "avg_onboarding_weeks": 6,
            "avg_utilization": 0.68
        },
        "labor_violations_detected": True,  # PILLAR V FAILS
        "child_labor_risk_score": 0.72      # PILLAR V FAILS
    }

    conditions_4 = {
        "current_inventory": {"SKU-A": 6000, "SKU-B": 4800},
        "demand_forecast": {"SKU-A": 3000, "SKU-B": 2400},
        "customer_commitments": [
            {"id": "CUST-005", "criticality": "medium", "deadline": later}
        ],
        "sustainability_metrics": {
            "carbon_intensity_score": 55,
            "labor_rights_score": 28,
            "certification_count": 1
        },
        "esg_verified": True,
        "emissions_anchored": True,
        "use_of_proceeds_tracked": True
    }

    r4 = manager.make_supply_chain_decision(
        disruption_4, route_4, conditions_4, "Labor Rights Violation"
    )
    _print_supply_chain_result(r4)

    # ------------------------------------------------------------------
    # SCENARIO 5: Low inventory with customer deadline pressure
    # Solvency Protocol analog: inadequate buffer triggers Epistemic Hold
    # even with a viable alternative, because urgency demands verified
    # truth before committing to an irreversible reroute.
    # Expected: EPISTEMIC_HOLD (low inventory buffer + urgent deadline).
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 5: Low Inventory (Solvency Protocol Analog)")
    print("-" * 70)

    disruption_5 = {
        "event_type": "LOGISTICS_CONGESTION",
        "severity_reports": [
            {"source": "freight_forwarder", "severity": 0.70},
            {"source": "port_monitor", "severity": 0.65}
        ],
        "duration_estimates": [
            {"source": "freight_forwarder", "days": 10},
            {"source": "port_monitor", "days": 8}
        ],
        "alternative_suppliers_screened": True,
        "restricted_goods_involved": False,
        "estimated_resolution_days": 9
    }

    route_5 = {
        "alternative_routes": [
            {
                "route_id": "AIR_FREIGHT_EXPRESS",
                "capacity_available": 0.60,
                "reliability_score": 0.92
            }
        ],
        "cost_comparisons": [
            {"route_id": "AIR_FREIGHT_EXPRESS", "alternative_cost_ratio": 4.2}
        ],
        "supplier_network": {
            "qualified_alternatives": 2,
            "total_alternatives": 3,
            "avg_onboarding_weeks": 2,
            "avg_utilization": 0.70
        },
        "labor_violations_detected": False,
        "child_labor_risk_score": 0.05
    }

    conditions_5 = {
        "current_inventory": {
            "SKU-A": 280,   # Only 3 days coverage
            "SKU-B": 190    # Only 3 days coverage
        },
        "demand_forecast": {"SKU-A": 2800, "SKU-B": 1900},
        "customer_commitments": [
            {
                "id": "CUST-006",
                "criticality": "critical",
                "deadline": soon  # 5 days away
            }
        ],
        "sustainability_metrics": {
            "carbon_intensity_score": 82,
            "labor_rights_score": 90,
            "certification_count": 5
        },
        "esg_verified": True,
        "emissions_anchored": True,
        "use_of_proceeds_tracked": True
    }

    r5 = manager.make_supply_chain_decision(
        disruption_5, route_5, conditions_5, "Low Inventory Urgency"
    )
    _print_supply_chain_result(r5)

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("SUPPLY CHAIN SESSION SUMMARY")
    print("=" * 70)

    summary = manager.get_summary()
    print(f"  Total decisions:     {summary['totalDecisions']}")
    print(f"  PROCEED:             {summary['proceedCount']}")
    print(f"  EPISTEMIC_HOLD:      {summary['epistemicHoldCount']}")
    print(f"  REFUSE:              {summary['refuseCount']}")
    print(f"  Hold rate:           {summary['epistemicHoldRate']:.1%} "
          f"(target: {summary['targetHoldRate']:.1%})")
    print(f"  Average confidence:  {summary['averageConfidence']:.3f}")
    print(f"  Ledger entries:      {summary['ledgerEntries']}")
    print(f"  Latest Merkle root:  {summary['latestMerkleRoot']}")
    print(f"  Architecture mode:   {summary['architectureMode']}")
    print(f"  PUF attestation:     {summary['pufAttestation']}")
    print()
    print("  NL=NA: Every rerouting decision was logged to the Immutable")
    print("  Ledger before any route change was authorized.")
    print("  No log, no reroute.")
    print()
    print("  Three immutable mandates:")
    print("    No Spy. No Weapon. No Switch Off.")
    print("=" * 70)
    print()

    # Export audit trail (Pillar IV)
    manager.engine.export_audit_trail("/tmp/tl_supply_chain_audit.json")
    print("  Audit trail exported: /tmp/tl_supply_chain_audit.json")
    print()


def _print_supply_chain_result(result: Dict[str, Any]):
    """Print formatted supply chain decision result."""
    state_labels = {
        "PROCEED": "OK",
        "EPISTEMIC_HOLD": "HOLD",
        "REFUSE": "REFUSE"
    }
    label = state_labels.get(result["state"], "")

    print(f"  State:           {label} {result['state']} ({result['stateValue']})")
    print(f"  processActive:   {result['processActive']}")
    print(f"  Event type:      {result['eventType']}")
    print(f"  Confidence:      {result['confidence']:.3f}")
    print(f"  Position:        {result['positionLabel']}")
    print(f"  Log committed:   {result['logHash']}")
    print(f"  Merkle root:     {result['merkleRoot']}")

    if result.get("permissionToken"):
        print(f"  Permission token: {result['permissionToken']}")
        print(f"  laneOrigin:       {result['laneOrigin']}")
    else:
        print(f"  Permission token: None")

    plan = result.get("responsePlan", {})
    action = plan.get("primaryAction", "N/A")
    print(f"  Response action: {action}")

    if action == "IMPLEMENT_REROUTE":
        route = plan.get("selectedRoute", "N/A")
        print(f"  Selected route:  {route}")
    elif action == "EPISTEMIC_HOLD_PROTOCOL":
        reqs = plan.get("dataRequirements", [])
        if reqs:
            print(f"  Data needed:     {', '.join(reqs[:3])}")
        deadline = plan.get("resolutionDeadline", "")
        if deadline:
            print(f"  Resolve by:      {deadline}")

    if result.get("regulatoryFailures"):
        for f in result["regulatoryFailures"]:
            print(f"  Compliance FAIL: {f}")

    if not result.get("esgCompliant"):
        print(f"  ESG mandate:     FAILED (Pillar VI forced Epistemic Hold)")

    if result.get("regulatoryWarnings"):
        for w in result["regulatoryWarnings"][:1]:
            print(f"  Warning:         {w}")

    print(f"  NL=NA:           {result['nlNaStatus']}")


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    run_supply_chain_demo()


"""
---
Creator: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Email: leogouk@gmail.com
Repository: https://github.com/FractonicMind/TernaryLogic
Successor: support@tl-goukassian.org
DOI 1: 10.1007/s43681-025-00910-6
DOI 2: 10.1007/s43681-026-01124-0
---
"""
