#!/usr/bin/env python3
"""
Full workflow test - runs through ALL phases with realistic answers
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from llm_client import create_llm_client, StudentInteractionHandler
from runtime_parser import Runtime
from canvas_state import CanvasState, compile_canvas_from_student_state, compile_final_document
from orchestrator import WorkflowOrchestrator

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")

# ============================================================================
# PHASE 1 ANSWERS - Theoretical Framework & Agents
# ============================================================================
PHASE1_ANSWERS = {
    "1.1": "yes",
    "1.2.1": "A",
    "1.2.2": "I want to model how workers lose control over their labor and how that shapes their decisions. The tension is whether agents can coordinate or resist when agency is suppressed.",
    "1.2.3": "Alienation is separation from creative capacities because production treats labor as owned by someone else. It manifests as mechanical compliance and survival-driven decisions.",
    "1.2.4": "Non-domination focuses on vulnerability to arbitrary power. The harm isn't disconnection but exposure to unchecked authority.",
    "1.2.5": "Single multi-round design - baseline and experiment in one simulation.",
    "1.2.6": "A - Modify one variable",
    "CHECKPOINT 1.2": "Yes, aligns with KB[2].",
    "1.3.1": "Baseline: owner controls all aspects, workers have no input.",
    "1.3.2A": "Experiment: introduce safeguard limiting arbitrary power.",
    "1.3.3": "Tests A vs B by comparing behavior under alienation vs reduced domination.",
    "CHECKPOINT 1.3": "Yes, tests the theoretical tension.",
    "1.4.1": "Small workshop with fixed workstations. Owner's office overlooks floor. Cramped space reinforces isolation.",
    "1.4.2": "3",
    "CHECKPOINT 1.4": "Yes, progression tests hypothesis.",
    "1.5.1": "4",
    "CHECKPOINT 1.5": "Yes, agents represent key positions.",
    "1.7": "Self-Reflections and Non-anthropomorphic agent.",
    "1.8": "Section 1 complete.",
}

# Iterative Phase 1 answers
PHASE1_ROUNDS = [
    "Round 1 - Baseline Alienation: Pure control, no worker input.",
    "Round 2 - Reduced Domination: Add safeguard limiting arbitrary power.",
    "Round 3 - Comparative Analysis: Review behavioral shifts.",
]

PHASE1_AGENTS = [
    ("Worker+Alice", "Human"),
    ("Worker+Ben", "Human"),
    ("Owner+Marta", "Human"),
    ("Analyst+Reporter", "Human"),
]

PHASE1_AGENT_DETAILS = [
    ("Alice's goal: gain influence over work organization.", "Alice is thoughtful but hesitant, suppresses ideas.", "no"),
    ("Ben's goal: secure predictable fair treatment.", "Ben is practical, prefers routine, pushes back on arbitrary orders.", "no"),
    ("Marta's goal: maintain productivity while asserting authority.", "Marta is confident and directive, tightens control in conflict.", "yes - If questioned: assert control. If compliant: maintain brisk style."),
    ("Analyst's goal: identify behavioral differences between conditions.", "Analyst is precise and detached, only observes.", "no"),
]

# ============================================================================
# PHASE 2 ANSWERS - Drafting
# ============================================================================

# 2.1.1 - Agent prompt confirmations
AGENT_PROMPT_CONFIRMS = ["Yes, captures Alice's role.", "Yes, captures Ben's role.", "Yes, captures Marta's role.", "Yes, captures Analyst's role."]

# 2.2.x - Round instruction answers (per round)
ROUND_ANSWERS = {
    1: {  # Baseline Alienation
        "2.2.1": "The workshop hums with machinery. Workers move mechanically between stations. Marta watches from her elevated office, issuing directives. No one questions, no one suggests. The air feels heavy with unspoken tension.",
        "2.2.2": "Alienation manifests as complete separation from decision-making. Workers execute tasks without understanding purpose. Their labor feels external, imposed.",
        "2.2.3": "Non-domination is absent - arbitrary power is unchecked. Marta can change orders without justification. Workers have no protection.",
        "2.2.4": "Workers CAN: complete assigned tasks, request clarification. Workers CANNOT: suggest changes, refuse orders, negotiate.",
        "2.2.5": "Complete three production cycles. Marta assigns tasks. Workers comply or face consequences.",
        "2.2.6": "Marta assigns tasks, workers comply silently. Any hesitation triggers reassertion of control. Round ends with production complete.",
        "2.2.7": "Yes, include Marta's behavior rules.",
        "2.2.8": "Compiled looks correct.",
        "2.2.9": "Worker+Alice, Worker+Ben, Owner+Marta",
        "2.2.10": "All",
        "2.2.11": "Default",
        "2.2.12": "Total messages: 15",
        "2.2.13": "Pause",
        "2.2.14": "5",
        "2.2.15": "5",
        "2.2.16": "no",
        "2.2.17": "no",
        "2.2.18": "default",
        "2.2.19": "Config looks correct.",
    },
    2: {  # Reduced Domination
        "2.2.1": "Same workshop, but a new rule: Marta must justify task changes. Workers have a feedback channel. The air feels slightly different - there's a possibility of voice.",
        "2.2.2": "Alienation persists structurally but workers have more information. They still don't control labor but understand decisions better.",
        "2.2.3": "Non-domination is partially activated - arbitrary power is constrained. Workers can question without fear of immediate retaliation.",
        "2.2.4": "Workers CAN: request justification, use feedback channel, suggest improvements. Workers CANNOT: refuse justified orders.",
        "2.2.5": "Complete production while testing the new feedback mechanism. Observe if participation increases.",
        "2.2.6": "Marta assigns tasks but must explain. Workers may ask questions. Round ends when production completes with feedback logged.",
        "2.2.7": "Yes, Marta's behaviors adapt to constraint.",
        "2.2.8": "Compiled looks correct.",
        "2.2.9": "Worker+Alice, Worker+Ben, Owner+Marta",
        "2.2.10": "All",
        "2.2.11": "Default",
        "2.2.12": "Total messages: 20",
        "2.2.13": "Pause",
        "2.2.14": "5",
        "2.2.15": "5",
        "2.2.16": "yes",
        "2.2.17": "no",
        "2.2.18": "default",
        "2.2.19": "Config looks correct.",
    },
    3: {  # Comparative Analysis
        "2.2.1": "Analyst reviews transcripts from both rounds. No active simulation - purely analytical. Looking for patterns of behavioral change.",
        "2.2.2": "Alienation analysis: identify markers of mechanical compliance, withdrawal, survival-driven decisions in Round 1.",
        "2.2.3": "Non-domination analysis: identify markers of increased participation, questioning, confidence in Round 2.",
        "2.2.4": "Analyst CAN: review all transcripts, identify patterns, make theoretical claims. CANNOT: interact with original agents.",
        "2.2.5": "Produce comparative report attributing behavioral changes to either alienation reduction or domination reduction.",
        "2.2.6": "Analyst reviews Round 1, then Round 2, then produces comparative analysis with theoretical attribution.",
        "2.2.7": "No additional behaviors needed.",
        "2.2.8": "Compiled looks correct.",
        "2.2.9": "Analyst+Reporter",
        "2.2.10": "All",
        "2.2.11": "Default",
        "2.2.12": "Per participant: 3",
        "2.2.13": "Auto",
        "2.2.14": "3",
        "2.2.15": "3",
        "2.2.16": "no",
        "2.2.17": "no",
        "2.2.18": "default",
        "2.2.19": "Config looks correct.",
    }
}

# 2.3.x - Helper functions
# Note: Only provide content for the 2 advanced functions selected in 1.7
# Selected: Self-Reflections and Non-anthropomorphic (NOT Moderator)
PHASE2_3_ANSWERS = {
    "2.3.1": "",  # Moderator - NOT selected, skip
    "2.3.2": "Analyst summarizes behavioral patterns and attributes to A or B.",  # Required
    "2.3.3": "Use environmental cues instead of facial expressions: 'The machine hums louder' signals tension, 'The light flickers' signals uncertainty, 'Tools clatter' signals frustration.",  # Selected
    "2.3.4": "Self-reflection: 'How did that interaction make you feel about your role?'",  # Selected
    "2.3.5": "Section 2 complete.",
}

# ============================================================================
# PHASE 3 ANSWERS - Review
# ============================================================================
PHASE3_ANSWERS = {
    "3.1": "Design looks complete and coherent.",
    "3.2": "Yes, ready for export.",
    "3.2.5": "Verified all components present.",
    "3.3": "Final confirmation - ready to run simulation.",
}


class FullWorkflowAnswerProvider:
    """Provides answers for full workflow"""

    def __init__(self):
        self.counters = {}
        self.current_round = 1
        self.answers_given = []

    def get_answer(self, prompt: str, step_id: str, orchestrator) -> str:
        """Get answer based on step"""

        # Track current round from orchestrator state
        if "current_phase2_round_counter" in orchestrator.student_state:
            self.current_round = orchestrator.student_state["current_phase2_round_counter"]

        answer = self._lookup_answer(step_id, orchestrator)
        self.answers_given.append((step_id, answer[:40] if answer else "None"))

        time.sleep(0.1)  # Small delay for readability
        print(f"> {answer}")
        return answer

    def _lookup_answer(self, step_id: str, orchestrator) -> str:
        # Phase 1 simple answers
        if step_id in PHASE1_ANSWERS:
            return PHASE1_ANSWERS[step_id]

        # Phase 1 iterative - rounds (1.4.3)
        if step_id == "1.4.3":
            idx = self.counters.get("1.4.3", 0)
            self.counters["1.4.3"] = idx + 1
            if idx < len(PHASE1_ROUNDS):
                return PHASE1_ROUNDS[idx]
            return "Additional round."

        # Phase 1 iterative - agent IDs (1.5.2)
        if step_id == "1.5.2":
            idx = self.counters.get("1.5.2", 0)
            self.counters["1.5.2"] = idx + 1
            if idx < len(PHASE1_AGENTS):
                return PHASE1_AGENTS[idx][0]
            return "Agent"

        # Phase 1 iterative - agent types (1.5.3)
        if step_id == "1.5.3":
            idx = self.counters.get("1.5.3", 0)
            self.counters["1.5.3"] = idx + 1
            if idx < len(PHASE1_AGENTS):
                return PHASE1_AGENTS[idx][1]
            return "Human"

        # Phase 1 iterative - agent goals (1.6.1)
        if step_id == "1.6.1":
            idx = self.counters.get("1.6.1", 0)
            self.counters["1.6.1"] = idx + 1
            if idx < len(PHASE1_AGENT_DETAILS):
                return PHASE1_AGENT_DETAILS[idx][0]
            return "Goal for agent."

        # Phase 1 iterative - agent personas (1.6.2)
        if step_id == "1.6.2":
            idx = self.counters.get("1.6.2", 0)
            self.counters["1.6.2"] = idx + 1
            if idx < len(PHASE1_AGENT_DETAILS):
                return PHASE1_AGENT_DETAILS[idx][1]
            return "Persona for agent."

        # Phase 1 iterative - agent behaviors (1.6.3)
        if step_id == "1.6.3":
            idx = self.counters.get("1.6.3", 0)
            self.counters["1.6.3"] = idx + 1
            if idx < len(PHASE1_AGENT_DETAILS):
                return PHASE1_AGENT_DETAILS[idx][2]
            return "no"

        # Phase 2.1.1 - Agent prompt confirmations
        if step_id == "2.1.1":
            idx = self.counters.get("2.1.1", 0)
            self.counters["2.1.1"] = idx + 1
            if idx < len(AGENT_PROMPT_CONFIRMS):
                return AGENT_PROMPT_CONFIRMS[idx]
            return "Confirmed."

        # Phase 2.2.x - Round instructions (keyed by round)
        if step_id.startswith("2.2."):
            round_num = self.current_round
            if round_num in ROUND_ANSWERS and step_id in ROUND_ANSWERS[round_num]:
                return ROUND_ANSWERS[round_num][step_id]
            return f"Answer for {step_id} round {round_num}"

        # Phase 2.3.x - Helpers
        if step_id in PHASE2_3_ANSWERS:
            return PHASE2_3_ANSWERS[step_id]

        # Phase 3
        if step_id in PHASE3_ANSWERS:
            return PHASE3_ANSWERS[step_id]

        return f"[Auto-answer for {step_id}]"


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Use mock client (default)")
    parser.add_argument("--base-url", help="vLLM server URL")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--max-steps", type=int, default=200, help="Maximum steps to run")
    args = parser.parse_args()

    print("=" * 70)
    print("FULL WORKFLOW TEST - All 3 Phases")
    print("=" * 70 + "\n")

    # Load runtime
    runtime_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "runtime-files")
    runtime = Runtime(
        os.path.join(runtime_path, "B42_Runtime_Phase1_Conceptualization.txt"),
        os.path.join(runtime_path, "B42_Runtime_Phase2_Drafting.txt"),
        os.path.join(runtime_path, "B42_Runtime_Phase3_Review.txt")
    )
    print(f"Loaded {len(runtime.steps)} workflow steps\n")

    # Create LLM client
    if args.base_url:
        print(f"Using vLLM: {args.base_url}")
        llm = create_llm_client("vllm", base_url=args.base_url, model=args.model)
    else:
        print("Using MOCK client\n")
        llm = create_llm_client("mock")

    # Load BIOS prompt
    bios_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bios_reduced_prompt.txt")
    with open(bios_path, 'r') as f:
        bios_prompt = f.read()

    handler = StudentInteractionHandler(llm, bios_prompt)
    answer_provider = FullWorkflowAnswerProvider()

    def get_input(prompt: str) -> str:
        return answer_provider.get_answer(prompt, orchestrator.current_step_id, orchestrator)

    orchestrator = WorkflowOrchestrator(
        runtime=runtime,
        student_handler=handler,
        starting_step="1.1",
        get_student_input=get_input
    )

    print("Starting full workflow...\n")
    print("-" * 70)

    step_count = 0
    phase_tracker = {"1": 0, "2": 0, "3": 0}

    try:
        while orchestrator.current_step_id and step_count < args.max_steps:
            step_count += 1
            current_phase = orchestrator.current_step_id[0]
            phase_tracker[current_phase] = phase_tracker.get(current_phase, 0) + 1

            print(f"\n--- Step {orchestrator.current_step_id} ({step_count}) ---")

            step = orchestrator.runtime.get_step(orchestrator.current_step_id)
            print(f"Target: {step.target}")

            success = orchestrator.execute_step(orchestrator.current_step_id)
            if not success:
                print(f"ERROR at {orchestrator.current_step_id}")
                break

            current_step = orchestrator.runtime.get_step(orchestrator.current_step_id)
            next_step = orchestrator.resolve_next_step(
                orchestrator.current_step_id,
                current_step.next_step
            )

            if next_step and next_step not in ["END", "DONE"]:
                print(f"-> Next: {next_step}")
                orchestrator.current_step_id = next_step
            else:
                print("-> WORKFLOW COMPLETE")
                break

    except KeyboardInterrupt:
        print("\n\nInterrupted")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

    # Summary
    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETE")
    print("=" * 70)
    print(f"Total steps: {step_count}")
    print(f"Phase 1: {phase_tracker.get('1', 0)} steps")
    print(f"Phase 2: {phase_tracker.get('2', 0)} steps")
    print(f"Phase 3: {phase_tracker.get('3', 0)} steps")

    # Compile canvas
    canvas = compile_canvas_from_student_state(orchestrator.student_state)
    orchestrator.canvas = canvas

    print(f"\nAgents created: {len(canvas.agents)}")
    print(f"Rounds defined: {len(canvas.rounds)}")
    print(f"Phase 1 complete: {canvas.status.phase1_complete}")

    # Save outputs
    state_path = os.path.join(OUTPUT_DIR, "full_workflow_state.json")
    doc_path = os.path.join(OUTPUT_DIR, "full_workflow_document.txt")

    orchestrator.save_state(state_path)

    final_doc = compile_final_document(canvas)
    with open(doc_path, "w") as f:
        f.write(final_doc)
    print(f"\nSaved: {state_path}, {doc_path}")


if __name__ == "__main__":
    main()
