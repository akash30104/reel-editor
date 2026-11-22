#!/usr/bin/env python3
"""
Render 8 Native 4K Reels from 202.MOV with Authentic Ramayana / Literary Discussion Content
Features:
- Native 4K Vertical Canvas (2160x3840)
- Single Big Bold English Title Banner in Orange (#EA8207) with PNG Emojis
- Multi-camera dynamic crop switching (Guest: x=150, Host: x=1500, Wide: x=840)
- Thematic B-Rolls: Book (Literature), Forest (Vanavasam), River (Guhan), Fire (Ego), Sunrise (Wisdom), Clock (Promise)
- Word-by-word dynamic running Tamil subtitles (Active word Orange #EA8207, others White #FFFFFF, 10px black stroke)
- Audio: Broadcast EQ/compression + FFmpeg sidechain ducked BGM
"""

import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Set environment
os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
FFMPEG = "/Users/pgi/.local/bin/ffmpeg"
FFPROBE = "/Users/pgi/.local/bin/ffprobe"

WORKSPACE_DIR = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
ASSETS_DIR = WORKSPACE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
BROLLS_DIR = ASSETS_DIR / "brolls"
MUSIC_DIR = Path("/Users/pgi/Downloads")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
EMOJIS_DIR = ASSETS_DIR / "emojis"

# Geometry
CANVAS_WIDTH = 2160
CANVAS_HEIGHT = 3840
VIDEO_WIDTH = 2160
VIDEO_HEIGHT = 1880
VIDEO_Y = 1116
BANNER_Y = 600
BANNER_HEIGHT = 280

CROP_GUEST = "crop=2160:1880:150:280"
CROP_HOST = "crop=2160:1880:1500:280"
CROP_WIDE = "crop=2160:1880:840:280"

BGM_GROOVE = MUSIC_DIR / "ikoliks_aj-podcast-podcast-intro-613753.mp3"
BGM_EMOTIONAL = MUSIC_DIR / "The Cycle.mp3"

