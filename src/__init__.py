"""
Ternary Logic Framework
=======================

A three-valued logic system for economic decision-making under uncertainty.

The Ternary Logic Framework introduces a third state between binary yes/no decisions:
the Epistemic Hold, a mandatory pause for deliberation when uncertainty exceeds
institutionally calibrated thresholds.

States:
    PROCEED (+1): Execute action when conditions are clear and verified
    EPISTEMIC_HOLD (0): Pause for deliberation when uncertainty is significant
    REFUSE (-1): Reject action when conditions definitively fail requirements

Key Features:
    - Institutionally governed threshold calibration (no universal defaults)
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
    >>> # Thresholds must be calibrated by your institution.
    >>> # No universal values exist. See docs/Threshold_Calibration.md.
    >>> engine = TLEngine(
    ...     proceed_threshold=YOUR_INSTITUTION_PROCEED_THRESHOLD,
    ...     hold_threshold=YOUR_INSTITUTION_HOLD_THRESHOLD
    ... )
    >>> decision = engine.evaluate(
    ...     confidence=0.92,
    ...     reasoning="Strong market signals across all indicators"
    ... )
    >>>
    >>> if decision.state == TLState.PROCEED:
    ...     execute_trade()
    >>> elif decision.state == TLState.EPISTEMIC_HOLD:
    ...     request_additional_analysis()
    >>> else:  # TLState.REFUSE
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
    TLDecorator,
)

# Utility functions
from .core import (
    calculate_confidence,
    analyze_uncertainty,
    verify_mandate,
)

# Public API
__all__ = [
    "TLState",
    "TLValue",
    "TLEngine",
    "EpistemicHoldEvent",
    "TLDecorator",
    "calculate_confidence",
    "analyze_uncertainty",
    "verify_mandate",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]

# Package metadata
FRAMEWORK_NAME = "Ternary Logic Framework"
FRAMEWORK_DESCRIPTION = (
    "Three-valued logic for economic decision-making under uncertainty"
)
REPOSITORY_URL = "https://github.com/FractonicMind/TernaryLogic"
SUPPORT_EMAIL = "support@tl-goukassian.org"

# Threshold governance.
# The TL framework does not ship threshold values of any kind.
# Thresholds are institutionally calibrated governance decisions.
# They must be established through historical backtesting,
# regulatory requirements, board-approved risk appetite,
# and market regime analysis specific to your deployment.
# TLEngine raises ValueError if instantiated without explicit values.
# See docs/Threshold_Calibration.md for calibration methodology.
PROCEED_THRESHOLD = None
HOLD_THRESHOLD = None

# Target Epistemic Hold rate: studies indicate 15-25% is optimal
# for balancing deliberation quality against operational speed.
# Monitor and report; recalibrate thresholds if consistently outside
# this range. This is a monitoring guideline, not a threshold.
TARGET_EPISTEMIC_HOLD_RATE = 0.20


def get_version() -> str:
    """Return the framework version."""
    return __version__


def get_info() -> dict:
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

    2. Calibrate thresholds for your institution:
       Thresholds are NOT provided by the framework.
       They must be established through:
         - Historical backtesting (20+ years of data)
         - Regulatory requirements (Basel III, FATF, etc.)
         - Board-approved risk appetite
         - Market regime analysis
       See docs/Threshold_Calibration.md for calibration methodology.
       TLEngine raises ValueError if instantiated without explicit values.

    3. Create an engine with your calibrated thresholds:
       >>> engine = TLEngine(
       ...     proceed_threshold=YOUR_INSTITUTION_PROCEED_THRESHOLD,
       ...     hold_threshold=YOUR_INSTITUTION_HOLD_THRESHOLD
       ... )

    4. Evaluate a decision:
       >>> decision = engine.evaluate(
       ...     confidence=0.75,
       ...     reasoning="Mixed market signals"
       ... )

    5. Act on the decision:
       >>> if decision.state == TLState.PROCEED:
       ...     # Execute action
       >>> elif decision.state == TLState.EPISTEMIC_HOLD:
       ...     # Pause for additional analysis
       >>> else:  # TLState.REFUSE
       ...     # Reject action

    6. Get statistics:
       >>> stats = engine.get_statistics()
       >>> print(f"Hold rate: {stats['epistemic_hold_rate']:.2%}")

    7. Export audit trail:
       >>> engine.export_audit_trail('audit.json')

    States:
    -------
    PROCEED (+1)       : confidence >= proceed_threshold  (institution-defined)
    EPISTEMIC_HOLD (0) : hold_threshold <= confidence < proceed_threshold
    REFUSE (-1)        : confidence < hold_threshold       (institution-defined)

    Target Hold Rate: 15-25% (optimal for deliberate decision-making)

    For more information: https://github.com/FractonicMind/TernaryLogic
    """
    print(guide)


def _init_message():
    """Display initialization message in interactive mode."""
    import sys
    if hasattr(sys, 'ps1'):
        print(f"Ternary Logic Framework v{__version__} loaded")
        print("Use quick_start() for usage guide")
        print("IMPORTANT: Thresholds must be calibrated by your institution.")
        print("           TLEngine raises ValueError without explicit values.")


try:
    _init_message()
except Exception:
    pass


"""
---
Creator: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Email: leogouk@gmail.com
Repository: https://github.com/FractonicMind/TernaryLogic
Support: support@tl-goukassian.org
---
"""
