import os
import subprocess
import json
import math

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
RAW_VIDEO = os.path.join(BASE_DIR, "RAW VIDEOS", "1205 2k.mp4")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
BGM_AUDIO = os.path.join(BASE_DIR, "my-video", "assets", "bgm_bed.mp3")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
os.chdir(BASE_DIR)

# 1. Define Cuts (Raw Timestamps, Speaker, and Zoom Framing)
# Speaker 1 = Left (striped shirt, green lanyard)
# Speaker 2 = Right (blue shirt, microphone)
cuts = [
    # idx, start, end, speaker, zoom
    (1,  0.41,  1.95, 2, True),   # 1.54s - Speaker 2 (Hook, 1.15x Zoom)
    (2,  8.27, 11.38, 1, False),  # 3.11s - Speaker 1 (Normal 1.0x)
    (3, 12.08, 14.80, 2, True),   # 2.72s - Speaker 2 (1.15x Zoom)
    (4, 14.80, 17.50, 1, False),  # 2.70s - Speaker 1 (Normal 1.0x)
    (5, 17.78, 20.55, 2, True),   # 2.77s - Speaker 2 (1.15x Zoom)
    (6, 20.85, 22.79, 1, False),  # 1.94s - Speaker 1 (Normal 1.0x)
    (7, 24.69, 27.50, 2, True),   # 2.81s - Speaker 2 (1.15x Zoom)
    (8, 27.50, 30.50, 1, False),  # 3.00s - Speaker 1 (Normal 1.0x)
    (9, 30.50, 33.24, 2, True),   # 2.74s - Speaker 2 (1.15x Zoom)
    (10, 33.91, 37.94, 1, False), # 4.03s - Speaker 1 (Normal 1.0x)
    (11, 38.64, 43.10, 2, True),  # 4.46s - Speaker 2 (1.15x Zoom)
]

print("=== 1. EXTRACTING & CROPPING VIDEO CHUNKS ===")
chunk_files = []
timeline_timestamps = []
current_time = 0.0

