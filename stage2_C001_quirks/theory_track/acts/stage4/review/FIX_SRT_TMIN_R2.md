# FIX_SRT_TMIN_R2: response to REVIEW_SRT_TMIN_R1 (ITERATE: 1 A, 3 B, 6 C)

**Scope.**
- This is PU-only. No signal efficiency, signal sample or signal yield was computed or opened.
- Nothing frozen was edited: WP_RULE, frozen_inputs, run_stage4, `code/`, `finder/` and `data/acts_stage4/prod/` are
  untouched. G3B1 was read read-only.
- Compute: 6 runs of 43-72 s each, 1 core, nice 15.

**Code.** `acts/stage4/g3/srt_tmin_check.py` now takes `--version {v1,v2}`.
- **v1** is the R1 logic. Its re-run (`srt_tmin_check_v1_rerun.json`) reproduces `srt_tmin_check.json` exactly: 6.12 /
  24.275 ns, 34/31 loose, 48/10 R04.
- **v2** adds the following:
  - the PV time (A-1);
  - three mixing partners (C-4);
  - the k ≤ −1 line (B-1);
  - raw-t vs min-Δt ordering (B-3 iii);
  - the even/odd split (C-2);
  - event counts (C-3);
  - `--sigma-pv-ps`, `--extra-smear-ps` and `--fixed-window` options (A-1 sensitivity, C-6).

**Outputs** (all in `data/acts_stage4/g3/`).
- `srt_tmin_check_v2.json` is nominal.
- `srt_tmin_check_v2_spv150.json`, `_v2_spv230.json` and `_v2_st60.json` are the variations.
- `srt_dt_hist_k0_*.npy` and `srt_dt_hist_kp1_*.npy` are the per-hit spectra.
- The R1 JSON is kept unchanged.

## 0. Finding → status

| finding | status | where |
|---|---|---|
| A-1 PV time | **RESOLVED.** Defined in the rule, edges and fractions re-derived, sensitivity run, the decision table redone | §1, §5 |
| B-1 k ≤ −1 | **RESOLVED.** Kept in B; a separate line, 0 at G3, with bounds | §2, §5 |
| B-2 P_oot conditioning | **RESOLVED.** The text conditions on ¬present | §5 |
| B-3 signal-side conventions | **RESOLVED.** Pre-declared, one choice each, with design status | §3, §5 |
| C-1 per-edge budget | **RESOLVED.** Stated explicitly as a user design choice | §4 |
| C-2 same-sample edge bias | **RESOLVED.** Even/odd split, +7 % / −1 % | §1 |
| C-3 clustering | **RESOLVED.** Event counts in every table | §1 |
| C-4 ×3 mixing | **RESOLVED.** Partners e+1, e+2, e+3 | §1 |
| C-5 model limits | **RESOLVED.** Caveat text included in PC-19 | §5 |
| C-6 σ_t 60 ps | **RESOLVED.** Run (+48.7 ps smearing) | §1 |

## 1. A-1: the PU-only PV time

**Definition (v2; the PC-19 text in §5).**
- Each PU-only event gets a PV time t_PV = σ_t,PV · z, with z ~ N(0, 1) from
  `numpy.random.default_rng([trials.trial_seed of the event's road-0 trial, 0x5254])`.
- σ_t,PV = **190 ps**: the luminous-region σ_t from the plan (l.288), `cms_phase2_public.json`, and the value with which
  `s4pu` draws the PU vertex times (VERIFIED).
- The 4 roads of an event share one stored PV (x, y, z), so they share t_PV.
- Δt = t_BTL − t_PV − |u|/c for every hit and every crossing.
- No PV-resolution term is added. The reviewer measured ≤ 15 ps of t_max for 40 ps. If one is added later, it applies
  identically to B and signal.

**Check of the stored-field route.**
- The stored `btl_dt0` minus t_PV equals the in-time Δt recomputed from S5 to 7.9 × 10⁻⁷ ns over 3.77 × 10⁶ candidates
  (3 float32 band-edge n_band mismatches). Raw-t order does not depend on t_PV.
- So P(late | present) needs only stored fields. P_oot and the edges need S5 + PV + normal/axis, which are all stored.
  **No production change is needed.**

