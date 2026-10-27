# Critical review R4 (narrow verifier): Stage-4 plan after fix R3 (`acts/stage4/plan.md`), C001 quirks theory track

Reviewer: S4PLAN-R4, a fresh critical reviewer, 2026-10-13. Role: `jfc/src/agents/critical_reviewer.md`; methodology
`01-core.md` and `03-review.md` §6.

Classification, as in R2/R3:
- **A** blocks or invalidates;
- **B** must be fixed in the plan before the user decides and before `WP_RULE.md` is frozen;
- **C** is minor.

The verdict is PASS only with 0 A and 0 B. Approved decisions are not reopened.

**Scope.** This round checks whether review R3's B-1…B-4 and C-1…C-9 are genuinely resolved, and whether fix R3
introduced a new A or B.

**Orchestrator update received during the review** (taken into account):
1. D4-17 option (i) is **approved**.
2. The cloud is **dropped**: Mac only.
3. New deadline: everything, Stage 5 included, must be done by Saturday night 2026-10-17. That is ≈ 4.5 Mac days in total.
   This is answered in §5. The schedule itself is the next fixer's task.

**Inputs read:**
- `plan.md` (1754 lines; §0, §2.2, §2.5, §2.6, §4.1, §4.2 guns/NI, §5, §6, §10-§12 in full);
- `FIX_S4PLAN_R3.md`, `REVIEW_S4PLAN_R3.md`;
- `probes/f3r_campaigns.py`, `data/acts_stage4/fix_r3/f3r_campaigns.json`, `f3r_split.json`;
- the LOG.md user decisions;
- `sim/stage3/results/P2.json` (Λ_R per mass);
- `data/acts_stage4/review_r1_constructive/r1c_signal_handles.json` (βγ_IT).

**Independent checks** (≈ 0.001 CPU-h, TT env read-only, no acts env, no finder run, no ρ = 2, no signal; scratch in
`data/acts_stage4/review_r4/`):
- `r4_checks.py` → `r4_checks.json`:
  - the campaigns re-implemented from the §6.2 text (not by importing f3r): CPU-h, Mac and Mac + cloud wall, the largest
    t₁ from a root find, and the G2b t₂,max;
  - the budget-split ratio by an independent Monte Carlo (seed 4242, 4 × 10⁶ draws) and by numerical quadrature;
  - the reach and the cloud burn;
  - a Bethe-ratio ESTIMATE for the dE/dx admissibility. Its Si constants are recalled from memory, so they are UNVERIFIED
    and used for the reviewer's cross-check only.
- `r4_deadline.py` → `r4_deadline.json`: the deadline fit (§5).

---

## 1. Status of the R3 items

| R3 item | Verdict | Evidence / residual |
|---|---|---|
| **B-1** no scope fits the cap | **Resolved** | See *B-1 detail* below the table. Residual: new **B-1** (C′) and C-1 (cloud now dropped). |
| **B-2** fallback empty at R_E; best-of risk | **Resolved (design); D4-17 (i) now approved** | See *B-2 detail* below the table. Residuals: C-2, C-3, C-4. |
| **B-3** budget split | **Resolved** | See *B-3 detail* below the table. Nit: C-5. |
| **B-4** χ²_core inside the counting rungs | **Resolved** | See *B-4 detail* below the table. |
| C-1 stale PROPOSED | Resolved | `grep PROPOSED` hits only the historical l.18. D4-17 is now approved, so its "pending" marks are stale again (C-1 below). |
| C-2 storage | Resolved | §6.3 total 1.0 + 3.4 + 1.7 + 0.2 + 24 + 0.4 + 0.8 = 31.5 ≈ 32 GB ✓. The f_lo/f_hi strata are pre-declared ✓. |
| C-3 w_core cell | Resolved | Tagged "strong on PU (M); signal E"; §12 risk 2b ✓. |
| C-4 number nits | Resolved | 159-228 s; q90 vs median; "2-mrad distinct" ✓. |
| C-5 to C-9 | Resolved | The N_IP2/N_2S2 mapping (§2.2 item 5) ✓. The G3 fourth branch and cross-family compounding ✓. The C-8 rephrase ✓. C5 is behind G2c ✓. |

