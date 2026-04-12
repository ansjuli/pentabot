import sounddevice as sd
import numpy as np

DEVICE = 9
device_info = sd.query_devices(DEVICE)

SAMPLE_RATE = int(device_info['default_samplerate'])  # ✅ use correct rate
DURATION = 3

print(f"🎤 Using sample rate: {SAMPLE_RATE}")
print("🎤 Speak now...")

audio = sd.rec(
    int(SAMPLE_RATE * DURATION),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype='float32',
    device=DEVICE
)

sd.wait()

print("Max amplitude:", np.max(np.abs(audio)))