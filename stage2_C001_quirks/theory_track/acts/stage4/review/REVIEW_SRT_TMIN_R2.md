# REVIEW_SRT_TMIN_R2: narrow verification of the round-2 SR-T window fix (FIX_SRT_TMIN_R2, proposed PC-19)

Fresh critical reviewer (narrow verifier), 2026-10-14.

**Target.**
- `acts/stage4/review/FIX_SRT_TMIN_R2.md`, including the PC-19 block in §5.
- `acts/stage4/g3/srt_tmin_check.py --version v2`.
- `data/acts_stage4/g3/srt_tmin_check_v2{,_spv150,_spv230,_st60}.json`.

**Read.**
- The reviewer spec and `methodology/03-review.md`.
- `FIX_SRT_TMIN_R1.md` and `REVIEW_SRT_TMIN_R1.md`.
- WP_RULE §1.4 (l.184-210), §4.1-4.2 (σ_ln, the zero-count rule), §6.2 (the PC-18 composition, l.468-472) and the
  PC table.
- `weights._btl_inband` and `btl_band`; `run_stage4.py` l.355-470 (the PV draw, the `btl` and `trials` storage).
- `code/s4pu.py` (PU vertex times, `hs_vtx`); `code/s4sig.py` l.118-140; `sim/stage3/code/make_inputs.py` (signal
  `vtx_lumi`, σ_t = 0.190 ns); plan l.288.

**Signal-blindness.**
- No signal efficiency, signal sample or signal yield was computed or opened.
- Signal-side code was read only to confirm where the vertex time comes from.

**Compute.**
- The reviewer's independent code (scratchpad only, not in the project) made 2 runs of about 80 s each, on 1 core at
  nice 15, reading the G3B1 files (77 jobs).
- One run had a bug in the reviewer's own code (partners e+2 and e+3 shifted by 50 and 75 ns). It was fixed and re-run.

## Verdict

**ITERATE (narrow): 0 A, 1 B, 6 C.**

- All R1 findings (A-1, B-1, B-2, B-3) are resolved.
- Every key number in the FIX and the JSONs was reproduced exactly by the reviewer's independent implementation.
- The PC-19 block is signal-independent, conservative for B, computable from stored fields, and matches the v2 script.
- The one B is a text gap in the new σ_t,PV → σ_ln proposal. Its formula, scope and low-count fallback are unspecified,
  so applying it as written would need a post-hoc choice. The fix is one sentence; no re-run is needed.

---

## 1. Independent re-check (reviewer's own code)

**What the reviewer's code does.** It is a re-implementation from the WP_RULE text, and it does not import
`srt_tmin_check`.
- **In-band.** The §1.4 in-band test is written in the reviewer's own numba kernel: u·n₃ > 0, |u·n₂| < W_c,
  d² < 9(max(σ_n, 10⁻⁴)² + t_tol²), with t_tol and W_c from `meta.finder_cfg`.
- **PV time.** Per event, z = `default_rng([trial_seed(road 0), 0x5254]).standard_normal()` and t_PV = σ·z. The stored
  quantity is Δt at t_PV = 0 plus z, so every σ_PV comes from a single pass. This is valid because the raw-t order is
  t_PV-invariant.
- **Mixing.** Partners e+1, e+2, e+3 (mod n_ev), each shifted by +25 ns.
- **Edges.** Taken from exact sorted per-(candidate, hit) values on a 5 ps grid, with no histogram binning.

**Results.** Each row compares FIX R2 / JSON against the reviewer's value.

