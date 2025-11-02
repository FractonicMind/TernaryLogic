# Ternary Logic Framework - Complete API Reference

**Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)**  

*Complete technical reference for implementing Ternary Logic in economic decision-making systems*

---

## Core Classes

### TLState

**Enumeration representing the three states of ternary logic**

```python
from ternary_logic import TLState

class TLState(Enum):
    PROCEED = 1          # High confidence to proceed
    HALT = -1            # High confidence to stop/reject
    EPISTEMIC_HOLD = 0   # Uncertainty detected - requires deliberation
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
    state: TLState              # Decision state
    confidence: float           # Overall confidence (0-1)
    rationale: str             # Decision explanation  
    next_steps: List[str]      # Recommended actions
    metadata: Dict[str, Any]   # Additional context
```

**Properties:**
- `state`: Final decision state (PROCEED/HALT/EPISTEMIC_HOLD)
- `confidence`: Overall confidence level in decision
- `rationale`: Human-readable explanation of decision logic
- `next_steps`: List of recommended actions based on state
- `metadata`: Additional context (timestamps, calculations, etc.)

**Example:**
```python
result = TLResult(
    state=TLState.EPISTEMIC_HOLD,
    confidence=0.55,
    rationale="Conflicting market signals require additional data",
    next_steps=["Gather order flow data", "Check regulatory announcements"],
    metadata={'epistemic_hold_trigger': 'signal_conflict', 'timestamp': now()}
)
```

---

## Eight Pillars Integration

### PillarIntegration

**Enforces implementation of all Eight Pillars**

```python
from ternary_logic.pillars import PillarIntegration

class PillarIntegration:
    def __init__(self):
        self.epistemic_hold = EpistemicHoldPillar()
        self.immutable_ledger = ImmutableLedgerPillar()
        self.goukassian_principle = GoukassianPrinciplePillar()
        self.decision_logs = DecisionLogsPillar()
        self.economic_rights = EconomicRightsPillar()
        self.sustainable_capital = SustainableCapitalPillar()
        self.hybrid_shield = HybridShieldPillar()
        self.anchors = AnchorsPillar()
```

### Pillar 1: EpistemicHoldPillar

```python
class EpistemicHoldPillar:
    def trigger_hold(self, 
                    transaction: Dict,
                    target_latency: int = 300) -> HoldResult:
        """
        Triggers Epistemic Hold with 300ms target latency
        
        Args:
            transaction: Transaction data
            target_latency: Target processing time in ms
            
        Returns:
            HoldResult with deliberation outcome
        """
```

### Pillar 2: ImmutableLedgerPillar

```python
class ImmutableLedgerPillar:
    def commit_transaction(self,
                          transaction: Dict,
                          decision_log: DecisionLog) -> LedgerEntry:
        """
        Commits to write-once immutable ledger
        
        Args:
            transaction: Verified transaction data
            decision_log: Associated decision documentation
            
        Returns:
            Immutable ledger entry with cryptographic proof
        """
```

### Pillar 3: GoukassianPrinciplePillar

```python
class GoukassianPrinciplePillar:
    def create_lantern(self,
                      deliberation_data: Dict) -> Lantern:
        """
        Creates cryptographic proof of deliberation
        
        Args:
            deliberation_data: Data from Epistemic Hold
            
        Returns:
            Lantern artifact with signature
        """
    
    def verify_license(self, lantern: Lantern) -> bool:
        """
        Verifies system license based on Lantern
        "Forfeit the Lantern, Forfeit the License"
        """
```

### Pillar 4: DecisionLogsPillar

```python
class DecisionLogsPillar:
    def create_decision_log(self,
                           inputs: Dict,
                           process: Dict,
                           outcome: TLState) -> DecisionLog:
        """
        Creates comprehensive audit trail
        Enforces "No Log = No Action"
        """
```

### Pillar 5: EconomicRightsPillar

