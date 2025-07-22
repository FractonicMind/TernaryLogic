"""
Core Ternary Logic Implementation
Goukassian Framework - Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com

This module implements the fundamental ternary logic system that enables
intelligent decision-making under uncertainty.
"""

from enum import Enum
from typing import Union, Optional, List, Dict, Any
from dataclasses import dataclass
import numpy as np

class TernaryState(Enum):
    """Three states of ternary logic according to Goukassian Framework"""
    TRUE = 1
    FALSE = 0
    INDETERMINATE = -1
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"TernaryState.{self.name}"

@dataclass
class TernaryResult:
    """Result of a ternary decision with full context and recommendations"""
    state: TernaryState
    confidence: float
    reasoning: str
    next_steps: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __str__(self):
        return f"TernaryResult(state={self.state}, confidence={self.confidence:.2f})"

class TernaryValue:
    """
    Core ternary value with uncertainty handling
    
    This class represents a single ternary value with associated confidence,
    implementing the Sacred Pause principle when uncertainty is high.
    """
    
    def __init__(self, value: Union[float, int, None], confidence: float = 1.0):
        """
        Initialize a ternary value
        
        Args:
            value: The numeric value (None indicates missing/unknown data)
            confidence: Confidence level (0.0 to 1.0)
        """
        self.value = value
        self.confidence = max(0.0, min(1.0, confidence))
        
    @property
    def state(self) -> TernaryState:
        """Determine ternary state based on value and confidence"""
        if self.value is None or self.confidence < 0.5:
            return TernaryState.INDETERMINATE
        elif self.value > 0:
            return TernaryState.TRUE
        else:
            return TernaryState.FALSE
    
    def __and__(self, other: 'TernaryValue') -> 'TernaryValue':
        """Ternary AND operation - Goukassian implementation"""
        if self.state == TernaryState.FALSE or other.state == TernaryState.FALSE:
            return TernaryValue(0, min(self.confidence, other.confidence))
        elif self.state == TernaryState.INDETERMINATE or other.state == TernaryState.INDETERMINATE:
            return TernaryValue(None, min(self.confidence, other.confidence))
        else:
            return TernaryValue(1, min(self.confidence, other.confidence))
    
    def __or__(self, other: 'TernaryValue') -> 'TernaryValue':
        """Ternary OR operation - Goukassian implementation"""
        if self.state == TernaryState.TRUE or other.state == TernaryState.TRUE:
            return TernaryValue(1, max(self.confidence, other.confidence))
        elif self.state == TernaryState.INDETERMINATE or other.state == TernaryState.INDETERMINATE:
            return TernaryValue(None, max(self.confidence, other.confidence))
        else:
            return TernaryValue(0, max(self.confidence, other.confidence))
    
    def __invert__(self) -> 'TernaryValue':
        """Ternary NOT operation - Goukassian implementation"""
        if self.state == TernaryState.INDETERMINATE:
            return TernaryValue(None, self.confidence)
        else:
            return TernaryValue(-self.value if self.value is not None else None, self.confidence)

