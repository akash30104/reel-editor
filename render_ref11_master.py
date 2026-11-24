#!/usr/bin/env python3
"""
render_ref11_master.py
Master Renderer for Reel 1 in Reference 11 Style:

1. Canvas & Layout (Reference 11 Master Specification):
   - Canvas: 1080x1920 @ 30 fps
   - Top black bar: Y = 0 to 408
   - Header Banner: Y = 408 to 558 (Height 150px)
     * Background: Signature Reference 11 Orange #FF8400 (RGB: 255, 132, 0)
     * 3px solid black border lines top and bottom
     * Clean English Title: "Lessons from Ramayana 🏹"
   - Active Video Window: Y = 558 to 1498 (Height 940px, centered)
     * Strict SDR BT.709 color pipeline (strips all iPhone HDR/HLG/BT.2020 tags so orange never displays as red)
     * 100% Acoustic Lip-Sync: Every speaker cut starts at 1988.0 + timeline_elapsed
     * Speaker framing:
       - Host Woman: crop=1206:1050:2150:650 -> scale=1080:940
       - Guest Man: crop=1206:1050:450:750 -> scale=1080:940
       - Guest Punch-in (1.15x): crop=1048:913:530:820 -> scale=1080:940
     * Thematic B-Roll cutaways illustrating spoken dialogue without timeline disruption
     * First 0.6s B&W hook snap into warm natural color grade
   - Bottom black bar: Y = 1498 to 1920

2. Subtitles:
   - Dynamic fast single-word / 2-word bursts
   - Font: User's handwriting font MyHandwriting.ttf
   - Color: Signature Orange #FF8400 (RGB: 255, 132, 0) with 7px solid black stroke & drop shadow
   - Placement: Lower third of video window (Y = 1340)
   - Accurate Spoken Tanglish: Strictly synchronized with Whisper millisecond acoustic speech timestamps

3. Audio:
   - Pro Studio Master reel1_pro_mastered_audio.wav (-14.0 LUFS dialogue + ducked flute BGM @ -23 dB)

4. Output:
   - /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_11_Style.mp4
"""

import os
import sys
import re
import shutil
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

# Vibrant Reference 11 Signature Orange #FF8400:
COLOR_ORANGE_RGBA = (255, 132, 0, 255) # #FF8400
COLOR_BLACK = (0, 0, 0, 255)

print("🎬 Step 1: Generating Native Reference 11 Header Banner (#FF8400)...")
banner_png = WORKSPACE / "ref11_master_banner.png"

im = NSImage.alloc().initWithSize_((WIDTH, BANNER_H))
im.lockFocus()

# Fill #FF8400 Reference 11 Orange in sRGB (255, 132, 0)
NSColor.colorWithSRGBRed_green_blue_alpha_(255.0/255.0, 132.0/255.0, 0.0/255.0, 1.0).set()
NSRectFill(Cocoa.NSMakeRect(0, 0, WIDTH, BANNER_H))

# 3px black borders
Cocoa.NSColor.blackColor().set()
Cocoa.NSRectFill(Cocoa.NSMakeRect(0, 0, WIDTH, 3))
Cocoa.NSRectFill(Cocoa.NSMakeRect(0, BANNER_H - 3, WIDTH, 3))

font1 = NSFont.fontWithName_size_("Montserrat-Bold", 58.0) or NSFont.boldSystemFontOfSize_(58.0)
s1 = "Lessons from Ramayana 🏹"
as1 = NSAttributedString.alloc().initWithString_attributes_(s1, {NSFontAttributeName: font1, NSForegroundColorAttributeName: Cocoa.NSColor.blackColor()})
sz1 = as1.size()

# Center horizontally and vertically
x_pos = (WIDTH - sz1.width) / 2.0
y_pos = (BANNER_H - sz1.height) / 2.0
as1.drawAtPoint_((x_pos, y_pos))

im.unlockFocus()

