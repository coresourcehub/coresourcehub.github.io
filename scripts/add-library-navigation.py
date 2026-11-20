#!/usr/bin/env python3
"""Add an accessible CO Resource Hub navigation strip to extracted Policy Library HTML.
This modifies presentation HTML only; all original PDF documents remain unchanged.
Idempotent: existing inserted strip is not duplicated on future builds.
"""
from pathlib import Path
import re

root = Path("_site/policy-library")
nav = '''<!-- CO Resource Hub cross-site navigation (added during deployment) -->
<style id="cohub-navigation-styles">
.cohub-site-nav{box-sizing:border-box;background:#112f46;color:#fff;padding:9px clamp(14px,3vw,28px);font:600 14px/1.55 system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;position:relative;z-index:2000}
.cohub-site-nav *{box-sizing:border-box}
.cohub-site-nav-inner{max-width:1280px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:12px 22px;justify-content:space-between}
.cohub-site-nav a{color:#fff!important;text-decoration:none!important;border-bottom:1px solid transparent}
.cohub-site-nav a:hover{text-decoration:underline!important}
.cohub-site-nav a:focus-visible{outline:3px solid #f0b94d;outline-offset:4px}
.cohub-site-nav .cohub-home{font-weight:800;letter-spacing:.01em}
.cohub-site-nav-links{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center}
@media print{.cohub-site-nav{display:none!important}}
</style>
<nav class="cohub-site-nav" aria-label="CO Resource Hub site navigation">
 <div class="cohub-site-nav-inner">
  <a class="cohub-home" href="/" aria-label="Return to CO Resource Hub homepage">← CO Resource Hub Home</a>
  <div class="cohub-site-nav-links">
   <a href="/policy-library/" aria-label="Policy Library main search">Policy Library Search</a>
   <a href="/facilities/">Facilities Directory</a>
  </div>
 </div>
</nav>
<!-- End CO Resource Hub cross-site navigation -->
'''
updated=[]
for page in root.rglob("*.html"):
    source=page.read_text(encoding="utf-8")
    if 'id="cohub-navigation-styles"' in source:
        continue
    modified,count=re.subn(r"(<body\b[^>]*>)",lambda m:m.group(1)+"\n"+nav,source,count=1,flags=re.I)
    if count:
        page.write_text(modified,encoding="utf-8")
        updated.append(str(page))
print(f"Added navigation strip to {len(updated)} Policy Library HTML pages")
if not updated and not any('id="cohub-navigation-styles"' in p.read_text(encoding="utf-8") for p in root.rglob("*.html")):
    raise SystemExit("No editable policy-library HTML pages found")
