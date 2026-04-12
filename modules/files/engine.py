import os
import tempfile
import threading
import time
from pathlib import Path
import json
from core.input_cleaner import InputCleaner

cleaner = InputCleaner()

EXTENSIONS = {
    "music": [".mp3", ".wav", ".flac"],
    "videos": [".mp4", ".mkv", ".mov"],
    "documents": [".pdf", ".docx", ".txt"],
    "images": [".jpg", ".jpeg", ".png", ".gif"]
}

USER_FOLDERS = [
    os.path.expanduser("~"),
    "D:\\",
    "E:\\"
]

EXCLUDE_FOLDERS = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    os.path.expanduser("~\\AppData"),
    os.path.expanduser("~\\.vscode"),
    "C:\\Python"
]

class FileEngine:
    def __init__(self, auto_rescan=True, rescan_interval=600, mishear_file="modules/files/file_mishears.json"):
        self.files = {cat: [] for cat in EXTENSIONS}
        self.auto_rescan = auto_rescan
        self.rescan_interval = rescan_interval

        self.mishears_file = Path(mishear_file)
        if self.mishears_file.exists():
            with open(self.mishears_file, "r", encoding="utf-8") as f:
                self.mishears = json.load(f)
        else:
            self.mishears = {}

        thread = threading.Thread(target=self.background_scan, daemon=True)
        thread.start()

    def background_scan(self):
        while True:
            self.scan_all()
            if not self.auto_rescan:
                break
            time.sleep(self.rescan_interval)

    def scan_all(self):
        self.files = {cat: [] for cat in EXTENSIONS}
        for folder in USER_FOLDERS:
            if not os.path.exists(folder):
                continue
            for root, _, files in os.walk(folder):
                if any(root.startswith(ex) for ex in EXCLUDE_FOLDERS):
                    continue
                for file in files:
                    for category, exts in EXTENSIONS.items():
                        if file.lower().endswith(tuple(exts)):
                            self.files[category].append(os.path.join(root, file))

    def handle(self, category, command_text=None):
        files = self.files.get(category, [])
        if not files:
            return f"No {category} files found."

        if command_text and "folder" in command_text:
            folder_map = {
                "music": os.path.expanduser("~\\Music"),
                "videos": os.path.expanduser("~\\Videos"),
                "documents": os.path.expanduser("~\\Documents"),
                "images": os.path.expanduser("~\\Pictures")
            }
            folder = folder_map.get(category)
            if folder and os.path.exists(folder):
                os.startfile(folder)
                return f"Opening your {category} folder."

        if category in ["music", "videos"]:
            playlist_path = os.path.join(tempfile.gettempdir(), f"echo_{category}.m3u")
            with open(playlist_path, "w", encoding="utf-8") as f:
                for file in files:
                    f.write(file + "\n")
            os.startfile(playlist_path)
            return f"Opening all {category} in your player."

        if category == "images":
            os.startfile(os.path.expanduser("~\\Pictures"))
            return "Opening your images."

        if category == "documents":
            os.startfile(os.path.expanduser("~\\Documents"))
            return "Opening your documents."

        return f"Could not handle {category}."