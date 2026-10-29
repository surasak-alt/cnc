# -*- coding: utf-8 -*-
"""
Trading REA Command Line Interface (CLI - 2026-2036 Ideal War-Room Architecture)
Mirrors morluto/rea's CLI interface for AI agents and human traders:
- decompile: Phase 1 Market-AST disassembly + Empirical Statistical Mining
- trace: Phase 2 Evidence Bundle v2 + Red Team + 1,000-Path Quantum Monte Carlo + Truth Gate
- synthesize: Phase 3 Clean-Room Order generation with Bayesian Dynamic Risk
- pipeline: Full end-to-end 3-Phase Autonomous War-Room execution
- autopsy: Post-trade Bayesian learning update
- decompile-strategy: Static analysis of external EA or Pine Script
- audit-broker: Reverse-engineer broker spread & stops
- mcp-serve: Start MCP server for Claude Code / Gemini / Antigravity
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Force UTF-8 encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from providers.market_decompiler import MarketDecompiler
from providers.empirical_trace_engine import EmpiricalTraceEngine
from providers.broker_blindspot_engine import BrokerBlindspotEngine
from providers.clean_room_synthesizer import CleanRoomSynthesizer
from providers.ea_strategy_decompiler import EAStrategyDecompiler
from providers.self_evolving_brain import BayesianSelfEvolvingBrain
from mcp.server import TradingREAMCPServer


def cmd_decompile(args):
    print(f"\n🔍 [PHASE 1: DECOMPILE] Disassembling Market-AST & Mining {args.bars} Bars for {args.symbol} ({args.tf})...")
    decompiler = MarketDecompiler(args.symbol)
    ast = decompiler.decompile(args.tf, args.bars)
    emp = ast.empirical_distribution

    print("\n" + "="*76)
    print(f"📊 MARKET-AST: {ast.symbol} [{ast.timeframe}] | Regime: {ast.market_regime}")
    print(f"💰 Current Bid: {ast.current_bid} | Ask: {ast.current_ask} | ATR(14): {ast.atr_14}")
    print(f"⚡ Swing Points: {len(ast.swing_points)} | Active FVGs: {len(ast.active_fvgs)} | Liquidity Pools: {len(ast.liquidity_pools)}")
    print(f"📈 Effort vs Result Ratio: {ast.volume_delta.effort_vs_result_ratio} (Absorption: {ast.volume_delta.absorption_detected})")
    print(f"🔬 Empirical Stop-Hunt Mining (N={emp.sweep_sample_size} sweeps across {emp.bars_analyzed} bars):")
    print(f"   • Mean Pierce (μ): {emp.mean_pierce_atr}x ATR | Std Dev (σ): {emp.std_pierce_atr}x ATR")
    print(f"   • 95th Percentile Safe SL: {emp.p95_safe_sl_atr}x ATR")
    print(f"   • Anomaly Vol Reversal Rate: {round(emp.anomaly_vol_reversal_rate*100, 1)}% vs Normal Vol: {round(emp.normal_vol_reversal_rate*100, 1)}%")
    print(f"   • Statistical Significance: Z={emp.z_score_stat}, p-value={emp.p_value} (Significant: {emp.is_statistically_significant})")
    print(f"🌐 Cross-Asset Radar: {ast.cross_asset_radar.description}")
    print("="*76)

    if args.json:
        print(ast.model_dump_json(indent=2))


def cmd_trace(args):
    print(f"\n🔎 [PHASE 2: UNDERSTAND] Running Multi-Agent War-Room & Evidence Trace for {args.symbol}...")
    decompiler = MarketDecompiler(args.symbol)
    ast = decompiler.decompile(args.tf, 500)
    tracer = EmpiricalTraceEngine(args.symbol)
    bundle = tracer.build_evidence_bundle(ast)

    vault_dir = CURRENT_DIR / "evidence_vault"
    vault_dir.mkdir(exist_ok=True)
    bundle_path = vault_dir / f"{bundle.bundle_id}.json"
    with open(bundle_path, "w", encoding="utf-8") as f:
        f.write(bundle.model_dump_json(indent=2))

    mc = bundle.monte_carlo_audit
    rt = bundle.red_team_critique
    tg = bundle.truth_gate_audit

    print("\n" + "="*76)
    print(f"🛡️ EVIDENCE BUNDLE: {bundle.bundle_id}")
    print(f"🎯 Classified Algo: {bundle.algo_footprint.algo_type} (Mined Winrate: {round(bundle.algo_footprint.historical_win_probability*100, 1)}%, N={bundle.algo_footprint.sample_size})")
    print(f"🎲 Quantum Monte Carlo ({mc.total_paths} Paths in {mc.execution_time_ms} ms | 0 Tokens):")
    print(f"   • Simulated Winrate: {mc.simulated_winrate_pct}% | Expected Value: +{mc.expected_value_r}R | Survived Stress: {mc.survived_stress_test}")
    print(f"👹 Red Team Adversarial Critique:")
    print(f"   • {rt.adversarial_verdict}")
    for atk in rt.attack_vectors:
        print(f"   • [Attack Vector] {atk}")
    print(f"🔒 Deterministic Truth Gatekeeper & FSM:")
    print(f"   • Zero-Hallucination Verified: {tg.is_verified_zero_hallucination} ({tg.cross_checked_metrics_count} metrics cross-checked) | State: {tg.fsm_state}")
    print(f"🧠 Final Statistical Confidence: {round(bundle.confidence_score*100, 1)}%")
    print(f"⚖️ Verdict: {bundle.verdict}")
    print(f"📝 Summary: {bundle.reasoning_summary}")
    if bundle.known_limitations:
        print(f"⚠️ Known Limitations ({len(bundle.known_limitations)}):")
        for lim in bundle.known_limitations:
            print(f"   • {lim}")
    print(f"💾 Saved Evidence Snapshot: {bundle_path.name}")
    print("="*76)

    if args.json:
        print(bundle.model_dump_json(indent=2))


def cmd_synthesize(args):
    print(f"\n⚡ [PHASE 3: RECREATE] Synthesizing Clean-Room Order for {args.symbol}...")
    decompiler = MarketDecompiler(args.symbol)
    ast = decompiler.decompile(args.tf, 500)
    tracer = EmpiricalTraceEngine(args.symbol)
    bundle = tracer.build_evidence_bundle(ast)

    brain = BayesianSelfEvolvingBrain(args.symbol)
    alloc = brain.get_dynamic_risk_allocation(bundle.algo_footprint.algo_type, bundle.confidence_score)
    effective_risk = args.risk if args.risk > 0 else alloc["recommended_risk_percent"]

    synthesizer = CleanRoomSynthesizer(args.symbol)
    order = synthesizer.synthesize_order(ast, bundle, account_type=args.account, risk_percent=effective_risk)

    print("\n" + "="*76)
    if order is None:
        print(f"❌ EXECUTION REJECTED BY WAR-ROOM GATEKEEPER")
        print(f"Reason: {bundle.reasoning_summary}")
    else:
        print(f"🚀 CLEAN-ROOM ORDER GENERATED: {order.order_id}")
        print(f"Action: {order.action} {order.symbol} @ {order.entry_price}")
        print(f"Hard SL: {order.hard_sl} (P95 Buffer: {order.stop_hunt_sl_buffer_atr}x ATR) | Hard TP: {order.hard_tp} (R:R = 1:{order.risk_reward_ratio})")
        print(f"SL Distance: {round(abs(order.entry_price - order.hard_sl), 2)} USD ({int(round(abs(order.entry_price - order.hard_sl)*100))} Points)")
        print(f"Lot Size: {order.lot_size} | Risk: {order.risk_percent}% ({order.risk_amount_money} {'Cents' if order.account_type=='CENT' else 'USD'} on {order.base_capital} {order.account_type})")
        print(f"Bayesian Brain Tier: {alloc['setup_tier']} (Weight: {alloc['bayesian_weight']}, Gen: {alloc['brain_generation']})")
        print(f"Server-Side Zero Ping: {order.zero_ping_server_side} | Authorized by: {order.evidence_bundle_ref}")
    print("="*76)

    if args.json and order is not None:
        print(order.model_dump_json(indent=2))


def cmd_pipeline(args):
    print("\n" + "#"*76)
    print("🛡️ TRADING REA: 2026-2036 AUTONOMOUS MULTI-AGENT WAR-ROOM PIPELINE")
    print("#"*76)

    decompiler = MarketDecompiler(args.symbol)
    ast = decompiler.decompile(args.tf, 500)
    emp = ast.empirical_distribution
    print(f"\n[1/4] Decompile & Big-Data Mining ({emp.bars_analyzed} bars):")
    print(f"      • Extracted {len(ast.swing_points)} swings, {len(ast.active_fvgs)} FVGs, {len(ast.liquidity_pools)} Liquidity Pools ({ast.market_regime})")
    print(f"      • Mined N={emp.sweep_sample_size} Stop-Hunts: Mean={emp.mean_pierce_atr}x ATR, P95 Safe SL={emp.p95_safe_sl_atr}x ATR (Z={emp.z_score_stat}, p={emp.p_value})")
    print(f"      • Cross-Asset Radar: {ast.cross_asset_radar.description}")

    tracer = EmpiricalTraceEngine(args.symbol)
    bundle = tracer.build_evidence_bundle(ast)
    mc = bundle.monte_carlo_audit
    rt = bundle.red_team_critique
    tg = bundle.truth_gate_audit
    print(f"\n[2/4] War-Room Debate & Quantum Simulation:")
    print(f"      • Algo Footprint: {bundle.algo_footprint.algo_type} (Empirical Winrate: {round(bundle.algo_footprint.historical_win_probability*100, 1)}%)")
    print(f"      • 1,000-Path Vectorized Monte Carlo: {mc.simulated_winrate_pct}% Winrate, EV=+{mc.expected_value_r}R in {mc.execution_time_ms} ms (0 Tokens)")
    print(f"      • Red Team Adversarial Check: {rt.adversarial_verdict}")
    print(f"      • Truth Gatekeeper: Verified={tg.is_verified_zero_hallucination} | FSM State={tg.fsm_state}")

    brain = BayesianSelfEvolvingBrain(args.symbol)
    alloc = brain.get_dynamic_risk_allocation(bundle.algo_footprint.algo_type, bundle.confidence_score)
    print(f"\n[3/4] Self-Evolving Bayesian Brain (Gen {alloc['brain_generation']}):")
    print(f"      • Tier: {alloc['setup_tier']} | Bayesian Weight: {alloc['bayesian_weight']} | Confidence: {round(bundle.confidence_score*100, 1)}%")

    synthesizer = CleanRoomSynthesizer(args.symbol)
    order = synthesizer.synthesize_order(ast, bundle, account_type=args.account, risk_percent=args.risk)
    if order:
        print(f"\n[4/4] Clean-Room 0ms Order Synthesis:")
        print(f"      • {order.action} {order.symbol} @ {order.entry_price} | Hard SL: {order.hard_sl} | Hard TP: {order.hard_tp} (R:R 1:{order.risk_reward_ratio})")
        print(f"      • Lot: {order.lot_size} | Capital Base: {order.base_capital} ({order.account_type}) | Risk: {order.risk_amount_money}")
    else:
        print(f"\n[4/4] Clean-Room Synthesis: NO ORDER DISPATCHED ({bundle.verdict})")
    print("#"*76 + "\n")


def cmd_autopsy(args):
    brain = BayesianSelfEvolvingBrain(args.symbol)
    res = brain.record_post_trade_autopsy(
        algo_type=args.algo,
        outcome=args.outcome,
        realized_r=args.r,
        observed_pierce_atr=args.pierce,
        notes=args.notes
    )
    print("\n" + "="*76)
    print("🧬 BAYESIAN POST-TRADE AUTOPSY RECORDED:")
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print("="*76)


def cmd_audit_broker(args):
    broker = BrokerBlindspotEngine(args.symbol)
    res = broker.audit_broker_rules()
    print("\n" + "="*76)
    print(f"🏦 BROKER MICROSTRUCTURE AUDIT: {args.symbol}")
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print("="*76)


def cmd_decompile_strategy(args):
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        return
    with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    decompiler = EAStrategyDecompiler()
    report = decompiler.decompile_code(code, Path(args.file).name)
    print("\n" + "="*76)
    print(f"🕵️ STRATEGY REVERSE-ENGINEERING AUDIT REPORT")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("="*76)


def cmd_mcp_serve(args):
    server = TradingREAMCPServer()
    server.run()


def main():
    parser = argparse.ArgumentParser(description="Trading REA: 2026-2036 Autonomous Reverse-Engineering Trading System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_dec = subparsers.add_parser("decompile", help="Phase 1: Decompile market & mine statistical distribution")
    p_dec.add_argument("--symbol", default="XAUUSD")
    p_dec.add_argument("--tf", default="M15")
    p_dec.add_argument("--bars", type=int, default=500)
    p_dec.add_argument("--json", action="store_true")

    p_tra = subparsers.add_parser("trace", help="Phase 2: Run War-Room & generate Evidence Bundle v2")
    p_tra.add_argument("--symbol", default="XAUUSD")
    p_tra.add_argument("--tf", default="M15")
    p_tra.add_argument("--json", action="store_true")

    p_syn = subparsers.add_parser("synthesize", help="Phase 3: Synthesize Clean-Room Order")
    p_syn.add_argument("--symbol", default="XAUUSD")
    p_syn.add_argument("--tf", default="M15")
    p_syn.add_argument("--account", choices=["STANDARD", "CENT"], default="STANDARD")
    p_syn.add_argument("--risk", type=float, default=1.0)
    p_syn.add_argument("--json", action="store_true")

    p_pipe = subparsers.add_parser("pipeline", help="Run full 2026-2036 War-Room REA pipeline end-to-end")
    p_pipe.add_argument("--symbol", default="XAUUSD")
    p_pipe.add_argument("--tf", default="M15")
    p_pipe.add_argument("--account", choices=["STANDARD", "CENT"], default="STANDARD")
    p_pipe.add_argument("--risk", type=float, default=1.0)

    p_aut = subparsers.add_parser("autopsy", help="Record post-trade autopsy to Bayesian Self-Evolving Brain")
    p_aut.add_argument("--symbol", default="XAUUSD")
    p_aut.add_argument("--algo", default="ICEBERG_ABSORPTION_WALL")
    p_aut.add_argument("--outcome", choices=["WIN", "LOSS"], required=True)
    p_aut.add_argument("--r", type=float, default=2.2)
    p_aut.add_argument("--pierce", type=float, default=0.44)
    p_aut.add_argument("--notes", default="Post-session update")

    p_brok = subparsers.add_parser("audit-broker", help="Reverse-engineer broker spread & freeze levels")
    p_brok.add_argument("--symbol", default="XAUUSD")

    p_strat = subparsers.add_parser("decompile-strategy", help="Decompile external EA/PineScript file")
    p_strat.add_argument("--file", required=True)

    subparsers.add_parser("mcp-serve", help="Launch Trading REA MCP Server (stdio)")

    args = parser.parse_args()
    dispatch = {
        "decompile": cmd_decompile,
        "trace": cmd_trace,
        "synthesize": cmd_synthesize,
        "pipeline": cmd_pipeline,
        "autopsy": cmd_autopsy,
        "audit-broker": cmd_audit_broker,
        "decompile-strategy": cmd_decompile_strategy,
        "mcp-serve": cmd_mcp_serve,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
