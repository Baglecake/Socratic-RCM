# BIOS v2.2 - Force-Read Enforcement Improvements

**Date**: 2025-01-19
**Previous Version**: v2.1.1 (RCM output fix)
**Status**: Testing Required

---

## Issues Addressed

Based on comprehensive testing with local LLM (Gemma) documented in [chat_test3.txt](../../../chat_test3.txt), three critical force-read failures were identified:

### Issue 1: Platform Configuration Questions Skipped ❌
**Problem**: BIOS executed Steps 2.2.1-2.2.8 (round scenario/concept/rules questions) correctly but then **skipped Steps 2.2.9-2.2.19** entirely (platform configuration for each round), jumping directly to Phase 2.3 (helper templates).

**Impact**: 11 steps × 5 rounds = **55 questions skipped**. This resulted in no platform configuration data collected (participants, flow settings, style settings, options, model selection).

**Evidence**: chat_test3.txt lines 700-707 show jump from Round 5 rules directly to "Phase 2 complete! Moving to final review."

### Issue 2: File Export Question Hallucinated ❌
**Problem**: BIOS asked "Export time—would you like your simulation exported as: A) Raw text B) Google Doc C) Downloadable PDF D) All of the above?" (chat_test3.txt line 736-738).

**This question DOES NOT EXIST in Phase 3 runtime file.**

**Impact**: Violates Prohibition #5 (NO FILE CREATION). The BIOS invented a feature that contradicts core prohibitions. This demonstrates the BIOS is improvising questions not in runtime files.

**Evidence**: Phase 3 runtime only contains Steps 3.1, 3.2, and 3.3 - no export options defined.

### Issue 3: Table Data Not Accumulated in Final Output ❌
**Problem**: BIOS generated tables throughout Phase 2 (Round 1-5 Concept A/B, Rules tables) but initial compilation (chat_test3.txt lines 779-798) only referenced tables ("See table Round 1 - Concept A") without including actual data.

**Impact**: Student had to ask "Are you unable to include the table data?" before BIOS provided complete output. This shows no explicit accumulation step exists.

**Evidence**: Tables were created during workflow but not automatically compiled into final document.

---

## Fixes Applied

### 1. BIOS System Prompt Changes (v2.1.1 → v2.2)

#### **Added Prohibition #7: NO IMPROVISATION**
```
7. **NO IMPROVISATION**: NEVER ask questions not explicitly defined in runtime files.
   If you think a question is needed but cannot find it in the runtime file, STOP and
   report: "Runtime error: Cannot locate next step."
```

**Purpose**: Prevent BIOS from inventing questions (like the file export option).

#### **Strengthened RUNTIME EXECUTION LOOP**

**Step 2 - RETRIEVE** (lines 52-56):
```diff
- Read ENTIRE step block: TARGET, INSTRUCTION, REQUIRED OUTPUT, RCM CUE, CONSTRAINT
+ Read ENTIRE step block: TARGET, INSTRUCTION, REQUIRED OUTPUT, RCM CUE, CONSTRAINT, **NEXT STEP**
+ **CRITICAL**: The NEXT STEP field is MANDATORY. If you cannot find it, STOP and report error.
+ **NEVER skip steps**. Each step MUST be executed before advancing.
+ **NEVER jump phases** without completing all steps in current phase.
```

**Step 6 - ADVANCE** (lines 83-93):
```diff
- Use NEXT STEP from runtime file (NEVER improvise sequence)
+ **READ the NEXT STEP field from current step block**
+ **VERIFY that NEXT STEP exists in runtime file before proceeding**
+ If NEXT STEP not found: STOP and report "Runtime error: Step X.Y.Z specifies NEXT STEP [value] but I cannot locate it."
+ **NEVER improvise or assume what comes next**
```

**Added SPECIAL ENFORCEMENT** (lines 95-97):
```
**SPECIAL ENFORCEMENT**:
- **Phase 2.2 Platform Configuration**: After Step 2.2.8 (compile round instructions),
  you MUST proceed to Step 2.2.9 (platform config). DO NOT skip to Phase 2.3.
- **Phase 3 Compilation**: You MUST retrieve and execute ALL Phase 3 steps from runtime file.
  DO NOT add export options not specified in runtime.
```

#### **Enhanced ERROR HANDLING**

**Added new error case** (lines 169-171):
```
### Cannot Find NEXT STEP in Runtime
- STOP execution
- Report: "Runtime error: Current step specifies NEXT STEP [value] but I cannot locate it in the runtime file."
```

#### **Updated SUCCESS METRICS**

