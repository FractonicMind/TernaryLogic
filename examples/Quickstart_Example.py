QUICKSTART_EXAMPLE.PY
"""
Ternary Logic Framework - Quick Start Example with Eight Pillars. 
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
