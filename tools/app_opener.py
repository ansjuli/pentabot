import subprocess
import difflib


class AppOpener:
    def __init__(self, apps_cache=None):
        self.apps = apps_cache or {}

    def set_apps(self, apps):
        self.apps = apps

    def normalize(self, text):
        return text.lower().strip()

    # ----------------------------
    # STRICT VALIDATION (IMPORTANT FIX)
    # ----------------------------
    def is_valid_query(self, text):
        if not text:
            return False

        text = text.strip()
        words = text.split()

        if len(words) == 0:
            return False

        # must contain meaningful word
        if not any(len(w) > 2 for w in words):
            return False

        # block garbage single-word noise
        junk = {"huh", "lol", "uh", "um", "hmm", "a"}

        if all(w in junk for w in words):
            return False

        return True

    # ----------------------------
    # STRONG MATCHER (FIXED)
    # ----------------------------
    def find_best_match(self, query):
        query = self.normalize(query)

        best_match = None
        best_score = 0

        for name, appid in self.apps.items():
            name_l = name.lower()

            # exact match
            if query == name_l:
                return appid

            # containment match (very important for firefox, paint etc.)
            if query in name_l or name_l in query:
                return appid

            # fuzzy match
            score = difflib.SequenceMatcher(None, query, name_l).ratio()

            if score > best_score:
                best_score = score
                best_match = appid

        # STRICT threshold to avoid OneDrive/Photos mistakes
        if best_score < 0.72:
            return None

        return best_match

    # ----------------------------
    # MAIN ENTRY
    # ----------------------------
    def open_app(self, text):
        text = self.normalize(text)

        if not self.is_valid_query(text):
            print(f"[Echo] Ignored invalid app query: {text}")
            return False

        app_id = self.find_best_match(text)

        if not app_id:
            print(f"[Echo] App not found: {text}")
            return False

        try:
            subprocess.Popen(
                f'explorer.exe shell:AppsFolder\\{app_id}',
                shell=True
            )

            print(f"[Echo] Opened app ✔ -> {text}")
            return True

        except Exception as e:
            print(f"[Echo] Failed to open app: {e}")
            return False