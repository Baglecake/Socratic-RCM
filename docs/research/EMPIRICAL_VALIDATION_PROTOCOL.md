# Empirical Validation Protocol for Algorythmic RAG
## A Mixed-Methods Research Design

---

## Executive Summary

This protocol establishes rigorous empirical methods for validating Algorythmic RAG's effectiveness across three core claims:

1. **Boundary Preservation Hypothesis**: RCM-guided students produce more original, theoretically grounded work than AI-assisted students
2. **Process Efficacy Hypothesis**: Process-retrieval scaffolding improves learning outcomes compared to content-retrieval or no-scaffolding conditions
3. **Adaptive Guidance Hypothesis**: PRAR successfully addresses Perception-Orchestration-Elicitation limitations identified in current Socratic LLMs

The protocol employs a convergent parallel mixed-methods design combining:
- Randomized controlled trials (quantitative)
- Qualitative analysis of student work (qualitative)
- Interaction log analysis (computational)
- Student surveys and interviews (qualitative)

**Timeline**: 2 academic semesters (pilot + full study)
**Sample Size**: 150-200 students across 6 course sections
**IRB Status**: Protocol requires institutional review board approval before implementation

---

## Study 1: Boundary Preservation and Learning Outcomes

### Research Questions

**RQ1.1**: Do RCM-guided students produce more original simulation designs than students using standard AI assistance?

**RQ1.2**: Does enforcing non-generation constraints improve or impair learning outcomes in theoretical operationalization tasks?

**RQ1.3**: How do students perceive the value of constraint-based vs. generative AI assistance?

### Study Design: Randomized Controlled Trial

**Participants**: 150 students enrolled in SOC B42 or equivalent classical theory course across 6 sections (25 students per section)

**Random Assignment**: Within each section, students randomly assigned to one of three conditions:

1. **Experimental Condition (RCM-Guided)**: Full Algorythmic RAG implementation with strict Socratic constraints
   - B42 Chatstorm TA system as currently implemented
   - System prompt v7.3 with RCM framework
   - Required Values Index enforcement
   - No creative content generation allowed

2. **Active Control (Standard AI)**: Access to GPT-4 with general academic assistance prompt
   - Standard OpenAI ChatGPT interface
   - General prompt: "You are a helpful teaching assistant for a sociology course. Help students design multi-agent simulations to explore classical social theory."
   - No specific constraints on content generation
   - Students can request examples, drafts, suggestions

3. **Passive Control (Traditional)**: Instructor office hours and written assignment guidelines only
   - No AI assistance
   - Standard pedagogical support (lectures, readings, rubric)
   - Can consult instructor during office hours

**Stratification**: Random assignment stratified by:
- Prior GPA (< 3.0, 3.0-3.5, > 3.5)
- Prior sociology coursework (introductory only vs. intermediate/advanced)
- Self-reported AI familiarity (low, medium, high)

### Data Collection

**Pre-Study Measures** (Week 1):
- Demographic questionnaire
- Prior knowledge assessment (10-item multiple choice on classical theory)
- AI familiarity and attitudes scale (adapted from Kasneci et al. 2023)
- Self-efficacy in theoretical application (7-point Likert scale, 8 items)

**During-Study Measures** (Weeks 2-12):
- **Interaction logs**: Full conversation transcripts for Experimental and Active Control conditions
  - Automated logging via OpenAI API
  - De-identified before analysis
  - Coded for: number of turns, student word count, AI word count, content generation instances

- **Intermediate artifacts**: Required Values completion tracking (Experimental condition only)
  - Timestamped completion of each field ([Concept A], [Agent Goal], etc.)
  - Version history showing revision patterns
  - Alignment scores (does [Concept A] match selected theoretical option?)

- **Weekly surveys** (5 minutes, administered via Canvas):
  - Confidence in project progress (3 items)
  - Perceived AI helpfulness (4 items)
  - Cognitive load (NASA-TLX adapted for academic work)
  - Open-ended: "What was most helpful/frustrating this week?"

**Post-Study Measures** (Week 13-14):
- **Final simulation quality** (primary outcome):
  - Theoretical grounding score (0-30 points, see rubric below)
  - Methodological rigor score (0-30 points)
  - Originality score (0-20 points)
  - Overall quality score (0-20 points)
  - Scored by 2 blind raters (instructors from non-participating sections)
  - Inter-rater reliability target: Cohen's κ > 0.70

