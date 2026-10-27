# REVIEW_WP_RULE_R1: freeze check of `acts/stage4/WP_RULE.md` (DRAFT, Phase A)

Critical reviewer, 2026-10-13. Authority: `acts/stage4/plan.md` (R9 PASS; sha256 `77d3dc9e…a7e4`, unchanged). Reviewed:
`WP_RULE.md` (DRAFT, 681 lines), `PHASE_A_REPORT.md`, `finder/production.py`, `finder/weights.py` (subset kernel,
constants), `finder/finder.py` (Config, road, Δφ), `run_stage4.py` (frozen-input plumbing). Ignored: G1 work
(`run_chain.py`, `data/acts_stage4/g1/`).

**Signal-blindness of this review.** No signal efficiency, toy or yield was computed. The only signal-derived numbers
are generator/truth kinematics that the plan pre-declares as rule inputs: δ₉₅ (plan §2.5 item 2: truth pT(QQ̄) + MET
smearing) and βγ_IT (already frozen in `f4r_admissibility.json`). The dE/dx point (B-1) is arithmetic on plan numbers
(hits per layer, PU μ_c), not a signal sample. Compute ≈ 0.01 CPU-h. Scratch: `data/acts_stage4/review_wp1/`
(`r1_inputs.py/.json`, `r1_dedx_dilution.py/.json`).

## Verdict

**NOT FREEZE-READY: 1 A, 9 B, 9 C.**

The transcription is complete and faithful (Task 1: every §2.5 item 9 element is present with the plan's values; the 12
hashes in Appendix A.3 reproduce). The rule cannot be frozen yet, for four reasons:
- a production code path breaks the road = δ₉₅ identity as soon as δ₉₅ ≠ 0.25 (A-1). The recommended δ₉₅ is 0.15 rad.
- The dE/dx estimator, as drafted, makes the D4-17 fallback's "keeps the signal by construction" premise false at the
  normalised PU density (B-1). The signal-side dE model is also undefined (B-2).
- One user-approved decision is contradicted (D4-12 endcap seeds; B-3).
- Several frozen methods are under-specified where a later choice would be post hoc (B-4…B-9).

Applying the recommended values (F-1 = 0.15 rad, F-3 = 92 with the e_adm table below) is not enough. A-1, B-1, B-2,
B-5 and B-6 need code. B-4, B-7, B-8 and B-9 need text. B-3 needs a user decision. After these, a narrow verifier pass
suffices.

---

## 1. Transcription check (Task 1)

| §2.5 item 9 element | WP_RULE | status |
|---|---|---|
| Ladder: 23 rungs, order, thresholds (N_IP2 4…7; W_c/2^k = 37.5/18.75/9.4/4.7; p > 10⁻³/0.01/0.05; N_2S2 1…3; h, o ∈ {2,3,5}; e ∈ {1.3,1.6,2.0}) | §3 | ✓ identical. `weights.W_K/P_MIN/E_MIN` match |
| Variable definitions (crossings, N_IT2/N_IP2/N_2S2, w_core, χ²_core, Δφ, f_CKF, stored-only list) | §1.1 | ✓ (f_CKF open, B-6; h/o open, B-7) |
| B sum, log-normal σ_ln, B₈₄ = 84th pct | §4.1 | ✓ |
| Zero/low-count rule 4a (M_j ≥ 10; largest-M_j zero at 1.14/M, σ_ln = 1; others → 1; c among non-zero factors; flag) | §4.2 | ✓ verbatim |
| Split 0.11 + 0.11; combined guard ≤ 0.3 incl. tighter pairs; continuation (larger B₈₄ moves, tie → SR-G, ≤ 44 steps); (R,R) / one-category branches | §5.1-5.2 | ✓ |
| Items 6-11 (no WP → fallback; t_min rule; templates/toys; freeze timing; probe rows; campaigns/union) | §5.3-5.4 | ✓ |
| Per-family extrapolation + closure tests (T1 lever arm, T2, T3, T1w, T1e, T3s, trend, c-test, direction-split failure paths, family compounding, G3 branch) | §6.1-6.4 | ✓ |
| C′: σ̂_h² = σ²_loc,max + t_tol² + (δn_max·\|u\|)², δn_max = 2 mrad; σ_tot with δn = 0; χ²₃ ≤ 48; pre-CKF/pre-merge hand-over; attribution (≥ 3 core hits, ≥ 3 layers, ≥ 1 IT+PS, ±4σ̂_h, ≥ 2 particles; looper rule; per-link); V4-10 + failure path; sampling; P_PV-line 0.22 | §7 | ✓ |
| Fallback: k_adm rule, smoothed Λ_R (forms, P2 hash), βγ_IT rule + max rule, R (restricted, T_cut 100 keV, PDG-2024 Si), 1.25, r_fb, ≤ 20 selections, primary rule, mixed admissibility, no best-of, R_A-R_E tables only, one limit at primary | §8, App. A | ✓ (omits "both are reported wherever both exist": C-9) |
| Campaigns (§6.2) | §9 | ✓ spot-checked C1/C2/C4′/C5 |
| Hashes | A.3 | ✓ all 12 recomputed and equal (finder, kernels, weights, production, pu_inputs, run_stage4, pu_chain_interim, f4r script + json, P2.json, r1c json, plan.md) |

