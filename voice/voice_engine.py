import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

model = Model("models/vosk-model-small-en-us-0.15")  # path to vosk model
recognizer = KaldiRecognizer(model, 16000)

audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    audio_queue.put(bytes(indata))

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000,
                          dtype='int16', channels=1, callback=callback):

        print("[Pentabot] Listening...")

        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                return text