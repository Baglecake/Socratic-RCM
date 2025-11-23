# BIOS Orchestrator API - Setup Guide

**Goal**: Run the orchestrator locally and make it accessible to students via Custom GPT + ngrok.

---

## Architecture Overview

```
Student → Custom GPT (Builder) → GPT Action → ngrok HTTPS → localhost:8000 → Orchestrator → Runtime Files
                                                                     ↓
                                                                LLM (validation)
```

**Benefits**:
- ✅ Students use familiar GPT interface
- ✅ Code enforces workflow (no step skipping)
- ✅ Free (runs on your laptop)
- ✅ No cloud deployment needed

---

## Prerequisites

1. **Python 3.8+** installed
2. **OpenAI API key** (or Anthropic API key)
3. **ngrok account** (free tier is fine)
4. **Custom GPT access** (ChatGPT Plus/Pro)

---

## Step 1: Install Python Dependencies

```bash
cd experimental/bios-architecture/orchestrator_api

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- uvicorn (ASGI server)
- pydantic (data validation)
- openai/anthropic (optional, for LLM calls)

---

## Step 2: Set Environment Variables

Create a `.env` file in `orchestrator_api/`:

```bash
# Choose LLM provider: openai, anthropic, or mock
LLM_PROVIDER=openai

# OpenAI API key (if using OpenAI)
OPENAI_API_KEY=sk-your-key-here

# OR Anthropic API key (if using Anthropic)
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Or export directly:

```bash
export OPENAI_API_KEY="sk-your-key-here"
export LLM_PROVIDER="openai"
```

**For testing without API costs**, use `LLM_PROVIDER=mock` (no API key needed).

---

## Step 3: Start the FastAPI Server

```bash
cd experimental/bios-architecture/orchestrator_api
uvicorn main:app --reload --port 8000
```

You should see:

```
============================================================
BIOS Orchestrator API Started
============================================================
LLM Provider: openai
API Key: Set
Endpoint: POST /next_step
Docs: http://localhost:8000/docs
============================================================

INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Test it**: Open http://localhost:8000 in your browser. You should see:

```json
{
  "status": "running",
  "service": "BIOS Orchestrator API",
  "active_sessions": 0,
  "docs": "/docs"
}
```

**Explore the API**: Go to http://localhost:8000/docs to see interactive Swagger UI.

---

## Step 4: Install and Configure ngrok

### Install ngrok

**Mac (Homebrew)**:
```bash
brew install ngrok
```

**Other platforms**: Download from https://ngrok.com/download

### Authenticate ngrok

1. Sign up at https://ngrok.com (free tier is fine)
2. Get your auth token from https://dashboard.ngrok.com/get-started/your-authtoken
3. Configure ngrok:

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### Start ngrok

In a **new terminal** (keep uvicorn running):

```bash
ngrok http 8000
```

You'll see:

```
Session Status: online
Forwarding: https://abc123xyz.ngrok.app -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123xyz.ngrok.app`). This is your public endpoint.

**Important**: This URL changes every time you restart ngrok (unless you have a paid plan). You'll need to update the Custom GPT Action each time.

---

## Step 5: Test the API via ngrok

Open a **third terminal** and test:

```bash
curl https://abc123xyz.ngrok.app/
```

You should get the same JSON response as http://localhost:8000.

Test the `/next_step` endpoint:

```bash
curl -X POST https://abc123xyz.ngrok.app/next_step \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "current_step_id": null,
    "student_message": "I want to start my project"
  }'
```

You should get:

```json
{
  "next_step_id": "1.1.1",
  "message_for_student": "What is your project goal? ...",
  "done": false,
  "debug_info": {...}
}
```

**If this works, your API is ready for Custom GPT integration.**

---

## Step 6: Create Custom GPT

Go to https://chat.openai.com/gpts/editor

### Name and Description

- **Name**: B42 Chatstorm Teaching Assistant
- **Description**: Helps students design agent-based simulations for B42 final project

### Instructions (System Prompt)

Paste the following (also available in `custom_gpt_instructions.txt`):

```
You are the B42 Chatstorm Teaching Assistant, helping students design agent-based simulations.

CRITICAL: You NEVER control the workflow. You ALWAYS use the next_step Action.

On EVERY user message:
1. Call the next_step Action with:
   - session_id: Use the conversation ID (or a constant like "conv-{timestamp}")
   - current_step_id: The last next_step_id you received (null if this is the first message)
   - student_message: The user's message

2. Show the message_for_student field to the user EXACTLY as returned.

3. DO NOT make up questions. DO NOT skip steps. DO NOT improvise.

4. If done=true, congratulate them and offer to export the design.

You are a passthrough for the orchestrator. The orchestrator enforces the workflow.
```

### Conversation Starters

Add these to help students:

- "Help me start my B42 final project"
- "I want to design a simulation"
- "I need help with my Chatstorm design"

### Knowledge (Optional)

