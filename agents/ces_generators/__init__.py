"""
CES Agent Generators

Transforms CES (Canadian Election Study) survey data into dynamically-configured
agents for Social RL simulations.

Key principle: Agents are NOT static personas. They are dynamically generated
from CES variables, with the ContextInjector providing turn-by-turn adaptation.
"""

from .row_to_agent import (
    CESAgentConfig,
    ces_row_to_agent,
    ces_cluster_to_prototype,
    CESVariableMapper,
)

__all__ = [
    "CESAgentConfig",
    "ces_row_to_agent",
    "ces_cluster_to_prototype",
    "CESVariableMapper",
]
