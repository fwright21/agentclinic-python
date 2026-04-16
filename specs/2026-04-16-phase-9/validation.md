# Phase 9 — Validation

## Checks

### Migrations
- [ ] `python migrate.py` runs without errors
- [ ] `diagnosis_runs` has `outcome` and `visit_number` columns

### Visit log
- [ ] Agent detail page shows full visit history table
- [ ] Visit numbers assigned correctly (1, 2, 3...)
- [ ] Most recent visit first
- [ ] Ailment, therapy, symptoms, report all visible per visit
- [ ] Outcome badge shown per visit

### Outcome update
- [ ] Staff can update outcome via dropdown (OPEN / RESOLVED / RECURRING)
- [ ] CHRONIC cannot be manually set
- [ ] Agent status updates after outcome change

### CHRONIC detection
- [ ] Submit same ailment 3 times for one agent
- [ ] All 3 runs show CHRONIC outcome
- [ ] Agent status updates to Chronic automatically

### Status sync
- [ ] Agent with all RESOLVED visits → status = Resolved
- [ ] Agent with any RECURRING → status = Recurring
- [ ] Agent with any CHRONIC → status = Chronic

## Done when
All boxes checked. Run 3 diagnoses for one agent with the same ailment and confirm CHRONIC is auto-applied.
