# Production Style Sheet: Short-Form Video & Social Reels

> **Target Standard**: Instagram Reels, YouTube Shorts, and TikTok (9:16 Vertical Format)  
> **Reference Analysis**: Derived from spectral, frame, and pixel measurements across all reference reels in `STYLE REFERENCE/`. Designed as the definitive production blueprint for every reel edit.

---

## 1. Canvas & Technical Specifications

| Parameter | Specification | Notes |
| :--- | :--- | :--- |
| **Aspect Ratio** | `9:16` (Vertical) | Native mobile short-form standard |
| **Resolution** | `1080 x 1920 px` | Full HD Vertical canvas |
| **Frame Rate** | `30 fps` (or `29.97 fps`) | `50/60 fps` accepted for high-motion b-roll |
| **Video Codec** | `H.264 (AVC)` / `MP4` | High Profile, Level 4.2, YUV420p |
| **Bitrate Target** | `7.0 – 9.0 Mbps` | Optimal balance between quality and mobile streaming |
| **Audio Codec** | `AAC-LC` | 48,000 Hz (or 44,100 Hz), Stereo, 192–320 kbps |
| **Duration Target** | `20s – 59s` | Sweet spot for retention & algorithmic distribution |

### Safe Zones & Margins (1080 x 1920)
- **Top Safe Margin (`0 – 250 px`)**: Reserved for platform search bars, audio icons, and header chrome. No essential faces or titles above $y = 250\text{px}$ unless using the dedicated header banner.
- **Bottom Safe Margin (`1550 – 1920 px`)**: Reserved for profile handles, audio titles, captions, and platform interaction tabs. All burned subtitles must clear $y = 1550\text{px}$.
- **Right Margin Buffer (`120 px`)**: Keep interactive visual elements away from the right edge to avoid clash with like, comment, and share buttons.

---

## 2. Layout & Framing Archetypes

### Archetype 1: Signature Podcast Letterbox (Default for 2-Person Talks / Interviews)
Used in 5 out of 6 reference reels (`Career vs Relationship`, `relationship reel`, `young entrepreneur`). Symmetrical top/bottom letterboxing with a prominent amber-orange header banner.

```
+-------------------------------------------------------+  Y = 0
|                                                       |
|              Top Black Letterbox (416 px)             |
|                                                       |
+-------------------------------------------------------+  Y = 416
|   Header Topic Banner (142 px) — Orange #EA8207       |
|   "Topic Question / Hook Statement"       [Emoji]     |
+-------------------------------------------------------+  Y = 558
|                                                       |
|                                                       |
|              Main Video Window (940 px)               |
|             (1080 x 940 px, Active Frame)             |
|                                                       |
|            [ Hook Subtitle / Captions ]               |  Y ≈ 1080 - 1380
|                                                       |
|                                                       |
+-------------------------------------------------------+  Y = 1498
|                                                       |
|            Bottom Black Letterbox (422 px)            |
|                                                       |
+-------------------------------------------------------+  Y = 1920
```

#### Exact Coordinate Map:
1. **Top Black Bar**: `Y: 0` to `Y: 415` (`416 px` height, fill: `#000000`)
2. **Topic Header Banner**: `Y: 416` to `Y: 557` (`142 px` height, fill: `#EA8207`)
3. **Active Video Window**: `Y: 558` to `Y: 1497` (`940 px` height, width: `1080 px`)
4. **Bottom Black Bar**: `Y: 1498` to `Y: 1919` (`422 px` height, fill: `#000000`)
5. **In-Window B-Roll**: Replaces the active video window (`1080 x 940`) while keeping top/bottom letterboxes and the orange banner intact.

---

### Archetype 2: Full-Bleed Solo Talking Head (Cinematic 9:16)
Used in narrative and high-energy monologue reels (Ref: `3 AM OUT AT UNF`).
- **Canvas**: Full-bleed `1080 x 1920 px`.
- **Opening Visual Shock**: The first `0.5s – 1.0s` opens in **high-contrast Black & White**, snapping instantly to full color on the core hook punchline.
- **Top Dynamic Progress Bar**: An 8px accent line (`#EA8207`) along $y = 0$ that expands continuously across the video duration.
- **Pattern Interrupts**: Cut-synced digital punch-in (`1.15x`) alternating every 2–3 seconds.
- **Lower-Third Captions**: Positioned at $y \approx 1400 - 1500\text{px}$ (comfortably clearing platform UI).

