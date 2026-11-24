# CAUSE_METHOD (p3-f, investigator Jorunn): method and pre-stated criterion, written before any p3-f job

Written 2026-11-24 15:00-15:25 -0500 (`date`), before any p3-f computation. Its sha256 is recorded in
`phase3_selection/logs/investigator_jorunn_2026-11-24_14-55.md` before the first job. Binding texts: ADVISOR_B2CAP_freja
Addendum 1 A1-A3, A6; STR l.340-548, l.1119-1228, l.2713-2760. No redesign is built or compared here. `dev.pu1` is not
opened. No direct count is used as an input of any measurement below.

## A.0 What is to be explained (transcribed from `outputs/p3b/b2_dev_closure.json` → `occupancy`)

Occupancy model (P3B §4.1): B(R04) = N_cfg·P_real(R04); B(R05) = N_cfg·P_real(R05); B(r ≥ R06) = N_cfg·C(R05)·E_model(r),
with P_real the pass fraction of the frozen random-configuration ensemble ("fixed random ribbons") on the real hits of
the 16,000 C1 ρ = 1 trials, C(R05) = P_real(R05)/E_model(R05), N_cfg from the GLS fit at R04-R05.
Observed residuals ln r = ln(B/B_dir): R04 +0.00628 (in-sample), **R05 −0.16644 (σ_tot 0.0193, in-sample)**,
**R06 +0.35481 (σ_tot 0.0335, held out)**. These two numbers are the target; they are not an input of any measurement.

## A.1 Hypothesis tested (one mechanism, stated now)

The model counts **configurations** (planes of the frozen ensemble that pass rung r, times a constant N_cfg); the direct
count counts **distinct finder groups** (refitted candidates grouped at ≥ 50 % shared hits of the smaller set, a group
counted at r if a member passes r). Hypothesis H: *the residuals are caused by the configuration-to-group map: (a) the
finder's refit moves a plane to its least-squares plane and recentres its axis (and collection window), changing which
hit set is counted and its width; (b) the ensemble probability ("basin volume") per distinct group depends on the
group's width, so the number of distinct groups is not proportional to the number of passing configurations.*

## A.2 Measurements (one campaign `p3-f-occx`, C1 ρ = 1 development sample `c1.pu1`, all 4,000 events, 16,000 trials)

Per trial (event replayed exactly as `p3b/occ_replay`, PV/φ_MET checked bit-exact against the stored trial, job raises
otherwise), M = 10,000 configurations θ from the **frozen p3-b ensemble** (`occ_core`: φ_a = φ_MET ± 0.15, η_a ∈ U(−1, 1),
ψ ∈ U(0, π), |n_z| ≥ 0.2), fresh seeds (`qv2|p3f.occx|<job>|<trial>`).

**(i) Dorte's diagnostic.** For every θ the fixed-ribbon flags exactly as `occ_core.real_planes` (band, road, layer
crossings, `thin_core._set_vars`, `col_flags`): P_fix(r) per column; C(R06) = P_fix(R06)/E_model(R06) with the frozen
E_model (no new model run). Expected ≈ 310 R06 configurations (C(R06) to ≈ ±6 %).

**(ii) Mechanism measurement M_G: hit-level emulation of the number of distinct finder-like groups.**
- *Map θ → candidate (refit map).* Eligible if the fixed band of θ has N_IT2 ≥ 3 and N_IP2 ≥ 6 (cost cut; check C2
  below). The finder's refit is applied starting from (n, a) of θ with the arithmetic of `kernels.refit_packed`
  (selection |u·n| < 3σ(n), u·a > 0, |u·n2| < 75 mm, the road; pre-filter |u·n₀| < 5 mm, 60 mm on 2S, w.r.t. the
  starting normal; weights 1/sg², n ← smallest eigenvector of the weighted scatter, sign kept, axis ← in-plane
  projection of the mean unit vector of the selected hits; 3 updates then the final selection; < 4 hits → no
  candidate). Candidate variables by `thin_core._set_vars` arithmetic (= `cand_vars`); R04 also requires the frozen
  aligned cuts on the refitted axis, |Δφ(axis, MET)| < 0.15 and |η(axis)| < 1.0 (`frozen_inputs.json`); rung flags by
  `col_flags`. S(θ) = the candidate's final hit list.
