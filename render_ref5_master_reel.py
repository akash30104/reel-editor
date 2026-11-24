#!/usr/bin/env python3
"""
Master Render Engine for Reference 5 (Ref5) Style Instagram Reel / YouTube Short.
Source: IMG_4246.MOV (4K 60fps) -> 9:16 Vertical (1080x1920 @ 30fps)
"""

import os
import sys
import json
import time
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Workspace Paths
WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Desktop/reels editor/raw videos/IMG_4246.MOV")
EXPORT_DIR = Path("/Users/pgi/Desktop/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

FONTS_DIR = WORKSPACE / "assets" / "fonts"
AUDIO_DIR = WORKSPACE / "assets" / "audio"
STICKERS_DIR = WORKSPACE / "assets" / "stickers"
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
FONT_SANS_ITALIC = str(FONTS_DIR / "Montserrat-Italic.ttf")
FONT_SUB = str(FONTS_DIR / "Inter-Variable.ttf")

# Dimensions & FPS
WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Strict 3-Color Palette
COLOR_YELLOW = (255, 242, 0, 255)  # #FFF200 Bright Yellow
COLOR_WHITE = (255, 255, 255, 255) # #FFFFFF Pure White
COLOR_BLACK = (10, 10, 10, 255)     # #0A0A0A Jet Black
COLOR_SHADOW = (10, 10, 10, 180)

# Studio Color Grade for IMG_4246
COLOR_GRADE = (
    "curves=master='0/0.02 0.5/0.52 1/0.98',"
    "eq=contrast=1.15:saturation=1.25:brightness=0.015,"
    "colorbalance=rs=0.04:gs=0.02:bs=-0.04"
)
SDR_FILTER = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,format=yuv420p"

# Speaker Crops
CROP_GUEST = "crop=1215:2160:2140:0,scale=1080:1920:flags=lanczos"
CROP_GUEST_PUNCH = "crop=1050:1866:2220:147,scale=1080:1920:flags=lanczos"
CROP_HOST = "crop=1215:2160:740:0,scale=1080:1920:flags=lanczos"

# External B-Rolls
BROLL_PHONE = BROLLS_DIR / "broll_phone_dating.mp4"
BROLL_COUPLE = BROLLS_DIR / "broll_couple.mp4"
BROLL_BREAKUP = BROLLS_DIR / "broll_breakup.mp4"
BROLL_MOVIE = Path("/Users/pgi/Downloads/vidssave.com Best love scene _ true love _ irugapatru movie _ #shorts #movie #love #emotional 1080P.mp4")
BROLL_HABITS = Path("/Users/pgi/Downloads/From Klickpin.com- Sweet couple habits for people who love beauty for busy days for meaningful relationships-pin-id-1125688869368431907.mp4")
BROLL_FOOD = Path("/Users/pgi/Downloads/From Klickpin.com- Refresh this smart comfort food roundup that look high-end but stay practical that balance trend comfort and everyday function.mp4")
BROLL_SUNRISE = BROLLS_DIR / "broll_golden_sunrise.mp4"

# Cut Schedule Definition
# Each cut: {type: "speaker"|"broll"|"black", dur: float, ...}
CUTS = [
    # 0.0s - 2.9s: Cold Open Hook Statement (Guest Punch)
    {
        "id": "01_hook_q",
        "type": "speaker",
        "raw_ss": 131.90,
        "dur": 2.90,
        "crop": CROP_GUEST_PUNCH,
        "desc": "Modern love or modern confusion?"
    },
    # 2.9s - 5.1s: Situationship is not love (B-Roll Phone Dating)
    {
        "id": "02_hook_a",
        "type": "broll",
        "broll": BROLL_PHONE,
        "broll_ss": 1.0,
        "raw_audio_ss": 135.90,
        "dur": 2.20,
        "desc": "Situationship is NOT a modern love!"
    },
    # 5.1s - 8.1s: Host Question - SELECTIVE B&W BEAT WITH VINTAGE GRAIN!
    {
        "id": "03_question_bw",
        "type": "speaker_bw",
        "raw_ss": 149.10,
        "dur": 3.00,
        "crop": CROP_HOST,
        "desc": "What is the meaning of it? How does it feel?"
    },
    # 8.1s - 11.0s: Extreme stage of attraction (B-Roll Couple)
    {
        "id": "04_attraction_broll",
        "type": "broll",
        "broll": BROLL_COUPLE,
        "broll_ss": 2.0,
        "raw_audio_ss": 152.10,
        "dur": 2.90,
        "desc": "It is an extreme stage of attraction!"
    },
    # 11.0s - 13.1s: Extreme stage of infatuation (B-Roll Breakup Tension)
    {
        "id": "05_infatuation_broll",
        "type": "broll",
        "broll": BROLL_BREAKUP,
        "broll_ss": 3.0,
        "raw_audio_ss": 158.10,
        "dur": 2.10,
        "desc": "Extreme stage of infatuation!"
    },
    # 13.1s - 16.0s: Love is basically a chemical feeling (B-Roll Movie Scene)
    {
        "id": "06_chem_movie",
        "type": "broll",
        "broll": BROLL_MOVIE,
        "broll_ss": 10.0,
        "raw_audio_ss": 164.40,
        "dur": 2.90,
        "desc": "Love is basically a chemical feeling..."
    },
    # 16.0s - 18.5s: Rush of Dopamine! (B-Roll Couple Afloat)
    {
        "id": "07_dopamine",
        "type": "broll",
        "broll": BROLL_COUPLE,
        "broll_ss": 6.5,
        "raw_audio_ss": 167.30,
        "dur": 2.50,
        "desc": "Rush of Dopamine!"
    },
    # 18.5s - 21.5s: Rush of Oxytocin! (Guest Talking Head Punch)
    {
        "id": "08_oxytocin",
        "type": "speaker",
        "raw_ss": 169.80,
        "dur": 3.00,
        "crop": CROP_GUEST,
        "desc": "Rush of Oxytocin!"
    },
    # 21.5s - 25.9s: Serotonin sleep hormone (B-Roll Golden Sunrise)
    {
        "id": "09_serotonin",
        "type": "broll",
        "broll": BROLL_SUNRISE,
        "broll_ss": 1.0,
        "raw_audio_ss": 172.80,
        "dur": 4.40,
        "desc": "Serotonin is sleep hormone, you relax!"
    },
    # 25.9s - 32.9s: When in love you sleep well (B-Roll Sweet Habits)
    {
        "id": "10_sleep_habits",
        "type": "broll",
        "broll": BROLL_HABITS,
        "broll_ss": 0.5,
        "raw_audio_ss": 179.20,
        "dur": 7.00,
        "desc": "When you are in love you sleep well... around comfortable people!"
    },
    # 32.9s - 33.9s: 1-SECOND SOLID JET BLACK SCREEN PAUSE (ATTENTION RESET)
    {
        "id": "11_black_pause",
        "type": "black",
        "dur": 1.00,
        "desc": "1-Second Solid Jet Black Pause (#0A0A0A)"
    },
    # 33.9s - 37.0s: Men in relationship put on weight (Guest Punch)
    {
        "id": "12_weight_q",
        "type": "speaker",
        "raw_ss": 189.90,
        "dur": 3.10,
        "crop": CROP_GUEST_PUNCH,
        "desc": "Men in happy relationship tend to put on weight. Why?"
    },
    # 37.0s - 40.5s: BECAUSE NO STRESS! (B-Roll Delicious Comfort Food)
    {
        "id": "13_no_stress",
        "type": "broll",
        "broll": BROLL_FOOD,
        "broll_ss": 1.0,
        "raw_audio_ss": 193.00,
        "dur": 3.50,
        "desc": "BECAUSE NO STRESS!"
    },
    # 40.5s - 46.1s: Even women! Scientifically hair gets curlier (B-Roll Couple Romance)
    {
        "id": "14_women_curls",
        "type": "broll",
        "broll": BROLL_COUPLE,
        "broll_ss": 10.0,
        "raw_audio_ss": 197.90,
        "dur": 5.60,
        "desc": "Even women! Scientifically hair gets healthier and curlier!"
    },
    # 46.1s - 48.6s: Aspirational Clean Loop Ending (B-Roll Sunrise + Kinetic 3-Line Title)
    {
        "id": "15_loop_ending",
        "type": "broll",
        "broll": BROLL_SUNRISE,
        "broll_ss": 7.0,
        "dur": 2.50,
        "desc": "Aspirational Loop Ending"
    }
]

TOTAL_DURATION = sum(c["dur"] for c in CUTS)
print(f"🎬 Scheduled Cuts: {len(CUTS)} | Total Timeline Duration: {TOTAL_DURATION:.2f}s")

def render_video_tracks():
    print("\n--- RENDERING VIDEO CUTS ---")
    concat_list = WORKSPACE / "ref5_video_cuts.txt"
    rendered_files = []
    
    with open(concat_list, "w") as f_out:
        for idx, cut in enumerate(CUTS):
            cut_mp4 = WORKSPACE / f"ref5_cut_{idx:02d}.mp4"
            rendered_files.append(cut_mp4)
            dur = cut["dur"]
            
            if cut["type"] == "black":
                # Solid Jet Black #0A0A0A screen
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
                # Selective Color / B&W Beat with vintage film grain
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
            print(f"  [{idx+1}/{len(CUTS)}] Rendered {cut['id']} ({dur:.2f}s)")
            
    # Concat all video cuts
    master_video = WORKSPACE / "ref5_assembled_video.mp4"
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "copy", str(master_video)
    ]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Video track assembled: {master_video}")
    return master_video