- **Learning outcomes assessment**:
  - Post-test on theoretical concepts (same 10-item test from pre-study, plus 10 application items)
  - Transfer task: Design simulation for new theoretical scenario not covered in course
  - Scored for: appropriate theory selection, concept operationalization, hypothesis formation

- **Exit survey and interviews**:
  - Perceived learning gains (SALG instrument adapted)
  - AI assistance evaluation (usefulness, appropriateness, frustration points)
  - Semi-structured interviews with 30 volunteers (10 per condition): 45-60 minutes, incentivized with $25 gift card

### Primary Outcome Measures

**Simulation Quality Rubric** (100 points total):

*Theoretical Grounding (30 points)*:
- [10] Concepts accurately reflect chosen theorist's framework
- [10] Concepts demonstrate deep reading of primary texts
- [10] Simulation design creates valid test of theoretical claim

*Methodological Rigor (30 points)*:
- [10] Baseline and experimental conditions create clean contrast
- [10] Agent designs appropriately operationalize theoretical concepts
- [10] Analysis plan connects simulation outcomes to theory

*Originality (20 points)*:
- [10] Novel setting/scenario (not replicated from examples)
- [10] Creative operationalization of abstract concepts

*Execution Quality (20 points)*:
- [10] Clear, specific agent prompts and round instructions
- [10] Thoughtful analysis of simulation results

**Plagiarism and AI-Generation Detection**:
- All submissions screened with GPTZero and Turnitin AI detection
- Suspicious submissions flagged for manual review
- Hypothesis: Experimental condition will show lowest AI-generation scores despite having AI access

### Statistical Analysis Plan

**Primary Analysis**: One-way ANOVA comparing simulation quality scores across three conditions
- Null hypothesis: No difference in mean quality scores
- Expected effect: Experimental ≥ Traditional > Active Control
- Post-hoc comparisons: Tukey HSD
- Planned contrasts:
  - Experimental vs. Active Control (tests boundary preservation)
  - Experimental vs. Traditional (tests process efficacy)
  - (Experimental + Active Control) vs. Traditional (tests general AI benefit)

**Secondary Analyses**:
- ANCOVA with pre-test scores and stratification variables as covariates
- Subgroup analysis by prior GPA and AI familiarity
- Mediation analysis: Does Required Values completion mediate effect of condition on quality?
- Moderation analysis: Does AI familiarity moderate treatment effect?

**Effect Size Targets**:
- Experimental vs. Active Control: Cohen's d > 0.50 (medium effect)
- Experimental vs. Traditional: Cohen's d > 0.35 (small-medium effect)
- Power analysis: N=150 provides 80% power to detect d=0.50 at α=0.05

### Qualitative Analysis

**Student Work Analysis** (Grounded Theory Approach):
- Purposive sampling: 10 simulation designs per condition (30 total)
- Selected to represent quality distribution (high, medium, low within each condition)
- Coding scheme:
  - Theory application patterns (how concepts are operationalized)
  - Creative vs. templatic design choices
  - Evidence of iteration and revision
  - Theoretical depth markers (citations, nuanced understanding)

**Interview Analysis** (Thematic Analysis):
- Transcribe all 30 interviews
- Initial coding by 2 researchers independently
- Code reconciliation and theme development
- Focus on:
  - Perceived learning experiences across conditions
  - Frustration points and workarounds
  - Relationship between constraints and creativity
  - Long-term pedagogical value perceptions

**Interaction Log Analysis** (Computational Methods):
- Automated coding of conversation patterns:
  - Student utterance length and complexity (Flesch-Kincaid grade level)
  - AI response types (question, explanation, example, directive)
  - Turn-taking patterns (who initiates topics, who closes loops)
  - Content generation instances (AI provides example agent, scenario description, etc.)

- Hypothesis testing:
  - H1: Experimental condition will show more student-generated text per conversation
  - H2: Active Control will show more AI-generated creative content
  - H3: Experimental condition will show more question-dense AI responses

### Timeline

