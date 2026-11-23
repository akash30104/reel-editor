# Project Rules & Master Guidelines (`rules.md`)

> **Master Video Editor**: Standardized execution protocol applying across all 4 reference styles.  
> **Core Principle**: Identical video structure, pacing, audio engineering, and validation rules; only visual style parameters (title look, subtitle font/fill/size/position) vary per reference template.

---

## 1. Project Rules (Non-Negotiable)

1. **Never Modify a Template File**: `templates/template_ref*.json` files are immutable style blueprints. The AI only decides content (hook selection, cut points, silence removal, b-roll choices, subtitle text, title text) and saves them in `edit_plan.json`.
2. **Always Use `render.py`**: All final videos must be rendered through the single deterministic rendering script. Same input + same template = bit-exact identical output every time.
3. **Never Edit Layout Manually**: All layout coordinates, fonts, and dimensions belong strictly inside the reference template file.
4. **Always Run `validate.py` Before Delivering**: Every video must pass all validation checks. If any check fails, fix `edit_plan.json` or re-render until 100% compliant.
5. **Mandatory Mild Background Music for ALL Videos**: Every single video without exception must have mild, subtle background music mixed beneath the dialogue (`-22 dB` to `-25 dB`). No raw dialogue-only video is ever permitted.
6. **Zero Watermarks**: Strictly no logos, watermarks, or initials in the top-right corner or anywhere on the frame. The video canvas must be 100% clean and distraction-free.

---

## 2. Video Structure (Fixed for All References)

Every video across all reference styles must follow this exact sequential order:
1. **HOOK**: Find the strongest, highest-energy hook statement in the raw video, cut it out, and place it at the very start ($t = 0.0\text{s}$).
2. **TITLE**: Show the reference-styled title for the full duration of the video.
3. **MAIN CONTENT**: The remaining speech in natural chronological order. Do NOT repeat the hook clip.
4. **END**: Clean ending on a decisive statement. No artificial intro or outro unless explicitly supplied.

---

## 3. Duration Standards

- **Strict Target Window**: Between **`1:20` and `1:40` minutes** (`80.0` to `100.0` seconds).
- **Trimming Protocol**: If raw speech exceeds 100s, remove silence gaps ($> 0.35\text{s}$), filler words, and repeated points. Retain only the highest-value content.
- **Duration Enforcement**: If rendered video falls outside `80.0s – 100.0s`, `validate.py` will reject it, requiring re-planning and re-rendering before delivery.

---

## 4. Title Rules

- **Language**: English only.
- **Line Count**: **Single line only**. Never wrap to two lines.
- **Weight**: Bold font.
- **Reference Inheritance**: Title font family, color, background box, and position are copied directly from that reference's title image.
- **Dynamic Fit**: If text length approaches the safe border, shrink font size smoothly to guarantee it remains on a single line.

---

## 5. Subtitle Rules

- **Language**: Same language as speech (Tamil).
- **Reference Inheritance**: Subtitle font family, fill color, font size, and screen position must be measured and copied directly from the reference video/images.
- **Stroke**: Solid black stroke (`#000000`) on every word.
- **Word-by-Word Progressive Reveal**:
  - Words appear one by one, synchronized with Whisper word-level timestamps.
  - Each word appears at its spoken timestamp and **stays on screen until the phrase/sentence ends**.
  - Future words must **never** be shown before they are spoken.
  - All words use the reference's measured subtitle fill color.
- **Sync Requirement**: Subtitle timing must be tightly bound to the audio waveform with zero drift.

---

## 6. B-Roll & Photo Rules

- **Supported Formats**: Video clips (`.mp4`) OR static photos (`.jpg`, `.png`).
- **Directories**:
  - Video clips: `/assets/broll_library/`
  - Photos: `/assets/broll_photos/`
- **Overlay Execution**:
  - B-roll is an overlay inside the video window only.
  - The speaker's audio track and subtitles must **continue without any break or gap** while b-roll plays.
  - B-roll must **never cover the title banner or subtitles**.
- **Keyword Matching**:
  - B-roll clips and photos are chosen strictly by matching context keywords in the transcript.
  - Photos fill the video window and transition when the topic changes.
  - **No Random Clips**: If no contextually matching clip or photo exists in the library, keep the speaker on screen. Never insert irrelevant media.

---

## 7. Camera & Motion Design

- **No Hook Zoom**: Do not add artificial hook zoom punch-ins or unreferenced effects.
- **Reference Fidelity**: Add zero animations, transitions, or effects that are not explicitly present in the reference style.

---

## 8. Audio Mastering Standards

