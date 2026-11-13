# INV_STATS_BKG: Stage-4 statistics and background anomalies (C001 theory track)

Investigator, 2026-10-16. Scope: STAGE4_RESULTS.md §10 items 3, 4 and 5, plus the closure and zero-count checks the
orchestrator asked for (items 1-5 below). The signal-efficiency anomalies (§10 items 1, 2 and 6) belong to the other
investigator and are not covered here.

Inputs were read-only: `acts/stage4/analysis/*.py` (freeze `bce02b6f…`), `WP_RULE.md`, `WP_RULE_PC19.md`,
`analysis/inputs/ambiguities.json` (A06, A07, A08, A12, A19, A20, A28, D4, D5, D6) and
`data/acts_stage4/analysis/{C12_v1,C1_v1}/*.json`. Nothing frozen was edited.

The investigation scripts are in `acts/stage4/investigation/`. They import the frozen `stats.py` and `background.py`
read-only, and their outputs are in `data/acts_stage4/investigation/`. Total compute was about 10 CPU-min on 1-2 cores.

Tags: **[V]** reproduced from the frozen outputs or code. **[E]** re-evaluated here by patching single factors of the
frozen chains. These are estimates; exact numbers need the fixed pipeline to be re-run.

## Summary

| # | item | class | root cause (one line) | minimal fix | outputs that change |
|---|---|---|---|---|---|
| 1 | asymptotic CLs ≈ 2.7 × 10⁻⁴ of the toys at FB0/FB1 | **(ii) bug** (cross-check only) | `stats._model` NLL has no saturated offset. At b ≈ 10⁸, \|NLL\| ≈ 2.8 × 10⁹, so L-BFGS-B's relative ftol (2.2 × 10⁻⁹ → ΔNLL ≈ 6) stops the nuisance profile after 1 iteration. q̃ is then essentially unprofiled, and the limit becomes ≈ 1.96√b/s | `stats.py:161` subtract `n − n ln n` | `limits.json` → `expected_asymptotic` only (11 C12 / 7 C1 points). Primary toys unchanged |
| 2 | SR-T FB2 chain lacks p(R09 \| R06) (C12 only) | **(ii) bug** (conservative, but large) | `background.chain_factors` A28 "merge" branch: the merged joint tail of variable v may be measured on a population that already contains an **added** cut of v, and the factor of that cut is dropped. It fires only when that population reaches ≥ 10. **The same defect hits the SM rows at FB0/FB1(±e) in both C1 and C12** (Z(νν), W(τ_h), tt̄1ℓ, and through them all the proxies) | `background.py:348-366` restrict the merge search to `pops[:first[v]]` | `background.json` (columns_T FB2/FB2e, sm FB0/FB1/±e), `bsum_wp.json` FB0, FB1, FB0e*, FB1e*, FB2-T, **`limits.json` toys (primary) at 23 of 33 points** (×30-70 lower at FB0/FB1, ×3 at FB2-T). Ladder and WP decision unchanged |
| 3 | σ_ln model spread 1.97 → 4.76 with more statistics | **(i) correct per frozen rule**, with a (iii) note | Main (thinning-start) vs factorisation model. In C12 the main route credits a measured χ² conditional, p(R09 \| R06 ∧ R07) = 2/35 (C1: 0/12, which entered as 1). The factorisation route's merged χ² tail, 0/35, enters as 1 because the R08 zero has the same M and comes first in ladder order (§4.2: one bound per term). Spread = ln(P_fact/P_main) = ln 117 = 4.76 | none under the freeze (the central is the upper envelope, so this is conservative). Pre-register a policy for the future | — |
| 4 | closure ×1.500 (T1), ×1.606 (T1w), ×2.41 compounded | **(i) correct**, applied exactly once | `background.compounded` / `end_state` apply T1 to every column and T1w (missing lever arm: × max(r, 1) and \|ln r\| in σ_ln) to R05-R14, F0e and all FB. T1e is untestable, so it adds no factor. The factor is not re-applied in `wp.py`, SR-T summands, F1 rungs, SM or C′ | none | — |
| 5 | C′/SM zero-count bounds below R07 | **(i)** one bound per term, largest M, ties first in ladder order; M is the §4.2 population. Side findings: **(ii)** looper "low gun counts" (§7) not implemented (conservative, B₈₄ −15-30 %); **(iii)** C′ dE/dx and h/o factors are taken from C′_PU/B1 instead of C′₀ (§7) | the effective bound is ≈ 1.14·c/N_sample (M cancels against the start fraction). With the zero persisting, each term alone needs ×10⁵-6 × 10⁶ more events (10⁸-3 × 10⁹ per sample), and all bounded terms together need ×1.1-1.5 × 10⁷ | none for the rule | see §5 |

