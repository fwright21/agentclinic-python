# Phase 9 — Plan

## File structure
```
agentclinic-python/
  migrations/
    006_add_visit_fields.sql          (create)
  src/
    visits.py                         (create — outcome logic, CHRONIC detection, status sync)
    database.py                       (update — get_all_visits_for_agent, update_visit_outcome, update_agent_status)
    main.py                           (update — POST /agents/{id}/visits/{visit_id}/outcome, update diagnose route)
    templates/
      agent_detail.html               (update — replace last diagnosis with full visit log)
  static/css/style.css                (update — visit table, outcome badge, outcome form)
```

## Steps

1. Create `migrations/006_add_visit_fields.sql`:
   - ALTER TABLE diagnosis_runs ADD COLUMN outcome TEXT DEFAULT 'OPEN'
   - ALTER TABLE diagnosis_runs ADD COLUMN visit_number INTEGER

2. Run `python migrate.py`

3. Create `src/visits.py`:
   - `assign_visit_number(agent_id)` — count existing runs for agent + 1
   - `check_and_apply_chronic(agent_id, ailment_id)` — if same ailment appears 3+ times, set all matching runs to CHRONIC
   - `sync_agent_status(agent_id)` — update agent status based on visit outcomes (CHRONIC > RECURRING > RESOLVED > Active)

4. Update `src/database.py`:
   - `get_all_visits_for_agent(agent_id)` — all diagnosis runs with ailment + therapy names, ordered by visit_number DESC
   - `update_visit_outcome(visit_id, outcome)` — set outcome on a single run
   - `update_agent_status(agent_id, status)` — update agents.status

5. Update `src/main.py`:
   - Update `POST /agents/{id}/diagnose`:
     - Assign visit_number before saving
     - After saving, call `check_and_apply_chronic` and `sync_agent_status`
   - Add `POST /agents/{agent_id}/visits/{visit_id}/outcome`:
     - Validates outcome is OPEN / RESOLVED / RECURRING (not CHRONIC)
     - Updates outcome
     - Calls `sync_agent_status`
     - Redirects to `/agents/{agent_id}`

6. Update `src/templates/agent_detail.html`:
   - Replace diagnosis result card with full visit history table
   - Columns: Visit # | Date | Ailment | Therapy | Symptoms | Report | Outcome (badge + update form)

7. Update `static/css/style.css`:
   - `.outcome-badge` — same colour mapping as status badges
   - `.outcome-form` — inline dropdown + small submit button
   - `.visit-table` — inherits agents-table styles
