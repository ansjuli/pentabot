# listener.py – Optional fallback listener
import speech_recognition as sr
from core.router import route
from core.tts import speak
import re
import time

EXIT_WORDS = ["exit", "quit", "stop"]

def clean_text(text):
    # basic filler removal
    fillers = ["uh", "um", "ah", "hmm", "like", "so", "well"]
    for f in fillers:
        text = text.replace(f, "")
    text = re.sub(r'\s+', " ", text).strip()
    return text.lower()

def fallback_listen():
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("[Echo] Fallback listener active...")

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=2)

    while True:
        try:
            with mic as source:
                audio = r.listen(source, timeout=None, phrase_time_limit=6)

            result = r.recognize_google(audio, show_all=True)
            if not result or "alternative" not in result:
                continue

            best_text = result["alternative"][0]["transcript"]
            best_text = clean_text(best_text)

            if any(word in best_text for word in EXIT_WORDS):
                speak("Okay, exiting fallback listener.")
                break

            handled = route(best_text)
            if handled:
                speak(f"Executed: {best_text}")
            else:
                speak("I did not understand.")

        except Exception as e:
            print(f"[Fallback Listener error]: {e}")
            time.sleep(1)
            continue