**Semester 1 (Pilot Study)**: Fall 2025
- N=60 students (2 sections, 30 per section)
- Refine instruments and procedures
- Test inter-rater reliability
- Identify technical issues

**Semester 2 (Full Study)**: Spring 2026
- N=150 students (6 sections)
- Full protocol implementation
- Data collection and analysis
- Summer 2026: Write-up and dissemination

---

## Study 2: Process Retrieval vs. Content Retrieval

### Research Questions

**RQ2.1**: Does process-retrieval (PRAR) produce better learning outcomes than content-retrieval (traditional RAG)?

**RQ2.2**: What are the differential effects on different student populations (high vs. low prior knowledge)?

**RQ2.3**: How do students use and perceive different RAG paradigms?

### Study Design: Comparative RAG Implementation

**Participants**: Same 150 students from Study 1, but different randomization:

**Two Conditions** (within Active Control group from Study 1):

1. **Process-RAG (PRAR)**: Algorythmic RAG with full RCM implementation
   - As implemented in Experimental condition above

2. **Content-RAG (Traditional)**: Modified B42 TA that retrieves content rather than process
   - Same knowledge base (assignment, rubric, theory documents)
   - Different system prompt:
     - Retrieves relevant theoretical passages when students ask about concepts
     - Provides example simulation designs from previous years
     - Explains theoretical concepts with generated examples
     - Does NOT enforce Required Values or process constraints
   - Uses standard RAG retrieval (semantic similarity to query)

**Measurement**: Same instruments as Study 1, with additional measures:

**RAG-Specific Metrics**:
- Retrieval patterns: What gets retrieved and when?
  - Process-RAG: Required Values Index entries, Step-by-Step Guide sections, constraint reminders
  - Content-RAG: Theoretical passages, example designs, concept explanations

- Retrieval effectiveness: Does retrieved information get used?
  - Code student work for incorporation of retrieved content
  - Track whether students follow retrieved process steps
  - Measure alignment between retrieval and subsequent student work

**Hypothesis**:
- Process-RAG will produce higher originality scores (less templatic)
- Content-RAG will produce faster completion but lower theoretical depth
- High prior knowledge students will benefit more from Process-RAG
- Low prior knowledge students may initially prefer Content-RAG but show lower learning gains

### Analysis

**Quantitative**: Independent samples t-tests comparing Process-RAG vs. Content-RAG on all outcome measures from Study 1

**Qualitative**: Comparative case analysis of 10 matched pairs (similar prior knowledge, GPA, AI familiarity, one in each condition)
- Trace how different RAG paradigms shape student thinking
- Identify critical incidents where Process-RAG constraints prevent shortcuts
- Document moments where Content-RAG examples become templates

---

## Study 3: Perception-Orchestration-Elicitation Validation

### Research Questions

**RQ3.1**: Does PRAR successfully implement the Perception-Orchestration-Elicitation framework identified by Liu et al. (2025)?

**RQ3.2**: Where does the system fail on P-O-E dimensions, and what patterns predict failure?

**RQ3.3**: How do P-O-E capabilities correlate with student learning outcomes?

### Study Design: Systematic Interaction Analysis

**Data Source**: Interaction logs from Experimental condition in Study 1 (N=50 students, ~1000 conversation turns)

**Coding Scheme** (adapted from Liu et al. 2025):

**Perception Dimension**:
- **P-Affirm**: Does system correctly identify when student response is accurate/appropriate?
  - Score 0-1: 0 = incorrect judgment, 0.5 = implicit recognition, 1 = explicit affirmation
- **P-Redirect**: Does system correctly identify when student response is erroneous/confused?
  - Score 0-1: 0 = misses error, 0.5 = vague concern, 1 = explicit correction

**Orchestration Dimension**:
- **O-Advance**: When student demonstrates understanding, does system progress appropriately?
  - Score 0-1: 0 = repeats previous content, 1 = introduces new challenge
- **O-Reconfigure**: When student is confused/incorrect, does system adapt explanation?
  - Score 0-1: 0 = continues unchanged, 1 = simplifies/restructures approach

**Elicitation Dimension**:
- **E-Strategic**: In positive learner states, does system ask higher-order questions?
  - Score 0-3: 0 = no question, 1 = factual recall, 2 = procedural, 3 = reasoning/transfer
