# CDOC Litigation Archive — Data and source review process

This archive uses the initial 47-record `litigation/cases.csv` supplied by the project researcher, covering filing years 2019–2026. The searchable directory is at `/litigation/` and individual records use `/litigation/case.html?docket=...&court=...`. These deep links resolve a **docket plus court** pair against the current CSV; they are not a permanent case-specific static HTML file. Keeping the same docket and court in future imports preserves the link.

## Updating the archive

1. Make a reviewed CSV with the **same column headers and UTF-8 encoding**.
2. Do not publish confidential submissions, personal correspondence, protected medical details, unredacted legal records, or non-public identifying information.
3. Run `python3 scripts/validate-litigation-csv.py litigation/cases.csv` and investigate warnings.
4. Check new/changed case titles, parties, named staff/officials, courts, dockets, filing years, descriptions, source URLs, and procedural disposition against accessible primary court documents. **Names appearing in a lawsuit do not establish wrongdoing.** Distinguish allegations from judicial findings, and do not claim an unverified disposition.
5. Include candid `Review stage`, `Summary evidence level`, `Case disposition / status`, `Source document type` and `Last research check` fields.
6. Commit the reviewed CSV to `main`, then use the repository's existing manual Pages deployment workflow. No HTML edits are required to update the displayed cases.

## CourtListener import architecture — planned, not automated yet

- Future connector: CourtListener API can provide docket metadata, parties, opinions, filings, citations, dates and public-source links, subject to its terms, coverage, rate limits, and access restrictions. CourtListener data may be incomplete or delayed.
- Store API tokens in **GitHub Actions secrets**, never client-side HTML, public CSV, or the Pages repository.
- Run a scheduled or manually dispatched import **into a staging file or review pull request**, never directly into the published `cases.csv`.
- Reconcile matching docket numbers + jurisdictions carefully; track CourtListener IDs separately from local case keys and document every field provenance.
- Produce a human review report of additions, changed statuses and disputed facts, and **require manual approval** before copying them into `cases.csv`.
- Keep immutable source snapshots privately or where permitted; publish only appropriate public-record extracts.
- The current static widget **does not perform API calls, scheduling, automatic court monitoring, or auto-publication**.

## Known limitations

- Research beta, not an exhaustive 2019–2026 census of correctional litigation.
- Most initial entries are docket-metadata-level discovery summaries and have no verified final disposition.
- One source record has `Court level=Attorney identified`, which is not a court level. It is currently preserved unchanged and should be corrected after case-source review.
- Exact-case research pages are generated from the CSV, not full judicial opinions or independently reviewed legal analysis.
- CSV search matches all fields; the user interface filters on court level and filing year and paginates in groups of ten. Larger imports may eventually warrant a server-side index.

The uploaded ZIP widget was used as the presentation starting point, then integrated into existing CO Resource Hub navigation and style. Original court links are maintained from CSV.
