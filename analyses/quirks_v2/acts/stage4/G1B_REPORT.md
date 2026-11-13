# Stage 4, gate G1b report: signal (A1/A2/A5) and C′ (C′₀/C′_PU) job kinds; G3 navigation-assertion fix

Executor G1b, 2026-10-13 18:20–20:45. Authority: `plan.md` (R9), the frozen `WP_RULE.md` and `frozen_inputs.json`
(neither modified). Previous work: `G1_REPORT.md`.

The signal now goes through the finder (post-freeze). Signal numbers were looked at only for plumbing checks:
- hit counts and road membership;
- that the matched-efficiency flags fill.

No efficiency was tabulated or used for any choice.

## 1. Summary

| item | status |
|---|---|
| Job kinds `a1`, `a2`, `a5`, `cp0`, `cppu` (`run_g1b.py` + `finder/g1b_tt.py`, new files) | **READY**. Each kind passed a smoke run of 2 small jobs through `run_job`; `validate()` passes |
| Hook into `run_stage4.py` (dispatch, manifest, list-`needs`, V4-10 in `check`) | **PREPARED, not applied**: G3 is running (HASH_ADDENDUM §4). Tested as the candidate module |
| G3 failure (ACTS `GridPortalLink insideBounds` assertion) | **Diagnosed and fixed** (additive `run_chain.py` patch, prepared, not applied). Reproduced on G3B1_00021 (event 3). It is in Fatras, not the CKF, and goes away on the 1-sector geometry: a φ-sector portal artefact. The fix deterministically re-runs the job with that event's seed replaced and records the replacement |
| Regression (PU-only, SM, dens; frozen config) | **bit-identical**, frozen vs patched candidates (both files); determinism control also bit-identical |
| V4-1 | PASS on every smoke and cost job. A1/A5: chain + injected = measured on all surfaces + deposit equality. A2: PU chain + numpy counters. C′: chain |
| V4-10 | C′₀ leak = 0 (smoke, ni30; G1 test samples of all 8 topologies). C′_PU per-event hash 12/12 equal. Positive control of the necessity argument: **214/214** attributed C′_PU candidates contain a χ²₃ ≤ 48 triple |
| C1 manifest | 1 335 runnable G1b jobs + the 760 PU/SM/dens jobs (the latter unchanged, verified) = **95.7 CPU-h** (M3 1-process units) |
| **C1 ETA** at the measured G3 throughput (3.6–4.0 est-CPU-s per wall s) | **≈ 24–26 h** (G1b part ≈ 7 h). Over the one-day cap: decision D-1 below |

## 2. What each kind does (all at the frozen config: road = δ₉₅ = 0.15, η_max = 1.0, mip_gev, require_btl)

**Common TT step (`g1b_tt`).**
- **Pool.** `assemble()` is `chain_inputs.prepare_event` with one difference: the TDR top-up is drawn from the PU
  (non-inserted) barrel rows only.
  - With no inserted rows it equals `prepare_event` bit for bit (tested).
  - So the PU pool is identical at every Λ of a row (A2 pairing), and quirk or toy hits never change the PU top-up.
  - Then CKF removal and U-5 b merging, with INT = the largest-dE member.
- **Trial.** `trial()` calls the frozen `production.process_trial`, so the S1–S5 records are unchanged and packed by
  `run_stage4.pack`.
  - It also captures the finder output of the same call in-process (`finder.find` is wrapped for the call;
    `production.py` is not modified).
  - It recomputes the 43 rung flags of **every** candidate with the frozen helpers and **asserts** that
    F.sum(0) = `row['n_pass']` on every trial.

**Signal.**

| kind | content | chain | per event / trial |
|---|---|---|---|
| `a1` | 307 p2 + 60 mv points, all status-1 events (all η, both halves; 162 608 events), one job per point, mv with `--mat-scale` 0.5/2 | `sig --no-pu` | nominal trial + V4-3 variants W_c 50/100/150 mm and t_tol 0/100 µm (packed flags only) |
| `a2` | E200/500/1000/1500 + Ẽ500 × Λ {0.45, 0.6, 0.85, 1, 1.5, 2, 3, 5} keV; all template counting rows (1 000 rows); 10 rows per job | `pu --event-seeds` with hseed('sigpu', spin, m, row): the A5 sig-mode PU seeds | per (row, Λ): `s4sig.digitise`, the same top-up, PV/MET and trial seed at every Λ → trial |
| `a5` | 5 points: the 5 A2 species-masses at Λ = 1 keV (decision D-3), 200 template counting rows each, 10 rows per job | `sig` (full chain with PU) | trial + S6-style dumps of every event (TT-level variations) + V4-6 |

