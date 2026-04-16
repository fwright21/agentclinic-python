# Phase 5 — Validation

## Checks

### Migrations
- [ ] `python migrate.py` runs without errors
- [ ] `ailments` table exists with 6 seed ailments
- [ ] `diagnosis_runs` table exists

### Ailments page
- [ ] `GET /ailments` returns 200
- [ ] All 6 ailments visible: name, description, recommended treatment

### Diagnosis chain
- [ ] `ANTHROPIC_API_KEY` set in `.env`
- [ ] Symptom form visible on agent detail page
- [ ] Submitting symptoms runs the chain without errors
- [ ] Diagnosis result appears on agent detail page after redirect
- [ ] Report follows format: "Issue: X. Treatment: Y. Logged: visit #N."
- [ ] Ailment name in result matches one of the 6 predefined ailments
- [ ] Token usage (prompt, completion, total) saved in `diagnosis_runs` table
- [ ] Token usage visible on agent detail page

## Done when
All boxes checked. Submit symptoms for at least 2 agents and confirm results are saved and displayed.
