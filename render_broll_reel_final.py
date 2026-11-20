import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_v5")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
BGM_AUDIO = os.path.join(BASE_DIR, "my-video", "assets", "bgm_bed.mp3")
WHOOSH_SFX = os.path.join(BASE_DIR, "my-video", "assets", "whoosh.mp3")

raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat_brolls.mp4")
final_mp4 = os.path.join(EXPORT_DIR, "tamil-short-reel.mp4")

# 1. Topic Header Banner (1080x142, #EA8207, with Real PNG Emoji 💔)
banner_png = os.path.join(BASE_DIR, "header_banner.png")
banner_img = Image.new("RGBA", (1080, 142), (234, 130, 7, 255))
draw_b = ImageDraw.Draw(banner_img)
font_b = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 52)

banner_text = "Toxic Relationship? "
bbox_b = draw_b.textbbox((0, 0), banner_text, font=font_b)
tw_b = bbox_b[2] - bbox_b[0]
th_b = bbox_b[3] - bbox_b[1]

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
print(f"Header banner saved: {banner_png}")

# 2. ASS Subtitles (White text + Signature Orange #EA8207 Highlights + 5px Black Stroke)
ass_file = os.path.join(BASE_DIR, "tamil_brolls_reel.ass")

# Timestamps from cuts (cumulative 67.30s)
subs = [
    (0.00,  3.90,  "ஏன் பெண்கள் {\\c&H000782EA&}Toxic பசங்க{\\c&H00FFFFFF&} மேல போறாங்க?"),
    (3.90,  6.97,  "ஏன்னா அவங்களுக்கு {\\c&H000782EA&}வேணும் ட்ராமாஸ்!{\\c&H00FFFFFF&}"),
    (6.97,  9.69,  "சண்டை போட்டுட்டு {\\c&H000782EA&}ஜாலியா இருப்பாங்க!{\\c&H00FFFFFF&}"),
    (9.69,  13.88, "அமைதியா போனா பலருக்கு {\\c&H000782EA&}Bore அடிக்கும்!{\\c&H00FFFFFF&}"),
    (13.88, 16.58, "வாழ்க்கையில எப்பவும் ஒரு {\\c&H000782EA&}Drama நடக்கணும்!{\\c&H00FFFFFF&}"),
    (16.58, 18.51, "அந்த சண்டையவே அவங்க {\\c&H000782EA&}Enjoy பண்ண{\\c&H00FFFFFF&} ஆரம்பிச்சுடுறாங்க!"),
    (18.51, 21.62, "{\\c&H000782EA&}Toxic People-அ{\\c&H00FFFFFF&} நாம எப்படி Handle பண்றது?"),
    (21.62, 25.95, "அது Office-ஆ இருக்கலாம் இல்ல {\\c&H000782EA&}Real Life-ஆ{\\c&H00FFFFFF&} இருக்கலாம்!"),
    (25.95, 28.72, "நாம ஏன் பண்றோம்னா {\\c&H000782EA&}பிடிக்காம பண்றோம்!{\\c&H00FFFFFF&}"),
    (28.72, 30.66, "{\\c&H000782EA&}கரெக்ட்!{\\c&H00FFFFFF&} அதுதான் நிஜமான உண்மை!"),
    (30.66, 34.59, "மக்கள் வாழ்க்கையில ரொம்ப {\\c&H000782EA&}Bored ஆயிடுறாங்க!{\\c&H00FFFFFF&}"),
    (34.59, 38.83, "அதனாலயே {\\c&H000782EA&}தப்பான ஆட்கள்{\\c&H00FFFFFF&} கூட சிக்கிக்கிறாங்க!"),
    (38.83, 42.95, "அப்போ இதுக்கு {\\c&H000782EA&}தீர்வு என்ன?{\\c&H00FFFFFF&} நாம என்ன பண்ணனும்?"),
    (42.95, 46.26, "முதல்ல நாம {\\c&H000782EA&}Clear Boundaries{\\c&H00FFFFFF&} போட கத்துக்கணும்!"),
    (46.26, 51.06, "எல்லாத்துக்கும் நாம உடனே {\\c&H000782EA&}React பண்ணக் கூடாது!{\\c&H00FFFFFF&}"),
    (51.06, 55.91, "அமைதியா இருந்தாலே {\\c&H000782EA&}பாதி பிரச்சனை{\\c&H00FFFFFF&} முடிஞ்சுடும்!"),
    (55.91, 60.75, "Toxic மனிதர்களை நாம {\\c&H000782EA&}மாத்த முடியாது!{\\c&H00FFFFFF&}"),
    (60.75, 67.30, "நன்றாக யோசித்துப் பாருங்கள் {\\c&H000782EA&}நிஜம் புரியும்!{\\c&H00FFFFFF&}"),
]

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
Style: HookSubtitle,Noto Sans Tamil,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,40,40,510,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    for i, (s, e, text) in enumerate(subs):
        st = "HookSubtitle" if i == 0 else "Default"
        f.write(f"Dialogue: 0,{fmt_time(s)},{fmt_time(e)},{st},,0,0,0,,{text}\n")

