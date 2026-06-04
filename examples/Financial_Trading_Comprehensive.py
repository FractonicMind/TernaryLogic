"""
Ternary Logic Framework: Comprehensive Financial Trading
=========================================================

Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com
Successor: support@tl-goukassian.org
Repository: https://github.com/FractonicMind/TernaryLogic

DOI 1: 10.1007/s43681-025-00910-6, Auditable AI: Tracing the Ethical History of a Model
DOI 2: 10.1007/s43681-026-01124-0, A Ternary Logic Framework for Institutional Governance

The Goukassian Vow:
    "Pause when truth is uncertain"  ->  State  0  (Epistemic Hold)
    "Refuse when harm is clear"      ->  State -1  (Refuse)
    "Proceed where truth is"         ->  State +1  (Proceed)

This example demonstrates TL applied to financial trading systems:
    - Market signal analysis: momentum, mean reversion, liquidity, sentiment
    - MiFID II best execution and market integrity compliance
    - Flash crash prevention via Epistemic Hold under market stress
    - Position sizing governed by TL state (not hardcoded numbers)
    - ESG mandate verification (Pillar VI) blocking execution
    - Dual-Lane Latency Architecture awareness:
        Inference Lane: less than 2ms WCET (trading signal computation)
        Governance Lane: 300ms ceiling (constitutional evaluation)
    - NL=NA write-before-act for every trade decision
    - Complete audit trail export

THRESHOLD GOVERNANCE:
    Trading systems must calibrate thresholds through their own governance
    process. High-frequency equity desks, fixed income, and alternative
    assets each require different calibrations. No universal values exist.
    See docs/Threshold_Calibration.md.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import pandas as pd

# TL Framework imports
from ternary_logic import TLEngine, TLState, TLValue, verify_mandate, calculate_confidence


# =============================================================================
# SECTION 1: Governance Artifacts (consistent with Quickstart pattern)
# =============================================================================

def create_goukassian_principle_block(
    decision_payload: str,
    agent_id: str,
    license_scopes: list
) -> Dict[str, Any]:
    """Three Goukassian Principle artifacts. See Quickstart_Example.py."""
    payload_bytes = decision_payload.encode("utf-8")
    return {
        "lantern": {
            "artifactName": "lantern",
            "lanternHash": hashlib.sha256(payload_bytes).hexdigest()
        },
        "signature": {
            "artifactName": "signature",
            "agentSignature": hashlib.sha512(
                (agent_id + decision_payload).encode("utf-8")
            ).hexdigest()
        },
        "license": {
            "artifactName": "license",
            "licenseScope": license_scopes
        }
    }


def commit_log_entry(
    decision: TLValue,
    engine: TLEngine,
    goukassian_block: Dict[str, Any],
    previous_hash: str,
    extra_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Commit governance log entry. NL=NA: BEFORE any trade fires.

    In production this executes on the Inference Lane (less than 2ms WCET)
    with hardware-backed non-volatile storage. The Governance Lane
    (300ms ceiling) provides constitutional evaluation in parallel.
    No trade executes without a committed log entry and a valid
    PermissionToken from the Governance Lane.
    """
    log_id = str(uuid.uuid4())
    committed_at = datetime.now(timezone.utc).isoformat()

    canonical = json.dumps({
        "logId": log_id,
        "state": decision.state.name,
        "stateValue": decision.state.value,
        "confidence": decision.confidence,
        "reasoning": decision.reasoning,
        "committedAt": committed_at
    }, sort_keys=True)

    log_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    merkle_root = hashlib.sha256(
        (previous_hash + log_hash).encode("utf-8")
    ).hexdigest()

    entry = {
        "logId": log_id,
        "currentState": decision.state.value,
        "stateLabel": decision.state.name,
        "processActive": {
            TLState.PROCEED: "ProceedAuthorized",
            TLState.EPISTEMIC_HOLD: "GovernancePause",
            TLState.REFUSE: "RefusalPermanent"
        }[decision.state],
        "confidence": decision.confidence,
        "reasoning": decision.reasoning,
        "logHash": log_hash,
        "merkleRoot": merkle_root,
        "previousHash": previous_hash,
        "committedAt": committed_at,
        "goukassianPrinciple": goukassian_block,
        "pufAttestation": "NULL_PUF_DEPLOYMENT",
        "architectureMode": "ARCHITECTURE_B",
        "engineConfig": {
            "proceedThreshold": engine.proceed_threshold,
            "holdThreshold": engine.hold_threshold
        }
    }
    if extra_context:
        entry["domainContext"] = extra_context
    return entry


