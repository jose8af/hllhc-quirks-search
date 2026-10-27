# Electroweak quirks at the HL-LHC: coplanar, non-helical tracker patterns

A phenomenology study of **quirks**: heavy particles charged under a new confining group with no light matter, so a
produced pair stays joined by a string of tension σ = Λ². For colour-neutral, electroweak-charged quirks with
Λ ≈ 0.1–100 keV the pair oscillates with an amplitude between metres and micrometres. It leaves tracker hits that are
non-helical and nearly coplanar with the primary vertex. The benchmark is a vector-like-lepton-like E = (1,1)₋₁ with
N_IC = 2, plus its scalar partner, in a CMS Phase-2-like tracker (B = 3.8 T, √s = 14 TeV, pile-up 200, 3 ab⁻¹).

> **Status.** Private phenomenology work using **public information only**. It is not a CMS (or ATLAS) result and has
> not been reviewed by any collaboration. "CMS Phase-2-like" means a detector model built from public TDRs. All results
> are from simulation. Plots carry the label "Private work (simulation)".

**Main deliverable:** [`stage2_C001_quirks/theory_track/paper/quirks_p1p2_note.pdf`](stage2_C001_quirks/theory_track/paper/quirks_p1p2_note.pdf)
(v0.4, 2026-10-17, 43 pp). Read its abstract and §12–13 (limitations, conclusions) first.

## Results so far

- **P1 (truth level, theory).** The solenoid field thickens the quirk plane through log-enhanced axis rotations at
  near-miss string crossings: Δs_B ∝ ε_B[ln(1/ε_B) + C], with ε_B = qB/Λ² and local slope c ≈ 0.104 at Λ = 1 keV,
  m_Q = 500 GeV. The slope is derived analytically, confirmed by blind numerics and tested on 2.2 × 10⁵ truth-level events.
  Full derivation: paper Appendix D and `stage2_C001_quirks/theory_track/analytic/NEAR_MISS_IMPULSE.md`.
- **P2 (detector level).** ACTS/Fatras model of the public Phase-2 tracker with a PU-200 overlay plus a dedicated barrel
  plane finder. **No working point exists**: the lowest expected background is ~10⁶ events, limited by simulation
  statistics and the pile-up extrapolation. The best expected limit is 790 × the predicted σ (m_Q = 200 GeV,
  Λ = 1.5 keV), so nothing is excluded. The most important next step is a data-driven pile-up background estimate.

## How to continue

1. Read the paper, then [`stage2_C001_quirks/theory_track/README.md`](stage2_C001_quirks/theory_track/README.md),
   which gives the status of every stage and the order to read each stage's documents in.
2. Set up the environments and see which data must be regenerated:
   [`stage2_C001_quirks/theory_track/REPRODUCE.md`](stage2_C001_quirks/theory_track/REPRODUCE.md).
   That file also lists the **open work / next steps** (§6).
3. The full history, including every decision and its reason, is in the append-only logs: `research/LOG.md`
   (discovery), `stage2_C001_quirks/LOG.md` and `stage2_C001_quirks/theory_track/LOG.md` (theory track, 6 stages).

## Repository map

| Path | What it is |
|---|---|
| `RESEARCH_PLAN.md`, `TOP_CANDIDATES.md`, `REJECTED_CANDIDATES.md`, `report/hllhc_report.pdf` | **Discovery phase** (2026-10-05/06): literature-driven search for HL-LHC opportunities; quirks were candidate C001 |
| `research/` | Discovery-phase working files: `tools/` (INSPIRE/arXiv helpers), `literature/`, `candidates/`, `reviews/`, `rankings/`, `LOG.md` |
| `stage2_C001_quirks/` | **Quirks study.** `literature/` (bibliography, literature map), `research/` (signal model, experimental status, samples/tools), `phase1_strategy/` (strategy draft, open questions), `phase2_exploration/` (sample requirements), `report/quirks_phase1_report.pdf` |
| `stage2_C001_quirks/theory_track/` | **Main work.** `investigations/`, `code/`, `outputs/` (theory gaps synthesis), `report/` (48-pp theory report) → six-stage programme: |
| `  analytic/` | Stage 1: analytic near-miss impulse coefficient c, blind numerics, novelty audit |
| `  sim/` | Stage 2: MadGraph5_aMC 2.9.22 + Pythia8 CP5 samples (hand-written UFO `sim/models/quirkE`, cards, production scripts) |
| `  sim/stage3/` | Stage 3: truth-level causal-string propagation of 218,571 events |
| `  acts/`, `acts/stage4/` | Stage 4: ACTS/Fatras Phase-2-like tracker at PU 200, plane finder, frozen working-point rule, analysis, results |
| `  stage5/` | Stage 5: final figures (`stage5/figures/final/`) |
| `  opendata/` | Stage 6: CMS Open Data feasibility note |
| `  paper/` | The note (LaTeX, xelatex) with figures, bibliography and review trail |

