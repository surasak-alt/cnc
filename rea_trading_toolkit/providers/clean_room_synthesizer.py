# -*- coding: utf-8 -*-
"""
Clean-Room Synthesizer Provider (Phase 3 of Trading REA - 2026-2036 Architecture)
Takes Phase 2 Verified Evidence Bundle and synthesizes the optimal Counter-Order:
- Blocks execution if Truth Gate or Red Team Veto triggers
- Entry at 50% FVG Consequent Encroachment (Equilibrium)
- Hard SL strictly beyond max(entry, swing) + Empirical P95 Buffer + Red Team Buffer
- Enforces minimum broker safe stop distance (prevents Error 10016 & 2-point SL bug)
- Strict Capital Risk: $100 (Standard) or 10,000 Cents (Cent)
"""

import uuid
from typing import Optional
import numpy as np
from contracts.market_ast import MarketAST
from contracts.evidence_bundle import TradingEvidenceBundle
from contracts.execution_order import CleanRoomOrder
from providers.broker_blindspot_engine import BrokerBlindspotEngine


class CleanRoomSynthesizer:
    def __init__(self, symbol: str = "XAUUSD"):
        self.symbol = symbol
        self.broker_engine = BrokerBlindspotEngine(symbol)

    def synthesize_order(
        self,
        ast: MarketAST,
        evidence: TradingEvidenceBundle,
        account_type: str = "STANDARD",
        risk_percent: float = 1.0
    ) -> Optional[CleanRoomOrder]:
        """
        Synthesizes a clean-room execution order ONLY if Truth Gate, Red Team,
        and Monte Carlo stress tests approve the setup.
        """
        # 1. Deterministic Gatekeeper Assertions
        if not evidence.truth_gate_audit.is_verified_zero_hallucination:
            return None
        if evidence.red_team_critique.veto_triggered:
            return None
        if evidence.verdict == "REJECT_RISK_EXCEEDED":
            return None

        # 2. Base Capital Standards (Strict Rule: $100 Standard or 10,000 Cents)
        if account_type.upper() == "CENT":
            base_capital = 10000.0  # Cents
            risk_money = base_capital * (risk_percent / 100.0)  # e.g. 100 Cents
        else:
            base_capital = 100.0    # Dollars
            risk_money = base_capital * (risk_percent / 100.0)  # e.g. $1.00

        broker_audit = self.broker_engine.audit_broker_rules()
        asym = broker_audit["asymmetric_bid_ask_compensation"]
        min_broker_sl = max(float(broker_audit["min_safe_sl_distance"]), 1.20)

        # 3. Empirical P95 Stop-Hunt Buffer + Red Team Adjustment
        atr = max(ast.atr_14, 0.80)
        emp_p95_mult = ast.empirical_distribution.p95_safe_sl_atr + evidence.red_team_critique.recommended_sl_adjustment_atr
        p95_buffer_dist = round(max(emp_p95_mult * atr, min_broker_sl), 2)

        bullish_fvgs = [f for f in ast.active_fvgs if f.gap_type == "BULLISH_FVG"]
        bearish_fvgs = [f for f in ast.active_fvgs if f.gap_type == "BEARISH_FVG"]

        sweep_findings = [f for f in evidence.findings if "STOP_HUNT" in f.category]
        is_buy_side_sweep = any("BUY_SIDE" in f.metric_name for f in sweep_findings)

        swing_highs = [p.price for p in ast.swing_points if p.kind == "SWING_HIGH"]
        swing_lows = [p.price for p in ast.swing_points if p.kind == "SWING_LOW"]

        if is_buy_side_sweep or (bearish_fvgs and not bullish_fvgs):
            # SELL_LIMIT Sniper Fade
            action = "SELL_LIMIT"
            raw_entry = bearish_fvgs[-1].equilibrium_ce if bearish_fvgs else round(ast.current_bid + (0.15 * atr), 2)
            # Ensure SELL_LIMIT is placed at or above current_bid
            entry = round(max(raw_entry, ast.current_bid), 2)

            # Anchor SL strictly above max(entry, recent_swing_high) + P95 buffer + Spread retreat
            anchor_high = max([entry, ast.current_ask] + (swing_highs[-3:] if swing_highs else [entry]))
            hard_sl = round(anchor_high + p95_buffer_dist + asym["sell_sl_retreat_buffer"], 2)

            sl_dist = max(abs(hard_sl - entry), min_broker_sl)
            hard_tp = round(entry - (sl_dist * 2.25), 2)
        else:
            # BUY_LIMIT Sniper Fade
            action = "BUY_LIMIT"
            raw_entry = bullish_fvgs[-1].equilibrium_ce if bullish_fvgs else round(ast.current_ask - (0.15 * atr), 2)
            # Ensure BUY_LIMIT is placed at or below current_ask, plus Ask lift buffer
            entry = round(min(raw_entry + asym["buy_limit_lift_buffer"], ast.current_ask), 2)

            # Anchor SL strictly below min(entry, recent_swing_low) - P95 buffer
            anchor_low = min([entry, ast.current_bid] + (swing_lows[-3:] if swing_lows else [entry]))
            hard_sl = round(anchor_low - p95_buffer_dist, 2)

            sl_dist = max(abs(entry - hard_sl), min_broker_sl)
            hard_tp = round(entry + (sl_dist * 2.25), 2)

        # 4. Calculate Lot Size strictly by Risk Amount and SL Distance
        sl_price_distance = max(abs(entry - hard_sl), min_broker_sl)
        # For XAUUSD (100 oz contract): 0.01 lot moving $1.00 = $1.00 (or 100 Cents on Cent account)
        raw_lot = (risk_money / max(sl_price_distance * 100.0, 1.0)) * 0.01
        lot_size = round(float(np.clip(raw_lot, 0.01, 1.0)), 2)

        rr_ratio = round(abs(hard_tp - entry) / max(abs(entry - hard_sl), 0.01), 2)
        order_id = f"REA-ORD-{uuid.uuid4().hex[:6].upper()}"

        return CleanRoomOrder(
            order_id=order_id,
            symbol=self.symbol,
            action=action,
            entry_price=round(entry, 2),
            hard_sl=round(hard_sl, 2),
            hard_tp=round(hard_tp, 2),
            lot_size=lot_size,
            risk_percent=risk_percent,
            risk_amount_money=round(risk_money, 2),
            account_type=account_type.upper(),
            base_capital=base_capital,
            spread_compensation_ticks=asym["buy_limit_lift_buffer"] if action == "BUY_LIMIT" else asym["sell_sl_retreat_buffer"],
            stop_hunt_sl_buffer_atr=round(emp_p95_mult, 3),
            zero_ping_server_side=True,
            evidence_bundle_ref=evidence.bundle_id,
            risk_reward_ratio=rr_ratio,
            notes=(
                f"Synthesized from {evidence.algo_footprint.algo_type} | "
                f"Confidence: {round(evidence.confidence_score*100, 1)}% | "
                f"MC 1000-Path EV: +{evidence.monte_carlo_audit.expected_value_r}R"
            )
        )