**Results** (G3B1, 77 jobs, T_seed = 6; illustrative only, since the binding edges come from C1 B1). All values are
VERIFIED from the JSONs. The format is: candidate counts (distinct events); P_oot is the mean over 3 mixing partners.

| | v1 (t_PV = 0; R1) | **v2 nominal (σ_PV = 190 ps)** | v2, R1 window [6.12, 24.275] kept | v2, upper edge kept at Δt_acc = 25 ns |
|---|---|---|---|---|
| t_min / t_max (ns) | 6.12 / 24.275 | **6.07 / 24.025** (copy method 6.07 / 24.05) | — | 6.07 / 25 |
| per-hit R₀ / R₊₁ / R_{k≤−1} in the window | 9.4e-5 / 7.7e-5 / 0 | **9.6e-5 / 9.3e-5 / 0 (< 5.0e-6, 95 %)** | — | — |
| loose: in-time late, P(late \| present) | 34 (17 ev), 7.0e-5 | **36 (18 ev), 7.4e-5** | 35 (17), 7.2e-5 | 36 (18), 7.4e-5 |
| loose: OOT late per partner, P_oot(late \| ¬present) | 31 (12 ev), 2.1e-5 | **39 / 20 / 24 (12 / 7 / 9 ev), 1.9e-5** | 531 / 424 / 408, 3.1e-4 | ≈ 6.1e4 per partner, 4.2e-2 |
| loose: k ≤ −1 late | not reported | **0** (< 1.8e-5 per candidate, 95 %, 12 crossings) | — | — |
| **loose: SR-T PU fraction** | 3.31e-5 | **3.24e-5** | 2.49e-4 (**×7.7**) | 3.13e-2 |
| R04: in-time late, P(late \| present) | 48 (11 ev), 1.5e-4 | **48 (12 ev), 1.5e-4** | 47 (11), 1.5e-4 | 48 (12), 1.5e-4 |
| R04: OOT late, P_oot | 10 (4 ev), 6.6e-6 | **16 / 8 / 19 (7 / 4 / 5 ev), 9.5e-6** | 258 / 192 / 206, 1.5e-4 | 2.4e-2 |
| R04: k ≤ −1 late | — | **0** (< 2.0e-5, 95 %) | — | — |
| **R04: SR-T PU fraction** | 3.18e-5 | **3.42e-5** | 1.46e-4 (**×4.3**) | 2.01e-2 |

The reviewer's A-1 finding is reproduced: the R1 window under-states B by ×7.7 (loose) and ×4.3 (R04). With the edges
re-derived, the SR-T PU fraction returns to about 3 × 10⁻⁵. The reviewer's 24.08 ns came from a different t_PV draw
(per trial, seed 12345). The 10⁻⁴ edge rests on about 55 hits, so draw-to-draw scatter of about 0.05 ns is expected.

**Sensitivity** (VERIFIED; same seeds).

| variation | edges (ns) | SR-T fraction, own edges (loose / R04) | SR-T fraction at the fixed nominal window [6.07, 24.025] |
|---|---|---|---|
| σ_PV 150 ps | 6.08 / 24.10 | 2.95e-5 / 3.02e-5 | 2.24e-5 / 2.65e-5 |
| σ_PV 230 ps | 6.115 / 23.925 | 3.16e-5 / 3.45e-5 | **5.84e-5 / 4.64e-5 (×1.8 / ×1.36)** |
| σ_t 60 ps (C-6: +48.7 ps on the stored t) | 6.06 / 24.025 | 3.29e-5 / 3.47e-5 | 3.24e-5 / 3.47e-5 |

- t_min is stable (6.06-6.115 ns) because it is set by slow and looping particles.
- t_max moves with σ_PV, 0.09 ns per 40 ps. A mis-set σ_PV changes B at a fixed window by up to ×1.8.
- **Proposed:** the σ_PV ± 40 ps variation (150 / 230 ps, at the fixed nominal window) enters σ_ln of B_SR-T. This is
  in the PC-19 block.
- The σ_t 60 ps variation is immaterial, as the reviewer found.

**C-2 (same-sample edges).** Edges were derived on one job parity and measured on the other.
- Edges from even jobs are [6.205, 24.025]; edges from odd jobs are [5.95, 24.025]. (Labels corrected in R3; review R2
  C-1.)
