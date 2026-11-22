#!/usr/bin/env python3
"""
Automated Reel Editor CLI
Edits raw podcast / interview video footage into viral 9:16 vertical reels with:
- Persistent Two-Line Orange (#EA8207) Topic Header with Twemojis
- Zero-Yellow Subtitles (White dialogue + Orange keywords + 5px black stroke)
- 100% External B-Roll cuts
- Ducked Lo-Fi BGM with EBU R128 (-14 LUFS) Audio Mastering
- 1080x1920 9:16 Canvas with 1080x940 Active Video Window

Usage:
    python edit_reel.py --input "RAW_VIDEOS/IMG_2409.MOV"
    python edit_reel.py --title "Career vs Relationship" --subtitle "எது முக்கியம்?"
"""

import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path

from core.config import (
    PACKAGE_ROOT, ASSETS_DIR, FONTS_DIR, EMOJIS_DIR,
    AUDIO_DIR, BROLLS_DIR, EXPORT_DIR, RAW_DIR,
    get_style_config
)
from core.banner import create_header_banner
from core.subtitle_generator import create_ass_subtitles
from core.camera_director import extract_cut_chunk
from core.audio_master import master_audio
from core.compositor import composite_final_reel, extract_qa_frames

def parse_args():
    parser = argparse.ArgumentParser(description="Automated Reel Video Editor")
    parser.add_argument("--input", "-i", type=str, help="Path to raw video input file")
    parser.add_argument("--style", type=str, default="reference_11", help="Preset style to apply (default: 'reference 11')")
    parser.add_argument("--title", "-t", type=str, default="1 Lakh Job Challenge", help="Line 1 Header Title")
    parser.add_argument("--subtitle", "-s", type=str, default="499 Days-ல 1 Lakh Jobs!", help="Line 2 Hook Subtitle")
    parser.add_argument("--emoji1", type=str, default="fire.png", help="Emoji 1 icon filename")
    parser.add_argument("--emoji2", type=str, default="target.png", help="Emoji 2 icon filename")
    parser.add_argument("--output", "-o", type=str, default=None, help="Output MP4 file path")
    return parser.parse_args()

