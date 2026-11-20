#!/usr/bin/env python3
"""Add independent CO Resource Hub navigation to extracted Policy Library HTML.

Runs on the staged website only. Does not modify original ZIP or PDFs.
"""
from pathlib import Path
import re

root = Path("_site/policy-library")
marker = "co-hub-global-navigation"
nav = """<nav id="co-hub-global-navigation" aria-label="CO Resource Hub site navigation" style="box-sizing:border-box;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;background:#112f46;color:#ffffff;padding:10px 20px;font:600 15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;">
<a href="/" style="color:#ffffff;text-decoration:underline;text-underline-offset:3px;padding:6px 2px;">← CO Resource Hub Home</a>
<a href="/facilities/" style="color:#ffffff;text-decoration:underline;text-underline-offset:3px;padding:6px 2px;">Facilities Directory</a>
</nav>"""
changed = 0
for page in root.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    if marker in text:
        continue
    result, n = re.subn(r"(<body\\b[^>]*>)", lambda match: match.group(1) + "\n" + nav + "\n", text, count=1, flags=re.I)
    if not n:
        print("No body tag; skipping:", page)
        continue
    page.write_text(result, encoding="utf-8")
    changed += 1
print(f"CO Resource Hub navigation injected into {changed} policy-library HTML pages.")
if not (root / "index.html").exists() or marker not in (root / "index.html").read_text(encoding="utf-8"):
    raise SystemExit("Navigation missing from policy library homepage")
