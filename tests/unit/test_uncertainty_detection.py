"""
Unit tests for uncertainty detection and measurement.
"""
import pytest
import numpy as np
import pandas as pd


class TestUncertaintyMeasurement:
    """Test uncertainty detection and quantification."""
    
    def test_market_volatility_calculation(self, market_data):
        """Test volatility-based uncertainty measurement."""
        # Simple volatility calculation
        returns = market_data['price'].pct_change().dropna()
        volatility = returns.std()
        
        # Normalize to 0-1 scale
        uncertainty = min(volatility * 10, 1.0)
        
        assert 0 <= uncertainty <= 1
    
    def test_information_asymmetry_detection(self):
        """Test incomplete information recognition."""
        # Simulate information gaps
        available_info = {
            'price': 100,
            'volume': 1000000,
            'bid': None,  # Missing
            'ask': None,  # Missing
            'sentiment': 0.6
        }
        
        # Count missing values
        missing_count = sum(1 for v in available_info.values() if v is None)
        total_fields = len(available_info)
        
        uncertainty = missing_count / total_fields
        
        assert uncertainty > 0.3  # Significant uncertainty from missing data
    
    def test_regime_change_detection(self):
        """Test detection of regime changes in data."""
        # Create data with regime change
        data1 = np.random.normal(100, 10, 50)
        data2 = np.random.normal(120, 15, 50)  # Regime change
        data = np.concatenate([data1, data2])
        
        # Simple change detection
        midpoint = len(data) // 2
        mean1 = np.mean(data[:midpoint])
        mean2 = np.mean(data[midpoint:])
        
        regime_change_detected = abs(mean2 - mean1) > 10
        
        assert regime_change_detected == True
    
    @pytest.mark.parametrize("noise_level,expected_uncertainty", [
        (0.1, 0.2),
        (0.5, 0.5),
        (1.0, 0.8),
    ])
    def test_noise_based_uncertainty(self, noise_level, expected_uncertainty):
        """Test uncertainty detection from signal noise."""
        signal = np.sin(np.linspace(0, 10, 100))
        noise = np.random.normal(0, noise_level, 100)
        noisy_signal = signal + noise
        
        # Calculate signal-to-noise ratio
        snr = np.var(signal) / np.var(noise) if np.var(noise) > 0 else float('inf')
        
        # Convert to uncertainty (inverse of SNR)
        uncertainty = 1 / (1 + snr)
        
        assert abs(uncertainty - expected_uncertainty) < 0.3
