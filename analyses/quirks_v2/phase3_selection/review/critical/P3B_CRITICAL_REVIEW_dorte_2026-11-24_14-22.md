# P3B critical review: work package p3-b (B2 pile-up), Phase 3, 1-bot review

Reviewer Dorte (Opus, critical reviewer), session start 2026-11-24 14:22 -0500 (`date`), session log
`phase3_selection/logs/reviewer_dorte_2026-11-24_14-22.md`. I did not open any signal sample.

Artifact: `phase3_selection/outputs/P3B_PILEUP_casper_2026-11-24.md` ("P3B"). Also read: code `src/p3b/` (closure.py,
thin_core.py, occ_model.py, occmod_job.py, refind_job.py, refind_cmp.py, and `production.process_trial` /
`weights.group_sets` of the chain), outputs `outputs/p3b/*.json` and `SCHEMA.md`, figure `b2_dev_lnr.png`, executor log
`logs/executor_casper_2026-11-24_10-19.md`, the p3-b part of `experiment_log.md`, ledger markers `p3-b-*`, SLOTS.md.
Frozen texts: STR §4.0 points 1-8 (l.340-548), §4.5 (l.1119-1228), §4.12 table (l.1870-1882), §4.17 rows 1, 2, 12, 14,
15 (l.2093-2112), §11.7 (l.2713-2780); COM l.184-190, l.340, l.351; EXP §5.6, §9 item 7, §10 items 8, 10. Advisor
ruling `review/advisor/ADVISOR_B2CAP_freja_2026-11-24_14-23.md` (its two questions to me are answered in §1).

Tags: [V] I re-derived it (command or file cited); [U] taken from the artifact unchecked.

## 0. Verdict

**Headline "both pile-up estimators are above the cap" — CORRECT as computed, and it does not depend on any open
reading.** I reproduced every number the headline rests on, recounted the direct reference from the raw C1 trial
records, and re-implemented the thinning independently (§2). Every evaluable development rung of repaired thinning is
on its own above the cap (smallest |ln r| = 0.234, at R04⊗2S≥3). So the r.m.s. is above 0.135 whatever rung set is
used. For the occupancy model every allowed variant gives 0.32-0.52. I found no code bug that could make either
excess.

The artifact still needs fixes before PASS. It **over-reads two frozen rules**: rule 1 is called "met" (P3B §8.1), and
rule 2 becomes "not submitted unless ordered". It calls the occupancy "cause" identified, but that cause is a
restatement. It leaves out the no-credit value and the second reading of the day-15 term. It presents an importance
sampling result at R08 that is checked against only one plain Monte Carlo toy. It rewords a frozen MUST sample as "not
requested". Its experiment log is nearly empty.

Counts: **A 1, B 9, C 6.**

## 1. Answers to the advisor's two questions

**(1a) Thinning, R1: a demonstrated cause? — YES as an operational cause of the excess; NO for the named mechanism.**
- What R1 shows [V: `b2a_refind_control.json`; code `refind_job.py` read]. It uses 400 ρ = 2 trials, replayed bit for
  bit; the PV, φ_MET and trial seed are checked, and the job raises if they differ. Each interaction is kept with
  probability ½, the same unit as thin_core. The frozen ρ = 1 `process_trial` then runs on the kept pool.
  - Re-found against the independent direct sample: ln = −0.032 ± 0.032 (R04), −0.069 ± 0.035 (R05), +0.048 ± 0.104
    (R06, 104 counts).
  - Candidate-level thinning against re-found, on the same trials (paired): +0.306 ± 0.009, +0.399 ± 0.011,
    +0.741 ± 0.104.
  - So the sample (two independent ρ = 1 chain events per ρ = 2 trial) and the thinning unit reproduce a ρ = 1 pool.
    The whole excess comes from one step: thinning keeps the ρ = 2 finder candidates, drops hits and regroups, instead
    of re-running the ρ = 1 finder. That is a cause in the sense of STR l.2759, because it points to a specific
    redesign (P3B §8 option (a)). R1 is itself that redesign run on 400 trials.
