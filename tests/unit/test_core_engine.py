"""
Unit tests for the core Ternary Logic decision engine.

Test philosophy:
    Tests verify that the state machine invariants hold for any
    institution-calibrated threshold values. No test hardcodes a
    threshold as if it were a standard. Every boundary test is
    expressed relative to the engine's actual configured thresholds.

    This ensures the test suite remains valid in 20 years regardless
    of what thresholds any given institution calibrates.
"""
import pytest
from ternary_logic import TLEngine, TLState


class TestTLDecisionEngine:
    """Test suite for core TL decision engine functionality."""

    def test_proceed_decision_above_threshold(self, tl_engine):
        """Confidence clearly above proceed_threshold produces PROCEED."""
        confidence = tl_engine.proceed_threshold + 0.05
        decision = tl_engine.evaluate(
            confidence=confidence,
            reasoning="Confidence clearly above proceed threshold"
        )
        assert decision.state == TLState.PROCEED
        assert decision.confidence >= tl_engine.proceed_threshold
        assert decision.reasoning is not None

    def test_refuse_decision_below_hold_threshold(self, tl_engine):
        """Confidence clearly below hold_threshold produces REFUSE."""
        confidence = tl_engine.hold_threshold - 0.05
        decision = tl_engine.evaluate(
            confidence=confidence,
            reasoning="Confidence clearly below hold threshold"
        )
        assert decision.state == TLState.REFUSE
        assert decision.confidence < tl_engine.hold_threshold

    def test_epistemic_hold_in_uncertainty_band(self, tl_engine):
        """Confidence in the uncertainty band produces EPISTEMIC_HOLD."""
        midpoint = (tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2
        decision = tl_engine.evaluate(
            confidence=midpoint,
            reasoning="Confidence in the uncertainty band"
        )
        assert decision.state == TLState.EPISTEMIC_HOLD
        assert tl_engine.hold_threshold <= decision.confidence < tl_engine.proceed_threshold

    def test_proceed_threshold_boundary(self, tl_engine):
        """Confidence exactly at proceed_threshold produces PROCEED."""
        decision = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold,
            reasoning="Confidence exactly at proceed threshold"
        )
        assert decision.state == TLState.PROCEED

    def test_hold_threshold_boundary(self, tl_engine):
        """Confidence exactly at hold_threshold produces EPISTEMIC_HOLD."""
        decision = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold,
            reasoning="Confidence exactly at hold threshold"
        )
        assert decision.state == TLState.EPISTEMIC_HOLD

    def test_just_below_proceed_threshold(self, tl_engine):
        """Confidence just below proceed_threshold produces EPISTEMIC_HOLD."""
        epsilon = 0.001
        confidence = tl_engine.proceed_threshold - epsilon
        decision = tl_engine.evaluate(
            confidence=confidence,
            reasoning="Confidence just below proceed threshold"
        )
        assert decision.state == TLState.EPISTEMIC_HOLD

    def test_just_below_hold_threshold(self, tl_engine):
        """Confidence just below hold_threshold produces REFUSE."""
        epsilon = 0.001
        confidence = tl_engine.hold_threshold - epsilon
        decision = tl_engine.evaluate(
            confidence=confidence,
            reasoning="Confidence just below hold threshold"
        )
        assert decision.state == TLState.REFUSE

    def test_decision_log_populated(self, tl_engine):
        """Every evaluate call adds an entry to the decision log."""
        initial_count = len(tl_engine.decision_log)
        tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05,
            reasoning="Test log population"
        )
        assert len(tl_engine.decision_log) == initial_count + 1

    def test_epistemic_hold_creates_audit_record(self, tl_engine):
        """Epistemic Hold creates a corresponding EpistemicHoldEvent."""
        initial_holds = len(tl_engine.epistemic_holds)
        midpoint = (tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2
        tl_engine.evaluate(
            confidence=midpoint,
            reasoning="Test audit record creation"
        )
        assert len(tl_engine.epistemic_holds) == initial_holds + 1

    def test_proceed_does_not_create_hold_record(self, tl_engine):
        """PROCEED does not create an EpistemicHoldEvent."""
        initial_holds = len(tl_engine.epistemic_holds)
        tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05,
            reasoning="Test no spurious hold record"
        )
        assert len(tl_engine.epistemic_holds) == initial_holds

    def test_refuse_does_not_create_hold_record(self, tl_engine):
        """REFUSE does not create an EpistemicHoldEvent."""
        initial_holds = len(tl_engine.epistemic_holds)
        tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05,
            reasoning="Test no spurious hold record on refuse"
        )
        assert len(tl_engine.epistemic_holds) == initial_holds

    def test_force_state_overrides_confidence(self, tl_engine):
        """force_state overrides confidence-based determination."""
        # High confidence but mandate failure forces EPISTEMIC_HOLD
        decision = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05,
            reasoning="Mandate failure override",
            force_state=TLState.EPISTEMIC_HOLD
        )
        assert decision.state == TLState.EPISTEMIC_HOLD

    def test_three_state_ordering_invariant(self, tl_engine):
        """Verify the three-state ordering invariant holds."""
        above = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05,
            reasoning="above"
        )
        mid = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="mid"
        )
        below = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05,
            reasoning="below"
        )
        assert above.state == TLState.PROCEED
        assert mid.state == TLState.EPISTEMIC_HOLD
        assert below.state == TLState.REFUSE

    def test_engine_requires_proceed_threshold(self):
        """TLEngine raises ValueError if proceed_threshold is None."""
        with pytest.raises(ValueError, match="proceed_threshold"):
            TLEngine(proceed_threshold=None, hold_threshold=0.30)

    def test_engine_requires_hold_threshold(self):
        """TLEngine raises ValueError if hold_threshold is None."""
        with pytest.raises(ValueError, match="hold_threshold"):
            TLEngine(proceed_threshold=0.80, hold_threshold=None)

    def test_engine_requires_valid_ordering(self):
        """TLEngine raises ValueError if hold_threshold >= proceed_threshold."""
        with pytest.raises(ValueError):
            TLEngine(proceed_threshold=0.40, hold_threshold=0.80)

    def test_statistics_reflect_all_three_states(self, tl_engine):
        """Statistics correctly count all three state types."""
        tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05,
            reasoning="proceed"
        )
        tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="hold"
        )
        tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05,
            reasoning="refuse"
        )
        stats = tl_engine.get_statistics()
        assert stats['proceed_count'] >= 1
        assert stats['hold_count'] >= 1
        assert stats['refuse_count'] >= 1
        assert stats['total_decisions'] == (
            stats['proceed_count'] + stats['hold_count'] + stats['refuse_count']
        )

    @pytest.mark.parametrize("offset,expected_state", [
        (0.10, TLState.PROCEED),
        (0.05, TLState.PROCEED),
        (-0.05, TLState.EPISTEMIC_HOLD),
        (-0.10, TLState.EPISTEMIC_HOLD),
    ])
    def test_proceed_threshold_boundary_parametrized(
        self, tl_engine, offset, expected_state
    ):
        """Parametrized boundary tests relative to proceed_threshold."""
        confidence = tl_engine.proceed_threshold + offset
        confidence = max(0.0, min(1.0, confidence))
        decision = tl_engine.evaluate(
            confidence=confidence,
            reasoning=f"Boundary test at proceed_threshold + {offset}"
        )
        assert decision.state == expected_state

    @pytest.mark.parametrize("offset,expected_state", [
        (0.10, TLState.EPISTEMIC_HOLD),
        (0.05, TLState.EPISTEMIC_HOLD),
        (-0.05, TLState.REFUSE),
        (-0.10, TLState.REFUSE),
    ])
    def test_hold_threshold_boundary_parametrized(
        self, tl_engine, offset, expected_state
    ):
        """Parametrized boundary tests relative to hold_threshold."""
        confidence = tl_engine.hold_threshold + offset
        confidence = max(0.0, min(1.0, confidence))
        decision = tl_engine.evaluate(
            confidence=confidence,
            reasoning=f"Boundary test at hold_threshold + {offset}"
        )
        assert decision.state == expected_state
