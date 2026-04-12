# wake_test.py – Vosk-only wake word test

import sounddevice as sd
import numpy as np
import queue
import json
from vosk import Model, KaldiRecognizer
from pathlib import Path
from core.router import route
from core.tts import speak

# -----------------------------
# Configuration
# -----------------------------
SAMPLE_RATE = 16000
BLOCK_SIZE = 8000
MIN_RMS_THRESHOLD = 500
EXIT_WORDS = ["exit", "quit", "stop"]

q = queue.Queue()

# -----------------------------
# Load Vosk model
# -----------------------------
print("[WakeTest] Loading Vosk model...")
model = Model("models/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
print("[WakeTest] Ready ✅")

# -----------------------------
# Helpers
# -----------------------------
def normalize(text):
    return text.lower().strip()

def log_failed(text):
    FAILED_LOG_FILE = Path("modules/system/failed_commands.json")
    FAILED_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if FAILED_LOG_FILE.exists():
        with open(FAILED_LOG_FILE, "r", encoding="utf-8") as f:
            failed_log = json.load(f)
    else:
        failed_log = []

    if text not in failed_log:
        failed_log.append(text)
        with open(FAILED_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(failed_log, f, indent=2)

def is_speech(data, threshold=MIN_RMS_THRESHOLD):
    audio = np.frombuffer(data, dtype=np.int16)
    rms = np.sqrt(np.mean(audio ** 2))
    return rms > threshold

# -----------------------------
# Command loop (used as wake test)
# -----------------------------
def wake_test_loop():
    print("[WakeTest] Listening continuously... say your wake word!")
    local_recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    while True:
        data = q.get()
        if not is_speech(data):
            continue

        if local_recognizer.AcceptWaveform(data):
            result = json.loads(local_recognizer.Result())
            text = normalize(result.get("text", ""))
            if not text:
                continue

            print(f"[Detected]: {text}")
            if any(word in text for word in EXIT_WORDS):
                speak("Exiting wake test.")
                break

            # Route text to your main router
            handled = route(text)
            if handled:
                speak(f"Executed: {text}")
            else:
                speak("Did not match any command.")
                log_failed(text)

# -----------------------------
# Audio callback
# -----------------------------
def vosk_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    print("[WakeTest] Starting microphone input...")
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype='int16',
        channels=1,
        callback=vosk_callback
    ):
        wake_test_loop()