**Added two new metrics** (lines 195-196):
```
✓ **ALL steps executed sequentially without skipping**
✓ **NO questions asked that aren't in runtime files**
```

#### **Updated MANTRA**

**Old**: "I execute steps silently. I show students questions with Socratic guidance. I cite theory from lectures. I never display debugging info."

**New**: "I execute steps silently. I show students questions with Socratic guidance. I cite theory from lectures. I never display debugging info. **I NEVER skip steps or improvise questions.**"

---

### 2. Phase 2 Runtime Changes

#### **Step 2.2.8 - Added CRITICAL STOP Barrier** (line 158)
```diff
CONSTRAINT:
- Use student's exact wording
- Follow KB[1] template structure
+ **CRITICAL STOP**: DO NOT proceed to Phase 2.3 yet! After compiling round instructions,
+ you MUST ask platform configuration questions (Steps 2.2.9-2.2.19) for THIS round
+ BEFORE moving to the next round or Phase 2.3.
NEXT STEP: 2.2.9 (platform config for same round)
```

**Purpose**: Explicit barrier to prevent BIOS from jumping to Phase 2.3 prematurely.

#### **Step 2.2.19 - Enhanced Loop Logic** (lines 284-290)
```diff
- NEXT STEP: 2.2.1 (next round) OR 2.3 (if all rounds complete)
+ NEXT STEP LOGIC:
+ - **Count total rounds from Step 1.4.2**
+ - **Check current round number**
+ - If current round < total rounds: Go to Step 2.2.1 (next round scenario)
+ - If current round = total rounds (all rounds complete): Go to Step 2.3.1 (helper templates)
+ **DO NOT skip to Phase 2.3 if rounds remain!**
+ NEXT STEP: 2.2.1 (next round) OR 2.3.1 (if all rounds complete)
```

**Purpose**: Explicit conditional logic to help BIOS determine correct next step.

---

### 3. Phase 3 Runtime Changes

#### **Step 3.2 - Removed "Export" Trigger Language** (line 30)
```diff
- RCM CUE: "This is your last chance to make changes before export"
+ RCM CUE: "This is your last chance to make changes before we compile everything"
```

**Purpose**: Avoid language that might trigger hallucinated export options.

#### **Added Step 3.2.5 - Compile Complete Design Document** (NEW - lines 38-89)

**TARGET**: Compile Complete Design Document

**INSTRUCTION**: Output the complete simulation design in chat with ALL accumulated data from Phases 1 and 2.

**REQUIRED OUTPUT**: Display comprehensive design document with these sections:
1. **SECTION 1: CONCEPT DEFINITIONS** (from Steps 1.2.3-1.2.4)
2. **SECTION 2: EXPERIMENTAL DESIGN** (from Steps 1.3.1-1.3.3)
3. **SECTION 3: SETTING & STRUCTURE** (from Steps 1.4.1-1.4.3)
4. **SECTION 4: AGENTS** (agent roster + all agent prompts from Phase 2.1)
5. **SECTION 5: ROUND DETAILS** - For each round:
   - Scenario
   - Concept A in this round
   - Concept B in this round
   - Rules table
   - Tasks
   - Sequence
   - **Platform Configuration Checklist** (NEW - includes all Step 2.2.9-2.2.17 data)
6. **SECTION 6: HELPER FUNCTIONS** (from Steps 2.3.1-2.3.4)

**CONSTRAINT**:
- This must be displayed IN CHAT using `||...||` markers
- Include ALL student data collected throughout workflow
- Include ALL tables generated during Phase 2
- **Do NOT offer file download, PDF, or Google Doc export**
- Student should be able to copy this text directly from chat

**Purpose**: Explicit compilation step that gathers all accumulated data and outputs complete document in chat.

#### **Step 3.3 - Removed Export/Deliverables Language** (lines 93-102)
```diff
- REQUIRED OUTPUT: "Ready: S1 (ref), [n] Agent Prompts, [n] Round Instructions+Config, Helpers.
-   Next: KB[3] Phase 3 testing. Review vs KB[2]. Excellent theoretical work on [A] vs [B]!"
+ REQUIRED OUTPUT: "Design complete! You've created a solid experiment testing [A] vs [B].
+   Next: Follow KB[3] Phase 3 testing instructions to run your simulation. Excellent theoretical work!"

CONSTRAINT:
- Celebrate student's work (supportive tone)
- Confirm readiness for KB[3] Phase 3 testing
+ - Do NOT mention export, download, files, or deliverables
```

**Purpose**: Simple acknowledgment statement with no language that could trigger hallucinated export options.

---

## Testing Plan

### Required Tests

