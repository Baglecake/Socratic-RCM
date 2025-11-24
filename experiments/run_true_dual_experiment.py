#!/usr/bin/env python3
"""
True Dual-LLM Experiment Runner

Runs Social RL experiments with GENUINE dual-LLM architecture:
- Performer: Larger model (e.g., 14B on A100) for creative generation
- Coach: Smaller model (e.g., 7B on A40) for strict validation

This is the research-grade setup where Coach and Performer are
truly different models running on separate GPUs/endpoints.

Usage:
    # With environment variables set in .env:
    python experiments/run_true_dual_experiment.py

    # With explicit endpoints:
    python experiments/run_true_dual_experiment.py \
        --performer-url https://a100-pod.runpod.net/v1 \
        --performer-model Qwen/Qwen2.5-14B-Instruct \
        --coach-url https://a40-pod.runpod.net/v1 \
        --coach-model Qwen/Qwen2.5-7B-Instruct

    # Test connectivity first:
    python experiments/run_true_dual_experiment.py --test-only
"""

import sys
import os
import json
import argparse
import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")


def test_endpoint(base_url: str, model: str, api_key: str, name: str) -> bool:
    """Test connectivity to an endpoint."""
    from openai import OpenAI

    print(f"\nTesting {name} endpoint...")
    print(f"  URL: {base_url}")
    print(f"  Model: {model}")

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=60.0,
            default_headers={"ngrok-skip-browser-warning": "true"}
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'ready' in one word."}
            ],
            max_tokens=10,
            temperature=0.1
        )

        result = response.choices[0].message.content.strip()
        print(f"  Response: {result}")
        print(f"  Status: CONNECTED")
        return True

    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")
        print(f"  Status: FAILED")
        return False