for idx, start, end, speaker, zoom in cuts:
    dur = end - start
    timeline_timestamps.append((current_time, current_time + dur, speaker, zoom))
    
    # Framing Crop Logic (2560x1440 -> 1080x1920)
    if speaker == 1:
        if zoom:
            vf = "crop=704:1252:203:40,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p"
        else:
            vf = "crop=810:1440:150:0,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p"
    else: # speaker == 2
        if zoom:
            vf = "crop=704:1252:1653:40,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p"
        else:
            vf = "crop=810:1440:1600:0,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p"

    out_chunk = os.path.join(TEMP_DIR, f"chunk_{idx:02d}.mp4")
    cmd = [
        "ffmpeg", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", RAW_VIDEO,
        "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
        out_chunk, "-y"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    chunk_files.append(out_chunk)
    print(f"Chunk {idx:02d}: Raw [{start:.2f}s - {end:.2f}s] -> Timeline [{current_time:.2f}s - {current_time+dur:.2f}s] (Spk {speaker}, Zoom: {zoom})")
    current_time += dur

total_dur = current_time
print(f"Total Video Duration: {total_dur:.2f} seconds")

# 2. Concat Chunks
print("\n=== 2. CONCATENATING SPEECH TIMELINE ===")
concat_list = os.path.join(TEMP_DIR, "concat.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for c in chunk_files:
        f.write(f"file '{c}'\n")

raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat.mp4")
cmd_concat = [
    "ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_list,
    "-c", "copy", raw_concat_mp4, "-y"
]
subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Concatenation complete!")

# 3. Build ASS Subtitle File
print("\n=== 3. GENERATING TAMIL ASS SUBTITLES ===")
ass_file = os.path.join(BASE_DIR, "tamil_reel.ass")

def fmt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

captions_data = [
    (timeline_timestamps[0][0], timeline_timestamps[0][1], "எல்லா முறையும் {\\c&H0000E6FF&}பழகுவது{\\c&H00FFFFFF&} எப்படி?"),
    (timeline_timestamps[1][0], timeline_timestamps[1][1], "நிகழ்ச்சியை {\\c&H0000E6FF&}தொடங்குவோம்{\\c&H00FFFFFF&} வாருங்கள்!"),
    (timeline_timestamps[2][0], timeline_timestamps[2][1], "மக்கள் அனைவரும் {\\c&H0000E6FF&}ஆவலுடன்{\\c&H00FFFFFF&} காத்திருக்கிறார்கள்."),
    (timeline_timestamps[3][0], timeline_timestamps[3][1], "இப்போது நாம் {\\c&H0000E6FF&}நேரடியாகப்{\\c&H00FFFFFF&} பார்க்கிறோம்."),
    (timeline_timestamps[4][0], timeline_timestamps[4][1], "ஏன் இந்த {\\c&H0000E6FF&}மாற்றம்{\\c&H00FFFFFF&} வந்தது?"),
    (timeline_timestamps[5][0], timeline_timestamps[5][1], "நாடகம் போல {\\c&H0000E6FF&}விறுவிறுப்பு{\\c&H00FFFFFF&} இருக்கும்!"),
    (timeline_timestamps[6][0], timeline_timestamps[6][1], "நல்ல {\\c&H0000E6FF&}ஜாலியாக{\\c&H00FFFFFF&} பேசலாம் வாங்க."),
    (timeline_timestamps[7][0], timeline_timestamps[7][1], "சண்டை இல்லாமல் {\\c&H0000E6FF&}மகிழ்ச்சியாக{\\c&H00FFFFFF&} இருக்கும்."),
    (timeline_timestamps[8][0], timeline_timestamps[8][1], "அடுத்து நடக்கப் போவது {\\c&H0000E6FF&}விறுவிறுப்பான{\\c&H00FFFFFF&} காட்சி!"),
    (timeline_timestamps[9][0], timeline_timestamps[9][1], "நிச்சயமாக இதை {\\c&H0000E6FF&}முழுமையாகப்{\\c&H00FFFFFF&} பாருங்கள்!"),
    (timeline_timestamps[10][0], timeline_timestamps[10][1], "தொடருங்கள் எங்களை {\\c&H0000E6FF&}சப்ஸ்கிரைப்{\\c&H00FFFFFF&} செய்யுங்கள்! 🚀"),
]

with open(ass_file, "w", encoding="utf-8") as f:
    f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans Tamil,54,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,40,40,320,1
Style: HookTitle,Noto Sans Tamil,64,&H00FFFFFF,&H000000FF,&H000782EA,&H80000000,-1,0,0,0,100,100,0,0,1,7,3,8,40,40,160,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,0:00:00.00,0:00:02.00,HookTitle,,0,0,0,,வீடியோ எடிட்டிங் ரகசியம்! 🔥
""")
    for s, e, text in captions_data:
        f.write(f"Dialogue: 0,{fmt_time(s)},{fmt_time(e)},Default,,0,0,0,,{text}\n")

print("ASS Subtitles generated successfully!")

# 4. Master Audio (Dialogue -14 LUFS + Ducked BGM at -20 dB)
print("\n=== 4. MASTERING AUDIO ===")
mastered_audio = os.path.join(TEMP_DIR, "mastered_audio.wav")
filter_complex_audio = (
    f"[0:a]loudnorm=I=-14:TP=-1.5:LRA=9[voice];"
    f"[1:a]volume=-20dB,afade=t=in:st=0:d=1,afade=t=out:st={total_dur-1.5:.2f}:d=1.5,atrim=0:{total_dur:.2f}[bgm];"
    f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
)

cmd_audio = [
    "ffmpeg", "-i", raw_concat_mp4, "-stream_loop", "-1", "-i", BGM_AUDIO,
    "-filter_complex", filter_complex_audio,
    "-map", "[aout]", "-c:a", "pcm_s16le", mastered_audio, "-y"
]
subprocess.run(cmd_audio, check=True)
print("Mastered audio created!")

# 5. Final Composite (Video + Progress Bar + Subtitles + Mastered Audio)
print("\n=== 5. COMPOSITING FINAL REEL (1080x1920 30FPS H.264) ===")
final_mp4 = os.path.join(EXPORT_DIR, "tamil-short-reel.mp4")

# Top animated progress bar:
# y=0, h=8, width grows from 0 to 1080 over total_dur
dur_str = f"{total_dur:.2f}"
vf_final = (
    f"drawbox=x=0:y=0:w='min(1080,1080*t/{dur_str})':h=8:color=0xEA8207@1:t=fill,"
    f"ass=filename={os.path.basename(ass_file)}:fontsdir={os.path.basename(FONTS_DIR)}"
)

cmd_final = [
    "ffmpeg", "-i", raw_concat_mp4, "-i", mastered_audio,
    "-vf", vf_final,
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    final_mp4, "-y"
]
subprocess.run(cmd_final, check=True)
print(f"Final Reel exported to: {final_mp4}")

# 6. Extract 4 Verification Frames for Framing QA
print("\n=== 6. EXTRACTING 4 FRAMES FOR FRAMING QA ===")
sample_times = [
    (1, 1.0,  os.path.join(EXPORT_DIR, "frame_1_hook.jpg")),
    (2, 4.0,  os.path.join(EXPORT_DIR, "frame_2_spk1.jpg")),
    (3, 12.0, os.path.join(EXPORT_DIR, "frame_3_spk2.jpg")),
    (4, 26.0, os.path.join(EXPORT_DIR, "frame_4_final.jpg")),
]

for num, t_sec, out_jpg in sample_times:
    cmd_sample = [
        "ffmpeg", "-ss", f"{t_sec:.2f}", "-i", final_mp4,
        "-vframes", "1", "-q:v", "2", out_jpg, "-y"
    ]
    subprocess.run(cmd_sample, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Frame {num} extracted at {t_sec}s -> {out_jpg}")

print("\n=== PIPELINE EXECUTION COMPLETE ===")
