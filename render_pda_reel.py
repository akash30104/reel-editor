#!/usr/bin/env python3
"""
Tamil Podcast Viral Reel Editor: PDA & Relationships
Renders topic-accurate viral 9:16 vertical reel based on Whisper Tamil transcription of IMG_7020.MOV.
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config import (
    ASSETS_DIR, FONTS_DIR, EMOJIS_DIR,
    AUDIO_DIR, EXPORT_DIR
)
from core.banner import create_header_banner
from core.subtitle_generator import create_ass_subtitles
from core.camera_director import extract_cut_chunk
from core.audio_master import master_audio
from core.compositor import composite_final_reel, extract_qa_frames

def main():
    raw_video = Path("/Users/pgi/Downloads/reels editor/raw videos/IMG_7020.MOV")
    export_dir = Path("/Users/pgi/Downloads/reels editor/export ")
    export_dir.mkdir(parents=True, exist_ok=True)
    
    final_output = export_dir / "IMG_7020_Viral_Reel.mp4"
    temp_dir = Path(tempfile.mkdtemp(prefix="reel_pda_"))

    print("==========================================")
    print("🎬 RENDERING ACCURATE TAMIL PODCAST REEL")
    print("==========================================")
    print(f"Input:   {raw_video}")
    print(f"Output:  {final_output}")
    print(f"Topic:   Relationship-ல PDA தவறா? 💔🔥")
    print("==========================================\n")

    try:
        # 1. Header Banner (Single Big Title)
        banner_png = temp_dir / "header_banner.png"
        print("📌 [1/5] Generating Single Big Title Header Banner...")
        create_header_banner(
            line1_text="Relationship-ல PDA தவறா?",
            line2_text=None,
            emoji1_name="broken_heart.png",
            emoji2_name="fire.png",
            output_path=str(banner_png),
            font_size=60
        )

        # 2. Editorial Timeline Cuts & Subtitles
        # Speaker 1 = Guest (Man / Left), Speaker 2 = Host (Woman / Right)
        cuts = [
            # 1. Opening Question: Guest asks about dating intent (Speaker 1, zoom, hook flash)
            (1,  70.50,  75.80, 1, True,  None, True,
             "நாம ஏன் ஃபர்ஸ்ட் வெளியே போறோம்? {\\c&H000782EA&}மனசு விட்டு பேசுறதுக்காகவா?{\\c&H00FFFFFF&}"),

            # 2. Host Agreement (Speaker 2)
            (2,  75.80,  77.00, 2, False, None, False,
             "ஆமாம், {\\c&H000782EA&}கண்டிப்பா!{\\c&H00FFFFFF&}"),

            # 3. Host calls out modern PDA trend in public spaces (Speaker 2, zoom)
            (3,  77.00,  83.50, 2, True,  None, False,
             "ஆனா இப்போ பார்க், பீச்-ல {\\c&H000782EA&}Public Display of Affection{\\c&H00FFFFFF&} தான் பண்றாங்க!"),

            # 4. Host asks the core debate question (Speaker 2)
            (4, 115.00, 122.00, 2, False, None, False,
             "இது {\\c&H000782EA&}Healthy Relationship-ஆ?{\\c&H00FFFFFF&} இல்ல Unhealthy-ஆ?"),

            # 5. Host continues questioning (Speaker 2, zoom)
            (5, 122.00, 126.50, 2, True,  None, False,
             "எல்லாரும் முன்னாடியும் {\\c&H000782EA&}PDA பண்றது சரியா?{\\c&H00FFFFFF&}"),

            # 6. Guest Core Philosophy on Intimacy & Value (Speaker 1)
            (6, 126.50, 136.00, 1, False, None, False,
             "Intimacy என்பது மத்தவங்க பாக்குற காட்சி பொருள் இல்ல! {\\c&H000782EA&}அது ரொம்ப High-Value விஷயம்!{\\c&H00FFFFFF&}"),

            # 7. Guest Hard-Hitting Climax / Punchline (Speaker 1, zoom)
            (7, 136.00, 142.50, 1, True,  None, False,
             "அதை ரோட்டுல பப்ளிக்கா பண்ணா, {\\c&H000782EA&}நீங்க எந்த அளவுக்கு தரம் கெட்டு போயிருக்கீங்கன்னு{\\c&H00FFFFFF&} தான் காட்டும்!"),
        ]

        print("✂️  [2/5] Rendering Individual Cuts with Framing Fix...")
        chunk_files = []
        timeline_subs = []
        current_time = 0.0

        for idx, start, end, speaker, zoom, broll, is_hook, sub_text in cuts:
            dur = end - start
            timeline_subs.append((current_time, current_time + dur, sub_text))
            chunk_file = str(temp_dir / f"chunk_{idx:02d}.mp4")
            extract_cut_chunk(
                raw_video_path=str(raw_video),
                start_time=start,
                end_time=end,
                output_chunk_path=chunk_file,
                speaker=speaker,
                zoom=zoom,
                is_hook_flash=is_hook,
                broll_path=broll
            )
            chunk_files.append(chunk_file)
            current_time += dur

        total_duration = current_time
        print(f"    Total Video Duration: {total_duration:.2f}s")

        # 3. Concatenate Cuts
        print("🔗 [3/5] Concatenating Video Chunks...")
        concat_txt = temp_dir / "concat_list.txt"
        with open(concat_txt, "w") as f:
            for ch in chunk_files:
                f.write(f"file '{ch}'\n")

        raw_concat_mp4 = str(temp_dir / "raw_concat.mp4")
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            raw_concat_mp4
        ]
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 4. Demucs Vocal Isolation & Audio Mastering (-14 LUFS)
        print("🎙️  [4/5] Audio Enhancement with Demucs & EBU R128 Mastering...")
        # Extract raw dialogue audio
        raw_speech_wav = str(temp_dir / "raw_speech.wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_concat_mp4,
            "-vn", "-ar", "44100", "-ac", "2", raw_speech_wav
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Separate clean vocals using demucs
        enhanced_speech_wav = raw_speech_wav
        try:
            print("    Running Demucs vocal enhancement...")
            demucs_bin = shutil.which("demucs") or str(PROJECT_ROOT / ".venv" / "bin" / "demucs")
            demucs_out_dir = temp_dir / "demucs_clean"
            subprocess.run([
                demucs_bin, "--two-stems=vocals", "-n", "htdemucs",
                "-o", str(demucs_out_dir), raw_speech_wav
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            demucs_vocals = demucs_out_dir / "htdemucs" / "raw_speech" / "vocals.wav"
            if demucs_vocals.exists():
                enhanced_speech_wav = str(demucs_vocals)
                print("    Demucs vocal enhancement applied successfully!")
        except Exception as e:
            print(f"    Demucs skipped (falling back to direct audio): {e}")

        # Master audio (-14 LUFS with ducked lo-fi BGM)
        mastered_audio_wav = str(temp_dir / "mastered_audio.wav")
        master_audio(enhanced_speech_wav, mastered_audio_wav, total_duration)

        # Subtitles (Zero-Yellow)
        ass_subtitles = str(temp_dir / "subtitles.ass")
        create_ass_subtitles(timeline_subs, ass_subtitles)

        # 5. Composite Final Reel
        print("🎨 [5/5] Compositing 9:16 Video Canvas with Burned Subtitles & Header...")
        composite_final_reel(
            concat_video_path=raw_concat_mp4,
            mastered_audio_path=mastered_audio_wav,
            banner_png_path=str(banner_png),
            ass_subtitle_path=ass_subtitles,
            output_mp4_path=str(final_output),
            duration=total_duration
        )

        # Extract QA verification frames
        qa_times = [
            ("1_hook_guest", 2.0),
            ("2_host_agree", 6.0),
            ("3_host_pda_beach", 10.0),
            ("4_host_question", 15.0),
            ("5_guest_intimacy", 26.0),
            ("6_guest_punchline", 38.0),
        ]
        qa_frames = extract_qa_frames(str(final_output), str(export_dir), qa_times)

        print("\n==========================================")
        print("🎉 REEL RENDERING COMPLETE!")
        print(f"Saved: {final_output}")
        print("QA Frames:")
        for qf in qa_frames:
            print(f"  - {qf}")
        print("==========================================\n")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
