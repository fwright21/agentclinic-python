# Phase 5 — Requirements

## Goal
Ailments catalog, LangChain diagnosis engine, symptom submission form on agent detail page. Token usage stored in DB per diagnosis run.

---

## Ailments catalog

### Schema
```sql
CREATE TABLE ailments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    recommended_treatment TEXT NOT NULL
);
```

### Seed ailments

| Name | Description | Recommended Treatment |
|---|---|---|
| Context Window Overflow | Agent loses earlier information mid-session due to context limit | Apply context flush and summary injection |
| Prompt Fatigue | Degraded output after long or repetitive instruction sets | Reduce instruction set, add memory summary |
| Hallucination Anxiety | Over-cautious refusals due to over-correction for hallucination | Recalibrate confidence threshold, loosen safety constraints |
| Token Budget Exhaustion | Agent hits token limits mid-task and truncates output | Split task into subtasks, apply compression prompt |
| Instruction Drift | Gradual deviation from original instructions over long session | Re-inject original instructions, reset session context |
| Repetition Compulsion | Agent loops or repeats same output across turns | Flush recent history, inject novelty prompt |

---

## Diagnosis runs

### Schema
```sql
CREATE TABLE diagnosis_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL REFERENCES agents(id),
    ailment_id INTEGER REFERENCES ailments(id),
    submitted_symptoms TEXT NOT NULL,
    report TEXT NOT NULL,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## LangChain diagnosis chain

- Model: Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
- Input: agent name + submitted symptoms
- Output (structured via Pydantic OutputParser):
  - `ailment_name` — must match one of the 6 predefined ailment names exactly
  - `report` — plain-English treatment report: "Issue: X. Treatment: Y. Logged: visit #N."
- Custom `BaseCallbackHandler` captures prompt + completion + total tokens from Anthropic response metadata
- Chain lives in `src/diagnosis.py`

---

## Symptom submission

- Form on `/agents/{id}` detail page
- Textarea: "Describe the symptoms"
- Submit button: "Run Diagnosis"
- `POST /agents/{id}/diagnose`
  - Runs diagnosis chain
  - Saves result to `diagnosis_runs` table
  - Redirects back to `/agents/{id}` with diagnosis result shown

---

## `/ailments` page

- Lists all ailments: name, description, recommended treatment
- Renders inside `base.html`

---

## Out of scope
- Follow-up / outcome tracking (Phase 9)
- Therapies catalog (Phase 6)
- Multiple diagnosis runs shown on agent detail (Phase 9)
