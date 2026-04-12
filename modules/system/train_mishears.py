# modules/system/train_mishears.py
import json
from pathlib import Path

MISHEARS_FILE = Path("modules/system/mishears.json")
FAILED_LOG_FILE = Path("modules/system/failed_commands.json")

def train_mishears():
    if MISHEARS_FILE.exists():
        with open(MISHEARS_FILE, "r", encoding="utf-8") as f:
            mishears = json.load(f)
    else:
        mishears = {}

    if FAILED_LOG_FILE.exists():
        with open(FAILED_LOG_FILE, "r", encoding="utf-8") as f:
            failed_log = json.load(f)
    else:
        print("[Echo Training] No failed commands logged ✅")
        return

    for phrase in failed_log:
        print(f"\n[Echo Training] Misheard phrase: '{phrase}'")
        correct = input("Correct mapping (leave empty to ignore): ").strip()
        if correct:
            mishears[phrase] = correct

    with open(MISHEARS_FILE, "w", encoding="utf-8") as f:
        json.dump(mishears, f, indent=2)
    print("[Echo Training] Mishears updated ✅")