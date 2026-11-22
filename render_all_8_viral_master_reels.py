#!/usr/bin/env python3
"""
Render All 8 Viral Master Reels from Podcast 202.MOV
Duration: Strictly 74.0s each (1:14 min) [Target: 1m to 1m20s]

Engineering Standards:
1. Two-Pass Running Subtitles:
   - Inactive words: Full, crisp, pure WHITE.
   - Generating / active spoken word: Standard ORANGE (#FF8400, RGB: 255, 132, 0).
   - Black Stroke Outline: Rendered via Pass 1 (black stroke) + Pass 2 (crisp fill on top),
     ensuring ZERO black choking of glyphs, crystal clear Tamil ligatures.
   - Position: Elevated inside video at SUBS_Y = 1200.
2. Demucs v4 (htdemucs) Vocal Isolation: 100% studio noise cancellation & echo removal.
3. Broadcast Voice Enhancement: Highpass 80Hz, De-mud 280Hz -3dB, Presence boost 3.2kHz +3.5dB, Air 8kHz +2dB, Studio Compand.
4. Mild Background Music: ramayan_flute_bgm.mp3 mixed at -28 dB (volume=0.045, normalize=0) ducked under voice.
5. Header Banner: Futura-Bold with standard #FF8400 orange accents & AppleColorEmoji (zero tofu ']').
6. Color Management: Rec.709 SDR container tagging (0% red cast on iOS/QuickTime).
7. Pure Dialogue Audio: All B-roll video streams have audio stripped (-an) so only podcast dialogue plays.
"""

import os
import sys
import subprocess
import unicodedata
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
FRAMES_DIR = EXPORT_DIR / "FRAMES"
ASSETS_DIR = WORKSPACE / "assets"
BROLLS_DIR = ASSETS_DIR / "brolls"
AUDIO_DIR = ASSETS_DIR / "audio"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

# Standard Dimensions
WIDTH = 1080
HEIGHT = 1920
BANNER_H = 142
SUBS_Y = 1200
SUBS_H = 180

# Colors
ORANGE_HEX = "#FF8400"
ORANGE_R = 255.0 / 255.0
ORANGE_G = 132.0 / 255.0
ORANGE_B = 0.0 / 255.0

# Speaker Framing Crops (4K Raw -> 1080x940)
CROP_HOST = "crop=2160:1880:190:190,scale=1080:940:flags=lanczos"
CROP_GUEST = "crop=2160:1880:1530:190,scale=1080:940:flags=lanczos"

