#!/usr/bin/env python3
"""
Add Professional FFmpeg Background Music (BGM) to All 5 Native 4K Reels
Uses:
- FFmpeg sidechaincompress for dynamic audio ducking (music ducks when speech is active)
- EQ frequency pocket carving (carving 2.4kHz & 400Hz so voice stays 100% clear)
- Seamless looping & smooth head/tail fades
- Zero video re-encoding (-c:v copy) to preserve native 4K 2160x3840 quality
"""

import os
import sys
import subprocess
from pathlib import Path

FFMPEG = "/Users/pgi/.local/bin/ffmpeg"
FFPROBE = "/Users/pgi/.local/bin/ffprobe"
os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")

EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
MUSIC_DIR = Path("/Users/pgi/Downloads")

REELS_MUSIC_CONFIG = [
    {
        "id": 1,
        "title": "IS PDA IN PUBLIC WRONG? 💔🔥",
        "file": "Reel_1_PDA_Relationship.mp4",
        "music": MUSIC_DIR / "ikoliks_aj-podcast-podcast-intro-613753.mp3",
        "music_name": "Modern Podcast Groove (Beat & Rhythm)",
        "gain_db": -17.5,
        "sidechain_ratio": 6.0,
        "fade_in": 0.5,
        "fade_out": 1.5
    },
    {
        "id": 2,
        "title": "WOULD YOU ACCEPT YOUR MOM'S EX? 💔⚠️",
        "file": "Reel_2_Breakup_RedFlags.mp4",
        "music": MUSIC_DIR / "The Cycle.mp3",
        "music_name": "The Cycle (Govind Vasantha - Meiyazhagan Emotional Score)",
        "gain_db": -9.0,
        "sidechain_ratio": 6.0,
        "fade_in": 0.5,
        "fade_out": 1.5
    },
    {
        "id": 3,
        "title": "A HOUSE WITHOUT A WOMAN IS JUST A ROOM! 🏠❤️",
        "file": "Reel_3_True_Man_Role.mp4",
        "music": MUSIC_DIR / "The Cycle.mp3",
        "music_name": "The Cycle (Govind Vasantha - Meiyazhagan Emotional Score)",
        "gain_db": -9.0,
        "sidechain_ratio": 6.0,
        "fade_in": 0.5,
        "fade_out": 1.5
    },
    {
        "id": 4,
        "title": "CASIO WATCH: REPAIR, DON'T REPLACE! ⌚💎",
        "file": "Reel_4_Irreplaceable_Mindset.mp4",
        "music": MUSIC_DIR / "ikoliks_aj-podcast-podcast-intro-613753.mp3",
        "music_name": "Modern Podcast Groove (Beat & Rhythm)",
        "gain_db": -17.5,
        "sidechain_ratio": 6.0,
        "fade_in": 0.5,
        "fade_out": 1.5
    },
    {
        "id": 5,
        "title": "CAN A WIFE EVER REPLACE A MOTHER? 🥺❤️",
        "file": "Reel_5_Mother_Love.mp4",
        "music": MUSIC_DIR / "The Cycle.mp3",
        "music_name": "The Cycle (Govind Vasantha - Meiyazhagan Emotional Score)",
        "gain_db": -9.0,
        "sidechain_ratio": 6.0,
        "fade_in": 0.5,
        "fade_out": 1.5
    }
]

def get_duration(file_path: Path) -> float:
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def measure_audio(file_path: Path) -> str:
    cmd = [
        FFMPEG, "-i", str(file_path),
        "-af", "volumedetect",
        "-vn", "-f", "null", "-"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    mean_v = "N/A"
    max_v = "N/A"
    for line in res.stderr.splitlines():
        if "mean_volume:" in line:
            mean_v = line.split("mean_volume:")[1].strip()
        elif "max_volume:" in line:
            max_v = line.split("max_volume:")[1].strip()
    return f"Mean: {mean_v}, Peak: {max_v}"

def process_reel_music(cfg):
    input_video = EXPORT_DIR / cfg["file"]
    music_file = cfg["music"]
    temp_output = EXPORT_DIR / f"temp_{cfg['file']}"

    print(f"\n==================================================")
    print(f"🎵 ADDING MUSIC TO REEL {cfg['id']}/5: {cfg['title']}")
    print(f"   Target Video: {input_video.name}")
    print(f"   Soundtrack:   {cfg['music_name']}")
    print(f"==================================================")

    if not input_video.exists():
        print(f"❌ Error: Video file not found at {input_video}")
        return False
    if not music_file.exists():
        print(f"❌ Error: Music file not found at {music_file}")
        return False

    dur = get_duration(input_video)
    fade_out_st = max(0.0, dur - cfg["fade_out"])

    # Sidechain ducking + EQ pocket carving filtergraph
    # 1. Carve 2.4kHz & 400Hz from music so vocal frequencies remain uncontested
    # 2. Sidechain ducking compresses music when voice is active
    # 3. amix with normalize=0 keeps original voice level intact
    fc = (
        f"[0:a]asplit=2[voice][key];"
        f"[1:a]volume={cfg['gain_db']:.1f}dB,"
        f"equalizer=f=2400:t=q:w=1.6:g=-4.5,"
        f"equalizer=f=400:t=q:w=1.2:g=-2.0,"
        f"afade=t=in:st=0:d={cfg['fade_in']:.1f},"
        f"afade=t=out:st={fade_out_st:.2f}:d={cfg['fade_out']:.1f}[bed];"
        f"[bed][key]sidechaincompress=threshold=0.035:ratio={cfg['sidechain_ratio']}:"
        f"attack=8:release=320:makeup=1:level_sc=1[duck];"
        f"[voice][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
        f"alimiter=limit=0.95:level=disabled,aresample=48000[aout]"
    )

    cmd = [
        FFMPEG, "-y",
        "-i", str(input_video),
        "-stream_loop", "-1", "-i", str(music_file),
        "-filter_complex", fc,
        "-map", "0:v:0", "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k",
        "-t", f"{dur:.2f}",
        str(temp_output)
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Overwrite destination with the music-mixed version
    temp_output.replace(input_video)

    stats = measure_audio(input_video)
    print(f"   ✅ Music Mixed & Remuxed ({dur:.1f}s)")
    print(f"   📊 Final Master Audio: {stats}")
    print(f"   📁 Output: {input_video}")
    return True

def main():
    print("=" * 60)
    print("🚀 BATCH MUSIC ENGINE (FFmpeg Sidechain Ducking + EQ Carving)")
    print("=" * 60)
    success_count = 0
    for cfg in REELS_MUSIC_CONFIG:
        if process_reel_music(cfg):
            success_count += 1
    print("\n" + "=" * 60)
    print(f"🎉 COMPLETED: Music Added to {success_count}/5 Reels Successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
