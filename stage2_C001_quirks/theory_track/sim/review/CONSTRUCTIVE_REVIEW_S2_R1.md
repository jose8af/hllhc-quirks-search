# Constructive review S2-R1: Stage 2 (MG5_aMC 2.9.22 + Pythia 8.313 quirk-pair samples)

Reviewer: constructive (downstream fitness), 2026-10-11. Classification per `jfc/src/methodology/03-review.md` §6.1:
**A** = correctness error (blocks); **B/C** = advisory (B = substantive for the next stages or for publication;
C = minor / documentation).

Material read: `sim/plan.md`, `sim/VALIDATION.md` (all), `sim/SAMPLES.md`, `sim/README.md`, `sim/E4_session_log.md`,
`results/*.json` (xsec, samples, summary_tables), all of `figures/` listed and 6 viewed, `scripts/{mg_events,stitch_trg,
convert_hepmc (header + weight block),val_xsec (bands),produce (seeds)}.py`, `outputs/THEORY_GAPS_SYNTHESIS.md` v5
(Box A/B, S-4, S-5, S-13, S-17, S-18, P1/P2 rows), `research/theory_signal_model.md` §2.2-2.4.

Spot checks (scripts and outputs in `sim/review/r1_constructive_checks/`, all run with `pixi run -e ana python`):

| ID | What | Output |
|---|---|---|
| c1 | weight bookkeeping (w, named merged, AUX, Weight) in TRGS/INC/LOPS | `c1_weights.out` |
| c2 | does the 9-point (μ_R, μ_F) set move the ISR tail? | `c2_scale_tail.out` |
| c3 | eikonal estimate of QED FSR off the quirk pair | `c3_qed_fsr_estimate.out` |
| c4 | per-point Stage-3 statistics of TRGS (N, Kish N_eff, INC share, file position) | `c4_stage3_stats.out` |
| c5 | bias of the documented "first N of `iter_events`" pattern | `c5_firstN_bias.out` |
| c6, c7 | is the file order random? (block structure, 46 files × 12 blocks) | `c6_file_order.out`, `c7_order_scan.out` |
| c8 | tail events per γ* bin (P1 γ*-dependent claims) | `c8_gamma_bins.out` |

Numbers reproduced: Σw(TRGS m500) = 2.5044 fb vs σ_matched(INC) 2.5070 fb; σ(pT>200) TRGS/INC = 0.2612/2.507 =
0.104; N(3 ab⁻¹) = 6.11 × 0.104 × 3000 = 1.91e3 (m500) and 7.27 (m1500); K(1300) = 1.311 (linear from 1100/1200);
named central weight = `w` to 3e-16; `Weight_MERGING=45` sum = Σw. File order is random (c7: rms z = 0.92 over 552
blocks, 3.8 % with |z| > 2, expect 4.6 %), so the only ordering issue is the stitching (A-1).

---

## 0. Summary for the orchestrator

**What is strong.** The cross-section chain is two-code verified at LO (MG vs App. A, FR vs hand UFO), the EW-scheme
and LO-scale numbers reproduce TH, the CP5 card was checked against the paper and the MG card-reordering pitfall was
found and fixed. The ME-cut migration was caught and fixed by stitching. TRGS is the full MLM phase space (Σw = σ_INC),
so trigger-threshold variations below 200 GeV are possible. Statistics in γ* bins are enough for P1's γ*-dependent
statements (c8: γ* > 2 has 2416/1014/238 tail events at 200/500/1000 GeV). The loader, seeds and reproduction recipe
are in place.

**What blocks (1 A).** The loader + stitched-file layout makes the Stage-3 usage pattern that the documentation
recommends (A-1) silently drop the INC complement, which is exactly the 4-7 % that §4.4 found missing. The fix is
cheap.

**What a referee would ask (B).**
- The ISR-tail uncertainty is under-covered. The μ_R weights do not vary the α_s of the emissions, no shower
  variations were run, and there is no NLO point (B-1).
- Normalisation and weight-column traps: `sigma_fb` is 17-38 % below σ_norm; 104 unmerged AUX columns; a mislabelled
  JSON key (B-2, B-3).
- Statistics are quoted in raw events, not effective events (B-4).
- Stage 4 lacks the per-event final-state particles that motivated MPI-on (B-5).
- The Λ grid misses the upper edge (B-6).
- P2 needs an interpolation closure test (B-7) and a split between template and pseudo-data events (B-8).
- The QED-FSR estimate is about 10× low and the approved setting did not take effect. It is harmless at present
  precision (B-9).
