#!/usr/bin/env python3
"""Add a source-labeled index/legislation reference to the staged Policy Library homepage.

Does not alter the original downloaded ZIP, public AR PDFs, or extracted AR text.
"""
from pathlib import Path
import re

homepage=Path("_site/policy-library/index.html")
html=homepage.read_text(encoding="utf-8")
marker="co-hub-ar-index-references"
if marker in html:
    print("Reference section already added")
    raise SystemExit(0)
section='''<section id="co-hub-ar-index-references" aria-labelledby="co-hub-index-heading" style="box-sizing:border-box;max-width:1120px;margin:18px auto;padding:20px 22px;border:1px solid #cbdde8;border-left:5px solid #257aa5;border-radius:13px;background:#fff;color:#193448;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif">
<h2 id="co-hub-index-heading" style="font-size:1.3rem;line-height:1.25;margin:0 0 12px">CDOC regulation index and policy-change references</h2>
<p style="margin:0 0 12px">CDOC's <strong>Administrative Regulations and OPR Index</strong> identifies AR numbers, titles, effective dates, annual review months, and responsible offices. Constituent Services supplied a copy labeled <strong>Updated October 2026</strong>; the publicly linked index's version has not been independently matched to that copy. Some index entries carry an <strong>RD</strong> (restricted distribution) suffix and may not have public full-text links.</p>
<p style="margin:0 0 12px"><a href="https://drive.google.com/file/d/160G9WIEwNjv_fcelt04CZ9TQZlOfQpBv/view?usp=drive_link" target="_blank" rel="noopener noreferrer" style="color:#14679b;font-weight:700">View CDOC's publicly linked Policy Index ↗</a> &nbsp;·&nbsp; <a href="https://cdoc.colorado.gov/about/department-policies" target="_blank" rel="noopener noreferrer" style="color:#14679b">Official Department Policies directory ↗</a></p>
<p style="margin:0 0 12px">CDOC also published its <a href="https://cdoc.colorado.gov/news-article/notice-of-policy-updates-in-alignment-with-hb-25-1013" target="_blank" rel="noopener noreferrer" style="color:#14679b;font-weight:700">HB25-1013 policy-update notice ↗</a>, identifying updated visitation-related ARs. Read the corresponding <a href="/legislation/bill.html?bill=HB25-1013" style="color:#14679b">HB25-1013 legislative research record</a> or <a href="https://leg.colorado.gov/bills/HB25-1013" target="_blank" rel="noopener noreferrer" style="color:#14679b">official General Assembly bill page ↗</a>.</p>
<p style="margin:0;font-size:.9rem;color:#526778"><strong>Verification pending:</strong> AR 600-05 appears in the HB25-1013 notice, but not in the received October index or the publicly listed 600-series directory; AR 950-02 is dated October 15, 2026 in the received index, while our research copy may represent an older version. Neither discrepancy establishes that a regulation was repealed, is confidential, or has a particular substantive change. This research library's original PDFs have not been replaced.</p>
</section>'''
# Place just inside the main area, preserving all existing navigation and AR controls.
m=re.search(r'<main\b[^>]*>',html,re.IGNORECASE)
if m:
    pos=m.end()
    html=html[:pos]+"\n"+section+"\n"+html[pos:]
else:
    m=re.search(r'<body\b[^>]*>',html,re.IGNORECASE)
    if not m:
        raise SystemExit("No main or body element found")
    pos=m.end()
    html=html[:pos]+"\n"+section+"\n"+html[pos:]
homepage.write_text(html,encoding="utf-8")
print("Added source-labeled policy index and HB25-1013 references to published library homepage")
