#!/usr/bin/env python3
"""
Transcribe 202.MOV Audio using Whisper on CPU (Multi-threaded)
Extracts segment-level timestamps [start, end, text] across the full 37 minutes.
"""

import os
import sys
import json
import time
from pathlib import Path

os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
import torch
import whisper

AUDIO_FILE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor/202_audio_16k.wav")
OUTPUT_JSON = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor/202_transcript.json")

def main():
    print("=" * 60)
    print("🎙️ STARTING WHISPER TRANSCRIPTION (CPU MULTI-THREADED 8 CORES)")
    print(f"Audio Source: {AUDIO_FILE} ({AUDIO_FILE.stat().st_size / (1024*1024):.2f} MB)")
    print("=" * 60)

    torch.set_num_threads(8)
    print(f"⚡ CPU Threads: {torch.get_num_threads()}")

    t0 = time.time()
    print("Loading whisper model 'base'...")
    model = whisper.load_model("base", device="cpu")
    print(f"Model loaded in {time.time() - t0:.2f}s")

    t_trans = time.time()
    print("Transcribing 37-minute Tamil audio...")
    result = model.transcribe(
        str(AUDIO_FILE),
        language="ta",
        fp16=False,
        word_timestamps=False,
        initial_prompt="தமிழ் பாட்காஸ்ட் பேட்டி, உறவுகள், காதல், திருமணம், குடும்பம்"
    )
    duration = time.time() - t_trans
    print(f"✅ Full transcription complete in {duration:.2f}s ({duration/60:.2f} mins)!")

    segments = result.get("segments", [])
    print(f"Total segments extracted: {len(segments)}")

    # Save to JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"💾 Full transcript saved to {OUTPUT_JSON}")

    # Summary of first 15 segments
    print("\n--- SAMPLE SEGMENTS (First 15) ---")
    for seg in segments[:15]:
        print(f"[{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}")

if __name__ == "__main__":
    main()