def main():
    args = parse_args()
    style_cfg = get_style_config(args.style)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Resolve Input Video
    input_video = None
    if args.input and Path(args.input).exists():
        input_video = Path(args.input).resolve()
    else:
        # Check RAW_VIDEOS folder
        raw_files = list(RAW_DIR.glob("*.MOV")) + list(RAW_DIR.glob("*.mov")) + list(RAW_DIR.glob("*.mp4"))
        if not raw_files:
            # Check legacy RAW VIDEOS folder if present
            legacy_raw = PACKAGE_ROOT / "RAW VIDEOS"
            if legacy_raw.exists():
                raw_files = list(legacy_raw.glob("*.MOV")) + list(legacy_raw.glob("*.mov")) + list(legacy_raw.glob("*.mp4"))

        if raw_files:
            # Pick latest modified
            input_video = sorted(raw_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]
            print(f"[INFO] Auto-detected raw video: {input_video.name}")
        else:
            print("[ERROR] No input video specified and none found in RAW_VIDEOS/")
            print("Please provide a video file: python edit_reel.py --input \"path/to/video.mov\"")
            sys.exit(1)

    output_video = args.output
    if not output_video:
        output_video = str(EXPORT_DIR / f"{input_video.stem}-reel.mp4")

    print(f"\n==========================================")
    print(f"🎬 AUTOMATED REEL EDITOR")
    print(f"==========================================")
    print(f"Style:    {style_cfg['name']}")
    print(f"Input:    {input_video}")
    print(f"Output:   {output_video}")
    print(f"Title:    {args.title}")
    print(f"Subtitle: {args.subtitle}")
    print(f"==========================================\n")

    temp_dir = Path(tempfile.mkdtemp(prefix="reel_edit_"))
    try:
        # Step 1: Generate Persistent 2-Line Header Banner
        banner_png = temp_dir / "header_banner.png"
        print("📌 [1/5] Generating Signature Two-Line Header Banner...")
        create_header_banner(
            line1_text=args.title,
            line2_text=args.subtitle,
            emoji1_name=args.emoji1,
            emoji2_name=args.emoji2,
            output_path=str(banner_png)
        )

        # Step 2: Define Timeline Cuts & B-Rolls
        # Default proven high-converting editorial timeline (60 seconds)
        broll_grad = str(BROLLS_DIR / "broll_graduates.mp4")
        broll_offer = str(BROLLS_DIR / "broll_offer_letter.mp4")
        broll_glitch = str(BROLLS_DIR / "broll_glitch_alert.mp4")
        broll_stress = str(BROLLS_DIR / "broll_stress_resolve.mp4")
        broll_success = str(BROLLS_DIR / "broll_skyscraper_success.mp4")

        cuts = [
            # 1. Opening Hook: Host/Girl (Speaker 2, Zoom 1.15x, 0.6s B&W flash)
            (1,  3.60,  9.20, 2, True,  None, True,
             "உங்களுக்கு எப்படி இந்த ஐடியா வந்தது? {\\c&H000782EA&}499 Days-ல 1 Lakh பேருக்கு{\\c&H00FFFFFF&} வேலை வாங்கி தரேன் சொன்னீங்க?!"),
            
            # 2. Backstory: 1000 Jobs
            (2,  255.00, 260.50, 1, False, None, False,
             "நான் என் கம்பெனில {\\c&H000782EA&}ஒரு 1000 பேருக்கு{\\c&H00FFFFFF&} வேலை வாங்கி தர போறேன்னு ஆரம்பிச்சேன்..."),
            
            # 3. B-Roll 1: College Graduates
            (3,  270.00, 275.50, 1, False, broll_grad, False,
             "ஆனா {\\c&H000782EA&}Day 7-லயே 600+ பேருக்கு{\\c&H00FFFFFF&} வேலை வாங்கி கொடுத்தாச்சு!"),
            
            # 4. Scaling Target
            (4,  281.50, 286.00, 1, True,  None, False,
             "1000 பேருக்கு முடிக்க முடியுதுன்னா, {\\c&H000782EA&}10,000 பேருக்கு{\\c&H00FFFFFF&} ஏன் முடிக்க முடியாதுன்னு மாத்துனேன்!"),
            
            # 5. B-Roll 2: Contract Offer Letter
            (5,  287.50, 292.50, 1, False, broll_offer, False,
             "அப்போ {\\c&H000782EA&}Day 39-ல பாத்தீங்கன்னா 5,500 பேருக்கு{\\c&H00FFFFFF&} வேலை கொடுத்தாச்சு!"),
            
            # 6. Disaster Setup
            (6,  292.50, 296.50, 1, False, None, False,
             "Day 40 காலையில எழுந்து {\\c&H000782EA&}இன்ஸ்டாகிராம் திறந்து{\\c&H00FFFFFF&} பார்க்கிறேன்..."),
            
            # 7. B-Roll 3: Critical Error / Banned Red Alert
            (7,  296.50, 299.80, 1, False, broll_glitch, False,
             "இன்ஸ்டாகிராம் அக்கவுண்ட் {\\c&H000782EA&}BANNED!{\\c&H00FFFFFF&} எப்படி இருக்கும்?!"),
            
            # 8. Guy Emotional Peak / The Question
            (8,  299.80, 305.50, 1, True,  None, False,
             "நீங்க கஷ்டப்பட்டு பில்ட் பண்ண எல்லாமே... {\\c&H000782EA&}ஒரு நொடியில போயிடுச்சுன்னா{\\c&H00FFFFFF&} என்ன பண்ணுவீங்க?!"),
            
            # 9. B-Roll 4: Dark Room Pressure & Resolve
            (9,  305.50, 309.50, 1, False, broll_stress, False,
             "மறுபடியும் ஆரம்பிப்பேன்! {\\c&H000782EA&}மறுபடியும் ஆரம்பிச்சேன்!{\\c&H00FFFFFF&}"),
            
            # 10. NGO Comparison
            (10, 348.00, 353.50, 1, False, None, False,
             "ஒரு NGO இவ்வளவு இன்வெஸ்ட் பண்ணி {\\c&H000782EA&}20,000 பேருக்கு வேலை{\\c&H00FFFFFF&} தரேன்னு முடிவு பண்ணா..."),
            
            # 11. B-Roll 5: Skyscraper Sunrise Victory
            (11, 353.50, 359.50, 1, False, broll_success, False,
             "நான் ஒரு ஆளா {\\c&H000782EA&}1,00,000 பேருக்கு வேலை{\\c&H00FFFFFF&} வாங்கி தருவேன்னு முடிவு பண்ணேன்!"),
            
            # 12. Climax / Call to Action
            (12, 309.50, 315.00, 1, True,  None, False,
             "இந்த சவால்தான் நம்மளை {\\c&H000782EA&}வேற ஒரு மனிதனா{\\c&H00FFFFFF&} மாத்தும்! ஜெயிப்போம்!"),
        ]

        print("✂️  [2/5] Rendering Individual Cuts & Integrating B-Rolls...")
        chunk_files = []
        timeline_subs = []
        current_time = 0.0

        for idx, start, end, speaker, zoom, broll, is_hook, sub_text in cuts:
            dur = end - start
            timeline_subs.append((current_time, current_time + dur, sub_text))
            chunk_file = str(temp_dir / f"chunk_{idx:02d}.mp4")
            extract_cut_chunk(
                raw_video_path=str(input_video),
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
        print(f"    Total Video Length: {total_duration:.2f}s ({total_duration/60:.2f} min)")

        # Step 3: Concat Video Chunks
        print("🔗 [3/5] Concatenating Video Segments...")
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

        # Step 4: Subtitles & Audio Mastering
        print("📝 [4/5] Building Zero-Yellow ASS Subtitles & Mastering Audio (-14 LUFS)...")
        ass_subtitles = str(temp_dir / "subtitles.ass")
        create_ass_subtitles(timeline_subs, ass_subtitles)

        mastered_audio_wav = str(temp_dir / "mastered_audio.wav")
        master_audio(raw_concat_mp4, mastered_audio_wav, total_duration)

        # Step 5: Final Composite & QA
        print("🎨 [5/5] Compositing 9:16 Reel with Guaranteed Looping Banner...")
        composite_final_reel(
            concat_video_path=raw_concat_mp4,
            mastered_audio_path=mastered_audio_wav,
            banner_png_path=str(banner_png),
            ass_subtitle_path=ass_subtitles,
            output_mp4_path=output_video,
            duration=total_duration
        )

        # Verification QA Frames
        qa_times = [
            ("hook_start", 2.0),
            ("broll_graduates", 13.0),
            ("broll_offer", 23.0),
            ("broll_glitch", 30.5),
            ("stress_resolve", 45.0),
            ("victory_sunrise", 53.0)
        ]
        qa_frames = extract_qa_frames(output_video, str(EXPORT_DIR), qa_times)

        print("\n==========================================")
        print("🎉 REEL EDITING COMPLETE!")
        print(f"Saved: {output_video}")
        print("QA Frames:")
        for qf in qa_frames:
            print(f"  - {qf}")
        print("==========================================\n")

    finally:
        # Cleanup temporary cut files
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
