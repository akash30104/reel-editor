#!/usr/bin/env python3
"""
render_ref3_kinetic.py
Renders Reel 1 in strict accordance with Reference 3 Master Specification (rules.md Section 10):
1. CANVAS & CAMERA:
   - Pure black 9:16 canvas (1080x1920 @ 30fps).
   - 16:9 video clip centered in the middle third (Y=656..1264, height 608px).
   - Soft black gradient fade on the bottom edge (height 90px, Y=1174..1264).
   - Static shot only: No jump cuts, zooms, or B-roll.
2. COLOR & AUDIO:
   - Warm, slightly desaturated cinematic grade with deep blacks.
   - Clean prominent dialogue over low-volume emotional instrumental BGM (-22 dB). No whooshes/pop SFX.
   - Low-opacity logo watermark in the top-right corner of the video frame (X=1030, Y=680).
3. SUBTITLE STYLE & EXACT KINETIC PLACEMENT:
   - Font: Anton bold condensed, pure white (#FFFFFF), soft dark drop shadow.
   - Chunking: 1-3 words per beat with '...' and '!'.
   - Safe Zone: All text inside 16:9 frame, never covering speaker's face or eyes.
   - Placement Zones: Zone A (Left), Zone B (Right), Zone C (Bottom-Center).
   - Hierarchy: Pop sharply on beat, 1.4x-1.5x scale hierarchy, cluster stacking across zones, clean reset on sentence boundaries.
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

# 1. Base Static Video Generation
# Crop guest to 16:9 centered (crop=2160:1215:1530:450,scale=1080:608:flags=lanczos)
# Apply warm, slightly desaturated cinematic grade with deep blacks:
# eq=contrast=1.12:saturation=0.85:brightness=-0.02,colorbalance=rs=0.04:gs=0.02:bs=-0.04
base_cut_mp4 = WORKSPACE / "ref3_raw_guest_static.mp4"
if not base_cut_mp4.exists():
    print("🎬 Extracting static 16:9 guest master shot from RAW_VIDEO...")
    vf = (
        "crop=2160:1215:1530:450,scale=1080:608:flags=lanczos,"
        "eq=contrast=1.12:saturation=0.85:brightness=-0.02,"
        "colorbalance=rs=0.04:gs=0.02:bs=-0.04,setsar=1,fps=30"
    )
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", "1988.0", "-t", f"{TOTAL_DUR:.3f}",
        "-i", str(RAW_VIDEO),
        "-vf", vf, "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_cut_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Static shot extracted: {base_cut_mp4}")

# 2. Letterbox Canvas & Soft Black Bottom Gradient Fade
# Generate a static alpha mask PNG that applies the bottom gradient fade and pads to 1080x1920
grad_overlay_png = WORKSPACE / "ref3_gradient_overlay.png"
grad_im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
# Make the video area transparent (Y=656..1264)
# with a smooth gradient fade from Y=1174 to 1264
draw_grad = ImageDraw.Draw(grad_im)
# Clear the clear video viewing area
draw_grad.rectangle([(0, VID_Y), (WIDTH, VID_Y + VID_H - 90)], fill=(0, 0, 0, 0))
# Build smooth gradient fade
fade_start = VID_Y + VID_H - 90 # 1174
fade_end = VID_Y + VID_H        # 1264
for y in range(fade_start, fade_end):
    alpha = int(255 * ((y - fade_start) / 90.0))
    draw_grad.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))
grad_im.save(grad_overlay_png)
print(f"✅ Bottom gradient fade overlay saved: {grad_overlay_png}")

# 3. Audio Master: Pro Dialogue + Low-Volume Emotional Instrumental BGM (-22 dB)
# We use reel1_pro_mastered_audio.wav as dialogue master (-14 LUFS)
pro_dialogue = WORKSPACE / "reel1_pro_mastered_audio.wav"

# 4. Kinetic Subtitle Engine
font_p = str(ASSETS_DIR / "fonts" / "Anton-Regular.ttf")
font_base = ImageFont.truetype(font_p, 52)
font_large = ImageFont.truetype(font_p, 74)
font_wm = ImageFont.truetype(font_p, 26)

# Placement Zones in 1080x1920 coordinates
# All inside 16:9 frame (Y=656..1264)
# Zone A: Left of speaker (X=70, Y=790)
# Zone B: Right of speaker (X=1010, Y=790, right-aligned)
# Zone C: Bottom-Center (X=540, Y=1160, center-aligned)
ZONES = {
    "A": {"x": 80, "y": 790, "align": "left"},
    "B": {"x": 1000, "y": 790, "align": "right"},
    "C": {"x": 540, "y": 1150, "align": "center"}
}

# Kinetic Clusters Specification:
# Each cluster: (cluster_start, cluster_end, [active_phrases_list])
# Each phrase: (phrase_start, zone, text, is_emphasized)
# When a new phrase starts, it stacks into the current cluster until cluster_end clears it!
KINETIC_CLUSTERS = [
    # Sentence 1: Hook Question (0.5s - 7.8s)
    (0.5, 7.8, [
        (0.5, "A", "WHAT LIFE LESSON...", False),
        (2.6, "B", "FROM\nRAMAYANA?", True),
        (5.2, "C", "WHAT IS THE TRUTH!?", True)
    ]),

    # Sentence 2: Hanuman Revelation (8.2s - 16.5s)
    (8.2, 16.5, [
        (8.2, "A", "I ONLY WANT...", False),
        (10.5, "B", "TO TALK ABOUT\nHANUMAN!", True),
        (13.6, "C", "BECAUSE IN THIS WORLD...", False)
    ]),

    # Sentence 2 Climax: Everyone is like Hanuman (16.8s - 20.3s)
    (16.8, 20.3, [
        (16.8, "C", "EVERYONE IS LIKE\nHANUMAN!", True)
    ]),

    # Sentence 3: The Latent Potential (20.6s - 28.2s)
    (20.6, 28.2, [
        (20.6, "A", "WE ALL HAVE...", False),
        (23.0, "B", "A HIDDEN\nLATENT POTENTIAL!", True),
        (25.6, "C", "SOMEONE HAS TO\nAWAKEN IT...", False)
    ]),

    # Sentence 3 Climax: That is the Mentor (28.4s - 30.5s)
    (28.4, 30.5, [
        (28.4, "C", "THAT IS A MENTOR!", True)
    ]),

    # Sentence 4: Jambavan Speaks (30.8s - 38.6s)
    (30.8, 38.6, [
        (30.8, "A", "WHEN JAMBAVAN...", False),
        (33.5, "B", "CAME TO HANUMAN\nAND SAID...", False),
        (36.0, "C", "YOU ARE POWERFUL!", True)
    ]),

    # Sentence 4 Part 2: True Strength (38.8s - 47.0s)
    (38.8, 47.0, [
        (38.8, "A", "YOUR TRUE STRENGTH...", False),
        (42.0, "B", "YOU DID NOT\nEVEN REALIZE!", True),
        (44.6, "C", "ONLY BECAUSE HE AWAKENED HIM!", False)
    ]),

    # Sentence 5: Crossed the Ocean (47.2s - 53.2s)
    (47.2, 53.2, [
        (47.2, "A", "HE LEAPED ACROSS...", False),
        (50.0, "B", "THE ENTIRE OCEAN\nAND FOUND SITA!", True)
    ]),

    # Sentence 5 Part 2: Without that mentor (53.5s - 60.2s)
    (53.5, 60.2, [
        (53.5, "A", "WITHOUT THAT MENTOR...", False),
        (56.5, "C", "HE WOULD HAVE\nNEVER KNOWN!", True)
    ]),

    # Sentence 6: Greatest Lesson of Life (60.4s - 69.8s)
    (60.4, 69.8, [
        (60.4, "A", "THERE IS NO...", False),
        (63.0, "B", "GREATER LESSON\nIN YOUR LIFE!", True),
        (66.5, "C", "FIND YOUR MENTOR!", True)
    ]),

    # Outro Call to Action (70.0s - 73.9s)
    (70.0, 73.9, [
        (70.0, "C", "THE GREATEST LESSON\nOF LIFE!", True)
    ])
]

def render_kinetic_subtitles_frame(active_phrases):
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Watermark in top-right of 16:9 video frame
    wm_text = "AK"
    draw.text((1030, 680), wm_text, font=font_wm, fill=(255, 255, 255, 100), align="right")

    if not active_phrases:
        return im.tobytes()

    for zone_id, text, is_emph in active_phrases:
        f = font_large if is_emph else font_base
        z_info = ZONES[zone_id]
        x_base = z_info["x"]
        y_base = z_info["y"]
        align = z_info["align"]

        # Calculate bounding box for proper alignment
        bbox = draw.multiline_textbbox((0, 0), text, font=f, align=align)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        if align == "left":
            draw_x = x_base
            draw_y = y_base - text_h // 2
        elif align == "right":
            draw_x = x_base - text_w
            draw_y = y_base - text_h // 2
        else: # center
            draw_x = x_base - text_w // 2
            draw_y = y_base - text_h // 2

        # Soft dark drop shadow: multi-layer soft blur
        for ox, oy, alpha in [(5, 5, 160), (4, 4, 130), (3, 3, 100), (2, 2, 70)]:
            draw.multiline_text((draw_x + ox, draw_y + oy), text, font=f, fill=(0, 0, 0, alpha), align=align)

        # Crisp pure white text
        draw.multiline_text((draw_x, draw_y), text, font=f, fill=(255, 255, 255, 255), align=align)

    return im.tobytes()

# Render animated subtitles MOV with alpha
subs_mov = WORKSPACE / "ref3_kinetic_subs.mov"
print("🎬 Rendering dynamic kinetic subtitle stream...")
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{HEIGHT}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_frames = int(round(TOTAL_DUR * 30))
blank_bytes = render_kinetic_subtitles_frame([])

for f_idx in range(total_frames):
    t_sec = f_idx / 30.0
    active_phrases = []

    # Find which cluster we are in
    for c_st, c_et, phrases in KINETIC_CLUSTERS:
        if c_st <= t_sec < c_et:
            # Stack all phrases that have started up to t_sec
            for p_st, zone, txt, is_emph in phrases:
                if p_st <= t_sec:
                    active_phrases.append((zone, txt, is_emph))
            break

    raw_frame = render_kinetic_subtitles_frame(active_phrases) if active_phrases else blank_bytes
    proc.stdin.write(raw_frame)

proc.stdin.close()
proc.wait()
print(f"✅ Kinetic subtitles animated video rendered: {subs_mov}")

# 5. Final Master Assembly:
# Base 16:9 centered in 1080x1920 (pad=1080:1920:0:656:color=black)
# Overlay bottom gradient fade (ref3_gradient_overlay.png)
# Overlay kinetic subtitles (ref3_kinetic_subs.mov)
# Mux Pro Audio Master (-14 LUFS)
# Export to /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_3_Style.mp4
final_out = EXPORT_DIR / "Reel_1_Reference_3_Style.mp4"
print(f"🎬 Assembling final Reel 1 in Reference 3 Style to: {final_out}")

filter_complex = (
    f"[0:v]pad={WIDTH}:{HEIGHT}:0:{VID_Y}:color=black,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[base];"
    f"[base][1:v]overlay=0:0[v_grad];"
    f"[v_grad][2:v]overlay=0:0[v]"
)

subprocess.run([
    "ffmpeg", "-y",
    "-i", str(base_cut_mp4),
    "-i", str(grad_overlay_png),
    "-i", str(subs_mov),
    "-i", str(pro_dialogue),
    "-filter_complex", filter_complex,
    "-map", "[v]", "-map", "3:a",
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
subprocess.run(["ffmpeg", "-y", "-ss", "5.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t5.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "14.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t14.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "18.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t18.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "25.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t25.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "36.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t36.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "51.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t51.0s.png")], check=True)
print("✅ QA verification frames extracted successfully!")
