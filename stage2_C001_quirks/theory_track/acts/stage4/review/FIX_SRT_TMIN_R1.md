# FIX_SRT_TMIN_R1: the SR-T t_min definition with the out-of-time overlay

- **Finding.** `acts/stage4/g3/G3_REPORT.md` §2 (l.100-108), §7 item 6 and §8 item 3. With the frozen OOT overlay, t_min
  comes out as Δt_acc = 25 ns, so the SR-T window is empty.
- **Scope.** This file is PU-only. No signal efficiency was computed or looked at. Nothing frozen was edited: the text
  below is a **proposal, not applied**. The check script is new (`acts/stage4/g3/srt_tmin_check.py`); it reads
  `data/acts_stage4/prod/G3/G3B1` read-only and writes only `data/acts_stage4/g3/srt_tmin_check.json` and
  `srt_dt_hist_kp1.npy`.
- **Status.** PARTIALLY RESOLVED. The defect is diagnosed, an amendment is proposed and checked on G3, and production
  storage is confirmed sufficient. Applying the amendment needs the orchestrator/user decision in §4 and a logged
  re-review, because WP_RULE is frozen.

## 1. Diagnosis

**What t_min is meant to be.**
- Plan §2.3 (`plan.md` l.577-583) motivates t_min with the **in-time** PU per-hit tail: "> 2 ns 2.8 %, > 5 ns 7 × 10⁻⁴,
  > 10 ns 0/5610".
- It defines t_min as "the delay at which the per-hit rate in B1 falls below 10⁻⁴".
- The OOT overlay is named so that the **late fraction**, i.e. the background, includes out-of-time hits (plan l.1138;
  WP_RULE l.457).
- So t_min is the lower edge of the window: the point where the **in-time PU timing tail** becomes negligible.

**What the frozen text says.** WP_RULE l.188-189: "t_min = the smallest delay at which the per-hit late rate (in-band BTL
hits of B1 loose candidates, **in-time spectrum ⊕ overlay**) falls below 10⁻⁴", with the window [t_min, Δt_acc] (l.184),
Δt_acc = 25 ns (l.185) and the overlay k ∈ {−12…+3} at k × 25 ns (l.186-187).

**Why it gives 25 ns.** This is not an artefact of the G3 code; the frozen definition cannot be satisfied.
- The window's upper edge Δt_acc = 25 ns is exactly the arrival time of the **prompt hits of the next crossing (k = +1)**.
- The in-time per-hit Δt spectrum spans −0.93 to +6.51 ns. 14.0 % of in-time hits have Δt < 0, so 14 % of the k = +1
  hits land at Δt < 25 ns (VERIFIED, `srt_dt_hist.npy`; R₊₁(12.5, 25) = 0.139).
- These hits fall inside [t, 25 ns] for **every** t < 24.1 ns. No t_min below the k = +1 leading edge can meet 10⁻⁴, and
  the first grid point that does is t = Δt_acc, which gives an empty window.
- `analyse_g3.py` l.322-344 (`tmin_from_hist`) implements the text faithfully. It even dilutes the rate in the overlay's
  favour: l.330 divides by all 16 crossings' hits, a ×16 looser threshold. R(t) still stays at 8.8 × 10⁻³ up to 24.5 ns.

**A second, latent defect of the same kind (not reached at G3).**
- "Δt of the **earliest** in-band BTL hit" (l.184), read literally with an overlay that includes 12 *previous* crossings,
  makes a previous-crossing hit at Δt ≤ −24 ns the earliest hit.
- 23.9 % (loose) and 15.9 % (R04) of candidates have ≥ 1 in-band hit from a single extra crossing (VERIFIED, explicit
  mixing below).
- Over 12 crossings, a veto would therefore hit about 96 % / 87 % of candidates (ESTIMATE, 1 − (1 − f)¹²). This
  suppresses signal and background alike in an unintended way.
- G3 avoided it because its late tag used only the stored in-time `btl_dt0` (`analyse_g3.py` l.740).

**PC-18 intent.**
- PC-18 (WP_RULE l.468-472 and l.818; `FIX_WP_RULE_R2.md` l.153-159) was added for exactly the k = +1 case: a candidate
  without an in-time in-band hit whose earliest in-band hit is a k = +1 hit "at the Δt_acc edge".
- That term adds P̂₁(r ∧ ¬present) × P_oot(late) to B. The rule's intent is therefore:
  - the OOT background is **counted in B** through PC-18;
  - the OOT background is **not** used to place t_min.
- If Δt_acc = 25 ns stays the upper edge, the PC-18 term is large (§3: P_oot(late | ¬present) = 3.4 × 10⁻² loose,
  1.9 × 10⁻² R04).

