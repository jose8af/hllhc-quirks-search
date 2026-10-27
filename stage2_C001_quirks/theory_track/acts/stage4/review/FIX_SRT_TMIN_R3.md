# FIX_SRT_TMIN_R3: delta for REVIEW_SRT_TMIN_R2 (ITERATE narrow: 0 A, 1 B, 6 C)

**Scope.** This is PU-only, with no signal ε. Nothing frozen or in production was edited, and G3B1 was read read-only.
Compute: 5 runs, about 3.3 min each for v2 and 47 s for v1, plus a combine step; 1 core, nice 15.

**Script changes** (`acts/stage4/g3/srt_tmin_check.py`).
- k ≤ −1 is now measured by mixing (partners e+1…e+12 as crossings −1…−12).
- If an event has no road-0 trial, its t_PV is seeded from the lowest road present.
- New outputs: `late_count_C`, `L_composite` and `M_not_present`.
- A `--combine` mode applies the B-1 rule mechanically and writes `data/acts_stage4/g3/srt_sigma_ln_pv.json`.

## Finding → status

| finding | status | change |
|---|---|---|
| **B-1** σ_t,PV → σ_ln underspecified | **RESOLVED** | Formula, quantity, population with a ≥ 10 fallback, scope and the §4.1 slot are all in the PC-19 block. Evaluated mechanically on G3 (below). |
| C-1 parity labels | **RESOLVED** | FIX R2 §1 corrected in place: even = [6.205, 24.025], odd = [5.95, 24.025] (JSON keys `edges_even_jobs` / `edges_odd_jobs`). |
| C-2 provenance | **RESOLVED** | `srt_tmin_check_v1_rerun.json` (01:16), `_v2.json` (01:19), `_v2_spv150/230`, `_v2_st60` and `srt_sigma_ln_pv.json` were all regenerated with the final script. All R2 numbers are unchanged; v1 still reproduces R1 exactly (34/31, 48/10). |
| C-3 k ≤ −1 bound and M | **RESOLVED** | Mixing is primary. The count is a single count on M_¬pres, so the 95 % bound is 3/M_¬pres = **2.0 × 10⁻⁶** (loose and R04), replacing 12 × 3/N. P_oot and P_{k≤−1} share one M = M_¬pres and form one §4.2 factor. G3 gives 0 (mixing) and 0 (copy cross-check, bound 3/N = 1.5-1.6 × 10⁻⁶). |
| C-4 grid and "per hit" | **RESOLVED** | Stated: 5 ps grid; per (candidate, hit) pair. |
| C-5 σ_t 60 ps | **RESOLVED** | It enters σ_ln by the same rule as σ_t,PV (one variation). G3: 0.000 (loose), 0.016 (R04). |
| C-6 signal (ii) wording | **RESOLVED** | Wording changed to "earliest in-band hit (Δt > −Δt_bx/2)". In-time PU-late credit is stated as immaterial (≤ P(late \| present) ≈ 1.5 × 10⁻⁴ × f_pres). The OOT event assignment for signal is pinned by a hash, and the road-0 fallback is stated. |

## B-1 evaluated on G3 (illustrative; the binding values come from C1 B1)

Source: `srt_sigma_ln_pv.json`. All runs use the same z draws and the fixed nominal window [6.07, 24.025] ns.
- L is the SR-T late composite: f_pres·P(late) + f_¬pres·[P_oot + P_{k≤−1}].
- C is the late count: in-time late + Σ_{3 partners} OOT late + Σ_j k ≤ −1 late.

| population | C (nom / 150 / 230) | L nominal | L150 / L230 | σ_ln,PV | σ_ln,σt |
|---|---|---|---|---|---|
| loose S3 ∧ R01 | 119 / 54 / 266 | 3.24e-5 | 2.24e-5 / 5.84e-5 | 0.588 | 0.000 |
| R04 S2 (deepest qualifying here) | 91 / 51 / 158 | 3.42e-5 | 2.65e-5 / 4.64e-5 | **0.306** | 0.016 |

Under the rule, every rung deeper than R04 would take 0.306 at G3. C1 will be measured to deeper rungs, since its B1
sample is ×2.6 larger.

## Final PC-19 block (complete; NOT applied)

