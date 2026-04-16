# Phase 4 — Requirements

## Goal
Agent detail page at `/agents/{id}`. Schema updated with new fields. Seed data updated. Link from agents list.

## Schema changes (new migration)
Add to `agents` table:
- `reasoning_level` TEXT (one of: low, medium, high, xhigh)
- `skills` TEXT (comma-separated)
- `tools` TEXT (comma-separated)
- `mcps` TEXT (comma-separated, nullable)

## Updated seed agents

| Name | Model Type | Reasoning Level | Status | Skills | Tools | MCPs | Presenting Complaints |
|---|---|---|---|---|---|---|---|
| Pepper-Bot | ollama/qwen2.5 | low | Resolved | affirmation-generation, scheduling | telegram, apscheduler | — | Repeated affirmation sent twice in same day |
| Briefing-Agent | groq/llama-3.3 | medium | Recurring | summarisation, semantic-search, extraction | telegram, chat.py | mcp-memory | Token budget exceeded on evening digest |
| LinguistDebate-A | gpt-5.2 | high | Chronic | compression, review, benchmarking | codex-cli, deepeval | — | Quality drop on definition queries after compression |
| A2A-Coordinator | gpt-5.3 | xhigh | Active | coordination, protocol-design | run_tests.py | — | Repair turns spiking on PCL-1 protocol runs |
| ClaudeBot-7 | claude-sonnet-4.6 | medium | Unknown | planning, debugging, architecture | bash, file_read | mcp-registry | No recent activity logged |

## Page requirements
1. `/agents/{id}` returns 404 if agent not found
2. Page renders inside `base.html`
3. Shows all fields: name, model type, reasoning level, status (badge), presenting complaints, skills, tools, MCPs
4. Skills, tools, MCPs displayed as tags/pills
5. Link from agents list — agent name is clickable, links to `/agents/{id}`

## Out of scope
- Edit / delete agent
- Visit history (Phase 9)