**B-1 detail: the campaigns.** All rows reproduce to ±1 CPU-h (§2), and so do the largest t₁ values.
- G2a always stops for the user, in §0, §6.2, §10 D4-1/D4-16 and §11.
- G2b has one criterion, t₂ ≤ t₂,max of the chosen campaigns, worded identically in §0, §6.2, §10 and §11.
- ρ = 3 is only the optional C5, behind the T3 rule and G2c (§0, §4.1 step 2, §5, §6.2, V4-7, D4-5, §11).
- The C1 reach is stated honestly: 4.8 × 10⁻¹⁰ per trial against 3.3 × 10⁻¹⁰ required, so the deepest rungs rest on
  rung factorisation and T3. This appears in §0, §2.6, §4.1, §6.2 and §12 risk 11.
- No "3 days wall", "≤ 2 s target", "t₁ > 4" or "> 20 s" text is left.

**B-2 detail: the fallback.** The admissibility rule:
- uses only the Stage-3 truth Λ_R(m) and βγ_IT(m), a ℓ_max ∝ Λ⁻² scaling and a Bethe ratio;
- uses no detector-level efficiency, toy or limit;
- is deterministic;
- is non-empty where needed: k_adm = 0 means no width cut, and at E200 there is no dE/dx cut.

Λ_R ranges over 0.427-0.941 keV (`P2.json` → `edges.*.lower_lmax_RIT_closed`) ✓. 2^{5/2}·Λ_R gives 2.4-5.3 keV and
2·Λ_R gives 0.86-1.9 keV ✓.

The primary is r*_c if it is admissible, else r_fb, which is a deterministic rule with no comparison of ε or limits. Limits
are computed only at the primary selection, and R_A-R_E are ε/B tables only (§2.6 deliverables 1-2; §11 item 3) ✓. This is
signal-blind in the sense required: it is a per-hypothesis window fixed from generator/truth kinematics before any
detector-level look, like a mass window.

**B-3 detail: the budget split.**
- The ratio is 2.706 (independent Monte Carlo), 2.709 (quadrature), 2.509 (correlation 0.5) and 2.002 (fully correlated),
  against the plan's 2.71 / 2.50 / 2.0 ✓.
- 0.3/2.709 = 0.1107 ✓; median 0.011 ✓; P_PU ≲ 3.34 × 10⁻¹⁰ per event ✓.
- These values are consistent in §0, §2.5, §2.6, §4.1, §6.2, §11 G3, §12 and D4-4.
- All four R3 branches are defined (§2.5 item 5): the category at R, the no-WP category, termination in ≤ 44 = 2(R − 1)
  steps with R = 23, and the guard on the pair path ✓.

**B-4 detail: χ²_core.**
- The counting rungs are pure counts (§2.5 item 3), and p(χ²_core) > 10⁻³ heads the χ²_core family.
- There are 4 + 4 + 3 + 3 + 9 = 23 rungs ✓, and "23 × 23" ✓.
- In the §4.1 step-3b table, the w_core/χ²_core row covers all three p rungs, with the core re-centred per subset from
  per-hit moments. T1 is computable from counts.
- G2b times the in-job weights "for every rung family and the fallback selections" (§11 G2b; §4.1 "G2b times it") ✓.

## 2. Re-derivation of the campaign table (`r4_checks.json`)

Format: CPU-h, then (Mac wall h / Mac + cloud wall h). The plan's values are in brackets where they differ.

