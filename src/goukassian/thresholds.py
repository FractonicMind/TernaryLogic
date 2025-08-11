"""Dynamic threshold management."""

class ThresholdManager:
    """Manages decision thresholds."""
    
    def __init__(self):
        self.thresholds = {
            'confidence': 0.7,
            'risk': 0.3,
            'uncertainty': 0.5
        }
    
    def get_threshold(self, key):
        """Get threshold value."""
        return self.thresholds.get(key, 0.5)
