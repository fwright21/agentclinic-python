# Phase 11 — Validation

## AgentClinic API
- [ ] `POST /api/diagnose` returns 200 with ailment, therapy, treatment_steps, status
- [ ] Diagnosis run saved to DB
- [ ] Treatment steps are concrete and session-type specific
- [ ] `GET /api/diagnose/{id}` returns correct status

## AIBriefing integration
- [ ] `remedies` table created in AIBriefing SQLite
- [ ] `add_remedy()` called after successful diagnosis
- [ ] `get_pending_remedies()` returns pending items
- [ ] Evening digest shows "Agent Health Today" card with today's diagnosis runs
- [ ] Insights dashboard stat row shows pending remedy count
- [ ] Insights dashboard shows "Agent Health Trends" bar chart (top ailments, 7 days)
- [ ] Daily briefing HTML shows remedy count
- [ ] `chat.py` "review remedies" walks through pending items
- [ ] Approve → status updates to APPROVED in AIBriefing
- [ ] Approve → AgentClinic diagnosis_run outcome updated

## /diagnose skill
- [ ] `/diagnose` skill available in Claude Code
- [ ] POSTs to AgentClinic API and displays treatment steps
- [ ] Fallback works if server not running

## End-to-end test
- [ ] Invoke `/diagnose` in Claude Code with sample symptoms
- [ ] Remedy appears in AIBriefing pending queue
- [ ] Approve via `chat.py`
- [ ] Treatment steps displayed

## Done when
Full flow works end-to-end: session → diagnose → queue → approve → treatment steps.
