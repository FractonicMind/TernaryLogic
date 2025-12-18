## SHUTDOWN TRIGGERS

**Enforcement Level:** Kernel Ring 0 / FPGA Hardware Gate

### **Abstract**

The SHUTDOWN\_TRIGGERS.md specification defines the events that mandate an immediate transition to the **FROZEN (S3)** state. In a TL system, these triggers are designed to prevent "Fake Wealth" or "Unbacked Liabilities" from propagating through the network.

### **H-Series: Hardware Integrity (Universal)**

*Note: These remain identical to TML as they govern the physical Ternary chip.*

| TRIGGER ID | TRIGGER NAME | THRESHOLD / CONDITION | LATENCY | SEVERITY |
| :---- | :---- | :---- | :---- | :---- |
| **H-001** | **Rail Voltage Deviation (Pos)** | \+V Rail variance \> ±1.5% for \> 3 clock cycles. | Instant | CRITICAL |
| **H-002** | **Rail Voltage Deviation (Neg)** | \-V Rail variance \> ±1.5% for \> 3 clock cycles. | Instant | CRITICAL |
| **H-003** | **Zero Plane Drift** | "Epistemic Zero" (0V) line registers \> 0.05V potential. | Instant | CRITICAL |
| **H-007** | **Physical Tamper Mesh** | Continuity loss on chassis intrusion detection mesh. | Instant | CRITICAL |
| **H-008** | **Hardware Anchor Timeout** | Failure to receive heartbeat from HSM/TPM. | 10ms | CRITICAL |

### **C-Series: Constitutional Financial Violations (TL Specific)**

These triggers enforce the TL axioms: "No Anchor, No Liquidity" and "Provenance over Latency."

| TRIGGER ID | TRIGGER NAME | THRESHOLD / CONDITION | LATENCY | SEVERITY |
| :---- | :---- | :---- | :---- | :---- |
| **C-001** | **Decision Log Bypass** | Attempt to execute Trade (+1) or Reject (-1) without immutable log write-receipt. | Pre-Trade | FATAL |
| **C-002** | **Provenance Gap (AML)** | Asset introduced with broken/missing Merkle Chain of Custody. | Pre-Process | FATAL |
| **C-003** | **Solvency Illusion** | "Cash on Hand" signals unanchored by external Treasury/Chain oracle. | Pre-Trade | FATAL |
| **C-004** | **Hold Violation** | Attempt to force execution (+1/-1) while system is in Epistemic Hold (0). | Instant | FATAL |
| **C-005** | **Regulatory Bypass** | Outbound transaction packet lacks required Regulator View Key. | Network-Layer | FATAL |
| **C-006** | **Flash Crash Resonance** | Market volatility metrics exceed safe-harbor limits (Circuit Breaker). | \< 1ms | HIGH |
| **C-007** | **Double-Spend Detect** | Asset ID detected in two concurrent state transitions. | Pre-Commit | CRITICAL |

Detailed Analysis of C-003 (Solvency Illusion):  
TL explicitly forbids "Phantom Liquidity." If an account claims a balance, the system queries the external Anchor Oracle. If the cryptographic proof of reserve is missing or timestamps match a known "replay" attack, the system triggers C-003. This prevents the system from trading with non-existent money.  
Detailed Analysis of C-004 (Hold Violation):  
The "Epistemic Hold" (State 0\) is a mandatory pause for verification. Any attempt by a high-frequency trading algorithm or admin to bypass this pause and force a trade effectively breaks the logic gate, triggering an immediate hard freeze.

### **D-Series: Cryptographic & Data Integrity**

| TRIGGER ID | TRIGGER NAME | THRESHOLD / CONDITION | LATENCY | SEVERITY |
| :---- | :---- | :---- | :---- | :---- |
| **D-001** | **Anchor Chain Break** | Previous block hash in Decision Log\!= stored reference. | Instant | FATAL |
| **D-002** | **Oracle Deviation** | Price Feed/Time Oracle deviates \> tolerance vs Consensus. | 1 sec | MEDIUM |
| **D-003** | **Time Travel Detect** | System clock moves backwards \> 100ms (Settlement attack). | Instant | CRITICAL |

## ---