```python
class EconomicRightsPillar:
    def verify_regulatory_compliance(self,
                                    transaction: Dict) -> ComplianceResult:
        """
        Verifies FATF, IOSCO, Basel III compliance
        
        Checks:
            - AML/CFT requirements
            - Market manipulation indicators
            - Capital adequacy ratios
            - Data privacy (GDPR)
        """
    
    def generate_sar(self, suspicious_activity: Dict) -> SARReport:
        """
        Generates Suspicious Activity Report automatically
        """
```

### Pillar 6: SustainableCapitalPillar

```python
class SustainableCapitalPillar:
    def verify_esg_claims(self,
                         transaction: Dict) -> ESGVerification:
        """
        Verifies Environmental, Social, Governance claims
        
        Validates:
            - Carbon accounting (Scope 1,2,3)
            - Labor standards compliance
            - Governance metrics
            - Greenwashing detection
        """
    
    def calculate_green_haircut(self, asset: Dict) -> float:
        """
        Calculates ESG-adjusted collateral haircuts
        """
```

### Pillar 7: HybridShieldPillar

```python
class HybridShieldPillar:
    def balance_privacy_transparency(self,
                                    transaction: Dict) -> ShieldedData:
        """
        Balances privacy with transparency requirements
        
        Implements:
            - Zero-knowledge proofs
            - Selective disclosure
            - Regulatory access points
        """
```

### Pillar 8: AnchorsPillar

```python
class AnchorsPillar:
    def anchor_to_blockchain(self,
                           merkle_root: str,
                           chains: List[str] = ['ethereum', 'bitcoin']) -> AnchorProof:
        """
        Anchors to public blockchains for integrity
        """
```

---

## Core Evaluator Classes

### TLEvaluator

**Base evaluator with Eight Pillars integration**

```python
from ternary_logic.core import TLEvaluator

class TLEvaluator:
    def __init__(self, 
                halt_threshold: float = 0.3,
                hold_threshold: float = 0.7,
                enable_pillars: bool = True)
```

**Parameters:**
- `halt_threshold`: Below this confidence, recommend halting
- `hold_threshold`: Below this confidence, trigger Epistemic Hold
- `enable_pillars`: Enable Eight Pillars integration (mandatory for production)

**Methods:**

#### evaluate()
```python
def evaluate(self, 
            criteria: Dict[str, Optional[float]],
            weights: Optional[Dict[str, float]] = None,
            context: Optional[str] = None) -> TLResult
```

**Parameters:**
- `criteria`: Dictionary of factors with confidence scores (-1 to 1, None for unknown)
- `weights`: Optional importance weights for each criterion
- `context`: Additional context for decision logging

**Example with Pillars:**
```python
evaluator = TLEvaluator(enable_pillars=True)

criteria = {
    'market_signal': 0.7,
    'regulatory_compliance': None,  # Unknown - will trigger checks
    'esg_score': 0.8,
    'liquidity': 0.9
}

result = evaluator.evaluate(criteria)

if result.state == TLState.EPISTEMIC_HOLD:
    # Pillar 1: Epistemic Hold triggered
    # Pillar 3: Lantern created
    # Pillar 5: Regulatory verification initiated
    # Pillar 6: ESG claims verified
    print(f"Epistemic Hold: {result.rationale}")
```

---

### TLDecisionEngine

**Advanced decision engine with full pillar support**

```python
from ternary_logic.core import TLDecisionEngine

class TLDecisionEngine(TLEvaluator):
    def __init__(self, 
                halt_threshold: float = 0.3,
                hold_threshold: float = 0.7, 
                domain: str = "general",
                pillars_config: Dict = None)
```

**Parameters:**
- `halt_threshold`: Below this confidence, strongly consider halting
- `hold_threshold`: Below this confidence, engage Epistemic Hold
- `domain`: Domain context ("trading", "policy", "supply_chain", "general")
- `pillars_config`: Configuration for Eight Pillars

