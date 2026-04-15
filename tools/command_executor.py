# tools/command_executor.py

import os
import sys


def execute(decision: dict):
    intent = decision.get("intent")

    # 🔹 NETWORK SCAN (local info for now)
    if intent == "network_scan":
        print("[Pentabot] Running local network scan...")

        command = "ipconfig" if os.name == "nt" else "ifconfig"
        return os.system(command)

    # 🔹 PROCESS CHECK
    elif intent == "process_check":
        print("[Pentabot] Checking running processes...")

        command = "tasklist" if os.name == "nt" else "ps aux"
        return os.system(command)

    # 🔹 SHUTDOWN / EXIT
    elif intent == "shutdown":
        print("[Pentabot] Shutting down...")
        sys.exit()

    # 🧠 UNCERTAIN INPUT (NEW v0.2)
    elif intent == "uncertain":
        score = decision.get("score", 0)
        return f"[Pentabot] Not confident ({score:.2f}). Please repeat."

    # ❓ UNKNOWN INTENT
    elif intent == "unknown":
        return "[Pentabot] Command not recognized."

    # ⚠️ FALLBACK (safety)
    else:
        return "[Pentabot] No valid action found."