# Fix report R3: Stage-4 plan (`acts/stage4/plan.md`), C001 quirks theory track

Fixer R3, 2026-10-13.

**Inputs:**
- `review/REVIEW_S4PLAN_R3.md` (0 A, 4 B, 9 C), with the reviewer's scratch in `data/acts_stage4/review_r3/`;
- the user decisions of 2026-10-13 (LOG.md):
  - D4-10 (a′), D4-13, D4-14 and D4-15 approved;
  - the scope is chosen by the user after G2a;
  - each production run ≲ 1 day of wall time, several runs allowed, each approved by the user;
  - development and gate runs are not capped but are reported;
  - resources: the Mac plus an optional GCP free-trial VM (never upgraded).

**What was done:**
- The plan was edited in place.
- New arithmetic script: `acts/stage4/probes/f3r_campaigns.py`. Outputs: `data/acts_stage4/fix_r3/f3r_campaigns.json`
  and `f3r_split.json`.
- **Compute: < 0.001 CPU-h** (arithmetic and a 2 × 10⁶-draw log-normal Monte Carlo, in the TT env).
- No acts-env use, no install, no simulation, no signal look.
- Public documentation was read once (the GCP free-trial features page) to tag the cloud terms. No cloud account, project
  or resource was created.

## Items

| # | Finding | Status | What changed (plan section) |
|---|---|---|---|
| B-1 | No pre-defined scope fits the ≲ 1-day cap; G2a "2-4 s → proceed" breaks it; ρ = 3, the timeline and the §10 thresholds are inconsistent | **RESOLVED** | See *B-1 detail* below the table. |
| B-2 | The fallback's primary limit at R_E is empty where the fallback applies; the R_A-R_D limits have no rule (best-of risk) | **RESOLVED (design); user acknowledgement pending (D4-17)** | See *B-2 detail* below the table. |
| B-3 | 0.15 + 0.15 makes joint tightening routine (combined B₈₄ 0.41); four branches undefined | **RESOLVED** | See *B-3 detail* below the table. |
| B-4 | p(χ²_core) > 10⁻³ sits in the counting rungs, whose extrapolation and T1 use counts only | **RESOLVED, option (a)** | See *B-4 detail* below the table. |
| C-1 | Stale PROPOSED markers | RESOLVED | Header; §1.4 (D4-15); §2.2 (D4-14); §7 D4-10 block; §10 rows D4-10, D4-13, D4-14, D4-15; §11 item 4 (D4-13 in scope; the fallback limit uses the pyhf workspace); figure list. Still marked pending: the fallback acknowledgement (D4-17) and the scope/machines (D4-16, at G2a). `grep PROPOSED` now hits only the historical header sentence. |
| C-2 | Storage and the f_s rule | RESOLVED | §4.1 step 3b: (a) ≈ 4 GB + (b) ≥ 20 GB (1 % of ≥ 10⁵ loose sets × 2 kB × 10⁴ trials), ≈ 24 GB at the full B2 (≈ 5 GB with C1). §6.3 has a new row; total 8 → **≈ 32 GB** (≈ 10 GB with C1). Pre-declared strata: f_lo below N_IP2 ≥ 6, f_hi ≥ 0.1 at or above it; if 0.1 is too slow, G2b fails and the user is asked. |
| C-3 | The w_core "strong (M)" cell compares PU at full density with signal at Fatras density | RESOLVED | §2.6 cell: "strong on PU (M); signal at the normalised density E", with the MAD-breakdown argument (≈ 15-17 in-band IT + PS PU crossings vs ≈ 20 signal hits). New §12 risk 2b. |
| C-4 | Number nits | RESOLVED | (1) "+ B2 at its own t₂" removed (§0, §6.2, §10); the 560-1 700 range already includes B2 at t₂ = 8 t₁. (2) "167-228 s" → "159-228 s (per-trial sums of the stage times; median 211)" in §0 and §2.4. (3) §4.1 now says "≈ 1.1 × 10⁵ (median; q90 1.2 × 10⁵)". (4) "Distinct" is qualified as 2-mrad-merged wherever the probe count is used (§0, §2.4 table and text, §4.1); `n_distinct_hitsets` is a copy of `n_kept`. (5) The `f2r_profile.py` docstring is stale; this is noted in the plan header. The probe file is left unchanged as the audit record, per the file rules. |
| C-5 | `FIX_S4PLAN_R2.md` says D4-1 is "re-asked at G2a"; the plan asked only at t₁ > 4 s | RESOLVED (superseded) | G2a now **always** asks the user (§0, §6.2, §10 D4-1/D4-16, §11). The R2 fix record is left as history. |
| C-6 | N_L2 vs N_IP2/N_2S2 naming drift | RESOLVED | §2.2 item 5 states the mapping: N_L2 = N_IP2 + N_2S2; barrel N_IP2 ≤ 7, N_2S2 ≤ 3; N_L2 is kept as a diagnostic because the probes stored it. The T_seed stability rule (§2.2 item 4) and G3 (iv) now use the ladder variables. |
| C-7 | Failure-path interplay | RESOLVED | The G3 box lists the fourth branch (\|z\| < 2 with a significant trend → slope into σ_ln, and into the central value if the trend is anti-conservative). §4.1 step 4 adds that each family's test governs its own rungs and that corrections compound along the cumulative ladder, never cancelling. |
| C-8 | The χ²_core ordering justification is not about cut power | RESOLVED | §2.5 item 3 is rephrased as a per-trial PU-only statement. Width: 0 full-density trials with a candidate < 9.4 mm at N_L2 ≥ 9. χ²_core: 1.5 % per candidate, but 286-348 (p > 10⁻³) and 14-15 (p > 0.05) candidates per trial remain (`review_r3/r3_chi2core_p.json`). |
| C-9 | ρ = 3 has no timing gate | RESOLVED | ρ = 3 is only the optional campaign C5 (offered only if T3 fails), behind gate G2c (≥ 5 trials; must fit one day). See B-1. |

