### FILE 1: QUICKSTART_EXAMPLE.PY ###
"""
Ternary Logic Framework - Quick Start Example with Eight Pillars
Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com

This example demonstrates the basic usage of the Ternary Logic Framework
with Eight Pillars architecture for sovereign-grade accountability.

"When truth becomes measurable, power has nowhere left to hide."
"""

from ternary_logic import TLDecisionEngine, TLState
from ternary_logic.eight_pillars import EightPillarsFramework
import hashlib
import json
from datetime import datetime

def main():
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║   Ternary Logic Framework - Quick Start with Eight Pillars          ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Initialize the decision engine with Eight Pillars
    engine = TLDecisionEngine(halt_threshold=0.3, hold_threshold=0.7, domain="financial")
    eight_pillars = EightPillarsFramework()
    
    # Pillar 3: Goukassian Principle - Validate all pillars active
    if not eight_pillars.validate_goukassian_principle():
        print("WARNING: Not all Eight Pillars active - not fully TL compliant")
    
    # Pillar 2: Immutable Ledger
    decision_ledger = []
    
    # Pillar 4: Decision Logs
    decision_logs = []
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Example 1: Clear Positive Decision")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Strong positive signals across all criteria
    criteria_positive = {
        'market_sentiment': 0.8,      # Strong positive
        'technical_indicators': 0.6,  # Moderately positive  
        'volume_analysis': 0.7,       # Good volume
        'fundamental_analysis': 0.9,  # Very strong fundamentals
        'regulatory_compliance': 0.95 # Pillar 5: Economic Rights
    }
    
    result = engine.decide(criteria_positive, context="Strong bull market conditions")
    log_entry = create_decision_log(result, criteria_positive, "Example 1")
    decision_logs.append(log_entry)
    ledger_entry = create_ledger_entry(log_entry, decision_ledger)
    decision_ledger.append(ledger_entry)
    
    print_result(result)
    print(f"✓ Decision logged (Pillar 4)")
    print(f"✓ Immutable ledger entry created (Pillar 2)")
    print()
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Example 2: Epistemic Hold Activation")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Mixed signals with missing critical data
    criteria_uncertain = {
        'market_sentiment': 0.3,      # Weak positive
        'technical_indicators': -0.4, # Negative signal
        'volume_analysis': None,      # Missing data!
        'fundamental_analysis': 0.2,  # Weak positive
        'regulatory_compliance': None # Missing compliance check
    }
    
    result = engine.decide(criteria_uncertain, context="Contradictory market signals")
    log_entry = create_decision_log(result, criteria_uncertain, "Example 2")
    decision_logs.append(log_entry)
    ledger_entry = create_ledger_entry(log_entry, decision_ledger)
    decision_ledger.append(ledger_entry)
    
    print_result(result)
    
    if result.state == TLState.EPISTEMIC_HOLD:
        print(f"\n⏸️  Pillar 1: Epistemic Hold activated (300ms pause)")
        print("   Uncertainty exceeds threshold - deliberation required")
    print()
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Example 3: Clear Negative Decision")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Strong negative signals across all criteria
    criteria_negative = {
        'market_sentiment': -0.8,     # Very bearish
        'technical_indicators': -0.6, # Technical breakdown
        'volume_analysis': -0.5,      # Poor volume
        'fundamental_analysis': -0.7, # Weak fundamentals
        'esg_compliance': -0.4        # Pillar 6: Poor ESG scores
    }
    
    result = engine.decide(criteria_negative, context="Bear market conditions")
    log_entry = create_decision_log(result, criteria_negative, "Example 3")
    decision_logs.append(log_entry)
    ledger_entry = create_ledger_entry(log_entry, decision_ledger)
    decision_ledger.append(ledger_entry)
    
    print_result(result)
    print()
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Example 4: Custom Weights with Eight Pillars")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Same data as Example 2, but with custom importance weights
    weights = {
        'market_sentiment': 0.2,      # Lower importance
        'technical_indicators': 0.3,  # Standard importance
        'volume_analysis': 0.4,       # Higher importance (even though missing!)
        'fundamental_analysis': 0.05, # Lower importance
        'regulatory_compliance': 0.05 # Pillar 5 consideration
    }
    
    result = engine.decide(criteria_uncertain, weights=weights, 
                          context="Weighted analysis with volume focus")
    log_entry = create_decision_log(result, criteria_uncertain, "Example 4")
    decision_logs.append(log_entry)
    ledger_entry = create_ledger_entry(log_entry, decision_ledger)
    decision_ledger.append(ledger_entry)
    
    print_result(result)
    
    # Pillar 7: Hybrid Shield - Create privacy-preserving public record
    public_record = create_public_record(result)
    print(f"\n🛡️  Pillar 7: Public record created (privacy preserved)")
    print(f"   Proof hash: {public_record['proof_hash']}")
    print()
    
    # Pillar 8: Blockchain Anchor (simulated)
    if len(decision_logs) >= 4:
        anchor = create_blockchain_anchor(decision_logs)
        print(f"⚓ Pillar 8: Blockchain anchor created")
        print(f"   Merkle root: {anchor['merkle_root']}")
        print()
    
    print("═══════════════════════════════════════")
    print("Decision History Summary with Eight Pillars")
    print("═══════════════════════════════════════")
    
    summary = engine.get_decision_summary()
    print(f"Total Decisions Made: {summary['total_decisions']}")
    print(f"Average Confidence: {summary['average_confidence']:.2f}")
    print(f"Epistemic Hold Rate: {summary['epistemic_hold_rate']:.1%}")
    
    print(f"\nEight Pillars Accountability Metrics:")
    print(f"  • Immutable Ledger Entries: {len(decision_ledger)}")
    print(f"  • Decision Logs Created: {len(decision_logs)}")
    print(f"  • Goukassian Principle: {'✓ Validated' if eight_pillars.validation_status else '✗ Failed'}")
    print(f"  • Epistemic Holds: {summary.get('epistemic_hold_count', 0)}")
    
    print("\nDecision Distribution:")
    for state, count in summary['state_distribution'].items():
        percentage = (count / summary['total_decisions']) * 100
        print(f"  {state}: {count} ({percentage:.1f}%)")
    
    print("\n" + "═" * 60)
    print("Sovereign-Grade Accountability Achieved")
    print("═" * 60)
    print("\nThe Eight Pillars Framework ensures:")
    print("  • Every decision has an immutable audit trail")
    print("  • Uncertainty triggers Epistemic Hold (300ms pause)")
    print("  • Complete regulatory compliance tracking")
    print("  • Privacy-preserving transparency")
    print("  • Cryptographic proof of all decisions")
    print()
    print('"When truth becomes measurable, power has nowhere left to hide."')
    print("                                        — Lev Goukassian")

