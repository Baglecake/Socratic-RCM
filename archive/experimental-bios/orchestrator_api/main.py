"""
BIOS Orchestrator API - FastAPI server for Custom GPT integration

Exposes the orchestrator via REST API so students can interact through Custom GPT.
The GPT calls /next_step, and the orchestrator enforces workflow execution.

Run with:
    uvicorn main:app --reload --port 8000

Then expose via ngrok:
    ngrok http 8000
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# Add orchestrator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'orchestrator'))

from session_manager import SessionManager
from runtime_parser import Runtime


# ============================================================================
# Request/Response Models
# ============================================================================

class NextStepRequest(BaseModel):
    """Request from Custom GPT to get next step"""
    session_id: str = Field(..., description="Unique session ID for this student")
    current_step_id: Optional[str] = Field(None, description="Current step ID (null if starting)")
    student_message: str = Field(..., description="Student's response to previous question")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "user-123-conv-456",
                "current_step_id": "1.1.1",
                "student_message": "I want to explore class conflict in a workplace setting"
            }
        }


class NextStepResponse(BaseModel):
    """Response to Custom GPT with next question"""
    next_step_id: str = Field(..., description="Next step ID")
    message_for_student: str = Field(..., description="Question/message to show student")
    done: bool = Field(default=False, description="True if workflow is complete")
    canvas_update: Optional[Dict[str, Any]] = Field(None, description="Canvas update data (for debugging)")
    debug_info: Optional[Dict[str, Any]] = Field(None, description="Debug information")

    class Config:
        json_schema_extra = {
            "example": {
                "next_step_id": "1.1.2",
                "message_for_student": "What is your project goal? (2-3 sentences)",
                "done": False,
                "canvas_update": None,
                "debug_info": {"step_count": 1}
            }
        }


# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="BIOS Orchestrator API",
    description="Backend for B42 Chatstorm Custom GPT - enforces workflow execution",
    version="1.0.0"
)

# Enable CORS (needed for Custom GPT Actions)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Global State
# ============================================================================

# Session manager (handles all student sessions)
session_manager: Optional[SessionManager] = None


@app.on_event("startup")
async def startup_event():
    """Initialize session manager on startup"""
    global session_manager

    # Get LLM provider and API key from environment
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")

    if not api_key and llm_provider != "mock":
        print("WARNING: No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY env var.")
        print("Falling back to mock mode.")
        llm_provider = "mock"

    session_manager = SessionManager(
        llm_provider=llm_provider,
        api_key=api_key
    )

    print(f"\n{'='*60}")
    print("BIOS Orchestrator API Started")
    print(f"{'='*60}")
    print(f"LLM Provider: {llm_provider}")
    print(f"API Key: {'Set' if api_key else 'Not set (using mock)'}")
    print(f"Endpoint: POST /next_step")
    print(f"Docs: http://localhost:8000/docs")
    print(f"{'='*60}\n")


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "BIOS Orchestrator API",
        "active_sessions": session_manager.get_active_session_count() if session_manager else 0,
        "docs": "/docs"
    }


@app.post("/next_step", response_model=NextStepResponse)
async def next_step(req: NextStepRequest):
    """
    Get the next workflow step.

    This is called by the Custom GPT on every turn.
    The orchestrator controls step advancement (GPT never decides next step).
    """
    if session_manager is None:
        raise HTTPException(status_code=500, detail="Session manager not initialized")

    print(f"\n[API] /next_step called")
    print(f"  Session: {req.session_id}")
    print(f"  Current step: {req.current_step_id}")
    print(f"  Student message: {req.student_message[:100]}...")

    try:
        # Get or create session
        session = session_manager.get_or_create_session(req.session_id)
        orchestrator = session.orchestrator

        # If this is the first call (no current_step_id), just return first question
        if req.current_step_id is None:
            current_step = orchestrator.runtime.get_step(orchestrator.current_step_id)
            return NextStepResponse(
                next_step_id=orchestrator.current_step_id,
                message_for_student=current_step.required_output,
                done=False,
                debug_info={
                    "step_count": 0,
                    "target": current_step.target
                }
            )

        # Verify current_step_id matches session state
        if req.current_step_id != orchestrator.current_step_id:
            print(f"  WARNING: Step mismatch. Expected {orchestrator.current_step_id}, got {req.current_step_id}")
            # Use session's step as source of truth
            current_step_id = orchestrator.current_step_id
        else:
            current_step_id = req.current_step_id

        # Get current step
        current_step = orchestrator.runtime.get_step(current_step_id)

        # Store student's answer
        orchestrator.student_state[current_step_id] = req.student_message

        # Validate answer (simplified for now - just accept it)
        # In production, you'd use orchestrator.student_handler.validate_answer()
        validation_ok = True

        if not validation_ok:
            # TODO: Handle validation failure (ask for clarification)
            pass

        # Apply canvas update if present
        if current_step.canvas_update:
            from canvas_state import apply_canvas_update
            orchestrator.canvas = apply_canvas_update(
                orchestrator.canvas,
                current_step.canvas_update,
                orchestrator.student_state
            )
            print(f"  Canvas updated: {current_step.canvas_update.get('section')}")

        # Advance to next step (CODE controls this, not LLM!)
        next_step_id = current_step.next_step

        if next_step_id is None or next_step_id == "END" or next_step_id == "DONE":
            # Workflow complete
            return NextStepResponse(
                next_step_id=current_step_id,
                message_for_student="Workflow complete! Your simulation design is ready.",
                done=True,
                debug_info={
                    "total_steps": len(orchestrator.student_state),
                    "canvas_state": "complete"
                }
            )

        # Update orchestrator state
        orchestrator.current_step_id = next_step_id

        # Get next step
        next_step = orchestrator.runtime.get_step(next_step_id)

        # Return next question
        response = NextStepResponse(
            next_step_id=next_step_id,
            message_for_student=next_step.required_output,
            done=False,
            debug_info={
                "step_count": len(orchestrator.student_state),
                "target": next_step.target,
                "previous_step": current_step_id
            }
        )

        print(f"  → Next step: {next_step_id} ({next_step.target})")
        return response

    except KeyError as e:
        print(f"  ERROR: Step not found: {e}")
        raise HTTPException(status_code=400, detail=f"Step not found: {e}")
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions")
async def list_sessions():
    """List all active sessions (for debugging)"""
    if session_manager is None:
        return {"sessions": []}

    sessions_info = []
    for sid, session in session_manager.sessions.items():
        sessions_info.append({
            "session_id": sid,
            "current_step": session.get_current_step_id(),
            "answers_collected": len(session.get_student_answers()),
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat()
        })

    return {
        "active_sessions": len(sessions_info),
        "sessions": sessions_info
    }


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a specific session"""
    if session_manager is None:
        raise HTTPException(status_code=500, detail="Session manager not initialized")

    session_manager.delete_session(session_id)
    return {"status": "deleted", "session_id": session_id}


@app.post("/sessions/{session_id}/reset")
async def reset_session(session_id: str):
    """Reset a session to the beginning"""
    if session_manager is None:
        raise HTTPException(status_code=500, detail="Session manager not initialized")

    # Delete and recreate
    session_manager.delete_session(session_id)
    session = session_manager.get_or_create_session(session_id)

    return {
        "status": "reset",
        "session_id": session_id,
        "current_step": session.get_current_step_id()
    }


# ============================================================================
# Run locally (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("Starting BIOS Orchestrator API...")
    print("Docs will be available at: http://localhost:8000/docs")
    print("\nTo expose via ngrok, run in another terminal:")
    print("  ngrok http 8000")

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
