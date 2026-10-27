# Review S1-R4 (Stage 1, theory track, round 4, narrow scope)

Reviewer: S1-R4 (fresh). Date: 2026-10-11. Scope: verify R3-B1 and the R3 C items, and check that the fix pass (v5.1) introduced no
new inconsistency. Settled physics not reopened. Read-only except this file and one LOG line. No new runs.

## Verdict: PASS (A = 0, B = 0, C = 3 remaining)

## 1 R3-B1
Grep of NEAR_MISS_IMPULSE.md, predictions.json, NUMERICS.md (and PROPOSED_CHANGES.md) for "2-5", "2–5", "B*-driven", "B* systematic":
- Every "+2-5 %" instance is a withdrawal statement or a historical quote: NEAR_MISS §5.5 l.386 ("withdrawn as a B* magnitude"), §13/§14
  response rows (l.821, l.838), predictions.json changelog (l.356 historical v5 line, l.365 R3-B1 line), `scale_free_v5.adopted_systematic`
  (quotes it as withdrawn), NUMERICS §14 row B1 (l.664). No live use as a B* magnitude.
- The remaining "B*-driven" hits are mechanism wording, not a magnitude: NEAR_MISS l.97 (B*-driven motion enters at even order),
  predictions.json l.377 ("mechanism ... CONJECTURE").
- Live wording is the requested one in §0 item 5, §5.5 "Systematic adopted", §9.3 "Impact on the headline law", §10 item 1, P-9,
  predictions `adopted_systematic`, PROPOSED_CHANGES items 2 and 6: unmeasured, unattributed, provisional, order ±5 % on Δs_B
  (population, sign expected positive) above ≈ 5 keV; tens of % in c per event for k_B ≳ 10; B* at the real oscillation numbers unmeasured.
- §5.5 also quotes the floor content of the direct B₀ runs (+0.0025/+0.0105/+0.039 vs +0.025/+0.017/+0.044 at 7/10/13 keV, 500 GeV) and
  the propagated errors ±0.4/1.0/2.0/2.8 % (500 GeV), ±0.4/0.8/4.2 % (1 TeV). Both match `r3_impact_err_out.txt`. The shifts
  +0.3/+1.3/+2.8/+4.5 % and +0.2/+0.4/+3.4 % match FIX2 `m*_implied_rel_change_of_Ds_vs_3keV` (0.0026/0.0128/0.0280/0.0446; 0.0022/0.0042/0.0337).
- The fix is text only, as asked. **R3-B1: resolved.**

## 2 B* evidence vs FIX2.json
FIX2 `N1/m*/on_minus_off_s*.kB_ge5`, second entry (Δc(4)):
| setting | 500 GeV | 1 TeV | quoted |
|---|---|---|---|
| s = 1 | +0.01362 ± 0.00392 | +0.01254 ± 0.00383 | +0.0136 ± 0.0039 / +0.0125 ± 0.0038 ✓ |
| s = 1/3 | +0.00554 ± 0.00287 | +0.00021 ± 0.00345 | +0.0055 ± 0.0029 / +0.0002 ± 0.0035 ✓ |
| s = 1/9 | +0.00087 | −0.00033 | +0.0009 / −0.0003 ✓ ("≈ 0") |
B*-off k_B ≥ 5 Δc(4) at s = 1: −0.00033 / +0.00134, quoted "−0.0003/+0.0013" ✓. The numbers appear in §9.3 table and (i), NUMERICS §13.1 reading 1,
predictions `v4_FIX1.verdict`. Note: the "1/9 scale" values are ≈ 0 within errors (the 500 GeV point is 0.4 σ), consistent with the wording.

