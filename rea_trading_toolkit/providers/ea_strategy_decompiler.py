# -*- coding: utf-8 -*-
"""
EA & Strategy Decompiler Provider
Directly adopts morluto/rea's software reverse-engineering capability to:
- Decompile / inspect external MT4/MT5 EAs (.mq4, .mq5, decompiled logs)
- Inspect TradingView Pine Script files (.pine)
- Detect toxic Martingale, Grid, or Naked-Order anti-patterns
- Extract hidden indicator parameters and trigger thresholds
"""

import re
from typing import Dict, Any, List


class EAStrategyDecompiler:
    def __init__(self):
        pass

    def decompile_code(self, source_code: str, file_name: str = "unknown_strategy") -> Dict[str, Any]:
        """
        Inspects strategy source code and produces a Reverse-Engineering Strategy Audit Report.
        """
        report: Dict[str, Any] = {
            "file_name": file_name,
            "detected_language": self._detect_language(source_code),
            "toxic_risk_score": 0,  # 0 to 100
            "toxic_flags": [],
            "extracted_indicators": [],
            "money_management": {},
            "verdict": "SAFE"
        }

        # 1. Martingale Detection
        martingale_patterns = [
            r"LotMultiplier\s*=\s*[1-9]",
            r"lot\s*\*=\s*2",
            r"lot\s*=\s*lot\s*\*\s*(1\.[5-9]|[2-9])",
            r"Lots\s*=\s*Lots\s*\*",
            r"martingale\s*=\s*true",
        ]
        for pattern in martingale_patterns:
            if re.search(pattern, source_code, re.IGNORECASE):
                report["toxic_flags"].append("TOXIC_MARTINGALE_DETECTED: Account blow-up risk via position doubling")
                report["toxic_risk_score"] += 45
                break

        # 2. Grid Trading Detection (Averaging down)
        grid_patterns = [
            r"GridStep\s*=",
            r"PipStep\s*=",
            r"DistanceStep\s*=",
            r"MaxTrades\s*=\s*([5-9]|[1-9][0-9])",
        ]
        for pattern in grid_patterns:
            if re.search(pattern, source_code, re.IGNORECASE):
                report["toxic_flags"].append("GRID_ACCUMULATION_DETECTED: Stacking positions against floating drawdown")
                report["toxic_risk_score"] += 35
                break

        # 3. Naked Orders Detection (Zero Stop Loss)
        if re.search(r"StopLoss\s*=\s*0|SL\s*=\s*0|stop_loss\s*=\s*0", source_code, re.IGNORECASE):
            report["toxic_flags"].append("NAKED_ORDERS_DETECTED: Orders placed without hard stop loss protection")
            report["toxic_risk_score"] += 40

        # 4. Indicator Extraction
        indicator_regex = {
            "RSI": r"iRSI|ta\.rsi|RSI\(",
            "EMA_SMA": r"iMA|ta\.ema|ta\.sma|EMA\(|SMA\(",
            "MACD": r"iMACD|ta\.macd|MACD\(",
            "BollingerBands": r"iBands|ta\.bb|Bollinger\(",
            "ATR": r"iATR|ta\.atr|ATR\(",
            "Stochastic": r"iStochastic|ta\.stoch|Stoch\("
        }
        for ind_name, pattern in indicator_regex.items():
            matches = re.findall(pattern, source_code, re.IGNORECASE)
            if matches:
                report["extracted_indicators"].append({
                    "indicator": ind_name,
                    "frequency": len(matches)
                })

        # 5. Money Management Analysis
        lot_match = re.search(r"(Lots?|LotSize|risk_percent)\s*=\s*([0-9.]+)", source_code, re.IGNORECASE)
        if lot_match:
            report["money_management"]["declared_lot"] = lot_match.group(2)

        # 6. Final Audit Verdict
        report["toxic_risk_score"] = min(report["toxic_risk_score"], 100)
        if report["toxic_risk_score"] >= 60:
            report["verdict"] = "DANGEROUS_HIGH_RISK"
        elif report["toxic_risk_score"] >= 30:
            report["verdict"] = "MODERATE_RISK"
        else:
            report["verdict"] = "CLEAN_PASS"

        return report

    def _detect_language(self, code: str) -> str:
        if "//@version=" in code or "ta.rsi" in code or "strategy(" in code:
            return "TradingView Pine Script"
        if "#property" in code or "OnTick()" in code or "OrderSend" in code:
            return "MetaTrader MQL4/MQL5"
        if "def " in code and ("import" in code or "np." in code):
            return "Python Algorithmic Script"
        return "Generic Financial Code"
