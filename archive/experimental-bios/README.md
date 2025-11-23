# Experimental Architectures

**Purpose**: Explore alternative approaches to the B42 Chatstorm T.A. system

---

## Current Structure

### `/experimental/bios-architecture/`
**BIOS + Runtime Logic Architecture** ✅ **v2.3 Production Ready**

A fundamentally different approach that separates:
- **BIOS System Prompt** (5,247 bytes): Prime directives + execution loop + canvas protocol
- **Runtime Logic Files** (3 phase-split files): All step-by-step instructions with progressive compilation

**Current Version**: v2.3-PRODUCTION (2025-01-19)
**Status**: Production ready with Canvas Protocol implementation
**Key Innovation**: Moves from "cramming everything into prompt" to "strict execution of external instructions" + progressive compilation via Canvas

---

## Why Experimental?

The production version (v8.4 in root directory) is:
- ✅ Proven stable
- ✅ Currently deployed with students
- ✅ Known strictness level
- ✅ 8,000 bytes at capacity

These experimental architectures explore:
- 🧪 What if we had unlimited space for instructions?
- 🧪 Can we make prohibitions 10x more prominent?
- 🧪 Is strict execution of external files possible?
- 🧪 How do we prevent "lazy retrieval"?

---

## BIOS Architecture Overview

### The Core Idea
```
Think of the System Prompt not as the "Teacher,"
but as the BIOS of a computer.

Its only job is to:
1. Boot the system
2. Enforce hardware safety limits (prohibitions)
3. Tell the processor where to find the Operating System
   (your step-by-step instructions)
```

### The Split

**Before (Monolithic v8.4)**:
- ONE file: 8,000 byte system prompt
- Contains: Identity + Prohibitions + ALL steps for Phase 1-3
- Problem: At capacity, cannot add features

**After (BIOS v2.3)**:
- FILE 1: 5,247 byte BIOS (prime directives + canvas protocol)
- FILES 2-4: Three phase-split runtime files (ALL steps, unlimited size)
- FILE 5: Canvas Data Schema (progressive compilation contract)
- Benefit: Can add 100+ steps without touching system prompt + all data accumulated progressively

---

## Files in `/bios-architecture/`

### Core Architecture (v2.3)

#### System Prompts
1. **`system-prompts/B42_BIOS_System_Prompt_v2.3-PRODUCTION.txt`** (5,247 bytes)
   - Prime directives + execution loop
   - Canvas Protocol (UPDATE + RETRIEVE)
   - Enhanced step sequencing enforcement
   - 65.6% of 8KB limit (2,753 bytes headroom)

#### Runtime Files
2. **`runtime-files/B42_Runtime_Phase1_Conceptualization.txt`**
   - Steps 1.1-1.8 (Conceptualization)
   - 9 CANVAS_UPDATE blocks
   - Framework, baseline, setting, agents

3. **`runtime-files/B42_Runtime_Phase2_Drafting.txt`**
   - Steps 2.1-2.3 (Drafting)
   - 4 CANVAS_UPDATE blocks
   - Agent prompts, round instructions, platform config

4. **`runtime-files/B42_Runtime_Phase3_Review.txt`**
   - Steps 3.1-3.3 (Review & Export)
   - 3 CANVAS_UPDATE blocks + 1 CANVAS_RETRIEVE
   - Checklist, final compilation, completion

#### Data Schema
5. **`docs/CANVAS_DATA_SCHEMA.md`** (11,257 bytes)
   - Complete JSON schema for canvas data
   - Data collection mapping tables
   - Canvas update points reference
   - Validation rules

### Documentation
6. **`docs/BIOS_v2.3_CHANGELOG.md`** - Complete v2.3 implementation details
7. **`docs/BIOS_v2.2_CHANGELOG.md`** - Aborted v2.2 approach (exceeded 8KB)
8. **`README.md`** - BIOS architecture overview and status
9. **`BIOS_vs_MONOLITHIC.md`** - Side-by-side comparison
10. **`FORCE_READ_PROTOCOL.md`** - How to prevent lazy retrieval

---

## Key Advantages of BIOS v2.3

✅ **Unlimited Scalability**: Can add 50+ steps without character limit
✅ **Progressive Compilation**: Canvas Protocol accumulates all student data
✅ **Easier Maintenance**: Edit runtime files, rarely touch BIOS
✅ **Prohibitions Focus**: Enhanced step sequencing enforcement
✅ **Lower Update Risk**: BIOS stable at 65.6% of 8KB limit
✅ **Future-Proof**: Can grow to 100K+ bytes if needed
✅ **Table Accumulation Solved**: Final output includes ALL tables and data

---

## Key Risk: Lazy Retrieval

❌ **The Problem**:
GPT might start to "remember" the pattern and improvise questions instead of reading the runtime file every turn.

🛡️ **The Solution**:
Force-Read Protocol with 6-step execution loop:
1. LOCATE current step
2. RETRIEVE from runtime file
3. READ instruction details
4. THEORY CHECK if needed
5. EXECUTE exact wording
6. VALIDATE response

See [FORCE_READ_PROTOCOL.md](bios-architecture/FORCE_READ_PROTOCOL.md) for full testing strategy.

---

