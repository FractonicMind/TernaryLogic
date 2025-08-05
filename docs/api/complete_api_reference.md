# Ternary Logic Framework - Complete API Reference

**Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)**  

*Complete technical reference for implementing Ternary Logic in economic systems*

---

## Core Classes

### TLState

**Enumeration representing the three states of ternary logic**

```python
from ternary_logic import TLState

class TLState(Enum):
    PROCEED = 1          # High confidence to proceed
    HALT = -1            # High confidence to stop/reject
    EPISTEMIC_HOLD = 0   # Insufficient data - Epistemic Hold
```

**Methods:**
- `__str__()` → `str`: Returns human-readable state name
- `__repr__()` → `str`: Returns formal state representation

**Example:**
```python
state = TLState.EPISTEMIC_HOLD
print(state)  # Output: "EPISTEMIC_HOLD"
print(repr(state))  # Output: "TLState.EPISTEMIC_HOLD"
```

---

### TLValue

**Core ternary value with market uncertainty handling**

```python
from ternary_logic.core import TLValue

class TLValue:
    def __init__(self, value: Union[float, int, None], confidence: float = 1.0)
```

**Parameters:**
- `value` (float | int | None): The numeric value (None = missing/unknown market data)
- `confidence` (float): Confidence level between 0.0 and 1.0

**Properties:**
- `value`: The underlying numeric value
- `confidence`: Confidence level (automatically clamped to [0,1])
- `state`: Computed TLState based on value and confidence

**Methods:**

#### Logical Operations
```python
def __and__(self, other: 'TLValue') -> 'TLValue'
def __or__(self, other: 'TLValue') -> 'TLValue'  
def __invert__(self) -> 'TLValue'
```

**Truth Tables:**

| A | B | A AND B | A OR B |
|---|---|---------|--------|
| P | P | P | P |
| P | H | H | P |
| P | E | E | P |
| H | H | H | H |
| H | E | H | E |
| E | E | E | E |

*Where P=PROCEED, H=HALT, E=EPISTEMIC_HOLD*

**Example:**
```python
high_confidence = TLValue(0.8, confidence=0.9)
low_confidence = TLValue(0.6, confidence=0.4)

print(high_confidence.state)  # TLState.PROCEED
print(low_confidence.state)   # TLState.EPISTEMIC_HOLD

combined = high_confidence & low_confidence
print(combined.state)  # TLState.EPISTEMIC_HOLD (weakest link)
```

---

### TLResult

**Result container for economic decisions with full market context**

```python
from ternary_logic.core import TLResult

@dataclass
class TLResult:
    state: TLState
    confidence: float
    reasoning: str
    clarifying_questions: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
```

**Attributes:**
- `state`: The ternary decision state
- `confidence`: Numeric confidence level (0.0 to 1.0)
- `reasoning`: Human-readable explanation of the decision
- `clarifying_questions`: Recommended data gathering (especially for EPISTEMIC_HOLD states)
- `metadata`: Additional context and market information

**Example:**
```python
result = TLResult(
    state=TLState.EPISTEMIC_HOLD,
    confidence=0.45,
    reasoning="Conflicting market signals require additional analysis",
    clarifying_questions=[
        "What is the current options flow?",
        "Are there pending economic announcements?",
        "What is the sector correlation?"
    ],
    metadata={
        "missing_data": ["volume_analysis", "sector_rotation"],
        "signal_count": 4,
        "complexity_score": 0.8
    }
)
```

---

### TLEvaluator

**Main evaluator for economic decision-making with Epistemic Hold logic**

```python
from ternary_logic.core import TLEvaluator

class TLEvaluator:
    def __init__(self, 
                halt_threshold: float = 0.3,
                hold_threshold: float = 0.7)
```

**Parameters:**
- `halt_threshold` (float): Below this confidence, strongly consider halting
- `hold_threshold` (float): Below this confidence, engage epistemic hold

**Methods:**

#### evaluate()
```python
def evaluate(self, 
            request: str,
            context: Optional[Dict[str, Any]] = None) -> TLResult
```

**Parameters:**
- `request`: Economic decision request in natural language
- `context`: Market context and signals

**Returns:**
- `TLResult`: Complete decision result with reasoning and questions

**Epistemic Hold Logic:**
- If confidence < halt_threshold: Return HALT
- If confidence < hold_threshold or complexity > 0.7: Return EPISTEMIC_HOLD
- Otherwise: Return PROCEED based on signal direction

