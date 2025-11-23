"""
LLM Client - Interface for interacting with language models

Supports OpenAI, Anthropic, and local models. The LLM's role is:
1. Ask questions in RCM-flavored way
2. Validate student answers against constraints
3. Generate clarifying questions when needed
4. NEVER control workflow state or step advancement
"""

import json
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract base class for LLM clients"""

    @abstractmethod
    def send_message(self, system_prompt: str, user_message: str) -> str:
        """Send a message and get text response"""
        pass

    @abstractmethod
    def send_json(self, system_prompt: str, user_message: str) -> Dict:
        """Send a message and get JSON response"""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client (GPT-4, etc.)"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        # Import here to make it optional
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("Please install openai: pip install openai")

    def send_message(self, system_prompt: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content

    def send_json(self, system_prompt: str, user_message: str) -> Dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)


class AnthropicClient(LLMClient):
    """Anthropic API client (Claude)"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key
        self.model = model
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("Please install anthropic: pip install anthropic")

    def send_message(self, system_prompt: str, user_message: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text

    def send_json(self, system_prompt: str, user_message: str) -> Dict:
        # Anthropic doesn't have native JSON mode yet, so we parse the response
        response_text = self.send_message(
            system_prompt,
            user_message + "\n\nRespond with valid JSON only."
        )
        # Try to extract JSON from markdown code blocks if present
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()

        return json.loads(json_str)


class MockClient(LLMClient):
    """Mock client for testing without API calls"""

    def __init__(self):
        self.call_count = 0

    def send_message(self, system_prompt: str, user_message: str) -> str:
        self.call_count += 1
        return f"Mock response #{self.call_count}"

    def send_json(self, system_prompt: str, user_message: str) -> Dict:
        self.call_count += 1
        return {"ok": True, "reason": "Mock validation passed"}


class StudentInteractionHandler:
    """
    Handles the LLM's interaction with the student.
    The LLM asks questions and validates answers, but NEVER controls workflow.
    """

    def __init__(self, llm_client: LLMClient, bios_prompt: str):
        self.llm = llm_client
        self.bios_prompt = bios_prompt

    def ask_question(
        self,
        required_output: str,
        rcm_cue: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Ask the student a question using RCM approach.

        Args:
            required_output: The exact question from the runtime file
            rcm_cue: Optional RCM cue for how to approach the question
            context: Optional context about previous answers

        Returns:
            The question to present to the student (may be slightly reworded for flow)
        """
        # In a real implementation, you might let the LLM add very brief
        # encouragement or glue, but the core question must match required_output

        prompt = f"""You will ask the student this question:

"{required_output}"

"""
        if rcm_cue:
            prompt += f"""Use this RCM approach:
{rcm_cue}

"""
        if context:
            prompt += f"""Context from previous answers:
{context}

"""

        prompt += """Present the question naturally. You may add brief encouragement,
but the core question text must be preserved exactly."""

        # For now, just return the required_output directly
        # In production, you could use the LLM for minor rewording
        return required_output

    def validate_answer(
        self,
        answer: str,
        constraint: Optional[str],
        target: str
    ) -> Dict[str, Any]:
        """
        Validate a student's answer against the constraint.

        Returns:
            {"ok": bool, "reason": str, "suggestion": str}
        """
        if not constraint:
            # No constraint = always valid
            return {"ok": True, "reason": "No constraint specified"}

        validation_prompt = f"""You are checking whether a student's answer satisfies this requirement:

TARGET: {target}

CONSTRAINT:
{constraint}

STUDENT ANSWER:
{answer}

Evaluate:
1. Does the answer meet the constraint?
2. If not, what's missing?
3. If not, what's a brief, Socratic follow-up question to help them?

Respond with JSON:
{{
  "ok": true/false,
  "reason": "brief explanation",
  "suggestion": "Socratic follow-up question (only if ok=false)"
}}
"""

        try:
            result = self.llm.send_json(self.bios_prompt, validation_prompt)
            return result
        except Exception as e:
            # Fallback: if LLM fails, accept the answer
            print(f"Warning: Validation failed ({e}), accepting answer")
            return {"ok": True, "reason": "Validation error, accepting answer"}

    def remediate_answer(
        self,
        original_answer: str,
        validation_result: Dict,
        required_output: str
    ) -> str:
        """
        Ask a follow-up question to help student improve their answer.

        Returns:
            The follow-up question to ask
        """
        suggestion = validation_result.get("suggestion", "")
        reason = validation_result.get("reason", "")

        if suggestion:
            return suggestion
        else:
            # Generate a generic follow-up
            return f"{reason} Could you provide more detail?"


def create_llm_client(
    provider: str = "mock",
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> LLMClient:
    """
    Factory function to create the appropriate LLM client.

    Args:
        provider: "openai", "anthropic", or "mock"
        api_key: API key for the provider
        model: Model name (optional, uses defaults)

    Returns:
        LLMClient instance
    """
    if provider == "openai":
        if not api_key:
            raise ValueError("API key required for OpenAI")
        return OpenAIClient(api_key, model or "gpt-4")

    elif provider == "anthropic":
        if not api_key:
            raise ValueError("API key required for Anthropic")
        return AnthropicClient(api_key, model or "claude-3-5-sonnet-20241022")

    elif provider == "mock":
        return MockClient()

    else:
        raise ValueError(f"Unknown provider: {provider}")


if __name__ == "__main__":
    # Test the mock client
    client = create_llm_client("mock")
    handler = StudentInteractionHandler(client, "Test BIOS prompt")

    # Test asking a question
    question = handler.ask_question(
        "What is your project goal?",
        rcm_cue="Help them reflect on their theoretical interests"
    )
    print(f"Question: {question}")

    # Test validation
    validation = handler.validate_answer(
        "I want to study class conflict",
        "Must be 2-3 sentences",
        "Project goal"
    )
    print(f"Validation: {validation}")