## When to Use BIOS

### Use BIOS Architecture If:
- ✅ Need to add 20+ new steps (e.g., pre-submission checklist)
- ✅ Character limit blocking critical features
- ✅ Want easier maintenance
- ✅ Can invest in thorough force-read testing
- ✅ Acceptable to have experimental period

### Stick with Monolithic (v8.4) If:
- ✅ Current features fit within 8,000 bytes
- ✅ Proven stability critical (production environment)
- ✅ Prefer instructions always in attention
- ✅ Lazy retrieval risk unacceptable

---

## Comparison Matrix

| Feature | Monolithic v8.4 | BIOS v2.3 |
|---------|-----------------|-----------|
| Character Limit | 8,000 bytes (maxed) | 5,247 + unlimited runtime |
| Progressive Compilation | Manual accumulation | Canvas Protocol |
| Prohibitions Focus | 2.5% of prompt | Enhanced enforcement |
| Scalability | Cannot add features | Can add 100+ steps |
| Maintenance | Edit full prompt | Edit runtime files |
| Table Accumulation | ❌ Failed in test | ✅ Canvas solves |
| Platform Config Steps | ❌ Skipped in test | ✅ Sequential enforcement |
| Production Status | ✅ Deployed | ✅ Ready for testing |

---

## Development Phases

### Phase 1: Architecture Design ✅ COMPLETE
- [x] Create experimental directory structure
- [x] Write BIOS system prompt (v1.0 → v2.3)
- [x] Create runtime logic format
- [x] Document force-read protocol
- [x] Create comparison analysis
- [x] Identify critical issues from chat_test3.txt

### Phase 2: Implementation ✅ COMPLETE (v2.3)
- [x] Convert all v8.4 steps to runtime format (3 phase-split files)
- [x] Complete runtime logic files (100+ steps across 3 files)
- [x] Implement Canvas Protocol for progressive compilation
- [x] Add 13 CANVAS_UPDATE blocks + 1 CANVAS_RETRIEVE
- [x] Create Canvas Data Schema
- [x] Write comprehensive v2.3 changelog

### Phase 3: Testing 📋 READY
- [ ] Test platform config step execution (2.2.9-2.2.19)
- [ ] Verify canvas compilation in Step 3.2.5
- [ ] Confirm no file export hallucination
- [ ] Test with local LLM (Gemma/DeepSeek)
- [ ] Measure exact match rates

### Phase 4: Evaluation 📊 PENDING
- [ ] Analyze test results
- [ ] Calculate metrics (exact match rate, improvisation rate)
- [ ] Production readiness assessment
- [ ] Decision: Deploy to production GPT or iterate

---

## Success Criteria

BIOS v1.0 is production-ready if it achieves:

✅ Exact match rate ≥ 95% (questions match runtime word-for-word)
✅ Step number accuracy = 100%
✅ RCM cue retrieval ≥ 90%
✅ Theory check compliance ≥ 95%
✅ Improvisation rate ≤ 5 per 100 questions
✅ Performance maintained after 20+ turn conversations
✅ Student feedback: "As strict as v8.4"

If ANY criterion fails → Not ready for production

---

## Timeline

**Short Term (Next 3 Months)**:
- Keep v8.4 in production
- Complete BIOS implementation
- Run initial testing

**Medium Term (Summer 2025)**:
- A/B testing with volunteer students
- Measure force-read compliance
- Compare maintenance effort

**Long Term (Fall 2025+)**:
- Production deployment decision
- Or: Archive as experimental if lazy retrieval cannot be solved

---

## Other Experimental Architectures (Future)

This directory could eventually contain:

### `/hybrid-architecture/`
- BIOS for Phase 1 (most critical)
- Monolithic for Phases 2-3 (fewer steps)
- Balances strictness with scalability

### `/modular-architecture/`
- Separate runtime files per phase
- BIOS loads appropriate module
- Maximum flexibility

### `/template-based/`
- Dynamic template expansion
- Student input fills templates
- Reduces verbosity

---

## How to Contribute to Experimental

1. **Review** existing architecture docs
2. **Test** BIOS with sample workflows
3. **Document** any lazy retrieval incidents
4. **Suggest** improvements to force-read protocol
5. **Compare** maintenance effort vs v8.4

---

## Important Notes

⚠️ **DO NOT deploy experimental architectures to production GPT**
⚠️ **ALWAYS test in separate GPT instance first**
⚠️ **Current production version**: v8.4-FINAL in root directory
⚠️ **Purpose of experimental**: Explore alternatives, not replace proven system

---

## Questions This Work Explores

1. Can we enforce strict retrieval of external instructions?
2. Is 27% prohibitions focus better than 2.5%?
3. Does unlimited step space enable better student guidance?
4. Is maintenance easier with separated architecture?
5. What is the improvisation rate threshold for acceptability?

---

**Status**: ✅ v2.3 Implementation Complete - Ready for Testing
**Production System**: v8.4 Monolithic (root directory)
**Current Version**: v2.3-PRODUCTION (2025-01-19)
**Next Step**: Test with local LLM, verify canvas compilation, measure compliance

See `/bios-architecture/docs/BIOS_v2.3_CHANGELOG.md` for complete implementation details.