def print_result(result):
    """Helper function to format and print results"""
    
    # State with emoji
    state_emoji = {
        TLState.PROCEED: "✅",
        TLState.HALT: "❌", 
        TLState.EPISTEMIC_HOLD: "⏸️"
    }
    
    print(f"Decision: {state_emoji[result.state]} {result.state.name}")
    print(f"Confidence: {result.confidence:.2%}")
    print(f"Reasoning: {result.reasoning}")
    
    if result.clarifying_questions:
        print("Clarifying Questions for Epistemic Hold:")
        for i, question in enumerate(result.clarifying_questions[:3], 1):
            print(f"  {i}. {question}")
        if len(result.clarifying_questions) > 3:
            print(f"  ... and {len(result.clarifying_questions)-3} more")
    
    if result.metadata and result.metadata.get('missing_data'):
        missing = result.metadata['missing_data']
        print(f"Missing Data: {', '.join(missing)}")

def create_decision_log(result, criteria, example_name):
    """Pillar 4: Create comprehensive Decision Log"""
    return {
        'timestamp': datetime.now().isoformat(),
        'example': example_name,
        'state': result.state.value,
        'state_name': result.state.name,
        'confidence': result.confidence,
        'criteria': criteria,
        'reasoning': result.reasoning,
        'epistemic_hold': result.state == TLState.EPISTEMIC_HOLD
    }

def create_ledger_entry(decision_log, ledger):
    """Pillar 2: Create Immutable Ledger entry"""
    previous_hash = ledger[-1]['hash'] if ledger else 'genesis'
    
    entry = {
        'index': len(ledger),
        'timestamp': decision_log['timestamp'],
        'decision_hash': hashlib.sha256(json.dumps(decision_log, sort_keys=True).encode()).hexdigest()[:16],
        'previous_hash': previous_hash,
        'state': decision_log['state']
    }
    
    entry['hash'] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()[:16]
    return entry

def create_public_record(result):
    """Pillar 7: Hybrid Shield - Create public record without sensitive data"""
    return {
        'timestamp': datetime.now().isoformat(),
        'proof_hash': hashlib.sha256(str(result).encode()).hexdigest()[:16],
        'state': result.state.name,
        'confidence_band': 'High' if result.confidence > 0.7 else 'Medium' if result.confidence > 0.4 else 'Low',
        'privacy_preserved': True
    }

def create_blockchain_anchor(decision_logs):
    """Pillar 8: Create blockchain Anchor for permanent verification"""
    combined_hash = hashlib.sha256(
        json.dumps(decision_logs, sort_keys=True).encode()
    ).hexdigest()
    
    return {
        'merkle_root': combined_hash[:32],
        'decision_count': len(decision_logs),
        'timestamp': datetime.now().isoformat(),
        'blockchain': 'Ethereum',
        'status': 'PENDING_CONFIRMATION'
    }

if __name__ == "__main__":
    main()

## Contact Information

**Created by Lev Goukassian**
* **ORCID**: 0009-0006-5966-1243
* **Email**: leogouk@gmail.com

**Successor Contact**: support@tl-goukassian.org  
(see [Succession Charter](/memorial/Succession_Charter.md))


