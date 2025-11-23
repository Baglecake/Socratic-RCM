# Agent System

This directory contains the agent infrastructure for transforming PRAR canvas definitions into executable simulation participants.

## Status

**Phase 1: Core Implementation Complete**

The agent layer provides the bridge from PRAR (design) to simulation (execution).

## Structure

```
agents/
├── agent_config.py       # AgentConfig, AgentResponse, RoundConfig dataclasses
├── agent_factory.py      # Factory for instantiating agents from canvas
├── agent_runner.py       # Runtime for executing multi-agent simulations
├── persona_library/      # Reusable persona templates (planned)
├── ces_generators/       # CES-to-agent transformation (Phase 4)
└── README.md
```

## Core Components

### AgentConfig

Configuration dataclass for simulation agents:

```python
@dataclass
class AgentConfig:
    identifier: str      # e.g., "Worker+Alice"
    role: str            # e.g., "Worker"
    name: str            # e.g., "Alice"
    goal: str            # Agent's objective
    persona: str         # Behavioral description
    prompt: str          # Compiled system prompt
    model: str           # LLM model identifier
    temperature: float   # Generation temperature (0.0-1.0)
    max_tokens: int      # Response length limit
    behaviors: dict      # Conditional behavior rules
```

### AgentFactory

Factory for creating agents from canvas definitions:

```python
from agent_factory import AgentFactory

# Load from state file
factory = AgentFactory.from_state_file("path/to/state.json")

# Create individual agents
alice = factory.create("Worker+Alice")
marta = factory.create("Owner+Marta")

# Create all agents
agents = factory.create_all()

# Get round participants
round1_agents = factory.get_round_participants(1)

# Print canvas summary
print(factory.summary())
```

### AgentRunner

Runtime for executing multi-agent simulations:

```python
from agent_runner import AgentRunner, run_simulation
from agent_factory import AgentFactory
from llm_client import create_llm_client

# Quick simulation
transcripts = run_simulation(
    state_path="state.json",
    output_dir="outputs/",
    provider="mock",  # or "vllm", "openai"
    max_turns=15
)

# Manual control
factory = AgentFactory.from_state_file("state.json")
llm = create_llm_client("vllm", base_url="http://localhost:8000/v1")
runner = AgentRunner(factory, llm)

transcript = runner.execute_round(1)
runner.save_transcript(transcript, "round1.json")
```

## Command Line Usage

```bash
# Mock mode (testing)
python agent_runner.py \
  --state ../prar/outputs/2025-11-23_baseline_full_qwen/state.json \
  --output ./simulation_output \
  --max-turns 15

# With vLLM backend
python agent_runner.py \
  --state ../prar/outputs/2025-11-23_baseline_full_qwen/state.json \
  --output ./simulation_output \
  --provider vllm \
  --base-url http://localhost:8000/v1 \
  --model Qwen/Qwen2.5-7B-Instruct
```

## Output Format

Each round produces a transcript JSON:

```json
{
  "round_number": 1,
  "round_config": { ... },
  "messages": [
    {
      "agent_id": "Worker+Alice",
      "content": "...",
      "turn_number": 1,
      "timestamp": 1700000000.0
    }
  ],
  "duration_seconds": 12.5
}
```

## Integration with Dual-LLM Architecture

In the planned dual-LLM architecture (Phase 2):

- **Coach (PRAR)**: Validates agent outputs, enforces behavioral constraints
- **Performer (Agent)**: Executes agent personas via AgentRunner

The current AgentRunner provides the Performer execution layer. Coach integration will add validation hooks between turns.

## Roadmap

- [x] AgentConfig dataclass with canvas parsing
- [x] AgentFactory with state file loading
- [x] AgentRunner with round execution
- [x] Transcript generation and export
- [ ] Persona library templates
- [ ] Coach integration (Phase 2)
- [ ] Behavioral metrics extraction (Phase 3)
- [ ] CES agent generation (Phase 4)

## See Also

- [ROADMAP.md](../ROADMAP.md) - Development phases
- [prar/README.md](../prar/README.md) - PRAR methodology
- [local_rcm/README.md](../local_rcm/README.md) - Orchestrator documentation