### B-1 detail: the campaigns and the gates

**The campaigns.** §6.2 has a new subsection, "Production campaigns under the one-day cap". It defines C1-C4 plus an
optional C5, with fixed contents, frozen with `WP_RULE.md`:
- **C1 core** = review R3's S-cap without the k = 1 guns, which are C′ and therefore development;
- **C2** B1 → 12 000, B2 → 3 000, C → 5 × 5 000;
- **C3** B1 → 2 × 10⁴, B2 → 5 000;
- **C4** the rest of A2, A3, A4, A5 → 20 points;
- **C5** ρ = 3.

Each campaign is costed vs t₁ (t₂ = 8 t₁ until G2b), with walls on the Mac (7 workers ≈ 168 CPU-h/day) and on Mac +
cloud (8 vCPU × s_c = 0.6, best whole-block split). The table lists the largest t₁ per campaign and the number of
one-day runs. A campaign over one day at the measured speed is split into pre-defined sub-runs. The same table, condensed,
is in §0.

**The gates.**
- G2a: measure t₁, re-evaluate the table, and **always ask the user**. No automatic branch.
- G2b: one criterion, t₂ ≤ t₂,max of the user's chosen campaigns. That number is computed at G2a; it is identical in
  §6.2, §10 and §11.
- G2c: ρ = 3, only before C5.

**Text aligned across sections:**
- ρ = 3 removed from every default (§0, §4.1 step 2, §5, §6.2, V4-7, D4-5). "WP rung not reachable at ρ = 2" now goes
  directly to rung factorisation (T3); C5 is offered only if T3 fails.
- The T1 lever-arm fallback is defined without ρ = 3.
- §6.4 "≈ 70 h → ≈ 30 h" corrected; the PC is not in the user's resource list.
- §11: production = user-approved campaigns one at a time; the timeline counts one-day runs; dev/gate CPU-h are listed
  and not capped.
- §12 risk 1 rewritten, plus new risks 10 (cloud) and 11 (thin reach with C1).
- §2.5 item 11: the rule is applied on the union of campaigns, and continuation is never decided on signal.

