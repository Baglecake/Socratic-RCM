# File Upload Checklist - Code Interpreter BIOS

## Files to Upload to Custom GPT Knowledge (11 total)

### Runtime Files (3 files)
- [ ] B42_Runtime_Phase1_Conceptualization.txt
- [ ] B42_Runtime_Phase2_Drafting.txt
- [ ] B42_Runtime_Phase3_Review.txt

### Assignment Files (3 files)
- [ ] B42 Final Project.txt
- [ ] B42 Chatstorm T.A. Guide v4.2.txt
- [ ] Appendix A - Required Values Index v3.2.txt

### Theory Files (4 files)
- [ ] marx_theory.txt
- [ ] tocqueville_theory.txt
- [ ] wollstonecraft_theory.txt
- [ ] smith_theory.txt

### Validator Script (1 file)
- [ ] runtime_validator.py

---

## File Paths

### Runtime Files
```
/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/runtime-files/B42_Runtime_Phase1_Conceptualization.txt
/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/runtime-files/B42_Runtime_Phase2_Drafting.txt
/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/runtime-files/B42_Runtime_Phase3_Review.txt
```

### Assignment Files
```
/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/B42 Final Project.txt
/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/B42 Chatstorm T.A. Guide v4.2.txt
/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/Appendix A - Required Values Index v3.2.txt
```

### Theory Files
```
/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/marx_theory.txt
/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/tocqueville_theory.txt
/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/wollstonecraft_theory.txt
/Users/delcoburn/Documents/GitHub/Socratic-RCM/production/knowledge-base/smith_theory.txt
```

### Validator Script
```
/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/code-interpreter-version/runtime_validator.py
```

---

## File for Instructions (NOT uploaded)

This goes in the Custom GPT "Instructions" box:
```
/Users/delcoburn/Documents/GitHub/Socratic-RCM/experimental/bios-architecture/code-interpreter-version/CUSTOM_GPT_INSTRUCTIONS.txt
```

**DO NOT upload to Knowledge** - Copy/paste into Instructions field instead.

---

## Verification

After uploading, you should see **11 files** in the Knowledge section of your GPT.

Missing files? Common issues:
- Forgot runtime_validator.py (CRITICAL - without this, validation won't work)
- Uploaded CUSTOM_GPT_INSTRUCTIONS.txt (should be in Instructions, not Knowledge)
- Theory files not found (check production/knowledge-base directory)

---

## Quick Upload Script (Terminal)

If you want to prepare files in one location:

```bash
# Create staging directory
mkdir -p ~/Desktop/bios-upload

# Copy runtime files
cp experimental/bios-architecture/runtime-files/*.txt ~/Desktop/bios-upload/

# Copy assignment files
cp production/knowledge-base/"B42 Final Project.txt" ~/Desktop/bios-upload/
cp production/knowledge-base/"B42 Chatstorm T.A. Guide v4.2.txt" ~/Desktop/bios-upload/
cp production/knowledge-base/"Appendix A - Required Values Index v3.2.txt" ~/Desktop/bios-upload/

# Copy theory files
cp production/knowledge-base/*_theory.txt ~/Desktop/bios-upload/

# Copy validator
cp experimental/bios-architecture/code-interpreter-version/runtime_validator.py ~/Desktop/bios-upload/

# Check count (should be 11)
ls ~/Desktop/bios-upload | wc -l
```

Then upload all files from `~/Desktop/bios-upload/` at once.

---

**Total files**: 11 to upload + 1 for instructions = 12 files total
