import os
import subprocess

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_2409")
EXPORT_DIR = os.path.join(BASE_DIR, "EXPORT")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat_2409.mp4")
mastered_audio = os.path.join(TEMP_DIR, "mastered_audio_2409.wav")
banner_png = os.path.join(BASE_DIR, "header_banner_2409.png")
ass_file = os.path.join(BASE_DIR, "reel_2409_subtitles.ass")
final_mp4 = os.path.join(EXPORT_DIR, "1-lakh-jobs-challenge-reel.mp4")

os.chdir(BASE_DIR)
dur_str = "60.10"

filter_video = (
    f"color=c=black:s=1080x1920:r=30:d={dur_str}[bg];"
    f"[bg][0:v]overlay=0:558[base];"
    f"[base][2:v]overlay=0:416:repeatlast=1[frame];"
    f"[frame]ass=filename={os.path.basename(ass_file)}:fontsdir={os.path.basename(FONTS_DIR)}[vout]"
)

cmd_final = [
    "ffmpeg", "-i", raw_concat_mp4, "-i", mastered_audio, "-i", banner_png,
    "-filter_complex", filter_video,
    "-map", "[vout]", "-map", "1:a",
    "-t", dur_str,
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    final_mp4, "-y"
]

print("Starting final video composite...")
subprocess.run(cmd_final, check=True)
print(f"Final Reel exported to: {final_mp4}")

# Extract Verification Frames for QA
sample_times = [
    (1, 2.0,  os.path.join(EXPORT_DIR, "frame_2409_1_hook.jpg")),      # Hook Question Girl (Zoom, Persistent Banner, No Progress Bar)
    (2, 13.0, os.path.join(EXPORT_DIR, "frame_2409_2_graduates.jpg")), # B-ROLL 1: College Graduates + Persistent Banner
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

print("\n=== FAST COMPOSITE COMPLETE ===")
