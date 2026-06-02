"""
Ternary Logic Framework - Core Implementation
==============================================

A three-valued logic system for economic decision-making under uncertainty.

States:
    +1 (PROCEED):        Execute action when conditions are clear and verified
     0 (EPISTEMIC_HOLD): Pause for deliberation when uncertainty exceeds thresholds
    -1 (REFUSE):         Reject action when conditions definitively fail requirements

THRESHOLD GOVERNANCE:
    The TL framework does not ship universal threshold values.
    Thresholds are institutionally calibrated governance decisions that must
    be established through all of the following:

    1. Historical backtesting: minimize errors and costs over 20+ years of data
    2. Regulatory requirements: Basel III, FATF, SEC and other applicable mandates
    3. Institutional risk tolerance: board-approved risk appetite statement
    4. Market regime adaptation: dynamic adjustment for volatility conditions
    5. Mandate verification: automatic holds on verification failures are
       independent of confidence thresholds and cannot be overridden by them

    There is no universal default. A central bank monetary policy engine, a
    high-frequency equity trading system, and a supply chain ESG verifier
    operate under fundamentally different uncertainty profiles. The framework
    enforces that a threshold exists and is applied consistently. What that
    threshold is belongs entirely to the governed institution.

    TLEngine raises ValueError if instantiated without explicit threshold values.
    This is intentional and constitutional.

DISPLAY LABEL BOUNDARIES:
    ConfidenceLevel (HIGH/MEDIUM/LOW/CRITICAL) is a qualitative display
    classifier for human-readable output and audit logs only. The boundaries
    at which these labels switch (defined by DISPLAY_LABEL_* constants in
    __init__.py) are NOT decision thresholds. They do not determine state
    outcomes. Decision thresholds are institution-specific governed parameters.

CONFIDENCE CALCULATION:
    Composite score from four factors (each 25% weight):
    - Data Quality: completeness, freshness, cryptographic verification
    - Model Agreement: consensus across multiple models, low variance
    - Historical Accuracy: recent prediction success rate (90-day window)
    - Signal Strength: clear directional indicators, low noise

AUTOMATIC TRIGGERS:
    Epistemic Hold triggers automatically when:
    - Economic Rights and Transparency mandate fails (ownership, consent, provenance)
    - Sustainable Capital Allocation mandate fails (ESG data, emissions verification)
    - Data missing, stale (>24hrs), or unverifiable
    - Model conflict exceeds 30% disagreement
    These triggers override confidence scores entirely.

Created by: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Repository: https://github.com/FractonicMind/TernaryLogic
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import json
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Display label boundaries for qualitative output classification only.
# These are NOT decision thresholds. They define where ConfidenceLevel
# labels switch in human-readable output and audit logs.
# Decision thresholds are institution-specific governed parameters
# set via TLEngine constructor arguments.
_DISPLAY_LABEL_HIGH = 0.85
_DISPLAY_LABEL_MEDIUM = 0.60
_DISPLAY_LABEL_LOW = 0.40


class TLState(Enum):
    """Three-valued logic states for economic decisions."""
    PROCEED = 1          # +1: Clear to execute
    EPISTEMIC_HOLD = 0   # 0:  Pause for deliberation
    REFUSE = -1          # -1: Reject execution


class ConfidenceLevel(Enum):
    """Qualitative confidence level for display and audit log output only.

    These labels appear in TLValue.confidence_level and in exported audit
    trails to give human readers a qualitative sense of the confidence score.
    They have no effect on state determination. Whether a given confidence
    score produces PROCEED, EPISTEMIC_HOLD, or REFUSE depends entirely on
    the institution-calibrated thresholds set at TLEngine initialization.

    The numeric boundaries at which these labels switch are display constants,
    not governance parameters. They are prefixed with _DISPLAY_LABEL_ to
    make this distinction visible in code.
    """
    HIGH = "high"           # confidence >= _DISPLAY_LABEL_HIGH
    MEDIUM = "medium"       # _DISPLAY_LABEL_MEDIUM <= confidence < _DISPLAY_LABEL_HIGH
    LOW = "low"             # _DISPLAY_LABEL_LOW <= confidence < _DISPLAY_LABEL_MEDIUM
    CRITICAL = "critical"   # confidence < _DISPLAY_LABEL_LOW


@dataclass
class TLValue:
    """
    Ternary Logic value with metadata.

    Attributes:
        state: The TL state (PROCEED/EPISTEMIC_HOLD/REFUSE)
        confidence: Confidence score [0.0, 1.0]
        reasoning: Human-readable explanation
        metadata: Additional context data
        timestamp: When this value was created
    """
    state: TLState
    confidence: float
    reasoning: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                f"Confidence must be in [0.0, 1.0], got {self.confidence}"
            )

    @property
    def confidence_level(self) -> ConfidenceLevel:
        """Get qualitative display label for this confidence score.

        Returns a human-readable label for audit logs and display output.
        This label does NOT reflect whether the score resulted in PROCEED,
        EPISTEMIC_HOLD, or REFUSE. That determination depends on the
        institution-calibrated thresholds set at TLEngine initialization.
        """
        if self.confidence >= _DISPLAY_LABEL_HIGH:
            return ConfidenceLevel.HIGH
        elif self.confidence >= _DISPLAY_LABEL_MEDIUM:
            return ConfidenceLevel.MEDIUM
        elif self.confidence >= _DISPLAY_LABEL_LOW:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.CRITICAL

    def to_dict(self) -> Dict[str, Any]:
        return {
            'state': self.state.name,
            'state_value': self.state.value,
            'confidence': self.confidence,
            'confidence_level': self.confidence_level.value,
            'reasoning': self.reasoning,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class EpistemicHoldEvent:
    """Record of an Epistemic Hold occurrence with immutable audit trail."""
    event_id: str
    trigger_reason: str
    data_inputs: Dict[str, Any]
    model_outputs: Dict[str, Any]
    signal_conflicts: List[str]
    uncertainty_metrics: Dict[str, float]
    resolution_action: Optional[str] = None
    resolution_timestamp: Optional[datetime] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.event_id:
            hash_input = f"{self.timestamp.isoformat()}{self.trigger_reason}"
            self.event_id = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    def resolve(self, action: str):
        self.resolution_action = action
        self.resolution_timestamp = datetime.utcnow()
        logger.info(f"Epistemic Hold {self.event_id} resolved: {action}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_id': self.event_id,
            'trigger_reason': self.trigger_reason,
            'data_inputs': self.data_inputs,
            'model_outputs': self.model_outputs,
            'signal_conflicts': self.signal_conflicts,
            'uncertainty_metrics': self.uncertainty_metrics,
            'resolution_action': self.resolution_action,
            'resolution_timestamp': (
                self.resolution_timestamp.isoformat()
                if self.resolution_timestamp else None
            ),
            'timestamp': self.timestamp.isoformat()
        }


class TLEngine:
    """Core Ternary Logic decision engine for economic intelligence.

    Thresholds are mandatory constructor arguments. The engine raises
    ValueError if instantiated without explicit values. This is intentional:
    there are no universal defaults. Thresholds must be calibrated by your
    institution through historical backtesting, regulatory requirements,
    board-approved risk appetite, and market regime analysis.

    See docs/Threshold_Calibration.md for calibration methodology.
    See ThresholdProfile schema in the API spec for governance requirements.
    """

    def __init__(
        self,
        proceed_threshold: Optional[float] = None,
        hold_threshold: Optional[float] = None,
        epistemic_hold_rate_target: float = 0.20
    ):
        """
        Initialize TL Engine with institutionally calibrated thresholds.

        Args:
            proceed_threshold: Minimum confidence to PROCEED.
                               REQUIRED. No default. Must be calibrated by
                               your institution through historical backtesting,
                               regulatory requirements, and board-approved risk
                               appetite. Cannot be None in any deployment.
            hold_threshold:    Below this confidence triggers REFUSE.
                               REQUIRED. No default. Same calibration
                               requirements as proceed_threshold.
            epistemic_hold_rate_target: Monitoring target for hold rate.
                               Default 0.20 (20%). Studies indicate 15-25% is
                               optimal. Monitor and report; recalibrate
                               thresholds if consistently outside this range.

        Raises:
            ValueError: If proceed_threshold or hold_threshold is None,
                        or if thresholds do not satisfy the ordering constraint.
        """
        if proceed_threshold is None:
            raise ValueError(
                "proceed_threshold is required and has no default value. "
                "This threshold must be calibrated by your institution through "
                "historical backtesting, regulatory requirements, and "
                "board-approved risk appetite. "
                "No universal value is appropriate for all systems. "
                "See docs/Threshold_Calibration.md for calibration methodology."
            )
        if hold_threshold is None:
            raise ValueError(
                "hold_threshold is required and has no default value. "
                "This threshold must be calibrated by your institution through "
                "historical backtesting, regulatory requirements, and "
                "board-approved risk appetite. "
                "No universal value is appropriate for all systems. "
                "See docs/Threshold_Calibration.md for calibration methodology."
            )
        if not 0.0 < hold_threshold < proceed_threshold < 1.0:
            raise ValueError(
                f"Thresholds must satisfy: 0.0 < hold_threshold < "
                f"proceed_threshold < 1.0. "
                f"Got hold_threshold={hold_threshold}, "
                f"proceed_threshold={proceed_threshold}."
            )

        self.proceed_threshold = proceed_threshold
        self.hold_threshold = hold_threshold
        self.epistemic_hold_rate_target = epistemic_hold_rate_target
        self.epistemic_holds: List[EpistemicHoldEvent] = []
        self.decision_log: List[TLValue] = []
        logger.info(
            f"TL Engine initialized with institution-calibrated thresholds: "
            f"PROCEED >= {proceed_threshold}, REFUSE < {hold_threshold}"
        )

    def evaluate(
        self,
        confidence: float,
        reasoning: str,
        metadata: Optional[Dict[str, Any]] = None,
        force_state: Optional[TLState] = None
    ) -> TLValue:
        """
        Evaluate economic conditions and return TL state.

        State determination:
            confidence >= self.proceed_threshold  ->  PROCEED (+1)
            self.hold_threshold <= confidence
                                < self.proceed_threshold  ->  EPISTEMIC_HOLD (0)
            confidence < self.hold_threshold      ->  REFUSE (-1)

        Mandate failures use force_state=TLState.EPISTEMIC_HOLD with
        confidence=0.0 to override this determination entirely. Even
        a confidence of 1.0 does not prevent an Epistemic Hold if a
        mandate check fails.

        Args:
            confidence:   Confidence score [0.0, 1.0]
            reasoning:    Explanation for the decision
            metadata:     Additional context
            force_state:  Override automatic state for mandate failures

        Returns:
            TLValue with state, confidence, and reasoning
        """
        if force_state:
            state = force_state
        else:
            if confidence >= self.proceed_threshold:
                state = TLState.PROCEED
            elif confidence < self.hold_threshold:
                state = TLState.REFUSE
            else:
                state = TLState.EPISTEMIC_HOLD

        value = TLValue(
            state=state,
            confidence=confidence,
            reasoning=reasoning,
            metadata=metadata or {}
        )
        self.decision_log.append(value)

        if state == TLState.EPISTEMIC_HOLD:
            self._log_epistemic_hold(value)

        logger.info(f"TL Decision: {state.name} (confidence: {confidence:.3f})")
        return value

    def _log_epistemic_hold(self, value: TLValue):
        """Create audit record for Epistemic Hold event."""
        event = EpistemicHoldEvent(
            event_id="",
            trigger_reason=value.reasoning,
            data_inputs=value.metadata.get('inputs', {}),
            model_outputs=value.metadata.get('outputs', {}),
            signal_conflicts=value.metadata.get('conflicts', []),
            uncertainty_metrics={
                'confidence': value.confidence,
                'distance_to_proceed': abs(
                    value.confidence - self.proceed_threshold
                )
            }
        )
        self.epistemic_holds.append(event)
        logger.warning(f"EPISTEMIC HOLD triggered: {event.event_id}")

    def resolve_hold(self, event_id: str, action: str):
        """Resolve an Epistemic Hold with documented action."""
        for event in self.epistemic_holds:
            if event.event_id == event_id:
                event.resolve(action)
                return
        raise ValueError(f"Epistemic Hold event {event_id} not found")

    @property
    def epistemic_hold_rate(self) -> float:
        """Calculate current Epistemic Hold rate."""
        if not self.decision_log:
            return 0.0
        holds = sum(
            1 for d in self.decision_log if d.state == TLState.EPISTEMIC_HOLD
        )
        return holds / len(self.decision_log)

    def get_statistics(self) -> Dict[str, Any]:
        """Get engine performance statistics."""
        total = len(self.decision_log)
        if total == 0:
            return {
                'total_decisions': 0,
                'proceed_count': 0,
                'hold_count': 0,
                'refuse_count': 0,
                'epistemic_hold_rate': 0.0,
                'target_hold_rate': self.epistemic_hold_rate_target,
                'average_confidence': 0.0
            }

        proceed = sum(
            1 for d in self.decision_log if d.state == TLState.PROCEED
        )
        hold = sum(
            1 for d in self.decision_log if d.state == TLState.EPISTEMIC_HOLD
        )
        refuse = sum(
            1 for d in self.decision_log if d.state == TLState.REFUSE
        )
        avg_conf = sum(d.confidence for d in self.decision_log) / total

        return {
            'total_decisions': total,
            'proceed_count': proceed,
            'hold_count': hold,
            'refuse_count': refuse,
            'proceed_rate': proceed / total,
            'epistemic_hold_rate': hold / total,
            'refuse_rate': refuse / total,
            'target_hold_rate': self.epistemic_hold_rate_target,
            'average_confidence': avg_conf,
            'unresolved_holds': sum(
                1 for e in self.epistemic_holds if not e.resolution_action
            )
        }

    def export_audit_trail(self, filepath: str):
        """Export complete audit trail to JSON file."""
        audit_data = {
            'engine_config': {
                'proceed_threshold': self.proceed_threshold,
                'hold_threshold': self.hold_threshold,
                'target_hold_rate': self.epistemic_hold_rate_target
            },
            'statistics': self.get_statistics(),
            'decision_log': [d.to_dict() for d in self.decision_log],
            'epistemic_holds': [e.to_dict() for e in self.epistemic_holds],
            'export_timestamp': datetime.utcnow().isoformat()
        }
        with open(filepath, 'w') as f:
            json.dump(audit_data, f, indent=2)
        logger.info(f"Audit trail exported to {filepath}")


class TLDecorator:
    """Decorator for wrapping economic decision functions with TL logic."""

    def __init__(self, engine: TLEngine):
        self.engine = engine

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, tuple):
                if len(result) == 2:
                    confidence, reasoning = result
                    metadata = {}
                elif len(result) == 3:
                    confidence, reasoning, metadata = result
                else:
                    raise ValueError(
                        "Function must return (confidence, reasoning) or "
                        "(confidence, reasoning, metadata)"
                    )
            else:
                raise ValueError("Function must return tuple")
            return self.engine.evaluate(confidence, reasoning, metadata)
        return wrapper


def calculate_confidence(
    data_sources: List[Dict[str, Any]],
    models: List[Any] = None
) -> float:
    """
    Calculate composite confidence score from multiple factors.

    Each factor weighted at 25%:
    - Data Quality: completeness, freshness, verification
    - Model Agreement: consensus across models, low variance
    - Historical Accuracy: recent success rate (90-day)
    - Signal Strength: clear indicators, low noise

    Returns a score in [0.0, 1.0]. This score is an input to
    TLEngine.evaluate(). Whether it produces PROCEED, EPISTEMIC_HOLD,
    or REFUSE depends on the institution-calibrated thresholds set at
    TLEngine initialization. This function has no knowledge of those values.
    """
    data_quality = (
        sum(s.get('quality', 0.5) for s in data_sources)
        / max(len(data_sources), 1)
    )

    if models and len(models) > 1:
        outputs = [m.get('output', 0.5) for m in models]
        mean = sum(outputs) / len(outputs)
        variance = sum((o - mean) ** 2 for o in outputs) / len(outputs)
        model_agreement = max(0.0, 1.0 - variance)
    else:
        model_agreement = 0.5

    historical_accuracy = (
        data_sources[0].get('historical_accuracy', 0.75)
        if data_sources else 0.5
    )

    signal_strength = (
        sum(s.get('signal_strength', 0.5) for s in data_sources)
        / max(len(data_sources), 1)
    )

    confidence = 0.25 * (
        data_quality + model_agreement + historical_accuracy + signal_strength
    )
    return max(0.0, min(1.0, confidence))


def analyze_uncertainty(
    data_sources: List[Dict[str, float]],
    conflict_threshold: float = 0.3
) -> Dict[str, Any]:
    """Analyze uncertainty across multiple data sources."""
    if not data_sources:
        return {
            'average_confidence': 0.0,
            'confidence_variance': 0.0,
            'has_conflicts': False,
            'conflicts': []
        }

    confidences = [src['confidence'] for src in data_sources]
    avg = sum(confidences) / len(confidences)
    variance = sum((c - avg) ** 2 for c in confidences) / len(confidences)

    conflicts = []
    for i, src1 in enumerate(data_sources):
        for src2 in data_sources[i + 1:]:
            diff = abs(src1['confidence'] - src2['confidence'])
            if diff >= conflict_threshold:
                conflicts.append({
                    'sources': [src1['name'], src2['name']],
                    'difference': diff,
                    'values': [src1['confidence'], src2['confidence']]
                })

    return {
        'average_confidence': avg,
        'confidence_variance': variance,
        'has_conflicts': len(conflicts) > 0,
        'conflicts': conflicts,
        'source_count': len(data_sources)
    }


def verify_mandate(mandate_type: str, data: Dict[str, Any]) -> TLValue:
    """
    Verify Economic Rights or Sustainable Capital mandates.
    Automatic EPISTEMIC_HOLD on any verification failure.

    Mandate checks are binary pass/fail and override confidence scores.
    Even a confidence score of 1.0 does not prevent an Epistemic Hold
    if a mandate check fails. This is intentional and constitutional.
    """
    if mandate_type == 'economic_rights':
        checks = {
            'ownership_verified': data.get('ownership_verified', False),
            'consent_obtained': data.get('consent_obtained', False),
            'provenance_signed': data.get('provenance_signed', False),
            'regulatory_access': data.get('regulatory_access', False)
        }
    elif mandate_type == 'sustainable_capital':
        checks = {
            'esg_verified': data.get('esg_verified', False),
            'emissions_anchored': data.get('emissions_anchored', False),
            'use_of_proceeds_tracked': data.get('use_of_proceeds_tracked', False)
        }
    else:
        raise ValueError(f"Unknown mandate type: {mandate_type}")

    if not all(checks.values()):
        failed = [k for k, v in checks.items() if not v]
        return TLValue(
            state=TLState.EPISTEMIC_HOLD,
            confidence=0.0,
            reasoning=f"{mandate_type} mandate failed: {failed}",
            metadata={'failed_checks': failed, 'mandate': mandate_type}
        )

    return TLValue(
        state=TLState.PROCEED,
        confidence=1.0,
        reasoning=f"{mandate_type} verified"
    )


# ---------------------------------------------------------------------------
# DEMONSTRATION SCAFFOLD
# The block below runs only when this file is executed directly as a script:
#   python src/core.py
# It never runs when core.py is imported as a module.
# The threshold values below are SAMPLE VALUES FOR DEMONSTRATION ONLY.
# They are not recommendations, defaults, or standards.
# Every production deployment must establish its own calibrated values.
# See docs/Threshold_Calibration.md.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    _DEMO_PROCEED = 0.85  # SAMPLE ONLY - not a framework default
    _DEMO_HOLD = 0.40     # SAMPLE ONLY - not a framework default

    print("=" * 60)
    print("DEMONSTRATION MODE - sample thresholds, not production values")
    print(f"proceed_threshold={_DEMO_PROCEED}, hold_threshold={_DEMO_HOLD}")
    print("=" * 60)

    engine = TLEngine(
        proceed_threshold=_DEMO_PROCEED,
        hold_threshold=_DEMO_HOLD,
        epistemic_hold_rate_target=0.20
    )

    d1 = engine.evaluate(
        0.92,
        "Strong market signals, all indicators align",
        {'asset': 'BTC', 'signal_sources': 3}
    )
    print(f"\nDecision 1: {d1.state.name} (confidence: {d1.confidence})")

    d2 = engine.evaluate(
        0.65,
        "Conflicting signals between technical and fundamental analysis",
        {'asset': 'ETH', 'conflicts': ['Technical bearish', 'Fundamental bullish']}
    )
    print(f"\nDecision 2: {d2.state.name} (confidence: {d2.confidence})")

    d3 = engine.evaluate(
        0.25,
        "Market data incomplete, liquidity concerns",
        {'asset': 'XRP'}
    )
    print(f"\nDecision 3: {d3.state.name} (confidence: {d3.confidence})")

    if engine.epistemic_holds:
        engine.resolve_hold(
            engine.epistemic_holds[0].event_id,
            "Additional analysis completed"
        )

    print("\n" + "=" * 60)
    print("ENGINE STATISTICS")
    print("=" * 60)
    for key, value in engine.get_statistics().items():
        print(
            f"{key}: {value:.3f}"
            if isinstance(value, float)
            else f"{key}: {value}"
        )

"""
---
Creator: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Email: leogouk@gmail.com
Repository: https://github.com/FractonicMind/TernaryLogic
Support: support@tl-goukassian.org
---
"""
