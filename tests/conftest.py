"""
pytest configuration and shared fixtures for the Ternary Logic Framework tests.
"""
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Global test configuration
pytest.register_assert_rewrite('tests.fixtures.test_utilities')


@pytest.fixture(scope='session')
def test_data_dir():
    """Provide path to test data directory."""
    return Path(__file__).parent / 'fixtures'


@pytest.fixture
def tl_engine():
    """Provide a fresh TernaryLogicEngine instance."""
    # Mock implementation - replace with actual import
    class MockTLEngine:
        def __init__(self, confidence_threshold=0.7, risk_threshold=0.3):
            self.confidence_threshold = confidence_threshold
            self.risk_threshold = risk_threshold
        
        def make_decision(self, signals):
            from types import SimpleNamespace
            confidence = signals.get('confidence', 0.5)
            risk = signals.get('risk', 0.5)
            
            if confidence > self.confidence_threshold and risk < self.risk_threshold:
                state = 'PROCEED'
            elif confidence < 0.4 or risk > 0.7:
                state = 'HALT'
            else:
                state = 'HOLD'
            
            return SimpleNamespace(
                state=state, 
                confidence=confidence,
                risk_score=risk,
                rationale=f"Decision: {state}"
            )
    
    return MockTLEngine()


@pytest.fixture
def market_data():
    """Provide sample market data for testing."""
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    return pd.DataFrame({
        'date': dates,
        'price': np.random.randn(100).cumsum() + 100,
        'volume': np.random.randint(1000000, 10000000, 100),
        'volatility': np.random.uniform(0.1, 0.5, 100),
        'bid_ask_spread': np.random.uniform(0.01, 0.05, 100)
    })


@pytest.fixture
def policy_indicators():
    """Provide monetary policy indicators."""
    return {
        'inflation_rate': 2.3,
        'unemployment_rate': 4.1,
        'gdp_growth': 2.8,
        'interest_rate': 5.25,
        'money_supply_growth': 3.2,
        'exchange_rate_volatility': 0.15
    }


@pytest.fixture
def supply_chain_data():
    """Provide supply chain scenario data."""
    return {
        'supplier_reliability': 0.92,
        'lead_time_variability': 0.18,
        'quality_score': 0.88,
        'cost_volatility': 0.22,
        'disruption_probability': 0.05,
        'inventory_turnover': 12.5
    }


# Pytest hooks for custom reporting
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers."""
    for item in items:
        # Add markers based on test location
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)
