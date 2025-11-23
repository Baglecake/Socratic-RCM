#!/usr/bin/env python3
"""
Run Baseline Experiment - Full 3-Phase Workflow

Runs the complete Socratic-RCM workflow (all 3 phases) and saves outputs
to a timestamped experiments folder.

Usage:
    python run_baseline_experiment.py --base-url http://127.0.0.1:8000/v1 --model Qwen/Qwen2.5-7B-Instruct
    python run_baseline_experiment.py --mock  # For testing without LLM
"""
import os
import sys
import time
import json
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from llm_client import create_llm_client, StudentInteractionHandler
from runtime_parser import Runtime
from canvas_state import compile_canvas_from_student_state, compile_final_document
from orchestrator import WorkflowOrchestrator

# ============================================================================
# BASELINE EXPERIMENT ANSWERS
# These answers represent the "Alienation vs Non-Domination" baseline
# ============================================================================

PHASE1_ANSWERS = {
    "1.1": "yes",
    "1.2.1": "A",
    "1.2.2": "I want to model how workers lose control over their labor and how that shapes their decisions and relationships. The tension is whether agents can coordinate or resist when their agency is structurally suppressed.",
    "1.2.3": "Alienation is when workers become separated from their creative capacities because production treats their labor as owned by someone else. It manifests as mechanical compliance, withdrawal, and decisions driven by survival rather than self-expression.",
    "1.2.4": "Non-domination focuses on vulnerability to arbitrary power rather than internal estrangement. The harm isn't disconnection from labor but exposure to unchecked authority. Workers may feel their work is meaningful but still fear unpredictable interference.",
    "1.2.5": "Single multi-round design - baseline and experiment in one simulation. This lets me see how agents behave under pure alienation first, then observe how introducing a non-domination variable changes the dynamic.",
    "1.2.6": "A - Modify one variable. Since I want to isolate how alienation differs from non-domination, changing just one structural variable makes it clear whether behavior shifts come from that specific intervention.",
    "CHECKPOINT 1.2": "Yes, this aligns with KB[2]. The single-variable modification creates a controlled contrast between alienation and non-domination conditions.",
    "1.3.1": "The baseline is a workplace where the owner controls every aspect - task assignments, timing, workflow. Workers have no input. This reflects Marx because their labor feels imposed rather than self-generated.",
    "1.3.2A": "The experiment introduces one structural safeguard that limits arbitrary power - requiring justification for task changes or giving workers a protected input channel. This shifts toward non-domination while keeping everything else constant.",
    "1.3.3": "The baseline shows how workers behave under pure alienation with no control. The experiment adds protection against arbitrary power. Comparing them reveals whether changes stem from reduced alienation or reduced vulnerability to authority.",
    "CHECKPOINT 1.3": "Yes - the baseline expresses alienation under full control, the experiment tests non-domination by reducing arbitrary power. The contrast directly tests the theoretical tension.",
    "1.4.1": "A small manufacturing workshop with low ceilings and humming machines. Workstations are fixed for repetitive tasks. The owner's office overlooks the floor from a raised platform, making power visible in every interaction. The cramped space reinforces isolation.",
    "1.4.2": "3",
    "CHECKPOINT 1.4": "Yes, the progression tests the hypothesis - baseline alienation, then intervention, then analysis of which framework explains the changes.",
    "1.5.1": "4",
    "CHECKPOINT 1.5": "Yes - Worker+Alice and Worker+Ben represent those experiencing alienation/domination. Owner+Marta represents the source of control. Analyst+Reporter evaluates the theoretical claims.",
    "1.7": "Self-Reflections and Analyst agent for Round 3.",
    "1.8": "Section 1 complete - theoretical framework established with alienation vs non-domination contrast, 3-round design, 4 agents defined.",
}

PHASE1_ROUNDS = [
    "Baseline Alienation: Observe how workers act when they have no control over their labor and the owner directs everything. Establishes pure alienation dynamics.",
    "Reduced Domination: Introduce a safeguard limiting arbitrary power. Observe whether participation increases when workers aren't vulnerable to unpredictable authority.",
    "Comparative Analysis: Review transcripts from both rounds to identify behavioral shifts. Determine which theory better explains the patterns.",
]

