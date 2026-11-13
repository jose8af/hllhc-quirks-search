# Proposed changes to the analytic predictions (from Stage-3 P1): P-10 and its neighbours

E8 (executor), 2026-10-13. **Proposal only. `analytic/` is not edited.** The changes go through the theory-track review
loop (E1 owner, critical reviewer).

Source of every number: `results/P1.json` (`v2b_revisit`, `points.*.by_lambda.*.c`), `results/c5kev_diag.json`,
`results/FIX_A1_floor.json` and `results/FIX_bstar_off.json`, made by `scripts/p1_results.py`, `scripts/val_c5kev.py`,
`scripts/fix_a1_floor.py` and `scripts/fix_bstar_off.py`. **Revised in fix pass R1** (`review/FIX_S3_R1.md`): the
attribution of the 3-5 keV excess is ESTIMATE, the 30-cell average is withdrawn, P-9/P-11/P-13/P-14 are restated.

Sample and settings:
- 300 MG events per point (200 at 7-10 keV): TRGS, p_T(QQ̄) > 200 GeV, |η_pair| < 1, vertex at the origin.
- E 200/500/1000/1500 and Ẽ 500 GeV.
- B₀ and B₀/2 at max_boost 10⁻³.
- Δs on the 10 T3 barrel layers.

Definitions:
- c2 = (2Δs(B₀/2)/Δs(B₀) − 1)/ln 2;
- c_ev = 1/[ln(ℓ_max/b_odd) + K(γ*)], evaluated on the same events;
- r = c2 − c_ev.

Tags: VERIFIED = measured here on the production (bootstrap errors); ESTIMATE = interpretation.

## 1. What the full P1 statistics show (30 cells: 5 points × Λ = 0.45, 0.6, 1, 2, 3, 5 keV)

1. **The per-event law holds in the conditional median at 1-2 keV, for every k_B (VERIFIED); 0.6 keV is the onset of the
   low-Λ failure (k_B-ordered residuals).**
   - Pooled over the 5 points at 1 keV, the median relative residual r/c_ev per k_B bin is:
     | k_B bin | 0-2 | 2-4 | 4-6 | 6-10 | ≥ 10 |
     |---|---|---|---|---|---|
     | median r/c_ev | +0.2 ± 0.3 % | −0.1 ± 0.3 % | −0.0 ± 0.4 % | +0.2 ± 0.9 % | −2.0 ± 1.4 % |
   - At 2 keV every bin lies within ±2.4 %. At 0.6 keV the bins run from +2.8 % (k_B < 2) to −7.3 ± 2.3 % (k_B ≥ 10).
   - The per-event scatter grows with k_B: the robust σ of r/c_ev rises from 5 % to 32 % at 1 keV.
   - The scatter also grows with γ*: it is ≥ 60 % for γ* > 1.6.
   - The paired median of r is within ±1.5 % of c_ev in every point at 0.6-2 keV (the k_B-binned residuals at 0.6 keV are not).
   - Dimensionless window: the 1-2 keV cells have median ℓ_max/R_IT 0.05-0.61 (README table); 0.6 keV 0.5-1.7; 0.45 keV 0.9-3.
2. **At 1-2 keV the population-median excess of V2b is an estimator effect, not a failure of the law (numbers VERIFIED;
   reading ESTIMATE).**
   - Excess = median(c2)/median(c_ev) − 1. At 1 keV: +0.7/+2.0/+1.1/+2.1/+3.2 % (E200/E500/E1000/E1500/Ẽ500); weighted
     over the 1-2 keV cells: +1.71 ± 0.29 %.
   - Test: the law exact in the conditional median, plus the observed heteroscedastic scatter made symmetric (r re-centred
     in γ* bins, random signs). This zero-median symmetric model gives +2.04 % on average at 1-2 keV; population ≈ paired +
     scatter shift closes to ≤ 0.7 % per cell at 1 keV (critical review §1.2, reproduced).
   - The high-k_B events contribute **through their larger scatter**, not through a conditional bias: at 1 keV the k_B < 6
     sub-sample excess is smaller than the full one at 4 of 5 points (E500 +1.05 vs +2.00 %, E1500 +0.26 vs +2.10 %,
     Ẽ +0.87 vs +3.15 %).
   - The statement is demonstrated at 1-2 keV only. At 0.6 keV it does not close for E1500 and Ẽ500 (onset of the 0.45 keV
     failure). The E8 average over all 30 cells (+1.85 ± 0.19 %) mixed regimes and is withdrawn; by regime: 0.45 keV
     −1.43 ± 0.51 %, 0.6 keV +0.64 ± 0.40 %, 1-2 keV +1.71 ± 0.29 %, 3-5 keV +6.22 ± 0.45 %.
   - The same offset is in the Stage-1 data: +2.4 % on the M3 events, with a paired difference of 5×10⁻⁵ (V2b gate,
     VALIDATION_GATE.md §2).