**Code spot-check (production.py / weights.py).**
- The full-set flags implement the cumulative ladder exactly (`full_set_flags`):
  - NaN p fails every p rung;
  - FB0 = R04 ∧ p > 0.05 ∧ N_2S2 ≥ 3, and FB_k = FB0 ∧ w < W_{k}.
- The subset kernel matches plan §4.1 step 3b:
  - plane and axis are fixed;
  - c(T) and w_core(T) come from T's IT+PS hits, and the core is re-centred per subset;
  - 2S hits use the ±3|n₂,z|σ₁ rule;
  - the p rungs test λ_min against χ²-isf at ndf = n_core − 2 (NDF_MAX 4000, never binding);
  - dE/dx is the lowest-60 % mean of T's TBPX hits.
- **The Δφ(n₃, MET) < δ₉₅ cut is now applied:**
  - `aligned = dphi_met < wcfg.delta95` (l.141);
  - `F &= aligned` at every rung (l.158), including the N_L2 diagnostics;
  - R04 grouping is restricted to aligned candidates;
  - ρ = 2 weights are computed only on aligned sets (l.178), which is exact because the axis is fixed under thinning.
  - `dphi_met` is computed from the final axis `AX` (finder.py l.230).
- The road coupling is **not** correct (A-1).

---

## 2. Findings

### A (blocking)

**A-1. Road and cut are decoupled in production; δ_road stays 0.25 rad whatever δ₉₅ is frozen.**
- `run_stage4.run_pu_job` sets `wcfg.delta95` from `frozen_inputs.json` (l.205-208).
- It then calls `PR.process_trial(..., wcfg=wcfg)` without `cfg` (l.245), so `FF.Config()` is used. That Config has
  `road = 0.25` hard-coded (finder.py l.57).
- The road enters both the hit road (`road_select`, l.79) and the seeding (`seeds_fast(..., cfg.road, ...)`, l.206).
- WP_RULE §1.1 item 1 and plan §2.2 define δ_road = δ₉₅. With the recommended δ₉₅ = 0.15 rad (F-1 below), production
  would collect bands from a ×1.7 wider road than the frozen definition and then cut at 0.15. The candidate population,
  in-band hit counts and every B number would belong to a selection that is not the frozen one.
- **Fix:**
  - build `cfg = FF.Config(road=fz['delta95'])` in every job kind (PU, signal, SM, C′);
  - assert `cfg.road == wcfg.delta95` inside `process_trial`;
  - record both values in the output meta;
  - re-run `test_equivalence` at 0.25 (unchanged) and the smoke test at the frozen value;
  - regenerate the A.3 hashes.

### B (must change before the freeze)

**B-1. D1 dE/dx estimator: PU dilution makes the fallback admissibility rule unsound at the normalised density.**

D1 is the mean of the lowest 60 % of **all in-band** TBPX hits. A heavy ribbon pair gives ≈ 3 quirk hits per TBPX layer,
≈ 12 IT hits (plan §2.1). The in-band TBPX PU crossings at the TDR-normalised density are μ_c ≈ 8 + 3 + 1.5 + 1.0 ≈ 13.5
(plan §2.1 table). With ≥ 50 % MIP contamination, a lowest-60 % truncation keeps mostly PU hits, so the estimator
collapses towards 1 MIP whatever the quirk's R is.