- Loose: 2.61e-5 (measured on odd) and 4.32e-5 (measured on even), mean 3.47e-5, against 3.24e-5 same-sample (**+7 %**).
- R04: 4.18e-5 and 2.59e-5, mean 3.39e-5, against 3.42e-5 (**−1 %**).
- The bias is small compared with the event-clustered statistical error. The halves differ by ×1.7, consistent with
  about 10-20 contributing events.

**C-3 (clustering).** SR-T B rests on about **10-20 independent events** per term: loose in-time 18, OOT 7-12 per
partner; R04 12 and 4-7.
- The §4.2 event bootstrap σ_ln handles this.
- The "≥ 10 counts" M-rule counts candidates. The PC-19 text requires ≥ 10 counts **and** reports the event count.

## 2. B-1: k ≤ −1 delayed hits

- They are kept in B, as the frozen overlay intends.
- A previous-crossing hit enters the window only with a delay of 25j + Δt ≥ 31.07 ns. In Fatras PU none exists: the
  in-time Δt range is −1.34 … +6.64 ns at v2, and 0 candidates have any in-time in-band hit with Δt ≥ t_min + 25.
- **Per hit.** The 12 shifted windows are disjoint pieces of one spectrum, so Σ_j R₀([t_min + 25j, t_max + 25j]) ≤
  R₀(Δt ≥ t_min + 25) = 0 < 3/594 708 = **5.0 × 10⁻⁶** (95 %).
  - The reviewer's 12 × 3/N per hit over-counts, because the windows are disjoint.
  - **Per candidate**, 12 × 3/N = 1.8 × 10⁻⁵ (loose) and 2.0 × 10⁻⁵ (R04) is the right 95 % bound, because the 12
    crossings are independent events.
- The rule reports this as a separate B line even when it is 0. It rests on the simulated slow-particle tail only (C-5).

## 3. B-3: signal-side conventions, pre-declared before any signal is seen

Criterion: for the search, take the conservative choice (lower ε or higher B) unless it is unphysical.

| item | recommended choice | one-line reason | status |
|---|---|---|---|
| (i) signal t_PV | **the true signal vertex time `vtx[3]`** of the event, and `hs_vtx[3]` for SM kinds, with the same PV-resolution term as B (none at baseline) | The signal hits are generated with that vertex time as their origin (`code/s4sig.py` l.133-135), and the PU-only t_PV is drawn from the same luminous-region distribution, so B and ε use one convention. t_PV = 0 would add an unphysical 190 ps smear that only the signal side carries. | **not a design choice** (consistency, defect level) |
| (ii) OOT PU hits on signal candidates | **veto yes, credit no.** Signal candidates get the same mixed OOT overlay (B1 S5 hits, k = +1…+3 at +25k ns, and k ≤ −1) for the earliest-hit ordering. A candidate whose earliest in-window hit is an OOT PU hit is **not** counted in ε_SR-T. | This is the lower-ε choice and it is physical: OOT hits exist in signal events, but tagging by PU lateness is not signal. Both effects are ≤ P_oot + the k ≤ −1 bound ≈ (2-4) × 10⁻⁵ absolute (ESTIMATE from the PU numbers above). | **pre-registration, not a genuine design choice** (immaterial size) |
| (iii) "earliest" ordering | **smallest raw t_BTL** (as the stored `btl_dt0` and the PC-17-validated kernel) | On PU it is identical to min-Δt ordering: 0 disagreements out of 487 729 (loose) and 320 142 (R04) present candidates at nominal, 3 at σ_t = 60 ps (VERIFIED). In-band hits lie within W_c = 75 mm of the candidate axis, so the orderings can differ only for hits a few ×0.1 ns apart (ESTIMATE). The stored field then needs no re-definition. | **not a design choice** (immaterial on B; pinned for reproducibility) |

## 4. Decisions, with the corrected numbers (replaces FIX R1 §4)

**Defect fixes.**
- t_min is defined on the in-time tail.
- "Earliest" ignores previous-crossing hits that arrive promptly; delayed ones stay in B (B-1).
- Rates are normalised per hit of the same crossing.
- P_oot uses explicit mixing and is conditional on ¬present (B-2).
- The PU-only t_PV is defined (A-1).
- The signal-side conventions (i) and (iii) are pinned.

