#!/usr/bin/env python3
"""Capture Study B organic textile banner as a hi-res GIF.
Uses device_scale_factor=2 for 4096x2048 actual pixels
with identical 2048x1024 logical layout — no viewport changes.
"""
import subprocess, os, sys, glob

# ── CONFIG ──────────────────────────────────────────────────────
# Larger viewport — HTML uses vw units so layout scales cleanly
WIDTH = 3200
HEIGHT = 1600
DURATION = 10
FPS = 50
CROP_LEFT = 0.14
CROP_RIGHT = 0.164
CROP_TOP = 0.13
CROP_BOT = 0.13
CROP_W = int(WIDTH * (1 - CROP_LEFT - CROP_RIGHT))
CROP_H = int(HEIGHT * (1 - CROP_TOP - CROP_BOT))
CROP_X = int(WIDTH * CROP_LEFT)
CROP_Y = int(HEIGHT * CROP_TOP)
TRIM_START = 3
LOOP_DUR = 4.5
# ────────────────────────────────────────────────────────────────

DARK = "--dark" in sys.argv
VARIANT = "dark" if DARK else "light"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = "study_b_organic_dark.html" if DARK else "study_b_organic.html"
HTML_PATH = os.path.join(SCRIPT_DIR, HTML_FILE)
OUTPUT_GIF = os.path.join(SCRIPT_DIR, f"study_b_organic_hires{'_dark' if DARK else ''}.gif")
VIDEO_DIR = f"/tmp/wdf_banner_study_b_hires_{VARIANT}"

os.makedirs(VIDEO_DIR, exist_ok=True)
for f in glob.glob(os.path.join(VIDEO_DIR, "*.webm")):
    os.remove(f)

print(f"Recording Study B hi-res ({VARIANT}): {WIDTH}x{HEIGHT}...")

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
print(f"Video: {video_path} ({os.path.getsize(video_path)/(1024*1024):.1f} MB)")

palette = f"/tmp/wdf_palette_study_b_hires_{VARIANT}.png"

print(f"Generating palette at {FPS}fps (trim {TRIM_START}s, {LOOP_DUR}s loop)...")
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
print(f"\nHi-res GIF created: {OUTPUT_GIF}")
print(f"Size: {gif_size:.1f} MB")
print(f"Dimensions: {CROP_W}x{CROP_H} (cropped from {WIDTH}x{HEIGHT})")
print(f"Framerate: {FPS}fps, Loop: {LOOP_DUR}s")
