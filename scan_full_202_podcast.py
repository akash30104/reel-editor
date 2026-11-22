#!/usr/bin/env python3
"""
Scan 202.MOV across all 37 minutes using Whisper large-v3-turbo to extract:
1. True podcast topic & narrative arc
2. The exact Tamil dialogue spoken by Host and Guest
3. High-tension emotional moments for the 8 viral reels
4. Full chapter breakdown for the Raj Shamani style landscape full episode
"""

import os
os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
import whisper
import json
import time
from pathlib import Path

AUDIO_PATH = "/Users/pgi/.gemini/antigravity/scratch/reel-editor/202_audio_16k.wav"
OUTPUT_SCAN = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor/202_full_scan.json")

def main():
    print("Loading large-v3-turbo...")
    t0 = time.time()
    model = whisper.load_model("turbo")
    print(f"Model loaded in {time.time() - t0:.2f}s")

    # Sample windows across the entire 37-minute video (every 2.5 minutes, 40s duration)
    timestamps = [
        (60, 45, "01:00 - Intro & Topic Setting"),
        (150, 45, "02:30 - Early Debate"),
        (270, 45, "04:30 - Discussion Point 1"),
        (420, 45, "07:00 - Discussion Point 2"),
        (570, 45, "09:30 - Core Conflict"),
        (720, 45, "12:00 - Deep Philosophy"),
        (870, 45, "14:30 - Example Story"),
        (1020, 45, "17:00 - Emotional Peak 1"),
        (1200, 45, "20:00 - Perspective Clash"),
        (1380, 45, "23:00 - Mindset Shift"),
        (1560, 45, "26:00 - Relationship Dynamics"),
        (1740, 45, "29:00 - Real Life Realization"),
        (1920, 45, "32:00 - Core Life Lesson"),
        (2100, 45, "35:00 - Final Climax & Conclusion"),
    ]

    results = []

    for st, dur, label in timestamps:
        chunk_wav = f"/Users/pgi/.gemini/antigravity/scratch/reel-editor/chunk_{st}.wav"
        os.system(f"/Users/pgi/.local/bin/ffmpeg -y -ss {st} -t {dur} -i '{AUDIO_PATH}' -c:a pcm_s16le '{chunk_wav}' -loglevel error")
        
        t_start = time.time()
        res = model.transcribe(chunk_wav, language="ta")
        elapsed = time.time() - t_start
        text = res["text"].strip()
        print(f"\n[{label}] ({elapsed:.1f}s):")
        print(f"Tamil: {text}")

        # Also store segments with word timestamps if possible
        results.append({
            "st": st,
            "dur": dur,
            "label": label,
            "text": text,
            "segments": res["segments"]
        })

    with open(OUTPUT_SCAN, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Scan saved to {OUTPUT_SCAN}")

if __name__ == "__main__":
    main()
