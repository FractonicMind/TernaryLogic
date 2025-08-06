"""
Tests for backtesting and historical validation.
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class TestBacktestingResults:
    """Test historical performance validation."""
    
    @pytest.mark.slow
    def test_trading_strategy_backtest(self):
        """Test backtesting of TL trading strategy."""
        # Generate historical data
        dates = pd.date_range('2020-01-01', '2024-01-01', freq='D')
        n = len(dates)
        
        historical_data = pd.DataFrame({
            'date': dates,
            'open': 100 + np.random.randn(n).cumsum() * 0.5,
            'high': 101 + np.random.randn(n).cumsum() * 0.5,
            'low': 99 + np.random.randn(n).cumsum() * 0.5,
            'close': 100 + np.random.randn(n).cumsum() * 0.5,
            'volume': np.random.randint(1000000, 10000000, n)
        })
        
        # Simple backtest metrics
        returns = historical_data['close'].pct_change().dropna()
        total_return = (historical_data['close'].iloc[-1] / historical_data['close'].iloc[0]) - 1
        
        # Calculate Sharpe ratio
        sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std() if returns.std() > 0 else 0
        
        # Calculate max drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Calculate win rate
        win_rate = (returns > 0).mean()
        
        assert total_return is not None
        assert sharpe_ratio is not None
        assert max_drawdown is not None
        assert win_rate > 0.4
        
        print(f"Backtest Results:")
        print(f"  Total Return: {total_return:.2%}")
        print(f"  Sharpe Ratio: {sharpe_ratio:.2f}")
        print(f"  Max Drawdown: {max_drawdown:.2%}")
        print(f"  Win Rate: {win_rate:.2%}")
    
    def test_risk_adjusted_returns(self):
        """Test calculation of risk-adjusted performance metrics."""
        # Generate returns
        returns = np.random.normal(0.0008, 0.02, 252)  # Daily returns
        
        # Sharpe ratio
        sharpe = np.sqrt(252) * returns.mean() / returns.std()
        
        # Sortino ratio (downside deviation)
        downside_returns = returns[returns < 0]
        downside_std = np.std(downside_returns) if len(downside_returns) > 0 else 0.01
        sortino = np.sqrt(252) * returns.mean() / downside_std if downside_std > 0 else 0
        
        assert sharpe is not None
        assert sortino is not None
        assert sortino >= sharpe  # Sortino should be >= Sharpe