**Example:**
```python
evaluator = TLEvaluator(halt_threshold=0.3, hold_threshold=0.7)

result = evaluator.evaluate(
    "Should I execute this large block trade?",
    context={
        'market_volatility': 'elevated',
        'liquidity_conditions': 'moderate',
        'news_sentiment': 'mixed',
        'technical_signals': 'bullish',
        'position_size': 'large'
    }
)

print(result.state)  # Likely EPISTEMIC_HOLD due to elevated volatility
```

---

### TLDecisionEngine

**Enhanced decision engine with domain-specific trading features**

```python
from ternary_logic.core import TLDecisionEngine

class TLDecisionEngine(TLEvaluator):
    def __init__(self, 
                halt_threshold: float = 0.3,
                hold_threshold: float = 0.7, 
                domain: str = "general")
```

**Parameters:**
- `halt_threshold`: Below this confidence, strongly consider halting
- `hold_threshold`: Below this confidence, engage epistemic hold
- `domain`: Domain context ("trading", "policy", "supply_chain", "general")

**Additional Features:**
- Domain-specific enhancement of results
- Decision history tracking
- Performance analytics
- Specialized market recommendations

**Methods:**

#### decide()
```python
def decide(self, 
          request: str,
          context: Optional[Dict[str, Any]] = None,
          scenario: Optional[str] = None) -> TLResult
```

**Enhanced version of evaluate() with:**
- Domain-specific result enhancement
- Scenario tracking for improved recommendations
- Decision logging for performance analysis

#### get_decision_summary()
```python
def get_decision_summary() -> Dict[str, Any]
```

**Returns summary statistics:**
- Total decisions made
- State distribution (PROCEED/HALT/EPISTEMIC_HOLD percentages)
- Average confidence levels
- Epistemic Hold frequency
- Domain-specific metrics

**Example:**
```python
engine = TLDecisionEngine(domain="trading")

# Make several trading decisions...
for scenario in trading_scenarios:
    result = engine.decide(scenario['request'], scenario['context'])
    
# Get performance summary
summary = engine.get_decision_summary()
print(f"Epistemic Hold Rate: {summary['epistemic_hold_rate']:.1%}")
print(f"Average Confidence: {summary['average_confidence']:.2f}")
```

---

## Domain-Specific Applications

### Financial Trading

#### TradingAgent
```python
from ternary_logic.trading import TradingAgent

class TradingAgent:
    def __init__(self, 
                halt_threshold: float = 0.25,
                hold_threshold: float = 0.75,
                risk_tolerance: float = 0.3)
    
    def evaluate_trade_opportunity(self,
                                 symbol: str,
                                 market_data: Dict,
                                 uncertainty_tolerance: float = 0.2) -> TLResult
```

**Market Data Structure:**
```python
market_data = {
    'price_data': [100.0, 101.5, 102.1, ...],  # Historical prices
    'volume': 1500000,                          # Trading volume
    'sentiment': 0.3,                           # Market sentiment (-1 to 1)
    'technical_indicators': {
        'rsi': 65.4,
        'macd': 0.15,
        'bollinger_position': 0.7
    },
    'news_events': ['earnings_beat', 'analyst_upgrade'],
    'order_book': {
        'bid_size': 10000,
        'ask_size': 8500,
        'spread': 0.02
    }
}
```

#### PortfolioOptimizer
```python
from ternary_logic.trading import PortfolioOptimizer

class PortfolioOptimizer:
    def optimize_portfolio(self,
                          assets: Dict[str, Dict],
                          target_return: float,
                          max_risk: float) -> TLResult
```

**Asset Structure:**
```python
assets = {
    'AAPL': {
        'expected_return': 0.12,
        'volatility': 0.25,
        'data_quality': 0.9,        # Confidence in estimates
        'liquidity': 0.95
    },
    'CRYPTO_XYZ': {
        'expected_return': None,     # Unknown!
        'volatility': 0.80,
        'data_quality': 0.3,        # Low confidence
        'liquidity': 0.6
    }
}
```

### Supply Chain Management

#### DisruptionHandler
```python
from ternary_logic.supply_chain import DisruptionHandler

class DisruptionHandler:
    def evaluate_route_disruption(self,
                                event_data: Dict,
                                supply_chain_state: Dict) -> TLResult
```

**Event Data Structure:**
```python
event_data = {
    'event_type': 'geopolitical_tension',
    'severity': 0.7,              # 0 to 1 scale
    'duration_estimate': 14,       # Days
    'confidence': 0.4,            # Low confidence in estimates
    'affected_routes': ['suez_canal', 'trans_pacific'],
    'alternative_costs': {
        'cape_of_good_hope': 1.4,  # 140% of normal cost
        'air_freight': 3.2         # 320% of normal cost
    }
}
```

