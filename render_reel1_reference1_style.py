#!/usr/bin/env python3
"""
Render Reel 1 using Reference 1 Style:
- Source: 202.MOV (Reel 1: Hanuman / Mentorship)
- Visual Style of Reference 1:
  * 1080x1920 (9:16) vertical canvas with clean, minimalist letterboxed 16:9 widescreen video in center (1080x810 at y=555).
  * NO top header banner (clean black top and bottom letterbox bars, exactly like Reference 1).
  * Two-Tier Subtitles (Line 1: Crisp White #FFFFFF setup, Line 2: Bold Electric Yellow #FFE600 Punchline in ALL CAPS).
  * Two-pass text rendering (Pass 1 black stroke + Pass 2 fill) for 100% crisp typography without letter choking.
  * Studio vocal isolation via Demucs v4 (zero echo/noise).
  * Mild background music bed at -28 dB ducked under voice, loudness normalized to -14.5 LUFS.
  * Silent thematic B-rolls (Lord Hanuman latent power).
- Output: /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_1_Style.mp4
"""

import os
import sys
import subprocess
from pathlib import Path
import unicodedata

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
SUBS_H = 220
SUBS_Y = VID_Y + VID_H - SUBS_H - 40  # 555 + 810 - 220 - 40 = 1105 (inside lower video)

# Crops for 4K -> 1080x810
CROP_HOST = "crop=2160:1620:190:320,scale=1080:810:flags=lanczos"
CROP_GUEST = "crop=2160:1620:1530:320,scale=1080:810:flags=lanczos"

REEL_1_SPEC = {
    "filename": "Reel_1_Reference_1_Style.mp4",
    "cuts": [
        {
            "st": 1988.0, "et": 1996.0, "crop": CROP_HOST, "broll": None,
            "subtitles": [
                (0.3, 3.8, "ராமாயணத்துல இருந்து...", "LIFE LESSON"),
                (4.0, 7.8, "நாம் என்ன பாடம்", "எடுத்துக்கணும்?")
            ]
        },
        {
            "st": 1996.0, "et": 2008.5, "crop": CROP_GUEST, "broll": None,
            "subtitles": [
                (0.3, 5.8, "நான் வந்து", "ஹனுமான பத்தி மட்டும்!"),
                (6.0, 12.2, "Everybody in this world...", "IS LIKE HANUMAN! 🏹")
            ]
        },
        {
            "st": 2008.5, "et": 2018.5, "crop": None, "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"),
            "subtitles": [
                (0.3, 4.8, "நமக்குள்ள ஒளிஞ்சிருக்கு...", "LATENT POTENTIAL!"),
                (5.0, 9.8, "Someone has to show it...", "THAT'S THE MENTOR!")
            ]
        },
        {
            "st": 2018.5, "et": 2035.0, "crop": CROP_GUEST, "broll": None,
            "subtitles": [
                (0.3, 7.8, "ஜாம்பவான் நினைவுபடுத்தும் போது...", "JAMBAVAN'S ROLE"),
                (8.0, 16.2, "ஹனுமானுக்கே புரியுது...", "REAL INNER POWER! 🔥")
            ]
        },
        {
            "st": 2035.0, "et": 2048.0, "crop": None, "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"),
            "subtitles": [
                (0.3, 6.0, "இன்னைக்கு பல பேர்கிட்ட இல்லாதது...", "WHAT WE LACK TODAY"),
                (6.2, 12.8, "Unconditional...", "LOYALTY & DEDICATION!")
            ]
        },
        {
            "st": 2048.0, "et": 2062.0, "crop": CROP_GUEST, "broll": None,
            "subtitles": [
                (0.3, 6.5, "ஹனுமான் காட்டிய விசுவாசம் தான்...", "SELFLESS DEVOTION"),
                (6.8, 13.8, "வாழ்க்கையின் மிகப்பெரிய பாடம்!", "GREATEST LESSON OF LIFE! 🏹")
            ]
        }
    ]
}

def render_ref1_sub_frame(l1_text, l2_text, width=WIDTH, height=SUBS_H):
    """
    Reference 1 Subtitle Engine:
    Line 1: Crisp White (#FFFFFF), modern clean typography.
    Line 2: Electric Yellow / Gold (#FFE600), bold impact punchline in ALL CAPS.
    Two-pass outline: Pass 1 black stroke (width 7-8px) + Pass 2 clean fill on top.
    """
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

    # Choose fonts based on script (Tamil vs Latin)
    is_tamil_l1 = any(ord(c) > 0x0B80 and ord(c) < 0x0BFF for c in l1_text)
    is_tamil_l2 = any(ord(c) > 0x0B80 and ord(c) < 0x0BFF for c in l2_text)

    font_l1 = NSFont.fontWithName_size_("TamilSangamMN-Bold" if is_tamil_l1 else "Futura-Bold", 38.0) or NSFont.boldSystemFontOfSize_(38.0)
    font_l2 = NSFont.fontWithName_size_("TamilSangamMN-Bold" if is_tamil_l2 else "Futura-Bold", 54.0) or NSFont.boldSystemFontOfSize_(54.0)

    white_color = NSColor.whiteColor()
    yellow_color = NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 0.90, 0.0, 1.0)  # #FFE600
    black_color = NSColor.blackColor()

    # Pass 1 + Pass 2: Line 1 (White)
    astr_l1_stroke = NSAttributedString.alloc().initWithString_attributes_(l1_text, {
        NSFontAttributeName: font_l1,
        NSForegroundColorAttributeName: black_color,
        NSStrokeColorAttributeName: black_color,
        NSStrokeWidthAttributeName: 7.0
    })
    astr_l1_fill = NSAttributedString.alloc().initWithString_attributes_(l1_text, {
        NSFontAttributeName: font_l1,
        NSForegroundColorAttributeName: white_color
    })

    # Pass 1 + Pass 2: Line 2 (Yellow)
    astr_l2_stroke = NSAttributedString.alloc().initWithString_attributes_(l2_text, {
        NSFontAttributeName: font_l2,
        NSForegroundColorAttributeName: black_color,
        NSStrokeColorAttributeName: black_color,
        NSStrokeWidthAttributeName: 8.0
    })
    astr_l2_fill = NSAttributedString.alloc().initWithString_attributes_(l2_text, {
        NSFontAttributeName: font_l2,
        NSForegroundColorAttributeName: yellow_color
    })

    sz1 = astr_l1_fill.size()
    sz2 = astr_l2_fill.size()

    x1 = (width - sz1.width) / 2
    y1 = height - 85
    x2 = (width - sz2.width) / 2
    y2 = height - 170

    astr_l1_stroke.drawAtPoint_((x1, y1))
    astr_l1_fill.drawAtPoint_((x1, y1))

    astr_l2_stroke.drawAtPoint_((x2, y2))
    astr_l2_fill.drawAtPoint_((x2, y2))

    ctx.flushGraphics()
    return bytes(rep.bitmapData()[0:rep.bytesPerRow() * height])

