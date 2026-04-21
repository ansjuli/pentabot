import subprocess
import sys
import webbrowser
import shutil

from tools.nmap_tool import run_nmap_scan


def execute(decision: dict):
    intent = decision.get("intent")

    # =========================
    # NETWORK SCAN (NMAP)
    # =========================
    if intent == "network_scan":

        # 🔍 Pre-check dependency FIRST
        if not shutil.which("nmap"):
            return {
                "status": "missing",
                "tool": "nmap",
                "message": "Nmap is not installed"
            }

        # ✅ Ready state (DO NOT say scanning here)
        return {
            "status": "ready",
            "tool": "nmap",
            "message": "Scanning network..."
        }


    # =========================
    # INSTALL NMAP
    # =========================
    elif intent == "install_nmap":
        webbrowser.open("https://nmap.org/download.html")
        return {
            "status": "action",
            "tool": "nmap",
            "message": "Opening Nmap download page"
        }


    # =========================
    # PROCESS CHECK
    # =========================
    elif intent == "process_check":
        command = "tasklist" if sys.platform == "win32" else "ps aux"
        result = subprocess.getoutput(command)

        return {
            "status": "done",
            "tool": "system",
            "message": result
        }


    # =========================
    # SHUTDOWN
    # =========================
    elif intent == "shutdown":
        return {
            "status": "exit",
            "message": "Shutting down"
        }


    return {
        "status": "unknown",
        "message": "Command not recognized"
    }