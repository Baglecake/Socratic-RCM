# Canvas Data Schema v1.0

**Purpose**: Define the complete data structure for progressive canvas compilation in BIOS v2.3+

**Date**: 2025-01-19

---

## Canvas Structure

```json
{
  "project": {
    "title": "<derived from 1.2.2 project goal, first sentence>",
    "goal": "<full text from 1.2.2>",
    "theoretical_option": "<A/B/C/D/E from 1.2.1>",
    "theoretical_option_label": "<resolved from KB[2]>",
    "concept_a": {
      "name": "<derived from KB[2] based on option>",
      "definition": "<full text from 1.2.3>"
    },
    "concept_b": {
      "name": "<derived from KB[2] based on option>",
      "definition": "<full text from 1.2.4>"
    },
    "structure": "<Single multi-round | Two separate designs from 1.2.5>",
    "experiment_type": "<A: Modify variable | B: New design from 1.2.6>"
  },
  "baseline_experiment": {
    "baseline_description": "<full text from 1.3.1>",
    "experimental_design": {
      "type_a_variable": {
        "variable_name": "<from 1.3.2A Q1>",
        "baseline_value": "<from 1.3.2A Q2>",
        "experimental_value": "<from 1.3.2A Q3>"
      },
      "type_b_description": "<from 1.3.2B if applicable>",
      "rationale": "<from 1.3.3>"
    }
  },
  "setting": {
    "description": "<full text from 1.4.1>",
    "num_rounds": "<number from 1.4.2>",
    "round_plan": [
      {
        "round_num": 1,
        "name": "<from 1.4.3>",
        "purpose": "<from 1.4.3>"
      }
    ]
  },
  "agents": [
    {
      "index": 1,
      "identifier": "<[purpose]+[name] from 1.5.2>",
      "type": "<Human | Non-human from 1.5.3>",
      "goal": "<full text from 1.6.1>",
      "persona": "<full text from 1.6.2>",
      "behaviors": "<optional text from 1.6.3 or null>",
      "prompt": {
        "role": "<identifier from 1.5.2>",
        "primary_goal": "<goal from 1.6.1>",
        "persona": "<persona from 1.6.2>",
        "compiled_in_step": "2.1.1"
      }
    }
  ],
  "rounds": [
    {
      "index": 1,
      "scenario": "<full text from 2.2.1>",
      "concept_a_in_round": "<full text from 2.2.2>",
      "concept_b_in_round": "<full text from 2.2.3>",
      "rules": "<full text from 2.2.4>",
      "tasks": "<full text from 2.2.5>",
      "sequence": "<full text from 2.2.6>",
      "agent_behaviors": "<from 2.2.7 if applicable>",
      "compiled_s3_template": "<from 2.2.8>",
      "platform_config": {
        "participants": "<from 2.2.9>",
        "who_sends": "<All | Moderator from 2.2.10>",
        "order": "<Default | Random | Active | Moderator from 2.2.11>",
        "end_condition": {
          "method": "<Total msgs | Per participant | Moderator from 2.2.12>",
          "details": "<number or moderator config from 2.2.12>"
        },
        "transition": "<Pause | Auto | Moderator from 2.2.13>",
        "detail_level": "<Min | Brief | Med | Thor | Exh | Dyn from 2.2.14>",
        "creativity": "<Defaults | Custom config from 2.2.15>",
        "options": {
          "ask_questions": "<true | false from 2.2.16>",
          "self_reflection": "<true | false from 2.2.16>",
          "isolated": "<true | false from 2.2.16>"
        },
        "model": "<Defaults | DeepSeek42 from 2.2.17>",
        "compiled_checklist": "<from 2.2.18>"
      }
    }
  ],
  "helpers": {
    "moderator": {
      "used": "<true | false from 1.7 or 2.2>",
      "end_round_instructions": "<from 2.3.1 if used>"
    },
    "analyst": {
      "required": true,
      "note": "Required per v8.4, uses S4-ANALYST from KB[1]"
    },
    "non_anthropomorphic": {
      "used": "<true | false from 1.7>",
      "template": "<from 2.3.3 if used>"
    },
    "self_reflections": {
      "used": "<true | false from 1.7>",
      "note": "Checkbox only, configured in platform options per round"
    }
  },
  "status": {
    "phase1_complete": "<true after 1.8>",
    "phase2_complete": "<true after 2.3.5>",
    "phase3_checklist": {
      "all_fields_filled": "<from 3.1>",
      "no_paraphrasing": "<from 3.1>",
      "templates_match_kb1": "<from 3.1>",
      "advanced_functions_2plus": "<from 3.1>",
      "concepts_defined": "<from 3.1>",
      "persona_in_s2": "<from 3.1>",
      "behaviors_in_s3": "<from 3.1>",
      "config_per_round": "<from 3.1>"
    },
    "final_review_confirmed": "<true after 3.2>",
    "workflow_complete": "<true after 3.3>"
  }
}
```

---

## Data Collection Mapping

### Phase 1: Conceptualization

