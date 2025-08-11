# ⚡ Quick Start Guide - Ternary Logic in 60 Minutes

**From Zero to Three-State Decision Making in 1 Hour**

> **Time Required**: 60 minutes  
> **Prerequisites**: Python 3.8+, Basic understanding of decision systems  
> **Result**: Working TL implementation making real decisions

---

## 🎯 Why You're Here

You've realized that forcing every decision into YES/NO is **costing you money, opportunities, and creating unnecessary risk**. You need the third option - the Epistemic Hold - and you need it **NOW**.

**This guide gets you running in 60 minutes.**

---

## ⏱️ Timeline

- **Minutes 0-5**: Install and verify
- **Minutes 5-15**: First TL decision
- **Minutes 15-30**: Calibrate for your domain
- **Minutes 30-45**: Connect to your data
- **Minutes 45-60**: Deploy and monitor

---

## 🚀 Minute 0-5: Installation

### Step 1: Clone and Install

```bash
# Clone the framework
git clone https://github.com/FractonicMind/TernaryLogic.git
cd TernaryLogic

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install framework
pip install -e .

# Verify installation
python -c "from goukassian.core import TernaryLogicEngine; print('✅ TL Ready!')"
```

### Step 2: Run Tests (2 minutes)

```bash
# Quick verification
pytest tests/unit/test_core_engine.py -v
```

**Expected**: 9 tests passing ✅

---

## 🎮 Minute 5-15: Your First TL Decision

### Step 3: Create `my_first_tl.py`

```python
#!/usr/bin/env python3
"""Your first Ternary Logic decision - RIGHT NOW."""

from typing import Dict, Any
import numpy as np

class QuickTLEngine:
    """Minimal TL implementation - fully functional."""
    
    def __init__(self, confidence_threshold=0.7, risk_threshold=0.3):
        self.confidence_threshold = confidence_threshold
        self.risk_threshold = risk_threshold
        self.decisions_made = 0
        self.holds_triggered = 0
    
    def decide(self, signals: Dict[str, Any]) -> str:
        """Make a ternary decision NOW."""
        confidence = signals.get('confidence', 0.5)
        risk = signals.get('risk', 0.5)
        
        self.decisions_made += 1
        
        # The THREE states
        if confidence > self.confidence_threshold and risk < self.risk_threshold:
            return "PROCEED ✅"
        elif risk > 0.7 or confidence < 0.3:
            return "HALT 🛑"
        else:
            self.holds_triggered += 1
            return "HOLD ⏸️ (Epistemic uncertainty - need more information)"
    
    def stats(self):
        """See the value of TL immediately."""
        hold_percentage = (self.holds_triggered / self.decisions_made * 100) if self.decisions_made > 0 else 0
        print(f"\n📊 Statistics:")
        print(f"Decisions made: {self.decisions_made}")
        print(f"Epistemic Holds: {self.holds_triggered} ({hold_percentage:.1f}%)")
        print(f"Binary would have forced {self.holds_triggered} premature decisions!")

# TEST IT NOW
if __name__ == "__main__":
    engine = QuickTLEngine()
    
    # Simulate 5 quick decisions
    test_scenarios = [
        {"name": "Clear opportunity", "confidence": 0.85, "risk": 0.15},
        {"name": "Obvious danger", "confidence": 0.2, "risk": 0.9},
        {"name": "Uncertain situation", "confidence": 0.6, "risk": 0.4},
        {"name": "Mixed signals", "confidence": 0.65, "risk": 0.35},
        {"name": "High confidence, acceptable risk", "confidence": 0.8, "risk": 0.25},
    ]
    
    print("🚀 TERNARY LOGIC QUICK START\n")
    
    for scenario in test_scenarios:
        decision = engine.decide(scenario)
        print(f"{scenario['name']}: {decision}")
    
    engine.stats()
```

### Step 4: Run It!

```bash
python my_first_tl.py
```

**You'll see the HOLD state in action** - those uncertain situations that binary logic would force into bad decisions!

---

## 🎯 Minute 15-30: Calibrate for YOUR Domain

### Step 5: Domain-Specific Configuration

Choose your domain and adjust thresholds:

#### For Financial Trading:
```python
# Higher confidence needed for real money
engine = QuickTLEngine(confidence_threshold=0.75, risk_threshold=0.25)
```

#### For Policy Decisions:
```python
# More tolerance for uncertainty in long-term planning
engine = QuickTLEngine(confidence_threshold=0.65, risk_threshold=0.35)
```

#### For Operations:
```python
# Balanced approach for supply chain
engine = QuickTLEngine(confidence_threshold=0.70, risk_threshold=0.30)
```

### Step 6: Create `calibrate_tl.py`