---

## 3. Colour Palette

| Element | Hex Code | RGB | Purpose & Application |
| :--- | :--- | :--- | :--- |
| **Signature Amber Orange** | `#EA8207` | `234, 130, 7` | Header banner background, hook subtitles, active keyword emphasis in subtitles |
| **Solid Black** | `#000000` | `0, 0, 0` | Letterbox bars, banner headline text, 5px subtitle stroke |
| **Pure White** | `#FFFFFF` | `255, 255, 255` | Spoken dialogue subtitles, secondary title text |
| **Dark Backdrop / Card** | `#111111` | `17, 17, 17` | Video window base background |

> [!IMPORTANT]
> **Production Rules (Strict User Preferences)**:
> - **Zero Yellow**: Do not use yellow text in subtitles. Spoken dialogue must be pure `#FFFFFF`, and highlighted keywords must be `#EA8207` (Signature Orange) with 5px solid black outline.
> - **No Top Progress Bar**: Keep the top letterbox clean, solid black (`#000000`). No progress bar strip.
> - **No Floating Pill Cards**: Never overlay floating badges or pills over the speaker's chest. All topic titling lives strictly inside the Y=416-558 orange header banner.
> - **Internet B-Rolls Only**: B-rolls must be authentic stock footage sourced from the internet, never extracted from reference videos.

---

## 4. Typography

### A. Header Topic Banner
- **Font Family**: **Futura Bold / Heavy** (Alternatives: **Montserrat ExtraBold / Black (800/900)**, **Poppins Bold**).
- **Font Size**: `46 px` to `54 px` (1 or 2 lines maximum).
- **Text Color**: `#000000` (Pitch Black).
- **Letter Spacing**: `-0.02em` (tight tracking for punchy impact).
- **Casing**: **Title Case** (e.g. *Career vs Relationship*, *Love na 70 : 30 Formula va?*).
- **Emojis**: 1–2 relevant emoji symbols at the end of the second line (e.g. 🧐, 💔, 🏃, 👀, 👩‍❤️‍👨, 🔥).

### B. Hook Subtitle (0.0s – 3.0s)
- **Font Family**: Same as Header (**Futura Heavy** / **Montserrat Black** / **Noto Sans Tamil Bold**).
- **Font Size**: `64 px` to `76 px` (Large, high-retention hook).
- **Fill Color**: `#EA8207` (Signature Orange) or `#FFE600` (Yellow).
- **Stroke / Outline**: `#000000`, Width: `5 px` to `6 px`.
- **Drop Shadow**: `rgba(0, 0, 0, 0.85)`, `offset: 2px 8px`, `blur: 10px`.
- **Position**: Centered lower-third within the video window (`Y ≈ 1080 – 1180 px` for Archetype 1; `Y ≈ 1400 px` for Archetype 2).

### C. Continuous Dialogue Subtitles
- **Font Family**:
  - **English / Tanglish**: **Futura Medium** / **Montserrat SemiBold** / **Inter Bold**.
  - **Tamil**: **Noto Sans Tamil Bold** / **Mukta Malar Bold** (using HarfBuzz complex conjunct shaping; never raw bitmap).
- **Font Size**: `50 px` to `54 px`.
- **Fill Color**: `#FFFFFF` with active keyword highlighted in `#FFE600` (Yellow) or `#EA8207` (Orange).
- **Stroke / Outline**: `#000000`, Width: `4 px` to `5 px`.
- **Pacing**: `2 to 4 words` per line at a time.
- **Alignment**: Center-aligned horizontally.

---

## 5. Cut Pace & Rhythm

### Quantitative Edit Targets (Derived from Reference Reels)
- **Average Shot Duration**: **`1.7s` to `2.5s`** per shot.
- **Cuts Per Minute**: **`24` to `34` cuts/minute**.
- **Maximum Shot Duration**: Never exceed `3.5s – 4.0s` without an angle switch, scale pop, or b-roll cutaway.
- **Fast Reaction Shots**: `0.8s` to `1.2s` for listener nod, smirk, or reaction.

