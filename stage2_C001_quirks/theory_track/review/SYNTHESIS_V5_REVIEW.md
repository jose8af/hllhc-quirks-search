# Review SYN5-review: synthesis v5 (fresh verification reviewer, 2026-10-11)

Scope: `outputs/THEORY_GAPS_SYNTHESIS.md` (v5) vs `_v4.md` (diff, 230 lines), against `analytic/PROPOSED_CHANGES.md`, NEAR_MISS_IMPULSE v5.1 (§0, §7, §8, §10, §11), `predictions.json`, NOVELTY_AUDIT (§0, §4, erratum), T2 erratum 2. JFC classes: A wrong result, B misstatement / claim beyond evidence, C style.

**Verdict: PASS. A = 0, B = 0, C = 3.**

## Check 1: applied items match the source
- c 0.104 vs blind 0.105 +- 0.002; B exponent 1 - c (0.896; B^0.914 vs 0.911 +- 0.003); Lambda exponent -2 + 2c (-1.77/-1.79/-1.83/-1.86 at 0.6/1/3/10 keV): equal to P-10..P-13, §5.3.
- Delta s_B ~ eps_B[ln(1/eps_B)+C], C = 0.43/1.23/1.62; measured 1.13 +- 0.18 / 1.15 (k_B < 6.5); eps_B = 2.25e-4 (B/3.81 T)(keV/Lambda)^2; c falls 0.116 -> 0.070; literal constant-c form gives 0.944: all equal to NEAR_MISS §5.2-5.3, P-9.
- Tags and scope: verified near 1 keV, 3 keV at B0/2 (all) and B0/4 (k_B < 5), consistent to 5 keV, unattributed +-5 % above (header, S-3, §7 item 12): matches §0 item 5, §10 item 1. Floor part of the 3 keV excess is ESTIMATE; B* measured not derived; yo-yo accuracy 1-4 % / 10-35 %.
- Failed gamma* = 2 prediction (0.50 vs 0.75 +- 0.08, 10-event subset 0.96 +- 0.10, ~3 sigma), Kang-Luty ratios 1.04/1.21/1.68, eta ratios 0.97/0.84/0.50: match P-17, §4.4 table.
- Even-crossing erratum (T2 erratum 2, synthesis S-3, S-19, X-13, §6): 2.6e-3/3e-4/2.7e-5 vs max_boost, b_even = 0 at first order, <~ 1e-3 b_odd, floor above 2-3 keV, "from 3 keV" kept as upper bound; consistent with NEAR_MISS §6.1 and the T2 box. The 1/Lambda conclusion keeps its direction (1e-3 b_odd = 3.5 nm > 1/Lambda at 1 keV, < at 3 keV).
- S_Bscan R(1e-3), R(1e-4), B/1000 = 1.83 flagged unreliable; blind 1.073/1.147/1.320/1.460 vs predicted 1.072/1.144/1.311/1.455 equal P-13/NUMERICS §4.2.
- P1 title, option-(b) scope, MS as measured floor with Highland credited, novelty without MS: equal to NEAR_MISS §11. Knapen Eq. 9 = v_cm/v^2; 1e-3 bound credited to §II text after Eq. 9 (Fig. 3 numbers 0.4e-3/0.1e-3): equal to NOVELTY_AUDIT erratum. Credit-sentence numbers 1-5, 9, 10 map correctly. NG validity 0 / 3-8 % / 10-25 % and b_odd*Lambda = 1 at ~26 keV: equal to §7, P-18. FASER HEPData numbers equal §10.5 (Lambda <~ 1.5 keV propagated to §0.2, S-8, §4.5, §5 P6, Box A).

## Check 2: items not or partly applied
- #8 (S_Bscan.py header): not applied, valid (never edit code; floor note carried in X-3, §3.1 row 12, §9). #11 (report .tex): outside the write list, valid. #16: see C1.

## Check 3: stale statements (grep of v5)
- "fitted, not derived", "heuristic", "WORTH A CHECK (analytic", "1 + 0.10 ln", "0.08-0.11", "10-30 %", FASER "<~ 2 keV", "b ~ 16-30 A": every remaining hit is either in a quoted "v4 said" clause, in the §10.6 change table, in a flagged-superseded v4 history line (§0 v4 list, §10.1 B-1, §10.2/10.3 R3-B1, "Remaining after R3"), or in the killed-ideas rows. No unqualified current use. "b_even" is always qualified. Other "Lambda <~ 2 keV" hits (B-only route, eps) are unrelated to FASER.

## Check 4: diff scope
- All 230 diff lines map to an item, to the listed fixer extras, or to header/§10.6. §10.1-§10.5 text is intact (only italic "(v5: superseded...)" flags appended). No deletions of content other than replaced wording.

## Check 5: extras
- S-3 charge test: 2[1 - ln2/(ln(1/eps_B)+C)] = 1.856 -> "1.86", deviation 7 %, ratio 0.999 +- 0.001 (P-24): correct. S-17: 1.86^(1/1.9) = 1.386 -> 1.39, "~1.4 unchanged": correct.
- Lambda-exponent pointer: T3 median -1.9 kept, with E2 mean -1.81 and derived -1.79..-1.86 in the same bullet; the difference is correctly described as within layer-sampling scatter in §10.6 (NEAR_MISS §5.4). Reasonable, not reopened.

## Check 6: scope
- §4 proposals unchanged in content (only X-2/NG-validity/charge-factor numbers). §8 row 4b states Stages 2-6 are active (matches README status) and does not alter the Phase-1/2 proposals. No file outside theory_track modified (`find` newer than 2026-10-11 outside TT: none except .DS_Store; phase1_strategy, phase2_exploration, research mtimes 2026-10-07).

## C items
- C1: §10.6 #16 and PROPOSED_CHANGES #16 status say the NOVELTY_AUDIT title/scope change "not applied, flag to E3". E3 applied it afterwards (audit header line 3 and erratum, LOG 2026-10-11 E3). Update the two status cells.
- C2: X-3 line "c ~ 0.10-0.12" (S's measured range) sits next to the derived 0.104; add "(measured range, S)" to avoid reading it as the current value. Same for "c ~ 0.10" in R1 row (already followed by "derived 0.104").
- C3: Knapen comparison "6.5e-6 per oscillation x 1 m ~ 6.5 um" mixes a per-oscillation angle with a lever arm; it is as given in PROPOSED #16, but a reader may want "order-of-magnitude" stated. Also S_Bscan.py has no header warning (#8); optional one-line comment if the user allows a code edit.
