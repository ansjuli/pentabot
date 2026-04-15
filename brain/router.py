# brain/router.py

from brain.confidence import match_intent

CONFIDENCE_THRESHOLD = 0.6


def route(text: str):
    intent, score = match_intent(text)

    print(f"[Confidence]: {score:.2f}")

    if score < CONFIDENCE_THRESHOLD:
        return {
            "intent": "uncertain",
            "raw": text,
            "score": score
        }

    if intent == "network_scan":
        return {"intent": "network_scan", "target": "local"}

    if intent == "process_check":
        return {"intent": "process_check"}

    if intent == "shutdown":
        return {"intent": "shutdown"}

    return {"intent": "unknown", "raw": text}