# Experiment log — phase3_selection (append-only)

## 2026-11-24 p3-b (Casper): B2 pile-up
- 10:22 Repaired thinning implemented as [SD4] states: one Bernoulli(1/2) per interaction per subset shared by all
  candidates of the trial, plane/axis fixed (v1 step 3b), variables recomputed on kept hits, grouping (frac 0.5) on the
  thinned R04 passers. Identity check (q = 1 reproduces the stored ρ = 2 n_grp/n_pass) passed exactly.

## 2026-11-24, work package p3-c (Birgit): MET model of B4-b

**10:16 pre-declarations** (full text: `logs/executor_birgit_2026-11-24_10-16.md` §P0-P9), written before any model number.

DECISION: parameters of the MET model from CMS NOTE-2018/006 (Fig. 25 jets, Fig. 35 u_perp soft term): the parameter
  set common to options A and B of EXP §4.6; the external validation is computed under both allowed readings of "a
  different figure" (R-A: ATLAS Fig. 18; R-B: CMS Fig. 35 u_par + Fig. 34), each with its own verdict.
ALTERNATIVES: option C (ATLAS 2013 jets extrapolated mu 140 -> 200, soft term from ATLAS Fig. 18, a tt-bar RMS that
  contains the jets); option D (known to be x2-4 above both PU-200 figures).
CONFIDENCE: HIGH for the parameter source; MEDIUM for which validation reading binds (left to the review; both given).
FLAG FOR HUMAN: YES (the reading of "a different figure").

DECISION: jet-response tail NOT SOURCED after three search rounds (retrieval_log #14, #20, #32-#36). Set as an
  unsourced quantity: probability 1.5 % per jet of a low-side response 1 - |N(0, 3 sigma)|; variation 0 to (3 %, 5
  sigma). Size anchored on a Run-1 statement (arXiv:1607.03663 §8.3: 98.5 % core, 97 % variation), order of magnitude
  only; the width factor 3 (5) has no anchor.
ALTERNATIVES: Gaussian only (the tail-down variation; multijets then come from the core alone); a double-sided
  Crystal Ball (no public parameters).
CONFIDENCE: LOW (by construction: no source). Never tuned to a result.
FLAG FOR HUMAN: YES.

DECISION: tail fraction of the Fig. 34 comparison tested at three thresholds (60, 78, 90 GeV), all must pass.
  I knew before declaring it that a single Gaussian soft term passes at 78 GeV and fails at 60 and 90 GeV (hand
  arithmetic on my reading of the figure), so choosing one threshold would have chosen the verdict.
ALTERNATIVES: one threshold (78 GeV: expected pass; 60 or 90 GeV: expected fail).
CONFIDENCE: HIGH that this is the honest form. FLAG FOR HUMAN: NO.

DECISION: "lost" leptons are left out of the visible sum (STR l.1329-1333, literal); the reading "an electron that
  fails identification stays in the sum as a calorimeter deposit" is computed beside it (variation `lost_e_kept`).
ALTERNATIVES: as stated. CONFIDENCE: MEDIUM (physically an unidentified electron still deposits its energy; the
  literal reading gives more lost-lepton Z(ll) and is the larger background). FLAG FOR HUMAN: YES.

DECISION: trigger weight evaluated at the model's MET_reco (the public L1 curve is against generator-level visible
  MET; v1 evaluated its function at its smeared MET). ALTERNATIVES: evaluate at the true MET (would remove multijets
  by the trigger alone, although a mismeasured jet is also mismeasured at Level 1). CONFIDENCE: MEDIUM. FLAG: YES.

DECISION: events per Z(nunu) pilot count: primary = STR-literal (N_SM = v1's twelve processes kept + the three
  additions at the MET-model N_trig; M from v2 weights of the pilot); secondary and tertiary readings in the JSON.
ALTERNATIVES: rescale Z(nunu) (secondary) or all twelve (tertiary) by the Z(nunu) v2/v1 ratio. CONFIDENCE: MEDIUM.
FLAG FOR HUMAN: YES (fixed before any yield existed).

