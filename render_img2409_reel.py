import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
RAW_VIDEO = os.path.join(BASE_DIR, "RAW VIDEOS", "IMG_2409.MOV")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_2409")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
BGM_AUDIO = os.path.join(BASE_DIR, "my-video", "assets", "bgm_bed.mp3")
WHOOSH_SFX = os.path.join(BASE_DIR, "my-video", "assets", "whoosh.mp3")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
os.chdir(BASE_DIR)

print("=== 1. GENERATING TOPIC HEADER BANNER ===")
# 1080x142 px, Fill: #EA8207 (234, 130, 7)
banner_png = os.path.join(BASE_DIR, "header_banner_2409.png")
banner_img = Image.new("RGBA", (1080, 142), (234, 130, 7, 255))
draw_b = ImageDraw.Draw(banner_img)
font_b = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 52)

banner_text = "1 Lakh Job Challenge "
bbox_b = draw_b.textbbox((0, 0), banner_text, font=font_b)
tw_b = bbox_b[2] - bbox_b[0]
th_b = bbox_b[3] - bbox_b[1]

emoji_fire = Image.open(os.path.join(BASE_DIR, "emojis", "fire.png")).convert("RGBA")
emoji_size = 50
emoji_fire = emoji_fire.resize((emoji_size, emoji_size), Image.Resampling.LANCZOS)

total_w = tw_b + emoji_size + 10
start_bx = (1080 - total_w) // 2
text_by = (142 - th_b) // 2 - 4
emoji_by = (142 - emoji_size) // 2

draw_b.text((start_bx, text_by), banner_text, fill=(0, 0, 0, 255), font=font_b)
banner_img.paste(emoji_fire, (start_bx + tw_b + 10, emoji_by), emoji_fire)
banner_img.save(banner_png)
print(f"Header banner saved: {banner_png}")

# Cuts Timeline definition:
# (idx, raw_start, raw_end, speaker, zoom, broll_file, subtitle_tamil)
# Speaker 1 = Guy (Left side of 3840x2160)
# Speaker 2 = Girl (Right side of 3840x2160)
broll_grad = os.path.join(BASE_DIR, "temp_img2409", "broll_grad.mp4")
broll_offer = os.path.join(BASE_DIR, "temp_img2409", "broll_offer.mp4")
broll_glitch = os.path.join(BASE_DIR, "temp_img2409", "yt_error_glitch.mp4")
broll_stress = os.path.join(BASE_DIR, "internet_brolls", "yt_stress.mp4")
broll_success = os.path.join(BASE_DIR, "internet_brolls", "yt_success.mp4")

cuts = [
    # 1. Opening Hook: Girl (Speaker 2, Zoom 1.15x, 0.6s B&W flash to color)
    (1,  3.60,  9.20, 2, True,  None,
     "உங்களுக்கு எப்படி இந்த ஐடியா வந்தது? {\\c&H000782EA&}499 Days-ல 1 Lakh பேருக்கு{\\c&H00FFFFFF&} வேலை வாங்கி தரேன் சொன்னீங்க?!"),
    
    # 2. Guy starts the backstory: 1000 Jobs
    (2,  255.00, 260.50, 1, False, None,
     "நான் என் கம்பெனில {\\c&H000782EA&}ஒரு 1000 பேருக்கு{\\c&H00FFFFFF&} வேலை வாங்கி தர போறேன்னு ஆரம்பிச்சேன்..."),
    
    # 3. B-Roll 1 (Internet B-Roll: College Graduates / Career Aspirants)
    (3,  270.00, 275.50, 1, False, broll_grad,
     "ஆனா {\\c&H000782EA&}Day 7-லயே 600+ பேருக்கு{\\c&H00FFFFFF&} வேலை வாங்கி கொடுத்தாச்சு!"),
    
    # 4. Guy scaling to 10,000 target
    (4,  281.50, 286.00, 1, True,  None,
     "1000 பேருக்கு முடிக்க முடியுதுன்னா, {\\c&H000782EA&}10,000 பேருக்கு{\\c&H00FFFFFF&} ஏன் முடிக்க முடியாதுன்னு மாத்துனேன்!"),
    
    # 5. B-Roll 2 (Internet B-Roll: Signing Employment Contracts & Offer Letters)
    (5,  287.50, 292.50, 1, False, broll_offer,
     "அப்போ {\\c&H000782EA&}Day 39-ல பாத்தீங்கன்னா 5,500 பேருக்கு{\\c&H00FFFFFF&} வேலை கொடுத்தாச்சு!"),
    
    # 6. Guy setup to disaster
    (6,  292.50, 296.50, 1, False, None,
     "Day 40 காலையில எழுந்து {\\c&H000782EA&}இன்ஸ்டாகிராம் திறந்து{\\c&H00FFFFFF&} பார்க்கிறேன்..."),
    
    # 7. B-Roll 3 (Internet B-Roll: Critical Error / Glitch Flashing Red Warning)
    (7,  296.50, 299.80, 1, False, broll_glitch,
     "இன்ஸ்டாகிராம் அக்கவுண்ட் {\\c&H000782EA&}BANNED!{\\c&H00FFFFFF&} எப்படி இருக்கும்?!"),
    
    # 8. Guy Emotional Peak / The Question
    (8,  299.80, 305.50, 1, True,  None,
     "நீங்க கஷ்டப்பட்டு பில்ட் பண்ண எல்லாமே... {\\c&H000782EA&}ஒரு நொடியில போயிடுச்சுன்னா{\\c&H00FFFFFF&} என்ன பண்ணுவீங்க?!"),
    
    # 9. B-Roll 4 (Internet B-Roll: Devastation, Darkness & Resolve)
    (9,  305.50, 309.50, 1, False, broll_stress,
     "மறுபடியும் ஆரம்பிப்பேன்! {\\c&H000782EA&}மறுபடியும் ஆரம்பிச்சேன்!{\\c&H00FFFFFF&}"),
    
    # 10. Guy Turning Point: NGO comparison
    (10, 348.00, 353.50, 1, False, None,
     "ஒரு NGO இவ்வளவு இன்வெஸ்ட் பண்ணி {\\c&H000782EA&}20,000 பேருக்கு வேலை{\\c&H00FFFFFF&} தரேன்னு முடிவு பண்ணா..."),
    
    # 11. B-Roll 5 (Internet B-Roll: High-Rise Skyscraper Sunrise Victory)
    (11, 353.50, 359.50, 1, False, broll_success,
     "நான் ஒரு ஆளா {\\c&H000782EA&}1,00,000 பேருக்கு வேலை{\\c&H00FFFFFF&} வாங்கி தருவேன்னு முடிவு பண்ணேன்!"),
    
    # 12. Guy Climax / Call to Action
    (12, 309.50, 315.00, 1, True,  None,
     "இந்த சவால்தான் நம்மளை {\\c&H000782EA&}வேற ஒரு மனிதனா{\\c&H00FFFFFF&} மாத்தும்! ஜெயிப்போம்!"),
]

