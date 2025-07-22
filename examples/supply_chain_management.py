"""
Goukassian Framework - Supply Chain Management Example
Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com

This example demonstrates how the Ternary Logic framework enables intelligent
supply chain responses to disruptions by implementing graduated responses
rather than binary reroute/don't-reroute decisions.

"The Sacred Pause prevents supply chain overreactions."
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

# Import Goukassian Framework
from goukassian import TernaryDecisionEngine, TernaryState
from goukassian.core import TernaryResult

class GlobalSupplyChainManager:
    """
    Global Supply Chain Management using Ternary Logic
    
    This system demonstrates how the Sacred Pause principle prevents costly
    overreactions to supply chain disruptions while ensuring adequate response
    to genuine threats.
    """
    
    def __init__(self, 
                 confidence_threshold: float = 0.70,
                 cost_sensitivity: float = 0.3,
                 time_sensitivity: float = 0.4):
        """
        Initialize the Supply Chain Manager
        
        Args:
            confidence_threshold: Minimum confidence for major route changes
            cost_sensitivity: Weight given to cost considerations (0-1)
            time_sensitivity: Weight given to time/speed considerations (0-1)
        """
        self.engine = TernaryDecisionEngine(
            confidence_threshold=confidence_threshold,
            domain="supply_chain"
        )
        self.cost_sensitivity = cost_sensitivity
        self.time_sensitivity = time_sensitivity
        
        # Supply chain state
        self.active_routes = {}
        self.inventory_levels = {}
        self.disruption_history = []
        self.adaptation_history = []
        
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
        else:
            signals['disruption_severity'] = None
            
        # Duration Estimates
        if 'duration_estimates' in disruption_event:
            signals['disruption_duration'] = self._assess_disruption_duration(
                disruption_event['duration_estimates']
            )
        else:
            signals['disruption_duration'] = None
            
        # Alternative Route Viability
        if 'alternative_routes' in route_info:
            signals['route_alternatives'] = self._assess_alternative_routes(
                route_info['alternative_routes'],
                route_info.get('cost_comparisons', None)
            )
        else:
            signals['route_alternatives'] = None
            
        # Inventory Buffer Analysis
        if 'current_inventory' in market_conditions:
            signals['inventory_buffer'] = self._assess_inventory_situation(
                market_conditions['current_inventory'],
                market_conditions.get('demand_forecast', None)
            )
        else:
            signals['inventory_buffer'] = None
            
        # Market Impact Assessment
        if 'customer_commitments' in market_conditions:
            signals['customer_impact'] = self._assess_customer_impact(
                market_conditions['customer_commitments'],
                disruption_event.get('timeline', None)
            )
        else:
            signals['customer_impact'] = None
            
        # Supplier Network Status
        if 'supplier_network' in route_info:
            signals['supplier_flexibility'] = self._assess_supplier_network(
                route_info['supplier_network']
            )
        else:
            signals['supplier_flexibility'] = None
            
        # Financial Impact Analysis
        if 'cost_implications' in disruption_event:
            signals['financial_impact'] = self._assess_financial_impact(
                disruption_event['cost_implications'],
                market_conditions.get('budget_constraints', None)
            )
        else:
            signals['financial_impact'] = None
            
        return signals
    
    def make_supply_chain_decision(self, 
                                 disruption_event: Dict,
                                 route_info: Dict,
                                 market_conditions: Dict,
                                 response_options: List[str] = None) -> TernaryResult:
        """
        Make supply chain response decision using Ternary Logic
        
        Args:
            disruption_event: Information about the disruption
            route_info: Current and alternative route information
            market_conditions: Market demand and inventory data
            response_options: Available response strategies
            
        Returns:
            TernaryResult with supply chain recommendation
        """
        
        # Analyze disruption signals
        signals = self.analyze_disruption_signals(disruption_event, route_info, market_conditions)
        
        # Define signal weights based on business priorities
        weights = self._get_supply_chain_weights(market_conditions)
        
        # Apply risk management overlay
        risk_adjusted_signals = self._apply_supply_chain_risk_management(
            signals, disruption_event, market_conditions
        )
        
        # Make decision using Ternary Logic
        decision = self.engine.decide(
            criteria=risk_adjusted_signals,
            weights=weights,
            context=f"Supply chain disruption response: {disruption_event.get('event_type', 'Unknown')}"
        )
        
        # Enhance decision with supply chain specific guidance
        decision = self._enhance_supply_chain_decision(
            decision, disruption_event, signals, response_options
        )
        
        # Log decision for supply chain analytics
        self._log_supply_chain_decision(decision, disruption_event, signals)
        
        return decision
    
    def implement_response_strategy(self, 
                                  decision: TernaryResult, 
                                  disruption_event: Dict,
                                  route_info: Dict) -> Dict:
        """
        Implement supply chain response based on Ternary Logic decision
        
        Returns implementation plan with specific actions
        """
        
        implementation_plan = {
            'decision_type': decision.state.name,
            'confidence_level': decision.confidence,
            'implementation_timeline': self._determine_implementation_timeline(decision),
            'resource_allocation': self._calculate_resource_allocation(decision),
            'monitoring_requirements': decision.next_steps
        }
        
        if decision.state == TernaryState.TRUE:
            # Implement major route change or disruption response
            implementation_plan.update({
                'primary_action': 'IMPLEMENT_MAJOR_CHANGE',
                'route_modification': self._design_route_modification(decision, route_info),
                'inventory_adjustments': self._calculate_inventory_adjustments(decision),
                'supplier_communications': self._generate_supplier_communications(decision),
                'customer_notifications': self._generate_customer_notifications(decision)
            })
            
        elif decision.state == TernaryState.FALSE:
            # Maintain current operations with enhanced monitoring
            implementation_plan.update({
                'primary_action': 'MAINTAIN_CURRENT_OPERATIONS',
                'enhanced_monitoring': self._design_enhanced_monitoring(decision),
                'contingency_preparation': self._prepare_contingencies(decision),
                'stakeholder_updates': self._generate_stakeholder_updates(decision)
            })
            
        else:  # INDETERMINATE - Sacred Pause
            # Implement graduated response with continuous assessment
            implementation_plan.update({
                'primary_action': 'GRADUATED_RESPONSE',
                'sacred_pause_protocol': self._design_sacred_pause_protocol(decision),
                'data_gathering_plan': self._create_data_gathering_plan(decision),
                'trigger_conditions': self._define_trigger_conditions(decision),
                'escalation_procedures': self._design_escalation_procedures(decision)
            })
            
        return implementation_plan
    
    def _assess_disruption_severity(self, severity_reports: List[Dict]) -> Optional[float]:
        """Assess overall disruption severity from multiple reports"""
        if not severity_reports:
            return None
            
        # Aggregate severity scores with confidence weighting
        weighted_severity = 0
        total_confidence = 0
        
        for report in severity_reports:
            if 'severity' in report and 'confidence' in report:
                weight = report['confidence']
                severity = report['severity']  # Assume 0-1 scale
                weighted_severity += severity * weight
                total_confidence += weight
                
        if total_confidence == 0:
            return None
            
        avg_severity = weighted_severity / total_confidence
        
        # Convert to signal scale (-1 to 1, where 1 = severe disruption requiring action)
        return (avg_severity * 2) - 1
    
    def _assess_disruption_duration(self, duration_estimates: Dict) -> Optional[float]:
        """Assess disruption duration implications"""
        if 'estimated_days' not in duration_estimates:
            return None
            
        estimated_days = duration_estimates['estimated_days']
        confidence = duration_estimates.get('confidence', 0.5)
        
        # Longer disruptions require more proactive response
        # Signal strength based on duration and confidence
        if estimated_days <= 3:
            duration_signal = -0.5  # Short duration - less urgent
        elif estimated_days <= 14:
            duration_signal = 0.0   # Medium duration - neutral
        elif estimated_days <= 30:
            duration_signal = 0.5   # Long duration - action needed
        else:
            duration_signal = 1.0   # Very long - urgent action
            
        # Adjust by confidence in estimate
        return duration_signal * confidence
    
    def _assess_alternative_routes(self, 
                                 alternative_routes: List[Dict], 
                                 cost_comparisons: Optional[Dict]) -> Optional[float]:
        """Assess viability of alternative routes"""
        if not alternative_routes:
            return None
            
        viable_routes = 0
        total_routes = len(alternative_routes)
        
        for route in alternative_routes:
            viability_score = 0
            
            # Check route capacity
            if route.get('capacity_available', 0) > 0.7:  # 70% capacity available
                viability_score += 0.4
                
            # Check cost implications
            if cost_comparisons and route.get('route_id') in cost_comparisons:
                cost_ratio = cost_comparisons[route['route_id']]
                if cost_ratio < 1.3:  # Less than 130% of normal cost
                    viability_score += 0.3
                elif cost_ratio < 1.6:  # Less than 160% of normal cost
                    viability_score += 0.1
                    
            # Check reliability
            reliability = route.get('reliability_score', 0.5)
            viability_score += reliability * 0.3
            
            if viability_score > 0.6:  # Threshold for "viable"
                viable_routes += 1
                
        if total_routes == 0:
            return None
            
        viability_ratio = viable_routes / total_routes
        
        # Convert to signal: more viable alternatives = positive signal for change
        return (viability_ratio * 2) - 1
    
    def _assess_inventory_situation(self, 
                                  current_inventory: Dict, 
                                  demand_forecast: Optional[Dict]) -> Optional[float]:
        """Assess inventory buffer situation"""
        
        # Calculate inventory coverage in days
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
        
        # Convert to urgency signal
        if avg_coverage > 30:      # More than 30 days
            return -1.0            # No urgency
        elif avg_coverage > 14:    # 14-30 days
            return -0.5            # Low urgency
        elif avg_coverage > 7:     # 7-14 days
            return 0.0             # Medium urgency
        elif avg_coverage > 3:     # 3-7 days
            return 0.5             # High urgency
        else:                      # Less than 3 days
            return 1.0             # Critical urgency
    
    def _assess_customer_impact(self, 
                              customer_commitments: List[Dict], 
                              disruption_timeline: Optional[Dict]) -> Optional[float]:
        """Assess potential customer impact"""
        if not customer_commitments:
            return None
            
        at_risk_revenue = 0
        total_revenue = 0
        
        disruption_start = disruption_timeline.get('estimated_start') if disruption_timeline else datetime.now()
        
        for commitment in customer_commitments:
            revenue = commitment.get('revenue_value', 0)
            delivery_date = commitment.get('delivery_date')
            
            total_revenue += revenue
            
            if delivery_date and delivery_date > disruption_start:
                # Commitment could be affected by disruption
                days_until_delivery = (delivery_date - disruption_start).days
                
                if days_until_delivery <= 14:  # Within 2 weeks
                    at_risk_revenue += revenue
                elif days_until_delivery <= 30:  # Within 1 month
                    at_risk_revenue += revenue * 0.5  # Partial risk
                    
        if total_revenue == 0:
            return None
            
        risk_ratio = at_risk_revenue / total_revenue
        
        # Convert to action urgency signal
        return risk_ratio * 2 - 1  # Scale to [-1, 1]
    
    def _assess_supplier_network(self, supplier_network: Dict) -> Optional[float]:
        """Assess supplier network flexibility"""
        
        if 'alternative_suppliers' not in supplier_network:
            return None
            
        alternative_suppliers = supplier_network['alternative_suppliers']
        total_suppliers = supplier_network.get('total_suppliers', 1)
        
        # Calculate supplier diversification
        diversification_ratio = len(alternative_suppliers) / total_suppliers
        
        # Assess average supplier capacity
        total_capacity = 0
        supplier_count = 0
        
        for supplier in alternative_suppliers:
            if 'available_capacity' in supplier:
                total_capacity += supplier['available_capacity']
                supplier_count += 1
                
        avg_capacity = total_capacity / supplier_count if supplier_count > 0 else 0
        
        # Combine diversification and capacity
        flexibility_score = (diversification_ratio * 0.6) + (avg_capacity * 0.4)
        
        # Convert to confidence in current supply chain
        return (flexibility_score * 2) - 1
    
    def _assess_financial_impact(self, 
                               cost_implications: Dict, 
                               budget_constraints: Optional[Dict]) -> Optional[float]:
        """Assess financial impact of disruption response"""
        
        additional_cost = cost_implications.get('additional_cost_estimate', 0)
        
        if budget_constraints:
            available_budget = budget_constraints.get('emergency_budget', float('inf'))
            if available_budget == 0:
                return 1.0  # No budget - high constraint
                
            cost_ratio = additional_cost / available_budget
            
            if cost_ratio <= 0.5:     # Within 50% of budget
                return -0.5           # Financially comfortable
            elif cost_ratio <= 1.0:   # Within budget
                return 0.0            # Neutral
            elif cost_ratio <= 2.0:   # Up to 2x budget
                return 0.5            # Concerning
            else:                     # More than 2x budget
                return 1.0            # Prohibitive
        else:
            # No budget information - assess based on absolute cost
            if additional_cost < 100000:      # Less than $100K
                return -0.3
            elif additional_cost < 500000:    # Less than $500K
                return 0.0
            elif additional_cost < 1000000:   # Less than $1M
                return 0.3
            else:                             # More than $1M
                return 0.7
    
    def _get_supply_chain_weights(self, market_conditions: Dict) -> Dict[str, float]:
        """Determine signal weights based on business priorities"""
        
        base_weights = {
            'disruption_severity': 0.25,     # Core disruption assessment
            'disruption_duration': 0.20,     # Timeline considerations
            'route_alternatives': 0.15,      # Solution availability
            'inventory_buffer': 0.20,        # Urgency based on stock
            'customer_impact': 0.10,         # Customer satisfaction
            'supplier_flexibility': 0.05,    # Network resilience
            'financial_impact': 0.05         # Cost considerations
        }
        
        # Adjust weights based on business context
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
            
        return base_weights
    
    def _apply_supply_chain_risk_management(self, 
                                          signals: Dict, 
                                          disruption_event: Dict,
                                          market_conditions: Dict) -> Dict:
        """Apply risk management overlay to signals"""
        
        risk_adjusted = signals.copy()
        
        # Critical inventory situation increases all urgency signals
        inventory_signal = signals.get('inventory_buffer', 0) or 0
        if inventory_signal > 0.7:  # Critical inventory
            for key in risk_adjusted:
                if risk_adjusted[key] is not None and risk_adjusted[key] > 0:
                    risk_adjusted[key] *= 1.3
                    
        # High-impact customers increase urgency
        customer_signal = signals.get('customer_impact', 0) or 0
        if customer_signal > 0.6:  # High customer impact
            for key in ['disruption_severity', 'disruption_duration']:
                if key in risk_adjusted and risk_adjusted[key] is not None:
                    risk_adjusted[key] = min(1.0, risk_adjusted[key] * 1.2)
                    
        return risk_adjusted
    
    def _design_sacred_pause_protocol(self, decision: TernaryResult) -> Dict:
        """Design Sacred Pause protocol for supply chain"""
        
        pause_duration_hours = max(4, min(48, (1 - decision.confidence) * 72))
        
        return {
            'pause_duration_hours': pause_duration_hours,
            'monitoring_frequency': 'every_2_hours',
            'escalation_triggers': [
                'inventory_drops_below_critical',
                'customer_complaints_increase',
                'disruption_severity_increases',
                'alternative_routes_become_unavailable'
            ],
            'communication_protocol': [
                'notify_stakeholders_of_pause',
                'explain_data_gathering_rationale',
                'provide_regular_status_updates',
                'communicate_decision_timeline'
            ]
        }
    
    def _log_supply_chain_decision(self, 
                                 decision: TernaryResult, 
                                 disruption_event: Dict,
                                 signals: Dict):
        """Log decision for supply chain analytics"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'disruption_type': disruption_event.get('event_type', 'unknown'),
            'decision': decision.state.name,
            'confidence': decision.confidence,
            'signals': {k: v for k, v in signals.items() if v is not None},
            'missing_signals': [k for k, v in signals.items() if v is None],
            'reasoning': decision.reasoning
        }
        
        # In production, this would write to supply chain analytics system
        print(f"Supply Chain Decision Log: {json.dumps(log_entry, indent=2)}")

