"""
Goukassian Framework - Central Banking Policy Analysis
Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com

This example demonstrates how the Ternary Logic framework can enhance
Federal Reserve monetary policy decisions by formally recognizing uncertainty
and implementing graduated policy responses.

"The Sacred Pause guides monetary policy when data contradicts itself."
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

# Import Goukassian Framework
from goukassian import TernaryDecisionEngine, TernaryState
from goukassian.core import TernaryResult

class FederalReservePolicyEngine:
    """
    Federal Reserve Policy Analysis using Ternary Logic
    
    This engine demonstrates how the Sacred Pause principle applies to
    monetary policy decisions when economic indicators are contradictory
    or uncertain.
    """
    
    def __init__(self, 
                 confidence_threshold: float = 0.70,
                 inflation_target: float = 0.02,
                 unemployment_target: float = 0.04):
        """
        Initialize the Fed Policy Engine
        
        Args:
            confidence_threshold: Minimum confidence for policy changes
            inflation_target: Fed's inflation target (2%)
            unemployment_target: Natural rate of unemployment estimate
        """
        self.engine = TernaryDecisionEngine(
            confidence_threshold=confidence_threshold,
            domain="policy"
        )
        self.inflation_target = inflation_target
        self.unemployment_target = unemployment_target
        
        # Policy state tracking
        self.current_fed_funds_rate = 0.05  # 5.0%
        self.policy_history = []
        self.pause_history = []  # Track Sacred Pause activations
        
        # Economic forecasting
        self.forecast_horizon = 8  # 8 quarters ahead
        
    def analyze_economic_indicators(self, economic_data: Dict) -> Dict[str, float]:
        """
        Analyze economic indicators for monetary policy implications
        
        Returns dictionary with policy-relevant signals or None for missing data
        """
        indicators = {}
        
        # Core Inflation Indicators
        if 'core_pce_inflation' in economic_data:
            indicators['inflation_trend'] = self._analyze_inflation_trend(
                economic_data['core_pce_inflation']
            )
        else:
            indicators['inflation_trend'] = None
            
        if 'inflation_expectations' in economic_data:
            indicators['inflation_expectations'] = self._analyze_inflation_expectations(
                economic_data['inflation_expectations']
            )
        else:
            indicators['inflation_expectations'] = None
            
        # Labor Market Indicators
        if 'unemployment_rate' in economic_data:
            indicators['labor_market_strength'] = self._analyze_labor_market(
                economic_data['unemployment_rate'],
                economic_data.get('job_openings', None)
            )
        else:
            indicators['labor_market_strength'] = None
            
        # Economic Growth Indicators
        if 'gdp_growth' in economic_data:
            indicators['economic_momentum'] = self._analyze_economic_growth(
                economic_data['gdp_growth']
            )
        else:
            indicators['economic_momentum'] = None
            
        # Financial Conditions
        if 'financial_conditions_index' in economic_data:
            indicators['financial_conditions'] = self._analyze_financial_conditions(
                economic_data['financial_conditions_index']
            )
        else:
            indicators['financial_conditions'] = None
            
        # Global Economic Conditions
        if 'global_growth' in economic_data:
            indicators['global_conditions'] = self._analyze_global_conditions(
                economic_data['global_growth'],
                economic_data.get('trade_tensions', None)
            )
        else:
            indicators['global_conditions'] = None
            
        # Financial Stability Indicators
        if 'credit_spreads' in economic_data:
            indicators['financial_stability'] = self._analyze_financial_stability(
                economic_data['credit_spreads'],
                economic_data.get('asset_valuations', None)
            )
        else:
            indicators['financial_stability'] = None
            
        return indicators
    
    def make_policy_decision(self, 
                           economic_data: Dict,
                           policy_options: Dict = None) -> TernaryResult:
        """
        Make monetary policy decision using Ternary Logic framework
        
        Args:
            economic_data: Economic indicators dictionary
            policy_options: Available policy actions (optional)
            
        Returns:
            TernaryResult with policy recommendation and reasoning
        """
        
        # Analyze economic indicators
        indicators = self.analyze_economic_indicators(economic_data)
        
        # Define indicator weights based on current economic conditions
        weights = self._get_policy_weights(economic_data)
        
        # Apply Fed mandate priorities (dual mandate focus)
        mandate_adjusted_indicators = self._apply_dual_mandate_focus(indicators, economic_data)
        
        # Make decision using Ternary Logic
        decision = self.engine.decide(
            criteria=mandate_adjusted_indicators,
            weights=weights,
            context="Federal Reserve monetary policy decision"
        )
        
        # Enhance decision with policy-specific information
        decision = self._enhance_policy_decision(decision, economic_data, indicators)
        
        # Log decision for FOMC records
        self._log_policy_decision(decision, indicators, economic_data)
        
        return decision
    
    def generate_policy_statement(self, 
                                decision: TernaryResult, 
                                economic_data: Dict) -> Dict:
        """
        Generate FOMC-style policy statement based on Ternary Logic decision
        
        Returns structured policy communication
        """
        
        statement = {
            'decision_date': datetime.now().strftime('%Y-%m-%d'),
            'policy_action': self._translate_decision_to_action(decision),
            'fed_funds_target': self._calculate_new_fed_funds_rate(decision),
            'vote': self._generate_committee_vote(decision),
            'economic_assessment': self._generate_economic_assessment(economic_data),
            'policy_rationale': decision.reasoning,
            'forward_guidance': self._generate_forward_guidance(decision),
            'uncertainty_acknowledgment': self._generate_uncertainty_statement(decision)
        }
        
        if decision.state == TernaryState.INDETERMINATE:
            statement.update({
                'sacred_pause_explanation': self._explain_policy_pause(decision),
                'data_monitoring_plan': decision.next_steps,
                'next_evaluation_timeline': self._determine_next_evaluation(decision)
            })
            
        return statement
    
    def _analyze_inflation_trend(self, inflation_data: List[float]) -> Optional[float]:
        """Analyze inflation trend relative to Fed target"""
        if len(inflation_data) < 4:
            return None
            
        recent_inflation = np.mean(inflation_data[-3:])  # Last 3 months
        trend = np.polyfit(range(len(inflation_data)), inflation_data, 1)[0]
        
        # Signal strength based on deviation from target and trend
        target_deviation = (recent_inflation - self.inflation_target) / self.inflation_target
        trend_component = trend * 12  # Annualize monthly trend
        
        # Combine deviation and trend (positive = tighten, negative = ease)
        signal = (target_deviation * 0.7) + (trend_component * 0.3)
        return np.clip(signal * 2, -1, 1)
    
    def _analyze_inflation_expectations(self, expectations_data: Dict) -> Optional[float]:
        """Analyze inflation expectations anchoring"""
        if 'five_year_forward' not in expectations_data:
            return None
            
        five_year_expectation = expectations_data['five_year_forward']
        target_deviation = (five_year_expectation - self.inflation_target) / self.inflation_target
        
        # Check for anchoring (expectations close to target)
        if abs(target_deviation) < 0.1:  # Within 10% of target
            return 0  # Well-anchored
        elif target_deviation > 0:
            return target_deviation * 2  # Above target - tighten
        else:
            return target_deviation * 2  # Below target - ease
    
    def _analyze_labor_market(self, unemployment_rate: float, job_openings: Optional[float]) -> Optional[float]:
        """Analyze labor market strength"""
        
        # Unemployment gap (negative = below natural rate = tight labor market)
        unemployment_gap = (unemployment_rate - self.unemployment_target) / self.unemployment_target
        
        signal = -unemployment_gap  # Negative gap suggests tightening needed
        
        # Enhance with job openings if available
        if job_openings is not None:
            # High job openings relative to unemployment suggests tight market
            openings_to_unemployed = job_openings / unemployment_rate if unemployment_rate > 0 else 0
            if openings_to_unemployed > 1.5:  # More openings than unemployed
                signal += 0.3  # Additional tightening signal
            elif openings_to_unemployed < 0.8:
                signal -= 0.3  # Additional easing signal
                
        return np.clip(signal, -1, 1)
    
    def _analyze_economic_growth(self, gdp_growth: List[float]) -> Optional[float]:
        """Analyze economic growth momentum"""
        if len(gdp_growth) < 2:
            return None
            
        recent_growth = np.mean(gdp_growth[-2:])  # Last 2 quarters
        trend_growth = 0.025  # Assume 2.5% trend growth
        
        growth_gap = (recent_growth - trend_growth) / trend_growth
        
        # Strong growth above trend suggests tightening, weak growth suggests easing
        return np.clip(growth_gap, -1, 1)
    
    def _analyze_financial_conditions(self, fci: float) -> Optional[float]:
        """Analyze financial conditions index"""
        # FCI typically normalized around 0
        # Positive = tighter conditions, Negative = easier conditions
        
        # If conditions are already tight, less need for monetary tightening
        # If conditions are easy, more room for monetary tightening
        signal = -fci / 2  # Invert FCI for policy signal
        return np.clip(signal, -1, 1)
    
    def _analyze_global_conditions(self, global_growth: float, trade_tensions: Optional[float]) -> Optional[float]:
        """Analyze global economic conditions"""
        
        global_trend = 0.03  # Assume 3% global trend growth
        growth_signal = (global_growth - global_trend) / global_trend
        
        # Adjust for trade tensions if available
        if trade_tensions is not None:
            # High trade tensions create downside risks
            tension_adjustment = -trade_tensions * 0.5
            growth_signal += tension_adjustment
            
        # Strong global growth supports tightening, weak growth suggests caution
        return np.clip(growth_signal, -1, 1)
    
    def _analyze_financial_stability(self, credit_spreads: float, asset_valuations: Optional[float]) -> Optional[float]:
        """Analyze financial stability indicators"""
        
        # Wide credit spreads suggest financial stress (negative for tightening)
        spread_signal = -credit_spreads * 2
        
        # High asset valuations might suggest bubble risk (positive for tightening)
        valuation_signal = 0
        if asset_valuations is not None:
            valuation_signal = asset_valuations * 0.5
            
        combined_signal = (spread_signal * 0.7) + (valuation_signal * 0.3)
        return np.clip(combined_signal, -1, 1)
    
    def _get_policy_weights(self, economic_data: Dict) -> Dict[str, float]:
        """Determine indicator weights based on current economic conditions"""
        
        base_weights = {
            'inflation_trend': 0.25,          # Core to Fed mandate
            'inflation_expectations': 0.20,   # Critical for credibility
            'labor_market_strength': 0.20,    # Other half of dual mandate
            'economic_momentum': 0.15,        # Growth considerations
            'financial_conditions': 0.10,     # Policy transmission
            'global_conditions': 0.05,        # External factors
            'financial_stability': 0.05       # Systemic risk
        }
        
        # Adjust weights based on economic regime
        if economic_data.get('inflation_regime') == 'high':
            base_weights['inflation_trend'] *= 1.3
            base_weights['inflation_expectations'] *= 1.2
            base_weights['labor_market_strength'] *= 0.8
        elif economic_data.get('inflation_regime') == 'low':
            base_weights['labor_market_strength'] *= 1.2
            base_weights['economic_momentum'] *= 1.1
            
        return base_weights
    
    def _apply_dual_mandate_focus(self, indicators: Dict, economic_data: Dict) -> Dict:
        """Apply Federal Reserve dual mandate focus to indicators"""
        
        dual_mandate_adjusted = indicators.copy()
        
        # If both inflation and unemployment suggest same direction, strengthen signal
        inflation_signal = indicators.get('inflation_trend', 0) or 0
        labor_signal = indicators.get('labor_market_strength', 0) or 0
        
        if inflation_signal * labor_signal > 0:  # Same sign
            # Both suggest same policy direction - strengthen signals
            if 'inflation_trend' in dual_mandate_adjusted and dual_mandate_adjusted['inflation_trend'] is not None:
                dual_mandate_adjusted['inflation_trend'] *= 1.2
            if 'labor_market_strength' in dual_mandate_adjusted and dual_mandate_adjusted['labor_market_strength'] is not None:
                dual_mandate_adjusted['labor_market_strength'] *= 1.2
        elif inflation_signal * labor_signal < 0:  # Opposite signs
            # Conflicting mandate signals - this creates uncertainty
            if 'inflation_trend' in dual_mandate_adjusted and dual_mandate_adjusted['inflation_trend'] is not None:
                dual_mandate_adjusted['inflation_trend'] *= 0.7
            if 'labor_market_strength' in dual_mandate_adjusted and dual_mandate_adjusted['labor_market_strength'] is not None:
                dual_mandate_adjusted['labor_market_strength'] *= 0.7
                
        return dual_mandate_adjusted
    
    def _enhance_policy_decision(self, 
                               decision: TernaryResult, 
                               economic_data: Dict,
                               indicators: Dict) -> TernaryResult:
        """Enhance decision with Fed-specific context"""
        
        if decision.state == TernaryState.INDETERMINATE:
            # Add Fed-specific guidance for Sacred Pause
            fed_steps = [
                "Await additional employment and inflation data",
                "Monitor financial market conditions for stability",
                "Assess global economic developments and risks",
                "Evaluate effectiveness of current policy stance",
                "Consider communication strategy for uncertainty"
            ]
            decision.next_steps.extend(fed_steps)
            
        # Add Fed metadata
        if decision.metadata is None:
            decision.metadata = {}
            
        decision.metadata.update({
            'current_fed_funds_rate': self.current_fed_funds_rate,
            'inflation_target': self.inflation_target,
            'missing_indicators': [k for k, v in indicators.items() if v is None],
            'indicator_count': len([v for v in indicators.values() if v is not None]),
            'dual_mandate_conflict': self._assess_mandate_conflict(indicators)
        })
        
        return decision
    
    def _assess_mandate_conflict(self, indicators: Dict) -> bool:
        """Assess if dual mandate objectives are in conflict"""
        
        inflation_signal = indicators.get('inflation_trend', 0) or 0
        labor_signal = indicators.get('labor_market_strength', 0) or 0
        
        # Conflict if signals have opposite signs and both are significant
        return (inflation_signal * labor_signal < 0 and 
                abs(inflation_signal) > 0.3 and 
                abs(labor_signal) > 0.3)
    
    def _translate_decision_to_action(self, decision: TernaryResult) -> str:
        """Translate ternary decision to Fed policy action"""
        
        if decision.state == TernaryState.TRUE:
            if decision.confidence > 0.8:
                return "Raise federal funds rate by 50 basis points"
            else:
                return "Raise federal funds rate by 25 basis points"
        elif decision.state == TernaryState.FALSE:
            if decision.confidence > 0.8:
                return "Lower federal funds rate by 50 basis points"
            else:
                return "Lower federal funds rate by 25 basis points"
        else:  # INDETERMINATE
            return "Maintain current federal funds rate target"
    
    def _generate_forward_guidance(self, decision: TernaryResult) -> str:
        """Generate forward guidance based on decision"""
        
        if decision.state == TernaryState.INDETERMINATE:
            return ("The Committee will continue to monitor economic developments " +
                   "and will adjust monetary policy as appropriate to achieve its " +
                   "dual mandate objectives. The timing and magnitude of future " +
                   "policy adjustments will depend on incoming data and their " +
                   "implications for the economic outlook.")
        elif decision.state == TernaryState.TRUE:
            return ("The Committee expects that ongoing increases in the target range " +
                   "will be appropriate to achieve the dual mandate objectives, " +
                   "with the timing and magnitude dependent on economic developments.")
        else:  # FALSE
            return ("The Committee expects that ongoing decreases in the target range " +
                   "may be appropriate to support employment and return inflation " +
                   "to the 2 percent objective over time.")
    
    def _explain_policy_pause(self, decision: TernaryResult) -> str:
        """Explain Sacred Pause in Fed communication style"""
        
        return ("The Committee determined that maintaining the current policy stance " +
               "is appropriate while assessing the cumulative effects of previous " +
               "policy adjustments and monitoring economic developments. This " +
               f"approach (confidence level: {decision.confidence:.1%}) reflects " +
               "the Committee's commitment to data-dependent policymaking and " +
               "prudent risk management in the face of economic uncertainty.")
    
    def _log_policy_decision(self, 
                           decision: TernaryResult, 
                           indicators: Dict,
                           economic_data: Dict):
        """Log decision for FOMC records"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'decision': decision.state.name,
            'confidence': decision.confidence,
            'indicators': {k: v for k, v in indicators.items() if v is not None},
            'missing_indicators': [k for k, v in indicators.items() if v is None],
            'reasoning': decision.reasoning,
            'current_fed_funds_rate': self.current_fed_funds_rate
        }
        
        # In production, this would write to secure Fed records system
        print(f"FOMC Decision Log: {json.dumps(log_entry, indent=2)}")