10:19-10:27 test runs on 300-1,000-event files (scratch, not results): generator job 11-19 ms per event; unit tests of
the model pass (limiting case R = 1, no lost lepton, S = 0 reproduces the visible sum to 4e-15 GeV: an identity by
construction of U_true, stated as such; core width 0.1301 for the table's 0.13; tail fraction beyond 3 sigma 0.0063
against 0.0061 expected). First bug: `p3c_io.load` used a pilot column name that does not exist
(`hs_sigma_gen_mb`); the pilot's column is `sigma_gen_mb`. Fixed before any pilot number was used.
Importance sampling of the tail state (proposal 0.25 per jet, exact reweighting) added for the multijets, because
K plain throws cannot populate a 1.5 % x 1.5 % double-tail configuration.

## p3-a (Aurora): final pilot classification — 2026-11-24 10:40 -0500

- Tried: importing p2w_subset.py unchanged for the BASE reading and adding categories c0-c4 in a copied road loop
  (src/p3a/p3a_subset.py). Worked: BASE rows identical to Phase 2 on a slice (7 of 7 rows, znn-00000); 4 synthetic
  tests pass (BASE = p2w_subset on 119 random events; relations; Nils's verifier accepts the witnesses; hard window).
- Did not work as planned: (1) classifying the w_v1 = 0 Z events inside the base pass would have put that campaign near
  10 CPU-h (measured 14 ms per event on znn-00000, the same as for w > 0), above my 9 CPU-h limit: moved to its own
  campaign p3-a-cls-m0, queued after the variants. (2) Nils's search at five more widths on all 64,005 row events
  projected 4.4 CPU-h: restricted to the widths at which an event is counted and to every 2nd pilot file.
- Diagnostic: 14 "bad" witnesses of Nils's search in the first slice were all k = 6-7 sets of fewer than 4 hits (his
  verifier's size check), none with k <= 3; the bad counter now counts only k <= 3 (as his review did).

DECISION: the "finder's maximum core width" of STR l.761-762 (R04 and FB(0)) is counted under two readings, w_core < 75 mm
  (W_c of frozen_inputs.json) and collection window only; neither is chosen.
ALTERNATIVES: only 75 mm (Tove, Bjorn); only "none" (Cecilie, Ingvild: the Phase-2 R04 column).
CONFIDENCE: MEDIUM (the text names a "maximum core width" that no Phase-2 document transcribes)
FLAG FOR HUMAN: YES (PREREG_v2 must state it; it sets H of the T2 candidate FB(k_adm = 0))

DECISION: every Z(nunu) event is classified, also the 1,297,459 with w_v1 = 0 (separate campaign), because ADD l.607
  replaces M by the day-12 MET model and a v2 weight may be non-zero where w_v1 = 0.
ALTERNATIVES: w > 0 only (Phase 2), which would need a new campaign after p3-c delivers.
CONFIDENCE: MEDIUM (cost 4 CPU-h for an input the orchestrator's brief does not list)
FLAG FOR HUMAN: NO
- 13:28 Repaired thinning on the development sample (1,000 ρ = 2 events, K = 64) OVER-predicts the development direct
  counts: r = 1.30 / 1.38 / 2.17 at R04 / R05 / R06 (σ_tot ≈ 0.02); development s_model 0.506 > cap 0.135.
  Union (no grouping) ×1.42 at R04. The repair moves v1's R04–R05 under-prediction to an over-prediction and makes the
  R06 over-prediction larger (v1: ×1.58). Remediation attempts: see the session log (q = 1 identity; refit + dedup
  emulation fails its q = 1 sanity check; re-ranking has no effect; hit-level refind control running).
  DECISION: s_model of thinning reported both over the evaluable cumulative rungs (0.506, primary as the r.m.s. "on the
  development samples" of the B2-a rungs R04–R07) and with the crossing rungs (0.536).
  ALTERNATIVES: crossing rungs only / R04–R05 only — every reading is far above 0.135, the cap status does not depend on it.
  CONFIDENCE: HIGH (the choice changes no verdict). FLAG FOR HUMAN: NO.
- 13:45 Random planes on REAL ρ = 1 hits (16,000 trials × 1,000 planes): R04 14,630, R05 3,563, R06 31 passes;
  R05/R04 = 0.244 (finder groups: 0.289), R06/R05 = 0.0087 ± 18 % (finder groups: 0.0050). Information for the
  occupancy model, whose inputs are R04 and R05 only.
- 13:55 Occupancy model (B2-b), frozen definition (session log 10:56): held-out development R06 ln r = +0.355 ± 0.034
  (in-sample R04 +0.006, R05 -0.166) -> s_model 0.355 > cap. Remediation O1-O4 (trend of C, normalisation variants,
  real-hit random-plane fall, random planes vs finder groups): none brings R06 inside the cap; cause: the number of
  finder-distinct groups per passing configuration changes with the width cut (+0.17 R04->R05, ≈ -0.55 R05->R06).
- 14:17 Refind control: hit-level thinned + re-found ρ = 2 events reproduce the direct counts (-0.03 / -0.07 / +0.05);
  the repaired thinning exceeds them on the same trials (+0.31 / +0.40 / +0.74): estimator definition, not sample/code.
  DECISION: no redesign adopted (Phase 3 does not redesign; any redesign would be chosen after seeing R06); both
  estimators reported as above the cap; decision point 2 decides (STR §11.7 rules 1-2).
  ALTERNATIVES: full ρ = 1 re-find of each thinned subset (≈ 1,200 CPU-h at K = 64 for 3,000 events); a measured
  configuration-to-group map for the occupancy model (R06 no longer held out); a larger declared s_model (cap still binds).
  CONFIDENCE: HIGH on the measurement, MEDIUM on the cause attribution for the occupancy model. FLAG FOR HUMAN: YES.

## 2026-11-24 14:55 p3-e (Hilde): campaign p3-e-devpu1 (dev.pu1, STR §4.17 row 12) defined and tested
- 298 jobs × 20 events = 5,960 events, the c1.pu1 command with stream dev.pu1. Per-job caches in the job scratch.
  Memory limit 1,054 MB. Test job devpu1-0000 on maxwell: done; CPU, RSS and schema as c1.pu1; p3-b readers load it.
  Kept as part of the campaign. Seeds disjoint from c1.pu1, c1.pu2, prod.pu1, prod.pu2 and reserve.pu1. Not launched.
- DECISION: 20 events/job (as c1.pu1) rather than fewer. ALTERNATIVES: 15/job (397 jobs) for more timeout margin.
  CONFIDENCE: high (worst-job ESTIMATE ≈ 1,540 s wall at 4/node vs 1,800 s cap). FLAG FOR HUMAN: no.
- DECISION: per-job Pythia MPI init (as Casper's prod campaigns), +≈ 70 CPU-s/job (≈ 5.8 CPU-h). ALTERNATIVES: per-node
  shared init file as c1.pu1. CONFIDENCE: medium. FLAG FOR HUMAN: no (orchestrator's call; see P3E §6).
- Open: interaction-level Pythia seeds (mod 9×10⁸) repeat at ≈ 0.5 % between dev.pu1 and prod.pu1 (ESTIMATE; P3E §6).

## p3-d (Gorm, T1 likelihood Phase-3 part) — 2026-11-24
- 14:32 Plan in `logs/executor_gorm_2026-11-24_14-32.md` (readings R1-R9 of the frozen text declared before any run).
- 14:50 pyhf 0.7.6 ToyCalculator generates at the conditional MLE (source, calculators.py l.93-116); on the one-bin
  m = 0 workspace lambda_hat sits at the lower bound and no background-only toy fluctuates (smoke: 0/200, expected
  limit 3.08 ~ the B = 0 value 2.996 against the convention's 10.8 at kappa = 10). STR l.1601 [U] confirmed in smoke.
- 14:51 Exact one-bin sums re-derived (p3d_exact.py): STR l.1680-1686 reproduced to every printed digit.
- 14:52 v1-count workspace (v1 factor chains at FB2&h>5&o>5, v2 treatment): pyhf fits fail in 20-40 % of toys at
  mu ~ mu95 (deficit region; counts 3e5-1e9, pile-up log widths up to 5.2). Remediation attempts in the session log.
  DECISION: the term's independent binomial widths are combined into one nuisance per term (R1).
  ALTERNATIVES: one nuisance per factor (about 11 more parameters).
  CONFIDENCE: MEDIUM (exact for the uncensored log-normal; censoring then bounds the product). FLAG FOR HUMAN: NO.

## 2026-11-24 14:56 -0500 p3-b review cycle 1 (fixer Ivar): judgement calls of 24 Nov not logged by the executor (DOR B9)
Appended by the fixer from the executor's session log and P3B v1; the times are the executor's (session log), the
decisions are his unless marked. Nothing above is changed.
- 10:56 (executor) **Occupancy-model definition frozen before any comparison with a direct count** (session log
  l.111-118).
  DECISION: ensemble NZ_MIN 0.2, φ_a ∈ φ_MET ± 0.15, η_a ∈ U(−1, 1), ψ ∈ U(0, π); densities φ-averaged, 2 mm z bins;
  toys conditional on R04; IS (β = 0.5) primary at R05–R08, plain MC as the check; C held at R05 (trend = variant);
  N_cfg by GLS at R04–R05; s_model = max(|ln r(R06)|, in-sample r.m.s.); day-15 = one scale A on R04–R07, weights
  1/(σ_stat² + s_model²); fit-probability fractions from development R06 finder groups (Df-2).
  ALTERNATIVES: C trend as primary; diagonal / R04-only / R05-only N_cfg; plain MC as primary.
  CONFIDENCE: HIGH that it preceded the comparison (model code sha256 in the occmod outputs = files of 10:37; DOR §4).
  FLAG FOR HUMAN: NO.
- 10:56 (executor) **Day-15 reading of STR l.2741 "the development model's R04–R07 inputs".**
  DECISION (executor): reading (i), one scale A fitted on the development direct counts at R04–R07 (uses the held-out
  R06 and the 7 R07 counts). ALTERNATIVES: reading (ii), the B2-b model with its R04–R05 normalisation (STR
  l.1145-1146) evaluated at R07–R09 (DOR B4). Both are now tabled in P3B v2 §6: R08 347 / 443, R09 4.1 / 5.25 events.
  CONFIDENCE: LOW that the frozen text selects (i). FLAG FOR HUMAN: YES (orchestrator; not chosen by the fixer). Both
  are the rule-1 projection input only, "no credit" (advisor B2CAP point 8 (ii)).
- 13:30 (executor) **s_model rung set for thinning** (frozen text silent).
  DECISION: report cumulative evaluable R04–R06 (0.506) and with crossing rungs (0.536); DOR adds R04–R05 0.291, R04
  0.259, smallest single rung 0.234. ALTERNATIVES: as listed. CONFIDENCE: HIGH that the cap status does not depend on
  the reading (every reading > 0.135). FLAG FOR HUMAN: NO (reported under every reading).
- ≈ 13:40–14:15 (executor) **Thinning variants R2 (refit + dedup, modes 1/2) and R3 (re-rank, mode 3).**
  RESULT: R2 failed its own q = 1 sanity check (2,361 / 2,644 groups vs stored 2,731 / 3,061): not a valid emulation,
  neither supports nor excludes the refit as mechanism. R3: ≤ 1 % change. Neither adopted. FLAG FOR HUMAN: NO.
- **[DT2] (STR l.1198-1200), logged as a [D].**
  DECISION [D]: repaired thinning has no evaluable rung beyond R06 on the development sample (R07: 7 direct counts,
  σ_tot 0.38; B2-g projection to 3,000 events: σ_tot(R07) 0.159 at the development direct rate) → its validated range
  is declared **R04–R06** in PREREG_v2; R07 rests on the occupancy model and the direct count. With s_model above the
  cap the range matters only if the re-find redesign is ordered at the day-15 pause.
  ALTERNATIVES: R04–R07 if the 96,000-trial direct rate is at v1's 7.3×10⁻⁴ (σ_tot 0.126); not chosen, the
  development evidence says R06. CONFIDENCE: HIGH. FLAG FOR HUMAN: YES — "user informed" duty of [DT2]; the
  orchestrator's RESULT notice of 24 Nov (advisor Addendum 1 A5) carries it ("validated range is R04–R06 at most").
- 14:20 (executor) **Enlarged development sample `dev.pu1` called "not requested" (P3B v1 §7).** CORRECTED: it is a
  frozen MUST line (STR l.2105, ≈ 5,960 events, 100 CPU-h, role "decision point 2, s_model, crossing rungs"); not
  producing it would be a deviation (DOR B8). Advisor Addendum 1 A4: produce it now (orchestrator launch, p3-e);
  sealed per A2. FLAG FOR HUMAN: NO (ordered).
- **Times (DOR B9).** P3B v1 header end time "14:30" was not read from the clock (file mtime 14:20:23, commit f881aa3
  14:21:04 -0500); session-log "13:30" N_eff line does not match the final data (4 passing R08 subsets, not 1).
  Correction note appended to the executor's session log; P3B v2 header corrected.
- 15:05 v1-count workspace (51 parameters): three remediations of the fit failures (method ladder with L-BFGS-B;
  free-first + mu continuation; KKT active set with projection) leave 14-19 of 80 toys dropped at 5,500 s per
  1000 + 1000 unit; the b-only median q~ is on the jump (3.3e5 at mu = 800, 4.7e4 at mu = 300). T1-c (iii)-(v) and
  (iv) on this workspace: infeasible as specified (~430 CPU-h and unresolved). Branch stopped; decision requested
  in the artifact. Table in the session log 15:05.
  DECISION: continue only the independent items (T1-c (i), (ii), pyhf demonstration, recipe, builder).
  ALTERNATIVES: redesign the v1-count conversion (e.g. the v2 pile-up treatment applied to v1's pile-up term, or a
  different v1 selection) — a choice for the orchestrator/advisor, not made here.
  CONFIDENCE: HIGH that the present workspace is not fit-able within budget. FLAG FOR HUMAN: YES.

## p3-f (investigator Jorunn), 24 Nov 2026 — B2 occupancy cause investigation (Task A) and re-find yield (Task B)
- 15:00 **Method hashed before any job** (`outputs/p3f/CAUSE_METHOD_jorunn.md`, sha256 99dfcafb…0d83 in the session
  log). Mechanism measurement M_G = Horvitz-Thompson count of distinct finder-like groups (refit map: the finder's refit
  started from each configuration of the frozen p3-b ensemble; group identity >= 1/2 shared hits; basin volume by local
  sampling) on the c1.pu1 hits; prediction ln r̂ = ln r(R04) + ln[B_model(r)/B_model(R04)] − ln[Ĝ(r)/Ĝ(R04)]; "cause
  found" iff at R05 and R06 sign agrees, |ln r̂ − ln r_obs| <= 2 σ_comb and |ln r̂| >= 2 σ_G. Measurement (i) (10x
  random planes, C(R06)) in the same campaign.
  DECISION: refit map as the verdict measurement (the finder counts groups of refitted candidates); fixed-ribbon HT
  count and the per-configuration refit transfer as diagnostics only. ALTERNATIVES: fixed-map HT as the verdict (the
  model's own object; would test basin volumes without the refit); per-configuration refit transfer only (cheaper, no
  distinct counting). CONFIDENCE: MEDIUM that the emulation is close enough to the finder to be decisive either way
  (D4 checks its absolute faithfulness at R04). FLAG FOR HUMAN: NO.
- 15:08 (code check, before the campaign) **Local sampler defect fixed:** uniform box + doubling gave V = 0 for some
  configurations; replaced by an unbiased nested-box mixture in hit-geometry-aligned coordinates (session log 15:05-15:12).
  Same estimand; only R04 volumes looked at. FLAG FOR HUMAN: NO.

## 2026-11-24 15:15 -0500 p3-b review cycle 1 (fixer Ivar): what each finding was, what changed, result
Artifact v2: `outputs/P3B_PILEUP_v2_ivar_2026-11-24.md` (v1 unchanged). Session log `logs/fixer_ivar_2026-11-24_14-48.md`.
- A1 (closure failure, both estimators): stated plainly with the rule-2 status of the advisor ruling; resolution is
  the orchestrator's rule-2 process (thinning: re-find variant at the pause; occupancy: cause investigation to 30 Nov).
- B1/B6/B7: rule wording replaced by the binding wording (rule 1 not met now; thinning "redesign identified"; occupancy
  "no cause demonstrated"); R0/R1/R2/R3 and O1-O4 relabelled; self-check corrected (no occupancy remediation, and why).
- B2/B4/B5: `pileup_term.py` extended (no v1 key changed): no-credit 485 (dev bound 2,910 flagged), reading (ii) R09
  5.25, planning widths with R06 as last test rung (R08 0.822, R09 0.917). FAIL vs not-submitted readings stated.
- B3: `src/p3b/is_check.py` (new, diagnostic). IS statistical error at R08 8.7 % (DOR's 12 % not reproduced);
  heavy-tailed weights (top 1 % of configurations = 51 % of the sum). Paired plain check, 6.4e8 toys on the 6,400
  stored configurations (3 jobs, 0.886 CPU-h, maxwell): 45 R08 passes, plain/IS = 1.13 ± 0.15; R07 1.080 ± 0.012.
  DECISION: quote the MC error at R08 as ≈ 15 % (R09 ≈ 21 %) [E]; keep IS as the primary estimator (frozen 10:56).
  ALTERNATIVES: replace IS by the plain value (rejected: would change a frozen choice after seeing the check; the two
  agree within 0.9σ). CONFIDENCE: HIGH that the v1 factor-12.6 alarm is excluded; MEDIUM on the 15 % figure (a ±5 %
  check would need ≈ 8 CPU-h). FLAG FOR HUMAN: NO.
- B8/B9: dev.pu1 restated as a frozen MUST sample being produced; DECISION blocks, [DT2] [D] and the time corrections
  appended (entry above; correction note in the executor's session log).
- Figures: plots.py fixed for every ELI A item (x labels, legends, R07 in frame with open = not evaluable, error bars
  on both occupancy readings, no-credit segment); regenerated on maxwell (1 job). Lint: 0 violations (20 files).
- Linter glob (`*/src/*.py` misses `src/p3b/`): NOT edited — `conventions` -> `tools/jfc/src/conventions/` is
  read-only. FLAG FOR HUMAN: orchestrator to decide (study copy or tools/jfc change).
- 15:27 **V1 recapture validation of the basin-volume estimator FAILED** (0.82 / 1.43, per-trial 0.33-6.9, heavy
  tails); V2: distinct R04 hit-set classes of ribbons on ρ = 1 hits do not saturate at 10⁶ configurations (≥ 160-170 per
  trial and rising), above the finder's 171 groups: the finder does not enumerate distinct sets either.
  DECISION: amendment A1 (hashed 2026-11-24 15:30:28 -0500, sha256 7f0e545a…): verdict measurement replaced by the per-configuration refit
  transfer M_T (former diagnostic D2); criterion unchanged; decided on R04-only validation, before any campaign.
  ALTERNATIVES: (a) improve the volume estimator (more local draws, other proposal) — rejected: even exact volumes count
  an object the finder does not count (V2); (b) a seed-measure emulation (sample the finder's hit-pair seeds and refit)
  — rejected as the verdict: it recomputes the finder's candidate count (a near-restatement of the direct count, the
  objection DOR (1b) made to O4); (c) stop with NOT FOUND now — rejected: M_T is cheap and pre-statable.
  CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES — a pre-stated verdict measurement was replaced after a validation failure
  (before any R05/R06 number); the reviewer should check A1 against the original hash.

## 2026-11-24 15:31 -0500 p3-b review cycle 2 (fixer Ivar): Liv B-new-1 and C items (artifact v3; no jobs, no new Monte Carlo)
- B-new-1: the cycle-1 entry above ("quote the MC error at R08 as ≈ 15 % (R09 ≈ 21 %)") is **corrected** (not
  rewritten): the 8.7 % of the stored 200-toy runs is a lower bound; the fresh 2,000-toy IS run has a ×6.3 larger
  per-toy variance → stored R08 error ≈ 22 % [E] (R07 5.7 %), R09 ≈ 26 % with the fit-probability fraction (0.145).
  Configuration sampling 0–1.6 % [E, Liv]. Plain above IS with the same sign at R06/R07/R08 (+4.6/+8.0/+13.5 %):
  stated as a possible IS bias. Reading (ii) at the plain value 503 events > no-credit 485 (reading (i) 394).
  Derived with `src/p3b/is_check_c2.py` (standard library; einstein; reproduces liv_ischeck.json exactly).
  DECISION: quote ≈ 22 % / ≈ 26 % and the asymmetric plain interval (+28 % / −1 %); keep IS primary (frozen 10:56).
  ALTERNATIVES: quote the plain value as central (rejected: frozen choice; the bias is possible, not shown at > 2σ).
  CONFIDENCE: MEDIUM (22 % is itself a lower bound if the weight tail is under-sampled at 2,000 toys). FLAG FOR HUMAN:
  NO (orchestrator: note 503 > 485 for the day-15 reading).
- JSON: one new key `occupancy_day15.mc_rel_error_c2` (0.217 / 0.261) on the R08/R09 records; `mc_rel_error_b3`
  kept, documented as superseded (SCHEMA.md). Key diff: 4 added, 0 changed, 0 removed.
- C-1 (rule-2 quote completed, Q3 granted at Gate A), C-2 (reading (iii) listed, not chosen), C-3 (dev.pu1 seed
  qualifier), C-4 (B3 inputs copied to outputs/p3b/is_check_inputs/, sha256 identical), C-5 (mixed route stated and
  flagged), C-7 (toy ESS 11–43 per seed, 195 total) applied. C-6 (figure style) NOT applied: needs a plot job.

## 2026-11-24 15:43 -0500 p3-b review cycle 3 (fixer Ivar): Oddvar B-new-2 and text/JSON C items (artifact v4; no jobs)
- B-new-2: v3's "the frozen script censors the term at 485" / "every R08+ candidate carries ≥ 485 events" was wrong
  (and is corrected here, append-only, for the cycle-2 entry above): the frozen projection takes min(term,
  (N_trig/96,000)·Exp(1)) in every pseudo-experiment (mean 426, 68 % value 485; strategy_budget.py l.585-587, l.678;
  STR l.953-954, l.1586-1588) [V: read]. Oddvar's toy [E]: censoring binds in 56.5–67.0 % of pseudo-experiments for
  R08 medians 347–503; mean contribution 241–286 events vs 425.5 without credit.
- C-1: truth/stored = 1.13 ± 0.17 (not ± 0.15), interval [0.97, 1.30]. C-2: 22 % is a firm lower bound (fresh IS also
  misses the tail). C-3: R07 pull 1.4σ with the 5.7 % error (1.9σ with 4.1 %), R06 2.4σ / 1.5σ, flagged as computed
  with lower-bound errors. C-4: `mc_rel_error_c2` added to the reading (ii) records (key diff 4 added, 0 changed);
  2S transfer tagged [E]; no MC term in the frozen s_tot stated. C-5: pileup_term.py not rerun, stated. C-6: §11 numbering.
- No number, flag or route changed beyond these. FLAG FOR HUMAN: NO.
- 16:01 Reading R1' declared before any R1' toy (advisor Tuva 15:57; outputs/p3d/R1prime_DECLARATION.md,
  sha256 1f7593e8…, committed 846d7e8 as DEVIATIONS V17).
- 16:30 Feasibility probes (A) R1' and (B) rescaled parametrisation on R1 and R1': all three fail the declared
  criterion (three-start agreement on 20 toys; R1 rescaled also > 2 % dropped); unit cost 3,700-5,100 s, projection
  ~300 CPU-h for T1-c (iii)+(v) against the 45 CPU-h cap. Stop rule: (iii)-(v) not launched; DECISION to the user.
  DECISION: none taken by me (stop and report).
  ALTERNATIVES (for the user/advisor): Phase-4a-only test on the v2 workspace (COM amendment); a smaller test design.
  CONFIDENCE: HIGH on the measurement. FLAG FOR HUMAN: YES.
- 16:10 Builder fix (advisor point 8): credited pile-up = static fit bound 485 + drawn bound in generation (95 %
  variant 1,275 recorded); no-credit pile-up = counted 0 of 96,000; checked (p3-d-ph2).

### p3-a (Aurora), continued — 2026-11-24 16:44 -0500

- Did not work: one campaign per variant (NFS: 1.8 MB/s per reader). Worked: all variants from one read per file
  (p3a_multi.py); 231 jobs, 9.9 CPU-h, 5 h of wall.
- Did not work: witness verification with a plane normal re-fitted without weights (43 of 62 "failures" on a smoke
  test, all plane membership), then with the verifier's weights (17 of 432). Worked: the classifier's own plane
  normal recovered by repeating its seed loop (17 of 17 accepted).
- Not attempted: classification of the w_v1 = 0 events on v1's road axis (9.4 CPU-h for an input the binding run would
  not use); an independent search for s = 3 rows with k_IP >= 4.

DECISION: the open readings are separate columns (BASE as produced, OWN, PLANS4, HARD, UNION); BASE is never altered.
ALTERNATIVES: replace the Phase-2 number by the union (largest lower bound, 1,526); adopt the own-axis count.
CONFIDENCE: HIGH (the 23 Nov ruling says "quoted as produced" and "not fixed now")
FLAG FOR HUMAN: NO

DECISION: in the NOT BINDING dry run the R07 pile-up term is read as a counted term, N_trig/48,000 x Gamma(36) (STR l.1013
  "35 in 48,000 trials"); R11 and R14-type rows use the ends of PU_R11 with W_PU of strategy_budget.py; FB(k < 4) has
  no pile-up term (lower bound).
ALTERNATIVES: a lognormal row for R07 with an invented width; the R07 or R08 rows as upper proxies for FB(k).
CONFIDENCE: MEDIUM (no approved row exists for these candidates; the Z term is 85-100 % of every reading)
FLAG FOR HUMAN: YES (the binding run needs p3-b's rows for every T2 candidate, FB(k) included)

DECISION: the DIF-C row (parent-only witness) is reported as m = 1 (own-hit count) and m = 0 (attributed to the term's
  class); not chosen.
ALTERNATIVES: either alone.
CONFIDENCE: MEDIUM (STR l.2731 and l.752 read differently for a witness made of the parent's hits)
FLAG FOR HUMAN: YES (PREREG_v2: does a looping parent count for a B1 term)

DECISION: stop-and-report, not repaired: the binding run needs the v2 MET model's per-event weight and MET azimuth for
  the classification itself (ADD l.360-361, l.607); interface built (variant v2), campaign defined, not launched.
ALTERNATIVES: declare the rule-1 count to be read on v1's preselection and axis (an orchestrator / advisor matter).
CONFIDENCE: HIGH that the dependence exists; the choice is not mine
FLAG FOR HUMAN: YES

### p3-a fix round 1 (Ulf, fixer) — 2026-11-24 16:57 -0500

- Text-only v2 of the p3-a artifact (`outputs/P3A_PILOT_FINAL_v2_ulf_2026-11-24.md`) answering Sindre's review
  (A-1, B-1…B-4, C-1…C-8). No job, no count recomputed; v1, code, JSON unchanged.

DECISION (recorded by the fixer for Aurora's plan reversal, review C-6): the 1,297,459 Z(νν) events with w_v1 = 0 were
  NOT classified, although the plan (executor_aurora_2026-11-24_10-16.md, fact 5) said every Z(νν) event would be
  (decided 11:08 by Aurora). Reason: classification on v1's road axis is not the input a v2 MET-model weight needs
  (the axis moves too; §8 item 1); not cost (11.3 + 9.4 = 20.7 CPU-h was inside the 26 CPU-h stop limit).
ALTERNATIVES: classify them on v1's axis (9.4 CPU-h [ESTIMATE]) as the plan said.
CONFIDENCE: HIGH that the reason is sound (Sindre C-6 agrees); the binding route is the orchestrator's item 9.
FLAG FOR HUMAN: NO (part of the item-9 ruling)

DECISION (fixer): §4.1 pointer on reading S3 lowered from "w_core, MEDIUM-HIGH" to "no clear pointer"; the DIF-C row's
  attribution stated as open in §0 (both readings, m = 0 / 1, with ADD l.603-605, l.257-258 and STR l.748-749 quoted);
  coverage labels on every s = 3 row in §0, §3.1, §6, §7.
ALTERNATIVES: keep v1's pointers (rejected: review B-1, B-2 show the frozen text does not support them alone).
CONFIDENCE: HIGH (text corrections; no count moves)
FLAG FOR HUMAN: NO (S3 and the DIF-C attribution stay FLAG FOR HUMAN in the artifact)
