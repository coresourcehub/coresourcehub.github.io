# CDOC Litigation Archive — Data and source review process

## November 2026 expansion — 75 records and executive leadership context

- The 75-record user-supplied CSV and workbook were reconciled to the previous 47-record dataset by **court + docket number**. All 47 earlier records were retained and 28 new records added. Previously enriched keywords and relevant research notes were merged conservatively to avoid discarding the project's work.
- The master CSV covers **2018–2026**, with **two** pre-2019 records. The default directory view filters to **2019–present**; a clearly labeled checkbox allows users to include and search historical cases. The filing-year chart, keyword counts and overview are computed from the selected period while the homepage card states the full 75-record coverage.
- A source-linked, three-entry **Executive Leadership Timeline** is stored separately in `litigation/leadership.json`: Dean Williams (2019–2022); Moses “Andre” Stancil, interim (Dec 2022–Jan 2023); and Stancil, permanent (Jan 31, 2023–present, checked November 2026). Dates of appointment/announcement may precede the start of service. Leadership roles do not imply culpability in contemporaneous lawsuits.
- For copyright reasons, leadership portraits **are not embedded** until an explicit reusable license or permission is obtained. The website shows labeled image placeholders and clickable links to credited source photographs. Stock, screenshot crops, and unlicensed editorial photos should not be uploaded as if cleared.
- A published court order in Gambrell, 1:24-cv-01853, identifies **Jason Guidry** as interim Chief of Behavioral Health. The user supplied an alternate `Jason Goudry` spelling from a screenshot, but identity equivalence is **unverified**. Search can discover that research note; do not treat the two spellings as a confirmed merged alias.
- Workbook **Expansion Notes** preserved here: earlier index 47; new records 28; expanded 75; 2 records pre-2019. Filing year differs from alleged-event year. Appeals/removals may track the same dispute; do not count 75 records as 75 unique underlying disputes. The sample includes civil-rights, habeas, state appeals, federal appeals, administrative and other actions. Verify allegations, filing dates, identities and dispositions against primary sources before making substantive assertions.
- Future imports should replace/reconcile `litigation/cases.csv` rather than append blindly. Keep the existing static Pages workflow; CourtListener discovery, if added, must propose staged updates for human review and never auto-publish.



This archive uses the expanded 75-record `litigation/cases.csv` supplied by the project researcher, covering filing years 2018–2026. The searchable directory is at `/litigation/` and individual records use `/litigation/case.html?docket=...&court=...`. These deep links resolve a **docket plus court** pair against the current CSV; they are not a permanent case-specific static HTML file. Keeping the same docket and court in future imports preserves the link.

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

## Keyword enrichment and confidence

On November 20, 2026, the 47-case dataset's preliminary keyword column was expanded. For most cases, additions are descriptive indexing terms from the *existing CSV summaries and docket metadata* (for example, amended complaints, named defendants, and pending pleading review); they are **not independently verified substantive violations**. Two cases received additional source checks:

- **Turley v. Warden, Sterling Correctional Facility et al**, 1:26-cv-00341: [published federal docket and May 15, 2026 order](https://dockets.justia.com/docket/colorado/codce/1:2026cv00341/251088), identifying deliberate-indifference and ADA-accommodation *claims*, and partial dismissal/surviving claims; not a final liability determination.
- **Boles v. CDOC et al**, appeal 24-1444: [September 18, 2025 Tenth Circuit opinion](https://law.justia.com/cases/federal/appellate-courts/ca10/24-1444/24-1444-2025-09-18.html), identifying ADA/wheelchair access, exhaustion, kosher diet, RLUIPA, First Amendment and other issues; specific outcomes require attention to each distinct claim.

Do not treat a keyword like “Civil rights”, “Medical care”, “Disability rights”, or “Eighth Amendment claim” as a court finding that rights were violated. A keyword may mean an allegation, type of lawsuit, legal theory, procedural context, or source-verified topic. Further pleadings/opinions review is necessary before adding detailed substantive tags to other docket-only cases.

## Known limitations

- Research beta, not an exhaustive 2019–2026 census of correctional litigation.
- Most initial entries are docket-metadata-level discovery summaries and have no verified final disposition.
- One source record has `Court level=Attorney identified`, which is not a court level. It is currently preserved unchanged and should be corrected after case-source review.
- Exact-case research pages are generated from the CSV, not full judicial opinions or independently reviewed legal analysis.
- CSV search matches all fields; the user interface filters on court level and filing year and paginates in groups of ten. Larger imports may eventually warrant a server-side index.

The uploaded ZIP widget was used as the presentation starting point, then integrated into existing CO Resource Hub navigation and style. Original court links are maintained from CSV.

## Browse-by-topic interface (November 2026)

- The searchable litigation page offers **featured research topic buttons with case counts** and an expandable set of **all indexed CSV keywords**.
- Featured topics use a short, editable list of **exact keyword aliases** in `litigation/index.html`; they do **not** infer issues by scanning arbitrary summaries. For example, ADA / disability can group `ADA`, `ADA accommodation`, `Disability rights`, and `Wheelchair access` when those explicit keywords appear in a case.
- Each number counts **distinct case records tagged with the topic**, not keyword appearances, proven claims, or findings. The full keyword list counts distinct case records per exact phrase; semantically similar phrases may have different counts.
- The selected topic is combined with free-text search, court level and filing year as an **AND filter**. Clicking the active topic again, or the Clear topic control, removes the topic filter.
- Keyword chips on individual case cards are interactive and apply an exact keyword filter. The original text-based case search, year graph, source links and pagination remain available.
- Counts are **calculated in the visitor's browser directly from `cases.csv` on each load**, so replacing the reviewed CSV and redeploying updates them. Topic alias mappings may need manual review when new terms are introduced.
- All tags are labeled as **research topics, not judicial findings**. A medical or civil rights keyword is not evidence that a violation was legally established.