**Pillars Configuration Example:**
```python
pillars_config = {
    'economic_rights': {
        'fatf_enabled': True,
        'iosco_enabled': True,
        'basel_iii_enabled': True,
        'gdpr_enabled': True
    },
    'sustainable_capital': {
        'esg_verification': True,
        'greenwashing_detection': True,
        'carbon_accounting': True
    },
    'immutable_ledger': {
        'ledger_type': 'distributed',
        'consensus': 'pbft'
    },
    'anchors': {
        'chains': ['ethereum', 'bitcoin'],
        'frequency': 300  # seconds
    }
}

engine = TLDecisionEngine(
    domain="trading",
    pillars_config=pillars_config
)
```

---

## Domain-Specific Applications

### Financial Trading with Regulatory Compliance

#### TradingAgent
```python
from ternary_logic.trading import TradingAgent

class TradingAgent:
    def __init__(self, 
                halt_threshold: float = 0.25,
                hold_threshold: float = 0.75,
                risk_tolerance: float = 0.3,
                regulatory_mode: str = "strict")
    
    def evaluate_trade_opportunity(self,
                                 symbol: str,
                                 market_data: Dict,
                                 regulatory_context: Dict) -> TLResult
```

**Regulatory Context Structure:**
```python
regulatory_context = {
    'jurisdiction': 'US',
    'entity_type': 'institutional',
    'aml_check_required': True,
    'pattern_detection': {
        'layering': False,
        'spoofing': False,
        'wash_trading': False
    },
    'basel_iii_ratios': {
        'lcr': 1.15,  # Liquidity Coverage Ratio
        'nsfr': 1.08  # Net Stable Funding Ratio
    }
}
```

### Central Banking with ESG Integration

#### MonetaryPolicyEngine
```python
from ternary_logic.policy import MonetaryPolicyEngine

class MonetaryPolicyEngine:
    def evaluate_policy_options(self,
                               economic_indicators: Dict,
                               policy_options: Dict,
                               esg_considerations: Dict) -> TLResult
```

**ESG Considerations Structure:**
```python
esg_considerations = {
    'climate_stress_test': {
        'physical_risk': 0.3,
        'transition_risk': 0.5,
        'confidence': 0.7
    },
    'green_asset_eligibility': {
        'bonds_verified': 150,  # Number of verified green bonds
        'greenwashing_detected': 12,
        'total_assessed': 200
    },
    'sustainable_mandate': True
}
```

---

## Configuration and Calibration

### Threshold Calibration by Domain

```python
DOMAIN_THRESHOLDS = {
    'high_frequency_trading': {
        'halt': 0.2,
        'hold': 0.85,
        'max_hold_duration': 100,  # ms
        'regulatory_compliance': 0.999  # 99.9% required
    },
    'central_banking': {
        'halt': 0.35,
        'hold': 0.65,
        'max_hold_duration': 3600000,  # 1 hour
        'esg_verification': 0.95  # 95% accuracy required
    },
    'retail_banking': {
        'halt': 0.3,
        'hold': 0.7,
        'max_hold_duration': 30000,  # 30 seconds
        'aml_compliance': 1.0  # 100% required
    }
}
```

### Pillar-Specific Configuration

```python
PILLAR_REQUIREMENTS = {
    'epistemic_hold': {
        'target_latency': 300,  # ms
        'max_latency': 1000,
        'min_deliberation_depth': 3
    },
    'immutable_ledger': {
        'write_once': True,
        'admin_override': False,  # Cannot be changed
        'cryptographic_linking': True
    },
    'goukassian_principle': {
        'lantern_required': True,
        'license_check': True,
        'no_spy_no_weapon': True
    },
    'decision_logs': {
        'completeness': 1.0,  # 100% required
        'causal_chain': True,
        'no_log_no_action': True
    },
    'economic_rights': {
        'fatf_compliance': 1.0,
        'iosco_compliance': 0.999,
        'basel_iii_monitoring': 'continuous',
        'gdpr_compliance': True
    },
    'sustainable_capital': {
        'esg_verification_accuracy': 0.95,
        'greenwashing_false_positive': 0.05,
        'carbon_accounting_scopes': [1, 2, 3]
    }
}
```

---

## Error Handling and Exceptions

### TLException Hierarchy

