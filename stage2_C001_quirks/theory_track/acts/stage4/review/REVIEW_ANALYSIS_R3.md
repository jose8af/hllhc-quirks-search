# REVIEW_ANALYSIS_R3: narrow verification of FIX_ANALYSIS_R3 and the Stage-5 additions

| | |
|---|---|
| Date | 2026-10-14 (~10:00-10:30) |
| Reviewer | fresh critical reviewer, narrow verifier (spec `jfc/src/agents/critical_reviewer.md`, `methodology/03-review.md`) |
| Target | `review/FIX_ANALYSIS_R3.txt` against `REVIEW_ANALYSIS_R2.md` (A-1, B-1, B-2); Stage-5 additions (`analysis/products.py`, `stats.expected_limit_toys` bands, `inputs/schema.json` v2, `run_all` stage `products`); freeze `inputs/analysis_freeze.json` (25 files) |
| Signal values | **not looked at**. Code paths only; no signal efficiency or acceptance value was read. The only Stage-3 number read is the pooled Stage-3 status-code share (bookkeeping), quoted coarsely. |
| Checks run | All at nice 15, one process, < 10 s CPU each. (1) Freeze re-hash. (2) Recount of σ from the stored `gen_d123_r3.json` counters. (3) Refusal-path probes of `run_all.main` / `limits_stage` in the scratchpad (`r3/b2_probe.py`, `r3/b2_probe2.py`). (4) `selftest` (PASS). (5) A.3 re-hash. (6) Stage-3 row identity across Λ, the jets layout and the status shares. |
| **Verdict** | **ITERATE: 0 A, 2 B, 8 C** |

## 0. Verified (no finding)

### Freeze

- 25/25 files of `analysis_freeze.json` re-hash to the stored values.
- The freeze file itself hashes to `8322b8409ead…7069fc`.
- `selftest` reports `freeze: true` and SELFTEST PASS, including the 5 new B2_* tests.
- Coverage:
  - all 14 `analysis/*.py` files;
  - the 5 `inputs/*.json` files (`fix_r1.json` is excluded; it is not read by the code);
  - the 6 imported files (`g3/analyse_g3.py`, `g3/srt_tmin_check.py`, `code/s4pu.py`, `code/s4cp.py`, `code/s4sig.py`,
    `jobs/C1.json`).
- `normalisation.json` records the sha256 of its generator source (`gen_d123_r3.json` 04a65379…), so that source is
  covered transitively.
- The admissibility inputs are sha-checked in `Admissibility.__init__`.

### A-1: RESOLVED

- **Code path.**
  - `gen_d123.generate_counted` increments `attempts` exactly at the tries that reach `forceHadronLevel`, after the
    parton-level pre-filters. Those filters are the tt nlep filter and PRE_MET = 150, in the same order as
    `s4pu.HardScatter.generate`.
  - The counter is per call and is returned for the accepted event.
  - `mode_nt` and `merge` both use σ = σ_gen·N/(T·(1 − F/A)).
  - `merge` refuses inputs that lack `attempts`.
  - The hard-coded SIG_TAU_L/SIG_TAU_H literals are gone. They are derived in `normalise.build` from the same run.
- **Discriminating check: recount from the stored counters.** All 11 processes reproduce the stored
  `sigma_MET200_pb` exactly from σ_gen·N·A/(T·(A − F)). F/A lies between 0.229 and 0.262 for every process (Z 0.240,
  Wτ 0.249, tt1l 0.229, …).
- **Comparison with my independent R2 probe** (correct formula):

  | process | R3 run | R2 probe |
  |---|---|---|
  | Wτν | 7.10 pb | 7.13 pb |
  | Weν | 5.21 pb | 4.98 pb |
  | Zνν | 14.27 pb | 14.76 pb |
  | tt1l | 3.50 pb | 3.09 pb (470 attempts, ~10 % stat) |

  All agree within statistics.
- **τ_h class.** σ_τh = max(σ(Wτν)·f_h, σ(Wτ_h sample)·f_h).
  - The first term is the unbiased estimator.
  - The second term is biased low by P(MET|h)/P(MET) < 1, but the max always picks the larger.
  - The result, 4.50 pb, is ≥ the BR-based 6.59 × 0.648 = 4.27 pb. That is conservative.
- **D3 text.** `ambiguities.json` D3 is amended to the per-attempt reading.

### B-1: RESOLVED

