# Process-Retrieval Augmented Reasoning (PRAR)

PRAR is the methodological framework underlying the Socratic-RCM system. This directory contains the formal method specification, reusable configurations, and canonical outputs.

## Conceptual Foundation

PRAR inverts the traditional RAG paradigm:

| Dimension | Traditional RAG | PRAR |
|-----------|-----------------|------|
| Retrieval target | Information | Process schemas |
| Generation goal | Answers | Scaffolding questions |
| Learner role | Consumer | Producer |
| System constraint | Accuracy | Restraint |

The system retrieves *procedural knowledge* (how to guide) rather than *declarative knowledge* (what to say), enabling structured cognitive governance without content generation.

## Directory Structure

```
prar/
├── configs/          # Reusable PRAR configurations
│   ├── theoretical_frameworks/
│   ├── agent_templates/
│   └── workflow_schemas/
│
├── templates/        # Canonical starter files
│   ├── baseline_answers.py
│   ├── agent_skeleton.json
│   └── project_scaffold.json
│
├── outputs/          # PRAR-generated artifacts
│   └── YYYY-MM-DD_name/
│       ├── state.json
│       ├── canvas.json
│       └── document.txt
│
└── README.md         # This file
```

## Relationship to Experiments

PRAR outputs are the *raw products* of running the 112-step workflow. Experiments are *research instances* that contextualize those outputs with:

- Research questions
- Model configurations
- Interpretive analysis
- Comparative notes

```
prar/outputs/           → Raw PRAR artifacts (state, canvas, document)
experiments/            → Research contextualization (notes, analysis, comparisons)
```

## The 112-Step Workflow

PRAR executes a three-phase workflow:

**Phase 1: Conceptualization** (38 steps)
- Theoretical framework selection (Options A-E)
- Concept definition and contrast
- Experiment design specification
- Agent and setting configuration

**Phase 2: Drafting** (66 steps)
- Agent prompt compilation
- Round instruction development
- Platform configuration
- Helper function setup

**Phase 3: Review** (4 steps)
- Design verification
- Completeness check
- Export preparation

## Theoretical Options

PRAR supports five theoretical frameworks from the B42 Chatstorm assignment:

| Option | Framework | Theorists | Concept A | Concept B |
|--------|-----------|-----------|-----------|-----------|
| A | Class Conflict / Alienation | Marx, Wollstonecraft | Alienation | Non-domination |
| B | Democratic Participation | Tocqueville, Smith | Civic virtue | Self-interest |
| C | Gender and Power | Wollstonecraft, Marx | Domination | Exploitation |
| D | Economic Rationality | Smith, Tocqueville | Market behavior | Democratic norms |
| E | Custom | User-defined | User-defined | User-defined |

## Usage

PRAR is executed through the local orchestrator:

```bash
cd local_rcm
python scripts/run_baseline_experiment.py \
  --base-url http://127.0.0.1:8000/v1 \
  --model Qwen/Qwen2.5-7B-Instruct
```

Outputs are saved to `prar/outputs/` with timestamped folders.

## Citation

When referencing the PRAR methodology:

```bibtex
@misc{coburn2025prar,
  author = {Coburn, Del},
  title = {Process-Retrieval Augmented Reasoning: A Socratic Framework for Pedagogical Applications},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Baglecake/Socratic-RCM}
}
```

## See Also

- [ROADMAP.md](../ROADMAP.md) - Development phases and implementation roadmap
- [local_rcm/README.md](../local_rcm/README.md) - Orchestrator documentation
- [agents/README.md](../agents/README.md) - Agent system (consumes PRAR outputs)
- [social_rl/README.md](../social_rl/README.md) - Social RL framework
- [theory/README.md](../theory/README.md) - Theoretical knowledge base