| t₁ | C1 | C2 | C3 | C4 | C5 | C1-C4 |
|---|---|---|---|---|---|---|
| 2 | 72 (10/6) | 88 (13/8) | 56 (8/5) | 80 (11/7) | 38 | 296 |
| 5 | 114 (16/10) | 154 (22/14) | 110 (16/10) | 144 (21/13) | 83 | 522 |
| 8 | 157 (22/13) | 220 (31/20) | 163 (23/16) | 209 (30/18) | 128 | 748 |
| 10 | 185 (26/16) | 264 (38/24) | 198 (28/20) | 251 [252] (36/22) | 158 | 899 |
| 20 | 327 (47/28) | 483 (69/42) | 376 (54/38) | 466 (67/43) | 308 | 1652 |

**Largest t₁ for one day** (root find; the plan floors these to a 0.1 s grid):

| | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|
| Mac (s) | 8.79 | 5.64 | 8.29 | 6.11 | 10.68 |
| Mac + cloud (s) | 16.92 | 10.27 | 12.37 | 11.03 | — |
| Plan (Mac / Mac + cloud) | 8.7 / 16.9 | 5.6 / 10.2 | 8.2 / 12.3 | 6.1 / 11.0 | 10.6 |

All agree ✓.

**G2b t₂,max for C1:**
- t₁ = 5 s: 136.6 s on the Mac and 297 s on Mac + cloud (plan: 136 / ≈ 300) ✓;
- t₁ = 8 s: 84.1 s and 279 s (plan: 84 / 279) ✓.

**Other numbers:**
- Burn $30.8 / $68.4 / $119.9 ✓.
- Reach 4.77 × 10⁻¹⁰, 1.59 × 10⁻¹⁰ and 9.5 × 10⁻¹¹ ✓.
- Direct reach 1.5 × 10⁻⁴, 6.25 × 10⁻⁵ and 3.75 × 10⁻⁵ ✓.

**Reconciliation with the 330 CPU-h of the recommended scope at t₁ = 2 s.** The campaigns sum to 296: A5 is 32.2 vs 30,
validation is 30 vs 40, and C′ (≈ 20) is moved out of the campaigns. The plan discloses this (l.1243-1245). The last item
is the subject of B-1.

## 3. Category A

None.

## 4. Category B

### B-1. C′ (topology guns and toys) was reclassified by the fixer as "development, not capped" although it produces production inputs to the B sum, and its with-PU part is costed as a flat 15-20 CPU-h, independent of t₁.

**Evidence.**
- C′ supplies P(pass | topology) for B_corr, B_conv, B_V0, B_NI and B_DIF. These enter the WP rule's B(r) (§2.5 item 4;
  §4.2 "Full B sum"). They are physics outputs of the final result, not development or gate runs.
- The user's rule exempts "dev/gate/test runs" only. R3 B-1 item 4 asked for this to be put to the user. Instead the fixer
  classified C′ itself:
  - §0 l.150;
  - §5 l.1182;
  - §6.2 l.1244, l.1331;
  - §11 item 5: "development, not capped, reported", which means no approval as a production run.
- Several C′ samples carry PU:
  - the PV pair gun is "without and with PU, 10⁵ events" (§4.2 l.1114-1115);
  - the NI toy "is run with PU overlaid" (§4.2);
  - the §5 table says "10⁵ each, with and without PU … mostly no".

  The with-PU event count is never fixed. Each with-PU event costs (4.7 + t₁) s of PU chain plus finder, like an SM event.
  - 10⁴ with-PU gun events cost 19 / 27 / 41 CPU-h at t₁ = 2 / 5 / 10 s.
  - 10⁵ cost 186 / 269 / 408 CPU-h, i.e. 1.1-2.4 Mac days, uncapped and unapproved.

  §4.2 still says "≈ 10-15 CPU-h (no PU, fast)", which contradicts "with PU" in the same paragraph.

**Required fix.**
1. Fix the with-PU event counts of the PV pair gun, the NI toy and the DIF toy.
2. Cost them as a function of t₁, as for the C block.
3. Treat C′ as production: put it inside C1 (as review R3's S-cap did, ≈ 12 CPU-h for the no-PU part plus the with-PU part
   at t₁), or define it as its own capped, user-approved run. Alternatively, record an explicit user ruling that C′ counts
   as development.