- What R1 does **not** show is why the finder keeps fewer distinct sets. P3B §3.3 names "seeding, 3-iteration refit from
  its own seeds". That is an inference:
  - R2, the only test aimed at the refit and dedup, failed its own q = 1 sanity check. It gives 2,361 / 2,644 groups
    against the stored 2,731 / 3,061 [U, session log l.141-144]. So it neither supports nor excludes the refit.
  - No seed-survival test was made, and no matching of thinned groups to re-found groups by hit overlap.
  - `refind_job.py` stores only counts per column, not the re-found hit sets, so that matching cannot be done on the
    existing outputs.
  - P3B §3.3 should say "localised, mechanism not isolated" (finding B6).
- Statistical reach: at R06 the re-found/direct test has σ = 0.10. It excludes an R06 sample offset of the size of
  the excess (0.77), but not one of 0.2.

**(1b) Occupancy model, O4: a demonstrated cause? — NO. O4 is a restatement; O3 is a weak (≈ 1.8σ) localisation.**
- By construction (closure.py l.236-242), B(r) = N_cfg·C(R05)·E_model(r) and C(R05) = P_real(R05)/E_model(R05). So
  "N_cfg(r) = B_dir(r)/P_real(r) is rung-dependent" (O4) is the closure failure in other words: the in-sample R05
  residual (−0.166) and the held-out R06 residual (+0.355) re-expressed [V: re-derived from `b2_dev_closure.json`,
  §2.3]. It does not say why the number of finder-distinct groups per passing random ribbon changes with width.
- O3 holds the real evidence. The semi-analytic arithmetic follows random ribbons on real ρ = 1 hits to a constant
  factor: C(R04) = 1.184, C(R05) = 1.207, C(R06) = 1.24 [V: P_real/E_model from the JSON].
  - C(R06) rests on **31** passing real planes (±18 %). So C(R06)/C(R05) = 1.03 ± 0.18 against the excess factor
    e^0.355 = 1.43.
  - The arithmetic is therefore exonerated only at about 1.8σ: ln 1.43 − ln 1.03 = 0.33, against σ ≈ 0.18.
- Nothing tests a mechanism. The obvious candidate is that the finder refits its planes to the hits while the model
  scores fixed random planes, so the width distribution of found planes differs from that of random ribbons. It is not
  examined.
- A cheap diagnostic that needs no direct count would make the localisation firm: rerun `occin` with 10× the random
  planes (≈ 15 CPU-h at the measured 1.54 CPU-h per 1,000 planes/trial). That gives ≈ 300 real R06 planes and C(R06)
  to ±6 %.
- Until then, rule 2's "a cause is found" stands for the occupancy model only as the hypothesis "the
  configuration-to-group map, not the occupancy" (finding B6). If the orchestrator orders redesign (b) anyway, as the
  advisor's point 3 does, that is the orchestrator's reading of rule 2. It should be labelled so, not described as
  resting on a demonstrated cause.

**(2) s_model rung set for thinning: every reading is above the cap [V].**

| reading | value |
|---|---|
| cumulative evaluable R04-R06 | 0.506 |
| with the crossing rungs | 0.536 |
| R04-R05 only | 0.291 |
| R04 alone | 0.259 |
| the single smallest evaluable rung (R04⊗2S≥3) | 0.234 |

All exceed 0.135. Adding the non-evaluable R07 (+1.47) only raises the value. For the occupancy model every allowed
variant is above the cap: 0.355 (primary), 0.374 (trend of C), 0.349 / 0.389 / 0.521 (N_cfg variants, O2 [U]), 0.322
(R06⊗2S≥3), ≈ 0.40 with the plain Monte Carlo E_model at R06 [V: E_model_plain(R06)/E_model(R06) = 1.046].

**(3) Times (STATE §0.7) — inconsistent; finding B9.**
- The artifact header says "10:19–14:30 -0500 (`date`)". The artifact file mtime is 14:20:23 and the commit f881aa3
  is at 14:21:04 [V: `ls --time-style`, `git log`]. 14:30 lies after both, so it was not read from the clock.
