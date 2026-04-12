# modules/files/scanner.py
import os

# File extensions per category
EXTENSIONS = {
    "music": [".mp3", ".wav", ".flac"],
    "videos": [".mp4", ".mkv", ".mov"],
    "documents": [".pdf", ".docx", ".txt"],
    "images": [".jpg", ".jpeg", ".png", ".gif"]
}

# Folders to scan (user + custom)
USER_FOLDERS = [
    os.path.expanduser("~\\Music"),
    os.path.expanduser("~\\Videos"),
    os.path.expanduser("~\\Documents"),
    os.path.expanduser("~\\Pictures"),
    "D:\\MySongs",        # example custom folder
    "E:\\CustomVideos"    # example custom folder
]

# Folders to exclude (system, programs, Python, VSCode)
EXCLUDE_FOLDERS = [
    os.path.expanduser("~\\AppData"),
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Python",               # adjust to your Python path
    os.path.expanduser("~\\.vscode")
]

def scan_files():
    """
    Scan all USER_FOLDERS for files matching EXTENSIONS,
    excluding EXCLUDE_FOLDERS. Returns dict: category -> list of file paths
    """
    all_files = {cat: [] for cat in EXTENSIONS.keys()}

    for folder in USER_FOLDERS:
        if not os.path.exists(folder):
            continue

        for root, _, files in os.walk(folder):
            # Skip excluded folders
            if any(root.startswith(ex) for ex in EXCLUDE_FOLDERS):
                continue

            for file in files:
                for category, exts in EXTENSIONS.items():
                    if file.lower().endswith(tuple(exts)):
                        full_path = os.path.join(root, file)
                        all_files[category].append(full_path)

    return all_files