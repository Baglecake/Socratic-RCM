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


def compile_canvas_from_student_state(student_state: Dict[str, Any]) -> CanvasState:
    """
    Build a complete CanvasState from the collected student answers.
    Call this after Phase 1 completes to populate the canvas for Phase 2.

    Args:
        student_state: Dict of step_id -> answer (from orchestrator.student_state)

    Returns:
        Populated CanvasState
    """
    canvas = CanvasState()

    # --- Project Info ---
    canvas.project.goal = student_state.get("1.2.2", "")
    canvas.project.theoretical_option = student_state.get("1.2.1", "")

    # Map option letter to label
    option_labels = {
        "A": "Class Conflict / Alienation",
        "B": "Cultural Systems",
        "C": "Institutional Power",
        "D": "Network Dynamics",
        "E": "Custom Framework"
    }
    opt = student_state.get("1.2.1", "").upper().strip()
    canvas.project.theoretical_option_label = option_labels.get(opt, opt)

    # Concepts A and B
    canvas.project.concept_a = ConceptDefinition(
        name="Concept A",
        definition=student_state.get("1.2.3", "")
    )
    canvas.project.concept_b = ConceptDefinition(
        name="Concept B",
        definition=student_state.get("1.2.4", "")
    )

    # Design approach
    canvas.project.design_approach = student_state.get("1.2.5", "")

    # Variable (from Type A experiment path)
    if "1.3.2A" in student_state:
        canvas.project.variable = VariableDefinition(
            name="Modified Variable",
            baseline=student_state.get("1.3.1", ""),
            experimental=student_state.get("1.3.2A", ""),
            rationale=student_state.get("1.3.3", "")
        )
    elif "1.3.2B" in student_state:
        canvas.project.variable = VariableDefinition(
            name="New Design",
            baseline=student_state.get("1.3.1", ""),
            experimental=student_state.get("1.3.2B", ""),
            rationale=student_state.get("1.3.3", "")
        )

    # Setting
    canvas.project.setting = student_state.get("1.4.1", "")

    # Rounds
    rounds_count_str = student_state.get("1.4.2", "1")
    try:
        canvas.project.rounds_count = int(rounds_count_str)
    except:
        canvas.project.rounds_count = 1

    round_plans = student_state.get("1.4.3", [])
    if isinstance(round_plans, str):
        round_plans = [round_plans]
    canvas.project.rounds_plan = " | ".join(round_plans)

    # Create round definitions
    for i, plan in enumerate(round_plans):
        canvas.rounds.append(RoundDefinition(
            round_number=i + 1,
            scenario=plan
        ))

    # --- Agents ---
    agent_ids = student_state.get("1.5.2", [])
    agent_types = student_state.get("1.5.3", [])
    agent_goals = student_state.get("1.6.1", [])
    agent_personas = student_state.get("1.6.2", [])
    agent_behaviors = student_state.get("1.6.3", [])

    # Normalize to lists
    if isinstance(agent_ids, str): agent_ids = [agent_ids]
    if isinstance(agent_types, str): agent_types = [agent_types]
    if isinstance(agent_goals, str): agent_goals = [agent_goals]
    if isinstance(agent_personas, str): agent_personas = [agent_personas]
    if isinstance(agent_behaviors, str): agent_behaviors = [agent_behaviors]

    for i, agent_id in enumerate(agent_ids):
        agent = AgentDefinition(
            identifier=agent_id,
            goal=agent_goals[i] if i < len(agent_goals) else "",
            persona=agent_personas[i] if i < len(agent_personas) else "",
            prompt=""  # Will be generated in Phase 2
        )
        canvas.agents.append(agent)

    # --- Helpers ---
    helpers_answer = student_state.get("1.7", "")
    if "self-reflect" in helpers_answer.lower():
        canvas.helpers.self_reflection_prompts = "Enabled"
    if "analyst" in helpers_answer.lower():
        canvas.helpers.analyst_function = "Enabled"
    if "moderator" in helpers_answer.lower():
        canvas.helpers.moderator_function = "Enabled"
    if "non-anthropomorphic" in helpers_answer.lower():
        canvas.helpers.non_anthropomorphic_cues = "Enabled"

    # --- Status ---
    if "1.8" in student_state:
        canvas.status.phase1_complete = True

    # =========================================================================
    # PHASE 2 DATA
    # =========================================================================

    # Agent prompts from 2.1.1
    agent_prompts = student_state.get("2.1.1", [])
    if isinstance(agent_prompts, str):
        agent_prompts = [agent_prompts]
    # The prompts are confirmations - we need to build actual prompts from Phase 1 data
    for i, agent in enumerate(canvas.agents):
        agent.prompt = f"ROLE: You are {agent.identifier}\nPRIMARY GOAL: {agent.goal}\nPERSONA: {agent.persona}"

    # Round details from 2.2.x
    def get_list_item(key: str, index: int) -> str:
        val = student_state.get(key, [])
        if isinstance(val, str):
            return val if index == 0 else ""
        if isinstance(val, list) and index < len(val):
            return val[index]
        return ""

    for i, round_def in enumerate(canvas.rounds):
        round_def.concept_a_manifestation = get_list_item("2.2.2", i)
        round_def.concept_b_manifestation = get_list_item("2.2.3", i)
        round_def.rules = get_list_item("2.2.4", i)
        round_def.tasks = get_list_item("2.2.5", i)
        round_def.sequence = get_list_item("2.2.6", i)
        round_def.behaviors = get_list_item("2.2.7", i)
        round_def.compiled_instructions = get_list_item("2.2.8", i)

        # Platform config from 2.2.9-2.2.18
        round_def.platform_config = PlatformConfig(
            participants=get_list_item("2.2.9", i),
            who_sends=get_list_item("2.2.10", i),
            order=get_list_item("2.2.11", i),
            end_condition=get_list_item("2.2.12", i),
            transition=get_list_item("2.2.13", i),
            detail_level=get_list_item("2.2.14", i),
            creativity=get_list_item("2.2.15", i),
            ask_questions=get_list_item("2.2.16", i).lower() == "yes",
            self_reflection=get_list_item("2.2.17", i).lower() == "yes",
            isolated=False,
            model=get_list_item("2.2.18", i)
        )

    # Helper templates from 2.3.x
    if "2.3.1" in student_state:
        canvas.helpers.moderator_function = student_state.get("2.3.1", "")
    if "2.3.2" in student_state:
        canvas.helpers.analyst_function = student_state.get("2.3.2", "")
    if "2.3.3" in student_state:
        canvas.helpers.non_anthropomorphic_cues = student_state.get("2.3.3", "")
    if "2.3.4" in student_state:
        canvas.helpers.self_reflection_prompts = student_state.get("2.3.4", "")

    # Update status
    if "2.3.5" in student_state:
        canvas.status.phase2_complete = True
    if "3.3" in student_state:
        canvas.status.phase3_complete = True
        canvas.status.ready_for_export = True

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

    # Helper Functions
    doc.append("=== HELPER FUNCTIONS ===")
    doc.append("")

    # Required function (Analyst is always required)
    doc.append("REQUIRED:")
    if canvas.helpers.analyst_function:
        doc.append(f"  Analyst: {canvas.helpers.analyst_function}")
    else:
        doc.append("  Analyst: (not configured)")
    doc.append("")

    # Advanced functions (user selects 2 of 3)
    doc.append("ADVANCED FUNCTIONS (2 of 3 selected):")
    advanced_count = 0
    if canvas.helpers.moderator_function:
        doc.append(f"  [X] Moderator: {canvas.helpers.moderator_function}")
        advanced_count += 1
    else:
        doc.append("  [ ] Moderator: (not selected)")
    if canvas.helpers.self_reflection_prompts:
        doc.append(f"  [X] Self-Reflections: {canvas.helpers.self_reflection_prompts}")
        advanced_count += 1
    else:
        doc.append("  [ ] Self-Reflections: (not selected)")
    if canvas.helpers.non_anthropomorphic_cues:
        doc.append(f"  [X] Non-Anthropomorphic: {canvas.helpers.non_anthropomorphic_cues}")
        advanced_count += 1
    else:
        doc.append("  [ ] Non-Anthropomorphic: (not selected)")
    doc.append(f"  ({advanced_count}/2 advanced functions configured)")
    doc.append("")

    # Status
    doc.append("=== STATUS ===")
    doc.append(f"Phase 1 Complete: {canvas.status.phase1_complete}")
    doc.append(f"Phase 2 Complete: {canvas.status.phase2_complete}")
    doc.append(f"Phase 3 Complete: {canvas.status.phase3_complete}")
    doc.append(f"Ready for Export: {canvas.status.ready_for_export}")
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
