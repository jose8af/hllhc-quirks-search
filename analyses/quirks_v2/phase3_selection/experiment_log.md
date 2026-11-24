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
