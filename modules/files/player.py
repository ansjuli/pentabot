import os
import vlc
import time

def open_file(path, filetype=None):
    if not os.path.exists(path):
        print(f"[Echo] File does not exist: {path}")
        return

    if filetype == "music":
        try:
            player = vlc.MediaPlayer(path)
            player.play()
            time.sleep(0.5)  # allow VLC to start
        except Exception as e:
            print(f"[Echo] VLC error: {e}, fallback to default player")
            os.startfile(path)
    else:
        os.startfile(path)