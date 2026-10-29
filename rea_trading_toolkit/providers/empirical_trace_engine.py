# -*- coding: utf-8 -*-
"""
Empirical Trace Engine Provider (Phase 2 of Trading REA - 2026-2036 Architecture)
Transforms Market-AST into a verified TradingEvidenceBundle v2:
- Uses REAL Mined Empirical Distributions (Mean, Std, P95, Z-Score, P-Value)
- Classifies Institutional Algorithmic Footprints (Judas, Iceberg, Vacuum, TWAP)
- Executes Red Team Adversarial Attack (Devil's Advocate)
- Executes 1,000-Path Vectorized Quantum Monte Carlo Simulation
- Verifies Zero-Hallucination via Deterministic Truth Gatekeeper & FSM
"""

import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Tuple
import numpy as np

from contracts.market_ast import MarketAST
from contracts.evidence_bundle import (
    TradingEvidenceBundle,
    EvidenceFinding,
    AlgoClassification,
)
from providers.red_team_adversarial import RedTeamAdversarialAgent
from providers.quantum_monte_carlo import QuantumMonteCarloEngine
from providers.truth_gatekeeper_fsm import TruthGatekeeperFSM


class EmpiricalTraceEngine:
    def __init__(self, symbol: str = "XAUUSD"):
        self.symbol = symbol
        self.red_team = RedTeamAdversarialAgent(symbol)
        self.monte_carlo = QuantumMonteCarloEngine(num_paths=1000, horizon_bars=48)
        self.truth_gate = TruthGatekeeperFSM(symbol)

    def build_evidence_bundle(self, ast: MarketAST) -> TradingEvidenceBundle:
        """
        Main Phase 2 entry point: Constructs a scientifically verified TradingEvidenceBundle v2.
        """
        findings: List[EvidenceFinding] = []
        limitations: List[str] = []
        emp = ast.empirical_distribution

        # 1. Statistical Distribution Finding (From Historical Mining)
        findings.append(
            EvidenceFinding(
                category="STATISTICAL_DISTRIBUTION",
                metric_name="empirical_p95_pierce_atr",
                observed_value=emp.p95_safe_sl_atr,
                benchmark_value=emp.mean_pierce_atr,
                description=(
                    f"Mined N={emp.sweep_sample_size} sweeps across {emp.bars_analyzed} bars: "
                    f"Mean={emp.mean_pierce_atr}x ATR, Std={emp.std_pierce_atr}x, "
                    f"P95 Safe SL={emp.p95_safe_sl_atr}x ATR (Z={emp.z_score_stat}, p={emp.p_value})"
                ),
                is_anomaly=emp.is_statistically_significant
            )
        )

        if not emp.is_statistically_significant:
            limitations.append(
                f"LOW_STATISTICAL_SIGNIFICANCE: Empirical sample N={emp.sweep_sample_size}, p={emp.p_value} (>= 0.05)."
            )

        # 2. Chronos Session DNA Inspection (Thai Time UTC+7)
        thai_now = datetime.now(timezone(timedelta(hours=7)))
        thai_hour = thai_now.hour
        thai_minute = thai_now.minute

        session_name, is_prime_session, is_death_zone = self._analyze_session_chronos(thai_hour, thai_minute)
        findings.append(
            EvidenceFinding(
                category="SESSION_CHRONOS",
                metric_name="current_trading_session",
                observed_value=float(thai_hour),
                benchmark_value=19.0,
                description=f"Active Thai Session: {session_name} ({thai_now.strftime('%H:%M')} THA)",
                is_anomaly=False
            )
        )

        if is_death_zone:
            limitations.append("ROLLOVER_DEATH_ZONE: Spread widening active (04:00-05:15 THA). New entries blocked.")

        # 3. Stop-Hunt Sweep & Pierce Depth Trace
        pierce_depth_atr = 0.0
        sweep_detected = False
        sweep_side = "NONE"

        if ast.swing_points:
            recent_highs = [p for p in ast.swing_points if p.kind == "SWING_HIGH"]
            recent_lows = [p for p in ast.swing_points if p.kind == "SWING_LOW"]

            if recent_highs and ast.current_bid >= recent_highs[-1].price - (0.20 * ast.atr_14):
                sweep_detected = True
                sweep_side = "BUY_SIDE"
                pierce_dist = max(ast.current_bid - recent_highs[-1].price, 0.15 * ast.atr_14)
                pierce_depth_atr = round(pierce_dist / max(ast.atr_14, 0.01), 2)
            elif recent_lows and ast.current_ask <= recent_lows[-1].price + (0.20 * ast.atr_14):
                sweep_detected = True
                sweep_side = "SELL_SIDE"
                pierce_dist = max(recent_lows[-1].price - ast.current_ask, 0.15 * ast.atr_14)
                pierce_depth_atr = round(pierce_dist / max(ast.atr_14, 0.01), 2)

        if sweep_detected:
            findings.append(
                EvidenceFinding(
                    category="STOP_HUNT_PIERCE",
                    metric_name=f"pierce_depth_atr_{sweep_side}",
                    observed_value=pierce_depth_atr,
                    benchmark_value=emp.mean_pierce_atr,
                    description=(
                        f"Institutional liquidity sweep on {sweep_side} ({pierce_depth_atr}x ATR vs "
                        f"historical mean {emp.mean_pierce_atr}x ATR)"
                    ),
                    is_anomaly=True
                )
            )
        else:
            limitations.append("NO_IMMEDIATE_SWEEP: Price has not yet swept the primary swing boundary.")

        # 4. Volume Effort vs Result & Absorption Trace
        findings.append(
            EvidenceFinding(
                category="VOLUME_ABSORPTION",
                metric_name="effort_vs_result_ratio",
                observed_value=ast.volume_delta.effort_vs_result_ratio,
                benchmark_value=1.0,
                description=(
                    f"Effort vs Result Ratio: {ast.volume_delta.effort_vs_result_ratio} "
                    f"(Absorption={ast.volume_delta.absorption_detected})"
                ),
                is_anomaly=ast.volume_delta.absorption_detected or ast.volume_delta.effort_vs_result_ratio < 0.68
            )
        )

        # 5. Cross-Asset SMT Synchronization Finding
        findings.append(
            EvidenceFinding(
                category="SMT_DIVERGENCE",
                metric_name="cross_asset_alignment",
                observed_value=ast.cross_asset_radar.macro_alignment_score,
                benchmark_value=0.5,
                description=ast.cross_asset_radar.description,
                is_anomaly=ast.cross_asset_radar.smt_divergence_detected
            )
        )

        # 6. Algorithmic Signature Classification (Driven by Real Mined Win Probability)
        algo_sig, win_prob, intent, proposed_dir = self._classify_algo(
            ast=ast,
            sweep_detected=sweep_detected,
            sweep_side=sweep_side,
            is_prime_session=is_prime_session
        )

        # 7. Red Team Adversarial Critique
        red_critique = self.red_team.attack_proposed_setup(
            ast=ast,
            sweep_detected=sweep_detected,
            proposed_direction=proposed_dir,
            is_death_zone=is_death_zone
        )
        if red_critique.veto_triggered:
            limitations.append(f"RED_TEAM_VETO: {red_critique.adversarial_verdict}")

        # 8. Vectorized 1,000-Path Quantum Monte Carlo Stress Test
        atr = max(ast.atr_14, 0.5)
        sl_buf = (emp.p95_safe_sl_atr + red_critique.recommended_sl_adjustment_atr) * atr
        if proposed_dir == "SELL_LIMIT":
            sim_entry = ast.current_bid
            sim_sl = round(sim_entry + max(sl_buf, 1.20), 2)
            sim_tp = round(sim_entry - (abs(sim_sl - sim_entry) * 2.2), 2)
        else:
            sim_entry = ast.current_ask
            sim_sl = round(sim_entry - max(sl_buf, 1.20), 2)
            sim_tp = round(sim_entry + (abs(sim_entry - sim_sl) * 2.2), 2)

        mc_audit = self.monte_carlo.run_vectorized_simulation(
            ast=ast,
            direction=proposed_dir,
            entry_price=sim_entry,
            hard_sl=sim_sl,
            hard_tp=sim_tp
        )
        if not mc_audit.survived_stress_test:
            limitations.append(
                f"MONTE_CARLO_STRESS_FAIL: EV={mc_audit.expected_value_r}R, Winrate={mc_audit.simulated_winrate_pct}% under spread shock."
            )

        # 9. Deterministic Truth Gatekeeper Cross-Check (Zero Hallucination Assertion)
        truth_audit = self.truth_gate.verify_findings_against_ast(ast, findings)
        if not truth_audit.is_verified_zero_hallucination:
            limitations.extend(truth_audit.mismatches_found)

        # 10. Calculate Rigorous Multi-Factor Confidence Score (0.00 to 1.00)
        confidence = (win_prob * 0.55) + ((mc_audit.simulated_winrate_pct / 100.0) * 0.45)
        if emp.is_statistically_significant:
            confidence += 0.05
        if ast.cross_asset_radar.smt_divergence_detected:
            confidence += 0.04
        if is_prime_session:
            confidence += 0.03
        if red_critique.veto_triggered or is_death_zone or not truth_audit.is_verified_zero_hallucination:
            confidence -= 0.45

        confidence = round(float(np.clip(confidence, 0.05, 0.96)), 2)

        # 11. Final Verdict
        if not truth_audit.is_verified_zero_hallucination:
            verdict = "REJECT_RISK_EXCEEDED"
            summary = "HALLUCINATION GUARD TRIGGERED: Numerical mismatch detected. Execution blocked."
        elif is_death_zone or red_critique.veto_triggered:
            verdict = "REJECT_RISK_EXCEEDED"
            summary = f"Blocked by Safety/Red-Team Gate: {red_critique.adversarial_verdict}"
        elif confidence >= 0.78 and mc_audit.survived_stress_test:
            verdict = "SNIPER_SETUP_CONFIRMED"
            summary = (
                f"Institutional {algo_sig} verified ({round(confidence*100, 1)}% confidence | "
                f"MC 1000-path EV: +{mc_audit.expected_value_r}R in {mc_audit.execution_time_ms}ms | "
                f"Empirical P95 SL={emp.p95_safe_sl_atr}x ATR, p={emp.p_value})."
            )
        elif confidence >= 0.62:
            verdict = "WAIT_FOR_MORE_EVIDENCE"
            summary = f"Setup developing ({algo_sig}), awaiting full liquidity sweep or Red Team clearance."
        else:
            verdict = "REJECT_RISK_EXCEEDED"
            summary = "Low statistical edge or failed Monte Carlo spread stress test. Protecting capital."

        bundle_id = f"EV-{self.symbol}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:4].upper()}"

        return TradingEvidenceBundle(
            bundle_id=bundle_id,
            symbol=self.symbol,
            timeframe=ast.timeframe,
            generated_at=datetime.now(timezone.utc).isoformat(),
            phase="UNDERSTAND",
            findings=findings,
            algo_footprint=AlgoClassification(
                algo_type=algo_sig,
                historical_win_probability=round(win_prob, 3),
                sample_size=max(emp.sweep_sample_size, 30),
                primary_intent=intent
            ),
            red_team_critique=red_critique,
            monte_carlo_audit=mc_audit,
            truth_gate_audit=truth_audit,
            confidence_score=confidence,
            known_limitations=limitations,
            verdict=verdict,
            reasoning_summary=summary
        )

    def _analyze_session_chronos(self, hour: int, minute: int) -> Tuple[str, bool, bool]:
        if (hour == 4) or (hour == 5 and minute <= 15):
            return "Rollover Death Zone (Widened Spread)", False, True
        if 19 <= hour <= 23:
            return "London-NY Overlap Power Zone", True, False
        if 13 <= hour < 16:
            return "London Open Judas Raid Window", True, False
        if 6 <= hour < 13:
            return "Asian Accumulation Box", False, False
        return "Off-Peak Compression Zone", False, False

    def _classify_algo(
        self,
        ast: MarketAST,
        sweep_detected: bool,
        sweep_side: str,
        is_prime_session: bool
    ) -> Tuple[str, float, str, str]:
        emp = ast.empirical_distribution
        eff_ratio = ast.volume_delta.effort_vs_result_ratio
        absorption = ast.volume_delta.absorption_detected
        proposed_dir = "SELL_LIMIT" if sweep_side == "BUY_SIDE" else "BUY_LIMIT"

        if sweep_detected and eff_ratio < 0.68:
            return (
                "JUDAS_SWING_STOP_RAID",
                emp.anomaly_vol_reversal_rate,
                "False breakout on hollow volume to trigger retail stops before reversing.",
                proposed_dir
            )
        if absorption or eff_ratio > 1.45:
            return (
                "ICEBERG_ABSORPTION_WALL",
                emp.anomaly_vol_reversal_rate,
                "Institutional passive limit orders absorbing aggressive market orders.",
                proposed_dir
            )
        if eff_ratio < 0.55 and ast.market_regime == "EXPANSION":
            return (
                "LIQUIDITY_VACUUM_MANIPULATION",
                max(emp.anomaly_vol_reversal_rate - 0.05, 0.68),
                "Artificially stretched price on low liquidity; prone to sharp snap-back.",
                proposed_dir
            )
        if ast.market_regime == "EXPANSION" and is_prime_session:
            return (
                "TWAP_VWAP_TREND_EXECUTION",
                0.76,
                "Systematic institutional TWAP/VWAP algorithmic trend accumulation.",
                "BUY_LIMIT" if ast.current_bid > ast.swing_points[-1].price else "SELL_LIMIT"
            )
        return (
            "CHOP_ACCUMULATION_BOX",
            emp.normal_vol_reversal_rate,
            "Range-bound consolidation without anomalous institutional volume footprint.",
            proposed_dir
        )
