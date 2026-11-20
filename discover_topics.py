import whisper
import os

model = whisper.load_model("tiny")

chunks = [
    (120, 180),
    (180, 240),
    (240, 300),
    (300, 360),
    (360, 420),
    (420, 467),
]

for s, e in chunks:
    wav = f"audio_topics/chunk_{s}_{e}.wav"
    res = model.transcribe(wav, task="translate")
    text = " ".join([seg['text'] for seg in res['segments']]).strip()
    print(f"=== CHUNK [{s}s - {e}s] ===")
    print(f"{text}\n")
