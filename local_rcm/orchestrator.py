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
            raw_next_step = current_step.next_step
            
            # Resolve conditional next steps
            next_step_id = self.resolve_next_step(self.current_step_id, raw_next_step)

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

    def _text_to_int(self, text: str) -> int:
        """Helper to convert text numbers to integers"""
        text = text.lower()
        word_map = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
        }
        
        # Try to find digits first
        import re
        digits = re.search(r'\d+', text)
        if digits:
            return int(digits.group())
            
        # Find all word matches and their positions
        matches = []
        for word, val in word_map.items():
            # Use word boundary to avoid partial matches (e.g. "one" in "phone")
            # But simple 'in' check is safer for now given the limited map
            idx = text.find(word)
            if idx != -1:
                matches.append((idx, val))
        
        if matches:
            # Sort by index (position in string)
            matches.sort(key=lambda x: x[0])
            print(f"[System] Detected number: {matches[0][1]} (from '{text}')")
            return matches[0][1]
                
        return 1  # Default fallback

    def resolve_next_step(self, current_step_id: str, raw_next_step: str) -> Optional[str]:
        """
        Resolve the next step ID, handling conditionals and loops.
        """
        print(f"[DEBUG] resolve_next_step: current={current_step_id}, raw_next={raw_next_step}")
        
        if not raw_next_step:
            return None

        # --- SPECIFIC LOGIC FIRST ---

        # Case 3: Branching at 1.3.1
        if "1.3.2A or 1.3.2B" in raw_next_step:
            # Check answer to 1.2.6
            answer_1_2_6 = self.student_state.get("1.2.6", "").lower()
            if "option a" in answer_1_2_6 or "modify one variable" in answer_1_2_6:
                return "1.3.2A"
            else:
                return "1.3.2B"

        # Case 4: Branching at 1.3.1 (Alternative check)
        if current_step_id == "1.3.1":
             # Check answer to 1.2.6
            answer_1_2_6 = self.student_state.get("1.2.6", "").lower()
            if "option a" in answer_1_2_6 or "modify one variable" in answer_1_2_6:
                return "1.3.2A"
            else:
                return "1.3.2B"

        # Case 5: Loop at 1.4.3 (Round Name and Purpose)
        if current_step_id == "1.4.3":
            rounds_answer = self.student_state.get("1.4.2", "1")
            if isinstance(rounds_answer, list): rounds_answer = rounds_answer[-1]
            total_rounds = self._text_to_int(rounds_answer)
            
            current_round = self.student_state.get("current_round_counter", 1)
            
            print(f"[DEBUG] Loop 1.4.3: Total Rounds={total_rounds}, Current Round={current_round}")
            
            if current_round < total_rounds:
                self.student_state["current_round_counter"] = current_round + 1
                print(f"[DEBUG] Loop 1.4.3: Continuing loop (Next: 1.4.3)")
                return "1.4.3"
            else:
                if "current_round_counter" in self.student_state:
                    del self.student_state["current_round_counter"]
                print(f"[DEBUG] Loop 1.4.3: Loop complete (Next: CHECKPOINT 1.4)")
                return "CHECKPOINT 1.4"

        # Case 6: Loop at 1.5.2/1.5.3 (Agent Definition)
        if current_step_id == "1.5.3":
            agents_answer = self.student_state.get("1.5.1", "1")
            if isinstance(agents_answer, list): agents_answer = agents_answer[-1]
            total_agents = self._text_to_int(agents_answer)
            
            current_agent = self.student_state.get("current_agent_counter", 1)
            
            if current_agent < total_agents:
                self.student_state["current_agent_counter"] = current_agent + 1
                return "1.5.2"
            else:
                # Don't delete counter yet, might need it for 1.6
                # Actually 1.6 starts fresh, so we can reset or reuse
                # But let's keep it clean
                if "current_agent_counter" in self.student_state:
                    del self.student_state["current_agent_counter"]
                return "CHECKPOINT 1.5"

        # Case 7: Loop at 1.6.3 (Agent Details)
        if current_step_id == "1.6.3":
            agents_answer = self.student_state.get("1.5.1", "1")
            if isinstance(agents_answer, list): agents_answer = agents_answer[-1]
            total_agents = self._text_to_int(agents_answer)
            
            current_agent = self.student_state.get("current_agent_detail_counter", 1)
            
            if current_agent < total_agents:
                self.student_state["current_agent_detail_counter"] = current_agent + 1
                return "1.6.1"
            else:
                if "current_agent_detail_counter" in self.student_state:
                    del self.student_state["current_agent_detail_counter"]
                return "1.7"

        # Case 9: Loop at 2.1.1 (Agent Prompt Creation)
        if current_step_id == "2.1.1":
            agents_answer = self.student_state.get("1.5.1", "1")
            if isinstance(agents_answer, list): agents_answer = agents_answer[-1]
            total_agents = self._text_to_int(agents_answer)
            
            current_agent = self.student_state.get("current_agent_prompt_counter", 1)
            
            if current_agent < total_agents:
                self.student_state["current_agent_prompt_counter"] = current_agent + 1
                return "2.1.1"
            else:
                if "current_agent_prompt_counter" in self.student_state:
                    del self.student_state["current_agent_prompt_counter"]
                return "2.2.1"

        # --- GENERIC LOGIC LAST ---

        # Case 1: Simple ID (no spaces, no parens)
        if " " not in raw_next_step and "(" not in raw_next_step:
            return raw_next_step
            
        # Case 2: Checkpoint (e.g. "CHECKPOINT 1.2")
        if raw_next_step.startswith("CHECKPOINT"):
            return raw_next_step.split("(")[0].strip()

        # Case 8: Loops (simplified fallback)
        return raw_next_step.split(" ")[0]

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

        # Prepare context with loop info
        context = self._get_recent_context()
        
        # Inject loop context
        if step_id == "1.4.3":
            current_round = self.student_state.get("current_round_counter", 1)
            context += f"\n[SYSTEM NOTE]: Current Round: {current_round}"
            
        if step_id in ["1.5.2", "1.5.3"]:
            current_agent = self.student_state.get("current_agent_counter", 1)
            context += f"\n[SYSTEM NOTE]: Current Agent: {current_agent}"
            
        if step_id in ["1.6.1", "1.6.2", "1.6.3"]:
            current_agent = self.student_state.get("current_agent_detail_counter", 1)
            context += f"\n[SYSTEM NOTE]: Current Agent: {current_agent}"

        # Substitute placeholders in the question
        question_text = self._substitute_placeholders(step.required_output, step_id)

        # 1. Ask the question (LLM may add RCM flavor)
        question = self.student_handler.ask_question(
            question_text,
            step.rcm_cue,
            context=context
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
        # If this is a looping step (like 1.4.3), we should append or store in a list
        if step_id in self.student_state:
            current_val = self.student_state[step_id]
            if isinstance(current_val, list):
                current_val.append(student_answer)
                self.student_state[step_id] = current_val
            else:
                # Convert to list
                self.student_state[step_id] = [current_val, student_answer]
        else:
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

        # Filter out internal counters (keys starting with "current_")
        valid_items = {k: v for k, v in self.student_state.items() if not k.startswith("current_")}
        
        recent_items = list(valid_items.items())[-last_n:]
        context_lines = []
        for step_id, answer in recent_items:
            # Handle non-string answers (lists, ints, etc.)
            if isinstance(answer, list):
                answer_str = " | ".join(str(x) for x in answer)
            else:
                answer_str = str(answer)
                
            # Truncate long answers
            short_answer = answer_str[:100] + "..." if len(answer_str) > 100 else answer_str
            context_lines.append(f"{step_id}: {short_answer}")

        return "\n".join(context_lines)

    def _substitute_placeholders(self, text: str, step_id: str) -> str:
        """
        Substitute placeholders in text with actual values.
        
        Supported placeholders:
        - [n]: Current loop counter (round or agent number)
        - [Identifier]: Current agent identifier
        - [A/B]: Concept A or B (if available)
        """
        if not text:
            return ""
            
        # Replace [n] with current counter
        if "[n]" in text:
            counter = 1
            if "1.4" in step_id:
                counter = self.student_state.get("current_round_counter", 1)
            elif "1.5" in step_id:
                counter = self.student_state.get("current_agent_counter", 1)
            elif "1.6" in step_id:
                counter = self.student_state.get("current_agent_detail_counter", 1)
            elif "2.1" in step_id:
                # Phase 2.1 iterates through agents
                counter = self.student_state.get("current_agent_prompt_counter", 1)
            elif "1.7" in step_id:
                # Step 1.7 asks for all rounds at once or needs to be treated as a single question
                # We'll replace [n] with "1, 2, 3..." based on total rounds
                rounds_answer = self.student_state.get("1.4.2", "1")
                if isinstance(rounds_answer, list): rounds_answer = rounds_answer[-1]
                total_rounds = self._text_to_int(rounds_answer)
                counter = ", ".join(str(i) for i in range(1, total_rounds + 1))
            
            text = text.replace("[n]", str(counter))
            
        # Replace [Identifier] with current agent name
        if "[Identifier]" in text:
            # We need to find which agent we are currently processing
            # This depends on the phase and loop
            agent_name = "Agent"
            
            # Get the list of agents from 1.5.2
            agents_list = self.student_state.get("1.5.2", [])
            if not isinstance(agents_list, list):
                agents_list = [agents_list]
                
            # Determine which index we need
            idx = 0
            if "1.6" in step_id:
                counter = self.student_state.get("current_agent_detail_counter", 1)
                idx = counter - 1
            elif "2.1" in step_id:
                counter = self.student_state.get("current_agent_prompt_counter", 1)
                idx = counter - 1
                
            if 0 <= idx < len(agents_list):
                agent_name = agents_list[idx]
                
            text = text.replace("[Identifier]", str(agent_name))

        # Special handling for Step 2.1.1 Template Generation
        if "2.1.1" in step_id and "[Goal]" in text and "[Persona]" in text:
            # We need to fill in the template with data from Phase 1
            
            # Get current agent index
            counter = self.student_state.get("current_agent_prompt_counter", 1)
            idx = counter - 1
            
            # Get Goal (1.6.1)
            goals = self.student_state.get("1.6.1", [])
            if not isinstance(goals, list): goals = [goals]
            goal = goals[idx] if 0 <= idx < len(goals) else "[Goal not found]"
            
            # Get Persona (1.6.2)
            personas = self.student_state.get("1.6.2", [])
            if not isinstance(personas, list): personas = [personas]
            persona = personas[idx] if 0 <= idx < len(personas) else "[Persona not found]"
            
            text = text.replace("[Goal]", str(goal))
            text = text.replace("[Persona]", str(persona))
            
        return text

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
            "runtime-files"
        )

    # Use the COMPLETE runtime file
    complete_path = os.path.join(runtime_base_path, "B42_Runtime_Logic_v2.0-COMPLETE.txt")

    # Parse runtime files
    print("Loading runtime files...")
    # The Runtime class constructor expects 3 paths, but we only have one COMPLETE file.
    # We need to update the Runtime class to accept a single file or handle this.
    # For now, let's pass the same file 3 times or update Runtime.
    # Let's check Runtime.__init__ again.
    
    # Actually, let's update Runtime to handle a single file or list of files.
    # But first, let's see if we can just pass the same file 3 times as a hack, 
    # or if we should modify Runtime.
    # Modifying Runtime is cleaner.
    
    runtime = Runtime(complete_path, complete_path, complete_path) # Hack for now to avoid changing Runtime signature immediately
    # Wait, if we pass the same file 3 times, it will parse it 3 times.
    # That's inefficient but safe since it's a dict update.
    
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