Toy (Moyal-proxy Landau, plan numbers only; `review_wp1/r1_dedx_dilution.json`): median estimator and P(> e_adm) for a
12-hit quirk at loss ratio R:

| R (example) | in-band (D1) | core, w ≤ 18.75 mm | core, w ≤ 9.4 mm | core, w ≤ 4.7 mm | no PU |
|---|---|---|---|---|---|
| 2.4 (E1000, e_adm 1.6) | 1.30; P(> 1.6) = 0.05 | 1.54; 0.37 | 1.88; 0.91 | 2.12; 1.00 | 2.46; 1.00 |
| 2.8 (≈ E1200, e_adm 2.0) | 1.37; P(> 2.0) = 0.01 | 1.65; 0.11 | 2.12; 0.68 | 2.43; 0.95 | 2.87; 1.00 |
| 1.7 (E500, e_adm 1.3) | 1.21; P(> 1.3) = 0.16 | 1.31; 0.55 | 1.46; 0.94 | 1.57; 0.99 | 1.74; 1.00 |

Consequences:
- e_adm (plan §2.6: e_min ≤ R/1.25) is calibrated on the **undiluted** R. At the normalised density r_fb would remove
  ≳ 90 % of the signal "by construction" at exactly the heavy, Λ ≈ 1-2 keV points where the plan expects a non-trivial
  fallback limit. This is the failure mode for which R3 B-2 rejected R2's fallback.
- B stays valid: it is measured with the same estimator. The defect is in the fallback design, which is why this is B
  and not A.
- It must be fixed **before** the freeze. B2 stores only per-trial sums of the dE/dx columns, so a later estimator change
  means regenerating B2.

**Fix**, signal-blind, all pre-declared:
- (i) compute dE/dx over the **core** IT hits (|u·n₂ − c| < 2.5 w_core, the χ²_core core). This is the plan's
  "in-band IT hits" restricted to the core, and needs a logged plan change.
- (ii) make admissibility dilution-aware. Either:
  - e_adm(m, Λ) = the largest e ≤ R_eff/1.25, with R_eff the median of a **frozen mixture model**. The model has
    quirk IT hits per layer from Stage-3 truth, PU core crossings = μ_c(B1-measured density) × 2·2.5·W_{k_adm}/(in-window
    length), and the same Landau proxy and estimator; or
  - the simpler conservative rule: **no dE/dx level is admissible unless k_adm ≥ 3**, and then e_adm = the largest
    e ≤ R/1.25 − 0.2.

  Either way the rule uses no detector-level signal efficiency.
- In `weights.subset_weights` the dE/dx buffer must then be filled from core hits; `dedx_sets` must be changed the
  same way. Re-validate with the q = 1 test.

**B-2. The signal-side energy deposit is not defined, so the MIP unit cannot be shared by signal and background.**
- Stage-3 `h_dE` is the **mean** Bethe loss with no fluctuation (HANDOVER l.83, l.89).
- V4-1 requires `depositedEnergy = h_dE`.
- Plan §2.3 says "h_dE with Landau fluctuations added at injection", but no model is given. WP_RULE §1.4 only repeats
  the sentence.
- PU and the muon gun get Fatras' Landau-sampled loss. In thin Si the most probable value is ≈ 0.7× the mean. If quirk
  hits carry the mean (or Landau with mean = h_dE), the quirk/MIP ratio is biased by up to ×1.4, which is larger than
  the 1.3 → 1.6 → 2.0 rung spacing.

