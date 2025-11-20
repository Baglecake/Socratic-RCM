# B42-BIOS v2.4 - Enhancements

**Date**: 2025-01-19
**Version**: BIOS v2.4 (Code Interpreter + Schema Validation + Canvas Visibility)

---

## What's New

### 1. Schema Validation (Data Structure Enforcement)

The validator now checks that canvas data matches the expected structure **before** displaying compiled sections to students.

**How It Works**:
- After Phase 1 (Step 1.8): Validates that project, baseline_experiment, setting, and agents data are complete
- After Phase 2.1: Validates that all agent prompts have been drafted
- After Phase 2.2: Validates that all round instructions and platform configs are complete

**What It Validates**:
- **Required fields are present**: e.g., `project.goal`, `agents[].persona`, `rounds[].sequence`
- **Data types are correct**: e.g., `setting.num_rounds` is a number
- **Arrays are populated**: e.g., `agents[]` array has at least one agent
- **Nested structures are complete**: e.g., `rounds[].platform_config` has all required fields

**Error Handling**:
If validation fails, GPT shows clear error messages:
```
⚠️ Your design is incomplete. Please provide the following:
- Missing project.goal: Please provide your 2-3 sentence project goal
- Missing agents[0].persona: Please provide a 2-3 sentence persona for [Agent Identifier]
```

GPT then uses RCM to help student provide missing information (without writing it for them).

---

### 2. Progressive Canvas Display (Section Compilation Visibility)

After each phase completes AND schema validation passes, GPT displays the compiled section to the student.

**Phase 1 Complete (Step 1.8)**:
- Displays: **Section 1 (Design Plan)** in template format
- Shows: Full design plan with all project details, agents roster, round plan
- Student sees their complete conceptual design before moving to drafting

**Phase 2.1 Complete (All agent prompts)**:
- Displays: **Section 2 (Agent Prompts)** in S2 template format
- Shows: All agent prompts formatted as `ROLE / PRIMARY GOAL / PERSONA`
- Students can copy-paste directly into Chatstorm agent system prompts

**Phase 2.2 Complete (All round instructions)**:
- Displays: **Section 3 (Round Instructions)** in S3 template format
- Shows: All round custom instructions with platform configs
- Students can copy-paste directly into Chatstorm round custom instructions

**Benefits**:
- Students don't need to hold everything in memory throughout the workflow
- Clear visibility into their progress
- Copy-paste ready outputs for Chatstorm deployment
- Reduces cognitive load

---

## Technical Implementation

### Enhanced `runtime_validator.py`

**New Classes**:
- `CanvasSchemaValidator`: Validates canvas data structure
  - `validate_phase1_complete()`: Checks Phase 1 data completeness
  - `validate_phase2_1_complete()`: Checks agent prompts
  - `validate_phase2_2_complete()`: Checks round instructions
  - `validate_data_types()`: Type checking (numbers, arrays, etc.)

**New Methods in `WorkflowValidator`**:
- `update_canvas_data(section, data)`: Updates canvas data during workflow
- `validate_canvas_schema(phase)`: Validates canvas against schema for specific phase
- `_get_canvas_summary()`: Returns summary of canvas data state

**New Helper Function**:
- `validate_phase_complete(validator, phase)`: GPT calls this to validate schema

**Schema Reference**:
The validator uses the schema structure defined in `documentation/CANVAS_DATA_SCHEMA.md` (not uploaded to GPT, but used as reference for validation logic).

---

### Enhanced `CUSTOM_GPT_INSTRUCTIONS.txt`

**New Section**: "CANVAS COMPILATION DISPLAY (Schema-Validated Output)"

**Instructions Added**:
1. After Phase 1 (Step 1.8):
   - Call `validate_phase_complete(validator, "phase1")`
   - If valid: Display Section 1 template with all collected data
   - If invalid: Show errors, use RCM to get missing info

2. After Phase 2.1 (All agent prompts):
   - Call `validate_phase_complete(validator, "phase2_1")`
   - If valid: Display Section 2 templates for all agents
   - If invalid: Show errors

3. After Phase 2.2 (All round instructions):
   - Call `validate_phase_complete(validator, "phase2_2")`
   - If valid: Display Section 3 templates for all rounds
   - If invalid: Show errors

