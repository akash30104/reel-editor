import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
RAW_VIDEO = os.path.join(BASE_DIR, "RAW VIDEOS", "1205 2k.mp4")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_shark")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
INTERNET_BROLLS_DIR = os.path.join(BASE_DIR, "internet_brolls")
BGM_AUDIO = os.path.join(BASE_DIR, "my-video", "assets", "bgm_bed.mp3")
WHOOSH_SFX = os.path.join(BASE_DIR, "my-video", "assets", "whoosh.mp3")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
os.chdir(BASE_DIR)

print("=== 1. GENERATING TOPIC HEADER BANNER ===")
# 1080x142 px, Fill: #EA8207 (234, 130, 7)
banner_png = os.path.join(BASE_DIR, "header_banner_shark.png")
banner_img = Image.new("RGBA", (1080, 142), (234, 130, 7, 255))
draw_b = ImageDraw.Draw(banner_img)
font_b = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 52)

banner_text = "Japanese Shark Story "
bbox_b = draw_b.textbbox((0, 0), banner_text, font=font_b)
tw_b = bbox_b[2] - bbox_b[0]
th_b = bbox_b[3] - bbox_b[1]

emoji_shark = Image.open(os.path.join(BASE_DIR, "emojis", "shark.png")).convert("RGBA")
emoji_size = 50
emoji_shark = emoji_shark.resize((emoji_size, emoji_size), Image.Resampling.LANCZOS)

total_w = tw_b + emoji_size + 10
start_bx = (1080 - total_w) // 2
text_by = (142 - th_b) // 2 - 4
emoji_by = (142 - emoji_size) // 2

draw_b.text((start_bx, text_by), banner_text, fill=(0, 0, 0, 255), font=font_b)
banner_img.paste(emoji_shark, (start_bx + tw_b + 10, emoji_by), emoji_shark)
banner_img.save(banner_png)
print(f"Header banner saved: {banner_png}")

# Cuts Timeline definition:
# (idx, raw_start, raw_end, speaker, zoom, broll_file, subtitle_tamil)
broll_japan = os.path.join(INTERNET_BROLLS_DIR, "broll_japan.mp4")
broll_fish = os.path.join(INTERNET_BROLLS_DIR, "broll_fish.mp4")
broll_stress = os.path.join(INTERNET_BROLLS_DIR, "broll_stress.mp4")
broll_business = os.path.join(INTERNET_BROLLS_DIR, "broll_business.mp4")

