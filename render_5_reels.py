#!/usr/bin/env python3
"""
Batch Renderer: 5 High-Quality Viral Tamil Podcast Reels
Renders 5 distinct reels from IMG_7020.MOV with locked reference style:
- Single big bold orange title (#EA8207, auto-fitted font size, Twemojis)
- Seated camera framing fix (headroom, gestures, no head cutoff)
- Relevant HD B-rolls integrated per topic
- Meta AI Demucs v4 vocal isolation & EBU R128 (-14 LUFS) mastering
- Zero-Yellow subtitles (white dialogue, orange highlights, 5px black stroke)
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

from core.banner import create_header_banner
from core.subtitle_generator import create_ass_subtitles
from core.camera_director import extract_cut_chunk
from core.audio_master import master_audio
from core.compositor import composite_final_reel, extract_qa_frames

RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/IMG_7020.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
BROLLS_DIR = PROJECT_ROOT / "assets" / "brolls"

# B-Roll file paths
broll_couple = str(BROLLS_DIR / "broll_couple.mp4")
broll_breakup = str(BROLLS_DIR / "broll_breakup.mp4")
broll_business = str(BROLLS_DIR / "broll_business.mp4")
broll_clock = str(BROLLS_DIR / "broll_clock.mp4")
broll_family = str(BROLLS_DIR / "broll_family.mp4")

REELS = [
    {
        "id": 1,
        "filename": "Reel_1_PDA_Relationship.mp4",
        "title": "Relationship-ல PDA தவறா?",
        "emoji1": "broken_heart.png",
        "emoji2": "fire.png",
        "cuts": [
            (1,  70.50,  75.80, 1, True,  None, True,
             "நாம ஏன் ஃபர்ஸ்ட் வெளியே போறோம்? {\\c&H000782EA&}மனசு விட்டு பேசவா?{\\c&H00FFFFFF&}"),
            (2,  75.80,  77.00, 2, False, None, False,
             "ஆமாம், {\\c&H000782EA&}கண்டிப்பா!{\\c&H00FFFFFF&}"),
            (3,  77.00,  83.50, 2, True,  broll_couple, False,
             "ஆனா இப்போ பார்க், பீச்-ல {\\c&H000782EA&}Public Display of Affection{\\c&H00FFFFFF&} தான் பண்றாங்க!"),
            (4, 115.00, 122.00, 2, False, None, False,
             "இது {\\c&H000782EA&}Healthy Relationship-ஆ?{\\c&H00FFFFFF&} இல்ல Unhealthy-ஆ?"),
            (5, 122.00, 126.50, 2, True,  None, False,
             "எல்லாரும் முன்னாடியும் {\\c&H000782EA&}PDA பண்றது சரியா?{\\c&H00FFFFFF&}"),
            (6, 126.50, 136.00, 1, False, None, False,
             "Intimacy என்பது மத்தவங்க பாக்குற காட்சி பொருள் இல்ல! {\\c&H000782EA&}அது ரொம்ப High-Value விஷயம்!{\\c&H00FFFFFF&}"),
            (7, 136.00, 142.50, 1, True,  None, False,
             "அதை ரோட்டுல பப்ளிக்கா பண்ணா, {\\c&H000782EA&}நீங்க எந்த அளவுக்கு தரம் கெட்டு போயிருக்கீங்கன்னு{\\c&H00FFFFFF&} தான் காட்டும்!")
        ]
    },
    {
        "id": 2,
        "filename": "Reel_2_Breakup_RedFlags.mp4",
        "title": "Breakup பண்ண இந்த 1 காரணம் போதும்!",
        "emoji1": "broken_heart.png",
        "emoji2": "fire.png",
        "cuts": [
            (1, 148.50, 154.50, 2, True,  None, True,
             "Boys side-ல இருந்து சொல்லுங்க... {\\c&H000782EA&}ஒரு பொண்ணுகிட்ட என்ன பழக்கம் இருந்தா{\\c&H00FFFFFF&} Breakup பண்ணனும்?"),
            (2, 154.50, 159.00, 2, False, None, False,
             "நீங்க பசங்களுக்கு என்ன {\\c&H000782EA&}Suggestion தருவீங்க?{\\c&H00FFFFFF&}"),
            (3, 159.00, 166.00, 1, False, None, False,
             "முதல்ல உங்க Partner {\\c&H000782EA&}உங்க Career-க்கு Support{\\c&H00FFFFFF&} பண்றாங்களான்னு பாக்கணும்!"),
            (4, 166.00, 172.50, 1, True,  broll_breakup, False,
             "உங்க வளர்ச்சியை தடுக்கிற பழக்கம் இருந்தா, {\\c&H000782EA&}அது பெரிய Red Flag!{\\c&H00FFFFFF&}"),
            (5, 172.50, 180.00, 1, False, None, False,
             "அவங்க கூட இருக்கும்போது {\\c&H000782EA&}Insecurity இல்லாம மன அமைதி{\\c&H00FFFFFF&} கிடைக்கணும்!"),
            (6, 180.00, 186.50, 1, True,  None, False,
             "அது இல்லாத Relationship-ல {\\c&H000782EA&}நீங்க இருக்கவே கூடாது!{\\c&H00FFFFFF&} விலகிடுங்க!")
        ]
    },
    {
        "id": 3,
        "filename": "Reel_3_True_Man_Role.mp4",
        "title": "ஒரு ஆணின் உண்மையான அடையாளம்!",
        "emoji1": "fire.png",
        "emoji2": "target.png",
        "cuts": [
            (1, 288.00, 294.50, 2, True,  None, True,
             "Relationship-ல {\\c&H000782EA&}Support-உம் Care-உம் தான்{\\c&H00FFFFFF&} ரொம்ப முக்கியம் இல்லையா?"),
            (2, 294.50, 298.50, 1, False, None, False,
             "ஆமாம், {\\c&H000782EA&}கண்டிப்பா அதுதான் base!{\\c&H00FFFFFF&}"),
            (3, 298.50, 308.00, 1, True,  broll_business, False,
             "ஒரு ஆணோட உண்மையான பலம் {\\c&H000782EA&}பெண்ணுக்கு பாதுகாப்பும் மரியாதையும்{\\c&H00FFFFFF&} தர்றதுலதான் இருக்கு!"),
            (4, 308.00, 318.00, 1, False, None, False,
             "அவங்களோட Status-ஐ உயர்த்துற ஆம்பளையாதான் {\\c&H000782EA&}நம்ம இருக்கணும்!{\\c&H00FFFFFF&}"),
            (5, 318.00, 328.00, 1, True,  None, False,
             "ஒரு பெண் இல்லாத வீடு {\\c&H000782EA&}வீடே கெடையாது...{\\c&H00FFFFFF&} அது வெறும் ரூம்!"),
            (6, 328.00, 334.00, 1, False, None, False,
             "அவங்கள மதிக்கிறவன்தான் {\\c&H000782EA&}உண்மையான ஆண்மகன்!{\\c&H00FFFFFF&}")
        ]
    },
    {
        "id": 4,
        "filename": "Reel_4_Irreplaceable_Mindset.mp4",
        "title": "Replaceable-ஆ? Irreplaceable-ஆ?",
        "emoji1": "target.png",
        "emoji2": "bulb.png",
        "cuts": [
            (1, 448.00, 454.00, 2, True,  None, True,
             "நம்ம லைஃப்ல {\\c&H000782EA&}ஒருத்தரோட Value-வை{\\c&H00FFFFFF&} எப்படி புரிஞ்சுக்கிறது?"),
            (2, 454.00, 461.00, 1, False, None, False,
             "இந்த உலகத்துல {\\c&H000782EA&}Replaceable-ஆ இருக்கீங்களா,{\\c&H00FFFFFF&} இல்ல Irreplaceable-ஆன்னு பாக்கணும்!"),
            (3, 461.00, 468.00, 1, True,  broll_clock, False,
             "யார் வேணா Replace பண்ணக்கூடிய இடத்துல இருந்தா, {\\c&H000782EA&}உங்க நேரத்துக்கு மதிப்பிருக்காது!{\\c&H00FFFFFF&}"),
            (4, 468.00, 476.00, 1, True,  None, False,
             "உங்க திறமையையும் கேரக்டரையும் {\\c&H000782EA&}யாராலயும் மாற்ற முடியாத அளவுக்கு{\\c&H00FFFFFF&} வளர்த்துக்கோங்க!")
        ]
    },
    {
        "id": 5,
        "filename": "Reel_5_Mother_Love.mp4",
        "title": "அம்மாவுக்கு இணையான அன்பு இல்ல!",
        "emoji1": "broken_heart.png",
        "emoji2": "fire.png",
        "cuts": [
            (1, 870.00, 875.00, 2, True,  None, True,
             "அம்மாவோட அன்பை பத்தி {\\c&H000782EA&}நீங்க என்ன நினைக்கிறீங்க?{\\c&H00FFFFFF&}"),
            (2, 875.00, 883.00, 1, False, None, False,
             "ஒரு அம்மாவுக்கு தெரியுறது {\\c&H000782EA&}குழந்தையோட எதிர்காலம் மட்டும்தான்!{\\c&H00FFFFFF&}"),
            (3, 883.00, 892.00, 1, True,  broll_family, False,
             "தன் கஷ்டத்தை காட்டிக்காம, {\\c&H000782EA&}குழந்தையோட கனவுகளுக்காக வாழறவங்க{\\c&H00FFFFFF&} அம்மா!"),
            (4, 892.00, 902.00, 1, False, None, False,
             "இந்த உலகத்துல எந்த உறவு மாறினாலும், {\\c&H000782EA&}அம்மாவுடைய தியாகம்{\\c&H00FFFFFF&} என்னைக்கும் மாறாது!"),
            (5, 902.00, 912.00, 1, True,  None, False,
             "அவங்கள மதிக்கிறவங்க {\\c&H000782EA&}வாழ்க்கையில என்னைக்குமே தோற்க மாட்டாங்க!{\\c&H00FFFFFF&}")
        ]
    }
]

def render_single_reel(reel_cfg):
    reel_id = reel_cfg["id"]
    output_mp4 = EXPORT_DIR / reel_cfg["filename"]
    print(f"\n==========================================")
    print(f"🎬 RENDERING REEL {reel_id}/5: {reel_cfg['title']}")
    print(f"==========================================")
    print(f"Output: {output_mp4}")

    temp_dir = Path(tempfile.mkdtemp(prefix=f"reel_{reel_id}_"))
    try:
        # 1. Header Banner (Single Big Title with auto-fit)
        banner_png = temp_dir / "header_banner.png"
        print("  📌 [1/5] Generating Auto-Fitted Single Big Title Header...")
        create_header_banner(
            line1_text=reel_cfg["title"],
            line2_text=None,
            emoji1_name=reel_cfg["emoji1"],
            emoji2_name=reel_cfg["emoji2"],
            output_path=str(banner_png)
        )

        # 2. Extract Cuts
        print("  ✂️  [2/5] Rendering Cuts & B-Rolls with Seated Framing...")
        chunk_files = []
        timeline_subs = []
        current_time = 0.0
        broll_sample_t = None

        for idx, start, end, speaker, zoom, broll, is_hook, sub_text in reel_cfg["cuts"]:
            dur = end - start
            if broll and broll_sample_t is None:
                broll_sample_t = current_time + (dur / 2.0)
            timeline_subs.append((current_time, current_time + dur, sub_text))
            chunk_file = str(temp_dir / f"chunk_{idx:02d}.mp4")
            extract_cut_chunk(
                raw_video_path=str(RAW_VIDEO),
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
        print(f"      Total Duration: {total_duration:.2f}s | B-Roll midpoint: {broll_sample_t:.2f}s")

        # 3. Concatenate Cuts
        print("  🔗 [3/5] Concatenating Video Chunks...")
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

        # 4. Demucs Vocal Isolation & EBU R128 Mastering
        print("  🎙️  [4/5] Audio Enhancement with Demucs & EBU R128 Mastering...")
        raw_speech_wav = str(temp_dir / "raw_speech.wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_concat_mp4,
            "-vn", "-ar", "44100", "-ac", "2", raw_speech_wav
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        enhanced_speech_wav = raw_speech_wav
        try:
            demucs_bin = shutil.which("demucs") or str(PROJECT_ROOT / ".venv" / "bin" / "demucs")
            demucs_out_dir = temp_dir / "demucs_clean"
            subprocess.run([
                demucs_bin, "--two-stems=vocals", "-n", "htdemucs",
                "-o", str(demucs_out_dir), raw_speech_wav
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            demucs_vocals = demucs_out_dir / "htdemucs" / "raw_speech" / "vocals.wav"
            if demucs_vocals.exists():
                enhanced_speech_wav = str(demucs_vocals)
                print("      Demucs vocal separation applied successfully!")
        except Exception as e:
            print(f"      Demucs note: {e}")

        mastered_audio_wav = str(temp_dir / "mastered_audio.wav")
        master_audio(enhanced_speech_wav, mastered_audio_wav, total_duration)

        # Zero-Yellow ASS Subtitles
        ass_subtitles = str(temp_dir / "subtitles.ass")
        create_ass_subtitles(timeline_subs, ass_subtitles)

        # 5. Composite Final Reel
        print("  🎨 [5/5] Compositing 9:16 Video Canvas with Subtitles & Header...")
        composite_final_reel(
            concat_video_path=raw_concat_mp4,
            mastered_audio_path=mastered_audio_wav,
            banner_png_path=str(banner_png),
            ass_subtitle_path=ass_subtitles,
            output_mp4_path=str(output_mp4),
            duration=total_duration
        )

        # QA Snapshot extraction (midpoint of B-roll guaranteed!)
        qa_times = [
            (f"reel_{reel_id}_hook", 2.0),
            (f"reel_{reel_id}_broll", broll_sample_t if broll_sample_t else (total_duration * 0.4)),
            (f"reel_{reel_id}_climax", max(5.0, total_duration - 3.0))
        ]
        qa_frames = extract_qa_frames(str(output_mp4), str(EXPORT_DIR), qa_times)
        print(f"  ✅ REEL {reel_id} COMPLETE! Saved: {output_mp4.name}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    print("==================================================")
    print("🚀 BATCH EDITING 5 HIGH-QUALITY REELS (IMG_7020)")
    print("==================================================")

    for reel_cfg in REELS:
        render_single_reel(reel_cfg)

    print("\n==================================================")
    print("🎉 ALL 5 REELS COMPLETED SUCCESSFULLY!")
    print(f"Destination: {EXPORT_DIR}")
    print("==================================================")

if __name__ == "__main__":
    main()
