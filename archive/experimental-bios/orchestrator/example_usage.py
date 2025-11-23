#!/usr/bin/env python3
"""
Example Usage - BIOS Orchestrator

This script demonstrates how to use the orchestrator in different modes:
1. Mock mode (no API calls) - for testing
2. OpenAI mode - with GPT-4
3. Anthropic mode - with Claude
4. Custom starting point (resume from specific step)
"""

import os
import sys
from llm_client import create_llm_client
from orchestrator import create_orchestrator


def load_bios_prompt() -> str:
    """Load the reduced BIOS prompt for orchestrator"""
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "bios_reduced_prompt.txt"
    )
    with open(prompt_path, 'r') as f:
        return f.read()


def run_mock_test():
    """Run a quick test with mock LLM (no API calls)"""
    print("=== Mock Test Mode ===\n")

    # Create mock LLM client
    llm = create_llm_client("mock")

    # Load BIOS prompt
    bios_prompt = load_bios_prompt()

    # Create orchestrator
    orchestrator = create_orchestrator(
        llm_client=llm,
        bios_prompt=bios_prompt,
        starting_step="1.1.1"
    )

    print("\nOrchestrator initialized successfully!")
    print(f"Current step: {orchestrator.current_step_id}")
    print("\nTo run the workflow, call: orchestrator.run_workflow()")
    print("(Not running in mock mode to avoid infinite loop)")

    return orchestrator


def run_with_openai(api_key: str, model: str = "gpt-4"):
    """Run with OpenAI GPT"""
    print(f"=== OpenAI Mode ({model}) ===\n")

    # Create OpenAI client
    llm = create_llm_client("openai", api_key=api_key, model=model)

    # Load BIOS prompt
    bios_prompt = load_bios_prompt()

    # Create orchestrator
    orchestrator = create_orchestrator(
        llm_client=llm,
        bios_prompt=bios_prompt,
        starting_step="1.1.1"
    )

    print("\nStarting workflow...")
    print("You will be asked questions step by step.")
    print("The orchestrator GUARANTEES no steps will be skipped.\n")

    # Run the workflow
    final_canvas = orchestrator.run_workflow()

    # Save final state
    orchestrator.save_state("workflow_final_state.json")

    print("\n=== Workflow Complete ===")
    print(f"Total steps completed: {len(orchestrator.get_student_answers())}")

    return orchestrator


def run_with_anthropic(api_key: str, model: str = "claude-3-5-sonnet-20241022"):
    """Run with Anthropic Claude"""
    print(f"=== Anthropic Mode ({model}) ===\n")

    # Create Anthropic client
    llm = create_llm_client("anthropic", api_key=api_key, model=model)

    # Load BIOS prompt
    bios_prompt = load_bios_prompt()

    # Create orchestrator
    orchestrator = create_orchestrator(
        llm_client=llm,
        bios_prompt=bios_prompt,
        starting_step="1.1.1"
    )

    print("\nStarting workflow...")
    print("You will be asked questions step by step.")
    print("The orchestrator GUARANTEES no steps will be skipped.\n")

    # Run the workflow
    final_canvas = orchestrator.run_workflow()

    # Save final state
    orchestrator.save_state("workflow_final_state.json")

    print("\n=== Workflow Complete ===")
    print(f"Total steps completed: {len(orchestrator.get_student_answers())}")

    return orchestrator


def run_from_checkpoint(step_id: str, provider: str = "mock", api_key: str = None):
    """Resume workflow from a specific step"""
    print(f"=== Resume from Step {step_id} ===\n")

    # Create LLM client
    llm = create_llm_client(provider, api_key=api_key)

    # Load BIOS prompt
    bios_prompt = load_bios_prompt()

    # Create orchestrator starting from specific step
    orchestrator = create_orchestrator(
        llm_client=llm,
        bios_prompt=bios_prompt,
        starting_step=step_id
    )

    print(f"Starting from step: {step_id}\n")

    if provider != "mock":
        # Run the workflow
        final_canvas = orchestrator.run_workflow()
        orchestrator.save_state(f"workflow_checkpoint_{step_id.replace('.', '_')}.json")

    return orchestrator


