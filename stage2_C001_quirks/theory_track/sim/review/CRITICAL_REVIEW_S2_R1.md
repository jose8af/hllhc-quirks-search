# Critical review, Stage 2 (MG5_aMC 2.9.22 + Pythia 8.313 quirk samples), round 1

Reviewer: critical reviewer (single reviewer, JFC `agents/critical_reviewer.md`, classes per `methodology/03-review.md`).
Date: 2026-10-11.

Material reviewed (all in `theory_track/sim/`):
- documents: `plan.md`, `VALIDATION.md`, `SAMPLES.md`, `README.md`, `E4_session_log.md`;
- results: `results/*.json`, `results/summary_tables.md`;
- `figures/` (6 of the 33 PNGs opened), `scripts/`, `cards/`, `models/quirkE`, `models/fr`, `logs/`, `probes/`;
- data: `../data/sim/{npz,aux,SAMPLES_INDEX.json}`;
- context: `outputs/THEORY_GAPS_SYNTHESIS.md` S-13, `code/T2_kinematics.py`, `code/T3_causal.py`,
  `research/theory_signal_model.md` §1.1, §2, §5 and App. A, `research/cache/pdf/1903.12179.txt`;
- the MG install at `/Users/jochoafl/8A/MadGraph/MG5_aMC_v2_9_22` (read only).

Scratch scripts and their outputs are in `review/r1_checks/` (`c1`…`c7`, each with a `.out` file). Nothing outside
`sim/review/` was written.

---

## 1. Independent spot-checks (what I recomputed, and the result)

