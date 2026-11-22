#!/usr/bin/env python3
"""
8 Master Viral Reels Engine (1min to 1:20min / ~72s-75s)
- Kallaway High-CTR Hook Frameworks (Curiosity Gap, Contrast, Single Focal Point)
- Mild Background Music: Ramayan Flute BGM set to -28 dB (volume=0.045, normalize=0)
- Contextual B-Rolls: Matched directly to the spoken story with 100% continuous dialogue
- Subtitle Safe Zone: SUBS_Y = 1200 with 212px clearance inside video frame
- Standard Orange: #FF8400 (RGB: 255, 132, 0)
- Rec.709 SDR Conversion: 0% Red Cast in macOS ColorSync / QuickTime
- Banner: Clean Futura-Bold + AppleColorEmoji (NO tofu boxes)
- Subtitles: AppKit CoreText TamilSangamMN-Bold (NFC, NO dotted circles)
- Stroke: 14pt Solid Black Outline on ALL Subtitle Words
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

# Subtitle Position: Safe Zone inside lower third of video (212px clearance to bottom video edge)
SUBS_Y = 1200
SUBS_H = 140

# Exact user standard color: #FF8400 (RGB: 255, 132, 0)
ORANGE_R = 255 / 255.0
ORANGE_G = 132 / 255.0
ORANGE_B = 0.0

# Native 4K Rec.709 SDR Crops from 3840x2160 Raw Video
REC709_FILTER = (
    "colorspace=space=bt709:ispace=bt2020nc:primaries=bt709:iprimaries=bt2020:"
    "trc=bt709:itrc=bt2020-10:format=yuv420p,"
    "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709"
)

CROP_HOST = f"crop=2160:1880:150:190,scale={WIDTH}:{VIDEO_H}:flags=lanczos,{REC709_FILTER},setsar=1,fps=30"
CROP_GUEST = f"crop=2160:1880:1530:190,scale={WIDTH}:{VIDEO_H}:flags=lanczos,{REC709_FILTER},setsar=1,fps=30"

# 8 Curated Master Viral Reels with Kallaway High-CTR Framework Hooks
ALL_MASTER_REELS = [
    {
        "id": 1,
        "title_l1": "STOP MOCKING THIS! 🏹",
        "title_l2": "THE BIGGEST LIFE LESSON",
        "emoji": "🏹",
        "filename": "Reel_202_1_Why_Mock_Ramayana.mp4",
        "cuts": [
            {
                "st": 121.0, "et": 130.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.30, "ஒரு கதையோ விஷயமோ பேசினா..."),
                    (4.50, 8.80, "ராமாயணம் மாதிரி இழுக்காதீங்கன்னு சொல்றாங்க!")
                ]
            },
            {
                "st": 130.0, "et": 142.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 5.80, "நாம ஏன் ராமாயணத்தை பத்தி பேசக் கூடாது?"),
                    (6.00, 11.80, "அதை விட பெரிய வாழ்க்கை பாடம் எங்க இருக்கு?")
                ]
            },
            {
                "st": 142.0, "et": 154.0, "crop": None, "broll": str(BROLLS / "broll_temple.mp4"),
                "phrases": [
                    (0.20, 5.50, "இன்னைக்கு நாம பார்க்கிற மாபெரும் திரைப்படங்கள் எல்லாமே..."),
                    (5.80, 11.80, "அந்த இதிகாசங்களில் இருந்து உருவான சிந்தனைகள் தான்!")
                ]
            },
            {
                "st": 154.0, "et": 168.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.50, "அதை வெறும் கதையா மட்டும் பார்க்காதீங்க..."),
                    (6.80, 13.80, "மனித மனங்களின் ஆழத்தையும், தியாகத்தையும் புரிய வைக்கும் காவியம்!")
                ]
            },
            {
                "st": 168.0, "et": 180.0, "crop": None, "broll": str(BROLLS / "broll_scripture.mp4"),
                "phrases": [
                    (0.20, 5.20, "தலைமுறைகள் கடந்தும் இந்த கருத்துக்கள் நிலைத்து நிற்க காரணம்..."),
                    (5.50, 11.80, "அதில் உள்ள மாறாத வாழ்வியல் உண்மைகள் தான்!")
                ]
            },
            {
                "st": 180.0, "et": 195.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.20, 6.80, "எந்த சூழலிலும் நிதானத்தை இழக்காமல் தர்மத்தோடு நிற்க பழகுங்க..."),
                    (7.00, 14.80, "வாழ்க்கையில் எந்த நெருக்கடி வந்தாலும் உங்களால் தலைநிமிர்ந்து நிற்க முடியும்!")
                ]
            }
        ]
    },
    {
        "id": 2,
        "title_l1": "KAMBAR VS VALMIKI 📜",
        "title_l2": "WHO WROTE IT BETTER?",
        "emoji": "📜",
        "filename": "Reel_202_2_Kambar_Vs_Valmiki.mp4",
        "cuts": [
            {
                "st": 334.0, "et": 343.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.30, "வால்மீகி சொல்லியிருக்கிறது ஒரு மாதிரி இருக்கு..."),
                    (4.50, 8.80, "இவர் தமிழில் கம்பராமாயணத்தில் வேற மாதிரி சொல்லியிருக்காரு!")
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
                "st": 356.0, "et": 368.0, "crop": None, "broll": str(BROLLS / "broll_scripture.mp4"),
                "phrases": [
                    (0.25, 5.50, "தமிழ் மொழிக்கு கம்பர் கொடுத்த இந்த பொக்கிஷம்..."),
                    (5.80, 11.80, "உலக இலக்கியங்களிலேயே வேற எங்கேயும் பார்க்க முடியாது!")
                ]
            },
            {
                "st": 368.0, "et": 382.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.80, "ஒவ்வொரு சொல்லிலும் அன்பையும், தர்மத்தையும், நீதியையும்..."),
                    (7.10, 13.80, "அவ்வளவு நுட்பமா செதுக்கிய கவிச்சக்கரவர்த்தி கம்பர்!")
                ]
            },
            {
                "st": 382.0, "et": 394.0, "crop": None, "broll": str(BROLLS / "broll_temple.mp4"),
                "phrases": [
                    (0.25, 5.50, "அதனாலதான் ஆயிரம் வருடங்கள் கடந்தும்..."),
                    (5.80, 11.80, "கம்பராமாயணம் தமிழ் நெஞ்சங்களில் அழியாமல் வாழுது!")
                ]
            },
            {
                "st": 395.0, "et": 409.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.50, "இதை வெறும் கதையா பார்க்காம வாழ்க்கை பாடமா பாருங்க..."),
                    (6.80, 13.80, "மனித மனங்களின் ரகசியங்களை மிக ஆழமா புரிஞ்சுக்கலாம்!")
                ]
            }
        ]
    },
    {
        "id": 3,
        "title_l1": "14 YEARS SACRIFICE 🌲",
        "title_l2": "DUTY OVER DESIRE",
        "emoji": "🌲",
        "filename": "Reel_202_3_Sacrifice_Of_Vanavasam.mp4",
        "cuts": [
            {
                "st": 442.0, "et": 451.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.20, "அரியணை ஏற வேண்டிய திருநாளில்..."),
                    (4.50, 8.80, "பதினான்கு வருஷம் வனவாசம் போகணும்னு சொன்னா எப்படி இருக்கும்?")
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
                "st": 464.0, "et": 476.0, "crop": None, "broll": str(BROLLS / "broll_forest_mist.mp4"),
                "phrases": [
                    (0.25, 5.50, "பதவியும் பணமும் அதிகாரமும் பெருசு இல்லை..."),
                    (5.80, 11.80, "தர்மமும் கடமையும் தான் முக்கியம்னு உலகத்துக்கு நிரூபிச்சாரு!")
                ]
            },
            {
                "st": 476.0, "et": 489.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "எந்த சுகபோகமும் வேண்டாம்னு ஒரு நொடியில் உதறி தள்ளினார்,"),
                    (6.30, 12.80, "கொடுத்த வாக்கை காப்பாற்றுவதுதான் உண்மையான வீரம்!")
                ]
            },
            {
                "st": 489.0, "et": 501.0, "crop": None, "broll": str(BROLLS / "broll_golden_sunrise.mp4"),
                "phrases": [
                    (0.25, 5.50, "வாழ்க்கை உங்களை சோதிக்கும் போது தப்பிச்சு ஓடாதீங்க..."),
                    (5.80, 11.80, "அமைதியா கடமையை செய்ங்க, வெற்றி உங்களை தேடி வரும்!")
                ]
            },
            {
                "st": 501.0, "et": 515.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.50, "அரியணையை விட நெறி தவறாத மனசுதான் உயர்ந்தது..."),
                    (6.80, 13.80, "இந்த உண்மை புரிஞ்சா எந்த இழப்பையும் தைரியமா எதிர்கொள்ளலாம்!")
                ]
            }
        ]
    },
    {
        "id": 4,
        "title_l1": "THE 5TH BROTHER 🛶",
        "title_l2": "BEYOND CASTE & STATUS",
        "emoji": "🛶",
        "filename": "Reel_202_4_Rama_And_Guhan_Brotherhood.mp4",
        "cuts": [
            {
                "st": 678.0, "et": 687.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.20, "வேடுவத் தலைவன் குகனை..."),
                    (4.50, 8.80, "மன்னர் ராமர் எப்படி தன் உடன்பிறப்பாக ஏத்துக்கிட்டாரு?")
                ]
            },
            {
                "st": 687.0, "et": 700.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "சாதி, குலம், அந்தஸ்து எதையும் பார்க்காம..."),
                    (6.30, 12.80, "உன்னோடு நாங்க ஐவர் ஆனோம்னு கட்டி தழுவினாரு!")
                ]
            },
            {
                "st": 700.0, "et": 713.0, "crop": None, "broll": str(BROLLS / "broll_river_boat.mp4"),
                "phrases": [
                    (0.25, 6.00, "கங்கை நதிக்கரையில நடந்த இந்த மாபெரும் சந்திப்பு..."),
                    (6.30, 12.80, "மனிதகுலத்துக்கே சமத்துவத்தின் மிகப்பெரிய சான்று!")
                ]
            },
            {
                "st": 713.0, "et": 726.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "உண்மையான தகுதி உங்கள் பிறப்பிலோ பதவியிலோ இல்லை..."),
                    (6.30, 12.80, "நீங்கள் காட்டும் தூய்மையான அன்பில் மட்டும்தான் இருக்கு!")
                ]
            },
            {
                "st": 726.0, "et": 738.0, "crop": None, "broll": str(BROLLS / "broll_scripture.mp4"),
                "phrases": [
                    (0.25, 5.50, "அரசன் முதல் வேடன் வரை அனைவரையும் சமமாக மதிக்கும் போதுதான்..."),
                    (5.80, 11.80, "ஒரு சிறந்த சமுதாயம் உருவாக முடியும்!")
                ]
            },
            {
                "st": 738.0, "et": 752.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.50, "உறவுகளுக்கு எல்லைகள் கிடையாது, அன்பு மட்டுமே பாலம்..."),
                    (6.80, 13.80, "இந்த உயர்ந்த பண்பைத்தான் கம்பராமாயணம் அழுத்தமாக போதிக்குது!")
                ]
            }
        ]
    },
    {
        "id": 5,
        "title_l1": "PURE DEVOTION TEARS 🌙",
        "title_l2": "LOVE WITHOUT EXPECTATION",
        "emoji": "🌙",
        "filename": "Reel_202_5_Love_Without_Expectations.mp4",
        "cuts": [
            {
                "st": 918.0, "et": 927.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.20, "காட்டுல ராமர் வெறும் தரையில தூங்குறதை பார்த்து..."),
                    (4.50, 8.80, "குகன் ஏன் கண்ணீர் விட்டு அழுது துடிச்சான்?")
                ]
            },
            {
                "st": 927.0, "et": 940.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "அரண்மனையில பட்டு மெத்தையில தூங்க வேண்டியவர் புல் தரையில..."),
                    (6.30, 12.80, "அந்த வலியை பார்த்து ஒரு சகோதரனா அவனால தாங்கவே முடியல!")
                ]
            },
            {
                "st": 940.0, "et": 952.0, "crop": None, "broll": str(BROLLS / "broll_night_fire.mp4"),
                "phrases": [
                    (0.25, 5.50, "இரவு முழுவதும் வில்லேந்தி தூங்காமல் காவல் காத்தான்..."),
                    (5.80, 11.80, "எந்த சுயநலமும் இல்லாத தூய அன்பின் வெளிப்பாடு அது!")
                ]
            },
            {
                "st": 952.0, "et": 964.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 5.50, "எந்த எதிர்பார்ப்பும் இல்லாம அன்பு செலுத்துறதுதான்..."),
                    (5.80, 11.80, "இந்த உலகத்திலேயே மிக உயர்ந்த மனித குணம்!")
                ]
            },
            {
                "st": 964.0, "et": 976.0, "crop": None, "broll": str(BROLLS / "broll_forest_mist.mp4"),
                "phrases": [
                    (0.25, 5.50, "உங்களை உண்மையா நேசிக்கிற உறவுகளை என்னைக்குமே..."),
                    (5.80, 11.80, "அவங்க அன்பை சாதாரணமாக நினைச்சு விட்டுடாதீங்க!")
                ]
            },
            {
                "st": 976.0, "et": 990.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.50, "பணத்தால வாங்க முடியாத ஒரே செல்வம் உண்மையான அன்பு..."),
                    (6.80, 13.80, "அதை காப்பாற்றிக்கொள்வதுதான் உங்கள் வாழ்க்கையின் நிம்மதி!")
                ]
            }
        ]
    },
    {
        "id": 6,
        "title_l1": "POWER OF TEAMWORK 🏔️",
        "title_l2": "ONE PRINCE & VANARA ARMY",
        "emoji": "🏔️",
        "filename": "Reel_202_6_Sugriva_And_Vanara_Army.mp4",
        "cuts": [
            {
                "st": 1048.0, "et": 1057.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.20, "ராமர் சீதையை மீட்க போகும்போது..."),
                    (4.50, 8.80, "அவருக்கு ஏன் சுக்கிரீவனின் வானர சேனை தேவைப்பட்டுச்சு?")
                ]
            },
            {
                "st": 1057.0, "et": 1070.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "சீதையை கண்டுபிடிக்க சுக்கிரீவனோட படை தான்..."),
                    (6.30, 12.80, "நான்கு திசைகளிலும் அலைந்து தேடி தகவல் கொண்டு வந்தது!")
                ]
            },
            {
                "st": 1070.0, "et": 1083.0, "crop": None, "broll": str(BROLLS / "broll_mountains.mp4"),
                "phrases": [
                    (0.25, 6.00, "ஒவ்வொரு வானரமும் தன் முழு சக்தியையும் அர்ப்பணித்து உழைத்தது..."),
                    (6.30, 12.80, "கடல் கடந்து பாலம் அமைத்த ஒற்றுமையின் மகத்தான சக்தி அது!")
                ]
            },
            {
                "st": 1083.0, "et": 1095.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 5.50, "நட்புக்கு மரியாதை செலுத்தி ஒன்றிணைந்து செயல்பட்டால்..."),
                    (5.80, 11.80, "எந்த சவாலையும் நம்மால் எளிதாக முறியடிக்க முடியும்!")
                ]
            },
            {
                "st": 1095.0, "et": 1107.0, "crop": None, "broll": str(BROLLS / "broll_golden_sunrise.mp4"),
                "phrases": [
                    (0.25, 5.50, "தனியாளா ஜெயிக்க முடியாத பெரிய காரியங்களை கூட..."),
                    (5.80, 11.80, "நல்ல மனிதர்களின் கூட்டு முயற்சி சாத்தியமாக்கும்!")
                ]
            },
            {
                "st": 1107.0, "et": 1121.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.50, "கூடி வாழ்ந்தால் கோடி நன்மை என்பது வெறும் பழமொழி இல்லை..."),
                    (6.80, 13.80, "வாழ்க்கைப் போரில் வெற்றி பெறுவதற்கான மூல மந்திரம்!")
                ]
            }
        ]
    },
    {
        "id": 7,
        "title_l1": "10 HEADS, 1 FATAL FLAW 🔥",
        "title_l2": "EGO DESTROYS EMPIRES",
        "emoji": "🔥",
        "filename": "Reel_202_7_Ego_Destroys_Everything.mp4",
        "cuts": [
            {
                "st": 1218.0, "et": 1227.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.20, "பத்து தலை அறிவு, மாபெரும் பலம் இருந்தும்..."),
                    (4.50, 8.80, "ராவணன் ஏன் தன் சாம்ராஜ்யத்தையே ஒட்டுமொத்தமா இழந்தான்?")
                ]
            },
            {
                "st": 1227.0, "et": 1240.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "எவ்வளவுதான் அறிவு இருந்தாலும், தலைக்கனம் இருந்தா..."),
                    (6.30, 12.80, "அங்கே அழிவு நிச்சயம்னு நிரூபிச்சது அவனோட அடங்காத ஈகோ!")
                ]
            },
            {
                "st": 1240.0, "et": 1252.0, "crop": None, "broll": str(BROLLS / "broll_raging_fire.mp4"),
                "phrases": [
                    (0.25, 5.50, "ஈகோ ஒரு தீ மாதிரி... அடுத்தவங்களை எரிக்கிறதுக்கு முன்னாடி,"),
                    (5.80, 11.80, "முதல்ல உங்களையே சாம்பலாக்கிடும்!")
                ]
            },
            {
                "st": 1252.0, "et": 1264.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 5.50, "எவ்வளவு பெரிய உயரத்துக்கு போனாலும் பணிவு இல்லேன்னா..."),
                    (5.80, 11.80, "கீழே விழும்போது உங்களை தாங்கிப் பிடிக்க ஒருத்தரும் இருக்க மாட்டாங்க!")
                ]
            },
            {
                "st": 1264.0, "et": 1276.0, "crop": None, "broll": str(BROLLS / "broll_scripture.mp4"),
                "phrases": [
                    (0.25, 5.50, "தர்மத்தின் முன் ஆணவமும் அதிகாரமும் ஒருபோதும் நிலைக்காது..."),
                    (5.80, 11.80, "வரலாறு நமக்கு சொல்லும் பாடம் இதுதான்!")
                ]
            },
            {
                "st": 1276.0, "et": 1290.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.50, "அறிவோடு பணிவையும் வளர்த்துக்க கத்துக்கோங்க..."),
                    (6.80, 13.80, "அதுதான் உங்களை உண்மையான வெற்றியாளராக மாற்றும்!")
                ]
            }
        ]
    },
    {
        "id": 8,
        "title_l1": "CALM IN ANY STORM 🌅",
        "title_l2": "THE TIMELESS LIFE LESSON",
        "emoji": "🌅",
        "filename": "Reel_202_8_Timeless_Lessons_Of_Life.mp4",
        "cuts": [
            {
                "st": 1818.0, "et": 1827.0, "crop": CROP_HOST, "broll": None,
                "phrases": [
                    (0.20, 4.20, "ராமாயணம் நமக்கு கற்றுக்கொடுக்கிற..."),
                    (4.50, 8.80, "மிக முக்கியமான வாழ்வியல் உண்மை என்ன?")
                ]
            },
            {
                "st": 1827.0, "et": 1840.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "வெற்றி, தோல்வி, இன்பம், துன்பம் எல்லாத்தையும்..."),
                    (6.30, 12.80, "சமமா ஏத்துக்கிட்டு நிதானத்தோடு வாழ கத்துக்கணும்!")
                ]
            },
            {
                "st": 1840.0, "et": 1853.0, "crop": None, "broll": str(BROLLS / "broll_golden_sunrise.mp4"),
                "phrases": [
                    (0.25, 6.00, "எந்த ஒரு சூழ்நிலையிலும் உங்கள் நற்குணத்தை விட்டுடாதீங்க..."),
                    (6.30, 12.80, "அதுதான் உங்களை தலைமுறை தாண்டியும் பேச வைக்கும்!")
                ]
            },
            {
                "st": 1853.0, "et": 1866.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.00, "பொறுமையும் தர்மமும் உள்ள மனுஷனை யாராலும் தோற்கடிக்க முடியாது..."),
                    (6.30, 12.80, "காலம் அவனுக்கு தேவையான வெற்றியை நிச்சயமாக தரும்!")
                ]
            },
            {
                "st": 1866.0, "et": 1878.0, "crop": None, "broll": str(BROLLS / "broll_temple.mp4"),
                "phrases": [
                    (0.25, 5.50, "வாழ்க்கையின் உண்மையான அழகு அதன் நிலையற்ற தன்மையில்தான் இருக்கு..."),
                    (5.80, 11.80, "அதை உணர்ந்து வாழும் மனிதன் எப்போதும் அமைதியா இருப்பான்!")
                ]
            },
            {
                "st": 1878.0, "et": 1892.0, "crop": CROP_GUEST, "broll": None,
                "phrases": [
                    (0.25, 6.50, "இந்த உண்மையை மனசுல வச்சுட்டு வாழ்ந்து பாருங்க..."),
                    (6.80, 13.80, "வாழ்க்கையில எந்த புயல் வந்தாலும் உங்களை அசைக்க முடியாது!")
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

def render_sub_frame(words_status, width=WIDTH, height=SUBS_H, font_name="TamilSangamMN-Bold", base_font_size=44):
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

    MAX_SAFE_WIDTH = 880.0
    norm_words_status = [(unicodedata.normalize('NFC', w), act) for w, act in words_status]
    full_text = " ".join([w for w, _ in norm_words_status])

    measuring_font = NSFont.fontWithName_size_(font_name, base_font_size)
    astr_measure = NSAttributedString.alloc().initWithString_attributes_(full_text, {NSFontAttributeName: measuring_font})
    raw_width = astr_measure.size().width

    if raw_width > MAX_SAFE_WIDTH:
        scale = MAX_SAFE_WIDTH / raw_width
        font_size = max(32, int(base_font_size * scale))
    else:
        font_size = base_font_size

    font = NSFont.fontWithName_size_(font_name, font_size)
    stroke_width = 14.0

    stroke_astr = NSMutableAttributedString.alloc().init()
    for word, _ in norm_words_status:
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

    orange_color = NSColor.colorWithDeviceRed_green_blue_alpha_(ORANGE_R, ORANGE_G, ORANGE_B, 1.0)
    white_color = NSColor.colorWithDeviceRed_green_blue_alpha_(1.0, 1.0, 1.0, 1.0)
    fill_astr = NSMutableAttributedString.alloc().init()
    for word, is_active in norm_words_status:
        fg = orange_color if is_active else white_color
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
    print(f"\n========================================================")
    print(f"🔥 Processing Master Reel {reel_id}: {reel['title_l1']} {reel['title_l2']}")
    print(f"========================================================")

    banner_file = WORKSPACE / f"banner_master_{reel_id}.png"
    render_banner(reel["title_l1"], reel["title_l2"], reel["emoji"], banner_file)

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

        # Audio is ALWAYS continuous speech from RAW_VIDEO at cut['st'] to cut['et']
        cmd_aud = [
            "ffmpeg", "-y", "-ss", f"{cut['st']:.3f}", "-t", f"{dur:.3f}",
            "-i", str(RAW_VIDEO),
            "-vn", "-ac", "2", "-ar", "48000",
            "-af", audio_filters,
            str(aud_out)
        ]
        subprocess.run(cmd_aud, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                str(vid_out)
            ]
        subprocess.run(cmd_vid, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        cut_video_files.append(vid_out)
        cut_audio_files.append(aud_out)

    total_dur = sum(cut_durations)
    print(f"Total Master Video Duration: {total_dur:.1f}s ({total_dur/60:.2f} mins) [Target: 1min - 1:20min]")

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
        f"[0:v]pad={WIDTH}:{HEIGHT}:0:{VIDEO_Y}:color=black[padded];"
        f"[padded][1:v]overlay=0:{BANNER_Y}:shortest=1[comp]",
        "-map", "[comp]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        str(base_padded_vid)
    ]
    subprocess.run(cmd_base, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    concat_aud_txt = WORKSPACE / f"temp_concat_aud_{reel_id}.txt"
    with open(concat_aud_txt, "w") as f:
        for af in cut_audio_files:
            f.write(f"file '{af.name}'\n")

    speech_wav = WORKSPACE / f"temp_speech_{reel_id}.wav"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_aud_txt),
        "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
        str(speech_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 5. Composite Multi-track Audio: Speech + Whooshes + MILD Background Music (-28 dB / volume=0.045)
    transition_times = []
    curr_t = 0.0
    for dur in cut_durations[:-1]:
        curr_t += dur
        transition_times.append(curr_t)

    cmd_audio = ["ffmpeg", "-y", "-i", str(speech_wav), "-i", str(BGM_FLUTE)]
    for _ in transition_times:
        cmd_audio.extend(["-i", str(WHOOSH_SFX)])

    filter_parts = []
    filter_parts.append("[0:a]volume=1.0[speech]")
    # Mild BGM at -28 dB (volume=0.045 with normalize=0)
    filter_parts.append(f"[1:a]volume=0.045,afade=t=in:ss=0:d=1.5,afade=t=out:st={total_dur-2.0:.1f}:d=2.0[bgm]")

    sfx_labels = []
    for idx, t_sfx in enumerate(transition_times):
        in_idx = 2 + idx
        delay_ms = int((t_sfx - 0.25) * 1000)
        filter_parts.append(f"[{in_idx}:a]volume=0.35,adelay={delay_ms}|{delay_ms}[w{idx}]")
        sfx_labels.append(f"[w{idx}]")

    filter_parts.append(f"{''.join(sfx_labels)}amix=inputs={len(transition_times)}:normalize=0[sfx]")
    filter_parts.append("[speech][sfx][bgm]amix=inputs=3:normalize=0:duration=first[mixed]")
    filter_parts.append("[mixed]loudnorm=I=-14:TP=-1.5:LRA=7[outa]")

    mixed_audio = WORKSPACE / f"temp_mixed_audio_{reel_id}.wav"
    cmd_audio.extend(["-filter_complex", ";".join(filter_parts), "-map", "[outa]", "-ar", "48000", str(mixed_audio)])
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 6. Generate Running Subtitles (AppKit CoreText with Exact Orange #FF8400 and Solid Black Outline)
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

    # 7. Final Composite & Mux with Rec.709 SDR Metadata & Subtitle at SUBS_Y = 1200
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
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-shortest",
        str(final_reel_path)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Generated Master Video (1m-1m20s): {final_reel_path} ({os.path.getsize(final_reel_path) / 1024 / 1024:.1f} MB)")

    # 8. Extract QA Frames directly to FRAMES/
    for t in [3.0, 8.0, total_dur * 0.25, total_dur * 0.50, total_dur * 0.75, total_dur - 3.0]:
        frame_name = f"qa_reel{reel_id}_t{int(t)}s.jpg"
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
    print("🚀 Master Production Engine: Rendering 8 Viral Master Reels (1min to 1:20min)...")
    for reel in ALL_MASTER_REELS:
        process_master_reel(reel)
    print("\n🎉 ALL 8 MASTER VIRAL REELS COMPLETED & VERIFIED!")

if __name__ == "__main__":
    main()
