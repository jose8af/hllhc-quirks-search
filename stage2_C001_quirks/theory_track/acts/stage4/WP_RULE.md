# WP_RULE.md: Stage-4 working-point rule and frozen definitions (C001 quirks theory track)

> **STATUS: FREEZE CANDIDATE (fix R2 of review `review/REVIEW_WP_RULE_R2.md`, 2026-10-13; fix R1:
> `review/FIX_WP_RULE_R1.md`). NOT YET FROZEN.** The orchestrator checks the R2 diffs (`review/FIX_WP_RULE_R2.md`) and
> freezes. This file transcribes everything that
> plan §2.5 item 9 requires to be frozen, from `acts/stage4/plan.md` (review R9 PASS; its sha256 is in Appendix A.3).
>
> **No signal efficiency has been computed.** No signal efficiency, signal toy or signal yield was looked at to write
> it. The only signal-derived inputs are generator/truth-level quantities that the plan pre-declares as rule inputs: δ₉₅
> (truth pT(QQ̄) and the MET model, §1.3), βγ_IT and Λ_R (§8), and the truth TBPX quirk-hit counts of the dE/dx dilution
> model (§8). None is a detector-level signal efficiency.
>
> Where this file and the plan differ, the plan wins **except for the logged plan changes PC-1…PC-17 of §10**, which
> this file supersedes the plan on. The former **[DRAFT-D*n*]** items are resolved (§10); the tags are kept as anchors.
> No input is open: the MIP unit (F-2) is filled from G1's V4-9 muon gun (§1.4, fix R2).

Notation: a rung r is a cumulative selection. "Passes R*k*" means it passes every requirement of rungs 1…k.
B₈₄ = the 84th percentile of the log-normal background sum. q = 1/ρ.

---

## 0. Freeze scope (plan §2.5 item 9) → sections of this file

| plan §2.5 item 9 element | here |
|---|---|
| the ladders (23 rungs per category), with thresholds and order | §3 |
| the variable definitions (incl. w_core and χ²_core) | §1 (and §2 for the per-hit-set convention) |
| the budget split (0.11 + 0.11 and its branches) | §5 |
| the B sum and the B₈₄ rule | §4 |
| the per-family extrapolation methods and closure tests (§4.1), with the failure paths | §6 |
| the zero- and low-count rule (item 4a) | §4.2 |
| the C′ preselection and attribution rules: σ̂_h, δn_max, σ_tot with δn = 0, the shared PV/hit hand-over (pre-CKF, pre-merge toy measurements), the C′₀ necessity check V4-10 and its failure path | §7 |
| the fallback deliverable: admissibility rule, frozen inputs (smoothed Λ_R, the βγ_IT table and its hash), fallback selections (§2.6) | §8, Appendix A |
| the campaign definitions (§6.2) | §9 |
| this rule (§2.5 items 1-11) | §5.4 |
| (Phase A additions requested by the orchestrator) storage policy; sub-sampling fractions; in-job weight method; code sha256 | §S, §6.3, Appendix A.3 |

---

## 1. Variable definitions

### 1.1 F0 finder (plan §2.2; code `acts/stage4/finder/`, equivalent to `probes/f1r_finder.py`, `G2A_REPORT.md`)

Input: the hit pool after CKF removal (§1.6), analysis-level merging (U-5 b) and the hit-time window, plus the PV and the
MET of §1.7. The PU-only trial PV is a luminous-region point (σ_xy 5 µm, σ_z 45 mm) drawn independently of the PU
vertices (§4.1 step 1). The coordinates are u = x − PV.

1. **Window and road.** W_c = 75 mm (= R(TBPX L4)/2 rounded up).
   - Road: |Δφ(u, φ_MET)| < δ_road + asin(min(1, W_c/r)), with **δ_road = δ₉₅ = 0.15 rad** (§1.3), in the hit road
     **and** in the seeding. Code: `production.process_trial` raises unless `finder.Config.road == WCfg.delta95`; with
     no `cfg` it builds `Config(road=WCfg.delta95)`; `production.config_from_frozen(frozen_inputs)` and
     `run_stage4.finder_configs` build both from `frozen_inputs.json`; the per-trial row records road, δ₉₅ and η_max
     (review WP_RULE R1 A-1).
   - Hits must be forward of the PV (u·n₃ > 0) and within |u·n₂| < W_c.
2. **Seeds (barrel).** Pairs (a ∈ TBPX L4, b ∈ L3):
   - |Δφ_ab| < 0.3 and |Δη_ab| < 0.2;
   - n = unit(u_a × u_b), skipped if sin∠(u_a, u_b) < 10⁻³;
   - kept if some c ∈ L2 (|Δφ_bc| ≤ 0.4) has |n·u_c| < 3σ_tot,c (with the seed term σ_seed|u_c|, σ_seed = 0.03/(|u_b| sin∠));
   - seed score = the number of layers with ≥ 2 crossings in the seed band; **T_seed = 6**.

   **Barrel-only (D4-12 re-decided by the user, 2026-10-13; PC-7).** The endcap/mixed triplets and the (L3, L2, L1)
   missing-L4 family of plan §2.2 item 2 are **not in scope**; they are documented future work (§8 "cannot claim"). An
   endcap category, if added later, gets its own background-only ladder, frozen before its first signal efficiency (the
   D4-14 precedent), and is not part of this rule.
3. **Collection.** |n·u| < 3σ_tot.
   - **σ_tot² = σ_n²(n, hit) + t_tol², with no normal-uncertainty term (δn = 0)**; t_tol = 30 µm.
   - σ_n comes from the local errors projected on n: σ_n² = (−n_x c_y + n_y c_x)² σ₀² + n_z² σ₁², floored at 10⁻⁴ mm.
   - The pre-declared variation (not the default) is δn = min(δn_fit, δn_max), added in quadrature as (δn·|u|)², with
     δn_max = 2 mrad. It runs in A5/B1 beside t_tol = 0 / 100 µm.
4. **Refit.**
   - Pre-filter |u·n_seed| < 5 mm (IT, PS) / 60 mm (2S).
   - 3 iterations of the PV-constrained weighted plane fit: n = the smallest eigenvector of Σ wᵢ uᵢuᵢᵀ, wᵢ = 1/σ_tot,i².
   - Re-collect at 3σ_tot each time; the axis n₃ is re-estimated each iteration as the in-plane mean hit direction.
   - Every distinct (a, b) seed with seed N_L2 ≥ T_seed is refitted. A candidate needs N_L2 ≥ 4.
   - Ranking (−N_L2, χ²/ndf), stable.
   - Duplicate merge: a candidate whose normal is within 2 mrad (|1 − |n·g|| < 2·10⁻⁶) of an already-kept one is dropped.
5. **Crossings.**
   - Single-sensor layers (TBPX): n_hits.
   - Stacked OT layers (TBPS, TB2S): min(n_in, n_out).
   - Layer counts: N_IT2 = TBPX layers with ≥ 2 crossings; N_IP2 = IT + PS (TBPX L1-4, TBPS L1-3) layers with ≥ 2;
     N_2S2 = TB2S layers with ≥ 2; N_OT2; N_L2 = N_IP2 + N_2S2 (diagnostic).
   - The R0 hit count (N_OT2h) is a diagnostic only.
6. **w_core** = 1.4826 × MAD of u·n₂ over the candidate's in-band IT + PS hits, with centre c = their median.
   - One step, no iteration; 2S hits excluded. n₂ = n × n₃ of the final refit.
   - The iteratively trimmed width is rejected.
7. **χ²_core** = λ_min(Σ_core wᵢ uᵢuᵢᵀ)/(n_core − 2).
   - Core = IT + PS in-band hits with |u·n₂ − c| **≤** 2.5 w_core (closed interval, as in every kernel), plus 2S hits whose n₂ coordinate lies within that interval
     enlarged by 3σ of their n₂ projection (3|n₂,z|σ₁).
   - One step. Defined for n_core ≥ 4.
   - p(χ²_core) = P(χ²_{n_core−2} > λ_min). Undefined p fails every p rung.
8. **|Δφ(n₃, MET)|**: the azimuth difference of the final axis and the MET.
9. **f_CKF = n_CKF,band / (n_CKF,band + n_band)** **[D5, resolved]**.
   - n_band = the candidate's in-band hits (its final hit set); n_CKF,band = the CKF-used measurements (removed from the
     pool before the finder, §1.6 item 1; chain flag bit 0) that lie in the candidate's **final band**: road (§1.1
     item 1), |n·u| < 3σ_tot (δn = 0), forward u·n₃ > 0, |u·n₂| < W_c, on the 10 barrel counting layers.
   - One implementation: `chain_inputs.ckf_band_counts`, called by `production.process_trial(..., ckf=)` (stores
     `n_ckf_band`, `n_band`, `f_ckf` per stored candidate) and by `run_stage4`. ckf = None (interim chain): −1 / NaN.
   - The count of CKF tracks with ≥ 5 band hits (review B-6) is **not stored**: the chain hands over no CKF track id.
     It is a diagnostic only and enters no rule.
   - Treatment in B: see §1.2.
10. **Stored only, never cut on:** Δw (rms of u·n₂, all in-band hits), |n_z|, χ²/ndf (all hits), the stub-match count,
    seed N_L2 (stored as a lower bound ≥ T_seed), and the truth composition.

### 1.2 F0 selection (plan §2.2 item 6)

- **Fixed cuts at every rung:** N_IT2 ≥ 3, **|Δφ(n₃, MET)| < δ₉₅ = 0.15 rad**, **|η(n₃)| < η_max = 1.0**, f_CKF < 0.2.
- **|η(n₃)| < η_max = 1.0 (barrel-only selection; PC-7).** η(n₃) = asinh(n₃,z / √(n₃,x² + n₃,y²)) of the final axis
  (PV frame). The value is fixed from the barrel geometry alone (`surfaces_s3.json`; no signal input):
  - the barrel edges seen from the nominal IP, asinh(z_half/r) (`sim/stage3/code/surfaces_s3.json`; corrected in fix
    R2, review WP_RULE R2 B-1), are: TBPX L4 1.12 (the outer seeding layer, needed by R04 and every rung); TBPX L3
    1.41; TB2S L1 1.30-1.31; TB2S L2 1.12 (needed by N_2S2 ≥ 2, R13); TB2S L3 **0.94** (needed by N_2S2 ≥ 3, i.e. R14
    and every FB selection); ≥ 1.57 for the other IT/PS layers (TBPX L1 2.60, L2 1.90; TBPS L1-L3 2.27-1.57);
  - **η_max = 1.0 is the TB2S L3 edge (0.94) rounded UP to one decimal.** It lies below the seeding-layer edge, so the
    seeding acceptance is complete at |z_PV| ≲ 29 mm (z = r·sinh 1.0 = 172 mm at TBPX L4 vs z_half = 201 mm).
  - **Consequence:** for 0.94 ≲ |η(n₃)| < 1.0 (nominal IP; the edge moves with z_PV) the axis leaves the TB2S L3
    coverage, so R14 and every FB selection (N_2S2 ≥ 3) have reduced acceptance there, for signal and background
    alike. ε carries it; no rung is changed. The value is geometry-only either way (no signal input).
  - It is applied in-job like the Δφ cut (`production`: `aligned = (Δφ < δ₉₅) ∧ (|η(n₃)| < η_max)` before every
    rung, the grouping population, the DP and the IS); the axis is fixed under thinning, so the ρ = 2 weights are exact
    in it. Signal applies the same cut; ε carries the fiducial loss explicitly.
  - **Smoke (PU-only, interim, `data/acts_stage4/wp_fix1/regress_smoke.json`):** with δ₉₅ = 0.15 and η_max = 1.0,
    R04 keeps 441/737 and 309/446 candidates (ρ = 1) and 19 318/28 890 (ρ = 2) of the δ₉₅ = 0.25, no-η values.
