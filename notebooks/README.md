# Notebooks

This directory contains canonical notebook snapshots for reproducibility. Active development notebooks are maintained externally on Google Colab to leverage GPU resources.

## Repository Notebooks

### Canonical Snapshots (Outputs Stripped)

| Notebook | Purpose | Description |
|----------|---------|-------------|
| [baseline_snapshot.ipynb](baseline_snapshot.ipynb) | PRAR Workflow | Full 3-phase PRAR workflow execution with vLLM/Qwen |
| [social_rl_demo.ipynb](social_rl_demo.ipynb) | Social RL | Social RL framework demonstration and experimentation |

**baseline_snapshot.ipynb** documents:
- vLLM server setup on Colab A100
- Repository cloning and dependency installation
- Phase 1 test execution (test_realistic.py)
- Full baseline experiment (run_baseline_experiment.py)
- Output archival to `prar/outputs/`

**social_rl_demo.ipynb** documents:
- Social RL runner configuration
- Context injection and feedback extraction
- Multi-round simulation execution
- Output analysis

## External Development Notebooks (Google Colab)

Active notebooks are hosted on Google Colab to leverage GPU resources and avoid repository bloat. These represent iterative development and experimentation.

| Notebook | Purpose | Link |
|----------|---------|------|
| PRAR Phase 1 | Phase 1 validation (38 steps) with Qwen 7B via vLLM | [Open in Colab](https://colab.research.google.com/drive/13aaQFlCmEREAaliogKGwPA9xOfQ0mddo?usp=sharing) |
| PRAR Full Baseline | Complete 3-phase workflow (112 steps) | [Open in Colab](https://colab.research.google.com/drive/1MsDxrTfQArZHEiWfbruZdqR2o0aq0RCS?usp=sharing) |
| Dual-Instance Pipeline | Coach/Performer architecture validation | [Open in Colab](https://colab.research.google.com/drive/1AgA37uoZje-KQ6Pl3uCwaBQzfgfXd33B?usp=sharing) |

## Related Notebooks (Other Locations)

| Notebook | Location | Purpose |
|----------|----------|---------|
| dual-instance-v1.ipynb | [dual-instance/](../dual-instance/) | Dual-LLM architecture validation |

## Running Notebooks

### Prerequisites

- Google Colab account with GPU access (A100 recommended for vLLM)
- Sufficient Colab compute units for inference
- For local execution: Python 3.9+, dependencies from `local_rcm/requirements.txt`

### Colab Execution

1. Open the desired Colab link above
2. Select Runtime > Change runtime type > A100 GPU
3. Execute cells sequentially
4. Outputs are saved to the appropriate `outputs/` directory

### Local Execution

```bash
# Install dependencies
pip install -r local_rcm/requirements.txt

# For Social RL (auto-detects Ollama/OpenAI)
python run_social_rl_local.py

# For PRAR workflow
cd local_rcm
python scripts/run_baseline_experiment.py --mock  # or with vLLM
```

## Expected Outputs

### PRAR Workflow

```
prar/outputs/YYYY-MM-DD_baseline_*/
├── state.json      # Complete workflow state
├── document.txt    # Human-readable design document
├── config.json     # Experiment metadata
└── notes.md        # Execution summary
```

### Social RL

```
outputs/social_rl_YYYY-MM-DD_HHMMSS/
├── round1_social_rl.json
├── round2_social_rl.json
├── round3_social_rl.json
└── policy_state.json
```

## Notebook Management Policy

To maintain repository hygiene and reproducibility:

1. **Canonical snapshots** (outputs stripped) are committed to `notebooks/`
2. **Iterative development notebooks** remain on Colab and are linked in this README
3. **Experiment outputs** are committed to `prar/outputs/` or `outputs/` with metadata
4. **Validation notebooks** (e.g., dual-instance) live in dedicated directories

This approach balances reproducibility with repository size constraints while maintaining clear provenance for all experimental work.

## See Also

- [ROADMAP.md](../ROADMAP.md) - Development phases
- [social_rl/README.md](../social_rl/README.md) - Social RL framework
- [prar/README.md](../prar/README.md) - PRAR methodology
- [local_rcm/README.md](../local_rcm/README.md) - Orchestrator documentation
