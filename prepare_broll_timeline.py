import os
import subprocess

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
RAW_VIDEO = os.path.join(BASE_DIR, "RAW VIDEOS", "1205 2k.mp4")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render_v5")
BROLLS_DIR = os.path.join(BASE_DIR, "brolls")

os.makedirs(TEMP_DIR, exist_ok=True)
os.chdir(BASE_DIR)

# Cut definition:
# (idx, raw_start, raw_end, speaker, zoom, broll_file)
# If broll_file is not None, use the broll video for visual while keeping the dialogue audio!
cuts = [
    (1,  33.91, 37.81, 1, True,  None),                                   # Hook Question (Spk 1, Zoom)
    (2,  38.64, 41.71, 2, False, os.path.join(BROLLS_DIR, "broll_drama_hook.mp4")), # "வேணும் ட்ராமாஸ்!" -> B-ROLL 1 (Drama)
    (3,  41.91, 44.63, 2, True,  None),                                   # "சண்டை போட்டுட்டு ஜாலியா இருப்பாங்க!" (Spk 2, Zoom)
    (4,  44.94, 49.13, 2, False, os.path.join(BROLLS_DIR, "broll_boredom.mp4")),    # "Bore அடிக்கும்!" -> B-ROLL 2 (Boredom)
    (5,  52.74, 55.44, 2, True,  None),                                   # "Drama நடக்கணும்!" (Spk 2, Zoom)
    (6,  56.93, 58.86, 2, False, None),                                   # "Enjoy பண்ண..." (Spk 2, Normal)
    (7,   8.27, 11.38, 1, True,  None),                                   # "Toxic People Handle..." (Spk 1, Zoom)
    (8,  12.08, 16.41, 2, False, os.path.join(BROLLS_DIR, "broll_real_life.mp4")),  # "Real Life..." -> B-ROLL 3 (Real Life)
    (9,  17.78, 20.55, 2, True,  None),                                   # "பிடிக்காம பண்றோம்..." (Spk 2, Zoom)
    (10, 20.85, 22.79, 1, False, None),                                   # "கரெக்ட்! நிஜமான உண்மை!" (Spk 1, Normal)
    (11, 24.69, 28.62, 2, True,  os.path.join(BROLLS_DIR, "broll_conflict.mp4")),   # "Bored ஆயிடுறாங்க!" -> B-ROLL 4 (Conflict)
    (12, 29.00, 33.24, 2, False, None),                                   # "தப்பான ஆட்கள்..." (Spk 2, Normal)
    (13, 68.39, 72.51, 1, True,  None),                                   # "தீர்வு என்ன?" (Spk 1, Zoom)
    (14, 72.84, 76.15, 2, False, None),                                   # "Clear Boundaries..." (Spk 2, Normal)
    (15, 79.70, 84.50, 2, True,  None),                                   # "React பண்ணக் கூடாது!" (Spk 2, Zoom)
    (16, 86.67, 91.52, 1, False, None),                                   # "பாதி பிரச்சனை..." (Spk 1, Normal)
    (17, 91.86, 96.70, 2, True,  None),                                   # "மாத்த முடியாது!" (Spk 2, Zoom)
    (18, 99.94, 106.49, 2, False, None),                                  # "நிஜம் புரியும்!" (Spk 2, Normal)
]

print("=== 1. PREPARING EXTENDED TIMELINE WITH B-ROLLS ===")
chunk_files = []
timeline_timestamps = []
current_time = 0.0

for idx, start, end, speaker, zoom, broll in cuts:
    dur = end - start
    timeline_timestamps.append((current_time, current_time + dur, speaker, zoom, broll is not None))
    out_chunk = os.path.join(TEMP_DIR, f"chunk_{idx:02d}.mp4")
    
    # First extract clean dialogue audio segment (pcm_s16le, 48000Hz, stereo)
    tmp_audio = os.path.join(TEMP_DIR, f"audio_{idx:02d}.wav")
    cmd_a = [
        "ffmpeg", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", RAW_VIDEO,
        "-vn", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
        tmp_audio, "-y"
    ]
    subprocess.run(cmd_a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Now determine video stream:
    if broll and os.path.exists(broll):
        # Loop or scale B-roll to exactly 1080x940, 30fps, matching dur
        cmd_v = [
            "ffmpeg", "-stream_loop", "-1", "-i", broll, "-i", tmp_audio,
            "-t", f"{dur:.3f}",
            "-vf", "scale=1080:940:flags=lanczos,fps=30,format=yuv420p",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-c:a", "copy",
            "-map", "0:v", "-map", "1:a",
            out_chunk, "-y"
        ]
        subprocess.run(cmd_v, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Chunk {idx:02d}: B-ROLL [{broll}] -> Timeline [{current_time:.2f}s - {current_time+dur:.2f}s] ({dur:.2f}s)")
    else:
        # Standard Talking Head Video Crop
        if idx == 1:
            # Opening Hook: 0.6s B&W flash snapping to color!
            # Using curves or hue filter
            vf = (
                "crop=1198:1044:150:120,scale=1080:940:flags=lanczos,fps=30,format=yuv420p,"
                "hue=s='if(lt(t,0.6),0,1)'"
            )
        elif speaker == 1:
            if zoom:
                vf = "crop=1198:1044:150:120,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"
            else:
                vf = "crop=1378:1200:80:80,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"
        else: # speaker == 2
            if zoom:
                vf = "crop=1198:1044:1200:120,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"
            else:
                vf = "crop=1378:1200:1100:80,scale=1080:940:flags=lanczos,fps=30,format=yuv420p"

        cmd_v = [
            "ffmpeg", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", RAW_VIDEO,
            "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
            out_chunk, "-y"
        ]
        subprocess.run(cmd_v, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Chunk {idx:02d}: Raw [{start:.2f}s - {end:.2f}s] -> Timeline [{current_time:.2f}s - {current_time+dur:.2f}s] (Spk {speaker}, Zoom: {zoom})")

    chunk_files.append(out_chunk)
    current_time += dur

total_dur = current_time
print(f"\nTotal Speech Timeline: {total_dur:.2f} seconds ({total_dur/60:.2f} min)")

# Concat Chunks
concat_list = os.path.join(TEMP_DIR, "concat.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for c in chunk_files:
        f.write(f"file '{c}'\n")

raw_concat_mp4 = os.path.join(TEMP_DIR, "raw_concat_brolls.mp4")
cmd_concat = [
    "ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_list,
    "-c", "copy", raw_concat_mp4, "-y"
]
subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Concatenation complete: raw_concat_brolls.mp4")