```python
class TLException(Exception):
    """Base exception for Ternary Logic Framework"""
    
class PillarViolationException(TLException):
    """Raised when a pillar requirement is violated"""
    
class EpistemicHoldTimeoutException(TLException):
    """Raised when Epistemic Hold exceeds maximum duration"""
    
class RegulatoryComplianceException(TLException):
    """Raised when regulatory requirements are not met"""
    
class ESGVerificationException(TLException):
    """Raised when ESG claims cannot be verified"""
    
class LanternForfeitException(TLException):
    """Raised when Lantern is forfeited (license revoked)"""
    
class DecisionLogException(TLException):
    """Raised when No Log = No Action is violated"""
```

### Exception Handling Example

```python
try:
    engine = TLDecisionEngine(enable_pillars=True)
    result = engine.decide(transaction_data)
    
except LanternForfeitException as e:
    # Critical: License revoked
    shutdown_system()
    notify_governance()
    
except RegulatoryComplianceException as e:
    # Regulatory violation detected
    generate_sar()
    enter_emergency_mode()
    
except EpistemicHoldTimeoutException as e:
    # Hold exceeded maximum duration
    escalate_to_human()
    log_timeout_event()
    
except TLException as e:
    # Generic TL framework error
    log_error(e)
    enter_safe_mode()
```

---

## Performance Metrics and Monitoring

### MetricsCollector

```python
from ternary_logic.monitoring import MetricsCollector

class MetricsCollector:
    def __init__(self):
        self.decisions = []
        self.pillar_metrics = {}
        
    def track_decision(self, result: TLResult) -> None:
        """Track decision for metrics"""
        
    def get_metrics(self) -> Dict[str, Any]:
        """
        Returns:
            - state_distribution: % of PROCEED/HALT/EPISTEMIC_HOLD
            - average_confidence: Mean confidence level
            - epistemic_hold_rate: Frequency of holds
            - regulatory_compliance_rate: % compliant
            - esg_verification_accuracy: % accurate
            - average_hold_duration: Mean time in hold
            - pillar_performance: Per-pillar metrics
        """
```

### Required Metrics Thresholds

```python
REQUIRED_METRICS = {
    'epistemic_hold_rate': (0.15, 0.25),  # 15-25%
    'regulatory_compliance_rate': (0.999, 1.0),  # >99.9%
    'esg_verification_accuracy': (0.95, 1.0),  # >95%
    'decision_log_completeness': (1.0, 1.0),  # 100%
    'average_hold_duration': (0, 30000),  # <30 seconds
    'false_positive_rate': (0, 0.05)  # <5%
}
```

---

## Integration Examples

### Complete Implementation Example

```python
from ternary_logic import TLDecisionEngine, TLState
from ternary_logic.pillars import PillarIntegration
from ternary_logic.monitoring import MetricsCollector

# Initialize with full pillar support
engine = TLDecisionEngine(
    domain="trading",
    halt_threshold=0.25,
    hold_threshold=0.75,
    enable_pillars=True
)

# Configure pillars
pillars = PillarIntegration()
pillars.economic_rights.enable_fatf()
pillars.sustainable_capital.enable_esg_verification()
pillars.immutable_ledger.set_consensus('pbft')
pillars.anchors.set_chains(['ethereum', 'bitcoin'])

# Initialize monitoring
metrics = MetricsCollector()

# Process transaction
transaction = {
    'type': 'securities_trade',
    'value': 1000000,
    'parties': ['entity_a', 'entity_b'],
    'esg_labeled': True,
    'jurisdiction': 'EU'
}

try:
    # Evaluate with full pillar integration
    result = engine.decide(
        transaction,
        context={'market_conditions': 'volatile'}
    )
    
    # Track metrics
    metrics.track_decision(result)
    
    if result.state == TLState.PROCEED:
        # All pillars passed
        execute_trade(transaction)
        
    elif result.state == TLState.EPISTEMIC_HOLD:
        # Deliberation required
        print(f"Hold triggered: {result.rationale}")
        print(f"Next steps: {result.next_steps}")
        
    else:  # HALT
        # Risk or violation detected
        reject_trade(transaction)
        log_rejection(result)
        
except Exception as e:
    handle_error(e)
    
finally:
    # Always create decision log
    log_decision(result)
```

