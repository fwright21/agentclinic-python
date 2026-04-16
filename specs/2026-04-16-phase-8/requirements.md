# Phase 8 — Requirements

## Goal
Staff dashboard at `/dashboard` with four views: summary counts, agent health table, ailment frequency, diagnosis run queue.

---

## Dashboard sections

### 1. Summary counts
- Total agents
- Total diagnosis runs
- Active ailments (distinct ailments with at least one diagnosis run)
- Agents flagged for high token usage (at least one diagnosis run with total_tokens > 1000)

### 2. Agent health table
- One row per agent
- Columns: Name (link to /agents/{id}) | Model Type | Status badge | Most recent ailment | Last diagnosis date | Token flag
- Token flag: ⚠️ if any diagnosis run for this agent has total_tokens > 1000

### 3. Ailment frequency
- List of ailments ranked by number of diagnosis runs
- Show: ailment name | count | simple bar (CSS width, no JS)

### 4. Diagnosis run queue
- Most recent 10 diagnosis runs across all agents
- Columns: Agent name | Ailment | Therapy | Tokens | Date

---

## Token flag threshold
`HIGH_TOKEN_THRESHOLD = 1000` — defined as a constant in `src/dashboard.py`, easy to change.

---

## Out of scope
- Treatment effectiveness (no outcomes yet — Phase 9)
- Real-time updates
- Filtering / sorting