- The figures are far from the JFC rules (B-10).

---

## 1. Category A

### A-1. `iter_events(sample='trig')` on the stitched files returns a biased subset for the documented "first N" usage; the docstring's equal-weight claim is false for TRGS
**Evidence.**
- `stitch_trg.py` concatenates `[TRG rows] + [INC rows with pT_ME < 100]`, and the loader alias `trig` now points to
  TRGS.
- `mg_events.iter_events` yields the selected rows in file order. Its docstring says "unweighted MG events: weights
  are equal up to MLM/systematics factors". `plan.md` §4/§5 and the loader header tell Stage 3 to "take the first N at
  every Λ".
- c4: in the tail (w > 0, pT > 200, |η_pair| < 2.5), the first INC-origin event is at selected position
  6195-16927, i.e. after **every** TRG tail event, at all 17 points. Any N below the TRG count therefore never sees
  the complement.
- The complement carries **3.9-7.3 % of σ_tail** (c4, column INCsig%), with per-event weights **4-11× larger**
  (3.7-4.4× at the benchmarks, 7-11× on the fine grid). SAMPLES.md says "≈ 4-5×".
- The complement is kinematically different. Its weighted median γ*−1 is 0.260 vs 0.273 for the TRG part (m500) and
  0.113 vs 0.149 (m1500) (c1).
- If the events are treated as unweighted (as the docstring invites), the median γ*−1 of the tail is biased by
  +0.03 / +0.4 / +1.0 / +1.7 % at 500 / 1000 / 800 / 1500 GeV relative to the weighted full TRGS (c5, unweighted
  median over all tail rows). The rows are 98-99.5 % TRG, so this equals dropping the complement; the TRG-only
  weighted median in c1 gives +1.8 % at 1500 GeV.
  Efficiencies and yields built as unweighted fractions of the first N miss the 4-7 % component that VALIDATION §4.4
  classed as a FAIL of the "migration ≤ 1 %" criterion.
- Using the full file unweighted is also wrong, because the INC rows need their 4-11× weight.

**Why A.** The recommended interface, used as documented, recomputes the very bias the stitching was built to remove,
and the docstring states something false about the file. The size (≤ 2 % on medians, 4-7 % on rates) is small but
systematic and mass dependent, and it would enter every Stage-3/4 efficiency.

**Fix (≈ 1 h).**
1. In `stitch_trg.py`, shuffle the stitched rows with a fixed seed (keep `origin`). Re-run it and the loader
   validation (`val_loader.py`).
2. Make the loader weight-explicit. Either:
   - (a) `iter_events(..., unweight=True, seed=…)`: deterministic hit-or-miss unweighting (keep row k if
     u_k < w_k / max w). This gives an equal-weight subsample, so "first N" is valid and the same events are used at
     every Λ. Or:
   - (b) always return `info['w']` and state in the docstring that Stage-3 summaries must be weighted.
3. Correct the docstring and SAMPLES.md ("4-11×", plus the Kish N_eff, see B-4).
4. Add a unit test: weighted median γ*−1 of `iter_events(trig)` = that of the full file, within statistics.

---

## 2. Category B (advisory, substantive)

### B-1. The ISR-tail (pT(QQ̄) > 200) modelling uncertainty is under-covered: the 9-point "scale" weights do not vary the α_s of the emissions; no shower variation; no NLO point
**Evidence (c2).**
- In MLM (`ickkw = 1`) MG evaluates the α_s of the extra partons at the CKKW clustering scales. `--mur` only rescales
  the "hard" α_s, which a Drell-Yan-like core does not have.
- Under μ_R × 2, events with n_me = 1 have a mean weight ratio of 0.9996 (500 GeV). Only 1-5 % of events have any
  μ_R dependence.
- The tail fraction f(pT > 200) moves by only ±0.3-1 % over the 9 points (m500: 0.0849-0.0860 vs 0.0854). The 9-point
  envelope is μ_F (PDF evolution) almost entirely.
- VALIDATION §3 quotes "9-point scale ±0.8…1.8 %" on the ℓ_max median as if it were a scale uncertainty on the tail.
- V-SHOWER (ISR/FSR variations) was not run. NLO-FxFx was deferred (D6).
- The only tail-rate handles left are merging (−5.5/+3.9 %), multiplicity (+3.9 %) and the MLM vs LO+PS difference
  (9-10 %).
