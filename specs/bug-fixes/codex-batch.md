# Bug Fix Batch — Codex
**Model:** Codex CLI GPT-5.3 `medium`  
**Files touched:** `src/api.py`, `src/diagnosis.py`, `src/database.py`  
**These fixes require cross-file integration and async wiring.**

---

## B3 — Replace `infer_ailment()` with `run_diagnosis()` (LangChain chain)

Files: `src/api.py` (change), `src/diagnosis.py` (read-only reference), `src/database.py` (read-only reference)

The API's `POST /api/diagnose` uses a keyword matcher (`infer_ailment()`) instead of the
existing LangChain/Groq diagnosis chain (`run_diagnosis()` in `src/diagnosis.py`).
Same symptoms submitted via the API vs the web form produce different diagnoses.

**What `run_diagnosis()` returns:**
```python
{
    "ailment_name": str,
    "therapy_name": str,
    "report": str,
    "prompt_tokens": int,
    "completion_tokens": int,
    "total_tokens": int,
}
```

**Fix:**
1. Remove `infer_ailment()` function from `src/api.py`
2. Import `run_diagnosis` from `src.diagnosis`
3. In `POST /api/diagnose`, replace:
   ```python
   ailment_name, therapy_name = await infer_ailment(req.symptoms)
   ```
   With:
   ```python
   result = await run_diagnosis(req.agent_name, req.symptoms)
   ailment_name = result["ailment_name"]
   therapy_name = result["therapy_name"]
   ```
4. Store `result["report"]` in the diagnosis_runs INSERT (see B4 — do together)

---

## B4 — Replace raw INSERT with `save_diagnosis_run()`

Files: `src/api.py` (change), `src/database.py` (read-only reference), `src/visits.py` (read-only reference)

The `POST /api/diagnose` handler does a bare INSERT into `diagnosis_runs` that omits:
`ailment_id`, `therapy_id`, `visit_number`, `prompt_tokens`, `completion_tokens`, `total_tokens`, `outcome`.
API-submitted diagnoses are invisible in the web UI, visit history, and dashboard.

**Fix:**
1. Import `save_diagnosis_run` from `src.database`
2. Import `assign_visit_number`, `check_and_apply_chronic`, `sync_agent_status` from `src.visits`
3. Import `get_ailment_by_name`, `get_therapy_by_name` from `src.database`
4. Replace the raw INSERT with:
   ```python
   ailment = await get_ailment_by_name(ailment_name)
   ailment_id = ailment["id"] if ailment else None

   therapy = await get_therapy_by_name(therapy_name)
   therapy_id = therapy["id"] if therapy else None

   visit_number = await assign_visit_number(agent_id)

   report = result["report"].replace("visit #N", f"visit #{visit_number}")

   diagnosis_id = await save_diagnosis_run(
       agent_id=agent_id,
       ailment_id=ailment_id,
       symptoms=req.symptoms,
       report=report,
       prompt_tokens=result["prompt_tokens"],
       completion_tokens=result["completion_tokens"],
       total_tokens=result["total_tokens"],
       therapy_id=therapy_id,
       visit_number=visit_number,
       outcome="OPEN",
   )

   if ailment_id:
       await check_and_apply_chronic(agent_id, ailment_id)
   await sync_agent_status(agent_id)
   ```
5. Remove the now-redundant `get_db()` / raw aiosqlite connection from the POST handler
   (the imported functions handle their own connections)

**Note:** B3 and B4 must be done together — they touch the same call site in `POST /api/diagnose`.