**Production is unaffected.**
- The window and the overlay are offline by construction (l.208-210).
- The in-job columns `n_pass_T` / `S_ded_T` (r ∧ present) do not depend on t_min.

## 2. Proposed amended rule text (diff, NOT applied)

WP_RULE §1.4, replacing l.188-189, plus two consequential edits:

```diff
-  - SR-T: ≥ 1 in-band BTL hit with Δt ∈ [t_min, Δt_acc]. Δt = t_BTL − t_PV − |u|/c of the **earliest** in-band BTL hit.
+  - SR-T: ≥ 1 in-band BTL hit with Δt ∈ [t_min, t_max]. Δt = t_BTL − t_PV − |u|/c of the **earliest** in-band BTL hit
+    with Δt > −Δt_bx/2 (Δt_bx = 25 ns, the bunch spacing). Hits of earlier crossings are not used; they could only veto,
+    so this is conservative for B (FIX_SRT_TMIN_R1).
   - σ_t = 35 ps (60 ps variation); Δt_acc = 25 ns (12.5 ns variation).
   - **Out-of-time overlay:** BTL hits of independent PU-200 events shifted by k × 25 ns, k ∈ {−12, …, +3} (the TDR
     readout window: 12 previous and 3 following crossings), each with its per-crossing BTL time spread.
-  - **t_min** = the smallest delay at which the per-hit late rate (in-band BTL hits of B1 loose candidates, in-time
-    spectrum ⊕ overlay) falls below 10⁻⁴; fixed from PU-only B1 + overlay only (§2.5 item 7), before any signal ε.
+  - **Window edges.** R_k(a, b) = N_k(Δt ∈ [a, b]) / N_k, the per-hit rate of the in-band BTL hits of the B1 loose
+    candidates (S3 ∧ R01) from crossing k, normalised per hit of that crossing. k = 0 is in time. k = +1 is built by
+    explicit event mixing: the candidates of event e get the S5 BTL hits of event e + 1 (mod n_ev) of the same job,
+    with t + 25 ns, about the candidate's own plane, axis and PV.
+    - **t_max** = min(Δt_acc, the largest t ≤ Δt_bx with R₊₁(Δt_bx/2, t) < 10⁻⁴). This is the leading edge of the
+      next crossing.
+    - **t_min** = the smallest t ≥ 0 with R₀(t, t_max) < 10⁻⁴. This is the in-time late tail.
+    - Both edges are fixed from PU-only B1 + overlay only (§2.5 item 7), before any signal ε, and are re-derived for
+      each σ_t / Δt_acc variation (60 ps by extra offline smearing of the stored t).
+    - The per-hit window occupancy R₀ + R₊₁ (< 2 × 10⁻⁴ by construction) is reported. k ≤ −1 is excluded by the Δt
+      cut above. k ≥ +2 lands at Δt ≳ 49 ns > t_max and is later than any k = +1 hit.
```

The consequential edits change no logic:
- l.208 "the time window [t_min, Δt_acc]" becomes "[t_min, t_max]";
- l.470 (PC-18) "lands in [t_min, Δt_acc]" becomes "lands in [t_min, t_max]";
- PC-18 is completed with "P_oot(late) = fraction of the candidates in the measuring population (≥ 10 counts, §4.2)
  whose earliest k = +1 mixed in-band hit has Δt ∈ [t_min, t_max]";
- the Appendix A `sr_t` row (l.950) and `frozen_inputs.json` gain `t_max` and `dt_bx_ns`;
- a new plan-change row PC-19 is added.

**(a) No reference to signal.** Both edges are quantiles of PU-only per-hit spectra at the frozen 10⁻⁴. Δt_bx and
Δt_acc are detector constants.

**(b) The OOT background is counted conservatively.**
- PC-18 is kept, with P_oot measured by explicit mixing (not zero: §3).
- Previous-crossing hits are never allowed to veto.
- For a candidate with an in-time hit, the decomposition is exact. Its earliest hit is in-time unless that hit is
  already > t_max, and none of the 594 708 in-time hits is.

**(c) Computable from stored data: YES.** C1/C2B B1 jobs are 25 events × 4 roads (`jobs/C1.json`, `C2B.json`), so
mixing is possible within each job. Each needed input is written by the frozen runner:
- S5 all BTL hits per event (ev, sid, x, y, z, s0, s1, dE, t, INT), `run_stage4.py` l.382-384 and l.510-511;
- per-trial `trials.pv` (l.469) and `trials.ev`;
- per-candidate `tag`, `trial`, `rungs`, `normal`, `axis`, `btl_n_band`, `btl_dt0` (`production.py` l.419-451);
- t_tol and w_c in `meta.finder_cfg`;
- the in-job r ∧ present columns (S1/S1′).