- *Group identity.* θ' is in the r-neighbourhood of θ if its candidate passes r and shares ≥ 0.5·min(|S'|, |S|) hits
  with S(θ) (the `weights.group_sets` criterion, all in-band hits).
- *Basin volume.* V_r(θ) = ensemble probability of the r-neighbourhood of θ, estimated by local sampling around θ in
  rotation coordinates: ω = (ω_a, ω_2, ω_n) uniform in a box of half-widths (h_a, h_2, h_n) about the body axes
  (a, n2, n) of θ; θ' = frame of θ rotated by exp(ω); weight w(θ') = J(ω)·cosh²η'·1_D(θ')/Vol(D), with
  J = 2(1 − cos|ω|)/|ω|² (Haar density in exponential coordinates), dφ dη dψ = cosh²η dμ_Haar, D the ensemble domain,
  Vol(D) = 0.3·∫_{−1}^{1}(π − 2 arcsin(0.2 cosh η)) dη. V̂_r = 8 h_a h_2 h_n · mean[w·1_member,r].
  Box: initial h_2 = 4·(0.1 mm)/ρ₇₅ (ρ₇₅ = 75th percentile of u·a over the IP hits of S), h_a = 4·(0.1 mm)/max(5 mm,
  w₉₀) (w₉₀ = 90th percentile of |u·n2 − median|), h_n = 0.15; if any R04 member has |ω_k| > 0.75 h_k, h_k is doubled
  and the sampling restarted with fresh draws (≤ 6 doublings; configurations still at the edge are flagged and counted).
- *Horvitz-Thompson count.* Ĝ(r) = (1/M) Σ_i s_i·1_r(θ_i)/V̂_r(θ_i) per trial (s_i: subsampling weight below), averaged
  over trials. E[Ĝ] = number of distinct r-neighbourhood classes per trial (exact if V is exact).
- *Cost rules (fixed now; they change the precision, not the expectation):* V is computed for every configuration
  passing R06, with probability 1/2 (s = 2) for those passing R05 and not R06, 1/8 (s = 8) for those passing R04 only;
  N_loc = 64 local draws (256 for R06 passers). These numbers may be changed **once**, before the campaign, from the
  timing test only (log entry); the timing test prints no R05/R06 ratio.

**Decomposition (diagnostics only; they cannot change the verdict):** D1 the same HT count with the fixed-ribbon map
(no refit; θ eligible if it passes R04 fixed); D2 the per-configuration refit transfer
ln[P_refit(r)/P_refit(R04)] − ln[P_fix(r)/P_fix(R04)] (no distinct counting); D3 the arithmetic term ln[C(R05)/C(R06)]
from (i); D4 Ĝ_refit(R04) against B_dir(R04) = 170.86 (absolute faithfulness of the emulation at the derivation rung;
reported, not a criterion); the s = 3 (N_2S2 ≥ 3) versions of all of them.

## A.3 Prediction and pre-stated criterion