cuts = [
    # 1. Hook Opening (Speaker 2, 1.15x Zoom, 0.6s B&W snap to color)
    (1,  317.00, 321.20, 2, True,  None,
     "ஜப்பான்ல மக்களுக்கு மீன் ரொம்ப பிடிக்கும்... {\\c&H000782EA&}Fish சாப்பிடுவாங்க!{\\c&H00FFFFFF&}"),
    
    # 2. B-Roll 1 (Internet B-Roll: Japan / Tokyo Street)
    (2,  321.20, 325.30, 2, False, broll_japan,
     "ஆனா அவங்களுக்கு {\\c&H000782EA&}Fresh Fish-ஆ{\\c&H00FFFFFF&} உடனே கிடைக்காது!"),
    
    # 3. Speaker 1 Normal (Question / Reaction)
    (3,  325.30, 328.60, 1, False, None,
     "அப்போ மீனவர்கள் என்ன பண்றாங்கன்னா {\\c&H000782EA&}பெரிய தொட்டில{\\c&H00FFFFFF&} போடுறாங்க!"),
    
    # 4. B-Roll 2 (Internet B-Roll: Fish Swimming Underwater)
    (4,  328.60, 331.00, 1, False, broll_fish,
     "கொண்டு வரும்போது மீன்கள் எல்லாம் {\\c&H000782EA&}டல்லா செத்து போயிடுது!{\\c&H00FFFFFF&}"),
    
    # 5. Speaker 2 Zoom (Dilemma / Hook Setup)
    (5,  331.00, 335.00, 2, True,  None,
     "அதை {\\c&H000782EA&}உயிரோட வச்சுக்க{\\c&H00FFFFFF&} என்ன பண்ணனும் தெரியுமா?"),
    
    # 6. Speaker 1 Zoom (Curiosity)
    (6,  335.00, 339.50, 1, True,  None,
     "என்ன பண்றாங்க? {\\c&H000782EA&}எப்படி பிரெஷ்ஷா{\\c&H00FFFFFF&} வைக்க முடியும்?"),
    
    # 7. Speaker 2 Normal (The Shark Strategy!)
    (7,  339.50, 344.80, 2, False, None,
     "தொட்டிக்குள்ள சின்ன மீன்கள் கூட {\\c&H000782EA&}ஒரு சுறா மீனை{\\c&H00FFFFFF&} உள்ள போடுறான்!"),
    
    # 8. B-Roll 2 continuation (Fish running from predator)
    (8,  344.80, 349.50, 2, False, broll_fish,
     "சுறா மீன் துரத்தும்போது மீன்கள் {\\c&H000782EA&}தப்பிக்க ஓடிக்கிட்டே{\\c&H00FFFFFF&} இருக்கும்!"),
    
    # 9. Speaker 2 Zoom (The Fresh Outcome)
    (9,  349.50, 353.50, 2, True,  None,
     "கரைக்கு வரும்போது எல்லா மீன்களும் {\\c&H000782EA&}செம பிரெஷ்ஷா{\\c&H00FFFFFF&} இருக்கும்!"),
    
    # 10. B-Roll 3 (Internet B-Roll: Workplace Stress / Challenges)
    (10, 353.50, 358.50, 2, False, broll_stress,
     "வாழ்க்கையிலயும் Business-லயும் {\\c&H000782EA&}சவால்கள் (Stress){\\c&H00FFFFFF&} கண்டிப்பா வேணும்!"),
    
    # 11. Speaker 2 Zoom (Why Challenges Matter)
    (11, 358.50, 364.00, 2, True,  None,
     "அந்த ஸ்ட்ரெஸ் தான் நம்மளை {\\c&H000782EA&}Active-ஆ உயிரோட{\\c&H00FFFFFF&} ஓட வைக்கும்!"),
    
    # 12. B-Roll 4 (Internet B-Roll: Business Success / Entrepreneurship)
    (12, 364.00, 369.00, 2, False, broll_business,
     "இதுதான் {\\c&H000782EA&}Happy Stress!{\\c&H00FFFFFF&} ரிஸ்க் எடுத்து ஜெயிக்கணும்!"),
    
    # 13. Speaker 2 Normal (Comfort Zone is Dangerous)
    (13, 369.00, 374.80, 2, False, None,
     "எந்த ஒரு சவாலும் இல்லன்னா வாழ்க்கை {\\c&H000782EA&}ரொம்ப வெறுப்பா{\\c&H00FFFFFF&} ஆயிடும்!"),
    
    # 14. Speaker 1 Zoom (Call to Action)
    (14, 374.80, 380.00, 1, True,  None,
     "அதனால சவால்களை பார்த்து {\\c&H000782EA&}பயப்படவே கூடாது!{\\c&H00FFFFFF&}"),
    
    # 15. Speaker 2 Zoom (Climax / Victory)
    (15, 380.00, 385.00, 2, True,  None,
     "எதிர்த்து நின்னு போராடுங்க... {\\c&H000782EA&}வாழ்க்கையில ஜெயிப்பீங்க!{\\c&H00FFFFFF&}"),
]

print("\n=== 2. RENDERING INDIVIDUAL CUTS WITH INTERNET B-ROLLS ===")
chunk_files = []
timeline_subs = []
current_time = 0.0
raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat_shark.mp4")
mastered_audio = os.path.join(TEMP_DIR, "mastered_audio.wav")
skip_chunks = os.path.exists(raw_concat_mp4) and os.path.exists(mastered_audio)