- **Dialogue (Primary)**: Speaker voice is the dominant track. Background noise removed, vocal clarity preserved, normalized to **`-14.0 LUFS`** (EBU R128 standard).
- **Mild Background Music (Mandatory for ALL Videos)**: Every single video across all reference styles must have continuous mild background music (instrumental, flute, strings, or lo-fi bed) ducked to **`-22 dB to -25 dB`** under speech with smooth head (1.0s) and tail (2.0s) fades. Zero videos may be delivered with dead air or vocal-only silence.
- **Continuity**: Continuous audio bed without abrupt jumps or gaps during visual cutaways.

---

## 9. Automated Validation Suite (`validate.py`)

Before any reel is marked ready, `validate.py` automatically asserts:
1. **Duration**: $80.0\text{s} \le \text{Duration} \le 100.0\text{s}$.
2. **Title Line Count**: Exactly single line (no `\n`, text bbox within margin).
3. **Subtitle Specifications**:
   - Subtitle font family matches the template.
   - Subtitle fill color matches the template.
   - Subtitle font size matches the template.
   - Solid black stroke is present on all words.
   - Word-by-word progressive reveal verified (timing offsets strictly sequential).
4. **Audio Integrity**:
   - Zero audio gaps/silences during b-roll video or photo overlays.
   - Background music is present and verified active across the entire video.
   - Background music loudness is between $-25\text{ dB}$ and $-20\text{ dB}$.
   - Voice loudness is $-14.0 \pm 0.5\text{ LUFS}$.
5. **Sync Tolerance**: Audio-subtitle alignment drift $< 100\text{ms}$.
6. **Watermark Enforcement**: Zero watermarks or corner initials present.

---

## 10. Reference 3 Master Specification (Minimalist Motivational Kinetic Short) [LOCKED MASTER STANDARD]

> [!IMPORTANT]
> **PERMANENTLY LOCKED MASTER STANDARD**: Reference 3 style is officially locked. Whenever instructed to edit a raw video in **Reference 3** (`refeance 3` / `Reference 3 Style`), the editor must strictly execute the following parameters defined in `templates/template_ref3.json` and demonstrated in `render_ref3_kinetic.py`. No deviations in layout, color, audio standards, or subtitle motion are permitted.

### 1. Canvas & Camera
- **Canvas**: Pure black (`#000000`) 9:16 vertical canvas (`1080×1920 @ 30fps`).
- **Framing & Aspect Ratio**: Center the 16:9 clip in the middle third ($Y = 656 \text{ to } 1264$, height $608\text{px}$, width $1080\text{px}$) letterbox style. This exact frame size must be preserved.
- **Active Speaker Tracking**: The frame must dynamically switch to **whoever is actually talking**. Never show a listening speaker while another person is speaking:
  - When the Host speaks ($0.0\text{s} - 8.6\text{s}$), crop and center the Host camera.
  - When the Guest speaks ($8.6\text{s} - 74.0\text{s}$), crop and center the Guest camera.
  - Cut cleanly on the natural speech pause ($t = 8.6\text{s}$) to preserve absolute speech-to-face synchronization.
- **Gradient Fade**: Soft black gradient fade on the bottom edge of the video frame ($Y = 1174 \text{ to } 1264$, $90\text{px}$ fade height) dissolving the speaker's torso cleanly into the pure black lower canvas.
- **Motion Protocol**: Static shot only. Absolutely **no jump cuts, zooms, punch-ins, or B-roll**.

### 2. Color & Audio
- **Cinematic Color Grade**: Warm, slightly desaturated cinematic grade with deep rich blacks (`eq=contrast=1.12:saturation=0.85:brightness=-0.02,colorbalance=rs=0.04:gs=0.02:bs=-0.04`).
- **Audio Master & Mandatory Mild Music**: Clean, crisp dialogue normalized to broadcast standard **`-14.0 LUFS`** / **`-1.0 dBTP`**. **Mild background music is strictly mandatory** across the entire video: continuous emotional instrumental flute/strings background music bed (`ramayan_flute_bgm.mp3`) mixed at **`-22 dB to -24 dB`** under speech with smooth 1.0s head fade and 2.0s tail fade. Strictly **no whooshes, risers, or pop sound effects**.
- **Watermark**: **REMOVED / DISABLED**. Strictly **no watermark** in the top-right corner or anywhere on the frame. Clean, distraction-free aesthetic.

### 3. Subtitle Style & Exact Placement [REFERENCE 3 LOCKED STANDARD]
- **Language**: **TANGLISH (Romanized Tamil + English keywords matching spoken audio)**. Modeled directly on Reference 3 (`referance/referance 3/vidssave.com kisthenics podcast... 720P.mp4`):
  - Spoken Tamil is transcribed phonetically in Roman script (e.g. `VANAKKAM GANESH...!`, `FINE BRO...!`, `ORU QUICK CRISP INTRO...`, `COLLEGE STUDENT...!`, `START FROM SCRATCH!`, `ZERO KNOWLEDGE..!`, `PRIVATE LIMITED COMPANY!`, etc.).
  - Emotive punctuation (`...!`, `..`, `!`, `?`) gives the typography authentic kinetic energy.