- S-13 itself attributes a 37 % reach spread between groups partly to ISR/K handling.

**Downstream.**
- P2 uses the MET recoil (pT(QQ̄)) and the γ* distribution of triggered events; a template fit needs a credible
  pT(QQ̄)-shape uncertainty.
- Stage 4/5 yields scale with f(pT > 200), and a conventional LO-MLM tail uncertainty is ±10-20 %, not ±1 %.
- P1 is barely affected (the thickness is m_Q independent and is studied in γ* bins).

**Fix.**
1. Run MG's standalone `systematics` on the kept LHE with `--alps=0.5,1,2` (and `--together=mur,muf,alps`). Convert
   to merged weights with the per-event matching factor w/AUX_central, as `val_xsec.py` already does for NNPDF23. This
   needs an LHE ↔ npz-row map (B-5).
2. Reshower one 500 GeV TRG chunk with Pythia `UncertaintyBands` (`isr:muRfac` = 0.5/2), or run two separate runs.
3. Run the planned FxFx 0-1j NLO point at 500 GeV.
4. Until then, state in VALIDATION §0/§1.4/§3 that the 9-point band is a normalisation (μ_F) band, not an ISR-shape
   band. Carry the merging envelope plus LO+PS-vs-MLM (≈ ±10 %) as the provisional tail-rate nuisance.

### B-2. Normalisation recipe: three easy ways to get the yield wrong
**Evidence.**
- (i) `mg_events.sigma_fb(..., n_ic=2)` returns 2 × the LO-MLM σ in the Gμ scheme. That is **17-38 % below
  σ_norm**: σ_norm/(2 σ_matched) = 1.17 (200), 1.22 (500), 1.30 (1000), 1.38 (1500 GeV). The function name and
  docstring do not warn about this.
- (ii) σ_norm is in SAMPLES.md and `xsec.json` but not in the npz files or the index, so every downstream user must
  re-join it by hand.
- (iii) `xsec.json:normalisation_E.rows.*.lo_mg_gmu_fb` holds the **α = 1/127.9** LO (98.74 fb at 200 GeV). The Gμ
  value is 92.52 fb. The key name is wrong.
- (iv) σ_norm omits two **positive** corrections that the theory track itself quantifies: inelastic γγ (+4.0-4.2 %,
  S-20/T6) and the IC Sommerfeld factor (+5-15 %, TH §2.4). The EW-scheme spread (+7…10 %) is a nuisance on top.
  SAMPLES.md does not list these.

**Fix.**
1. Write `sigma_norm_fb` and a `normalisation_tag` into each npz and into SAMPLES_INDEX.json.
2. Add `yield_fb(selection, sample='trig')` = σ_norm × Σw_sel / Σw_all. For TRGS, Σw_all = σ_matched(INC), already
   true.
3. Rename `sigma_fb` to `sigma_lo_mlm_fb` (or add a loud docstring line).
4. Rename the JSON key to `lo_mg_alpha127p9_fb`.
5. Add a "not included in σ_norm" box to SAMPLES.md: γγ +4 %, Sommerfeld +5-15 %, NLO-EW −few % (UNVERIFIED);
   nuisances EW ±7-10 %, PDF4LHC21 ±3.7/6.6/18.5 %.

### B-3. Weight-column hygiene in the npz files
**Evidence (c1).**
- `wvar` has 211 columns. The 104 `AUX_*` and `Weight` are **unmerged** LHE weights: they sum to 1.23-1.46 ×
  σ_matched and are non-zero on vetoed rows. They sit in the same array, in the same "fb per event" units, as the 107
  merged named columns.
- The AUX → meaning map (e.g. AUX_45 = unmerged central, AUX_104 = NNPDF23LO, per `val_xsec.py`) is documented
  nowhere in SAMPLES.md.
- 21 % of rows have w = 0. They are kept for the qCut 67.5/90 variations. The loader filters them, but anyone who
  reads the arrays directly gets 21 % unphysical rows in unweighted counts or medians (`kept` in SAMPLES.md counts
  them).

**Fix.**
1. Either convert the AUX columns to merged ones (× w/AUX_central) or rename them `LHE_unmerged_<meaning>`.
2. Write the name map into SAMPLES.md.
3. Add one helper (`variations(c, kind='scale9'|'pdf68'|'merging'|'dyn')`) so every stage uses the same envelope
   recipe: CT18 asymmetric Hessian ÷ 1.645, 9-point or 7-point.