### Central Banking Policy

#### MonetaryPolicyEngine
```python
from ternary_logic.policy import MonetaryPolicyEngine

class MonetaryPolicyEngine:
    def evaluate_policy_options(self,
                               economic_indicators: Dict,
                               policy_options: Dict,
                               mandate_priorities: List[str]) -> TLResult
```

**Economic Indicators Structure:**
```python
economic_indicators = {
    'inflation_rate': {'value': 0.025, 'confidence': 0.8, 'trend': 'rising'},
    'unemployment': {'value': 0.045, 'confidence': 0.9, 'trend': 'stable'},
    'gdp_growth': {'value': None, 'confidence': 0.0, 'trend': 'unknown'},
    'financial_conditions': {'value': -0.5, 'confidence': 0.7, 'trend': 'easing'}
}
```

---

## Configuration and Customization

### Confidence Threshold Calibration

**Domain-Specific Recommended Thresholds:**

```python
RECOMMENDED_THRESHOLDS = {
    'high_frequency_trading': {
        'halt': 0.2,    # Conservative 
        'hold': 0.85    # Low uncertainty tolerance
    },
    'portfolio_management': {
        'halt': 0.3,
        'hold': 0.7     # Balanced approach
    },
    'options_trading': {
        'halt': 0.25,
        'hold': 0.8     # Higher precision needed
    },
    'supply_chain': {
        'halt': 0.35,
        'hold': 0.65    # More tolerance for uncertainty
    },
    'monetary_policy': {
        'halt': 0.4,
        'hold': 0.6     # Policy flexibility important
    }
}
```

### Custom Confidence Functions

```python
def market_confidence_function(price_quality: float,
                             volume_profile: float,
                             news_clarity: float,
                             technical_agreement: float) -> float:
    """
    Custom confidence calculation for market decisions
    
    Args:
        price_quality: Price discovery efficiency (0-1)
        volume_profile: Volume pattern reliability (0-1)
        news_clarity: Information clarity (0-1)
        technical_agreement: Technical indicator consensus (0-1)
    
    Returns:
        Overall confidence score (0-1)
    """
    weights = [0.3, 0.3, 0.2, 0.2]  # Customizable weights
    factors = [price_quality, volume_profile, news_clarity, technical_agreement]
    
    # Apply uncertainty penalty for missing factors
    penalty = sum(1 for f in factors if f < 0.1) * 0.1
    
    return max(0, sum(w * f for w, f in zip(weights, factors)) - penalty)
```

### Signal Aggregation Methods

**Built-in Aggregation Methods:**

```python
from ternary_logic.utils import MarketAggregation

# Weighted average (default)
result = MarketAggregation.weighted_average(signals, weights, confidences)

# Volatility-adjusted mean
result = MarketAggregation.volatility_adjusted(signals, volatilities)

# Correlation-weighted aggregate
result = MarketAggregation.correlation_weighted(signals, correlation_matrix)

# Robust median with outlier detection
result = MarketAggregation.robust_median(signals, outlier_threshold=2.0)
```

---

## Error Handling and Validation

### Common Exceptions

```python
from ternary_logic.exceptions import (
    InsufficientMarketDataError,
    InvalidConfidenceError,
    ThresholdCalibrationError,
    MarketClosedError
)

try:
    result = evaluator.evaluate(request, context)
except InsufficientMarketDataError as e:
    print(f"Not enough market data: {e}")
    # Implement data gathering protocol
    
except MarketClosedError as e:
    print(f"Market closed: {e}")
    # Queue for next trading session
    
except ThresholdCalibrationError as e:
    print(f"Thresholds need adjustment: {e}")
    # Recalibrate for current market regime
```

### Input Validation

```python
from ternary_logic.utils import validate_market_context

# Validate market context
try:
    validate_market_context(context)
except ValueError as e:
    print(f"Invalid market context: {e}")
    
# Check for required market signals
required_signals = ['price', 'volume', 'volatility']
missing_signals = [signal for signal in required_signals 
                  if signal not in context or context[signal] is None]

if missing_signals:
    print(f"Critical market data missing: {missing_signals}")
    # Cannot proceed with trading decision
```

---

## Performance Optimization

### Batch Processing

