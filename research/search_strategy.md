# Search strategy as executed
1. **Ten cluster scouts (sonnet)**: leptoquarks/flavour; dark sectors; SUSY corners; LLPs; exotic Higgs/scalars; EFT/EW; compositeness/heavy states; ALPs/light states; QCD/substructure/quantum-information; older 'orphaned' ideas + Snowmass/Yellow-Report gap statements. Each: topcite (incl. date<2012), forward/backward citation chains via INSPIRE `refersto/citedby:recid`, gap-phrase searches, `--gaps` sentence extraction from PDFs, closest CMS/ATLAS/LHCb search lookup. Query logs are in each `literature/scout_*.json` (`queries_run`; the QCD scout's early log was overwritten by a shared-scratch collision and reconstructed).
2. **Merge/dedupe** (orchestrator): 199 seeds -> 74 directions (`tools/merge_seeds.py`); 986 unique papers.
3. **Gate 2 triage (6 sonnet)**: proper CMS/ATLAS/LHCb coverage checks with collaboration-filtered INSPIRE queries, HEPData/public pages, reading closest results; PASS/HOLD/REJECT.
4. **Gate 3 adversarial (7 opus, 27 PASS directions)**: kill attempts with >=8 query formulations each.
5. **Gate 4 independent reviews (opus)**: experimental, feasibility, theory for 10 directions, mutually blind.
6. **Arbiter (strongest model)** + citation audit.
Known weaknesses: INSPIRE title/abstract queries miss full-text and CMS PAS/ATLAS-CONF items; `abstract "..."` syntax returns nothing (use `abstracts.value:`); `refersto:arxiv:` is unreliable (use recid); WebFetch is lossy; only 10 of 74 directions got full review (lean budget); three batches were interrupted by session rate limits and rerun.
