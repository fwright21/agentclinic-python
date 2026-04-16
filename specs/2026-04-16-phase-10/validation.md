# Phase 10 — Validation

## Checks

### Error pages
- [ ] `GET /agents/999` renders 404.html (not plain text)
- [ ] Trigger a 500 error manually — renders 500.html

### Input sanitisation
- [ ] Submit empty symptoms → error shown, no diagnosis run created
- [ ] Submit symptoms < 10 chars → error shown
- [ ] Submit valid symptoms → diagnosis runs normally

### Logging
- [ ] Each request logged to stdout with method, path, status, response time

### Tests
- [ ] `pytest tests/` runs without errors
- [ ] All route tests pass
- [ ] No real Groq calls made during tests
- [ ] Test DB isolated from `agentclinic.db`

## Done when
`pytest tests/` passes with 0 failures.
