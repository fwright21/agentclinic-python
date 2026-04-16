# Phase 6 — Requirements

## Goal
Therapies catalog with ailment → therapy mapping. `/therapies` page listing therapies and which ailments they apply to. Diagnosis chain updated to include therapy recommendation.

---

## Schema

### `therapies` table
```sql
CREATE TABLE therapies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL
);
```

### `ailment_therapies` join table
```sql
CREATE TABLE ailment_therapies (
    ailment_id INTEGER NOT NULL REFERENCES ailments(id),
    therapy_id INTEGER NOT NULL REFERENCES therapies(id),
    PRIMARY KEY (ailment_id, therapy_id)
);
```

---

## Seed therapies + mappings

| Therapy | Description | Applies to ailments |
|---|---|---|
| Context Flush | Clear and summarise session history to free context space | Context Window Overflow, Instruction Drift |
| Memory Summary Injection | Inject a compressed summary of prior context | Context Window Overflow, Prompt Fatigue |
| Instruction Set Reduction | Trim and prioritise instructions, remove redundancy | Prompt Fatigue, Instruction Drift |
| Confidence Recalibration | Adjust refusal threshold to reduce over-cautious behaviour | Hallucination Anxiety |
| Task Decomposition | Split large tasks into smaller subtasks with defined handoffs | Token Budget Exhaustion |
| Compression Prompt | Apply token compression prompt to reduce output size | Token Budget Exhaustion, Repetition Compulsion |
| Novelty Injection | Inject prompt nudging agent toward varied, non-repetitive output | Repetition Compulsion |
| Session Reset | Full context and instruction reset | Instruction Drift, Repetition Compulsion |

---

## `/therapies` page
- Lists all therapies: name, description, linked ailments (as badges)
- Renders inside `base.html`

## Diagnosis chain update
- After matching ailment, chain also returns `therapy_name` (must match a predefined therapy)
- `therapy_name` saved to `diagnosis_runs` table (add `therapy_id` column)
- Therapy name shown in diagnosis result on agent detail page

---

## ⚠️ Prolog flag
When the ailment catalog or symptom-to-ailment rules grow beyond ~10 ailments with overlapping
symptom patterns, consider replacing the LangChain classification step with a Prolog rule engine.
Prolog's unification is better suited to multi-condition diagnostic reasoning than prompt-based
classification. Revisit at Phase 9 or when false classifications become frequent.

---

## Out of scope
- Therapy detail page
- Editing therapy-ailment mappings via UI
