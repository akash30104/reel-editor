import subprocess
import whisper
import os

model = whisper.load_model("tiny")

# Sample 15s in the middle of each minute
samples = [
    (15, 30, "0-60s"),
    (75, 90, "60-120s"),
    (135, 150, "120-180s"),
    (195, 210, "180-240s"),
    (255, 270, "240-300s"),
    (315, 330, "300-360s"),
    (375, 390, "360-420s"),
    (435, 450, "420-467s"),
]

for s, e, label in samples:
    tmp = f"sample_{s}_{e}.wav"
    subprocess.run(["ffmpeg", "-y", "-ss", str(s), "-to", str(e), "-i", "RAW VIDEOS/1205 2k.mp4", "-vn", "-ar", "16000", "-ac", "1", tmp], capture_output=True)
    # English translation gives us the meaning
    res_en = model.transcribe(tmp, task="translate")
    # Tamil gives us the spoken words
    res_ta = model.transcribe(tmp, language="ta")
    en = res_en['text'].strip()
    ta = res_ta['text'].strip()
    print(f"=== {label} [{s}s - {e}s] ===", flush=True)
    print(f"  EN: {en}", flush=True)
    print(f"  TA: {ta}", flush=True)
    print("", flush=True)
    if os.path.exists(tmp):
        os.remove(tmp)
