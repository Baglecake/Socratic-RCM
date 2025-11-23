# Agent System

This directory contains the agent infrastructure for transforming PRAR canvas definitions into executable simulation participants.

## Status

**Phase 1: In Development**

The agent layer is the bridge from PRAR (design) to simulation (execution).

## Planned Structure

```
agents/
├── agent_config.py       # AgentConfig dataclass
├── agent_factory.py      # Factory for instantiating agents from canvas
├── persona_library/      # Reusable persona templates
│   ├── worker.json
│   ├── owner.json
│   └── analyst.json
├── ces_generators/       # CES-to-agent transformation (Phase 4)
│   └── row_to_agent.py
└── README.md
```

## AgentConfig (Planned)

```python
@dataclass
class AgentConfig:
    identifier: str      # e.g., "Worker+Alice"
    role_prompt: str     # Compiled from canvas agent definition
    goal: str            # Agent's objective
    persona: str         # Behavioral description
    model: str           # LLM model identifier
    temperature: float   # Generation temperature (0.0-1.0)
    max_tokens: int      # Response length limit
    behaviors: dict      # Conditional behavior rules (optional)
```

## AgentFactory (Planned)

```python
from canvas_state import CanvasState

factory = AgentFactory(canvas)

# Create individual agents
alice = factory.create("Worker+Alice")
marta = factory.create("Owner+Marta")

# Create all agents from canvas
agents = factory.create_all()
```

## Integration with Dual-LLM

In the dual-LLM architecture:

- **Coach (PRAR)**: Validates and scaffolds
- **Performer (Agent)**: Executes agent behavior

AgentConfig defines *what* the performer should do. The AgentFactory produces callable agents that can be invoked by the simulation runner.

## CES Agent Generation (Phase 4)

Future capability to generate agents from Canadian Election Study data:

```python
from ces_generators import row_to_agent

ces_row = {
    "age": 55,
    "region": "Atlantic",
    "income": 40000,
    "party_id": "Liberal",
    "education": "BA",
    "gender": "Woman",
    "political_interest": "Low"
}

agent = row_to_agent(ces_row)
# Returns AgentConfig with generated persona
```

## See Also

- [ROADMAP.md](../ROADMAP.md) - Development phases
- [prar/README.md](../prar/README.md) - PRAR methodology
- [local_rcm/README.md](../local_rcm/README.md) - Orchestrator documentation
