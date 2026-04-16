# Phase 10 — Plan

## File structure
```
agentclinic-python/
  src/
    main.py                     (update — exception handlers, logging middleware, input validation)
    templates/
      404.html                  (create)
      500.html                  (create)
  tests/
    conftest.py                 (create — async test client fixture)
    test_routes.py              (create — all route tests)
```

## Steps

1. Update `src/main.py`:
   - Add `logging` middleware — log method, path, status, response time
   - Add `@app.exception_handler(404)` → render `404.html`
   - Add `@app.exception_handler(500)` → render `500.html`
   - Add symptoms validation in `POST /agents/{id}/diagnose`:
     - Strip whitespace
     - If len < 10 → redirect back with `?error=too_short`
   - Show error message on agent detail page if `?error=too_short`

2. Create `src/templates/404.html`:
   - Extends `base.html`
   - "404 — Agent not found" heading
   - Back link to `/agents`

3. Create `src/templates/500.html`:
   - Extends `base.html`
   - "500 — Something went wrong" heading
   - Back link to `/`

4. Create `tests/conftest.py`:
   - Async httpx `AsyncClient` fixture pointing at the FastAPI app
   - Test DB setup — use a separate `test.db` so tests don't touch `agentclinic.db`

5. Create `tests/test_routes.py`:
   - One test per route listed in requirements
   - Mock `run_diagnosis` using `unittest.mock.patch`
   - All tests async