def render_pro_audio():
    print("\n--- MASTERING AUDIO & SFX ---")
    # 1. Extract and join dialogue slices
    dialogue_cuts = []
    for idx, cut in enumerate(CUTS):
        out_wav = WORKSPACE / f"ref5_audio_{idx:02d}.wav"
        dur = cut["dur"]
        
        if cut["type"] == "black" or cut["id"] == "15_loop_ending":
            # Generate silence for pause and ending
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={dur:.3f}",
                "-c:a", "pcm_s16le", str(out_wav)
            ]
        elif "raw_ss" in cut:
            cmd = [
                "ffmpeg", "-y", "-accurate_seek", "-ss", f"{cut['raw_ss']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(out_wav)
            ]
        elif "raw_audio_ss" in cut:
            cmd = [
                "ffmpeg", "-y", "-accurate_seek", "-ss", f"{cut['raw_audio_ss']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(out_wav)
            ]
            
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dialogue_cuts.append(out_wav)
        
    concat_audio_txt = WORKSPACE / "ref5_audio_concat.txt"
    with open(concat_audio_txt, "w") as f:
        for wav in dialogue_cuts:
            f.write(f"file '{wav.name}'\n")
            
    raw_dialogue = WORKSPACE / "ref5_raw_dialogue.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_audio_txt),
        "-c:a", "pcm_s16le", str(raw_dialogue)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Synchronize SFX triggers
    # Trigger Timestamps:
    # 0.0s: Hit SFX (Hook start)
    # 2.9s: Whoosh SFX (Cut to broll)
    # 16.0s: Pop SFX (Dopamine sticker)
    # 18.5s: Pop SFX (Oxytocin sticker)
    # 21.5s: Pop SFX (Serotonin sticker)
    # 32.9s: Riser SFX (Black pause)
    # 37.0s: Hit SFX (Punchline "No Stress!")
    
    sfx_filter = (
        f"[1:a]asplit=2[hit_a][hit_b];"
        f"[3:a]asplit=3[pop_a][pop_b][pop_c];"
        f"[hit_a]adelay=0|0,volume=0.9[sfx_hit0];"
        f"[2:a]adelay=2900|2900,volume=0.8[sfx_w1];"
        f"[pop_a]adelay=16000|16000,volume=0.85[sfx_pop1];"
        f"[pop_b]adelay=18500|18500,volume=0.85[sfx_pop2];"
        f"[pop_c]adelay=21500|21500,volume=0.85[sfx_pop3];"
        f"[4:a]adelay=32900|32900,volume=0.9[sfx_rise];"
        f"[hit_b]adelay=37000|37000,volume=1.0[sfx_hit1];"
        f"[sfx_hit0][sfx_w1][sfx_pop1][sfx_pop2][sfx_pop3][sfx_rise][sfx_hit1]amix=inputs=7:normalize=0[all_sfx]"
    )
    sfx_track = WORKSPACE / "ref5_sfx_track.wav"
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
    
    # 3. Final Master Audio (-14 LUFS, Ducked BGM at -23dB)
    pro_audio = WORKSPACE / "ref5_master_pro_audio.wav"
    master_filter = (
        f"[1:a]volume=0.07,aloop=loop=-1:size=2e+09,afade=t=in:st=0:d=1.5,afade=t=out:st={TOTAL_DURATION-2.0}:d=2.0[bgm];"
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
    
    print(f"✅ Pro Audio Engineered (-14 LUFS): {pro_audio}")
    return pro_audio

def render_typography_and_stickers_overlay():
    print("\n--- GENERATING FRAME-BY-FRAME TYPOGRAPHY & STICKERS OVERLAY ---")
    overlay_mov = WORKSPACE / "ref5_overlay_track.mov"
    
    # Load fonts
    f_title_setup = ImageFont.truetype(FONT_SANS_REG, 52)
    f_title_hero = ImageFont.truetype(FONT_SERIF_ITALIC, 110)
    f_title_allcaps = ImageFont.truetype(FONT_SERIF_REG, 64)
    f_box_text = ImageFont.truetype(FONT_SANS_REG, 48)
    f_sub = ImageFont.truetype(FONT_SUB, 50)
    
    # Load stickers
    sticker_dopamine = Image.open(STICKERS_DIR / "sticker_dopamine.png").convert("RGBA")
    sticker_oxytocin = Image.open(STICKERS_DIR / "sticker_oxytocin.png").convert("RGBA")
    sticker_serotonin = Image.open(STICKERS_DIR / "sticker_serotonin.png").convert("RGBA")
    sticker_no_stress = Image.open(STICKERS_DIR / "sticker_no_stress.png").convert("RGBA")
    
    total_frames = int(TOTAL_DURATION * FPS)
    
    # Subtitle timeline schedule (t_start, t_end, text, style)
    # style: "tier_b" (conversational boxed), "tier_a" (kinetic title), "box_punch" (yellow box)
    SCHEDULE = [
        # 0.0 - 2.9: Kinetic Title Hook
        (0.0, 2.9, ("MODERN LOVE OR", "Modern Confusion?"), "kinetic_hook"),
        # 2.9 - 5.1: Situationship is not love
        (2.9, 5.1, "SITUATIONSHIP IS NOT LOVE", "yellow_box"),
        # 5.1 - 8.1: Question
        (5.1, 8.1, "what is the meaning of it?", "tier_b"),
        # 8.1 - 11.0: Extreme attraction
        (8.1, 11.0, ("EXTREME STAGE OF", "Attraction ❤️"), "kinetic_attraction"),
        # 11.0 - 13.1: Infatuation
        (11.0, 13.1, "EXTREME INFATUATION", "yellow_box"),
        # 13.1 - 16.0: Chemical feeling
        (13.1, 16.0, "love is basically a chemical feeling", "tier_b"),
        # 16.0 - 18.5: Dopamine
        (16.0, 18.5, "the rush of dopamine ⚡", "sticker_dopamine"),
        # 18.5 - 21.5: Oxytocin
        (18.5, 21.5, "the rush of oxytocin ❤️", "sticker_oxytocin"),
        # 21.5 - 25.9: Serotonin
        (21.5, 25.9, "serotonin is the sleep hormone", "sticker_serotonin"),
        # 25.9 - 32.9: Sleep well
        (25.9, 32.9, "when you are in love, you sleep well", "tier_b"),
        # 32.9 - 33.9: Solid Jet Black pause (no graphic)
        (32.9, 33.9, "", "none"),
        # 33.9 - 37.0: Weight question
        (33.9, 37.0, "men in happy relationships put on weight...", "tier_b"),
        # 37.0 - 40.5: Punchline: NO STRESS!
        (37.0, 40.5, "BECAUSE NO STRESS!", "punch_no_stress"),
        # 40.5 - 46.1: Woman curls
        (40.5, 46.1, "scientifically, a woman's hair gets healthier", "tier_b"),
        # 46.1 - 48.6: Clean Loop Ending
        (46.1, 48.6, ("REAL LOVE IS", "Peace of Mind", "ZERO STRESS"), "loop_ending")
    ]
    
    pipe = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS),
        "-i", "-", "-c:v", "png", "-r", str(FPS), str(overlay_mov)
    ], stdin=subprocess.PIPE)
    
    empty_frame = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0)).tobytes()
    
    for frame_idx in range(total_frames):
        t = frame_idx / float(FPS)
        
        # Find active event
        active_event = None
        for (st, et, data, style) in SCHEDULE:
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
            # Tier A: White Sans setup + Huge Yellow Serif Italic hero
            setup_txt, hero_txt = data
            bb1 = draw.textbbox((0, 0), setup_txt, font=f_title_setup)
            w1 = bb1[2] - bb1[0]
            draw.text(((WIDTH - w1)//2 + 3, 383), setup_txt, font=f_title_setup, fill=COLOR_SHADOW)
            draw.text(((WIDTH - w1)//2, 380), setup_txt, font=f_title_setup, fill=COLOR_WHITE)
            
            bb2 = draw.textbbox((0, 0), hero_txt, font=f_title_hero)
            w2 = bb2[2] - bb2[0]
            draw.text(((WIDTH - w2)//2 + 4, 454), hero_txt, font=f_title_hero, fill=COLOR_SHADOW)
            draw.text(((WIDTH - w2)//2, 450), hero_txt, font=f_title_hero, fill=COLOR_YELLOW)
            
        elif style == "yellow_box":
            # Solid Bright Yellow box with Jet Black text
            box_txt = data
            bb = draw.textbbox((0, 0), box_txt, font=f_box_text)
            bw = bb[2] - bb[0]
            bh = bb[3] - bb[1]
            bx = (WIDTH - bw) // 2
            by = 480
            draw.rounded_rectangle([bx - 26, by - 16, bx + bw + 26, by + bh + 16], radius=12, fill=COLOR_SHADOW)
            draw.rounded_rectangle([bx - 24, by - 14, bx + bw + 24, by + bh + 14], radius=12, fill=COLOR_YELLOW)
            draw.text((bx, by - 4), box_txt, font=f_box_text, fill=COLOR_BLACK)
            
        elif style == "kinetic_attraction":
            setup_txt, hero_txt = data
            bb1 = draw.textbbox((0, 0), setup_txt, font=f_title_setup)
            w1 = bb1[2] - bb1[0]
            draw.text(((WIDTH - w1)//2 + 3, 383), setup_txt, font=f_title_setup, fill=COLOR_SHADOW)
            draw.text(((WIDTH - w1)//2, 380), setup_txt, font=f_title_setup, fill=COLOR_WHITE)
            
            bb2 = draw.textbbox((0, 0), hero_txt, font=f_title_hero)
            w2 = bb2[2] - bb2[0]
            draw.text(((WIDTH - w2)//2 + 4, 454), hero_txt, font=f_title_hero, fill=COLOR_SHADOW)
            draw.text(((WIDTH - w2)//2, 450), hero_txt, font=f_title_hero, fill=COLOR_YELLOW)
            
        elif style == "tier_b":
            # Tier B: Standard Boxed Conversational Subtitles (lower third)
            sub_txt = data
            bb = draw.textbbox((0, 0), sub_txt, font=f_sub)
            sw = bb[2] - bb[0]
            sh = bb[3] - bb[1]
            sx = (WIDTH - sw) // 2
            sy = 1450
            draw.rounded_rectangle([sx - 20, sy - 12, sx + sw + 20, sy + sh + 14], radius=8, fill=COLOR_BLACK)
            draw.text((sx, sy - 3), sub_txt, font=f_sub, fill=COLOR_WHITE)
            
        elif style == "sticker_dopamine":
            # Boxed subtitle + floating Dopamine 3D sticker
            sub_txt = data
            bb = draw.textbbox((0, 0), sub_txt, font=f_sub)
            sw = bb[2] - bb[0]
            sh = bb[3] - bb[1]
            sx = (WIDTH - sw) // 2
            sy = 1450
            draw.rounded_rectangle([sx - 20, sy - 12, sx + sw + 20, sy + sh + 14], radius=8, fill=COLOR_BLACK)
            draw.text((sx, sy - 3), sub_txt, font=f_sub, fill=COLOR_WHITE)
            
            # Place sticker upper center
            im.alpha_composite(sticker_dopamine, dest=((WIDTH - sticker_dopamine.width)//2, 450))
            
        elif style == "sticker_oxytocin":
            sub_txt = data
            bb = draw.textbbox((0, 0), sub_txt, font=f_sub)
            sw = bb[2] - bb[0]
            sh = bb[3] - bb[1]
            sx = (WIDTH - sw) // 2
            sy = 1450
            draw.rounded_rectangle([sx - 20, sy - 12, sx + sw + 20, sy + sh + 14], radius=8, fill=COLOR_BLACK)
            draw.text((sx, sy - 3), sub_txt, font=f_sub, fill=COLOR_WHITE)
            
            im.alpha_composite(sticker_oxytocin, dest=((WIDTH - sticker_oxytocin.width)//2, 450))
            
        elif style == "sticker_serotonin":
            sub_txt = data
            bb = draw.textbbox((0, 0), sub_txt, font=f_sub)
            sw = bb[2] - bb[0]
            sh = bb[3] - bb[1]
            sx = (WIDTH - sw) // 2
            sy = 1450
            draw.rounded_rectangle([sx - 20, sy - 12, sx + sw + 20, sy + sh + 14], radius=8, fill=COLOR_BLACK)
            draw.text((sx, sy - 3), sub_txt, font=f_sub, fill=COLOR_WHITE)
            
            im.alpha_composite(sticker_serotonin, dest=((WIDTH - sticker_serotonin.width)//2, 450))
            
        elif style == "punch_no_stress":
            # Stamp sticker_no_stress at center
            im.alpha_composite(sticker_no_stress, dest=((WIDTH - sticker_no_stress.width)//2, 550))
            
            # Lower third highlight box
            punch_txt = "BECAUSE NO STRESS!"
            bb = draw.textbbox((0, 0), punch_txt, font=f_box_text)
            bw = bb[2] - bb[0]
            bh = bb[3] - bb[1]
            bx = (WIDTH - bw) // 2
            by = 1450
            draw.rounded_rectangle([bx - 26, by - 16, bx + bw + 26, by + bh + 16], radius=12, fill=COLOR_SHADOW)
            draw.rounded_rectangle([bx - 24, by - 14, bx + bw + 24, by + bh + 14], radius=12, fill=COLOR_YELLOW)
            draw.text((bx, by - 4), punch_txt, font=f_box_text, fill=COLOR_BLACK)
            
        elif style == "loop_ending":
            # 3-Line Kinetic Title: White Sans + Huge Yellow Serif + White Serif All-Caps
            line1, line2, line3 = data
            
            # Line 1: White Sans
            bb1 = draw.textbbox((0, 0), line1, font=f_title_setup)
            w1 = bb1[2] - bb1[0]
            draw.text(((WIDTH - w1)//2 + 3, 403), line1, font=f_title_setup, fill=COLOR_SHADOW)
            draw.text(((WIDTH - w1)//2, 400), line1, font=f_title_setup, fill=COLOR_WHITE)
            
            # Line 2: Huge Yellow Serif Italic
            bb2 = draw.textbbox((0, 0), line2, font=f_title_hero)
            w2 = bb2[2] - bb2[0]
            draw.text(((WIDTH - w2)//2 + 4, 484), line2, font=f_title_hero, fill=COLOR_SHADOW)
            draw.text(((WIDTH - w2)//2, 480), line2, font=f_title_hero, fill=COLOR_YELLOW)
            
            # Line 3: White Serif All-Caps
            bb3 = draw.textbbox((0, 0), line3, font=f_title_allcaps)
            w3 = bb3[2] - bb3[0]
            draw.text(((WIDTH - w3)//2 + 3, 623), line3, font=f_title_allcaps, fill=COLOR_SHADOW)
            draw.text(((WIDTH - w3)//2, 620), line3, font=f_title_allcaps, fill=COLOR_WHITE)
            
        pipe.stdin.write(im.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    print(f"✅ Typography & Graphics Overlay Track Generated: {overlay_mov}")
    return overlay_mov

def composite_master(master_video, overlay_mov, pro_audio):
    out_mp4 = EXPORT_DIR / "Reel_IMG_4246_Ref5_Style.mp4"
    print(f"\n🎬 COMPOSITING FINAL MASTER REEL IN STRICT BT.709...")
    print(f"Master Export: {out_mp4}")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(master_video),
        "-i", str(overlay_mov),
        "-i", str(pro_audio),
        "-filter_complex",
        f"[0:v][1:v]overlay=0:0:shortest=1,{SDR_FILTER}[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-color_range", "tv",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "256k", "-shortest",
        str(out_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"🎉 MASTER REEL COMPLETED & DELIVERED: {out_mp4}")
    
    # Extract Verification QA Frames
    qa_checkpoints = [
        (1.5, "qa_ref5_hook_kinetic"),
        (3.8, "qa_ref5_yellow_box"),
        (6.5, "qa_ref5_selective_bw_beat"),
        (17.5, "qa_ref5_sticker_dopamine"),
        (20.0, "qa_ref5_sticker_oxytocin"),
        (23.5, "qa_ref5_sticker_serotonin"),
        (29.0, "qa_ref5_sleep_broll_subs"),
        (33.5, "qa_ref5_jet_black_pause"),
        (38.5, "qa_ref5_punchline_no_stress"),
        (47.5, "qa_ref5_clean_loop_ending")
    ]
    
    print("\n📸 Extracting QA Verification Frames...")
    for snap_t, lbl in qa_checkpoints:
        frame_out = FRAMES_DIR / f"{lbl}.png"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{snap_t:.1f}", "-i", str(out_mp4),
            "-vframes", "1", str(frame_out)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  Captured {frame_out.name} at t={snap_t:.1f}s")
        
    return out_mp4

def main():
    t_start = time.time()
    print("=" * 70)
    print("🚀 RENDERING MASTER INSTAGRAM REEL IN REF5 STYLE FROM IMG_4246.MOV")
    print("=" * 70)
    
    v_track = render_video_tracks()
    a_track = render_pro_audio()
    o_track = render_typography_and_stickers_overlay()
    master = composite_master(v_track, o_track, a_track)
    
    t_elapsed = time.time() - t_start
    print("=" * 70)
    print(f"🎉 PRODUCTION COMPLETED IN {t_elapsed:.2f}s!")
    print(f"Master Deliverable: {master}")
    print("=" * 70)

if __name__ == "__main__":
    main()
