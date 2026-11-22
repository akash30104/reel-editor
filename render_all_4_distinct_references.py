#!/usr/bin/env python3
"""
Master Distinct Multi-Reference Renderer for Reel 1:
Produces 4 completely different visual architectures matching references 1, 2, 3, and 4:

1. Reel_1_Reference_1_Style.mp4:
   - 16:9 Centered Letterbox (1080x810 at y=555). Clean black top and bottom bars.
   - Side-Aligned Two-Tier Subtitles: Positioned on the open side beside the speaker (Left when Guest on right; Right when Host on left).
   - Line 1: Crisp White (#FFFFFF). Line 2: Bold Electric Yellow (#FFE600) ALL CAPS punchline.
   - B-Roll: Lord Hanuman face, crown, eyes, and golden aura 100% visible and centered (no cut-off head).

2. Reel_1_Reference_2_Style.mp4 (Raj Shamani Style):
   - FULL-BLEED VERTICAL 9:16 (1080x1920). Zero black bars. Close-up vertical punch-in on speaker.
   - Dynamic Center Karaoke Subtitles (y=1250): Solid White inactive words + Neon Yellow/Green active word highlight.

3. Reel_1_Reference_3_Style (Kisthenics Style):
   - 2.35:1 Anamorphic Cinematic Film Scope (1080x460 at y=730). Deep cinematic black bars top (0-730) and bottom (1190-1920).
   - Filmic letterbox typography with quotation marks ("ஹனுமான் பலம்...!", "YOU ARE LIKE HANUMAN!").

4. Reel_1_Reference_4_Style (Delta Weatherman / Split-Screen Podcast Style):
   - Dual-Speaker Split Screen: Host on top (1080x956), Guest on bottom (1080x956), separated by an 8px divider bar.
   - Both speakers visible simultaneously with center divider subtitles.
   - Opening 4.0s hook banner: "ராமாயணம் கற்றுத்தரும் வாழ்க்கை பாடம் 🏹".

All 4 master reels exported to /Users/pgi/Downloads/reels editor/export /
"""

import os
import sys
import subprocess
from pathlib import Path

import objc
from Cocoa import (
    NSBitmapImageRep, NSGraphicsContext, NSColor, NSRectFill, NSMakeRect,
    NSFont, NSAttributedString, NSMutableAttributedString,
    NSFontAttributeName, NSForegroundColorAttributeName,
    NSStrokeColorAttributeName, NSStrokeWidthAttributeName,
    NSDeviceRGBColorSpace
)
from PIL import Image

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
ASSETS_DIR = WORKSPACE / "assets"
BROLLS_DIR = ASSETS_DIR / "brolls"
AUDIO_DIR = ASSETS_DIR / "audio"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920

