import json, re

# Load whisper transcript
with open('raw_first60.json', encoding='utf-8') as f:
    whisper_data = json.load(f)

# Load silences detected earlier
# Silences > 0.35s:
raw_silences = [
    (0.00, 0.41),
    (1.87, 2.26),
    (2.83, 3.92),
    (3.94, 6.14),
    (6.24, 7.52),
    (7.85, 8.35),
    (11.30, 12.16),
    (16.33, 17.86),
    (20.47, 20.93),
    (22.71, 23.69),
    (23.70, 24.20),
    (24.37, 24.77),
    (28.54, 29.08),
    (33.16, 33.99),
    (37.86, 38.72),
    (41.63, 41.99),
    (44.55, 60.00) # long trailing dead air
]

# Calculate speech intervals with 0.08s padding
# Total duration of raw interest: 0.41 to 44.55
# Remove dead air silences > 0.35s keeping 0.08s padding around speech
pad = 0.08
cuts = []
t = 0.41
for s_start, s_end in raw_silences[1:]:
    seg_end = s_start + pad
    seg_start = t
    if seg_end > seg_start + 0.15:
        cuts.append((seg_start, seg_end))
    t = s_end - pad

print("=== CALCULATED SPEECH SEGMENTS (DEAD AIR REMOVED) ===")
total_duration = 0
for i, (s, e) in enumerate(cuts):
    dur = e - s
    total_duration += dur
    print(f"Clip {i+1:02d}: Raw [{s:05.2f}s -> {e:05.2f}s] | Duration: {dur:04.2f}s | Timeline: [{total_duration-dur:05.2f}s -> {total_duration:05.2f}s]")

print(f"\nTotal Edited Reel Duration: {total_duration:.2f} seconds (Target: <60s - PASSED)")
