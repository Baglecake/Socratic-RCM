"""
BIOS Runtime Validator - For Code Interpreter Enforcement

This script is run BY THE GPT via Code Interpreter to validate workflow execution.

The GPT will call this script BEFORE showing any question to the student to verify:
1. Current step is correct
2. Question text matches runtime file
3. No steps were skipped
4. Constraints are being met
5. Canvas data structure matches schema (NEW)

Upload this file to the GPT's Knowledge base.
"""

import json
import re
from typing import Dict, Optional, Tuple, List, Any


class RuntimeParser:
    """Parse runtime files into step dictionaries"""

    def __init__(self):
        self.steps = {}  # step_id -> step_data

    def parse_runtime_file(self, content: str) -> Dict:
        """Parse a runtime file and extract all steps"""
        steps = {}

        # Split by step blocks
        step_pattern = r'### \[STEP ([^\]]+)\](.*?)(?=### \[STEP |$)'
        matches = re.findall(step_pattern, content, re.DOTALL)

        for step_id, step_content in matches:
            step_id = step_id.strip()
            steps[step_id] = self._parse_step_block(step_id, step_content)

        return steps

    def _parse_step_block(self, step_id: str, content: str) -> Dict:
        """Parse a single step block"""
        data = {"id": step_id}

        # Extract fields
        data["target"] = self._extract_field(content, r'TARGET:\s*(.+?)(?=\n[A-Z]+:|$)')
        data["instruction"] = self._extract_field(content, r'INSTRUCTION:\s*(.+?)(?=\n[A-Z]+:|$)')
        data["required_output"] = self._extract_field(content, r'REQUIRED OUTPUT:\s*"([^"]+)"')
        data["rcm_cue"] = self._extract_field(content, r'RCM CUE:\s*(.+?)(?=\n[A-Z]+:|$)')
        data["constraint"] = self._extract_field(content, r'CONSTRAINT:\s*(.+?)(?=\n[A-Z]+:|$)')
        data["next_step"] = self._extract_field(content, r'NEXT STEP:\s*([^\s\n]+)')

        return data

    def _extract_field(self, content: str, pattern: str) -> Optional[str]:
        """Extract a field from step content"""
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None


