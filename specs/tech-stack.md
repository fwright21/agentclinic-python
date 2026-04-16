# Tech Stack

AgentClinic is a Python web application with server-side rendering and a
LangChain-powered AI diagnosis layer.

## Core

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.11+ | Primary stack |
| Framework | FastAPI | Lightweight, async, Pydantic-native — closest Python equivalent to Hono |
| Validation | Pydantic | Type hints + validation across API and AI layers |
| Templating | Jinja2 | Server-side HTML rendering; no JS build step |
| CSS | Plain CSS | No build step required |

## Data

| Layer | Choice | Rationale |
|---|---|---|
| Database | SQLite via `aiosqlite` | Embedded, no infrastructure; async driver keeps FastAPI event loop unblocked |
| Migrations | Plain `.sql` files + `migrate.py` | Simple, explicit, mirrors course pattern |

## AI Layer (Phase 5 — Ailments Catalog onwards)

Introduced at Phase 5 so the diagnosis engine is built alongside the data model
it depends on, not bolted on afterwards.

| Layer | Choice | Rationale |
|---|---|---|
| Orchestration | LangChain (`langchain-anthropic`) | Primary stack; chains for triage, diagnosis, treatment |
| LLM | Claude Haiku 4.5 | Low cost, sufficient for classification and structured output |
| Output parsing | Pydantic `OutputParser` | Structured extraction from free-text agent intake |
| Token tracking | Custom `BaseCallbackHandler` | Reads Anthropic response usage metadata (prompt + completion tokens) exposed by `langchain-anthropic` — no third-party tokenizer needed |

## Testing

| Layer | Choice | Rationale |
|---|---|---|
| Framework | pytest | Standard Python testing |
| HTTP client | httpx (async) | FastAPI-native async test client |

## Tooling

- `uvicorn --reload` — dev server
- `python-dotenv` — .env loading
- `venv` — environment isolation

## What We Are Not Using

- No React, Vue, or TypeScript — server-side rendering keeps the stack simple
- No ORM — plain SQL is sufficient at this scale
- No Docker — not yet; later phase concern