- **PV/MET** (plan §1.7):
  - PV = Stage-3 vertex ⊕ (10, 10, 15) µm;
  - MET = truth pair pT (p_qp + p_qm; = −recoil to 0.5 %) ⊕ 25 GeV per component;
  - both drawn from hseed('sig-pvmet', spin, m, row), so they are the same in A1/A2/A5 and at every Λ.
- **Efficiency flags per trial and rung (`sig.eff*`).** The plan §2.4 definition: some candidate passes the rung and
  holds ≥ 50 % of the event's written barrel quirk measurements.
  - These are counted pre-CKF and pre-merge, so CKF stealing and merging count as losses.
  - Variants: `eff_fckf` (+ f_CKF < 0.2, WP_RULE §1.2), `eff_T` (+ BTL present), `eff_fckf_T`.
  - Every candidate with ≥ 1 quirk link is stored (`sig.cand.*`: nq, frac, rungs, f_CKF, BTL, vars), so any other
    threshold can be applied offline.
- **Per-trial table `sig.tab`:** row, Λ, status, probe_excluded (WP_RULE §5.4 item 10, flagged and still run),
  n_q_written / ckf / pool / road, best_frac.
- **Quirk BTL hits** are stored per trial (`sig.qbtl`); the PU BTL is stored once per row.

**C′ (WP_RULE §7).**

| kind | content |
|---|---|
| `cp0` | 8 topologies, 5.4 × 10⁵ events, 5 000 per job (108 jobs). No PU, no top-up |
| `cppu` | 8 × 500 slots, 20 per job (200 jobs); `needs` = all C′₀ jobs of the topology |

Each `cp0` event:
1. the V4-10 hash of the pre-CKF, pre-merge toy measurements + PV;
2. the exhaustive-triple preselection (χ²₃ = λ_min(Σ uuᵀ/σ̂²) ≤ 48 about the stored PV, 3 distinct layers, ≥ 2 toy
   particles). Particle identity = full SimHit barcode incl. subParticle, matched by truth position: conversion
   e⁺e⁻ are distinct;
3. `process_trial` at the stored PV and road;
4. attribution of **every** candidate:
   - ≥ 3 core toy links in ≥ 3 layers, ≥ 1 of them IT + PS;
   - each within 4σ̂ of the candidate plane at its stored C′₀ position;
   - ≥ 2 particles (looper: ≥ 2 crossings in a layer);
   - merged measurements are tested per toy link.

C′₀ stores the toy measurements and SimHits of the events C′_PU may overlay: guns with global index < 500, NI/DIF
preselected.

Each `cppu` job:
1. **Refuses** if V4-10 failed for its NI/DIF topology (leak > 0).
2. Slot s overlays source event pre[s mod N_pre]. N_pre = 0 writes an empty "not run" output.
3. Inserts the stored SimHits (`run_chain.py cppu`).
4. Replaces the with-PU toy rows by the stored C′₀ rows, matched one-to-one by truth position; the CKF flag is kept
   from the with-PU event.
5. Checks the per-event hash, then top-up (PU rows), trial and attribution, with the stored PV and road.
6. **Positive control:** every attributed candidate's own passing links must contain a preselection triple
   (WP_RULE §7 "why f_pre is exact").

Records cover attributed candidates plus near misses (≥ 2 passing links).

## 3. Validation

**V4-1.**
- `a1`/`a5`: chain `v41_pass` (incl. the G1 lost-SimHit tolerance) and `sig_v41_pass` (injected = measured on all
  surfaces, deposit equality, numpy bookkeeping) are both required.
- `a2`: chain `v41_pass` and 0 numpy V4-1 failures over every (row, Λ).
- `cp0`/`cppu`: chain `v41_pass`.
- All smoke and cost jobs: PASS.

**V4-6 (A5).** Quirk measurements on CKF tracks: 0/69 (smoke, 2 events), recorded per job (`meta.v46`).

