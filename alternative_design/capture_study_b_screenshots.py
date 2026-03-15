#!/usr/bin/env python3
"""Capture Study B via lossless screenshots stitched into a GIF.
Same 2048x1024 viewport + same crop as the current banner.
Produces higher quality than Playwright video recording.
"""
import subprocess, os, sys, glob, shutil

# ── CONFIG ──────────────────────────────────────────────────────
WIDTH = 2048
HEIGHT = 1024
FPS = 50
LOOP_DUR = 4.5
TOTAL_FRAMES = int(FPS * LOOP_DUR)  # 225 frames
FRAME_INTERVAL_MS = int(1000 / FPS)  # 20ms per frame
WARMUP_MS = 3000
CROP_LEFT = 0.14
CROP_RIGHT = 0.164
CROP_TOP = 0.13
CROP_BOT = 0.13
CROP_W = int(WIDTH * (1 - CROP_LEFT - CROP_RIGHT))
CROP_H = int(HEIGHT * (1 - CROP_TOP - CROP_BOT))
CROP_X = int(WIDTH * CROP_LEFT)
CROP_Y = int(HEIGHT * CROP_TOP)
# ────────────────────────────────────────────────────────────────

DARK = "--dark" in sys.argv
VARIANT = "dark" if DARK else "light"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOCIAL = "--social" in sys.argv
if SOCIAL:
    HTML_FILE = "study_b_organic_bold_header_dark.html" if DARK else "study_b_organic_bold_header.html"
else:
    HTML_FILE = "study_b_organic_bold_dark.html" if DARK else "study_b_organic_bold.html"
HTML_PATH = os.path.join(SCRIPT_DIR, HTML_FILE)
if SOCIAL:
    os.makedirs(os.path.join(SCRIPT_DIR, "socials"), exist_ok=True)
    OUTPUT_GIF = os.path.join(SCRIPT_DIR, "socials", f"wdf_banner_social{'_dark' if DARK else '_light'}.gif")
else:
    OUTPUT_GIF = os.path.join(SCRIPT_DIR, f"study_b_organic_ss{'_dark' if DARK else ''}.gif")
FRAME_DIR = f"/tmp/wdf_frames_study_b_{VARIANT}"

# Clean frame dir
if os.path.exists(FRAME_DIR):
    shutil.rmtree(FRAME_DIR)
os.makedirs(FRAME_DIR)

print(f"Capturing {TOTAL_FRAMES} frames ({VARIANT}) at {WIDTH}x{HEIGHT}, {FPS}fps, {LOOP_DUR}s loop...")

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
    page.goto(f"file://{HTML_PATH}")
    page.wait_for_timeout(WARMUP_MS)

    # Hijack everything: stop rAF loop, pause CSS animations, expose manual frame control
    page.evaluate("""
    () => {
        // 1. Stop the rAF draw loop
        window._stopped = false;
        const origRAF = window.requestAnimationFrame;
        window.requestAnimationFrame = (cb) => {
            if (!window._stopped) return origRAF(cb);
        };
        window._stopped = true;

        // 2. Pause ALL CSS animations globally
        document.documentElement.style.setProperty('--anim-state', 'paused');
        document.getAnimations().forEach(a => a.pause());

        // 3. Store references to all CSS animations for seeking
        window._cssAnims = document.getAnimations();

        // 4. Expose function to render a precise frame
        window.drawAtTime = (elapsedSec) => {
            // Seek all CSS animations to the correct time
            const ms = elapsedSec * 1000;
            window._cssAnims.forEach(a => {
                if (a.effect && a.effect.getTiming) {
                    const dur = a.effect.getTiming().duration;
                    // Set currentTime modulo duration for looping anims
                    a.currentTime = ms % (dur || 1);
                }
            });

            // Draw canvas at exact time
            const fakeTs = (window._baseTs || performance.now()) + elapsedSec * 1000;
            if (!window._baseTs) window._baseTs = performance.now();
            if (typeof t0 !== 'undefined') t0 = window._baseTs;
            draw(fakeTs);
        };
    }
    """)

    for i in range(TOTAL_FRAMES):
        elapsed = (i / TOTAL_FRAMES) * LOOP_DUR
        page.evaluate(f"window.drawAtTime({elapsed})")
        path = os.path.join(FRAME_DIR, f"frame_{i:04d}.png")
        page.screenshot(path=path, type="png")
        if (i + 1) % 50 == 0 or i == TOTAL_FRAMES - 1:
            print(f"  Frame {i + 1}/{TOTAL_FRAMES}")

    page.close()
    browser.close()

print(f"All {TOTAL_FRAMES} frames captured. Generating GIF...")

palette = f"/tmp/wdf_palette_ss_{VARIANT}.png"

# Generate palette from all frames
subprocess.run([
    "ffmpeg", "-y", "-framerate", str(FPS),
    "-i", os.path.join(FRAME_DIR, "frame_%04d.png"),
    "-vf", f"crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y},palettegen=max_colors=256:stats_mode=diff",
    palette
], check=True, capture_output=True)

# Encode GIF
subprocess.run([
    "ffmpeg", "-y", "-framerate", str(FPS),
    "-i", os.path.join(FRAME_DIR, "frame_%04d.png"),
    "-i", palette,
    "-lavfi", f"crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y}[x];[x][1:v]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
    OUTPUT_GIF
], check=True, capture_output=True)

gif_size = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)
print(f"\nGIF created: {OUTPUT_GIF}")
print(f"Size: {gif_size:.1f} MB")
print(f"Dimensions: {CROP_W}x{CROP_H} (cropped from {WIDTH}x{HEIGHT})")
print(f"Framerate: {FPS}fps, Loop: {LOOP_DUR}s, Frames: {TOTAL_FRAMES}")