The stored fields reproduce exactly. On 3.77 × 10⁶ G3 candidates, re-running the band kernel against the stored
`btl_n_band` / `btl_dt0` gives 3 float32 band-edge mismatches and max |Δdt0| = 8 × 10⁻⁷ ns (VERIFIED).

**No production change is needed.**

## 3. Check on G3 (`srt_tmin_check.py`, 23 s, 1 core, nice 15; `data/acts_stage4/g3/srt_tmin_check.json`)

The sample is G3B1: 77 jobs, T_seed = 6, PU-only. The final edges come from C1's own B1.

| quantity | value | tag |
|---|---|---|
| t_min (in-time tail, R₀ < 10⁻⁴) | **6.12 ns** (as G3's in-time value; R₀ = 9.4 × 10⁻⁵) | VERIFIED |
| t_max (k = +1 leading edge, explicit mixing) | **24.275 ns** (R₊₁ = 7.7 × 10⁻⁵); copy method 24.31 ns | VERIFIED |
| per-hit window occupancy R₀ + R₊₁ | 1.7 × 10⁻⁴ | VERIFIED |
| loose (S3 ∧ R01), 1 963 659 candidates | present 24.8 %; P(late \| present) = 34/487 729 = **7.0 × 10⁻⁵**; P_oot(late \| ¬present) = 31/1 475 930 = **2.1 × 10⁻⁵**; **SR-T fraction 3.3 × 10⁻⁵** | VERIFIED (counts) |
| R04 (S2), 1 824 063 candidates | present 17.6 %; 48/320 142 = **1.5 × 10⁻⁴**; 10/1 503 921 = **6.6 × 10⁻⁶**; **SR-T fraction 3.2 × 10⁻⁵** | VERIFIED (counts) |
| same, upper edge kept at Δt_acc = 25 ns (t_min = 6.12) | P_oot(late \| ¬present) = 3.4 × 10⁻² (loose), 1.9 × 10⁻² (R04); SR-T fraction 2.6 × 10⁻² / 1.6 × 10⁻² | VERIFIED |

- **Caveat on t_max.** It depends on the per-crossing time spread. The vertex time is smeared by the beam-spot σ_t
  (`code/s4pu.py` l.136-138; the value itself was not re-checked by this fixer, UNVERIFIED) and on σ_t = 35 ps.
- **Counting rule.** The counts are event-clustered. The B estimate uses them only through the frozen ≥ 10-count and
  zero-count rules.

## 4. Rejected alternatives, and what is a defect fix vs a design decision

Rejected:
1. **Literal reading (t_min = 25 ns, SR-T empty).** It deletes a pre-registered category and wastes its budget share.
   The text cannot be satisfied, so this is not a conservative choice.
2. **G3's shifted-copy overlay with a 16-crossing denominator.** It dilutes the 10⁻⁴ threshold ×16, which is
   anti-conservative. Copies also miss the candidate–hit geometry correlation: the in-time presence is 24.8 % against
   23.9 % from mixing, because the candidate's own particles reach the BTL. Mixing is exact and cheap.
3. **Moving the Δt_acc baseline to its 12.5 ns variation.** That changes a frozen hit-acceptance baseline, not the SR-T
   edge. It would also cut the late window by half on grounds that touch the signal side (heavy-mass delays are
   15-27 ns), so it is not a signal-free fix.

**Defect fixes** (they restore the stated intent and contain no new choice):
- t_min is defined on the in-time tail;
- "earliest" excludes earlier crossings;
- rates are normalised per hit of the same crossing;
- P_oot uses explicit mixing.

**Design decision for the user** (it changes the window's upper edge, a definition change):
- **Recommended:** t_max = 24.3 ns, set by the k = +1 leading edge at the same 10⁻⁴. SR-T PU fraction ≈ 3 × 10⁻⁵.
- **Alternative:** keep the upper edge at Δt_acc = 25 ns and let PC-18 carry the k = +1 hits. This is valid and
  conservative, but the SR-T PU fraction is ≈ 2 × 10⁻², about 10³ times larger, so SR-T would keep only about 1.7
  decades of time rejection.
- **Secondary option:** one 10⁻⁴ budget split across both edges instead of 10⁻⁴ per edge (total ≤ 2 × 10⁻⁴).

Whichever is chosen must be logged as PC-19, entered in WP_RULE / frozen_inputs with a re-hash, and re-reviewed before
any SR-T signal ε.