**V4-10.**
- **C′₀ leak** (attributed candidates at any rung in non-preselected events) = 0 in every test: smoke ni30 200 events;
  G1 test samples 50 events × 8 topologies.
- Caveat: without PU, C′₀ candidates are rare (0 in these samples). The leak test is therefore mostly carried by the
  full C′₀ sample.
- f_pre in these small samples: ni22 0.74, ni30 0.84–1.0, ni61 0.92, DIF 0.76. This is above the plan's ESTIMATE
  0.07–0.5 at 22 mm, as σ̂ can only raise it.
- **C′_PU hash:** 12/12 events equal (23/15/… toy measurements matched one-to-one, 0 unmatched).
- **Positive control:** 8 C′_PU ni30 events (preselected sources) gave 214 attributed candidates, 162 of them at some
  rung. The implication test passed **214/214**.
- **Physics note (not a bug; diagnostic in `scratchpad/diag.py`, summarised here):**
  - Single-prong-line candidates collect up to 12 toy links in 6 layers but only 1 particle. They are B_PU by rule.
  - The parent's L1/L2 hits often fail 4σ̂ about the prong plane (helix and MS).
  - So attributed counts per event vary strongly (0–111). C1 measures them.

**Regression and hash addendum:** HASH_ADDENDUM.md §3. PU/SM/dens are bit-identical (97/86/82 keys); the chain fix is
bit-identical without replacement, and with replacement the other events are bit-identical.

## 4. G3 failures: diagnosis and fix

- **Errors.** G3B1_00021 (19:01) and G3B1_00059 (20:03): `RuntimeError: Checking volume outside of bounds: Assertion
  'surface().insideBounds(position, BoundaryTolerance::None())' failed` (`GridPortalLink.hpp:584`) inside
  `Sequencer.run()`. One bad event kills the 25-event job.
- **Reproduced on G3B1_00021.** The failing event is event 3, with seed 3930681229184174995.
- **Where it happens:**
  - with `--no-ckf` it fails identically, so it is the Fatras propagation;
  - with `--nphi 1` the same events run, so it is the Gen-3 grid portals between the 32 φ-sectors (sector-boundary
    artefact).
- **Rate:** ≈ 1/700 events.
- **Why not a geometry fix.** A tolerance or geometry fix changes every event (not bit-identical; needs a re-validation
  of V4-9).
- **The fix.** Deterministic event replacement on exactly this assertion (HASH_ADDENDUM §2):
  - the first event without a Dump record is re-seeded with hseed('nav-replace', …);
  - the job reruns in-process;
  - at most 5 replacements; listed in `chain_meta.replaced_events`.
- **Patched candidate on G3B1_00021:** completes, event 3 replaced, V4-1 PASS, 303 s.
- **To do after G3:** rerun the 2 failed jobs. The decision on admitting them to the G3 union is open (D-2).

## 5. Costs (measured)

Measured under load: 7 G3 workers + ≤ 2 G1b processes on the 8-core M3; G3 wall/estimate = 1.74.

| kind | measured | manifest estimate (1-process units) | jobs | CPU-h |
|---|---|---|---|---|
| A1 | 0.029 s/event loaded (496-event point: 14.4 s/job incl. 6 finder configs) | 0.03 s/ev + 12 s/job | 367 | 2.6 |
| A2 | 56 s per row loaded (PU chain 11.9 s + 8 × 5.5 s), = 1.74 × the estimate | 4.83 + 8 × 3.41 s per row | 100 | 9.3 |
| A5 | 20.9 s/event loaded (incl. job overhead; 4.4 MB dumps per 2 events) | 8.7 s/ev | 100 | 2.7 |
| C′₀ | 0.012 s/ev (ni22), 0.0015 (γ); loaded | 0.012 s/ev | 108 | 2.2 |
| C′_PU | 18.5–20 s/event loaded | 8.4 s/ev | 200 | 10.0 |
| **G1b total** | | | 875 + 460 | **26.8** |
| PU B1/B2, SM, dens (unchanged) | | | 760 | 68.9 |
| **C1 runnable** | | | 2 095 | **95.7** |

`val` (15 CPU-h) stays a placeholder, not run. Disk:
- A5 ≈ 2.2 GB;
- C′₀ ≈ 0.6 GB (stored overlay sources);
- C′_PU ≈ 0.15 MB/event;
- A2 ≈ 0.27 MB/row.