| # | Quantity | VALIDATION / SAMPLES | Recomputed (script) | Status |
|---|---|---|---|---|
| R1 | σ_matched E-INC 500 = Σw | 2.507 fb | 2.5070 fb. Acceptance from Σw/σ_LHE is 0.4652; from the count of w≠0 it is 0.4650. Per-event weights equal to 0.15 %; both chunks have σ_LHE 5.397 / 5.381 fb (c2 A) | OK |
| R2 | σ E-TRG 500, E-LOPS 500, S-INC 500, E-INC/TRG 1500 | 0.5141 / 2.454 / 0.1886 / 0.005199 / 0.001468 | 0.51413 / 2.4536 / 0.18864 / 0.0051986 / 0.0014678 (c2 A) | OK |
| R3 | Quirk masses in the npz (E/Ẽ, 200-1500) | `set MXE/MSXE m` | m exactly, for every event of 10 files checked (c2 A, ad hoc) | OK |
| R4 | TRG generation cut enforced | pT(QQ̄)_ME ≥ 100 | E/Ẽ benchmarks: 0 TRG events below 100 GeV, except 1 event at 99.97 GeV (E500; Pythia status-23 rounding) (c2 B) | OK |
| R5 | ME-cut closure, E500 | TRG/INC 0.927 ± 0.015; generation-cut closure 0.998; INC tail with pT_ME < 100: 7.1 ± 0.4 % | 0.927 ± 0.015; 0.998; 7.07 ± 0.38 %. All six (spin, m) points reproduce §4.4 to the last digit (c2 B) | OK |
| R6 | TRGS: share of the tail σ that comes from INC | "0.4-2 % of the stitched tail events" (§4.4) | Events: 0.6-1.7 %. **σ: 3.9-7.1 %**, because ⟨w_INC⟩/⟨w_TRG⟩ = 3.7-6.6 (c2 B) | OK (see A1) |
| R7 | TRGS vs INC shape, pT(QQ̄) 200-1000 GeV and 2(γ*−1) | "agrees within stat" | χ²/ndf = 7.4-20.8/16 for pT and 9.4-20.6/15 for x. Raw TRG/INC fails in x at E500/E1000 (p < 0.001) (c5) | OK (C-6) |
| R8 | Median ℓ_max bias, E500 / E200 / Ẽ200 | (i) −9.8 / −25.6 / −21.8 %; (ii) +0.5 / −4.6 / −4.0 %; (iii) +1.1 / −1.2 / −4.8 % | Identical to 0.1 %, with my own weighted median and my own selection code (c2 D) | OK |
| R9 | CP5 actually applied | all nominal jobs | The "changed settings" table of every PY8 job (312 production + 6 pilot logs): all nominal samples show pSet 20, α_s 0.118 NLO (ISR/FSR/MPI/ME), pT0Ref 1.41, ecmPow 0.03, bProfile 2, coreRadius 0.76, coreFraction 0.63, CR range 5.18. Only V-TUNE-{INC,TRG} are at Monash defaults; V-MPI has MPI off. One settings signature per sample; seeds unique (c1) | OK |
| R10 | CP5 values vs arXiv:1903.12179 | Table 3 CP5 column | `research/cache/pdf/1903.12179.txt` l.897-918 prints 1.41 / 0.03 / 0.76 / 0.63 / 5.18, EcmRef 7000, rapidityOrder on, 0.118/NLO ×4. The transcription is exact (C-3 for CMSSW precision) | OK |
| R11 | §4.2 merging variations; §5 tune and MPI | σ, f(pT>200), f(pT>300) table | All reproduce to 4 digits, e.g. V-MERGE-50: 2.4809 / 0.0986 / 0.0474; Monash σ −10.8 % (c7) | OK |
| R12 | Yields table §1.2 (500, 1000 GeV) | 6.11 fb × 0.104 → 1.91e3; 0.1967 × 0.146 → 86 | `xsec.json` 1909.5 and 86.1; t16 banner has aEWM1 = 127.9, Gf = 1.208403e-5 (s_W² = 0.22225, checked analytically) | OK |
| R13 | QED FSR off the quirks | "none occurred" | M_hard − M_shower: median 0, |ΔM|/M < 6e-4, fraction with ΔM > 0.1 GeV ≤ 1.5e-4 (c6) | OK |
| R14 | md5 in SAMPLES.md | cca86057, 16be7e42, 54a41bda | identical | OK |
| R15 | Event order in the npz (MG LHE order) | implicit in "take the first N" | Random within TRG/INC/LOPS files: block multiplicity fractions are flat; Spearman ρ(index, x) ≈ 0 (c4) | OK. TRGS is the exception, see A1 |

Model (item 1 of the brief).
- E = (1,1)₋₁ Dirac fermion and Ẽ = (1,1)₋₁ complex scalar, both with hypercharge-only couplings
  (`couplings.py` GC_XEA = i e Q and GC_XEZ = −i e Q s_W/c_W, plus the seagulls 2ie²Q²(1, r, r²)).
- The QNUMBERS blocks in the banners give 3Q = −3, 2s+1 = 2 / 1 and colour singlet.
- p1 = pid < 0 is therefore the +1 quirk. This is consistent with `run_causal`'s default charges = (+1, −1).
- This matches BRIEF.md l.11. The review brief calls E "doublet-like"; that is not what BRIEF or the model say (C-1).

Cross sections (item 1).
- N_IC: the samples are N_IC = 1; σ_norm carries ×2. This is correct.
- LO matches App. A × (127.9/132.507)² to −0.6…+0.2 %.
- The scale band at μ = √ŝ is 9-point. At LO DY μ_R does not enter, so this equals TH's ×½/×2, as it should.
- The CT18 Hessian is handled correctly: 29 pairs, asymmetric, 90 % → 68 % by ÷1.645.

---

## 2. Findings

### Category A (must fix before PASS)

**A1. The recommended trigger sample TRGS cannot be used through the documented "first N events" interface. Its INC piece sits at the end of the file and carries 4-6× larger weights.**

