# Fix S3-R2: Stage 3, round 2 (C001 quirks theory track)

Fixer, 2026-10-13. Input: `review/REVIEW_S3_R2.md` (PASS; 0 A, 1 B, 8 C) and `review/r2_checks/`.
Text, tables and figure cosmetics only. No new production. CPU ≈ 0.005 CPU-h (two bookkeeping scripts, 11 s + 2 s;
figure redraws from the delivered JSONs).

New scripts (saved outputs only):
- `scripts/fix_r2_bstar_context.py` → `results/FIX_R2_bstar_context.json`: paired on − off per bin and pooled; B* off
  against the full E 500 + E 1000 production; per-event (c_on − c_off)/c_ev quantiles; on-arm control in c; floor
  allowance at the subsample ε⊥. 20 000 bootstrap resamples.
- `scripts/fix_r2_notes.py` → `results/FIX_R2_notes.json`: sep_IT slope errors; list of the c06 model-zero events.

**Regression.** `P1.json`, `P2.json` and `P2_points.json` are byte-identical before and after (md5 b25f18ed…, df1b7c68…,
1eb173be…). Figures were redrawn with `p1_results.py --figures-only` (new option, which reads P1.json and does not
write it) and `p2_results.py --figures-only`. `make_docs.py` was rerun. The diff of the generated blocks shows only the
intended changes: the §0 B*-off verdict, the slope errors and two notes in the README auto block. SAMPLES.md is
unchanged.

| item | resolution | where |
|---|---|---|
| **B-1** B*-off reading | **RESOLVED.** "Removes the bulk in every bin" is withdrawn. Text quotes pooled paired on − off: +27.6 ± 12.1 % for k_B ≥ 6 (2.3σ), +8.6 ± 4.2 % for all 160 (2.1σ); the per-bin values are 0.8-1.8σ. k_B < 4 now reads "consistent with removal (+4.1 ± 2.2 %, 1.8σ)". k_B 4-6 is stated to show no excess to remove (on +1.7 ± 4.1, off +2.7 ± 1.3 %). Added the same-event B*-on row next to the B*-off row, plus the paired, production, per-event and floor rows. Strongest support, recomputed by script: B* off +1.8 ± 0.7 % (160) vs full production +9.7 ± 1.3 % (600), difference +8.0 ± 1.4 %, **5.5σ**; 5.7σ against the 440 production events not in the sample. Added the per-event-spread sentence: k_B ≥ 10 median +8 ± 19 %, IQR −30 … +112 % of c. Attribution remains ESTIMATE everywhere. P-11 has no B*-off statement (checked; nothing to change). | VALIDATION §0 preface, §0 auto row (make_docs), §8 item 5; README headline 4; PROPOSED_CHANGES §1 table and attribution, P-10; DECISIONS_PENDING U-1 context |
| C-1 control in c | RESOLVED. 5/160 events have \|c_on − c_prod\| > 0.01, max 0.091 in c (= max 2.3 % in Δs_B), all at Δs_B 0.027-0.11 µm. The bin medians move by ≤ 2.2 points. | VALIDATION §8 item 5; `FIX_R2_bstar_context.json` `control_c` |
| C-2 floor at subsample ε⊥ | RESOLVED. k_B ≥ 10: 6.9-18.2 % (full population 8.8-23 %). Given per bin in the table. | VALIDATION §8 item 5 (floor bullet and table); README; PROPOSED_CHANGES |
| C-3 sep_IT slope errors | RESOLVED. ± 0.017-0.044 per point (toys on the per-Λ bootstrap errors); F_m1000 −1.985 ± 0.023 (reviewer's event bootstrap: ± 0.025). The central slopes are P2.json's, unchanged. | README headline 6 and auto block (make_docs); HANDOVER §5.3; `FIX_R2_notes.json` |
| C-4 robust totals | RESOLVED. 198/243 robust components are < 2× sampling sd (recounted; the count is now computed in make_docs). The totals are stated as noise-limited upper bounds, and symmetrisation and the < 2σ treatment are deferred to Stage 4. | VALIDATION §9 item 12; HANDOVER §5 item 4; README headline 6 and auto block |
| C-5 interpolated edges | RESOLVED. Stated as fit (stat) error only (0.40-0.58 keV); Stage 4 is to add the neighbouring-mass systematic. | VALIDATION §9 item 8; HANDOVER §5.3; README auto block |
| C-6 c06 model zero | RESOLVED. 4 events listed: F_m200/L5 r54998, F_m1000/L0.45 r30405, F_m1500/L3 r735, S_m500/L5 r22057; none at 7-10 keV. The count is 4; the "5" in FIX_S3_R1.md was a miscount. | VALIDATION §9 item 11; HANDOVER §5 item 4; `FIX_R2_notes.json` |
| C-7 figure cosmetics | RESOLVED. `p2_observables.png`: hspace 0.42, so the labels no longer overlap. `p1_v2b_revisit.png`: the identity-check dots moved to their own right panel with their own x label; the README caption is updated. | `scripts/p1_results.py`, `scripts/p2_results.py`, figures/ |
| C-8 one ACTS event per physics event | RESOLVED. Marked as a requirement not yet tested: all V8 variants still inject 10 events into one ACTS event. | HANDOVER §4 action 3; VALIDATION §5 (V8) |

Also fixed in passing: the B*-on row errors in the VALIDATION §8 table had been typed from an earlier bootstrap. They now
match `FIX_bstar_off.json`; the central values are unchanged.

Not done: the review asked for no further work, and the D12/O-1 floor test, symmetrisation and the c06 edge-case
investigation remain deferred as listed.
