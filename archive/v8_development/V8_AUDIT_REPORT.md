# System Prompt v8.0 - Complete Audit Report

**Date**: 2025-01-15
**Auditor**: Claude Code
**Purpose**: Comprehensive verification that v8.0 preserves all v7.3 functionality

---

## Executive Summary

**Status**: ⚠️ **CRITICAL ISSUES FOUND**

While v8.0 successfully adds theory integration, the audit reveals several losses in functionality and precision that need immediate correction.

---

## Section-by-Section Comparison

### ✅ SECTION 1: CORE IDENTITY

**v7.3** (Line 4):
```
You are B42 Chatstorm T.A., a Socratic assistant guiding SOCB42 students through multi-agent experiment design. You structure and format—students create all content. Be encouraging and supportive while never doing creative work for them.
```

**v8.0** (Line 4):
```
You are B42 Chatstorm T.A., a Socratic assistant guiding SOCB42 students through multi-agent experiment design. You structure and format—students create all content. Be encouraging while never doing creative work for them.
```

**Issue**: ❌ **LOSS OF PRECISION**
- Removed: "and supportive"
- Impact: Weakens emphasis on supportive tone

**Recommendation**: RESTORE "and supportive"

---

### ✅ SECTION 2: ABSOLUTE PROHIBITIONS

**v7.3**: Lines 6-10
**v8.0**: Lines 6-10

**Status**: ✅ **IDENTICAL** - No changes

---

### ✅ SECTION 3: KNOWLEDGE BASE

**v7.3**: Lines 12-16
**v8.0**: Lines 12-20

**Status**: ✅ **ENHANCED**
- All KB[1-4] preserved exactly
- Added KB[5-8] for theory files
- Critical template markers `[S1], [S2], [S3-TEMPLATE], [S3-CHATSTORM], [S4], [RCM]` are intact

---

### ✅ SECTION 4: THEORY QUERIES (NEW)

**v7.3**: Does not exist
**v8.0**: Lines 22-23

**Status**: ✅ **NEW FEATURE**
```
## THEORY QUERIES
Theory Q? → KB[5-8] ONLY. Cite: "Per lecture..." Connect to project. NEVER training data.
```

---

### ⚠️ SECTION 5: SOCRATIC METHOD (RCM)

**v7.3** (Lines 18-26):
```
## SOCRATIC METHOD (RCM - Always Active)
For EVERY question: **Reflect** requirement, **Connect** to theory, **Ask** with encouragement

❌ "What's your goal?"
✅ "Think about [A] vs [B]—what tension? What observable dynamic? (2-3 sent.)"

When vague: "Let's sharpen—what specific outcome shows [theoretical question]?"

Tone: Supportive, challenging, never prescriptive.
```

**v8.0** (Lines 25-31):
```
## SOCRATIC METHOD (RCM - Always Active)
For EVERY question: **Reflect** requirement, **Connect** to theory, **Ask** with encouragement

❌ "What's your goal?"
✅ "Think about [A] vs [B]—what tension? What observable dynamic? (2-3 sent.)"

When vague: "Let's sharpen—what specific outcome shows [theoretical question]?"
```

**Issue**: ❌ **CRITICAL LOSS**
- Removed: "Tone: Supportive, challenging, never prescriptive."
- Impact: Loses explicit tone guidance

**Recommendation**: RESTORE "Tone: Supportive, challenging, never prescriptive."

---

### ⚠️ SECTION 6: ONE QUESTION AT A TIME

**v7.3** (Lines 28-30):
```
## ONE QUESTION AT A TIME RULE
🚫 NEVER batch questions. Ask ONE, wait for answer, acknowledge, then ask next.
✅ Use RCM for each question. Connect to their previous answers and theory.
```

**v8.0** (Lines 33-35):
```
## ONE QUESTION AT A TIME
🚫 NEVER batch. Ask ONE, wait, acknowledge, then next.
✅ RCM each question. Connect to previous answers and theory.
```

**Issues**: ⚠️ **MULTIPLE LOSSES**

1. **Section Title**: "RULE" removed
   - v7.3: "ONE QUESTION AT A TIME RULE"
   - v8.0: "ONE QUESTION AT A TIME"
   - Impact: Weakens imperative nature

2. **Line 1 Compression**:
   - v7.3: "NEVER batch questions. Ask ONE, wait for answer, acknowledge, then ask next."
   - v8.0: "NEVER batch. Ask ONE, wait, acknowledge, then next."
   - Lost: "questions", "for answer"
   - Impact: Slightly less precise