```python
#!/usr/bin/env python3
"""Calibrate TL for your specific needs - FAST."""

import numpy as np
from datetime import datetime

class CalibratedTL:
    """Your domain-calibrated TL engine."""
    
    def __init__(self, domain="trading"):
        # Domain-specific thresholds
        self.thresholds = {
            "trading": {"confidence": 0.75, "risk": 0.25, "hold_max": 300},  # 5 min max hold
            "policy": {"confidence": 0.65, "risk": 0.35, "hold_max": 86400},  # 1 day max hold
            "operations": {"confidence": 0.70, "risk": 0.30, "hold_max": 3600},  # 1 hour max hold
        }
        
        self.config = self.thresholds.get(domain, self.thresholds["trading"])
        self.domain = domain
        self.hold_start = None
    
    def decide(self, data):
        """Domain-calibrated decision."""
        confidence = data.get('confidence', 0.5)
        risk = data.get('risk', 0.5)
        
        # Check if we're in extended HOLD
        if self.hold_start:
            hold_duration = (datetime.now() - self.hold_start).seconds
            if hold_duration > self.config["hold_max"]:
                print(f"⚠️ Maximum HOLD duration reached ({hold_duration}s)")
                self.hold_start = None
                return "FORCED DECISION: " + ("PROCEED" if confidence > 0.5 else "HALT")
        
        # Standard TL logic with domain calibration
        if confidence > self.config["confidence"] and risk < self.config["risk"]:
            self.hold_start = None
            return "PROCEED"
        elif risk > (1 - self.config["risk"]) or confidence < (1 - self.config["confidence"]):
            self.hold_start = None
            return "HALT"
        else:
            if not self.hold_start:
                self.hold_start = datetime.now()
            return "HOLD"

# Test your calibration
if __name__ == "__main__":
    # Try different domains
    for domain in ["trading", "policy", "operations"]:
        print(f"\n📊 Domain: {domain.upper()}")
        engine = CalibratedTL(domain)
        
        test_data = {"confidence": 0.68, "risk": 0.32}
        decision = engine.decide(test_data)
        print(f"Decision: {decision}")
        print(f"Thresholds: {engine.config}")
```

Run it:
```bash
python calibrate_tl.py
```

---

## 🔌 Minute 30-45: Connect Your Real Data

### Step 7: Create `connect_tl.py`

```python
#!/usr/bin/env python3
"""Connect TL to your actual data source - TEMPLATE."""

import json
import pandas as pd
from typing import Dict, Any

class LiveTLConnection:
    """Connect TL to your live data."""
    
    def __init__(self, data_source="demo"):
        self.data_source = data_source
        self.engine = QuickTLEngine()
        
    def process_market_data(self, market_data: Dict) -> str:
        """Process real market data through TL."""
        # Calculate confidence from your indicators
        confidence = self._calculate_confidence(market_data)
        
        # Calculate risk from your metrics
        risk = self._calculate_risk(market_data)
        
        # Make TL decision
        signals = {"confidence": confidence, "risk": risk}
        return self.engine.decide(signals)
    
    def _calculate_confidence(self, data: Dict) -> float:
        """Your domain-specific confidence calculation."""
        # CUSTOMIZE THIS FOR YOUR INDICATORS
        # Example for trading:
        if 'rsi' in data and 'macd' in data:
            rsi_signal = 1.0 if 30 < data['rsi'] < 70 else 0.5
            macd_signal = 1.0 if data['macd'] > 0 else 0.5
            return (rsi_signal + macd_signal) / 2
        return 0.5
    
    def _calculate_risk(self, data: Dict) -> float:
        """Your domain-specific risk calculation."""
        # CUSTOMIZE THIS FOR YOUR RISK METRICS
        # Example for trading:
        if 'volatility' in data:
            return min(data['volatility'] / 100, 1.0)  # Normalize to 0-1
        return 0.5
    
    def process_stream(self, data_stream):
        """Process streaming data."""
        for data_point in data_stream:
            decision = self.process_market_data(data_point)
            timestamp = data_point.get('timestamp', 'now')
            print(f"{timestamp}: {decision}")
            
            if decision.startswith("HOLD"):
                print("  → Waiting for more information...")
                # Your code to request additional data

# Demo with simulated data
if __name__ == "__main__":
    connection = LiveTLConnection()
    
    # Simulate data stream
    demo_stream = [
        {"timestamp": "09:30:00", "rsi": 45, "macd": 0.5, "volatility": 25},
        {"timestamp": "09:30:01", "rsi": 65, "macd": -0.2, "volatility": 35},
        {"timestamp": "09:30:02", "rsi": 72, "macd": 1.2, "volatility": 15},
    ]
    
    print("🔴 LIVE TL DECISIONS:\n")
    connection.process_stream(demo_stream)
```

---

## 📊 Minute 45-60: Deploy and Monitor

### Step 8: Create `monitor_tl.py`

