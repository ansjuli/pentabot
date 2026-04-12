import os

BASE_DIR = os.path.expanduser("~")

PATHS = {
    "music": os.path.join(BASE_DIR, "Music"),
    "videos": os.path.join(BASE_DIR, "Videos"),
    "documents": os.path.join(BASE_DIR, "Documents"),
    "images": os.path.join(BASE_DIR, "Pictures"),
}

EXTENSIONS = {
    "music": [".mp3", ".wav"],
    "videos": [".mp4", ".mkv"],
    "documents": [".pdf", ".docx", ".txt"],
    "images": [".jpg", ".png", ".jpeg"]
}