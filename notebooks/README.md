# Notebooks

This directory contains the canonical baseline notebook for reproducibility purposes. Active development notebooks are maintained externally on Google Colab.

## Canonical Snapshot

**[baseline_snapshot.ipynb](baseline_snapshot.ipynb)**

A stripped (outputs removed) snapshot of the full 3-phase PRAR workflow execution. This notebook documents the foundational methodology and serves as a reproducibility anchor for the project.

Contents:
- vLLM server setup on Colab A100
- Repository cloning and dependency installation
- Phase 1 test execution (test_realistic.py)
- Full baseline experiment (run_baseline_experiment.py)
- Output archival

## External Development Notebooks (Colab)

Active notebooks are hosted on Google Colab to leverage GPU resources and avoid repository bloat. These represent iterative development and experimentation.

| Notebook | Purpose | Link |
|----------|---------|------|
| PRAR Phase 1 | Phase 1 validation with Qwen 7B via vLLM | [Open in Colab](https://colab.research.google.com/drive/13aaQFlCmEREAaliogKGwPA9xOfQ0mddo?usp=sharing) |
| PRAR Full Baseline | Complete 3-phase workflow (112 steps) | [Open in Colab](https://colab.research.google.com/drive/1MsDxrTfQArZHEiWfbruZdqR2o0aq0RCS?usp=sharing) |
| Dual-Instance Pipeline | Coach/Performer architecture validation | [Open in Colab](https://colab.research.google.com/drive/1AgA37uoZje-KQ6Pl3uCwaBQzfgfXd33B?usp=sharing) |

## Running the Baseline Notebook

### Prerequisites

- Google Colab account with GPU access (A100 recommended)
- Sufficient Colab compute units for vLLM inference

### Steps

1. Open [baseline_snapshot.ipynb](baseline_snapshot.ipynb) in Colab
2. Select Runtime > Change runtime type > A100 GPU
3. Execute cells sequentially:
   - Cells 1-5: vLLM server setup
   - Cells 6-8: Model verification
   - Cells 9-12: Repository setup
   - Cells 13+: Experiment execution

### Expected Output

The notebook produces:
- `prar/outputs/YYYY-MM-DD_baseline_full_qwen/state.json`
- `prar/outputs/YYYY-MM-DD_baseline_full_qwen/document.txt`
- `prar/outputs/YYYY-MM-DD_baseline_full_qwen/config.json`
- `prar/outputs/YYYY-MM-DD_baseline_full_qwen/notes.md`

## Notebook Management Policy

To maintain repository hygiene:

1. **Canonical snapshots** (outputs stripped) are committed to `notebooks/`
2. **Iterative notebooks** remain on Colab and are linked in this README
3. **Experiment outputs** are committed to `experiments/` with metadata

This approach balances reproducibility with repository size constraints.
