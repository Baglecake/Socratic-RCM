# Experimental Architectures

**Purpose**: Explore alternative approaches to the B42 Chatstorm T.A. system

---

## Current Structure

### `/experimental/bios-architecture/`
**BIOS + Runtime Logic Architecture** 🧪

A fundamentally different approach that separates:
- **BIOS System Prompt** (~1,500 bytes): Prime directives + execution loop
- **Runtime Logic File** (unlimited): All step-by-step instructions

**Status**: Experimental design phase
**Concept Source**: Gemini architectural analysis
**Key Innovation**: Moves from "cramming everything into prompt" to "strict execution of external instructions"

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

**After (BIOS v1.0)**:
- FILE 1: 1,500 byte BIOS (prime directives only)
- FILE 2: Unlimited runtime logic (ALL steps, unlimited size)
- Benefit: Can add 100+ steps without touching system prompt

---

## Files in `/bios-architecture/`

### Core Architecture
1. **`B42_BIOS_System_Prompt_v1.0.txt`**
   - Minimal system prompt (~1,500 bytes)
   - Prime directives + execution loop
   - Force-read protocol

2. **`B42_Runtime_Logic_v1.0.txt`**
   - Step-by-step instructions in standardized format
   - Each step: TARGET, INSTRUCTION, REQUIRED OUTPUT, RCM CUE, CONSTRAINT
   - Currently: 13 steps (demo), will expand to 100+

### Documentation
3. **`README.md`** - Architecture overview and development status
4. **`BIOS_vs_MONOLITHIC.md`** - Side-by-side comparison
5. **`FORCE_READ_PROTOCOL.md`** - How to prevent lazy retrieval
6. **`ARCHITECTURE_DESIGN.md`** - (planned) Detailed design doc
7. **`MIGRATION_GUIDE.md`** - (planned) How to convert v8.4 → BIOS
8. **`TESTING_PROTOCOL.md`** - (planned) Testing procedures

---

## Key Advantages of BIOS

✅ **Unlimited Scalability**: Can add 50+ steps without character limit
✅ **Easier Maintenance**: Edit text file, don't touch system prompt
✅ **Prohibitions Focus**: 27% of prompt vs 2.5% in monolithic
✅ **Lower Update Risk**: BIOS unchanged, edit runtime safely
✅ **Future-Proof**: Can grow to 100K+ bytes if needed

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

| Feature | Monolithic v8.4 | BIOS v1.0 |
|---------|-----------------|-----------|
| Character Limit | 8,000 bytes (maxed) | 1,500 + unlimited |
| Prohibitions Focus | 2.5% of prompt | 27% of prompt |
| Scalability | Cannot add features | Can add 100+ steps |
| Maintenance | Edit full prompt | Edit text file |
| Lazy Retrieval Risk | None | Moderate (requires testing) |
| Production Status | ✅ Deployed | 🧪 Experimental |

---

## Development Phases

### Phase 1: Architecture Design ✅
- [x] Create experimental directory structure
- [x] Write BIOS system prompt v1.0
- [x] Create runtime logic format
- [x] Document force-read protocol
- [x] Create comparison analysis

### Phase 2: Implementation 🚧
- [ ] Convert all v8.4 steps to runtime format
- [ ] Complete runtime logic file (100+ steps)
- [ ] Write migration guide
- [ ] Create testing scripts

### Phase 3: Testing 📋
- [ ] Automated force-read compliance testing
- [ ] Volunteer student testing
- [ ] Compare strictness to v8.4
- [ ] Measure exact match rates

### Phase 4: Evaluation 📊
- [ ] Analyze test results
- [ ] Calculate metrics (exact match rate, improvisation rate)
- [ ] Production readiness assessment
- [ ] Decision: Deploy, Iterate, or Archive

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

**Status**: 🧪 Experimental design complete, implementation in progress
**Production System**: v8.4 Monolithic (root directory)
**Next Step**: Complete runtime file conversion, begin force-read testing

See `/bios-architecture/README.md` for detailed status and next actions.