**Fix (freeze text plus an analysis-level function):**
- Quirk dE per hit is sampled from **the same energy-loss model Fatras uses** for PU and muons (Landau MPV and width
  evaluated at the hit's βγ, from `h_E`, and the path `h_dl` in Si). V4-1 then applies to the pre-fluctuation value.
- Seeds are hash(row, Λ, hit), so the draws are identical across rungs.
- **Calibration closure (signal-blind):** the same numpy sampler applied to muon-gun truth hits must reproduce the Fatras
  muon-gun MIP unit (F-2) within 3 %. Otherwise the rule is a bug, not a tuning knob.

**B-3. D4-12 conflict: the draft freezes a barrel-only, single-seed-family F0 against a user-approved decision.**
- LOG 2026-10-13 records the user approving **D4-12: endcap seeds in F0 from the start** (69 % of counting-set events
  have |η_pair| > 1).
- Plan §2.2 item 2 also defines the (L3, L2, L1) missing-L4 family.
- The draft implements neither, and the endcap ladder ("fraction of crossed layers") is undefined (WP_RULE §3, §10).
- A rule frozen like this changes the analysis scope. Adding the seeds after the freeze means re-running B1/B2 under
  item 9.

**User decision required before the freeze**, one of:
- (a) implement endcap/mixed triplets, the (L3, L2, L1) family and an explicit endcap ladder before production, which
  needs a G2a/G2b re-timing (t₁ rises);
- (b) re-decide D4-12 to barrel-only for C1/C2. Then WP_RULE §8 "cannot claim" must add |η_pair| ≳ 1 and the 1.0-1.3
  transition, and ε must carry the fiducial loss explicitly. A later endcap category gets its own background-only
  ladder, frozen before its first signal efficiency (the D4-14 precedent).

Reviewer recommendation under the deadline: (b), with the (L3, L2, L1) family also stated as not in scope. This is the
user's call; it must not be decided silently by the freeze.

**B-4. F-1 δ₉₅: population and aggregation undefined.** The plan rule (truth pT(QQ̄) ⊕ σ⊥ smearing, 95 % quantile) does
not say over which events, or how masses combine. The answers differ:
- 0.149 rad with the trigger weight and offline preselection;
- 0.178 rad without them;
- 0.130-0.149 rad across species-masses.

The cut acts on background at every rung, so it must be **one global value**. Freeze the rule in the open-inputs table
(§3). It gives **0.15 rad**, not the 0.25 planning value; see A-1 for the road coupling. The σ⊥ = 15/35 GeV variations
are signal-efficiency systematics and do **not** move the cut.

**B-5. F-4/D7 SR-T: the definition must be frozen now, and the in-job factor must exist before any C1 B2 job.**
- ρ = 2 stores only per-trial sums plus ≤ 200 random R04 sets and 1 % of the loose sets with hit records.
- The plan's per-subset first factor P(≥ 1 in-band BTL hit) at the WP-relevant rungs (R06+, ≈ 0.75 full sets per trial
  at R06; PHASE_A §8) is therefore **not computable offline** with useful variance.
- SR-T carries half the budget, so without the factor its B₈₄ at ρ = 2 depth has no method.
- At ρ = 1 everything is offline-computable: S2 has normal and axis, S5 has all BTL hits with INT.

**Fix:**
- Freeze the BTL band, Δt and the overlay as in §3 F-4.
- Add a BTL-presence flag to the subset kernel (an extra column per IS/DP column, or at least for R04-R14, F0e and
  FB*), q = 1-validated, before C1-B2.
- G3 may run without it: the G3 branch decision (T1/T1w/trend/T_seed) does not use SR-T.

**B-6. F-5/D5 f_CKF: the formula and its treatment in the extrapolation are missing.**
- After CKF removal f_CKF ≡ 0, so the fixed cut f_CKF < 0.2 is vacuous unless counted pre-removal (D5, accepted).
- But f_CKF is a ratio over in-band hits. It changes per thinned subset and is in neither the DP nor the IS. If it is
  applied to B1 counts but not to B2 weights, T1/T1w compare different selections.

**Fix:**
- f_CKF = n_CKF,band/(n_CKF,band + n_band), where n_CKF,band = CKF-used pre-removal measurements inside the
  candidate's final 3σ_tot band, window and forward cone (all layers). Also store the number of CKF tracks with ≥ 5
  band hits.
- Pass the CKF-used hits (G1) to `process_trial` and store n_CKF,band per compact record.
- **B_PU credits no f_CKF rejection** (factor 1). The in-job ladders stay f_CKF-free, so closure is clean and the
  choice is conservative; plan §2.6 rates f_CKF as weak on combinatorial PU.
- SM C, C′_PU and C′₀ apply it through rung factorisation from the stored records (rule 4a).
- Signal applies it in the selection.

**B-7. Composition of the factorised families with the in-job columns is not written; D6 is open.** The in-job columns
are F0 ∧ e and FB_k[∧ e], while the ladder order is …R14 → h → o → e. WP_RULE §6.2 does not say which conditional
multiplies which thinned column. Freeze:
- P₁(R15-R20) = P̂₁(R14) × p(h/o rung | R14);
- P₁(R21-R23) = P̂₁(R14 ∧ e_x) × p(h > 5 ∧ o > 5 | R14 ∧ e_x);
- P₁(r_fb) = P̂₁(FB_k[∧ e]) × p(h > 5 ∧ o > 5 | FB_k[∧ e]).

