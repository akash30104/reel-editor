#!/usr/bin/env python3
"""
render_ref4_perfect.py
Master rendering script for Reel 1 strictly conforming to Reference 4 Master Specification:
- 50/50 vertical split-screen with cinematic MCU framing: Host (Woman) top, Guest (Man) bottom.
- Alternating 16:9 letterboxed thematic B-rolls every 3–6s on pure black canvas.
- Center-seam highlight callout banners with white border lines, dark strip, white supporting text,
  and large golden-yellow Tamil script keywords shaped by HarfBuzz via libass.
- Animated YouTube subscribe card outro in the final 4.5s with speaker avatar and YouTube logo.
- Dialogue normalized to -14.0 LUFS over soft melodic strings/flute BGM (-23 dB). Zero watermarks.
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

pro_dialogue = WORKSPACE / "reel1_pro_mastered_audio.wav"
bgm_music = ASSETS_DIR / "audio" / "ramayan_flute_bgm.mp3"

# 1. Cuts Schedule (Alternating Split-Screen & 16:9 B-Rolls)
# 202.MOV starts at 1988.0s
CUTS_SCHEDULE = [
    # 01. Split-Screen: Host asks opening question (0.0s - 4.5s, dur 4.5s)
    {"type": "split", "st": 0.0, "et": 4.5, "raw_ss": 1988.0},

    # 02. B-Roll 1: Temple / Heritage (4.5s - 8.5s, dur 4.0s)
    {"type": "broll", "st": 4.5, "et": 8.5, "file": BROLLS_DIR / "broll_temple.mp4", "broll_ss": 2.0},

    # 03. Split-Screen: Guest opens Hanuman Hook (8.5s - 13.0s, dur 4.5s)
    {"type": "split", "st": 8.5, "et": 13.0, "raw_ss": 1996.5},

    # 04. B-Roll 2: Hanuman Divine Power (13.0s - 16.5s, dur 3.5s)
    {"type": "broll", "st": 13.0, "et": 16.5, "file": BROLLS_DIR / "broll_hanuman_power.mp4", "broll_ss": 1.0},

    # 05. Split-Screen: Latent Potential & Mentor (16.5s - 21.0s, dur 4.5s)
    {"type": "split", "st": 16.5, "et": 21.0, "raw_ss": 2004.5},

    # 06. B-Roll 3: Golden Sunrise Awakening (21.0s - 24.5s, dur 3.5s)
    {"type": "broll", "st": 21.0, "et": 24.5, "file": BROLLS_DIR / "broll_golden_sunrise.mp4", "broll_ss": 3.0},

    # 07. Split-Screen: Unconditional Loyalty Principle (24.5s - 29.5s, dur 5.0s)
    {"type": "split", "st": 24.5, "et": 29.5, "raw_ss": 2012.5},

    # 08. B-Roll 4: Modern Office / Colleague Walkout (29.5s - 34.0s, dur 4.5s)
    {"type": "broll", "st": 29.5, "et": 34.0, "file": BROLLS_DIR / "broll_business.mp4", "broll_ss": 5.0},

    # 09. Split-Screen: 2 Years Work Left Without Word (34.0s - 39.0s, dur 5.0s)
    {"type": "split", "st": 34.0, "et": 39.0, "raw_ss": 2022.0},

    # 10. B-Roll 5: Walking with Purpose / Direction (39.0s - 43.5s, dur 4.5s)
    {"type": "broll", "st": 39.0, "et": 43.5, "file": BROLLS_DIR / "broll_purpose_direction.mp4", "broll_ss": 2.0},

    # 11. Split-Screen: Loyalty Stands By You (43.5s - 48.5s, dur 5.0s)
    {"type": "split", "st": 43.5, "et": 48.5, "raw_ss": 2031.5},

    # 12. B-Roll 6: Promenade Crowd / Modern Society (48.5s - 53.5s, dur 5.0s)
    {"type": "broll", "st": 48.5, "et": 53.5, "file": BROLLS_DIR / "broll_crowd_promenade.mp4", "broll_ss": 4.0},

    # 13. Split-Screen: Rare Quality / Lack of Loyalty (53.5s - 59.0s, dur 5.5s)
    {"type": "split", "st": 53.5, "et": 59.0, "raw_ss": 2041.5},

    # 14. B-Roll 7: Majestic Mountain Peaks (59.0s - 64.0s, dur 5.0s)
    {"type": "broll", "st": 59.0, "et": 64.0, "file": BROLLS_DIR / "broll_mountains.mp4", "broll_ss": 3.0},

    # 15. Split-Screen Climax: Final Lesson (64.0s - 69.5s, dur 5.5s)
    {"type": "split", "st": 64.0, "et": 69.5, "raw_ss": 2052.0},

    # 16. Outro Card: Centered White Channel Card & Subscribe Animation (69.5s - 74.0s, dur 4.5s)
    {"type": "outro", "st": 69.5, "et": 74.0}
]

# 2. Render Segments
SEGS_DIR = WORKSPACE / "ref4_perfect_segs"
SEGS_DIR.mkdir(parents=True, exist_ok=True)

# Tight cinematic MCU crop for Host (Woman on top) and Guest (Man on bottom)
# In 3840x2160 raw footage:
# Woman (Host): x0=2094, y0=680, w=1012, h=900 -> 1080x960
# Man (Guest): x0=494, y0=830, w=1012, h=900 -> 1080x960
vf_host = (
    "crop=1012:900:2094:680,scale=1080:960:flags=lanczos,"
    "eq=contrast=1.08:saturation=0.92:brightness=-0.01,"
    "colorbalance=rs=0.03:gs=0.01:bs=-0.03,setsar=1,fps=30"
)
vf_guest = (
    "crop=1012:900:494:830,scale=1080:960:flags=lanczos,"
    "eq=contrast=1.08:saturation=0.92:brightness=-0.01,"
    "colorbalance=rs=0.03:gs=0.01:bs=-0.03,setsar=1,fps=30"
)

seg_files = []
print("🎬 Generating Reference 4 perfect visual segments...")

# Pre-extract avatar for outro
avatar_png = WORKSPACE / "ref4_avatar.png"
if not avatar_png.exists():
    import cv2
    cap_av = cv2.VideoCapture(str(RAW_VIDEO))
    cap_av.set(cv2.CAP_PROP_POS_MSEC, 1995 * 1000)
    ret_av, frame_av = cap_av.read()
    if ret_av:
        gx0, gy0, gw, gh = 850, 1000, 320, 320
        face_crop = frame_av[gy0:gy0+gh, gx0:gx0+gw]
        face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
        im_face = Image.fromarray(face_rgb).resize((130, 130), Image.Resampling.LANCZOS)
        mask = Image.new("L", (130, 130), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse([(0, 0), (130, 130)], fill=255)
        im_round = Image.new("RGBA", (130, 130), (0, 0, 0, 0))
        im_round.paste(im_face, (0, 0), mask=mask)
        im_round.save(str(avatar_png))
    cap_av.release()

for idx, item in enumerate(CUTS_SCHEDULE):
    seg_mp4 = SEGS_DIR / f"seg_{idx:02d}.mp4"
    dur = item["et"] - item["st"]

    if item["type"] == "split":
        raw_ss = item["raw_ss"]
        # Stack Woman top and Man bottom, with a clean 2px black seam line at Y=960
        fc = f"[0:v]{vf_host}[top];[0:v]{vf_guest}[bot];[top][bot]vstack=inputs=2,drawbox=x=0:y=959:w=1080:h=2:color=black:t=fill[v]"
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
        total_outro_frames = int(round(dur * 30))
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
        font_btn = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
        font_watch = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
        font_yt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)

        av_img = Image.open(str(avatar_png)).convert("RGBA") if avatar_png.exists() else None

        def make_outro_img(is_clicked):
            im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
            draw = ImageDraw.Draw(im)

            # White Card in Center (Y=620..1060)
            card_w, card_h = 760, 440
            card_x0 = (WIDTH - card_w) // 2 # 160
            card_y0 = 620
            card_x1 = card_x0 + card_w     # 920
            card_y1 = card_y0 + card_h     # 1060

            # Card shadow & background
            draw.rounded_rectangle([(card_x0-6, card_y0-6), (card_x1+6, card_y1+6)], radius=28, fill=(20, 20, 20, 160))
            draw.rounded_rectangle([(card_x0, card_y0), (card_x1, card_y1)], radius=24, fill=(255, 255, 255, 255))

            # Avatar (Circular portrait)
            av_cx, av_cy, av_r = 540, 725, 65
            if av_img:
                im.paste(av_img, (av_cx - 65, av_cy - 65), mask=av_img)
            else:
                draw.ellipse([(av_cx - av_r, av_cy - av_r), (av_cx + av_r, av_cy + av_r)], fill=(235, 130, 7, 255))

            # Channel Name: "VIRAL PODCAST"
            bbox_t = draw.textbbox((0, 0), "VIRAL PODCAST", font=font_title)
            tw = bbox_t[2] - bbox_t[0]
            draw.text((540 - tw // 2, 810), "VIRAL PODCAST", font=font_title, fill=(18, 18, 18, 255))

            # Channel subtext: "@tamilpodcast • 1.2M subscribers"
            bbox_s = draw.textbbox((0, 0), "@tamilpodcast • 1.2M subscribers", font=font_sub)
            sw = bbox_s[2] - bbox_s[0]
            draw.text((540 - sw // 2, 856), "@tamilpodcast • 1.2M subscribers", font=font_sub, fill=(110, 110, 110, 255))

            # Subscribe Button: Red Pill -> Dark Gray Subscribed
            btn_w, btn_h = 280, 68
            btn_x0 = 540 - btn_w // 2
            btn_y0 = 910
            btn_x1 = btn_x0 + btn_w
            btn_y1 = btn_y0 + btn_h

            if not is_clicked:
                draw.rounded_rectangle([(btn_x0, btn_y0), (btn_x1, btn_y1)], radius=34, fill=(230, 33, 23, 255))
                bbox_b = draw.textbbox((0, 0), "SUBSCRIBE", font=font_btn)
                bw = bbox_b[2] - bbox_b[0]
                draw.text((540 - bw // 2, btn_y0 + 19), "SUBSCRIBE", font=font_btn, fill=(255, 255, 255, 255))
            else:
                draw.rounded_rectangle([(btn_x0 - 15, btn_y0), (btn_x1 + 15, btn_y1)], radius=34, fill=(35, 35, 35, 255))
                bbox_b = draw.textbbox((0, 0), "🔔 SUBSCRIBED", font=font_btn)
                bw = bbox_b[2] - bbox_b[0]
                draw.text((540 - bw // 2, btn_y0 + 19), "🔔 SUBSCRIBED", font=font_btn, fill=(255, 255, 255, 255))

            # Below Card: "Watch full video on"
            bbox_w = draw.textbbox((0, 0), "Watch full video on", font=font_watch)
            ww = bbox_w[2] - bbox_w[0]
            draw.text((540 - ww // 2, 1150), "Watch full video on", font=font_watch, fill=(255, 255, 255, 255))

            # YouTube Logo + "YouTube" text
            yt_icon_w, yt_icon_h = 72, 50
            bbox_yt = draw.textbbox((0, 0), "YouTube", font=font_yt)
            yt_text_w = bbox_yt[2] - bbox_yt[0]

            total_yt_w = yt_icon_w + 16 + yt_text_w
            yt_start_x = 540 - total_yt_w // 2
            yt_y = 1215

            draw.rounded_rectangle([(yt_start_x, yt_y), (yt_start_x + yt_icon_w, yt_y + yt_icon_h)], radius=14, fill=(255, 0, 0, 255))
            tri_x0 = yt_start_x + 28
            tri_y0 = yt_y + 14
            tri_pts = [(tri_x0, tri_y0), (tri_x0 + 22, tri_y0 + 11), (tri_x0, tri_y0 + 22)]
            draw.polygon(tri_pts, fill=(255, 255, 255, 255))
            draw.text((yt_start_x + yt_icon_w + 16, yt_y + 1), "YouTube", font=font_yt, fill=(255, 255, 255, 255))

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

# Concat video track
concat_txt = WORKSPACE / "ref4_perfect_concat.txt"
concat_txt.write_text("\n".join([f"file '{p}'" for p in seg_files]) + "\n")
base_visual_mp4 = WORKSPACE / "ref4_perfect_base.mp4"
print("🎬 Concatenating Reference 4 visual track...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c", "copy", str(base_visual_mp4)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 3. Master ASS Subtitle File for Center-Seam Highlight Banners
ass_file = WORKSPACE / "ref4_perfect_banners.ass"
ass_content = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BannerBox,Arial,10,&H200A0A0A,&H00000000,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: BorderLine,Arial,10,&H00FFFFFF,&H00000000,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: SupText,Arial,42,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,1,0,0,100,100,0,0,1,2,2,8,20,20,20,1
Style: MainTamil,Tamil Sangam MN,90,&H0000D7FF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,4,8,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text

; 01. Hook 1: Lesson from Ramayana
Dialogue: 0,0:00:00.80,0:00:04.20,BannerBox,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 260 l 0 260{\\p0}
Dialogue: 1,0:00:00.80,0:00:04.20,BorderLine,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 1,0:00:00.80,0:00:04.20,BorderLine,,0,0,0,,{\\pos(0,1090)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 2,0:00:00.80,0:00:04.20,SupText,,0,0,0,,{\\pos(540,865)}LESSON FROM RAMAYANA
Dialogue: 2,0:00:00.80,0:00:04.20,MainTamil,,0,0,0,,{\\pos(540,945)}என்ன கத்துக்கணும்?

; 02. Hook 2: Everybody is Hanuman
Dialogue: 0,0:00:09.00,0:00:12.80,BannerBox,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 260 l 0 260{\\p0}
Dialogue: 1,0:00:09.00,0:00:12.80,BorderLine,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 1,0:00:09.00,0:00:12.80,BorderLine,,0,0,0,,{\\pos(0,1090)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 2,0:00:09.00,0:00:12.80,SupText,,0,0,0,,{\\pos(540,865)}EVERY HUMAN BEING
Dialogue: 2,0:00:09.00,0:00:12.80,MainTamil,,0,0,0,,{\\pos(540,945)}ஒவ்வொருத்தரும் அனுமன்!

; 03. Takeaway 1: Latent Potential
Dialogue: 0,0:00:17.00,0:00:20.80,BannerBox,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 260 l 0 260{\\p0}
Dialogue: 1,0:00:17.00,0:00:20.80,BorderLine,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 1,0:00:17.00,0:00:20.80,BorderLine,,0,0,0,,{\\pos(0,1090)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 2,0:00:17.00,0:00:20.80,SupText,,0,0,0,,{\\pos(540,865)}HIDDEN POWER
Dialogue: 2,0:00:17.00,0:00:20.80,MainTamil,,0,0,0,,{\\pos(540,945)}LATENT POTENTIAL!

; 04. Principle: Unconditional Loyalty
Dialogue: 0,0:00:25.00,0:00:29.20,BannerBox,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 260 l 0 260{\\p0}
Dialogue: 1,0:00:25.00,0:00:29.20,BorderLine,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 1,0:00:25.00,0:00:29.20,BorderLine,,0,0,0,,{\\pos(0,1090)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 2,0:00:25.00,0:00:29.20,SupText,,0,0,0,,{\\pos(540,865)}THE GREATEST PRINCIPLE
Dialogue: 2,0:00:25.00,0:00:29.20,MainTamil,,0,0,0,,{\\pos(540,945)}UNCONDITIONAL LOYALTY

; 05. Live Example: 2 Years Work
Dialogue: 0,0:00:34.50,0:00:38.80,BannerBox,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 260 l 0 260{\\p0}
Dialogue: 1,0:00:34.50,0:00:38.80,BorderLine,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 1,0:00:34.50,0:00:38.80,BorderLine,,0,0,0,,{\\pos(0,1090)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 2,0:00:34.50,0:00:38.80,SupText,,0,0,0,,{\\pos(540,865)}AFTER 2 YEARS OF WORK
Dialogue: 2,0:00:34.50,0:00:38.80,MainTamil,,0,0,0,,{\\pos(540,945)}சொல்லாம கொள்ளாம போயிட்டாங்க!

; 06. Reality: Loyalty stands by you
Dialogue: 0,0:00:44.00,0:00:48.20,BannerBox,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 260 l 0 260{\\p0}
Dialogue: 1,0:00:44.00,0:00:48.20,BorderLine,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 1,0:00:44.00,0:00:48.20,BorderLine,,0,0,0,,{\\pos(0,1090)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 2,0:00:44.00,0:00:48.20,SupText,,0,0,0,,{\\pos(540,865)}IN TODAY'S WORLD
Dialogue: 2,0:00:44.00,0:00:48.20,MainTamil,,0,0,0,,{\\pos(540,945)}LOYALTY STANDS BY YOU!

; 07. Rare Quality: No Loyalty
Dialogue: 0,0:00:54.00,0:00:58.50,BannerBox,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 260 l 0 260{\\p0}
Dialogue: 1,0:00:54.00,0:00:58.50,BorderLine,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 1,0:00:54.00,0:00:58.50,BorderLine,,0,0,0,,{\\pos(0,1090)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 2,0:00:54.00,0:00:58.50,SupText,,0,0,0,,{\\pos(540,865)}A RARE QUALITY
Dialogue: 2,0:00:54.00,0:00:58.50,MainTamil,,0,0,0,,{\\pos(540,945)}LOYALTY-E இல்ல!

; 08. Climax: Selfless Dedication
Dialogue: 0,0:00:64.80,0:00:69.20,BannerBox,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 260 l 0 260{\\p0}
Dialogue: 1,0:00:64.80,0:00:69.20,BorderLine,,0,0,0,,{\\pos(0,830)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 1,0:00:64.80,0:00:69.20,BorderLine,,0,0,0,,{\\pos(0,1090)\\p1}m 0 0 l 1080 0 l 1080 2 l 0 2{\\p0}
Dialogue: 2,0:00:64.80,0:00:69.20,SupText,,0,0,0,,{\\pos(540,865)}LIFE'S GREATEST TRUTH
Dialogue: 2,0:00:64.80,0:00:69.20,MainTamil,,0,0,0,,{\\pos(540,945)}SELFLESS DEDICATION!
"""
ass_file.write_text(ass_content)
print(f"✅ Master ASS file written: {ass_file}")

# 4. Master Assembly & Audio Mixing
final_out = EXPORT_DIR / "Reel_1_Reference_4_Style.mp4"
print(f"🎬 Assembling Master Reference 4 Reel to: {final_out}")

filter_complex = (
    f"[0:v]ass='{ass_file}'[v];"
    f"[2:a]volume=0.06,afade=t=in:ss=0:d=1.0,afade=t=out:st=71.5:d=2.5[bgm];"
    f"[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[a]"
)

subprocess.run([
    "ffmpeg", "-y",
    "-i", str(base_visual_mp4),
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
subprocess.run(["ffmpeg", "-y", "-ss", "2.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t2.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "6.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t6.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "10.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t10.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "14.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t14.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "18.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t18.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "22.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t22.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "26.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t26.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "36.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t36.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "45.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t45.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "61.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t61.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "66.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t66.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "72.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_outro_t72.0s.png")], check=True)
print("✅ Reference 4 QA verification frames extracted successfully!")
