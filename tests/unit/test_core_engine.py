"""
Unit tests for the core Ternary Logic decision engine.
"""
import pytest
import numpy as np


class TestTLDecisionEngine:
    """Test suite for core TL decision engine functionality."""
    
    def test_proceed_decision_clear_signals(self, tl_engine):
        """Test +1 decision with clear positive signals."""
        signals = {
            'confidence': 0.85,
            'risk': 0.15,
            'signal_strength': 0.9,
            'information_quality': 0.88
        }
        
        decision = tl_engine.make_decision(signals)
        
        assert decision.state == 'PROCEED'
        assert decision.confidence > 0.8
        assert decision.rationale is not None
    
    def test_halt_decision_high_risk(self, tl_engine):
        """Test -1 decision with systematic risk detected."""
        signals = {
            'confidence': 0.3,
            'risk': 0.85,
            'systematic_risk': True,
            'volatility_spike': 0.9
        }
        
        decision = tl_engine.make_decision(signals)
        
        assert decision.state == 'HALT'
        assert decision.risk_score > 0.7
    
    def test_epistemic_hold_mixed_signals(self, tl_engine):
        """Test 0 decision with conflicting information."""
        signals = {
            'confidence': 0.55,
            'risk': 0.45,
            'conflicting_indicators': True,
            'information_asymmetry': 0.7
        }
        
        decision = tl_engine.make_decision(signals)
        
        assert decision.state == 'HOLD'
        assert 0.4 < decision.confidence < 0.7
    
    def test_threshold_boundary_behavior(self, tl_engine):
        """Test behavior at confidence/risk thresholds."""
        boundary_signals = {
            'confidence': 0.7,  # Exactly at threshold
            'risk': 0.3,  # Exactly at threshold
            'signal_strength': 0.7
        }
        
        decision = tl_engine.make_decision(boundary_signals)
        assert decision.state in ['PROCEED', 'HOLD']
    
    @pytest.mark.parametrize("confidence,risk,expected_state", [
        (0.9, 0.1, 'PROCEED'),
        (0.3, 0.8, 'HALT'),
        (0.5, 0.5, 'HOLD'),
        (0.8, 0.2, 'PROCEED'),
        (0.2, 0.7, 'HALT'),
    ])
    def test_decision_matrix(self, tl_engine, confidence, risk, expected_state):
        """Test decision matrix across confidence/risk combinations."""
        signals = {
            'confidence': confidence,
            'risk': risk,
            'signal_strength': confidence
        }
        
        decision = tl_engine.make_decision(signals)
        assert decision.state == expected_state
