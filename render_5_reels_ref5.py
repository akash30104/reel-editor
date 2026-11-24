#!/usr/bin/env python3
"""
Multi-Reel Batch Render Engine for Reference 5 (Ref5) Style.
Renders 5 Extra Reels from IMG_4246.MOV:
  - Reel_IMG_4246_Ref5_Part2.mp4 (Modern Dating Trap / Compatibility)
  - Reel_IMG_4246_Ref5_Part3.mp4 (Physical vs Mental Attraction / True Chemistry)
  - Reel_IMG_4246_Ref5_Part4.mp4 (Influencer vs Influential / Doors Open)
  - Reel_IMG_4246_Ref5_Part5.mp4 (Social Media Commodity / Actors)
  - Reel_IMG_4246_Ref5_Part6.mp4 (Losing Independence & Integrity)

Strict Ref5 Rules:
1. Aspect Ratio: 9:16 Vertical (1080x1920 @ 30fps).
2. Strict 3-Color Palette: #FFF200 (Bright Yellow), #FFFFFF (Pure White), #0A0A0A (Jet Black). No other accent colors!
3. Two-Tier Typography System:
   - Tier A: Stylized Kinetic Titles (Setup spaced Sans, Hero 175px Serif Italic in Yellow with drop shadow + Apple Color Emoji).
   - Tier B: Ultra-Visible Big & Bold Conversational Subtitles (80-88px Arial Bold with stroke_width=2 inside solid Jet Black box + Apple Color Emoji).
4. Single-Caption Rule: Exactly ONE single caption stream on screen at any moment (Zero duplicate cards / subtitles).
5. Visual Pattern Interrupts:
   - 1.0s Solid Jet Black Pause (#0A0A0A) before punchlines.
   - Selective Color / B&W Beat with vintage grain during intense questions.
   - 70%+ Contextual Real-Life B-Rolls (100% Non-AI, 100% Unique across all reels).
6. Camera Framing: 100% locked & centered on Person 1 (Guest, X=2890). Never show host or wide 2-shot!
7. Audio: Broadcast-grade pro audio (-14 LUFS, ducked mild ambient BGM, SFX hits/whooshes/pops/risers).
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Workspace Paths
WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Desktop/reels editor/raw videos/IMG_4246.MOV")
EXPORT_DIR = Path("/Users/pgi/Desktop/reels editor/export ")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

FONTS_DIR = WORKSPACE / "assets" / "fonts"
AUDIO_DIR = WORKSPACE / "assets" / "audio"
BROLLS_DIR = WORKSPACE / "assets" / "brolls"

# Audio Assets
SFX_HIT = AUDIO_DIR / "hit.wav"
SFX_WHOOSH = AUDIO_DIR / "whoosh.mp3"
SFX_POP = AUDIO_DIR / "pop.wav"
SFX_RISER = AUDIO_DIR / "riser.wav"
BGM_TRACK = AUDIO_DIR / "ref5_bgm.mp3"

# Fonts
FONT_SERIF_ITALIC = str(FONTS_DIR / "PlayfairDisplay-Italic.ttf")
FONT_SERIF_REG = str(FONTS_DIR / "PlayfairDisplay-Regular.ttf")
FONT_SANS_REG = str(FONTS_DIR / "Montserrat-Regular.ttf")
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"
font_emoji = ImageFont.truetype(EMOJI_FONT, 160)

WIDTH = 1080
HEIGHT = 1920
FPS = 30

COLOR_YELLOW = (255, 242, 0, 255)  # #FFF200 Bright Yellow
COLOR_WHITE = (255, 255, 255, 255) # #FFFFFF Pure White
COLOR_BLACK = (10, 10, 10, 255)     # #0A0A0A Jet Black
COLOR_SHADOW = (10, 10, 10, 200)

COLOR_GRADE = (
    "curves=master='0/0.02 0.5/0.52 1/0.98',"
    "eq=contrast=1.15:saturation=1.25:brightness=0.015,"
    "colorbalance=rs=0.04:gs=0.02:bs=-0.04"
)
SDR_FILTER = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,format=yuv420p"

# Person 1 (Guest, X=2890) Crops
CROP_GUEST = "crop=1215:2160:2282:0,scale=1080:1920:flags=lanczos"
CROP_GUEST_PUNCH = "crop=1050:1866:2365:100,scale=1080:1920:flags=lanczos"

def render_emoji(char, target_size=88):
    im = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.text((10, 10), char, font=font_emoji, embedded_color=True)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
        aspect = im.width / im.height
        new_w = max(1, int(target_size * aspect))
        im = im.resize((new_w, target_size), Image.Resampling.LANCZOS)
    return im

def draw_spaced_sans(draw, text, y, font, fill_color, letter_spacing=22):
    full_str = text.strip()
    char_widths = [font.getbbox(c)[2] - font.getbbox(c)[0] for c in full_str]
    total_w = sum(char_widths) + (len(full_str) - 1) * letter_spacing
    cur_x = (WIDTH - total_w) // 2
    for c, w in zip(full_str, char_widths):
        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 4)]:
            draw.text((cur_x + dx, y + dy), c, font=font, fill=COLOR_SHADOW)
        draw.text((cur_x, y), c, font=font, fill=fill_color)
        cur_x += w + letter_spacing

def draw_serif_hero(draw, im, text, emoji_char, y, font, fill_color):
    bbox = font.getbbox(text)
    txt_w = bbox[2] - bbox[0]
    txt_h = bbox[3] - bbox[1]
    emoji_w = 0
    emoji_im = None
    if emoji_char:
        emoji_im = render_emoji(emoji_char, target_size=115)
        emoji_w = emoji_im.width + 25
    total_w = txt_w + emoji_w
    cur_x = (WIDTH - total_w) // 2
    for dx, dy in [(-4, -4), (4, -4), (-4, 4), (4, 4), (0, 7), (0, 10)]:
        draw.text((cur_x + dx, y + dy), text, font=font, fill=COLOR_SHADOW)
    draw.text((cur_x, y), text, font=font, fill=fill_color)
    if emoji_im:
        im.paste(emoji_im, (cur_x + txt_w + 25, y + (txt_h - emoji_im.height)//2), emoji_im)

def draw_yellow_card(draw, im, text, emoji_char, sy, font_size=68):
    font_bold = ImageFont.truetype(FONT_BOLD, font_size)
    bbox = font_bold.getbbox(text)
    txt_w = bbox[2] - bbox[0]
    txt_h = bbox[3] - bbox[1]
    emoji_im = None
    emoji_w = 0
    if emoji_char:
        emoji_im = render_emoji(emoji_char, target_size=int(font_size * 1.05))
        emoji_w = emoji_im.width + 20
    box_w = min(1000, txt_w + emoji_w + 100)
    box_h = txt_h + 60
    box_x = (WIDTH - box_w) // 2
    box_y = sy
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=24, fill=COLOR_YELLOW)
    txt_x = box_x + (box_w - (txt_w + emoji_w)) // 2
    txt_y = box_y + (box_h - txt_h) // 2 - 4
    draw.text((txt_x, txt_y), text, font=font_bold, fill=COLOR_BLACK)
    if emoji_im:
        im.paste(emoji_im, (txt_x + txt_w + 20, box_y + (box_h - emoji_im.height) // 2), emoji_im)

def draw_boxed_sub(draw, im, text, emoji_char, font_size=84, y_pos=1440):
    font_sub = ImageFont.truetype(FONT_BOLD, font_size)
    bbox = font_sub.getbbox(text)
    txt_w = bbox[2] - bbox[0]
    txt_h = bbox[3] - bbox[1]
    emoji_im = None
    emoji_w = 0
    if emoji_char:
        emoji_im = render_emoji(emoji_char, target_size=int(font_size * 0.95))
        emoji_w = emoji_im.width + 20
    pad_x = 42
    pad_y = 24
    box_w = min(1000, txt_w + emoji_w + (pad_x * 2))
    box_h = txt_h + (pad_y * 2)
    box_x = (WIDTH - box_w) // 2
    box_y = y_pos
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=20, fill=COLOR_BLACK)
    txt_x = box_x + (box_w - (txt_w + emoji_w)) // 2
    txt_y = box_y + pad_y - 4
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        draw.text((txt_x + dx, txt_y + dy), text, font=font_sub, fill=COLOR_WHITE)
    draw.text((txt_x, txt_y), text, font=font_sub, fill=COLOR_WHITE)
    if emoji_im:
        im.paste(emoji_im, (txt_x + txt_w + 20, box_y + (box_h - emoji_im.height) // 2), emoji_im)

# ==============================================================================
# 5 REELS CONFIGURATION FOR REF5 STYLE
# ==============================================================================
REELS_REF5 = [
    {
        "part": 2,
        "name": "Modern Dating Trap",
        "export_name": "Reel_IMG_4246_Ref5_Part2.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 558.0, "dur": 3.0, "crop": CROP_GUEST_PUNCH, "desc": "We are building a dating app..."},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "mixkit_smartphone_1.mp4", "broll_ss": 2.0, "raw_audio_ss": 561.0, "dur": 3.5, "desc": "Phone app matching"},
            {"id": "c3", "type": "speaker_bw", "raw_ss": 564.5, "dur": 3.2, "crop": CROP_GUEST, "desc": "What I strongly felt now..."},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "broll_river_boat.mp4", "broll_ss": 1.0, "raw_audio_ss": 567.7, "dur": 3.5, "desc": "Whether they are on the same boat"},
            {"id": "c5", "type": "speaker", "raw_ss": 571.2, "dur": 3.0, "crop": CROP_GUEST_PUNCH, "desc": "Commitment is there... Destination"},
            {"id": "c6", "type": "black", "dur": 1.0, "desc": "1.0s Solid Black Pause"},
            {"id": "c7", "type": "broll", "broll": BROLLS_DIR / "mixkit_coffee_1.mp4", "broll_ss": 3.0, "raw_audio_ss": 575.2, "dur": 4.5, "desc": "Compatibility discussions"},
            {"id": "c8", "type": "broll", "broll": BROLLS_DIR / "mixkit_sunset_1.mp4", "broll_ss": 5.0, "dur": 2.5, "desc": "Clean Loop Ending"}
        ],
        "schedule": [
            (0.0, 3.0, ("MODERN DATING APP", "Trap?", "📱"), "kinetic_hook"),
            (3.0, 6.5, ("SWIPING FOR LOVE", "💔"), "yellow_card_top"),
            (6.5, 9.7, ("BEFORE ANY COMMITMENT", "💭"), "tier_b"),
            (9.7, 13.2, ("ARE YOU ON THE SAME BOAT?", "⛵"), "tier_b"),
            (13.2, 16.2, ("GOING TO A DESTINATION", "🧭"), "tier_b"),
            (16.2, 17.2, ("", None), "none"),
            (17.2, 21.7, ("REAL COMPATIBILITY", "☕"), "punch_yellow"),
            (21.7, 24.2, ("TRUE ALIGNMENT", "Same Vision", "ZERO REGRETS", "✨"), "loop_ending")
        ]
    },
    {
        "part": 3,
        "name": "Physical vs Mental Attraction",
        "export_name": "Reel_IMG_4246_Ref5_Part3.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 765.0, "dur": 2.8, "crop": CROP_GUEST_PUNCH, "desc": "Advanced chemistry... True chemistry"},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "mixkit_gym_1.mp4", "broll_ss": 1.0, "raw_audio_ss": 767.8, "dur": 3.5, "desc": "Remove all the physical features"},
            {"id": "c3", "type": "speaker_bw", "raw_ss": 771.3, "dur": 3.5, "crop": CROP_GUEST, "desc": "Just the muscles and no skin..."},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "mixkit_fitness_1.mp4", "broll_ss": 2.0, "raw_audio_ss": 774.8, "dur": 3.2, "desc": "What attraction are you going to feel?"},
            {"id": "c5", "type": "black", "dur": 1.0, "desc": "1.0s Solid Black Pause"},
            {"id": "c6", "type": "speaker", "raw_ss": 779.0, "dur": 3.2, "crop": CROP_GUEST_PUNCH, "desc": "First when you meet a person..."},
            {"id": "c7", "type": "broll", "broll": BROLLS_DIR / "broll_students.mp4", "broll_ss": 2.0, "raw_audio_ss": 782.2, "dur": 4.0, "desc": "Sit and talk to each other"},
            {"id": "c8", "type": "broll", "broll": BROLLS_DIR / "mixkit_nature_1.mp4", "broll_ss": 4.0, "dur": 2.5, "desc": "Clean Loop Ending"}
        ],
        "schedule": [
            (0.0, 2.8, ("TRUE CHEMISTRY OR", "Muscles?", "🧠"), "kinetic_hook"),
            (2.8, 6.3, ("REMOVE PHYSICAL FEATURES", "⚠️"), "yellow_card_top"),
            (6.3, 9.8, ("JUST THE MUSCLES & NO SKIN", "⚡"), "tier_b"),
            (9.8, 13.0, ("WHAT ATTRACTION IS LEFT?", "❓"), "tier_b"),
            (13.0, 14.0, ("", None), "none"),
            (14.0, 17.2, ("WHEN YOU MEET SOMEONE", "👀"), "tier_b"),
            (17.2, 21.2, ("TALK TO THEIR SOUL", "🗣️"), "punch_yellow"),
            (21.2, 23.7, ("INNER CHEMISTRY", "Soul First", "TRUE CONNECTION", "🤍"), "loop_ending")
        ]
    },
    {
        "part": 4,
        "name": "Influencer vs Influential",
        "export_name": "Reel_IMG_4246_Ref5_Part4.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 901.0, "dur": 2.8, "crop": CROP_GUEST_PUNCH, "desc": "What do you think about influencer culture?"},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "broll_business.mp4", "broll_ss": 2.0, "raw_audio_ss": 903.8, "dur": 3.5, "desc": "Two types of people: Influential person"},
            {"id": "c3", "type": "speaker_bw", "raw_ss": 907.3, "dur": 3.2, "crop": CROP_GUEST, "desc": "Every door opens... He is influential"},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "broll_investor_handshake.mp4", "broll_ss": 1.0, "raw_audio_ss": 910.5, "dur": 3.5, "desc": "Everyone will do any favor"},
            {"id": "c5", "type": "black", "dur": 1.0, "desc": "1.0s Solid Black Pause"},
            {"id": "c6", "type": "speaker", "raw_ss": 915.0, "dur": 3.0, "crop": CROP_GUEST_PUNCH, "desc": "There is the second type of people..."},
            {"id": "c7", "type": "broll", "broll": BROLLS_DIR / "mixkit_influencer_1.mp4", "broll_ss": 2.0, "raw_audio_ss": 918.0, "dur": 4.2, "desc": "They tell you: be like me!"},
            {"id": "c8", "type": "broll", "broll": BROLLS_DIR / "broll_city_skyline.mp4", "broll_ss": 4.0, "dur": 2.5, "desc": "Clean Loop Ending"}
        ],
        "schedule": [
            (0.0, 2.8, ("INFLUENCER VS", "Influential", "👑"), "kinetic_hook"),
            (2.8, 6.3, ("TWO TYPES OF PEOPLE", "👥"), "yellow_card_top"),
            (6.3, 9.5, ("THE INFLUENTIAL PERSON", "🚪"), "tier_b"),
            (9.5, 13.0, ("EVERY DOOR OPENS", "🔑"), "tier_b"),
            (13.0, 14.0, ("", None), "none"),
            (14.0, 17.0, ("THE SECOND TYPE SAYS...", "📱"), "tier_b"),
            (17.0, 21.2, ("BE LIKE ME!", "🤡"), "punch_yellow"),
            (21.2, 23.7, ("COMMAND RESPECT", "Open Doors", "NOT FOLLOWERS", "🏛️"), "loop_ending")
        ]
    },
    {
        "part": 5,
        "name": "Social Media Commodity",
        "export_name": "Reel_IMG_4246_Ref5_Part5.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 1045.0, "dur": 2.8, "crop": CROP_GUEST_PUNCH, "desc": "Free? You are spending your soul..."},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "mixkit_social_media_1.mp4", "broll_ss": 2.0, "raw_audio_ss": 1047.8, "dur": 3.8, "desc": "You are spending your time"},
            {"id": "c3", "type": "speaker_bw", "raw_ss": 1051.6, "dur": 3.2, "crop": CROP_GUEST, "desc": "You are the commodity being sold there"},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "broll_clock.mp4", "broll_ss": 1.0, "raw_audio_ss": 1054.8, "dur": 3.2, "desc": "Do they live their life?"},
            {"id": "c5", "type": "black", "dur": 1.0, "desc": "1.0s Solid Black Pause"},
            {"id": "c6", "type": "speaker", "raw_ss": 1059.0, "dur": 3.0, "crop": CROP_GUEST_PUNCH, "desc": "Influencers are basically actors"},
            {"id": "c7", "type": "broll", "broll": BROLLS_DIR / "mixkit_thinking_1.mp4", "broll_ss": 3.0, "raw_audio_ss": 1062.0, "dur": 4.0, "desc": "It is just a profession"},
            {"id": "c8", "type": "broll", "broll": BROLLS_DIR / "broll_mountains.mp4", "broll_ss": 3.0, "dur": 2.5, "desc": "Clean Loop Ending"}
        ],
        "schedule": [
            (0.0, 2.8, ("SOCIAL MEDIA IS", "Not Free", "💸"), "kinetic_hook"),
            (2.8, 6.6, ("YOU SPEND YOUR SOUL & TIME", "⏳"), "yellow_card_top"),
            (6.6, 9.8, ("YOU ARE THE COMMODITY", "📦"), "tier_b"),
            (9.8, 13.0, ("THEY SELL YOUR ATTENTION", "👁️"), "tier_b"),
            (13.0, 14.0, ("", None), "none"),
            (14.0, 17.0, ("INFLUENCERS ARE ACTORS", "🎭"), "tier_b"),
            (17.0, 21.0, ("IT'S ALL SCRIPTED!", "🎬"), "punch_yellow"),
            (21.0, 23.5, ("OWN YOUR LIFE", "Reclaim Time", "DON'T BE SOLD", "⛰️"), "loop_ending")
        ]
    },
    {
        "part": 6,
        "name": "Losing Independence & Integrity",
        "export_name": "Reel_IMG_4246_Ref5_Part6.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 1640.0, "dur": 3.0, "crop": CROP_GUEST_PUNCH, "desc": "The person loses the innocence..."},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "broll_empty_room.mp4", "broll_ss": 2.0, "raw_audio_ss": 1643.0, "dur": 3.5, "desc": "The person loses his integrity"},
            {"id": "c3", "type": "speaker_bw", "raw_ss": 1646.5, "dur": 3.2, "crop": CROP_GUEST, "desc": "He loses his influence on himself"},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "mixkit_friends_1.mp4", "broll_ss": 3.0, "raw_audio_ss": 1649.7, "dur": 3.5, "desc": "Always dependent on someone else"},
            {"id": "c5", "type": "black", "dur": 1.0, "desc": "1.0s Solid Black Pause"},
            {"id": "c6", "type": "speaker", "raw_ss": 1654.2, "dur": 3.0, "crop": CROP_GUEST_PUNCH, "desc": "Someone who says they are independent..."},
            {"id": "c7", "type": "broll", "broll": BROLLS_DIR / "mixkit_success_1.mp4", "broll_ss": 1.0, "raw_audio_ss": 1657.2, "dur": 4.0, "desc": "Totally dependent on it"},
            {"id": "c8", "type": "broll", "broll": BROLLS_DIR / "broll_golden_sunrise.mp4", "broll_ss": 3.0, "dur": 2.5, "desc": "Clean Loop Ending"}
        ],
        "schedule": [
            (0.0, 3.0, ("THE INDEPENDENCE", "Paradox?", "⚖️"), "kinetic_hook"),
            (3.0, 6.5, ("LOSING INNOCENCE & INTEGRITY", "🥀"), "yellow_card_top"),
            (6.5, 9.7, ("LOSING SELF INFLUENCE", "🌪️"), "tier_b"),
            (9.7, 13.2, ("DEPENDENT ON VALIDATION", "⛓️"), "tier_b"),
            (13.2, 14.2, ("", None), "none"),
            (14.2, 17.2, ("THEY CALL IT INDEPENDENCE", "🤔"), "tier_b"),
            (17.2, 21.2, ("TRUE FREEDOM IS SELF TRUST", "🦅"), "punch_yellow"),
            (21.2, 23.7, ("STAND IN TRUTH", "Keep Integrity", "UNSHAKEABLE", "🌅"), "loop_ending")
        ]
    }
]

def render_ref5_reel(cfg):
    part = cfg["part"]
    name = cfg["name"]
    export_path = EXPORT_DIR / cfg["export_name"]
    cuts = cfg["cuts"]
    schedule = cfg["schedule"]
    total_dur = sum(c["dur"] for c in cuts)
    
    print(f"\n{'='*70}\n🚀 RENDERING REF5 REEL PART {part}: {name} ({total_dur:.2f}s)\n{'='*70}")
    
    # 1. Render Video Cuts
    concat_list = WORKSPACE / f"ref5_p{part}_video_cuts.txt"
    with open(concat_list, "w") as f_out:
        for idx, cut in enumerate(cuts):
            cut_mp4 = WORKSPACE / f"ref5_p{part}_cut_{idx:02d}.mp4"
            dur = cut["dur"]
            
            if cut["type"] == "black":
                cmd = [
                    "ffmpeg", "-y", "-f", "lavfi",
                    "-i", f"color=c=0x0A0A0A:s={WIDTH}x{HEIGHT}:d={dur:.3f}:r={FPS}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", str(cut_mp4)
                ]
            elif cut["type"] == "speaker":
                crop = cut["crop"]
                vf = f"{crop},{COLOR_GRADE},{SDR_FILTER},fps={FPS},setsar=1"
                cmd = [
                    "ffmpeg", "-y", "-accurate_seek", "-ss", f"{cut['raw_ss']:.3f}", "-t", f"{dur:.3f}",
                    "-i", str(RAW_VIDEO),
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", str(cut_mp4)
                ]
            elif cut["type"] == "speaker_bw":
                crop = cut["crop"]
                vf = f"{crop},hue=s=0,curves=master='0/0.05 0.5/0.5 1/0.95',noise=alls=15:allf=t+u,{SDR_FILTER},fps={FPS},setsar=1"
                cmd = [
                    "ffmpeg", "-y", "-accurate_seek", "-ss", f"{cut['raw_ss']:.3f}", "-t", f"{dur:.3f}",
                    "-i", str(RAW_VIDEO),
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", str(cut_mp4)
                ]
            elif cut["type"] == "broll":
                broll_file = cut["broll"]
                ss = cut.get("broll_ss", 0.0)
                vf = f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},fps={FPS},setsar=1,{COLOR_GRADE},{SDR_FILTER}"
                cmd = [
                    "ffmpeg", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-stream_loop", "-1",
                    "-i", str(broll_file),
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", str(cut_mp4)
                ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            f_out.write(f"file '{cut_mp4.name}'\n")
            
    video_assembled = WORKSPACE / f"ref5_p{part}_video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "copy", str(video_assembled)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Master Audio & SFX
    dialogue_cuts = []
    for idx, cut in enumerate(cuts):
        out_wav = WORKSPACE / f"ref5_p{part}_audio_{idx:02d}.wav"
        dur = cut["dur"]
        if cut["type"] == "black" or idx == len(cuts) - 1:
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={dur:.3f}",
                "-c:a", "pcm_s16le", str(out_wav)
            ]
        elif "raw_ss" in cut:
            cmd = [
                "ffmpeg", "-y", "-accurate_seek", "-ss", f"{cut['raw_ss']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO), "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(out_wav)
            ]
        elif "raw_audio_ss" in cut:
            cmd = [
                "ffmpeg", "-y", "-accurate_seek", "-ss", f"{cut['raw_audio_ss']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO), "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(out_wav)
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dialogue_cuts.append(out_wav)
        
    concat_audio_txt = WORKSPACE / f"ref5_p{part}_audio_concat.txt"
    with open(concat_audio_txt, "w") as f:
        for wav in dialogue_cuts:
            f.write(f"file '{wav.name}'\n")
            
    raw_dialogue = WORKSPACE / f"ref5_p{part}_dialogue.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_audio_txt),
        "-c:a", "pcm_s16le", str(raw_dialogue)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Tactile SFX
    sfx_filter = (
        f"[1:a]asplit=2[h1][h2];"
        f"[h1]adelay=0|0,volume=0.55[sfx_h0];"
        f"[2:a]adelay=3000|3000,volume=0.45[sfx_w1];"
        f"[4:a]adelay=13000|13000,volume=0.50[sfx_rise];"
        f"[h2]adelay=17000|17000,volume=0.60[sfx_h1];"
        f"[sfx_h0][sfx_w1][sfx_rise][sfx_h1]amix=inputs=4:normalize=0[all_sfx]"
    )
    sfx_track = WORKSPACE / f"ref5_p{part}_sfx.wav"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_dialogue),
        "-i", str(SFX_HIT),
        "-i", str(SFX_WHOOSH),
        "-i", str(SFX_POP),
        "-i", str(SFX_RISER),
        "-filter_complex", sfx_filter,
        "-map", "[all_sfx]", "-c:a", "pcm_s16le", str(sfx_track)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Pro Audio Master (-14 LUFS)
    pro_audio = WORKSPACE / f"ref5_p{part}_master_audio.wav"
    master_filter = (
        f"[1:a]volume=0.018,aloop=loop=-1:size=2e+09,afade=t=in:st=0:d=1.5,afade=t=out:st={total_dur-2.0}:d=2.0[bgm];"
        f"[0:a][2:a]amix=inputs=2:normalize=0[dialogue_sfx];"
        f"[dialogue_sfx][bgm]amix=inputs=2:duration=first:dropout_transition=2,"
        f"loudnorm=I=-14.0:TP=-1.0:LRA=11[aout]"
    )
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_dialogue),
        "-i", str(BGM_TRACK),
        "-i", str(sfx_track),
        "-filter_complex", master_filter,
        "-map", "[aout]", "-c:a", "pcm_s16le", str(pro_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Typography & Graphics Overlay
    overlay_mov = WORKSPACE / f"ref5_p{part}_overlay.mov"
    f_title_setup = ImageFont.truetype(FONT_SANS_REG, 75)
    f_title_hero = ImageFont.truetype(FONT_SERIF_ITALIC, 175)
    f_title_allcaps = ImageFont.truetype(FONT_SERIF_REG, 95)
    
    total_frames = int(total_dur * FPS)
    pipe = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS),
        "-i", "-", "-c:v", "png", "-r", str(FPS), str(overlay_mov)
    ], stdin=subprocess.PIPE)
    
    empty_frame = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0)).tobytes()
    
    for frame_idx in range(total_frames):
        t = frame_idx / float(FPS)
        active_event = None
        for (st, et, data, style) in schedule:
            if st <= t < et:
                active_event = (st, et, data, style)
                break
                
        if not active_event or active_event[3] == "none":
            pipe.stdin.write(empty_frame)
            continue
            
        st, et, data, style = active_event
        im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        
        if style == "kinetic_hook":
            setup_txt, hero_txt, emoji_char = data
            draw_spaced_sans(draw, setup_txt, y=420, font=f_title_setup, fill_color=COLOR_WHITE)
            draw_serif_hero(draw, im, hero_txt, emoji_char, y=520, font=f_title_hero, fill_color=COLOR_YELLOW)
        elif style == "yellow_card_top":
            txt, emoji_char = data
            draw_yellow_card(draw, im, txt, emoji_char, sy=480, font_size=64)
        elif style == "tier_b":
            txt, emoji_char = data
            draw_boxed_sub(draw, im, txt, emoji_char, font_size=84, y_pos=1440)
        elif style == "punch_yellow":
            txt, emoji_char = data
            draw_yellow_card(draw, im, txt, emoji_char, sy=1440, font_size=72)
        elif style == "loop_ending":
            setup_txt, hero_txt, sub_txt, emoji_char = data
            draw_spaced_sans(draw, setup_txt, y=400, font=f_title_setup, fill_color=COLOR_WHITE)
            draw_serif_hero(draw, im, hero_txt, emoji_char, y=500, font=f_title_hero, fill_color=COLOR_YELLOW)
            draw_serif_hero(draw, im, sub_txt, None, y=700, font=f_title_allcaps, fill_color=COLOR_WHITE)
            
        pipe.stdin.write(im.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    
    # 4. Final Composite
    print(f"🎬 Merging final export for Part {part}...")
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(video_assembled),
        "-i", str(overlay_mov),
        "-i", str(pro_audio),
        "-filter_complex", "[0:v][1:v]overlay=0:0[vout]",
        "-map", "[vout]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(export_path)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    size_mb = export_path.stat().st_size / 1024 / 1024
    print(f"✅ EXPORTED REF5 PART {part}: {export_path} ({size_mb:.2f} MB)")
    return export_path

def main():
    print("=================================================================")
    print("STARTING 5-REEL BATCH RENDER FOR REFERENCE 5 (REF5) STYLE")
    print("=================================================================")
    start_all = time.time()
    
    exported = []
    for cfg in REELS_REF5:
        t0 = time.time()
        p = render_ref5_reel(cfg)
        elapsed = time.time() - t0
        exported.append((p, elapsed))
        
    print("\n" + "="*70)
    print("🎉 ALL 5 REF5 REELS COMPLETED SUCCESSFULLY!")
    for p, elapsed in exported:
        print(f"  * {p.name} ({p.stat().st_size/1024/1024:.2f} MB) in {elapsed:.1f}s")
    print(f"Total Batch Runtime: {(time.time() - start_all)/60:.2f} minutes")
    print("="*70)

if __name__ == "__main__":
    main()
