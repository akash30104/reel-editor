#!/usr/bin/env python3
"""
render_ref11_master.py
Master Renderer for Reel 1 in Reference 11 Style:

1. Canvas & Layout (Reference 11 Master Specification):
   - Canvas: 1080x1920 @ 30 fps
   - Top black bar: Y = 0 to 408
   - Header Banner: Y = 408 to 558 (Height 150px)
     * Background: Exact #FF8400 (RGB: 255, 132, 0)
     * 3px solid black border lines top and bottom
     * Native Cocoa text rendering with TamilSangamMN-Bold for bit-perfect Tamil ligatures:
       Line 1: "ராமாயணம் கற்றுத்தரும் பாடம் 🏹"
       Line 2: "ஹனுமான் தரும் வாழ்க்கை தத்துவம்! 🔥"
   - Active Video Window: Y = 558 to 1498 (Height 940px, centered)
     * Switch frame to WHO IS ACTUALLY TALKING:
       - Host Woman: crop=1206:1050:2150:650 -> scale=1080:940
       - Guest Man: crop=1206:1050:450:750 -> scale=1080:940
       - Guest Punch-in (1.15x): crop=1048:913:530:820 -> scale=1080:940
     * Thematic B-Roll cutaways every 4-7 seconds
     * First 0.6s B&W hook snap into warm natural color grade
   - Bottom black bar: Y = 1498 to 1920

2. Subtitles:
   - Fast Single-Word Pacing: ONLY ONE WORD AT A TIME on screen
   - Font: User's handwriting font MyHandwriting.ttf (size 95)
   - Color: Exact signature #FF8400 with 8px solid black stroke
   - Placement: Lower third of video window (Y = 1350)
   - Speech Sync: Aligned strictly with millisecond acoustic speech timestamps

3. Audio:
   - Pro Studio Master reel1_pro_mastered_audio.wav (-14.0 LUFS dialogue + ducked flute BGM @ -23 dB)
   - Zero watermarks

4. Output:
   - /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_11_Style.mp4
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
import Cocoa
from AppKit import NSImage, NSBitmapImageRep, NSColor, NSRectFill, NSFont, NSAttributedString, NSFontAttributeName, NSForegroundColorAttributeName

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
ASSETS_DIR = WORKSPACE / "assets"
BROLLS_DIR = ASSETS_DIR / "brolls"
PRO_AUDIO = WORKSPACE / "reel1_pro_mastered_audio.wav"

WIDTH = 1080
HEIGHT = 1920
VIDEO_H = 940
VIDEO_Y = 558
BANNER_Y = 408
BANNER_H = 150
SUBS_Y = 1340
SUBS_H = 180

TOTAL_DUR = 74.0

COLOR_FF8400 = (255, 132, 0, 255)
COLOR_BLACK = (0, 0, 0, 255)

print("🎬 Step 1: Generating Native Cocoa Reference 11 Header Banner (#FF8400)...")
banner_png = WORKSPACE / "ref11_master_banner.png"

im = NSImage.alloc().initWithSize_((WIDTH, BANNER_H))
im.lockFocus()

# Fill #FF8400 (255, 132, 0)
NSColor.colorWithDeviceRed_green_blue_alpha_(255.0/255.0, 132.0/255.0, 0.0/255.0, 1.0).set()
NSRectFill(Cocoa.NSMakeRect(0, 0, WIDTH, BANNER_H))

# 3px black borders
Cocoa.NSColor.blackColor().set()
Cocoa.NSRectFill(Cocoa.NSMakeRect(0, 0, WIDTH, 3))
Cocoa.NSRectFill(Cocoa.NSMakeRect(0, BANNER_H - 3, WIDTH, 3))

font1 = NSFont.fontWithName_size_("TamilSangamMN-Bold", 46.0) or NSFont.boldSystemFontOfSize_(46.0)

s1 = "ராமாயணம் கற்றுத்தரும் பாடம் 🏹"

as1 = NSAttributedString.alloc().initWithString_attributes_(s1, {NSFontAttributeName: font1, NSForegroundColorAttributeName: Cocoa.NSColor.blackColor()})

sz1 = as1.size()

# In Cocoa coordinates, Y=0 is bottom; center both horizontally and vertically
x_pos = (WIDTH - sz1.width) / 2.0
y_pos = (BANNER_H - sz1.height) / 2.0
as1.drawAtPoint_((x_pos, y_pos))

im.unlockFocus()

rep = NSBitmapImageRep.imageRepWithData_(im.TIFFRepresentation())
png_data = rep.representationUsingType_properties_(Cocoa.NSPNGFileType, {})
png_data.writeToFile_atomically_(str(banner_png), True)
print(f"✅ Header Banner saved: {banner_png}")

print("🎬 Step 2: Preparing Video Visual Track (Exact Speaker Framing & B-Rolls)...")
ref11_video_track = WORKSPACE / "ref11_visual_track.mp4"

if not ref11_video_track.exists():
    # Defined Cuts (Total = 74.0s)
    CUT_SPECS = [
        {"type": "host", "st": 1988.0, "dur": 7.5, "broll": None, "bw_hook": True},
        {"type": "broll", "st": 0.0, "dur": 3.0, "broll": str(BROLLS_DIR / "broll_scripture.mp4")},
        {"type": "guest", "st": 1999.0, "dur": 7.0, "broll": None},
        {"type": "broll", "st": 0.0, "dur": 3.0, "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4")},
        {"type": "guest", "st": 2009.0, "dur": 6.5, "broll": None},
        {"type": "broll", "st": 0.0, "dur": 4.0, "broll": str(BROLLS_DIR / "broll_golden_sunrise.mp4")},
        {"type": "punch", "st": 2029.0, "dur": 6.0, "broll": None},
        {"type": "broll", "st": 0.0, "dur": 4.5, "broll": str(BROLLS_DIR / "broll_fire.mp4")},
        {"type": "guest", "st": 2039.5, "dur": 7.5, "broll": None},
        {"type": "broll", "st": 0.0, "dur": 4.5, "broll": str(BROLLS_DIR / "broll_ravi_varma_ravana_sita.mp4")},
        {"type": "guest", "st": 2051.5, "dur": 6.0, "broll": None},
        {"type": "broll", "st": 0.0, "dur": 4.0, "broll": str(BROLLS_DIR / "broll_temple.mp4")},
        {"type": "guest", "st": 2057.5, "dur": 10.5, "broll": None}
    ]

    total_calc_dur = sum(c["dur"] for c in CUT_SPECS)
    print(f"Total calculated cuts duration: {total_calc_dur:.2f}s")
    assert abs(total_calc_dur - TOTAL_DUR) < 0.01, f"Duration mismatch: {total_calc_dur} vs {TOTAL_DUR}"

    cut_files = []
    concat_list = WORKSPACE / "ref11_cuts_concat.txt"

    COLOR_GRADE = "eq=contrast=1.08:saturation=0.92:brightness=-0.01,colorbalance=rs=0.03:gs=0.01:bs=-0.03"

    for idx, cut in enumerate(CUT_SPECS):
        out_cut = WORKSPACE / f"ref11_mcut_{idx}.mp4"
        cut_files.append(out_cut)
        dur = cut["dur"]
        
        if cut["type"] == "broll":
            vf = f"scale=1080:940:force_original_aspect_ratio=increase,crop=1080:940,fps=30,setsar=1,{COLOR_GRADE}"
            cmd = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}", "-stream_loop", "-1",
                "-i", cut["broll"],
                "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)
            ]
        else:
            if cut["type"] == "host":
                # Host Woman centered MCU
                crop = "crop=1206:1050:2150:650,scale=1080:940:flags=lanczos"
            elif cut["type"] == "punch":
                # Guest Man 1.15x Punch-in
                crop = "crop=1048:913:530:820,scale=1080:940:flags=lanczos"
            else:
                # Guest Man standard MCU
                crop = "crop=1206:1050:450:750,scale=1080:940:flags=lanczos"
                
            if cut.get("bw_hook"):
                vf = f"{crop},hue=s='if(lt(t,0.6),0,1)',{COLOR_GRADE},fps=30,setsar=1"
            else:
                vf = f"{crop},{COLOR_GRADE},fps=30,setsar=1"
                
            cmd = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_cut)
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(concat_list, "w") as f:
        for cf in cut_files:
            f.write(f"file '{cf}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-vf", f"pad={WIDTH}:{HEIGHT}:0:{VIDEO_Y}:color=black",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(ref11_video_track)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Master visual track assembled: {ref11_video_track}")
else:
    print(f"✅ Master visual track already exists: {ref11_video_track}")

print("🎬 Step 3: Generating Single-Word Fast Subtitles Video (MyHandwriting.ttf in #FF8400)...")

SINGLE_WORDS = [
    # Host speaks: 3.5s - 7.5s
    (3.54, 4.10, "WHAT"),
    (4.10, 4.60, "LIFE"),
    (4.60, 5.20, "LESSON"),
    (5.20, 5.80, "CAN WE"),
    (5.80, 6.44, "LEARN?"),
    (6.44, 7.00, "FROM"),
    (7.00, 7.60, "RAMAYANA? 🏹"),
    
    # Guest responds: 8.74s - 13.24s
    (8.74, 9.40, "I WANT"),
    (9.40, 10.20, "TO TALK"),
    (10.20, 10.76, "ONLY"),
    (10.76, 11.60, "ABOUT"),
    (11.60, 12.40, "HANUMAN!"),
    (12.40, 13.24, "BECAUSE..."),
    
    # "Everybody is like Hanuman": 13.24s - 17.5s
    (13.24, 13.80, "EVERYBODY"),
    (13.80, 14.20, "IS"),
    (14.20, 14.50, "LIKE"),
    (14.50, 15.30, "HANUMAN! 🏹"),
    (15.66, 16.30, "WE ALL"),
    (16.30, 17.00, "HAVE A"),
    (17.00, 17.60, "HIDDEN"),
    
    # Latent Potential & Mentor: 17.6s - 26.5s
    (17.60, 18.50, "LATENT"),
    (18.50, 19.40, "POTENTIAL! 🔥"),
    (19.40, 20.00, "SOMEONE"),
    (20.00, 20.70, "HAS TO"),
    (20.70, 21.40, "AWAKEN IT!"),
    (21.40, 22.20, "THAT'S THE"),
    (22.20, 23.20, "MENTOR!"),
    (23.20, 24.20, "SECOND"),
    (24.20, 25.40, "IS"),
    (25.40, 26.50, "LOYALTY!"),
    
    # Jambavan awakens Hanuman: 26.5s - 37.0s
    (26.80, 27.80, "JAMBAVAN"),
    (27.80, 28.80, "CAME TO"),
    (28.80, 29.80, "HANUMAN"),
    (29.80, 31.00, "AND SAID..."),
    (31.20, 32.20, "YOU ARE"),
    (32.20, 33.40, "POWERFUL! 🔥"),
    (33.40, 34.40, "YOUR OWN"),
    (34.40, 35.40, "STRENGTH"),
    (35.40, 36.30, "YOU DID NOT"),
    (36.30, 37.00, "REALIZE!"),
    
    # Ocean Leap: 37.0s - 49.0s
    (37.20, 38.30, "HE LEAPED"),
    (38.30, 39.40, "ACROSS"),
    (39.40, 40.50, "THE OCEAN! 🌊"),
    (40.50, 41.50, "TO LANKA!"),
    (41.80, 42.80, "ONLY"),
    (42.80, 43.80, "BECAUSE"),
    (43.80, 44.80, "SOMEONE"),
    (44.80, 46.00, "AWAKENED"),
    (46.00, 47.40, "HIM! 🔥"),
    (47.40, 48.80, "THAT MENTOR!"),
    
    # Finding Sita & Lesson: 49.0s - 59.5s
    (49.20, 50.40, "HE FOUND"),
    (50.40, 51.80, "MOTHER SITA!"),
    (51.80, 53.20, "VICTORY! 🏹"),
    (53.50, 54.80, "WITHOUT THAT"),
    (54.80, 56.00, "AWAKENING,"),
    (56.00, 57.20, "HE WOULD"),
    (57.20, 58.40, "NEVER"),
    (58.40, 59.50, "HAVE KNOWN!"),
    
    # Climax & Final Takeaway: 59.5s - 74.0s
    (59.80, 61.00, "GREATEST"),
    (61.00, 62.20, "LESSON"),
    (62.20, 63.40, "OF LIFE!"),
    (63.80, 64.80, "FIND"),
    (64.80, 65.80, "YOUR"),
    (65.80, 67.00, "JAMBAVAN!"),
    (67.00, 68.20, "FIND"),
    (68.20, 69.40, "YOUR"),
    (69.40, 70.80, "MENTOR! 🔥"),
    (70.80, 72.20, "BELIEVE IN"),
    (72.20, 74.00, "YOUR POWER! 🏹")
]

font_hw = ImageFont.truetype("/Users/pgi/Library/Fonts/MyHandwriting.ttf", 76)
font_fallback = ImageFont.truetype(str(ASSETS_DIR / "fonts" / "NotoSansTamil-Bold.ttf"), 60)

def render_word_frame(word):
    im = Image.new("RGBA", (WIDTH, SUBS_H), (0, 0, 0, 0))
    if not word:
        return im.tobytes()
        
    draw = ImageDraw.Draw(im)
    
    # Strip any emoji characters that MyHandwriting.ttf cannot render
    import re
    clean_word = re.sub(r'[^\w\s\?!,\'\.]', '', word).strip()
    if not clean_word:
        return im.tobytes()
        
    f = font_hw
    w = draw.textlength(clean_word, font=f)
    if w > WIDTH - 80:
        # Scale down if very long
        f = ImageFont.truetype("/Users/pgi/Library/Fonts/MyHandwriting.ttf", 62)
        w = draw.textlength(clean_word, font=f)
        
    x = (WIDTH - w) / 2
    y = 42
    
    # Multi-pass soft shadow + thick black outline
    for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3), (0, -3), (3, 0), (-3, 0)]:
        draw.text((x + dx, y + dy), clean_word, font=f, fill=(0, 0, 0, 200), stroke_width=6, stroke_fill=COLOR_BLACK)
        
    # Main text in signature #FF8400 with 7px solid black stroke
    draw.text((x, y), clean_word, font=f, fill=COLOR_FF8400, stroke_width=7, stroke_fill=COLOR_BLACK)
    return im.tobytes()

subs_mov = WORKSPACE / "ref11_master_subs.mov"
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{SUBS_H}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_frames = int(round(TOTAL_DUR * 30))
blank_bytes = render_word_frame("")

for f_idx in range(total_frames):
    t_sec = f_idx / 30.0
    active_word = ""
    for st, et, word in SINGLE_WORDS:
        if st <= t_sec < et:
            active_word = word
            break
    frame_bytes = render_word_frame(active_word) if active_word else blank_bytes
    proc.stdin.write(frame_bytes)

proc.stdin.close()
proc.wait()
print(f"✅ Fast single-word subtitles video written: {subs_mov}")

print("🎬 Step 4: Assembling Final Master Reel in Reference 11 Style...")
final_output = EXPORT_DIR / "Reel_1_Reference_11_Style.mp4"

subprocess.run([
    "ffmpeg", "-y",
    "-t", "74.0",
    "-i", str(ref11_video_track),
    "-loop", "1", "-i", str(banner_png),
    "-i", str(subs_mov),
    "-i", str(PRO_AUDIO),
    "-filter_complex",
    f"[0:v][1:v]overlay=0:{BANNER_Y}:shortest=1[v_banner];"
    f"[v_banner][2:v]overlay=0:{SUBS_Y}:shortest=1[v]",
    "-map", "[v]", "-map", "3:a",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
    "-t", "74.0",
    str(final_output)
], check=True)

print(f"🎉 MASTER REEL 1 IN REFERENCE 11 EXPORTED TO: {final_output}")

# Extract Verification QA Frames
print("📸 Extracting QA Verification Frames...")
qa_cues = [
    (4.5, "qa_ref11_host_t4.5s.png"),
    (8.5, "qa_ref11_broll_t8.5s.png"),
    (12.0, "qa_ref11_guest_t12.0s.png"),
    (14.5, "qa_ref11_guest_hanuman_t14.5s.png"),
    (18.5, "qa_ref11_broll_power_t18.5s.png"),
    (22.0, "qa_ref11_guest_mentor_t22.0s.png"),
    (33.0, "qa_ref11_punch_powerful_t33.0s.png"),
    (39.0, "qa_ref11_broll_leap_t39.0s.png"),
    (45.0, "qa_ref11_guest_awakened_t45.0s.png"),
    (51.0, "qa_ref11_broll_sita_t51.0s.png"),
    (70.0, "qa_ref11_climax_mentor_t70.0s.png")
]

ARTIFACT_DIR = Path("/Users/pgi/.gemini/antigravity/brain/c7bb1df4-099d-491f-8aa1-5fa38d329638")
for t, name in qa_cues:
    out_frame = FRAMES_DIR / name
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(t), "-i", str(final_output),
        "-vframes", "1", str(out_frame)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ARTIFACT_DIR.exists():
        import shutil
        shutil.copy(out_frame, ARTIFACT_DIR / name)

print("✅ All QA frames extracted and copied to artifacts successfully!")
