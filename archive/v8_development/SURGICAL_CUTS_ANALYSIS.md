# Surgical Cuts Analysis - v8.1 Optimization

**Current**: 8,202 bytes (with newlines)
**Target**: <8,000 bytes
**Need to Cut**: ~202 characters
**Strategy**: Ultra-precise, zero functional impact

---

## Proposed Minimal Cuts (Ranked by Safety)

### Category 1: Redundant Words in Instructions (Safest)

1. **Line 50**: "Check KB[2]. Acknowledge exact option name from KB[2]."
   - Current: 57 chars
   - Proposed: "Check KB[2]. Acknowledge exact option name."
   - Savings: 10 chars
   - Impact: "from KB[2]" is redundant - already checking KB[2]

2. **Line 84**: "→ RCM: "What setting makes [A] vs [B] visible?""
   - Current: 49 chars
   - Proposed: "→ RCM: "What makes [A] vs [B] visible?""
   - Savings: 8 chars
   - Impact: "setting" is redundant with line 83's "Setting:"

3. **Line 100**: "→ RCM: "Purpose captures theoretical function.""
   - Current: 48 chars
   - Proposed: "→ RCM: "Purpose = theoretical function.""
   - Savings: 9 chars
   - Impact: "captures" → "=" (standard shorthand)

4. **Line 114**: "→ RCM: "This defines WHO they are." **NOTE:** → Section 2"
   - Current: 60 chars
   - Proposed: "→ RCM: "Defines WHO they are." **NOTE:** → Section 2"
   - Savings: 5 chars
   - Impact: "This" is redundant with context

5. **Line 117**: "→ If yes: "Describe rule(s), connect to theory.""
   - Current: 48 chars
   - Proposed: "→ If yes: "Describe rule(s), connect theory.""
   - Savings: 3 chars
   - Impact: "to" is unnecessary preposition

**Category 1 Total**: 35 chars

---

### Category 2: Parenthetical Clarifications (Safe)

6. **Line 42**: "Position: "Phase 1, Step X.Y.Z""
   - Already removed "(now with sub-steps)"
   - No further cut

7. **Line 62**: "→ Record. Student decides round count later."
   - Current: 45 chars
   - Proposed: "→ Record. Student decides rounds later."
   - Savings: 6 chars
   - Impact: "count" implied by "rounds"

8. **Line 127**: "→ After all: Check ≥2 used."
   - Current: 27 chars
   - Proposed: "→ After all: Check ≥2."
   - Savings: 5 chars
   - Impact: "used" is implied

9. **Line 120**: "Complete one agent before next."
   - Current: 31 chars
   - Proposed: "Complete one before next."
   - Savings: 6 chars
   - Impact: "agent" is clear from context

**Category 2 Total**: 17 chars

---

### Category 3: Instruction Verb Compression (Safe)

10. **Line 45**: ""Have you completed your storyboard? (yes/no)" → If no, suggest but allow proceeding."
    - Current: 88 chars
    - Proposed: ""Have you completed your storyboard? (yes/no)" → If no, suggest but allow."
    - Savings: 11 chars
    - Impact: "proceeding" is redundant with "allow"

11. **Line 91**: "→ Display table after all."
    - Current: 26 chars
    - Proposed: "→ Table after all."
    - Savings: 8 chars
    - Impact: "Display" is action verb that's implied

12. **Line 103**: "→ Display roster after all."
    - Current: 27 chars
    - Proposed: "→ Roster after all."
    - Savings: 8 chars
    - Impact: Same as above

13. **Line 130**: "Use KB[1] [S1-TEMPLATE]. Output ||...||"
    - Current: 40 chars
    - Proposed: "KB[1] [S1-TEMPLATE]. Output ||...||"
    - Savings: 4 chars
    - Impact: "Use" is implied action

14. **Line 136**: "Per agent: Use KB[1] [S2-TEMPLATE]. Pull Identifier/Goal/Persona from S1."
    - Current: 74 chars
    - Proposed: "Per agent: KB[1] [S2-TEMPLATE]. Pull Identifier/Goal/Persona from S1."
    - Savings: 4 chars
    - Impact: "Use" is implied

**Category 3 Total**: 35 chars

---

### Category 4: Article and Preposition Removal (Safe)

15. **Line 53**: "→ RCM: Connect to theory. Probe if vague."
    - Current: 42 chars
    - Proposed: "→ RCM: Connect theory. Probe if vague."
    - Savings: 3 chars
    - Impact: "to" is unnecessary preposition

16. **Line 56**: "→ RCM: "Key features agents experience?""
    - Current: 44 chars
    - Proposed: "→ RCM: "Features agents experience?""
    - Savings: 4 chars
    - Impact: "Key" is implied by context

17. **Line 77**: "→ RCM: "What does [theory] predict?""
    - Current: 38 chars
    - Proposed: "→ RCM: "What [theory] predicts?""
    - Savings: 5 chars
    - Impact: Grammatical simplification

18. **Line 111**: "→ RCM: "Be concrete—what will they accomplish?""
    - Current: 48 chars
    - Proposed: "→ RCM: "Be concrete—what they accomplish?""
    - Savings: 5 chars
    - Impact: "will" is implied future tense

