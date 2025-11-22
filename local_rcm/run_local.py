#!/usr/bin/env python3
"""
Local Socratic-RCM Launcher
Runs the BIOS Orchestrator using a local Ollama model.
"""

import os
import sys
import argparse
from llm_client import create_llm_client
from orchestrator import create_orchestrator

def load_bios_prompt() -> str:
    """Load the reduced BIOS prompt for orchestrator"""
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "bios_reduced_prompt.txt"
    )
    try:
        with open(prompt_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Could not find bios_reduced_prompt.txt at {prompt_path}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Run Socratic-RCM locally with Ollama")
    parser.add_argument("--model", default="gemma:2b", help="Ollama model to use (default: gemma:2b)")
    parser.add_argument("--url", default="http://localhost:11434", help="Ollama API URL")
    parser.add_argument("--start-step", default="1.1", help="Step ID to start from")
    
    args = parser.parse_args()
    
    print(f"=== Socratic-RCM Local (Model: {args.model}) ===\n")
    
    # check if requests is installed
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library is missing.")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)

    # Create Ollama client
    try:
        llm = create_llm_client("ollama", model=args.model, base_url=args.url)
        # Test connection
        print(f"Connecting to Ollama at {args.url}...")
        llm.send_message("system", "ping")
        print("✓ Connected to Ollama")
    except Exception as e:
        print(f"\nError connecting to Ollama: {e}")
        print("Make sure Ollama is running (usually 'ollama serve')")
        print(f"And that you have pulled the model: 'ollama pull {args.model}'")
        sys.exit(1)

    # Load BIOS prompt
    bios_prompt = load_bios_prompt()

    # Create orchestrator
    try:
        orchestrator = create_orchestrator(
            llm_client=llm,
            bios_prompt=bios_prompt,
            starting_step=args.start_step,
            runtime_base_path=os.path.join(os.path.dirname(__file__), "runtime-files")
        )
    except Exception as e:
        print(f"Error initializing orchestrator: {e}")
        sys.exit(1)

    print("\nStarting workflow...")
    print("You will be asked questions step by step.")
    print("Press Ctrl+C to exit at any time.\n")

    try:
        # Run the workflow
        final_canvas = orchestrator.run_workflow()
        
        # Save final state
        output_file = "workflow_final_state.json"
        orchestrator.save_state(output_file)
        print(f"\n✓ Workflow saved to {output_file}")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        # Save checkpoint
        orchestrator.save_state("workflow_checkpoint.json")
    except Exception as e:
        print(f"\nRuntime Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