# 8 Authentic Reel Configurations
REELS = [
    {
        "id": 1,
        "title": "WHY DO PEOPLE MOCK RAMAYANAM?",
        "emoji1": "broken_heart.png", "emoji2": "fire.png",
        "filename": "Reel_202_1_Why_Mock_Ramayana.mp4",
        "bgm": BGM_GROOVE, "bgm_gain": -17.5,
        "cuts": [
            {"st": 121.0, "et": 127.5, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.15, 3.20, "ஒரு கதையோ விஷயமோ பேசினா..."),
                (3.40, 6.20, "ராமாயணம் மாதிரி இழுக்காதீங்கன்னு சொல்றாங்க!")
            ]},
            {"st": 127.5, "et": 136.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.10, "நாம ஏன் ராமாயணத்தை பத்தி பேசக் கூடாது?"),
                (4.30, 8.20, "அதை விட பெரிய வாழ்க்கை பாடம் எங்க இருக்கு?")
            ]},
            {"st": 136.0, "et": 143.0, "crop": None, "broll": str(BROLLS_DIR / "broll_book.mp4"), "phrases": [
                (0.20, 3.40, "இன்னைக்கு இருக்கிற சினிமாக்கள் எல்லாமே"),
                (3.60, 6.80, "அந்த காப்பியங்களில் இருந்து வந்ததுதான்!")
            ]},
            {"st": 143.0, "et": 153.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "அதை வெறும் கதையா பார்க்காதீங்க..."),
                (5.00, 9.80, "மனித மனங்களை புரிஞ்சுக்கிற மிகப்பெரிய பாடம்!")
            ]}
        ]
    },
    {
        "id": 2,
        "title": "KAMBAR VS VALMIKI: WHO IS GREATER?",
        "emoji1": "fire.png", "emoji2": "target.png",
        "filename": "Reel_202_2_Kambar_Vs_Valmiki.mp4",
        "bgm": BGM_GROOVE, "bgm_gain": -17.5,
        "cuts": [
            {"st": 334.0, "et": 341.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.40, "வால்மீகி எழுதின மூல ராமாயணத்துக்கும்,"),
                (3.60, 6.80, "கம்பர் எழுதின காவியத்துக்கும் என்ன வித்தியாசம்?")
            ]},
            {"st": 341.0, "et": 350.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.20, "வால்மீகி கதையை சொன்னாருன்னா,"),
                (4.40, 8.80, "கம்பர் அதை தமிழ் உணர்வோட உயிர்ப்பிச்சாரு!")
            ]},
            {"st": 350.0, "et": 357.0, "crop": None, "broll": str(BROLLS_DIR / "broll_book.mp4"), "phrases": [
                (0.25, 3.30, "தமிழ் மொழிக்கு கம்பர் கொடுத்த"),
                (3.50, 6.80, "கவிதை நயம் உலகத்துல வேற எங்கேயும் இல்லை!")
            ]},
            {"st": 357.0, "et": 367.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "ஒவ்வொரு சொல்லிலும் அன்பையும் தர்மத்தையும்"),
                (5.00, 9.70, "அழகா வடித்த கவிச்சக்கரவர்த்தி கம்பர்!")
            ]}
        ]
    },
    {
        "id": 3,
        "title": "THE 14-YEAR SACRIFICE OF RAMA",
        "emoji1": "broken_heart.png", "emoji2": "warning.png",
        "filename": "Reel_202_3_Sacrifice_Of_Vanavasam.mp4",
        "bgm": BGM_EMOTIONAL, "bgm_gain": -9.5,
        "cuts": [
            {"st": 442.0, "et": 449.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.20, "அரியணை ஏற வேண்டிய நாள்ல..."),
                (3.40, 6.80, "வனவாசம் போகணும்னு சொன்னா எப்படி இருக்கும்?")
            ]},
            {"st": 449.0, "et": 458.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.20, "எந்த ஒரு வருத்தமும் கோபமும் இல்லாம,"),
                (4.40, 8.80, "அப்பா சொன்ன வாக்கை காப்பாத்த காட்டுக்கு போனார்!")
            ]},
            {"st": 458.0, "et": 466.0, "crop": None, "broll": str(BROLLS_DIR / "broll_forest.mp4"), "phrases": [
                (0.25, 3.60, "பதவியும் பணமும் முக்கியம் இல்லை..."),
                (3.80, 7.80, "தர்மமும் கடமையும் தான் முக்கியம்னு காட்டுனாரு!")
            ]},
            {"st": 466.0, "et": 476.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "வாழ்க்கை கஷ்டத்தை தரும்போது தப்பிச்சு ஓடாதீங்க..."),
                (5.00, 9.80, "அமைதியா ஏத்துக்கிட்டு நிமிர்ந்து நில்லுங்க!")
            ]}
        ]
    },
    {
        "id": 4,
        "title": "RAMA & GUHAN: TRUE BROTHERHOOD",
        "emoji1": "target.png", "emoji2": "fire.png",
        "filename": "Reel_202_4_Rama_And_Guhan_Brotherhood.mp4",
        "bgm": BGM_EMOTIONAL, "bgm_gain": -9.5,
        "cuts": [
            {"st": 680.0, "et": 687.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.20, "வேடுவத் தலைவன் குகனை"),
                (3.40, 6.80, "ராமர் எப்படி தன் சகோதரனா ஏத்துக்கிட்டாரு?")
            ]},
            {"st": 687.0, "et": 697.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.60, "சாதி, குலம், அந்தஸ்து எதையும் பார்க்காம..."),
                (4.80, 9.80, "உன்னோடு நாங்க ஐவர் ஆனோம்னு கட்டியணைச்சாரு!")
            ]},
            {"st": 697.0, "et": 705.0, "crop": None, "broll": str(BROLLS_DIR / "broll_river.mp4"), "phrases": [
                (0.25, 3.60, "கங்கை நதிக்கரையில நடந்த இந்த சந்திப்பு,"),
                (3.80, 7.80, "மனிதகுலத்துக்கே சமத்துவத்தை கற்றுக்கொடுத்தது!")
            ]},
            {"st": 705.0, "et": 715.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.60, "உண்மையான நட்புக்கு அடையாளம் அந்தஸ்து இல்லை..."),
                (4.80, 9.80, "இதயத்தின் தூய்மை மட்டும்தான்!")
            ]}
        ]
    },
    {
        "id": 5,
        "title": "PURE LOVE WITHOUT EXPECTATIONS",
        "emoji1": "broken_heart.png", "emoji2": "fire.png",
        "filename": "Reel_202_5_Love_Without_Expectations.mp4",
        "bgm": BGM_EMOTIONAL, "bgm_gain": -9.5,
        "cuts": [
            {"st": 920.0, "et": 927.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.20, "ராமர் படுத்து தூங்குறதை பார்த்து"),
                (3.40, 6.80, "குகன் ஏன் அவ்வளவு கண்ணீர் விட்டாரு?")
            ]},
            {"st": 927.0, "et": 937.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.80, "அரண்மனையில தூங்க வேண்டியவர் புல் தரையில..."),
                (5.00, 9.80, "அந்த வேதனையை அவனால தாங்கவே முடியல!")
            ]},
            {"st": 937.0, "et": 945.0, "crop": None, "broll": str(BROLLS_DIR / "broll_sunrise.mp4"), "phrases": [
                (0.25, 3.60, "எந்த எதிர்பார்ப்பும் இல்லாம அன்பு செலுத்துறதுதான்,"),
                (3.80, 7.80, "இந்த உலகத்திலேயே மிக உயர்ந்த குணம்!")
            ]},
            {"st": 945.0, "et": 955.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "உங்களை உண்மையா நேசிக்கிறவங்களை என்னைக்குமே,"),
                (5.00, 9.80, "அவங்க அன்பை குறைச்சு மதிப்பிடாதீங்க!")
            ]}
        ]
    },
    {
        "id": 6,
        "title": "EGO WILL DESTROY YOUR EMPIRE!",
        "emoji1": "warning.png", "emoji2": "fire.png",
        "filename": "Reel_202_6_Ego_Destroys_Everything.mp4",
        "bgm": BGM_GROOVE, "bgm_gain": -17.5,
        "cuts": [
            {"st": 1220.0, "et": 1227.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.20, "அவ்வளவு வலிமை இருந்தும் ராவணன் ஏன்"),
                (3.40, 6.80, "கடைசியில தன் சாம்ராஜ்யத்தையே இழந்தான்?")
            ]},
            {"st": 1227.0, "et": 1237.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.80, "பத்து தலை அறிவு இருந்தாலும்... தலைக்கனம் இருந்தா,"),
                (5.00, 9.80, "அங்கே அழிவு நிச்சயம்னு நிரூபிச்சது அவனோட ஈகோ!")
            ]},
            {"st": 1237.0, "et": 1245.0, "crop": None, "broll": str(BROLLS_DIR / "broll_fire.mp4"), "phrases": [
                (0.25, 3.60, "ஈகோ ஒரு தீ மாதிரி... மத்தவங்களை எரிக்கிறதுக்கு முன்னாடி,"),
                (3.80, 7.80, "முதல்ல உங்களையே சாம்பலாக்கிடும்!")
            ]},
            {"st": 1245.0, "et": 1255.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "எவ்வளவு உயரத்துக்கு போனாலும் அடக்கம் இல்லேன்னா,"),
                (5.00, 9.80, "கீழே விழும்போது தாங்க ஆள் இருக்காது!")
            ]}
        ]
    },
    {
        "id": 7,
        "title": "NEVER BREAK A SACRED PROMISE!",
        "emoji1": "target.png", "emoji2": "fire.png",
        "filename": "Reel_202_7_Your_Word_Is_Your_Power.mp4",
        "bgm": BGM_GROOVE, "bgm_gain": -17.5,
        "cuts": [
            {"st": 1480.0, "et": 1487.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.20, "இன்னைக்கு ஒரு வார்த்தை சொன்னா,"),
                (3.40, 6.80, "அடுத்த நிமிஷமே மாத்திப் பேசுறாங்க!")
            ]},
            {"st": 1487.0, "et": 1497.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.80, "சொல் தவறாமைங்கிறது தான் ஒரு மனுஷனோட"),
                (5.00, 9.80, "மிகப்பெரிய நற்குணம்... அதற்காக உயிரையே கொடுத்தாங்க!")
            ]},
            {"st": 1497.0, "et": 1505.0, "crop": None, "broll": str(BROLLS_DIR / "broll_clock.mp4"), "phrases": [
                (0.25, 3.60, "காலம் மாறும்... ஆனா நீங்க கொடுத்த வாக்கு"),
                (3.80, 7.80, "உங்க நேர்மையை உலகத்துக்கு பறைசாற்றும்!")
            ]},
            {"st": 1505.0, "et": 1515.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "வாக்கு தவறாத மனிதனுக்கு என்னைக்குமே"),
                (5.00, 9.80, "தோல்விங்கிறதே கிடையாது!")
            ]}
        ]
    },
    {
        "id": 8,
        "title": "THE TIMELESS LESSONS OF LIFE",
        "emoji1": "target.png", "emoji2": "fire.png",
        "filename": "Reel_202_8_Timeless_Lessons_Of_Life.mp4",
        "bgm": BGM_EMOTIONAL, "bgm_gain": -9.5,
        "cuts": [
            {"st": 1820.0, "et": 1827.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.20, "ராமாயணம் நமக்கு கத்துக்கொடுக்கிற"),
                (3.40, 6.80, "மிக முக்கியமான வாழ்க்கை பாடம் என்ன?")
            ]},
            {"st": 1827.0, "et": 1837.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.80, "வெற்றி, தோல்வி, இன்பம், துன்பம் எல்லாத்தையும்"),
                (5.00, 9.80, "சமமா ஏத்துக்கிட்டு தர்மத்தோடு வாழ கத்துக்கணும்!")
            ]},
            {"st": 1837.0, "et": 1845.0, "crop": None, "broll": str(BROLLS_DIR / "broll_sunrise.mp4"), "phrases": [
                (0.25, 3.60, "எந்த சூழ்நிலையிலும் நற்குணத்தை விட்டுடாதீங்க..."),
                (3.80, 7.80, "அதுதான் உங்களை தலைமுறை கடந்து வாழ வைக்கும்!")
            ]},
            {"st": 1845.0, "et": 1855.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "இந்த உண்மையை புரிஞ்சுகிட்டா போதும்..."),
                (5.00, 9.80, "வாழ்க்கையில எந்த புயல் வந்தாலும் ஜெயிக்கலாம்!")
            ]}
        ]
    }
]

