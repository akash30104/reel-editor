import subprocess
from PIL import Image
import numpy as np

# Load speech segments
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

speakers = []
for i, (s, e, dur) in enumerate(speech_segs[:32]):
    mid = (s + e) / 2.0
    t1 = mid - 0.15
    t2 = mid + 0.15
    subprocess.run(["ffmpeg", "-y", "-ss", f"{t1:.2f}", "-i", "RAW VIDEOS/1205 2k.mp4", "-vframes", "1", "t1.jpg"], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-ss", f"{t2:.2f}", "-i", "RAW VIDEOS/1205 2k.mp4", "-vframes", "1", "t2.jpg"], capture_output=True)
    
    a1 = np.array(Image.open("t1.jpg"), dtype=float)
    a2 = np.array(Image.open("t2.jpg"), dtype=float)
    diff = np.abs(a1 - a2)
    
    # Left half: x=100..1000, y=100..700 (Spk 1 face/torso)
    left_diff = diff[100:700, 100:1000].mean()
    # Right half: x=1300..2300, y=100..700 (Spk 2 face/torso)
    right_diff = diff[100:700, 1300:2300].mean()
    
    spk = 1 if left_diff > right_diff * 1.1 else 2
    speakers.append((i+1, s, e, dur, spk, left_diff, right_diff))
    print(f"Seg {i+1:02d}: [{s:05.2f}s - {e:05.2f}s] ({dur:04.2f}s) -> Speaker {spk} (L: {left_diff:.2f}, R: {right_diff:.2f})")