def demonstrate_fed_policy_analysis():
    """
    Demonstrate the Federal Reserve Policy Engine with realistic scenarios
    """
    
    print("🏛️  Federal Reserve Policy Analysis - Goukassian Framework")
    print("=" * 65)
    print()
    print("Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)")
    print("Contact: leogouk@gmail.com")
    print('"The Sacred Pause guides monetary policy when data contradicts itself."')
    print()
    
    # Initialize Fed policy engine
    fed_engine = FederalReservePolicyEngine(
        confidence_threshold=0.70,
        inflation_target=0.02,
        unemployment_target=0.04
    )
    
    # Scenario 1: Clear Tightening Signals
    print("📈 Scenario 1: Clear Tightening Environment")
    print("-" * 42)
    
    tightening_data = {
        'core_pce_inflation': [0.025, 0.027, 0.029, 0.031, 0.033],  # Rising inflation
        'inflation_expectations': {'five_year_forward': 0.028},      # Above target
        'unemployment_rate': 3.2,                                   # Below natural rate
        'job_openings': 11.5,                                      # High job openings
        'gdp_growth': [0.030, 0.035],                             # Strong growth
        'financial_conditions_index': -0.5,                        # Easy conditions
        'global_growth': 0.035,                                    # Strong global growth
        'credit_spreads': 0.8,                                     # Normal spreads
        'inflation_regime': 'high'
    }
    
    decision = fed_engine.make_policy_decision(tightening_data)
    statement = fed_engine.generate_policy_statement(decision, tightening_data)
    
    print(f"Policy Decision: {decision.state.name} (Confidence: {decision.confidence:.2f})")
    print(f"Action: {statement['policy_action']}")
    print(f"Reasoning: {decision.reasoning}")
    print(f"Forward Guidance: {statement['forward_guidance'][:100]}...")
    print()
    
    # Scenario 2: Conflicting Dual Mandate Signals
    print("⚠️  Scenario 2: Dual Mandate Conflict - Sacred Pause Likely")
    print("-" * 55)
    
    conflicting_data = {
        'core_pce_inflation': [0.015, 0.012, 0.011, 0.010],       # Below target, falling
        'inflation_expectations': {'five_year_forward': 0.018},    # Below target
        'unemployment_rate': 3.0,                                  # Very low (overheating?)
        'job_openings': 12.0,                                     # Very high
        'gdp_growth': [0.015, 0.010],                            # Slowing growth
        'financial_conditions_index': 1.2,                        # Tight conditions
        'global_growth': 0.020,                                   # Weak global growth
        'credit_spreads': 2.5,                                    # Widening spreads
        'trade_tensions': 0.7,                                    # High tensions
        'inflation_regime': 'low'
    }
    
    decision = fed_engine.make_policy_decision(conflicting_data)
    statement = fed_engine.generate_policy_statement(decision, conflicting_data)
    
    print(f"Policy Decision: {decision.state.name} (Confidence: {decision.confidence:.2f})")
    print(f"Action: {statement['policy_action']}")
    print(f"Reasoning: {decision.reasoning}")
    
    if decision.state == TernaryState.INDETERMINATE:
        print("Sacred Pause Explanation:")
        print(f"  {statement['sacred_pause_explanation']}")
        print("Data Monitoring Plan:")
        for i, step in enumerate(statement['data_monitoring_plan'][:3], 1):
            print(f"  {i}. {step}")
    print()
    
    # Scenario 3: Missing Critical Data
    print("❓ Scenario 3: Missing Critical Economic Data")
    print("-" * 44)
    
    incomplete_data = {
        'core_pce_inflation': None,                                # Missing inflation data!
        'inflation_expectations': None,                            # Missing expectations!
        'unemployment_rate': 4.1,                                 # Available
        'job_openings': None,                                     # Missing
        'gdp_growth': None,                                       # Missing growth data!
        'financial_conditions_index': 0.2,                        # Available
        'global_growth': None,                                    # Missing
        'credit_spreads': None                                    # Missing
    }
    
    decision = fed_engine.make_policy_decision(incomplete_data)
    statement = fed_engine.generate_policy_statement(decision, incomplete_data)
    
    print(f"Policy Decision: {decision.state.name} (Confidence: {decision.confidence:.2f})")
    print(f"Action: {statement['policy_action']}")
    print(f"Reasoning: {decision.reasoning}")
    
    if 'missing_indicators' in decision.metadata:
        missing = decision.metadata['missing_indicators']
        print(f"Missing Critical Data: {', '.join(missing)}")
        
    print()
    print("📊 Federal Reserve Decision Summary")
    print("-" * 35)
    print("The Goukassian Framework enables the Federal Reserve to:")
    print("• Acknowledge uncertainty honestly in policy communications")
    print("• Avoid overconfident policy moves with insufficient data")
    print("• Implement graduated responses based on confidence levels")
    print("• Maintain credibility by explaining the basis for policy pauses")
    print()
    print("As Lev Goukassian noted: 'Central banking is ultimately about")
    print("making the best possible decisions with imperfect information.'")

if __name__ == "__main__":
    demonstrate_fed_policy_analysis()
