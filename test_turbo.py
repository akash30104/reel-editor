import os
os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
import whisper
import time

print("Loading Whisper large-v3-turbo...")
t0 = time.time()
model = whisper.load_model("turbo")
print(f"Model loaded in {time.time() - t0:.2f}s")

audio_path = "/Users/pgi/.gemini/antigravity/scratch/reel-editor/slice_intro.wav"
print("Transcribing 2-minute intro...")
t1 = time.time()
res = model.transcribe(audio_path, language="ta")
print(f"Done in {time.time() - t1:.2f}s")
print("Detected text:")
for s in res["segments"]:
    print(f"[{s['start']:.2f} - {s['end']:.2f}]: {s['text'].strip()}")
