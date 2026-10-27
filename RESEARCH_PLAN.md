# RESEARCH_PLAN — HL-LHC idea discovery (Phase 0: literature & candidate discovery)

Date: 2026-10-05. Everything lives under this directory (`hllhc_search/`); nothing global is installed or modified.

## 0. Environment audit (verified, not assumed)

| Capability | Status |
|---|---|
| INSPIRE REST API (`inspirehep.net/api/literature`, refs, citations, `topcite`) | works via curl/urllib, no key |
| arXiv API (`https://export.arxiv.org/api/query`) | works (must use https) |
| arXiv PDFs + `pdftotext` | works (poppler installed) |
| HEPData (`hepdata.net`) | reachable (HTTP 200) — used to check published limits/tables |
| WebSearch / WebFetch | available (deferred tools; WebFetch is lossy: prefer curl for APIs) |
| Python 3.14, jq, curl | present; no `requests`/PyMuPDF → stdlib only |
| Persistent local files | yes |
| Subagents (Agent tool) | yes; model selectable per agent: haiku / sonnet / opus / fable |
| MCP research servers | none relevant (Blender, XTB, Claude Docs only) |
| Git repo | no (not initialised; could `git init` later, local only) |

Not available: CMS/ATLAS internal documents, CDS full-text search API beyond what INSPIRE mirrors. Experimental coverage will therefore be checked via INSPIRE (`collaboration:CMS/ATLAS/LHCb`, `t`/`a` searches), HEPData, CMS/ATLAS public results pages (WebFetch), and PDF reading.

JFC reference (studied): `jfc-mit/jfc` (arXiv:2603.20179). Key transferable ideas: orchestrator never does the work and holds only summaries + verdicts; every phase = executor → independent reviewer(s) → A/B/C-severity triage → fix/re-review loop → commit; human gate at the decisive point; strict per-agent input/output specs; experiment log for oversight. I adopt these and adapt them to discovery (no data analysis at this stage).

## 1. Agent architecture

Orchestrator (main session, no deep reading, holds only digests + verdicts + the experiment log `research/LOG.md`).

| Role | Model | Input | Output |
|---|---|---|---|
| S — Literature Scouts (parallel, one per topic cluster) | haiku/sonnet | topic cluster + helper CLI | `literature/scout_<cluster>.json` (papers + "open question" quotes + candidate seeds) |
| L — Lineage agent | sonnet | seed paper IDs | `literature/lineage/<seed>.md` (backward/forward citation map, who followed up on each "future work" statement) |
| T — Theory deep-reader | opus | source PDFs (not summaries) | `reviews/theory/<id>.md` |
| E — Experimental status (skeptical experimentalist) | opus | candidate name + signature only (blind to T report) | `reviews/experimental/<id>.md` |
| F — HL-LHC feasibility | opus | candidate + signature only (blind to T/E) | `reviews/feasibility/<id>.md` |
| A — Adversarial novelty killer | opus | candidate claim only | `reviews/adversarial/<id>.md` |
| R — Arbiter | strongest available (fable, else opus) | all four independent reports + source paper list | `rankings/`, `reports/` |

Independence rule: T, E, F, A each receive only the candidate card's *neutral* part (name, framework, seminal refs, proposed signature) — never another agent's conclusions. The arbiter sees all reports and must verify any cited claim exists in the record; claims without a reference ID are discarded.

## 2. Search strategy (complementary channels)