- **(i) Missing processes.**
  - tt 2ℓ, single top t-channel, WW, WZ and ZZ are generated with the same pre-filters and the same `presel`
    (`EXTRA`, injected at run time; `s4pu.py` is unchanged and its hash is frozen).
  - They enter `n_trig.breakdown` as 0.21, 0.11, 0.13, 0.14 and 0.10 (×10⁶).
  - Each gets a flagged proxy B_SM = N_trig,p × max P(r | preselected) in `background.sm_term` l.732-756.
  - A proxy row whose source is missing becomes "missing cross section" in `wp.sm_terms`, so the B sum becomes
    incomplete and limits refuse. That is safe.
  - `_proxy_fraction_of_B_SM` is reported.
- **(ii) Veto inefficiency.** It is the event weight 0.05^n_veto inside `presel`. `presel` feeds both N_trig and the
  `smregen` B_SM weights, so they stay on one footing.
- **N_trig.** The breakdown sums to 4.085e7 (rel. stat 2.0 %).

### B-2 (i): RESOLVED

Probed with `r3/b2_probe.py`:

| case | result |
|---|---|
| an identical copy of `normalisation.json` at another path, no `--dev` | REFUSED |
| the same with `--dev` | runs; manifest `dev` true, label "DEV…", `freeze.match` false, mismatch entry "--inputs … (not frozen)" |
| the frozen file via a relative path | accepted (non-DEV) |
| the frozen file via a symlink | accepted (non-DEV) |

### B-2 (ii): resolved for explicit upstream directories only (see B-1 below)

Called directly, `limits_stage` refuses in each of these cases:
- the signal manifest has `dev` true;
- the background manifest has `freeze.match` false;
- the background manifest has no `freeze` key.

With `--dev` it propagates DEV into `limits.json` (label "DEV…", `dev` true).

### Acceptance × ε factorisation for the primary (A2) chain: CLEAN

These definitions were checked in the code:

- **A** (`products.acceptance_point`):
  - denominator: Σw over **all** template-half events of the point;
  - numerator: w × 1[in_eta25] × ⟨ε_trig·pass⟩ over 20 MET-smearing replicas;
  - the trigger weight, MET > 250, the jet > 100 / |η| < 2.4 requirement and min Δφ > 0.5 are identical to
    `gen_d123.presel` (and therefore to N_trig);
  - MET_true = pT(QQ̄), the same definition as `signal.met_reco`;
  - the jets layout (pT, η, φ, m) was verified against `convert_hepmc.py:19`.
- **ε_A2** (`signal.eff_table`): the denominator is every template-half, in_eta25 row (`run_g1b` l.115:
  `template=True, counting=True, status1=False`). Status ≠ 1 rows count as failures, and nothing applies the trigger,
  preselection or veto.
- **Factor ledger:**

  | factor | where it enters |
  |---|---|
  | ε_fid | A only |
  | ε_trig, ε_presel | A only |
  | ε_status | ε only |
  | ε_finder (incl. f_CKF < 0.2) | ε only |
  | ε_PV-ID | 1 (labelled) |

  No factor appears twice and none is missing. This is plan §3's chain.
- **Limits.** `limits_stage` uses only sample A2. Its s_c = ε_c, and b is in events after trigger and preselection
  (B = N_trig-scaled). The limit μ is therefore "signal events in the trigger + preselection acceptance", and
  σ_95 = μ_95/(L·A) is consistent.
- **Same events across Λ.** Stage-3 rows are the same production events at every Λ (checked: `p2/F_m1000` L1 vs L2,
  identical rows and p_qp). So:
  - A at Λ is evaluated on the same events as the A2 rows, which were drawn from the Λ = 0.45 point;
  - the joint-across-Λ row bootstrap in `edges` is legitimate for A1 too.
  - All 40 A2 (species, Λ) Stage-3 points exist, so no acceptance entry silently drops out.

### Toy bands, schema v2 and the other new outputs

- **Toy bands.** `expected_limit_toys` solves CLs at the 2.3/16/50/84/97.7 % quantiles of the b-only Q distribution,
  using the same CRN toys.
  - For one bin this equals the quantiles of μ_up, because μ_up is monotone in n.
  - For two bins it is the usual approximation (the weights depend on μ).
  - The median is unchanged from R1.
  - The labels say "quantiles of the b-only test statistic; discrete at small B". That is adequate.
- **Schema v2.** It lists the new keys. `validate_outputs` checks the top-level keys.
- **edges_det.** Half-maximum crossings in ln Λ, joint row bootstrap, labelled. It is not logistic as the proposal
  says, but it is labelled as half-maximum.
- **sep_it_det and event_display.** Numbers only, no selection is fed back, so they cannot bias results.

## 1. Category A

None.

## 2. Category B

