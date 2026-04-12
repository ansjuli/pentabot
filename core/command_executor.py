import json
import subprocess
from difflib import get_close_matches, SequenceMatcher
import jellyfish
from pathlib import Path
from modules.system.app_opener import AppOpener

app_opener = AppOpener()

COMMANDS_PATH = Path(__file__).parent.parent / "commands.json"
COMMANDS = json.load(COMMANDS_PATH.open("r", encoding="utf-8"))


def run_command(cmd):
    subprocess.Popen(cmd, shell=True)
    print(f"[Echo] Command executed ✅ -> {cmd}")


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def execute_command(text):
    text = text.lower().strip()

    if len(text.split()) <= 1:
        return None

    # ----------------------------
    # SAFE FUZZY MATCH (v0.4.1)
    # ----------------------------
    matches = get_close_matches(text, COMMANDS.keys(), n=1, cutoff=0.5)

    if matches:
        cmd_key = matches[0]
        score = similarity(text, cmd_key)

        print(f"[Echo Debug] Match: '{cmd_key}' | Score: {score:.2f}")

        if score >= 0.75:
            run_command(COMMANDS[cmd_key])
            return f"Opening {cmd_key}"
        else:
            print("[Echo] Low confidence match ignored ⚠️")
            return None

    # ----------------------------
    # PHONETIC MATCH (SAFE)
    # ----------------------------
    text_code = jellyfish.metaphone(text)

    for key, cmd in COMMANDS.items():
        if jellyfish.metaphone(key) == text_code:
            score = similarity(text, key)

            if score >= 0.75:
                run_command(cmd)
                return f"Opening {key}"

    # ----------------------------
    # APP FALLBACK
    # ----------------------------
    opened = app_opener.open_app(text)
    if opened:
        return f"Opening {text}"

    return None