### Cutting Rules:
1. **Zero Dead-Air**:
   - Detect and cut all silence gaps longer than `0.35s` (using FFmpeg `silencedetect` or Python).
   - Preserve `0.08s` padding on speech boundaries to avoid clipping word transients.
   - Cut obvious retakes, false starts, and filler stumbles.
2. **Audio-Driven Jump Cuts**:
   - Cut synchronously on the speaker's first consonant.
   - J-Cut / L-Cut dialogue overlap by 2–4 frames during speaker exchanges.
3. **Pattern Interrupts (1.15x Face Zoom)**:
   - When staying on the same speaker, alternate between **Normal framing (1.0x)** and **1.15x punch-in zoom** on their face every 2–3 seconds.
   - Sync the zoom transition exactly to phrase boundaries.

---

## 6. Transitions & Motion Design

1. **Straight Hard Cuts (95% of Edits)**:
   - Instantaneous cut on dialogue/action. Avoid dissolve, slide, or wipe transitions on talking-head footage.
2. **Hook Flash / Desaturation**:
   - Opening 0.5s–1.0s in Black & White, snapping to full color on the first punchline.
3. **B-Roll Cutaways**:
   - Insert relevant stock footage, screen recording, or illustration inside the video window (or full-bleed) for 1.5s–3.0s whenever a tangible concept is spoken.
4. **Transition SFX**:
   - Accompany angle switches, punch-ins, and b-roll cuts with subtle whooshes (`whoosh.mp3`) lasting 150–250ms.

---

## 7. Sound & Audio Engineering

### Loudness Targets (EBU R128 Standard)
| Metric | Target Standard | Permitted Tolerance |
| :--- | :--- | :--- |
| **Integrated Loudness** | **`-14.0 LUFS`** | `-13.5` to `-14.5 LUFS` (Platform standard) |
| **True Peak** | **`-1.0 dBFS`** | Max `-1.0 dBFS` (prevents lossy codec inter-sample clipping) |
| **Loudness Range (LRA)** | **`4.5` to `6.5 LU`** | Consistent, compressed vocal presence |

### Audio Mix Hierarchy
1. **Dialogue (Stem 1 — Dominant)**:
   - High-pass filter at `80 Hz`.
   - Gentle presence boost (+2.5 dB) at `3 kHz – 4 kHz` for clarity on phone speakers.
   - Mastered to -14.0 LUFS.
2. **Background Music (Stem 2 — Ambient Bed)**:
   - Genre: Lo-fi hip-hop, ambient chill, low-tempo groove.
   - Level: Ducked to **`-20 dB to -24 dB`** under speech.
   - Fade-in (0.8s) and smooth fade-out (1.5s) at end.
3. **Sound Effects (Stem 3 — Accents)**:
   - Whoosh / Swish on camera cuts & scale pops.
   - Pop / Wood-click on key text / emoji pop-ins.
   - Peaking at `-8 dBFS to -10 dBFS`.

---

## 8. Master Checklist for Every Edit

- [ ] **Geometry**: 1080x1920, 30fps, H.264 MP4.
- [ ] **Framing Archetype Selected**:
  - Archetype 1: Letterbox (416px top bar, 142px orange banner, 940px video, 422px bottom bar).
  - Archetype 2: Full-bleed vertical with 8px top progress bar.
- [ ] **Hook Setup (0–3s)**:
  - Header banner question set with emoji.
  - Bold hook subtitle in orange/yellow with 5px black stroke.
  - 1.15x punch-in or 0.6s B&W flash active.
- [ ] **Pacing**:
  - Silences $> 0.35\text{s}$ removed (0.08s padding).
  - Average cut duration `1.7s – 2.5s` (24–34 cuts/min).
  - Alternating 1.15x zoom punch-in every 2–3s.
- [ ] **Captions**:
  - 2–4 words per line, centered lower-third.
  - Noto Sans Tamil Bold (Tamil) / Futura or Montserrat (English).
  - White text, 5px black stroke, key words in yellow (`#FFE600`).
- [ ] **Audio Finalization**:
  - Normalized to **`-14.0 LUFS`** (True Peak `-1.0 dBFS`).
  - Background music ducked to **`-20 dB`**.
  - Transition whooshes on cuts.