---

## Testing and Validation

### Unit Testing Example

```python
import pytest
from ternary_logic import TLDecisionEngine, TLState

def test_epistemic_hold_trigger():
    """Test that Epistemic Hold triggers correctly"""
    engine = TLDecisionEngine(hold_threshold=0.7)
    
    # Low confidence should trigger hold
    result = engine.evaluate({'signal': 0.5}, confidence=0.5)
    assert result.state == TLState.EPISTEMIC_HOLD
    
def test_regulatory_compliance():
    """Test Pillar 5 regulatory checks"""
    engine = TLDecisionEngine(enable_pillars=True)
    
    # Transaction requiring AML check
    transaction = {
        'value': 50000,
        'cross_border': True,
        'pep_involved': True
    }
    
    result = engine.evaluate_with_compliance(transaction)
    assert 'aml_verified' in result.metadata
    
def test_esg_verification():
    """Test Pillar 6 ESG verification"""
    engine = TLDecisionEngine(enable_pillars=True)
    
    # Green bond requiring verification
    bond = {
        'type': 'green_bond',
        'use_of_proceeds': 'solar_farm',
        'third_party_verified': False
    }
    
    result = engine.evaluate_esg_claim(bond)
    assert result.metadata['greenwashing_risk'] > 0.5
```

---

## Migration Guide

### Migrating from Binary Logic

```python
# Binary Logic (OLD)
def make_decision(data):
    if confidence > 0.5:
        return "PROCEED"
    else:
        return "HALT"

# Ternary Logic (NEW)
def make_decision(data):
    engine = TLDecisionEngine(enable_pillars=True)
    result = engine.evaluate(data)
    
    if result.state == TLState.EPISTEMIC_HOLD:
        # New capability: intelligent uncertainty handling
        gather_more_data()
        return "AWAITING_INFORMATION"
    
    return result.state.name
```

### Migrating from TML to TL

```python
# TML (Moral Logic) - OLD
from ternary_moral_logic import SacredPause

# TL (Economic Logic) - NEW  
from ternary_logic import EpistemicHold

# Update terminology
# Sacred Pause → Epistemic Hold
# Moral reasoning → Economic reasoning
# Always Memory → Immutable Ledger
```

---

## Best Practices

### Production Deployment Checklist

1. ✅ All Eight Pillars implemented and tested
2. ✅ Thresholds calibrated for specific domain
3. ✅ Regulatory compliance modules activated
4. ✅ ESG verification enabled (if applicable)
5. ✅ Monitoring dashboard configured
6. ✅ Emergency procedures documented
7. ✅ Governance bodies notified
8. ✅ Backup systems ready
9. ✅ Team training completed
10. ✅ Audit trail active

### Performance Optimization

```python
# Use caching for regulatory checks
from functools import lru_cache

@lru_cache(maxsize=1000)
def check_sanctions(entity_id: str) -> bool:
    """Cache sanctions checks for performance"""
    return pillars.economic_rights.check_sanctions(entity_id)

# Batch processing for efficiency
def process_batch(transactions: List[Dict]) -> List[TLResult]:
    """Process multiple transactions efficiently"""
    with pillars.batch_mode():
        return [engine.evaluate(t) for t in transactions]
```

---

## Support and Resources

### Documentation
- [Eight Pillars Specification](../pillars/)
- [Governance Framework](../governance/)
- [Implementation Examples](../examples/)
- [Research Papers](../research/)

### Community
- GitHub: https://github.com/FractonicMind/TernaryLogic
- Support: support@tl-goukassian.org

---

## Contact & Engagement

**Primary Contact**: leogouk@gmail.com  
**Successor Contact**: support@tl-goukassian.org  
(see [Succession Charter](/memorial/SUCCESSION_CHARTER.md))

---

*API Version: 2.0.0*  
*Last Updated: November 2025*  
*Framework Version: 1.0.0*