# Cuts Specification
CUTS = [
    {
        "st": 1988.0, "et": 1996.0, "speaker": "host", "broll": None,
        "ref1_subs": [
            (0.3, 3.8, "ராமாயணத்துல இருந்து...", "LIFE LESSON"),
            (4.0, 7.8, "நாம் என்ன பாடம்", "எடுத்துக்கணும்?")
        ],
        "karaoke_phrases": [
            (0.3, 3.8, "ராமாயணத்துல இருந்து..."),
            (4.0, 7.8, "நாம் என்ன வாழ்க்கை பாடம் எடுத்துக்கணும்?")
        ],
        "ref3_subs": [
            (0.3, 3.8, '"ராமாயணம் தரும் பாடம்..."'),
            (4.0, 7.8, '"நாம் என்ன கற்றுக்கொள்ள வேண்டும்?"')
        ]
    },
    {
        "st": 1996.0, "et": 2008.5, "speaker": "guest", "broll": None,
        "ref1_subs": [
            (0.3, 5.8, "நான் வந்து", "ஹனுமான பத்தி மட்டும்!"),
            (6.0, 12.2, "Everybody in this world...", "IS LIKE HANUMAN! 🏹")
        ],
        "karaoke_phrases": [
            (0.3, 5.8, "நான் வந்து ஹனுமான பத்தி மட்டும் பேச நினைக்கிறேன்!"),
            (6.0, 12.2, "Everybody in this world is like Hanuman!")
        ],
        "ref3_subs": [
            (0.3, 5.8, '"நான் பேச நினைப்பது ஹனுமான் பற்றி..."'),
            (6.0, 12.2, '"EVERYBODY IS LIKE HANUMAN!"')
        ]
    },
    {
        "st": 2008.5, "et": 2018.5, "speaker": "broll", "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"),
        "ref1_subs": [
            (0.3, 4.8, "நமக்குள்ள ஒளிஞ்சிருக்கு...", "LATENT POTENTIAL!"),
            (5.0, 9.8, "Someone has to show it...", "THAT'S THE MENTOR!")
        ],
        "karaoke_phrases": [
            (0.3, 4.8, "நமக்குள்ள Latent potential ஒளிஞ்சிருக்கு..."),
            (5.0, 9.8, "But someone has to show it to us, that's the MENTOR!")
        ],
        "ref3_subs": [
            (0.3, 4.8, '"நமக்குள்ளே உறங்கும் அளப்பரிய சக்தி..."'),
            (5.0, 9.8, '"THE POWER OF A TRUE MENTOR"')
        ]
    },
    {
        "st": 2018.5, "et": 2035.0, "speaker": "guest", "broll": None,
        "ref1_subs": [
            (0.3, 7.8, "ஜாம்பவான் நினைவுபடுத்தும் போது...", "JAMBAVAN'S ROLE"),
            (8.0, 16.2, "ஹனுமானுக்கே புரியுது...", "REAL INNER POWER! 🔥")
        ],
        "karaoke_phrases": [
            (0.3, 7.8, "ஜாம்பவான் வந்து நினைவுபடுத்தும் போது தான்..."),
            (8.0, 16.2, "ஹனுமானுக்கே தன்னுடைய உண்மையான பலம் புரியுது!")
        ],
        "ref3_subs": [
            (0.3, 7.8, '"ஜாம்பவான் வழிகாட்டலில்..."'),
            (8.0, 16.2, '"அனுமன் உணர்ந்த தன்னிகரற்ற பலம்!"')
        ]
    },
    {
        "st": 2035.0, "et": 2048.0, "speaker": "broll", "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"),
        "ref1_subs": [
            (0.3, 6.0, "இன்னைக்கு பல பேர்கிட்ட இல்லாதது...", "WHAT WE LACK TODAY"),
            (6.2, 12.8, "Unconditional...", "LOYALTY & DEDICATION!")
        ],
        "karaoke_phrases": [
            (0.3, 6.0, "இன்னைக்கு பல பேர்கிட்ட இல்லாதது என்னன்னா..."),
            (6.2, 12.8, "Unconditional Loyalty and Dedication!")
        ],
        "ref3_subs": [
            (0.3, 6.0, '"இன்று பலரிடமும் மறைந்துபோன ஒன்று..."'),
            (6.2, 12.8, '"UNCONDITIONAL LOYALTY"')
        ]
    },
    {
        "st": 2048.0, "et": 2062.0, "speaker": "guest", "broll": None,
        "ref1_subs": [
            (0.3, 6.5, "ஹனுமான் காட்டிய விசுவாசம் தான்...", "SELFLESS DEVOTION"),
            (6.8, 13.8, "வாழ்க்கையின் மிகப்பெரிய பாடம்!", "GREATEST LESSON OF LIFE! 🏹")
        ],
        "karaoke_phrases": [
            (0.3, 6.5, "ஹனுமான் காட்டிய அந்த தன்னலமற்ற விசுவாசம் தான்..."),
            (6.8, 13.8, "வாழ்க்கையின் மிகப்பெரிய பாடம்! 🏹")
        ],
        "ref3_subs": [
            (0.3, 6.5, '"தன்னலமற்ற விசுவாசத்தின் வெளிப்பாடு..."'),
            (6.8, 13.8, '"வாழ்க்கையின் மிக உன்னத பாடம்! 🏹"')
        ]
    }
]

