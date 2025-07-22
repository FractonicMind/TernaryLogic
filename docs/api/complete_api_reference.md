# Goukassian Framework - Complete API Reference

**Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)**  
**Contact: leogouk@gmail.com**

*Complete technical reference for implementing Ternary Logic in your systems*

---

## Core Classes

### TernaryState

**Enumeration representing the three states of ternary logic**

```python
from goukassian import TernaryState

class TernaryState(Enum):
    TRUE = 1          # High confidence to proceed
    FALSE = 0         # High confidence to stop/reject
    INDETERMINATE = -1  # Insufficient data - Sacred Pause
```

**Methods:**
- `__str__()` → `str`: Returns human-readable state name
- `__repr__()` → `str`: Returns formal state representation

**Example:**
```python
state = TernaryState.INDETERMINATE
print(state)  # Output: "INDETERMINATE"
print(repr(state))  # Output: "TernaryState.INDETERMINATE"
```

---

### TernaryValue

**Core ternary value with uncertainty handling**

```python
from goukassian.core import TernaryValue

class TernaryValue:
    def __init__(self, value: Union[float, int, None], confidence: float = 1.0)
```

**Parameters:**
- `value` (float | int | None): The numeric value (None = missing/unknown data)
- `confidence` (float): Confidence level between 0.0 and 1.0

**Properties:**
- `value`: The underlying numeric value
- `confidence`: Confidence level (automatically clamped to [0,1])
- `state`: Computed TernaryState based on value and confidence

**Methods:**

#### Logical Operations
```python
def __and__(self, other: 'TernaryValue') -> 'TernaryValue'
def __or__(self, other: 'TernaryValue') -> 'TernaryValue'  
def __invert__(self) -> 'TernaryValue'
```

**Truth Tables:**

| A | B | A AND B | A OR B |
|---|---|---------|--------|
| T | T | T | T |
| T | F | F | T |
| T | I | I | T |
| F | F | F | F |
| F | I | F | I |
| I | I | I | I |

*Where T=TRUE, F=FALSE, I=INDETERMINATE*

**Example:**
```python
high_confidence = TernaryValue(0.8, confidence=0.9)
low_confidence = TernaryValue(0.6, confidence=0.4)

print(high_confidence.state)  # TernaryState.TRUE
print(low_confidence.state)   # TernaryState.INDETERMINATE

combined = high_confidence & low_confidence
print(combined.state)  # TernaryState.INDETERMINATE (weakest link)
```

---

### TernaryResult

**Result container for ternary decisions with full context**

```python
from goukassian.core import TernaryResult

@dataclass
class TernaryResult:
    state: TernaryState
    confidence: float
    reasoning: str
    next_steps: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
```

**Attributes:**
- `state`: The ternary decision state
- `confidence`: Numeric confidence level (0.0 to 1.0)
- `reasoning`: Human-readable explanation of the decision
- `next_steps`: Recommended actions (especially for INDETERMINATE states)
- `metadata`: Additional context and debugging information

**Example:**
```python
result = TernaryResult(
    state=TernaryState.INDETERMINATE,
    confidence=0.45,
    reasoning="Conflicting market signals require additional analysis",
    next_steps=[
        "Gather additional market sentiment data",
        "Wait for earnings announcement",
        "Re-evaluate in 2 hours"
    ],
    metadata={
        "missing_data": ["volume_analysis", "sector_rotation"],
        "signal_count": 4,
        "threshold": 0.7
    }
)
```

---

### TernaryLogicEngine

**Main engine for ternary decision-making with Sacred Pause logic**

```python
from goukassian.core import TernaryLogicEngine

class TernaryLogicEngine:
    def __init__(self, confidence_threshold: float = 0.7)
```

**Parameters:**
- `confidence_threshold` (float): Minimum confidence for TRUE/FALSE decisions

**Methods:**