**Genuine design decisions for the user.**
1. **The upper edge (recommended: t_max from the k = +1 leading edge).**

   | option | edges at G3 (v2) | SR-T PU fraction, loose / R04 |
   |---|---|---|
   | **t_max (recommended)** | 6.07 / 24.03 ns | **3.2e-5 / 3.4e-5** |
   | upper edge kept at Δt_acc = 25 ns, PC-18 carries the k = +1 hits | 6.07 / 25 ns | 3.1e-2 / 2.0e-2 |

   The 25 ns option costs about **×10³** in B, leaving SR-T with only about 1.5-1.7 decades of time rejection.
2. **The threshold budget (C-1).** The recommended rule uses 10⁻⁴ per edge, so the per-hit window occupancy is
   R₀ + R₊₁ + R_{k≤−1} = 1.9 × 10⁻⁴. That is above the frozen single 10⁻⁴.
   - The alternative splits one 10⁻⁴ budget across the edges (0.5 × 10⁻⁴ each). That would move t_min to about 6.3-6.4
     ns and t_max to about 23.95-24.0 ns (ESTIMATE from the tail probes, not run).
   - Either way B is measured in the chosen window, so this is a choice of window, not a bias.
3. **σ_t,PV.** The plan value is 190 ps. The ±40 ps variation enters σ_ln (proposed). This is a choice only if the
   user wants a different central value.

The signal-side item (ii) is pre-registered as the conservative choice and needs no decision unless the user objects.

## 5. Combined amended-rule block (would become PC-19; NOT applied)

