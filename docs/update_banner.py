#!/usr/bin/env python3
"""Update banner HTML: embed real logo, fix aspect ratio, tighten layout."""
import base64, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load logo as base64
with open("/Users/leo.francia/Downloads/Servicenow_icon.png", "rb") as f:
    logo_b64 = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"

html = open(os.path.join(SCRIPT_DIR, "wdf-connectors_banner.html")).read()

# 1. Fix aspect ratio: 16/9 → 7/2 (3.5:1)
html = html.replace("aspect-ratio: 16 / 9", "aspect-ratio: 7 / 2")
html = html.replace("min-width: 580px", "min-width: 400px")

# 2. Replace hub-icon CSS: svg fill → img sizing
html = html.replace(
    """  .hub-icon svg {
    width: clamp(54px, 5.8vw, 80px);
    height: clamp(54px, 5.8vw, 80px);
    fill: var(--now-green);
    stroke: none;
  }""",
    """  .hub-icon img {
    width: clamp(40px, 5vw, 65px);
    height: clamp(40px, 5vw, 65px);
    object-fit: contain;
  }"""
)

# 3. Shrink hub circle for shorter banner
html = html.replace(
    "width: clamp(260px, 30vw, 420px);\n    height: clamp(260px, 30vw, 420px);",
    "width: clamp(160px, 22vw, 260px);\n    height: clamp(160px, 22vw, 260px);"
)

# 4. Shrink hub text
html = html.replace(
    "font-size: clamp(1.5rem, 2.4vw, 2.3rem);",
    "font-size: clamp(1rem, 1.6vw, 1.5rem);"
)
html = html.replace(
    """  .hub-sub {
    font-family: var(--mono);
    font-size: clamp(0.65rem, 0.9vw, 0.9rem);""",
    """  .hub-sub {
    font-family: var(--mono);
    font-size: clamp(0.45rem, 0.6vw, 0.65rem);"""
)

# 5. Nodes: tighter layout, 2-column grid
html = html.replace(
    """  .nodes {
    position: absolute;
    right: 5%;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: clamp(0.35rem, 0.7vw, 0.65rem);
    z-index: 20;
  }""",
    """  .nodes {
    position: absolute;
    right: 4%;
    top: 50%;
    transform: translateY(-50%);
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: clamp(0.25rem, 0.45vw, 0.4rem);
    z-index: 20;
  }"""
)

# 6. Nodes: smaller cards
html = html.replace(
    "padding: clamp(0.35rem, 0.65vw, 0.6rem) clamp(0.55rem, 0.9vw, 1rem) clamp(0.35rem, 0.65vw, 0.6rem) clamp(0.45rem, 0.7vw, 0.75rem);",
    "padding: clamp(0.25rem, 0.4vw, 0.4rem) clamp(0.4rem, 0.6vw, 0.7rem) clamp(0.25rem, 0.4vw, 0.4rem) clamp(0.35rem, 0.5vw, 0.55rem);"
)
html = html.replace(
    "min-width: clamp(155px, 16vw, 220px);",
    "min-width: clamp(110px, 12vw, 160px);"
)

# 7. Node icon smaller
html = html.replace(
    """  .node-icon {
    width: clamp(22px, 2.4vw, 32px);
    height: clamp(22px, 2.4vw, 32px);""",
    """  .node-icon {
    width: clamp(18px, 1.8vw, 24px);
    height: clamp(18px, 1.8vw, 24px);"""
)

# 8. Node text smaller
html = html.replace(
    "font-size: clamp(0.6rem, 0.78vw, 0.78rem);",
    "font-size: clamp(0.48rem, 0.6vw, 0.62rem);"
)
html = html.replace(
    "font-size: clamp(0.34rem, 0.42vw, 0.42rem);",
    "font-size: clamp(0.28rem, 0.34vw, 0.34rem);"
)

# 9. Node pip smaller
html = html.replace(
    "width: 5px; height: 5px;",
    "width: 4px; height: 4px;"
)

# 10. Badge smaller
html = html.replace(
    "font-size: clamp(0.38rem, 0.5vw, 0.5rem);",
    "font-size: clamp(0.3rem, 0.38vw, 0.4rem);"
)

# 11. Orbit ring tighter
html = html.replace("inset: -20px;", "inset: -12px;")

# 12. Move hub closer to center
html = html.replace(
    """  .hub {
    position: absolute;
    left: 8%;""",
    """  .hub {
    position: absolute;
    left: 12%;"""
)

# 13. Badge position adjusted
html = html.replace("left: 46%;", "left: 44%;")

# 14. Replace SVG logo with actual PNG logo
html = html.replace(
    """          <svg viewBox="0 0 100 100">
            <path d="M26 91.6 Q50 76 74 91.6 A48 48 0 1 1 26 91.6 Z" fill="var(--now-green)"/>
            <circle cx="50" cy="50" r="26" fill="white"/>
          </svg>""",
    f'          <img src="{logo_b64}" alt="ServiceNow">'
)

out = os.path.join(SCRIPT_DIR, "wdf-connectors_banner.html")
with open(out, "w") as f:
    f.write(html)

print("Banner updated: real logo, 3.5:1 aspect ratio, tighter layout")
