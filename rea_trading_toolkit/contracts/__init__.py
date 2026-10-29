# -*- coding: utf-8 -*-
"""
Trading REA Contracts Package (2026-2036 Architecture)
Defines strict Pydantic schemas for the 3-Phase REA Architecture:
1. Phase 1: MarketAST (Decompiled Market Structure + Empirical Distribution + Cross-Asset Radar)
2. Phase 2: TradingEvidenceBundle (Empirical Evidence v2 + Red Team + Monte Carlo + Truth Gate)
3. Phase 3: CleanRoomOrder (Execution Synthesis)
"""

from .market_ast import (
    MarketAST,
    FairValueGap,
    LiquidityPool,
    SwingPoint,
    VolumeDeltaProfile,
    EmpiricalHabitDistribution,
    CrossAssetRadar,
)
from .evidence_bundle import (
    TradingEvidenceBundle,
    EvidenceFinding,
    AlgoClassification,
    RedTeamCritique,
    MonteCarloAudit,
    TruthGateAudit,
)
from .execution_order import CleanRoomOrder, AccountType, OrderAction

__all__ = [
    "MarketAST",
    "FairValueGap",
    "LiquidityPool",
    "SwingPoint",
    "VolumeDeltaProfile",
    "EmpiricalHabitDistribution",
    "CrossAssetRadar",
    "TradingEvidenceBundle",
    "EvidenceFinding",
    "AlgoClassification",
    "RedTeamCritique",
    "MonteCarloAudit",
    "TruthGateAudit",
    "CleanRoomOrder",
    "AccountType",
    "OrderAction",
]