**ETA.** 95.7 CPU-h / (3.6–4.0 est-CPU-s per wall s, measured on G3) = **24–27 h wall** (G1b ≈ 7 h).
- Without the dens B-9 re-run (15.9 CPU-h), C1 is ≈ 20–22 h.
- The plan's pre-defined sub-runs: C1a = A1, A2, A5, C′ ≈ 27 CPU-h ≈ 7–8 h; C1b = B1, B2, C, dens ≈ 69 CPU-h
  ≈ 18–19 h.

## 6. C1 readiness and the exact launch sequence (run only AFTER G3 has exited and passed)

```
cd /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track
acts/stage4/validation/g1b_post_g3.sh          # applies both patches (sha-checked), regression on applied files,
                                               # deletes the candidates, regenerates jobs/C1.json
# (optional, orchestrator decision D-2) rerun the 2 failed G3 jobs with the fixed chain:
#   pixi run python -m acts.stage4.run_stage4 run --campaign G3 --workers 2
mkdir -p data/acts_stage4/prod/C1
nohup caffeinate -i pixi run python -m acts.stage4.run_stage4 run --campaign C1 --workers 7 --mem-gb 19 \
      > data/acts_stage4/prod/C1/run_stdout.txt 2>&1 &
pixi run python -m acts.stage4.run_stage4 status --campaign C1      # progress / ETA
pixi run python -m acts.stage4.run_stage4 check  --campaign C1      # V4-1 + V4-10 per output
```

Job order (the runner's `order`, then the longest first):
- 0: C′₀ and B1;
- 1: A2, A5, B2, SM;
- 2: C′_PU (after its C′₀) and dens (after its B1);
- 3: A1.

## 7. Decisions / flags

- **D-1 (C1 > 24 h).** At the measured G3 throughput C1 is ≈ 24–27 h. Options:
  - (a) run it as is;
  - (b) the plan's C1a (G1b blocks, ≈ 7–8 h) then C1b (≈ 18–19 h);
  - (c) defer dens (B-9) to its own run (−16 CPU-h).
- **D-2 (G3 provenance).** The 2 failed G3 jobs can only be produced with the patched (hash-addendum) files. Should
  they be rerun and admitted to the union?
- **D-3 (A5 core points; plan says only "5 points").** G1b chose the 5 A2 species-masses at Λ = 1 keV. This gives
  paired rows and the same PU generator seeds as A2, for the numpy-vs-ACTS check. One constant (`A5_LAM`) changes it
  before the manifest is regenerated. CONFIDENCE MEDIUM.
- **D-4 (matched definition with few quirk hits).** With the ≥ 50 % rule, events with 2–5 barrel quirk hits (forward
  pairs) are "matched" by a PU candidate holding 1–2 of them. The per-candidate nq and frac are stored, so a minimum
  nq (e.g. ≥ 3) can be imposed offline. FLAG for the efficiency definition.
- **Other choices (flagged):**
  - A1 uses status = 1 events only (162 608 of 162 771; status ≠ 1 is an efficiency loss per HANDOVER);
  - probe-excluded rows are run and flagged, not dropped;
  - MET = pair pT (not −recoil; 0.5 % apart);
  - the top-up base excludes inserted rows in A2/A5/C′_PU;
  - C′ near-miss records = ≥ 2 passing links.
- **Navigation-replacement bias:** ≈ 0.14 % of events are conditioned away; the replaced ids are listed per job.

## 8. Files

- **New:**
  - `acts/stage4/run_g1b.py`, `acts/stage4/finder/g1b_tt.py`;
  - `acts/stage4/validation/{g1b_apply_hook.py, g1b_apply_chainfix.py, g1b_regress.py, g1b_chainfix_test.py,
    g1b_post_g3.sh}`;
  - `acts/stage4/HASH_ADDENDUM.md`;
  - candidates `acts/stage4/_rs4_candidate.py` and `acts/stage4/code/_run_chain_candidate.py` (deleted by the post-G3
    script).
- **Data:**
  - `data/acts_stage4/prod/smokeG1b/` (smoke + cost jobs);
  - `data/acts_stage4/prod/_regress/`;
  - `data/acts_stage4/g1b/` (regression JSONs, navfix logs and test, frozen copies).
- **Compute:** ≈ 1.2 CPU-h (≤ 2 processes, nice 15).
