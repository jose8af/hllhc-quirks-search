# REVIEW_SRT_TMIN_R1: critical review of the proposed SR-T window fix (FIX_SRT_TMIN_R1)

Fresh critical reviewer, 2026-10-14. Target: `acts/stage4/review/FIX_SRT_TMIN_R1.md` (proposed amendment of WP_RULE
§1.4 l.184-189, PC-18 l.468-472 / l.818), `acts/stage4/g3/srt_tmin_check.py`, `data/acts_stage4/g3/srt_tmin_check.json`.
Read: reviewer spec + `methodology/03-review.md`; WP_RULE §1.4, §4.2, §6.2, PC table, App. A; `G3_REPORT.md` §2, §7.6,
§8.3; `analyse_g3.py` (`_srt_kernel`, `srt_hits`, `tmin_from_hist`, `srt_test`); plan §1.3 (beam spot), §1.5 (BTL
σ_t), §2.3 (SR-T); `FIX_WP_RULE_R2.md` (PC-18 origin); `run_stage4.py` l.340-515; `production.py` l.415-451;
`code/s4pu.py` (MinBias vertex times), `finder/pu_inputs.lum_pv`; `jobs/C1.json`; `frozen_inputs.json`.

**Signal-blindness.** No signal efficiency, signal sample or signal yield was computed or opened. Checks use only the
G3B1 PU-only files (read-only) and the two stored per-hit histograms. Compute ≈ 2 × 47 s, 1 core, nice 15. Reviewer
scratch scripts lived in the session scratchpad (not in the project); their logic is given in A-1 so it can be redone.

## Verdict

**ITERATE: 1 A, 3 B, 6 C.**

The diagnosis is right and the check script implements the proposed text faithfully. The amendment is not safe as
written: the upper edge t_max sits exactly where the PU-only **PV-time convention** (t_PV = 0) matters. With a realistic
PV time, the recommended window under-states the SR-T PU background by ×4-8 (A-1). The remedy is cheap, offline, and
needs no production change.

---

## 1. Answers to the five questions

**(1) Diagnosis: CORRECT (VERIFIED).**
- In-time per-hit Δt spans −0.9325 … +6.5125 ns (594 708 loose (cand, hit) pairs; reviewer re-read of
  `srt_dt_hist.npy`). k = +1 hits therefore start at 24.07 ns. R₊₁(12.5, 25) = 0.139 (JSON).
- The frozen R(t) on [t, 25 ns] includes ≈ 14 % of the k = +1 hits for every t < 24.07 ns, so no t_min < Δt_acc can reach
  10⁻⁴. `tmin_from_hist` implements the frozen text, with a ×16 denominator. G3's 8.8 × 10⁻³ ≈ 0.139/16 is consistent.
- The "earliest hit" veto by previous crossings under a literal reading is real. 1 − (1 − f)¹² = 0.96 / 0.87 is an
  ESTIMATE that assumes the k = −j presence equals the mixed k = +1 presence (0.239 / 0.159). That is reasonable.

**(2) Signal independence and conservativeness: PARTLY.**
- *Signal independence: YES.* Both edges are quantiles of PU-only spectra at the frozen 10⁻⁴. Δt_bx/2 = 12.5 ns is a
  constant.
- *Dropping hits with Δt < −12.5 ns from "earliest".* For a fixed set of overlay hits, removing hits from the arg-min
  can only turn a not-late candidate into a late one, never the reverse. So B(amended) ≥ B(literal): conservative
  relative to the frozen reading. Relative to the "truth" under the amended rule, the residual is k ≤ −1 hits that land
  in the window, which the text wrongly says are excluded (B-1). They are 0 in the G3 Fatras spectrum.
- *OOT carried through PC-18: YES* in the script, as P(k=+1 late | ¬present) (but see B-2 on the text).
  - The decomposition is exact: the in-time raw t ≤ 6.51 + ~9 ns is always before any k = +1 raw t ≥ 24.07 + 3.8 ns.
  - The reviewer's independent re-implementation (t_PV = 0) reproduces every count exactly: 34 / 31 loose, 48 / 10 R04.
