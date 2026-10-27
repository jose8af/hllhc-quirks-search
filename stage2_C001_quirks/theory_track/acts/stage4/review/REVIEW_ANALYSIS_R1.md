# REVIEW_ANALYSIS_R1: critical review of the Stage-4 analysis pipeline (`acts/stage4/analysis/`)

| | |
|---|---|
| Date | 2026-10-14 |
| Reviewer | fresh critical reviewer (spec `jfc/src/agents/critical_reviewer.md`, `methodology/03-review.md`) |
| Target | `acts/stage4/analysis/*.py` (common, hitrec, signal, admissibility, background, srt, wp, stats, run_all); `inputs/{analysis_map,schema,ambiguities,normalisation}.json`; LOG 2026-10-14 03:05 |
| Governing texts | `WP_RULE.md` (1b2ea9bd…), `WP_RULE_PC19.md` (d30bcc2f…), `HASH_ADDENDUM.md` (e273c077…), `plan.md`, LOG decisions 2026-10-13 20:35 / 2026-10-14 00:40 |
| Signal values | **not looked at.** Only code paths, the G3 T_seed = 6 background dry run and file conventions |
| **Verdict** | **ITERATE: 4 A, 9 B, 10 C** |

## 0. What I checked and how

- **Governing hashes.** I recomputed the sha256 of the governing files. WP_RULE 1b2ea9bd…, PC19 d30bcc2f…, HASH_ADDENDUM
  e273c077…, frozen_inputs 2adc8f9d… and srt_tmin_check 9d0c902a… all equal the constants in `common.py`.
- **Code.** I read every module line by line against WP_RULE §1-§8, PC-19 and the logged decisions.
- **G3 dry run.** I read `data/acts_stage4/analysis/dryrun_g3_tseed6/{background,bsum_wp,srt}.json` (background only).
  The factor chains, the end states, the B₈₄ ladder and the SR-T factors were inspected numerically.
- **Two small checks** (nice 15, one process, < 2 min each):
  1. h and o recomputed with `B1Records.compute_f1` on 4 G3B1 jobs, 300 records per rung. h ≈ 0.7-1.5·10⁶, o ≈
     0.2-19·10⁶, h NaN 0 %, o NaN 1.7-6.5 %. Every PU record passes h > 5 ∧ o > 5. The dry-run tables agree:
     N = M on 1 505-4 977 records for every F1 parent.
  2. The BTL event-index convention in B1 and A2 files (§A-4).

**Verified correct (no finding).**
- **WP rule** (`stats.rstar`, `combined_guard`, `wp_rule`): r*_c is the loosest rung with B₈₄ ≤ 0.11 at that rung and
  every tighter one; the pair guard checks ≤ 0.3 over every component-wise tighter pair. The continuation moves the
  larger-B₈₄ category (tie: SR-G), a category at R = 23 stays, and the loop is limited to 2(R − 1) steps. The
  "exactly one category" and "no WP" branches are implemented.
- **Zero-count rule inside one `Term`.** The largest-M zero factor gets 1.14/M with σ_ln 1.0 (ties: first along the
  ladder); every other zero enters as 1; σ_stat ≥ 1/√N.
- **A28 implementation** (`chain_factors`), traced on the dry-run chains (see §2, A28).
- **Closure end state.** Branches come from `analyse_g3.family_test` (reproduces G3: T1 1.319, T1w 1.424). The T1 × T1w
  compounding gives a factor of 1.88 on width/χ²/2S/FB columns. The upper envelope is applied at every column once any
  family is anti-conservative, with σ_model = ln(max/min). A significant conservative trend enters σ_ln only. There is
  no +50 % step and no union count (per-hit-set n_grp/S_ded everywhere except the NOGRP columns).
- **Density σ_ln (PC-11) and normalisation σ_ln.** Density uses the deepest qualifying value for deeper rungs, 1.0 when
  DENS is absent; normalisation is ln 1.3.