rep = NSBitmapImageRep.imageRepWithData_(im.TIFFRepresentation())
png_data = rep.representationUsingType_properties_(Cocoa.NSPNGFileType, {})
png_data.writeToFile_atomically_(str(banner_png), True)
print(f"✅ Header Banner saved: {banner_png}")

print("🎬 Step 2: Preparing Video Visual Track (Exact 100% Lip-Sync Alignment + SDR BT.709)...")
ref11_video_track = WORKSPACE / "ref11_visual_track.mp4"

# Timeline starts at 1988.0s in 202.MOV. Every speaker segment at timeline T has raw_ss = 1988.0 + T!
CUT_SPECS = [
    {"type": "host",   "timeline_st": 0.0,  "dur": 7.8, "broll": None, "bw_hook": True},
    {"type": "guest",  "timeline_st": 7.8,  "dur": 3.8, "broll": None},
    {"type": "broll",  "timeline_st": 11.6, "dur": 3.4, "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4")},
    {"type": "guest",  "timeline_st": 15.0, "dur": 5.5, "broll": None},
    {"type": "broll",  "timeline_st": 20.5, "dur": 5.0, "broll": str(BROLLS_DIR / "broll_scripture.mp4")},
    {"type": "punch",  "timeline_st": 25.5, "dur": 8.5, "broll": None},
    {"type": "broll",  "timeline_st": 34.0, "dur": 5.0, "broll": str(BROLLS_DIR / "broll_fire.mp4")},
    {"type": "guest",  "timeline_st": 39.0, "dur": 7.0, "broll": None},
    {"type": "punch",  "timeline_st": 46.0, "dur": 6.0, "broll": None},
    {"type": "broll",  "timeline_st": 52.0, "dur": 5.0, "broll": str(BROLLS_DIR / "broll_golden_sunrise.mp4")},
    {"type": "guest",  "timeline_st": 57.0, "dur": 9.0, "broll": None},
    {"type": "broll",  "timeline_st": 66.0, "dur": 4.0, "broll": str(BROLLS_DIR / "broll_temple.mp4")},
    {"type": "punch",  "timeline_st": 70.0, "dur": 4.0, "broll": None}
]

total_calc_dur = sum(c["dur"] for c in CUT_SPECS)
print(f"Total calculated cuts duration: {total_calc_dur:.2f}s")
assert abs(total_calc_dur - TOTAL_DUR) < 0.01, f"Duration mismatch: {total_calc_dur} vs {TOTAL_DUR}"

cut_files = []
concat_list = WORKSPACE / "ref11_cuts_concat.txt"

COLOR_GRADE = "eq=contrast=1.08:saturation=0.92:brightness=-0.01,colorbalance=rs=0.03:gs=0.01:bs=-0.03"
SDR_FILTER = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,format=yuv420p"

for idx, cut in enumerate(CUT_SPECS):
    out_cut = WORKSPACE / f"ref11_mcut_{idx}.mp4"
    cut_files.append(out_cut)
    dur = cut["dur"]
    t_st = cut["timeline_st"]
    raw_ss = 1988.0 + t_st
    
    if cut["type"] == "broll":
        vf = f"scale=1080:940:force_original_aspect_ratio=increase,crop=1080:940,fps=30,setsar=1,{COLOR_GRADE},{SDR_FILTER}"
        cmd = [
            "ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}", "-stream_loop", "-1",
            "-i", cut["broll"],
            "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            str(out_cut)
        ]
    else:
        if cut["type"] == "host":
            crop = "crop=1206:1050:2150:650,scale=1080:940:flags=lanczos"
        elif cut["type"] == "punch":
            crop = "crop=1048:913:530:820,scale=1080:940:flags=lanczos"
        else:
            crop = "crop=1206:1050:450:750,scale=1080:940:flags=lanczos"
            
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
    for cf in cut_files:
        f.write(f"file '{cf}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
    "-vf", f"pad={WIDTH}:{HEIGHT}:0:{VIDEO_Y}:color=black,{SDR_FILTER}",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    str(ref11_video_track)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"✅ Master visual track assembled: {ref11_video_track}")