- *Mixing within a 25-event job: VALID.*
  - Events are independent seeded PU-200 draws (`s4pu.MinBias.event`, hseed per event).
  - Hits are taken about the candidate's own plane, axis and PV. The (e + 1) mod n_ev wrap and the reuse of event e + 1's
    hits as in-time for its own candidates add correlation, not bias.
  - Candidates of the 4 roads of an event share one overlay, so the counts are event-clustered (C-3).
- *Precision of the 10⁻⁴ edge: ADEQUATE* (t_max from ≈ 44 pair counts).
  - R₊₁ rises from 2.5 × 10⁻⁵ at 24.2 ns to 1.4 × 10⁻⁴ at 24.3 ns, so even with a clustering deff of ≈ 5-10 the edge moves
    ≲ 0.05 ns.
  - B does not inherit the edge's error, because it is measured with the edge.
- *Sensitivity to the PV-time convention: NOT ADDRESSED.* This is A-1.

**(3) t_max vs BTL resolution, and the normalisation.**
- The plan assumes σ_t = 35 ps per hit (30-40 ps at start, 50-60 ps at end of life; 60 ps variation, plan l.333).
- 25 − 24.275 = 0.725 ns ≈ 20 σ_t, so the edge is not set by BTL resolution. It is set by:
  - the trial-PV vs PU-vertex z offset and the path excess (in-time core: mean +0.47 ns, rms 0.48 ns);
  - the PU vertex time spread (190 ps).
- Reviewer convolution of both spectra with an extra 40 ps Gaussian moves t_max to 24.260 ns and leaves t_min at
  6.12 ns. The 60 ps variation is therefore harmless (C-6).
- What does matter is the reference time t_PV (A-1).
- Normalising per hit of the same crossing is reasonable: N₊₁/N₀ = 569 068 / 594 708 = 0.96, so a per-in-time-hit
  normalisation differs by 4 %.
- The per-edge 10⁻⁴ budget gives a window occupancy of 1.7 × 10⁻⁴, above the frozen single 10⁻⁴. That is a design
  choice (C-1).

**(4) The script implements the proposed text: YES.**
- R_k, t_max and t_min are implemented as written.
- The loose-only per-hit histograms are re-histogrammed when a trial mixes loose and R04 candidates.
- The in-time histogram equals G3's (`hist_in_time_equals_g3: true`).
- The Δt > −12.5 ns filter is implicit: no k ≤ −1 is mixed, and no k ∈ {0, +1} hit is < −0.93 ns.
- P_oot is computed conditional on ¬present. The proposed text says otherwise (B-2).

**(5) Production storage: VERIFIED.**
- `run_stage4.py`:
  - l.383-384 append all BTL hits of every event, with columns ev (job-relative ie), sid, x, y, z, s0, s1, dE, t, INT;
  - l.509-511 store them as float32 `btl` (+ `btl_cols`);
  - l.468-469 store `trials.pv`, and l.419/465 store `trials.trial_seed`.
- `production.py` l.419-447 stores tag, normal, axis and rungs, and `btl_n_band`, `btl_n_int`, `btl_dt0` (smallest
  **raw** t).
- C1 B1 = 200 jobs × 25 events × 4 roads, ρ = 1 (`jobs/C1.json`), so within-job mixing works (5000 events, ×2.6 G3).
- For the A-1 remedy, `trials.trial_seed` gives a reproducible per-trial t_PV draw. For SM kinds, the HS vertex 4-vector
  is persisted in `meta_json → chain_meta.ev_info[ie].hs_vtx` (s4pu l.291, run_stage4 l.447/454).
- **No production change is needed** (fixer claim confirmed).

**(6) Post-hoc dependence of SR-T signal ε.**
- The edges are fixed by procedure from C1's own B1. G3 values are illustrative only: T_seed = 6 at G3 vs the frozen
  `t_seed = 4`.
- Three items are still open and must be pinned before any signal ε (B-3):
  - the signal-side t_PV;
  - whether k = +1 PU hits apply to signal candidates;
  - "earliest" by raw t vs by Δt.
- The fixer correctly requires the option choice (t_max vs 25 ns vs a split budget) before any SR-T ε.

---

## 2. Findings

### A-1. t_max is placed on an unphysically sharp k = +1 edge: the PU-only PV carries t_PV = 0, while the PU vertices carry σ_t = 190 ps. B_SR-T is under-stated ×4-8.