| Canvas Field | Runtime Step | Data Type | Required |
|--------------|--------------|-----------|----------|
| `project.title` | 1.2.2 | Derived (first sentence) | Yes |
| `project.goal` | 1.2.2 | Full text (2-3 sent) | Yes |
| `project.theoretical_option` | 1.2.1 | Single letter (A/B/C/D/E) | Yes |
| `project.theoretical_option_label` | 1.2.1 + KB[2] | Resolved string | Yes |
| `project.concept_a.name` | KB[2] + 1.2.1 | Derived from option | Yes |
| `project.concept_a.definition` | 1.2.3 | Full text (2-3 sent) | Yes |
| `project.concept_b.name` | KB[2] + 1.2.1 | Derived from option | Yes |
| `project.concept_b.definition` | 1.2.4 | Full text (2-3 sent) | Yes |
| `project.structure` | 1.2.5 | Single or Two designs | Yes |
| `project.experiment_type` | 1.2.6 | A or B | Yes |
| `baseline_experiment.baseline_description` | 1.3.1 | Full text (2-3 sent) | Yes |
| `baseline_experiment.experimental_design.type_a_variable.*` | 1.3.2A | Three answers | If Type A |
| `baseline_experiment.experimental_design.type_b_description` | 1.3.2B | Full text (2-3 sent) | If Type B |
| `baseline_experiment.experimental_design.rationale` | 1.3.3 | Full text (3 sent) | Yes |
| `setting.description` | 1.4.1 | Full text (4-5 sent) | Yes |
| `setting.num_rounds` | 1.4.2 | Number | Yes |
| `setting.round_plan[].round_num` | 1.4.3 loop | Integer 1-N | Yes |
| `setting.round_plan[].name` | 1.4.3 | String | Yes |
| `setting.round_plan[].purpose` | 1.4.3 | Text (2-3 sent) | Yes |
| `agents[].index` | 1.5.1 loop | Integer 1-N | Yes |
| `agents[].identifier` | 1.5.2 | [purpose]+[name] format | Yes |
| `agents[].type` | 1.5.3 | Human or Non-human | Yes |
| `agents[].goal` | 1.6.1 | Full text (2-3 sent) | Yes |
| `agents[].persona` | 1.6.2 | Full text (2-3 sent) | Yes |
| `agents[].behaviors` | 1.6.3 | Full text or null | Optional |

### Phase 2: Drafting

| Canvas Field | Runtime Step | Data Type | Required |
|--------------|--------------|-----------|----------|
| `agents[].prompt.role` | 2.1.1 | From 1.5.2 identifier | Yes |
| `agents[].prompt.primary_goal` | 2.1.1 | From 1.6.1 goal | Yes |
| `agents[].prompt.persona` | 2.1.1 | From 1.6.2 persona | Yes |
| `agents[].prompt.compiled_in_step` | 2.1.1 | "2.1.1" marker | Yes |
| `rounds[].index` | 2.2.1 loop | Integer 1-N | Yes |
| `rounds[].scenario` | 2.2.1 | Full text (4-5 sent) | Yes |
| `rounds[].concept_a_in_round` | 2.2.2 | Full text (2-3 sent) | Yes |
| `rounds[].concept_b_in_round` | 2.2.3 | Full text (2-3 sent) | Yes |
| `rounds[].rules` | 2.2.4 | Full text | Yes |
| `rounds[].tasks` | 2.2.5 | Full text | Yes |
| `rounds[].sequence` | 2.2.6 | Full text (2-3 sent) | Yes |
| `rounds[].agent_behaviors` | 2.2.7 | From 1.6.3 if defined | Optional |
| `rounds[].compiled_s3_template` | 2.2.8 | Full compiled template | Yes |
| `rounds[].platform_config.participants` | 2.2.9 | List of agent identifiers | Yes |
| `rounds[].platform_config.who_sends` | 2.2.10 | All or Moderator | Yes |
| `rounds[].platform_config.order` | 2.2.11 | Default/Random/Active/Moderator | Yes |
| `rounds[].platform_config.end_condition.*` | 2.2.12 | Method + details | Yes |
| `rounds[].platform_config.transition` | 2.2.13 | Pause/Auto/Moderator | Yes |
| `rounds[].platform_config.detail_level` | 2.2.14 | Min/Brief/Med/Thor/Exh/Dyn | Yes |
| `rounds[].platform_config.creativity` | 2.2.15 | Defaults or Custom | Yes |
| `rounds[].platform_config.options.*` | 2.2.16 | Three booleans | Yes |
| `rounds[].platform_config.model` | 2.2.17 | Defaults or DeepSeek42 | Yes |
| `rounds[].platform_config.compiled_checklist` | 2.2.18 | Full checklist display | Yes |
| `helpers.moderator.used` | 1.7 or 2.2 | Boolean | Yes |
| `helpers.moderator.end_round_instructions` | 2.3.1 | Text (2-3 sent) | If used |
| `helpers.analyst.required` | Always | true | Yes |
| `helpers.non_anthropomorphic.used` | 1.7 | Boolean | Yes |
| `helpers.non_anthropomorphic.template` | 2.3.3 | Template ref | If used |
| `helpers.self_reflections.used` | 1.7 | Boolean | Yes |

