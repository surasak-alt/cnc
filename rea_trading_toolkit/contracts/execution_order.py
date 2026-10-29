# -*- coding: utf-8 -*-
"""
Execution Order Contract
Phase 3 of Trading REA: Synthesizes a clean-room counter-execution order
based strictly on the Evidence Bundle.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class AccountType(str):
    STANDARD = "STANDARD"
    CENT = "CENT"


class OrderAction(str):
    BUY_LIMIT = "BUY_LIMIT"
    SELL_LIMIT = "SELL_LIMIT"
    BUY_STOP = "BUY_STOP"
    SELL_STOP = "SELL_STOP"


class CleanRoomOrder(BaseModel):
    order_id: str
    symbol: str
    action: Literal["BUY_LIMIT", "SELL_LIMIT", "BUY_STOP", "SELL_STOP"]
    entry_price: float
    hard_sl: float
    hard_tp: float
    lot_size: float
    risk_percent: float = Field(default=1.0, description="Risk % of capital")
    risk_amount_money: float = Field(description="Strict monetary risk (e.g. $1.00 or 100 Cents)")
    account_type: Literal["STANDARD", "CENT"] = "STANDARD"
    base_capital: float = Field(default=100.0, description="$100 Standard or 10,000 Cents")
    
    # REA Protection Parameters
    spread_compensation_ticks: float = Field(default=0.0)
    stop_hunt_sl_buffer_atr: float = Field(default=0.78, description="95th percentile pierce buffer")
    zero_ping_server_side: bool = True
    evidence_bundle_ref: str = Field(description="ID of evidence bundle authorizing this trade")
    
    # Expected Metrics
    risk_reward_ratio: float
    notes: Optional[str] = None
