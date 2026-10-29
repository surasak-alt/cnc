# -*- coding: utf-8 -*-
"""
Trading REA Providers Subsystem (2026-2036 Ideal Architecture)
Implements specialized analysis, adversarial war-room, simulation, and execution engines:
- MarketDecompiler (Phase 1 + Empirical Mining + Cross-Asset Radar)
- EmpiricalTraceEngine (Phase 2)
- CleanRoomSynthesizer (Phase 3)
- QuantumMonteCarloEngine (1,000-Path Vectorized NumPy Simulator)
- RedTeamAdversarialAgent (Market Maker Devil's Advocate)
- TruthGatekeeperFSM (Anti-Hallucination & Delta Gate)
- BayesianSelfEvolvingBrain (Post-Trade Autopsy & Dynamic Risk)
- BrokerBlindspotEngine
- EAStrategyDecompiler
"""

from .market_decompiler import MarketDecompiler
from .empirical_trace_engine import EmpiricalTraceEngine
from .broker_blindspot_engine import BrokerBlindspotEngine
from .clean_room_synthesizer import CleanRoomSynthesizer
from .ea_strategy_decompiler import EAStrategyDecompiler
from .quantum_monte_carlo import QuantumMonteCarloEngine
from .red_team_adversarial import RedTeamAdversarialAgent
from .truth_gatekeeper_fsm import TruthGatekeeperFSM
from .self_evolving_brain import BayesianSelfEvolvingBrain

__all__ = [
    "MarketDecompiler",
    "EmpiricalTraceEngine",
    "BrokerBlindspotEngine",
    "CleanRoomSynthesizer",
    "EAStrategyDecompiler",
    "QuantumMonteCarloEngine",
    "RedTeamAdversarialAgent",
    "TruthGatekeeperFSM",
    "BayesianSelfEvolvingBrain",
]
