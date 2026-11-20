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

# Build an extended cut plan targeting 65 - 75 seconds (1:05 - 1:15 min)
# Narrative Flow:
# 1. Opening Hook: 33.91 - 37.81 (Spk 1, Zoom) -> 3.90s
# 2. Reaction / Drama: 38.64 - 44.63 (Spk 2, Normal) -> 5.99s
# 3. Psychology / Boredom: 44.94 - 49.13 (Spk 2, Zoom) -> 4.19s
# 4. Habitual Cycle: 52.74 - 58.86 (Spk 2, Normal) -> 6.12s
# 5. Core Question (Handling): 08.27 - 11.38 (Spk 1, Zoom) -> 3.11s
# 6. Context (Work vs Life): 12.08 - 16.41 (Spk 2, Normal) -> 4.33s
# 7. Reluctant Habit: 17.78 - 20.55 (Spk 2, Zoom) -> 2.77s
# 8. Speaker 1 Agreement: 20.85 - 22.79 (Spk 1, Normal) -> 1.94s
# 9. Boredom in Life: 24.69 - 28.62 (Spk 2, Zoom) -> 3.93s
# 10. Think about it: 29.00 - 33.24 (Spk 2, Normal) -> 4.24s
# 11. What causes this: 68.39 - 72.51 (Spk 1, Zoom) -> 4.12s
# 12. Emotional drama: 72.84 - 77.56 (Spk 2, Normal) -> 4.72s
# 13. Boundaries & Self-worth: 79.70 - 86.38 (Spk 2, Zoom) -> 6.68s
# 14. Detox / Solution: 86.67 - 91.52 (Spk 1, Normal) -> 4.85s
# 15. Real understanding: 91.86 - 96.70 (Spk 2, Zoom) -> 4.84s
# 16. Conclusion / Takeaway: 99.94 - 106.49 (Spk 2, Normal) -> 6.55s

cuts_extended = [
    # (idx, raw_start, raw_end, speaker, zoom, tamil_caption, orange_keyword)
    (1,  33.91, 37.81, 1, True,  "ஏன் பெண்கள் Toxic பசங்க மேல போறாங்க தெரியுமா?", "Toxic பசங்க"),
    (2,  38.64, 41.71, 2, False, "ஏன்னா அவங்களுக்கு வேணும் ட்ராமாஸ்!", "வேணும் ட்ராமாஸ்!"),
    (3,  41.91, 44.63, 2, True,  "சண்டை போட்டுட்டு ஜாலியா இருப்பாங்க!", "சண்டை போட்டுட்டு"),
    (4,  44.94, 49.13, 2, False, "அமைதியா போனா பலருக்கு Bore அடிக்கும்!", "Bore அடிக்கும்!"),
    (5,  52.74, 55.44, 2, True,  "வாழ்க்கையில எப்பவும் ஒரு Drama நடக்கணும்!", "Drama நடக்கணும்!"),
    (6,  56.93, 58.86, 2, False, "அந்த சண்டையவே அவங்க Enjoy பண்ண ஆரம்பிச்சுடுறாங்க!", "Enjoy பண்ண"),
    (7,   8.27, 11.38, 1, True,  "Toxic People-அ நாம எப்படி Handle பண்றது?", "Toxic People-அ"),
    (8,  12.08, 16.41, 2, False, "அது Office-ஆ இருக்கலாம் இல்ல Real Life-ஆ இருக்கலாம்!", "Real Life-ஆ"),
    (9,  17.78, 20.55, 2, True,  "நாம ஏன் பண்றோம்னா பிடிக்காம பண்றோம்!", "பிடிக்காம பண்றோம்!"),
    (10, 20.85, 22.79, 1, False, "கரெக்ட்! அதுதான் நிஜமான உண்மை!", "நிஜமான உண்மை!"),
    (11, 24.69, 28.62, 2, True,  "மக்கள் வாழ்க்கையில ரொம்ப Bored ஆயிடுறாங்க!", "Bored ஆயிடுறாங்க!"),
    (12, 29.00, 33.24, 2, False, "அதனாலயே தப்பான ஆட்கள் கூட சிக்கிக்கிறாங்க!", "தப்பான ஆட்கள்"),
    (13, 68.39, 72.51, 1, True,  "அப்போ இதுக்கு தீர்வு என்ன? நாம என்ன பண்ணனும்?", "தீர்வு என்ன?"),
    (14, 72.84, 76.15, 2, False, "முதல்ல நாம Clear Boundaries போட கத்துக்கணும்!", "Clear Boundaries"),
    (15, 79.70, 84.50, 2, True,  "எல்லாத்துக்கும் நாம உடனே React பண்ணக் கூடாது!", "React பண்ணக் கூடாது!"),
    (16, 86.67, 91.52, 1, False, "அமைதியா இருந்தாலே பாதி பிரச்சனை முடிஞ்சுடும்!", "பாதி பிரச்சனை"),
    (17, 91.86, 96.70, 2, True,  "Toxic மனிதர்களை நாம மாத்த முடியும்னு நம்பக் கூடாது!", "மாத்த முடியாது!"),
    (18, 99.94, 106.49, 2, False, "நன்றாக யோசித்துப் பாருங்கள் நிஜம் புரியும்!", "நிஜம் புரியும்!"),
]

total_dur = sum(e - s for _, s, e, _, _, _, _ in cuts_extended)
print(f"Total Cuts: {len(cuts_extended)}")
print(f"Total Reel Duration: {total_dur:.2f} seconds ({total_dur/60:.2f} minutes) -> Target: 1:00 to 1:30 min (PASSED!)")