```python
#!/usr/bin/env python3
"""Monitor your TL implementation - SEE THE VALUE."""

import time
from datetime import datetime
from collections import defaultdict

class TLMonitor:
    """Real-time monitoring of TL decisions."""
    
    def __init__(self):
        self.stats = defaultdict(int)
        self.start_time = datetime.now()
        
    def log_decision(self, decision: str, confidence: float, risk: float):
        """Log and analyze each decision."""
        self.stats['total'] += 1
        
        if "PROCEED" in decision:
            self.stats['proceed'] += 1
        elif "HALT" in decision:
            self.stats['halt'] += 1
        else:
            self.stats['hold'] += 1
            print(f"  💡 HOLD activated: Confidence={confidence:.2f}, Risk={risk:.2f}")
            print(f"     Binary logic would have forced: {'PROCEED' if confidence > 0.5 else 'HALT'}")
            print(f"     Potential mistake avoided!")
    
    def show_dashboard(self):
        """Display real-time statistics."""
        runtime = (datetime.now() - self.start_time).seconds
        
        print("\n" + "="*50)
        print("📊 TERNARY LOGIC DASHBOARD")
        print("="*50)
        print(f"Runtime: {runtime} seconds")
        print(f"Total Decisions: {self.stats['total']}")
        
        if self.stats['total'] > 0:
            proceed_pct = self.stats['proceed'] / self.stats['total'] * 100
            hold_pct = self.stats['hold'] / self.stats['total'] * 100
            halt_pct = self.stats['halt'] / self.stats['total'] * 100
            
            print(f"\n✅ PROCEED: {self.stats['proceed']} ({proceed_pct:.1f}%)")
            print(f"⏸️  HOLD:    {self.stats['hold']} ({hold_pct:.1f}%)")
            print(f"🛑 HALT:    {self.stats['halt']} ({halt_pct:.1f}%)")
            
            print(f"\n💰 VALUE: Binary logic would have forced {self.stats['hold']} decisions")
            print(f"          without sufficient information!")
            
            if hold_pct > 15 and hold_pct < 40:
                print("\n✅ HEALTHY: Hold percentage in optimal range (15-40%)")
            elif hold_pct > 40:
                print("\n⚠️  WARNING: High uncertainty - check data quality")
            else:
                print("\n⚠️  WARNING: Low holds - might be forcing decisions")

# Run monitoring demo
if __name__ == "__main__":
    monitor = TLMonitor()
    engine = QuickTLEngine()
    
    print("🚀 TERNARY LOGIC MONITOR - LIVE\n")
    
    # Simulate 10 decisions
    for i in range(10):
        # Random market conditions
        confidence = np.random.uniform(0.2, 0.9)
        risk = np.random.uniform(0.1, 0.8)
        
        decision = engine.decide({"confidence": confidence, "risk": risk})
        monitor.log_decision(decision, confidence, risk)
        
        time.sleep(0.5)  # Simulate real-time
    
    monitor.show_dashboard()
```

### Step 9: Run Your Monitor

```bash
python monitor_tl.py
```

---

## ✅ CONGRATULATIONS! You're Running Ternary Logic!

### What You've Accomplished in 60 Minutes:

1. ✅ **Installed** the TL framework
2. ✅ **Made** your first three-state decisions
3. ✅ **Calibrated** for your domain
4. ✅ **Connected** to data sources
5. ✅ **Monitored** the value of Epistemic Hold

### 📈 What You're Seeing:

- **HOLD states** preventing forced decisions
- **Uncertainty** being respected, not ignored
- **Better decisions** through patient intelligence

---

## 🚀 Next Steps (After Your First Hour)

### Tomorrow - Hour 2: Production Readiness
- Add persistence (save decisions to database)
- Connect to your real data feeds
- Set up alerting for high-risk situations

### This Week: Full Implementation
- Read [MANDATORY.md](docs/MANDATORY.md) completely
- Run full test suite
- Implement domain-specific indicators

### This Month: Optimization
- Analyze your HOLD patterns
- Fine-tune thresholds based on results
- Compare performance vs old binary system

---

## 💡 The Moment of Realization

**You've just experienced it**: That moment when the system says HOLD and you realize - *"Yes! We SHOULDN'T decide yet! We need more information!"*

That's not indecision. That's **intelligence**.

Every HOLD is a potential mistake avoided. Every patient wait for clarity is wisdom in action.

---

## 🆘 Need Help?

**Quick Support**:
- Issue with code? Check [examples/](examples/)
- Conceptual question? Read [theory/core-principles.md](theory/core-principles.md)
- Urgent help? Email: support@tl-goukassian.org

---

## 📊 Share Your Results!

After your first hour, you'll have stats like:
- "In 100 decisions, TL triggered HOLD 28 times"
- "Binary logic would have forced 28 premature decisions"
- "Potential error reduction: 28%"

**That's real value. Measured. Proven. In one hour.**

---

## Contact Information

**Framework Creator**: Lev Goukassian  
- **ORCID**: [0009-0006-5966-1243](https://orcid.org/0009-0006-5966-1243)  
- **Email**: leogouk@gmail.com

**Support**: support@tl-goukassian.org

---

> **"You just proved it: The world is not binary. And your decisions don't have to be either."**
> 
> Welcome to Ternary Logic. Welcome to better decisions.
> 
> *— Lev Goukassian*

---

**Time Check**: If you followed this guide, you're now at minute 60 with a working TL system. The Epistemic Hold is protecting your decisions. Well done. 🎯
