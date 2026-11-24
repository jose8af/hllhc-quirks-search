# P3-A — FINAL classification of the pilot and the rule-1 counts it gives (inputs to decision point 2)

Aurora (Fable 5.2, executor, work package p3-a), 2026-11-24. Plan written before any code or job:
`phase3_selection/logs/executor_aurora_2026-11-24_10-16.md`. `STR`, `ADD`, `EXP`, `COM` as in `PHASE3_BRIEF.md`;
`TOV`, `ING`, `CEC`, `BJO` as in EXP §0.2; `NIL` = `phase2_exploration/review/RULE1_SUBSET_REVIEW_nils_2026-11-23.md`;
`YLV` = `phase2_exploration/review/RULE1_B50_REVIEW_ylva_2026-11-23.md`.
Result files (all under `phase3_selection/outputs/p3a/`): `C` = `p3a_counts.json`, `T` = `p3a_dp2_inputs.json`
(every number of this document that another work package may use), `D` = `p3a_rule1_dryrun.json`,
`I` = `p3a_indep_summary.json`, `W` = `p3a_witness_check.json`, `A` = `p3a_attrib.json`, `X` = `p3a_xcheck.json`;
generated tables `p3a_tables.md` (copied in the appendix, numbered T1–T12).
Tags: VERIFIED = computed in this session from the files named; ESTIMATE; UNVERIFIED = transcribed.
**No signal file was opened. No efficiency was formed. Nothing here is the binding reading and nothing here chooses a
convention: where the frozen text leaves a choice open, the count is given under every reading.**

## v2 (Ulf, Opus 5.5, fixer, review round 1), 2026-11-24: change table v1 → v2

