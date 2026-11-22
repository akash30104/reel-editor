#!/usr/bin/env python3
"""
Render Viral Master Reel: EVERYBODY IS LIKE HANUMAN (THE MENTOR LESSON)
Total Duration: 74.0s (1:14 min) [Target: 1min to 1:20min]

Features:
1. Pure Content: Real, gripping life lesson from podcast (1988s to 2062s).
2. Studio-Grade Audio: Demucs vocal separation (noise cancellation) + Voice Enhancement EQ/Compression + -14 LUFS normalization.
3. Mild Cinematic Music: Ramayan Flute BGM bed at -28 dB under vocals.
4. Kallaway Hook Banner: Futura-Bold + AppleColorEmoji + #FF8400 orange accents.
5. Perfect Subtitles: AppKit CoreText (TamilSangamMN-Bold) + 14pt solid black stroke + #FF8400 highlight + SUBS_Y=1200 (elevated safe zone).
6. Apple QuickTime Rec.709 SDR Standard: 0% red cast.
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image

# AppKit CoreText imports
import AppKit
import CoreText
import Foundation

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
ORANGE = "#FF8400"
ORANGE_RGB = (255, 132, 0)
WHITE_RGB = (255, 255, 255)
BLACK_RGB = (0, 0, 0)

CROP_HOST = "crop=2160:1880:190:190,scale=1080:940:flags=lanczos"
CROP_GUEST = "crop=2160:1880:1530:190,scale=1080:940:flags=lanczos"
SUBS_Y = 1200

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
            # Dynamic B-roll with continuous guest dialogue
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

def generate_banner():
    banner_path = WORKSPACE / "banner_hanuman_mentor.png"
    W, H = 1080, 142
    color_space = CoreText.CGColorSpaceCreateDeviceRGB()
    context = CoreText.CGBitmapContextCreate(
        None, W, H, 8, W * 4, color_space,
        CoreText.kCGImageAlphaPremultipliedLast
    )
    
    # Solid Black Background
    CoreText.CGContextSetRGBFillColor(context, 0, 0, 0, 1.0)
    CoreText.CGContextFillRect(context, CoreText.CGRectMake(0, 0, W, H))
    
    # Orange Top and Bottom Accent Borders (4px)
    r_o, g_o, b_o = [c/255.0 for c in ORANGE_RGB]
    CoreText.CGContextSetRGBFillColor(context, r_o, g_o, b_o, 1.0)
    CoreText.CGContextFillRect(context, CoreText.CGRectMake(0, H - 4, W, 4))
    CoreText.CGContextFillRect(context, CoreText.CGRectMake(0, 0, W, 4))
    
    def draw_text(txt, font_name, size, y_bottom, is_orange=False):
        font = AppKit.NSFont.fontWithName_size_(font_name, size)
        if not font:
            font = AppKit.NSFont.boldSystemFontOfSize_(size)
        if is_orange:
            col = AppKit.NSColor.colorWithRed_green_blue_alpha_(r_o, g_o, b_o, 1.0)
        else:
            col = AppKit.NSColor.whiteColor()
            
        para = AppKit.NSMutableParagraphStyle.alloc().init()
        para.setAlignment_(AppKit.NSTextAlignmentCenter)
        
        attrs = {
            AppKit.NSFontAttributeName: font,
            AppKit.NSForegroundColorAttributeName: col,
            AppKit.NSParagraphStyleAttributeName: para
        }
        
        astr = AppKit.NSAttributedString.alloc().initWithString_attributes_(txt, attrs)
        line = CoreText.CTLineCreateWithAttributedString(astr)
        rect = CoreText.CTLineGetImageBounds(line, context)
        x_draw = (W - rect.size.width) / 2.0
        CoreText.CGContextSetTextPosition(context, x_draw, y_bottom)
        CoreText.CTLineDraw(line, context)
        
    draw_text(REEL_SPEC["title_l1"], "Futura-Bold", 42, 80, is_orange=True)
    draw_text(REEL_SPEC["title_l2"], "Futura-Bold", 32, 26, is_orange=False)
    
    cg_img = CoreText.CGBitmapContextCreateImage(context)
    rep = AppKit.NSBitmapImageRep.alloc().initWithCGImage_(cg_img)
    png_data = rep.representationUsingType_properties_(AppKit.NSBitmapImageFileTypePNG, None)
    png_data.writeToFile_atomically_(str(banner_path), True)
    print("✅ Generated Header Banner:", banner_path)
    return banner_path

def render_subtitle_frame(phrase, active_idx):
    W, H = 1080, 180
    color_space = CoreText.CGColorSpaceCreateDeviceRGB()
    context = CoreText.CGBitmapContextCreate(
        None, W, H, 8, W * 4, color_space,
        CoreText.kCGImageAlphaPremultipliedLast
    )
    CoreText.CGContextClearRect(context, CoreText.CGRectMake(0, 0, W, H))
    
    words = phrase.split()
    font_size = 46
    font = AppKit.NSFont.fontWithName_size_("TamilSangamMN-Bold", font_size)
    if not font:
        font = AppKit.NSFont.boldSystemFontOfSize_(font_size)
        
    r_o, g_o, b_o = [c/255.0 for c in ORANGE_RGB]
    orange_col = AppKit.NSColor.colorWithRed_green_blue_alpha_(r_o, g_o, b_o, 1.0)
    white_col = AppKit.NSColor.whiteColor()
    black_col = AppKit.NSColor.blackColor()
    
    mastr = AppKit.NSMutableAttributedString.alloc().init()
    for i, w in enumerate(words):
        w_norm = unicodedata.normalize("NFC", w) if 'unicodedata' in globals() else w
        fill_col = orange_col if i == active_idx else white_col
        attrs = {
            AppKit.NSFontAttributeName: font,
            AppKit.NSForegroundColorAttributeName: fill_col,
            AppKit.NSStrokeColorAttributeName: black_col,
            AppKit.NSStrokeWidthAttributeName: Foundation.NSNumber.numberWithFloat_(-14.0)
        }
        astr = AppKit.NSAttributedString.alloc().initWithString_attributes_(w_norm + " ", attrs)
        mastr.appendAttributedString_(astr)
        
    para = AppKit.NSMutableParagraphStyle.alloc().init()
    para.setAlignment_(AppKit.NSTextAlignmentCenter)
    mastr.addAttribute_value_range_(AppKit.NSParagraphStyleAttributeName, para, Foundation.NSMakeRange(0, mastr.length()))
    
    line = CoreText.CTLineCreateWithAttributedString(mastr)
    rect = CoreText.CTLineGetImageBounds(line, context)
    x_draw = (W - rect.size.width) / 2.0
    y_draw = 45.0
    
    CoreText.CGContextSetTextPosition(context, x_draw, y_draw)
    CoreText.CTLineDraw(line, context)
    
    cg_img = CoreText.CGBitmapContextCreateImage(context)
    rep = AppKit.NSBitmapImageRep.alloc().initWithCGImage_(cg_img)
    data = rep.representationUsingType_properties_(AppKit.NSBitmapImageFileTypePNG, None)
    return bytes(data.bytes())

import unicodedata

def main():
    print("=" * 65)
    print("🚀 RENDERING VIRAL MASTER REEL: EVERYBODY IS LIKE HANUMAN 🏹")
    print("=" * 65)

    banner_path = generate_banner()
    total_dur = sum(c["et"] - c["st"] for c in REEL_SPEC["cuts"])
    print(f"Total Video Duration: {total_dur:.1f}s ({total_dur/60:.2f} mins) [Target: 1m - 1m20s]")

    # 1. Process Video Cuts
    cut_files = []
    concat_list = WORKSPACE / "temp_viral_concat.txt"

    for idx, cut in enumerate(REEL_SPEC["cuts"]):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"temp_viral_cut_{idx}.mp4"
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
    base_vid = WORKSPACE / "temp_viral_base.mp4"
    cmd_base = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-loop", "1", "-i", str(banner_path),
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

    # 3. Audio Extraction & Demucs Vocal Separation (Noise Cancellation)
    raw_audio_track = WORKSPACE / "temp_viral_dialogue_raw.wav"
    audio_cuts = []
    for idx, cut in enumerate(REEL_SPEC["cuts"]):
        dur = cut["et"] - cut["st"]
        acut = WORKSPACE / f"temp_viral_acut_{idx}.wav"
        audio_cuts.append(acut)
        cmd_acut = [
            "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
            "-i", str(RAW_VIDEO),
            "-ar", "44100", "-ac", "2",
            str(acut)
        ]
        subprocess.run(cmd_acut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    aconcat_list = WORKSPACE / "temp_viral_aconcat.txt"
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
        "-o", str(WORKSPACE / "demucs_viral"), str(raw_audio_track)
    ], check=True)
    isolated_vocals = WORKSPACE / "demucs_viral" / "htdemucs" / "temp_viral_dialogue_raw" / "vocals.wav"
    print("✅ Isolated Clean Vocals:", isolated_vocals)

    # 4. Voice Enhancement + BGM Mixing (-14.0 LUFS Broadcast Standard)
    bgm_file = AUDIO_DIR / "ramayan_flute_bgm.mp3"
    mixed_audio = WORKSPACE / "temp_viral_mixed_audio.wav"
    
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

    subs_mov = WORKSPACE / "temp_viral_subs.mov"
    cmd_sub_pipe = [
        "ffmpeg", "-y",
        "-f", "image2pipe", "-framerate", "30", "-i", "-",
        "-c:v", "png", "-pix_fmt", "rgba",
        str(subs_mov)
    ]
    sub_proc = subprocess.Popen(cmd_sub_pipe, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_frames = int(round(total_dur * 30))
    blank_png = render_subtitle_frame("", -1)

    for f_idx in range(total_frames):
        t_sec = f_idx / 30.0
        active_ev = None
        for w_st, w_et, phr, w_i in sub_events:
            if w_st <= t_sec < w_et:
                active_ev = (phr, w_i)
                break
        if active_ev:
            png_bytes = render_subtitle_frame(active_ev[0], active_ev[1])
        else:
            png_bytes = blank_png
        sub_proc.stdin.write(png_bytes)

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
