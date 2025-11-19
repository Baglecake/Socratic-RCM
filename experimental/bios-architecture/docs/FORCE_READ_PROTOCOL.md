# Force-Read Protocol: Preventing Lazy Retrieval

**Purpose**: Ensure GPT reads the runtime file every turn instead of relying on memory

---

## The Lazy Retrieval Problem

### What Is It?
"Lazy retrieval" occurs when an LLM with access to external files starts to:
1. Remember the general pattern of instructions
2. Assume it "knows" what to do next
3. Skip actually reading the file
4. Generate responses based on pattern-matching rather than exact retrieval

### Why It's Dangerous
```
Expected:  GPT reads [STEP 1.2.2] → Outputs exact question → Student answers
Reality:   GPT remembers "Step 1.2.2 is about project goals" → Improvises question
Result:    Question doesn't match runtime file, loses precision
```

### Example Scenario
```
RUNTIME FILE SAYS:
[STEP 1.2.2]
REQUIRED OUTPUT: "Project goal: What question/dynamic will you model?
                  Think theoretically—what tension? (2-3 sent.)"

LAZY GPT MIGHT SAY:
"What's your project goal? What do you want to explore?" ❌

CORRECT GPT SAYS:
"Project goal: What question/dynamic will you model?
 Think theoretically—what tension? (2-3 sent.)" ✅
```

---

## Force-Read Mechanisms in BIOS v1.0

### 1. Mandatory Execution Loop

The BIOS requires a **6-step sequence** every turn:

```
FOR EVERY SINGLE TURN:

1. LOCATE: Determine current Phase/Step (e.g., "1.2.2")
   ↓
2. RETRIEVE: Search B42_Runtime_Logic.txt for [STEP 1.2.2]
   ↓
3. READ: Extract INSTRUCTION, REQUIRED OUTPUT, RCM CUE, CONSTRAINT
   ↓
4. THEORY CHECK: If theory involved, search KB[5-8]
   ↓
5. EXECUTE: Output the EXACT question from REQUIRED OUTPUT
   ↓
6. VALIDATE: Check student response against CONSTRAINT
   ↓
7. ADVANCE: Move to next step, repeat from step 1
```

**Enforcement**: The BIOS explicitly states "For EVERY single turn, you MUST perform this exact sequence"

### 2. Internal Verification Checklist

Before executing each step, GPT must internally verify:

```
Before asking the question:
- [ ] I have retrieved [STEP X.Y.Z] from KB[1]
- [ ] I have read the REQUIRED OUTPUT for this step
- [ ] I have checked KB[5-8] if theory is involved
- [ ] I am using the EXACT wording from the runtime file
```

**Enforcement**: "Internally verify" creates a mental checkpoint

### 3. Explicit Anti-Lazy Language

The BIOS includes a dedicated "FORCE-READ ENFORCEMENT" section:

```
CRITICAL: You must READ the runtime file EVERY turn.
DO NOT rely on memory or "knowing the gist."
```

**Enforcement**: Direct prohibition against the lazy pattern

### 4. "NO HALLUCINATED STEPS" Prohibition

One of the 5 absolute prohibitions:

```
2. NO HALLUCINATED STEPS:
   NEVER invent questions, skip steps, or modify instructions.
   Execute ONLY what is in B42_Runtime_Logic.txt.
```

**Enforcement**: Treats improvisation as a hardware-level violation

### 5. Position Tracking Requirement

GPT must display current position every turn:

```
"Phase [X], Step [Y.Z.W]"

After each student response:
"✅ [Step X.Y.Z] complete. Moving to [Step X.Y.Z+1]..."
```

**Enforcement**: Makes step numbers visible, easier to catch mismatches

### 6. Mantra: "I retrieve, read, and execute"

Final line of BIOS:

```
MANTRA: "I do not create. I do not improvise. I retrieve, read, and execute."
```

**Enforcement**: Reinforces the execution mindset

---

## How to Test Force-Read Compliance

### Test 1: Word-for-Word Match
**Setup**: Compare GPT output to runtime file
**Method**:
1. GPT asks question at Step 1.2.2
2. Copy GPT's exact wording
3. Search runtime file for [STEP 1.2.2] REQUIRED OUTPUT
4. Compare character-by-character

**Pass Criteria**: 100% match (including punctuation, sentence count)
**Fail Indicator**: Any paraphrasing, reordering, or substitution

**Example**:
```
RUNTIME: "Project goal: What question/dynamic will you model?
          Think theoretically—what tension? (2-3 sent.)"

GPT OUTPUT: "Project goal: What question/dynamic will you model?
             Think theoretically—what tension? (2-3 sent.)" ✅

GPT OUTPUT: "What's your project goal? What dynamic will you explore?" ❌
```

