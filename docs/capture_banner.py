#!/usr/bin/env python3
"""
Capture the WDF banner animation as a high-quality GIF.
Uses Playwright video recording + ffmpeg.

Usage:
  python3 docs/capture_banner.py          # light version
  python3 docs/capture_banner.py --dark   # dark version
"""
import subprocess, os, sys, glob

# ── CONFIG ──────────────────────────────────────────────────────
WIDTH = 2048          # viewport width (HTML scales via vw units)
HEIGHT = 1024         # viewport height (scene aspect-ratio 2:1)
DURATION = 12         # seconds to record
FPS = 50              # GIF framerate (50fps = max practical, GIF min delay = 20ms)
CROP_PCT = 0.12       # trim 12% from left/right edges
CROP_TOP = 0.135      # trim 13.5% from top
CROP_BOT = 0.13       # trim 13% from bottom
CROP_W = int(WIDTH * (1 - 2 * CROP_PCT))
CROP_H = int(HEIGHT * (1 - CROP_TOP - CROP_BOT))
CROP_X = int(WIDTH * CROP_PCT)
CROP_Y = int(HEIGHT * CROP_TOP)
TRIM_START = 3
LOOP_DUR = 9          # 2 full breathe cycles (4.5s each) for seamless loop
# ────────────────────────────────────────────────────────

DARK = "--dark" in sys.argv
VARIANT = "dark" if DARK else "light"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = "wdf-connectors_banner_dark.html" if DARK else "wdf-connectors_banner.html"
HTML_PATH = os.path.join(SCRIPT_DIR, HTML_FILE)
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
GIF_NAME = "wdf_connectors_banner_dark.gif" if DARK else "wdf_connectors_banner.gif"
OUTPUT_GIF = os.path.join(REPO_ROOT, ".gitbook", "assets", GIF_NAME)
VIDEO_DIR = f"/tmp/wdf_banner_capture_{VARIANT}"

os.makedirs(VIDEO_DIR, exist_ok=True)
for f in glob.glob(os.path.join(VIDEO_DIR, "*.webm")):
    os.remove(f)

print(f"Recording {VARIANT} banner: {WIDTH}x{HEIGHT}...")

# ── RECORD VIDEO ────────────────────────────────────────
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": WIDTH, "height": HEIGHT},
        device_scale_factor=1,
        record_video_dir=VIDEO_DIR,
        record_video_size={"width": WIDTH, "height": HEIGHT},
    )
    page = context.new_page()
    page.goto(f"file://{HTML_PATH}")
    page.wait_for_timeout(2000)
    page.wait_for_timeout(DURATION * 1000)
    page.close()
    context.close()
    browser.close()

videos = glob.glob(os.path.join(VIDEO_DIR, "*.webm"))
if not videos:
    print("ERROR: No video recorded!")
    sys.exit(1)

video_path = videos[0]
print(f"Video recorded: {video_path} ({os.path.getsize(video_path)/(1024*1024):.1f} MB)")

# ── CONVERT TO GIF ─────────────────────────────────────
palette = f"/tmp/wdf_palette_{VARIANT}.png"

print(f"Generating palette at {FPS}fps (trimming first {TRIM_START}s)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", str(TRIM_START), "-t", str(LOOP_DUR), "-i", video_path,
    "-vf", f"crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y},fps={FPS},palettegen=max_colors=256:stats_mode=diff",
    palette
], check=True, capture_output=True)

print("Encoding GIF...")
subprocess.run([
    "ffmpeg", "-y", "-ss", str(TRIM_START), "-t", str(LOOP_DUR), "-i", video_path,
    "-i", palette,
    "-lavfi", f"crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y},fps={FPS}[x];[x][1:v]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
    OUTPUT_GIF
], check=True, capture_output=True)

gif_size = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)
print(f"\n{VARIANT.upper()} GIF created: {OUTPUT_GIF}")
print(f"Size: {gif_size:.1f} MB")
print(f"Dimensions: {CROP_W}x{CROP_H} (cropped from {WIDTH}x{HEIGHT})")
print(f"Framerate: {FPS}fps")

if gif_size > 25:
    print(f"\nWARNING: GIF is {gif_size:.0f}MB - consider reducing FPS or duration")
