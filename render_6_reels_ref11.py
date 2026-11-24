#!/usr/bin/env python3
"""
Multi-Reel Batch Render Engine for Reference 11 (Ref11) Style.
Renders 6 Reels from IMG_4246.MOV:
  - Reel_IMG_4246_Ref11_Part1.mp4 ("Chemistry of Love ❤️")
  - Reel_IMG_4246_Ref11_Part2.mp4 ("Why True Love Brings Peace 💤")
  - Reel_IMG_4246_Ref11_Part3.mp4 ("The Love Of My Life Trap 💔")
  - Reel_IMG_4246_Ref11_Part4.mp4 ("Two Types of Influence 👑")
  - Reel_IMG_4246_Ref11_Part5.mp4 ("Know Your Boundaries 🛡️")
  - Reel_IMG_4246_Ref11_Part6.mp4 ("When Friendships Break 🤝")

Strict Ref11 Specifications:
1. Canvas: 1080x1920 @ 30fps.
2. Top Bar: Y = 0..408 (Solid Black).
3. Header Banner: Y = 408..558 (Height 150px):
   - Background: Signature Reference 11 Orange #FF8400 (RGB: 255, 132, 0).
   - 3px solid black border lines top and bottom.
   - High-impact bold title + emoji.
4. Active Video Window: Y = 558..1498 (Height 940px, centered):
   - 100% Locked on Person 1 (Guest, X=2890): crop=1215:1050:2282:350,scale=1080:940.
   - Never show host or wide 2-shot!
   - 0.6s B&W hook snap into warm natural color grade.
   - Thematic B-Roll cutaways inside the 1080x940 window (100% unique, zero duplicates).
5. Subtitles:
   - Lower third of video window (Y = 1340).
   - Signature Orange #FF8400 with 7px solid black stroke & drop shadow.
   - Rapid speech beats synchronized to dialogue.
6. Bottom Bar: Y = 1498..1920 (Solid Black).
7. Audio: -14 LUFS pro audio with mild ducked ambient BGM.
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

BGM_TRACK = AUDIO_DIR / "ref5_bgm.mp3"

WIDTH = 1080
HEIGHT = 1920
VIDEO_H = 940
VIDEO_Y = 558
BANNER_Y = 408
BANNER_H = 150
SUBS_Y = 1340
FPS = 30

# Colors
COLOR_ORANGE = (255, 132, 0, 255) # #FF8400
COLOR_BLACK = (0, 0, 0, 255)
COLOR_WHITE = (255, 255, 255, 255)

# Fonts
FONT_BANNER = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_SUBS = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"
font_emoji = ImageFont.truetype(EMOJI_FONT, 160)

# SDR BT.709 Pipeline
COLOR_GRADE = (
    "curves=master='0/0.02 0.5/0.52 1/0.98',"
    "eq=contrast=1.12:saturation=1.20:brightness=0.015,"
    "colorbalance=rs=0.03:gs=0.01:bs=-0.03"
)
SDR_FILTER = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,format=yuv420p"

# Person 1 (Guest, X=2890) inside 1080x940 window
CROP_GUEST_REF11 = "crop=1215:1050:2282:350,scale=1080:940:flags=lanczos"
CROP_GUEST_PUNCH = "crop=1050:908:2365:420,scale=1080:940:flags=lanczos"

def render_emoji(char, target_size=60):
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

def generate_header_banner(title, emoji_char, out_path):
    im = Image.new("RGBA", (WIDTH, BANNER_H), COLOR_ORANGE)
    draw = ImageDraw.Draw(im)
    
    # 3px solid black border lines top and bottom
    draw.rectangle([0, 0, WIDTH, 3], fill=COLOR_BLACK)
    draw.rectangle([0, BANNER_H - 3, WIDTH, BANNER_H], fill=COLOR_BLACK)
    
    font = ImageFont.truetype(FONT_BANNER, 56)
    bbox = font.getbbox(title)
    txt_w = bbox[2] - bbox[0]
    txt_h = bbox[3] - bbox[1]
    
    emoji_im = None
    emoji_w = 0
    if emoji_char:
        emoji_im = render_emoji(emoji_char, target_size=56)
        emoji_w = emoji_im.width + 15
        
    total_w = txt_w + emoji_w
    cur_x = (WIDTH - total_w) // 2
    cur_y = (BANNER_H - txt_h) // 2 - 4
    
    draw.text((cur_x, cur_y), title, font=font, fill=COLOR_BLACK)
    if emoji_im:
        im.paste(emoji_im, (cur_x + txt_w + 15, (BANNER_H - emoji_im.height) // 2), emoji_im)
        
    im.save(out_path)

def draw_ref11_sub(draw, im, text, emoji_char):
    font = ImageFont.truetype(FONT_SUBS, 72)
    bbox = font.getbbox(text)
    txt_w = bbox[2] - bbox[0]
    txt_h = bbox[3] - bbox[1]
    
    emoji_im = None
    emoji_w = 0
    if emoji_char:
        emoji_im = render_emoji(emoji_char, target_size=68)
        emoji_w = emoji_im.width + 15
        
    total_w = txt_w + emoji_w
    cur_x = (WIDTH - total_w) // 2
    cur_y = SUBS_Y
    
    # 7px solid black stroke
    for dx in range(-7, 8):
        for dy in range(-7, 8):
            if dx*dx + dy*dy <= 49:
                draw.text((cur_x + dx, cur_y + dy), text, font=font, fill=COLOR_BLACK)
    # Fill in #FF8400 Signature Orange
    draw.text((cur_x, cur_y), text, font=font, fill=COLOR_ORANGE)
    
    if emoji_im:
        im.paste(emoji_im, (cur_x + txt_w + 15, cur_y + (txt_h - emoji_im.height) // 2), emoji_im)

# ==============================================================================
# 6 REELS CONFIGURATION FOR REF11 STYLE
# ==============================================================================
REELS_REF11 = [
    {
        "part": 1,
        "title": "Chemistry of Love",
        "emoji": "❤️",
        "export_name": "Reel_IMG_4246_Ref11_Part1.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 131.9, "dur": 3.0, "crop": CROP_GUEST_REF11, "hook_bw": True, "desc": "Modern love or confusion"},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "mixkit_driving_1.mp4", "broll_ss": 2.0, "raw_audio_ss": 134.9, "dur": 3.5, "desc": "Extreme stage of attraction"},
            {"id": "c3", "type": "speaker", "raw_ss": 149.0, "dur": 3.2, "crop": CROP_GUEST_PUNCH, "desc": "Love is basically a chemical feeling"},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "mixkit_sunset_2.mp4", "broll_ss": 1.0, "raw_audio_ss": 167.3, "dur": 4.0, "desc": "Rush of dopamine & oxytocin"},
            {"id": "c5", "type": "speaker", "raw_ss": 171.3, "dur": 3.5, "crop": CROP_GUEST_REF11, "desc": "Serotonin sleep hormone"},
            {"id": "c6", "type": "broll", "broll": BROLLS_DIR / "broll_forest_mist.mp4", "broll_ss": 0.5, "dur": 2.0, "desc": "Loop ending"}
        ],
        "subs": [
            (0.0, 3.0, "MODERN LOVE OR CONFUSION?", "🤔"),
            (3.0, 6.5, "STAGE OF ATTRACTION", "❤️"),
            (6.5, 9.7, "CHEMICAL REACTION", "🧪"),
            (9.7, 13.7, "RUSH OF OXYTOCIN", "⚡"),
            (13.7, 17.2, "SEROTONIN SLEEP HORMONE", "😴"),
            (17.2, 19.2, "TRUE PEACE OF MIND", "✨")
        ]
    },
    {
        "part": 2,
        "title": "Why True Love Brings Peace",
        "emoji": "💤",
        "export_name": "Reel_IMG_4246_Ref11_Part2.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 180.0, "dur": 3.0, "crop": CROP_GUEST_REF11, "hook_bw": True, "desc": "You sleep well when comfortable"},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "mixkit_sleep_1.mp4", "broll_ss": 2.0, "raw_audio_ss": 183.0, "dur": 3.8, "desc": "Sleeping peacefully"},
            {"id": "c3", "type": "speaker", "raw_ss": 186.8, "dur": 3.2, "crop": CROP_GUEST_PUNCH, "desc": "Men in relationship put on weight"},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "mixkit_coffee_2.mp4", "broll_ss": 1.0, "raw_audio_ss": 193.0, "dur": 3.5, "desc": "Because no stress"},
            {"id": "c5", "type": "speaker", "raw_ss": 196.5, "dur": 3.5, "crop": CROP_GUEST_REF11, "desc": "Scientifically hair gets curlier"},
            {"id": "c6", "type": "broll", "broll": BROLLS_DIR / "broll_curly_hair.mp4", "broll_ss": 1.0, "dur": 2.2, "desc": "Loop ending"}
        ],
        "subs": [
            (0.0, 3.0, "YOU SLEEP WELL?", "🛌"),
            (3.0, 6.8, "AROUND COMFORTABLE PEOPLE", "🤍"),
            (6.8, 10.0, "HAPPY COUPLES PUT ON WEIGHT", "🍔"),
            (10.0, 13.5, "BECAUSE NO STRESS!", "😎"),
            (13.5, 17.0, "HAIR GETS CURLIER!", "✨"),
            (17.0, 19.2, "HEALTHY RELATIONSHIP", "🥂")
        ]
    },
    {
        "part": 3,
        "title": "The Love Of My Life Trap",
        "emoji": "💔",
        "export_name": "Reel_IMG_4246_Ref11_Part3.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 455.0, "dur": 3.0, "crop": CROP_GUEST_REF11, "hook_bw": True, "desc": "I think I found the love of my life"},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "mixkit_car_1.mp4", "broll_ss": 1.0, "raw_audio_ss": 458.0, "dur": 3.5, "desc": "He dropped down and came home"},
            {"id": "c3", "type": "speaker", "raw_ss": 461.5, "dur": 3.2, "crop": CROP_GUEST_PUNCH, "desc": "We have a lot of things in common"},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "broll_breakup.mp4", "broll_ss": 2.0, "raw_audio_ss": 468.0, "dur": 3.8, "desc": "Preference and discussions"},
            {"id": "c5", "type": "speaker", "raw_ss": 472.0, "dur": 3.2, "crop": CROP_GUEST_REF11, "desc": "This was something I also experienced"},
            {"id": "c6", "type": "broll", "broll": BROLLS_DIR / "mixkit_thinking_2.mp4", "broll_ss": 1.0, "dur": 2.2, "desc": "Loop ending"}
        ],
        "subs": [
            (0.0, 3.0, "FOUND THE LOVE OF MY LIFE?", "💘"),
            (3.0, 6.5, "A LOT OF THINGS IN COMMON", "👀"),
            (6.5, 9.7, "PLANNING TO GET MARRIED", "💍"),
            (9.7, 13.5, "TALKING ABOUT WORK & PREFERENCES", "⚖️"),
            (13.5, 16.7, "IS IT REAL COMPATIBILITY?", "❓"),
            (16.7, 18.9, "TEST BEFORE YOU COMMIT", "🛡️")
        ]
    },
    {
        "part": 4,
        "title": "Two Types of Influence",
        "emoji": "👑",
        "export_name": "Reel_IMG_4246_Ref11_Part4.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 900.0, "dur": 3.0, "crop": CROP_GUEST_REF11, "hook_bw": True, "desc": "What do you think about influencer culture?"},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "broll_startup_team.mp4", "broll_ss": 1.0, "raw_audio_ss": 903.0, "dur": 3.8, "desc": "The influential person"},
            {"id": "c3", "type": "speaker", "raw_ss": 906.8, "dur": 3.2, "crop": CROP_GUEST_PUNCH, "desc": "He goes, every door opens"},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "broll_stock_growth.mp4", "broll_ss": 2.0, "raw_audio_ss": 910.0, "dur": 3.5, "desc": "Everyone knows him"},
            {"id": "c5", "type": "speaker", "raw_ss": 913.5, "dur": 3.2, "crop": CROP_GUEST_REF11, "desc": "Influencer says: be like me"},
            {"id": "c6", "type": "broll", "broll": BROLLS_DIR / "mixkit_influencer_2.mp4", "broll_ss": 0.5, "dur": 2.2, "desc": "Loop ending"}
        ],
        "subs": [
            (0.0, 3.0, "WHAT IS INFLUENCE?", "👑"),
            (3.0, 6.8, "THE INFLUENTIAL PERSON", "💼"),
            (6.8, 10.0, "EVERY DOOR OPENS FOR HIM", "🚪"),
            (10.0, 13.5, "EVERYONE DOES ANY FAVOR", "🤝"),
            (13.5, 16.7, "INFLUENCERS SAY: BE LIKE ME", "📱"),
            (16.7, 18.9, "BUILD REAL AUTHORITY", "🏛️")
        ]
    },
    {
        "part": 5,
        "title": "Know Your Boundaries",
        "emoji": "🛡️",
        "export_name": "Reel_IMG_4246_Ref11_Part5.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 1495.0, "dur": 3.0, "crop": CROP_GUEST_REF11, "hook_bw": True, "desc": "Stay in our boundaries"},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "broll_river.mp4", "broll_ss": 2.0, "raw_audio_ss": 1498.0, "dur": 3.8, "desc": "Don't beg for something"},
            {"id": "c3", "type": "speaker", "raw_ss": 1501.8, "dur": 3.2, "crop": CROP_GUEST_PUNCH, "desc": "When we breach the circle"},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "broll_forest.mp4", "broll_ss": 1.0, "raw_audio_ss": 1505.0, "dur": 3.5, "desc": "We are torn apart"},
            {"id": "c5", "type": "speaker", "raw_ss": 1508.5, "dur": 3.2, "crop": CROP_GUEST_REF11, "desc": "If someone steps out it is for good"},
            {"id": "c6", "type": "broll", "broll": BROLLS_DIR / "mixkit_nature_2.mp4", "broll_ss": 0.5, "dur": 2.2, "desc": "Loop ending"}
        ],
        "subs": [
            (0.0, 3.0, "STAY IN YOUR BOUNDARIES", "🛡️"),
            (3.0, 6.8, "DON'T BEG TO BE ACCEPTED", "🚫"),
            (6.8, 10.0, "WHEN WE BREACH THE CIRCLE", "⚠️"),
            (10.0, 13.5, "WE GET TORN APART", "💔"),
            (13.5, 16.7, "LEAVING IS FOR GOOD", "🕊️"),
            (16.7, 18.9, "RESPECT YOUR WORTH", "👑")
        ]
    },
    {
        "part": 6,
        "title": "When Friendships Break",
        "emoji": "🤝",
        "export_name": "Reel_IMG_4246_Ref11_Part6.mp4",
        "cuts": [
            {"id": "c1", "type": "speaker", "raw_ss": 1530.0, "dur": 3.0, "crop": CROP_GUEST_REF11, "hook_bw": True, "desc": "Hard break in our friends"},
            {"id": "c2", "type": "broll", "broll": BROLLS_DIR / "broll_crowd_promenade.mp4", "broll_ss": 2.0, "raw_audio_ss": 1533.0, "dur": 3.5, "desc": "When it comes to the end"},
            {"id": "c3", "type": "speaker", "raw_ss": 1536.5, "dur": 3.2, "crop": CROP_GUEST_PUNCH, "desc": "They are not going to come back"},
            {"id": "c4", "type": "broll", "broll": BROLLS_DIR / "mixkit_friends_2.mp4", "broll_ss": 0.5, "raw_audio_ss": 1540.0, "dur": 3.5, "desc": "When the same thing happens within us"},
            {"id": "c5", "type": "speaker", "raw_ss": 1543.5, "dur": 3.2, "crop": CROP_GUEST_REF11, "desc": "You can't force it"},
            {"id": "c6", "type": "broll", "broll": BROLLS_DIR / "broll_forest_mist.mp4", "broll_ss": 1.0, "dur": 2.2, "desc": "Loop ending"}
        ],
        "subs": [
            (0.0, 3.0, "FRIENDSHIP HARD BREAKS", "💔"),
            (3.0, 6.5, "THEY ARE NOT COMING BACK", "🚶"),
            (6.5, 9.7, "YOU CANNOT FORCE CONNECTION", "⛓️"),
            (9.7, 13.2, "ACCEPT THE REALITY", "🧠"),
            (13.2, 16.4, "FOCUS ON YOUR PATH", "🧭"),
            (16.4, 18.6, "PROTECT YOUR PEACE", "🕊️")
        ]
    }
]

def render_ref11_reel(cfg):
    part = cfg["part"]
    title = cfg["title"]
    emoji_char = cfg["emoji"]
    export_path = EXPORT_DIR / cfg["export_name"]
    cuts = cfg["cuts"]
    subs = cfg["subs"]
    total_dur = sum(c["dur"] for c in cuts)
    
    print(f"\n{'='*70}\n🚀 RENDERING REF11 REEL PART {part}: {title} ({total_dur:.2f}s)\n{'='*70}")
    
    # 1. Header Banner
    banner_png = WORKSPACE / f"ref11_p{part}_banner.png"
    generate_header_banner(title, emoji_char, banner_png)
    
    # 2. Render Video Window Cuts (1080x940)
    concat_list = WORKSPACE / f"ref11_p{part}_video_cuts.txt"
    with open(concat_list, "w") as f_out:
        for idx, cut in enumerate(cuts):
            cut_mp4 = WORKSPACE / f"ref11_p{part}_cut_{idx:02d}.mp4"
            dur = cut["dur"]
            
            if cut["type"] == "speaker":
                crop = cut["crop"]
                if cut.get("hook_bw", False):
                    vf = f"{crop},{COLOR_GRADE},hue=s=0,fade=t=out:st=0.6:d=0.3,{SDR_FILTER},fps={FPS},setsar=1"
                else:
                    vf = f"{crop},{COLOR_GRADE},{SDR_FILTER},fps={FPS},setsar=1"
                cmd = [
                    "ffmpeg", "-y", "-accurate_seek", "-ss", f"{cut['raw_ss']:.3f}", "-t", f"{dur:.3f}",
                    "-i", str(RAW_VIDEO),
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", str(cut_mp4)
                ]
            elif cut["type"] == "broll":
                broll_file = cut["broll"]
                ss = cut.get("broll_ss", 0.0)
                vf = f"scale={WIDTH}:{VIDEO_H}:force_original_aspect_ratio=increase,crop={WIDTH}:{VIDEO_H},fps={FPS},setsar=1,{COLOR_GRADE},{SDR_FILTER}"
                cmd = [
                    "ffmpeg", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-stream_loop", "-1",
                    "-i", str(broll_file),
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", str(cut_mp4)
                ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            f_out.write(f"file '{cut_mp4.name}'\n")
            
    window_video = WORKSPACE / f"ref11_p{part}_window.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "copy", str(window_video)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Master Audio
    dialogue_cuts = []
    for idx, cut in enumerate(cuts):
        out_wav = WORKSPACE / f"ref11_p{part}_audio_{idx:02d}.wav"
        dur = cut["dur"]
        if idx == len(cuts) - 1:
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
        
    concat_audio_txt = WORKSPACE / f"ref11_p{part}_audio_concat.txt"
    with open(concat_audio_txt, "w") as f:
        for wav in dialogue_cuts:
            f.write(f"file '{wav.name}'\n")
            
    raw_dialogue = WORKSPACE / f"ref11_p{part}_dialogue.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_audio_txt),
        "-c:a", "pcm_s16le", str(raw_dialogue)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    pro_audio = WORKSPACE / f"ref11_p{part}_master_audio.wav"
    master_filter = (
        f"[1:a]volume=0.015,aloop=loop=-1:size=2e+09,afade=t=in:st=0:d=1.5,afade=t=out:st={total_dur-2.0}:d=2.0[bgm];"
        f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,"
        f"loudnorm=I=-14.0:TP=-1.0:LRA=11[aout]"
    )
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_dialogue),
        "-i", str(BGM_TRACK),
        "-filter_complex", master_filter,
        "-map", "[aout]", "-c:a", "pcm_s16le", str(pro_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 4. Subtitles Overlay (1080x1920)
    overlay_mov = WORKSPACE / f"ref11_p{part}_subs.mov"
    total_frames = int(total_dur * FPS)
    pipe = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS),
        "-i", "-", "-c:v", "png", "-r", str(FPS), str(overlay_mov)
    ], stdin=subprocess.PIPE)
    
    empty_frame = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0)).tobytes()
    
    for frame_idx in range(total_frames):
        t = frame_idx / float(FPS)
        active_sub = None
        for (st, et, text, emoji_c) in subs:
            if st <= t < et:
                active_sub = (text, emoji_c)
                break
                
        if not active_sub:
            pipe.stdin.write(empty_frame)
            continue
            
        text, emoji_c = active_sub
        im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw_ref11_sub(draw, im, text, emoji_c)
        pipe.stdin.write(im.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    
    # 5. Composite into full 1080x1920 Reference 11 Canvas
    print(f"🎬 Merging final export for Ref11 Part {part}...")
    canvas_filter = (
        f"color=c=0x000000:s={WIDTH}x{HEIGHT}:d={total_dur:.3f}:r={FPS}[base];"
        f"[base][0:v]overlay=0:{VIDEO_Y}[with_win];"
        f"[with_win][1:v]overlay=0:{BANNER_Y}[with_banner];"
        f"[with_banner][2:v]overlay=0:0[vout]"
    )
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(window_video),
        "-i", str(banner_png),
        "-i", str(overlay_mov),
        "-i", str(pro_audio),
        "-filter_complex", canvas_filter,
        "-map", "[vout]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(export_path)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    size_mb = export_path.stat().st_size / 1024 / 1024
    print(f"✅ EXPORTED REF11 PART {part}: {export_path} ({size_mb:.2f} MB)")
    return export_path

def main():
    print("=================================================================")
    print("STARTING 6-REEL BATCH RENDER FOR REFERENCE 11 (REF11) STYLE")
    print("=================================================================")
    start_all = time.time()
    
    exported = []
    for cfg in REELS_REF11:
        t0 = time.time()
        p = render_ref11_reel(cfg)
        elapsed = time.time() - t0
        exported.append((p, elapsed))
        
    print("\n" + "="*70)
    print("🎉 ALL 6 REF11 REELS COMPLETED SUCCESSFULLY!")
    for p, elapsed in exported:
        print(f"  * {p.name} ({p.stat().st_size/1024/1024:.2f} MB) in {elapsed:.1f}s")
    print(f"Total Batch Runtime: {(time.time() - start_all)/60:.2f} minutes")
    print("="*70)

if __name__ == "__main__":
    main()
