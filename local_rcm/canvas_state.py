"""
Canvas State - Mirrors CANVAS_DATA_SCHEMA.md

This module implements the canvas state object that accumulates student data
progressively throughout the workflow.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
import json


@dataclass
class ConceptDefinition:
    name: str = ""
    definition: str = ""


@dataclass
class VariableDefinition:
    name: str = ""
    baseline: str = ""
    experimental: str = ""
    rationale: str = ""


@dataclass
class ProjectInfo:
    goal: str = ""
    theoretical_option: str = ""
    theoretical_option_label: str = ""
    concept_a: Optional[ConceptDefinition] = None
    concept_b: Optional[ConceptDefinition] = None
    design_approach: str = ""
    variable: Optional[VariableDefinition] = None
    setting: str = ""
    rounds_count: int = 0
    rounds_plan: str = ""


@dataclass
class AgentDefinition:
    identifier: str = ""
    goal: str = ""
    persona: str = ""
    prompt: str = ""


@dataclass
class PlatformConfig:
    participants: str = ""
    who_sends: str = ""
    order: str = ""
    end_condition: str = ""
    transition: str = ""
    detail_level: str = ""
    creativity: str = ""
    ask_questions: bool = False
    self_reflection: bool = False
    isolated: bool = False
    model: str = ""


@dataclass
class RoundDefinition:
    round_number: int
    scenario: str = ""
    concept_a_manifestation: str = ""
    concept_b_manifestation: str = ""
    rules: str = ""
    tasks: str = ""
    sequence: str = ""
    behaviors: str = ""
    compiled_instructions: str = ""
    platform_config: Optional[PlatformConfig] = None


@dataclass
class HelperFunctions:
    moderator_function: str = ""
    analyst_function: str = ""
    non_anthropomorphic_cues: str = ""
    self_reflection_prompts: str = ""


@dataclass
class WorkflowStatus:
    phase1_complete: bool = False
    phase2_complete: bool = False
    phase3_complete: bool = False
    ready_for_export: bool = False


@dataclass
class CanvasState:
    """Complete canvas state mirroring CANVAS_DATA_SCHEMA.md"""
    project: ProjectInfo = field(default_factory=ProjectInfo)
    agents: List[AgentDefinition] = field(default_factory=list)
    rounds: List[RoundDefinition] = field(default_factory=list)
    helpers: HelperFunctions = field(default_factory=HelperFunctions)
    status: WorkflowStatus = field(default_factory=WorkflowStatus)

    def to_dict(self) -> Dict:
        """Convert canvas state to dictionary"""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Convert canvas state to JSON string"""
        return json.dumps(self.to_dict(), indent=indent)


def apply_canvas_update(
    canvas: CanvasState,
    update: Dict,
    student_state: Dict[str, str]
) -> CanvasState:
    """
    Apply a CANVAS_UPDATE to the canvas state.

    Args:
        canvas: Current canvas state
        update: The CANVAS_UPDATE block (section, action, data template)
        student_state: Dict of step_id -> student_answer

    Returns:
        Updated canvas state
    """
    section = update.get("section")
    action = update.get("action")

    # This is a simplified version - in production you'd parse the
    # actual data templates from the CANVAS_UPDATE blocks and map
    # student answers to the correct fields

    if section == "project":
        if "goal" in update.get("raw_content", ""):
            # Extract the step ID that contains the goal
            # For now, we'll use a simple approach
            pass

    elif section == "agents":
        # Handle agent additions
        pass

    elif section == "rounds":
        # Handle round data
        pass

    elif section == "helpers":
        # Handle helper functions
        pass

    elif section == "status":
        # Update workflow status
        if "phase1_complete" in update.get("raw_content", ""):
            canvas.status.phase1_complete = True
        elif "phase2_complete" in update.get("raw_content", ""):
            canvas.status.phase2_complete = True
        elif "phase3_complete" in update.get("raw_content", ""):
            canvas.status.phase3_complete = True

    return canvas


