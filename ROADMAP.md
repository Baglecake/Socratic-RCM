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

**Status:** COMPLETE

**Goal:** Transform canvas agent definitions into executable simulation participants.

### Components

**AgentConfig** - Configuration dataclass with canvas parsing
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
    temperature: float   # Generation temperature
    max_tokens: int      # Response length limit
    behaviors: dict      # Conditional behavior rules
```

**AgentFactory** - Canvas-to-agent instantiation
```python
factory = AgentFactory.from_state_file("state.json")
alice = factory.create("Worker+Alice")
all_agents = factory.create_all()
round1_participants = factory.get_round_participants(1)
```

**AgentRunner** - Multi-agent simulation execution
```python
runner = AgentRunner(factory, llm_client)
transcript = runner.execute_round(1)
runner.save_transcript(transcript, "round1.json")
```

### Deliverables

- [x] `agents/agent_config.py` - AgentConfig, AgentResponse, RoundConfig dataclasses
- [x] `agents/agent_factory.py` - Factory for instantiating agents from canvas
- [x] `agents/agent_runner.py` - Runtime for multi-agent simulation execution
- [x] Integration tests with mock LLM
- [ ] `agents/persona_library/` - Reusable persona templates (deferred)

### Outcome

The agent layer successfully bridges PRAR canvas outputs to executable simulations. Agents can be instantiated from state.json files and executed in rounds with transcript logging.

---

## Phase 2: Dual-LLM Architecture

**Status:** COMPLETE (Dual-Instance validated)

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

- [x] `dual-instance/dual-instance-v1.ipynb` - Validated Coach/Performer separation
- [ ] `dual_llm/coach.py` - PRAR validation and questioning (production)
- [ ] `dual_llm/performer.py` - Agent persona execution (production)
- [ ] `dual_llm/pipeline.py` - Coordinated execution flow

### Outcome

Dual-instance architecture validated in Colab notebook. Ready for production implementation.

---

## Phase 2.5: Social RL Architecture

**Status:** COMPLETE

**Goal:** Implement RL through social interaction - agents learn from social feedback without explicit reward functions.

### The Novel RL Formulation

| Traditional RL | Social RL (This Implementation) |
|---------------|--------------------------------|
| Environment | Other agents + theoretical constraints |
| State | Round context + concept manifestations |
| Action | Agent utterance/response |
| Reward | Social feedback (engagement, alignment, contribution) |
| Policy | PRAR process schemas |

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    SocialRLRunner                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │ ContextInjector │  │ FeedbackExtract │  │ ProcessRetr │  │
│  │                 │  │                 │  │             │  │
│  │ - Dynamic       │  │ - Engagement    │  │ - PRAR cues │  │
│  │   manifestations│  │ - Alignment     │  │ - Policy    │  │
│  │ - Per-turn      │  │ - Contribution  │  │   adaptation│  │
│  │   adaptation    │  │                 │  │             │  │
│  └────────┬────────┘  └────────┬────────┘  └──────┬──────┘  │
│           │                    │                   │         │
│           └────────────────────┼───────────────────┘         │
│                                │                             │
│                    ┌───────────▼───────────┐                 │
│                    │   Coach/Performer     │                 │
│                    │   Validated Output    │                 │
│                    └───────────────────────┘                 │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Components

**ContextInjector** - Dynamic manifestation generation
```python
# Instead of static prompts, each turn gets dynamic context:
context = injector.generate_turn_context(
    agent_id="Worker+Alice",
    round_config=round_config,
    turn_number=turn,
    conversation_history=history,
    accumulated_feedback=feedback  # Social signals shape context
)
```

**SocialFeedbackExtractor** - Extract learning signals from interaction
```python
# Social feedback as reward signal:
feedback = extractor.extract_round_feedback(round_num, messages, participants)
# Returns: engagement, theoretical_alignment, contribution_value per agent
```

**ProcessRetriever** - PRAR-based policy with adaptation
```python
# Process retrieval as policy (guides HOW to reason, not WHAT to say):
policy = retriever.retrieve_policy("Worker", feedback=agent_feedback)
rcm_cue = retriever.generate_rcm_cue(policy, feedback)

# Soft policy adaptation based on feedback deltas:
retriever.adapt_policy("Worker", {"engagement_delta": 0.15})
```

### Key Innovations

1. **No Explicit Reward Function**: Learning signals emerge from interaction
2. **Process Retrieval as Policy**: PRAR guides reasoning, adapts based on feedback
3. **Dynamic Context Injection**: Manifestations evolve per turn
4. **Theoretical Grounding**: Framework constraints prevent drift

### Deliverables

- [x] `social_rl/context_injector.py` - Dynamic manifestation generation
- [x] `social_rl/feedback_extractor.py` - Social feedback extraction
- [x] `social_rl/process_retriever.py` - PRAR policy retrieval and adaptation
- [x] `social_rl/runner.py` - Main SocialRLRunner execution engine
- [x] `social_rl/__init__.py` - Package exports
- [x] `notebooks/social_rl_demo.ipynb` - Demo notebook

### Usage

```python
from social_rl import SocialRLRunner, SocialRLConfig, create_social_rl_runner