total_dur = sum(c["et"] - c["st"] for c in CUTS)

# Studio Mixed Audio: Demucs Vocals + Ducked Flute BGM (-14.5 LUFS)
demucs_vocals = WORKSPACE / "demucs_run_1" / "htdemucs" / "temp_raw_audio_1" / "vocals.wav"
bgm_file = AUDIO_DIR / "ramayan_flute_bgm.mp3"
mixed_audio = WORKSPACE / "master_distinct_audio.wav"

cmd_audio = [
    "ffmpeg", "-y",
    "-i", str(demucs_vocals),
    "-stream_loop", "-1", "-i", str(bgm_file),
    "-filter_complex",
    "[0:a]highpass=f=80,equalizer=f=280:t=q:w=1.5:g=-3.0,equalizer=f=3200:t=q:w=1.2:g=+3.5,equalizer=f=8000:t=q:w=1.0:g=+2.0,compand=attacks=0.02:decays=0.15:points=-60/-60|-24/-12|0/-3:soft-knee=6[vocal_clean];"
    "[1:a]volume=0.045[bgm_soft];"
    "[vocal_clean][bgm_soft]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14.5:TP=-1.5:LRA=4[out]",
    "-map", "[out]",
    str(mixed_audio)
]
subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# =============================================================
# 1. RENDER REFERENCE 1 (16:9 Letterbox + Side Subtitles)
# =============================================================
def render_style_1():
    print("\n🎬 RENDERING REEL 1 IN REFERENCE 1 STYLE:")
    print("   -> 16:9 Letterbox (1080x810) + Side Subtitles Beside Speaker + Uncropped Hanuman Face")
    
    vid_h = 810
    vid_y = (HEIGHT - vid_h) // 2  # 555
    subs_h = 240
    subs_y = vid_y + vid_h - subs_h - 30  # 1095
    
    cut_files = []
    concat_list = WORKSPACE / "style1_concat.txt"
    for idx, cut in enumerate(CUTS):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"style1_cut_{idx}.mp4"
        cut_files.append(out_cut)
        if cut["broll"]:
            # Hanuman B-roll scaled to 1080x810
            vf = "scale=1080:810,setsar=1,fps=30"
            cmd = ["ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}", "-stream_loop", "-1", "-i", cut["broll"], "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        else:
            crop = "crop=2160:1620:190:320,scale=1080:810:flags=lanczos" if cut["speaker"] == "host" else "crop=2160:1620:1530:320,scale=1080:810:flags=lanczos"
            cmd = ["ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}", "-i", str(RAW_VIDEO), "-vf", f"{crop},setsar=1,fps=30", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    with open(concat_list, "w") as f:
        for cf in cut_files: f.write(f"file '{cf}'\n")
        
    base_vid = WORKSPACE / "style1_base.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-vf", f"pad={WIDTH}:{HEIGHT}:0:{vid_y}:color=black",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_vid)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Subtitles: Side-aligned
    def render_side_frame(l1, l2, align):
        rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
            None, WIDTH, subs_h, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
        )
        ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
        NSGraphicsContext.setCurrentContext_(ctx)
        NSColor.clearColor().set()
        NSRectFill(NSMakeRect(0, 0, WIDTH, subs_h))
        if not l1 and not l2:
            ctx.flushGraphics()
            return bytes(rep.bitmapData()[0:rep.bytesPerRow() * subs_h])
            
        f1 = NSFont.fontWithName_size_("TamilSangamMN-Bold", 40.0) or NSFont.boldSystemFontOfSize_(40.0)
        f2 = NSFont.fontWithName_size_("Futura-Bold", 54.0) or NSFont.fontWithName_size_("TamilSangamMN-Bold", 50.0) or NSFont.boldSystemFontOfSize_(50.0)
        c_white = NSColor.whiteColor()
        c_yellow = NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 0.90, 0.0, 1.0)
        c_black = NSColor.blackColor()
        
        a1_s = NSAttributedString.alloc().initWithString_attributes_(l1, {NSFontAttributeName: f1, NSForegroundColorAttributeName: c_black, NSStrokeColorAttributeName: c_black, NSStrokeWidthAttributeName: 7.0})
        a1_f = NSAttributedString.alloc().initWithString_attributes_(l1, {NSFontAttributeName: f1, NSForegroundColorAttributeName: c_white})
        a2_s = NSAttributedString.alloc().initWithString_attributes_(l2, {NSFontAttributeName: f2, NSForegroundColorAttributeName: c_black, NSStrokeColorAttributeName: c_black, NSStrokeWidthAttributeName: 8.0})
        a2_f = NSAttributedString.alloc().initWithString_attributes_(l2, {NSFontAttributeName: f2, NSForegroundColorAttributeName: c_yellow})
        
        sz1 = a1_f.size()
        sz2 = a2_f.size()
        if align == "left":
            x1, x2 = 70.0, 70.0
        elif align == "right":
            x1, x2 = WIDTH - sz1.width - 70.0, WIDTH - sz2.width - 70.0
        else:
            x1, x2 = (WIDTH - sz1.width) / 2, (WIDTH - sz2.width) / 2
            
        y1, y2 = subs_h - 90, subs_h - 175
        a1_s.drawAtPoint_((x1, y1))
        a1_f.drawAtPoint_((x1, y1))
        a2_s.drawAtPoint_((x2, y2))
        a2_f.drawAtPoint_((x2, y2))
        ctx.flushGraphics()
        return bytes(rep.bitmapData()[0:rep.bytesPerRow() * subs_h])

    sub_events = []
    curr_t = 0.0
    for cut in CUTS:
        al = "right" if cut["speaker"] == "host" else "left"
        for pst, pet, l1, l2 in cut["ref1_subs"]:
            sub_events.append((curr_t + pst, curr_t + pet, l1, l2, al))
        curr_t += (cut["et"] - cut["st"])

    subs_mov = WORKSPACE / "style1_subs.mov"
    proc = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{subs_h}", "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_f = int(round(total_dur * 30))
    blank = render_side_frame("", "", "left")
    for f_idx in range(total_f):
        t_sec = f_idx / 30.0
        active_ev = None
        for w_st, w_et, l1, l2, al in sub_events:
            if w_st <= t_sec < w_et:
                active_ev = (l1, l2, al)
                break
        raw = render_side_frame(active_ev[0], active_ev[1], active_ev[2]) if active_ev else blank
        proc.stdin.write(raw)
    proc.stdin.close()
    proc.wait()

    final_out = EXPORT_DIR / "Reel_1_Reference_1_Style.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(base_vid), "-i", str(subs_mov), "-i", str(mixed_audio),
        "-filter_complex", f"[0:v][1:v]overlay=0:{subs_y}[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest",
        str(final_out)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref1_t10s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-ss", "15.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref1_hanuman_t15s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✅ Completed: {final_out.name}")

