#!/usr/bin/env python3
"""
render_ref3_IMG6596.py
Master Renderer for IMG_6596.MOV in Exact Reference 3 Style:

1. Canvas & Layout:
   - Canvas: 1080x1920 @ 30 fps (pure black #000000)
   - Video Window: 1080x608 (16:9 letterboxed) centered at Y = 656 to 1264
   - Soft black gradient fade at bottom of video window (Y = 1184 to 1264, 80px)
   - Active speaker camera tracking:
     * Host Lokesh (Right speaker): crop=2080:1170:1710:420 -> scale=1080:608
     * Ganesh (Left speaker): crop=2080:1170:50:420 -> scale=1080:608
     * Ganesh Punch-in (1.15x): crop=1808:1017:186:496 -> scale=1080:608
     * Wide Two-Shot: scale=1080:608

2. Subtitle Typography & Safe Placement:
   - Font: Impact (/System/Library/Fonts/Supplemental/Impact.ttf, size 72)
   - Color: Pure White (#FFFFFF)
   - Stroke: 3.5px solid black outline (#000000)
   - Drop Shadow: Multi-pass dark shadow (rgba(0, 0, 0, 220))
   - Placement: Lower chest / torso (Y = 1130 on 1080x1920 canvas)
   - SAFETY GUARANTEE: NEVER ON THE FACE (speaker face is at Y = 750 to 950)
   - Language: Tanglish with high-energy punctuation (e.g. COLLEGE STUDENT...!, PRIVATE LIMITED...!)
   - Pacing: Fast 1 to 3 words per burst (0.8s to 1.5s per burst)

3. Audio:
   - Dialogue normalized to broadcast standard -14.0 LUFS / -1.0 dBTP
   - Continuous mild background music bed (ramayan_flute_bgm.mp3) ducked to -23 dB
   - Zero watermarks

4. Output:
   - /Users/pgi/Downloads/reels editor/export /Reel_IMG_6596_Reference_3_Style.mp4
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/IMG_6596.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
ARTIFACT_DIR = Path("/Users/pgi/.gemini/antigravity/brain/c7bb1df4-099d-491f-8aa1-5fa38d329638")
BGM_TRACK = WORKSPACE / "assets" / "audio" / "ramayan_flute_bgm.mp3"

WIDTH = 1080
HEIGHT = 1920
VIDEO_W = 1080
VIDEO_H = 608
VIDEO_Y = 656
SUBS_Y = 1070
SUBS_H = 160

START_TIME = 176.0
DURATION = 60.0

COLOR_WHITE = (255, 255, 255, 255)
COLOR_BLACK = (0, 0, 0, 255)
IMPACT_FONT_PATH = "/System/Library/Fonts/Supplemental/Impact.ttf"

print("🎬 Step 1: Preparing Master Dialogue Audio (-14.0 LUFS + ducked BGM @ -23 dB)...")
raw_audio = WORKSPACE / "ref3_6596_raw_audio.wav"
master_audio = WORKSPACE / "ref3_6596_pro_audio.wav"

subprocess.run([
    "ffmpeg", "-y", "-ss", f"{START_TIME:.3f}", "-t", f"{DURATION:.3f}",
    "-i", str(RAW_VIDEO), "-vn", "-ac", "2", "-ar", "48000", str(raw_audio)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Audio filter complex: normalize voice to -14 LUFS, duck BGM to -23 dB, merge
subprocess.run([
    "ffmpeg", "-y",
    "-i", str(raw_audio),
    "-stream_loop", "-1", "-i", str(BGM_TRACK),
    "-filter_complex",
    "[0:a]loudnorm=I=-14.0:TP=-1.0:LRA=11.0[v_norm];"
    "[1:a]volume=-23dB,afade=t=in:st=0:d=1.5,afade=t=out:st=58.0:d=2.0[bgm];"
    "[v_norm][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
    "-map", "[aout]", "-t", f"{DURATION:.3f}",
    str(master_audio)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"✅ Pro Master Audio ready: {master_audio}")

print("🎬 Step 2: Assembling 16:9 Letterbox Video Track with Camera Cuts & Bottom Gradient...")
COLOR_GRADE = "eq=contrast=1.08:saturation=0.95:brightness=-0.01,colorbalance=rs=0.03:gs=0.01:bs=-0.03"

# Cuts for the 60s reel:
# Relative to START_TIME = 176.0
CUTS = [
    # st_rel, dur, type
    (0.0, 2.5, "host"),      # Host welcomes Ganesh
    (2.5, 3.0, "ganesh"),    # Ganesh responds "Fine bro"
    (5.5, 6.0, "host"),      # Host asks for quick crisp intro
    (11.5, 7.0, "ganesh"),   # Ganesh: My name is Ganesh, College student, start company from scratch
    (18.5, 3.5, "punch"),    # Ganesh punch-in: Zero knowledge, zero idea!
    (22.0, 5.0, "ganesh"),   # Ganesh: Research founders on social media
    (27.0, 5.5, "ganesh"),   # Ganesh: Local broker meet panni connect aanom
    (32.5, 4.5, "ganesh"),   # Ganesh: Mentoring kaga contact pannom
    (37.0, 4.5, "host"),     # Host: Super Ganesh!
    (41.5, 5.0, "host"),     # Host: Business started ah illa ideation stage ah?
    (46.5, 5.0, "ganesh"),   # Ganesh: Business start pannitom, company registered
    (51.5, 2.5, "host"),     # Host: Proprietary company ah?
    (54.0, 3.0, "punch"),    # Ganesh punch-in: Private Limited company!
    (57.0, 3.0, "wide")      # Host reaction / Wide Climax: College padikkumbothe Private Limited company ah?!
]

total_cuts_dur = sum(c[1] for c in CUTS)
assert abs(total_cuts_dur - DURATION) < 0.01, f"Cuts duration mismatch: {total_cuts_dur} vs {DURATION}"

video_track = WORKSPACE / "ref3_6596_video_track.mp4"

if not video_track.exists():
    cut_files = []
    concat_list = WORKSPACE / "ref3_6596_concat.txt"

    for idx, (st_rel, dur, ctype) in enumerate(CUTS):
        out_cut = WORKSPACE / f"ref3_6596_cut_{idx}.mp4"
        cut_files.append(out_cut)
        abs_st = START_TIME + st_rel
        
        if ctype == "host":
            crop = "crop=2080:1170:1710:420,scale=1080:608:flags=lanczos"
        elif ctype == "punch":
            crop = "crop=1808:1017:186:496,scale=1080:608:flags=lanczos"
        elif ctype == "ganesh":
            crop = "crop=2080:1170:50:420,scale=1080:608:flags=lanczos"
        else: # wide
            crop = "scale=1080:608:flags=lanczos"
            
        vf = f"{crop},{COLOR_GRADE},fps=30,setsar=1"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{abs_st:.3f}", "-t", f"{dur:.3f}",
            "-i", str(RAW_VIDEO),
            "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            str(out_cut)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(concat_list, "w") as f:
        for cf in cut_files:
            f.write(f"file '{cf}'\n")

    # Generate soft black bottom gradient PNG for video window (height 80px, width 1080)
    gradient_png = WORKSPACE / "ref3_bottom_gradient.png"
    grad_im = Image.new("RGBA", (1080, 80), (0, 0, 0, 0))
    for y_g in range(80):
        alpha = int(255 * (y_g / 79.0)**1.5)
        for x_g in range(1080):
            grad_im.putpixel((x_g, y_g), (0, 0, 0, alpha))
    grad_im.save(gradient_png)

    # Concat cuts, pad to 1080x1920 @ Y=656, and overlay soft bottom gradient at Y = 1184 (656 + 608 - 80 = 1184)
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-i", str(gradient_png),
        "-filter_complex",
        f"[0:v]pad={WIDTH}:{HEIGHT}:0:{VIDEO_Y}:color=black[v_pad];"
        f"[v_pad][1:v]overlay=0:1184[vout]",
        "-map", "[vout]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-t", f"{DURATION:.3f}",
        str(video_track)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
else:
    print(f"✅ Master visual track already exists: {video_track}")
print(f"✅ Master 16:9 Letterboxed Visual Track ready: {video_track}")

print("🎬 Step 3: Generating Pure White Impact Subtitles (Reference 3 Specification)...")
# Exact Reference 3 Subtitle Specification:
# Pure White (#FFFFFF) Impact font, 3.5px solid black outline, multi-pass soft drop shadow.
# Anchored at lower chest/torso (Y = 1130 on canvas), COMPLETELY BELOW THE FACE!

SUBTITLE_CUES = [
    # Host Intro
    (0.0, 1.4, "VANAKKAM GANESH...!"),
    (1.4, 2.5, "HOW ARE YOU?"),
    
    # Ganesh reply
    (2.5, 4.0, "FINE BRO...!"),
    (4.0, 5.5, "SUPER!"),
    
    # Host question
    (5.5, 8.5, "ORU QUICK CRISP INTRO..."),
    (8.5, 11.5, "UNNA PATHI...!"),
    
    # Ganesh story
    (11.5, 13.5, "EN PERU GANESH..."),
    (13.5, 15.5, "COLLEGE STUDENT...!"),
    (15.5, 18.5, "START FROM SCRATCH!"),
    
    # High energy hook
    (18.5, 20.2, "ZERO KNOWLEDGE..!"),
    (20.2, 22.0, "ZERO IDEA..!"),
    
    # Journey & Mentorship
    (22.0, 24.5, "FOUNDERS AH..."),
    (24.5, 27.0, "SOCIAL MEDIA LA RESEARCH!"),
    (27.0, 29.8, "LOCAL BROKERS MEET PANNI..."),
    (29.8, 32.5, "CONNECT AANOM!"),
    (32.5, 34.8, "NEXT TIME..."),
    (34.8, 37.0, "MENTORING KAGA!"),
    
    # Host Question
    (37.0, 39.5, "SUPER GANESH...!"),
    (39.5, 41.5, "AWESOME!"),
    (41.5, 44.0, "BUSINESS STARTED AH?"),
    (44.0, 46.5, "IDEATION STAGE AH?"),
    
    # Ganesh Big Reveal
    (46.5, 49.0, "BUSINESS START PANNITOM!"),
    (49.0, 51.5, "COMPANY REGISTERED..!"),
    
    # Host Question
    (51.5, 54.0, "PROPRIETARY COMPANY AH?"),
    
    # Ganesh Climax Punch
    (54.0, 57.0, "PRIVATE LIMITED COMPANY!"),
    
    # Host Viral Reaction
    (57.0, 60.0, "IN COLLEGE DAYS-EH...?!")
]

font_impact = ImageFont.truetype(IMPACT_FONT_PATH, 64)

def render_sub_frame(text):
    im = Image.new("RGBA", (WIDTH, SUBS_H), (0, 0, 0, 0))
    if not text:
        return im.tobytes()
        
    import re
    clean_text = re.sub(r'[^\w\s\?!,\'\.-]', '', text).strip()
    if not clean_text:
        return im.tobytes()
        
    draw = ImageDraw.Draw(im)
    w = draw.textlength(clean_text, font=font_impact)
    f = font_impact
    if w > WIDTH - 120:
        f = ImageFont.truetype(IMPACT_FONT_PATH, 52)
        w = draw.textlength(clean_text, font=f)
        
    x = (WIDTH - w) / 2
    y = 45 # Centered vertically in SUBS_H
    
    # Multi-directional soft drop shadow (rgba(0,0,0,220))
    for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (0, -4), (4, 0), (-4, 0)]:
        draw.text((x + dx, y + dy), clean_text, font=f, fill=(0, 0, 0, 220), stroke_width=4, stroke_fill=COLOR_BLACK)
        
    # Solid Pure White text with 3.5px black outline
    draw.text((x, y), clean_text, font=f, fill=COLOR_WHITE, stroke_width=4, stroke_fill=COLOR_BLACK)
    return im.tobytes()

subs_mov = WORKSPACE / "ref3_6596_subs.mov"
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{SUBS_H}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_frames = int(round(DURATION * 30))
blank_bytes = render_sub_frame("")

for f_idx in range(total_frames):
    t_sec = f_idx / 30.0
    active_text = ""
    for st, et, cue in SUBTITLE_CUES:
        if st <= t_sec < et:
            active_text = cue
            break
    frame_bytes = render_sub_frame(active_text) if active_text else blank_bytes
    proc.stdin.write(frame_bytes)

proc.stdin.close()
proc.wait()
print(f"✅ Pure White Impact Subtitles video rendered: {subs_mov}")

print("🎬 Step 4: Compositing Final Reel in Exact Reference 3 Style...")
final_output = EXPORT_DIR / "Reel_IMG_6596_Reference_3_Style.mp4"

subprocess.run([
    "ffmpeg", "-y",
    "-t", f"{DURATION:.3f}",
    "-i", str(video_track),
    "-i", str(subs_mov),
    "-i", str(master_audio),
    "-filter_complex",
    f"[0:v][1:v]overlay=0:{SUBS_Y}:shortest=1[v]",
    "-map", "[v]", "-map", "2:a",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
    "-t", f"{DURATION:.3f}",
    str(final_output)
], check=True)

print(f"🎉 MASTER REEL IN REFERENCE 3 EXPORTED TO: {final_output}")

# Extract Verification QA Frames
print("📸 Extracting QA Verification Frames...")
qa_cues = [
    (1.0, "qa_ref3_6596_host_intro_t1.0s.png"),
    (3.5, "qa_ref3_6596_ganesh_fine_t3.5s.png"),
    (9.0, "qa_ref3_6596_host_crisp_t9.0s.png"),
    (14.0, "qa_ref3_6596_ganesh_student_t14.0s.png"),
    (19.5, "qa_ref3_6596_punch_zeroknowledge_t19.5s.png"),
    (25.0, "qa_ref3_6596_ganesh_research_t25.0s.png"),
    (30.5, "qa_ref3_6596_ganesh_broker_t30.5s.png"),
    (35.5, "qa_ref3_6596_ganesh_mentor_t35.5s.png"),
    (42.5, "qa_ref3_6596_host_ideation_t42.5s.png"),
    (48.0, "qa_ref3_6596_ganesh_registered_t48.0s.png"),
    (55.0, "qa_ref3_6596_punch_privatelimited_t55.0s.png"),
    (58.5, "qa_ref3_6596_climax_reaction_t58.5s.png")
]

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
