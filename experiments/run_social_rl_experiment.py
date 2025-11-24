#!/usr/bin/env python3
"""
Social RL Experiment Runner

Demonstrates the Social RL framework with:
- Dual-LLM Coach/Performer architecture
- PRAR-based reasoning guidance
- Social feedback extraction
- Policy adaptation across rounds

This script runs a baseline experiment to showcase how agents learn through
social interaction, guided by process retrieval, without explicit reward functions.

Usage:
    python experiments/run_social_rl_experiment.py --model qwen2.5:7b --rounds 1
    python experiments/run_social_rl_experiment.py --help
"""

import sys
import json
import argparse
import datetime
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import llm_client directly to avoid module __init__.py issues
import importlib.util
llm_spec = importlib.util.spec_from_file_location(
    "llm_client",
    str(PROJECT_ROOT / "local_rcm" / "llm_client.py")
)
llm_module = importlib.util.module_from_spec(llm_spec)
llm_spec.loader.exec_module(llm_module)

OllamaClient = llm_module.OllamaClient
OpenAIClient = llm_module.OpenAIClient
MockClient = llm_module.MockClient
create_llm_client = llm_module.create_llm_client


class DualLLMCompatibleClient:
    """
    Wrapper that makes standard LLM clients compatible with DualLLMClient.

    Adds temperature and max_tokens parameters to send_message calls.
    """

    def __init__(self, client, default_temperature: float = 0.7):
        self._client = client
        self._default_temperature = default_temperature
        self._calls = []

    def send_message(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = None,
        max_tokens: int = 512
    ) -> str:
        """Send message with optional temperature override."""
        # Track the call for analysis
        self._calls.append({
            "temperature": temperature or self._default_temperature,
            "max_tokens": max_tokens,
            "prompt_length": len(system_prompt) + len(user_message)
        })

        # Most local models don't support temperature per-call,
        # but we can still route through the client
        return self._client.send_message(system_prompt, user_message)

    @property
    def call_log(self):
        return self._calls


def create_experiment_canvas() -> dict:
    """
    Create a minimal canvas for experiment demonstration.

    This is a simplified version for quick testing. For full experiments,
    use the canvas from prar/outputs/*/state.json files.
    """
    return {
        "project": {
            "goal": "Demonstrate Social RL learning through workplace interaction",
            "theoretical_option": "A",
            "theoretical_option_label": "Class Conflict / Alienation",
            "concept_a": {
                "name": "Alienation",
                "definition": "Workers become separated from their creative capacities because production treats their labor as owned by someone else."
            },
            "concept_b": {
                "name": "Non-domination",
                "definition": "Vulnerability to arbitrary power rather than internal estrangement."
            },
            "setting": "A small manufacturing workshop with humming machines. The owner's office overlooks the floor from a raised platform."
        },
        "agents": [
            {
                "identifier": "Worker+Alice",
                "goal": "Gain more influence over how her work is organized",
                "persona": "Alice is thoughtful but hesitant, often suppressing ideas because she assumes her input won't matter.",
                "prompt": "ROLE: You are Worker+Alice\nPERSONA: Alice is thoughtful but hesitant. She follows directives to avoid conflict."
            },
            {
                "identifier": "Worker+Ben",
                "goal": "Secure predictable, fair treatment",
                "persona": "Ben is practical and prefers routine. He follows instructions unless they feel arbitrary.",
                "prompt": "ROLE: You are Worker+Ben\nPERSONA: Ben is practical and prefers routine. Arbitrary orders trigger pushback."
            },
            {
                "identifier": "Owner+Marta",
                "goal": "Maintain productivity while asserting authority",
                "persona": "Marta is confident and directive, making quick decisions without explanation.",
                "prompt": "ROLE: You are Owner+Marta\nPERSONA: Confident and directive. Handles conflict by tightening control.",
                "behaviors": {
                    "raw": "If worker questions: assert stronger control. If workers comply: maintain brisk directive style."
                }
            }
        ],
        "rounds": [
            {
                "round_number": 1,
                "scenario": "Baseline Alienation: Workers have no control over their labor. The owner directs everything without explanation.",
                "concept_a_manifestation": "Alienation manifests as complete separation from decision-making. Workers execute tasks without understanding purpose.",
                "concept_b_manifestation": "Non-domination is absent - arbitrary power is unchecked.",
                "rules": "Workers CAN: complete assigned tasks, request clarification. Workers CANNOT: suggest changes, refuse orders, negotiate.",
                "tasks": "Complete one production cycle. Marta assigns tasks. Observe compliance patterns.",
                "sequence": "Marta assigns tasks, workers comply silently. Any hesitation triggers reassertion of control.",
                "platform_config": {
                    "participants": "Worker+Alice, Worker+Ben, Owner+Marta",
                    "who_sends": "All",
                    "order": "Default",
                    "end_condition": "Total messages: 9"
                }
            }
        ]
    }


