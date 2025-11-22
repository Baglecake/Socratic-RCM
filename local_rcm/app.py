#!/usr/bin/env python3
"""
Socratic-RCM Streamlit App

A web interface for the RCM orchestrator with optional student simulation.

Usage:
    streamlit run app.py
"""

import os
import sys
import json
import streamlit as st

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from llm_client import create_llm_client, StudentSimulator
from orchestrator import create_orchestrator
from canvas_state import compile_final_document, compile_canvas_from_student_state


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Socratic-RCM",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_session_state():
    """Initialize session state variables"""
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = None
    if "simulator" not in st.session_state:
        st.session_state.simulator = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "workflow_started" not in st.session_state:
        st.session_state.workflow_started = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "auto_mode" not in st.session_state:
        st.session_state.auto_mode = False
    if "step_count" not in st.session_state:
        st.session_state.step_count = 0


init_session_state()


# =============================================================================
# SIDEBAR - Configuration
# =============================================================================

with st.sidebar:
    st.title("🎓 Socratic-RCM")
    st.markdown("---")

    # LLM Configuration
    st.subheader("🔧 LLM Configuration")

    llm_mode = st.selectbox(
        "LLM Mode",
        ["mock", "runpod", "openai"],
        help="Select the LLM backend"
    )

    if llm_mode == "runpod":
        base_url = st.text_input(
            "RunPod Endpoint URL",
            value="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1",
            help="Your RunPod serverless endpoint URL"
        )
        api_key = st.text_input(
            "RunPod API Key",
            type="password",
            help="Your RunPod API key"
        )
        model_name = st.text_input(
            "Model Name",
            value="Qwen/Qwen2.5-7B-Instruct",
            help="Model deployed on RunPod"
        )
    elif llm_mode == "openai":
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Your OpenAI API key"
        )
        model_name = st.selectbox(
            "Model",
            ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
        )
        base_url = None
    else:
        base_url = None
        model_name = None

    st.markdown("---")

    # Simulation Mode
    st.subheader("🤖 Student Simulation")
    auto_mode = st.checkbox(
        "Enable Auto-Mode",
        value=st.session_state.auto_mode,
        help="Use LLM to simulate student responses"
    )
    st.session_state.auto_mode = auto_mode

    if auto_mode:
        auto_steps = st.slider(
            "Steps per click",
            min_value=1,
            max_value=10,
            value=1,
            help="Number of steps to auto-complete per click"
        )

    st.markdown("---")

    # Workflow Control
    st.subheader("🎮 Workflow Control")

    if st.button("🚀 Start/Reset Workflow", use_container_width=True):
        try:
            # Create LLM client
            if llm_mode == "runpod":
                llm_client = create_llm_client(
                    provider="runpod",
                    base_url=base_url,
                    api_key=api_key,
                    model=model_name
                )
            elif llm_mode == "openai":
                llm_client = create_llm_client(
                    provider="openai",
                    api_key=api_key,
                    model=model_name
                )
            else:
                llm_client = create_llm_client(provider="mock")

            # Load BIOS prompt
            bios_path = os.path.join(os.path.dirname(__file__), "bios_reduced_prompt.txt")
            with open(bios_path, 'r') as f:
                bios_prompt = f.read()

            # Create orchestrator
            st.session_state.orchestrator = create_orchestrator(
                llm_client=llm_client,
                bios_prompt=bios_prompt,
                starting_step="1.1"
            )

            # Create simulator if auto mode
            if auto_mode:
                st.session_state.simulator = StudentSimulator(llm_client)

            # Reset state
            st.session_state.messages = []
            st.session_state.workflow_started = True
            st.session_state.step_count = 0

            # Get first question
            step = st.session_state.orchestrator.runtime.get_step(
                st.session_state.orchestrator.current_step_id
            )
            st.session_state.current_question = step.required_output

            st.success("✓ Workflow initialized!")
            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")

    # Progress Display
    if st.session_state.orchestrator:
        st.subheader("📊 Progress")
        orch = st.session_state.orchestrator
        current = orch.current_step_id or "Complete"

        # Parse phase from step ID
        if current != "Complete":
            phase = current.split(".")[0]
            phase_names = {"1": "Conceptualization", "2": "Drafting", "3": "Review"}
            phase_name = phase_names.get(phase, "Unknown")
        else:
            phase_name = "Complete"

        st.metric("Current Step", current)
        st.metric("Phase", phase_name)
        st.metric("Steps Completed", st.session_state.step_count)
        st.metric("Answers Collected", len(orch.student_state))

    st.markdown("---")

    # Export
    st.subheader("💾 Export")
    if st.session_state.orchestrator:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 JSON", use_container_width=True):
                state = {
                    "current_step": st.session_state.orchestrator.current_step_id,
                    "student_state": st.session_state.orchestrator.student_state
                }
                st.download_button(
                    "Download JSON",
                    json.dumps(state, indent=2),
                    "rcm_state.json",
                    "application/json"
                )
        with col2:
            if st.button("📝 Document", use_container_width=True):
                canvas = compile_canvas_from_student_state(
                    st.session_state.orchestrator.student_state
                )
                doc = compile_final_document(canvas)
                st.download_button(
                    "Download TXT",
                    doc,
                    "rcm_document.txt",
                    "text/plain"
                )


