# The Reflect and Connect Model (RCM)
## A Socratic RAG Framework for Pedagogical Applications

> **B42 Chatstorm T.A. - Implementation of RCM for Social Theory**

[![Status](https://img.shields.io/badge/status-production-brightgreen)]()
[![Version](https://img.shields.io/badge/version-8.4-blue)]()
[![Framework](https://img.shields.io/badge/framework-RCM-purple)]()
[![GPT Builder](https://img.shields.io/badge/OpenAI-GPT%20Builder-412991)]()

---

## Quick Links

- **Production System**: [production/](production/) - v8.4-FINAL (Ready for student deployment)
- **Experimental**: [experimental/bios-architecture/](experimental/bios-architecture/) - BIOS + Runtime (Research branch)
- **Theory KB**: [theory/](theory/) - Lecture notes (Marx, Tocqueville, Wollstonecraft, Smith)
- **Documentation**: [docs/](docs/) - Architecture, research, papers
- **Literature**: [literature/](literature/) - Academic references

---

## Repository Structure

```
Socratic-RCM/
├── production/              # ✅ Current production system (v8.4)
│   ├── system-prompt/      # GPT Builder instructions
│   ├── knowledge-base/     # Assignment docs & templates
│   └── deployment/         # Deployment checklist
│
├── experimental/           # ⚠️ Experimental branches
│   └── bios-architecture/  # BIOS + Runtime approach (research)
│
├── theory/                 # Shared theory knowledge base
│   ├── marx_theory.txt
│   ├── tocqueville_theory.txt
│   ├── wollstonecraft_theory.txt
│   └── smith_theory.txt
│
├── docs/                   # Project documentation
│   ├── research/          # Validation protocols, toolkits
│   ├── architecture/      # System design docs
│   └── papers/            # Research papers (LaTeX)
│
├── literature/             # Academic references
└── archive/                # Deprecated files
```

---

## Current Version: v8.4 (Production)

**Last Updated:** 2025-01-19
**Status:** Production Ready
**Framework:** Reflect and Connect Model (RCM)

### Quick Start

1. **Deploy Production System**:
   - See [production/README.md](production/README.md) for deployment instructions
   - Upload system prompt + knowledge base to GPT Builder
   - Disable DALL-E image generation in settings

2. **Understand the Architecture**:
   - Read [The Reflect and Connect Model](#the-reflect-and-connect-model-rcm) below
   - Review [docs/architecture/](docs/architecture/) for design rationale

3. **Explore Experimental Branches**:
   - [experimental/bios-architecture/](experimental/bios-architecture/) - Overcoming 8KB limit (research)

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

### Experimental: BIOS + Runtime (Research)

**Separated Architecture**:
- BIOS (~7KB): Execution engine with prohibitions & force-read protocol
- Runtime Files (unlimited): Step-by-step workflow instructions
- **Goal**: Overcome 8KB limit while maintaining strict control
- **Status**: Force-read reliability issues (step-skipping observed)

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

[LICENSE]LICENSE

---

## Contact

For questions or collaboration:  
Issues: [GitHub Issues](https://github.com/Baglecake/Socratic-RCM/issues)
  
> **Del Coburn**  
> University of Toronto  
> 📧 del.coburn@mail.utoronto.ca  
---

**Status**: Production system (v8.4) ready for student deployment ✅  
**Experimental**: BIOS architecture under active research ⚠️
