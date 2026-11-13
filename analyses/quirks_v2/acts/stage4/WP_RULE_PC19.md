# WP_RULE_PC19: the SR-T window, PV time and out-of-time background (amendment PC-19 to WP_RULE.md)

| | |
|---|---|
| **Date** | 2026-10-14 |
| **Status** | Final and frozen; this file is read-only. |
| **Approval** | The user approved the three design points (relayed by the orchestrator, 2026-10-14). |
| **Review trail** | FIX_SRT_TMIN_R1 → REVIEW R1 (ITERATE 1A 3B 6C) → FIX R2 → REVIEW R2 (ITERATE 0A 1B 6C) → FIX R3 → REVIEW R3 (**PASS** 0A 0B 5C). The R3 C items are folded in here (C-2 to C-5 wording) and in `acts/stage4/g3/srt_tmin_check.py` (C-1). All files are in `acts/stage4/review/`. |
| **Evidence (G3, illustrative)** | `data/acts_stage4/g3/srt_tmin_check_v2*.json` and `srt_sigma_ln_pv.json`. The binding values come from C1 B1. |
| **Hashes** | `acts/stage4/HASH_ADDENDUM.md` §6 |

**The three approved design points.**
1. **Upper window edge.** t_max is derived from the next-crossing (k = +1) per-hit rate. The upper edge is not
   Δt_acc = 25 ns.
2. **Threshold.** The threshold is 10⁻⁴ at each edge, not a split budget.
3. **PV time spread.** σ_t,PV = 190 ps nominal, varied at 150 and 230 ps.

**Precedence.**
- This file amends `WP_RULE.md` for **all SR-T quantities**: §1.4 (SR-T / SR-G, l.181-215), §4.1 (the σ_ln² line,
  l.331), §6.2 (the SR-T method row l.457 and the SR-T composition l.468-472, PC-18), Appendix A (the `sr_t` row,
  l.950) and the PC table (§10).
- Where the two texts differ on an SR-T quantity, **this file takes precedence**.
- `WP_RULE.md` (sha256 `1b2ea9bd…`, checked by `run_stage4` during production) and `frozen_inputs.json` are **not
  edited**. The constants listed at the end of this file belong to this file and are not read by any production code.
- Production is unaffected. The window, the PV time and the overlay are offline by construction, and every input is
  already stored.
- §5.4 item 7 holds unchanged: t_min and the window come from PU-only B1 and the overlay only.

---

## §1.4 (SR-T / SR-G): replaces WP_RULE l.184 and l.188-189; amends l.206-210

### Definition

- SR-T requires that the **earliest** in-band BTL hit has Δt ∈ [t_min, t_max].
  - Δt = t_BTL − t_PV − |u|/c.
  - "Earliest" is the smallest raw t_BTL among the in-band hits with Δt > −Δt_bx/2, where Δt_bx = 25 ns.
- Previous-crossing hits that arrive promptly are not used. They could only veto, so leaving them out is conservative
  for B.
- Delayed previous-crossing hits (k ≤ −1, Δt > −Δt_bx/2) are used, and they stay in B.
- SR-G is everything else.

### PV time

- **PU-only events.** t_PV = σ_t,PV · z, drawn once per event.
  - z = `numpy.random.default_rng([trial_seed, 0x5254]).standard_normal()`.
  - trial_seed is the one of the event's road-0 trial. If an event has no road-0 trial, use the lowest road present.
  - The 4 roads share one PV, so they share t_PV.
  - σ_t,PV = 190 ps. This is the luminous region of plan §1.3; the PU vertex times use the same value.
- **Signal and SM samples.** t_PV is the true vertex time: `vtx[3]` for signal and `hs_vtx[3]` for SM.
- Any PV-resolution term is applied in the same way to all samples. The baseline has none.

### Fixed inputs

- σ_t = 35 ps, with a 60 ps variation.
- Δt_acc = 25 ns, with a 12.5 ns variation. Δt_acc is the hit-time acceptance; the window edge is t_max.

### Out-of-time overlay

- It consists of the BTL hits of independent PU-200 events, shifted by k × 25 ns, with k ∈ {−12, …, +3}. This is the
  TDR readout window: 12 previous and 3 following crossings.
- Each overlay event keeps its own per-crossing BTL time spread.

### Mixing

