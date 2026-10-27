# External bounds for the D7 overlay (FIGURE_PLAN item 6), 2026-10-16

**Files.**
- `stage5/external_bounds.json` holds the data.
- `stage5/build_external_bounds.py` writes it. The script uses only the standard library and is run with `python3 -I`.
- `make_figures.py` reads it in `overlay_external()` and draws the result on D7.
- The output figure is the final `figures/final/D7_exclusion_map.{pdf,png,json}` (real Stage-4 run C12FC_v1, no stamp). The sidecar lists the sha256 of `external_bounds.json`. (The old `figures/placeholder/` version is superseded.)
- In the D7 tag the recast curves are named without an experiment word: "Farina-Low HSCP recast", "monojet recast", "Evans-Luty out-of-time recast" (display names only; the labels in `external_bounds.json` are unchanged).

**Rebuild.**
```
python3 -I stage5/build_external_bounds.py --hepdata-t2 <t2.csv> --faser-fig5 <summary_limits_gray.pdf>
```
The inputs are not stored in TT. Their URLs and sha256 are recorded in `inputs` in the JSON.
- HEPData t2 csv: `https://www.hepdata.net/download/table/ins3184325/Exclusion%20Contours/1/csv`
- FASER Fig. 5: the arXiv e-print `2607.26195`, file `figs/summary_limits_gray.pdf`
The build downloads were kept in the session scratchpad (`.../scratchpad/extbounds/`) and were treated as untrusted data.

## Conventions and our model
- **Our model.** E = (1,1)₋₁ vector-like Dirac fermion with N_IC = 2. Ẽ is the scalar with the same SM charges (BRIEF.md).
- **Λ convention.** We use string tension σ = Λ². FASER writes the force as Λ². Farina–Low take T = Λ² (they note T ≈ 1.6 Λ² in QCD and "take T = Λ² for simplicity"). D0 uses L ≈ m_Q/Λ² (Eq. 1). So no conversion is needed. D0 is the one case where the agreement is only up to O(1), because it gives only this length estimate.
- **Units and point order.** Points are `[m_GeV, lam_keV]`.
- **Tags.**
  - VERIFIED means the number comes from a tabulated source: HEPData, or a table or quoted value in the paper.
  - ESTIMATE means the number was digitised from a figure.

## Schema `external_bounds v1`
`curves[id]` has these fields:
- `label`
- `applies_to`: `E` and/or `Etilde`
- `model`
- `model_match`: `{E, Etilde}`
- `source`
- `method`
- `uncertainty_tag`
- `kind`
- `points`
- `draw`
- `notes`
- `artefact_edges` (optional)
- `no_limit_at_lam_keV` (optional)

`kind` takes one of three values:
- `upper_mass_edge`: at each Λ, masses below the curve are excluded.
- `polygon`: a closed region; the inside is excluded. Edges listed in `artefact_edges` are plot-frame edges, not limits.
- `benchmarks`: isolated limit points. The source gives no curve between them.

How D7 uses it:
- D7 draws the curves that have `draw: true` and `"E"` in `applies_to`. Regions are hatched.
- The axis range is never changed.
- Curves that fall entirely outside the plotted range are listed in the figure's tag block instead of being drawn.
- The top-level `cross_checks` array holds the table below.

## Curves

