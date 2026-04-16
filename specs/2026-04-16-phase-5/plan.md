# Phase 5 — Plan

## File structure
```
agentclinic-python/
  migrations/
    003_create_ailments.sql         (create)
    004_create_diagnosis_runs.sql   (create)
  src/
    diagnosis.py                    (create — LangChain chain + token callback)
    database.py                     (update — ailment + diagnosis_run queries)
    main.py                         (update — /ailments route, POST /agents/{id}/diagnose)
    templates/
      ailments.html                 (create)
      agent_detail.html             (update — add symptom form + last diagnosis result)
  .env                              (update — add ANTHROPIC_API_KEY)
  requirements.txt                  (update — add langchain-anthropic if missing)
```

## Steps

1. Create `migrations/003_create_ailments.sql`:
   - CREATE TABLE ailments
   - INSERT 6 seed ailments

2. Create `migrations/004_create_diagnosis_runs.sql`:
   - CREATE TABLE diagnosis_runs

3. Run `python migrate.py`

4. Create `src/diagnosis.py`:
   - `TokenTracker(BaseCallbackHandler)` — captures `on_llm_end`, reads usage metadata, stores prompt/completion/total tokens
   - `DiagnosisResult(BaseModel)` — Pydantic model: `ailment_name: str`, `report: str`
   - `run_diagnosis(agent_name: str, symptoms: str) -> dict` — async function:
     - Builds prompt with agent name, symptoms, and list of valid ailment names
     - Runs ChatAnthropic chain with TokenTracker callback
     - Parses structured output
     - Returns `{ailment_name, report, prompt_tokens, completion_tokens, total_tokens}`

5. Update `src/database.py`:
   - `get_all_ailments()` — all ailments
   - `get_ailment_by_name(name: str)` — lookup by name
   - `save_diagnosis_run(agent_id, ailment_id, symptoms, report, prompt_tokens, completion_tokens, total_tokens)`
   - `get_last_diagnosis_for_agent(agent_id)` — most recent diagnosis run for agent

6. Update `src/main.py`:
   - `GET /ailments` → renders `ailments.html`
   - `POST /agents/{id}/diagnose`:
     - Reads form field `symptoms`
     - Calls `run_diagnosis(agent.name, symptoms)`
     - Looks up ailment_id from ailment_name
     - Saves to diagnosis_runs
     - Redirects to `/agents/{id}`

7. Create `src/templates/ailments.html`:
   - Extends `base.html`
   - Table: Name | Description | Recommended Treatment

8. Update `src/templates/agent_detail.html`:
   - Add symptom submission form (textarea + submit button)
   - If last diagnosis exists: show report, ailment, token usage

9. Update `static/css/style.css`:
   - Form styles: textarea, submit button
   - Diagnosis result card style

10. Add to `.env`:
    - `ANTHROPIC_API_KEY=your_key_here`

## ⚠️ Note for executor
Phase 9 (Claude Code / Sonnet) — do not implement follow-up logic or outcome tracking here.
Keep diagnosis chain simple: one submission → one result.
