# BIOS Orchestrator API

**FastAPI server for Custom GPT integration - makes the orchestrator accessible to students**

---

## What This Is

A **REST API wrapper** around the BIOS orchestrator that allows students to interact via Custom GPT while the backend enforces workflow execution.

**Architecture:**
```
Student → Custom GPT (familiar interface)
            ↓
       GPT Action (calls /next_step)
            ↓
       ngrok HTTPS URL
            ↓
       localhost:8000 FastAPI
            ↓
       Orchestrator (code-enforced workflow)
            ↓
       Runtime Files (Step definitions)
```

**Benefits:**
- ✅ Students use familiar GPT Builder interface
- ✅ Code enforces workflow (guaranteed no step skipping)
- ✅ Free (runs on your laptop via ngrok)
- ✅ No cloud deployment needed (for development)
- ✅ Session persistence across calls
- ✅ Full logging and debugging

---

## Quick Start

### 1. Install Dependencies

```bash
cd experimental/bios-architecture/orchestrator_api
pip install -r requirements.txt
```

### 2. Set API Key

```bash
export OPENAI_API_KEY="sk-your-key-here"
export LLM_PROVIDER="openai"
```

Or use `LLM_PROVIDER=mock` for testing without API costs.

### 3. Start the Server

```bash
uvicorn main:app --reload --port 8000
```

### 4. Expose via ngrok (separate terminal)

```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.app`).

### 5. Configure Custom GPT

1. Go to https://chat.openai.com/gpts/editor
2. Paste instructions from `custom_gpt_instructions.txt`
3. Add Action using schema from `custom_gpt_action_schema.json`
4. Replace `YOUR_NGROK_URL_HERE` with your ngrok URL
5. Test!

**Full setup guide**: See [SETUP.md](SETUP.md)

---

## API Endpoints

### `POST /next_step`

Get the next workflow step.

**Request:**
```json
{
  "session_id": "user-123",
  "current_step_id": "1.1.1",
  "student_message": "I want to explore class conflict"
}
```

**Response:**
```json
{
  "next_step_id": "1.1.2",
  "message_for_student": "What is your project goal? (2-3 sentences)",
  "done": false,
  "debug_info": {
    "step_count": 1,
    "target": "Project Goal"
  }
}
```

### `GET /`

Health check.

**Response:**
```json
{
  "status": "running",
  "service": "BIOS Orchestrator API",
  "active_sessions": 2
}
```

### `GET /sessions`

List all active sessions (for debugging).

### `DELETE /sessions/{session_id}`

Delete a specific session.

### `POST /sessions/{session_id}/reset`

Reset a session to the beginning.

---

## How It Works

### Session Management

Each Custom GPT conversation gets a unique `session_id`. The session persists:
- Current step_id
- Canvas state
- Student answers
- Orchestrator instance

**Example flow:**

1. Student sends first message
2. Custom GPT calls `/next_step` with `session_id="conv-123"` and `current_step_id=null`
3. API creates new session, returns Step 1.1.1 question
4. Student answers
5. Custom GPT calls `/next_step` with `session_id="conv-123"` and `current_step_id="1.1.1"`
6. API stores answer, advances to Step 1.1.2, returns next question
7. Repeat until `done=true`

### Workflow Enforcement

**Key principle**: The LLM (Custom GPT) NEVER decides the next step. Code controls advancement.

```python
# In main.py
current_step = runtime.get_step(current_step_id)
orchestrator.student_state[current_step_id] = student_message
next_step_id = current_step.next_step  # CODE decides, not LLM
orchestrator.current_step_id = next_step_id
```

This **guarantees**:
- ✅ No step skipping (Step 2.2.6 will NEVER be skipped)
- ✅ No hallucinated questions (questions read from runtime files)
- ✅ Correct sequencing (NEXT STEP field controls flow)

---

## Files

```
orchestrator_api/
├── main.py                          # FastAPI application
├── session_manager.py               # Session state management
├── requirements.txt                 # Python dependencies
├── SETUP.md                         # Detailed setup guide
├── custom_gpt_instructions.txt      # System prompt for Custom GPT
├── custom_gpt_action_schema.json    # OpenAPI schema for GPT Action
└── README.md                        # This file
```

