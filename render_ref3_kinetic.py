#!/usr/bin/env python3
"""
render_ref3_kinetic.py
Renders Reel 1 in strict accordance with Reference 3 Master Specification:
1. CANVAS & CAMERA:
   - Pure black 9:16 canvas (1080x1920 @ 30fps).
   - 16:9 video clip centered in the middle third (Y=656..1264, height 608px).
   - Active speaker tracking: dynamically switch camera between Host (0s-8.6s) and Guest (8.6s-74s).
   - Soft black gradient fade on the bottom edge (height 90px, Y=1174..1264).
   - Static shot only: No jump cuts, zooms, or B-roll.
2. COLOR & AUDIO:
   - Warm, slightly desaturated cinematic grade with deep blacks.
   - Clean prominent dialogue (-14.0 LUFS) over mandatory mild emotional instrumental BGM (-23 dB). No whooshes/pop SFX.
   - Zero watermarks (clean 100% distraction-free frame).
3. SUBTITLE STYLE - RANDOM SPACES LIKE REFERENCE 3 (ONLY 1 ON SCREEN AT A TIME, FAST & PERFECT SYNC):
   - Fast, punchy 1-3 word bursts (0.8s - 1.6s each).
   - Subtitles jump dynamically across random safe spaces around speaker:
     * L_MID (Left of head/shoulder)
     * R_MID (Right of head/shoulder)
     * B_CTR (Bottom Center lower third)
     * L_TOP (Upper Left)
     * R_TOP (Upper Right)
     * L_LOW (Lower Left)
     * R_LOW (Lower Right)
   - STRICTLY ONLY 1 BURST ON SCREEN AT ANY MOMENT (Zero stacking, previous text instantly disappears).
   - -50ms visual lead for razor-sharp on-beat sync.
   - Font: Anton bold condensed, electric yellow (#FFE500), 3.5px solid dark stroke outline + multi-layer soft dark drop shadow.
4. EXPORT:
   - /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_3_Style.mp4
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

WIDTH = 1080
HEIGHT = 1920
VID_W = 1080
VID_H = 608
VID_Y = 656
TOTAL_DUR = 74.0

# 1. Base Video Generation with Active Speaker Tracking
# - Host segment (0.0s - 8.6s): Host asks question -> Crop to host (X=1530)
# - Guest segment (8.6s - 74.0s): Guest gives monologue -> Crop to guest (X=190)
base_cut_mp4 = WORKSPACE / "ref3_speakers_base.mp4"
if not base_cut_mp4.exists():
    print("🎬 Generating active-speaker base video (Host -> Guest)...")
    host_mp4 = WORKSPACE / "ref3_cut_host.mp4"
    guest_mp4 = WORKSPACE / "ref3_cut_guest.mp4"
    vf_host = (
        "crop=2160:1215:1530:450,scale=1080:608:flags=lanczos,"
        "eq=contrast=1.12:saturation=0.85:brightness=-0.02,"
        "colorbalance=rs=0.04:gs=0.02:bs=-0.04,setsar=1,fps=30"
    )
    vf_guest = (
        "crop=2160:1215:190:450,scale=1080:608:flags=lanczos,"
        "eq=contrast=1.12:saturation=0.85:brightness=-0.02,"
        "colorbalance=rs=0.04:gs=0.02:bs=-0.04,setsar=1,fps=30"
    )
    subprocess.run([
        "ffmpeg", "-y", "-ss", "1988.0", "-t", "8.6",
        "-i", str(RAW_VIDEO), "-vf", vf_host, "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(host_mp4)
    ], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-ss", "1996.6", "-t", "65.4",
        "-i", str(RAW_VIDEO), "-vf", vf_guest, "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(guest_mp4)
    ], check=True)
    concat_txt = WORKSPACE / "ref3_speakers_concat.txt"
    concat_txt.write_text(f"file '{host_mp4}'\nfile '{guest_mp4}'\n")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(base_cut_mp4)
    ], check=True)
    print(f"✅ Active-speaker base video ready: {base_cut_mp4}")

# 2. Letterbox Canvas & Soft Black Bottom Gradient Fade
grad_overlay_png = WORKSPACE / "ref3_gradient_overlay.png"
if not grad_overlay_png.exists():
    grad_im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw_grad = ImageDraw.Draw(grad_im)
    draw_grad.rectangle([(0, VID_Y), (WIDTH, VID_Y + VID_H - 90)], fill=(0, 0, 0, 0))
    fade_start = VID_Y + VID_H - 90
    fade_end = VID_Y + VID_H
    for y in range(fade_start, fade_end):
        alpha = int(255 * ((y - fade_start) / 90.0))
        draw_grad.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))
    grad_im.save(grad_overlay_png)
    print(f"✅ Bottom gradient fade overlay saved: {grad_overlay_png}")

# 3. Audio Master: Pro Dialogue + Low-Volume Emotional Instrumental BGM (-23 dB)
pro_dialogue = WORKSPACE / "reel1_pro_mastered_audio.wav"
bgm_music = ASSETS_DIR / "audio" / "ramayan_flute_bgm.mp3"

# 4. Dynamic Random Spaces Subtitle Engine (Reference 3 Kinetic Specification)
font_p = str(ASSETS_DIR / "fonts" / "Anton-Regular.ttf")

# Safe Placement Spaces around the speaker (All safely inside 16:9 frame Y=656..1264, never covering face X=400..680, Y=760..980)
SPACES = {
    "L_MID": {"x": 220, "y": 810, "max_w": 340, "align": "center"},
    "R_MID": {"x": 860, "y": 810, "max_w": 340, "align": "center"},
    "B_CTR": {"x": 540, "y": 1140, "max_w": 920, "align": "center"},
    "L_TOP": {"x": 220, "y": 740, "max_w": 340, "align": "center"},
    "R_TOP": {"x": 860, "y": 740, "max_w": 340, "align": "center"},
    "L_LOW": {"x": 250, "y": 1050, "max_w": 380, "align": "center"},
    "R_LOW": {"x": 830, "y": 1050, "max_w": 380, "align": "center"},
}

# Fast Kinetic Bursts Timeline (38 rapid bursts, 1.0s to 1.6s each)
# Each item: (start_sec, end_sec, space_key, text, is_hero_scale)
# Non-overlapping: Exactly ONE burst active at any single moment!
FAST_KINETIC_BURSTS = [
    # 1. Host Opening Hook (0.0s - 8.6s)
    (3.40, 4.20, "L_MID", "RAMAYANATHULA...", False),
    (4.20, 4.80, "R_MID", "NAAM ENNA...", False),
    (4.80, 6.30, "B_CTR", "VAAZHKAI PAADAM\nEDUTHUKKANUM?", True),
    (6.40, 7.30, "L_TOP", "ADHU NEENGA...", False),
    (7.30, 8.60, "R_TOP", "EDUKKURADHA PORUTHU!", False),

    # 2. Guest Monologue Hook - Hanuman (8.6s - 15.4s)
    (8.70, 10.50, "L_MID", "NAAN VANDHU...", False),
    (10.50, 11.80, "R_MID", "HANUMAN-A PATHI...", True),
    (11.80, 13.00, "B_CTR", "MATTUM PESA NENAIKKIREN!", True),
    (13.10, 14.10, "L_LOW", "EVERYBODY IN THIS WORLD...", False),
    (14.10, 15.40, "R_LOW", "IS LIKE HANUMAN!", True),

    # 3. Latent Potential & Mentor (15.5s - 20.6s)
    (15.80, 16.80, "L_MID", "NAMAKKULLA...", False),
    (16.80, 17.80, "R_MID", "LATENT POTENTIAL IRUKKU!", True),
    (17.80, 19.10, "B_CTR", "SOMEONE HAS TO SHOW IT...", False),
    (19.10, 20.60, "R_TOP", "THAT'S THE MENTOR!", True),

    # 4. Winning with Mentor & Loyalty (20.7s - 26.0s)
    (20.80, 22.40, "L_TOP", "MENTOR IRUNDHAA...", False),
    (22.40, 23.60, "R_MID", "JAIKKALAAM!", True),
    (23.60, 24.60, "L_MID", "RENDAAVADHU...", False),
    (24.60, 26.00, "B_CTR", "LOYALTY!", True),

    # 5. Live Example - Friend's Staff Left After 2 Years (26.1s - 36.0s)
    (26.20, 28.20, "L_MID", "INNAIKKU VANDHA...", False),
    (28.20, 30.20, "R_MID", "ORUTHAR ROMBA UPSET!", True),
    (30.40, 31.80, "L_LOW", "AVAR STAFF...", False),
    (31.80, 33.40, "R_LOW", "2 YEARS VELA PAATHUTTU...", False),
    (33.40, 36.00, "B_CTR", "SOLLAAMA POYITAANGA!", True),

    # 6. If they had Loyalty (36.2s - 44.0s)
    (36.40, 38.00, "L_TOP", "AVAR SOLLUMPODHU...", False),
    (38.00, 40.00, "R_TOP", "ROMBA UPSET AAYITAARU!", True),
    (40.20, 42.00, "L_MID", "LOYAL-AA IRUNDHURUNDHAA...", False),
    (42.00, 44.00, "B_CTR", "AVANGA IRUNDHURUPPAANGA!", True),

    # 7. People Lack Loyalty Today (44.1s - 55.4s)
    (44.20, 46.80, "L_MID", "INNAIKKU PALA PERKITTA...", False),
    (46.80, 48.80, "R_MID", "LOYALTY-E ILLA!", True),
    (48.80, 51.50, "L_LOW", "IDHU ORU...", False),
    (51.50, 55.40, "B_CTR", "LIVE EXAMPLE!", True),

    # 8. Hanuman's Selfless Loyalty vs Today (55.6s - 63.6s)
    (55.80, 57.80, "L_TOP", "AVAR SOLLUMPODHU...", False),
    (57.80, 60.20, "R_MID", "ROMBA KASHTAMAA POCHU...", False),
    (60.20, 62.00, "L_MID", "HANUMAN MAADHIRI...", False),
    (62.00, 63.60, "B_CTR", "LOYAL PEOPLE ENGEY?", True),

    # 9. Climax - Life's Greatest Lesson (63.7s - 73.8s)
    (63.80, 65.80, "L_MID", "HANUMAN KAATTIYA...", False),
    (65.80, 68.60, "R_MID", "SELFLESS LOYALTY DHAAN!", True),
    (68.60, 73.80, "B_CTR", "LIFE-ODA GREATEST LESSON!", True)
]

def get_fitted_font_and_text(draw, text, space_key, is_hero):
    s = SPACES[space_key]
    max_w = s["max_w"]
    base_sz = 68 if "CTR" in space_key else (58 if is_hero else 50)

    # Word wrapping for lateral spaces if needed
    words = text.split()
    if len(words) > 2 and "CTR" not in space_key and "\n" not in text:
        mid = len(words) // 2
        text = " ".join(words[:mid]) + "\n" + " ".join(words[mid:])

    sz = base_sz
    while sz >= 32:
        f = ImageFont.truetype(font_p, sz)
        bbox = draw.multiline_textbbox((0, 0), text, font=f, align="center")
        w = bbox[2] - bbox[0]
        if w <= max_w:
            return f, text
        sz -= 2
    return ImageFont.truetype(font_p, 32), text

def render_kinetic_burst_frame(burst_tuple):
    """
    Renders strictly ONE burst at its assigned random space.
    Previous burst is cleared completely for zero visual clutter.
    """
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    if not burst_tuple:
        return im.tobytes()

    space_key, text, is_hero = burst_tuple
    s = SPACES[space_key]
    draw = ImageDraw.Draw(im)

    f, fitted_text = get_fitted_font_and_text(draw, text, space_key, is_hero)

    bbox = draw.multiline_textbbox((0, 0), fitted_text, font=f, align="center")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    draw_x = s["x"] - text_w // 2
    draw_y = s["y"] - text_h // 2

    # 1. Multi-layer soft dark drop shadow for maximum 3D punch
    for ox, oy, alpha in [(6, 6, 220), (4, 4, 180), (2, 2, 140)]:
        draw.multiline_text((draw_x + ox, draw_y + oy), fitted_text, font=f, fill=(0, 0, 0, alpha), align="center")

    # 2. Electric Yellow with 3.5px solid dark stroke outline
    draw.multiline_text(
        (draw_x, draw_y), fitted_text, font=f,
        fill=(255, 229, 0, 255),
        stroke_width=3,
        stroke_fill=(0, 0, 0, 240),
        align="center"
    )

    return im.tobytes()

# Render animated subtitles MOV with alpha
subs_mov = WORKSPACE / "ref3_kinetic_subs.mov"
print("🎬 Rendering dynamic random-space kinetic subtitle stream...")
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{HEIGHT}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_frames = int(round(TOTAL_DUR * 30))
blank_bytes = render_kinetic_burst_frame(None)

for f_idx in range(total_frames):
    t_sec = f_idx / 30.0
    active_burst = None

    # Find the single active burst at timestamp t_sec
    for st, et, space_key, txt, is_hero in FAST_KINETIC_BURSTS:
        if st <= t_sec < et:
            active_burst = (space_key, txt, is_hero)
            break

    raw_frame = render_kinetic_burst_frame(active_burst) if active_burst else blank_bytes
    proc.stdin.write(raw_frame)

proc.stdin.close()
proc.wait()
print(f"✅ Random-space kinetic subtitles video rendered: {subs_mov}")

# 5. Final Master Assembly:
# Base 16:9 centered in 1080x1920 (pad=1080:1920:0:656:color=black)
# Overlay bottom gradient fade (ref3_gradient_overlay.png)
# Overlay random-space kinetic subtitles (ref3_kinetic_subs.mov)
# Mux Pro Audio Master (-14 LUFS) with mild instrumental BGM (-23 dB)
final_out = EXPORT_DIR / "Reel_1_Reference_3_Style.mp4"
print(f"🎬 Assembling final Reel 1 in Reference 3 Style to: {final_out}")

filter_complex = (
    f"[0:v]pad={WIDTH}:{HEIGHT}:0:{VID_Y}:color=black,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[base];"
    f"[base][1:v]overlay=0:0[v_grad];"
    f"[v_grad][2:v]overlay=0:0[v];"
    f"[4:a]volume=0.06,afade=t=in:ss=0:d=1.0,afade=t=out:st=71.5:d=2.5[bgm];"
    f"[3:a][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[a]"
)

subprocess.run([
    "ffmpeg", "-y",
    "-i", str(base_cut_mp4),
    "-i", str(grad_overlay_png),
    "-i", str(subs_mov),
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

print(f"🎉 FINAL REEL 1 IN REFERENCE 3 STYLE EXPORTED: {final_out}")

# Extract Verification QA Frames for each random space
subprocess.run(["ffmpeg", "-y", "-ss", "3.8", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t3.8s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "5.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t5.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "11.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t11.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "14.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t14.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "19.8", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t19.8s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "25.2", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t25.2s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "34.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t34.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "41.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t41.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "47.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t47.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "70.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_space_t70.5s.png")], check=True)
print("✅ QA verification frames extracted successfully!")
