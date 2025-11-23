# Experiment: Baseline Phase 1 - Alienation vs Non-Domination

## Date: 2025-11-23

## Purpose
First successful run of Phase 1 with real LLM (Qwen 7B via vLLM on Google Colab).

## What Was Tested
- Full Phase 1 workflow (42 steps)
- Runtime file parsing and step execution
- Loop handling (rounds, agents, agent details)
- Conditional routing (Type A experiment path)
- Canvas compilation from student state
- JSON export

## Model Configuration
- Model: Qwen/Qwen2.5-7B-Instruct
- Backend: vLLM on Colab A100
- Temperature: Default

## Results
- All 42 Phase 1 steps executed successfully
- Canvas correctly populated with:
  - Project goal and theoretical framework
  - 4 agents (Worker+Alice, Worker+Ben, Owner+Marta, Analyst+Reporter)
  - 3 rounds defined
  - Baseline vs experimental variable specified
- Phase 2/3 fields empty (as expected - not yet executed)

## Key Observations
1. JSON validation fix (send_json without response_format) worked correctly
2. Framework coherence maintained throughout
3. Agent prompts generated correctly from student answers

## Next Steps
- Run full baseline (all 3 phases) to complete Section 2 and Section 3
- Save as separate experiment folder