---

## 1. Asymptotic CLs ≈ 2.7 × 10⁻⁴ × toys (STAGE4_RESULTS §10.3)

**Facts [V].**
- At all 11 failing C12 points (7 in C1), r_fb = FB0 or FB1, b ≈ (5.7-8.8) × 10⁷ per bin, and the workspace σ_ln =
  ln(B₈₄/B_med) = **0.83-1.12**. The hypothesis that σ_ln = 5-8 drives the failure is therefore wrong: those are the
  per-term ladder σ_ln, not the per-bin σ used in the likelihood.
- The asymptotic median equals the **unprofiled** Poisson limit 1.96√b/s to within 0.89-1.20 at every failing point
  (`inv_asym_C12_v1.json`, field `noprofile_1p96sqrtb_over_s`). The near-constant ratio to the toys is then ≈ 1/(√b·σ)
  ≈ 10⁻⁴, as observed.

**Mechanism [V]** (`inv_asym_mech.log`, E200 0.45 keV):
- `_model.nll = Σ(λ − n ln λ) + ½Σα²` (`stats.py:161`) carries the full n ln n term, so |NLL| ≈ 2.8 × 10⁹.
- scipy L-BFGS-B stops when ΔNLL/|NLL| < factr·eps = 2.2 × 10⁻⁹, i.e. ΔNLL < 6.2.
- Near the crossing (μ ≈ 2 × 10⁶, μs ≈ 2 × 10⁴), the whole profile gain is (μs)²/2b ≈ 2.3 < 6.2. The optimiser takes one
  step (α_G = −0.00038 instead of the optimum −0.00020) and stops. Frozen q̃ = 3.48, where the correct profiled q̃ is ≈ 0.
  CLs therefore crosses 0.05 at the unprofiled μ.
- At μ ≥ 2 × 10⁷ the gain is ≫ 6 and the profile converges. q̃(μ) is thus non-monotone. Whether the ×4 bracketing grid
  in `expected_limit_asymptotic` (`stats.py:193-198`) lands on the broken or the working branch depends on s. This is why
  the failing set looks random (and differs between C1 and C12), while all failures are at FB0/FB1, where b ≳ 5 × 10⁷.
  At FB2-FB4, b ≈ 10⁶ and ftol·|NLL| ≈ 0.03, which is harmless.

**Fix (`stats.py:161`).**
```python
        sat = np.where(n > 0, n - n * np.log(np.maximum(n, 1e-300)), 0.0)        # saturated offset (pyhf-equivalent)
        return float(np.sum(la - n * np.log(la) - sat) + 0.5 * np.sum((al - aux) ** 2))
```
An alternative is `options=dict(ftol=1e-15)` in both `minimize` calls (`stats.py:169, 172`).

**Verified [V]:** with the offset, asymptotic/toys = **0.81-1.05 at all FB0/FB1 points** and 0.21-1.05 over all 33 points
(C1: 0.38-1.05). The remaining 0.2-0.5 at FB2-FB4 (σ_ln 1.9-4.1) is the genuine difference between the asymptotic and
the hybrid-toy statistic, not a bug.

**Impact:** only `expected_asymptotic` in `limits.json`, plus the ⚠ marks and §10.3 of the report. The primary toys
are untouched. D6 ("agrees with pyhf to 10⁻⁴") was evidently validated only at small b.

