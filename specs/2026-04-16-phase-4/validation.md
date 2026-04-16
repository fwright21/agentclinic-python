# Phase 4 — Validation

## Checks

- [ ] `python migrate.py` runs without errors
- [ ] All 5 agents have reasoning_level, skills, tools populated in DB
- [ ] `GET /agents` — agent names are clickable links
- [ ] `GET /agents/1` returns 200 and renders detail page
- [ ] `GET /agents/999` returns 404
- [ ] Detail page shows: name, model type, reasoning level, status badge, presenting complaints
- [ ] Skills displayed as pills
- [ ] Tools displayed as pills
- [ ] MCPs displayed as pills (or "—" if none)
- [ ] Back link to `/agents` present
- [ ] Page renders inside base.html layout

## Done when
All boxes checked and detail page renders correctly at `http://localhost:8000/agents/1`.
