#!/usr/bin/env python3
"""
Capture the WDF banner animation as a high-quality GIF.
Uses Playwright for recording and ffmpeg for GIF conversion.
"""
import subprocess, os, sys, time, glob

# ── CONFIG ──────────────────────────────────────────────
WIDTH = 1440          # 2x retina for crisp display at 730px GitBook width
ASPECT = 16 / 9
HEIGHT = int(WIDTH / ASPECT)  # 810
DURATION = 8          # seconds to record
FPS = 50              # max practical GIF framerate (GIF minimum delay = 20ms)
# ────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(SCRIPT_DIR, "wdf-connectors_banner.html")
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_GIF = os.path.join(REPO_ROOT, ".gitbook", "assets", "wdf_connectors_banner.gif")
VIDEO_DIR = "/tmp/wdf_banner_capture"

os.makedirs(VIDEO_DIR, exist_ok=True)

# Clean old captures
for f in glob.glob(os.path.join(VIDEO_DIR, "*.webm")):
    os.remove(f)

print(f"Recording {WIDTH}x{HEIGHT} for {DURATION}s...")

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
    # Wait for animations to be visible
    page.wait_for_timeout(2000)
    # Record for the full duration
    page.wait_for_timeout(DURATION * 1000)
    # Close to flush the video
    page.close()
    context.close()
    browser.close()

# Find video file
videos = glob.glob(os.path.join(VIDEO_DIR, "*.webm"))
if not videos:
    print("ERROR: No video recorded!")
    sys.exit(1)

video_path = videos[0]
video_size = os.path.getsize(video_path) / (1024 * 1024)
print(f"Video recorded: {video_path} ({video_size:.1f} MB)")

# ── CONVERT TO GIF ─────────────────────────────────────
# Two-pass palette generation for maximum quality
palette = "/tmp/wdf_palette.png"

print(f"Generating palette at {FPS}fps...")
subprocess.run([
    "ffmpeg", "-y", "-i", video_path,
    "-vf", f"fps={FPS},scale={WIDTH}:-1:flags=lanczos,palettegen=max_colors=256:stats_mode=diff",
    palette
], check=True, capture_output=True)

print("Encoding GIF...")
subprocess.run([
    "ffmpeg", "-y", "-i", video_path,
    "-i", palette,
    "-lavfi", f"fps={FPS},scale={WIDTH}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
    OUTPUT_GIF
], check=True, capture_output=True)

gif_size = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)
print(f"\nGIF created: {OUTPUT_GIF}")
print(f"Size: {gif_size:.1f} MB")
print(f"Dimensions: {WIDTH}x{HEIGHT}")
print(f"Framerate: {FPS}fps")

if gif_size > 25:
    print(f"\nWARNING: GIF is {gif_size:.0f}MB - consider reducing FPS or duration")
