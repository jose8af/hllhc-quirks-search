# FIX S2-R1: response to the Stage-2 critical and constructive reviews (round 1)

Fixer, 2026-10-11. Brief: approved scope within plan §4 and the 35 CPU-h budget. Reviews: `CRITICAL_REVIEW_S2_R1.md` (A1, A2,
B1-B9, C-1..C-11) and `CONSTRUCTIVE_REVIEW_S2_R1.md` (A-1, B-1..B-10, C-1..C-16). Line numbers refer to the files as they are
after this fix. Status: RESOLVED / PARTIALLY RESOLVED / NOT DONE (reason) / DEFERRED (`DEFERRED.md`).

**Compute used in this fix:** ≈ 5.5 CPU-h, of which top-ups + V-INTERP ≈ 3.2, V-SHOWER ≈ 1.2, QED and regeneration tests
≈ 0.5, alps ≈ 0.2, probe reruns ≈ 0.2, row map and validation ≈ 0.2. Stage-2 total ≈ 23.5 of the 35 CPU-h plan budget.
**Events added:** E-TRG 200 +100k, E-INC 200 +100k, E-TRG 300 +40k, E-INC 300 +50k LHE (B-4); V-INTERP 550 GeV 50k (B-7);
V-SHOWER 4 × 50k re-showers of existing LHE (no new LHE). Delivered total 2.41 M LHE; the pre-fix total was 2.07 M, not the
2.40 M the first draft stated.

## Category A

| Item | Status | What changed (file:line) | New numbers / evidence |
|---|---|---|---|
| **A1** (crit.) / **A-1** (constr.): TRGS order and weights | RESOLVED | `scripts/stitch_trg.py:25,47` writes the TRGS rows in a seeded random order (`SHUFFLE_SEED = 20261011` + m (+100000 for Ẽ); `shuffle_seed`, `row_src` stored) and adds `kind`, `nlhe`, `sigma_ref_fb`, `source_ids`. All 17 TRGS regenerated. `scripts/mg_events.py:18` docstring states the weights are unequal (4-11×), `:108` `iter_events` always returns `info['w']` and has `unweight=True` (deterministic hit-or-miss, `:100`, seed over all rows, independent of the selection), `split=`. Regression check `scripts/val_loader.py:55` (`firstn_check`): INC share of w and the weighted median of 2(γ*−1) in the first 500/2000/5000 events (weighted and unweighted) and in the template/toy halves vs the full file. `val_loader.py` re-run. SAMPLES.md:66 (weights "4-11×", N_eff, shuffle); VALIDATION §4.4 (l.365), §6 (l.514); plan.md:284 ("first N" only with weights) | First-N check **PASS at all 4 points** (\|pull\| < 3, max 2.8); first 2000 tail events at E 500 now contain 31 INC rows (was 0). Unweighting efficiency 16-28 %. INC share of the tail σ 3.9-7.3 %, ⟨w_INC⟩/⟨w_TRG⟩ 3.7-11 (SAMPLES.md) |
| **A2** (crit.): headline ranges vs JSON | RESOLVED | New `scripts/val_headlines.py` generates VALIDATION §0 (l.30-63, between AUTO-HEADLINES markers) from `results/*.json`; it is part of the `docs` stage of `run_all.sh`. §3 rewritten (l.241) | N_osc of the trick, mixed comparison: **−2.7…+14.8 %** (no sign-definite bias at 1 TeV). Like-for-like (B4): +26…+52 %. DJR d01 plan metric 2.5-9.5 %, d12 4.9-13.8 % over E-INC 200/500/1000, Ẽ-INC 500 and both V-MERGE samples (was "≤ 7 % / ≤ 12 %") |

## Category B (critical review)

