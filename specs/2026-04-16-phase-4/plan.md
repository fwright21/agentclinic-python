# Phase 4 — Plan

## File structure
```
agentclinic-python/
  migrations/
    002_add_agent_fields.sql     (create)
  src/
    database.py                  (update — add get_agent_by_id())
    main.py                      (update — add /agents/{id} route)
    templates/
      agent_detail.html          (create)
      agents.html                (update — name links to /agents/{id})
  static/css/style.css           (update — add tag/pill styles)
```

## Steps

1. Create `migrations/002_add_agent_fields.sql`:
   - ALTER TABLE agents ADD COLUMN reasoning_level TEXT
   - ALTER TABLE agents ADD COLUMN skills TEXT
   - ALTER TABLE agents ADD COLUMN tools TEXT
   - ALTER TABLE agents ADD COLUMN mcps TEXT
   - UPDATE agents SET ... for all 5 seed agents with new field values

2. Run `python migrate.py` to apply migration

3. Update `src/database.py`:
   - Add `get_agent_by_id(id: int)` — returns single agent dict or None

4. Update `src/main.py`:
   - Add `GET /agents/{id}` route
   - Returns 404 if agent not found
   - Renders `agent_detail.html`

5. Create `src/templates/agent_detail.html`:
   - Extends `base.html`
   - Agent name as `<h1>`
   - Detail grid: model type, reasoning level, status badge
   - Presenting complaints section
   - Skills, tools, MCPs as tag pills (split on comma)
   - Back link to `/agents`

6. Update `src/templates/agents.html`:
   - Wrap agent name in `<a href="/agents/{{ agent.id }}">{{ agent.name }}</a>`

7. Update `static/css/style.css`:
   - `.tag` — pill style: small, rounded, border, muted background
   - `.tags` — flex wrap container
