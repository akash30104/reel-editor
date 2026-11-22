#!/usr/bin/env python3
"""
Verify and transcribe the 8 exact topics from 202.MOV corresponding to
'Relationship Truths Nobody Tells You: Love, Trust, Cheating & Breakups'
"""

import os
os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
import whisper
import json
from pathlib import Path

AUDIO_PATH = "/Users/pgi/.gemini/antigravity/scratch/reel-editor/202_audio_16k.wav"

TOPIC_CANDIDATES = [
    {"id": 1, "name": "Options Syndrome", "st": 320, "dur": 25, "prompt": "Options, dating, relationship, commitment, choose"},
    {"id": 2, "name": "3 Cs Communication", "st": 440, "dur": 25, "prompt": "Communication, care, commitment, 3 Cs, relationship"},
    {"id": 3, "name": "Changing Yourself", "st": 850, "dur": 25, "prompt": "Change, sacrifice, partner, love, identity"},
    {"id": 4, "name": "Phone Passwords", "st": 1050, "dur": 25, "prompt": "Password, phone, privacy, social media, trust, check"},
    {"id": 5, "name": "Location Tracking", "st": 1250, "dur": 25, "prompt": "Location tracking, care, doubt, insecurity, freedom"},
    {"id": 6, "name": "Red Flags & Walk Away", "st": 1500, "dur": 25, "prompt": "Red flags, walk away, toxic, breakup, respect"},
    {"id": 7, "name": "Losing Interest", "st": 1620, "dur": 25, "prompt": "Losing interest, distance, reply, call, priority"},
    {"id": 8, "name": "Taking Back Ex", "st": 1760, "dur": 25, "prompt": "Ex, breakup, second chance, patch up, trust, mistake"}
]

def main():
    print("Loading Whisper model...")
    model = whisper.load_model("small")

    results = {}
    for c in TOPIC_CANDIDATES:
        out_wav = f"/Users/pgi/.gemini/antigravity/scratch/reel-editor/cand_{c['id']}.wav"
        os.system(f"/Users/pgi/.local/bin/ffmpeg -y -ss {c['st']} -t {c['dur']} -i '{AUDIO_PATH}' -c:a pcm_s16le '{out_wav}' -loglevel error")
        
        res = model.transcribe(
            out_wav,
            language="ta",
            beam_size=5,
            condition_on_previous_text=False,
            initial_prompt=f"தமிழ் பாட்காஸ்ட், Laven Lokesh, {c['prompt']}"
        )
        print(f"\n==========================================")
        print(f"REEL {c['id']}: {c['name']} (Offset {c['st']}s)")
        print(f"==========================================")
        for s in res["segments"]:
            st = s["start"] + c["st"]
            et = s["end"] + c["st"]
            txt = s["text"].strip()
            print(f"[{st:.2f} - {et:.2f}] {txt}")
        results[c["id"]] = res

    with open("/Users/pgi/.gemini/antigravity/scratch/reel-editor/cand_transcripts.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
