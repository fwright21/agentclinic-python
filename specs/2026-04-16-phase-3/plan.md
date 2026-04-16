# Phase 3 — Plan

## File structure
```
agentclinic-python/
  migrations/
    001_create_agents.sql    (create)
  src/
    database.py              (create)
    main.py                  (update — add /agents route)
    templates/
      agents.html            (create)
  migrate.py                 (create)
  agentclinic.db             (created on first migrate run)
```

## Steps

1. Create `migrations/001_create_agents.sql`:
   - CREATE TABLE IF NOT EXISTS agents
   - Fields: id, name, model_type, status, presenting_complaints, created_at
   - INSERT 5 seed agents

2. Create `migrate.py`:
   - Connects to `agentclinic.db` via `aiosqlite`
   - Reads and runs all `.sql` files in `migrations/` in filename order
   - Idempotent — safe to run multiple times (uses IF NOT EXISTS)

3. Create `src/database.py`:
   - Async function `get_db()` — returns aiosqlite connection to `agentclinic.db`
   - Async function `get_all_agents()` — returns all rows from agents table

4. Update `src/main.py`:
   - Add `GET /agents` route
   - Calls `get_all_agents()`, passes results to `TemplateResponse`

5. Create `src/templates/agents.html`:
   - Extends `base.html`
   - `<h1>Agents</h1>`
   - Table: Name | Model Type | Status | Presenting Complaints
   - Status cell uses CSS class matching status value (e.g. `class="status-active"`)

6. Add status badge styles to `static/css/style.css`:
   - `.status-active`, `.status-resolved`, `.status-recurring`, `.status-chronic`, `.status-unknown`
   - Each uses the corresponding `--status-*` colour token as background or text colour

7. Run: `python migrate.py` to create DB and seed data