### Test 2: Step Number Consistency
**Setup**: Track step progression
**Method**:
1. Note which step GPT says it's on: "Phase 1, Step 1.2.2"
2. Check if question matches [STEP 1.2.2] in runtime file
3. Verify next step advances correctly: 1.2.2 → 1.2.3

**Pass Criteria**: Step numbers always match content
**Fail Indicator**: Step 1.2.2 displayed but question is from 1.2.3

### Test 3: Unexpected Input Handling
**Setup**: Give vague/unexpected answer
**Method**:
1. GPT asks Step 1.2.2 question
2. Student gives vague answer: "I want to study society"
3. Check if GPT uses RCM CUE from [STEP 1.2.2]

**Pass Criteria**: GPT retrieves and uses exact RCM CUE from runtime file
**Fail Indicator**: GPT improvises a generic follow-up question

**Example**:
```
RUNTIME RCM CUE for 1.2.2:
"Think about the core tension between your two theorists.
 What observable dynamic would show this tension playing out?"

GPT SHOULD SAY (retrieving from runtime): ✅
"Think about the core tension between your two theorists.
 What observable dynamic would show this tension playing out?"

GPT SHOULD NOT SAY (improvising): ❌
"Can you be more specific about what aspect of society you want to study?"
```

### Test 4: Mid-Conversation Retrieval
**Setup**: Test if GPT "forgets" to retrieve after several turns
**Method**:
1. Complete Steps 1.1 through 1.2.4 (6+ turns)
2. At Step 1.2.5, check word-for-word match
3. Verify GPT still retrieving exact wording

**Pass Criteria**: Same precision at Step 1.2.5 as Step 1.1
**Fail Indicator**: Early steps match runtime, later steps drift

### Test 5: Theory Check Enforcement
**Setup**: Step requires theory (e.g., defining "alienation")
**Method**:
1. GPT reaches Step 1.2.3 (Concept A definition)
2. Student asks "What is alienation?"
3. Check if GPT cites KB[5] (marx_theory.txt)

**Pass Criteria**: GPT says "Per lecture..." and cites KB[5]
**Fail Indicator**: GPT provides general definition without checking KB[5]

---

## Metrics to Track

### Primary Metric: Exact Match Rate
```
Exact Match Rate = (# of questions matching runtime word-for-word) / (Total questions asked)

Target: ≥95%
Acceptable: ≥90%
Failure: <90%
```

### Secondary Metrics

| Metric | Calculation | Target |
|--------|-------------|--------|
| **Step Number Accuracy** | Displayed step matches content | 100% |
| **RCM Cue Retrieval** | Uses runtime RCM when student vague | ≥90% |
| **Theory Check Compliance** | Cites KB[5-8] when theory involved | ≥95% |
| **Improvisation Incidents** | # of hallucinated/modified questions | ≤5 per 100 questions |

---

## What "Good" Looks Like

### Example of Correct Force-Read Behavior

**Turn 1**:
```
GPT: "Phase 1, Step 1.1"
GPT: "Have you completed your storyboard? (yes/no)"
     ↑ Matches [STEP 1.1] REQUIRED OUTPUT exactly ✅
```

**Turn 2** (Student says "no"):
```
GPT: "I recommend completing it first, but you may proceed if you prefer."
     ↑ Matches [STEP 1.1] CONSTRAINT exactly ✅
GPT: "✅ Step 1.1 complete. Moving to Step 1.2.1..."
GPT: "Phase 1, Step 1.2.1"
GPT: "Which theoretical option from KB[2]? (A, B, C, D, or E)"
     ↑ Matches [STEP 1.2.1] REQUIRED OUTPUT exactly ✅
```

**Turn 3** (Student says "Option A: Gendered Domination and Alienation"):
```
GPT: "✅ Noted: Option A - Gendered Domination and Alienation (Wollstonecraft & Marx)"
     ↑ Retrieved option name from KB[2] ✅
GPT: "✅ Step 1.2.1 complete. Moving to Step 1.2.2..."
GPT: "Phase 1, Step 1.2.2"
GPT: "Project goal: What question/dynamic will you model?
      Think theoretically—what tension? (2-3 sent.)"
     ↑ Matches [STEP 1.2.2] REQUIRED OUTPUT exactly ✅
```

---

## What "Bad" Looks Like (Lazy Retrieval Detected)

### Example 1: Paraphrasing Questions
```
RUNTIME: "Project goal: What question/dynamic will you model?
          Think theoretically—what tension? (2-3 sent.)"

GPT SAYS: "What's your project goal? Describe the dynamic you want to explore." ❌
          ↑ Improvising, not retrieving exact wording
```

### Example 2: Skipping Step Numbers
```
GPT: "Phase 1, Step 1.2.2"
GPT: "Which theoretical option from KB[2]? (A, B, C, D, or E)" ❌
     ↑ This is the question for Step 1.2.1, not 1.2.2
     ↑ Step number doesn't match content
```

