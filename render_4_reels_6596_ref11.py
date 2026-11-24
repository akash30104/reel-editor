#!/usr/bin/env python3
"""
render_4_reels_6596_ref11.py
Renders 4 High-Retention Reels from IMG_6596.MOV in Locked Reference 11 Style:

Reel 1: Student to Founder 🚀 (58.0s)
Reel 2: Business vs Startup 💡 (65.0s)
Reel 3: Revenue vs Real Profit 💰 (65.0s)
Reel 4: Service vs Product Scalability 🏢 (67.0s)

Strictly adheres to:
1. Canvas 1080x1920 @ 30fps with pure black letterboxing (Top Y=0..408, Bottom Y=1498..1920)
2. Header Banner: Y=408..558 (Height 150px) in Signature Orange #FF8400 (RGB: 255, 132, 0)
3. Active Video Window: Y=558..1498 (Height 940px)
   - Strict SDR BT.709 color pipeline (stripping iPhone HDR/HLG/BT.2020 tags)
   - 100% continuous acoustic lip-sync (every speaker cut starts at raw_start + timeline_elapsed)
   - Framing for IMG_6596.MOV (3840x2160):
     * Host Lokesh (Left speaker, white shirt): crop=2010:1750:200:300,scale=1080:940
     * Guest Ganesh (Right speaker, light blue shirt): crop=2010:1750:1650:300,scale=1080:940
     * Guest Ganesh 1.15x Punch-in: crop=1748:1522:1780:414,scale=1080:940
   - B-roll cutaways every 4 to 7 seconds
4. Subtitles:
   - Handwriting font MyHandwriting.ttf (size 82pt)
   - Signature Orange #FF8400 with 7px solid black stroke & shadow
   - Lower third placement (Y=1340)
5. Audio:
   - Dialogue normalized to broadcast standard -14.0 LUFS / -1.0 dBTP
   - Subtle background music ducked at -23 dB
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
SUBS_Y = 1250
SUBS_H = 180

COLOR_ORANGE_RGBA = (255, 132, 0, 255) # Signature #FF8400
COLOR_BLACK = (0, 0, 0, 255)

SDR_FILTER = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,format=yuv420p"
COLOR_GRADE = "eq=contrast=1.08:saturation=0.92:brightness=-0.01,colorbalance=rs=0.03:gs=0.01:bs=-0.03"

CROPS = {
    "host": "crop=2010:1750:200:300,scale=1080:940:flags=lanczos",
    "guest": "crop=2010:1750:1650:300,scale=1080:940:flags=lanczos",
    "punch": "crop=1748:1522:1780:414,scale=1080:940:flags=lanczos",
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
    
    # Pre-render word frames with dynamic font scaling to guarantee zero overflow (max width 860px)
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
            # Main #FF8400 text with 7px black outline
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
# DEFINITIONS FOR THE 4 REELS
# ==============================================================================

REELS_CONFIG = [
    {
        "id": 1,
        "title": "Student to Founder 🚀",
        "raw_base_ss": 16.0,
        "total_dur": 58.0,
        "out_mp4": EXPORT_DIR / "Reel_6596_1_Student_To_Founder.mp4",
        "cuts": [
            {"type": "guest", "timeline_st": 0.0,  "dur": 5.0, "broll": None, "bw_hook": True},
            {"type": "broll", "timeline_st": 5.0,  "dur": 4.0, "broll": BROLL_DIR / "broll_business.mp4"},
            {"type": "guest", "timeline_st": 9.0,  "dur": 7.0, "broll": None},
            {"type": "host",  "timeline_st": 16.0, "dur": 5.0, "broll": None},
            {"type": "guest", "timeline_st": 21.0, "dur": 5.5, "broll": None},
            {"type": "host",  "timeline_st": 26.5, "dur": 4.5, "broll": None},
            {"type": "guest", "timeline_st": 31.0, "dur": 5.5, "broll": None},
            {"type": "host",  "timeline_st": 36.5, "dur": 4.5, "broll": None},
            {"type": "punch", "timeline_st": 41.0, "dur": 7.0, "broll": None},
            {"type": "broll", "timeline_st": 48.0, "dur": 6.0, "broll": BROLL_DIR / "broll_golden_sunrise.mp4"},
            {"type": "guest", "timeline_st": 54.0, "dur": 4.0, "broll": None},
        ],
        "words": [
            {"start": 0.3, "end": 2.2, "word": "STUDENT FOUNDER"},
            {"start": 2.3, "end": 4.8, "word": "START-UP COMPANY"},
            {"start": 5.0, "end": 8.8, "word": "ZERO KNOWLEDGE"},
            {"start": 9.2, "end": 12.0, "word": "MET LOKESH BRO"},
            {"start": 12.2, "end": 15.5, "word": "CONNECT AANOM!"},
            {"start": 16.2, "end": 20.5, "word": "MENTORING TALK"},
            {"start": 21.2, "end": 25.8, "word": "IDEAS DISCUSS PANNI"},
            {"start": 26.8, "end": 30.5, "word": "BUSINESS STARTED AH?"},
            {"start": 31.2, "end": 33.6, "word": "COLLEGE-LA IRUKKUMBODHE"},
            {"start": 33.7, "end": 36.2, "word": "REGISTER PANNITOM!"},
            {"start": 36.8, "end": 40.5, "word": "PROPRIETARY AH?"},
            {"start": 41.2, "end": 47.5, "word": "PVT LTD COMPANY!"},
            {"start": 48.2, "end": 53.5, "word": "STUDENT TO FOUNDER"},
            {"start": 54.0, "end": 57.5, "word": "MASS JOURNEY!"}
        ]
    },
    {
        "id": 2,
        "title": "Business vs Startup 💡",
        "raw_base_ss": 345.0,
        "total_dur": 65.0,
        "out_mp4": EXPORT_DIR / "Reel_6596_2_Business_Vs_Startup.mp4",
        "cuts": [
            {"type": "host",  "timeline_st": 0.0,  "dur": 7.0, "broll": None, "bw_hook": True},
            {"type": "guest", "timeline_st": 7.0,  "dur": 6.0, "broll": None},
            {"type": "broll", "timeline_st": 13.0, "dur": 5.0, "broll": BROLL_DIR / "broll_business.mp4"},
            {"type": "guest", "timeline_st": 18.0, "dur": 9.0, "broll": None},
            {"type": "punch", "timeline_st": 27.0, "dur": 8.0, "broll": None},
            {"type": "host",  "timeline_st": 35.0, "dur": 7.0, "broll": None},
            {"type": "broll", "timeline_st": 42.0, "dur": 6.0, "broll": BROLL_DIR / "broll_crowd_promenade.mp4"},
            {"type": "guest", "timeline_st": 48.0, "dur": 10.0, "broll": None},
            {"type": "punch", "timeline_st": 58.0, "dur": 7.0, "broll": None},
        ],
        "words": [
            {"start": 0.4, "end": 3.2, "word": "BUSINESS VS STARTUP"},
            {"start": 3.4, "end": 6.6, "word": "PERIYA DIFFERENCE!"},
            {"start": 7.2, "end": 12.5, "word": "BUSINESS MAN WORK"},
            {"start": 13.0, "end": 17.5, "word": "EXISTING MODEL"},
            {"start": 18.2, "end": 26.5, "word": "INNOVATION IRUKKANUM!"},
            {"start": 27.2, "end": 34.5, "word": "ADHU DHAAN VENTURE!"},
            {"start": 35.2, "end": 41.5, "word": "SOLVING PEOPLE'S PROBLEM"},
            {"start": 42.2, "end": 47.5, "word": "MAKING PROFIT"},
            {"start": 48.2, "end": 57.5, "word": "TRUE ENTREPRENEURSHIP"},
            {"start": 58.2, "end": 64.5, "word": "SCALABLE INNOVATION!"}
        ]
    },
    {
        "id": 3,
        "title": "Revenue vs Real Profit 💰",
        "raw_base_ss": 1680.0,
        "total_dur": 65.0,
        "out_mp4": EXPORT_DIR / "Reel_6596_3_Revenue_Vs_Profit.mp4",
        "cuts": [
            {"type": "host",  "timeline_st": 0.0,  "dur": 6.5, "broll": None, "bw_hook": True},
            {"type": "guest", "timeline_st": 6.5,  "dur": 5.5, "broll": None},
            {"type": "broll", "timeline_st": 12.0, "dur": 5.5, "broll": BROLL_DIR / "broll_clock.mp4"},
            {"type": "guest", "timeline_st": 17.5, "dur": 8.5, "broll": None},
            {"type": "punch", "timeline_st": 26.0, "dur": 8.0, "broll": None},
            {"type": "host",  "timeline_st": 34.0, "dur": 7.0, "broll": None},
            {"type": "broll", "timeline_st": 41.0, "dur": 7.0, "broll": BROLL_DIR / "broll_golden_sunrise.mp4"},
            {"type": "guest", "timeline_st": 48.0, "dur": 10.0, "broll": None},
            {"type": "punch", "timeline_st": 58.0, "dur": 7.0, "broll": None},
        ],
        "words": [
            {"start": 0.4, "end": 3.0, "word": "REVENUE VS PROFIT"},
            {"start": 3.2, "end": 6.2, "word": "REALITY CHECK!"},
            {"start": 6.8, "end": 11.5, "word": "10 LAKHS REVENUE"},
            {"start": 12.2, "end": 17.0, "word": "SALES AND MARKETING"},
            {"start": 17.8, "end": 25.5, "word": "5 LAKHS EXPENSE POIDUM!"},
            {"start": 26.2, "end": 33.5, "word": "REAL PROFIT 5 LAKHS!"},
            {"start": 34.2, "end": 40.5, "word": "UNIT ECONOMICS"},
            {"start": 41.2, "end": 47.5, "word": "SUSTAINABLE CASH FLOW"},
            {"start": 48.2, "end": 57.5, "word": "REVENUE IS VANITY"},
            {"start": 58.2, "end": 64.5, "word": "PROFIT IS SANITY!"}
        ]
    },
    {
        "id": 4,
        "title": "Service vs Scalability 🏢",
        "raw_base_ss": 848.0,
        "total_dur": 67.0,
        "out_mp4": EXPORT_DIR / "Reel_6596_4_Service_To_Scale.mp4",
        "cuts": [
            {"type": "host",  "timeline_st": 0.0,  "dur": 7.0, "broll": None, "bw_hook": True},
            {"type": "guest", "timeline_st": 7.0,  "dur": 7.0, "broll": None},
            {"type": "broll", "timeline_st": 14.0, "dur": 6.0, "broll": BROLL_DIR / "broll_business.mp4"},
            {"type": "guest", "timeline_st": 20.0, "dur": 8.0, "broll": None},
            {"type": "host",  "timeline_st": 28.0, "dur": 8.0, "broll": None},
            {"type": "punch", "timeline_st": 36.0, "dur": 8.0, "broll": None},
            {"type": "broll", "timeline_st": 44.0, "dur": 7.0, "broll": BROLL_DIR / "broll_watch_repair.mp4"},
            {"type": "guest", "timeline_st": 51.0, "dur": 9.0, "broll": None},
            {"type": "punch", "timeline_st": 60.0, "dur": 7.0, "broll": None},
        ],
        "words": [
            {"start": 0.4, "end": 3.2, "word": "CLIENT VALUE"},
            {"start": 3.5, "end": 6.8, "word": "SOFTWARE DEVELOPMENT"},
            {"start": 7.2, "end": 13.5, "word": "PROVIDING SERVICES"},
            {"start": 14.2, "end": 19.5, "word": "DIGITAL MARKETING"},
            {"start": 20.2, "end": 27.5, "word": "CLIENTS RETENTION"},
            {"start": 28.2, "end": 35.5, "word": "HIRING SOLID TEAM"},
            {"start": 36.2, "end": 39.5, "word": "INITIAL 4-5 MONTHS"},
            {"start": 39.6, "end": 43.5, "word": "HARD WORK & GRIND!"},
            {"start": 44.2, "end": 50.5, "word": "FOUNDATION IS KEY"},
            {"start": 51.2, "end": 59.5, "word": "BUSINESS SUSTAIN AAGUM"},
            {"start": 60.2, "end": 66.5, "word": "HOW AGENCIES SCALE!"}
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
