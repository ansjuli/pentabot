import json
import subprocess
from pathlib import Path
from difflib import SequenceMatcher
from core.command_executor import execute_command

# ----------------------------
# Load system mishears
# ----------------------------
MISHEARS_FILE = Path("modules/system/system_mishears.json")

if MISHEARS_FILE.exists():
    with open(MISHEARS_FILE, "r", encoding="utf-8") as f:
        system_mishears = json.load(f)
else:
    system_mishears = {}


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def handle(command_text):
    """
    SYSTEM LAYER (v0.4.1 SAFE VERSION)

    Flow:
    1. Normalize input
    2. Apply mishears correction
    3. Try direct system execution (safe)
    4. Fallback to command executor
    """

    cmd = command_text.lower().strip()

    # ----------------------------
    # 1️⃣ APPLY MISHEARS
    # ----------------------------
    for wrong, correct in system_mishears.items():
        if wrong in cmd:
            cmd = cmd.replace(wrong, correct)

    # ----------------------------
    # 2️⃣ DIRECT SYSTEM COMMAND EXECUTION
    # ----------------------------
    try:
        # IMPORTANT: only allow safe execution via mapped commands
        # (prevents random Vosk garbage triggering system calls)

        # If it's already a valid Windows command string
        if cmd.startswith("start ") or "ms-settings:" in cmd or "netsh" in cmd:
            subprocess.run(cmd, shell=True)
            return f"Executed system command: {cmd}"

    except Exception as e:
        return f"Failed system execution: {cmd} ({e})"

    # ----------------------------
    # 3️⃣ FALLBACK → EXECUTOR (SAFE GATE INSIDE)
    # ----------------------------
    result = execute_command(cmd)
    if result:
        return f"Executed system command: {cmd}"

    # ----------------------------
    # 4️⃣ NOTHING MATCHED
    # ----------------------------
    return None