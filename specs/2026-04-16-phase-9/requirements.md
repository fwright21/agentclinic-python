# Phase 9 — Requirements

## Goal
Full visit log on agent detail page. Outcome tracking (RESOLVED / RECURRING / CHRONIC).
CHRONIC auto-flagged after 3+ diagnosis runs with the same ailment. Staff or agent can submit
symptoms via the existing form — same chain, same output.

---

## Schema changes

### Add `outcome` to `diagnosis_runs`
```sql
ALTER TABLE diagnosis_runs ADD COLUMN outcome TEXT DEFAULT 'OPEN';
-- Values: OPEN, RESOLVED, RECURRING, CHRONIC
```

### Add `visit_number` to `diagnosis_runs`
```sql
ALTER TABLE diagnosis_runs ADD COLUMN visit_number INTEGER;
-- Auto-assigned per agent: 1, 2, 3... on insert
```

---

## Visit log on agent detail page

Replace "Last Diagnosis" with a full visit history table:

| Visit # | Date | Ailment | Therapy | Symptoms | Report | Outcome |
|---|---|---|---|---|---|---|

- Most recent first
- Outcome shown as a badge (OPEN=blue, RESOLVED=emerald, RECURRING=amber, CHRONIC=red)
- Staff can update outcome inline via a small form (dropdown: OPEN / RESOLVED / RECURRING)
  — CHRONIC is set automatically, not manually

---

## Outcome logic

### Auto-CHRONIC
After each diagnosis run, check if the same ailment has appeared 3+ times for this agent.
If yes → set all runs with that ailment to CHRONIC.

### Manual outcome update
`POST /agents/{agent_id}/visits/{visit_id}/outcome`
- Form field: `outcome` (OPEN / RESOLVED / RECURRING)
- Staff updates outcome after reviewing the agent
- CHRONIC cannot be manually set or unset

---

## Agent status sync
After any outcome update or new diagnosis:
- If any visit is CHRONIC → agent status = Chronic
- Else if any visit is RECURRING → agent status = Recurring
- Else if all visits RESOLVED → agent status = Resolved
- Else → agent status = Active

---

## Out of scope
- Email / notification on CHRONIC flag
- Visit diff / comparison view
