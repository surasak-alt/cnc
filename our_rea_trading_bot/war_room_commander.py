# -*- coding: utf-8 -*-
"""
Autonomous War-Room Commander (Our REA Live Trading Bot)
Integrates:
1. Universal Trading REA Toolkit (MarketDecompiler, EmpiricalTraceEngine, CleanRoomSynthesizer, TruthGatekeeperFSM, BayesianSelfEvolvingBrain)
2. Intelligent Model Router with Auto-Fallback Cascade (Gemini 4 Argon -> Pro -> Flash -> Local NumPy)
3. MT5 Zero-Ping Execution Bridge ($100 Standard / 10,000 Cents Cent Account)
"""

import sys
from pathlib import Path
from typing import Dict, Any

BOT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BOT_DIR.parent
TOOLKIT_DIR = WORKSPACE_ROOT / "rea_trading_toolkit"

for p in (str(BOT_DIR), str(TOOLKIT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from providers.market_decompiler import MarketDecompiler
from providers.empirical_trace_engine import EmpiricalTraceEngine
from providers.clean_room_synthesizer import CleanRoomSynthesizer
from providers.truth_gatekeeper_fsm import TruthGatekeeperFSM
from providers.self_evolving_brain import BayesianSelfEvolvingBrain

from model_intelligence_router import ModelIntelligenceRouter
from mt5_execution_bridge import MT5ExecutionBridge


class WarRoomCommander:
    def __init__(self, symbol: str = "XAUUSD", timeframe: str = "M15"):
        self.symbol = symbol
        self.timeframe = timeframe
        self.decompiler = MarketDecompiler(symbol)
        self.tracer = EmpiricalTraceEngine(symbol)
        self.synthesizer = CleanRoomSynthesizer(symbol)
        self.gatekeeper = TruthGatekeeperFSM(symbol)
        self.brain = BayesianSelfEvolvingBrain(symbol)
        self.router = ModelIntelligenceRouter()
        self.mt5_bridge = MT5ExecutionBridge(symbol)

    def execute_war_room_cycle(
        self,
        account_type: str = "STANDARD",
        risk_percent: float = 1.0,
        execute_live_mt5: bool = False,
        force_wake_ai: bool = True,
        simulate_gemini4_exhausted: bool = False,
        simulate_pro_exhausted: bool = False
    ) -> Dict[str, Any]:
        """
        Runs the complete 4-Stage Autonomous War-Room Cycle with strict model routing,
        automatic failover cascade, and real token measurement.
        """
        # Stage 1: Tier 0 Local Decompilation & Empirical Mining (0 Tokens)
        ast = self.decompiler.decompile(self.timeframe, num_bars=500)

        # Stage 2: Tier 1 Local Delta Gate Check (0 Tokens)
        delta_status = self.gatekeeper.check_delta_gate(ast)
        if delta_status["is_dead_air_skipped"] and not force_wake_ai:
            route_info = self.router.route_task("DEAD_AIR_CHECK", is_dead_air=True)
            return {
                "status": "SKIPPED_BY_LOCAL_DELTA_GATE",
                "delta_gate": delta_status,
                "model_routing": route_info,
                "tokens_consumed": 0
            }

        # Stage 3: War-Room Evidence Trace (Red Team + 1,000-Path Monte Carlo + Truth Gate)
        bundle = self.tracer.build_evidence_bundle(ast)

        # Stage 4: Model Routing & Auto-Failover Cascade Check
        route_info = self.router.route_task(
            task_type="FINAL_TRIGGER_SNIPER_AUTH",
            is_dead_air=False,
            confidence=bundle.confidence_score,
            simulate_gemini4_exhausted=simulate_gemini4_exhausted,
            simulate_pro_exhausted=simulate_pro_exhausted
        )

        # Stage 5: Bayesian Dynamic Risk & Fallback Safety Cap Enforcement
        alloc = self.brain.get_dynamic_risk_allocation(
            bundle.algo_footprint.algo_type,
            bundle.confidence_score
        )
        raw_risk = risk_percent if risk_percent > 0 else alloc["recommended_risk_percent"]
        # Enforce fallback model's maximum allowed risk cap and minimum confidence
        capped_risk = min(raw_risk, route_info.get("enforced_max_risk_pct", 1.5))
        min_conf_req = route_info.get("enforced_min_confidence", 0.78)

        order = None
        if bundle.confidence_score >= min_conf_req:
            order = self.synthesizer.synthesize_order(
                ast=ast,
                evidence=bundle,
                account_type=account_type,
                risk_percent=capped_risk
            )

        dsl_audit = self.router.encode_micro_dsl_payload(
            ast_dict=ast.model_dump(),
            bundle_dict=bundle.model_dump(),
            order_dict=order.model_dump() if order else None
        )
        if route_info.get("active_model_id"):
            self.router.record_token_consumption(
                route_info["active_model_id"],
                dsl_audit["total_measured_tokens_per_wake"]
            )

        endurance_audit = self.router.audit_package_endurance(
            measured_tokens_per_wake=dsl_audit["total_measured_tokens_per_wake"]
        )

        # Stage 6: Live MT5 Pending Order Dispatch (if requested and approved)
        mt5_dispatch = {"executed": False, "mode": "STANDBY_ANALYSIS_ONLY"}
        if execute_live_mt5 and order is not None:
            mt5_dispatch = self.mt5_bridge.place_pending_order(
                action_str=order.action,
                entry_price=order.entry_price,
                hard_sl=order.hard_sl,
                hard_tp=order.hard_tp,
                lot_size=order.lot_size,
                comment=f"REA_{bundle.algo_footprint.algo_type[:10]}"
            )

        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "model_intelligence_routing": route_info,
            "micro_dsl_token_measurement": dsl_audit,
            "package_quota_endurance": endurance_audit["package_endurance_summary"]["1_ANTIGRAVITY_PRO_WORKSPACE_SUBSCRIPTION"],
            "failover_cascade_matrix": endurance_audit["package_endurance_summary"]["2_FAILOVER_CASCADE_SIMULATION"],
            "bayesian_brain_allocation": alloc,
            "evidence_verdict": bundle.verdict,
            "clean_room_order": order.model_dump() if order else None,
            "mt5_execution_result": mt5_dispatch
        }