# =============================================================================
# MAIN AREA
# =============================================================================

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Socratic-RCM Workflow")
with col2:
    if st.session_state.orchestrator and st.session_state.orchestrator.current_step_id:
        st.markdown(f"### Step: `{st.session_state.orchestrator.current_step_id}`")

st.markdown("---")

# Workflow not started
if not st.session_state.workflow_started:
    st.info("👈 Configure settings and click **Start/Reset Workflow** to begin")

    # Show quick start guide
    with st.expander("📖 Quick Start Guide"):
        st.markdown("""
        ### How to Use

        1. **Configure LLM** - Select mock (testing), RunPod (GPU), or OpenAI
        2. **Enable Auto-Mode** (optional) - Let the LLM simulate a student
        3. **Start Workflow** - Click the button to begin
        4. **Answer Questions** - Type responses or use auto-mode
        5. **Export** - Download your simulation design as JSON or TXT

        ### Modes

        - **Mock Mode**: Testing without API calls
        - **RunPod Mode**: Connect to your RunPod serverless endpoint
        - **OpenAI Mode**: Use GPT-4 (requires API key)
        - **Auto-Mode**: LLM generates student responses automatically

        ### RunPod Setup

        1. Create a RunPod account at runpod.io
        2. Deploy a serverless vLLM endpoint with Qwen2.5-7B-Instruct
        3. Copy your endpoint URL and API key
        4. Paste them in the sidebar configuration
        """)

