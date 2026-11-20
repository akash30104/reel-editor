import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_2409")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat_2409.mp4")
mastered_audio = os.path.join(TEMP_DIR, "mastered_audio_2409.wav")
ass_file = os.path.join(BASE_DIR, "reel_2409_subtitles.ass")
final_mp4 = os.path.join(EXPORT_DIR, "1-lakh-jobs-challenge-reel.mp4")

os.chdir(BASE_DIR)
dur_str = "60.10"

print("=== 1. CREATING TWO-LINE REFERENCE TITLE BANNER ===")
banner_w = 1080
banner_h = 150
bg_color = (234, 130, 7, 255) # #EA8207

banner = Image.new("RGBA", (banner_w, banner_h), bg_color)
draw = ImageDraw.Draw(banner)

# 2px black border lines matching style reference
draw.line([(0, 0), (banner_w, 0)], fill=(0, 0, 0, 255), width=2)
draw.line([(0, banner_h - 1), (banner_w, banner_h - 1)], fill=(0, 0, 0, 255), width=2)

font_l1 = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 48)
font_l2 = ImageFont.truetype(os.path.join(FONTS_DIR, "NotoSansTamil-Bold.ttf"), 42)

# Line 1: '1 Lakh Job Challenge ' + fire emoji
text_l1 = "1 Lakh Job Challenge "
bbox_l1 = draw.textbbox((0, 0), text_l1, font=font_l1)
w_l1 = bbox_l1[2] - bbox_l1[0]
h_l1 = bbox_l1[3] - bbox_l1[1]

emoji_fire = Image.open(os.path.join(BASE_DIR, "emojis", "fire.png")).convert("RGBA")
emoji_fire = emoji_fire.resize((44, 44), Image.Resampling.LANCZOS)

total_w_l1 = w_l1 + 44 + 8
start_x_l1 = (banner_w - total_w_l1) // 2
y_l1 = 18

draw.text((start_x_l1, y_l1), text_l1, fill=(0, 0, 0, 255), font=font_l1)
banner.paste(emoji_fire, (start_x_l1 + w_l1 + 8, y_l1 + (h_l1 - 44) // 2 + 2), emoji_fire)

# Line 2: '499 Days-ல 1 Lakh Jobs! ' + target emoji
text_l2 = "499 Days-ல 1 Lakh Jobs! "
bbox_l2 = draw.textbbox((0, 0), text_l2, font=font_l2)
w_l2 = bbox_l2[2] - bbox_l2[0]
h_l2 = bbox_l2[3] - bbox_l2[1]

emoji_target = Image.open(os.path.join(BASE_DIR, "emojis", "target.png")).convert("RGBA")
emoji_target = emoji_target.resize((42, 42), Image.Resampling.LANCZOS)

total_w_l2 = w_l2 + 42 + 8
start_x_l2 = (banner_w - total_w_l2) // 2
y_l2 = 82

draw.text((start_x_l2, y_l2), text_l2, fill=(0, 0, 0, 255), font=font_l2)
banner.paste(emoji_target, (start_x_l2 + w_l2 + 8, y_l2 + (h_l2 - 42) // 2 + 2), emoji_target)

banner_path = os.path.join(BASE_DIR, "header_banner_perfect.png")
banner.save(banner_path)
print(f"Header banner saved: {banner_path}")

print("=== 2. RENDERING COMPOSITE WITH GUARANTEED LOOPED TITLE BANNER ===")
filter_video = (
    f"color=c=black:s=1080x1920:r=30:d={dur_str}[bg];"
    f"[bg][0:v]overlay=0:558[base];"
    f"[2:v]loop=loop=-1:size=1:start=0[looped_banner];"
    f"[base][looped_banner]overlay=0:408:shortest=1[frame];"
    f"[frame]ass=filename={os.path.basename(ass_file)}:fontsdir={os.path.basename(FONTS_DIR)}[vout]"
)

cmd_final = [
    "ffmpeg", "-i", raw_concat_mp4, "-i", mastered_audio, "-i", banner_path,
    "-filter_complex", filter_video,
    "-map", "[vout]", "-map", "1:a",
    "-t", dur_str,
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    final_mp4, "-y"
]

subprocess.run(cmd_final, check=True)
print(f"Final Reel exported to: {final_mp4}")

print("=== 3. EXTRACTING QA FRAMES ACROSS ENTIRE DURATION ===")
sample_times = [
    (1, 2.0,  os.path.join(EXPORT_DIR, "frame_2409_1_hook.jpg")),      # Hook Question Girl
    (2, 13.0, os.path.join(EXPORT_DIR, "frame_2409_2_graduates.jpg")), # B-ROLL 1: College Graduates
    (3, 23.0, os.path.join(EXPORT_DIR, "frame_2409_3_offer.jpg")),     # B-ROLL 2: Contract Offer Letter
    (4, 30.5, os.path.join(EXPORT_DIR, "frame_2409_4_glitch.jpg")),    # B-ROLL 3: Critical Error / Banned Red Alert
    (5, 45.0, os.path.join(EXPORT_DIR, "frame_2409_5_stress.jpg")),    # B-ROLL 4: Pressure & Devastation
    (6, 53.0, os.path.join(EXPORT_DIR, "frame_2409_6_success.jpg")),   # B-ROLL 5: Skyscraper Sunrise Victory
]

for num, t_sec, out_jpg in sample_times:
    cmd_sample = [
        "ffmpeg", "-ss", f"{t_sec:.2f}", "-i", final_mp4,
        "-vframes", "1", "-q:v", "2", out_jpg, "-y"
    ]
    subprocess.run(cmd_sample, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Frame {num} extracted at {t_sec}s -> {out_jpg}")

print("\n=== VERIFICATION COMPLETE ===")
