# Regression log

## 2026-11-18 — C1 SM family (v) FAIL (Phase 2, STR §4.1 item 5)
- Trigger: `phase2_exploration/outputs/c1_compare_sm_ignatius_2026-11-18.json` (R04 z +3.64, coherence z +4.6).
- Investigator: Jorund. Ticket: `phase2_exploration/REGRESSION_TICKET_SM.md` (2026-11-18 12:27 -0500).
- Finding: the z-scores use 1/√(weighted candidates) as width (c1_compare.py l.350, v1 background.py l.205); the
  event-level width is 5.0 % at R04, not 0.5 %. With event-level widths: +0.36σ, +0.60σ, +0.53σ. Generator
  environment checked: no difference found. Origin: Phase 2 comparison code, wording gap in STR §4.1 items 1 and 4.
- Status: OPEN. No fix applied. Frozen FAIL stays on record. Waiting for the user's ruling (amendment E4 or
  implementation bug; v1 width). No rerun recommended. Same defect expected in the C′_PU family (not yet read).