def interactive_mode():
    """Interactive mode - ask user which provider to use"""
    print("=== BIOS Orchestrator - Interactive Mode ===\n")
    print("Select LLM provider:")
    print("1. Mock (testing only, no API calls)")
    print("2. OpenAI (GPT-4)")
    print("3. Anthropic (Claude)")
    print("4. Exit")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        return run_mock_test()

    elif choice == "2":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = input("Enter OpenAI API key: ").strip()
        model = input("Model (default: gpt-4): ").strip() or "gpt-4"
        return run_with_openai(api_key, model)

    elif choice == "3":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            api_key = input("Enter Anthropic API key: ").strip()
        model = input("Model (default: claude-3-5-sonnet-20241022): ").strip() or "claude-3-5-sonnet-20241022"
        return run_with_anthropic(api_key, model)

    elif choice == "4":
        print("Exiting...")
        sys.exit(0)

    else:
        print("Invalid choice")
        return interactive_mode()


def demonstrate_step_parsing():
    """Demonstrate that the runtime parser correctly loads all steps"""
    print("=== Runtime Parser Demonstration ===\n")

    # Import directly
    from runtime_parser import Runtime

    # Load runtime files
    base_path = os.path.join(os.path.dirname(__file__), "..", "runtime-files")
    runtime = Runtime(
        f"{base_path}/B42_Runtime_Phase1_Conceptualization.txt",
        f"{base_path}/B42_Runtime_Phase2_Drafting.txt",
        f"{base_path}/B42_Runtime_Phase3_Review.txt"
    )

    print(f"Loaded {len(runtime.steps)} steps total\n")

    # Show some example steps
    example_steps = ["1.1.1", "2.2.6", "2.2.9", "3.1"]

    for step_id in example_steps:
        if step_id in runtime.steps:
            step = runtime.get_step(step_id)
            print(f"Step {step_id}:")
            print(f"  Target: {step.target}")
            print(f"  Required Output: {step.required_output}")
            print(f"  Next Step: {step.next_step}")
            if step.constraint:
                print(f"  Constraint: {step.constraint[:60]}...")
            print()

    # Verify Step 2.2.6 exists (the one that was skipped in testing)
    if "2.2.6" in runtime.steps:
        print("✓ Step 2.2.6 (Sequence) is present in runtime files")
        step = runtime.get_step("2.2.6")
        print(f"  Question: {step.required_output}")
    else:
        print("✗ Step 2.2.6 NOT FOUND (this would be a problem)")

    # Verify Step 2.2.9 exists (the platform config step that was hallucinated)
    if "2.2.9" in runtime.steps:
        print("\n✓ Step 2.2.9 (Platform Config) is present in runtime files")
        step = runtime.get_step("2.2.9")
        print(f"  Question: {step.required_output}")
    else:
        print("\n✗ Step 2.2.9 NOT FOUND (this would be a problem)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BIOS Orchestrator Example Usage")
    parser.add_argument(
        "--mode",
        choices=["interactive", "mock", "openai", "anthropic", "demo"],
        default="interactive",
        help="Execution mode"
    )
    parser.add_argument("--api-key", help="API key for OpenAI/Anthropic")
    parser.add_argument("--model", help="Model name")
    parser.add_argument("--start-step", default="1.1.1", help="Starting step ID")

    args = parser.parse_args()

    if args.mode == "demo":
        # Just demonstrate step parsing
        demonstrate_step_parsing()

    elif args.mode == "interactive":
        interactive_mode()

    elif args.mode == "mock":
        run_mock_test()

    elif args.mode == "openai":
        api_key = args.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OpenAI API key required (--api-key or OPENAI_API_KEY env var)")
            sys.exit(1)
        run_with_openai(api_key, args.model or "gpt-4")

    elif args.mode == "anthropic":
        api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: Anthropic API key required (--api-key or ANTHROPIC_API_KEY env var)")
            sys.exit(1)
        run_with_anthropic(api_key, args.model or "claude-3-5-sonnet-20241022")
