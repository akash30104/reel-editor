import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any

def extract_audio_wav(video_path: str, output_wav: str) -> str:
    """Extracts 16kHz mono WAV for Whisper."""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-ar", "16000", "-ac", "1",
        output_wav
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_wav

def transcribe_audio(audio_path: str, language: str = "ta") -> Dict[str, Any]:
    """
    Transcribes audio using OpenAI Whisper.
    Falls back gracefully if whisper is not installed or CPU only.
    """
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language=language, verbose=False)
        return result
    except ImportError:
        print("[WARNING] Whisper not installed. Install via: pip install openai-whisper")
        return {"text": "", "segments": []}