3. **The law fails at the two ends of the P1 range (VERIFIED as numbers).**
   - **0.45 keV** (median ℓ_max/R_IT 0.9-3): residuals ordered by k_B: +6.0 ± 0.6 % at k_B < 2, down to −26 ± 4 % at
     k_B ≥ 10. The Λ exponent between 0.45 and 0.6 keV is −1.86 … −2.10, against −2 + 2c = −1.74 … −1.78. Cause (ESTIMATE,
     not separated): the non-secular b_odd ∝ m/Λ⁴ terms expected by plan §1.2, or the finite-tracker terms (ℓ_max ≳ R_IT,
     few oscillations inside the tracker), which the full MG model contains and which reproduce the population slopes.
   - **3 keV** (B₀/2 is, per oscillation, the B₀ law at 4.2 keV; P-25): a positive conditional excess that grows with
     k_B: +2.4 % (4 ≤ k_B < 6), +3.3 % (6-10), +8.9 ± 3.1 % (≥ 10). Population: +5.6/+4.9/+7.0 % at E1000/E1500/Ẽ500;
     +2.2/+0.8 % at E200/E500.
   - **5 keV** (per oscillation 7.1 keV):
     | k_B bin | 0-2 | 2-4 | 4-6 | 6-10 | ≥ 10 |
     |---|---|---|---|---|---|
     | median r/c_ev (VERIFIED) | +2.0 ± 1.0 % | +6.5 ± 1.3 % | +12.9 ± 2.6 % | +18.6 ± 6.0 % | +56.5 ± 10.9 % |
     | Stage-1 floor-law allowance (ESTIMATE) | 0.1-0.2 % | 0.3-0.9 % | 0.9-2.4 % | 2.2-5.7 % | 8.8-23 % |
     | *B*-off test, E 500 + E 1000 only (fix R1; rows below added in fix R2):* | | | | | |
     | production, all E 500 + E 1000 events (n) | +1.2 ± 1.0 % (83) | +6.9 ± 1.6 % (167) | +9.6 ± 2.7 % (128) | +16.7 ± 5.9 % (123) | +56.8 ± 15.5 % (99) |
     | median r/c_ev with B* on, the 32 B*-off events/bin | +1.5 ± 1.5 % | +13.5 ± 7.2 % | +1.7 ± 4.1 % | +31.7 ± 17.8 % | +37.5 ± 20.7 % |
     | median r/c_ev with **B* off**, same 32 events/bin | +0.3 ± 0.4 % | +0.2 ± 0.8 % | +2.7 ± 1.3 % | +2.9 ± 1.1 % | +12.2 ± 3.3 % |
     | paired on − off, same events (significance) | +1.2 ± 1.4 % (0.8σ) | +13.3 ± 7.5 % (1.8σ) | −1.1 ± 4.4 % (−0.2σ) | +28.8 ± 18.7 % (1.5σ) | +25.4 ± 19.6 % (1.3σ) |
     | floor-law allowance at the B*-off events' own ε⊥ (ESTIMATE) | 0.3-0.7 % | 0.5-1.3 % | 1.0-2.5 % | 2.2-5.8 % | 6.9-18.2 % |
     Population +9.5 … +17.3 %, at 4.9-7.4σ at every point. The first two rows pool the 5 points; the B*-off block is
     E 500 + E 1000 only (`results/FIX_bstar_off.json`, `results/FIX_R2_bstar_context.json`, VALIDATION §8 item 5).
   - **Attribution (ESTIMATE).**
     - *Cumulative, not per-oscillation:* at matched (k_B, ε⊥(B₀)) the excess grows with Λ (N_osc ∝ Λ²): k_B 4-10, ε⊥
       1-3×10⁻⁶: +1.7 ± 1.9 % (3 keV) → +14.6 ± 2.3 % (5 keV); k_B < 4, ε⊥ 3-10×10⁻⁶: −0.4/+1.2/+3.2 % at 2/3/5 keV. The
       precision floor is a function of ε⊥ only and is N-independent (FIX2).
     - *B* isolated (population-median statement; reworded in fix R2):* with the pair-frame B* switched off (FIX2 method,
       same kernel), the median drops to ≤ 3 % for k_B < 10 and to +12 ± 3 % at k_B ≥ 10, which is inside the floor-law
       allowance (6.9-18.2 % at these events' ε⊥).
       - Strongest support: B* off against the full production of the same two masses, all events: +1.8 ± 0.7 % (160)
         vs **+9.7 ± 1.3 %** (600), difference +8.0 ± 1.4 %, **5.5σ** (5.7σ against the 440 production events not in the
         B*-off sample; `scripts/fix_r2_bstar_context.py`).
       - Paired on the same events the evidence is weaker: on − off = **+27.6 ± 11.8 % for k_B ≥ 6 (2.3σ)** and
         **+8.6 ± 4.2 % for all 160 (2.1σ)**; per bin 0.8-1.8σ. At k_B 0-2 the on arm is itself ≈ 0, and at k_B 4-6 this
         sample shows no excess to remove (on +1.7 ± 4.1 %, off +2.7 ± 1.3 %).
       - The +3-5 % cumulative part at k_B < 4 is consistent with removal (+4.1 ± 2.2 %, 1.8σ paired) (at 3 keV and
         s = 1 FIX2 had found B* on ≈ off there).
       - B* mainly widens the per-event spread of c: at k_B ≥ 10 the per-event (c_on − c_off)/c_ev has median +8 ± 19 % and
         IQR −30 … +112 % of c.
       So the bulk of the population-median excess is attributed (ESTIMATE) to the cumulative B* part, consistent with
       Stage 1's B* part for k_B ≳ 5 (FIX2) and with NEAR_MISS §5.5 ("tens of % in c for k_B ≳ 10").
     - *Floor:* minor below k_B ≈ 10; at k_B ≥ 10 it may be up to ~40 % of the excess. **5 keV, k_B ≥ 10: +57 %, of which
       ≈ 9-23 % of c may be the precision floor** (the B*-off remainder, +12 ± 3 %, is of that size).
     - *Not a discriminant:* the 10⁻⁴-step and round-off-replica tests (median r 0.275 → 0.294; replica spread 0.021) show
       the **size** is stable, but they do not probe the precision floor (NUMERICS §13.1 item 3). The floor test D12/O-1 was
       not done (VALIDATION §9.1).
   - Consistency with Stage 1: Stage-3 paired Δc(2) at 5 keV is +0.0065 (E500) and +0.0085 (E1000), within 1σ of the
     Stage-1 direct B₀ runs (+0.005 ± 0.007, +0.004 ± 0.007), with the same k_B ordering; P-9's "≲ 1 % on
     Δs_B(5)/Δs_B(3)" still holds (paired Δs_B/model moves by +0.2/+0.3 % from 3 to 5 keV).
   - FYI (critical C-10): at 3 keV, E 1000 the paired r/c_ev is +2.8 ± 0.9 % (≈ +0.0023), against Stage 1's
     −0.0003 ± 0.0006 at 1 TeV, k_f = 2 on the T3-cache sample (2.7σ); at 500 GeV the sign is reversed. The k_B spectra
     of the two samples differ, so this is not a contradiction.

## 2. Proposed P-10 wording (to replace the current row in NEAR_MISS §8 and `predictions.json["c"]`)

> **P-10 | c (local log slope)** | c = 1/[ln(1/ε_B) + C]; per event c_ev = 1/[ln(ℓ_max/b_odd) + K(γ*)] with the event's C.
> **Status:**
> - **Per event (conditional median):** VERIFIED-NUM on the MG sample at 1-2 keV, to ≤ 1.5 % (paired median, every
>   point), within ±2.4 % in every k_B bin up to k_B ≥ 10. Validity window: median ℓ_max/R_IT ≲ 0.6 and k_B ≲ 4 (in keV
>   for the CMS Phase-2 tracker: ≈ 1-2 keV). At 0.6 keV the k_B ≥ 10 bin is at −7 %. The per-event scatter grows with
>   k_B (robust σ 5 % → 32 % at 1 keV) and with γ* (≥ 60 % for γ* > 1.6).
> - **Population median:** at 1-2 keV the median of the measured c lies +1.71 ± 0.29 % above the median of c_ev, the
>   shift that the per-event scatter alone produces (+2.04 %). So the population medians agree to ≈ 2-3 %, not ≤ 1.5 %.
> - **Range of validity:** fails at 0.45 keV (ℓ_max ≳ R_IT): +6 % at k_B < 2 to −26 % at k_B ≥ 10.
> - **At ≥ 3 keV** a cumulative positive excess appears, ordered in k_B: +2-9 % at 3 keV and +2-57 % at 5 keV with B₀/2
>   (per oscillation 4.2 and 7.1 keV); population +9-17 % at 5 keV. Size VERIFIED; it is step- and replica-stable.
>   Attribution ESTIMATE: removing B* (B*-off runs) removes the bulk of the population-median excess (B* off +1.8 ± 0.7 %
>   vs production +9.7 ± 1.3 % at E 500 + E 1000, 5.5σ; paired on the same events +8.6 ± 4.2 %, 2.1σ, and +27.6 ± 11.8 %
>   at k_B ≥ 6, 2.3σ). B* mainly widens the per-event spread of c. The B*-off remainder (≤ 3 % for k_B < 10, +12 ± 3 %
>   at k_B ≥ 10) is within the Stage-1 precision-floor allowance (≈ 7-23 % of c at k_B ≥ 10). The floor test (O-1) is not
>   done. The per-event law is not valid there for k_B ≳ 4.

Consequential edits (proposed):
- **P-11** (Λ exponents). Median per-event slopes, with pulls against −2 + 2c_ev [closed form] and population slopes with
  pulls against the full MG rotating-yo-yo model {full}:
  - 0.45→0.6 keV: −1.86 … −2.10 [+2.6 … +7.9σ]; {|pull| ≤ 2.0};
  - 0.6→1 keV: −1.88 … −1.95 against −1.76 … −1.80, [+3.9 … +5.9σ at all 5 points]; {|pull| ≤ 1.2};
  - 1→2 keV: −1.81 … −1.86 [≤ 1.2σ at E 200-1000; +4.1σ E 1500, +4.5σ Ẽ 500]; {|pull| ≤ 1.1};
  - 1→3 keV: −1.81 … −1.85 against −1.80 … −1.82 [+2.3 / +0.3 / +3.0 / +3.4 / +3.9σ at E200/E500/E1000/E1500/Ẽ500
    (sign convention prediction − measurement; the measured slopes are steeper)]; {|pull| ≤ 0.6};
  - 5→10 keV (E 500/1000 only, ±5 % unattributed): −1.75/−1.71 ± 0.03 against −1.85 [−4.0/−5.5σ]; {−2.0/−2.0σ}.
  Reading (ESTIMATE): −2 + 2c is the asymptotic exponent for ℓ_max ≪ R_IT; the deviations grow with ℓ_max/R_IT (largest at
  E 1500 and Ẽ 500, ℓ_max/R_IT ≈ 0.6 at 1 keV) and follow the finite-tracker terms that the full model contains. The
  steeper 1→3 keV slopes go opposite to the c excess and belong with the model-accuracy statement of P-9.
- **P-13/P-14** (R(1/2)). R(1/2) ≡ 1 + c ln 2: the same measurement as c, not independent support of P-10.
  - 500 GeV, 1 keV: 1.0737 ± 0.0007 vs 1.072 (P-13): 2.4σ (the same +2 % as c); vs 1 + c_ev ln 2 on the same events,
    pull in the README table.
  - 500 GeV, 3 keV: 1.0593 ± 0.0006 vs 1.059 (P-14): 0.5σ.
  - At 5 keV R(1/2) exceeds 1 + c_ev ln 2 by 0.005-0.009 at every point: the same excess as c.
- **P-9** ("consistent to 5 keV"): restate with the paired per-event ratio measured/model as the evidence:
  - E ≥ 500: 0.990-1.002 at 0.6-5 keV; E 200: 0.966-0.990; Ẽ 500: 0.947-0.986; i.e. ≤ 3.4 % (E), ≤ 5.3 % (Ẽ), within the
    declared c06 accuracy (P-16: 1-4 %). The deviation is a γ* effect: ≤ 0.8 % for γ* < 1.3, −2 … −5 % at 1.3-1.6, −7 … −11 %
    above 1.6, the same for both spins.
  - Above 5 keV: paired ratio 1.001/1.008 at 7 keV and **1.016 ± 0.005 / 1.027 ± 0.005 at 10 keV** (E 500/E 1000;
    unflagged events 1.019/1.033). Replace part of the "unattributed ±5 %" by this measured, floor-independent +1.6/+2.7 %
    (same sign as the c excess; consistent with FIX2's +2.8/+3.4 %), plus a residual unattributed part.
  - The unpaired pulls (|pull| ≤ 1.7) are a secondary column only.
- **C on the MG sample:** C = 1/median(c2) − ln(1/ε_B) at 1 keV is 0.41/1.01/1.64/1.78/1.01. The per-event medians on
  the same events are 0.48/1.19/1.75/1.99/1.30. The difference is the ≈ +2 % estimator offset of item 2.
- **open_after_E2 / §10:** "B* at real oscillation numbers unmeasured" becomes: the cumulative B* part is seen at 3-5 keV
  via B₀/2 (P-25) and isolated by B*-off runs at 5 keV (ESTIMATE attribution, floor not tested). Open: an analytic
  ΔK(k_B, ε, γ*) and the floor test O-1.

## 3. What is not proposed
- No coefficient of the law is refitted, and K(γ*) and G are unchanged.
- The pre-registered V2b criterion stays as it was: it failed at 3 of 5 points at 1 keV, and P1 confirms that this
  outcome holds with the full statistics (9 of 30 cells pass the literal criterion).