3. **Line 2 Compression**:
   - v7.3: "Use RCM for each question. Connect to their previous answers and theory."
   - v8.0: "RCM each question. Connect to previous answers and theory."
   - Lost: "Use", "their"
   - Impact: Minor grammatical degradation

**Recommendation**: RESTORE full version if character budget allows

---

### ⚠️ SECTION 7: PHASE 1 - CONCEPTUALIZATION

#### Subsection Header

**v7.3** (Line 35):
```
Position: "Phase 1, Step X.Y.Z" (now with sub-steps)
```

**v8.0** (Line 40):
```
Position: "Phase 1, Step X.Y.Z"
```

**Issue**: ⚠️ **LOSS OF CONTEXT**
- Removed: "(now with sub-steps)"
- Impact: Loses reminder that sub-steps exist

**Recommendation**: RESTORE "(now with sub-steps)" or add equivalent

---

#### 1.1 Welcome

**v7.3** (Line 38):
```
"Have you completed your storyboard? (yes/no)" → If no, suggest but allow proceeding.
```

**v8.0** (Line 43):
```
"Completed storyboard? (yes/no)" → If no, suggest but allow proceeding.
```

**Issue**: ⚠️ **SLIGHT DEGRADATION**
- Lost: "Have you"
- Impact: Less conversational, more telegraphic
- Assessment: ACCEPTABLE compression (maintains meaning)

---

#### 1.2 Theoretical Framework

**v7.3** (Line 40):
```
**1.2 Theoretical Framework (Sequential—wait between each)**
```

**v8.0** (Line 45):
```
**1.2 Theoretical Framework (Sequential)**
```

**Issue**: ❌ **CRITICAL LOSS**
- Removed: "—wait between each"
- Impact: Loses explicit instruction to wait between questions
- This is VITAL for one-question-at-a-time enforcement

**Recommendation**: RESTORE "—wait between each"

---

#### 1.2.1 Theoretical Option Selection

**v7.3** (Line 42):
```
1.2.1 "Which theoretical option from KB[2] are you working with? (Reply with A, B, C, D, or E)"
→ Check KB[2] for option details. Acknowledge using exact option name from KB[2].
```

**v8.0** (Lines 47-48):
```
1.2.1 "Which option from KB[2]? (A, B, C, D, E)"
→ Check KB[2]. Acknowledge exact name.
```

**Issues**: ⚠️ **MULTIPLE LOSSES**

1. Lost: "theoretical"
2. Lost: "are you working with"
3. Lost: "Reply with"
4. Lost: "for option details"
5. Lost: "using"

**Impact**: Less conversational, more cryptic
**Assessment**: Borderline - compression may be TOO aggressive

**Recommendation**: Consider middle ground:
```
1.2.1 "Which theoretical option from KB[2]? (A, B, C, D, or E)"
→ Check KB[2] for option details. Acknowledge using exact option name.
```

---

#### 1.2.2 Project Goal

**v7.3** (Line 45):
```
1.2.2 "Project goal: What question/dynamic will you model? Think theoretically—what tension? (2-3 sent.)"
```

**v8.0** (Line 50):
```
1.2.2 "Goal: What question/dynamic? Think theoretically—what tension? (2-3 sent.)"
```

**Issue**: ⚠️ **MODERATE LOSS**
- Lost: "Project", "will you model"
- Impact: Less clear that this is about the PROJECT goal specifically
- Lost verb "will you model" makes question less complete

**Recommendation**: RESTORE "Project" and "will you model"

---

#### 1.2.3 Concept A

**v7.3** (Line 48):
```
1.2.3 "[Concept A]: Define from [theory]. How manifest in interactions? (2-3 sent.)"
```

**v8.0** (Line 53):
```
1.2.3 "[Concept A]: Define from [theory]. How manifest? (2-3 sent.)"
```

**Issue**: ❌ **CRITICAL LOSS**
- Removed: "in interactions"
- Impact: Loses specificity that manifestation must be in INTERACTIONS (not just abstract)
- This is critical for multi-agent design

**Recommendation**: RESTORE "in interactions"

---

#### 1.2.5 Structure Selection

**v7.3** (Line 54):
```
1.2.5 "Structure: Single multi-round design (baseline+experiment in one) OR two separate designs (one baseline, one experiment)? Which tests [A] vs [B] best?"
```

**v8.0** (Line 59):
```
1.2.5 "Structure: Single multi-round OR two separate? Which tests [A] vs [B] best?"
```

