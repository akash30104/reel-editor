import subprocess
import os

# Let's inspect the cuts in relationship reel part 4.mp4
# In relationship reel part 4:
# Talking head has speakers at desk.
# B-roll cuts are movie clips, couples, drama, etc.
# Let's find timestamps where B-roll appears!

for ref in ['relationship reel part 4.mp4', 'relationship reel part 8.mp4', 'Career vs Relationship 1 (1).mp4']:
    print(f"=== Scanning {ref} ===")
    # let's extract 1 frame every 2 seconds
    dur_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', f'STYLE REFERENCE/{ref}']
    dur = float(subprocess.run(dur_cmd, capture_output=True, text=True).stdout.strip())
    print(f"Duration: {dur:.2f}s")
