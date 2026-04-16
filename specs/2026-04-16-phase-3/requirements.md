# Phase 3 — Requirements

## Goal
SQLite database with an `agents` table. Migration system. 5 seed agents. `/agents` page listing all agents.

## Requirements

1. `migrations/` directory with plain `.sql` migration files
2. `migrate.py` script that runs all `.sql` files in order
3. `agents` table with fields:
   - `id` INTEGER PRIMARY KEY AUTOINCREMENT
   - `name` TEXT NOT NULL
   - `model_type` TEXT NOT NULL
   - `status` TEXT NOT NULL (one of: Active, Resolved, Recurring, Chronic, Unknown)
   - `presenting_complaints` TEXT
   - `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
4. 5 seed agents pre-loaded (see below)
5. `/agents` route returning a page listing all agents
6. Agents list page renders inside `base.html`
7. Each agent row shows: name, model type, status (with status colour), presenting complaints

## Seed Agents

| Name | Model Type | Status | Presenting Complaints |
|---|---|---|---|
| GPT-4-Agent-01 | gpt-4 | Active | Hallucination on factual queries |
| ClaudeBot-7 | claude-3 | Chronic | Repeated context window overflow |
| Gemini-Probe-3 | gemini-pro | Resolved | Prompt fatigue after long sessions |
| MistralX-2 | mistral-7b | Recurring | Token budget exceeded on summaries |
| LlamaGuard-9 | llama-3 | Unknown | No recent activity logged |

## Out of scope
- Agent detail page (Phase 4)
- Pagination
- Search / filtering