- **Font & Fill**: **Impact** (`/System/Library/Fonts/Supplemental/Impact.ttf`, size 64pt), **Pure White (`#FFFFFF`)** with crisp **`3.5px solid black outline` (`#000000`)** and multi-layer soft dark drop shadow (`rgba(0, 0, 0, 0.85)` offset `4px, 4px`, blur `6px`).
- **Safe Zone & Face Protection Guarantee**:
  - **NEVER COVER THE SPEAKER'S FACE, EYES, NOSE, OR MOUTH**.
  - All subtitles are strictly anchored at the **lower chest / torso** ($Y \approx 1130$ on 1080x1920 canvas, local $Y \approx 474$ inside the 608px video window).
  - Since the speaker's face is positioned at $Y = 750 \text{ to } 950$, placing subtitles at $Y \approx 1130$ guarantees over 180px of clear headroom, completely clear of the face.
- **Pacing**: Rapid **1 to 3 words per burst** (`0.8s to 1.5s` per burst). Exactly ONE burst is displayed on screen at any single moment. When the next burst triggers, the previous burst vanishes cleanly.

---

## 11. Reference 4 Master Specification (Split-Screen Kinetic Highlight Banner Short) [LOCKED MASTER STANDARD]

> [!IMPORTANT]
> **PERMANENTLY LOCKED MASTER STANDARD**: Reference 4 style is officially locked. Whenever instructed to edit a raw video in **Reference 4** (`refeance 4` / `Reference 4 Style`), the editor must strictly execute the following parameters defined in `templates/template_ref4.json` and demonstrated in `render_ref4_final.py`. No deviations in framing, B-roll pacing, subtitle banner design, or audio balance are permitted.

### 1. Framing & B-Roll
- **Main Layout (50/50 Vertical Split-Screen)**:
  - Exact 50/50 vertical split-screen on a `1080×1920 @ 30fps` canvas.
  - **Cinematic Medium Close-Up (MCU) Framing**: Both speakers fill their respective halves with tight, intimate framing (head near top, shoulders/chest filling the frame, no excessive empty wall space):
    - **Host (Woman) Top Half**: Crop `1012×900` from $(2094, 680)$, scaled to `1080×960` occupying $Y = 0 \text{ to } 960$.
    - **Guest (Man) Bottom Half**: Crop `1012×900` from $(494, 830)$, scaled to `1080×960` occupying $Y = 960 \text{ to } 1920$.
    - **Center Seam**: Clean 2px dark seam separating the two halves at $Y = 960$.
  - **Color Grade**: Warm natural studio grade (`eq=contrast=1.08:saturation=0.92:brightness=-0.01,colorbalance=rs=0.03:gs=0.01:bs=-0.03`).
- **Cinematic B-Roll Cutaways**:
  - Every **3–6 seconds**, cut to relevant topic footage or movie clips.
  - Centered on a pure black 9:16 canvas (`1080×1920`) in **letterbox style** (`16:9` aspect ratio, `1080×608` centered at $Y = 656$).
  - Smooth transitions alternating between split-screen dialogue and visual cutaways.

### 2. Subtitle Banner & Exact Speech Synchronization
- **Trigger Rule**: **Do NOT subtitle every word**. Display kinetic callout banners **ONLY** on key hooks, dates, percentages, and core takeaways.
- **Anchor Position & Expanded Scale**: Full-width, semi-transparent dark horizontal strip (`rgba(10, 10, 10, 0.88)`) anchored across the **exact center seam** ($Y = 960$) between the two speakers ($Y = 780 \text{ to } 1140$, total height $360\text{px}$).
- **Framing Borders**: Crisp white horizontal top and bottom border lines (`3px`, `#FFFFFF`) framing the strip cleanly at $Y = 780$ and $Y = 1140$.
- **Enlarged High-Impact Typography**:
  - **Supporting Words / Numbers**: Extra large white bold-italic sans-serif (`Arial Bold Italic`, size **`56px`**, `#FFFFFF`) positioned neatly at $Y = 815$.
  - **Focal Keyword**: Massive golden-yellow stylized Tamil font (`Tamil Sangam MN`, size **`115px`**, `#FFD700`) centered inside the strip at $Y = 915$ with a soft dark drop shadow (5px offset) and solid 4px dark stroke outline (`#000000`), rendered via HarfBuzz COMPLEX text shaping (`libass`) for authentic Tamil ligature accuracy.
- **Exact Acoustic Speech Synchronization**:
  - Banner cues must strictly match the acoustic speech onsets measured from the dialogue track (`precise_words.json`).
  - Text must never appear before a speaker starts talking (e.g., Host begins speaking at `3.5s`, not at `0.8s`).
  - Banners hold through the spoken thought and cut cleanly out when the phrase concludes.