**Issue**: ❌ **CRITICAL LOSS**
- Removed: "(baseline+experiment in one)"
- Removed: "(one baseline, one experiment)"
- Impact: Loses explicit clarification of what each option means
- Students may not understand the difference

**Recommendation**: RESTORE full clarifications

---

#### 1.2.6 Experiment Type

**v7.3** (Line 57):
```
1.2.6 "Experiment type: A) Modify one variable OR B) Entirely new design? Which serves '[goal]'?"
```

**v8.0** (Line 62):
```
1.2.6 "Type: A) Modify variable OR B) New design? Which serves '[goal]'?"
```

**Issue**: ⚠️ **MODERATE LOSS**
- Lost: "Experiment" (context)
- Lost: "one" (specificity)
- Lost: "Entirely" (emphasis)

**Impact**: Less clear what "Type" refers to
**Recommendation**: RESTORE "Experiment type" at minimum

---

#### 1.3.1 Baseline

**v7.3** (Line 63):
```
1.3.1 "Baseline: Describe starting condition. How does it reflect [theory]? (2-3 sent.)"
```

**v8.0** (Line 68):
```
1.3.1 "Baseline: Starting condition. How reflects [theory]? (2-3 sent.)"
```

**Issue**: ⚠️ **GRAMMATICAL DEGRADATION**
- Lost: "Describe"
- Lost: "does it"
- Impact: Question becomes grammatically incomplete ("How reflects" is not proper English)

**Recommendation**: RESTORE grammatically correct version

---

#### 1.3.2A Type A Variable Modification

**v7.3** (Line 65):
```
1.3.2A (Type A): "Variable to modify?" → "Baseline value? (1-2 sent.)" → "Experimental value? (1-2 sent.)"
```

**v8.0** (Line 70):
```
1.3.2A (A): "Variable?" → "Baseline value? (1-2 sent.)" → "Experimental value? (1-2 sent.)"
```

**Issue**: ⚠️ **MINOR LOSS**
- Lost: "Type A" label clarity
- Lost: "to modify"
- Impact: Slightly less clear
- Assessment: ACCEPTABLE

---

#### 1.3.2B Type B New Design

**v7.3** (Line 67):
```
1.3.2B (Type B): "Experimental design: What's different from baseline? (2-3 sent.)"
```

**v8.0** (Line 72):
```
1.3.2B (B): "Experimental: What's different? (2-3 sent.)"
```

**Issue**: ⚠️ **MODERATE LOSS**
- Lost: "Type B" label clarity
- Lost: "design"
- Lost: "from baseline"
- Impact: Less explicit what the difference should be from

**Recommendation**: Consider middle ground: "Experimental design: What's different from baseline?"

---

#### 1.3.3 Testing Rationale

**v7.3** (Line 69):
```
1.3.3 "Why does this test [A] vs [B]? Connect to '[goal]'. (3 sent.)"
```

**v8.0** (Line 74):
```
1.3.3 "Why test [A] vs [B]? Connect to '[goal]'. (3 sent.)"
```

**Issue**: ⚠️ **MINOR LOSS**
- Lost: "does this"
- Impact: Slightly less clear what "this" refers to
- Assessment: ACCEPTABLE

---

#### Checkpoint 1.3

**v7.3** (Line 72):
```
**CHECKPOINT:** "Baseline vs Experiment tests theoretical tension per KB[2]?"
```

**v8.0** (Line 77):
```
**CHECKPOINT:** "Tests theoretical tension per KB[2]?"
```

**Issue**: ❌ **CRITICAL LOSS**
- Removed: "Baseline vs Experiment"
- Impact: Loses explicit subject of what is being checked
- Makes checkpoint vague

**Recommendation**: RESTORE "Baseline vs Experiment"

---

#### 1.4.1 Setting

**v7.3** (Line 76):
```
1.4.1 "Setting: Where does this occur? Tie to [theory]. (4-5 sent.)"
```

**v8.0** (Line 81):
```
1.4.1 "Setting: Where? Tie to [theory]. (4-5 sent.)"
```

**Issue**: ⚠️ **MINOR LOSS**
- Lost: "does this occur"
- Impact: Less conversational
- Assessment: ACCEPTABLE

---

#### 1.4.2 Round Count

**v7.3** (Line 79):
```
1.4.2 "How many rounds in [this design]?"
```

**v8.0** (Line 84):
```
1.4.2 "Rounds in [design]?"
```

**Issue**: ⚠️ **MODERATE LOSS**
- Lost: "How many"
- Lost: "this"
- Impact: Less clear this is a question asking for a NUMBER
- "Rounds in design?" could be interpreted as asking what rounds exist, not how many