---

## Development

### Run locally

```bash
uvicorn main:app --reload --port 8000
```

Auto-reloads on code changes.

### View API docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Test without Custom GPT

```bash
curl -X POST http://localhost:8000/next_step \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "current_step_id": null,
    "student_message": "I want to start my project"
  }'
```

### Debug sessions

```bash
# List active sessions
curl http://localhost:8000/sessions

# Reset a session
curl -X POST http://localhost:8000/sessions/test-123/reset

# Delete a session
curl -X DELETE http://localhost:8000/sessions/test-123
```

### Logs

Watch the uvicorn terminal for real-time logs:

```
[API] /next_step called
  Session: conv-123
  Current step: 1.1.1
  Student message: I want to explore class conflict...
  → Next step: 1.1.2 (Project Goal)
```

---

## Deployment

### Development (ngrok - free)

See [SETUP.md](SETUP.md)

### Production (Railway/Render - free tier)

1. Push code to GitHub
2. Connect Railway/Render to your repo
3. Set environment variables (OPENAI_API_KEY, LLM_PROVIDER)
4. Get permanent HTTPS URL
5. Update Custom GPT Action with production URL

**No code changes needed** - same FastAPI app works for both development and production.

---

## Troubleshooting

**FastAPI won't start**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

**ngrok connection refused**
- Make sure uvicorn is running first
- Check port 8000 is not already in use

**Custom GPT Action fails**
- Check ngrok URL is correct in Action schema
- Check uvicorn and ngrok are both running
- Test endpoint with curl first

**Sessions not persisting**
- Check Custom GPT is using same `session_id` on each call
- Check session_id logic in Custom GPT instructions

**LLM API errors**
- Check API key is set correctly
- Check you have credits/quota
- Use `LLM_PROVIDER=mock` for testing

---

## Architecture Comparison

### Before (Prompt-Based BIOS)

```
Student → Custom GPT → BIOS system prompt
                        ↓
                 LLM decides next step (unreliable)
                        ↓
                 May skip steps (lazy retrieval)
```

**Result**: Step 2.2.6 skipped, Step 2.2.9 hallucinated

### After (Code Orchestrator + API)

```
Student → Custom GPT → /next_step API
                        ↓
                 Code decides next step (reliable)
                        ↓
                 Runtime files = source of truth
```

**Result**: Guaranteed no skipping, no hallucination

---

## Integration with Orchestrator

The API uses the orchestrator we built earlier:

```python
from orchestrator import create_orchestrator
from llm_client import create_llm_client

llm = create_llm_client("openai", api_key=api_key)
orchestrator = create_orchestrator(llm, bios_prompt, starting_step="1.1.1")
```

**The orchestrator handles**:
- Runtime file parsing
- Step execution
- Canvas updates
- Answer validation

**The API handles**:
- HTTP endpoints
- Session management
- Request/response formatting
- Multi-student support

---

## Success Metrics

With this architecture, you get:

1. ✅ **Zero step skipping** - Code enforces sequence
2. ✅ **Zero hallucination** - Questions from runtime files
3. ✅ **Full logging** - Every step tracked
4. ✅ **Session persistence** - Students can pause/resume
5. ✅ **Multi-student** - Each gets their own session
6. ✅ **Easy updates** - Edit runtime files, restart server
7. ✅ **Debuggable** - Inspect any session's state

---

## Next Steps

Once you have it running:

1. **Test full workflow** - Phase 1 → 2 → 3
2. **Monitor logs** - Verify no step skipping
3. **Enhance validation** - Implement constraint checking
4. **Add analytics** - Track completion rates, retry rates
5. **Build dashboard** - Web UI to view all sessions
6. **Deploy to production** - Railway/Render for permanent URL

---

**Status**: ✅ Ready to deploy

**Documentation**: See [SETUP.md](SETUP.md) for detailed setup instructions

**Parent project**: [BIOS Orchestrator](../orchestrator/README.md)
