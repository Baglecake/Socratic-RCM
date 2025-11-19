# BIOS + Runtime Architecture (Experimental)

**Status**: ⚠️ **Experimental - Not Production Ready**
**Created**: 2025-01-18
**Updated**: 2025-01-19 (v2.1 fixes applied, force-read issues persist)
**Concept Source**: Gemini architectural analysis

**Latest Version**: BIOS v2.1-PRODUCTION + Phase-Split Runtime Files
- ✅ User testing complete (5 UI issues fixed)
- ❌ Force-read reliability issues (step-skipping observed)
- ⚠️ Not recommended for student deployment

**Recommendation**: Use [production/](../../production/) v8.4 for student deployment.

See [docs/PRODUCTION_FIXES_v2.1.md](docs/PRODUCTION_FIXES_v2.1.md) for detailed testing feedback.

---

## Core Concept

Move from **"Monolithic Prompt"** to **"BIOS + OS"** architecture:

- **System Prompt** = BIOS (Basic Input/Output System)
  - Prime directives only
  - Prohibitions enforcement
  - Runtime loop protocol
  - ~1,000-2,000 bytes

- **Runtime Logic File** = Operating System
  - Every step's detailed instructions
  - Specific question phrasing
  - RCM cues per step
  - Unlimited size (can be 100+ pages)

---

## The Problem This Solves

### Current v8.4 Architecture (Monolithic)
```
System Prompt (8,000 bytes)
├── Identity (50 bytes)
├── Prohibitions (200 bytes)
├── Knowledge Base refs (300 bytes)
├── RCM Method (400 bytes)
├── Phase 1 (3,000 bytes) ← ALL SPECIFIC STEPS
├── Phase 2 (2,500 bytes) ← ALL SPECIFIC STEPS
└── Phase 3 (1,500 bytes) ← ALL SPECIFIC STEPS
```

**Issues**:
- ✅ High strictness (always in attention)
- ❌ Constant character limit pressure
- ❌ Hard to update (editing giant prompt is risky)
- ❌ Cannot add new features without compression

### BIOS Architecture (Proposed)
```
System Prompt "BIOS" (1,500 bytes)
├── Identity (50 bytes)
├── Prohibitions (400 bytes) ← ENHANCED, PRIMARY FOCUS
├── Runtime Loop Protocol (800 bytes) ← FORCE-READ MECHANISM
└── Error Handling (250 bytes)

Runtime Logic File (unlimited)
├── [STEP 1.1] Welcome
├── [STEP 1.2.1] Theoretical option
├── [STEP 1.2.2] Project goal
├── [STEP 1.2.3] Concept A
├── ... (100+ steps possible)
└── [STEP 3.X] Final review
```

**Benefits**:
- ✅ Prohibitions get 25% of prompt (not 5%)
- ✅ Unlimited detail in runtime file
- ✅ Easy updates (edit text file only)
- ✅ Scalable (add 50 more steps without touching prompt)

**Risk**:
- ❌ "Lazy Retrieval" - LLM might guess instead of reading file
- 🛡️ **Mitigation**: Force-Read Protocol (RETRIEVE → READ → EXECUTE loop)

---

## Comparison Matrix

| Feature | Monolithic (v8.4) | BIOS + Runtime |
|---------|-------------------|----------------|
| **Space Constraint** | 8,000 byte hard limit | Unlimited runtime file |
| **Strictness** | High (always loaded) | Variable (must force retrieval) |
| **Updates** | Risky (full prompt edit) | Easy (edit text file) |
| **Scalability** | Cannot add features | Can add 100+ steps |
| **Risk** | Context window overflow | Lazy retrieval |
| **Prohibitions Focus** | 5% of prompt | 25% of prompt |
| **Deployment** | 1 file upload | 2 files upload |

---

## The Force-Read Protocol

The key to preventing lazy retrieval is mandating a strict execution loop:

```
RUNTIME LOOP (Mandatory Protocol)
For every single turn:

1. LOCATE: Determine current Phase/Step (e.g., "1.2.2")
2. RETRIEVE: Search B42_Runtime_Logic.txt for [STEP X.Y.Z]
3. READ: Read INSTRUCTION, REQUIRED OUTPUT, RCM CUE
4. THEORY CHECK: If theory needed, search KB[5-8]
5. EXECUTE: Output exact question from logic file
```

This forces the LLM to **quote the step internally** before executing, reducing hallucination risk.

---

## Files in This Directory

### Core Architecture Files
- **`B42_BIOS_System_Prompt_v1.0.txt`** - Minimal system prompt (~1,500 bytes)
- **`B42_Runtime_Logic_v1.0.txt`** - Complete step-by-step instructions (unlimited)

