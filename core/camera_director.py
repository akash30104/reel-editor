import subprocess
from pathlib import Path
from typing import Optional
from core.config import VIDEO_WIDTH, VIDEO_HEIGHT

def extract_cut_chunk(
    raw_video_path: str,
    start_time: float,
    end_time: float,
    output_chunk_path: str,
    speaker: int = 1,
    zoom: bool = False,
    is_hook_flash: bool = False,
    broll_path: Optional[str] = None
) -> str:
    """
    Extracts a cut from the raw footage or integrates a B-roll:
    - Speaker 1 (Left, e.g. Guest) vs Speaker 2 (Right, e.g. Host)
    - Dynamic Punch-in Zoom (1.15x)
    - Opening Hook B&W flash transition (0.6s)
    - B-Roll scaling and cropping to exact 1080x940 window
    """
    duration = end_time - start_time

    if broll_path and Path(broll_path).exists():
        # B-Roll path: scale and crop to 1080x940, take audio from raw video cut
        filter_broll = (
            f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},setsar=1,fps=30[vout]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", broll_path,
            "-ss", f"{start_time:.2f}", "-t", f"{duration:.2f}", "-i", raw_video_path,
            "-filter_complex", filter_broll,
            "-map", "[vout]", "-map", "1:a",
            "-t", f"{duration:.2f}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "pcm_s16le",
            output_chunk_path
        ]
    else:
        # Camera framing from 4K/1080p source
        if speaker == 2:
            # Speaker 2 (Host / Right)
            crop_rect = "1565:1362:2100:300" if zoom else "1800:1567:1950:250"
        else:
            # Speaker 1 (Guest / Left)
            crop_rect = "1565:1362:350:300" if zoom else "1800:1567:200:250"

        if is_hook_flash:
            # 0.6s black & white flash to high energy color hook
            filter_v = (
                f"crop={crop_rect},scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},setsar=1,fps=30,"
                f"split[v1][v2];"
                f"[v1]trim=0:0.6,hue=s=0,setpts=PTS-STARTPTS[vbw];"
                f"[v2]trim=0.6:{duration:.2f},setpts=PTS-STARTPTS[vcol];"
                f"[vbw][vcol]concat=n=2:v=1:a=0[vout]"
            )
        else:
            filter_v = f"crop={crop_rect},scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},setsar=1,fps=30[vout]"

        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{start_time:.2f}", "-t", f"{duration:.2f}", "-i", raw_video_path,
            "-filter_complex", filter_v,
            "-map", "[vout]", "-map", "0:a",
            "-t", f"{duration:.2f}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "pcm_s16le",
            output_chunk_path
        ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return str(output_chunk_path)
