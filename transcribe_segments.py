import whisper
import json

print("Loading tiny model...")
model = whisper.load_model("tiny")

results = {}
for start in range(0, 180, 30):
    wav = f"audio_seg_{start}_{start+30}.wav"
    print(f"Transcribing {wav}...")
    try:
        # transcribing in Tamil with English prompt
        res = model.transcribe(wav, language="ta")
        print(f"--- Seg {start}s - {start+30}s ---")
        for s in res['segments']:
            print(f"[{start + s['start']:.2f} - {start + s['end']:.2f}]: {s['text']}")
        results[f"{start}_{start+30}"] = res
    except Exception as e:
        print(f"Error on {wav}: {e}")

with open("whisper_0_180.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Done!")
