import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import numpy as np

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_2409")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat_2409.mp4")
mastered_audio = os.path.join(TEMP_DIR, "mastered_audio_2409.wav")
ass_file = os.path.join(BASE_DIR, "reel_2409_subtitles.ass")
final_mp4 = os.path.join(EXPORT_DIR, "1-lakh-jobs-challenge-reel.mp4")
banner_path = os.path.join(BASE_DIR, "header_banner_perfect.png")

os.chdir(BASE_DIR)
dur_str = "60.10"

print("=== 1. VERIFYING PERFECT TWO-LINE TITLE BANNER ===")
assert os.path.exists(banner_path), "Banner file missing!"

print("=== 2. RENDERING COMPOSITE WITH -loop 1 -framerate 30 BANNER ===")
filter_video = (
    f"color=c=black:s=1080x1920:r=30:d={dur_str}[bg];"
    f"[bg][0:v]overlay=0:558[base];"
    f"[base][2:v]overlay=0:408[frame];"
    f"[frame]ass=filename={os.path.basename(ass_file)}:fontsdir={os.path.basename(FONTS_DIR)}[vout]"
)

cmd_final = [
    "ffmpeg", "-y",
    "-i", raw_concat_mp4,
    "-i", mastered_audio,
    "-loop", "1", "-framerate", "30", "-t", dur_str, "-i", banner_path,
    "-filter_complex", filter_video,
    "-map", "[vout]", "-map", "1:a",
    "-t", dur_str,
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    final_mp4
]

print("Executing FFmpeg...")
subprocess.run(cmd_final, check=True)
print(f"Final Reel exported to: {final_mp4}")

print("=== 3. VERIFYING BANNER PERSISTENCE ACROSS FULL TIMELINE ===")
sample_times = [
    (1, 2.0,  os.path.join(EXPORT_DIR, "frame_2409_1_hook.jpg")),      # Hook Question Girl
    (2, 13.0, os.path.join(EXPORT_DIR, "frame_2409_2_graduates.jpg")), # B-ROLL 1: College Graduates
    (3, 23.0, os.path.join(EXPORT_DIR, "frame_2409_3_offer.jpg")),     # B-ROLL 2: Contract Offer Letter
    (4, 30.5, os.path.join(EXPORT_DIR, "frame_2409_4_glitch.jpg")),    # B-ROLL 3: Critical Error / Banned Red Alert
    (5, 45.0, os.path.join(EXPORT_DIR, "frame_2409_5_stress.jpg")),    # B-ROLL 4: Pressure & Devastation
    (6, 53.0, os.path.join(EXPORT_DIR, "frame_2409_6_success.jpg")),   # B-ROLL 5: Skyscraper Sunrise Victory
]

all_passed = True
for num, t_sec, out_jpg in sample_times:
    cmd_sample = [
        "ffmpeg", "-y", "-ss", f"{t_sec:.2f}", "-i", final_mp4,
        "-vframes", "1", "-q:v", "2", out_jpg
    ]
    subprocess.run(cmd_sample, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    img = Image.open(out_jpg)
    crop = img.crop((0, 408, 1080, 558))
    arr = np.array(crop)
    orange = np.sum((arr[:, :, 0] > 180) & (arr[:, :, 1] > 100) & (arr[:, :, 2] < 50))
    pct = orange / (1080 * 150)
    print(f"Frame {num} ({t_sec:4.1f}s): orange={pct*100:.1f}%, file={out_jpg}")
    if pct < 0.70:
        all_passed = False

if all_passed:
    print("\nSUCCESS: All frames have the persistent two-line reference title banner!")
else:
    print("\nFAILURE: Some frames missed the banner!")
