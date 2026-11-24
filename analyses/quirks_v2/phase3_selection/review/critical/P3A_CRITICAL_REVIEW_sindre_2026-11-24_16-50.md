# Critical review of work package p3-a (final pilot classification, rule-1 counts)

Sindre (Fable 5.2, critical reviewer, rule 1(c)), 2026-11-24 16:50 -0500 (`date`). I did not write, run or edit any
p3-a code. Artifact: `phase3_selection/outputs/P3A_PILOT_FINAL_aurora_2026-11-24.md` (`ART`), read in full to l.647
(§0–§9 and tables T1–T2; the remaining generated tables T3–T12 were checked through the JSON they are printed from,
not read line by line). `STR`, `ADD`, `COM`, `NIL`, `YLV` as in the artifact.
Tags: VERIFIED = re-derived or measured by me (file or command given); ESTIMATE; UNVERIFIED = transcribed.
No signal file was opened, no efficiency formed. No git, no subagent. I do not give the rule-1 verdict.

My own files: `review/critical/sindre_recount.py` (independent recount; imports no p3-a script; columns addressed by
name), `review/critical/sindre_recount.json`. Compute: one job on maxwell, nice 15, 20.4 CPU-s, 230 MB
(`/usr/bin/time -v`), after `pgrep … "qv2run job" -c` = 1; SLOTS.md line written.

## Verdict: ITERATE (1 A, 4 B, 8 C)

**The numbers are right.** Every count I re-derived equals the artifact. No convention was fixed. The A item is the
blocker the executor herself reported (her §8 item 1), which I confirm and extend; it is resolved by an advisor
ruling, not by the executor. The four B items are text corrections in the artifact: two "points to" statements that
are firmer than the frozen text allows, a missing coverage label on the s = 3 rows, and an incomplete item 9.
None of the findings moves any count, and none can bring a reading near 300.

## 1. What I re-derived (focus 1) [all VERIFIED, `sindre_recount.json`]

Method: my script reads the 575 + 232 raw job outputs on cajuela (`p3a/p3-a-clsxz/000`, `p3a/p3-a-clsxb/000`), forms
the five readings from the named columns and counts rows with k ≤ 3 (s = 0) or k ≤ 5 (s = 3) per term. It shares
no code with `p3a_counts.py`. It is a recount of the classified outputs, **not** a re-classification: the
classifier itself was checked by Nils (R08, s = 0) and by the executor's §5; I add nothing to that.

| quantity | artifact | mine |
|---|---|---|
| all count tables, 5 readings × 6 widths × s = 0 / 3 × S / F, labels m, u, pv0, pv2 (480 tables, every term) | `p3a_counts.json` | **480 of 480 identical** |
| pilot files per label; each classified once and completely; duplicate (file, event, orientation) rows | 1,083; once; — | 1,083 (460 Z + 623); max 1; 0 duplicates |
| Z(νν): generated / full class / 0.05 class / w_v1 = 0 | 2.3×10⁶ / 994,446 / 8,095 / 1,297,459 | the same (sum of file meta) |
| M = Σw/w_max, full class | 993,885.9 | 974,008.2056 / 0.98 = 993,885.924 |
| weight classes are clean | — | full class w ∈ [0.9739, 0.98]; low class w ∈ [0.0487, 0.0490]; no row with w = 0 |
| m_Z BASE (S), s = 0: R04n / R04w / R05 / R06 / R07 / R08 | 13,923 / 13,915 / 11,566 / 7,202 / 3,781 / 1,501 | the same |
| m_Z BASE (F): R06 / R08; s = 3 R08 (S / F); FB(0) 75 mm / none (S) | 6,981 / 1,474; 969 / 846; 7,046 / 7,052 | the same |
| R08, s = 0 (S): OWN / PLANS4 / HARD / UNION; 0.05 class BASE | 1,449 / 1,378 / 138 / 1,526; 13 | the same |
| falls R05→R06→R07→R08, BASE (S) | ×1.61, ×1.90, ×2.52 | 1.6059, 1.9048, 2.5190 |
| 1/H(R06), Z(νν), BASE (S) | 138 | 993,885.924 / 7,203 = 137.98 (with m instead of m + 1: 138.00) |
| by deficit k at R08 (S): 0 / 1 / 2 / 3 | 26 / 80 / 318 / 1,077 | the same; R06 157 / 491 / 2,135 / 4,419, the same |
| weighted m at R08 | 1,500.17 | 1,470.170 / 0.98 = 1,500.17 |
| non-Z rows in 1.92×10⁷ events × orientations, pools m and u | 1 (DIF-C 0076, event 22,673, orientation 20) | 1 in each pool, the same row |
| that row: k at R04n / R04w / R05 / R06 / R07 / R08, s = 0; s = 3 | 3 / 3 / 3 / 3 / 4 / 4; 6–7 | the same (S and F); `n_early_prod` = 0 |
| rows of flagged events (n_early_prod > 0), any label | 0 | 0 |
| dry run: number of projections; below 299.1; smallest; smallest on a full sample | 1,440; 0; 3,610; 4,726 | 1,440; 0; 3,609.6 (pv2); 4,725.7 (u, HARD, F, R14-type) (`p3a_rule1_dryrun.json`) |
| independent search, confirmed fractions (S): s = 0 R04 / R07 / R08; s = 3 R08 | 93.1 / 94.9 / 94.7 %; 70.4 % | 6,495 of 6,977; 1,795 of 1,892; 699 of 738; 330 of 469 (`p3a_indep_summary.json`) |

