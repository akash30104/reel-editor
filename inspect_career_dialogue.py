import subprocess
import whisper

model = whisper.load_model("base")

# Test segments around 235s to 310s
slices = [
    (236.0, 244.0),
    (244.0, 252.0),
    (252.0, 260.0),
    (260.0, 270.0),
    (270.0, 280.0),
    (280.0, 290.0),
    (290.0, 305.0),
]

for s, e in slices:
    tmp_wav = "tmp_slice.wav"
    subprocess.run(["ffmpeg", "-y", "-ss", str(s), "-to", str(e), "-i", "RAW VIDEOS/1205 2k.mp4", "-vn", "-ar", "16000", "-ac", "1", tmp_wav], capture_output=True)
    res = model.transcribe(tmp_wav, language="ta", initial_prompt="Career vs Relationship வேலை காதல் பணம் வெற்றி")
    txt = " ".join([seg['text'] for seg in res['segments']]).strip()
    print(f"[{s:05.1f}s - {e:05.1f}s]: {txt}")
