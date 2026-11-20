import speech_recognition as sr
import subprocess, os, re

# Detect exact silences between 315 and 390
cmd = ['ffmpeg', '-ss', '315', '-to', '390', '-i', 'RAW VIDEOS/1205 2k.mp4', '-af', 'silencedetect=noise=-30dB:d=0.3', '-f', 'null', '-']
res = subprocess.run(cmd, capture_output=True, text=True)
starts = [float(x) for x in re.findall(r'silence_start:\s*([0-9.]+)', res.stderr)]
ends = [float(x) for x in re.findall(r'silence_end:\s*([0-9.]+)', res.stderr)]
silences = list(zip(starts, ends))
pad = 0.08

speech_segs = []
cur_start = 0.0
for s_start, s_end in silences:
    seg_end = s_start + pad
    seg_start = cur_start
    if seg_end - seg_start > 0.4:
        speech_segs.append((315.0 + seg_start, 315.0 + seg_end))
    cur_start = s_end - pad

if 390.0 - (315.0 + cur_start) > 0.4:
    speech_segs.append((315.0 + cur_start, 390.0))

print(f"Found {len(speech_segs)} speech segments between 315s and 390s")

r = sr.Recognizer()
transcript_lines = []
for i, (s, e) in enumerate(speech_segs):
    dur = e - s
    wav = f"tmp_seg_{i}.wav"
    subprocess.run(['ffmpeg', '-y', '-ss', f"{s:.3f}", '-to', f"{e:.3f}", '-i', 'RAW VIDEOS/1205 2k.mp4', '-ar', '16000', '-ac', '1', wav], capture_output=True)
    try:
        with sr.AudioFile(wav) as src:
            audio = r.record(src)
        txt = r.recognize_google(audio, language='ta-IN')
    except Exception:
        txt = ""
    print(f"[{s:.2f}s - {e:.2f}s] ({dur:.2f}s): {txt}")
    transcript_lines.append((s, e, dur, txt))
    if os.path.exists(wav):
        os.remove(wav)

with open("japanese_shark_transcript.txt", "w", encoding="utf-8") as f:
    for s, e, dur, txt in transcript_lines:
        f.write(f"{s:.2f}\t{e:.2f}\t{dur:.2f}\t{txt}\n")
