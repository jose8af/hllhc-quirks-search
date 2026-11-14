# Session log — physics reviewer Dolores, Phase 1 review cycle 2 (2026-11-13 20:10)

- Read `agents/physics_reviewer.md` (prompt template followed), `outputs/FRAMING.md`, the cycle-1 physics review
  (Casimir), `outputs/FIX_REPORT_cycle1_dmitri.md`, and STRATEGY v2 (`STRATEGY_dmitri_2026-11-13_19-25.md`, l.1-2392,
  six consecutive chunks). Did not read methodology or conventions files.
- Opened to check specific claims: `outputs/digests/D4_v1_record_alfred.md` l.160-209 (v1 per-term counts);
  `src/strategy_budget.py` l.1-60, l.503-540 (section [12]); v1 `stage4/analysis/gen_d123.py` l.1-270 (definition of
  PV pairs and of the DIF/NI rates); `stage4/code/s4cp.py` grep (gun vertex placement).
- Arithmetic (python3 -I, standard library, scratchpad scripts chk.py, chk2.py, chk3.py):
  - floors: PV pairs κ = 16.18, floor 18.43; DIF 3.72 / 4.24; Z(νν) 4.56 / 5.19; allocation ratio M_PV/M_Z 13.90
    expected vs 13.91 planned; pool 600.8 CPU-h. All reproduce Table 4.4a.
  - one-bin CLs (n as test statistic, negative-binomial prior predictive): κ = 1/10/35 medians 3.00/10.77/27.78; fixed
    1.14κ: 4.06/8.16/14.28; κ = 35 true-λ medians 20.6/44.2/75.2/111.7. All reproduce §4.11 table.
  - exact coverage, s = 10, m redrawn: κ = 1, λ = 0.5: 0.9448; κ = 1, λ = 3: 0.9562; κ = 10, λ = 0.5: 0.9816. Reproduces
    the fixer's 0.945.
  - extrapolation widths with the document's own rule σ_b := b₀ (< 3 evaluable rungs per family): occupancy
    0.45/0.61/1.30/2.47 at R08/R09/R11/R14 vs text 0.20/0.45/1.23/2.44; single interaction 0.78/1.04/2.22 vs
    0.36/0.78/2.11. Script [12] hard-codes σ_b = 0.029 / 0.097.
  - log-normal width 2.44: q84 ×11.5, mean ×19.6.
  - σ_ln at m = 0: sd(ln λ) = 1.28 vs ½ ln(q84/q16) = 1.18 (two definitions in §4.11).
  - α_IC(200 GeV, 1 keV) = 0.0448; δ used 3.3/6.3/13.3 %, standard vector-current O(α) 3.4/6.6/13.9 %.
- Key finding from v1 code: PV pairs = pairs of prompt charged HS-vertex particles in the road (gen_d123 l.158-160,
  172-179, 253), i.e. the same tracks as B4's hard-scatter term; DIF and NI rates already include ×200 minimum-bias
  interactions (l.21-23, 286-287), gun at the drawn PV (s4cp l.4-5).
- Wrote `review/physics/STRATEGY_PHYSICS_REVIEW_v2_dolores_2026-11-13_20-10.md`. Cycle-1: 11 RESOLVED, 5 PARTIAL,
  1 DEFERRED (acceptable), 0 NOT RESOLVED. New: A = 1, B = 7, C = 9. Verdict: not yet approved.
