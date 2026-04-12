import json
import subprocess
from difflib import get_close_matches
import jellyfish
from pathlib import Path

class AppOpener:
    def __init__(self, cache_file="modules/system/learned_app_cache.json",
                 mishear_file="modules/system/app_mishears.json"):
        self.cache_file = Path(cache_file)
        self.learned_cache = json.load(self.cache_file.open("r")) if self.cache_file.exists() else {}

        self.mishear_file = Path(mishear_file)
        self.mishears = json.load(self.mishear_file.open("r")) if self.mishear_file.exists() else {}

        # Scan apps once
        self.installed_apps_cache = self._scan_installed_apps()

    def _scan_installed_apps(self):
        apps = {}
        try:
            result = subprocess.run(
                ['powershell', '-Command', 'Get-StartApps | ConvertTo-Json'],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            for entry in data:
                name = entry.get("Name", "").lower()
                appid = entry.get("AppID", "")
                if name:
                    apps[name] = appid
        except Exception as e:
            print(f"[Echo] Failed to get installed apps: {e}")
        print(f"[Echo] Found {len(apps)} installed apps ✅")
        return apps

    def save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.learned_cache, f, indent=2)

    def normalize(self, name):
        for wrong, correct in self.mishears.items():
            name = name.replace(wrong, correct)
        return name.lower().strip()

    def _is_valid_app_name(self, name):
        return len(name.split()) <= 3 and any(c.isalnum() for c in name)

    def open_app(self, name):
        name = self.normalize(name)
        if not self._is_valid_app_name(name):
            print(f"[Echo] '{name}' not valid ❌")
            return False

        # Learned cache
        if name in self.learned_cache:
            return self._launch(self.learned_cache[name], name)

        # Fuzzy match
        matches = get_close_matches(name, self.installed_apps_cache.keys(), n=1, cutoff=0.65)
        if matches:
            match = matches[0]
            self.learned_cache[name] = self.installed_apps_cache[match]
            self.save_cache()
            return self._launch(self.installed_apps_cache[match], match)

        # Phonetic match
        code = jellyfish.metaphone(name)
        for key, cmd in self.installed_apps_cache.items():
            if jellyfish.metaphone(key) == code:
                self.learned_cache[name] = cmd
                self.save_cache()
                return self._launch(cmd, key)

        print(f"[Echo] App '{name}' not found ❌")
        return False

    def _launch(self, cmd, display_name):
        try:
            if cmd.lower().endswith(".exe"):
                subprocess.Popen(cmd, shell=True)
            else:
                subprocess.Popen(f'explorer.exe shell:AppsFolder\\{cmd}', shell=True)
            print(f"[Echo] Opened {display_name} ✅")
            return True
        except Exception as e:
            print(f"[Echo] Failed to open {display_name}: {e}")
            return False