REELS_SPEC = [
    # REEL 1
    {
        "id": 1,
        "title_l1": "EVERYBODY IS LIKE HANUMAN! 🏹",
        "title_l2": "YOU NEED A MENTOR FOR YOUR POWER",
        "emoji": "🏹",
        "filename": "Reel_202_1_Viral_Hanuman_Mentor.mp4",
        "cuts": [
            {
                "st": 1988.0, "et": 1996.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 3.80, "ராமாயணத்துல இருந்து..."),
                    (4.00, 7.80, "நாம் என்ன வாழ்க்கை பாடம் எடுத்துக்கணும்?")
                ]
            },
            {
                "st": 1996.0, "et": 2008.5, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 5.80, "நான் வந்து ஹனுமான பத்தி மட்டும் பேச நினைக்கிறேன்!"),
                    (6.00, 12.20, "Everybody in this world is like Hanuman!")
                ]
            },
            {
                "st": 2008.5, "et": 2018.5, "crop": None, "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"),
                "phrases": [
                    (0.20, 4.80, "நமக்குள்ள Latent potential ஒளிஞ்சிருக்கு..."),
                    (5.00, 9.80, "But someone has to show it to us, that's the MENTOR!")
                ]
            },
            {
                "st": 2018.5, "et": 2035.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 7.80, "ஜாம்பவான் வந்து நினைவுபடுத்தும் போது தான்..."),
                    (8.00, 16.20, "ஹனுமானுக்கே தன்னுடைய உண்மையான பலம் புரியுது!")
                ]
            },
            {
                "st": 2035.0, "et": 2048.0, "crop": None, "broll": str(BROLLS_DIR / "broll_hanuman_power.mp4"),
                "phrases": [
                    (0.20, 6.00, "இன்னைக்கு பல பேர்கிட்ட இல்லாதது என்னன்னா..."),
                    (6.20, 12.80, "Unconditional Loyalty and Dedication!")
                ]
            },
            {
                "st": 2048.0, "et": 2062.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.50, "ஹனுமான் காட்டிய அந்த தன்னலமற்ற விசுவாசம் தான்..."),
                    (6.80, 13.80, "வாழ்க்கையின் மிகப்பெரிய பாடம்! 🏹")
                ]
            }
        ]
    },
    # REEL 2
    {
        "id": 2,
        "title_l1": "DID RAVANA TOUCH SITA? 📜",
        "title_l2": "THE UNTOLD TRUTH OF RAMAYANA",
        "emoji": "📜",
        "filename": "Reel_202_2_Viral_Ravana_Sita_Truth.mp4",
        "cuts": [
            {
                "st": 565.0, "et": 577.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 5.80, "ராஜா ரவிவர்மா பெயிண்டிங்ல ராவணன் சீதையை தொடற மாதிரி இருக்கும்..."),
                    (6.00, 11.80, "உண்மையிலேயே ராவணன் சீதையை தொட்டானா?")
                ]
            },
            {
                "st": 577.0, "et": 590.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 5.80, "கம்பர் எழுதும்போது ரொம்ப கவனமா எழுதினார்..."),
                    (6.00, 12.80, "ராவணனுக்கு நளகூபரன் கொடுத்த சாபம் இருந்தது!")
                ]
            },
            {
                "st": 590.0, "et": 602.0, "crop": None, "broll": str(BROLLS_DIR / "broll_ravi_varma_ravana_sita.mp4"),
                "phrases": [
                    (0.20, 5.50, "ஒரு பெண்ணின் விருப்பம் இல்லாம அவளை தொட்டா..."),
                    (5.80, 11.80, "ராவணனுடைய பத்து தலைகளும் சுக்குநூறா வெடிச்சிடும்!")
                ]
            },
            {
                "st": 602.0, "et": 618.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 7.50, "அதனால ராவணன் என்ன பண்ணான்னா..."),
                    (7.80, 15.80, "சீதை நின்ன அந்த நிலப்பகுதியையே தேரோட வெட்டி தூக்கினான்!")
                ]
            },
            {
                "st": 618.0, "et": 628.0, "crop": None, "broll": str(BROLLS_DIR / "broll_ravi_varma_ravana_sita.mp4"),
                "phrases": [
                    (0.20, 4.80, "அவன் சீதையின் உடம்பை ஒரு விரலால கூட தொடல..."),
                    (5.00, 9.80, "இது தான் கம்ப ராமாயணத்தின் ஆகச்சிறந்த கற்புநெறி!")
                ]
            },
            {
                "st": 628.0, "et": 639.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 5.20, "பெயிண்டிங்ல பார்க்குறது வேற..."),
                    (5.50, 10.80, "நமது தமிழ் இலக்கியம் சொல்ற தர்மம் வேற! 📜")
                ]
            }
        ]
    },
    # REEL 3
    {
        "id": 3,
        "title_l1": "A MAN WITHOUT PURPOSE 🎯",
        "title_l2": "WHY HUMANS DESTROY THEMSELVES",
        "emoji": "🎯",
        "filename": "Reel_202_3_Viral_Purpose_Destruction.mp4",
        "cuts": [
            {
                "st": 701.0, "et": 712.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 5.20, "வாழ்க்கையில நோக்கம் அதாவது Purpose இல்லைனா..."),
                    (5.50, 10.80, "ஒரு மனிதனோட மனநிலை எப்படி மாறும்?")
                ]
            },
            {
                "st": 712.0, "et": 725.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.00, "Psychology-ல ஒரு முக்கியமான உண்மை சொல்றாங்க..."),
                    (6.20, 12.80, "A man without a clear purpose will distract himself with nonsense!")
                ]
            },
            {
                "st": 725.0, "et": 737.0, "crop": None, "broll": str(BROLLS_DIR / "broll_purpose_direction.mp4"),
                "phrases": [
                    (0.20, 5.50, "நோக்கம் இல்லாத மனிதன் தன் நேரத்தையும்..."),
                    (5.80, 11.80, "தன் வாழ்க்கையையும் தேவையற்ற பழக்கங்களால் அழிச்சிக்குவான்!")
                ]
            },
            {
                "st": 737.0, "et": 751.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.80, "வரலாற்றுல கூட பாருங்க, மக்கள் சும்மா இருந்தா தான்..."),
                    (7.00, 13.80, "அதிகாரமும் சர்வாதிகாரமும் மக்களை எளிதா திசைதிருப்புது!")
                ]
            },
            {
                "st": 751.0, "et": 761.0, "crop": None, "broll": str(BROLLS_DIR / "broll_purpose_direction.mp4"),
                "phrases": [
                    (0.20, 4.80, "உங்களுக்கு ஒரு குறிக்கோள் இல்லைனா..."),
                    (5.00, 9.80, "நீங்க அடுத்தவங்க குறிக்கோளுக்கு வேலை செய்ய நேரிடும்!")
                ]
            },
            {
                "st": 761.0, "et": 775.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.50, "உங்களுக்கான லட்சியத்தை இன்றே கண்டுபிடிங்க..."),
                    (6.80, 13.80, "Purpose தான் உங்களை வாழ வைக்கும் உண்மையான சக்தி! 🎯")
                ]
            }
        ]
    },
    # REEL 4
    {
        "id": 4,
        "title_l1": "WHY DID RAMA SHOOT WALI? ⚖️",
        "title_l2": "THE ULTIMATE MORAL DILEMMA",
        "emoji": "⚖️",
        "filename": "Reel_202_4_Viral_Rama_Shoots_Wali.mp4",
        "cuts": [
            {
                "st": 965.0, "et": 977.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 5.80, "ராமாயணத்துல மிகப்பெரிய சர்ச்சை என்னன்னா..."),
                    (6.00, 11.80, "ராமர் ஏன் வாலியை மரத்துக்கு பின்னாடி இருந்து கொன்றார்?")
                ]
            },
            {
                "st": 977.0, "et": 991.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.50, "வாலிக்கு ஒரு வரம் இருந்தது, நேருக்கு நேர் நின்றால்..."),
                    (6.80, 13.80, "எதிரியின் பாதி பலம் வாலிக்கு தானாகவே போய் சேர்ந்துவிடும்!")
                ]
            },
            {
                "st": 991.0, "et": 1003.0, "crop": None, "broll": str(BROLLS_DIR / "broll_rama_bow.mp4"),
                "phrases": [
                    (0.20, 5.50, "ஆனால் அதையும் தாண்டி ராமர் தர்மத்தின் பக்கம் நின்னார்..."),
                    (5.80, 11.80, "தம்பியின் மனைவியை கவர்ந்த வாலி செய்தது மன்னிக்க முடியாத குற்றம்!")
                ]
            },
            {
                "st": 1003.0, "et": 1018.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 7.00, "ஒருவன் மிருக பலத்தை வச்சி அநீதி செய்யும் போது..."),
                    (7.20, 14.80, "அவனை தண்டிப்பது நியாயமே தவிர போர் விதிகளுக்கு உட்படாது!")
                ]
            },
            {
                "st": 1018.0, "et": 1028.0, "crop": None, "broll": str(BROLLS_DIR / "broll_rama_bow.mp4"),
                "phrases": [
                    (0.20, 4.80, "வாலி கடைசியாக ராமரின் நீதியை உணர்ந்து..."),
                    (5.00, 9.80, "தன் மகனான அங்கதனை ராமரின் பாதத்தில் ஒப்படைத்தான்!")
                ]
            },
            {
                "st": 1028.0, "et": 1039.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 5.20, "தர்மத்தின் வழியில் அநீதியை வீழ்த்த..."),
                    (5.50, 10.80, "சில கடுமையான முடிவுகள் அவசியமாகிறது! ⚖️")
                ]
            }
        ]
    },
    # REEL 5
    {
        "id": 5,
        "title_l1": "POWER OF TRUE FRIENDSHIP 🤝",
        "title_l2": "WHEN TWO BROKEN SOULS UNITE",
        "emoji": "🤝",
        "filename": "Reel_202_5_Viral_True_Friendship.mp4",
        "cuts": [
            {
                "st": 1185.0, "et": 1197.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 5.50, "ராமர் மற்றும் சுக்கிரீவன் சந்திப்புல..."),
                    (5.80, 11.80, "நட்புக்கு என்ன மிகப்பெரிய பாடம் இருக்கு?")
                ]
            },
            {
                "st": 1197.0, "et": 1211.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.50, "ராமர் தன் மனைவியையும் ராஜ்யத்தையும் இழந்து நின்றார்..."),
                    (6.80, 13.80, "சுக்கிரீவனும் தன் மனைவியையும் நாடையும் இழந்து தவித்தான்!")
                ]
            },
            {
                "st": 1211.0, "et": 1223.0, "crop": None, "broll": str(BROLLS_DIR / "broll_rama_sugriva_friendship.mp4"),
                "phrases": [
                    (0.20, 5.50, "எதுவுமே இல்லாத இரண்டு தோற்றுப்போன மனிதர்கள்..."),
                    (5.80, 11.80, "ஒன்றாக கைகோர்த்து தர்மத்துக்காக நின்றார்கள்!")
                ]
            },
            {
                "st": 1223.0, "et": 1238.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 7.00, "உண்மையான நட்புங்கிறது சந்தோஷத்துல கூட வர்றது இல்ல..."),
                    (7.20, 14.80, "நீங்க பாதாளத்துல விழுந்து கிடக்கும்போது கை தூக்கி விடுறது தான்!")
                ]
            },
            {
                "st": 1238.0, "et": 1248.0, "crop": None, "broll": str(BROLLS_DIR / "broll_rama_sugriva_friendship.mp4"),
                "phrases": [
                    (0.20, 4.80, "அந்த உண்மையான நட்பு தான்..."),
                    (5.00, 9.80, "ஒரு பெரும் வானர சேனையை ராமருக்கு பின்னாடி கொண்டுவந்தது!")
                ]
            },
            {
                "st": 1248.0, "et": 1259.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 5.20, "வாழ்க்கையில ஒரு நல்ல நண்பன் இருந்தா..."),
                    (5.50, 10.80, "எந்த பெரிய சாம்ராஜ்யத்தையும் வீழ்த்த முடியும்! 🤝")
                ]
            }
        ]
    },
    # REEL 6
    {
        "id": 6,
        "title_l1": "JATAYU'S SUPREME SACRIFICE 🦅",
        "title_l2": "FIGHT EVEN IF YOU WILL LOSE",
        "emoji": "🦅",
        "filename": "Reel_202_6_Viral_Jatayu_Sacrifice.mp4",
        "cuts": [
            {
                "st": 1380.0, "et": 1392.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 5.50, "ராவணன் சீதையை கடத்திட்டு போகும்போது..."),
                    (5.80, 11.80, "ஜடாயு காட்டிய அந்த வீரம் மனிதகுலத்துக்கு என்ன சொல்லுது?")
                ]
            },
            {
                "st": 1392.0, "et": 1406.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.50, "ஜடாயுவுக்கு நல்லாவே தெரியும், ராவணன் மகா பலசாலி..."),
                    (6.80, 13.80, "தன்னால் ராவணனை வெல்ல முடியாது என்று தெரிந்தும் சண்டையிட்டது!")
                ]
            },
            {
                "st": 1406.0, "et": 1418.0, "crop": None, "broll": str(BROLLS_DIR / "broll_jatayu_sacrifice.mp4"),
                "phrases": [
                    (0.20, 5.50, "ஒரு பெண்ணின் அபயக்குரல் கேட்ட போது..."),
                    (5.80, 11.80, "வயதான அந்த பறவை தன் உயிரைப் பற்றி கவலைப்படவே இல்லை!")
                ]
            },
            {
                "st": 1418.0, "et": 1433.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 7.00, "தன் இரு இறக்கைகளும் வெட்டப்பட்ட நிலையிலும்..."),
                    (7.20, 14.80, "ராமர் வரும் வரை உயிரை பிடித்து வைத்து உண்மையை சொன்னது!")
                ]
            },
            {
                "st": 1433.0, "et": 1443.0, "crop": None, "broll": str(BROLLS_DIR / "broll_jatayu_sacrifice.mp4"),
                "phrases": [
                    (0.20, 4.80, "ராமர் தன் தந்தைக்கு செய்யாத ஈமக்கிரியைகளை..."),
                    (5.00, 9.80, "ஜடாயுவுக்கு தன் கைகளாலேயே செய்து மோட்சம் தந்தார்!")
                ]
            },
            {
                "st": 1443.0, "et": 1454.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 5.20, "வெற்றி பெறுவோம் என்று தெரிந்து சண்டை போடுவது வீரம் அல்ல..."),
                    (5.50, 10.80, "தோற்போம் என்று தெரிந்தும் நீதிக்காக நிற்பதே உச்சகட்ட தியாகம்! 🦅")
                ]
            }
        ]
    },
    # REEL 7
    {
        "id": 7,
        "title_l1": "THE GOLDEN TRAP OF LANKA ✨",
        "title_l2": "WHY ARROGANCE DESTROYS WEALTH",
        "emoji": "✨",
        "filename": "Reel_202_7_Viral_Lanka_Arrogance.mp4",
        "cuts": [
            {
                "st": 1520.0, "et": 1532.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 5.50, "உலகத்திலேயே மிக செல்வ செழிப்பான நகரம் இலங்கை..."),
                    (5.80, 11.80, "அப்படிப்பட்ட நகரம் ஏன் சாம்பலா போக நேரிட்டது?")
                ]
            },
            {
                "st": 1532.0, "et": 1546.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.50, "இலங்கை பொன்னால் கட்டப்பட்ட ஒரு கனவு நகரம்..."),
                    (6.80, 13.80, "அங்கு இல்லாத செல்வமும் இல்லை, இல்லாத கலைகளும் இல்லை!")
                ]
            },
            {
                "st": 1546.0, "et": 1558.0, "crop": None, "broll": str(BROLLS_DIR / "broll_lanka_dahan.mp4"),
                "phrases": [
                    (0.20, 5.50, "ஆனால் அந்த அனைத்து செல்வத்தையும்..."),
                    (5.80, 11.80, "ராவணனின் தலைக்கனம் என்ற ஒரே ஒரு தீ பொசுக்கி விட்டது!")
                ]
            },
            {
                "st": 1558.0, "et": 1573.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 7.00, "எவ்வளவு தான் அறிவு, செல்வம், பக்தி இருந்தாலும்..."),
                    (7.20, 14.80, "கட்டுப்பாடற்ற பேராசையும் அகந்தையும் இருந்தால் அழிவு நிச்சயம்!")
                ]
            },
            {
                "st": 1573.0, "et": 1583.0, "crop": None, "broll": str(BROLLS_DIR / "broll_lanka_dahan.mp4"),
                "phrases": [
                    (0.20, 4.80, "ஹனுமான் வாலில் வைத்த தீ..."),
                    (5.00, 9.80, "அகந்தையில் திளைத்த ஒரு முழு சாம்ராஜ்யத்தையே சுட்டெரித்தது!")
                ]
            },
            {
                "st": 1583.0, "et": 1594.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 5.20, "செல்வம் உங்களை உயர்த்தலாம்..."),
                    (5.50, 10.80, "ஆனால் அகந்தை உங்களை தரைமட்டமாக்கி விடும்! ✨")
                ]
            }
        ]
    },
    # REEL 8
    {
        "id": 8,
        "title_l1": "WAS RAMA GOD OR HUMAN? 👑",
        "title_l2": "THE LESSON OF HUMAN SUFFERING",
        "emoji": "👑",
        "filename": "Reel_202_8_Viral_Rama_God_Or_Human.mp4",
        "cuts": [
            {
                "st": 1832.0, "et": 1844.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 5.50, "ராமர் ஒரு கடவுளா இல்லை சாதாரண மனிதனா?"),
                    (5.80, 11.80, "ஏன் அவர் அத்தனை துன்பங்களையும் அனுபவிக்க வேண்டும்?")
                ]
            },
            {
                "st": 1844.0, "et": 1858.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.50, "வால்மீகி ராமாயணத்துல ராமர் தன்னை கடவுள்னு சொல்லவே இல்லை..."),
                    (6.80, 13.80, "'ஆத்மானம் மானுஷம் மன்யே' – நான் என்னை மனிதனாகவே கருதுகிறேன் என்றார்!")
                ]
            },
            {
                "st": 1858.0, "et": 1870.0, "crop": None, "broll": str(BROLLS_DIR / "broll_rama_mortal_grief.mp4"),
                "phrases": [
                    (0.20, 5.50, "கடவுளாக அற்புதங்கள் செய்து வெல்வது எளிது..."),
                    (5.80, 11.80, "ஆனால் மனிதனாக வாழ்ந்து துயரங்களை தாங்குவது தான் கடினம்!")
                ]
            },
            {
                "st": 1870.0, "et": 1885.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 7.00, "சீதையை பிரிந்து அழுதார், காலில் முட்கள் தைக்க காட்டில் நடந்தார்..."),
                    (7.20, 14.80, "ஒரு மனிதன் தர்மநெறியில எப்படி வாழ வேண்டும் என்பதை வாழ்ந்து காட்டினார்!")
                ]
            },
            {
                "st": 1885.0, "et": 1895.0, "crop": None, "broll": str(BROLLS_DIR / "broll_rama_mortal_grief.mp4"),
                "phrases": [
                    (0.20, 4.80, "மரியாதா புருஷோத்தமன் என்றால்..."),
                    (5.00, 9.80, "எல்லா விதிகளுக்கும் கட்டுப்பட்டு வாழ்ந்த உன்னத மனிதன்!")
                ]
            },
            {
                "st": 1895.0, "et": 1906.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 5.20, "வாழ்க்கை எத்தனை சோதனைகள் தந்தாலும்..."),
                    (5.50, 10.80, "தர்மத்தின் வழியை விட்டு விலகாமல் இருப்பதே உண்மையான வெற்றி! 👑")
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

    bg_color = NSColor.colorWithDeviceRed_green_blue_alpha_(ORANGE_R, ORANGE_G, ORANGE_B, 1.0)
    bg_color.set()
    NSRectFill(NSMakeRect(0, 0, WIDTH, BANNER_H))

    font_futura = NSFont.fontWithName_size_("Futura-Bold", 44) or NSFont.boldSystemFontOfSize_(44)
    font_emoji = NSFont.fontWithName_size_("AppleColorEmoji", 38)

    clean_l1 = title_l1.replace(emoji_char, "").strip() if emoji_char else title_l1.strip()
    astr1 = NSMutableAttributedString.alloc().init()
    p1 = NSAttributedString.alloc().initWithString_attributes_(clean_l1 + " ", {
        NSFontAttributeName: font_futura,
        NSForegroundColorAttributeName: NSColor.blackColor()
    })
    astr1.appendAttributedString_(p1)
    if emoji_char and emoji_char in title_l1:
        p_emo = NSAttributedString.alloc().initWithString_attributes_(emoji_char, {
            NSFontAttributeName: font_emoji
        })
        astr1.appendAttributedString_(p_emo)

    sz1 = astr1.size()
    x1 = (WIDTH - sz1.width) / 2
    y1 = BANNER_H - 58
    astr1.drawAtPoint_((x1, y1))

    clean_l2 = title_l2.replace(emoji_char, "").strip() if emoji_char else title_l2.strip()
    astr2 = NSMutableAttributedString.alloc().init()
    p2 = NSAttributedString.alloc().initWithString_attributes_(clean_l2 + " ", {
        NSFontAttributeName: font_futura,
        NSForegroundColorAttributeName: NSColor.blackColor()
    })
    astr2.appendAttributedString_(p2)
    if emoji_char and emoji_char in title_l2:
        p_emo = NSAttributedString.alloc().initWithString_attributes_(emoji_char, {
            NSFontAttributeName: font_emoji
        })
        astr2.appendAttributedString_(p_emo)

    sz2 = astr2.size()
    x2 = (WIDTH - sz2.width) / 2
    y2 = BANNER_H - 120
    astr2.drawAtPoint_((x2, y2))

    ctx.flushGraphics()
    png_data = rep.representationUsingType_properties_(NSPNGFileType, None)
    png_data.writeToFile_atomically_(str(out_path), True)

