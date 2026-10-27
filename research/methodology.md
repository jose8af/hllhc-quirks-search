# Methodology & shared agent rules

Workspace root: `/Users/jochoafl/FISICA_USFQ/hllhc_search/research/`. Write only inside it. Never modify anything outside the project directory.

## Tools
- `python3 research/tools/inspire.py search|get|refs|cites ...` (INSPIRE; JSON lines; cached; see file docstring). INSPIRE query syntax: `t leptoquark and date > 2010 and topcite 100+`, `a author`, `refersto:recid:N`, `citedby:recid:N`, `collaboration:CMS`, `abstracts` words via `abstracts.value:"…"` (NOT `abstract "…"`, which returns nothing), `arxiv_eprints.categories`/`primarch hep-ph`, `tc p` (published), `tc r` (review).
- `python3 research/tools/arxiv_pdf.py <arxiv-id> [--gaps]` downloads + converts the PDF to text (path printed) and lists "future work"-type sentences.
- WebSearch / WebFetch for CMS/ATLAS public result pages, HEPData (`hepdata.net`), CDS. WebFetch is lossy: prefer reading PDFs via the tool above for facts/numbers.

## Evidence rules
1. Every factual claim cites a paper by arXiv ID (or INSPIRE recid / DOI if no arXiv) + location (section/figure/table) where possible. Verify the ID exists by looking it up with inspire.py; never type an ID from memory without verification.
2. No numbers (limits, cross sections, projections) from memory. Read them from the source, or mark `UNVERIFIED`.
3. Do not write "new", "never studied", "first", "unexplored" as findings. Use the status taxonomy: `proposed-not-searched`, `theory-explored-untested`, `searched-limited-regime`, `LHC-not-projected-to-HL`, `one-observable-not-another`, `indirectly-covered`, `constrained-but-region-open`, `well-covered`. List the queries used.
4. A "future work" sentence is a lead only. Check by forward citations whether it was followed up.
5. Distinguish novel theory / novel phenomenology / novel experimental analysis.

## Candidate seed schema (scout output, JSON list)
```json
{
 "name": "short descriptive name",
 "cluster": "cluster id",
 "framework": "theory framework",
 "idea": "2-3 sentence description",
 "signature_hypothesis": "what CMS/ATLAS would look at (final state / observable)",
 "seminal_refs": [{"id": "arXiv:....", "title": "...", "year": 0, "why": "..."}],
 "followup_refs": [{"id": "...", "title": "...", "year": 0}],
 "gap_evidence": [{"id": "arXiv:...", "quote": "verbatim sentence from paper", "location": "sec/page"}],
 "exp_coverage_seen": [{"id": "...", "note": "closest existing CMS/ATLAS/LHCb search seen"}],
 "gap_type_guess": "taxonomy label",
 "novelty_kind": "theory|phenomenology|experimental-analysis",
 "queries_used": ["..."],
 "confidence": "low|medium|high",
 "notes": ""
}
```
Papers file (`papers`): list of `{recid, arxiv, title, authors, year, cites, role: seminal|review|followup|experimental|projection|recast, cluster}`.
