# -*- coding: utf-8 -*-
"""
Trading Evidence Bundle Contract (Evidence v2 - 2026-2036 Architecture)
Phase 2 of Trading REA: Provides empirical, non-hallucinatory proof,
Red Team Adversarial Critique, Vectorized Monte Carlo Audit, and Truth Gate Verification.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class EvidenceFinding(BaseModel):
    category: Literal[
        "STOP_HUNT_PIERCE",
        "VOLUME_ABSORPTION",
        "LIQUIDITY_PURGE",
        "SESSION_CHRONOS",
        "SMT_DIVERGENCE",
        "BROKER_ANOMALY",
        "STATISTICAL_DISTRIBUTION"
    ]
    metric_name: str
    observed_value: float
    benchmark_value: float
    description: str
    is_anomaly: bool = True


class AlgoClassification(BaseModel):
    algo_type: Literal[
        "JUDAS_SWING_STOP_RAID",
        "ICEBERG_ABSORPTION_WALL",
        "LIQUIDITY_VACUUM_MANIPULATION",
        "TWAP_VWAP_TREND_EXECUTION",
        "CHOP_ACCUMULATION_BOX"
    ]
    historical_win_probability: float = Field(ge=0.0, le=1.0)
    sample_size: int = Field(default=100, description="Number of historical setups mined")
    primary_intent: str = Field(description="Institutional intent behind the move")


class RedTeamCritique(BaseModel):
    """
    Adversarial Agent acting as the Institutional Market Maker trying to break our trade.
    """
    attack_vectors: List[str] = Field(default_factory=list)
    vulnerability_score: float = Field(ge=0.0, le=1.0, description="0.0 = Invulnerable, 1.0 = Fatal Trap")
    recommended_sl_adjustment_atr: float = Field(default=0.0, description="Extra ATR buffer demanded by Red Team")
    veto_triggered: bool = Field(default=False, description="True if Red Team proves setup is a retail trap")
    adversarial_verdict: str


class MonteCarloAudit(BaseModel):
    """
    Vectorized NumPy 1,000-Path Stochastic Simulation with Spread & Slippage Stress.
    """
    total_paths: int = 1000
    execution_time_ms: float = Field(description="Execution latency in milliseconds (0 tokens)")
    simulated_winrate_pct: float
    expected_value_r: float
    stress_test_spread_shock_pts: float
    survived_stress_test: bool


class TruthGateAudit(BaseModel):
    """
    Deterministic Anti-Hallucination & Anti-Bias Gatekeeper + FSM State.
    """
    is_verified_zero_hallucination: bool = True
    cross_checked_metrics_count: int = 0
    mismatches_found: List[str] = Field(default_factory=list)
    fsm_state: Literal["IDLE", "DECOMPILED", "EVIDENCE_VERIFIED", "PENDING_ARMED", "BLOCKED_BY_GATE"]


class TradingEvidenceBundle(BaseModel):
    bundle_id: str = Field(description="Unique Evidence Hash e.g. EV-XAUUSD-20261029-0955")
    symbol: str
    timeframe: str
    generated_at: str
    phase: Literal["UNDERSTAND"] = "UNDERSTAND"
    
    # 1. Concrete Empirical Evidence
    findings: List[EvidenceFinding] = Field(default_factory=list)
    
    # 2. Classified Institutional Algorithmic Signature
    algo_footprint: AlgoClassification
    
    # 3. 2026-2036 War-Room Audits
    red_team_critique: RedTeamCritique
    monte_carlo_audit: MonteCarloAudit
    truth_gate_audit: TruthGateAudit
    
    # 4. Confidence & Limitations (Crucial REA Concept)
    confidence_score: float = Field(ge=0.0, le=1.0, description="Calculated statistical confidence")
    known_limitations: List[str] = Field(default_factory=list, description="Explicit unknowns e.g. upcoming news, low volume")
    
    # 5. Final Verdict
    verdict: Literal["SNIPER_SETUP_CONFIRMED", "WAIT_FOR_MORE_EVIDENCE", "REJECT_RISK_EXCEEDED"]
    reasoning_summary: str
