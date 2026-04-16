# Phase 8 — Plan

## File structure
```
agentclinic-python/
  src/
    dashboard.py                (create — all dashboard queries)
    main.py                     (update — /dashboard route)
    templates/
      dashboard.html            (create)
  static/css/style.css          (update — dashboard layout, bar chart, token flag)
```

## Steps

1. Create `src/dashboard.py`:
   - `HIGH_TOKEN_THRESHOLD = 1000`
   - `get_summary_counts()` — total agents, total diagnosis runs, active ailments count, flagged agents count
   - `get_agent_health_table()` — agents with most recent ailment, last diagnosis date, token flag
   - `get_ailment_frequency()` — ailments ranked by diagnosis run count, with max count for bar scaling
   - `get_recent_diagnosis_runs(limit=10)` — most recent runs with agent name, ailment, therapy, tokens, date

2. Update `src/main.py`:
   - `GET /dashboard` → calls all 4 dashboard queries, renders `dashboard.html`

3. Create `src/templates/dashboard.html`:
   - Extends `base.html`
   - Section 1: 4 summary count cards in a row
   - Section 2: agent health table
   - Section 3: ailment frequency list with CSS bars
   - Section 4: recent diagnosis runs table

4. Update `static/css/style.css`:
   - `.summary-cards` — grid, 4 columns
   - `.summary-card` — surface, border, padding
   - `.bar-track` / `.bar-fill` — CSS-only frequency bar
   - `.token-flag` — amber warning colour
