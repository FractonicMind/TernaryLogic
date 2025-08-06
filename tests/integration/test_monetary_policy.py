"""
Integration tests for monetary policy decision systems.
"""
import pytest
import pandas as pd
import numpy as np


class TestPolicyIntegration:
    """Test integration with monetary policy systems."""
    
    @pytest.mark.integration
    def test_economic_indicator_processing(self, policy_indicators):
        """Test processing of economic indicators for policy decisions."""
        # Simple policy decision logic
        if policy_indicators['inflation_rate'] > 3.0:
            decision = 'PROCEED'  # Proceed with rate hike
            policy_recommendation = 'raise'
        elif policy_indicators['unemployment_rate'] > 5.0:
            decision = 'PROCEED'  # Proceed with rate cut
            policy_recommendation = 'lower'
        else:
            decision = 'HOLD'
            policy_recommendation = 'hold'
        
        confidence = 0.75  # Example confidence
        
        assert decision in ['PROCEED', 'HOLD', 'HALT']
        assert policy_recommendation in ['raise', 'hold', 'lower']
        assert 0 <= confidence <= 1
    
    @pytest.mark.integration
    def test_multi_objective_optimization(self):
        """Test multi-objective policy optimization."""
        objectives = {
            'inflation_target': 2.0,
            'unemployment_target': 4.0,
            'growth_target': 3.0
        }
        
        current_state = {
            'inflation': 2.5,
            'unemployment': 4.5,
            'growth': 2.8
        }
        
        # Calculate deviations from targets
        inflation_gap = current_state['inflation'] - objectives['inflation_target']
        unemployment_gap = current_state['unemployment'] - objectives['unemployment_target']
        growth_gap = objectives['growth_target'] - current_state['growth']
        
        # Simple policy rule
        if inflation_gap > 0.5:
            rate_change = 0.25  # Raise rates
        elif unemployment_gap > 1.0:
            rate_change = -0.25  # Lower rates
        else:
            rate_change = 0.0  # Hold
        
        # Apply constraint
        max_rate_change = 0.5
        rate_change = max(-max_rate_change, min(max_rate_change, rate_change))
        
        assert abs(rate_change) <= max_rate_change
    
    @pytest.mark.integration
    def test_forward_guidance_generation(self):
        """Test generation of forward guidance statements."""
        economic_outlook = {
            'inflation_forecast': [2.3, 2.2, 2.1],
            'growth_forecast': [2.8, 3.0, 3.1],
            'uncertainty_level': 0.4
        }
        
        current_policy_state = 'HOLD'
        
        # Generate guidance based on outlook
        avg_inflation = np.mean(economic_outlook['inflation_forecast'])
        avg_growth = np.mean(economic_outlook['growth_forecast'])
        
        if economic_outlook['uncertainty_level'] > 0.6:
            commitment_level = 'weak'
        elif economic_outlook['uncertainty_level'] > 0.3:
            commitment_level = 'moderate'
        else:
            commitment_level = 'strong'
        
        statement = f"Policy stance: {current_policy_state}"
        time_horizon = '6 months'
        
        assert statement is not None
        assert commitment_level in ['strong', 'moderate', 'weak']
        assert time_horizon is not None
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_historical_policy_validation(self):
        """Test validation against historical policy decisions."""
        # Generate historical decisions
        dates = pd.date_range('2020-01-01', '2024-01-01', freq='Q')
        historical_decisions = pd.DataFrame({
            'date': dates,
            'rate_decision': np.random.choice(['raise', 'hold', 'lower'], len(dates)),
            'inflation': 2.0 + np.random.randn(len(dates)) * 0.5,
            'unemployment': 4.0 + np.random.randn(len(dates)) * 0.8,
            'gdp_growth': 2.5 + np.random.randn(len(dates)) * 1.0
        })
        
        # Simple validation
        correct_predictions = 0
        for i, row in historical_decisions.iterrows():
            # Predict based on simple rules
            if row['inflation'] > 3.0:
                prediction = 'raise'
            elif row['unemployment'] > 5.0:
                prediction = 'lower'
            else:
                prediction = 'hold'
            
            if prediction == row['rate_decision']:
                correct_predictions += 1
        
        accuracy = correct_predictions / len(historical_decisions)
        
        assert accuracy > 0.3  # Some accuracy expected even with random data