PHASE1_AGENTS = [
    ("Worker+Alice", "Human"),
    ("Worker+Ben", "Human"),
    ("Owner+Marta", "Human"),
    ("Analyst+Reporter", "Human"),
]

PHASE1_AGENT_DETAILS = [
    (
        "Alice's goal is to gain more influence over how her work is organized. In the baseline, alienation prevents this. In the experiment, progress shows whether reduced arbitrary power enables participation.",
        "Alice is thoughtful but hesitant, often suppressing ideas because she assumes her input won't matter. She follows directives to avoid conflict. When given protected input channels, she becomes more confident.",
        "no"
    ),
    (
        "Ben's goal is to secure predictable, fair treatment. In the baseline, arbitrary orders create anxiety. In the experiment, he should show less resistance if domination is reduced.",
        "Ben is practical and prefers routine. He follows instructions unless they feel arbitrary, which triggers pushback. His decisions prioritize stability and consistent treatment.",
        "no"
    ),
    (
        "Marta's goal is maintaining productivity while asserting authority. In the baseline, she expects compliance. In the experiment, limiting her discretion may force more justification and negotiation.",
        "Marta is confident and directive, making quick decisions without explanation. She handles conflict by tightening control. Under constraints, she becomes more methodical.",
        "yes - If worker questions: assert stronger control. If workers comply: maintain brisk directive style."
    ),
    (
        "The Analyst's goal is identifying clear behavioral differences between conditions and attributing them to alienation or non-domination. Success is measured by accurate theoretical attribution.",
        "The Analyst is precise and detached, focusing only on empirical patterns. Never participates in the simulation, only observes and reports.",
        "no"
    ),
]

AGENT_PROMPT_CONFIRMS = [
    "Yes, captures Alice's role accurately.",
    "Yes, captures Ben's role accurately.",
    "Yes, captures Marta's role accurately.",
    "Yes, captures Analyst's role accurately."
]

ROUND_ANSWERS = {
    1: {  # Baseline Alienation
        "2.2.1": "The workshop hums with machinery. Workers move mechanically between stations. Marta watches from her elevated office, issuing directives without explanation. No one questions, no one suggests. The air feels heavy with unspoken tension. This is pure alienation - labor as external imposition.",
        "2.2.2": "Alienation manifests as complete separation from decision-making. Workers execute tasks without understanding purpose. Their labor feels external, imposed. Creative capacities are dormant.",
        "2.2.3": "Non-domination is absent - arbitrary power is unchecked. Marta can change orders without justification. Workers have no protection against sudden changes.",
        "2.2.4": "Workers CAN: complete assigned tasks, request clarification on instructions. Workers CANNOT: suggest changes, refuse orders, negotiate timing, modify workflow.",
        "2.2.5": "Complete three production cycles. Marta assigns tasks. Workers comply or face consequences. Observe compliance patterns and signs of withdrawal.",
        "2.2.6": "Marta assigns tasks, workers comply silently. Any hesitation triggers reassertion of control. Round ends with production complete. Track instances of mechanical compliance.",
        "2.2.7": "Yes, include Marta's behavior rules for tightening control.",
        "2.2.8": "Compiled instructions look correct for baseline alienation condition.",
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
        "2.2.19": "Config looks correct for baseline round.",
    },
    2: {  # Reduced Domination
        "2.2.1": "Same workshop, but a new structural rule: Marta must justify task changes. Workers have a protected feedback channel. The air feels slightly different - there's a possibility of voice, though alienation from labor itself persists.",
        "2.2.2": "Alienation persists structurally but workers have more information. They still don't control labor but understand decisions better. The separation remains but feels less arbitrary.",
        "2.2.3": "Non-domination is partially activated - arbitrary power is constrained. Workers can question without fear of immediate retaliation. Vulnerability to unchecked authority is reduced.",
        "2.2.4": "Workers CAN: request justification for changes, use feedback channel, suggest improvements within scope. Workers CANNOT: refuse justified orders, unilaterally change workflow.",
        "2.2.5": "Complete production while testing the new feedback mechanism. Observe if participation increases when workers aren't vulnerable to arbitrary power.",
        "2.2.6": "Marta assigns tasks but must explain changes. Workers may ask questions through feedback channel. Round ends when production completes with feedback logged.",
        "2.2.7": "Yes, Marta's behaviors adapt to constraint - more methodical, must justify.",
        "2.2.8": "Compiled instructions look correct for reduced domination condition.",
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
        "2.2.19": "Config looks correct for experimental round.",
    },
    3: {  # Comparative Analysis
        "2.2.1": "Analyst reviews transcripts from both rounds. No active simulation - purely analytical. Looking for patterns of behavioral change between alienation and reduced domination conditions.",
        "2.2.2": "Alienation analysis: identify markers of mechanical compliance, withdrawal, survival-driven decisions in Round 1. Count instances of suppressed initiative.",
        "2.2.3": "Non-domination analysis: identify markers of increased participation, questioning, confidence in Round 2. Count instances of worker voice.",
        "2.2.4": "Analyst CAN: review all transcripts, identify patterns, make theoretical claims, compare conditions. Analyst CANNOT: interact with original agents, modify transcripts.",
        "2.2.5": "Produce comparative report attributing behavioral changes to either alienation reduction or domination reduction. Determine which framework better explains observed patterns.",
        "2.2.6": "Analyst reviews Round 1, then Round 2, then produces comparative analysis with explicit theoretical attribution.",
        "2.2.7": "No additional behaviors needed for Analyst.",
        "2.2.8": "Compiled instructions look correct for analysis round.",
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
        "2.2.19": "Config looks correct for analysis round.",
    }
}

