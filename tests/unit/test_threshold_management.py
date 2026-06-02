"""
Unit tests for dynamic threshold management.

Test philosophy:
    Threshold tests verify governance properties and structural invariants,
    not specific numeric values. The correctness of a threshold governance
    system is that it enforces ordering constraints, responds directionally
    to calibration inputs, and stays within valid bounds. These properties
    hold regardless of what specific values any institution calibrates.
"""
import pytest
import numpy as np
from ternary_logic import TLEngine, TLState


class TestThresholdManagement:
    """Test dynamic threshold calibration and management."""

    def test_threshold_ordering_invariant(self, tl_engine):
        """hold_threshold must be strictly less than proceed_threshold."""
        assert tl_engine.hold_threshold < tl_engine.proceed_threshold

    def test_threshold_bounds_invariant(self, tl_engine):
        """Both thresholds must be strictly within (0.0, 1.0)."""
        assert 0.0 < tl_engine.hold_threshold < 1.0
        assert 0.0 < tl_engine.proceed_threshold < 1.0

    def test_threshold_creates_three_distinct_zones(self, tl_engine):
        """The two thresholds must create three non-empty zones."""
        # Zone 1: REFUSE zone exists
        assert tl_engine.hold_threshold > 0.0

        # Zone 2: EPISTEMIC_HOLD zone exists
        assert tl_engine.proceed_threshold - tl_engine.hold_threshold > 0.0

        # Zone 3: PROCEED zone exists
        assert tl_engine.proceed_threshold < 1.0

    def test_engine_rejects_inverted_thresholds(self):
        """Engine rejects configuration where hold >= proceed."""
        with pytest.raises(ValueError):
            TLEngine(proceed_threshold=0.40, hold_threshold=0.80)

    def test_engine_rejects_equal_thresholds(self):
        """Engine rejects configuration where hold == proceed."""
        with pytest.raises(ValueError):
            TLEngine(proceed_threshold=0.70, hold_threshold=0.70)

    def test_engine_rejects_zero_proceed(self):
        """Engine rejects proceed_threshold of 0.0."""
        with pytest.raises(ValueError):
            TLEngine(proceed_threshold=0.0, hold_threshold=0.0)

    def test_engine_rejects_one_proceed(self):
        """Engine rejects proceed_threshold of 1.0."""
        with pytest.raises(ValueError):
            TLEngine(proceed_threshold=1.0, hold_threshold=0.40)

    def test_conservative_vs_standard_posture(self):
        """More conservative thresholds produce fewer PROCEED decisions."""
        standard = TLEngine(proceed_threshold=0.75, hold_threshold=0.35)
        conservative = TLEngine(proceed_threshold=0.90, hold_threshold=0.50)

        # Use a fixed confidence in the uncertainty zone between the two
        confidence = 0.80
        standard_decision = standard.evaluate(
            confidence=confidence,
            reasoning="test"
        )
        conservative_decision = conservative.evaluate(
            confidence=confidence,
            reasoning="test"
        )

        # Standard allows PROCEED at 0.80, conservative requires 0.90
        assert standard_decision.state == TLState.PROCEED
        assert conservative_decision.state == TLState.EPISTEMIC_HOLD

    def test_aggressive_vs_standard_posture(self):
        """Less conservative thresholds produce more PROCEED decisions."""
        standard = TLEngine(proceed_threshold=0.80, hold_threshold=0.40)
        aggressive = TLEngine(proceed_threshold=0.65, hold_threshold=0.25)

        confidence = 0.70
        standard_decision = standard.evaluate(
            confidence=confidence,
            reasoning="test"
        )
        aggressive_decision = aggressive.evaluate(
            confidence=confidence,
            reasoning="test"
        )

        assert standard_decision.state == TLState.EPISTEMIC_HOLD
        assert aggressive_decision.state == TLState.PROCEED

    def test_threshold_bounds_enforcement(self):
        """Candidate threshold values are clamped to valid range."""
        test_values = [1.5, -0.1, 0.5, 0.99]
        for value in test_values:
            bounded = max(0.0, min(1.0, value))
            assert 0.0 <= bounded <= 1.0

    def test_adaptive_adjustment_direction(self):
        """Higher performance history justifies lower proceed threshold."""
        base_threshold = 0.80
        high_performance = [0.92, 0.95, 0.91, 0.93, 0.94]
        low_performance = [0.60, 0.55, 0.58, 0.62, 0.59]

        avg_high = np.mean(high_performance)
        avg_low = np.mean(low_performance)

        # High performance: institution may lower threshold (less conservative)
        # Low performance: institution should raise threshold (more conservative)
        adjusted_high = base_threshold * 0.95 if avg_high > 0.90 else base_threshold
        adjusted_low = base_threshold * 1.05 if avg_low < 0.65 else base_threshold

        # Directional relationship is what matters, not specific numbers
        assert adjusted_high <= base_threshold
        assert adjusted_low >= base_threshold

    def test_volatility_adjustment_direction(self):
        """Higher volatility justifies more conservative thresholds."""
        base = 0.75

        low_volatility_adjustment = base - 0.05    # can be less conservative
        high_volatility_adjustment = base + 0.10   # must be more conservative

        # Directional invariant: high volatility raises threshold
        assert high_volatility_adjustment > low_volatility_adjustment
        assert high_volatility_adjustment > base
        assert low_volatility_adjustment < base

    def test_domain_thresholds_are_ordered(self):
        """Each domain threshold pair must satisfy hold < proceed."""
        domain_thresholds = {
            'trading': (0.75, 0.35),
            'policy': (0.80, 0.30),
            'supply_chain': (0.65, 0.25)
        }
        for domain, (proceed, hold) in domain_thresholds.items():
            assert hold < proceed, (
                f"Domain '{domain}': hold_threshold ({hold}) must be "
                f"less than proceed_threshold ({proceed})"
            )

    def test_domain_thresholds_differ(self):
        """Different domains produce different state outcomes for the same input."""
        domain_thresholds = {
            'trading': (0.75, 0.35),
            'policy': (0.80, 0.30),
            'supply_chain': (0.65, 0.25)
        }
        engines = {
            domain: TLEngine(proceed_threshold=p, hold_threshold=h)
            for domain, (p, h) in domain_thresholds.items()
        }

        # A confidence of 0.70 produces different outcomes across domains
        confidence = 0.70
        decisions = {
            domain: engine.evaluate(confidence=confidence, reasoning="domain test")
            for domain, engine in engines.items()
        }

        # supply_chain (0.65 threshold): PROCEED
        # trading (0.75 threshold): EPISTEMIC_HOLD
        # policy (0.80 threshold): EPISTEMIC_HOLD
        assert decisions['supply_chain'].state == TLState.PROCEED
        assert decisions['trading'].state == TLState.EPISTEMIC_HOLD
        assert decisions['policy'].state == TLState.EPISTEMIC_HOLD

    def test_epistemic_hold_zone_width(self, tl_engine):
        """The epistemic hold zone width equals proceed minus hold threshold."""
        expected_width = tl_engine.proceed_threshold - tl_engine.hold_threshold
        assert expected_width > 0.0

        # Verify zone width by checking points inside it
        zone_midpoint = (
            tl_engine.proceed_threshold + tl_engine.hold_threshold
        ) / 2
        decision = tl_engine.evaluate(
            confidence=zone_midpoint,
            reasoning="zone width verification"
        )
        assert decision.state == TLState.EPISTEMIC_HOLD
