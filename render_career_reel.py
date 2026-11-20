import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
RAW_VIDEO = os.path.join(BASE_DIR, "RAW VIDEOS", "1205 2k.mp4")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_career")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
BROLLS_DIR = os.path.join(BASE_DIR, "brolls")
BGM_AUDIO = os.path.join(BASE_DIR, "my-video", "assets", "bgm_bed.mp3")
WHOOSH_SFX = os.path.join(BASE_DIR, "my-video", "assets", "whoosh.mp3")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
os.chdir(BASE_DIR)

print("=== 1. GENERATING TOPIC HEADER BANNER ===")
# 1080x142 px, Fill: #EA8207 (234, 130, 7)
banner_png = os.path.join(BASE_DIR, "header_banner_career.png")
banner_img = Image.new("RGBA", (1080, 142), (234, 130, 7, 255))
draw_b = ImageDraw.Draw(banner_img)
font_b = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 52)

banner_text = "Career vs Relationship? "
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

# Cuts Timeline definition:
# (idx, raw_start, raw_end, speaker, zoom, broll_file, subtitle_tamil)
cuts = [
    # 1. Hook Question (Speaker 1, 1.15x Zoom, 0.6s B&W snap to color)
    (1,  236.37, 240.15, 1, True,  None,
     "Career முக்கியமா? இல்ல {\\c&H000782EA&}Relationship முக்கியமா?{\\c&H00FFFFFF&}"),
    
    # 2. B-Roll 1 (broll_opening_hook.mp4 - Ambition / Career)
    (2,  240.15, 243.93, 1, False, os.path.join(BROLLS_DIR, "broll_opening_hook.mp4"),
     "20s-ல வேலைக்கு ஓடும்போது {\\c&H000782EA&}காதலை இழக்கிறோமா?{\\c&H00FFFFFF&}"),
    
    # 3. Speaker 1 Zoom (Dilemma)
    (3,  244.36, 248.00, 1, True,  None,
     "நம்ம வாழ்க்கையில {\\c&H000782EA&}வெற்றி அடையணும்னு{\\c&H00FFFFFF&} ஓடுறோம்!"),
    
    # 4. B-Roll 2 (broll_drama_hook.mp4 - Relationship friction)
    (4,  248.00, 251.36, 1, False, os.path.join(BROLLS_DIR, "broll_drama_hook.mp4"),
     "ஆனா கூட இருக்கிறவங்களுக்கு {\\c&H000782EA&}நேரம் கொடுக்க முடியல!{\\c&H00FFFFFF&}"),
    
    # 5. Speaker 2 Normal (Validation)
    (5,  252.22, 255.00, 2, False, None,
     "{\\c&H000782EA&}கரெக்ட்!{\\c&H00FFFFFF&} இது பல பேரோட பெரிய பிரச்சனை!"),
    
    # 6. Speaker 1 Normal (Question)
    (6,  256.50, 258.39, 1, False, None,
     "அப்போ இதுல {\\c&H000782EA&}எதை நாம தேர்ந்தெடுக்கணும்?{\\c&H00FFFFFF&}"),
    
    # 7. Speaker 2 Zoom (Insight)
    (7,  259.69, 263.50, 2, True,  None,
     "முதல்ல ஒன்னு புரிஞ்சுக்கணும்... {\\c&H000782EA&}Career Growth{\\c&H00FFFFFF&} ரொம்ப அவசியம்!"),
    
    # 8. B-Roll 3 (broll_real_life.mp4 - Daily life struggle)
    (8,  263.50, 268.49, 2, False, os.path.join(BROLLS_DIR, "broll_real_life.mp4"),
     "ஆனா Relationship-க்காக அதை {\\c&H000782EA&}சமரசம் பண்ணா{\\c&H00FFFFFF&} பின்னாடி வருந்துவோம்!"),
    
    # 9. Speaker 2 Normal
    (9,  272.23, 275.28, 2, False, None,
     "பணம் சம்பாதிக்கலாம்... {\\c&H000782EA&}வெற்றி பெறலாம்!{\\c&H00FFFFFF&}"),
    
    # 10. Speaker 2 Zoom
    (10, 275.53, 278.08, 2, True,  None,
     "ஆனா உண்மையான அன்பு இல்லனா {\\c&H000782EA&}எல்லாம் பாழ்!{\\c&H00FFFFFF&}"),
    
    # 11. B-Roll 4 (broll_conflict.mp4 - Clear Boundaries)
    (11, 278.41, 283.35, 2, False, os.path.join(BROLLS_DIR, "broll_conflict.mp4"),
     "ரெண்டுமே வேணும்னா {\\c&H000782EA&}Clear Boundaries{\\c&H00FFFFFF&} இருக்கணும்!"),
    
    # 12. Speaker 2 Normal
    (12, 284.96, 290.85, 2, False, None,
     "வேலை நேரத்துல வேலை... {\\c&H000782EA&}உறவுகளுக்கு நேரம்!{\\c&H00FFFFFF&}"),
    
    # 13. Speaker 1 Zoom
    (13, 291.79, 295.14, 1, True,  None,
     "அப்போ நம்மை புரிஞ்சிக்கிற {\\c&H000782EA&}துணை வேணும்!{\\c&H00FFFFFF&}"),
    
    # 14. Speaker 2 Zoom
    (14, 298.79, 303.52, 2, True,  None,
     "கண்டிப்பா! உங்க Partner உங்க {\\c&H000782EA&}கனவுகளை மதிக்கணும்!{\\c&H00FFFFFF&}"),
    
    # 15. Speaker 2 Normal
    (15, 303.90, 308.00, 2, False, None,
     "அப்படிப்பட்ட புரிதல் இருந்தா {\\c&H000782EA&}Career-ம் ஜெயிக்கலாம்!{\\c&H00FFFFFF&}"),
    
    # 16. Speaker 2 Zoom
    (16, 308.00, 313.96, 2, True,  None,
     "உங்க {\\c&H000782EA&}Relationship-ம்{\\c&H00FFFFFF&} ரொம்ப அழகா வாழும்!"),
    
    # 17. Speaker 1 Normal (Takeaway / Climax)
    (17, 322.97, 328.54, 1, False, None,
     "இதுதான் உண்மையான {\\c&H000782EA&}வாழ்க்கை வெற்றி!{\\c&H00FFFFFF&}"),
]

