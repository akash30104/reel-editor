import whisper
import subprocess

# Extract 15s to 35s
subprocess.run(['ffmpeg', '-y', '-ss', '16.5', '-to', '33.0', '-i', 'RAW VIDEOS/1205 2k.mp4', '-vn', '-ar', '16000', '-ac', '1', 'segment_toxic.wav'], capture_output=True)

model = whisper.load_model('base')
# transcribe in Tamil with prompt
res = model.transcribe('segment_toxic.wav', language='ta', initial_prompt='ஏன் பெண்கள் toxic பசங்க மேல போறாங்க drama சண்டை')

print("Tamil:")
for s in res['segments']:
    print(f"[{s['start']:.2f} - {s['end']:.2f}]: {s['text']}")

# transcribe in English (translate)
res_en = model.transcribe('segment_toxic.wav', task='translate')
print("\nEnglish translation:")
for s in res_en['segments']:
    print(f"[{s['start']:.2f} - {s['end']:.2f}]: {s['text']}")