**New Section**: "SCHEMA VALIDATION ERRORS"
- Guidelines for displaying validation errors to students
- RCM-based error resolution (GPT guides, doesn't write)

---

## Files Modified

1. **runtime_validator.py** (experimental/bios-architecture/code-interpreter-version/)
   - Added: `CanvasSchemaValidator` class (~160 lines)
   - Added: Schema validation methods to `WorkflowValidator`
   - Added: `validate_phase_complete()` helper function
   - Total: 633 lines (from 367)

2. **CUSTOM_GPT_INSTRUCTIONS.txt** (experimental/bios-architecture/code-interpreter-version/)
   - Added: "CANVAS COMPILATION DISPLAY" section (~260 lines)
   - Added: Phase 1, 2.1, 2.2 display templates
   - Added: Schema validation error handling
   - Total: 520 lines (from 304)

3. **B42-BIOS/README.md**
   - Updated: "What This Does" section
   - Updated: "validator/" description
   - Updated: "CUSTOM_GPT_INSTRUCTIONS.txt" description

4. **B42-BIOS/documentation/CANVAS_DATA_SCHEMA.md** (NEW)
   - Added: Schema reference document for developers
   - Not uploaded to GPT, but used as validation reference

---

## Testing the Enhancements

### Test 1: Phase 1 Schema Validation

**Scenario**: Complete Phase 1 but leave out agent persona

**Expected Behavior**:
```
⚠️ Phase 1 data incomplete:
  - Missing or empty agents[0].persona

Please provide a 2-3 sentence persona for [Agent Identifier].
This describes how the agent behaves and makes decisions.
```

GPT should NOT display Section 1 template until persona is provided.

---

### Test 2: Phase 1 Compilation Display

**Scenario**: Complete all Phase 1 steps with valid data

**Expected Behavior**:
After Step 1.8, GPT should:
1. Validate schema internally (Code Interpreter)
2. Display complete Section 1 template with all collected data
3. Show formatted output with:
   - Design Plan
   - Theoretical Problem
   - Goal
   - Setting
   - Concept A & B definitions
   - Baseline & Experimental designs
   - Round plan
   - All agents with goals/personas
4. Ask: "Ready to start drafting agent prompts? (yes/no)"

---

### Test 3: Phase 2.1 Agent Prompts Display

**Scenario**: Complete all agent prompts in Phase 2.1

**Expected Behavior**:
After last agent prompt, GPT should:
1. Validate all agents have prompts
2. Display Section 2 templates for ALL agents
3. Format each as:
   ```
   ROLE: You are the [Agent Identifier] + [purpose]+[name] + [human/non-human].
   PRIMARY GOAL: [Agent Goal]
   PERSONA: [Agent Persona]
   ```
4. Ask: "Ready to start drafting round instructions? (yes/no)"

---

### Test 4: Phase 2.2 Round Instructions Display

**Scenario**: Complete all round instructions and platform configs

**Expected Behavior**:
After last round config (Step 2.2.18 for final round), GPT should:
1. Validate all rounds have complete data
2. Display Section 3 templates for ALL rounds
3. Include full S3 template with:
   - SCENARIO
   - OBJECTIVE
   - INTERACTION RULES
   - TASKS THIS ROUND
   - AGENT BEHAVIORS
   - SEQUENCE
   - PLATFORM CONFIGURATION (all 9 fields)
4. Proceed to Phase 3 (Review)

---

### Test 5: Missing Platform Config Detection

**Scenario**: Complete Round 1 instructions but forget to specify "Detail level"

**Expected Behavior**:
```
⚠️ Phase 2.2 data incomplete:
  - Missing or empty rounds[0].platform_config.detail_level

Please specify the detail level for Round 1:
Min / Brief / Med / Thor / Exh / Dyn
```

GPT should NOT proceed to next round or display Section 3 until fixed.

---

## Benefits of These Enhancements

### For Students:
1. **Clear progress visibility**: See compiled sections after each phase
2. **Reduced cognitive load**: Don't hold everything in memory
3. **Copy-paste ready outputs**: Direct deployment to Chatstorm
4. **Error detection before proceeding**: Catch missing data early

### For Instructors:
1. **Data completeness guarantee**: Schema validation ensures nothing is missed
2. **Consistent formatting**: All students get properly structured outputs
3. **Debugging capability**: Schema errors show exactly what's missing

### For the BIOS:
1. **Data integrity**: Canvas data structure matches expected schema
2. **Phase gate enforcement**: Can't proceed with incomplete data
3. **Traceability**: Validation log tracks schema checks
4. **Type safety**: Number fields are numbers, arrays are arrays, etc.

---

## Comparison: Before vs After

### Before (BIOS v2.3):
- ✓ Step sequencing enforced
- ✓ Question validation
- ✓ Constraint checking
- ✗ No data structure validation
- ✗ Canvas updates internal only
- ✗ Students don't see compiled sections until end

### After (BIOS v2.4):
- ✓ Step sequencing enforced
- ✓ Question validation
- ✓ Constraint checking
- ✓ **Schema validation at phase boundaries** (NEW)
- ✓ **Progressive Canvas display** (NEW)
- ✓ **Students see compiled sections after validation** (NEW)
- ✓ **Type checking for data fields** (NEW)

---

## Implementation Notes

### Schema Definition
The schema is defined in `CANVAS_DATA_SCHEMA.md` but encoded directly in `CanvasSchemaValidator` class. This avoids needing to upload the schema file to GPT.

### Validation Timing
Schema validation occurs:
- After Step 1.8 (Phase 1 complete)
- After completing all agent prompts in Phase 2.1
- After completing all round configs in Phase 2.2

NOT validated on every step (too expensive). Only at phase boundaries.

### Canvas Data Tracking
The `WorkflowValidator` instance maintains `canvas_data` dict that accumulates student answers. This is what gets validated against schema.

GPT should call `validator.update_canvas_data(section, data)` after collecting each section's worth of data.

### Display Format
The display templates use the original S1, S2, S3 template formats from KB[3] (B42 Chatstorm T.A. Guide v4.2.txt). This ensures consistency with the assignment requirements.

---

## Deployment

**No changes to deployment process**. Just re-upload:
1. `runtime_validator.py` (enhanced version)
2. `CUSTOM_GPT_INSTRUCTIONS.txt` (enhanced version)

All other files remain the same (11 total files to upload).

---

## Version History

- **v2.3** (2025-01-18): Code Interpreter validation, step enforcement
- **v2.4** (2025-01-19): Schema validation + Progressive Canvas display

---

**Status**: ✅ Ready to deploy

**Recommendation**: Test with one student first to verify schema validation and Canvas display work as expected.
