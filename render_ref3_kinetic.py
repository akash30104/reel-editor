#!/usr/bin/env python3
"""
render_ref3_kinetic.py
Renders Reel 1 in strict accordance with Reference 3 Master Specification (rules.md Section 10):
1. CANVAS & CAMERA:
   - Pure black 9:16 canvas (1080x1920 @ 30fps).
   - 16:9 video clip centered in the middle third (Y=656..1264, height 608px).
   - Active speaker tracking: dynamically switch camera between Host (0s-8s) and Guest (8s-74s).
   - Soft black gradient fade on the bottom edge (height 90px, Y=1174..1264).
   - Static shot only: No jump cuts, zooms, or B-roll.
2. COLOR & AUDIO:
   - Warm, slightly desaturated cinematic grade with deep blacks.
   - Clean prominent dialogue over mandatory mild emotional instrumental BGM (-23 dB). No whooshes/pop SFX.
   - Zero watermarks (clean 100% distraction-free frame).
3. SUBTITLE STYLE & EXACT KINETIC PLACEMENT:
   - Font: Anton bold condensed, electric yellow (#FFE500), soft dark drop shadow.
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

# 1. Base Video Generation with Active Speaker Tracking
# - Host segment (0.0s - 8.6s): Host asks question -> Crop to host (X=1530)
# - Guest segment (8.6s - 74.0s): Guest gives monologue -> Crop to guest (X=190)
# Both cropped to 16:9 (2160x1215), scaled to 1080x608, and color-graded
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

# 3. Audio Master: Pro Dialogue + Low-Volume Emotional Instrumental BGM (-23 dB)
# We use reel1_pro_mastered_audio.wav as dialogue master (-14 LUFS)
pro_dialogue = WORKSPACE / "reel1_pro_mastered_audio.wav"
bgm_music = ASSETS_DIR / "audio" / "ramayan_flute_bgm.mp3"

# 4. Kinetic Subtitle Engine
font_p = str(ASSETS_DIR / "fonts" / "Anton-Regular.ttf")
font_base = ImageFont.truetype(font_p, 52)
font_large = ImageFont.truetype(font_p, 74)

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
    # Sentence 1: Hook Question (2.0s - 8.6s) - Host asks about Ramayana lesson
    (2.0, 8.6, [
        (2.2, "A", "FROM RAMAYANA...", False),
        (4.2, "B", "WHAT LIFE LESSON...", True),
        (6.4, "C", "SHOULD WE LEARN?", True)
    ]),

    # Sentence 2 Part 1: Hanuman Hook (8.6s - 13.4s) - Guest begins monologue
    (8.6, 13.4, [
        (9.0, "A", "I ONLY WANT...", False),
        (11.0, "B", "TO TALK ABOUT\nHANUMAN!", True)
    ]),

    # Sentence 2 Part 2: Everyone is like Hanuman (13.4s - 20.4s)
    (13.4, 20.4, [
        (13.8, "A", "IN THIS WORLD...", False),
        (16.5, "C", "EVERYONE IS LIKE\nHANUMAN!", True)
    ]),

    # Sentence 3: Hidden Latent Potential & Mentor (20.6s - 30.2s)
    (20.6, 30.2, [
        (20.8, "A", "WE HAVE A HIDDEN...", False),
        (23.2, "B", "LATENT POTENTIAL!", True),
        (26.8, "C", "A MENTOR HAS TO\nAWAKEN IT!", True)
    ]),

    # Sentence 4 Part 1: When Jambavan Reminds Him (30.4s - 36.8s)
    (30.4, 36.8, [
        (30.8, "A", "WHEN JAMBAVAN...", False),
        (33.8, "B", "REMINDS HIM...", True)
    ]),

    # Sentence 4 Part 2: Hanuman Realizes True Strength (36.8s - 45.4s)
    (36.8, 45.4, [
        (37.2, "A", "HANUMAN REALIZES...", False),
        (40.8, "C", "HIS TRUE STRENGTH!", True)
    ]),

    # Sentence 5: Unconditional Loyalty & Dedication (45.4s - 59.2s)
    (45.4, 59.2, [
        (45.8, "A", "WHAT PEOPLE LACK TODAY...", False),
        (51.0, "B", "IS UNCONDITIONAL...", False),
        (54.5, "C", "LOYALTY AND DEDICATION!", True)
    ]),

    # Sentence 6: Life's Greatest Lesson (59.4s - 73.8s)
    (59.4, 73.8, [
        (59.8, "A", "THAT SELFLESS LOYALTY...", False),
        (64.2, "B", "HANUMAN SHOWED...", False),
        (68.0, "C", "IS LIFE'S GREATEST LESSON!", True)
    ])
]

def render_kinetic_subtitles_frame(active_phrases):
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

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

        # Soft dark drop shadow: multi-layer soft blur for high legibility
        for ox, oy, alpha in [(5, 5, 200), (4, 4, 160), (3, 3, 120), (2, 2, 80)]:
            draw.multiline_text((draw_x + ox, draw_y + oy), text, font=f, fill=(0, 0, 0, alpha), align=align)

        # Crisp vibrant electric yellow text (#FFE500 per Reference 3 specification)
        draw.multiline_text((draw_x, draw_y), text, font=f, fill=(255, 229, 0, 255), align=align)

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
subprocess.run(["ffmpeg", "-y", "-ss", "5.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t5.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "11.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t11.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "18.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t18.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "28.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t28.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "42.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t42.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "56.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t56.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "69.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t69.5s.png")], check=True)
print("✅ QA verification frames extracted successfully!")