4. State "rows with w = 0 exist; always weight or use the loader" at the top of SAMPLES.md.

### B-4. Statistics are quoted in raw events; Stage-3 targets should be in effective events tied to the precision goal
**Evidence (c4, c5).**
- Kish N_eff/N in the tail is 0.85-0.90 at the benchmarks but **0.70-0.78 on the fine grid** (N_eff ≈ 4.4-5.5k).
- The plan's "200 events survive down to ε ≈ 2.5 %" is therefore ≈ 4 % in effective events.
- With N = 2000 the median γ*−1 has a ±2.7 % (E1000) bootstrap error. Independent 2000-event head subsamples deviate
  by up to +7.4 % (2.7σ, c5/c6). "≥ 200 events" therefore gives ≈ ±9 % on a median: enough for efficiency maps, far
  from P2's 1-3 % CRB claims.
- At 200-400 GeV, MC N_eff in the tail (12.3k / 4.4k / 4.9k) is only about 2.5-3× the expected 3 ab⁻¹ signal after a
  Knapen-like ε ≈ 0.18 (4.9k / 1.6k / 0.6k).

**Fix.**
1. Add N_eff to SAMPLES.md.
2. Restate the Stage-3 requirement as "≥ 200 *effective* events after selection, and MC-stat ≤ ⅓ of the 3 ab⁻¹
   data-stat for P2 template points".
3. Top up the INC complement on the fine grid: +80k INC per mass brings the weight ratio from 7-11× to ≈ 2×, ≈ 1
   CPU-h per mass.
4. Top up TRG at 200-400 GeV (≈ 1 CPU-h per 20k matched).

### B-5. Stage-4 inputs: the per-event final state was deleted, and rows cannot be mapped back to LHE events
**Evidence.**
- D2 justifies MPI and hadronisation on "for the Stage-4 ACTS overlay" and UE occupancy (plan §7).
- The npz keeps only `recoil`, `recoil_eta5`, `nu` and 4 jets; HepMC was deleted.
- A CMS-like tracker study of a coplanarity finder needs the signal event's own charged particles: the ISR-jet tracks
  and UE hits near the quirk plane (S-5 counts on the MET wedge being depleted of jet activity; the finder's fake rate
  depends on UE hits inside that wedge).
- Pythia seeds are recorded (`produce.py`: `(seed·10 + j)`) and the LHE is kept, so regeneration is possible. But
  there is no (chunk, split, event) column in the npz to map a Stage-3 row back to its LHE event. The same map is
  needed for B-1(1).

**Fix.**
1. Add `chunk`, `split` and `ievt` columns (re-run the converter on the kept LHE, or reconstruct the map from the
   chunk/split ordering).
2. For the Stage-3 subset of each point, reshower deterministically and store the charged stable particles (pT > 0.5
   GeV, |η| < 4, production vertex). That is ≈ 100-200 tracks/event, i.e. tens of MB per point.
3. Document that the beam-spot shift (σ_z ≈ 4-5 cm, σ_t, UNVERIFIED) must be applied jointly to the T3 quirk hits
   and to these particles in Stage 4.

### B-6. The Λ grid planned for Stage 3 ({0.3, 0.45, 0.6, 1, 2, 3, 5, 10} keV, plan §4) does not reach the upper edge and thinly samples the lower edge
**Evidence.**
- Box A: the lower 50 % edge is at 0.45-0.7 keV, mass dependent (0.55 → 0.7 at 1 TeV); full efficiency is reached
  only at ≈ 2 keV for 1 TeV; the **upper edge** (pair merging) is at ≈ 20-30 keV. FASER's contour is quoted at
  0.3/0.5/1/1.7/3/10/30/100 keV.
- The grid gives 2-3 points across the lower edge and none at the upper edge.
- Stage 1's B law is verified only up to ≈ 5 keV (unattributed ±5 % above). P1 claims above 5 keV need the measured
  systematic.

**Fix.**
1. Use {0.3, 0.4, 0.5, 0.6, 0.7, 0.85, 1, 1.5, 2, 3, 5, 10, 20, 30} keV, with 20/30 keV at reduced N. The cost
   scales as N_osc ∝ Λ²: 0.017 s/event at 1 keV gives ≈ 15 s/event at 30 keV, i.e. ≈ 1 h per 200-event mass point
   (ESTIMATE; measure first).
