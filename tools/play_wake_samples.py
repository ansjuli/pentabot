# tools/play_wake_samples.py
import sounddevice as sd
import soundfile as sf
import os

WAKE_SAMPLES_DIR = "wake_samples"
SAMPLE_RATE = 16000

files = [f for f in os.listdir(WAKE_SAMPLES_DIR) if f.endswith(".wav")]

for i, file in enumerate(files, 1):
    path = os.path.join(WAKE_SAMPLES_DIR, file)
    print(f"\n🎧 Playing sample {i}: {file}")
    data, sr = sf.read(path, dtype='float32')
    sd.play(data, samplerate=sr)
    sd.wait()  # wait until finished