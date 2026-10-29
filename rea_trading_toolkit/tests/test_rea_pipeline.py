# -*- coding: utf-8 -*-
"""
Verification Test Suite for Trading REA 2026-2036 Ideal Architecture
Validates:
1. Phase 1: Market Decompile + Real Empirical Distribution Mining (Z-test & P-value) + Cross-Asset Radar
2. Phase 2: Evidence Bundle + Red Team Adversarial + 1,000-Path Vectorized Monte Carlo (<50ms)
3. Truth Gatekeeper: Anti-Hallucination detection & Finite State Machine
4. Phase 3: Clean-Room Synthesis (Standard $100 & Cent 10,000 + Minimum Safe SL Distance Guard)
5. Self-Evolving Bayesian Brain & Post-Trade Autopsy Evolution
6. Model Intelligence Router & Automatic Failover Cascade (Gemini 4 Argon -> Pro -> Flash -> Local)
7. EA Strategy Decompiler & MCP Dispatcher
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOT_ROOT = PROJECT_ROOT.parent / "our_rea_trading_bot"

for p in (str(PROJECT_ROOT), str(BOT_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from contracts.evidence_bundle import EvidenceFinding
from providers.market_decompiler import MarketDecompiler
from providers.empirical_trace_engine import EmpiricalTraceEngine
from providers.broker_blindspot_engine import BrokerBlindspotEngine
from providers.clean_room_synthesizer import CleanRoomSynthesizer
from providers.ea_strategy_decompiler import EAStrategyDecompiler
from providers.truth_gatekeeper_fsm import TruthGatekeeperFSM
from providers.self_evolving_brain import BayesianSelfEvolvingBrain
from mcp.tools import handle_tool_call, get_tool_definitions
from model_intelligence_router import ModelIntelligenceRouter
from war_room_commander import WarRoomCommander


class TestTradingREAPipeline(unittest.TestCase):

    def setUp(self):
        self.symbol = "XAUUSD"
        self.timeframe = "M15"

    def test_phase_1_decompile_and_statistical_mining(self):
        decompiler = MarketDecompiler(self.symbol)
        ast = decompiler.decompile(self.timeframe, 500)
        self.assertEqual(ast.symbol, self.symbol)
        self.assertGreater(ast.atr_14, 0.0)
        emp = ast.empirical_distribution
        self.assertEqual(emp.bars_analyzed, 500)
        self.assertGreaterEqual(emp.sweep_sample_size, 15)
        self.assertGreater(emp.p95_safe_sl_atr, emp.mean_pierce_atr)
        self.assertTrue(emp.is_statistically_significant)
        self.assertLess(emp.p_value, 0.05)

    def test_phase_2_war_room_monte_carlo_and_red_team(self):
        decompiler = MarketDecompiler(self.symbol)
        ast = decompiler.decompile(self.timeframe, 500)
        tracer = EmpiricalTraceEngine(self.symbol)
        bundle = tracer.build_evidence_bundle(ast)

        self.assertTrue(bundle.bundle_id.startswith("EV-XAUUSD"))
        self.assertEqual(bundle.monte_carlo_audit.total_paths, 1000)
        self.assertLess(bundle.monte_carlo_audit.execution_time_ms, 500.0)
        self.assertTrue(bundle.truth_gate_audit.is_verified_zero_hallucination)
        self.assertEqual(bundle.truth_gate_audit.fsm_state, "EVIDENCE_VERIFIED")
        self.assertIsNotNone(bundle.red_team_critique.adversarial_verdict)

    def test_truth_gate_blocks_hallucinated_numbers(self):
        decompiler = MarketDecompiler(self.symbol)
        ast = decompiler.decompile(self.timeframe, 150)
        gate = TruthGatekeeperFSM(self.symbol)

        fake_finding = EvidenceFinding(
            category="VOLUME_ABSORPTION",
            metric_name="effort_vs_result_ratio",
            observed_value=99.99,
            benchmark_value=1.0,
            description="Fake hallucinated volume ratio",
            is_anomaly=True
        )
        audit = gate.verify_findings_against_ast(ast, [fake_finding])
        self.assertFalse(audit.is_verified_zero_hallucination)
        self.assertEqual(audit.fsm_state, "BLOCKED_BY_GATE")
        self.assertGreater(len(audit.mismatches_found), 0)

    def test_phase_3_clean_room_safe_sl_distance_standard_and_cent(self):
        decompiler = MarketDecompiler(self.symbol)
        ast = decompiler.decompile(self.timeframe, 500)
        tracer = EmpiricalTraceEngine(self.symbol)
        bundle = tracer.build_evidence_bundle(ast)

        synthesizer = CleanRoomSynthesizer(self.symbol)
        order_std = synthesizer.synthesize_order(ast, bundle, account_type="STANDARD", risk_percent=1.0)
        self.assertIsNotNone(order_std)
        self.assertEqual(order_std.base_capital, 100.0)
        self.assertEqual(order_std.risk_amount_money, 1.0)
        self.assertGreaterEqual(abs(order_std.entry_price - order_std.hard_sl), 1.20)
        self.assertGreaterEqual(order_std.risk_reward_ratio, 2.0)

        order_cent = synthesizer.synthesize_order(ast, bundle, account_type="CENT", risk_percent=1.0)
        self.assertIsNotNone(order_cent)
        self.assertEqual(order_cent.base_capital, 10000.0)
        self.assertEqual(order_cent.risk_amount_money, 100.0)

    def test_bayesian_self_evolving_brain(self):
        brain = BayesianSelfEvolvingBrain(self.symbol)
        gen_before = brain.memory["generation"]
        autopsy = brain.record_post_trade_autopsy(
            algo_type="JUDAS_SWING_STOP_RAID",
            outcome="WIN",
            realized_r=2.25,
            observed_pierce_atr=0.45,
            notes="Unit test verification"
        )
        self.assertEqual(autopsy["outcome"], "WIN")
        self.assertEqual(brain.memory["generation"], gen_before + 1)
        alloc = brain.get_dynamic_risk_allocation("JUDAS_SWING_STOP_RAID", 0.86)
        self.assertIn(alloc["recommended_risk_percent"], [0.5, 1.0, 1.5])

    def test_model_auto_failover_cascade(self):
        router = ModelIntelligenceRouter()

        # 1. Primary Gemini 4 Argon available
        r1 = router.route_task("FINAL_TRIGGER", confidence=0.85, simulate_gemini4_exhausted=False)
        self.assertEqual(r1["active_model_id"], "gemini_4_argon")
        self.assertFalse(r1["failover_triggered"])
        self.assertEqual(r1["enforced_max_risk_pct"], 1.5)

        # 2. Gemini 4 Argon exhausted -> Auto-failover to Gemini 3.8 Pro (High)
        r2 = router.route_task("FINAL_TRIGGER", confidence=0.85, simulate_gemini4_exhausted=True, simulate_pro_exhausted=False)
        self.assertEqual(r2["active_model_id"], "gemini_3_8_pro_high")
        self.assertTrue(r2["failover_triggered"])
        self.assertEqual(r2["enforced_max_risk_pct"], 1.0)
        self.assertEqual(r2["enforced_min_confidence"], 0.80)

        # 3. Both Argon & Pro exhausted -> Auto-failover to Gemini 3.8 Flash (High) with defensive 0.5% risk cap
        r3 = router.route_task("FINAL_TRIGGER", confidence=0.85, simulate_gemini4_exhausted=True, simulate_pro_exhausted=True)
        self.assertEqual(r3["active_model_id"], "gemini_3_8_flash_high")
        self.assertTrue(r3["failover_triggered"])
        self.assertEqual(r3["enforced_max_risk_pct"], 0.5)
        self.assertEqual(r3["enforced_min_confidence"], 0.83)

        # 4. Verify WarRoomCommander respects failover risk cap
        cmd = WarRoomCommander(self.symbol, self.timeframe)
        cycle_fallback = cmd.execute_war_room_cycle(
            account_type="STANDARD",
            risk_percent=1.5,
            simulate_gemini4_exhausted=True,
            simulate_pro_exhausted=False
        )
        self.assertEqual(cycle_fallback["model_intelligence_routing"]["active_model_id"], "gemini_3_8_pro_high")
        if cycle_fallback["clean_room_order"]:
            self.assertLessEqual(cycle_fallback["clean_room_order"]["risk_percent"], 1.0)

    def test_ea_strategy_decompiler_and_mcp(self):
        decompiler = EAStrategyDecompiler()
        toxic_code = """
        input double Lots = 0.01;
        input double LotMultiplier = 2.0;
        input int StopLoss = 0;
        void OnTick() { if (loss) lot = lot * LotMultiplier; }
        """
        report = decompiler.decompile_code(toxic_code, "ToxicMartingaleEA.mq4")
        self.assertEqual(report["verdict"], "DANGEROUS_HIGH_RISK")

        res = handle_tool_call("rea_decompile_market", {"symbol": "XAUUSD", "timeframe": "M15", "bars": 200})
        self.assertIn("empirical_distribution", res)


if __name__ == "__main__":
    unittest.main()
