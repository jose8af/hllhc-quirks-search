# Session log: arbiter Eloise, Phase 1 review cycle 2, 2026-11-13 20:45

- **20:45. Start.** Read `agents/arbiter.md` (Prompt Template) and `AGENT_RULES.md`, the study and phase `CLAUDE.md`,
  `FRAMING.md`, and the cycle-1 verdict (Dagmar, M1–M35). Head-node rules: read-only work and standard-library
  `python3` only; no sub-agents; no git.
- **Reviews read in full:**
  - physics, Dolores (1 A, 7 B, 9 C);
  - critical, Dorothea (3 A, 9 B, 10 C);
  - constructive, Edmund (1 A, 7 B, 11 C);
  - the fix report (Dmitri).
- **STRATEGY v2 parts read:** l.1-180, 268-367, 540-720, 950-962, 1032-1044, 1100-1375, 1598-1606 and 2015-2275. Also
  `prompt.md` l.60-100 (D1–D10) and `ORCHESTRATOR_STATE.md` l.18-22.
- **Fact checks in the source.**
  - `TT/acts/stage4/analysis/gen_d123.py`:
    - l.21-23: γ, V⁰, PV pairs and loopers come from the hard-scatter vertex; NI and DIF come from the hard scatter
      plus Poisson(200) minimum bias, with per-interaction rates × 200.
    - l.159-160 and l.172-179: PV pairs are pairs of prompt charged hard-scatter particles in the road.
    - l.253: the PV-pair rate is computed on the SM preselected events.
    - l.286-287: `per_PU200_event = 200 ×`.
  - `TT/acts/stage4/code/s4cp.py`:
    - l.13: the PV-pair gun takes its kinematics from one minimum-bias interaction.
    - l.110-113: the gun vertex is the drawn PV.
  - **Conclusions:**
    - The PV-pair / B4 overlap is real (P-B2).
    - The overlap extends to γ, V⁰ and loopers (my Case-5 addition to N8).
    - v1 already counted pile-up NI and DIF, placed at the PV (P-B1).
- **Arithmetic** (`python3 -I`, standard library):
  - Criterion (a) fail probability at the declared s_model:
    - F = 1.5, s_model 0.20: 0.043 at σ_stat = 0, 0.093 at σ_stat = 0.135;
    - F = 2, s_model 0.35: 0.048 at σ_stat = 0, 0.098 at σ_stat = 0.231;
    - for 12 tests, 1 − (1 − p)¹² = 0.41–0.71. K-N1 is confirmed.
  - Pile-up widths with σ_b := b₀: 0.45 / 0.61 / 1.30 / 2.47 at R08 / R09 / R11 / R14. P-B3, K-N4 and N-B2 are
    confirmed.
  - B4-c test-half statistics at 25.2 s per event: W(τ_h) +60.7 CPU-h (v2's 61 is confirmed), tt̄ 1ℓ ≈ +115 CPU-h,
    W(τ_ℓ) ≈ +210 CPU-h.
  - PV-pair pool share: 7.65×10⁷ × 11.5 ms = 244 CPU-h.
- **Contradictions resolved:**
  - M26: physics PARTIAL against critical RESOLVED. I side with physics, because the v1 code contradicts the premise.
  - M12: constructive PARTIAL against critical RESOLVED. I side with constructive: v2 l.1037-1038 re-measures P_geo
    and H on 2×10⁶ events at the T2 candidates, which count zero there.
  - M15: critical PARTIAL against constructive RESOLVED for r = 1. I side with critical, because N-B5 itself shows the
    defect.
- **Severity rulings:**
  - Physics A1 (rated A) against critical N6 (rated B): A, because the headline rests on H and the counts to test it
    exist.
  - Critical N1 (rated A) against constructive N-B5 (rated B): A, because the user is shown the wrong numbers and they
    change the expected outcome under [SD8].
- **20:45–. Verdict written:** `review/arbiter/STRATEGY_ARBITER_v2_eloise_2026-11-13_20-45.md`.
  - ITERATE: new findings A = 4 (N1–N4), B = 14 (N5–N18).
  - M1–M35: R 20, P 7, D 8 (all 8 accepted).
  - Gate A: five questions (Q1 C1 blinding; Q2 message and pool; Q3 D4 exception; Q4 budget, calendar and stop rule;
    Q5 D7 reading), plus eight defaults.
  - Net CPU of my rulings ≈ −96 CPU-h [E].
- **Nothing else written.** No git commands were run.