## 2. SR-T FB2 chain: the A28 merge-population defect (§10.4), and its SM twin at FB0/FB1

**Code path [V]** (`background.chain_factors`, `background.py:335-378`). Variables are added in ladder order. A cut q of
variable v is measured as N(P ∧ q)/N(P ∧ q′) on the tightest population in `pops` with N(P ∧ q′) ≥ 10. If there is
none, all earlier factors of v are dropped (l. 367) and one joint factor N(P ∧ q)/N(P) is taken on the tightest P in
`pops` with N(P) ≥ 10 (l. 366).

That search runs over **all** of `pops`, including the populations that already contain an **added** cut of v. If such
a population has ≥ 10 entries, the "joint tail" becomes the conditional p(q | … ∧ q_first), while the factor
p(q_first | …) has just been deleted. This contradicts A28 ("its whole tail beyond P is ONE joint factor N(P & q)/N(P)")
and the docstring ("MERGED into one joint factor").

**SR-T FB2 (C12) [V].** Start R06 ∧ BTL (M = 1 874 groups):
- p(R09 | R06) = 16/1 874;
- p(R10 | R06 ∧ R09) = N/16, with N < 10;
- at R11 no population with the R10 cut reaches 10, so the code merges. It drops 16/1 874 and the R10 factor, finds
  P = R06 ∧ R09 (16 ≥ 10), and enters p(R11 | R06 ∧ R09) = 0/16 → bound 1.14/16 = 0.071.
- Correct: p(R11 | R06) = 0/1 874 → 1.14/1 874. This is identical to keeping 16/1 874 × 1.14/16, so both readings agree.

**Why only with C2B:** in C1, N(R06 ∧ BTL ∧ R09) = **6 < 10**. The search fell through to R06 (0/782), which is
correct. C2B lifted it to 16 ≥ 10, which switched on the defective branch. The SR-G FB2 chain never merges (126 ≥ 10
at every step), so it is unaffected. The whole effect is the ≥ 10 population fallback flipping with statistics.

**Scan of every merged factor** (587 in C1, 585 in C12, `inv_*` scan): the same defect appears in the
**SM rows at FB0, FB1 and their e variants, in both C1 and C12**:

| SM row | frozen merged factor | correct (start population) | B frozen → fixed [E] |
|---|---|---|---|
| Z(νν) FB0 | p(R11 \| R04 ∧ R09) = 0/29 | 0/93 404 | 3.6 × 10⁷ → 1.1 × 10⁴ |
| Z(νν) FB1 | 0/10 | 0/21 741 | 2.6 × 10⁷ → 1.2 × 10⁴ |
| W(τ_h) FB0 / FB1 | 1/30, 0/14 | 1/78 439, 0/18 436 | 7.4 / 5.1 × 10⁶ → 2.9 / 3.9 × 10³ |
| tt̄1ℓ FB0 / FB1 | 1/57, 0/15 | 1/123 744, 0/29 625 | 2.4 / 2.7 × 10⁶ → 1.1 / 1.4 × 10³ |

The proxies inherit the change (W(eν), W(μν) and WW from W(τ); tt̄2ℓ, single top and tW from tt̄1ℓ; WZ and ZZ from
Z(νν)). W(τ_ℓ) was not affected: its R04 ∧ R09 population had < 10, so the search fell through correctly. "SM Z(νν)
dominates FB0/FB1" (report §4) is an artefact of this defect.

**Fix (`background.py`, `chain_factors`).**
```python
    pops = [(C.RUNGS[start_col], base)]
    out = []
    last = {}
    first = {}                                         # NEW: index in pops before the first added cut of each variable
    for q in todo:
        v = VAR_OF_REQ[q]
        first.setdefault(v, len(pops))                 # NEW
        ...
        else:
            got = next(((nm, m) for nm, m in reversed(pops[:first[v]]) if rec.groups(m)[0] >= 10), None)   # was pops
```
The non-merged per-step branch (l. 356) may keep using any population. Its conditioning on q′ makes it consistent.