Crossing k ≠ 0 of a B1 candidate in event e, in a job with n_ev events, uses the S5 BTL hits of event e + j (mod n_ev)
of the same job. The hits are taken about the candidate's own plane, axis, PV and t_PV.
- **k = +1:** j = 1, 2, 3 (three independent realisations), at t + 25 ns.
- **k = −j:** j = 1…12, at t − 25j.
- **Event count.** This needs n_ev ≥ 13 per job. G3B1 and C1/C2B B1 jobs have n_ev = 25.
- **Shared partners.** Realisation j of k = +1 and crossing −j share partner e + j for j = 1-3. Each term of the additive
  P_OOT stays unbiased; the sharing affects only the bootstrap variance.

### Window edges

- **Per-hit rate.** R_k(a, b) = N_k(Δt ∈ [a, b]) / N_k.
  - The counts are per (candidate, in-band hit) pair, over the B1 loose candidates (S3 ∧ R01).
  - They are normalised per pair of the same crossing.
  - The k = +1 spectrum uses realisation j = 1.
- **The edges, on a 5 ps grid:**
  - **t_max** = min(Δt_acc, the largest t ≤ Δt_bx with R₊₁(Δt_bx/2, t) < 10⁻⁴). This is the leading edge of the next
    crossing.
  - **t_min** = the smallest t ≥ 0 with R₀(t, t_max) < 10⁻⁴. This is the in-time late tail.
  - The threshold is 10⁻⁴ **per edge** (user-approved).
- **When they are fixed.** Both edges come only from PU-only C1 B1 plus the overlay (§5.4 item 7), before any signal
  ε, at the nominal σ_t (35 ps) and σ_t,PV (190 ps).
- **Reported:** R₀, R₊₁ and R_{k≤−1} = Σ_{j=1..12} R₀(t_min + 25j, t_max + 25j) in the window. Each one is given with
  its 95 % bound when it is 0.
- **G3 (illustrative):** [6.07, 24.025] ns.

### Stored fields

- **Per stored candidate (any ρ):** `btl_n_band`, `btl_n_int` and `btl_dt0`.
  - `btl_dt0` is the Δt of the in-band hit with the smallest raw time, stored with t_PV = 0.
  - Offline, Δt = btl_dt0 − t_PV, with t_PV as defined above.
  - Under the σ_t variation, the Δt is recomputed from the smeared S5 hits instead.
- **Not in-job, by construction:** the time window [t_min, t_max], the PV time and the out-of-time overlay.
- The in-job columns r ∧ BTL-present are unchanged (PC-17).

---

## §6.2 (SR-T composition; completes PC-18) and §4.1 (σ_ln): replaces WP_RULE l.468-472 and amends l.331

### The SR-T background term

SR-T: P̂₁(r ∧ BTL-present) × P(late) + P̂₁(r ∧ ¬BTL-present) × P_OOT(late).

- **P(late)** is the fraction of the BTL-present candidates in the measuring population whose earliest in-time in-band
  hit has Δt ∈ [t_min, t_max].
- **P_OOT(late)** = [n̄₊₁ + n_{k≤−1}] / M_¬pres.
  - It is **one §4.2 factor**.
  - M_¬pres is the number of candidates in the measuring population **without an in-time in-band BTL hit**.
- **n̄₊₁** is the mean, over the three k = +1 realisations, of the number of those candidates whose earliest mixed k = +1
  in-band hit has Δt ∈ [t_min, t_max].
- **n_{k≤−1}** = Σ_{j=1..12} of the number of those candidates that have a mixed crossing −j in-band hit with
  Δt ∈ [t_min, t_max].
  - The sum over j is conservative compared with the union.
  - The proxy is the partner's maximum Δt ≥ t_min + 25j.
  - It enters at its measured value. It is also reported as a separate line, with the 95 % bound 3/M_¬pres when it is
    0.
- The number of distinct events behind each count is reported. σ_ln,stat comes from the §4.2 event bootstrap.

### Timing-model σ_ln terms

These terms are mechanical and fixed before C1 is seen.

- **Quantity.** L(P) = f_pres · P(late) + f_¬pres · P_OOT(late), on population P, with the window held at the nominal
  edges.
- **Variation sets.**
  - {σ_t,PV = 150, 230 ps} gives σ_ln,PV.
  - {σ_t = 60 ps} gives σ_ln,σt.
  - Each variation uses the same z draws and seeds as the nominal.
  - σ_t = 60 ps is applied as +48.7 ps Gaussian smearing of the stored S5 t, seeded by [job seed, 0x534D]. It is
    applied to the in-time hits and to the mixed hits.
- **Formula.** σ_ln,X(P) = the maximum, over the variations v of the set, of |ln(L_v(P) / L_nom(P))|.
- **Population for SR-T ladder rung r:** the B1 ρ = 1 candidate records passing r, i.e. S3 ∧ r for r < R04 and S2 ∧ r
  for r ≥ R04.