### 3. Audio & Outro
- **Audio Master & Mandatory Mild Music**:
  - Crisp, prominent dialogue normalized to broadcast standard **`-14.0 LUFS`** / **`-1.0 dBTP`**.
  - **Mandatory mild background music**: Soft emotional instrumental flute/strings background music bed (`ramayan_flute_bgm.mp3`) mixed at **`-23 dB`** under speech with smooth head and tail fades.
  - Strictly no whooshes, risers, or pop sound effects.
  - **Zero Watermarks**: No watermark in top-right corner or anywhere on the frame.
- **Outro Rule (NO Subscribe Card)**:
  - **Subscribe card is completely removed**.
  - Dialogue and split-screen interaction play naturally through to the decisive spoken climax and natural conclusion ($t = 74.0\text{s}$).

## 12. Reference 11 Master Specification (Single-Word Highlight Banner Short) [LOCKED MASTER STANDARD]

> [!IMPORTANT]
> **PERMANENTLY LOCKED MASTER STANDARD**: Reference 11 style is officially locked. Whenever instructed to edit a raw video in **Reference 11** (`reference 11` / `11referance`), the editor must strictly execute the parameters defined in `templates/template_ref11.json` and executed in `render_ref11_master.py`.

### 1. Canvas & Header Banner
- **Canvas**: Exact 9:16 vertical canvas (`1080×1920 @ 30fps`).
- **Top Black Bar**: Pure black canvas from $Y = 0 \text{ to } 408$.
- **Persistent Header Banner**:
  - **Position**: Anchored across $Y = 408 \text{ to } 558$ (height $150\text{px}$).
  - **Background**: Exact signature orange **`#FF8400`** (`RGB: 255, 132, 0`).
  - **Framing Borders**: 3px solid black border lines top ($Y = 408$) and bottom ($Y = 558$).
  - **Typography & Layout**: **Single-line title centered horizontally and vertically** inside the orange banner. Rendered via native Cocoa/AppKit (`TamilSangamMN-Bold`, size 46px, `#000000` solid black) with full color Apple Color Emojis:
    - Title: `ராமாயணம் கற்றுத்தரும் பாடம் 🏹` (perfect center alignment at $X \approx 210.5, Y \approx 44.5$)

### 2. Active Video Window & Speaker Framing
- **Dimensions & Placement**: $1080\times 940\text{px}$ window centered across $Y = 558 \text{ to } 1498$.
- **Bottom Black Bar**: Pure black canvas from $Y = 1498 \text{ to } 1920$.
- **Dynamic Speaker Switching**:
  - **Host (Woman) Framing**: When Host speaks, cut to Host Woman Medium Close-Up centered in the $1080\times 940$ frame (`crop=1206:1050:2150:650,scale=1080:940`).
  - **Guest (Man) Framing**: When Guest speaks, cut to Guest Man Medium Close-Up centered in the $1080\times 940$ frame (`crop=1206:1050:450:750,scale=1080:940`).
  - **Climax Punch-in**: Subtle 1.15x punch-in on high-energy vocal peaks (`crop=1048:913:530:820,scale=1080:940`).
- **Pacing & B-Roll Cutaways**:
  - Visual cutaways every **4 to 7 seconds** alternating between speaker close-ups and thematic B-roll footage.
  - First 0.6s begins in B&W snapping into warm natural studio color grade (`eq=contrast=1.08:saturation=0.92:brightness=-0.01,colorbalance=rs=0.03:gs=0.01:bs=-0.03`).

### 3. Subtitle Pacing & Speech Synchronization
- **Pacing**: **Fast single word / single punchy phrase at a time** (`ONLY ONE WORD AT A TIME` on screen).
- **Typography**: User's signature handwriting font **`MyHandwriting.ttf`** (slightly decreased to size **`76pt`** for optimal screen balance).
- **Color & Stroke**: Exact signature orange **`#FF8400`** with crisp **`7px solid black stroke outline`** (`#000000`).
- **Position**: Centered horizontally at lower third of the video window ($Y = 1340$).
- **Exact Speech Sync**: Subtitles strictly align with acoustic speech onsets measured in `precise_words.json`. Words hold through their spoken duration and cut out cleanly.

### 4. Audio Mastering
- **Dialogue Target**: Normalized to broadcast standard **`-14.0 LUFS`** / **`-1.0 dBTP`**.
- **Mandatory Mild Music**: Continuous emotional instrumental flute BGM (`ramayan_flute_bgm.mp3`) ducked to **`-23 dB`** under speech with smooth head/tail fades.
- **Zero Watermarks**: No watermark in top-right corner or anywhere on the frame.


