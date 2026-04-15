# brain/confidence.py

from difflib import get_close_matches

COMMAND_PATTERNS = {
    "network_scan": ["scan network", "network scan"],
    "process_check": ["check process", "show processes", "process list"],
    "shutdown": ["exit", "stop", "quit"]
}


def match_intent(text: str):
    text = text.lower()

    best_match = None
    best_score = 0

    for intent, patterns in COMMAND_PATTERNS.items():
        matches = get_close_matches(text, patterns, n=1, cutoff=0.5)

        if matches:
            score = similarity(text, matches[0])

            if score > best_score:
                best_score = score
                best_match = intent

    return best_match, best_score


def similarity(a, b):
    return len(set(a.split()) & set(b.split())) / max(len(a.split()), 1)