# Phase 3 — Validation

## Checks

- [ ] `python migrate.py` runs without errors
- [ ] `agentclinic.db` created in project root
- [ ] `agents` table exists with correct schema
- [ ] 5 seed agents present in database
- [ ] `GET /agents` returns 200
- [ ] Page renders inside base.html layout (header, nav, footer visible)
- [ ] All 5 agents visible in the table
- [ ] Each agent shows: name, model type, status, presenting complaints
- [ ] Status badges display with correct colours (Active=blue, Resolved=emerald, Recurring=amber, Chronic=red, Unknown=slate)

## Done when
All boxes checked and agents list renders correctly in browser at `http://localhost:8000/agents`.
