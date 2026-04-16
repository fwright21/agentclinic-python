# Task Assessment — AgentClinic Python Edition

Generated: 2026-04-16
Tool: task-optimizer (Step 0)

---

```
TASK ASSESSMENT
───────────────
Complexity: complex

10 phases, 3+ sessions, novel AI layer (LangChain + token tracking),
junior engineer — needs spec-first discipline throughout.

Model plan:
  Phase 1 (Hello FastAPI — server + one route): Codex / GPT-5.1-Codex-Mini, Low
    — locked spec, boilerplate only, no decisions
  Phase 2 (Base layout — Jinja2 templates + CSS): Codex / GPT-5.1-Codex-Mini, Low
    — templating is mechanical once pattern is set
  Phase 3 (Agents list — SQLite + migrations + seed): Codex / GPT-5.2-Codex, Medium
    — some decisions on schema design
  Phase 4 (Agent detail page): Codex / GPT-5.1-Codex-Mini, Low
    — follows pattern from Phase 3
  Phase 5 (Ailments catalog): Codex / GPT-5.1-Codex-Mini, Low
    — same pattern as Phase 3-4
  Phase 6 (Therapies catalog): Codex / GPT-5.1-Codex-Mini, Low
    — same pattern
  Phase 7 (Appointment booking — form + validation): Codex / GPT-5.2-Codex, Medium
    — form validation + state logic adds decisions
  Phase 8 (Staff dashboard): Codex / GPT-5.2-Codex, Medium
    — aggregation queries + layout decisions
  Phase 9 (AI diagnosis layer — LangChain + token tracking): Claude Code / Sonnet
    — LangChain chains are primary stack; Sonnet knows it best
    — token tracking callback design needs judgment
  Phase 10 (Polish + tests): Codex / GPT-5.1-Codex-Mini, Low-Medium
    — pytest + httpx tests against locked routes

Verbosity:
  Phases 1–8: COMPACT — executing specs, not learning
  Phase 9: EXPAND — LangChain chain design + token tracking needs explanation
  Phase 10: COMPACT

Token strategy:
  Make a handoff after Phase 4 and after Phase 8 to reset context.
  Phases 1–8 are Codex tasks — hand off via /codex:rescue after each feature spec.
  Phase 9 stays in Claude Code / Sonnet (LangChain expertise).

Compression:
  Phases 1–8: Compact-mode rules — code output, no prose
  Phase 9 (explanations): compact-mode fallback (round3 slot — not yet ready)
  Phase 10: Compact-mode rules — code output

Switch instructions:
  ⚠️ Phases 1–8: Current: Claude Code (Sonnet) → Hand off to Codex after each spec
    A) Run /codex:rescue with the feature spec path
    B) Use /codex:review after each phase for a quick check
  ⚠️ Phase 9: Stay in Claude Code / Sonnet — do not hand to Codex
  ⚠️ Phase 10: Current: Sonnet → Codex / GPT-5.1-Codex-Mini
    A) Run /codex:rescue with test requirements
```