| quantity | FIX R2 / JSON | reviewer | |
|---|---|---|---|
| v1 (t_PV = 0) edges | 6.12 / 24.275 | 6.12 / 24.275 | ✓ |
| v1 loose late in / OOT (e+1) | 34 (17 ev) / 31 (12 ev) | 34 (17) / 31 (12) | ✓ |
| v1 R04 late in / OOT | 48 (11) / 10 (4) | 48 (11) / 10 (4) | ✓ |
| **v2 edges, σ_PV 190 ps** | **6.07 / 24.025** | **6.07 / 24.025** | ✓ |
| v2 per-hit R₀ / R₊₁ in the window | 9.6e-5 / 9.3e-5 | 9.58e-5 / 9.31e-5 (N₀ = 594 708, N₊₁ = 569 068) | ✓ |
| in-time Δt range at v2 | −1.34 … +6.64 ns | −1.340 … +6.645 ns | ✓ |
| loose: in-time late, P(late \| present) | 36 (18 ev), 7.4e-5 | 36 (18), 7.38e-5 (of 487 729 present) | ✓ |
| loose: OOT late per partner, P_oot | 39/20/24 (12/7/9 ev), 1.9e-5 | 39/20/24 (12/7/9), 1.87e-5 | ✓ |
| loose SR-T PU fraction | 3.24e-5 | 3.242e-5 (N = 1 963 659) | ✓ |
| R04: in-time late; OOT per partner | 48 (12); 16/8/19 (7/4/5) | 48 (12); 16/8/19 (7/4/5) | ✓ |
| R04 SR-T PU fraction | 3.42e-5 | 3.417e-5 (N = 1 824 063) | ✓ |
| R1 window [6.12, 24.275] at 190 ps (loose / R04) | 2.49e-4 / 1.46e-4 | 2.49e-4 / 1.46e-4 | ✓ |
| 25 ns upper edge at 190 ps (loose / R04) | 3.13e-2 / 2.01e-2 | 3.13e-2 / 2.01e-2 | ✓ |
| σ_PV 150: edges; own-edge fraction; fraction in the fixed window | 6.08/24.10; 2.95e-5 / 3.02e-5; 2.24e-5 / 2.65e-5 | 6.08/24.10; 2.95e-5 / 3.02e-5; 2.24e-5 / 2.65e-5 | ✓ |
| σ_PV 230: edges; own-edge fraction; fraction in the fixed window | 6.115/23.925; 3.16e-5 / 3.45e-5; 5.84e-5 / 4.64e-5 | identical | ✓ |
| stored `btl_dt0` − t_PV vs recomputed | 7.9e-7 ns, 3 n_band mismatches | 7.9e-7 ns, 1 + 2 mismatches | ✓ |
| raw-t vs min-Δt ordering disagreements | 0 / 0 | 0 / 0 | ✓ |
| candidates with an in-time in-band Δt ≥ t_min + 25 (k ≤ −1) | 0 / 0 | 0 / 0 | ✓ |

**Additional reviewer checks.**
- **Shared PV.** The 4 roads of an event share one stored PV: 0 of 250 events (10 jobs) have differing `trials.pv`. This
  confirms the per-event t_PV. `run_stage4.py` l.379 draws `lum_pv` once per event.
- **k ≤ −1 via mixing.** The *mixed* independent-crossing per-hit spectrum (e+1 hits, unshifted) also ends at +6.61 ns.
  0 of 569 068 hits have Δt ≥ 31.07 ns, so k ≤ −1 = 0 is confirmed by mixing as well as by the copy method.
- **Signal t_PV consistency.** Signal `vtx[3]` comes from `make_inputs.py` with SIG_T_NS = 0.190, and SM `hs_vtx[3]` from
  `s4pu` with `sigma_t_ps`. Both are drawn from the same luminous-region σ_t as the PU vertices, so B-3(i) is consistent
  (VERIFIED).

## 2. Status of the R1 findings

- **A-1: RESOLVED.**
  - t_PV ~ N(0, 190 ps) per event, seeded from `trials.trial_seed` (road 0, salt 0x5254), is defined in the rule. It is
    used for the edges, P(late) and P_oot.
  - The edges were re-derived as [6.07, 24.025] ns and reproduced independently.
  - The R1 window under-states B by ×7.7 / ×4.3, reproduced. The decision table was redone.
  - The difference from the R1 reviewer's 24.08 ns is draw-to-draw. R1 used per-trial draws with a fixed seed; R2 uses
    per-event draws. The 10⁻⁴ edge rests on about 55 hits, so this is expected.
- **B-1: RESOLVED.**
  - k ≤ −1 delayed hits stay in B as a separate line, P_{k≤−1}.
  - The per-hit "disjoint windows ⇒ a single 3/N bound" argument is correct: the 12 windows are ≈ 18 ns wide at a 25 ns
    pitch.
  - The value is 0 at G3, by both copy and mixing (reviewer).