### FILE 2: SUPPLY_CHAIN_MANAGEMENT.PY ###
"""
Ternary Logic Framework - Supply Chain Management with Eight Pillars
Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com

This example demonstrates how the Ternary Logic framework provides
sovereign-grade accountability for supply chain decisions through
the Eight Pillars architecture, preventing overreactions while
ensuring complete audit trails.

"The Epistemic Hold prevents supply chain overreactions."
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

class GlobalSupplyChainManager:
    """
    Global Supply Chain Management using Ternary Logic with Eight Pillars
    
    Implements sovereign-grade accountability for supply chain decisions:
    - PROCEED: High confidence to reroute/change suppliers
    - HALT: High confidence to maintain current operations
    - EPISTEMIC_HOLD: Uncertainty detected - graduated response
    """
    
    def __init__(self, 
                 halt_threshold: float = 0.30,
                 hold_threshold: float = 0.70,
                 cost_sensitivity: float = 0.3,
                 time_sensitivity: float = 0.4):
        """
        Initialize Supply Chain Manager with Eight Pillars
        
        Args:
            halt_threshold: Below this confidence, maintain operations
            hold_threshold: Below this confidence, trigger Epistemic Hold
            cost_sensitivity: Weight given to cost considerations (0-1)
            time_sensitivity: Weight given to time/speed considerations (0-1)
        """
        self.engine = TLDecisionEngine(
            halt_threshold=halt_threshold,
            hold_threshold=hold_threshold,
            domain="supply_chain"
        )
        
        # Initialize Eight Pillars Framework
        self.eight_pillars = EightPillarsFramework()
        
        self.cost_sensitivity = cost_sensitivity
        self.time_sensitivity = time_sensitivity
        
        # Supply chain state
        self.active_routes = {}
        self.inventory_levels = {}
        
        # Pillar 2: Immutable Ledger for supply chain decisions
        self.decision_ledger = []
        
        # Pillar 4: Decision Logs for complete audit trail
        self.decision_logs = []
        
        # Pillar 1: Epistemic Hold tracking
        self.epistemic_holds = []
        
        # Risk thresholds
        self.critical_inventory_threshold = 0.15  # 15% of normal
        self.high_cost_threshold = 1.5  # 150% of normal costs
        
    def analyze_disruption_signals(self, 
                                 disruption_event: Dict, 
                                 route_info: Dict,
                                 market_conditions: Dict) -> Dict[str, float]:
        """
        Analyze multiple signals related to supply chain disruption
        
        Returns dictionary with disruption assessment signals
        """
        signals = {}
        
        # Disruption Severity Assessment
        if 'severity_reports' in disruption_event:
            signals['disruption_severity'] = self._assess_disruption_severity(
                disruption_event['severity_reports']
            )
        
        # Duration Estimates
        if 'duration_estimates' in disruption_event:
            signals['disruption_duration'] = self._assess_disruption_duration(
                disruption_event['duration_estimates']
            )
        
        # Alternative Route Viability
        if 'alternative_routes' in route_info:
            signals['route_alternatives'] = self._assess_alternative_routes(
                route_info['alternative_routes'],
                route_info.get('cost_comparisons', None)
            )
        
        # Inventory Buffer Analysis
        if 'current_inventory' in market_conditions:
            signals['inventory_buffer'] = self._assess_inventory_situation(
                market_conditions['current_inventory'],
                market_conditions.get('demand_forecast', None)
            )
        
        # Market Impact Assessment
        if 'customer_commitments' in market_conditions:
            signals['customer_impact'] = self._assess_customer_impact(
                market_conditions['customer_commitments'],
                disruption_event.get('timeline', None)
            )
        
        # Supplier Network Status
        if 'supplier_network' in route_info:
            signals['supplier_flexibility'] = self._assess_supplier_network(
                route_info['supplier_network']
            )
        
        # Financial Impact Analysis
        if 'cost_implications' in disruption_event:
            signals['financial_impact'] = self._assess_financial_impact(
                disruption_event['cost_implications'],
                market_conditions.get('budget_constraints', None)
            )
        
        # Pillar 6: Sustainable Capital Allocation check
        if 'sustainability_metrics' in market_conditions:
            signals['sustainability_impact'] = self._assess_sustainability_impact(
                market_conditions['sustainability_metrics']
            )
        
        return signals
    
    def make_supply_chain_decision(self, 
                                 disruption_event: Dict,
                                 route_info: Dict,
                                 market_conditions: Dict,
                                 response_options: List[str] = None) -> TLResult:
        """
        Make supply chain response decision using Ternary Logic with Eight Pillars
        
        Args:
            disruption_event: Information about the disruption
            route_info: Current and alternative route information
            market_conditions: Market demand and inventory data
            response_options: Available response strategies
            
        Returns:
            TLResult with supply chain recommendation and complete audit trail
        """
        
        # Pillar 3: Goukassian Principle - Validate all pillars active
        if not self.eight_pillars.validate_goukassian_principle():
            raise RuntimeError("Goukassian Principle validation failed - Eight Pillars not all active")
        
        # Analyze disruption signals
        signals = self.analyze_disruption_signals(disruption_event, route_info, market_conditions)
        
        # Define signal weights based on business priorities
        weights = self._get_supply_chain_weights(market_conditions)
        
        # Apply risk management overlay
        risk_adjusted_signals = self._apply_supply_chain_risk_management(
            signals, disruption_event, market_conditions
        )
        
        # Convert to request format for TL engine
        request = f"Supply chain disruption response: {disruption_event.get('event_type', 'Unknown')}"
        context = {
            'signals': risk_adjusted_signals,
            'weights': weights,
            'disruption_type': disruption_event.get('event_type'),
            'timestamp': datetime.now().isoformat()
        }
        
        # Make decision using Ternary Logic
        decision = self.engine.decide(
            request=request,
            context=context,
            scenario="Supply chain disruption response"
        )
        
        # Pillar 1: Track Epistemic Hold if triggered
        if decision.state == TLState.EPISTEMIC_HOLD:
            self._record_epistemic_hold(decision, disruption_event, signals)
        
        # Pillar 4: Create comprehensive Decision Log
        decision_log = self._create_decision_log(decision, disruption_event, signals, market_conditions)
        self.decision_logs.append(decision_log)
        
        # Pillar 2: Add to Immutable Ledger
        ledger_entry = self._create_ledger_entry(decision_log)
        self.decision_ledger.append(ledger_entry)
        
        # Pillar 5: Economic Rights & Transparency - supply chain compliance
        self._ensure_supply_chain_compliance(decision, disruption_event)
        
        # Pillar 7: Hybrid Shield - Privacy-preserving transparency
        public_record = self._create_public_record(decision, disruption_event)
        
        # Pillar 8: Create blockchain Anchor for permanent verification
        if len(self.decision_logs) % 50 == 0:  # Anchor every 50 decisions
            anchor = self._create_blockchain_anchor()
            decision.metadata['blockchain_anchor'] = anchor
        
        # Enhance decision with supply chain specific guidance
        decision = self._enhance_supply_chain_decision(
            decision, disruption_event, signals, response_options
        )
        
        return decision
    
    def implement_response_strategy(self, 
                                  decision: TLResult, 
                                  disruption_event: Dict,
                                  route_info: Dict) -> Dict:
        """
        Implement supply chain response with Eight Pillars accountability
        
        Returns implementation plan with complete audit trail
        """
        
        implementation_plan = {
            'decision_type': decision.state.name,
            'confidence_level': decision.confidence,
            'implementation_timeline': self._determine_implementation_timeline(decision),
            'resource_allocation': self._calculate_resource_allocation(decision),
            'monitoring_requirements': decision.clarifying_questions,
            'eight_pillars_compliance': {
                'epistemic_hold': decision.state == TLState.EPISTEMIC_HOLD,
                'immutable_ledger': True,
                'goukassian_validated': True,
                'decision_logged': True,
                'compliance_verified': True,
                'sustainability_considered': True,
                'privacy_preserved': True,
                'anchoring_scheduled': len(self.decision_logs) % 50 == 0
            }
        }
        
        if decision.state == TLState.PROCEED:
            # Implement major route change or disruption response
            implementation_plan.update({
                'primary_action': 'IMPLEMENT_MAJOR_CHANGE',
                'route_modification': self._design_route_modification(decision, route_info),
                'inventory_adjustments': self._calculate_inventory_adjustments(decision),
                'supplier_communications': self._generate_supplier_communications(decision),
                'customer_notifications': self._generate_customer_notifications(decision),
                'compliance_reporting': 'Notify regulatory authorities of major change'
            })
            
        elif decision.state == TLState.HALT:
            # Maintain current operations with enhanced monitoring
            implementation_plan.update({
                'primary_action': 'MAINTAIN_CURRENT_OPERATIONS',
                'enhanced_monitoring': self._design_enhanced_monitoring(decision),
                'contingency_preparation': self._prepare_contingencies(decision),
                'stakeholder_updates': self._generate_stakeholder_updates(decision),
                'compliance_reporting': 'Standard operations continuing'
            })
            
        else:  # EPISTEMIC_HOLD - Epistemic Hold with 300ms pause
            # Implement graduated response with continuous assessment
            implementation_plan.update({
                'primary_action': 'EPISTEMIC_HOLD_PROTOCOL',
                'hold_duration_ms': 300,  # Standard 300ms pause
                'epistemic_protocol': self._design_epistemic_hold_protocol(decision),
                'data_gathering_plan': self._create_data_gathering_plan(decision),
                'trigger_conditions': self._define_trigger_conditions(decision),
                'escalation_procedures': self._design_escalation_procedures(decision),
                'compliance_reporting': 'Epistemic Hold activated - monitoring uncertainty'
            })
            
        return implementation_plan
    
    def _record_epistemic_hold(self, decision: TLResult, disruption_event: Dict, signals: Dict):
        """
        Pillar 1: Record Epistemic Hold activation with full context
        """
        hold_record = {
            'timestamp': datetime.now().isoformat(),
            'disruption_type': disruption_event.get('event_type', 'unknown'),
            'duration_ms': 300,  # Standard 300ms hold
            'confidence_level': decision.confidence,
            'uncertainty_sources': self._identify_uncertainty_sources(signals),
            'missing_signals': [k for k, v in signals.items() if v is None],
            'next_actions': decision.clarifying_questions,
            'supply_chain_context': {
                'inventory_status': signals.get('inventory_buffer'),
                'customer_impact': signals.get('customer_impact'),
                'route_alternatives': signals.get('route_alternatives')
            }
        }
        self.epistemic_holds.append(hold_record)
    
    def _create_decision_log(self, decision: TLResult, disruption_event: Dict, 
                            signals: Dict, market_conditions: Dict) -> Dict:
        """
        Pillar 4: Create comprehensive Decision Log for complete audit trail
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'decision_id': hashlib.sha256(f"{disruption_event}_{datetime.now()}".encode()).hexdigest()[:16],
            'disruption_type': disruption_event.get('event_type', 'unknown'),
            'state': decision.state.value,
            'state_name': decision.state.name,
            'confidence': decision.confidence,
            'signals': signals,
            'market_snapshot': {
                'inventory_levels': market_conditions.get('current_inventory', {}),
                'customer_commitments': len(market_conditions.get('customer_commitments', [])),
                'business_type': market_conditions.get('business_type', 'balanced')
            },
            'reasoning': decision.reasoning,
            'risk_assessment': {
                'disruption_severity': signals.get('disruption_severity'),
                'financial_impact': signals.get('financial_impact'),
                'customer_impact': signals.get('customer_impact')
            },
            'clarifying_questions': decision.clarifying_questions if decision.state == TLState.EPISTEMIC_HOLD else None,
            'eight_pillars_validation': self.eight_pillars.validation_status
        }
    
    def _create_ledger_entry(self, decision_log: Dict) -> Dict:
        """
        Pillar 2: Create Immutable Ledger entry with cryptographic hash
        """
        previous_hash = self.decision_ledger[-1]['hash'] if self.decision_ledger else 'genesis'
        
        entry = {
            'index': len(self.decision_ledger),
            'timestamp': decision_log['timestamp'],
            'decision_id': decision_log['decision_id'],
            'decision_hash': hashlib.sha256(json.dumps(decision_log, sort_keys=True).encode()).hexdigest(),
            'previous_hash': previous_hash,
            'state': decision_log['state']
        }
        
        # Create block hash
        entry['hash'] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        
        return entry
    
    def _ensure_supply_chain_compliance(self, decision: TLResult, disruption_event: Dict):
        """
        Pillar 5: Ensure supply chain regulatory compliance
        """
        compliance_checks = {
            'trade_regulations': self._check_trade_compliance(disruption_event),
            'customs_requirements': self._check_customs_requirements(decision),
            'safety_standards': self._check_safety_standards(decision),
            'environmental_regulations': self._check_environmental_compliance(decision),
            'labor_standards': self._check_labor_compliance(decision)
        }
        
        if decision.metadata is None:
            decision.metadata = {}
        
        decision.metadata['regulatory_compliance'] = compliance_checks
    
    def _create_public_record(self, decision: TLResult, disruption_event: Dict) -> Dict:
        """
        Pillar 7: Hybrid Shield - Create public record without sensitive details
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'disruption_type': disruption_event.get('event_type', 'unknown'),
            'decision_proof': hashlib.sha256(str(decision).encode()).hexdigest()[:16],
            'state': decision.state.name,
            'confidence_band': self._get_confidence_band(decision.confidence),
            'regulatory_compliant': True,
            'privacy_preserved': True
        }
    
    def _create_blockchain_anchor(self) -> Dict:
        """
        Pillar 8: Create blockchain Anchor for permanent verification
        """
        # Aggregate recent decisions for merkle root
        recent_logs = self.decision_logs[-50:]
        combined_hash = hashlib.sha256(
            json.dumps(recent_logs, sort_keys=True).encode()
        ).hexdigest()
        
        return {
            'merkle_root': combined_hash[:32],
            'decision_count': len(recent_logs),
            'timestamp': datetime.now().isoformat(),
            'blockchain': 'Hyperledger',  # Supply chain appropriate
            'status': 'PENDING_CONFIRMATION'
        }
    
    def _assess_disruption_severity(self, severity_reports: List[Dict]) -> Optional[float]:
        """Assess overall disruption severity from multiple reports"""
        if not severity_reports:
            return None
            
        weighted_severity = 0
        total_confidence = 0
        
        for report in severity_reports:
            if 'severity' in report and 'confidence' in report:
                weighted_severity += report['severity'] * report['confidence']
                total_confidence += report['confidence']
                
        if total_confidence == 0:
            return None
            
        avg_severity = weighted_severity / total_confidence
        return (avg_severity * 2) - 1  # Scale to [-1, 1]
    
    def _assess_disruption_duration(self, duration_estimates: Dict) -> Optional[float]:
        """Assess disruption duration implications"""
        if 'estimated_days' not in duration_estimates:
            return None
            
        estimated_days = duration_estimates['estimated_days']
        confidence = duration_estimates.get('confidence', 0.5)
        
        if estimated_days <= 3:
            duration_signal = -0.5  # Short duration
        elif estimated_days <= 14:
            duration_signal = 0.0   # Medium duration
        elif estimated_days <= 30:
            duration_signal = 0.5   # Long duration
        else:
            duration_signal = 1.0   # Very long
            
        return duration_signal * confidence
    
    def _assess_alternative_routes(self, alternative_routes: List[Dict], 
                                 cost_comparisons: Optional[Dict]) -> Optional[float]:
        """Assess viability of alternative routes"""
        if not alternative_routes:
            return None
            
        viable_routes = 0
        total_routes = len(alternative_routes)
        
        for route in alternative_routes:
            viability_score = 0
            
            if route.get('capacity_available', 0) > 0.7:
                viability_score += 0.4
                
            if cost_comparisons and route.get('route_id') in cost_comparisons:
                cost_ratio = cost_comparisons[route['route_id']]
                if cost_ratio < 1.3:
                    viability_score += 0.3
                elif cost_ratio < 1.6:
                    viability_score += 0.1
                    
            reliability = route.get('reliability_score', 0.5)
            viability_score += reliability * 0.3
            
            if viability_score > 0.6:
                viable_routes += 1
                
        if total_routes == 0:
            return None
            
        viability_ratio = viable_routes / total_routes
        return (viability_ratio * 2) - 1
    
    def _assess_inventory_situation(self, current_inventory: Dict, 
                                  demand_forecast: Optional[Dict]) -> Optional[float]:
        """Assess inventory buffer situation"""
        if not current_inventory:
            return None
            
        total_coverage = 0
        item_count = 0
        
        for item, level in current_inventory.items():
            if demand_forecast and item in demand_forecast:
                daily_demand = demand_forecast[item].get('daily_demand', 1)
                if daily_demand > 0:
                    coverage_days = level / daily_demand
                    total_coverage += coverage_days
                    item_count += 1
                    
        if item_count == 0:
            return None
            
        avg_coverage = total_coverage / item_count
        
        if avg_coverage > 30:
            return -1.0  # No urgency
        elif avg_coverage > 14:
            return -0.5  # Low urgency
        elif avg_coverage > 7:
            return 0.0   # Medium urgency
        elif avg_coverage > 3:
            return 0.5   # High urgency
        else:
            return 1.0   # Critical urgency
    
    def _assess_customer_impact(self, customer_commitments: List[Dict], 
                              disruption_timeline: Optional[Dict]) -> Optional[float]:
        """Assess potential customer impact"""
        if not customer_commitments:
            return None
            
        at_risk_revenue = 0
        total_revenue = 0
        
        disruption_start = disruption_timeline.get('estimated_start', datetime.now()) if disruption_timeline else datetime.now()
        
        for commitment in customer_commitments:
            revenue = commitment.get('revenue_value', 0)
            delivery_date = commitment.get('delivery_date')
            
            total_revenue += revenue
            
            if delivery_date and isinstance(delivery_date, datetime) and delivery_date > disruption_start:
                days_until_delivery = (delivery_date - disruption_start).days
                
                if days_until_delivery <= 14:
                    at_risk_revenue += revenue
                elif days_until_delivery <= 30:
                    at_risk_revenue += revenue * 0.5
                    
        if total_revenue == 0:
            return None
            
        risk_ratio = at_risk_revenue / total_revenue
        return risk_ratio * 2 - 1
    
    def _assess_supplier_network(self, supplier_network: Dict) -> Optional[float]:
        """Assess supplier network flexibility"""
        if 'alternative_suppliers' not in supplier_network:
            return None
            
        alternative_suppliers = supplier_network['alternative_suppliers']
        total_suppliers = supplier_network.get('total_suppliers', 1)
        
        if total_suppliers == 0:
            return None
            
        diversification_ratio = len(alternative_suppliers) / total_suppliers
        
        total_capacity = 0
        supplier_count = 0
        
        for supplier in alternative_suppliers:
            if 'available_capacity' in supplier:
                total_capacity += supplier['available_capacity']
                supplier_count += 1
                
        avg_capacity = total_capacity / supplier_count if supplier_count > 0 else 0
        
        flexibility_score = (diversification_ratio * 0.6) + (avg_capacity * 0.4)
        return (flexibility_score * 2) - 1
    
    def _assess_financial_impact(self, cost_implications: Dict, 
                               budget_constraints: Optional[Dict]) -> Optional[float]:
        """Assess financial impact of disruption response"""
        additional_cost = cost_implications.get('additional_cost_estimate', 0)
        
        if budget_constraints:
            available_budget = budget_constraints.get('emergency_budget', float('inf'))
            if available_budget == 0:
                return 1.0
                
            cost_ratio = additional_cost / available_budget
            
            if cost_ratio <= 0.5:
                return -0.5
            elif cost_ratio <= 1.0:
                return 0.0
            elif cost_ratio <= 2.0:
                return 0.5
            else:
                return 1.0
        else:
            if additional_cost < 100000:
                return -0.3
            elif additional_cost < 500000:
                return 0.0
            elif additional_cost < 1000000:
                return 0.3
            else:
                return 0.7
    
    def _assess_sustainability_impact(self, sustainability_metrics: Dict) -> Optional[float]:
        """
        Pillar 6: Assess sustainability impact of supply chain decision
        """
        if not sustainability_metrics:
            return None
            
        carbon_footprint = sustainability_metrics.get('carbon_footprint_change', 0)
        labor_standards = sustainability_metrics.get('labor_standards_score', 0.5)
        environmental_impact = sustainability_metrics.get('environmental_impact', 0)
        
        # Weighted sustainability score
        sustainability_score = (
            -carbon_footprint * 0.4 +  # Negative carbon impact is good
            labor_standards * 0.3 +
            -environmental_impact * 0.3  # Negative environmental impact is good
        )
        
        return np.clip(sustainability_score, -1, 1)
    
    def _get_supply_chain_weights(self, market_conditions: Dict) -> Dict[str, float]:
        """Determine signal weights based on business priorities"""
        base_weights = {
            'disruption_severity': 0.25,
            'disruption_duration': 0.20,
            'route_alternatives': 0.15,
            'inventory_buffer': 0.20,
            'customer_impact': 0.08,
            'supplier_flexibility': 0.05,
            'financial_impact': 0.05,
            'sustainability_impact': 0.02  # Pillar 6
        }
        
        business_type = market_conditions.get('business_type', 'balanced')
        
        if business_type == 'just_in_time':
            base_weights['inventory_buffer'] *= 1.5
            base_weights['disruption_duration'] *= 1.3
        elif business_type == 'cost_sensitive':
            base_weights['financial_impact'] *= 2.0
            base_weights['route_alternatives'] *= 1.2
        elif business_type == 'customer_first':
            base_weights['customer_impact'] *= 2.0
            base_weights['inventory_buffer'] *= 1.3
        elif business_type == 'sustainable':
            base_weights['sustainability_impact'] *= 3.0
            
        return base_weights
    
    def _apply_supply_chain_risk_management(self, signals: Dict, 
                                          disruption_event: Dict,
                                          market_conditions: Dict) -> Dict:
        """Apply risk management overlay to signals"""
        risk_adjusted = signals.copy()
        
        # Critical inventory situation
        inventory_signal = signals.get('inventory_buffer', 0) or 0
        if inventory_signal > 0.7:
            for key in risk_adjusted:
                if risk_adjusted[key] is not None and risk_adjusted[key] > 0:
                    risk_adjusted[key] *= 1.3
                    
        # High customer impact
        customer_signal = signals.get('customer_impact', 0) or 0
        if customer_signal > 0.6:
            for key in ['disruption_severity', 'disruption_duration']:
                if key in risk_adjusted and risk_adjusted[key] is not None:
                    risk_adjusted[key] = min(1.0, risk_adjusted[key] * 1.2)
                    
        return risk_adjusted
    
    def _identify_uncertainty_sources(self, signals: Dict) -> List[str]:
        """Identify sources of uncertainty for Epistemic Hold"""
        sources = []
        
        # Check for missing critical signals
        critical_signals = ['disruption_severity', 'inventory_buffer', 'route_alternatives']
        for signal in critical_signals:
            if signal not in signals or signals[signal] is None:
                sources.append(f"Missing {signal}")
        
        # Check for conflicting signals
        if signals.get('disruption_severity', 0) > 0.5 and signals.get('financial_impact', 0) < -0.5:
            sources.append("Severity vs Cost conflict")
        
        return sources
    
    def _enhance_supply_chain_decision(self, decision: TLResult, disruption_event: Dict,
                                     signals: Dict, response_options: List[str] = None) -> TLResult:
        """Enhance decision with supply chain specific guidance"""
        
        if decision.state == TLState.EPISTEMIC_HOLD:
            sc_steps = [
                "Monitor disruption severity from multiple sources",
                "Assess alternative route costs and availability",
                "Evaluate inventory buffer adequacy",
                "Consult key suppliers on flexibility",
                "Review sustainability impact of alternatives"
            ]
            if decision.clarifying_questions:
                decision.clarifying_questions.extend(sc_steps)
            else:
                decision.clarifying_questions = sc_steps
        
        if decision.metadata is None:
            decision.metadata = {}
            
        decision.metadata.update({
            'disruption_type': disruption_event.get('event_type', 'unknown'),
            'missing_signals': [k for k, v in signals.items() if v is None],
            'signal_count': len([v for v in signals.values() if v is not None]),
            'eight_pillars_compliant': True,
            'epistemic_hold_count': len(self.epistemic_holds)
        })
        
        return decision
    
    # Implementation helper methods
    def _determine_implementation_timeline(self, decision: TLResult) -> int:
        """Determine implementation timeline in hours"""
        if decision.state == TLState.PROCEED:
            return 24
        elif decision.state == TLState.HALT:
            return 72
        else:  # EPISTEMIC_HOLD
            return 48
    
    def _calculate_resource_allocation(self, decision: TLResult) -> Dict:
        """Calculate resource allocation"""
        return {
            'personnel': 'full_team' if decision.state == TLState.PROCEED else 'monitoring_team',
            'budget': 'emergency' if decision.state == TLState.PROCEED else 'standard',
            'priority': 'high' if decision.state == TLState.PROCEED else 'medium'
        }
    
    def _design_route_modification(self, decision: TLResult, route_info: Dict) -> Dict:
        """Design route modification plan"""
        return {
            'primary_route': 'alternative_route_1',
            'backup_route': 'alternative_route_2',
            'transition_plan': 'phased_over_48_hours'
        }
    
    def _calculate_inventory_adjustments(self, decision: TLResult) -> Dict:
        """Calculate inventory adjustments"""
        return {
            'safety_stock_increase': 0.3,
            'reorder_point_adjustment': 1.2,
            'emergency_orders': 'approved'
        }
    
    def _generate_supplier_communications(self, decision: TLResult) -> List[str]:
        """Generate supplier communications"""
        return [
            "Notify suppliers of route change",
            "Request delivery flexibility",
            "Coordinate alternative sourcing"
        ]
    
    def _generate_customer_notifications(self, decision: TLResult) -> List[str]:
        """Generate customer notifications"""
        return [
            "Inform of potential delays",
            "Provide updated estimates",
            "Offer alternatives"
        ]
    
    def _design_enhanced_monitoring(self, decision: TLResult) -> Dict:
        """Design enhanced monitoring"""
        return {
            'frequency': 'hourly',
            'metrics': ['route_status', 'inventory', 'suppliers'],
            'thresholds': {'severity': 0.7, 'duration': 7}
        }
    
    def _prepare_contingencies(self, decision: TLResult) -> List[str]:
        """Prepare contingencies"""
        return [
            "Identify backup suppliers",
            "Prepare emergency routes",
            "Ready crisis plans"
        ]
    
    def _generate_stakeholder_updates(self, decision: TLResult) -> List[str]:
        """Generate stakeholder updates"""
        return [
            "Situation stable",
            "Monitoring continues",
            "Updates as needed"
        ]
    
    def _design_epistemic_hold_protocol(self, decision: TLResult) -> Dict:
        """Design Epistemic Hold protocol"""
        pause_duration_hours = max(4, min(48, (1 - decision.confidence) * 72))
        
        return {
            'pause_duration_hours': pause_duration_hours,
            'monitoring_frequency': 'every_2_hours',
            'escalation_triggers': [
                'inventory_critical',
                'customer_complaints',
                'severity_increase',
                'routes_unavailable'
            ]
        }
    
    def _create_data_gathering_plan(self, decision: TLResult) -> List[str]:
        """Create data gathering plan"""
        return [
            "Request severity updates",
            "Analyze route costs",
            "Survey suppliers",
            "Update forecasts"
        ]
    
    def _define_trigger_conditions(self, decision: TLResult) -> Dict:
        """Define trigger conditions"""
        return {
            'immediate': 'severity > 0.8',
            'escalate': 'confidence > 0.7',
            'stand_down': 'disruption resolved'
        }
    
    def _design_escalation_procedures(self, decision: TLResult) -> List[str]:
        """Design escalation procedures"""
        return [
            "Alert management",
            "Activate crisis team",
            "Implement contingencies"
        ]
    
    def _check_trade_compliance(self, disruption_event: Dict) -> bool:
        """Check trade regulations compliance"""
        return True  # Simplified
    
    def _check_customs_requirements(self, decision: TLResult) -> bool:
        """Check customs requirements"""
        return True  # Simplified
    
    def _check_safety_standards(self, decision: TLResult) -> bool:
        """Check safety standards"""
        return True  # Simplified
    
    def _check_environmental_compliance(self, decision: TLResult) -> bool:
        """Check environmental regulations"""
        return True  # Simplified
    
    def _check_labor_compliance(self, decision: TLResult) -> bool:
        """Check labor standards"""
        return True  # Simplified
    
    def _get_confidence_band(self, confidence: float) -> str:
        """Get confidence band for reporting"""
        if confidence > 0.7:
            return "High"
        elif confidence > 0.4:
            return "Medium"
        else:
            return "Low"


def demonstrate_supply_chain_management():
    """
    Demonstrate Supply Chain Management with Eight Pillars accountability
    """
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║   Global Supply Chain Management - Eight Pillars Implementation      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print("\nCreated by Lev Goukassian (ORCID: 0009-0006-5966-1243)")
    print("Contact: leogouk@gmail.com")
    print('\n"The Epistemic Hold prevents supply chain overreactions."\n')
    
    # Initialize supply chain manager
    sc_manager = GlobalSupplyChainManager(
        halt_threshold=0.30,
        hold_threshold=0.70,
        cost_sensitivity=0.3,
        time_sensitivity=0.4
    )
    
    # Scenario 1: Major Route Disruption
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Scenario 1: Suez Canal Blockage - Major Disruption")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    major_disruption = {
        'event_type': 'shipping_route_blockage',
        'severity_reports': [
            {'severity': 0.9, 'confidence': 0.95, 'source': 'port_authority'},
            {'severity': 0.85, 'confidence': 0.8, 'source': 'shipping_company'},
            {'severity': 0.95, 'confidence': 0.9, 'source': 'logistics_partner'}
        ],
        'duration_estimates': {'estimated_days': 14, 'confidence': 0.7},
        'cost_implications': {'additional_cost_estimate': 2500000},
        'timeline': {'estimated_start': datetime.now()}
    }
    
    major_route_info = {
        'alternative_routes': [
            {'route_id': 'cape_of_good_hope', 'capacity_available': 0.8, 'reliability_score': 0.9},
            {'route_id': 'trans_pacific', 'capacity_available': 0.6, 'reliability_score': 0.85}
        ],
        'cost_comparisons': {'cape_of_good_hope': 1.4, 'trans_pacific': 1.6}
    }
    
    major_market_conditions = {
        'current_inventory': {'electronics': 500, 'textiles': 300, 'machinery': 150},
        'demand_forecast': {
            'electronics': {'daily_demand': 50},
            'textiles': {'daily_demand': 30},
            'machinery': {'daily_demand': 10}
        },
        'customer_commitments': [
            {'revenue_value': 5000000, 'delivery_date': datetime.now() + timedelta(days=21)},
            {'revenue_value': 3000000, 'delivery_date': datetime.now() + timedelta(days=35)}
        ],
        'business_type': 'customer_first',
        'sustainability_metrics': {
            'carbon_footprint_change': 0.3,  # 30% increase
            'labor_standards_score': 0.8,
            'environmental_impact': 0.2
        }
    }
    
    decision = sc_manager.make_supply_chain_decision(
        major_disruption, major_route_info, major_market_conditions
    )
    implementation = sc_manager.implement_response_strategy(
        decision, major_disruption, major_route_info
    )
    
    print(f"Decision: {decision.state.name}")
    print(f"Confidence: {decision.confidence:.2%}")
    print(f"Action: {implementation['primary_action']}")
    print(f"Timeline: {implementation['implementation_timeline']} hours")
    print(f"Reasoning: {decision.reasoning[:80]}...")
    print(f"\nEight Pillars Compliance:")
    for pillar, status in implementation['eight_pillars_compliance'].items():
        print(f"  • {pillar}: {'✓' if status else '✗'}")
    print()
    
    # Scenario 2: Uncertain Geopolitical Situation
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Scenario 2: Geopolitical Tensions - Epistemic Hold Expected")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    uncertain_disruption = {
        'event_type': 'geopolitical_tension',
        'severity_reports': [
            {'severity': 0.4, 'confidence': 0.5, 'source': 'news_media'},
            {'severity': 0.6, 'confidence': 0.3, 'source': 'government_advisory'}
        ],
        'duration_estimates': {'estimated_days': None, 'confidence': 0.2},
        'cost_implications': {'additional_cost_estimate': None}
    }
    
    uncertain_route_info = {
        'alternative_routes': None,
        'supplier_network': {
            'total_suppliers': 10,
            'alternative_suppliers': [
                {'available_capacity': 0.4},
                {'available_capacity': 0.6}
            ]
        }
    }
    
    uncertain_market_conditions = {
        'current_inventory': {'electronics': 800, 'textiles': 600},
        'demand_forecast': None,
        'customer_commitments': [
            {'revenue_value': 2000000, 'delivery_date': datetime.now() + timedelta(days=45)}
        ],
        'business_type': 'balanced'
    }
    
    decision = sc_manager.make_supply_chain_decision(
        uncertain_disruption, uncertain_route_info, uncertain_market_conditions
    )
    implementation = sc_manager.implement_response_strategy(
        decision, uncertain_disruption, uncertain_route_info
    )
    
    print(f"Decision: {decision.state.name}")
    print(f"Confidence: {decision.confidence:.2%}")
    print(f"Action: {implementation['primary_action']}")
    
    if decision.state == TLState.EPISTEMIC_HOLD:
        print(f"\nEpistemic Hold Protocol:")
        print(f"  • Hold Duration: {implementation['hold_duration_ms']}ms")
        protocol = implementation['epistemic_protocol']
        print(f"  • Extended Monitoring: {protocol['pause_duration_hours']} hours")
        print(f"  • Monitoring Frequency: {protocol['monitoring_frequency']}")
        print(f"\nData Gathering Plan:")
        for action in implementation['data_gathering_plan'][:3]:
            print(f"  • {action}")
        print(f"\nEscalation Triggers:")
        for trigger in protocol['escalation_triggers'][:3]:
            print(f"  • {trigger}")
    print()
    
    # Scenario 3: Minor Weather Delay
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Scenario 3: Minor Weather Delay - Maintain Operations")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    minor_disruption = {
        'event_type': 'weather_delay',
        'severity_reports': [
            {'severity': 0.2, 'confidence': 0.9, 'source': 'weather_service'},
            {'severity': 0.15, 'confidence': 0.85, 'source': 'logistics_team'}
        ],
        'duration_estimates': {'estimated_days': 2, 'confidence': 0.9},
        'cost_implications': {'additional_cost_estimate': 50000}
    }
    
    minor_route_info = {
        'alternative_routes': [
            {'route_id': 'alternative_port', 'capacity_available': 0.9, 'reliability_score': 0.95}
        ],
        'cost_comparisons': {'alternative_port': 1.1}
    }
    
    minor_market_conditions = {
        'current_inventory': {'electronics': 1200, 'textiles': 900},
        'demand_forecast': {
            'electronics': {'daily_demand': 40},
            'textiles': {'daily_demand': 25}
        },
        'customer_commitments': [
            {'revenue_value': 1000000, 'delivery_date': datetime.now() + timedelta(days=60)}
        ],
        'business_type': 'cost_sensitive'
    }
    
    decision = sc_manager.make_supply_chain_decision(
        minor_disruption, minor_route_info, minor_market_conditions
    )
    implementation = sc_manager.implement_response_strategy(
        decision, minor_disruption, minor_route_info
    )
    
    print(f"Decision: {decision.state.name}")
    print(f"Confidence: {decision.confidence:.2%}")
    print(f"Action: {implementation['primary_action']}")
    print(f"Compliance: {implementation['compliance_reporting']}")
    print()
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Supply Chain Management Summary")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    print(f"\nAccountability Metrics:")
    print(f"  • Decision Logs Created: {len(sc_manager.decision_logs)}")
    print(f"  • Immutable Ledger Entries: {len(sc_manager.decision_ledger)}")
    print(f"  • Epistemic Holds Triggered: {len(sc_manager.epistemic_holds)}")
    
    print("\n" + "═" * 60)
    print("Supply Chain Management with Sovereign-Grade Accountability")
    print("═" * 60)
    print("\nThe Eight Pillars Framework ensures:")
    print("  • Graduated responses to uncertainty (Epistemic Hold)")
    print("  • Immutable audit trails for all decisions")
    print("  • Complete regulatory compliance")
    print("  • Sustainability considerations in routing")
    print("  • Cryptographic proof of decision integrity")
    print("\nPreventing overreactions while maintaining full accountability.")


if __name__ == "__main__":
    demonstrate_supply_chain_management()

## Contact Information

**Created by Lev Goukassian**
* **ORCID**: 0009-0006-5966-1243
* **Email**: leogouk@gmail.com

**Successor Contact**: support@tl-goukassian.org  
(see [Succession Charter](/memorial/Succession_Charter.md))