# =============================================================
# 2. RENDER REFERENCE 2 (Full-Bleed Vertical 9:16 + Raj Shamani Center Karaoke)
# =============================================================
def render_style_2():
    print("\n🎬 RENDERING REEL 1 IN REFERENCE 2 STYLE:")
    print("   -> FULL-BLEED 9:16 VERTICAL (No black bars!) + Close-Up Speaker Punch-in + Center Karaoke")
    
    cut_files = []
    concat_list = WORKSPACE / "style2_concat.txt"
    for idx, cut in enumerate(CUTS):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"style2_cut_{idx}.mp4"
        cut_files.append(out_cut)
        if cut["broll"]:
            # Hanuman vertical 9:16 crop with face in upper third
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:0:150,setsar=1,fps=30"
            cmd = ["ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}", "-stream_loop", "-1", "-i", cut["broll"], "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        else:
            # Full 9:16 vertical punch-in directly on speaker
            crop = "crop=1080:1920:730:190,scale=1080:1920:flags=lanczos" if cut["speaker"] == "host" else "crop=1080:1920:2070:190,scale=1080:1920:flags=lanczos"
            cmd = ["ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}", "-i", str(RAW_VIDEO), "-vf", f"{crop},setsar=1,fps=30", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(concat_list, "w") as f:
        for cf in cut_files: f.write(f"file '{cf}'\n")

    base_vid = WORKSPACE / "style2_base.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_vid)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Karaoke Subtitles
    subs_h = 240
    def render_karaoke_frame(words_status):
        rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
            None, WIDTH, subs_h, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
        )
        ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
        NSGraphicsContext.setCurrentContext_(ctx)
        NSColor.clearColor().set()
        NSRectFill(NSMakeRect(0, 0, WIDTH, subs_h))
        if not words_status:
            ctx.flushGraphics()
            return bytes(rep.bitmapData()[0:rep.bytesPerRow() * subs_h])
            
        font = NSFont.fontWithName_size_("TamilSangamMN-Bold", 50.0) or NSFont.boldSystemFontOfSize_(50.0)
        c_white = NSColor.whiteColor()
        c_yellow = NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 0.90, 0.0, 1.0)
        c_black = NSColor.blackColor()
        
        s_astr = NSMutableAttributedString.alloc().init()
        for w, _ in words_status:
            astr = NSAttributedString.alloc().initWithString_attributes_(w + " ", {NSFontAttributeName: font, NSForegroundColorAttributeName: c_black, NSStrokeColorAttributeName: c_black, NSStrokeWidthAttributeName: 8.0})
            s_astr.appendAttributedString_(astr)
            
        f_astr = NSMutableAttributedString.alloc().init()
        for w, is_act in words_status:
            c = c_yellow if is_act else c_white
            astr = NSAttributedString.alloc().initWithString_attributes_(w + " ", {NSFontAttributeName: font, NSForegroundColorAttributeName: c})
            f_astr.appendAttributedString_(astr)
            
        sz = f_astr.size()
        x = (WIDTH - sz.width) / 2
        y = (subs_h - sz.height) / 2
        s_astr.drawAtPoint_((x, y))
        f_astr.drawAtPoint_((x, y))
        ctx.flushGraphics()
        return bytes(rep.bitmapData()[0:rep.bytesPerRow() * subs_h])

    sub_events = []
    curr_t = 0.0
    for cut in CUTS:
        for pst, pet, phrase in cut["karaoke_phrases"]:
            words = phrase.split()
            w_dur = (pet - pst) / max(len(words), 1)
            for w_idx in range(len(words)):
                sub_events.append((curr_t + pst + (w_idx * w_dur), curr_t + pst + ((w_idx + 1) * w_dur), phrase, w_idx))
        curr_t += (cut["et"] - cut["st"])

    subs_mov = WORKSPACE / "style2_subs.mov"
    proc = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{subs_h}", "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_f = int(round(total_dur * 30))
    blank = render_karaoke_frame([])
    for f_idx in range(total_f):
        t_sec = f_idx / 30.0
        active_ev = None
        for w_st, w_et, phr, w_i in sub_events:
            if w_st <= t_sec < w_et:
                active_ev = (phr, w_i)
                break
        if active_ev:
            words = active_ev[0].split()
            status = [(w, i == active_ev[1]) for i, w in enumerate(words)]
            raw = render_karaoke_frame(status)
        else:
            raw = blank
        proc.stdin.write(raw)
    proc.stdin.close()
    proc.wait()

    final_out = EXPORT_DIR / "Reel_1_Reference_2_Style.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(base_vid), "-i", str(subs_mov), "-i", str(mixed_audio),
        "-filter_complex", "[0:v][1:v]overlay=0:1280[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest",
        str(final_out)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref2_t10s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✅ Completed: {final_out.name}")

