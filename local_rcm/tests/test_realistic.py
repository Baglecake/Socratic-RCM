#!/usr/bin/env python3
"""
Realistic test - simulates a student working through the full workflow
Uses vLLM for validation (if available) or mock
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

# Realistic student answers - like a grad student working on Marx/alienation project
STUDENT_ANSWERS = {
    # Phase 1.1 - Welcome
    "1.1": "yes",

    # Phase 1.2 - Theoretical Framework
    "1.2.1": "A",  # Option A from KB[2]
    "1.2.2": "I want to model how workers lose control over their labor and how that shapes their decisions and relationships. The tension is whether agents can coordinate or resist when their agency is structurally suppressed.",
    "1.2.3": "Alienation is when workers become separated from their creative capacities because production treats their labor as owned by someone else. It manifests as mechanical compliance, withdrawal, and decisions driven by survival rather than self-expression.",
    "1.2.4": "Non-domination focuses on vulnerability to arbitrary power rather than internal estrangement. The harm isn't disconnection from labor but exposure to unchecked authority. Workers may feel their work is meaningful but still fear unpredictable interference.",
    "1.2.5": "Single multi-round design - baseline and experiment in one simulation. This lets me see how agents behave under pure alienation first, then observe how introducing a non-domination variable changes the dynamic.",
    "1.2.6": "A - Modify one variable. Since I want to isolate how alienation differs from non-domination, changing just one structural variable makes it clear whether behavior shifts come from that specific intervention.",
    "CHECKPOINT 1.2": "Yes, this aligns with KB[2]. The single-variable modification creates a controlled contrast between alienation and non-domination conditions.",

    # Phase 1.3 - Experiment Design
    "1.3.1": "The baseline is a workplace where the owner controls every aspect - task assignments, timing, workflow. Workers have no input. This reflects Marx because their labor feels imposed rather than self-generated.",
    "1.3.2A": "The experiment introduces one structural safeguard that limits arbitrary power - requiring justification for task changes or giving workers a protected input channel. This shifts toward non-domination while keeping everything else constant.",
    "1.3.3": "The baseline shows how workers behave under pure alienation with no control. The experiment adds protection against arbitrary power. Comparing them reveals whether changes stem from reduced alienation or reduced vulnerability to authority.",
    "CHECKPOINT 1.3": "Yes - the baseline expresses alienation under full control, the experiment tests non-domination by reducing arbitrary power. The contrast directly tests the theoretical tension.",

    # Phase 1.4 - Setting and Rounds
    "1.4.1": "A small manufacturing workshop with low ceilings and humming machines. Workstations are fixed for repetitive tasks. The owner's office overlooks the floor from a raised platform, making power visible in every interaction. The cramped space reinforces isolation.",
    "1.4.2": "3",
    "1.4.3_1": "Baseline Alienation: Observe how workers act when they have no control over their labor and the owner directs everything. Establishes pure alienation dynamics.",
    "1.4.3_2": "Reduced Domination: Introduce a safeguard limiting arbitrary power. Observe whether participation increases when workers aren't vulnerable to unpredictable authority.",
    "1.4.3_3": "Comparative Analysis: Review transcripts from both rounds to identify behavioral shifts. Determine which theory better explains the patterns.",
    "CHECKPOINT 1.4": "Yes, the progression tests the hypothesis - baseline alienation, then intervention, then analysis of which framework explains the changes.",

    # Phase 1.5 - Agents
    "1.5.1": "4",
    "1.5.2_1": "Worker+Alice",
    "1.5.3_1": "Human",
    "1.5.2_2": "Worker+Ben",
    "1.5.3_2": "Human",
    "1.5.2_3": "Owner+Marta",
    "1.5.3_3": "Human",
    "1.5.2_4": "Analyst+Reporter",
    "1.5.3_4": "Human",
    "CHECKPOINT 1.5": "Yes - Worker+Alice and Worker+Ben represent those experiencing alienation/domination. Owner+Marta represents the source of control. Analyst+Reporter evaluates the theoretical claims.",

    # Phase 1.6 - Agent Details
    "1.6.1_1": "Alice's goal is to gain more influence over how her work is organized. In the baseline, alienation prevents this. In the experiment, progress shows whether reduced arbitrary power enables participation.",
    "1.6.2_1": "Alice is thoughtful but hesitant, often suppressing ideas because she assumes her input won't matter. She follows directives to avoid conflict. When given protected input channels, she becomes more confident.",
    "1.6.3_1": "no",

    "1.6.1_2": "Ben's goal is to secure predictable, fair treatment. In the baseline, arbitrary orders create anxiety. In the experiment, he should show less resistance if domination is reduced.",
    "1.6.2_2": "Ben is practical and prefers routine. He follows instructions unless they feel arbitrary, which triggers pushback. His decisions prioritize stability and consistent treatment.",
    "1.6.3_2": "no",

    "1.6.1_3": "Marta's goal is maintaining productivity while asserting authority. In the baseline, she expects compliance. In the experiment, limiting her discretion may force more justification and negotiation.",
    "1.6.2_3": "Marta is confident and directive, making quick decisions without explanation. She handles conflict by tightening control. Under constraints, she becomes more methodical.",
    "1.6.3_3": "yes - If worker questions: assert stronger control. If workers comply: maintain brisk directive style.",

    "1.6.1_4": "The Analyst's goal is identifying clear behavioral differences between conditions and attributing them to alienation or non-domination. Success is measured by accurate theoretical attribution.",
    "1.6.2_4": "The Analyst is precise and detached, focusing only on empirical patterns. Never participates in the simulation, only observes and reports.",
    "1.6.3_4": "no",

    # Phase 1.7-1.8
    "1.7": "Self-Reflections and Analyst agent for Round 3.",
    "1.8": "Section 1 complete - theoretical framework established with alienation vs non-domination contrast, 3-round design, 4 agents defined.",
}

class RealisticAnswerProvider:
    """Provides realistic answers based on step context"""

    def __init__(self):
        self.step_counts = {}  # Track iterations for looping steps
        self.answers_given = []

    def get_answer(self, prompt: str, step_id: str, orchestrator) -> str:
        """Get realistic answer for current step"""

        # Handle looping steps
        if step_id == "1.4.3":
            count = self.step_counts.get("1.4.3", 0) + 1
            self.step_counts["1.4.3"] = count
            key = f"1.4.3_{count}"
        elif step_id == "1.5.2":
            count = self.step_counts.get("1.5.2", 0) + 1
            self.step_counts["1.5.2"] = count
            key = f"1.5.2_{count}"
        elif step_id == "1.5.3":
            count = self.step_counts.get("1.5.3", 0) + 1
            self.step_counts["1.5.3"] = count
            key = f"1.5.3_{count}"
        elif step_id == "1.6.1":
            count = self.step_counts.get("1.6.1", 0) + 1
            self.step_counts["1.6.1"] = count
            key = f"1.6.1_{count}"
        elif step_id == "1.6.2":
            count = self.step_counts.get("1.6.2", 0) + 1
            self.step_counts["1.6.2"] = count
            key = f"1.6.2_{count}"
        elif step_id == "1.6.3":
            count = self.step_counts.get("1.6.3", 0) + 1
            self.step_counts["1.6.3"] = count
            key = f"1.6.3_{count}"
        else:
            key = step_id

        answer = STUDENT_ANSWERS.get(key, f"[No answer for {key}]")
        self.answers_given.append((step_id, key, answer[:50]))

        # Simulate typing delay
        time.sleep(0.3)

        print(f"> {answer}")
        return answer


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", help="vLLM server URL")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--mock", action="store_true", help="Use mock client")
    args = parser.parse_args()

    print("=" * 60)
    print("REALISTIC STUDENT SIMULATION")
    print("Project: Alienation vs Non-Domination in Worker Agency")
    print("=" * 60 + "\n")

    # Load runtime
    runtime_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "runtime-files")
    runtime = Runtime(
        os.path.join(runtime_path, "B42_Runtime_Phase1_Conceptualization.txt"),
        os.path.join(runtime_path, "B42_Runtime_Phase2_Drafting.txt"),
        os.path.join(runtime_path, "B42_Runtime_Phase3_Review.txt")
    )
    print(f"Loaded {len(runtime.steps)} workflow steps\n")

    # Create LLM client
    if args.mock or not args.base_url:
        print("Using MOCK client (no API calls)\n")
        llm = create_llm_client("mock")
    else:
        print(f"Using vLLM: {args.base_url}")
        print(f"Model: {args.model}\n")
        llm = create_llm_client("vllm", base_url=args.base_url, model=args.model)

    # Load BIOS prompt
    bios_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bios_reduced_prompt.txt")
    with open(bios_path, 'r') as f:
        bios_prompt = f.read()

    handler = StudentInteractionHandler(llm, bios_prompt)
    answer_provider = RealisticAnswerProvider()

    def get_input(prompt: str) -> str:
        return answer_provider.get_answer(prompt, orchestrator.current_step_id, orchestrator)

    orchestrator = WorkflowOrchestrator(
        runtime=runtime,
        student_handler=handler,
        starting_step="1.1",
        get_student_input=get_input
    )

    print("Starting simulation...\n")
    print("-" * 60)

    try:
        step_count = 0
        max_steps = 50  # Safety limit

        while orchestrator.current_step_id and step_count < max_steps:
            step_count += 1

            # Stop at Phase 2 for this test
            if orchestrator.current_step_id.startswith("2."):
                print(f"\n{'=' * 60}")
                print("PHASE 1 COMPLETE - Stopping before Phase 2")
                print("=" * 60)
                break

            print(f"\n--- Step {orchestrator.current_step_id} ({step_count}) ---")

            step = orchestrator.runtime.get_step(orchestrator.current_step_id)
            print(f"Target: {step.target}")

            success = orchestrator.execute_step(orchestrator.current_step_id)

            if not success:
                print(f"ERROR at step {orchestrator.current_step_id}")
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
                print("-> Workflow section complete")
                break

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

    # Summary
    print("\n" + "=" * 60)
    print("SIMULATION SUMMARY")
    print("=" * 60)
    print(f"Steps completed: {step_count}")
    print(f"Final position: {orchestrator.current_step_id}")

    # Compile canvas from student state
    print("\n" + "=" * 60)
    print("COMPILING CANVAS FROM STUDENT STATE...")
    print("=" * 60)

    canvas = compile_canvas_from_student_state(orchestrator.student_state)
    orchestrator.canvas = canvas  # Update orchestrator's canvas

    # Show canvas structure
    print("\n--- PROJECT ---")
    print(f"Goal: {canvas.project.goal[:80]}..." if len(canvas.project.goal) > 80 else f"Goal: {canvas.project.goal}")
    print(f"Framework: {canvas.project.theoretical_option_label}")
    print(f"Concept A: {canvas.project.concept_a.definition[:60]}..." if canvas.project.concept_a else "")
    print(f"Concept B: {canvas.project.concept_b.definition[:60]}..." if canvas.project.concept_b else "")
    print(f"Setting: {canvas.project.setting[:60]}...")
    print(f"Rounds: {canvas.project.rounds_count}")

    print("\n--- AGENTS ---")
    for agent in canvas.agents:
        print(f"  {agent.identifier}: {agent.goal[:50]}...")

    print("\n--- ROUNDS ---")
    for round_def in canvas.rounds:
        print(f"  Round {round_def.round_number}: {round_def.scenario[:50]}...")

    print("\n--- HELPERS ---")
    if canvas.helpers.self_reflection_prompts:
        print(f"  Self-Reflection: {canvas.helpers.self_reflection_prompts}")
    if canvas.helpers.analyst_function:
        print(f"  Analyst: {canvas.helpers.analyst_function}")

    print(f"\n--- STATUS ---")
    print(f"  Phase 1 Complete: {canvas.status.phase1_complete}")

    # Save state with updated canvas
    state_path = os.path.join(OUTPUT_DIR, "test_realistic_state.json")
    doc_path = os.path.join(OUTPUT_DIR, "test_realistic_document.txt")

    orchestrator.save_state(state_path)

    # Also save the compiled document
    print("\n" + "=" * 60)
    print("FINAL DOCUMENT PREVIEW")
    print("=" * 60)
    final_doc = compile_final_document(canvas)
    print(final_doc[:2000])
    if len(final_doc) > 2000:
        print(f"\n... [{len(final_doc) - 2000} more characters]")

    # Save full document
    with open(doc_path, "w") as f:
        f.write(final_doc)
    print(f"\nFull document saved to: {doc_path}")


if __name__ == "__main__":
    main()