```diff
 WP_RULE §1.4 (SR-T / SR-G), replacing l.184 and l.188-189 and amending l.206-210:
-  - SR-T: ≥ 1 in-band BTL hit with Δt ∈ [t_min, Δt_acc]. Δt = t_BTL − t_PV − |u|/c of the **earliest** in-band BTL hit.
+  - SR-T: the **earliest** in-band BTL hit has Δt ∈ [t_min, t_max], where Δt = t_BTL − t_PV − |u|/c and "earliest" = the
+    smallest raw t_BTL among the in-band hits with Δt > −Δt_bx/2 (Δt_bx = 25 ns). Previous-crossing hits that arrive
+    promptly are not used; they could only veto, so this is conservative for B. Delayed previous-crossing hits
+    (k ≤ −1, Δt > −Δt_bx/2) are used and stay in B.
+  - **PV time.** PU-only trials: t_PV = σ_t,PV · z per event, z ~ N(0,1) from
+    numpy default_rng([trial_seed of the event's road-0 trial, 0x5254]), σ_t,PV = 190 ps (plan §1.3; the luminous
+    region). Signal and SM samples: t_PV = the true vertex time (signal `vtx[3]`, SM `hs_vtx[3]`). Any PV-resolution
+    term is applied identically to all samples (none at baseline).
   - σ_t = 35 ps (60 ps variation); Δt_acc = 25 ns (12.5 ns variation).
   - **Out-of-time overlay:** BTL hits of independent PU-200 events shifted by k × 25 ns, k ∈ {−12, …, +3} (the TDR
     readout window: 12 previous and 3 following crossings), each with its per-crossing BTL time spread.
-  - **t_min** = the smallest delay at which the per-hit late rate (in-band BTL hits of B1 loose candidates, in-time
-    spectrum ⊕ overlay) falls below 10⁻⁴; fixed from PU-only B1 + overlay only (§2.5 item 7), before any signal ε.
+  - **Window edges.** R_k(a, b) = N_k(Δt ∈ [a, b]) / N_k, the per-hit rate of the in-band BTL hits of the B1 loose
+    candidates (S3 ∧ R01) from crossing k, normalised per hit of that crossing. k = +1 is built by explicit mixing: the
+    candidates of event e get the S5 BTL hits of event e + 1 (mod n_ev) of the same job at t + 25 ns, about the
+    candidate's own plane, axis, PV and t_PV.
+    - t_max = min(Δt_acc, the largest t ≤ Δt_bx with R₊₁(Δt_bx/2, t) < 10⁻⁴): the leading edge of the next crossing.
+    - t_min = the smallest t ≥ 0 with R₀(t, t_max) < 10⁻⁴: the in-time late tail.
+    - [user design choice: 10⁻⁴ per edge (recommended), or 0.5 × 10⁻⁴ per edge]
+    - Both edges are fixed from PU-only C1 B1 + overlay only (§2.5 item 7), before any signal ε, at the nominal σ_t and
+      σ_t,PV.
+    - Reported: R₀, R₊₁ and R_{k≤−1} = Σ_{j=1..12} R₀(t_min + 25j, t_max + 25j) (copy method) in the window, each
+      with its 95 % bound when it is 0.
-    - Per stored candidate (any ρ): `btl_n_band`, `btl_n_int`, `btl_dt0` (Δt of the in-band hit with the smallest raw
-      time, with t_PV = 0: the PU-only trial PV carries no time; offline P(late) applies the trial t_PV convention).
+    - Per stored candidate (any ρ): `btl_n_band`, `btl_n_int`, `btl_dt0` (Δt of the in-band hit with the smallest raw
+      time, stored with t_PV = 0; offline, Δt = btl_dt0 − t_PV with t_PV as defined above).
-    - **Not in-job, by construction:** the time window [t_min, Δt_acc] and the out-of-time overlay. …
+    - **Not in-job, by construction:** the time window [t_min, t_max], the PV time and the out-of-time overlay. …

 WP_RULE §6.2 composition, SR-T (PC-18 completed):
-  - SR-T: P̂₁(r ∧ BTL-present) × P(late) + P̂₁(r ∧ ¬BTL-present) × P_oot(late) (PC-18). … lands in [t_min, Δt_acc]. …
+  - SR-T: P̂₁(r ∧ BTL-present) × P(late) + P̂₁(r ∧ ¬BTL-present) × [P_oot(late) + P_{k≤−1}(late)] (PC-18, PC-19).
+    - P(late) = the fraction of the BTL-present candidates of the measuring population whose earliest in-time in-band
+      hit has Δt ∈ [t_min, t_max].
+    - P_oot(late) = the fraction of the candidates of the measuring population **without an in-time in-band BTL hit**
+      whose earliest mixed k = +1 in-band hit has Δt ∈ [t_min, t_max]. It is the mean over the mixing partners
+      e + 1, e + 2, e + 3 (independent events).
+    - P_{k≤−1}(late) = the same for delayed previous-crossing hits (copy method). It is reported as a separate line even
+      when 0, with the bound 12 × 3/M.
+    - M_j and the §4.2 ≥ 10-count rule refer to the conditioning sub-population. The number of distinct events behind
+      each count is reported (the B estimate rests on few events; §4.2 event bootstrap).
+    - Systematic: σ_t,PV = 150 / 230 ps at the fixed nominal window enters σ_ln of B_SR-T (G3: ×0.7 to ×1.8).
+  - Signal ε_SR-T (pre-registered, PC-19): the same Δt, t_PV and "earliest" definitions. The same mixed OOT overlay
+    (k = +1…+3 and k ≤ −1, B1 S5 hits) enters the earliest-hit ordering (it can veto). A candidate whose earliest
+    in-window hit is an OOT PU hit is **not** counted in ε_SR-T (no credit for PU lateness).
+  - Model limits (AN caveat): Fatras-only PU; no SiPM dark counts or noise, no neutron or cavern background; the
+    slow-particle tail is as simulated. A flat random in-band hit rate would fill [t_min, t_max] and is not in B.

 Appendix A `sr_t` row and frozen_inputs.json `sr_t`: + "t_max": "from B1 + k=+1 mixing by the frozen rule",
   "dt_bx_ns": 25.0, "sigma_t_pv_ps": 190.0, "sigma_t_pv_variation_ps": [150, 230], "tpv_seed_salt": 21076,
   "late_rate_threshold_per_edge": 1e-4 (or the user's split).
 PC table: + | PC-19 | SR-T window [t_min, t_max] (t_max = k=+1 leading edge), PU-only t_PV ~ N(0, 190 ps) seeded from
   trial_seed, earliest = raw t over Δt > −Δt_bx/2, k ≤ −1 kept, P_oot conditional on ¬present (3 mixing partners),
   σ_t,PV variation in σ_ln, signal-side conventions pre-registered | §1.4, §6.2 | FIX_SRT_TMIN_R1/R2, REVIEW_SRT_TMIN_R1 |
```

Applying this needs a logged WP_RULE / frozen_inputs change with a re-hash, and a re-review, before any SR-T signal ε.
C1 production is unaffected: every input is already stored.
