import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
RAW_VIDEO = os.path.join(BASE_DIR, "RAW VIDEOS", "1205 2k.mp4")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_v3")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
BGM_AUDIO = os.path.join(BASE_DIR, "my-video", "assets", "bgm_bed.mp3")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
os.chdir(BASE_DIR)

# 1. Generate Header Banner PNG (1080x142, #EA8207 background, Black Bold Title)
print("=== 1. CREATING TOPIC HEADER BANNER ===")
banner_png = os.path.join(BASE_DIR, "header_banner.png")
banner_img = Image.new("RGBA", (1080, 142), (234, 130, 7, 255))
draw_b = ImageDraw.Draw(banner_img)
try:
    font_b = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 52)
except:
    font_b = ImageFont.load_default()

banner_title = "Toxic Relationship? 💔"
bbox = draw_b.textbbox((0, 0), banner_title, font=font_b)
bw = bbox[2] - bbox[0]
bh = bbox[3] - bbox[1]
bx = (1080 - bw) // 2
by = (142 - bh) // 2 - 4
draw_b.text((bx, by), banner_title, fill=(0, 0, 0, 255), font=font_b)
banner_img.save(banner_png)
print(f"Header banner saved: {banner_png}")

# 2. Define Cuts (Raw Timestamps, Speaker, Zoom Framing)
# Video window size: 1080x940
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

print("\n=== 2. EXTRACTING & CROPPING VIDEO CHUNKS TO 1080x940 ===")
chunk_files = []
timeline_timestamps = []
current_time = 0.0

for idx, start, end, speaker, zoom in cuts:
    dur = end - start
    timeline_timestamps.append((current_time, current_time + dur, speaker, zoom))
    
    # Precise 1080x940 crops for Letterbox Video Window
    if speaker == 1:
        if zoom:
            vf = "crop=1198:1044:150:120,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"
        else:
            vf = "crop=1378:1200:80:80,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"
    else: # speaker == 2
        if zoom:
            vf = "crop=1198:1044:1200:120,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"
        else:
            vf = "crop=1378:1200:1100:80,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"

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

# 3. Concat Chunks into 1080x940 continuous speech stream
print("\n=== 3. CONCATENATING SPEECH TIMELINE (1080x940) ===")
concat_list = os.path.join(TEMP_DIR, "concat.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for c in chunk_files:
        f.write(f"file '{c}'\n")

raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat_940.mp4")
cmd_concat = [
    "ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_list,
    "-c", "copy", raw_concat_mp4, "-y"
]
subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Concatenation complete!")

# 4. Generate Tamil ASS Subtitle File (PURE WHITE, NO YELLOW)
print("\n=== 4. GENERATING PURE WHITE TAMIL SUBTITLES ===")
ass_file = os.path.join(BASE_DIR, "tamil_white_reel.ass")

def fmt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# Accurate Tamil spoken dialogue (PURE WHITE TEXT, NO YELLOW)
captions_data = [
    # Cut 1: Hook (0.00s - 3.90s)
    (0.00, 1.90, "ஏன் பெண்கள் Toxic பசங்க"),
    (1.90, 3.90, "மேல போறாங்க தெரியுமா? 🤔"),
    
    # Cut 2: Response (3.90s - 8.36s)
    (3.90, 6.10, "ஏன்னா அவங்களுக்கு வேணும் ட்ராமாஸ்! 🔥"),
    (6.10, 8.36, "சண்டை போட்டுட்டு ஜாலியா இருப்பாங்க!"),
    
    # Cut 3: Core Problem (8.36s - 11.47s)
    (8.36, 9.90, "எனக்கு இருக்குற பெரிய பிரச்சனை..."),
    (9.90, 11.47, "Toxic People-அ எப்படி Handle பண்றது?"),
    
    # Cut 4: Context (11.47s - 14.19s)
    (11.47, 12.80, "அது Work-ஆ இருக்கலாம்..."),
    (12.80, 14.19, "இல்ல Real Life-ஆ இருக்கலாம்!"),
    
    # Cut 5: Why we do it (14.19s - 16.96s)
    (14.19, 16.96, "நாம ஏன் பண்றோம்னா பிடிக்காம பண்றோம்!"),
    
    # Cut 6: Agreement (16.96s - 18.90s)
    (16.96, 18.90, "கரெக்ட்! அதுதான் நிஜம்! 👍"),
    
    # Cut 7: Truth (18.90s - 21.71s)
    (18.90, 21.71, "மக்கள் வாழ்க்கையில ரொம்ப Bored ஆயிடுறாங்க!"),
    
    # Cut 8: Conclusion (21.71s - 24.71s)
    (21.71, 24.71, "நன்றாக யோசித்துப் பாருங்கள் நிஜம் புரியும்! 💡"),
]

# Alignment 2 (bottom center), MarginV=500 -> perfectly positions inside 1080x940 video window at y ~ 1380px
# PrimaryColour=&H00FFFFFF& (PURE WHITE), OutlineColour=&H00000000& (BLACK)
with open(ass_file, "w", encoding="utf-8") as f:
    f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: WhiteSubtitle,Noto Sans Tamil,54,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,40,40,500,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    for s, e, text in captions_data:
        f.write(f"Dialogue: 0,{fmt_time(s)},{fmt_time(e)},WhiteSubtitle,,0,0,0,,{text}\n")

print(f"Pure White Tamil ASS Subtitles written: {ass_file}")

# 5. Master Audio (Dialogue + Ducked BGM at -20 dB -> Normalized to -14 LUFS)
print("\n=== 5. MASTERING AUDIO TO -14 LUFS ===")
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

# 6. Final Composite (Archetype 1: Letterbox Layout + Orange Banner + Video Window + White Subtitles)
print("\n=== 6. COMPOSITING FINAL REEL (ARCHETYPE 1 LETTERBOX) ===")
final_mp4 = os.path.join(EXPORT_DIR, "tamil-short-reel.mp4")

dur_str = f"{total_dur:.2f}"
# Canvas: 1080x1920 black
# Video: 1080x940 at y=558
# Banner: 1080x142 at y=416
# Progress bar: top 8px
# ASS subtitles: burned via libass + HarfBuzz
filter_composite = (
    f"color=c=black:s=1080x1920:r=30:d={dur_str}[bg];"
    f"[bg][0:v]overlay=0:558[base];"
    f"[base][2:v]overlay=0:416[frame];"
    f"[frame]drawbox=x=0:y=0:w='min(1080,1080*t/{dur_str})':h=8:color=0xEA8207@1:t=fill[pb];"
    f"[pb]ass=filename={os.path.basename(ass_file)}:fontsdir={os.path.basename(FONTS_DIR)}[vout]"
)

cmd_final = [
    "ffmpeg", "-i", raw_concat_mp4, "-i", mastered_audio, "-i", banner_png,
    "-filter_complex", filter_composite,
    "-map", "[vout]", "-map", "1:a",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    final_mp4, "-y"
]
subprocess.run(cmd_final, check=True)
print(f"Final Reel exported to: {final_mp4}")

# 7. Extract 4 Verification Frames for Framing QA
print("\n=== 7. EXTRACTING 4 FRAMES FOR QA ===")
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
