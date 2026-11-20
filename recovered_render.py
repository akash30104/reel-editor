import os
import subprocess

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
RAW_VIDEO = os.path.join(BASE_DIR, "RAW VIDEOS", "1205 2k.mp4")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_v2")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
BGM_AUDIO = os.path.join(BASE_DIR, "my-video", "assets", "bgm_bed.mp3")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
os.chdir(BASE_DIR)

# 1. Timeline Cuts (Accurate dialogue on "Toxic Relationship / Toxic People")
# Speaker 1 = Left (striped shirt, green lanyard)
# Speaker 2 = Right (blue shirt, microphone)
cuts = [
    # idx, start, end, speaker, zoom, description
    (1, 33.91, 37.81, 1, True),   # 3.90s - Spk 1 (Hook, 1.15x Zoom): ஏன் பெண்கள் Toxic பசங்க மேல போறாங்க?
    (2, 38.64, 43.10, 2, False),  # 4.46s - Spk 2 (1.0x Normal): ஏன்னா அவங்களுக்கு வேணும் ட்ராமாஸ்!
    (3,  8.27, 11.38, 1, True),   # 3.11s - Spk 1 (1.15x Zoom): Toxic People-அ எப்படி Handle பண்றது?
    (4, 12.08, 14.80, 2, False),  # 2.72s - Spk 2 (1.0x Normal): அது Work-ஆ இருக்கலாம் இல்ல Real Life!
    (5, 17.78, 20.55, 2, True),   # 2.77s - Spk 2 (1.15x Zoom): நாம ஏன் பண்றோம்னா பிடிக்காம பண்றோம்!
    (6, 20.85, 22.79, 1, False),  # 1.94s - Spk 1 (1.0x Normal): கரெக்ட்! அதுதான் நிஜம்!
    (7, 24.69, 27.50, 2, True),   # 2.81s - Spk 2 (1.15x Zoom): மக்கள் வாழ்க்கையில ரொம்ப Bored ஆயிடுறாங்க!
    (8, 27.50, 30.50, 2, False),  # 3.00s - Spk 2 (1.0x Normal): நன்றாக யோசித்துப் பாருங்கள்!
]

print("=== 1. EXTRACTING & CROPPING VIDEO CHUNKS ===")
chunk_files = []
timeline_timestamps = []
current_time = 0.0

for idx, start, end, speaker, zoom in cuts:
    dur = end - start
    timeline_timestamps.append((current_time, current_time + dur, speaker, zoom))
    
    # 2560x1440 -> 1080x1920 Framing
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

# 3. Build ASS Subtitle File with ORANGE Captions (#EA8207 -> &H000782EA&)
print("\n=== 3. GENERATING ACCURATE TAMIL SUBTITLES IN ORANGE (#EA8207) ===")
ass_file = os.path.join(BASE_DIR, "tamil_orange_reel.ass")

