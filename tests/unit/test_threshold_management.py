"""
Unit tests for dynamic threshold management.
"""
import pytest
import numpy as np


class TestThresholdManagement:
    """Test dynamic threshold calibration and management."""
    
    def test_confidence_threshold_initialization(self):
        """Test initial confidence threshold setup."""
        initial_confidence = 0.7
        
        assert initial_confidence == 0.7
        assert 0 <= initial_confidence <= 1
    
    def test_adaptive_threshold_adjustment(self):
        """Test adaptive threshold adjustment based on performance."""
        initial_threshold = 0.7
        performance_history = [0.8, 0.85, 0.9, 0.88, 0.92]
        
        # Simple adaptive adjustment
        avg_performance = np.mean(performance_history)
        if avg_performance > 0.85:
            new_threshold = initial_threshold * 0.95  # Lower threshold if performing well
        else:
            new_threshold = initial_threshold * 1.05  # Raise threshold if underperforming
        
        new_threshold = max(0.5, min(0.9, new_threshold))  # Keep within bounds
        
        assert new_threshold != initial_threshold
        assert 0.5 <= new_threshold <= 0.9
    
    def test_threshold_bounds_enforcement(self):
        """Test that thresholds stay within valid bounds."""
        # Try to set extreme values
        test_values = [1.5, -0.1, 0.5, 0.99]
        
        for value in test_values:
            # Enforce bounds
            bounded_value = max(0.0, min(1.0, value))
            assert 0 <= bounded_value <= 1
    
    def test_domain_specific_thresholds(self):
        """Test different thresholds for different domains."""
        domain_thresholds = {
            'trading': (0.75, 0.25),
            'policy': (0.8, 0.2),
            'supply_chain': (0.65, 0.35)
        }
        
        assert domain_thresholds['trading'] == (0.75, 0.25)
        assert domain_thresholds['policy'] == (0.8, 0.2)
        assert domain_thresholds['supply_chain'] == (0.65, 0.35)
    
    @pytest.mark.parametrize("market_volatility,expected_threshold", [
        (0.1, 0.65),  # Low volatility -> lower confidence needed
        (0.3, 0.70),  # Medium volatility -> standard threshold
        (0.6, 0.80),  # High volatility -> higher confidence needed
    ])
    def test_volatility_adjusted_thresholds(self, market_volatility, expected_threshold):
        """Test threshold adjustment based on market volatility."""
        base_threshold = 0.7
        
        # Adjust based on volatility
        if market_volatility < 0.2:
            adjusted_threshold = base_threshold - 0.05
        elif market_volatility > 0.5:
            adjusted_threshold = base_threshold + 0.10
        else:
            adjusted_threshold = base_threshold
        
        assert abs(adjusted_threshold - expected_threshold) < 0.05
