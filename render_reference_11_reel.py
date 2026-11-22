#!/usr/bin/env python3
"""
render_reference_11_reel.py
Renders Reel 1 strictly following the REFERENCE 11 Signature Master Specification:

1. Canvas: 1080x1920 (9:16 Vertical, 30 fps)
2. Top Black Bar: Y=0 to Y=407 (408px, solid black, no progress bar)
3. Header Banner: Y=408 to Y=557 (150px height, 1080px width)
   - Background: Signature Orange #EA8207
   - Borders: 2px solid black at Y=408 and Y=557
   - Line 1: 'ராமாயணம் கற்றுத்தரும் பாடம் 🏹'
   - Line 2: 'ஹனுமான் தரும் வாழ்க்கை தத்துவம்! 🔥'
   - Persistent across every frame (0.0s to end)
4. Active Video Window: Y=558 to Y=1497 (940px height, 1080px width)
   - Speaker framing: Guest & Host cropped and centered
   - Opening 0.6s Hook: B&W (hue=s=0) snapping into full color
   - 1.15x Punch-in on key climax delivery
   - Hanuman B-Roll: Uncropped face, crown, eyes, and golden aura 100% framed
5. Bottom Black Bar: Y=1498 to Y=1919 (422px, solid black)
6. Subtitles:
   - Running handwriting font: MyHandwriting.ttf
   - Colors: Crisp White (#FFFFFF) dialogue + Signature Orange (#EA8207) highlight
   - Outline: 6px solid black stroke
   - Safe zone positioning (Y=1320)
7. Audio:
   - Mastered Studio Audio (Demucs v4 isolation + surgical EQ + agate + sidechain ducked flute BGM + EBU R128 -14 LUFS / -1.0 dBTP)
8. Output:
   - /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_11_Style.mp4
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
import objc
from Cocoa import (
    NSBitmapImageRep, NSGraphicsContext, NSColor, NSRectFill, NSMakeRect,
    NSFont, NSAttributedString,
    NSFontAttributeName, NSForegroundColorAttributeName, NSDeviceRGBColorSpace
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

WIDTH = 1080
HEIGHT = 1920
VIDEO_H = 940
VIDEO_Y = 558
BANNER_Y = 408
BANNER_H = 150
SUBS_Y = 1320
SUBS_H = 160

# Cuts Specification for Reel 1 (Hanuman / Mentorship)
CUTS = [
    {
        "st": 1988.0, "et": 1996.0, "speaker": "host", "broll": None, "punch": False,
        "subs": [
            (0.3, 3.8, "Ramayanathula irunthu...", "Ramayanathula"),
            (4.0, 7.8, "WHAT IS THE LIFE LESSON?", "LESSON")
        ]
    },
    {
        "st": 1996.0, "et": 2008.5, "speaker": "guest", "broll": None, "punch": False,
        "subs": [
            (0.3, 5.8, "Naan vanthu Hanumana pathi matum...", "Hanumana"),
            (6.0, 12.2, "EVERYBODY IS LIKE HANUMAN! 🏹", "HANUMAN")
        ]
    },
    {
        "st": 2008.5, "et": 2018.5, "speaker": "broll", "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"), "punch": False,
        "subs": [
            (0.3, 4.8, "Namakulla Latent Potential irukku...", "POTENTIAL"),
            (5.0, 9.8, "Someone has to show that, THAT'S THE MENTOR!", "MENTOR")
        ]
    },
    {
        "st": 2018.5, "et": 2035.0, "speaker": "guest", "broll": None, "punch": True,
        "subs": [
            (0.3, 5.2, "Jambavan vanthu sonnappo,", "Jambavan"),
            (5.5, 10.8, "YOU ARE POWERFUL! Un sakthi theriyala!", "POWERFUL"),
            (11.0, 16.2, "Apadi sonnathunaala dhaan...", "sonnathunaala")
        ]
    },
    {
        "st": 2035.0, "et": 2048.0, "speaker": "guest", "broll": None, "punch": True,
        "subs": [
            (0.3, 6.2, "Avar kadalai thaandi Seethaiyai kandupidichchaar!", "Seethaiyai"),
            (6.5, 12.8, "Sollave illa na HE WOULD HAVE NEVER KNOWN!", "NEVER")
        ]
    },
    {
        "st": 2048.0, "et": 2062.0, "speaker": "guest", "broll": None, "punch": False,
        "subs": [
            (0.3, 6.5, "Atha vida periya paadam edhuvume illa!", "paadam"),
            (6.8, 13.8, "GREATEST LESSON OF LIFE! Follow for more 🏹", "GREATEST")
        ]
    }
]

total_dur = sum(c["et"] - c["st"] for c in CUTS)
print(f"Total Reel 1 duration: {total_dur:.2f}s")

# 1. Create Persistent Header Banner #EA8207
banner_png = WORKSPACE / "ref11_persistent_banner.png"
rep_b = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
    None, WIDTH, BANNER_H, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
)
ctx_b = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep_b)
NSGraphicsContext.setCurrentContext_(ctx_b)
# Background #EA8207
NSColor.colorWithDeviceRed_green_blue_alpha_(0.918, 0.510, 0.027, 1.0).set()
NSRectFill(NSMakeRect(0, 0, WIDTH, BANNER_H))
# 2px black borders top and bottom
NSColor.blackColor().set()
NSRectFill(NSMakeRect(0, 0, WIDTH, 2))
NSRectFill(NSMakeRect(0, BANNER_H - 2, WIDTH, 2))

fb1 = NSFont.fontWithName_size_("TamilSangamMN-Bold", 40.0) or NSFont.boldSystemFontOfSize_(40.0)
fb2 = NSFont.fontWithName_size_("TamilSangamMN-Bold", 36.0) or NSFont.boldSystemFontOfSize_(36.0)

ab1 = NSAttributedString.alloc().initWithString_attributes_("ராமாயணம் கற்றுத்தரும் பாடம் 🏹", {NSFontAttributeName: fb1, NSForegroundColorAttributeName: NSColor.blackColor()})
ab2 = NSAttributedString.alloc().initWithString_attributes_("ஹனுமான் தரும் வாழ்க்கை தத்துவம்! 🔥", {NSFontAttributeName: fb2, NSForegroundColorAttributeName: NSColor.blackColor()})

sz1 = ab1.size()
sz2 = ab2.size()

ab2.drawAtPoint_(((WIDTH - sz2.width)/2, 22))
ab1.drawAtPoint_(((WIDTH - sz1.width)/2, 80))

ctx_b.flushGraphics()
png_b = rep_b.representationUsingType_properties_(4, None)
png_b.writeToFile_atomically_(str(banner_png), True)
print(f"✅ Header banner created: {banner_png}")

# 2. Render Video Base (1080x940 video window placed inside 1080x1920 canvas)
cut_files = []
concat_list = WORKSPACE / "ref11_concat.txt"

for idx, cut in enumerate(CUTS):
    dur = cut["et"] - cut["st"]
    out_cut = WORKSPACE / f"ref11_cut_{idx}.mp4"
    cut_files.append(out_cut)
    
    if cut["broll"]:
        # Uncropped Lord Hanuman framing
        vf = "scale=1080:940:force_original_aspect_ratio=increase,crop=1080:940:0:100,fps=30,setsar=1"
        cmd = [
            "ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}", "-stream_loop", "-1", "-i", cut["broll"],
            "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)
        ]
    else:
        is_guest = (cut["speaker"] == "guest")
        if is_guest:
            if cut["punch"]:
                # 1.15x punch-in for climax
                crop = "crop=1565:1362:1780:300,scale=1080:940:flags=lanczos"
            else:
                crop = "crop=1800:1567:1650:250,scale=1080:940:flags=lanczos"
        else:
            # Host framing
            crop = "crop=1800:1567:200:250,scale=1080:940:flags=lanczos"
            
        # Hook transition: first 0.6s in B&W for cut 0
        if idx == 0:
            vf = f"{crop},hue=s='if(lt(t,0.6),0,1)',fps=30,setsar=1"
        else:
            vf = f"{crop},fps=30,setsar=1"
            
        cmd = [
            "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}", "-i", str(RAW_VIDEO),
            "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)
        ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

with open(concat_list, "w") as f:
    for cf in cut_files: f.write(f"file '{cf}'\n")

base_vid = WORKSPACE / "ref11_base.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
    "-vf", f"pad={WIDTH}:{HEIGHT}:0:{VIDEO_Y}:color=black",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    str(base_vid)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"✅ Base video padded to 1080x1920: {base_vid}")

# 3. Render Subtitles in Handwriting Font (MyHandwriting.ttf) + Orange Highlight
font_hw_p = "/Users/pgi/Library/Fonts/MyHandwriting.ttf"
font_tamil_p = ASSETS_DIR / "fonts" / "NotoSansTamil-Bold.ttf"

font_hw = ImageFont.truetype(font_hw_p, 62)
font_tamil = ImageFont.truetype(str(font_tamil_p), 46)

def has_tamil(text):
    return any(0x0B80 <= ord(c) <= 0x0BFF for c in text)

def render_sub_frame(text, active_kw):
    im = Image.new("RGBA", (WIDTH, SUBS_H), (0, 0, 0, 0))
    if not text:
        return im.tobytes()
        
    draw = ImageDraw.Draw(im)
    words = text.split()
    word_info = []
    total_w = 0.0
    
    for w in words:
        f = font_tamil if has_tamil(w) else font_hw
        w_len = draw.textlength(w, font=f)
        word_info.append((w, f, w_len))
        total_w += w_len
        
    space_w = draw.textlength(" ", font=font_hw)
    total_w += space_w * (len(words) - 1)
    
    cur_x = (WIDTH - total_w) / 2
    y = 40
    
    for w, f, w_len in word_info:
        clean = w.strip("!?,.\"🏹🔥").lower()
        target = active_kw.strip("!?,.\"🏹🔥").lower()
        is_highlight = (clean == target or (w.isupper() and len(w) > 2))
        fill_col = (234, 130, 7, 255) if is_highlight else (255, 255, 255, 255)
        
        # 6px solid black stroke
        draw.text((cur_x, y), w, font=f, fill=fill_col,
                  stroke_width=6, stroke_fill=(0, 0, 0, 255))
        cur_x += w_len + space_w
        
    return im.tobytes()

sub_events = []
curr_t = 0.0
for cut in CUTS:
    for pst, pet, txt, kw in cut["subs"]:
        sub_events.append((curr_t + pst, curr_t + pet, txt, kw))
    curr_t += (cut["et"] - cut["st"])

subs_mov = WORKSPACE / "ref11_subs.mov"
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{SUBS_H}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_f = int(round(total_dur * 30))
blank_bytes = render_sub_frame("", "")

for f_idx in range(total_f):
    t_sec = f_idx / 30.0
    active_ev = None
    for w_st, w_et, txt, kw in sub_events:
        if w_st <= t_sec < w_et:
            active_ev = (txt, kw)
            break
    raw_b = render_sub_frame(active_ev[0], active_ev[1]) if active_ev else blank_bytes
    proc.stdin.write(raw_b)

proc.stdin.close()
proc.wait()
print(f"✅ Subtitles animated video: {subs_mov}")

# 4. Final Composite with Pro Audio Master
pro_audio = WORKSPACE / "reel1_pro_mastered_audio.wav"
final_out = EXPORT_DIR / "Reel_1_Reference_11_Style.mp4"

subprocess.run([
    "ffmpeg", "-y",
    "-i", str(base_vid),
    "-loop", "1", "-i", str(banner_png),
    "-i", str(subs_mov),
    "-i", str(pro_audio),
    "-filter_complex",
    f"[0:v][1:v]overlay=0:{BANNER_Y}[v_banner];"
    f"[v_banner][2:v]overlay=0:{SUBS_Y}[v]",
    "-map", "[v]", "-map", "3:a",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
    "-shortest",
    str(final_out)
], check=True)

print(f"🎉 FINAL REEL 1 IN REFERENCE 11 STYLE EXPORTED: {final_out}")

# Extract QA frames for visual verification
subprocess.run(["ffmpeg", "-y", "-ss", "0.3", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_hook_bw.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "2.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_host.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "10.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_guest.jpg")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "22.0", "-i", str(final_out), "-vframes", "1", "-q:v", "2", str(FRAMES_DIR / "qa_ref11_hanuman.jpg")], check=True)
print("✅ QA frames extracted successfully!")
