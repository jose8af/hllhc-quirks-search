# theory_track/sim — Stage 2: MadGraph5_aMC@NLO + Pythia8 generation of quirk pairs (replaces code/T2_kinematics.py)

Local tools (do not modify the installs, except linking our model into MG `models/`; user approved 2026-10-11):
- MadGraph5_aMC v2.9.22: /Users/jochoafl/8A/MadGraph/MG5_aMC_v2_9_22 (Pythia8 + LHAPDF6 + MG5aMC_PY8_interface in HEPTools/)
  [2026-10-27 handoff: scripts now read this location from `$MG5_DIR` and FeynRules from `$FEYNRULES_PATH`; see ../REPRODUCE.md]
- FeynRules: /Users/jochoafl/8A/FeynRules/feynrules-current; Mathematica batch: /Applications/Mathematica.app/Contents/MacOS/wolframscript

Layout:
- `models/`   hand-written minimal UFO (SM + E = (1,1)_{-1} SU(2)-singlet Dirac fermion, scalar Ẽ = (1,1)_{-1} singlet); FeynRules cross-check model
- `cards/`    proc/run/param/pythia8 cards
- `mg_out/`   MadGraph `output` directories (never inside the MG install)
- `scripts/`  generation, conversion (LHE/HepMC → T3_causal input), validation
- `SAMPLES.md` sample inventory (process, σ, N, weights, seeds, files in ../data/sim/)
Large files (LHE, HepMC, converted npz) go in ../data/sim/ (documented in ../data/README.md).

Added by E4 (2026-10-11, plan turn):
- `plan.md`   Stage-2 plan (environment, model, cards, sample table, format, validation, decisions, risks) — read first
- `pixi.toml` separate pixi workspace: env `mg` (py3.9 + six + conda-forge LHAPDF 6.5.5, runs MG 2.9.22), env `ana` (py3.11, pyhepmc, fastjet, mplhep)
- `models/quirkE/` hand-written UFO (import by absolute path: `import model <abs>/sim/models/quirkE-no_b_mass`); `models/fr/` FeynRules cross-check (.fr + batch .wls + UFO)
- `probes/`   ≤ 1000-event probe scripts and logs; `E4_session_log.md` milestones
- `scripts/mg_configure.py`, `patch_ptqq_cut.py`, `convert_hepmc.py`, `mg_events.py` (loader for T3_causal)
- Run MG with `LHAPDF_DATA_PATH=../data/sim/lhapdf PYTHONDONTWRITEBYTECODE=1 pixi run -e mg python /Users/jochoafl/8A/MadGraph/MG5_aMC_v2_9_22/bin/mg5_aMC <script>`
  (PYTHONDONTWRITEBYTECODE keeps Python from writing `__pycache__` into the MG install)
- **Status: STAGE 2 PASS (R2, 2026-10-11)** (`review/REVIEW_S2_R2.md`: 0A/0B/8C; C-1…C-7 applied, C-8 in `DEFERRED.md`).
  - σ table normalisation: σ_norm = N_IC (2) × K_WG × LO(α(M_Z)) reproduces the TH §2.3 table to −0.36…+0.15 %; yields with
    `mg_events.sigma_norm_fb` (not `sigma_lo_mlm_fb`, which has no K); nuisance ±5 % (K transfer + EW scheme); γγ and
    Sommerfeld are not included.
  - Tail-rate uncertainty of f(pT(QQ̄) > 200) at LO-MLM: +12…+15 % / −11…−13 % (ME α_s ⊕ merging ⊕ shower; ESTIMATE); NLO-FxFx deferred (D-1).
  - ℓ_max bias of the fixed-pT ISR trick, like-for-like: −26 / −13 / −8 % (E) and −23 / −12 / −4 % (Ẽ) at 200/500/1000 GeV;
    reference medians known to ±5.0…5.2 % (ESTIMATE).
  - Pending user decision on QED FSR off the quirks (absent from the delivered samples by default; −0.1…−1.1 ± 0.5…0.8 % on the
    tail ℓ_max median): re-shower ≈ 15 CPU-h vs a one-sided ℓ_max systematic.
- Status 2026-10-11 05:45: Stage 2 production + validation DONE (revised 2026-10-11 after review S2-R1, see below). Read `VALIDATION.md` §0, then `SAMPLES.md`. Recommended samples:
  `data/sim/npz/{E,S}-TRGS_m<m>.npz` (trigger region, stitched), `*-INC_*` (inclusive MLM), `*-LOPS_*` (LO+PS). Loader `scripts/mg_events.py`.
  Production driver `scripts/produce.py` (resumable); validation `scripts/val_*.py` → `results/*.json`, `figures/`.

Revised by the fixer after review S2-R1 (2026-10-11; `review/FIX_S2_R1.md`, deferred items `DEFERRED.md`):
- **How to run everything:** `scripts/run_all.sh <stage>` or the pixi task chain
  `pixi run -e ana {probes, produce, vshower, post, validate, docs}` (each depends on the previous; `docs-only` = documents only).
  See VALIDATION.md §9.
- **Using the samples (read SAMPLES.md first):** weights are mandatory (TRGS INC rows carry 3.7-9.6× the TRG weight; the loader
  returns `info['w']`, or use `iter_events(..., unweight=True)`); yields with `mg_events.sigma_norm_fb` (N_IC = 2, LO × K),
  not `sigma_lo_mlm_fb`/`sigma_fb` (LO-MLM, no K); templates vs pseudo-data with `split='template'|'toy'`.
- New scripts: `add_rowmap.py` (row → LHE event, Pythia job, seed; template/toy split), `reshower.py` (regenerate the full
  Pythia record of any row, bit-for-bit), `annotate_npz.py` (σ_norm metadata), `run_vshower.sh` + `val_shower.py`
  (V-SHOWER), `run_alps.py` (MG emission-α_s weights), `val_interp.py` (550 GeV closure), `val_qed.py` (QED FSR test),
  `val_reshower.py`, `val_probe_rerun.py`, `val_headlines.py` (VALIDATION §0 from the JSON), `run_all.sh`;
  after S2-R2: `val_trgs_stats.py` (TRGS weight structure + template/toy pull → `results/trgs_stats.json`).
- `cards/`: effective `run_card_prod_*.dat` / `proc_card_prod_*.dat` per sample class; opt-in `pythia8_quirk_qedfsr.dat`
  (QED FSR off the quirks; not used for the delivered samples, VALIDATION §7).