print("🎬 Step 3: Generating Accurate Tanglish Spoken Subtitles Video (MyHandwriting.ttf in #FF8400)...")

# Exact spoken Tamil/Tanglish words matching whisper acoustic timestamps:
SPEECH_SYNCED_WORDS = [
    # Host (0.0 - 7.8s): "ராமாயணத்துல இருந்து நாம் என்ன கத்துக்கணும்?"
    (2.60, 3.40, "RAMAYANATHULA..."),
    (3.40, 4.30, "NAAM ENNA"),
    (4.30, 5.50, "KATTHUKKANUM?"),
    (6.40, 7.60, "EDHU MUKKIYAM? 🏹"),
    
    # Guest (7.8 - 11.6s): "நான் வந்து ஹனுமான பத்தி மட்டும் பேச நினைக்கிறேன்..."
    (8.20, 9.20, "NAAN VANDHU"),
    (9.20, 10.40, "HANUMAN-A PATHI"),
    (10.40, 11.40, "MATTUM"),
    
    # "Everybody is like Hanuman" (11.6 - 15.0s)
    (11.80, 13.00, "EVERYBODY IS"),
    (13.00, 14.60, "LIKE HANUMAN! 🏹"),
    
    # Latent Potential & Mentor (15.0 - 20.5s): "நமக்குள்ள Latent potential இருக்கு..."
    (15.20, 16.20, "NAMAKKULLA"),
    (16.20, 17.10, "LATENT POTENTIAL"),
    (17.10, 17.80, "IRUKKU! 🔥"),
    (18.00, 18.90, "SOMEONE HAS TO"),
    (18.90, 19.40, "SHOW IT TO US,"),
    (19.40, 20.40, "THAT'S THE MENTOR!"),
    
    # Second is Loyalty (20.5 - 25.5s)
    (20.80, 21.80, "MENTOR MADHIRI"),
    (21.80, 22.80, "IRUNDHA JEIKKALAAM!"),
    (23.00, 24.20, "SECOND IS"),
    (24.20, 25.40, "LOYALTY! 🤝"),
    
    # Workplace example (25.5 - 34.0s)
    (26.20, 27.50, "ORU COMPANY-LA"),
    (27.50, 29.00, "STAFF ORUTHAN"),
    (29.00, 30.50, "VARUTHAPPATTAAR,"),
    (30.80, 32.20, "2 YEARS"),
    (32.20, 33.60, "VELA SENJITTU..."),
    
    # Sollama vittutaanga (34.0 - 39.0s)
    (34.00, 35.50, "SOLLAMA KOLLAMA"),
    (35.50, 37.00, "VELAIYA"),
    (37.00, 38.60, "VITTUTAANGA! 💔"),
    
    # Loyal-aa irundhaa (39.0 - 46.0s)
    (39.50, 40.80, "ENAKKU THERIYUM-NU"),
    (40.80, 42.20, "LOYAL-AA IRUNDHA..."),
    (42.20, 43.60, "AVANGA"),
    (43.60, 45.40, "IRUNDHIRUPPAANGA!"),
    
    # People lack loyalty (46.0 - 52.0s)
    (46.00, 47.40, "NADANDHIRUKKALAAM,"),
    (47.40, 48.80, "EXAMPLE SOLLANUM-NA,"),
    (48.80, 50.40, "PEOPLE LACK"),
    (50.40, 51.80, "LOYALTY! ⚠️"),
    
    # I will give example / Nambikkai (52.0 - 57.0s)
    (52.20, 53.60, "I WILL GIVE"),
    (53.60, 55.00, "AN EXAMPLE..."),
    (55.00, 56.60, "ENNOADA NAMBIKKAI!"),
    
    # Faithful (57.0 - 66.0s)
    (57.20, 58.80, "NAAN KANDIPPAA"),
    (58.80, 60.40, "SOLLUREN,"),
    (60.40, 62.00, "FAITHFUL-AA"),
    (62.00, 63.60, "IRUKKAVANGA"),
    (63.60, 65.40, "AVANGADHAAN!"),
    
    # Climax (66.0 - 74.0s)
    (66.20, 68.00, "HANUMAN-ODA"),
    (68.00, 69.80, "LOYALTY... 🏹"),
    (70.00, 71.80, "POWERFUL-AANA"),
    (71.80, 73.80, "KAARIYAM! 🔥")
]

