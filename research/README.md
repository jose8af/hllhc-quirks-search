# hllhc_search — HL-LHC idea-discovery workspace

Local project (nothing global). Goal: find under-explored, HL-LHC-relevant phenomenology ideas before choosing an analysis. See `../RESEARCH_PLAN.md` for the plan, `methodology.md` for agent rules, `search_strategy.md` for what was searched.

Layout: `tools/` (INSPIRE/arXiv helpers, merge script), `cache/` (API+PDF cache), `literature/` (scout outputs, `papers.json`), `candidates/` (raw seeds -> 74 merged directions -> gate verdicts), `reviews/{triage,adversarial,experimental,feasibility,theory}/`, `rankings/`, `reports/`, `LOG.md` (chronological log incl. failures).

Reproduce: `python3 tools/merge_seeds.py` regenerates `candidates/merged_candidates.json` from `candidates/raw_seeds.json`. Scout outputs are `literature/scout_*.json`.

Pipeline status is in `LOG.md`. Human checkpoint: the ranked set in `../TOP_CANDIDATES.md` (once written by the arbiter stage).