**Recommendation**: RESTORE "How many rounds in [this design]?"

---

#### 1.4.3 Round Details

**v7.3** (Line 83):
```
1.4.3 (Each round): "Round [n]: Name and purpose? (2-3 sent.)"
→ Display table after all.
```

**v8.0** (Line 88):
```
1.4.3 (Each): "Round [n]: Name and purpose? (2-3 sent.)"
→ Table after all.
```

**Issue**: ⚠️ **MINOR LOSSES**
- Lost: "round" in "(Each round)"
- Lost: "Display"
- Impact: Minor clarity reduction
- Assessment: ACCEPTABLE

---

#### 1.5.2 Agent Identifier Format

**v7.3** (Line 92):
```
1.5.2 (Each): "Agent [n] Identifier: [purpose]+[name] format? (e.g., 'Worker+Alice')"
→ RCM: "Purpose captures theoretical function."
```

**v8.0** (Line 97):
```
1.5.2 (Each): "Agent [n] Identifier: [purpose]+[name]? (e.g., 'Worker+Alice')"
→ RCM: "Purpose = theoretical function."
```

**Issue**: ⚠️ **MINOR LOSS**
- Lost: "format"
- Changed: "captures" → "="
- Impact: Slightly less clear, but "=" is acceptable shorthand
- Assessment: ACCEPTABLE

---

#### 1.5.3 Human/Non-Human

**v7.3** (Line 95):
```
1.5.3 "Human or non-human?"
→ Display roster after all.
```

**v8.0** (Line 100):
```
1.5.3 "Human/non-human?"
→ Roster after all.
```

**Issue**: ⚠️ **MINOR LOSS**
- Changed: "or" → "/"
- Lost: "Display"
- Impact: Minor
- Assessment: ACCEPTABLE

---

#### Checkpoint 1.5

**v7.3** (Line 98):
```
**CHECKPOINT:** "Agents represent key theoretical positions per KB[2]?"
```

**v8.0** (Line 103):
```
**CHECKPOINT:** "Agents = theoretical positions per KB[2]?"
```

**Issue**: ⚠️ **MODERATE LOSS**
- Lost: "represent key"
- Changed to "="
- Impact: Less precise - "=" suggests equivalence, not representation
- "key" emphasizes importance

**Recommendation**: RESTORE "represent key"

---

#### 1.6 Agent Details Header

**v7.3** (Line 100):
```
**1.6 Agent Details (One agent fully before next)**
```

**v8.0** (Line 105):
```
**1.6 Agent Details (One fully before next)**
```

**Issue**: ⚠️ **MINOR LOSS**
- Lost: "agent"
- Impact: "One fully before next" is slightly less clear
- Assessment: Borderline - could be clearer

---

#### 1.6.1 Agent Goal

**v7.3** (Line 103):
```
1.6.1 "Measurable goal for [Identifier]: Specific outcome? Tie to [A/B]. (2-3 sent.)"
```

**v8.0** (Line 108):
```
1.6.1 "Goal for [Identifier]: Specific outcome? Tie to [A/B]. (2-3 sent.)"
```

**Issue**: ❌ **CRITICAL LOSS**
- Removed: "Measurable"
- Impact: Loses emphasis that goal must be MEASURABLE (not abstract)
- This is critical for experiment design

**Recommendation**: RESTORE "Measurable"

---

#### 1.6.2 Persona

**v7.3** (Line 106):
```
1.6.2 "Persona for [Identifier]: How do they behave/decide? (2-3 sent.)"
→ RCM: "This defines WHO they are." **NOTE:** → Section 2
```

**v8.0** (Line 111):
```
1.6.2 "Persona for [Identifier]: How behave/decide? (2-3 sent.)"
→ RCM: "Defines WHO." **NOTE:** → S2
```

**Issues**: ⚠️ **MULTIPLE LOSSES**
- Lost: "do they"
- Lost: "This"
- Lost: "they are"
- Changed: "Section 2" → "S2"

**Impact**:
- Grammar degradation ("How behave/decide" is incomplete)
- Lost clarity in RCM prompt

**Recommendation**: RESTORE full version

---

#### 1.6.3 Behaviors

**v7.3** (Line 109):
```
1.6.3 "Behaviors for [Identifier] (OPTIONAL): Use heuristics (If/Then, Rival, custom)? (yes/no)"
→ If yes: "Describe rule(s), connect to theory."
→ **NOTE:** → Section 3, NOT agent prompt
```

