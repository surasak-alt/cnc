# -*- coding: utf-8 -*-
"""
Bayesian Self-Evolving Brain & Post-Trade Autopsy Provider (2026-2036 Architecture)
Allows Trading REA to continuously learn from post-trade outcomes, update Bayesian
weights in evidence_vault/bayesian_memory.json, and dynamically scale risk (0.5% - 1.5%).
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


class BayesianSelfEvolvingBrain:
    def __init__(self, symbol: str = "XAUUSD"):
        self.symbol = symbol
        self.vault_dir = Path(__file__).resolve().parent.parent / "evidence_vault"
        self.vault_dir.mkdir(exist_ok=True)
        self.memory_file = self.vault_dir / "bayesian_memory.json"
        self.memory = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.memory_file.exists():
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "generation": 1,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "algo_weights": {
                "JUDAS_SWING_STOP_RAID": {"wins": 28, "losses": 6, "bayesian_weight": 1.24},
                "ICEBERG_ABSORPTION_WALL": {"wins": 24, "losses": 6, "bayesian_weight": 1.20},
                "LIQUIDITY_VACUUM_MANIPULATION": {"wins": 18, "losses": 7, "bayesian_weight": 1.08},
                "TWAP_VWAP_TREND_EXECUTION": {"wins": 20, "losses": 7, "bayesian_weight": 1.12},
                "CHOP_ACCUMULATION_BOX": {"wins": 8, "losses": 12, "bayesian_weight": 0.60},
            },
            "autopsy_history": []
        }

    def save(self) -> None:
        self.memory["updated_at"] = datetime.now(timezone.utc).isoformat()
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    def record_post_trade_autopsy(
        self,
        algo_type: str,
        outcome: str,
        realized_r: float,
        observed_pierce_atr: float,
        notes: str
    ) -> Dict[str, Any]:
        """
        Updates Bayesian posterior weights after a trade closes.
        """
        rec = self.memory["algo_weights"].get(
            algo_type, {"wins": 10, "losses": 5, "bayesian_weight": 1.0}
        )
        if outcome.upper() == "WIN":
            rec["wins"] += 1
        else:
            rec["losses"] += 1

        total = max(rec["wins"] + rec["losses"], 1)
        win_rate = rec["wins"] / total
        rec["bayesian_weight"] = round(float(max(0.50, min(1.50, win_rate * 1.55))), 2)
        self.memory["algo_weights"][algo_type] = rec
        self.memory["generation"] += 1

        autopsy_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "algo_type": algo_type,
            "outcome": outcome.upper(),
            "realized_r": realized_r,
            "observed_pierce_atr": observed_pierce_atr,
            "updated_bayesian_weight": rec["bayesian_weight"],
            "notes": notes
        }
        self.memory["autopsy_history"].append(autopsy_entry)
        self.memory["autopsy_history"] = self.memory["autopsy_history"][-100:]
        self.save()
        return autopsy_entry

    def get_dynamic_risk_allocation(self, algo_type: str, confidence_score: float) -> Dict[str, Any]:
        """
        Determines optimal risk percentage (0.5%, 1.0%, or 1.5%) based on Bayesian weight and confidence.
        """
        rec = self.memory["algo_weights"].get(algo_type, {"wins": 10, "losses": 5, "bayesian_weight": 1.0})
        w = rec["bayesian_weight"]
        adjusted_conf = min(0.98, confidence_score * (0.85 + 0.15 * w))

        if adjusted_conf >= 0.85 and w >= 1.15:
            risk_pct = 1.5
            tier = "A+ SOVEREIGN SNIPER"
        elif adjusted_conf >= 0.75:
            risk_pct = 1.0
            tier = "A INSTITUTIONAL STANDARD"
        elif adjusted_conf >= 0.65:
            risk_pct = 0.5
            tier = "B DEFENSIVE PROBE"
        else:
            risk_pct = 0.0
            tier = "C CAPITAL LOCK (NO TRADE)"

        return {
            "algo_type": algo_type,
            "bayesian_weight": w,
            "adjusted_confidence": round(adjusted_conf, 3),
            "recommended_risk_percent": risk_pct,
            "setup_tier": tier,
            "brain_generation": self.memory["generation"]
        }
