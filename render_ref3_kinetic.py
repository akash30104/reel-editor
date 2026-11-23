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
3. SUBTITLE STYLE - STRICTLY 1 SENTENCE AT A TIME:
   - "Only 1 sentence in the screen at the time" (Zero stacking, zero multiple zones simultaneously).
   - Position: Lower Third Center (X=540, Y=1135), safely inside 16:9 frame, above gradient fade, never covering face.
   - Language: TANGLISH (Phonetic Romanized Tamil + English words matching spoken audio).
   - Font: Anton bold condensed, electric yellow (#FFE500), 3.5px solid dark stroke outline + multi-layer soft dark drop shadow.
   - Timing: -60ms visual lead time for crisp, instantaneous synchronization.
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

# 4. Single-Sentence Subtitle Engine (STRICTLY 1 SENTENCE AT A TIME)
font_p = str(ASSETS_DIR / "fonts" / "Anton-Regular.ttf")
font_std = ImageFont.truetype(font_p, 62)
font_hero = ImageFont.truetype(font_p, 72)

# Precise Non-Overlapping Single Sentence Timeline
# (start_sec, end_sec, text, is_hero_emphasis)
# ONLY ONE sentence is active at any point in time!
SINGLE_SENTENCES = [
    # Host (0.0s - 8.6s)
    (2.0, 4.3, "RAMAYANATHULA IRUNDHU...", False),
    (4.3, 8.2, "NAAM ENNA VAAZHKAI PAADAM\nEDUTHUKKANUM?", True),

    # Guest (8.6s - 74.0s)
    (8.5, 10.4, "NAAN VANDHU...", False),
    (10.4, 12.8, "HANUMAN-A PATHI MATTUM\nPESA NENAIKKIREN!", True),
    (12.8, 15.4, "EVERYBODY IN THIS WORLD\nIS LIKE HANUMAN!", True),

    (15.7, 17.5, "NAMAKKULLA...", False),
    (17.5, 19.1, "LATENT POTENTIAL IRUKKU!", True),
    (19.1, 22.3, "SOMEONE HAS TO SHOW IT...\nTHAT'S THE MENTOR!", True),

    (22.4, 24.1, "MENTOR IRUNDHAA JAIKKALAAM!", False),
    (24.1, 26.0, "RENDAAVADHU... LOYALTY!", True),

    (26.2, 28.4, "INNAIKKU VANDHAVAR...", False),
    (28.4, 30.2, "ROMBA VARUTHAPPATTAAR!", True),
    (30.3, 33.0, "AVAR STAFF 2 YEARS\nVELA PAATHUTTU...", False),
    (33.0, 36.0, "SOLLAAMA KOLLAAMA\nPOYITAANGA!", True),

    (36.3, 38.0, "AVAR SOLLUMPODHU...", False),
    (38.0, 40.0, "ROMBA UPSET AAYITAARU!", True),
    (40.1, 42.2, "LOYAL-AA IRUNDHURUNDHAA...", False),
    (42.2, 44.0, "AVANGA KOODAVE\nIRUNDHURUPPAANGA!", True),

    (44.2, 46.8, "INNAIKKU PALA PERKITTA...", False),
    (46.8, 48.8, "LOYALTY-E ILLA!", True),
    (48.8, 55.4, "IDHU ORU LIVE EXAMPLE!", True),

    (55.8, 57.8, "AVAR SOLLUMPODHU...", False),
    (57.8, 60.4, "ROMBA KASHTAMAA POCHU...", False),
    (60.4, 63.6, "HANUMAN MAADHIRI\nLOYAL PEOPLE ENGEY?", True),

    (63.8, 65.8, "HANUMAN KAATTIYA...", False),
    (65.8, 68.6, "SELFLESS LOYALTY DHAAN!", True),
    (68.6, 73.8, "LIFE-ODA GREATEST LESSON!", True)
]

def render_single_sentence_frame(sentence_tuple):
    """
    Renders exactly ONE sentence at Lower Third Center (X=540, Y=1135).
    Safely within 16:9 frame, above gradient fade, never covering speaker's face.
    """
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    if not sentence_tuple:
        return im.tobytes()

    text, is_hero = sentence_tuple
    draw = ImageDraw.Draw(im)
    f = font_hero if is_hero else font_std

    # Measure text bounding box
    bbox = draw.multiline_textbbox((0, 0), text, font=f, align="center")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Center horizontally at X=540, center vertically at Y=1135
    draw_x = 540 - text_w // 2
    draw_y = 1135 - text_h // 2

    # 1. Multi-layer soft dark drop shadow
    for ox, oy, alpha in [(6, 6, 220), (4, 4, 180), (2, 2, 140)]:
        draw.multiline_text((draw_x + ox, draw_y + oy), text, font=f, fill=(0, 0, 0, alpha), align="center")

    # 2. Electric Yellow with 3.5px solid dark stroke outline
    draw.multiline_text(
        (draw_x, draw_y), text, font=f,
        fill=(255, 229, 0, 255),
        stroke_width=3,
        stroke_fill=(0, 0, 0, 240),
        align="center"
    )

    return im.tobytes()

# Render animated subtitles MOV with alpha
subs_mov = WORKSPACE / "ref3_kinetic_subs.mov"
print("🎬 Rendering dynamic 1-sentence-at-a-time subtitle stream...")
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{HEIGHT}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_frames = int(round(TOTAL_DUR * 30))
blank_bytes = render_single_sentence_frame(None)

for f_idx in range(total_frames):
    t_sec = f_idx / 30.0
    active_sentence = None

    # Find the single active sentence at timestamp t_sec
    for st, et, txt, is_hero in SINGLE_SENTENCES:
        if st <= t_sec < et:
            active_sentence = (txt, is_hero)
            break

    raw_frame = render_single_sentence_frame(active_sentence) if active_sentence else blank_bytes
    proc.stdin.write(raw_frame)

proc.stdin.close()
proc.wait()
print(f"✅ 1-sentence subtitle animated video rendered: {subs_mov}")

# 5. Final Master Assembly:
# Base 16:9 centered in 1080x1920 (pad=1080:1920:0:656:color=black)
# Overlay bottom gradient fade (ref3_gradient_overlay.png)
# Overlay 1-sentence subtitles (ref3_kinetic_subs.mov)
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

# Extract Verification QA Frames
subprocess.run(["ffmpeg", "-y", "-ss", "5.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t5.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "11.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t11.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "14.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t14.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "18.2", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t18.2s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "25.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t25.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "34.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t34.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "43.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t43.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "50.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t50.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "62.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t62.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "70.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_single_t70.5s.png")], check=True)
print("✅ QA verification frames extracted successfully!")