Evidence.
- `scripts/stitch_trg.py:35` writes `np.concatenate([v, ci[k][comp]])`: all TRG rows first, then the INC complement.
- The documented Stage-3 access path is the following:
  - `plan.md:275` "`iter_events(...)` yields the selected events in file order, so Stage 3 can take the first N at every Λ";
  - `scripts/mg_events.py:65-66`, docstring "unweighted MG events: weights are equal up to MLM/systematics factors";
  - the alias `trig` → TRGS (`stitch_trg.py:47`, VALIDATION §4.4).
- c2 C: in the tail selection (pT > 200, |η| < 2.5) the first INC-origin event appears only at positions
  14376 / 16316 / 16927 (E 200 / 500 / 1000) and 7495 / 8423 / 8586 (Ẽ). These events carry 3.9-7.3 % of the tail σ
  with ⟨w_INC⟩/⟨w_TRG⟩ = 3.7-6.6.
- So any Stage-3 run that takes the first N ≤ 7.5k-17k events, as plan §4 intends ("≥ 200 events per point"), gets
  exactly the raw ME-cut sample. VALIDATION §4.4 found that sample fails closure: TRG/INC = 0.927 ± 0.015, and the
  x-shape fails with χ² = 41/15 at E500 (c5).
- Even when the INC events are included, an unweighted use under-weights them by a factor 4-6.
- c3 measures the first-N (unweighted) vs weighted TRGS medians: up to +7.4 % in 2(γ*−1) and +2.5 % in leading-jet
  pT at N = 2000, and ±1-2.5 % at N = 10000. Part of this is statistical; the systematic part (TRG vs TRGS) is
  −0.9…−1.4 % in N_osc and is unknown for jet/MET-based efficiencies.
- The deliverable is therefore internally inconsistent: the fix announced in §4.4 is not effective through the
  interface that the plan hands to Stage 3.

Required fix (cheap).
1. In `stitch_trg.py`, write the TRGS rows in a deterministic random order (fixed seed; store the permutation), so
   that any prefix is a fair sample.
