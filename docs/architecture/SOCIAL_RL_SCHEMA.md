# Social RL Schema Specification

This document defines the data schemas for Social RL outputs, establishing a stable contract for serialization and analysis.

## Overview

Social RL produces structured JSON outputs that capture:
- Agent messages with context and PRAR cues
- Social feedback metrics per agent
- Policy adaptations triggered by feedback
- Round-level synthesis and duration

These schemas are implemented in:
- `social_rl/schema.py` - TypedDicts and dataclasses
- `prar/schema.py` - PRAR-specific schemas including policy state

## Schema Version

Current version: **0.2.0**

## Round Result Schema

Each round produces a JSON file (`roundN_social_rl.json`) with the following structure:

```json
{
  "meta": {
    "experiment_id": "social_rl_2025-11-23_175825",
    "prar_run_id": "2025-11-23_baseline_full_qwen",
    "framework": "Alienation vs Non-Domination",
    "framework_option": "A",
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "performer_temperature": 0.7,
    "coach_temperature": 0.1,
    "social_rl_version": "0.2.0",
    "timestamp": "2025-11-23T17:58:25.123456"
  },
  "round_number": 1,
  "round_config": {
    "scenario": "...",
    "rules": "...",
    "tasks": "..."
  },
  "messages": [...],
  "feedback": {...},
  "policy_adaptations": [...],
  "synthesis": "...",
  "duration_seconds": 45.2
}
```

### Meta Block

| Field | Type | Description |
|-------|------|-------------|
| `experiment_id` | string | Unique experiment identifier (directory name) |
| `prar_run_id` | string | Source PRAR output directory |
| `framework` | string | Human-readable framework name |
| `framework_option` | string | Framework option code (A-E) |
| `model` | string | LLM model identifier |
| `performer_temperature` | float | Temperature for agent generation |
| `coach_temperature` | float | Temperature for validation |
| `social_rl_version` | string | Schema/code version |
| `timestamp` | string | ISO format timestamp |

### Message Schema

