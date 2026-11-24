# [RESULT] Both pile-up estimators above their cap on development samples (reviewed); no decision now

Written 2026-11-24 14:47 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

**Phase 3, quirks v2 study — Tue 24 Nov 2026, 14:47 -05.** No decision is needed from you now.

**RESULT (development, not a verdict; reviewed):** both pile-up estimators are above the cap s_model ≤ 0.135 on the development samples: repaired thinning 0.506, occupancy model 0.355 (held-out R06, ln r = +0.355 ± 0.034).

- **Thinning:** the cause is localised: re-running the finder on the thinned events removes the excess. The redesign it points to costs ≈ 1,200 CPU-h beyond the approved figure (ESTIMATE) and will be put to you at the day-15 pause. Its validated range is R04–R06 at most ([DT2]). If you decline it, thinning is "not submitted".
- **Occupancy model:** no cause is demonstrated yet. An investigation runs until Mon 30 Nov. A redesign is tried once, on a fresh development sample (`dev.pu1`, 100 CPU-h, in the approved plan), only if the investigation finds a cause; otherwise the model is "not submitted".
- The cap status becomes binding at the day-15 reading (Sat 5 Dec at the latest under the default calendar), which is already expected to pause on B₅₀ (≈ 6×10⁴ events against the 300 line).

**Reach outlook vs last report:** equally promising at present (ESTIMATE, v1 placeholder efficiencies only), because the reading is led by the SM ceiling, not by pile-up. It is less promising in the branch where that ceiling is removed, because a pile-up term with no credit enters at ≈ 485 events beyond R07, above the 300 line by itself.

Checked by: an independent critical review (own recount from the raw records, own thinning code; not a bug) and an advisor ruling on the frozen rules (STR §11.7 rules 1–2).

Files: `analyses/quirks_v2/phase3_selection/outputs/P3B_PILEUP_casper_2026-11-24.md` (corrections pending), `phase3_selection/review/critical/P3B_CRITICAL_REVIEW_dorte_2026-11-24_14-22.md`, `phase3_selection/review/advisor/ADVISOR_B2CAP_freja_2026-11-24_14-23.md` (with Addendum 1).

Still open from earlier notices: the calendar shift (default C applies Wed 25 Nov 12:00) and the docker build permission for C1-c.