# =============================================================
# 3. RENDER REFERENCE 3 (2.35:1 Anamorphic Cinema Scope)
# =============================================================
def render_style_3():
    print("\n🎬 RENDERING REEL 1 IN REFERENCE 3 STYLE:")
    print("   -> 2.35:1 ANAMORPHIC CINEMA SCOPE (1080x460 at y=730) + Deep Black Letterbox + Film Typography")
    
    vid_h = 460
    vid_y = (HEIGHT - vid_h) // 2  # 730
    
    cut_files = []
    concat_list = WORKSPACE / "style3_concat.txt"
    for idx, cut in enumerate(CUTS):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"style3_cut_{idx}.mp4"
        cut_files.append(out_cut)
        if cut["broll"]:
            vf = "scale=1080:460:force_original_aspect_ratio=increase,crop=1080:460,setsar=1,fps=30"
            cmd = ["ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}", "-stream_loop", "-1", "-i", cut["broll"], "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        else:
            # 2.35:1 Cinema scope crop
            crop = "crop=2800:1190:200:480,scale=1080:460:flags=lanczos" if cut["speaker"] == "host" else "crop=2800:1190:1000:480,scale=1080:460:flags=lanczos"
            cmd = ["ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}", "-i", str(RAW_VIDEO), "-vf", f"{crop},setsar=1,fps=30", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(concat_list, "w") as f:
        for cf in cut_files: f.write(f"file '{cf}'\n")

    base_vid = WORKSPACE / "style3_base.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-vf", f"pad={WIDTH}:{HEIGHT}:0:{vid_y}:color=black",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_vid)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Subtitles: Centered in the black bar below video (y = 1260)
    subs_h = 160
    subs_y = 1260
    def render_ref3_frame(quote_text):
        rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
            None, WIDTH, subs_h, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
        )
        ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
        NSGraphicsContext.setCurrentContext_(ctx)
        NSColor.clearColor().set()
        NSRectFill(NSMakeRect(0, 0, WIDTH, subs_h))
        if not quote_text:
            ctx.flushGraphics()
            return bytes(rep.bitmapData()[0:rep.bytesPerRow() * subs_h])

        f = NSFont.fontWithName_size_("TamilSangamMN-Bold", 46.0) or NSFont.boldSystemFontOfSize_(46.0)
        c_gold = NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 0.90, 0.3, 1.0)
        c_black = NSColor.blackColor()

        a_s = NSAttributedString.alloc().initWithString_attributes_(quote_text, {NSFontAttributeName: f, NSForegroundColorAttributeName: c_black, NSStrokeColorAttributeName: c_black, NSStrokeWidthAttributeName: 7.0})
        a_f = NSAttributedString.alloc().initWithString_attributes_(quote_text, {NSFontAttributeName: f, NSForegroundColorAttributeName: c_gold})

        sz = a_f.size()
        x = (WIDTH - sz.width) / 2
        y = (subs_h - sz.height) / 2
        a_s.drawAtPoint_((x, y))
        a_f.drawAtPoint_((x, y))
        ctx.flushGraphics()
        return bytes(rep.bitmapData()[0:rep.bytesPerRow() * subs_h])

    sub_events = []
    curr_t = 0.0
    for cut in CUTS:
        for pst, pet, txt in cut["ref3_subs"]:
            sub_events.append((curr_t + pst, curr_t + pet, txt))
        curr_t += (cut["et"] - cut["st"])

    subs_mov = WORKSPACE / "style3_subs.mov"
    proc = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{subs_h}", "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_f = int(round(total_dur * 30))
    blank = render_ref3_frame("")
    for f_idx in range(total_f):
        t_sec = f_idx / 30.0
        active_ev = None
        for w_st, w_et, txt in sub_events:
            if w_st <= t_sec < w_et:
                active_ev = txt
                break
        raw = render_ref3_frame(active_ev) if active_ev else blank
        proc.stdin.write(raw)
    proc.stdin.close()
    proc.wait()

    final_out = EXPORT_DIR / "Reel_1_Reference_3_Style.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(base_vid), "-i", str(subs_mov), "-i", str(mixed_audio),
        "-filter_complex", f"[0:v][1:v]overlay=0:{subs_y}[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest",
        str(final_out)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref3_t10s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✅ Completed: {final_out.name}")

