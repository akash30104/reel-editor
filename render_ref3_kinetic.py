#!/usr/bin/env python3
"""
render_ref3_kinetic.py
Renders Reel 1 in strict accordance with Reference 3 Master Specification:
1. CANVAS & CAMERA:
   - Pure black 9:16 canvas (1080x1920 @ 30fps).
   - 16:9 video clip centered in the middle third (Y=656..1264, height 608px).
   - Active speaker tracking: dynamically switch camera between Host (0s-8.6s) and Guest (8.6s-74s).
   - Soft black gradient fade on the bottom edge (height 90px, Y=1174..1264).
   - Static shot only: No jump cuts, zooms, or B-roll.
2. COLOR & AUDIO:
   - Warm, slightly desaturated cinematic grade with deep blacks.
   - Clean prominent dialogue (-14.0 LUFS) over mandatory mild emotional instrumental BGM (-23 dB). No whooshes/pop SFX.
   - Zero watermarks (clean 100% distraction-free frame).
3. SUBTITLE STYLE & EXACT KINETIC PLACEMENT:
   - Language: TANGLISH (Phonetic Romanized Tamil + English words matching spoken audio).
   - Font: Anton bold condensed, electric yellow (#FFE500), dark drop shadow + stroke.
   - Chunking: 1-3 words per beat with '...' and '!'.
   - Safe Zone: All text inside 16:9 frame, never covering speaker's face or eyes.
   - Placement Zones: Zone A (Left), Zone B (Right), Zone C (Bottom-Center).
   - Hierarchy: Pop sharply on beat (-60ms visual lead for snappy sync), 1.4x scale hierarchy, cluster stacking across zones, clean reset on sentence boundaries.
4. EXPORT:
   - /Users/pgi/Downloads/reels editor/export /Reel_1_Reference_3_Style.mp4
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
ASSETS_DIR = WORKSPACE / "assets"

WIDTH = 1080
HEIGHT = 1920
VID_W = 1080
VID_H = 608
VID_Y = 656
TOTAL_DUR = 74.0

# 1. Base Video Generation with Active Speaker Tracking
# - Host segment (0.0s - 8.6s): Host asks question -> Crop to host (X=1530)
# - Guest segment (8.6s - 74.0s): Guest gives monologue -> Crop to guest (X=190)
base_cut_mp4 = WORKSPACE / "ref3_speakers_base.mp4"
if not base_cut_mp4.exists():
    print("🎬 Generating active-speaker base video (Host -> Guest)...")
    host_mp4 = WORKSPACE / "ref3_cut_host.mp4"
    guest_mp4 = WORKSPACE / "ref3_cut_guest.mp4"
    vf_host = (
        "crop=2160:1215:1530:450,scale=1080:608:flags=lanczos,"
        "eq=contrast=1.12:saturation=0.85:brightness=-0.02,"
        "colorbalance=rs=0.04:gs=0.02:bs=-0.04,setsar=1,fps=30"
    )
    vf_guest = (
        "crop=2160:1215:190:450,scale=1080:608:flags=lanczos,"
        "eq=contrast=1.12:saturation=0.85:brightness=-0.02,"
        "colorbalance=rs=0.04:gs=0.02:bs=-0.04,setsar=1,fps=30"
    )
    subprocess.run([
        "ffmpeg", "-y", "-ss", "1988.0", "-t", "8.6",
        "-i", str(RAW_VIDEO), "-vf", vf_host, "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(host_mp4)
    ], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-ss", "1996.6", "-t", "65.4",
        "-i", str(RAW_VIDEO), "-vf", vf_guest, "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(guest_mp4)
    ], check=True)
    concat_txt = WORKSPACE / "ref3_speakers_concat.txt"
    concat_txt.write_text(f"file '{host_mp4}'\nfile '{guest_mp4}'\n")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(base_cut_mp4)
    ], check=True)
    print(f"✅ Active-speaker base video ready: {base_cut_mp4}")

# 2. Letterbox Canvas & Soft Black Bottom Gradient Fade
grad_overlay_png = WORKSPACE / "ref3_gradient_overlay.png"
if not grad_overlay_png.exists():
    grad_im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw_grad = ImageDraw.Draw(grad_im)
    draw_grad.rectangle([(0, VID_Y), (WIDTH, VID_Y + VID_H - 90)], fill=(0, 0, 0, 0))
    fade_start = VID_Y + VID_H - 90
    fade_end = VID_Y + VID_H
    for y in range(fade_start, fade_end):
        alpha = int(255 * ((y - fade_start) / 90.0))
        draw_grad.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))
    grad_im.save(grad_overlay_png)
    print(f"✅ Bottom gradient fade overlay saved: {grad_overlay_png}")

# 3. Audio Master: Pro Dialogue + Low-Volume Emotional Instrumental BGM (-23 dB)
pro_dialogue = WORKSPACE / "reel1_pro_mastered_audio.wav"
bgm_music = ASSETS_DIR / "audio" / "ramayan_flute_bgm.mp3"

# 4. Kinetic Subtitle Engine
font_p = str(ASSETS_DIR / "fonts" / "Anton-Regular.ttf")
font_base = ImageFont.truetype(font_p, 52)
font_large = ImageFont.truetype(font_p, 72)

# Placement Zones in 1080x1920 coordinates
# All safely inside 16:9 frame (Y=656..1264)
# Zone A: Left of speaker (X=75, Y=785)
# Zone B: Right of speaker (X=1005, Y=785, right-aligned)
# Zone C: Bottom-Center (X=540, Y=1140, center-aligned, just above gradient fade)
ZONES = {
    "A": {"x": 75, "y": 785, "align": "left"},
    "B": {"x": 1005, "y": 785, "align": "right"},
    "C": {"x": 540, "y": 1140, "align": "center"}
}

# Authentic Spoken Tanglish Clusters with -60ms Visual Lead Time
# Syllables matched directly to audio onset for instant snappy synchronization!
KINETIC_CLUSTERS = [
    # Cluster 1: Host asks Question (1.8s - 8.2s)
    # Audio: "சரி இந்த ராமாயணத்துல இருந்து நாம் என்ன வாழ்க்கை பாடம் எடுத்துக்கணும்?"
    (1.8, 8.2, [
        (2.0, "A", "RAMAYANATHULA IRUNDHU...", False),
        (3.7, "B", "NAAM ENNA...", False),
        (4.4, "C", "VAAZHKAI PAADAM\nEDUTHUKKANUM?", True)
    ]),

    # Cluster 2: Guest delivers Hook - Hanuman (8.3s - 15.3s)
    # Audio: "நான் வந்து ஹனுமான பத்தி மட்டும் பேச நினைக்கிறேன்... Everybody in this world is like Hanuman!"
    (8.3, 15.3, [
        (8.5, "A", "NAAN VANDHU...", False),
        (10.5, "B", "HANUMAN-A PATHI MATTUM\nPESA NENAIKKIREN!", True),
        (13.0, "C", "EVERYBODY IN THIS WORLD\nIS LIKE HANUMAN!", True)
    ]),

    # Cluster 3: Latent Potential & Mentor (15.5s - 22.3s)
    # Audio: "நமக்குள்ள Latent potential இருக்கு, but someone has to come and show it to us that's the mentor"
    (15.5, 22.3, [
        (15.8, "A", "NAMAKKULLA...", False),
        (16.3, "B", "LATENT POTENTIAL IRUKKU!", True),
        (17.6, "C", "SOMEONE HAS TO SHOW IT...", False),
        (19.2, "A", "THAT'S THE MENTOR!", True)
    ]),

    # Cluster 4: Winning with Mentor & Loyalty (22.4s - 26.0s)
    # Audio: "மெண்டார் இருந்தா ஜெயிக்கலாம்... ரெண்டாவது Loyalty!"
    (22.4, 26.0, [
        (22.5, "B", "MENTOR IRUNDHAA JAIKKALAAM!", False),
        (23.3, "A", "RENDAAVADHU...", False),
        (23.9, "C", "LOYALTY!", True)
    ]),

    # Cluster 5: Live Example - Friend's Staff Left After 2 Years (26.1s - 36.0s)
    # Audio: "இன்னைக்கு வந்த கலைஞர்/நண்பர் வருத்தப்பட்டார்... ஏன்னா அவர் ஸ்டாஃப் 2 வருஷம் வேலை பார்த்துட்டு சொல்லாம வேலைய விட்டுட்டாங்க"
    (26.1, 36.0, [
        (26.2, "A", "INNAIKKU VANDHAVAR...", False),
        (28.5, "B", "ROMBA VARUTHAPPATTAAR!", True),
        (30.3, "C", "AVAR STAFF 2 YEARS\nVELA PAATHUTTU...", False),
        (33.0, "A", "SOLLAAMA KOLLAAMA\nPOYITAANGA!", True)
    ]),

    # Cluster 6: If they had Loyalty (36.2s - 43.8s)
    # Audio: "அவர் சொல்லும்போது ரொம்ப upset ஆயிட்டாரு... Loyal-ஆ இருந்திருந்தா அவங்க இருந்திருப்பாங்க"
    (36.2, 43.8, [
        (36.4, "B", "AVAR SOLLUMPODHU...", False),
        (38.0, "A", "ROMBA UPSET AAYITAARU!", True),
        (40.1, "B", "LOYAL-AA IRUNDHURUNDHAA...", False),
        (42.3, "C", "AVANGA KOODAVE\nIRUNDHURUPPAANGA!", True)
    ]),

    # Cluster 7: People Lack Loyalty Today (44.0s - 55.4s)
    # Audio: "இன்னைக்கு பல பேர்கிட்ட இல்லாதது என்னன்னா... Loyalty இல்ல! இது ஒரு Live Example!"
    (44.0, 55.4, [
        (44.2, "A", "INNAIKKU PALA PERKITTA...", False),
        (47.0, "B", "LOYALTY-E ILLA!", True),
        (48.9, "C", "IDHU ORU LIVE EXAMPLE!", True)
    ]),

    # Cluster 8: Hanuman's Loyalty vs Today (55.6s - 63.4s)
    # Audio: "அவர் சொல்லும்போது எனக்கு ரொம்ப கஷ்டமா போச்சு... ஹனுமான் மாதிரி விசுவாசம் உள்ளவங்க எங்க?"
    (55.6, 63.4, [
        (55.8, "A", "AVAR SOLLUMPODHU...", False),
        (57.9, "B", "ROMBA KASHTAMAA POCHU...", False),
        (60.5, "C", "HANUMAN MAADHIRI\nLOYAL PEOPLE ENGEY?", True)
    ]),

    # Cluster 9: Climax - Life's Greatest Lesson (63.6s - 73.8s)
    # Audio: "ஹனுமான் காட்டிய அந்த தன்னலமற்ற விசுவாசம் தான்... வாழ்க்கையின் மிகப்பெரிய பாடம்!"
    (63.6, 73.8, [
        (63.8, "A", "HANUMAN KAATTIYA...", False),
        (65.9, "B", "SELFLESS LOYALTY DHAAN!", True),
        (68.8, "C", "LIFE-ODA GREATEST LESSON!", True)
    ])
]

def render_kinetic_subtitles_frame(active_zone_dict):
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    if not active_zone_dict:
        return im.tobytes()

    for zone_id, (text, is_emph) in active_zone_dict.items():
        f = font_large if is_emph else font_base
        z_info = ZONES[zone_id]
        x_base = z_info["x"]
        y_base = z_info["y"]
        align = z_info["align"]

        bbox = draw.multiline_textbbox((0, 0), text, font=f, align=align)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        if align == "left":
            draw_x = x_base
            draw_y = y_base - text_h // 2
        elif align == "right":
            draw_x = x_base - text_w
            draw_y = y_base - text_h // 2
        else: # center
            draw_x = x_base - text_w // 2
            draw_y = y_base - text_h // 2

        # 1. Multi-layer soft dark drop shadow for cinematic depth
        for ox, oy, alpha in [(6, 6, 220), (4, 4, 180), (2, 2, 140)]:
            draw.multiline_text((draw_x + ox, draw_y + oy), text, font=f, fill=(0, 0, 0, alpha), align=align)

        # 2. Clean 3px dark stroke outline to prevent background bleed
        draw.multiline_text(
            (draw_x, draw_y), text, font=f,
            fill=(255, 229, 0, 255),
            stroke_width=3,
            stroke_fill=(0, 0, 0, 240),
            align=align
        )

    return im.tobytes()

# Render animated subtitles MOV with alpha
subs_mov = WORKSPACE / "ref3_kinetic_subs.mov"
print("🎬 Rendering dynamic kinetic subtitle stream...")
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{HEIGHT}",
    "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(subs_mov)
], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_frames = int(round(TOTAL_DUR * 30))
blank_bytes = render_kinetic_subtitles_frame({})

for f_idx in range(total_frames):
    t_sec = f_idx / 30.0
    active_zone_dict = {}

    # Find active cluster
    for c_st, c_et, phrases in KINETIC_CLUSTERS:
        if c_st <= t_sec < c_et:
            # Add each phrase that has started up to t_sec into its zone
            for p_st, zone, txt, is_emph in phrases:
                if p_st <= t_sec:
                    active_zone_dict[zone] = (txt, is_emph)
            break

    raw_frame = render_kinetic_subtitles_frame(active_zone_dict) if active_zone_dict else blank_bytes
    proc.stdin.write(raw_frame)

proc.stdin.close()
proc.wait()
print(f"✅ Kinetic subtitles animated video rendered: {subs_mov}")

# 5. Final Master Assembly:
# Base 16:9 centered in 1080x1920 (pad=1080:1920:0:656:color=black)
# Overlay bottom gradient fade (ref3_gradient_overlay.png)
# Overlay kinetic subtitles (ref3_kinetic_subs.mov)
# Mux Pro Audio Master (-14 LUFS) with mild instrumental BGM (-23 dB)
final_out = EXPORT_DIR / "Reel_1_Reference_3_Style.mp4"
print(f"🎬 Assembling final Reel 1 in Reference 3 Style to: {final_out}")

filter_complex = (
    f"[0:v]pad={WIDTH}:{HEIGHT}:0:{VID_Y}:color=black,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[base];"
    f"[base][1:v]overlay=0:0[v_grad];"
    f"[v_grad][2:v]overlay=0:0[v];"
    f"[4:a]volume=0.06,afade=t=in:ss=0:d=1.0,afade=t=out:st=71.5:d=2.5[bgm];"
    f"[3:a][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[a]"
)

subprocess.run([
    "ffmpeg", "-y",
    "-i", str(base_cut_mp4),
    "-i", str(grad_overlay_png),
    "-i", str(subs_mov),
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

print(f"🎉 FINAL REEL 1 IN REFERENCE 3 STYLE EXPORTED: {final_out}")

# Extract Verification QA Frames
subprocess.run(["ffmpeg", "-y", "-ss", "5.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t5.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "11.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t11.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "18.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t18.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "24.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t24.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "33.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t33.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "42.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t42.5s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "50.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t50.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "61.0", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t61.0s.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-ss", "69.5", "-i", str(final_out), "-vframes", "1", str(FRAMES_DIR / "qa_ref3_kinetic_t69.5s.png")], check=True)
print("✅ QA verification frames extracted successfully!")
