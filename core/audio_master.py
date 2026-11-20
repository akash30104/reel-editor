import subprocess
from pathlib import Path
from core.config import AUDIO_DIR, TARGET_LUFS, TRUE_PEAK, LRA, BGM_DUCK_DB

def master_audio(
    speech_audio_path: str,
    output_wav_path: str,
    duration: float,
    bgm_path: str = None
) -> str:
    """
    Blends spoken dialogue with ducked background music (-20 dB with smooth fades)
    and applies broadcast EBU R128 loudness normalization (-14 LUFS).
    """
    if bgm_path is None:
        bgm_path = str(AUDIO_DIR / "bgm_bed.mp3")

    fade_out_start = max(0.0, duration - 1.5)
    filter_audio = (
        f"[1:a]volume={BGM_DUCK_DB}dB,afade=t=in:st=0:d=1,afade=t=out:st={fade_out_start:.2f}:d=1.5,atrim=0:{duration:.2f}[bgm];"
        f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,"
        f"loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK}:LRA={LRA}[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", speech_audio_path,
        "-stream_loop", "-1", "-i", bgm_path,
        "-filter_complex", filter_audio,
        "-map", "[aout]",
        "-c:a", "pcm_s16le",
        output_wav_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return str(output_wav_path)