### B-1 (residual of R2 B-2 (ii)): with the default `--signal-from`/`--bkg-from` (= `--out`), the upstream provenance check reads the manifest that the current run has just overwritten, so stale DEV outputs pass as non-DEV

`run_all.main` l.477 writes **this** run's `manifest.json` into `--out` before it calls `limits_stage`. `limits_stage`
then reads `sig_dir/manifest.json` and `bkg_dir/manifest.json` as the "upstream" manifests, and by default both
directories are `--out`. Any `signal_eff.json` or `bsum_wp.json` left in that directory by an earlier `--dev` run (or
by unfrozen code) is therefore certified by the current run's `freeze.match: true, dev: false`.

**Demonstrated** (`scratchpad/r3/b2_probe2.py`):
- Setup: an `--out` directory holding a DEV manifest, a DEV-labelled `signal_eff.json` and a `bsum_wp.json`.
- Run: a frozen `run_all --campaigns C1 --stages limits` without `--dev`.
- Result: the manifest is overwritten to `dev: false`, and the upstream check passes.
  - With an incomplete B sum the refusal came only from "B sum incomplete".
  - With `complete_inputs` true, `limits.json` was written with **`dev: false`** and no DEV label.

**Same gap in the `products` stage.** `products` reads `out/signal_eff.json`, `signal_rows_*.npz` and
`signal_obs_*.npz` whatever produced them. It stamps `acceptance.json`, `edges_det.json` and `sep_it_det.json` with the
current run's `dev` flag, so a stale DEV `signal_eff.json` also yields non-DEV Stage-5 inputs.

R2 B-2 (ii) asked for exactly this to be impossible. The explicit-directory path is fixed, but the default path is not.

**Fix (cheap).** Choose either option:
1. **Embedded stamp.** Have the producing stages stamp their own outputs: `signal_eff.json` and `bsum_wp.json` (and
   the npz files via a sidecar) get `dev`, `freeze.match` and the code/inputs sha256 at write time. Have
   `limits_stage` and `products` check those embedded stamps instead of `manifest.json`.
2. **Pre-run manifest.** In `main`, read the pre-existing `out/manifest.json` before overwriting it. Refuse (or force
   DEV) when a consumed file was not produced in this run and the earlier manifest is DEV or unfrozen.

Then add a selftest for the same-directory case.

### B-2: `acceptance.json` pairs A with A1/A5 finder efficiencies whose denominators do not match A's; for A1 the fiducial factor is counted twice, and the attached note misstates the denominator

`products.acceptance` writes an entry for every `cfg == 'BM'` point of kinds a2, a1 and a5. Each entry holds A
(template half, ε_fid included, all statuses) together with `finder_at_report_rungs` from that sample's
`signal_eff`. The `finder_note` tells Stage 5: "eps_total = A × eps_finder … over all counting rows
(|eta_pair| < 2.5, status != 1 as failures)". That is true only for A2:

| sample | ε denominator (code) | product A × ε |
|---|---|---|
| A2 | template, in_eta25, all statuses (`run_g1b` l.115) | clean |
| A1 | **both halves, all η, status == 1 only** (`run_g1b` l.299) | **ε_fid twice**; ε_status missing |
| A5 | template, in_eta25, **status == 1 only** (l.128) | ε_status missing |

- The status share is negligible: pooled Stage-3 status ≠ 1 is ≈ 0.1 %.
- The A1 double count is not negligible:
  - every point of the 307-point A1 grid would carry ε_fid once in A and again in ε_A1, because non-fiducial rows
    sit in the A1 denominator as failures;
  - this is the input for the Stage-5 "ε maps by factor" figure (plan §11 item 3; `proposed_schema` note).
- The bias is conservative (it under-states the A1 ε_total), but it is a definite factor error in a Stage-5 input, and
  the label is wrong.
- `limits.json` / σ_95 are **not** affected, because they use A2 only.

**Fix.** Choose either option:
1. Write acceptance entries for A2 keys only. The proposed schema already keys `acceptance.json` by the `signal_eff`
   **a2** key.
2. For A1/A5:
   - compute the finder ε over the A2-like denominator (A1: restrict to in_eta25 rows, with status ≠ 1 as failures;
     the Stage-3 records carry both flags per row);
   - and state the per-sample denominator in the note.

## 3. Category C (notes)

