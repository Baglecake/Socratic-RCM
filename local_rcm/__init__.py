"""
Socratic-RCM Local Orchestrator

A local implementation of the Socratic Research Co-pilot Machine workflow
for designing agent-based simulations grounded in theoretical frameworks.
"""

from .orchestrator import WorkflowOrchestrator
from .canvas_state import (
    CanvasState,
    compile_canvas_from_student_state,
    compile_final_document
)
from .runtime_parser import Runtime
from .llm_client import create_llm_client, StudentInteractionHandler, StudentSimulator, FRAMEWORK_THEORISTS

__version__ = "0.1.0"
__all__ = [
    "WorkflowOrchestrator",
    "CanvasState",
    "compile_canvas_from_student_state",
    "compile_final_document",
    "Runtime",
    "create_llm_client",
    "StudentInteractionHandler",
    "StudentSimulator",
    "FRAMEWORK_THEORISTS",
]
