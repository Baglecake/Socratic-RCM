# Socratic-RCM Local Orchestrator

A local implementation of the Socratic Research Co-pilot Machine (RCM) workflow for designing agent-based simulations grounded in theoretical frameworks.

## Overview

This orchestrator guides users through a 3-phase workflow to design agent-based simulations:

- **Phase 1: Conceptualization** - Define theoretical framework, concepts, variables, setting, and agents
- **Phase 2: Drafting** - Configure round instructions, agent prompts, and platform settings
- **Phase 3: Review** - Validate and export the complete simulation design

## Directory Structure

```
local_rcm/
├── orchestrator.py       # Core workflow engine
├── canvas_state.py       # Canvas data model and compilation
├── llm_client.py         # LLM abstraction (mock, vLLM, etc.)
├── runtime_parser.py     # Runtime file parser
├── example_usage.py      # Main entry point
├── bios_reduced_prompt.txt
├── requirements.txt
├── runtime-files/        # Workflow definition files
│   ├── B42_Runtime_Logic_v2.0-COMPLETE.txt   # Full 112-step workflow
│   ├── B42_Runtime_Phase1_Conceptualization.txt
│   ├── B42_Runtime_Phase2_Drafting.txt
│   └── B42_Runtime_Phase3_Review.txt
├── tests/                # Test suite
│   ├── test_auto.py
│   ├── test_realistic.py
│   └── test_full_workflow.py
├── notebooks/            # Jupyter notebooks
│   ├── colab_vllm_server.ipynb
│   └── run_on_colab.ipynb
└── output/               # Generated outputs (gitignored)
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Mock LLM)

```bash
python example_usage.py --mode mock
```

### With vLLM Server

Start a vLLM server (locally or via Colab with ngrok):

```bash
python example_usage.py --mode vllm --base-url https://YOUR_NGROK_URL/v1
```

### Running Tests

```bash
# Full workflow test (112 steps)
python tests/test_full_workflow.py

# Phase 1 only test
python tests/test_realistic.py
```

## Workflow Output

The orchestrator produces:

1. **State JSON** - Complete student responses and canvas data
2. **Document TXT** - Human-readable simulation design document

### Helper Functions

The workflow supports these helper functions:

| Function | Type | Description |
|----------|------|-------------|
| Analyst | Required | Summarizes behavioral patterns |
| Moderator | Advanced | Controls conversation flow |
| Self-Reflections | Advanced | Agent introspection prompts |
| Non-Anthropomorphic | Advanced | Environmental cues instead of facial expressions |

Users select **2 of 3** advanced functions during the workflow.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Runtime Files  │────▶│   Orchestrator  │────▶│   Canvas State  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   LLM Client    │
                        │ (Mock/vLLM/API) │
                        └─────────────────┘
```

## License

Part of the Socratic-RCM research project.
