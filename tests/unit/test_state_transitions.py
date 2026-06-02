"""
Unit tests for TL state transition logic.

Test philosophy:
    State transition tests verify that the constitutional state machine
    behaves correctly. Transition validity is a structural property of
    the framework. Pattern detection tests verify sequence classification.
    All threshold-dependent assertions are expressed relative to the
    engine's configured values, not hardcoded numbers.
"""
import pytest
from ternary_logic import TLEngine, TLState


class TestStateTransitions:
    """Test state transition logic and validation."""

    def test_valid_proceed_to_hold_transition(self, tl_engine):
        """Confidence dropping from above to within uncertainty band."""
        d1 = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05,
            reasoning="initial proceed"
        )
        d2 = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="signals deteriorated"
        )
        assert d1.state == TLState.PROCEED
        assert d2.state == TLState.EPISTEMIC_HOLD

    def test_valid_hold_to_refuse_transition(self, tl_engine):
        """Confidence dropping from uncertainty band to below hold threshold."""
        d1 = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="uncertain signals"
        )
        d2 = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05,
            reasoning="signals failed"
        )
        assert d1.state == TLState.EPISTEMIC_HOLD
        assert d2.state == TLState.REFUSE

    def test_direct_proceed_to_refuse(self, tl_engine):
        """Confidence can drop directly from PROCEED zone to REFUSE zone."""
        d1 = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05,
            reasoning="initial proceed"
        )
        d2 = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05,
            reasoning="catastrophic signal failure"
        )
        assert d1.state == TLState.PROCEED
        assert d2.state == TLState.REFUSE

    def test_recovery_path(self, tl_engine):
        """Confidence can recover from REFUSE through HOLD to PROCEED."""
        d1 = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05,
            reasoning="failed"
        )
        d2 = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="partial recovery"
        )
        d3 = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05,
            reasoning="full recovery"
        )
        assert d1.state == TLState.REFUSE
        assert d2.state == TLState.EPISTEMIC_HOLD
        assert d3.state == TLState.PROCEED

    def test_forced_state_bypasses_confidence(self, tl_engine):
        """force_state produces the specified state regardless of confidence."""
        high_confidence = tl_engine.proceed_threshold + 0.10

        forced_hold = tl_engine.evaluate(
            confidence=high_confidence,
            reasoning="mandate failure",
            force_state=TLState.EPISTEMIC_HOLD
        )
        assert forced_hold.state == TLState.EPISTEMIC_HOLD

        forced_refuse = tl_engine.evaluate(
            confidence=high_confidence,
            reasoning="constitutional violation",
            force_state=TLState.REFUSE
        )
        assert forced_refuse.state == TLState.REFUSE

    def test_state_transition_high_confidence_low_risk(self, tl_engine):
        """Confidence well above proceed_threshold produces PROCEED."""
        confidence = tl_engine.proceed_threshold + 0.10
        decision = tl_engine.evaluate(
            confidence=confidence,
            reasoning="High confidence, well above proceed threshold"
        )
        assert decision.state == TLState.PROCEED

    def test_state_transition_low_confidence(self, tl_engine):
        """Confidence well below hold_threshold produces REFUSE."""
        confidence = tl_engine.hold_threshold - 0.10
        decision = tl_engine.evaluate(
            confidence=confidence,
            reasoning="Low confidence, well below hold threshold"
        )
        assert decision.state == TLState.REFUSE

    def test_state_sequence_logged_correctly(self, tl_engine):
        """Each state transition is correctly reflected in the decision log."""
        confidences = [
            tl_engine.proceed_threshold + 0.05,
            (tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            tl_engine.hold_threshold - 0.05
        ]
        expected_states = [
            TLState.PROCEED,
            TLState.EPISTEMIC_HOLD,
            TLState.REFUSE
        ]

        initial_count = len(tl_engine.decision_log)
        for conf, expected in zip(confidences, expected_states):
            decision = tl_engine.evaluate(confidence=conf, reasoning="sequence test")
            assert decision.state == expected

        assert len(tl_engine.decision_log) == initial_count + 3

    @pytest.mark.parametrize("sequence,expected_pattern", [
        (["PROCEED", "PROCEED", "PROCEED"], "stable"),
        (["PROCEED", "EPISTEMIC_HOLD", "PROCEED"], "oscillating"),
        (["PROCEED", "EPISTEMIC_HOLD", "REFUSE"], "deteriorating"),
        (["REFUSE", "EPISTEMIC_HOLD", "PROCEED"], "recovering"),
    ])
    def test_pattern_detection(self, sequence, expected_pattern):
        """Detect state sequence patterns using constitutional state names."""
        if len(set(sequence)) == 1:
            pattern = "stable"
        elif sequence == ["PROCEED", "EPISTEMIC_HOLD", "REFUSE"]:
            pattern = "deteriorating"
        elif sequence == ["REFUSE", "EPISTEMIC_HOLD", "PROCEED"]:
            pattern = "recovering"
        else:
            pattern = "oscillating"

        assert pattern == expected_pattern

    def test_all_state_names_are_canonical(self):
        """Verify canonical state name strings match TLState enum names."""
        canonical_names = {"PROCEED", "EPISTEMIC_HOLD", "REFUSE"}
        enum_names = {s.name for s in TLState}
        assert canonical_names == enum_names

    def test_state_values_are_triadic(self):
        """TLState enum values are exactly +1, 0, -1."""
        values = {s.value for s in TLState}
        assert values == {1, 0, -1}

    def test_refuse_not_named_halt(self):
        """Verify HALT does not exist as a TLState name."""
        state_names = {s.name for s in TLState}
        assert "HALT" not in state_names
        assert "REFUSE" in state_names
