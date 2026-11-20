import subprocess
from PIL import Image
import numpy as np

# Sample every 1s from relationship reel part 4.mp4
ref = "STYLE REFERENCE/relationship reel part 4.mp4"
for sec in range(0, 45, 1):
    subprocess.run(["ffmpeg", "-y", "-ss", str(sec), "-i", ref, "-vframes", "1", "-q:v", "3", "test_frame.jpg"], capture_output=True)
    im = Image.open("test_frame.jpg")
    arr = np.array(im)[558:1498, :] # 1080x940 video window
    
    # Podcast studio has specific mean color and std
    # Check if this frame is B-roll or Studio
    mean_rgb = arr.mean(axis=(0,1))
    # studio podcast frame has mean around [150..170, 120..140, 100..120]
    is_studio = (140 < mean_rgb[0] < 175) and (110 < mean_rgb[1] < 145) and (95 < mean_rgb[2] < 125)
    print(f"t={sec:02d}s: Studio={is_studio} | RGB={mean_rgb[:3].astype(int)}")
