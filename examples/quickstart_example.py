"""
Ternary Logic Framework - Quick Start Example
Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com

This example demonstrates the basic usage of the Ternary Logic Framework
for intelligent decision-making under uncertainty.

"The world is not binary. And the future will not be either."
"""

from ternary_logic import TLDecisionEngine, TLState

def main():
    print("🚀 Ternary Logic Framework - Quick Start Demo")
    print("=" * 50)
    print()
    
    # Initialize the decision engine
    engine = TLDecisionEngine(confidence_threshold=0.7, domain="financial")
    
    print("📊 Example 1: Clear Positive Decision")
    print("-" * 35)
    
    # Strong positive signals across all criteria
    criteria_positive = {
        'market_sentiment': 0.8,      # Strong positive
        'technical_indicators': 0.6,  # Moderately positive  
        'volume_analysis': 0.7,       # Good volume
        'fundamental_analysis': 0.9   # Very strong fundamentals
    }
    
    result = engine.decide(criteria_positive, context="Strong bull market conditions")
    print_result(result)
    print()
    
    print("⚠️  Example 2: Uncertain Decision with Missing Data")
    print("-" * 48)
    
    # Mixed signals with missing critical data
    criteria_uncertain = {
        'market_sentiment': 0.3,      # Weak positive
        'technical_indicators': -0.4,  # Negative signal
        'volume_analysis': None,      # Missing data!
        'fundamental_analysis': 0.2   # Weak positive
    }
    
    result = engine.decide(criteria_uncertain, context="Contradictory market signals")
    print_result(result)
    print()
    
    print("❌ Example 3: Clear Negative Decision")
    print("-" * 34)
    
    # Strong negative signals across all criteria
    criteria_negative = {
        'market_sentiment': -0.8,     # Very bearish
        'technical_indicators': -0.6, # Technical breakdown
        'volume_analysis': -0.5,      # Poor volume
        'fundamental_analysis': -0.7  # Weak fundamentals
    }
    
    result = engine.decide(criteria_negative, context="Bear market conditions")
    print_result(result)
    print()
    
    print("🔍 Example 4: Custom Weights")
    print("-" * 25)
    
    # Same data as Example 2, but with custom importance weights
    weights = {
        'market_sentiment': 0.2,      # Lower importance
        'technical_indicators': 0.3,  # Standard importance
        'volume_analysis': 0.4,       # Higher importance (even though missing!)
        'fundamental_analysis': 0.1   # Lower importance
    }
    
    result = engine.decide(criteria_uncertain, weights=weights, 
                          context="Weighted analysis with volume focus")
    print_result(result)
    print()
    
    print("📈 Decision History Summary")
    print("-" * 25)
    summary = engine.get_decision_summary()
    print(f"Total Decisions Made: {summary['total_decisions']}")
    print(f"Average Confidence: {summary['average_confidence']:.2f}")
    print(f"Epistemic Hold Rate: {summary['epistemic_hold_rate']:.1%}")
    print()
    print("Decision Distribution:")
    for state, count in summary['state_distribution'].items():
        percentage = (count / summary['total_decisions']) * 100
        print(f"  {state}: {count} ({percentage:.1f}%)")
    
    print()
    print("✨ The Epistemic Hold in Action!")
    print("Notice how the framework intelligently recognizes uncertainty")
    print("and recommends gathering more information rather than forcing")  
    print("a premature binary decision.")
    print()
    print('As Lev Goukassian said: "The world is not binary.')
    print('And the future will not be either."')

def print_result(result):
    """Helper function to nicely format and print results"""
    
    # State with emoji
    state_emoji = {
        TLState.PROCEED: "✅",
        TLState.HALT: "❌", 
        TLState.EPISTEMIC_HOLD: "⚠️"
    }
    
    print(f"Decision: {state_emoji[result.state]} {result.state.name}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reasoning: {result.reasoning}")
    
    if result.next_steps:
        print("Recommended Next Steps:")
        for i, step in enumerate(result.next_steps[:3], 1):  # Show first 3 steps
            print(f"  {i}. {step}")
        if len(result.next_steps) > 3:
            print(f"  ... and {len(result.next_steps)-3} more steps")
    
    if result.metadata and result.metadata.get('missing_data'):
        missing = result.metadata['missing_data']
        print(f"Missing Data: {', '.join(missing)}")

if __name__ == "__main__":
    main()

## Contact Information

**Created by Lev Goukassian**
* **ORCID**: 0009-0006-5966-1243
* **Email**: leogouk@gmail.com

**Successor Contact**: support@tl-goukassian.org  
(see [Succession Charter](/memorial/SUCCESSION_CHARTER.md))