1. **Platform Configuration Enforcement Test**
   - Run through Phase 2 with 3 rounds
   - Verify Steps 2.2.9-2.2.19 asked for EACH round
   - Verify no skip to Phase 2.3 until all rounds complete

2. **Export Hallucination Prevention Test**
   - Complete full workflow through Phase 3
   - Verify NO file export question appears
   - Verify Step 3.2.5 outputs complete document in chat
   - Verify Step 3.3 simple completion message only

3. **Table Accumulation Test**
   - Complete workflow with 5 rounds
   - Verify Step 3.2.5 includes ALL:
     * Agent prompts (5 agents)
     * Round scenarios (5 rounds)
     * Concept A/B tables (5 rounds each)
     * Rules tables (5 rounds)
     * Platform config checklists (5 rounds)

4. **Sequential Execution Verification**
   - Monitor for any step-skipping
   - Verify NEXT STEP field followed precisely
   - Verify no improvised questions

### Success Criteria

- ✅ All platform config questions asked (Steps 2.2.9-2.2.19 × rounds)
- ✅ NO file export option appears
- ✅ Complete design document output in chat at Step 3.2.5
- ✅ All tables included in final compilation
- ✅ No step-skipping observed
- ✅ No hallucinated questions

---

## Version Comparison

| Feature | v2.1.1 | v2.2 |
|---------|--------|------|
| **RCM Verbatim Output** | ✅ Fixed | ✅ Retained |
| **Platform Config Questions** | ❌ Skipped | ✅ Enforced with CRITICAL STOP |
| **File Export Hallucination** | ❌ Present | ✅ Prevented (Prohibition #7 + language removal) |
| **Table Compilation** | ❌ References only | ✅ Full accumulation (Step 3.2.5) |
| **Step-Skipping Prevention** | ⚠️ Weak | ✅ Strong (NEXT STEP verification) |
| **Improvisation Prevention** | ⚠️ Implied | ✅ Explicit (Prohibition #7) |
| **Error Reporting** | Basic | Enhanced (NEXT STEP validation) |

---

## Files Modified

### Created
- `B42_BIOS_System_Prompt_v2.2-PRODUCTION.txt` (new version)

### Modified
- `B42_Runtime_Phase2_Drafting.txt`:
  - Step 2.2.8: Added CRITICAL STOP barrier (line 158)
  - Step 2.2.19: Enhanced loop logic (lines 284-290)

- `B42_Runtime_Phase3_Review.txt`:
  - Step 3.2: Changed RCM CUE wording (line 30)
  - **NEW** Step 3.2.5: Complete design compilation (lines 38-89)
  - Step 3.3: Removed export language (lines 93-102)

---

## Deployment Recommendation

**Status**: ⚠️ **Requires Testing Before Production**

**Next Steps**:
1. Upload BIOS v2.2 + updated runtime files to test GPT instance
2. Run comprehensive test with same scenario as chat_test3.txt
3. Verify all three issues resolved:
   - Platform config questions appear
   - No file export hallucination
   - Complete table compilation
4. If successful: Update production deployment
5. If issues persist: Analyze test output and iterate

**Rollback Plan**: If v2.2 introduces regressions, revert to v2.1.1 (which successfully fixed RCM output issue).

---

## Known Limitations

1. **NEXT STEP verification relies on GPT following instructions** - The BIOS can verify NEXT STEP exists, but enforcement still depends on GPT actually checking.

2. **Platform config enforcement uses explicit barrier language** - We're relying on "CRITICAL STOP" prominence to override GPT's tendency to skip ahead.

3. **Table accumulation is comprehensive but verbose** - Step 3.2.5 specifies 6 sections with detailed subsections. This may produce very long output.

4. **No automated round counting** - Step 2.2.19 instructs BIOS to "count total rounds from Step 1.4.2" but doesn't provide algorithm. BIOS must infer from context.

---

## Future Improvements

If v2.2 testing shows continued force-read failures:

1. **Consider adding step numbering enforcement** - Require BIOS to output "Executing Step X.Y.Z" internally (not shown to student) to force awareness.

2. **Add Phase 2.2 loop counter** - Explicitly track "Round 1 of 5 complete" to help BIOS know when to exit loop.

3. **Split Phase 2.2 into separate sub-phases** - Instead of one long loop, create Phase 2.2A (Round 1), Phase 2.2B (Round 2), etc.

4. **Consider returning to monolithic architecture** - If force-read reliability cannot be achieved, BIOS+Runtime separation may not be viable.

---

**Version**: BIOS v2.2 + Phase 2/3 Runtime Updates
**Date**: 2025-01-19
**Next**: Deploy to test environment and validate fixes
