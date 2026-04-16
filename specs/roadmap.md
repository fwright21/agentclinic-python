# Roadmap

Phases are intentionally small — each one is a shippable slice of work,
independently reviewable and testable.

Spec-first: every phase gets a `specs/YYYY-MM-DD-<name>/` directory containing
`requirements.md`, `plan.md`, and `validation.md` before any code is written.

---

## Phase 1 — Hello FastAPI ✅
- [x] Install FastAPI + uvicorn, configure dev server
- [x] Single `/` route returning "AgentClinic is open for business"
- [x] Confirm Python types and Pydantic wiring work end-to-end

## Phase 2 — Base Layout
- [ ] Jinja2 templates: shared layout (header, nav, main, footer)
- [ ] Plain CSS (reset, custom properties, typography)
- [ ] All routes render inside the shared layout

## Phase 3 — Agent List
- [ ] SQLite via `aiosqlite` + first migration (`agents` table)
- [ ] `migrate.py` script for running `.sql` migration files
- [ ] Seed a handful of fictional agents
- [ ] `/agents` page listing all agents

## Phase 4 — Agent Detail
- [ ] `/agents/{id}` page showing a single agent's profile
- [ ] Fields: name, model type, current status, presenting complaints
- [ ] Link from agents list

## Phase 5 — Ailments Catalog + Diagnosis Engine (AI layer starts here)
- [ ] `ailments` table + seed data (e.g. "context-window overflow", "prompt fatigue", "hallucination anxiety")
- [ ] `/ailments` list page
- [ ] Link agents to one or more ailments
- [ ] LangChain diagnosis chain: reads agent symptoms → matches ailment → returns structured result
- [ ] Custom `BaseCallbackHandler` for token tracking per diagnosis run
- [ ] Plain-English report output: "Issue: X. Treatment: Y. Logged: visit #N."

## Phase 6 — Therapies Catalog
- [x] `therapies` table + seed data
- [x] `/therapies` list page
- [x] Map ailments → recommended therapies (join table)
- [x] Diagnosis chain updated to include treatment prescription
- [ ] ⚠️ Prolog flag: if ailment catalog grows beyond ~10 ailments with overlapping symptom patterns, consider replacing LangChain classification with a Prolog rule engine (see Phase 6 spec)

## Phase 7 — Visit Log (replaces Appointment Booking)
- [ ] Merged into Phase 9 — visits are created automatically when a diagnosis runs
- [ ] No manual appointment booking — agents "visit" when they submit symptoms

## Phase 8 — Staff Dashboard
- [x] `/dashboard` with four views:
  - Summary counts: total agents, open appointments, active ailments
  - Agent health table: current ailment + token usage flagged if high
  - Ailment trends: most common ailments, treatment effectiveness rates
  - Appointment queue: upcoming appointments with status

## Phase 9 — Visit Log + Outcomes
- [x] `outcome` + `visit_number` columns added to `diagnosis_runs`
- [x] Full visit history on agent detail page
- [x] Staff or agent submits symptoms via existing form — same chain
- [x] Manual outcome update: OPEN / RESOLVED / RECURRING
- [x] Auto-CHRONIC: 3+ runs with same ailment → all flagged CHRONIC
- [x] Agent status synced after each diagnosis or outcome update

## Phase 10 — Polish + Tests
- [ ] Error pages (404, 500)
- [ ] Input sanitisation on all forms
- [ ] Basic logging middleware
- [ ] pytest + httpx test suite covering all routes
- [ ] Async test configuration (pytest-asyncio)

---

Later phases (not yet planned): auth, deployment, reporting exports, API endpoint
for agents to submit symptoms programmatically.
