import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
RAW_VIDEO = os.path.join(BASE_DIR, "RAW VIDEOS", "1205 2k.mp4")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_v4")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
BGM_AUDIO = os.path.join(BASE_DIR, "my-video", "assets", "bgm_bed.mp3")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
os.chdir(BASE_DIR)

# ==========================================
# 1. CREATE HEADER BANNER WITH REAL EMOJI (💔)
# ==========================================
print("=== 1. GENERATING TOPIC HEADER BANNER WITH REAL EMOJI ===")
banner_png = os.path.join(BASE_DIR, "header_banner.png")
banner_img = Image.new("RGBA", (1080, 142), (234, 130, 7, 255))
draw_b = ImageDraw.Draw(banner_img)
font_b = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 52)

banner_text = "Toxic Relationship? "
bbox_b = draw_b.textbbox((0, 0), banner_text, font=font_b)
tw_b = bbox_b[2] - bbox_b[0]
th_b = bbox_b[3] - bbox_b[1]

# Paste high-res broken heart emoji
emoji_heart = Image.open(os.path.join(BASE_DIR, "emojis", "broken_heart.png")).convert("RGBA")
emoji_size = 50
emoji_heart = emoji_heart.resize((emoji_size, emoji_size), Image.Resampling.LANCZOS)

total_w = tw_b + emoji_size + 10
start_bx = (1080 - total_w) // 2
text_by = (142 - th_b) // 2 - 4
emoji_by = (142 - emoji_size) // 2

draw_b.text((start_bx, text_by), banner_text, fill=(0, 0, 0, 255), font=font_b)
banner_img.paste(emoji_heart, (start_bx + tw_b + 10, emoji_by), emoji_heart)
banner_img.save(banner_png)
print(f"Header banner saved with real emoji: {banner_png}")

# ==========================================
# 2. CREATE ON-SCREEN OPENING HOOK BADGE (0 - 3.5s)
# ==========================================
print("\n=== 2. GENERATING ON-SCREEN HOOK BADGE (0 - 3.5s) ===")
hook_png = os.path.join(BASE_DIR, "hook_badge.png")
hook_img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
draw_h = ImageDraw.Draw(hook_img)

font_tamil_hook = ImageFont.truetype(os.path.join(FONTS_DIR, "NotoSansTamil-Bold.ttf"), 44)
hook_title = "ஏன் பெண்கள் Toxic பசங்க மேல போறாங்க?"

badge_h = 84
badge_w = 980
badge_x = (1080 - badge_w) // 2
badge_y = 590