- **Qualification.** Rung r qualifies if its late count is ≥ 10 in the nominal run **and** in every variation of the
  set. The late count is C = (in-time late) + Σ over the 3 k = +1 realisations of (OOT late) + n_{k≤−1}.
- **Fallback.**
  - A rung that does not qualify takes the value of the deepest qualifying rung before it in ladder order.
  - A factorised F1 rung takes the value of its parent in-job rung, as in the §6.2 composition:
    - R15-R20 (h, o) take it from R14;
    - R21-R23 (dE/dx) take it from R14 ∧ e_x (column F0e>x);
    - the fallback rungs take it from FB_k[∧ e].
  - The same fallback then applies to that parent.
  - If **no rung before it** qualifies, σ_ln,X = 1.0.
- **Scope.** These terms apply only to the SR-T term of B_PU, and to both of its summands. They do not apply to B_SM
  (true `hs_vtx[3]`, not varied), to the C′₀ / C′_PU terms, or to SR-G.
- **§4.1 slot.** For B_PU,SR-T(r):

  σ_ln² = stat² + (extrapolation-model spread)² + (density normalisation)² + (normalisation)² + σ_ln,PV(r)² + σ_ln,σt(r)².

  For every other term, both new terms are 0.
- **G3 (illustrative), from `srt_sigma_ln_pv.json`:** σ_ln,PV = 0.588 (loose) and 0.306 (R04); σ_ln,σt = 0.032
  (loose) and 0.016 (R04).

### Signal ε_SR-T (pre-registered)

- It uses the same Δt, t_PV and "earliest" definitions as above.
- **Assigning OOT events.** Crossing k ∈ {−12…−1, +1…+3} of signal row (spin, m, row) uses C1 B1 event index
  i_k = int.from_bytes(blake2b(f"srt-oot|{spin}|{m}|{row}|{k}".encode(), digest_size=8).digest(), "big") mod N_B1.
  - C1 B1 events are ordered by (job id, ev).
  - If i_k is already used by an earlier crossing of the **same row** (crossings in the order −12…−1, +1…+3), it is
    incremented mod N_B1 until it is unused. Events are not required to be unique across rows.
- Those hits enter the earliest-hit ordering, so they can veto.
- A candidate whose **earliest in-band hit (Δt > −Δt_bx/2) is an OOT PU hit** is **not** counted in ε_SR-T. OOT-PU
  lateness earns no credit.
- In-time PU hits of the signal overlay are treated as in production. Their late credit is at most
  P(late | present) ≈ 1.5 × 10⁻⁴ × f_pres, which is immaterial.

### Model limits (caveat for the analysis note)

- The PU is simulated with Fatras only. There are no SiPM dark counts or noise and no neutron or cavern background.
- The slow-particle tail is as simulated.
- A flat random in-band hit rate would fill [t_min, t_max], and it is not in B.

---

## Appendix A `sr_t` constants of this amendment

These constants belong to this file. `frozen_inputs.json` is not edited.

```json
{"t_max": "from C1 B1 + k=+1 mixing by this rule", "t_min": "from C1 B1 in-time spectrum by this rule",
 "dt_bx_ns": 25.0, "edge_grid_ns": 0.005, "late_rate_threshold_per_edge": 1e-4,
 "sigma_t_pv_ps": 190.0, "sigma_t_pv_variation_ps": [150, 230], "sigma_t_variation_extra_smear_ps": 48.7,
 "tpv_seed_salt": 21076, "smear_seed_salt": 21325,
 "oot_mixing": {"kp1_partners": [1, 2, 3], "km_partners": "1..12", "min_n_ev": 13},
 "reference_implementation": "acts/stage4/g3/srt_tmin_check.py (sha256 in HASH_ADDENDUM.md §6)"}
```

## PC table row

| PC-19 | SR-T window [t_min, t_max] (t_max = the k=+1 leading edge, 10⁻⁴ per edge); PU-only t_PV ~ N(0, 190 ps) seeded from trial_seed; earliest = raw t over Δt > −Δt_bx/2; k ≤ −1 kept (mixing); P_OOT = one factor on M_¬pres; σ_ln,PV and σ_ln,σt by fixed-window variation (mechanical fallback); signal-side conventions pre-registered | §1.4, §4.1, §6.2, App. A | FIX_SRT_TMIN_R1-R3, REVIEW_SRT_TMIN_R1-R3; user approval 2026-10-14 |
