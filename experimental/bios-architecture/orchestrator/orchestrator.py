"""
BIOS Orchestrator - Code-enforced workflow execution

This is the "kernel" that enforces the BIOS specification.
The orchestrator:
1. Owns the step_id state machine
2. Reads runtime files to know what question to ask
3. Uses LLM as "smart IO device" for RCM interaction
4. Updates canvas state progressively
5. GUARANTEES no step skipping
"""

import os
from typing import Dict, Optional, Callable
from runtime_parser import Runtime, Step
from canvas_state import CanvasState, apply_canvas_update, compile_final_document
from llm_client import StudentInteractionHandler, LLMClient


class WorkflowOrchestrator:
    """
    Main orchestrator that enforces BIOS workflow execution.

    The LLM NEVER controls step advancement. Code owns the state machine.
    """

    def __init__(
        self,
        runtime: Runtime,
        student_handler: StudentInteractionHandler,
        canvas: Optional[CanvasState] = None,
        starting_step: str = "1.1.1",
        get_student_input: Optional[Callable[[str], str]] = None
    ):
        """
        Initialize the orchestrator.

        Args:
            runtime: Parsed runtime files
            student_handler: LLM interface for interaction
            canvas: Canvas state (creates new if None)
            starting_step: Which step to start from (default: 1.1.1)
            get_student_input: Function to get input from student
                               If None, uses input() for CLI
        """
        self.runtime = runtime
        self.student_handler = student_handler
        self.canvas = canvas or CanvasState()
        self.current_step_id = starting_step
        self.student_state: Dict[str, str] = {}  # step_id -> answer
        self.get_student_input = get_student_input or self._cli_input
        self.max_retries = 3  # Max attempts for validation

    def _cli_input(self, prompt: str) -> str:
        """Default input function for CLI"""
        print(f"\n{prompt}")
        return input("> ")

    def run_workflow(self) -> CanvasState:
        """
        Execute the complete workflow from current step to completion.

        Returns:
            Final canvas state with all accumulated data
        """
        print("=== BIOS Orchestrator Started ===")
        print(f"Starting at step: {self.current_step_id}\n")

        step_count = 0

        while self.current_step_id is not None:
            step_count += 1
            print(f"\n--- Step {self.current_step_id} ({step_count}) ---")

            # Execute current step
            success = self.execute_step(self.current_step_id)

            if not success:
                print(f"ERROR: Failed to complete step {self.current_step_id}")
                break

            # Get next step from runtime (CODE decides, not LLM)
            current_step = self.runtime.get_step(self.current_step_id)
            next_step_id = current_step.next_step

            # Handle special next step values
            if next_step_id == "END" or next_step_id == "DONE":
                next_step_id = None

            # Log advancement
            if next_step_id:
                print(f"✓ Advancing: {self.current_step_id} → {next_step_id}")
            else:
                print(f"✓ Workflow complete at step {self.current_step_id}")

            self.current_step_id = next_step_id

        print(f"\n=== Workflow Complete ({step_count} steps executed) ===")
        return self.canvas

    def execute_step(self, step_id: str) -> bool:
        """
        Execute a single step: ask question, validate, store answer, update canvas.

        Returns:
            True if step completed successfully, False otherwise
        """
        try:
            step = self.runtime.get_step(step_id)
        except KeyError:
            print(f"ERROR: Step {step_id} not found in runtime files")
            return False

        print(f"Target: {step.target}")

        # Special handling for Phase 3 retrieval
        if "CANVAS_RETRIEVE" in step.instruction:
            return self.execute_canvas_retrieve(step)

        # 1. Ask the question (LLM may add RCM flavor)
        question = self.student_handler.ask_question(
            step.required_output,
            step.rcm_cue,
            context=self._get_recent_context()
        )

        # 2. Get student's answer
        student_answer = self.get_student_input(question)

        # 3. Validate answer (with retries)
        for attempt in range(self.max_retries):
            validation = self.student_handler.validate_answer(
                student_answer,
                step.constraint,
                step.target
            )

            if validation.get("ok"):
                # Answer is valid
                print(f"✓ Answer accepted")
                break
            else:
                # Answer needs improvement
                print(f"⚠ Validation issue: {validation.get('reason')}")

                if attempt < self.max_retries - 1:
                    # Ask for clarification
                    follow_up = self.student_handler.remediate_answer(
                        student_answer,
                        validation,
                        step.required_output
                    )
                    student_answer = self.get_student_input(follow_up)
                else:
                    # Max retries reached, accept anyway
                    print(f"⚠ Max retries reached, accepting answer")
                    break

        # 4. Store the answer
        self.student_state[step_id] = student_answer

        # 5. Apply canvas update if present
        if step.canvas_update:
            print(f"📝 Updating canvas: {step.canvas_update.get('section')}")
            self.canvas = apply_canvas_update(
                self.canvas,
                step.canvas_update,
                self.student_state
            )

        return True

    def execute_canvas_retrieve(self, step: Step) -> bool:
        """
        Special handler for CANVAS_RETRIEVE steps (Phase 3 final compilation).
        """
        print("📋 Compiling final design document from canvas...")

        # Compile the document
        final_doc = compile_final_document(self.canvas)

        # Show it to the student
        print("\n" + "="*60)
        print("FINAL DESIGN DOCUMENT")
        print("="*60)
        print(final_doc)
        print("="*60 + "\n")

        # Ask for confirmation
        confirmation = self.get_student_input(step.required_output)
        self.student_state[step.id] = confirmation

        return True

    def _get_recent_context(self, last_n: int = 3) -> str:
        """
        Get context from recent answers to help LLM with flow.

        Args:
            last_n: Number of recent answers to include

        Returns:
            Summary of recent answers
        """
        if not self.student_state:
            return ""

        recent_items = list(self.student_state.items())[-last_n:]
        context_lines = []
        for step_id, answer in recent_items:
            # Truncate long answers
            short_answer = answer[:100] + "..." if len(answer) > 100 else answer
            context_lines.append(f"{step_id}: {short_answer}")

        return "\n".join(context_lines)

    def get_canvas_state(self) -> CanvasState:
        """Get current canvas state"""
        return self.canvas

    def get_student_answers(self) -> Dict[str, str]:
        """Get all student answers collected so far"""
        return self.student_state.copy()

    def save_state(self, filepath: str):
        """Save current workflow state to file"""
        import json

        state = {
            "current_step": self.current_step_id,
            "student_state": self.student_state,
            "canvas": self.canvas.to_dict()
        }

        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

        print(f"State saved to: {filepath}")

    def load_state(self, filepath: str):
        """Load workflow state from file"""
        import json

        with open(filepath, 'r') as f:
            state = json.load(f)

        self.current_step_id = state["current_step"]
        self.student_state = state["student_state"]
        # Note: Canvas state loading would need more work to reconstruct dataclasses

        print(f"State loaded from: {filepath}")


