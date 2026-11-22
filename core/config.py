import os
from pathlib import Path

# Base Paths (Independent of operating system and user directory)
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PACKAGE_ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
EMOJIS_DIR = ASSETS_DIR / "emojis"
AUDIO_DIR = ASSETS_DIR / "audio"
BROLLS_DIR = ASSETS_DIR / "brolls"
EXPORT_DIR = PACKAGE_ROOT / "EXPORT"
RAW_DIR = PACKAGE_ROOT / "RAW_VIDEOS"

# Canvas & Layout Constants
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920

# Active Video Window (Matches Style Reference DaVinci Crop)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 940
VIDEO_Y = 558

# Header Banner Constants
BANNER_WIDTH = 1080
BANNER_HEIGHT = 150
BANNER_Y = 408
BANNER_BG_COLOR = (234, 130, 7, 255)  # Signature #EA8207
BANNER_BORDER_COLOR = (0, 0, 0, 255)
BANNER_TEXT_COLOR = (0, 0, 0, 255)

# Subtitle Styling Constants (Zero-Yellow Strict Rule)
FONT_PRIMARY = "Noto Sans Tamil"
COLOR_DIALOGUE = "&H00FFFFFF"     # Pure White
COLOR_KEYWORD = "&H000782EA"      # ASS hex format for #EA8207 (BBGGRR)
COLOR_STROKE = "&H00000000"       # Pure Black
STROKE_WIDTH = 5
SUBTITLE_MARGIN_V = 490

# Audio Mastering Constants
TARGET_LUFS = -14.0
TRUE_PEAK = -1.5
LRA = 9.0
BGM_DUCK_DB = -20


# Preset Styles Dictionary
PRESET_STYLES = {
    "reference_11": {
        "name": "REFERENCE 11",
        "canvas_width": CANVAS_WIDTH,
        "canvas_height": CANVAS_HEIGHT,
        "video_width": VIDEO_WIDTH,
        "video_height": VIDEO_HEIGHT,
        "video_y": VIDEO_Y,
        "banner_y": BANNER_Y,
        "banner_height": BANNER_HEIGHT,
        "banner_bg_hex": "#EA8207",
        "banner_bg_rgba": BANNER_BG_COLOR,
        "banner_border_width": 2,
        "banner_border_color": BANNER_BORDER_COLOR,
        "subtitle_dialogue": COLOR_DIALOGUE,
        "subtitle_keyword": COLOR_KEYWORD,
        "subtitle_stroke": COLOR_STROKE,
        "subtitle_stroke_width": STROKE_WIDTH,
        "subtitle_margin_v": SUBTITLE_MARGIN_V,
        "font_primary": FONT_PRIMARY,
        "zero_yellow": True,
        "no_progress_bar": True,
        "no_pill_badges": True,
        "internet_brolls_only": True,
        "target_lufs": TARGET_LUFS,
        "bgm_duck_db": BGM_DUCK_DB,
        "min_duration": 60.0,
        "max_duration": 90.0,
    }
}

# Alias mapping
PRESET_ALIASES = {
    "ref11": "reference_11",
    "reference11": "reference_11",
    "reference 11": "reference_11",
    "style 11": "reference_11",
    "11": "reference_11",
}

def get_style_config(style_name: str = "reference_11"):
    key = PRESET_ALIASES.get(style_name.lower().strip(), style_name.lower().strip())
    return PRESET_STYLES.get(key, PRESET_STYLES["reference_11"])
