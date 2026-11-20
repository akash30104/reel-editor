import subprocess, json, os

os.chdir(r"c:\Users\91861\Downloads\REEL EDITOR")

wav_path = "raw_first60.wav"
if not os.path.exists(wav_path):
    cmd = ['ffmpeg', '-ss', '0', '-t', '60', '-i', r'RAW VIDEOS\1205 2k.mp4', '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', wav_path, '-y']
    subprocess.run(cmd, check=True)

cmd_whisper = ['whisper', wav_path, '--model', 'small', '--language', 'ta', '--output_format', 'json']
subprocess.run(cmd_whisper, check=True)

with open('raw_first60.json', encoding='utf-8') as f:
    data = json.load(f)

print("--- TAMIL TRANSCRIPT WITH TIMESTAMPS ---")
for seg in data.get('segments', []):
    s = seg['start']
    e = seg['end']
    t = seg['text'].strip()
    print(f"[{s:05.2f}s - {e:05.2f}s]: {t}")
