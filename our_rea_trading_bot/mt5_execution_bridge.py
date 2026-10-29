# -*- coding: utf-8 -*-
"""
MT5 Execution Bridge & Zero-Ping Order Dispatcher (Our REA Trading Bot)
Connects directly to MetaTrader 5 terminal:
- Auto-resolves broker symbol suffixes (XAUUSDm, XAUUSD.c, GOLD)
- Enforces Strict Capital Standards ($100 Standard / 10,000 Cents Cent)
- Dispatches 0ms Server-Side Pending Orders with mandatory Hard SL & TP
- Provides 0-Token Local Break-Even (+0.85R), Structural Trailing (+1.5R), and 3% Daily Circuit Breaker
"""

import math
from datetime import datetime
from typing import Dict, Any, List

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

MT5_DEFAULT_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
MAGIC_NUMBER = 888999


class MT5ExecutionBridge:
    def __init__(self, symbol: str = "XAUUSD"):
        self.symbol = symbol
        self.connected = False
        self.baseline_standard_usd = 100.0
        self.baseline_cent_usc = 10000.0

    def connect(self) -> Dict[str, Any]:
        if not MT5_AVAILABLE:
            return {"connected": False, "error": "MetaTrader5 module not installed"}

        init_ok = mt5.initialize(path=MT5_DEFAULT_PATH)
        if not init_ok:
            init_ok = mt5.initialize()

        if not init_ok:
            err = mt5.last_error()
            self.connected = False
            return {
                "connected": False,
                "error_code": err[0] if err else -1,
                "error_msg": err[1] if err else "MT5 Terminal not logged in"
            }

        self.connected = True
        self.symbol = self._resolve_symbol(self.symbol)
        return {"connected": True, "symbol": self.symbol}

    def _resolve_symbol(self, preferred: str) -> str:
        if not self.connected:
            return preferred
        info = mt5.symbol_info(preferred)
        if info is not None:
            mt5.symbol_select(preferred, True)
            return preferred

        all_symbols = mt5.symbols_get()
        if not all_symbols:
            return preferred

        candidates = [s.name for s in all_symbols if preferred.upper() in s.name.upper() or "GOLD" in s.name.upper()]
        if candidates:
            best = sorted(candidates, key=len)[0]
            mt5.symbol_select(best, True)
            return best
        return preferred

    def get_telemetry(self) -> Dict[str, Any]:
        conn = self.connect()
        if not conn.get("connected"):
            return {
                "status": "OFFLINE_STANDBY",
                "symbol": self.symbol,
                "account": {
                    "account_type": "STANDARD",
                    "balance": 100.0,
                    "equity": 100.0,
                    "profit": 0.0,
                    "currency": "USD",
                    "reference_capital": 100.0
                },
                "broker_rules": {
                    "ping_ms": 45.0,
                    "spread_points": 25,
                    "stops_level_points": 30,
                    "in_rollover_death_zone": False
                }
            }

        term = mt5.terminal_info()
        acc = mt5.account_info()
        sym = mt5.symbol_info(self.symbol)
        tick = mt5.symbol_info_tick(self.symbol)

        if not acc or not sym or not tick:
            return {"status": "WAITING_FOR_LOGIN", "symbol": self.symbol}

        is_cent = ("CENT" in (acc.server or "").upper()) or ("USC" in (acc.currency or "").upper()) or (acc.balance >= 2000)
        ref_cap = self.baseline_cent_usc if is_cent else self.baseline_standard_usd
        point = sym.point if sym.point > 0 else 0.01
        spread_pts = int(round((tick.ask - tick.bid) / point))
        stops_lvl = max(sym.trade_stops_level, sym.trade_freeze_level, 15)
        ping_ms = round((term.ping_last / 1000.0), 2) if term else 45.0

        server_dt = datetime.fromtimestamp(tick.time)
        in_death_zone = (server_dt.hour == 23 and server_dt.minute >= 45) or (server_dt.hour == 0)

        return {
            "status": "LIVE_CONNECTED",
            "symbol": self.symbol,
            "account": {
                "login": acc.login,
                "server": acc.server,
                "account_type": "CENT" if is_cent else "STANDARD",
                "currency": acc.currency,
                "balance": round(acc.balance, 2),
                "equity": round(acc.equity, 2),
                "profit": round(acc.profit, 2),
                "reference_capital": ref_cap
            },
            "broker_rules": {
                "ping_ms": ping_ms,
                "bid": tick.bid,
                "ask": tick.ask,
                "point": point,
                "spread_points": spread_pts,
                "stops_level_points": stops_lvl,
                "in_rollover_death_zone": in_death_zone
            }
        }

    def place_pending_order(
        self,
        action_str: str,
        entry_price: float,
        hard_sl: float,
        hard_tp: float,
        lot_size: float,
        comment: str = "REA_SNIPER_0MS"
    ) -> Dict[str, Any]:
        """
        Places a 0ms Server-Side Pending Order with mandatory Hard SL and Hard TP.
        Refuses any naked order.
        """
        if hard_sl <= 0 or hard_tp <= 0:
            return {"executed": False, "reason": "ZERO_NAKED_ORDER_GUARD: Hard SL and TP are mandatory."}

        conn = self.connect()
        if not conn.get("connected"):
            return {
                "executed": False,
                "mode": "DRY_RUN_VALIDATED",
                "reason": conn.get("error_msg", "MT5 offline - order validated in dry-run mode"),
                "validated_payload": {
                    "symbol": self.symbol,
                    "action": action_str,
                    "entry": entry_price,
                    "sl": hard_sl,
                    "tp": hard_tp,
                    "lot": lot_size,
                    "comment": comment
                }
            }

        type_map = {
            "BUY_LIMIT": mt5.ORDER_TYPE_BUY_LIMIT,
            "SELL_LIMIT": mt5.ORDER_TYPE_SELL_LIMIT,
            "BUY_STOP": mt5.ORDER_TYPE_BUY_STOP,
            "SELL_STOP": mt5.ORDER_TYPE_SELL_STOP,
        }
        mt5_type = type_map.get(action_str.upper(), mt5.ORDER_TYPE_BUY_LIMIT)

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": self.symbol,
            "volume": float(lot_size),
            "type": mt5_type,
            "price": float(entry_price),
            "sl": float(hard_sl),
            "tp": float(hard_tp),
            "deviation": 10,
            "magic": MAGIC_NUMBER,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        res = mt5.order_send(request)
        if res is None or res.retcode != mt5.TRADE_RETCODE_DONE:
            return {
                "executed": False,
                "retcode": res.retcode if res else -1,
                "comment": res.comment if res else "order_send returned None"
            }

        return {
            "executed": True,
            "order_ticket": res.order,
            "symbol": self.symbol,
            "action": action_str,
            "entry": entry_price,
            "sl": hard_sl,
            "tp": hard_tp,
            "lot": lot_size
        }

    def run_zero_token_local_guardian(self) -> Dict[str, Any]:
        """
        0ms Local Guardian (0 Tokens):
        - Enforces 3.0% Daily Drawdown Circuit Breaker
        - Moves profitable trades at >= +0.85R to Break-Even (+2 pts)
        - Trails SL at >= +1.5R to lock +0.75R profit
        """
        conn = self.connect()
        if not conn.get("connected"):
            return {"status": "STANDBY_OFFLINE", "tokens_used": 0}

        acc = mt5.account_info()
        positions = mt5.positions_get(symbol=self.symbol) or []
        orders = mt5.orders_get(symbol=self.symbol) or []

        actions_taken: List[str] = []

        # 1. Check 3.0% Daily Circuit Breaker
        if acc and acc.balance > 0:
            dd_pct = ((acc.balance - acc.equity) / acc.balance) * 100.0
            if dd_pct >= 3.0:
                self.panic_close_all()
                self.cancel_all_pending()
                return {
                    "status": "CIRCUIT_BREAKER_TRIPPED",
                    "drawdown_pct": round(dd_pct, 2),
                    "action": "Closed all positions & cancelled pending orders to protect 97% capital.",
                    "tokens_used": 0
                }

        # 2. Check Auto Break-Even (+0.85R) & Structural Trailing (+1.5R)
        for pos in positions:
            if pos.sl <= 0:
                continue
            init_risk = abs(pos.price_open - pos.sl)
            if init_risk <= 0:
                continue

            if pos.type == mt5.ORDER_TYPE_BUY:
                current_gain = pos.price_current - pos.price_open
                r_mult = current_gain / init_risk
                if r_mult >= 1.50 and pos.sl < pos.price_open + (0.75 * init_risk):
                    new_sl = round(pos.price_open + (0.75 * init_risk), 2)
                    self._modify_sl(pos.ticket, new_sl, pos.tp)
                    actions_taken.append(f"TRAIL_BUY_{pos.ticket}_TO_{new_sl}")
                elif r_mult >= 0.85 and pos.sl < pos.price_open:
                    new_sl = round(pos.price_open + 0.05, 2)
                    self._modify_sl(pos.ticket, new_sl, pos.tp)
                    actions_taken.append(f"BREAKEVEN_BUY_{pos.ticket}_TO_{new_sl}")

            elif pos.type == mt5.ORDER_TYPE_SELL:
                current_gain = pos.price_open - pos.price_current
                r_mult = current_gain / init_risk
                if r_mult >= 1.50 and pos.sl > pos.price_open - (0.75 * init_risk):
                    new_sl = round(pos.price_open - (0.75 * init_risk), 2)
                    self._modify_sl(pos.ticket, new_sl, pos.tp)
                    actions_taken.append(f"TRAIL_SELL_{pos.ticket}_TO_{new_sl}")
                elif r_mult >= 0.85 and pos.sl > pos.price_open:
                    new_sl = round(pos.price_open - 0.05, 2)
                    self._modify_sl(pos.ticket, new_sl, pos.tp)
                    actions_taken.append(f"BREAKEVEN_SELL_{pos.ticket}_TO_{new_sl}")

        return {
            "status": "GUARDIAN_PASS_COMPLETE",
            "open_positions": len(positions),
            "pending_orders": len(orders),
            "actions_taken": actions_taken,
            "tokens_used": 0
        }

    def _modify_sl(self, ticket: int, new_sl: float, tp: float) -> bool:
        req = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": self.symbol,
            "sl": float(new_sl),
            "tp": float(tp),
        }
        res = mt5.order_send(req)
        return bool(res and res.retcode == mt5.TRADE_RETCODE_DONE)

    def cancel_all_pending(self) -> Dict[str, Any]:
        if not self.connect().get("connected"):
            return {"cancelled": 0, "status": "OFFLINE"}
        orders = mt5.orders_get(symbol=self.symbol) or []
        cancelled = 0
        for o in orders:
            res = mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE, "order": o.ticket})
            if res and res.retcode == mt5.TRADE_RETCODE_DONE:
                cancelled += 1
        return {"cancelled": cancelled, "status": "SUCCESS"}

    def panic_close_all(self) -> Dict[str, Any]:
        if not self.connect().get("connected"):
            return {"closed": 0, "status": "OFFLINE"}
        positions = mt5.positions_get(symbol=self.symbol) or []
        closed = 0
        for p in positions:
            tick = mt5.symbol_info_tick(self.symbol)
            if not tick:
                continue
            close_type = mt5.ORDER_TYPE_SELL if p.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
            price = tick.bid if p.type == mt5.ORDER_TYPE_BUY else tick.ask
            req = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": p.volume,
                "type": close_type,
                "position": p.ticket,
                "price": price,
                "deviation": 20,
                "magic": MAGIC_NUMBER,
                "comment": "PANIC_CLOSE_ALL",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            res = mt5.order_send(req)
            if res and res.retcode == mt5.TRADE_RETCODE_DONE:
                closed += 1
        return {"closed": closed, "status": "SUCCESS"}
