# Socratic-RCM Working Document

> **Purpose**: Comprehensive reference document for development, onboarding, and maintaining context across sessions.
> **Last Updated**: 2025-11-24
> **Maintainer**: Del Coburn / Claude Development Sessions

---

## Table of Contents

0. [Social Aesthetics & Research Programme](#0-social-aesthetics--research-programme)
1. [Project Overview](#1-project-overview)
2. [Vision: Dual-LLM Agent Simulation](#2-vision-dual-llm-agent-simulation)
3. [Architecture Summary](#3-architecture-summary)
4. [Deployment Targets](#4-deployment-targets)
5. [Local Setup (local_rcm/)](#5-local-setup-local_rcm)
6. [Production GPT Builder (v8.4)](#6-production-gpt-builder-v84)
7. [Experimental BIOS Architecture](#7-experimental-bios-architecture)
8. [Data Models & Schemas](#8-data-models--schemas)
9. [LLM Client Architecture](#9-llm-client-architecture)
10. [Runtime Files & Workflow](#10-runtime-files--workflow)
11. [Testing Infrastructure](#11-testing-infrastructure)
12. [GPU/Cloud Options](#12-gpucloud-options)
13. [Current Status & Known Issues](#13-current-status--known-issues)
14. [Development Roadmap](#14-development-roadmap)
15. [Quick Reference](#15-quick-reference)
16. [Social Aesthetics: 2×2×2 Architecture Sweep Results](#16-social-aesthetics-22×2-architecture-sweep-results)
17. [Session Log](#17-session-log)

---

## 0. Social Aesthetics & Research Programme

### Theoretical Foundation

**Social Aesthetics** is the governing theory of this research programme. It addresses the question: *under what conditions do social aesthetics embed themselves into a cybernetic order of relationality between AI architecture and the human presence?*

Drawing on Bateson's simulacra, Baudrillard's hyperreal, and Weber's sociogeographies, Social Aesthetics proposes that:

1. **LLMs traffic in pure simulacra** - signs without original referents, tokens without lived experience
2. **Meaning cannot be grounded semantically** for current LLMs
3. **Meaning CAN be grounded architecturally** - through material configuration of roles, rules, and feedback
4. **Social conditions emerge from architectural constraints**, not model "intelligence"

### Architecturally Grounded Simulacra

Rather than pursuing impossible semantic understanding, this system creates what we term **architecturally grounded simulacra** - where the "original" exists not in semantic understanding but in:

- **Temperature parameters** that create genuine behavioral difference (Coach τ=0.1 vs Performer τ=0.7)
- **Canvas configurations** that encode institutional rules (CAN/CANNOT constraints)
- **Process schemas (PRAR)** that structure reasoning as policy
- **Social RL feedback** that turns interaction into consistent pressure on behavior

### Socratic-RCM as Research Platform

This repository implements a **Social Aesthetics engine**: it turns social theory + design ethics into architectural constraints that shape how simulacra interact. The platform enables:

1. **Encoding classical theory into architecture** (alienation/non-domination as rules, not psychology)
2. **Running simulations that expose relational dynamics** (measurable shifts in speech patterns)
3. **Eventually grounding agents in sociogeographic conditions** (CES data, Weberian stratification)

### Critical Distinction: B42 vs Research

| Component | Purpose | Theory Source |
|-----------|---------|---------------|
| `b42_theory_library/` | **[B42-Pedagogy]** Theory texts for student exercises (Marx, Wollstonecraft, etc.) | Lecture materials |
| Social Aesthetics paper | **[Research Core]** The theoretical framework for this research programme | `Dev Copy - Social Aesthetics...txt` |
| Alienation vs Non-Domination | **[Use-Case]** A demonstration framework, not THE theory | Worked example |

> **Note on Alienation vs Non-Domination**: This is used as the primary demonstration framework because it provides a clean, theoretically grounded contrast between arbitrary and constrained power. We do NOT claim it as the unique or privileged theory; it is a worked example of how Social Aesthetics can be operationalized. Changing one architectural rule (requiring justification) yields measurable shifts in interaction patterns (alienation markers: 3→0, justification: 1→7).

---

## 1. Project Overview

### What is Socratic-RCM?

**The Reflect and Connect Model (RCM)** is a Socratic RAG framework for pedagogical applications. Unlike traditional RAG that retrieves content to answer questions, RCM retrieves **process schemas** to generate **Socratic scaffolds** that guide learners through complex creative tasks without doing the work for them.

### Core Innovation: Process-Retrieval Architecture

```
Traditional RAG: Query -> Retrieve Information -> Generate Answer
Pedagogical RAG (RCM): Query -> Retrieve Process Schema -> Generate Socratic Scaffold
```

### The RCM Method

For **EVERY** question, the system follows:
1. **Reflect**: Help student articulate the requirement
2. **Connect**: Link to relevant social theory from lecture notes
3. **Ask**: Pose a Socratic question with encouragement

### Key Constraint

**Students create ALL content. The system NEVER fills placeholders, writes creative content, or paraphrases student ideas.**

### Primary Use Case

The B42 Chatstorm T.A. guides sociology students (SOCB42 at University of Toronto) through designing multi-agent simulation experiments that test theoretical tensions between classical theorists (Marx, Wollstonecraft, Tocqueville, Smith).

---

## 2. Vision: Dual-LLM Agent Simulation

### The Big Picture

This project is evolving from a teaching assistant into a **generalizable agent simulation framework** governed by PRAR (Process-Retrieval Augmented Reasoning). The architecture mirrors CQB (Central Query Brain) principles: central orchestrator owns workflow state, LLMs are demoted to "IO devices."

### Evolution Path

```
CURRENT STATE (B42 Teaching Assistant):
┌─────────────────┐                    ┌─────────────────┐
│  Human Student  │ <-- Socratic --> │   LLM Coach     │
│  (types answers)│     PRAR          │  (asks/validates)│
└─────────────────┘                    └─────────────────┘

NEAR FUTURE (B42 Dual-LLM):
┌─────────────────┐                    ┌─────────────────┐
│  Student Agent  │ <-- Socratic --> │   Coach LLM     │
│  (LLM #2)       │     PRAR          │  (LLM #1)       │
│  Generated from │                    │  Same PRAR/RCM  │
│  Option A-E     │                    │  logic          │
└─────────────────┘                    └─────────────────┘

GENERALIZED FUTURE (CES/Research Simulations):
┌─────────────────┐                    ┌─────────────────┐
│  N Synthetic    │ <-- Process   --> │   Coach LLM     │
│  Agents         │     Schema         │                 │
│  (demographics) │     (PRAR)         │  Interrogates,  │
│  CES respondents│                    │  validates,     │
│  Survey panels  │                    │  shapes behavior│
└─────────────────┘                    └─────────────────┘
```

### Dual-LLM Architecture Concept

**LLM #1 - Coach/Orchestrator**:
- Continues PRAR/RCM function
- Reads runtime steps, formulates Socratic questions
- Validates agent responses against constraints
- Never controls workflow state (code does)

**LLM #2 - Agent**:
- Inhabits a generated persona (student, CES respondent, etc.)
- Responds to Socratic prompts from Coach
- Produces content that Coach validates/shapes
- Persona built from config (B42 option, CES demographics, etc.)

### B42 Dual-LLM Flow

1. Orchestrator presents 5 theoretical options (A-E)
2. User (or system) selects option
3. **AgentConfig generated**: System prompt tailored to theoretical problem
   - "You are a B42 student examining Marx vs Wollstonecraft..."
   - Framework-specific constraints and vocabulary
4. **Agent LLM instantiated** with this persona
5. **Coach LLM + Orchestrator** run the 3-phase workflow
   - Coach formulates RCM questions
   - Agent responds as the "student"
   - Orchestrator validates, updates canvas, advances steps

### CES/Research Generalization

Same architecture, different inputs:

| Component | B42 Mode | CES Mode |
|-----------|----------|----------|
| **AgentConfig Source** | Option A-E selection | CES survey row |
| **Persona Elements** | Theoretical framework | Demographics, ideology, prior vote |
| **Runtime Schema** | B42 3-phase workflow | Survey experiment rounds |
| **Canvas/Output** | Simulation design document | Survey responses, behavioral traces |

### What Already Exists (Proto-Agent)

The `StudentSimulator` class in `llm_client.py` is already a proto-agent:

```python
class StudentSimulator:
    def __init__(self, llm_client, persona=None):
        self.llm = llm_client
        self.persona = persona or STUDENT_PERSONA
        self.conversation_history = []

    def set_framework(self, option):  # Update persona after option selection
        if option in FRAMEWORK_PERSONAS:
            self.persona = FRAMEWORK_PERSONAS[option] + guidelines
```

**Framework-Specific Personas** already exist:
- Option A: Marx + Wollstonecraft (alienation, domination)
- Option B: Tocqueville only (democratic paradoxes)
- Option C: Marx + Tocqueville (revolution vs conformity)
- Option D: Smith + Tocqueville (commerce vs equality)
- Option E: Custom framework

### Implementation Phases

**Phase 0 - Single Model, Dual Roles** (Can start now):
- One RunPod model
- Different system prompts for coach vs agent
- Same infrastructure, test the logic

**Phase 1 - Same Family, Two Endpoints**:
- Coach: Lower temp, more careful reasoning
- Agent: Higher temp, more "human-ish" responses

**Phase 2 - Different Models**:
- Coach: Large reasoning model
- Agents: Smaller/faster models for population-scale simulation

### Relationship to CQB

This project is a **specialized, PRAR-flavored mini-CQB**:

| CQB Principle | Socratic-RCM Implementation |
|---------------|----------------------------|
| Central orchestrator | `WorkflowOrchestrator` state machine |
| LLMs as tools | `LLMClient` abstraction, pluggable backends |
| Multi-step pipelines as code | Runtime files parsed into `Step` objects |
| RAG | Process-Retrieval (PRAR) over schemas, not facts |

### Key Insight

> "Keep RCM/PRAR as the governing logic. Turn the 'student' slot into a generated agent. Use a second LLM (or second role) to inhabit that agent, while the first LLM continues to be the Socratic PRAR engine."

---

## 3. Architecture Summary

### Three Deployment Paradigms

```
+------------------+     +------------------+     +------------------+
|   GPT Builder    |     |  Local Python    |     |  Experimental    |
|   (Production)   |     |  Orchestrator    |     |  BIOS + Runtime  |
+------------------+     +------------------+     +------------------+
        |                        |                        |
   Monolithic              Code-enforced            Separated
   8KB System              State Machine            Architecture
   Prompt                  + LLM Client             (Research)
        |                        |                        |
   production/             local_rcm/              experimental/
+------------------+     +------------------+     +------------------+
```

### What Each Paradigm Solves

| Paradigm | Problem Solved | Trade-off |
|----------|---------------|-----------|
| GPT Builder | Zero-code deployment for students | 8KB limit, no customization |
| Local Orchestrator | Full control, GPU options, testing | Requires hosting/setup |
| BIOS + Runtime | Overcomes 8KB limit | Force-read reliability issues |

---

## 3. Deployment Targets

### 3.1 GPT Builder (Production v8.4)

**Location**: `production/`

**Files**:
- `system-prompt/B42 Chatstorm TA System Prompt v8.4-FINAL.txt` (7,994 bytes)
- `knowledge-base/` - 4 assignment docs + 4 theory files
- `deployment/DEPLOYMENT_CHECKLIST.md`

**Status**: Production-ready, actively deployed for students

**Limitations**:
- At 99% of 8KB character limit
- Cannot add new features
- Requires DALL-E disabled in GPT settings

### 3.2 Local Python Orchestrator

**Location**: `local_rcm/`

**Core Files**:
- `orchestrator.py` - Workflow state machine
- `canvas_state.py` - Data model and compilation
- `llm_client.py` - Multi-backend LLM interface
- `runtime_parser.py` - Runtime file parser
- `app.py` - Streamlit web interface
- `runpod_setup.py` - RunPod connectivity test

**Status**: Active development, ready for local/vLLM/RunPod execution

### 3.3 Experimental BIOS Architecture

**Location**: `experimental/bios-architecture/`

**Status**: Research branch - force-read reliability issues

**Purpose**: Overcome 8KB limit by separating BIOS (kernel) from Runtime (instructions)

---

## 4. Local Setup (local_rcm/)

### Directory Structure

```
local_rcm/
├── orchestrator.py          # Core workflow engine (state machine)
├── canvas_state.py          # Data model & compilation
├── llm_client.py            # LLM abstraction (mock/OpenAI/Anthropic/vLLM)
├── runtime_parser.py        # Runtime file parser
├── app.py                   # Streamlit web interface
├── example_usage.py         # CLI entry point
├── runpod_setup.py          # RunPod connectivity test
├── bios_reduced_prompt.txt  # Minimal system instructions
├── requirements.txt         # Dependencies
├── runtime-files/           # 3-phase workflow definitions
│   ├── B42_Runtime_Phase1_Conceptualization.txt
│   ├── B42_Runtime_Phase2_Drafting.txt
│   ├── B42_Runtime_Phase3_Review.txt
│   └── B42_Runtime_Logic_v2.0-COMPLETE.txt
├── tests/                   # Test suite
│   ├── test_full_workflow.py
│   ├── test_realistic.py
│   ├── test_auto.py
│   └── test_simulator.py
└── output/                  # Generated workflows (gitignored)
```

### Installation

```bash
cd local_rcm
pip install -r requirements.txt
```

**Dependencies**:
- `requests>=2.31.0`
- `openai>=1.0.0`
- `anthropic>=0.18.0`
- `streamlit>=1.28.0`

### Running the Local Setup

#### Option 1: CLI with Mock (Testing)
```bash
python example_usage.py --mode mock
```

#### Option 2: CLI with vLLM/RunPod
```bash
python example_usage.py --mode vllm --base-url "https://api.runpod.ai/v2/YOUR_ENDPOINT/openai/v1" --api-key YOUR_KEY
```

#### Option 3: Streamlit Web Interface
```bash
streamlit run app.py
```

### Core Module: orchestrator.py

The `WorkflowOrchestrator` class enforces the BIOS specification:

```python
class WorkflowOrchestrator:
    """
    Main orchestrator that enforces BIOS workflow execution.
    The LLM NEVER controls step advancement. Code owns the state machine.
    """

    def __init__(self, runtime, student_handler, canvas=None, starting_step="1.1.1"):
        self.runtime = runtime
        self.student_handler = student_handler
        self.canvas = canvas or CanvasState()
        self.current_step_id = starting_step
        self.student_state = {}  # step_id -> answer
```

**Key Methods**:
- `run_workflow()` - Execute complete workflow
- `execute_step(step_id)` - Execute single step with validation
- `resolve_next_step()` - Handle conditional routing and loops
- `save_state() / load_state()` - Persist workflow state

### Core Module: llm_client.py

**LLM Providers Supported**:

| Provider | Class | Notes |
|----------|-------|-------|
| Mock | `MockClient` | Testing without API calls |
| OpenAI | `OpenAIClient` | GPT-4, also works with vLLM |
| Anthropic | `AnthropicClient` | Claude models |
| RunPod | `OpenAIClient` | Via OpenAI-compatible API |
| Ollama | `OllamaClient` | Local models |

**Factory Function**:
```python
llm = create_llm_client(
    provider="runpod",  # or "openai", "anthropic", "vllm", "ollama", "mock"
    api_key="your-key",
    model="Qwen/Qwen2.5-7B-Instruct",
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT/openai/v1"
)
```

### Core Module: canvas_state.py

**Data Model**:
```python
@dataclass
class CanvasState:
    project: ProjectInfo           # Goal, concepts, framework
    agents: List[AgentDefinition]  # Agent roster with prompts
    rounds: List[RoundDefinition]  # Round instructions + config
    helpers: HelperFunctions       # Moderator, analyst, etc.
    status: WorkflowStatus         # Phase completion flags
```

**Key Functions**:
- `compile_canvas_from_student_state()` - Build canvas from collected answers
- `compile_final_document()` - Generate exportable document
- `apply_canvas_update()` - Apply runtime updates to canvas

### Core Module: runtime_parser.py

**Step Structure**:
```python
@dataclass
class Step:
    id: str                    # e.g., "1.2.3"
    target: str                # What this step collects
    instruction: str           # Internal guidance
    required_output: str       # Exact question text
    rcm_cue: str               # RCM guidance
    constraint: str            # Validation rules
    next_step: str             # Next step ID or conditional
    canvas_update: Dict        # Canvas update block
```

---

## 5. Production GPT Builder (v8.4)

### System Prompt Structure (7,994 bytes)

```
# B42 Chatstorm T.A. v8.4

## CORE IDENTITY
## ABSOLUTE PROHIBITIONS (5 rules)
## KNOWLEDGE BASE (8 files)
## THEORY QUERIES
## SOCRATIC METHOD (RCM)
## ONE QUESTION AT A TIME RULE
## THREE-PHASE WORKFLOW
  ### PHASE 1: CONCEPTUALIZATION (Steps 1.1-1.8)
  ### PHASE 2: DRAFTING (Steps 2.1-2.3)
  ### PHASE 3: REVIEW & EXPORT
## POSITION TRACKING
## KEY TERMS
## PROTOCOLS
## SUCCESS CRITERIA
```

### Absolute Prohibitions

1. **NO CREATIVE WRITING** - System never writes/paraphrases student ideas
2. **NO BATCHING** - ONE question at a time only
3. **NO PLACEHOLDER ACCEPTANCE** - Rejects `[...]`, "TBD", vague responses
4. **NO TRAINING DATA THEORY** - Uses ONLY KB[5-8] lecture notes
5. **NO FILE CREATION** - Displays in chat with `||...||` markers

### Knowledge Base Files

| KB ID | File | Purpose |
|-------|------|---------|
| KB[1] | B42 Chatstorm T.A. Guide v4.2.txt | Templates |
| KB[2] | B42 Final Project.txt | Assignment requirements |
| KB[3] | B42 Step-by-Step Guide.txt | Workflow phases |
| KB[4] | Appendix A - Required Values Index v3.2.txt | Field definitions |
| KB[5] | marx_theory.txt | Marx theory |
| KB[6] | tocqueville_theory.txt | Tocqueville theory |
| KB[7] | wollstonecraft_theory.txt | Wollstonecraft theory |
| KB[8] | smith_theory.txt | Smith theory |

### Deployment Steps

See `production/deployment/DEPLOYMENT_CHECKLIST.md` for complete steps:
1. Create new GPT in GPT Builder
2. Paste system prompt
3. Upload all knowledge base files
4. Disable DALL-E image generation
5. Test workflow execution

---

## 6. Experimental BIOS Architecture

### Concept

Move from **"Monolithic Prompt"** to **"BIOS + OS"** architecture:

- **BIOS** (~5KB): Prime directives, prohibitions, runtime loop protocol
- **Runtime Files** (unlimited): Detailed step instructions, RCM cues

### Problem Solved

| Aspect | Monolithic (v8.4) | BIOS + Runtime |
|--------|-------------------|----------------|
| Space Constraint | 8,000 byte hard limit | Unlimited runtime file |
| Updates | Risky (full prompt edit) | Easy (edit text file) |
| Scalability | Cannot add features | Can add 100+ steps |

### Current Status

**Version**: v2.3
**Status**: Experimental - NOT recommended for production

**Issues**:
- Force-read reliability problems
- Step-skipping observed in testing
- LLM sometimes doesn't retrieve runtime instructions

### Files

```
experimental/bios-architecture/
├── system-prompts/
│   ├── B42_BIOS_System_Prompt_v2.3-PRODUCTION.txt (5,247 bytes)
│   ├── B42_BIOS_System_Prompt_v2.2-PRODUCTION.txt (aborted)
│   └── B42_BIOS_System_Prompt_v2.1-PRODUCTION.txt
├── runtime-files/
│   ├── B42_Runtime_Phase1_Conceptualization.txt
│   ├── B42_Runtime_Phase2_Drafting.txt
│   └── B42_Runtime_Phase3_Review.txt
└── docs/
    ├── CANVAS_DATA_SCHEMA.md
    ├── FORCE_READ_PROTOCOL.md
    ├── BIOS_vs_MONOLITHIC.md
    └── [other design docs]
```

---

## 7. Data Models & Schemas

### Canvas Data Schema

The canvas accumulates student data progressively:

```json
{
  "project": {
    "goal": "string",
    "theoretical_option": "A|B|C|D|E",
    "theoretical_option_label": "string",
    "concept_a": { "name": "string", "definition": "string" },
    "concept_b": { "name": "string", "definition": "string" },
    "design_approach": "single|two-design",
    "variable": {
      "name": "string",
      "baseline": "string",
      "experimental": "string",
      "rationale": "string"
    },
    "setting": "string",
    "rounds_count": "integer",
    "rounds_plan": "string"
  },
  "agents": [
    {
      "identifier": "[purpose]+[name]",
      "goal": "string",
      "persona": "string",
      "prompt": "string (generated in Phase 2)"
    }
  ],
  "rounds": [
    {
      "round_number": "integer",
      "scenario": "string",
      "concept_a_manifestation": "string",
      "concept_b_manifestation": "string",
      "rules": "string",
      "tasks": "string",
      "sequence": "string",
      "platform_config": {
        "participants": "string",
        "who_sends": "All|Moderator",
        "order": "Default|Random|Active|Moderator",
        "end_condition": "string",
        "transition": "Pause|Auto|Moderator",
        "detail_level": "Min|Brief|Med|Thor|Exh|Dyn",
        "creativity": "string",
        "ask_questions": "boolean",
        "self_reflection": "boolean",
        "model": "string"
      }
    }
  ],
  "helpers": {
    "moderator_function": "string",
    "analyst_function": "string",
    "non_anthropomorphic_cues": "string",
    "self_reflection_prompts": "string"
  },
  "status": {
    "phase1_complete": "boolean",
    "phase2_complete": "boolean",
    "phase3_complete": "boolean",
    "ready_for_export": "boolean"
  }
}
```

### Theoretical Framework Options

| Option | Name | Theorists | Key Concepts |
|--------|------|-----------|--------------|
| A | Class Conflict / Alienation | Marx, Wollstonecraft | alienation, exploitation, patriarchy, domination |
| B | Cultural Systems | Tocqueville | equality, tyranny of majority, conformity |
| C | Institutional Power | Marx, Tocqueville | revolution, class consciousness, conformity |
| D | Network Dynamics | Smith, Tocqueville | commerce, self-interest, equality |
| E | Custom Framework | Student-defined | Variable |

---

## 8. LLM Client Architecture

### StudentInteractionHandler

Wraps LLM client for Socratic interactions:

```python
class StudentInteractionHandler:
    def __init__(self, llm_client, bios_prompt):
        self.llm = llm_client
        self.bios_prompt = bios_prompt
        self.chosen_framework = None  # Set after step 1.2.1

    def ask_question(self, required_output, rcm_cue, context) -> str
    def validate_answer(self, answer, constraint, target) -> Dict
    def validate_framework_coherence(self, answer) -> Dict
    def remediate_answer(self, answer, validation, required_output) -> str
```

### StudentSimulator

For automated testing and demos:

```python
class StudentSimulator:
    """Simulates a student responding to Socratic questions."""

    def __init__(self, llm_client, persona=None):
        self.llm = llm_client
        self.persona = persona or STUDENT_PERSONA
        self.conversation_history = []

    def set_framework(self, option)  # Update persona after option selection
    def respond(self, question) -> str  # Generate student response
    def get_input_function()  # Returns function for orchestrator
```

### Framework-Specific Personas

The simulator updates its persona after the student selects a theoretical option to ensure framework coherence:

```python
FRAMEWORK_PERSONAS = {
    "A": """You chose Option A: Class Conflict / Alienation (Marx + Wollstonecraft).
YOUR THEORETICAL TOOLKIT: alienation, exploitation, class conflict, patriarchy...
STRICT RULE: Do NOT reference Tocqueville or Smith.""",
    # ... etc for B, C, D, E
}
```

---

## 9. Runtime Files & Workflow

### Three-Phase Workflow

**Phase 1: Conceptualization** (Steps 1.1-1.8)
- Welcome and storyboard check
- Theoretical framework selection
- Concept A/B definitions
- Experiment structure
- Baseline/experimental design
- Setting and rounds
- Agent roster and details
- Advanced functions selection
- Section 1 compilation

**Phase 2: Drafting** (Steps 2.1-2.3)
- Agent prompts (one per agent)
- Round instructions (scenario, rules, tasks)
- Platform configuration (per round)
- Helper templates (moderator, analyst, etc.)

**Phase 3: Review & Export** (Steps 3.1-3.3)
- Checklist verification
- Final document compilation
- Export options

### Step Structure in Runtime Files

```
### [STEP 1.2.3]
TARGET: Concept A Definition
INSTRUCTION: Ask student to define the first concept in their theoretical tension.
REQUIRED OUTPUT: "[Concept A]: Define from [theory]. How manifest in interactions? (2-3 sent.)"
RCM CUE:
- Reflect: "What are the key features of [Concept A]?"
- Connect: "How would agents experience this in interactions?"
- Ask: "What specific behaviors or outcomes would signal [Concept A] is present?"
CONSTRAINT:
- Must be 2-3 sentences
- Must reference the theorist's definition
- Must explain how it manifests
THEORY CHECK: YES - Search KB[5-8] for this concept
CANVAS_UPDATE: { "section": "project", "action": "update", ... }
NEXT STEP: 1.2.4
```

### Conditional Routing

The orchestrator handles several types of conditional routing:

1. **Type A/B Branching** (at 1.3.1): Based on answer to 1.2.6
2. **Round Loops** (at 1.4.3): Repeats for each round
3. **Agent Loops** (at 1.5.2/1.5.3, 1.6.1-1.6.3): Repeats for each agent
4. **Phase 2 Round Loop** (at 2.2.19): Repeats round instructions for each round

---

## 10. Testing Infrastructure

### Test Files

| File | Purpose | Mode |
|------|---------|------|
| `test_realistic.py` | Phase 1 with realistic answers | Mock or vLLM |
| `test_full_workflow.py` | Complete Phase 1-3 | Mock |
| `test_auto.py` | Automated testing | Any LLM |
| `test_simulator.py` | Student simulator testing | Any LLM |

### Running Tests

```bash
# Mock mode (no API)
python tests/test_realistic.py --mock

# With vLLM/RunPod
python tests/test_realistic.py --base-url "https://..." --api-key "..."

# Full workflow test
python tests/test_full_workflow.py
```

### Realistic Test Data

`test_realistic.py` includes a complete set of realistic student answers for an alienation vs. non-domination project:

```python
STUDENT_ANSWERS = {
    "1.2.1": "A",  # Option A: Class Conflict / Alienation
    "1.2.2": "I want to model how workers lose control over their labor...",
    # ... complete answers for Phase 1
}
```

---

## 11. GPU/Cloud Options

### Option 1: RunPod Serverless (Recommended)

**Setup**:
1. Create RunPod account at runpod.io
2. Deploy Serverless vLLM endpoint:
   - Template: vLLM
   - Model: `Qwen/Qwen2.5-7B-Instruct` (or similar)
3. Get API key from Settings > API Keys
4. Get endpoint URL: `https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1`

**Test Connection**:
```bash
python runpod_setup.py --endpoint-id YOUR_ID --api-key YOUR_KEY
```

**Usage**:
```python
llm = create_llm_client(
    provider="runpod",
    api_key="rp_xxxxxxxx",
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT/openai/v1",
    model="Qwen/Qwen2.5-7B-Instruct"
)
```

### Option 2: Google Colab + VSCode Extension

**Requirements**:
- Google Colab Pro (for GPU access)
- VSCode with Jupyter extension

**Steps**:
1. Install Colab extension in VSCode
2. Connect to Colab runtime
3. Install vLLM in Colab notebook
4. Use Colab's GPU for inference

### Option 3: Local vLLM Server

**Requirements**:
- Local NVIDIA GPU (8GB+ VRAM)
- vLLM installed locally

**Setup**:
```bash
pip install vllm
vllm serve Qwen/Qwen2.5-7B-Instruct --port 8000
```

**Usage**:
```python
llm = create_llm_client(
    provider="vllm",
    base_url="http://localhost:8000/v1",
    model="Qwen/Qwen2.5-7B-Instruct"
)
```

### Option 4: Ollama (Lightweight Local)

**Requirements**:
- Ollama installed
- Less powerful model (fits on CPU or small GPU)

**Setup**:
```bash
ollama pull gemma:2b
ollama serve
```

**Usage**:
```python
llm = create_llm_client(
    provider="ollama",
    model="gemma:2b",
    base_url="http://localhost:11434"
)
```

---

## 12. Current Status & Known Issues

### Production (v8.4)

**Status**: Stable, deployed

**Known Issues**:
- Image generation requires DALL-E disabled
- At 99% character capacity (7,994/8,000 bytes)
- Cannot add new features without compression

### Local Orchestrator

**Status**: Active development

**Known Issues**:
- Runtime file path hardcoded to `B42_Runtime_Logic_v2.0-COMPLETE.txt`
- Some canvas update logic is placeholder
- Need to verify all loop counters work correctly

**Working Features**:
- Mock mode testing
- RunPod integration
- Streamlit web interface
- Student simulator with framework personas
- Canvas compilation and export

### Experimental BIOS

**Status**: Research only

**Known Issues**:
- Force-read protocol unreliable
- Step-skipping observed
- NOT recommended for production

---

## 14. Development Roadmap

### Phase 0: Foundation (Current Priority)

**Goal**: Get local_rcm running reliably with GPU backend

1. **Verify local_rcm works end-to-end with RunPod**
   - Test full Phase 1-3 workflow
   - Verify canvas compilation
   - Test export functionality

2. **Fix runtime file path issue**
   - Currently expects `B42_Runtime_Logic_v2.0-COMPLETE.txt`
   - Should gracefully handle 3 phase files

3. **Test with Colab VSCode extension** (alternative GPU option)
   - Document Colab setup process
   - Verify GPU inference works

### Phase 1: Dual-LLM B42 Mode

**Goal**: Generate student agents from theoretical option selection

1. **Refactor StudentSimulator into AgentSimulator**
   - Accept `AgentConfig` dataclass
   - Generalize persona generation
   - Support different LLM backends for coach vs agent

2. **Add dual LLMClient support to orchestrator**
   ```python
   class WorkflowOrchestrator:
       def __init__(self, ..., coach_llm, agent_llm=None):
           self.coach_llm = coach_llm
           self.agent_llm = agent_llm or coach_llm  # Fallback to single model
   ```

3. **Implement AgentConfig factory**
   - Input: Option A-E selection
   - Output: Full agent persona config
   - System prompt, constraints, theoretical vocabulary

4. **Test dual-LLM workflow**
   - Coach generates Socratic questions
   - Agent responds as framework-specific student
   - Verify canvas compilation and export

### Phase 2: Generalization

**Goal**: Abstract agent generation beyond B42

1. **Create AgentFactory interface**
   ```python
   class AgentFactory(ABC):
       @abstractmethod
       def create_agent(self, config: dict) -> AgentConfig

   class B42AgentFactory(AgentFactory):
       def create_agent(self, option: str) -> AgentConfig

   class CESAgentFactory(AgentFactory):
       def create_agent(self, survey_row: dict) -> AgentConfig
   ```

2. **Create RuntimeSchema interface**
   - B42 workflow (current 3-phase)
   - CES survey experiment workflow
   - Generic multi-round process schema

3. **Add batch agent simulation**
   - Run N agents through same process schema
   - Aggregate results for analysis
   - Support parallel execution

### Phase 3: Research Platform

**Goal**: Full CES-style population simulation

1. **CES data integration**
   - Parse CES survey data
   - Generate agent configs from demographics
   - Map ideology, prior vote, etc. to persona elements

2. **Experimental runtime schemas**
   - Baseline survey round
   - Treatment/stimulus exposure
   - Post-treatment response measurement

3. **Analysis and export**
   - Structured output for statistical analysis
   - Behavioral trace logging
   - Comparison to real survey data

### Infrastructure Enhancements (Ongoing)

1. **Improve canvas update logic**
   - Currently simplified/placeholder
   - Should fully parse CANVAS_UPDATE blocks

2. **Add conversation history to Streamlit**
   - Currently limited to last 10 messages
   - Add export of full conversation

3. **Framework coherence validation**
   - Currently keyword-based
   - Could use LLM for semantic validation

4. **API wrapper (for future Custom GPT Actions)**
   - FastAPI/Flask wrapper around orchestrator
   - Expose endpoints for external callers

---

## 15. Quick Reference

### Key Commands

```bash
# Install dependencies
cd local_rcm && pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py

# Test with mock
python example_usage.py --mode mock

# Test RunPod connection
python runpod_setup.py --endpoint-id XXX --api-key YYY

# Run realistic test
python tests/test_realistic.py --mock
```

### Important Paths

| Path | Purpose |
|------|---------|
| `local_rcm/orchestrator.py` | Main workflow engine |
| `local_rcm/llm_client.py` | LLM client implementations |
| `local_rcm/app.py` | Streamlit web interface |
| `local_rcm/runtime-files/` | Workflow step definitions |
| `production/system-prompt/` | GPT Builder system prompt |
| `b42_theory_library/` | [B42-Pedagogy] Theory texts for student exercises |

### Environment Variables (if needed)

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
RUNPOD_API_KEY=rp_...
```

---

## 16. Social Aesthetics: 2×2×2 Architecture Sweep Results

### Experimental Design

A full 2×2×2 factorial experiment testing the **Social Aesthetics** framework's core hypothesis: that architectural configuration systematically shapes semiotic regimes in multi-agent deliberation.

**Factors**:
| Factor | Levels | Description |
|--------|--------|-------------|
| Challenge Mode | off / always | Whether Coach injects dissent/provocation |
| Context Mode | progressive / adaptive | Static accumulation vs émile-style existential pressure |
| LLM Configuration | dual / single | TRUE dual (14B Performer + 7B Coach) vs single model |

**Conditions (8 total)**:
| Condition | Challenge | Context | LLM | H-Prediction |
|-----------|-----------|---------|-----|--------------|
| A | off | progressive | dual | Baseline |
| B | off | progressive | single | Baseline |
| C | off | adaptive | dual | Active Contestation |
| D | off | adaptive | single | Active Contestation |
| E | always | progressive | dual | Stimulated Dialogue |
| F | always | progressive | single | Stimulated Dialogue |
| G | always | adaptive | dual | **Productive Dissonance (H5)** |
| H | always | adaptive | single | Productive Dissonance |

### Sweep Results (Seed 1, 2025-11-24)

**Full 2×2×2 sweep completed** with TRUE dual-LLM (14B Performer + 7B Coach on separate RunPod endpoints):

| Cond | Challenge | Context | LLM | R1 | R2 | R3 |
|------|-----------|---------|-----|-----|-----|-----|
| A | off | progressive | dual | UNKNOWN | UNKNOWN | ACTIVE_CONTESTATION |
| B | off | progressive | single* | UNKNOWN | UNKNOWN | STIMULATED_DIALOGUE |
| C | off | adaptive | dual | **ENGAGED_HARMONY** | UNKNOWN | UNKNOWN |
| D | off | adaptive | single* | UNKNOWN | UNKNOWN | UNKNOWN |
| E | always | progressive | dual | UNKNOWN | ACTIVE_CONTESTATION | UNKNOWN |
| F | always | progressive | single* | STIMULATED_DIALOGUE | UNKNOWN | STIMULATED_DIALOGUE |
| G | always | adaptive | dual | **ENGAGED_HARMONY** | UNKNOWN | ACTIVE_CONTESTATION |
| H | always | adaptive | single* | STIMULATED_DIALOGUE | UNKNOWN | ACTIVE_CONTESTATION |

*Note: B, D, F, H ran as pseudo-dual (same model both roles) rather than true single-LLM. Re-run needed with `--no-dual-llm` flag.

**Key Observations**:
- **ENGAGED_HARMONY validated**: Detected in C(R1) and G(R1) - both ADAPTIVE + Dual conditions
- **No pathological collapse**: Zero PATERNALISTIC_HARMONY or PROCEDURALIST_RETREAT across all conditions
- **High UNKNOWN rate**: Many rounds fell outside defined regime thresholds (especially justification at 67%)
- **No divergence injections**: Émile-style infrastructure ready but never triggered (engagement stayed high)

### Key Finding: H5 Falsified, ENGAGED_HARMONY Discovered

**Condition G seed 1 (G1)** was the critical test case for H5:
- **Hypothesis H5**: ADAPTIVE + challenge ON + dual-LLM → PRODUCTIVE_DISSONANCE in R3
- **Observed**: ADAPTIVE + challenge ON + dual-LLM → **ENGAGED_HARMONY** in R3

**G1 Round 3 Metrics**:
```
engagement       = 0.73  (high - within 0.5-1.0)
voice_valence    = 1.0   (all empowered, no alienation)
stance_valence   = 1.0   (all bridging, no dismissive)
justificatory_pct = 0.42 (moderate - "balanced justification" band)
```

**Why UNKNOWN classification**: These values fall OUTSIDE the PRODUCTIVE_DISSONANCE signature:
- voice_valence = 1.0 but PD requires (0.0, 0.5)
- stance_valence = 1.0 but PD requires (0.3, 0.7)

### New Regime: ENGAGED_HARMONY

Added to `experiments/social_aesthetics_regimes.py` as the 6th regime:

```python
# ENGAGED_HARMONY - High engagement genuine consensus (non-pathological)
# Key differentiator from PATERNALISTIC_HARMONY: engagement STAYS HIGH
RegimeSignature(
    engagement_range=(0.5, 1.0),       # High engagement (vs PH's low)
    voice_valence_range=(0.5, 1.0),    # Strongly empowered
    stance_valence_range=(0.8, 1.0),   # High bridging
    justificatory_pct_range=(0.3, 0.6) # Moderate justification
)
```

**Conceptual distinction**:
- **ENGAGED_HARMONY**: Genuine constructive consensus with HIGH engagement
- **PATERNALISTIC_HARMONY**: Pseudo-consensus with LOW engagement (withdrawal)

### Revised Regime Typology

| Regime | Type | Key Signature |
|--------|------|---------------|
| ACTIVE_CONTESTATION | Healthy | High engagement, mixed voice, mixed stance |
| ENGAGED_HARMONY | **Healthy** | High engagement, positive voice, high bridging |
| PRODUCTIVE_DISSONANCE | Aspirational | Moderate engagement, mixed voice, balanced stance |
| STIMULATED_DIALOGUE | Transitional | Variable - may collapse |
| PATERNALISTIC_HARMONY | Pathological | **LOW** engagement, positive voice, high bridging |
| PROCEDURALIST_RETREAT | Pathological | Defensive withdrawal, high justification |

### Hypothesis Status Update

| Hypothesis | Prediction | Status | Evidence |
|------------|------------|--------|----------|
| **H1** | Baseline → Paternalistic Harmony or Proceduralist Retreat | NOT SUPPORTED | B produced STIMULATED_DIALOGUE, not pathology |
| **H2** | Challenge ON → higher engagement | PARTIALLY SUPPORTED | Challenge ON showed more ACTIVE_CONTESTATION |
| **H3** | ADAPTIVE → avoids Proceduralist Retreat | SUPPORTED | Zero PROCEDURALIST_RETREAT in any condition |
| **H4** | Dual-LLM → sustains tension better | PARTIALLY SUPPORTED | Dual showed ENGAGED_HARMONY; single showed STIMULATED_DIALOGUE |
| **H5** | ADAPTIVE + challenge + dual → Productive Dissonance | **NOT SUPPORTED** | G produced ENGAGED_HARMONY, not PRODUCTIVE_DISSONANCE |
| **H5b** | ADAPTIVE + challenge + dual → Non-pathological regime | **SUPPORTED** | G avoided all pathological collapse |

**Key Theoretical Insight**: The convergence to ENGAGED_HARMONY rather than PRODUCTIVE_DISSONANCE reveals that agents lack **identity salience** - there's nothing constitutionally at stake when they compromise.

### Theoretical Interpretation: Identity Salience

The convergence to ENGAGED_HARMONY (rather than maintained disagreement) suggests a deeper issue: **agents lack identity salience**.

Drawing on Weber's sociogeographic theory:
- Human identity is grounded in **place** - a bidirectional tie where one's presence distinguishes and is distinguished by context
- Identity elements must be **expressed into context and validated by that context**
- Without this grounding, cooperation is costless - there's nothing constitutionally violated by changing positions

**Current agents have**:
- CES demographic profiles (thin signifier)
- No existential stake in positions (no tie-to-place)
- No accumulated history of enaction in context

**Future architecture implication**: To achieve true PRODUCTIVE_DISSONANCE, agents need:
- SociogeographicBody (position, tie-to-place, affordances)
- Identity enaction scoring (how much one has invested in context)
- Validation mechanisms (context confirms/disconfirms identity)

See `emile_reference_files/embodied_qse_emile.py` for the architectural pattern that could ground agents in place.

---

## 17. Session Log

### 2025-11-22 - Initial Comprehensive Audit

**Session Goals**:
- Perform exhaustive audit of entire codebase
- Understand all components and their relationships
- Create this working document

**Completed**:
- Explored all directories and key files
- Analyzed Custom GPT v8.4 system prompt
- Examined local orchestrator architecture
- Reviewed LLM client implementations
- Analyzed runtime file structure
- Reviewed testing infrastructure
- Examined experimental BIOS architecture
- Created this comprehensive working document

**Key Findings**:
1. Local setup is functional with mock mode
2. RunPod integration is ready to test
3. Canvas compilation works but has placeholder logic
4. Experimental BIOS has reliability issues
5. Production v8.4 is at capacity limit

---

### 2025-11-23 - Social RL Framework Complete + RunPod GPU Integration

**Session Goals**:
- Complete Social RL framework implementation
- Integrate Dual-LLM Coach/Performer architecture
- Deploy GPU-accelerated inference via RunPod Pod
- Run robust experiments validating the relational dynamics framework

**Completed**:

1. **Social RL Framework (Phase 2.5)**
   - `SocialRLRunner`: Main execution engine integrating all components
   - `ContextInjector`: Dynamic per-turn manifestation generation
   - `SocialFeedbackExtractor`: Extract engagement, alignment, contribution
   - `ProcessRetriever`: PRAR-based reasoning policy with adaptation
   - `DualLLMClient`: Coach (temp=0.1) validates Performer (temp=0.7) outputs

2. **Relational Dynamics Metrics (`social_rl/metrics.py`)**
   - Participation asymmetry (worker vs owner ratios)
   - Justification density (owner utterances with reasons)
   - Domination markers ("that's final", "because I said so")
   - Alienation markers ("just doing my job", "I suppose")
   - Automatic computation and `metrics.json` output

3. **Experiment CLI (`experiments/run_social_rl_experiment.py`)**
   - Supports: mock, ollama, openai, vllm providers
   - Custom `--experiment-id` for descriptive output naming
   - Auto-saves: `meta.json`, `metrics.json`, round results, policy state
   - Git commit hash captured for reproducibility

4. **RunPod GPU Integration**
   - Deployed A40 GPU Pod with vLLM serving Qwen2.5-7B-Instruct
   - Pod endpoint: `https://dinz851kfl1ztt-644118d9-8000.proxy.runpod.net/v1`
   - ~10 seconds per LLM call vs minutes on CPU
   - Successfully ran multiple parallel experiments

**Key Experimental Results**:

| Experiment | Rounds | Dual-LLM | Messages | Duration | Key Finding |
|------------|--------|----------|----------|----------|-------------|
| robust_test_12turns | 1 | Yes | 12 | 124s | Baseline metrics established |
| robust_test_no_dual_llm | 1 | No | 9 | ~90s | Comparison without validation |
| **robust_test_2rounds_prar** | 2 | Yes | 18 | 218s | **Alienation markers: 3 → 0** |

**Critical Finding**: The 2-round experiment (`robust_test_2rounds_prar`) showed:
- Round 1 (Baseline Alienation): 3 alienation markers from Worker+Alice ("I suppose")
- Round 2 (Reduced Domination): 0 alienation markers

This is exactly the measurable shift GPT recommended for the Social Aesthetics paper:
> "When we flip one architectural rule—from arbitrary power to constrained power with justification—the system produces measurable shifts in alienation-coded speech."

**Files Modified**:
- `social_rl/runner.py`: Added `experiment_id` parameter for output naming
- `experiments/run_social_rl_experiment.py`: Full CLI with all providers
- `social_rl/metrics.py`: Relational dynamics metrics computation
- `experiments/README.md`: Documentation for running experiments

**Current Architecture**:
```
PRAR State (112-step workflow)
    ↓
Canvas (agents, rounds, rules)
    ↓
SocialRLRunner
    ├── ContextInjector (dynamic manifestations)
    ├── FeedbackExtractor (social signals)
    ├── ProcessRetriever (policy guidance)
    └── DualLLMClient (Coach + Performer)
            ↓
        vLLM/RunPod
        (Qwen2.5-7B-Instruct)
            ↓
        Validated Output
            ↓
        Metrics + Transcripts
```

**Next Steps**:
1. Run extended 3-round experiment with Analyst round
2. Generate multiple runs for statistical stability
3. Implement behavioral metrics extraction for paper
4. Prepare reproducibility package for publication

---

### 2025-11-22 - Vision Integration (chat_gpt_debrief.txt)

**Session Goals**:
- Ingest ChatGPT conversation about project vision
- Understand dual-LLM architecture goals
- Update working document with roadmap

**Key Insights from Debrief**:

1. **This is a mini-CQB**: The project implements CQB principles with PRAR as the governance model. Orchestrator owns state, LLMs are IO devices.

2. **Dual-LLM Architecture Vision**:
   - LLM #1 (Coach): Continues PRAR/RCM function
   - LLM #2 (Agent): Generated persona (student, CES respondent)
   - Same orchestrator governs both

3. **Evolution Path**:
   - Current: Human student + Socratic LLM
   - Near: Generated student agent + Coach LLM
   - Future: N synthetic agents (CES demographics) + Coach LLM

4. **Existing Proto-Agent**: `StudentSimulator` with framework personas is the foundation for agent generation

5. **Generalization Strategy**:
   - AgentConfig/AgentFactory layer
   - RuntimeSchema abstraction (B42, CES, etc.)
   - Same PRAR orchestrator underneath

**Updated Roadmap**:
- Phase 0: Foundation (get RunPod working)
- Phase 1: Dual-LLM B42 mode
- Phase 2: Generalization (AgentFactory, RuntimeSchema)
- Phase 3: Research platform (CES simulation)

**Next Steps**:
1. Test RunPod integration end-to-end
2. Verify existing auto-mode/simulator tests
3. Begin Phase 0 foundation work

---

### 2025-11-24 - ENGAGED_HARMONY Discovery & H5 Falsification

**Session Goals**:
- Analyze Condition G seed 1 (G1) results from 2×2×2 architecture sweep
- Understand why G1 was classified as UNKNOWN instead of PRODUCTIVE_DISSONANCE
- Update regime typology based on empirical findings
- Document theoretical implications for agent identity architecture

**Completed**:

1. **G1 Deep Analysis**
   - Reviewed semiotic_state_log.json: R1=ACTIVE_CONTESTATION, R2-R3=UNKNOWN
   - Analyzed R3 metrics: eng=0.73, voice=1.0, stance=1.0, just=0.42
   - Diagnosed: values fall OUTSIDE PRODUCTIVE_DISSONANCE ranges
   - Identified pattern: genuine constructive consensus, not maintained disagreement

2. **New Regime: ENGAGED_HARMONY**
   - Added to `experiments/social_aesthetics_regimes.py` as 6th regime
   - Key differentiator from PATERNALISTIC_HARMONY: engagement stays HIGH
   - Signature: high engagement + positive voice + high bridging + moderate justification
   - Updated priority order in `identify_regime()` function

3. **H5 Hypothesis Update**
   - H5 (original): ADAPTIVE + challenge + dual-LLM → Productive Dissonance
   - Status: NOT SUPPORTED (falsified by G1)
   - H5b (new): ADAPTIVE + challenge + dual-LLM → Non-pathological regime
   - Status: SUPPORTED (G1 avoided pathological collapse)

4. **Theoretical Framework Extension**
   - Identified root cause: agents lack "identity salience" (Weber's tie-to-place)
   - Added `embodied_qse_emile.py` to `emile_reference_files/` as architectural pattern
   - Documented future direction: SociogeographicBody for grounded agents

**Key Files Modified**:
- `experiments/social_aesthetics_regimes.py` - Added ENGAGED_HARMONY regime, H5b hypothesis
- `WORKING_DOCUMENT.md` - Added Section 16 on Architecture Sweep Results
- `Dev Copy - Social Aesthetics...v3.txt` - Added Section 4 empirical findings

**Key Finding**:
> Condition G produced ENGAGED_HARMONY (non-pathological convergence) rather than PRODUCTIVE_DISSONANCE (maintained disagreement). This falsifies H5 as written but supports the broader Social Aesthetics claim that architecture systematically shapes semiotic fields. The finding also reveals that current agents lack the identity salience needed for true positional commitment.

**Remaining Tasks**:
- Re-run B, D, F, H with `--no-dual-llm` flag (currently pseudo-dual, not true single-LLM)
- Tune regime thresholds (high UNKNOWN rate suggests justification band 0.3-0.6 too narrow)
- Add more seeds for statistical power (currently seed 1 only)
- Implement identity salience (tie_to_place, symbolic self) for agents

---

### 2025-11-24 (Continued) - Full Sweep Completion & Repository Sync

**Session Goals**:
- Complete and verify full 2×2×2 architecture sweep
- Commit all experimental outputs and documentation to GitHub
- Update WORKING_DOCUMENT.md with current state

**Completed**:

1. **Full 2×2×2 Sweep Executed**
   - All 8 conditions (A-H) run with TRUE dual-LLM (14B Performer + 7B Coach)
   - Results saved to `outputs/full_sweep_A/` through `outputs/full_sweep_H/`
   - ENGAGED_HARMONY detected in C(R1) and G(R1)
   - No pathological collapse in any condition

2. **Issue Identified: Single-LLM Conditions**
   - B, D, F, H were supposed to be single-LLM but ran as pseudo-dual
   - `dual_llm: true` but `true_dual_llm: null` in meta.json
   - Need re-run with explicit `--no-dual-llm` flag

3. **Repository Synchronized**
   - Committed émile infrastructure + sweep results (commit 50d0bb3)
   - Committed all experimental outputs + documentation (commit a9d8b37)
   - 183 files, 28,103 insertions pushed to GitHub

4. **Documentation Updated**
   - `todo` file: Full ChatGPT conversation about project evolution
   - `catchup` file: Session summary for context continuity
   - `generalizing_on_ces`: CES generalization notes
   - This WORKING_DOCUMENT.md: Updated with sweep results

**Key Files Added**:
- `emile_reference_files/` - Émile patterns for identity grounding
- `experiments/social_aesthetics_regimes.py` - 6-regime classifier
- `experiments/run_ces_experiment.py` - Full 2×2×2 runner
- `social_rl/context_injector.py` - Émile-style SemioticStateTracker

**Infrastructure Now Available**:
```
ADAPTIVE Mode = PROGRESSIVE + émile-style existential pressure + hysteresis
├── EMA smoothing (α=0.35)
├── Collapse detection (PATERNALISTIC_HARMONY, PROCEDURALIST_RETREAT)
├── Min dwell rounds (2)
├── Collapse confirmation rounds (2)
└── Divergence injection when collapse confirmed
```

**Next Steps**:
1. Re-run B, D, F, H with true single-LLM (`--no-dual-llm`)
2. Tune regime thresholds to reduce UNKNOWN classifications
3. Add seeds 2-5 for statistical validation
4. Port identity salience from `embodied_qse_emile.py`

---

### 2025-11-24 (Session 3) - Multi-Seed Sweep Complete & Identity Metrics Implemented

**Session Goals**:
- Fix Ollama 404 connectivity errors in multi-seed runs
- Complete full seed 2-3 sweep with valid data
- Derive identity_salience + tie_to_place metrics from CES profiles

**Completed**:

1. **Diagnosed Connectivity Issue**
   - Recent runs (G_seed2-5, A-H seed2-3) had Ollama 404 errors
   - Root cause: Commands defaulted to `--provider ollama` instead of `--provider vllm`
   - Fixed by explicitly specifying RunPod endpoints

2. **Re-ran All Experiments with Proper Endpoints**
   - G seeds 2-5: TRUE dual-LLM (14B Performer + 7B Coach)
   - A-H seeds 2-3: Full 2×2×2 sweep
   - All outputs saved to `outputs/*_fixed/` directories

3. **Multi-Seed Results Summary**

   **G Seeds (ENGAGED_HARMONY Replication)**:
   | Seed | R1 | R2 | R3 |
   |------|-----|-----|-----|
   | G1 (sweep) | SD | SD | UN |
   | G2 | **EH** | UN | **EH** |
   | G3 | **EH** | UN | SD |
   | G4 | **EH** | UN | AC |
   | G5 | **EH** | - | - |

   **Result: 4/4 fixed seeds show ENGAGED_HARMONY in Round 1 (100% replication)**

   **Full Seed 2-3 Results**:
   | Cond | S2 R1 | S2 R3 | S3 R1 | S3 R3 | EH Count |
   |------|-------|-------|-------|-------|----------|
   | A | UN | UN | **EH** | UN | 1 |
   | B | **EH** | **EH** | UN | SD | 2 |
   | C | UN | - | UN | AC | 0 |
   | D | **EH** | AC | **EH** | SD | 2 |
   | E | SD | **EH** | **EH** | UN | 2 |
   | F | **EH** | UN | **EH** | AC | 2 |
   | G | **EH** | **EH** | **EH** | SD | 3 |
   | H | UN | - | UN | UN | **0** |

   **Key Findings**:
   - **G produces EH most reliably** (3 instances across 2 seeds)
   - **H never produces EH** (0/6 rounds) - single-LLM + adaptive is problematic
   - **Round 1 EH rate**: 56% (9/16 observations)
   - **Round 2 is transition**: almost always UNKNOWN

4. **Identity Metrics Implemented**

   Created `agents/ces_generators/identity_metrics.py` with:
   - `compute_identity_salience()`: partisanship + turnout + ideological clarity
   - `compute_tie_to_place()`: urban/rural + birthplace + age + income
   - `get_identity_category()`: rooted_partisan, urban_engaged, settled_swing, unanchored

   **Agent Identity Profiles**:
   | Agent | Salience | Tie | Category |
   |-------|----------|-----|----------|
   | Urban Progressive | 0.83 | 0.55 | urban_engaged |
   | Suburban Swing | 0.20 | 0.78 | settled_swing |
   | Rural Conservative | 0.83 | 0.90 | **rooted_partisan** |
   | Disengaged Renter | 0.17 | 0.48 | unanchored |

**Key Files Added**:
- `agents/ces_generators/identity_metrics.py` - Identity salience derivation
- `outputs/*_fixed/` - 16 fixed experiment outputs

**Theoretical Insight**:
The identity metrics now enable the G-identity experiment proposed in `notes/Next`:
- G-base: current G settings
- G-identity: when `identity_salience` and `tie_to_place` are both high, add prompt nudge to maintain positional commitment

**Next Steps**:
1. ~~Implement G-identity variant with identity-aware prompts~~ **COMPLETED** (see Session 4 below)
2. Run G-base vs G-identity comparison (ready to test)
3. Update Section 4 of Social Aesthetics paper with multi-seed results

---

### Session 4 - 2025-11-24: Grit Constraint Implementation

**Context**: Gemini's analysis of `gemini_on_vectors` identified the "Vector Gap" problem - the Disengaged Renter showed `engagement=0.80` (Posterior) vs `0.17` (Prior from CES profile). This revealed **hyper-enfranchisement**: low-salience agents were acting like model citizens due to LLM "Toxic Positivity."

**Diagnosis**:
- **The Vector Logic**: `Faith = 1.0 - (Critical_Concepts / Total)` misdiagnosed silence as faith
- **Reality**: Disengaged Renter was too polite to use critical concepts
- **Mechanism**: `[REFLECT]` and `[OBSERVE]` PRAR cues acted as cognitive stimulants
- **Result**: Architecture forced agents to become model citizens, overwriting sociology

**Solution - Grit Constraint**:

Implemented architectural resistance for low-salience agents in `agents/ces_generators/`:

1. **Enhanced `identity_metrics.py`**:
   - Added support for both raw CES 2021 codes (`cps21_*`) and normalized Parquet variables
   - New variables: `cps25_interest_gen_1`, `cps25_aff_pid`, `pes25_parents_born`
   - Created `needs_grit_constraint(metrics, threshold=0.3)` function

2. **Updated `row_to_agent.py`**:
   - Import identity metrics into constraint generation pipeline
   - Compute `identity_salience` before generating prompts
   - If salience < 0.3, inject skepticism constraint:
     ```
     GRIT: You are deeply skeptical of this process. You believe talking
     changes nothing. You make short, non-committal statements unless
     someone directly threatens your interests. You need strong evidence
     before engaging substantively.
     ```

**Test Results** (from `test_grit_constraint.py`):

| Agent | Salience | Grit Injected? |
|-------|----------|----------------|
| Urban Progressive | 0.83 | NO |
| Suburban Swing | 0.20 | **YES** |
| Rural Conservative | 0.83 | NO |
| Disengaged Renter | 0.17 | **YES** |

**Theoretical Significance**:
- This is the first **architectural intervention** targeting LLM inherent helpfulness bias
- If grit constraint succeeds → validates Social Aesthetics (architecture shapes behavior)
- If LLMs override grit constraint → proves "Toxic Positivity" as a fundamental limitation

**Ready for Experiment**:
- G-base: Current G configuration (no identity awareness)
- G-identity: G + grit constraints for low-salience agents
- Hypothesis: G-identity will show Disengaged Renter with engagement ~0.2 (not 0.8)

**Files Modified**:
- `agents/ces_generators/identity_metrics.py` - Added Parquet support and `needs_grit_constraint()`
- `agents/ces_generators/row_to_agent.py` - Grit constraint injection in `_generate_constraints()`
- `agents/ces_generators/__init__.py` - Export `needs_grit_constraint`

**Test Files Created**:
- `test_grit_constraint.py` - Verify constraint injection for 4 standard agents
- `test_grit_canvas_output.py` - Show full canvas output with grit constraint

---

## Appendix A: File Count by Directory

```
production/           ~10 files (system prompt + knowledge base)
local_rcm/            ~20 files (orchestrator + tests)
experimental/         ~30 files (BIOS versions + docs)
b42_theory_library/   4 files [B42-Pedagogy] (theorist lecture notes for student exercises)
docs/                 ~15 files (architecture + research docs)
literature/           11 files (academic papers)
archive/              ~50 files (deprecated versions)
```

## Appendix B: Theory Files Summary

| File | Theorist | Key Concepts |
|------|----------|--------------|
| marx_theory.txt | Karl Marx | alienation, exploitation, class conflict, commodification |
| wollstonecraft_theory.txt | Mary Wollstonecraft | patriarchy, sexual alienation, domination, virtue |
| tocqueville_theory.txt | Alexis de Tocqueville | equality, tyranny of majority, conformity, associations |
| smith_theory.txt | Adam Smith | commerce, self-interest, division of labor, sympathy |

---

*This document should be updated as development progresses. Add session logs, track issues, and document solutions.*
