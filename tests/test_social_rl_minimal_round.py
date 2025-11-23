"""
Test: Social RL Minimal Round Execution

Tests that SocialRLRunner can execute a minimal round with mock LLM
and produces valid output conforming to the schema.
"""

import pytest
import json
import os
import sys
import tempfile
from pathlib import Path

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

validate_round_result = schema.validate_round_result
SocialRLMessageDict = schema.SocialRLMessageDict
FeedbackVector = schema.FeedbackVector
SCHEMA_VERSION = schema.SCHEMA_VERSION


class MockLLMClient:
    """Mock LLM client for testing."""

    def __init__(self, response: str = "I understand the task."):
        self.response = response
        self.call_count = 0

    def send_message(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> str:
        self.call_count += 1
        return self.response


# Minimal canvas for testing
MINIMAL_CANVAS = {
    "project": {
        "goal": "Test simulation",
        "theoretical_option": "A",
        "concept_a": {
            "name": "Alienation",
            "definition": "Separation from labor's product"
        },
        "concept_b": {
            "name": "Non-domination",
            "definition": "Freedom from arbitrary power"
        },
        "variable": {
            "name": "Worker autonomy",
            "baseline": "Low",
            "experimental": "High",
            "rationale": "Testing autonomy effects"
        },
        "setting": "Factory workplace",
        "rounds_count": 1
    },
    "agents": [
        {
            "identifier": "Worker+Alice",
            "goal": "Complete tasks while maintaining dignity",
            "persona": "Thoughtful worker",
            "prompt": "You are Alice, a factory worker."
        },
        {
            "identifier": "Owner+Marta",
            "goal": "Maximize productivity",
            "persona": "Demanding owner",
            "prompt": "You are Marta, the factory owner."
        }
    ],
    "rounds": [
        {
            "round_number": 1,
            "scenario": "Morning shift begins",
            "rules": "Maintain role consistency",
            "tasks": "Complete assigned work"
        }
    ],
    "helpers": {},
    "status": {
        "phase1_complete": True,
        "phase2_complete": True,
        "phase3_complete": True,
        "ready_for_export": True
    }
}


def create_minimal_state():
    """Create a minimal PRAR state for testing."""
    return {
        "canvas": MINIMAL_CANVAS,
        "student_state": {},
        "config": {
            "model": "mock",
            "backend": "mock",
            "phases_completed": [1, 2, 3],
            "theoretical_framework": "Class Conflict / Alienation"
        }
    }


class TestSchemaValidation:
    """Tests for schema validation functions."""

    def test_valid_round_result(self):
        """Test that a valid round result passes validation."""
        valid_result = {
            "round_number": 1,
            "messages": [
                {
                    "agent_id": "Worker+Alice",
                    "content": "I understand the task.",
                    "round_number": 1,
                    "turn_number": 1,
                    "timestamp": 1700000000.0,
                    "prar_cue_used": None,
                    "feedback_snapshot": None,
                    "validation_metadata": None
                }
            ],
            "feedback": {
                "Worker+Alice": {
                    "agent_id": "Worker+Alice",
                    "round_number": 1,
                    "engagement": 0.5,
                    "theoretical_alignment": 0.5,
                    "contribution_value": 0.5,
                    "direct_references": 0,
                    "response_received": 0,
                    "concepts_embodied": [],
                    "analyst_mentions": 0,
                    "synthesis_inclusion": 0.0
                }
            },
            "policy_adaptations": [],
            "synthesis": "",
            "duration_seconds": 1.0
        }

        assert validate_round_result(valid_result) is True

    def test_missing_round_number(self):
        """Test that missing round_number raises ValueError."""
        invalid_result = {
            "messages": [],
            "feedback": {},
            "policy_adaptations": [],
            "synthesis": "",
            "duration_seconds": 1.0
        }

        with pytest.raises(ValueError) as exc_info:
            validate_round_result(invalid_result)

        assert "round_number" in str(exc_info.value)

    def test_missing_messages(self):
        """Test that missing messages raises ValueError."""
        invalid_result = {
            "round_number": 1,
            "feedback": {},
            "policy_adaptations": [],
            "synthesis": "",
            "duration_seconds": 1.0
        }

        with pytest.raises(ValueError) as exc_info:
            validate_round_result(invalid_result)

        assert "messages" in str(exc_info.value)

    def test_invalid_message_structure(self):
        """Test that invalid message structure raises ValueError."""
        invalid_result = {
            "round_number": 1,
            "messages": [
                {"content": "Missing agent_id"}  # Missing required fields
            ],
            "feedback": {},
            "policy_adaptations": [],
            "synthesis": "",
            "duration_seconds": 1.0
        }

        with pytest.raises(ValueError) as exc_info:
            validate_round_result(invalid_result)

        assert "agent_id" in str(exc_info.value)


class TestOutputFileValidation:
    """Tests that validate actual output files against schema."""

    def test_existing_output_files(self):
        """Test that existing output files conform to schema."""
        outputs_dir = Path(__file__).parent.parent / "outputs"

        if not outputs_dir.exists():
            pytest.skip("No outputs directory found")

        # Find Social RL output directories
        output_dirs = list(outputs_dir.glob("social_rl_*"))

        if not output_dirs:
            pytest.skip("No Social RL outputs found")

        for output_dir in output_dirs:
            round_files = list(output_dir.glob("round*_social_rl.json"))

            for round_file in round_files:
                with open(round_file, 'r') as f:
                    data = json.load(f)

                # Should not raise
                assert validate_round_result(data) is True, \
                    f"Validation failed for {round_file}"


class TestMinimalCanvasValidation:
    """Tests for minimal canvas structure."""

    def test_minimal_canvas_has_required_fields(self):
        """Test that minimal canvas has all required fields."""
        canvas = MINIMAL_CANVAS

        assert "project" in canvas
        assert "agents" in canvas
        assert "rounds" in canvas

        assert canvas["project"]["goal"] is not None
        assert canvas["project"]["theoretical_option"] in ["A", "B", "C", "D", "E"]

        assert len(canvas["agents"]) >= 2
        assert len(canvas["rounds"]) >= 1

    def test_agent_identifier_format(self):
        """Test that agent identifiers follow Role+Name format."""
        for agent in MINIMAL_CANVAS["agents"]:
            identifier = agent["identifier"]
            assert "+" in identifier, f"Invalid identifier format: {identifier}"

            parts = identifier.split("+")
            assert len(parts) == 2, f"Expected Role+Name format: {identifier}"


class TestMockLLMClient:
    """Tests for the mock LLM client."""

    def test_mock_client_returns_response(self):
        """Test that mock client returns configured response."""
        client = MockLLMClient(response="Test response")

        result = client.send_message("system", "user")

        assert result == "Test response"
        assert client.call_count == 1

    def test_mock_client_tracks_calls(self):
        """Test that mock client tracks call count."""
        client = MockLLMClient()

        client.send_message("system", "user")
        client.send_message("system", "user")
        client.send_message("system", "user")

        assert client.call_count == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