#### evaluate()
```python
def evaluate(self, 
            criteria: Dict[str, Union[float, None]], 
            weights: Optional[Dict[str, float]] = None) -> TernaryResult
```

**Parameters:**
- `criteria`: Dictionary mapping criterion names to values (None = missing data)
- `weights`: Optional importance weights for each criterion

**Returns:**
- `TernaryResult`: Complete decision result with reasoning and next steps

**Sacred Pause Logic:**
- If aggregate confidence ≥ threshold: Return TRUE/FALSE based on value
- If aggregate confidence < threshold: Return INDETERMINATE (Sacred Pause)

**Example:**
```python
engine = TernaryLogicEngine(confidence_threshold=0.75)

criteria = {
    'market_sentiment': 0.6,    # Moderately positive
    'technical_analysis': -0.3,  # Slightly negative
    'volume_data': None,        # Missing!
    'news_sentiment': 0.8       # Very positive
}

weights = {
    'market_sentiment': 0.3,
    'technical_analysis': 0.2,
    'volume_data': 0.4,         # High weight but missing data
    'news_sentiment': 0.1
}

result = engine.evaluate(criteria, weights)
print(result.state)  # Likely INDETERMINATE due to missing volume_data
```

---

### TernaryDecisionEngine

**Enhanced decision engine with domain-specific features**

```python
from goukassian.core import TernaryDecisionEngine

class TernaryDecisionEngine(TernaryLogicEngine):
    def __init__(self, 
                confidence_threshold: float = 0.7, 
                domain: str = "general")
```

**Parameters:**
- `confidence_threshold`: Minimum confidence for binary decisions
- `domain`: Domain context ("financial", "medical", "policy", "general")

**Additional Features:**
- Domain-specific enhancement of results
- Decision history tracking
- Performance analytics
- Specialized next-step recommendations

**Methods:**

#### decide()
```python
def decide(self, 
          criteria: Dict[str, Union[float, None]], 
          weights: Optional[Dict[str, float]] = None,
          context: Optional[str] = None) -> TernaryResult
```

**Enhanced version of evaluate() with:**
- Domain-specific result enhancement
- Context tracking for improved recommendations
- Decision logging for performance analysis

#### get_decision_summary()
```python
def get_decision_summary() -> Dict[str, Any]
```

**Returns summary statistics:**
- Total decisions made
- State distribution (TRUE/FALSE/INDETERMINATE percentages)
- Average confidence levels
- Sacred Pause frequency
- Domain-specific metrics

**Example:**
```python
engine = TernaryDecisionEngine(domain="financial")

# Make several decisions...
for scenario in trading_scenarios:
    result = engine.decide(scenario['criteria'], context=scenario['context'])
    
# Get performance summary
summary = engine.get_decision_summary()
print(f"Sacred Pause Rate: {summary['indeterminate_rate']:.1%}")
print(f"Average Confidence: {summary['average_confidence']:.2f}")
```

---

## Domain-Specific Applications

### Financial Trading

#### TradingAgent
```python
from goukassian.financial import TradingAgent

class TradingAgent:
    def __init__(self, 
                confidence_threshold: float = 0.75,
                risk_tolerance: float = 0.3)
    
    def evaluate_trade_opportunity(self,
                                 symbol: str,
                                 market_data: Dict,
                                 uncertainty_tolerance: float = 0.2) -> TernaryResult
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
from goukassian.financial import PortfolioOptimizer

class PortfolioOptimizer:
    def optimize_portfolio(self,
                          assets: Dict[str, Dict],
                          target_return: float,
                          max_risk: float) -> TernaryResult
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
from goukassian.supply_chain import DisruptionHandler

class DisruptionHandler:
    def evaluate_route_disruption(self,
                                event_data: Dict,
                                supply_chain_state: Dict) -> TernaryResult
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
from goukassian.policy import MonetaryPolicyEngine

class MonetaryPolicyEngine:
    def evaluate_policy_options(self,
                               economic_indicators: Dict,
                               policy_options: Dict,
                               mandate_priorities: List[str]) -> TernaryResult
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
    'high_frequency_trading': 0.85,    # Low uncertainty tolerance
    'strategic_planning': 0.65,        # Moderate uncertainty acceptable
    'emergency_response': 0.45,        # Action required despite uncertainty
    'research_decisions': 0.75,        # Scientific rigor required
    'medical_diagnosis': 0.80,         # Patient safety priority
    'financial_regulation': 0.70       # Balanced approach
}
```

