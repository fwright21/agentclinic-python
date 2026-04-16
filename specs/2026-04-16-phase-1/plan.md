# Phase 1 — Plan

## File structure
```
agentclinic-python/
  src/
    __init__.py
    main.py
  requirements.txt   (update)
  .env               (exists)
```

## Notes
- venv already configured (Python 3.11)
- `requirements.txt` already populated

## Steps

1. Install: `pip install -r requirements.txt` inside venv
2. Create `src/__init__.py` — empty
3. Create `src/main.py`:
   - Import FastAPI, dotenv
   - Load `.env` on startup
   - `GET /` returns JSON: `{"message": "AgentClinic is open for business"}`
4. Run: `uvicorn src.main:app --reload` — confirm 200 at `http://localhost:8000/`
