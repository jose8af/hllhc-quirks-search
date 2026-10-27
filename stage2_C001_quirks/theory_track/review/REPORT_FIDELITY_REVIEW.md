# Report fidelity review (RP-fid, Opus) — quirks_theory_report.tex vs synthesis v4
Date 2026-10-08. Saved by the orchestrator from the reviewer's final reply (the reviewer's file write was refused by the tool).

**Verdict: ITERATE (0 A, 3 B, 13 C).** Report faithful to v4: numbers match in every checked table (incl. the 8-row
smearing table and all 12 stopped-reach cells); no withdrawn claim appears as a live claim outside review history /
own-errors.

## B items
1. **Data relocation**: report still points to the session scratchpad (caution box l.189-191; next-steps row 0 l.995;
   own-errors "Reproducibility" l.687; file tree lacks `data/`; inventory l.1084). Repoint to `theory_track/data/`
   (`cache/T2_kinematics_cache.npz`, `pdf/CT18NLO/`, `athena_quirks_snapshot/`, `tdr_geometry/`, `data/README.md`;
   env `T2_CACHE`/`T2_PDF` override).
2. **FASER HEPData** (writer's finding confirmed): 57/72/113/149/163/179/173 GeV at 0.3/0.5/1/1.7/3/10/30 keV, 71 GeV at
   100 keV [`research/theory_signal_model.md` l.103, l.483; already plotted by `code/T1_figure.py`]. Re-run of R3 per-Λ
   logic with Λ-flat Run-2+3 bands (B=0: 220-340; B=10: 170-260; B≈80: 150-200 GeV):
   corrected statement — *beats FASER/D0 at Λ ≲ 1.5 keV and (extrapolated) near 100 keV even with B≈80; at 2-5 keV
   needs B ≲ 10; at 10-30 keV B≈0; 50 keV undecided (no HEPData point).* Exec summary l.90, stopped bullet l.822,
   recast and P6 text still say Λ ≲ 2 keV; Box A l.358 leads with by-eye values. Use HEPData as the single primary set.
3. **(a3)/(a4) tables** (TH, OQ): must/should severities are not in v4 §4.3-4.4 — label them as the writer's or remove.

## C items
- Exec l.109: strategy 6/16/33 ns are medians at fixed pT = 250 GeV that coincide with the 84th percentiles of the real
  spectrum (6.2/16.5/32.8 ns) — reword.
- Exec l.106: add R4-C2 qualifier (Λ-independence tested only at γ* = 1.28; γ* dependence only at 1 keV).
- §4 l.601 "23 rows count 12/5/3/1" sums to 21 (v2 rows only; rows 22-23 added in v3).
- Own-docs table, window row: truth-level window is EST (T3 code only), causal thickness VER.
- Own-disc writer item 1: by-eye gaps are 8/14/13/~5 GeV at 1/1.7-2/3/5 keV.
- Ranked row 5 "Corrects 2108.06748 §5" → "not supported by the theorem".
- 2512.20696 authors are Asadi, Kribs, Luty — drop "et al.".
- 1911.02223 App.A cell: 0.24 vs 0.10 trigger efficiencies are Knapen's D^c vs E^c, not Knapen vs Li on the same channel.
- Athena: snapshot confirms MonopoleLooperKillerToolCfg (QuirksConfig.py l.69), DistChord()=0 / yerr=0 TODOs
  (HyperbolaStepper.cxx l.80-86), "possible instability" TODO (HyperbolaStep.cxx l.116-117); MaxSteps=2e6 / BSM_Only come
  from G4UserActionsConfig.py and LooperKiller.cxx, read by T2 on 2026-10-07 but not in the snapshot — say so.
- "KLN" → "Kang-Luty" in text (S-5, ranked rows 6/14/16, Li-method discrepancy row); INSPIRE confirms 2 authors.
- T2_transverse_check caption accurate; optionally note no convergence test was run.
- T1_lambda_plane caption: freeze-in contours carry T1 normalisation (×2.2 above 2512.20696 Fig.4, unresolved).
- T6_coverage caption: also flag displaced band 0.3-3 MeV (v4: 0.1-3 MeV), stopped box extends in Λ beyond computed
  0.3-3 keV, exclusive γγ drawn as coverage though killed as discovery channel.
- T2_string_methods_B caption: "within 3-35%" is a median; single events −47%…+36%.
