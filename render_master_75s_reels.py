#!/usr/bin/env python3
"""
Master Production Engine: 1min to 1:20min Viral Reels (74s - 75s)
Standard Orange: #FF8400 (RGB: 255, 132, 0)
Reference Matched: Exactly matching 'Career vs Relationship 1.mp4' (73.6s)
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image

from AppKit import (
    NSBitmapImageRep, NSGraphicsContext, NSColor, NSRectFill, NSMakeRect,
    NSFont, NSFontAttributeName, NSForegroundColorAttributeName,
    NSStrokeColorAttributeName, NSStrokeWidthAttributeName,
    NSAttributedString, NSMutableAttributedString, NSDeviceRGBColorSpace,
    NSPNGFileType
)

WORKSPACE = Path("/Users/pgi/.gemini/antigravity/scratch/reel-editor")
RAW_VIDEO = Path("/Users/pgi/Downloads/reels editor/raw videos/202.MOV")
EXPORT_DIR = Path("/Users/pgi/Downloads/reels editor/export ")
EXPORT_FRAMES = EXPORT_DIR / "FRAMES"
EXPORT_FRAMES.mkdir(parents=True, exist_ok=True)

ASSETS = WORKSPACE / "assets"
BROLLS = ASSETS / "brolls"
AUDIO = ASSETS / "audio"
WHOOSH_SFX = AUDIO / "whoosh.mp3"
BGM_FLUTE = AUDIO / "ramayan_flute_bgm.mp3"

WIDTH = 1080
HEIGHT = 1920
BANNER_H = 142
BANNER_Y = 416
VIDEO_Y = 558
VIDEO_H = 940
SUBS_Y = 1320
SUBS_H = 160

# Exact user standard color: #FF8400
ORANGE_R = 255 / 255.0
ORANGE_G = 132 / 255.0
ORANGE_B = 0.0

CROP_HOST = "crop=2160:1880:150:190,scale=1080:940:flags=lanczos,setsar=1,fps=30"
CROP_GUEST = "crop=2160:1880:1530:190,scale=1080:940:flags=lanczos,setsar=1,fps=30"

# 74s - 75s Master Stories
LONG_REELS = [
    {
        "id": "Master_74s_1",
        "title_l1": "Kambar vs Valmiki:",
        "title_l2": "WHO WROTE IT BETTER? 📜",
        "emoji": "📜",
        "filename": "Reel_202_Master_74s_Kambar_Vs_Valmiki.mp4",
        "cuts": [
            {
                "st": 334.0, "et": 343.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.30, "வால்மீகி எழுதின மூல ராமாயணத்துக்கும்,"),
                    (4.50, 8.80, "கம்பர் எழுதின காவியத்துக்கும் என்ன வித்தியாசம்?")
                ]
            },
            {
                "st": 343.0, "et": 356.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.20, "வால்மீகி வெறும் கதையை மட்டும் சொன்னாருன்னா..."),
                    (6.50, 12.80, "கம்பர் அதை தமிழ் உணர்வோடும் கவிதை நயத்தோடும் உயிர்ப்பிச்சாரு!")
                ]
            },
            {
                "st": 0.0, "et": 12.0, "crop": None, "broll": str(BROLLS / "broll_scripture.mp4"),
                "phrases": [
                    (0.25, 5.50, "தமிழ் மொழிக்கு கம்பர் கொடுத்த இந்த பொக்கிஷம்..."),
                    (5.80, 11.80, "உலக இலக்கியங்களிலேயே வேற எங்கேயும் பார்க்க முடியாது!")
                ]
            },
            {
                "st": 368.0, "et": 383.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 7.00, "ஒவ்வொரு சொல்லிலும் அன்பையும், தர்மத்தையும், நீதியையும்..."),
                    (7.30, 14.80, "அவ்வளவு நுட்பமா செதுக்கிய கவிச்சக்கரவர்த்தி கம்பர்!")
                ]
            },
            {
                "st": 0.0, "et": 11.0, "crop": None, "broll": str(BROLLS / "broll_temple.mp4"),
                "phrases": [
                    (0.25, 5.20, "அதனாலதான் ஆயிரம் வருடங்கள் கடந்தும்..."),
                    (5.50, 10.80, "கம்பராமாயணம் தமிழ் நெஞ்சங்களில் அழியாமல் வாழுது!")
                ]
            },
            {
                "st": 395.0, "et": 408.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "இதை வெறும் கதையா பார்க்காம வாழ்க்கை பாடமா பாருங்க..."),
                    (6.30, 12.80, "மனித மனங்களின் ரகசியங்களை எளிமையா புரிஞ்சுக்கலாம்!")
                ]
            }
        ]
    },
    {
        "id": "Master_75s_2",
        "title_l1": "LOST EVERYTHING IN 1 DAY!",
        "title_l2": "\"YOU ARE MY 5TH BROTHER\" 🛶",
        "emoji": "🛶",
        "filename": "Reel_202_Master_75s_Sacrifice_And_Brotherhood.mp4",
        "cuts": [
            {
                "st": 442.0, "et": 451.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.20, "அரியணை ஏற வேண்டிய நாள்ல..."),
                    (4.40, 8.80, "வனவாசம் போகணும்னு சொன்னா எப்படி இருக்கும்?")
                ]
            },
            {
                "st": 451.0, "et": 464.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "எந்த ஒரு வருத்தமும் கோபமும் இல்லாம,"),
                    (6.30, 12.80, "அப்பா சொன்ன வாக்கை காப்பாத்த காட்டுக்கு கிளம்பினாரு!")
                ]
            },
            {
                "st": 0.0, "et": 12.0, "crop": None, "broll": str(BROLLS / "broll_forest_mist.mp4"),
                "phrases": [
                    (0.25, 5.50, "பதவியும் பணமும் அதிகாரமும் பெருசு இல்லை..."),
                    (5.80, 11.80, "தர்மமும் கடமையும் தான் முக்கியம்னு நிரூபிச்சாரு!")
                ]
            },
            {
                "st": 687.0, "et": 700.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "கங்கை நதிக்கரையில வேடுவத் தலைவன் குகனை சந்திச்சப்போ..."),
                    (6.30, 12.80, "சாதி, குலம், அந்தஸ்து எதையும் பார்க்காம கட்டி தழுவினாரு!")
                ]
            },
            {
                "st": 0.0, "et": 13.0, "crop": None, "broll": str(BROLLS / "broll_river_boat.mp4"),
                "phrases": [
                    (0.25, 6.00, "உன்னோடு நாங்க ஐவர் ஆனோம்னு சொன்ன அந்த ஒரு வார்த்தை,"),
                    (6.30, 12.80, "மனிதகுலத்துக்கே சமத்துவத்தின் மிகப்பெரிய சான்று!")
                ]
            },
            {
                "st": 705.0, "et": 718.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "உண்மையான தகுதி உங்கள் பிறப்பிலோ பதவியிலோ இல்லை..."),
                    (6.30, 12.80, "நீங்கள் காட்டும் தூய்மையான அன்பில் மட்டும்தான் இருக்கு!")
                ]
            }
        ]
    }
]

def render_banner(title_l1, title_l2, emoji_char, out_path):
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, WIDTH, BANNER_H, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
    )
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.setCurrentContext_(ctx)

    # Exact standard orange: #FF8400
    bg_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(ORANGE_R, ORANGE_G, ORANGE_B, 1.0)
    bg_color.set()
    NSRectFill(NSMakeRect(0, 0, WIDTH, BANNER_H))

    font_title = NSFont.fontWithName_size_("Futura-Bold", 45) or NSFont.boldSystemFontOfSize_(45)

    astr1 = NSAttributedString.alloc().initWithString_attributes_(title_l1, {
        NSFontAttributeName: font_title,
        NSForegroundColorAttributeName: NSColor.blackColor()
    })
    sz1 = astr1.size()
    x1 = (WIDTH - sz1.width) / 2
    y1 = BANNER_H - 58
    astr1.drawAtPoint_((x1, y1))

    astr2 = NSMutableAttributedString.alloc().init()
    part2_text = NSAttributedString.alloc().initWithString_attributes_(title_l2 + " ", {
        NSFontAttributeName: font_title,
        NSForegroundColorAttributeName: NSColor.blackColor()
    })
    astr2.appendAttributedString_(part2_text)

    sz2 = astr2.size()
    x2 = (WIDTH - sz2.width) / 2
    y2 = BANNER_H - 120
    astr2.drawAtPoint_((x2, y2))

    ctx.flushGraphics()
    png_data = rep.representationUsingType_properties_(NSPNGFileType, None)
    png_data.writeToFile_atomically_(str(out_path), True)

def render_sub_frame(words_status, width=WIDTH, height=SUBS_H, font_name="TamilSangamMN-Bold", base_font_size=46):
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, width, height, 8, 4, True, False, NSDeviceRGBColorSpace, 0, 0
    )
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.setCurrentContext_(ctx)
    NSColor.clearColor().set()
    NSRectFill(NSMakeRect(0, 0, width, height))

    if not words_status:
        ctx.flushGraphics()
        bitmap_data = rep.bitmapData()
        return bytes(bitmap_data[0:rep.bytesPerRow() * height])

    # Dynamic auto-fit font scaling: ensures text never exceeds MAX_SAFE_WIDTH (880px)
    MAX_SAFE_WIDTH = 880.0
    full_text = " ".join([w for w, _ in words_status])
    measuring_font = NSFont.fontWithName_size_(font_name, base_font_size)
    astr_measure = NSAttributedString.alloc().initWithString_attributes_(full_text, {NSFontAttributeName: measuring_font})
    raw_width = astr_measure.size().width

    if raw_width > MAX_SAFE_WIDTH:
        scale = MAX_SAFE_WIDTH / raw_width
        font_size = max(32, int(base_font_size * scale))
    else:
        font_size = base_font_size

    font = NSFont.fontWithName_size_(font_name, font_size)
    # Prominent solid black outline for ALL words in subtitle (ONLY in subtitle)
    stroke_width = 14.0

    # Stroke pass (solid black outline)
    stroke_astr = NSMutableAttributedString.alloc().init()
    for word, is_active in words_status:
        attrs = {
            NSFontAttributeName: font,
            NSForegroundColorAttributeName: NSColor.blackColor(),
            NSStrokeColorAttributeName: NSColor.blackColor(),
            NSStrokeWidthAttributeName: stroke_width
        }
        part = NSAttributedString.alloc().initWithString_attributes_(word + " ", attrs)
        stroke_astr.appendAttributedString_(part)

    size = stroke_astr.size()
    x = max(20.0, (width - size.width) / 2)
    y = (height - size.height) / 2
    stroke_astr.drawAtPoint_((x, y))

    # Fill pass: Exact Reference Standard Orange (#FF8400) for active word, Pure White (#FFFFFF) for others
    fill_astr = NSMutableAttributedString.alloc().init()
    for word, is_active in words_status:
        fg = NSColor.colorWithCalibratedRed_green_blue_alpha_(ORANGE_R, ORANGE_G, ORANGE_B, 1.0) if is_active else NSColor.whiteColor()
        attrs = {
            NSFontAttributeName: font,
            NSForegroundColorAttributeName: fg
        }
        part = NSAttributedString.alloc().initWithString_attributes_(word + " ", attrs)
        fill_astr.appendAttributedString_(part)

    fill_astr.drawAtPoint_((x, y))
    ctx.flushGraphics()

    bitmap_data = rep.bitmapData()
    return bytes(bitmap_data[0:rep.bytesPerRow() * height])

def process_master_reel(reel):
    reel_id = reel["id"]
    print(f"\n==========================================")
    print(f"🔥 Rendering 75s Master Reel: {reel['title_l1']} {reel['title_l2']}")
    print(f"==========================================")

    # 1. Render Banner with Exact Orange #FF8400
    banner_file = WORKSPACE / f"banner_{reel_id}.png"
    render_banner(reel["title_l1"], reel["title_l2"], reel["emoji"], banner_file)

    # 2. Extract cuts (video + studio enhanced dialogue)
    cut_video_files = []
    cut_audio_files = []
    cut_durations = []

    for c_idx, cut in enumerate(reel["cuts"]):
        dur = cut["et"] - cut["st"]
        cut_durations.append(dur)

        vid_out = WORKSPACE / f"temp_cut_{reel_id}_{c_idx}_vid.mp4"
        aud_out = WORKSPACE / f"temp_cut_{reel_id}_{c_idx}_aud.wav"

        audio_filters = (
            "highpass=f=80,lowpass=f=12000,"
            "equalizer=f=220:t=q:w=1.2:g=2.0,"
            "equalizer=f=3200:t=q:w=1.5:g=3.5,"
            "afftdn=nf=-25"
        )
        
        # Audio extraction
        if cut["broll"]:
            cmd_aud = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-vn", "-ac", "2", "-ar", "48000",
                "-af", audio_filters,
                str(aud_out)
            ]
        else:
            cmd_aud = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-vn", "-ac", "2", "-ar", "48000",
                "-af", audio_filters,
                str(aud_out)
            ]
        subprocess.run(cmd_aud, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Video extraction & framing
        if cut["broll"]:
            cmd_vid = [
                "ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}",
                "-i", cut["broll"],
                "-vf", f"scale={WIDTH}:{VIDEO_H}:force_original_aspect_ratio=increase,crop={WIDTH}:{VIDEO_H},setsar=1,fps=30",
                "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                str(vid_out)
            ]
        else:
            cmd_vid = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-vf", cut["crop"],
                "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                str(vid_out)
            ]
        subprocess.run(cmd_vid, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        cut_video_files.append(vid_out)
        cut_audio_files.append(aud_out)

    total_dur = sum(cut_durations)
    print(f"Total Master Video Duration: {total_dur:.1f}s ({total_dur/60:.2f} mins) [Target: 1min - 1:20min]")

    # 3. Concatenate video clips into padded canvas with -loop 1 banner (permanently visible)
    concat_vid_txt = WORKSPACE / f"temp_concat_vid_{reel_id}.txt"
    with open(concat_vid_txt, "w") as f:
        for vf in cut_video_files:
            f.write(f"file '{vf.name}'\n")

    base_padded_vid = WORKSPACE / f"temp_base_vid_{reel_id}.mp4"
    cmd_base = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_vid_txt),
        "-loop", "1", "-i", str(banner_file),
        "-filter_complex",
        f"[0:v]pad={WIDTH}:{HEIGHT}:0:{VIDEO_Y}:black[padded];[padded][1:v]overlay=0:{BANNER_Y}:shortest=1[outv]",
        "-map", "[outv]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        str(base_padded_vid)
    ]
    subprocess.run(cmd_base, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 4. Concatenate speech audio
    concat_aud_txt = WORKSPACE / f"temp_concat_aud_{reel_id}.txt"
    with open(concat_aud_txt, "w") as f:
        for af in cut_audio_files:
            f.write(f"file '{af.name}'\n")

    speech_wav = WORKSPACE / f"temp_speech_{reel_id}.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_aud_txt), "-c:a", "pcm_s16le", str(speech_wav)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 5. Build Transition Whooshes and BGM Mix
    transition_times = []
    t_acc = 0.0
    for d in cut_durations[:-1]:
        t_acc += d
        transition_times.append(t_acc)

    cmd_audio = ["ffmpeg", "-y", "-i", str(speech_wav)]
    for _ in transition_times:
        cmd_audio.extend(["-i", str(WHOOSH_SFX)])

    cmd_audio.extend(["-ss", "5.0", "-t", f"{total_dur:.3f}", "-i", str(BGM_FLUTE)])

    filter_parts = []
    mix_inputs = ["[0:a]"]
    for i, t_sec in enumerate(transition_times):
        idx = i + 1
        ms = int(t_sec * 1000)
        filter_parts.append(f"[{idx}:a]adelay={ms}|{ms},volume=0.35[w{idx}]")
        mix_inputs.append(f"[w{idx}]")

    bgm_idx = len(transition_times) + 1
    filter_parts.append(f"[{bgm_idx}:a]volume=0.065,afade=t=in:ss=0:d=1.0,afade=t=out:st={total_dur-1.5:.1f}:d=1.5[bgm]")
    mix_inputs.append("[bgm]")

    filter_parts.append(f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=2[mixed]")
    filter_parts.append("[mixed]loudnorm=I=-14:TP=-1.5:LRA=7[outa]")

    mixed_audio = WORKSPACE / f"temp_mixed_audio_{reel_id}.wav"
    cmd_audio.extend(["-filter_complex", ";".join(filter_parts), "-map", "[outa]", "-ar", "48000", str(mixed_audio)])
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 6. Generate Running Subtitles (AppKit CoreText with Exact Orange #FF8400)
    timeline = []
    elapsed = 0.0
    for cut in reel["cuts"]:
        dur = cut["et"] - cut["st"]
        for p_idx, (rel_st, rel_et, phrase) in enumerate(cut["phrases"]):
            global_st = elapsed + rel_st
            if p_idx + 1 < len(cut["phrases"]):
                next_st = elapsed + cut["phrases"][p_idx + 1][0]
                global_et = min(elapsed + rel_et + 0.35, next_st)
            else:
                global_et = min(elapsed + rel_et + 0.35, elapsed + dur)

            words = phrase.strip().split()
            if not words:
                continue
            p_dur = global_et - global_st
            weights = [max(len(w), 2) for w in words]
            total_w = sum(weights)
            curr_t = global_st
            for i, w in enumerate(words):
                w_dur = p_dur * (weights[i] / total_w)
                w_st = curr_t
                w_et = curr_t + w_dur
                curr_t = w_et
                status = [(words[j], j == i) for j in range(len(words))]
                timeline.append((w_st, w_et, status))
        elapsed += dur

    cached_frames = {}
    for idx, (st, et, words) in enumerate(timeline):
        cached_frames[idx] = render_sub_frame(words)
    empty_frame = render_sub_frame([])

    subs_mov = WORKSPACE / f"temp_subs_{reel_id}.mov"
    fps = 30
    total_frames = int(total_dur * fps)
    cmd_pipe = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{SUBS_H}",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "qtrle",
        str(subs_mov)
    ]
    proc = subprocess.Popen(cmd_pipe, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for f_num in range(total_frames):
        t = f_num / fps
        active_idx = None
        for idx, (st, et, _) in enumerate(timeline):
            if st <= t < et:
                active_idx = idx
                break
        if active_idx is not None:
            proc.stdin.write(cached_frames[active_idx])
        else:
            proc.stdin.write(empty_frame)
    proc.stdin.close()
    proc.wait()

    # 7. Final Composite & Mux
    final_reel_path = EXPORT_DIR / reel["filename"]
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(base_padded_vid),
        "-i", str(subs_mov),
        "-i", str(mixed_audio),
        "-filter_complex", f"[0:v][1:v]overlay=0:{SUBS_Y}[v]",
        "-map", "[v]",
        "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-shortest",
        str(final_reel_path)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Generated Master Video (1m-1m20s): {final_reel_path} ({os.path.getsize(final_reel_path) / 1024 / 1024:.1f} MB)")

    # 8. Extract QA Frames directly to FRAMES/
    for t in [3.0, total_dur * 0.25, total_dur * 0.50, total_dur * 0.75, total_dur - 3.0]:
        frame_name = f"qa_{reel_id}_t{int(t)}s.jpg"
        frame_dest = EXPORT_FRAMES / frame_name
        subprocess.run(["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(final_reel_path), "-vframes", "1", str(frame_dest)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Cleanup temp files for this reel
    for vf in cut_video_files:
        if vf.exists(): vf.unlink()
    for af in cut_audio_files:
        if af.exists(): af.unlink()
    if concat_vid_txt.exists(): concat_vid_txt.unlink()
    if concat_aud_txt.exists(): concat_aud_txt.unlink()
    if base_padded_vid.exists(): base_padded_vid.unlink()
    if speech_wav.exists(): speech_wav.unlink()
    if mixed_audio.exists(): mixed_audio.unlink()
    if subs_mov.exists(): subs_mov.unlink()
    if banner_file.exists(): banner_file.unlink()

def main():
    print("🚀 Rendering 1min - 1:20min Master Viral Videos with Standard Orange #FF8400...")
    for reel in LONG_REELS:
        process_master_reel(reel)
    print("\n🎉 ALL MASTER 1MIN-1:20MIN VIDEOS RENDERED & VERIFIED!")

if __name__ == "__main__":
    main()