PHASE2_3_ANSWERS = {
    "2.3.1": "",  # Moderator - NOT selected
    "2.3.2": "Analyst summarizes behavioral patterns from both rounds and attributes differences to either alienation (separation from labor) or non-domination (reduced arbitrary power).",
    "2.3.3": "Use environmental cues instead of facial expressions: 'The machine hums louder' signals tension, 'The light flickers' signals uncertainty, 'Tools clatter' signals frustration, 'Silence settles' signals resignation.",
    "2.3.4": "Self-reflection prompts: 'How did that interaction affect your sense of control over your work?' and 'Did you feel your input mattered in that exchange?'",
    "2.3.5": "Section 2 complete - all rounds configured with alienation/non-domination manifestations.",
}

PHASE3_ANSWERS = {
    "3.1": "Design looks complete and coherent. Theoretical framework clearly distinguishes alienation from non-domination.",
    "3.2": "Yes, ready for export. All components present.",
    "3.2.5": "Verified: agents have correct prompts, rounds have correct conditions, helper functions enabled.",
    "3.3": "Final confirmation - baseline experiment ready to run. Will test alienation vs non-domination hypothesis.",
}


class BaselineAnswerProvider:
    """Provides answers for baseline experiment"""

    def __init__(self):
        self.counters = {}
        self.current_round = 1
        self.answers_given = []

    def get_answer(self, prompt: str, step_id: str, orchestrator) -> str:
        if "current_phase2_round_counter" in orchestrator.student_state:
            self.current_round = orchestrator.student_state["current_phase2_round_counter"]

        answer = self._lookup_answer(step_id, orchestrator)
        self.answers_given.append((step_id, self.current_round, answer[:50] if answer else ""))

        time.sleep(0.2)
        print(f"> {answer}")
        return answer

    def _lookup_answer(self, step_id: str, orchestrator) -> str:
        if step_id in PHASE1_ANSWERS:
            return PHASE1_ANSWERS[step_id]

        if step_id == "1.4.3":
            idx = self.counters.get("1.4.3", 0)
            self.counters["1.4.3"] = idx + 1
            return PHASE1_ROUNDS[idx] if idx < len(PHASE1_ROUNDS) else "Additional round."

        if step_id == "1.5.2":
            idx = self.counters.get("1.5.2", 0)
            self.counters["1.5.2"] = idx + 1
            return PHASE1_AGENTS[idx][0] if idx < len(PHASE1_AGENTS) else "Agent"

        if step_id == "1.5.3":
            idx = self.counters.get("1.5.3", 0)
            self.counters["1.5.3"] = idx + 1
            return PHASE1_AGENTS[idx][1] if idx < len(PHASE1_AGENTS) else "Human"

        if step_id == "1.6.1":
            idx = self.counters.get("1.6.1", 0)
            self.counters["1.6.1"] = idx + 1
            return PHASE1_AGENT_DETAILS[idx][0] if idx < len(PHASE1_AGENT_DETAILS) else "Goal"

        if step_id == "1.6.2":
            idx = self.counters.get("1.6.2", 0)
            self.counters["1.6.2"] = idx + 1
            return PHASE1_AGENT_DETAILS[idx][1] if idx < len(PHASE1_AGENT_DETAILS) else "Persona"

        if step_id == "1.6.3":
            idx = self.counters.get("1.6.3", 0)
            self.counters["1.6.3"] = idx + 1
            return PHASE1_AGENT_DETAILS[idx][2] if idx < len(PHASE1_AGENT_DETAILS) else "no"

        if step_id == "2.1.1":
            idx = self.counters.get("2.1.1", 0)
            self.counters["2.1.1"] = idx + 1
            return AGENT_PROMPT_CONFIRMS[idx] if idx < len(AGENT_PROMPT_CONFIRMS) else "Confirmed."

        if step_id.startswith("2.2."):
            round_num = self.current_round
            if round_num in ROUND_ANSWERS and step_id in ROUND_ANSWERS[round_num]:
                return ROUND_ANSWERS[round_num][step_id]
            return f"Answer for {step_id} round {round_num}"

        if step_id in PHASE2_3_ANSWERS:
            return PHASE2_3_ANSWERS[step_id]

        if step_id in PHASE3_ANSWERS:
            return PHASE3_ANSWERS[step_id]

        return f"[Auto-answer for {step_id}]"