def load_canvas_from_state(state_path: str) -> dict:
    """Load canvas from an existing state.json file."""
    with open(state_path, 'r') as f:
        state = json.load(f)
    return state.get("canvas", state)


def run_experiment(
    model: str = "qwen2.5:7b",
    provider: str = "ollama",
    rounds: int = 1,
    max_turns: int = 9,
    use_dual_llm: bool = True,
    state_path: Optional[str] = None,
    verbose: bool = True,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    experiment_id: Optional[str] = None
) -> dict:
    """
    Run a Social RL experiment.

    Args:
        model: Model name to use
        provider: LLM provider (ollama, mock, openai, vllm)
        rounds: Number of rounds to run
        max_turns: Maximum turns per round
        use_dual_llm: Whether to use Dual-LLM Coach/Performer architecture
        state_path: Optional path to state.json with pre-configured canvas
        verbose: Print progress
        base_url: Base URL for vLLM/RunPod endpoint
        api_key: API key for vLLM/RunPod
        experiment_id: Custom experiment ID (auto-generated if not provided)

    Returns:
        Experiment results dict
    """
    from social_rl.runner import SocialRLRunner, SocialRLConfig
    from social_rl.dual_llm_client import DualLLMClient, DualLLMConfig

    print("=" * 60)
    print("SOCIAL RL EXPERIMENT")
    print("=" * 60)
    print(f"Model: {model}")
    print(f"Provider: {provider}")
    print(f"Rounds: {rounds}")
    print(f"Dual-LLM: {'enabled' if use_dual_llm else 'disabled'}")
    print("=" * 60)

    # Generate experiment ID if not provided
    import os
    import subprocess
    if not experiment_id:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        experiment_id = f"social_rl_{timestamp}"

    # Get git commit hash for reproducibility
    try:
        git_commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=PROJECT_ROOT,
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        git_commit = "unknown"

    # Create LLM client
    effective_api_key = api_key or os.environ.get("RUNPOD_API_KEY") or os.environ.get("OPENAI_API_KEY")

    if provider == "mock":
        base_client = MockClient()
        print("\n[Using MockClient for testing - no actual LLM calls]\n")
    elif provider == "ollama":
        print(f"\nConnecting to Ollama ({model})...")
        base_client = OllamaClient(model=model)
    elif provider == "vllm":
        if not base_url:
            base_url = os.environ.get("OPENAI_BASE_URL")
        if not base_url:
            raise ValueError("--base-url required for vLLM provider (or set OPENAI_BASE_URL env var)")
        print(f"\nConnecting to vLLM endpoint: {base_url}")
        print(f"Model: {model}")
        base_client = OpenAIClient(
            api_key=effective_api_key or "not-needed",
            model=model,
            base_url=base_url,
            timeout=180.0  # Longer timeout for serverless cold starts
        )
    elif provider == "openai":
        if not effective_api_key:
            raise ValueError("--api-key or OPENAI_API_KEY environment variable required")
        base_client = OpenAIClient(api_key=effective_api_key, model=model, base_url=base_url)
    else:
        base_client = create_llm_client(provider, model=model)

    # Wrap client for DualLLM compatibility
    wrapped_client = DualLLMCompatibleClient(base_client)

    # Create Dual-LLM client if enabled
    dual_llm = None
    if use_dual_llm:
        dual_config = DualLLMConfig(
            performer_temperature=0.7,
            coach_temperature=0.1,
            log_coach_critiques=True,
            max_validation_retries=1
        )
        dual_llm = DualLLMClient(
            performer_client=wrapped_client,
            coach_client=wrapped_client,
            config=dual_config
        )
        print("Dual-LLM Client configured (Coach + Performer)\n")

    # Load or create canvas
    if state_path:
        print(f"Loading canvas from: {state_path}")
        canvas = load_canvas_from_state(state_path)
    else:
        print("Using demonstration canvas")
        canvas = create_experiment_canvas()

    # Configure runner
    config = SocialRLConfig(
        manifestation_mode="progressive",
        use_prar_cues=True,
        prar_intensity="medium",
        use_coach_validation=use_dual_llm,
        verbose=verbose,
        auto_save=True
    )

    # Create runner
    runner = SocialRLRunner(
        canvas=canvas,
        llm_client=wrapped_client,
        config=config,
        dual_llm_client=dual_llm,
        experiment_id=experiment_id
    )

    # Execute rounds
    results = []
    for round_num in range(1, min(rounds + 1, len(canvas.get("rounds", [])) + 1)):
        print(f"\n{'='*60}")
        print(f"EXECUTING ROUND {round_num}")
        print(f"{'='*60}\n")

        try:
            result = runner.execute_round(round_num, max_turns=max_turns)
            results.append(result)
        except Exception as e:
            print(f"Error in round {round_num}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Generate report
    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETE")
    print("=" * 60)

    report = runner.generate_report()
    print(report)

    # Build standardized meta block
    meta = {
        "experiment_id": experiment_id,
        "framework": canvas.get("project", {}).get("theoretical_option_label", "Unknown"),
        "framework_option": canvas.get("project", {}).get("theoretical_option", "A"),
        "model": model,
        "provider": provider,
        "backend": f"{provider}" + (f" ({base_url})" if base_url else ""),
        "performer_temperature": 0.7 if use_dual_llm else None,
        "coach_temperature": 0.1 if use_dual_llm else None,
        "dual_llm_enabled": use_dual_llm,
        "rounds_executed": len(results),
        "max_turns_per_round": max_turns,
        "git_commit": git_commit,
        "social_rl_version": "0.2.0",
        "prar_state_file": state_path,
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Save meta.json
    if results and runner.output_dir:
        meta_path = runner.output_dir / "meta.json"
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        print(f"  [SAVED] {meta_path}")

    # Compute and save metrics.json
    metrics = None
    if results and runner.output_dir:
        try:
            from social_rl.metrics import compute_experiment_metrics
            metrics = compute_experiment_metrics(results)
            metrics_path = runner.output_dir / "metrics.json"
            with open(metrics_path, "w") as f:
                json.dump(metrics, f, indent=2)
            print(f"  [SAVED] {metrics_path}")

            # Print summary
            summary = metrics.get("summary", {})
            if summary.get("key_observations"):
                print("\n  Metrics Summary:")
                for obs in summary["key_observations"]:
                    print(f"    - {obs}")
        except Exception as e:
            print(f"  [METRICS WARNING] Could not compute metrics: {e}")

    # Save final results
    if results:
        print(f"\nResults saved to: {runner.output_dir}")

    return {
        "meta": meta,
        "results": [r.to_dict() for r in results],
        "metrics": metrics,
        "report": report,
        "output_dir": str(runner.output_dir),
        "llm_calls": wrapped_client.call_log
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run a Social RL experiment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick test with mock client (no LLM needed)
  python experiments/run_social_rl_experiment.py --provider mock

  # Run with local Ollama model
  python experiments/run_social_rl_experiment.py --model qwen2.5:7b

  # Run with RunPod vLLM endpoint
  python experiments/run_social_rl_experiment.py \\
    --provider vllm \\
    --base-url https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1 \\
    --model Qwen/Qwen2.5-7B-Instruct \\
    --api-key YOUR_RUNPOD_KEY

  # Run multiple rounds with existing canvas
  python experiments/run_social_rl_experiment.py \\
    --state prar/outputs/2025-11-23_baseline_full_qwen/state.json \\
    --rounds 2

  # Run without Dual-LLM (simpler, single temperature)
  python experiments/run_social_rl_experiment.py --no-dual-llm
"""
    )

    parser.add_argument(
        "--model", "-m",
        default="qwen2.5:7b",
        help="Model name (default: qwen2.5:7b)"
    )
    parser.add_argument(
        "--provider", "-p",
        default="ollama",
        choices=["ollama", "openai", "vllm", "mock"],
        help="LLM provider (default: ollama). Use 'vllm' for RunPod serverless."
    )
    parser.add_argument(
        "--rounds", "-r",
        type=int,
        default=1,
        help="Number of rounds to run (default: 1)"
    )
    parser.add_argument(
        "--max-turns", "-t",
        type=int,
        default=9,
        help="Maximum turns per round (default: 9)"
    )
    parser.add_argument(
        "--state", "-s",
        help="Path to state.json with pre-configured canvas"
    )
    parser.add_argument(
        "--no-dual-llm",
        action="store_true",
        help="Disable Dual-LLM architecture"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Reduce output verbosity"
    )
    parser.add_argument(
        "--base-url",
        help="Base URL for vLLM/RunPod endpoint (e.g., https://api.runpod.ai/v2/YOUR_ID/openai/v1)"
    )
    parser.add_argument(
        "--api-key",
        help="API key for vLLM/RunPod (or set RUNPOD_API_KEY env var)"
    )
    parser.add_argument(
        "--experiment-id",
        help="Custom experiment ID (default: auto-generated)"
    )

    args = parser.parse_args()

    try:
        results = run_experiment(
            model=args.model,
            provider=args.provider,
            rounds=args.rounds,
            max_turns=args.max_turns,
            use_dual_llm=not args.no_dual_llm,
            state_path=args.state,
            verbose=not args.quiet,
            base_url=args.base_url,
            api_key=args.api_key,
            experiment_id=args.experiment_id
        )

        print(f"\nExperiment completed successfully!")
        print(f"Experiment ID: {results['meta']['experiment_id']}")
        print(f"Total LLM calls: {len(results['llm_calls'])}")
        print(f"Output directory: {results['output_dir']}")

    except KeyboardInterrupt:
        print("\nExperiment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nExperiment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