**Re-evaluated with the fix [E]** (`inv_fb2_srt.json`, `inv_fb_sm_C12_v1_withfb2.json`, `inv_fb_sm_C1_v1.json`).
Each patched chain was re-run through the frozen `Term`, the B sum was recomputed with the frozen `stats.b84`, and the
limits with the frozen `expected_limit_toys`.

| selection (C12) | B₈₄ T frozen → fixed | B₈₄ G frozen → fixed | B median G |
|---|---|---|---|
| FB0 | 1.7 × 10⁸ → 4.1 × 10⁶ | 2.7 × 10⁸ → 6.5 × 10⁷ | 8.8 × 10⁷ → 1.6 × 10⁶ |
| FB1 | 1.4 × 10⁸ → 3.2 × 10⁶ | 1.9 × 10⁸ → 2.7 × 10⁷ | 6.5 × 10⁷ → 1.1 × 10⁶ |
| FB2 | **9.3 × 10⁷ → 3.6 × 10⁶** (C1: 6.3 × 10⁶) | 1.0 × 10⁷ (unchanged) | — |

After the fix, FB0/FB1 is dominated by PU (trend σ_ln 5.2 at index 20) and C′, not by SM.

The primary toy μ₉₅ (events) and μ₉₅/N_exp, C12:

| point | r_fb | μ₉₅ frozen | μ₉₅ fixed | μ₉₅/N_exp frozen → fixed |
|---|---|---|---|---|
| E200 0.45 / 0.6 / 0.85 / 1 | FB0/FB0/FB0/FB1 | 7.6/7.6/3.8/2.6 × 10⁹ | 1.5/1.5/0.76/0.48 × 10⁸ | 2.3 × 10⁴ → 460; 8 × 10³ → 150 (1 keV) |
| E200 1.5 | FB2 | 1.7 × 10⁷ | 1.7 × 10⁷ (ε_T = 0) | **53 → 53 (best point unchanged)** |
| E500 0.6 / 0.85 / 1 / 1.5 | FB0/FB0/FB0/FB1 | 12/5.7/3.6/1.4 × 10⁹ | 1.7/1.9/1.1/0.40 × 10⁸ | 1.1 × 10⁶ → 1.6 × 10⁴ … 1.4 × 10⁵ → 3.8 × 10³ |
| E500 2 | FB2 | 8.3 × 10⁷ | **2.7 × 10⁷** (C1 3.5 × 10⁷) | 7.9 × 10³ → 2.5 × 10³ |
| E1000 0.6-2 | FB0/FB1 | 1.9-7.2 × 10⁹ | 0.54-2.3 × 10⁸ | 5-19 × 10⁶ → 1.4-6 × 10⁵ |
| E1500 0.85-2 | FB0/FB1 | 3.1-15 × 10⁹ | 0.9-3.1 × 10⁸ | 1.2-6.1 × 10⁸ → 3.6 × 10⁶-1.2 × 10⁷ |
| Ẽ500 1 / 1.5 / 2 | FB0/FB0/FB1 | 5.6/5.4/2.0 × 10⁹ | 0.78/1.7/0.57 × 10⁸ | 7.4 × 10⁶ → 1.0 × 10⁵ … |
| Ẽ500 3 | FB2 | 8.7 × 10⁷ | **3.2 × 10⁷** (C1 4.1 × 10⁷) | 1.1 × 10⁵ → 4.3 × 10⁴ |

- **Conclusions unchanged:** there is no exclusion or discovery anywhere, the best μ₉₅/N_exp is still 53, the ladder
  has no WP, and the minimum ladder B₈₄ is still 1.6 × 10⁶. No ladder rung and no FB3/FB4 column contains the defect.
- C1_v1 FB0/FB1 limits move by the same ×30-50 (`inv_fb_sm_C1_v1.json`).
- **Cascade if fixed:** re-run `run_all --stages background,srt,wp,products,limits` for C12_v1 and C1_v1. This is
  well under the 2 473 s full run, because the signal stage is unaffected. Then update STAGE4_RESULTS §2.4 (FB rows),
  §4 (table, "dominant" column), §9, §10.4, and STAGE4_SUMMARY.json.

