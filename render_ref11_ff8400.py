#!/usr/bin/env python3
"""
render_ref11_ff8400.py
Renders Reel 1 in Reference 11 Style with EXACT #FF8400 color and 1-by-1 fast-changing karaoke subtitles:

1. Color Code: Exact #FF8400 (RGB: 255, 132, 0)
   - Title Banner Background: #FF8400
   - Subtitle Active Generating Word: #FF8400
2. Subtitles:
   - Font: User's handwriting font MyHandwriting.ttf (NotoSansTamil-Bold fallback for Tamil script)
   - Colors: Pure White (#FFFFFF) inactive words + Signature Orange (#FF8400) active generating word
   - Outline: 6px solid black (#000000) stroke
   - Pacing: 1-by-1 rapid word-by-word highlight changing every 0.3s - 0.7s
3. Layout (Reference 11 Master):
   - Canvas: 1080x1920 @ 30 fps
   - Top black bar: Y=0 to Y=407
   - Persistent Banner: Y=408 to Y=557 (Height 150px, background #FF8400, 2px black borders)
   - Active Video Window: Y=558 to Y=1497 (Height 940px, centered)
   - Hook Transition: First 0.6s B&W snapping into full color
   - Punch-in: 1.15x on climax
   - Hanuman B-Roll: Uncropped face, crown, eyes, and golden aura 100% framed
   - Bottom black bar: Y=1498 to Y=1919
4. Audio:
   - Pro Studio Audio Master (Demucs v4 vocal isolation + surgical EQ + ducked flute BGM -14.0 LUFS)
5. Output:
   - /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_11_Style.mp4
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
VIDEO_H = 940
VIDEO_Y = 558
BANNER_Y = 408
BANNER_H = 150
SUBS_Y = 1330
SUBS_H = 160

# Exact user-demanded color #FF8400
COLOR_FF8400 = (255, 132, 0, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_BLACK = (0, 0, 0, 255)

# Cuts Specification for Reel 1 (Hanuman / Mentorship)
CUTS = [
    {"st": 1988.0, "et": 1996.0, "speaker": "host", "broll": None, "punch": False},
    {"st": 1996.0, "et": 2008.5, "speaker": "guest", "broll": None, "punch": False},
    {"st": 2008.5, "et": 2018.5, "speaker": "broll", "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"), "punch": False},
    {"st": 2018.5, "et": 2035.0, "speaker": "guest", "broll": None, "punch": True},
    {"st": 2035.0, "et": 2048.0, "speaker": "guest", "broll": None, "punch": True},
    {"st": 2048.0, "et": 2062.0, "speaker": "guest", "broll": None, "punch": False}
]

total_dur = sum(c["et"] - c["st"] for c in CUTS)
print(f"Total Reel 1 duration: {total_dur:.2f}s")

# 1. Title Banner in EXACT #FF8400
banner_png = WORKSPACE / "ref11_banner_ff8400.png"
font_ta_banner = ImageFont.truetype(str(ASSETS_DIR / "fonts" / "NotoSansTamil-Bold.ttf"), 44)
font_ta_banner_sub = ImageFont.truetype(str(ASSETS_DIR / "fonts" / "NotoSansTamil-Bold.ttf"), 38)

im_b = Image.new("RGBA", (WIDTH, BANNER_H), (255, 132, 0, 255)) # #FF8400
draw_b = ImageDraw.Draw(im_b)

# 2px black borders top and bottom
draw_b.line([(0, 0), (WIDTH, 0)], fill=(0, 0, 0, 255), width=3)
draw_b.line([(0, BANNER_H - 1), (WIDTH, BANNER_H - 1)], fill=(0, 0, 0, 255), width=3)

t1 = "ராமாயணம் கற்றுத்தரும் பாடம் 🏹"
t2 = "ஹனுமான் தரும் வாழ்க்கை தத்துவம்! 🔥"

w1 = draw_b.textlength(t1, font=font_ta_banner)
w2 = draw_b.textlength(t2, font=font_ta_banner_sub)

draw_b.text(((WIDTH - w1)/2, 20), t1, font=font_ta_banner, fill=(0, 0, 0, 255))
draw_b.text(((WIDTH - w2)/2, 85), t2, font=font_ta_banner_sub, fill=(0, 0, 0, 255))

im_b.save(banner_png)
print(f"✅ Header Banner in #FF8400 saved: {banner_png}")

# 2. Fast 1-by-1 Word Karaoke Subtitle Events
# Format: (st, et, [words_in_chunk], active_word_index)
WORD_EVENTS = [
    # Cut 0 (0.0s to 8.0s)
    (0.4, 1.4, ["ராமாயணத்துல", "இருந்து..."], 0),
    (1.4, 2.3, ["ராமாயணத்துல", "இருந்து..."], 1),
    (2.5, 3.2, ["நாம்", "என்ன"], 0),
    (3.2, 3.9, ["நாம்", "என்ன"], 1),
    (3.9, 4.8, ["வாழ்க்கை", "பாடம்"], 0),
    (4.8, 5.8, ["வாழ்க்கை", "பாடம்"], 1),
    (5.8, 6.6, ["எடுத்துக்கணும்?"], 0),
    (6.6, 7.2, ["LIFE", "LESSON? 🏹"], 0),
    (7.2, 7.9, ["LIFE", "LESSON? 🏹"], 1),

    # Cut 1 (8.0s to 20.5s)
    (8.3, 9.0, ["நான்", "வந்து"], 0),
    (9.0, 9.7, ["நான்", "வந்து"], 1),
    (9.7, 10.5, ["ஹனுமான", "பத்தி"], 0),
    (10.5, 11.3, ["ஹனுமான", "பத்தி"], 1),
    (11.3, 12.2, ["மட்டும்", "பேச"], 0),
    (12.2, 13.0, ["மட்டும்", "பேச"], 1),
    (13.0, 14.1, ["நினைக்கிறேன்!"], 0),
    (14.1, 14.8, ["EVERYBODY", "IN"], 0),
    (14.8, 15.4, ["EVERYBODY", "IN"], 1),
    (15.4, 16.0, ["THIS", "WORLD"], 0),
    (16.0, 16.8, ["THIS", "WORLD"], 1),
    (16.8, 17.5, ["IS", "LIKE"], 0),
    (17.5, 18.2, ["IS", "LIKE"], 1),
    (18.2, 20.4, ["HANUMAN! 🏹"], 0),

    # Cut 2 (20.5s to 30.5s)
    (20.8, 21.6, ["நமக்குள்ள", "ஒரு"], 0),
    (21.6, 22.3, ["நமக்குள்ள", "ஒரு"], 1),
    (22.3, 23.4, ["LATENT", "POTENTIAL"], 0),
    (23.4, 24.6, ["LATENT", "POTENTIAL"], 1),
    (24.6, 25.7, ["ஒளிஞ்சிருக்கு..."], 0),
    (25.7, 26.5, ["Someone", "has", "to"], 0),
    (26.5, 27.1, ["Someone", "has", "to"], 1),
    (27.1, 27.7, ["Someone", "has", "to"], 2),
    (27.7, 28.5, ["show", "that..."], 0),
    (28.5, 29.2, ["show", "that..."], 1),
    (29.2, 29.7, ["THAT'S", "THE", "MENTOR!"], 0),
    (29.7, 30.1, ["THAT'S", "THE", "MENTOR!"], 1),
    (30.1, 30.5, ["THAT'S", "THE", "MENTOR!"], 2),

    # Cut 3 (30.5s to 47.0s)
    (30.8, 31.8, ["ஜாம்பவான்", "வந்து"], 0),
    (31.8, 32.6, ["ஜாம்பவான்", "வந்து"], 1),
    (32.6, 33.5, ["ஹனுமான்", "கிட்ட"], 0),
    (33.5, 34.3, ["ஹனுமான்", "கிட்ட"], 1),
    (34.3, 35.3, ["சொல்லும்போது..."], 0),
    (35.3, 36.2, ["YOU", "ARE"], 0),
    (36.2, 37.0, ["YOU", "ARE"], 1),
    (37.0, 38.6, ["POWERFUL! 🔥"], 0),
    (38.8, 39.6, ["உன்", "சக்தி"], 0),
    (39.6, 40.5, ["உன்", "சக்தி"], 1),
    (40.5, 41.5, ["உனக்கு", "தெரியல..."], 0),
    (41.5, 42.8, ["உனக்கு", "தெரியல..."], 1),
    (42.8, 44.0, ["அப்படின்னு", "அவர்"], 0),
    (44.0, 45.2, ["அப்படின்னு", "அவர்"], 1),
    (45.2, 46.8, ["சொன்னதுனால", "தான்!"], 0),
    (46.0, 46.8, ["சொன்னதுனால", "தான்!"], 1),

    # Cut 4 (47.0s to 60.0s)
    (47.3, 48.2, ["அவர்", "கடலை"], 0),
    (48.2, 49.2, ["அவர்", "கடலை"], 1),
    (49.2, 50.2, ["தாண்டி", "சீதையை"], 0),
    (50.2, 51.5, ["தாண்டி", "சீதையை"], 1),
    (51.5, 53.0, ["கண்டுபிடிச்சார்!"], 0),
    (53.2, 54.3, ["சொல்லவே", "இல்லன்னா..."], 0),
    (54.3, 55.4, ["சொல்லவே", "இல்லன்னா..."], 1),
    (55.4, 56.2, ["HE", "WOULD", "HAVE"], 0),
    (56.2, 57.0, ["HE", "WOULD", "HAVE"], 1),
    (57.0, 57.8, ["HE", "WOULD", "HAVE"], 2),
    (57.8, 58.9, ["NEVER"], 0),
    (58.9, 60.0, ["KNOWN!"], 0),

    # Cut 5 (60.0s to 74.0s)
    (60.5, 61.4, ["அதை", "விட"], 0),
    (61.4, 62.2, ["அதை", "விட"], 1),
    (62.2, 63.1, ["பெரிய", "பாடம்"], 0),
    (63.1, 64.1, ["பெரிய", "பாடம்"], 1),
    (64.1, 65.3, ["வாழ்க்கையில"], 0),
    (65.3, 66.2, ["எதுவுமே", "இல்ல!"], 0),
    (66.2, 67.0, ["எதுவுமே", "இல்ல!"], 1),
    (67.0, 68.2, ["GREATEST"], 0),
    (68.2, 69.4, ["LESSON"], 0),
    (69.4, 70.2, ["OF", "LIFE! 🏹"], 0),
    (70.2, 71.2, ["OF", "LIFE! 🏹"], 1),
    (71.2, 72.0, ["Follow", "for", "more 🏹"], 0),
    (72.0, 72.8, ["Follow", "for", "more 🏹"], 1),
    (72.8, 73.9, ["Follow", "for", "more 🏹"], 2)
]

# Fonts
font_hw_p = "/Users/pgi/Library/Fonts/MyHandwriting.ttf"
font_ta_p = ASSETS_DIR / "fonts" / "NotoSansTamil-Bold.ttf"

font_hw = ImageFont.truetype(font_hw_p, 70)
font_ta = ImageFont.truetype(str(font_ta_p), 52)

def has_tamil(text):
    return any(0x0B80 <= ord(c) <= 0x0BFF for c in text)

def render_karaoke_frame(words, active_idx):
    im = Image.new("RGBA", (WIDTH, SUBS_H), (0, 0, 0, 0))
    if not words:
        return im.tobytes()
        
    draw = ImageDraw.Draw(im)
    word_info = []
    total_w = 0.0
    
    for i, w in enumerate(words):
        f = font_ta if has_tamil(w) else font_hw
        w_len = draw.textlength(w, font=f)
        word_info.append((w, f, w_len, i == active_idx))
        total_w += w_len
        
    space_w = draw.textlength(" ", font=font_hw)
    total_w += space_w * (len(words) - 1)
    
    cur_x = (WIDTH - total_w) / 2
    y = 40
    
    for w, f, w_len, is_active in word_info:
        # Active word in #FF8400, other words in full crisp white #FFFFFF
        fill_col = COLOR_FF8400 if is_active else COLOR_WHITE
        # 6px solid black outline
        draw.text((cur_x, y), w, font=f, fill=fill_col,
                  stroke_width=6, stroke_fill=COLOR_BLACK)
        cur_x += w_len + space_w
        
    return im.tobytes()

# Render animated subtitles MOV with alpha
subs_mov = WORKSPACE / "ref11_fast_subs_ff8400.mov"
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{SUBS_H}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_f = int(round(total_dur * 30))
blank_bytes = render_karaoke_frame([], -1)

for f_idx in range(total_f):
    t_sec = f_idx / 30.0
    active_ev = None
    for st, et, words, idx in WORD_EVENTS:
        if st <= t_sec < et:
            active_ev = (words, idx)
            break
    raw_b = render_karaoke_frame(active_ev[0], active_ev[1]) if active_ev else blank_bytes
    proc.stdin.write(raw_b)

proc.stdin.close()
proc.wait()
print(f"✅ Fast 1-by-1 karaoke subtitles animated video: {subs_mov}")

# 3. Base Video (Re-use existing ref11_base.mp4)
base_vid = WORKSPACE / "ref11_base.mp4"

# 4. Pro Audio Master
pro_audio = WORKSPACE / "reel1_pro_mastered_audio.wav"

# 5. Composite Final Reel
final_out = EXPORT_DIR / "Reel_1_Reference_11_Style.mp4"

subprocess.run([
    "ffmpeg", "-y",
    "-i", str(base_vid),
    "-loop", "1", "-i", str(banner_png),
    "-i", str(subs_mov),
    "-i", str(pro_audio),
    "-filter_complex",
    f"[0:v][1:v]overlay=0:{BANNER_Y}[v_banner];"
    f"[v_banner][2:v]overlay=0:{SUBS_Y}[v]",
    "-map", "[v]", "-map", "3:a",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
    "-shortest",
    str(final_out)
], check=True)

print(f"🎉 FINAL REEL 1 IN REFERENCE 11 STYLE EXPORTED: {final_out}")

# Extract verification frames
subprocess.run(["ffmpeg", "-y", "-ss", "2.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_t2s_ff8400.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_t10s_ff8400.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "18.5", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_t18s_ff8400.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "23.5", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_t23s_ff8400.jpg")], check=True)
print("✅ QA frames extracted successfully!")
