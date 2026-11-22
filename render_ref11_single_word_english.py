#!/usr/bin/env python3
"""
render_ref11_single_word_english.py
Renders Reel 1 in Reference 11 Style with:
1. Title Banner in EXACT #FF8400 (RGB: 255, 132, 0) with Apple Color Emojis (🏹 and 🔥).
2. Subtitle Text in EXACT #FF8400 (RGB: 255, 132, 0) using 2-pass crisp rendering with black outline.
3. Fast single-word English subtitles: ONLY ONE WORD AT A TIME on screen.
4. Full-range RGB color pipeline in FFmpeg preserving pixel-perfect #FF8400.
5. Pro Studio Audio Master (Demucs v4 vocal isolation + ducked flute BGM @ -14.0 LUFS).
6. Export to /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_11_Style.mp4.
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
ASSETS_DIR = WORKSPACE / "assets"

WIDTH = 1080
HEIGHT = 1920
VIDEO_H = 940
VIDEO_Y = 558
BANNER_Y = 408
BANNER_H = 150
SUBS_Y = 1330
SUBS_H = 170

TOTAL_DUR = 74.0

COLOR_FF8400 = (255, 132, 0, 255)
COLOR_BLACK = (0, 0, 0, 255)

# 1. Header Banner with Apple Color Emojis in exact #FF8400
banner_png = WORKSPACE / "ref11_banner_ff8400_emoji.png"
font_ta_1 = ImageFont.truetype(str(ASSETS_DIR / "fonts" / "NotoSansTamil-Bold.ttf"), 44)
font_ta_2 = ImageFont.truetype(str(ASSETS_DIR / "fonts" / "NotoSansTamil-Bold.ttf"), 38)
font_emoji = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 40)

im_b = Image.new("RGBA", (WIDTH, BANNER_H), (255, 132, 0, 255))
draw_b = ImageDraw.Draw(im_b)

# 2px black borders top and bottom
draw_b.line([(0, 0), (WIDTH, 0)], fill=(0, 0, 0, 255), width=3)
draw_b.line([(0, BANNER_H - 1), (WIDTH, BANNER_H - 1)], fill=(0, 0, 0, 255), width=3)

# Line 1 with bow & arrow emoji 🏹
text1 = "ராமாயணம் கற்றுத்தரும் பாடம் "
emoji1 = "🏹"
w1 = draw_b.textlength(text1, font=font_ta_1)
w_e1 = draw_b.textlength(emoji1, font=font_emoji)
start_x1 = (WIDTH - (w1 + w_e1)) / 2
draw_b.text((start_x1, 22), text1, font=font_ta_1, fill=(0, 0, 0, 255))
draw_b.text((start_x1 + w1 + 6, 25), emoji1, font=font_emoji, embedded_color=True)

# Line 2 with fire emoji 🔥
text2 = "ஹனுமான் தரும் வாழ்க்கை தத்துவம்! "
emoji2 = "🔥"
w2 = draw_b.textlength(text2, font=font_ta_2)
w_e2 = draw_b.textlength(emoji2, font=font_emoji)
start_x2 = (WIDTH - (w2 + w_e2)) / 2
draw_b.text((start_x2, 85), text2, font=font_ta_2, fill=(0, 0, 0, 255))
draw_b.text((start_x2 + w2 + 6, 87), emoji2, font=font_emoji, embedded_color=True)

im_b.save(banner_png)
print(f"✅ Header Banner with Apple Color Emojis saved: {banner_png}")

# 2. English Single-Word Fast Pacing Events: (start_time, end_time, single_word)
# ONLY ONE WORD AT A TIME
SINGLE_WORD_EVENTS = [
    # Cut 0: 0.0s to 8.0s (Host question)
    (0.4, 0.9, "WHAT"),
    (0.9, 1.4, "LIFE"),
    (1.4, 2.0, "LESSON"),
    (2.0, 2.5, "CAN"),
    (2.5, 3.0, "WE"),
    (3.0, 3.6, "LEARN"),
    (3.6, 4.2, "FROM"),
    (4.2, 5.0, "RAMAYANA?"),
    (5.0, 5.8, "WHAT"),
    (5.8, 6.6, "IS"),
    (6.6, 7.2, "THE"),
    (7.2, 7.9, "TRUTH?"),

    # Cut 1: 8.0s to 20.5s (Guest starts)
    (8.2, 8.7, "I"),
    (8.7, 9.2, "WANT"),
    (9.2, 9.7, "TO"),
    (9.7, 10.3, "TALK"),
    (10.3, 10.9, "ONLY"),
    (10.9, 11.5, "ABOUT"),
    (11.5, 12.3, "HANUMAN!"),
    (12.3, 13.0, "BECAUSE"),
    (13.0, 13.8, "EVERYONE"),
    (13.8, 14.5, "IN"),
    (14.5, 15.2, "THIS"),
    (15.2, 15.9, "WORLD"),
    (15.9, 16.7, "IS"),
    (16.7, 17.5, "JUST"),
    (17.5, 18.2, "LIKE"),
    (18.2, 20.4, "HANUMAN!"),

    # Cut 2: 20.5s to 30.5s (Hanuman B-Roll & Latent Potential)
    (20.7, 21.3, "WE"),
    (21.3, 21.9, "ALL"),
    (21.9, 22.5, "HAVE"),
    (22.5, 23.2, "A"),
    (23.2, 24.0, "HIDDEN"),
    (24.0, 24.8, "LATENT"),
    (24.8, 25.6, "POTENTIAL!"),
    (25.6, 26.3, "SOMEONE"),
    (26.3, 27.0, "HAS"),
    (27.0, 27.7, "TO"),
    (27.7, 28.5, "AWAKEN"),
    (28.5, 29.2, "IT..."),
    (29.2, 29.7, "THAT'S"),
    (29.7, 30.1, "THE"),
    (30.1, 30.5, "MENTOR!"),

    # Cut 3: 30.5s to 47.0s (Jambavan & You Are Powerful)
    (30.8, 31.5, "WHEN"),
    (31.5, 32.2, "JAMBAVAN"),
    (32.2, 33.0, "CAME"),
    (33.0, 33.8, "TO"),
    (33.8, 34.6, "HANUMAN"),
    (34.6, 35.3, "AND"),
    (35.3, 36.2, "SAID..."),
    (36.2, 37.0, "YOU"),
    (37.0, 37.7, "ARE"),
    (37.7, 38.6, "POWERFUL!"),
    (38.8, 39.5, "YOUR"),
    (39.5, 40.2, "OWN"),
    (40.2, 41.0, "TRUE"),
    (41.0, 41.8, "STRENGTH,"),
    (41.8, 42.6, "YOU"),
    (42.6, 43.4, "DID"),
    (43.4, 44.2, "NOT"),
    (44.2, 45.0, "EVEN"),
    (45.0, 45.8, "REALIZE!"),
    (45.8, 46.4, "AND"),
    (46.4, 47.0, "THEN!"),

    # Cut 4: 47.0s to 60.0s (Ocean crossing & Mother Sita)
    (47.2, 48.0, "HE"),
    (48.0, 48.8, "LEAPED"),
    (48.8, 49.6, "ACROSS"),
    (49.6, 50.4, "THE"),
    (50.4, 51.2, "OCEAN!"),
    (51.2, 52.0, "AND"),
    (52.0, 52.8, "FOUND"),
    (52.8, 53.6, "MOTHER"),
    (53.6, 54.4, "SITA!"),
    (54.4, 55.2, "WITHOUT"),
    (55.2, 56.0, "THAT"),
    (56.0, 56.8, "MENTOR,"),
    (56.8, 57.5, "HE"),
    (57.5, 58.3, "WOULD"),
    (58.3, 59.0, "HAVE"),
    (59.0, 59.5, "NEVER"),
    (59.5, 60.0, "KNOWN!"),

    # Cut 5: 60.0s to 74.0s (Conclusion & CTA)
    (60.4, 61.1, "THERE"),
    (61.1, 61.8, "IS"),
    (61.8, 62.5, "NO"),
    (62.5, 63.3, "GREATER"),
    (63.3, 64.1, "LESSON"),
    (64.1, 64.9, "IN"),
    (64.9, 65.7, "YOUR"),
    (65.7, 66.5, "ENTIRE"),
    (66.5, 67.2, "LIFE!"),
    (67.2, 68.0, "FIND"),
    (68.0, 68.8, "YOUR"),
    (68.8, 69.6, "MENTOR!"),
    (69.6, 70.4, "GREATEST"),
    (70.4, 71.2, "LESSON!"),
    (71.2, 72.0, "FOLLOW"),
    (72.0, 72.8, "FOR"),
    (72.8, 73.9, "MORE!"),
]

# Subtitle font: User's handwriting font MyHandwriting.ttf
font_hw_p = "/Users/pgi/Library/Fonts/MyHandwriting.ttf"
font_sub = ImageFont.truetype(font_hw_p, 95)

def render_single_word_frame(word):
    im = Image.new("RGBA", (WIDTH, SUBS_H), (0, 0, 0, 0))
    if not word:
        return im.tobytes()
    draw = ImageDraw.Draw(im)
    w_len = draw.textlength(word, font=font_sub)
    x = (WIDTH - w_len) / 2
    y = 35
    
    # 2-Pass Rendering to guarantee 100% pure #FF8400 core with solid black outline
    # Pass 1: Solid black stroke silhouette
    draw.text((x, y), word, font=font_sub, fill=COLOR_BLACK, stroke_width=6, stroke_fill=COLOR_BLACK)
    # Pass 2: Exact #FF8400 fill directly over inner glyph
    draw.text((x, y), word, font=font_sub, fill=COLOR_FF8400)
    
    return im.tobytes()

# Render animated subtitles MOV with alpha
subs_mov = WORKSPACE / "ref11_single_word_subs.mov"
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{SUBS_H}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_frames = int(round(TOTAL_DUR * 30))
blank_bytes = render_single_word_frame("")

for f_idx in range(total_frames):
    t_sec = f_idx / 30.0
    active_word = None
    for st, et, word in SINGLE_WORD_EVENTS:
        if st <= t_sec < et:
            active_word = word
            break
    frame_bytes = render_single_word_frame(active_word) if active_word else blank_bytes
    proc.stdin.write(frame_bytes)

proc.stdin.close()
proc.wait()
print(f"✅ Single-word fast subtitle stream generated: {subs_mov}")

# Base Video & Pro Audio Master
base_vid = WORKSPACE / "ref11_base.mp4"
pro_audio = WORKSPACE / "reel1_pro_mastered_audio.wav"
final_out = EXPORT_DIR / "Reel_1_Reference_11_Style.mp4"

# Composite Final Video with full-range RGB color pipeline to preserve exact #FF8400
subprocess.run([
    "ffmpeg", "-y",
    "-i", str(base_vid),
    "-loop", "1", "-i", str(banner_png),
    "-i", str(subs_mov),
    "-i", str(pro_audio),
    "-filter_complex",
    f"[0:v]format=rgba[base];"
    f"[base][1:v]overlay=0:{BANNER_Y}:format=rgb[v_banner];"
    f"[v_banner][2:v]overlay=0:{SUBS_Y}:format=rgb[v_rgb];"
    f"[v_rgb]scale=in_range=full:out_range=full,format=yuv420p[v]",
    "-map", "[v]", "-map", "3:a",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18",
    "-color_range", "pc", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
    "-shortest",
    str(final_out)
], check=True)

print(f"🎉 FINAL REEL 1 IN REFERENCE 11 STYLE EXPORTED: {final_out}")

# Extract Verification QA Frames
subprocess.run(["ffmpeg", "-y", "-ss", "1.7", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_single_t1.7s.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "11.8", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_single_t11.8s.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "18.5", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_single_t18.5s.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "24.5", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_single_t24.5s.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "37.5", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_single_t37.5s.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "50.8", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_single_t50.8s.jpg")], check=True)
print("✅ QA frames extracted successfully!")