def create_experiment_folder(base_dir: str, name: str) -> str:
    """Create timestamped experiment folder"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{timestamp}_{name}"
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def save_config(folder: str, model: str, backend: str, base_url: str, phases_completed: list):
    """Save experiment configuration"""
    config = {
        "experiment_name": "Baseline Full - Alienation vs Non-Domination",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "model": model,
        "backend": backend,
        "base_url": base_url,
        "phases_completed": phases_completed,
        "script": "scripts/run_baseline_experiment.py",
        "theoretical_framework": {
            "option": "A",
            "name": "Class Conflict / Alienation",
            "theorists": ["Marx", "Wollstonecraft"],
            "concept_a": "Alienation",
            "concept_b": "Non-domination"
        },
        "experiment_design": {
            "type": "Single multi-round",
            "variable_modification": "Type A (single variable)",
            "rounds": 3,
            "agents": 4
        }
    }
    with open(os.path.join(folder, "config.json"), "w") as f:
        json.dump(config, f, indent=2)


def save_notes(folder: str, step_count: int, phase_tracker: dict, model: str, success: bool):
    """Save experiment notes"""
    notes = f"""# Experiment: Baseline Full - Alienation vs Non-Domination

## Date: {datetime.now().strftime("%Y-%m-%d")}

## Purpose
Full 3-phase workflow with real LLM to generate complete simulation configuration.

## Model Configuration
- Model: {model}
- Backend: vLLM
- Temperature: Default

## Results
- Total steps executed: {step_count}
- Phase 1 steps: {phase_tracker.get('1', 0)}
- Phase 2 steps: {phase_tracker.get('2', 0)}
- Phase 3 steps: {phase_tracker.get('3', 0)}
- Success: {success}

## What Was Generated
- Project goal and theoretical framework
- 4 agents (Worker+Alice, Worker+Ben, Owner+Marta, Analyst+Reporter)
- 3 rounds with specific instructions:
  - Round 1: Baseline Alienation
  - Round 2: Reduced Domination
  - Round 3: Comparative Analysis
- Helper functions configured
- Platform configuration for each round

