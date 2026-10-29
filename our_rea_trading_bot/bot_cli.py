# -*- coding: utf-8 -*-
"""
Our REA Trading Bot CLI (`our_rea_trading_bot/bot_cli.py`)
Commands:
- war-room: Run full War-Room cycle, model routing check, and real token measurement
- model-audit: Inspect 4-Tier AI Model Routing & Package Quota Endurance (Hours/Day & Month)
- execute-sniper: Synthesize and dispatch 0ms Pending Order to MT5
- guard: Run 0ms Zero-Token Local Guardian (Break-Even +0.85R, Trailing +1.5R, 3% Circuit Breaker)
- cancel-all: Cancel all pending orders in MT5
- panic-close: Emergency close all open positions in MT5
"""

import sys
import json
import argparse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BOT_DIR = Path(__file__).resolve().parent
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from war_room_commander import WarRoomCommander
from model_intelligence_router import ModelIntelligenceRouter
from mt5_execution_bridge import MT5ExecutionBridge


def main():
    parser = argparse.ArgumentParser(description="Our REA Autonomous Trading Bot Commander")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_wr = subparsers.add_parser("war-room", help="Run full War-Room analysis + Model & Token Audit")
    p_wr.add_argument("--symbol", default="XAUUSD")
    p_wr.add_argument("--tf", default="M15")
    p_wr.add_argument("--account", choices=["STANDARD", "CENT"], default="STANDARD")
    p_wr.add_argument("--risk", type=float, default=1.0)

    p_ma = subparsers.add_parser("model-audit", help="Audit AI Model Tiers & Real Token Package Quota")
    p_ma.add_argument("--symbol", default="XAUUSD")
    p_ma.add_argument("--tf", default="M15")

    p_ex = subparsers.add_parser("execute-sniper", help="Execute 0ms Pending Sniper Order on MT5")
    p_ex.add_argument("--symbol", default="XAUUSD")
    p_ex.add_argument("--tf", default="M15")
    p_ex.add_argument("--account", choices=["STANDARD", "CENT"], default="STANDARD")
    p_ex.add_argument("--risk", type=float, default=1.0)

    p_gd = subparsers.add_parser("guard", help="Run 0-Token Local Guardian (BE, Trailing, 3% Breaker)")
    p_gd.add_argument("--symbol", default="XAUUSD")

    p_ca = subparsers.add_parser("cancel-all", help="Cancel all pending orders")
    p_ca.add_argument("--symbol", default="XAUUSD")

    p_pc = subparsers.add_parser("panic-close", help="Emergency close all positions")
    p_pc.add_argument("--symbol", default="XAUUSD")

    args = parser.parse_args()

    if args.command == "war-room":
        cmd = WarRoomCommander(args.symbol, args.tf)
        res = cmd.execute_war_room_cycle(
            account_type=args.account,
            risk_percent=args.risk,
            execute_live_mt5=False,
            force_wake_ai=True
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "model-audit":
        cmd = WarRoomCommander(args.symbol, args.tf)
        res = cmd.execute_war_room_cycle(force_wake_ai=True)
        dsl = res["micro_dsl_token_measurement"]
        router = ModelIntelligenceRouter()
        audit = router.audit_package_endurance(measured_tokens_per_wake=dsl["total_measured_tokens_per_wake"])
        print("\n" + "="*78)
        print("🧠 AI MODEL INTELLIGENCE ROUTING & REAL TOKEN QUOTA AUDIT")
        print("="*78)
        print(f"📏 Real Measured Micro-DSL Payload ({dsl['character_count']} chars):")
        print("-" * 78)
        print(dsl["micro_dsl_text"])
        print("-" * 78)
        print(f"🔢 Measured Input Tokens: {dsl['measured_input_tokens']} | Output Tokens: {dsl['measured_output_tokens']} | Total/Wake: {dsl['total_measured_tokens_per_wake']} Tokens")
        print(f"🎯 Selected Tier for Current Market: {res['model_intelligence_routing']['selected_tier']}")
        print(f"🤖 Assigned AI Model: {res['model_intelligence_routing']['assigned_model']}")
        print(f"📝 Routing Reason: {res['model_intelligence_routing']['routing_reason']}")
        print("\n📊 PACKAGE ENDURANCE SUMMARY (1 DAY & 1 MONTH):")
        print(json.dumps(audit["package_endurance_summary"], indent=2, ensure_ascii=False))
        print("="*78)

    elif args.command == "execute-sniper":
        cmd = WarRoomCommander(args.symbol, args.tf)
        res = cmd.execute_war_room_cycle(
            account_type=args.account,
            risk_percent=args.risk,
            execute_live_mt5=True,
            force_wake_ai=True
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "guard":
        bridge = MT5ExecutionBridge(args.symbol)
        print(json.dumps(bridge.run_zero_token_local_guardian(), indent=2, ensure_ascii=False))

    elif args.command == "cancel-all":
        bridge = MT5ExecutionBridge(args.symbol)
        print(json.dumps(bridge.cancel_all_pending(), indent=2, ensure_ascii=False))

    elif args.command == "panic-close":
        bridge = MT5ExecutionBridge(args.symbol)
        print(json.dumps(bridge.panic_close_all(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
