---
name: demucs
description: AI Audio Enhancement & Source Separation using Meta Research Demucs (v4). Separates spoken vocals and dialogue from background music, room reverb, and studio noise for pristine speech clarity.
---

# Demucs — AI Audio Enhancement & Vocal Separation

Uses Meta AI Research's state-of-the-art hybrid transformer model (`htdemucs`) to isolate clean dialogue from background music, hum, reverb, and room noise.

## Usage

```bash
# Isolate vocals / speech from raw audio or video
python -m demucs --two-stems=vocals -o separated/ "audio.wav"
```

The isolated clean speech is output to:
`separated/htdemucs/<track_name>/vocals.wav`
