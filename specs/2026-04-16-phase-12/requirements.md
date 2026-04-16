# Phase 12 — Real-Agent Self-Healing: Log Watcher + Human-in-the-Loop

## Goal
Extend self-healing to real bots (Pepper affirmation bot, AIBriefing Telegram bot).
A persistent log watcher monitors their error logs. On detecting a known error pattern,
it auto-POSTs to AgentClinic for diagnosis. Staff approves the remedy via AIBriefing chat.py.
The bots themselves are never modified.

---

## Architecture

```
Bot runs in background (cron / launchd)
    → writes errors to *_error.log
    → log_watcher.py tails the log
    → pattern match detects known error
    → POSTs to POST /api/diagnose (same endpoint as Phase 11)
    → remedy queued in AIBriefing as PENDING
    → daily briefing shows "N remedies to review"
    → staff approves via chat.py
    → treatment steps displayed (manual action required)
```

---

## Part 1 — Log Watcher

### `log_watcher.py` (AgentClinic or standalone script)

Watches two log files:
- `/Users/francescawright/Documents/MyDailyAffirmationBot/affirmation_error.log`
- `/Users/francescawright/Documents/AIBriefing/telegram_error.log`

Behaviour:
- Tail each file from current end (not from beginning)
- On new line: check against error pattern registry
- If match: POST to `http://localhost:8000/api/diagnose`
  - `agent_name`: derived from log file (e.g. "Pepper Affirmation Bot")
  - `session_type`: "bot"
  - `symptoms`: matched error line(s) (last N lines for context)
- Deduplication: don't re-POST the same error within a cooldown window (default: 30 min)
- Runs as a persistent background process (not a one-shot script)

### Error pattern registry (`log_patterns.py`)

```python
PATTERNS = [
    {
        "pattern": r"telegram\.error\.Conflict",
        "symptoms": "Telegram Conflict: multiple bot instances running",
        "agent_name": "Pepper Affirmation Bot",
    },
    {
        "pattern": r"telegram\.error\.NetworkError",
        "symptoms": "Telegram NetworkError: connectivity issue",
        "agent_name": "Pepper Affirmation Bot",
    },
    {
        "pattern": r"ERROR.*telegram_bot",
        "symptoms": "AIBriefing Telegram bot error",
        "agent_name": "AIBriefing Bot",
    },
    # Extendable — add patterns without modifying watcher
]
```

---

## Part 2 — AgentClinic API extension

### `session_type = "bot"` in treatment step generator

Add bot-specific treatment steps to `treatment.py`:

| Therapy | Bot steps |
|---|---|
| Session Reset | Kill duplicate processes (`pkill -f bot_name.py`), restart via cron |
| Context Flush | Restart bot cleanly — no persistent state to flush |
| Novelty Injection | N/A for bots — flag for human review |
| Task Decomposition | N/A for bots — flag for human review |

### `PATCH /api/diagnose/{id}/approve` (already planned in Phase 11)
- Already covers bot remedies — no new endpoint needed

---

## Part 3 — AIBriefing chat.py extension

- "review remedies" flow already handles bot remedies
- Bot remedies show `session_type: bot` clearly
- Treatment steps for bots are manual (staff executes the command)
- No auto-execution of shell commands — human always confirms

---

## Part 4 — Watcher process management

### Launch as background process
```bash
nohup python log_watcher.py >> watcher.log 2>&1 &
```

Or add to cron to restart if it dies:
```
*/5 * * * * pgrep -f log_watcher.py || nohup python /path/to/log_watcher.py >> /path/to/watcher.log 2>&1 &
```

No launchd required — keep it simple.

---

## Out of scope
- Auto-executing remedies (shell commands never run without human approval)
- Watching stdout (bots already write to file logs — no need)
- Modifying the bots themselves
- Push notifications (Telegram message on new remedy — later)