**Evidence.**
- `pu_inputs.lum_pv` draws (x, y, z) only, and WP_RULE l.207 says "the PU-only trial PV carries no time". The script
  uses Δt = t_BTL − 0 − |u|/c.
- The PU vertices are drawn with σ_t = `sigma_t_ps` = 190 ps (`acts/geometry/cms_phase2_public.json`, `s4pu.py`
  l.135-138; plan l.288).
- In the real experiment Δt is taken w.r.t. the hard-scatter PV time, which is independent of the PU vertex times. The
  PU-hit Δt then carries an extra N(0, 190 ps): √2 × 190 = 270 ps of vertex-time spread in total, not 190 ps.
- The 10⁻⁴ leading edge of k = +1 lies in the Gaussian-dominated low tail, so it is exactly where this matters. (The
  in-time t_min tail at 6 ns is from slow and looping particles and hardly moves.)

**Reviewer check.** `srt_tmin_check.py` loop re-implemented with TB → TB − t_PV,trial, t_PV,trial ~ N(0, 0.19 ns) per
trial (rng seed 12345). Everything else is identical, and the σ = 0 run reproduces the fixer's JSON exactly.

| | t_PV = 0 (fixer) | t_PV ~ N(0, 190 ps), window [6.12, 24.275] (as proposed) | t_PV ~ N(0, 190 ps), edges re-derived |
|---|---|---|---|
| t_min / t_max | 6.12 / 24.275 | same | **6.115 / 24.080** |
| loose: n_late_in / n_late_oot (events) | 34 (17) / 31 (12) | 35 (17) / **487 (166)** | 38 (19) / 37 (14) |
| loose P_oot(late \| ¬present) | 2.1 × 10⁻⁵ | **3.3 × 10⁻⁴ (×16)** | 2.5 × 10⁻⁵ |
| loose SR-T PU fraction | 3.31 × 10⁻⁵ | **2.66 × 10⁻⁴ (×8.0)** | 3.82 × 10⁻⁵ |
| R04: n_late_in / n_late_oot (events) | 48 (11) / 10 (4) | 32 (11) / 199 (87) | 34 (12) / 19 (7) |
| R04 SR-T PU fraction | 3.18 × 10⁻⁵ | **1.27 × 10⁻⁴ (×4.0)** | 2.91 × 10⁻⁵ |

The per-hit histogram convolution gives the same picture: R₊₁(12.5, 24.275) = 1.23 × 10⁻³ vs 7.7 × 10⁻⁵ at t_PV = 0.

**Why A.**
- The recommended option is presented as "conservative for B". With the PV time as it is in data, the PU background in
  the recommended window is under-stated by ×8 (loose) / ×4 (R04).
- The frozen 25 ns edge was insensitive to this (P_oot ≈ 2-3 × 10⁻² either way). The new edge makes it first-order.
- The frozen text's "offline P(late) applies the trial t_PV convention" (l.207) is undefined, so the gap is in the
  rule, not only in the script.

**Required fix (offline, no production change).**
1. Define t_PV for PU-only trials as a seeded draw t_PV ~ N(0, σ_t,lum = 190 ps) from `trials.trial_seed`, optionally
   ⊕ a PV time resolution. 40 ps is immaterial: t_max moves by 15 ps.
2. Use that t_PV for the edge derivation, for P(late | present) and for P_oot. Re-derive both edges from C1 B1. On G3:
   t_max ≈ 24.08 ns, t_min ≈ 6.12 ns.
3. Replace "the trial t_PV convention" (l.207) by this text.
4. State the same reference for every sample kind: SM/signal = the true HS vertex time `hs_vtx[3]`, with the same
   resolution if one is used.
5. Optional: report the σ_t,lum = 150 / 230 ps sensitivity of t_max.
6. The decision table in FIX §4 should be redone with the corrected numbers.

### B-1. "k ≤ −1 is excluded by the Δt cut above" is false.

- The cut Δt > −12.5 ns removes only previous-crossing hits that arrive promptly.
- A k = −j hit with a delay of 25j + Δt (≥ 31 ns for j = 1) lands in [t_min, t_max]. It belongs to the frozen overlay
  (k ∈ {−12…+3}) and to B.
