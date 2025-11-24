# v8.4 Deployment Checklist

**Version**: v8.4-FINAL
**Date**: 2025-01-18
**Status**: Ready for Production

---

## Pre-Deployment Verification

- [x] System prompt at 8,000 bytes (exactly at limit)
- [x] KB[1] Guide updated with Analyst requirement
- [x] All theory files present in `/b42_theory_library/` folder
- [x] Legacy versions archived
- [x] Documentation complete

---

## GPT Builder Upload Steps

### Step 1: System Prompt
1. Open [B42 Chatstorm TA System Prompt v8.4-FINAL.txt](B42 Chatstorm TA System Prompt v8.4-FINAL.txt)
2. Copy entire contents (Cmd+A, Cmd+C)
3. Go to GPT Builder → Instructions field
4. Paste contents
5. Verify character count shows ~8,000 bytes

### Step 2: Knowledge Base Files (Upload in this order)

#### Core Workflow Files
- [ ] Upload `B42 Chatstorm T.A. Guide v4.2.txt` → KB[1]
- [ ] Upload `B42 Final Project.txt` → KB[2]
- [ ] Upload `B42 Step-by-Step Guide to Your Final Project.txt` → KB[3]
- [ ] Upload `Appendix A - Required Values Index v3.2.txt` → KB[4]

#### Theory Lecture Notes
- [ ] Upload `b42_theory_library/marx_theory.txt` → KB[5]
- [ ] Upload `b42_theory_library/tocqueville_theory.txt` → KB[6]
- [ ] Upload `b42_theory_library/wollstonecraft_theory.txt` → KB[7]
- [ ] Upload `b42_theory_library/smith_theory.txt` → KB[8]

**Total files**: 9 (1 system prompt + 8 knowledge base files)

---

## Post-Deployment Testing

### Test 1: Theory Query
**Prompt**: "Can you explain Marx's concept of alienation?"

**Expected Behavior**:
- ✅ GPT responds with "Per lecture..." citation
- ✅ Content matches KB[5] (marx_theory.txt)
- ✅ Does NOT use general training data

### Test 2: Analyst Requirement
**Prompt**: Start a project, select 2 advanced functions (e.g., Moderator + Self-Reflections)

**Expected Behavior**:
- ✅ GPT confirms ≥2 requirement met
- ✅ GPT states Analyst is **required** for final summary round
- ✅ GPT does NOT say "optional"

### Test 3: Reasoning Acknowledgment
**Prompt**: At step 1.2.5, provide complete answer with detailed reasoning about design choice

**Expected Behavior**:
- ✅ GPT acknowledges reasoning
- ✅ GPT proceeds to 1.2.6 immediately
- ✅ GPT does NOT ask for explanation again

### Test 4: Sequential Processing
**Prompt**: Start Phase 1

**Expected Behavior**:
- ✅ GPT asks ONE question at a time
- ✅ GPT waits for answer before next question
- ✅ GPT uses RCM (Reflect-Connect-Ask) format

### Test 5: One-Question-at-a-Time
**Prompt**: Any step in workflow

**Expected Behavior**:
- ✅ GPT never batches multiple questions
- ✅ Each question individually numbered (e.g., "1.2.3")
- ✅ Acknowledgment before next question

---

## Verification Checklist

### System Prompt Loaded Correctly
- [ ] Instructions field shows full v8.4 content
- [ ] Character count ~8,000 bytes
- [ ] No truncation errors

### Knowledge Base Files Loaded
- [ ] All 8 files visible in Files section
- [ ] File names match exactly
- [ ] No upload errors

### Core Features Working
- [ ] Theory queries route to KB[5-8]
- [ ] Analyst marked as required
- [ ] Reasoning acknowledgment working
- [ ] One-question-at-a-time enforced
- [ ] Checkpoints display correctly

---

## Rollback Plan (If Needed)

If v8.4 has issues, revert to v8.3:

1. System Prompt: Use `archive/v8_development/B42 Chatstorm TA System Prompt v8.3-FINAL.txt`
2. KB[1]: Revert `B42 Chatstorm T.A. Guide v4.2.txt` to version with "OPTIONAL" (git revert if tracked)

**Known Issue with v8.3**: Analyst will be treated as optional (this is why we upgraded to v8.4)

---

## Common Issues & Solutions

### Issue: GPT says Analyst is optional
**Cause**: KB[1] not uploaded or old version used
**Solution**: Re-upload `B42 Chatstorm T.A. Guide v4.2.txt` (modified version with "REQUIRED")

### Issue: GPT asks same question twice
**Cause**: System prompt v8.2 or earlier
**Solution**: Verify v8.4 system prompt loaded (check Line 62)

### Issue: Theory queries use general knowledge
**Cause**: Theory files not uploaded or not retrievable
**Solution**: Re-upload all 4 theory files from `/b42_theory_library/` folder

### Issue: GPT batches multiple questions
**Cause**: "—wait between each" marker missing
**Solution**: Verify v8.4 system prompt (Line 47)

---

## Success Criteria

Deployment is successful when:

1. ✅ All 5 tests pass
2. ✅ No error messages in GPT Builder
3. ✅ Student workflow proceeds smoothly through Phase 1
4. ✅ Analyst is consistently required
5. ✅ Theory citations use "Per lecture..." format

---

## Support Resources

### Documentation
- [CURRENT_VERSION_README.md](CURRENT_VERSION_README.md) - Overview and features
- [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - File organization
- [archive/v8_development/README.md](archive/v8_development/README.md) - Development history

### Version History
- See `/archive/v8_development/` for all v8 iterations
- See `/archive/v7_era/` for baseline v7.3

### Key Changes from v7.3
- Theory integration (KB[5-8])
- Reasoning acknowledgment (Line 62)
- Analyst requirement (Line 124 + KB[1])

---

## Post-Deployment

After successful deployment:

- [ ] Test with real student scenario
- [ ] Monitor for unexpected behaviors
- [ ] Document any issues in GitHub repo
- [ ] Update this checklist if needed

---

**Deployment Date**: _____________
**Deployed By**: _____________
**GPT Builder URL**: _____________
**Status**: [ ] Success  [ ] Issues (describe below)

**Notes**:
