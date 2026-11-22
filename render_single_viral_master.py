#!/usr/bin/env python3
"""
Render Master Viral Reel: EVERYBODY IS LIKE HANUMAN (THE MENTOR LESSON)
Duration: 74.0s (1:14 min)

Integrates:
1. Demucs v4 (htdemucs) Vocal Separation & Studio Noise Cancellation
2. Broadcast Voice Enhancement (Highpass, De-mud EQ, Presence Boost, Compand)
3. Audible Flute BGM bed at -28 dB under vocals
4. Real Podcast Spoken Content (1988.0s to 2062.0s)
5. AppKit CoreText Tamil Subtitles (14pt black stroke, #FF8400 highlight, SUBS_Y=1200)
6. Rec.709 SDR Container Tagging (0% Red Cast)
"""

import os
import sys
import subprocess
import unicodedata
from pathlib import Path
from PIL import Image

from AppKit import (
    NSBitmapImageRep, NSGraphicsContext, NSColor, NSRectFill, NSMakeRect,
    NSFont, NSFontAttributeName, NSForegroundColorAttributeName,
    NSStrokeColorAttributeName, NSStrokeWidthAttributeName,
    NSAttributedString, NSMutableAttributedString, NSDeviceRGBColorSpace,
    NSPNGFileType
)

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
ASSETS_DIR = WORKSPACE / "assets"
BROLLS_DIR = ASSETS_DIR / "brolls"
AUDIO_DIR = ASSETS_DIR / "audio"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

# Colors
ORANGE_HEX = "#FF8400"
ORANGE_R = 255.0 / 255.0
ORANGE_G = 132.0 / 255.0
ORANGE_B = 0.0 / 255.0

WIDTH = 1080
HEIGHT = 1920
BANNER_H = 142
SUBS_Y = 1200
SUBS_H = 180

CROP_HOST = "crop=2160:1880:190:190,scale=1080:940:flags=lanczos"
CROP_GUEST = "crop=2160:1880:1530:190,scale=1080:940:flags=lanczos"

REEL_SPEC = {
    "title_l1": "EVERYBODY IS LIKE HANUMAN! 🏹",
    "title_l2": "YOU NEED A MENTOR FOR YOUR POWER",
    "emoji": "🏹",
    "filename": "Reel_202_Viral_Hanuman_Mentor.mp4",
    "cuts": [
        {
            # Host asks the core question
            "st": 1988.0, "et": 1996.0, "crop": CROP_HOST, "broll": None,
            "phrases": [
                (0.20, 3.80, "ராமாயணத்துல இருந்து..."),
                (4.00, 7.80, "நாம் என்ன வாழ்க்கை பாடம் எடுத்துக்கணும்?")
            ]
        },
        {
            # Guest delivers the hook
            "st": 1996.0, "et": 2008.5, "crop": CROP_GUEST, "broll": None,
            "phrases": [
                (0.20, 5.80, "நான் வந்து ஹனுமான பத்தி மட்டும் பேச நினைக்கிறேன்!"),
                (6.00, 12.20, "Everybody in this world is like Hanuman!")
            ]
        },
        {
            # Thematic B-roll with continuous guest dialogue
            "st": 2008.5, "et": 2018.5, "crop": None, "broll": str(BROLLS_DIR / "broll_golden_sunrise.mp4"),
            "phrases": [
                (0.20, 4.80, "நமக்குள்ள Latent potential ஒளிஞ்சிருக்கு..."),
                (5.00, 9.80, "But someone has to show it to us, that's the MENTOR!")
            ]
        },
        {
            # Guest explains Jambavan & self-doubt
            "st": 2018.5, "et": 2035.0, "crop": CROP_GUEST, "broll": None,
            "phrases": [
                (0.20, 7.80, "ஜாம்பவான் வந்து நினைவுபடுத்தும் போது தான்..."),
                (8.00, 16.20, "ஹனுமானுக்கே தன்னுடைய உண்மையான பலம் புரியுது!")
            ]
        },
        {
            # Thematic B-roll on Loyalty
            "st": 2035.0, "et": 2048.0, "crop": None, "broll": str(BROLLS_DIR / "broll_temple.mp4"),
            "phrases": [
                (0.20, 6.00, "இன்னைக்கு பல பேர்கிட்ட இல்லாதது என்னன்னா..."),
                (6.20, 12.80, "Unconditional Loyalty and Dedication!")
            ]
        },
        {
            # Guest delivers the final climax
            "st": 2048.0, "et": 2062.0, "crop": CROP_GUEST, "broll": None,
            "phrases": [
                (0.20, 6.50, "ஹனுமான் காட்டிய அந்த தன்னலமற்ற விசுவாசம் தான்..."),
                (6.80, 13.80, "வாழ்க்கையின் மிகப்பெரிய பாடம்! 🏹")
            ]
        }
    ]
}

def render_banner(title_l1, title_l2, emoji_char, out_path):
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, WIDTH, BANNER_H, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
    )
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.setCurrentContext_(ctx)

    bg_color = NSColor.colorWithDeviceRed_green_blue_alpha_(ORANGE_R, ORANGE_G, ORANGE_B, 1.0)
    bg_color.set()
    NSRectFill(NSMakeRect(0, 0, WIDTH, BANNER_H))

    font_futura = NSFont.fontWithName_size_("Futura-Bold", 44) or NSFont.boldSystemFontOfSize_(44)
    font_emoji = NSFont.fontWithName_size_("AppleColorEmoji", 38)

    clean_l1 = title_l1.replace(emoji_char, "").strip() if emoji_char else title_l1.strip()
    astr1 = NSMutableAttributedString.alloc().init()
    p1 = NSAttributedString.alloc().initWithString_attributes_(clean_l1 + " ", {
        NSFontAttributeName: font_futura,
        NSForegroundColorAttributeName: NSColor.blackColor()
    })
    astr1.appendAttributedString_(p1)
    if emoji_char and emoji_char in title_l1:
        p_emo = NSAttributedString.alloc().initWithString_attributes_(emoji_char, {
            NSFontAttributeName: font_emoji
        })
        astr1.appendAttributedString_(p_emo)

    sz1 = astr1.size()
    x1 = (WIDTH - sz1.width) / 2
    y1 = BANNER_H - 58
    astr1.drawAtPoint_((x1, y1))

    clean_l2 = title_l2.replace(emoji_char, "").strip() if emoji_char else title_l2.strip()
    astr2 = NSMutableAttributedString.alloc().init()
    p2 = NSAttributedString.alloc().initWithString_attributes_(clean_l2 + " ", {
        NSFontAttributeName: font_futura,
        NSForegroundColorAttributeName: NSColor.blackColor()
    })
    astr2.appendAttributedString_(p2)
    if emoji_char and emoji_char in title_l2:
        p_emo = NSAttributedString.alloc().initWithString_attributes_(emoji_char, {
            NSFontAttributeName: font_emoji
        })
        astr2.appendAttributedString_(p_emo)

    sz2 = astr2.size()
    x2 = (WIDTH - sz2.width) / 2
    y2 = BANNER_H - 120
    astr2.drawAtPoint_((x2, y2))

    ctx.flushGraphics()
    png_data = rep.representationUsingType_properties_(NSPNGFileType, None)
    png_data.writeToFile_atomically_(str(out_path), True)
    print("✅ Rendered Header Banner:", out_path)

def render_sub_frame(words_status, width=WIDTH, height=SUBS_H, font_name="TamilSangamMN-Bold", base_font_size=44):
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, width, height, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
    )
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.setCurrentContext_(ctx)
    NSColor.clearColor().set()
    NSRectFill(NSMakeRect(0, 0, width, height))

    if not words_status:
        ctx.flushGraphics()
        bitmap_data = rep.bitmapData()
        return bytes(bitmap_data[0:rep.bytesPerRow() * height])

    MAX_SAFE_WIDTH = 880.0
    norm_words_status = [(unicodedata.normalize('NFC', w), act) for w, act in words_status]
    full_text = " ".join([w for w, _ in norm_words_status])

    font = NSFont.fontWithName_size_(font_name, base_font_size) or NSFont.boldSystemFontOfSize_(base_font_size)
    test_astr = NSAttributedString.alloc().initWithString_attributes_(full_text, {NSFontAttributeName: font})
    test_width = test_astr.size().width

    if test_width > MAX_SAFE_WIDTH:
        scale_factor = MAX_SAFE_WIDTH / test_width
        chosen_font_size = max(base_font_size * scale_factor, 28.0)
        font = NSFont.fontWithName_size_(font_name, chosen_font_size) or NSFont.boldSystemFontOfSize_(chosen_font_size)

    stroke_num = -14.0
    orange_color = NSColor.colorWithDeviceRed_green_blue_alpha_(ORANGE_R, ORANGE_G, ORANGE_B, 1.0)
    white_color = NSColor.whiteColor()
    black_color = NSColor.blackColor()

    mastr = NSMutableAttributedString.alloc().init()
    for w, is_active in norm_words_status:
        fill_color = orange_color if is_active else white_color
        attrs = {
            NSFontAttributeName: font,
            NSForegroundColorAttributeName: fill_color,
            NSStrokeColorAttributeName: black_color,
            NSStrokeWidthAttributeName: stroke_num
        }
        astr = NSAttributedString.alloc().initWithString_attributes_(w + " ", attrs)
        mastr.appendAttributedString_(astr)

    total_sz = mastr.size()
    x = (width - total_sz.width) / 2
    y = (height - total_sz.height) / 2
    mastr.drawAtPoint_((x, y))

    ctx.flushGraphics()
    bitmap_data = rep.bitmapData()
    return bytes(bitmap_data[0:rep.bytesPerRow() * height])

def main():
    print("=" * 65)
    print("🚀 RENDERING VIRAL MASTER REEL: EVERYBODY IS LIKE HANUMAN 🏹")
    print("=" * 65)

    banner_png = WORKSPACE / "banner_hanuman_master.png"
    render_banner(REEL_SPEC["title_l1"], REEL_SPEC["title_l2"], REEL_SPEC["emoji"], banner_png)

    total_dur = sum(c["et"] - c["st"] for c in REEL_SPEC["cuts"])
    print(f"Total Video Duration: {total_dur:.1f}s ({total_dur/60:.2f} mins) [Target: 1m - 1m20s]")

    # 1. Process Video Cuts
    cut_files = []
    concat_list = WORKSPACE / "temp_hanuman_concat.txt"

    for idx, cut in enumerate(REEL_SPEC["cuts"]):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"temp_hanuman_cut_{idx}.mp4"
        cut_files.append(out_cut)

        if cut["broll"]:
            vf = "scale=1080:940:force_original_aspect_ratio=increase,crop=1080:940,setsar=1,fps=30"
            cmd = [
                "ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}",
                "-stream_loop", "-1", "-i", cut["broll"],
                "-vf", vf, "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                str(out_cut)
            ]
        else:
            vf = f"{cut['crop']},colorspace=space=bt709:ispace=bt2020nc:primaries=bt709:iprimaries=bt2020:trc=bt709:itrc=bt2020-10:format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,setsar=1,fps=30"
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

    # 2. Concat & Pad with Banner
    base_vid = WORKSPACE / "temp_hanuman_base.mp4"
    cmd_base = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-loop", "1", "-i", str(banner_png),
        "-filter_complex",
        "[0:v]pad=1080:1920:0:558:color=black[padded];"
        "[padded][1:v]overlay=0:416:shortest=1[comp]",
        "-map", "[comp]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_vid)
    ]
    subprocess.run(cmd_base, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ Generated Base Video with Banner:", base_vid)

    # 3. Audio Extraction & Demucs Vocal Separation (Studio Noise Cancellation)
    raw_audio_track = WORKSPACE / "temp_hanuman_raw_audio.wav"
    audio_cuts = []
    for idx, cut in enumerate(REEL_SPEC["cuts"]):
        dur = cut["et"] - cut["st"]
        acut = WORKSPACE / f"temp_hanuman_acut_{idx}.wav"
        audio_cuts.append(acut)
        cmd_acut = [
            "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
            "-i", str(RAW_VIDEO),
            "-ar", "44100", "-ac", "2",
            str(acut)
        ]
        subprocess.run(cmd_acut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    aconcat_list = WORKSPACE / "temp_hanuman_aconcat.txt"
    with open(aconcat_list, "w") as f:
        for ac in audio_cuts:
            f.write(f"file '{ac}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(aconcat_list),
        "-c", "copy", str(raw_audio_track)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("🎙️ Running Demucs Vocal Separation (Studio-Grade Noise Cancellation)...")
    subprocess.run([
        sys.executable, "-m", "demucs", "--two-stems=vocals",
        "-o", str(WORKSPACE / "demucs_hanuman_run"), str(raw_audio_track)
    ], check=True)
    isolated_vocals = WORKSPACE / "demucs_hanuman_run" / "htdemucs" / "temp_hanuman_raw_audio" / "vocals.wav"
    print("✅ Isolated Clean Vocals:", isolated_vocals)

    # 4. Voice Enhancement + BGM Mixing (-14.0 LUFS Broadcast Standard)
    bgm_file = AUDIO_DIR / "ramayan_flute_bgm.mp3"
    mixed_audio = WORKSPACE / "temp_hanuman_mixed_audio.wav"
    
    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(isolated_vocals),
        "-stream_loop", "-1", "-i", str(bgm_file),
        "-filter_complex",
        "[0:a]highpass=f=80,equalizer=f=280:t=q:w=1.5:g=-3.0,equalizer=f=3200:t=q:w=1.2:g=+3.5,equalizer=f=8000:t=q:w=1.0:g=+2.0,compand=attacks=0.02:decays=0.15:points=-60/-60|-24/-12|0/-3:soft-knee=6[vocal_clean];"
        "[1:a]volume=0.045[bgm_soft];"
        "[vocal_clean][bgm_soft]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[out]",
        "-map", "[out]",
        str(mixed_audio)
    ]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ Generated Master Enhanced Audio:", mixed_audio)

    # 5. Build Subtitles Stream at SUBS_Y = 1200
    sub_events = []
    curr_t = 0.0
    for cut in REEL_SPEC["cuts"]:
        for pst, pet, phrase in cut["phrases"]:
            words = phrase.split()
            w_dur = (pet - pst) / max(len(words), 1)
            for w_idx in range(len(words)):
                w_st = curr_t + pst + (w_idx * w_dur)
                w_et = w_st + w_dur
                sub_events.append((w_st, w_et, phrase, w_idx))
        curr_t += (cut["et"] - cut["st"])

    subs_mov = WORKSPACE / "temp_hanuman_subs.mov"
    cmd_sub_pipe = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{WIDTH}x{SUBS_H}", "-framerate", "30", "-i", "-",
        "-c:v", "png", "-pix_fmt", "rgba",
        str(subs_mov)
    ]
    sub_proc = subprocess.Popen(cmd_sub_pipe, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_frames = int(round(total_dur * 30))
    blank_bytes = render_sub_frame([])

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
            raw_bytes = render_sub_frame(status)
        else:
            raw_bytes = blank_bytes
        sub_proc.stdin.write(raw_bytes)

    sub_proc.stdin.close()
    sub_proc.wait()
    print("✅ Generated Subtitles Overlay Stream:", subs_mov)

    # 6. Final Composite Mux
    final_output = EXPORT_DIR / REEL_SPEC["filename"]
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
    subprocess.run(cmd_final, check=True)
    size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"\n🎉 MASTER VIRAL REEL COMPLETED: {final_output} ({size_mb:.1f} MB, {total_dur:.1f}s)")

    # 7. Extract QA Frame
    qa_frame = FRAMES_DIR / "qa_viral_hanuman_mentor.jpg"
    subprocess.run([
        "ffmpeg", "-y", "-ss", "14.0", "-i", str(final_output),
        "-vframes", "1", "-q:v", "2", str(qa_frame)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("📸 Saved QA Inspection Frame:", qa_frame)

if __name__ == "__main__":
    main()