def run_true_dual_experiment(
    performer_url: str,
    performer_model: str,
    coach_url: str,
    coach_model: str,
    api_key: str,
    state_path: Optional[str] = None,
    rounds: int = 1,
    max_turns: int = 9,
    performer_temp: float = 0.7,
    coach_temp: float = 0.1,
    experiment_id: Optional[str] = None,
    verbose: bool = True
) -> dict:
    """
    Run a true dual-LLM Social RL experiment.

    Args:
        performer_url: vLLM endpoint URL for Performer
        performer_model: Model name for Performer
        coach_url: vLLM endpoint URL for Coach
        coach_model: Model name for Coach
        api_key: API key for endpoints
        state_path: Path to state.json with canvas
        rounds: Number of rounds to execute
        max_turns: Max turns per round
        performer_temp: Temperature for Performer (default 0.7)
        coach_temp: Temperature for Coach (default 0.1)
        experiment_id: Custom experiment ID
        verbose: Print progress

    Returns:
        Experiment results dict
    """
    from social_rl.runner import SocialRLRunner, SocialRLConfig
    from social_rl.dual_llm_client import create_true_dual_llm

    print("=" * 70)
    print("TRUE DUAL-LLM SOCIAL RL EXPERIMENT")
    print("=" * 70)
    print(f"Performer: {performer_model} @ {performer_url}")
    print(f"  Temperature: {performer_temp}")
    print(f"Coach: {coach_model} @ {coach_url}")
    print(f"  Temperature: {coach_temp}")
    print(f"Rounds: {rounds}, Max turns: {max_turns}")
    print("=" * 70)

    # Generate experiment ID
    if not experiment_id:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        experiment_id = f"true_dual_{timestamp}"

    # Get git commit
    try:
        import subprocess
        git_commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=PROJECT_ROOT,
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        git_commit = "unknown"

    # Create TRUE dual-LLM client (separate models!)
    print("\nInitializing true dual-LLM client...")
    dual_llm = create_true_dual_llm(
        performer_base_url=performer_url,
        performer_model=performer_model,
        coach_base_url=coach_url,
        coach_model=coach_model,
        performer_temp=performer_temp,
        coach_temp=coach_temp,
        api_key=api_key,
        timeout=180.0
    )
    print("  Dual-LLM client created with SEPARATE models")

    # Load canvas
    if state_path:
        print(f"\nLoading canvas from: {state_path}")
        with open(state_path, 'r') as f:
            state = json.load(f)
        canvas = state.get("canvas", state)
    else:
        # Use default baseline canvas
        default_state = PROJECT_ROOT / "prar/outputs/2025-11-23_baseline_full_qwen/state.json"
        if default_state.exists():
            print(f"\nLoading default canvas: {default_state}")
            with open(default_state, 'r') as f:
                state = json.load(f)
            canvas = state.get("canvas", state)
            state_path = str(default_state)
        else:
            raise FileNotFoundError(
                "No state.json found. Provide --state path or ensure "
                "prar/outputs/2025-11-23_baseline_full_qwen/state.json exists"
            )

    print(f"  Framework: {canvas.get('project', {}).get('theoretical_option_label', 'Unknown')}")
    print(f"  Agents: {[a['identifier'] for a in canvas.get('agents', [])]}")

    # Configure runner - note we need a fallback LLM for non-dual paths
    # Create a simple performer-only client as fallback
    from openai import OpenAI

    class FallbackClient:
        """Fallback client using performer endpoint."""
        def __init__(self):
            self.client = OpenAI(
                api_key=api_key,
                base_url=performer_url,
                timeout=180.0,
                default_headers={"ngrok-skip-browser-warning": "true"}
            )
            self.model = performer_model

        def send_message(self, system_prompt: str, user_message: str) -> str:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=performer_temp,
                max_tokens=512
            )
            return response.choices[0].message.content

    fallback_llm = FallbackClient()

    # Configure Social RL
    config = SocialRLConfig(
        manifestation_mode="progressive",
        use_prar_cues=True,
        prar_intensity="medium",
        use_coach_validation=True,  # Enable dual-LLM validation
        coach_temperature=coach_temp,
        performer_temperature=performer_temp,
        verbose=verbose,
        auto_save=True
    )

    # Create runner with dual-LLM
    runner = SocialRLRunner(
        canvas=canvas,
        llm_client=fallback_llm,
        config=config,
        dual_llm_client=dual_llm,
        experiment_id=experiment_id
    )

    # Execute rounds
    results = []
    for round_num in range(1, min(rounds + 1, len(canvas.get("rounds", [])) + 1)):
        print(f"\n{'='*70}")
        print(f"EXECUTING ROUND {round_num}")
        print(f"{'='*70}\n")

        try:
            result = runner.execute_round(round_num, max_turns=max_turns)
            results.append(result)

            # Print validation stats
            validation_count = sum(
                1 for m in result.messages
                if m.validation_metadata and m.validation_metadata.get("used_dual_llm")
            )
            retry_count = sum(
                m.validation_metadata.get("attempts", 1) - 1
                for m in result.messages
                if m.validation_metadata
            )
            print(f"\n  Dual-LLM validations: {validation_count}")
            print(f"  Coach-triggered retries: {retry_count}")

        except Exception as e:
            print(f"Error in round {round_num}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Generate report
    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)

    report = runner.generate_report()
    print(report)

    # Build meta block
    meta = {
        "experiment_id": experiment_id,
        "experiment_type": "true_dual_llm",
        "framework": canvas.get("project", {}).get("theoretical_option_label", "Unknown"),
        "framework_option": canvas.get("project", {}).get("theoretical_option", "A"),
        "performer": {
            "model": performer_model,
            "endpoint": performer_url,
            "temperature": performer_temp
        },
        "coach": {
            "model": coach_model,
            "endpoint": coach_url,
            "temperature": coach_temp
        },
        "rounds_executed": len(results),
        "max_turns_per_round": max_turns,
        "git_commit": git_commit,
        "social_rl_version": "0.3.0",  # True dual-LLM version
        "prar_state_file": state_path,
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Save meta.json
    if results and runner.output_dir:
        meta_path = runner.output_dir / "meta.json"
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        print(f"\n  [SAVED] {meta_path}")

    # Compute metrics
    metrics = None
    if results and runner.output_dir:
        try:
            from social_rl.metrics import compute_experiment_metrics
            metrics = compute_experiment_metrics(results)
            metrics_path = runner.output_dir / "metrics.json"
            with open(metrics_path, "w") as f:
                json.dump(metrics, f, indent=2)
            print(f"  [SAVED] {metrics_path}")
        except Exception as e:
            print(f"  [METRICS WARNING] {e}")

    if results:
        print(f"\nResults saved to: {runner.output_dir}")

    return {
        "meta": meta,
        "results": [r.to_dict() for r in results],
        "metrics": metrics,
        "report": report,
        "output_dir": str(runner.output_dir) if runner.output_dir else None
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run a TRUE dual-LLM Social RL experiment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables (set in .env):
  PERFORMER_BASE_URL  - Performer endpoint URL
  PERFORMER_MODEL     - Performer model name
  COACH_BASE_URL      - Coach endpoint URL
  COACH_MODEL         - Coach model name
  RUNPOD_API_KEY      - API key for RunPod endpoints

Examples:
  # Run with .env configuration:
  python experiments/run_true_dual_experiment.py

  # Test connectivity only:
  python experiments/run_true_dual_experiment.py --test-only

  # Override endpoints:
  python experiments/run_true_dual_experiment.py \\
      --performer-url https://a100-endpoint/v1 \\
      --coach-url https://a40-endpoint/v1

  # Run 2 rounds with custom canvas:
  python experiments/run_true_dual_experiment.py \\
      --state prar/outputs/2025-11-23_baseline_full_qwen/state.json \\
      --rounds 2
"""
    )

    # Endpoint configuration
    parser.add_argument(
        "--performer-url",
        default=os.getenv("PERFORMER_BASE_URL"),
        help="Performer endpoint URL (or set PERFORMER_BASE_URL)"
    )
    parser.add_argument(
        "--performer-model",
        default=os.getenv("PERFORMER_MODEL", "Qwen/Qwen2.5-14B-Instruct"),
        help="Performer model name"
    )
    parser.add_argument(
        "--coach-url",
        default=os.getenv("COACH_BASE_URL"),
        help="Coach endpoint URL (or set COACH_BASE_URL)"
    )
    parser.add_argument(
        "--coach-model",
        default=os.getenv("COACH_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        help="Coach model name"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("RUNPOD_API_KEY"),
        help="API key for endpoints"
    )

    # Experiment configuration
    parser.add_argument(
        "--state", "-s",
        help="Path to state.json with canvas"
    )
    parser.add_argument(
        "--rounds", "-r",
        type=int,
        default=1,
        help="Number of rounds (default: 1)"
    )
    parser.add_argument(
        "--max-turns", "-t",
        type=int,
        default=9,
        help="Max turns per round (default: 9)"
    )
    parser.add_argument(
        "--performer-temp",
        type=float,
        default=0.7,
        help="Performer temperature (default: 0.7)"
    )
    parser.add_argument(
        "--coach-temp",
        type=float,
        default=0.1,
        help="Coach temperature (default: 0.1)"
    )
    parser.add_argument(
        "--experiment-id",
        help="Custom experiment ID"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Reduce verbosity"
    )

    # Test mode
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Only test endpoint connectivity, don't run experiment"
    )

    args = parser.parse_args()

    # Validate required arguments
    if not args.performer_url:
        print("ERROR: --performer-url required (or set PERFORMER_BASE_URL in .env)")
        print("\nCurrent .env values:")
        print(f"  PERFORMER_BASE_URL = {os.getenv('PERFORMER_BASE_URL', 'NOT SET')}")
        print(f"  COACH_BASE_URL = {os.getenv('COACH_BASE_URL', 'NOT SET')}")
        sys.exit(1)

    if not args.coach_url:
        print("ERROR: --coach-url required (or set COACH_BASE_URL in .env)")
        sys.exit(1)

    if not args.api_key:
        args.api_key = "not-needed"  # vLLM doesn't require API key

    # Test mode
    if args.test_only:
        print("\n" + "=" * 50)
        print("ENDPOINT CONNECTIVITY TEST")
        print("=" * 50)

        performer_ok = test_endpoint(
            args.performer_url,
            args.performer_model,
            args.api_key,
            "Performer"
        )
        coach_ok = test_endpoint(
            args.coach_url,
            args.coach_model,
            args.api_key,
            "Coach"
        )

        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(f"Performer: {'READY' if performer_ok else 'FAILED'}")
        print(f"Coach: {'READY' if coach_ok else 'FAILED'}")

        if performer_ok and coach_ok:
            print("\nBoth endpoints ready! Run without --test-only to start experiment.")
            sys.exit(0)
        else:
            print("\nFix endpoint issues before running experiment.")
            sys.exit(1)

    # Run experiment
    try:
        results = run_true_dual_experiment(
            performer_url=args.performer_url,
            performer_model=args.performer_model,
            coach_url=args.coach_url,
            coach_model=args.coach_model,
            api_key=args.api_key,
            state_path=args.state,
            rounds=args.rounds,
            max_turns=args.max_turns,
            performer_temp=args.performer_temp,
            coach_temp=args.coach_temp,
            experiment_id=args.experiment_id,
            verbose=not args.quiet
        )

        print(f"\nExperiment completed!")
        print(f"Experiment ID: {results['meta']['experiment_id']}")
        print(f"Output: {results['output_dir']}")

    except KeyboardInterrupt:
        print("\nExperiment interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\nExperiment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
