#!/usr/bin/env python3
"""
Render 8 Native 4K Reels from 202.MOV (37-Minute LLB's Podcast)
Features:
- Native 4K vertical canvas (2160x3840)
- Single big bold English title banner in Orange (#EA8207) with emojis
- Multi-camera dynamic crop switching (Guest: x=150, Host: x=1500, Wide: x=840)
- Thematic 4K B-rolls (couple, business, clock, dating, room, breakup, crowd, family)
- Frame-accurate running Tamil subtitles (active word in Orange, others in White, 10px black stroke)
- Audio: Demucs v4 vocal isolation + broadcast EQ/compression + FFmpeg sidechain ducked BGM
"""

import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Environment setup
PYTHON_VENV = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor/.venv/bin/python3")
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

# Canvas 4K geometry
CANVAS_WIDTH = 2160
CANVAS_HEIGHT = 3840
VIDEO_WIDTH = 2160
VIDEO_HEIGHT = 1880
VIDEO_Y = 1116
BANNER_Y = 600
BANNER_HEIGHT = 280

# Multi-cam crops from 3840x2160 raw frame
CROP_GUEST = "crop=2160:1880:150:280"
CROP_HOST = "crop=2160:1880:1500:280"
CROP_WIDE = "crop=2160:1880:840:280"

# Soundtracks
BGM_GROOVE = MUSIC_DIR / "ikoliks_aj-podcast-podcast-intro-613753.mp3"
BGM_EMOTIONAL = MUSIC_DIR / "The Cycle.mp3"

EMOJIS_DIR = ASSETS_DIR / "emojis"