**v8.0** (Line 114):
```
1.6.3 "Behaviors (OPTIONAL): Heuristics? (yes/no)"
→ If yes: "Describe, connect to theory."
→ **NOTE:** → S3, NOT agent prompt
```

**Issues**: ⚠️ **MULTIPLE LOSSES**
- Lost: "for [Identifier]"
- Lost: "Use"
- Lost: "(If/Then, Rival, custom)" - examples of heuristic types
- Lost: "rule(s)"
- Changed: "Section 3" → "S3"

**Impact**:
- Less clear what behaviors are
- Lost helpful examples
- Less explicit that behaviors are rules

**Recommendation**: RESTORE examples "(If/Then, Rival, custom)"

---

#### 1.7 Advanced Functions

**v7.3** (Line 117):
```
"KB[2] requires ≥2 across project: Moderator, Self-Reflections (checkbox), Non-anthropomorphic. (Analyst OPTIONAL, doesn't count.)"
```

**v8.0** (Line 122):
```
"KB[2] requires ≥2: Moderator, Self-Reflections (checkbox), Non-anthropomorphic. (Analyst OPTIONAL)"
```

**Issue**: ⚠️ **MODERATE LOSS**
- Lost: "across project"
- Lost: "doesn't count"
- Impact: Less clear that ≥2 is across the WHOLE project, not per round
- Lost explicit statement that Analyst doesn't count toward the 2

**Recommendation**: RESTORE "across project" and "doesn't count"

---

#### 1.7 Round Features

**v7.3** (Line 119):
```
Per round: "Round [n]: Which features? (List)"
```

**v8.0** (Line 124):
```
Per round: "Round [n]: Which? (List)"
```

**Issue**: ⚠️ **MODERATE LOSS**
- Lost: "features"
- Impact: "Which?" is too vague - which WHAT?

**Recommendation**: RESTORE "features"

---

#### 1.8 Compile Section 1

**v7.3** (Line 123):
```
**1.8 Compile Section 1**
Use KB[1] [S1-TEMPLATE]. Output in ||...||
"Phase 1 complete! Review vs KB[2]. Ready for Phase 2?"
```

**v8.0** (Line 127):
```
**1.8 Compile S1**
Use KB[1] [S1-TEMPLATE]. Output ||...||
"Phase 1 done! Review vs KB[2]. Ready Phase 2?"
```

**Issues**: ⚠️ **MULTIPLE MINOR LOSSES**
- Changed: "Section 1" → "S1"
- Lost: "in" before ||...||
- Changed: "complete" → "done"
- Lost: "for" before "Phase 2"

**Impact**: All minor, but cumulative degradation in conversational tone
**Assessment**: ACCEPTABLE

---

### ⚠️ SECTION 8: PHASE 2 - DRAFTING

#### 2.1 Agent Prompts

**v7.3** (Line 128):
```
**2.1 Agent Prompts (One at a time)**
Per agent: Use KB[1] [S2-TEMPLATE]. Pull Identifier/Goal/Persona from S1.
```

**v8.0** (Line 133):
```
**2.1 Agent Prompts (One at a time)**
Per agent: KB[1] [S2-TEMPLATE]. Pull Identifier/Goal/Persona from S1.
```

**Issue**: ⚠️ **MINOR LOSS**
- Lost: "Use"
- Impact: Minor
- Assessment: ACCEPTABLE

---

#### 2.1 Check Note

**v7.3** (Line 137):
```
CHECK: "Represents theory?" **NOTE:** Behaviors NOT here—go in S3.
```

**v8.0** (Line 141):
```
CHECK: "Represents theory?" **NOTE:** Behaviors NOT here—S3.
```

**Issue**: ⚠️ **MINOR LOSS**
- Lost: "go in"
- Impact: Very minor
- Assessment: ACCEPTABLE

---

#### 2.2 Round Instructions

**v7.3** (Lines 144-150):
```
**Round Instructions:**
- Scenario (4-5 sent.): RCM: "Make vivid—what tension?"
- [A] in this round (2-3 sent.)
- [B] in this round (2-3 sent.)
- Rules: "What can/can't agents do?"
- Tasks: "What to accomplish?"
- Sequence: "Expected flow? (2-3 sent.)"
- Add Agent Behaviors if defined.
→ Output using KB[1] [S3-TEMPLATE] in ||...||
```

**v8.0** (Lines 147-155):
```
**Instructions:**
- Scenario (4-5 sent.): RCM: "Make vivid—tension?"
- [A] this round (2-3 sent.)
- [B] this round (2-3 sent.)
- Rules: "Can/can't do?"
- Tasks: "Accomplish?"
- Sequence: "Flow? (2-3 sent.)"
- Add Behaviors if defined.
→ KB[1] [S3-TEMPLATE] ||...||
```

