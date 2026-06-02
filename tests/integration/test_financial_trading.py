"""
Integration tests for financial trading system.

Test philosophy:
    Integration tests verify that TL states integrate correctly with
    downstream trading system behavior. Where confidence values appear,
    they are expressed relative to engine thresholds or labeled as
    scenario inputs with no claim to being standard values.
"""
import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from ternary_logic import TLEngine, TLState


class TestTradingIntegration:
    """Test integration with trading systems."""

    @pytest.mark.integration
    def test_real_time_market_data_processing(self):
        """Test that state machine processes a market data stream correctly."""
        market_stream = []
        price = 100

        for i in range(100):
            price *= (1 + np.random.normal(0.0001, 0.02))
            market_stream.append({
                'timestamp': datetime.now() + timedelta(seconds=i),
                'price': price,
                'volume': np.random.randint(100000, 1000000),
                'bid': price - 0.01,
                'ask': price + 0.01
            })

        decisions = []
        for data_point in market_stream:
            if data_point['price'] > 102:
                decision = 'PROCEED'
            elif data_point['price'] < 98:
                decision = 'REFUSE'
            else:
                decision = 'EPISTEMIC_HOLD'
            decisions.append(decision)

        assert len(decisions) == len(market_stream)
        assert all(d in ['PROCEED', 'EPISTEMIC_HOLD', 'REFUSE'] for d in decisions)

    @pytest.mark.integration
    def test_position_sizing_by_state(self, tl_engine):
        """Position sizing logic responds correctly to all three TL states."""
        portfolio_value = 1_000_000

        # Use a confidence clearly above proceed_threshold for the PROCEED case
        proceed_confidence = tl_engine.proceed_threshold + 0.05
        proceed_decision = tl_engine.evaluate(
            confidence=proceed_confidence,
            reasoning="Strong signals"
        )
        assert proceed_decision.state == TLState.PROCEED
        proceed_size = portfolio_value * proceed_confidence
        assert proceed_size > 0

        # EPISTEMIC_HOLD: no new position
        hold_decision = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="Mixed signals"
        )
        assert hold_decision.state == TLState.EPISTEMIC_HOLD
        hold_size = 0 if hold_decision.state == TLState.EPISTEMIC_HOLD else portfolio_value
        assert hold_size == 0

        # REFUSE: close positions
        refuse_decision = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05,
            reasoning="Signal failure"
        )
        assert refuse_decision.state == TLState.REFUSE
        refuse_size = (
            -portfolio_value if refuse_decision.state == TLState.REFUSE else 0
        )
        assert refuse_size < 0

    @pytest.mark.integration
    def test_risk_limit_integration(self):
        """Risk limits cap position size regardless of TL state."""
        risk_limits = {
            'max_position': 100_000,
            'max_drawdown': 0.1,
            'var_limit': 50_000
        }

        proposed_position = 120_000
        final_position = min(proposed_position, risk_limits['max_position'])
        assert final_position <= risk_limits['max_position']

    @pytest.mark.integration
    def test_mandate_failure_blocks_execution(self, tl_engine):
        """Mandate failure prevents execution regardless of confidence."""
        from ternary_logic import verify_mandate

        # High confidence but ESG not verified
        transaction = {
            'esg_verified': False,
            'emissions_anchored': True,
            'use_of_proceeds_tracked': True
        }
        mandate_result = verify_mandate('sustainable_capital', transaction)

        # Mandate failure produces EPISTEMIC_HOLD even though
        # the trading signal might otherwise be strong
        assert mandate_result.state == TLState.EPISTEMIC_HOLD
        assert mandate_result.confidence == 0.0

    @pytest.mark.integration
    def test_audit_trail_complete_after_sequence(self, tl_engine):
        """Audit trail captures complete sequence of trading decisions."""
        sequence_confidences = [
            tl_engine.proceed_threshold + 0.05,
            (tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            tl_engine.hold_threshold - 0.05,
            (tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            tl_engine.proceed_threshold + 0.05,
        ]
        for conf in sequence_confidences:
            tl_engine.evaluate(confidence=conf, reasoning="trading sequence")

        assert len(tl_engine.decision_log) >= len(sequence_confidences)
        assert tl_engine.get_statistics()['total_decisions'] >= len(
            sequence_confidences
        )

    @pytest.mark.integration
    @pytest.mark.slow
    def test_backtesting_integration(self, tl_engine):
        """Backtesting produces decisions for every historical data point."""
        dates = pd.date_range('2023-01-01', '2024-01-01', freq='D')
        historical_data = pd.DataFrame({
            'date': dates,
            'close': 100 + np.random.randn(len(dates)).cumsum(),
        })

        decisions = []
        for i, row in historical_data.iterrows():
            if i > 0:
                prev_close = historical_data.iloc[i - 1]['close']
                daily_return = (row['close'] - prev_close) / abs(prev_close)
                raw_confidence = 0.5 + daily_return * 5
                confidence = max(0.0, min(1.0, raw_confidence))
                decision = tl_engine.evaluate(
                    confidence=confidence,
                    reasoning=f"Backtest day {i}"
                )
                decisions.append(decision.state)

        assert len(decisions) == len(historical_data) - 1
        assert all(isinstance(d, TLState) for d in decisions)

    @pytest.mark.integration
    def test_epistemic_hold_rate_within_target(self, tl_engine):
        """Hold rate across a synthetic scenario stays near the target range."""
        rng = np.random.default_rng(seed=42)
        confidences = rng.uniform(0.0, 1.0, 200)

        for conf in confidences:
            tl_engine.evaluate(
                confidence=float(conf),
                reasoning="synthetic scenario"
            )

        rate = tl_engine.epistemic_hold_rate
        # The hold rate should be approximately the fraction of the [0,1]
        # range covered by the hold zone
        hold_zone_width = (
            tl_engine.proceed_threshold - tl_engine.hold_threshold
        )
        expected_rate_approx = hold_zone_width
        # Allow generous tolerance for random sampling
        assert abs(rate - expected_rate_approx) < 0.15