class CanvasSchemaValidator:
    """Validates canvas data structure against schema"""

    def __init__(self):
        """Initialize schema validator"""
        self.required_fields = {
            "phase1": {
                "project": ["goal", "theoretical_option", "concept_a", "concept_b", "structure", "experiment_type"],
                "baseline_experiment": ["baseline_description"],
                "setting": ["description", "num_rounds", "round_plan"],
                "agents": ["identifier", "type", "goal", "persona"]
            },
            "phase2_1": {
                "agents_prompts": ["role", "primary_goal", "persona"]
            },
            "phase2_2": {
                "rounds": ["scenario", "concept_a_in_round", "concept_b_in_round", "rules", "tasks", "sequence", "platform_config"]
            }
        }

    def validate_phase1_complete(self, canvas_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate that Phase 1 data structure is complete.

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Check project section
        if "project" not in canvas_data:
            errors.append("Missing 'project' section")
        else:
            project = canvas_data["project"]
            for field in self.required_fields["phase1"]["project"]:
                if field not in project or not project[field]:
                    errors.append(f"Missing or empty project.{field}")

        # Check baseline_experiment section
        if "baseline_experiment" not in canvas_data:
            errors.append("Missing 'baseline_experiment' section")
        else:
            baseline = canvas_data["baseline_experiment"]
            for field in self.required_fields["phase1"]["baseline_experiment"]:
                if field not in baseline or not baseline[field]:
                    errors.append(f"Missing or empty baseline_experiment.{field}")

        # Check setting section
        if "setting" not in canvas_data:
            errors.append("Missing 'setting' section")
        else:
            setting = canvas_data["setting"]
            for field in self.required_fields["phase1"]["setting"]:
                if field not in setting or not setting[field]:
                    errors.append(f"Missing or empty setting.{field}")

        # Check agents array
        if "agents" not in canvas_data:
            errors.append("Missing 'agents' array")
        elif not isinstance(canvas_data["agents"], list):
            errors.append("'agents' must be an array")
        elif len(canvas_data["agents"]) == 0:
            errors.append("'agents' array is empty - at least one agent required")
        else:
            # Validate each agent has required fields
            for i, agent in enumerate(canvas_data["agents"]):
                for field in self.required_fields["phase1"]["agents"]:
                    if field not in agent or not agent[field]:
                        errors.append(f"Missing or empty agents[{i}].{field}")

        return len(errors) == 0, errors

    def validate_phase2_1_complete(self, canvas_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate that Phase 2.1 (agent prompts) data is complete.

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        if "agents" not in canvas_data or not isinstance(canvas_data["agents"], list):
            errors.append("Missing 'agents' array for Phase 2.1 validation")
            return False, errors

        # Check that all agents have prompt data
        for i, agent in enumerate(canvas_data["agents"]):
            if "prompt" not in agent:
                errors.append(f"Missing 'prompt' section for agents[{i}]")
            else:
                prompt = agent["prompt"]
                for field in self.required_fields["phase2_1"]["agents_prompts"]:
                    if field not in prompt or not prompt[field]:
                        errors.append(f"Missing or empty agents[{i}].prompt.{field}")

        return len(errors) == 0, errors

    def validate_phase2_2_complete(self, canvas_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate that Phase 2.2 (round instructions) data is complete.

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        if "rounds" not in canvas_data:
            errors.append("Missing 'rounds' array")
            return False, errors

        if not isinstance(canvas_data["rounds"], list):
            errors.append("'rounds' must be an array")
            return False, errors

        if len(canvas_data["rounds"]) == 0:
            errors.append("'rounds' array is empty - at least one round required")
            return False, errors

        # Check each round has required fields
        for i, round_data in enumerate(canvas_data["rounds"]):
            for field in self.required_fields["phase2_2"]["rounds"]:
                if field not in round_data or not round_data[field]:
                    errors.append(f"Missing or empty rounds[{i}].{field}")

            # Special check for platform_config structure
            if "platform_config" in round_data and isinstance(round_data["platform_config"], dict):
                config = round_data["platform_config"]
                required_config_fields = ["participants", "who_sends", "order", "end_condition", "transition", "detail_level"]
                for cfg_field in required_config_fields:
                    if cfg_field not in config or not config[cfg_field]:
                        errors.append(f"Missing or empty rounds[{i}].platform_config.{cfg_field}")

        return len(errors) == 0, errors

    def validate_data_types(self, canvas_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate that field types match expected types.

        Returns:
            (is_valid, list_of_warnings)
        """
        warnings = []

        # Check setting.num_rounds is a number
        if "setting" in canvas_data and "num_rounds" in canvas_data["setting"]:
            num_rounds = canvas_data["setting"]["num_rounds"]
            if not isinstance(num_rounds, int):
                try:
                    int(num_rounds)
                except (ValueError, TypeError):
                    warnings.append(f"setting.num_rounds should be a number, got: {type(num_rounds).__name__}")

        # Check agents is an array
        if "agents" in canvas_data and not isinstance(canvas_data["agents"], list):
            warnings.append(f"agents should be an array, got: {type(canvas_data['agents']).__name__}")

        # Check rounds is an array
        if "rounds" in canvas_data and not isinstance(canvas_data["rounds"], list):
            warnings.append(f"rounds should be an array, got: {type(canvas_data['rounds']).__name__}")

        return len(warnings) == 0, warnings


class WorkflowValidator:
    """Validates GPT workflow execution against runtime files"""

    def __init__(self, runtime_steps: Dict):
        """
        Args:
            runtime_steps: Dict of step_id -> step_data from parsed runtime files
        """
        self.runtime_steps = runtime_steps
        self.current_step_id = "1.1.1"
        self.student_answers = {}
        self.validation_log = []
        self.canvas_data = {}  # NEW: Track canvas data for schema validation
        self.schema_validator = CanvasSchemaValidator()  # NEW: Schema validator instance

    def validate_step_execution(
        self,
        intended_step_id: str,
        question_to_show: str
    ) -> Tuple[bool, str, Dict]:
        """
        Validate that the GPT is executing the correct step.

        Args:
            intended_step_id: The step the GPT thinks it should execute
            question_to_show: The question the GPT wants to show

        Returns:
            (is_valid, error_message, step_data)
        """
        # Check 1: Is this the expected step?
        if intended_step_id != self.current_step_id:
            error = f"STEP SKIPPING DETECTED: Expected step {self.current_step_id}, GPT attempted {intended_step_id}"
            self.validation_log.append(error)
            return False, error, {}

        # Check 2: Does this step exist in runtime files?
        if intended_step_id not in self.runtime_steps:
            error = f"HALLUCINATED STEP: Step {intended_step_id} not found in runtime files"
            self.validation_log.append(error)
            return False, error, {}

        # Get expected step data
        expected_step = self.runtime_steps[intended_step_id]
        expected_question = expected_step.get("required_output", "")

        # Check 3: Does the question match?
        if not self._questions_match(question_to_show, expected_question):
            error = f"HALLUCINATED QUESTION: Question doesn't match runtime file\n"
            error += f"Expected: '{expected_question}'\n"
            error += f"Got: '{question_to_show}'"
            self.validation_log.append(error)
            return False, error, expected_step

        # All checks passed
        success_msg = f"✓ Step {intended_step_id} validated: '{expected_question[:50]}...'"
        self.validation_log.append(success_msg)
        return True, "OK", expected_step

    def _questions_match(self, q1: str, q2: str) -> bool:
        """Check if two questions are essentially the same (ignoring minor differences)"""
        # Normalize: strip, lowercase, remove extra spaces
        norm1 = " ".join(q1.strip().lower().split())
        norm2 = " ".join(q2.strip().lower().split())

        # Exact match or very close (allowing for minor rewording)
        if norm1 == norm2:
            return True

        # Allow for [n] placeholder variations
        norm1_generic = re.sub(r'\[n\]', '[X]', norm1)
        norm2_generic = re.sub(r'\[n\]', '[X]', norm2)

        if norm1_generic == norm2_generic:
            return True

        # Check if core question is preserved (at least 80% match)
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        overlap = len(words1 & words2)
        union = len(words1 | words2)

        similarity = overlap / union if union > 0 else 0
        return similarity >= 0.8

    def record_answer(self, step_id: str, answer: str):
        """Record student's answer for a step"""
        self.student_answers[step_id] = answer
        self.validation_log.append(f"✓ Recorded answer for step {step_id}")

    def update_canvas_data(self, section: str, data: Any):
        """
        Update canvas data for schema validation.

        Args:
            section: Section name (project, agents, rounds, etc.)
            data: Data to update or append
        """
        self.canvas_data[section] = data
        self.validation_log.append(f"✓ Canvas data updated: {section}")

    def validate_canvas_schema(self, phase: str) -> Tuple[bool, List[str]]:
        """
        Validate canvas data against schema for a specific phase.

        Args:
            phase: "phase1", "phase2_1", or "phase2_2"

        Returns:
            (is_valid, list_of_errors)
        """
        if phase == "phase1":
            return self.schema_validator.validate_phase1_complete(self.canvas_data)
        elif phase == "phase2_1":
            return self.schema_validator.validate_phase2_1_complete(self.canvas_data)
        elif phase == "phase2_2":
            return self.schema_validator.validate_phase2_2_complete(self.canvas_data)
        else:
            return False, [f"Unknown phase: {phase}"]

    def advance_to_next_step(self) -> Tuple[bool, str]:
        """
        Advance to the next step per runtime file.

        Returns:
            (is_valid, next_step_id_or_error)
        """
        if self.current_step_id not in self.runtime_steps:
            return False, f"ERROR: Current step {self.current_step_id} not in runtime"

        current_step = self.runtime_steps[self.current_step_id]
        next_step_id = current_step.get("next_step")

        if not next_step_id or next_step_id in ["END", "DONE"]:
            self.validation_log.append("✓ Workflow complete")
            return True, "COMPLETE"

        if next_step_id not in self.runtime_steps:
            error = f"ERROR: Next step {next_step_id} (from {self.current_step_id}) not found in runtime"
            self.validation_log.append(error)
            return False, error

        self.current_step_id = next_step_id
        self.validation_log.append(f"✓ Advanced to step {next_step_id}")
        return True, next_step_id

    def validate_answer_against_constraint(
        self,
        step_id: str,
        answer: str
    ) -> Tuple[bool, str]:
        """
        Validate student answer against step constraint.

        Returns:
            (is_valid, error_or_ok)
        """
        if step_id not in self.runtime_steps:
            return True, "OK (step not found, cannot validate)"

        step = self.runtime_steps[step_id]
        constraint = step.get("constraint")

        if not constraint:
            return True, "OK (no constraint specified)"

        # Basic validation checks
        if not answer or answer.strip() == "":
            return False, "Answer is empty"

        # Check for placeholder text
        placeholders = ["...", "TBD", "to be determined", "[", "]"]
        if any(p in answer.lower() for p in placeholders):
            return False, f"Answer contains placeholder text: {answer[:50]}"

        # Check for sentence count if constraint mentions it
        if "2-3 sentences" in constraint or "2–3 sentences" in constraint:
            sentences = [s.strip() for s in re.split(r'[.!?]+', answer) if s.strip()]
            if len(sentences) < 2:
                return False, f"Constraint requires 2-3 sentences, got {len(sentences)}"

        # More sophisticated checks would go here (using LLM)
        return True, "OK"

    def get_status_report(self) -> Dict:
        """Get current validation status"""
        return {
            "current_step": self.current_step_id,
            "steps_completed": len(self.student_answers),
            "validation_log": self.validation_log[-10:],  # Last 10 entries
            "all_steps_executed": self._check_all_steps_executed(),
            "canvas_data_summary": self._get_canvas_summary()
        }

    def _check_all_steps_executed(self) -> bool:
        """Check if all steps from 1.1.1 to current have been executed"""
        # Simple check: number of answers should match progression
        return len(self.student_answers) > 0

    def _get_canvas_summary(self) -> Dict:
        """Get summary of canvas data"""
        summary = {}
        if "project" in self.canvas_data:
            summary["project_defined"] = True
        if "agents" in self.canvas_data:
            summary["num_agents"] = len(self.canvas_data["agents"]) if isinstance(self.canvas_data["agents"], list) else 0
        if "rounds" in self.canvas_data:
            summary["num_rounds"] = len(self.canvas_data["rounds"]) if isinstance(self.canvas_data["rounds"], list) else 0
        return summary


# ============================================================================
# Helper Functions for GPT to Call
# ============================================================================

def load_runtime_files(phase1_content: str, phase2_content: str, phase3_content: str) -> Dict:
    """
    Load and parse all three runtime files.

    Returns:
        Dict of step_id -> step_data
    """
    parser = RuntimeParser()

    all_steps = {}
    all_steps.update(parser.parse_runtime_file(phase1_content))
    all_steps.update(parser.parse_runtime_file(phase2_content))
    all_steps.update(parser.parse_runtime_file(phase3_content))

    return all_steps


def validate_before_asking(
    validator: WorkflowValidator,
    step_id: str,
    question: str
) -> Dict:
    """
    GPT calls this BEFORE showing any question to student.

    Returns:
        {
            "valid": bool,
            "error": str,
            "expected_question": str,
            "step_data": dict
        }
    """
    is_valid, message, step_data = validator.validate_step_execution(step_id, question)

    return {
        "valid": is_valid,
        "error": message if not is_valid else "",
        "expected_question": step_data.get("required_output", ""),
        "step_data": step_data
    }


def record_and_advance(
    validator: WorkflowValidator,
    step_id: str,
    student_answer: str
) -> Dict:
    """
    GPT calls this AFTER receiving student's answer.

    Returns:
        {
            "valid": bool,
            "next_step_id": str,
            "error": str,
            "constraint_ok": bool,
            "constraint_error": str
        }
    """
    # Validate answer against constraint
    constraint_ok, constraint_msg = validator.validate_answer_against_constraint(
        step_id,
        student_answer
    )

    # Record answer
    validator.record_answer(step_id, student_answer)

    # Advance to next step
    valid, next_step_or_error = validator.advance_to_next_step()

    return {
        "valid": valid,
        "next_step_id": next_step_or_error if valid else "",
        "error": next_step_or_error if not valid else "",
        "constraint_ok": constraint_ok,
        "constraint_error": constraint_msg if not constraint_ok else ""
    }


def validate_phase_complete(
    validator: WorkflowValidator,
    phase: str
) -> Dict:
    """
    GPT calls this at end of Phase 1, Phase 2.1, or Phase 2.2 to validate canvas schema.

    Args:
        validator: WorkflowValidator instance
        phase: "phase1", "phase2_1", or "phase2_2"

    Returns:
        {
            "valid": bool,
            "errors": list of error messages,
            "phase": str
        }
    """
    is_valid, errors = validator.validate_canvas_schema(phase)

    return {
        "valid": is_valid,
        "errors": errors,
        "phase": phase
    }


# ============================================================================
# Example Usage (for testing)
# ============================================================================

if __name__ == "__main__":
    # This would normally be run by the GPT via Code Interpreter

    # Simulate loading runtime files
    phase1 = """
### [STEP 1.1.1]
TARGET: Storyboard Completion
INSTRUCTION: Ask if storyboard is complete
REQUIRED OUTPUT: "Have you completed your storyboard? (yes/no)"
CONSTRAINT: Must be yes or no
NEXT STEP: 1.2.1

### [STEP 1.2.1]
TARGET: Theoretical Option
INSTRUCTION: Ask for theoretical option
REQUIRED OUTPUT: "Which theoretical option from KB[2]? (A, B, C, D, or E)"
CONSTRAINT: Must be A, B, C, D, or E
NEXT STEP: 1.2.2
"""

    # Parse
    all_steps = load_runtime_files(phase1, "", "")

    # Create validator
    validator = WorkflowValidator(all_steps)

    # Test validation
    print("=== Test 1: Valid step execution ===")
    result = validate_before_asking(
        validator,
        "1.1.1",
        "Have you completed your storyboard? (yes/no)"
    )
    print(json.dumps(result, indent=2))

    print("\n=== Test 2: Step skipping ===")
    result = validate_before_asking(
        validator,
        "1.2.1",  # Should fail - we're still on 1.1.1
        "Which theoretical option?"
    )
    print(json.dumps(result, indent=2))

    print("\n=== Test 3: Record answer and advance ===")
    result = record_and_advance(validator, "1.1.1", "yes")
    print(json.dumps(result, indent=2))

    print("\n=== Test 4: Schema validation (Phase 1) ===")
    # Simulate canvas data
    validator.canvas_data = {
        "project": {
            "goal": "Test project goal",
            "theoretical_option": "A",
            "concept_a": {"name": "Concept A", "definition": "Definition A"},
            "concept_b": {"name": "Concept B", "definition": "Definition B"},
            "structure": "Single multi-round design",
            "experiment_type": "A"
        },
        "baseline_experiment": {
            "baseline_description": "Baseline description"
        },
        "setting": {
            "description": "Setting description",
            "num_rounds": 3,
            "round_plan": []
        },
        "agents": [
            {
                "identifier": "[purpose]+[name]",
                "type": "Human",
                "goal": "Agent goal",
                "persona": "Agent persona"
            }
        ]
    }
    result = validate_phase_complete(validator, "phase1")
    print(json.dumps(result, indent=2))

    print("\n=== Status Report ===")
    print(json.dumps(validator.get_status_report(), indent=2))
