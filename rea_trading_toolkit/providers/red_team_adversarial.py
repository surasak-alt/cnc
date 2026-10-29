# -*- coding: utf-8 -*-
"""
Red Team Adversarial Agent Provider (2026-2036 Ideal Architecture)
Simulates an Institutional Market Maker attempting to hunt and destroy
our proposed trade setup before a single cent is risked.
"""

from typing import List
from contracts.market_ast import MarketAST
from contracts.evidence_bundle import RedTeamCritique


class RedTeamAdversarialAgent:
    def __init__(self, symbol: str = "XAUUSD"):
        self.symbol = symbol

    def attack_proposed_setup(
        self,
        ast: MarketAST,
        sweep_detected: bool,
        proposed_direction: str,
        is_death_zone: bool
    ) -> RedTeamCritique:
        """
        Challenges the trade setup from an adversarial Market Maker perspective.
        """
        attacks: List[str] = []
        vulnerability = 0.10
        extra_sl_buffer_atr = 0.0
        veto = False

        # Attack Vector 1: Rollover / Spread Toxicity
        spread_to_atr = ast.spread_ticks / max(ast.atr_14, 0.05)
        if is_death_zone or spread_to_atr > 0.35:
            attacks.append(
                f"SPREAD_TOXICITY_TRAP: Spread is {round(spread_to_atr*100, 1)}% of ATR. Broker spread widening will trigger SL prematurely."
            )
            vulnerability += 0.45
            veto = True

        # Attack Vector 2: Unswept High-Density Liquidity Pool Behind Our Back
        high_density_bsl = [p for p in ast.liquidity_pools if p.pool_type == "BUY_SIDE_LIQUIDITY" and p.estimated_stop_density in ("HIGH", "INSANE")]
        high_density_ssl = [p for p in ast.liquidity_pools if p.pool_type == "SELL_SIDE_LIQUIDITY" and p.estimated_stop_density in ("HIGH", "INSANE")]

        if "SELL" in proposed_direction.upper() and high_density_bsl and not sweep_detected:
            top_pool = max(p.level for p in high_density_bsl)
            if abs(top_pool - ast.current_bid) < 0.90 * ast.atr_14:
                attacks.append(
                    f"BAIT_LIQUIDITY_ABOVE: Unswept high-density Buy-Side Liquidity pool sits at {top_pool}. "
                    "Institutional algos will likely raid that pool before dropping."
                )
                vulnerability += 0.25
                extra_sl_buffer_atr = 0.22

        if "BUY" in proposed_direction.upper() and high_density_ssl and not sweep_detected:
            bot_pool = min(p.level for p in high_density_ssl)
            if abs(ast.current_ask - bot_pool) < 0.90 * ast.atr_14:
                attacks.append(
                    f"BAIT_LIQUIDITY_BELOW: Unswept high-density Sell-Side Liquidity pool sits at {bot_pool}. "
                    "Institutional algos will likely sweep below that level first."
                )
                vulnerability += 0.25
                extra_sl_buffer_atr = 0.22

        # Attack Vector 3: Fading Real Volume Momentum (No Vacuum / No Absorption)
        eff_ratio = ast.volume_delta.effort_vs_result_ratio
        if 0.72 <= eff_ratio <= 1.35 and not ast.volume_delta.absorption_detected:
            attacks.append(
                f"GENUINE_FLOW_WARNING: Effort/Result ratio ({eff_ratio}) shows balanced volume backing the move, not a hollow fakeout."
            )
            vulnerability += 0.20

        # Attack Vector 4: Statistical Significance Audit
        emp = ast.empirical_distribution
        if not emp.is_statistically_significant:
            attacks.append(
                f"LOW_STATISTICAL_POWER: Sample size N={emp.sweep_sample_size}, p-value={emp.p_value} does not pass p < 0.05 threshold."
            )
            vulnerability += 0.20

        vulnerability = round(min(vulnerability, 1.0), 2)
        if vulnerability >= 0.65:
            veto = True

        if veto:
            verdict = f"RED_TEAM_VETO (Vulnerability {int(vulnerability*100)}%): Setup rejected due to fatal institutional trap risk."
        elif extra_sl_buffer_atr > 0:
            verdict = f"SURVIVED_WITH_MODIFICATION (Vulnerability {int(vulnerability*100)}%): Widen SL buffer by +{extra_sl_buffer_atr}x ATR."
        else:
            verdict = f"CLEAN_SNIPER_PASS (Vulnerability {int(vulnerability*100)}%): Setup is resilient against institutional stop-hunting."

        return RedTeamCritique(
            attack_vectors=attacks,
            vulnerability_score=vulnerability,
            recommended_sl_adjustment_atr=extra_sl_buffer_atr,
            veto_triggered=veto,
            adversarial_verdict=verdict
        )
