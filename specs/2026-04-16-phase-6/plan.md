# Phase 6 — Plan

## File structure
```
agentclinic-python/
  migrations/
    005_create_therapies.sql         (create)
  src/
    diagnosis.py                     (update — add therapy_name to output)
    database.py                      (update — therapy queries, update diagnosis_runs)
    main.py                          (update — /therapies route)
    templates/
      therapies.html                 (create)
      agent_detail.html              (update — show therapy in diagnosis result)
```

## Steps

1. Create `migrations/005_create_therapies.sql`:
   - CREATE TABLE therapies
   - CREATE TABLE ailment_therapies
   - ALTER TABLE diagnosis_runs ADD COLUMN therapy_id INTEGER REFERENCES therapies(id)
   - INSERT 8 seed therapies
   - INSERT ailment_therapies mappings

2. Run `python migrate.py`

3. Update `src/database.py`:
   - `get_all_therapies()` — all therapies with linked ailment names
   - `get_therapy_by_name(name: str)` — lookup by name
   - `get_therapies_for_ailment(ailment_id: int)` — therapies for a given ailment

4. Update `src/diagnosis.py`:
   - Add `therapy_name: str` to `DiagnosisResult` Pydantic model
   - Update prompt to include list of valid therapy names
   - Return `therapy_name` in result dict

5. Update `src/main.py`:
   - `GET /therapies` → renders `therapies.html`
   - Update `POST /agents/{id}/diagnose` to save `therapy_id`

6. Create `src/templates/therapies.html`:
   - Extends `base.html`
   - Table: Therapy name | Description | Linked ailments (as badges)

7. Update `src/templates/agent_detail.html`:
   - Show therapy name in diagnosis result card
