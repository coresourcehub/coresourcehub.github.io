#!/usr/bin/env python3
"""Validate standalone litigation CSV before publishing. No external API access."""
import csv, re, sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

file = Path(sys.argv[1]) if len(sys.argv)>1 else Path("litigation/cases.csv")
required = {
    "Case title","Docket / case number","Filing year (verify)","Court","Court level",
    "Named persons / entities (search index)","Preliminary keywords","Plaintiff representation",
    "Preliminary summary / source-verified event","Public source URL","Review stage",
    "Summary evidence level","Case disposition / status","Last research check"
}
with file.open(encoding="utf-8-sig",newline="") as f:
    reader=csv.DictReader(f)
    missing=required-set(reader.fieldnames or [])
    if missing: raise SystemExit("Missing headers: "+", ".join(sorted(missing)))
    rows=list(reader)
errors=[];warnings=[]
keys=Counter()
for idx,r in enumerate(rows,2):
    key=(r["Docket / case number"].strip(),r["Court"].strip())
    keys[key]+=1
    if not key[0] or not key[1]: errors.append(f"Row {idx}: docket/court missing")
    if not r["Case title"].strip(): errors.append(f"Row {idx}: case title missing")
    if not re.fullmatch(r"(?:19|20)\d{2}",r["Filing year (verify)"].strip()): warnings.append(f"Row {idx}: filing year needs review")
    link=r["Public source URL"].strip()
    p=urlparse(link)
    if p.scheme!="https" or not p.netloc: errors.append(f"Row {idx}: public source must be HTTPS")
    if not r["Review stage"].strip(): warnings.append(f"Row {idx}: missing review stage")
    if not r["Summary evidence level"].strip(): warnings.append(f"Row {idx}: missing evidence level")
    if r["Court level"].strip()=="Attorney identified":warnings.append(f"Row {idx}: anomalous Court level 'Attorney identified' — source preserved")
for (d,c),v in keys.items():
    if v>1:errors.append(f"Duplicate docket/court pair: {d} / {c} ({v} rows)")
print(f"Litigation CSV: {len(rows)} records; {len(keys)} unique docket/court keys")
for w in warnings: print("REVIEW:",w)
for e in errors: print("ERROR:",e,file=sys.stderr)
if errors: raise SystemExit(1)
print("Validation passed with",len(warnings),"review warning(s).")
