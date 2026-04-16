#!/usr/bin/env python3
"""
Log watcher for bot error monitoring.
Watches error logs and POSTs to AgentClinic when patterns match.
"""

import re
import time
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

from log_patterns import (
    LOG_PATTERNS,
    DEDUP_WINDOW_MINUTES,
    ERROR_LOG_FILES,
    get_agent_for_log,
)

API_URL = "http://localhost:8000/api/diagnose"

last_errors = {}


def get_last_position(log_path: str) -> int:
    """Get last read position from marker file."""
    marker = Path(str(log_path) + ".pos")
    if marker.exists():
        return int(marker.read_text().strip())
    return 0


def save_last_position(log_path: str, pos: int):
    """Save last read position to marker file."""
    marker = Path(str(log_path) + ".pos")
    marker.write_text(str(pos))


def should_dedup(error_key: str) -> bool:
    """Check if error should be deduplicated."""
    now = datetime.now()
    if error_key in last_errors:
        last_time = last_errors[error_key]
        if (now - last_time).total_seconds() < DEDUP_WINDOW_MINUTES * 60:
            return True
    last_errors[error_key] = now
    return False


def check_log_file(log_path: str):
    """Check a single log file for new errors."""
    if not Path(log_path).exists():
        return

    last_pos = get_last_position(log_path)

    with open(log_path, "r") as f:
        f.seek(last_pos)
        new_lines = f.readlines()
        new_pos = f.tell()
        save_last_position(log_path, new_pos)

    if not new_lines:
        return

    content = "".join(new_lines[-5:])  # Last 5 lines for context

    for pattern_def in LOG_PATTERNS:
        pattern = pattern_def["pattern"]
        if re.search(pattern, content, re.IGNORECASE):
            error_key = f"{log_path}:{pattern}"
            if should_dedup(error_key):
                continue

            try:
                response = requests.post(
                    API_URL,
                    json={
                        "agent_name": pattern_def["agent_name"],
                        "session_type": "bot",
                        "symptoms": pattern_def["symptoms"],
                    },
                    timeout=10,
                )
                if response.status_code == 200:
                    print(
                        f"[{datetime.now().isoformat()}] Posted to API: {pattern_def['symptoms']}"
                    )
                else:
                    print(
                        f"[{datetime.now().isoformat()}] API error: {response.status_code}"
                    )
            except Exception as e:
                print(f"[{datetime.now().isoformat()}] POST failed: {e}")


def main():
    print(f"[{datetime.now().isoformat()}] Log watcher started")
    while True:
        for log_path in ERROR_LOG_FILES:
            try:
                check_log_file(log_path)
            except Exception as e:
                print(f"Error checking {log_path}: {e}")
        time.sleep(10)


if __name__ == "__main__":
    main()
