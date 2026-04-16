# Phase 11 — Self-Healing: API, Treatment Executor, AIBriefing Integration

## Goal
AgentClinic becomes actionable. Sessions (Claude Code, Codex, any AI session) can invoke
`/diagnose`, which POSTs context to AgentClinic's API. AgentClinic diagnoses, generates
concrete treatment steps, and queues the remedy for staff review in AIBriefing. Staff
approves via `chat.py`. Approved remedies return actionable treatment steps.

---

## Flow

```
AI session goes wrong (or user notices issue)
    → /diagnose skill invoked in Claude Code / Codex
    → session context + symptoms POSTed to AgentClinic API
    → diagnosis chain runs (ailment + therapy classified)
    → treatment plan generated (concrete steps for that session type)
    → remedy queued in AIBriefing SQLite as pending
    → daily HTML briefing shows "N remedies to review"
    → staff reviews via chat.py → approve or reject
    → if approved → treatment steps available via API / displayed in session
```

---

## Part 1 — AgentClinic API endpoint

### `POST /api/diagnose`
Accepts JSON:
```json
{
  "agent_name": "Claude Code Session",
  "session_type": "claude-code | codex | other",
  "symptoms": "Context is getting heavy, responses recapping too much"
}
```

Returns JSON:
```json
{
  "diagnosis_id": 42,
  "ailment": "Context Window Overflow",
  "therapy": "Context Flush",
  "treatment_steps": [
    "Run /compact to summarise conversation history",
    "If issue persists, start a new session with a handoff file"
  ],
  "status": "PENDING_APPROVAL"
}
```

- Runs the existing diagnosis chain
- Saves to `diagnosis_runs` table
- Also creates a pending remedy in AIBriefing

### Treatment step generator
Each therapy maps to concrete steps per session type:

| Therapy | Claude Code steps | Codex steps |
|---|---|---|
| Context Flush | Run `/compact` | Start new Codex session |
| Memory Summary Injection | Run `session-handoff` skill, paste summary into new session | Export context summary, re-inject |
| Instruction Set Reduction | Review and trim CLAUDE.md active rules | Reduce system prompt |
| Compression Prompt | Run `ultra` skill | Apply `round3_refined` prompt |
| Session Reset | Close session, resume from handoff | New Codex session from spec |
| Novelty Injection | Ask model to approach differently: "Try a completely different approach" | Change effort level or model |
| Confidence Recalibration | Relax constraints in prompt | Adjust model temperature/effort |
| Task Decomposition | Break task into subtasks using `subagents-prompt` skill | Split into multiple Codex tasks |

---

## Part 2 — AIBriefing integration

### New `remedies` table in AIBriefing SQLite
```python
class Remedy(Base):
    __tablename__ = "remedies"
    id = Column(Integer, primary_key=True)
    diagnosis_id = Column(Integer)           # AgentClinic diagnosis_run.id
    agent_name = Column(String)
    session_type = Column(String)
    ailment = Column(String)
    therapy = Column(String)
    treatment_steps = Column(Text)           # JSON list
    status = Column(String, default="PENDING")  # PENDING, APPROVED, REJECTED
    created_at = Column(DateTime, default=datetime.now)
    reviewed_at = Column(DateTime, nullable=True)
```

### Daily HTML briefing
- Add "Remedies to Review" count to the summary section
- Shows: N pending remedies

### chat.py integration
New command: `review remedies`
- Walks through PENDING remedies one by one
- Shows: agent, ailment, therapy, treatment steps
- User responds: approve / reject / skip
- Updates status in DB
- If approved: marks diagnosis_run outcome as APPROVED in AgentClinic

---

## Part 3 — `/diagnose` skill for Claude Code

New skill: `diagnose`
- Collects: current session symptoms (user describes or auto-detected)
- POSTs to `http://localhost:8000/api/diagnose`
- Displays returned treatment steps
- If server not running: falls back to local diagnosis (runs chain directly)

---

## Out of scope
- Automated symptom detection (no auto-trigger yet — user or agent invokes manually)
- Push notifications (Telegram message on new remedy — later)
- Two-way sync between AgentClinic and AIBriefing DBs (one-way write for now)
