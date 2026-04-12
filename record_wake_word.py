import sounddevice as sd
import numpy as np
import librosa
import soundfile as sf
import os

# -----------------------------
# CONFIG
# -----------------------------
DEVICE = 9               # Your microphone device index
INPUT_SR = 48000         # Native mic rate
TARGET_SR = 16000        # MFCC target rate
CHANNELS = 1
DURATION = 2.0           # seconds per sample
OUTPUT_DIR = "wake_samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def record_sample(filename):
    print(f"🎤 Recording {filename} for {DURATION} seconds...")
    audio = sd.rec(int(INPUT_SR * DURATION), samplerate=INPUT_SR, channels=CHANNELS, dtype='float32', device=DEVICE)
    sd.wait()
    
    # Flatten mono channel if necessary
    audio = audio[:, 0] if audio.ndim > 1 else audio
    
    # Resample to 16k for MFCC
    audio_16k = librosa.resample(audio, orig_sr=INPUT_SR, target_sr=TARGET_SR)
    
    # Save
    sf.write(os.path.join(OUTPUT_DIR, filename), audio_16k, TARGET_SR)
    print(f"✅ Saved {filename} at {TARGET_SR} Hz")

# -----------------------------
# RECORD MULTIPLE SAMPLES
# -----------------------------
for i in range(1, 6):  # record 5 samples
    input(f"\nPress Enter and say 'echo' for sample {i}...")
    record_sample(f"echo{i}.wav")