v2 answers the critical review `review/critical/P3A_CRITICAL_REVIEW_sindre_2026-11-24_16-50.md` (A-1, B-1…B-4,
C-1…C-8). v1 (`P3A_PILOT_FINAL_aurora_2026-11-24.md`) is unchanged. **Text only:** no job was run and no count was
recomputed (Sindre's independent recount reproduced all 480 count tables). The only figures added that are not in
v1 are (a) the s = 3 confirmed fractions under reading F, ratios of the stored `confirmed` / `counted` fields of
`I`; (b) numbers quoted from the review and labelled as Sindre's. Code, JSON and the appendix tables T1–T12 are
unchanged. Every changed passage is listed below (v1 text → v2 text; line breaks folded).

| # | finding | where | v1 | v2 |
|---|---|---|---|---|
| 1 | B-3 | §0 table, R14-type row | \| R14 = R17 = R20 = FB(4) \| 969 / 846 \| | \| R14 = R17 = R20 = FB(4) (s = 3; re-derived in part ᵃ) \| 969 / 846 \| |
| 2 | B-3 | §0 table, FB(3)–FB(1) row | \| FB(3) / FB(2) / FB(1) \| 2,212 | \| FB(3) / FB(2) / FB(1) (s = 3; re-derived in part ᵃ) \| 2,212 |
| 3 | B-3, C-7 | §0 table, FB(0) row | \| FB(0) (R04 width: 75 mm; window only) \| | \| FB(0) (R04 width: 75 mm; window only) (s = 3; re-derived in part ᵃ; OWN ᵇ) \| |
| 4 | B-3, C-7 | §0, footnotes under the table (new) | M(Z) = 993,885.9. R06–R07: | ᵃ **s = 3 coverage (review B-3):** share of the counted events confirmed by Nils's independent search (every 2nd file; `I`), reading S / F: R08 (R14-type, FB(4)) 70.4 / 76.3 %; R07 (FB(3)) 74.5 / 79.5 %; R06 (FB(2)) 77.2 / 81.2 %; R05 (FB(1)) 77.7 / 81.1 %; R04 (FB(0)) 77.3 / 80.4 % [VERIFIED: ratios `confirmed`/`counted` of `I`]. Rows that need k_IP ≥ 4 have **no independent search** (98 of the 139 not found at R08); in the witness check (39 files) the stored witness gives k ≤ 5 for 1,743 of 2,307 s = 3 rows, for the rest no witness was kept (§5 item 4). The s = 0 rows: 93–95 % confirmed. ᵇ OWN at FB(0) is 6,376 with the 75 mm cut and 6,373 with none: a looser requirement giving a smaller count is the non-maximality of §1 C2 (541 OWN rows), not an error; each count stays a lower bound. M(Z) = 993,885.9. R06–R07: |
| 5 | B-1 | §0 item 2, last sentence | The one B1 row (DIF-C, R04–R06 only) is a single looping pion whose later arc comes from the Geant4 hand-over; by the frozen attribution it belongs to the parent's class, not to the DIF-C term (§3.3). | The one B1 row (DIF-C, R04–R06 only) is a single looping pion whose later arc comes from the Geant4 hand-over. **Its attribution is open (§3.3):** both readings are given (m_DIF-C = 1 as rule 1's own wording counts passes, ADD l.603-605; m_DIF-C = 0 if the attribution rule of STR l.747-753 sends it to the parent's class) and neither is chosen. It touches no T2 candidate: k = 4 > k_max = 3 at R07 and R08, k = 6–7 > 5 at s = 3 [VERIFIED, Sindre]. |
| 6 | A-1, B-4 | §0 item 5 (whole item) | 5. **Stop-and-report item (§8 item 1):** ADD l.607 replaces the v1 preselection by the day-12 MET model. That changes not only N_trig of the additions but the per-event weights and the **road axis** (v1's reconstructed MET azimuth) on which the classification was made; swapping two inputs does not make the reading binding. The pass that would (variant `v2` of `p3a_multi.py`, tested, ≈ 2.5–12 CPU-h) is defined, not launched: it needs p3-c's per-event MET. The verdict "above" would need m_Z to fall from 1,501 to 3. | 5. **Stop-and-report item (§8 item 1; the orchestrator's item 9):** ADD l.607 replaces the v1 preselection by the day-12 MET model. That changes not only N_trig of the additions but the per-event weights and the **road axis** (v1's reconstructed MET azimuth) on which the classification was made; swapping two inputs does not make the reading binding. `pilot.c0.hs` has the same dependence: its parents were drawn in proportion to w_v1 inside the v1 road (`p2a_hspool.py` l.14-17, l.57-59), so under a v2 MET model it would have to be regenerated, not reclassified. **The counts of this document cannot enter a binding reading until the orchestrator, after an advisor call, rules on this item:** (i) the rule-1 count is read on v1's preselection and axis, or (ii) a new pass with the v2 MET model's per-event weights and axis (for the Z(νν) term: variant `v2` of `p3a_multi.py`, tested, ≈ 2.5–12 CPU-h, defined, not launched, it needs p3-c's per-event MET; for `pilot.c0.hs`: regeneration). Neither is chosen here. **Sindre's bound** [ESTIMATE, Sindre, review A-1]: if the v2 model only adds weight on the v1 axis, B₅₀ ≥ ≈ 27,200 at R09; it covers neither events that lose weight nor an axis change. The verdict "above" would need m_Z to fall from 1,501 to 3. |
| 7 | C-6 | §1, 'Not run, although planned' | **Not run, although planned:** the Z(νν) events with w_v1 = 0 (1,297,459; §8 item 1) and the second half of the files for the independent search. | **Not run, although planned:** the Z(νν) events with w_v1 = 0 (1,297,459; §8 item 1) and the second half of the files for the independent search. The first is a reversal of the plan (fact 5: "I therefore classify ALL 2.3e6 Z(nunu) events"), made at 11:08 for the reason of §8 item 1 (v1's axis is not the input a v2 weight needs), not for cost (11.3 + 9.4 = 20.7 CPU-h was inside the 26 CPU-h stop limit); it is now recorded as its own DECISION block in `experiment_log.md` (fixer, review C-6). |
| 8 | B-3 | §3.1 table, R14-type row | \| R14 = R17 = R20 = FB(4) \| 4.7 mm, 3 \| | \| R14 = R17 = R20 = FB(4) (re-derived in part: 70.4 % S / 76.3 % F ᵃ) \| 4.7 mm, 3 \| |
| 9 | B-3 | §3.1 table, FB(3) row | \| FB(3) \| 9.4 mm, 3 \| | \| FB(3) (re-derived in part: 74.5 % S / 79.5 % F ᵃ) \| 9.4 mm, 3 \| |
| 10 | B-3 | §3.1 table, FB(2) row | \| FB(2) \| 18.75 mm, 3 \| | \| FB(2) (re-derived in part: 77.2 % S / 81.2 % F ᵃ) \| 18.75 mm, 3 \| |
| 11 | B-3 | §3.1 table, FB(1) row | \| FB(1) \| 37.5 mm, 3 \| | \| FB(1) (re-derived in part: 77.7 % S / 81.1 % F ᵃ) \| 37.5 mm, 3 \| |
| 12 | B-3, C-7 | §3.1 table, FB(0) 75 mm row | \| FB(0), R04 width read as w_core < 75 mm \| 75 mm, 3 \| | \| FB(0), R04 width read as w_core < 75 mm (re-derived in part: 77.3 % S / 80.4 % F ᵃ; OWN ᵇ) \| 75 mm, 3 \| |
| 13 | B-3, C-7 | §3.1 table, FB(0) window row | \| FB(0), R04 width read as "collection window only" \| none, 3 \| | \| FB(0), R04 width read as "collection window only" (re-derived in part: 77.3 % S / 80.4 % F ᵃ; OWN ᵇ) \| none, 3 \| |
| 14 | B-3, C-7 | §3.1, bullets under the table (new first two) | - **Every count is exact or a lower bound, valid for "above" only.** The B1, hs and lowpt zeros are "none found by a non-maximal search; not an upper statement". | - ᵃ **s = 3 rows: coverage label (review B-3).** Share of the counted Z(νν) events confirmed by Nils's independent search on every 2nd file (`I`; S / F as in the row). Rows that need k_IP ≥ 4 have no independent search at all (98 of the 139 not found at R08); the stored witness verifies k ≤ 5 for 1,743 of 2,307 s = 3 rows of the witness check (§5 item 4). The s = 0 rows: 93–95 % confirmed. A label of the check, not a correction of the count. - ᵇ OWN at FB(0): 6,376 with the 75 mm cut against 6,373 with no width cut (S): the looser requirement gives the smaller count. This is the non-maximality of §1 C2 (541 OWN rows with a larger k at a wider width), not an error. - **Every count is exact or a lower bound, valid for "above" only.** The B1, hs and lowpt zeros are "none found by a non-maximal search; not an upper statement". |
| 15 | B-1 | §3.3, attribution sentence | parent carries its Geant4 crossings. Under the frozen rule this row is attributed to the parent's class (j ≥ n/2 = 4 with the parent's hits), not to the Geant4-vertex class of the DIF-C term (j = 0 there). | parent carries its Geant4 crossings. **If** the attribution rule of STR l.747-753 is applied to this pilot count, the row is attributed to the parent's class (j = 4 ≥ n/2 = 3.5 with the parent's hits), not to the Geant4-vertex class of the DIF-C term (j = 0 there). Whether that rule applies to a B1 pilot count is itself open: the frozen texts below speak for one reading or the other; neither is chosen here. |
| 16 | B-1 | §3.3, after the readings table (new table of frozen texts) | Neither is chosen. No T2 candidate is touched (the row is not counted at R07, R08 or at s = 3). | Frozen texts that bear on the choice (quoted; review B-1 added the last three): \| text \| what it says \| speaks for \| \|---\|---\|---\| \| STR l.752 \| "Attributed candidates are the term, pure pile-up candidates are B2, and mixed candidates belong to no term" \| m = 0 (the witness is the parent's, not the Geant4-vertex class) \| \| ADD l.603-605 (replacement wording of rule 1 itself) \| each B1 class "is read on its own pilot sample …, m being the number of (event, road orientation) passes over 21 orientations; the parents of DIF-C and NI-C carry their Geant4 crossings beyond half a turn" \| m = 1: the rule's own sentence counts passes, names no attribution filter, and names the parent's later arcs as part of what is read \| \| STR l.748-749 \| "so direct counts on samples with pile-up are attributed by truth" \| m = 1: the attribution rule is introduced for samples with pile-up; the pilot has none \| \| ADD l.257-258 ([L15] (i)) \| repeated crossings by one curling particle are "absent from every sample, except for the parent of a decay or interaction after a turn (DIF-C, NI-C), whose later arcs are taken from Geant4" \| m = 1: sent to the pile-up route (B2), whose samples stop every particle at half a turn [UNVERIFIED, Sindre B-1], the row is read by nothing; m = 0 removes the only place where this topology is counted \| Neither is chosen; the choice belongs to PREREG_v2 (§8 item 2). No T2 candidate is touched (k = 4 > k_max = 3 at R07 and R08; k = 6–7 > 5 at s = 3) [VERIFIED, Sindre's recount `sindre_recount.json`]. |
| 17 | C-1 | §3.5, DIF bound | H(R06) < 2.9×10⁻⁷ per (event, orientation) at 68 %. | H(R06) < 2.9×10⁻⁷ per event of M (the 21 orientations of an event summed, as ADD l.384-386 defines m and M) at 68 %, i.e. ≈ 1.4×10⁻⁸ per (event, orientation). |
| 18 | B-2 | §4.1, 'A fact …' bullet heading | - **A fact the text's own argument can be tested on (T7b).** Of the 749 events | - **A fact the text's own argument can be tested on (T7b; post hoc: computed after the counts were known).** Of the 749 events |
| 19 | B-2 | §4.1, 'Points to' bullet (whole) | - **Points to: w_core** (the reading coded in Phase 2). The rung variable named in STR l.776 is w_core; and the ceiling property of l.769 and l.788 ("whatever the finder chose") holds only if every set the finder can pass at the rung is in a class: with the hard window 615 of 749 finder-type sets at R08 would be outside every class, so H would not be a ceiling for the finder's own cut. Against: the word "ribbon … of the width of r" reads geometrically, and the hard window is the more restrictive (strict-side for a pass verdict, lenient for a ceiling). CONFIDENCE: MEDIUM-HIGH. FLAG FOR HUMAN: YES (factor 10.9 in m). | - **Points to: no clear pointer** (v1: "w_core, MEDIUM-HIGH"; lowered on review B-2). Each reading satisfies one half of the text's argument. *For w_core:* it is the finder's variable and the rung variable named in STR l.776, and the ceiling property of l.769 and l.788 ("whatever the finder chose") needs every set the finder can pass at the rung to be in a class; with the hard window 615 of 749 finder-type sets at R08 would be outside every class. *For the hard window:* the argument of STR l.769 runs from a candidate found **with** pile-up to its own-hit subset ("the term's own hits … lie inside its ribbon"), and STR l.776 ("the widest-holding ribbon of a superset of hits is at least as good") is literally true for a geometric window but not for a MAD: the own hits of a set with w_core < W can have w_core > W, and added hits can push w_core up (NIL §3, the two T7 trials); the hard window is therefore the reading under which STR l.769 and l.776 hold as written, and "ribbon … of the width of r" reads geometrically. The 615-of-749 statistic is **post-hoc evidence**: it was computed after the counts were known and argues for the reading that gives the larger, already quoted number. The hard window is the more restrictive reading (strict side for a pass verdict, lenient for a ceiling). The verdict "above" holds under both (138 counts → B₅₀ 5,947 at R09, §6). CONFIDENCE: none given (no pointer). FLAG FOR HUMAN: YES (factor 10.9 in m). |
| 20 | C-2 | §4.9, factor of the smallest projection | the smallest projection over all candidates, readings and variants is above the limit by a factor 16 (HARD) to 110 (every other reading), §6. | the smallest projection over all candidates, readings and variants **on a full sample** is above the limit by a factor 16 (HARD) to 110 (every other reading); including the 115-file PV-seed subsample the factors are 12 and 96 [VERIFIED by Sindre, `D`], §6. |
| 21 | B-3 | §5 item 4, 'F within 0.5 points' | reading S (F within 0.5 points): **s = 0: | reading S (at s = 0 reading F is within 0.5 points, R08 94.2 % against 94.7 %; at s = 3 it is not: F is higher, R08 76.3 % (309 of 405) against 70.4 %, R04 80.4 % against 77.3 % [VERIFIED, `I`]): **s = 0: |
| 22 | C-5 | §5 item 4, witness check of the last 17 | (`p3a_witness_resolve.json`: 17 of 17) [VERIFIED]. | (`p3a_witness_resolve.json`: 17 of 17) [VERIFIED]. For those 17 the plane is the classifier's own, so the check there tests the verifier's cuts, not the plane search; this is valid because the definition is existential (a plane exists) (review C-5). |
| 23 | C-4 | §5 item 4, 'Not done' | planes with N_IP2 < 4); the second half of the files. | planes with N_IP2 < 4); the second half of the files (≈ 0.74 CPU-h, `cpu_s_in_jobs` ind; 8.7 CPU-h of the budget were left; review C-4 recommends running it before the binding text is written: an orchestrator decision). |
| 24 | A-1, B-4 | §6, 'Why it is not binding' (3) | (3) the Z weights and the road axis are v1's (§8 item 1); | (3) the Z weights and the road axis are v1's, and the `pilot.c0.hs` parents were drawn by w_v1 inside the v1 road (§8 item 1; these counts cannot enter a binding reading until the orchestrator, after an advisor call, rules on that item, (i) or (ii)); |
| 25 | C-3 | §6 table, R07 pile-up cell | read as N_trig/48,000 × Gamma(36) (median 3.0×10⁴) \| | read as N_trig/48,000 × Gamma(36) (median 3.0×10⁴); reading by Aurora, no approved row \| |
| 26 | C-3 | §6 table, R11 pile-up cell | \| R11 \| 0.48–0.81 (s_tot 1.29) \| | \| R11 \| 0.48–0.81 (s_tot 1.29); reading by Aurora, no approved row \| |
| 27 | C-3, B-3 | §6 table, R14-type row label and pile-up cell | \| R14 = R17 = R20, FB(4) \| none; or ≤ R11 value (s_tot 2.47) \| | \| R14 = R17 = R20, FB(4) (s = 3; m re-derived in part ᵃ) \| none; or ≤ R11 value (s_tot 2.47); reading by Aurora, no approved row \| |
| 28 | B-3 | §6, note under the table (new) | (B₅₀ values VERIFIED as arithmetic, ESTIMATE as physics; | (ᵃ s = 3 rows, R14-type and FB(0)–FB(4): the m_Z they use is re-derived only in part, 70.4–77.7 % (S) confirmed by Nils's search, none for k_IP ≥ 4; §3.1.) (B₅₀ values VERIFIED as arithmetic, ESTIMATE as physics; |
| 29 | C-2 | §6, smallest outside HARD | smallest outside HARD 33,274 (OWN, F, FB(4), true PV). | smallest outside HARD on a full sample 33,274 (OWN, F, FB(4), true PV); including the 115-file subsample 28,823 (PLANS4, F, R14-type, pv2) [VERIFIED by Sindre, `D`]. |
| 30 | B-4 | §6, heading of the last paragraph | **How the binding run is made (inputs swapped by path, no code change):** | **How the dry run is repeated with other pile-up rows and N_trig (inputs swapped by path, no code change).** This alone is **not** the binding run: the Z(νν) weights and road axis and the `pilot.c0.hs` sample depend on v1's MET (§8 item 1, to be ruled by the orchestrator after an advisor call). Inputs: |
| 31 | A-1 | §7, sentence before the table (new) | ## 7. The numbers that feed decision point 2 (STR §11.7), in one table | ## 7. The numbers that feed decision point 2 (STR §11.7), in one table None of these numbers enters a binding reading until the orchestrator, after an advisor call, rules on §8 item 1 (the orchestrator's item 9: (i) v1's preselection and axis, or (ii) a new pass with the MET-model weights and axis, with regeneration of `pilot.c0.hs`). |
| 32 | B-3 | §7, R14-type row | \| m_H, Z(νν), R14 = R17 = R20 = FB(4) \| 969 / 846 (HARD 151 / 110) \| VERIFIED \| §3.1 \| | \| m_H, Z(νν), R14 = R17 = R20 = FB(4) (s = 3) \| 969 / 846 (HARD 151 / 110) \| VERIFIED as counted; **re-derived in part**: 70.4 % (S) / 76.3 % (F) confirmed by Nils's search on half the files, no independent search for k_IP ≥ 4 \| §3.1, §5 \| |
| 33 | B-3 | §7, FB(3)–FB(0) row | \| m_H, Z(νν), FB(3) / FB(2) / FB(1) / FB(0) \| 2,212 / 4,113 / 6,224 / 7,046 or 7,052 (S) \| VERIFIED \| §3.1, §4.4 \| | \| m_H, Z(νν), FB(3) / FB(2) / FB(1) / FB(0) (s = 3) \| 2,212 / 4,113 / 6,224 / 7,046 or 7,052 (S) \| VERIFIED as counted; **re-derived in part**: 74.5 / 77.2 / 77.7 / 77.3 % (S) confirmed by Nils's search on half the files, no independent search for k_IP ≥ 4 \| §3.1, §4.4, §5 \| |
| 34 | B-1 | §7, B1 R06–R07 row | \| 0, 0 (DIF-C R06: 1 own-hit row, parent-only witness) \| | \| 0, 0 (DIF-C R06: 1 or 0, attribution open, both readings given, §3.3) \| |
| 35 | A-1, B-3 | §7, B₅₀ row | \| rule-1 projection B₅₀ \| **NOT BINDING**: 63,170 (S) / 62,037 (F) at R09; 40,836 / 35,669 at R14-type; ≥ 4,726 in every reading on a full sample \| VERIFIED arithmetic, ESTIMATE physics \| §6 \| | \| rule-1 projection B₅₀ \| **NOT BINDING** (§8 item 1 not ruled): 63,170 (S) / 62,037 (F) at R09; 40,836 / 35,669 at R14-type (s = 3, m re-derived in part); ≥ 4,726 in every reading on a full sample \| VERIFIED arithmetic, ESTIMATE physics \| §6 \| \| B₅₀ if the v2 MET model only adds weight on the v1 axis \| ≥ ≈ 27,200 at R09 (Sindre's bound; covers neither weight lost nor an axis change) \| ESTIMATE, Sindre (review A-1) \| §8 item 1 \| |
| 36 | A-1, B-4 | §8 item 1, end (new (c)–(e)) | 1,501 to 3); the number can. I did not classify the w_v1 = 0 events on v1's axis: 9.4 CPU-h [ESTIMATE] for an input that would not be the one needed. | 1,501 to 3); the number can. I did not classify the w_v1 = 0 events on v1's axis: 9.4 CPU-h [ESTIMATE] for an input that would not be the one needed. **Added in v2 (review A-1, B-4).** (c) **`pilot.c0.hs` has the same dependence, and no reclassification pass can remove it:** its parents are drawn "INSIDE the road of their own event, \|dphi(parent, phimet_reco_v1)\| < 0.15" and in proportion to w_v1, "so events failing v1's preselection (w = 0) are never fired" (`p2a_hspool.py` l.14-17, l.57-59; ADD l.377-379). Under (ii) this sample must be regenerated (chain rerun), not re-read; **the ≈ 2.5–12 CPU-h pass above covers the Z(νν) term only.** In the dry run `pilot.c0.hs` is a zero-count floor of 2.8 events, so it cannot move the verdict; it decides whether a reading binding on the v2 model is achievable at all. (d) **Status: the counts of this document cannot enter a binding reading until the orchestrator, after an advisor call, rules on this item** (the orchestrator's item 9): (i) or (ii), and what happens to `pilot.c0.hs` under each. Neither is chosen here. (e) **Sindre's bound** [ESTIMATE, Sindre, review A-1], needing no new pass: if the v2 model only adds weight on the v1 axis, the worst case is that all 2.3×10⁶ events are full-weight and no new event counts: 41.70×10⁶ / 2.3×10⁶ = 18.1 events per count, × 1,502 ≈ 27,200 events at R09, so B₅₀ ≥ ≈ 27,200. It does not cover events that lose weight, nor an axis change; for those there is no bound, only the size of the gap (m_Z would have to fall from 1,501 to 3). |
| 37 | B-1 | §8 item 2, DIF-C | and whether a parent-only witness counts for a B1 term (§3.3). | and whether a parent-only witness counts for a B1 term (§3.3: both readings, m = 0 or 1, and the frozen texts for each, ADD l.603-605 and l.257-258 and STR l.748-749 among them). |
| 38 | B-3, C-4 | §8 item 5 | and covers half of the files (§5 item 4). | and covers half of the files (§5 item 4). Every s = 3 row of §0, §3.1 and §7 now carries this label (70.4–77.7 % (S) confirmed; none for k_IP ≥ 4). Running the second half (≈ 0.74 CPU-h) before the binding text is written is recommended by review C-4; not run in v2 (no new jobs). |
| 39 | C-8 | §8 item 8 | 8. `qv2run rebuild-ledger` not run by me. Nothing of mine is running; slot released in `SLOTS.md`. | 8. `qv2run rebuild-ledger` not run by me. Nothing of mine is running; slot released in `SLOTS.md`. The orchestrator should rebuild the ledger before the CPU total is quoted: ≈ 1.0 CPU-h is outside the ledger, and a fourth process ran beside three jobs at 12:00 (self-reported; review C-8). |
| — | (all) | title block | — | this section added |

Status per finding: **A-1** not the fixer's (orchestrator + advisor ruling); stated in §0 item 5, §6, §7, §8 item 1
with Sindre's bound. **B-1, B-2, B-3, B-4** resolved in the text. **C-1, C-2, C-3, C-5, C-7** resolved in the text;
**C-4** recommendation recorded (job not run: no new jobs); **C-6** recorded in §1 and as a DECISION block in
`experiment_log.md`; **C-8** orchestrator action recorded in §8 item 8.

## 0. Summary

1. **The final classification is the Phase-2 classification, reproduced and completed.** The pilot files were
   generated with the hand-over variant that addendum 1 froze per stream (radius cut; option (a) for DIF-C and NI-C;
   by class for hs and lowpt), so no chain was rerun. All 1,083 pilot files were reclassified with the reviewed
   Phase-2 classifier imported unchanged: **14,757 of 14,757 rows identical** to Phase 2 [VERIFIED]. Added: every
   reading the frozen text leaves open, the six widths (R04 both ways), s = 0 and s = 3, both pools, two PV choices.
2. **Final ceiling counts (exact or lower bounds, valid for "above" only)** [VERIFIED]:

| T2 candidate | m_Z, as produced (S / F) | other readings (S): own axis / PLAN-S4 search / hard window | every B1 class, hs, lowpt |
|---|---|---|---|
| R07 | 3,781 / 3,668 | 3,613 / 3,531 / 568 | 0 |
| **R08 = R09 = R11** | **1,501 / 1,474** | 1,449 / 1,378 / 138 | 0 |
| R14 = R17 = R20 = FB(4) (s = 3; re-derived in part ᵃ) | 969 / 846 | 946 / 945 / 151 | 0 |
| FB(3) / FB(2) / FB(1) (s = 3; re-derived in part ᵃ) | 2,212 / 1,964; 4,113 / 3,802; 6,224 / 5,870 | 2,081 / 2,150 / 410; 3,841 / 4,035 / 1,192; 5,737 / 6,208 / 2,859 | 0 |
| FB(0) (R04 width: 75 mm; window only) (s = 3; re-derived in part ᵃ; OWN ᵇ) | 7,046 / 6,641; 7,052 / 6,645 | 6,376 / 7,046 / 5,367; 6,373 / 7,052 / 6,373 | 0 |

   ᵃ **s = 3 coverage (review B-3):** share of the counted events confirmed by Nils's independent search (every 2nd
   file; `I`), reading S / F: R08 (R14-type, FB(4)) 70.4 / 76.3 %; R07 (FB(3)) 74.5 / 79.5 %; R06 (FB(2)) 77.2 /
   81.2 %; R05 (FB(1)) 77.7 / 81.1 %; R04 (FB(0)) 77.3 / 80.4 % [VERIFIED: ratios `confirmed`/`counted` of `I`].
   Rows that need k_IP ≥ 4 have **no independent search** (98 of the 139 not found at R08); in the witness check
   (39 files) the stored witness gives k ≤ 5 for 1,743 of 2,307 s = 3 rows, for the rest no witness was kept
   (§5 item 4). The s = 0 rows: 93–95 % confirmed.
   ᵇ OWN at FB(0) is 6,376 with the 75 mm cut and 6,373 with none: a looser requirement giving a smaller count is the
   non-maximality of §1 C2 (541 OWN rows), not an error; each count stays a lower bound.

   M(Z) = 993,885.9. R06–R07: 7,202 → 3,781 (S); falls ×1.61, ×1.90, ×2.52 per width step (R05→R06→R07→R08), nothing
   like the pile-up fall. 1/H(R06) = 138 for Z(νν); not measurable for the B1 classes (empty); G_t = 1 (not measured).
   The one B1 row (DIF-C, R04–R06 only) is a single looping pion whose later arc comes from the Geant4 hand-over.
   **Its attribution is open (§3.3):** both readings are given (m_DIF-C = 1 as rule 1's own wording counts passes,
   ADD l.603-605; m_DIF-C = 0 if the attribution rule of STR l.747-753 sends it to the parent's class) and neither is
   chosen. It touches no T2 candidate: k = 4 > k_max = 3 at R07 and R08, k = 6–7 > 5 at s = 3 [VERIFIED, Sindre].
3. **Open choices (none chosen; §4):** width reading S3 (1,501 against 138), axis convention (1,501 / 1,449), search
   (1,501 / 1,378; union 1,526), R04 width (7,046 / 7,052 at FB(0)), N_IT2 (S / F), hit merging (1,501 merged /
   1,516 not merged), PV for Z(νν) (1,501 draw / 1,510 true vertex; ±2 % at every candidate, event-level reshuffle
   6–9 %), M (993,885.9 measured / 1,011,080 planned), flagged events (identical), best candidate (G not available:
   every candidate given), pile-up at N_2S2 ≥ 3 (none / ≤ R11 value). Nils's conditions: §5 (independent search
   confirms 93–95 % of the counted events at R04–R08 for s = 0, as at the width he covered; 70–77 % at s = 3, where
   40–70 % of the rest is outside the reach of his search).
4. **Dry run of rule 1, NOT BINDING** (v1-based EST pile-up rows; planning N_trig of the three MET additions; v1
   weights): B₅₀ = 63,170 (S) / 62,037 (F) at R09, 63,246–63,294 at R08, 189,341 at R07, 40,836 / 35,669 at the
   R14-type candidates and FB(4), 93,021–296,198 at FB(3)…FB(0). **All 1,440 projections (every candidate, reading,
   pool, PV, flagged variant) are above 299.1**; the smallest on a full sample is 4,726 (hard window, F, FB(4)).
5. **Stop-and-report item (§8 item 1; the orchestrator's item 9):** ADD l.607 replaces the v1 preselection by the
   day-12 MET model. That changes not only N_trig of the additions but the per-event weights and the **road axis**
   (v1's reconstructed MET azimuth) on which the classification was made; swapping two inputs does not make the
   reading binding. `pilot.c0.hs` has the same dependence: its parents were drawn in proportion to w_v1 inside the v1
   road (`p2a_hspool.py` l.14-17, l.57-59), so under a v2 MET model it would have to be regenerated, not reclassified.
   **The counts of this document cannot enter a binding reading until the orchestrator, after an advisor call, rules
   on this item:** (i) the rule-1 count is read on v1's preselection and axis, or (ii) a new pass with the v2 MET
   model's per-event weights and axis (for the Z(νν) term: variant `v2` of `p3a_multi.py`, tested, ≈ 2.5–12 CPU-h,
   defined, not launched, it needs p3-c's per-event MET; for `pilot.c0.hs`: regeneration). Neither is chosen here.
   **Sindre's bound** [ESTIMATE, Sindre, review A-1]: if the v2 model only adds weight on the v1 axis, B₅₀ ≥ ≈ 27,200
   at R09; it covers neither events that lose weight nor an axis change. The verdict "above" would need m_Z to fall
   from 1,501 to 3.

CPU: ≈ 11.3 CPU-h of 20 (no stop rule near). No signal file opened; no efficiency formed.

## 1. What was run

Code (all new, `phase3_selection/src/p3a/`; Phase-2 code imported, never edited): `p3a_subset.py` (classifier: BASE =
`p2w_subset.py` unchanged + witness categories c0–c4, six widths, s = 0 / 3, S / F, k per layer type), `p3a_multi.py`
(every variant from one read of each pilot file; `classify_pool` of `p3a_subset.py` imported unchanged),
`p3a_indep.py` (Nils's search and verifier, imported unchanged, at the other widths and s = 3), `p3a_counts.py`,
`p3a_indep_summary.py`, `p3a_witness_check.py`, `p3a_attrib.py`, `p3a_xcheck.py`, `p3a_rule1_dryrun.py`,
`p3a_tables.py`, `test_p3a_subset.py` (4 synthetic tests, pass), `p3a_campaigns.py`. Campaign files and the queue
script: `tools/runner/examples/p3a/`. Node landau, at most 3 jobs, SSH runner; bulk outputs
`/nfs/cajuela/jdochoa/quirks_v2/data/p3a/<campaign>/000/`, markers `ledger/markers/<campaign>/`.

| campaign | what | pilot files | jobs done | CPU-h (markers, all attempts) | status |
|---|---|---|---|---|---|
| `p3-a-clsxz` | Z(νν), one read per file: **m** (merged pool, PV draw, w_v1 > 0 = the Phase-2 configuration), **u** (pool not merged), **pv0** (PV = true vertex), **pv2** (other PV seed, every 4th file), **ind** (Nils's search on the counted events, every 2nd file) | 460 (2.3×10⁶ generated; 1,002,541 with w_v1 > 0) | 115 / 115 | 9.02 | complete, 0 errors |
| `p3-a-clsxb` | B1 / hs / lowpt, one read per file: **m**, **u**; 21 orientations (hs: 1); witness hit tables for every row | 623 (1.92×10⁷ events) | 116 / 116 | 0.91 | complete, 0 errors |
| `p3-a-cls-m` | first design, one read per variant (`p3a_subset.py` alone): **stopped by me** (NFS-bound, see below) | 60 Z | 5 done, 1 failed (killed) | 0.37 | kept only as a cross-check of the two drivers |
| ssh slices, tests, summaries, witness check | synthetic tests 0.18; timing and regression slices, two killed jobs, summaries ≈ 0.3; witness check ≈ 0.45 (two runs and the resolution) | — | — | ≈ 1.0 [ESTIMATE, `/usr/bin/time` and job logs; not in the ledger] | — |
| **total p3-a** | | | | **≈ 11.3 of 20 budgeted** | |

VERIFIED from the markers (sum of `cpu_s` over every non-`started` line: 10.30 CPU-h; `qv2run rebuild-ledger` was not run
by me). In-job CPU by variant (`C`, `cpu_s_in_jobs`): m 3.15, u 2.46, pv0 2.50, pv2 0.62, ind 0.74 CPU-h.

**Deviation from my plan (cost only).** The plan had one campaign per variant. The first one ran at 980 s of wall for
240 CPU-s per 12 files: a 169 MB pilot file read at 1.8 MB/s from landau (dd, 10:50, three of my jobs reading). Each
further pass over the 77 GB of Z(νν) files would have cost about 3.5 h of wall. I stopped it and read every file once
for all variants (`p3a_multi.py`). The two drivers agree on the 60 files both classified: 1,987 of 1,987 rows
identical in every column (`X`) [VERIFIED].
**Not run, although planned:** the Z(νν) events with w_v1 = 0 (1,297,459; §8 item 1) and the second half of the files
for the independent search. The first is a reversal of the plan (fact 5: "I therefore classify ALL 2.3e6 Z(nunu)
events"), made at 11:08 for the reason of §8 item 1 (v1's axis is not the input a v2 weight needs), not for cost
(11.3 + 9.4 = 20.7 CPU-h was inside the 26 CPU-h stop limit); it is now recorded as its own DECISION block in
`experiment_log.md` (fixer, review C-6).

**Pre-declared checks (plan, C1–C4).**
- **C1 regression: PASS.** My BASE rows equal the Phase-2 rows of `p2w_subset.py` for every (file, event,
  orientation): 14,757 of 14,757 rows, all five Phase-2 widths, s = 0 / 3, S / F; no row only in Phase 2, none only in
  mine (`C` `regression_phase2`). 1,083 pilot files, each classified exactly once and completely (the script stops
  otherwise); 0 kernel errors; 6,015,303 (event, orientation) roads past the prefilter, 8,478,764,727 seeds, 595,283
  aligned planes (ING l.45: 6.02×10⁶, 8.48×10⁹, 5.95×10⁵). m_Z(R08) = 1,501 (S) / 1,474 (F); 969 / 846 at s = 3 [VERIFIED].
- **C2 relations.** Width-monotone for full sets (c0, c1): 0 violations. HARD never below OWN: 0. min(c0, c2) never
  above BASE: 0. F never below S: 0. Listed, not removed: in 201 BASE rows and 541 OWN rows the stored k is larger at a
  wider width than at a narrower one. That cannot happen for a maximal search; it is the non-maximality NIL §3
  measured (each count stays a lower bound).
- **C3 dry run.** Empty pilot reproduces 160.8 / 238.3 / 262.3 / 283.8; Ingvild's (S) and (F) readings reproduce
  `rule1_valid_b50_ingvild_2026-11-23.json` bit for bit (`D` `check2`) before any of my counts is used.
- **C4 independent search and witness check:** §5.
- Synthetic tests (`test_p3a_subset.py`, 630 CPU-s): BASE of my road loop = `p2w_subset.classify_pool` on 119 random
  events; category relations; my witnesses pass Nils's verifier; hard-window flag on constructed events. 4 / 4 pass.

## 2. What "final" means here, and the definitions used as frozen

1. **Frozen hand-over variant.** STR l.744-746 planned two variants "compared on 100 events in Phase 3 and one is
   frozen"; ADD §3 P6 (approved 17 Nov, decision D9; COM l.322) superseded that line (ADD l.614) and decided per
   stream: v1's radius cut for DIF, NI 22 / 30 / 61.5 mm and NI-X; option (a) ("hybrid": Fatras parent to the Geant4
   vertex time plus injected Geant4 crossings) for DIF-C and NI-C; `autoh` (by class) for `pilot.c0.hs` and
   `pilot.c0.lowpt`; products from the slab exit, β < 0.1 not handed over. The pilot was generated with exactly this
   (table T10, read from the `trunc_mode`, `n_per_ev_mode`, `beta_min` and `handover` fields of all 623 B1 / hs / lowpt
   files in my jobs). **The Phase-2 classifications therefore already ran on the frozen hand-over variant; "final"
   needs no new chain run**, and none was made. What is final here is the classification of those files under every
   reading of the estimator text, with the Phase-2 number reproduced row by row as one of them.
2. **Own-hit classes (STR l.755-762, quoted).** "The no-pile-up state of an event of term t is classified on subsets of
   the term's own hits … For rung r, a width-only pass over those hits finds the ribbon through the PV in the road, of
   the width of r, that holds the most double-crossing layers. The deficits are counted per layer type: k_IP = max(0,
   n_IP(r) − N_IP2), k_2S = max(0, n_2S(r) − N_2S2), k = k_IP + k_2S (the fixed cut N_IT2 ≥ 3 is a cut on a subset of the
   IP layers and is part of k_IP). f₀(r) = P_geo(r) is the probability of k = 0, and f_k(r) that of a deficit k, for
   k = 1 … k_max = ⌊n(r)/2⌋ ("near-pass"). At the counting rungs R01–R04, where the ladder has no width cut yet, the
   width is the finder's maximum core width (frozen configuration, transcribed in Phase 2); at R12–R14 it is the R08
   width." All own hits, before CKF (Df-9 option (a), STR l.780). The ceiling count is near-pass inclusive:
   H = P_geo + Σ_k f_k (STR l.799; advisor ruling LOG 19 Nov 15:24), m = number of (event, road orientation) with
   k ≤ k_max; n = 7, k_max = 3 without the 2S requirement (s = 0) and n = 10, k_max = 5 with N_2S2 ≥ 3 (s = 3).
3. **T2 candidates and the count each one reads** (STR l.1794-1798: R07, R08, R09, R11, R14, R17, R20 and FB(k_adm),
   each with and without the displaced-vertex veto). H applies "the counting and width cuts only … an untested
   conditional is 1, so for an untested term H is flat from R08 to R11 and from R14 to R20" (STR l.800-802); the
   vertex veto is a B3 conditional. So: R07 → (9.4 mm, s = 0); R08 = R09 = R11 → (4.7 mm, s = 0); R14 = R17 = R20 →
   (4.7 mm, s = 3). The fallback is `fb0 = R04 & p > 0.05 & N_2S2 ≥ 3`, `FBk = fb0 & w_core < W_c/2^k`
   (`acts/stage4/finder/production.py` l.180-183 [VERIFIED by reading]), k_adm ∈ {0, …, 4} per hypothesis
   (`wp_rule_tables.py` l.72): FB(k) → (none | 37.5 | 18.75 | 9.4 | 4.7 mm, s = 3). FB(4) has the cuts of R14.
   **FB(0) reads the R04-width count at s = 3**, so the R04 width of STR l.761-762 belongs to a T2 candidate (§4.4).
4. **Attribution (STR l.747-753, quoted).** "Let n(r) be the number of double-crossing layers that rung r requires and
   j the number of the candidate's double-crossing layers whose two hits come from particles of one origin class of §2.
   The candidate is attributed to that class if j ≥ n/2, mixed if 1 ≤ j < n/2 for every class, and pure pile-up if j = 0
   for the hard-scatter and Geant4 classes." In the pilot: the Z(νν) files have `mu = 0.0` and `mode = hs0x` in all
   460 (checked in the job; `p3a_counts.py` stops otherwise) and contain no Geant4 vertex, so every hit is of the one
   class "particles of the hard-scatter vertex that Fatras traces" (STR l.230; conversions and Fatras-made secondaries
   included). **Every counted Z(νν) witness is attributed by construction** (j = its number of double-crossing layers
   ≥ n − k_max ≥ n/2); there is no mixed and no pure-pile-up candidate in a no-pile-up sample of one class. In a B1 /
   hs / lowpt file two classes exist: the products of the Geant4 vertex (the B1 class) and the parent hadron, a Fatras
   particle (pile-up route for the minimum-bias share, hard-scatter route in `pilot.c0.hs`). For every stored row of
   these samples the witness hit table was dumped and j computed per class (§3.3).
5. **Subset pass.** The classifier of Phase 2 (`p2w_subset.py`, sha256 c68b7b69…, reviewed by Nils) is imported
   unchanged and gives the reading BASE. Its readings S1–S5 (CEC l.38-54) are readings of text the strategy does not
   fix; by the advisor ruling of 23 Nov 19:44 (Vigdis) the axis convention and reading S3 are NOT fixed now, and the
   binding-m candidate is the count "as produced, exact or lower bound, valid for 'above' only". I therefore add the
   other readings as separate columns and change nothing in BASE:

| reading | what is counted | where it comes from |
|---|---|---|
| **BASE** | `p2w_subset.plane_best` unchanged: the plane's full hit set judged with the finder's stored axis and w_core < W; else window-and-fill subsets (7 window offsets, axes along the plane and along each IP hit), each judged with its own axis | Phase 2 as produced (binding-m candidate of the 23 Nov ruling) |
| **OWN** | one single axis convention: every set, the full set included, judged with its own in-plane axis (the convention of `p2w_subset._eval`); all my searches | NIL condition 2 (b): "a full set is judged with the finder's axis, a subset with its own" |
| **HARD** | reading S3 replaced by a hard window: every IP hit of the subset inside one window of full width 2W/1.4826 (own axis; pure windows at every IP hit added to the search) | NIL condition 2 (a), his category H |
| **PLANS4** | the full set with the finder's axis; else window-and-fill with the centres **as PLAN S4 words them** ("each IP hit and each midpoint of neighbours", plane's axis), own-axis judged | NIL §1 row 6: "the code is a different heuristic from the one S4 describes" |
| **UNION** | the smallest k of all of the above (both axis conventions, all searches) | information only, like NIL's 1,610 |

   S / F: reading S has no separate N_IT2 requirement (CEC S5: "is part of k_IP"), F requires N_IT2 ≥ 3 of the subset.
   Every count in every reading has a witness; none is a proven maximum: **each is exact or a lower bound, valid for an
   "above" statement only** (NIL condition 1). A zero is "none found by a non-maximal search; not an upper statement"
   (ruling of 23 Nov, item 2).

## 3. Final classification: the counts

All numbers VERIFIED (`C`, `T`; label m = merged pool, PV draw, w_v1 > 0, flagged events WITH), unless tagged otherwise.
Samples: DIF 4×10⁶, DIF-C 4×10⁶, NI 22 / 30 / 61.5 mm 10⁶ each, NI-X 4×10⁶, NI-C 2×10⁶ events × 21 orientations;
hs 2×10⁶ (own road); lowpt 2×10⁵ × 21; Z(νν) 2.3×10⁶ generated: 994,446 in the full-weight class (w_v1 ≥ 0.5), 8,095 in
the 0.05 class, 1,297,459 with w_v1 = 0 (in no term under v1 weights; not classified). M of the Z term from the
unrounded weights of the 460 files: Σw/w_max = 974,008.2056 / 0.98 = **993,885.9** (= YLV §2; the single value).

### 3.1 Ceiling counts m_H per term at every T2 candidate (full table: T1)

| T2 candidate | (width, s) | Z(νν) full class, **BASE** (S / F) = Phase 2 as produced | OWN (S / F) | PLANS4 (S / F) | HARD (S / F) | UNION (S / F), information | Z 0.05 class BASE (S / F) | DIF, DIF-C, NI 22 / 30 / 61.5, NI-X, NI-C, hs, lowpt (every reading, pools m and u) |
|---|---|---|---|---|---|---|---|---|
| R07 | 9.4 mm, 0 | 3,781 / 3,668 | 3,613 / 3,512 | 3,531 / 3,422 | 568 / 565 | 3,804 / 3,692 | 36 / 35 | 0 |
| **R08 = R09 = R11** | 4.7 mm, 0 | **1,501 / 1,474** | 1,449 / 1,420 | 1,378 / 1,349 | 138 / 138 | 1,526 / 1,500 | 13 / 13 | 0 |
| R14 = R17 = R20 = FB(4) (re-derived in part: 70.4 % S / 76.3 % F ᵃ) | 4.7 mm, 3 | 969 / 846 | 946 / 814 | 945 / 816 | 151 / 110 | 995 / 865 | 12 / 9 | 0 |
| FB(3) (re-derived in part: 74.5 % S / 79.5 % F ᵃ) | 9.4 mm, 3 | 2,212 / 1,964 | 2,081 / 1,846 | 2,150 / 1,900 | 410 / 351 | 2,235 / 1,982 | 25 / 20 | 0 |
| FB(2) (re-derived in part: 77.2 % S / 81.2 % F ᵃ) | 18.75 mm, 3 | 4,113 / 3,802 | 3,841 / 3,564 | 4,035 / 3,731 | 1,192 / 1,048 | 4,119 / 3,809 | 43 / 36 | 0 |
| FB(1) (re-derived in part: 77.7 % S / 81.1 % F ᵃ) | 37.5 mm, 3 | 6,224 / 5,870 | 5,737 / 5,427 | 6,208 / 5,854 | 2,859 / 2,690 | 6,231 / 5,877 | 62 / 51 | 0 |
| FB(0), R04 width read as w_core < 75 mm (re-derived in part: 77.3 % S / 80.4 % F ᵃ; OWN ᵇ) | 75 mm, 3 | 7,046 / 6,641 | 6,376 / 6,033 | 7,046 / 6,641 | 5,367 / 5,076 | 7,046 / 6,641 | 65 / 54 | 0 |
| FB(0), R04 width read as "collection window only" (re-derived in part: 77.3 % S / 80.4 % F ᵃ; OWN ᵇ) | none, 3 | 7,052 / 6,645 | 6,373 / 6,025 | 7,052 / 6,645 | 6,373 / 6,025 | 7,052 / 6,645 | 65 / 54 | 0 |

- ᵃ **s = 3 rows: coverage label (review B-3).** Share of the counted Z(νν) events confirmed by Nils's independent
  search on every 2nd file (`I`; S / F as in the row). Rows that need k_IP ≥ 4 have no independent search at all (98
  of the 139 not found at R08); the stored witness verifies k ≤ 5 for 1,743 of 2,307 s = 3 rows of the witness
  check (§5 item 4). The s = 0 rows: 93–95 % confirmed. A label of the check, not a correction of the count.
- ᵇ OWN at FB(0): 6,376 with the 75 mm cut against 6,373 with no width cut (S): the looser requirement gives the
  smaller count. This is the non-maximality of §1 C2 (541 OWN rows with a larger k at a wider width), not an error.
- **Every count is exact or a lower bound, valid for "above" only.** The B1, hs and lowpt zeros are "none found by a
  non-maximal search; not an upper statement".
- (HARD at s = 3 can exceed HARD at s = 0 at R08 because k_max is 5 instead of 3: events with N_IP2 = 2–3 and three
  2S layers count at s = 3 only.)
- The same table for the pool variant u and the PV variant pv0: T6, T7 and §4.6, §4.7.

### 3.2 R06–R07 counts and the fall per width step (STR l.879-880, l.2723-2724; T2, T3)

Z(νν) full class, s = 0, BASE (S): **R05 11,566 → R06 7,202 → R07 3,781 → R08 1,501**; falls ×1.61, ×1.90, ×2.52 per
halving of the width (F: 11,220 → 6,981 → 3,668 → 1,474; ×1.61, ×1.90, ×2.49). R04: 13,923 (window only) / 13,915
(w_core < 75 mm). Under HARD the falls are ×2.46, ×3.51, ×4.12 (4,910 → 1,993 → 568 → 138). The pile-up falls of v1
are ×201 and ×339 (STR l.1014). The R08 count exists, so the extrapolation of STR l.879-880 is not needed for the
branch of rule 3; as a check, R07 / (R06→R07 fall) = 1,985 against 1,501 counted (BASE S) [ESTIMATE by construction].
**Branch of §11.7 rule 3 as these counts read: (b), "a counted ceiling leads the projection"** (the Z term, §6);
this is a reading of the table, the decision is not mine.
B1 classes: 0 at R06 and R07 in every class and reading, except DIF-C at R06 (1 own-hit row; §3.3).

### 3.3 The B1, hard-scatter-parent and low-p_T alarm samples

**One stored row in 1.92×10⁷ events × orientations** (any k within k_max, at any width, in any category, pools m and u;
T7c): `p2-c-pilot-c0-difc-0076`, event 22,673, orientation 20 (the event Tove and Ingvild found). k = 3 at R04, R05,
R06 (s = 0), k = 4 at R07 and R08; at s = 3 k = 6–7 (not counted). Not flagged. No event is counted in more than one
orientation; the row is in an off-road orientation (k ≠ 0; ADD l.390-391: reported as an alarm, 1 of 1).
**Attribution by truth (`A`; STR l.747-753):** the witness at R04–R06 has 11 hits, **all of the parent** (a π⁺ of
p_T 0.525 GeV decaying at r = 633 mm), no product hit; its four double-crossing IP layers are made by the parent alone
(j_parent = 4, j_product = 0). It is one curling pion crossing four layers twice, with its later arc injected from
Geant4 (option (a) of the hand-over): the repeated-crossing topology of [L15], present here only because the DIF-C
parent carries its Geant4 crossings. **If** the attribution rule of STR l.747-753 is applied to this pilot count, the
row is attributed to the parent's class (j = 4 ≥ n/2 = 3.5 with the parent's hits), not to the Geant4-vertex class of
the DIF-C term (j = 0 there). Whether that rule applies to a B1 pilot count is itself open: the frozen texts below
speak for one reading or the other; neither is chosen here.

| count of DIF-C at R04 / R05 / R06 (s = 0) | value | reading |
|---|---|---|
| own-hit count as rule 1 words it (STR l.2731: "the own-hit count m of the pilot sample") | 1 | every own hit of the event, parent included (Phase 2, BJO, ING) |
| own-hit count restricted to witnesses attributed to the term's class (STR l.752 "attributed candidates are the term") | 0 | parent-only witness → pile-up route (B2) for the minimum-bias share |

Frozen texts that bear on the choice (quoted; review B-1 added the last three):

| text | what it says | speaks for |
|---|---|---|
| STR l.752 | "Attributed candidates are the term, pure pile-up candidates are B2, and mixed candidates belong to no term" | m = 0 (the witness is the parent's, not the Geant4-vertex class) |
| ADD l.603-605 (replacement wording of rule 1 itself) | each B1 class "is read on its own pilot sample …, m being the number of (event, road orientation) passes over 21 orientations; the parents of DIF-C and NI-C carry their Geant4 crossings beyond half a turn" | m = 1: the rule's own sentence counts passes, names no attribution filter, and names the parent's later arcs as part of what is read |
| STR l.748-749 | "so direct counts on samples with pile-up are attributed by truth" | m = 1: the attribution rule is introduced for samples with pile-up; the pilot has none |
| ADD l.257-258 ([L15] (i)) | repeated crossings by one curling particle are "absent from every sample, except for the parent of a decay or interaction after a turn (DIF-C, NI-C), whose later arcs are taken from Geant4" | m = 1: sent to the pile-up route (B2), whose samples stop every particle at half a turn [UNVERIFIED, Sindre B-1], the row is read by nothing; m = 0 removes the only place where this topology is counted |

Neither is chosen; the choice belongs to PREREG_v2 (§8 item 2). No T2 candidate is touched (k = 4 > k_max = 3 at R07
and R08; k = 6–7 > 5 at s = 3) [VERIFIED, Sindre's recount `sindre_recount.json`].
Plainly: the seven B1 classes, the hard-scatter-parent sample and the low-p_T alarm sample hold **no** own-hit pass or
near-pass at any T2 candidate, in any reading, with merged or unmerged hits. The low-p_T alarm (ADD l.396-397: "one
own-hit pass at a T2 candidate rung is by itself above 300") did not fire. This zero comes from a search that is not
maximal and has no "above" protection (NIL §4): it is not an upper statement.

### 3.4 Own-hit classes (k per layer type; T4, T5)

Z(νν) full class, BASE (S), by deficit k = 0 / 1 / 2 / 3: R06 157 / 491 / 2,135 / 4,419; R07 81 / 213 / 965 / 2,522;
**R08 26 / 80 / 318 / 1,077** (= ING l.21). P_geo-type passes (k = 0): 26 at R08 (Tove's finder pass count: 11).
72 % of the R08 count sits at the largest allowed deficit. At s = 3, R08: k = 0…5: 3 / 19 / 41 / 82 / 201 / 623.
Per layer type at s = 3 (k_IP, k_2S) the largest classes at R08 are (2, 3) 210, (4, 1) 199, (3, 2) 164 (UNION S;
T5 gives PLANS4, OWN and UNION at R08 and R04w; for BASE the split is not available because `p2w_subset.plane_best`
returns k only). The k_max class boundary carries most of the count: a different k_max would change m by a large
factor; k_max = ⌊n/2⌋ is frozen (STR l.760).
What the R08 witnesses are made of (UNION S, 1,526 events, best witness; `T` `witness_Z_R08`): 778 of two particles,
505 of three; 692 with every hit on a selected CKF track, 1,403 with at least half, 72 with none; 363 contain a hit
of a secondary-vertex product, 62 a Fatras-made hit. (BJO l.54-56 on the 253 finder near-passes: 138 two-particle,
54 with a secondary-product hit.) Björn's D9 question (are configurations with a secondary-product hit also what the
hs B1 term stands for) is open; without them the R08 count would be at least 1,526 − 363 = 1,163 [ESTIMATE: UNION
witnesses, not BASE rows].

### 3.5 Enrichment 1/H(R06) and the gains G_t (STR §4.4 point 5, §11.7; T9)

- **Z(νν): H(R06) = (7,202 + 1)/993,885.9 = 7.25×10⁻³ per full-weight event, enrichment E = 1/H(R06) = 138** (BASE S;
  F: 6,981 → 142; HARD: 1,993 → 498; OWN: 6,773 → 147). Rule 3 (b) of §11.7 reads E ≥ 10² as "enriched test
  overlays (or enriched hit-level events) sized for N ≥ 24".
- B1 classes, hs, lowpt: m(R06) = 0 (DIF-C: 1 or 0, §3.3). H(R06) ≤ 1.14/M at 68 %: E ≥ 3.5×10⁶ (DIF, NI-X),
  ≥ 1.76×10⁶ (NI-C, hs), ≥ 8.8×10⁵ (NI 22 / 30 / 61.5), ≥ 1.8×10⁵ (lowpt); these are bounds from empty samples, not
  measured enrichments. **Phase 1 assumed** H(R06) ≥ 0.004 for DIF (STR l.1048) and sized the scan slice N_scan =
  4,000/H(R06) ≤ 10⁶ from it. **The pilot found** no DIF event in class k ≤ 3 at R06 in 4×10⁶ × 21 orientations, i.e.
  H(R06) < 2.9×10⁻⁷ per event of M (the 21 orientations of an event summed, as ADD l.384-386 defines m and M) at
  68 %, i.e. ≈ 1.4×10⁻⁸ per (event, orientation). **Implication:** 4,000 passing and near-pass DIF events for the
  enriched overlays (STR l.1045-1049) cannot be collected from any affordable scan slice (already void by EXP §9 item
  2; this is the direct measurement). Strategy-revision input for the B1 work package.
- **G_t.** STR l.862-871 defines the gain of biased generation as (exposure gain of the road orientations, at most
  2π/0.30 = 20.9) × (stiffness gain, "needs the particle spectra"), "the gain is not measured yet … until then every
  number in this document assumes G = 1". What the pilot fixes: the orientation factor is realised in the count
  itself (21 fixed orientations per event, over-read 0.27 %, ADD l.384-386), so it is in M, not a further gain. The
  stiffness gain cannot be measured on the pilot: it needs passing or near-pass events whose parent p_T can be
  compared with the generated spectrum, and the B1 samples hold one such row (a 0.525 GeV pion, at the soft edge of
  the pool; §3.3), none at R07–R08. The analytic sagitta bound that would define the excluded soft bulk (COM B1-e) is
  not written. **G_t = 1 for every term (not measured); "gain per term recorded before the freeze" (COM B1-e) is
  open.** The single row says the opposite of the bound's premise at R04–R06: the one near-pass found comes from the
  softest parents, through repeated crossings, not from a stiff configuration.

### 3.6 Flagged events (T8)

Flagged events (n_early_prod > 0 at β_min = 0.1): NI 22 10, NI 30 15, NI 61.5 18, NI-X 212, NI-C 59, hs 38, lowpt 4
(356; = TOV l.24, HED), DIF and DIF-C 0. **No flagged event carries a stored row in any reading, width, s or pool:**
WITH − WITHOUT = 0 in all 120 pairs of count tables of each pool (m and u); the two variants differ only through M of five empty terms.

## 4. The open choices: what the frozen text fixes, the counts under every reading, and what the text points to

I choose none of them. "Points to" is my reading of the plan's text, flagged for the advisor call that the ruling of
23 Nov requires before any of these is fixed. Counts: Z(νν) full class at R08 = R09 = R11, s = 0, unless stated.

### 4.1 Reading S3: "the ribbon … of the width of r" — w_core (a MAD) or a hard window [NOT fixed, ruling of 23 Nov]
- **Text.** STR l.756-757: "a width-only pass over those hits finds the ribbon through the PV in the road, of the width
  of r, that holds the most double-crossing layers"; STR l.776 (table of cuts): "core width w_core (R05–R08) | yes: the
  widest-holding ribbon of a superset of hits is at least as good | applied in the classes"; STR l.769: "the term's own
  hits of an attributed candidate lie inside its ribbon and make at least n − k_max of its layers, so the event is in
  a class k ≤ k_max by the subset definition, whatever the finder chose without pile-up"; STR l.788: "H classified on
  all own hits is then a true ceiling for every cut of the table".
- **Counts.** w_core < W (BASE): **1,501 (S) / 1,474 (F)**. Hard window of full width 2W/1.4826 (HARD): **138 / 138**
  (Nils: 137, lower bound of his search). R07: 3,781 / 568. s = 3 at R08: 969 / 151.
- **A fact the text's own argument can be tested on (T7b; post hoc: computed after the counts were known).** Of the
  749 events at R08 whose counted witness is a
  full set judged exactly as the finder judges a candidate (c0: the finder's plane fit, its axis, its w_core < 4.7 mm,
  k ≤ 3), **615 have no hard-window witness with k ≤ 3** (R07: 1,809 of 2,368). A candidate the finder would pass at
  the rung's w_core cut is therefore, in most cases, not inside a hard window of that width.
- **Points to: no clear pointer** (v1: "w_core, MEDIUM-HIGH"; lowered on review B-2). Each reading satisfies one half
  of the text's argument. *For w_core:* it is the finder's variable and the rung variable named in STR l.776, and the
  ceiling property of l.769 and l.788 ("whatever the finder chose") needs every set the finder can pass at the rung
  to be in a class; with the hard window 615 of 749 finder-type sets at R08 would be outside every class. *For the
  hard window:* the argument of STR l.769 runs from a candidate found **with** pile-up to its own-hit subset ("the
  term's own hits … lie inside its ribbon"), and STR l.776 ("the widest-holding ribbon of a superset of hits is at
  least as good") is literally true for a geometric window but not for a MAD: the own hits of a set with w_core < W
  can have w_core > W, and added hits can push w_core up (NIL §3, the two T7 trials); the hard window is therefore
  the reading under which STR l.769 and l.776 hold as written, and "ribbon … of the width of r" reads geometrically.
  The 615-of-749 statistic is **post-hoc evidence**: it was computed after the counts were known and argues for the
  reading that gives the larger, already quoted number. The hard window is the more restrictive reading (strict side
  for a pass verdict, lenient for a ceiling). The verdict "above" holds under both (138 counts → B₅₀ 5,947 at R09,
  §6). CONFIDENCE: none given (no pointer). FLAG FOR HUMAN: YES (factor 10.9 in m).

### 4.2 Axis convention: full set with the finder's axis, subsets with their own [NOT fixed, ruling of 23 Nov]
- **Text.** Nothing in STR l.755-778 names an axis; "ribbons inside road and barrel" (l.777) need one for the
  alignment cuts, and w_core is defined on u·n₂, which depends on it.
- **Counts.** As coded in Phase 2 (BASE; mixed): 1,501 / 1,474. One own-axis convention for every set (OWN):
  **1,449 / 1,420** (Nils's own-axis search: ≥ 1,419, and "at most 74 of the 1,501 rest on a witness that holds only
  under the finder's axis"; mine: 77 of the 1,501 BASE events have no own-axis witness with k ≤ 3, and 25 events are
  counted only by my additional searches, T7b and UNION 1,526). R07: 3,781 / 3,613. At "no width" 975 of 13,923 full sets
  fail under their own axis.
- **Points to: no clear pointer.** The finder's convention applied to each set is the mixed one for a full set (its
  stored axis is how `cand_vars` computes w_core and the alignment of every finder candidate) and the own axis for a
  subset (the refit's rule for a hit set); that is what BASE does, and it is the only convention under which a finder
  candidate is always in a class (same argument as §4.1). A single own-axis rule is simpler to state. Effect on m:
  −3.5 % (S). CONFIDENCE: LOW-MEDIUM. FLAG FOR HUMAN: YES.

### 4.3 Search inside a plane: the code's heuristic against PLAN S4 as written [Nils §1 row 6; deviation recorded 23 Nov]
- **Text.** CEC l.47-50 (PLAN S4): "the full hit set first (the finder's choice); else for every window centre (each IP
  hit and each midpoint of neighbours) the hits inside ±W/1.4826, then layers completed with outside hits, cheapest
  layer first … Every subset found is a witness; the search is not proven maximal". The code (`p2w_subset.py`
  l.232-267): 7 window centres at steps of h/2 around the median, for the plane's axis and for an axis along each IP
  hit. STR fixes no search; it defines a maximum ("holds the most double-crossing layers").
- **Counts.** Code as run (BASE): 1,501 / 1,474. PLAN S4 centres as written, plane's axis (PLANS4): **1,378 / 1,349**.
  Both, with every own-axis search (UNION): 1,526 / 1,500. R07: 3,781 / 3,531 / 3,804.
- **Points to:** the definition is the maximum, so every search gives a lower bound and the largest valid count is
  the closest to the text; the heuristic of the code counts 123 more events (net) than the centres S4 describes and misses
  25 that the other searches find. None is the frozen number: the ruling of 23 Nov keeps 1,501 / 1,474 "as produced",
  with 1,526 / 1,500 as information of the same kind as Nils's 1,610 (his union used a search of his own; mine uses
  only searches inside the classifier's planes). The verdict "above" does not depend on it.

### 4.4 The width at R04 (and FB(0)): "the finder's maximum core width" [Nils §1 row 7; deviation recorded 23 Nov]
- **Text.** STR l.760-762: "At the counting rungs R01–R04, where the ladder has no width cut yet, the width is the
  finder's maximum core width (frozen configuration, transcribed in Phase 2)". The frozen configuration has one width:
  `w_c_mm = 75.0` (`acts/stage4/frozen_inputs.json`), the half-width of the finder's collection window |u·n₂| < W_c. No
  Phase-2 document transcribes a "maximum core width" (grep of `phase2_exploration/outputs`, `COMMITMENTS.md`, `LOG.md`).
- **Readings and counts** (Z full class; S / F): (A) w_core < 75 mm, the coding of Tove and Björn (BJO l.75-77):
  **R04 13,915 / 13,524; FB(0) 7,046 / 6,641**. (B) collection window only, no cut on w_core (Cecilie's code; w_core can
  reach 1.4826 × 75 = 111 mm): **13,923 / 13,532; 7,052 / 6,645**. Difference 8 events at s = 0, 6 at s = 3 (0.06–0.09 %).
- **Points to: (A)**, weakly: a "maximum core width" from the frozen configuration can only be W_c, used as the width
  W of the rung; (B) is what "no width cut yet" would give without the sentence. The R04 column of Phase 2 (ING l.48)
  is reading (B); **any R04 or FB(0) number quoted from Phase 2 carries the label "no width cut (deviation from STR
  l.761-763)"**; this document gives both. FB(0) is a T2 candidate for the hypotheses with k_adm = 0, so PREREG_v2
  must state the reading. CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES (text needs a transcription; effect < 0.1 %).

### 4.5 N_IT2 ≥ 3: part of k_IP (S) or required of the subset (F) [reading S5]
- **Text.** STR l.758-759: "the fixed cut N_IT2 ≥ 3 is a cut on a subset of the IP layers and is part of k_IP".
- **Counts.** S 1,501, F 1,474 (−1.8 %); at s = 3: 969 / 846 (−12.7 %); FB(0): 7,046 / 6,641.
- **Points to: S** (the quoted sentence; NIL l.45-47 shows that at n_IP = 7 a missing IT layer is a missing IP layer, so
  (S) is not a loose reading at s = 0). At s = 3 the difference is larger because k_max = 5 admits subsets with one or
  two IT layers. Both are carried everywhere.

### 4.6 Hit merging before the finder [EXP §10 item 10; BJO D3]
- **Text.** STR, ADD and COM do not mention the merging of hits for the own-hit classification (grep "merg": only
  v1's "merged clusters … not modelled [L8]"). STR l.744-745: "The finder therefore sees the same detector model as
  everywhere else"; STR l.755: "classified on subsets of the term's own hits". The frozen v1 chain builds the finder's
  pool as "the hit pool after CKF removal, analysis-level merging and the hit-time window" (`chain_inputs.py` l.5-18,
  WP_RULE §1.1; sha256 in `frozen_inputs.json`): two measurements on one sensor merge when their truth positions are
  closer than one pitch in both directions.
- **Counts** (all 1,083 files reclassified without `merge_pool`; T6, T7). Merged (label m): 1,501 / 1,474. **Not
  merged (label u): 1,516 / 1,486** (+1.0 %). Paired: every merged-pool event is also counted unmerged; 15 more appear.
  R07 3,781 → 3,795; R14-type 969 → 979; FB(0, 75 mm) 7,046 → 7,059 (4 lost, 17 gained). B1, hs, lowpt: 0 in both;
  the DIF-C row unchanged.
- **Points to: merged.** The plan asks for "the same detector model as everywhere else", and everywhere else the
  finder's input is the merged pool; a ceiling for the finder with pile-up must be counted on hits as the finder
  receives them. Against: "the term's own hits" could be read as the raw hits, and merging removes close pairs, the
  dominant topology (BJO D3), so unmerged is the strict side for a ceiling: +1.0 %, measured.
  CONFIDENCE: MEDIUM-HIGH. FLAG FOR HUMAN: NO (1 %; to be stated in PREREG_v2).

### 4.7 The primary vertex of the Z(νν) pilot events [EXP §10 item 10; TOV A5]
- **Text.** STR l.757: "the ribbon through the PV"; nothing on how the PV of a pilot event is obtained. v1's convention
  (`g1b_tt.py` l.42, l.91, "plan §1.7"): PV = true vertex + N(0, (10, 10, 15) µm). The B1 files store their own PV draw
  (ADD l.502). R-8 (PV identification efficiency, STR l.2152) is a separate factor, not in H.
- **Counts** (460 Z files; T6, T7). PV draw of Phase 2 (label m): 1,501 / 1,474. **True vertex (pv0): 1,510 / 1,482**
  (+0.6 %); 1,409 events in both, 92 only with the draw, 101 only with the true vertex. Another seed of the same draw,
  on every 4th file (pv2): 361 against 358 for label m on the same 115 files; 326 in both, 32 / 35 only in one. R07:
  3,781 / 3,775; R14-type: 969 / 948 (−2.2 %); FB(0, 75 mm): 7,046 / 7,059.
- **Reading of the numbers.** About 6–9 % of the counted events change with a 10–15 µm shift of the PV (the plane
  tolerance is 30 µm), in both directions; the net change is within ±2.2 % at every T2 candidate, the size of the
  Poisson error of the count (√1,501 = 39). The seed of the draw is a noise of that size, not a reading.
- **Points to: the draw** (v1's convention, the one every other sample of the chain uses; a true vertex is not what
  the finder is given anywhere else). CONFIDENCE: MEDIUM-HIGH. FLAG FOR HUMAN: NO.

### 4.8 M of the Z term [EXP §10 item 10, §12 item 5; TOV A4]
- **Text.** ADD l.358: "M = 1.011×10⁶" (a planning value); ADD l.607: "the H per full-weight event of the Z(νν) pilot
  (M = Σw/w_max; 1.011×10⁶ with v1's weights, replaced by the day-12 MET model)". The definition is fixed; the number
  is whatever the definition gives on the files.
- **Value.** Σw/w_max = **993,885.9** from the unrounded weights (my jobs: 974,008.2056 / 0.98; = Björn, = Ylva's
  single M; Tove's 993,887.3 came from rounded weights). 41.96 events per Z count; 2.14 per count of the 0.05 class.
  With the planned 1,011,080 every Z-term number is 1.7 % lower (YLV §3 item 4: 62,095 / 60,982 at R09) [UNVERIFIED
  by me]. Weighted m (Σw_pass/w_max; BJO D4): 1,500.17 instead of 1,501 at R08 (−0.055 %), 3,778.9 instead of 3,781 at R07.
- **Points to: the measured 993,885.9** (the text defines M; 1.011×10⁶ was its estimate before the files existed).
  **Open, and not mine to close:** the same sentence replaces the v1 weights by the MET model of day 12 (§8 item 1).

### 4.9 The best-candidate rule (lowest G) [EXP §10 item 10; TOV A3; ruling (iii)]
- **Text.** STR l.2753-2754: "B₅₀ is read at the best candidate: the candidate with the lowest G (§4.12 rule 3),
  computed before the freeze with v1 placeholder efficiencies and this projected background (§4.12 rule 4)". Ruling
  (iii) (LOG 19 Nov 15:24): "if G is unavailable, at every T2 candidate, and they must agree".
- **Status.** G is not computed here: it needs the T1 likelihood builder and the T2 script on the 16 candidates
  (wave 2 of Phase 3). §6 gives the projection at **every** T2 candidate, FB(k) for every k_adm; they agree ("above").
- **Points to:** G at the binding reading if the T2 script exists by then, else ruling (iii). With the present
  counts the choice cannot change the verdict: the smallest projection over all candidates, readings and variants **on
  a full sample** is above the limit by a factor 16 (HARD) to 110 (every other reading); including the 115-file
  PV-seed subsample the factors are 12 and 96 [VERIFIED by Sindre, `D`], §6.

### 4.10 A pile-up estimate for the N_2S2 ≥ 3 candidates [EXP §10 item 10; TOV A3]
- **Text.** STR l.1015-1016: "There is no v1 number for the 2S step; R14 is at most the R11 value"; widths (STR §4.0
  point 7; `strategy_budget.py` l.680): R11 1.29, R14 2.47. STR l.2738-2741: at day 15 the pile-up term is "the
  development model's R04–R07 inputs" (p3-b). ADD l.599-600: "the pile-up term is the present chain's estimate".
  FB(k): no pile-up number anywhere in STR, ADD or COM.
- **Readings used in the dry run** (§6): (i) no pile-up term (a lower bound of B; valid for "above" only); (ii) the R11
  value as an upper value for R14 = R17 = R20 and FB(4) (medians 0.48–0.81 events, width 2.47, capped by the
  no-credit draw 425.5 × Exp(1)); FB(0)–FB(3): (i) only. The binding run takes the rows p3-b delivers.
- **Points to:** (ii) for R14-type candidates is the frozen sentence; for FB(k < 4) the text gives nothing and the
  occupancy model must supply it. The pile-up term is < 0.02 % of the projection at these candidates either way.

### 4.11 The flagged-event variant [EXP §10 item 6]
- **Text.** ADD §3 P6 (vi), release condition: "by a per-event flag that removes such events from the count m and
  reports their number, or by a higher β cut". COM l.322 (D9, approved): "the slow-fragment residue handled by keeping
  the β cut at 0.1 and flagging the affected events". Advisor ruling (LOG 18 Nov 11:03): "PREREG_v2 fixes … the binding
  variant … (recommended: WITH flagged events binding, WITHOUT as cross-check)".
- **Note for the PREREG drafter:** the addendum's sentence says the flag *removes* the events from m (that is WITHOUT),
  the ruling recommends WITH as binding. The two texts do not say the same thing; I do not resolve it.
- **Counts.** Identical: no flagged event has a stored row in any reading (§3.6); B₅₀ WITH − WITHOUT ≤ 0.009 events.

## 5. Nils's conditions (review of 23 Nov) and the ruling's items, one by one

1. *"Lower bound, 'above' only."* Carried on every count of this document (§2 item 5, §3.1). The non-maximality is
   visible in my own columns: UNION − BASE = 25 events at R08 (S), 201 width-non-monotone BASE rows (§1, C2).
2. *"The count depends on two readings … both go into the day-15 text."* §4.1 (S3: 1,501 against 138) and §4.2 (axis:
   1,501 against 1,449), with a count under each at every T2 candidate (§3.1) and a dry-run projection under each (§6).
3. *"Quote 1,501 (S) / 1,474 (F) as produced."* Done; reproduced row by row (C1). My other columns are labelled
   readings, not replacements.
4. *"R04–R07 and s = 3 (969 / 846) read, not re-derived."* Two checks, both with code that neither Cecilie nor I wrote:
   - **Independent search** (`I`, T11; Nils's `search_event` and `verify` unchanged, W passed as argument; every 2nd
     pilot file, 230 files, 7,309 full-class row events). Fraction of the counted events confirmed by a verified
     witness of his search with k ≤ k_max, reading S (at s = 0 reading F is within 0.5 points, R08 94.2 % against 94.7 %; at s = 3 it is not: F is higher,
     R08 76.3 % (309 of 405) against 70.4 %, R04 80.4 % against 77.3 % [VERIFIED, `I`]): **s = 0: R04 93.1 % (6,495 of 6,977),
     R05 92.8 %, R06 93.9 %, R07 94.9 % (1,795 of 1,892), R08 94.7 % (699 of 738; his own run: 1,419 of 1,501 =
     94.5 %)**. The widths he did not cover behave as the one he did. **s = 3: R04 77.3 %, R05 77.7 %, R06 77.2 %,
     R07 74.5 %, R08 70.4 % (330 of 469).** His search keeps planes with N_IP2 ≥ 4 only and minimises k_IP only, so
     an s = 3 row that needs k_IP ≥ 4 is outside its reach: of the 139 not found at R08, 98 are such rows and 41 are
     in reach (R07: 167 / 115; R04: 332 / 464). Within reach the confirmed fraction at s = 3 is 89 % at R08 (330 of
     371) and 85–89 % at R04–R07. 0 witnesses of his search with k ≤ 3 were rejected by his verifier.
   - **The classifier's own witnesses under his verifier** (`W`): every 12th pilot file (39 files), every full-class
     row counted in UNION (S), every width at which it is counted; the witness of the unchanged classifier is given
     to Nils's verifier. **Own-axis subset witnesses: 432 checked (R05 65, R06 147, R07 150, R08 69, R04 1), 432
     accepted, 0 rejected**: 415 with a plane normal re-fitted on the witness hits, and the other 17 (all "3σ
     membership" with the re-fitted normal) with the normal of the classifier's own plane, recovered by repeating its
     seed loop (`p3a_witness_resolve.json`: 17 of 17) [VERIFIED]. For those 17 the plane is the classifier's own, so the check
     there tests the verifier's cuts, not the plane search; this is valid because the definition is existential (a
     plane exists) (review C-5). **Full-set witnesses** (the plane's whole hit set
     judged with the finder's axis, the Phase-2 branch Nils reviewed by reading): 3,968 checked over the six widths
     (R08: 48, R07: 175); the own-axis verifier with a re-fitted normal also accepts 3,245 of them (R08: 37 of 48;
     R07: 132 of 175); the other 723 hold under the convention they were counted with (finder's axis and normal) and
     were not re-verified under it by independent code at these widths (at R08 Nils did: 136 of 136). At s = 3 the
     stored witness (chosen for s = 0) also gives k ≤ 5 in 1,743 of 2,307 cases (R08: 53 of 71); for the rest the
     s = 3 pass comes from another subset of the event, which is not stored and was not verified.
     One change after a first look, recorded: the first version used an unweighted re-fitted normal and "failed" 43
     of 62 witnesses on a 2-file smoke test for plane membership; that was the fit, not the witnesses (the weighted
     fit and the kernel's own normal accept them). The final file set (39 files) is not the smoke-test set.
   - Not done: a re-derivation of the s = 3 rows with k_IP ≥ 4 by an independent *search* (none exists that looks at
     planes with N_IP2 < 4); the second half of the files (≈ 0.74 CPU-h, `cpu_s_in_jobs` ind; 8.7 CPU-h of the budget
     were left; review C-4 recommends running it before the binding text is written: an orchestrator decision).
5. *"R04 has no width cut although STR l.761-763 requires the finder's maximum core width."* §4.4: counted both ways,
   8 events of 13,923 apart; FB(0) identified as the T2 candidate it touches.
6. *"The search heuristic differs from PLAN S4 (lowering only)."* §4.3: PLAN S4's centres coded as written give 1,378
   against 1,501; "lowering only" is confirmed in the sense that the code's heuristic finds more than the described
   one, and both are lower bounds (UNION 1,526).
7. *B1 / hs / lowpt zeros: "none found by a non-maximal search; not an upper statement".* Wording used throughout;
   additionally the zeros hold in all five readings and in both pools, and the B1 branch of my driver reproduces the
   one Phase-2 row exactly.
8. *"The combined 1,610 is information only."* Not re-derived (it needs his full search on every row event); my
   UNION (1,526) is the analogous number from searches inside the classifier's planes.

## 6. Dry run of the rule-1 projection — **NOT BINDING**

`p3a_rule1_dryrun.py` → `D`. Arithmetic: `p2t_rule1_prelim.reading` (Tove's, reviewed by Björn and re-derived by Ylva)
copied with N_t and the pile-up rows as arguments; constants, N_t and random streams of the approved
`p2z_addendum1.py` imported unchanged; 10⁵ draws; limit 299.1; single M = 993,885.9. Checks C3 pass first.
**Why it is not binding:** (1) the pile-up term is the v1-based EST rows, not the development occupancy model (p3-b);
(2) the three MET additions are at their planning N_trig (Z(ττ) 426,340; lost-lepton Z(ℓℓ) 29,844; multijets 400,000;
N_t(Z term) = 41,704,632), not at the MET model's (p3-c); (3) the Z weights and the road axis are v1's, and the `pilot.c0.hs` parents were drawn by w_v1 inside the v1
road (§8 item 1; these counts cannot enter a binding reading until the orchestrator, after an advisor call, rules on
that item, (i) or (ii));
(4) the binding reading has its own advisor call.

| T2 candidate | pile-up row (EST) | **BASE** m_Z S / F | **B₅₀ BASE (S)** [16–84 %] | B₅₀ BASE (F) | B₅₀ OWN (S) | B₅₀ PLANS4 (S) | B₅₀ HARD (S) | ≥ 299.1 in every reading |
|---|---|---|---|---|---|---|---|---|
| R07 | v1 direct count 35 / 48,000 trials, read as N_trig/48,000 × Gamma(36) (median 3.0×10⁴); reading by Aurora, no approved row | 3,781 / 3,668 | 189,341 [183,888–195,218] | 184,596 | 182,285 | 178,840 | 54,409 | yes |
| R08 | 88 / 118 / 148 (s_tot 0.43) | 1,501 / 1,474 | 63,246 / 63,271 / 63,294 | 62,113 / 62,138 / 62,161 | 61,064 / 61,089 / 61,112 | 58,081 / 58,106 / 58,128 | 6,024 / 6,048 / 6,070 | yes |
| **R09** | 6.74 (s_tot 0.59) | 1,501 / 1,474 | **63,170** [61,578–64,802] | **62,037** | 60,988 | 58,004 | 5,947 | yes |
| R11 | 0.48–0.81 (s_tot 1.29); reading by Aurora, no approved row | 1,501 / 1,474 | 63,163–63,164 | 62,030–62,031 | 60,981–60,982 | 57,998 | 5,940–5,941 | yes |
| R14 = R17 = R20, FB(4) (s = 3; m re-derived in part ᵃ) | none; or ≤ R11 value (s_tot 2.47); reading by Aurora, no approved row | 969 / 846 | 40,836; 40,842–40,846 | 35,669; 35,675–35,678 | 39,871 | 39,829 | 6,488 | yes |
| FB(3) | none (lower bound) | 2,212 / 1,964 | 93,021 | 82,605 | 87,522 | 90,417 | 17,359 | yes |
| FB(2) | none (lower bound) | 4,113 / 3,802 | 172,829 | 159,764 | 161,412 | 169,556 | 50,202 | yes |
| FB(1) | none (lower bound) | 6,224 / 5,870 | 261,450 | 246,573 | 241,001 | 260,775 | 120,193 | yes |
| FB(0), 75 mm / window only | none (lower bound) | 7,046 / 6,641; 7,052 / 6,645 | 295,947; 296,198 | 278,931; 279,099 | 267,823; 267,697 | 295,947; 296,198 | 225,475; 267,697 | yes |

(ᵃ s = 3 rows, R14-type and FB(0)–FB(4): the m_Z they use is re-derived only in part, 70.4–77.7 % (S) confirmed by Nils's
search, none for k_IP ≥ 4; §3.1.)
(B₅₀ values VERIFIED as arithmetic, ESTIMATE as physics; full table T12 and `D`. The R09 and R08 rows for BASE equal
Ingvild's 63,170 / 62,037 and 63,246 / 63,271 / 63,294, with Ylva's M: the change of M moves them by +0.09 events.)

- **1,440 projections** (4 labels × 5 readings × S / F × 11 candidate rows × their pile-up rows × WITH / WITHOUT):
  **all at or above 299.1.** Smallest: 3,610 (HARD, F, FB(4), no pile-up term, the 115-file PV-seed subsample);
  smallest on a full sample 4,726 (HARD, F, FB(4), unmerged pool); smallest outside HARD on a full sample 33,274 (OWN, F,
  FB(4), true PV); including the 115-file subsample 28,823 (PLANS4, F, R14-type, pv2) [VERIFIED by Sindre, `D`]. Smallest single draw of the BASE (S) R09 reading: 55,082. Monte-Carlo error of the median 6 events; three
  other seeds 63,171–63,180.
- Term medians at R09, BASE (S): Z 63,014; Z 0.05 class 29; DIF 18.0, DIF-C 16.6, NI-X 16.2, NI-C 16.9, NI 22 / 30 /
  61.5 3.3 / 4.5 / 4.4, hs 2.8 (zero-count floors); pile-up 6.7. **The Z term is 99.75 % of the reading.**
- Variants at R09, BASE (S): unmerged 63,801; true PV 63,543; other PV seed (115 files, own M) 60,921 ± 3,200 (Poisson
  on 361 counts) [the last ESTIMATE of its error].
- WITH against WITHOUT flagged events: |ΔB₅₀| ≤ 0.009 events.
- **What would have to change for a reading at or below 299.1:** m_Z ≤ 3 at R09 (ADD §4.1: pause at 4). The smallest
  count at any T2 candidate in any reading on a full sample is 109 (HARD, F, s = 3, unmerged pool).

**How the dry run is repeated with other pile-up rows and N_trig (inputs swapped by path, no code change).** This
alone is **not** the binding run: the Z(νν) weights and road axis and the `pilot.c0.hs` sample depend on v1's MET
(§8 item 1, to be ruled by the orchestrator after an advisor call). Inputs: `outputs/p3a/inputs/pileup_rows.json`
(replace `rows` by the development model's per candidate: `type`, `median`, `s_tot`, `cap_mean`; keys as in the file,
or new keys plus an edit of the candidate table `CANDS` at the top of the script), `outputs/p3a/inputs/met_ntrig.json`
(`n_trig` of the three additions), then
`<tt python> src/p3a/p3a_rule1_dryrun.py outputs/p3a/p3a_counts.json <out.json> --tag "<text>"` on a worker (≈ 1 CPU-min).
`z_weights.json` has `mode: "v1"` only: a v2 weight needs a new classification pass first (§8 item 1; the script stops
with a message if the mode is changed).

## 7. The numbers that feed decision point 2 (STR §11.7), in one table

None of these numbers enters a binding reading until the orchestrator, after an advisor call, rules on §8 item 1 (the
orchestrator's item 9: (i) v1's preselection and axis, or (ii) a new pass with the MET-model weights and axis,
with regeneration of `pilot.c0.hs`).

| input of decision point 2 | value | tag | where |
|---|---|---|---|
| m_H, Z(νν) (all SM hard scatter + multijets), R08 = R09 = R11 | **1,501 (S) / 1,474 (F)**, as produced, exact or lower bound, "above" only | VERIFIED | §3.1; `T` `m_H` |
| the same under the readings not fixed: own axis / PLAN-S4 search / hard window / union | 1,449 / 1,378 / 138 / 1,526 (S) | VERIFIED | §4.1–4.3 |
| m_H, Z(νν), R07 | 3,781 / 3,668 (HARD 568) | VERIFIED | §3.1 |
| m_H, Z(νν), R14 = R17 = R20 = FB(4) (s = 3) | 969 / 846 (HARD 151 / 110) | VERIFIED as counted; **re-derived in part**: 70.4 % (S) / 76.3 % (F) confirmed by Nils's search on half the files, no independent search for k_IP ≥ 4 | §3.1, §5 |
| m_H, Z(νν), FB(3) / FB(2) / FB(1) / FB(0) (s = 3) | 2,212 / 4,113 / 6,224 / 7,046 or 7,052 (S) | VERIFIED as counted; **re-derived in part**: 74.5 / 77.2 / 77.7 / 77.3 % (S) confirmed by Nils's search on half the files, no independent search for k_IP ≥ 4 | §3.1, §4.4, §5 |
| m_H, Z 0.05 class, R08 | 13 / 13 | VERIFIED | §3.1 |
| m_H, DIF, DIF-C, NI 22 / 30 / 61.5, NI-X, NI-C, hs, lowpt, every T2 candidate | 0 (none found; not an upper statement) | VERIFIED | §3.3 |
| M (Z term) | 993,885.9 (v1 weights) | VERIFIED | §4.8 |
| R06–R07 counts, Z(νν) | 7,202 / 3,781 (S); fall ×1.61 (R05→R06), ×1.90 (R06→R07), ×2.52 (R07→R08) | VERIFIED | §3.2 |
| R06–R07 counts, B1 classes | 0, 0 (DIF-C R06: 1 or 0, attribution open, both readings given, §3.3) | VERIFIED | §3.3 |
| enrichment 1/H(R06), Z(νν) | 138 (S) | VERIFIED | §3.5 |
| enrichment 1/H(R06), B1 classes | not measured (empty); ≥ 8.8×10⁵ … 3.5×10⁶ at 68 % | ESTIMATE (bound) | §3.5 |
| gains G_t | 1 (not measured; orientation factor 21 already in M) | — | §3.5 |
| frozen hand-over variant | ADD P6 per stream, as generated | VERIFIED (file meta) | §2, T10 |
| rule-1 projection B₅₀ | **NOT BINDING** (§8 item 1 not ruled): 63,170 (S) / 62,037 (F) at R09; 40,836 / 35,669 at R14-type (s = 3, m re-derived in part); ≥ 4,726 in every reading on a full sample | VERIFIED arithmetic, ESTIMATE physics | §6 |
| B₅₀ if the v2 MET model only adds weight on the v1 axis | ≥ ≈ 27,200 at R09 (Sindre's bound; covers neither weight lost nor an axis change) | ESTIMATE, Sindre (review A-1) | §8 item 1 |

## 8. Open issues, and what I stop on

1. **The v2 MET model changes more of the rule-1 input than its N_trig (stop-and-report item; nothing reworded by
   me).** ADD l.360-361: "'41' is provisional: it uses v1's preselection and is recomputed with the v2 MET model at
   day 12 from the generator-level summary stored with every event"; ADD l.607: M "replaced by the day-12 MET model".
   My brief swaps two inputs (pile-up rows, N_trig of the additions). The classification depends on v1's MET in two
   more ways: (a) the **weights** (which events are in the full-weight class, hence m and M); (b) the **road axis**:
   the road is |Δφ(n₃, MET)| < 0.15 around `phimet_reco_v1`, v1's reconstructed MET azimuth stored with each event.
   A MET model with another resolution moves the axis of every event and gives weight to events that have none now
   (1,297,459 of 2.3×10⁶). Then m_Z itself must be recounted, not only rescaled.
   *Phase 1 assumed* the pilot's count carries over and only the events-per-count is recomputed. *Phase 3 found* that
   the count is tied to v1's MET direction and preselection. *Implications:* the binding reading needs either (i) a
   statement that the rule-1 count is read on v1's preselection and axis (then only M's label changes), or (ii) one
   more classification pass with per-event (w, φ_MET) of the v2 model. For (ii) the code exists and is tested
   (`p3a_multi.py --variants v2 --met-dir <dir with <pilot stem>.met.npz holding 'w' and 'phimet'>`; with v1's values
   it reproduces variant m, 32 of 32 rows on a slice). **Campaign definition, not launched** (it needs p3-c's
   per-event output): the 115 jobs of `tools/runner/examples/p3a/p3-a-clsxz.json` with `--variants v2 --met-dir …`
   and the output `<id>.v2.npz`; cost ≈ 2.5 CPU-h if the selected events are as many and as busy as v1's, up to
   ≈ 12 CPU-h if most events get a weight [ESTIMATE: 8.3 ms per w_v1 > 0 event, 26 ms per w_v1 = 0 event measured on
   2,040 and 2,760 events; the w_v1 = 0 events hold 2.6 times more rows, because a jet near the MET axis is what
   fails v1's min-Δφ cut and it fills the road]. The verdict cannot plausibly change (m_Z would have to fall from
   1,501 to 3); the number can. I did not classify the w_v1 = 0 events on v1's axis: 9.4 CPU-h [ESTIMATE] for an
   input that would not be the one needed.
   **Added in v2 (review A-1, B-4).** (c) **`pilot.c0.hs` has the same dependence, and no reclassification pass can
   remove it:** its parents are drawn "INSIDE the road of their own event, |dphi(parent, phimet_reco_v1)| < 0.15" and
   in proportion to w_v1, "so events failing v1's preselection (w = 0) are never fired" (`p2a_hspool.py` l.14-17,
   l.57-59; ADD l.377-379). Under (ii) this sample must be regenerated (chain rerun), not re-read; **the ≈ 2.5–12
   CPU-h pass above covers the Z(νν) term only.** In the dry run `pilot.c0.hs` is a zero-count floor of 2.8 events, so
   it cannot move the verdict; it decides whether a reading binding on the v2 model is achievable at all.
   (d) **Status: the counts of this document cannot enter a binding reading until the orchestrator, after an advisor
   call, rules on this item** (the orchestrator's item 9): (i) or (ii), and what happens to `pilot.c0.hs` under each.
   Neither is chosen here. (e) **Sindre's bound** [ESTIMATE, Sindre, review A-1], needing no new pass: if the v2 model
   only adds weight on the v1 axis, the worst case is that all 2.3×10⁶ events are full-weight and no new event
   counts: 41.70×10⁶ / 2.3×10⁶ = 18.1 events per count, × 1,502 ≈ 27,200 events at R09, so B₅₀ ≥ ≈ 27,200. It does
   not cover events that lose weight, nor an axis change; for those there is no bound, only the size of the gap
   (m_Z would have to fall from 1,501 to 3).
2. **Conventions to be fixed in PREREG_v2 with their own advisor call** (ruling of 23 Nov): S3 (§4.1), axis (§4.2),
   search (§4.3), R04 width (§4.4), merging (§4.6), PV (§4.7), flagged variant (§4.11, with the wording conflict noted
   there), whether m is weighted (§4.8), and whether a parent-only witness counts for a B1 term (§3.3: both readings, m = 0 or 1, and the frozen texts
   for each, ADD l.603-605 and l.257-258 and STR l.748-749 among them). Each must
   carry "fixed after the pilot count was seen, verdict the same under both".
3. **G_t not measured; the sagitta bound of COM B1-e not written** (§3.5). The B1 development work package needs to
   know that the pilot gives no enrichment for DIF or NI at R06 and that the only near-pass is a looping parent.
4. **The DIF-C row is a looper**, visible only where option (a) restored the parent's later arcs. It is one event at
   R04–R06; it is direct evidence that repeated crossings by one soft particle make near-pass configurations, which
   every other sample of the chain cannot contain ([L15]). No count at a T2 candidate; a sentence for [L15].
5. **Independent re-derivation is partial at s = 3** (rows needing k_IP ≥ 4 are outside the reach of Nils's search)
   and covers half of the files (§5 item 4). Every s = 3 row of §0, §3.1 and §7 now carries this label (70.4–77.7 % (S)
   confirmed; none for k_IP ≥ 4). Running the second half (≈ 0.74 CPU-h) before the binding text is written is
   recommended by review C-4; not run in v2 (no new jobs).
6. **G / best candidate** not available (§4.9); **pile-up rows for FB(k < 4)** do not exist in any frozen text (§4.10).
7. **Runner behaviour worth knowing:** the SSH driver fixes its slot count from the 1-minute load at launch (a cap of
   2 instead of 3 when started within a minute of a finished campaign) and re-dispatches a killed job as attempt 2.
   My own error: two "stop" commands killed their own ssh shell (pkill pattern matching itself), so the first campaign
   ran 15 minutes longer than I thought; cost ≈ 0.2 CPU-h, no output affected (session log, 11:59).
8. `qv2run rebuild-ledger` not run by me. Nothing of mine is running; slot released in `SLOTS.md`. The orchestrator
   should rebuild the ledger before the CPU total is quoted: ≈ 1.0 CPU-h is outside the ledger, and a fourth process
   ran beside three jobs at 12:00 (self-reported; review C-8).

## 9. Self-check

Against `agents/executor.md` and `phase3_selection/CLAUDE.md`:
- Plan before code: yes (session log, 10:16; first job 10:37). Session log and `experiment_log.md` kept as I went.
- Frozen criteria quoted, not reworded; no convention chosen after seeing the count: every open choice of §4 has a
  count under each reading and no reading is selected; "points to" statements are labelled as mine and flagged.
- Stop-and-report: §8 item 1 (a frozen sentence, ADD l.607, cannot be applied by swapping the two inputs my brief
  names); reported here and in the final report, not repaired.
- Anti-fabrication: no parameter tuned. The witness target, the widths, the categories, the stride of the independent
  search and of the witness check were fixed before the corresponding outputs were read. One change after a first
  look is recorded: the witness check's plane normal (first unweighted, then the verifier's own weighting; §5), made
  on a 2-file smoke test and applied to a different, larger file set.
- Formulas: k = (7 − N_IP2) + max(0, s − N_2S2), k_max = ⌊(7 + s)/2⌋ (STR l.757-760; limiting case: a full two-track
  plane gives k = 0 at every width, test T1; removed layers give the exact k, test T2). H = Gamma(m + 1)/M (STR
  l.2731); B = Σ_t (N_t/M_t) Gamma(m_t + 1) + pile-up (STR l.2730-2757), checked by the empty-pilot reproduction and
  by the closed form of YLV part D (Z term 41.9612 × 1,502 = 63,025.7 against my Z-term median 63,014 and mean-based
  total 63,169 against 63,170). E = 1/H(R06) = M/(m + 1): 993,885.9/7,203 = 138.0. Falls are count ratios.
- No algebraic circularity: m comes from pilot hits only; N_t and the pile-up rows from the approved Phase-1/2 script;
  M from the stored weights. The regression against Phase 2 is a reproducibility check (same classifier imported),
  not an independent validation, and is not presented as one; the independent parts are §5 item 4.
- Blinding: no signal file opened (the scripts read `pilot/`, `p2c/rule1_valid/` and their own outputs only); no
  efficiency formed.
- Figures: none (tables only); nothing to lint. JFC items "≥ 2 selection approaches", MVA, cutflow, closure tests,
  variable quality gate: not this work package (T2 and the consolidation).
- Every number tagged; no constant from memory (constants are imported from `p2z_addendum1.py`,
  `strategy_budget.py`, `frozen_inputs.json` or quoted with file and line).
- Not done / limits: §8. The UNION and "points to" columns are information, not results.

## Appendix: generated tables (`outputs/p3a/p3a_tables.md`, written by `src/p3a/p3a_tables.py`)

### T1. Ceiling counts m_H per term at every T2 candidate (label m: merged pool, PV draw; WITH flagged events)

| T2 candidate (width, s) | reading | Z full class (S / F) | Z 0.05 class (S / F) | DIF | DIFC | NI22 | NI30 | NI61 | NIX | NIC | HS | LOWPT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R07 (R07, s = 0) | BASE | 3,781 / 3,668 | 36 / 35 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R07 (R07, s = 0) | PLANS4 | 3,531 / 3,422 | 32 / 31 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R07 (R07, s = 0) | OWN | 3,613 / 3,512 | 34 / 34 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R07 (R07, s = 0) | HARD | 568 / 565 | 8 / 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R07 (R07, s = 0) | UNION | 3,804 / 3,692 | 36 / 35 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R08 = R09 = R11 (R08, s = 0) | BASE | 1,501 / 1,474 | 13 / 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R08 = R09 = R11 (R08, s = 0) | PLANS4 | 1,378 / 1,349 | 11 / 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R08 = R09 = R11 (R08, s = 0) | OWN | 1,449 / 1,420 | 13 / 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R08 = R09 = R11 (R08, s = 0) | HARD | 138 / 138 | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R08 = R09 = R11 (R08, s = 0) | UNION | 1,526 / 1,500 | 13 / 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R14 = R17 = R20 = FB(4) (R08, s = 3) | BASE | 969 / 846 | 12 / 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R14 = R17 = R20 = FB(4) (R08, s = 3) | PLANS4 | 945 / 816 | 12 / 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R14 = R17 = R20 = FB(4) (R08, s = 3) | OWN | 946 / 814 | 12 / 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R14 = R17 = R20 = FB(4) (R08, s = 3) | HARD | 151 / 110 | 1 / 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R14 = R17 = R20 = FB(4) (R08, s = 3) | UNION | 995 / 865 | 12 / 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width none (R04n, s = 3) | BASE | 7,052 / 6,645 | 65 / 54 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width none (R04n, s = 3) | PLANS4 | 7,052 / 6,645 | 65 / 54 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width none (R04n, s = 3) | OWN | 6,373 / 6,025 | 60 / 52 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width none (R04n, s = 3) | HARD | 6,373 / 6,025 | 60 / 52 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width none (R04n, s = 3) | UNION | 7,052 / 6,645 | 65 / 54 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width 75 mm (R04w, s = 3) | BASE | 7,046 / 6,641 | 65 / 54 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width 75 mm (R04w, s = 3) | PLANS4 | 7,046 / 6,641 | 65 / 54 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width 75 mm (R04w, s = 3) | OWN | 6,376 / 6,033 | 60 / 52 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width 75 mm (R04w, s = 3) | HARD | 5,367 / 5,076 | 56 / 48 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(0), width 75 mm (R04w, s = 3) | UNION | 7,046 / 6,641 | 65 / 54 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(1) (R05, s = 3) | BASE | 6,224 / 5,870 | 62 / 51 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(1) (R05, s = 3) | PLANS4 | 6,208 / 5,854 | 61 / 50 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(1) (R05, s = 3) | OWN | 5,737 / 5,427 | 56 / 48 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(1) (R05, s = 3) | HARD | 2,859 / 2,690 | 35 / 29 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(1) (R05, s = 3) | UNION | 6,231 / 5,877 | 62 / 51 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(2) (R06, s = 3) | BASE | 4,113 / 3,802 | 43 / 36 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(2) (R06, s = 3) | PLANS4 | 4,035 / 3,731 | 43 / 36 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(2) (R06, s = 3) | OWN | 3,841 / 3,564 | 41 / 34 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(2) (R06, s = 3) | HARD | 1,192 / 1,048 | 16 / 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(2) (R06, s = 3) | UNION | 4,119 / 3,809 | 43 / 36 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(3) (R07, s = 3) | BASE | 2,212 / 1,964 | 25 / 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(3) (R07, s = 3) | PLANS4 | 2,150 / 1,900 | 24 / 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(3) (R07, s = 3) | OWN | 2,081 / 1,846 | 24 / 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(3) (R07, s = 3) | HARD | 410 / 351 | 3 / 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FB(3) (R07, s = 3) | UNION | 2,235 / 1,982 | 25 / 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### T2. Z(nunu) full-weight class per width, s = 0 and s = 3, every reading (S / F); label m

| reading | s | R04n | R04w | R05 | R06 | R07 | R08 |
|---|---|---|---|---|---|---|---|
| BASE | 0 | 13,923 / 13,532 | 13,915 / 13,524 | 11,566 / 11,220 | 7,202 / 6,981 | 3,781 / 3,668 | 1,501 / 1,474 |
| BASE | 3 | 7,052 / 6,645 | 7,046 / 6,641 | 6,224 / 5,870 | 4,113 / 3,802 | 2,212 / 1,964 | 969 / 846 |
| PLANS4 | 0 | 13,923 / 13,532 | 13,915 / 13,524 | 11,520 / 11,173 | 7,019 / 6,798 | 3,531 / 3,422 | 1,378 / 1,349 |
| PLANS4 | 3 | 7,052 / 6,645 | 7,046 / 6,641 | 6,208 / 5,854 | 4,035 / 3,731 | 2,150 / 1,900 | 945 / 816 |
| OWN | 0 | 12,948 / 12,598 | 12,954 / 12,602 | 10,762 / 10,443 | 6,773 / 6,578 | 3,613 / 3,512 | 1,449 / 1,420 |
| OWN | 3 | 6,373 / 6,025 | 6,376 / 6,033 | 5,737 / 5,427 | 3,841 / 3,564 | 2,081 / 1,846 | 946 / 814 |
| HARD | 0 | 12,948 / 12,598 | 10,084 / 9,817 | 4,910 / 4,825 | 1,993 / 1,978 | 568 / 565 | 138 / 138 |
| HARD | 3 | 6,373 / 6,025 | 5,367 / 5,076 | 2,859 / 2,690 | 1,192 / 1,048 | 410 / 351 | 151 / 110 |
| UNION | 0 | 13,923 / 13,532 | 13,915 / 13,524 | 11,577 / 11,231 | 7,219 / 6,997 | 3,804 / 3,692 | 1,526 / 1,500 |
| UNION | 3 | 7,052 / 6,645 | 7,046 / 6,641 | 6,231 / 5,877 | 4,119 / 3,809 | 2,235 / 1,982 | 995 / 865 |

### T3. Fall per width step, Z(nunu) full class, s = 0 (count ratio wide / narrow); extrapolation R07 -> R08

| reading | R05/R06 | R06/R07 | R07/R08 | R07 count / (R06/R07 fall) [EST of R08] | R08 counted |
|---|---|---|---|---|---|
| BASE (S) | 1.61 | 1.90 | 2.52 | 1,985 | 1,501 |
| BASE (F) | 1.61 | 1.90 | 2.49 | 1,927 | 1,474 |
| PLANS4 (S) | 1.64 | 1.99 | 2.56 | 1,776 | 1,378 |
| PLANS4 (F) | 1.64 | 1.99 | 2.54 | 1,723 | 1,349 |
| OWN (S) | 1.59 | 1.87 | 2.49 | 1,927 | 1,449 |
| OWN (F) | 1.59 | 1.87 | 2.47 | 1,875 | 1,420 |
| HARD (S) | 2.46 | 3.51 | 4.12 | 162 | 138 |
| HARD (F) | 2.44 | 3.50 | 4.09 | 161 | 138 |
| UNION (S) | 1.60 | 1.90 | 2.49 | 2,004 | 1,526 |
| UNION (F) | 1.61 | 1.90 | 2.46 | 1,948 | 1,500 |

### T4. Own-hit classes: Z(nunu) full class by deficit k (reading BASE, S; label m)

| width | s = 0: k = 0 / 1 / 2 / 3 | s = 3: k = 0 / 1 / 2 / 3 / 4 / 5 |
|---|---|---|
| R04n | 253 / 958 / 4,056 / 8,656 | 33 / 98 / 268 / 556 / 1,475 / 4,622 |
| R04w | 251 / 959 / 4,055 / 8,650 | 33 / 97 / 268 / 557 / 1,474 / 4,617 |
| R05 | 224 / 846 / 3,484 / 7,012 | 29 / 83 / 247 / 486 / 1,325 / 4,054 |
| R06 | 157 / 491 / 2,135 / 4,419 | 22 / 55 / 167 / 325 / 901 / 2,643 |
| R07 | 81 / 213 / 965 / 2,522 | 16 / 39 / 71 / 177 / 460 / 1,449 |
| R08 | 26 / 80 / 318 / 1,077 | 3 / 19 / 41 / 82 / 201 / 623 |

### T5. k per layer type at s = 3 (k_IP, k_2S of the best witness; reading PLANS4 and OWN, S; R08 and R04w)

| reading, width | (k_IP, k_2S): count |
|---|---|
| PLANS4, R08 | (0,0): 3; (0,1): 10; (0,2): 10; (0,3): 2; (1,0): 9; (1,1): 15; (1,2): 19; (1,3): 35; (2,0): 13; (2,1): 40; (2,2): 45; (2,3): 192; (3,0): 19; (3,1): 76; (3,2): 148; (4,0): 32; (4,1): 204; (5,0): 73 |
| PLANS4, R04w | (0,0): 33; (0,1): 57; (0,2): 86; (0,3): 71; (1,0): 40; (1,1): 98; (1,2): 181; (1,3): 634; (2,0): 84; (2,1): 257; (2,2): 484; (2,3): 3209; (3,0): 48; (3,1): 275; (3,2): 700; (4,0): 81; (4,1): 584; (5,0): 124 |
| OWN, R08 | (0,0): 3; (0,1): 7; (0,2): 10; (0,3): 4; (1,0): 7; (1,1): 17; (1,2): 19; (1,3): 29; (2,0): 18; (2,1): 37; (2,2): 52; (2,3): 191; (3,0): 16; (3,1): 72; (3,2): 156; (4,0): 38; (4,1): 196; (5,0): 74 |
| OWN, R04w | (0,0): 27; (0,1): 48; (0,2): 87; (0,3): 61; (1,0): 29; (1,1): 77; (1,2): 161; (1,3): 586; (2,0): 77; (2,1): 212; (2,2): 426; (2,3): 2909; (3,0): 44; (3,1): 256; (3,2): 642; (4,0): 82; (4,1): 537; (5,0): 115 |
| UNION, R08 | (0,0): 3; (0,1): 10; (0,2): 10; (0,3): 3; (1,0): 9; (1,1): 16; (1,2): 20; (1,3): 34; (2,0): 18; (2,1): 41; (2,2): 55; (2,3): 210; (3,0): 16; (3,1): 79; (3,2): 164; (4,0): 36; (4,1): 199; (5,0): 72 |
| UNION, R04w | (0,0): 33; (0,1): 57; (0,2): 86; (0,3): 71; (1,0): 40; (1,1): 98; (1,2): 181; (1,3): 634; (2,0): 84; (2,1): 257; (2,2): 484; (2,3): 3209; (3,0): 48; (3,1): 275; (3,2): 700; (4,0): 81; (4,1): 584; (5,0): 124 |

### T6. Variants at the T2 widths: Z(nunu) full class, reading BASE (S / F), each label

| label (pool, PV, files) | R07 s=0 | R08 s=0 | R08 s=3 | R04n s=3 | R04w s=3 | R05 s=3 | R06 s=3 | R07 s=3 | M (Z) | pilot files |
|---|---|---|---|---|---|---|---|---|---|---|
| m (merged, PV draw, w pos) | 3,781 / 3,668 | 1,501 / 1,474 | 969 / 846 | 7,052 / 6,645 | 7,046 / 6,641 | 6,224 / 5,870 | 4,113 / 3,802 | 2,212 / 1,964 | 993,885.9 | 460 Z + 623 |
| u (not merged, PV draw, w pos) | 3,795 / 3,678 | 1,516 / 1,486 | 979 / 853 | 7,065 / 6,660 | 7,059 / 6,656 | 6,240 / 5,887 | 4,131 / 3,818 | 2,221 / 1,971 | 993,885.9 | 460 Z + 623 |
| pv0 (merged, PV true, w pos) | 3,775 / 3,670 | 1,510 / 1,482 | 948 / 822 | 7,066 / 6,666 | 7,059 / 6,662 | 6,255 / 5,903 | 4,105 / 3,801 | 2,226 / 1,990 | 993,885.9 | 460 Z + 0 |
| pv2 (merged, PV draw2, w pos) | 921 / 899 | 361 / 349 | 221 / 185 | 1,771 / 1,670 | 1,771 / 1,670 | 1,582 / 1,487 | 1,040 / 956 | 535 / 466 | 248,246.3 | 115 Z + 0 |

### T7. Paired comparison with label m on the same pilot files (Z full class, BASE S): counted in both / only m / only variant

| variant | width, s | both | only m | only variant | m on these files | variant |
|---|---|---|---|---|---|---|
| u | R07, s = 0 | 3,781 | 0 | 14 | 3,781 | 3,795 |
| u | R08, s = 0 | 1,501 | 0 | 15 | 1,501 | 1,516 |
| u | R08, s = 3 | 969 | 0 | 10 | 969 | 979 |
| u | R04n, s = 3 | 7,048 | 4 | 17 | 7,052 | 7,065 |
| u | R04w, s = 3 | 7,042 | 4 | 17 | 7,046 | 7,059 |
| u | R05, s = 3 | 6,222 | 2 | 18 | 6,224 | 6,240 |
| u | R06, s = 3 | 4,112 | 1 | 19 | 4,113 | 4,131 |
| u | R07, s = 3 | 2,211 | 1 | 10 | 2,212 | 2,221 |
| pv0 | R07, s = 0 | 3,541 | 240 | 234 | 3,781 | 3,775 |
| pv0 | R08, s = 0 | 1,409 | 92 | 101 | 1,501 | 1,510 |
| pv0 | R08, s = 3 | 903 | 66 | 45 | 969 | 948 |
| pv0 | R04n, s = 3 | 6,613 | 439 | 453 | 7,052 | 7,066 |
| pv0 | R04w, s = 3 | 6,606 | 440 | 453 | 7,046 | 7,059 |
| pv0 | R05, s = 3 | 5,858 | 366 | 397 | 6,224 | 6,255 |
| pv0 | R06, s = 3 | 3,873 | 240 | 232 | 4,113 | 4,105 |
| pv0 | R07, s = 3 | 2,085 | 127 | 141 | 2,212 | 2,226 |
| pv2 | R07, s = 0 | 852 | 88 | 69 | 940 | 921 |
| pv2 | R08, s = 0 | 326 | 32 | 35 | 358 | 361 |
| pv2 | R08, s = 3 | 201 | 26 | 20 | 227 | 221 |
| pv2 | R04n, s = 3 | 1,624 | 144 | 147 | 1,768 | 1,771 |
| pv2 | R04w, s = 3 | 1,623 | 144 | 148 | 1,767 | 1,771 |
| pv2 | R05, s = 3 | 1,445 | 110 | 137 | 1,555 | 1,582 |
| pv2 | R06, s = 3 | 958 | 78 | 82 | 1,036 | 1,040 |
| pv2 | R07, s = 3 | 488 | 43 | 47 | 531 | 535 |

### T7b. Full sets judged as the finder judges them (c0, finder axis, w_core < W) against the other readings; Z full class, s = 0, S

| width | c0 counted (k <= 3) | of them without a HARD witness (k <= 3) | without an OWN witness | BASE counted | BASE without OWN | BASE without HARD |
|---|---|---|---|---|---|---|
| R04n | 13,923 | 975 | 975 | 13,923 | 975 | 975 |
| R04w | 13,913 | 3,829 | 961 | 13,915 | 961 | 3,831 |
| R05 | 10,975 | 6,070 | 815 | 11,566 | 815 | 6,656 |
| R06 | 5,622 | 3,657 | 446 | 7,202 | 446 | 5,209 |
| R07 | 2,368 | 1,809 | 191 | 3,781 | 191 | 3,213 |
| R08 | 749 | 615 | 77 | 1,501 | 77 | 1,363 |

### T7c. Every stored row of the B1 / hs / lowpt samples (any k within k_max at any width in any category)

| term | file | event | orientation | flagged | BASE S k at s = 0 (R04n..R08) | BASE S k at s = 3 | UNION S s = 0 | UNION S s = 3 |
|---|---|---|---|---|---|---|---|---|
| DIFC | p2-c-pilot-c0-difc-0076.npz | 22673 | 20 | 0 | 3 / 3 / 3 / 3 / 4 / 4 | 6 / 6 / 6 / 6 / 7 / 7 | 3 / 3 / 3 / 3 / 4 / 4 | 6 / 6 / 6 / 6 / 7 / 7 |

### T8. Flagged events (n_early_prod > 0): events per stream, and counted rows WITH minus WITHOUT (all readings, widths, s)

| term | DIF | DIFC | NI22 | NI30 | NI61 | NIX | NIC | HS | LOWPT |
|---|---|---|---|---|---|---|---|---|---|
| flagged events | 0 | 0 | 10 | 15 | 18 | 212 | 59 | 38 | 4 |
| largest WITH - WITHOUT count in any table | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### T9. H(R06) and the enrichment E = 1/H(R06) per term (s = 0; BASE S; H = Gamma(m + 1)/M: mean (m + 1)/M; m = 0: 68 % upper value 1.14/M)

| term | m(R06) | M | H(R06) mean | E = 1/H | m(R07) | m(R08) |
|---|---|---|---|---|---|---|
| Z | 7,202 | 993,885.9 | 0.00725 | 138 | 3,781 | 1,501 |
| DIF | 0 | 4,000,000.0 | 2.5e-07 | 4,000,000 (>= 3,510,514 at 68 %) | 0 | 0 |
| DIFC | 1 | 4,000,000.0 | 5e-07 | 2,000,000 | 0 | 0 |
| NI22 | 0 | 1,000,000.0 | 1e-06 | 1,000,000 (>= 877,628 at 68 %) | 0 | 0 |
| NI30 | 0 | 1,000,000.0 | 1e-06 | 1,000,000 (>= 877,628 at 68 %) | 0 | 0 |
| NI61 | 0 | 1,000,000.0 | 1e-06 | 1,000,000 (>= 877,628 at 68 %) | 0 | 0 |
| NIX | 0 | 4,000,000.0 | 2.5e-07 | 4,000,000 (>= 3,510,514 at 68 %) | 0 | 0 |
| NIC | 0 | 2,000,000.0 | 5e-07 | 2,000,000 (>= 1,755,257 at 68 %) | 0 | 0 |
| HS | 0 | 2,000,000.0 | 5e-07 | 2,000,000 (>= 1,755,257 at 68 %) | 0 | 0 |
| LOWPT | 0 | 200,000.0 | 5e-06 | 200,000 (>= 175,526 at 68 %) | 0 | 0 |

### T10. Hand-over variant per stream as recorded in the pilot files (label m)

| stream | files | trunc_mode | events per mode (-1 neutral, 0 radius, 3 hybrid) | beta_min |
|---|---|---|---|---|
| pilot.c0.dif | 111 | {'radius': 111} | {'-1': 204437, '0': 3795563, '1': 0, '2': 0, '3': 0} | {'0.1': 111} |
| pilot.c0.difc | 121 | {'hybrid': 121} | {'-1': 0, '0': 0, '1': 0, '2': 0, '3': 4000000} | {'0.1': 121} |
| pilot.c0.hs | 77 | {'autoh': 77} | {'-1': 109661, '0': 1146131, '1': 0, '2': 0, '3': 744208} | {'0.1': 77} |
| pilot.c0.lowpt | 9 | {'autoh': 9} | {'-1': 3695, '0': 62572, '1': 0, '2': 0, '3': 133733} | {'0.1': 9} |
| pilot.c0.ni22 | 49 | {'radius': 49} | {'-1': 130937, '0': 869063, '1': 0, '2': 0, '3': 0} | {'0.1': 49} |
| pilot.c0.ni30 | 36 | {'radius': 36} | {'-1': 128799, '0': 871201, '1': 0, '2': 0, '3': 0} | {'0.1': 36} |
| pilot.c0.ni61 | 37 | {'radius': 37} | {'-1': 128348, '0': 871652, '1': 0, '2': 0, '3': 0} | {'0.1': 37} |
| pilot.c0.nic | 60 | {'hybrid': 60} | {'-1': 0, '0': 0, '1': 0, '2': 0, '3': 2000000} | {'0.1': 60} |
| pilot.c0.nix | 123 | {'radius': 123} | {'-1': 459888, '0': 3540112, '1': 0, '2': 0, '3': 0} | {'0.1': 123} |
| pilot.hs0.znn | 460 | {'None': 460} | {} | {'None': 460} |

### T11. Independent search (Nils's code) on the counted Z events of every 2nd pilot file

| width, s, reading | counted (Phase-2 rows) | confirmed (verified witness, k <= k_max) | of which k same or lower | not found | with a hard-window witness (S only) |
|---|---|---|---|---|---|
| R04n_s0_F | 6,784 | 6,320 (93.2 %) | 6,082 | 464 |  |
| R04n_s0_S | 6,977 | 6,495 (93.1 %) | 6,251 | 482 | 6,495 |
| R04n_s3_F | 3,309 | 2,662 (80.4 %) | 2,353 | 647 |  |
| R04n_s3_S | 3,508 | 2,712 (77.3 %) | 2,389 | 796 | 2,712 |
| R04w_s0_F | 6,784 | 6,316 (93.1 %) | 6,077 | 468 |  |
| R04w_s0_S | 6,977 | 6,492 (93.0 %) | 6,246 | 485 | 5,020 |
| R04w_s3_F | 3,309 | 2,662 (80.4 %) | 2,351 | 647 |  |
| R04w_s3_S | 3,508 | 2,712 (77.3 %) | 2,387 | 796 | 2,234 |
| R05_s0_F | 5,593 | 5,193 (92.8 %) | 5,017 | 400 |  |
| R05_s0_S | 5,770 | 5,353 (92.8 %) | 5,170 | 417 | 2,466 |
| R05_s3_F | 2,916 | 2,364 (81.1 %) | 2,108 | 552 |  |
| R05_s3_S | 3,099 | 2,409 (77.7 %) | 2,141 | 690 | 1,163 |
| R06_s0_F | 3,466 | 3,257 (94.0 %) | 3,166 | 209 |  |
| R06_s0_S | 3,580 | 3,362 (93.9 %) | 3,268 | 218 | 1,023 |
| R06_s3_F | 1,901 | 1,544 (81.2 %) | 1,374 | 357 |  |
| R06_s3_S | 2,054 | 1,586 (77.2 %) | 1,406 | 468 | 459 |
| R07_s0_F | 1,832 | 1,744 (95.2 %) | 1,713 | 88 |  |
| R07_s0_S | 1,892 | 1,795 (94.9 %) | 1,763 | 97 | 285 |
| R07_s3_F | 984 | 782 (79.5 %) | 701 | 202 |  |
| R07_s3_S | 1,105 | 823 (74.5 %) | 738 | 282 | 135 |
| R08_s0_F | 726 | 684 (94.2 %) | 674 | 42 |  |
| R08_s0_S | 738 | 699 (94.7 %) | 687 | 39 | 66 |
| R08_s3_F | 405 | 309 (76.3 %) | 278 | 96 |  |
| R08_s3_S | 469 | 330 (70.4 %) | 294 | 139 | 49 |

### T12. Rule-1 projection, DRY RUN, **NOT BINDING** (NOT BINDING (dry run of p3-a: v1-based EST pile-up rows, planning N_trig of the three MET additions, v1 weights))

| T2 candidate | pile-up row | reading | m_Z (S) | B50 (S) [16-84 %] | m_Z (F) | B50 (F) | pauses |
|---|---|---|---|---|---|---|---|
| R07 | R07_direct | BASE | 3,781 | 189,341 [183,888-195,218] | 3,668 | 184,596 | yes |
| R07 | R07_direct | PLANS4 | 3,531 | 178,840 [173,430-184,676] | 3,422 | 174,264 | yes |
| R07 | R07_direct | OWN | 3,613 | 182,285 [176,858-188,136] | 3,512 | 178,048 | yes |
| R07 | R07_direct | HARD | 568 | 54,409 [49,522-59,823] | 565 | 54,284 | yes |
| R07 | R07_direct | UNION | 3,804 | 190,310 [184,849-196,187] | 3,692 | 185,602 | yes |
| R08 | R08@88 | BASE | 1,501 | 63,246 [61,655-64,880] | 1,474 | 62,113 | yes |
| R08 | R08@118 | BASE | 1,501 | 63,271 [61,678-64,902] | 1,474 | 62,138 | yes |
| R08 | R08@148 | BASE | 1,501 | 63,294 [61,697-64,925] | 1,474 | 62,161 | yes |
| R08 | R08@88 | PLANS4 | 1,378 | 58,081 [56,556-59,647] | 1,349 | 56,864 | yes |
| R08 | R08@118 | PLANS4 | 1,378 | 58,106 [56,579-59,671] | 1,349 | 56,889 | yes |
| R08 | R08@148 | PLANS4 | 1,378 | 58,128 [56,599-59,694] | 1,349 | 56,911 | yes |
| R08 | R08@88 | OWN | 1,449 | 61,064 [59,501-62,669] | 1,420 | 59,847 | yes |
| R08 | R08@118 | OWN | 1,449 | 61,089 [59,524-62,692] | 1,420 | 59,872 | yes |
| R08 | R08@148 | OWN | 1,449 | 61,112 [59,543-62,715] | 1,420 | 59,895 | yes |
| R08 | R08@88 | HARD | 138 | 6,024 [5,548-6,533] | 138 | 6,024 | yes |
| R08 | R08@118 | HARD | 138 | 6,048 [5,570-6,559] | 138 | 6,048 | yes |
| R08 | R08@148 | HARD | 138 | 6,070 [5,589-6,582] | 138 | 6,070 | yes |
| R08 | R08@88 | UNION | 1,526 | 64,295 [62,691-65,942] | 1,500 | 63,204 | yes |
| R08 | R08@118 | UNION | 1,526 | 64,320 [62,714-65,965] | 1,500 | 63,229 | yes |
| R08 | R08@148 | UNION | 1,526 | 64,343 [62,733-65,988] | 1,500 | 63,252 | yes |
| R09 | R09 | BASE | 1,501 | 63,170 [61,578-64,802] | 1,474 | 62,037 | yes |
| R09 | R09 | PLANS4 | 1,378 | 58,004 [56,479-59,569] | 1,349 | 56,787 | yes |
| R09 | R09 | OWN | 1,449 | 60,988 [59,424-62,592] | 1,420 | 59,771 | yes |
| R09 | R09 | HARD | 138 | 5,947 [5,473-6,457] | 138 | 5,947 | yes |
| R09 | R09 | UNION | 1,526 | 64,219 [62,614-65,864] | 1,500 | 63,128 | yes |
| R11 | R11_lo | BASE | 1,501 | 63,163 [61,571-64,795] | 1,474 | 62,030 | yes |
| R11 | R11_hi | BASE | 1,501 | 63,164 [61,572-64,796] | 1,474 | 62,031 | yes |
| R11 | R11_lo | PLANS4 | 1,378 | 57,998 [56,473-59,562] | 1,349 | 56,781 | yes |
| R11 | R11_hi | PLANS4 | 1,378 | 57,998 [56,473-59,563] | 1,349 | 56,782 | yes |
| R11 | R11_lo | OWN | 1,449 | 60,981 [59,417-62,585] | 1,420 | 59,764 | yes |
| R11 | R11_hi | OWN | 1,449 | 60,982 [59,418-62,586] | 1,420 | 59,765 | yes |
| R11 | R11_lo | HARD | 138 | 5,940 [5,466-6,450] | 138 | 5,940 | yes |
| R11 | R11_hi | HARD | 138 | 5,941 [5,467-6,451] | 138 | 5,941 | yes |
| R11 | R11_lo | UNION | 1,526 | 64,212 [62,607-65,857] | 1,500 | 63,121 | yes |
| R11 | R11_hi | UNION | 1,526 | 64,213 [62,607-65,858] | 1,500 | 63,122 | yes |
| R14=R17=R20 | none | BASE | 969 | 40,836 [39,560-42,150] | 846 | 35,669 | yes |
| R14=R17=R20 | R14_lo | BASE | 969 | 40,842 [39,566-42,158] | 846 | 35,675 | yes |
| R14=R17=R20 | R14_hi | BASE | 969 | 40,846 [39,569-42,161] | 846 | 35,678 | yes |
| R14=R17=R20 | none | PLANS4 | 945 | 39,829 [38,569-41,127] | 816 | 34,407 | yes |
| R14=R17=R20 | R14_lo | PLANS4 | 945 | 39,835 [38,575-41,135] | 816 | 34,414 | yes |
| R14=R17=R20 | R14_hi | PLANS4 | 945 | 39,839 [38,578-41,138] | 816 | 34,417 | yes |
| R14=R17=R20 | none | OWN | 946 | 39,871 [38,610-41,170] | 814 | 34,326 | yes |
| R14=R17=R20 | R14_lo | OWN | 946 | 39,877 [38,616-41,177] | 814 | 34,332 | yes |
| R14=R17=R20 | R14_hi | OWN | 946 | 39,881 [38,620-41,180] | 814 | 34,335 | yes |
| R14=R17=R20 | none | HARD | 151 | 6,488 [5,988-7,018] | 110 | 4,768 | yes |
| R14=R17=R20 | R14_lo | HARD | 151 | 6,496 [5,994-7,025] | 110 | 4,774 | yes |
| R14=R17=R20 | R14_hi | HARD | 151 | 6,499 [5,997-7,029] | 110 | 4,777 | yes |
| R14=R17=R20 | none | UNION | 995 | 41,927 [40,634-43,259] | 865 | 36,466 | yes |
| R14=R17=R20 | R14_lo | UNION | 995 | 41,933 [40,640-43,266] | 865 | 36,472 | yes |
| R14=R17=R20 | R14_hi | UNION | 995 | 41,937 [40,643-43,269] | 865 | 36,475 | yes |
| FB(0) width none | none | BASE | 7,052 | 296,198 [292,740-299,723] | 6,645 | 279,099 | yes |
| FB(0) width none | none | PLANS4 | 7,052 | 296,198 [292,740-299,723] | 6,645 | 279,099 | yes |
| FB(0) width none | none | OWN | 6,373 | 267,697 [264,410-271,048] | 6,025 | 253,079 | yes |
| FB(0) width none | none | HARD | 6,373 | 267,697 [264,410-271,048] | 6,025 | 253,079 | yes |
| FB(0) width none | none | UNION | 7,052 | 296,198 [292,740-299,723] | 6,645 | 279,099 | yes |
| FB(0) width 75 mm | none | BASE | 7,046 | 295,947 [292,490-299,469] | 6,641 | 278,931 | yes |
| FB(0) width 75 mm | none | PLANS4 | 7,046 | 295,947 [292,490-299,469] | 6,641 | 278,931 | yes |
| FB(0) width 75 mm | none | OWN | 6,376 | 267,823 [264,535-271,175] | 6,033 | 253,415 | yes |
| FB(0) width 75 mm | none | HARD | 5,367 | 225,475 [222,460-228,550] | 5,076 | 213,247 | yes |
| FB(0) width 75 mm | none | UNION | 7,046 | 295,947 [292,490-299,469] | 6,641 | 278,931 | yes |
| FB(1) | none | BASE | 6,224 | 261,450 [258,202-264,761] | 5,870 | 246,573 | yes |
| FB(1) | none | PLANS4 | 6,208 | 260,775 [257,530-264,084] | 5,854 | 245,899 | yes |
| FB(1) | none | OWN | 5,737 | 241,001 [237,882-244,179] | 5,427 | 227,977 | yes |
| FB(1) | none | HARD | 2,859 | 120,193 [117,991-122,441] | 2,690 | 113,087 | yes |
| FB(1) | none | UNION | 6,231 | 261,744 [258,493-265,057] | 5,877 | 246,867 | yes |
| FB(2) | none | BASE | 4,113 | 172,829 [170,185-175,523] | 3,802 | 159,764 | yes |
| FB(2) | none | PLANS4 | 4,035 | 169,556 [166,937-172,224] | 3,731 | 156,784 | yes |
| FB(2) | none | OWN | 3,841 | 161,412 [158,858-164,017] | 3,564 | 149,773 | yes |
| FB(2) | none | HARD | 1,192 | 50,202 [48,784-51,659] | 1,048 | 44,153 | yes |
| FB(2) | none | UNION | 4,119 | 173,081 [170,435-175,777] | 3,809 | 160,058 | yes |
| FB(3) | none | BASE | 2,212 | 93,021 [91,087-95,001] | 1,964 | 82,605 | yes |
| FB(3) | none | PLANS4 | 2,150 | 90,417 [88,510-92,369] | 1,900 | 79,919 | yes |
| FB(3) | none | OWN | 2,081 | 87,522 [85,646-89,442] | 1,846 | 77,651 | yes |
| FB(3) | none | HARD | 410 | 17,359 [16,532-18,222] | 351 | 14,884 | yes |
| FB(3) | none | UNION | 2,235 | 93,986 [92,042-95,976] | 1,982 | 83,360 | yes |
| FB(4) | none | BASE | 969 | 40,836 [39,560-42,150] | 846 | 35,669 | yes |
| FB(4) | R14_lo | BASE | 969 | 40,842 [39,566-42,158] | 846 | 35,675 | yes |
| FB(4) | R14_hi | BASE | 969 | 40,846 [39,569-42,161] | 846 | 35,678 | yes |
| FB(4) | none | PLANS4 | 945 | 39,829 [38,569-41,127] | 816 | 34,407 | yes |
| FB(4) | R14_lo | PLANS4 | 945 | 39,835 [38,575-41,135] | 816 | 34,414 | yes |
| FB(4) | R14_hi | PLANS4 | 945 | 39,839 [38,578-41,138] | 816 | 34,417 | yes |
| FB(4) | none | OWN | 946 | 39,871 [38,610-41,170] | 814 | 34,326 | yes |
| FB(4) | R14_lo | OWN | 946 | 39,877 [38,616-41,177] | 814 | 34,332 | yes |
| FB(4) | R14_hi | OWN | 946 | 39,881 [38,620-41,180] | 814 | 34,335 | yes |
| FB(4) | none | HARD | 151 | 6,488 [5,988-7,018] | 110 | 4,768 | yes |
| FB(4) | R14_lo | HARD | 151 | 6,496 [5,994-7,025] | 110 | 4,774 | yes |
| FB(4) | R14_hi | HARD | 151 | 6,499 [5,997-7,029] | 110 | 4,777 | yes |
| FB(4) | none | UNION | 995 | 41,927 [40,634-43,259] | 865 | 36,466 | yes |
| FB(4) | R14_lo | UNION | 995 | 41,933 [40,640-43,266] | 865 | 36,472 | yes |
| FB(4) | R14_hi | UNION | 995 | 41,937 [40,643-43,269] | 865 | 36,475 | yes |

All labels, readings, candidates, pile-up rows, flagged variants: 1440 projections, 1440 at or above 299.1; smallest B50 3,610, largest 297,932.
Largest |B50(WITH) - B50(WITHOUT flagged events)| over label m: 0.009 events.