- **PC-19 SR-T background factors** (`srt.fractions`, `srt_factors`): edges from C1 (+G3 dry) B1 only. P(late) is on
  BTL-present candidates and P_OOT = (n̄₊₁ + n_{k≤−1})/M_¬pres; the k ≤ −1 proxy is max Δt ≥ t_min + 25j. The
  fixed-window variations and the mechanical fallback (none → 1.0) are as written. The dry run reproduces the reference
  (6.07/24.025 ns; 0.306/0.016 at R04).
- **Signal match** (`hitrec.signal_match`): ≥ 3 core quirk hits, in ≥ 3 distinct layers, and ≥ 50 % of the core hits.
  The core is recomputed exactly as `g1b_tt.core_mask`, and the executor's self-check reports 0 mismatches.
- **Signal ladder composition** (`signal.ladder_flags`) is the same as the background composition (§6.2). f_CKF < 0.2
  is applied at every rung for signal and enters no B_PU factor.
- **Admissibility.** k_adm thresholds equal A.1 (≥, 1e-12 tolerance); e_adm comes from the hash-checked A.2b;
  `rung_levels` / `rstar_admissible` / `primary` implement §8, including mixed admissibility. Per-point best-of is not
  possible: the primary is chosen from admissibility only.
- **T_seed guard.** `run_all` refuses G3 in a production union and a non-G3 dry run. `admission` requires the
  finder_cfg.tseed of each job to equal 4 (6 for the dry run). `limits_stage` refuses differing signal and background
  manifests.

---

## 1. Category A (must fix before PASS)

### A-1: the SR-T "¬BTL-present × P_OOT" summand is set to 0 at every rung beyond ρ = 2 reach

`wp.srt_pu_term` (l.67): `p_nt = max(es_all['P_per_trial'] − es_T['P_per_trial'], 0.0)`.

- The two end states are independent estimates: separate factor chains, separate zero bounds and an envelope each.
- The BTL-present chain runs on a smaller population (M_T ≈ M/6), so its 1.14/M bound is larger. The result is
  P_T > P_all beyond reach.
- **Evidence (dry run, `background.json` end_state vs end_state_T):**

  | rung | P_all | P_T |
  |---|---|---|
  | R08 | 6.09e-4 | 6.16e-4 |
  | R09 | 6.07e-6 | 9.98e-6 |
  | R14 | 3.62e-7 | 2.25e-6 |
  | F0e | 1.5e-7 | 8.4e-7 |

  Hence p_nt = 0. In `bsum_wp.json` the term "not present x P_OOT" has value **0** at R14, R17 and R20 (and R08-R23).
- PC-18/PC-19 require the summand. It is not small: at R04 the dry-run P_OOT·M_¬pres ≈ 14.3 counts against
  P(late)·M_pres = 48.
- A value of 0 also violates "a zero never enters as 0".
- **Fix (conservative, minimal).**
  - Use the full difference only where both columns are thinning estimates (reachable at ρ = 2; PC-18 "both in-job").
  - Elsewhere use P(r ∧ ¬BTL) ≤ P(r), i.e. the full-column end state, as the base of the ¬present summand.

### A-2: more than one zero bound per term (violates WP_RULE §4.2 "a bound enters at most once per term")

- `wp.pu_term` handles this correctly (an F1 factor of 0 enters as 1 when the column already holds its bound).
- Three other composers do not:
  - **`srt_pu_term`** (l.68-77) multiplies the column end state (whose chain may already hold a 1.14/M bound) by a
    timing factor N/M via a new `Term`. With N = 0 that is a second bound, and the F1 factor can add a third.
    **Evidence:** at R14 the present summand carries the chain bound p(w<4.7 | R06 ∧ BTL) = 0/247 → 1.14/247 **and**
    P(late) = 0/254 → 1.14/254. Its value is 1.3 events. Under the literal rule the largest-M zero factor, P(late)
    (M = 254), carries the bound and the chain zero (M = 247) enters as 1, which gives ≈ 2.8·10² events, i.e. the
    current value is ×≈ 220 low.
  - **`sm_terms`** (l.96-99) and **`cp_terms`** (l.119-120) multiply 1.14/M for F1 N = 0 onto r['B'] even when
    r['zero_branch'] is true.
