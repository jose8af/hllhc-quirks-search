# Session log: Ludmila, physics reviewer, review cycle 8 (STRATEGY v8)

- 05:40 Read role file `agents/physics_reviewer.md` (no methodology spec, no conventions read). Read FRAMING.md.
- Diffed `budget_stdout_v7.txt` vs `budget_stdout_v8.txt`: 23 added lines (v8 block) + 1 changed line (old l.373). No other value changed.
- Read script [9b] (l.480–960), the v8 block (l.853–891), `kap_nodif`, `ALPHA`, `pmf_pred`, `PU9`, `K_PIL`.
- Diffed STRATEGY v7 vs v8 (250 lines of diff): physics content of the diff confined to §0 pause paragraph, labels, Q2 table/grid, rule 1 S13 sentence, rider, Df-9 row. Defaults, CPU-h, calendar, expected-outcome numbers unchanged.
- Recomputation (scratch `rc.py`, `rc2.py`, `rc3.py` in the session scratchpad; script loaded via runpy, stdout suppressed):
  - empty-pilot row 75 [38–148] reproduced; hand: Σκ = 84.85 (DIF pilot κ 65.1 dominates), Σ medians 65.5, mean 91.6 incl. PU.
  - Z(νν) pilot row: m = 19 / 20 / 21 → 289 / 300 / 311; crossing at 20 confirmed.
  - (γ) rows as coded reproduced (104/180/255/294/331/448); hand Σ means 121/197/273/311/349/462.
  - (γ) on the pilot exposure (one common λ ~ Gamma(m_p+1)/2.3e6 applied to all SM N_trig ×1.663 + MJ): m_p = 2/6/10/12/13/15/21 → 113/189/264/300/318/353/462. Crossing at 12 pilot counts, not 13.
  - rejection grid as coded reproduced (×34 → 297, ×31 → 324; e⁻¹ ×69 → 301 (rounding of ≈69.4), ×235 → 300; 0.255: ×47 → 299, ×159 → 300).
  - grid on the pilot exposures the caption claims: remaining terms only → f_D=0 ×35 [×24], e⁻¹ ×75 / ×311 [×51 / ×209]; DIF also on its pilot (floor kept), conversions at pilot Z κ → f_D=0 ×46 [×31], 1/4 ×80/×172, e⁻¹ ×127 / none [×86 / none], 1/2 ×391 / none.
  - (c) credit rows at pilot exposures: 61 / 84 (non-DIF), 84 / 92 with DIF at its pilot floor; below 300 either way.
  - (α1) own-hit rows: (385+183)/0.2 + floors = 2.85e3 etc. reproduced by hand.
- v1 record `background.json` checked: γ 86/13/2 per 500 at R05/R06/R07 (2/13 conditional at R07 and at R09), DIF 81 (R05), 2/81 (R06), 1/81 (R07); photon rates 0.3786 / 0.2552. Consistent with script.
- Sweep of v8 for the family terms done (§0, §4.4, §11.7, Q2, rider, Df-9, §12.5).
- Finding W1 (B): exposures in the (γ) rows, the (c) rows and the rejection grid are pool, not pilot, while captions state rule 1 at pilot exposures; numbers shown to the user change (grid floor ×34 → ×46; (γ) pilot crossing 13 → 12).
- Wrote review `review/physics/STRATEGY_PHYSICS_REVIEW_v8_ludmila_2026-11-14_05-40.md`.