- The session-log entry "13:30" quotes "N_eff … R08 0 (one passing subset in 128,000)". The thin outputs have not
  changed since 13:23:07 (last marker), and they contain **4** passing R08 subsets [V: §2.1]. The artifact's "N_eff
  4.1, four passing subsets" is correct, so the 13:30 log line does not describe these data.
- The same log has two headings the executor himself corrected (10:58/10:59 → 10:56).
- The other times are consistent with the evidence I checked:
  - `src/p3b` mtimes: test_thin.py 10:22:03; occ_model.py / occmod_job.py 10:37:14; pileup_term.py 10:56:12.
  - Markers: thin 10:36-13:23, direct 13:25-13:28, occin 11:03-13:34, occmod 13:40-13:54, refind 13:38-14:16.
  - The occmod outputs record code sha256 values equal to the current occ_core/occ_model/occmod_job files. So the
    model code ran unchanged from before the 10:56 freeze.

## 2. Re-derivations (maxwell, 1 process, nice 19; script `review/critical/dorte_rederive.py`, output
`review/critical/dorte_rederive.json`; SLOTS.md line 14:25)

### 2.1 Aggregation and double counting [V]
- `p3-b-thin`: 50 files, 2,000 trials, **2,000 unique** (job, event, road) keys, 1,000 events.
- `p3-b-direct`: 4 files, 16,000 trials, **16,000 unique**, 4,000 events. No trial is counted twice.
- Rates per trial, thinning / direct:

| rung | thinning | direct |
|---|---|---|
| R04 | 221.4188 | 170.8564 |
| R05 | 68.0635 | 49.4557 |
| R06 | 0.53722 | 0.247875 |
| R07 | 1.898×10⁻³ | 4.375×10⁻⁴ |

- ln r = +0.2592 / +0.3194 / +0.7735 / +1.468, r.m.s.(R04-R06) = 0.5058. These equal P3B §3.2 and the JSON.
- R08: 4 passing subsets of 128,000 (3.125×10⁻⁵ per trial).

### 2.2 Direct reference, independent of `direct_job.py` [V]
- I summed `trials.n_grp[:, 3:7]` over the 200 raw C1 files `p2-a-c1-pu1/000/c1pu1-*.npz`: 16,000 trials and
  2,733,703 / 791,291 / 3,966 / 7 groups at R04-R07, identical to `p3-b-direct`.
- The reference is the C1 ρ = 1 sample (stream `c1.pu1`). It is independent of the thinning input (`c1.pu2`) and of
  the R1 re-find (also `c1.pu2`).
- For the occupancy model the reference is the **same** 4,000 events as its inputs (densities, P_real, N_cfg). That is
  allowed by STR l.1145-1148 (development R06 on the development sample) and is handled by the joint event bootstrap
  (closure.py l.188-194, `same_events_as_direct: true`).

### 2.3 Occupancy and day-15 numbers from the JSON [V]
- C(R04) = 1.18386, C(R05) = 1.20684. In-sample ln r = +0.00628 / −0.16644, r.m.s. 0.1178.
- R06: N_cfg·C(R05)·E(R06) = 0.35345 per trial → ln r = +0.35481. Trend variant +0.37403.
- Day-15: ln A = 12.0873; R07 / R08 / R09 = 5.47×10⁴ / 346.95 / 4.112 events at N_trig 4.0848×10⁷. All as P3B.
- The B2-b (R04-R05-normalised) model gives **R08 = 443.3, R09 = 5.25 events**. The no-credit value is 485 events,
  i.e. N_trig·1.14/96,000; with the 16,000 development trials it would be 2,910.
- The plain Monte Carlo E_model at R08 (6.04×10⁻¹⁰, against IS 4.78×10⁻¹¹) would make the day-15 R08 term **4,383
  events** (finding B3).

### 2.4 Thinning re-implemented independently [V]
**Method.** `dorte_rederive.py` part C rewrites the thinning without the executor's kernels:
- plain numpy for the counting variables and w_core (1.4826·MAD of u·n2 over the kept IP hits);
- my own leader-based grouping, with python sets and an inverted index (first qualifying group in creation order,
  ≥ ½ of the smaller set);
