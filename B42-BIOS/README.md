# B42-BIOS - Complete Deployment Package

**All files needed for Code Interpreter BIOS deployment in one place**

---

## Directory Structure

```
B42-BIOS/
├── runtime-files/           (3 files) - Workflow step definitions
│   ├── B42_Runtime_Phase1_Conceptualization.txt
│   ├── B42_Runtime_Phase2_Drafting.txt
│   └── B42_Runtime_Phase3_Review.txt
│
├── assignment-files/        (3 files) - Templates and requirements
│   ├── B42 Final Project.txt
│   ├── B42 Chatstorm T.A. Guide v4.2.txt
│   └── Appendix A - Required Values Index v3.2.txt
│
├── theory-files/            (4 files) - Theory content
│   ├── marx_theory.txt
│   ├── tocqueville_theory.txt
│   ├── wollstonecraft_theory.txt
│   └── smith_theory.txt
│
├── validator/               (1 file) - Python validation script
│   └── runtime_validator.py
│
├── documentation/           (3 files) - Setup guides
│   ├── DEPLOYMENT_GUIDE.md
│   ├── FILE_CHECKLIST.md
│   └── README.md
│
├── CUSTOM_GPT_INSTRUCTIONS.txt  - System prompt (paste into GPT Instructions)
└── README.md                    - This file
```

**Total: 11 files to upload + 1 instructions file**

---

## Quick Deploy

### Step 1: Create Custom GPT

1. Go to https://chat.openai.com/gpts/editor
2. Click "Create a GPT"

### Step 2: Basic Configuration

- **Name**: B42 Chatstorm Teaching Assistant
- **Description**: Socratic assistant for B42 final project with code-enforced workflow

### Step 3: Paste Instructions

Open `CUSTOM_GPT_INSTRUCTIONS.txt` (in this directory)

Copy the ENTIRE contents and paste into the "Instructions" box

### Step 4: Enable Code Interpreter

Scroll down to "Capabilities"

Check: [x] **Code Interpreter** (REQUIRED)

### Step 5: Upload Knowledge Files

Click "Upload files" in the Knowledge section

Upload ALL these files (11 total):

**From runtime-files/ (3 files)**:
- B42_Runtime_Phase1_Conceptualization.txt
- B42_Runtime_Phase2_Drafting.txt
- B42_Runtime_Phase3_Review.txt

**From assignment-files/ (3 files)**:
- B42 Final Project.txt
- B42 Chatstorm T.A. Guide v4.2.txt
- Appendix A - Required Values Index v3.2.txt

**From theory-files/ (4 files)**:
- marx_theory.txt
- tocqueville_theory.txt
- wollstonecraft_theory.txt
- smith_theory.txt

**From validator/ (1 file)**:
- runtime_validator.py

### Step 6: Save & Test

- Click "Save"
- Choose "Only me" (for testing)
- Test: "Help me start my project"
- Expected: "Have you completed your storyboard? (yes/no)"

---

## What This Does

This BIOS uses **Code Interpreter to validate workflow execution**:

✅ **No step skipping** - Python validator checks every step advancement
✅ **No hallucinated questions** - Validator provides correct question text
✅ **All 52 steps guaranteed** - Validator enforces sequencing
✅ **Constraint checking** - Validates answer quality
✅ **Schema validation** - Checks canvas data structure at phase boundaries (NEW)
✅ **Progressive Canvas display** - Shows compiled sections to students after validation (NEW)
✅ **Full logging** - Tracks every step for debugging

---

## Files Explained

### runtime-files/ - The Workflow (52 steps)

Contains all workflow steps with:
- Required question text
- RCM cues
- Constraints
- Next step field

The validator reads these to enforce correct execution.

### assignment-files/ - Templates & Requirements

- **B42 Final Project.txt** - Assignment description
- **B42 Chatstorm T.A. Guide v4.2.txt** - Complete workflow templates (S1, S2, S3, S4)
- **Appendix A** - Field index for all required values

### theory-files/ - Theory Content

Lecture notes for Marx, Tocqueville, Wollstonecraft, Smith.

GPT cites these when students ask theory questions.

### validator/ - The Enforcement Code

**runtime_validator.py** - Python script that:
- Parses runtime files at startup
- Validates step before GPT shows question
- Checks question text matches runtime
- Records answers
- Controls step advancement
- **Validates canvas data structure against schema** (NEW)
- **Ensures complete data before phase transitions** (NEW)

This is what prevents skipping, hallucination, and incomplete data compilation.

### CUSTOM_GPT_INSTRUCTIONS.txt - System Prompt

The complete GPT instructions including:
- BIOS v2.3 identity and prohibitions
- **Mandatory Code Interpreter validation protocol**
- **Schema-validated Canvas compilation display** (NEW)
- **Progressive section display after each phase** (NEW)
- RCM philosophy
- Error handling

Paste this into the GPT "Instructions" box (do NOT upload to Knowledge).

---

## Documentation

See `documentation/` folder for:

- **DEPLOYMENT_GUIDE.md** - Detailed step-by-step setup
- **FILE_CHECKLIST.md** - Quick upload reference
- **README.md** - Architecture overview

---

## Testing Critical Steps

Once deployed, verify these work:

**Step 2.2.6 (Sequence)**:
- Must ask: "Sequence: Expected flow? (2-3 sent.)"
- Must NOT skip

**Step 2.2.9 (Platform Config)**:
- Must ask: "Which agents in Round [n]?"
- Must NOT ask: "What platform will you use?"

If both are correct → Validation is working!

---

## Troubleshooting

**"Code Interpreter not working"**
- Check "Code Interpreter" is enabled in Capabilities
- Check runtime_validator.py is uploaded

**"Questions don't match runtime"**
- Validator should catch this automatically
- Check all 3 runtime files are uploaded

**"Steps being skipped"**
- Should be impossible if validator is running
- Check Code Interpreter is actually being called

---

## Deployment Time

- **First time**: 10-15 minutes
- **Updates**: 2-3 minutes (just re-upload changed files)

---

## Support

- Full setup guide: `documentation/DEPLOYMENT_GUIDE.md`
- File checklist: `documentation/FILE_CHECKLIST.md`
- Architecture details: `documentation/README.md`

---

**Status**: ✅ Ready to deploy

**All files are in this directory - just upload to GPT!**