FONT_PATH = "/Users/pgi/Library/Fonts/MyHandwriting.ttf"

def render_word_frame(word):
    im = Image.new("RGBA", (WIDTH, SUBS_H), (0, 0, 0, 0))
    if not word:
        return im.tobytes()
        
    draw = ImageDraw.Draw(im)
    clean_word = re.sub(r'[^A-Za-z0-9\s\?!\',\.\-]', '', word).strip()
    if not clean_word:
        return im.tobytes()
        
    f = ImageFont.truetype(FONT_PATH, 78)
    w = draw.textlength(clean_word, font=f)
    if w > 940:
        scaled_size = max(46, int(78 * 920 / w))
        f = ImageFont.truetype(FONT_PATH, scaled_size)
        w = draw.textlength(clean_word, font=f)
        
    x = (WIDTH - w) / 2
    y = 45
    
    # Multi-pass shadow + thick black outline for maximum contrast
    for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (0, -4), (4, 0), (-4, 0)]:
        draw.text((x + dx, y + dy), clean_word, font=f, fill=(0, 0, 0, 200), stroke_width=6, stroke_fill=COLOR_BLACK)
        
    # Main text in signature Reference 11 Orange #FF8400 with 7px solid black stroke
    draw.text((x, y), clean_word, font=f, fill=COLOR_ORANGE_RGBA, stroke_width=7, stroke_fill=COLOR_BLACK)
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
    for st, et, word in SPEECH_SYNCED_WORDS:
        if st <= t_sec < et:
            active_word = word
            break
    frame_bytes = render_word_frame(active_word) if active_word else blank_bytes
    proc.stdin.write(frame_bytes)

proc.stdin.close()
proc.wait()
print(f"✅ Accurate speech-synced subtitles video written: {subs_mov}")

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
    f"[v_banner][2:v]overlay=0:{SUBS_Y}:shortest=1,{SDR_FILTER}[v]",
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
    (9.5, "qa_ref11_guest_hanuman_t9.5s.png"),
    (13.5, "qa_ref11_broll_hanuman_t13.5s.png"),
    (17.5, "qa_ref11_guest_latent_t17.5s.png"),
    (24.0, "qa_ref11_broll_loyalty_t24.0s.png"),
    (32.0, "qa_ref11_punch_2years_t32.0s.png"),
    (36.0, "qa_ref11_broll_fire_t36.0s.png"),
    (42.0, "qa_ref11_guest_loyal_t42.0s.png"),
    (49.0, "qa_ref11_punch_lackloyalty_t49.0s.png"),
    (54.0, "qa_ref11_broll_sunrise_t54.0s.png"),
    (63.0, "qa_ref11_guest_faithful_t63.0s.png"),
    (72.0, "qa_ref11_climax_arrow_t72.0s.png")
]

ARTIFACT_DIR = Path("/Users/pgi/.gemini/antigravity/brain/c7bb1df4-099d-491f-8aa1-5fa38d329638")
for t, name in qa_cues:
    out_frame = FRAMES_DIR / name
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(t), "-i", str(final_output),
        "-vframes", "1", str(out_frame)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ARTIFACT_DIR.exists():
        shutil.copy(out_frame, ARTIFACT_DIR / name)

print("✅ All QA frames extracted and copied to artifacts successfully!")
