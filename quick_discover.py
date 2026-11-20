import subprocess
import whisper
import os

model = whisper.load_model("base")

spots = [
    (130, 145),
    (180, 195),
    (240, 255),
    (310, 325),
    (370, 385),
    (420, 435),
]

for s, e in spots:
    wav = f"spot_{s}_{e}.wav"
    subprocess.run(["ffmpeg", "-y", "-ss", str(s), "-to", str(e), "-i", "RAW VIDEOS/1205 2k.mp4", "-vn", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav], capture_output=True)
    res = model.transcribe(wav, language="ta", fp16=False)
    txt = res['text'].strip()
    print(f"[{s}s - {e}s]: {txt}", flush=True)
    if os.path.exists(wav):
        os.remove(wav)