## 3. Model spread 1.97 → 4.76 at R10-R14, F0e, FB4 (§10.5)

**Which models [V]** (`background.json` → `columns`, R11):
- The power law is undefined beyond R07 (B1 < 10 groups).
- The spread is ln(P_fact/P_main):
  - C12: 2.84 × 10⁻⁵ / 2.44 × 10⁻⁷ = 117 → **4.76**;
  - C1: 6.85 × 10⁻⁵ / 9.55 × 10⁻⁶ = 7.2 → **1.97**.

| factor | main route (start R06, thinning) C1 → C12 | factorisation route (start R07, B1 direct) C1 → C12 |
|---|---|---|
| width | p(R07 \| R06) 12/4 950 → 35/11 858; p(R08 \| R06 ∧ R07) 0/12 → **0/35 bound** | P(R07) direct 12/20 000 → 35/48 000; p(R08 \| R07) **0/12 → 0/35 bound** |
| χ²_core R09 | 0/12 (zero, tie with R08, enters as 1) → **2/35 = 0.057** (credited) | merged joint tail p(R11 \| R07) 0/12 → **0/35: tie with R08, enters as 1** |
| χ²_core R10, R11 | 14/57, 5/14 on R06 ∧ R09 → 32/126, 12/32 | (merged above) |
| χ² rejection credited | 0.088 → **0.0054** | **1 → 1** |

**Classification (i).**
- Every step follows the frozen code and rule: the §4.2 "one bound per term, ties first in ladder order, other zeros
  enter as 1", A28 merge, A06 envelope, and "tightest population, else a looser ancestor".
- The factorisation route merges because its start, R07, has no looser ancestor in its own chain. The main route can
  fall back to R06 ∧ R09 (126). This is a legitimate model difference, not a population bug.
- The central value is the upper envelope (P_fact) at both C1 and C12, so the larger spread only adds σ_ln, which is
  conservative.
- The non-monotone PU column has the same mechanism. SR-T R11 = R08 (4.75 × 10⁻⁵) > R09 (4.1 × 10⁻⁷) because at R11
  the χ² joint tail 0/1 874 ties the w bound 0/1 874 and enters as 1. FB4-T vs FB3-T works the same way. This is rule
  consistent (B need not be monotone).

**(iii) note for a future pre-registration (not actionable under the freeze):**
- A zero factor neutralised to 1 by "one bound per term" credits **less** rejection than a 1-2-count measurement on the
  same M. A route with an extra observed count can therefore move the envelope spread by orders of magnitude.
- Candidate policies:
  - compute the spread only between models with the same set of zero-bounded variables;
  - or let the factorisation route use the main route's looser ancestors.

## 4. Closure end state (×1.500, ×1.606, ×2.41)

**[V]**
- `closure()`: T1 reading A (R04) r = 1.5001, branch anti-conservative. Reading B and T1w: r = 1.6061, "anti-conservative
  (missing lever arm)" (lever 0.029 > 0.1 fails). T1e is untestable (< 10 B1 counts), which goes to T3 with no factor.
  The trend is significant and conservative (slope −0.361).
- `compounded()` (l. 136-155) / `families_of_column()` (l. 157-170): the counting family T1 applies to every column. For
  the T1 family, `T1_governing_branch` = anti-conservative selects reading A (1.500); reading B is "missing lever arm",
  so it is not among the governing-branch candidates (C-8).
- T1w applies to R05-R14 (cols 4-13), F0e (14-16) and all FB (17-36, including FB0 through its χ²/2S cuts), as A07
  lists. The missing-lever-arm path is × max(r, 1) = 1.606 with |ln r| = 0.474 in σ_ln,closure (review B-2).
  Product: 1.500 × 1.606 = **2.409** (C1: 1.504 × 1.610 = 2.422). This matches `end_state[*].closure_factor` at every
  column ≥ R05.