# =============================================================
# 4. RENDER REFERENCE 4 (Dual-Speaker Split Screen Podcast)
# =============================================================
def render_style_4():
    print("\n🎬 RENDERING REEL 1 IN REFERENCE 4 STYLE:")
    print("   -> DUAL-SPEAKER SPLIT SCREEN (Host Top 1080x960 / Guest Bottom 1080x960) + Center Divider Subtitles")
    
    cut_files = []
    concat_list = WORKSPACE / "style4_concat.txt"
    for idx, cut in enumerate(CUTS):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"style4_cut_{idx}.mp4"
        cut_files.append(out_cut)
        if cut["broll"]:
            # Stack Host on top, Hanuman B-roll on bottom
            cmd = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}", "-i", str(RAW_VIDEO),
                "-ss", "0.0", "-t", f"{dur:.3f}", "-stream_loop", "-1", "-i", cut["broll"],
                "-filter_complex",
                "[0:v]crop=1920:1700:200:190,scale=1080:960:flags=lanczos,fps=30,setsar=1[top];"
                "[1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,fps=30,setsar=1[bot];"
                "[top][bot]vstack=inputs=2[stacked];"
                "[stacked]drawbox=x=0:y=956:w=1080:h=8:color=0xFFE600@1.0:t=fill[out]",
                "-map", "[out]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)
            ]
        else:
            # Stack Host on top (1080x960), Guest on bottom (1080x960) with 8px divider
            cmd = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}", "-i", str(RAW_VIDEO),
                "-filter_complex",
                "[0:v]crop=1920:1700:200:190,scale=1080:960:flags=lanczos,fps=30,setsar=1[top];"
                "[0:v]crop=1920:1700:1650:190,scale=1080:960:flags=lanczos,fps=30,setsar=1[bot];"
                "[top][bot]vstack=inputs=2[stacked];"
                "[stacked]drawbox=x=0:y=956:w=1080:h=8:color=0xFFE600@1.0:t=fill[out]",
                "-map", "[out]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(concat_list, "w") as f:
        for cf in cut_files: f.write(f"file '{cf}'\n")

    base_vid = WORKSPACE / "style4_base.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_vid)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Subtitles: Placed directly across the center divider line (y = 880 to 1040)
    subs_h = 180
    subs_y = 870
    def render_split_sub_frame(l1, l2):
        rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
            None, WIDTH, subs_h, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
        )
        ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
        NSGraphicsContext.setCurrentContext_(ctx)
        NSColor.clearColor().set()
        NSRectFill(NSMakeRect(0, 0, WIDTH, subs_h))
        if not l1 and not l2:
            ctx.flushGraphics()
            return bytes(rep.bitmapData()[0:rep.bytesPerRow() * subs_h])

        # Dark translucent pill banner behind text
        NSColor.colorWithDeviceRed_green_blue_alpha_(0.05, 0.05, 0.05, 0.88).set()
        NSRectFill(NSMakeRect(60, 20, WIDTH - 120, subs_h - 40))

        f1 = NSFont.fontWithName_size_("TamilSangamMN-Bold", 36.0) or NSFont.boldSystemFontOfSize_(36.0)
        f2 = NSFont.fontWithName_size_("Futura-Bold", 46.0) or NSFont.fontWithName_size_("TamilSangamMN-Bold", 44.0) or NSFont.boldSystemFontOfSize_(44.0)

        a1 = NSAttributedString.alloc().initWithString_attributes_(l1, {NSFontAttributeName: f1, NSForegroundColorAttributeName: NSColor.whiteColor()})
        a2 = NSAttributedString.alloc().initWithString_attributes_(l2, {NSFontAttributeName: f2, NSForegroundColorAttributeName: NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 0.9, 0.0, 1.0)})

        sz1 = a1.size()
        sz2 = a2.size()
        x1 = (WIDTH - sz1.width) / 2
        y1 = subs_h - 75
        x2 = (WIDTH - sz2.width) / 2
        y2 = subs_h - 135

        a1.drawAtPoint_((x1, y1))
        a2.drawAtPoint_((x2, y2))
        ctx.flushGraphics()
        return bytes(rep.bitmapData()[0:rep.bytesPerRow() * subs_h])

    sub_events = []
    curr_t = 0.0
    for cut in CUTS:
        for pst, pet, l1, l2 in cut["ref1_subs"]:
            sub_events.append((curr_t + pst, curr_t + pet, l1, l2))
        curr_t += (cut["et"] - cut["st"])

    subs_mov = WORKSPACE / "style4_subs.mov"
    proc = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{subs_h}", "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_f = int(round(total_dur * 30))
    blank = render_split_sub_frame("", "")
    for f_idx in range(total_f):
        t_sec = f_idx / 30.0
        active_ev = None
        for w_st, w_et, l1, l2 in sub_events:
            if w_st <= t_sec < w_et:
                active_ev = (l1, l2)
                break
        raw = render_split_sub_frame(active_ev[0], active_ev[1]) if active_ev else blank
        proc.stdin.write(raw)
    proc.stdin.close()
    proc.wait()

    # Opening 4s hook headline banner
    hook_banner = WORKSPACE / "style4_hook_banner.png"
    rep_b = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, WIDTH, 160, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
    )
    ctx_b = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep_b)
    NSGraphicsContext.setCurrentContext_(ctx_b)
    NSColor.colorWithDeviceRed_green_blue_alpha_(0.1, 0.1, 0.1, 0.90).set()
    NSRectFill(NSMakeRect(0, 0, WIDTH, 160))
    fb = NSFont.fontWithName_size_("TamilSangamMN-Bold", 42.0) or NSFont.boldSystemFontOfSize_(42.0)
    ab = NSAttributedString.alloc().initWithString_attributes_("ராமாயணம் கற்றுத்தரும் வாழ்க்கை பாடம் 🏹", {NSFontAttributeName: fb, NSForegroundColorAttributeName: NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 0.9, 0.0, 1.0)})
    sz_b = ab.size()
    ab.drawAtPoint_(((WIDTH - sz_b.width)/2, (160 - sz_b.height)/2))
    ctx_b.flushGraphics()
    png_d = rep_b.representationUsingType_properties_(4, None)
    png_d.writeToFile_atomically_(str(hook_banner), True)

    final_out = EXPORT_DIR / "Reel_1_Reference_4_Style.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(base_vid), "-loop", "1", "-i", str(hook_banner), "-i", str(subs_mov), "-i", str(mixed_audio),
        "-filter_complex",
        "[1:v]format=rgba,fade=t=out:st=3.5:d=0.5:alpha=1[banner_faded];"
        f"[0:v][banner_faded]overlay=0:120:enable='between(t,0,4.0)'[base_with_banner];"
        f"[base_with_banner][2:v]overlay=0:{subs_y}[v]",
        "-map", "[v]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest",
        str(final_out)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    subprocess.run(["ffmpeg", "-y", "-ss", "2.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref4_t2s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref4_t10s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✅ Completed: {final_out.name}")

def main():
    print("=" * 80)
    print("🚀 RENDERING 4 RADICALLY DISTINCT REFERENCE STYLES FOR REEL 1")
    print("=" * 80)
    render_style_1()
    render_style_2()
    render_style_3()
    render_style_4()
    print("\n" + "=" * 80)
    print("🎉 ALL 4 DISTINCT REFERENCE REELS COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()
