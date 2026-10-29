# -*- coding: utf-8 -*-
"""
Market AST (Abstract Syntax Tree) Contract
Phase 1 of Trading REA: Decompiles unstructured candlestick/tick feeds
into formal structured market primitives + Real-Time Empirical Habit Distribution.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class SwingPoint(BaseModel):
    kind: Literal["SWING_HIGH", "SWING_LOW"]
    price: float
    bar_index: int
    timestamp: str
    strength: int = Field(default=3, description="Number of confirming bars on each side")
    is_swept: bool = Field(default=False, description="Whether liquidity above/below was purged")


class FairValueGap(BaseModel):
    gap_type: Literal["BULLISH_FVG", "BEARISH_FVG"]
    top_price: float
    bottom_price: float
    equilibrium_ce: float = Field(description="50% Consequent Encroachment Level")
    bar_index: int
    timestamp: str
    is_filled: bool = False
    volume_quality: float = Field(default=1.0, description="Relative tick volume backing the displacement")


class LiquidityPool(BaseModel):
    pool_type: Literal["BUY_SIDE_LIQUIDITY", "SELL_SIDE_LIQUIDITY"]
    level: float
    touch_count: int = Field(default=1, description="Number of touches creating retail stop accumulation")
    estimated_stop_density: str = Field(default="MEDIUM", description="LOW, MEDIUM, HIGH, INSANE")
    is_purged: bool = False


class VolumeDeltaProfile(BaseModel):
    effort_vs_result_ratio: float = Field(description="Body size relative to tick volume. <0.65 = Hollow, >1.5 = Ultra Absorption")
    tick_velocity_anomaly: bool = Field(default=False, description="Sudden burst in ticks/sec")
    absorption_detected: bool = Field(default=False, description="Large volume with minimal price movement")


class EmpiricalHabitDistribution(BaseModel):
    """
    Scientifically mined statistical distribution from actual historical bars (No hardcoded guessing).
    """
    bars_analyzed: int
    sweep_sample_size: int = Field(description="Total number of historical swing breaches found (N)")
    mean_pierce_atr: float = Field(description="Empirical Mean (mu) of stop-hunt pierce in ATR units")
    std_pierce_atr: float = Field(description="Empirical Standard Deviation (sigma) in ATR units")
    p95_safe_sl_atr: float = Field(description="95th Percentile pierce depth (mu + 1.65*sigma or empirical P95)")
    anomaly_vol_reversal_rate: float = Field(description="Win rate when sweep occurs on Volume Vacuum/Absorption")
    normal_vol_reversal_rate: float = Field(description="Win rate when sweep occurs on normal volume")
    z_score_stat: float = Field(description="Two-proportion Z-test statistic proving edge over random")
    p_value: float = Field(description="Statistical p-value (< 0.05 means statistically significant)")
    is_statistically_significant: bool = Field(description="True if N >= 20 and p_value < 0.05")


class CrossAssetRadar(BaseModel):
    """
    Synchronizes XAUUSD with correlated macro assets (XAGUSD, EURUSD, USDJPY).
    """
    smt_divergence_detected: bool = False
    divergent_asset: Optional[str] = None
    macro_alignment_score: float = Field(default=0.5, description="-1.0 (Bearish) to +1.0 (Bullish)")
    description: str = "NEUTRAL_SYNCHRONIZATION"


class MarketAST(BaseModel):
    symbol: str
    timeframe: str
    decompiled_at: str
    current_bid: float
    current_ask: float
    spread_ticks: float
    atr_14: float
    market_regime: Literal["EXPANSION", "RETRACEMENT", "REVERSAL", "CONSOLIDATION_CHOP"]
    swing_points: List[SwingPoint] = Field(default_factory=list)
    active_fvgs: List[FairValueGap] = Field(default_factory=list)
    liquidity_pools: List[LiquidityPool] = Field(default_factory=list)
    volume_delta: VolumeDeltaProfile
    empirical_distribution: EmpiricalHabitDistribution
    cross_asset_radar: CrossAssetRadar
    notes: List[str] = Field(default_factory=list)
