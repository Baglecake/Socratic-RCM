#!/usr/bin/env python3
"""
Auto-test script - runs through first few steps with pre-defined answers
"""
import os
import sys

# Add local_rcm to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from llm_client import create_llm_client, StudentInteractionHandler
from runtime_parser import Runtime
from canvas_state import CanvasState
from orchestrator import WorkflowOrchestrator

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")

# Pre-defined answers for testing
TEST_ANSWERS = [
    "yes",  # 1.1 - Have you completed storyboard?
    "A",    # 1.2.1 - Theoretical option
    "I want to model how structural power shapes worker agency and whether cooperation or resistance emerges under constraint.",  # 1.2.2
    "Alienation is when workers lose control over their labor. It shows up as mechanical compliance and withdrawal.",  # 1.2.3
    "Non-domination focuses on vulnerability to arbitrary power, not internal estrangement like alienation.",  # 1.2.4
    "Single multi-round design with baseline and experiment in one simulation.",  # 1.2.5
    "A - Modify one variable",  # 1.2.6
    "Yes, this aligns with KB[2] testing A vs B.",  # CHECKPOINT 1.2
    "The baseline starts with full managerial control where workers have no input over their labor.",  # 1.3.1
    "The experiment adds a safeguard limiting arbitrary power, like requiring justification for orders.",  # 1.3.2A
    "This tests A vs B by showing baseline alienation then measuring change when domination is reduced.",  # 1.3.3
    "Yes, baseline vs experiment tests the theoretical tension.",  # CHECKPOINT 1.3
    "A small workshop where the owner controls all tasks. Power dynamics are visible in every interaction.",  # 1.4.1
    "3",  # 1.4.2 - Number of rounds
    "Baseline Alienation - observe behavior under full control.",  # 1.4.3 Round 1
    "Reduced Domination - add safeguard and observe changes.",  # 1.4.3 Round 2
    "Comparative Analysis - review patterns across conditions.",  # 1.4.3 Round 3
]

answer_index = 0

def get_test_answer(prompt: str) -> str:
    """Return pre-defined answers"""
    global answer_index
    if answer_index < len(TEST_ANSWERS):
        answer = TEST_ANSWERS[answer_index]
        answer_index += 1
        print(f"> {answer}")
        return answer
    else:
        print("> [END OF TEST ANSWERS]")
        return "test complete"

def main():
    print("=== Auto-Test Mode ===\n")

    # Load runtime files
    runtime_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "runtime-files")
    runtime = Runtime(
        os.path.join(runtime_path, "B42_Runtime_Phase1_Conceptualization.txt"),
        os.path.join(runtime_path, "B42_Runtime_Phase2_Drafting.txt"),
        os.path.join(runtime_path, "B42_Runtime_Phase3_Review.txt")
    )
    print(f"Loaded {len(runtime.steps)} steps\n")

    # Create mock LLM (no API calls)
    llm = create_llm_client("mock")

    # Load BIOS prompt
    bios_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bios_reduced_prompt.txt")
    with open(bios_path, 'r') as f:
        bios_prompt = f.read()

    # Create handler
    handler = StudentInteractionHandler(llm, bios_prompt)

    # Create orchestrator with our auto-answer function
    orchestrator = WorkflowOrchestrator(
        runtime=runtime,
        student_handler=handler,
        starting_step="1.1",
        get_student_input=get_test_answer
    )

    print("Starting auto-test (will stop after pre-defined answers)...\n")

    try:
        # Run until we run out of answers
        step_count = 0
        max_steps = len(TEST_ANSWERS) + 2  # A few extra for safety

        while orchestrator.current_step_id and step_count < max_steps:
            step_count += 1
            print(f"\n--- Step {orchestrator.current_step_id} ({step_count}) ---")

            step = orchestrator.runtime.get_step(orchestrator.current_step_id)
            print(f"Target: {step.target}")

            success = orchestrator.execute_step(orchestrator.current_step_id)

            if not success:
                print(f"ERROR at step {orchestrator.current_step_id}")
                break

            # Get next step
            current_step = orchestrator.runtime.get_step(orchestrator.current_step_id)
            next_step = orchestrator.resolve_next_step(orchestrator.current_step_id, current_step.next_step)

            if next_step and next_step not in ["END", "DONE"]:
                print(f"-> Advancing: {orchestrator.current_step_id} -> {next_step}")
                orchestrator.current_step_id = next_step
            else:
                print(f"-> Workflow complete at {orchestrator.current_step_id}")
                break

    except Exception as e:
        print(f"\nTest stopped: {e}")

    print(f"\n=== Test Complete ===")
    print(f"Steps executed: {step_count}")
    print(f"Answers used: {answer_index}")
    print(f"Final step: {orchestrator.current_step_id}")

    # Show collected state
    print(f"\nCollected answers:")
    for k, v in orchestrator.student_state.items():
        if not k.startswith("current_"):
            val_str = str(v)[:60] + "..." if len(str(v)) > 60 else str(v)
            print(f"  {k}: {val_str}")

if __name__ == "__main__":
    main()
