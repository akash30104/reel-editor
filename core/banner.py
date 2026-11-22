import os
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from core.config import (
    BANNER_WIDTH, BANNER_HEIGHT, BANNER_BG_COLOR,
    BANNER_BORDER_COLOR, BANNER_TEXT_COLOR,
    FONTS_DIR, EMOJIS_DIR
)

def create_header_banner(
    line1_text: str = "Relationship-ல PDA தவறா?",
    line2_text: Optional[str] = None,
    emoji1_name: str = "broken_heart.png",
    emoji2_name: Optional[str] = "fire.png",
    output_path: str = "header_banner.png",
    font_size: Optional[int] = None
) -> str:
    """
    Generates a persistent header banner:
    - Single-title mode (if line2_text is None/empty): Larger, bold font with dynamic auto-scaling so text NEVER clips.
    - Two-line mode (if line2_text is provided): 2-line title layout matching legacy reference.
    """
    is_single_line = not line2_text or not line2_text.strip()
    banner_h = 130 if is_single_line else BANNER_HEIGHT

    banner = Image.new("RGBA", (BANNER_WIDTH, banner_h), BANNER_BG_COLOR)
    draw = ImageDraw.Draw(banner)

    # 2px solid black border lines top and bottom
    draw.line([(0, 0), (BANNER_WIDTH, 0)], fill=BANNER_BORDER_COLOR, width=2)
    draw.line([(0, banner_h - 1), (BANNER_WIDTH, banner_h - 1)], fill=BANNER_BORDER_COLOR, width=2)

    # Load Fonts
    tamil_font_path = FONTS_DIR / "NotoSansTamil-Bold.ttf"
    if not tamil_font_path.exists():
        tamil_font_path = FONTS_DIR / "MuktaMalar-Bold.ttf"

    font_path_str = str(tamil_font_path) if tamil_font_path.exists() else None

    if is_single_line:
        # === SINGLE BIG TITLE MODE WITH AUTO-FIT ===
        text = f"{line1_text.strip()} "
        
        emoji_size = 48
        emojis_to_render = []
        if emoji1_name:
            e1_file = EMOJIS_DIR / emoji1_name
            if e1_file.exists():
                emojis_to_render.append(Image.open(e1_file).convert("RGBA").resize((emoji_size, emoji_size), Image.Resampling.LANCZOS))
        if emoji2_name:
            e2_file = EMOJIS_DIR / emoji2_name
            if e2_file.exists():
                emojis_to_render.append(Image.open(e2_file).convert("RGBA").resize((emoji_size, emoji_size), Image.Resampling.LANCZOS))

        emojis_total_w = len(emojis_to_render) * emoji_size + max(0, len(emojis_to_render) - 1) * 8
        
        # Max allowable total width: banner width minus at least 48px padding on each side (984px max)
        max_allowed_w = BANNER_WIDTH - 96

        chosen_size = font_size or 58
        while chosen_size > 30:
            try:
                font = ImageFont.truetype(font_path_str or "arialbd.ttf", chosen_size)
            except Exception:
                font = ImageFont.load_default()
                break
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            total_w = w + (emojis_total_w + 8 if emojis_to_render else 0)
            if total_w <= max_allowed_w:
                break
            chosen_size -= 2

        start_x = (BANNER_WIDTH - total_w) // 2
        y = (banner_h - h) // 2 - 2

        draw.text((start_x, y), text, fill=BANNER_TEXT_COLOR, font=font)

        curr_x = start_x + w + 4
        emoji_y = (banner_h - emoji_size) // 2
        for em in emojis_to_render:
            banner.paste(em, (curr_x, emoji_y), em)
            curr_x += emoji_size + 8

    else:
        # === TWO-LINE TITLE MODE ===
        try:
            font_l1 = ImageFont.truetype(font_path_str or "arialbd.ttf", font_size or 48)
            font_l2 = ImageFont.truetype(font_path_str or "arialbd.ttf", int((font_size or 48) * 0.88))
        except Exception:
            font_l1 = ImageFont.load_default()
            font_l2 = ImageFont.load_default()

        # Line 1
        text1 = f"{line1_text.strip()} "
        bbox1 = draw.textbbox((0, 0), text1, font=font_l1)
        w1 = bbox1[2] - bbox1[0]
        h1 = bbox1[3] - bbox1[1]

        emoji1_file = EMOJIS_DIR / emoji1_name if emoji1_name else None
        has_emoji1 = emoji1_file and emoji1_file.exists()
        emoji1_size = 44

        total_w1 = w1 + (emoji1_size + 8 if has_emoji1 else 0)
        start_x1 = (BANNER_WIDTH - total_w1) // 2
        y1 = 18

        draw.text((start_x1, y1), text1, fill=BANNER_TEXT_COLOR, font=font_l1)
        if has_emoji1:
            im_e1 = Image.open(emoji1_file).convert("RGBA").resize((emoji1_size, emoji1_size), Image.Resampling.LANCZOS)
            banner.paste(im_e1, (start_x1 + w1 + 8, y1 + (h1 - emoji1_size) // 2 + 2), im_e1)

        # Line 2
        text2 = f"{line2_text.strip()} "
        bbox2 = draw.textbbox((0, 0), text2, font=font_l2)
        w2 = bbox2[2] - bbox2[0]
        h2 = bbox2[3] - bbox2[1]

        emoji2_file = EMOJIS_DIR / emoji2_name if emoji2_name else None
        has_emoji2 = emoji2_file and emoji2_file.exists()
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