**Category 4 Total**: 17 chars

---

### Category 5: Spacing Around Slashes (Safe Formatting)

19. **Lines 165-168**: FLOW section
    - "All / Moderator" → "All/Moderator" (save 2 chars × 4 instances = 8 chars)
    - "Default / Random / Active / Moderator" → "Default/Random/Active/Moderator" (save 6 chars)
    - Total: 14 chars

20. **Lines 171-172**: STYLE section
    - "Min / Brief / Med / Thor / Exh / Dyn" → "Min/Brief/Med/Thor/Exh/Dyn" (save 10 chars)
    - "Defaults / Custom" → "Defaults/Custom" (save 2 chars)
    - Total: 12 chars

**Category 5 Total**: 26 chars

---

### Category 6: Section Reference Abbreviations (Safe)

21. **Line 114**: "**NOTE:** → Section 2"
    - Current: 22 chars (just this part)
    - Proposed: "**NOTE:** → S2"
    - Savings: 8 chars
    - Impact: Standard abbreviation

22. **Line 118**: "**NOTE:** → Section 3, NOT agent prompt"
    - Current: 40 chars (just this part)
    - Proposed: "**NOTE:** → S3, NOT agent prompt"
    - Savings: 8 chars
    - Impact: Standard abbreviation

23. **Line 197**: "Ready: Section 1 (ref)"
    - Current: 22 chars (just this part)
    - Proposed: "Ready: S1 (ref)"
    - Savings: 7 chars
    - Impact: Standard abbreviation

**Category 6 Total**: 23 chars

---

### Category 7: Conjunction Removal (Safe)

24. **Line 4**: "Be encouraging and supportive while never doing creative work for them."
    - Current: 71 chars
    - Proposed: "Be encouraging, supportive, never doing creative work for them."
    - Savings: 8 chars
    - Impact: "and" + "while" → comma (maintains meaning)

25. **Line 59**: "→ RCM: "If [A] suggests [X], what does [B] propose?""
    - Current: 52 chars
    - Proposed: "→ RCM: "If [A] suggests [X], what [B] proposes?""
    - Savings: 5 chars
    - Impact: "does" → verb form change

**Category 7 Total**: 13 chars

---

### Category 8: Ultra-Minimal Word Cuts (Safe)

26. **Line 66**: "**CHECKPOINT:** Display framework. "Aligns with KB[2] for testing [A] vs [B]?""
    - Current: 79 chars
    - Proposed: "**CHECKPOINT:** Display framework. "Aligns with KB[2] testing [A] vs [B]?""
    - Savings: 4 chars
    - Impact: "for" is unnecessary preposition

27. **Line 131**: ""Phase 1 complete! Review vs KB[2]. Ready for Phase 2?""
    - Current: 55 chars
    - Proposed: ""Phase 1 complete! Review vs KB[2]. Ready Phase 2?""
    - Savings: 4 chars
    - Impact: "for" is unnecessary

28. **Line 180**: "CHECK: "Config appropriate for round goals? Tests hypothesis?""
    - Current: 62 chars
    - Proposed: "CHECK: "Config appropriate? Tests hypothesis?""
    - Savings: 16 chars
    - Impact: "for round goals" can be inferred from context

**Category 8 Total**: 24 chars

---

## Recommended Cut Strategy

### Conservative Approach (200 chars exactly)

Apply cuts in this priority order:

1. **Category 5** (Spacing): 26 chars - ZERO functional impact
2. **Category 1** (Redundant words): 35 chars - Removes only redundancy
3. **Category 3** (Implied verbs): 35 chars - Removes implied actions
4. **Category 6** (Section refs): 23 chars - Standard abbreviations
5. **Category 2** (Clarifications): 17 chars - Removes implied context
6. **Category 4** (Articles/preps): 17 chars - Grammar simplification
7. **Category 7** (Conjunctions): 13 chars - Punctuation changes
8. **Category 8** (Ultra-minimal): 24 chars - Preposition removal
9. **Additional 10 chars** from remaining safe options

**Total**: ~200 chars

---

## Impact Assessment

### Functional Impact: ZERO
- All cuts remove only redundancy or implied words
- No change to workflow logic
- No change to question content
- No change to checkpoint subjects
- All critical markers preserved

### Readability Impact: MINIMAL
- Slightly more concise
- Still grammatically correct
- Maintains professional tone
- All instructions remain clear

---

## What NOT to Cut

**Protected Elements** (these must NEVER be cut):
- "and supportive" (Line 4)
- "Tone: Supportive, challenging, never prescriptive." (Line 33)
- "—wait between each" (Line 47)
- "in interactions" (Line 55)
- "(baseline+experiment in one)" (Line 61)
- "Baseline vs Experiment" (Line 79)
- "Measurable" (Line 110)
- "across project" and "doesn't count" (Line 124)
- "(how many?)" prompts (Line 167)
- "Design addresses KB[2]" (Line 195)
- All KB[1] template markers
- All [A] vs [B] references
- All RCM components

---

## Next Step

Create v8.2 with these surgical cuts applied.
