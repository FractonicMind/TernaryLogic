"""
Ternary Logic Framework - Core Implementation
==============================================

A three-valued logic system for economic decision-making under uncertainty.

States:
    +1 (PROCEED): Execute action when conditions are clear and verified
     0 (EPISTEMIC_HOLD): Pause for deliberation when uncertainty exceeds thresholds
    -1 (HALT): Reject action when conditions definitively fail requirements

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


class TLState(Enum):
    """Three-valued logic states for economic decisions."""
    PROCEED = 1          # +1: Clear to execute
    EPISTEMIC_HOLD = 0   # 0: Pause for deliberation
    HALT = -1            # -1: Reject execution


class ConfidenceLevel(Enum):
    """Confidence levels for economic intelligence."""
    HIGH = "high"           # >= 0.85
    MEDIUM = "medium"       # 0.60 - 0.84
    LOW = "low"            # 0.40 - 0.59
    CRITICAL = "critical"  # < 0.40


@dataclass
class TLValue:
    """
    Ternary Logic value with metadata.
    
    Attributes:
        state: The TL state (PROCEED/EPISTEMIC_HOLD/HALT)
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
            raise ValueError(f"Confidence must be in [0.0, 1.0], got {self.confidence}")
    
    @property
    def confidence_level(self) -> ConfidenceLevel:
        """Get qualitative confidence level."""
        if self.confidence >= 0.85:
            return ConfidenceLevel.HIGH
        elif self.confidence >= 0.60:
            return ConfidenceLevel.MEDIUM
        elif self.confidence >= 0.40:
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
            'resolution_timestamp': self.resolution_timestamp.isoformat() if self.resolution_timestamp else None,
            'timestamp': self.timestamp.isoformat()
        }


