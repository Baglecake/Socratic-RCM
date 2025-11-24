# Experiments

This directory contains experiment runners for the Social RL framework.

## Quick Start

```bash
# Test with mock client (no LLM required)
python experiments/run_social_rl_experiment.py --provider mock

# Run with local Ollama model
python experiments/run_social_rl_experiment.py --model qwen2.5:7b

# Run with RunPod vLLM endpoint
python experiments/run_social_rl_experiment.py \
  --provider vllm \
  --base-url https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1 \
  --model Qwen/Qwen2.5-7B-Instruct \
  --api-key YOUR_RUNPOD_KEY

# Run with pre-configured canvas
python experiments/run_social_rl_experiment.py \
  --state prar/outputs/2025-11-23_baseline_full_qwen/state.json
```

## RunPod / vLLM Setup

For long-running experiments with stable GPU inference:

1. Deploy a vLLM serverless endpoint on RunPod
2. Set environment variables:
   ```bash
   export OPENAI_BASE_URL=https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1
   export RUNPOD_API_KEY=your_api_key
   export OPENAI_MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
   ```
3. Run experiments:
   ```bash
   python experiments/run_social_rl_experiment.py \
     --provider vllm \
     --model $OPENAI_MODEL_NAME \
     --rounds 3
   ```

## Experiment Scripts

### run_social_rl_experiment.py

Main experiment runner demonstrating:

- **Dual-LLM Architecture**: Coach (validation) + Performer (generation) pattern
- **PRAR Integration**: Process-retrieval augmented reasoning cues
- **Social Feedback**: Engagement, alignment, and contribution metrics
- **Policy Adaptation**: Agents adapt based on social feedback across rounds

#### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--model` | LLM model name | qwen2.5:7b |
| `--provider` | LLM provider (ollama, openai, vllm, mock) | ollama |
| `--rounds` | Number of rounds to execute | 1 |
| `--max-turns` | Maximum turns per round | 9 |
| `--state` | Path to state.json with canvas | (demo canvas) |
| `--no-dual-llm` | Disable Coach/Performer architecture | false |
| `--quiet` | Reduce output verbosity | false |
| `--base-url` | vLLM/RunPod endpoint URL | (env var) |
| `--api-key` | API key for RunPod | (env var) |
| `--experiment-id` | Custom experiment ID | (auto-generated) |

## Understanding the Output

Each experiment produces:

```
outputs/social_rl_TIMESTAMP/
├── meta.json               # Experiment metadata (model, temps, git commit)
├── metrics.json            # Relational dynamics metrics (participation, domination, etc.)
├── round1_social_rl.json   # Round 1 messages and feedback
├── round2_social_rl.json   # Round 2 (if executed)
├── policy_state.json       # Policy adaptation history
└── social_rl_report.txt    # Human-readable summary
```

### meta.json Structure

```json
{
  "experiment_id": "social_rl_2025-11-23_162944",
  "framework": "Class Conflict / Alienation",
  "framework_option": "A",
  "model": "Qwen/Qwen2.5-7B-Instruct",
  "provider": "vllm",
  "backend": "vllm (https://api.runpod.ai/...)",
  "performer_temperature": 0.7,
  "coach_temperature": 0.1,
  "dual_llm_enabled": true,
  "git_commit": "abc1234",
  "social_rl_version": "0.2.0"
}
```

### metrics.json Structure

Relational dynamics metrics computed from message content:

```json
{
  "per_round": { "round_1": { ... } },
  "aggregate": {
    "participation": {
      "total_messages": 9,
      "by_role": { "Worker": 6, "Owner": 3 },
      "worker_ratio": 0.667,
      "owner_ratio": 0.333
    },
    "justification": {
      "total_count": 2,
      "owner_density": 0.667
    },
    "domination": {
      "total_count": 1,
      "examples": [{ "agent": "Owner+Marta", "match": "that's final" }]
    },
    "alienation": {
      "total_count": 2,
      "examples": [{ "agent": "Worker+Alice", "match": "just doing my job" }]
    }
  },
  "summary": {
    "participation_asymmetry": "worker_dominant",
    "domination_level": "moderate",
    "alienation_level": "moderate",
    "key_observations": ["Workers dominated conversation (67% of messages)"]
  }
}
```

### Relational Dynamics Metrics

- **Participation Asymmetry**: Worker vs owner message ratios
- **Justification Density**: Owner utterances with reasons ("because...", "due to...")
- **Domination Markers**: Power without justification ("that's final", "because I said so")
- **Alienation Markers**: Worker externality talk ("not my call", "just doing my job")

### Social Feedback Metrics

- **Engagement**: How actively the agent participates (0.0-1.0)
- **Theoretical Alignment**: How well responses embody framework concepts (0.0-1.0)
- **Contribution Value**: Impact on group discussion (0.0-1.0)
- **Direct References**: Count of times agent was addressed by name
- **Response Received**: Count of direct responses to agent's statements

## Research Questions

The experiment framework supports investigating:

1. How do agents adapt when structural constraints change?
2. Does the Coach/Performer pattern improve theoretical coherence?
3. How do PRAR cues influence agent reasoning style?
4. What patterns emerge in social feedback across rounds?

## Extending Experiments

To create custom experiments:

1. Design a canvas using the PRAR workflow (see notebooks/)
2. Export the state.json file
3. Run with `--state your_state.json`

See [social_rl/README.md](../social_rl/README.md) for component documentation.
