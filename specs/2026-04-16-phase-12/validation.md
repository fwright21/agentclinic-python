# Phase 12 — Validation

## Log watcher
- [ ] `log_watcher.py` starts without errors
- [ ] Tailing a log file with a test error line triggers a POST to `/api/diagnose`
- [ ] POST body has correct `agent_name`, `session_type: "bot"`, `symptoms`
- [ ] Same error within 30 min does NOT re-POST (dedup working)
- [ ] Different error within 30 min DOES POST

## Pattern matching
- [ ] `telegram.error.Conflict` matched → Pepper agent, correct symptoms
- [ ] Unknown error line → no POST

## Treatment steps
- [ ] `get_treatment_steps(therapy, "bot")` returns bot-specific steps
- [ ] Steps are manual instructions, not auto-executed commands

## AIBriefing integration
- [ ] Bot remedy appears in pending queue after watcher POST
- [ ] `session_type: bot` visible in chat.py review flow
- [ ] Approve → diagnosis_run outcome updated

## End-to-end test
- [ ] Append a fake `telegram.error.Conflict` line to affirmation_error.log
- [ ] Remedy appears in AIBriefing pending queue within 10 seconds
- [ ] Review via chat.py → approve
- [ ] Treatment steps displayed

## HTML updates
- [ ] Evening digest "Agent Health Today" card shows bot runs with "auto-detected" badge
- [ ] Insights dashboard "Agent Health Trends" shows bot issues section with frequency chart
- [ ] Bot runs visually distinct from session runs in both HTMLs

## Done when
Appending an error line to a bot log file results in a remedy in the AIBriefing queue within seconds, approvable via chat.py.