Each conditional p is measured at ρ = 1 on B1 on the tightest population with M ≥ 10 (4a), and the c-test applies. SR-T
multiplies as P̂₁(r ∧ BTL-present) × P(late).

D6 (needed before A1, the first signal efficiencies):
- split centre = c (the w_core median);
- per layer, two clusters by sign(u·n₂ − c);
- helix ndf = Σ_subsets (2 n_hits) − n_par, with n_par = 3 (PV origin: κ, φ₀, tan λ) or 5 (free origin on the plane);
- h = min over hypotheses of Σχ²/Σndf;
- o: ndf = n_layers − 2, with a ≥ 0 and r₀ ≤ r_min enforced as bounds;
- **undefined (ndf ≤ 0, < 3 hits in a subset, < 4 resolvable two-cluster layers) passes.** This is accepted: no
  rejection is credited.

**B-8. D2 (per-hit-set from R04): the governing convention of each test is not fixed.** Freeze:
- **per-hit-set is governing** for B, T1/T1w/T1e, T3 conditionals at rungs ≥ R04, and the trend test, which is run
  over the rungs ≥ R04 with ≥ 10 B1 counts;
- union counts (all rungs) are diagnostics only;
- the T1 lever arm is computed in one convention, S_ded/N_grp(ρ = 2). Mixing S_ded with the union N_pass would
  overstate the lever arm by the ×3.4-4.6 dedup factor.

D2 itself is accepted. Every WP, fallback and closure rung lies inside R04. At ρ = 2, sets failing R04 have w_R04 = 0
exactly (counts are monotone under thinning), so nothing is lost.

**B-9. The density-normalisation σ_ln term has no computation path once per-set weights are not stored (plan change
§7.2).** The plan's "re-run the thinning with the top-up at its lower/upper value" cannot be done from per-trial sums.
Pre-declare one of:
- (a) **in-job columns with interaction-type-dependent q.** Fatras interactions get q = ½. Top-up crossings get
  q_T = (r − 1)/(2(r_nom − 1)) for r ∈ {r_low, r_up}, feasible while r_up − 1 ≤ 2(r_nom − 1). Limit this to R04-R08,
  R11 and FB0-FB4 to keep t₂ ≲ 45 s;
- (b) a **direct ρ = 1 re-run on the S6 dumps** (2 000 C1 B1 events × 4 roads; ≈ 2 × 9 CPU-h) at r_low and r_up. The
  log-ratio at the deepest rung with ≥ 10 counts is applied as σ_ln to every deeper rung.

(a) is better. (b) is the minimum. Either must be in WP_RULE before the B2 jobs run.

### C (acceptable; optional notes)

- **C-1.** δ₉₅ ignores the detector-level axis error of n₃ (PU hits in the band shift the mean-direction axis). This
  matters more at 0.15 than at 0.25 rad. Report ε(Δφ cut) at A1/V4-3 as a diagnostic; no re-tuning (item 9).
- **C-2.** T_seed = 6 is frozen, but the plan makes T_seed(ρ) subject to the G3 (iv) stability gate. Reference that
  gate and its action in WP_RULE: T_seed(ρ) := 4 if the per-family pass fractions move by > 2σ, then re-time.
- **C-3.** State whether G3 (own seed prefix) enters the §5.4 item 11 union. Recommended: it enters only if produced
  with the frozen code hashes. The G3 branch governs the residual; union T1/trend are reported, and an
  anti-conservative union result still triggers its branch.
- **C-4.** S_ded takes the max over group members of **noisy** IS means (64 subsets). E[max] ≥ max E, so the result is
  biased upward at R07+ (conservative; it can push T1w towards z < −2). Diagnostic at G3: nsub = 256 on a subsample.
