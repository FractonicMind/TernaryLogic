"""
Ternary Logic Framework - Comprehensive Financial Trading Example
Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com

This example demonstrates how the Ternary Logic framework prevents flash crashes
and improves trading performance by recognizing when to pause rather than force trades.

"The Epistemic Hold saves portfolios."
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

# Import Ternary Logic Framework
from ternary_logic import TLDecisionEngine, TLState
from ternary_logic.core import TLResult

class TLTradingAlgorithm:
    """
    Advanced trading algorithm using Ternary Logic for uncertainty-aware decisions
    
    This algorithm demonstrates the Epistemic Hold principle in live trading:
    - PROCEED: High confidence to execute trade
    - HALT: High confidence to avoid trade  
    - EPISTEMIC_HOLD: Insufficient data - pause and monitor
    """
    
    def __init__(self, 
                 confidence_threshold: float = 0.75,
                 position_size_limit: float = 0.1,
                 max_drawdown: float = 0.05):
        """
        Initialize the TL Trading Algorithm
        
        Args:
            confidence_threshold: Minimum confidence for trade execution
            position_size_limit: Maximum position size as fraction of portfolio
            max_drawdown: Maximum acceptable drawdown before risk reduction
        """
        self.engine = TLDecisionEngine(
            confidence_threshold=confidence_threshold,
            domain="financial"
        )
        self.position_size_limit = position_size_limit
        self.max_drawdown = max_drawdown
        
        # Trading state tracking
        self.positions = {}
        self.portfolio_value = 1000000  # $1M starting portfolio
        self.trade_history = []
        self.pause_history = []  # Track Epistemic Hold activations
        
        # Risk management
        self.daily_var = 0.0
        self.current_drawdown = 0.0
        
    def analyze_market_signals(self, symbol: str, market_data: Dict) -> Dict[str, float]:
        """
        Analyze multiple market signals for trading decision
        
        Returns dictionary with signal values or None for missing data
        """
        signals = {}
        
        # Technical Analysis Signals
        if 'price_data' in market_data:
            signals['momentum'] = self._calculate_momentum(market_data['price_data'])
            signals['mean_reversion'] = self._calculate_mean_reversion(market_data['price_data'])
            signals['volatility'] = self._calculate_volatility_signal(market_data['price_data'])
        else:
            signals['momentum'] = None
            signals['mean_reversion'] = None  
            signals['volatility'] = None
            
        # Fundamental Analysis Signals
        if 'earnings_data' in market_data:
            signals['earnings_quality'] = self._analyze_earnings(market_data['earnings_data'])
        else:
            signals['earnings_quality'] = None
            
        # Market Microstructure Signals
        if 'order_book' in market_data:
            signals['liquidity'] = self._analyze_liquidity(market_data['order_book'])
            signals['order_flow'] = self._analyze_order_flow(market_data['order_book'])
        else:
            signals['liquidity'] = None
            signals['order_flow'] = None
            
        # Sentiment and News Signals  
        if 'news_sentiment' in market_data:
            signals['sentiment'] = market_data['news_sentiment']
        else:
            signals['sentiment'] = None
            
        # Cross-Asset Signals
        if 'market_regime' in market_data:
            signals['market_regime'] = market_data['market_regime']
        else:
            signals['market_regime'] = None
            
        return signals
    
    def make_trading_decision(self, 
                            symbol: str, 
                            market_data: Dict,
                            current_position: float = 0.0) -> TLResult:
        """
        Make trading decision using Ternary Logic framework
        
        Args:
            symbol: Trading symbol
            market_data: Market data dictionary
            current_position: Current position size
            
        Returns:
            TLResult with trading decision and reasoning
        """
        
        # Analyze market signals
        signals = self.analyze_market_signals(symbol, market_data)
        
        # Define signal weights based on market conditions
        weights = self._get_signal_weights(symbol, market_data)
        
        # Add risk management overlay
        risk_adjusted_signals = self._apply_risk_management(signals, current_position)
        
        # Make decision using Ternary Logic
        decision = self.engine.decide(
            criteria=risk_adjusted_signals,
            weights=weights,
            context=f"Trading decision for {symbol}"
        )
        
        # Enhance decision with trading-specific information
        decision = self._enhance_trading_decision(decision, symbol, signals, current_position)
        
        # Log decision for analysis
        self._log_trading_decision(symbol, decision, signals, market_data)
        
        return decision
    
    def execute_trade(self, 
                     symbol: str, 
                     decision: TLResult, 
                     market_data: Dict) -> Dict:
        """
        Execute trading decision based on Ternary Logic result
        
        Returns execution report with trade details or pause information
        """
        
        execution_report = {
            'symbol': symbol,
            'timestamp': datetime.now(),
            'decision_state': decision.state.name,
            'confidence': decision.confidence,
            'reasoning': decision.reasoning
        }
        
        if decision.state == TLState.PROCEED:
            # Execute long trade
            position_size = self._calculate_position_size(decision.confidence, symbol)
            execution_report.update({
                'action': 'BUY',
                'position_size': position_size,
                'expected_return': self._estimate_expected_return(market_data),
                'risk_estimate': self._estimate_position_risk(position_size, symbol)
            })
            
            # Update portfolio
            self.positions[symbol] = self.positions.get(symbol, 0) + position_size
            self.trade_history.append(execution_report)
            
        elif decision.state == TLState.HALT:
            # Execute short trade or close long position
            current_position = self.positions.get(symbol, 0)
            if current_position > 0:
                # Close long position
                execution_report.update({
                    'action': 'SELL',
                    'position_size': -current_position,
                    'reason': 'Close long position based on negative signals'
                })
                self.positions[symbol] = 0
            else:
                # Execute short trade
                position_size = -self._calculate_position_size(decision.confidence, symbol)
                execution_report.update({
                    'action': 'SELL_SHORT',
                    'position_size': position_size,
                    'expected_return': self._estimate_expected_return(market_data),
                    'risk_estimate': self._estimate_position_risk(position_size, symbol)
                })
                self.positions[symbol] = self.positions.get(symbol, 0) + position_size
                
            self.trade_history.append(execution_report)
            
        else:  # EPISTEMIC_HOLD - Epistemic Hold activated
            # Implement Epistemic Hold protocol
            execution_report.update({
                'action': 'EPISTEMIC_HOLD',
                'monitoring_actions': decision.next_steps,
                'pause_duration': self._determine_pause_duration(decision),
                'data_requirements': self._identify_missing_data(decision)
            })
            
            # Log pause for analysis
            self.pause_history.append(execution_report)
            
        return execution_report
    
    def _calculate_momentum(self, price_data: List[float]) -> Optional[float]:
        """Calculate momentum signal from price data"""
        if len(price_data) < 20:
            return None
            
        prices = np.array(price_data[-20:])
        short_ma = np.mean(prices[-5:])
        long_ma = np.mean(prices[-20:])
        
        momentum = (short_ma - long_ma) / long_ma
        return np.clip(momentum * 10, -1, 1)  # Scale to [-1, 1]
    
    def _calculate_mean_reversion(self, price_data: List[float]) -> Optional[float]:
        """Calculate mean reversion signal"""
        if len(price_data) < 50:
            return None
            
        prices = np.array(price_data[-50:])
        current_price = prices[-1]
        mean_price = np.mean(prices)
        std_price = np.std(prices)
        
        if std_price == 0:
            return 0
            
        z_score = (current_price - mean_price) / std_price
        # Return negative z-score (mean reversion signal)
        return np.clip(-z_score / 2, -1, 1)
    
    def _calculate_volatility_signal(self, price_data: List[float]) -> Optional[float]:
        """Calculate volatility-based signal"""
        if len(price_data) < 30:
            return None
            
        returns = np.diff(np.log(price_data[-30:]))
        current_vol = np.std(returns[-5:])
        avg_vol = np.mean([np.std(returns[i:i+5]) for i in range(0, len(returns)-5, 5)])
        
        if avg_vol == 0:
            return 0
            
        vol_ratio = current_vol / avg_vol
        # Lower volatility is positive signal, higher volatility is negative
        return np.clip(2 - vol_ratio, -1, 1)
    
    def _analyze_earnings(self, earnings_data: Dict) -> Optional[float]:
        """Analyze earnings quality signal"""
        if not all(key in earnings_data for key in ['eps_actual', 'eps_estimate']):
            return None
            
        eps_surprise = (earnings_data['eps_actual'] - earnings_data['eps_estimate']) / abs(earnings_data['eps_estimate'])
        return np.clip(eps_surprise * 2, -1, 1)
    
    def _analyze_liquidity(self, order_book: Dict) -> Optional[float]:
        """Analyze market liquidity signal"""
        if not all(key in order_book for key in ['bid_size', 'ask_size', 'spread']):
            return None
            
        total_size = order_book['bid_size'] + order_book['ask_size']
        spread = order_book['spread']
        
        # Higher size and lower spread indicate better liquidity
        liquidity_score = total_size / (1 + spread * 1000)  # Normalize
        return np.clip((liquidity_score - 5000) / 5000, -1, 1)
    
    def _analyze_order_flow(self, order_book: Dict) -> Optional[float]:
        """Analyze order flow imbalance"""
        if not all(key in order_book for key in ['bid_size', 'ask_size']):
            return None
            
        total_size = order_book['bid_size'] + order_book['ask_size']
        if total_size == 0:
            return 0
            
        imbalance = (order_book['bid_size'] - order_book['ask_size']) / total_size
        return np.clip(imbalance, -1, 1)
    
    def _get_signal_weights(self, symbol: str, market_data: Dict) -> Dict[str, float]:
        """Determine signal weights based on market conditions"""
        
        base_weights = {
            'momentum': 0.2,
            'mean_reversion': 0.15,
            'volatility': 0.1,
            'earnings_quality': 0.15,
            'liquidity': 0.1,
            'order_flow': 0.1,
            'sentiment': 0.1,
            'market_regime': 0.1
        }
        
        # Adjust weights based on market regime
        if market_data.get('market_regime') == 'trending':
            base_weights['momentum'] *= 1.5
            base_weights['mean_reversion'] *= 0.5
        elif market_data.get('market_regime') == 'ranging':
            base_weights['momentum'] *= 0.5
            base_weights['mean_reversion'] *= 1.5
            
        return base_weights
    
    def _apply_risk_management(self, signals: Dict, current_position: float) -> Dict:
        """Apply risk management overlay to signals"""
        
        risk_adjusted = signals.copy()
        
        # Portfolio heat check
        if self.current_drawdown > self.max_drawdown * 0.8:
            # Reduce all signals when approaching max drawdown
            for key in risk_adjusted:
                if risk_adjusted[key] is not None:
                    risk_adjusted[key] *= 0.5
                    
        # Position size check
        if abs(current_position) > self.position_size_limit * 0.8:
            # Reduce signals for new positions when near limit
            for key in risk_adjusted:
                if risk_adjusted[key] is not None and np.sign(risk_adjusted[key]) == np.sign(current_position):
                    risk_adjusted[key] *= 0.3
                    
        return risk_adjusted
    
    def _enhance_trading_decision(self, 
                                decision: TLResult, 
                                symbol: str, 
                                signals: Dict,
                                current_position: float) -> TLResult:
        """Enhance decision with trading-specific context"""
        
        if decision.state == TLState.EPISTEMIC_HOLD:
            # Add trading-specific guidance for Epistemic Hold
            trading_steps = [
                f"Monitor {symbol} for improved signal clarity",
                "Check for news events or earnings announcements",
                "Verify data quality for missing indicators",
                "Consider reducing position size if uncertainty persists"
            ]
            decision.next_steps.extend(trading_steps)
            
        # Add trading metadata
        if decision.metadata is None:
            decision.metadata = {}
            
        decision.metadata.update({
            'symbol': symbol,
            'current_position': current_position,
            'missing_signals': [k for k, v in signals.items() if v is None],
            'signal_count': len([v for v in signals.values() if v is not None]),
            'portfolio_heat': self.current_drawdown / self.max_drawdown if self.max_drawdown > 0 else 0
        })
        
        return decision
    
    def _calculate_position_size(self, confidence: float, symbol: str) -> float:
        """Calculate position size based on confidence level"""
        
        base_size = self.position_size_limit * confidence
        
        # Adjust for current portfolio heat
        heat_adjustment = 1 - (self.current_drawdown / self.max_drawdown) if self.max_drawdown > 0 else 1
        
        return base_size * heat_adjustment * self.portfolio_value
    
    def _estimate_expected_return(self, market_data: Dict) -> float:
        """Estimate expected return based on market data"""
        # Simplified estimation for demonstration
        return 0.05  # 5% expected return
    
    def _estimate_position_risk(self, position_size: float, symbol: str) -> float:
        """Estimate position risk"""
        # Simplified risk estimation
        return abs(position_size) * 0.02  # 2% risk per position
    
    def _determine_pause_duration(self, decision: TLResult) -> int:
        """Determine how long to pause based on uncertainty factors"""
        
        base_duration = 300  # 5 minutes base pause
        
        # Longer pause for lower confidence
        confidence_multiplier = (1 - decision.confidence) + 0.5
        
        # Longer pause for more missing data
        missing_data_count = len(decision.metadata.get('missing_signals', []))
        data_multiplier = 1 + (missing_data_count * 0.2)
        
        return int(base_duration * confidence_multiplier * data_multiplier)
    
    def _identify_missing_data(self, decision: TLResult) -> List[str]:
        """Identify what data is needed to resolve uncertainty"""
        
        missing_data = decision.metadata.get('missing_signals', [])
        
        data_sources = {
            'momentum': 'Sufficient price history (20+ periods)',
            'mean_reversion': 'Extended price history (50+ periods)', 
            'volatility': 'Recent price data (30+ periods)',
            'earnings_quality': 'Latest earnings report and estimates',
            'liquidity': 'Real-time order book data',
            'order_flow': 'Level 2 market data',
            'sentiment': 'News sentiment analysis',
            'market_regime': 'Market classification model update'
        }
        
        return [data_sources.get(item, item) for item in missing_data]
    
    def _log_trading_decision(self, 
                            symbol: str, 
                            decision: TLResult, 
                            signals: Dict,
                            market_data: Dict):
        """Log decision for performance analysis"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol,
            'decision': decision.state.name,
            'confidence': decision.confidence,
            'signals': {k: v for k, v in signals.items() if v is not None},
            'missing_signals': [k for k, v in signals.items() if v is None],
            'reasoning': decision.reasoning
        }
        
        # In production, this would write to a proper logging system
        print(f"Trading Decision Log: {json.dumps(log_entry, indent=2)}")
    
    def get_performance_summary(self) -> Dict:
        """Get comprehensive performance analysis"""
        
        total_decisions = len(self.trade_history) + len(self.pause_history)
        
        if total_decisions == 0:
            return {"status": "No trading decisions made yet"}
        
        trades = len(self.trade_history)
        pauses = len(self.pause_history)
        
        return {
            "total_decisions": total_decisions,
            "trades_executed": trades,
            "epistemic_holds": pauses,
            "pause_rate": pauses / total_decisions,
            "current_positions": len([p for p in self.positions.values() if p != 0]),
            "portfolio_value": self.portfolio_value,
            "current_drawdown": self.current_drawdown,
            "avg_confidence_trades": np.mean([t.get('confidence', 0) for t in self.trade_history]) if trades > 0 else 0,
            "framework_version": "Ternary Logic Framework v1.0"
        }