2. Fit the 50 % edge with an interpolating function and quote its uncertainty.

### B-7. Mass grid for P2: 100 GeV spacing needs an interpolation (morphing) closure test
**Evidence.**
- The E grid (14 masses, 200-1500) is ample for P1 (thickness is m_Q independent) and for the reach (≈ 1.1-1.3 TeV).
- P2 aims at σ(m)/m ≈ 1-3 % (5-15 GeV at 500 GeV, S-4). That is ≪ the 100 GeV spacing, so any template-based or
  SBI-on-grid inference interpolates in m_Q.
- The γ* shape moves slowly (median γ*−1 0.30 → 0.18 from 200 → 1000), but the interpolation error is unmeasured.

**Fix.**
1. Generate two off-grid TRG points (e.g. 450 and 650 GeV, ≈ 1 CPU-h each).
2. In Stage 3, show that templates interpolated from the neighbours reproduce them to ≪ 1 % in the fitted
   observables. (Optional: a fine 10 GeV mini-grid around 500 GeV if SBI is pursued.)

### B-8. P2 pseudo-experiments must not reuse template events (tautology guard)
**Evidence.**
- Stage 3 deliberately propagates the same kinematic events at every Λ. That is good for smooth efficiency curves.
- With the "take the first N" pattern, templates and toys for P2 would both come from the head of the same file. Fit
  closure would then be partly circular (03-review §6.4, tautological comparison).

**Fix.** Add a deterministic `split` column (e.g. from a hash of (chunk, ievt) → {template, toy, spare}) and make
`iter_events(..., split=...)` the only route. State the rule in SAMPLES.md.

### B-9. QED FSR off the quirks: the approved setting (D12) did not take effect, and the quoted ESTIMATE is ≈ 10× low (harmless at present precision)
**Evidence.**
- D12 (approved): keep QED FSR on and report the rate. VALIDATION §7 finds 0 events with an m(QQ̄) deficit > 5 GeV,
  says Pythia "does not act on these BSM states with the settings used" without a diagnosis, and estimates the
  physical rate at "10⁻³".
- c3 (eikonal final-state dipole, dP = (2α/π)[(1+β²)/(2β) ln((1+β)/(1−β)) − 1] dE/E, β = β*, per event from the
  samples):
  - P(E_γ > 5 GeV) ≈ 1.5 / 1.4 / 1.2 % (LOPS 200 / 500 / 1000) and 1.9 % (TRGS-200 tail);
  - P(E_γ > 20 GeV) ≈ 0.8-1.3 %.
- About 700 such events would therefore have been expected in a 50k sample, so the shower was certainly inactive.
- Impact: the mean fractional loss of pair kinetic energy is ≈ (2α/π)·R ≈ 0.3 %. Shifts in γ*−1 or the ℓ_max median
  are ≲ 0.3 %, below MC stat. This **cannot bite P1/P2 at the present precision**, but a referee would ask.

**Fix.**
1. Correct the estimate in VALIDATION §7 (formula + c3 numbers).
2. Diagnose the cause with a 1k-event run printing `TimeShower:QEDshowerByOther` and the interface settings. Either
   enable it (a 500 GeV TRG chunk, compare γ* and MET) or document it as a ≲ 0.3 % known bias.

### B-10. Figures are far from the JFC plotting rules (04-output.md); the plan promised mplhep + a non-CMS label
**Evidence (grep of `scripts/val_*.py` + inspection of 6 PNGs).**
- Custom figsizes ((11,4), (14,6), (15,6), (6.4,6), …), `ax.set_title(...)`, numeric `fontsize=`, `ax.step` for
  histograms, `tight_layout()`, PNG only (0 PDF), no `mh.style.use("CMS")`, no `exp_label`, no √s on any figure.
- DJR figures: the y-axis is unlabelled (values 10⁻¹⁶-10⁻¹³ without units) and the ratio points have no `yerr`.
- `xsec_normalisation.png`: no PDF/scale band, and the extrapolated-K points (1300-1500) look the same as the
  interpolated ones.
- `lmax_bias.png`: the selection (pT > 200, |η| < 2.5) is not stated.
- Plan §3.3/§6 said "mplhep, non-CMS label".
- Advisory for internal validation plots. Any figure reused in Stage 5 or the paper must be redone: there the
  violations are Category A per 04-output.md.

