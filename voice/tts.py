# core/tts.py – Reliable TTS (no freeze, always speaks)

import pyttsx3
import threading
import queue

speech_queue = queue.Queue()

def speak_once(text):
    try:
        engine = pyttsx3.init()

        # Female voice
        voices = engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)

        print(f"[TTS] Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print(f"[TTS Error]: {e}")

def tts_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        speak_once(text)
        speech_queue.task_done()

# Start worker
threading.Thread(target=tts_worker, daemon=True).start()

def speak(text):
    speech_queue.put(text)