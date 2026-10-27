# Stage 5 final figures - critical review R2 (fresh reviewer, 2026-10-16)

Scope: verify R1 B1-B6 and the fixed C items. Read the PNGs D2 (F200), D4, D5 (F1500), D7, D8 (RA_F1000, RA_S500), D9, D11 myself.

## R1 B findings
- B1 RESOLVED. The m_Q line is gone. The only reference line is "2 m_Q (M_QQ threshold)", on a bin edge. Text reads "pair-mass proxy, >= 2m_Q" and "low cluster: PU BTL hits". S500 now spans 0-3000 GeV with no mass in the overflow. F1000 spans 0-4800 GeV. Independent recomputation from signal_obs_a2.npz (R_A rung 4, f_CKF < 0.2, first candidate per event): 1051 events, 850 with M_est defined, median M_est/m_Q = 2.256, 3 events in 1.3-1.7 m_Q, 19.06 % below 0.5 m_Q. This matches FIGURES_FINAL §D8.
- B2 RESOLVED. The dotted "MET road of the fake trial (+-0.15 rad)" is drawn in the fake colour. trials.phimet[28] = 2.29739 and delta95 = 0.15 in B1_00201.npz match the sidecar. The sidecar gives delta-phi = 0.0172 against the signal MET at 2.3146. The caveat text is correct.
- B3 RESOLVED. D2, D4 axes read "R04 N_IP2 >= 7" and so on.
- B4 RESOLVED. The D9 text block sits inside the frame, right-aligned, with no overprint.
- B5 RESOLVED. D4 diamonds are drawn only for rungs >= R08, and the text states "factorisation == B1 direct at R01-R07 (not drawn)".
- B6 RESOLVED. EXTERNAL_BOUNDS.md l.7 points to the final D7. The only "placeholder" left is the explicit "superseded" note. The PRL claim is now "arXiv e-print".

## Fixed C
- C1 RESOLVED. D5 F1500 has a tight frame with no overlap.
- C3 RESOLVED. D4 now reads "trend significant: yes".
- C5 RESOLVED. D7 uses "Farina-Low HSCP recast", "monojet recast" and "Evans-Luty out-of-time recast". There is no CMS wording.
- C2, C6, C8 are documentation items, noted as done in FIX_STAGE5_R1.md. C4, C7, C9 were left as accepted or pending.

## Regression checks
- Labels are "Private work (simulation)" and "sqrt(s) = 14 TeV, PU 200, 3 ab^-1" on all PNGs viewed. There is no experiment name or logo, and the sidecars have 0 stamps.
- No WP or discovery is implied. D5 and D7 say "no WP / s8 fallback", "no expected exclusion" and "no 5 sigma".
- D7 cell values match R1: 37.6 at E200 1.5 keV and 39.1 at 2 keV.
- 31 regenerated PNGs are newer than R1. The truth figures and D1/D10 are untouched (timestamps 13:04). index.json is complete, with all 11 ids.

## Category A
None.

## Category B
None.

## Category C (optional)
- C-1 FIGURES_FINAL §D8 calls the pooled N = 850 "exactly what the figure plots". The figure shows only 3-4 Lambda values per mass (N = 8-43 per curve; the sidecar sums to 414 + 95 undefined). 850 is the pooled value over all 40 A2 points. The numbers are correct, so reword it as "pooled over all points".
- C-2 D9: the legend fills the top third of the panel and the A2 arrows are small. This is cosmetic.
- C-3 D4: the end-state line has a kink at R09-R10, from the closure/extrapolation switch. A one-line note would help.

## Verdict
**PASS** (0 A, 0 B, 3 C).