print("\n=== 2. RENDERING INDIVIDUAL CUTS ===")
chunk_files = []
timeline_subs = []
current_time = 0.0

for idx, start, end, speaker, zoom, broll, sub_text in cuts:
    dur = end - start
    timeline_subs.append((current_time, current_time + dur, sub_text))
    out_chunk = os.path.join(TEMP_DIR, f"chunk_{idx:02d}.mp4")
    
    # Dialogue Audio Segment (pcm_s16le, 48000Hz, 2ch)
    tmp_audio = os.path.join(TEMP_DIR, f"audio_{idx:02d}.wav")
    cmd_a = [
        "ffmpeg", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", RAW_VIDEO,
        "-vn", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
        tmp_audio, "-y"
    ]
    subprocess.run(cmd_a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if broll and os.path.exists(broll):
        # B-Roll scaled to 1080x940, 30fps
        cmd_v = [
            "ffmpeg", "-stream_loop", "-1", "-i", broll, "-i", tmp_audio,
            "-t", f"{dur:.3f}",
            "-vf", "scale=1080:940:flags=lanczos,fps=30,format=yuv420p",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-c:a", "copy",
            "-map", "0:v", "-map", "1:a",
            out_chunk, "-y"
        ]
        subprocess.run(cmd_v, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Cut {idx:02d}: B-ROLL [{os.path.basename(broll)}] -> [{current_time:.2f}s - {current_time+dur:.2f}s] ({dur:.2f}s)")
    else:
        # Talking Head Video Crop
        if idx == 1:
            # Opening Hook: 0.6s B&W flash snapping to color!
            vf = (
                "crop=1198:1044:150:120,scale=1080:940:flags=lanczos,fps=30,format=yuv420p,"
                "hue=s='if(lt(t,0.6),0,1)'"
            )
        elif speaker == 1:
            if zoom:
                vf = "crop=1198:1044:150:120,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"
            else:
                vf = "crop=1378:1200:80:80,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"
        else: # speaker == 2
            if zoom:
                vf = "crop=1198:1044:1200:120,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"
            else:
                vf = "crop=1378:1200:1100:80,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"

        cmd_v = [
            "ffmpeg", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", RAW_VIDEO,
            "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
            out_chunk, "-y"
        ]
        subprocess.run(cmd_v, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Cut {idx:02d}: Talking Head [Spk {speaker}, Zoom: {zoom}] -> [{current_time:.2f}s - {current_time+dur:.2f}s] ({dur:.2f}s)")

    chunk_files.append(out_chunk)
    current_time += dur

total_dur = current_time
dur_str = f"{total_dur:.2f}"
print(f"\nTotal Video Duration: {total_dur:.2f} seconds ({total_dur/60:.2f} min)")

# Concat video chunks
concat_list = os.path.join(TEMP_DIR, "concat.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for c in chunk_files:
        f.write(f"file '{c}'\n")

raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat_career.mp4")
cmd_concat = [
    "ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_list,
    "-c", "copy", raw_concat_mp4, "-y"
]
subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Concatenation complete: raw_concat_career.mp4")

# 3. Create ASS Subtitles (White text + Signature Orange #EA8207 Highlights + 5px Black Outline)
ass_file = os.path.join(BASE_DIR, "career_subtitles.ass")

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
    for i, (s, e, text) in enumerate(timeline_subs):
        st = "HookSubtitle" if i == 0 else "Default"
        f.write(f"Dialogue: 0,{fmt_time(s)},{fmt_time(e)},{st},,0,0,0,,{text}\n")

print(f"ASS subtitles saved: {ass_file}")

# 4. Master Audio with Ducked BGM (-20 dB) + Whoosh SFX on Opening Hook
mastered_audio = os.path.join(TEMP_DIR, "mastered_audio.wav")
filter_audio = (
    f"[1:a]volume=-20dB,afade=t=in:st=0:d=1,afade=t=out:st={total_dur-1.5:.2f}:d=1.5,atrim=0:{dur_str}[bgm];"
    f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:TP=-1.5:LRA=9[aout]"
)

cmd_audio = [
    "ffmpeg", "-i", raw_concat_mp4, "-stream_loop", "-1", "-i", BGM_AUDIO,
    "-filter_complex", filter_audio,
    "-map", "[aout]", "-c:a", "pcm_s16le", mastered_audio, "-y"
]
subprocess.run(cmd_audio, check=True)
print("Mastered audio created with -14 LUFS loudness!")

# 5. Final Composite:
# Canvas: 1080x1920
# Video at (0, 558)
# Orange Header Banner at (0, 416)
# Top 8px Orange Progress Bar
# ASS Subtitles burned via libass
# (NO PILL BADGE)
final_mp4 = os.path.join(EXPORT_DIR, "career-vs-relationship-reel.mp4")

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

# 6. Extract 4 Verification Frames for QA
sample_times = [
    (1, 2.0,  os.path.join(EXPORT_DIR, "frame_1_career_hook.jpg")),   # Hook Question (Clean, No Pill Card)
    (2, 5.0,  os.path.join(EXPORT_DIR, "frame_2_broll.jpg")),          # B-ROLL 1: Office/Career Tension
    (3, 20.0, os.path.join(EXPORT_DIR, "frame_3_conflict.jpg")),       # Speaker 2 Punch-in Zoom
    (4, 40.0, os.path.join(EXPORT_DIR, "frame_4_lesson.jpg")),         # B-ROLL 4 / Relationship Insight
]

for num, t_sec, out_jpg in sample_times:
    cmd_sample = [
        "ffmpeg", "-ss", f"{t_sec:.2f}", "-i", final_mp4,
        "-vframes", "1", "-q:v", "2", out_jpg, "-y"
    ]
    subprocess.run(cmd_sample, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Frame {num} extracted at {t_sec}s -> {out_jpg}")

print("\n=== PIPELINE EXECUTION COMPLETE ===")