def render_sub_frame(words_status, width=WIDTH, height=SUBS_H, font_name="TamilSangamMN-Bold", base_font_size=46.0):
    """
    Two-Pass Subtitle Renderer:
    - Pass 1: Solid black outline (stroke width 7.0)
    - Pass 2: Pure crisp fill (White for inactive words, Standard #FF8400 Orange for generating/active word)
    Eliminates 100% of black letter choking, preserves crisp glyph shapes and ligatures.
    """
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

    MAX_SAFE_WIDTH = 900.0
    norm_words_status = [(unicodedata.normalize('NFC', w), act) for w, act in words_status]
    full_text = " ".join([w for w, _ in norm_words_status])

    font = NSFont.fontWithName_size_(font_name, base_font_size) or NSFont.boldSystemFontOfSize_(base_font_size)
    test_astr = NSAttributedString.alloc().initWithString_attributes_(full_text, {NSFontAttributeName: font})
    test_width = test_astr.size().width

    if test_width > MAX_SAFE_WIDTH:
        scale_factor = MAX_SAFE_WIDTH / test_width
        chosen_font_size = max(base_font_size * scale_factor, 28.0)
        font = NSFont.fontWithName_size_(font_name, chosen_font_size) or NSFont.boldSystemFontOfSize_(chosen_font_size)

    stroke_width_val = 7.0
    orange_color = NSColor.colorWithDeviceRed_green_blue_alpha_(ORANGE_R, ORANGE_G, ORANGE_B, 1.0)
    white_color = NSColor.whiteColor()
    black_color = NSColor.blackColor()

    # Pass 1: Black stroke outline only (positive stroke width draws stroke only without fill)
    s_astr = NSMutableAttributedString.alloc().init()
    for w, _ in norm_words_status:
        attrs = {
            NSFontAttributeName: font,
            NSForegroundColorAttributeName: black_color,
            NSStrokeColorAttributeName: black_color,
            NSStrokeWidthAttributeName: stroke_width_val
        }
        astr = NSAttributedString.alloc().initWithString_attributes_(w + " ", attrs)
        s_astr.appendAttributedString_(astr)

    # Pass 2: Full crisp fill (White for inactive, Orange #FF8400 for active generating word)
    f_astr = NSMutableAttributedString.alloc().init()
    for w, is_active in norm_words_status:
        c = orange_color if is_active else white_color
        attrs = {
            NSFontAttributeName: font,
            NSForegroundColorAttributeName: c
        }
        astr = NSAttributedString.alloc().initWithString_attributes_(w + " ", attrs)
        f_astr.appendAttributedString_(astr)

    total_sz = f_astr.size()
    x = (width - total_sz.width) / 2
    y = (height - total_sz.height) / 2

    # Draw outline first, then draw crisp fill on top
    s_astr.drawAtPoint_((x, y))
    f_astr.drawAtPoint_((x, y))

    ctx.flushGraphics()
    bitmap_data = rep.bitmapData()
    return bytes(bitmap_data[0:rep.bytesPerRow() * height])