- **f_CKF < 0.2 is a selection cut for signal, SM C, C′_PU and C′₀, not for B_PU (review B-6).**
  - B_PU credits **no** f_CKF rejection (factor 1). The in-job ladders (B1 and B2 columns) are f_CKF-free, so T1, T1w,
    T1e compare identical selections. This is conservative; plan §2.6 rates f_CKF as weak on combinatorial PU.
  - SM C, C′_PU and C′₀ apply it as a rung factor from the stored records (`f_ckf`, rule 4a); signal applies it in the
    selection.
- **Ladder thresholds:** N_IP2, w_core, p(χ²_core) and N_2S2 (§3).
- **No fixed Δw cut.**

### 1.3 δ₉₅ (plan §2.5 item 2)

**Frozen value: δ₉₅ = 0.15 rad** (F-1, review B-4). It is one global value (the cut acts on background at every rung),
used as δ_road (hit road and seeding) and as the fixed cut (`finder.Config.road = production.WCfg.delta95 = 0.15`). The
planning value 0.25 rad (synthesis S-5) is used only by dev/smoke runs.

**The rule (generator level; no detector response, no PU, no detector-level efficiency), exactly as executed:**
1. Population: Stage-3 p2 truth events, configuration BM, template half (tt_split = 0), in_eta25; one Λ point per
   species-mass, **as executed the lexicographically first p2 key** (`L0.35`, not `L0.3`; harmless: the generator
   kinematics are Λ-independent, identical p_qp across Λ), all 17 species-masses, **200 template events per
   species-mass** (the executed statistical base; the full Stage-2 samples suggested in review R1 were not used, which
   is acceptable for a definition); event weights w. Jets = the 4 stored leading truth jets.
2. pT(QQ̄) = transverse part of p_qp + p_qm. MET_reco = pT(QQ̄) + N(0, σ⊥ = 25 GeV) per component, 40 independent
   smearing replicas per event (seed 20261013).
3. Event weight = w × ε_trig(MET_reco) × preselection, with ε_trig = 0.98 · ½[1 + erf((MET_reco − 200 GeV)/(20 GeV·√2))]
   and the offline preselection of plan §3 on truth jets: MET_reco > 250 GeV, ≥ 1 jet with pT > 100 GeV and |η| < 2.4,
   min Δφ(jet₁₋₄, MET_reco) > 0.5.
4. Per species-mass: the weighted 95 % quantile of |Δφ(MET_reco, pT(QQ̄))|.
5. **δ₉₅ = the maximum over species-masses, rounded up to 0.01 rad.**

Result: per-mass 0.130-0.149 rad, max 0.149 → **0.15 rad**. Script `data/acts_stage4/review_wp1/r1_inputs.py`,
output `r1_inputs.json` (sha256 in A.3; `delta95_summary.delta95_sig25_max_over_species_mass`).
- The σ⊥ = 15/35 GeV values (max 0.089/0.214 rad) are **signal-efficiency systematics** (ε of the Δφ cut). They do not
  move the cut.
- **Not re-tuned** for the barrel-only selection (PC-7): the population is |η_pair| < 2.5 as executed.
- **Barrel-only diagnostic (review WP_RULE R2 C-3):** restricted to |η_pair| < 1 (47-76 events per mass) the maximum
  is 0.1525 (`review_wp2/r2_delta95_barrel_diag.json`), within the statistical noise; not re-tuned (by design), ε(Δφ)
  at A1 covers it.
- **C-1 diagnostic:** δ₉₅ ignores the detector-level error of n₃ (PU hits in the band move the axis). ε(Δφ cut) is
  reported at A1/V4-3 as a diagnostic only; no re-tuning (item 9).

### 1.4 F1 variables (plan §2.3; not in the in-job code; computed offline from the §S hit records)

- **h (non-helicity).**
  - Split the candidate hits into ≤ 2 subsets by the sign of the in-plane coordinate along n₂ (a two-cluster split per
    layer).
  - Fit each subset with a helix (a circle in rφ plus a straight line in s-z), under (i) a PV origin and (ii) a free
    origin on the plane.
  - h = the min over the hypotheses of χ²_helix/ndf.
- **o (opening linearity).**
  - Per resolvable layer (IT and PS only; never 2S), the |separation| s_l of the two in-plane clusters along n₂.
  - o = χ²_lin/ndf of s_l = a(r_l − r₀), with a ≥ 0 and r₀ ≤ r_min, using the hit errors.
  - Defined for ≥ 4 resolvable layers with two clusters.
- **[D6, resolved] h and o, frozen definitions (review B-7):**
  - split centre = c (the w_core median of §1.1 item 6); per layer the hits form two clusters by sign(u·n₂ − c);
  - h: each of the ≤ 2 subsets is fitted with a helix; for hypothesis H ∈ {PV origin, n_par = 3 (κ, φ₀, tan λ); free
    origin on the plane, n_par = 5}: χ²_H = Σ_subsets χ²_s, ndf_H = Σ_subsets (2 n_s − n_par); **h = min_H χ²_H/ndf_H**;
  - o: ndf = n_layers − 2 (resolvable layers with two clusters), a ≥ 0 and r₀ ≤ r_min enforced as bounds;
  - **undefined passes:** ndf_H ≤ 0 for both hypotheses, a subset with < 3 hits, or < 4 resolvable two-cluster layers →
    the h (resp. o) rungs pass. No rejection is credited for an undefined value.
- **SR-T / SR-G [D7, resolved; F-4 definition frozen; review B-5].**
  - **In-band BTL hit:** a BTL hit with |n·u| < 3σ_tot (σ_n from the BTL local errors projected on n, ⊕ t_tol), |u·n₂| <
    W_c and u·n₃ > 0, about the candidate's final plane, axis and PV.
  - SR-T: ≥ 1 in-band BTL hit with Δt ∈ [t_min, Δt_acc]. Δt = t_BTL − t_PV − |u|/c of the **earliest** in-band BTL hit.
  - σ_t = 35 ps (60 ps variation); Δt_acc = 25 ns (12.5 ns variation).
  - **Out-of-time overlay:** BTL hits of independent PU-200 events shifted by k × 25 ns, k ∈ {−12, …, +3} (the TDR
    readout window: 12 previous and 3 following crossings), each with its per-crossing BTL time spread.
  - **t_min** = the smallest delay at which the per-hit late rate (in-band BTL hits of B1 loose candidates, in-time
    spectrum ⊕ overlay) falls below 10⁻⁴; fixed from PU-only B1 + overlay only (§2.5 item 7), before any signal ε.
  - SR-G = everything else.
  - **In-job first factor (implemented and q = 1-validated in fix R2; review WP_RULE R2 B-2; PC-17).**
    `production.process_trial(..., btl=(B, INT_B))` receives ALL BTL measurements of the trial (G1 columns, t in ns)
    with their interaction ids (same scheme as the tracker INT) and computes, for each of the 43 in-job columns r, the
    column **r ∧ BTL-present** (`RUNGS_T` = r + "&BTL"): P̂₁(r ∧ ≥ 1 in-band BTL hit).
    - Band: exactly the in-band definition above (`weights.btl_band`, brute force over all BTL hits, no road
      pre-filter), about the candidate's final plane, axis and PV (fixed under thinning, like every per-subset family).
    - ρ = 1 (every trial): `n_pass_T`, `n_grp_T` (full-set flags ∧ present; per-hit-set groups as §2).
    - ρ > 1: per subset T of the candidate's interactions S, with I_B = the distinct interactions of its in-band BTL hits:
      - counting columns (exact): w_{r∧B} = w_r(S) − (1 − q)^|I_B| · w_r(S ∖ I_B), the DP of §6.3 on the set with the
        hits of the I_B interactions removed (`weights.drop_interactions`);
      - per-subset columns (IS, same draws): the IS weight W is multiplied by f(T) = 1 if T keeps an interaction of
        S ∩ I_B, else 1 − (1 − q)^|I_B ∖ S| (the BTL-only interactions integrated analytically;
        `weights.subset_weights_btl`). Unbiased: E[W f flag_r] = P_q(T passes r ∧ ≥ 1 in-band BTL interaction kept).
      - Stored: `S_uni_T`, `S_ded_T` (group max), `V_uni_T`, run check `meanW_pull_T` (IS mean W·f vs the exact DP
        P(R04 ∧ BTL)); per stored set `w_T`.
    - Per stored candidate (any ρ): `btl_n_band`, `btl_n_int`, `btl_dt0` (Δt of the in-band hit with the smallest raw
      time, with t_PV = 0: the PU-only trial PV carries no time; offline P(late) applies the trial t_PV convention).
    - **Not in-job, by construction:** the time window [t_min, Δt_acc] and the out-of-time overlay. t_min is fixed
      **from** B1 + overlay (above), so it cannot be applied in the jobs that measure it. They enter P(late) only (§6.2
      composition), measured at ρ = 1 on B1 (S2 + S5 BTL hits with INT and t) ⊕ the overlay.
    - `btl=None` leaves every existing output bit-identical and adds no key (validated, `data/acts_stage4/wp_fix2/`).
    - **Gate:** `process_trial` raises for ρ > 1 without `btl=` when `require_btl=True` (kwarg) or `WCfg.require_btl`
      (set to `frozen` by `config_from_frozen`). The G1 runner passes `btl=` and `require_btl=True` for every ρ > 1
      non-development job and refuses ρ > 1 production if `process_trial` lacks `btl=`. G3B2 therefore carries the
      columns as well (it can enter the union, §5.4 item 11).
