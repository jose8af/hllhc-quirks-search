# REVIEW_ANALYSIS_R2: critical review of the Stage-4 analysis pipeline, round 2 (D1-D3 implemented)

| | |
|---|---|
| Date | 2026-10-14 (~08:05-08:40) |
| Reviewer | fresh critical reviewer (spec `jfc/src/agents/critical_reviewer.md`, `methodology/03-review.md`) |
| Target | `acts/stage4/analysis/` frozen as `inputs/analysis_freeze.json` (20 files, sha256 9c3c23fc…); FIX_ANALYSIS_R1/R2, `inputs/fix_r1.json`, `INVESTIGATION_D1_D3.{txt,json}`, `inputs/normalisation.json`, `data/acts_stage4/analysis/d123/`, LOG 2026-10-14, `inputs/ambiguities.json` D1-D3 |
| Signal values | **not looked at** (code paths, dry-run background, generator-level normalisation only) |
| Checks run | all nice 15, one process, ≤ 1 min CPU each: freeze re-hash; `selftest` (PASS); dry-run `bsum_wp.json` scan; 4 generator-only Pythia probes of the hadronisation-failure bookkeeping (scratchpad `r2/hadfail_probe.py`, s4pu config imported unchanged, tt = None) |
| **Verdict** | **ITERATE: 1 A, 2 B, 9 C** |

## 0. Verified (no finding)

- **Freeze.** All 20 files of `analysis_freeze.json` re-hashed: 20/20 match. The freeze file itself hashes to
  9c3c23fc15db…, which is the LOG value. `selftest` gives `freeze: true` and SELFTEST PASS.
- **R1 Category A: all four resolved.**

  | R1 | code | cheapest discriminating check |
  |---|---|---|
  | A-1 | `wp.srt_pu_term` l.83-91: P(r) − P(r∧BTL) only if both columns are reachable thinning estimates, otherwise the full column; never ≤ 0 | dry run `bsum_wp.json`: **every** "not present × P_OOT" summand (23 rungs × T, 20 FB) is > 0, min 1.58 events; R08 2.2e4, R14 13.1, R23 1.58 |
  | A-2 | `add_guarded` in the SR-T, PU, SM and C′ composers; each summand is one `Term` | selftest A2_* 4/4. Dry run R14 "present × P(late)" = 81.7 events. That equals R1's literal single-bound value (≈ 2.8e2 at 1.28e8) × 3.63e7/1.28e8 = 79, i.e. one bound, not the old ×220-low double bound |
  | A-3 | `depth_term` `okd`: deepest ladder rung with LADDER_REQ ⊆ COL_REQ[col]; `wp.sm_terms`/`cp_terms` use `rows[col]` for all 37 columns | selftest A3: FB0 starts at R04, value ≠ R14 |
  | A-4 | `srt.c1_b1_event_index` builds the index from the manifest (job id, job-relative e); lookup is `B[btl[:,0] == e]`; `run_all` l.104 refuses when no OOT hit is found | selftest A4 on G3B1: 289/300 lookups with BTL hits, 66 in-band OOT hits, 7 earliest-OOT; A4_relative_index true |

- **R1 Category B: resolved.**
  - **B-1:** the T3 branch is wired, and "non-informative" is flagged.
  - **B-2:** max(r, 1) (selftest).
  - **B-3:** global c_max is applied in `depth_term` for SM and C′.
  - **B-4:** `srt.time_independence` runs on the union.
  - **B-5:** `limits_stage` refuses on `rho_dens.trigger`.
  - **B-6:** status ≠ 1 rows count as failures.
  - **B-7:** N_pre = 0 path, V4-10 leak correction, C′_PU source clustering.
  - **B-9:** `srt_pv`/`srt_sigt` are in `SHARED`, and `retrend` rescales the central value.
  - **B-8:** implemented, with the gaps listed in new B-2.
- **D1 preselection code path** (`gen_d123.presel`) **= the signal definition** (WP_RULE l.145-147, plan §3):
  - the same trigger weight, ε_trig = 0.98·½[1 + erf((MET_reco − 200)/(20√2))];
  - the same σ⊥ = 25 GeV per-component MET smearing;
  - MET_reco > 250, ≥ 1 jet with pT > 100 and |η| < 2.4, min Δφ(jet₁₋₄, MET_reco) > 0.5.
