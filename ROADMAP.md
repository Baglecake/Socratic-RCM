# Development Roadmap

This document outlines the phased development plan for Socratic-RCM, from the current stable baseline through to a publishable dual-LLM simulation engine.

## Current State

**Phase 0: Core Infrastructure** - COMPLETE

- Working PRAR/RCM workflow with vLLM/Qwen
- Full 112-step baseline experiment validated
- Canvas data model with JSON export
- Experiment versioning infrastructure
- Clean repository structure

---

## Phase 1: Agent Layer

**Status:** Next priority

**Goal:** Transform canvas agent definitions into executable simulation participants.

### Components

**AgentConfig**
```python
@dataclass
class AgentConfig:
    identifier: str      # e.g., "Worker+Alice"
    role_prompt: str     # Compiled from canvas
    model: str           # LLM model identifier
    temperature: float   # Generation temperature
    max_tokens: int      # Response length limit
```

**AgentFactory**
```python
factory = AgentFactory(canvas)
alice = factory.create("Worker+Alice")
marta = factory.create("Owner+Marta")
```

### Deliverables

- [ ] `agents/agent_config.py` - AgentConfig dataclass
- [ ] `agents/agent_factory.py` - Factory for instantiating agents from canvas
- [ ] `agents/persona_library/` - Reusable persona templates
- [ ] Integration tests with mock LLM

### Why This Matters

This is the bridge from PRAR (design) to simulation (execution). Without executable agents, the canvas remains a static document.

---

## Phase 2: Dual-LLM Architecture

**Status:** Planned

**Goal:** Separate cognitive governance (Coach) from agent behavior (Performer).

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐              ┌─────────────┐         │
│   │   Coach     │              │  Performer  │         │
│   │   (PRAR)    │              │  (Agent)    │         │
│   │             │              │             │         │
│   │ - Validates │              │ - Acts as   │         │
│   │ - Questions │              │   persona   │         │
│   │ - Enforces  │              │ - Generates │         │
│   │   rules     │              │   dialogue  │         │
│   │             │              │             │         │
│   │ Low temp    │              │ Higher temp │         │
│   │ (0.0-0.2)   │              │ (0.5-0.8)   │         │
│   └─────────────┘              └─────────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Configuration

```json
{
  "coach": {
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "temperature": 0.1,
    "role": "PRAR validator and question generator"
  },
  "performer": {
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "temperature": 0.7,
    "role": "Agent persona execution"
  }
}
```

### Rationale

A single model cannot simultaneously:
- Follow strict PRAR protocol (discipline)
- Authentically embody a simulated persona (expression)

Separating these roles enables reliable governance AND authentic behavior.

### Deliverables

- [ ] `dual_llm/coach.py` - PRAR validation and questioning
- [ ] `dual_llm/performer.py` - Agent persona execution
- [ ] `dual_llm/pipeline.py` - Coordinated execution flow
- [ ] Configuration schema for dual-model setups

---

## Phase 3: Interaction Simulation

**Status:** Planned

**Goal:** Execute multi-agent rounds with transcript logging and behavioral metrics.

### SimulationRunner

```python
runner = SimulationRunner(
    canvas=canvas,
    coach=coach_model,
    performers=agent_factory
)

for round_num in range(1, canvas.rounds_count + 1):
    transcript = runner.execute_round(round_num)
    runner.save_transcript(f"round{round_num}_transcript.json")
```

### Outputs

```
experiments/YYYY-MM-DD_simulation/
├── round1_transcript.json
├── round2_transcript.json
├── round3_transcript.json
├── behavioral_metrics.json
└── analysis_notes.md
```

### Behavioral Metrics

- Message sentiment
- Assertiveness indicators
- Compliance patterns
- Conflict triggers
- Thematic markers (alienation, domination, etc.)

### Deliverables

- [ ] `local_rcm/simulation_runner.py`
- [ ] Transcript logging format
- [ ] Basic behavioral metrics extraction
- [ ] Round-by-round execution with pause points

---

## Phase 4: CES Agent Generator

**Status:** Future

**Goal:** Generate synthetic survey respondents from Canadian Election Study data.

### Concept

Transform CES demographic/attitudinal rows into parameterized agent configurations:

```
CES Row:
  Age: 55
  Region: Atlantic
  Income: 40k
  PartyID: Liberal
  Education: BA
  Gender: Woman
  Political Interest: Low

→ AgentConfig:
  persona: "You are a 55-year-old woman from the Atlantic region..."
  behavioral_priors: "Low political engagement, moderate consistency..."
  voting_history: "Liberal-leaning with occasional strategic voting..."
```

### Applications

- Synthetic survey response generation
- Public opinion simulation
- Electoral behavior modeling
- Policy reaction prediction

### Deliverables

- [ ] `agents/ces_generators/row_to_agent.py`
- [ ] CES variable mapping schema
- [ ] Persona generation templates
- [ ] Validation against actual CES distributions

---

## Phase 5: Emergent Behavior (Optional)

**Status:** Research direction

**Goal:** Incorporate distinction mechanics from theoretical frameworks.

### Concepts

- Surplus-driven agent conflict
- Recursive distinction states
- Field presence as contextual influence
- Phase-shift dynamics in persuasion

This phase represents theoretical extension rather than core functionality.

---

## Phase 6: Publication

**Status:** Long-term goal

### Outputs

1. **Paper**: "PRAR-Guided Dual-LLM Agent Simulations: A Framework for Computational Sociology"

2. **Tool**: Socratic-RCM Lab - unified execution interface

3. **Dataset**: Synthetic CES simulation corpus

4. **Reproducibility Package**: Notebooks, configs, and documentation

### Positioning

This work sits at the intersection of:
- Computational social science
- Multi-agent LLM systems
- Pedagogical AI
- Simulation methodology

The combination of PRAR (structured governance) with dual-LLM agent simulation is novel in the literature.

---

## Implementation Priority

| Phase | Priority | Dependency | Estimated Complexity |
|-------|----------|------------|---------------------|
| 1 | HIGH | None | Medium |
| 2 | HIGH | Phase 1 | High |
| 3 | MEDIUM | Phase 2 | Medium |
| 4 | MEDIUM | Phase 3 | High |
| 5 | LOW | Phase 4 | Research |
| 6 | LOW | All | Documentation |

---

## Next Steps

1. Implement AgentConfig and AgentFactory (Phase 1)
2. Test with baseline canvas from completed experiment
3. Design dual-LLM configuration schema
4. Prototype coach/performer separation