- my own Bernoulli(½) per interaction, with my own seed.

It takes from the chain only the geometry tables `LC_OF`/`SIDE_OF`. It runs on the first 40 trials of C1 pu2 (jobs
c1pu2-0000 to 0003), with K = 8 subsets per trial. Runtime 12.5 min wall, 584 s CPU.
- **q = 1 identity: 40 / 40 trials exact** against the stored ρ = 2 `trials.n_grp` at R04-R07 (for example
  2731/1019/2/0, 3186/1210/2/0).
- **q = ½, own / p3-b-thin on the same 40 trials:**

| rung | own | p3-b-thin | own / p3-b |
|---|---|---|---|
| R04 | 230.47 | 228.28 | **1.010 ± 0.009** |
| R05 | 69.59 | 69.11 | **1.007** |
| R06 | 0.581 | 0.601 | **0.967** (186 own subset-groups, ≈ ±0.07 [E]) |

- On these 40 trials the R06 excess over the direct rate (0.2479) is ×2.3 in my implementation too.

**Conclusion.** The ×2.17 thinning excess at R06 is not an implementation artefact of the grouping, the
interaction-level draws, the rung recount or the normalisation. It belongs to the frozen estimator definition, as R1
also shows.

### 2.5 CPU [V]
- Markers, terminal rows summed: thin 1.392, direct 0.015, occin 1.541, occmod 0.478 (9 rows including the replaced
  occmod-000 attempt), refind 1.317; **4.743 CPU-h**. This matches P3B §1.
- My own use: ≈ 0.17 CPU-h on maxwell (the §2.4 run 584 s; tests and the IS check a few seconds). Slot released (SLOTS.md RELEASED line).

## 3. Findings

### Category A (must resolve)

**A1. Closure-method failure of both pile-up estimators is open (JFC alarm band; STR §4.0 point 4 (c), §11.7 rule 2).**
- Thinning: (b) χ²/ndf = 4,839/14 (V_boot) and 3,392/14 (with s_model²J) [V: `b2_dev_closure.json`]. R06 is beyond
  L + 2σ_tot.
- Occupancy model: held-out pull 10.6σ (statistical) [V: 0.355/0.034].
- P3B reports both honestly, not reframed, and the JSON flags agree (`above_cap: true`, `b_verdict: FAIL`). This is not
  an executor error; it is the headline.
- By the phase-3 alarm rule it still blocks B2 from advancing until rule 2 has run. Either one redesign is tried and
  measured on a sample not yet seen, or the estimator is formally declared "not submitted" at the freeze.
- Resolution owner: the orchestrator (advisor points 3-5). Required in P3B: a closing statement of which estimator
  takes which route, once ordered.
- Recommended in addition: before any thinning re-find variant (a) is costed for the pause package, measure its N_eff
  per CPU-h on the existing 400 control trials, as the advisor asks.

### Category B (must fix before PASS)

**B1. Rule 1 and rule 2 are over-read (P3B §0, §3.3 last paragraph, §4.4 last paragraph, §8.1-2).**
- STR l.396 applies the cap rule "after trying a redesign (§11.7)". Rule 1 reads the cap status at the binding day-15
  reading (l.2744-2745, l.2756-2757). P3B §8.1 "Rule-1 pause condition met" is therefore premature.
- Rule 2 (l.2759-2760) says an estimator above its cap "is redesigned if a cause is found by day 15". P3B states
  "cause identified" for both and in the same breath "not submitted … unless the user/orchestrator orders a redesign".
  That inverts the frozen default.
- P3B §3.3 also says "no redesign that stays inside the frozen definition … is available", yet §8.2 (a) is one: the
  re-find keeps [SD4] and has no fitted parameter.
- Fix: restate rules 1 and 2 as written. Say which cause is demonstrated (see B6). Remove the internal contradiction.
  The advisor has ruled the same; the artifact text must follow.

**B2. The no-credit value of the pile-up term and its eligibility reading are missing from the artifact (STR
l.1175-1178, l.1018, l.1586-1588, §4.0 point 6, §4.12 table l.1873-1878).**
- §6 says "the frozen rule gives the term no credit" but never gives the value. The value is 485 events (68 % zero-count
  bound of the 96,000 direct trials; mean 425.5 as the frozen script draws it). It appears in `pileup_term.json`
  (`no_credit_value`) but nowhere in the text.
