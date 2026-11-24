import whisper
import json
from pathlib import Path

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
AUDIO_FILE = WORKSPACE / "IMG_4246_audio_16k.wav"

# 11 Segments definition
segments_meta = [
    # --- Ref5 Reels 2 to 6 ---
    {"id": "ref5_reel2", "name": "Modern Dating Trap", "start": 545.0, "dur": 45.0},
    {"id": "ref5_reel3", "name": "Physical vs Mental Attraction", "start": 745.0, "dur": 45.0},
    {"id": "ref5_reel4", "name": "Influencer vs Influential", "start": 895.0, "dur": 45.0},
    {"id": "ref5_reel5", "name": "Are Influencers Living Real Life", "start": 1045.0, "dur": 45.0},
    {"id": "ref5_reel6", "name": "Losing Independence & Integrity", "start": 1640.0, "dur": 45.0},

    # --- Ref11 Reels 1 to 6 ---
    {"id": "ref11_reel1", "name": "Chemistry Of Love", "start": 131.9, "dur": 48.0},
    {"id": "ref11_reel2", "name": "Sleeping With Peace", "start": 180.0, "dur": 45.0},
    {"id": "ref11_reel3", "name": "Love Of My Life Trap", "start": 445.0, "dur": 45.0},
    {"id": "ref11_reel4", "name": "True Power of Influence", "start": 900.0, "dur": 45.0},
    {"id": "ref11_reel5", "name": "Escaping Toxic Circles", "start": 1495.0, "dur": 45.0},
    {"id": "ref11_reel6", "name": "Friendship Hard Breaks", "start": 1530.0, "dur": 45.0},
]

print("Loading Whisper model...")
model = whisper.load_model("base")
audio = whisper.load_audio(str(AUDIO_FILE))
sr = 16000

catalog = {}
for seg in segments_meta:
    sid = seg["id"]
    st = seg["start"]
    en = st + seg["dur"]
    print(f"Transcribing {sid}: {st}s to {en}s...")
    chunk = audio[int(st*sr) : int(en*sr)]
    res = model.transcribe(chunk, language="en", word_timestamps=True, fp16=False)
    
    # adjust word timestamps relative to video start
    words_adjusted = []
    for s in res["segments"]:
        for w in s.get("words", []):
            words_adjusted.append({
                "word": w["word"].strip(),
                "start": round(st + w["start"], 3),
                "end": round(st + w["end"], 3),
                "rel_start": round(w["start"], 3),
                "rel_end": round(w["end"], 3),
            })
            
    full_text = " ".join([s["text"].strip() for s in res["segments"]])
    catalog[sid] = {
        "meta": seg,
        "full_text": full_text,
        "words": words_adjusted,
        "segments": res["segments"]
    }
    print(f"[{sid}] {full_text[:90]}...\n")

out_file = WORKSPACE / "transcriptions_11_reels.json"
with open(out_file, "w") as f:
    json.dump(catalog, f, indent=2)

print(f"Saved complete word-level transcriptions to {out_file}")