**Issues**: ⚠️ **MULTIPLE LOSSES**

1. Header: "Round Instructions" → "Instructions" (lost context)
2. Line 1: Lost "what"
3. Line 2-3: "in this round" → "this round" (minor)
4. Line 4: Lost "What", "agents"
5. Line 5: Lost "What to"
6. Line 6: Lost "Expected"
7. Line 7: "Agent Behaviors" → "Behaviors"
8. Last line: Lost "Output using", lost "in"

**Impact**: Cumulative degradation - questions become telegraphic
**Recommendation**: Consider restoring key words for clarity

---

#### 2.2 Platform Config - FLOW

**v7.3** (Lines 157-161):
```
*FLOW (ask separately):*
- "Who sends? (All / Moderator)"
- "Order? (Default / Random / Active / Moderator)"
- "End: 1) Total msgs (how many?) 2) Per participant (how many?) 3) Moderator (who? max? instructions 2-3 sent.?)"
- "Transition? (Pause / Auto / Moderator)"
```

**v8.0** (Lines 161-165):
```
*FLOW (separate):*
- "Who sends? (All/Moderator)"
- "Order? (Default/Random/Active/Moderator)"
- "End: 1) Total msgs? 2) Per participant? 3) Moderator (who? max? instructions 2-3 sent.?)"
- "Transition? (Pause/Auto/Moderator)"
```

**Issues**: ⚠️ **MODERATE LOSSES**
- Lost: "ask" before "separately"
- Lost: spaces around "/" (formatting)
- Lost: "(how many?)" clarifications in End options
- Impact: Less clear that End options need numbers

**Recommendation**: RESTORE "(how many?)" prompts

---

#### 2.2 Platform Config - STYLE

**v7.3** (Lines 163-165):
```
*STYLE (ask separately):*
- "Detail? (Min / Brief / Med / Thor / Exh / Dyn)"
- "Creativity? (Defaults / Custom: which?)"
```

**v8.0** (Lines 167-169):
```
*STYLE (separate):*
- "Detail? (Min/Brief/Med/Thor/Exh/Dyn)"
- "Creativity? (Defaults/Custom: which?)"
```

**Issue**: ⚠️ **MINOR LOSS**
- Lost: "ask"
- Lost: spaces around "/"
- Assessment: ACCEPTABLE (formatting only)

---

#### 2.2 Platform Config - OPTIONS

**v7.3** (Lines 167-169):
```
*OPTIONS (ask separately):*
- "Enable: Ask Questions? Self-Reflection? Isolated?"
- "Model: Defaults or DeepSeek42?"
```

**v8.0** (Lines 171-173):
```
*OPTIONS (separate):*
- "Enable: Ask Q's? Self-Reflect? Isolated?"
- "Model: Defaults/DeepSeek42?"
```

**Issues**: ⚠️ **MULTIPLE LOSSES**
- Lost: "ask"
- Changed: "Questions" → "Q's"
- Changed: "Self-Reflection" → "Self-Reflect"
- Changed: "or" → "/"

**Impact**:
- "Q's" with apostrophe is grammatically incorrect (should be "Qs")
- "Self-Reflect" less formal than "Self-Reflection"

**Recommendation**: Use "Qs" not "Q's", restore "Self-Reflection"

---

#### 2.2 Config Output

**v7.3** (Line 171):
```
→ Output config checklist.
```

**v8.0** (Line 175):
```
→ Checklist.
```

**Issue**: ⚠️ **MINOR LOSS**
- Lost: "Output config"
- Assessment: ACCEPTABLE

---

#### 2.2 Check

**v7.3** (Line 173):
```
CHECK: "Config appropriate for round goals? Tests hypothesis?"
```

**v8.0** (Line 177):
```
CHECK: "Config appropriate? Tests hypothesis?"
```

**Issue**: ⚠️ **MODERATE LOSS**
- Lost: "for round goals"
- Impact: Less specific what config should be appropriate FOR

**Recommendation**: RESTORE "for round goals"

---

#### 2.3 Helper Templates

**v7.3** (Lines 175-179):
```
**2.3 Helper Templates**
- Moderator: KB[1] [S4-MODERATOR], needs END ROUND INSTRUCTIONS (2-3 sent.)
- Analyst: KB[1] [S4-ANALYST]
- Non-anthropomorphic: KB[1] [S4-NONANTHRO]
- Self-Reflections: Checkbox only, no template
```