2. Make the weights mandatory and say so: correct the `iter_events` docstring ("TRGS events are NOT equal-weight;
   use info['w']"). Optionally provide `iter_events(..., unweight=True)`, which accept-rejects with w/w_max and a
   fixed seed for users who need equal-weight events.
3. Add a regression check to `val_loader.py`: in the first N = 2000 selected events, the share of w from origin = 1
   matches the full-file share within statistics.
4. Update VALIDATION §4.4, §6 and SAMPLES.md accordingly. The plan text "take the first N" must name the weighting
   requirement.

**A2. Headline numbers in §0 and §3 do not match the tables and `results/lmax_bias.json`.**

Evidence.
- VALIDATION §0 item 3 (l.41) and §3 conclusion (b) (l.241) say the fixed-pT trick "biases N_osc by +1…+15 %".
- `lmax_bias.json` `bias_vs_iv.*.nosc_median_bias` gives:
  - old-cache (i): +7.4, +6.0, +0.6, +13.2, +2.5, **−1.2** %;
  - MG-LO (i): +7.4, +5.8, +2.6, +14.8, +2.3, **−2.7** %.
- So the bias changes sign at Ẽ 1000 GeV (−2.7 ± 1.0 %, 2.7σ). The VALIDATION table itself (l.221) shows −1.2 %.
- Similarly, §0 item 4 (l.46) says "≤ 7 % in d01". The §4.1 table has 8.5 % (Ẽ-INC 500) and 8.2/9.5 % (V-MERGE).
  §0 does not say that it covers only E-INC.

Required fix. Correct the ranges to "−3…+15 %, no sign-definite bias at 1 TeV". Re-derive every §0 number from the
JSON with one script (e.g. extend `val_summary.py` to emit the §0 bullets), so that §0 cannot go stale.

### Category B (advisory, should be fixed; do not block)

**B1. The EW-scheme nuisance is mis-cited and its logic is not right for this normalisation.**
- VALIDATION §1.3 l.131-132 and plan D8 say the scheme spread "justifies TH §2.4's ±7 %". TH actually recommends
  **±5 %**: §2.4 "Recommendation: a ±5% 'EW scheme' nuisance", and §5 table "±5% (ESTIMATE …)". The 7 % is the
  α² ratio, not the nuisance.
- More importantly, σ_norm = K_WG × LO(α(M_Z)), where K_WG = σ_WG/LO(α(M_Z)). The α choice therefore cancels in the
  product: σ_norm inherits the WG scheme.
- Also, the WG reference is the right-selectron, which is the same (1,1)₋₁ hypercharge-only state. So the s_W²
  dependence of variant (a) cancels as well.
- The Gμ-vs-α(M_Z) LO ratio (+6.9…+9.8 %) is therefore not the uncertainty of σ_norm.
- Fix: quote TH's ±5 % (K transfer + scheme) as the nuisance. Present t15 as a check of the α rescaling only. Note
  that the residual scheme uncertainty is that of the WG Resummino tables (NLO EW, UNVERIFIED).

**B2. The MG install footprint is under-reported.**
- `find $MG -newermt 2026-10-10` lists **13 new `.pyc` files (11 more than the 2 reported) and new or changed
  `__pycache__` directories**:
  - `madgraph/__pycache__/__init__`;
  - `madgraph/various/__pycache__/{__init__,misc,banner,hepmc_parser,lhe_parser}.cpython-39.pyc` and
    `systematics.cpython-39.opt-1.pyc`;
  - `madgraph/iolibs/__pycache__/{__init__,files,file_writers}`;
  - `models/__pycache__/{__init__,check_param_card}`;
  - `HEPTools/lhapdf6_py3/.../lhapdf/__pycache__/__init__`.
- All the non-opt files are stamped 02:38:07. That is the end of the discarded MG-showered chunk (MG's
  HepMC-merging step runs without `-O`). Before that, the install only had `*.opt-1.pyc`, from 2025.
- `input/mg5_configuration.txt`: `# auto_update = 7` is correct (l.86), and there are three `mg5_path` lines as
  claimed. However, the revert left a **dangling `# MG5 MAIN DIRECTORY` comment plus a blank line** at the end of
  the file (`tail | cat -et`), so the file is not byte-identical to its prior state.
- `.DS_Store` and `aloha/` mtimes changed (01:00, 02:05). That is Finder, not attributable to E4.
- No model was linked and no symlink was created; `models/` is unchanged apart from `__pycache__`.
- Functionally harmless, but the brief's rule was "only a model or link".
- Fix: list the exact footprint in VALIDATION §8. With the user's approval, delete the new non-opt cpython-39 `.pyc`
  files and the HEPTools lhapdf `__pycache__`, and remove the dangling comment.

**B3. Tagging discipline: VERIFIED is used for single-generator results, against VALIDATION's own definition
(l.8-10).**
- The following are LO-MLM, single-code statistics, with no independent cross-check. Per l.9-10 they are
  **ESTIMATE**:
  - §3 "ISR tail and ℓ_max bias (VERIFIED, quantified)";
  - §4 "MLM (VERIFIED)";
  - §5 "CP5 vs Monash (VERIFIED)";
  - §1.4 bands "(VERIFIED)" (computed from weights).
- §1.2 "σ_norm/TH = 0.9964-1.0015 (VERIFIED)" re-uses TH's own K values, so it verifies only the LO part (already
  §1.1) and the interpolation.
- The E K-factors are transcribed from TH exactly like the Ẽ ones, but only Ẽ is flagged UNVERIFIED (l.116).
- Fix: re-tag. ℓ_max bias and f(pT>200) become ESTIMATE (LO-MLM, CP5; no NLO/FxFx, no shower variation). E K
  becomes UNVERIFIED transcription of TH, as for Ẽ.

