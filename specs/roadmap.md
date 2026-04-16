# Roadmap

Phases are intentionally small — each one is a shippable slice of work,
independently reviewable and testable.

Spec-first: every phase gets a `specs/YYYY-MM-DD-<name>/` directory containing
`requirements.md`, `plan.md`, and `validation.md` before any code is written.

---

## Phase 1 — Hello FastAPI
- [ ] Install FastAPI + uvicorn, configure dev server
- [ ] Single `/` route returning "AgentClinic is open for business"
- [ ] Confirm Python types and Pydantic wiring work end-to-end

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
- [ ] `therapies` table + seed data
- [ ] `/therapies` list page
- [ ] Map ailments → recommended therapies
- [ ] Diagnosis chain updated to include treatment prescription

## Phase 7 — Appointment Booking
- [ ] `appointments` table (agent_id, ailment_id, datetime, status)
- [ ] Form to book an appointment from an agent's detail page
- [ ] Validation + confirmation page
- [ ] Appointment status: PENDING / ACTIVE / CLOSED

## Phase 8 — Staff Dashboard
- [ ] `/dashboard` with four views:
  - Summary counts: total agents, open appointments, active ailments
  - Agent health table: current ailment + token usage flagged if high
  - Ailment trends: most common ailments, treatment effectiveness rates
  - Appointment queue: upcoming appointments with status

## Phase 9 — Follow-up + Visit States
- [ ] `visits` table linking agents to diagnosis runs + outcomes
- [ ] Agent re-submission detects prior visit → triggers follow-up flow
- [ ] Diagnosis chain evaluates outcome: RESOLVED / RECURRING / CHRONIC
- [ ] CHRONIC (3+ recurrences of same ailment) flagged for staff attention

## Phase 10 — Polish + Tests
- [ ] Error pages (404, 500)
- [ ] Input sanitisation on all forms
- [ ] Basic logging middleware
- [ ] pytest + httpx test suite covering all routes
- [ ] Async test configuration (pytest-asyncio)

---

Later phases (not yet planned): auth, deployment, reporting exports, API endpoint
for agents to submit symptoms programmatically.
