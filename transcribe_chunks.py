import whisper
import subprocess
import os

model = whisper.load_model("tiny")

# Test key clips
clips_to_test = [
    (33.9, 37.9, "Hook"),
    (38.6, 44.6, "Drama"),
    (44.9, 49.1, "Reason 1"),
    (52.7, 58.8, "Reason 2"),
    (68.4, 74.6, "Reason 3"),
    (79.7, 86.4, "Life lesson"),
    (86.7, 96.7, "Solution"),
    (99.9, 106.5, "Conclusion"),
]

for s, e, desc in clips_to_test:
    tmp_wav = "tmp_slice.wav"
    subprocess.run(["ffmpeg", "-y", "-ss", str(s), "-to", str(e), "-i", "RAW VIDEOS/1205 2k.mp4", "-vn", "-ar", "16000", "-ac", "1", tmp_wav], capture_output=True)
    # transcribe English translation first to understand meaning
    res_en = model.transcribe(tmp_wav, task="translate")
    txt_en = " ".join([seg['text'] for seg in res_en['segments']]).strip()
    # transcribe Tamil
    res_ta = model.transcribe(tmp_wav, language="ta")
    txt_ta = " ".join([seg['text'] for seg in res_ta['segments']]).strip()
    print(f"[{s:05.1f}s - {e:05.1f}s] ({desc}):")
    print(f"  EN: {txt_en}")
    print(f"  TA: {txt_ta}\n")

if os.path.exists("tmp_slice.wav"):
    os.remove("tmp_slice.wav")
