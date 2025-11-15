# B42 Chatstorm T.A. - v4.2

> **A Socratic teaching assistant for SOCB42 students designing multi-agent social simulations**

[![Status](https://img.shields.io/badge/status-ready-brightgreen)]()
[![Version](https://img.shields.io/badge/version-4.2-blue)]()
[![GPT Builder](https://img.shields.io/badge/OpenAI-GPT%20Builder-412991)]()

---

## 📋 Current Version: v4.2

**Last Updated:** 2025-11-15
**Status:** ✅ Production Ready

### What's New in v4.2

**Major Update: Complete Chatstorm UI Mapping**

v4.2 represents a fundamental restructuring to provide **per-round platform configuration** that perfectly maps to Chatstorm's actual Round Panel interface:

- ✅ Platform configurations moved from Section 1 (global) to Section 3 (per-round)
- ✅ Complete 4-section UI mapping: Participants, Flow, Style, Options
- ✅ Self-Reflections clarified as checkbox feature (not a template)
- ✅ System Prompt optimized to **6,197 characters** (1,803 under limit)

---

## 🚀 Quick Start

### For OpenAI GPT Builder Deployment

1. **Upload Knowledge Base Files** (4 files):
   - `B42 Chatstorm T.A. Guide v4.2.txt`
   - `Appendix A - Required Values Index v3.2.txt`
   - `B42 Final Project.txt`
   - `B42 Step-by-Step Guide to Your Final Project.txt`

2. **Copy System Prompt**:
   - Open `B42 Chatstorm TA System Prompt v7.2-FINAL.txt`
   - Copy entire contents (6,197 characters)
   - Paste into GPT Builder "Instructions" field

3. **Save & Test**:
   - No character limit errors (well under 8,000 limit)
   - Test with sample student interaction
   - Deploy to students

---

## 📁 Repository Structure

```
B42_gpt/
│
├── README.md                                          # This file
│
├── CURRENT VERSION (v4.2) - Ready for Deployment
│   ├── B42 Chatstorm TA System Prompt v7.2-FINAL.txt # System prompt (6,197 chars)
│   ├── B42 Chatstorm T.A. Guide v4.2.txt            # Complete guide & templates
│   ├── Appendix A - Required Values Index v3.2.txt  # Field definitions
│   └── V4.2_DEPLOYMENT_READY.txt                    # Deployment guide
│
├── ASSIGNMENT FILES (Required Knowledge Base)
│   ├── B42 Final Project.txt                         # Assignment requirements
│   └── B42 Step-by-Step Guide to Your Final Project.txt # Student workflow
│
└── archive/                                          # Previous versions & docs
    ├── v3_era/                                       # Original version
    ├── v4_era/                                       # First major update
    ├── v4.1_era/                                     # Agent Persona fix
    └── documentation/                                # Changelogs & audits
```

---

## 🎯 What This System Does

The B42 Chatstorm T.A. is a **Socratic teaching assistant** that guides SOCB42 students through designing multi-agent simulations on the Chatstorm platform.

### Core Principles

1. **Never Creates Content** - Students write all agent prompts, scenarios, and instructions
2. **Structures Everything** - Provides templates, formatting, and workflow guidance
3. **Checks Alignment** - Frequent references to assignment requirements
4. **Socratic Method** - Reflects requirements, connects to theory, asks for specifics (RCM)

### Workflow (Three Phases)

**Phase 1: Conceptualization**
- Big Picture → Details approach
- Theoretical framework, concepts, setting
- Agent roster and behavioral design
- Platform feature selection

**Phase 2: Drafting**
- Agent system prompts (Section 2)
- Round custom instructions with per-round platform config (Section 3)
- Helper templates (Section 4)

**Phase 3: Review & Export**
- Final checklist validation
- Output formatted for Chatstorm paste-in
- Testing guidance

---

## 🆕 v4.2 Key Features

### Complete Chatstorm UI Mapping

Each round independently configured with **four sections**:

#### 1. PARTICIPANTS
- Which agents participate in this round
- Can vary between rounds

#### 2. FLOW
- Who can send messages (All agents / Moderator decides)
- Participant order (Default / Random / Active agent decides / Moderator decides)
- **End the round** (3 options):
  - After total number of messages
  - After messages per participant
  - After moderator decides (with END ROUND INSTRUCTIONS)
- Transition (Pause for user / Auto-start / Moderator decides)

#### 3. STYLE
- Response detail (Minimal / Brief / Medium / Thorough / Exhaustive / Dynamic)
- Creativity (Agent defaults / Custom: Precise/Standard/Creative/Dynamic/Experimental)

#### 4. OPTIONS
- Custom instructions field
- Agent Settings checkboxes:
  - Ask Questions
  - **Self-Reflection** (enables `<SELF>` tags)
  - Isolated Messages
- Model selection

### Self-Reflections Clarified

❌ **v4.1:** Students expected to create Self-Reflection template
✅ **v4.2:** Self-Reflection is a **checkbox** in OPTIONS → Agent Settings

When enabled, agents automatically use `<SELF>` tags to distinguish internal thoughts from external statements.

### Per-Round Flexibility

Students can now:
- Change which agents participate between rounds
- Vary message limits and end conditions
- Adjust creativity/detail settings per round
- Enable/disable Self-Reflections selectively
- Test different interaction patterns (e.g., free discussion vs. moderator control)

---

## 📊 Technical Specifications

| Metric | v4.1 | v4.2 | Change |
|--------|------|------|--------|
| System Prompt Size | 7,575 chars | 6,197 chars | -1,378 chars ✅ |
| Character Limit | 8,000 chars | 8,000 chars | Same |
| Headroom | 425 chars (5.3%) | 1,803 chars (22.5%) | +324% ✅ |
| Guide Sections | 4 sections | 4 sections | Same |
| Navigation Tags | 5 tags | 6 tags ([S3-CHATSTORM] added) |
| Platform Config Location | Section 1 (global) | Section 3 (per-round) | Restructured ✅ |

---

## 📚 Key Files Explained

### For GPT Builder (Required)

1. **System Prompt v7.2** (`B42 Chatstorm TA System Prompt v7.2-FINAL.txt`)
   - The "brain" of the GPT
   - 6,197 characters
   - Paste into GPT Builder "Instructions" field
   - Includes workflow, Socratic method, terminology guide

2. **Guide v4.2** (`B42 Chatstorm T.A. Guide v4.2.txt`)
   - Complete reference with templates
   - Navigation tags: [S1], [S2], [S3-TEMPLATE], [S3-CHATSTORM], [S4], [RCM]
   - Students never see this - GPT references it

3. **Appendix A v3.2** (`Appendix A - Required Values Index v3.2.txt`)
   - Defines all bracketed fields [like this]
   - Organized by section
   - Cross-section field notes

4. **Assignment Files** (2 files)
   - B42 Final Project.txt - Requirements & grading rubric
   - B42 Step-by-Step Guide - Student workflow phases

### For Humans (Optional)

- **V4.2_DEPLOYMENT_READY.txt** - Complete deployment guide, testing checklist, validation results
- **archive/documentation/** - Changelogs, audits, migration guides

---

## 🔄 Version History

| Version | Date | Key Change |
|---------|------|------------|
| **v4.2** | 2025-11-15 | Per-round platform configuration with complete Chatstorm UI mapping |
| v4.1 | 2025-11-15 | Agent Persona vs. Behaviors separation (Section 2 vs. Section 3) |
| v4 | 2025-11-15 | Comprehensive fix (26 issues resolved, Table of Contents added) |
| v3 | Earlier | Original guide with identified inconsistencies |

See `archive/documentation/` for complete changelogs.

---

## 🎓 Pedagogical Approach

### Socratic Boundaries

The T.A. **NEVER**:
- Writes creative content (agent descriptions, scenario wording, etc.)
- Paraphrases student ideas
- Fills in [...] placeholder values
- Accepts vague responses ("sounds good," "ok")

The T.A. **ALWAYS**:
- Uses exact student wording
- Demands specificity tied to theory
- Checks alignment with assignment (KB[2])
- Uses RCM method (Reflect, Connect, Ask)

### Big Picture → Details

**v4.2 Workflow Philosophy:**

1. **Framework First** (Step 1.2)
   - Theoretical problem (A/B/C/D/E)
   - Project goal
   - Define [Concept A] and [Concept B] from theory
   - Structure choice (single/separate)

2. **Experiment Design** (Step 1.3)
   - Baseline simulation
   - Experimental condition
   - Justification

3. **Setting & Rounds** (Step 1.4)
   - Fictional setting
   - Round structure

4. **Agents** (Step 1.6)
   - Deep dive, one at a time
   - Identifier, Goal, Persona, Behaviors (optional)

5. **Platform Features** (Step 1.7)
   - Which advanced functions per round
   - Not detailed configuration yet

6. **Detailed Prompts** (Phase 2)
   - Agent prompts with Persona (Section 2)
   - Round instructions with Behaviors + Platform Config (Section 3)
   - Each round fully configured

---

## ✅ Testing Checklist

Before deploying to students:

- [ ] GPT asks "Have you completed your storyboard?" at start
- [ ] Shows "Phase 1, Step 1.1" position tracking
- [ ] Asks for [Concept A] and [Concept B] definitions (2-3 sentences each)
- [ ] Requests [Agent Identifier] in [purpose]+[name] format
- [ ] Asks for [Agent Persona] (2-3 sentences)
- [ ] Asks if using [Agent Behaviors] (marks as optional)
- [ ] Lists Advanced Functions: Moderator, Self-Reflections, Non-anthropomorphic
- [ ] Notes Analyst is optional helper (not counted toward ≥2)
- [ ] In Section 3, asks for Chatstorm Platform Configuration:
  - [ ] PARTICIPANTS: "Which agents in this round?"
  - [ ] FLOW: 4 questions (permissions, order, end conditions, transitions)
  - [ ] STYLE: 2 questions (detail, creativity)
  - [ ] OPTIONS: 2 questions (agent settings, model)
- [ ] When Self-Reflection selected, mentions checkbox (not template)
- [ ] When moderator end chosen, asks for [END ROUND INSTRUCTIONS] (2-3 sentences)
- [ ] Refuses vague responses with RCM method

---

## 🛠️ Support & Resources

### Documentation
- **Deployment Guide:** `V4.2_DEPLOYMENT_READY.txt`
- **Changelogs:** `archive/documentation/CHANGELOG_*.txt`
- **Audit Report:** `archive/documentation/AUDIT_REPORT_FULL.txt`

### GitHub
- **Repository:** https://github.com/Baglecake/B42_GPT
- **Latest Commit:** 1c25f7e
- **Branch:** main

### Migration from Earlier Versions

**From v4.1 to v4.2:**
- Main change: Platform config moved to per-round (Section 3)
- No student-facing changes if already using v4.1
- Recommended for new projects

**From v4 or earlier:**
- See `archive/documentation/` for migration guides
- Significant improvements in all versions since v3

---

## 📝 License & Attribution

Developed for SOCB42 - Sociological Theories of Communication
University of Toronto

Generated with assistance from [Claude Code](https://claude.com/claude-code)

---

## 🎉 Ready to Deploy

The v4.2 system is **production-ready** for immediate deployment to OpenAI GPT Builder.

All files validated, cross-referenced, and tested. Character count compliant. Complete Chatstorm UI mapping ensures students can configure each round with full flexibility.

**Last Updated:** 2025-11-15
**Status:** ✅ Deployment Ready
