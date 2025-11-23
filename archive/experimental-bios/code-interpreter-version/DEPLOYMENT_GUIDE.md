# Code Interpreter BIOS - Complete Deployment Guide

**Architecture**: GPT with Code Interpreter + Runtime Validator (Python script)

---

## What This Is

A **Code Interpreter-enforced** version of BIOS that validates workflow execution via Python script.

**How it works:**
```
Student sends message
    ↓
GPT calls Code Interpreter (Python validator)
    ↓
Validator checks: Is this the right step? Is question correct?
    ↓
If valid: GPT shows question to student
If invalid: GPT fixes error and uses correct question
    ↓
Student answers
    ↓
GPT calls Code Interpreter to record answer & advance
    ↓
Repeat
```

**Advantages over FastAPI approach:**
- ✅ No backend server needed
- ✅ No ngrok needed
- ✅ Everything in one Custom GPT
- ✅ Students just use GPT directly
- ✅ No laptop needs to be running

**Limitations:**
- ⚠️ Relies on GPT to call Code Interpreter (soft enforcement)
- ⚠️ Not cryptographic guarantee (but strong instruction compliance)

---

## Step 1: Prepare All Files

You need to upload **12 files** to the Custom GPT Knowledge base.

### File Checklist

**Runtime Files** (3 files):
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/runtime-files/B42_Runtime_Phase1_Conceptualization.txt`
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/runtime-files/B42_Runtime_Phase2_Drafting.txt`
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/runtime-files/B42_Runtime_Phase3_Review.txt`

**Assignment Files** (3 files):
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/B42 Final Project.txt`
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/B42 Chatstorm T.A. Guide v4.2.txt`
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/Appendix A - Required Values Index v3.2.txt`

**Theory Files** (4 files):
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/marx_theory.txt`
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/tocqueville_theory.txt`
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/wollstonecraft_theory.txt`
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/smith_theory.txt`