| id | source | model / match to E (Ẽ) | method, tag | content |
|---|---|---|---|---|
| `FASER_obs` (drawn), `FASER_exp`, `FASER_exp_p1s`, `FASER_exp_m1s` | FASER, arXiv:2607.26195 (e-print; journal reference not checked). HEPData ins3184325, table "Exclusion Contours", doi:10.17182/hepdata.181308.v1/t2 | (1,1,−1) fermion, N_IC = 2, 13.6 TeV, 186.3 fb⁻¹. **Exact match to E.** Ẽ is **not directly comparable**: this is a fermion limit and FASER gives no scalar result. | HEPData, VERIFIED | 19 Λ values from 0.3 to 105 keV. Observed m_max = 57.3 / 72.5 / 106 / 113 / 149.1 / 162.6 / 172 / 175 / 179 / 175 / 173 / 157.8 / 139.7 / 117.0 / 104.2 / 96.0 / 77 / 71 / 66 GeV at Λ = 0.3 / 0.5 / 0.75 / 1 / 1.7 / 3 / 5 / 7.5 / 10 / 17 / 30 / 50 / 65 / 75 / 85 / 90 / 95 / 100 / 105 keV |
| `D0_2010` | D0, arXiv:1008.3547, PRL 105 (2010) 211803. Abstract, Eq. 1, Table I | Charged (\|Q\| = 1), colourless fermion, N = 2 (3, 5 also given), p p̄ at 1.96 TeV, 2.4 fb⁻¹. **Probable match to E.** Charge, colour, spin and N match. The Letter does not state the SU(2)_L representation or hypercharge (it uses a modified Kang–Luty MadGraph). FASER overlays it on its (1,1,−1) plane. Ẽ: not comparable. | paper text + Table I, VERIFIED | Region m = 60 to 107 GeV, Λ = 10 keV to 1 MeV. The limit does not depend on Λ. The Λ edges are the scenario range of the paper. The edge at 60 GeV is the lowest simulated mass. |
| `FarinaLow_E_TabII` | Farina & Low, arXiv:1703.00912, Table II | Fermion (1,1)₋₁, N_c = 2, T = Λ², 13 TeV, CMS HSCP 12.9 fb⁻¹ + ATLAS monojet. **Exact match to E.** | paper table, VERIFIED | 650 GeV at Λ = 1 eV, 150 GeV at 100 eV, no limit ("–") at 1 keV |
| `FarinaLow_Etilde_TabII` | same, Table II | Scalar (1,1)₋₁, N_c = 2. **Exact match to Ẽ.** | paper table, VERIFIED | 350 GeV at 1 eV, 60 GeV at 100 eV, no limit at 1 keV |
| `FarinaLow_HSCP_viaFASER` | FASER Fig. 5, gray region "Reinterpreted CMS HSCP", which FASER cites to Farina–Low | As FASER applies it to E | vector extraction, ESTIMATE | Upper edge running from 225 eV (m ≈ 3 GeV) through 100 eV (153 GeV) to 2.4 eV (685 GeV). The part below 60 eV and above 200 GeV is present in the PDF path but clipped from the published figure. |
| `FarinaLow_monojet_viaFASER` | FASER Fig. 5, "Reinterpreted ATLAS/CMS monojet" | As FASER applies it; **disagrees with FL Table II** (see the cross-checks) | vector extraction, ESTIMATE | m < 56 to 57 GeV for Λ from 0.16 keV to 1.7 MeV |
| `CMS_OoT_EvansLuty_viaFASER` | FASER Fig. 5, "Reinterpreted CMS OoT" (cites CMS 1801.00359; this is the Evans–Luty recast, 1811.08903) | As FASER applies it. The recast's own model was **not re-checked here**. | vector extraction, ESTIMATE | Polygon covering m ≈ 88 to 202 GeV for Λ ≤ 0.15 keV. Not requested in item 6; kept because FASER shows it as an existing limit. |
| `D0_viaFASER` (not drawn) | FASER Fig. 5, "DØ" box | as for D0 | vector extraction, ESTIMATE | Used only as a cross-check |

**Farina–Low Fig. 3 (`pfin.pdf`) is not used.** It is for the coloured (3,1)₂/₃ triplet, which is not comparable to E. For uncoloured quirks, Farina–Low publish only the Table II benchmarks.

**How the vector extraction works.** FASER Fig. 5 is a vector PDF made by matplotlib. The script decompresses its content stream and parses the path operators. Calibration uses the figure's own major tick marks, which are read from the same stream:
- x axis: m = 60 to 200 GeV, linear.
- y axis: Λ = 10² to 10⁶ eV, logarithmic.

The closure test is FASER's own observed and expected curves in the same PDF. They reproduce HEPData t2 with |Δm| < 0.005 GeV and |Δ ln Λ| < 10⁻⁶. So the extraction error is negligible. What remains is the accuracy of FASER's drawing and FASER's choices in rendering other papers' limits.