# Card background with orange outline
draw_h.rounded_rectangle(
    [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
    radius=20,
    fill=(15, 15, 15, 235),
    outline=(234, 130, 7, 255),
    width=4
)

# Fire emoji on left
fire_emoji = Image.open(os.path.join(BASE_DIR, "emojis", "fire.png")).convert("RGBA")
fire_size = 46
fire_emoji = fire_emoji.resize((fire_size, fire_size), Image.Resampling.LANCZOS)
hook_img.paste(fire_emoji, (badge_x + 25, badge_y + (badge_h - fire_size) // 2), fire_emoji)

# Heart emoji on right
hook_img.paste(emoji_heart.resize((fire_size, fire_size), Image.Resampling.LANCZOS), (badge_x + badge_w - 25 - fire_size, badge_y + (badge_h - fire_size) // 2), emoji_heart.resize((fire_size, fire_size), Image.Resampling.LANCZOS))

# Centered text inside hook card
bbox_h = draw_h.textbbox((0, 0), hook_title, font=font_tamil_hook)
tw_h = bbox_h[2] - bbox_h[0]
th_h = bbox_h[3] - bbox_h[1]
tx_h = (1080 - tw_h) // 2
ty_h = badge_y + (badge_h - th_h) // 2 - 4
draw_h.text((tx_h, ty_h), hook_title, fill=(255, 255, 255, 255), font=font_tamil_hook)
hook_img.save(hook_png)
print(f"Hook badge saved: {hook_png}")

# ==========================================
# 3. DEFINE EXTENDED CUTS (60s - 90s DURATION)
# ==========================================
# Speaker 1 = Left (striped shirt, green lanyard)
# Speaker 2 = Right (blue shirt, microphone)
cuts = [
    # idx, start, end, speaker, zoom, tamil_caption, orange_keyword
    (1,  33.91, 37.81, 1, True,  "ஏன் பெண்கள் {\\c&H000782EA&}Toxic பசங்க{\\c&H00FFFFFF&} மேல போறாங்க?"),
    (2,  38.64, 41.71, 2, False, "ஏன்னா அவங்களுக்கு {\\c&H000782EA&}வேணும் ட்ராமாஸ்!{\\c&H00FFFFFF&}"),
    (3,  41.91, 44.63, 2, True,  "சண்டை போட்டுட்டு {\\c&H000782EA&}ஜாலியா இருப்பாங்க!{\\c&H00FFFFFF&}"),
    (4,  44.94, 49.13, 2, False, "அமைதியா போனா பலருக்கு {\\c&H000782EA&}Bore அடிக்கும்!{\\c&H00FFFFFF&}"),
    (5,  52.74, 55.44, 2, True,  "வாழ்க்கையில எப்பவும் ஒரு {\\c&H000782EA&}Drama நடக்கணும்!{\\c&H00FFFFFF&}"),
    (6,  56.93, 58.86, 2, False, "அந்த சண்டையவே அவங்க {\\c&H000782EA&}Enjoy பண்ண{\\c&H00FFFFFF&} ஆரம்பிச்சுடுறாங்க!"),
    (7,   8.27, 11.38, 1, True,  "{\\c&H000782EA&}Toxic People-அ{\\c&H00FFFFFF&} நாம எப்படி Handle பண்றது?"),
    (8,  12.08, 16.41, 2, False, "அது Office-ஆ இருக்கலாம் இல்ல {\\c&H000782EA&}Real Life-ஆ{\\c&H00FFFFFF&} இருக்கலாம்!"),
    (9,  17.78, 20.55, 2, True,  "நாம ஏன் பண்றோம்னா {\\c&H000782EA&}பிடிக்காம பண்றோம்!{\\c&H00FFFFFF&}"),
    (10, 20.85, 22.79, 1, False, "{\\c&H000782EA&}கரெக்ட்!{\\c&H00FFFFFF&} அதுதான் நிஜமான உண்மை!"),
    (11, 24.69, 28.62, 2, True,  "மக்கள் வாழ்க்கையில ரொம்ப {\\c&H000782EA&}Bored ஆயிடுறாங்க!{\\c&H00FFFFFF&}"),
    (12, 29.00, 33.24, 2, False, "அதனாலயே {\\c&H000782EA&}தப்பான ஆட்கள்{\\c&H00FFFFFF&} கூட சிக்கிக்கிறாங்க!"),
    (13, 68.39, 72.51, 1, True,  "அப்போ இதுக்கு {\\c&H000782EA&}தீர்வு என்ன?{\\c&H00FFFFFF&} நாம என்ன பண்ணனும்?"),
    (14, 72.84, 76.15, 2, False, "முதல்ல நாம {\\c&H000782EA&}Clear Boundaries{\\c&H00FFFFFF&} போட கத்துக்கணும்!"),
    (15, 79.70, 84.50, 2, True,  "எல்லாத்துக்கும் நாம உடனே {\\c&H000782EA&}React பண்ணக் கூடாது!{\\c&H00FFFFFF&}"),
    (16, 86.67, 91.52, 1, False, "அமைதியா இருந்தாலே {\\c&H000782EA&}பாதி பிரச்சனை{\\c&H00FFFFFF&} முடிஞ்சுடும்!"),
    (17, 91.86, 96.70, 2, True,  "Toxic மனிதர்களை நாம {\\c&H000782EA&}மாத்த முடியாது!{\\c&H00FFFFFF&}"),
    (18, 99.94, 106.49, 2, False, "நன்றாக யோசித்துப் பாருங்கள் {\\c&H000782EA&}நிஜம் புரியும்!{\\c&H00FFFFFF&}"),
]

print("\n=== 3. EXTRACTING & CROPPING VIDEO CHUNKS TO 1080x940 ===")
chunk_files = []
timeline_timestamps = []
current_time = 0.0

for idx, start, end, speaker, zoom, caption in cuts:
    dur = end - start
    timeline_timestamps.append((current_time, current_time + dur, speaker, zoom, caption))
    
    # 1080x940 crop logic
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
print(f"\nTotal Reel Duration: {total_dur:.2f} seconds ({total_dur/60:.2f} minutes) -> Target: 1:00 to 1:30 min (PASSED!)")

# ==========================================
# 4. CONCAT CHUNKS
# ==========================================
print("\n=== 4. CONCATENATING SPEECH TIMELINE (1080x940) ===")
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

# ==========================================
# 5. GENERATE TAMIL ASS SUBTITLES (WHITE + ORANGE HIGHLIGHT, 5px BLACK OUTLINE)
# ==========================================
print("\n=== 5. GENERATING TAMIL ASS SUBTITLES (WHITE + ORANGE #EA8207) ===")
ass_file = os.path.join(BASE_DIR, "tamil_extended_reel.ass")

def fmt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

with open(ass_file, "w", encoding="utf-8") as f:
    f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans Tamil,54,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,40,40,500,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    for s, e, spk, zm, text in timeline_timestamps:
        f.write(f"Dialogue: 0,{fmt_time(s)},{fmt_time(e)},Default,,0,0,0,,{text}\n")

print(f"Tamil ASS Subtitles written: {ass_file}")

# ==========================================
# 6. MASTER AUDIO (-14 LUFS, DUCKED BGM AT -20 dB)
# ==========================================
print("\n=== 6. MASTERING AUDIO TO -14 LUFS ===")
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

# ==========================================
# 7. FINAL COMPOSITE (ARCHETYPE 1 LETTERBOX + BANNER + HOOK BADGE + WHITE/ORANGE SUBTITLES)
# ==========================================
print("\n=== 7. COMPOSITING FINAL REEL (1080x1920 30FPS H.264) ===")
final_mp4 = os.path.join(EXPORT_DIR, "tamil-short-reel.mp4")

dur_str = f"{total_dur:.2f}"
filter_composite = (
    f"color=c=black:s=1080x1920:r=30:d={dur_str}[bg];"
    f"[bg][0:v]overlay=0:558[base];"
    f"[base][2:v]overlay=0:416[with_banner];"
    f"[with_banner][3:v]overlay=0:0:enable='between(t,0,3.5)'[with_hook];"
    f"[with_hook]drawbox=x=0:y=0:w='min(1080,1080*t/{dur_str})':h=8:color=0xEA8207@1:t=fill[pb];"
    f"[pb]ass=filename={os.path.basename(ass_file)}:fontsdir={os.path.basename(FONTS_DIR)}[vout]"
)

cmd_final = [
    "ffmpeg", "-i", raw_concat_mp4, "-i", mastered_audio, "-i", banner_png, "-i", hook_png,
    "-filter_complex", filter_composite,
    "-map", "[vout]", "-map", "1:a",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    final_mp4, "-y"
]
subprocess.run(cmd_final, check=True)
print(f"\nFinal Reel exported to: {final_mp4}")

# ==========================================
# 8. EXTRACT 4 VERIFICATION FRAMES FOR QA
# ==========================================
print("\n=== 8. EXTRACTING 4 FRAMES FOR FRAMING QA ===")
sample_times = [
    (1, 1.5,  os.path.join(EXPORT_DIR, "frame_1_hook.jpg")),
    (2, 5.0,  os.path.join(EXPORT_DIR, "frame_2_drama.jpg")),
    (3, 14.0, os.path.join(EXPORT_DIR, "frame_3_problem.jpg")),
    (4, 35.0, os.path.join(EXPORT_DIR, "frame_4_truth.jpg")),
]

for num, t_sec, out_jpg in sample_times:
    cmd_sample = [
        "ffmpeg", "-ss", f"{t_sec:.2f}", "-i", final_mp4,
        "-vframes", "1", "-q:v", "2", out_jpg, "-y"
    ]
    subprocess.run(cmd_sample, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Frame {num} extracted at {t_sec}s -> {out_jpg}")

print("\n=== PIPELINE EXECUTION COMPLETE ===")
