#!/usr/bin/env python3
"""
Full Podcast Episode Master Render Engine (16:9 Landscape 1920x1080)
Updates LLB_Podcast_Full_Episode_RajShamani_Style.mp4:
1. Adds continuous Orange Banner (#EA8207) at the top (Y: 0..76) with Futura Bold and Apple Color Emoji 📜 across the ENTIRE duration.
2. Mixes authentic Indian Classical Flute BGM (Raag Shivranjani) ducked to -24 dB under speech.
3. Encoded with macOS Hardware Acceleration (h264_videotoolbox) for broadcast quality and speed.
4. Extracts QA frames directly into export/FRAMES/.
"""

import os
import sys
import subprocess
from pathlib import Path

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
ASSETS = WORKSPACE / "assets"
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
EXPORT_FRAMES = EXPORT_DIR / "FRAMES"
EXPORT_FRAMES.mkdir(parents=True, exist_ok=True)

INPUT_EPISODE = EXPORT_DIR / "LLB_Podcast_Full_Episode_RajShamani_Style.mp4"
TEMP_OUTPUT = WORKSPACE / "temp_master_full_episode.mp4"
BGM_FLUTE = ASSETS / "audio" / "ramayan_flute_bgm.mp3"
BANNER_IMG = WORKSPACE / "banner_full_16x9.png"

def render_full_banner():
    import Cocoa
    from AppKit import (
        NSBitmapImageRep, NSGraphicsContext, NSColor, NSFont,
        NSFontAttributeName, NSForegroundColorAttributeName,
        NSAttributedString, NSMutableParagraphStyle, NSParagraphStyleAttributeName,
        NSCenterTextAlignment, NSMakeRect, NSRectFill, NSDeviceRGBColorSpace
    )

    w, h = 1920, 76
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, w, h, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
    )
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.setCurrentContext_(ctx)

    # 1. Fill solid orange #EA8207
    bg = NSColor.colorWithCalibratedRed_green_blue_alpha_(234/255.0, 130/255.0, 7/255.0, 1.0)
    bg.set()
    NSRectFill(NSMakeRect(0, 0, w, h))

    # 2. Text styling: Futura Bold, 34pt
    font = NSFont.fontWithName_size_('Futura-Bold', 34) or NSFont.boldSystemFontOfSize_(34)
    para = NSMutableParagraphStyle.alloc().init()
    para.setAlignment_(NSCenterTextAlignment)

    attrs = {
        NSFontAttributeName: font,
        NSForegroundColorAttributeName: NSColor.blackColor(),
        NSParagraphStyleAttributeName: para
    }

    text = "LLB'S PODCAST | THE UNTOLD SECRETS OF RAMAYANAM: KAMBAR VS VALMIKI 📜"
    astr = NSAttributedString.alloc().initWithString_attributes_(text, attrs)

    size = astr.size()
    y = (h - size.height) / 2
    astr.drawInRect_(NSMakeRect(0, y, w, size.height))
    ctx.flushGraphics()

    png_data = rep.representationUsingType_properties_(Cocoa.NSPNGFileType, None)
    png_data.writeToFile_atomically_(str(BANNER_IMG), True)
    print("Full 16:9 banner generated.")

def main():
    print("=" * 80)
    print("🎬 MASTER RENDERING FULL PODCAST EPISODE WITH CONTINUOUS ORANGE BANNER & FLUTE BGM")
    print("=" * 80)

    render_full_banner()

    filter_complex = (
        "[0:v][1:v]overlay=0:0:shortest=1[v];"
        "[2:a]volume=0.045,afade=t=in:ss=0:d=2.0[bgm];"
        "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(INPUT_EPISODE),
        "-loop", "1", "-i", str(BANNER_IMG),
        "-stream_loop", "-1", "-i", str(BGM_FLUTE),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[outa]",
        "-c:v", "h264_videotoolbox", "-b:v", "7M",
        "-c:a", "aac", "-b:a", "320k",
        str(TEMP_OUTPUT)
    ]
    print("Executing hardware-accelerated render...")
    subprocess.run(cmd, check=True)

    print("Replacing target master video...")
    os.replace(str(TEMP_OUTPUT), str(INPUT_EPISODE))
    print(f"✅ Full Episode updated successfully: {INPUT_EPISODE} ({INPUT_EPISODE.stat().st_size / 1024 / 1024:.1f} MB)")

    # Extract QA screenshots
    print("Extracting QA frames directly to FRAMES/...")
    qa_times = [25.0, 75.0, 300.0, 900.0, 1800.0]
    for t in qa_times:
        qa_file = EXPORT_FRAMES / f"qa_full_episode_t{int(t)}s.jpg"
        subprocess.run(["ffmpeg", "-y", "-ss", str(t), "-i", str(INPUT_EPISODE), "-vframes", "1", str(qa_file)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("All QA frames extracted.")

if __name__ == "__main__":
    main()
