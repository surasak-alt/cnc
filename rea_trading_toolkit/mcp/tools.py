# -*- coding: utf-8 -*-
"""
Trading REA MCP Tools Registry
Defines the tool definitions and dispatch handlers for the MCP Server.
"""

import json
from typing import Dict, Any, List

from providers.market_decompiler import MarketDecompiler
from providers.empirical_trace_engine import EmpiricalTraceEngine
from providers.broker_blindspot_engine import BrokerBlindspotEngine
from providers.clean_room_synthesizer import CleanRoomSynthesizer
from providers.ea_strategy_decompiler import EAStrategyDecompiler


def get_tool_definitions() -> List[Dict[str, Any]]:
    return [
        {
            "name": "rea_decompile_market",
            "description": "Phase 1: Decompiles raw market OHLCV and tick feed into a structured Market-AST (Swings, FVGs, Liquidity Pools, Volume Delta).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "default": "XAUUSD", "description": "Trading asset symbol"},
                    "timeframe": {"type": "string", "default": "M15", "description": "M1, M5, M15, H1, H4, D1"},
                    "bars": {"type": "integer", "default": 100, "description": "Number of bars to analyze"}
                },
                "required": ["symbol"]
            }
        },
        {
            "name": "rea_build_evidence_bundle",
            "description": "Phase 2: Evaluates market habits and outputs an official Trading Evidence Bundle v2 with empirical metrics, confidence score, and known limitations.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "default": "XAUUSD"},
                    "timeframe": {"type": "string", "default": "M15"}
                },
                "required": ["symbol"]
            }
        },
        {
            "name": "rea_synthesize_clean_order",
            "description": "Phase 3: Synthesizes a clean-room zero-ping pending order (Limit Entry at 50% FVG Equilibrium with Hard SL/TP) strictly based on empirical evidence.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "default": "XAUUSD"},
                    "timeframe": {"type": "string", "default": "M15"},
                    "account_type": {"type": "string", "enum": ["STANDARD", "CENT"], "default": "STANDARD"},
                    "risk_percent": {"type": "number", "default": 1.0, "description": "Percentage risk per trade"}
                },
                "required": ["symbol"]
            }
        },
        {
            "name": "rea_audit_broker_blindspot",
            "description": "Reverse-engineers broker spread, TRADE_STOPS_LEVEL, and calculates Asymmetric Bid/Ask compensation buffers.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "default": "XAUUSD"}
                },
                "required": ["symbol"]
            }
        },
        {
            "name": "rea_inspect_external_strategy",
            "description": "Reverse-engineers external EA, MQL4/MQL5 code, or Pine Script to detect toxic Martingale/Grid traps and extract indicator formulas.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "code_content": {"type": "string", "description": "The script source code string to inspect"},
                    "strategy_name": {"type": "string", "default": "TargetStrategy"}
                },
                "required": ["code_content"]
            }
        }
    ]


def handle_tool_call(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    symbol = args.get("symbol", "XAUUSD")
    tf = args.get("timeframe", "M15")

    if name == "rea_decompile_market":
        decompiler = MarketDecompiler(symbol)
        bars = args.get("bars", 100)
        ast = decompiler.decompile(tf, bars)
        return ast.model_dump()

    elif name == "rea_build_evidence_bundle":
        decompiler = MarketDecompiler(symbol)
        ast = decompiler.decompile(tf, 100)
        tracer = EmpiricalTraceEngine(symbol)
        bundle = tracer.build_evidence_bundle(ast)
        return bundle.model_dump()

    elif name == "rea_synthesize_clean_order":
        decompiler = MarketDecompiler(symbol)
        ast = decompiler.decompile(tf, 100)
        tracer = EmpiricalTraceEngine(symbol)
        bundle = tracer.build_evidence_bundle(ast)
        synthesizer = CleanRoomSynthesizer(symbol)
        acc_type = args.get("account_type", "STANDARD")
        risk = args.get("risk_percent", 1.0)
        order = synthesizer.synthesize_order(ast, bundle, account_type=acc_type, risk_percent=risk)
        if order is None:
            return {
                "status": "REJECTED_BY_EVIDENCE",
                "reason": bundle.reasoning_summary,
                "evidence_bundle_ref": bundle.bundle_id
            }
        return order.model_dump()

    elif name == "rea_audit_broker_blindspot":
        broker = BrokerBlindspotEngine(symbol)
        return broker.audit_broker_rules()

    elif name == "rea_inspect_external_strategy":
        decompiler = EAStrategyDecompiler()
        code = args.get("code_content", "")
        name_str = args.get("strategy_name", "TargetStrategy")
        return decompiler.decompile_code(code, name_str)

    else:
        raise ValueError(f"Unknown Trading REA tool: {name}")
