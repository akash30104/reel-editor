import whisper
import json

print("Loading Whisper model 'base'...")
model = whisper.load_model('base')
print("Transcribing raw_0_45.wav in Tamil...")
result = model.transcribe('raw_0_45.wav', language='ta', word_timestamps=True)

with open('whisper_raw_0_45_ta.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\n=== TRANSCRIPTION RESULTS ===")
for seg in result['segments']:
    s = seg['start']
    e = seg['end']
    txt = seg['text']
    print(f"[{s:05.2f} - {e:05.2f}]: {txt}")
