#!/usr/bin/env python3
"""
Test the Student Simulator with vLLM backend.

This script demonstrates how to use the StudentSimulator to autonomously
run through the RCM workflow with Qwen generating student responses.

Usage:
    # Quick test (5 steps only)
    python tests/test_simulator.py --base-url https://YOUR_NGROK_URL/v1 --steps 5

    # Full Phase 1 test
    python tests/test_simulator.py --base-url https://YOUR_NGROK_URL/v1 --steps 30

    # Full workflow (112 steps) - takes a while!
    python tests/test_simulator.py --base-url https://YOUR_NGROK_URL/v1 --full
"""

import os
import sys
import argparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from llm_client import create_llm_client, StudentSimulator
from orchestrator import create_orchestrator
from canvas_state import compile_final_document


def run_simulator_test(base_url: str, model: str, max_steps: int = 5):
    """
    Run the student simulator test.

    Args:
        base_url: vLLM server URL (e.g., https://xxxx.ngrok.io/v1)
        model: Model name on the vLLM server
        max_steps: Maximum number of steps to run (for testing)
    """
    print("=" * 60)
    print("STUDENT SIMULATOR TEST")
    print("=" * 60)
    print(f"vLLM URL: {base_url}")
    print(f"Model: {model}")
    print(f"Max steps: {max_steps}")
    print("=" * 60)

    # Create vLLM client
    print("\n1. Creating vLLM client...")
    vllm_client = create_llm_client(
        provider="vllm",
        base_url=base_url,
        model=model
    )

    # Create student simulator
    print("2. Creating student simulator...")
    simulator = StudentSimulator(vllm_client)

    # Test a single response first
    print("\n3. Testing single response...")
    test_question = "What theoretical tension would you like to explore in your simulation?"
    print(f"   Question: {test_question}")
    response = simulator.respond(test_question)
    print(f"   Response: {response}")

    if not response or len(response) < 10:
        print("\n❌ ERROR: Simulator not generating good responses")
        print("   Check your vLLM server and model.")
        return False

    print("\n✓ Single response test passed!")

    # Reset for full test
    simulator.reset()

    # Create orchestrator with simulator
    print("\n4. Creating orchestrator...")

    # Load BIOS prompt
    bios_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bios_reduced_prompt.txt")
    with open(bios_path, 'r') as f:
        bios_prompt = f.read()

    orchestrator = create_orchestrator(
        llm_client=vllm_client,  # Used for validation
        bios_prompt=bios_prompt,
        starting_step="1.1"  # Runtime uses 1.1, not 1.1.1
    )

    # Override input function with simulator
    orchestrator.get_student_input = simulator.get_input_function()

    # Run limited steps
    print(f"\n5. Running {max_steps} steps with simulated student...")
    print("-" * 60)

    step_count = 0
    while orchestrator.current_step_id is not None and step_count < max_steps:
        step_count += 1
        print(f"\n--- Step {orchestrator.current_step_id} ({step_count}/{max_steps}) ---")

        success = orchestrator.execute_step(orchestrator.current_step_id)

        if not success:
            print(f"❌ Failed at step {orchestrator.current_step_id}")
            break

        # Get next step
        current_step = orchestrator.runtime.get_step(orchestrator.current_step_id)
        raw_next_step = current_step.next_step
        next_step_id = orchestrator.resolve_next_step(orchestrator.current_step_id, raw_next_step)

        if next_step_id == "END" or next_step_id == "DONE":
            next_step_id = None

        if next_step_id:
            print(f"✓ {orchestrator.current_step_id} → {next_step_id}")

        orchestrator.current_step_id = next_step_id

    # Results
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print(f"Steps executed: {step_count}")
    print(f"Student answers collected: {len(orchestrator.student_state)}")

    # Show collected answers
    print("\nCollected Answers:")
    for step_id, answer in list(orchestrator.student_state.items())[:10]:
        if not step_id.startswith("current_"):
            answer_preview = str(answer)[:80] + "..." if len(str(answer)) > 80 else str(answer)
            print(f"  {step_id}: {answer_preview}")

    if len(orchestrator.student_state) > 10:
        print(f"  ... and {len(orchestrator.student_state) - 10} more")

    # Save output
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Save state
    state_file = os.path.join(output_dir, "simulator_test_state.json")
    orchestrator.save_state(state_file)
    print(f"\nState saved to: {state_file}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Test Student Simulator with vLLM")
    parser.add_argument("--base-url", required=True, help="vLLM server URL (e.g., https://xxxx.ngrok.io/v1)")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct", help="Model name")
    parser.add_argument("--steps", type=int, default=5, help="Number of steps to test (default: 5)")
    parser.add_argument("--full", action="store_true", help="Run full 112-step workflow")

    args = parser.parse_args()

    max_steps = 112 if args.full else args.steps

    success = run_simulator_test(args.base_url, args.model, max_steps)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