- §8.2 asserts "selections stay available flagged". That is the §4.0 point 6 / §4.12 "not submitted" reading.
- STR l.1176-1178 says for the both-FAIL case "no selection beyond R07 is then eligible ([SD8])", and the §4.12 table
  gives "R07-direct … 'closure fails' for pile-up".
- "Not submitted" (NOT TESTED) and "FAIL" are different classes. Which applies depends on whether a redesign is
  submitted and how it ends. The artifact must state both readings and their consequence for the R08/R09 candidates:
  every R08+ candidate carries ≥ 485 events of pile-up under no credit, against 347 / 4.1 with credit.
- It must also say which zero-count bound applies at day 15: the frozen planning value is 485 at 96,000 trials. Rule 1
  speaks of "the samples that exist at day 15", and the development sample's bound would be 2,910. That is a reading to
  flag, not to choose.

**B3. The R08 (and so R09) model value rests on importance sampling validated by a single plain toy (P3B §4.2).**
- P3B §4.2 compares IS with plain Monte Carlo at R05-R07 and reports "model MC error at R08 7 %". It omits the R08
  comparison.
- Plain E_model(R08) = 6.04×10⁻¹⁰ against IS 4.78×10⁻¹¹, a factor 12.6 [V: `E_model_plain` in the JSON].
- The plain value comes from **one** passing toy of 1.28×10⁶. Per seed the passes are 0, 1, 0, 0, 0, 0, 0, 0
  [V: occmod-00*.npz]. IS predicts 0.079 passing toys (P = 7.6 % for ≥ 1).
- At R07 plain and IS agree: 12 passing toys against 12.5 expected [V].
- So R08 is not contradicted, but it is not validated either. The 7 % is the spread of 8 IS seeds, which
  underestimates the error if the IS weights are heavy-tailed. They are:
  - the top 1 % of the stage-B configurations carry **51 %** of the R08 IS sum (27 % at R07);
  - an error estimate from the within-seed second moments (`isr[:, 3, 1]`) gives ≈ 12 % at R08 against the quoted
    7 % [E: maxwell, 8 occmod files].
- The day-15 R08 term (347 events) and R09 (4.1) scale directly with this number. With the plain value R08 would be
  4,383 events.
- Fix: report the R08 comparison. Add one validation that has power at R08, for example plain toys at an intermediate
  cut between R07 and R08, or a stratified plain run on the top-weighted stage-B configurations. Report the IS
  effective sample size at R08 from `isr[:, 3, 1]`.