class TernaryLogicEngine:
    """
    Main engine for ternary decision-making according to Goukassian Framework
    
    This engine implements the Sacred Pause principle: when confidence is below
    threshold, return INDETERMINATE rather than forcing a binary decision.
    """
    
    def __init__(self, confidence_threshold: float = 0.7):
        """
        Initialize the ternary logic engine
        
        Args:
            confidence_threshold: Minimum confidence required for TRUE/FALSE decisions
        """
        self.confidence_threshold = confidence_threshold
        
    def evaluate(self, 
                criteria: Dict[str, Union[float, None]], 
                weights: Optional[Dict[str, float]] = None) -> TernaryResult:
        """
        Evaluate multiple criteria using ternary logic
        
        This method implements the core Goukassian Framework logic for handling
        uncertainty in multi-criteria decision-making.
        
        Args:
            criteria: Dict of criterion_name -> value (None indicates missing data)
            weights: Optional weights for each criterion
            
        Returns:
            TernaryResult with decision and comprehensive metadata
        """
        
        if weights is None:
            weights = {k: 1.0 for k in criteria.keys()}
            
        # Convert to ternary values
        ternary_values = []
        missing_data = []
        
        for criterion, value in criteria.items():
            if value is None:
                missing_data.append(criterion)
                ternary_values.append(TernaryValue(None, 0.0))
            else:
                # Confidence based on data quality (can be enhanced with domain knowledge)
                confidence = 1.0 if abs(value) > 0.5 else 0.6
                ternary_values.append(TernaryValue(value, confidence))
        
        # Weighted aggregation following Goukassian principles
        total_weight = sum(weights.values())
        weighted_sum = 0
        weighted_confidence = 0
        
        for (criterion, tv), weight in zip(zip(criteria.keys(), ternary_values), weights.values()):
            if tv.value is not None:
                weighted_sum += tv.value * weight
                weighted_confidence += tv.confidence * weight
        
        if total_weight > 0:
            avg_value = weighted_sum / total_weight
            avg_confidence = weighted_confidence / total_weight
        else:
            avg_value = 0
            avg_confidence = 0
            
        # Apply Sacred Pause principle - don't force decisions with low confidence
        final_value = TernaryValue(avg_value, avg_confidence)
        
        # Override to INDETERMINATE if below confidence threshold
        if avg_confidence < self.confidence_threshold:
            final_state = TernaryState.INDETERMINATE
        else:
            final_state = final_value.state
            
        # Generate reasoning and next steps
        reasoning = self._generate_reasoning(criteria, final_value, missing_data, final_state)
        next_steps = self._generate_next_steps(final_state, missing_data, avg_confidence)
        
        return TernaryResult(
            state=final_state,
            confidence=avg_confidence,
            reasoning=reasoning,
            next_steps=next_steps,
            metadata={
                'missing_data': missing_data,
                'weighted_average': avg_value,
                'confidence_threshold': self.confidence_threshold,
                'criteria_count': len(criteria),
                'missing_count': len(missing_data)
            }
        )
    
    def _generate_reasoning(self, criteria: Dict, final_value: TernaryValue, 
                          missing_data: List[str], final_state: TernaryState) -> str:
        """Generate human-readable reasoning for the decision"""
        
        if final_state == TernaryState.INDETERMINATE:
            if missing_data:
                return (f"Sacred Pause activated: Insufficient data for confident decision. "
                       f"Missing critical information: {', '.join(missing_data)}. "
                       f"Confidence ({final_value.confidence:.2f}) below threshold "
                       f"({self.confidence_threshold:.2f}).")
            else:
                return (f"Sacred Pause activated: Conflicting signals result in low confidence "
                       f"({final_value.confidence:.2f} < {self.confidence_threshold:.2f}). "
                       f"Additional analysis recommended before proceeding.")
        elif final_state == TernaryState.TRUE:
            return (f"High confidence decision: Positive signals outweigh negatives "
                   f"(confidence: {final_value.confidence:.2f} ≥ {self.confidence_threshold:.2f}).")
        else:
            return (f"High confidence decision: Negative signals outweigh positives "
                   f"(confidence: {final_value.confidence:.2f} ≥ {self.confidence_threshold:.2f}).")
    
    def _generate_next_steps(self, final_state: TernaryState, missing_data: List[str], 
                           confidence: float) -> List[str]:
        """Generate actionable next steps based on the decision"""
        
        if final_state == TernaryState.INDETERMINATE:
            steps = []
            if missing_data:
                steps.append(f"Priority: Gather missing data for {', '.join(missing_data[:3])}")
                if len(missing_data) > 3:
                    steps.append(f"Also collect data for {len(missing_data)-3} additional criteria")
            
            steps.extend([
                "Establish monitoring system for key indicators",
                "Set trigger conditions for re-evaluation",
                f"Re-evaluate when confidence exceeds {self.confidence_threshold:.2f}",
                "Consider consulting domain experts for missing information"
            ])
            return steps
        else:
            return [
                "Proceed with decision implementation",
                "Establish monitoring for changing conditions", 
                "Set up periodic re-evaluation schedule",
                "Document decision rationale for future reference"
            ]