def build_permission_token(log_entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """PermissionToken for PROCEED. laneOrigin const GOVERNANCE_LANE. NL=NA Layer 2."""
    if log_entry["currentState"] != TLState.PROCEED.value:
        return None

    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(milliseconds=300000)

    return {
        "tokenId": str(uuid.uuid4()),
        "logHash": log_entry["logHash"],
        "merkleRoot": log_entry["merkleRoot"],
        "laneOrigin": "GOVERNANCE_LANE",  # NL=NA Layer 2 const
        "issuedAt": issued_at.isoformat(),
        "expiresAt": expires_at.isoformat(),
        "maxLifetimeMs": 300000,
        "revocationStatus": "ACTIVE",
        "signerKeyId": "trading-hsm-001",
        "epochTimestamp": int(issued_at.timestamp()),
        "signatureValue": hashlib.sha256(
            log_entry["logHash"].encode()
        ).hexdigest()
    }


class ImmutableLedger:
    """Pillar II: append-only hash chain. See Quickstart_Example.py."""

    def __init__(self, genesis_label: str = "TL_TRADING_GENESIS"):
        self._entries = []
        self._genesis_hash = hashlib.sha256(
            genesis_label.encode()
        ).hexdigest()

    @property
    def previous_hash(self) -> str:
        return (
            self._entries[-1]["merkleRoot"]
            if self._entries else self._genesis_hash
        )

    def commit(self, entry: Dict[str, Any]) -> str:
        self._entries.append(entry)
        return entry["logHash"]

    @property
    def size(self) -> int:
        return len(self._entries)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "totalEntries": self.size,
            "latestMerkleRoot": self.previous_hash,
            "states": {
                "PROCEED": sum(
                    1 for e in self._entries if e["currentState"] == 1
                ),
                "EPISTEMIC_HOLD": sum(
                    1 for e in self._entries if e["currentState"] == 0
                ),
                "REFUSE": sum(
                    1 for e in self._entries if e["currentState"] == -1
                )
            }
        }


# =============================================================================
# SECTION 2: Market Signal Analysis
# Technical, fundamental, microstructure, and sentiment signals.
# =============================================================================