Prediction from the measurement alone (the model ratios are the frozen model's own outputs, no direct count):
  ln r̂(r) = ln r(R04) + ln[B_model(r)/B_model(R04)] − ln[Ĝ(r)/Ĝ(R04)],   r = R05, R06,
with ln r(R04) = +0.00628 (in-sample derivation rung) and B_model(R05)/B_model(R04) = P_real(R05)/P_real(R04),
B_model(R06)/B_model(R04) = C(R05)E_model(R06)/P_real(R04) (p3-b values). σ_G(r): event bootstrap (2,000 replicas,
events keyed job|event) of ln[Ĝ(r)/Ĝ(R04)]; σ_comb(r) = √(σ_G² + σ_tot,obs²) with σ_tot,obs = 0.0193 / 0.0335.

**"Cause found" (Addendum 1 A1)** = this measurement, which does not use the R05/R06 closure residuals, reproduces their
sign and size within its stated error: for **both** r = R05 and R06
 (a) sign(ln r̂) = sign(ln r_obs) (− at R05, + at R06);
 (b) |ln r̂(r) − ln r_obs(r)| ≤ 2 σ_comb(r);
 (c) |ln r̂(r)| ≥ 2 σ_G(r) (the prediction is distinguishable from "no effect").
All three at both rungs → **CAUSE FOUND**. Otherwise → **CAUSE NOT FOUND**; one rung only → "NOT FOUND (partial)";
σ_G(R06) > 0.12 → "NOT FOUND (insufficient precision)". The verdict uses M_G only; D1-D4 are reported as localisation.

**Validation before the campaign (code checks; a failure is fixed as a bug before the campaign, never after):**
- V1 recapture: on 4 trials with M_bf = 2×10⁵ configurations, Σ_i #{j ≠ i in the r-neighbourhood of i} against
  Σ_i (M_bf − 1)V̂_r(θ_i), r = R04, both maps: ratio within 1 ± max(0.10, 3σ).
- V2 saturation: on 2 trials with M = 10⁶, the greedy (rank order −N_IP2, then χ²/ndf) leader grouping of all R04
  candidates, counted at M = 10⁵, 3×10⁵, 10⁶, against Ĝ(R04): reported (semantic check of the class count).
- C2 eligibility loss: on 400 trials, the fraction of Ĝ_refit(R04) from configurations with fixed N_IP2 = 5
  (eligibility lowered to N_IP2 ≥ 5): reported; if > 5 % the campaign uses N_IP2 ≥ 5.
- C1 replay identity and the p3-b fixed-ribbon arithmetic: P_fix(R04) on the test trials against p3-b's per-trial rate
  (statistical agreement).

## A.4 What a CAUSE FOUND implies (form fixed now; written out in the ticket only if found)

N_cfg(r) := N_cfg^GLS · ρ(r), ρ(r) = [Ĝ(r)/P_fix(r)]/[Ĝ(R04)/P_fix(R04)] measured by this procedure on development hits at
R04, R05, R06; ρ(r) := ρ(R06) for R07-R09 (held, as C is held at R05); the s = 3 family takes ρ_s3 from the same
procedure with N_2S2 ≥ 3, held at R06 beyond; N_cfg^GLS is the frozen R04-R05 GLS normalisation applied to
P_real(r)·ρ(r); no other scale. Inputs that use the finder's refit/grouping arithmetic are labelled "not independent"
(M14). s_model rule, cap 0.135, F = 1.5 and the rung set unchanged; one variant, one comparison (advisor point 4).

## B. Thinning re-find yield (Task B; no direct count compared)

Campaign `p3-f-refind`: the 400 control trials of P3B R1 (C1 ρ = 2 jobs c1pu2-0000…0039, 200 events), replayed and
checked exactly as `p3b/refind_job.py`; K_B = 3 new independent thinning draws per trial (interaction kept with
probability ½, seeds `qv2|p3f.refind|<job>|<trial>|<d>`), the frozen ρ = 1 `process_trial` on each; stored per draw: the
group counts per column, and the hit sets (pool row indices) and variables of the re-found R04 candidates with
w_core < 37.5 or p > 10⁻³, with group ids. Measured: rate per column, relative bootstrap error over events s_boot(K) for
K = 1…3 draws, the within-trial (draw-to-draw) and between-trial variance components, CPU per draw (markers).
N_eff(K, N_ev) = 1/s²(K, N_ev) with s² = (σ_b² + σ_w²/K)/N_ev (fitted from the measured components; checked against the
direct K = 1, 2, 3 bootstraps). Projection to 3,000 ρ = 2 events (6,000 trials) for K = 1, 3, 8, 16, 64: CPU-h, N_eff
per rung, evaluability σ_tot = √(1/N_96k + 1/N_eff) ≤ 0.135 with N_96k the P3B B2-g expected 96,000-trial direct counts
(P3B §3.4 table, both development and v1 rates at R07). Rungs with too few re-found counts (R07+) are projected from
the R06 variance structure, stated as ESTIMATE.
