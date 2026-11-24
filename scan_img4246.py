import whisper

model = whisper.load_model("base")
audio = whisper.load_audio("/Users/pgi/.gemini/antigravity/scratch/reel-editor/IMG_4246_audio_16k.wav")
sr = 16000

for st in [0, 60, 150, 300, 500, 750, 1000, 1300, 1600]:
    chunk = audio[st*sr : (st+35)*sr]
    res = model.transcribe(chunk, fp16=False)
    lang = res["language"]
    print(f"\n=== At {st}s (lang={lang}) ===")
    for s in res["segments"]:
        st_t = s["start"] + st
        et_t = s["end"] + st
        txt = s["text"]
        print(f"  [{st_t:.1f} - {et_t:.1f}] {txt}")