**Fix.**
1. Create one `plotstyle.py`: `mh.style.use("CMS")`, `figsize=(10,10)`, ratio `height_ratios=[3,1]` with
   `sharex=True` + `hspace=0`, `mh.histplot` with explicit `yerr` for derived quantities, PDF+PNG, `mpl_magic`.
2. Use a non-CMS label, e.g. `exp_label(exp="", llabel="Private work (simulation)", rlabel="√s = 14 TeV")`.
3. Add **"PU 200, 3 ab⁻¹" only on detector-level (Stage 4) or yield figures**. Generator-level Stage-2 plots have no
   pile-up and must not carry "PU 200".
4. Use open markers (or a hatch) for the extrapolated-K masses and add the PDF4LHC21 band to the σ figure.

---

## 3. Category C (minor / documentation)

| ID | Item | Suggested fix |
|---|---|---|
| C-1 | **1→2 jet DJR (d12 8-14 %, "marginal").** It is bounded by V-NJ1 (+3.9 % on f) and the merging envelope; d12 drives the 2nd-jet fraction, not pT(QQ̄). P1/P2 are insensitive. The quadratic reference fit (χ²/ndf 2-5) is the weak part of the test. | Show d12 for the qCut-variation runs overlaid, with stat errors on the ratio; quote the 2-jet fraction change between (20,30) and (50,75). |
| C-2 | **Extrapolated K at 1.3-1.5 TeV.** It is bounded in practice: these masses are beyond reach (≤ 19 events at 3 ab⁻¹ before efficiency) and K is smooth (+0.019/100 GeV). The anchor at 1200 GeV is a 13 TeV NLO+NLL K (TH §2.2) while ≤ 1 TeV uses 13.6 TeV NNLL, so there is a seam at 1.0-1.2 TeV. No uncertainty is attached to the ESTIMATE. | Assign ±2 % (linear vs quadratic extrapolation) or compute with Resummino (public) at 14 TeV for 1.1-1.5 TeV. |
| C-3 | K(13.6 TeV) is used at 14 TeV (TH assumption, < 1.5 %). The `xsec.json` note says "K_WG(13.6 TeV)" without saying it is applied at 14 TeV. | One sentence in SAMPLES.md/VALIDATION §1.2. |
| C-4 | TRGS and INC share the complement events, so "TRGS agrees with INC within stat" is partly tautological for the 4-7 % share. The independent test is the generation-cut closure (done, PASS). | Say so in §4.4; never use TRGS and INC as independent nominal/cross-check pairs. |
| C-5 | m1100: TRGS vs INC σ(pT>200) = 0.006399 vs 0.006766 (−5.4 %, ≈ 2σ of INC stat). | Note it; the INC top-up of B-4 resolves it. |
| C-6 | Ẽ only at 200/500/1000 GeV (user decision). Enough for a P2 spin-hypothesis bias test (fit Ẽ pseudo-data with E templates) at three masses. Not enough for an Ẽ shape interpolation across the Ẽ reach (≲ 600 GeV). | Plan the spin-bias test at 200/500; add Ẽ 300/400/600 only if Ẽ becomes a result. |
| C-7 | Not simulated: \|q\| = 2 (S-17), γγ → QQ̄ (V-GAMGAM), Sommerfeld, NLO EW. | A "not simulated / size / sign" box in SAMPLES.md (see B-2). |
| C-8 | The vertex is at the origin (D9) and T3_causal assumes the origin. | Stage 3/4 handover note: apply the luminous region and the vertex time consistently (B-5(3)). |
| C-9 | `eta_max` in the loader cuts η_pair (T2 table convention). The Phase-2 tracker reaches \|η\| ≈ 4, and the per-quirk η of slow heavy pairs differs from η_pair. | Define the Stage-4 fiducial denominator per quirk; keep η_pair only for T2 comparisons. |
| C-10 | The TRGS files lack `nlhe` and `sigma_lhe_fb` (renamed `*_trg`/`*_inc`), so code expecting them breaks; there is no `kind` tag. | Add `kind='stitched'` and keep both originals. |
| C-11 | "σ_norm/TH = 0.996-1.0015 (VERIFIED)" is an LO two-code check (MG vs App. A code). It is not a validation of K, which is transcribed from TH. | Phrase it as such. |
| C-12 | `plan.md` header still says "production and validation in progress", and §0 keeps the "≲ 1-2 % below 100 GeV" probe claim that V4d overturned. | Update the header; add a pointer to VALIDATION §4.4. |
| C-13 | No CP5 eigentune / UE variations. The CP5→Monash shift (≤ 2 % on tail observables, +6-8 % n_jets) is reported as a shift, not a band. This matters only for Stage-4 UE occupancy. | Optional: CP5 eigentune pair on one point if Stage 4 shows UE sensitivity. |
| C-14 | The MET proxy assumes the quirks are invisible; S-4 (iv) notes ≲ 5 GeV calorimeter deposit by the pair (a one-sided ≲ 2 % MET bias). | Stage-4 note: add the pair's calorimeter deposit to the MET model. |
| C-15 | The fine-grid INC samples (20k LHE, ≈ 0.8-1.4k tail events) give f(pT>200) with ≈ 3 % stat. The yields table uses INC denominators that carry this error, but it is not quoted. | Add the stat error to the f columns. |
| C-16 | `T2compat_cache.npz` and `P-INC` sit in the physics directory. | Move them to `npz/aux/` (they are already flagged as non-physics). |