def fmt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# Exact, Natural Tamil Captions matching spoken words:
# Primary color is &H000782EA (Signature Orange #EA8207)
# Keyword highlight is &H0000FFFF (Bright Yellow #FFFF00)
captions_data = [
    # Cut 1: Hook (0.00s - 3.90s)
    (0.00, 1.90, "ஏன் பெண்கள் {\\c&H0000FFFF&}Toxic பசங்க{\\c&H000782EA&}"),
    (1.90, 3.90, "மேல போறாங்க {\\c&H0000FFFF&}தெரியுமா?{\\c&H000782EA&} 🤔"),
    
    # Cut 2: Response (3.90s - 8.36s)
    (3.90, 6.10, "ஏன்னா அவங்களுக்கு {\\c&H0000FFFF&}வேணும் ட்ராமாஸ்!{\\c&H000782EA&} 🔥"),
    (6.10, 8.36, "சண்டை போட்டுட்டு {\\c&H0000FFFF&}ஜாலியா இருப்பாங்க!{\\c&H000782EA&}"),
    
    # Cut 3: Core Problem (8.36s - 11.47s)
    (8.36, 9.90, "எனக்கு இருக்குற {\\c&H0000FFFF&}பெரிய பிரச்சனை...{\\c&H000782EA&}"),
    (9.90, 11.47, "{\\c&H0000FFFF&}Toxic People-அ{\\c&H000782EA&} எப்படி Handle பண்றது?"),
    
    # Cut 4: Context (11.47s - 14.19s)
    (11.47, 12.80, "அது {\\c&H0000FFFF&}Work-ஆ{\\c&H000782EA&} இருக்கலாம்..."),
    (12.80, 14.19, "இல்ல {\\c&H0000FFFF&}Real Life-ஆ{\\c&H000782EA&} இருக்கலாம்!"),
    
    # Cut 5: Why we do it (14.19s - 16.96s)
    (14.19, 16.96, "நாம ஏன் பண்றோம்னா {\\c&H0000FFFF&}பிடிக்காம பண்றோம்!{\\c&H000782EA&}"),
    
    # Cut 6: Agreement (16.96s - 18.90s)
    (16.96, 18.90, "{\\c&H0000FFFF&}கரெக்ட்!{\\c&H000782EA&} அதுதான் நிஜம்! 👍"),
    
    # Cut 7: Truth (18.90s - 21.71s)
    (18.90, 21.71, "மக்கள் வாழ்க்கையில {\\c&H0000FFFF&}Bored ஆயிடுறாங்க!{\\c&H000782EA&}"),
    
    # Cut 8: Conclusion (21.71s - 24.71s)
    (21.71, 24.71, "நன்றாக யோசித்துப் பாருங்கள் {\\c&H0000FFFF&}நிஜம் புரியும்!{\\c&H000782EA&} 💡"),
]

with open(ass_file, "w", encoding="utf-8") as f:
    f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: OrangeCaption,Noto Sans Tamil,56,&H000782EA,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,40,40,320,1
Style: HookBanner,Noto Sans Tamil,62,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,8,40,40,160,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,0:00:00.00,0:00:03.90,HookBanner,,0,0,0,,ஏன் Toxic பசங்க? 💔
""")
    for s, e, text in captions_data:
        f.write(f"Dialogue: 0,{fmt_time(s)},{fmt_time(e)},OrangeCaption,,0,0,0,,{text}\n")

print("Accurate Tamil ASS Subtitles in Signature Orange generated successfully!")

# 4. Master Audio (Dialogue + Ducked BGM at -20 dB -> Normalized to -14 LUFS)
print("\n=== 4. MASTERING AUDIO TO -14 LUFS ===")
mastered_audio = os.path.join(TEMP_DIR, "mastered_audio.wav")
filter_complex_audio = (
    f"[1:a]volume=-20dB,afade=t=in:st=0:d=1,afade=t=out:st={total_dur-1.5:.2f}:d=1.5,atrim=0:{total_dur:.2f}[bgm];"
    f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:TP=-1.5:LRA=9[aout]"
)

cmd_audio = [
    "ffmpeg", "-i", raw_concat_mp4, "-stream_loop", "-1", "-i", BGM_AUDIO,
    "-filter_complex", filter_complex_audio,
    "-map", "[aout]", "-c:a", "pcm_s16le", mastered_audio, "-y"
]
subprocess.run(cmd_audio, check=True)
print("Mastered audio created!")

# 5. Final Composite (1080x1920 30FPS H.264)
print("\n=== 5. COMPOSITING FINAL REEL WITH ORANGE SUBTITLES ===")
final_mp4 = os.path.join(EXPORT_DIR, "tamil-short-reel.mp4")

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
    (1, 1.5,  os.path.join(EXPORT_DIR, "frame_1_hook.jpg")),
    (2, 5.5,  os.path.join(EXPORT_DIR, "frame_2_drama.jpg")),
    (3, 10.0, os.path.join(EXPORT_DIR, "frame_3_problem.jpg")),
    (4, 19.5, os.path.join(EXPORT_DIR, "frame_4_truth.jpg")),
]

for num, t_sec, out_jpg in sample_times:
    cmd_sample = [
        "ffmpeg", "-ss", f"{t_sec:.2f}", "-i", final_mp4,
        "-vframes", "1", "-q:v", "2", out_jpg, "-y"
    ]
    subprocess.run(cmd_sample, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Frame {num} extracted at {t_sec}s -> {out_jpg}")

print("\n=== PIPELINE EXECUTION COMPLETE ===")
