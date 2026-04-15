import os

def execute(decision):

    intent = decision.get("intent")

    if intent == "network_scan":
        print("[Pentabot] Running local scan...")
        return os.system("ipconfig" if os.name == "nt" else "ifconfig")

    elif intent == "process_check":
        print("[Pentabot] Checking processes...")
        return os.system("tasklist" if os.name == "nt" else "ps aux")

    elif intent == "shutdown":
        print("[Pentabot] Stopping system...")
        exit()

    else:
        return "[Pentabot] Unknown command"