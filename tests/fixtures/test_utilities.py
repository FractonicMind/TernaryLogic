"""
Custom testing utilities for the TL framework.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional


class TLTestFramework:
    """Utilities for testing the Ternary Logic framework."""
    
    def create_test_scenario(self, scenario_type: str, complexity_level: str = 'medium'):
        """
        Generate test scenarios for specific domains.
        
        Args:
            scenario_type: Type of scenario (trading, policy, supply_chain)
            complexity_level: Complexity level (low, medium, high)
        
        Returns:
            Dictionary containing scenario parameters
        """
        base_params = {
            'confidence': np.random.uniform(0.3, 0.9),
            'risk': np.random.uniform(0.1, 0.7),
            'complexity': complexity_level
        }
        
        if scenario_type == 'trading':
            return {
                **base_params,
                'volatility': np.random.uniform(0.1, 0.5),
                'momentum': np.random.uniform(-1, 1),
                'volume': np.random.randint(100000, 10000000),
                'spread': np.random.uniform(0.01, 0.05)
            }
        elif scenario_type == 'policy':
            return {
                **base_params,
                'inflation': np.random.uniform(0, 5),
                'unemployment': np.random.uniform(2, 8),
                'gdp_growth': np.random.uniform(-2, 5),
                'interest_rate': np.random.uniform(0, 10)
            }
        elif scenario_type == 'supply_chain':
            return {
                **base_params,
                'supplier_reliability': np.random.uniform(0.6, 0.99),
                'lead_time': np.random.randint(1, 30),
                'quality_score': np.random.uniform(0.7, 1.0),
                'inventory_level': np.random.uniform(0, 1)
            }
        else:
            return base_params
    
    def validate_tl_decision(self, expected_state: str, actual_state: str,
                           tolerance: float = 0.0) -> bool:
        """
        Validate TL decision state classification.
        
        Args:
            expected_state: Expected TL state
            actual_state: Actual TL state from engine
            tolerance: Tolerance for confidence/risk scores
        
        Returns:
            Boolean indicating if decision is valid
        """
        if tolerance == 0:
            return expected_state == actual_state
        
        # Allow for boundary cases with tolerance
        state_values = {'HALT': -1, 'HOLD': 0, 'PROCEED': 1}
        expected_value = state_values.get(expected_state, 0)
        actual_value = state_values.get(actual_state, 0)
        
        return abs(expected_value - actual_value) <= tolerance
    
    def generate_market_conditions(self, condition_type: str) -> pd.DataFrame:
        """
        Generate realistic market condition data.
        
        Args:
            condition_type: Type of market condition
        
        Returns:
            DataFrame with market data
        """
        n_days = 252  # One trading year
        dates = pd.date_range('2023-01-01', periods=n_days, freq='B')
        
        if condition_type == 'bull_market':
            trend = 0.0008
            volatility = 0.015
        elif condition_type == 'bear_market':
            trend = -0.0005
            volatility = 0.025
        elif condition_type == 'high_volatility':
            trend = 0.0001
            volatility = 0.04
        elif condition_type == 'sideways':
            trend = 0.0
            volatility = 0.012
        else:
            trend = 0.0003
            volatility = 0.018
        
        returns = np.random.normal(trend, volatility, n_days)
        prices = 100 * np.exp(np.cumsum(returns))
        
        return pd.DataFrame({
            'date': dates,
            'price': prices,
            'returns': returns,
            'volume': np.random.randint(1000000, 10000000, n_days),
            'volatility': pd.Series(returns).rolling(20).std()
        })


class DataGenerator:
    """Generate test data for various scenarios."""
    
    @staticmethod
    def generate_price_series(n_points: int, trend: float = 0.0,
                            volatility: float = 0.02) -> np.ndarray:
        """Generate synthetic price series."""
        returns = np.random.normal(trend, volatility, n_points)
        prices = 100 * np.exp(np.cumsum(returns))
        return prices
    
    @staticmethod
    def generate_correlation_matrix(n_assets: int, avg_correlation: float = 0.3) -> np.ndarray:
        """Generate valid correlation matrix."""
        # Generate random matrix
        random_matrix = np.random.randn(n_assets, n_assets)
        
        # Make it symmetric and positive definite
        cov_matrix = np.dot(random_matrix, random_matrix.T)
        
        # Convert to correlation
        d = np.sqrt(np.diag(cov_matrix))
        corr_matrix = cov_matrix / d[:, None] / d[None, :]
        
        # Ensure diagonal is 1
        np.fill_diagonal(corr_matrix, 1.0)
        
        return corr_matrix
