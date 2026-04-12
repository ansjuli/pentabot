# modules/system/failure_logger.py
import json
from pathlib import Path

FAILED_LOG_FILE = Path("modules/system/failed_commands.json")

def log_failed_command(text):
    FAILED_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if FAILED_LOG_FILE.exists():
        with open(FAILED_LOG_FILE, "r", encoding="utf-8") as f:
            failed_log = json.load(f)
    else:
        failed_log = []

    if text not in failed_log:
        failed_log.append(text)
        with open(FAILED_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(failed_log, f, indent=2)