### Example 3: Generic RCM Cues (Not from Runtime)
```
RUNTIME RCM CUE: "Think about the core tension between your two theorists.
                  What observable dynamic would show this tension playing out?"

GPT SAYS: "Can you elaborate on that?" ❌
          ↑ Generic probe, not the specific RCM cue from runtime
```

### Example 4: Skipping Theory Check
```
Student asks: "What is alienation?"

RUNTIME: THEORY CHECK: YES - Search KB[5] (marx_theory.txt)

GPT SAYS: "Alienation is when workers feel disconnected from their labor..." ❌
          ↑ Used general knowledge, didn't check KB[5]
          ↑ Should say "Per lecture..." and cite KB[5]
```

---

## Automated Testing Script (Pseudocode)

```python
def test_force_read_compliance(gpt_session, runtime_file):
    test_results = {
        "exact_match": 0,
        "total_questions": 0,
        "step_number_accurate": 0,
        "rcm_cue_retrieved": 0,
        "theory_check_complied": 0,
        "improvisation_count": 0
    }

    for step in runtime_file.get_all_steps():
        # 1. GPT should ask the question
        gpt_output = gpt_session.get_next_question()

        # 2. Check exact match
        expected_question = step.get("REQUIRED OUTPUT")
        if gpt_output == expected_question:
            test_results["exact_match"] += 1
        else:
            test_results["improvisation_count"] += 1
            log_mismatch(step.number, expected_question, gpt_output)

        # 3. Check step number displayed
        displayed_step = gpt_session.get_current_step_number()
        if displayed_step == step.number:
            test_results["step_number_accurate"] += 1

        test_results["total_questions"] += 1

        # 4. Test RCM cue (give vague answer)
        gpt_session.send_student_input("I don't know")
        gpt_follow_up = gpt_session.get_response()
        expected_rcm = step.get("RCM CUE")
        if expected_rcm in gpt_follow_up:
            test_results["rcm_cue_retrieved"] += 1

        # 5. Test theory check (if applicable)
        if step.get("THEORY CHECK") == "YES":
            gpt_session.send_student_input("What does [concept] mean?")
            gpt_theory_response = gpt_session.get_response()
            if "Per lecture" in gpt_theory_response:
                test_results["theory_check_complied"] += 1

    # Calculate rates
    exact_match_rate = test_results["exact_match"] / test_results["total_questions"]
    improvisation_rate = test_results["improvisation_count"] / test_results["total_questions"]

    return exact_match_rate >= 0.95 and improvisation_rate <= 0.05
```

---

## If Force-Read Fails

### Diagnosis
1. **Check retrieval logs**: Is GPT actually searching the file?
2. **Review prompt emphasis**: Are prohibitions strong enough?
3. **Test at different conversation lengths**: Does it fail after 10+ turns?
4. **Compare to monolithic**: Does v8.4 maintain strictness better?

### Iteration Options

#### Option 1: Strengthen Force-Read Language
- Add "CRITICAL" markers
- Increase repetition of anti-lazy language
- Add verification checklist before EVERY question

#### Option 2: Add Explicit Retrieval Quotes
- Require GPT to quote the step it retrieved:
  ```
  Internal retrieval:
  [STEP 1.2.2]
  REQUIRED OUTPUT: "Project goal: What question/dynamic will you model?"

  Now executing:
  "Project goal: What question/dynamic will you model?"
  ```

#### Option 3: Hybrid Architecture
- Keep BIOS for Phase 1 (most critical)
- Embed Phases 2-3 in system prompt (less critical, fewer steps)

#### Option 4: Abort BIOS Approach
- If force-read cannot be reliably enforced
- Archive as experimental
- Stick with monolithic v8.4
- Wait for GPT Builder to increase character limit

---

## Success Criteria

BIOS v1.0 is production-ready if:

✅ Exact match rate ≥ 95% across 100+ questions
✅ Step number accuracy = 100%
✅ RCM cue retrieval ≥ 90%
✅ Theory check compliance ≥ 95%
✅ Improvisation rate ≤ 5 per 100 questions
✅ Maintains performance after 20+ turn conversations
✅ Student feedback: "As strict as previous version"

If ANY criterion fails → BIOS is not ready for production

---

## Timeline for Force-Read Testing

### Week 1: Setup
- Complete runtime file conversion (all steps)
- Upload BIOS + runtime to test GPT instance
- Prepare test scripts

### Week 2: Automated Testing
- Run 100 questions through test script
- Measure exact match rate
- Log all improvisation incidents

### Week 3: Human Testing
- 5 volunteer students run through Phase 1
- Collect feedback on strictness
- Compare to v8.4 experience

### Week 4: Analysis
- Calculate all metrics
- Review improvisation patterns
- Decision: Deploy, Iterate, or Archive

---

**Bottom Line**: Force-read protocol is the make-or-break feature of BIOS architecture.

If it works → Unlimited scalability
If it fails → Stick with monolithic v8.4
