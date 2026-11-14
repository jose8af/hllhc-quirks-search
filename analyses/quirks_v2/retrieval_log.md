# Retrieval Log

## 2026-11-13 — Phase 1 strategy (Brigitte). No RAG corpus (deviation V8); look-ups in the repo's literature cache.

| # | query / need | where looked | result |
|---|---|---|---|
| 1 | closest published central-tracker quirk studies: methods, pile-up, backgrounds, reach | `stage2_C001_quirks/theory_track/paper/P2_NOVELTY_AUDIT.md` §1.1-1.4 (audit of arXiv:1708.02243, 1911.02223, 2002.07503, 2410.00269, 2509.08878 with page numbers) | FOUND: Knapen et al. 650 GeV at 300 fb-1 (5 events, B = 0), Table I efficiencies; Li et al. 0.12 fb background, 450 (150) GeV at 100 fb-1, 400 GeV at 300 fb-1 for N_IC = 2. Paper content transcribed, not re-read (UNVERIFIED) |
| 2 | existing experimental bounds on the E benchmark | `…/theory_track/stage5/EXTERNAL_BOUNDS.md` (FASER HEPData ins3184325, D0 1008.3547, Farina-Low 1703.00912) | FOUND: FASER 113/162.6/172/179 GeV at 1/3/5/10 keV; D0 107 GeV; Farina-Low 650/150 GeV at 1/100 eV |
| 3 | systematic programmes of experimental reference analyses | `stage2_C001_quirks/research/experimental_status_2026.md` §2 (l.115-150), l.335 | FOUND for CMS disappearing tracks (Table 7 values), CMS HSCP, ATLAS dE/dx+ToF; FASER: only the shower-scale term (6 %, up to 28 %). FASER full table and statistical method NOT FOUND in the repo → retrieval task R-10 |
| 4 | source of the v1 K-factors and slepton tables | `stage2_C001_quirks/research/theory_signal_model.md` l.155-170 | FOUND: which tables were used (LHC SUSY cross-section WG right-selectron, 13 TeV NLO+NLL and 13.6 TeV NNLO_approx+NNLL) and the implied K range 1.06-1.29; table values NOT in the repo → R-1 |
| 5 | cosmic and beam-halo rates | same file l.147, l.322 (arXiv:1801.00359 Table 4) | PARTIAL: 8.8 ± 3.1 cosmic and 2.6 ± 0.2 halo events in 586 h for a stopped-particle selection; no tracker-level rate → R-6 |
| 6 | public Phase-2 MET trigger turn-on; jet response; timing-layer resolution; vertex identification efficiency; HL-LHC luminosity uncertainty; cited SM K-factors | grep over `research/`, `stage2_C001_quirks/research/`, digests D2, D5 | NOT FOUND with a usable number and page (v1 parameters are ESTIMATE or graphical readings) → R-2, R-3, R-5, R-7, R-8, R-9. Nothing was taken from memory |
| 7 | Barbashov solution class; Knapen et al. Sec. III.D wording | digest D3 §1 items 9, 13; novelty audit §1.1 (p. 6: beam-pipe conversions) | PARTIAL: audit supports "beam-pipe conversions only"; exact corrected sentences need the papers → R-11 |

## 2026-11-13 — Phase 1 strategy v2 (fixer Dmitri, review cycle 1). Repo look-ups only; nothing from the web or from memory.

| # | query / need | where looked | result |
|---|---|---|---|
| 8 | per-process N_trig for the floor table and the no-pile-up allocation | `stage2_C001_quirks/theory_track/data/acts_stage4/analysis/C12FC_v1/bsum_wp.json` → `n_trig.value`, `n_trig.breakdown.*.N_trig` (read with `python3 -I`) | FOUND: total 4.0848e7; twelve processes, Z(nunu)+j 2.508e7 … ZZ 1.045e5 (values in `strategy_budget.py`). Single-interaction rates per triggered event taken from digests D4 l.395 and D2 l.69 (UNVERIFIED by me) |
| 9 | public sizes for detector variations, timing tails, readout window, noise occupancy, MET performance at pile-up 200, infracolour Coulomb correction in the quirk literature, K/pi differences between hadronisation models, lepton-veto response to quirks, recent ATLAS/CMS quirk searches | not looked up in this session (head node, repo only) | NOT RETRIEVED → new retrieval tasks R-12 to R-20 in STRATEGY v2 §6.4; R-3 and R-7 extended. The formula and numbers quoted for the infracolour correction come from the physics review (P-B5) and the arbiter's re-derivation and are reproduced arithmetically in the script; they are not a literature value |