- **D1 vetoes.** The e/μ/γ vetoes apply only to SM, as in plan §3 ("vetoes cost the signal ≈ 0"). Each proxy is
  looser, i.e. it raises N_trig and B (conservative):
  - **no τ_h veto**;
  - only prompt and isolated objects are vetoed;
  - SM jets have pT > 30 GeV. The signal's Stage-2 jets have pT > 20 GeV and |η| < 5 (`sim/scripts/convert_hepmc.py:19`).
    The SM min Δφ therefore sees fewer jets, so it is looser.
- **D1 footing.** `sm_term` weights each HS candidate by its event's preselection weight from the same `presel`.
  - The weight is regenerated from the stored seed, and `hs_met` is verified; a mismatch makes the term refuse.
  - The proxy for W(eν)/W(μν) is converted to "per preselected event" consistently: P/f_cls × f_presel.
  - Pure-PU candidates stay in B_PU (`n_hs_band ≥ 1`). Nothing is double counted.
  - The event index ie = trials.ev − ev0 is consistent with `run_stage4.py:419` (ev = ev0 + ie).
- **D2.**
  - **Unit:** rate_t is per preselected event (Σw-normalised), the same footing as N_trig.
  - **Road:** |Δφ(·, φ_MET,reco)| < 0.15 rad, the frozen δ₉₅. The gun offset is ±0.1, so this is conservative.
  - **NI 0.22 factor:** applied exactly once.
    - `normalisation.json` ni30 = (0.700 + 50.65)·2.4e-3 = 0.1233, with no 0.22.
    - `wp.cp_terms` applies 0.22 to ni* only.
    - `cprime_term` does not apply it.
    - selftest R2_ni_pv_line passes.
  - **Max over processes:** conservative.
  - **"Unweighted larger everywhere":** this claim is not load-bearing. `cprime_term` recomputes R_t at analysis time
    and multiplies by max(1, R_t) automatically, and it records `spectrum_reweight` in `background.json`. The gun RNG
    replay is verified (1000/1000 φ_MET).
- **D3.**
  - The W(τν) τ-class split (`SM_PSEUDO`) uses τ_l events from the inclusive sample and τ_h pooled from both samples,
    so there is no double counting.
  - K_tt 1.9 is conservative relative to the rule's 1.4.
  - The W(τ_h) BR treatment is correct (σ_gen excludes the forced BR).

## 1. Category A

### A-1: the hadronisation-failure correction uses the failure fraction per *try*, not per *hadronisation attempt*: W, tt (and W(e/μ)) σ are 20-30 % low, and N_trig is about 10 % low (anti-conservative)

`gen_d123.mode_nt` l.236 and `normalise.merge` l.118 compute **σ = σ_gen · N_acc/(T − F)**, i.e. they divide the stored
value by (1 − F/T). This follows the investigator's and the orchestrator's D3 prescription "/(1 − r)".

- In `s4pu.HardScatter.generate` (and `generate_counted`), `forceHadronLevel` is called **only** for the A tries that
  pass the parton-level `PRE_MET` = 150 GeV filter (and, for tt, the nlep = 1 filter).
- Failures are independent of MET (investigator). The unbiased estimator is therefore
  **σ = σ_gen · (A/T) · N/(A − F) = σ_gen · N / (T·(1 − F/A))**.
- (1 − F/T) equals (1 − F/A) only if A = T. That holds roughly for Z(νν) (A/T ≈ 0.9). It fails badly for W (A/T ≈ 0.3)
  and tt (A/T ≈ 0.06).

**Evidence.** Generator-only probe with the exact s4pu configuration (`scratchpad/r2/hadfail_probe.py`):

| process | T | A | F | F/A | F/T | σ (fixer formula) | σ (correct) | ratio |
|---|---|---|---|---|---|---|---|---|
| Wtaunu_j | 3000 | 910 | 227 | **0.249** | 0.076 | 5.79 pb | 7.13 pb | **1.23** |
| ttbar_1l | 8000 | 470 | 111 | **0.236** | 0.014 | 2.39 pb | 3.09 pb | **1.29** |
| Wenu_j | 2000 | 574 | 136 | **0.237** | 0.068 | 4.08 pb | 4.98 pb | **1.22** |
| Znunu_j | 1500 | 1369 | 322 | **0.235** | 0.215 | 14.37 pb | 14.76 pb | 1.03 |