- **Fix.** Evaluate each SR-T summand (chain factors + F1 + timing factor), and each SM/C′ term (+ F1), as **one**
  `Term`, so that the largest-M zero factor alone carries the bound. At R14 that is P(late) (M = 254 > 247), and the
  chain zero enters as 1. Alternatively apply the `pu_term` guard everywhere, which is more conservative.

### A-3: SM and C′ terms at the fallback selections are evaluated at R14 (a tighter selection)

- `wp.sm_terms` l.90: `r = v['rows'][col] if col < 14 else v['rows'][13]`.
- `wp.cp_terms` l.108: `v['rows'][min(col, 13)]`.
- For FB columns (17-36) both take the **R14** row. But FB0-FB3 are looser than R14:
  - FB0 = R04 ∧ p > 0.05 ∧ N_2S2 ≥ 3, with no width cut;
  - FB_k uses w < W_k with k < 4, where R14 needs w < 4.7.
- B_SM and B_C′ are therefore underestimated at the primary selection of most (m, Λ) points (k_adm ≤ 3 covers most of
  A.2b). The ×1/p(w<4.7 | …) loss is large, and these terms enter both categories in full.
- F0e (14-16) → R14 is the conservative direction and is fine.
- **Fix.** Compute the SM and C′ rows for every in-job requirement column (COL_REQ 0-36). Start from the deepest rung
  whose requirement prefix ⊆ COL_REQ[col], as `bpu_columns.start_of` does. In `depth_term`, `c <= col` is wrong for
  col ≥ 14.

### A-4: signal ε_SR-T: the OOT B1 hits are looked up with the wrong event index (OOT veto almost never applied)

- `srt.signal_srt` (l.215-232) builds `ev_index` from `range(ev0, max(trials.ev)+1)` (absolute event numbers) and
  selects `B[bev == e]` with `bev = btl[:, 0]`.
- In B1 files `btl[:, 0]` is the **job-relative** event index. Verified on `prod/G3/G3B1/G3B1_00005.npz`: meta
  ev0 = 125, trials.ev 125-149, btl col0 0-24. `srt.job_arrays` correctly uses `(ie + p) % n_ev` with ie = ev − ev0.
  (Signal A2 files are consistent, with trials.ev 0-9 = btl col0, so `signal.analyse_file` is fine.)
- For every assigned event outside job B1_00000 the selection is empty, so the OOT hits never enter the earliest-hit
  ordering.
- The PC-19 veto ("those hits enter the earliest-hit ordering, so they can veto"; "OOT-PU lateness earns no credit") is
  silently dropped, so **ε_SR-T is overestimated** (anti-conservative limits).
- **Fix.** Use `B[bev == e − ev0_job]`, store (jid, path, ev0, e) per entry, and add a unit check: the number of OOT
  in-band hits found > 0 for a sample of rows, and n_earliest_oot is reported.
- Also order C1 B1 by (job id, ev) **from the manifest**, not from what was admitted or present. N_B1 must not depend on
  missing jobs (C-level part).

---

## 2. Readings A01-A30: is each one the conservative one and consistent with the text?

