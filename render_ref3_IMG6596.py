#!/usr/bin/env python3
"""
render_ref3_IMG6596.py
Master Renderer for IMG_6596.MOV in Exact Reference 3 Style:

1. Canvas & Layout:
   - Canvas: 1080x1920 @ 30 fps (pure black #000000)
   - Video Window: 1080x608 (16:9 letterboxed) centered at Y = 656 to 1264
   - Soft black gradient fade at bottom of video window (Y = 1184 to 1264, 80px)
   - Active speaker camera tracking:
     * Host Lokesh (Left speaker, white shirt): crop=2080:1170:50:420 -> scale=1080:608
     * Ganesh (Right speaker, light blue shirt, glasses): crop=2080:1170:1710:420 -> scale=1080:608
     * Ganesh Punch-in (1.15x): crop=1808:1017:1840:480 -> scale=1080:608
     * Wide Two-Shot: scale=1080:608

2. Subtitle Typography & Safe Placement:
   - Font: Impact (/System/Library/Fonts/Supplemental/Impact.ttf, size 64)
   - Color: Pure White (#FFFFFF)
   - Stroke: 4px solid black outline (#000000)
   - Drop Shadow: Multi-pass dark shadow (rgba(0, 0, 0, 220))
   - Placement: Lower chest / bottom of video frame (Y = 1170 on 1080x1920 canvas)
   - SAFETY GUARANTEE: NEVER ON THE FACE (speaker face is at Y = 750 to 950)
   - Speech-locked sync: Every cue begins exactly when the speaker articulates the words

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
import re
import shutil
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
SUBS_Y = 1170
SUBS_H = 140

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
    (0.0, 2.2, "host"),      # Host welcomes Ganesh (0.0 - 2.2s)
    (2.2, 1.3, "ganesh"),    # Ganesh responds "Fine bro... super!" (2.2 - 3.5s)
    (3.5, 8.3, "host"),      # Host asks for quick crisp intro (3.5 - 11.8s)
    (11.8, 6.7, "ganesh"),   # Ganesh: My name is Ganesh, College student (11.8 - 18.5s)
    (18.5, 3.1, "punch"),    # Ganesh punch-in: Zero knowledge, zero idea! (18.5 - 21.6s)
    (21.6, 6.6, "ganesh"),   # Ganesh: Research founders on social media (21.6 - 28.2s)
    (28.2, 4.3, "punch"),    # Ganesh punch-in: Lokesh bro meet panni connect aanom! (28.2 - 32.5s)
    (32.5, 10.0, "ganesh"),  # Ganesh: Mentoring kaga contact pannom (32.5 - 42.5s)
    (42.5, 3.7, "host"),     # Host: Business started ah illa ideation stage ah? (42.5 - 46.2s)
    (46.2, 6.3, "ganesh"),   # Ganesh: Business start pannitom, company registered (46.2 - 52.5s)
    (52.5, 1.7, "host"),     # Host: Proprietary company ah? (52.5 - 54.2s)
    (54.2, 2.6, "punch"),    # Ganesh punch-in: Private Limited company! (54.2 - 56.8s)
    (56.8, 3.2, "wide")      # Host reaction / Wide Climax: College padikkumbothe Private Limited company ah?! (56.8 - 60.0s)
]

total_cuts_dur = sum(c[1] for c in CUTS)
assert abs(total_cuts_dur - DURATION) < 0.01, f"Cuts duration mismatch: {total_cuts_dur} vs {DURATION}"

video_track = WORKSPACE / "ref3_6596_video_track.mp4"

# Force re-generation of cuts & video track
cut_files = []
concat_list = WORKSPACE / "ref3_6596_concat.txt"

for idx, (st_rel, dur, ctype) in enumerate(CUTS):
    out_cut = WORKSPACE / f"ref3_6596_cut_{idx}.mp4"
    cut_files.append(out_cut)
    abs_st = START_TIME + st_rel
    
    if ctype == "host":
        # Host Lokesh (Left speaker, white shirt)
        crop = "crop=2080:1170:50:420,scale=1080:608:flags=lanczos"
    elif ctype == "punch":
        # Ganesh Punch-in 1.15x
        crop = "crop=1808:1017:1840:480,scale=1080:608:flags=lanczos"
    elif ctype == "ganesh":
        # Ganesh (Right speaker, light blue shirt, glasses)
        crop = "crop=2080:1170:1710:420,scale=1080:608:flags=lanczos"
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
print(f"✅ Master 16:9 Letterboxed Visual Track ready: {video_track}")

print("🎬 Step 3: Generating Pure White Impact Subtitles (Speech-Locked Acoustic Timestamps)...")

# Exact speech-synchronized cues with acoustic onsets:
SUBTITLE_CUES = [
    # Host Intro (0.0s - 2.2s)
    (0.0, 1.2, "VANAKKAM GANESH...!"),
    (1.2, 2.2, "EPPADI IRUKKEENGA?"),
    
    # Ganesh reply (2.2s - 3.5s)
    (2.3, 3.5, "FINE BRO... SUPER!"),
    
    # Host question (3.5s - 11.8s)
    (3.5, 6.4, "ORU QUICK CRISP INTRO..."),
    (6.5, 9.2, "UNNA PATHI...!"),
    (9.2, 11.8, "HOW YOU STARTED?"),
    
    # Ganesh story (11.8s - 18.5s)
    (12.1, 14.1, "EN PERU GANESH..."),
    (14.1, 16.2, "COLLEGE STUDENT...!"),
    (16.2, 18.5, "START FROM SCRATCH!"),
    
    # High energy hook (18.5s - 21.6s)
    (18.9, 20.2, "ZERO KNOWLEDGE..!"),
    (20.2, 21.6, "ZERO IDEA..!"),
    
    # Research founders (21.6s - 28.2s)
    (21.8, 24.8, "FOUNDERS AH..."),
    (24.8, 28.2, "SOCIAL MEDIA LA RESEARCH!"),
    
    # Lokesh bro meet panni (28.2s - 32.5s)
    (28.4, 30.6, "LOKESH BRO MEET PANNI..."),
    (30.6, 32.5, "CONNECT AANOM!"),
    
    # Mentoring & Journey (32.5s - 42.5s)
    (33.0, 35.8, "MENTORING KAGA..."),
    (35.8, 38.8, "CONTACT PANNOM!"),
    (38.8, 42.2, "IDEA SHARE PANNOM...!"),
    
    # Host Question (42.5s - 46.2s)
    (42.8, 44.5, "BUSINESS STARTED AH?"),
    (44.5, 46.2, "IDEATION STAGE AH?"),
    
    # Ganesh Big Reveal (46.2s - 52.5s)
    (46.3, 48.5, "BUSINESS START PANNITOM!"),
    (48.5, 52.2, "COMPANY REGISTERED..!"),
    
    # Host Question (52.5s - 54.2s)
    (52.8, 54.2, "PROPRIETARY COMPANY AH?"),
    
    # Ganesh Climax Punch (54.2s - 56.8s)
    (54.2, 56.8, "PRIVATE LIMITED COMPANY! 🔥"),
    
    # Host Viral Reaction (56.8s - 60.0s)
    (57.2, 60.0, "COLLEGE DAYS-LA PRIVATE LIMITED-AH?! 🚀")
]

font_impact = ImageFont.truetype(IMPACT_FONT_PATH, 62)

def render_sub_frame(text):
    im = Image.new("RGBA", (WIDTH, SUBS_H), (0, 0, 0, 0))
    if not text:
        return im.tobytes()
        
    clean_text = re.sub(r'[^A-Za-z0-9\s\?!\',\.\-]', '', text).strip()
    if not clean_text:
        return im.tobytes()
        
    draw = ImageDraw.Draw(im)
    w = draw.textlength(clean_text, font=font_impact)
    f = font_impact
    if w > WIDTH - 120:
        scaled_size = max(44, int(62 * (WIDTH - 140) / w))
        f = ImageFont.truetype(IMPACT_FONT_PATH, scaled_size)
        w = draw.textlength(clean_text, font=f)
        
    x = (WIDTH - w) / 2
    y = 40 # Centered vertically in SUBS_H
    
    # Multi-directional soft drop shadow (rgba(0,0,0,220))
    for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (0, -4), (4, 0), (-4, 0)]:
        draw.text((x + dx, y + dy), clean_text, font=f, fill=(0, 0, 0, 220), stroke_width=4, stroke_fill=COLOR_BLACK)
        
    # Solid Pure White text with 4px black outline
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
    (2.8, "qa_ref3_6596_ganesh_fine_t2.8s.png"),
    (5.0, "qa_ref3_6596_host_crisp_t5.0s.png"),
    (13.0, "qa_ref3_6596_ganesh_enperu_t13.0s.png"),
    (15.0, "qa_ref3_6596_ganesh_student_t15.0s.png"),
    (19.5, "qa_ref3_6596_punch_zeroknowledge_t19.5s.png"),
    (23.0, "qa_ref3_6596_ganesh_research_t23.0s.png"),
    (29.5, "qa_ref3_6596_punch_lokeshbro_t29.5s.png"),
    (31.5, "qa_ref3_6596_ganesh_connect_t31.5s.png"),
    (34.5, "qa_ref3_6596_ganesh_mentor_t34.5s.png"),
    (43.5, "qa_ref3_6596_host_ideation_t43.5s.png"),
    (47.5, "qa_ref3_6596_ganesh_start_t47.5s.png"),
    (50.0, "qa_ref3_6596_ganesh_registered_t50.0s.png"),
    (53.5, "qa_ref3_6596_host_proprietary_t53.5s.png"),
    (55.5, "qa_ref3_6596_punch_privatelimited_t55.5s.png"),
    (58.5, "qa_ref3_6596_climax_reaction_t58.5s.png")
]

for t, name in qa_cues:
    out_frame = FRAMES_DIR / name
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(t), "-i", str(final_output),
        "-vframes", "1", str(out_frame)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ARTIFACT_DIR.exists():
        shutil.copy(out_frame, ARTIFACT_DIR / name)

print("✅ All QA frames extracted and copied to artifacts successfully!")
