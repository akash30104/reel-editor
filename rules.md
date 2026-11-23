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

## 10. Reference 3 Master Specification (Minimalist Motivational Kinetic Short)

> **Trigger**: Whenever instructed to edit a raw video in **Reference 3** (`refeance 3` / `Reference 3 Style`), the editor must strictly execute the following parameters defined in `templates/template_ref3.json` and measured from `references/ref3/reference_3_source.mp4`.

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

### 3. Subtitle Style & Exact Kinetic Placement
- **Language**: **TANGLISH (Romanized Tamil + English keywords matching spoken audio)**. Modeled directly on the Reference 3 video (`referance/referance 3/vidssave.com kisthenics podcast... 720P.mp4`):
  - Spoken Tamil is transcribed phonetically in Roman script (e.g. `RAMAYANATHULA IRUNDHU...`, `NAAM ENNA...`, `HANUMAN-A PATHI MATTUM...`, `LATENT POTENTIAL IRUKKU!`, `SOLLAAMA KOLLAAMA POYITAANGA!`, `LOYALTY-E ILLA!`, `SELFLESS LOYALTY DHAAN!`, etc.).
  - Spoken English phrases are rendered in English (`EVERYBODY IN THIS WORLD IS LIKE HANUMAN!`, `THAT'S THE MENTOR!`, `LOYALTY!`, `LIVE EXAMPLE!`).
  - **Zero Content Mismatch**: Never fabricate mythical storylines or conceptual English summaries that do not match what the speaker is saying. Subtitles must strictly reflect the authentic spoken topic and real-life examples.
- **Font & Fill**: Bold condensed sans-serif (**Anton** / **Impact**), vibrant **Electric Yellow (`#FFE500` / RGB: 255, 229, 0)** with a 3px dark stroke outline (`#000000`) and a multi-layer soft dark drop shadow (`rgba(0,0,0,0.85)` offset `4px, 4px`, blur `6px`). The yellow text color ensures ultra-high contrast and readability against both the background wall and clothing.
- **Chunking & Pacing**: Rapid **1 to 3 words per beat**. Use `"..."` and `"!"` to control dramatic pacing and impact.
- **Zero Latency / Visual Lead (-60ms to -80ms)**: Subtitle frames trigger with a 60ms to 80ms visual lead relative to the acoustic syllable onset. This compensates for human visual latency and ensures the viewer reads the text with crisp, instantaneous synchronization without any perceived lag or delay.
- **Safe Zone Protection**: All text must reside strictly within the 16:9 video frame boundaries ($Y = 656 \text{ to } 1264$). **Never cover the speaker's face, eyes, or mouth**.
- **Dynamic Placement Zones (Rotated per phrase)**:
  - **Zone A (Left)**: Left of the speaker's head/shoulder ($X = 75 \text{ to } 390$, left-aligned, vertical center $Y \approx 785$).
  - **Zone B (Right)**: Right of the speaker's head/shoulder ($X = 690 \text{ to } 1005$, right-aligned, vertical center $Y \approx 785$).
  - **Zone C (Bottom-Center)**: Lower third of the video frame, directly above the bottom gradient ($X = 540$, center-aligned, vertical center $Y \approx 1140$).
- **Hierarchy & Kinetic Animation**:
  - **Pop-in Sharp**: Words pop onto the screen sharply on the exact spoken beat. Zero slow fades or blurry zooms.
  - **Scale Hierarchy**: Emphasized/hook words scale **`1.4x`** larger than supporting words.
  - **Cluster Stacking & Reset**: Stack 2 to 3 sequential phrases across different zones (e.g. Zone A $\rightarrow$ Zone B $\rightarrow$ Zone C) to form a brief visual kinetic cluster, then **clear all text cleanly** at the start of the next sentence. When a zone receives a new phrase within the same cluster, it cleanly updates that zone.

