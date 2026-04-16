# Phase 1 — Requirements

## Goal
Working FastAPI dev server with a single route confirming the app is running.

## Requirements

1. FastAPI + uvicorn installed and configured
2. `GET /` returns JSON: `{"message": "AgentClinic is open for business"}`
3. Dev server runs via `uvicorn src.main:app --reload`
4. Pydantic available and importable (wiring confirmed for later phases)
5. `python-dotenv` installed and `.env` loading confirmed

## Out of scope
- Templates
- Database
- Any other routes
