#!/usr/bin/env python3
"""
render_4_reels_6596_ref11.py
Master Producer for 4 High-Retention Reels from IMG_6596.MOV in Locked Reference 11 Style:

Reel 1: Student to Founder 🚀 (Raw: 176.0s - 236.0s, 60.0s)
Reel 2: Why Register Pvt Ltd? 🏢 (Raw: 236.0s - 296.0s, 60.0s)
Reel 3: Business vs Entrepreneur 💡 (Raw: 296.0s - 356.0s, 60.0s)
Reel 4: Venture vs Traditional Trade 🚀 (Raw: 356.0s - 416.0s, 60.0s)

Key Professional Enhancements:
1. Speech-Locked Acoustic Synchronization: Derived directly from Whisper millisecond audio alignment.
2. Rich Warm Studio Color Grading:
   - curves=master='0/0.02 0.5/0.52 1/0.98' (lifted clean blacks, smooth rolloff)
   - eq=contrast=1.16:saturation=1.25:brightness=0.015 (rich vibrant color)
   - colorbalance=rs=0.04:gs=0.02:bs=-0.04 (warm studio skin tones, neutral whites)
   - unsharp=5:5:0.6:5:5:0.0 (high-frequency luma definition on faces & clothing)
   - setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,format=yuv420p (SDR BT.709 bitstream lock)
3. Header Banner: #FF8400 Signature Orange, 3px black borders, centered bold English title with Apple Color Emoji.
4. Subtitles: MyHandwriting.ttf in #FF8400 Orange with 7px solid black outline & multi-angle shadow.
   - Dynamic scaling ensures max width <= 860px (zero edge overflow).
5. Curated Contextual B-Rolls: Business, startup documents, craftsmanship, market crowds, and golden sunrise.
6. Pro Audio: Dialogue normalized to -14.0 LUFS (-1.0 dBTP) with ducked BGM at -23 dB.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

import Cocoa
from Cocoa import NSImage, NSColor, NSRectFill, NSFont, NSAttributedString, NSString
from Cocoa import NSForegroundColorAttributeName, NSFontAttributeName, NSBitmapImageRep

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/IMG_6596.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

BROLL_DIR = WORKSPACE / "assets" / "brolls"
BGM_FLUTE = WORKSPACE / "assets" / "audio" / "ramayan_flute_bgm.mp3"
FONT_PATH = WORKSPACE / "assets" / "fonts" / "MyHandwriting.ttf"

WIDTH = 1080
HEIGHT = 1920
BANNER_Y = 408
BANNER_H = 150
VIDEO_Y = 558
VIDEO_H = 940
SUBS_Y = 1260
SUBS_H = 180

COLOR_ORANGE_RGBA = (255, 132, 0, 255) # Signature #FF8400
COLOR_BLACK = (0, 0, 0, 255)

# Cinematic warm studio grade
COLOR_GRADE = (
    "curves=master='0/0.02 0.5/0.52 1/0.98',"
    "eq=contrast=1.16:saturation=1.25:brightness=0.015,"
    "colorbalance=rs=0.04:gs=0.02:bs=-0.04,"
    "unsharp=5:5:0.6:5:5:0.0"
)
SDR_FILTER = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,format=yuv420p"

CROPS = {
    "host": "crop=2010:1750:1650:300,scale=1080:940:flags=lanczos",
    "host_punch": "crop=1748:1522:1780:414,scale=1080:940:flags=lanczos",
    "guest": "crop=2010:1750:200:300,scale=1080:940:flags=lanczos",
    "punch": "crop=1748:1522:330:414,scale=1080:940:flags=lanczos",
    "wide": "crop=2480:2160:680:0,scale=1080:940:flags=lanczos",
}

def generate_header_banner(title_text, out_png):
    im = NSImage.alloc().initWithSize_((WIDTH, BANNER_H))
    im.lockFocus()
    
    # Fill #FF8400 Signature Orange in sRGB
    NSColor.colorWithSRGBRed_green_blue_alpha_(255.0/255.0, 132.0/255.0, 0.0/255.0, 1.0).set()
    NSRectFill(Cocoa.NSMakeRect(0, 0, WIDTH, BANNER_H))
    
    # 3px black borders
    NSColor.blackColor().set()
    NSRectFill(Cocoa.NSMakeRect(0, 0, WIDTH, 3))
    NSRectFill(Cocoa.NSMakeRect(0, BANNER_H - 3, WIDTH, 3))
    
    # Title Text in bold black
    font = NSFont.boldSystemFontOfSize_(56.0)
    attrs = {
        NSFontAttributeName: font,
        NSForegroundColorAttributeName: NSColor.blackColor()
    }
    astr = NSAttributedString.alloc().initWithString_attributes_(title_text, attrs)
    str_sz = astr.size()
    
    # Center text horizontally & vertically
    tx = (WIDTH - str_sz.width) / 2.0
    ty = (BANNER_H - str_sz.height) / 2.0
    astr.drawAtPoint_(Cocoa.NSMakePoint(tx, ty))
    
    im.unlockFocus()
    rep = NSBitmapImageRep.imageRepWithData_(im.TIFFRepresentation())
    png_data = rep.representationUsingType_properties_(Cocoa.NSPNGFileType, {})
    png_data.writeToFile_atomically_(str(out_png), True)
    print(f"✅ Header banner created: {out_png}")

def generate_subtitles_mov(words_list, total_dur, out_mov):
    fps = 30
    total_frames = int(total_dur * fps)
    dummy = Image.new("RGBA", (1, 1))
    draw_dummy = ImageDraw.Draw(dummy)
    
    cache = {}
    for w in words_list:
        word = w["word"].strip()
        if word not in cache:
            sz = 78
            f = ImageFont.truetype(str(FONT_PATH), sz)
            bbox = draw_dummy.textbbox((0, 0), word, font=f)
            tw = bbox[2] - bbox[0]
            while tw > 860 and sz > 36:
                sz -= 2
                f = ImageFont.truetype(str(FONT_PATH), sz)
                bbox = draw_dummy.textbbox((0, 0), word, font=f)
                tw = bbox[2] - bbox[0]
                
            im = Image.new("RGBA", (WIDTH, SUBS_H), (0, 0, 0, 0))
            draw = ImageDraw.Draw(im)
            th = bbox[3] - bbox[1]
            x = (WIDTH - tw) // 2
            y = (SUBS_H - th) // 2 - 5
            
            # 8-direction shadow
            for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (0, -4), (4, 0), (-4, 0)]:
                draw.text((x + dx, y + dy), word, font=f, fill=(0, 0, 0, 200), stroke_width=6, stroke_fill=COLOR_BLACK)
            # Main #FF8400 text with 7px solid black stroke
            draw.text((x, y), word, font=f, fill=COLOR_ORANGE_RGBA, stroke_width=7, stroke_fill=COLOR_BLACK)
            cache[word] = im.tobytes()
            
    empty_frame = Image.new("RGBA", (WIDTH, SUBS_H), (0, 0, 0, 0)).tobytes()
    
    p = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{SUBS_H}", "-r", str(fps),
        "-i", "-", "-c:v", "png", "-r", str(fps), str(out_mov)
    ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for f_idx in range(total_frames):
        t = f_idx / fps
        active_word = None
        for w in words_list:
            if w["start"] <= t <= w["end"]:
                active_word = w["word"].strip()
                break
        if active_word and active_word in cache:
            p.stdin.write(cache[active_word])
        else:
            p.stdin.write(empty_frame)
            
    p.stdin.close()
    p.wait()
    print(f"✅ Subtitles track generated: {out_mov}")

def render_reel(reel_id, title, raw_base_ss, total_dur, cut_specs, words_list, out_mp4):
    print("\n" + "=" * 65)
    print(f"🎬 RENDERING REEL {reel_id}: {title} ({total_dur}s)")
    print(f"Master Export: {out_mp4}")
    print("=" * 65)
    
    # 1. Header Banner
    banner_png = WORKSPACE / f"ref11_banner_reel{reel_id}.png"
    generate_header_banner(title, banner_png)
    
    # 2. Render Cuts
    cut_files = []
    concat_list = WORKSPACE / f"ref11_cuts_concat_{reel_id}.txt"
    
    for idx, cut in enumerate(cut_specs):
        out_cut = WORKSPACE / f"ref11_cut_{reel_id}_{idx}.mp4"
        cut_files.append(out_cut)
        
        dur = cut["dur"]
        t_st = cut["timeline_st"]
        raw_ss = raw_base_ss + t_st
        
        if cut["type"] == "broll":
            vf = f"scale=1080:940:force_original_aspect_ratio=increase,crop=1080:940,fps=30,setsar=1,{COLOR_GRADE},{SDR_FILTER}"
            cmd = [
                "ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}", "-stream_loop", "-1",
                "-i", str(cut["broll"]),
                "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                str(out_cut)
            ]
        else:
            crop = CROPS[cut["type"]]
            if cut.get("bw_hook"):
                vf = f"{crop},hue=s='if(lt(t,0.6),0,1)',{COLOR_GRADE},{SDR_FILTER},fps=30,setsar=1"
            else:
                vf = f"{crop},{COLOR_GRADE},{SDR_FILTER},fps=30,setsar=1"
                
            cmd = [
                "ffmpeg", "-y", "-ss", f"{raw_ss:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                str(out_cut)
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    with open(concat_list, "w") as f:
        for c in cut_files:
            f.write(f"file '{c.resolve()}'\n")
            
    video_track = WORKSPACE / f"ref11_video_track_{reel_id}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-vf", f"pad={WIDTH}:{HEIGHT}:0:{VIDEO_Y}:color=black,{SDR_FILTER}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(video_track)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Video track assembled: {video_track}")
    
    # 3. Audio Mastering (-14 LUFS, ducked BGM)
    raw_audio = WORKSPACE / f"ref11_raw_audio_{reel_id}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-ss", f"{raw_base_ss:.3f}", "-t", f"{total_dur:.3f}",
        "-i", str(RAW_VIDEO),
        "-vn", "-ac", "2", "-ar", "48000", str(raw_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    pro_audio = WORKSPACE / f"ref11_pro_audio_{reel_id}.wav"
    filter_audio = (
        f"[1:a]volume=0.07,aloop=loop=-1:size=2e+09,afade=t=in:st=0:d=1.5,afade=t=out:st={total_dur-2.0}:d=2.0[bgm];"
        f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,"
        f"loudnorm=I=-14.0:TP=-1.0:LRA=11[aout]"
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_audio), "-i", str(BGM_FLUTE),
        "-filter_complex", filter_audio, "-map", "[aout]",
        "-c:a", "pcm_s16le", str(pro_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Master Pro Audio engineered (-14 LUFS): {pro_audio}")
    
    # 4. Subtitles Track
    subs_mov = WORKSPACE / f"ref11_subs_{reel_id}.mov"
    generate_subtitles_mov(words_list, total_dur, subs_mov)
    
    # 5. Final Composite
    print("🎬 Compositing Master Reel in strict SDR BT.709...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(video_track),
        "-loop", "1", "-i", str(banner_png),
        "-i", str(subs_mov),
        "-i", str(pro_audio),
        "-filter_complex",
        f"[0:v][1:v]overlay=0:{BANNER_Y}:shortest=1[v_banner];"
        f"[v_banner][2:v]overlay=0:{SUBS_Y}:shortest=1,{SDR_FILTER}[v]",
        "-map", "[v]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "256k", "-shortest",
        str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"🎉 MASTER REEL {reel_id} DELIVERED: {out_mp4}")
    
    # QA Frames
    for snap_t in [5.0, 15.0, 30.0, total_dur - 5.0]:
        frame_out = FRAMES_DIR / f"qa_reel_{reel_id}_t{snap_t:.1f}s.png"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{snap_t:.1f}", "-i", str(out_mp4),
            "-vframes", "1", str(frame_out)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"📸 QA verification frames extracted for Reel {reel_id}")

# ==============================================================================
# SPEECH-LOCKED DEFINITIONS FOR THE 4 REELS
# ==============================================================================

REELS_CONFIG = [
    # --------------------------------------------------------------------------
    # REEL 1: Student to Founder 🚀
    # Raw Window: 176.0s to 236.0s (60.0s)
    # --------------------------------------------------------------------------
    {
        "id": 1,
        "title": "Student to Founder 🚀",
        "raw_base_ss": 176.0,
        "total_dur": 60.0,
        "out_mp4": EXPORT_DIR / "Reel_6596_1_Student_To_Founder.mp4",
        "cuts": [
            {"type": "host",  "timeline_st": 0.0,  "dur": 2.0, "broll": None, "bw_hook": True},
            {"type": "guest", "timeline_st": 2.0,  "dur": 1.5, "broll": None},
            {"type": "host",  "timeline_st": 3.5,  "dur": 8.5, "broll": None},
            {"type": "guest", "timeline_st": 12.0, "dur": 6.5, "broll": None},
            {"type": "punch", "timeline_st": 18.5, "dur": 3.1, "broll": None},
            {"type": "broll", "timeline_st": 21.6, "dur": 6.6, "broll": BROLL_DIR / "broll_business.mp4"},
            {"type": "punch", "timeline_st": 28.2, "dur": 4.3, "broll": None},
            {"type": "guest", "timeline_st": 32.5, "dur": 10.0, "broll": None},
            {"type": "host",  "timeline_st": 42.5, "dur": 3.7, "broll": None},
            {"type": "guest", "timeline_st": 46.2, "dur": 6.3, "broll": None},
            {"type": "host",  "timeline_st": 52.5, "dur": 1.7, "broll": None},
            {"type": "punch", "timeline_st": 54.2, "dur": 2.6, "broll": None},
            {"type": "broll", "timeline_st": 56.8, "dur": 3.2, "broll": BROLL_DIR / "broll_golden_sunrise.mp4"},
        ],
        "words": [
            {"start": 0.1, "end": 1.5, "word": "GANESH BRO WELCOME!"},
            {"start": 2.0, "end": 3.0, "word": "SUPER BRO FINE!"},
            {"start": 3.6, "end": 8.0, "word": "TELL YOUR QUICK INTRO"},
            {"start": 8.3, "end": 11.5, "word": "WHO ARE YOU?"},
            {"start": 12.7, "end": 15.5, "word": "MY NAME IS GANESH"},
            {"start": 16.4, "end": 19.3, "word": "COLLEGE 2ND YEAR"},
            {"start": 19.7, "end": 21.2, "word": "ZERO IDEA & KNOWLEDGE"},
            {"start": 21.8, "end": 24.5, "word": "RESEARCH ON SOCIAL MEDIA"},
            {"start": 24.8, "end": 27.2, "word": "STARTED MY RESEARCH"},
            {"start": 27.3, "end": 29.9, "word": "MET LOKESH BRO!"},
            {"start": 30.1, "end": 35.8, "word": "CONNECTED ON PODCAST"},
            {"start": 36.1, "end": 38.9, "word": "TALKED ABOUT MENTORING"},
            {"start": 39.1, "end": 40.5, "word": "DISCUSSED STARTUP PLANS"},
            {"start": 41.0, "end": 42.0, "word": "SUPER!"},
            {"start": 42.9, "end": 46.2, "word": "BUSINESS STARTED AH?"},
            {"start": 46.3, "end": 48.5, "word": "BUSINESS START PANNITOM!"},
            {"start": 49.7, "end": 52.4, "word": "COMPANY REGISTERED"},
            {"start": 52.5, "end": 54.2, "word": "PROPRIETARY AH?"},
            {"start": 54.3, "end": 56.5, "word": "PRIVATE LIMITED COMPANY!"},
            {"start": 57.0, "end": 59.5, "word": "COLLEGE-LA PRIVATE LIMITED!"}
        ]
    },
    # --------------------------------------------------------------------------
    # REEL 2: Why Register Pvt Ltd? 🏢
    # Raw Window: 236.0s to 296.0s (60.0s)
    # --------------------------------------------------------------------------
    {
        "id": 2,
        "title": "Why Register Pvt Ltd? 🏢",
        "raw_base_ss": 236.0,
        "total_dur": 60.0,
        "out_mp4": EXPORT_DIR / "Reel_6596_2_Business_Vs_Startup.mp4",
        "cuts": [
            {"type": "host",  "timeline_st": 0.0,  "dur": 2.5, "broll": None, "bw_hook": True},
            {"type": "guest", "timeline_st": 2.5,  "dur": 4.0, "broll": None},
            {"type": "host",  "timeline_st": 6.5,  "dur": 2.0, "broll": None},
            {"type": "guest", "timeline_st": 8.5,  "dur": 3.5, "broll": None},
            {"type": "host",  "timeline_st": 12.0, "dur": 1.5, "broll": None},
            {"type": "guest", "timeline_st": 13.5, "dur": 2.5, "broll": None},
            {"type": "broll", "timeline_st": 16.0, "dur": 6.0, "broll": BROLL_DIR / "broll_business.mp4"},
            {"type": "guest", "timeline_st": 22.0, "dur": 9.0, "broll": None},
            {"type": "host",  "timeline_st": 31.0, "dur": 2.0, "broll": None},
            {"type": "punch", "timeline_st": 33.0, "dur": 8.0, "broll": None},
            {"type": "broll", "timeline_st": 41.0, "dur": 5.5, "broll": BROLL_DIR / "broll_watch_repair.mp4"},
            {"type": "host_punch", "timeline_st": 46.5, "dur": 13.5, "broll": None},
        ],
        "words": [
            {"start": 0.1, "end": 1.5, "word": "WHO ADVISED PVT LTD?"},
            {"start": 3.2, "end": 5.8, "word": "FIRST WE THOUGHT LLP"},
            {"start": 6.9, "end": 7.8, "word": "WHAT IS LLP?"},
            {"start": 9.6, "end": 11.5, "word": "LIMITED LIABILITY PARTNERSHIP"},
            {"start": 12.1, "end": 13.1, "word": "HOW MANY PARTNERS?"},
            {"start": 13.3, "end": 15.3, "word": "TWO PARTNERS REQUIRED"},
            {"start": 16.8, "end": 21.0, "word": "LLP VS PRIVATE LIMITED"},
            {"start": 21.3, "end": 23.5, "word": "AUDIT & COMPLIANCE RULES"},
            {"start": 24.8, "end": 28.5, "word": "DOCUMENTATION PROCESS"},
            {"start": 29.6, "end": 32.7, "word": "WHAT IS THE BENEFIT?"},
            {"start": 33.1, "end": 37.3, "word": "WHEN RAISING FUNDING"},
            {"start": 37.5, "end": 40.5, "word": "INVESTORS PREFER PVT LTD!"},
            {"start": 42.7, "end": 45.5, "word": "HUGE ADVANTAGE FOR SCALING"},
            {"start": 46.6, "end": 47.3, "word": "SUPER!"},
            {"start": 47.6, "end": 50.8, "word": "START REAL COMPANY FROM COLLEGE"},
            {"start": 51.1, "end": 54.2, "word": "START A REAL BUSINESS"},
            {"start": 54.5, "end": 59.5, "word": "BUILT FOR BIG GROWTH!"}
        ]
    },
    # --------------------------------------------------------------------------
    # REEL 3: Business vs Entrepreneur 💡
    # Raw Window: 296.0s to 356.0s (60.0s)
    # --------------------------------------------------------------------------
    {
        "id": 3,
        "title": "Business vs Entrepreneur 💡",
        "raw_base_ss": 296.0,
        "total_dur": 60.0,
        "out_mp4": EXPORT_DIR / "Reel_6596_3_Revenue_Vs_Profit.mp4",
        "cuts": [
            {"type": "host",  "timeline_st": 0.0,  "dur": 5.0, "broll": None, "bw_hook": True},
            {"type": "guest", "timeline_st": 5.0,  "dur": 11.0, "broll": None},
            {"type": "host",  "timeline_st": 16.0, "dur": 3.5, "broll": None},
            {"type": "broll", "timeline_st": 19.5, "dur": 6.5, "broll": BROLL_DIR / "broll_crowd_promenade.mp4"},
            {"type": "guest", "timeline_st": 26.0, "dur": 10.5, "broll": None},
            {"type": "host",  "timeline_st": 36.5, "dur": 2.5, "broll": None},
            {"type": "host",  "timeline_st": 39.0, "dur": 10.0, "broll": None},
            {"type": "broll", "timeline_st": 49.0, "dur": 5.0, "broll": BROLL_DIR / "broll_clock.mp4"},
            {"type": "host_punch", "timeline_st": 54.0, "dur": 6.0, "broll": None},
        ],
        "words": [
            {"start": 0.1, "end": 1.4, "word": "FIRST BIG QUESTION"},
            {"start": 2.4, "end": 4.6, "word": "WANT TO BE A BUSINESSMAN?"},
            {"start": 6.1, "end": 7.8, "word": "I AM A BUSINESSMAN"},
            {"start": 8.3, "end": 10.5, "word": "FOCUS ON BRAND VALUE"},
            {"start": 10.8, "end": 13.5, "word": "NOT JUST MAKING MONEY"},
            {"start": 13.6, "end": 15.5, "word": "WANT TO BE A REAL FOUNDER"},
            {"start": 17.0, "end": 18.8, "word": "HOW DO YOU LOOK AT BRAND?"},
            {"start": 20.8, "end": 24.5, "word": "SOLVING CUSTOMER NEEDS"},
            {"start": 27.5, "end": 35.5, "word": "BRAND IS REPUTATION & TRUST"},
            {"start": 36.5, "end": 37.5, "word": "EXACTLY!"},
            {"start": 39.7, "end": 43.0, "word": "BUSINESS VS ENTREPRENEUR!"},
            {"start": 43.6, "end": 48.8, "word": "BUSINESSMAN WORKS EXISTING MODEL"},
            {"start": 49.1, "end": 54.0, "word": "REPLICATES EXISTING REVENUE"},
            {"start": 54.3, "end": 56.0, "word": "ENTREPRENEUR IS DIFFERENT"},
            {"start": 56.1, "end": 59.8, "word": "ENTREPRENEUR SOLVES UNSEEN PROBLEMS!"}
        ]
    },
    # --------------------------------------------------------------------------
    # REEL 4: Venture vs Traditional Trade 🚀
    # Raw Window: 356.0s to 416.0s (60.0s)
    # --------------------------------------------------------------------------
    {
        "id": 4,
        "title": "Venture vs Traditional Trade 🚀",
        "raw_base_ss": 356.0,
        "total_dur": 60.0,
        "out_mp4": EXPORT_DIR / "Reel_6596_4_Service_To_Scale.mp4",
        "cuts": [
            {"type": "guest", "timeline_st": 0.0,  "dur": 6.0, "broll": None, "bw_hook": True},
            {"type": "host",  "timeline_st": 6.0,  "dur": 7.5, "broll": None},
            {"type": "punch", "timeline_st": 13.5, "dur": 6.5, "broll": None},
            {"type": "broll", "timeline_st": 20.0, "dur": 6.0, "broll": BROLL_DIR / "broll_business.mp4"},
            {"type": "guest", "timeline_st": 26.0, "dur": 8.0, "broll": None},
            {"type": "punch", "timeline_st": 34.0, "dur": 8.5, "broll": None},
            {"type": "host",  "timeline_st": 42.5, "dur": 5.0, "broll": None},
            {"type": "broll", "timeline_st": 47.5, "dur": 6.0, "broll": BROLL_DIR / "broll_golden_sunrise.mp4"},
            {"type": "punch", "timeline_st": 53.5, "dur": 6.5, "broll": None},
        ],
        "words": [
            {"start": 0.1, "end": 2.9, "word": "NO EXISTING PRODUCT"},
            {"start": 3.4, "end": 5.8, "word": "FIRST-MOVER INNOVATION"},
            {"start": 6.6, "end": 10.5, "word": "CREATING NEW VALUE"},
            {"start": 14.4, "end": 22.0, "word": "INNOVATION IN WHOLE BUSINESS"},
            {"start": 22.5, "end": 25.8, "word": "IT BECOMES A VENTURE!"},
            {"start": 26.5, "end": 32.0, "word": "SOLVING PROBLEMS AT PROFIT"},
            {"start": 32.4, "end": 34.2, "word": "TRADITIONAL BUSINESS NO INNOVATION"},
            {"start": 34.6, "end": 38.5, "word": "VALUE RETURN IS LINEAR"},
            {"start": 38.9, "end": 42.5, "word": "NOT EXPONENTIALLY HIGH"},
            {"start": 47.2, "end": 50.5, "word": "NEW SOLUTION FOR REAL PAIN"},
            {"start": 50.6, "end": 56.0, "word": "SOLVING EXPONENTIALLY BIG PROBLEMS"},
            {"start": 56.5, "end": 59.5, "word": "EXPONENTIALLY HIGH VALUE!"}
        ]
    }
]

def main():
    print("=" * 70)
    print("🚀 BATCH RENDERING 4 REELS FROM IMG_6596.MOV IN REFERENCE 11 STYLE")
    print("=" * 70)
    t_start = time.time()
    for cfg in REELS_CONFIG:
        render_reel(
            reel_id=cfg["id"],
            title=cfg["title"],
            raw_base_ss=cfg["raw_base_ss"],
            total_dur=cfg["total_dur"],
            cut_specs=cfg["cuts"],
            words_list=cfg["words"],
            out_mp4=cfg["out_mp4"]
        )
    print("\n" + "=" * 70)
    print(f"🎉 ALL 4 REELS COMPLETED IN {time.time() - t_start:.2f}s!")
    print("=" * 70)

if __name__ == "__main__":
    main()
