# [DECISION] MET model validation FAILED (stated); decision needed on the unsourced jet-response tail (sets multijet N_trig 7e5-5e8)

Written 2026-11-24 17:24 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

**Phase 3, quirks v2 study — Tue 24 Nov 2026.** A failed criterion (stated) and one decision for you.

**MET model (B4-b): external validation FAILED under both allowed readings.**
- MET tail fractions are ×1.49 / 1.13 / 0.78 at 60 / 78 / 90 GeV, against a 20 % tolerance.
- The other experiment's tt̄ widths are 34.6 vs 36.5 and 42.5 vs 37.5 GeV, against 0.5 GeV.
- Four remediation variants were tried; none passes. Cause: the two source figures differ in their recoil-response correction.

The frozen consequence is applied: Z(ττ), lost-lepton Z(ℓℓ) and multijets carry the full variation as their width (STR l.1400-1401). Internal check (b) PASS. No stop rule fires: the model's parameters come from public documents (CMS NOTE-2018/006, which you supplied).

**Decision needed: the non-Gaussian jet-response tail.** Three search rounds found no public source for it, and that one parameter alone sets the multijet N_trig:
- 7.1×10⁵ with the Gaussian core only;
- 4.28×10⁷ at the value declared in advance (1.5 % per jet, 3σ);
- 4.8×10⁸ at the declared upper value.

For comparison, Phase 1 planned 4×10⁵, and a 13 TeV monojet analysis at pile-up 23 has ≤ 1.0–1.4 % multijets; the model gives 1.7 % / 51 % / 92 % for the three settings. The frozen text says the tail is taken from public sources and "nothing is filled from memory", so no agent, advisor or orchestrator picks it.

**Options**
- **(A)** The declared tail as nominal, with the full variation as width.
- **(B)** Gaussian-only nominal, as recorded on 16 Nov before any result; the tail stated as a limitation and as a one-sided upward width.
- **(C)** You supply a source or a number.

**Recommendation:** (C) if you have a source; otherwise (B). The reason is the frozen rule "nothing is filled from memory", not the numbers.

**What happens until you answer:**
- Every number is carried under all three settings.
- The MET model is not frozen, and the one-time signal-acceptance step (A, m_mig) waits.
- Events per Z(νν) pilot count are 40.5 / 81.9 / 519, against the provisional 41.
- The binding day-15 reading is not yet made; it needs your answer. Please answer by Thu 3 Dec (day 15 is Sat 5 Dec at the latest under the default calendar).

**Reach outlook vs last report** (ESTIMATE, v1 placeholder efficiencies only; no reach number recomputed):
- Under (B): equally promising (40.5 against 41 per count; multijet zero-count allowance 0.81 against 0.46 planned).
- Under (A) or the upper tail: less promising (multijets become the largest SM term; allowance 48.7 or 550 events, against a summed SM allowance of 167.8).

Files: `analyses/quirks_v2/phase3_selection/outputs/P3C_MET_MODEL_birgit_2026-11-24.md` (§8); advisor ruling `phase3_selection/review/advisor/ADVISOR_MET_ITEM9_wenche_2026-11-24_17-23.md`. A critical review of the model is running.

Also open: the calendar shift and the p3-b review default (both Wed 25 Nov 12:00), and the docker permission for C1-c.
