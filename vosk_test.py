# vosk_test_fixed.py – simple microphone recognition test

import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

SAMPLE_RATE = 16000

# Load Vosk model
print("[Test] Loading Vosk model...")
model = Model("models/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
print("[Test] Ready. Speak something!")

def callback(indata, frames, time, status):
    if status:
        print("[SD Status]:", status)
    # Convert buffer directly to bytes for Vosk
    data = bytes(indata)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")
        if text:
            print(f"[Recognized]: {text}")

# Open mic stream
with sd.RawInputStream(samplerate=SAMPLE_RATE,
                       blocksize=8000,
                       dtype='int16',
                       channels=1,
                       callback=callback):
    print("[Test] Listening... Press Ctrl+C to stop")
    import time
    while True:
        time.sleep(1)