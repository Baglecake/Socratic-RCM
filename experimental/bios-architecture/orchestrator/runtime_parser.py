"""
Runtime Parser - Parses BIOS runtime files into Step objects

This module reads the runtime .txt files (Phase 1, 2, 3) and converts them
into a structured Step graph that the orchestrator can execute.
"""

import re
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Step:
    """Represents a single step in the BIOS workflow"""
    id: str
    target: str
    instruction: str
    required_output: str
    rcm_cue: Optional[str] = None
    constraint: Optional[str] = None
    next_step: Optional[str] = None
    canvas_update: Optional[Dict] = None

    def __repr__(self):
        return f"Step({self.id}, target='{self.target}')"


class Runtime:
    """Parses and stores all workflow steps from runtime files"""

    def __init__(self, phase1_path: str, phase2_path: str, phase3_path: str):
        self.steps: Dict[str, Step] = {}
        self._parse_runtime_file(phase1_path)
        self._parse_runtime_file(phase2_path)
        self._parse_runtime_file(phase3_path)

    def get_step(self, step_id: str) -> Step:
        """Retrieve a step by ID (e.g., '2.2.6')"""
        if step_id not in self.steps:
            raise KeyError(f"Step {step_id} not found in runtime files")
        return self.steps[step_id]

    def _parse_runtime_file(self, filepath: str):
        """Parse a single runtime file and extract all steps"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into step blocks (look for ### [STEP X.X.X])
        step_pattern = r'### \[STEP ([^\]]+)\](.*?)(?=### \[STEP |$)'
        matches = re.findall(step_pattern, content, re.DOTALL)

        for step_id, step_content in matches:
            step = self._parse_step_block(step_id.strip(), step_content.strip())
            self.steps[step.id] = step

    def _parse_step_block(self, step_id: str, content: str) -> Step:
        """Parse a single step block into a Step object"""

        # Extract fields using regex
        target = self._extract_field(content, r'TARGET:\s*(.+?)(?=\n[A-Z]+:|$)')
        instruction = self._extract_field(content, r'INSTRUCTION:\s*(.+?)(?=\n[A-Z]+:|$)')
        required_output = self._extract_field(content, r'REQUIRED OUTPUT:\s*"([^"]+)"')
        rcm_cue = self._extract_field(content, r'RCM CUE:\s*(.+?)(?=\n[A-Z]+:|$)')
        constraint = self._extract_field(content, r'CONSTRAINT:\s*(.+?)(?=\n[A-Z]+:|$)')
        next_step = self._extract_field(content, r'NEXT STEP:\s*([^\s\n]+)')

        # Extract CANVAS_UPDATE block if present
        canvas_update = self._extract_canvas_update(content)

        return Step(
            id=step_id,
            target=target or "",
            instruction=instruction or "",
            required_output=required_output or "",
            rcm_cue=rcm_cue,
            constraint=constraint,
            next_step=next_step,
            canvas_update=canvas_update
        )

    def _extract_field(self, content: str, pattern: str) -> Optional[str]:
        """Extract a field from step content using regex"""
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None

    def _extract_canvas_update(self, content: str) -> Optional[Dict]:
        """Extract CANVAS_UPDATE block if present"""
        # Look for CANVAS_UPDATE: followed by JSON-like structure
        pattern = r'CANVAS_UPDATE:\s*\{(.+?)\}(?=\n[A-Z]+:|$)'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            # Parse the canvas update block
            # For now, return a simple dict representation
            # In production, you'd parse this more carefully
            update_content = match.group(1).strip()

            # Extract section and action
            section_match = re.search(r'"section":\s*"([^"]+)"', update_content)
            action_match = re.search(r'"action":\s*"([^"]+)"', update_content)

            if section_match and action_match:
                return {
                    "section": section_match.group(1),
                    "action": action_match.group(1),
                    "raw_content": update_content
                }

        return None


if __name__ == "__main__":
    # Test the parser
    import os

    base_path = os.path.dirname(os.path.dirname(__file__))
    runtime = Runtime(
        f"{base_path}/runtime-files/B42_Runtime_Phase1_Conceptualization.txt",
        f"{base_path}/runtime-files/B42_Runtime_Phase2_Drafting.txt",
        f"{base_path}/runtime-files/B42_Runtime_Phase3_Review.txt"
    )

    print(f"Loaded {len(runtime.steps)} steps")

    # Test retrieving a specific step
    if "2.2.6" in runtime.steps:
        step = runtime.get_step("2.2.6")
        print(f"\nStep 2.2.6:")
        print(f"  Target: {step.target}")
        print(f"  Required Output: {step.required_output}")
        print(f"  Next Step: {step.next_step}")
