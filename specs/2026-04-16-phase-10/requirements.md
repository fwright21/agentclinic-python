# Phase 10 — Requirements

## Goal
Error pages, input sanitisation, basic logging, pytest test suite.

---

## Error pages
- `404.html` — "Agent not found" style, consistent with base layout
- `500.html` — "Something went wrong", consistent with base layout
- FastAPI exception handlers registered for 404 and 500

## Input sanitisation
- All form inputs: strip whitespace, reject if empty after strip
- Symptoms field: min 10 chars after strip — return form with error message if too short
- No HTML injection — FastAPI + Jinja2 auto-escapes by default, confirm this is active

## Logging middleware
- Log every request: method, path, status code, response time
- Use Python stdlib `logging` — no third-party dependency
- Log to stdout (uvicorn already captures this)

## Test suite (pytest + httpx)

### Routes to cover
| Route | Test |
|---|---|
| `GET /` | 200, contains "AgentClinic" |
| `GET /agents` | 200, contains agent names |
| `GET /agents/1` | 200, contains "Pepper-Bot" |
| `GET /agents/999` | 404 |
| `GET /ailments` | 200, contains ailment names |
| `GET /therapies` | 200 |
| `GET /dashboard` | 200 |
| `POST /agents/1/diagnose` | 200 redirect (mock chain — do not call Groq in tests) |
| `POST /agents/1/diagnose` empty symptoms | 422 or redirect with error |

### Setup
- `pytest-asyncio` already in requirements
- `httpx` already in requirements
- Mock `run_diagnosis` in route tests — do not make real Groq calls
- `conftest.py` with async test client fixture

---

## Out of scope
- Auth
- Full integration tests hitting Groq