Closed-form check of the dry run: 41,704,631.6 / 993,885.9 = 41.961 events per Z count; × 1,502 = 63,026 (mean of the
Z term) against her Z-term median 63,014 and B₅₀ 63,169.8. Consistent (median of Gamma(1,502) is 1,501.67).

**The DIF-C row touches no T2 candidate**: k = 4 > k_max = 3 at R07 and R08, and k = 6–7 > 5 at s = 3. VERIFIED.
**R06 → R07 and E = 138**: confirmed. E is ≥ 100 under every reading she lists (142 F, 147 OWN, 498 HARD), so
the E-branch of §11.7 rule 3 (b) does not depend on an open convention. All of this is on v1 weights (finding A-1).

## 2. Findings

### A-1 (must resolve; owner: orchestrator and advisor, not the executor). The counts cannot enter a binding reading until the MET-model question of her §8 item 1 is ruled on — and the question is wider than she states.

Answer to focus (4): **she is right.** Swapping `pileup_rows.json` and `met_ntrig.json` does not make the reading binding.
Evidence, read in the code:

- The road of every Z(νν) event is centred on `phimet_reco_v1` and only events with `w_v1 > 0` are classified
  (`p2w_subset.py:474-475`, `p3a_multi.py:57-58, 64`; `_eval` cuts on `|Δφ(axis, phimet)| < road`, `p2w_subset.py:158, 337`).
- m counts events of the class w ≥ 0.5 and M is Σw/w_max of the same class. ADD l.607 replaces these weights by the
  day-12 MET model. A change of weights changes **m and M together**; 1,297,459 of 2.3×10⁶ generated events (56 %)
  were never classified, so their contribution to m under another weight does not exist in any file.
- ADD l.360-361 says only that the events-per-count ("41") is recomputed. It does not say the count is. So option (i)
  of her §8 ("read on v1's preselection and axis") is a reading of the frozen text, and option (ii) is a new pass.
  Choosing between them is an advisor matter. She chose neither. Correct.

What she does **not** say, and the ruling needs:

- **`pilot.c0.hs` has the same dependence and no reclassification pass can remove it.** Its parents are drawn
  "INSIDE the road of their own event, |dphi(parent, phimet_reco_v1)| < 0.15" and in proportion to `w_v1`, "so events
  failing v1's preselection (w = 0) are never fired" (`p2a_hspool.py:14-17, 57-59`; ADD l.377-379). Under a v2 MET
  model this sample would have to be regenerated (chain rerun), not re-read. It is a zero-count floor of 2.8 events
  in the dry run, so it cannot move the verdict; it does decide whether "binding on the v2 model" is achievable at all.
- A bound that needs no new pass [ESTIMATE, mine]: if the v2 model only **adds** weight on the v1 axis, the worst
  case is that all 2.3×10⁶ events are full-weight and no new event counts: 41.70×10⁶ / 2.3×10⁶ = 18.1 events per count,
  × 1,502 ≈ 27,200 events at R09. This bound does not cover events that **lose** weight, nor an axis change. For
  those there is no bound, only the size of the gap (m_Z would have to fall from 1,501 to 3).
