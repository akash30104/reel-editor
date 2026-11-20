import whisper
import json

model = whisper.load_model("base")

for name in ["120_180", "180_240", "240_300"]:
    wav = f"audio_topics/chunk_{name}.wav"
    res = model.transcribe(wav, language="ta", initial_prompt="வாழ்க்கை காதல் வேலை தொழில் வெற்றி பணம் சமரசம் உறவு")
    print(f"=== CHUNK {name} ===")
    for seg in res['segments']:
        s = seg['start']
        e = seg['end']
        t = seg['text']
        print(f"[{s:05.2f} - {e:05.2f}]: {t}")
    print()
