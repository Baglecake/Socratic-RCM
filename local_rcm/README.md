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
├── app.py                # Streamlit web interface
├── orchestrator.py       # Core workflow engine
├── canvas_state.py       # Canvas data model and compilation
├── llm_client.py         # LLM abstraction + StudentSimulator
├── runtime_parser.py     # Runtime file parser
├── runpod_setup.py       # RunPod connectivity test
├── example_usage.py      # CLI entry point
├── bios_reduced_prompt.txt
├── requirements.txt
├── runtime-files/        # Workflow definition files
│   ├── B42_Runtime_Logic_v2.0-COMPLETE.txt
│   ├── B42_Runtime_Phase1_Conceptualization.txt
│   ├── B42_Runtime_Phase2_Drafting.txt
│   └── B42_Runtime_Phase3_Review.txt
├── tests/                # Test suite
│   ├── test_auto.py
│   ├── test_realistic.py
│   ├── test_full_workflow.py
│   └── test_simulator.py
└── output/               # Generated outputs (gitignored)
```

## Installation

```bash
pip install -r requirements.txt
```

## RunPod Setup (Recommended for GPU)

RunPod provides reliable GPU access via serverless endpoints.

### 1. Create RunPod Account
- Sign up at https://runpod.io

### 2. Deploy vLLM Endpoint
- Go to **Serverless** > **+ New Endpoint**
- Select the **vLLM** template
- Choose model: `Qwen/Qwen2.5-7B-Instruct`
- Configure resources (24GB+ VRAM recommended)
- Deploy and wait for status: **Ready**

### 3. Get Credentials
- **Endpoint ID**: From the endpoint dashboard URL
- **API Key**: Settings > API Keys > Create new key

### 4. Test Connection
```bash
python runpod_setup.py --endpoint-id YOUR_ENDPOINT_ID --api-key YOUR_API_KEY
```

## Usage

### Streamlit Web Interface (Recommended)

```bash
streamlit run app.py
```

1. Select **RunPod** mode in the sidebar
2. Enter your endpoint URL: `https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1`
3. Enter your RunPod API key
4. Enable **Auto-Mode** for LLM-simulated student responses
5. Click **Start/Reset Workflow**

### Mock Mode (Testing)

```bash
python example_usage.py --mode mock
```

### OpenAI Mode

```bash
python example_usage.py --mode openai --api-key YOUR_KEY
```

## Auto-Mode (Student Simulator)

The simulator uses a sociology student persona that:
- References Marx, Wollstonecraft, Tocqueville, Adam Smith
- Gives substantive 2-4 sentence responses
- Switches persona based on chosen theoretical framework (Options A-E)
- Maintains conversation consistency

## Running Tests

```bash
# Full workflow test (mock)
python tests/test_full_workflow.py

# Phase 1 only
python tests/test_realistic.py
```

## Workflow Output

The orchestrator produces:

1. **State JSON** - Complete student responses and canvas data
2. **Document TXT** - Human-readable simulation design document

### Helper Functions

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
                        │(Mock/RunPod/API)│
                        └─────────────────┘
```

## License

Part of the Socratic-RCM research project.