- The failure fraction per attempt is process-independent: 0.235-0.249. The investigator also quotes "24-25 % of
  hadronisation attempts".
- The corrected Z value, ≈ 14.3-14.8 pb, matches p6's 14.56 pb better than the stored 13.89.

**Knock-on.**
- `normalise.py` hard-codes SIG_TAU_L = 1.89 and SIG_TAU_H = 3.56 pb (investigator numbers, same formula).
  - The fixer's own 3000-event run gives σ(Wτν) = 5.76 pb, so τ_l = 5.76 × 1099/3000 = 2.11 pb, already 10 % above 1.89.
  - Corrected: τ_l ≈ 2.57 pb (×1.36) and τ_h ≈ 4.2-4.4 pb (×1.2).
- Recomputing `normalisation.json` with f_att = 0.24 gives **N_trig ≈ 3.98e7, not 3.63e7 (+9.6 %)**. The breakdown,
  in units of 1e6:

  | process | now | corrected |
  |---|---|---|
  | Z | 24.9 | 25.6 |
  | W τ_l | 1.66 | 2.25 |
  | W τ_h | 4.27 | 5.15 |
  | W e | 1.92 | 2.34 |
  | W μ | 1.81 | 2.20 |
  | tt | 1.72 | 2.23 |

- Every N_trig-scaled term (B_PU, PC-19 SR-T, C′) is about 10 % low.
- B_SM is low by:
  - ×1.23-1.36 for the W(τ_l) and W(τ_h) terms;
  - ×1.29 for tt;
  - ×1.22 for the W(e/μ) proxies.

**Why A.** This is a definite computational error in an input cross section, in the anti-conservative direction.
It exceeds 20 % on three SM terms. It is not covered by "the ±30 % nuisance", which is a width and not a central-value
licence.

**Fix (cheap).**
1. In `generate_counted`, also count A (the tries that reach `forceHadronLevel`). Use
   σ = σ_gen·N·A/(T·(A − F)) in `mode_nt` and `merge`.
2. Re-run `nt` with the same seed tags. The event streams are deterministic, so f_presel and the rates are unchanged;
   ≈ 50 CPU-min.
   - Minimal alternative: rescale the stored σ by (1 − F/T)/(1 − f_att), with f_att measured per process from a
     counted re-run.
3. Replace the hard-coded SIG_TAU_L/SIG_TAU_H by values from the same run:
   - σ_τl = σ(Wtaunu_j) × N_lep/N;
   - σ_τh = the pooled estimate from σ(Wtaunu_j) × N_had/N and σ(Wtauhnu_j) × 0.648 (or the larger of the two).
4. Re-run `normalise`, re-freeze, and log the change. If D3's "/(1 − r)" text in `ambiguities.json` is meant
   literally, amend it to the per-attempt reading.

## 2. Category B

### B-1: N_trig is not demonstrably an upper value (WP_RULE l.326, item D1 "omitted processes")

- **(i) Missing processes.** tt̄ 2ℓ, single top and VV are **not** in N_trig, but the frozen rule says they "enter
  N_trig only". This is flagged (`normalisation.json n_trig.not_included`, FIX_R2 "OPEN"), but it is anti-conservative.
  - My rough expectation is a few % of N_trig (tt̄ 2ℓ with τ_h survives because no τ_h veto is applied; ZZ → ννqq;
    WZ; tW).
  - Not computed, so UNVERIFIED.
- **(ii) Ideal vetoes.** The generator-level e/μ/γ veto is 100 % efficient for prompt, isolated objects in |η| < 2.5.
  A realistic veto (ID efficiency < 1) lets more W(ℓν)/W(τ_l) events through.
  - Example: W(eν) has 3361/5000 vetoed. At a 95 % veto efficiency, f_presel rises by ≈ 0.03 (≈ +30 % on that process),
    which is ≈ +4 % on N_trig.
  - So the "each proxy is the looser choice" statement is not true for this one. Here the dropped τ_h veto
    (+W τ_h events) partly compensates.
- **Recommendation.**
  - Generate the three missing processes at generator level with the same `presel`. This is a few CPU-min and can share
    the A-1 re-run.
  - Or add a flagged, logged conservative allowance (e.g. ×1.10 on N_trig).
  - Tell the user that the vetoes are modelled as ideal.

### B-2: gaps in the freeze and refusal logic (R1 B-8 hygiene)