```json
{
  "agent_id": "Worker+Alice",
  "content": "...",
  "round_number": 1,
  "turn_number": 1,
  "timestamp": 1700000000.0,
  "prar_cue_used": "[REFLECT] ... [CONNECT] ... [OBSERVE] ...",
  "feedback_snapshot": null,
  "validation_metadata": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | Yes | Agent identifier (Role+Name format) |
| `content` | string | Yes | Message content |
| `round_number` | int | Yes | Current round |
| `turn_number` | int | Yes | Turn within round |
| `timestamp` | float | Yes | Unix timestamp |
| `prar_cue_used` | string | No | PRAR reasoning cue injected |
| `feedback_snapshot` | object | No | Feedback at time of message |
| `validation_metadata` | object | No | Coach validation details |

#### Extended Message Fields (Optional)

| Field | Type | Description |
|-------|------|-------------|
| `context_frame` | object | Dynamic context injection details |
| `role` | string | Message role: "assistant", "system", "user" |
| `internal` | boolean | True for coach-only messages (not shown to agents) |

### Context Frame Schema

```json
{
  "base_scenario": "...",
  "concept_a_manifestation": "...",
  "concept_b_manifestation": "...",
  "experiential_cue": "...",
  "social_feedback_summary": "...",
  "prar_cue": "..."
}
```

### Feedback Vector Schema

```json
{
  "Worker+Alice": {
    "agent_id": "Worker+Alice",
    "round_number": 1,
    "engagement": 0.8,
    "theoretical_alignment": 0.72,
    "contribution_value": 0.65,
    "direct_references": 3,
    "response_received": 2,
    "concepts_embodied": ["alienation", "labor"],
    "analyst_mentions": 1,
    "synthesis_inclusion": 0.5
  }
}
```

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `agent_id` | string | - | Agent identifier |
| `round_number` | int | - | Round number |
| `engagement` | float | 0.0-1.0 | Participation level |
| `theoretical_alignment` | float | 0.0-1.0 | Framework adherence |
| `contribution_value` | float | 0.0-1.0 | Substantive contribution |
| `direct_references` | int | >= 0 | Times referenced by others |
| `response_received` | int | >= 0 | Responses to this agent |
| `concepts_embodied` | list | - | Detected concept expressions |
| `analyst_mentions` | int | >= 0 | Analyst function mentions |
| `synthesis_inclusion` | float | 0.0-1.0 | Inclusion in synthesis |

### Policy Adaptation Schema

```json
{
  "agent_id": "Worker+Alice",
  "adaptation_type": "activate_cue",
  "cue": "emphasize_non_domination",
  "reason": "engagement low, alignment below threshold",
  "round_number": 2,
  "feedback_trigger": {
    "engagement": 0.3,
    "alignment": 0.4
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string | Affected agent |
| `adaptation_type` | string | Type: "activate_cue", "deactivate_cue", "adjust_intensity" |
| `cue` | string | The specific cue affected |
| `reason` | string | Human-readable explanation |
| `round_number` | int | When adaptation occurred |
| `feedback_trigger` | object | Feedback values that triggered this |

## PRAR Policy State Schema

The policy state links PRAR outputs to Social RL execution:

```json
{
  "framework_option": "A",
  "framework_name": "Class Conflict / Alienation",
  "policies": [
    {
      "role": "Worker",
      "cues_active": ["reflect_on_alienation", "connect_to_labor"],
      "cue_states": {
        "reflect_on_alienation": {
          "cue_id": "reflect_on_alienation",
          "active": true,
          "intensity": 0.8,
          "last_triggered": "2025-11-23T17:58:25"
        }
      },
      "feedback_snapshot": {
        "engagement": 0.7,
        "alignment": 0.8
      }
    }
  ],
  "timestamp": "2025-11-23T17:58:25",
  "source_run_id": "2025-11-23_baseline_full_qwen",
  "social_rl_version": "0.2.0"
}
```

## Validation

Use the validation functions in `social_rl/schema.py`:

```python
from social_rl.schema import validate_round_result, load_round_result

# Validate a dict
validate_round_result(data)  # Raises ValueError if invalid

# Load and validate from file
result = load_round_result("outputs/social_rl_.../round1_social_rl.json")
```

## Usage Example

```python
from social_rl.schema import (
    RoundResult,
    SocialRLMessage,
    AgentFeedback,
    create_experiment_meta,
    save_round_result
)

# Create messages
msg = SocialRLMessage(
    agent_id="Worker+Alice",
    content="I understand the task...",
    round_number=1,
    turn_number=1,
    timestamp=time.time(),
    prar_cue_used="[REFLECT] ..."
)

# Create feedback
feedback = AgentFeedback(
    agent_id="Worker+Alice",
    round_number=1,
    engagement=0.8,
    theoretical_alignment=0.7,
    contribution_value=0.6
)

# Create round result with metadata
result = RoundResult(
    round_number=1,
    messages=[msg],
    feedback={"Worker+Alice": feedback},
    meta=create_experiment_meta(
        experiment_id="social_rl_2025-11-23_175825",
        prar_run_id="2025-11-23_baseline_full_qwen",
        framework="Alienation vs Non-Domination",
        framework_option="A",
        model="Qwen/Qwen2.5-7B-Instruct"
    )
)

# Save to file
save_round_result(result, "round1_social_rl.json")
```

## Schema Evolution

When updating schemas:
1. Increment `SCHEMA_VERSION` in both schema.py files
2. Update this document
3. Ensure backward compatibility where possible
4. Document breaking changes in CHANGELOG

## See Also

- [social_rl/README.md](../../social_rl/README.md) - Social RL framework
- [prar/README.md](../../prar/README.md) - PRAR methodology
- [ROADMAP.md](../../ROADMAP.md) - Development roadmap