1. **Seminal-paper discovery**: INSPIRE `topcite` queries per topic cluster + reviews (PDG reviews, Snowmass, Yellow Reports, HL/HE-LHC WG reports) → seminal set, then forward-citation descendants.
2. **Citation chains**: INSPIRE `refersto:recid:X` (descendants, sorted by citations/date) and `references`. Specifically test "did anyone follow up on the 'future work' statement?"
3. **Gap-phrase mining**: INSPIRE full-abstract searches for the phrases in the brief ("unexplored", "blind spot", "poorly constrained", "dedicated search", "we leave … for future work", …) restricted to hep-ph, in combination with cluster terms; the hit is a *lead*, not evidence. Full-text "future work" sentences extracted from PDFs of the top ~100 leads.
4. **Experiment-side mapping**: for each lead, `collaboration:(CMS or ATLAS or LHCb)` searches using multiple synonyms of the signature; HEPData and public-results pages; recast/reinterpretation (CheckMATE, MadAnalysis5, SModelS, Recast, GAMBIT, "LHC Reinterpretation Forum").
5. **Topic clusters** (broad on purpose; clusters beyond the user's list are mandatory): leptoquarks/flavour; dark/hidden sectors & portals; SUSY (RPV, compressed, stealth, long-lived, natural-SUSY corners); LLPs; exotic Higgs decays & extended scalars; EW precision/EFT (SMEFT, HEFT, anomalous couplings, VBS/triboson); compositeness/vector-like fermions; ALPs/light states; jet substructure/energy correlators/QCD-exotic signatures; neutrino mass models (Type-II/III seesaw, HNL); doubly-charged & exotic-charge states; CP violation, EDM-collider links; flavour-violating Higgs/top decays; photon-induced / forward-proton (PPS/AFP) processes; heavy-ion/ultra-peripheral; top-quark exotic couplings; quantum-information observables at colliders; timing/MIP-timing-detector enabled signatures; model-independent anomaly-motivated directions; "orphaned" 1980s–2000s ideas (technicolor variants, anomalous couplings, Higgs-triplet, fourth generation corners, etc.).
6. **Old-literature pass**: INSPIRE date-filtered (<2012) topcite queries per cluster, to find ideas whose collider consequences were never revisited after the Higgs discovery or after detector upgrades.

Helper tooling (all stdlib, in `research/tools/`): `inspire.py` (search/get/refs/cites with rate limiting, caching to `research/cache/`), `arxiv_pdf.py` (download + pdftotext + "future work" sentence extraction), `dedupe.py`.

## 3. Model allocation

- Cheap (haiku): bulk scouting, metadata, classification, dedupe, gap-phrase harvesting.
- Mid (sonnet): lineage, longer scouting, card drafting.
- Strong (opus): all four independent reviews (T/E/F/A) for every candidate that enters the shortlist stage.
- Strongest (fable if the Agent tool accepts it, else opus with extended effort): arbiter.
- Escalation rule: a candidate reaches strong-model review only if it passes the cheap triage gate (below). Any candidate on the final shortlist must have all four independent strong-model reviews — cost optimisation never skips this.

## 4. Candidate scoring

Ten criteria scored 0–5: theoretical importance; phenomenological richness; experimental novelty; HL-LHC relevance; feasibility; potential sensitivity improvement; signature distinctiveness; literature gap; theoretical robustness; publication impact. Plus confidence H/M/L and a *gap-type* label from the status taxonomy in the brief (e.g. "studied at LHC, not projected to HL-LHC"). Hard rules: (i) experimental novelty and literature gap scores are capped at 2 unless the adversarial review failed to find a covering search; (ii) a score is accompanied by one-paragraph justification with reference IDs; (iii) total is shown but ranking uses the veto rules below first, then the sum. Rankings are decision support, not the decision.

Veto rules (candidate → rejected): covered by an existing CMS/ATLAS/LHCb search of the same signature with HL-relevant sensitivity; excluded in the relevant parameter space; no plausible trigger/rate; irreducible background with no discriminant; gap was an artifact of terminology mismatch.

## 5. Review / gating strategy (JFC-style)

Stage = executor → independent reviewer → triage (A: invalidates, B: must fix, C: note) → fix → re-review → log.

- Gate 1 (after scouting): dedupe + coverage audit — is each cluster represented, any cluster with < N leads is re-scouted with different terms.
- Gate 2 (candidate pool → ~40): cheap triage on three yes/no questions with evidence: identifiable collider observable? searched-for-already (quick check)? plausible HL-LHC sensitivity?
- Gate 3 (~40 → ~20): lineage + one strong adversarial pass.
- Gate 4 (~20 → shortlist): full independent T/E/F reviews; second adversarial round on survivors.
- Gate 5: arbiter. Citation audit: every reference ID is resolved against INSPIRE (existence, title, year match); unresolvable references are struck.
- **Human checkpoint** after the arbiter: ranked set presented, no selection made on the user's behalf.

## 6. Expected artifacts

As in the brief (`research/README.md`, `methodology.md`, `search_strategy.md`, `literature/{papers.json,seminal_papers.md,citation_graph.md}`, `candidates/{candidate_database.json,candidate_cards/,rejected_candidates.md}`, `reviews/{theory,experimental,feasibility,adversarial}/`, `rankings/{ranking.md,ranking.json}`, `reports/{literature_review.md,top_candidates.md}`), plus `research/LOG.md`, `research/tools/`, `research/cache/`. Top-level deliverables `TOP_CANDIDATES.md` and `REJECTED_CANDIDATES.md` are written to the project root (copies/links to `reports/`). Stage-2 (analysis) is not started until the human picks a candidate.

## 7. Stopping criteria for discovery phase

Stop scouting when all hold: (a) every cluster has ≥ 3 independent search passes (topcite, gap-phrase, citation-chain); (b) the last two scouting rounds added < 10% new candidate names after dedupe; (c) candidate pool ≥ 50 (target 50–150 depending on yield); (d) ≥ 10 candidates survive Gate 4 *or* we document that fewer than 10 survive and why. Hard cap on cost: stop and report if the shortlist review would exceed ~40 strong-model agent runs without human approval.

## 8. Scientific-standards rules (apply to all agents)

- No claim of "new/unexplored/first" without listing the searches performed (query strings + databases) and the closest existing works. Use the status taxonomy label instead.
- No fabricated IDs, limits, cross sections. Every number carries a reference ID and location (section/figure/table), or is marked `UNVERIFIED`.
- Small back-of-envelope calculations (cross sections, yields) are allowed only when labelled as such, with inputs and sources.
- Absence of search hits is recorded as "not found with these queries", never as absence.
