import os
os.environ["PATH"] = "/Users/pgi/.local/bin:" + os.environ.get("PATH", "")
import whisper

audio_path = "/Users/pgi/.gemini/antigravity/scratch/reel-editor/slice_test.wav"
model = whisper.load_model("small")
res = model.transcribe(
    audio_path,
    language="ta",
    beam_size=5,
    condition_on_previous_text=False,
    initial_prompt="ராமாயணம், திரைப்படம், வாழ்க்கை, உறவுகள், நட்பு, ராமர், குகன்"
)
print("Language:", res["language"])
print("Text:\n", res["text"])
for s in res["segments"]:
    st = s["start"]
    et = s["end"]
    txt = s["text"].strip()
    print(f"[{st:.2f} - {et:.2f}] {txt}")