### Custom Confidence Functions

```python
def custom_confidence_function(data_quality: float,
                             source_reliability: float,
                             temporal_relevance: float,
                             cross_validation: float) -> float:
    """
    Custom confidence calculation for domain-specific needs
    
    Args:
        data_quality: Completeness and accuracy of data (0-1)
        source_reliability: Historical accuracy of source (0-1)
        temporal_relevance: How recent/relevant the data is (0-1)
        cross_validation: Agreement with other sources (0-1)
    
    Returns:
        Overall confidence score (0-1)
    """
    weights = [0.3, 0.3, 0.2, 0.2]  # Customizable weights
    factors = [data_quality, source_reliability, temporal_relevance, cross_validation]
    
    return sum(w * f for w, f in zip(weights, factors))

# Use in TernaryLogicEngine
engine = TernaryLogicEngine()
engine.confidence_function = custom_confidence_function
```

### Signal Aggregation Methods

**Built-in Aggregation Methods:**

```python
from goukassian.utils import AggregationMethods

# Weighted average (default)
result = AggregationMethods.weighted_average(values, weights, confidences)

# Confidence-weighted geometric mean
result = AggregationMethods.confidence_geometric_mean(values, confidences)

# Uncertainty-penalized average
result = AggregationMethods.uncertainty_penalized(values, confidences, penalty=0.5)

# Robust median with outlier detection
result = AggregationMethods.robust_median(values, confidences, outlier_threshold=2.0)
```

---

## Error Handling and Validation

### Common Exceptions

```python
from goukassian.exceptions import (
    InsufficientDataError,
    InvalidConfidenceError,
    ThresholdCalibrationError,
    DomainMismatchError
)

try:
    result = engine.evaluate(criteria)
except InsufficientDataError as e:
    print(f"Not enough data for decision: {e}")
    # Implement data gathering protocol
    
except InvalidConfidenceError as e:
    print(f"Confidence values out of range: {e}")
    # Check confidence calculations
    
except ThresholdCalibrationError as e:
    print(f"Confidence threshold needs adjustment: {e}")
    # Recalibrate threshold for domain
```

### Input Validation

```python
from goukassian.utils import validate_criteria, validate_weights

# Validate input structure
try:
    validate_criteria(criteria)
    validate_weights(weights, criteria.keys())
except ValueError as e:
    print(f"Input validation failed: {e}")
    
# Check for required minimum data
min_required_fields = ['market_sentiment', 'technical_analysis']
missing_fields = [field for field in min_required_fields 
                 if field not in criteria or criteria[field] is None]

if missing_fields:
    print(f"Critical fields missing: {missing_fields}")
    # Cannot proceed with decision
```

---

## Performance Optimization

### Batch Processing

```python
from goukassian.utils import BatchProcessor

processor = BatchProcessor(engine)

# Process multiple decisions efficiently
scenarios = [scenario1, scenario2, scenario3, ...]
results = processor.evaluate_batch(scenarios, parallel=True, max_workers=4)

# Get aggregated statistics
batch_stats = processor.get_batch_statistics(results)
print(f"Batch Sacred Pause Rate: {batch_stats['pause_rate']:.1%}")
```

### Caching and Memoization

```python
from goukassian.utils import CachedTernaryEngine

# Enable intelligent caching for repeated similar decisions
cached_engine = CachedTernaryEngine(
    base_engine=engine,
    cache_size=1000,
    similarity_threshold=0.95
)

result = cached_engine.evaluate(criteria)  # May use cached result
```

