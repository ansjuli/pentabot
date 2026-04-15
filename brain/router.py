def route(text: str):
    text = text.lower()

    # SIMPLE INTENTS (Phase 1)
    if "scan" in text and "network" in text:
        return {
            "intent": "network_scan",
            "target": "local"
        }

    if "process" in text:
        return {
            "intent": "process_check"
        }

    if "exit" in text or "stop" in text:
        return {
            "intent": "shutdown"
        }

    return {
        "intent": "unknown",
        "raw": text
    }