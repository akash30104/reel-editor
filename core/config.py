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