# 8 High-Retention Viral Reel Configurations
REELS_202 = [
    {
        "id": 1,
        "title": "WHY DO MODERN RELATIONSHIPS FAIL?",
        "emoji1": "broken_heart.png", "emoji2": "fire.png",
        "filename": "Reel_202_1_Modern_Dating_Trap.mp4",
        "bgm": BGM_GROOVE, "bgm_gain": -17.5,
        "cuts": [
            {"num": 1, "st": 210.0, "et": 216.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 2.80, "ஏன் இப்போ ரிலேஷன்ஷிப்ல"),
                (3.00, 5.80, "இவ்வளவு ஈகோ வருது?")
            ]},
            {"num": 2, "st": 216.0, "et": 226.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.80, "இன்னைக்கு யாரும் விட்டுக்கொடுக்க"),
                (5.00, 9.70, "தயாரா இல்லை... நான் தான் பெருசு!")
            ]},
            {"num": 3, "st": 226.0, "et": 233.0, "crop": None, "broll": str(BROLLS_DIR / "broll_couple.mp4"), "phrases": [
                (0.30, 3.40, "ரெண்டு பேரும் பிடிவாதம் புடிச்சா"),
                (3.60, 6.70, "காதல் அங்கே காணாம போயிடும்!")
            ]},
            {"num": 4, "st": 233.0, "et": 245.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 5.50, "அன்பு இருந்தா ஈகோவே இருக்காது..."),
                (5.80, 11.50, "ஈகோ இருந்தா அங்கே காதலே இல்லை!")
            ]}
        ]
    },
    {
        "id": 2,
        "title": "MONEY DISPUTES DESTROY FAMILIES!",
        "emoji1": "warning.png", "emoji2": "fire.png",
        "filename": "Reel_202_2_Money_Vs_Marriage.mp4",
        "bgm": BGM_GROOVE, "bgm_gain": -17.5,
        "cuts": [
            {"num": 1, "st": 460.0, "et": 467.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.20, "பணம்னு வரும்போது குடும்பத்துல"),
                (3.40, 6.70, "வழக்கு மன்றம் வரைக்கும் போறாங்க!")
            ]},
            {"num": 2, "st": 467.0, "et": 476.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.50, "என் வீட்ல பணம்... உன் வீட்ல பணம்னு"),
                (4.70, 8.70, "கணக்கு பார்க்க ஆரம்பிச்சா பிரிவுதான்!")
            ]},
            {"num": 3, "st": 476.0, "et": 483.0, "crop": None, "broll": str(BROLLS_DIR / "broll_business.mp4"), "phrases": [
                (0.30, 3.20, "பணம் சம்பாதிக்கலாம்..."),
                (3.50, 6.70, "ஆனா உடைந்த உறவை சம்பாதிக்க முடியாது!")
            ]},
            {"num": 4, "st": 483.0, "et": 495.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 5.50, "பணத்துக்காக உறவை பலி கொடுக்காதீங்க..."),
                (5.80, 11.50, "மனிதர்கள் தான் உண்மையான சொத்து!")
            ]}
        ]
    },
    {
        "id": 3,
        "title": "WHAT IS YOUR REAL PURPOSE IN LIFE?",
        "emoji1": "target.png", "emoji2": "fire.png",
        "filename": "Reel_202_3_Life_Purpose_Under_30.mp4",
        "bgm": BGM_EMOTIONAL, "bgm_gain": -9.0,
        "cuts": [
            {"num": 1, "st": 700.0, "et": 708.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.50, "உங்க வாழ்க்கையோட உண்மையான"),
                (3.80, 7.50, "நோக்கம் என்னன்னு தெரியுமா?")
            ]},
            {"num": 2, "st": 708.0, "et": 718.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.80, "நிறைய பேர் மத்தவங்க மெச்சணும்னு"),
                (5.00, 9.60, "வாழ்க்கையை வீணடிச்சிட்டு இருக்காங்க!")
            ]},
            {"num": 3, "st": 718.0, "et": 725.0, "crop": None, "broll": str(BROLLS_DIR / "broll_clock.mp4"), "phrases": [
                (0.30, 3.20, "காலம் ஓடிக்கிட்டே இருக்கு..."),
                (3.50, 6.70, "உன் கனவுக்காக நீ என்ன பண்ண?")
            ]},
            {"num": 4, "st": 725.0, "et": 735.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.50, "பயத்தை தூக்கி எறிஞ்சிடு..."),
                (4.80, 9.60, "உன் இலக்கை நோக்கி ஓடு!")
            ]}
        ]
    },
    {
        "id": 4,
        "title": "FIRST LOVE VS REAL MATURITY!",
        "emoji1": "broken_heart.png", "emoji2": "thinking.png",
        "filename": "Reel_202_4_First_Love_Vs_Maturity.mp4",
        "bgm": BGM_EMOTIONAL, "bgm_gain": -9.0,
        "cuts": [
            {"num": 1, "st": 1080.0, "et": 1087.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.20, "ஃபர்ஸ்ட் லவ் தான் எப்பவும்"),
                (3.50, 6.60, "மறக்க முடியாத காதலா?")
            ]},
            {"num": 2, "st": 1087.0, "et": 1097.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.80, "அது வெறும் ஈர்ப்பு... மெச்சூரிட்டி"),
                (5.10, 9.60, "வந்த பிறகுதான் உண்மை காதல் தெரியும்!")
            ]},
            {"num": 3, "st": 1097.0, "et": 1104.0, "crop": None, "broll": str(BROLLS_DIR / "broll_phone_dating.mp4"), "phrases": [
                (0.30, 3.20, "பழைய நினைவுகளைப் பிடிச்சிட்டு"),
                (3.50, 6.70, "வாழ்க்கையை தொலைச்சிடாதீங்க!")
            ]},
            {"num": 4, "st": 1104.0, "et": 1115.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 5.20, "உங்களை புரிஞ்சுக்கிட்ட ஒருத்தர் கூட"),
                (5.50, 10.60, "வாழ்றதுதான் உண்மையான காதல்!")
            ]}
        ]
    },
    {
        "id": 5,
        "title": "NEVER BREAK A PROMISE IN LOVE!",
        "emoji1": "red_heart.png", "emoji2": "target.png",
        "filename": "Reel_202_5_Never_Break_Promise.mp4",
        "bgm": BGM_EMOTIONAL, "bgm_gain": -9.0,
        "cuts": [
            {"num": 1, "st": 1320.0, "et": 1328.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 3.80, "ஒருத்தருக்கு கொடுத்த வாக்கை"),
                (4.10, 7.60, "எக்காரணத்துக்காகவும் மீறக்கூடாது!")
            ]},
            {"num": 2, "st": 1328.0, "et": 1337.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.25, 4.20, "நம்பிக்கையை உடைக்கிறது"),
                (4.50, 8.60, "ஒரு உயிரை கொல்றதுக்கு சமம்!")
            ]},
            {"num": 3, "st": 1337.0, "et": 1344.0, "crop": None, "broll": str(BROLLS_DIR / "broll_empty_room.mp4"), "phrases": [
                (0.30, 3.20, "உடைந்த நம்பிக்கை"),
                (3.50, 6.70, "மீண்டும் ஒட்டவே ஒட்டாது!")
            ]},
            {"num": 4, "st": 1344.0, "et": 1355.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 5.20, "உண்மையான காதல்ல வார்த்தை முக்கியம்..."),
                (5.50, 10.60, "கொடுத்த வாக்கை காப்பாத்துறவன் தான் ஆண்மகன்!")
            ]}
        ]
    },
    {
        "id": 6,
        "title": "WHO IS THE REAL VILLAIN IN A BREAKUP?",
        "emoji1": "warning.png", "emoji2": "broken_heart.png",
        "filename": "Reel_202_6_Who_Is_The_Villain.mp4",
        "bgm": BGM_GROOVE, "bgm_gain": -17.5,
        "cuts": [
            {"num": 1, "st": 1560.0, "et": 1568.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.50, "பிரேக்அப் ஆனா எப்பவுமே"),
                (3.80, 7.60, "எக்ஸ் தான் வில்லனா?")
            ]},
            {"num": 2, "st": 1568.0, "et": 1578.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.50, "எல்லாரும் அவங்க பக்க நியாயத்தை"),
                (4.80, 9.60, "மட்டும் தான் உலகத்துக்கு சொல்லுவாங்க!")
            ]},
            {"num": 3, "st": 1578.0, "et": 1585.0, "crop": None, "broll": str(BROLLS_DIR / "broll_breakup.mp4"), "phrases": [
                (0.30, 3.20, "தப்பு ரெண்டு பக்கமும் இருக்கும்..."),
                (3.50, 6.70, "ஆனா ஒருத்தர் மட்டும் பழிசுமப்பார்!")
            ]},
            {"num": 4, "st": 1585.0, "et": 1595.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "உண்மையை ஒத்துக்க தைரியம் வேணும்..."),
                (5.10, 9.60, "மத்தவங்களை வில்லனாக்குறது சுலபம்!")
            ]}
        ]
    },
    {
        "id": 7,
        "title": "A LIFE WITHOUT PURPOSE IS PAIN!",
        "emoji1": "fire.png", "emoji2": "warning.png",
        "filename": "Reel_202_7_Life_Without_Purpose.mp4",
        "bgm": BGM_EMOTIONAL, "bgm_gain": -9.0,
        "cuts": [
            {"num": 1, "st": 1800.0, "et": 1808.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 3.50, "ஒரு பர்பஸ் இல்லாத வாழ்க்கை"),
                (3.80, 7.60, "மிகப்பெரிய நரகமா மாறிடும்!")
            ]},
            {"num": 2, "st": 1808.0, "et": 1818.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.25, 4.50, "இலக்கு இல்லாத போது சின்ன பிரச்சனை கூட"),
                (4.80, 9.60, "நம்மளை உடைச்சி தூக்கி எறிஞ்சிடும்!")
            ]},
            {"num": 3, "st": 1818.0, "et": 1825.0, "crop": None, "broll": str(BROLLS_DIR / "broll_crowd_promenade.mp4"), "phrases": [
                (0.30, 3.20, "கூட்டத்துல ஒருத்தனா நிக்காதே..."),
                (3.50, 6.70, "உன் பாதையை நீயே உருவாக்கு!")
            ]},
            {"num": 4, "st": 1825.0, "et": 1835.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "நோக்கத்தோடு வாழ ஆரம்பி..."),
                (5.10, 9.60, "வலி கூட உனக்கு வலிமையா மாறும்!")
            ]}
        ]
    },
    {
        "id": 8,
        "title": "WHY ARE YOUTH AFRAID OF MARRIAGE?",
        "emoji1": "red_heart.png", "emoji2": "warning.png",
        "filename": "Reel_202_8_Fear_Of_Marriage.mp4",
        "bgm": BGM_EMOTIONAL, "bgm_gain": -9.0,
        "cuts": [
            {"num": 1, "st": 2040.0, "et": 2048.0, "crop": CROP_HOST, "broll": None, "phrases": [
                (0.20, 3.50, "இன்னைக்கு இளைஞர்கள் கல்யாணத்தை"),
                (3.80, 7.60, "பார்த்து ஏன் இவ்வளவு பயப்படுறாங்க?")
            ]},
            {"num": 2, "st": 2048.0, "et": 2058.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.25, 4.80, "சுத்தி பார்க்குற விவாகரத்துகள்..."),
                (5.10, 9.60, "நம்பிக்கையின்மை தான் பயத்துக்கு காரணம்!")
            ]},
            {"num": 3, "st": 2058.0, "et": 2065.0, "crop": None, "broll": str(BROLLS_DIR / "broll_family.mp4"), "phrases": [
                (0.30, 3.20, "கல்யாணம்னா வெறும் பந்தம் இல்ல..."),
                (3.50, 6.70, "ரெண்டு மனசுகளின் பொறுப்பு!")
            ]},
            {"num": 4, "st": 2065.0, "et": 2075.0, "crop": CROP_GUEST, "broll": None, "phrases": [
                (0.20, 4.80, "சரியான புரிதல் இருந்தா..."),
                (5.10, 9.60, "குடும்ப வாழ்க்கை தான் மிகப்பெரிய சொர்க்கம்!")
            ]}
        ]
    }
]