4. Make §0, §4.2, §5, §6.2 and §11 consistent.

Under the new deadline this also matters for the schedule (§5).

## 5. Fit to the 4.5-day deadline (orchestrator request; Mac only, ≈ 168 CPU-h per day; t₂ = 8 t₁ until G2b)

**Assumed budget:** ≈ 1 day for finder development and gates, ≈ 1.5 days for analysis, reviews and Stage 5. That leaves
**≈ 2 Mac days ≈ 336 CPU-h of production wall**, with no margin for a rerun.

The gate and development runs also occupy the Mac inside the development day:
- G1 2, G2 6 and C′ ≈ 20 CPU-h (no-PU part only, see B-1);
- the G3 pilot, 13 / 19 / 26 CPU-h at t₁ = 2 / 3 / 5 s;
- in total ≈ 41 / 45 / 54 CPU-h, i.e. 6-8 h of wall.

Source: `r4_deadline.json`. Wall times are in Mac days.

| t₁ | C1 | C2 | C3 | C4 (A3 + A4 included) | C4 without A3, A4 ("C4′") | C5 |
|---|---|---|---|---|---|---|
| 2 s | 72 (0.43) | 88 (0.52) | 56 (0.33) | 80 (0.47) | 63 (0.38) | 38 (0.23) |
| 3 s | 86 (0.51) | 110 (0.65) | 74 (0.44) | 101 (0.60) | 79 (0.47) | 53 (0.31) |
| 5 s | 114 (0.68) | 154 (0.92) | 110 (0.65) | 144 (0.86) | 110 (0.65) | 83 (0.49) |

**Realistic sets (≤ 2 days):**

| t₁ | Fits | Defer |
|---|---|---|
| 2 s | C1-C4 = 296 CPU-h = **1.76 d** fits, with ≈ 6 h margin. Safer: C1 + C2 + C4′ = 1.33 d, then C3 (0.33 d) only if the gates went smoothly | C5; A3 and A4 if the margin is needed |
| 3 s | C1 + C2 + C4′ = **1.63 d** (C1-C4 = 2.21 d does not fit) | C3, A3, A4, C5 |
| 5 s | C1 + C2 = **1.60 d**. Alternatively C1 + C4′ = 1.33 d (grid coverage instead of PU reach). C1 + C2 + C4′ = 2.25 d does not fit | C3, C4 (or C2), A3, A4, C5 |

**Recommendation.** Defer, in this order: **C5 always** (it is a ρ = 3 rescue path, and its G2c gate costs time), then
**A3 toys**, **A4 material**, **C3**.

Keep **C1 + C2** as the core: C2 brings the thinning reach from 4.8 to 1.6 × 10⁻¹⁰, below the 3.3 × 10⁻¹⁰ requirement,
and adds the five SM samples. C4′ (the rest of the A2 grid plus A5 → 20 points) is the next priority.

Above t₁ ≈ 5 s, only C1 + one more campaign fits. At t₁ ≳ 8.8 s, C1 alone takes a full Mac day. At the measured 211 s
nothing fits: the deadline then depends entirely on the parallel speed-up work reaching ≲ 5 s.

**Caveats.**
- Running Stage-5 analysis on C1 while C2/C4′ run (light TT-level work) is what makes 1.5 days for analysis and review
  plausible.
- Each campaign needs the user's approval, so approval latency adds to the wall time.
- The plan's §11 timeline (3-4 days of implementation, 1-2 days post-production, 1-2 days of reviews) is incompatible with
  the deadline. The next fixer's schedule must replace it.

## 6. Category C

