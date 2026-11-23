#!/usr/bin/env python3
"""
render_ref4_splitscreen.py
Renders Reel 1 in strict accordance with Reference 4 Master Specification:
1. FRAMING & B-ROLL:
   - 50/50 vertical split-screen (Host top half Y=0..960, Guest bottom half Y=960..1920).
   - Static framing, warm natural studio grade.
   - B-Roll cutaways every 3–6 seconds: relevant 16:9 B-roll centered on pure black 9:16 canvas (letterbox style).
2. SUBTITLE BANNER & EXACT PLACEMENT:
   - Display kinetic callout banners ONLY on key hooks, dates, percentages, and takeaways (not every word).
   - Full-width semi-transparent dark horizontal strip across exact center seam (Y=960).
   - Framed by thin white horizontal top and bottom border lines.
   - Supporting words: Medium white bold-italic sans-serif.
   - Focal keyword: Large golden-yellow stylized bold font centered with soft drop shadow.
   - Pop words in sequentially, then cut cleanly out.
3. AUDIO & OUTRO:
   - Clean dialogue (-14.0 LUFS) over soft emotional instrumental BGM (-23 dB).
   - Outro (last 4.5 seconds): Cut to black canvas with centered white channel card,
     animated subscribe button click, and "Watch full video on YouTube" text below.
4. EXPORT:
   - /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_4_Style.mp4
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
ASSETS_DIR = WORKSPACE / "assets"
BROLLS_DIR = ASSETS_DIR / "brolls"

WIDTH = 1080
HEIGHT = 1920
TOTAL_DUR = 74.0

# 1. Base Audio and Video Sources
pro_dialogue = WORKSPACE / "reel1_pro_mastered_audio.wav"
bgm_music = ASSETS_DIR / "audio" / "ramayan_flute_bgm.mp3"

# 2. Master Cut Segments Schedule (Alternating Split-Screen and 16:9 Letterboxed B-Roll)
# Raw video starts at 1988.0s. Each split-screen segment takes its corresponding offset from 202.MOV!
CUTS_SCHEDULE = [
    # 01. Split-Screen: Host asks the core question (0.0s - 4.5s, dur 4.5s)
    {"type": "split", "st": 0.0, "et": 4.5, "raw_ss": 1988.0},

    # 02. B-Roll 1: Temple / Ramayana Heritage (4.5s - 8.5s, dur 4.0s)
    {"type": "broll", "st": 4.5, "et": 8.5, "file": BROLLS_DIR / "broll_temple.mp4", "broll_ss": 2.0},

    # 03. Split-Screen: Guest opens Hanuman Hook (8.5s - 13.0s, dur 4.5s)
    {"type": "split", "st": 8.5, "et": 13.0, "raw_ss": 1996.5},

    # 04. B-Roll 2: Hanuman Power (13.0s - 16.5s, dur 3.5s)
    {"type": "broll", "st": 13.0, "et": 16.5, "file": BROLLS_DIR / "broll_hanuman_power.mp4", "broll_ss": 1.0},

    # 05. Split-Screen: Latent Potential & Mentor (16.5s - 21.0s, dur 4.5s)
    {"type": "split", "st": 16.5, "et": 21.0, "raw_ss": 2004.5},

    # 06. B-Roll 3: Golden Sunrise / Awakening Power (21.0s - 24.5s, dur 3.5s)
    {"type": "broll", "st": 21.0, "et": 24.5, "file": BROLLS_DIR / "broll_golden_sunrise.mp4", "broll_ss": 3.0},

    # 07. Split-Screen: Second is Loyalty (24.5s - 29.5s, dur 5.0s)
    {"type": "split", "st": 24.5, "et": 29.5, "raw_ss": 2012.5},

    # 08. B-Roll 4: Business / Colleague Work Environment (29.5s - 34.0s, dur 4.5s)
    {"type": "broll", "st": 29.5, "et": 34.0, "file": BROLLS_DIR / "broll_business.mp4", "broll_ss": 5.0},

    # 09. Split-Screen: Friend's Staff Left Without Word (34.0s - 39.0s, dur 5.0s)
    {"type": "split", "st": 34.0, "et": 39.0, "raw_ss": 2022.0},

    # 10. B-Roll 5: Purpose / Direction & Devotion (39.0s - 43.5s, dur 4.5s)
    {"type": "broll", "st": 39.0, "et": 43.5, "file": BROLLS_DIR / "broll_purpose_direction.mp4", "broll_ss": 2.0},

    # 11. Split-Screen: People Lack Loyalty Today (43.5s - 48.5s, dur 5.0s)
    {"type": "split", "st": 43.5, "et": 48.5, "raw_ss": 2031.5},

    # 12. B-Roll 6: Crowd / Modern Society Live Example (48.5s - 53.5s, dur 5.0s)
    {"type": "broll", "st": 48.5, "et": 53.5, "file": BROLLS_DIR / "broll_crowd_promenade.mp4", "broll_ss": 4.0},

    # 13. Split-Screen: Painful to Witness Lack of Loyalty (53.5s - 59.0s, dur 5.5s)
    {"type": "split", "st": 53.5, "et": 59.0, "raw_ss": 2041.5},

    # 14. B-Roll 7: Majestic Mountains / Hanuman Selfless Loyalty (59.0s - 64.0s, dur 5.0s)
    {"type": "broll", "st": 59.0, "et": 64.0, "file": BROLLS_DIR / "broll_mountains.mp4", "broll_ss": 3.0},

    # 15. Split-Screen: Final Climax - Life's Greatest Lesson (64.0s - 69.5s, dur 5.5s)
    {"type": "split", "st": 64.0, "et": 69.5, "raw_ss": 2052.0},

    # 16. Outro Card: Centered White Channel Card & Subscribe Animation (69.5s - 74.0s, dur 4.5s)
    {"type": "outro", "st": 69.5, "et": 74.0}
]

# 3. Center-Seam Highlight Callout Banners
# Displayed ONLY on key hooks, dates, percentages, and takeaways (NOT every word)
# (start_sec, end_sec, supporting_text, focal_keyword)
CALLOUT_BANNERS = [
    # Hook 1: Host core question
    (3.0, 6.8, "LESSON FROM RAMAYANA", "WHAT SHOULD WE LEARN?"),

    # Hook 2: Guest Hanuman statement
    (10.5, 14.8, "EVERY HUMAN BEING", "EVERYBODY IS HANUMAN!"),

    # Takeaway 1: Latent Potential
    (16.5, 20.0, "HIDDEN POWER", "LATENT POTENTIAL"),

    # Takeaway 2: The Mentor
    (20.2, 24.2, "TO AWAKEN YOUR POWER", "YOU NEED A MENTOR!"),

    # Key Principle: Unconditional Loyalty
    (24.5, 28.5, "THE GREATEST PRINCIPLE", "UNCONDITIONAL LOYALTY"),

    # Key Stat / Live Example: 2 Years
    (30.5, 35.5, "AFTER 2 YEARS OF WORK", "LEFT WITHOUT LOYALTY!"),

    # Takeaway 3: Loyalty stands by you
    (40.2, 44.0, "REAL DEDICATION", "LOYALTY STANDS BY YOU!"),

    # Current Reality: Lack of loyalty
    (46.5, 51.5, "IN TODAY'S WORLD", "PEOPLE LACK LOYALTY!"),

    # Final Climax: Selfless Loyalty
    (64.5, 69.2, "HANUMAN'S LIFE TRUTH", "SELFLESS DEDICATION!")
]

# Build Video Segments
SEGS_DIR = WORKSPACE / "ref4_segs"
SEGS_DIR.mkdir(parents=True, exist_ok=True)

vf_host = (
    "crop=2160:1920:1530:120,scale=1080:960:flags=lanczos,"
    "eq=contrast=1.08:saturation=0.92:brightness=-0.01,"
    "colorbalance=rs=0.03:gs=0.01:bs=-0.03,setsar=1,fps=30"
)
vf_guest = (
    "crop=2160:1920:190:120,scale=1080:960:flags=lanczos,"
    "eq=contrast=1.08:saturation=0.92:brightness=-0.01,"
    "colorbalance=rs=0.03:gs=0.01:bs=-0.03,setsar=1,fps=30"
)

seg_files = []

print("🎬 Generating Reference 4 visual segments...")
for idx, item in enumerate(CUTS_SCHEDULE):
    seg_mp4 = SEGS_DIR / f"seg_{idx:02d}.mp4"
    dur = item["et"] - item["st"]

    if item["type"] == "split":
        # Render 50/50 vertical split-screen from 202.MOV
        raw_ss = item["raw_ss"]
        fc = f"[0:v]{vf_host}[top];[0:v]{vf_guest}[bot];[top][bot]vstack=inputs=2[v]"
        cmd = [
            "ffmpeg", "-y", "-ss", f"{raw_ss:.2f}", "-t", f"{dur:.2f}",
            "-i", str(RAW_VIDEO),
            "-filter_complex", fc, "-map", "[v]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            str(seg_mp4)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    elif item["type"] == "broll":
        # Render 16:9 B-roll centered in 1080x1920 on pure black canvas (letterbox)
        b_file = item["file"]
        b_ss = item.get("broll_ss", 0.0)
        vf_broll = (
            "scale=1080:608:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,"
            "setsar=1,fps=30"
        )
        cmd = [
            "ffmpeg", "-y", "-ss", f"{b_ss:.2f}", "-t", f"{dur:.2f}",
            "-i", str(b_file),
            "-vf", vf_broll,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            str(seg_mp4)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    elif item["type"] == "outro":
        # Render Outro card animation:
        # First 1.5s: Red Subscribe Button
        # Next 3.0s: Clicked Subscribed Button
        total_outro_frames = int(round(dur * 30))
        font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
        font_btn = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
        font_outro = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
        font_av = ImageFont.truetype(str(ASSETS_DIR / "fonts" / "Anton-Regular.ttf"), 56)

        def make_outro_img(is_clicked):
            im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
            draw = ImageDraw.Draw(im)
            card_x0, card_y0 = 160, 720
            card_x1, card_y1 = 920, 1060
            draw.rounded_rectangle([(card_x0-4, card_y0-4), (card_x1+4, card_y1+4)], radius=24, fill=(30, 30, 30, 180))
            draw.rounded_rectangle([(card_x0, card_y0), (card_x1, card_y1)], radius=20, fill=(255, 255, 255, 255))

            av_cx, av_cy, av_r = 270, 840, 52
            draw.ellipse([(av_cx - av_r, av_cy - av_r), (av_cx + av_r, av_cy + av_r)], fill=(235, 130, 7, 255))
            draw.text((av_cx - 16, av_cy - 36), "P", font=font_av, fill=(255, 255, 255, 255))

            draw.text((360, 810), "VIRAL PODCAST", font=font_bold, fill=(15, 15, 15, 255))
            draw.text((360, 856), "@tamilpodcast • 1.2M subscribers", font=font_sub, fill=(100, 100, 100, 255))

            btn_x0, btn_y0 = 360, 930
            btn_x1, btn_y1 = 640, 1000
            if not is_clicked:
                draw.rounded_rectangle([(btn_x0, btn_y0), (btn_x1, btn_y1)], radius=35, fill=(230, 33, 23, 255))
                draw.text((btn_x0 + 44, btn_y0 + 18), "SUBSCRIBE", font=font_btn, fill=(255, 255, 255, 255))
            else:
                draw.rounded_rectangle([(btn_x0, btn_y0), (btn_x1 + 40, btn_y1)], radius=35, fill=(40, 40, 40, 255))
                draw.text((btn_x0 + 32, btn_y0 + 18), "🔔 SUBSCRIBED", font=font_btn, fill=(255, 255, 255, 255))

            text_yt = "▶ Watch full video on YouTube"
            bbox_yt = draw.textbbox((0, 0), text_yt, font=font_outro)
            yt_w = bbox_yt[2] - bbox_yt[0]
            draw.text((540 - yt_w // 2, 1140), text_yt, font=font_outro, fill=(255, 255, 255, 255))
            return im.convert("RGB").tobytes()

        raw_unsub = make_outro_img(False)
        raw_sub = make_outro_img(True)

        p_outro = subprocess.Popen([
            "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
            "-framerate", "30", "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            str(seg_mp4)
        ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        for f_idx in range(total_outro_frames):
            is_clicked = (f_idx >= 45) # Click at 1.5s
            p_outro.stdin.write(raw_sub if is_clicked else raw_unsub)
        p_outro.stdin.close()
        p_outro.wait()

    seg_files.append(seg_mp4)

# Concat all visual segments
concat_txt = WORKSPACE / "ref4_segs_concat.txt"
concat_txt.write_text("\n".join([f"file '{p}'" for p in seg_files]) + "\n")
base_visual_mp4 = WORKSPACE / "ref4_base_visual.mp4"
print("🎬 Concatenating Reference 4 visual track...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c", "copy", str(base_visual_mp4)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 4. Center-Seam Highlight Callout Banners Generator (MOV with alpha)
print("🎬 Rendering Center-Seam Highlight Callout Banners...")
font_support = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf", 34)
font_focal = ImageFont.truetype(str(ASSETS_DIR / "fonts" / "Anton-Regular.ttf"), 64)

def render_banner_frame(banner_data):
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    if not banner_data:
        return im.tobytes()

    sup_text, focal_text = banner_data
    draw = ImageDraw.Draw(im)

    # Center seam at Y=960, strip height 150px (Y=885..1035)
    y_top = 885
    y_bot = 1035

    # 1. Full-width semi-transparent dark horizontal strip
    draw.rectangle([(0, y_top), (WIDTH, y_bot)], fill=(12, 12, 12, 215))

    # 2. Thin white horizontal top and bottom border lines
    draw.line([(0, y_top), (WIDTH, y_top)], fill=(255, 255, 255, 255), width=2)
    draw.line([(0, y_bot), (WIDTH, y_bot)], fill=(255, 255, 255, 255), width=2)

    # 3. Supporting words: Medium white bold-italic sans-serif
    sup_bbox = draw.textbbox((0, 0), sup_text, font=font_support)
    sup_w = sup_bbox[2] - sup_bbox[0]
    draw.text((540 - sup_w // 2, 902), sup_text, font=font_support, fill=(255, 255, 255, 255))

    # 4. Focal keyword: Large golden-yellow stylized/bold font with drop shadow
    focal_bbox = draw.textbbox((0, 0), focal_text, font=font_focal)
    focal_w = focal_bbox[2] - focal_bbox[0]

    # Drop shadow
    draw.text((540 - focal_w // 2 + 4, 948 + 4), focal_text, font=font_focal, fill=(0, 0, 0, 200))
    # Golden-Yellow with solid dark stroke
    draw.text(
        (540 - focal_w // 2, 948), focal_text, font=font_focal,
        fill=(255, 204, 0, 255), # Golden-Yellow
        stroke_width=2, stroke_fill=(0, 0, 0, 220)
    )

    return im.tobytes()

banners_mov = WORKSPACE / "ref4_banners.mov"
p_banner = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{HEIGHT}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(banners_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_banner_frames = int(round(TOTAL_DUR * 30))
blank_banner_bytes = render_banner_frame(None)

for f_idx in range(total_banner_frames):
    t_sec = f_idx / 30.0
    active_b = None
    # Don't show banners during outro
    if t_sec < 69.5:
        for st, et, sup_t, foc_t in CALLOUT_BANNERS:
            if st <= t_sec < et:
                active_b = (sup_t, foc_t)
                break
    p_banner.stdin.write(render_banner_frame(active_b) if active_b else blank_banner_bytes)

p_banner.stdin.close()
p_banner.wait()
print(f"✅ Center-seam highlight banners rendered: {banners_mov}")

# 5. Master Assembly & Sound Mixing
final_out = EXPORT_DIR / "Reel_1_Reference_4_Style.mp4"
print(f"🎬 Assembling Final Reference 4 Reel to: {final_out}")

filter_complex = (
    f"[0:v][1:v]overlay=0:0[v];"
    f"[3:a]volume=0.06,afade=t=in:ss=0:d=1.0,afade=t=out:st=71.5:d=2.5[bgm];"
    f"[2:a][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[a]"
)

subprocess.run([
    "ffmpeg", "-y",
    "-i", str(base_visual_mp4),
    "-i", str(banners_mov),
    "-i", str(pro_dialogue),
    "-i", str(bgm_music),
    "-filter_complex", filter_complex,
    "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
    "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
    "-shortest",
    "-movflags", "+faststart",
    str(final_out)
], check=True)

print(f"🎉 FINAL REEL 1 IN REFERENCE 4 STYLE EXPORTED: {final_out}")

# Extract Verification QA Frames
subprocess.run(["ffmpeg", "-y", "-ss", "2.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_split_t2.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "5.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t5.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "6.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t6.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "12.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t12.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "15.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t15.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "22.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t22.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "32.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t32.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "47.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t47.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "61.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t61.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "72.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_outro_t72.0s.png")], check=True)
print("✅ Reference 4 QA verification frames extracted successfully!")