**B4. The ℓ_max / N_osc comparison with the fixed-pT trick is apples-to-apples for ℓ_max but not for the headline
N_osc.**
- The reference (iv) applies |η_pair| < 2.5. The headline (i) applies no η cut (`val_lmax.py:54,59`, all events).
- Only (i') (|η| < 2.5 after the kick, `val_lmax.py:60`) uses the same selection. Its N_osc bias is +26…+52 % vs
  +1…+15 % (actually −3…+15 %) for (i).
- For ℓ_max the two differ by only 1-2.6 points (−25.6 vs −26.5, −10.7 vs −13.0, −6.4 vs −8.0 for E, MG LO), so
  the ℓ_max conclusion stands.
- Also, T2 §3's original comparison (`T2_kinematics.py:287-302`) used no η cut on either side and only m = 500. So
  neither variant reproduces the S-13 definition exactly. "S-13's +20 % lies inside this range" (l.242) is
  uninformative across +1…+52 %.
- (i) is T2's implementation (R = 110, |z| = 270, no η cut). TH App. A used |η| < 1.5, r < 108.3, |z| < 265 and pT
  of 250 or 500 GeV. The label "TH App. A / T2 §3" (l.209) conflates the two.
- Fix: make (i') the primary like-for-like number for N_osc. Show (i) as "T2 §3 as implemented". State the S-13
  correspondence explicitly.
- The ℓ_max and N_osc definitions themselves are correct and identical to T2. ℓ_max = 2(γ*−1)m/σ. N_osc = S_exit/D/2,
  where D = 2p*(βγ)_pair/σ is the lab distance between crossings. σ = 50.68 GeV/cm per keV² is checked.

**B5. The headline uncertainties of the ℓ_max biases omit the merging systematic, and the shower-scale variation was
never run.**
- §0 l.40: "Each value has ±1 % stat and ±1-2 % scale uncertainty". But `lmax_bias.json` F_500 `syst_on_iv` has
  V-MERGE-20 −4.6 ± 3.7 % and V-MERGE-50 −2.4 ± 3.6 %, comparable to the claimed accuracy of (ii) ("−5…+0.5 %").
- TH §5 lists the Pythia ISR shower scale ×½/×2 as the primary ISR/acceptance nuisance. FASER saw ≈ 25 %.
- V-SHOWER was not produced (§8 item 7). Yet §0 calls S-13 "VERIFIED, quantified".
- Fix: either run V-SHOWER at 500 GeV (Pythia `UncertaintyBands` weights; ≤ 1.3 CPU-h per plan §4), or state in §0
  that the ±5 % merging envelope and the missing shower variation bound the precision of (ii)-(iv) at ≈ ±5 %.

**B6. Loader `sigma_fb` is easy to misuse for yields.**
- `mg_events.py:82-87` returns N_IC × Σw, i.e. LO-MLM in the Gμ scheme without K. At 500 GeV in the tail that is
  2 × 0.2612 = 0.522 fb, vs σ_norm × f = 6.11 × 0.104 = 0.636 fb (−18 %).
- Stage 3 will compute yields; plan §5 advertises `sigma_fb(..., n_ic=2)` for "the matched σ of a selection".
- Fix: add `sigma_norm_fb(m, spin, selection)` = σ_norm(TH, interpolated as in `xsec.json`) × (Σw_sel/Σw_INC), or a
  loud docstring warning plus a K/scheme factor table in `SAMPLES_INDEX.json`.

**B7. Reproducibility gaps. Production is reproducible; the σ reference numbers are less so.**
- (a) t16, the LO grid used for σ_norm, gets α = 1/127.9 only from the param card **left behind by t15(b)**
  (`val_xsec.py:123` comment; `probes/t16_lo_grid.mg` has no `set aEWM1`/`set Gf`). Re-running t4 or t16 in another
  order silently changes the LO by 7 %.
- (b) There is no script for t3 (E 500 LO = 2.454 fb, used in `val_xsec.py:86`); it was run interactively via
  `generate_events`.
- (c) There is no pixi task chain; VALIDATION §9 omits the probe re-runs and their order.
- (d) The MG path is hard-coded in `produce.py:25` and `mg_configure.py:12`. The run card is the MG default plus
  `mg_configure` edits; the `cards/run_*.dat` promised in plan §9.2 are not in `cards/`.
- Fix: make every probe script set all EW inputs explicitly. Add `probes/t3_E_incl.mg`. Add pixi tasks
  (`probes`, `produce`, `stitch`, `validate`) in dependency order. Snapshot the effective `run_card.dat` of each
  `prod_*` output into `cards/`.

**B8. The DJR smoothness criterion (V4a) fails for d12 under the plan's own metric, and the metric cannot detect a
step.**
- §4.1: d12 deviations are 11.7 % (E-INC 500, stat 3.8 %), 11.6 % and 13.8 %, against the plan's 10 % criterion.
  The text calls this "Marginal".
- The reference fit is a single quadratic in log y over ±0.6 decades, with χ²/ndf 2-5 even away from qCut
  (`mlm.json`). So the max-deviation number mixes fit inadequacy with any real step.
- Visually there is no step (`djr_E-INC_m500.png`), and the tail observables are bounded directly (§4.2), so this
  does not block.
- Fix: use a local step test. Fit separate linear (log y) segments on [lq−0.3, lq) and (lq, lq+0.3] and quote the
  discontinuity at lq with its error. Report PASS/FAIL against the plan criterion explicitly.

**B9. The figures do not follow the plan or the JFC output rules (non-blocking for Stage-2 diagnostics; must be redone
in Stage 5).**
- Plan §3.3 promised mplhep; VALIDATION l.13 says "plain matplotlib".
- The scripts use `set_title`, numeric `fontsize`, `ax.step`, `tight_layout`, custom figsize and PNG only
  (`val_*.py`, grep).
- Code identifiers leak into titles and legends, e.g. "TRG_CP5_vs_Monash", "V-TUNE-TRG", "log10d01".
- The figures do not say "generator level". The extrapolated (ESTIMATE) σ points at 1300-1500 GeV in
  `xsec_normalisation.png` look identical to the verified ones.
- **No CMS-type label anywhere.** LABEL = "Private work (simulation)" (`vlib.py:19`); no `exp_label` calls. This
  satisfies the brief's hard rule.

### Category C (notes)

- **C-1.** The review brief describes E as "doublet-like". BRIEF l.11 and the UFO make E the SU(2)-singlet
  (1,1)₋₁ (the doublet is L). The model is right; correct the brief wording in future hand-offs. Also, the UFO
  particle attribute `Y = 0` is cosmetic (as in MG's sm); the hypercharge enters through the couplings.
- **C-2.** K above 1200 GeV is extrapolated with the slope between K₁₃.₆(1000) = 1.254 and K₁₃(1200) = 1.292, which
  mixes two √s. Using the 13 TeV slope gives 1.342 instead of 1.349 at 1500 GeV (−0.5 %). The PDF uncertainty beyond
  1200 GeV is frozen at 25 % (`val_xsec.py:125`), which likely underestimates it; tag it as a lower bound.
- **C-3.** The CP5 transcription matches the paper. CMSSW's CP5 block uses full precision (ecmPow 0.03344,
  coreRadius 0.7634, CR range 5.176) and `SigmaTotal` settings; the effect is ≲ 0.3 % on pT0 at 14 TeV. pSet 20 is
  NNPDF3.1 QCD+LUXQED rather than the paper's NNPDF3.1 NNLO. Both are already noted as ESTIMATE; fine.
- **C-4.** One TRG event has pT_ME = 99.97 GeV (status-23 rounding), so the TRG/INC boundary overlaps at the 10⁻⁵
  level. Negligible.
- **C-5.** `etaj = 5` at ME level with `JetMatching:etaJetMax = 1000` (banner). This is the MG default; the effect on
  the pT > 200 tail is negligible.
- **C-6.** The TRGS-vs-INC agreement (SAMPLES/§4.4) is partly correlated, because TRGS contains the INC
  pT_ME < 100 events. The independent test is the generation-cut closure (0.989-1.029), which passes. Say so.
- **C-7.** QED FSR off the quirks does not occur in Pythia with these settings (R13). D12's intent ("keep, physical")
  is therefore not realised. The impact is negligible, and §7 states it correctly.
- **C-8.** Not delivered and not listed in §8: plan V1b's extension (FR vs HW at 200 and 1000 GeV and on an MLM
  pT(QQ̄) shape). Low risk, since the Feynman rules are identical.
- **C-9.** `val_lmax.py` docstring says `figures/lmax_bias_*.png`; the script writes `lmax_bias.png`. `logs/` keeps a
  stale old-flow `convert_E-INC_m500_c0.log`.
- **C-10.** The probe hint "+9 ± 6 %" (plan §0) is correctly retracted in §3(c).
- **C-11.** f(pT>200) is LO-MLM × inclusive K. An NLO K in the tail may differ (TH §5, plan risk 3). This is
  documented; the FxFx point is deferred.

---

## 3. Delivery against the approved plan (§4, §6, §7.1)

| Plan item | Delivered | Comment |
|---|---|---|
| Sample table §4 (≈ 2.3 M LHE) | 46 points, 2.40 M LHE, plus 17 stitched TRGS | complete. S-TRG-fine was dropped by decision; V-SHOWER and V-GAMGAM (optional) not run |
| D1 CP5 nominal, Monash check | yes, verified in all 318 logs (R9) | the MG card re-ordering pitfall was found and handled; a good catch |
| D4 ME cut 100 + V4d closure | closure measured; the plan's "≲ 1-2 %" was wrong (3.9-7.1 %); stitching introduced | A1 concerns the delivery of the stitched sample |
| D6 normalisation to TH §2.3 | yes | B1, B6 |
| D10 no symlink | none | B2 footprint |
| V1a-e | PASS as stated | — |
| V2 | PASS (inclusive γ* worst −1.8 ± 0.8 %) | — |
| V3 | done | B4, B5, A2 |
| V4a | d01 PASS, d12 fails the metric | B8 |
| V4b-c | PASS | — |
| V4d | the "migration ≤ 1 %" criterion FAILED, honestly reported; remedy = TRGS | A1 |
| V5 | done; PDF4LHC21 not added | — |
| V6 | done | C-7 |
| V7 | done: 2000 events, 0 failures, status 1 = both exit (`T3_causal.py:245`) | A1 (loader usage) |
| V8 | MPI and tune done; shower not done | B5 |

---

## 4. Verdict

**ITERATE.**

Open Category A items:
- **A1.** TRGS: the INC complement is appended at the end of the file and carries 4-6× larger weights, while the
  documented Stage-3 path takes the first N events, unweighted. For N up to 7.5k-17k tail events this silently
  returns the ME-cut sample that failed closure. Fix: shuffle with a fixed seed, make the weights mandatory or
  provide an unweighting option, add a regression check, and update the docs.
- **A2.** The §0/§3 headline ranges disagree with `lmax_bias.json` and the §4.1 table. The N_osc bias of the trick is
  −3…+15 %, not +1…+15 %; the d01 bound of 7 % excludes Ẽ and V-MERGE. Fix: correct the ranges and generate §0 from
  the JSON.

Everything else holds up under independent recomputation:
- σ from the weights, closure, stitching arithmetic and ℓ_max biases (R1-R15);
- CP5 in every production job;
- the model couplings and N_IC.

Both A items are cheap. The B items (notably B1, B2, B3, B5, B6) should be addressed in the same iteration.