- §6 of the artifact is headed "How the binding run is made (inputs swapped by path, no code change)". That heading
  contradicts §8 item 1 and should not survive (see B-4).

Required: an advisor ruling on (i) against (ii), stating also what happens to `pilot.c0.hs`, before any text calls a
reading from these counts binding.

### B-1. The DIF-C row: §0 states one reading as the frozen rule; the text that speaks for the other is not quoted.

ART §0 item 2: "by the frozen attribution it belongs to the parent's class, not to the DIF-C term". ART §3.3 then says
"Neither is chosen". The summary is what gets copied. Three texts are missing from §3.3:

- ADD l.603-605, the replacement wording of rule 1 itself: each B1 class is read on its own pilot sample, "m being the
  number of (event, road orientation) passes over 21 orientations; **the parents of DIF-C and NI-C carry their Geant4
  crossings beyond half a turn**". The rule's own sentence counts passes, names no attribution filter, and names the
  parent's later arcs as part of what is read. That points to **1**, not 0.
- STR l.748-749: the attribution rule is introduced for "direct counts on samples with pile-up". The pilot has none.
- ADD l.257-258 ([L15] (i)): repeated crossings by one curling particle are "absent from every sample, except for the
  parent of a decay or interaction after a turn (DIF-C, NI-C)". If the row is sent to "the pile-up route (B2)", it
  is read by nothing: the B2 samples stop every particle at half a turn. The reading "0" removes the only place where
  this topology is counted.

Effect on any T2 candidate: none (verified above). Effect on the PREREG question "does a looping parent count for a B1
term": the artifact currently leans the wrong way. Fix: reword §0 item 2 to "attribution of this row is open (§3.3)",
and add the three quotations to the §3.3 table.

### B-2. §4.1 "Points to: w_core, CONFIDENCE MEDIUM-HIGH" is one-sided on the choice that carries a factor 10.9.

The ruling of 23 Nov says S3 is NOT fixed now. She does not fix it, but the pointer is stronger than the text.

- Her argument: the ceiling property of STR l.769 / l.788 needs every finder-passable set to be in a class, and 615 of
  749 finder-type sets at R08 have no hard-window witness. That is a fair necessary condition and I confirm the
  numbers (`p3a_dp2_inputs.json` `c0_vs_readings`: R08 c0 749, c0_not_hard 615; R07 2,368 / 1,809).
- What is missing: the same sentence of STR l.769 fails under w_core too. It argues from a candidate found **with**
  pile-up to its own-hit subset ("the term's own hits … lie inside its ribbon"). A MAD is not inherited by subsets:
  the own hits of a set with w_core < W can have w_core > W, and added hits can push w_core up (Nils §3, the two T7
  trials, is this mechanism). So "the widest-holding ribbon of a superset of hits is at least as good" (STR l.776)
  is literally true for a geometric window and not for a MAD. Each reading satisfies one half of the text's argument.
- The 615-of-749 statistic was computed after the counts were known and is used to argue for the reading that gives
  the larger, already quoted number. It is evidence, but it is post-hoc evidence and should be labelled so.

Fix: add the second point, label the statistic, and lower the pointer to "no clear pointer; w_core is the finder's
variable, the hard window is the reading under which STR l.769 and l.776 hold as written". Keep FLAG FOR HUMAN.
The verdict "above" holds under both (138 counts → 5,947).

### B-3. The s = 3 rows carry no coverage label where they feed decision point 2; one statement about them is wrong.

The ruling of 23 Nov requires the day-15 text to carry which rows were re-derived. ART §5 item 4 and §8 item 5 say it;
the tables of §0, §3.1 and §7 (R14 = R17 = R20 = FB(4), FB(0)–FB(3)) do not.

- Independent search at s = 3: 70.4 % (R08) to 77.7 % confirmed, on half the files. Rows needing k_IP ≥ 4 have no
  independent search at all (98 of the 139 not found at R08). The stored witness verifies only 1,743 of 2,307 s = 3
  rows; for the other 24 % no witness was kept.
