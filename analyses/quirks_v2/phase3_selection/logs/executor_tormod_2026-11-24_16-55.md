# Session log — Tormod (executor, Opus), work package p3-g: channel (i), B1 + B3 development

Started 2026-11-24 16:55 -0500 (from `date`). Brief: orchestrator prompt of 16:46 + `PHASE3_BRIEF.md`.
Abbreviations: STR, ADD, EXP, COM as in the brief; P3A = `outputs/P3A_PILOT_FINAL_aurora_2026-11-24.md`.

## Read before planning (done 16:00–16:55)
AGENT_RULES, CLAUDE.md overrides, agents/executor.md, phase3 CLAUDE.md, PHASE3_BRIEF; STR §4.0 (l.340-548), §4.4
(l.724-1118), §4.6 (l.1229-1296), §2 (route table, B1-g, l.197-282), §4.17 rows 11/13/13a, §11.7; COM rows B1-a…g,
B3-a…d and the version-4/5 and addendum-1 amendment rows; ADD §0.3, §1, §2, §3 (P1–P7); EXP §0–§2, §5, §7, §9, §10,
§12; P3A (all); ESK; Kari's NI note (EXP §7 box); P3B v4 §4 (occupancy model); retrieval_log (R-7, R-18).
Code read: p2x_b1.py, p2u_d2_chain.py, c1_cp_job.py, c1_pu_job.py, cpu_attrib.py, run_chain.py (main, Inject,
build_sequencer), run_stage4.run_pu_job, run_g1b.run_cppu_job, g1b_tt (assemble, trial, cand_extra, replace_toy_rows),
p3a_multi.do_variant, p2w_subset.classify_pool, p3b occ_model header. Pilot file schemas read from the npz metadata.

## Facts that shape the plan (Phase 1 assumed / Phase 3 finds)
1. **The pilot's B1 samples hold no near-pass event** (P3A §3.3: one DIF-C looper row in 1.92×10⁷ events × orientations,
   none at any T2 candidate). STR l.840 / l.874-875 assumed the 1,000 near-pass overlays of sample 11 would be made of B1
   near-pass events. The only near-pass population of the pilot is the Z(νν) sample (13,923 rows at R04, k ≤ 3).
   Reading used (and the only executable one): the near-pass overlays of sample 11 are Z(νν) pilot near-pass events
   (sample 11 includes the Z(νν) pilot). Stated as a reading, not chosen among alternatives (no alternative exists
   except the single DIF-C row, which is also overlaid and reported apart).
2. **Unbiased DIF overlays (13a) are expected to hold ≈ 0 attributed candidates** (H_DIF = 0 in 8.4×10⁷ (event,
   orientation); ESK: 0 of 1,000 at R04–R05 under the frozen rule). The DIF ceiling and completeness tests on 13a will
   therefore have ≈ no power; S_CKF on 13a is undefined if no class event exists. This is measured, not assumed.
3. **Z pilot files store hits, truth positions, PV seed and MET axis, not SimHit momenta**; B1 files store full
   SimHits (`toy`). So: DIF overlays = v1's `cppu` mode with the stored SimHits (no chain-code change); Z overlays =
   the same mode with SimHits built from the stored truth positions and times (momentum direction PV→hit, |p| = 1 GeV,
   a placeholder that the smearing digitisation does not use: checked on a no-pile-up test before any campaign).
   After the chain, own rows are replaced by the stored no-pile-up rows (v1 `replace_toy_rows`, CKF flag from the
   pile-up event): the own measurements are then identical to the ones P3A classified.
4. **The occupancy model of p3-b treats layers as independent Poisson** and carries one measured plane-level
   correlation factor C(R04) = 1.184, C(R05) = 1.207 (P3B v4 §4.2); there are no layer-to-layer factors. π_k is
   predicted from that model under two readings (C applied / not applied), none chosen.
