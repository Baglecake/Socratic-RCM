# Experiment: Baseline Full - Alienation vs Non-Domination

## Date: 2025-11-23

## Purpose
Full 3-phase workflow with real LLM to generate complete simulation configuration.

## Model Configuration
- Model: Qwen/Qwen2.5-7B-Instruct
- Backend: vLLM
- Temperature: Default

## Results
- Total steps executed: 112
- Phase 1 steps: 38
- Phase 2 steps: 66
- Phase 3 steps: 4
- Success: True

## What Was Generated
- Project goal and theoretical framework
- 4 agents (Worker+Alice, Worker+Ben, Owner+Marta, Analyst+Reporter)
- 3 rounds with specific instructions:
  - Round 1: Baseline Alienation
  - Round 2: Reduced Domination
  - Round 3: Comparative Analysis
- Helper functions configured
- Platform configuration for each round

## Files
- state.json: Complete workflow state with canvas
- document.txt: Compiled human-readable document
- config.json: Experiment metadata
- notes.md: This file
