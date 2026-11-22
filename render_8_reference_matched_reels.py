#!/usr/bin/env python3
"""
Master Production Engine: Render 8 Reference-Matched 4K Vertical Reels (2160x3840)
Directly fixes all user critique:
1. Header Title: Clean Title Case, Futura Bold / Arial Bold, 2 lines, centered, NO synthetic bloated outline loop!
2. Subtitles: Noto Sans Tamil Bold, 2-4 words per line, active word in Signature Orange (#EA8207), base in White (#FFFFFF), 8px black stroke, lower-third.
3. Music: vidssave.com Royalty Free Music (Epic/Inspiring/Cinematic) ducked to -24 dB with sidechain compression.
4. B-Rolls: 8 authentic, relevant, high-definition internet B-rolls matching the podcast discussion (Temple, Scripture, Forest, Boat, Fire, Mountains, Flames, Sunrise).
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Path configuration
os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
FFMPEG = "/Users/pgi/.local/bin/ffmpeg"
FFPROBE = "/Users/pgi/.local/bin/ffprobe"

WORKSPACE_DIR = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
ASSETS_DIR = WORKSPACE_DIR / "assets"
BROLLS_DIR = ASSETS_DIR / "brolls"
FONTS_DIR = WORKSPACE_DIR / "fonts"
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
FRAMES_DIR = EXPORT_DIR / "FRAMES"
BGM_PATH = Path("/Users/pgi/Downloads/vidssave.com Royalty Free Music - Epic Inspiring Dramatic Cinematic Emotional Background _ FREE DOWNLOAD 1080P.mp4")

# 4K Geometry (2160x3840 Canvas) - Exact 2x scale of Reference
CANVAS_WIDTH = 2160
CANVAS_HEIGHT = 3840
BANNER_Y = 832
BANNER_H = 284
VIDEO_Y = 1116
VIDEO_W = 2160
VIDEO_H = 1880

# Native 4K Crops from 3840x2160 Raw Video
CROP_GUEST = "crop=2160:1880:150:280,setsar=1,fps=30"
CROP_HOST = "crop=2160:1880:1500:280,setsar=1,fps=30"
CROP_WIDE = "crop=2160:1880:840:280,setsar=1,fps=30"

# 8 Curated High-Impact Reels
REELS = [
    {
        "id": 1,
        "title_l1": "Why Do People",
        "title_l2": "Mock Ramayanam?",
        "emoji": "🏹",
        "filename": "Reel_202_1_Why_Mock_Ramayana.mp4",
        "broll": str(BROLLS_DIR / "broll_temple.mp4"),
        "cuts": [
            {"st": 121.0, "et": 127.5, "crop": CROP_HOST, "broll": False, "phrases": [
                (0.15, 3.20, "ஒரு கதையோ விஷயமோ பேசினா..."),
                (3.40, 6.20, "ராமாயணம் மாதிரி இழுக்காதீங்கன்னு சொல்றாங்க!")
            ]},
            {"st": 127.5, "et": 136.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.10, "நாம ஏன் ராமாயணத்தை பத்தி பேசக் கூடாது?"),
                (4.30, 8.20, "அதை விட பெரிய வாழ்க்கை பாடம் எங்க இருக்கு?")
            ]},
            {"st": 136.0, "et": 143.0, "crop": None, "broll": True, "phrases": [
                (0.20, 3.40, "இன்னைக்கு இருக்கிற சினிமாக்கள் எல்லாமே"),
                (3.60, 6.80, "அந்த காப்பியங்களில் இருந்து வந்ததுதான்!")
            ]},
            {"st": 143.0, "et": 153.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.80, "அதை வெறும் கதையா பார்க்காதீங்க..."),
                (5.00, 9.80, "மனித மனங்களை புரிஞ்சுக்கிற மிகப்பெரிய பாடம்!")
            ]}
        ]
    },
    {
        "id": 2,
        "title_l1": "Kambar vs Valmiki:",
        "title_l2": "The Great Epic",
        "emoji": "📜",
        "filename": "Reel_202_2_Kambar_Vs_Valmiki.mp4",
        "broll": str(BROLLS_DIR / "broll_scripture.mp4"),
        "cuts": [
            {"st": 334.0, "et": 341.0, "crop": CROP_HOST, "broll": False, "phrases": [
                (0.20, 3.40, "வால்மீகி எழுதின மூல ராமாயணத்துக்கும்,"),
                (3.60, 6.80, "கம்பர் எழுதின காவியத்துக்கும் என்ன வித்தியாசம்?")
            ]},
            {"st": 341.0, "et": 350.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.20, "வால்மீகி கதையை சொன்னாருன்னா,"),
                (4.40, 8.80, "கம்பர் அதை தமிழ் உணர்வோட உயிர்ப்பிச்சாரு!")
            ]},
            {"st": 350.0, "et": 357.0, "crop": None, "broll": True, "phrases": [
                (0.25, 3.30, "தமிழ் மொழிக்கு கம்பர் கொடுத்த"),
                (3.50, 6.80, "கவிதை நயம் உலகத்துல வேற எங்கேயும் இல்லை!")
            ]},
            {"st": 357.0, "et": 367.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.80, "ஒவ்வொரு சொல்லிலும் அன்பையும் தர்மத்தையும்"),
                (5.00, 9.70, "அழகா வடித்த கவிச்சக்கரவர்த்தி கம்பர்!")
            ]}
        ]
    },
    {
        "id": 3,
        "title_l1": "The 14-Year Sacrifice",
        "title_l2": "Of Vanavasam",
        "emoji": "🌲",
        "filename": "Reel_202_3_Sacrifice_Of_Vanavasam.mp4",
        "broll": str(BROLLS_DIR / "broll_forest_mist.mp4"),
        "cuts": [
            {"st": 442.0, "et": 449.0, "crop": CROP_HOST, "broll": False, "phrases": [
                (0.20, 3.20, "அரியணை ஏற வேண்டிய நாள்ல..."),
                (3.40, 6.80, "வனவாசம் போகணும்னு சொன்னா எப்படி இருக்கும்?")
            ]},
            {"st": 449.0, "et": 458.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.25, 4.20, "எந்த ஒரு வருத்தமும் கோபமும் இல்லாம,"),
                (4.40, 8.80, "அப்பா சொன்ன வாக்கை காப்பாத்த காட்டுக்கு போனார்!")
            ]},
            {"st": 458.0, "et": 466.0, "crop": None, "broll": True, "phrases": [
                (0.25, 3.60, "பதவியும் பணமும் முக்கியம் இல்லை..."),
                (3.80, 7.80, "தர்மமும் கடமையும் தான் முக்கியம்னு காட்டுனாரு!")
            ]},
            {"st": 466.0, "et": 476.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.80, "வாழ்க்கை கஷ்டத்தை தரும்போது தப்பிச்சு ஓடாதீங்க..."),
                (5.00, 9.80, "அமைதியா ஏத்துக்கிட்டு நிமிர்ந்து நில்லுங்க!")
            ]}
        ]
    },
    {
        "id": 4,
        "title_l1": "Rama & Guhan:",
        "title_l2": "The 5th Brother",
        "emoji": "🛶",
        "filename": "Reel_202_4_Rama_And_Guhan_Brotherhood.mp4",
        "broll": str(BROLLS_DIR / "broll_river_boat.mp4"),
        "cuts": [
            {"st": 680.0, "et": 687.0, "crop": CROP_HOST, "broll": False, "phrases": [
                (0.20, 3.20, "வேடுவத் தலைவன் குகனை"),
                (3.40, 6.80, "ராமர் எப்படி தன் சகோதரனா ஏத்துக்கிட்டாரு?")
            ]},
            {"st": 687.0, "et": 697.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.25, 4.60, "சாதி, குலம், அந்தஸ்து எதையும் பார்க்காம..."),
                (4.80, 9.80, "உன்னோடு நாங்க ஐவர் ஆனோம்னு கட்டியணைச்சாரு!")
            ]},
            {"st": 697.0, "et": 705.0, "crop": None, "broll": True, "phrases": [
                (0.25, 3.60, "கங்கை நதிக்கரையில நடந்த இந்த சந்திப்பு,"),
                (3.80, 7.80, "மனிதகுலத்துக்கே சமத்துவத்தை கற்றுக்கொடுத்தது!")
            ]},
            {"st": 705.0, "et": 715.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.60, "உண்மையான நட்புக்கு அடையாளம் அந்தஸ்து இல்லை..."),
                (4.80, 9.80, "இதயத்தின் தூய்மை மட்டும்தான்!")
            ]}
        ]
    },
    {
        "id": 5,
        "title_l1": "Guhan's Tears:",
        "title_l2": "Pure Devotion",
        "emoji": "🌙",
        "filename": "Reel_202_5_Love_Without_Expectations.mp4",
        "broll": str(BROLLS_DIR / "broll_night_fire.mp4"),
        "cuts": [
            {"st": 920.0, "et": 927.0, "crop": CROP_HOST, "broll": False, "phrases": [
                (0.20, 3.20, "ராமர் படுத்து தூங்குறதை பார்த்து"),
                (3.40, 6.80, "குகன் ஏன் அவ்வளவு கண்ணீர் விட்டாரு?")
            ]},
            {"st": 927.0, "et": 937.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.25, 4.80, "அரண்மனையில தூங்க வேண்டியவர் புல் தரையில..."),
                (5.00, 9.80, "அந்த வேதனையை அவனால தாங்கவே முடியல!")
            ]},
            {"st": 937.0, "et": 945.0, "crop": None, "broll": True, "phrases": [
                (0.25, 3.60, "எந்த எதிர்பார்ப்பும் இல்லாம அன்பு செலுத்துறதுதான்,"),
                (3.80, 7.80, "இந்த உலகத்திலேயே மிக உயர்ந்த குணம்!")
            ]},
            {"st": 945.0, "et": 955.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.80, "உங்களை உண்மையா நேசிக்கிறவங்களை என்னைக்குமே,"),
                (5.00, 9.80, "அவங்க அன்பை குறைச்சு மதிப்பிடாதீங்க!")
            ]}
        ]
    },
    {
        "id": 6,
        "title_l1": "Sugriva & The Army:",
        "title_l2": "Searching For Sita",
        "emoji": "🏔️",
        "filename": "Reel_202_6_Sugriva_And_Vanara_Army.mp4",
        "broll": str(BROLLS_DIR / "broll_mountains.mp4"),
        "cuts": [
            {"st": 1050.0, "et": 1058.0, "crop": CROP_HOST, "broll": False, "phrases": [
                (0.20, 3.40, "ராமர் சீதையை தேடி போகும்போது..."),
                (3.60, 7.80, "அவருக்கு ஏன் ஒரு பெரும் படை தேவைப்பட்டுச்சு?")
            ]},
            {"st": 1058.0, "et": 1068.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.25, 4.80, "சீதையை கண்டுபிடிக்க சுக்கிரீவனோட வானர படை தான்"),
                (5.00, 9.80, "உலகமெங்கும் தேடி பல திசைகளிலும் அலைஞ்சது!")
            ]},
            {"st": 1068.0, "et": 1076.0, "crop": None, "broll": True, "phrases": [
                (0.25, 3.60, "நட்புக்கு கைமாறு செய்த ராமர்..."),
                (3.80, 7.80, "சீதையை மீட்க உதவிய வானர சேனை!")
            ]},
            {"st": 1076.0, "et": 1085.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.60, "கூடி வாழ்ந்தால் கோடி நன்மை..."),
                (4.80, 8.80, "ஒற்றுமை தான் எந்த போரிலும் மாபெரும் வெற்றி தரும்!")
            ]}
        ]
    },
    {
        "id": 7,
        "title_l1": "Ravana's Ego:",
        "title_l2": "Fall Of An Empire",
        "emoji": "🔥",
        "filename": "Reel_202_7_Ego_Destroys_Everything.mp4",
        "broll": str(BROLLS_DIR / "broll_raging_fire.mp4"),
        "cuts": [
            {"st": 1220.0, "et": 1227.0, "crop": CROP_HOST, "broll": False, "phrases": [
                (0.20, 3.20, "அவ்வளவு வலிமை இருந்தும் ராவணன் ஏன்"),
                (3.40, 6.80, "கடைசியில தன் சாம்ராஜ்யத்தையே இழந்தான்?")
            ]},
            {"st": 1227.0, "et": 1237.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.25, 4.80, "பத்து தலை அறிவு இருந்தாலும்... தலைக்கனம் இருந்தா,"),
                (5.00, 9.80, "அங்கே அழிவு நிச்சயம்னு நிரூபிச்சது அவனோட ஈகோ!")
            ]},
            {"st": 1237.0, "et": 1245.0, "crop": None, "broll": True, "phrases": [
                (0.25, 3.60, "ஈகோ ஒரு தீ மாதிரி... மத்தவங்களை எரிக்கிறதுக்கு முன்னாடி,"),
                (3.80, 7.80, "முதல்ல உங்களையே சாம்பலாக்கிடும்!")
            ]},
            {"st": 1245.0, "et": 1255.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.80, "எவ்வளவு உயரத்துக்கு போனாலும் அடக்கம் இல்லேன்னா,"),
                (5.00, 9.80, "கீழே விழும்போது தாங்க ஆள் இருக்காது!")
            ]}
        ]
    },
    {
        "id": 8,
        "title_l1": "Timeless Lessons:",
        "title_l2": "Calm In Any Storm",
        "emoji": "🌅",
        "filename": "Reel_202_8_Timeless_Lessons_Of_Life.mp4",
        "broll": str(BROLLS_DIR / "broll_golden_sunrise.mp4"),
        "cuts": [
            {"st": 1820.0, "et": 1827.0, "crop": CROP_HOST, "broll": False, "phrases": [
                (0.20, 3.20, "ராமாயணம் நமக்கு கத்துக்கொடுக்கிற"),
                (3.40, 6.80, "மிக முக்கியமான வாழ்க்கை பாடம் என்ன?")
            ]},
            {"st": 1827.0, "et": 1837.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.25, 4.80, "வெற்றி, தோல்வி, இன்பம், துன்பம் எல்லாத்தையும்"),
                (5.00, 9.80, "சமமா ஏத்துக்கிட்டு தர்மத்தோடு வாழ கத்துக்கணும்!")
            ]},
            {"st": 1837.0, "et": 1845.0, "crop": None, "broll": True, "phrases": [
                (0.25, 3.60, "எந்த சூழ்நிலையிலும் நற்குணத்தை விட்டுடாதீங்க..."),
                (3.80, 7.80, "அதுதான் உங்களை தலைமுறை கடந்து வாழ வைக்கும்!")
            ]},
            {"st": 1845.0, "et": 1855.0, "crop": CROP_GUEST, "broll": False, "phrases": [
                (0.20, 4.80, "இந்த உண்மையை புரிஞ்சுகிட்டா போதும்..."),
                (5.00, 9.80, "வாழ்க்கையில எந்த புயல் வந்தாலும் ஜெயிக்கலாம்!")
            ]}
        ]
    }
]

def make_4k_banner(line1, line2, emoji, out_path):
    img = Image.new("RGBA", (CANVAS_WIDTH, BANNER_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = 70
    draw.rounded_rectangle(
        [margin, 8, CANVAS_WIDTH - margin, BANNER_H - 8],
        radius=48,
        fill=(234, 130, 7, 255),
        outline=(0, 0, 0, 255),
        width=10
    )

    # Clean 4K Typography - Futura Bold (index 2) or Arial Bold
    font_path = "/System/Library/Fonts/Supplemental/Futura.ttc"
    try:
        font = ImageFont.truetype(font_path, 88, index=2)
    except Exception:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 84)

    text2 = f"{line2} {emoji}" if emoji else line2

    bbox1 = draw.textbbox((0, 0), line1, font=font)
    bbox2 = draw.textbbox((0, 0), text2, font=font)
    w1 = bbox1[2] - bbox1[0]
    w2 = bbox2[2] - bbox2[0]
    h1 = bbox1[3] - bbox1[1]
    h2 = bbox2[3] - bbox2[1]

    y1 = (BANNER_H - (h1 + h2 + 16)) // 2 - 8
    y2 = y1 + h1 + 20

    x1 = (CANVAS_WIDTH - w1) // 2
    x2 = (CANVAS_WIDTH - w2) // 2

    # Draw pure clean black text (Single crisp pass - NO artificial dilated stroke loop!)
    draw.text((x1, y1), line1, font=font, fill=(0, 0, 0, 255))
    draw.text((x2, y2), text2, font=font, fill=(0, 0, 0, 255))

    img.save(out_path, "PNG")

def sec_to_ass(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def make_4k_running_subs(cuts, ass_path):
    lines = []
    lines.append("[Script Info]")
    lines.append("Title: 4K Reference Matched Running Subtitles")
    lines.append("ScriptType: v4.00+")
    lines.append(f"PlayResX: {CANVAS_WIDTH}")
    lines.append(f"PlayResY: {CANVAS_HEIGHT}")
    lines.append("WrapStyle: 0\n")

    lines.append("[V4+ Styles]")
    lines.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    lines.append("Style: Running,Noto Sans Tamil,104,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,8,0,2,120,120,920,1\n")

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

def render_reel(reel):
    rid = reel["id"]
    print(f"\n=======================================================")
    print(f"🎬 RENDERING REEL {rid}: {reel['title_l1']} {reel['title_l2']}")
    print(f"=======================================================")

    banner_png = WORKSPACE_DIR / f"banner_final_{rid}.png"
    make_4k_banner(reel["title_l1"], reel["title_l2"], reel["emoji"], banner_png)

    ass_path = WORKSPACE_DIR / f"subs_final_{rid}.ass"
    make_4k_running_subs(reel["cuts"], ass_path)

    temp_cuts = []
    total_dur = 0.0

    for i, cut in enumerate(reel["cuts"]):
        cut_dur = cut["et"] - cut["st"]
        total_dur += cut_dur
        cut_out = WORKSPACE_DIR / f"cut_final_{rid}_{i}.mp4"

        if cut["broll"]:
            cmd = [
                FFMPEG, "-y",
                "-ss", "0", "-t", f"{cut_dur:.3f}",
                "-i", reel["broll"],
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
                f"[0:v]{cut['crop']}[v]",
                "-map", "[v]", "-map", "0:a:0",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
                "-c:a", "pcm_s16le",
                str(cut_out)
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        temp_cuts.append(cut_out)

    concat_list = WORKSPACE_DIR / f"concat_final_{rid}.txt"
    with open(concat_list, "w") as f:
        for c in temp_cuts:
            f.write(f"file '{c}'\n")

    cuts_joined = WORKSPACE_DIR / f"joined_final_{rid}.mp4"
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", str(cuts_joined)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Master Composite: 4K Letterbox Canvas + Banner + Video + Subtitles + Ducked Music
    final_output = EXPORT_DIR / reel["filename"]
    filter_complex = (
        f"color=c=black:s={CANVAS_WIDTH}x{CANVAS_HEIGHT}:d={total_dur:.3f}[bg];"
        f"[bg][0:v]overlay=0:{VIDEO_Y}[comp1];"
        f"[comp1][1:v]overlay=0:{BANNER_Y}[comp2];"
        f"[comp2]subtitles='{ass_path}':fontsdir='{FONTS_DIR}'[outv];"
        f"[0:a]volume=2.2,highpass=f=80,equalizer=f=3000:t=q:w=1.5:g=2.5,compand=attacks=0.02:decays=0.1:points=-60/-60|-20/-10|0/-1[clean_voice];"
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
        str(final_output)
    ]
    subprocess.run(comp_cmd, check=True)
    print(f"✅ RENDER COMPLETE: {final_output}")

    # Extract QA frame at 12s directly into FRAMES directory
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    qa_frame = FRAMES_DIR / f"frame_qa_final_{rid}.jpg"
    subprocess.run([
        FFMPEG, "-y", "-ss", "12", "-i", str(final_output),
        "-vframes", "1", str(qa_frame)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"📸 QA Frame saved: {qa_frame}")

def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    for r in REELS:
        render_reel(r)
    print("\n🎉 ALL 8 REFERENCE-MATCHED 4K REELS SUCCESSFULLY RENDERED!")

if __name__ == "__main__":
    main()