Every stage has `review/` folders with the reviews and fix reports. Results JSON and figures are in the repo, so most
numbers can be checked without re-running anything.

## Not in this repository

| Item | Size | How to get it |
|---|---|---|
| `stage2_C001_quirks/theory_track/data/` (MC samples, truth propagation, ACTS production, geometry downloads) | 46 GB | Regenerate (commands and CPU costs in `REPRODUCE.md` §2), or ask the author for a copy. Index: `theory_track/DATA_README_snapshot.md`. A few small files in it **are** tracked (≈ 43 MB): the final Stage 4 analysis output `data/acts_stage4/analysis/C12FC_v1/`, `STAGE4_SUMMARY.json`, investigation JSONs, `STAGE3_INDEX.json`, the patched PDF `.info` files and the Windows bundle env |
| `stage2_C001_quirks/theory_track/sim/mg_out/` (MadGraph process directories) | 1.5 GB | Recreated by `sim/scripts/produce.py` |
| `research/cache/` (arXiv PDFs and API responses) | 2.3 GB | Refilled on demand by `research/tools/` |
| `analytic/novelty_sources/` scans and OCR of third-party papers | — | Bibliographic details in `analytic/NOVELTY_AUDIT.md` |
| pixi environments (`.pixi/`) | ~1.3 GB | `pixi install` in each workspace (lockfiles are tracked) |

## Environments and tools

[pixi](https://pixi.sh) workspaces (lockfiles are for osx-arm64; see `REPRODUCE.md` §1 for other platforms):
`theory_track/pixi.toml` (numerics), `theory_track/sim/pixi.toml` (MadGraph driver `mg` and analysis `ana`),
`theory_track/acts/pixi.toml` (pyacts 48.0.0; the wheel needs macOS 26).
External, not installed by pixi: **MadGraph5_aMC v2.9.22** with HEPTools (Pythia8, LHAPDF6, MG5aMC_PY8_interface),
pointed to by `export MG5_DIR=/path/to/MG5_aMC_v2_9_22`; xelatex for the paper. FeynRules + Mathematica are only used
for the UFO cross-check (`export FEYNRULES_PATH=...`).

## How the work was organised

The work follows the JFC agentic-analysis workflow ([arXiv:2603.20179](https://arxiv.org/abs/2603.20179),
[github.com/violatingcp/jfc](https://github.com/violatingcp/jfc)): executor → independent critical and constructive
reviewers → A/B/C-severity triage → fix → fresh reviewer → PASS, with human decisions at the gates. It was carried out
by one person orchestrating Claude Code agents, which is why the documents mention executors (E1…), reviewers (R1…),
investigators (T1…T6), "orchestrator" and "user decisions". Numbers are tagged VERIFIED / ESTIMATE where that
distinction matters. Pre-registered rules (e.g. `acts/stage4/WP_RULE.md`, the analysis freeze
`acts/stage4/analysis/inputs/analysis_freeze.json`) were fixed before signal efficiencies were looked at. Keep them
frozen, or version them explicitly.

## License

No license has been chosen yet: all rights reserved. Contact the author before reusing the material outside the
collaboration that continues this work.
