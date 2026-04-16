# Phase 1 — Validation

## Checks

- [x] `pip install -r requirements.txt` completes with no errors
- [x] `uvicorn src.main:app --reload` starts without errors
- [x] `GET http://localhost:8000/` returns 200
- [x] Response body contains `"AgentClinic is open for business"`
- [x] `from pydantic import BaseModel` imports without error
- [x] `.env` is loaded (confirm with a test env var print or dotenv check)

## Done when
All boxes checked and server stays running without errors.