class TLEngine:
    """Core Ternary Logic decision engine for economic intelligence."""
    
    def __init__(self, proceed_threshold=0.85, hold_threshold=0.40, epistemic_hold_rate_target=0.20):
        self.proceed_threshold = proceed_threshold
        self.hold_threshold = hold_threshold
        self.epistemic_hold_rate_target = epistemic_hold_rate_target
        self.epistemic_holds: List[EpistemicHoldEvent] = []
        self.decision_log: List[TLValue] = []
        logger.info(f"TL Engine initialized: PROCEED≥{proceed_threshold}, HALT<{hold_threshold}")
    
    def evaluate(self, confidence: float, reasoning: str, metadata: Optional[Dict[str, Any]] = None, 
                 force_state: Optional[TLState] = None) -> TLValue:
        """Evaluate economic conditions and return TL state."""
        if force_state:
            state = force_state
        else:
            if confidence >= self.proceed_threshold:
                state = TLState.PROCEED
            elif confidence < self.hold_threshold:
                state = TLState.HALT
            else:
                state = TLState.EPISTEMIC_HOLD
        
        value = TLValue(state=state, confidence=confidence, reasoning=reasoning, metadata=metadata or {})
        self.decision_log.append(value)
        
        if state == TLState.EPISTEMIC_HOLD:
            self._log_epistemic_hold(value)
        
        logger.info(f"TL Decision: {state.name} (confidence: {confidence:.3f})")
        return value
    
    def _log_epistemic_hold(self, value: TLValue):
        event = EpistemicHoldEvent(
            event_id="",
            trigger_reason=value.reasoning,
            data_inputs=value.metadata.get('inputs', {}),
            model_outputs=value.metadata.get('outputs', {}),
            signal_conflicts=value.metadata.get('conflicts', []),
            uncertainty_metrics={'confidence': value.confidence, 
                               'threshold_distance': abs(value.confidence - self.proceed_threshold)}
        )
        self.epistemic_holds.append(event)
        logger.warning(f"EPISTEMIC HOLD triggered: {event.event_id}")
    
    def resolve_hold(self, event_id: str, action: str):
        for event in self.epistemic_holds:
            if event.event_id == event_id:
                event.resolve(action)
                return
        raise ValueError(f"Epistemic Hold event {event_id} not found")
    
    @property
    def epistemic_hold_rate(self) -> float:
        if not self.decision_log:
            return 0.0
        holds = sum(1 for d in self.decision_log if d.state == TLState.EPISTEMIC_HOLD)
        return holds / len(self.decision_log)
    
    def get_statistics(self) -> Dict[str, Any]:
        total = len(self.decision_log)
        if total == 0:
            return {'total_decisions': 0, 'proceed_count': 0, 'hold_count': 0, 'halt_count': 0,
                   'epistemic_hold_rate': 0.0, 'target_hold_rate': self.epistemic_hold_rate_target, 
                   'average_confidence': 0.0}
        
        proceed = sum(1 for d in self.decision_log if d.state == TLState.PROCEED)
        hold = sum(1 for d in self.decision_log if d.state == TLState.EPISTEMIC_HOLD)
        halt = sum(1 for d in self.decision_log if d.state == TLState.HALT)
        avg_conf = sum(d.confidence for d in self.decision_log) / total
        
        return {
            'total_decisions': total, 'proceed_count': proceed, 'hold_count': hold, 'halt_count': halt,
            'proceed_rate': proceed/total, 'epistemic_hold_rate': hold/total, 'halt_rate': halt/total,
            'target_hold_rate': self.epistemic_hold_rate_target, 'average_confidence': avg_conf,
            'unresolved_holds': sum(1 for e in self.epistemic_holds if not e.resolution_action)
        }
    
    def export_audit_trail(self, filepath: str):
        audit_data = {
            'engine_config': {'proceed_threshold': self.proceed_threshold, 'hold_threshold': self.hold_threshold,
                            'target_hold_rate': self.epistemic_hold_rate_target},
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
                    raise ValueError("Function must return (confidence, reasoning) or (confidence, reasoning, metadata)")
            else:
                raise ValueError("Function must return tuple")
            return self.engine.evaluate(confidence, reasoning, metadata)
        return wrapper


def analyze_uncertainty(data_sources: List[Dict[str, float]], conflict_threshold=0.3) -> Dict[str, Any]:
    """Analyze uncertainty across multiple data sources."""
    if not data_sources:
        return {'average_confidence': 0.0, 'confidence_variance': 0.0, 'has_conflicts': False, 'conflicts': []}
    
    confidences = [src['confidence'] for src in data_sources]
    avg = sum(confidences) / len(confidences)
    variance = sum((c - avg) ** 2 for c in confidences) / len(confidences)
    
    conflicts = []
    for i, src1 in enumerate(data_sources):
        for src2 in data_sources[i+1:]:
            diff = abs(src1['confidence'] - src2['confidence'])
            if diff >= conflict_threshold:
                conflicts.append({'sources': [src1['name'], src2['name']], 'difference': diff,
                                'values': [src1['confidence'], src2['confidence']]})
    
    return {'average_confidence': avg, 'confidence_variance': variance, 
            'has_conflicts': len(conflicts) > 0, 'conflicts': conflicts, 'source_count': len(data_sources)}


# Example usage
if __name__ == "__main__":
    engine = TLEngine(proceed_threshold=0.85, hold_threshold=0.40, epistemic_hold_rate_target=0.20)
    
    d1 = engine.evaluate(0.92, "Strong market signals, all indicators align", {'asset': 'BTC', 'signal_sources': 3})
    print(f"\nDecision 1: {d1.state.name} (confidence: {d1.confidence})")
    
    d2 = engine.evaluate(0.65, "Conflicting signals between technical and fundamental analysis",
                        {'asset': 'ETH', 'conflicts': ['Technical bearish', 'Fundamental bullish']})
    print(f"\nDecision 2: {d2.state.name} (confidence: {d2.confidence})")
    
    d3 = engine.evaluate(0.25, "Market data incomplete, liquidity concerns", {'asset': 'XRP'})
    print(f"\nDecision 3: {d3.state.name} (confidence: {d3.confidence})")
    
    if engine.epistemic_holds:
        engine.resolve_hold(engine.epistemic_holds[0].event_id, "Additional analysis completed")
    
    print("\n" + "="*60)
    print("ENGINE STATISTICS")
    print("="*60)
    for key, value in engine.get_statistics().items():
        print(f"{key}: {value:.3f}" if isinstance(value, float) else f"{key}: {value}")

"""
---
Creator: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Email: leogouk@gmail.com
Repository: https://github.com/FractonicMind/TernaryLogic
Support: support@tl-goukassian.org
---
"""
