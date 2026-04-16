# Phase 8 — Validation

## Checks

### Summary counts
- [ ] `GET /dashboard` returns 200
- [ ] Total agents count correct
- [ ] Total diagnosis runs count correct
- [ ] Active ailments count correct
- [ ] Flagged agents count correct (or 0 if no runs yet)

### Agent health table
- [ ] All agents listed
- [ ] Status badges correct
- [ ] Most recent ailment shown (or — if no runs)
- [ ] Token flag ⚠️ appears if any run > 1000 tokens

### Ailment frequency
- [ ] All ailments listed in descending order by count
- [ ] CSS bars proportional to count

### Diagnosis run queue
- [ ] Up to 10 most recent runs shown
- [ ] Columns: agent, ailment, therapy, tokens, date

## Done when
All boxes checked. Dashboard renders correctly at `http://localhost:8000/dashboard`.
