import subprocess
import os
from PIL import Image
import numpy as np

# Load the speech segments
import re
with open(r'C:\Users\91861\.gemini\antigravity\brain\821c98cc-7767-421b-b10e-3565795f6465\.system_generated\steps\1108\output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

starts = [float(x) for x in re.findall(r'silence_start:\s*([0-9.]+)', text)]
ends = [float(x) for x in re.findall(r'silence_end:\s*([0-9.]+)', text)]
silences = list(zip(starts, ends))
pad = 0.08

speech_segs = []
cur_start = 0.0
for s_start, s_end in silences:
    seg_end = s_start + pad
    seg_start = cur_start
    if seg_end - seg_start > 0.4:
        speech_segs.append((seg_start, seg_end, seg_end - seg_start))
    cur_start = s_end - pad

print(f"Total speech segments: {len(speech_segs)}")

# Let's inspect who is speaking by sampling 1 frame in the middle of each segment
# Speaker 1 is on Left: x=0..1280. Has striped shirt + green lanyard.
# Speaker 2 is on Right: x=1280..2560. Has light blue shirt.
os.makedirs("seg_frames", exist_ok=True)

seg_speakers = []
for i, (s, e, dur) in enumerate(speech_segs[:40]):
    mid = (s + e) / 2.0
    out_jpg = f"seg_frames/seg_{i+1:02d}.jpg"
    subprocess.run(["ffmpeg", "-y", "-ss", f"{mid:.2f}", "-i", "RAW VIDEOS/1205 2k.mp4", "-vframes", "1", "-q:v", "3", out_jpg], capture_output=True)
    
    # check motion or mouth or head position
    im = Image.open(out_jpg)
    # let's determine based on who is gesturing / facing camera
    # We can print segment details
    print(f"Seg {i+1:02d}: [{s:05.2f}s - {e:05.2f}s] (dur: {dur:04.2f}s)")

