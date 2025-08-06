"""
Performance tests for execution speed.
"""
import pytest
import time
import numpy as np


class TestExecutionSpeed:
    """Test execution speed and performance benchmarks."""
    
    @pytest.mark.performance
    def test_single_decision_speed(self, tl_engine):
        """Benchmark single decision execution time."""
        signals = {'confidence': 0.75, 'risk': 0.25}
        
        start_time = time.perf_counter()
        result = tl_engine.make_decision(signals)
        end_time = time.perf_counter()
        
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        
        assert result.state is not None
        assert execution_time < 10  # Less than 10ms
        print(f"Single decision time: {execution_time:.3f}ms")
    
    @pytest.mark.performance
    def test_batch_decision_speed(self, tl_engine):
        """Benchmark batch decision processing."""
        # Create batch of 1000 decisions
        batch = [
            {'confidence': np.random.random(), 'risk': np.random.random()}
            for _ in range(1000)
        ]
        
        start_time = time.perf_counter()
        results = [tl_engine.make_decision(signals) for signals in batch]
        end_time = time.perf_counter()
        
        total_time = end_time - start_time
        
        assert len(results) == 1000
        assert total_time < 5.0  # Less than 5 seconds for 1000
        print(f"Batch processing: {1000/total_time:.0f} decisions/second")
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_high_frequency_decisions(self, tl_engine):
        """Test sustained high-frequency decision making."""
        duration = 1.0  # 1 second test
        decisions = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            signals = {
                'confidence': np.random.random(),
                'risk': np.random.random()
            }
            tl_engine.make_decision(signals)
            decisions += 1
        
        decisions_per_second = decisions / duration
        
        assert decisions_per_second > 100  # At least 100 decisions/second
        print(f"Achieved {decisions_per_second:.0f} decisions/second")
