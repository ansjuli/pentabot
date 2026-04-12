import sounddevice as sd
import numpy as np
import librosa
import threading
import queue
import time
import os
from scipy.spatial.distance import cosine

# -----------------------------
# CONFIG
# -----------------------------
DEVICE = 9               # Realtek Microphone Array
INPUT_SR = 16000         # lowered to 16kHz for CPU efficiency
CHANNELS = 1
DURATION = 1.0           # seconds per chunk
THRESHOLD = 0.7          # MFCC similarity threshold
DEBOUNCE_TIME = 1.0      # seconds to ignore repeats
ENERGY_THRESHOLD = 0.01  # ignore near-silence

WAKE_DIR = "wake_samples"  # folder with recorded wake words
wake_files = [f for f in os.listdir(WAKE_DIR) if f.endswith(".wav")]

# -----------------------------
# QUEUE FOR AUDIO
# -----------------------------
q = queue.Queue()

# -----------------------------
# LOAD WAKE WORD FEATURES
# -----------------------------
wake_features = []
for file in wake_files:
    audio, sr = librosa.load(os.path.join(WAKE_DIR, file), sr=INPUT_SR)
    mfcc = librosa.feature.mfcc(y=audio, sr=INPUT_SR, n_mfcc=13)
    wake_features.append(np.mean(mfcc.T, axis=0))

# -----------------------------
# HELPERS
# -----------------------------
def is_audio_loud_enough(audio):
    return np.max(np.abs(audio)) > ENERGY_THRESHOLD

def extract_mfcc(audio):
    mfcc = librosa.feature.mfcc(y=audio, sr=INPUT_SR, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

def cosine_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

def detect_wake_word(audio_chunk):
    if not is_audio_loud_enough(audio_chunk):
        return False
    mfcc_live = extract_mfcc(audio_chunk)
    for ref in wake_features:
        score = cosine_similarity(mfcc_live, ref)
        if score > THRESHOLD:
            print(f"[WakeWord] Match score: {score:.2f} ✅")
            return True
    return False

# -----------------------------
# AUDIO CALLBACK
# -----------------------------
def callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio = indata[:, 0] if indata.ndim > 1 else indata
    q.put(audio.copy())

# -----------------------------
# LISTENER THREAD
# -----------------------------
def wake_listener():
    print("[WakeWord] Listening for wake word...")
    last_trigger = 0

    try:
        with sd.InputStream(
            samplerate=INPUT_SR,
            device=DEVICE,
            channels=CHANNELS,
            dtype='float32',
            latency='low',
            blocksize=int(INPUT_SR * DURATION),
            callback=callback
        ):
            while True:
                chunk = q.get()
                if detect_wake_word(chunk):
                    now = time.time()
                    if now - last_trigger > DEBOUNCE_TIME:
                        last_trigger = now
                        print("🔥 Wake word detected!")
                        # Call Echo command listener here
    except Exception as e:
        print(f"[WakeWord] Error opening stream: {e}")

# -----------------------------
# RUN LISTENER
# -----------------------------
if __name__ == "__main__":
    threading.Thread(target=wake_listener, daemon=True).start()
    while True:
        time.sleep(1)