def compile_final_document(canvas: CanvasState) -> str:
    """
    Compile the final Chatstorm-ready document from canvas state.
    This implements the CANVAS_RETRIEVE functionality.
    """
    doc = []

    # Project Goal
    doc.append("=== PROJECT GOAL ===")
    doc.append(canvas.project.goal)
    doc.append("")

    # Theoretical Framework
    doc.append("=== THEORETICAL FRAMEWORK ===")
    doc.append(f"Option: {canvas.project.theoretical_option_label}")
    doc.append("")

    # Concepts
    doc.append("=== CONCEPTS ===")
    if canvas.project.concept_a:
        doc.append(f"Concept A: {canvas.project.concept_a.name}")
        doc.append(f"Definition: {canvas.project.concept_a.definition}")
        doc.append("")
    if canvas.project.concept_b:
        doc.append(f"Concept B: {canvas.project.concept_b.name}")
        doc.append(f"Definition: {canvas.project.concept_b.definition}")
        doc.append("")

    # Variable (if experimental design)
    if canvas.project.variable:
        doc.append("=== VARIABLE ===")
        doc.append(f"Variable: {canvas.project.variable.name}")
        doc.append(f"Baseline: {canvas.project.variable.baseline}")
        doc.append(f"Experimental: {canvas.project.variable.experimental}")
        doc.append(f"Rationale: {canvas.project.variable.rationale}")
        doc.append("")

    # Setting
    doc.append("=== SETTING ===")
    doc.append(canvas.project.setting)
    doc.append("")

    # Agents
    doc.append("=== AGENTS ===")
    for agent in canvas.agents:
        doc.append(f"\n{agent.identifier}:")
        doc.append(f"Goal: {agent.goal}")
        doc.append(f"Persona: {agent.persona}")
        doc.append(f"Prompt: {agent.prompt}")
        doc.append("")

    # Rounds
    for round_def in canvas.rounds:
        doc.append(f"=== ROUND {round_def.round_number} ===")
        doc.append(f"Scenario: {round_def.scenario}")
        if round_def.concept_a_manifestation:
            doc.append(f"Concept A Manifestation: {round_def.concept_a_manifestation}")
        if round_def.concept_b_manifestation:
            doc.append(f"Concept B Manifestation: {round_def.concept_b_manifestation}")
        if round_def.rules:
            doc.append(f"Rules: {round_def.rules}")
        if round_def.tasks:
            doc.append(f"Tasks: {round_def.tasks}")
        if round_def.sequence:
            doc.append(f"Sequence: {round_def.sequence}")

        if round_def.platform_config:
            doc.append("\nPlatform Configuration:")
            config = round_def.platform_config
            doc.append(f"  Participants: {config.participants}")
            doc.append(f"  Who Sends: {config.who_sends}")
            doc.append(f"  Order: {config.order}")
            doc.append(f"  End Condition: {config.end_condition}")
            doc.append(f"  Transition: {config.transition}")
            doc.append(f"  Detail Level: {config.detail_level}")
        doc.append("")

    # Helper Functions (if any)
    if canvas.helpers.moderator_function or canvas.helpers.analyst_function:
        doc.append("=== HELPER FUNCTIONS ===")
        if canvas.helpers.moderator_function:
            doc.append(f"Moderator: {canvas.helpers.moderator_function}")
        if canvas.helpers.analyst_function:
            doc.append(f"Analyst: {canvas.helpers.analyst_function}")
        doc.append("")

    return "\n".join(doc)


if __name__ == "__main__":
    # Test canvas state
    canvas = CanvasState()

    # Add some test data
    canvas.project.goal = "Test project goal"
    canvas.project.concept_a = ConceptDefinition(
        name="Class Domination",
        definition="Test definition"
    )

    canvas.agents.append(AgentDefinition(
        identifier="Worker+Alice",
        goal="Survive in capitalist system",
        persona="Factory worker",
        prompt="You are Alice, a factory worker..."
    ))

    # Test compilation
    print("=== Canvas State (JSON) ===")
    print(canvas.to_json())

    print("\n=== Final Document ===")
    print(compile_final_document(canvas))