| id | assessment |
|---|---|
| A01 | OK. ε(R01-R04, N_L2) are labelled lower bounds; every WP and fallback rung lies inside S4, so it is exact. Affects only R_A (a table) |
| A02 | OK. Frozen chain convention; a quirk hit counts only if it dominates (conservative for the match) |
| A03 | OK. No MS term inflates h for real helices (C′), so more pass h > 5: conservative on B. "Non-empty subset < 3 hits → undefined → passes" matches §1.4 |
| A04 | OK (definitional; o gives no PU rejection, see C-10) |
| A05 | OK. Expected groups per trial ≥ the per-road indicator: conservative |
| A06 | OK. Power law through ρ = 1, 2 = B1 direct; envelope everywhere once any family is anti: conservative |
| A07 | OK (user-approved literal compounding). **However:** "T1e untestable → T3, no factor" relies on T3, which is computed but not applied, and T3 is degenerate (B-1) |
| A08 | Acceptable G3 convention, |a + b·x|. Hidden effect: at deep rungs this term dominates (σ_trend 2.9 at R14, 4.8 at R20/FB, 5.2-5.8 at F0e in the dry run). Conservative, but the user should know it alone can remove every WP (C-9). The anti-conservative-trend central factor is not re-evaluated for R15-R20 (B-9) |
| A09 | Wording: the code never goes looser than the start rung (no "superset" fallback); a missing population gives factor 1 with σ_ln 1.0 (conservative) (C-5) |
| A10 | Literal and conservative (larger bounds on BTL-present), but it is what triggers A-1. Keep it, with the A-1 and A-2 fixes (D5) |
| A11, A12 | OK, conservative |
| A13 | Candidate counting is conservative. The F1 factor from B1 is 1.000 in practice, so no credit is taken (C-7) |
| A14 | Genuine user decision (D1) |
| A15 | OK, fail-safe (the B sum is flagged INCOMPLETE and no WP is claimed) |
| A16 | OK. The largest carried value is conservative and consistent with "the same fallback then applies to that parent" |
| A17 | OK (§4.2). Relies on the time-independence test, which is not re-run in production (B-4) |
| A18 | OK. A fixed format, decided before signal |
| A19 | Acceptable. Dropping the cross-bin correlation is negligible at B ≪ 1. **ε from A2core is the right pre-declared choice** |
| A20 | Toys are the conservative choice (D4) |
| A21 | **Not fully conservative.** Status ≠ 1 rows are removed from the denominator; plan §1.3 says "carry … as an efficiency loss" (B-6). The rest is OK (no-finder trials = failures, all η) |
| A22 | OK by design, but the implementation is broken (A-4) |
| A23 | OK (1.0 when absent) |
| A24 | **Slightly below the literal text.** §6.4: "c = joint/product (the max over bins and pairs) multiplies … if any c > 1 at 2σ" means the global max, not the max among the flagged. c is also not applied to the SM and C′ chains (§4.2 applies to every factor of every term) (B-3) |
| A25 | OK (approximate; p = 1 anyway) |
| A26 | OK |
| A27 | OK. A seeded random subsample is unbiased |
| A28 | **Confirmed correct, conservative and minimal.** In the dry run p(w<9.4 \| R06) = 9/1505 and p(w<4.7 \| R06) = 0/1505. The per-step marginal reading would multiply nested tails (×1/0.006 too low at R08; χ²_core similarly). Stepwise conditioning on the previous cut of the same variable, else the merged joint tail, telescopes exactly to the direct cumulative ratio when populations coincide (FB0 chain = B1 direct 9/1.09·10⁶ verified). When a merge drops earlier factors whose cuts are inside the chosen population, the result is larger (conservative). It is not a rule change: it is the only reading of "conditional p_{r→r+1} measured on the tightest population with ≥ 10" that is a conditional |
| A29 | Reasonable. No T-specific closure is pre-registered |
| A30 | OK and literal. Edges come from C1 B1 only (`campaign in ('C1','G3')`; G3 is impossible in production) |

**Hidden choices that could move the result:** D1 (N_trig, ×3.9), A08 (trend magnitude at deep rungs), A10 + A-1/A-2
(SR-T), A24 (c), and the untested cross-variable factorisation (B-1). None depends on signal values.

---

## 3. Category B (advisory, but recommended before the C1b analysis is run)

- **B-1: T3 is computed but never applied, and it is degenerate.**
  - `run_all` computes `G3.t3_test` and stores it; `end_state` never uses its branch.
  - In the dry run T3 is degenerate (R06 from R04, same variable), and it stays degenerate as long as r₁ is a width
    rung (R07 needs ≥ 10 B1 counts, and R09 needs w < 4.7 ∧ p > 10⁻³, with 0 in G3).
  - So the cross-variable factorisation that sets B at every WP candidate (w → χ²_core → 2S → dE/dx, e.g.
    p(p > 10⁻³ | R06) applied at w < 4.7) has **no closure test**. The c-test covers only layer-crossing correlations.
  - **Recommendation:**
    - wire the T3 branch (anti: × N_obs/N_pred; conservative: |ln| in σ_ln) into every factorised column;
    - flag "T3 non-informative" in `bsum_wp.json`;
    - tell the user before C1b results are read. Whether to pre-declare a non-degenerate cross-variable T3 variant, or
      an extra σ_ln, is a **user decision**; the frozen rule has no branch for an untestable T3.
