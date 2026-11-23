#!/usr/bin/env python3
"""
render.py
Master Deterministic Rendering Engine for Video Reels.
Loads the reference template and edit plan, builds active speaker framing,
generates kinetic typography, balances broadcast audio, and renders bit-exact reels.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "EXPORT"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = EXPORT_DIR / "FRAMES"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = BASE_DIR / "temp_ref3_render"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
VID_W = 1080
VID_H = 608
VID_Y = 656

SPACES = {
    "L_MID": {"x": 220, "y": 810, "max_w": 340, "align": "center"},
    "R_MID": {"x": 860, "y": 810, "max_w": 340, "align": "center"},
    "B_CTR": {"x": 540, "y": 1140, "max_w": 920, "align": "center"},
    "L_TOP": {"x": 220, "y": 740, "max_w": 340, "align": "center"},
    "R_TOP": {"x": 860, "y": 740, "max_w": 340, "align": "center"},
    "L_LOW": {"x": 250, "y": 1050, "max_w": 380, "align": "center"},
    "R_LOW": {"x": 830, "y": 1050, "max_w": 380, "align": "center"},
}

def parse_args():
    parser = argparse.ArgumentParser(description="Master Deterministic Reel Renderer")
    parser.add_argument("--plan", default=str(BASE_DIR / "edit_plan.json"), help="Path to edit_plan.json")
    parser.add_argument("--template", default=None, help="Path to reference template JSON")
    return parser.parse_args()

def load_config(plan_path, template_path_arg):
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
    
    tpl_path = Path(template_path_arg) if template_path_arg else (BASE_DIR / plan.get("template_file", "templates/template_ref3.json"))
    with open(tpl_path, "r", encoding="utf-8") as f:
        template = json.load(f)
        
    return plan, template

def build_gradient_overlay(out_png):
    if out_png.exists():
        return
    print("🎨 Creating bottom gradient fade overlay...")
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0, VID_Y), (WIDTH, VID_Y + VID_H - 90)], fill=(0, 0, 0, 0))
    fade_start = VID_Y + VID_H - 90
    fade_end = VID_Y + VID_H
    for y in range(fade_start, fade_end):
        alpha = int(255 * ((y - fade_start) / 90.0))
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))
    im.save(out_png)
    print(f"✅ Bottom gradient fade overlay saved: {out_png}")

def get_fitted_font_and_text(font_path, text, space_key, is_hero):
    s = SPACES[space_key]
    max_w = s["max_w"]
    base_sz = 68 if "CTR" in space_key else (58 if is_hero else 50)

    words = text.split()
    if len(words) > 2 and "CTR" not in space_key and "\n" not in text:
        mid = len(words) // 2
        text = " ".join(words[:mid]) + "\n" + " ".join(words[mid:])

    dummy_img = Image.new("RGBA", (10, 10))
    draw = ImageDraw.Draw(dummy_img)

    sz = base_sz
    while sz >= 32:
        f = ImageFont.truetype(str(font_path), sz)
        bbox = draw.multiline_textbbox((0, 0), text, font=f, align="center")
        w = bbox[2] - bbox[0]
        if w <= max_w:
            return f, text
        sz -= 2
    return ImageFont.truetype(str(font_path), 32), text

def render_kinetic_frame(font_path, burst_tuple):
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    if not burst_tuple:
        return im.tobytes()

    space_key, text, is_hero = burst_tuple
    s = SPACES[space_key]
    draw = ImageDraw.Draw(im)

    f, fitted_text = get_fitted_font_and_text(font_path, text, space_key, is_hero)

    bbox = draw.multiline_textbbox((0, 0), fitted_text, font=f, align="center")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    draw_x = s["x"] - text_w // 2
    draw_y = s["y"] - text_h // 2

    # Multi-layer soft dark drop shadow
    for ox, oy, alpha in [(6, 6, 220), (4, 4, 180), (2, 2, 140)]:
        draw.multiline_text((draw_x + ox, draw_y + oy), fitted_text, font=f, fill=(0, 0, 0, alpha), align="center")

    # Electric Yellow (#FFE500) with 3.5px solid dark stroke
    draw.multiline_text(
        (draw_x, draw_y), fitted_text, font=f,
        fill=(255, 229, 0, 255),
        stroke_width=3,
        stroke_fill=(0, 0, 0, 240),
        align="center"
    )
    return im.tobytes()

def render_subtitles_mov(font_path, bursts, total_duration, out_mov):
    print("🎬 Generating dynamic random-space kinetic subtitles MOV...")
    proc = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{HEIGHT}",
        "-framerate", "30", "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(out_mov)
    ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_frames = int(round(total_duration * 30))
    blank_bytes = render_kinetic_frame(font_path, None)

    for f_idx in range(total_frames):
        t_sec = f_idx / 30.0
        active = None
        for b in bursts:
            st = b["start"]
            et = b["end"]
            if st <= t_sec < et:
                active = (b["space"], b["text"], b["hero"])
                break
        raw_b = render_kinetic_frame(font_path, active) if active else blank_bytes
        proc.stdin.write(raw_b)

    proc.stdin.close()
    proc.wait()
    print(f"✅ Dynamic kinetic subtitles saved: {out_mov}")

def main():
    args = parse_args()
    plan, template = load_config(args.plan, args.template)

    raw_video_path = BASE_DIR / plan["raw_video"]
    if not raw_video_path.exists():
        print(f"❌ Error: Raw video not found at: {raw_video_path}")
        sys.exit(1)

    total_duration = plan["total_duration"]
    cuts = plan["cuts"]
    bursts = plan["kinetic_bursts"]
    font_path = BASE_DIR / template["subtitles"]["font_path"]
    bgm_path = BASE_DIR / template["audio_mastering"]["bgm_track"]
    output_mp4 = BASE_DIR / plan["output_video"]
    output_mp4.parent.mkdir(parents=True, exist_ok=True)

    print(f"🎬 Starting render for '{plan['project']}' using '{template['name']}'...")
    print(f"   Raw Video: {raw_video_path}")
    print(f"   Target Duration: {total_duration:.2f}s")
    print(f"   Output: {output_mp4}")

    # 1. Render Video Chunks & Audio Chunks
    video_chunk_files = []
    audio_chunk_files = []
    color_eq = template["color_grade"]["ffmpeg_eq_filter"]

    for c in cuts:
        cid = c["id"]
        raw_ss = c["raw_start"]
        raw_dur = c["duration"]
        crop_vf = c["crop"]
        vf = f"{crop_vf},{color_eq},setsar=1,fps=30"

        v_chunk = TEMP_DIR / f"chunk_{cid:02d}.mp4"
        a_chunk = TEMP_DIR / f"audio_{cid:02d}.wav"
        video_chunk_files.append(v_chunk)
        audio_chunk_files.append(a_chunk)

        if not v_chunk.exists() or v_chunk.stat().st_size < 10000:
            print(f"   Extracting Video Chunk {cid:02d} ({c['speaker']}, {raw_dur:.2f}s)...")
            cmd_v = [
                "ffmpeg", "-y", "-ss", str(raw_ss), "-t", str(raw_dur),
                "-i", str(raw_video_path), "-vf", vf, "-an",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                str(v_chunk)
            ]
            subprocess.run(cmd_v, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        if not a_chunk.exists() or a_chunk.stat().st_size < 1000:
            cmd_a = [
                "ffmpeg", "-y", "-ss", str(raw_ss), "-t", str(raw_dur),
                "-i", str(raw_video_path), "-vn",
                "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
                str(a_chunk)
            ]
            subprocess.run(cmd_a, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 2. Concat Video Base
    base_cut_mp4 = TEMP_DIR / "ref3_speakers_base.mp4"
    concat_v_txt = TEMP_DIR / "video_concat.txt"
    with open(concat_v_txt, "w", encoding="utf-8") as f:
        for vf in video_chunk_files:
            f.write(f"file '{vf.resolve().as_posix()}'\n")

    print("🎬 Concatenating active speaker video track...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_v_txt),
        "-c", "copy", str(base_cut_mp4)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 3. Concat & Master Dialogue Audio
    dialogue_concat_wav = TEMP_DIR / "dialogue_concat.wav"
    concat_a_txt = TEMP_DIR / "audio_concat.txt"
    with open(concat_a_txt, "w", encoding="utf-8") as f:
        for af in audio_chunk_files:
            f.write(f"file '{af.resolve().as_posix()}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_a_txt),
        "-c:a", "pcm_s16le", str(dialogue_concat_wav)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    dialogue_master_wav = TEMP_DIR / "dialogue_master.wav"
    print("🎙️ Normalizing dialogue track to -14.0 LUFS broadcast standard...")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(dialogue_concat_wav),
        "-af", "loudnorm=I=-14.0:TP=-1.0:LRA=7",
        "-c:a", "pcm_s16le", str(dialogue_master_wav)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 4. Bottom Gradient Overlay
    grad_overlay_png = TEMP_DIR / "ref3_gradient_overlay.png"
    build_gradient_overlay(grad_overlay_png)

    # 5. Dynamic Kinetic Subtitles MOV
    subs_mov = TEMP_DIR / "ref3_kinetic_subs.mov"
    render_subtitles_mov(font_path, bursts, total_duration, subs_mov)

    # 6. Final Master Assembly
    print(f"🚀 Assembling final reel into {output_mp4}...")
    filter_complex = (
        f"[0:v]pad={WIDTH}:{HEIGHT}:0:{VID_Y}:color=black,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[base];"
        f"[base][1:v]overlay=0:0[v_grad];"
        f"[v_grad][2:v]overlay=0:0[v];"
        f"[4:a]volume=0.06,afade=t=in:ss=0:d=1.0,afade=t=out:st={total_duration-2.5:.2f}:d=2.5[bgm];"
        f"[3:a][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[a]"
    )

    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(base_cut_mp4),
        "-i", str(grad_overlay_png),
        "-i", str(subs_mov),
        "-i", str(dialogue_master_wav),
        "-i", str(bgm_path),
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
        "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-shortest",
        "-movflags", "+faststart",
        str(output_mp4)
    ]
    subprocess.run(cmd_final, check=True)
    print(f"🎉 FINAL REEL SUCCESSFULLY EXPORTED TO: {output_mp4}")

    # 7. Extract QA Verification Frames
    print("📸 Extracting QA Verification Frames across key kinetic moments...")
    qa_times = [1.2, 2.5, 4.8, 8.2, 13.5, 19.5, 24.5, 31.0, 37.5, 41.5, 52.0, 58.0]
    for qt in qa_times:
        qa_frame = FRAMES_DIR / f"qa_ref3_t{qt:.1f}s.png"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(qt), "-i", str(output_mp4),
            "-vframes", "1", str(qa_frame)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ QA verification frames extracted!")

if __name__ == "__main__":
    main()