### Phase 3: Review & Export

| Canvas Field | Runtime Step | Data Type | Required |
|--------------|--------------|-----------|----------|
| `status.phase1_complete` | 1.8 | Boolean | Yes |
| `status.phase2_complete` | 2.3.5 | Boolean | Yes |
| `status.phase3_checklist.*` | 3.1 | Eight booleans | Yes |
| `status.final_review_confirmed` | 3.2 | Boolean | Yes |
| `status.workflow_complete` | 3.3 | Boolean | Yes |

---

## Canvas Update Points

Progressive compilation occurs at these specific steps:

### Phase 1 Updates

| After Step | Canvas Section Updated | Fields Added |
|------------|------------------------|--------------|
| 1.2.2 | `project.title`, `project.goal` | Create canvas with title |
| 1.2.3 | `project.concept_a.definition` | Add Concept A |
| 1.2.4 | `project.concept_b.definition` | Add Concept B |
| CHECKPOINT 1.2 | `project.*` | Complete framework section |
| 1.3.3 | `baseline_experiment.*` | Complete baseline/experiment |
| CHECKPOINT 1.3 | Verify baseline section | Display to student |
| 1.4.3 | `setting.round_plan[]` | Add all rounds |
| CHECKPOINT 1.4 | `setting.*` | Complete setting section |
| 1.5.3 | `agents[].index`, `.identifier`, `.type` | After all roster collected |
| CHECKPOINT 1.5 | Agent roster | Display roster table |
| 1.6.3 | `agents[i].*` | After EACH agent's details |
| 1.8 | `status.phase1_complete` | Mark Phase 1 done |

### Phase 2 Updates

| After Step | Canvas Section Updated | Fields Added |
|------------|------------------------|--------------|
| 2.1.1 | `agents[i].prompt.*` | After EACH agent prompt |
| 2.2.8 | `rounds[i].compiled_s3_template` | After EACH round instructions |
| 2.2.18 | `rounds[i].platform_config.*` | After EACH round config |
| 2.3.5 | `helpers.*`, `status.phase2_complete` | Mark Phase 2 done |

### Phase 3 Updates

| After Step | Canvas Section Updated | Fields Added |
|------------|------------------------|--------------|
| 3.1 | `status.phase3_checklist.*` | Checklist verification |
| 3.2 | `status.final_review_confirmed` | Review confirmed |
| 3.3 | `status.workflow_complete` | Workflow complete |

---

## CANVAS_UPDATE Block Format

Each runtime step that triggers a canvas update will include:

```
CANVAS_UPDATE:
||CANVAS_UPDATE||
{
  "section": "<project | agents | rounds | helpers | status>",
  "action": "<create | update | append>",
  "index": <optional: for arrays>,
  "data": {
    <field>: "<value>"
  }
}
||END_CANVAS_UPDATE||
```

### Example: Step 1.2.2 (Create Canvas)

```
CANVAS_UPDATE:
||CANVAS_UPDATE||
{
  "section": "project",
  "action": "create",
  "data": {
    "title": "<student's project goal, first sentence>",
    "goal": "<student's full response to 1.2.2>"
  }
}
||END_CANVAS_UPDATE||
```

### Example: Step 1.6.3 (Add Agent Details)

```
CANVAS_UPDATE:
||CANVAS_UPDATE||
{
  "section": "agents",
  "action": "update",
  "index": <current agent index>,
  "data": {
    "goal": "<student's response to 1.6.1>",
    "persona": "<student's response to 1.6.2>",
    "behaviors": "<student's response to 1.6.3 or null>"
  }
}
||END_CANVAS_UPDATE||
```

### Example: Step 2.2.18 (Platform Config)

```
CANVAS_UPDATE:
||CANVAS_UPDATE||
{
  "section": "rounds",
  "action": "update",
  "index": <current round number>,
  "data": {
    "platform_config": {
      "participants": "<from 2.2.9>",
      "who_sends": "<from 2.2.10>",
      "order": "<from 2.2.11>",
      "end_condition": "<from 2.2.12>",
      "transition": "<from 2.2.13>",
      "detail_level": "<from 2.2.14>",
      "creativity": "<from 2.2.15>",
      "options": {
        "ask_questions": <from 2.2.16>,
        "self_reflection": <from 2.2.16>,
        "isolated": <from 2.2.16>
      },
      "model": "<from 2.2.17>",
      "compiled_checklist": "<from 2.2.18>"
    }
  }
}
||END_CANVAS_UPDATE||
```

---

## Validation Rules

Before implementing canvas updates, verify:

1. **Data Availability**: Every field referenced in CANVAS_UPDATE must have been collected in a prior step
2. **Index Tracking**: Array indices (agents, rounds) must be tracked correctly through loops
3. **Optional Fields**: Null handling for optional fields (behaviors, type B design, etc.)
4. **Timing**: Canvas update happens AFTER student response accepted, not during question
5. **Student Visibility**: Canvas updates are internal; student sees compiled sections at checkpoints

---

**Status**: Schema v1.0 - Ready for implementation
**Next**: Implement BIOS v2.3 canvas protocol + runtime CANVAS_UPDATE blocks
