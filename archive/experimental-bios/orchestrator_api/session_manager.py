"""
Session Manager - Track student workflow state across API calls

Each student gets a unique session that persists:
- Current step_id
- Canvas state
- Student answers
- Orchestrator instance
"""

import os
import sys
from typing import Dict, Optional
from datetime import datetime

# Add parent directory to path to import orchestrator modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'orchestrator'))

from orchestrator import WorkflowOrchestrator, create_orchestrator
from canvas_state import CanvasState
from llm_client import create_llm_client


class StudentSession:
    """Represents a single student's workflow session"""

    def __init__(self, session_id: str, orchestrator: WorkflowOrchestrator):
        self.session_id = session_id
        self.orchestrator = orchestrator
        self.created_at = datetime.now()
        self.last_activity = datetime.now()

    def get_current_step_id(self) -> Optional[str]:
        """Get the current step ID"""
        return self.orchestrator.current_step_id

    def get_canvas_state(self) -> CanvasState:
        """Get the current canvas state"""
        return self.orchestrator.get_canvas_state()

    def get_student_answers(self) -> Dict[str, str]:
        """Get all student answers so far"""
        return self.orchestrator.get_student_answers()

    def update_activity(self):
        """Mark session as recently active"""
        self.last_activity = datetime.now()


class SessionManager:
    """
    Manages multiple student sessions.

    Each Custom GPT conversation gets a unique session_id.
    The session persists the orchestrator state across API calls.
    """

    def __init__(self, llm_provider: str = "openai", api_key: Optional[str] = None):
        self.sessions: Dict[str, StudentSession] = {}
        self.llm_provider = llm_provider
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        # Load BIOS prompt once
        bios_prompt_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'orchestrator',
            'bios_reduced_prompt.txt'
        )
        with open(bios_prompt_path, 'r') as f:
            self.bios_prompt = f.read()

    def get_or_create_session(self, session_id: str) -> StudentSession:
        """
        Get existing session or create new one.

        Args:
            session_id: Unique identifier for this student session

        Returns:
            StudentSession instance
        """
        if session_id not in self.sessions:
            # Create new orchestrator for this session
            llm = create_llm_client(
                provider=self.llm_provider,
                api_key=self.api_key
            )

            orchestrator = create_orchestrator(
                llm_client=llm,
                bios_prompt=self.bios_prompt,
                starting_step="1.1.1"
            )

            # Create session
            session = StudentSession(session_id, orchestrator)
            self.sessions[session_id] = session

            print(f"[SessionManager] Created new session: {session_id}")
        else:
            session = self.sessions[session_id]
            session.update_activity()

        return session

    def get_session(self, session_id: str) -> Optional[StudentSession]:
        """Get existing session (returns None if not found)"""
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str):
        """Delete a session (e.g., after workflow completion)"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            print(f"[SessionManager] Deleted session: {session_id}")

    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """
        Remove sessions that haven't been active in max_age_hours.

        Args:
            max_age_hours: Maximum age in hours before session is deleted
        """
        from datetime import timedelta

        now = datetime.now()
        cutoff = now - timedelta(hours=max_age_hours)

        old_sessions = [
            sid for sid, session in self.sessions.items()
            if session.last_activity < cutoff
        ]

        for sid in old_sessions:
            self.delete_session(sid)

        if old_sessions:
            print(f"[SessionManager] Cleaned up {len(old_sessions)} old sessions")

    def get_active_session_count(self) -> int:
        """Get number of active sessions"""
        return len(self.sessions)

    def list_sessions(self):
        """List all active sessions (for debugging)"""
        print(f"\n=== Active Sessions ({len(self.sessions)}) ===")
        for sid, session in self.sessions.items():
            print(f"  {sid}:")
            print(f"    Current step: {session.get_current_step_id()}")
            print(f"    Answers collected: {len(session.get_student_answers())}")
            print(f"    Last activity: {session.last_activity}")


if __name__ == "__main__":
    # Test session manager
    manager = SessionManager(llm_provider="mock")

    # Create a session
    session = manager.get_or_create_session("test-session-1")
    print(f"Session created: {session.session_id}")
    print(f"Current step: {session.get_current_step_id()}")

    # Get same session again
    session2 = manager.get_or_create_session("test-session-1")
    print(f"Same session? {session is session2}")

    # List sessions
    manager.list_sessions()
