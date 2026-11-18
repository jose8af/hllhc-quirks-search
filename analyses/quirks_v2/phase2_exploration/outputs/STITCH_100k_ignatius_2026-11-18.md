# Stitch closure with the 100k inclusive sample at m = 200 GeV — executor Ignatius (channel (i)), 2026-11-18

Diagnostic for S2-c / f₂₀₀ (channel (ii)); not one of the 41 C1 comparisons. Code `src/stitch_100k.py`; output
`outputs/stitch_100k_ignatius.json`; run on landau, nice 19, 2026-11-18 10:5x (light read of 7 npz files).
Channel (ii)'s files are not changed.

## Definition (unchanged from Rosalie's §3, EXPLORATION_i_rosalie §3)
v1's TRGS stitching (TRG generated with p_T(QQ̄)_ME ≥ 100 GeV ∪ INC rows with p_T(QQ̄)_ME < 100) is exact if
σ_TRG(p_T(QQ̄) > 200) = σ_INC(p_T(QQ̄) > 200, p_T(QQ̄)_ME ≥ 100) (`sim/scripts/stitch_trg.py` l.4–5). p_T(QQ̄) =
`pt_pair` after the shower; p_T(QQ̄)_ME = hypot of `p_qq_hard` x, y (stitch_trg.py l.40). INC chunks merged as
`merge_chunks.py` l.2–3 (w × N_LHE,chunk / N_LHE,total). Errors √Σw² of the selected rows; z = Δ/√(e_T² + e_I²).
Samples (done markers checked by the script): TRG `p2-a-c1-s2/c1s2-trg-m200-c00` (20,000 LHE); INC
`p2-a-c1-s2/c1s2-inc-m200-c00` + `p2-a-c1-s2inc/c1s2-inc-m200-c01…c05` (6 × 20,000 = 120,000 LHE; distinct MG seeds;
FSR off, CP5, xqcut 30, qCut 45 as v1) [VERIFIED, chunk JSONs].

## Result [VERIFIED, outputs/stitch_100k_ignatius.json]

| sample | σ(p_T > 200) [fb] | rows |
|---|---|---|
| TRG (20k) | 4.2468 ± 0.0740 | 4,237 |
| INC merged (120k), p_T_ME ≥ 100 | 4.2464 ± 0.0774 | 3,917 |
| **ratio TRG / INC** | **1.0001 ± 0.0252, z = 0.00** | |

Per INC chunk (σ, ratio TRG/chunk): c00 3.798 ± 0.179 (1.118: the 20k value of Rosalie's §3, reproduced exactly),
c01 4.197 ± 0.189 (1.012), c02 4.671 ± 0.199 (0.909), c03 4.214 ± 0.189 (1.008), c04 4.283 ± 0.190 (0.992),
c05 4.316 ± 0.191 (0.984).

Spread check: χ² of the six chunk values about their mean = 11.07 for 5 dof (p = 0.050) [VERIFIED, scipy]; the sample
standard deviation of the chunks is 0.280 fb against a mean √Σw² of 0.189 fb (×1.49). The per-chunk σ_LHE values agree
to 0.3 % (0.16868–0.16945 pb), so the MG normalisation does not cause it. Reading: √Σw² may understate the chunk-to-chunk
spread (p = 0.05 is not conclusive). With the error of the INC value scaled by 1.49, the ratio is 1.000 ± 0.032.

For reference: σ_INC(p_T > 200, all p_T_ME) = 4.461 fb, of which the p_T_ME < 100 complement is 0.214 ± 0.017 fb
(4.8 %), i.e. the piece the stitching takes from INC.

## Implication for f₂₀₀ (channel (ii): E 200 f₂₀₀ = 0.0484, band +4.3 / −3.2 %, EXPLORATION_ii_edgar §2.4 [UNVERIFIED by me])
- **The 2.3σ excess seen with 20k INC events was a fluctuation of chunk c00.** With 120k INC events the TRG and INC
  tails agree to 0.0 ± 2.5 % (± 3.2 % with the scaled error). The generation cut closes, as v1 stated.
- A real 5 % excess is disfavoured at 2.0σ (1.6σ with the scaled error); a 12 % excess at 4.8σ (3.7σ). The 95 %
  (2σ) upper limit on a TRG excess is ≈ 5 % (≈ 6.5 % scaled) [VERIFIED arithmetic from the numbers above].
- So nothing indicates that the inclusive-only f₂₀₀ is biased low at E 200: no change of the frozen f₂₀₀ definition
  and no extra one-sided band piece is motivated by this check. The residual statistical sensitivity (±2.5–3.2 %) is
  below channel (ii)'s E 200 band (+4.3 / −3.2 %).
- **Not rechecked:** E 500 (20k INC: 1.055 ± 0.038, 1.5σ). Given the E 200 outcome it is most likely a fluctuation too,
  but it is untested; a 100k INC at m 500 would cost ≈ 1.3 CPU-h (ESTIMATE, as at m 200). Not run (not asked).
- Caveat: these samples have QED FSR off (v1's C1 setting); channel (ii)'s nominal has QED FSR on. The closure tests
  the ME cut of the generation, which does not depend on FSR.