- **C-1: the factorisation ε_finder(fiducial) × A versus ε_finder | preselected.**
  - This is plan §3's chain, flagged as A43; not reopened.
  - The sign of the correlation is not established:
    - the φ_MET road resolution is better at high MET, which is conservative;
    - higher pair pT means higher βγ and lower dE/dx against the e_adm levels, which could be anti-conservative for light
      quirks.
  - The exact check is free: weight each A2 row by its truth preselection weight. MET_reco per row is reproducible
    from `hseed('sig-pvmet', …)` (`signal.met_reco`), and the jets come from the Stage-3 record. Report
    ε_w/ε at the report rungs.
  - Recommended as a cross-check before Stage 5, not required.
- **C-2: the tW allowance, 0.10 × N_trig(tt 1ℓ + 2ℓ) = 0.26e6 (0.6 % of N_trig).**
  - It is the *inclusive* ratio σ(tW)/σ(tt̄) ≈ 0.085-0.09 at 14 TeV, rounded up (my recollection; UNVERIFIED). It is
    not a high-MET tail ratio.
  - It inherits K_tt = 1.9 implicitly.
  - "Conservative" is not demonstrated, but the term is immaterial: even ×2 is +0.6 % of N_trig, inside the 2 % stat.
  - It is adequately flagged (UNVERIFIED in A37, `allowance: true`, "[N_trig is itself an ALLOWANCE]" in the proxy
    flag).
- **C-3: the flat 5 % veto inefficiency (A38).**
  - It is a plausible central value for prompt isolated e/μ, but not demonstrably conservative. Loose e/γ veto
    inefficiencies at PU 200 can be 5-10 % (UNVERIFIED).
  - Sensitivity (R2 estimate): each extra 5 % adds ≈ +4 % to N_trig, through W(eν)/W(μν).
  - The omitted τ_h veto and K at the rule top partly compensate.
  - A38 should carry ESTIMATE/UNVERIFIED and this sensitivity, and the user should be told that the vetoes are modelled
    as 95 % efficient.
- **C-4: stale text in frozen files.**
  - `normalisation.json` `n_trig.not_included` still says "tt 2l, single top, VV … not generated".
  - The `normalise.py` docstring l.6-8 still gives 1.89/3.56 pb and "NOT generated".
  - The `gen_d123.py` docstring l.20 still gives the old per-try formula.
  - `n_trig.topups` lists `gen_d123.json`, which is actually the **min-bias** source (`minbias=`), not a statistics
    top-up.
  - All are cosmetic, but they appear in a user-facing frozen input.
- **C-5: processes outside the rule list.**
  - Z(ττ)+j, Z(ℓℓ)+j with both leptons lost, and QCD multijet with fake MET are not in N_trig. Each is typically
    ≲ 1-2 % of monojet-like signal regions (UNVERIFIED).
  - The current composition (Z 61 %, W 30 %, top 7 %, VV 1 %) looks monojet-like, and K_V = 1.4 at the rule top leaves
    headroom.
  - Mention this to the user.
- **C-6: freeze coverage edge.**
  - `acts/stage4/finder/{finder,weights,production}.py` are imported at analysis time.
  - The `products` stage reads `data/sim_stage3/STAGE3_INDEX.json` and `sim/stage3/results/P2.json`.
  - These are A.3-hashed and currently match: I re-hashed all 21 A.3 files, and only `run_stage4.py`/`run_chain.py`
    differ, both HASH_ADDENDUM-allowed. But they are not checked at analysis run time, and the Stage-3 chunk npz files
    are not hashed at all.
  - Adding the A.3 check (or these paths to IMPORTED_FROZEN) is free.
- **C-7: `sep_it_det` definition.**
  - It takes the median over matched *candidates*, not events, and f_CKF < 0.2 is not applied.
  - That is fine for a calibration, but label it in the file.
- **C-8: VV / single-top pre-filter.**
  - pT̂ > 150 on 2→2 diboson and single-top cuts ISR-boosted configurations in which each boson is soft. This is the
    same convention as the frozen production samples.
  - The effect on N_trig is ≪ 1 %. Note only.

## 4. Verdict

**ITERATE: 0 A, 2 B, 8 C.**

R2 A-1, B-1 and B-2 (i) are genuinely resolved: σ is per attempt and recounts exactly, the missing processes and the
veto allowance are in, and `--inputs` is refused. The primary A2 chain σ × L × A × ε factorises cleanly.

The two B items to fix:
- **B-1:** the default same-directory path still launders DEV upstream outputs into non-DEV `limits.json` and Stage-5
  products. This was demonstrated.
- **B-2:** `acceptance.json` combines A with the A1/A5 finder ε on mismatched denominators: ε_fid is counted twice for
  A1, and the note is wrong.

Both fixes are local, need no CPU, and need no re-freeze of physics inputs; only code and a selftest change.
