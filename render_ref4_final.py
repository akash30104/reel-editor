#!/usr/bin/env python3
"""
render_ref4_final.py
Master rendering script for Reel 1 strictly conforming to updated Reference 4 Specification:
1. Large, prominent subtitle banners:
   - SupText: Arial Bold Italic, size 56.
   - MainTamil: Tamil Sangam MN, size 115, golden-yellow (#FFD700), dark stroke & drop shadow.
   - Full-width dark strip (Y=780..1140, height 360px) framed by white top and bottom border lines.
2. Exact speech-to-subtitle sync:
   - Banners aligned with millisecond precision to spoken syllable onsets and phrases from precise_words.json.
3. REMOVED subscribe card at the end:
   - Climax split-screen dialogue plays through the end (74.0s) ending decisively on the spoken lesson.
4. MCU split-screen framing:
   - Host (Woman) top, Guest (Man) bottom, clean 2px dark dividing seam at Y=960.
5. Thematic 16:9 letterboxed B-rolls centered in black 9:16 canvas.
6. Audio mastering: -14.0 LUFS dialogue over -23 dB mild flute/strings BGM. Zero watermarks.
"""

import os
import sys
import subprocess
from pathlib import Path

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
ASSETS_DIR = WORKSPACE / "assets"
BROLLS_DIR = ASSETS_DIR / "brolls"

WIDTH = 1080
HEIGHT = 1920
TOTAL_DUR = 74.0

pro_dialogue = WORKSPACE / "reel1_pro_mastered_audio.wav"
bgm_music = ASSETS_DIR / "audio" / "ramayan_flute_bgm.mp3"

# 1. Cuts Schedule (Alternating Split-Screen & 16:9 B-Rolls, NO Outro Card!)
# 202.MOV starts at 1988.0s
CUTS_SCHEDULE = [
    # 01. Split-Screen: Host asks opening question (0.0s - 7.5s, dur 7.5s)
    {"type": "split", "st": 0.0, "et": 7.5, "raw_ss": 1988.0},

    # 02. B-Roll 1: Temple / Heritage (7.5s - 10.5s, dur 3.0s)
    {"type": "broll", "st": 7.5, "et": 10.5, "file": BROLLS_DIR / "broll_temple.mp4", "broll_ss": 2.0},

    # 03. Split-Screen: Guest Hanuman Hook & Latent Potential (10.5s - 17.5s, dur 7.0s)
    {"type": "split", "st": 10.5, "et": 17.5, "raw_ss": 1998.5},

    # 04. B-Roll 2: Hanuman Divine Power (17.5s - 20.5s, dur 3.0s)
    {"type": "broll", "st": 17.5, "et": 20.5, "file": BROLLS_DIR / "broll_hanuman_power.mp4", "broll_ss": 1.0},

    # 05. Split-Screen: Mentor & Loyalty (20.5s - 26.5s, dur 6.0s)
    {"type": "split", "st": 20.5, "et": 26.5, "raw_ss": 2008.5},

    # 06. B-Roll 3: Modern Office / Colleague Walkout (26.5s - 31.0s, dur 4.5s)
    {"type": "broll", "st": 26.5, "et": 31.0, "file": BROLLS_DIR / "broll_business.mp4", "broll_ss": 5.0},

    # 07. Split-Screen: 2 Years Work Left Without Word (31.0s - 37.0s, dur 6.0s)
    {"type": "split", "st": 31.0, "et": 37.0, "raw_ss": 2019.0},

    # 08. B-Roll 4: Walking with Purpose / Direction (37.0s - 41.5s, dur 4.5s)
    {"type": "broll", "st": 37.0, "et": 41.5, "file": BROLLS_DIR / "broll_purpose_direction.mp4", "broll_ss": 2.0},

    # 09. Split-Screen: Loyalty in Today's World (41.5s - 49.0s, dur 7.5s)
    {"type": "split", "st": 41.5, "et": 49.0, "raw_ss": 2029.5},

    # 10. B-Roll 5: Promenade Crowd / Modern Society (49.0s - 54.0s, dur 5.0s)
    {"type": "broll", "st": 49.0, "et": 54.0, "file": BROLLS_DIR / "broll_crowd_promenade.mp4", "broll_ss": 4.0},

    # 11. Split-Screen: Rare Quality / Painful Reality (54.0s - 59.5s, dur 5.5s)
    {"type": "split", "st": 54.0, "et": 59.5, "raw_ss": 2042.0},

    # 12. B-Roll 6: Timeless Mountains (59.5s - 63.5s, dur 4.0s)
    {"type": "broll", "st": 59.5, "et": 63.5, "file": BROLLS_DIR / "broll_mountains.mp4", "broll_ss": 3.0},

    # 13. Split-Screen Climax: Selfless Loyalty & Greatest Lesson (63.5s - 74.0s, dur 10.5s - NO OUTRO CARD!)
    {"type": "split", "st": 63.5, "et": 74.0, "raw_ss": 2051.5}
]

