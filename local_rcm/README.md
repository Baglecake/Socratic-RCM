# Local Orchestrator

The local orchestrator executes the 112-step PRAR workflow independently of GPT Builder, providing a Python-based implementation suitable for research, testing, and integration with various LLM backends.

## Architecture

```mermaid
flowchart TB
    subgraph Input
        RF[Runtime Files]
        BP[BIOS Prompt]
    end

    subgraph Orchestrator
        RP[Runtime Parser]
        WO[Workflow Orchestrator]
        CS[Canvas State]
    end

    subgraph LLM Layer
        LC[LLM Client]
        SH[Student Handler]
    end

    subgraph Backends
        MK[Mock]
        VL[vLLM]
        OA[OpenAI]
        AN[Anthropic]
    end

    subgraph Output
        ST[state.json]
        DC[document.txt]
    end

    RF --> RP
    RP --> WO
    BP --> SH
    WO --> CS
    WO --> SH
    SH --> LC
    LC --> MK
    LC --> VL
    LC --> OA
    LC --> AN
    CS --> ST
    CS --> DC
```

## Workflow Execution

```mermaid
sequenceDiagram
    participant U as User/Simulator
    participant O as Orchestrator
    participant L as LLM Client
    participant C as Canvas State

    O->>O: Load runtime files
    O->>O: Initialize at step 1.1

    loop Each Step
        O->>L: Generate question
        L-->>O: Formatted question
        O->>U: Present question
        U-->>O: Answer
        O->>L: Validate answer
        L-->>O: Validation result
        O->>C: Store answer
        O->>O: Resolve next step
    end

    O->>C: Compile canvas
    C-->>O: Final document
```

## Directory Structure

```
local_rcm/
├── orchestrator.py       # Workflow state machine (owns step advancement)
├── canvas_state.py       # Data model, compilation, JSON export
├── llm_client.py         # LLM abstraction + StudentSimulator
├── runtime_parser.py     # Step definition parser
├── app.py                # Streamlit web interface
├── example_usage.py      # CLI entry point
├── bios_reduced_prompt.txt
├── requirements.txt
│
├── runtime-files/        # Workflow definitions (56 steps total)
│   ├── B42_Runtime_Phase1_Conceptualization.txt
│   ├── B42_Runtime_Phase2_Drafting.txt
│   └── B42_Runtime_Phase3_Review.txt
│
├── scripts/              # Experiment execution
│   └── run_baseline_experiment.py
│
├── tests/                # Automated test suite
│   ├── test_auto.py
│   ├── test_realistic.py
│   └── test_full_workflow.py
│
└── output/               # Generated outputs (gitignored)
```

## Installation

```bash
cd local_rcm
pip install -r requirements.txt
```

## Usage

### Baseline Experiment (Recommended)

Execute the complete 3-phase workflow with automatic output versioning:

```bash
# Mock mode (no LLM calls, instant execution)
python scripts/run_baseline_experiment.py --mock

# With vLLM backend (requires running vLLM server)
python scripts/run_baseline_experiment.py \
  --base-url http://127.0.0.1:8000/v1 \
  --model Qwen/Qwen2.5-7B-Instruct
```

Outputs are saved to `experiments/YYYY-MM-DD_name/`.

### Streamlit Interface

Interactive web interface for step-by-step execution:

```bash
streamlit run app.py
```

### Test Suite

```bash
# Full workflow (112 steps, mock mode)
python tests/test_full_workflow.py --mock

# Phase 1 only (42 steps)
python tests/test_realistic.py --mock
```

## Three-Phase Workflow

```mermaid
flowchart LR
    subgraph Phase1[Phase 1: Conceptualization]
        direction TB
        P1A[Framework Selection]
        P1B[Concept Definition]
        P1C[Experiment Design]
        P1D[Agent Configuration]
        P1A --> P1B --> P1C --> P1D
    end

    subgraph Phase2[Phase 2: Drafting]
        direction TB
        P2A[Agent Prompts]
        P2B[Round Instructions]
        P2C[Platform Config]
        P2D[Helper Functions]
        P2A --> P2B --> P2C --> P2D
    end

    subgraph Phase3[Phase 3: Review]
        direction TB
        P3A[Design Verification]
        P3B[Export Preparation]
        P3A --> P3B
    end

    Phase1 --> Phase2 --> Phase3
```

| Phase | Steps | Purpose |
|-------|-------|---------|
| Phase 1 | 38 | Theoretical framework, concepts, agents, setting |
| Phase 2 | 66 | Round instructions, prompts, platform configuration |
| Phase 3 | 4 | Verification and export |

## Canvas Data Model

The canvas accumulates structured data throughout the workflow:

```mermaid
erDiagram
    CANVAS ||--|| PROJECT : contains
    CANVAS ||--o{ AGENT : has
    CANVAS ||--o{ ROUND : has
    CANVAS ||--|| HELPERS : configures
    CANVAS ||--|| STATUS : tracks

    PROJECT {
        string goal
        string theoretical_option
        object concept_a
        object concept_b
        object variable
        string setting
        int rounds_count
    }

    AGENT {
        string identifier
        string goal
        string persona
        string prompt
    }

    ROUND {
        int round_number
        string scenario
        string rules
        string tasks
        object platform_config
    }

    HELPERS {
        string analyst_function
        string moderator_function
        string self_reflection
        string non_anthropomorphic
    }

    STATUS {
        bool phase1_complete
        bool phase2_complete
        bool phase3_complete
        bool ready_for_export
    }
```

## LLM Backend Configuration

| Backend | Use Case | Configuration |
|---------|----------|---------------|
| Mock | Testing, CI | `--mock` flag |
| vLLM | Local GPU, Colab | `--base-url http://host:8000/v1` |
| OpenAI | API access | `--api-key YOUR_KEY` |
| Anthropic | Claude models | Requires anthropic package |

### vLLM Setup (Colab/RunPod)

```bash
# Start vLLM server
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct \
  --dtype bfloat16 \
  --port 8000

# Run orchestrator
python scripts/run_baseline_experiment.py \
  --base-url http://127.0.0.1:8000/v1 \
  --model Qwen/Qwen2.5-7B-Instruct
```

## Output Files

Each experiment produces:

| File | Description |
|------|-------------|
| `state.json` | Complete workflow state including all student answers and compiled canvas |
| `document.txt` | Human-readable simulation design document |
| `config.json` | Experiment metadata (model, backend, phases completed) |
| `notes.md` | Execution summary and observations |

## Design Principles

1. **Orchestrator owns state**: The LLM never controls workflow progression
2. **Deterministic execution**: Same inputs produce identical step sequences
3. **LLM-agnostic**: Backend can be swapped without code changes
4. **Incremental compilation**: Canvas builds progressively from student responses