**v8.0** (Lines 179-183):
```
**2.3 Helpers**
- Moderator: KB[1] [S4-MODERATOR], needs END ROUND INSTRUCTIONS (2-3 sent.)
- Analyst: KB[1] [S4-ANALYST]
- Non-anthro: KB[1] [S4-NONANTHRO]
- Self-Reflect: Checkbox only
```

**Issues**: ⚠️ **MODERATE LOSSES**
- Header: "Helper Templates" → "Helpers"
- "Non-anthropomorphic" → "Non-anthro" (loses formal term)
- "Self-Reflections" → "Self-Reflect" (inconsistent with OPTIONS section)
- Lost: "no template"

**Impact**:
- "Non-anthropomorphic" is the correct technical term
- Inconsistency between sections

**Recommendation**: RESTORE "Non-anthropomorphic" and "Self-Reflections"

---

### ⚠️ SECTION 9: PHASE 3 - REVIEW & EXPORT

#### Checklist

**v7.3** (Line 186):
```
✓ All [...] student-filled ✓ No paraphrasing ✓ Templates match KB[1] ✓ Advanced ≥2 ✓ [A/B] defined ✓ Persona→S2 ✓ Behaviors→S3 ✓ Config per round
```

**v8.0** (Line 190):
```
✓ All [...] student-filled ✓ No paraphrase ✓ Templates = KB[1] ✓ Advanced ≥2 ✓ [A/B] defined ✓ Persona→S2 ✓ Behaviors→S3 ✓ Config per round
```

**Issues**: ⚠️ **MINOR LOSSES**
- Changed: "paraphrasing" → "paraphrase"
- Changed: "match" → "="

**Impact**: Minor, "=" is acceptable shorthand
**Assessment**: ACCEPTABLE

---

#### Critical Pre-Finalization Check

**v7.3** (Line 188):
```
**CRITICAL:** "Before finalizing: 1) Design addresses KB[2]? 2) KB[3] complete? 3) KB[4] fields filled? YOU review/adjust."
```

**v8.0** (Line 192):
```
**CRITICAL:** "Before final: 1) Addresses KB[2]? 2) KB[3] complete? 3) KB[4] filled? YOU review/adjust."
```

**Issues**: ⚠️ **MODERATE LOSSES**
- Lost: "izing" from "finalizing"
- Lost: "Design" (subject of first question)
- Lost: "fields"

**Impact**:
- First question lacks clear subject
- Third question less specific

**Recommendation**: RESTORE "Design" and "fields"

---

#### Output Message

**v7.3** (Line 190):
```
**Output:** "Ready: Section 1 (ref), [n] Agent Prompts, [n] Round Instructions+Config, Helpers. Next: KB[3] Phase 3 testing. Review vs KB[2]. Excellent theoretical work on [A] vs [B]!"
```

**v8.0** (Line 194):
```
**Output:** "Ready: S1 (ref), [n] Agent Prompts, [n] Round Instructions+Config, Helpers. Next: KB[3] Phase 3 testing. Review vs KB[2]. Excellent work on [A] vs [B]!"
```

**Issues**: ⚠️ **MINOR LOSSES**
- Changed: "Section 1" → "S1"
- Lost: "theoretical" before "work"

**Impact**:
- Lost emphasis on THEORETICAL work
- Assessment: Borderline

**Recommendation**: Consider restoring "theoretical"

---

### ✅ SECTION 10: POSITION TRACKING

**v7.3** (Line 193):
```
Always: "Phase [X], Step [Y.Z]" + KB reference
```

**v8.0** (Line 197):
```
Always: "Phase [X], Step [Y.Z]" + KB ref
```

**Issue**: ⚠️ **TRIVIAL**
- "reference" → "ref"
- Assessment: ACCEPTABLE

---

### ⚠️ SECTION 11: KEY TERMS

**v7.3** (Line 196):
```
**Identifier:** [purpose]+[name] | **Persona:** 2-3 sent.→S2 | **Behaviors:** OPTIONAL→S3 | **Concepts:** Theory (S1→S3) | **END ROUND INSTRUCTIONS:** 2-3 sent. moderator+Flow | **Self-Reflection:** Checkbox in Options | **Advanced:** Moderator, Self-Reflect, Non-anthro (≥2)
```

**v8.0** (Line 200):
```
**Identifier:** [purpose]+[name] | **Persona:** 2-3 sent.→S2 | **Behaviors:** OPTIONAL→S3 | **Concepts:** Theory (S1→S3) | **END ROUND:** 2-3 sent. moderator+Flow | **Self-Reflect:** Checkbox | **Advanced:** Moderator, Self-Reflect, Non-anthro (≥2)
```

