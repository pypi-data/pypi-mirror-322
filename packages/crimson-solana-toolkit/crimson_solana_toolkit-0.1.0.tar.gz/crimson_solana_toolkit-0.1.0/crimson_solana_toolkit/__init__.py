"""
Crimson Solana Toolkit - A comprehensive toolkit for Solana blockchain operations
integrated with the Crimson Agent ecosystem.
"""

from .agent import SolanaAgent
from .programs import (
    MemoProgram,
    TokenProgram,
    NFTProgram,
    DeFiProgram,
    GovernanceProgram,
    StakingProgram
)
from .tools import (
    BlockchainAnalytics,
    TokenAnalytics,
    NFTAnalytics,
    DeFiAnalytics,
    GovernanceAnalytics
)

__version__ = "0.1.0"
__author__ = "Crimson AI Team"
__email__ = "team@crimson.ai"

__all__ = [
    # Core
    "SolanaAgent",
    
    # Programs
    "MemoProgram",
    "TokenProgram",
    "NFTProgram",
    "DeFiProgram",
    "GovernanceProgram",
    "StakingProgram",
    
    # Analytics
    "BlockchainAnalytics",
    "TokenAnalytics",
    "NFTAnalytics",
    "DeFiAnalytics",
    "GovernanceAnalytics",
]

# Package metadata
PACKAGE_NAME = "crimson_solana_toolkit"
DESCRIPTION = "A comprehensive Solana blockchain toolkit for the Crimson Agent ecosystem"
REPOSITORY = "https://github.com/crimson-ai/crimson-solana-toolkit"
DOCUMENTATION = "https://crimson-solana-toolkit.readthedocs.io/"