You can upload:
- Theory files (marx_theory.txt, tocqueville_theory.txt, etc.)
- Assignment files (B42 Final Project.txt, Step-by-Step Guide.txt)

But the orchestrator already has access to these via runtime files.

---

## Step 7: Add the Action

Click **"Create new action"** in the Custom GPT editor.

### Action Schema

Paste this OpenAPI schema (also available in `custom_gpt_action_schema.json`):

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "BIOS Orchestrator API",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://YOUR_NGROK_URL_HERE.ngrok.app"
    }
  ],
  "paths": {
    "/next_step": {
      "post": {
        "summary": "Get next workflow step",
        "operationId": "next_step",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "session_id": {
                    "type": "string",
                    "description": "Unique session ID"
                  },
                  "current_step_id": {
                    "type": "string",
                    "nullable": true,
                    "description": "Current step ID (null if starting)"
                  },
                  "student_message": {
                    "type": "string",
                    "description": "Student's response"
                  }
                },
                "required": ["session_id", "student_message"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Next step",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "next_step_id": {
                      "type": "string"
                    },
                    "message_for_student": {
                      "type": "string"
                    },
                    "done": {
                      "type": "boolean"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

**IMPORTANT**: Replace `YOUR_NGROK_URL_HERE` with your actual ngrok URL.

### Privacy

Set to **"Only me"** for testing, or **"Anyone with a link"** for students.

---

## Step 8: Test the Custom GPT

1. Click **"Test"** in the GPT editor
2. Send a message: "Help me start my project"
3. The GPT should:
   - Call your `/next_step` endpoint via ngrok
   - Receive the first question from the orchestrator
   - Display it to you

**Check your FastAPI logs** (in the terminal running uvicorn). You should see:

```
[API] /next_step called
  Session: conv-12345
  Current step: None
  Student message: Help me start my project...
  → Next step: 1.1.1 (Project Goal)
```

**If this works, your integration is complete!**

---

## Troubleshooting

### FastAPI won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Fix**: Make sure you activated the virtual environment and ran `pip install -r requirements.txt`

### ngrok connection refused

**Error**: `Failed to establish connection`

**Fix**: Make sure uvicorn is running on port 8000 before starting ngrok.

### Custom GPT Action fails

**Error**: `Action failed to execute`

**Fix**:
1. Check ngrok is running and URL is correct
2. Check FastAPI logs for errors
3. Test the endpoint with curl first
4. Make sure OpenAPI schema has correct ngrok URL

### Session state not persisting

**Issue**: Each call seems to start from scratch

**Fix**: Make sure the Custom GPT is using the same `session_id` on each call. Check the GPT instructions include the session_id logic.

### LLM validation errors

**Error**: OpenAI/Anthropic API errors

**Fix**:
1. Check API key is set correctly
2. Check you have credits/quota
3. For testing, use `LLM_PROVIDER=mock` to avoid API calls

---

## Development Workflow

### Typical session

1. Start FastAPI: `uvicorn main:app --reload --port 8000`
2. Start ngrok (separate terminal): `ngrok http 8000`
3. Copy ngrok URL to Custom GPT Action schema
4. Test via Custom GPT
5. Watch logs in uvicorn terminal
6. Make code changes (uvicorn auto-reloads)

### Debugging

**View active sessions**:
```bash
curl http://localhost:8000/sessions
```

**Reset a session**:
```bash
curl -X POST http://localhost:8000/sessions/SESSION_ID/reset
```

**Delete a session**:
```bash
curl -X DELETE http://localhost:8000/sessions/SESSION_ID
```

**View API docs**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Production Deployment (Optional)

For permanent deployment (instead of ngrok):

### Option 1: Railway.app (Free tier)

1. Push code to GitHub
2. Connect Railway to your repo
3. Set environment variables (OPENAI_API_KEY, etc.)
4. Railway gives you a permanent HTTPS URL
5. Update Custom GPT Action with Railway URL

### Option 2: Render.com (Free tier)

Similar process to Railway.

### Option 3: Your own server

Deploy with nginx + gunicorn + systemd.

---

## Next Steps

Once the integration is working:

1. **Test full workflow**: Run through Phase 1, 2, 3
2. **Monitor logs**: Watch for step skipping or hallucination (should be impossible)
3. **Enhance validation**: Implement proper constraint checking via LLM
4. **Add analytics**: Track completion rates, retry rates, etc.
5. **Build admin dashboard**: Web UI to view all sessions

---

## Files Reference

- `main.py` - FastAPI application
- `session_manager.py` - Session state management
- `requirements.txt` - Python dependencies
- `SETUP.md` - This file
- `custom_gpt_instructions.txt` - System prompt for Custom GPT
- `custom_gpt_action_schema.json` - OpenAPI schema for Action

---

**Status**: Ready to deploy

**Questions?** Check the main [README.md](../orchestrator/README.md) for orchestrator details.