- **Applied once:** `end_state()` multiplies `base × fac × f_tr × f3` (l. 493).
  - `wp.pu_term` / `srt_pu_term` take `P_per_trial` as-is. Each SR-T summand uses one end state (es_T or es_all).
  - The R15-R20 `retrend` touches only the trend.
  - SM and C′ carry no closure factor.
  - f_tr = 1 (the trend is conservative), and T3 = 1 (non-informative, flagged).
  - No other code path reads `closure_factor` or `ratio` (grep over `analysis/*.py`).
- This is the user-approved literal end state (LOG.md l. 210; WP_RULE §6.4 "upper envelope … × N_obs/N_pred"; A07,
  which flags the R04 double count as conservative).

**(i) correct.** One consequence of the literal rule, for the record: the envelope members P_fact and P_pow are B1-direct
(ρ = 1, i.e. the observation itself), and they are also × 2.41. This is conservative by construction. It is not a
second application.

## 5. Zero-count bounds of the C′ and SM terms beyond R07

**Rule check [V]** (`Term.evaluate`, `background.py:196-214`; `wp.add_guarded`, `_f1_on_row`):
- **At most one bound per term** at every rung and FB column (`inv_zero_bounds_C12_v1.json`: n_bounds ≤ 1; up to 2 zeros
  per term). The bound sits on the largest-M zero, and ties go to the first in ladder order. Example: DIF R09 has w
  0/81 (bound) and χ² 0/81 (enters as 1).
- F1 factors on an already bounded SM/C′ row enter as 1 (A-2 guard).
- **M is the §4.2/§7 population:** the tightest population of that sample with ≥ 10, along the cumulative chain from the
  deepest rung with ≥ 10 (C′_PU attributed candidates, SM HS candidates). Defect 2 does not touch any ladder or FB3/FB4
  SM/C′ row.

**M values and what statistics would push each bound below 0.11** (C12, SR-G; SR-T is identical by A12).

N_need assumes the zero persists, so the bound scales as 1/N_sample. "×data" is N_need over the 3 ab⁻¹ data-equivalent
count of that process [E].

| term | zero factor carrying the bound (rung R08-R09) | M | B central | B₈₄ alone | sample now | N_need (term alone ≤ 0.11) | ×data |
|---|---|---|---|---|---|---|---|
| C′ DIF | p(R08 \| R05) merged w tail, C′_PU attributed | **81** (of 7 760 attr. in 500 ev.) | 1.7 × 10⁵ | 4.7 × 10⁵ | 500 | **2.2 × 10⁹** | ≈ 36 (N_trig·rate·f_pre = 6.2 × 10⁷) |
| C′ PV pair | p(R08 \| R02) merged w tail | **24** | 1.4 × 10⁵ | 6.0 × 10⁵ | 500 | **2.7 × 10⁹** | ≈ 2 (1.2 × 10⁹) |
| C′ γ | p(R08 \| R06) | 13 | 4.2 × 10⁴ (R08) | 1.3 × 10⁵ | 500 | 5.7 × 10⁸ | ≈ 37 |
| C′ looper | P(R01) direct, 0/500 C′_PU | 500 | 3.4 × 10⁴ | 1.9-2.5 × 10⁵ | 500 | 0.9-1.1 × 10⁹ | ≈ 70-90 |
| C′ V0 | — | 358 | 5.8 × 10³ | 1.6 × 10⁴ | 500 | 7 × 10⁷ | — |
| SM Z(νν) | p(R08 \| R06) merged w tail, HS candidates | **81** (presel-weighted start 32.3/2 000) | 1.6 × 10⁴ | 4.6 × 10⁴ | 2 000 | **8.3 × 10⁸** | ≈ 14 (σKL = 6.0 × 10⁷) |
| SM W(τ_ℓ) (→ W(eν), W(μν) proxies) | p(R08 \| R06) | **14** | 8.6 × 10³ (+1.0/0.9 × 10⁴ proxies) | 2.9 × 10⁴ | 375 | 1.0 × 10⁸ | — |
| SM W(τ_h), tt̄1ℓ (R07, FB3) | P(R07) direct, presel-weighted 0 | 1 625 / 2 000 | 1.3 / 0.9 × 10⁴ | 3-5 × 10⁴ | 1 625 / 2 000 | 5.7 / 4.9 × 10⁸ | — |