- **C-5.** D9 (top-up dE/t resampled from the same sensor's Fatras hits) is accepted. It is strictly better than dE = 0,
  which was anti-conservative for the dE/dx rungs. Optional variation: resample from low-p hits only, inside the
  density σ_ln.
- **C-6.** The path correction r_xy/|u| assumes a straight radial track. It is common to signal and background and is
  part of the definition. Fine.
- **C-7.** D3: nsub = 64 and f_lo = f_hi = 1 are accepted (G2b PASS at full cost; V-c 0/2 000 mismatches; V-d pulls
  ≤ 1.1). Add a per-trial run check: |meanW − DP| pull < 3.
- **C-8.** Plan §2.5 item 9 names `acts/stage4/finder/WP_RULE.md`; the file is `acts/stage4/WP_RULE.md`. Log the path.
- **C-9.** §8 omits "both are reported wherever both exist" (plan §2.6). Add it.

---

## 3. Open freeze inputs: recommended values and sources

| input | recommended value | source / rule to freeze | needed before |
|---|---|---|---|
| **F-1 δ₉₅** | **0.15 rad** (indicative 0.149 = max over 17 species-masses; per-mass 0.130-0.149; σ⊥ = 15/35 GeV give 0.089/0.214) | Yes, it is an acceptance-defining generator-level quantity, like W_c: truth kinematics plus the plan's MET model, with no detector-level signal efficiency and no background comparison. **Rule:** MET_reco = pT(QQ̄) + N(0, σ⊥ = 25 GeV) per component; events weighted by ε_trig (T₅₀ 200, σ_T 20, plateau 0.98) × offline preselection (MET_reco > 250, ≥ 1 jet pT > 100 \|η\| < 2.4, min Δφ(j1-4, MET) > 0.5; plan §3), fiducial \|η_pair\| < 2.5; per species-mass the weighted 95 % quantile of \|Δφ(MET_reco, pT(QQ̄))\|; **δ₉₅ = max over species-masses, rounded up to 0.01 rad**. Use the full Stage-2 MG samples (Λ-independent; the indicative value used one Stage-3 p2 point, 200 events, template half: `review_wp1/r1_inputs.json`). Frozen script + output hash in A.3; the same value goes into `Config.road` and `WCfg.delta95` (A-1) | freeze |
| **F-2 MIP unit** | value in GeV from the muon gun; definition: **0.6-truncated mean of the pooled path-corrected TBPX dE of all muon-gun hits** (the large-n limit; candidates have 12-40 IT hits, a muon 4, and a per-track median at n = 4 is biased high) | V4-9 gun (pT 1-10 GeV, \|η\| < 2.5), ≥ 10⁴ μ through the same Fatras + digitisation config. CKF is irrelevant for a single muon, so this does **not** need G1 (the interim/acts chain suffices). Plus the B-2 closure of the quirk dE sampler | B2 production (in-job dE/dx columns); ρ = 1 is offline-recomputable from S4 |
| **F-3 muon-gun βγ** | **92** (pT uniform 1-10 GeV, η uniform \|η\| < 2.5; 62 for log-uniform pT) | Generator-level, from the gun definition (pin the pT shape in the G1 gun config); no G1 output needed. e_adm is **unchanged** for βγ_μ ∈ [30, 300] at the median βγ_IT (`r1_inputs.json` → `e_adm`). Table below. Subject to B-1 (dilution) | freeze |
| **F-4 SR-T** | Band: BTL hit with \|n·u\| < 3σ_tot (σ_n from the BTL local errors, + t_tol), \|u·n₂\| < W_c, u·n₃ > 0, final plane. Δt = t_BTL − t_PV − \|u\|/c of the earliest in-band hit. t_min = the plan rule (per-hit late rate in B1 + OOT overlay < 10⁻⁴); Δt_acc 25 ns. OOT overlay: BTL hits of independent PU-200 events shifted by k × 25 ns, k ∈ {−12…+3} (the TDR window), with the per-crossing BTL time spread | Plan §2.3, §2.5 item 7, §4.1 table; in-job per-subset BTL-presence (B-5) | definition: freeze; in-job: before C1-B2 (not needed for G3) |
| **F-5 f_CKF** | f_CKF = n_CKF,band/(n_CKF,band + n_band) < 0.2 (pre-removal count, D5); B_PU credits factor 1 (B-6) | Plan §2.2 items 5-6, §1.6; needs the G1 CKF-used flag | definition: freeze; storage: G1 |

**e_adm at the median βγ_IT** (PDG-2024 Si, T_cut 100 keV, βγ_μ = 92; before any B-1 dilution correction):
- R = 1.08 / 1.32 / 1.41 at E200 / E300 / E400, and 1.10 / 1.48 for Ẽ200 / Ẽ500 → no admissible level;
- **1.3** at E500 / E600 (R 1.71 / 1.67) and E700 / E800 (1.95 / 1.96);
- **1.6** at E900 (2.22), E1000 (2.40) and Ẽ1000 (2.14);
- **2.0** at E1100-E1500 (2.68-3.43).

The max rule lowers some levels at small Λ:
- E500 / E600: none at Λ ≤ 0.5 keV;
- E900: 1.3 at 0.3 keV;
- E1100: 1.6 at Λ ≤ 0.5 keV;
- E1200: 1.6 at Λ ≤ 0.35 keV;
- Ẽ1000: 1.3 at Λ ≤ 0.7 keV.

This matches plan §2.6 / review R5, except that E500 now also loses 1.3 at 0.5 keV (borderline, R/1.25 ≈ 1.30). This is
why βγ_μ and the script must be frozen with a hash.

---

## 4. Executor DRAFT decisions and PHASE_A §7 plan changes

| item | class | reason / condition |
|---|---|---|
| D1 dE/dx estimator (lowest-60 % in-band TBPX, sinθ, muon-gun median unit) | **B** | B-1 (core hits + dilution-aware admissibility), B-2 (signal dE model), F-2 (pooled unit) |
| D2 per-hit-set from R04; union at R01-R03 (= §7.1) | **C**, with B-8 | cost-justified; all decision rungs are inside R04; fix the governing convention |
| D3 IS nsub 64; f_lo = f_hi = 1 (= §7.5) | **C** | validated; C-4, C-7 |
| D5 f_CKF counted pre-removal | **C** (concept), with B-6 | otherwise vacuous; formula and B_PU treatment must be frozen |
| D6 h/o open points; undefined → pass | **B** (must be fixed), "undefined → pass" **C** | B-7 concrete values |
| D7 SR-T band / overlay | **B** | B-5, F-4 |
| D9 top-up dE/t resampled (= §7.4) | **C** | C-5 |
| D4-12 barrel-only, no endcap/(L3,L2,L1) | **B** | B-3: user decision |
| §7.2 summed ρ = 2 weights, per-set only for samples (a)/(b) | **C**, conditional on B-5 and B-9 | T1/T1w/T1e/trend/bootstrap/reach need only per-trial sums and full-set counts (checked: S1′ has S_uni, S_ded, V_uni, n_grp, n_pass). T3s uses S7 (INT, normal, axis stored). The density σ_ln and SR-T depth are the two things it breaks |
| §7.3 storage policy S1-S8 | **C** | S4 = R04 ∧ (w < 37.5 ∨ p > 10⁻³) contains every rung ≥ R05 and FB0-FB4 (FB0 needs p > 0.05). Every 4a measuring population for rungs ≥ R05 is ⊂ R05 (140-300/trial ≫ 10). The c-test uses S3 (per-layer crossings stored). Add n_CKF,band (B-6) |
| §7.6 43 in-job columns | **C**, with B-5/B-9 | h/o factorised per plan; add BTL-presence and (option a) density-variation columns |

**Signal-blindness of Phase A:** nothing found that weakens it. All Phase-A numbers are PU-only. The S4 threshold, IS
settings and grouping population were chosen on PU-only cost and rung logic. The only signal-adjacent items (δ₉₅, e_adm)
are generator-level by plan design.

## 5. Path to freeze (ordered)

1. User: D4-12 (B-3).
2. Code:
   - A-1 (road = δ₉₅);
   - B-1 (core-hit dE/dx in `dedx_sets` and `subset_weights`);
   - B-2 (quirk dE sampler + muon closure);
   - B-5 (BTL-presence in-job);
   - B-6 (n_CKF,band);
   - B-9 (a) if chosen.
   
   Then re-run V-c (q = 1), `test_equivalence` and the smoke test, and regenerate the hashes.
3. Inputs: freeze F-1 (script, 0.15 rad indicative), F-3 (92), F-2 (muon gun, pooled), the F-4 definition and the
   F-5 formula. Write `frozen_inputs.json`.
4. Text: B-4, B-7 (composition, D6), B-8, B-9; C-2, C-3, C-8, C-9; log the plan changes §7.1-7.6 + B-1/B-6/B-9.
5. Narrow verifier on the diff; then FREEZE.
