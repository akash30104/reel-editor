import whisper
import json

model = whisper.load_model("base")
audio = whisper.load_audio("/Users/pgi/.gemini/antigravity/scratch/reel-editor/IMG_4246_audio_16k.wav")
sr = 16000

chunk = audio[int(123*sr) : int(205*sr)]
res = model.transcribe(chunk, language="en", word_timestamps=True, fp16=False)

words_data = []
for seg in res["segments"]:
    s_st = seg["start"] + 123
    s_et = seg["end"] + 123
    s_txt = seg["text"]
    print(f"\n--- [{s_st:.2f} - {s_et:.2f}] {s_txt} ---")
    for w in seg.get("words", []):
        w_word = w["word"].strip()
        w_st = round(w["start"] + 123, 2)
        w_et = round(w["end"] + 123, 2)
        w_obj = {
            "word": w_word,
            "start": w_st,
            "end": w_et
        }
        words_data.append(w_obj)
        print(f"  {w_word}: {w_st} -> {w_et}")

with open("/Users/pgi/.gemini/antigravity/scratch/reel-editor/ref5_raw_words.json", "w") as f:
    json.dump(words_data, f, indent=2)
print("\nSaved ref5_raw_words.json")
