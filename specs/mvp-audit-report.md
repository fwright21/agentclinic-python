# AgentClinic MVP Audit Report
**Date:** 2026-04-16  
**Phases covered:** 1–12  
**Audited by:** Claude Sonnet

---

## Phase Status Summary

| Phase | Title | Status |
|---|---|---|
| 1 | Hello FastAPI | ✅ Complete |
| 2 | Base Layout | ✅ Complete |
| 3 | Agent List | ✅ Complete |
| 4 | Agent Detail | ✅ Complete |
| 5 | Ailments Catalog + Diagnosis Engine | ✅ Complete |
| 6 | Therapies Catalog | ✅ Complete |
| 7 | Appointment Booking | ~~Dropped~~ |
| 8 | Staff Dashboard | ✅ Complete |
| 9 | Visit Log + Outcomes | ✅ Complete |
| 10 | Polish + Tests | ✅ Complete |
| 11 | Self-Healing API + AIBriefing Integration | ✅ Complete |
| 12 | Real-Agent Self-Healing: Log Watcher | ✅ Complete |

---

## Bugs Found

### 🔴 Critical

**B1 — `log_watcher.py`: `f.tell()` called after file close**  
File: `log_watcher.py` line 65  
`new_pos = f.tell()` is outside the `with open()` block. File handle is closed at that point.  
Raises `ValueError: I/O operation on closed file` on every new log match — watcher is non-functional.  
Fix: move `new_pos = f.tell()` inside the `with` block.

**B2 — `api.py`: `infer_ailment()` returns ailment names not in the DB**  
File: `src/api.py`  
Keyword matcher returns: "Memory Drift", "Repetition Loop", "Predictability Fatigue", "Confidence Deficit", "Complexity Overload", "Output Bloat" — none exist in the `ailments` table.  
DB ailments: Context Window Overflow, Hallucination Anxiety, Instruction Drift, Prompt Fatigue, Repetition Compulsion, Token Budget Exhaustion.  
Fix: align `infer_ailment()` names with DB, or replace with `run_diagnosis()`.

**B3 — `api.py`: uses keyword matching instead of LangChain diagnosis chain**  
File: `src/api.py`  
Web UI uses `run_diagnosis()` (Groq/LangChain). API has its own keyword matcher. Same symptoms produce different diagnoses depending on submission path. Spec says "runs the existing diagnosis chain."  
Fix: replace `infer_ailment()` with `await run_diagnosis()` from `src/diagnosis.py`.

**B4 — `api.py`: `diagnosis_runs` INSERT missing columns**  
File: `src/api.py`  
POST /api/diagnose only saves `agent_id`, `submitted_symptoms`, `report`. Leaves `ailment_id`, `therapy_id`, `visit_number`, `prompt_tokens`, `completion_tokens`, `total_tokens` all NULL.  
API-submitted diagnoses are invisible in the web UI, visit history, and dashboard.  
Fix: use `save_diagnosis_run()` from `src/database.py` with full column set.

**B5 — `PATCH /api/diagnose/{id}/approve` updates wrong DB**  
File: `src/api.py`  
The PATCH endpoint runs `UPDATE remedies ... WHERE diagnosis_id = ?` against `agentclinic.db`. Remedies live in `aibriefing.db`. This UPDATE either hits a non-existent table or does nothing useful.  
Fix: remove the remedies UPDATE from the PATCH endpoint — `chat.py` already calls `update_remedy_status()` directly on `aibriefing.db` before calling PATCH. PATCH only needs to update `diagnosis_runs.outcome`.

---

### 🟡 Structural Issues

**S1 — `api.py`: `add_remedy` errors silently swallowed**  
File: `src/api.py`  
`except Exception as e: pass` — if AIBriefing import fails or `add_remedy()` errors, the diagnosis returns 200 with nothing queued. Failures are invisible.  
Fix: at minimum `logger.warning(f"add_remedy failed: {e}")`.

**S2 — `diagnosis.py`: `"visit #N"` never substituted in report**  
File: `src/diagnosis.py`  
The LLM prompt asks for `"Logged: visit #N."` — the LLM outputs this literally since visit number is never passed in.  
Fix: post-process the report string to substitute actual visit number, or pass it into the prompt.

---

## Risk Areas (not bugs, worth watching)

- **`infer_ailment` coverage** — keyword matching has gaps. Symptoms not matching any keyword fall back to "Unknown Condition" / "Session Reset" which is not useful.
- **`log_watcher.py` runs in foreground only** — no process management or restart-on-crash. Needs cron keepalive for production use (documented in spec).
- **AIBriefing path hardcoded** — `sys.path.insert(0, "~/Documents/AIBriefing")` in `api.py`. Breaks if AIBriefing moves or on any other machine.

