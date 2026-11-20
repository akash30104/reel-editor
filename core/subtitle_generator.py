import os
from pathlib import Path
from typing import List, Tuple
from core.config import (
    COLOR_DIALOGUE, COLOR_KEYWORD, COLOR_STROKE,
    STROKE_WIDTH, SUBTITLE_MARGIN_V, FONT_PRIMARY
)

def format_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def create_ass_subtitles(
    segments: List[Tuple[float, float, str]],
    output_path: str = "subtitles.ass"
) -> str:
    """
    Builds an Advanced SubStation Alpha (.ass) subtitle file adhering strictly to:
    - Pure white dialogue (&H00FFFFFF)
    - Signature orange keyword highlights (&H000782EA)
    - 5px solid black outline (&H00000000)
    - ZERO yellow
    """
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{FONT_PRIMARY},54,{COLOR_DIALOGUE},&H000000FF,{COLOR_STROKE},&H80000000,-1,0,0,0,100,100,0,0,1,{STROKE_WIDTH},2,2,40,40,{SUBTITLE_MARGIN_V},1
Style: HookSubtitle,{FONT_PRIMARY},62,{COLOR_DIALOGUE},&H000000FF,{COLOR_STROKE},&H80000000,-1,0,0,0,100,100,0,0,1,{STROKE_WIDTH+1},3,2,40,40,{SUBTITLE_MARGIN_V+20},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header)
        for i, (start_t, end_t, text) in enumerate(segments):
            style = "HookSubtitle" if i == 0 else "Default"
            st_str = format_ass_time(start_t)
            et_str = format_ass_time(end_t)
            f.write(f"Dialogue: 0,{st_str},{et_str},{style},,0,0,0,,{text}\n")

    return str(output_path)
