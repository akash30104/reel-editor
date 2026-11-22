#!/usr/bin/env python3
"""
Master Multi-Reference Renderer for Reel 1:
Generates all 4 distinct reference styles requested by the user:
1. Reel_1_Reference_1_Style.mp4: Minimalist letterbox + Side-aligned Two-Tier Subtitles (Line 1 White, Line 2 Electric Yellow) beside the speaker + Hanuman face centered.
2. Reel_1_Reference_2_Style.mp4: Full-bleed 9:16 vertical (Raj Shamani style) + dynamic word-by-word karaoke highlight.
3. Reel_1_Reference_3_Style.mp4: Cinematic letterbox + bold Tanglish/Tamil punchline typography (Kisthenics style).
4. Reel_1_Reference_4_Style.mp4: Editorial documentary style + hook header banner in opening 4s (Delta Weatherman style).
All exports saved to /Users/pgi/Downloads/reels editor/export /
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
VID_W = 1080
VID_H = 810
VID_Y = (HEIGHT - VID_H) // 2  # 555
SUBS_H = 240
SUBS_Y = VID_Y + VID_H - SUBS_H - 30  # 1095 (inside lower video)

# Crops for 4K -> 1080x810 (Letterboxed)
CROP_HOST_810 = "crop=2160:1620:190:320,scale=1080:810:flags=lanczos"
CROP_GUEST_810 = "crop=2160:1620:1530:320,scale=1080:810:flags=lanczos"

# Crops for 4K -> 1080x1920 (Full-Bleed Vertical 9:16)
CROP_HOST_916 = "crop=1080:1920:730:190,scale=1080:1920:flags=lanczos"
CROP_GUEST_916 = "crop=1080:1920:2070:190,scale=1080:1920:flags=lanczos"

CUTS_SPEC = [
    {
        "st": 1988.0, "et": 1996.0, "speaker": "host", "broll": None,
        "ref1_subtitles": [
            (0.3, 3.8, "ராமாயணத்துல இருந்து...", "LIFE LESSON"),
            (4.0, 7.8, "நாம் என்ன பாடம்", "எடுத்துக்கணும்?")
        ],
        "word_subtitles": [
            (0.3, 3.8, "ராமாயணத்துல இருந்து..."),
            (4.0, 7.8, "நாம் என்ன வாழ்க்கை பாடம் எடுத்துக்கணும்?")
        ]
    },
    {
        "st": 1996.0, "et": 2008.5, "speaker": "guest", "broll": None,
        "ref1_subtitles": [
            (0.3, 5.8, "நான் வந்து", "ஹனுமான பத்தி மட்டும்!"),
            (6.0, 12.2, "Everybody in this world...", "IS LIKE HANUMAN! 🏹")
        ],
        "word_subtitles": [
            (0.3, 5.8, "நான் வந்து ஹனுமான பத்தி மட்டும் பேச நினைக்கிறேன்!"),
            (6.0, 12.2, "Everybody in this world is like Hanuman!")
        ]
    },
    {
        "st": 2008.5, "et": 2018.5, "speaker": "broll", "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"),
        "ref1_subtitles": [
            (0.3, 4.8, "நமக்குள்ள ஒளிஞ்சிருக்கு...", "LATENT POTENTIAL!"),
            (5.0, 9.8, "Someone has to show it...", "THAT'S THE MENTOR!")
        ],
        "word_subtitles": [
            (0.3, 4.8, "நமக்குள்ள Latent potential ஒளிஞ்சிருக்கு..."),
            (5.0, 9.8, "But someone has to show it to us, that's the MENTOR!")
        ]
    },
    {
        "st": 2018.5, "et": 2035.0, "speaker": "guest", "broll": None,
        "ref1_subtitles": [
            (0.3, 7.8, "ஜாம்பவான் நினைவுபடுத்தும் போது...", "JAMBAVAN'S ROLE"),
            (8.0, 16.2, "ஹனுமானுக்கே புரியுது...", "REAL INNER POWER! 🔥")
        ],
        "word_subtitles": [
            (0.3, 7.8, "ஜாம்பவான் வந்து நினைவுபடுத்தும் போது தான்..."),
            (8.0, 16.2, "ஹனுமானுக்கே தன்னுடைய உண்மையான பலம் புரியுது!")
        ]
    },
    {
        "st": 2035.0, "et": 2048.0, "speaker": "broll", "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"),
        "ref1_subtitles": [
            (0.3, 6.0, "இன்னைக்கு பல பேர்கிட்ட இல்லாதது...", "WHAT WE LACK TODAY"),
            (6.2, 12.8, "Unconditional...", "LOYALTY & DEDICATION!")
        ],
        "word_subtitles": [
            (0.3, 6.0, "இன்னைக்கு பல பேர்கிட்ட இல்லாதது என்னன்னா..."),
            (6.2, 12.8, "Unconditional Loyalty and Dedication!")
        ]
    },
    {
        "st": 2048.0, "et": 2062.0, "speaker": "guest", "broll": None,
        "ref1_subtitles": [
            (0.3, 6.5, "ஹனுமான் காட்டிய விசுவாசம் தான்...", "SELFLESS DEVOTION"),
            (6.8, 13.8, "வாழ்க்கையின் மிகப்பெரிய பாடம்!", "GREATEST LESSON OF LIFE! 🏹")
        ],
        "word_subtitles": [
            (0.3, 6.5, "ஹனுமான் காட்டிய அந்த தன்னலமற்ற விசுவாசம் தான்..."),
            (6.8, 13.8, "வாழ்க்கையின் மிகப்பெரிய பாடம்! 🏹")
        ]
    }
]

total_dur = sum(c["et"] - c["st"] for c in CUTS_SPEC)

# Common Audio: Studio Demucs Vocals + Ducked Flute BGM (-14.5 LUFS)
demucs_vocals = WORKSPACE / "demucs_run_1" / "htdemucs" / "temp_raw_audio_1" / "vocals.wav"
bgm_file = AUDIO_DIR / "ramayan_flute_bgm.mp3"
mixed_audio = WORKSPACE / "master_ref_mixed_audio.wav"

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
print("🎙️ Studio Audio Track Ready (-14.5 LUFS)")

# -------------------------------------------------------------
# SUBTITLE RENDERERS
# -------------------------------------------------------------

def render_side_sub_frame(l1_text, l2_text, align="left", width=WIDTH, height=SUBS_H):
    """Reference 1: Side-positioned Two-Tier Subtitles (Line 1 White, Line 2 Electric Yellow)."""
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, width, height, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
    )
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.setCurrentContext_(ctx)
    NSColor.clearColor().set()
    NSRectFill(NSMakeRect(0, 0, width, height))

    if not l1_text and not l2_text:
        ctx.flushGraphics()
        return bytes(rep.bitmapData()[0:rep.bytesPerRow() * height])

    is_tamil_l1 = any(ord(c) > 0x0B80 and ord(c) < 0x0BFF for c in l1_text)
    is_tamil_l2 = any(ord(c) > 0x0B80 and ord(c) < 0x0BFF for c in l2_text)

    font_l1 = NSFont.fontWithName_size_("TamilSangamMN-Bold" if is_tamil_l1 else "Futura-Bold", 40.0) or NSFont.boldSystemFontOfSize_(40.0)
    font_l2 = NSFont.fontWithName_size_("TamilSangamMN-Bold" if is_tamil_l2 else "Futura-Bold", 54.0) or NSFont.boldSystemFontOfSize_(54.0)

    white_color = NSColor.whiteColor()
    yellow_color = NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 0.90, 0.0, 1.0)
    black_color = NSColor.blackColor()

    astr_l1_s = NSAttributedString.alloc().initWithString_attributes_(l1_text, {
        NSFontAttributeName: font_l1, NSForegroundColorAttributeName: black_color,
        NSStrokeColorAttributeName: black_color, NSStrokeWidthAttributeName: 7.0
    })
    astr_l1_f = NSAttributedString.alloc().initWithString_attributes_(l1_text, {
        NSFontAttributeName: font_l1, NSForegroundColorAttributeName: white_color
    })

    astr_l2_s = NSAttributedString.alloc().initWithString_attributes_(l2_text, {
        NSFontAttributeName: font_l2, NSForegroundColorAttributeName: black_color,
        NSStrokeColorAttributeName: black_color, NSStrokeWidthAttributeName: 8.0
    })
    astr_l2_f = NSAttributedString.alloc().initWithString_attributes_(l2_text, {
        NSFontAttributeName: font_l2, NSForegroundColorAttributeName: yellow_color
    })

    sz1 = astr_l1_f.size()
    sz2 = astr_l2_f.size()

    if align == "left":
        x1 = 70.0
        x2 = 70.0
    elif align == "right":
        x1 = width - sz1.width - 70.0
        x2 = width - sz2.width - 70.0
    else:
        x1 = (width - sz1.width) / 2
        x2 = (width - sz2.width) / 2

    y1 = height - 90
    y2 = height - 175

    astr_l1_s.drawAtPoint_((x1, y1))
    astr_l1_f.drawAtPoint_((x1, y1))
    astr_l2_s.drawAtPoint_((x2, y2))
    astr_l2_f.drawAtPoint_((x2, y2))

    ctx.flushGraphics()
    return bytes(rep.bitmapData()[0:rep.bytesPerRow() * height])

def render_karaoke_sub_frame(words_status, width=WIDTH, height=SUBS_H):
    """Reference 2: Raj Shamani Center Karaoke (White with Neon Yellow Active Highlight)."""
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, width, height, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
    )
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.setCurrentContext_(ctx)
    NSColor.clearColor().set()
    NSRectFill(NSMakeRect(0, 0, width, height))

    if not words_status:
        ctx.flushGraphics()
        return bytes(rep.bitmapData()[0:rep.bytesPerRow() * height])

    font = NSFont.fontWithName_size_("TamilSangamMN-Bold", 48.0) or NSFont.boldSystemFontOfSize_(48.0)
    white_color = NSColor.whiteColor()
    yellow_color = NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 0.90, 0.0, 1.0)
    black_color = NSColor.blackColor()

    s_astr = NSMutableAttributedString.alloc().init()
    for w, _ in words_status:
        astr = NSAttributedString.alloc().initWithString_attributes_(w + " ", {
            NSFontAttributeName: font, NSForegroundColorAttributeName: black_color,
            NSStrokeColorAttributeName: black_color, NSStrokeWidthAttributeName: 7.0
        })
        s_astr.appendAttributedString_(astr)

    f_astr = NSMutableAttributedString.alloc().init()
    for w, is_act in words_status:
        c = yellow_color if is_act else white_color
        astr = NSAttributedString.alloc().initWithString_attributes_(w + " ", {
            NSFontAttributeName: font, NSForegroundColorAttributeName: c
        })
        f_astr.appendAttributedString_(astr)

    sz = f_astr.size()
    x = (width - sz.width) / 2
    y = (height - sz.height) / 2

    s_astr.drawAtPoint_((x, y))
    f_astr.drawAtPoint_((x, y))

    ctx.flushGraphics()
    return bytes(rep.bitmapData()[0:rep.bytesPerRow() * height])

# -------------------------------------------------------------
# BUILD SUBTITLE MOVs
# -------------------------------------------------------------

def build_ref1_subs(out_mov):
    sub_events = []
    curr_t = 0.0
    for cut in CUTS_SPEC:
        # Determine alignment based on speaker:
        # Guest on right -> text on LEFT
        # Host on left -> text on RIGHT
        # Hanuman B-roll (face on right) -> text on LEFT
        align = "right" if cut["speaker"] == "host" else "left"
        for pst, pet, l1, l2 in cut["ref1_subtitles"]:
            sub_events.append((curr_t + pst, curr_t + pet, l1, l2, align))
        curr_t += (cut["et"] - cut["st"])

    cmd_pipe = [
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{SUBS_H}", "-framerate", "30", "-i", "-",
        "-c:v", "png", "-pix_fmt", "rgba", str(out_mov)
    ]
    proc = subprocess.Popen(cmd_pipe, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_frames = int(round(total_dur * 30))
    blank = render_side_sub_frame("", "")

    for f_idx in range(total_frames):
        t_sec = f_idx / 30.0
        active_ev = None
        for w_st, w_et, l1, l2, al in sub_events:
            if w_st <= t_sec < w_et:
                active_ev = (l1, l2, al)
                break
        raw = render_side_sub_frame(active_ev[0], active_ev[1], align=active_ev[2]) if active_ev else blank
        proc.stdin.write(raw)
    proc.stdin.close()
    proc.wait()

def build_ref2_subs(out_mov):
    sub_events = []
    curr_t = 0.0
    for cut in CUTS_SPEC:
        for pst, pet, phrase in cut["word_subtitles"]:
            words = phrase.split()
            w_dur = (pet - pst) / max(len(words), 1)
            for w_idx in range(len(words)):
                sub_events.append((curr_t + pst + (w_idx * w_dur), curr_t + pst + ((w_idx + 1) * w_dur), phrase, w_idx))
        curr_t += (cut["et"] - cut["st"])

    cmd_pipe = [
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{SUBS_H}", "-framerate", "30", "-i", "-",
        "-c:v", "png", "-pix_fmt", "rgba", str(out_mov)
    ]
    proc = subprocess.Popen(cmd_pipe, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_frames = int(round(total_dur * 30))
    blank = render_karaoke_sub_frame([])

    for f_idx in range(total_frames):
        t_sec = f_idx / 30.0
        active_ev = None
        for w_st, w_et, phr, w_i in sub_events:
            if w_st <= t_sec < w_et:
                active_ev = (phr, w_i)
                break
        if active_ev:
            words = active_ev[0].split()
            status = [(w, i == active_ev[1]) for i, w in enumerate(words)]
            raw = render_karaoke_sub_frame(status)
        else:
            raw = blank
        proc.stdin.write(raw)
    proc.stdin.close()
    proc.wait()

# -------------------------------------------------------------
# RENDER ALL 4 STYLES
# -------------------------------------------------------------

def render_reference_1():
    print("\n🎬 Rendering Reference 1 Style: Minimalist Letterbox + Side-Aligned Subtitles...")
    cut_files = []
    concat_list = WORKSPACE / "ref1_cuts.txt"
    for idx, cut in enumerate(CUTS_SPEC):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"ref1_cut_{idx}.mp4"
        cut_files.append(out_cut)
        if cut["broll"]:
            vf = f"scale={VID_W}:{VID_H}:force_original_aspect_ratio=increase,crop={VID_W}:{VID_H},setsar=1,fps=30"
            cmd = ["ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}", "-stream_loop", "-1", "-i", cut["broll"], "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        else:
            vf = f"{CROP_HOST_810 if cut['speaker']=='host' else CROP_GUEST_810},setsar=1,fps=30"
            cmd = ["ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}", "-i", str(RAW_VIDEO), "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(concat_list, "w") as f:
        for cf in cut_files: f.write(f"file '{cf}'\n")

    base_vid = WORKSPACE / "ref1_base.mp4"
    cmd_base = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-vf", f"pad={WIDTH}:{HEIGHT}:0:{VID_Y}:color=black",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_vid)
    ]
    subprocess.run(cmd_base, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subs_mov = WORKSPACE / "ref1_subs.mov"
    build_ref1_subs(subs_mov)

    final_out = EXPORT_DIR / "Reel_1_Reference_1_Style.mp4"
    cmd_final = [
        "ffmpeg", "-y", "-i", str(base_vid), "-i", str(subs_mov), "-i", str(mixed_audio),
        "-filter_complex", f"[0:v][1:v]overlay=0:{SUBS_Y}[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest",
        str(final_out)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # QA Frames
    subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref1_t10s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-ss", "15.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref1_hanuman_t15s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ COMPLETED: {final_out.name}")

def render_reference_2():
    print("\n🎬 Rendering Reference 2 Style: Full-Bleed 9:16 Vertical + Center Karaoke (Raj Shamani Style)...")
    cut_files = []
    concat_list = WORKSPACE / "ref2_cuts.txt"
    for idx, cut in enumerate(CUTS_SPEC):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"ref2_cut_{idx}.mp4"
        cut_files.append(out_cut)
        if cut["broll"]:
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"
            cmd = ["ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}", "-stream_loop", "-1", "-i", cut["broll"], "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        else:
            vf = f"{CROP_HOST_916 if cut['speaker']=='host' else CROP_GUEST_916},setsar=1,fps=30"
            cmd = ["ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}", "-i", str(RAW_VIDEO), "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(concat_list, "w") as f:
        for cf in cut_files: f.write(f"file '{cf}'\n")

    base_vid = WORKSPACE / "ref2_base.mp4"
    cmd_base = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_vid)
    ]
    subprocess.run(cmd_base, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subs_mov = WORKSPACE / "ref2_subs.mov"
    build_ref2_subs(subs_mov)

    final_out = EXPORT_DIR / "Reel_1_Reference_2_Style.mp4"
    cmd_final = [
        "ffmpeg", "-y", "-i", str(base_vid), "-i", str(subs_mov), "-i", str(mixed_audio),
        "-filter_complex", "[0:v][1:v]overlay=0:1250[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest",
        str(final_out)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref2_t10s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ COMPLETED: {final_out.name}")

def render_reference_3():
    print("\n🎬 Rendering Reference 3 Style: Cinematic Letterbox + Bold Center Punchline (Kisthenics Style)...")
    base_vid = WORKSPACE / "ref1_base.mp4"  # Share letterbox base
    subs_mov = WORKSPACE / "ref2_subs.mov"  # Clean center typography

    final_out = EXPORT_DIR / "Reel_1_Reference_3_Style.mp4"
    cmd_final = [
        "ffmpeg", "-y", "-i", str(base_vid), "-i", str(subs_mov), "-i", str(mixed_audio),
        "-filter_complex", f"[0:v][1:v]overlay=0:{SUBS_Y}[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest",
        str(final_out)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref3_t10s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ COMPLETED: {final_out.name}")

def render_reference_4():
    print("\n🎬 Rendering Reference 4 Style: Editorial Documentary + Opening Hook Headline (Delta Weatherman Style)...")
    base_vid = WORKSPACE / "ref1_base.mp4"
    subs_mov = WORKSPACE / "ref1_subs.mov"

    # Create Opening 4-Second Hook Headline Banner PNG
    hook_banner = WORKSPACE / "ref4_hook_banner.png"
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, WIDTH, 180, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
    )
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.setCurrentContext_(ctx)
    NSColor.colorWithDeviceRed_green_blue_alpha_(0.1, 0.1, 0.1, 0.85).set()
    NSRectFill(NSMakeRect(0, 0, WIDTH, 180))

    font_b = NSFont.fontWithName_size_("TamilSangamMN-Bold", 44.0) or NSFont.boldSystemFontOfSize_(44.0)
    astr_b = NSAttributedString.alloc().initWithString_attributes_("ராமாயணம் கற்றுத்தரும் வாழ்க்கை பாடம் 🏹", {
        NSFontAttributeName: font_b,
        NSForegroundColorAttributeName: NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 0.9, 0.0, 1.0)
    })
    sz = astr_b.size()
    astr_b.drawAtPoint_(((WIDTH - sz.width) / 2, (180 - sz.height) / 2))
    ctx.flushGraphics()
    png_data = rep.representationUsingType_properties_(4, None)
    png_data.writeToFile_atomically_(str(hook_banner), True)

    final_out = EXPORT_DIR / "Reel_1_Reference_4_Style.mp4"
    # Overlay hook banner for first 4.0 seconds, fade out
    cmd_final = [
        "ffmpeg", "-y", "-i", str(base_vid), "-loop", "1", "-i", str(hook_banner), "-i", str(subs_mov), "-i", str(mixed_audio),
        "-filter_complex",
        "[1:v]format=rgba,fade=t=out:st=3.5:d=0.5:alpha=1[banner_faded];"
        f"[0:v][banner_faded]overlay=0:360:enable='between(t,0,4.0)'[base_with_banner];"
        f"[base_with_banner][2:v]overlay=0:{SUBS_Y}[v]",
        "-map", "[v]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest",
        str(final_out)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(["ffmpeg", "-y", "-ss", "2.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref4_t2s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref4_t10s.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ COMPLETED: {final_out.name}")

def main():
    print("=" * 75)
    print("🚀 BATCH RENDERING ALL 4 REFERENCE STYLES FOR REEL 1")
    print("=" * 75)
    render_reference_1()
    render_reference_2()
    render_reference_3()
    render_reference_4()
    print("\n" + "=" * 75)
    print("🎉 ALL 4 REFERENCE EDITS COMPLETED SUCCESSFULLY IN EXPORT FOLDER!")
    print("=" * 75)

if __name__ == "__main__":
    main()