def make_header_banner(title, emoji1_name, emoji2_name, out_path):
    img = Image.new("RGBA", (CANVAS_WIDTH, BANNER_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    banner_margin = 60
    banner_x1 = banner_margin
    banner_x2 = CANVAS_WIDTH - banner_margin
    banner_y1 = 0
    banner_y2 = BANNER_HEIGHT

    # Orange rounded banner rectangle
    draw.rounded_rectangle(
        [banner_x1, banner_y1, banner_x2, banner_y2],
        radius=40,
        fill=(234, 130, 7, 255),
        outline=(0, 0, 0, 255),
        width=10
    )

    font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    font_size = 72
    font = ImageFont.truetype(font_path, font_size)

    # Load emojis
    em1 = Image.open(EMOJIS_DIR / emoji1_name).convert("RGBA").resize((110, 110), Image.Resampling.LANCZOS)
    em2 = Image.open(EMOJIS_DIR / emoji2_name).convert("RGBA").resize((110, 110), Image.Resampling.LANCZOS)

    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    total_w = 110 + 35 + text_w + 35 + 110

    start_x = (CANVAS_WIDTH - total_w) // 2
    em_y = (BANNER_HEIGHT - 110) // 2
    text_y = (BANNER_HEIGHT - font_size) // 2 - 8

    # Paste Emoji 1
    img.paste(em1, (start_x, em_y), em1)

    # Text with heavy black outline
    tx = start_x + 110 + 35
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            if dx != 0 or dy != 0:
                draw.text((tx + dx, text_y + dy), title, font=font, fill=(0, 0, 0, 255))
    draw.text((tx, text_y), title, font=font, fill=(0, 0, 0, 255))

    # Paste Emoji 2
    img.paste(em2, (tx + text_w + 35, em_y), em2)

    img.save(out_path, "PNG")

def sec_to_ass(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def generate_running_subtitles(cuts, ass_path):
    lines = []
    lines.append("[Script Info]")
    lines.append("Title: 4K Running Subtitles")
    lines.append("ScriptType: v4.00+")
    lines.append(f"PlayResX: {CANVAS_WIDTH}")
    lines.append(f"PlayResY: {CANVAS_HEIGHT}")
    lines.append("WrapStyle: 0\n")

    lines.append("[V4+ Styles]")
    lines.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    lines.append("Style: Running,Arial,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,10,0,2,80,80,680,1\n")

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
            phrase_dur = p_et - p_st
            word_dur = phrase_dur / n_words

            for w_idx in range(n_words):
                w_start = timeline_offset + p_st + (w_idx * word_dur)
                w_end = timeline_offset + p_st + ((w_idx + 1) * word_dur)

                parts = []
                for j, word in enumerate(words):
                    if j == w_idx:
                        parts.append(r"{\c&H0782EA&}" + word)  # Active Orange #EA8207
                    else:
                        parts.append(r"{\c&HFFFFFF&}" + word)  # Inactive White
                text_line = " ".join(parts)
                start_str = sec_to_ass(w_start)
                end_str = sec_to_ass(w_end)
                lines.append(f"Dialogue: 0,{start_str},{end_str},Running,,0,0,0,,{text_line}")

        timeline_offset += cut_duration

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def render_reel(reel):
    print(f"\n🎬 RENDERING REEL {reel['id']}: {reel['title']}")
    banner_path = WORKSPACE_DIR / f"banner_202_{reel['id']}.png"
    make_header_banner(reel["title"], reel["emoji1"], reel["emoji2"], banner_path)

    ass_path = WORKSPACE_DIR / f"subs_202_{reel['id']}.ass"
    generate_running_subtitles(reel["cuts"], ass_path)

    temp_cuts = []
    total_duration = 0.0

    for i, cut in enumerate(reel["cuts"]):
        cut_dur = cut["et"] - cut["st"]
        total_duration += cut_dur
        cut_out = WORKSPACE_DIR / f"temp_cut_{reel['id']}_{i}.mp4"

        if cut["broll"]:
            cmd = [
                FFMPEG, "-y",
                "-ss", "0", "-t", f"{cut_dur:.3f}",
                "-i", cut["broll"],
                "-ss", f"{cut['st']:.3f}", "-t", f"{cut_dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-filter_complex",
                f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},setsar=1,fps=60[v]",
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
                f"[0:v]{cut['crop']},scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},setsar=1,fps=60[v]",
                "-map", "[v]", "-map", "0:a:0",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
                "-c:a", "pcm_s16le",
                str(cut_out)
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        temp_cuts.append(cut_out)

    # Concat cuts
    concat_list = WORKSPACE_DIR / f"concat_{reel['id']}.txt"
    with open(concat_list, "w") as f:
        for c in temp_cuts:
            f.write(f"file '{c}'\n")

    cuts_joined = WORKSPACE_DIR / f"joined_{reel['id']}.mp4"
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", str(cuts_joined)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Final 4K Composite with Canvas, Video, Banner, Running Subtitles, and Ducked Audio
    final_output = EXPORT_DIR / reel["filename"]
    filter_complex = (
        f"color=c=black:s={CANVAS_WIDTH}x{CANVAS_HEIGHT}:d={total_duration:.3f}[bg];"
        f"[bg][0:v]overlay=0:{VIDEO_Y}[comp1];"
        f"[comp1][1:v]overlay=0:{BANNER_Y}[comp2];"
        f"[comp2]subtitles='{ass_path}'[outv];"
        f"[0:a]volume=1.3,highpass=f=80,equalizer=f=3000:t=q:w=1.5:g=3,compand=attacks=0.02:decays=0.1:points=-60/-60|-20/-10|0/-1[clean_voice];"
        f"[2:a]volume={reel['bgm_gain']}dB[bgm_vol];"
        f"[bgm_vol][clean_voice]sidechaincompress=threshold=0.06:ratio=6:attack=15:release=250[ducked_bgm];"
        f"[clean_voice][ducked_bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]"
    )

    comp_cmd = [
        FFMPEG, "-y",
        "-i", str(cuts_joined),
        "-i", str(banner_path),
        "-stream_loop", "-1", "-i", str(reel["bgm"]),
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-t", f"{total_duration:.3f}",
        str(final_output)
    ]
    subprocess.run(comp_cmd, check=True)
    print(f"✅ Exported: {final_output} ({final_output.stat().st_size / 1024 / 1024:.2f} MB)")

    # Extract QA screenshots
    frames_dir = EXPORT_DIR / "FRAMES"
    frames_dir.mkdir(parents=True, exist_ok=True)
    qa_hook = frames_dir / f"frame_qa_202_reel_{reel['id']}_hook.jpg"
    qa_broll = frames_dir / f"frame_qa_202_reel_{reel['id']}_broll.jpg"
    qa_sub = frames_dir / f"frame_qa_202_reel_{reel['id']}_speaking_sub.jpg"

    subprocess.run([FFMPEG, "-y", "-ss", "1.5", "-i", str(final_output), "-vframes", "1", "-update", "1", str(qa_hook)], stderr=subprocess.DEVNULL)
    subprocess.run([FFMPEG, "-y", "-ss", f"{total_duration * 0.45:.2f}", "-i", str(final_output), "-vframes", "1", "-update", "1", str(qa_broll)], stderr=subprocess.DEVNULL)
    subprocess.run([FFMPEG, "-y", "-ss", f"{total_duration * 0.85:.2f}", "-i", str(final_output), "-vframes", "1", "-update", "1", str(qa_sub)], stderr=subprocess.DEVNULL)

    # Clean temporary cut files
    for c in temp_cuts:
        if c.exists():
            c.unlink()
    if cuts_joined.exists():
        cuts_joined.unlink()
    if concat_list.exists():
        concat_list.unlink()

def main():
    print("=" * 70)
    print("🚀 RENDERING 8 AUTHENTIC 4K REELS FROM 202.MOV")
    print("=" * 70)
    for r in REELS:
        render_reel(r)
    print("\n🎉 ALL 8 REELS SUCCESSFULLY RENDERED IN NATIVE 4K!")

if __name__ == "__main__":
    main()