def demonstrate_supply_chain_management():
    """
    Demonstrate the Supply Chain Management system with realistic scenarios
    """
    
    print("🚚 Global Supply Chain Management - Goukassian Framework")
    print("=" * 60)
    print()
    print("Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)")
    print("Contact: leogouk@gmail.com")
    print('"The Sacred Pause prevents supply chain overreactions."')
    print()
    
    # Initialize supply chain manager
    sc_manager = GlobalSupplyChainManager(
        confidence_threshold=0.70,
        cost_sensitivity=0.3,
        time_sensitivity=0.4
    )
    
    # Scenario 1: Major Route Disruption - Clear Action Needed
    print("🌊 Scenario 1: Suez Canal Blockage - Major Disruption")
    print("-" * 47)
    
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
        'business_type': 'customer_first'
    }
    
    decision = sc_manager.make_supply_chain_decision(
        major_disruption, major_route_info, major_market_conditions
    )
    implementation = sc_manager.implement_response_strategy(
        decision, major_disruption, major_route_info
    )
    
    print(f"Decision: {decision.state.name} (Confidence: {decision.confidence:.2f})")
    print(f"Action: {implementation['primary_action']}")
    print(f"Reasoning: {decision.reasoning}")
    print(f"Timeline: {implementation['implementation_timeline']} hours")
    print()
    
    # Scenario 2: Uncertain Geopolitical Situation
    print("⚠️  Scenario 2: Geopolitical Tensions - Uncertain Impact")
    print("-" * 53)
    
    uncertain_disruption = {
        'event_type': 'geopolitical_tension',
        'severity_reports': [
            {'severity': 0.4, 'confidence': 0.5, 'source': 'news_media'},
            {'severity': 0.6, 'confidence': 0.3, 'source': 'government_advisory'}
        ],
        'duration_estimates': {'estimated_days': None, 'confidence': 0.2},  # Unknown duration
        'cost_implications': {'additional_cost_estimate': None},  # Unknown costs
    }
    
    uncertain_route_info = {
        'alternative_routes': None,  # No alternatives assessed yet
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
        'demand_forecast': None,  # Forecast uncertain due to situation
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
    
    print(f"Decision: {decision.state.name} (Confidence: {decision.confidence:.2f})")
    print(f"Action: {implementation['primary_action']}")
    print(f"Reasoning: {decision.reasoning}")
    
    if decision.state == TernaryState.INDETERMINATE:
        print("Sacred Pause Protocol:")
        protocol = implementation['sacred_pause_protocol']
        print(f"  Pause Duration: {protocol['pause_duration_hours']} hours")
        print(f"  Monitoring: {protocol['monitoring_frequency']}")
        print("  Escalation Triggers:")
        for trigger in protocol['escalation_triggers'][:2]:
            print(f"    • {trigger}")
    print()
    
    # Scenario 3: Minor Disruption - Status Quo Appropriate
    print("✅ Scenario 3: Minor Weather Delay - Maintain Operations")
    print("-" * 54)
    
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
        'cost_comparisons': {'alternative_port': 1.1}  # Only 10% more expensive
    }
    
    minor_market_conditions = {
        'current_inventory': {'electronics': 1200, 'textiles': 900},  # Good inventory
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
    
    print(f"Decision: {decision.state.name} (Confidence: {decision.confidence:.2f})")
    print(f"Action: {implementation['primary_action']}")
    print(f"Reasoning: {decision.reasoning}")
    print()
    
    print("📊 Supply Chain Management Summary")
    print("-" * 34)
    print("The Goukassian Framework enables supply chain managers to:")
    print("• Avoid costly overreactions to uncertain disruptions")
    print("• Implement graduated responses based on confidence levels")
    print("• Maintain operational efficiency during minor disruptions")
    print("• Gather critical data before making major route changes")
    print("• Balance multiple competing priorities intelligently")
    print()
    print("As Lev Goukassian noted: 'The Sacred Pause prevents")
    print("supply chain overreactions while ensuring adequate response")
    print("to genuine threats.'")

if __name__ == "__main__":
    demonstrate_supply_chain_management()