- **B-2: RESOLVED.**
  - The PC-19 text conditions P_oot on "without an in-time in-band BTL hit".
  - The script divides by (¬present).sum(), and so does the reviewer.
- **B-3: RESOLVED.** Each of the three signal-side choices is pre-declared with a reason:
  - (i) the true vertex time: consistent, verified above;
  - (ii) veto yes, credit no: the lower-ε choice;
  - (iii) raw-t ordering: 0 disagreements on B, reproduced.
- **C-1 to C-6:** addressed as stated (see C-1 below for a label slip in the C-2 prose).

## 3. The PC-19 block

**Self-consistency.**
- t_max = min(Δt_acc, largest t ≤ Δt_bx with R₊₁(Δt_bx/2, t) < 10⁻⁴), then t_min = smallest t ≥ 0 with
  R₀(t, t_max) < 10⁻⁴. Both are monotone and well defined. The edge uses partner e+1 only, while P_oot uses the mean over
  e+1..e+3, and the text says exactly that.
- **Composition.** P̂₁(r ∧ present)·P(late) + P̂₁(r ∧ ¬present)·[P_oot + P_{k≤−1}].
  - It is exact for the G3 spectra. For a present candidate, the in-time earliest hit (Δt ≤ 6.64 ns) always precedes
    any k = +1 hit (≥ 23.8 ns), and no delayed k ≤ −1 hit exists.
  - In general, ignoring a k ≤ −1 hit that precedes the in-time hit only drops a veto, which is conservative.
- **Signal-independent.** Both edges are quantiles of PU-only B1 spectra at a frozen threshold. σ_t,PV is a plan
  constant.
- **Conservative for B.** Excluding prompt previous-crossing hits from "earliest" can only remove vetoes. B is measured in
  the same window it is derived on; the even/odd split (C-2) shows a +7 % / −1 % same-sample effect. The 10⁻⁴-per-edge
  budget is flagged as a user design choice.
- **Computable from stored fields.**
  - Inputs: `trials.trial_seed`, `trials.ev/road/pv`, `cand.normal/axis/trial/tag/rungs`, `btl` (with t and INT),
    `btl_dt0` and `btl_n_band`. All are present in the G3B1 files, and C1 uses the same runner.
  - P(late | present) follows from `btl_dt0` − t_PV alone (7.9e-7 ns agreement).
- **Matches the v2 script.** The R_k definitions, the edge order, the mixing about the candidate's own plane, axis, PV and
  t_PV, P_oot conditioning, raw-t "earliest" and the salt 0x5254 = 21076 (as in the frozen_inputs proposal) all match.
  The minor differences (binning/grid, k ≤ −1 proxy) are listed as C-3 and C-4.

## 4. Findings

### B-1. The σ_t,PV variation into σ_ln is coherent in kind, but underspecified as rule text.

**Coherent part.**
- Holding the window fixed at the nominal edges and varying the model parameter is the right way to cover a mis-modelled
  luminous-region time spread: the window would not be re-tuned.
- It parallels the PC-11 density term, a model variation entering the log-normal σ_ln of a B factor.
- G3 reproduces ×0.69 / ×1.80 (loose) and ×0.77 / ×1.36 (R04).
- The variation is a real shift, not noise: the same z draws are used, and loose OOT counts go 39/20/24 → 85/61/81 at
  230 ps.

**Missing from the PC-19 block.** "enters σ_ln of B_SR-T (G3: ×0.7 to ×1.8)" does not say:
- (a) **The formula.** For example σ_ln,PV = max(|ln(P₁₅₀/P_nom)|, |ln(P₂₃₀/P_nom)|), the conservative choice for an
  asymmetric ×0.7 / ×1.8, as in PC-11.
- (b) **The quantity varied.** It should be the SR-T late composite f_pres·P(late) + f_¬pres·[P_oot + P_{k≤−1}], on the
  §4.2 measuring population of these factors. It should not be a deep-rung count, which will be 0 at the working-point
  rungs and make the ratio undefined. A ≥ 10-count condition and a fallback are also needed, e.g. the value at the
  tightest population with ≥ 10 counts in all three runs, as PC-11 does.
- (c) **The scope.** It should apply to B_PU's SR-T term only. In the SM samples t_PV is the true `hs_vtx[3]`, which is
  not varied.