- The amendment drops it silently, and P_oot mixes only k = +1.
- Numerically this is 0 in Fatras PU: the in-time spectrum ends at 6.51 ns, so R₀(31.1, 49.3) = 0/594 708. But a
  naïve 95 % bound is 12 × 3/594 708 ≈ 6 × 10⁻⁵ per hit, not negligible against 10⁻⁴.
- **Fix:** keep k ≤ −1 in the text. Their in-window contribution is R₀ shifted by 25|k| (the copy method suffices,
  since previous crossings are independent). Report the measured value (0 at G3) and note that it rests on the
  simulated delay tail (C-5).

### B-2. PC-18 completion text and the script disagree on P_oot.

- The proposed text reads: "P_oot(late) = fraction of the candidates in the measuring population … whose earliest k = +1
  mixed in-band hit has Δt ∈ [t_min, t_max]". That is unconditional.
- The factor multiplies P̂₁(r ∧ ¬present), and the script computes P(k = +1 late | ¬present) (`late_oot.sum() /
  (~pres).sum()`). That is the correct quantity.
- **Fix:** write "among the candidates of the measuring population **without an in-time in-band BTL hit**". M_j and the
  §4.2 ≥ 10 rule then refer to that sub-population.

### B-3. Signal-side and "earliest" conventions are not pinned. They must be pre-registered before any SR-T ε.

The amendment defines the window only for B. Three choices would otherwise be made with signal in hand:
- (i) the signal t_PV: the true HS time, a smeared HS time, or 0 (A-1);
- (ii) whether signal candidates also receive the k = +1 mixed PU hits (and k ≤ −1). This would let a signal candidate
  without a quirk or in-time hit be tagged by a PU k = +1 hit. The conservative choice is to credit no OOT-PU lateness to
  ε, or to apply the identical overlay to both B and ε;
- (iii) "earliest" = smallest raw t_BTL (as `btl_dt0` / `_srt_kernel` do) or smallest Δt. The two orderings can differ
  between a quirk hit and a PU hit at different |u|.

**Fix:** one sentence each in §1.4.

### C (optional)

- **C-1.** The per-edge 10⁻⁴ (window occupancy R₀ + R₊₁ = 1.7 × 10⁻⁴ > the frozen single 10⁻⁴) is a design choice, not a
  "defect fix". FIX §4 does list the split-budget option, but the decision record should state it explicitly.
- **C-2.** The edges and P_oot are measured on the same sample. Placing t_max where the sample fluctuates low biases
  P_oot down slightly. The steep edge makes this small. Optionally derive the edges on even jobs and measure on odd ones,
  or report the shift.
- **C-3.** The counts are strongly clustered. At t_PV = 0, the loose late_oot 31 come from 12 events and late_in 34 from
  17; for R04, 10 come from 4 events and 48 from 11. §4.2's event-bootstrap σ_ln handles this, but the "≥ 10 counts"
  M-rule counts candidates. Note in the B table that SR-T B rests on ~10-20 independent events.
- **C-4.** Mixing can use e + 1, e + 2, e + 3 (still independent events) for ×3 OOT statistics at no cost.
- **C-5.** The model limits should be stated in the AN. The B1 PU is Fatras-only: there are no SiPM dark-count or noise
  hits, no low-energy neutron or cavern background, and only simulated slow-particle tails. A flat random in-band hit
  rate would fill [t_min, t_max] uniformly and is not in B. This is a theory-track caveat, not a fix.
- **C-6.** The σ_t variation via offline smearing (√(60² − 35²) = 48.7 ps on the stored t) is fine: the edge moves
  ≲ 20 ps. The amended text says the edges are re-derived per variation; the check script does not do it yet. It should
  before use.

## 3. Items verified without finding

- G3 numbers: t_min 6.12 ns, 594 708 hits, kernel check (3 band-edge mismatches, |Δdt0| ≤ 8 × 10⁻⁷ ns).
- JSON vs FIX §3 table: all values match to the quoted digits.
- Literal-reading rejection (empty window) and rejection of the ×16 dilution: correct.
- Production unaffected: the window is offline, and `n_pass_T` / `S_ded_T` are independent of t_min/t_max.
- `frozen_inputs.json` t_seed = 4; the edges will come from the T_seed = 4 C1 B1, as the fix states.
