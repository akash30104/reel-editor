import subprocess
import whisper
import os

model = whisper.load_model("small")

clips = [
    (70, 100, "70-100s"),
    (130, 160, "130-160s"),
    (190, 220, "190-220s"),
    (250, 280, "250-280s"),
    (310, 340, "310-340s"),
    (370, 400, "370-400s"),
]

for s, e, label in clips:
    tmp = "tmp_inspect.wav"
    subprocess.run(["ffmpeg", "-y", "-ss", str(s), "-to", str(e), "-i", "RAW VIDEOS/1205 2k.mp4", "-vn", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", tmp], capture_output=True)
    res = model.transcribe(tmp, language="ta", fp16=False)
    txt = res['text'].strip()
    print(f"=== {label} ===", flush=True)
    print(txt, flush=True)
    print("", flush=True)
    if os.path.exists(tmp):
        os.remove(tmp)