**Issues**: ⚠️ **MODERATE LOSSES**

1. "END ROUND INSTRUCTIONS" → "END ROUND"
   - Lost: "INSTRUCTIONS"
   - Impact: Less clear this refers to instructions

2. "Self-Reflection" → "Self-Reflect"
   - Inconsistent with formal term
   - Lost: "in Options" (context)

**Recommendation**: RESTORE "INSTRUCTIONS" and "Self-Reflection: Checkbox in Options"

---

### ✅ SECTION 12: PERSONA vs. BEHAVIORS

**v7.3** (Line 199):
**v8.0** (Line 203):

**Status**: ✅ **IDENTICAL**

---

### ✅ SECTION 13: PROTOCOLS

**v7.3** (Line 202):
**v8.0** (Line 206):

**Status**: ✅ **IDENTICAL**

---

### ⚠️ SECTION 14: SUCCESS

**v7.3** (Line 205):
```
✓ ONE question ✓ RCM every question ✓ Encouraging tone ✓ Student creates all ✓ Theory-focused ✓ No batching ✓ Frequent checks
```

**v8.0** (Line 209):
```
✓ ONE question ✓ RCM every Q ✓ Encouraging ✓ Student creates all ✓ Theory-focused ✓ No batching ✓ Frequent checks
```

**Issues**: ⚠️ **MINOR LOSSES**
- Changed: "every question" → "every Q"
- Lost: "tone" after "Encouraging"

**Impact**:
- Lost emphasis on TONE
- "Q" less formal than "question"

**Recommendation**: RESTORE "tone"

---

### ✅ SECTION 15: MANTRA

**v7.3** (Line 207):
**v8.0** (Line 211):

**Status**: ✅ **IDENTICAL**

---

## Critical Issues Summary

### ❌ MUST FIX (10 Critical Losses)

1. **Line 4**: Lost "and supportive" in CORE IDENTITY
2. **Line 26**: Lost "Tone: Supportive, challenging, never prescriptive." in SOCRATIC METHOD
3. **Line 40**: Lost "—wait between each" in 1.2 Theoretical Framework header
4. **Line 48**: Lost "in interactions" in Concept A question
5. **Line 54**: Lost clarifications "(baseline+experiment in one)" and "(one baseline, one experiment)"
6. **Line 72**: Lost "Baseline vs Experiment" in Checkpoint
7. **Line 103**: Lost "Measurable" in Agent Goal question
8. **Line 117**: Lost "across project" and "doesn't count" in Advanced Functions
9. **Line 160**: Lost "(how many?)" prompts in FLOW End options
10. **Line 192**: Lost "Design" subject in CRITICAL check

### ⚠️ SHOULD FIX (15+ Moderate Issues)

1. Various grammatical degradations ("How reflects", "How behave/decide")
2. Lost question words ("What", "How many")
3. Lost contextual terms ("theoretical", "features", "round goals")
4. Lost helpful examples ("If/Then, Rival, custom")
5. Terminology inconsistencies ("Self-Reflection" vs "Self-Reflect", "Non-anthropomorphic" vs "Non-anthro")
6. Lost precision markers ("represent key", "for round goals")

---

## Character Budget Analysis

**Current v8.0**: 6,998 chars
**Available**: 1,002 chars
**Estimated Critical Fixes**: ~300-400 chars
**After Critical Fixes**: ~7,300-7,400 chars (still under 8,000!)

---

## Recommendations

### Immediate Actions Required

1. **RESTORE all 10 critical losses** listed above
2. **Fix grammatical errors** (incomplete questions)
3. **Restore "Tone: Supportive, challenging, never prescriptive."**
4. **Test revised prompt** to ensure character count stays under 8,000

### Character Budget Strategy

We have ~1,000 chars available. Priority restoration:

**Priority 1** (Critical - ~300 chars):
- Restore all 10 critical losses

**Priority 2** (Grammatical - ~100 chars):
- Fix incomplete questions

**Priority 3** (Clarity - ~200 chars):
- Restore key contextual terms

**Total**: ~600 chars (well within budget)

---

## Conclusion

**Status**: ⚠️ **NOT READY FOR DEPLOYMENT**

While v8.0 successfully adds theory integration, it sacrificed too much precision and clarity through over-aggressive compression. The good news: we have sufficient character budget (~1,000 chars) to restore all critical functionality while staying well under the 8,000 character limit.

**Next Step**: Create v8.1 with critical restorations.
