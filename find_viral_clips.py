#!/usr/bin/env python3
"""
Find Viral Content Clips from full_202_podcast_transcript.json
Target duration per clip: 68s to 78s (1min to 1:20min).
Identifies top viral story arcs with emotional tension, debate, and profound life lessons.
"""

import json
import os
import re

TRANSCRIPT_PATH = "/Users/pgi/.gemini/antigravity/scratch/reel-editor/full_202_podcast_transcript.json"

VIRAL_KEYWORDS = [
    # Story & Characters
    "ராவணன்", "சீதை", "ராமர்", "குகன்", "சுக்கிரீவன்", "அனுமன்", "கம்பர்", "வால்மீகி", 
    "பெயிண்டிங்", "ராஜா ரவிவர்மா", "தசரதன்", "லட்சுமணன்", "விபீஷணன்", "இலங்கை", "வனவாசம்",
    # Psychological & Life Lessons
    "பாடம்", "வாழ்க்கை", "தப்பு", "உண்மை", "நட்பு", "அன்பு", "தியாகம்", "கர்மா", "ஈகோ", 
    "தலைக்கனம்", "தோல்வி", "வெற்றி", "மனசு", "குணம்", "பணம்", "துரோகம்", "நம்பிக்கை"
]

def analyze_transcript():
    if not os.path.exists(TRANSCRIPT_PATH):
        print(f"Error: {TRANSCRIPT_PATH} not found yet!")
        return

    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    print(f"Loaded {len(segments)} segments across {segments[-1]['end']:.1f}s.")

    # Search for contiguous windows of 68s to 78s with high viral keyword density & conversational flow
    target_min_dur = 68.0
    target_max_dur = 78.0

    candidates = []

    for i in range(len(segments)):
        st = segments[i]["start"]
        curr_text = []
        for j in range(i, len(segments)):
            seg = segments[j]
            curr_text.append(seg["text"].strip())
            dur = seg["end"] - st
            if target_min_dur <= dur <= target_max_dur:
                full_str = " ".join(curr_text)
                # Count keywords
                score = sum(full_str.count(kw) for kw in VIRAL_KEYWORDS)
                candidates.append({
                    "start": st,
                    "end": seg["end"],
                    "duration": dur,
                    "score": score,
                    "text": full_str,
                    "first_line": curr_text[0] if curr_text else "",
                    "segments": segments[i:j+1]
                })
            elif dur > target_max_dur:
                break

    # Sort by score
    candidates.sort(key=lambda x: x["score"], reverse=True)

    # Filter non-overlapping candidates
    selected = []
    for cand in candidates:
        if all(abs(cand["start"] - s["start"]) > 80.0 for s in selected):
            selected.append(cand)
            if len(selected) >= 8:
                break

    print("\n" + "="*70)
    print(f"🔥 TOP {len(selected)} VIRAL CONTENT CLIPS (Target: 1min - 1:20min)")
    print("="*70)

    for idx, s in enumerate(selected, 1):
        print(f"\n🎬 CLIP {idx}: {s['start']:.1f}s - {s['end']:.1f}s (Dur: {s['duration']:.1f}s, Score: {s['score']})")
        print(f"   🎯 Hook Line: \"{s['first_line']}\"")
        print(f"   📜 Full Text:\n   {s['text'][:250]}...")

    # Save candidates to file
    out_file = "/Users/pgi/.gemini/antigravity/scratch/reel-editor/viral_clips_candidates.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Saved candidates to {out_file}")

if __name__ == "__main__":
    analyze_transcript()