- **C-1. Documentation lag from today's user decisions.**
  - D4-17 (i) is approved: update §2.6 l.769, l.848-853, §10 D4-17 and FIX "needs user input".
  - The cloud is dropped. These are now obsolete and should be marked as such:
    - §6.5;
    - D4-8 (b);
    - the Mac + cloud columns and "largest t₁" values (§0, §6.2, §11 G2a, §12 risks 1 and 10);
    - G2b's Mac + cloud t₂,max;
    - "≈ 280 CPU-h".

    The sequencing gap (G2a is meant to see a measured s_c, but cloud set-up is gate 6, after G3) disappears with the cloud.
  - While §6.5 stood, it was acceptable:
    - VERIFIED and UNVERIFIED terms were separated;
    - the 8-vCPU limit and Spot availability were UNVERIFIED;
    - nothing implied creating resources;
    - "never upgrade" was respected.

    It never said explicitly that the account, project and VM would be created by the user. That is moot now.
- **C-2. βγ_IT(m) is not a "published Stage-3 quantity".** §2.6 l.780 and D4-17 call it published. It exists only in the
  constructive reviewer's probe (`r1c_signal_handles.json`, template events). Pre-declare its source:
  - Stage-3 truth, template half or the toy half;
  - median over which Λ (it is Λ-independent to ±4 %);
  - the script that computes it at the freeze for all 17 species-masses.

  Λ_R(m) is published (`P2.json` → `edges.*.lower_lmax_RIT_closed`), but it is non-monotonic in m (E800 0.737, E900
  0.652 keV, stat error ≈ 0.02). Pre-declare whether the per-mass value or the smoothed `edge_fits_in_m` is used, so that
  k_adm does not jump with noise.
- **C-3. Wrong βγ range.** The §2.6 table's "E500-E1500, IT median βγ 0.9-1.0" disagrees with `r1c_signal_handles.json`:
  E500 0.89-0.95, E1000 0.67-0.68, E1500 0.52-0.54, Ẽ500 1.07-1.08, E200 1.80-1.87.

  Reviewer Bethe ESTIMATE (`r4_checks.json`, Si constants UNVERIFIED) of R_BB:
  - 1.63 / 2.20 / 3.09 for E500 / E1000 / E1500, so e_adm = 1.3 / 1.6 / 2.0;
  - 1.08 for E200 and 1.41 for Ẽ500, so no admissible dE/dx level for either.

  So the §2.6 expectation "a loose level for E500-E1500" is roughly right (better for heavy E). However, **Ẽ500 gets no
  dE/dx rung**, which bears on "Ẽ500 at Λ ≳ 2 keV: plausible". Correct the range and add Ẽ500 to the "none" list. Also
  note that e_min is in units of the muon-gun MIP peak while R_BB is relative to the Bethe minimum; state the conversion
  at the freeze.
- **C-4. A mixed-admissibility branch is not stated.** At a point where r*_T is admissible and r*_G is not (or the reverse),
  the primary pair is (r*_T, r_fb,G). The combined guard of §2.5 item 5 was evaluated on (r*_T, r*_G). Say that the
  "exactly one category has a WP" branch applies: the background-free claim is made for the admissible category alone,
  and the other bin goes in at r_fb with its own B. One sentence suffices.
- **C-5. Unequal-category range.** "0.16-0.22 if the two categories are unequal" (§2.5 l.679): `f3r_split.json` also has
  0.125 (5 % ratio). Write 0.13-0.22.
- **C-6. Lean option (b) is not defined in campaign terms.** D4-1 still offers (b) lean and (c) (a) + all toys without a
  campaign breakdown under the cap. Either drop them (C1 = minimal supersedes lean) or map them onto campaigns.

## Verdict

**ITERATE.** 0 Category A, 1 Category B, 6 Category C.

R3 B-1…B-4 and C-1…C-9 are genuinely resolved. The campaign arithmetic, the split factor 2.71, the 3.3 × 10⁻¹⁰
requirement, the reach and the burn all reproduce independently. The one B was introduced by the fix: C′ was reclassified
as uncapped development without costing its with-PU part. It is a text and costing fix and needs no production, ρ = 2 or
signal run.