**B4. The day-15 pile-up term is given under one reading only (P3B §6; PHASE3_BRIEF §2 "report the result under every
allowed reading").**
- STR l.2741 ("at day 15: the development model's R04–R07 inputs") is read as a single scale A fitted to the
  development direct counts at R04-R07. That fit includes the held-out R06 and the 7 counts at R07, with weights
  declared at 10:56 [V: session log l.117, closure.py l.282-293].
- Another reading is allowed by the text: the B2-b model with its R04-R05 normalisation (STR l.1145-1146 "using rungs
  R04–R05 only"), evaluated with inputs extended to R07. It gives R08 = 443, R09 = 5.25 [V §2.3]. R08 is in the JSON
  (`occupancy_B2b_model`); R09 is `null` there and absent from the text.
- The executor's reading also uses the held-out rung to set the normalisation. After that, R06 is no longer a check
  of the day-15 term. That is not a "×2.41 patch", but it is a fit to the deepest direct counts and should be said.
- Fix: table both readings in §6, give the R09 value of the B2-b reading in the JSON, and flag the choice for the
  orchestrator.

**B5. The planning-width column assumes an R07 test rung that the work package's own projection says will not be
evaluable (P3B §6, §3.4).**
- The "planning (cap)" widths (R08 0.427, R09 0.589) take d_in = 1, i.e. a last evaluable width test at R07 on the
  96,000-trial sample.
- P3B §3.4 projects R07 **not evaluable** at the development direct rate: 42 expected counts, σ_tot 0.159. With R06 as
  the last test rung (d_in = 2 at R08) and s_model at the cap, the planning width at R08 is √(0.135² + 4·0.405²) = 0.83,
  not 0.43 [V: arithmetic].
- The artifact presents "planning" and "measured" side by side without saying that the planning column contradicts §3.4.
- Fix: add the cap/R06-only column, or state the dependence on the R07 rate explicitly (v1 rate: evaluable; development
  rate: not).

**B6. The causes are stated beyond what is shown (P3B §0 "A cause is identified for both", §3.3 R1 "reading", §4.4
O4).**
- See §1. For thinning, write "localised to candidate-level thinning versus re-finding (7σ at R06 on the same trials);
  mechanism not isolated; R2 failed its sanity check".
- For the occupancy model, write "O4 restates the closure failure; O3 localises the problem outside the occupancy
  arithmetic at about 1.8σ (31 real R06 planes)".
- The DAILY_NOTES line ("cause identified for both … the finder keeps fewer distinct sets") and LOG l.1011 inherit the
  overstatement.

**B7. The occupancy "remediation attempts" O1-O4 are variants and diagnostics, not remediations (P3B §4.4, §10 self-check
"≥ 3 remediation attempts per failing estimator").**
- O1 is the pre-declared trend variant, O2 the normalisation variants, O3 and O4 diagnostics. None changes the model to
  remove the failure. For thinning, R2 (refit + dedup, three modes) and R3 (re-rank) are real attempts; R0 and R1 are a
  bug search and a control.
- Not changing the model was right under the frozen rules: nothing may be chosen after seeing R06, and rule 2 places
  the redesign at decision point 2.
- But the self-check claim "≥ 3 remediation attempts per failing estimator" is not true for the occupancy model.
- Fix: relabel them as robustness variants and diagnostics, say that no model remediation was attempted and why, and
  point to the rule-2 attempt the advisor ordered.

**B8. A frozen MUST sample is reworded as "not requested" (P3B §7 last bullet; STR §4.17 row 12, l.2105; budget row
l.2520).**
- The enlarged development closure sample (`dev.pu1`, ≈ 5,960 events, 100 CPU-h, Phase 3, role "development (decision
  point 2, s_model, crossing rungs)") is a MUST line of the frozen plan. STR l.1146 names it as an input sample of the
  occupancy model.
- P3B calls it "not requested" and argues it cannot change the cap status. That is true for the current models (s_model
  is a bias at 10σ), but the sample has other frozen roles:
  - it is the only held-out sample for a rule-2 redesign (the advisor's point 5 now depends on it);
  - it strengthens the day-15 "R04–R07 inputs": 7 R07 counts become ≈ 17;
  - it is used for crossing-rung evaluability.
- Not producing it is a deviation to be reported by PHASE3_BRIEF §2 (stop and report), not a waiver by the executor.
- Fix: restate it as a frozen item not yet produced (outside the 15 CPU-h budget) and hand it to the orchestrator.
  P3B's own number for R07 (≈ 31,000 events for 55 counts) shows that even this sample does not make development R07
  evaluable; say so.

**B9. Logs and times (AGENT_RULES "Working rules"; STATE §0.7).**
- `experiment_log.md` has **one** p3-b entry (10:22, the identity check). It has no DECISION / ALTERNATIVES /
  CONFIDENCE / FLAG blocks for the judgement calls of the day:
  - the occupancy definition frozen at 10:56;
  - the day-15 reading (B4);
  - the s_model rung-set readings;
  - the R2/R3 failures;
  - the [DT2] trigger (STR l.1198-1200 requires a [D] with the user informed: deepest evaluable thinning rung R06);
  - the decision not to produce `dev.pu1` (B8).
- Times: the header end "14:30" comes after the file mtime 14:20:23 and the commit 14:21:04, and the session-log
  "13:30" line does not match the data (§1 (3)).
- Fix: add the blocks, log [DT2] as a [D], correct the header time and the 13:30 entry (append a correction, do not
  rewrite).

### Category C (suggestions)

**C1. 2S credit in the "measured (dev)" widths (P3B §6, s = 3 rows).** The s_f = 0.224 credit (d_out = 0) is built from
the nine development 2S comparisons. Six of them sit on the derivation rungs R04/R05 of the same sample, which are
consistency checks (STR §4.0 point 1). Only R06⊗2S is outside the derivation. Label the column "hypothetical
bookkeeping" or compute s_f from R06⊗2S only.

**C2.** §5 puts v2 (ln(P/N)) and C1 (ln(N/P)) slopes in one table. Convert C1 to one sign convention.

**C3.** COM l.351: both estimators, the model's correlation factors and the direct counts come from the same chain, so
the closure cannot see [L15] (half-turn limit, EXP §9 item 7). Add it to §11 as a standing limitation of any B2
verdict.

**C4.** R1 has one draw per trial and stores only counts. If R1 is reused (the advisor's N_eff-per-CPU-h measurement),
store the re-found groups' hit sets, so that thinned and re-found groups can be matched. That would show the mechanism
of B6.

**C5.** The R1 re-found/direct comparison at R05 is −0.069 ± 0.035 (2.0σ). Say so, with the 2.0σ, rather than "reproduces
the direct counts".

**C6. Figures.** I concur with the plot validator (Elias) that the three figures lack an x-axis label. The physics
content of `b2_dev_lnr.png` matches the JSON. The R07 points are off-frame, as the caption says. Consider an inset or an
arrow with the value.

## 4. Checks with no finding (evidence)
- **Thinning definition = [SD4] as frozen.**
  - One Bernoulli(½) per interaction per subset, shared by all candidates (thin_core.py l.164-167).
  - Plane and axis fixed. Only aligned ρ = 2 candidates with N_IT2 ≥ 3, N_IP2 ≥ 7 are processed (l.214); thinning only
    removes hits, so no other candidate can pass R04.
  - Grouping on the kept hits with v1's `group_sets` (frac 0.5).
  - Counting "groups with ≥ 1 passing member" per column (l.193-199), as `process_trial` l.263-268.
  - K = 64 [V: thin npz shape (40, 64, 34)]. The mark array is reset per subset by the subset index (no carry-over of
    groups between subsets).
- **The q = 1 identity** holds in my independent implementation on all 40 trials of §2.4, against `trials.n_grp` of the
  stored ρ = 2 records.
- **Occupancy IS estimator.**
  - The weight is the exact inverse of the window-mixture proposal. Units in categories with no mass in a window carry
    factor 1 there, which matches β = 0 for those units.
  - The proposal keeps full support through the (1 − β)g component.
  - Stage B is resampled ∝ P_R04, so E = E[P_R04]·mean_B[P(w | R04)] is unbiased (occmod_job.py l.90-92; closure.py
    l.199-212).
- **Frozen before comparison.**
  - The occupancy definition (session log l.111-118) is implemented as written in closure.py: C held at R05, trend
    variant, GLS N_cfg on R04-R05, s_model = max(|ln r(R06)|, r.m.s.), day-15 weights.
  - The model code ran with sha256 values equal to the current files, last modified 10:37 (before the freeze).
  - No variant was adopted after R06 was seen. O2/O3 and R2/R3 are labelled diagnostics.
  - The executor saw direct R04-R06 counts of one file during the 10:10-10:19 inspection, and the C1 rates were known
    from Phase 2. Neither enters a free parameter.
- **s_model definitions** match STR l.390-392 (thinning: r.m.s. of development ln r; "every comparison is a test",
  l.1138-1139) and l.1146-1148 (occupancy: held-out R06 or in-sample r.m.s. if larger).
- **B2-g** projection: σ_tot(R07) = √(1/42 + 1/683) = 0.159 [V], not evaluable. N_eff values equal the JSON.
- **Blinding:** the only data paths in `src/p3b/` are the C1 pile-up samples `p2-a-c1-pu1`, `p2-a-c1-pu2` and the
  `p3b` outputs [V: grep of path, glob and np.load lines; "sig" matches only σ variables]. I opened no signal file.