def generate_4k_banner(title_text: str, emoji1: str, emoji2: str, output_path: Path):
    """Generates the signature Orange (#EA8207) 4K English header banner with image emojis."""
    img = Image.new("RGBA", (CANVAS_WIDTH, BANNER_HEIGHT), (234, 130, 7, 255))
    draw = ImageDraw.Draw(img)

    # 4px top/bottom solid black border
    draw.rectangle([(0, 0), (CANVAS_WIDTH, 3)], fill=(0, 0, 0, 255))
    draw.rectangle([(0, BANNER_HEIGHT - 4), (CANVAS_WIDTH, BANNER_HEIGHT - 1)], fill=(0, 0, 0, 255))

    # Prepare emojis (96x96)
    emoji_size = 96
    rendered_emojis = []
    for en in [emoji1, emoji2]:
        if en:
            ep = EMOJIS_DIR / en
            if ep.exists():
                em = Image.open(ep).convert("RGBA").resize((emoji_size, emoji_size), Image.Resampling.LANCZOS)
                rendered_emojis.append(em)

    emojis_w = len(rendered_emojis) * emoji_size + max(0, len(rendered_emojis) - 1) * 16
    max_w = CANVAS_WIDTH - 160  # 80px side margins

    font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    if not Path(font_path).exists():
        font_path = "/System/Library/Fonts/Helvetica.ttc"

    chosen_size = 96
    full_text = f"{title_text.strip()} "
    while chosen_size > 40:
        font = ImageFont.truetype(font_path, chosen_size)
        bbox = draw.textbbox((0, 0), full_text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        total_w = tw + (emojis_w + 16 if rendered_emojis else 0)
        if total_w <= max_w:
            break
        chosen_size -= 2

    start_x = (CANVAS_WIDTH - total_w) // 2
    text_y = (BANNER_HEIGHT - th) // 2 - 6

    draw.text((start_x, text_y), full_text, fill=(0, 0, 0, 255), font=font)

    cur_x = start_x + tw + 8
    emoji_y = (BANNER_HEIGHT - emoji_size) // 2
    for em in rendered_emojis:
        img.paste(em, (cur_x, emoji_y), em)
        cur_x += emoji_size + 16

    img.save(str(output_path))
    return output_path

def generate_exact_running_ass(cuts_cfg, output_ass: Path):
    """Generates frame-accurate running ASS subtitles (Orange active word, White others)."""
    header = """[Script Info]
Title: Frame-Accurate Running Subtitles
ScriptType: v4.00+
PlayResX: 2160
PlayResY: 3840
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans Tamil,108,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,10,2,2,80,80,980,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    t_cursor = 0.0

    for cut in cuts_cfg:
        dur = cut["et"] - cut["st"]
        for sp_rel_start, sp_rel_end, sentence in cut["phrases"]:
            words = sentence.split()
            if not words:
                continue
            t_phrase_start = t_cursor + sp_rel_start
            t_phrase_end = t_cursor + sp_rel_end
            phrase_dur = max(0.4, t_phrase_end - t_phrase_start)

            total_chars = sum(len(w) for w in words)
            w_offset = 0.0

            for i, w in enumerate(words):
                w_fraction = len(w) / total_chars if total_chars > 0 else (1.0 / len(words))
                w_dur = phrase_dur * w_fraction
                t_w_start = t_phrase_start + w_offset
                t_w_end = t_w_start + w_dur
                w_offset += w_dur

                styled_parts = []
                for j, other_w in enumerate(words):
                    if j == i:
                        styled_parts.append(r"{\c&H000782EA&}" + other_w)
                    else:
                        styled_parts.append(r"{\c&H00FFFFFF&}" + other_w)

                ass_line = " ".join(styled_parts)
                start_str = f"{int(t_w_start//3600):d}:{int((t_w_start%3600)//60):02d}:{t_w_start%60:05.2f}"
                end_str = f"{int(t_w_end//3600):d}:{int((t_w_end%3600)//60):02d}:{t_w_end%60:05.2f}"
                events.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{ass_line}")

        t_cursor += dur

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    return output_ass

def enhance_and_master_audio(raw_speech_wav: Path, bgm_file: Path, bgm_gain: float, output_mastered_wav: Path, total_duration: float, temp_dir: Path):
    """Demucs v4 vocal isolation + vocal EQ/compression + ducked BGM + peak limiter."""
    print("     🤖 Isolating speech dialogue with Meta Demucs v4 (htdemucs)...")
    demucs_out_dir = temp_dir / "demucs"
    cmd_demucs = [
        str(PYTHON_VENV), "-m", "demucs",
        "--two-stems=vocals", "-n", "htdemucs",
        "-o", str(demucs_out_dir),
        str(raw_speech_wav)
    ]
    subprocess.run(cmd_demucs, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    stem_name = raw_speech_wav.stem
    isolated_vocals = demucs_out_dir / "htdemucs" / stem_name / "vocals.wav"
    if not isolated_vocals.exists():
        isolated_vocals = raw_speech_wav

    print("     🎛️  Applying vocal enhancement (highpass, boxiness EQ, clarity boost, compressor)...")
    enhanced_vocals = temp_dir / "enhanced_vocals.wav"
    vocal_filter = (
        "highpass=f=85,lowpass=f=13500,"
        "equalizer=f=260:width_type=q:width=1.8:g=-2.5,"
        "equalizer=f=3400:width_type=q:width=1.2:g=3.2,"
        "deesser=i=0.4:m=0.5:f=0.6:s=o,"
        "acompressor=threshold=-18dB:ratio=3.2:attack=12:release=110"
    )
    cmd_eq = [
        FFMPEG, "-y",
        "-i", str(isolated_vocals),
        "-af", vocal_filter,
        str(enhanced_vocals)
    ]
    subprocess.run(cmd_eq, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("     🎵 Mixing ducked BGM with sidechain compression & EQ carving...")
    fade_out_st = max(0.0, total_duration - 1.5)
    fc = (
        f"[0:a]asplit=2[voice][key];"
        f"[1:a]volume={bgm_gain:.1f}dB,"
        f"equalizer=f=2400:t=q:w=1.6:g=-4.5,"
        f"equalizer=f=400:t=q:w=1.2:g=-2.0,"
        f"afade=t=in:st=0:d=0.5,"
        f"afade=t=out:st={fade_out_st:.2f}:d=1.5[bed];"
        f"[bed][key]sidechaincompress=threshold=0.035:ratio=6.0:attack=8:release=320:makeup=1:level_sc=1[duck];"
        f"[voice][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
        f"alimiter=limit=0.95:level=disabled,aresample=48000[aout]"
    )
    cmd_master = [
        FFMPEG, "-y",
        "-i", str(enhanced_vocals),
        "-stream_loop", "-1", "-i", str(bgm_file),
        "-filter_complex", fc,
        "-map", "[aout]",
        "-c:a", "pcm_s16le",
        "-t", f"{total_duration:.2f}",
        str(output_mastered_wav)
    ]
    subprocess.run(cmd_master, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_mastered_wav

def render_single_202_reel(reel_cfg):
    reel_id = reel_cfg["id"]
    output_mp4 = EXPORT_DIR / reel_cfg["filename"]
    print(f"\n==================================================")
    print(f"🎬 RENDERING 4K REEL {reel_id}/8: {reel_cfg['title']}")
    print(f"==================================================")
    print(f"Target: {output_mp4.name}")

    temp_dir = Path(tempfile.mkdtemp(prefix=f"reel202_{reel_id}_"))
    try:
        # 1. Generate 4K English Title Banner
        print("  📌 [1/6] Generating 4K English Title Banner...")
        banner_png = temp_dir / "banner.png"
        generate_4k_banner(reel_cfg["title"], reel_cfg["emoji1"], reel_cfg["emoji2"], banner_png)

        # 2. Extract 4K camera cuts & B-rolls
        print("  ✂️  [2/6] Extracting 4K multi-cam cuts & thematic B-rolls...")
        chunk_files = []
        total_duration = 0.0
        broll_time = None

        for idx, cut in enumerate(reel_cfg["cuts"]):
            dur = cut["et"] - cut["st"]
            chunk_file = temp_dir / f"chunk_{idx:02d}.mp4"
            dur_str = f"{dur:.2f}"

            if cut["broll"] and Path(cut["broll"]).exists():
                print(f"     [Cut {cut['num']}] Thematic B-Roll: {Path(cut['broll']).name} ({dur:.1f}s)")
                vf = (
                    f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
                    f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
                    f"format=yuv420p,fps=30"
                )
                cmd_cut = [
                    FFMPEG, "-y",
                    "-ss", f"{cut['st']:.2f}", "-t", dur_str, "-i", str(RAW_VIDEO),
                    "-stream_loop", "-1", "-t", dur_str, "-i", str(cut["broll"]),
                    "-filter_complex", f"[1:v]{vf}[vout]",
                    "-map", "[vout]", "-map", "0:a",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
                    "-c:a", "pcm_s16le",
                    str(chunk_file)
                ]
                if broll_time is None:
                    broll_time = total_duration + (dur / 2.0)
            else:
                crop_filter = cut["crop"]
                print(f"     [Cut {cut['num']}] Raw Camera Cut ({dur:.1f}s) -> {crop_filter.split(':')[0]}")
                vf = f"{crop_filter},format=yuv420p,fps=30"
                cmd_cut = [
                    FFMPEG, "-y",
                    "-ss", f"{cut['st']:.2f}", "-t", dur_str, "-i", str(RAW_VIDEO),
                    "-vf", vf,
                    "-map", "0:v:0", "-map", "0:a:0",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
                    "-c:a", "pcm_s16le",
                    str(chunk_file)
                ]

            subprocess.run(cmd_cut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            chunk_files.append(chunk_file)
            total_duration += dur

        print(f"  ⏱️  Total Duration: {total_duration:.2f}s")

        # Concat chunks
        concat_list = temp_dir / "concat.txt"
        with open(concat_list, "w") as f:
            for cf in chunk_files:
                f.write(f"file '{cf.resolve()}'\n")

        raw_concat_video = temp_dir / "raw_concat.mp4"
        cmd_concat = [
            FFMPEG, "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c", "copy",
            str(raw_concat_video)
        ]
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 3. Running ASS Subtitles
        print("  ✍️  [3/6] Generating Frame-Accurate Running ASS Subtitles...")
        sub_ass = temp_dir / "subtitles.ass"
        generate_exact_running_ass(reel_cfg["cuts"], sub_ass)

        # 4. Audio Enhancement & BGM Mixing
        print("  🎵 [4/6] Enhancing Audio (Demucs Vocal Isolation + EQ + Ducked BGM)...")
        raw_audio = temp_dir / "raw_audio.wav"
        cmd_ext_a = [
            FFMPEG, "-y",
            "-i", str(raw_concat_video),
            "-vn", "-ac", "2", "-ar", "44100",
            str(raw_audio)
        ]
        subprocess.run(cmd_ext_a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        mastered_audio = temp_dir / "mastered_audio.wav"
        enhance_and_master_audio(
            raw_speech_wav=raw_audio,
            bgm_file=reel_cfg["bgm"],
            bgm_gain=reel_cfg["bgm_gain"],
            output_mastered_wav=mastered_audio,
            total_duration=total_duration,
            temp_dir=temp_dir
        )

        # 5. Composite Final 4K Reel
        print("  🖥️  [5/6] Compositing Native 4K Reel (2160x3840)...")
        fonts_dir_str = str(FONTS_DIR.resolve())
        dur_str = f"{total_duration:.2f}"

        fc_composite = (
            f"color=c=black:s={CANVAS_WIDTH}x{CANVAS_HEIGHT}:r=30:d={dur_str}[bg];"
            f"[bg][0:v]overlay=0:{VIDEO_Y}[base];"
            f"[base][2:v]overlay=0:{BANNER_Y}[frame];"
            f"[frame]ass=filename='subtitles.ass':fontsdir='{fonts_dir_str}'[vout]"
        )

        cmd_final = [
            FFMPEG, "-y",
            "-i", str(raw_concat_video),
            "-i", str(mastered_audio),
            "-loop", "1", "-framerate", "30", "-t", dur_str, "-i", str(banner_png),
            "-filter_complex", fc_composite,
            "-map", "[vout]", "-map", "1:a",
            "-t", dur_str,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "256k",
            str(output_mp4)
        ]
        subprocess.run(cmd_final, check=True, cwd=str(temp_dir))
        print(f"  ✅ 4K Reel Rendered: {output_mp4.name} ({output_mp4.stat().st_size / (1024*1024):.2f} MB)")

        # 6. Extract QA Frames
        print("  📸 [6/6] Extracting Verification QA Frames...")
        qa_targets = [
            ("hook", 1.0),
            ("speaking_sub", 3.0),
            ("climax", total_duration - 2.5)
        ]
        if broll_time is not None:
            qa_targets.append(("broll", broll_time))

        for qa_name, t_snap in qa_targets:
            frames_dir = EXPORT_DIR / "FRAMES"
            frames_dir.mkdir(parents=True, exist_ok=True)
            qa_img = frames_dir / f"frame_qa_202_reel_{reel_id}_{qa_name}.jpg"
            cmd_snap = [
                FFMPEG, "-y",
                "-ss", f"{t_snap:.2f}",
                "-i", str(output_mp4),
                "-vframes", "1",
                "-q:v", "2",
                str(qa_img)
            ]
            subprocess.run(cmd_snap, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"     📸 QA Frame [{qa_name} at {t_snap:.1f}s]: {qa_img.name}")

        return True

    finally:
        # Cleanup temp directory
        try:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

def main():
    print("=" * 65)
    print("🚀 BATCH 4K RENDER: 8 VIRAL REELS FROM 202.MOV")
    print(f"Raw Footage: {RAW_VIDEO} (37 Mins, 4K 60fps)")
    print(f"Canvas:      {CANVAS_WIDTH}x{CANVAS_HEIGHT} (Native 4K Vertical 9:16)")
    print(f"Destination: {EXPORT_DIR}")
    print("=" * 65)

    success = 0
    for reel in REELS_202:
        if render_single_202_reel(reel):
            success += 1

    print("\n" + "=" * 65)
    print(f"🎉 4K BATCH RENDERING COMPLETE: {success}/8 Reels Rendered Successfully!")
    print("=" * 65)

if __name__ == "__main__":
    main()