def create_orchestrator(
    llm_client: LLMClient,
    bios_prompt: str,
    runtime_base_path: Optional[str] = None,
    starting_step: str = "1.1.1"
) -> WorkflowOrchestrator:
    """
    Factory function to create a fully configured orchestrator.

    Args:
        llm_client: LLM client for student interaction
        bios_prompt: BIOS system prompt (reduced version for orchestrator)
        runtime_base_path: Path to runtime files directory
        starting_step: Which step to start from

    Returns:
        Configured WorkflowOrchestrator
    """
    # Determine runtime file paths
    if runtime_base_path is None:
        runtime_base_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "runtime-files"
        )

    phase1_path = os.path.join(runtime_base_path, "B42_Runtime_Phase1_Conceptualization.txt")
    phase2_path = os.path.join(runtime_base_path, "B42_Runtime_Phase2_Drafting.txt")
    phase3_path = os.path.join(runtime_base_path, "B42_Runtime_Phase3_Review.txt")

    # Parse runtime files
    print("Loading runtime files...")
    runtime = Runtime(phase1_path, phase2_path, phase3_path)
    print(f"✓ Loaded {len(runtime.steps)} steps")

    # Create student interaction handler
    student_handler = StudentInteractionHandler(llm_client, bios_prompt)

    # Create orchestrator
    orchestrator = WorkflowOrchestrator(
        runtime=runtime,
        student_handler=student_handler,
        starting_step=starting_step
    )

    return orchestrator


if __name__ == "__main__":
    # Simple test with mock client
    from llm_client import create_llm_client

    print("=== BIOS Orchestrator Test ===\n")

    # Create a mock LLM client (no API calls)
    llm = create_llm_client("mock")

    # Simple BIOS prompt for testing
    bios_prompt = """You are the B42 Chatstorm T.A., a Socratic assistant.
You must not write content for students. Ask clarifying questions when needed."""

    # Create orchestrator
    try:
        orchestrator = create_orchestrator(
            llm_client=llm,
            bios_prompt=bios_prompt,
            starting_step="1.1.1"
        )

        print("\nOrchestrator created successfully!")
        print("In production, call orchestrator.run_workflow() to begin.")

    except Exception as e:
        print(f"Error creating orchestrator: {e}")
        import traceback
        traceback.print_exc()
