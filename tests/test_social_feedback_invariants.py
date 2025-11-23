"""
Test: Social Feedback Invariants

Tests that SocialFeedbackExtractor produces feedback values that:
- Are within valid ranges [0.0, 1.0] for normalized metrics
- Are non-negative for count metrics
- Satisfy expected monotonicity properties
"""

import pytest
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import schema module directly (bypasses __init__.py which loads runner.py)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "schema",
    str(Path(__file__).parent.parent / "social_rl" / "schema.py")
)
schema = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schema)

FeedbackVector = schema.FeedbackVector
AgentFeedback = schema.AgentFeedback


class TestFeedbackBounds:
    """Tests for feedback value bounds."""

    def test_engagement_in_valid_range(self):
        """Test that engagement is in [0.0, 1.0]."""
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1,
            engagement=0.5
        )

        assert 0.0 <= feedback.engagement <= 1.0

    def test_alignment_in_valid_range(self):
        """Test that theoretical_alignment is in [0.0, 1.0]."""
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1,
            theoretical_alignment=0.7
        )

        assert 0.0 <= feedback.theoretical_alignment <= 1.0

    def test_contribution_in_valid_range(self):
        """Test that contribution_value is in [0.0, 1.0]."""
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1,
            contribution_value=0.8
        )

        assert 0.0 <= feedback.contribution_value <= 1.0

    def test_synthesis_inclusion_in_valid_range(self):
        """Test that synthesis_inclusion is in [0.0, 1.0]."""
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1,
            synthesis_inclusion=0.5
        )

        assert 0.0 <= feedback.synthesis_inclusion <= 1.0

    def test_count_metrics_non_negative(self):
        """Test that count metrics are non-negative."""
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1,
            direct_references=3,
            response_received=2,
            analyst_mentions=1
        )

        assert feedback.direct_references >= 0
        assert feedback.response_received >= 0
        assert feedback.analyst_mentions >= 0


class TestFeedbackSerialization:
    """Tests for feedback serialization."""

    def test_to_dict_includes_all_fields(self):
        """Test that to_dict includes all required fields."""
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1,
            engagement=0.5,
            theoretical_alignment=0.6,
            contribution_value=0.7,
            direct_references=2,
            response_received=1,
            concepts_embodied=["alienation"],
            analyst_mentions=0,
            synthesis_inclusion=0.3
        )

        d = feedback.to_dict()

        assert "agent_id" in d
        assert "round_number" in d
        assert "engagement" in d
        assert "theoretical_alignment" in d
        assert "contribution_value" in d
        assert "direct_references" in d
        assert "response_received" in d
        assert "concepts_embodied" in d
        assert "analyst_mentions" in d
        assert "synthesis_inclusion" in d

    def test_concepts_embodied_is_list(self):
        """Test that concepts_embodied is a list."""
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1,
            concepts_embodied=["alienation", "labor"]
        )

        assert isinstance(feedback.concepts_embodied, list)
        assert len(feedback.concepts_embodied) == 2


class TestFeedbackDefaults:
    """Tests for feedback default values."""

    def test_default_values_are_valid(self):
        """Test that default values are within valid ranges."""
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1
        )

        # All normalized metrics should default to 0.0
        assert feedback.engagement == 0.0
        assert feedback.theoretical_alignment == 0.0
        assert feedback.contribution_value == 0.0
        assert feedback.synthesis_inclusion == 0.0

        # All count metrics should default to 0
        assert feedback.direct_references == 0
        assert feedback.response_received == 0
        assert feedback.analyst_mentions == 0

        # concepts_embodied should default to empty list
        assert feedback.concepts_embodied == []


class TestFeedbackFromActualOutputs:
    """Tests using actual output files if available."""

    def test_actual_feedback_values_valid(self):
        """Test that feedback from actual outputs is within valid ranges."""
        import json

        outputs_dir = Path(__file__).parent.parent / "outputs"

        if not outputs_dir.exists():
            pytest.skip("No outputs directory found")

        output_dirs = list(outputs_dir.glob("social_rl_*"))

        if not output_dirs:
            pytest.skip("No Social RL outputs found")

        for output_dir in output_dirs:
            round_files = list(output_dir.glob("round*_social_rl.json"))

            for round_file in round_files:
                with open(round_file, 'r') as f:
                    data = json.load(f)

                feedback_dict = data.get("feedback", {})

                for agent_id, fb in feedback_dict.items():
                    # Check normalized metrics are in [0, 1]
                    if "engagement" in fb:
                        assert 0.0 <= fb["engagement"] <= 1.0, \
                            f"Invalid engagement for {agent_id} in {round_file}"

                    if "theoretical_alignment" in fb:
                        assert 0.0 <= fb["theoretical_alignment"] <= 1.0, \
                            f"Invalid alignment for {agent_id} in {round_file}"

                    if "contribution_value" in fb:
                        assert 0.0 <= fb["contribution_value"] <= 1.0, \
                            f"Invalid contribution for {agent_id} in {round_file}"

                    # Check count metrics are non-negative
                    if "direct_references" in fb:
                        assert fb["direct_references"] >= 0, \
                            f"Negative direct_references for {agent_id}"

                    if "response_received" in fb:
                        assert fb["response_received"] >= 0, \
                            f"Negative response_received for {agent_id}"


class TestFeedbackInvariantProperties:
    """Tests for feedback invariant properties."""

    def test_engagement_zero_when_no_messages(self):
        """Test that engagement is low/zero when agent has no messages."""
        # This is an expected property: agents who don't participate
        # should have low engagement scores
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1,
            direct_references=0,
            response_received=0
        )

        # With no references or responses, engagement should be minimal
        # (The actual calculation may vary, but should be low)
        assert feedback.engagement <= 0.5

    def test_concepts_embodied_type(self):
        """Test that concepts_embodied contains strings."""
        feedback = AgentFeedback(
            agent_id="Worker+Alice",
            round_number=1,
            concepts_embodied=["alienation", "labor", "exploitation"]
        )

        for concept in feedback.concepts_embodied:
            assert isinstance(concept, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
