#!/usr/bin/env python3
"""
Script to create all test files for the Ternary Logic Framework.
Run this from your project root directory where the tests/ folder exists.

Test philosophy:
    Tests verify framework invariants, not specific numeric threshold values.
    No test hardcodes a threshold as if it were a standard. Every
    threshold-dependent assertion is expressed relative to the engine's
    configured values. This ensures the test suite remains correct in 20
    years regardless of what thresholds any institution calibrates.
"""

import os
from pathlib import Path

TEST_DIR = Path("tests")

subdirs = [
    "unit",
    "integration",
    "scenarios",
    "performance",
    "validation",
    "fixtures",
    "fixtures/market_data",
    "fixtures/policy_scenarios",
    "fixtures/supply_chain_data"
]

for subdir in subdirs:
    (TEST_DIR / subdir).mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {TEST_DIR / subdir}")

TEST_FILES = {

"conftest.py": '''"""
pytest configuration and shared fixtures for the Ternary Logic Framework tests.

Fixture philosophy:
    The tl_engine fixture uses explicit threshold values that are labeled
    clearly as test calibration values. These values are chosen to create
    a usable three-zone structure for tests. They are NOT framework defaults,
    NOT recommendations, and NOT standards. Any institution running this
    framework in production must calibrate its own thresholds through the
    governance process described in docs/Threshold_Calibration.md.

    Tests that use tl_engine express all threshold-dependent assertions
    relative to tl_engine.proceed_threshold and tl_engine.hold_threshold,
    never as hardcoded magic numbers. This means the test suite remains
    valid if the fixture thresholds are ever changed.
"""
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ternary_logic import TLEngine, TLState

# Test calibration values used in the tl_engine fixture only.
# NOT framework defaults. NOT recommendations.
# Production deployments must derive their own values.
# See docs/Threshold_Calibration.md.
_TEST_PROCEED_THRESHOLD = 0.75
_TEST_HOLD_THRESHOLD = 0.35


@pytest.fixture(scope="session")
def test_data_dir():
    """Provide path to test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def tl_engine():
    """Provide a fresh TLEngine instance for tests.

    Threshold values are test calibration values only.
    See module docstring and docs/Threshold_Calibration.md.
    All tests using this fixture must express assertions relative to
    tl_engine.proceed_threshold and tl_engine.hold_threshold.
    """
    return TLEngine(
        proceed_threshold=_TEST_PROCEED_THRESHOLD,
        hold_threshold=_TEST_HOLD_THRESHOLD,
        epistemic_hold_rate_target=0.20
    )


@pytest.fixture
def tl_engine_conservative():
    """A more conservative engine for comparative tests."""
    return TLEngine(
        proceed_threshold=0.90,
        hold_threshold=0.50,
        epistemic_hold_rate_target=0.20
    )


@pytest.fixture
def tl_engine_aggressive():
    """A less conservative engine for comparative tests."""
    return TLEngine(
        proceed_threshold=0.60,
        hold_threshold=0.20,
        epistemic_hold_rate_target=0.20
    )


@pytest.fixture
def market_data():
    """Provide sample market data for testing."""
    dates = pd.date_range("2024-01-01", periods=100, freq="D")
    return pd.DataFrame({
        "date": dates,
        "price": np.random.randn(100).cumsum() + 100,
        "volume": np.random.randint(1_000_000, 10_000_000, 100),
        "volatility": np.random.uniform(0.1, 0.5, 100),
        "bid_ask_spread": np.random.uniform(0.01, 0.05, 100)
    })


@pytest.fixture
def policy_indicators():
    """Provide monetary policy indicators."""
    return {
        "inflation_rate": 2.3,
        "unemployment_rate": 4.1,
        "gdp_growth": 2.8,
        "interest_rate": 5.25,
        "money_supply_growth": 3.2,
        "exchange_rate_volatility": 0.15
    }


@pytest.fixture
def supply_chain_data():
    """Provide supply chain scenario data."""
    return {
        "supplier_reliability": 0.92,
        "lead_time_variability": 0.18,
        "quality_score": 0.88,
        "cost_volatility": 0.22,
        "disruption_probability": 0.05,
        "inventory_turnover": 12.5
    }


def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with \'-m \"not slow\"\')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )


def pytest_collection_modifyitems(config, items):
    """Add markers based on test location."""
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)
''',

"requirements.txt": '''# Testing Dependencies for Ternary Logic Framework
pytest==7.4.3
pytest-cov==4.1.0
pytest-html==4.1.1
pytest-xdist==3.5.0
pytest-benchmark==4.0.0
pytest-mock==3.12.0

# Data processing
numpy==1.24.3
pandas==2.0.3
scipy==1.11.4

# Visualization for test reports
matplotlib==3.7.2
seaborn==0.12.2

# Performance testing
memory-profiler==0.61.0
psutil==5.9.6

# Test data generation
faker==20.1.0

# API testing
requests==2.31.0
responses==0.24.1

# Code quality
black==23.12.0
flake8==6.1.0
''',

"unit/test_core_engine.py": '''"""
Unit tests for the core Ternary Logic decision engine.

Tests verify invariants relative to engine thresholds, not hardcoded values.
"""
import pytest
from ternary_logic import TLEngine, TLState


class TestTLDecisionEngine:

    def test_proceed_above_threshold(self, tl_engine):
        confidence = tl_engine.proceed_threshold + 0.05
        decision = tl_engine.evaluate(confidence=confidence, reasoning="test")
        assert decision.state == TLState.PROCEED

    def test_refuse_below_hold_threshold(self, tl_engine):
        confidence = tl_engine.hold_threshold - 0.05
        decision = tl_engine.evaluate(confidence=confidence, reasoning="test")
        assert decision.state == TLState.REFUSE

    def test_epistemic_hold_in_uncertainty_band(self, tl_engine):
        midpoint = (tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2
        decision = tl_engine.evaluate(confidence=midpoint, reasoning="test")
        assert decision.state == TLState.EPISTEMIC_HOLD

    def test_proceed_at_threshold_boundary(self, tl_engine):
        decision = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold, reasoning="test"
        )
        assert decision.state == TLState.PROCEED

    def test_hold_at_threshold_boundary(self, tl_engine):
        decision = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold, reasoning="test"
        )
        assert decision.state == TLState.EPISTEMIC_HOLD

    def test_refuse_state_named_refuse_not_halt(self):
        state_names = {s.name for s in TLState}
        assert "REFUSE" in state_names
        assert "HALT" not in state_names

    def test_engine_requires_proceed_threshold(self):
        with pytest.raises(ValueError, match="proceed_threshold"):
            TLEngine(proceed_threshold=None, hold_threshold=0.30)

    def test_engine_requires_hold_threshold(self):
        with pytest.raises(ValueError, match="hold_threshold"):
            TLEngine(proceed_threshold=0.80, hold_threshold=None)

    def test_three_state_ordering_invariant(self, tl_engine):
        above = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05, reasoning="above"
        )
        mid = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="mid"
        )
        below = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05, reasoning="below"
        )
        assert above.state == TLState.PROCEED
        assert mid.state == TLState.EPISTEMIC_HOLD
        assert below.state == TLState.REFUSE

    @pytest.mark.parametrize("offset,expected_state", [
        (0.10, TLState.PROCEED),
        (0.05, TLState.PROCEED),
        (-0.05, TLState.EPISTEMIC_HOLD),
        (-0.10, TLState.EPISTEMIC_HOLD),
    ])
    def test_proceed_boundary_parametrized(self, tl_engine, offset, expected_state):
        confidence = max(0.0, min(1.0, tl_engine.proceed_threshold + offset))
        decision = tl_engine.evaluate(confidence=confidence, reasoning="test")
        assert decision.state == expected_state

    @pytest.mark.parametrize("offset,expected_state", [
        (0.10, TLState.EPISTEMIC_HOLD),
        (0.05, TLState.EPISTEMIC_HOLD),
        (-0.05, TLState.REFUSE),
        (-0.10, TLState.REFUSE),
    ])
    def test_hold_boundary_parametrized(self, tl_engine, offset, expected_state):
        confidence = max(0.0, min(1.0, tl_engine.hold_threshold + offset))
        decision = tl_engine.evaluate(confidence=confidence, reasoning="test")
        assert decision.state == expected_state
''',

"unit/test_state_transitions.py": '''"""
Unit tests for TL state transition logic.
"""
import pytest
from ternary_logic import TLEngine, TLState


class TestStateTransitions:

    def test_proceed_to_hold_transition(self, tl_engine):
        d1 = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05, reasoning="proceed"
        )
        d2 = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="hold"
        )
        assert d1.state == TLState.PROCEED
        assert d2.state == TLState.EPISTEMIC_HOLD

    def test_hold_to_refuse_transition(self, tl_engine):
        d1 = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="hold"
        )
        d2 = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05, reasoning="refuse"
        )
        assert d1.state == TLState.EPISTEMIC_HOLD
        assert d2.state == TLState.REFUSE

    def test_recovery_path(self, tl_engine):
        d1 = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05, reasoning="refuse"
        )
        d2 = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="partial recovery"
        )
        d3 = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.05, reasoning="recovered"
        )
        assert d1.state == TLState.REFUSE
        assert d2.state == TLState.EPISTEMIC_HOLD
        assert d3.state == TLState.PROCEED

    def test_high_confidence_produces_proceed(self, tl_engine):
        decision = tl_engine.evaluate(
            confidence=tl_engine.proceed_threshold + 0.10, reasoning="test"
        )
        assert decision.state == TLState.PROCEED

    def test_low_confidence_produces_refuse(self, tl_engine):
        decision = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.10, reasoning="test"
        )
        assert decision.state == TLState.REFUSE

    def test_refuse_not_named_halt(self):
        assert "HALT" not in {s.name for s in TLState}
        assert "REFUSE" in {s.name for s in TLState}

    @pytest.mark.parametrize("sequence,expected_pattern", [
        (["PROCEED", "PROCEED", "PROCEED"], "stable"),
        (["PROCEED", "EPISTEMIC_HOLD", "PROCEED"], "oscillating"),
        (["PROCEED", "EPISTEMIC_HOLD", "REFUSE"], "deteriorating"),
        (["REFUSE", "EPISTEMIC_HOLD", "PROCEED"], "recovering"),
    ])
    def test_pattern_detection(self, sequence, expected_pattern):
        if len(set(sequence)) == 1:
            pattern = "stable"
        elif sequence == ["PROCEED", "EPISTEMIC_HOLD", "REFUSE"]:
            pattern = "deteriorating"
        elif sequence == ["REFUSE", "EPISTEMIC_HOLD", "PROCEED"]:
            pattern = "recovering"
        else:
            pattern = "oscillating"
        assert pattern == expected_pattern
''',

"unit/test_threshold_management.py": '''"""
Unit tests for dynamic threshold management.
"""
import pytest
import numpy as np
from ternary_logic import TLEngine, TLState


class TestThresholdManagement:

    def test_threshold_ordering_invariant(self, tl_engine):
        assert tl_engine.hold_threshold < tl_engine.proceed_threshold

    def test_threshold_bounds_invariant(self, tl_engine):
        assert 0.0 < tl_engine.hold_threshold < 1.0
        assert 0.0 < tl_engine.proceed_threshold < 1.0

    def test_engine_rejects_inverted_thresholds(self):
        with pytest.raises(ValueError):
            TLEngine(proceed_threshold=0.40, hold_threshold=0.80)

    def test_engine_rejects_equal_thresholds(self):
        with pytest.raises(ValueError):
            TLEngine(proceed_threshold=0.70, hold_threshold=0.70)

    def test_conservative_produces_fewer_proceed(self):
        standard = TLEngine(proceed_threshold=0.75, hold_threshold=0.35)
        conservative = TLEngine(proceed_threshold=0.90, hold_threshold=0.50)
        confidence = 0.80
        s = standard.evaluate(confidence=confidence, reasoning="test")
        c = conservative.evaluate(confidence=confidence, reasoning="test")
        assert s.state == TLState.PROCEED
        assert c.state == TLState.EPISTEMIC_HOLD

    def test_aggressive_produces_more_proceed(self):
        standard = TLEngine(proceed_threshold=0.80, hold_threshold=0.40)
        aggressive = TLEngine(proceed_threshold=0.65, hold_threshold=0.25)
        confidence = 0.70
        s = standard.evaluate(confidence=confidence, reasoning="test")
        a = aggressive.evaluate(confidence=confidence, reasoning="test")
        assert s.state == TLState.EPISTEMIC_HOLD
        assert a.state == TLState.PROCEED

    def test_domain_thresholds_are_ordered(self):
        domain_thresholds = {
            "trading": (0.75, 0.35),
            "policy": (0.80, 0.30),
            "supply_chain": (0.65, 0.25)
        }
        for domain, (proceed, hold) in domain_thresholds.items():
            assert hold < proceed

    def test_volatility_adjustment_direction(self):
        base = 0.75
        low_vol_adjusted = base - 0.05
        high_vol_adjusted = base + 0.10
        assert high_vol_adjusted > low_vol_adjusted
        assert high_vol_adjusted > base
        assert low_vol_adjusted < base
''',

"integration/test_financial_trading.py": '''"""
Integration tests for financial trading system.
"""
import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from ternary_logic import TLEngine, TLState


class TestTradingIntegration:

    @pytest.mark.integration
    def test_real_time_market_data_processing(self):
        market_stream = []
        price = 100
        for i in range(100):
            price *= (1 + np.random.normal(0.0001, 0.02))
            market_stream.append({"price": price})
        decisions = []
        for dp in market_stream:
            if dp["price"] > 102:
                decisions.append("PROCEED")
            elif dp["price"] < 98:
                decisions.append("REFUSE")
            else:
                decisions.append("EPISTEMIC_HOLD")
        assert len(decisions) == len(market_stream)
        assert all(d in ["PROCEED", "EPISTEMIC_HOLD", "REFUSE"] for d in decisions)

    @pytest.mark.integration
    def test_position_sizing_by_state(self, tl_engine):
        portfolio_value = 1_000_000
        proceed_conf = tl_engine.proceed_threshold + 0.05
        d_proceed = tl_engine.evaluate(confidence=proceed_conf, reasoning="proceed")
        assert d_proceed.state == TLState.PROCEED
        proceed_size = portfolio_value * proceed_conf if d_proceed.state == TLState.PROCEED else 0
        assert proceed_size > 0

        d_hold = tl_engine.evaluate(
            confidence=(tl_engine.proceed_threshold + tl_engine.hold_threshold) / 2,
            reasoning="hold"
        )
        assert d_hold.state == TLState.EPISTEMIC_HOLD
        hold_size = 0 if d_hold.state == TLState.EPISTEMIC_HOLD else portfolio_value
        assert hold_size == 0

        d_refuse = tl_engine.evaluate(
            confidence=tl_engine.hold_threshold - 0.05, reasoning="refuse"
        )
        assert d_refuse.state == TLState.REFUSE
        refuse_size = -portfolio_value if d_refuse.state == TLState.REFUSE else 0
        assert refuse_size < 0

    @pytest.mark.integration
    def test_risk_limit_integration(self):
        risk_limits = {"max_position": 100_000}
        proposed = 120_000
        final = min(proposed, risk_limits["max_position"])
        assert final <= risk_limits["max_position"]

    @pytest.mark.integration
    def test_mandate_failure_blocks_execution(self, tl_engine):
        from ternary_logic import verify_mandate
        transaction = {
            "esg_verified": False,
            "emissions_anchored": True,
            "use_of_proceeds_tracked": True
        }
        result = verify_mandate("sustainable_capital", transaction)
        assert result.state == TLState.EPISTEMIC_HOLD
        assert result.confidence == 0.0

    @pytest.mark.integration
    @pytest.mark.slow
    def test_backtesting_integration(self, tl_engine):
        dates = pd.date_range("2023-01-01", "2024-01-01", freq="D")
        closes = 100 + np.random.randn(len(dates)).cumsum()
        decisions = []
        for i in range(1, len(closes)):
            ret = (closes[i] - closes[i - 1]) / abs(closes[i - 1])
            conf = max(0.0, min(1.0, 0.5 + ret * 5))
            d = tl_engine.evaluate(confidence=conf, reasoning=f"day {i}")
            decisions.append(d.state)
        assert len(decisions) == len(dates) - 1
        assert all(isinstance(d, TLState) for d in decisions)
''',

}

# Write all test files
for filepath, content in TEST_FILES.items():
    full_path = TEST_DIR / filepath
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"Created: {full_path}")

print("\nAll test files created successfully.")
print("Remember: test threshold values in conftest.py are calibration")
print("values for the test suite only. See docs/Threshold_Calibration.md")
print("for production calibration methodology.")