**The reach of the minimal option is stated** (§0, §6.2, §2.6). The thinning reach is 4.8 × 10⁻¹⁰ per trial with C1,
1.6 × 10⁻¹⁰ after C2 and 9.5 × 10⁻¹¹ after C3. The per-category requirement is 3.3 × 10⁻¹⁰ with the R3 split.

### B-2 detail: the fallback

§2.6 was rewritten.

**Admissibility, per hypothesis.** It is computed from the published Stage-3 truth Λ_R(m) and βγ_IT(m), the analogue of
a mass window centred on the hypothesised mass:
- width rungs with Λ ≥ Λ_R·2^{(k+1)/2};
- dE/dx rungs with e_min ≤ R_BB(βγ_IT)/1.25, where R_BB is the PDG Bethe ratio, computed and cited at the freeze.

**The fallback selection.** r_fb(m, Λ, c) is the tightest ladder selection with only the inadmissible thresholds relaxed.
There are ≤ 20 such selections, weighted in-job.

**The primary result.** It is r*_c if that rung exists and is admissible; otherwise it is r_fb.

**What is forbidden.** Per-point best-of is forbidden. Limits are computed only at the primary selection. R_A-R_E are
ε/B tables only.

**What the fallback can and cannot claim** is listed in §2.6. The plain expectation: at Λ ≲ 1 keV and E200 it gives ε, B
and the observables, and essentially no exclusion.

**Alternatives for the user** (D4-17): (ii) R_E everywhere; (iii) split-template.

### B-3 detail: the budget split

**Split 0.11 + 0.11** (§2.5 item 5). Justification (`f3r_split.json`): the combined/per-category B₈₄ ratio at
σ_ln = 2.3 is 2.71 (independent), 2.50 (correlation 0.5) and 2.0 (fully correlated). So 0.3/2.71 = 0.1107. The combined
B₈₄ is then 0.298 / 0.275 / 0.22. It exceeds 0.3 only for σ_ln ≳ 2.4 with nearly equal categories (0.32 at 2.5, 0.38 at
3.0).

**The combined guard stays, now applied to the pair:** a pair is accepted only if it and every component-wise tighter
pair pass. The branches are deterministic:
1. tighten the category with the larger B₈₄,c (tie → SR-G);
2. a category at its tightest rung R stays and the other moves;
3. if (R, R) fails, both categories go to the fallback;
4. if only one category has a WP, the combined check is not applied; that category alone claims background-free, the
   other goes to the fallback, and the likelihood stays two-bin at the per-bin primary selections.

The loop terminates in ≤ 44 steps.

**Dependent numbers updated:**
- §2.6: median ≲ 0.011, P_PU ≲ 3 × 10⁻¹⁰;
- §11 G3: B₈₄,c ≤ 0.11;
- D4-4.

### B-4 detail: χ²_core

p(χ²_core) > 10⁻³ is now the head of the χ²_core family (§2.5 item 3). The counting rungs are pure counts. There are now
**23 rungs**, and "22 × 22" becomes "23 × 23".

§4.1 step 3b:
- the counting row notes that T1 is computable from counts;
- the w_core/χ²_core row covers all three p rungs;
- the core is **re-centred per subset**, with χ² summed over per-hit moments (per-interaction pre-summed moments are not
  enough). The per-hit storage already provides this;
- subsets are conditional on N_IP2 ≥ 7, now without a χ² pre-filter. Their number per ρ = 2 trial is unmeasured (the
  probes stored N_L2), so G2b times it, including the weights.

## Campaign table (`f3r_campaigns.json`; CPU-h, t₂ = 8 t₁; wall in h for the Mac / for Mac + cloud)

