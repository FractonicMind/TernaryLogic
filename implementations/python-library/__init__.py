"""
Ternary Logic Framework
=======================

A three-valued logic system for economic decision-making under uncertainty.

The Ternary Logic Framework introduces a third state between binary yes/no decisions:
the Epistemic Hold - a mandatory pause for deliberation when uncertainty exceeds 
acceptable thresholds.

States:
    PROCEED (+1): Execute action when conditions are clear and verified
    EPISTEMIC_HOLD (0): Pause for deliberation when uncertainty is significant
    HALT (-1): Reject action when conditions fail requirements

Key Features:
    - Confidence-based decision making
    - Immutable audit trails (Decision Logs)
    - Real-time model risk management
    - Cryptographic verification support
    - Regulatory compliance by design

Applications:
    - Central banking and monetary policy
    - Trading and investment decisions
    - Supply chain optimization
    - Risk management systems
    - Financial market infrastructure

Example Usage:
    >>> from ternary_logic import TLEngine, TLState
    >>> 
    >>> engine = TLEngine()
    >>> decision = engine.evaluate(
    ...     confidence=0.92,
    ...     reasoning="Strong market signals across all indicators"
    ... )
    >>> 
    >>> if decision.state == TLState.PROCEED:
    ...     execute_trade()
    >>> elif decision.state == TLState.EPISTEMIC_HOLD:
    ...     request_additional_analysis()
    >>> else:  # HALT
    ...     reject_trade()

Created by: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Repository: https://github.com/FractonicMind/TernaryLogic
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Lev Goukassian"
__email__ = "leogouk@gmail.com"
__license__ = "MIT"

# Core classes
from .core import (
    TLState,
    TLValue,
    TLEngine,
    EpistemicHoldEvent,
    ConfidenceLevel,
    TLDecorator,
)

# Utility functions
from .core import (
    analyze_uncertainty,
)

# Public API
__all__ = [
    # Core enums and classes
    "TLState",
    "TLValue",
    "TLEngine",
    "EpistemicHoldEvent",
    "ConfidenceLevel",
    
    # Decorators and utilities
    "TLDecorator",
    "analyze_uncertainty",
    
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]

# Package metadata
FRAMEWORK_NAME = "Ternary Logic Framework"
FRAMEWORK_DESCRIPTION = "Three-valued logic for economic decision-making under uncertainty"
REPOSITORY_URL = "https://github.com/FractonicMind/TernaryLogic"
SUPPORT_EMAIL = "support@tl-goukassian.org"

# Framework constants
DEFAULT_PROCEED_THRESHOLD = 0.85
DEFAULT_HOLD_THRESHOLD = 0.40
TARGET_EPISTEMIC_HOLD_RATE = 0.20  # 15-25% optimal range

# Confidence level boundaries
CONFIDENCE_HIGH = 0.85
CONFIDENCE_MEDIUM = 0.60
CONFIDENCE_LOW = 0.40

def get_version():
    """Return the framework version."""
    return __version__

def get_info():
    """Return framework information."""
    return {
        'name': FRAMEWORK_NAME,
        'version': __version__,
        'description': FRAMEWORK_DESCRIPTION,
        'author': __author__,
        'email': __email__,
        'repository': REPOSITORY_URL,
        'support': SUPPORT_EMAIL,
        'license': __license__,
    }

def quick_start():
    """Print quick start guide."""
    guide = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║         TERNARY LOGIC FRAMEWORK - QUICK START                 ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    1. Import the framework:
       >>> from ternary_logic import TLEngine, TLState
    
    2. Create an engine:
       >>> engine = TLEngine()
    
    3. Evaluate a decision:
       >>> decision = engine.evaluate(
       ...     confidence=0.75,
       ...     reasoning="Mixed market signals"
       ... )
    
    4. Act on the decision:
       >>> if decision.state == TLState.PROCEED:
       ...     # Execute action
       >>> elif decision.state == TLState.EPISTEMIC_HOLD:
       ...     # Pause for additional analysis
       >>> else:  # TLState.HALT
       ...     # Reject action
    
    5. Get statistics:
       >>> stats = engine.get_statistics()
       >>> print(f"Hold rate: {stats['epistemic_hold_rate']:.2%}")
    
    6. Export audit trail:
       >>> engine.export_audit_trail('audit.json')
    
    States:
    -------
    PROCEED (+1)       : confidence ≥ 0.85
    EPISTEMIC_HOLD (0) : 0.40 ≤ confidence < 0.85
    HALT (-1)          : confidence < 0.40
    
    Target Hold Rate: 15-25% (optimal for thoughtful decision-making)
    
    For more information: https://github.com/FractonicMind/TernaryLogic
    """
    print(guide)

# Package initialization message
def _init_message():
    """Display initialization message when package is imported."""
    import sys
    if hasattr(sys, 'ps1'):  # Interactive mode
        print(f"Ternary Logic Framework v{__version__} loaded")
        print(f"Use quick_start() for usage guide")

# Show message on import in interactive mode
try:
    _init_message()
except:
    pass


"""
---
Creator: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Email: leogouk@gmail.com
Repository: https://github.com/FractonicMind/TernaryLogic
Support: support@tl-goukassian.org
---
"""