```diff
 WP_RULE §1.4 (SR-T / SR-G), replacing l.184 and l.188-189 and amending l.206-210:
-  - SR-T: ≥ 1 in-band BTL hit with Δt ∈ [t_min, Δt_acc]. Δt = t_BTL − t_PV − |u|/c of the **earliest** in-band BTL hit.
+  - SR-T: the **earliest** in-band BTL hit has Δt ∈ [t_min, t_max], where Δt = t_BTL − t_PV − |u|/c and "earliest" = the
+    smallest raw t_BTL among the in-band hits with Δt > −Δt_bx/2 (Δt_bx = 25 ns).
+    - Previous-crossing hits that arrive promptly are not used. They could only veto, so this is conservative for B.
+    - Delayed previous-crossing hits (k ≤ −1, Δt > −Δt_bx/2) are used and stay in B.
+  - **PV time.**
+    - PU-only events: t_PV = σ_t,PV · z per event, z = numpy default_rng([trial_seed, 0x5254]).standard_normal(). The
+      trial_seed is that of the event's road-0 trial, or of its lowest road present. σ_t,PV = 190 ps (plan §1.3; the
+      luminous region; the PU vertex times use the same value).
+    - Signal and SM samples: t_PV = the true vertex time (signal `vtx[3]`, SM `hs_vtx[3]`).
+    - Any PV-resolution term is applied identically to all samples (none at baseline).
   - σ_t = 35 ps (60 ps variation); Δt_acc = 25 ns (12.5 ns variation).
   - **Out-of-time overlay:** BTL hits of independent PU-200 events shifted by k × 25 ns, k ∈ {−12, …, +3} (the TDR
     readout window: 12 previous and 3 following crossings), each with its per-crossing BTL time spread.
-  - **t_min** = the smallest delay at which the per-hit late rate (in-band BTL hits of B1 loose candidates, in-time
-    spectrum ⊕ overlay) falls below 10⁻⁴; fixed from PU-only B1 + overlay only (§2.5 item 7), before any signal ε.
+  - **Mixing.** Crossing k ≠ 0 of a B1 candidate in event e of a job with n_ev events uses the S5 BTL hits of event
+    e + j (mod n_ev) of the same job, about the candidate's own plane, axis, PV and t_PV:
+    - k = +1: j = 1, 2, 3 (three independent realisations), at t + 25 ns;
+    - k = −j: j = 1…12, at t − 25 j.
+  - **Window edges.**
+    - R_k(a, b) = N_k(Δt ∈ [a, b]) / N_k, counted per (candidate, in-band hit) pair over the B1 loose candidates
+      (S3 ∧ R01) and normalised per pair of the same crossing. The k = +1 spectrum uses realisation j = 1.
+    - On a 5 ps grid:
+      - t_max = min(Δt_acc, the largest t ≤ Δt_bx with R₊₁(Δt_bx/2, t) < 10⁻⁴): the leading edge of the next crossing.
+      - t_min = the smallest t ≥ 0 with R₀(t, t_max) < 10⁻⁴: the in-time late tail.
+    - [user design choice: 10⁻⁴ per edge (recommended), or 0.5 × 10⁻⁴ per edge]
+    - Both edges are fixed from PU-only C1 B1 + overlay only (§2.5 item 7), before any signal ε, at the nominal σ_t
+      (35 ps) and σ_t,PV (190 ps).
+    - Reported: R₀, R₊₁ and R_{k≤−1} = Σ_{j=1..12} R₀(t_min + 25j, t_max + 25j) in the window, each with its 95 % bound
+      when it is 0.
-    - Per stored candidate (any ρ): `btl_n_band`, `btl_n_int`, `btl_dt0` (Δt of the in-band hit with the smallest raw
-      time, with t_PV = 0: the PU-only trial PV carries no time; offline P(late) applies the trial t_PV convention).
+    - Per stored candidate (any ρ): `btl_n_band`, `btl_n_int`, `btl_dt0` (Δt of the in-band hit with the smallest raw
+      time, stored with t_PV = 0; offline, Δt = btl_dt0 − t_PV with t_PV as defined above).
-    - **Not in-job, by construction:** the time window [t_min, Δt_acc] and the out-of-time overlay. …
+    - **Not in-job, by construction:** the time window [t_min, t_max], the PV time and the out-of-time overlay. …

 WP_RULE §6.2 composition, SR-T (PC-18 completed):
-  - SR-T: P̂₁(r ∧ BTL-present) × P(late) + P̂₁(r ∧ ¬BTL-present) × P_oot(late) (PC-18). … lands in [t_min, Δt_acc]. …
+  - SR-T: P̂₁(r ∧ BTL-present) × P(late) + P̂₁(r ∧ ¬BTL-present) × P_OOT(late) (PC-18, PC-19).
+    - **P(late)** = the fraction of the BTL-present candidates of the measuring population whose earliest in-time
+      in-band hit has Δt ∈ [t_min, t_max].
+    - **P_OOT(late)** = [n̄₊₁ + n_{k≤−1}] / M_¬pres. It is **one §4.2 factor**, and M_¬pres = the candidates of the
+      measuring population **without an in-time in-band BTL hit**.
+      - n̄₊₁ = the mean over the three k = +1 realisations of the number of those candidates whose earliest mixed k = +1
+        in-band hit has Δt ∈ [t_min, t_max].
+      - n_{k≤−1} = Σ_{j=1..12} the number of those candidates with a mixed crossing −j in-band hit with Δt ∈ [t_min,
+        t_max]. The sum over j is conservative relative to the union. Its proxy is the partner's max Δt ≥ t_min + 25j.
+      - n_{k≤−1} enters at its measured value. It is also reported as a separate line, with the 95 % bound 3/M_¬pres
+        when it is 0.
+    - The number of distinct events behind each count is reported. The §4.2 event bootstrap gives σ_ln,stat.
+    - **Timing-model σ_ln terms (mechanical, fixed before C1 is seen).**
+      - *Quantity.* L(P) = f_pres · P(late) + f_¬pres · P_OOT(late), evaluated on population P with the window held at
+        the nominal edges.
+      - *Variation sets.* {σ_t,PV = 150, 230 ps} for σ_ln,PV and {σ_t = 60 ps} for σ_ln,σt. Each variation uses the
+        same z draws and seeds as the nominal; σ_t 60 ps = +48.7 ps Gaussian smearing of the stored t, seeded by
+        [job seed, 0x534D].
+      - *Formula.* σ_ln,X(P) = max over the set's variations v of |ln(L_v(P) / L_nom(P))|.
+      - *Population and fallback.*
+        - For the SR-T ladder rung r, the B1 ρ = 1 candidate records passing r: S3 ∧ r for r < R04, S2 ∧ r for
+          r ≥ R04.
+        - r qualifies if its late count C = (in-time late) + Σ over the 3 k = +1 realisations (OOT late) + n_{k≤−1}
+          is ≥ 10 in the nominal run **and** in every variation of the set.
+        - A rung that does not qualify takes the value of the deepest qualifying rung before it in ladder order.
+        - A factorised F1 rung (h, o, e) takes the value of its parent in-job rung (R14, or FB_k[∧ e]), and the same
+          fallback applies.
+        - If no rung qualifies, σ_ln,X = 1.0.
+      - *Scope.* These terms apply only to B_PU's SR-T term, to both summands above. They do not apply to B_SM (true
+        `hs_vtx[3]`, not varied), the C′₀ / C′_PU terms or SR-G.
+      - *§4.1 slot.* For B_PU,SR-T(r): σ_ln² = stat² + (extrapolation-model spread)² + (density normalisation)² +
+        (normalisation)² + σ_ln,PV(r)² + σ_ln,σt(r)². For every other term both are 0.
+  - **Signal ε_SR-T (pre-registered, PC-19).**
+    - It uses the same Δt, t_PV and "earliest" definitions.
+    - Out-of-time overlay for signal: crossing k ∈ {−12…−1, +1…+3} of signal row (spin, m, row) uses the C1 B1 event
+      with index blake2b("srt-oot|spin|m|row|k") mod N_B1. C1 B1 events are ordered by (job id, ev), and on a
+      collision the index is incremented to the next unused event.
+    - Those hits enter the earliest-hit ordering, so they can veto.
+    - A candidate whose **earliest in-band hit (Δt > −Δt_bx/2) is an OOT PU hit** is **not** counted in ε_SR-T (no
+      credit for OOT-PU lateness).
+    - In-time PU hits of the signal overlay are treated as in production. Their late credit is ≤ P(late | present) ≈
+      1.5 × 10⁻⁴ × f_pres, which is immaterial.
+  - **Model limits (AN caveat).** The PU is Fatras-only: there are no SiPM dark counts or noise and no neutron or cavern
+    background, and the slow-particle tail is as simulated. A flat random in-band hit rate would fill [t_min, t_max] and
+    is not in B.

 Appendix A `sr_t` row and frozen_inputs.json `sr_t`: + "t_max": "from B1 + k=+1 mixing by the frozen rule",
   "dt_bx_ns": 25.0, "edge_grid_ns": 0.005, "sigma_t_pv_ps": 190.0, "sigma_t_pv_variation_ps": [150, 230],
   "tpv_seed_salt": 21076, "smear_seed_salt": 21325, "oot_mixing": {"kp1_partners": [1, 2, 3], "km_partners": "1..12"},
   "late_rate_threshold_per_edge": 1e-4 (or the user's split).
 PC table: + | PC-19 | SR-T window [t_min, t_max] (t_max = the k=+1 leading edge); PU-only t_PV ~ N(0, 190 ps) seeded from
   trial_seed; earliest = raw t over Δt > −Δt_bx/2; k ≤ −1 kept (mixing); P_OOT = one factor on M_¬pres; σ_ln,PV and
   σ_ln,σt by fixed-window variation (mechanical fallback); signal-side conventions pre-registered | §1.4, §6.2, §4.1 |
   FIX_SRT_TMIN_R1/R2/R3, REVIEW_SRT_TMIN_R1/R2 |
```

Applying this needs a logged WP_RULE / frozen_inputs change with a re-hash, and a re-review, before any SR-T signal ε.
C1 production is unaffected: every input is already stored.
