# v7 Era Archive

This folder contains system prompt versions from the v7 iteration (November 2024).

---

## System Prompt Versions

### B42 Chatstorm TA System Prompt v7.2-FINAL.txt
- Pre-theory integration version
- Production version before v7.3

### B42 Chatstorm TA System Prompt v7.3-FINAL.txt
- **Date**: November 2024
- **Size**: 7,976 bytes
- **Status**: Final production version before v8 series
- **Features**:
  - Complete Socratic workflow (Phases 1-3)
  - RCM (Reflect-Connect-Ask) method
  - One-question-at-a-time enforcement
  - All critical navigation markers
  - Advanced functions (≥2 required)
  - Sequential processing
  - Checkpoint enforcement

---

## Why v7.3 is Important

v7.3-FINAL served as the **baseline** for v8 development. All v8 versions were audited against v7.3 to ensure:

1. ✅ No loss of critical features
2. ✅ Preservation of Socratic method
3. ✅ Maintained one-question-at-a-time rule
4. ✅ All checkpoints intact
5. ✅ Navigation markers preserved

---

## What Was Added in v8

v8.0 added theory integration (KB[5-8]) on top of v7.3's foundation:
- KB[5]: marx_theory.txt
- KB[6]: tocqueville_theory.txt
- KB[7]: wollstonecraft_theory.txt
- KB[8]: smith_theory.txt

Plus theory query protocol:
```
Theory Q? → KB[5-8] ONLY. Cite: "Per lecture..." Connect to project. NEVER training data.
```

---

## Character Budget

| Version | Bytes | Remaining (of 8,000) |
|---------|-------|----------------------|
| v7.2 | ~7,950 | ~50 |
| v7.3 | 7,976 | 24 |

---

## Superseded By

These files are superseded by:
- **[B42 Chatstorm TA System Prompt v8.4-FINAL.txt](../../B42 Chatstorm TA System Prompt v8.4-FINAL.txt)** (current production)

v8.4 includes all v7.3 features PLUS:
- Theory integration (KB[5-8])
- Reasoning acknowledgment
- Analyst requirement enforcement

---

**Archived**: 2025-01-18
**Production Period**: November 2024 - January 2025
**Replaced By**: v8 series
