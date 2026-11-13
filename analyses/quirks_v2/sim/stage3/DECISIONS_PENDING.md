# Stage 3: user decisions pending (from the R1 reviews)

Fix pass R1, 2026-10-13. **None of these is decided here.** Each item gives the options, the cost and the reviewers'
recommendations. Sources: `review/CONSTRUCTIVE_REVIEW_S3_R1.md` ("Scope decisions for the user") and
`review/CRITICAL_REVIEW_S3_R1.md`. The numbers quoted are truth level; tags as in README.

## U-1: what P1 claims above 3 keV
**Context.** At 3-5 keV the high-k_B events carry a positive c excess (size VERIFIED: up to +57 ± 11 % at 5 keV,
k_B ≥ 10). Fix R1 attributes its bulk to the cumulative B* term (B*-off runs: residual ≤ 3 % for k_B < 10, +12 ± 3 % at
k_B ≥ 10; attribution ESTIMATE; floor test O-1 not done). Fix R2 (review B-1): the support is a population-median
statement, 5.5σ for B* off against the full E 500 + E 1000 production but only 2.1σ (all) / 2.3σ (k_B ≥ 6) paired on the
same events; B* mainly widens the per-event c spread (VALIDATION §8 item 5).

| option | content | cost |
|---|---|---|
| (a) | Publish the excess as a measured, empirical result: k_B-binned table, size stable under steps and replicas, B*-off remainder within the floor allowance; mechanism open. Restrict the closed-form claims to ℓ_max ≪ R_IT (median ℓ_max/R_IT ≲ 0.6) and k_B ≲ 4. | documentation only |
| (b) | First derive or fit ΔK(k_B, ε, γ*) (NEAR_MISS §10), then claim a law above 3 keV. | weeks of analytic work |

Recommendation: constructive reviewer **(a)**. The critical reviewer requires only that the attribution stay ESTIMATE
(done). Related: the floor test O-1 (plan D12, approved, not done; ≈ 1 CPU-h + 1-2 days person time for an
extended-precision step map) would turn the k_B ≥ 10 remainder and the > 5 keV ±5 % into measurements.

## U-2: how B and MS combine in P1
**Context.** Per event (same rows) Δs_BM/√(Δs_B² + Δs_M²) = 0.99-1.00 at 0.45 keV, 0.95-1.00 at 0.6 keV and 0.80-0.97 at
1-3 keV (VERIFIED, README table). The crossover Δs_B = Δs_MS is mass-dependent: 1.91 / 1.50 / 1.25 / 1.16 keV (E 200 /
500 / 1000 / 1500) and 1.59 keV (Ẽ 500).

| option | content | cost |
|---|---|---|
| (a) | Add one measured panel / table (Δs_BM vs the quadrature sum, sub-quadrature in the crossover region) to the P1 statement; stays within plan option (b) (MS as a measured floor). | ≈ 1 h; data already in `P1.json` (`B_MS_combination`) |
| (b) | Leave MS purely as a floor number, with the crossover quoted as 1.2-1.9 keV and no combination rule. | none |

Recommendation: constructive reviewer: a referee will ask for the combination rule (B-4); it lists both options without
choosing. Critical reviewer: no position.

## U-3: merged-regime coverage for P2
**Context.** At Λ ≥ 15 keV toys exist only for E 1000/1200 (200 each, ≈ 6 independent N = 30 pseudo-experiments per
point). The other masses and Ẽ have templates only.

| option | content | cost |
|---|---|---|
| (a) | Accept: test merged-regime coverage at E 1000/1200 only; use template ↔ toy swap (cross-validation) where both exist. | free |
| (b) | Run toys at 2-3 more masses and Ẽ 500 at 15-40 keV. | ≈ 0.03 CPU-h/event at Λ ≥ 15 keV → ≈ 25 CPU-h per mass for 200 events × 4 Λ (ESTIMATE, from SAMPLES p2_hi 323 CPU-h / 10 891 events) |

Recommendation: constructive reviewer: state the restriction (done, README/HANDOVER); more toys only if Stage 4 needs
coverage away from 1 TeV. The 25 µm edge would need Λ > 40 keV at most masses.

## U-4: Stage-4 geometry
**Context.** Stage-3 hits lie on the simplified cylinders/discs; no trajectories are stored. Straight-line extrapolation
to module planes is not safe for quirks (sagitta ≈ 1.7 mm on TBPX L1, string bending O(10 µm) at 1 keV; ESTIMATE).

| option | content | cost |
|---|---|---|
| (a) | Plan D1 (a): the simplified surfaces are the Stage-4 sensitive surfaces, and the Fatras PU-200 hits are simulated on the same surfaces. Each cylinder/disc is one digitisation module. | no rerun |
| (b) | Plan D1 (b): module planes (17 092 modules); rerun the Stage-4 subset with a module-plane recorder (new kernel recorder version). | a kernel recorder change + a rerun of the Stage-4 subset (size set by U-3/U-5 and the Stage-4 point list; not estimated here) |

Recommendation: constructive reviewer lists both (B-7) and requires the contract to be explicit (done in HANDOVER §2).

## U-5: Stage-4 digitisation model in the merged regime
**Context.** ACTS `DigitizationAlgorithm` defaults to `doMerge = True`, `mergeNsigma = 1` (14.4 µm with the generic
smearing config); on whole-cylinder "modules" this merges the two quirks' close hits (V8: 463/470, 442/472, 375/448
measurements at 10/15/30 keV; exact with `doMerge = False`).

| option | content | cost |
|---|---|---|
| (a) | Geometric (channelised) digitisation with CMS-like pitch and clustering: the physical merging; needs the energy deposit from `h_dE` and, for realism, U-4 (b). | Stage-4 configuration work; more if module planes are required |
| (b) | Smearing with `doMerge = False` (no merging): exact hit counts; merging handled at analysis level from the truth-level pair separation. | none |
| (default) | `doMerge = True` at 1σ on whole surfaces | matches neither; both reviewers advise against |

Recommendation: constructive reviewer: choose (a) or (b) explicitly; the default matches neither. Critical reviewer:
Stage 4 must check the merge settings and inject one ACTS event per physics event (B-5).
