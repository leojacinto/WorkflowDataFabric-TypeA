#!/usr/bin/env python3
"""Capture Study B organic textile banner as a GIF.
Fully deterministic 4.5s loop — record exact cycle for seamless GIF.
"""
import subprocess, os, sys, glob

# ── CONFIG ──────────────────────────────────────────────────────
WIDTH = 2048
HEIGHT = 1024
DURATION = 10         # total recording (includes warmup)
FPS = 50
CROP_LEFT = 0.14      # trim 14% from left
CROP_RIGHT = 0.164    # trim ~16.4% from right (another 20% of remaining space removed)
CROP_TOP = 0.13
CROP_BOT = 0.13
CROP_W = int(WIDTH * (1 - CROP_LEFT - CROP_RIGHT))
CROP_H = int(HEIGHT * (1 - CROP_TOP - CROP_BOT))
CROP_X = int(WIDTH * CROP_LEFT)
CROP_Y = int(HEIGHT * CROP_TOP)
TRIM_START = 3
LOOP_DUR = 4.5        # exact animation cycle for perfect loop
# ────────────────────────────────────────────────────────────────

DARK = "--dark" in sys.argv
VARIANT = "dark" if DARK else "light"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = "study_b_organic_dark.html" if DARK else "study_b_organic.html"
HTML_PATH = os.path.join(SCRIPT_DIR, HTML_FILE)
OUTPUT_GIF = os.path.join(SCRIPT_DIR, f"study_b_organic{'_dark' if DARK else ''}.gif")
VIDEO_DIR = f"/tmp/wdf_banner_study_b_{VARIANT}"

os.makedirs(VIDEO_DIR, exist_ok=True)
for f in glob.glob(os.path.join(VIDEO_DIR, "*.webm")):
    os.remove(f)

print(f"Recording Study B ({VARIANT}): {WIDTH}x{HEIGHT}...")

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

palette = "/tmp/wdf_palette_study_b.png"

print(f"Generating palette at {FPS}fps (trimming first {TRIM_START}s, {LOOP_DUR}s loop)...")
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
print(f"\nGIF created: {OUTPUT_GIF}")
print(f"Size: {gif_size:.1f} MB")
print(f"Dimensions: {CROP_W}x{CROP_H} (cropped from {WIDTH}x{HEIGHT})")
print(f"Framerate: {FPS}fps, Loop: {LOOP_DUR}s")
