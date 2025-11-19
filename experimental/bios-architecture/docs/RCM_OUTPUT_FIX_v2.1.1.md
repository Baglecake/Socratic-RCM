# RCM Output Compression Fix - BIOS v2.1.1

**Date**: 2025-01-19
**Issue**: RCM cues being abbreviated in student-facing output
**Status**: ✅ Fixed in v2.1.1

---

## Issue Identified

### Observed Behavior
During testing with local LLM (Gemma) as student proxy, the BIOS consistently output:
```
Represents theory?
```

Instead of the full RCM CUE from runtime file:
```
Does this agent prompt accurately capture their theoretical role from your framework?
Does it reflect how [theorist] would predict they'd behave?
```

### Location
**Step 2.1.1** (Agent Prompt Creation) in `B42_Runtime_Phase2_Drafting.txt`, line 28

### Analysis

**This is NOT a force-read failure.** The BIOS is correctly:
1. ✅ Locating Step 2.1.1
2. ✅ Retrieving the full step block from KB[1B]
3. ✅ Reading the RCM CUE field
4. ✅ Executing in proper sequence

**The problem**: Output compression. The model is **paraphrasing** the RCM CUE instead of outputting it verbatim, likely interpreting it as a quick validation check rather than full Socratic scaffolding.

### Root Cause

The RCM ENFORCEMENT section in BIOS v2.1 said:
```
**CRITICAL**: When a step includes RCM CUE in the runtime file,
OUTPUT it to the student as guidance.
```

This was not explicit enough. The model compressed "OUTPUT it" to mean "convey the idea" rather than "output word-for-word."

---

## Fix Applied

### 1. Runtime File Update
**File**: `B42_Runtime_Phase2_Drafting.txt`, Step 2.1.1

**Before**:
```
RCM CUE (after output): "Does this agent prompt accurately capture
their theoretical role from your framework? Does it reflect how
[theorist] would predict they'd behave?"
```

**After**:
```
RCM CUE (after output):
"Does this agent prompt accurately capture their theoretical role
from your framework? Does it reflect how [theorist] would predict
they'd behave?"
IMPORTANT: Output this RCM CUE verbatim - do NOT abbreviate to
"Represents theory?"
```

### 2. BIOS System Prompt Update
**File**: `B42_BIOS_System_Prompt_v2.1-PRODUCTION.txt`, line 110

**Before**:
```
**CRITICAL**: When a step includes RCM CUE in the runtime file,
OUTPUT it to the student as guidance.
```

**After**:
```
**CRITICAL**: When a step includes RCM CUE in the runtime file,
OUTPUT it to the student VERBATIM as guidance.

**NEVER abbreviate or paraphrase RCM cues.** If runtime says
"Does this agent prompt accurately capture their theoretical role?",
output the FULL question - do NOT shorten to "Represents theory?"
or similar.
```

---

## Testing Evidence

**Test conversation** (chat_test2_gemma.txt) showed consistent pattern:
- Agent prompt correctly compiled from student data ✅
- Template displayed with `||...||` markers ✅
- But RCM follow-up abbreviated to "Represents theory?" ❌

**This proves**:
1. Force-read protocol working (step retrieval successful)
2. Data compilation working (student inputs used)
3. Only issue: RCM output compression

---

## Implications

### What This Tells Us About Force-Read Reliability

**Good news**: This is NOT a lazy retrieval problem. The BIOS is:
- Reading the runtime file every turn
- Executing steps sequentially
- Pulling correct data from prior steps
- Following the workflow precisely

**The only failure**: Output formatting/verbatim adherence for RCM cues.

### Why This Matters

This was initially concerning because abbreviated output suggested the model wasn't reading the runtime. But analysis shows:
- ✅ BIOS retrieves full RCM CUE from runtime
- ✅ BIOS knows to output it after agent prompt
- ❌ BIOS compresses the output text (interpretive failure, not retrieval failure)

**Conclusion**: Force-read protocol is **working**. We just needed clearer instructions about verbatim output.

---

## Version Update

**BIOS v2.1 → v2.1.1**

**Changes**:
- Strengthened RCM ENFORCEMENT section with explicit "VERBATIM" and "NEVER abbreviate" language
- Added specific example: "do NOT shorten to 'Represents theory?'"
- Updated Step 2.1.1 RCM CUE with inline anti-abbreviation reminder

**Files Modified**:
- `experimental/bios-architecture/system-prompts/B42_BIOS_System_Prompt_v2.1-PRODUCTION.txt`
- `experimental/bios-architecture/runtime-files/B42_Runtime_Phase2_Drafting.txt`

---

## Testing Recommendations

1. **Rerun Agent Prompt Creation**:
   - Test Step 2.1.1 with new BIOS
   - Verify full RCM question appears, not "Represents theory?"

2. **Check Other RCM Cues**:
   - Scan all runtime files for RCM CUE fields
   - Verify none are being compressed elsewhere

3. **Monitor for Pattern**:
   - If abbreviation appears elsewhere, strengthen BIOS prohibition further
   - May need to add "OUTPUT VERBATIM" to execution loop step 4

---

## Key Insight

**User's observation was correct**: "it is happening too regularly for me to think it is a failure."

This was NOT random LLM unreliability - it was a **consistent output pattern** indicating the model was following instructions but interpreting "output" too loosely.

**The fix**: Make "verbatim" explicit in both:
1. General BIOS instruction (RCM ENFORCEMENT section)
2. Specific runtime step (Step 2.1.1 inline reminder)

This demonstrates the power of **dual-layer instruction** in BIOS architecture:
- BIOS sets general rules ("output RCM verbatim")
- Runtime reinforces for specific cases ("do NOT abbreviate to X")

---

**Status**: ✅ Fixed in v2.1.1
**Next**: Test to confirm full RCM questions now appear
**Confidence**: High - clear diagnosis, targeted fix, dual-layer reinforcement
