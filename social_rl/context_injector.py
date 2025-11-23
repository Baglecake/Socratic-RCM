"""
ContextInjector - Dynamic round/turn context generation for Social RL.

This module implements Round-Context Injection: instead of static prompts,
each turn dynamically generates concept manifestations based on:
- Current round configuration
- Recent conversation history
- Accumulated social feedback
- Theoretical framework constraints

This is the core of the "Process Retrieval as Policy" paradigm.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import json


class ManifestationType(Enum):
    """Types of manifestation generation strategies."""
    STATIC = "static"           # Use canvas manifestations as-is
    PROGRESSIVE = "progressive" # Intensify based on turn number
    REACTIVE = "reactive"       # Adapt based on conversation history
    ADAPTIVE = "adaptive"       # Full social feedback integration


@dataclass
class TurnContext:
    """Complete context for a single turn."""
    agent_id: str
    round_number: int
    turn_number: int

    # Static context from canvas
    base_scenario: str
    base_rules: str
    base_tasks: str

    # Dynamic manifestations (the key innovation)
    concept_a_manifestation: str
    concept_b_manifestation: str
    experiential_context: str  # How the agent is "experiencing" this

    # Social context
    recent_exchanges: List[Dict[str, str]]
    social_feedback_summary: str

    # Process retrieval cue
    prar_cue: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "round_number": self.round_number,
            "turn_number": self.turn_number,
            "base_scenario": self.base_scenario,
            "concept_a_manifestation": self.concept_a_manifestation,
            "concept_b_manifestation": self.concept_b_manifestation,
            "experiential_context": self.experiential_context,
            "social_feedback_summary": self.social_feedback_summary,
            "prar_cue": self.prar_cue
        }


@dataclass
class TheoreticalFramework:
    """Theoretical framework configuration for manifestation generation."""
    option: str  # A, B, C, D, E
    label: str   # "Class Conflict / Alienation", etc.
    concept_a_name: str
    concept_a_definition: str
    concept_b_name: str
    concept_b_definition: str

    # Manifestation templates per intensity level
    intensity_templates: Dict[str, Dict[str, str]] = field(default_factory=dict)

    @classmethod
    def from_canvas_project(cls, project: Dict[str, Any]) -> "TheoreticalFramework":
        """Create from canvas project info."""
        concept_a = project.get("concept_a", {})
        concept_b = project.get("concept_b", {})

        return cls(
            option=project.get("theoretical_option", "A"),
            label=project.get("theoretical_option_label", ""),
            concept_a_name=concept_a.get("name", "Concept A"),
            concept_a_definition=concept_a.get("definition", ""),
            concept_b_name=concept_b.get("name", "Concept B"),
            concept_b_definition=concept_b.get("definition", ""),
            intensity_templates=cls._get_default_templates(project.get("theoretical_option", "A"))
        )

    @staticmethod
    def _get_default_templates(option: str) -> Dict[str, Dict[str, str]]:
        """Get default intensity templates for each framework option."""
        templates = {
            "A": {  # Class Conflict / Alienation
                "low": {
                    "concept_a": "You feel a mild sense of disconnection from your work, performing tasks without full understanding.",
                    "concept_b": "You notice decisions are made without your input, but accept this as normal."
                },
                "medium": {
                    "concept_a": "The separation between your labor and its meaning becomes clearer. You work, but for whose benefit?",
                    "concept_b": "Power feels arbitrary - rules change without explanation, affecting you directly."
                },
                "high": {
                    "concept_a": "Complete alienation - you are a mere instrument, your humanity reduced to labor capacity.",
                    "concept_b": "Domination is total. Your compliance isn't choice but survival under arbitrary authority."
                }
            },
            "B": {  # Democratic Participation (Tocqueville/Smith)
                "low": {
                    "concept_a": "You feel some responsibility toward the collective good.",
                    "concept_b": "Personal benefit matters, but you consider others."
                },
                "medium": {
                    "concept_a": "Civic participation feels meaningful - your voice might matter.",
                    "concept_b": "Self-interest competes with community obligations."
                },
                "high": {
                    "concept_a": "Deep civic virtue - you prioritize collective welfare over personal gain.",
                    "concept_b": "Rational self-interest dominates - community is instrumental."
                }
            }
        }
        return templates.get(option, templates["A"])


class ContextInjector:
    """
    Generates dynamic turn-specific context for agents.

    The key innovation: instead of static prompts, each turn receives
    context that reflects:
    1. Progressive intensification through the round
    2. Reactions to recent social exchanges
    3. Accumulated social feedback signals
    4. Theoretical framework constraints

    This creates emergent, socially-grounded behavior without
    explicit reward signals - social interaction IS the learning.
    """

    def __init__(
        self,
        framework: TheoreticalFramework,
        llm_client: Optional[Any] = None,
        mode: ManifestationType = ManifestationType.PROGRESSIVE
    ):
        """
        Initialize the context injector.

        Args:
            framework: Theoretical framework configuration
            llm_client: Optional LLM for adaptive manifestation generation
            mode: Manifestation generation strategy
        """
        self.framework = framework
        self.llm = llm_client
        self.mode = mode

        # Accumulated social feedback per agent
        self.agent_feedback: Dict[str, List[Dict[str, Any]]] = {}

        # PRAR cue templates
        self.prar_templates = self._load_prar_templates()

    def _load_prar_templates(self) -> Dict[str, str]:
        """Load PRAR process retrieval cue templates."""
        return {
            "reflect": "Consider how your current situation relates to {concept_a} and {concept_b}.",
            "connect": "Your experience connects to broader patterns of {framework_label}.",
            "ask": "What would authentic engagement look like given your constraints?"
        }

    def generate_turn_context(
        self,
        agent_id: str,
        agent_config: Dict[str, Any],
        round_config: Dict[str, Any],
        turn_number: int,
        conversation_history: List[Dict[str, str]],
        accumulated_feedback: Optional[Dict[str, Any]] = None
    ) -> TurnContext:
        """
        Generate complete context for a single turn.

        Args:
            agent_id: Agent identifier
            agent_config: Agent configuration dict
            round_config: Round configuration dict
            turn_number: Current turn number
            conversation_history: Messages so far
            accumulated_feedback: Social feedback from previous rounds

        Returns:
            TurnContext with all dynamic components
        """
        # Calculate intensity based on turn progression
        max_turns = self._parse_max_turns(round_config.get("end_condition", "15"))
        intensity = self._calculate_intensity(turn_number, max_turns)

        # Generate manifestations based on mode
        if self.mode == ManifestationType.STATIC:
            concept_a_manif = round_config.get("concept_a_manifestation", "")
            concept_b_manif = round_config.get("concept_b_manifestation", "")
        elif self.mode == ManifestationType.PROGRESSIVE:
            concept_a_manif, concept_b_manif = self._generate_progressive_manifestations(
                round_config, intensity
            )
        elif self.mode == ManifestationType.REACTIVE:
            concept_a_manif, concept_b_manif = self._generate_reactive_manifestations(
                round_config, conversation_history, intensity
            )
        else:  # ADAPTIVE
            concept_a_manif, concept_b_manif = self._generate_adaptive_manifestations(
                agent_id, round_config, conversation_history,
                accumulated_feedback, intensity
            )

        # Generate experiential context (how this agent experiences the situation)
        experiential = self._generate_experiential_context(
            agent_config, round_config, conversation_history, intensity
        )

        # Generate social feedback summary
        social_summary = self._summarize_social_context(
            agent_id, conversation_history, accumulated_feedback
        )

        # Generate PRAR cue
        prar_cue = self._generate_prar_cue(intensity)

        return TurnContext(
            agent_id=agent_id,
            round_number=round_config.get("round_number", 1),
            turn_number=turn_number,
            base_scenario=round_config.get("scenario", ""),
            base_rules=round_config.get("rules", ""),
            base_tasks=round_config.get("tasks", ""),
            concept_a_manifestation=concept_a_manif,
            concept_b_manifestation=concept_b_manif,
            experiential_context=experiential,
            recent_exchanges=conversation_history[-3:] if conversation_history else [],
            social_feedback_summary=social_summary,
            prar_cue=prar_cue
        )

    def _calculate_intensity(self, turn_number: int, max_turns: int) -> str:
        """Calculate intensity level based on round progression."""
        progress = turn_number / max(max_turns, 1)
        if progress < 0.33:
            return "low"
        elif progress < 0.66:
            return "medium"
        else:
            return "high"

    def _parse_max_turns(self, end_condition: str) -> int:
        """Parse max turns from end condition string."""
        end_lower = end_condition.lower()
        if "total messages:" in end_lower:
            try:
                return int(end_lower.split(":")[-1].strip())
            except ValueError:
                pass
        return 15  # default

    def _generate_progressive_manifestations(
        self,
        round_config: Dict[str, Any],
        intensity: str
    ) -> tuple:
        """Generate manifestations that intensify through the round."""
        templates = self.framework.intensity_templates.get(intensity, {})

        # Start with canvas manifestation, enhance with intensity
        base_a = round_config.get("concept_a_manifestation", "")
        base_b = round_config.get("concept_b_manifestation", "")

        template_a = templates.get("concept_a", "")
        template_b = templates.get("concept_b", "")

        # Combine base with intensity template
        if intensity == "low":
            return base_a, base_b
        elif intensity == "medium":
            enhanced_a = f"{base_a}\n\nYou're experiencing this as: {template_a}"
            enhanced_b = f"{base_b}\n\nThis feels like: {template_b}"
            return enhanced_a, enhanced_b
        else:  # high
            enhanced_a = f"{base_a}\n\n{template_a}"
            enhanced_b = f"{base_b}\n\n{template_b}"
            return enhanced_a, enhanced_b

    def _generate_reactive_manifestations(
        self,
        round_config: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        intensity: str
    ) -> tuple:
        """Generate manifestations that react to conversation dynamics."""
        base_a, base_b = self._generate_progressive_manifestations(round_config, intensity)

        if not conversation_history:
            return base_a, base_b

        # Analyze recent exchanges for reactive elements
        recent = conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history

        # Detect interaction patterns
        patterns = self._detect_interaction_patterns(recent)

        # Add reactive context
        reactive_context = self._generate_reactive_context(patterns)

        enhanced_a = f"{base_a}\n\nGiven what just happened: {reactive_context}"
        enhanced_b = base_b

        return enhanced_a, enhanced_b

    def _generate_adaptive_manifestations(
        self,
        agent_id: str,
        round_config: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        accumulated_feedback: Optional[Dict[str, Any]],
        intensity: str
    ) -> tuple:
        """
        Full adaptive generation using social feedback.

        This is where the "RL through social interaction" happens:
        accumulated feedback shapes how concepts manifest for this agent.
        """
        base_a, base_b = self._generate_reactive_manifestations(
            round_config, conversation_history, intensity
        )

        if not accumulated_feedback:
            return base_a, base_b

        # Extract feedback signals for this agent
        agent_signals = accumulated_feedback.get(agent_id, {})

        # Engagement signal: how much others respond to this agent
        engagement = agent_signals.get("engagement", 0.5)

        # Alignment signal: how well agent aligns with theoretical framework
        alignment = agent_signals.get("theoretical_alignment", 0.5)

        # Contribution signal: quality of contributions
        contribution = agent_signals.get("contribution_value", 0.5)

        # Adapt manifestations based on feedback
        if engagement < 0.3:
            # Low engagement - prompt more assertive behavior
            adaptive_a = f"{base_a}\n\nYour contributions haven't been acknowledged. How does this affect your sense of {self.framework.concept_a_name.lower()}?"
        elif engagement > 0.7:
            # High engagement - reinforce current approach
            adaptive_a = f"{base_a}\n\nOthers are responding to you. This engagement shapes your experience."
        else:
            adaptive_a = base_a

        if alignment < 0.3:
            # Low theoretical alignment - reinforce framework
            adaptive_b = f"{base_b}\n\nRemember: your situation embodies {self.framework.concept_b_name}."
        else:
            adaptive_b = base_b

        return adaptive_a, adaptive_b

    def _generate_experiential_context(
        self,
        agent_config: Dict[str, Any],
        round_config: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        intensity: str
    ) -> str:
        """Generate how the agent subjectively experiences the current situation."""
        role = agent_config.get("role", "Participant")
        persona = agent_config.get("persona", "")

        # Base experiential template
        templates = {
            "Worker": {
                "low": "The work continues. You do what's asked.",
                "medium": "Each task weighs heavier. The routine reveals its constraints.",
                "high": "Your labor is extracted, your voice suppressed. This is your reality."
            },
            "Owner": {
                "low": "Operations proceed smoothly. Your decisions shape the workflow.",
                "medium": "Control requires constant assertion. Compliance must be maintained.",
                "high": "Your authority is absolute here. Every interaction reinforces the hierarchy."
            },
            "Analyst": {
                "low": "You observe the interactions, noting patterns.",
                "medium": "Theoretical concepts become visible in the exchanges.",
                "high": "The data reveals the full dynamic. Document what you see."
            }
        }

        role_templates = templates.get(role, templates["Worker"])
        base_experiential = role_templates.get(intensity, role_templates["medium"])

        # Enhance with persona
        if persona:
            return f"{base_experiential}\n\nAs {persona.split('.')[0]}."

        return base_experiential

    def _summarize_social_context(
        self,
        agent_id: str,
        conversation_history: List[Dict[str, str]],
        accumulated_feedback: Optional[Dict[str, Any]]
    ) -> str:
        """Summarize relevant social context for this agent."""
        if not conversation_history:
            return "The conversation begins."

        # Count references to this agent
        references = sum(
            1 for msg in conversation_history
            if agent_id.split("+")[-1].lower() in msg.get("content", "").lower()
        )

        # Recent speaker pattern
        recent_speakers = [msg.get("agent_id", "") for msg in conversation_history[-3:]]

        summary_parts = []
        if references > 0:
            summary_parts.append(f"You've been referenced {references} times.")

        if accumulated_feedback and agent_id in accumulated_feedback:
            feedback = accumulated_feedback[agent_id]
            if feedback.get("engagement", 0.5) > 0.7:
                summary_parts.append("Others are engaging with your contributions.")
            elif feedback.get("engagement", 0.5) < 0.3:
                summary_parts.append("Your voice hasn't been acknowledged much.")

        return " ".join(summary_parts) if summary_parts else "The conversation continues."

    def _detect_interaction_patterns(self, recent: List[Dict[str, str]]) -> Dict[str, Any]:
        """Detect patterns in recent interactions."""
        patterns = {
            "conflict": False,
            "compliance": False,
            "question_asked": False,
            "directive_given": False
        }

        for msg in recent:
            content = msg.get("content", "").lower()
            if "?" in content:
                patterns["question_asked"] = True
            if any(word in content for word in ["must", "will", "should", "need to"]):
                patterns["directive_given"] = True
            if any(word in content for word in ["yes", "understand", "okay", "i'll"]):
                patterns["compliance"] = True
            if any(word in content for word in ["but", "however", "disagree", "refuse"]):
                patterns["conflict"] = True

        return patterns

    def _generate_reactive_context(self, patterns: Dict[str, Any]) -> str:
        """Generate context based on detected patterns."""
        if patterns["conflict"]:
            return "Tension has emerged. How do you respond to resistance?"
        elif patterns["directive_given"] and patterns["compliance"]:
            return "Orders given, compliance follows. The hierarchy operates."
        elif patterns["question_asked"]:
            return "Questions have been raised. Do they get answered?"
        else:
            return "The interaction proceeds."

    def _generate_prar_cue(self, intensity: str) -> str:
        """Generate PRAR process retrieval cue based on intensity."""
        cue_parts = []

        # RCM: Reflect-Connect-Ask
        reflect = self.prar_templates["reflect"].format(
            concept_a=self.framework.concept_a_name,
            concept_b=self.framework.concept_b_name
        )

        connect = self.prar_templates["connect"].format(
            framework_label=self.framework.label
        )

        ask = self.prar_templates["ask"]

        if intensity == "low":
            return f"[REFLECT]: {reflect}"
        elif intensity == "medium":
            return f"[REFLECT]: {reflect}\n[CONNECT]: {connect}"
        else:
            return f"[REFLECT]: {reflect}\n[CONNECT]: {connect}\n[ASK]: {ask}"

    def compile_dynamic_prompt(
        self,
        agent_config: Dict[str, Any],
        turn_context: TurnContext
    ) -> str:
        """
        Compile the complete dynamic prompt for an agent turn.

        This replaces the static AgentConfig.compile_system_prompt().
        """
        parts = []

        # Base agent identity
        parts.append(f"ROLE: You are {agent_config.get('identifier', 'Unknown')}")
        parts.append(f"PRIMARY GOAL: {agent_config.get('goal', '')}")
        parts.append(f"PERSONA: {agent_config.get('persona', '')}")
        parts.append("")

        # Current round context
        parts.append("=== CURRENT SITUATION ===")
        parts.append(f"SCENARIO: {turn_context.base_scenario}")
        parts.append(f"RULES: {turn_context.base_rules}")
        parts.append(f"TASKS: {turn_context.base_tasks}")
        parts.append("")

        # Dynamic theoretical context (the key innovation)
        parts.append("=== HOW YOU'RE EXPERIENCING THIS ===")
        parts.append(turn_context.experiential_context)
        parts.append("")
        parts.append(f"[{self.framework.concept_a_name}]: {turn_context.concept_a_manifestation}")
        parts.append(f"[{self.framework.concept_b_name}]: {turn_context.concept_b_manifestation}")
        parts.append("")

        # Social context
        if turn_context.social_feedback_summary:
            parts.append("=== SOCIAL CONTEXT ===")
            parts.append(turn_context.social_feedback_summary)
            parts.append("")

        # PRAR cue (process retrieval)
        if turn_context.prar_cue:
            parts.append("=== PROCESS CUE ===")
            parts.append(turn_context.prar_cue)
            parts.append("")

        # Behavioral constraints from agent config
        behaviors = agent_config.get("behaviors", {}).get("raw", "")
        if behaviors:
            parts.append(f"BEHAVIORAL RULES: {behaviors}")

        return "\n".join(parts)

    def update_feedback(self, agent_id: str, feedback: Dict[str, Any]):
        """Update accumulated feedback for an agent."""
        if agent_id not in self.agent_feedback:
            self.agent_feedback[agent_id] = []
        self.agent_feedback[agent_id].append(feedback)

    def get_accumulated_feedback(self) -> Dict[str, Dict[str, float]]:
        """Get summarized accumulated feedback for all agents."""
        summary = {}
        for agent_id, feedback_list in self.agent_feedback.items():
            if feedback_list:
                # Average the feedback signals
                summary[agent_id] = {
                    "engagement": sum(f.get("engagement", 0.5) for f in feedback_list) / len(feedback_list),
                    "theoretical_alignment": sum(f.get("theoretical_alignment", 0.5) for f in feedback_list) / len(feedback_list),
                    "contribution_value": sum(f.get("contribution_value", 0.5) for f in feedback_list) / len(feedback_list)
                }
        return summary


# Convenience function for testing
def create_context_injector_from_canvas(canvas: Dict[str, Any], mode: str = "progressive") -> ContextInjector:
    """Create a ContextInjector from canvas data."""
    project = canvas.get("project", {})
    framework = TheoreticalFramework.from_canvas_project(project)

    mode_map = {
        "static": ManifestationType.STATIC,
        "progressive": ManifestationType.PROGRESSIVE,
        "reactive": ManifestationType.REACTIVE,
        "adaptive": ManifestationType.ADAPTIVE
    }

    return ContextInjector(framework, mode=mode_map.get(mode, ManifestationType.PROGRESSIVE))


if __name__ == "__main__":
    # Test the context injector
    print("=== ContextInjector Test ===")

    # Create test framework
    framework = TheoreticalFramework(
        option="A",
        label="Class Conflict / Alienation",
        concept_a_name="Alienation",
        concept_a_definition="Workers become separated from the products of their labor",
        concept_b_name="Non-domination",
        concept_b_definition="Freedom from arbitrary power"
    )

    injector = ContextInjector(framework, mode=ManifestationType.PROGRESSIVE)

    # Test turn context generation
    test_agent = {"identifier": "Worker+Alice", "goal": "Gain influence", "persona": "Thoughtful but hesitant", "role": "Worker"}
    test_round = {
        "round_number": 1,
        "scenario": "Manufacturing workshop baseline",
        "rules": "Workers can complete tasks, request clarification",
        "tasks": "Complete three production cycles",
        "concept_a_manifestation": "Alienation manifests as separation from decision-making",
        "concept_b_manifestation": "Non-domination is absent",
        "end_condition": "Total messages: 15"
    }

    # Generate contexts at different turns
    for turn in [1, 5, 12]:
        context = injector.generate_turn_context(
            "Worker+Alice", test_agent, test_round, turn, []
        )
        print(f"\n--- Turn {turn} (intensity: {injector._calculate_intensity(turn, 15)}) ---")
        print(f"Experiential: {context.experiential_context}")
        print(f"Concept A: {context.concept_a_manifestation[:100]}...")