- **E-Heuristic**: In negative learner states, does system ask intuitive/exploratory questions?
  - Score 0-3: Same scale as E-Strategic
- **ESA (Elicitation Strategy Adaptivity)**: E-Strategic minus E-Heuristic average
  - Higher ESA = better adaptation

**Coding Procedure**:
1. Two trained coders (graduate students in sociology education) independently code 100 randomly selected conversation turns
2. Calculate inter-rater reliability (target: Krippendorff's α > 0.70 for each dimension)
3. Reconcile differences through discussion
4. Primary coder completes remaining turns
5. Secondary coder spot-checks 20% of remaining turns to monitor drift

**Student State Classification**:
Each student turn coded as one of four states (following Liu et al. 2025):
- **Accurate**: Provides correct theoretical definition, appropriate design choice, etc.
- **Erroneous**: Provides incorrect information, theoretically weak choice
- **Comprehension**: Explicitly expresses understanding ("I see how alienation differs from inequality")
- **Confusion**: Explicitly expresses uncertainty ("I don't understand how to operationalize this")

**Analysis**:

*Descriptive Statistics*:
- Mean scores on each P-O-E dimension
- Distribution of scores (0, 0.5, 1 for P/O; 0-3 for E)
- ESA calculation and distribution
- Comparison to Liu et al.'s benchmark scores for existing models (GPT-4.1, Claude-Sonnet-4, etc.)

*Failure Pattern Analysis*:
- Identify conversation turns where system scores 0 on any P-O-E dimension
- Qualitative analysis: What student states trigger failures?
- Pattern mining: Do failures cluster around specific Required Values?
- Error taxonomy development (similar to Liu et al.'s failure case analysis)

*Predictive Modeling*:
- Regression: Do P-O-E scores predict simulation quality scores?
- Hypothesis: Higher P-Redirect and O-Reconfigure scores will predict higher learning outcomes
- Mediation: Does P-O-E performance mediate the effect of condition on outcomes?

**Expected Findings**:
- **Strengths**: High P-Affirm (>0.85), moderate O-Advance (>0.70)
- **Weaknesses**: Lower P-Redirect (<0.60), ESA near zero (similar to current LLMs)
- **Implications**: PRAR improves on standard LLMs but doesn't fully solve P-O-E challenges
- **Design Recommendations**: Specific improvements to Required Values Index to boost P-Redirect

---

## Study 4: Longitudinal Transfer and Retention

### Research Questions

**RQ4.1**: Do learning benefits of PRAR persist beyond the immediate course?

**RQ4.2**: Does RCM experience transfer to subsequent theoretical work?

**RQ4.3**: How do students retrospectively evaluate the pedagogical value of constraint-based AI?

### Study Design: Follow-Up Assessment

**Participants**: Subset of Study 1 participants who enroll in subsequent advanced sociology courses (estimated N=60-80)

**Follow-Up Timeline**:
- 1 semester later (immediate transfer)
- 2 semesters later (delayed retention)

**Measures**:

*Transfer Task* (1 semester follow-up):
- Students complete new simulation design for different theoretical framework (e.g., Weber if they studied Marx/Tocqueville)
- Scored on same rubric as original project
- Hypothesis: Experimental condition students will show higher quality on transfer task

*Retention Assessment* (2 semesters follow-up):
- Multiple-choice test on classical theory concepts from SOCB42
- Short essay: "Explain how you would design a multi-agent simulation to test [theoretical claim X]"
- Hypothesis: Experimental condition will show better retention and more sophisticated design thinking

*Retrospective Survey*:
- "How useful was the AI assistance you received in SOCB42 for your subsequent coursework?"
- "Do you wish you had access to similar AI guidance in other courses?"
- "How did the constraints on AI assistance affect your learning?"
- Open-ended reflections on pedagogical value

**Analysis**:
- Mixed-effects models accounting for repeated measures
- Qualitative analysis of retrospective reflections
- Comparison of transfer task quality across original conditions

---

## Study 5: Instructor Perspective and Adoption

### Research Questions

**RQ5.1**: How do instructors perceive the value and limitations of PRAR?

**RQ5.2**: What factors facilitate or impede adoption of Algorythmic RAG in new courses?

**RQ5.3**: How does PRAR change instructor pedagogical practices?

### Study Design: Multi-Site Implementation Study

**Participants**: 8-10 sociology instructors at 4-6 institutions

**Recruitment**:
- Purposive sampling for variation in:
  - Institution type (R1, teaching-focused, community college)
  - Course level (introductory, intermediate, advanced)
  - Instructor experience (junior, senior)
  - Theoretical focus (classical, contemporary, methods)

**Procedure**:
1. **Pre-Implementation** (1 month before term):
   - Instructors complete Process Corpus Construction Toolkit (see Appendix)
   - Adapt Required Values Index and Step-by-Step Guide for their course
   - Attend 2-hour training on PRAR implementation
   - Pre-implementation interview (30 min): pedagogical goals, AI attitudes, concerns

2. **Implementation** (1 semester):
   - Deploy customized Algorythmic RAG system
   - Weekly check-ins (15 min): troubleshooting, observations
   - Mid-semester formative feedback from students
   - Instructor keeps reflection journal (prompted weekly)

3. **Post-Implementation** (within 2 weeks of term end):
   - Review student work and outcomes
   - 60-min semi-structured interview
   - Complete adoption decision: continue, modify, discontinue?

**Interview Protocol**:

*Pre-Implementation*:
- What are your pedagogical goals for this course?
- How do you typically scaffold complex theoretical application?
- What concerns do you have about AI in education?
- What would success look like for PRAR in your course?

*Post-Implementation*:
- How did students engage with the PRAR system?
- What worked well? What didn't?
- How did this change your teaching?
- Did it achieve your pedagogical goals?
- Would you use it again? What would you change?
- How feasible is PRAR for other instructors?

**Observation Data**:
- Instructor adaptation patterns: How did they modify the Process Corpus?
- Student engagement metrics: Usage frequency, conversation length
- Outcomes: Student work quality in adapted courses

**Analysis**:
- Thematic analysis of interviews and reflection journals
- Cross-case comparison: What factors predict successful adoption?
- Process tracing: How do instructors adapt PRAR to their contexts?
- Feasibility assessment: Time costs, technical barriers, pedagogical fit

**Expected Themes**:
- Initial resistance to constraints ("students need examples")
- Recognition of originality benefits
- Challenges adapting to different theoretical frameworks
- Time investment in Process Corpus construction
- Desire for instructor dashboard/monitoring tools

---

## Ethical Considerations and IRB Protocol

### Informed Consent

**Student Participants**:
- Informed consent obtained at course start
- Clear explanation that AI assistance is experimental
- Right to withdraw without academic penalty (alternative assignment available)
- Data de-identification procedures explained
- Compensation for interview participation

**Instructor Participants**:
- Informed consent for interviews and observation
- Confidentiality protections for negative findings
- Institutional approval for course modifications

### Data Privacy and Security

**Conversation Logs**:
- Stored on encrypted servers
- Student names replaced with anonymous IDs
- No identifiable information in research publications
- Data retention: 5 years post-publication, then destroyed
- Students can request log deletion (without penalty)

**AI Safety**:
- System monitoring for harmful outputs
- Flagging mechanism for inappropriate responses
- Instructor override capability
- Clear instructions for students if system malfunctions

### Equity Considerations

**Access**:
- All students have equal AI access regardless of condition
- Alternative assignment for students who decline AI use
- Technical support for students with limited tech experience

**Representation**:
- Oversample from underrepresented groups in interviews
- Subgroup analysis by demographics (with adequate N)
- Explicit attention to whose voices shape findings

### Conflicts of Interest

**Researcher Positionality**:
- Lead researcher is developer of PRAR framework (potential bias toward positive findings)
- Mitigation: Independent data analysis by researchers not involved in system development
- Pre-registration of hypotheses and analysis plans
- Transparent reporting of all findings, including null results

---

## Dissemination Plan

### Academic Publications (Target Journals)

**Quantitative Outcomes** (Study 1-2):
- *International Journal of Artificial Intelligence in Education* (IJAIED)
- *Computers & Education*
- Target: Submit Fall 2026

**Qualitative Analysis** (Study 1, 3):
- *Learning and Instruction*
- *Teaching Sociology*
- Target: Submit Spring 2027

**P-O-E Framework Validation** (Study 3):
- *Educational Psychology Review*
- Or as short paper at EDM (Educational Data Mining) conference
- Target: Submit Summer 2026

**Longitudinal Follow-Up** (Study 4):
- *Journal of Educational Psychology*
- Target: Submit Fall 2027

### Conference Presentations

- **Learning Analytics & Knowledge (LAK)** 2026: Interaction log analysis
- **AI in Education (AIED)** 2026: PRAR framework and initial outcomes
- **American Sociological Association (ASA)** 2026: Sociology education section
- **ACL Workshop on NLP for Education** 2026: Process retrieval methods

### Open Science Practices

**Pre-Registration**:
- Study 1 and 2 pre-registered on Open Science Framework before data collection
- Hypotheses, analysis plans, and sample size determinations documented

**Data Sharing**:
- De-identified interaction logs shared on PhysioNet (with proper consent)
- Coding schemes and rubrics shared on OSF
- Qualified researchers can request access for secondary analysis

**Materials Sharing**:
- Process Corpus Construction Toolkit (open access)
- System prompts and knowledge base templates (GitHub repository)
- Survey instruments and interview protocols (OSF)

---

## Budget Estimate

### Personnel
- Graduate Research Assistants (2 GRAs × 20 hrs/week × 30 weeks × $25/hr): $30,000
- Interview transcription services (30 interviews × $100): $3,000
- Blind raters for simulation scoring (2 raters × 150 projects × $15/project): $4,500

### Participant Compensation
- Interview incentives (60 students × $25): $1,500
- Survey completion incentives (200 students × $5): $1,000

### Technology
- OpenAI API costs (estimated 1M tokens × $0.01/1K): $10,000
- Server hosting and data storage: $2,000
- Software licenses (NVivo, SPSS): $1,500

### Other
- Conference travel (2 conferences × $1,500): $3,000
- Publication fees (open access): $4,000

**Total Estimated Budget**: $60,500

---

## Timeline Summary

| Semester | Activities | Deliverables |
|----------|-----------|--------------|
| **Summer 2025** | IRB approval, instrument development, RA training | IRB protocol, pre-registration |
| **Fall 2025** | Pilot study (N=60), instrument refinement | Pilot report, refined instruments |
| **Spring 2026** | Full Study 1-3 implementation (N=150) | Complete data collection |
| **Summer 2026** | Data analysis, paper writing | Conference submissions, first papers |
| **Fall 2026** | Follow-up data (Study 4, 1-semester) | Follow-up data collection |
| **Spring 2027** | Final analysis, dissemination | Journal submissions |
| **Fall 2027** | Final follow-up (Study 4, 2-semester) | Longitudinal paper |

---

## Success Criteria

This validation protocol will be considered successful if:

1. **Scientific Rigor**: Achieves target sample sizes, acceptable inter-rater reliability (κ > 0.70), and sufficient statistical power

2. **Empirical Support**: Finds statistically significant advantages for PRAR on at least 2 of 3 primary outcomes (theoretical grounding, originality, learning gains)

3. **Practical Feasibility**: Demonstrates that at least 60% of instructors successfully implement PRAR with positive student outcomes

4. **Theoretical Contribution**: Advances understanding of process-retrieval paradigms and provides actionable design principles

5. **Dissemination Impact**: Results published in 3+ peer-reviewed venues and presented at 3+ conferences

---

## Contingency Plans

**Low Enrollment**: If N < 120, extend data collection to additional semester

**Technical Failures**: Backup system prompts and manual fallback procedures documented

**Null Findings**: Pre-commitment to publish regardless of results; negative findings inform iteration

**IRB Delays**: Pilot study can begin with limited data collection while full approval pending

---

## Conclusion

This empirical validation protocol provides comprehensive, rigorous methods for testing Algorythmic RAG's core claims. By combining randomized controlled trials, qualitative analysis, computational methods, and longitudinal follow-up, we will establish whether PRAR represents a genuine advance in pedagogical AI or requires further refinement. The multi-study design allows triangulation across methods and provides rich, actionable insights for both researchers and practitioners.