print(f"ASS subtitles saved: {ass_file}")

# 3. Master Audio with Ducked BGM (-20 dB) + Whoosh SFX on Cuts
total_dur = 67.30
dur_str = f"{total_dur:.2f}"
mastered_audio = os.path.join(TEMP_DIR, "mastered_audio.wav")

filter_audio = (
    f"[1:a]volume=-20dB,afade=t=in:st=0:d=1,afade=t=out:st={total_dur-1.5:.2f}:d=1.5,atrim=0:{total_dur:.2f}[bgm];"
    f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:TP=-1.5:LRA=9[aout]"
)

cmd_audio = [
    "ffmpeg", "-i", raw_concat_mp4, "-stream_loop", "-1", "-i", BGM_AUDIO,
    "-filter_complex", filter_audio,
    "-map", "[aout]", "-c:a", "pcm_s16le", mastered_audio, "-y"
]
subprocess.run(cmd_audio, check=True)
print("Mastered audio created!")

# 4. Final Video Composite:
# Canvas: 1080x1920
# Video at (0, 558)
# Banner at (0, 416)
# Top 8px progress bar
# Subtitles burned via libass
# (NO PILL BADGE!)
filter_video = (
    f"color=c=black:s=1080x1920:r=30:d={dur_str}[bg];"
    f"[bg][0:v]overlay=0:558[base];"
    f"[base][2:v]overlay=0:416[frame];"
    f"[frame]drawbox=x=0:y=0:w='min(1080,1080*t/{dur_str})':h=8:color=0xEA8207@1:t=fill[pb];"
    f"[pb]ass=filename={os.path.basename(ass_file)}:fontsdir={os.path.basename(FONTS_DIR)}[vout]"
)

cmd_final = [
    "ffmpeg", "-i", raw_concat_mp4, "-i", mastered_audio, "-i", banner_png,
    "-filter_complex", filter_video,
    "-map", "[vout]", "-map", "1:a",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    final_mp4, "-y"
]
subprocess.run(cmd_final, check=True)
print(f"Final Reel exported to: {final_mp4}")

# 5. Extract 4 Verification Frames for QA
sample_times = [
    (1, 1.5,  os.path.join(EXPORT_DIR, "frame_1_hook.jpg")),       # Hook Question (Clean, No Pill Card)
    (2, 5.0,  os.path.join(EXPORT_DIR, "frame_2_drama.jpg")),      # B-ROLL 1: Intense Relationship Drama
    (3, 11.5, os.path.join(EXPORT_DIR, "frame_3_problem.jpg")),    # B-ROLL 2: Boredom Cutaway
    (4, 23.5, os.path.join(EXPORT_DIR, "frame_4_truth.jpg")),      # B-ROLL 3: Real Life Struggle
]

for num, t_sec, out_jpg in sample_times:
    cmd_sample = [
        "ffmpeg", "-ss", f"{t_sec:.2f}", "-i", final_mp4,
        "-vframes", "1", "-q:v", "2", out_jpg, "-y"
    ]
    subprocess.run(cmd_sample, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Frame {num} extracted at {t_sec}s -> {out_jpg}")

print("\n=== PIPELINE EXECUTION COMPLETE ===")
