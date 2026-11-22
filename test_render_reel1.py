#!/usr/bin/env python3
"""
Test render Reel 1 with authentic reference styling:
- 1080x1920 canvas (matching young entrepreneur reel part 3.mp4 & style-sheet.md)
- Clean Futura Bold 2-line Title Case banner (NO synthetic bloated outline!)
- Noto Sans Tamil Bold running subtitles (Active Orange #EA8207, others White #FFFFFF, 4px black outline, 2-4 words/line)
- Relevant B-Roll: broll_temple.mp4 inside active video window
- BGM ducked to -24 dB with sidechain compression
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
FFMPEG = "/Users/pgi/.local/bin/ffmpeg"

WORKSPACE_DIR = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
ASSETS_DIR = WORKSPACE_DIR / "assets"
BROLLS_DIR = ASSETS_DIR / "brolls"
FONTS_DIR = WORKSPACE_DIR / "fonts"
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
BGM_PATH = Path("/Users/pgi/Downloads/vidssave.com Royalty Free Music - Epic Inspiring Dramatic Cinematic Emotional Background _ FREE DOWNLOAD 1080P.mp4")

# 1080x1920 Exact Reference Layout
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920
TOP_BAR_H = 416
BANNER_Y = 416
BANNER_H = 142
VIDEO_Y = 558
VIDEO_W = 1080
VIDEO_H = 940
BOTTOM_BAR_Y = 1498
BOTTOM_BAR_H = 422

CROP_GUEST = "crop=1620:1410:150:280,scale=1080:940"
CROP_HOST = "crop=1620:1410:2070:280,scale=1080:940"
CROP_WIDE = "crop=2400:1410:720:280,scale=1080:940"

def make_clean_banner(line1, line2, emoji, out_path):
    img = Image.new("RGBA", (CANVAS_WIDTH, BANNER_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = 35
    draw.rounded_rectangle(
        [margin, 4, CANVAS_WIDTH - margin, BANNER_H - 4],
        radius=24,
        fill=(234, 130, 7, 255),
        outline=(0, 0, 0, 255),
        width=5
    )

    # Use Futura Bold (or Arial Bold)
    font_path = "/System/Library/Fonts/Supplemental/Futura.ttc"
    try:
        font = ImageFont.truetype(font_path, 44, index=2)
    except Exception:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 42)

    # Title Case Text
    text2 = f"{line2} {emoji}" if emoji else line2

    bbox1 = draw.textbbox((0, 0), line1, font=font)
    bbox2 = draw.textbbox((0, 0), text2, font=font)
    w1 = bbox1[2] - bbox1[0]
    w2 = bbox2[2] - bbox2[0]
    h1 = bbox1[3] - bbox1[1]
    h2 = bbox2[3] - bbox2[1]

    y1 = (BANNER_H - (h1 + h2 + 8)) // 2 - 4
    y2 = y1 + h1 + 10

    x1 = (CANVAS_WIDTH - w1) // 2
    x2 = (CANVAS_WIDTH - w2) // 2

    # Draw pure clean black text (NO artificial multi-pass dilation!)
    draw.text((x1, y1), line1, font=font, fill=(0, 0, 0, 255))
    draw.text((x2, y2), text2, font=font, fill=(0, 0, 0, 255))

    img.save(out_path, "PNG")
    print(f"✅ Clean banner generated: {out_path}")

def sec_to_ass(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def make_running_subs(cuts, ass_path):
    lines = []
    lines.append("[Script Info]")
    lines.append("Title: Reference Matched Subtitles")
    lines.append("ScriptType: v4.00+")
    lines.append(f"PlayResX: {CANVAS_WIDTH}")
    lines.append(f"PlayResY: {CANVAS_HEIGHT}")
    lines.append("WrapStyle: 0\n")

    # Use Noto Sans Tamil Bold font with 4px black outline
    lines.append("[V4+ Styles]")
    lines.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    lines.append("Style: Running,Noto Sans Tamil,52,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4,0,2,60,60,460,1\n")

    lines.append("[Events]")
    lines.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

    timeline_offset = 0.0
    for cut in cuts:
        cut_duration = cut["et"] - cut["st"]
        phrases = cut.get("phrases", [])
        for p_st, p_et, sentence in phrases:
            words = sentence.strip().split()
            n_words = len(words)
            if n_words == 0:
                continue

            # Split into chunks of 3 words per line
            chunk_size = 3
            for c_start in range(0, n_words, chunk_size):
                c_words = words[c_start : c_start + chunk_size]
                chunk_len = len(c_words)
                total_chunks = (n_words + chunk_size - 1) // chunk_size
                chunk_dur = (p_et - p_st) / total_chunks
                c_st = p_st + (c_start // chunk_size) * chunk_dur
                c_et = c_st + chunk_dur
                word_dur = chunk_dur / chunk_len

                for w_idx in range(chunk_len):
                    w_start = timeline_offset + c_st + (w_idx * word_dur)
                    w_end = timeline_offset + c_st + ((w_idx + 1) * word_dur)

                    parts = []
                    for j, word in enumerate(c_words):
                        if j == w_idx:
                            parts.append(r"{\c&H0782EA&}" + word)  # Active Orange #EA8207
                        else:
                            parts.append(r"{\c&HFFFFFF&}" + word)  # White
                    text_line = " ".join(parts)
                    start_str = sec_to_ass(w_start)
                    end_str = sec_to_ass(w_end)
                    lines.append(f"Dialogue: 0,{start_str},{end_str},Running,,0,0,0,,{text_line}")

        timeline_offset += cut_duration

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Subtitles generated: {ass_path}")

def render_test_reel():
    reel_id = 1
    title_l1 = "Why Do People"
    title_l2 = "Mock Ramayanam?"
    emoji = "🏹"
    banner_png = WORKSPACE_DIR / f"test_banner_{reel_id}.png"
    make_clean_banner(title_l1, title_l2, emoji, banner_png)

    cuts = [
        {"st": 121.0, "et": 127.5, "crop": CROP_HOST, "broll": None, "phrases": [
            (0.15, 3.20, "ஒரு கதையோ விஷயமோ பேசினா..."),
            (3.40, 6.20, "ராமாயணம் மாதிரி இழுக்காதீங்கன்னு சொல்றாங்க!")
        ]},
        {"st": 127.5, "et": 136.0, "crop": CROP_GUEST, "broll": None, "phrases": [
            (0.20, 4.10, "நாம ஏன் ராமாயணத்தை பத்தி பேசக் கூடாது?"),
            (4.30, 8.20, "அதை விட பெரிய வாழ்க்கை பாடம் எங்க இருக்கு?")
        ]},
        {"st": 136.0, "et": 143.0, "crop": None, "broll": str(BROLLS_DIR / "broll_temple.mp4"), "phrases": [
            (0.20, 3.40, "இன்னைக்கு இருக்கிற சினிமாக்கள் எல்லாமே"),
            (3.60, 6.80, "அந்த காப்பியங்களில் இருந்து வந்ததுதான்!")
        ]},
        {"st": 143.0, "et": 153.0, "crop": CROP_GUEST, "broll": None, "phrases": [
            (0.20, 4.80, "அதை வெறும் கதையா பார்க்காதீங்க..."),
            (5.00, 9.80, "மனித மனங்களை புரிஞ்சுக்கிற மிகப்பெரிய பாடம்!")
        ]}
    ]

    ass_path = WORKSPACE_DIR / f"test_subs_{reel_id}.ass"
    make_running_subs(cuts, ass_path)

    temp_cuts = []
    total_dur = 0.0

    for i, cut in enumerate(cuts):
        cut_dur = cut["et"] - cut["st"]
        total_dur += cut_dur
        cut_out = WORKSPACE_DIR / f"test_cut_{reel_id}_{i}.mp4"

        if cut["broll"]:
            cmd = [
                FFMPEG, "-y",
                "-ss", "0", "-t", f"{cut_dur:.3f}",
                "-i", cut["broll"],
                "-ss", f"{cut['st']:.3f}", "-t", f"{cut_dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-filter_complex",
                f"[0:v]scale={VIDEO_W}:{VIDEO_H}:force_original_aspect_ratio=increase,crop={VIDEO_W}:{VIDEO_H},setsar=1,fps=30[v]",
                "-map", "[v]", "-map", "1:a:0",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
                "-c:a", "pcm_s16le",
                str(cut_out)
            ]
        else:
            cmd = [
                FFMPEG, "-y",
                "-ss", f"{cut['st']:.3f}", "-t", f"{cut_dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-filter_complex",
                f"[0:v]{cut['crop']},setsar=1,fps=30[v]",
                "-map", "[v]", "-map", "0:a:0",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
                "-c:a", "pcm_s16le",
                str(cut_out)
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        temp_cuts.append(cut_out)

    concat_list = WORKSPACE_DIR / f"test_concat_{reel_id}.txt"
    with open(concat_list, "w") as f:
        for c in temp_cuts:
            f.write(f"file '{c}'\n")

    cuts_joined = WORKSPACE_DIR / f"test_joined_{reel_id}.mp4"
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", str(cuts_joined)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Composite: Letterbox + Banner + Video + Subs + Soft Ducked Music
    test_out = WORKSPACE_DIR / f"test_reel_{reel_id}.mp4"
    filter_complex = (
        f"color=c=black:s={CANVAS_WIDTH}x{CANVAS_HEIGHT}:d={total_dur:.3f}[bg];"
        f"[bg][0:v]overlay=0:{VIDEO_Y}[comp1];"
        f"[comp1][1:v]overlay=0:{BANNER_Y}[comp2];"
        f"[comp2]subtitles='{ass_path}':fontsdir='{FONTS_DIR}'[outv];"
        f"[0:a]volume=1.3,highpass=f=80,equalizer=f=3000:t=q:w=1.5:g=3,compand=attacks=0.02:decays=0.1:points=-60/-60|-20/-10|0/-1[clean_voice];"
        f"[2:a]volume=-24dB[bgm_vol];"
        f"[bgm_vol][clean_voice]sidechaincompress=threshold=0.06:ratio=6:attack=15:release=250[ducked_bgm];"
        f"[clean_voice][ducked_bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]"
    )

    comp_cmd = [
        FFMPEG, "-y",
        "-i", str(cuts_joined),
        "-i", str(banner_png),
        "-stream_loop", "-1", "-i", str(BGM_PATH),
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "320k",
        "-t", f"{total_dur:.3f}",
        str(test_out)
    ]
    subprocess.run(comp_cmd, check=True)
    print(f"🎬 TEST REEL RENDERED: {test_out}")

    # Extract QA frames at 3s, 10s, 18s, 26s
    for t, label in [(3, "hook"), (10, "speaking_sub"), (18, "broll"), (26, "climax")]:
        qa_frame = WORKSPACE_DIR / f"test_qa_{label}.jpg"
        subprocess.run([
            FFMPEG, "-y", "-ss", str(t), "-i", str(test_out),
            "-vframes", "1", str(qa_frame)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"📸 QA frame: {qa_frame}")

if __name__ == "__main__":
    render_test_reel()
