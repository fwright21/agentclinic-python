# Mission

AgentClinic is a clinic management system for AI agents. Agents check in when
something is wrong, get diagnosed, receive a treatment plan, and are discharged
when the issue is resolved.

The diagnosis is handled by a LangChain-powered engine — the "therapist" in the
system. It identifies the issue, prescribes a remedy, and writes a plain-English
report. Reports follow this format:

> "Issue was context window overflow. Applied context flush and summary injection.
> Recorded in visit log #42."

The CRUD app is the scaffolding. The diagnosis engine is the real deliverable.

---

## What We Do

AgentClinic gives AI agents a structured place to report problems and receive
treatment. It gives operators visibility into what is going wrong, how often,
and whether treatments are working.

---

## Who We Serve

- **Agents** — systems reporting an issue (hallucination, token overflow, prompt
  fatigue, context loss). They submit symptoms, receive a diagnosis + treatment,
  and re-submit to trigger a follow-up when the issue persists or recurs.
- **Staff / operators** — humans who monitor the dashboard, review visit records,
  and track treatment outcomes across the agent population.

## How the Diagnosis Engine Works

The diagnosis engine is a LangChain chain that acts as the therapist. On each
agent submission it:
1. Triages the intake — assigns severity and routes the case
2. Matches symptoms to known ailments
3. Prescribes treatment
4. Writes a plain-English report
5. Tracks its own token usage (self-diagnosis)

When an agent re-submits referencing a prior visit, the engine detects it as a
follow-up and evaluates whether the issue is RESOLVED, RECURRING, or CHRONIC.

---

## Workflow

```
Agent submits symptoms
        ↓
  [DIAGNOSIS ENGINE]
    1. Triage — severity + routing assigned
    2. Diagnosis — symptoms matched to ailment
    3. Treatment — prescription returned + logged
        ↓
  Agent re-submits referencing prior visit
        ↓
  [FOLLOW-UP] engine evaluates outcome
        ↓
  RESOLVED / RECURRING / CHRONIC
```

---

## Staff Dashboard

The dashboard shows:
- **Summary counts** — total agents, open appointments, active ailments
- **Agent health table** — each agent's current ailment + token usage flagged if high
- **Ailment trends** — most common ailments, treatment effectiveness rates
- **Appointment queue** — upcoming appointments with status

---

## What Success Looks Like

- A working Python + FastAPI web app with SQLite persistence
- A LangChain diagnosis chain that reads symptoms, identifies the ailment, and
  writes a plain-English treatment report
- Token usage tracked per diagnosis run and surfaced on the dashboard
- Staff can see what is wrong with the agent population at a glance

---

## Tone

Plain English. Clinical but not cold. Reports are short and factual:

> "Issue: prompt fatigue. Treatment: reduced instruction set, added memory summary.
> Logged: visit #17."

No jargon beyond what is necessary. No whimsy. Just clear, useful output.