else:
    # Main workflow area
    orch = st.session_state.orchestrator

    if orch.current_step_id is None:
        # Workflow complete
        st.success("🎉 Workflow Complete!")

        # Show final document
        with st.expander("📄 Final Design Document", expanded=True):
            canvas = compile_canvas_from_student_state(orch.student_state)
            doc = compile_final_document(canvas)
            st.text(doc)

    else:
        # Current step info
        try:
            step = orch.runtime.get_step(orch.current_step_id)

            # Question display
            st.subheader("💭 Current Question")
            question_text = orch._substitute_placeholders(step.required_output, orch.current_step_id)
            st.info(question_text)

            # RCM Cue (if present)
            if step.rcm_cue:
                with st.expander("🎯 RCM Guidance"):
                    st.markdown(step.rcm_cue)

            st.markdown("---")

            # Response area
            if st.session_state.auto_mode:
                # Auto mode - show button to generate response
                st.subheader("🤖 Auto Mode")

                if st.button("▶️ Generate Response & Continue", use_container_width=True):
                    with st.spinner("Generating student response..."):
                        # Generate response
                        response = st.session_state.simulator.respond(question_text)

                    st.markdown("**Student Response:**")
                    st.write(response)

                    # Validate the response
                    validation = {"ok": True, "reason": "No constraint"}
                    if step.constraint:
                        with st.spinner("Instructor validating..."):
                            validation = orch.student_handler.validate_answer(
                                response,
                                step.constraint,
                                step.target
                            )

                        if validation.get("ok"):
                            st.success(f"✓ Instructor: {validation.get('reason', 'Accepted')}")
                        else:
                            st.warning(f"⚠️ Instructor feedback: {validation.get('reason', 'Needs improvement')}")
                            if validation.get("suggestion"):
                                st.info(f"💡 {validation.get('suggestion')}")
                    else:
                        st.success("✓ Response recorded")

                    # Add to messages with validation info
                    st.session_state.messages.append({
                        "step": orch.current_step_id,
                        "question": question_text,
                        "answer": response,
                        "validation": validation.get("reason", "Accepted")
                    })

                    # Store in orchestrator
                    step_id = orch.current_step_id
                    if step_id in orch.student_state:
                        current_val = orch.student_state[step_id]
                        if isinstance(current_val, list):
                            current_val.append(response)
                        else:
                            orch.student_state[step_id] = [current_val, response]
                    else:
                        orch.student_state[step_id] = response

                    # Set framework after step 1.2.1 (theoretical option selection)
                    if step_id == "1.2.1":
                        orch.student_handler.set_framework(response)
                        # Also update the student simulator's persona
                        if st.session_state.simulator:
                            st.session_state.simulator.set_framework(response)
                        st.info(f"Framework locked: {response}")

                    # Brief pause to show feedback
                    import time
                    time.sleep(1)

                    # Advance to next step
                    raw_next = step.next_step
                    next_step = orch.resolve_next_step(step_id, raw_next)
                    if next_step in ["END", "DONE"]:
                        next_step = None
                    orch.current_step_id = next_step
                    st.session_state.step_count += 1

                    st.rerun()

            else:
                # Manual mode - show input
                st.subheader("✍️ Your Response")
                user_response = st.text_area(
                    "Enter your response:",
                    key=f"response_{orch.current_step_id}",
                    height=100
                )

                if st.button("Submit Response", use_container_width=True):
                    if user_response.strip():
                        # Add to messages
                        st.session_state.messages.append({
                            "step": orch.current_step_id,
                            "question": question_text,
                            "answer": user_response
                        })

                        # Store in orchestrator
                        step_id = orch.current_step_id
                        if step_id in orch.student_state:
                            current_val = orch.student_state[step_id]
                            if isinstance(current_val, list):
                                current_val.append(user_response)
                            else:
                                orch.student_state[step_id] = [current_val, user_response]
                        else:
                            orch.student_state[step_id] = user_response

                        # Set framework after step 1.2.1 (theoretical option selection)
                        if step_id == "1.2.1":
                            orch.student_handler.set_framework(user_response)
                            # Also update the student simulator's persona (if in auto mode)
                            if st.session_state.simulator:
                                st.session_state.simulator.set_framework(user_response)
                            st.info(f"Framework locked: {user_response}")

                        # Advance to next step
                        raw_next = step.next_step
                        next_step = orch.resolve_next_step(step_id, raw_next)
                        if next_step in ["END", "DONE"]:
                            next_step = None
                        orch.current_step_id = next_step
                        st.session_state.step_count += 1

                        st.rerun()
                    else:
                        st.warning("Please enter a response")

        except KeyError:
            st.error(f"Step {orch.current_step_id} not found in runtime")

        st.markdown("---")

        # Conversation history
        st.subheader("📜 Conversation History")
        if st.session_state.messages:
            for i, msg in enumerate(reversed(st.session_state.messages[-10:])):
                with st.expander(f"Step {msg['step']}", expanded=(i == 0)):
                    st.markdown(f"**Q:** {msg['question']}")
                    st.markdown(f"**A:** {msg['answer']}")
        else:
            st.caption("No responses yet")

        # Canvas preview
        with st.expander("📋 Canvas Preview"):
            if orch.student_state:
                canvas = compile_canvas_from_student_state(orch.student_state)
                doc = compile_final_document(canvas)
                st.text(doc[:2000] + "..." if len(doc) > 2000 else doc)
            else:
                st.caption("Canvas is empty")


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.caption("Socratic-RCM | Reflect-Connect-Ask | University of Toronto")