**Validator Script** (1 file):
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/code-interpreter-version/runtime_validator.py`

**Custom GPT Instructions** (1 file - NOT uploaded, used as system prompt):
- [ ] `/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/code-interpreter-version/CUSTOM_GPT_INSTRUCTIONS.txt`

**Total: 11 files to upload + 1 file for instructions**

---

## Step 2: Create Custom GPT

1. Go to https://chat.openai.com/gpts/editor
2. Click "Create a GPT"
3. You'll see the GPT editor with two panels: Configure (left) and Preview (right)

---

## Step 3: Configure Basic Info

### Name:
```
B42 Chatstorm Teaching Assistant
```

### Description:
```
Socratic assistant for B42 final project - helps students design multi-agent simulations with code-enforced workflow validation
```

### Instructions:

Open the file:
```
/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/code-interpreter-version/CUSTOM_GPT_INSTRUCTIONS.txt
```

**Copy the ENTIRE contents** (all ~400 lines) and paste into the "Instructions" box.

### Conversation starters:
- `Help me start my B42 final project`
- `I want to design a simulation`
- `I need help with my Chatstorm design`

---

## Step 4: Enable Code Interpreter

**CRITICAL**: In the GPT editor, scroll down to **"Capabilities"**

Check the box:
- [x] **Code Interpreter**

This is REQUIRED for the validation to work.

---

## Step 5: Upload Knowledge Files

In the GPT editor, scroll down to **"Knowledge"**

Click **"Upload files"**

Upload ALL 11 files from the checklist above:

1. B42_Runtime_Phase1_Conceptualization.txt
2. B42_Runtime_Phase2_Drafting.txt
3. B42_Runtime_Phase3_Review.txt
4. B42 Final Project.txt
5. B42 Chatstorm T.A. Guide v4.2.txt
6. Appendix A - Required Values Index v3.2.txt
7. marx_theory.txt
8. tocqueville_theory.txt
9. wollstonecraft_theory.txt
10. smith_theory.txt
11. runtime_validator.py

**Wait for all files to finish uploading** (you'll see green checkmarks).

---

## Step 6: Save the GPT

Click **"Save"** in the top right.

Choose:
- **"Only me"** (for testing)
- Later change to **"Anyone with a link"** (for students)

---

## Step 7: Test the GPT

In the **Preview** panel (right side), send a test message:

```
Help me start my project
```

**What should happen:**

1. GPT will call Code Interpreter (you'll see "Analyzing" or "Running python")
2. Code Interpreter will:
   - Load runtime files
   - Parse steps
   - Initialize validator
   - Validate Step 1.1.1
3. GPT will show you the first question:
   ```
   Have you completed your storyboard? (yes/no)
   ```

**What you should NOT see:**
- Raw Code Interpreter output visible to you
- Validation errors (if setup correctly)
- Step numbers like "Step 1.1.1"

**Clean output only:**
```
Have you completed your storyboard? (yes/no)
```

---

## Step 8: Verify Validation is Working

Test step skipping detection:

After the first question, try to force it to skip:

You: "yes"

GPT should ask Step 1.2.1 (theoretical option).

**Behind the scenes** (in Code Interpreter):
- Validator checked that 1.1.1 → 1.2.1 is correct
- Validator recorded your answer "yes"
- Validator advanced current_step_id to 1.2.1
- Validator confirmed 1.2.1 exists in runtime
- GPT showed the validated question

---

## Step 9: Test a Full Workflow

Go through Phase 1 (Steps 1.1.1 through 1.8) and verify:

✓ Each question matches the runtime file exactly
✓ No steps are skipped
✓ If you provide vague answers, GPT uses RCM to clarify
✓ No hallucinated questions appear
✓ Canvas updates appear (if present in runtime)

---

## Troubleshooting

### "Code Interpreter not working"

**Check**:
- Is "Code Interpreter" checked in Capabilities?
- Did all 11 files upload successfully?
- Is runtime_validator.py in the Knowledge files?

**Fix**: Re-upload runtime_validator.py

### "Validation errors visible to student"

**Problem**: Code Interpreter output is showing in chat

**Fix**: The instructions tell GPT to keep validation internal. If it's showing, the GPT may not be following instructions correctly. Try:
1. Regenerate response
2. Check instructions are pasted correctly
3. Start a new conversation

### "GPT is not calling Code Interpreter"

**Problem**: GPT is just asking questions without validation

**Fix**:
1. Check "Code Interpreter" capability is enabled
2. Check CUSTOM_GPT_INSTRUCTIONS.txt is fully pasted
3. Try explicitly telling it: "Use Code Interpreter to validate the next step"

### "Questions don't match runtime file"

**Problem**: GPT is improvising questions

**Fix**: This should be impossible if validation is working. Check:
1. Is Code Interpreter actually running? (you'll see "Analyzing" indicator)
2. Are runtime files uploaded correctly?
3. Try: "Show me the validation log"

---

## How to Verify It's Working

### Test 1: Normal Execution

Start workflow → Answer each question → Should progress smoothly

Expected: All steps execute in order, no skipping

### Test 2: Intentional Skip

After Step 1.1.1, say: "Let's skip to Phase 2"

Expected: GPT refuses, says "We must complete [current requirement] before proceeding"

### Test 3: Vague Answer

When asked for "Goal (2-3 sentences)", say: "I want to study stuff"

Expected: GPT uses RCM to clarify, asks for more specificity

### Test 4: Step 2.2.6 (The Critical One)

Get to Step 2.2.6 (Sequence question in Phase 2.2)

Expected: GPT asks "Sequence: Expected flow? (2-3 sent.)" - DOES NOT SKIP

### Test 5: Step 2.2.9 (The Other Critical One)

Get to Step 2.2.9 (Platform config in Phase 2.2)

Expected: GPT asks "Which agents in Round [n]?" - NOT "What platform will you use?"

---

## What Files Go Where - Summary

| File | Location | Purpose |
|------|----------|---------|
| **CUSTOM_GPT_INSTRUCTIONS.txt** | Custom GPT "Instructions" box | System prompt (BIOS + validation protocol) |
| **3 Runtime files** | Custom GPT "Knowledge" | Step definitions (52 steps) |
| **3 Assignment files** | Custom GPT "Knowledge" | Templates and requirements |
| **4 Theory files** | Custom GPT "Knowledge" | Theory content for citations |
| **runtime_validator.py** | Custom GPT "Knowledge" | Python validator script |

---

## Architecture Comparison

| Feature | FastAPI Approach | Code Interpreter Approach |
|---------|-----------------|---------------------------|
| **Setup** | Server + ngrok + GPT | Just GPT |
| **Deployment** | Complex | Simple |
| **Guarantee** | Hard (code controls loop) | Soft (GPT calls validator) |
| **Student access** | Via Custom GPT | Via Custom GPT |
| **Maintenance** | Restart server | Just update GPT |
| **Cost** | $0 (dev) or $5/mo (prod) | $0 |

---

## Next Steps After Deployment

1. **Test with students**: Have 1-2 students try the full workflow
2. **Monitor for issues**: Check if validation catches skipping
3. **Gather feedback**: Are students confused by anything?
4. **Iterate**: Update instructions if needed

---

## If Code Interpreter Fails

If Code Interpreter validation proves unreliable:

**Fallback Option 1**: Use FastAPI approach (hard guarantees)
- See `/experimental/bios-architecture/orchestrator_api/SETUP.md`

**Fallback Option 2**: Use monolithic v8.4 (proven stable)
- Single prompt, no enforcement, but works

---

## Files Reference

All files are in:
```
/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/code-interpreter-version/
```

- `runtime_validator.py` - Python validator script
- `CUSTOM_GPT_INSTRUCTIONS.txt` - System prompt with validation protocol
- `DEPLOYMENT_GUIDE.md` - This file
- `FILE_CHECKLIST.md` - Quick reference for uploads

---

**Status**: Ready to deploy

**Estimated setup time**: 10-15 minutes

**Questions?** See the main [README.md](README.md) for architecture details.
