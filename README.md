# 🎬 Viral Reel Editor (Automated 9:16 Video Engine)

An automated video editing pipeline engineered to turn raw podcast / interview footage into viral **9:16 Instagram Reels / YouTube Shorts** adhering strictly to signature broadcast standards.

---

## ✨ Features & Design Rules

1. **Persistent Two-Line Header Banner (`#EA8207`)**:
   - 1080x150 px banner locked at `y = 408`.
   - **Line 1**: Main Topic Title + Twemoji (`🔥`, `💡`, `💔`, `🎯`).
   - **Line 2**: Hook Question / Mission Subtitle.
   - Guaranteed **100% persistent loop** across every second and cut of the video.
2. **Zero-Yellow Subtitles**:
   - Spoken dialogue in crisp pure white (`#FFFFFF`).
   - Keyword highlights in signature orange (`#EA8207`).
   - Solid 5px black stroke (`#000000`).
   - Rendered using bundled Unicode Tamil & English fonts (`Noto Sans Tamil Bold`, `Mukta Malar Bold`).
3. **Smart Camera Framing & Cuts**:
   - Auto-crops 1080x940 active window for 2-speaker podcast setups (Guest on Left, Host on Right).
   - Dynamic 1.15x punch-in zoom for impactful statements.
   - 0.6s black-and-white flash to color on opening hook.
4. **100% Outside B-Roll Integration**:
   - Bundled library of cinematic stock B-rolls (graduates, job contracts, error glitch warnings, struggle & resolve, skyscraper sunrise victory).
5. **Mastered Audio**:
   - Blended with royalty-free lo-fi background music ducked at `-20 dB` under speech.
   - Broadcast-standard EBU R128 loudness normalization to `-14.0 LUFS` (`TP = -1.5 dB`).
6. **Clean Letterboxing**:
   - Clean solid black top and bottom letterbox.
   - No floating pill badges, no distracting progress bars.

---

## 🚀 Setup on ANY New Laptop (Windows / macOS / Linux)

### 1. Prerequisites
- **Python 3.10+**
- **FFmpeg**:
  - **Windows**: `winget install Gyan.FFmpeg` or download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (ensure `ffmpeg` is in your PATH).
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg`

### 2. Clone the Repository
```bash
git clone https://github.com/akash30104/reel-editor.git
cd reel-editor
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚡ How to Edit Reels

You **do not need to recreate any reference styles**! Just drop your raw video and run:

### Simple One-Click Run:
Drop your `.mov` or `.mp4` into `RAW_VIDEOS/`, then run:
```bash
python edit_reel.py
```

### Custom Title & Subtitle:
```bash
python edit_reel.py --input "RAW_VIDEOS/my_video.mov" \
                    --title "Career vs Relationship" \
                    --subtitle "எது முக்கியம்?" \
                    --emoji1 "broken_heart.png" \
                    --emoji2 "fire.png"
```

The exported video and verification QA frames will be saved in `EXPORT/`.

---

## 📁 Repository Structure

```
reel-editor/
├── edit_reel.py             # Main one-click CLI editor
├── core/
│   ├── config.py            # Resolution, colors, fonts, margins
│   ├── banner.py            # Two-line header banner with Twemojis
│   ├── subtitle_generator.py# Zero-yellow ASS subtitle generator
│   ├── camera_director.py   # Speaker crop, 1.15x zoom, hook transitions
│   ├── audio_master.py      # EBU R128 (-14 LUFS) & ducked BGM
│   ├── compositor.py        # 9:16 vertical canvas & looping banner
│   └── transcriber.py       # Whisper speech-to-text integration
├── assets/
│   ├── fonts/               # Noto Sans Tamil & Mukta Malar bold fonts
│   ├── emojis/              # Twemoji icons (fire, target, heart, bulb, etc.)
│   ├── audio/               # Ducked BGM loop & whoosh SFX
│   └── brolls/              # Stock footage library (graduates, contracts, glitch, etc.)
├── RAW_VIDEOS/              # Local folder for input raw videos
├── EXPORT/                  # Final exported 9:16 reels
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🔒 Reference 3 Master Standard (Minimalist Motivational Kinetic Short)
Permanently locked in `templates/template_ref3.json` and `rules.md` (Section 10):
- **Canvas**: Pure black 9:16 vertical canvas (`1080x1920 @ 30fps`).
- **Framing**: Middle third 16:9 letterbox (`1080x608`, $Y=656..1264$) with 90px soft black bottom gradient fade.
- **Active Speaker Tracking**: Automatically cuts between Host and Guest on active speech.
- **Subtitles**: Dynamic random-space kinetic subtitles (`L_MID`, `R_MID`, `B_CTR`, `L_TOP`, `R_TOP`, `L_LOW`, `R_LOW`), strictly 1 fast burst at a time (`0.8s - 1.6s`), Electric Yellow (`#FFE500`) Anton bold condensed font, 3.5px black stroke, and `-50ms` acoustic visual lead sync.
- **Audio**: Broadcast dialogue at `-14.0 LUFS` with continuous mild instrumental BGM ducked at `-23 dB`. Zero watermarks.

To render in Reference 3:
```bash
python render_ref3_kinetic.py
```

---

## 🔒 Reference 11 Master Standard (Single-Word Highlight Banner Short)
Permanently locked in `templates/template_ref11.json` and `rules.md` (Section 12):
- **Canvas**: Exact 9:16 vertical canvas (`1080x1920 @ 30fps`) with strict SDR BT.709 color pipeline (`-pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709`).
- **Top Black Bar**: $Y = 0 \text{ to } 408$.
- **Header Banner**: 1080x150 px banner anchored at $Y = 408..558$ with 3px black borders, signature orange background (`#FF8400`), and centered English bold title ("Lessons from Ramayana 🏹").
- **Active Video Window**: Centered 1080x940 window at $Y = 558..1498$ with 100% continuous acoustic lip-sync (`raw_ss = 1988.0 + T`), active speaker switching (Host Woman / Guest Man), 1.15x climax punch-ins, and B-roll cutaways every 4-7 seconds.
- **Subtitles**: Spoken Tanglish single-word/phrase bursts rendered in `MyHandwriting.ttf` (size 82pt) in signature orange (`#FF8400`) with 7px black outline and drop shadow at $Y = 1340$, speech-locked to Whisper acoustic timestamps.
- **Audio**: Clean dialogue at `-14.0 LUFS` (`-1.0 dBTP`) with soft instrumental flute BGM ducked at `-23 dB`.

To render in Reference 11:
```bash
python render_ref11_master.py
```
