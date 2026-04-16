# Bug Fix Batch — Haiku
**Model:** Claude Haiku 4.5  
**Files touched:** `log_watcher.py`, `src/api.py`, `src/main.py`  
**All fixes are single-file, no integration decisions required.**

---

## B1 — `log_watcher.py`: `f.tell()` called after file close

File: `log_watcher.py`

The `with open(log_path, "r") as f:` block closes the file at line ~63.  
`new_pos = f.tell()` on line 65 is outside the block — file is already closed.  
Raises `ValueError: I/O operation on closed file` every time new lines are found.

**Fix:** Move `new_pos = f.tell()` inside the `with` block, before the block closes.

```python
# Current (broken):
with open(log_path, "r") as f:
    f.seek(last_pos)
    new_lines = f.readlines()

if not new_lines:
    return

new_pos = f.tell()   # ← WRONG: file is closed here

# Fixed:
with open(log_path, "r") as f:
    f.seek(last_pos)
    new_lines = f.readlines()
    new_pos = f.tell()   # ← inside block, file still open

if not new_lines:
    return
```

---

## B5 — `src/api.py`: `PATCH /approve` updates remedies in wrong DB

File: `src/api.py`, function `approve_diagnosis()`

The PATCH endpoint runs `UPDATE remedies SET status = 'APPROVED' WHERE diagnosis_id = ?`
against `agentclinic.db`. Remedies live in `aibriefing.db`. `chat.py` already calls
`update_remedy_status()` on `aibriefing.db` before calling this endpoint.
The UPDATE in `agentclinic.db` hits the wrong place.

**Fix:** Remove the remedies UPDATE entirely from the PATCH endpoint.
Keep only the `diagnosis_runs` outcome update.

```python
# Remove these lines from approve_diagnosis():
await conn.execute(
    "UPDATE remedies SET status = 'APPROVED' WHERE diagnosis_id = ?",
    (diagnosis_id,),
)
await conn.commit()
```

---

## S1 — `src/api.py`: silent `add_remedy` error swallowing

File: `src/api.py`, POST `/diagnose` handler

`except Exception as e: pass` means if AIBriefing isn't reachable or `add_remedy()` fails,
the error is completely invisible. Diagnosis returns 200 but nothing is queued.

**Fix:** Replace `pass` with a `logger.warning`. Add logger at top of file if not present.

```python
import logging
logger = logging.getLogger("agentclinic.api")

# In the except block:
except Exception as e:
    logger.warning(f"add_remedy failed — remedy not queued in AIBriefing: {e}")
```

---

## S2 — `src/main.py`: visit number not substituted in report

File: `src/main.py`, `diagnose_agent()` route handler

`run_diagnosis()` returns a `report` string where the LLM outputs "visit #N" literally
since the visit number is never passed in. The actual `visit_number` is available
in `diagnose_agent()` after `assign_visit_number()` is called.

**Fix:** After calling `run_diagnosis()`, replace "visit #N" in the report with the actual visit number.

```python
visit_number = await assign_visit_number(agent_id)
result = await run_diagnosis(agent["name"], symptoms)

# Add this line:
result["report"] = result["report"].replace("visit #N", f"visit #{visit_number}")
```

---

## B2 — `src/api.py`: `infer_ailment()` returns names not in DB

File: `src/api.py`

`infer_ailment()` returns ailment names that don't exist in the `ailments` table.
DB ailments are: Context Window Overflow, Hallucination Anxiety, Instruction Drift,
Prompt Fatigue, Repetition Compulsion, Token Budget Exhaustion.

**Fix:** Remap each return value to a valid DB ailment name. Therapy names must also
match valid therapies: Context Flush, Memory Summary Injection, Instruction Set Reduction,
Confidence Recalibration, Task Decomposition, Compression Prompt, Novelty Injection, Session Reset.

```python
async def infer_ailment(symptoms: str) -> tuple[str, str]:
    symptoms_lower = symptoms.lower()
    if "context" in symptoms_lower or "heavy" in symptoms_lower or "recap" in symptoms_lower:
        return ("Context Window Overflow", "Context Flush")
    if "forget" in symptoms_lower or "memory" in symptoms_lower:
        return ("Instruction Drift", "Memory Summary Injection")
    if "stuck" in symptoms_lower or "repeating" in symptoms_lower or "loop" in symptoms_lower:
        return ("Repetition Compulsion", "Session Reset")
    if "creative" in symptoms_lower or "boring" in symptoms_lower or "predictable" in symptoms_lower:
        return ("Prompt Fatigue", "Novelty Injection")
    if "unsure" in symptoms_lower or "hesitat" in symptoms_lower or "cautious" in symptoms_lower:
        return ("Hallucination Anxiety", "Confidence Recalibration")
    if "overwhelm" in symptoms_lower or "complex" in symptoms_lower:
        return ("Token Budget Exhaustion", "Task Decomposition")
    if "verbose" in symptoms_lower or "long" in symptoms_lower or "wordy" in symptoms_lower:
        return ("Prompt Fatigue", "Compression Prompt")
    return ("Instruction Drift", "Session Reset")
```