- **(i) `--inputs`.** Any normalisation file is accepted. `freeze_status()` checks the frozen
  `inputs/normalisation.json`, but `run_all` l.268 reads `a.inputs`, which can be any path. Signal and limits are then
  neither refused nor DEV-stamped. The manifest records the content, but nothing enforces it.
- **(ii) Upstream provenance in `limits_stage`.** It checks only T_seed in the upstream `manifest.json` files
  (`--signal-from`, `--bkg-from`); it ignores their `freeze.match` and `dev`. The background, srt and wp stages never
  refuse on a freeze mismatch (by design). Two consequences:
  - a DEV `signal_eff.json` can produce a `limits.json` with `dev: false`;
  - so can a background built with unfrozen code or inputs.
- **Fix.**
  - Refuse (or force DEV) unless `Path(a.inputs).resolve()` is the frozen file.
  - In `limits_stage`, refuse without `--dev` unless both upstream manifests have `freeze.match` true and `dev` false.

## 3. Category C (notes)

- **C-1 Missing OOT files.** `srt.signal_srt` skips OOT lookups whose B1 file is missing (`n_lookups_missing_file`;
  11/300 on G3). The veto then cannot act, so ε_SR-T is slightly too high.
  - Conservative alternative: no SR-T credit for a row with a missing-file crossing, or re-draw.
  - At minimum, report the fraction in `signal_srt.json`.
- **C-2 Independent MET smearing in `smregen`.** The SM preselection weight uses an MET smearing
  (`hseed('presel', sd)`) independent of the production road's MET (`run_stage4.py:376`; φ is stored as
  `trials.phimet`).
  - min Δφ and MET > 250 are therefore decorrelated from the actual road by ~25√2/MET ≈ 0.15 rad.
  - This is second order, and probably conservative (preselected events can have roads nearer jets).
  - Using the stored `trials.phimet` for the Δφ part would make it exact.
- **C-3 Weights only at the base.** Preselection weights enter only the SM base count; the chain conditionals are
  unweighted. Likewise, the C′ spectrum fold R_t is measured only at one rung, plus f_pre. Both are acceptable
  approximations under D1/D2; label them.
- **C-4 PV-line σ_ln missing.** WP_RULE l.319-320: "P_PV-line … is varied with the PV-line tolerance in the NI σ_ln".
  This is not wired (`rates.sigma_ln = 0`). The central 0.22 is an upper value, so the effect is small. Add the term,
  or log why not.
- **C-5 Hash coverage.** Not in the freeze or in A.3: `code/s4pu.py` (used at analysis time by `smregen`),
  `code/s4cp.py`, `code/s4sig.py`, `jobs/C1.json` (sets N_B1 for the OOT assignment). Also, `sm_regen.json` in the
  output directory is reused as a cache without a hash.
  - The `hs_met` check and the φ_MET replay protect most of this.
  - Adding them to `IMPORTED_FROZEN` costs nothing.
- **C-6 W(eν)/W(μν) proxy.** "Conservative" is plausible but not shown: at high W pT the τ_h products are collinear
  with the MET road, which makes max(τ_l, τ_h) a likely upper bound. Keep the flag, and report
  `_proxy_fraction_of_B_SM` to the user.
- **C-7 `hadron_ancestor`.** The 400-visit cutoff returns "prompt", which makes the veto tighter. Negligible.
- **C-8 `gen_d123` cosmetics.** The `minbias.rel_stat` formula reduces to 1/√n, and `sum_w`/`sum_w2` in `minbias` are
  copied from the last process. Both are informational only.
- **C-9 Unpersisted R_t.** The FIX_R2 R_t values (γ 0.011 … looper 1.0) are not persisted anywhere. They are recomputed
  in `background.json` `cprime.*.spectrum_reweight` at the C1b run; check there that looper R_t ≤ 1.

## 4. Verdict

**ITERATE.** One Category A:
- **A-1:** σ_SM is corrected for hadronisation failures per try instead of per hadronisation attempt. Effects:
  - W(τ), W(e/μ) and tt cross sections are ×0.78-0.81 low;
  - the hard-coded σ_τl/σ_τh are low as well;
  - N_trig is 3.63e7 instead of ≈ 3.98e7.

The fix is local: `gen_d123` counts A, ≈ 50 CPU-min re-run, then `normalise` and re-freeze. It should share one re-run
with B-1(i). Neither is blocked by production. Everything else of R1 is genuinely resolved.