| t₁ (s) | C1 | C2 | C3 | C4 | C5 | C1-C4 | one-day runs, Mac / Mac + cloud |
|---|---|---|---|---|---|---|---|
| 2 | 72 (10 / 6) | 88 (13 / 8) | 56 (8 / 5) | 80 (11 / 7) | 38 (5) | 296 | 4 / 4 |
| 5 | 114 (16 / 10) | 154 (22 / 14) | 110 (16 / 10) | 144 (21 / 13) | 83 (12) | 522 | 4 / 4 |
| 8 | 157 (22 / 13) | 220 (31 / 20) | 163 (23 / 16) | 209 (30 / 18) | 128 (18) | 748 | 6 / 4 |
| 10 | 185 (26 / 16) | 264 (38 / 24) | 198 (28 / 20) | 252 (36 / 22) | 158 (23) | 899 | 8 / 4 |
| 20 | 327 (47 / 28) | 483 (69 / 42) | 376 (54 / 38) | 466 (67 / 43) | 308 (44) | 1 652 | 11 / 8 |

**Largest t₁ for one day, Mac / Mac + cloud:**
- C1: 8.7 / 16.9 s;
- C2: 5.6 / 10.2 s;
- C3: 8.2 / 12.3 s;
- C4: 6.1 / 11.0 s;
- C5: 10.6 s (Mac only).

**G2b t₂,max for C1:**
- at t₁ = 5 s: 136 s on the Mac, 297 s on Mac + cloud;
- at t₁ = 8 s: 84 s and 279 s.

## Item 2 of the task: cloud execution (§6.5, new)

§6.5 covers:
- the account terms, tagged VERIFIED or UNVERIFIED;
- the VM suggestion: t2d-standard-8 (no SMT), with c2d-, n2d- or e2-standard-8 as fallbacks, on Ubuntu 24.04 or
  Debian 12;
- linux-64 pixi locks as separate projects (`acts/stage4/cloud/{acts,tt}/pixi.toml`, pyacts 48.0.0 manylinux wheel),
  solved on the Mac with `pixi lock` and installed `--frozen` on the VM;
- restartability: a resumable runner and jobs ≲ 30 min; a standard VM is recommended, and Spot is UNVERIFIED on a trial;
- data volumes: in ≲ 1 GB; out ≈ 3 / 12 / 12 / 2 GB for C1-C4;
- validation: (1) the per-vCPU speed s_c measured first; (2) same-machine bit identity; (3) the finder on Mac-produced
  inputs, identical within 10⁻⁶ for ≥ 99 % of candidates; (4) the V4-8 statistical chain check;
- budget burn: ≈ $31 for C1 only, ≈ $68 for C1-C4, ≈ $120 for C1-C4 split plus C5, against $300. The binding limit is
  the 90-day window.

All prices and the 8-vCPU limit are UNVERIFIED. The $300/90-day terms, the GPU and quota restrictions and the
end-of-trial behaviour are VERIFIED from the GCP free-trial features page.

## Consistency check (step 4 of the task)

- **Numbers checked, same in every section:**
  - the cap: 168 / ≈ 280 CPU-h;
  - the C1 limits: 8.7 / 16.9 s;
  - the full scope: 4 runs up to 5.6 / ≈ 10 s;
  - the split: 0.11;
  - the rung count: 23;
  - the reach: 5 × 10⁻¹⁰ (C1) → 10⁻¹⁰ (C3) against 3 × 10⁻¹⁰;
  - disk: ≈ 32 GB.

  Sections covered: §0 (summary and compute), §2.2, §2.5, §2.6, §4.1, §5, §6.1-6.5, §10 (D4-1, 4, 5, 8, 10, 13-17),
  §11 (deliverables, gates, production, timeline), §12.
- **G2a/G2b/G2c wording** is identical in §0, §6.2, §10 and §11.
- **Final grep:** no "PROPOSED" outside the historical header sentence; no "3 days wall"; no "≤ 2 s target"; no
  "B₈₄,c ≤ 0.15" outside the R3 justification of the split; no "22 × 22".

## Needs user input

1. **D4-16, at G2a:** the scope and machines (C1 only vs C1-C4, Mac vs Mac + cloud), from the table at the measured t₁.
2. **D4-17, before the freeze:** acknowledge the redefined fallback. Recommended: (i) the hypothesis-admissible rung.
   Alternatives: (ii) R_E everywhere; (iii) split-template.
3. **If the cloud is wanted,** the user creates the free-trial account (never upgraded). The first cloud step measures
   s_c, and the 8-vCPU limit and Spot availability are checked in the console.