print("\n=== 2. RENDERING INDIVIDUAL CUTS WITH 100% OUTSIDE B-ROLLS ===")
chunk_files = []
timeline_subs = []
current_time = 0.0
raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat_2409.mp4")
skip_chunks = os.path.exists(raw_concat_mp4) and os.path.getsize(raw_concat_mp4) > 10000000

for idx, start, end, speaker, zoom, broll, sub_text in cuts:
    dur = end - start
    timeline_subs.append((current_time, current_time + dur, sub_text))
    out_chunk = os.path.join(TEMP_DIR, f"chunk_{idx:02d}.mp4")
    chunk_files.append(out_chunk)
    current_time += dur

total_dur = current_time
dur_str = f"{total_dur:.2f}"
print(f"Total Video Duration: {total_dur:.2f} seconds ({total_dur/60:.2f} min)")

# 3. Create ASS Subtitles (White dialogue + Orange #EA8207 highlights + 5px Black Stroke, 0 Yellow)
ass_file = os.path.join(BASE_DIR, "reel_2409_subtitles.ass")

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
Style: HookSubtitle,Noto Sans Tamil,62,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,40,40,510,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    for i, (s, e, text) in enumerate(timeline_subs):
        st = "HookSubtitle" if i == 0 else "Default"
        f.write(f"Dialogue: 0,{fmt_time(s)},{fmt_time(e)},{st},,0,0,0,,{text}\n")

print(f"ASS subtitles saved: {ass_file}")

# 4. Master Audio with Ducked BGM (-20 dB) + EBU R128 (-14 LUFS)
mastered_audio = os.path.join(TEMP_DIR, "mastered_audio_2409.wav")
if not os.path.exists(mastered_audio) or os.path.getsize(mastered_audio) < 1000000:
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
    print("Reusing existing mastered_audio_2409.wav")

# 5. Final Composite:
# Canvas: 1080x1920
# Video at (0, 558)
# Persistent Orange Header Banner at (0, 416) with repeatlast=1
# Solid black top & bottom letterbox (NO PROGRESS BAR)
# ASS Subtitles burned via libass
# (NO PILL BADGE)
final_mp4 = os.path.join(EXPORT_DIR, "1-lakh-jobs-challenge-reel.mp4")

filter_video = (
    f"color=c=black:s=1080x1920:r=30:d={dur_str}[bg];"
    f"[bg][0:v]overlay=0:558[base];"
    f"[base][2:v]overlay=0:416:repeatlast=1[frame];"
    f"[frame]ass=filename={os.path.basename(ass_file)}:fontsdir={os.path.basename(FONTS_DIR)}[vout]"
)

cmd_final = [
    "ffmpeg", "-i", raw_concat_mp4, "-i", mastered_audio, "-loop", "1", "-i", banner_png,
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
    (1, 2.0,  os.path.join(EXPORT_DIR, "frame_2409_1_hook.jpg")),      # Hook Question Girl (Zoom, Banner, No Progress Bar)
    (2, 13.0, os.path.join(EXPORT_DIR, "frame_2409_2_graduates.jpg")), # B-ROLL 1: College Graduates / Careers + Persistent Banner
    (3, 23.0, os.path.join(EXPORT_DIR, "frame_2409_3_offer.jpg")),     # B-ROLL 2: Contract Offer Letter + Persistent Banner
    (4, 30.5, os.path.join(EXPORT_DIR, "frame_2409_4_glitch.jpg")),    # B-ROLL 3: Critical Error / Banned Red Alert + Persistent Banner
    (5, 45.0, os.path.join(EXPORT_DIR, "frame_2409_5_stress.jpg")),    # B-ROLL 4: Pressure & Devastation + Persistent Banner
    (6, 53.0, os.path.join(EXPORT_DIR, "frame_2409_6_success.jpg")),   # B-ROLL 5: Skyscraper Sunrise Victory + Persistent Banner
]

for num, t_sec, out_jpg in sample_times:
    cmd_sample = [
        "ffmpeg", "-ss", f"{t_sec:.2f}", "-i", final_mp4,
        "-vframes", "1", "-q:v", "2", out_jpg, "-y"
    ]
    subprocess.run(cmd_sample, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Frame {num} extracted at {t_sec}s -> {out_jpg}")

print("\n=== PIPELINE EXECUTION FOR IMG_2409 COMPLETE ===")