for idx, start, end, speaker, zoom, broll, sub_text in cuts:
    dur = end - start
    timeline_subs.append((current_time, current_time + dur, sub_text))
    out_chunk = os.path.join(TEMP_DIR, f"chunk_{idx:02d}.mp4")
    
    if not skip_chunks:
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
            vf_broll = "scale=1080:940:force_original_aspect_ratio=increase,crop=1080:940,fps=30,format=yuv420p"
            cmd_v = [
                "ffmpeg", "-stream_loop", "-1", "-i", broll, "-i", tmp_audio,
                "-t", f"{dur:.3f}",
                "-vf", vf_broll,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
                "-c:a", "copy",
                "-map", "0:v", "-map", "1:a",
                out_chunk, "-y"
            ]
            subprocess.run(cmd_v, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Cut {idx:02d}: INTERNET B-ROLL [{os.path.basename(broll)}] -> [{current_time:.2f}s - {current_time+dur:.2f}s] ({dur:.2f}s)")
        else:
            # Talking Head Video Crop
            if idx == 1:
                vf = (
                    "crop=1198:1044:1200:120,scale=1080:940:flags=lanczos,fps=30,format=yuv420p,"
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

if not skip_chunks:
    # Concat video chunks
    concat_list = os.path.join(TEMP_DIR, "concat.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for c in chunk_files:
            f.write(f"file '{c}'\n")

    cmd_concat = [
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c", "copy", raw_concat_mp4, "-y"
    ]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Concatenation complete: raw_concat_shark.mp4")
else:
    print("Reusing existing raw_concat_shark.mp4")

# 3. Create ASS Subtitles (Pure White dialogue + Signature Orange #EA8207 Highlights + 5px Black Outline)
ass_file = os.path.join(BASE_DIR, "japanese_shark_subtitles.ass")

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
if not os.path.exists(mastered_audio):
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
else:
    print("Reusing existing mastered_audio.wav")

# 5. Final Composite:
# Canvas: 1080x1920
# Video at (0, 558)
# Orange Header Banner at (0, 416)
# NO PROGRESS BAR (Clean solid black letterbox)
# ASS Subtitles burned via libass
# (NO PILL BADGE)
final_mp4 = os.path.join(EXPORT_DIR, "japanese-shark-story-reel.mp4")

filter_video = (
    f"color=c=black:s=1080x1920:r=30:d={dur_str}[bg];"
    f"[bg][0:v]overlay=0:558[base];"
    f"[base][2:v]overlay=0:416[frame];"
    f"[frame]ass=filename={os.path.basename(ass_file)}:fontsdir={os.path.basename(FONTS_DIR)}[vout]"
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

# 6. Extract Verification Frames for QA
sample_times = [
    (1, 2.0,  os.path.join(EXPORT_DIR, "frame_1_shark_hook.jpg")),   # Hook Opening (Clean, No Pill Card, No progress bar)
    (2, 6.0,  os.path.join(EXPORT_DIR, "frame_2_japan_broll.jpg")),  # Internet B-ROLL 1: Japan / Tokyo Street
    (3, 13.0, os.path.join(EXPORT_DIR, "frame_fish_underwater.jpg")),# Internet B-ROLL 2: Fish Swimming
    (4, 40.0, os.path.join(EXPORT_DIR, "frame_4_stress_broll.jpg")), # Internet B-ROLL 3: Challenge & Happy Stress
    (5, 50.0, os.path.join(EXPORT_DIR, "frame_business_hustle.jpg")),# Internet B-ROLL 4: Entrepreneurship
]

for num, t_sec, out_jpg in sample_times:
    cmd_sample = [
        "ffmpeg", "-ss", f"{t_sec:.2f}", "-i", final_mp4,
        "-vframes", "1", "-q:v", "2", out_jpg, "-y"
    ]
    subprocess.run(cmd_sample, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Frame {num} extracted at {t_sec}s -> {out_jpg}")

print("\n=== PIPELINE EXECUTION COMPLETE ===")
