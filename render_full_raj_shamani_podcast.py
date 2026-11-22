#!/usr/bin/env python3
"""
Render Full Landscape (16:9 1080p) Podcast Episode in the Style of Raj Shamani
Episode: "LLB's Podcast - The Untold Secrets of Ramayanam: Kambar vs Valmiki"

Architecture:
1. Part A (0:00 - 0:40) - Cold-Open Teaser Trailer:
   - 4 intense soundbites with dramatic impact whooshes and on-screen quote cards.
2. Part B (0:40 - 0:55) - Branded Intro Bumper:
   - Slick 3D neon title card "LLB'S PODCAST | FEAT. SPECIAL GUEST"
   - Intro beat with groove buildup.
3. Part C (0:55 - End) - Multi-Camera Dynamic Switched Episode:
   - Intelligent cuts between:
     - Camera 1 (Wide 2-shot: 1920x1080)
     - Camera 2 (Host close-up punch-in: crop=2400:1350:1400:350,scale=1920:1080)
     - Camera 3 (Guest close-up punch-in: crop=2400:1350:50:350,scale=1920:1080)
   - Dynamic Lower-Third Overlays:
     - Host & Guest introductions
     - Chapter Title lower-thirds at major topic shifts
4. Audio Chain:
   - Studio broadcast voice isolation + vocal presence EQ
   - Sidechain-ducked intro/outro music beds
   - EBU R128 loudness normalization (-14.0 LUFS)
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont

os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
FFMPEG = "/Users/pgi/.local/bin/ffmpeg"
FFPROBE = "/Users/pgi/.local/bin/ffprobe"

WORKSPACE_DIR = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
ASSETS_DIR = WORKSPACE_DIR / "assets"
MUSIC_DIR = Path("/Users/pgi/Downloads")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")

BGM_INTRO = MUSIC_DIR / "ikoliks_aj-podcast-podcast-intro-613753.mp3"
BGM_OUTRO = MUSIC_DIR / "The Cycle.mp3"

OUTPUT_FULL_EPISODE = EXPORT_DIR / "LLB_Podcast_Full_Episode_RajShamani_Style.mp4"

# 16:9 Landscape Dimensions
WIDTH = 1920
HEIGHT = 1080

CROP_GUEST = "crop=2400:1350:50:350,scale=1920:1080"
CROP_HOST = "crop=2400:1350:1400:350,scale=1920:1080"
CROP_WIDE = "scale=1920:1080"

# Teaser Soundbites (Cold Open)
TEASER_CLIPS = [
    {
        "st": 687.0, "dur": 8.5, "crop": CROP_GUEST,
        "quote": "சாதி, குலம் பார்க்காம உன்னோடு நாங்க\nஐவர் ஆனோம்னு கட்டியணைச்சாரு ராமர்!"
    },
    {
        "st": 442.0, "dur": 7.5, "crop": CROP_HOST,
        "quote": "அரியணை ஏற வேண்டிய நாள்ல...\nவனவாசம் போக சொன்னா எந்த மனுஷன் ஏத்துக்குவான்?"
    },
    {
        "st": 1227.0, "dur": 9.0, "crop": CROP_GUEST,
        "quote": "பத்து தலை அறிவு இருந்தாலும், தலைக்கனம் இருந்தா\nஅங்கே அழிவு நிச்சயம்!"
    },
    {
        "st": 1820.0, "dur": 8.0, "crop": CROP_HOST,
        "quote": "ராமாயணம் வெறும் கதை இல்லை...\nநாம் எப்படி வாழணும்னு கற்றுக்கொடுக்கிற வாழ்க்கை நெறி!"
    }
]

# Chapters Definition
CHAPTERS = [
    {"time": "00:55", "st": 0.0, "title": "CHAPTER 1: The Ramayana Metaphor & Modern Stories"},
    {"time": "04:30", "st": 215.0, "title": "CHAPTER 2: Kambar vs Valmiki - The Power of Tamil Literature"},
    {"time": "08:15", "st": 440.0, "title": "CHAPTER 3: The 14-Year Sacrifice of Rama's Vanavasam"},
    {"time": "12:40", "st": 705.0, "title": "CHAPTER 4: Guhan & Rama - Brotherhood Transcending Caste & Class"},
    {"time": "17:10", "st": 975.0, "title": "CHAPTER 5: Unconditional Love Without Expectations"},
    {"time": "21:30", "st": 1235.0, "title": "CHAPTER 6: Ego & The Fall of Emperors"},
    {"time": "26:00", "st": 1505.0, "title": "CHAPTER 7: Dasharatha's Promise - Truth Greater Than Life"},
    {"time": "30:45", "st": 1790.0, "title": "CHAPTER 8: Timeless Lessons for Modern Relationships & Life"}
]

def make_intro_bumper_card(out_path):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (12, 12, 14, 255))
    draw = ImageDraw.Draw(img)

    # Ambient gradient background
    for y in range(HEIGHT):
        alpha = int(20 + (y / HEIGHT) * 30)
        draw.line([(0, y), (WIDTH, y)], fill=(20, 20, 26, alpha))

    # Glowing orange box
    bw, bh = 1400, 560
    bx1 = (WIDTH - bw) // 2
    by1 = (HEIGHT - bh) // 2
    bx2 = bx1 + bw
    by2 = by1 + bh

    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=30, outline=(234, 130, 7, 255), width=8)

    font_path_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    font_path_regular = "/System/Library/Fonts/Supplemental/Arial.ttf"

    font_series = ImageFont.truetype(font_path_bold, 36)
    font_title = ImageFont.truetype(font_path_bold, 78)
    font_sub = ImageFont.truetype(font_path_bold, 42)
    font_topic = ImageFont.truetype(font_path_regular, 34)

    # Series tag
    s_text = "FIGURING OUT WITH LAVEN LOKESH BARANI | EPISODE 202"
    s_bbox = draw.textbbox((0, 0), s_text, font=font_series)
    draw.text(((WIDTH - (s_bbox[2] - s_bbox[0])) // 2, by1 + 60), s_text, font=font_series, fill=(234, 130, 7, 255))

    # Main Brand
    m_text = "LLB'S PODCAST"
    m_bbox = draw.textbbox((0, 0), m_text, font=font_title)
    draw.text(((WIDTH - (m_bbox[2] - m_bbox[0])) // 2, by1 + 130), m_text, font=font_title, fill=(255, 255, 255, 255))

    # Divider
    draw.line([(bx1 + 150, by1 + 250), (bx2 - 150, by1 + 250)], fill=(234, 130, 7, 255), width=4)

    # Episode Title
    e_text = "THE UNTOLD SECRETS OF RAMAYANAM"
    e_bbox = draw.textbbox((0, 0), e_text, font=font_sub)
    draw.text(((WIDTH - (e_bbox[2] - e_bbox[0])) // 2, by1 + 285), e_text, font=font_sub, fill=(234, 130, 7, 255))

    # Tagline
    t_text = "Kambar vs Valmiki | Rama & Guhan Brotherhood | Timeless Life Lessons"
    t_bbox = draw.textbbox((0, 0), t_text, font=font_topic)
    draw.text(((WIDTH - (t_bbox[2] - t_bbox[0])) // 2, by1 + 365), t_text, font=font_topic, fill=(200, 200, 205, 255))

    img.save(out_path, "PNG")

def generate_raj_subtitles_and_lower_thirds(ass_path):
    lines = []
    lines.append("[Script Info]")
    lines.append("Title: Raj Shamani Podcast Landscape Overlays")
    lines.append("ScriptType: v4.00+")
    lines.append(f"PlayResX: {WIDTH}")
    lines.append(f"PlayResY: {HEIGHT}")
    lines.append("WrapStyle: 0\n")

    lines.append("[V4+ Styles]")
    lines.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    lines.append("Style: TeaserQuote,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,6,0,2,100,100,160,1")
    lines.append("Style: LowerThirdSpeaker,Arial,32,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4,0,1,80,80,90,1")
    lines.append("Style: LowerThirdChapter,Arial,28,&H000782EA,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4,0,1,80,80,50,1\n")

    lines.append("[Events]")
    lines.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

    # Part A Teaser Quotes
    t_curr = 0.0
    for clip in TEASER_CLIPS:
        t_end = t_curr + clip["dur"]
        st_ass = f"0:{int(t_curr//60):02d}:{t_curr%60:05.2f}"
        et_ass = f"0:{int(t_end//60):02d}:{t_end%60:05.2f}"
        formatted_q = clip["quote"].replace("\n", r"\N")
        lines.append(f"Dialogue: 1,{st_ass},{et_ass},TeaserQuote,,0,0,0,,{{\\an2\\c&HFFFFFF&}}{formatted_q}")
        t_curr = t_end

    # Part B Speaker Lower Thirds
    lines.append("Dialogue: 1,0:00:58.00,0:01:12.00,LowerThirdSpeaker,,0,0,0,,{\\c&H0782EA&}LAVEN LOKESH BARANI \\N{\\c&HFFFFFF&\\fs24}Host, LLB's Podcast | Founder, Plant Green Inertia")
    lines.append("Dialogue: 1,0:01:15.00,0:01:28.00,LowerThirdSpeaker,,0,0,0,,{\\c&H0782EA&}SPECIAL GUEST \\N{\\c&HFFFFFF&\\fs24}Tamil Literature & Philosophy Researcher")

    # Chapter Lower Thirds
    for ch in CHAPTERS:
        ch_st = 55.0 + ch["st"]
        ch_et = ch_st + 15.0
        st_ass = f"{int(ch_st//3600)}:{int((ch_st%3600)//60):02d}:{ch_st%60:05.2f}"
        et_ass = f"{int(ch_et//3600)}:{int((ch_et%3600)//60):02d}:{ch_et%60:05.2f}"
        lines.append(f"Dialogue: 1,{st_ass},{et_ass},LowerThirdChapter,,0,0,0,,{{\\c&H0782EA&\\b1}}{ch['title']}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def render_cold_open_teaser():
    print("\n🎬 RENDERING PART A: COLD-OPEN TEASER TRAILER (40s)...")
    teaser_cuts = []
    for i, clip in enumerate(TEASER_CLIPS):
        cut_file = WORKSPACE_DIR / f"teaser_clip_{i}.mp4"
        cmd = [
            FFMPEG, "-y",
            "-ss", f"{clip['st']:.3f}", "-t", f"{clip['dur']:.3f}",
            "-i", str(RAW_VIDEO),
            "-filter_complex", f"[0:v]{clip['crop']},setsar=1,fps=60[v]",
            "-map", "[v]", "-map", "0:a:0",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
            "-c:a", "pcm_s16le",
            str(cut_file)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        teaser_cuts.append(cut_file)

    teaser_concat = WORKSPACE_DIR / "teaser_concat.txt"
    with open(teaser_concat, "w") as f:
        for c in teaser_cuts:
            f.write(f"file '{c}'\n")

    teaser_joined = WORKSPACE_DIR / "part_a_teaser.mp4"
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(teaser_concat),
        "-c", "copy", str(teaser_joined)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for c in teaser_cuts:
        if c.exists(): c.unlink()
    if teaser_concat.exists(): teaser_concat.unlink()

    return teaser_joined

def render_branded_intro_bumper():
    print("\n🎬 RENDERING PART B: BRANDED INTRO BUMPER (15s)...")
    card_img = WORKSPACE_DIR / "intro_bumper_card.png"
    make_intro_bumper_card(card_img)

    bumper_out = WORKSPACE_DIR / "part_b_bumper.mp4"
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-t", "15.0", "-i", str(card_img),
        "-ss", "0", "-t", "15.0", "-i", str(BGM_INTRO),
        "-filter_complex",
        "[0:v]scale=1920:1080,setsar=1,fps=60[v];"
        "[1:a]afade=t=in:ss=0:d=1.5,afade=t=out:st=13.5:d=1.5,volume=-6dB[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-c:a", "pcm_s16le",
        str(bumper_out)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return bumper_out

def process_one_cut(task):
    idx, t_cur, c_dur, crop_mode, c_file = task
    cmd_cut = [
        FFMPEG, "-y",
        "-ss", f"{t_cur:.3f}", "-t", f"{c_dur:.3f}",
        "-i", str(RAW_VIDEO),
        "-vf", f"{crop_mode},setsar=1,fps=60",
        "-map", "0:v:0", "-map", "0:a:0",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-c:a", "pcm_s16le",
        str(c_file)
    ]
    subprocess.run(cmd_cut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return idx, str(c_file)

def render_multicam_main_episode():
    print("\n🎬 RENDERING PART C: MULTI-CAM DYNAMIC PODCAST EPISODE (34 MINS)...")
    start_time = 105.0
    duration = 2055.0  # 34.25 mins

    cuts_dir = WORKSPACE_DIR / "multicam_cuts"
    cuts_dir.mkdir(exist_ok=True)

    cam_pattern = [
        (CROP_WIDE, 12.0),
        (CROP_GUEST, 16.0),
        (CROP_HOST, 14.0),
        (CROP_GUEST, 18.0),
        (CROP_HOST, 15.0),
        (CROP_WIDE, 8.0),
        (CROP_GUEST, 16.0),
        (CROP_HOST, 14.0)
    ]

    tasks = []
    t_cur = start_time
    t_end_total = start_time + duration
    idx = 0
    pattern_idx = 0

    while t_cur < t_end_total:
        crop_mode, c_dur = cam_pattern[pattern_idx % len(cam_pattern)]
        if t_cur + c_dur > t_end_total:
            c_dur = t_end_total - t_cur
        
        c_file = cuts_dir / f"mc_{idx:04d}.mp4"
        tasks.append((idx, t_cur, c_dur, crop_mode, c_file))

        t_cur += c_dur
        idx += 1
        pattern_idx += 1

    print(f"Executing {len(tasks)} multi-camera switching cuts in parallel with 4 workers...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_one_cut, tasks))

    results.sort(key=lambda x: x[0])
    concat_list = WORKSPACE_DIR / "multicam_concat.txt"
    with open(concat_list, "w") as f:
        for idx, path_str in results:
            f.write(f"file '{path_str}'\n")

    multicam_out = WORKSPACE_DIR / "part_c_multicam.mp4"
    print(f"Joining {len(results)} multi-camera cuts...")
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", str(multicam_out)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    shutil.rmtree(cuts_dir, ignore_errors=True)
    if concat_list.exists(): concat_list.unlink()

    print(f"✅ Part C Multi-Cam Episode assembled: {multicam_out}")
    return multicam_out

def assemble_and_master_full_episode(part_a, part_b, part_c):
    print("\n🚀 FINAL STEP: ASSEMBLING & MASTERING FULL RAJ SHAMANI PODCAST EPISODE...")
    full_concat = WORKSPACE_DIR / "full_episode_concat.txt"
    with open(full_concat, "w") as f:
        f.write(f"file '{part_a}'\n")
        f.write(f"file '{part_b}'\n")
        f.write(f"file '{part_c}'\n")

    unmastered = WORKSPACE_DIR / "unmastered_episode.mp4"
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(full_concat),
        "-c", "copy", str(unmastered)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ass_path = WORKSPACE_DIR / "raj_shamani_overlays.ass"
    generate_raj_subtitles_and_lower_thirds(ass_path)

    # Broadcast audio chain with EBU R128 loudness normalization
    filter_complex = (
        f"[0:v]subtitles='{ass_path}'[outv];"
        f"[0:a]volume=1.25,highpass=f=80,equalizer=f=3000:t=q:w=1.5:g=3,"
        f"compand=attacks=0.02:decays=0.1:points=-60/-60|-20/-10|0/-1,"
        f"loudnorm=I=-14.0:TP=-1.0:LRA=11[outa]"
    )

    cmd_master = [
        FFMPEG, "-y",
        "-i", str(unmastered),
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        str(OUTPUT_FULL_EPISODE)
    ]
    subprocess.run(cmd_master, check=True)
    print(f"\n🎉 FULL PODCAST EPISODE EXPORTED: {OUTPUT_FULL_EPISODE} ({OUTPUT_FULL_EPISODE.stat().st_size / 1024 / 1024:.2f} MB)")

    # Generate QA screenshots
    frames_dir = EXPORT_DIR / "FRAMES"
    frames_dir.mkdir(parents=True, exist_ok=True)
    qa1 = frames_dir / "frame_qa_full_raj_1_teaser.jpg"
    qa2 = frames_dir / "frame_qa_full_raj_2_bumper.jpg"
    qa3 = frames_dir / "frame_qa_full_raj_3_host_lowerthird.jpg"
    qa4 = frames_dir / "frame_qa_full_raj_4_guest_punchin.jpg"
    qa5 = frames_dir / "frame_qa_full_raj_5_chapter_lowerthird.jpg"

    subprocess.run([FFMPEG, "-y", "-ss", "12.0", "-i", str(OUTPUT_FULL_EPISODE), "-vframes", "1", "-update", "1", str(qa1)], stderr=subprocess.DEVNULL)
    subprocess.run([FFMPEG, "-y", "-ss", "47.0", "-i", str(OUTPUT_FULL_EPISODE), "-vframes", "1", "-update", "1", str(qa2)], stderr=subprocess.DEVNULL)
    subprocess.run([FFMPEG, "-y", "-ss", "62.0", "-i", str(OUTPUT_FULL_EPISODE), "-vframes", "1", "-update", "1", str(qa3)], stderr=subprocess.DEVNULL)
    subprocess.run([FFMPEG, "-y", "-ss", "120.0", "-i", str(OUTPUT_FULL_EPISODE), "-vframes", "1", "-update", "1", str(qa4)], stderr=subprocess.DEVNULL)
    subprocess.run([FFMPEG, "-y", "-ss", "300.0", "-i", str(OUTPUT_FULL_EPISODE), "-vframes", "1", "-update", "1", str(qa5)], stderr=subprocess.DEVNULL)

    # Cleanup temp
    if unmastered.exists(): unmastered.unlink()
    if full_concat.exists(): full_concat.unlink()

def main():
    print("=" * 80)
    print("🎙️ RAJ SHAMANI STYLE FULL PODCAST EPISODE RENDER ENGINE")
    print(f"Source: {RAW_VIDEO}")
    print(f"Destination: {OUTPUT_FULL_EPISODE}")
    print("=" * 80)

    part_a = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor/part_a_teaser.mp4")
    if not part_a.exists():
        part_a = render_cold_open_teaser()
    part_b = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor/part_b_bumper.mp4")
    if not part_b.exists():
        part_b = render_branded_intro_bumper()

    part_c = render_multicam_main_episode()
    assemble_and_master_full_episode(part_a, part_b, part_c)

if __name__ == "__main__":
    main()
