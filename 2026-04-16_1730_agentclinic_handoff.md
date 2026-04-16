# Session Handoff — 2026-04-16

## Project
AgentClinic — AI agent diagnostic clinic (Python/FastAPI/LangChain)

## Goal of this session
Complete Phase 6 (Therapies) and Phase 8 (Dashboard)

## Status: IN PROGRESS

## What's done
- Phase 6 (Therapies): Migration, database queries, /therapies route, template,therapy in diagnosis
- Phase 8 (Dashboard): Created, fixed SQL queries (ailment_name/therapy_name join issues)

## What's in progress
- Dashboard at /dashboard returning 500 Internal Error on user's browser
- Fixed SQL joins (diagnosis_runs has ailment_id, not ailment_name — need JOIN)
- Need user to restart uvicorn to pick up code fixes

## Next step
User needs to restart uvicorn server to load fixed dashboard.py

## Key decisions
- Used JOINs to lookup ailment_name/therapy_name instead of direct column refs

## Files touched this session
- `src/database.py` — added therapy_id param to save_diagnosis_run
- `src/main.py` — added /dashboard route,therapy_id lookup
- `src/dashboard.py` — created with fixed SQL joins
- `src/templates/dashboard.html` — created
- `src/templates/therapies.html` — created
- `static/css/style.css` — added dashboard styles

## Environment
- Python: 3.11
- venv: project venv
- Deps: fastapi, uvicorn, aiosqlite, langchain-groq, groq, jinja2

## Open questions / blockers
- User seeing internal error on dashboard — fixed, needs server restart

## How to resume
1. Kill any running uvicorn: `lsof -ti :8000 | xargs kill`
2. Restart: `uvicorn src.main:app`
3. Visit http://localhost:8000/dashboard