class TernaryDecisionEngine(TernaryLogicEngine):
    """
    Specialized decision engine with additional decision support features
    
    This class extends TernaryLogicEngine with practical features for
    real-world decision-making scenarios.
    """
    
    def __init__(self, confidence_threshold: float = 0.7, domain: str = "general"):
        """
        Initialize the decision engine
        
        Args:
            confidence_threshold: Minimum confidence for TRUE/FALSE decisions  
            domain: Domain context (e.g., 'financial', 'medical', 'policy')
        """
        super().__init__(confidence_threshold)
        self.domain = domain
        self.decision_history = []
        
    def decide(self, criteria: Dict[str, Union[float, None]], 
              weights: Optional[Dict[str, float]] = None,
              context: Optional[str] = None) -> TernaryResult:
        """
        Make a decision using the Goukassian Framework
        
        This is the main method for practical decision-making, implementing
        the Sacred Pause principle with full documentation and history.
        
        Args:
            criteria: Decision criteria with values or None for missing data
            weights: Optional importance weights for criteria
            context: Optional context description for this decision
            
        Returns:
            TernaryResult with decision, confidence, and recommendations
        """
        
        result = self.evaluate(criteria, weights)
        
        # Enhance result with domain-specific information
        if self.domain == "financial":
            result = self._enhance_financial_result(result, criteria)
        elif self.domain == "medical":
            result = self._enhance_medical_result(result, criteria)
        elif self.domain == "policy":
            result = self._enhance_policy_result(result, criteria)
            
        # Store in decision history
        decision_record = {
            'criteria': criteria,
            'weights': weights,
            'context': context,
            'result': result,
            'domain': self.domain
        }
        self.decision_history.append(decision_record)
        
        return result
    
    def _enhance_financial_result(self, result: TernaryResult, 
                                criteria: Dict[str, Union[float, None]]) -> TernaryResult:
        """Enhance result with financial domain knowledge"""
        if result.state == TernaryState.INDETERMINATE:
            financial_steps = [
                "Consider market volatility and liquidity conditions",
                "Review risk management protocols",
                "Consult market data providers for additional signals"
            ]
            result.next_steps.extend(financial_steps)
        return result
    
    def _enhance_medical_result(self, result: TernaryResult,
                              criteria: Dict[str, Union[float, None]]) -> TernaryResult:
        """Enhance result with medical domain knowledge"""
        if result.state == TernaryState.INDETERMINATE:
            medical_steps = [
                "Order additional diagnostic tests",
                "Consult specialist colleagues",
                "Review patient history for additional context"
            ]
            result.next_steps.extend(medical_steps)
        return result
    
    def _enhance_policy_result(self, result: TernaryResult,
                             criteria: Dict[str, Union[float, None]]) -> TernaryResult:
        """Enhance result with policy domain knowledge"""
        if result.state == TernaryState.INDETERMINATE:
            policy_steps = [
                "Conduct stakeholder consultation",
                "Review policy precedents and case studies", 
                "Assess potential unintended consequences"
            ]
            result.next_steps.extend(policy_steps)
        return result
    
    def get_decision_summary(self) -> Dict[str, Any]:
        """Get summary statistics of decision-making history"""
        if not self.decision_history:
            return {"total_decisions": 0}
            
        states = [record['result'].state for record in self.decision_history]
        state_counts = {state: states.count(state) for state in TernaryState}
        
        confidences = [record['result'].confidence for record in self.decision_history]
        avg_confidence = np.mean(confidences) if confidences else 0.0
        
        return {
            "total_decisions": len(self.decision_history),
            "state_distribution": {state.name: count for state, count in state_counts.items()},
            "average_confidence": avg_confidence,
            "indeterminate_rate": state_counts[TernaryState.INDETERMINATE] / len(self.decision_history),
            "domain": self.domain,
            "confidence_threshold": self.confidence_threshold
        }
