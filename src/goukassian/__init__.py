"""
Ternary Logic Framework - Intelligent Economic Decision-Making Under Uncertainty
Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com

"The world is not binary. And the future will not be either."
"""

from .core import (
    TLState,
    TLValue, 
    TLResult,
    TLEvaluator,
    TLDecisionEngine
)

__version__ = "1.0.0"
__author__ = "Lev Goukassian"
__email__ = "leogouk@gmail.com"
__orcid__ = "0009-0006-5966-1243"

__all__ = [
    "TLState",
    "TLValue",
    "TLResult", 
    "TLEvaluator",
    "TLDecisionEngine"
]
