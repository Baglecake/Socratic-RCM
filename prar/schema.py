"""
PRAR Schema Definitions

TypedDict definitions for PRAR (Process-Retrieval Augmented Reasoning) data structures.
These schemas formalize the contract between PRAR workflow outputs and downstream
consumers (Agent system, Social RL framework).
"""

from typing import TypedDict, List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


# =============================================================================
# Canvas Component Schemas
# =============================================================================

class ConceptDefinition(TypedDict):
    """Definition of a theoretical concept."""
    name: str
    definition: str
    theorist: Optional[str]
    manifestations: Optional[List[str]]


class VariableDefinition(TypedDict):
    """Experimental variable configuration."""
    name: str
    baseline: str
    experimental: str
    rationale: str


class ProjectInfo(TypedDict):
    """Project-level configuration from Phase 1."""
    goal: str
    theoretical_option: str  # "A", "B", "C", "D", or "E"
    concept_a: ConceptDefinition
    concept_b: ConceptDefinition
    variable: VariableDefinition
    setting: str
    rounds_count: int


class AgentDefinition(TypedDict):
    """Agent configuration from canvas."""
    identifier: str  # e.g., "Worker+Alice"
    goal: str
    persona: str
    prompt: str
    role: Optional[str]  # Extracted from identifier
    name: Optional[str]  # Extracted from identifier


class RoundDefinition(TypedDict):
    """Round configuration from canvas."""
    round_number: int
    scenario: str
    rules: str
    tasks: str
    compiled_instructions: Optional[str]
    platform_config: Optional[Dict[str, Any]]


class HelperFunctions(TypedDict, total=False):
    """Helper function configurations."""
    analyst_function: str
    moderator_function: str
    self_reflection: str
    non_anthropomorphic: str


class CanvasStatus(TypedDict):
    """Canvas completion status."""
    phase1_complete: bool
    phase2_complete: bool
    phase3_complete: bool
    ready_for_export: bool


# =============================================================================
# Full Canvas Schema
# =============================================================================

class Canvas(TypedDict):
    """Complete canvas data model."""
    project: ProjectInfo
    agents: List[AgentDefinition]
    rounds: List[RoundDefinition]
    helpers: HelperFunctions
    status: CanvasStatus


# =============================================================================
# PRAR State Schema
# =============================================================================

class PRARConfig(TypedDict):
    """Configuration metadata for a PRAR run."""
    model: str
    backend: str  # "vllm", "openai", "anthropic", "mock"
    base_url: Optional[str]
    phases_completed: List[int]
    theoretical_framework: str
    timestamp: str


class PRARState(TypedDict):
    """Complete PRAR workflow state."""
    student_state: Dict[str, str]  # step_id -> answer
    canvas: Canvas
    config: PRARConfig
    version: str


# =============================================================================
# Policy State Schema (PRAR <-> Social RL Contract)
# =============================================================================

class PolicyCueState(TypedDict):
    """State of a single reasoning cue."""
    cue_id: str
    active: bool
    intensity: float  # 0.0-1.0
    last_triggered: Optional[str]  # timestamp


class AgentPolicyState(TypedDict):
    """Policy state for a single agent."""
    role: str
    cues_active: List[str]
    cue_states: Dict[str, PolicyCueState]
    feedback_snapshot: Dict[str, float]


class PRARPolicyState(TypedDict):
    """
    Policy state artifact linking PRAR to Social RL.

    This is the formal contract: Social RL consumes PRAR-generated
    policy states and adapts them based on social feedback.
    """
    framework_option: str  # "A", "B", "C", "D", "E"
    framework_name: str  # Human-readable name
    policies: List[AgentPolicyState]
    timestamp: str
    source_run_id: str  # PRAR output directory name
    social_rl_version: str


# =============================================================================
# Theoretical Framework Schemas
# =============================================================================

class TheoreticalOption(TypedDict):
    """Configuration for a theoretical framework option."""
    option_id: str  # "A", "B", "C", "D", "E"
    name: str
    theorists: List[str]
    concept_a: str
    concept_b: str
    description: str


# Predefined theoretical options from B42
THEORETICAL_OPTIONS: Dict[str, TheoreticalOption] = {
    "A": {
        "option_id": "A",
        "name": "Class Conflict / Alienation",
        "theorists": ["Marx", "Wollstonecraft"],
        "concept_a": "Alienation",
        "concept_b": "Non-domination",
        "description": "Explores class dynamics through alienation and freedom from arbitrary power",
    },
    "B": {
        "option_id": "B",
        "name": "Democratic Participation",
        "theorists": ["Tocqueville", "Smith"],
        "concept_a": "Civic virtue",
        "concept_b": "Self-interest",
        "description": "Examines tension between collective participation and individual motivation",
    },
    "C": {
        "option_id": "C",
        "name": "Gender and Power",
        "theorists": ["Wollstonecraft", "Marx"],
        "concept_a": "Domination",
        "concept_b": "Exploitation",
        "description": "Analyzes intersections of gender-based and economic oppression",
    },
    "D": {
        "option_id": "D",
        "name": "Economic Rationality",
        "theorists": ["Smith", "Tocqueville"],
        "concept_a": "Market behavior",
        "concept_b": "Democratic norms",
        "description": "Explores relationship between economic and democratic decision-making",
    },
    "E": {
        "option_id": "E",
        "name": "Custom",
        "theorists": [],
        "concept_a": "User-defined",
        "concept_b": "User-defined",
        "description": "Custom theoretical framework defined by user",
    },
}


# =============================================================================
# Utility Functions
# =============================================================================

def load_prar_state(filepath: str) -> Dict[str, Any]:
    """
    Load PRAR state from a state.json file.

    Note: Returns Dict[str, Any] rather than PRARState because
    actual state files may have step IDs as top-level keys.
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def extract_canvas_from_state(state: Dict[str, Any]) -> Optional[Canvas]:
    """Extract canvas from PRAR state if present."""
    return state.get("canvas")


def get_framework_info(option_id: str) -> TheoreticalOption:
    """Get theoretical framework information by option ID."""
    if option_id not in THEORETICAL_OPTIONS:
        raise ValueError(f"Unknown framework option: {option_id}")
    return THEORETICAL_OPTIONS[option_id]


def create_policy_state(
    framework_option: str,
    policies: List[AgentPolicyState],
    source_run_id: str,
    version: str = "0.2.0"
) -> PRARPolicyState:
    """Create a policy state artifact."""
    framework = get_framework_info(framework_option)
    return {
        "framework_option": framework_option,
        "framework_name": framework["name"],
        "policies": policies,
        "timestamp": datetime.now().isoformat(),
        "source_run_id": source_run_id,
        "social_rl_version": version,
    }


def validate_canvas(canvas: Dict[str, Any]) -> bool:
    """
    Validate that a dict conforms to Canvas schema.

    Returns True if valid, raises ValueError with details if not.
    """
    required_keys = ["project", "agents", "rounds"]

    for key in required_keys:
        if key not in canvas:
            raise ValueError(f"Canvas missing required key: {key}")

    project = canvas["project"]
    project_required = ["goal", "theoretical_option"]
    for key in project_required:
        if key not in project:
            raise ValueError(f"Canvas project missing: {key}")

    if not isinstance(canvas["agents"], list):
        raise ValueError("Canvas agents must be a list")

    if not isinstance(canvas["rounds"], list):
        raise ValueError("Canvas rounds must be a list")

    return True


# =============================================================================
# Schema Version
# =============================================================================

SCHEMA_VERSION = "0.2.0"