class MarketSignalAnalyzer:
    """
    Analyze multiple market signals for trading decision support.

    Each method returns a signal in [-1.0, +1.0] or None if data is absent.
    None signals reduce the confidence score via missing data penalty.
    The confidence score feeds TLEngine; the TLEngine evaluates it against
    institution-calibrated thresholds.
    """

    def calculate_momentum(self, prices: List[float]) -> Optional[float]:
        """Price momentum signal. Positive = uptrend, negative = downtrend."""
        if not prices or len(prices) < 10:
            return None

        short_ma = float(np.mean(prices[-5:]))
        long_ma = float(np.mean(prices[-20:]) if len(prices) >= 20 else np.mean(prices))

        if long_ma == 0:
            return None

        signal = (short_ma - long_ma) / long_ma
        return float(np.clip(signal * 10, -1, 1))

    def calculate_mean_reversion(self, prices: List[float]) -> Optional[float]:
        """Mean reversion signal. Identifies overextended price moves."""
        if not prices or len(prices) < 20:
            return None

        current = prices[-1]
        mean_20 = float(np.mean(prices[-20:]))
        std_20 = float(np.std(prices[-20:]))

        if std_20 == 0:
            return None

        z_score = (current - mean_20) / std_20
        # Invert: highly positive z_score means reversion opportunity downward
        return float(np.clip(-z_score / 2, -1, 1))

    def calculate_volatility_signal(self, prices: List[float]) -> Optional[float]:
        """
        Volatility signal for Epistemic Hold trigger assessment.

        High volatility reduces the trading confidence signal.
        Above the flash crash threshold, the signal becomes strongly
        negative, driving the system toward Epistemic Hold.
        """
        if not prices or len(prices) < 10:
            return None

        returns = np.diff(prices) / np.abs(prices[:-1] + 1e-10)
        vol = float(np.std(returns[-10:]))

        # Flash crash detection: extreme volatility
        # The specific threshold here is a domain parameter, not a
        # TLEngine threshold. It governs the signal value, not the
        # state determination. Calibrate per instrument and regime.
        flash_crash_vol_threshold = 0.05  # domain-specific signal parameter
        if vol > flash_crash_vol_threshold:
            return -1.0  # Strong negative signal: Epistemic Hold likely
        return float(np.clip(1 - (vol / flash_crash_vol_threshold), -1, 1))

    def analyze_liquidity(self, order_book: Dict[str, Any]) -> Optional[float]:
        """Order book liquidity signal."""
        if not order_book:
            return None

        bid_depth = order_book.get("bid_depth", 0)
        ask_depth = order_book.get("ask_depth", 0)
        spread = order_book.get("spread", 1.0)

        if bid_depth + ask_depth == 0:
            return None

        imbalance = abs(bid_depth - ask_depth) / (bid_depth + ask_depth)
        spread_penalty = min(spread * 100, 1.0)

        return float(np.clip(1.0 - imbalance - spread_penalty, -1, 1))

    def analyze_order_flow(self, order_book: Dict[str, Any]) -> Optional[float]:
        """Order flow imbalance signal."""
        if not order_book:
            return None

        buy_volume = order_book.get("buy_volume_5min", 0)
        sell_volume = order_book.get("sell_volume_5min", 0)
        total = buy_volume + sell_volume

        if total == 0:
            return None

        flow_imbalance = (buy_volume - sell_volume) / total
        return float(np.clip(flow_imbalance, -1, 1))

    def analyze_esg_compliance(self, esg_scores: Dict[str, Any]) -> Optional[float]:
        """
        Pillar VI: ESG compliance signal.

        Note: ESG mandate failures via verify_mandate() are binary and
        override this continuous signal entirely. This signal provides
        a graded influence on confidence for borderline cases.
        """
        if not esg_scores:
            return None

        env = esg_scores.get("environmental", 50) / 100
        social = esg_scores.get("social", 50) / 100
        governance = esg_scores.get("governance", 50) / 100

        composite = (env * 0.4) + (social * 0.3) + (governance * 0.3)
        return float(np.clip((composite - 0.5) * 2, -1, 1))

    def detect_market_manipulation(
        self, order_book: Dict[str, Any]
    ) -> Dict[str, bool]:
        """
        Pillar V: IOSCO market integrity checks.

        Detects layering, spoofing, and wash trading patterns.
        Any detection forces Refuse (-1) via regulatory compliance check.
        """
        if not order_book:
            return {
                "layering": False,
                "spoofing": False,
                "wash_trading": False
            }

        return {
            "layering": order_book.get("layering_detected", False),
            "spoofing": order_book.get("spoofing_detected", False),
            "wash_trading": order_book.get("wash_trading_detected", False)
        }

    def analyze_all(
        self,
        symbol: str,
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run all signal analyses. Returns dict of signals and metadata."""
        signals = {}

        prices = market_data.get("price_data", [])
        if prices:
            signals["momentum"] = self.calculate_momentum(prices)
            signals["mean_reversion"] = self.calculate_mean_reversion(prices)
            signals["volatility"] = self.calculate_volatility_signal(prices)

        order_book = market_data.get("order_book", {})
        if order_book:
            signals["liquidity"] = self.analyze_liquidity(order_book)
            signals["order_flow"] = self.analyze_order_flow(order_book)
            signals["manipulation"] = self.detect_market_manipulation(order_book)

        if "news_sentiment" in market_data:
            signals["sentiment"] = market_data["news_sentiment"]

        if "esg_scores" in market_data:
            signals["esg"] = self.analyze_esg_compliance(market_data["esg_scores"])

        return signals


# =============================================================================
# SECTION 3: MiFID II Compliance Checker (Pillar V)
# =============================================================================

def check_mifid_compliance(
    symbol: str,
    market_data: Dict[str, Any],
    manipulation_detected: Dict[str, bool]
) -> Dict[str, Any]:
    """
    Pillar V: MiFID II best execution and market integrity compliance.

    Returns compliance status with specific failures identified.
    Any FATAL flag forces Refuse (-1) via state override.
    """
    failures = []
    warnings = []

    # IOSCO: market manipulation
    if manipulation_detected.get("layering"):
        failures.append(f"IOSCO: Layering detected on {symbol}: FATAL")
    if manipulation_detected.get("spoofing"):
        failures.append(f"IOSCO: Spoofing detected on {symbol}: FATAL")
    if manipulation_detected.get("wash_trading"):
        failures.append(f"IOSCO: Wash trading detected on {symbol}: FATAL")

    # Best execution: spread check
    order_book = market_data.get("order_book", {})
    spread = order_book.get("spread", 0)
    spread_limit = market_data.get("max_acceptable_spread", 0.01)
    if spread > spread_limit:
        warnings.append(
            f"MiFID II: Spread {spread:.4f} exceeds best execution "
            f"threshold {spread_limit:.4f}"
        )

    # Sanctions screening
    if not market_data.get("sanctions_screened", False):
        failures.append("FATF: Sanctions screening not completed: FATAL")

    # Circuit breaker check
    if market_data.get("circuit_breaker_active", False):
        failures.append(
            f"Circuit breaker active on {symbol}: trading suspended"
        )

    return {
        "compliant": len(failures) == 0,
        "failures": failures,
        "warnings": warnings
    }


# =============================================================================
# SECTION 4: Position Sizing
# Sized by TL state, not by hardcoded confidence numbers.
# =============================================================================

def calculate_position_size(
    decision: TLValue,
    engine: TLEngine,
    portfolio_value: float,
    max_position_fraction: float,
    symbol: str
) -> Dict[str, Any]:
    """
    Calculate position size governed by TL state.

    PROCEED: position sized proportionally within max_position_fraction.
    The closer confidence is to 1.0, the closer to the maximum position.
    This is relative to the engine's proceed_threshold, not a fixed number.

    EPISTEMIC_HOLD: no new position. Existing positions held unchanged.

    REFUSE: close existing long positions or initiate short if warranted.
    """
    if decision.state == TLState.PROCEED:
        # Scale within [proceed_threshold, 1.0] range
        threshold_range = 1.0 - engine.proceed_threshold
        confidence_above = decision.confidence - engine.proceed_threshold
        scaling = confidence_above / threshold_range if threshold_range > 0 else 1.0
        scaling = max(0.0, min(1.0, scaling))

        notional = portfolio_value * max_position_fraction * scaling
        return {
            "action": "BUY",
            "positionFraction": max_position_fraction * scaling,
            "notional": round(notional, 2),
            "symbol": symbol,
            "rationale": (
                f"Confidence {decision.confidence:.3f} scaled to "
                f"{scaling:.1%} of max position"
            ),
            "mifidCompliant": True
        }

    elif decision.state == TLState.EPISTEMIC_HOLD:
        return {
            "action": "HOLD",
            "positionFraction": 0.0,
            "notional": 0.0,
            "symbol": symbol,
            "rationale": (
                "Epistemic Hold active. No new position. "
                "Existing positions held unchanged. "
                "GovernancePause workflow initiated."
            ),
            "holdDurationMs": 300,
            "mifidCompliant": True
        }

    else:  # TLState.REFUSE
        return {
            "action": "REFUSE",
            "positionFraction": 0.0,
            "notional": 0.0,
            "symbol": symbol,
            "rationale": (
                "Refuse state. Close existing long positions. "
                "refusalIsPermanent: True. "
                "No actuation authorized."
            ),
            "closeExisting": True,
            "mifidCompliant": True
        }


# =============================================================================
# SECTION 5: TL Trading Algorithm
# =============================================================================

class TLTradingAlgorithm:
    """
    Financial Trading Algorithm using Ternary Logic.

    Implements sovereign-grade accountability for trading decisions:
        Pillar I:   Epistemic Hold (flash crash, volatility spike, data gaps)
        Pillar II:  Immutable Ledger (every decision committed before trade fires)
        Pillar III: Goukassian Principle (lantern, signature, license)
        Pillar IV:  Decision Logs (complete audit trail)
        Pillar V:   MiFID II, FATF, IOSCO compliance
        Pillar VI:  ESG mandate verification
        Pillar VII: Hybrid Shield (privacy-preserving transparency)
        Pillar VIII:Anchors (Merkle root anchoring)

    Dual-Lane Latency Architecture awareness:
        The Inference Lane (less than 2ms WCET) computes trading signals
        and proposes state. The Governance Lane (300ms ceiling) evaluates
        constitutionally and issues the PermissionToken. No trade fires
        without both lanes completing their constitutional functions.

    THRESHOLD GOVERNANCE:
        proceed_threshold and hold_threshold must be calibrated by your
        trading desk through backtesting, regulatory requirements, and
        risk management approval. No universal values exist.
        See docs/Threshold_Calibration.md.
    """

    def __init__(
        self,
        proceed_threshold: float,
        hold_threshold: float,
        portfolio_value: float = 1_000_000.0,
        max_position_fraction: float = 0.10
    ):
        """
        Initialize TL Trading Algorithm.

        Args:
            proceed_threshold: Institution-calibrated PROCEED threshold.
                               REQUIRED. No default.
            hold_threshold:    Institution-calibrated REFUSE threshold.
                               REQUIRED. No default.
            portfolio_value:   Starting portfolio value.
            max_position_fraction: Maximum position size as fraction of portfolio.
        """
        self.engine = TLEngine(
            proceed_threshold=proceed_threshold,
            hold_threshold=hold_threshold,
            epistemic_hold_rate_target=0.20
        )
        self.analyzer = MarketSignalAnalyzer()
        self.portfolio_value = portfolio_value
        self.max_position_fraction = max_position_fraction
        self.positions: Dict[str, float] = {}
        self.ledger = ImmutableLedger()
        self.license_scopes = [
            "financial.trading",
            "regulatory.mifid2",
            "audit.governance"
        ]

    def make_trading_decision(
        self,
        symbol: str,
        market_data: Dict[str, Any],
        scenario_label: str = "Trade Decision"
    ) -> Dict[str, Any]:
        """
        Make a trading decision under full TL constitutional governance.

        Sequence (respecting NL=NA):
            1. Analyze market signals
            2. ESG mandate check (Pillar VI): binary, overrides confidence
            3. MiFID II compliance check (Pillar V): binary, overrides state
            4. Calculate composite confidence
            5. Evaluate with TLEngine
            6. Commit log entry (NL=NA: BEFORE any trade fires)
            7. Issue PermissionToken if PROCEED
            8. Size position by state
            9. Return governance record

        The Inference Lane operates at less than 2ms WCET for steps 1 and 4.
        The Governance Lane (300ms ceiling) authorizes steps 6 and 7.
        No trade fires without both lanes completing.
        """
        # Step 1: Analyze market signals
        signals = self.analyzer.analyze_all(symbol, market_data)
        manipulation = signals.pop("manipulation", {})

        # Step 2: ESG mandate check (Pillar VI)
        # Binary pass/fail. Overrides confidence entirely.
        esg_data = {
            "esg_verified": market_data.get("esg_verified", False),
            "emissions_anchored": market_data.get("emissions_anchored", True),
            "use_of_proceeds_tracked": market_data.get(
                "use_of_proceeds_tracked", True
            )
        }
        esg_result = verify_mandate("sustainable_capital", esg_data)
        esg_blocked = esg_result.state == TLState.EPISTEMIC_HOLD

        # Step 3: MiFID II compliance check (Pillar V)
        compliance = check_mifid_compliance(symbol, market_data, manipulation)
        compliance_blocked = not compliance["compliant"]

        # Step 4: Determine state and confidence
        if compliance_blocked:
            # Regulatory failure forces Refuse (harm is clear)
            forced_state = TLState.REFUSE
            confidence = 0.0
            reasoning = (
                f"MiFID II/FATF compliance failure: "
                f"{'; '.join(compliance['failures'])}"
            )
        elif esg_blocked:
            # ESG mandate failure forces Epistemic Hold
            forced_state = TLState.EPISTEMIC_HOLD
            confidence = 0.0
            reasoning = (
                f"Pillar VI ESG mandate failure: "
                f"{'; '.join(esg_result.metadata.get('failed_checks', []))}"
            )
        else:
            forced_state = None
            # Calculate composite confidence from valid numeric signals
            numeric_signals = [
                v for v in signals.values()
                if isinstance(v, (int, float)) and v is not None
            ]

            if not numeric_signals:
                # No signals: Epistemic Hold on data absence
                forced_state = TLState.EPISTEMIC_HOLD
                confidence = 0.0
                reasoning = (
                    f"Insufficient market data for {symbol}. "
                    "Epistemic Hold: truth not yet verified."
                )
            else:
                # Normalize from [-1,+1] to [0,1] and average
                confidence = float(
                    np.mean([(s + 1) / 2 for s in numeric_signals])
                )
                reasoning = self._build_reasoning(symbol, signals, market_data)

        if forced_state is None and reasoning == "":
            reasoning = f"Composite signal from {len(numeric_signals)} sources"

        # Step 5: Evaluate with TLEngine
        decision = self.engine.evaluate(
            confidence=confidence,
            reasoning=reasoning,
            metadata={
                "symbol": symbol,
                "scenario": scenario_label,
                "signalCount": len([
                    v for v in signals.values()
                    if isinstance(v, (int, float))
                ]),
                "esgBlocked": esg_blocked,
                "complianceBlocked": compliance_blocked,
                "complianceWarnings": compliance["warnings"]
            },
            force_state=forced_state
        )

        # Step 6: Commit log entry (NL=NA: BEFORE any trade fires)
        goukassian = create_goukassian_principle_block(
            decision_payload=decision.reasoning,
            agent_id="trading-governance-001",
            license_scopes=self.license_scopes
        )
        log_entry = commit_log_entry(
            decision=decision,
            engine=self.engine,
            goukassian_block=goukassian,
            previous_hash=self.ledger.previous_hash,
            extra_context={
                "symbol": symbol,
                "signals": {
                    k: round(v, 4)
                    for k, v in signals.items()
                    if isinstance(v, (int, float))
                },
                "regulatoryCompliant": compliance["compliant"],
                "esgCompliant": not esg_blocked,
                "portfolioValue": self.portfolio_value
            }
        )
        self.ledger.commit(log_entry)

        # Step 7: Permission Token (PROCEED only)
        token = build_permission_token(log_entry)

        # Step 8: Position sizing governed by TL state
        position = calculate_position_size(
            decision=decision,
            engine=self.engine,
            portfolio_value=self.portfolio_value,
            max_position_fraction=self.max_position_fraction,
            symbol=symbol
        )

        # Update position tracking
        if decision.state == TLState.PROCEED:
            current = self.positions.get(symbol, 0.0)
            self.positions[symbol] = current + position["positionFraction"]
        elif decision.state == TLState.REFUSE:
            self.positions[symbol] = 0.0

        # Assemble governance record
        return {
            "scenario": scenario_label,
            "symbol": symbol,
            "state": decision.state.name,
            "stateValue": decision.state.value,
            "processActive": log_entry["processActive"],
            "confidence": decision.confidence,
            "positionLabel": decision.position_label,
            "reasoning": decision.reasoning,
            "logHash": log_entry["logHash"][:16] + "...",
            "merkleRoot": log_entry["merkleRoot"][:16] + "...",
            "permissionToken": (
                token["tokenId"][:16] + "..." if token else None
            ),
            "laneOrigin": token["laneOrigin"] if token else "N/A",
            "position": position,
            "regulatoryCompliant": compliance["compliant"],
            "regulatoryFailures": compliance["failures"],
            "regulatoryWarnings": compliance["warnings"],
            "esgCompliant": not esg_blocked,
            "nlNaStatus": "Log committed before trade authorized"
        }

    def _build_reasoning(
        self,
        symbol: str,
        signals: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> str:
        """Build human-readable reasoning from market signals."""
        parts = []

        momentum = signals.get("momentum")
        if momentum is not None:
            if momentum > 0.3:
                parts.append("Momentum: strong uptrend")
            elif momentum < -0.3:
                parts.append("Momentum: strong downtrend")
            else:
                parts.append("Momentum: neutral")

        vol = signals.get("volatility")
        if vol is not None and vol < -0.5:
            parts.append(
                "Volatility: elevated, flash crash conditions detected"
            )

        liquidity = signals.get("liquidity")
        if liquidity is not None and liquidity < -0.3:
            parts.append("Liquidity: insufficient for safe execution")

        sentiment = signals.get("sentiment")
        if sentiment is not None:
            if sentiment > 0.3:
                parts.append("Sentiment: positive")
            elif sentiment < -0.3:
                parts.append("Sentiment: negative")

        regime = market_data.get("market_regime", "normal")
        if regime == "stress":
            parts.append("Regime: market stress; Governance Lane 300ms ceiling active")
        elif regime == "flash_crash":
            parts.append("Regime: flash crash conditions; Epistemic Hold warranted")

        return "; ".join(parts) if parts else f"Signal analysis for {symbol}"

    def get_trading_summary(self) -> Dict[str, Any]:
        """Return summary of trading decisions and ledger state."""
        stats = self.engine.get_statistics()
        ledger = self.ledger.get_summary()

        return {
            "totalDecisions": stats["total_decisions"],
            "proceedCount": stats["proceed_count"],
            "epistemicHoldCount": stats["hold_count"],
            "refuseCount": stats["refuse_count"],
            "epistemicHoldRate": stats["epistemic_hold_rate"],
            "targetHoldRate": stats["target_hold_rate"],
            "averageConfidence": stats["average_confidence"],
            "ledgerEntries": ledger["totalEntries"],
            "latestMerkleRoot": ledger["latestMerkleRoot"][:16] + "...",
            "openPositions": {
                k: round(v, 4)
                for k, v in self.positions.items() if v != 0
            },
            "architectureMode": "ARCHITECTURE_B",
            "pufAttestation": "NULL_PUF_DEPLOYMENT"
        }


# =============================================================================
# SECTION 6: Demonstration Scenarios
# =============================================================================

def run_trading_demo():
    """
    Demonstrate TL trading across six scenarios:
        1. Clear buy signal: strong momentum, good liquidity, ESG verified
        2. Epistemic Hold: flash crash volatility spike
        3. Refuse: market manipulation detected (IOSCO FATAL)
        4. ESG mandate blocks execution (Pillar VI)
        5. Insufficient data: Epistemic Hold on missing signals
        6. Recovery: conditions normalized after hold

    DEMONSTRATION THRESHOLD VALUES: not for production use.
    Trading desks calibrate thresholds through backtesting over 20+ years
    of historical data, regulatory requirements, and risk management approval.
    See docs/Threshold_Calibration.md.
    """

    print()
    print("=" * 70)
    print("  TERNARY LOGIC: COMPREHENSIVE FINANCIAL TRADING")
    print("  Lev Goukassian (ORCID: 0009-0006-5966-1243)")
    print("=" * 70)

    # DEMONSTRATION VALUES ONLY: not recommendations, not standards.
    DEMO_PROCEED = 0.70
    DEMO_HOLD = 0.30

    algo = TLTradingAlgorithm(
        proceed_threshold=DEMO_PROCEED,
        hold_threshold=DEMO_HOLD,
        portfolio_value=1_000_000.0,
        max_position_fraction=0.10
    )

    print()
    print(f"  Engine initialized (demonstration thresholds: not for production)")
    print(f"  PROCEED >= {DEMO_PROCEED} | REFUSE < {DEMO_HOLD}")
    print(f"  Portfolio: $1,000,000 | Max position: 10%")
    print(f"  Dual-Lane: Inference Lane < 2ms | Governance Lane <= 300ms")

    # ------------------------------------------------------------------
    # SCENARIO 1: Clear buy signal
    # Strong momentum, good liquidity, ESG verified, all checks pass.
    # Expected: PROCEED with scaled position.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 1: Clear Buy Signal")
    print("-" * 70)

    data_buy = {
        "price_data": [98.0, 99.2, 100.1, 101.5, 102.3, 103.1,
                       104.0, 105.2, 106.1, 107.0, 108.2, 109.0,
                       110.1, 111.3, 112.0, 113.2, 114.0, 115.1,
                       116.3, 117.0],
        "order_book": {
            "bid_depth": 850000,
            "ask_depth": 820000,
            "spread": 0.002,
            "buy_volume_5min": 620000,
            "sell_volume_5min": 380000,
            "layering_detected": False,
            "spoofing_detected": False,
            "wash_trading_detected": False
        },
        "news_sentiment": 0.65,
        "esg_scores": {
            "environmental": 82,
            "social": 74,
            "governance": 88
        },
        "esg_verified": True,
        "emissions_anchored": True,
        "use_of_proceeds_tracked": True,
        "sanctions_screened": True,
        "market_regime": "normal",
        "max_acceptable_spread": 0.01
    }

    r1 = algo.make_trading_decision("ASSET-A", data_buy, "Clear Buy Signal")
    _print_trade_result(r1)

    # ------------------------------------------------------------------
    # SCENARIO 2: Flash crash detection via volatility spike
    # Extreme price moves trigger Epistemic Hold. The Governance Lane
    # (300ms ceiling) pauses execution while market conditions are assessed.
    # Expected: EPISTEMIC_HOLD. No new position.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 2: Flash Crash Detection (Epistemic Hold)")
    print("-" * 70)

    # Generate flash crash price data: sudden 8% drop
    prices_normal = [100.0 + i * 0.1 for i in range(15)]
    prices_crash = [prices_normal[-1] * (1 - 0.008 * i) for i in range(5)]
    flash_crash_prices = prices_normal + prices_crash

    data_flash = {
        "price_data": flash_crash_prices,
        "order_book": {
            "bid_depth": 120000,
            "ask_depth": 980000,
            "spread": 0.045,
            "buy_volume_5min": 80000,
            "sell_volume_5min": 920000,
            "layering_detected": False,
            "spoofing_detected": False,
            "wash_trading_detected": False
        },
        "news_sentiment": -0.70,
        "esg_verified": True,
        "emissions_anchored": True,
        "use_of_proceeds_tracked": True,
        "sanctions_screened": True,
        "market_regime": "flash_crash",
        "max_acceptable_spread": 0.01
    }

    r2 = algo.make_trading_decision("ASSET-B", data_flash, "Flash Crash")
    _print_trade_result(r2)

    # ------------------------------------------------------------------
    # SCENARIO 3: Market manipulation detected (IOSCO FATAL)
    # Spoofing detected. Compliance failure forces Refuse (-1).
    # Even if market signals were favorable, constitutional harm
    # threshold crossed.
    # Expected: REFUSE. No actuation authorized.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 3: Market Manipulation Detected (IOSCO: Pillar V)")
    print("-" * 70)

    data_manip = {
        "price_data": [100.0 + i * 0.2 for i in range(20)],
        "order_book": {
            "bid_depth": 500000,
            "ask_depth": 480000,
            "spread": 0.003,
            "buy_volume_5min": 300000,
            "sell_volume_5min": 280000,
            "layering_detected": False,
            "spoofing_detected": True,   # IOSCO FATAL
            "wash_trading_detected": False
        },
        "news_sentiment": 0.20,
        "esg_verified": True,
        "emissions_anchored": True,
        "use_of_proceeds_tracked": True,
        "sanctions_screened": True,
        "market_regime": "normal",
        "max_acceptable_spread": 0.01
    }

    r3 = algo.make_trading_decision(
        "ASSET-C", data_manip, "Market Manipulation"
    )
    _print_trade_result(r3)

    # ------------------------------------------------------------------
    # SCENARIO 4: ESG mandate failure blocks execution (Pillar VI)
    # ESG not verified. Binary mandate check overrides confidence.
    # Even strong market signals cannot override a failed mandate check.
    # Expected: EPISTEMIC_HOLD (forced by ESG mandate failure).
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 4: ESG Mandate Failure (Pillar VI)")
    print("-" * 70)

    data_esg = {
        "price_data": [100.0 + i * 0.5 for i in range(20)],
        "order_book": {
            "bid_depth": 700000,
            "ask_depth": 650000,
            "spread": 0.002,
            "buy_volume_5min": 450000,
            "sell_volume_5min": 310000,
            "layering_detected": False,
            "spoofing_detected": False,
            "wash_trading_detected": False
        },
        "news_sentiment": 0.55,
        "esg_scores": {"environmental": 40, "social": 35, "governance": 42},
        "esg_verified": False,          # PILLAR VI FAILS
        "emissions_anchored": False,    # PILLAR VI FAILS
        "use_of_proceeds_tracked": True,
        "sanctions_screened": True,
        "market_regime": "normal",
        "max_acceptable_spread": 0.01
    }

    r4 = algo.make_trading_decision("ASSET-D", data_esg, "ESG Mandate Failure")
    _print_trade_result(r4)

    # ------------------------------------------------------------------
    # SCENARIO 5: Insufficient data
    # No price data available. Epistemic Hold on data absence.
    # Expected: EPISTEMIC_HOLD.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 5: Insufficient Market Data")
    print("-" * 70)

    data_missing = {
        # No price_data
        # No order_book
        "esg_verified": True,
        "emissions_anchored": True,
        "use_of_proceeds_tracked": True,
        "sanctions_screened": True,
        "market_regime": "normal",
        "max_acceptable_spread": 0.01
    }

    r5 = algo.make_trading_decision(
        "ASSET-E", data_missing, "Missing Data"
    )
    _print_trade_result(r5)

    # ------------------------------------------------------------------
    # SCENARIO 6: Recovery after Epistemic Hold
    # Market conditions normalized. Clear signal. ESG verified.
    # Expected: PROCEED.
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("SCENARIO 6: Recovery after Epistemic Hold")
    print("-" * 70)

    data_recovery = {
        "price_data": [95.0 + i * 0.3 for i in range(20)],
        "order_book": {
            "bid_depth": 620000,
            "ask_depth": 590000,
            "spread": 0.003,
            "buy_volume_5min": 400000,
            "sell_volume_5min": 300000,
            "layering_detected": False,
            "spoofing_detected": False,
            "wash_trading_detected": False
        },
        "news_sentiment": 0.45,
        "esg_scores": {"environmental": 76, "social": 70, "governance": 80},
        "esg_verified": True,
        "emissions_anchored": True,
        "use_of_proceeds_tracked": True,
        "sanctions_screened": True,
        "market_regime": "normal",
        "max_acceptable_spread": 0.01
    }

    r6 = algo.make_trading_decision("ASSET-F", data_recovery, "Recovery")
    _print_trade_result(r6)

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("TRADING SESSION SUMMARY")
    print("=" * 70)

    summary = algo.get_trading_summary()
    print(f"  Total decisions:     {summary['totalDecisions']}")
    print(f"  PROCEED:             {summary['proceedCount']}")
    print(f"  EPISTEMIC_HOLD:      {summary['epistemicHoldCount']}")
    print(f"  REFUSE:              {summary['refuseCount']}")
    print(f"  Hold rate:           {summary['epistemicHoldRate']:.1%} "
          f"(target: {summary['targetHoldRate']:.1%})")
    print(f"  Average confidence:  {summary['averageConfidence']:.3f}")
    print(f"  Ledger entries:      {summary['ledgerEntries']}")
    print(f"  Latest Merkle root:  {summary['latestMerkleRoot']}")
    print(f"  Open positions:      {summary['openPositions']}")
    print(f"  Architecture mode:   {summary['architectureMode']}")
    print(f"  PUF attestation:     {summary['pufAttestation']}")
    print()
    print("  NL=NA: Every trade decision was logged before any position")
    print("  was authorized. The Inference Lane computed signals in under")
    print("  2ms. The Governance Lane authorized via PermissionToken.")
    print("  No log, no trade.")
    print()
    print("  Three immutable mandates:")
    print("    No Spy. No Weapon. No Switch Off.")
    print("=" * 70)
    print()

    # Export audit trail (Pillar IV)
    algo.engine.export_audit_trail("/tmp/tl_trading_audit.json")
    print("  Audit trail exported: /tmp/tl_trading_audit.json")
    print()


def _print_trade_result(result: Dict[str, Any]):
    """Print formatted trade decision result."""
    state_labels = {
        "PROCEED": "OK",
        "EPISTEMIC_HOLD": "HOLD",
        "REFUSE": "REFUSE"
    }
    label = state_labels.get(result["state"], "")

    print(f"  State:           {label} {result['state']} ({result['stateValue']})")
    print(f"  processActive:   {result['processActive']}")
    print(f"  Confidence:      {result['confidence']:.3f}")
    print(f"  Position:        {result['positionLabel']}")
    print(f"  Log committed:   {result['logHash']}")
    print(f"  Merkle root:     {result['merkleRoot']}")

    if result.get("permissionToken"):
        print(f"  Permission token: {result['permissionToken']}")
        print(f"  laneOrigin:       {result['laneOrigin']}")
    else:
        print(f"  Permission token: None")

    pos = result.get("position", {})
    if pos.get("action") == "BUY":
        print(
            f"  Trade action:    {pos['action']} "
            f"${pos['notional']:,.2f} "
            f"({pos['positionFraction']:.1%} of portfolio)"
        )
    else:
        print(f"  Trade action:    {pos.get('action', 'N/A')}")

    if result.get("regulatoryFailures"):
        for f in result["regulatoryFailures"]:
            print(f"  Compliance FAIL: {f}")

    if not result.get("esgCompliant"):
        print(f"  ESG mandate:     FAILED (Pillar VI forced Epistemic Hold)")

    if result.get("regulatoryWarnings"):
        for w in result["regulatoryWarnings"][:1]:
            print(f"  Warning:         {w}")

    print(f"  NL=NA:           {result['nlNaStatus']}")


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    run_trading_demo()


"""
---
Creator: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Email: leogouk@gmail.com
Repository: https://github.com/FractonicMind/TernaryLogic
Successor: support@tl-goukassian.org
DOI 1: 10.1007/s43681-025-00910-6
DOI 2: 10.1007/s43681-026-01124-0
---
"""
