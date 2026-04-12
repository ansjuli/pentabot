# main.py – Echo Core Offline Vosk-only

import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
from core.router import route
from core.tts import speak
from pathlib import Path

EXIT_WORDS = ["exit", "quit", "stop"]
SAMPLE_RATE = 16000
q = queue.Queue()

# Load Vosk model
print("[Echo] Loading Vosk model...")
model = Model("models/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
print("[Echo] Ready ✅")

# Vosk queue callback
def vosk_callback(indata, frames, time, status):
    if status:
        print(f"[SD] {status}")
    q.put(bytes(indata))

# Command loop
def vosk_loop():
    print("[Echo] Listening continuously for commands...")
    local_recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    while True:
        data = q.get()
        if local_recognizer.AcceptWaveform(data):
            result = json.loads(local_recognizer.Result())
            text = result.get("text", "").lower().strip()
            if not text:
                continue

            print(f"[Command Heard]: {text}")
            if any(word in text for word in EXIT_WORDS):
                speak("Okay, exiting.")
                break

            response = route(text)
            if response:
                speak(response)
            else:
                speak("I did not understand.")

# Run everything
if __name__ == "__main__":
    print("[Echo] Starting offline listener...")
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=vosk_callback
    ):
        vosk_loop()