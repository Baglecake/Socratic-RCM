# The Reflect and Connect Model (RCM)
## A Socratic RAG Framework For Process-Retrieval Augmented Reasoning (PRAR)

> **B42 Chatstorm T.A. - Implementation of RCM for Social Theory**

[![Status](https://img.shields.io/badge/status-production-brightgreen)]()
[![Version](https://img.shields.io/badge/version-8.4-blue)]()
[![Framework](https://img.shields.io/badge/framework-RCM-purple)]()
[![GPT Builder](https://img.shields.io/badge/OpenAI-GPT%20Builder-412991)]()

---

## Quick Links

| Component | Location | Status | Use Case |
|-----------|----------|--------|----------|
| **Production System** | [production/](production/) | ✅ Stable | GPT Builder deployment |
| **Local Orchestrator** | [local_rcm/](local_rcm/) | ✅ Active | Local/vLLM execution |
| **Experimental** | [experimental/](experimental/) | ⚠️ Research | Architecture testing |
| **Theory KB** | [theory/](theory/) | ✅ Stable | Shared lecture notes |
| **Documentation** | [docs/](docs/) | ✅ Current | Architecture, papers |

---

## Repository Structure

```
Socratic-RCM/
├── production/             #  GPT Builder system (v8.4)
│   ├── system-prompt/      # GPT Builder instructions
│   ├── knowledge-base/     # Assignment docs & templates
│   └── deployment/         # Deployment checklist
│
├── local_rcm/              # Local Python orchestrator
│   ├── orchestrator.py     # Core workflow engine
│   ├── canvas_state.py     # Data model & compilation
│   ├── llm_client.py       # LLM abstraction (mock/vLLM)
│   ├── runtime-files/      # Workflow definitions
│   ├── tests/              # Automated test suite
│   └── notebooks/          # Colab/Jupyter support
│
├── experimental/           # ⚠️ Research branches
│   └── bios-architecture/  # BIOS + Runtime approach
│
├── theory/                 # Shared theory knowledge base
│   └── *.txt               # Marx, Tocqueville, Wollstonecraft, Smith
│
├── docs/                   # Project documentation
│   ├── research/          # Validation protocols
│   ├── architecture/      # System design
│   └── papers/            # Research papers (LaTeX)
│
├── literature/             # Academic references
└── archive/                # Deprecated versions (v3-v8)
```

---

## Current Versions

**Last Updated:** 2025-11-22
**Framework:** Reflect and Connect Model (RCM)

### Which Version Should I Use?

| Deployment Target | Recommended Version | Location |
|-------------------|---------------------|----------|
| GPT Builder (students) | v8.4 Monolithic | [production/](production/) |
| Local Python (vLLM/API) | Local Orchestrator | [local_rcm/](local_rcm/) |
| Research/Testing | BIOS Architecture | [experimental/](experimental/) |

### Quick Start

**Option A: GPT Builder Deployment** (v8.4)
1. See [production/README.md](production/README.md) for instructions
2. Upload system prompt + knowledge base to GPT Builder
3. Disable DALL-E image generation in settings

**Option B: Local Python Orchestrator**
1. See [local_rcm/README.md](local_rcm/README.md) for setup
2. Run with mock LLM: `python example_usage.py --mode mock`
3. Run with vLLM: `python example_usage.py --mode vllm --base-url URL`

**Option C: Explore Experimental**
- [experimental/bios-architecture/](experimental/bios-architecture/) - BIOS + Runtime research

---

## The Reflect and Connect Model (RCM)

**RCM** is a Socratic RAG (Retrieval-Augmented Generation) framework designed for pedagogical applications where the goal is to guide learners through complex creative tasks without doing the work for them.

### Core Innovation: Process-Retrieval Architecture

Traditional RAG: `Query → Retrieve Information → Generate Answer`
Pedagogical RAG (RCM): `Query → Retrieve Process Schema → Generate Socratic Scaffold`

This architectural shift enables:

1. **Dynamic Protocol Adaptation**: The system retrieves context-appropriate questioning strategies
2. **Generative Restraint Through Process Guardrails**: Retrieved processes include boundary conditions (what NOT to generate)
3. **Recursive Reflection Architecture**: Multi-layered feedback loop (mechanics → theory → meta-cognition)

### RCM in Practice: B42 Chatstorm T.A.

The B42 Chatstorm T.A. implements RCM to guide sociology students through multi-agent experiment design:

- **Reflect**: Students articulate theoretical tensions (e.g., Marx's alienation vs. Wollstonecraft's domination)
- **Connect**: System prompts connections to social theory from lecture notes
- **Ask**: Socratic questions scaffold design without providing answers

**Key Constraint**: Students create ALL content. System NEVER fills placeholders or generates creative work.

---

## Technical Architecture

### Production System (v8.4)

**Monolithic Prompt Architecture**:
- Single 8KB system prompt contains all workflow steps
- Embedded in GPT Builder "Instructions" field
- Knowledge base: Assignment docs + theory lecture notes
- **Advantages**: Proven stability, high reliability, always in attention
- **Limitations**: At 99% character capacity (7,994/8,000 bytes)

See: [production/README.md](production/README.md)

### Local Orchestrator (local_rcm/)

**Python-based workflow engine**:
- Runs 112-step workflow locally (no GPT Builder required)
- Supports multiple LLM backends: mock, vLLM, OpenAI API
- Canvas state management with JSON export
- Automated test suite for validation
- Jupyter/Colab support for GPU inference via ngrok

See: [local_rcm/README.md](local_rcm/README.md)

### Experimental: BIOS + Runtime (Research)

**Separated Architecture**:
- BIOS (~7KB): Execution engine with prohibitions & force-read protocol
- Runtime Files (unlimited): Step-by-step workflow instructions
- **Goal**: Overcome 8KB limit while maintaining strict control
- **Status**: Research branch - force-read reliability under investigation

See: [experimental/bios-architecture/README.md](experimental/bios-architecture/README.md)

---

## Key Features

### Absolute Prohibitions (Hardware-Level Constraints)

1. **NO CREATIVE WRITING**: System never writes, rewrites, or paraphrases student ideas
2. **NO BATCHING**: ONE question at a time, wait for answer, then proceed
3. **NO PLACEHOLDER ACCEPTANCE**: Rejects [...], "TBD", vague responses
4. **NO TRAINING DATA THEORY**: Uses ONLY lecture notes (KB[5-8]), cites "Per lecture..."
5. **NO FILE CREATION**: Displays compiled templates in chat with `||...||` markers

### Socratic Method (RCM Protocol)

For EVERY question: **Reflect** requirement, **Connect** to theory, **Ask** with encouragement

**Example**:
```
❌ "What's your goal?"
✅ "Think about [A] vs [B]—what tension? What observable dynamic? (2-3 sent.)"
```

### Three-Phase Workflow

1. **Phase 1: Conceptualization** - Theoretical framework, agents, setting
2. **Phase 2: Drafting** - Agent prompts, round instructions, platform config
3. **Phase 3: Review & Export** - Checklist, final review, export for testing

---

## Testing & Validation

### Production Testing (v8.4)

**Test Results (2025-01-19)**:
- File creation prohibition working (in-chat display with `||...||`)
- Sequential workflow maintained (no step-skipping)
- Theory queries accurate (routes to KB[5-8])
- Clean student-facing output (no debugging info)
- Socratic guidance shown (RCM cues visible)

**Known Issues**:
- Image generation requires DALL-E disabled in GPT settings
- Character limit prevents further enhancements (7,994/8,000)

### Experimental Testing (BIOS v2.1)

**Test Results (2025-01-19)**:
- UI improvements successful (clean output, RCM shown)
- Force-read failures persist (step-skipping observed)
- Not recommended for student deployment

---

## Documentation

### For Deployment
- [production/README.md](production/README.md) - Production system deployment
- [production/deployment/DEPLOYMENT_CHECKLIST.md](production/deployment/DEPLOYMENT_CHECKLIST.md) - Step-by-step setup

### For Development
- [experimental/bios-architecture/README.md](experimental/bios-architecture/README.md) - BIOS architecture overview
- [experimental/bios-architecture/docs/](experimental/bios-architecture/docs/) - Technical design docs
- [docs/architecture/](docs/architecture/) - System architecture documentation

### For Research
- [docs/research/](docs/research/) - Validation protocols, corpus construction
- [docs/papers/](docs/papers/) - Research papers on Pedagogical RAG
- [literature/](literature/) - Academic references on RAG, Socratic pedagogy

---

## Citation

If you use this framework in your research or teaching, please cite:

```
Coburn, D. (2025). The Reflect and Connect Model: A Socratic RAG Framework
for Pedagogical Applications. GitHub repository:
https://github.com/delcoburn/Socratic-RCM
```

---

## License
  
License: [LICENSE](https://github.com/Baglecake/Socratic-RCM/LICENSE)

---

## Contact

For questions or collaboration:  
Issues: [GitHub Issues](https://github.com/Baglecake/Socratic-RCM/issues)
  
> **Del Coburn**  
> University of Toronto  
> 📧 del.coburn@mail.utoronto.ca  
---

**Status Summary**:
- ✅ **Production (v8.4)**: Ready for GPT Builder student deployment
- ✅ **Local Orchestrator**: Ready for local/vLLM execution
- ⚠️ **Experimental (BIOS)**: Research branch - not for production use
