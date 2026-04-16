# Phase 12 — Plan

## File structure
```
agentclinic-python/
  src/
    log_patterns.py       (create — error pattern registry)
    log_watcher.py        (create — tails bot error logs, POSTs to API)
    treatment.py          (update — add "bot" session_type steps)
  
  (No changes needed to AIBriefing or chat.py — Phase 11 covers approval flow)
```

## Steps

### 1. Create `src/log_patterns.py`
- `WATCHED_LOGS`: dict mapping log file path → agent_name
- `PATTERNS`: list of dicts with `pattern` (regex), `symptoms`, `agent_name`
- `match_line(line)` → returns matched pattern dict or None

### 2. Update `src/treatment.py`
- Add `"bot"` key to `TREATMENT_STEPS` for each therapy
- Bot steps are manual instructions (e.g. "Kill duplicate process: `pkill -f affirmation_bot.py`")

### 3. Create `src/log_watcher.py`
- `tail_file(path)` generator — yields new lines as they appear
- `Watcher` class:
  - `__init__`: loads patterns, initialises dedup cache `{(agent, pattern): last_posted_time}`
  - `should_post(agent, pattern_id)` → bool (30 min cooldown)
  - `post_diagnosis(agent_name, symptoms)` → calls `POST /api/diagnose`
  - `watch()` → main loop: tail both files, match, post
- `if __name__ == "__main__"`: run watcher, handle KeyboardInterrupt cleanly

### 4. Update briefing HTML for bot health

   **`evening_digest.py`:**
   - `get_recent_diagnoses(days=1, session_type="bot")` to filter bot-only runs
   - Extend the "Agent Health Today" card (added in Phase 11) with a **"Bot Health"** subsection:
     - Lists bot diagnosis runs from today separately from session runs
     - Status badge: PENDING_APPROVAL / APPROVED / REJECTED
     - Source badge: "auto-detected" (from log watcher) vs "manual"

   **`insights_dashboard.py`:**
   - Extend "Agent Health Trends" card (added in Phase 11):
     - Second tab or section: **"Bot Issues (7 days)"**
     - Bar chart: top bot error patterns by frequency
     - Shows which bot triggered most diagnoses

### 5. Add to roadmap
- Update `specs/roadmap.md` Phase 12 entry with checkboxes