## Files
- state.json: Complete workflow state with canvas
- document.txt: Compiled human-readable document
- config.json: Experiment metadata
- notes.md: This file
"""
    with open(os.path.join(folder, "notes.md"), "w") as f:
        f.write(notes)


def main():
    parser = argparse.ArgumentParser(description="Run baseline experiment - full 3-phase workflow")
    parser.add_argument("--base-url", help="vLLM server URL (e.g., http://127.0.0.1:8000/v1)")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct", help="Model name")
    parser.add_argument("--mock", action="store_true", help="Use mock client for testing")
    parser.add_argument("--max-steps", type=int, default=200, help="Maximum steps to run")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: experiments/)")
    parser.add_argument("--name", default="baseline_full_qwen", help="Experiment name suffix")
    args = parser.parse_args()

    # Determine output directory
    if args.output_dir:
        experiments_dir = args.output_dir
    else:
        experiments_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "prar", "outputs"
        )
    os.makedirs(experiments_dir, exist_ok=True)

    print("=" * 70)
    print("BASELINE EXPERIMENT - Full 3-Phase Workflow")
    print("Alienation vs Non-Domination")
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
    if args.mock or not args.base_url:
        print("Using MOCK client (no API calls)\n")
        llm = create_llm_client("mock")
        backend = "mock"
        base_url = "mock"
    else:
        print(f"Using vLLM: {args.base_url}")
        print(f"Model: {args.model}\n")
        llm = create_llm_client("vllm", base_url=args.base_url, model=args.model)
        backend = "vLLM"
        base_url = args.base_url

    # Load BIOS prompt
    bios_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bios_reduced_prompt.txt")
    with open(bios_path, 'r') as f:
        bios_prompt = f.read()

    handler = StudentInteractionHandler(llm, bios_prompt)
    answer_provider = BaselineAnswerProvider()

    def get_input(prompt: str) -> str:
        return answer_provider.get_answer(prompt, orchestrator.current_step_id, orchestrator)

    orchestrator = WorkflowOrchestrator(
        runtime=runtime,
        student_handler=handler,
        starting_step="1.1",
        get_student_input=get_input
    )

    print("Starting workflow...\n")
    print("-" * 70)

    step_count = 0
    phase_tracker = {"1": 0, "2": 0, "3": 0}
    success = False

    try:
        while orchestrator.current_step_id and step_count < args.max_steps:
            step_count += 1
            current_phase = orchestrator.current_step_id[0]
            phase_tracker[current_phase] = phase_tracker.get(current_phase, 0) + 1

            print(f"\n--- Step {orchestrator.current_step_id} ({step_count}) ---")

            step = orchestrator.runtime.get_step(orchestrator.current_step_id)
            print(f"Target: {step.target}")

            result = orchestrator.execute_step(orchestrator.current_step_id)
            if not result:
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
                success = True
                break

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

    # Summary
    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)
    print(f"Total steps: {step_count}")
    print(f"Phase 1: {phase_tracker.get('1', 0)} steps")
    print(f"Phase 2: {phase_tracker.get('2', 0)} steps")
    print(f"Phase 3: {phase_tracker.get('3', 0)} steps")
    print(f"Success: {success}")

    # Compile canvas
    canvas = compile_canvas_from_student_state(orchestrator.student_state)
    orchestrator.canvas = canvas

    print(f"\nAgents created: {len(canvas.agents)}")
    print(f"Rounds defined: {len(canvas.rounds)}")

    # Determine phases completed
    phases_completed = []
    if canvas.status.phase1_complete:
        phases_completed.append("1")
    if canvas.status.phase2_complete:
        phases_completed.append("2")
    if canvas.status.phase3_complete:
        phases_completed.append("3")

    # Create experiment folder and save outputs
    experiment_folder = create_experiment_folder(experiments_dir, args.name)
    print(f"\nSaving to: {experiment_folder}")

    # Save state
    state_path = os.path.join(experiment_folder, "state.json")
    orchestrator.save_state(state_path)

    # Save document
    doc_path = os.path.join(experiment_folder, "document.txt")
    final_doc = compile_final_document(canvas)
    with open(doc_path, "w") as f:
        f.write(final_doc)

    # Save config and notes
    save_config(experiment_folder, args.model, backend, base_url, phases_completed)
    save_notes(experiment_folder, step_count, phase_tracker, args.model, success)

    print(f"\nFiles saved:")
    print(f"  - {state_path}")
    print(f"  - {doc_path}")
    print(f"  - {os.path.join(experiment_folder, 'config.json')}")
    print(f"  - {os.path.join(experiment_folder, 'notes.md')}")

    if success:
        print("\nExperiment completed successfully!")
    else:
        print("\nExperiment completed with errors - check logs above.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