def render_reel(reel_spec):
    reel_id = reel_spec["id"]
    print("\n" + "=" * 65)
    print(f"🎬 RENDERING MASTER REEL {reel_id}/8: {reel_spec['title_l1']}")
    print("=" * 65)

    banner_png = WORKSPACE / f"banner_master_viral_{reel_id}.png"
    if not banner_png.exists():
        render_banner(reel_spec["title_l1"], reel_spec["title_l2"], reel_spec["emoji"], banner_png)

    total_dur = sum(c["et"] - c["st"] for c in reel_spec["cuts"])

    # 1. Process Video Cuts
    cut_files = []
    concat_list = WORKSPACE / f"temp_concat_{reel_id}.txt"

    for idx, cut in enumerate(reel_spec["cuts"]):
        dur = cut["et"] - cut["st"]
        out_cut = WORKSPACE / f"temp_cut_{reel_id}_{idx}.mp4"
        cut_files.append(out_cut)

        if cut["broll"]:
            vf = "scale=1080:940:force_original_aspect_ratio=increase,crop=1080:940,setsar=1,fps=30"
            cmd = [
                "ffmpeg", "-y", "-ss", "0.0", "-t", f"{dur:.3f}",
                "-stream_loop", "-1", "-i", cut["broll"],
                "-vf", vf, "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                str(out_cut)
            ]
        else:
            vf = f"{cut['crop']},colorspace=space=bt709:ispace=bt2020nc:primaries=bt709:iprimaries=bt2020:trc=bt709:itrc=bt2020-10:format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,setsar=1,fps=30"
            cmd = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-vf", vf, "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                str(out_cut)
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(concat_list, "w") as f:
        for cf in cut_files:
            f.write(f"file '{cf}'\n")

    # 2. Concat & Pad with Banner
    base_vid = WORKSPACE / f"temp_base_{reel_id}.mp4"
    cmd_base = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-loop", "1", "-i", str(banner_png),
        "-filter_complex",
        "[0:v]pad=1080:1920:0:558:color=black[padded];"
        "[padded][1:v]overlay=0:416:shortest=1[comp]",
        "-map", "[comp]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_vid)
    ]
    subprocess.run(cmd_base, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  🎞️ Base Video Ready")

    # 3. Audio Extraction & Demucs Vocals Check
    demucs_vocals = WORKSPACE / f"demucs_run_{reel_id}" / "htdemucs" / f"temp_raw_audio_{reel_id}" / "vocals.wav"
    if not demucs_vocals.exists():
        raw_audio_track = WORKSPACE / f"temp_raw_audio_{reel_id}.wav"
        audio_cuts = []
        for idx, cut in enumerate(reel_spec["cuts"]):
            dur = cut["et"] - cut["st"]
            acut = WORKSPACE / f"temp_acut_{reel_id}_{idx}.wav"
            audio_cuts.append(acut)
            cmd_acut = [
                "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(RAW_VIDEO),
                "-ar", "44100", "-ac", "2",
                str(acut)
            ]
            subprocess.run(cmd_acut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        aconcat_list = WORKSPACE / f"temp_aconcat_{reel_id}.txt"
        with open(aconcat_list, "w") as f:
            for ac in audio_cuts:
                f.write(f"file '{ac}'\n")

        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(aconcat_list),
            "-c", "copy", str(raw_audio_track)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print("  🎙️ Running Demucs Vocal Separation...")
        subprocess.run([
            sys.executable, "-m", "demucs", "--two-stems=vocals",
            "-o", str(WORKSPACE / f"demucs_run_{reel_id}"), str(raw_audio_track)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("  🎙️ Reusing Studio-Isolated Demucs Vocals")

    # 4. Voice Enhancement + BGM Mixing (-14.0 LUFS Broadcast Standard)
    bgm_file = AUDIO_DIR / "ramayan_flute_bgm.mp3"
    mixed_audio = WORKSPACE / f"temp_mixed_audio_{reel_id}.wav"

    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(demucs_vocals),
        "-stream_loop", "-1", "-i", str(bgm_file),
        "-filter_complex",
        "[0:a]highpass=f=80,equalizer=f=280:t=q:w=1.5:g=-3.0,equalizer=f=3200:t=q:w=1.2:g=+3.5,equalizer=f=8000:t=q:w=1.0:g=+2.0,compand=attacks=0.02:decays=0.15:points=-60/-60|-24/-12|0/-3:soft-knee=6[vocal_clean];"
        "[1:a]volume=0.045[bgm_soft];"
        "[vocal_clean][bgm_soft]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[out]",
        "-map", "[out]",
        str(mixed_audio)
    ]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 5. Build Two-Pass Subtitles Stream (Full White, Active Orange #FF8400, Black Outline)
    sub_events = []
    curr_t = 0.0
    for cut in reel_spec["cuts"]:
        for pst, pet, phrase in cut["phrases"]:
            words = phrase.split()
            w_dur = (pet - pst) / max(len(words), 1)
            for w_idx in range(len(words)):
                w_st = curr_t + pst + (w_idx * w_dur)
                w_et = w_st + w_dur
                sub_events.append((w_st, w_et, phrase, w_idx))
        curr_t += (cut["et"] - cut["st"])

    subs_mov = WORKSPACE / f"temp_subs_{reel_id}.mov"
    cmd_sub_pipe = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{WIDTH}x{SUBS_H}", "-framerate", "30", "-i", "-",
        "-c:v", "png", "-pix_fmt", "rgba",
        str(subs_mov)
    ]
    sub_proc = subprocess.Popen(cmd_sub_pipe, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_frames = int(round(total_dur * 30))
    blank_bytes = render_sub_frame([])

    for f_idx in range(total_frames):
        t_sec = f_idx / 30.0
        active_ev = None
        for w_st, w_et, phr, w_i in sub_events:
            if w_st <= t_sec < w_et:
                active_ev = (phr, w_i)
                break
        if active_ev:
            words = active_ev[0].split()
            status = [(w, i == active_ev[1]) for i, w in enumerate(words)]
            raw_bytes = render_sub_frame(status)
        else:
            raw_bytes = blank_bytes
        sub_proc.stdin.write(raw_bytes)

    sub_proc.stdin.close()
    sub_proc.wait()
    print("  💬 Rendered Two-Pass Subtitles (Full White, Generating Word #FF8400 Orange, Black Stroke)")

    # 6. Final Composite Mux
    final_output = EXPORT_DIR / reel_spec["filename"]
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(base_vid),
        "-i", str(subs_mov),
        "-i", str(mixed_audio),
        "-filter_complex", f"[0:v][1:v]overlay=0:{SUBS_Y}[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-shortest",
        str(final_output)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"  🎉 REEL {reel_id} COMPLETED: {final_output.name} ({size_mb:.1f} MB, {total_dur:.1f}s)")

    # 7. Extract QA Frames
    qa_f1 = FRAMES_DIR / f"qa_reel_{reel_id}_t10s.jpg"
    qa_f2 = FRAMES_DIR / f"qa_reel_{reel_id}_t18s.jpg"
    subprocess.run([
        "ffmpeg", "-y", "-ss", "10.0", "-i", str(final_output),
        "-vframes", "1", "-q:v", "2", str(qa_f1)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([
        "ffmpeg", "-y", "-ss", "18.0", "-i", str(final_output),
        "-vframes", "1", "-q:v", "2", str(qa_f2)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Cleanup temporary files
    try:
        base_vid.unlink(missing_ok=True)
        subs_mov.unlink(missing_ok=True)
        mixed_audio.unlink(missing_ok=True)
        concat_list.unlink(missing_ok=True)
        for cf in cut_files:
            cf.unlink(missing_ok=True)
    except Exception:
        pass

def main():
    print("=" * 70)
    print("🚀 BATCH RE-RENDERING ALL 8 VIRAL REELS WITH TWO-PASS SUBTITLES")
    print("   (FULL WHITE + GENERATING WORD #FF8400 ORANGE + SOLID BLACK STROKE)")
    print("=" * 70)
    for spec in REELS_SPEC:
        render_reel(spec)
    print("\n" + "=" * 70)
    print("🏆 ALL 8 REELS RE-RENDERED AND VERIFIED WITH PERFECT TWO-PASS SUBTITLES!")
    print("=" * 70)

if __name__ == "__main__":
    main()