### Documentation
- **`ARCHITECTURE_DESIGN.md`** - Detailed design rationale
- **`FORCE_READ_PROTOCOL.md`** - How to prevent lazy retrieval
- **`MIGRATION_GUIDE.md`** - How to convert v8.4 → BIOS
- **`TESTING_PROTOCOL.md`** - How to verify force-read is working

### Comparison
- **`BIOS_vs_MONOLITHIC.md`** - Side-by-side feature comparison
- **`RISK_ANALYSIS.md`** - Lazy retrieval mitigation strategies

---

## When to Use This Architecture

### Use BIOS Architecture If:
- ✅ You need to add many more steps (e.g., pre-submission checklist)
- ✅ Character limit is blocking critical features
- ✅ You want easier maintenance (edit text file vs. full prompt)
- ✅ You can test force-read protocol thoroughly

### Stick with Monolithic (v8.4) If:
- ✅ Current features fit within 8,000 bytes
- ✅ Proven stability is critical (production environment)
- ✅ You prefer instructions always in attention
- ✅ Lazy retrieval risk is unacceptable

---

## Development Status

### Phase 1: Architecture Design ✅
- [x] Create experimental directory structure
- [x] Document BIOS concept
- [x] Identify force-read protocol requirements

### Phase 2: Implementation ✅
- [x] Write BIOS system prompt v1.0
- [x] Convert v8.4 steps to runtime logic file (100% complete)
- [x] Implement force-read protocol
- [x] Create step templates
- [x] Split into phase-specific files (v2.0)
- [x] Fix production issues from testing (v2.1)

### Phase 3: Testing ✅
- [x] Test lazy retrieval scenarios (KB retrieval failure identified, fixed with split)
- [x] Verify force-read enforcement (theory queries working)
- [x] User testing with v2.0 (5 issues identified)
- [x] Apply fixes for v2.1 (all issues resolved)

### Phase 4: Evaluation ⚠️
- [x] Production readiness assessment (Not Ready - force-read issues)
- [x] Full Phase 1 workflow test with v2.1 (step-skipping observed)
- [ ] Force-read reliability improvements needed
- [ ] Additional testing after fixes
- [ ] **Decision**: Continue v8.4 for production, iterate BIOS for research

---

## Key Insight from Gemini

> "Think of the System Prompt not as the 'Teacher,' but as the BIOS of a computer. Its only job is to boot the system, enforce hardware safety limits (your prohibitions), and tell the processor where to find the Operating System (your Step-by-Step guide)."

This shifts focus from **"cramming everything into the prompt"** to **"enforcing strict execution of external instructions."**

---

## Version History

### v2.1-PRODUCTION (2025-01-19) ✅ Current
**Status**: Production ready for deployment

**Fixes from user testing**:
- Fixed Step 1.7 wording (removed "KB[2]" jargon)
- Added prohibition #6: NO RUNTIME DISPLAY
- Added RCM ENFORCEMENT section (show Socratic guidance)
- Added STUDENT-FACING OUTPUT FORMAT examples
- Modified execution loop to be silent (no debugging shown)

**Files**: `B42_BIOS_System_Prompt_v2.1-PRODUCTION.txt`

See: [PRODUCTION_FIXES_v2.1.md](PRODUCTION_FIXES_v2.1.md)

### v2.0-SPLIT (2025-01-18)
**Status**: Tested, issues identified

**Changes**:
- Split 30KB runtime into 3 phase files (2-19KB each)
- Added phase detection logic to BIOS
- Fixed KB retrieval reliability

**Files**: `B42_BIOS_System_Prompt_v2.0-SPLIT.txt`

See: [SPLIT_ARCHITECTURE.md](SPLIT_ARCHITECTURE.md)

### v1.0 (2025-01-18)
**Status**: Experimental, retrieval issues

**Changes**:
- Initial BIOS architecture
- Single 30KB runtime file (caused retrieval failures)
- Force-read protocol implemented

**Files**: `B42_BIOS_System_Prompt_v1.0.txt`

See: [CONVERSION_COMPLETE.md](CONVERSION_COMPLETE.md)

---

## Next Steps

1. ✅ **Deploy v2.1**: Upload to test GPT instance
2. **Full Workflow Test**: Run complete Phase 1 with student
3. **Verification**: Confirm no runtime info visible, RCM shown
4. **Comparison Test**: Run same scenario through v8.4 and v2.1
5. **Student Feedback**: Collect reactions to strictness and clarity
6. **Decision**: Deploy to production or iterate further

---

**Current Status**: ⚠️ **Experimental - Research Branch**

**Issue**: Force-read protocol shows step-skipping failures. GPT jumps between phases and displays template placeholders instead of student data.

**Recommended Action**:
- Use [production/](../../production/) v8.4 for student deployment
- Continue BIOS development as research project for future scalability
- Focus on improving force-read reliability before production consideration
