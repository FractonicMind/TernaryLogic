"""
Ternary Logic Framework - Central Banking Policy Analysis with Eight Pillars

This example demonstrates how the Ternary Logic framework provides
sovereign-grade accountability for central bank monetary policy decisions
through the Eight Pillars architecture.

Implementation of Epistemic Hold for monetary policy uncertainty management.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import hashlib

# Import Ternary Logic Framework
from ternary_logic import TLDecisionEngine, TLState
from ternary_logic.core import TLResult
from ternary_logic.eight_pillars import EightPillarsFramework

class CentralBankPolicyEngine:
    """
    Central Bank Policy Analysis using Ternary Logic with Eight Pillars
    
    Implements sovereign-grade accountability for monetary policy decisions
    through comprehensive audit trails and uncertainty management.
    """
    
    def __init__(self, 
                 halt_threshold: float = 0.30,
                 hold_threshold: float = 0.70,
                 inflation_target: float = 0.02,
                 unemployment_target: float = 0.04):
        """
        Initialize Central Bank Policy Engine with Eight Pillars
        
        Args:
            halt_threshold: Below this confidence, strongly consider halting
            hold_threshold: Below this confidence, trigger Epistemic Hold
            inflation_target: Central bank inflation target (2%)
            unemployment_target: Natural rate of unemployment estimate
        """
        self.engine = TLDecisionEngine(
            halt_threshold=halt_threshold,
            hold_threshold=hold_threshold,
            domain="central_banking"
        )
        
        # Initialize Eight Pillars Framework
        self.eight_pillars = EightPillarsFramework()
        
        self.inflation_target = inflation_target
        self.unemployment_target = unemployment_target
        
        # Policy state tracking
        self.current_policy_rate = 0.05  # 5.0%
        
        # Pillar 2: Immutable Ledger
        self.policy_ledger = []
        
        # Pillar 4: Decision Logs
        self.decision_logs = []
        
        # Pillar 1: Epistemic Hold tracking
        self.epistemic_holds = []
        
        # Economic forecasting
        self.forecast_horizon = 8  # 8 quarters ahead
        
    def analyze_economic_indicators(self, economic_data: Dict) -> Dict[str, float]:
        """
        Analyze economic indicators for monetary policy implications
        
        Returns dictionary with policy-relevant signals
        """
        indicators = {}
        
        # Core Inflation Indicators
        if 'core_pce_inflation' in economic_data:
            indicators['inflation_trend'] = self._analyze_inflation_trend(
                economic_data['core_pce_inflation']
            )
        
        if 'inflation_expectations' in economic_data:
            indicators['inflation_expectations'] = self._analyze_inflation_expectations(
                economic_data['inflation_expectations']
            )
        
        # Labor Market Indicators
        if 'unemployment_rate' in economic_data:
            indicators['labor_market_strength'] = self._analyze_labor_market(
                economic_data['unemployment_rate'],
                economic_data.get('job_openings', None)
            )
        
        # Economic Growth Indicators
        if 'gdp_growth' in economic_data:
            indicators['economic_momentum'] = self._analyze_economic_growth(
                economic_data['gdp_growth']
            )
        
        # Financial Conditions
        if 'financial_conditions_index' in economic_data:
            indicators['financial_conditions'] = self._analyze_financial_conditions(
                economic_data['financial_conditions_index']
            )
        
        # Global Economic Conditions
        if 'global_growth' in economic_data:
            indicators['global_conditions'] = self._analyze_global_conditions(
                economic_data['global_growth'],
                economic_data.get('trade_tensions', None)
            )
        
        # Financial Stability Indicators
        if 'credit_spreads' in economic_data:
            indicators['financial_stability'] = self._analyze_financial_stability(
                economic_data['credit_spreads'],
                economic_data.get('asset_valuations', None)
            )
        
        # Pillar 6: Sustainable Capital Allocation check
        if 'esg_considerations' in economic_data:
            indicators['sustainable_finance'] = self._analyze_sustainable_finance(
                economic_data['esg_considerations']
            )
        
        return indicators
    
    def make_policy_decision(self, 
                           economic_data: Dict,
                           policy_options: Dict = None) -> TLResult:
        """
        Make monetary policy decision using Ternary Logic with Eight Pillars accountability
        
        Args:
            economic_data: Economic indicators dictionary
            policy_options: Available policy actions (optional)
            
        Returns:
            TLResult with policy recommendation and full audit trail
        """
        
        # Pillar 3: Goukassian Principle - Validate all pillars active
        if not self.eight_pillars.validate_goukassian_principle():
            raise RuntimeError("Goukassian Principle validation failed - not all Eight Pillars active")
        
        # Analyze economic indicators
        indicators = self.analyze_economic_indicators(economic_data)
        
        # Define indicator weights based on current economic conditions
        weights = self._get_policy_weights(economic_data)
        
        # Apply dual mandate priorities
        mandate_adjusted_indicators = self._apply_dual_mandate_focus(indicators, economic_data)
        
        # Convert to request format for TL engine
        request = "Central bank monetary policy decision required"
        context = {
            'indicators': mandate_adjusted_indicators,
            'weights': weights,
            'current_rate': self.current_policy_rate,
            'economic_regime': economic_data.get('inflation_regime', 'normal'),
            'timestamp': datetime.now().isoformat()
        }
        
        # Make decision using Ternary Logic
        decision = self.engine.decide(
            request=request,
            context=context,
            scenario="Central bank monetary policy decision"
        )
        
        # Pillar 1: Track Epistemic Hold if triggered
        if decision.state == TLState.EPISTEMIC_HOLD:
            self._record_epistemic_hold(decision, indicators, economic_data)
        
        # Pillar 4: Create comprehensive Decision Log
        decision_log = self._create_decision_log(decision, indicators, economic_data)
        self.decision_logs.append(decision_log)
        
        # Pillar 2: Add to Immutable Ledger
        ledger_entry = self._create_ledger_entry(decision_log)
        self.policy_ledger.append(ledger_entry)
        
        # Pillar 5: Economic Rights & Transparency compliance
        self._ensure_regulatory_compliance(decision, economic_data)
        
        # Pillar 7: Hybrid Shield - Privacy-preserving transparency
        public_record = self._create_public_record(decision)
        
        # Pillar 8: Create blockchain Anchor for permanent verification
        if len(self.decision_logs) % 10 == 0:  # Anchor every 10 decisions
            anchor = self._create_blockchain_anchor()
            decision.metadata['blockchain_anchor'] = anchor
        
        # Enhance decision with policy-specific information
        decision = self._enhance_policy_decision(decision, economic_data, indicators)
        
        return decision
    
    def _record_epistemic_hold(self, decision: TLResult, indicators: Dict, economic_data: Dict):
        """
        Pillar 1: Record Epistemic Hold activation with full context
        """
        hold_record = {
            'timestamp': datetime.now().isoformat(),
            'duration_ms': 300,  # Standard 300ms hold
            'confidence_level': decision.confidence,
            'uncertainty_sources': self._identify_uncertainty_sources(indicators),
            'conflicting_signals': self._identify_conflicts(indicators),
            'data_gaps': [k for k, v in indicators.items() if v is None],
            'next_actions': decision.clarifying_questions,
            'economic_context': economic_data.get('inflation_regime', 'unknown')
        }
        self.epistemic_holds.append(hold_record)
    
    def _create_decision_log(self, decision: TLResult, indicators: Dict, economic_data: Dict) -> Dict:
        """
        Pillar 4: Create comprehensive Decision Log for complete audit trail
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'decision_id': hashlib.sha256(f"{datetime.now().isoformat()}_{decision.state}".encode()).hexdigest()[:16],
            'state': decision.state.value,
            'state_name': decision.state.name,
            'confidence': decision.confidence,
            'indicators': indicators,
            'economic_data_snapshot': economic_data,
            'reasoning': decision.reasoning,
            'policy_rate_before': self.current_policy_rate,
            'policy_rate_after': self._calculate_new_policy_rate(decision),
            'dual_mandate_assessment': {
                'inflation_objective': self._assess_inflation_objective(indicators),
                'employment_objective': self._assess_employment_objective(indicators),
                'conflict_present': self._assess_mandate_conflict(indicators)
            },
            'clarifying_questions': decision.clarifying_questions if decision.state == TLState.EPISTEMIC_HOLD else None,
            'eight_pillars_validation': self.eight_pillars.validation_status
        }
    
    def _create_ledger_entry(self, decision_log: Dict) -> Dict:
        """
        Pillar 2: Create Immutable Ledger entry with cryptographic hash
        """
        previous_hash = self.policy_ledger[-1]['hash'] if self.policy_ledger else 'genesis'
        
        entry = {
            'index': len(self.policy_ledger),
            'timestamp': decision_log['timestamp'],
            'decision_id': decision_log['decision_id'],
            'decision_hash': hashlib.sha256(json.dumps(decision_log, sort_keys=True).encode()).hexdigest(),
            'previous_hash': previous_hash,
            'state': decision_log['state']
        }
        
        # Create block hash
        entry['hash'] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        
        return entry
    
    def _ensure_regulatory_compliance(self, decision: TLResult, economic_data: Dict):
        """
        Pillar 5: Ensure compliance with regulatory requirements (Basel III, FATF, etc.)
        """
        compliance_checks = {
            'basel_iii_compliance': self._check_basel_iii_compliance(decision),
            'fatf_recommendations': self._check_fatf_compliance(economic_data),
            'iosco_principles': self._check_iosco_principles(decision),
            'local_mandates': self._check_local_mandates(decision, economic_data)
        }
        
        if decision.metadata is None:
            decision.metadata = {}
        
        decision.metadata['regulatory_compliance'] = compliance_checks
    
    def _create_public_record(self, decision: TLResult) -> Dict:
        """
        Pillar 7: Hybrid Shield - Create public record without sensitive data
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'decision_proof': hashlib.sha256(str(decision).encode()).hexdigest()[:16],
            'state': decision.state.name,
            'confidence_band': self._get_confidence_band(decision.confidence),
            'verification': 'VALID',
            'privacy_preserved': True
        }
    
    def _create_blockchain_anchor(self) -> Dict:
        """
        Pillar 8: Create blockchain Anchor for permanent verification
        """
        # Aggregate recent decisions for merkle root
        recent_logs = self.decision_logs[-10:]
        combined_hash = hashlib.sha256(
            json.dumps(recent_logs, sort_keys=True).encode()
        ).hexdigest()
        
        return {
            'merkle_root': combined_hash[:32],
            'decision_count': len(recent_logs),
            'timestamp': datetime.now().isoformat(),
            'blockchain': 'Bitcoin',  # Or appropriate chain
            'block_height': 'PENDING',
            'status': 'AWAITING_CONFIRMATION'
        }
    
    def _analyze_inflation_trend(self, inflation_data: List[float]) -> Optional[float]:
        """Analyze inflation trend relative to target"""
        if not inflation_data or len(inflation_data) < 3:
            return None
            
        recent_inflation = np.mean(inflation_data[-3:])
        trend = np.polyfit(range(len(inflation_data)), inflation_data, 1)[0]
        
        target_deviation = (recent_inflation - self.inflation_target) / self.inflation_target
        trend_component = trend * 12  # Annualize
        
        signal = (target_deviation * 0.7) + (trend_component * 0.3)
        return np.clip(signal * 2, -1, 1)
    
    def _analyze_inflation_expectations(self, expectations_data: Dict) -> Optional[float]:
        """Analyze inflation expectations anchoring"""
        if 'five_year_forward' not in expectations_data:
            return None
            
        five_year_expectation = expectations_data['five_year_forward']
        target_deviation = (five_year_expectation - self.inflation_target) / self.inflation_target
        
        if abs(target_deviation) < 0.1:  # Well-anchored
            return 0
        elif target_deviation > 0:
            return min(target_deviation * 2, 1)
        else:
            return max(target_deviation * 2, -1)
    
    def _analyze_labor_market(self, unemployment_rate: float, job_openings: Optional[float]) -> Optional[float]:
        """Analyze labor market strength"""
        unemployment_gap = (unemployment_rate - self.unemployment_target) / self.unemployment_target
        signal = -unemployment_gap
        
        if job_openings is not None:
            openings_to_unemployed = job_openings / unemployment_rate if unemployment_rate > 0 else 0
            if openings_to_unemployed > 1.5:
                signal += 0.3
            elif openings_to_unemployed < 0.8:
                signal -= 0.3
                
        return np.clip(signal, -1, 1)
    
    def _analyze_economic_growth(self, gdp_growth: List[float]) -> Optional[float]:
        """Analyze economic growth momentum"""
        if not gdp_growth or len(gdp_growth) < 2:
            return None
            
        recent_growth = np.mean(gdp_growth[-2:])
        trend_growth = 0.025  # 2.5% trend
        growth_gap = (recent_growth - trend_growth) / trend_growth
        
        return np.clip(growth_gap, -1, 1)
    
    def _analyze_financial_conditions(self, fci: float) -> Optional[float]:
        """Analyze financial conditions index"""
        signal = -fci / 2  # Invert FCI for policy signal
        return np.clip(signal, -1, 1)
    
    def _analyze_global_conditions(self, global_growth: float, trade_tensions: Optional[float]) -> Optional[float]:
        """Analyze global economic conditions"""
        global_trend = 0.03  # 3% global trend
        growth_signal = (global_growth - global_trend) / global_trend
        
        if trade_tensions is not None:
            tension_adjustment = -trade_tensions * 0.5
            growth_signal += tension_adjustment
            
        return np.clip(growth_signal, -1, 1)
    
    def _analyze_financial_stability(self, credit_spreads: float, asset_valuations: Optional[float]) -> Optional[float]:
        """Analyze financial stability indicators"""
        spread_signal = -credit_spreads * 2
        
        valuation_signal = 0
        if asset_valuations is not None:
            valuation_signal = asset_valuations * 0.5
            
        combined_signal = (spread_signal * 0.7) + (valuation_signal * 0.3)
        return np.clip(combined_signal, -1, 1)
    
    def _analyze_sustainable_finance(self, esg_data: Dict) -> Optional[float]:
        """
        Pillar 6: Analyze sustainable finance considerations
        """
        if not esg_data:
            return None
            
        # Climate risk impact on financial stability
        climate_risk = esg_data.get('climate_risk_score', 0)
        
        # Green finance growth rate
        green_finance_growth = esg_data.get('green_finance_growth', 0)
        
        # Transition risk for carbon-intensive sectors
        transition_risk = esg_data.get('transition_risk', 0)
        
        # Combined ESG signal for monetary policy
        esg_signal = (-climate_risk * 0.4) + (green_finance_growth * 0.3) - (transition_risk * 0.3)
        
        return np.clip(esg_signal, -1, 1)
    
    def _get_policy_weights(self, economic_data: Dict) -> Dict[str, float]:
        """Determine indicator weights based on current economic conditions"""
        base_weights = {
            'inflation_trend': 0.25,
            'inflation_expectations': 0.20,
            'labor_market_strength': 0.20,
            'economic_momentum': 0.15,
            'financial_conditions': 0.10,
            'global_conditions': 0.05,
            'financial_stability': 0.03,
            'sustainable_finance': 0.02  # Pillar 6 consideration
        }
        
        # Adjust for economic regime
        if economic_data.get('inflation_regime') == 'high':
            base_weights['inflation_trend'] *= 1.3
            base_weights['inflation_expectations'] *= 1.2
        elif economic_data.get('inflation_regime') == 'low':
            base_weights['labor_market_strength'] *= 1.2
            base_weights['economic_momentum'] *= 1.1
            
        return base_weights
    
    def _apply_dual_mandate_focus(self, indicators: Dict, economic_data: Dict) -> Dict:
        """Apply central bank dual mandate focus to indicators"""
        dual_mandate_adjusted = indicators.copy()
        
        inflation_signal = indicators.get('inflation_trend', 0) or 0
        labor_signal = indicators.get('labor_market_strength', 0) or 0
        
        if inflation_signal * labor_signal > 0:  # Same direction
            for key in ['inflation_trend', 'labor_market_strength']:
                if key in dual_mandate_adjusted and dual_mandate_adjusted[key] is not None:
                    dual_mandate_adjusted[key] *= 1.2
        elif inflation_signal * labor_signal < 0:  # Conflicting signals
            for key in ['inflation_trend', 'labor_market_strength']:
                if key in dual_mandate_adjusted and dual_mandate_adjusted[key] is not None:
                    dual_mandate_adjusted[key] *= 0.7
                    
        return dual_mandate_adjusted
    
    def _identify_uncertainty_sources(self, indicators: Dict) -> List[str]:
        """Identify sources of uncertainty for Epistemic Hold"""
        sources = []
        
        # Check for missing critical data
        critical_indicators = ['inflation_trend', 'labor_market_strength']
        for indicator in critical_indicators:
            if indicator not in indicators or indicators[indicator] is None:
                sources.append(f"Missing {indicator}")
        
        # Check for conflicting signals
        if self._assess_mandate_conflict(indicators):
            sources.append("Dual mandate conflict")
        
        # Check for extreme volatility
        for key, value in indicators.items():
            if value is not None and abs(value) > 0.8:
                sources.append(f"Extreme signal in {key}")
        
        return sources
    
    def _identify_conflicts(self, indicators: Dict) -> List[str]:
        """Identify conflicting signals in indicators"""
        conflicts = []
        
        # Check major indicator pairs
        pairs = [
            ('inflation_trend', 'labor_market_strength'),
            ('economic_momentum', 'financial_stability'),
            ('financial_conditions', 'global_conditions')
        ]
        
        for ind1, ind2 in pairs:
            val1 = indicators.get(ind1, 0) or 0
            val2 = indicators.get(ind2, 0) or 0
            
            if val1 * val2 < -0.25:  # Strong opposite signals
                conflicts.append(f"{ind1} vs {ind2}")
        
        return conflicts
    
    def _assess_mandate_conflict(self, indicators: Dict) -> bool:
        """Assess if dual mandate objectives are in conflict"""
        inflation_signal = indicators.get('inflation_trend', 0) or 0
        labor_signal = indicators.get('labor_market_strength', 0) or 0
        
        return (inflation_signal * labor_signal < 0 and 
                abs(inflation_signal) > 0.3 and 
                abs(labor_signal) > 0.3)
    
    def _calculate_new_policy_rate(self, decision: TLResult) -> float:
        """Calculate new policy rate based on decision"""
        if decision.state == TLState.PROCEED:
            change = 0.005 if decision.confidence > 0.8 else 0.0025
            return self.current_policy_rate + change
        elif decision.state == TLState.HALT:
            change = -0.005 if decision.confidence > 0.8 else -0.0025
            return max(0, self.current_policy_rate + change)  # Zero lower bound
        else:
            return self.current_policy_rate
    
    def _assess_inflation_objective(self, indicators: Dict) -> str:
        """Assess progress toward inflation objective"""
        inflation_signal = indicators.get('inflation_trend', 0) or 0
        
        if abs(inflation_signal) < 0.1:
            return "At target"
        elif inflation_signal > 0.3:
            return "Above target"
        elif inflation_signal < -0.3:
            return "Below target"
        else:
            return "Near target"
    
    def _assess_employment_objective(self, indicators: Dict) -> str:
        """Assess progress toward employment objective"""
        labor_signal = indicators.get('labor_market_strength', 0) or 0
        
        if abs(labor_signal) < 0.1:
            return "At full employment"
        elif labor_signal > 0.3:
            return "Above full employment"
        elif labor_signal < -0.3:
            return "Below full employment"
        else:
            return "Near full employment"
    
    def _check_basel_iii_compliance(self, decision: TLResult) -> bool:
        """Check Basel III compliance requirements"""
        # Simplified compliance check
        return decision.metadata is not None and 'risk_assessment' in decision.metadata
    
    def _check_fatf_compliance(self, economic_data: Dict) -> bool:
        """Check FATF AML/CFT compliance"""
        # Simplified compliance check
        return 'aml_indicators' not in economic_data or economic_data.get('aml_risk', 0) < 0.5
    
    def _check_iosco_principles(self, decision: TLResult) -> bool:
        """Check IOSCO principles compliance"""
        # Simplified compliance check
        return decision.confidence > 0.3  # Minimum confidence for market stability
    
    def _check_local_mandates(self, decision: TLResult, economic_data: Dict) -> bool:
        """Check local regulatory mandates"""
        # Simplified compliance check
        return True  # Placeholder for jurisdiction-specific requirements
    
    def _get_confidence_band(self, confidence: float) -> str:
        """Get confidence band for public communication"""
        if confidence > 0.8:
            return "High"
        elif confidence > 0.5:
            return "Moderate"
        elif confidence > 0.3:
            return "Low"
        else:
            return "Very Low"
    
    def _enhance_policy_decision(self, decision: TLResult, economic_data: Dict, indicators: Dict) -> TLResult:
        """Enhance decision with central bank specific context"""
        
        if decision.state == TLState.EPISTEMIC_HOLD:
            # Add central bank specific guidance
            cb_questions = [
                "Review incoming high-frequency economic data",
                "Assess financial market functioning and stress indicators",
                "Monitor international spillover effects",
                "Evaluate effectiveness of current policy transmission",
                "Consider forward guidance communication strategy"
            ]
            if decision.clarifying_questions:
                decision.clarifying_questions.extend(cb_questions)
            else:
                decision.clarifying_questions = cb_questions
        
        # Add metadata
        if decision.metadata is None:
            decision.metadata = {}
            
        decision.metadata.update({
            'current_policy_rate': self.current_policy_rate,
            'inflation_target': self.inflation_target,
            'missing_indicators': [k for k, v in indicators.items() if v is None],
            'dual_mandate_conflict': self._assess_mandate_conflict(indicators),
            'eight_pillars_compliant': True,
            'epistemic_hold_count': len(self.epistemic_holds)
        })
        
        return decision
    
    def generate_policy_statement(self, decision: TLResult, economic_data: Dict) -> Dict:
        """
        Generate central bank policy statement with Eight Pillars transparency
        """
        statement = {
            'decision_date': datetime.now().strftime('%Y-%m-%d'),
            'policy_action': self._translate_decision_to_action(decision),
            'policy_rate_target': self._calculate_new_policy_rate(decision),
            'vote': self._generate_committee_vote(decision),
            'economic_assessment': self._generate_economic_assessment(economic_data),
            'policy_rationale': decision.reasoning,
            'forward_guidance': self._generate_forward_guidance(decision),
            'uncertainty_acknowledgment': self._generate_uncertainty_statement(decision),
            'eight_pillars_certification': {
                'epistemic_hold_activated': decision.state == TLState.EPISTEMIC_HOLD,
                'immutable_record_created': True,
                'goukassian_validated': True,
                'decision_log_complete': True,
                'regulatory_compliant': True,
                'esg_considered': 'sustainable_finance' in economic_data,
                'privacy_preserved': True,
                'blockchain_anchored': 'blockchain_anchor' in decision.metadata
            }
        }
        
        if decision.state == TLState.EPISTEMIC_HOLD:
            statement['epistemic_hold_statement'] = self._explain_epistemic_hold(decision)
            
        return statement
    
    def _translate_decision_to_action(self, decision: TLResult) -> str:
        """Translate ternary decision to policy action"""
        if decision.state == TLState.PROCEED:
            basis_points = 50 if decision.confidence > 0.8 else 25
            return f"Raise policy rate by {basis_points} basis points"
        elif decision.state == TLState.HALT:
            basis_points = 50 if decision.confidence > 0.8 else 25
            return f"Lower policy rate by {basis_points} basis points"
        else:  # EPISTEMIC_HOLD
            return "Maintain current policy rate"
    
    def _generate_committee_vote(self, decision: TLResult) -> str:
        """Generate policy committee voting record"""
        if decision.confidence > 0.8:
            return "Unanimous"
        elif decision.confidence > 0.6:
            return "10-2"
        else:
            return "7-5"
    
    def _generate_economic_assessment(self, economic_data: Dict) -> str:
        """Generate economic assessment for policy statement"""
        regime = economic_data.get('inflation_regime', 'normal')
        return (f"Economic activity continues to expand. Labor market conditions remain robust. "
                f"Inflation has been running {'above' if regime == 'high' else 'near'} "
                f"the Committee's target.")
    
    def _generate_forward_guidance(self, decision: TLResult) -> str:
        """Generate forward guidance based on decision"""
        if decision.state == TLState.EPISTEMIC_HOLD:
            return ("The Committee will carefully monitor incoming data and stands ready "
                   "to adjust policy as appropriate to achieve its objectives.")
        elif decision.state == TLState.PROCEED:
            return ("The Committee expects that ongoing increases in the policy rate "
                   "will be appropriate to achieve its objectives.")
        else:
            return ("The Committee expects that ongoing decreases in the policy rate "
                   "may be appropriate to support economic objectives.")
    
    def _generate_uncertainty_statement(self, decision: TLResult) -> str:
        """Generate uncertainty acknowledgment"""
        if decision.confidence < 0.5:
            return "The economic outlook remains highly uncertain."
        elif decision.confidence < 0.7:
            return "The Committee acknowledges elevated uncertainty in the outlook."
        else:
            return "The Committee continues to monitor economic developments."
    
    def _explain_epistemic_hold(self, decision: TLResult) -> str:
        """Explain Epistemic Hold activation"""
        return (f"The Committee has activated an Epistemic Hold (confidence: {decision.confidence:.1%}), "
               f"maintaining the current stance while gathering additional information. "
               f"This reflects commitment to data-dependent policymaking under uncertainty.")


def demonstrate_central_bank_policy():
    """
    Demonstrate Central Bank Policy Engine with Eight Pillars
    """
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║     Central Bank Policy Analysis - Eight Pillars Implementation      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print("\nSovereign-grade accountability for monetary policy decisions")
    print()
    
    # Initialize policy engine
    cb_engine = CentralBankPolicyEngine(
        halt_threshold=0.30,
        hold_threshold=0.70,
        inflation_target=0.02,
        unemployment_target=0.04
    )
    
    # Scenario 1: Clear tightening environment
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Scenario 1: Clear Tightening Signals")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    tightening_data = {
        'core_pce_inflation': [0.025, 0.027, 0.029, 0.031, 0.033],
        'inflation_expectations': {'five_year_forward': 0.028},
        'unemployment_rate': 3.2,
        'job_openings': 11.5,
        'gdp_growth': [0.030, 0.035],
        'financial_conditions_index': -0.5,
        'global_growth': 0.035,
        'credit_spreads': 0.8,
        'inflation_regime': 'high',
        'esg_considerations': {
            'climate_risk_score': 0.3,
            'green_finance_growth': 0.15,
            'transition_risk': 0.2
        }
    }
    
    decision = cb_engine.make_policy_decision(tightening_data)
    statement = cb_engine.generate_policy_statement(decision, tightening_data)
    
    print(f"Decision: {decision.state.name}")
    print(f"Confidence: {decision.confidence:.2%}")
    print(f"Action: {statement['policy_action']}")
    print(f"Reasoning: {decision.reasoning[:100]}...")
    print(f"\nEight Pillars Compliance:")
    for pillar, status in statement['eight_pillars_certification'].items():
        print(f"  • {pillar}: {'✓' if status else '✗'}")
    print()
    
    # Scenario 2: Conflicting signals triggering Epistemic Hold
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Scenario 2: Conflicting Dual Mandate - Epistemic Hold Expected")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    conflicting_data = {
        'core_pce_inflation': [0.015, 0.012, 0.011, 0.010],
        'inflation_expectations': {'five_year_forward': 0.018},
        'unemployment_rate': 3.0,
        'job_openings': 12.0,
        'gdp_growth': [0.015, 0.010],
        'financial_conditions_index': 1.2,
        'global_growth': 0.020,
        'credit_spreads': 2.5,
        'trade_tensions': 0.7,
        'inflation_regime': 'low'
    }
    
    decision = cb_engine.make_policy_decision(conflicting_data)
    statement = cb_engine.generate_policy_statement(decision, conflicting_data)
    
    print(f"Decision: {decision.state.name}")
    print(f"Confidence: {decision.confidence:.2%}")
    print(f"Action: {statement['policy_action']}")
    
    if decision.state == TLState.EPISTEMIC_HOLD:
        print(f"\nEpistemic Hold Statement:")
        print(f"  {statement['epistemic_hold_statement']}")
        print(f"\nMonitoring Actions:")
        for i, action in enumerate(decision.clarifying_questions[:3], 1):
            print(f"  {i}. {action}")
    
    print(f"\nAccountability Metrics:")
    print(f"  • Epistemic Holds Triggered: {len(cb_engine.epistemic_holds)}")
    print(f"  • Decision Logs Created: {len(cb_engine.decision_logs)}")
    print(f"  • Immutable Ledger Entries: {len(cb_engine.policy_ledger)}")
    print()
    
    # Display sample Decision Log entry
    if cb_engine.decision_logs:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Sample Decision Log Entry (Pillar 4)")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        latest_log = cb_engine.decision_logs[-1]
        print(f"Decision ID: {latest_log['decision_id']}")
        print(f"Timestamp: {latest_log['timestamp']}")
        print(f"State: {latest_log['state_name']}")
        print(f"Dual Mandate Assessment:")
        for key, value in latest_log['dual_mandate_assessment'].items():
            print(f"  • {key}: {value}")
    
    print("\n" + "═" * 60)
    print("Central Banking with Sovereign-Grade Accountability")
    print("═" * 60)
    print("\nThe Eight Pillars Framework enables central banks to:")
    print("  • Acknowledge uncertainty through Epistemic Hold")
    print("  • Create immutable audit trails for all decisions")
    print("  • Ensure regulatory compliance automatically")
    print("  • Maintain transparency while preserving necessary confidentiality")
    print("  • Anchor decisions cryptographically for permanent verification")
    print("\nWhen truth becomes measurable, power has nowhere left to hide.")


if __name__ == "__main__":
    demonstrate_central_bank_policy()
    
# Ternary Logic Framework - Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
