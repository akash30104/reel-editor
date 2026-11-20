import subprocess

cmd = ['ffmpeg', '-ss', '180', '-to', '360', '-i', 'RAW VIDEOS/1205 2k.mp4', '-af', 'silencedetect=noise=-30dB:d=0.35', '-f', 'null', '-']
res = subprocess.run(cmd, capture_output=True, text=True)
with open('silences_180_360.txt', 'w', encoding='utf-8') as f:
    f.write(res.stderr)

print("Saved silences_180_360.txt")