## 3 R3 C items
- C1 floor amplitude: applied (§9.3 (ii) "Amplitude" and "Attributed ... ESTIMATE, not demonstrated"; NUMERICS §13.1 reading 3 "scaling, not magnitude", 3.8-3.9×).
- C2 B* part wording: applied (500 GeV half, 1 TeV ≈ 20 %; floor-free Δc(4) numbers as main evidence; mixed metrics removed).
- C3 M2b +11 % → +18 %: applied (§9.3, NUMERICS l.595; 0.16 %/1.7 %/18 %).
- C4 N-independence wording: applied ("N-independent within errors", values with 1 TeV 0.0082 ± 0.0027; "mild rise" at 500 GeV).
- C5 §12 stale rows: applied (Constr. B3 row now "not a clean test"; Crit. A1 row adds the §5.5 systematic).
- C6 §11 title: applied (§11 (b) carries the adopted title).
- C7 predictions.json: applied (3 keV "FAILED/open" flagged superseded l.53-54; v3_FU1 note_v5 points to v4_FIX1.verdict; meta.date 2026-10-11; impact errors corrected). Not changed: older changelog entries keep dates 2026-10-10 (correct, historical).
- C8 NUMERICS pointers: **partly applied.** §12.6 A1 row flagged "[superseded → §13]" (l.534) and l.404/l.497 point to §13. Still stale: §0 item 4 (l.18) "[superseded → §11 FU1, §12 A1 ... B*-correlated excess]" and §11 FU1 verdict (l.403) "[partly withdrawn → §12 A1 ...]" do not point to §13. The §14 row claims "§4.2 and §11 FU1 pointers now point to §13". (Remaining C-a.)
- C9 PROPOSED_CHANGES: applied (item 2 v5.1 caveats; item 6 "P1 scope decided: option (b)"; synthesis P1 row added as item 15; item 16 for NOVELTY_AUDIT).
- C10 direct B₀ runs one-solver: applied (§5.5 "one solver").

## 4 Consistency after the fix pass
- Scope of the headline law (verified ≈ 1 keV: c to 1-2 %, C to 0.1-0.2; 3 keV at B₀/2 and B₀/4 for k_B < 5; consistent at 5 keV, ≲ 1 % on Δs_B(5)/Δs_B(3), floor-free; ±5 % unattributed above) is the same in §5.5 "Scope", §8 P-9/P-14, §10 item 1 and predictions `scale_free_v5.scope` + `adopted_systematic`. §0 item 5 states the 1 keV verification and the unmeasured systematic but not "consistent to 5 keV" explicitly (C-b, harmless).
- Floor attribution tagged ESTIMATE everywhere checked (§0 item 6 does not discuss it; §5.5, §9.3 (ii), §10, P-14, predictions `v4_FIX1`, PROPOSED_CHANGES 2/6).
- Spot-check of 5 numbers against JSON, all OK: C = 0.43/1.23/1.62 (P-9 vs predictions); implied shifts +0.3/+1.3/+2.8/+4.5 % (FIX2); propagated errors ±0.4/1.0/2.0/2.8 % (r3 output); on − off Δc(4) k_B ≥ 5 s = 1 (FIX2); predicted floor +0.039 vs measured +0.044 at 13 keV (r3 table, quoted in §5.5, §14 and predictions).
- Internal check of the new wording: "≲ 1 % at 5-7 keV" vs the systematic "order ±5 %" are compatible (±5 % is stated for the population above ≈ 5 keV and covers the 10-13 keV region). No contradiction found.

## 5 PROPOSED_CHANGES.md items 2, 6, 15, 16
Present and coherent. Item 2 and 6 carry the v5.1 caveats (two-part excess, ESTIMATE floor, unmeasured ±5 % above ≈ 5 keV). Item 15 gives the option-(b) title identical to §11/line 1. Item 16 flags the Knapen Eq.9 recomputation (6.5×10⁻⁶; ×1 m = 6.5 µm vs causal 4.5 µm) and the title for E3/orchestrator. Item 3 (the "open weak-field/high-Λ systematic") is still true but its wording is older; fine.

## Remaining C items
- C-a: NUMERICS l.18 (§0 item 4) and l.403 (§11 FU1 verdict) still point to §12 A1 instead of §13; §14 row C8 overstates.
- C-b: NEAR_MISS §0 item 5 could add "consistent at 5 keV" to match §5.5/P-9.
- C-c: NEAR_MISS §8 header says "predictions.json (v4)"; the file is v5.1.