- ART §5 item 4 says "reading S (F within 0.5 points)" for both lists. True at s = 0 (R08: 94.2 against 94.7). False at
  s = 3: R08 (F) is 309 of 405 = 76.3 % against 70.4 %; R04 (F) 80.4 % against 77.3 % [VERIFIED, `p3a_indep_summary.json`].

Is this a defect of the count? No: it is a limit of the check, honestly stated in §5. What it does to "above 300":
nothing. Taking only the independently confirmed share, 0.70 × 969 = 680 counts ≈ 28,500 events [ESTIMATE]; the
hard-window count alone (110, F) is 4,726. Fix: put the label on the three tables; correct the "0.5 points" sentence.

### B-4. Item 9 (§8 item 1) is incomplete, and §6 contradicts it.

See A-1. Fix in the artifact: (a) add the `pilot.c0.hs` dependence (parents chosen by `w_v1` and `phimet_reco_v1`;
regeneration, not reclassification); (b) rename the §6 paragraph to "How the dry run is repeated with other pile-up
rows and N_trig" and say there that this alone is not the binding run; (c) state that the "≈ 2.5–12 CPU-h" pass covers
the Z(νν) term only.

### C items

- **C-1.** ART §3.5: "H(R06) < 2.9×10⁻⁷ per (event, orientation)". 1.14 / 4×10⁶ is per event of M with the 21
  orientations summed (ADD l.384-386 defines m and M that way). Per (event, orientation) it would be 1.4×10⁻⁸.
- **C-2.** ART §6: "smallest outside HARD 33,274" and §4.9 "factor 16 … to 110" are full-sample values. Including the
  115-file subsample the smallest outside HARD is 28,823 (PLANS4, F, R14-type, pv2) and the factors are 12 and 96
  [VERIFIED, `p3a_rule1_dryrun.json`]. Say "on a full sample" in both places.
- **C-3.** The R07 pile-up row (N_trig / 48,000 × Gamma(36)) and the R11 / R14 rows are her constructions, recorded as a
  DECISION in the experiment log. The §6 table should carry "reading by Aurora, no approved row" in the cell.
- **C-4.** The second half of the files for the independent search was not run. It would cost ≈ 0.74 CPU-h
  (`cpu_s_in_jobs` ind) and 8.7 CPU-h of the budget were left. Recommend running it before the binding text is written.
- **C-5.** The witness check was changed twice after it failed (unweighted normal, then weighted, then the classifier's
  own normal for the last 17). She records this. The last step is valid because the definition is existential (a
  plane exists), but for those 17 the plane is the classifier's, so the check is of the verifier's cuts, not of the
  plane search. One sentence.
- **C-6.** The plan (fact 5) and a DECISION block of the experiment log both say every Z(νν) event is classified,
  w_v1 = 0 included. It was not done. 11.3 + 9.4 = 20.7 CPU-h was inside the 26 CPU-h stop limit, so cost is not the
  reason; the reason given (v1 axis is not the needed input) is sound. Record the reversal as its own DECISION block.
- **C-7.** In the headline tables OWN at s = 3 is 6,373 with no width cut and 6,376 with the 75 mm cut: a looser
  requirement gives a smaller count. This is the non-maximality she lists in C2 (541 OWN rows); a footnote on the
  FB(0) row would stop a reader taking it for an error.
- **C-8.** `qv2run rebuild-ledger` not run; ≈ 1.0 CPU-h is outside the ledger; a fourth process ran beside three jobs
  at 12:00. All self-reported. The orchestrator should rebuild the ledger before the CPU total is quoted.

## 3. Nils's conditions (focus 2)

| condition | met? | evidence |
|---|---|---|
| 1. lower bound, "above" only | yes | on every count table; UNION − BASE = 25 at R08 confirms non-maximality (1,526 against 1,501, my recount) |
| 2. both open readings in the text (S3, axis) | yes | §4.1, §4.2; a count and a projection under each at every T2 candidate (T1, `p3a_rule1_dryrun.json`) |
| 3. 1,501 / 1,474 quoted as produced, not replaced | yes | BASE reproduced, 14,757 of 14,757 rows; other readings are separate columns |
| R04–R07 re-derived (his §4) | partly | 92.8–94.9 % confirmed by his search on 230 of 460 files; 723 of 3,968 full-set witnesses rest on the finder's axis and were not re-verified by independent code at these widths |
| s = 3 re-derived | partly | 70–77 %; no independent search for k_IP ≥ 4 (B-3) |
| R04 width (row 7), search heuristic (row 6) | yes | counted both ways (8 events of 13,923; 1,378 against 1,501) |
| zeros worded "none found …; not an upper statement" | yes | §3.1, §3.3, §7 |
| 1,610 information only | yes | not re-derived, not used |

