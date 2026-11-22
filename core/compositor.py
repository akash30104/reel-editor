import os
import subprocess
from pathlib import Path
from typing import List, Tuple
from PIL import Image
from core.config import (
    CANVAS_WIDTH, CANVAS_HEIGHT,
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_Y,
    BANNER_WIDTH, BANNER_HEIGHT, BANNER_Y,
    FONTS_DIR
)

def composite_final_reel(
    concat_video_path: str,
    mastered_audio_path: str,
    banner_png_path: str,
    ass_subtitle_path: str,
    output_mp4_path: str,
    duration: float
) -> str:
    """
    Renders the final 9:16 vertical reel (1080x1920) with:
    - 1080x940 video window at y=558
    - Guaranteed persistent 2-line title banner at y=408 (never disappears)
    - Solid black letterbox (no progress line, no badges)
    - Burned ASS subtitles using bundled Tamil/English fonts
    - High-quality H.264 video and 192kbps AAC audio
    """
    dur_str = f"{duration:.2f}"
    fonts_dir_name = str(FONTS_DIR.resolve())
    concat_video_path = str(Path(concat_video_path).resolve())
    mastered_audio_path = str(Path(mastered_audio_path).resolve())
    banner_png_path = str(Path(banner_png_path).resolve())
    output_mp4_path = str(Path(output_mp4_path).resolve())

    # Dynamically position banner flush on top of the video window (VIDEO_Y = 558)
    try:
        with Image.open(banner_png_path) as bimg:
            actual_banner_h = bimg.size[1]
    except Exception:
        actual_banner_h = BANNER_HEIGHT
    actual_banner_y = VIDEO_Y - actual_banner_h

    filter_complex = (
        f"color=c=black:s={CANVAS_WIDTH}x{CANVAS_HEIGHT}:r=30:d={dur_str}[bg];"
        f"[bg][0:v]overlay=0:{VIDEO_Y}[base];"
        f"[base][2:v]overlay=0:{actual_banner_y}[frame];"
        f"[frame]ass=filename='{Path(ass_subtitle_path).name}':fontsdir='{fonts_dir_name}'[vout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", concat_video_path,
        "-i", mastered_audio_path,
        "-loop", "1", "-framerate", "30", "-t", dur_str, "-i", banner_png_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", "1:a",
        "-t", dur_str,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k",
        output_mp4_path
    ]

    # Execute in the subtitle file's parent directory so FFmpeg can find fonts and ass
    work_dir = Path(ass_subtitle_path).parent
    subprocess.run(cmd, check=True, cwd=str(work_dir))
    return str(output_mp4_path)

def extract_qa_frames(
    video_path: str,
    output_dir: str,
    timestamps: List[Tuple[str, float]]
) -> List[str]:
    """
    Extracts verification frames across the video duration for QA.
    """
    out_paths = []
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for label, t_sec in timestamps:
        out_jpg = str(Path(output_dir) / f"frame_qa_{label}.jpg")
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{t_sec:.2f}",
            "-i", video_path,
            "-vframes", "1", "-q:v", "2",
            out_jpg
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out_paths.append(out_jpg)
    return out_paths
