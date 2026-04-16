# Phase 11 — Plan

## File structure
```
agentclinic-python/
  src/
    treatment.py                     (create — treatment step generator)
    api.py                           (create — POST /api/diagnose)
    main.py                          (update — mount api router)
  
AIBriefing/
  database.py                        (update — add Remedy table)
  remedies.py                        (create — add_remedy, get_pending_remedies, update_remedy_status)
  chat.py                            (update — add "review remedies" command)
  evening_digest.py / briefing.py    (update — add remedy count to HTML output)

~/.claude/skills/
  diagnose.md                        (create — /diagnose skill)
```

## Steps

### AgentClinic

1. Create `src/treatment.py`:
   - `TREATMENT_STEPS` dict — maps therapy name × session type → list of steps
   - `get_treatment_steps(therapy_name, session_type)` → list of strings

2. Create `src/api.py`:
   - FastAPI `APIRouter` with prefix `/api`
   - `POST /api/diagnose` — accepts JSON body, runs diagnosis chain,
     saves diagnosis run, calls AIBriefing `add_remedy()`, returns result
   - `GET /api/diagnose/{id}` — returns diagnosis run status + treatment steps

3. Update `src/main.py`:
   - `app.include_router(api_router)`

### AIBriefing

4. Update `AIBriefing/database.py`:
   - Add `Remedy` SQLAlchemy model
   - Run `Base.metadata.create_all(engine)` picks it up automatically

5. Create `AIBriefing/remedies.py`:
   - `add_remedy(diagnosis_id, agent_name, session_type, ailment, therapy, treatment_steps)`
   - `get_pending_remedies()` → list of PENDING remedies
   - `update_remedy_status(remedy_id, status)` → APPROVED or REJECTED
   - `get_remedy_count()` → count of PENDING

6. Update `AIBriefing/chat.py`:
   - Add "review remedies" command
   - Walks PENDING remedies: show details → approve/reject/skip
   - On approve → call AgentClinic `PATCH /api/diagnose/{id}/approve`

7. Update briefing HTML:

   **`evening_digest.py` — `generate_evening_html()`:**
   - Query `get_remedy_count()` (PENDING) and `get_recent_diagnoses(days=1)` from `remedies.py`
   - Add a new glass-card section: **"🩺 Agent Health Today"**
     - Stat: N remedies pending review
     - List: each diagnosis run from today — agent name, ailment, therapy, status badge
     - Link: "Open AgentClinic" → `http://localhost:8000/agents`
   - Only render card if there were any diagnosis runs today

   **`insights_dashboard.py`:**
   - Query `get_ailment_frequency(days=7)` and `get_remedy_count()` from `remedies.py`
   - Add a 4th stat box to the existing `.stat-row`: **"Remedies"** (PENDING count)
   - Add a new glass-card section after Topic Velocity: **"🩺 Agent Health Trends"**
     - Bar chart (Chart.js — already imported) showing top ailments by frequency over 7 days
     - Below chart: list each ailment with count + most common therapy prescribed
     - Labelled: "Most Common Issues (7 days)"

### Skill

8. Create `~/.claude/skills/diagnose.md`:
   - Collects symptoms from user
   - POSTs to AgentClinic API
   - Displays treatment steps
   - Fallback if server not running