- **B-2: the missing-lever-arm branch can lower B.**
  - `family_correction` returns factor r for any 'anti-conservative…' branch.
  - With 'anti-conservative (missing lever arm)', r can be < 1. In the dry run, B1/thin at R06 is 0.195/0.338 = 0.58.
  - Under "closure failure of unknown direction" the conservative literal is max(r, 1) with |ln r| in σ_ln. This is a
    one-line fix.
- **B-3: the c factor (A24).**
  - Use the global c_max over all bins, pairs and triples when any is flagged.
  - Apply c to the SM and C′ chain terms as well (`depth_term` adds no c).
  - In the dry run both maxima coincide (1.2675), so the effect is nil there.
- **B-4: the SR-T time-independence test (§6.2 SR-T row; §6.4 "part of the same gate") is not run on C1/C2B.**
  - It ran only at G3 (PASS).
  - Run `G3.srt_test` (or an equivalent) on the production union, and apply c if it fails.
- **B-5: the ρ_dens > 1.05 refusal is not implemented.**
  - The `admissibility.py` docstring claims "the run REFUSES to use this table".
  - In fact `rho_dens` is only written to `background.json`; the signal and limits stages never check it.
  - Make `limits_stage` (and the signal admissibility table) refuse when `rho_dens.trigger` is true.
- **B-6: status ≠ 1 rows are dropped from the signal denominator** (A21).
  - Plan §1.3 and HANDOVER say to carry them as an efficiency loss (≤ 1.5 % per point, status 0 ≤ 4/200).
  - Keep them in the denominator as failures. This is a small effect, but the conservative choice is free.
- **B-7: the C′ special paths.**
  - N_pre = 0 (the 500 with-PU events are not run) is reported as "C′_PU outputs not available", which leaves the B sum
    permanently INCOMPLETE. The rule says f_pre follows §4.2 and the conditional is set to 1.
  - The V4-10 leak correction f_pre × (1 + N_leak/N_attr,pre), with its σ_ln and flag, is not wired. The leak is 0 now.
  - The ⌈500/N_pre⌉ re-overlay needs the two-level bootstrap; the current bootstrap is one-level, per trial.
- **B-8: pre-registration hygiene (item 6 of the brief).**
  - Signal ε, the open D1-D4 values and the limit calculator are not yet fixed, and `limits_stage` writes limits even
    when `complete_inputs` is false (it only flags them).
  - **Recommendation:**
    - log the D1-D10 resolutions;
    - freeze `normalisation.json` and the analysis package sha256 (in the LOG) **before** the signal stage prints any ε;
    - make `limits_stage` refuse, or label the output NOT A RESULT, when the B sum is incomplete;
    - fix the primary calculator (D4) before the first limit is computed.
- **B-9: two smaller correctness items.**
  - (i) PC-19 σ_ln,PV and σ_ln,σt are measured on the combined L and come from the same variation, but `srt_pu_term`
    gives each SR-T summand an independent z ('srt_pv' and 'srt_sigt' are not in `SHARED`). Make them shared within
    the category.
  - (ii) For an anti-conservative trend, `retrend` updates only σ for R15-R20, not the central factor exp(ln r(x)).
    G3 and C1 are expected to be conservative, so this is latent.

## 4. Category C (notes)

- **C-1.** B_cosmic and B_halo are not in the sum, and contrary to the `wp.py` docstring they are not flagged. Add the
  plan's argument terms ("≪ 0.1", negligible) as an explicit flagged line.
- **C-2.** Admission:
  - the per-job `meta.frozen_inputs` dict is not compared with the T_seed-4 file;
  - a changed `frozen_inputs.json` is recorded but not refused;
  - A.3 files missing from a job's `code_sha256` are skipped silently.
- **C-3.** `limits_stage` passes its T_seed check when both manifests are absent (None == None).
- **C-4.** `expected_limit_toys` draws fresh randoms at every CLs evaluation during the bisection. Use common random
  numbers for a monotone CLs(μ).
