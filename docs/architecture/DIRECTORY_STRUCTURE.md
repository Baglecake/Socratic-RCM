# Socratic-RCM Directory Structure

**Last Updated**: 2025-01-18

---

## Root Directory - Production Files Only

```
/Socratic-RCM/
├── CURRENT_VERSION_README.md           ← Start here for deployment
├── README.md                            ← Project overview
├── DIRECTORY_STRUCTURE.md              ← This file
│
├── B42 Chatstorm TA System Prompt v8.4-FINAL.txt    ← Upload to GPT Builder
├── B42 Chatstorm T.A. Guide v4.2.txt                ← KB[1]
├── B42 Final Project.txt                             ← KB[2]
├── B42 Step-by-Step Guide to Your Final Project.txt ← KB[3]
├── Appendix A - Required Values Index v3.2.txt      ← KB[4]
│
├── b42_theory_library/                  ← [B42-Pedagogy] Theory texts for student exercises
│   ├── marx_theory.txt                  ← KB[5]
│   ├── tocqueville_theory.txt           ← KB[6]
│   ├── wollstonecraft_theory.txt        ← KB[7]
│   └── smith_theory.txt                 ← KB[8]
│
├── EMPIRICAL_VALIDATION_PROTOCOL.md     ← Research methodology
├── PAPER_INTEGRATION_COMPLETE.md        ← Paper enhancement summary
├── PROCESS_CORPUS_CONSTRUCTION_TOOLKIT.md  ← Toolkit documentation
│
└── archive/
    ├── v7_era/
    │   ├── README.md
    │   ├── B42 Chatstorm TA System Prompt v7.2-FINAL.txt
    │   └── B42 Chatstorm TA System Prompt v7.3-FINAL.txt
    │
    ├── v8_development/
    │   ├── README.md
    │   ├── B42 Chatstorm TA System Prompt v8.0-THEORY-INTEGRATION.txt
    │   ├── B42 Chatstorm TA System Prompt v8.1-RESTORED.txt
    │   ├── B42 Chatstorm TA System Prompt v8.2-FINAL.txt
    │   ├── B42 Chatstorm TA System Prompt v8.3-FINAL.txt
    │   ├── V8_AUDIT_REPORT.md
    │   ├── V8.1_FINAL_AUDIT.md
    │   ├── V8.1_RESTORATION_SUMMARY.md
    │   ├── SURGICAL_CUTS_ANALYSIS.md
    │   ├── V8.2_SURGICAL_CUTS_SUMMARY.md
    │   ├── V8.3_CHANGE_SUMMARY.md
    │   ├── V8.4_CHANGE_SUMMARY.md
    │   ├── KB1_ANALYST_FIX.md
    │   ├── SYSTEM_PROMPT_v8.0_CHANGELOG.md
    │   ├── V8_DEPLOYMENT_SUMMARY.md
    │   ├── V7_vs_V8_COMPARISON.md
    │   └── V4.2_DEPLOYMENT_READY.txt
    │
    ├── documentation/
    │   ├── CHANGELOG_v4.2_to_v4.3.txt
    │   └── ENHANCEMENT_PACKAGE_SUMMARY.md
    │
    ├── v3_era/
    ├── v4_era/
    └── v4.1_era/
```

---

## Quick Reference

### For Deployment
→ See **[CURRENT_VERSION_README.md](CURRENT_VERSION_README.md)**

### For Development History
→ See **[archive/v8_development/README.md](archive/v8_development/README.md)**

### For Research Methodology
→ See **[EMPIRICAL_VALIDATION_PROTOCOL.md](EMPIRICAL_VALIDATION_PROTOCOL.md)**

---

## File Counts

| Directory | Files |
|-----------|-------|
| Root (production) | 9 core files |
| b42_theory_library/ | [B42-Pedagogy] 4 lecture note files for student exercises |
| archive/v7_era/ | 2 system prompts + README |
| archive/v8_development/ | 4 system prompts + 11 docs + README |
| archive/documentation/ | Legacy enhancement docs |
| archive/v3_era/ | Historical v3 files |
| archive/v4_era/ | Historical v4 files |
| archive/v4.1_era/ | Historical v4.1 files |

---

**Principle**: Root directory contains ONLY current production files and essential documentation.
All historical versions and development artifacts are in `/archive/`.

## Experimental Directory

```
/experimental/
└── bios-architecture/
    ├── README.md                                ← Architecture overview
    ├── B42_BIOS_System_Prompt_v1.0.txt         ← Minimal system prompt (~1,500 bytes)
    ├── B42_Runtime_Logic_v1.0.txt              ← Unlimited step instructions
    ├── BIOS_vs_MONOLITHIC.md                   ← Feature comparison
    └── FORCE_READ_PROTOCOL.md                  ← Testing strategy
```

**Purpose**: Explore alternative "BIOS + Runtime" architecture
- System prompt = BIOS (prime directives only, ~1,500 bytes)
- Runtime file = OS (all steps, unlimited size)
- Status: 🧪 Experimental, not production-ready

**Key Benefit**: Unlimited scalability (can add 100+ steps)
**Key Risk**: Lazy retrieval (GPT might improvise instead of reading file)

See **[experimental/README.md](experimental/README.md)** for full details.

---

**Updated**: 2025-01-18 (added experimental directory)