def main():
    print("=" * 70)
    print("🎬 RENDERING REEL 1 USING REFERENCE 1 STYLE")
    print("   (MINIMALIST LETTERBOX + TWO-TIER WHITE/YELLOW IMPACT SUBTITLES)")
    print("=" * 70)

    total_dur = sum(c["et"] - c["st"] for c in REEL_1_SPEC["cuts"])

    # 1. Process Video Cuts
    cut_files = []
    concat_list = WORKSPACE / "ref1_temp_concat.txt"

    for idx, cut in enumerate(REEL_1_SPEC["cuts"]):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"ref1_cut_{idx}.mp4"
        cut_files.append(out_cut)

        if cut["broll"]:
            vf = f"scale={VID_W}:{VID_H}:force_original_aspect_ratio=increase,crop={VID_W}:{VID_H},setsar=1,fps=30"
            cmd = [
                "ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}",
                "-stream_loop", "-1", "-i", cut["broll"],
                "-vf", vf, "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                str(out_cut)
            ]
        else:
            vf = f"{cut['crop']},setsar=1,fps=30"
            cmd = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-vf", vf, "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                str(out_cut)
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(concat_list, "w") as f:
        for cf in cut_files:
            f.write(f"file '{cf}'\n")

    # 2. Concat & Pad with Minimalist Black Letterbox (NO TOP BANNER, EXACTLY LIKE REF 1)
    base_vid = WORKSPACE / "ref1_temp_base.mp4"
    cmd_base = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-vf", f"pad={WIDTH}:{HEIGHT}:0:{VID_Y}:color=black",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_vid)
    ]
    subprocess.run(cmd_base, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  🎞️ Base Letterbox Video Ready (1080x810 centered on 1080x1920)")

    # 3. Audio Extraction & Demucs Vocals (Reusing cached studio Demucs track)
    demucs_vocals = WORKSPACE / "demucs_run_1" / "htdemucs" / "temp_raw_audio_1" / "vocals.wav"
    bgm_file = AUDIO_DIR / "ramayan_flute_bgm.mp3"
    mixed_audio = WORKSPACE / "ref1_temp_mixed_audio.wav"

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
    print("  🎙️ Demucs Vocal Track + Ducked Flute BGM Ready (-14.5 LUFS)")

    # 4. Build Subtitles Stream (Two-Tier White/Yellow Reference 1 Style)
    sub_events = []
    curr_t = 0.0
    for cut in REEL_1_SPEC["cuts"]:
        for pst, pet, l1, l2 in cut["subtitles"]:
            sub_events.append((curr_t + pst, curr_t + pet, l1, l2))
        curr_t += (cut["et"] - cut["st"])

    subs_mov = WORKSPACE / "ref1_temp_subs.mov"
    cmd_sub_pipe = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{SUBS_H}", "-framerate", "30", "-i", "-",
        "-c:v", "png", "-pix_fmt", "rgba",
        str(subs_mov)
    ]
    sub_proc = subprocess.Popen(cmd_sub_pipe, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_frames = int(round(total_dur * 30))
    blank_bytes = render_ref1_sub_frame("", "")

    for f_idx in range(total_frames):
        t_sec = f_idx / 30.0
        active_ev = None
        for w_st, w_et, l1, l2 in sub_events:
            if w_st <= t_sec < w_et:
                active_ev = (l1, l2)
                break
        if active_ev:
            raw_bytes = render_ref1_sub_frame(active_ev[0], active_ev[1])
        else:
            raw_bytes = blank_bytes
        sub_proc.stdin.write(raw_bytes)

    sub_proc.stdin.close()
    sub_proc.wait()
    print("  💬 Rendered Two-Tier Subtitles (Line 1: White, Line 2: Electric Yellow #FFE600)")

    # 5. Final Composite Mux
    final_output = EXPORT_DIR / REEL_1_SPEC["filename"]
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(base_vid),
        "-i", str(subs_mov),
        "-i", str(mixed_audio),
        "-filter_complex", f"[0:v][1:v]overlay=0:{SUBS_Y}[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-shortest",
        str(final_output)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"\n🎉 REEL 1 COMPLETED IN REFERENCE 1 STYLE: {final_output.name} ({size_mb:.1f} MB, {total_dur:.1f}s)")

    # 6. Extract QA Frames
    qa_f1 = FRAMES_DIR / "qa_reel1_ref1_style_t10s.jpg"
    qa_f2 = FRAMES_DIR / "qa_reel1_ref1_style_hanuman_t15s.jpg"
    subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_output), "-vframes", "1", "-q:v", "2", str(qa_f1)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-ss", "15.0", "-i", str(final_output), "-vframes", "1", "-q:v", "2", str(qa_f2)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  📸 Saved QA Frames: {qa_f1.name}, {qa_f2.name}")

    # Cleanup temporary files
    try:
        base_vid.unlink(missing_ok=True)
        subs_mov.unlink(missing_ok=True)
        mixed_audio.unlink(missing_ok=True)
        concat_list.unlink(missing_ok=True)
        for cf in cut_files:
            cf.unlink(missing_ok=True)
    except Exception:
        pass

if __name__ == "__main__":
    main()
