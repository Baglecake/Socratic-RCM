#!/usr/bin/env python3
"""
Run Social RL locally - saves directly to your local filesystem.
Uses Ollama (local) or OpenAI API.
"""

import sys
import os
import json
import requests
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "social_rl"))
sys.path.insert(0, str(Path(__file__).parent / "agents"))
sys.path.insert(0, str(Path(__file__).parent / "local_rcm"))

from runner import SocialRLRunner, SocialRLConfig


class OllamaClient:
    """LLM client using local Ollama."""

    def __init__(self, model="llama3.2", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.call_count = 0

    def send_message(self, system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
        self.call_count += 1
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "stream": False,
                "options": {"temperature": temperature}
            }
        )
        response.raise_for_status()
        return response.json()["message"]["content"]


class OpenAIClient:
    """LLM client using OpenAI API."""

    def __init__(self, model="gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model
        self.call_count = 0

    def send_message(self, system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
        self.call_count += 1
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=512
        )
        return response.choices[0].message.content


def get_llm():
    """Get best available LLM client."""
    # Try Ollama first (local, free)
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        if r.status_code == 200:
            models = [m["name"] for m in r.json().get("models", [])]
            if models:
                # Prefer larger models
                for preferred in ["qwen2.5:7b", "llama3.2", "mistral", "llama3"]:
                    for m in models:
                        if preferred in m:
                            print(f"Using Ollama: {m}")
                            return OllamaClient(model=m.split(":")[0])
                # Use first available
                print(f"Using Ollama: {models[0]}")
                return OllamaClient(model=models[0].split(":")[0])
    except:
        pass

    # Try OpenAI
    if os.environ.get("OPENAI_API_KEY"):
        print("Using OpenAI API")
        return OpenAIClient()

    # Check .env
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip()
                    print("Using OpenAI API (from .env)")
                    return OpenAIClient()

    return None


def main():
    print("Loading canvas...")
    state_path = Path(__file__).parent / "prar/outputs/2025-11-23_baseline_full_qwen/state.json"
    with open(state_path) as f:
        canvas = json.load(f)["canvas"]

    print(f"Framework: {canvas['project'].get('theoretical_option_label')}")
    print(f"Agents: {[a['identifier'] for a in canvas['agents']]}")

    print("\nFinding LLM...")
    llm = get_llm()

    if not llm:
        print("\nERROR: No LLM available!")
        print("Options:")
        print("  1. Start Ollama: ollama serve")
        print("     Pull a model: ollama pull llama3.2")
        print("  2. Set OPENAI_API_KEY: export OPENAI_API_KEY=sk-...")
        sys.exit(1)

    # Test connection
    test = llm.send_message("You are helpful.", "Say 'ready'")
    print(f"✓ Connected: {test}")

    # Create runner
    config = SocialRLConfig(
        manifestation_mode="progressive",
        use_prar_cues=True,
        prar_intensity="medium",
        use_coach_validation=False,
        auto_save=True,
        verbose=True
    )

    runner = SocialRLRunner(canvas, llm, config)

    # Execute rounds
    print("\n" + "="*60)
    print("EXECUTING SOCIAL RL SIMULATION")
    print("="*60)

    result1 = runner.execute_round(round_number=1, max_turns=9)
    result2 = runner.execute_round(round_number=2, max_turns=9)

    # Print report
    print("\n" + runner.generate_report())

    # Show saved files
    print("\n" + "="*60)
    print("SAVED FILES")
    print("="*60)
    print(f"Output directory: {runner.output_dir}")
    for f in os.listdir(runner.output_dir):
        fpath = os.path.join(runner.output_dir, f)
        print(f"  {f}: {os.path.getsize(fpath)} bytes")


if __name__ == "__main__":
    main()
