#!/usr/bin/env python3
"""Pre-publication integrity check for the static CDOC Litigation Archive.

Checks format and relationship referential integrity. Does NOT independently
verify court facts or approve allegations, dates, identities, or case outcomes.
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

root = Path(__file__).resolve().parent.parent
directory = root / "litigation"
errors = []
warnings = []

def error(message):
    errors.append(message)

def warning(message):
    warnings.append(message)

def https_url(value):
    try:
        u = urlparse(value or "")
        return u.scheme == "https" and bool(u.netloc)
    except ValueError:
        return False

csv_file = directory / "cases.csv"
required = {
    "Case title", "Docket / case number", "Court", "Court level",
    "Filing year (verify)", "Named persons / entities (search index)",
    "Preliminary keywords", "Preliminary summary / source-verified event",
    "Public source URL", "Review stage", "Summary evidence level",
    "Case disposition / status", "Last research check"
}
with csv_file.open(encoding="utf-8-sig", newline="") as fp:
    reader = csv.DictReader(fp)
    missing = required.difference(reader.fieldnames or [])
    if missing:
        error("Missing CSV columns: " + ", ".join(sorted(missing)))
    rows = list(reader)

key_counts = Counter()
docket_lookup = {}
for n, r in enumerate(rows, 2):
    docket = (r.get("Docket / case number") or "").strip()
    court = (r.get("Court") or "").strip()
    title = (r.get("Case title") or "").strip()
    if not docket or not court or not title:
        error(f"CSV row {n}: title, court and docket are required")
    key_counts[(court, docket)] += 1
    docket_lookup.setdefault(docket, []).append(r)
    year = (r.get("Filing year (verify)") or "").strip()
    if not re.fullmatch(r"(19|20)\d{2}", year):
        warning(f"CSV row {n}: unverified/malformed filing year {year!r}")
    if not https_url((r.get("Public source URL") or "").strip()):
        error(f"CSV row {n}: missing or invalid HTTPS source URL")
    for col in ("Review stage", "Summary evidence level", "Preliminary summary / source-verified event"):
        if not (r.get(col) or "").strip():
            warning(f"CSV row {n}: missing {col}")
    if (r.get("Court level") or "").strip().lower() == "attorney identified":
        warning(f"CSV row {n}: 'Attorney identified' is not a court level")
for key, count in key_counts.items():
    if count > 1:
        error(f"Duplicate court/docket: {key} ({count} entries)")
if not rows:
    error("CSV contains no case records")

relationship_file = directory / "relationships.json"
relationships = json.loads(relationship_file.read_text(encoding="utf-8"))
used_in_groups = set()
group_ids = set()
for group in relationships.get("confirmed_groups", []):
    group_id = group.get("id")
    if not group_id or group_id in group_ids:
        error(f"Missing or repeated confirmed-group ID: {group_id}")
    group_ids.add(group_id)
    members = group.get("records") or []
    if len(members) < 2:
        error(f"Confirmed group {group_id}: expected >=2 records")
    for member in members:
        docket = member.get("docket", "")
        if docket not in docket_lookup:
            error(f"Confirmed group {group_id}: docket absent from CSV: {docket}")
        if docket in used_in_groups:
            error(f"Confirmed group member appears in multiple groups: {docket}")
        used_in_groups.add(docket)
    if not group.get("evidence") or not group.get("sources"):
        error(f"Confirmed group {group_id}: evidence and primary source links required")
    for link in group.get("sources") or []:
        if not https_url(link):
            error(f"Confirmed group {group_id}: non-HTTPS source")
for item in relationships.get("external_proceedings", []):
    if item.get("primary_docket") not in docket_lookup:
        error(f"External relationship source docket missing from CSV: {item.get('primary_docket')}")
    if item.get("status") not in ("confirmed", "confirmed_origin_only"):
        error(f"External relationship has no permitted verification status: {item.get('related_docket')}")
    if not https_url(item.get("source")):
        error(f"External relationship without HTTPS documentary source: {item.get('related_docket')}")
for item in relationships.get("review_watchlist", []):
    if item.get("status") != "not_confirmed":
        error("Unverified relationship watchlist must retain 'not_confirmed' status")
    for docket in item.get("dockets") or []:
        if docket not in docket_lookup:
            warning(f"Watchlist docket not present in CSV: {docket}")

leadership = json.loads((directory / "leadership.json").read_text(encoding="utf-8"))
for entry in leadership.get("entries", []):
    if not entry.get("name") or not entry.get("role"):
        error("Leadership entry missing name/role")
    if not entry.get("source_urls") or not all(https_url(x) for x in entry.get("source_urls", [])):
        error(f"Leadership entry missing HTTPS sources: {entry.get('name')}")
    if entry.get("portrait_reuse_status", "").startswith("Permission or"):
        if entry.get("portrait_file"):
            error(f"Uncleared leadership photo must not be embedded: {entry.get('name')}")

print(f"Litigation publication check: {len(rows)} court/docket records, "
      f"{len(group_ids)} confirmed internal relationship groups, "
      f"{len(relationships.get('external_proceedings', []))} external proceedings.")
print(f"2019+ records: {sum(int((r.get('Filing year (verify)') or '0')) >= 2019 for r in rows if (r.get('Filing year (verify)') or '0').isdigit())}")
for w in warnings:
    print("REVIEW WARNING:", w)
for e in errors:
    print("PUBLICATION ERROR:", e, file=sys.stderr)
if errors:
    sys.exit(1)
print("STRUCTURAL CHECK PASSED. Court-source fact checking and editorial approval are still required.")
