TREATMENT_STEPS = {
    "Context Flush": {
        "claude-code": [
            "Run /compact to summarise conversation history",
            "If issue persists, start a new session with a handoff file",
        ],
        "codex": [
            "Start new Codex session",
            "Paste handoff summary from previous session",
        ],
        "other": [
            "Restart session with fresh context",
            "Provide summary of previous session to maintain continuity",
        ],
        "bot": [
            "Restart bot cleanly — no persistent state to flush",
            "Verify bot restarts without errors",
        ],
    },
    "Memory Summary Injection": {
        "claude-code": [
            "Run session-handoff skill, paste summary into new session",
            "Continue from handoff file",
        ],
        "codex": [
            "Export context summary from current session",
            "Re-inject summary at start of new session",
        ],
        "other": [
            "Create summary of current conversation",
            "Resume with summary as context",
        ],
        "bot": [
            "Save current state to file",
            "Restart bot and reload state",
        ],
    },
    "Instruction Set Reduction": {
        "claude-code": [
            "Review and trim CLAUDE.md active rules",
            "Remove low-priority instructions",
        ],
        "codex": [
            "Reduce system prompt to essential instructions only",
            "Test with streamlined prompt",
        ],
        "other": [
            "Simplify instructions to top 3 priorities",
            "Re-test task completion",
        ],
    },
    "Compression Prompt": {
        "claude-code": [
            "Run ultra skill for maximum token compression",
            "Apply caveman-mode prompts",
        ],
        "codex": [
            "Apply round3_refined prompt for output compression",
            "Test with compressed output",
        ],
        "other": ["Use compact-mode prompts", "Reduce response verbosity"],
    },
    "Session Reset": {
        "claude-code": [
            "Close current session",
            "Resume from handoff file in new session",
        ],
        "codex": [
            "Start new Codex session from spec",
            "Continue without prior context",
        ],
        "other": ["End current session cleanly", "Begin fresh session"],
        "bot": [
            "Kill duplicate bot processes: pkill -f <bot_name>.py",
            "Restart bot via cron or launchctl",
        ],
    },
    "Novelty Injection": {
        "claude-code": [
            "Ask model: Try a completely different approach",
            "Explicitly request creative reframing",
        ],
        "codex": ["Change effort level or model", "Try different model tier"],
        "other": ["Prompt for alternative strategies", "Request fresh perspective"],
        "bot": [
            "Flag for human review — not applicable for automated bots",
        ],
    },
    "Confidence Recalibration": {
        "claude-code": [
            "Relax constraints in CLAUDE.md",
            "Allow more independent decision-making",
        ],
        "codex": ["Adjust model temperature/effort", "Lower reasoning effort"],
        "other": ["Reduce hesitation in prompts", "Encourage more decisive responses"],
    },
    "Task Decomposition": {
        "claude-code": [
            "Break task into subtasks using subagents-prompt skill",
            "Execute subtasks sequentially",
        ],
        "codex": ["Split into multiple Codex tasks", "Chain tasks together"],
        "other": ["Divide problem into smaller steps", "Solve incrementally"],
        "bot": [
            "Flag for human review — not applicable for automated bots",
        ],
    },
}


def generate_steps(therapy: str, session_type: str = "claude-code") -> list[str]:
    steps_by_type = TREATMENT_STEPS.get(therapy, {})
    if session_type in steps_by_type:
        return steps_by_type[session_type]
    if "other" in steps_by_type:
        return steps_by_type["other"]
    return []
