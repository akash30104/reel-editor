#!/usr/bin/env python3
"""
Transcribe full IMG_6596_audio_16k.wav (41 mins) using Whisper
Saves full segment timestamps to 6596_full_transcript.json
"""

import os
import sys
import json
import time
from pathlib import Path

os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
import torch
import whisper

AUDIO_FILE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor/IMG_6596_audio_16k.wav")
OUTPUT_JSON = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor/6596_full_transcript.json")

def main():
    print(f"🎙️ Starting full Whisper transcription of {AUDIO_FILE}...")
    torch.set_num_threads(8)
    
    t0 = time.time()
    model = whisper.load_model("base", device="cpu")
    print(f"Loaded whisper 'base' in {time.time() - t0:.2f}s")
    
    t1 = time.time()
    result = model.transcribe(
        str(AUDIO_FILE),
        language="ta",
        fp16=False,
        word_timestamps=False,
        initial_prompt="Lokesh bro, Ganesh, startup, student entrepreneur, business, private limited"
    )
    print(f"✅ Transcription complete in {time.time() - t1:.2f}s")
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to {OUTPUT_JSON} ({len(result.get('segments', []))} segments)")

if __name__ == "__main__":
    main()
