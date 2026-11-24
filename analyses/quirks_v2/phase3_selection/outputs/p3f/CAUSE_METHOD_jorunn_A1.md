# CAUSE_METHOD amendment A1 (p3-f, Jorunn): verdict measurement replaced after the pre-campaign validation failed

Written 2026-11-24 15:35 -0500 (`date`), after the validation runs V1/V2 of `CAUSE_METHOD_jorunn.md` (sha256
99dfcafb6c477bf11606b0716321170157c33cf4be0bbac00b8df50d99c60d83) and **before any campaign**. Only R04 quantities have
been computed or looked at; no R05/R06/R07 ratio of any kind has been formed by this session. This amendment is hashed
in the session log before the campaign is launched. Everything in the original method not changed below stays.

## 1. Why (validation results, R04 only; scratch outputs on maxwell, `val1.npz`, `val2.npz`, `val.json`)
- **V1 recapture FAILED** for both maps: Σ recaptures / Σ (M − 1)V̂ = 2350/2855 = 0.82 (fixed map) and 2376/1661 = 1.43
  (refit map), on 6 trials; per trial the ratio ranges from 0.33 to 6.9; in 4 of 12 (trial, map) cells one configuration
  carries > 40 % of the expected sum. The basin-volume estimator is heavy-tailed (typical V̂ too small because sparse
  far members are missed, rare V̂ very large). This is not a code bug that can be fixed inside the method: the 1/V̂ of
  the Horvitz-Thompson count is not reliable at any affordable N_loc.
- **V2 saturation**: the greedy distinct-class count of R04 configurations keeps rising with M (fixed map 27 / 73 / 159
  and 25 / 71 / 173 classes at 10⁵ / 3×10⁵ / 10⁶ configurations; refit map 21 / 49 / 107 and 20 / 47 / 120): the hit-set
  population available to ribbons on ρ = 1 hits is far larger than the 171 groups per trial the finder keeps.
  Consequence: neither the model nor the finder enumerates distinct hit sets; the finder samples configurations with its
  own (hit-pair seed) measure and refits them. A distinct-set count is therefore not the finder's counted object, and
  hypothesis A.1 (b) (basin volume per distinct set) cannot be tested as written.

## 2. Verdict measurement (replaces M_G): M_T, the per-configuration refit transfer
Same campaign design (frozen ensemble, c1.pu1, 16,000 trials, 10,000 configurations per trial, fresh seeds), no basin
volumes. For every configuration: the fixed-ribbon flags (measurement (i), unchanged) and the refit-map flags (map of
A.2, unchanged: the finder's refit from (n, a) of θ, R04 with the aligned cuts). P_refit(r) = fraction of configurations
whose refitted candidate passes r. Hypothesis H_T: *the finder's count follows the refitted configurations, i.e. the
residual is the change of the width fall caused by the finder's refit (and axis/window recentring) of a plane.*
  ln r̂(r) = ln r(R04) + ln[B_model(r)/B_model(R04)] − ln[P_refit(r)/P_refit(R04)],   r = R05, R06;
σ_T(r) = event-bootstrap error of ln[P_refit(r)/P_refit(R04)] (2,000 replicas). **The criterion of A.3 is unchanged**
(sign; |ln r̂ − ln r_obs| ≤ 2√(σ_T² + σ_tot,obs²); |ln r̂| ≥ 2σ_T; both rungs; σ_T(R06) ≤ 0.12, else "insufficient
precision").
Eligibility (C2, applied without a separate run): the campaign uses fixed N_IP2 ≥ 5 and stores the per-column refit
counts of configurations with fixed N_IP2 = 5 separately; if they are > 5 % of P_refit(R04) the N_IP2 ≥ 5 reading is
the verdict reading, otherwise N_IP2 ≥ 6 (rule of A.3, R04 only). Both readings are reported.
Diagnostics (no verdict): measurement (i) / D3 (C(R06)); D4' = P_refit(R04)/P_fix(R04); the s = 3 versions.
The validation finding of §1 is reported in the ticket as a result.

## 3. Implied redesign if CAUSE FOUND (form fixed now)
ρ(r) := [P_refit(r)/P_fix(r)] / [P_refit(R04)/P_fix(R04)] at R04-R06 on development hits; ρ(r) := ρ(R06) for R07-R09;
ρ_s3 likewise with N_2S2 ≥ 3; B(r) = N_cfg·ρ(r)·(model of A.4), N_cfg the frozen R04-R05 GLS normalisation applied to
P_real(r)·ρ(r); inputs that use the finder's refit arithmetic labelled "not independent" (M14).