| Item | Status | What changed | New numbers / why not |
|---|---|---|---|
| **B1** EW-scheme nuisance | RESOLVED | VALIDATION §1.3 rewritten (l.141): what the Gμ/α(M_Z) ratio is (α-rescaling check of the LO in σ_norm) and is not (σ_norm = K_WG × LO inherits the WG scheme; R-selectron = same (1,1)₋₁ state, so the s_W² dependence cancels too). §0 item 1; plan.md:338 D8 annotated | Nuisance = **TH's ±5 %** (K transfer + scheme, ESTIMATE) + residual WG-table scheme (UNVERIFIED). The ±7 % was a mis-citation (7 % = TH's α² ratio) |
| **B2** MG install footprint | RESOLVED | VALIDATION §8 (l.612) lists the true footprint. Install cleaned (brief item 15; diff below). `produce.py:84`, `run_alps.py`, `run_all.sh` set `PYTHONDONTWRITEBYTECODE=1` | 13 `.pyc` removed (list + md5: `review/r1_fix_mg_install/removed_pyc.txt`); 2 config lines removed; fixer runs wrote nothing into the install (`find -newermt 06:10`: empty) |
| **B3** tagging | RESOLVED | Tag definition sharpened (VALIDATION l.10-12: single generator → ESTIMATE). Re-tagged ESTIMATE: §2 (l.206), §3 (l.241), §4.1/4.2/4.4 (l.317, 346, 365), §5 (l.422), §1.4 bands (l.169). §1.2: σ_norm/TH is an LO two-code check + interpolation; **K transcription UNVERIFIED for E as for Ẽ** (l.98, 139). σ_norm rows of `xsec.json` tagged "VERIFIED (LO two-code check; K transcribed from TH = UNVERIFIED)" (`val_xsec.py`) | — |
| **B4** like-for-like ℓ_max / N_osc | RESOLVED | `scripts/val_lmax.py:74` adds (iv-noeta); biases (i) vs (iv-noeta). VALIDATION §3 (l.241): (i') vs (iv) (\|η\| < 2.5 both) PRIMARY; (i) vs (iv-noeta) = T2 §3 definition; mixed kept for traceability; the "TH App. A / T2 §3" conflation corrected; S-13 correspondence explicit | Like-for-like (i'): ℓ_max −26/−13/−8 % (E), −23/−12/−4 % (Ẽ); N_osc +26…+52 %. No-η (S-13 definition): ℓ_max −26…−4 %, N_osc +16…+29 %; at E 500 (T2 §3's mass) **+22.0 ± 0.9 %** vs S-13's "+20 %" |
| **B5** merging syst. and V-SHOWER in ℓ_max uncertainty | RESOLVED | V-SHOWER run (brief item 7; below). `val_lmax.py:129` builds `syst_budget` (stat ⊕ scale ⊕ merging ⊕ shower ⊕ ME α_s) per point; VALIDATION §3 budget table, §5.1 (l.447) | ℓ_max reference uncertainty **±5.0-5.2 %**, N_osc ±3.2-3.5 %, dominated by the statistically limited merging envelope (4.6 ± 3.7 %) |
| **B6** loader `sigma_fb` vs σ_norm | RESOLVED | `mg_events.py:137` `sigma_lo_mlm_fb` (alias `sigma_fb`, documented as LO-MLM, Gμ, no K) and `:151` `sigma_norm_fb` = σ_norm × Σw_sel/σ_ref; `scripts/annotate_npz.py` writes `sigma_norm_fb` (N_IC = 2), `sigma_ref_fb`, `normalisation_tag` to every npz and `_sigma_norm_fb` to SAMPLES_INDEX.json | `sigma_norm_fb(500,'trig',ptmin=200)` = 0.6365 fb → 1909 events at 3 ab⁻¹ (= table); `sigma_lo_mlm_fb` = 0.5224 fb (−18 %) |
| **B7** reproducibility | RESOLVED | (a) `probes/t16_lo_grid.mg:6` and `t4_xsec.mg:5` set aEWM1/Gf explicitly; (b) new `probes/t3_E_incl.mg`; reruns (`probes/*_rerun.log`, `scripts/val_probe_rerun.py`, `results/probe_rerun.json`); (c) `scripts/run_all.sh` + pixi task chain (`pixi.toml` `[feature.ana.tasks]`; lock file unchanged), README.md:27, VALIDATION §9 (l.633); (d) `cards/run_card_prod_*.dat`, `proc_card_prod_*.dat` (12 sample classes, from the banners). MG path still hard-coded (one constant per script; documented) | t16 rerun identical (14 masses; one −0.03 %); t3/t4 within MC error (max +0.87 % at E 1000, 2.5σ combined) |
| **B8** d12 vs the 10 % criterion | RESOLVED | `scripts/val_mlm.py:49` `step_test` (two straight-line fits around lq, discontinuity ± error, slope ratio, adjacent-bin step); VALIDATION §4.1 (l.317) | Plan metric: **d12 FAILS** at E-INC 500 (11.7 %) and V-MERGE 20/30, 50/75 (11.6, 13.8 %). Step test: all nominal samples PASS (\|disc\| ≤ 5.4 % d01, ≤ 3.4 % d12); **V-MERGE (20,30) d12 FAILS (−15.8 ± 2.8 %)**; its tail effect is inside the merging envelope |
| **B9** figures | PARTIALLY RESOLVED / DEFERRED | `scripts/vlib.py:19` label "Private work (simulation, generator level)" on all 33 regenerated figures; no CMS-type label anywhere; open markers for the extrapolated-K masses in `xsec_normalisation.png`; `lmax_bias.png` states the selection. Full JFC/mplhep restyle → DEFERRED.md D-3 | — |

## Category C (critical review)

| Item | Status | Change |
|---|---|---|
| C-1 E is a singlet | RESOLVED | plan.md:5 and README.md say "SU(2) singlet (1,1)₋₁" for E and Ẽ; no "doublet" anywhere in the Stage-2 docs. UFO `Y = 0` attribute is cosmetic (unchanged) |
| C-2 K extrapolation, PDF > 1200 | RESOLVED | `val_xsec.py:125` ±2 % on the extrapolated K (`K_unc_pct`), PDF beyond 1200 GeV tagged "LOWER BOUND"; VALIDATION §1.2 (l.90) |
| C-3 CMSSW CP5 precision | RESOLVED | VALIDATION §10 (l.668) note (≲ 0.3 % on pT0) |
| C-4 TRG/INC boundary rounding | NOTED | 10⁻⁵ level; no change |
| C-5 etaj = 5 | NOTED | negligible; unchanged |
| C-6 TRGS vs INC correlated | RESOLVED | VALIDATION §4.4 and SAMPLES.md:66: the independent test is the generation-cut closure; never use TRGS/INC as an independent pair |
| C-7 QED FSR not realised | RESOLVED (diagnosed) | see B-9 |
| C-8 V1b extension not delivered | RESOLVED (documented) | VALIDATION §8 item 9 (low risk) |
| C-9 docstring / stale log | RESOLVED | `val_lmax.py` docstring → `figures/lmax_bias.png`; stale log renamed `logs/oldflow_discarded_convert_E-INC_m500_c0.log` |
| C-10 probe hint retracted | NOTED | plan.md:31 now points to the result |
| C-11 tail K at NLO | DEFERRED | DEFERRED.md D-1; the LO tail-rate uncertainty is now quantified (§5.1) |

## Constructive review

| Item | Status | What changed | New numbers / why not |
|---|---|---|---|
| **A-1** | RESOLVED | = A1 above | — |
| **B-1** ISR-tail uncertainty | RESOLVED (FxFx DEFERRED) | (1) MG `systematics --alps=0.5,1,2` on the kept benchmark LHE (`scripts/run_alps.py`, 32 chunks, ≈ 0.2 CPU-h; ratios in `data/sim/aux/fixer/alps/`), applied per row via the row map; (2) V-SHOWER re-showers (`run_vshower.sh`); (3) FxFx → DEFERRED.md D-1; (4) VALIDATION §1.4 (l.169) now says the 9-point band is μ_F, not an ISR-shape band. Analysis `scripts/val_shower.py` → `results/shower.json`; VALIDATION §5.1 | ME α_s: f(pT>200) **+11…+15 % / −9…−11 %**, ℓ_max median ≤ 0.4 %. Shower μ_R ×½/×2: f +1.3/−1.6 ± 1.3 %, ℓ_max +1.2/−0.1 ± 2.4 %. **Tail rate +12…+15 % / −11…−13 %** (quadrature with merging and shower); shape ≈ ±5 % |
| **B-2** normalisation traps | RESOLVED | (i) see B6; (ii) σ_norm in every npz and the index; (iii) `xsec.json` key renamed `lo_mg_alpha127p9_fb` (`val_xsec.py:130`, `val_summary.py`); (iv) "Not included in σ_norm" box: SAMPLES.md:12, VALIDATION l.103, mg_events docstring | γγ +4.0-4.2 % (T6/S-20), Sommerfeld +5-15 % (TH §2.4/§5), NLO EW −few % (UNVERIFIED); nuisances ±5 % (K + scheme), PDF4LHC21 ±3.7/6.6/18.5 % |
| **B-3** weight columns, w = 0 rows | RESOLVED (documented) | SAMPLES.md:5 ("Read before using the arrays"): AUX_k ↔ LHE weight id map (1-44 scale×dyn, 45 central, 46-103 CT18 members, 104 NNPDF23LO), `Weight` = unmerged central, merging factor w/AUX_45, envelope recipes; w = 0 rows (13-21 %) explained. Columns kept (not converted): changing 2 GB of files for a documented convention is not minimal; the loader already drops w = 0. No `variations()` helper (the recipe is in SAMPLES.md and `val_xsec.bands`) | — |
| **B-4** effective statistics | RESOLVED | N_eff columns in SAMPLES.md (all files, TRGS table), VALIDATION §1.2 table (N_eff and N_eff/(0.18 N)); plan.md:239 restates the Stage-3 requirement in effective events. Top-ups via `produce.py --topup` (`produce.py:71,317`; existing merged file renormalised as one chunk, `merge_chunks.py:30`) | TRGS tail N_eff 200/300/400 GeV: **24.6k / 10.2k / 4.9k = 5.0× / 6.6× / 7.9×** the expected 3 ab⁻¹ signal after ε = 0.18 (was 12.3k / 4.4k / 4.9k = 2.5× / 2.8× / 7.9×). Criterion used: ≥ 5× after the Knapen-like ε = 0.18 of the review; before ε it is 0.9× / 1.2× / 1.4× (≥ 5× there would need ≈ 1 M more LHE at 200 GeV, beyond the budget) |
| **B-5** Stage-4 particles / row map | RESOLVED | `scripts/add_rowmap.py` adds `chunk, ievt_lhe, py8_job, ievt_job, py8_seed` to all 45 physics npz (6-D quirk-momentum matching to the kept LHE; block- and order-checked); `scripts/reshower.py` regenerates any Pythia job (+ `--keep-hepmc`); test `scripts/val_reshower.py` → `results/reshower_repro.json`; VALIDATION §6 (l.519); data/sim/README.md. HepMC not kept (approved) | **Bit-for-bit** reproduction of every kinematic column for E-INC 1500 c0 job 3 (1741 rows) and E-TRG 500 c0 job 0 (4513 rows); weights to 1e-13. Matching exact for ≥ 99 % of rows (Pythia's c/b on-shell rescaling moves ≤ 0.7 GeV) |
| **B-6** Λ grid | DEFERRED | DEFERRED.md D-2 (Stage-3 design) | — |
| **B-7** interpolation closure | RESOLVED (modest precision) | V-INTERP m550 INC 50k (`produce.py:61`), `scripts/val_interp.py` → `results/interp.json`, VALIDATION §4.5 (l.403); finer TRG test listed in DEFERRED.md | σ_matched −0.9 ± 0.9 %, f −0.8 ± 2.1 %, inclusive γ*−1 median −1.3 ± 1.0 %, tail ℓ_max median −4.2 ± 2.8 %, N_osc +0.3 ± 2.0 %; all \|pull\| < 1.5 |
| **B-8** template/toy split | RESOLVED | `tt_split` column (splitmix64 hash of (ID, m, chunk, ievt_lhe); `add_rowmap.py`) in all physics npz, carried into TRGS; `mg_events.py:66` `split='template'|'toy'` in `iter_events`, `sample_events_mg`, `sigma_*` (exact rescaling); SAMPLES.md rule | toy fraction 0.489-0.506; template/toy medians agree (val_loader) |
| **B-9** QED FSR | RESOLVED (diagnosis, card, docs) / NOT REGENERATED | Cause: `QEDshowerByOther` acts only on resonances, and the SLHA DECAY block resets `isResonance` (bit-identical test). Opt-in fix `cards/pythia8_quirk_qedfsr.dat` (+ `produce.py:50` option `qedfsr`); paired measurement `scripts/val_qed.py` → `results/qed_fsr.json`; VALIDATION §7 (l.533) and §0 item 9; photon rate corrected | 17 % of events radiate; P(E_γ > 5 GeV) = 2.0 % (first draft "10⁻³": ≈ 20× low). Tail median of ℓ_max **−0.7/−1.1/−0.1 % (E 200/500/1000), −0.5 % (Ẽ 500)**; mean −0.4…−0.8 %. Above 0.3 % → regeneration would be warranted; full re-shower ≈ 15 CPU-h > remaining ≈ 11.5 CPU-h: **decision for the orchestrator** |
| **B-10** figures | PARTIALLY / DEFERRED | = B9 above | — |
| C-1 d12 | RESOLVED | step test (B8) |
| C-2 K extrapolation ±2 % | RESOLVED | B/C-2 above |
| C-3 K(13.6) at 14 TeV | RESOLVED | VALIDATION §1.2, SAMPLES.md box |
| C-4 TRGS/INC tautology | RESOLVED | C-6 above |
| C-5 m1100 −5.4 % | RESOLVED (documented) | VALIDATION §1.2 note (≈ 2σ of INC stat) |
| C-6 Ẽ grid | NOTED | spin-bias test at 200/500 possible; no change |
| C-7 not-simulated box | RESOLVED | SAMPLES.md:12 |
| C-8 vertex/luminous region | NOTED | DEFERRED.md handover notes |
| C-9 η_pair vs per quirk | NOTED | DEFERRED.md handover notes |
| C-10 TRGS metadata | RESOLVED | `kind='stitched'`, `nlhe` = sum, `sigma_ref_fb`, originals `*_trg/*_inc` kept; `sigma_lhe_fb` deliberately not defined for a stitched file (`stitch_trg.py` docstring) |
| C-11 σ_norm/TH phrasing | RESOLVED | B3 above |
| C-12 stale plan header | RESOLVED | plan.md:3 status; plan.md:30 overturned probe claim with pointer to VALIDATION §4.4 |
| C-13 CP5 eigentunes | NOTED | VALIDATION §5 (only if Stage 4 shows UE sensitivity) |
| C-14 MET calorimeter deposit | NOTED | DEFERRED.md handover notes |
| C-15 stat error on f | RESOLVED | `f_stat_TRGS` (`val_xsec.py`), column "f stat" in VALIDATION §1.2 (0.3-2.8 %) |
| C-16 non-physics files | RESOLVED | `P-INC_m500.npz`, `T2compat_cache.npz` → `data/sim/npz/aux/` (index and `val_loader.py:128` updated) |

## Brief items not covered by a single review item

| Brief item | Status | Note |
|---|---|---|
| 15. MG install | RESOLVED | Removed exactly the 13 `.pyc` with birth time 2026-10-11, all absent from `MG5_aMC_v2.9.22.tar.gz` (0 `.pyc` in the release); sources identical to the release, so new files, not rewrites; pre-existing `__pycache__` directories kept. `input/mg5_configuration.txt`: removed the final blank line and the dangling `# MG5 MAIN DIRECTORY` (2 lines). Diff before → after: `review/r1_fix_mg_install/config_before_after.diff` (`235,236d234 <  / < # MG5 MAIN DIRECTORY`). After the fix the file equals the release template `input/.mg5_configuration_default.txt` except for the three HEPTools paths and the three MG-written `mg5_path` blocks, all of which predate E4 (`config_release_vs_after.diff`); `# auto_update = 7` unchanged. The three `mg5_path` blocks were kept (not stripped to the bare template), because the brief says "change NOTHING else" and they were present before E4. If the orchestrator wants the bare template tail, the remaining step is deleting the last 9 lines. Nothing else in the install was touched |
| 16. cheap C items, stale header | RESOLVED | above |
| Singlet wording | RESOLVED | C-1 |
| LOG line | DONE | `TT/LOG.md` (appended) |
| Propagation | DONE | Updated stale values: "+1…+15 %" (§0, §3) → −2.7…+14.8 % (mixed) / +26…+52 % (like-for-like); "≤ 7 % in d01" → full ranges; "±7 % justified" → ±5 % (VALIDATION §0, §1.3; plan D8, D8-approved row); "0.4-2 % of the stitched tail" → 3.9-7.3 % of σ (VALIDATION §4.4); "≈ 4-5×" → 4-11× (SAMPLES); "10⁻³" photon rate → 2 % (VALIDATION §7); "2.40 M LHE" → 2.07 M pre-fix / 2.41 M now (VALIDATION header, plan §4); "3.9-7.1 %" → 4.0-7.1 % after the E 200 top-up (VALIDATION §8, SAMPLES, plan); E 200/300 rows of every table (yields, bands, spectra, closure, budget, loader). Older lines of `TT/LOG.md` were not edited (append-only) |

## Items not done

1. **Regeneration with QED FSR off the quirks** (B-9): effect −0.1…−1.1 % (> 0.3 %), cost ≈ 15 CPU-h > remaining budget →
   orchestrator decision (re-shower with `cards/pythia8_quirk_qedfsr.dat`, or carry −1 % one-sided on ℓ_max).
2. Deferred by the brief: NLO + FxFx (D-1), Λ-grid extension (D-2), figure restyle (D-3): `DEFERRED.md`.
3. B-3 conversion of the AUX columns to merged ones: documented instead (see B-3).