```python
from ternary_logic.utils import BatchProcessor

processor = BatchProcessor(evaluator)

# Process multiple trading decisions efficiently
trades = [trade1, trade2, trade3, ...]
results = processor.evaluate_batch(trades, parallel=True, max_workers=4)

# Get aggregated statistics
batch_stats = processor.get_batch_statistics(results)
print(f"Batch Epistemic Hold Rate: {batch_stats['hold_rate']:.1%}")
```

### Caching and Memoization

```python
from ternary_logic.utils import CachedEvaluator

# Enable intelligent caching for repeated similar decisions
cached_evaluator = CachedEvaluator(
    base_evaluator=evaluator,
    cache_size=1000,
    similarity_threshold=0.95,
    ttl_seconds=300  # 5-minute cache for market data
)

result = cached_evaluator.evaluate(request, context)  # May use cached result
```

### Memory Management

```python
# Configure memory usage for high-frequency applications
engine.configure_memory(
    max_history_size=10000,     # Limit decision history
    cleanup_interval=3600,      # Cleanup old data hourly
    market_cache_size=5000      # Cache market calculations
)
```

---

## Integration Examples

### Pandas Integration

```python
import pandas as pd
from ternary_logic.integrations import pandas_integration

# Apply ternary logic to market data DataFrame
df = pd.DataFrame({
    'rsi': [30, 70, 50, 85],
    'macd': [0.5, -0.3, None, 0.8],
    'volume_ratio': [1.2, 0.8, 1.5, None],
    'news_sentiment': [0.6, -0.4, 0.2, 0.7]
})

results = pandas_integration.evaluate_trades(df, evaluator)
print(results[['decision', 'confidence', 'reasoning']])
```

### Trading Platform Integration

```python
from ternary_logic.integrations import trading_platforms

# Interactive Brokers integration
ib_integration = trading_platforms.IBIntegration(evaluator)
ib_integration.connect()

# Evaluate real-time trading opportunity
market_data = ib_integration.get_market_data('AAPL')
decision = ib_integration.evaluate_trade('AAPL', market_data)

if decision.state == TLState.PROCEED:
    ib_integration.place_order('AAPL', 100, 'BUY')
elif decision.state == TLState.EPISTEMIC_HOLD:
    print(f"Waiting for: {decision.clarifying_questions}")
```

### REST API Integration

```python
from ternary_logic.integrations import rest_api

# Create REST API endpoint for ternary decisions
app = rest_api.create_trading_api(evaluator)

# Example request:
# POST /api/evaluate
# {
#   "request": "Should I buy TSLA?",
#   "context": {
#     "current_price": 750.50,
#     "volatility": "high",
#     "news": "mixed",
#     "technicals": "bullish"
#   }
# }
#
# Response:
# {
#   "decision": "EPISTEMIC_HOLD",
#   "confidence": 0.55,
#   "reasoning": "High volatility with mixed news signals",
#   "clarifying_questions": [
#     "What is the options flow indicating?",
#     "Are there upcoming catalysts?"
#   ]
# }
```

---

## Monitoring and Analytics

### Trading Performance Metrics

```python
from ternary_logic.analytics import TradingAnalyzer

analyzer = TradingAnalyzer(engine)

# Analyze trading performance
performance = analyzer.calculate_performance(
    decisions=trading_history,
    market_outcomes=actual_prices,
    time_window='30d'
)

print(f"Win Rate (excluding holds): {performance['win_rate']:.2%}")
print(f"Epistemic Hold Value: {performance['hold_savings']:.2%}")
print(f"Optimal Thresholds: {performance['optimal_thresholds']}")
```

### Real-time Monitoring

```python
from ternary_logic.monitoring import MarketMonitor

monitor = MarketMonitor(engine)

# Set up monitoring dashboards
monitor.track_metrics([
    'decision_rate',
    'hold_frequency', 
    'confidence_distribution',
    'profit_loss'
])

# Real-time alerts
monitor.set_alert('hold_rate_high', threshold=0.4, action='notify_trader')
monitor.set_alert('confidence_low', threshold=0.5, action='pause_trading')
```

---

## Version Information

**Current Version:** 1.0.0  
**API Stability:** Stable  
**Python Compatibility:** 3.8+  
**Dependencies:** numpy>=1.19.0, pandas>=1.3.0, scipy>=1.7.0

---

*"This API reference provides the complete technical foundation for implementing the Epistemic Hold in your economic decision-making systems. The future is ternary."*

## Contact Information

**Created by Lev Goukassian**
* **ORCID**: 0009-0006-5966-1243
* **Email**: leogouk@gmail.com

**Successor Contact**: support@tl-goukassian.org  
(see [Succession Charter](/memorial/SUCCESSION_CHARTER.md))