## Cross-checks (all are also in `cross_checks` in the JSON)

| check | expected | found | verdict |
|---|---|---|---|
| FASER Fig. 5 path vs HEPData t2 (observed and expected) | identical | max \|Δm\| = 0.000 GeV, \|Δ ln Λ\| = 7.6e−7 | PASS |
| FASER text: "Masses up to 179 GeV are excluded for Λ = 10 keV" | 179 | 179.0 (t2) | PASS |
| FASER abstract: 300 eV < Λ < 100 keV | 0.3 to 100 keV | t2 covers 0.3 to 105 keV | PASS |
| Earlier TT use (theory_signal_model.md l.103 and l.483, code/T1_figure.py): 57/72/113/149/163/179/173/71 GeV | same | max \|Δ\| = 0.5 GeV (rounding) | PASS |
| D0 abstract: 107 GeV (N = 2) vs the point where σ_N=2 = σ_95 in Table I (16 vs 13 fb at 100 GeV, 9.3 vs 14 fb at 120 GeV, log-linear) | 107 | 106.7 | PASS |
| D0 box as drawn by FASER vs the D0 text | 107 GeV; 10 to 1000 keV | 107.14 GeV; 10.13 to 991 keV | PASS |
| FL Table II: E, 150 GeV at 100 eV vs FASER's HSCP edge at 100 eV | 150 | 152.7 | PASS (within 2 %) |
| FL Table II: E, 650 GeV at 1 eV vs FASER's HSCP edge | 650 at 1 eV | 685 at 2.4 eV, which is still rising toward lower Λ | **DISCREPANT** (about 5 % or more; not resolved) |
| FL Table II: E, no limit at 1 keV vs FASER's monojet region | none | m < 55.9 GeV | **DISCREPANT**. FL give only 30 GeV even for N = 5. FASER probably used a different source or a rescaling. |

## Caveats
1. **On the D7 grid, only FASER is visible.** The final D7 grid (C12FC_v1, A2 E points) has masses 200, 500, 1000 and 1500 GeV. Its cell edges put the frame at m ≈ 126 to 1840 GeV and Λ ≈ 0.39 to 6.5 keV. Every existing limit sits at m ≤ 179 GeV, so only the FASER edge enters the plot, at the left frame for Λ ≳ 1.25 keV. D0 (Λ ≥ 10 keV), FL (Λ ≤ 0.1 keV), HSCP, monojet and OoT are all outside the range. D7 lists them in its tag block rather than widening the axes.

   The "full" grid (200 to 1500 GeV in 100 GeV steps, Λ = 0.3 to 30 keV) has its left frame at 163 GeV. On that grid FASER would show only for Λ ≈ 3 to 35 keV, and D0 would stay outside (m < 107 GeV). In short, the HL-LHC reach lies far above every existing limit, and the overlay mainly shows that gap.
2. **D0's SU(2)_L assignment is not stated.** The match to E is "probable", not exact. D0 also excludes only down to its lowest simulated mass of 60 GeV.
3. **Farina–Low regions as drawn by FASER are FASER's rendering, not Farina–Low's own numbers.** FASER's HSCP edge agrees with FL Table II at 100 eV but not at 1 eV. FASER's monojet region contradicts FL Table II at 1 keV. The `*_viaFASER` curves are therefore tagged ESTIMATE, with these discrepancies recorded. The FL Table II benchmarks are the VERIFIED Farina–Low numbers.
4. **Ẽ has only one usable external bound:** the FL Table II scalar benchmarks, at Λ ≤ 0.1 keV. FASER and D0 are fermion limits, and converting them would need a scalar acceptance. FASER's t1 table of σ_fid^eff limits could in principle be used with a Ẽ prediction of σ_fid^eff, but that is not done here. D7 is drawn for E only.
5. **FASER t2 gives only the upper mass edge.** Following FASER's figure, the overlay hatches from the left frame up to that edge.