### Memory Management

```python
# Configure memory usage for large-scale applications
engine.configure_memory(
    max_history_size=10000,     # Limit decision history
    cleanup_interval=3600,      # Cleanup old data hourly
    confidence_cache_size=5000  # Cache confidence calculations
)
```

---

## Integration Examples

### Pandas Integration

```python
import pandas as pd
from goukassian.integrations import pandas_integration

# Apply ternary logic to DataFrame
df = pd.DataFrame({
    'signal_1': [0.5, -0.3, None, 0.8],
    'signal_2': [0.2, 0.7, -0.4, None],
    'confidence_1': [0.9, 0.6, 0.0, 0.95],
    'confidence_2': [0.8, 0.85, 0.7, 0.0]
})

results = pandas_integration.apply_ternary_logic(df, engine)
print(results[['decision', 'confidence', 'reasoning']])
```

### Scikit-learn Integration

```python
from goukassian.integrations import sklearn_integration
from sklearn.ensemble import RandomForestClassifier

# Combine traditional ML with ternary logic
ml_model = RandomForestClassifier()
ternary_classifier = sklearn_integration.TernaryClassifier(
    base_model=ml_model,
    confidence_method='prediction_proba',
    threshold=0.75
)

# Fit and predict with uncertainty awareness
ternary_classifier.fit(X_train, y_train)
predictions = ternary_classifier.predict(X_test)  # Includes INDETERMINATE class
```

### REST API Integration

```python
from goukassian.integrations import rest_api

# Create REST API endpoint for ternary decisions
app = rest_api.create_ternary_api(engine)

# Example request:
# POST /api/decide
# {
#   "criteria": {"signal_1": 0.5, "signal_2": null},
#   "weights": {"signal_1": 0.7, "signal_2": 0.3},
#   "context": "trading_decision"
# }
#
# Response:
# {
#   "decision": "INDETERMINATE",
#   "confidence": 0.45,
#   "reasoning": "Missing critical signal_2 data",
#   "next_steps": ["Gather signal_2 data", "Re-evaluate in 15 minutes"]
# }
```

---

## Monitoring and Analytics

### Decision Quality Metrics

```python
from goukassian.analytics import DecisionAnalyzer

analyzer = DecisionAnalyzer(engine)

# Analyze decision quality over time
quality_metrics = analyzer.calculate_quality_metrics(
    decisions=decision_history,
    outcomes=actual_outcomes,
    time_window='30d'
)

print(f"Decision Accuracy: {quality_metrics['accuracy']:.2%}")
print(f"Sacred Pause Effectiveness: {quality_metrics['pause_value']:.2%}")
print(f"Optimal Threshold: {quality_metrics['optimal_threshold']:.2f}")
```

### Real-time Monitoring

```python
from goukassian.monitoring import TernaryMonitor

monitor = TernaryMonitor(engine)

# Set up monitoring dashboards
monitor.track_metrics([
    'decision_rate',
    'pause_frequency', 
    'confidence_distribution',
    'error_rates'
])

# Real-time alerts
monitor.set_alert('pause_rate_high', threshold=0.4, action='email_admin')
monitor.set_alert('confidence_low', threshold=0.5, action='log_warning')
```

---

## Version Information

**Current Version:** 1.0.0  
**API Stability:** Stable  
**Python Compatibility:** 3.8+  
**Dependencies:** numpy>=1.19.0, pandas>=1.3.0, scipy>=1.7.0

**Contact for Support:**  
- **Creator:** Lev Goukassian
- **Email:** leogouk@gmail.com  
- **ORCID:** 0009-0006-5966-1243
- **Repository:** https://github.com/FractonicMind/TernaryLogic

---

*"This API reference provides the complete technical foundation for implementing the Sacred Pause in your decision-making systems. The future is ternary."*
