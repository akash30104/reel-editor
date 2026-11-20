import subprocess
import re
import json

# Read silence output
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

print(f"Total speech segments detected: {len(speech_segs)}")

# Print out segments up to 120s
cumulative = 0.0
for i, (s, e, dur) in enumerate(speech_segs):
    cumulative += dur
    print(f"[{i+1:02d}] Raw: {s:06.2f}s - {e:06.2f}s (Dur: {dur:04.2f}s) | Total: {cumulative:06.2f}s")
    if cumulative >= 90.0:
        break
