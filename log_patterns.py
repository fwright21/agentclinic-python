LOG_PATTERNS = [
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
        "pattern": r"telegram\.error\.TimedOut",
        "symptoms": "Telegram timed out waiting for response",
        "agent_name": "Pepper Affirmation Bot",
    },
    {
        "pattern": r"ERROR.*telegram_bot",
        "symptoms": "AIBriefing Telegram bot error",
        "agent_name": "AIBriefing Bot",
    },
    {
        "pattern": r"groq\.error\.RateLimitError",
        "symptoms": "Groq API rate limit hit",
        "agent_name": "AIBriefing Bot",
    },
    {
        "pattern": r"groq\.error\.APIConnectionError",
        "symptoms": "Groq API connection error",
        "agent_name": "AIBriefing Bot",
    },
    {
        "pattern": r"sqlite3\..*locked",
        "symptoms": "SQLite database locked",
        "agent_name": "AIBriefing Bot",
    },
]

DEDUP_WINDOW_MINUTES = 30

ERROR_LOG_FILES = [
    "/Users/francescawright/Documents/MyDailyAffirmationBot/affirmation_error.log",
    "/Users/francescawright/Documents/AIBriefing/telegram_error.log",
]


def get_agent_for_log(log_path: str) -> str:
    if "AffirmationBot" in log_path:
        return "Pepper Affirmation Bot"
    if "telegram" in log_path:
        return "AIBriefing Bot"
    return "Unknown Bot"
