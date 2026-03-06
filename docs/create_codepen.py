#!/usr/bin/env python3
"""
Opens a browser tab with a pre-filled CodePen containing the WDF banner.
Just run: python3 docs/create_codepen.py
Then save the pen in CodePen and share the URL.
"""
import json, html, webbrowser, tempfile, os, re

src = os.path.join(os.path.dirname(__file__), "wdf-connectors_banner.html")
with open(src) as f:
    content = f.read()

# Extract CSS (between <style> and </style>)
css = re.search(r'<style>(.*?)</style>', content, re.DOTALL).group(1).strip()

# Extract JS (between <script> and </script>)
js = re.search(r'<script>(.*?)</script>', content, re.DOTALL).group(1).strip()

# Extract body HTML (between <body> and </body>, minus <script>)
body = re.search(r'<body>(.*?)<script>', content, re.DOTALL).group(1).strip()

data = json.dumps({
    "title": "WDF Connectors Banner",
    "html": body,
    "css": css,
    "js": js,
    "css_external": "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap",
})

escaped = html.escape(data, quote=True)

page = f'''<!DOCTYPE html>
<html><body>
<p>Redirecting to CodePen...</p>
<form id="f" action="https://codepen.io/pen/define" method="POST" target="_blank">
<input type="hidden" name="data" value="{escaped}">
</form>
<script>document.getElementById("f").submit();</script>
</body></html>'''

tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w")
tmp.write(page)
tmp.close()
print(f"Opening CodePen prefill form: {tmp.name}")
webbrowser.open("file://" + tmp.name)
