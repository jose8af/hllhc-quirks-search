# Stage 2: deferred items (fixer S2-R1, 2026-10-11)

These items were raised by the S2-R1 reviews (`review/CRITICAL_REVIEW_S2_R1.md`, `review/CONSTRUCTIVE_REVIEW_S2_R1.md`) and
deferred by the orchestrator's fix brief. Costs are ESTIMATEs on this machine (M3, 8 cores; measured Stage-2 throughput
≈ 27 ms CPU per LHE event for MG + Pythia + conversion).

| # | Item | Why it matters | What to do | Cost (ESTIMATE) | When |
|---|---|---|---|---|---|
| D-1 | **NLO + FxFx point** (plan D6, "optional later"; critical C-11, constructive B-1(3)) | The ISR-tail rate f(pT > 200) at LO-MLM carries +12…+15 % / −11…−13 % (ME emission α_s, VALIDATION §5.1); an NLO-merged point is the only way to reduce it, and S-13 attributes part of the 37 % reach spread between groups to ISR/K handling | Loop-capable UFO: our E/Ẽ additions on top of MG's `loop_sm` (UV/R2 counterterms for the new colourless states via NLOCT/FeynRules, or a hand-written `loop_sm` extension), then `p p > xe+ xe- [QCD]` with FxFx 0-1j at 500 GeV, Pythia CP5, ~200k events; compare f(pT > 200), the pT(QQ̄) shape and the ℓ_max median with TRGS | 1-2 days of person time (model + validation) + ≈ 10-20 CPU-h (NLO integration and FxFx events are ~10× LO cost) | before publication (constructive review order: "before publication") |
| D-2 | **Λ-grid extension for Stage 3** (constructive B-6) | The planned grid {0.3, 0.45, 0.6, 1, 2, 3, 5, 10} keV samples the mass-dependent lower efficiency edge (0.45-0.7 keV) with 2-3 points and misses the upper (pair-merging) edge at ≈ 20-30 keV; FASER quotes 0.3-100 keV | Stage-3 design decision: e.g. {0.3, 0.4, 0.5, 0.6, 0.7, 0.85, 1, 1.5, 2, 3, 5, 10, 20, 30} keV, 20/30 keV at reduced N; fit the 50 % edge with an interpolating function. No regeneration: kinematics are Λ independent (the same rows at every Λ; `iter_events`, `split`) | Stage-3 CPU: run_causal ∝ N_osc ∝ Λ²: 0.017 s/event at 1 keV → ≈ 15 s/event at 30 keV, ≈ 1 h per 200-event mass point at 30 keV (measure first) | Stage 3 |
| D-3 | **Figure restyle to the JFC / mplhep rules** (critical B9, constructive B-10) | Stage-2 figures are internal diagnostics (custom figsize, `set_title`, numeric fontsize, `ax.step`, PNG only, no √s label, unlabelled DJR y axis, no yerr on DJR ratios, extrapolated-K points not distinguished until S2-R1). Any figure reused in Stage 5 or the paper must follow `methodology/04-output.md` (Category A there) | One `plotstyle.py`: `mh.style.use("CMS")` geometry only, `figsize=(10,10)`, ratio panels `height_ratios=[3,1]`, `sharex`, `hspace=0`, `mh.histplot` with explicit `yerr`, PDF+PNG; label `exp_label(exp="", llabel="Private work (simulation)", rlabel="√s = 14 TeV")`, never a CMS-type label; "generator level" on Stage-2 plots and "PU 200, 3 ab⁻¹" only on detector-level (Stage 4) or yield figures; PDF4LHC21 band on the σ figure | ≈ 0.5-1 day | Stage 5 |

Done in S2-R1 for the figures (not deferred): the label is "Private work (simulation, generator level)" on every Stage-2
figure (`vlib.LABEL`), no CMS-type label exists anywhere (`grep CMS scripts/*.py`: only the CP5 provenance), and the
extrapolated-K masses are drawn with open markers in `figures/xsec_normalisation.png`.

Related open points that are NOT deferred items of the brief but need an orchestrator decision (see `review/FIX_S2_R1.md`):
- **QED FSR off the quirks** is absent from the delivered samples (VALIDATION §7): −0.1…−1.1 % on the tail median of ℓ_max
  (paired bootstrap stat. error ±0.5…0.8 % per point; mean −0.4…−0.8 ± 0.2 %), above the 0.3 % threshold. **Default:
  delivered samples have no QED FSR off quirks; pending user decision: re-shower ~15 CPU-h vs one-sided systematic.** Either
  re-shower the physics samples with `cards/pythia8_quirk_qedfsr.dat` (no MG rerun; the LHE is kept; ≈ 15 CPU-h, beyond the
  remaining ≈ 11.5 CPU-h of the approved budget) or carry a one-sided ℓ_max systematic, stated as −1.1 ± 0.8 % (stat)
  (largest median shift) or the mean −0.4…−0.8 ± 0.2 %, not as a bare −1 % (S2-R2 C-5).
- **Finer interpolation closure for P2** (constructive B-7): the 550 GeV INC closure is statistically limited (±2-3 % on the
  tail medians). Two off-grid TRG points (450, 650 GeV, ≈ 1 CPU-h each) would test interpolation at ≪ 1 %, if P2's template
  fits need it (Stage 3).
- **Stage-4 handover notes** (constructive C-8, C-9, C-14, B-5(3)): apply the luminous region (σ_z ≈ 4-5 cm, σ_t; UNVERIFIED)
  jointly to the T3 quirk hits and to regenerated particles; define the fiducial denominator per quirk (Phase-2 tracker
  |η| ≈ 4), not per pair; add the pair's calorimeter deposit (≲ 5 GeV, one-sided ≲ 2 % MET bias) to the MET model.

## Added after review S2-R2 (2026-10-11)

- **C-8 (folded into D-3, figure restyle).** `figures/lmax_bias.png`: the y-axis label is clipped; and the figure does not
  say that the "(i) no η cut (both)" series is relative to (iv-noeta), not to the TRGS \|η\| < 2.5 reference named on the
  axis. Fix both when the figure is restyled under D-3 (label the reference per series in the legend, or split the panel).