- **The effective bound does not depend on M.** For example, C′ DIF = f_pre × (81/500) × 1.14/81 × c = 1.14·f_pre·c/500,
  and Z(νν) = (Σw/2 000) × 1.14/81 = 1.14·w̄/2 000. The bound is ≈ 1.14·c/N_sample per process. The quoted "M = 16-81"
  (report §8) is the substitute population, not the lever. Only more **events** help, and clustering of candidates
  within events does not bias the bound.
- **All bounded C′ + SM terms together ≤ 0.11:** ×**1.4 × 10⁷** more statistics at R08/R09 (×1.1 × 10⁷ at FB3,
  ×1.5 × 10⁷ at R14/FB4). That is **≈ 7 × 10⁹ C′_PU events per topology and ≈ 3 × 10¹⁰ SM events per sample**, i.e.
  ≳ 10-40 × the data-equivalent count of each process.
- Even then, PU alone stays at B₈₄ = 2.3 × 10³ (R09) / 3.0 × 10⁴ (R08), 4.3-5.4 decades over budget. **Statistics
  alone cannot produce a WP.** This confirms report §8 item 1 with sharper numbers.
- The cheapest real lever is the rule's own C′₀ route (10⁵ events per gun, 5 × 10⁴ DIF): ×100-200 on the C′ bounds,
  2-2.3 decades. It would need a new pre-registration for the w/χ² conditionals.

**Side findings (C′ rule conformance, §7):**
- **(ii) Looper "low gun counts" not implemented.** §7: "A gun topology with < 10 passes in 500 at the loosest counting
  rung starts its depth from the C′₀ factors under §4.2." The looper has 0/500 C′_PU at R01, and also 0/10⁵ attributed
  in C′₀. `depth_term` (`background.py:639-646`) instead enters P(R01) = 0/500 from C′_PU, giving a bound 1.14/500. The
  rule gives 1.14/10⁵. This is conservative.
  - Fix: in `cprime_term`, when `F[:,0].sum() < 10`, call `depth_term` on `r0` with `n_den = n0`.
  - Effect [E] (`inv_looper.log`): B₈₄ G 1.59 → 1.36 × 10⁶ (R08), 1.57 → 1.23 × 10⁶ (R09), FB3 2.9 → 2.0 × 10⁶,
    FB4 6.8 → 5.4 × 10⁶. Conclusions are unchanged.
- **(iii) C′ dE/dx and h/o factors.** §7 says "Depth from rung factorisation on C′_PU … and the **C′₀ h/o/dE/dx
  factors**". The code instead measures dE/dx inside the C′_PU chain (e.g. DIF p(e > 2.0 | R05) = 1/81; PV pair 0/24,
  which enters as 1). It takes h/o from the B1 PU records (`_f1_on_row`, population FB1 46/46) rather than from C′₀.
  This affects only the R15-R23 and FB-e columns (FB4e is used at E1000/E1500 5 keV). The direction is unknown. A
  C′₀ dE/dx zero with M ≈ 10⁴-10⁵ would take the bound away from the w factor. Needs a decision: literal §7 (C′₀) or
  the implemented C′_PU reading.
- A minor, conservative point: `depth_term` applies the global c = 1.196 whenever the chain is non-empty, including
  chains made only of "no population → 1" factors (looper).

## Files

- Scripts: `acts/stage4/investigation/inv_asym.py`, `inv_asym_mech.py`, `inv_fb2_srt.py`, `inv_fb_sm.py`,
  `inv_zero_bounds.py`, `inv_looper.py`. Run them with `PYTHONPATH=. pixi run python …` from the TT root.
- Outputs: `data/acts_stage4/investigation/inv_asym_{C12_v1,C1_v1}.json`, `inv_asym_mech.log`, `inv_fb2_srt.json`,
  `inv_fb_sm_C12_v1_withfb2.json`, `inv_fb_sm_C1_v1.json`, `inv_zero_bounds_C12_v1.json`, `inv_looper.json` (+ `.log`).