runner = create_social_rl_runner('state.json', llm_client, mode='progressive')
results = runner.execute_all_rounds()
print(runner.generate_report())
```

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

| Phase | Status | Dependency | Complexity |
|-------|--------|------------|------------|
| 1 | COMPLETE | None | Medium |
| 2 | COMPLETE | Phase 1 | High |
| 2.5 | COMPLETE | Phase 1-2 | High |
| 3 | MEDIUM | Phase 2.5 | Medium |
| 4 | MEDIUM | Phase 3 | High |
| 5 | LOW | Phase 4 | Research |
| 6 | LOW | All | Documentation |

---

## Next Steps: Implementation Roadmap

The following roadmap outlines concrete implementation tasks to move from the current state (Phase 2.5 complete) toward a publication-ready system.

---

### Immediate: Schema Formalization

**Goal:** Make PRAR and Social RL outputs follow explicit, versioned schemas.

**Tasks:**

1. Create `social_rl/schema.py` with TypedDicts or dataclasses:
   - `SocialRLMessage`: agent_id, role, content, turn_index, context_frame
   - `SocialRLRoundResult`: round_number, messages, feedback, policy_adaptations, duration_seconds
   - `FeedbackVector`: engagement, alignment, contribution_value
   - `PolicyAdaptation`: agent_id, type, cue, reason, round

2. Create `prar/schema.py`:
   - `PRARState`: student_state, canvas, metadata
   - `PRARPolicyState`: framework_option, policies, timestamp, source_run_id

3. Update `SocialRLRunner` to serialize via these schemas

4. Add metadata block to each output file:
   ```json
   "meta": {
     "experiment_id": "social_rl_2025-11-23_175825",
     "prar_run_id": "2025-11-23_baseline_full_qwen",
     "framework": "Alienation vs Non-Domination",
     "model": "Qwen/Qwen2.5-7B-Instruct",
     "performer_temperature": 0.7,
     "coach_temperature": 0.1,
     "social_rl_version": "0.2.0"
   }
   ```

**Deliverables:**
- [x] `social_rl/schema.py` - COMPLETE (TypedDicts, dataclasses, validation)
- [ ] `prar/schema.py` - Deferred
- [x] Updated runner with schema validation - COMPLETE
- [ ] `docs/architecture/SOCIAL_RL_SCHEMA.md` - Optional

---

### Short-term: Dual-LLM Client Implementation

**Goal:** Implement true coach/performer separation with distinct LLM clients.

**Tasks:**

1. Create `social_rl/dual_llm_client.py`:
   ```python
   class DualLLMClient:
       def __init__(self, performer_client, coach_client=None):
           self.performer = performer_client
           self.coach = coach_client or performer_client
           self.performer_temp = 0.7
           self.coach_temp = 0.1

       def generate(self, system, user, mode="performer"):
           client = self.performer if mode == "performer" else self.coach
           temp = self.performer_temp if mode == "performer" else self.coach_temp
           return client.send_message(system, user, temperature=temp)
   ```

2. Update `SocialRLRunner._generate_with_validation()`:
   - Use `mode="performer"` for initial generation
   - Use `mode="coach"` for critique/validation
   - Log coach critiques as internal messages (optional)

3. Update `run_social_rl_local.py` with CLI flags:
   - `--dual-llm`: Enable dual-LLM mode
   - `--coach-model`: Model for coach role
   - `--performer-model`: Model for performer role
   - `--coach-temp`, `--performer-temp`: Temperature overrides

4. Extract dual-instance logic from notebook to module

**Deliverables:**
- [x] `social_rl/dual_llm_client.py` - COMPLETE
- [x] Updated `SocialRLRunner` integration - COMPLETE
- [x] CLI flag support in `experiments/run_social_rl_experiment.py` - COMPLETE (--no-dual-llm)
- [ ] Documentation in `social_rl/README.md`

---

### Short-term: Test Suite for Social RL

**Goal:** Establish testable surface for Social RL components.

**Tasks:**

1. Create `tests/test_social_rl_minimal_round.py`:
   - Build synthetic canvas (1 round, 2 agents)
   - Use mock LLM client with deterministic responses
   - Assert `execute_round(1)` returns valid `SocialRLRoundResult`
   - Validate JSON structure matches schema

2. Create `tests/test_social_feedback_invariants.py`:
   - Construct message list, feed through `SocialFeedbackExtractor`
   - Assert feedback values in valid ranges [0, 1]
   - Test monotonicity properties

3. Create `tests/test_process_retriever_policies.py`:
   - Create `ProcessRetriever` with defined policies
   - Mock feedback and assert `get_active_cues` returns expected subsets

4. Add test runner configuration:
   - pytest configuration
   - CI integration (optional)

**Deliverables:**
- [ ] `tests/test_social_rl_minimal_round.py`
- [ ] `tests/test_social_feedback_invariants.py`
- [ ] `tests/test_process_retriever_policies.py`
- [ ] `pytest.ini` or `pyproject.toml` test config

---

### Medium-term: Experiment Structure Normalization

**Goal:** Create clear separation between PRAR outputs and Social RL experiments.

**Tasks:**

1. Establish experiment directory structure:
   ```
   experiments/
     social_rl/
       2025-11-23_alienation_qwen/
         prar_state.json        # Copy or symlink
         config.json            # Experiment metadata
         social_rl_*/           # Output directories
         analysis_notes.md      # Interpretive notes
   ```

2. Create `scripts/create_experiment.py`:
   - Initialize experiment directory
   - Copy/link PRAR state
   - Generate config.json template

3. Add README to `experiments/`:
   - Explain structure
   - Document naming conventions
   - Provide analysis guidance

4. Mark legacy directories:
   - Add README to `simulation_test/` indicating legacy status

**Deliverables:**
- [ ] `experiments/` directory structure
- [ ] `scripts/create_experiment.py`
- [ ] `experiments/README.md`
- [ ] Legacy directory documentation

---

### Medium-term: Behavioral Metrics (Phase 3)

**Goal:** Extract quantitative behavioral metrics from simulation transcripts.

**Tasks:**

1. Create `social_rl/metrics.py`:
   - Message sentiment analysis
   - Assertiveness indicators
   - Compliance patterns
   - Conflict triggers
   - Thematic markers (alienation, domination, etc.)

2. Extend `SocialFeedbackExtractor`:
   - Add behavioral metric extraction
   - Aggregate metrics per round and per experiment

3. Create analysis notebook:
   - Load experiment outputs
   - Compute behavioral metrics
   - Generate visualizations

**Deliverables:**
- [x] `social_rl/metrics.py` - COMPLETE (RelationalMetricsComputer with alienation, domination, justification markers)
- [x] Extended `SocialFeedbackExtractor` - COMPLETE (integrated with runner)
- [ ] Analysis notebook template

---

### Long-term: CES Agent Generation (Phase 5)

**Goal:** Generate synthetic survey respondents from Canadian Election Study data.

**Tasks:**

1. Create `agents/ces_generators/row_to_agent.py`:
   - CES row to AgentConfig transformation
   - Demographic-to-persona mapping
   - Behavioral prior generation

2. Define CES variable mapping schema

3. Create persona generation templates

4. Validate against actual CES distributions

**Deliverables:**
- [ ] `agents/ces_generators/row_to_agent.py`
- [ ] CES variable mapping documentation
- [ ] Validation scripts

---

### Long-term: Publication Package (Phase 6)

**Goal:** Prepare reproducibility package for academic publication.

**Tasks:**

1. Finalize paper: "PRAR-Guided Dual-LLM Agent Simulations: A Framework for Computational Sociology"

2. Create reproducibility package:
   - Canonical experiment configurations
   - Expected outputs for validation
   - Step-by-step reproduction guide

3. Prepare dataset: Synthetic CES simulation corpus

4. Documentation review and polish

**Deliverables:**
- [ ] Paper draft
- [ ] Reproducibility package
- [ ] Public dataset
- [ ] Final documentation

---

## Implementation Priority

| Task | Priority | Dependency | Complexity | Status |
|------|----------|------------|------------|--------|
| Schema formalization | High | None | Low | **COMPLETE** |
| Dual-LLM client | High | Schema | Medium | **COMPLETE** |
| Social RL tests | High | Schema | Medium | Partial |
| Experiment structure | Medium | None | Low | **COMPLETE** |
| Behavioral metrics | Medium | Tests | Medium | **COMPLETE** |
| CES generators | Low | Metrics | High | **NEXT** |
| Publication | Low | All | Documentation | Future |

---

## Completed Milestones

1. ~~Design dual-LLM configuration schema (Phase 2)~~ DONE
2. ~~Implement Social RL architecture (Phase 2.5)~~ DONE
3. ~~Test Social RL with real LLM backend (vLLM/Qwen)~~ DONE
4. ~~Local runner with Ollama support~~ DONE
5. ~~Schema formalization (`social_rl/schema.py`)~~ DONE (2025-11-23)
6. ~~Dual-LLM client implementation~~ DONE (2025-11-23)
7. ~~Behavioral metrics (`social_rl/metrics.py`)~~ DONE (2025-11-23)
8. ~~Experiment runner with CLI (`experiments/run_social_rl_experiment.py`)~~ DONE (2025-11-23)