- **C-5.** The A09 wording does not match the code (no looser-than-start fallback). The code's choice is conservative.
- **C-6.** Record in the manifest the sha256 of the imported frozen modules: `g3/analyse_g3.py` (44cfa9a7…, not hashed
  anywhere) and `g3/srt_tmin_check.py`.
- **C-7.** The F1 factor of the C′ terms comes from B1. The rule says the C′₀ h/o/dE/dx factors. In practice p = 1, so
  nothing is credited (conservative); fix it before crediting any F1 rejection to C′.
- **C-8.** The counting-family factor uses reading A's ratio when readings A and B have equal severity. max(r_A, r_B)
  would be the conservative choice; the effect is nil in G3.
- **C-9.** Tell the user that the trend σ_ln (|1.71 − 0.327·x| in G3) dominates every deep rung. It is the approved end
  state, not a bug.
- **C-10.** h and o give no PU rejection (p(h > 5 ∧ o > 5) = 1.000 on 1 505-4 977 B1 records; h ~ 10⁶). So D8 (T3s)
  is moot unless a factor < 1 is ever credited.

## 5. Open decisions D1-D10: recommended resolutions

| id | recommendation | genuine user decision? |
|---|---|---|
| D1 N_trig | Keep **1.28·10⁸** (Z(νν) + W(ℓν), truth MET > 200 GeV, no vetoes or preselection, × K 1.4) as the frozen value. It exceeds Z + W + tt̄ + single-t + VV after vetoes and the 250 GeV cut, and is covered by the ±30 % nuisance. Log it before any B is quoted | **YES** (moves B by up to ×3.9) |
| D2 rate_t | Run a short Pythia generator-level count per triggered W/Z+j event of γ, K⁰_S/Λ, NI-capable hadrons, kaons (DIF), PV pairs and loopers in the road (≲ 1 CPU-h). Otherwise enter conservative upper values with σ_ln 1.0, flagged. No WP claim until done | **YES** (new inputs; cost vs deadline) |
| D3 SM σ | Mechanical: take the sample-specific Pythia σ (sigmaGen × MET-filter efficiency) of the C1 SM jobs. If unavailable, use the upper bound W(τν) = W(ℓν) 15.8 pb, and get tt̄ 1ℓ from a small Pythia σ run. Keep W(τ_hν) = full W(τν) | no (orchestrator) |
| D4 calculator | **Toys primary** (3.0 events at b → 0); report asymptotic as a cross-check. Fix it before any limit is computed | orchestrator; inform the user |
| D5 SR-T population | Keep the literal BTL-present conditionals, with the A-1 and A-2 fixes | no |
| D6 pyhf | Do not change the pixi env while production runs. Keep the in-house asymptotic CLs, plus an isolated pyhf 0.7.6 cross-check of the final workspaces (JSON already pyhf-schema) | no |
| D7 V4-3 | Accept the in-job-definition variants as a labelled diagnostic (V4-3 is not a rule input). Re-run A1 with hit records only if CPU is spare | no |
| D8 T3s | Pre-declare: T3s is required only where a p(h/o) < 1 is credited. G3 gives p = 1.000, so nothing is credited. If C1 gives p < 1 at a WP-relevant population, run T3s on the S7 sets or credit factor 1 | no (pre-declare now) |
| D9 ε(R01-R04) | Accept as labelled lower bounds (they affect only R_A; all WP and fallback rungs are exact) | no |
| D10 A28 | **Confirm.** It is correct, conservative and minimal (§2). Log it as the reading of §6.2 step 3, not as a rule change | no (orchestrator logs it) |

## 6. Verdict

**ITERATE.** Category A:
- **A-1:** the SR-T ¬present summand is zeroed beyond reach.
- **A-2:** multiple zero bounds per term (SR-T, SM, C′).
- **A-3:** SM and C′ terms at the fallback selections are taken from R14.
- **A-4:** the signal ε_SR-T OOT veto is dropped (relative vs absolute event index).

All four fixes are local and cheap (wp.py, background.depth_term, srt.signal_srt). After them, re-run the G3 dry run.
Check that the "not present × P_OOT" term is > 0 at R08-R23, that each term carries ≤ 1 bound, and that the FB SM/C′
rows differ from R14. Add a unit check that signal OOT lookups find hits.