5. **R-7 tail fraction not sourced** (retrieval_log #24): B3-c "no credit is taken" (STR l.1285-1287) applies as
   written. Footprint derivation still reported if cheap.
6. Sample 5 (C1 Z(νν) hit level) was run with `--dump 0`: no event pools, so the paired pile-up-only pass needs the
   events regenerated (same seeds: the nominal trial must reproduce the stored candidates bit for bit — a check).
7. Geant4 injection unit cost 2.0× plan (EXP §5.6, D2): used for dev.g4pu.

## Plan

### Code (`phase3_selection/src/p3g/`; Phase-2 and v1 code imported, never edited; no chain file changed)
- `p3g_common.py` — paths, constants (rung indices from `production.RUNGS`, layer maps), attribution j per class
  (Eskil's definition: IT ≥ 2 own hits, PS ≥ 2 on each sensor, 2S likewise for the s = 3 family), logging.
- `p3g_prep.py` (worker, one pass) — builds the overlay source lists: (a) 1,000 Z(νν) near-pass events stratified by
  their BASE (S) class at R05, s = 0: k = 0 / 1 / 2 / 3, 250 each, drawn with a fixed seed from the P3A rows of label m
  (+ the one DIF-C row); (b) 1,000 unbiased DIF events = a seeded draw without regard to class from the pilot DIF
  files (stream `dev.ovl.dif`); writes compact source files (stored hits, truth, SimHits, PV, road axis, class).
  Small files on cajuela (one per campaign block), so jobs never stream the 93–320 MB pilot files.
- `p3g_ovl_job.py` (tt env, runner job) — overlay job: writes the cppu source file, runs v1 `run_chain.py cppu`
  (PU 200 + stored SimHits inserted), replaces own rows, then per event:
  T1 nominal trial (frozen config, CKF removal, top-up from PU rows only, merging) → candidates at R01–R43 with j_own,
  j_pu, f_CKF, n_own hits; T2 "own hits not CKF-removed, no f_CKF cut" (factorises π_k from S_CKF; npo only);
  T0 paired pile-up-only pass, own hits removed (13a and zhl). Own-hit class of the event (P3A classifier imported,
  unchanged) and its witness (plane, own crossings per layer) stored for the π_k prediction. Modes: `npo` (Z near-pass),
  `dif` (13a), `zhl` (sample-5 regeneration through v1's `sm` chain, own = vp 3000).
- `p3g_g4pu_job.py` (acts + g4 env) — dev.g4pu: PU 200 event; every pile-up hadron (π±, K±, p, K⁰_L, n, and γ for
  photonuclear only) fired through Geant4 (FTFP_BERT, existing `p2c_g4vtx.run_g4`), its decay / inelastic vertex
  products handed to Fatras by the frozen hand-over rule (slab exit, β < 0.1 dropped, parent truncated: radius cut for
  first-arc, option (a) for after-a-turn), each secondary once, own z; then chain + 4 finder trials; truth classes per
  hit (Fatras pile-up particle / Geant4 product with its vertex id). Built from p2x_b1 / p2c_handover / p2u_d2 pieces.
- `p3g_pik.py` — π_k prediction per near-pass event from the p3-b occupancy model (densities of the ρ = 1 development
  pool; band of the event's own witness plane; Poisson toys for the missing layers with the own hits fixed; R04 and
  R05 widths); readings C-applied / not.
- `p3g_tests.py` — every development test against its frozen criterion: ceiling (exact conditional Poisson test,
  Šidák), leak, mixed excess (paired readings), completeness bound 0.26, per-k comparison (classes ≥ 24 promoted,
  r.m.s. of ln(obs/pred) = s_model, cap 0.231), S_CKF with 68 % upper values, B1-g secondaries rule, NI test re-sizing,
  B3-a/B3-d conditionals on the Z pilot finder candidates (existing p2t outputs) where they exist.
- `p3g_plots.py` — figures (plotting separated), `test_p3g.py` — synthetic tests of j, the Poisson test, Šidák.

### Campaigns (prefix `p3-g-`; development role; none is pilot/production; CPU-h [ESTIMATE from EXP §3.1 unit costs:
chain 13.5 s per PU-200 event, finder trial 11.3 s; Geant4 injection 2.0× chain])
| campaign | sample (STR §4.17) | events | jobs | per event | CPU-h |
|---|---|---|---|---|---|
| p3-g-npo | row 11 near-pass overlays (Z near-pass, stream `pilot.ovl`) | 1,000 (+1 DIF-C) | 25 × 40 | chain + T1 + T2 ≈ 36 s | 10 |
| p3-g-ovldif | row 13a unbiased Geant4 DIF overlays (stream `dev.ovl.dif`) | 1,000 | 25 × 40 | chain + T1 + T0 ≈ 36 s | 10 |
| p3-g-g4pu | row 13 pile-up with Geant4 secondaries (stream `dev.g4pu`) | 1,000 (4,000 trials) | 100 × 10 | G4 ≈ 7 s + chain 27 s + 4 trials 45 s ≈ 80 s | 22 |
| p3-g-zhl | row 5 regenerated (stream `c1.sm`, same seeds) + paired pass | 1,000 | 25 × 40 | chain + T1 + T0 ≈ 36 s | 10 |
| tests, prep, analysis | smoke jobs (≤ 10 min), prep pass, π_k toys | — | — | — | ≈ 5 |
| **total** | | | | | **≈ 57 of 73** (stop and report before 95) |
Reserve ≈ 15 CPU-h: NI development overlays (pilot NI 30 / 61.5 mm, 500 each, the NI R05 re-sizing input) only if
the four above end within budget.

### Order
1. Code + synthetic tests (einstein editing only). 2. maxwell 1-job smoke tests ≤ 10 min (only with ≤ 3 qv2run jobs
there): no-PU injection check (Z own SimHits re-digitised → same written count, positions within smear), a 2-event
overlay, a 1-event g4pu. 3. When schrodinger is assigned (≤ 3 jobs): prep, then npo and ovldif, then g4pu, then zhl.
4. Analysis, figures, artifact `outputs/P3G_B1B3_tormod_<date>.md`, JSON in `outputs/p3g/`. Target: well before Thu 3 Dec.

### Pre-declared checks
- C1: injected own SimHits without pile-up give the same number of written measurements as stored (V4-1 style) and
  `replace_toy_rows` matches one-to-one. C2: the zhl nominal trial reproduces the stored sample-5 candidates (count per
  rung) for the regenerated jobs. C3: j recomputed agrees with Eskil's on one C′_PU file. C4: Poisson test reproduces
  the STR substitutions (8 in 4,000 vs 500 in 10⁶ → p = 0.0011; vs 2×10⁻³ → 0.55). C5: on the npo sample the k = 0
  class gives survival ≤ 1 and the T1 ⊂ T2 relation (with CKF never more passes than without own-CKF) holds per event.

### What I deliver
Artifact with each test's verdict against its frozen criterion (PASS / FAIL / NOT TESTED / NOT EVALUABLE as STR §4.0
point 5), the decision-point-2 numbers in one table, every open reading reported under each reading, CPU table.
