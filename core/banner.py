import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from core.config import (
    BANNER_WIDTH, BANNER_HEIGHT, BANNER_BG_COLOR,
    BANNER_BORDER_COLOR, BANNER_TEXT_COLOR,
    FONTS_DIR, EMOJIS_DIR
)

def create_header_banner(
    line1_text: str = "1 Lakh Job Challenge",
    line2_text: str = "499 Days-ல 1 Lakh Jobs!",
    emoji1_name: str = "fire.png",
    emoji2_name: str = "target.png",
    output_path: str = "header_banner.png"
) -> str:
    """
    Generates a 1080x150 persistent header banner with 2-line title and Twemojis
    matching the signature reference reel style.
    """
    banner = Image.new("RGBA", (BANNER_WIDTH, BANNER_HEIGHT), BANNER_BG_COLOR)
    draw = ImageDraw.Draw(banner)

    # 2px solid black border lines top and bottom
    draw.line([(0, 0), (BANNER_WIDTH, 0)], fill=BANNER_BORDER_COLOR, width=2)
    draw.line([(0, BANNER_HEIGHT - 1), (BANNER_WIDTH, BANNER_HEIGHT - 1)], fill=BANNER_BORDER_COLOR, width=2)

    # Load Fonts
    tamil_font_path = FONTS_DIR / "NotoSansTamil-Bold.ttf"
    if not tamil_font_path.exists():
        tamil_font_path = FONTS_DIR / "MuktaMalar-Bold.ttf"

    font_path_str = str(tamil_font_path) if tamil_font_path.exists() else None

    try:
        font_l1 = ImageFont.truetype(font_path_str or "arialbd.ttf", 48)
        font_l2 = ImageFont.truetype(font_path_str or "arialbd.ttf", 42)
    except Exception:
        font_l1 = ImageFont.load_default()
        font_l2 = ImageFont.load_default()

    # --- Line 1 ---
    text1 = f"{line1_text.strip()} "
    bbox1 = draw.textbbox((0, 0), text1, font=font_l1)
    w1 = bbox1[2] - bbox1[0]
    h1 = bbox1[3] - bbox1[1]

    emoji1_file = EMOJIS_DIR / emoji1_name
    has_emoji1 = emoji1_file.exists()
    emoji1_size = 44

    total_w1 = w1 + (emoji1_size + 8 if has_emoji1 else 0)
    start_x1 = (BANNER_WIDTH - total_w1) // 2
    y1 = 18

    draw.text((start_x1, y1), text1, fill=BANNER_TEXT_COLOR, font=font_l1)
    if has_emoji1:
        im_e1 = Image.open(emoji1_file).convert("RGBA").resize((emoji1_size, emoji1_size), Image.Resampling.LANCZOS)
        banner.paste(im_e1, (start_x1 + w1 + 8, y1 + (h1 - emoji1_size) // 2 + 2), im_e1)

    # --- Line 2 ---
    text2 = f"{line2_text.strip()} "
    bbox2 = draw.textbbox((0, 0), text2, font=font_l2)
    w2 = bbox2[2] - bbox2[0]
    h2 = bbox2[3] - bbox2[1]

    emoji2_file = EMOJIS_DIR / emoji2_name
    has_emoji2 = emoji2_file.exists()
    emoji2_size = 42

    total_w2 = w2 + (emoji2_size + 8 if has_emoji2 else 0)
    start_x2 = (BANNER_WIDTH - total_w2) // 2
    y2 = 82

    draw.text((start_x2, y2), text2, fill=BANNER_TEXT_COLOR, font=font_l2)
    if has_emoji2:
        im_e2 = Image.open(emoji2_file).convert("RGBA").resize((emoji2_size, emoji2_size), Image.Resampling.LANCZOS)
        banner.paste(im_e2, (start_x2 + w2 + 8, y2 + (h2 - emoji2_size) // 2 + 2), im_e2)

    banner.save(output_path)
    return str(output_path)
