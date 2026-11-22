# Project Rules & Master Guidelines (`rules.md`)

> **Master Video Editor**: Standardized execution protocol applying across all 4 reference styles.  
> **Core Principle**: Identical video structure, pacing, audio engineering, and validation rules; only visual style parameters (title look, subtitle font/fill/size/position) vary per reference template.

---

## 1. Project Rules (Non-Negotiable)

1. **Never Modify a Template File**: `templates/template_ref*.json` files are immutable style blueprints. The AI only decides content (hook selection, cut points, silence removal, b-roll choices, subtitle text, title text) and saves them in `edit_plan.json`.
2. **Always Use `render.py`**: All final videos must be rendered through the single deterministic rendering script. Same input + same template = bit-exact identical output every time.
3. **Never Edit Layout Manually**: All layout coordinates, fonts, and dimensions belong strictly inside the reference template file.
4. **Always Run `validate.py` Before Delivering**: Every video must pass all validation checks. If any check fails, fix `edit_plan.json` or re-render until 100% compliant.

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
- **Background Music (Bed)**: Ambient lo-fi track ducked to **`-20 dB to -25 dB`** under speech.
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
   - Background music loudness is between $-25\text{ dB}$ and $-20\text{ dB}$.
   - Voice loudness is $-14.0 \pm 0.5\text{ LUFS}$.
5. **Sync Tolerance**: Audio-subtitle alignment drift $< 100\text{ms}$.