Nils's conditions are met where they are conditions on wording. Where they are gaps in coverage, the gaps are
narrowed, not closed, and that is said in §5 but not in the tables (B-3).

## 4. Open conventions and "points to" statements (focus 3)

No convention was chosen: every count of §3.1, §6 and §7 is given under every reading, and BASE is the Phase-2 output
unchanged. Fairness of each pointer against the text I read:

| § | pointer | fair? |
|---|---|---|
| 3.3 DIF-C row | §0: "belongs to the parent's class" | **no** — B-1 |
| 4.1 S3 | w_core, MEDIUM-HIGH | **too strong** — B-2 |
| 4.2 axis | no clear pointer | yes (STR l.755-778 names no axis) |
| 4.3 search | the maximum is the definition; every search is a lower bound | yes |
| 4.4 R04 width | (A) 75 mm, weakly | yes; correctly notes that the Phase-2 R04 column is reading (B) |
| 4.5 N_IT2 | S | yes (STR l.758-759 quoted; both carried; the 12.7 % gap at s = 3 is stated) |
| 4.6 merging | merged | yes ("same detector model as everywhere else", STR l.744-745); unmerged is +1.0 % |
| 4.7 PV | the draw | yes; the 6–9 % event reshuffle is reported |
| 4.8 M | measured 993,885.9 | yes; the open half (v2 weights) is A-1 |
| 4.9 best candidate | every candidate given | yes (ruling (iii)) |
| 4.10 pile-up at s = 3 | R11 value for R14-type; nothing for FB(k < 4) | yes |
| 4.11 flagged variant | conflict between ADD P6 (vi) and the 18 Nov ruling noted, not resolved | yes, and a useful catch |

## 5. The three limitations of focus (5)

| item | defect or stated limitation | effect on an "above 300" verdict |
|---|---|---|
| 1,297,459 Z(νν) events with w_v1 = 0, not classified | Stated limitation under v1 weights (they are in no term: correct to leave out of m and M). A gap for any v2-weight reading (A-1). A reversal of her own plan (C-6). | Under v1: none. Under v2 weights on the v1 axis with weight only added: B₅₀ ≥ ≈ 27,200 [ESTIMATE]. Otherwise unbounded in principle; the gap is a factor 500 in m_Z. |
| s = 3 rows with k_IP ≥ 4 without an independent search | Stated limitation of the check, not of the count; label missing in the tables (B-3). | None: confirmed share alone ≈ 28,500 events; HARD (F) 4,726. |
| no pile-up row for FB(k < 4) | Stated limitation; no frozen text supplies one (STR l.1015-1016 covers R14 only). The dry-run values for FB(0)–FB(3) are lower bounds of B and are labelled so. | Strengthens "above" (a missing non-negative term). It would matter only for the lowest-G choice among candidates, which is not p3-a's. The binding text must say that p3-b supplies these rows or that they are absent. |

## 6. Template items

- Figures: none in the artifact; the figure checks do not apply. Systematics, closure tests, MVA: not this work package.
- Sanity: all counts non-negative; F ≤ S in every table (0 violations in my recount); counts fall with width for BASE
  (S): 13,923 → 1,501; the one non-monotone pair is C-7.
- Circularity: the 14,757-row regression is a reproducibility check with the same imported classifier; she says so.
  The independent parts are Nils's search and verifier.
- Uncited constants: none found; constants are imported from the approved scripts.
- "What would a competing group have that we do not?" A maximal subset search, which would turn the B1 / hs / low-p_T
  zeros into upper statements. Its absence is a declared limit and does not matter for an "above" reading.
- Not checked by me: the classifier's physics at widths other than R08 (I recounted, I did not reclassify);
  tables T3–T12 line by line; `p3a_subset.py` beyond the weight and axis lines; the campaign JSON beyond one job.
