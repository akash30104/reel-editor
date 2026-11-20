from PIL import Image, ImageDraw, ImageFont
import os

BASE_DIR = r"c:\Users\91861\Downloads\REEL EDITOR"
FONTS_DIR = os.path.join(BASE_DIR, "fonts")

# 1. Header Banner (1080x142, #EA8207, with Real PNG Emoji 💔)
banner = Image.new('RGBA', (1080, 142), (234, 130, 7, 255))
draw_b = ImageDraw.Draw(banner)
font_b = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 52)

text = 'Toxic Relationship? '
bbox = draw_b.textbbox((0, 0), text, font=font_b)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]

# Broken heart emoji
emoji = Image.open(os.path.join(BASE_DIR, 'emojis', 'broken_heart.png')).convert('RGBA')
emoji_size = 50
emoji = emoji.resize((emoji_size, emoji_size), Image.Resampling.LANCZOS)

total_w = tw + emoji_size + 10
start_x = (1080 - total_w) // 2
text_y = (142 - th) // 2 - 4
emoji_y = (142 - emoji_size) // 2

draw_b.text((start_x, text_y), text, fill=(0, 0, 0, 255), font=font_b)
banner.paste(emoji, (start_x + tw + 10, emoji_y), emoji)
banner_path = os.path.join(BASE_DIR, 'header_banner.png')
banner.save(banner_path)
print(f"Header banner with real emoji saved: {banner_path}")

# 2. Hook Badge for first 3 seconds (1080x1920 transparent overlay)
hook_overlay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
draw_h = ImageDraw.Draw(hook_overlay)

# Font for Tamil Hook
font_tamil_hook = ImageFont.truetype(os.path.join(FONTS_DIR, 'NotoSansTamil-Bold.ttf'), 44)
hook_text = "ஏன் பெண்கள் Toxic பசங்க மேல போறாங்க?"

# Pill badge coordinates inside the video window (y=558..1498)
# Position near top of video window: y=600..690
badge_h = 80
badge_w = 980
badge_x = (1080 - badge_w) // 2
badge_y = 590

# Draw dark semi-transparent card with orange border
draw_h.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)], radius=20, fill=(15, 15, 15, 230), outline=(234, 130, 7, 255), width=4)

# Fire emoji on left
fire_emoji = Image.open(os.path.join(BASE_DIR, 'emojis', 'fire.png')).convert('RGBA')
fire_size = 46
fire_emoji = fire_emoji.resize((fire_size, fire_size), Image.Resampling.LANCZOS)
hook_overlay.paste(fire_emoji, (badge_x + 25, badge_y + (badge_h - fire_size) // 2), fire_emoji)

# Broken heart emoji on right
heart_emoji = Image.open(os.path.join(BASE_DIR, 'emojis', 'broken_heart.png')).convert('RGBA')
heart_emoji = heart_emoji.resize((fire_size, fire_size), Image.Resampling.LANCZOS)
hook_overlay.paste(heart_emoji, (badge_x + badge_w - 25 - fire_size, badge_y + (badge_h - fire_size) // 2), heart_emoji)

# Center the Tamil text inside the badge
bbox_t = draw_h.textbbox((0, 0), hook_text, font=font_tamil_hook)
tw_h = bbox_t[2] - bbox_t[0]
th_h = bbox_t[3] - bbox_t[1]
tx_h = (1080 - tw_h) // 2
ty_h = badge_y + (badge_h - th_h) // 2 - 4

draw_h.text((tx_h, ty_h), hook_text, fill=(255, 255, 255, 255), font=font_tamil_hook)

hook_path = os.path.join(BASE_DIR, 'hook_badge.png')
hook_overlay.save(hook_path)
print(f"Hook badge saved: {hook_path}")
