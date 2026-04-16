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
- [ ] `therapies` table + seed data
- [ ] `/therapies` list page
- [ ] Map ailments → recommended therapies
- [ ] Diagnosis chain updated to include treatment prescription

## ~~Phase 7 — Appointment Booking~~ *(dropped — not needed)*

## Phase 8 — Staff Dashboard
- [ ] `/dashboard` with four views:
  - Summary counts: total agents, active ailments, diagnosis runs this week
  - Agent health table: current ailment + token usage flagged if high
  - Ailment trends: most common ailments, treatment effectiveness rates
  - Recent diagnosis runs: agent, ailment, therapy, outcome

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

## Phase 11 — Self-Healing: API, Treatment Executor, AIBriefing Integration
- [x] `POST /api/diagnose` — JSON endpoint for sessions to submit symptoms
- [x] `GET /api/diagnose/{id}` — returns diagnosis run status + treatment steps
- [x] Treatment step generator — maps therapy × session type to concrete steps
- [x] AIBriefing `remedies` table — pending approvals queue
- [x] AIBriefing `remedies.py` — `add_remedy`, `get_pending_remedies`, `update_remedy_status`
- [x] `chat.py` "review remedies" command — approve/reject flow
- [x] Evening digest: pending remedy count in Telegram notification
- [x] `/diagnose` skill for Claude Code / Codex sessions
- [x] End-to-end: session → diagnose → queue → approve → treatment steps

## Phase 12 — Real-Agent Self-Healing: Log Watcher + Human-in-the-Loop
- [ ] `log_patterns.py` — error pattern registry (regex → agent/symptoms)
- [ ] `log_watcher.py` — tails Pepper + AIBriefing error logs, POSTs on match
- [ ] 30-minute dedup window (no repeat POSTs for same error)
- [ ] `treatment.py` updated with `"bot"` session-type steps (manual instructions)
- [ ] Evening digest: bot health subsection with "auto-detected" badge
- [ ] Insights dashboard: bot issues frequency chart (7 days, by bot)
- [ ] End-to-end: error in log → remedy in AIBriefing queue → approve via chat.py

---

Later phases (not yet planned): auth, deployment, reporting exports, automated symptom detection, Telegram push on new remedy.