---

## 4. Answers to the five questions

1. **Mass/Λ grid.**
   - Mass: adequate for P1 and the reach (E 200-1500 in 100 GeV steps; benchmarks with 2.5× statistics). For P2 it
     needs an off-grid interpolation closure (B-7). Ẽ: three masses, enough for a spin-bias test (C-6).
   - Λ: the planned Stage-3 grid lacks the upper edge (20-30 keV) and is thin across the mass-dependent lower edge
     (B-6). Kinematics are Λ independent, so this is purely a Stage-3 choice: no regeneration needed.
2. **Weights, stitching, per-event systematics.**
   - The weights themselves are correct: named central = w to 1e-16, Σw = σ_matched, TRGS Σw = σ_INC, merged PDF and
     scale columns consistent between TRG and INC.
   - The traps are in the interface: A-1 (order plus equal-weight claim), B-2 (`sigma_fb` vs σ_norm; JSON key),
     B-3 (unmerged AUX columns; w = 0 rows), and B-1 (the "scale" weights do not cover the ISR-tail α_s).
3. **Caveats.**
   - 1→2 DJR: bounded (C-1).
   - Extrapolated K: bounded in practice, beyond reach (C-2).
   - No QED off the quirks: harmless (≲ 0.3 % on γ*), but the documented 10⁻³ is ≈ 10× low (B-9).
   - Large TRGS weights: under-documented (4-11×, N_eff/N 0.70-0.78; B-4), and they bite through A-1.
   - The caveat that can actually bite P2 is the one not listed: the ISR-tail uncertainty (B-1).
4. **What a phenomenology referee would ask for.**
   - NLO (FxFx) or at least α_s-emission and shower variations for the triggered tail (B-1).
   - The γγ and Sommerfeld contributions and the full normalisation nuisance list (B-2).
   - MC statistics relative to the expected data (B-4).
   - Particle-level UE for the tracker study and PU realism (B-5).
   - The upper Λ edge and the FASER comparison points (B-6).
   - Interpolation closure and independent toys for P2 (B-7, B-8).
   - A QED-radiation statement backed by a number (B-9).
5. **Figures vs the JFC rules.** Not close (B-10). They are fine as internal diagnostics but must be rebuilt for
   Stage 5, with a non-CMS label, √s = 14 TeV, and "PU 200, 3 ab⁻¹" only where those apply.

---

## 5. Verdict

**ITERATE (1 A, 10 B, 16 C).** The samples are physically sound and the validation is unusually thorough for a pheno
stage. The single Category-A item (A-1: stitched-file order plus the equal-weight docstring, which makes the
documented Stage-3 pattern drop the 4-7 % INC complement) is a ≈ 1 h fix: shuffle at stitch time, weight-explicit or
deterministic-unweighting iterator, corrected docstring, re-run `val_loader.py`. After it, Stage 3 can start.

Recommended order for the B items:
- before Stage 3 starts: B-2, B-3, B-4, B-8 (interface and documentation);
- alongside Stage 3: B-6 (Λ grid) and B-7 (off-grid masses);
- before Stage 4: B-5 (per-event particles, event map);
- before publication: B-1 (ISR-tail uncertainty, including the FxFx point), B-9 and B-10.
