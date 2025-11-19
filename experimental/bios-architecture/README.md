# BIOS + Runtime Architecture (Experimental)

**Status**: 🧪 Experimental Alternative to v8.4 Monolithic Prompt
**Created**: 2025-01-18
**Concept Source**: Gemini architectural analysis

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

### Phase 2: Implementation 🚧
- [ ] Write BIOS system prompt v1.0
- [ ] Convert v8.4 steps to runtime logic file
- [ ] Implement force-read protocol
- [ ] Create step templates

### Phase 3: Testing 📋
- [ ] Test lazy retrieval scenarios
- [ ] Verify force-read enforcement
- [ ] Compare strictness to v8.4
- [ ] Student workflow testing

### Phase 4: Evaluation 📊
- [ ] Performance metrics
- [ ] Maintenance comparison
- [ ] Production readiness assessment
- [ ] Decision: Deploy or Archive

---

## Key Insight from Gemini

> "Think of the System Prompt not as the 'Teacher,' but as the BIOS of a computer. Its only job is to boot the system, enforce hardware safety limits (your prohibitions), and tell the processor where to find the Operating System (your Step-by-Step guide)."

This shifts focus from **"cramming everything into the prompt"** to **"enforcing strict execution of external instructions."**

---

## Next Steps

1. **Design BIOS Prompt**: Write minimal system prompt with force-read loop
2. **Convert v8.4**: Transform current steps into runtime logic format
3. **Test Protocol**: Verify retrieval happens every turn
4. **A/B Compare**: Run parallel tests vs. v8.4

---

**Experimental Status**: Not production-ready
**Current Production**: v8.4 Monolithic (root directory)
**Purpose**: Explore architectural alternative for future scalability