- (d) **The §4.1 σ_ln² decomposition.** The line σ_ln² = stat² + model² + dens² + norm² needs the new (σ_t,PV)² term, or
  the term must be declared part of the "extrapolation-model spread".

**Why B and not A.** It is signal-independent, and every number needed is already computed. But the rule fixes B₈₄,
and so the working point. Leaving the formula and fallback open would force a choice after C1 B1 is seen.

**Fix.** One sentence in the PC-19 §6.2 block covering (a)-(d). No re-run is needed.

### C (optional)

- **C-1. FIX §1 "C-2" prose swaps the parity labels.**
  - The JSON has `edges_even_jobs` = [6.205, 24.025] and `edges_odd_jobs` = [5.95, 24.025]. The FIX says even = 5.95,
    odd = 6.205.
  - The fractions quoted (2.61e-5 measured on odd, 4.32e-5 on even) are correct for the JSON labels.
- **C-2. Provenance.** `srt_tmin_check_v2.json` (00:42) and `_v1_rerun.json` (00:40) pre-date the last edit of
  `srt_tmin_check.py` (00:47; `fixed_window` key absent).
  - The reviewer's independent code reproduces every number, so this is not a correctness issue.
  - Re-run nominal and v1 with the final script (≈ 1 min each) so that the outputs match the committed code.
- **C-3. P_{k≤−1} bound and population.**
  - **The bound.** The per-candidate bound 12 × 3/M is ×12 over-conservative. The estimator Σ_j (candidates with a copy
    hit in window j)/N is a single count, 0, and its 95 % bound is ≈ 3/N, by the same argument the FIX uses per hit.
  - **The population.** For the copy method the natural denominator is *all* candidates (the copied crossing is
    independent of in-time presence), which is what the script uses. The PC-19 text instead says M = the "conditioning
    sub-population".
  - **Whether it enters B.** State explicitly that P_{k≤−1} enters B at its measured value (an additive piece, not a §4.2
    zero factor) and that the bound is reported.
  - **Mixing variant.** Optionally state the mixing variant as primary, for parity with P_oot. It also gives 0 at G3.
- **C-4. Unstated choices in the edge text.** The rule text should state:
  - the 5 ps grid;
  - that "per hit" means per (candidate, hit) pair (594 708 pairs, not distinct hits).
  The reviewer's unbinned implementation gives identical edges at all four σ_PV settings, so this is immaterial.
- **C-5. The σ_t 60 ps variation.** PC-19 fixes both edges at the nominal σ_t, so this variation is also at the fixed
  window. Say whether it enters σ_ln like σ_t,PV (G3: ×1.00 loose, ×1.02 R04, immaterial) or is only reported.
- **C-6. Signal-side (ii) wording and pinning.**
  - "A candidate whose earliest in-window hit is an OOT PU hit" should read "whose earliest in-band hit (Δt > −Δt_bx/2) is
    an OOT PU hit".
  - In-time PU-late hits on signal candidates are still credited. This is immaterial (≲ 10⁻⁴ absolute), but say so.
  - The assignment of B1 overlay events to signal events (seed) is not pinned.
  - Add a fallback if an event lacks a road-0 trial, e.g. the lowest road present. All G3 events have one.

## 5. Items verified without finding

- PU vertex times are drawn with σ_t = 190 ps (`s4pu` l.135-138), matching plan l.288 (CMS-TDR-020).
- The salt is 0x5254 = 21076.
- The FIX §4 window occupancy is R₀ + R₊₁ + R_{k≤−1} = 9.58e-5 + 9.31e-5 + 0 = 1.89e-4 (FIX: 1.9e-4).
- Copy-method edges are 6.07 / 24.05 (JSON).
- The st60 run's `max_abs_ddt0` of 0.50 ns is expected: the stored t is unsmeared.
- **Scope.**
  - `WP_RULE.md` (Oct 13 18:18) and `finder/` are unchanged since before G3.
  - `frozen_inputs.json` (00:18) and `run_stage4.py` (00:31) pre-date the first FIX R2 output (00:40), so they were not
    changed by this fix. They were not attributed further.
  - The G3B1 files are unchanged (last written Oct 13 20:53).
  - The fix's outputs are only in `g3/`. C1 production is unaffected.