def demonstrate_trading_algorithm():
    """
    Demonstrate the TL Trading Algorithm with realistic scenarios
    """
    
    print("🚀 Ternary Logic Trading Algorithm Demonstration")
    print("=" * 55)
    print()
    print("Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)")
    print("Contact: leogouk@gmail.com")
    print('"The Epistemic Hold saves portfolios."')
    print()
    
    # Initialize algorithm
    algorithm = TLTradingAlgorithm(
        confidence_threshold=0.75,
        position_size_limit=0.1,
        max_drawdown=0.05
    )
    
    # Test Scenario 1: Clear Bull Signal
    print("📈 Scenario 1: Strong Bull Market Signals")
    print("-" * 40)
    
    bull_market_data = {
        'price_data': [100, 102, 104, 106, 108, 110, 112, 115, 118, 120] * 6,  # Strong uptrend
        'earnings_data': {'eps_actual': 2.50, 'eps_estimate': 2.00},  # Beat estimates
        'order_book': {'bid_size': 10000, 'ask_size': 8000, 'spread': 0.01},  # Good liquidity
        'news_sentiment': 0.8,  # Positive sentiment
        'market_regime': 'trending'
    }
    
    decision = algorithm.make_trading_decision('AAPL', bull_market_data)
    execution = algorithm.execute_trade('AAPL', decision, bull_market_data)
    
    print(f"Decision: {decision.state.name} (Confidence: {decision.confidence:.2f})")
    print(f"Action: {execution.get('action', 'N/A')}")
    print(f"Reasoning: {decision.reasoning}")
    print()
    
    # Test Scenario 2: Uncertain Market with Missing Data
    print("⚠️  Scenario 2: Uncertain Market - Missing Critical Data")
    print("-" * 52)
    
    uncertain_market_data = {
        'price_data': [100, 98, 102, 99, 103, 97, 101],  # Choppy, insufficient history
        'earnings_data': None,  # Missing earnings data
        'order_book': None,     # Missing order book
        'news_sentiment': 0.1,  # Slightly positive but weak
        'market_regime': None   # Unknown market regime
    }
    
    decision = algorithm.make_trading_decision('TSLA', uncertain_market_data)
    execution = algorithm.execute_trade('TSLA', decision, uncertain_market_data)
    
    print(f"Decision: {decision.state.name} (Confidence: {decision.confidence:.2f})")
    print(f"Action: {execution.get('action', 'N/A')}")
    print(f"Reasoning: {decision.reasoning}")
    
    if decision.state == TLState.EPISTEMIC_HOLD:
        print("Epistemic Hold Activated - Next Steps:")
        for i, step in enumerate(execution.get('monitoring_actions', [])[:3], 1):
            print(f"  {i}. {step}")
        print(f"Pause Duration: {execution.get('pause_duration', 0)} seconds")
    print()
    
    # Test Scenario 3: Clear Bear Signal
    print("📉 Scenario 3: Strong Bear Market Signals")
    print("-" * 38)
    
    bear_market_data = {
        'price_data': [120, 118, 115, 112, 110, 108, 106, 104, 102, 100] * 5,  # Strong downtrend
        'earnings_data': {'eps_actual': 1.50, 'eps_estimate': 2.00},  # Missed estimates
        'order_book': {'bid_size': 5000, 'ask_size': 15000, 'spread': 0.05},  # Poor liquidity
        'news_sentiment': -0.7,  # Very negative sentiment
        'market_regime': 'trending'
    }
    
    decision = algorithm.make_trading_decision('NFLX', bear_market_data)
    execution = algorithm.execute_trade('NFLX', decision, bear_market_data)
    
    print(f"Decision: {decision.state.name} (Confidence: {decision.confidence:.2f})")
    print(f"Action: {execution.get('action', 'N/A')}")
    print(f"Reasoning: {decision.reasoning}")
    print()
    
    # Performance Summary
    print("📊 Algorithm Performance Summary")
    print("-" * 32)
    summary = algorithm.get_performance_summary()
    
    print(f"Total Decisions: {summary['total_decisions']}")
    print(f"Trades Executed: {summary['trades_executed']}")
    print(f"Epistemic Holds: {summary['epistemic_holds']}")
    print(f"Pause Rate: {summary['pause_rate']:.1%}")
    print(f"Average Trade Confidence: {summary['avg_confidence_trades']:.2f}")
    print()
    
    print("✨ The Epistemic Hold in Action!")
    print("Notice how the algorithm intelligently recognizes when market")
    print("conditions are too uncertain for confident trading decisions.")
    print("This prevents flash crashes and reduces portfolio volatility.")
    print()
    print("As Lev Goukassian demonstrated: 'The Epistemic Hold saves portfolios.'")

if __name__ == "__main__":
    demonstrate_trading_algorithm()

## Contact Information

**Created by Lev Goukassian**
* **ORCID**: 0009-0006-5966-1243
* **Email**: leogouk@gmail.com

**Successor Contact**: support@tl-goukassian.org  
(see [Succession Charter](/memorial/SUCCESSION_CHARTER.md))