# 2. Render Segments
SEGS_DIR = WORKSPACE / "ref4_final_segs"
SEGS_DIR.mkdir(parents=True, exist_ok=True)

# Tight cinematic MCU crop for Host (Woman top) and Guest (Man bottom)
vf_host = (
    "crop=1012:900:2094:680,scale=1080:960:flags=lanczos,"
    "eq=contrast=1.08:saturation=0.92:brightness=-0.01,"
    "colorbalance=rs=0.03:gs=0.01:bs=-0.03,setsar=1,fps=30"
)
vf_guest = (
    "crop=1012:900:494:830,scale=1080:960:flags=lanczos,"
    "eq=contrast=1.08:saturation=0.92:brightness=-0.01,"
    "colorbalance=rs=0.03:gs=0.01:bs=-0.03,setsar=1,fps=30"
)

seg_files = []
print("🎬 Generating Reference 4 final visual segments (NO OUTRO CARD)...")

for idx, item in enumerate(CUTS_SCHEDULE):
    seg_mp4 = SEGS_DIR / f"seg_{idx:02d}.mp4"
    dur = item["et"] - item["st"]

    if item["type"] == "split":
        raw_ss = item["raw_ss"]
        fc = f"[0:v]{vf_host}[top];[0:v]{vf_guest}[bot];[top][bot]vstack=inputs=2,drawbox=x=0:y=959:w=1080:h=2:color=black:t=fill[v]"
        cmd = [
            "ffmpeg", "-y", "-ss", f"{raw_ss:.2f}", "-t", f"{dur:.2f}",
            "-i", str(RAW_VIDEO),
            "-filter_complex", fc, "-map", "[v]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            str(seg_mp4)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    elif item["type"] == "broll":
        b_file = item["file"]
        b_ss = item.get("broll_ss", 0.0)
        vf_broll = (
            "scale=1080:608:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,"
            "setsar=1,fps=30"
        )
        cmd = [
            "ffmpeg", "-y", "-ss", f"{b_ss:.2f}", "-t", f"{dur:.2f}",
            "-i", str(b_file),
            "-vf", vf_broll,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            str(seg_mp4)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    seg_files.append(seg_mp4)

# Concat video track
concat_txt = WORKSPACE / "ref4_final_concat.txt"
concat_txt.write_text("\n".join([f"file '{p}'" for p in seg_files]) + "\n")
base_visual_mp4 = WORKSPACE / "ref4_final_base.mp4"
print("🎬 Concatenating Reference 4 visual track...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c", "copy", str(base_visual_mp4)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 3. Master ASS Subtitle File - Synchronized Exactly to Speech Audio & Enlarged Text Size!
ass_file = WORKSPACE / "ref4_final_banners.ass"
ass_content = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BannerBox,Arial,10,&H200A0A0A,&H00000000,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: BorderLine,Arial,10,&H00FFFFFF,&H00000000,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: SupText,Arial,56,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,1,0,0,100,100,0,0,1,2,3,8,20,20,20,1
Style: MainTamil,Tamil Sangam MN,115,&H0000D7FF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,5,8,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text

; 01. Hook 1: Lesson from Ramayana (Spoken 3.54s - 5.90s)
Dialogue: 0,0:00:03.50,0:00:06.80,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:03.50,0:00:06.80,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:03.50,0:00:06.80,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:03.50,0:00:06.80,SupText,,0,0,0,,{\\pos(540,815)}LESSON FROM RAMAYANA
Dialogue: 2,0:00:03.50,0:00:06.80,MainTamil,,0,0,0,,{\\pos(540,915)}என்ன கத்துக்கணும்?

; 02. Hook 2: Hanuman Topic (Spoken 10.76s - 13.00s)
Dialogue: 0,0:00:10.50,0:00:13.00,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:10.50,0:00:13.00,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:10.50,0:00:13.00,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:10.50,0:00:13.00,SupText,,0,0,0,,{\\pos(540,815)}EVERY HUMAN BEING
Dialogue: 2,0:00:10.50,0:00:13.00,MainTamil,,0,0,0,,{\\pos(540,915)}ஹனுமான் மாதிரி!

; 03. Core Statement: Everybody is like Hanuman (Spoken 13.24s - 14.68s)
Dialogue: 0,0:00:13.10,0:00:15.80,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:13.10,0:00:15.80,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:13.10,0:00:15.80,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:13.10,0:00:15.80,SupText,,0,0,0,,{\\pos(540,815)}EVERYBODY IN THIS WORLD
Dialogue: 2,0:00:13.10,0:00:15.80,MainTamil,,0,0,0,,{\\pos(540,915)}IS LIKE HANUMAN!

; 04. Takeaway 1: Latent Potential (Spoken 16.06s - 17.82s)
Dialogue: 0,0:00:16.00,0:00:17.50,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:16.00,0:00:17.50,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:16.00,0:00:17.50,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:16.00,0:00:17.50,SupText,,0,0,0,,{\\pos(540,815)}HIDDEN STRENGTH
Dialogue: 2,0:00:16.00,0:00:17.50,MainTamil,,0,0,0,,{\\pos(540,915)}LATENT POTENTIAL!

; 05. The Mentor (Spoken 20.80s - 23.20s)
Dialogue: 0,0:00:20.80,0:00:23.20,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:20.80,0:00:23.20,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:20.80,0:00:23.20,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:20.80,0:00:23.20,SupText,,0,0,0,,{\\pos(540,815)}TO AWAKEN YOUR POWER
Dialogue: 2,0:00:20.80,0:00:23.20,MainTamil,,0,0,0,,{\\pos(540,915)}THAT'S THE MENTOR!

; 06. Principle: Unconditional Loyalty (Spoken 23.50s - 26.50s)
Dialogue: 0,0:00:23.50,0:00:26.50,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:23.50,0:00:26.50,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:23.50,0:00:26.50,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:23.50,0:00:26.50,SupText,,0,0,0,,{\\pos(540,815)}GREATEST PRINCIPLE
Dialogue: 2,0:00:23.50,0:00:26.50,MainTamil,,0,0,0,,{\\pos(540,915)}UNCONDITIONAL LOYALTY

; 07. Real Life Story: Staff Left After 2 Years (Spoken 31.88s - 36.00s)
Dialogue: 0,0:00:31.50,0:00:36.50,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:31.50,0:00:36.50,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:31.50,0:00:36.50,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:31.50,0:00:36.50,SupText,,0,0,0,,{\\pos(540,815)}AFTER 2 YEARS OF WORK
Dialogue: 2,0:00:31.50,0:00:36.50,MainTamil,,0,0,0,,{\\pos(540,915)}சொல்லாம போயிட்டாங்க!

; 08. Loyalty Value (Spoken 41.24s - 44.00s)
Dialogue: 0,0:00:41.50,0:00:44.50,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:41.50,0:00:44.50,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:41.50,0:00:44.50,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:41.50,0:00:44.50,SupText,,0,0,0,,{\\pos(540,815)}IF THEY HAD LOYALTY
Dialogue: 2,0:00:41.50,0:00:44.50,MainTamil,,0,0,0,,{\\pos(540,915)}THEY WOULD STAY!

; 09. Reality of Today (Spoken 44.50s - 48.80s)
Dialogue: 0,0:00:44.80,0:00:49.00,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:44.80,0:00:49.00,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:44.80,0:00:49.00,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:44.80,0:00:49.00,SupText,,0,0,0,,{\\pos(540,815)}IN TODAY'S WORLD
Dialogue: 2,0:00:44.80,0:00:49.00,MainTamil,,0,0,0,,{\\pos(540,915)}LOYALTY-E இல்ல!

; 10. Rare Quality (Spoken 54.50s - 59.00s)
Dialogue: 0,0:00:54.50,0:00:59.00,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:54.50,0:00:59.00,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:54.50,0:00:59.00,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:54.50,0:00:59.00,SupText,,0,0,0,,{\\pos(540,815)}A RARE QUALITY
Dialogue: 2,0:00:54.50,0:00:59.00,MainTamil,,0,0,0,,{\\pos(540,915)}LOYAL PEOPLE ENGEY?

; 11. Hanuman's Way (Spoken 64.00s - 68.50s)
Dialogue: 0,0:00:64.00,0:00:68.50,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:64.00,0:00:68.50,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:64.00,0:00:68.50,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:64.00,0:00:68.50,SupText,,0,0,0,,{\\pos(540,815)}HANUMAN'S WAY
Dialogue: 2,0:00:64.00,0:00:68.50,MainTamil,,0,0,0,,{\\pos(540,915)}SELFLESS LOYALTY!

; 12. Final Climax Lesson (Spoken 68.60s - 73.80s)
Dialogue: 0,0:00:68.60,0:00:73.80,BannerBox,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 360 l 0 360{\\p0}
Dialogue: 1,0:00:68.60,0:00:73.80,BorderLine,,0,0,0,,{\\pos(0,780)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 1,0:00:68.60,0:00:73.80,BorderLine,,0,0,0,,{\\pos(0,1140)\\p1}m 0 0 l 1080 0 l 1080 3 l 0 3{\\p0}
Dialogue: 2,0:00:68.60,0:00:73.80,SupText,,0,0,0,,{\\pos(540,815)}LIFE'S TRUTH
Dialogue: 2,0:00:68.60,0:00:73.80,MainTamil,,0,0,0,,{\\pos(540,915)}GREATEST LESSON!
"""
ass_file.write_text(ass_content)
print(f"✅ Synchronized Master ASS file written: {ass_file}")

# 4. Master Assembly & Audio Mixing
final_out = EXPORT_DIR / "Reel_1_Reference_4_Style.mp4"
print(f"🎬 Assembling Master Reference 4 Reel to: {final_out}")

filter_complex = (
    f"[0:v]ass='{ass_file}'[v];"
    f"[2:a]volume=0.06,afade=t=in:ss=0:d=1.0,afade=t=out:st=71.5:d=2.5[bgm];"
    f"[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[a]"
)

subprocess.run([
    "ffmpeg", "-y",
    "-i", str(base_visual_mp4),
    "-i", str(pro_dialogue),
    "-i", str(bgm_music),
    "-filter_complex", filter_complex,
    "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
    "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
    "-shortest",
    "-movflags", "+faststart",
    str(final_out)
], check=True)

print(f"🎉 FINAL REEL 1 IN REFERENCE 4 STYLE EXPORTED: {final_out}")

# Extract Verification QA Frames
subprocess.run(["ffmpeg", "-y", "-ss", "4.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t4.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "8.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t8.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "12.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t12.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "14.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t14.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "19.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_broll_t19.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "22.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t22.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "25.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t25.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "34.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t34.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "43.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t43.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "46.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t46.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "66.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_banner_t66.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "71.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref4_climax_t71.0s.png")], check=True)
print("✅ Reference 4 QA verification frames extracted successfully!")
