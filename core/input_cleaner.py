# core/input_cleaner.py
import json
from pathlib import Path
import re

class InputCleaner:
    def __init__(self):
        self.mishear_files = {
            "app": Path("modules/system/app_mishears.json"),
            "system": Path("modules/system/system_mishears.json"),
            "files": Path("modules/files/files_mishears.json")
        }
        self.mishears = {}
        for module, path in self.mishear_files.items():
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self.mishears[module] = json.load(f)
            else:
                self.mishears[module] = {}

    def clean_input(self, text, module="app"):
        text = text.lower().strip()
        fillers = ["i've been", "up", "to", "we'll see", "i'll be", "i went", "i am", "i was",
                   "uh", "um", "ah", "hmm", "you know", "like", "so", "well"]
        for f in fillers:
            text = text.replace(f, "")
        text = re.sub(r'\s+', " ", text).strip()
        # Apply mishears
        for wrong, correct in self.mishears.get(module, {}).items():
            if wrong in text:
                text = text.replace(wrong, correct)
        return text