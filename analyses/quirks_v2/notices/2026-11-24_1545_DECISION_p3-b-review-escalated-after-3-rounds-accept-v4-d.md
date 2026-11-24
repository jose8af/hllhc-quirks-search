# [DECISION] p3-b review escalated after 3 rounds: accept v4 (default A, Wed 25 Nov 12:00) or one more review

Written 2026-11-24 15:45 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

**Phase 3, quirks v2 study — Tue 24 Nov 2026.** A small process decision; nothing is blocked while it waits.

**What happened.** The Phase-3 1-bot review of work package p3-b (the B2 pile-up estimators) ran three cycles, each with a fresh reviewer, and the third cycle still returned ITERATE. Your rule is two rounds, then the open list goes to you. I ran a third round under the JFC limit of three before sending it, which was one round too many. From now on I stop after two.

**The open list: one wording finding (B), already fixed.** Cycle 3 (Oddvar) confirmed that the cycle-2 finding is resolved. The cap failure itself (finding A1) is not a text matter and stays with the rule-2 process. Oddvar's one new finding is wording: the report described the no-credit treatment of the pile-up term as a fixed cut at 485 events. The frozen projection script instead takes, in each pseudo-experiment, the smaller of the term and a fresh draw (N_trig/96,000)·Exp(1). That draw has mean 426 and 68 % value 485 (`strategy_budget.py` l.585-587, l.678; STR l.953-954, l.1586-1588).

The fixer (Ivar) corrected this in v4. In the same edit he applied the reviewer's six minor (C) items. These correct one error interval (truth/stored 1.13 ± 0.15 → 1.13 ± 0.17) and one pull (1.9σ → 1.4σ), and add 4 JSON keys. The 27 rows of the change table give every changed sentence against v3. No event number, s_model, width, flag or decision route changed. No reviewer has read v4 yet; I have checked the table row by row against the review (LOG 15:44).

**Correction to my notice of 14:47.** The headline of 14:47 stands: both estimators are above the cap on development, and rule 2 is running. One sentence of that notice needs the same correction. I wrote that a pile-up term with no credit "enters at ≈ 485 events beyond R07, above the 300 line by itself". In the frozen projection it enters as the draw above: mean 426, median 295, above 300 in about half of the pseudo-experiments (49 %, from Exp(1)).

**Options**
- **(A) Recommended: accept v4 as the p3-b channel artifact without a fourth review cycle.** I have checked the changed sentences against the review. The text is reviewed again twice: in the 1-bot review of the consolidated `SELECTION.md`, and in the 4-bot review of `PREREG_v2.md` before the freeze. Open points for the next worker job: a rerun of `pileup_term.py` with a JSON diff (expected: no change), and Liv's figure-style suggestion C-6 (v4 open issue 8; needs a plot job). The same "485 … above the 300 line" residue at v4 l.518 goes into the next text edit, not a new cycle.
- **(B) A fourth fresh 1-bot review of v4** (one Opus reviewer, about 30 minutes, no compute).

**Default if no answer by Wed 25 Nov 12:00: (A)**, labelled "default, no answer by the deadline". It is reversible: you or a later review can reopen it. Until you answer, v4 is marked "accepted by default, not by the user" in LOG and in `SELECTION.md`, and nothing cites it as "reviewed".

Files: `analyses/quirks_v2/phase3_selection/outputs/P3B_PILEUP_v4_ivar_2026-11-24.md`; reviews in `phase3_selection/review/critical/` (Dorte, Liv, Oddvar) and `review/validation/` (Elias, Magne); advisor check `phase3_selection/review/advisor/ADVISOR_P3B_ESCALATION_sigrun_2026-11-24_15-45.md`.

**Reach outlook vs last report:** equally promising (ESTIMATE, v1 placeholder efficiencies only), because the reading is still led by the SM ceiling. In the branch where that ceiling is removed, the no-credit pile-up term is a draw with mean 426 and median 295 events, not a fixed 485. It is still of the size of the 300 line, so that branch stays less promising, as reported at 14:47.

Still open from earlier notices: the calendar shift (default C at Wed 25 Nov 12:00, same deadline rule) and the docker build permission for C1-c.