- **dE/dx [D1, resolved; review B-1, B-2; plan changes PC-8, PC-13, PC-14].**
  - **Hits: the candidate's CORE TBPX hits only**, |u·n₂ − c| ≤ 2.5 w_core (the χ²_core core, §1.1 item 7; per subset
    re-centred in the IS kernel). The in-band estimator is diluted by PU (≈ 13.5 in-band TBPX PU crossings at the
    normalised density vs ≈ 8-12 quirk hits).
  - Per hit dE_corr = dE × r_xy/|u| (straight line from the PV through a barrel sensor).
  - Estimator = the mean of the lowest ⌈0.6 n⌉ values (TRUNC_FRAC = 0.6), in MIP units.
  - **MIP unit (F-2) procedure, frozen:** the **pooled** 0.6-truncated mean of the path-corrected TBPX deposits of **all**
    hits of the V4-9 muon gun (≥ 10⁴ μ, pT uniform 1-10 GeV, η uniform |η| < 2.5, the same Fatras + digitisation +
    surface-slab configuration as PU, same dE convention: Fatras deposit over the full surface slab, e.g. TBPX
    1.124 mm Si-eq, × r_xy/|u|). Pooled = the large-n limit (candidates have 8-40 IT hits, a muon 4). **Value (F-2,
    filled in fix R2): mip_gev = 3.5582·10⁻⁴ GeV** (`frozen_inputs.json` → `mip_gev` = 3.558235445283726·10⁻⁴; source
    `data/acts_stage4/g1/v49/v49.json` → `mip_unit.mip_gev_pooled_truncated`, 19 475 tracks, 54 585 pooled hits; sha256
    of v49.json in A.3). The per-track median (3.924·10⁻⁴, +10 %) is the superseded draft and a diagnostic only. CKF is
    irrelevant for a single muon.
  - **Quirk deposits (signal; B-2):** each quirk hit's dE is a draw of **the same energy-loss model Fatras uses for PU and
    muons** (G1's numpy re-implementation `acts/stage4/code/eloss.py` of the Fatras Bethe-Bloch Landau model over the same Fatras surface slab: full
    surface material with path correction, at the hit's βγ from `h_E` and its path). Seeds = hash(row, Λ, hit), so the
    draws are identical across rungs. `h_dE` (mean Bethe loss over the 0.15 mm active Si, no fluctuation) stays the truth
    record that V4-1 checks; it is **not** the measurement deposit.
  - **Calibration closure (signal-blind, B-2):** the same numpy sampler applied to the muon-gun truth hits must reproduce
    the Fatras muon-gun pooled unit within 3 %. Otherwise it is a bug, not a tuning knob; no signal job runs until it
    passes. **Result (G1, v49.json):** sampler/Fatras = 0.99955 (pooled) → PASS; per-kind KS p = 0.29-0.58.
  - Top-up crossings carry dE (and t) resampled from the same sensor's Fatras hits [D9, accepted (C-5)]; optional
    variation: resample from low-p hits only, inside the density σ_ln.
  - 4-bit ToT variation: as plan §2.3.

---

## 2. Distinct hit sets (plan §4.1 step 2: "counted once per distinct passing hit set") [D2, accepted; PC-1]

- **Grouping.** Greedy, in rank order: a candidate joins the first existing group (in creation order) whose leader shares
  ≥ 50 % of min(|H_c|, |H_leader|) in-band hits. Otherwise it founds a group. This is the review-R2 `r2_dupcheck` rule;
  the kernel is `weights.group_sets`.
- **Population.** Grouping runs **over the candidates passing R04** (N_IT2 ≥ 3, N_IP2 ≥ 7, |Δφ| < δ₉₅, |η(n₃)| < η_max),
  identically at every ρ.
- **Counts.**
  - At ρ = 1: N_grp(r) = the number of groups with ≥ 1 member passing r.
  - At ρ > 1: Σ_groups max_members w_r.
- **Rungs R01-R03 and the N_L2 diagnostics** carry candidate (union) counts only. Union counts are also kept at every
  rung.
- **Why, and the plan change.** Exact grouping of the full loose population costs ≈ 150 s per ρ = 2 trial (3·10⁵ sets;
  every hit is shared by ≈ 900 sets) and ≈ 4 s per ρ = 1 trial. That is unaffordable under the cap
  (`PHASE_A_REPORT.md` §2). Over the R04 population it costs ≈ 1 s per ρ = 2 trial and ≈ 0 at ρ = 1. Every WP, fallback
  and T1-capable rung lies inside R04. **Plan change proposed:** the per-hit-set convention and the T1/trend tests on it
  apply from R04 on; R01-R03 use union counts at both densities.
- **Governing convention per test (frozen; review B-8).**
  - **Per-hit-set is governing** for B, T1, T1w, T1e, the T3 conditionals at rungs ≥ R04, and the trend test, which is
    run over the rungs ≥ R04 with ≥ 10 B1 counts.
  - Union counts (all rungs) are **diagnostics only**.
  - The **T1 lever arm** is computed in one convention: ⟨S_ded⟩/⟨N_grp(ρ = 2)⟩ (per-hit-set numerator and denominator).
    Mixing S_ded with the union N_pass would overstate the lever arm by the ×3.4-4.6 dedup factor.
  - At ρ = 2, sets failing R04 have w_R04 = 0 exactly (counts are monotone under thinning), so nothing is lost by
    grouping only the R04 population.

---

## 3. The ladder (plan §2.5 item 3): 23 rungs per category, in this order

Each rung tightens exactly one threshold of the previous rung. The fixed cuts of §1.2 (incl. |η(n₃)| < 1.0) apply at
every rung. **Barrel only** (PC-7): there is no endcap ladder in this rule.

| rung | family | requirement added | threshold |
|---|---|---|---|
| R01 | F0 counting | N_IT2 ≥ 3 and N_IP2 ≥ 4 | — |
| R02 | F0 counting | N_IP2 ≥ 5 | |
| R03 | F0 counting | N_IP2 ≥ 6 | |
| R04 | F0 counting | N_IP2 ≥ 7 | (7 = all IT + PS barrel layers) |
| R05 | F0 width | w_core < 37.5 mm | W_c/2¹ |
| R06 | F0 width | w_core < 18.75 mm | W_c/2² |
| R07 | F0 width | w_core < 9.4 mm | W_c/2³ |
| R08 | F0 width | w_core < 4.7 mm | W_c/2⁴ |
| R09 | F0 core χ² | p(χ²_core) > 10⁻³ | |
| R10 | F0 core χ² | p(χ²_core) > 0.01 | |
| R11 | F0 core χ² | p(χ²_core) > 0.05 | |
| R12 | F0 2S | N_2S2 ≥ 1 | |
| R13 | F0 2S | N_2S2 ≥ 2 | |
| R14 | F0 2S | N_2S2 ≥ 3 | (= full F0) |
| R15-R17 | F1 helix | h > h_min | h_min ∈ {2, 3, 5} |
| R18-R20 | F1 opening | o > o_min (χ²_lin/ndf) | o_min ∈ {2, 3, 5} |
| R21-R23 | F1 dE/dx | dE/dx > e_min | e_min ∈ {1.3, 1.6, 2.0} MIP |

- **Categories.** SR-T and SR-G each walk **their own copy** of this ladder. SR-T requires the time tag at every rung.
- **B per rung.** B_c(r) is the total over all sources in category c.
- **Ordering principle (background only).** Counting rungs first (counts only: the base of the exact thinning and of T1),
  then width, core χ², 2S (2S last: P(≥ 2) ≈ 0.98 on TB2S L1), and F1 last in its R1 order.
- **Not adopted:** narrow/wide width categories.
- **Signal information used (disclosed, plan §2.5 item 3).** Review R2's `r2_corewidth.json` prompted the width family.
  Those probe rows are excluded from the template efficiencies (§5.4 item 10).

---

## 4. Background budget, B₈₄ and the zero-count rule

### 4.1 The B sum (plan §2.5 item 4; §4.2 "Full B sum")

B(r) = B_PU + B_SM,prompt + B_conv + B_V0 + B_NI + B_DIF + B_corr(k = 1 guns) + B_cosmic + B_halo, i.e.

**B = N_trig × [P_PU + P_SM,HS + Σ_t rate_t × P(pass | t)] + B_cosmic + B_halo**, with t ∈ {conversion, V0, NI(r_NI),
DIF, PV pair, looper}.

- rate_t is per triggered event in the road, from Pythia at generator level. P(pass | t) comes from the guns and toys.
- For NI and DIF: P(pass at r | t) = f_pre,t × P(pass at r | preselected t, PU).
- **B_NI** = Σ_{r_NI} (NIs per event at r_NI) × P_PV-line × P(pass | r_NI) × N_trig.
  - P_PV-line ≈ 0.22 is a conservative upper value (≈ ×15-35 above the per-NI fraction 0.006-0.014). It is varied with
    the PV-line tolerance in the NI σ_ln.
- **B_DIF** takes no PV-line factor (factor 1, conservative).
- **Counting once.**
  - B1 candidates whose in-band hits come from one interaction (k = 1) are assigned to B_PU. The gun terms cover only the
    hard-scatter and PV-vertex topologies.
  - In the SM samples, candidates with ≥ 1 hard-scatter in-band hit go to B_SM,HS. Pure-PU candidates belong to B_PU.
- **Missing samples** (tt̄ 2ℓ, single top, VV) enter N_trig only.
- **Normalisation.** Pythia σ × K-factor (NNLO/LO ≈ 1.2-1.4, to be cited) with a ±30 % nuisance.

**Log-normal terms.** Each term has a central value and a log-normal σ_ln:

σ_ln² = stat² + (extrapolation-model spread)² + (density normalisation)² + (normalisation)².

**Density-normalisation term of B_PU (review B-9; PC-11).** Per-set ρ = 2 weights are not stored (§S), so the plan's
"re-run the thinning with the top-up at its lower/upper ratio" has no in-job path. Frozen alternative (review option b):
- a **direct ρ = 1 re-run on the S6 dumps** (the first 2 000 C1 B1 events, pre-top-up chain output, × 4 roads) with the
  top-up regenerated from the job seed at its lower and at its upper value (plan §1.4, §4.1 step 5); ≈ 2 × 9 CPU-h,
  run in C1 after the B1 jobs;
- σ_ln,dens(r) = max(|ln(P_up/P_nom)|, |ln(P_low/P_nom)|) at r if r has ≥ 10 counts in all three runs (per-hit-set
  counts, the same 2 000 events at nominal); for every deeper rung, the value at the deepest rung with ≥ 10 counts;
- the same per-hit-set convention (§2) and the frozen finder config. Option (a) (in-job columns with interaction-type
  dependent q) is not implemented; it may replace (b) only by a logged change before the B2 jobs.
- **Cost and scheduling (review WP_RULE R2 C-7):** ≈ 18 CPU-h (2 000 events × 4 roads × 2 variations × ≈ 4 s per ρ = 1
  trial at δ₉₅ = 0.15), **in addition to** the C1 estimate (96-109 → ≈ 114-127 CPU-h, still inside one Mac day), ≈ +2.6 h
  wall at 7 workers; it moves the D4-16 "C2 ends by Thu 22:00" condition by that much. Runner: job kind `dens`
  (`run_stage4.DENS_BLOCKS['C1']`, G1), run after the B1 jobs that write S6; TT level only (no Fatras/CKF re-run).

- Every term is a product of measured factors. Each factor follows §4.2.
- B(r) is the Monte-Carlo sum of the log-normals.
- **B₈₄(r) = its 84th percentile** ("+1σ" in log space).

### 4.2 Zero- and low-count rule (plan §2.5 item 4a; applies to every factor of every B term: B1/B2 rung factorisation, C′₀ and C′_PU factors, NI/DIF preselection fractions, SM samples C)

- **Measuring population.** Each conditional p_j is measured on the tightest population of that sample with **M_j ≥ 10**.
  - The §6.4 factorisation/independence test covers that substitution (its c multiplies if c > 1 at 2σ).
  - c is evaluated among the term's non-zero factors only. A term in the zero branch carries the largest c measured among
    its other factors (c = 1 if none), and is flagged.
  - A pass fraction at a loose rung is a direct count.
- **N_j ≥ 1:** the central value is N_j/M_j, with σ_ln,stat from the event bootstrap (never below 1/√N_j).
- **N_j = 0:**
  - **Among the term's zero factors, the one with the largest M_j** (ties: the first along the ladder order) enters at
    **1.14/M_j** (the one-sided 68 % CL Poisson bound) with **σ_ln = 1.0**. So its 84th percentile is 3.1/M_j.
  - It is the term's only bounded factor; measured non-zero conditionals still multiply.
  - Every other zero factor of that term enters as 1.
  - A zero never enters as 0. A bound enters at most once per term.
- **Reporting.** A term using the zero branch is flagged in the B table. If it makes B₈₄,c(r) > 0.11 at every rung of c,
  item 6 applies (the §8 fallback, or the pre-declared, user-approved +50 % steps). No other remedy.

---

## 5. Working point per category (plan §2.5 items 5-11)

### 5.1 Per-category rung (item 5)

For c ∈ {T, G}: **r*_c = the loosest rung with B₈₄,c(r) ≤ 0.11 events in 3 ab⁻¹, for r*_c and for every tighter rung**
of that category.

- Why 0.11: two independent categories at σ_ln = 2.3 combine at ×2.71 the per-category B₈₄, and 0.3/2.71 = 0.11.
- This is a convention from log-normal algebra alone, with no signal input. It is not optimised.

### 5.2 Combined guard and continuation (item 5)

- **Combined guard (both categories have a WP).** The combined B₈₄ of B_T(r_T) + B_G(r_G) is computed by Monte Carlo
  over the log-normals. Shared sources (density normalisation, extrapolation model, K-factor) are fully correlated
  between the categories.
  - A pair (r_T, r_G) is **accepted** iff the combined B₈₄ ≤ 0.3 for it **and for every component-wise tighter pair**.
  - Start at (r*_T, r*_G).
- **Deterministic continuation.**
  - If the pair is not accepted, move the category with the larger B₈₄,c one rung tighter (tie: SR-G). A category at
    R = 23 stays there and the other one moves.
  - Stop at the first accepted pair. At most 2(R − 1) = 44 steps.
- **(R, R) reached and not accepted:** neither category has a background-free WP; both are reported under the §8
  fallback.
- **Exactly one category has a WP:** the combined check is not applied.
  - The background-free claim (B₈₄ ≤ 0.11 ≤ 0.3) is made for that category alone; the other is reported under §8.
  - The Stage-5 likelihood stays two-bin, each bin at its own pre-declared selection with its own log-normal B.
  - The 3-event discovery statement is made only for the background-free category.
- The planning split 0.1 PU + 0.1 SM + 0.1 rare is used only to size samples. It is **not** part of the rule.

### 5.3 No working point (item 6)

If no rung of category c satisfies §5.1, c has no WP and is reported with the §8 fallback, pre-defined. The user is told,
with these options: more B1/B2 statistics (later pre-defined campaigns, or the +50 % steps, each a ≲ 1-day user-approved
run), or accept the fallback. **No re-ordering of the ladder and no new rung after the freeze.**

### 5.4 Remaining items (verbatim content)

- **Item 1.** The selection shape (§1, §3) is fixed before any production. There is no fixed Δw cut.
- **Item 7.** t_min and the in-time window come from the PU-only BTL spectrum (B1) and the out-of-time overlay only.
- **Item 8.** Signal **templates** are used only to report efficiencies and edges at the WP that the rule fixes. Signal
  **toys** are used only for the P2 pseudo-experiments.
- **Item 9.** This file is frozen at the start of G2, before V4-3/A1 (the first signal efficiencies).
  - Any later finder change (a bug fix, a CPU optimisation) is logged with its reason, re-run on B1/B2 and re-reviewed.
  - Such a change may not use signal efficiencies as input.
- **Item 10. Probe rows excluded** from the template efficiencies:
  - E1000 chunk c00 event indices 7, 8, 15, 16, 24, 26, 39, 42 at 0.6/1/3 keV;
  - the fix-R1 rows of chunk c01 in `data/acts_stage4/fix_r1/f1r_summary.json` → `sig_t0.<point>.rows`.
- **Item 11.** The rule is applied to the union of all background samples produced so far.
  - **G3 (review C-3):** the G3 pilot (own seed prefix) enters the union **only if produced with the frozen code hashes
    (A.3)**. The G3 branch governs the residual; the union T1/trend are reported, and an anti-conservative union result
    still triggers its branch.
  - After C1 the result is labelled *preliminary (C1 statistics)*.
  - The reported r*_c is the one on the union of all campaigns run.
  - A further campaign is decided by the user on cost, background reach and closure, **never on signal yields or
    efficiencies**.

---

## 6. PU-only fake rate: extrapolation per rung family and closure tests (plan §4.1)

### 6.1 Samples and estimators

- **B1 (direct, ρ = 1).** Fresh PU-200 events: Poisson(200) interactions, the TDR top-up (§1.4) and a new PV per event.
  - K = 4 MET roads at φ₀ + kπ/2.
  - **The per-trial rate (the mean over the 4 roads of the per-road pass indicator) is the primary P_fake.** The ≥ 1-of-4
    rate is a diagnostic.
  - Errors and n_eff come from the event-level bootstrap.
- **B2 (density ladder, ρ = 2).** Superpositions of 2 independent normalised PU-200 events (own top-up each), 2 roads.
  - For each candidate found at ρ with interaction set S, and each rung r:
    **w_r = Σ_{T ⊆ S passes r} q^{|T|}(1 − q)^{|S|−|T|}**, q = 1/ρ, with the ρ-level plane and axis fixed.
  - **P̂₁(r) = ⟨Σ_sets w_r⟩_trials** (union bound, conservative). Each top-up crossing is its own interaction.
  - There is no fitted exponent. The power law A_r ρ^{α_r} is only the alternative model in the spread.
- **Reach.** A k_min = 20 candidate at ρ = 2 probes ⟨Σw⟩ ≈ 10⁻⁶/(2 N_ρ2) per trial: ≈ 5·10⁻¹⁰ (C1), 1.6·10⁻¹⁰ (after
  C2).
  - A rung is "reachable at ρ" if ≥ 10 candidates at density ρ pass it.
  - If the WP rung is not reachable at ρ = 2, P at the WP comes from rung factorisation (§6.2 step 3) from the deepest
    reachable rung, with T3.
  - ρ = 3 (C5) is offered only if T3 fails, and is deferred under the deadline.

### 6.2 Method per rung family (plan §4.1 step 3b table)

| family | how P₁(r) is obtained | closure test |
|---|---|---|
| counting N_IT2, N_IP2 (R01-R04) | per-subset recomputation from per-interaction (layer, side) counts — **exact** (§6.3) | T1 (ρ = 2 → 1), T2 (only if C5) |
| w_core, χ²_core, and the 2S rungs after them (R05-R14) | per-subset recomputation, plane and axis fixed; per subset c(T), w_core(T) from T's IT + PS hits; **core re-centred per subset**; χ²_core(T) summed per hit; importance sampling conditional on R04 (N_IP2 ≥ 7); hit re-collection after a refit ignored (covered by T1w) | **T1w**: T1 statistic and lever-arm rule at the tightest width or χ²_core rung with ≥ 10 B1 counts |
| dE/dx (R21-R23 with the F0 part) | per-subset recomputation of the truncated mean of T's **core** IT hits (§1.4) | T1e at the first dE/dx rung if it has ≥ 10 B1 counts, else T3 |
| h, o (R15-R20) | **factorisation**: P₁(F1 rung \| last F0 rung) measured directly at ρ = 1 on B1 × P₁(last F0 rung) from the rows above. Independence tested in 3 bins of road-hit count and at the two tightest F0 rungs reachable in B1; a correlation factor c (the max ratio over bins) multiplies if c > 1 at 2σ. Check: per-subset recomputation of h, o on 200 random ρ = 2 sets | T3 + the density-bin test + **T3s** (factorised vs recomputed on the 200 sets, \|z\| < 2) |
| SR-T time tag | factorisation P̂₁(r ∧ BTL-present) × P(late); the first factor by per-subset recomputation (BTL hits carry an interaction id; in-job columns `RUNGS_T`, implemented fix R2, §1.4: exact for the counting rungs, IS × f(T) for the per-subset rungs); the late fraction includes the out-of-time overlay | time-independence test (late fraction in bins of N_IP2, w_core, χ²_core, density) |

**Rung factorisation (step 3).** P(r+1) = P(r) × p_{r→r+1}, measured on the candidates passing r. Below the deepest
rung with ≥ 10 counts, each conditional is measured on the tightest population with ≥ 10 entries. Zero counts follow
§4.2.

**Composition of the factorised families with the in-job columns (frozen; review B-7).** The in-job columns are
R01-R14, F0 ∧ e and FB_k[∧ e]; the ladder order is …R14 → h → o → e. Then:
- P₁(R15-R20) = P̂₁(R14) × p(h/o rung | R14);
- P₁(R21-R23) = P̂₁(R14 ∧ e_x) × p(h > 5 ∧ o > 5 | R14 ∧ e_x), with e_x the rung's dE/dx level (column F0e>x);
- P₁(r_fb) = P̂₁(FB_k[∧ e]) × p(h > 5 ∧ o > 5 | FB_k[∧ e]);
- SR-T: P̂₁(r ∧ BTL-present) × P(late) **+ P̂₁(r ∧ ¬BTL-present) × P_oot(late)** (PC-18). The second term covers a
  candidate with no in-time in-band BTL hit whose earliest in-band hit comes from the out-of-time overlay and lands in
  [t_min, Δt_acc]. P̂₁(r ∧ ¬BTL-present) = full column − BTL-present column (both in-job); P_oot(late) is measured from
  the out-of-time overlay alone on the B1 trials, by the same rule as P(late). The term only adds background
  (conservative); it enters the same B₈₄ sum and the same zero-count rule.

Each conditional p is measured at ρ = 1 on B1 (S4 hit records) on the tightest population with M ≥ 10 (§4.2), and the
c-test (§6.4) applies. f_CKF enters no B_PU factor (§1.2).

### 6.3 In-job ρ = 2 weights as implemented (Phase A; `acts/stage4/finder/weights.py`, `production.py`)

- **Counting rungs: exact.** Single-layer interactions act independently per layer. The layer state is
  (min(n_in, 2), min(n_out, 2)), 9 states, handled by a DP per layer.
  - The multi-layer interactions (M ≤ 12 measured) are enumerated exactly (2^M configurations).
  - The joint law of (N_IT2, N_PS2, N_2S2) is the Poisson-binomial of the layer outcomes.
  - Validated against plain MC (2·10⁴ subsets) on 1 280 ρ = 2 sets: per-set pulls rms 0.98-1.05 on all 13 counting
    columns; summed-weight pulls |z| ≤ 1.3. Validated also against f1r `thin_weights` (`data/acts_stage4/g2b/weights_validation.json`).
  - Cost 4 µs per set (the MC costs 12 ms).
- **Per-subset families: importance sampling conditional on N_IP2 ≥ 7.**
  - Multi-layer interactions are drawn ~ Bernoulli(q). The IP-layer single-layer interactions are drawn exactly
    conditional on ≥ 2 crossings per IP layer (backward success tables). The 2S single-layer interactions are drawn
    ~ Bernoulli(q).
  - IS weight W = Π_IP p_l(base). Unbiased: E[W f] = E_q[1{N_IP2 ≥ 7} f].
  - **nsub = 64 subsets per set.**
  - Validated: q = 1 reproduces the full-set flags of 2 000 sets exactly; the IS sums agree with plain MC within errors;
    mean W agrees with the exact DP P(N_IP2 ≥ 7).
- **Sub-sampling fractions (plan §4.1 step 3b, fixed at G2b from PU-only timing).** **f_lo = f_hi = 1: no set is
  sub-sampled.**
  - G2b passed at the full in-job cost (t₂ = 35.0 s mean ≤ t₂,max = 66 s for C1 → C2; `PHASE_A_REPORT.md` §3).
  - The plan applies the strata only if G2b fails. The group-level machinery (`WCfg.f_is`) is kept but is not used.
  - Every R04 set is IS-weighted, so hit-record sample (a) is always weighted.
- **Columns computed in-job (43):**
  - R01-R14;
  - F0 × dE/dx for e ∈ {1.3, 1.6, 2.0};
  - FB0-FB4 and FB_k × dE/dx (§8);
  - the N_L2 ≥ 5…10 diagnostics.

  h, o and P(late) are not in-job (factorised at ρ = 1, §6.2). The SR-T first factor is in-job: **43 further columns
  r ∧ BTL-present** (`RUNGS_T`, with `btl=`; §1.4, fix R2). Validated (`data/acts_stage4/wp_fix2/btl_validation.json`,
  PU-only interim trials with the interim Fatras BTL hits): see `review/FIX_WP_RULE_R2.md`.
- **dE/dx columns use core IT hits** (§1.4) in both `weights.subset_weights` (per subset, re-centred core) and
  `production.dedx_sets` (full set). Validated (fix R1, `data/acts_stage4/wp_fix1/`): q = 1 kernel flags = full-set flags
  on 2 000 PU sets for all 33 IS columns (0 mismatches; `weights_validation.json` V-c) and, with synthetic Landau deposits
  and the width/χ² thresholds opened, on 300 sets for all 18 dE/dx columns (0 mismatches, 189/55/1 sets passing
  e > 1.3/1.6/2.0; `dedx_check2.json`); non-dE/dx columns, N_grp, S_uni, S_ded bit-identical to the pre-fix code at
  δ₉₅ = 0.25 with the η cut off (`regress_smoke.json`).
- **Per-trial run check (review C-7):** `row.meanW_pull` = (Σ mean W − Σ DP P(N_IP2 ≥ 7))/IS error; |pull| < 3 expected;
  a trial with |pull| ≥ 3 is flagged and reported (smoke: 0.63, 1.59). Same for the SR-T columns: `row.meanW_pull_T`
  (Σ mean W·f vs Σ DP P(R04 ∧ BTL); fix R2 smoke 1.63).
- **C-4 diagnostic (G3):** S_ded takes the max over group members of noisy IS means (biased upward, conservative); at G3
  re-run a subsample with nsub = 256 and report the shift.

### 6.4 Closure and factorisation tests (plan §4.1 step 4; gate V4-7)

- **T1 (ρ = 2 → 1)** at the tightest rung r₁ with ≥ 10 passing candidates (per-hit-set groups, §2) in B1.
  - **Lever arm:** ⟨S_ded⟩/⟨N_grp(ρ = 2)⟩ ≤ 0.1 (one convention, §2). If not, r₁ moves to the next tighter rung with
    ≥ 10 B1 counts.
  - If no rung has a 1-decade lever arm: use ρ = 3 → 1 if C5 ran. Otherwise use the rung with the largest lever arm and
    treat the missing lever arm as a closure failure of unknown direction (anti-conservative branch, upper envelope).
- **T2 (ρ = 3 → 2)**, only if C5 is produced.
- **T3 (rung factorisation):** predict r₁ from r₁ − 2 on B1 and compare with the direct count.
- **T1w, T1e, T3s:** the per-family tests of §6.2.
- **Statistic:** z = ln(N_obs/N_pred)/√(1/N_obs + σ²_ln,pred), with σ_ln,pred from the event bootstrap. **Pass: |z| < 2.**
- **Trend test.** T1 is evaluated at every rung with ≥ 10 B1 counts.
  - The slope of ln(N_obs/N_pred) vs the rung index must be compatible with 0 at 2σ.
  - If it is not, the slope extrapolated to the WP rung is added to σ_ln, and also to the central value if the trend is
    anti-conservative.
  - Run over the rungs ≥ R04 with ≥ 10 B1 counts, per-hit-set counts (governing). Union counts (all rungs) are
    reported as diagnostics (§2).
- **Factorisation/independence test.** On B1 loose candidates (§S S3 sample): the joint probability of the extra
  requirement in pairs and triples of layers vs the product of the single-layer conditionals, in 3 bins of road-hit
  count. c = joint/product (the max over bins and pairs) multiplies the step-3 estimate if any c > 1 at 2σ. The SR-T
  time-independence test is part of the same gate.
- **Failure paths (no model shopping):**
  - *Anti-conservative (z > +2).* The only remedy is more statistics in a pre-declared step (+50 % B1 or B2, at most
    twice, each a ≲ 1-day user-approved run). If it still fails: B_PU = the **upper envelope** of {thinning, power law,
    factorisation} × N_obs/N_pred of the failed test, with σ_ln enlarged to cover the spread.
  - *Conservative (z < −2).* No extra statistics. B_PU = the thinning value, uncorrected, with |ln(N_obs/N_pred)| added
    in quadrature to σ_ln; the bias is reported.
  - *|z| < 2 with a significant trend:* the trend rule above.
  - In all cases, if the WP becomes infeasible, §8 applies and the user is told.
- **Families pointing in different directions.**
  - Each family's test governs its own rungs: T1 the counting rungs, T1w the width/χ²_core rungs, T1e the dE/dx rungs,
    T3s/T3 the h/o rungs.
  - Corrections compound along the cumulative ladder and are never cancelled against an opposite correction of another
    family.
- **Result (step 5).**
  - P_fake(WP) = the thinning estimate when T1 (and T2) pass, else the failure value.
  - σ_ln combines the bootstrap, the model spread (power law, factorisation) and the density normalisation (the direct
    ρ = 1 S6 re-run of §4.1, PC-11).
- **G3 decides the unexplained ×1.6-1.8 residual** through these branches:
  - |z| < 2 and no trend → nominal;
  - z < −2 → conservative;
  - z > +2 → anti-conservative;
  - |z| < 2 with a trend → the trend rule.

  A cause found later may be cited, but it cannot change the branch already taken without a logged re-review.
- **T_seed stability (G3 (iv); review C-2).** T_seed = 6 is frozen. If at G3 the per-family pass fractions move by
  > 2σ between T_seed = 6 and 4, T_seed(ρ) := 4, the jobs are re-timed (G2b criterion) and the change is logged; this is
  the only pre-declared T_seed action.

---

## 7. SM samples and the C′ guns/toys (plan §4.2)

- **SM samples C** (Z(νν)+j, W(eν/μν/τν)+j, tt̄ 1ℓ; Pythia8 LO, truth MET > 200 GeV, + PU 200).
  - Candidates with ≥ 1 hard-scatter in-band hit belong to B_SM,HS.
  - **Depth comes from rung factorisation only:** start from the deepest rung with ≥ 10 such candidates, measure each
    conditional on the tightest population with ≥ 10, apply the c test, T3 and the T3 failure path, and §4.2.
  - Thinning is at most a k-decomposition diagnostic.
- **C′₀ (no PU).**
  - γ, K⁰_S/Λ, PV-pair, looper guns: 10⁵ each.
  - NI toy: 3 × 10⁴ per r_NI ∈ {22, 30, 61.5} mm. DIF toy: 5 × 10⁴.
  - It measures the topology-only rejection of h, o and dE/dx. The zero-count reach is 1.14/M.
- **C′_PU.** 8 topologies × 500 TDR-normalised PU-200 events, gun/toy aimed into one road.
  - Depth from rung factorisation on C′_PU (from the deepest rung with ≥ 10 counts) and the C′₀ h/o/dE/dx factors.
  - Not from thinning (T1 not applicable).
- **NI/DIF with PU: preselected toy events.**
  - **Overlay (hand-over).** The stored C′₀ simulated toy hits (Fatras SimHits) are **inserted** into the PU event; the
    toy is not re-simulated. Smearing and hit efficiency come from the toy's own seed.
  - **The PV is the same stored smeared PV draw** in both events.
  - **Pre-CKF, pre-merge.** The preselection and the V4-10 hash use **all** stored toy measurements before CKF removal and
    before the U-5 b merging. The attribution tests each toy-linked hit at its stored C′₀ position and σ.
- **Preselection (PU-independent).** Some triple of toy hits in 3 distinct layers, from ≥ 2 distinct toy particles, has
  χ²₃ = λ_min(Σ_h u_h u_hᵀ/σ̂_h²) ≤ 48 about the stored PV. The test is exhaustive over triples.
  - **σ̂_h² = σ²_loc,max,h + t_tol² + (δn_max·|u_h|)²**: σ_loc,max,h is the larger local error (the σ along the strip for
    2S), t_tol = 30 µm, **δn_max = 2 mrad**.
  - Since σ_tot has δn = 0 and σ_n ≤ σ_loc,max, **σ̂_h ≥ σ_tot,h(n) for every candidate**.
- **Attribution.** A with-PU candidate counts for topology t only if:
  - ≥ 3 of its core hits, in ≥ 3 distinct layers (≥ 1 of them IT + PS), come from the gun/toy particles, each within
    ±4σ̂_h of the candidate's PV plane, tested at its stored C′₀ position and σ;
  - and those hits come from ≥ 2 distinct gun/toy particles. For the looper gun instead: ≥ 2 crossings by the looper in
    ≥ 1 layer.
  - A U-5 b merged measurement is tested at each of its toy-linked stored C′₀ positions. Each toy link counts as a hit of
    its own particle only if that link's own stored position passes.
  - The rule is applied identically to the C′₀ candidates.
- **Why f_pre is exact.** Attribution ⇒ a triple with χ²₃ ≤ 48 about the same PV with the same σ̂_h ⇒ preselected. So
  P(pass ∧ not preselected) = 0 for any δn in σ_tot. Hence **P(pass at r | t) = f_pre,t × P(pass at r | preselected t,
  PU)**, with f_pre,t measured on the full C′₀ sample with its own Poisson σ_ln.
- **V4-10 (necessity check, zero cost).** Per NI/DIF topology on the full C′₀ sample: attributed candidates (any rung)
  in **non-preselected** events **= 0 exactly**, reported with f_pre. The with-PU toy measurements (pre-CKF, pre-merge)
  and the PV must equal the stored C′₀ ones (per-event hash).
  - Failure is a bug: that topology's C′_PU is not run or not used until it is fixed and re-checked.
  - If it cannot be fixed inside C1: the weight becomes f_pre × (1 + N_leak/N_attr,pre), |ln(1 + N_leak/N_attr,pre)| is
    added to σ_ln, the term is flagged and the user is told. No other remedy.
- **Sampling.**
  - N_pre ≥ 500: the first 500 by event index are overlaid.
  - N_pre < 500: each preselected event is overlaid ⌈500/N_pre⌉ times, with a two-level bootstrap.
  - N_pre = 0: f_pre follows §4.2, the conditional is set to 1, and that topology's 500 with-PU events are not run.
- **Low gun counts.** A gun topology with < 10 passes in 500 at the loosest counting rung starts its depth from the C′₀
  factors under §4.2.

---

## 8. Fallback deliverable (plan §2.6; D4-17 (i) approved 2026-10-13)

- **Width admissibility.**
  - **k_adm(m, Λ) = the largest k ∈ {0, …, 4} with Λ ≥ Λ_R(m)·2^{(k+1)/2}**; k = 0 means no width cut.
  - Λ_R(m) is the **smoothed** value from `sim/stage3/results/P2.json` → `edge_fits_in_m`: `F/lower_lmax_RIT_closed`
    `deg2` for E, `S/lower_lmax_RIT_closed` `deg1` for Ẽ.
  - P2.json sha256 `e63d19d8…2459` (A.3). Values in Appendix A.1.
- **dE/dx admissibility (dilution-aware; review B-1; PC-9).** **e_adm(m, Λ) = the largest e_min ∈ {1.3, 1.6, 2.0} MIP
  with e_min ≤ R_eff(m, Λ)/1.25**, else none. R_eff is the median of the production estimator (§1.4: core TBPX hits,
  lowest 60 %, pooled-MIP unit) in a **frozen mixture model** (`acts/stage4/finder/eadm_dilution.py` →
  `data/acts_stage4/frozen/eadm_dilution.json`, sha256 in A.3; table A.2b):
  - quirk hits: n_q(m, Λ) = the median number of truth TBPX quirk hits (both quirks) over the point's fiducial events
    (template half, in_eta25, status 1, |η_pair| < η_max = 1.0), all in the core, each with loss ratio R(βγ_IT(m, Λ))
    (below);
  - PU hits in the core: Poisson with mean Σ_l μ_c,l × min(1, 2·2.5·W_k/X_l): μ_c,l = 8, 3, 1.5, 1.0 (plan §2.1,
    TDR-normalised in-band TBPX L1-L4 crossings), X_l = min(2W_c, 2r_l) = 60, 123, 150, 150 mm, W_k = W_c/2^k at
    k = k_adm(m, Λ) (the worst case for that width rung); k_adm = 0 → the full band;
  - per-hit loss: Moyal(loc = R_hit, scale = 0.12 R_hit) in MIP units (thin-Si Landau proxy; R_hit = 1 for PU); the
    unit is the same estimator on a pooled large-n MIP sample; 4 000 toys per point, seed 20261013;
  - **PU-density update (pre-declared, PU-only; trigger tightened in fix R2, review WP_RULE R2 C-5):**
    - statistic: ρ_dens = Σ_l μ_c,l · (N̄_l(B1) / N_l(plan)) / Σ_l μ_c,l over TBPX L1-L4, with N̄_l(B1) the mean number
      of Fatras (pre-top-up, pre-CKF-removal) measurements on TBPX layer l per PU-200 event in the S6 dumps (the first
      2 000 C1 B1 events) and N_l(plan) = 6686, 4901, 3564, 2811 (plan §2.1 table). The top-up multiplies each layer
      by the frozen TDR ratio, so this ratio is the in-band crossing-density ratio that scales μ_c;
    - trigger: **ρ_dens > 1.05** → the script is re-run unchanged with μ_c × ρ_dens, and the new table and hash
      replace A.2b before any signal efficiency at the fallback is computed;
    - margin below the trigger: at μ_c × 1.1 the R_eff drop is ≤ 5.5 % and 7 cells lose a level
      (`data/acts_stage4/wp_fix2/eadm_mu_1p1_summary.json`; × 1.2: ≤ 10 %, 10 cells); at × 1.05 the drop is ≤ 3.5 % and
      3 cells (F_m1300, Λ = 5-10: 1.6 → 1.3) lose a level (`eadm_mu_1p05_summary.json`). Below the trigger the drop is
      thus smaller than the smallest measured conservatism of the proxy w.r.t. the Fatras model (R_eff 4.5-10 % higher,
      below); the closest cell margin to a level is 0.5 % (F_m1300, Λ = 10).
  - Result: dE/dx is admissible only where k_adm = 4 (w_core < 4.7 mm) at heavy masses: 1.3 at E900-E1200 and Ẽ1000,
    1.6 at E1300-E1500 (all at Λ ≥ 5 keV, Ẽ1000 at Λ ≥ 7 keV). Everywhere else none. The undiluted R/1.25 table
    (`e_adm_undiluted`) is kept for reference only.
  - **Conservative w.r.t. the Fatras model (diagnostic, not an input):** the same mixture with G1's Fatras-model sampler
    (`code/eloss.py`, TBPX slab; the CERNLIB-Landau mapping of G1, not `scipy.stats.landau`) gives R_eff higher by
    4.5-10 % at six k_adm = 4 points; the level changes only at E1200 (1.3 → 1.6). The proxy table is the frozen one
    (`data/acts_stage4/wp_fix1/eadm_fatras_sensitivity.json`, re-run identical in fix R2 with the final `eloss.py`).
    The frozen model itself samples only a Moyal proxy (`scipy.stats.moyal`), never `scipy.stats.landau`.
  - **Model assumptions (review WP_RULE R2 C-4):** (i) all n_q quirk hits are taken in the core; for an asymmetric
    two-cluster ribbon the MAD core can shrink to the majority cluster, but then the PU in the core is also far below
    the W_k bound, so the net direction is not signed; (ii) n_q is selected on |η_pair| < 1 while the cut is on η(n₃)
    (minor mismatch).
  - **βγ_IT(m, Λ) = max(βγ_IT(m), per-point median at Λ).**
  - βγ_IT(m): Stage-3 p2 truth, BM, template half (tt_split = 0), in_eta25 ∧ status = 1; per event the median of |p|/m
    over the IT hits (both quirks); per point the median over events; per species-mass the median over all p2 Λ points.
  - Script `probes/f4r_admissibility.py`, output `fix_r4/f4r_admissibility.json`. Values and hashes are in Appendix A.2
    and A.3.
  - The plan re-runs the script unchanged at the freeze; its output must reproduce the A.3 hash.
- **R, the restricted-loss ratio** (input to R_eff).
  - R = the restricted energy loss in Si (PDG restricted-loss formula, T_cut = 100 keV, PDG 2024 Si density-effect
    parameters: I = 173.0 eV, a = 0.1492, k = 3.2546, x₀ = 0.2015, x₁ = 2.8716, C̄ = 4.4355, δ₀ = 0.14) of the quirk at
    βγ_IT, divided by the same quantity for the calibration muon gun at its median βγ.
  - 1.25 is the pre-declared Landau / truncated-mean margin.
  - **F-3 frozen: βγ_μ = 92**, the median βγ of the V4-9 gun definition (pT uniform 1-10 GeV, η uniform |η| < 2.5;
    generator level, `review_wp1/r1_inputs.json` → `muon_gun`). The G1 gun config must use this pT/η shape. The
    undiluted level is unchanged for βγ_μ ∈ [30, 300] at the median βγ_IT.
- **The other families** (counting, χ²_core, 2S, h, o, SR-T) are admissible everywhere.
- **Fallback selection.** r_fb(m, Λ, c) = N_IT2 ≥ 3 ∧ N_IP2 ≥ 7 ∧ p(χ²_core) > 0.05 ∧ N_2S2 ≥ 3 ∧ (w_core < W_{k_adm}
  if k_adm ≥ 1) ∧ h > 5 ∧ o > 5 ∧ (dE/dx > e_adm if any), plus the time tag for c = T.
  - With the dilution-aware e_adm, the dE/dx term appears only with k_adm = 4 (FB4 ∧ e ∈ {1.3, 1.6}). At most 20 distinct
    selections (FB0-FB4 × {no dE/dx, 1.3, 1.6, 2.0}). R_E is one of them.
  - Their in-job weights are the FB columns of §6.3. h, o are factorised; SR-T as in §6.2.
- **Primary result per (m, Λ, c):**
  - r*_c, if it exists and is admissible (its width level ≤ k_adm and its dE/dx level ≤ e_adm);
  - otherwise **r_fb(m, Λ, c)**, with non-zero, log-normal B;
  - *mixed admissibility:* the pair (r*_c, r_fb,c′); the "exactly one category" branch of §5.2 applies at that point.
- **Per-point best-of is forbidden.** No comparison of ε, yields or limits between selections enters any reported result.
- **Both are reported wherever both exist** (plan §2.6; review C-9): where r*_c exists, its ε/B table and the r_fb
  table are both reported; only the primary carries the limit.
- **Deliverables.**
  - ε and B (central value, σ_ln, B₈₄) per category at r_fb and at R_A (end of counting, N_IP2 ≥ 7), R_B (R_A + w_core
    < 18.75 mm), R_C (R_A + w_core < 4.7 mm), R_D (full F0) and R_E (full F1). These are tables of ε and B only; **no
    limit at R_A-R_E**.
  - **One Stage-5 expected 95 % CL limit per (m, Λ), only at the primary selection.** Two-bin pyhf counting likelihood,
    B as a log-normal nuisance → `results/fallback_limits.json`. The D4-13 outputs use the same primaries.
  - The Fatras-density and truth-level results are kept only as labelled optimistic bounds.
- **What it can and cannot claim:** as plan §2.6. Not optimality, no 3-event discovery reach where B₈₄ > 0.3, and
  nothing for ℓ_max > R_IT or the merged regime. **Barrel-only (PC-7):** nothing for pairs with |η_pair| ≥ 1.0 (the
  selection is |η(n₃)| < 1.0); the 1.0-1.3 transition region and the endcap (|η_pair| > 1.3) are outside the analysis;
  ε carries the fiducial loss explicitly (69 % of counting-set events have |η_pair| > 1). Endcap and (L3, L2, L1) seed
  families are documented future work.

---

## 9. Campaigns (plan §6.2) and the user's choice

| campaign | content |
|---|---|
| **C1** | A1 (all, no PU); A2 on E200/500/1000/1500 + Ẽ500 × Λ ∈ {0.45, 0.6, 0.85, 1.0, 1.5, 2.0, 3.0, 5.0} keV, 200 events each (8 000, 1 000 rows); A5 on 5 points (1 000 events, full chain); B1 5 000 × 4 roads; B2 1 000 ρ = 2 × 2 roads; C Z(νν)+j, W(τν)+j, tt̄ 1ℓ × 2 000; C′₀ (≈ 12 CPU-h) and C′_PU (8 × 500); validation 15 CPU-h. Sub-runs C1a = A1, A2, A5, C′; C1b = B1, B2, C |
| **C2** | B1 +7 000 (→ 12 000); B2 +2 000 (→ 3 000); C → all five samples × 5 000 (+19 000); validation 5. Sub-runs C2-B (B1, B2), C2-C (SM) |
| C3 | B1 +8 000 (→ 2·10⁴); B2 +2 000 (→ 5 000) — deferred |
| C4 / **C4′** | the rest of A2 (all 307 points; 53 344 events, 2 400 rows); A3; A4; A5 → 20 points + PU 140. C4′ = C4 without A3 and A4 |
| C5 | ρ = 3, 2 000 events × 1 road; optional, behind G2c, deferred under the deadline |
| C1r | reduced C1 (deadline fallback only) |

- Seed ranges are disjoint across campaigns: `run_stage4.py` uses job seed = blake2b("stage4|sample|chunk"), with chunk
  numbers continuing across campaigns.
- **User decision (D4-16, LOG 2026-10-13 16:12):** C1 → C2, then C4′ only if C2 ends by Thu 2026-10-15 22:00. Each
  campaign ends with a short report, and the user can stop at any time.
- **G3 pilot** (development): B1 2 000 + B2 500, own seed prefix (samples G3B1, G3B2).

---

## §S. Storage policy (Phase A; new; implemented in `production.process_trial` and `run_stage4.pack`)

The aim is to keep everything the closure tests (§6.4), the item-4a populations (§4.2), the fallback selections (§8) and
the offline F1/SR-T computations need, at ≲ 50 GB in total.

**ρ = 1 PU-only trials (B1, G3B1; SM C and C′_PU use the same policy plus their truth tags, defined at G1):**

| id | stored for | content |
|---|---|---|
| S1 | **every trial** | seeds (job, trial), PV, φ_MET, distance to the nearest PU vertex, finder counters, timers; per rung (43 columns, §6.3): N_pass (candidates) and N_grp (distinct-hit-set groups; −1 where §2 defines none); with `btl=` also N_pass_T, N_grp_T (r ∧ BTL-present, §1.4) and n_btl, n_btl_present |
| S2 | every candidate passing **R04** (N_IT2 ≥ 3, N_IP2 ≥ 7, \|Δφ\| < δ₉₅, \|η(n₃)\| < 1.0); ≈ 400-1 300 per trial at the planning δ₉₅ = 0.25 (≈ 300-450 at the frozen 0.15 / 1.0, smoke) | compact record: all stored variables (§1.1), 10 per-layer crossings, p(χ²_core), dE/dx (core), normal, axis, Δφ, η(n₃), n_band, n_CKF,band, f_CKF, seed N_L2, group id, packed per-rung pass flags; with `btl=`: btl_n_band, btl_n_int, btl_dt0 (§1.4) |
| S3 | a **1 % Bernoulli sample of all loose (R01) candidates** | the same compact record (for the loose-candidate factorisation/independence test, §6.4) |
| S4 | every candidate passing **R04 ∧ (w_core < 37.5 mm ∨ p(χ²_core) > 10⁻³)** | **full hit records**: per in-band hit xyz, surface, σ (2), dE, interaction id, particle, generation, time (CSR into a per-trial union hit table) |
| S5 | every event | all BTL hits (surface, xyz, σ, dE, t, interaction id): SR-T offline |
| S6 | the first 2 000 C1 B1 events | the chain output before the top-up (barrel counting + BTL surfaces, typed columns), plan §4.1 step 1 / critical C-10. The top-up is regenerated from the job seed |

**Why the S4 threshold (and not N_IP2 ≥ 6 or ≥ 7 alone).**
- Every ladder rung beyond R04 needs w_core < 37.5 mm (R05+).
- Every fallback F0 part needs w_core < 37.5 mm (FB1-FB4) or p > 0.05 ⊂ p > 10⁻³ (FB0).
- So S4 contains every candidate that can pass any rung ≥ R05 or any fallback selection. It also contains every
  item-4a measuring population inside them, since R05 alone has ≈ 140-300 candidates per trial, i.e. ≥ 10 always.
- So every F1 (h, o, dE/dx) and SR-T quantity, at every rung and population the rule can use, is computable offline.
- N_IP2 ≥ 7 alone would store ≈ 4× more hit records (≈ 600-1 300 vs ≈ 140-300 per trial) for no rule-relevant gain.
  N_IP2 ≥ 6 would store ≈ 15× more.
- The counting-rung conditionals need only the S1 counts (S2 for candidate-level checks).

**ρ = 2 trials (B2, G3B2):**

| id | stored for | content |
|---|---|---|
| S1′ | **every trial** | S1 plus, per rung, S_uni = Σ w_r, S_ded = Σ_groups max w_r, the IS variance, IS diagnostics (mean W vs DP, zero-W fraction, M_max); with `btl=` (required, §1.4) the same for r ∧ BTL-present: S_uni_T, S_ded_T, V_uni_T, meanW_pull_T |
| S7 (a) | ≤ **200** random R04 sets per trial (all IS-weighted) | compact record + the 43 weights (+ the 43 w_T with `btl=`) + full hit records (as S4) |
| S8 (b) | a **1 % Bernoulli sample of the loose sets** | compact record + the 43 weights (+ w_T) + full hit records |

The per-set weights of the other sets are summed in-job and not stored. Plan §4.1 asked for "23 + ≤ 20 weights × 4 B
per set". At 3·10⁵ sets per trial that is ≈ 52 MB per trial (≈ 300 GB over C1 + C2). The per-trial sums are what the
estimator, the bootstrap and T1/trend use. **Plan change proposed** (`PHASE_A_REPORT.md` §7).

**Measured sizes (compressed npz; smoke and G2b, interim chain):**
- ρ = 1: ≈ 0.25 MB per trial, plus ≈ 1.2 MB per S6 event.
- ρ = 2: ≈ 1.9 MB per trial. S8 dominates.

**Disk estimate:**
- C1 ≈ 15 GB: B1 5.0, S6 2.4, B2 3.8, and ≈ 4 for the G1 blocks (ESTIMATE from plan §6.3).
- C2 ≈ 15 GB: B1 7.0, B2 7.7, SM 0.3.
- C4′ ≈ 3-8 GB (A5 dumps at the normalised density are uncertain).
- G3 ≈ 4 GB.
- **Total ≈ 37-42 GB.** 128 GB were free on 2026-10-13.

---

## 10. Freeze inputs, resolved decisions and plan changes (fix R1)

**Freeze inputs** (`data/acts_stage4/frozen/frozen_inputs.json`, Appendix A.4):
- **F-1** δ₉₅ = **0.15 rad** (§1.3); road = cut.
- **F-2** MIP unit: procedure frozen (§1.4, pooled truncated mean of the V4-9 muon gun). **Value filled (fix R2):
  mip_gev = 3.5582·10⁻⁴ GeV** (`v49.json` → `mip_unit.mip_gev_pooled_truncated`), after the B-2 sampler closure
  (sampler/Fatras 0.99955 ≤ 3 %: PASS).
- **F-3** βγ_μ = **92** (§8), kept. G1 measured a median 90.7 over the 19 475 gun tracks with ≥ 1 TBPX hit (a
  cross-check, recorded in `frozen_inputs.json` → `betagamma_mu_g1_measured`); the difference is immaterial: R_eff
  changes by ≤ 0.09 % and no e_adm cell changes (≤ 0.4 % and none even at 60.2; `review_wp2/r2_eadm_checks.json`).
  F-3 is a generator-level definition (median 92.5 of 2·10⁶ draws).
- **F-4** SR-T definition frozen (§1.4); t_min from B1 + overlay by the frozen rule; the in-job BTL-presence columns
  are **implemented and validated** (fix R2, PC-17) and required (`require_btl`) for every ρ > 1 production job.
- **F-5** f_CKF formula frozen (§1.1 item 9, §1.2); B_PU credit 1.
- **η_max = 1.0** (§1.2, barrel-only).

**Former DRAFT decisions:** D1 resolved (core hits, pooled unit, Fatras-model quirk deposits; §1.4); D2 accepted with the
governing convention (§2); D3 accepted (§6.3, C-7 run check added); D5 resolved (§1.1 item 9); D6 resolved (§1.4); D7
resolved (§1.4); D9 accepted (§1.4); D4-12 re-decided by the user: barrel-only (PC-7).

**Plan changes logged by this rule** (the plan is not edited; where these apply, this file supersedes `plan.md`):

| id | change | plan § | reason |
|---|---|---|---|
| PC-1 | per-hit-set convention from R04 on; R01-R03 and N_L2 diagnostics union only; governing convention per test (§2) | §4.1 step 2, §11 G3 (i) | cost (PHASE_A §7.1); review B-8 |
| PC-2 | ρ = 2 per-set weights stored only for samples (a)/(b); per-trial sums otherwise | §4.1 storage | ≈ 300 GB (PHASE_A §7.2) |
| PC-3 | storage policy S1-S8 (§S); disk ≈ 37-42 GB | §4.1, §6.3 | PHASE_A §7.3 |
| PC-4 | top-up carries dE and t resampled from the sensor's Fatras hits | §1.4 | PHASE_A §7.4; dE = 0 was anti-conservative |
| PC-5 | IS nsub = 64, f_lo = f_hi = 1 | §4.1 step 3b | G2b (PHASE_A §7.5) |
| PC-6 | 43 in-job columns; h/o/SR-T factorised | §4.1 | PHASE_A §7.6 |
| PC-7 | **D4-12 re-decided (user, 2026-10-13): barrel-only F0**, fixed cut \|η(n₃)\| < 1.0; endcap/mixed triplets, the endcap ladder and the (L3, L2, L1) family out of scope (future work); claims restricted (§8) | §2.2 item 2, §2.5 item 3, D4-12 | user decision under the deadline; review B-3 (b) |
| PC-8 | dE/dx over the **core** TBPX hits (was: in-band IT hits) | §2.3 | PU dilution (review B-1 (i)) |
| PC-9 | e_adm from the dilution-aware R_eff (was: R/1.25). **Affects the D4-17 (i) deliverable:** the admissible dE/dx levels shrink to the k_adm = 4 cells (principle unchanged; D4-17 was approved before the e_adm numbers existed); the user is told at the freeze checkpoint (review WP_RULE R2 C-6) | §2.6 | review B-1 (ii) |
| PC-10 | f_CKF counted pre-removal; B_PU credits no f_CKF rejection | §2.2 items 5-6 | review B-6 |
| PC-11 | density-normalisation σ_ln by a direct ρ = 1 re-run on the S6 dumps (was: thinning re-run) | §4.1 step 5 | per-set weights not stored (review B-9) |
| PC-12 | SR-T in-job BTL-presence column required before C1-B2 (superseded by PC-17: implemented before the freeze) | §4.1 step 3b | review B-5 |
| PC-13 | MIP unit = pooled truncated mean of all muon-gun hits (was: per-track median, DRAFT) | §2.3 | review F-2 |
| PC-14 | quirk deposits = draws of the Fatras energy-loss model over the same slab (was: "h_dE with Landau fluctuations") | §2.3 | review B-2 |
| PC-15 | δ₉₅ population/aggregation rule (§1.3): one global value, max over species-masses, 0.15 rad; road = cut | §2.5 item 2, §2.2 | review B-4, A-1 |
| PC-16 | this file lives at `acts/stage4/WP_RULE.md` (plan §2.5 item 9 names `acts/stage4/finder/WP_RULE.md`) | §2.5 item 9 | review C-8 |
| PC-17 | SR-T first factor in-job: 43 columns r ∧ BTL-present (`RUNGS_T`; exact DP via S ∖ I_B, IS × f(T)); `process_trial(btl=, require_btl=)`; ρ > 1 production refused without it; new stored keys only (the 43 existing columns bit-identical) | §4.1 step 3b, §2.3 | review WP_RULE R2 B-2 |
| PC-18 | SR-T background also includes candidates without an in-time BTL hit whose earliest in-band hit is an out-of-time overlay hit in the window: + P̂₁(r ∧ ¬BTL-present) × P_oot(late) (conservative; orchestrator decision 2026-10-13 on the fix-R2 open question) | §6.2, §2.3 | FIX_WP_RULE_R2 open question |

---

## Appendix A. Frozen inputs and hashes

Appendix A is generated by `acts/stage4/finder/wp_rule_tables.py` into `acts/stage4/WP_RULE_tables.md` and pasted
below by the same script, which then writes `data/acts_stage4/frozen/frozen_inputs.json` with this file's sha256.
Regenerate at the freeze (the STATUS line changes the sha256).

<!-- generated by acts/stage4/finder/wp_rule_tables.py from f4r_admissibility.json; do not edit -->
### A.1 Smoothed Λ_R(m) and the width admissibility thresholds (plan §2.6)

k_adm(m, Λ) = the largest k ∈ {0, …, 4} with Λ ≥ Λ_R(m)·2^{(k+1)/2}; the columns give Λ_R·2^{(k+1)/2} (keV): Λ at or above the column value admits width rung k (w_core < W_c/2^k); below the k = 1 column, k_adm = 0 (no width cut).

| species-mass | Λ_R smoothed (keV) | form | per-mass Λ_R (keV) | k ≥ 1 | k ≥ 2 | k ≥ 3 | k ≥ 4 |
|---|---|---|---|---|---|---|---|
| F_m200 | 0.4311 | F/deg2 | 0.4269 | 0.862 | 1.219 | 1.724 | 2.439 |
| F_m300 | 0.5132 | F/deg2 | 0.5022 | 1.026 | 1.452 | 2.053 | 2.903 |
| F_m400 | 0.5693 | F/deg2 | 0.5910 | 1.139 | 1.610 | 2.277 | 3.220 |
| F_m500 | 0.6100 | F/deg2 | 0.6264 | 1.220 | 1.725 | 2.440 | 3.451 |
| F_m600 | 0.6407 | F/deg2 | 0.6472 | 1.281 | 1.812 | 2.563 | 3.624 |
| F_m700 | 0.6643 | F/deg2 | 0.6857 | 1.329 | 1.879 | 2.657 | 3.758 |
| F_m800 | 0.6828 | F/deg2 | 0.7373 | 1.366 | 1.931 | 2.731 | 3.863 |
| F_m900 | 0.6976 | F/deg2 | 0.6522 | 1.395 | 1.973 | 2.790 | 3.946 |
| F_m1000 | 0.7093 | F/deg2 | 0.6812 | 1.419 | 2.006 | 2.837 | 4.012 |
| F_m1100 | 0.7188 | F/deg2 | 0.6953 | 1.438 | 2.033 | 2.875 | 4.066 |
| F_m1200 | 0.7263 | F/deg2 | 0.7120 | 1.453 | 2.054 | 2.905 | 4.109 |
| F_m1300 | 0.7324 | F/deg2 | 0.7163 | 1.465 | 2.072 | 2.930 | 4.143 |
| F_m1400 | 0.7372 | F/deg2 | 0.7621 | 1.474 | 2.085 | 2.949 | 4.170 |
| F_m1500 | 0.7409 | F/deg2 | 0.7759 | 1.482 | 2.096 | 2.964 | 4.191 |
| S_m200 | 0.5939 | S/deg1 | 0.5929 | 1.188 | 1.680 | 2.376 | 3.360 |
| S_m500 | 0.7733 | S/deg1 | 0.7826 | 1.547 | 2.187 | 3.093 | 4.374 |
| S_m1000 | 0.9441 | S/deg1 | 0.9415 | 1.888 | 2.670 | 3.776 | 5.341 |

(Identical, to the JSON rounding, to `k_thresholds_keV` "k>=k" of f4r_admissibility.json, which already includes the one-rung margin; checked by the generator.)

### A.2 βγ_IT(m) (median over the p2 Λ points) and the per-point medians used by the max rule

βγ_IT(m, Λ) = max(βγ_IT(m), per-point median at Λ).

| species-mass | βγ_IT(m) | 0.3 | 0.35 | 0.4 | 0.45 | 0.5 | 0.6 | 0.7 | 0.85 | 1 | 1.2 | 1.5 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F_m200 | 1.823 | 1.943 | 1.845 | 1.924 | 1.877 | 1.868 | 1.816 | 1.802 | 1.758 | 1.869 | 1.766 | 1.812 | 1.835 | 1.801 | 1.782 | 1.823 | 1.829 | 1.823 | 1.836 | 1.803 | — |
| F_m300 | 1.248 | 1.367 | 1.346 | 1.308 | 1.288 | 1.281 | 1.253 | 1.242 | 1.230 | 1.226 | 1.218 | 1.223 | 1.248 | 1.249 | 1.273 | 1.205 | 1.202 | 1.277 | 1.207 | 1.233 | — |
| F_m400 | 1.141 | 1.309 | 1.255 | 1.208 | 1.208 | 1.174 | 1.185 | 1.164 | 1.092 | 1.135 | 1.117 | 1.145 | 1.136 | 1.118 | 1.114 | 1.134 | 1.137 | — | — | — | — |
| F_m500 | 0.915 | 1.083 | 1.063 | 1.027 | 0.995 | 0.977 | 0.951 | 0.935 | 0.911 | 0.899 | 0.936 | 0.879 | 0.902 | 0.913 | 0.904 | 0.896 | 0.888 | 0.923 | 0.888 | 0.915 | — |
| F_m600 | 0.936 | 1.001 | 0.983 | 0.988 | 0.998 | 0.983 | 0.949 | 0.951 | 0.908 | 0.880 | 0.895 | 0.928 | 0.934 | 0.900 | 0.937 | 0.929 | 0.914 | — | — | — | — |
| F_m700 | 0.808 | 0.885 | 0.877 | 0.854 | 0.845 | 0.850 | 0.829 | 0.827 | 0.798 | 0.791 | 0.813 | 0.799 | 0.802 | 0.777 | 0.798 | 0.793 | 0.798 | 0.808 | 0.807 | 0.813 | — |
| F_m800 | 0.805 | 0.915 | 0.865 | 0.874 | 0.842 | 0.855 | 0.819 | 0.817 | 0.820 | 0.779 | 0.790 | 0.781 | 0.775 | 0.793 | 0.789 | 0.771 | 0.774 | — | — | — | — |
| F_m900 | 0.722 | 0.801 | 0.787 | 0.784 | 0.771 | 0.736 | 0.741 | 0.724 | 0.721 | 0.721 | 0.707 | 0.698 | 0.708 | 0.712 | 0.714 | 0.717 | 0.723 | — | — | — | — |
| F_m1000 | 0.677 | 0.763 | 0.726 | 0.725 | 0.714 | 0.705 | 0.683 | 0.678 | 0.679 | 0.666 | 0.676 | 0.670 | 0.674 | 0.680 | 0.667 | 0.673 | 0.679 | 0.676 | 0.671 | 0.670 | 0.675 |
| F_m1100 | 0.621 | 0.711 | 0.702 | 0.667 | 0.667 | 0.665 | 0.630 | 0.630 | 0.622 | 0.619 | 0.607 | 0.614 | 0.608 | 0.611 | 0.616 | 0.600 | 0.607 | — | — | — | — |
| F_m1200 | 0.595 | 0.700 | 0.679 | 0.640 | 0.618 | 0.630 | 0.606 | 0.590 | 0.607 | 0.594 | 0.577 | 0.592 | 0.600 | 0.589 | 0.590 | 0.592 | 0.589 | 0.598 | 0.597 | 0.582 | 0.583 |
| F_m1300 | 0.580 | 0.644 | 0.618 | 0.595 | 0.594 | 0.598 | 0.581 | 0.577 | 0.579 | 0.587 | 0.561 | 0.561 | 0.562 | 0.548 | 0.563 | 0.581 | 0.561 | — | — | — | — |
| F_m1400 | 0.531 | 0.639 | 0.612 | 0.615 | 0.611 | 0.583 | 0.548 | 0.550 | 0.527 | 0.534 | 0.519 | 0.522 | 0.511 | 0.527 | 0.523 | 0.516 | 0.503 | — | — | — | — |
| F_m1500 | 0.520 | 0.575 | 0.579 | 0.558 | 0.556 | 0.543 | 0.540 | 0.531 | 0.534 | 0.516 | 0.517 | 0.505 | 0.508 | 0.518 | 0.508 | 0.506 | 0.522 | 0.513 | 0.517 | 0.528 | 0.510 |
| S_m200 | 1.757 | 2.010 | 1.975 | 1.882 | 1.891 | 1.842 | 1.798 | 1.737 | 1.801 | 1.702 | 1.829 | 1.722 | 1.673 | 1.740 | 1.812 | 1.757 | 1.739 | 1.705 | 1.740 | 1.708 | — |
| S_m500 | 1.068 | 1.297 | 1.271 | 1.202 | 1.214 | 1.192 | 1.130 | 1.133 | 1.090 | 1.080 | 1.057 | 1.027 | 1.050 | 1.074 | 1.046 | 1.043 | 1.060 | 1.016 | 1.057 | 1.061 | 1.058 |
| S_m1000 | 0.744 | 0.929 | 0.908 | 0.889 | 0.867 | 0.858 | 0.809 | 0.804 | 0.780 | 0.740 | 0.740 | 0.726 | 0.733 | 0.730 | 0.741 | 0.744 | 0.756 | 0.723 | 0.742 | 0.743 | 0.735 |

### A.2b Dilution-aware dE/dx admissibility e_adm(m, Λ) (§8; `eadm_dilution.json`)

Cell = k_adm / e_adm (MIP; "–" = none). R_eff/1.25 ≥ e. Model inputs: η_max = 1, βγ_μ = 92, μ_c = [8.0, 3.0, 1.5, 1.0], X_l = [60.0, 123.0, 150.0, 150.0] mm, 4000 toys, seed 20261013, pooled unit 0.9861.

| species-mass | 0.3 | 0.35 | 0.4 | 0.45 | 0.5 | 0.6 | 0.7 | 0.85 | 1 | 1.2 | 1.5 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F_m200 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 1/– | 2/– | 3/– | 4/– | 4/– | 4/– | 4/– | 4/– | 4/– | 4/– |  |
| F_m300 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 2/– | 2/– | 4/– | 4/– | 4/– | 4/– | 4/– | 4/– | 4/– |  |
| F_m400 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 1/– | 2/– | 3/– | 4/– | 4/– | 4/– |  |  |  |  |
| F_m500 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 2/– | 3/– | 4/– | 4/– | 4/– | 4/– | 4/– | 4/– |  |
| F_m600 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 2/– | 3/– | 4/– | 4/– | 4/– |  |  |  |  |
| F_m700 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 2/– | 3/– | 4/– | 4/– | 4/– | 4/– | 4/– | 4/– |  |
| F_m800 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 2/– | 3/– | 4/– | 4/– | 4/– |  |  |  |  |
| F_m900 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 2/– | 3/– | 4/1.3 | 4/1.3 | 4/1.3 |  |  |  |  |
| F_m1000 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 1/– | 3/– | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 |
| F_m1100 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 1/– | 3/– | 4/1.3 | 4/1.3 | 4/1.3 |  |  |  |  |
| F_m1200 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 1/– | 3/– | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 |
| F_m1300 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 1/– | 3/– | 4/1.6 | 4/1.6 | 4/1.6 |  |  |  |  |
| F_m1400 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 1/– | 3/– | 4/1.6 | 4/1.6 | 4/1.6 |  |  |  |  |
| F_m1500 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 1/– | 3/– | 4/1.6 | 4/1.6 | 4/1.6 | 4/1.6 | 4/1.6 | 4/1.6 | 4/1.6 |
| S_m200 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 1/– | 2/– | 3/– | 4/– | 4/– | 4/– | 4/– | 4/– | 4/– |  |
| S_m500 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 2/– | 4/– | 4/– | 4/– | 4/– | 4/– | 4/– | 4/– |
| S_m1000 | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 0/– | 1/– | 2/– | 3/– | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 | 4/1.3 |

### A.3 Hashes (sha256) of the inputs and of the code this rule refers to

| file | sha256 |
|---|---|
| `acts/stage4/finder/finder.py` | `afeef69b94e52061aac0dad8baf6bf834d170589d6f7b12a4d0ee61c88e1195f` |
| `acts/stage4/finder/kernels.py` | `641132971c0fa10f792b6df38f57b887d4e9797b44ebbf0c48e6a47d91bd9b52` |
| `acts/stage4/finder/weights.py` | `a34e0b70f4733d45ba619d80611e85a1f1f352a4df3c4116603859946b8e2e31` |
| `acts/stage4/finder/production.py` | `6aff3d045dadc26fcca5bdc85027dddc776f43a3ba8517c9ffb3ab8c3aa62a22` |
| `acts/stage4/finder/pu_inputs.py` | `5c74938c4998748aac9ce7208d0d093507903a2a8a4764c2d90c8d2b8479621e` |
| `acts/stage4/finder/chain_inputs.py` | `8f5a81779e591b638fdb660b16ed47076c27731c4ff632c6fe27b30c961e723e` |
| `acts/stage4/run_stage4.py` | `85b978f5d85cee28d290d298bb96bb9895299f916bc4df632a9cf2bb66a4879e` |
| `acts/stage4/code/run_chain.py` | `b1130b40f6c729a1145d23ad15b8a176060d0cf3b718e8794f2efe5a9819e8c0` |
| `acts/stage4/code/eloss.py` | `3edcb325fa69ca7ce42734c5423b52fca11da12609ca7d805c305112d6f24eba` |
| `acts/stage4/code/pu_chain_interim.py` | `1e6bf2de7bce20d485f99311fa69f55b998cf9bb023664dc75176464f9938404` |
| `acts/stage4/probes/f4r_admissibility.py` | `b21e6951a02527f00ad1c776e60978aaefb2772b2bd0bca3d6c7cf7fe45711da` |
| `data/acts_stage4/fix_r4/f4r_admissibility.json` | `45847697b76fadaa7d2269c385258b0d67a2248cb1848fff78acedbc13bda97a` |
| `sim/stage3/results/P2.json` | `e63d19d8d1ae76dee9693bfff1098bc62a457e7d6c95c02d1fab83b502442459` |
| `data/acts_stage4/review_r1_constructive/r1c_signal_handles.json` | `14aba918c3ba7e016b6f083da96e2a1b3e52a58f139a84ed7c5ad19f270170c7` |
| `acts/stage4/finder/eadm_dilution.py` | `1dfc52be8a42080d3544a993cffe3da4596dd84663b667ce37741e3db127ec8c` |
| `data/acts_stage4/frozen/eadm_dilution.json` | `7661bd634053da542ef8f114bd6ccad27a36e2a75d0dd7aaea5bee325b9babcd` |
| `data/sim_stage3/STAGE3_INDEX.json` | `67f95ccd7eb3fc039e7ce5db911f525b86df81b3b5905b51b4f99019f7507e34` |
| `data/acts_stage4/review_wp1/r1_inputs.py` | `887e70710ffde1eb809cf00c825191ce236f1766ddc23eee93572db44dccba4e` |
| `data/acts_stage4/review_wp1/r1_inputs.json` | `56dcfaca87131545fb1178a4fe83b4df94955f0ecf49b4b2080aaa4ed3e58329` |
| `data/acts_stage4/g1/v49/v49.json` | `9228ca78ae922261c01e936e6cddfa44a9e152987b31e3b431e665e88d4efbf8` |
| `acts/stage4/plan.md` | `77d3dc9e71e91f237c9118d9210e7a4ac97d69654e73bc7c91943a6be7a647e4` |

f4r inputs as recorded in the JSON: "e63d19d8d1ae76dee9693bfff1098bc62a457e7d6c95c02d1fab83b502442459" (P2.json), "14aba918c3ba7e016b6f083da96e2a1b3e52a58f139a84ed7c5ad19f270170c7" (r1c).

### A.4 Frozen numeric inputs (`data/acts_stage4/frozen/frozen_inputs.json`)

| input | value |
|---|---|
| delta95 | 0.15 |
| eta_max | 1.0 |
| betagamma_mu | 92.0 |
| trunc_frac | 0.6 |
| e_levels | [1.3, 1.6, 2.0] |
| admissibility_margin | 1.25 |
| pu_density_update_trigger | 1.05 |
| f_ckf_cut | 0.2 |
| f_ckf_B_PU_credit | 1.0 |
| t_seed | 6 |
| w_c_mm | 75.0 |
| t_tol_mm | 0.03 |
| nsub | 64 |
| f_lo | 1.0 |
| f_hi | 1.0 |
| sr_t | {"sigma_t_ps": 35.0, "sigma_t_variation_ps": 60.0, "dt_acc_ns": 25.0, "dt_acc_variation_ns": 12.5, "overlay_bx": [-12, 3], "late_rate_threshold": 0.0001, "t_min": "from B1 + overlay by the frozen rule", "in_job_btl_presence": "implemented + validated (fix WP_RULE R2): production.process_trial(btl=, require_btl=), columns RUNGS_T = r & BTL-present; required for every rho > 1 production job"} |
| mip_gev | 0.0003558235445283726 GeV (= 3.5582·10⁻⁴; pooled 0.6-truncated mean of the V4-9 muon-gun TBPX deposits, §1.4; `v49.json`, 19475 tracks, sampler/Fatras 0.99955) |
| betagamma_mu_g1_measured | 90.69 (cross-check only; F-3 = 92) |

The orchestrator freezes by setting `frozen = true` (after the final hash regeneration) and copying the file to `acts/stage4/frozen_inputs.json`, which `run_stage4.py` reads.

