import urllib.request
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

categories = {
    'fish': 'https://mixkit.co/free-stock-video/fish/',
    'japan': 'https://mixkit.co/free-stock-video/tokyo/',
    'stress': 'https://mixkit.co/free-stock-video/stress/',
    'business': 'https://mixkit.co/free-stock-video/business/',
}

found_urls = {}
for cat, url in categories.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'https://assets\.mixkit\.co/videos/[^\"]+\.mp4', html)
            unique = list(dict.fromkeys(matches))
            print(f"Category '{cat}': found {len(unique)} MP4 URLs")
            if unique:
                found_urls[cat] = unique[0]
                print(f"  Sample: {unique[0]}")
    except Exception as e:
        print(f"Error on {cat}: {e}")

print("\n=== DOWNLOADING 4 INTERNET B-ROLLS ===")
os.makedirs("internet_brolls", exist_ok=True)
for cat, vurl in found_urls.items():
    out_file = os.path.join("internet_brolls", f"broll_{cat}.mp4")
    print(f"Downloading {cat} from {vurl}...")
    req = urllib.request.Request(vurl, headers=headers)
    with urllib.request.urlopen(req) as resp, open(out_file, "wb") as f:
        f.write(resp.read())
    size = os.path.getsize(out_file)
    print(f"Saved {out_file} ({size / 1024 / 1024:.2f} MB)")
