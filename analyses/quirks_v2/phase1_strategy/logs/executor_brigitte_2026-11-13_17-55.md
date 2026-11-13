# Session log — executor Brigitte (Phase 1 strategy), 2026-11-13 17:55

- 17:55 start. Read AGENT_RULES, STUDY OVERRIDES, prompt.md, LOG.md, DEVIATIONS.md, COMMITMENTS.md, publication plan
  (full), FRAMING, digests D1-D6 (full), FEAS_A/B/C (full), experiment_log, conventions/search.md, executor.md,
  JFC 01, 02, 03 (to Phase 3 in full, 4a-5 skimmed), 04, 05, 06 §6.1-6.4.1, 09, 12.
- Sources opened to check decisive digest claims: `TT/acts/stage4/plan.md` l.1811-1812 (V4-4 = reproducibility and
  seeds; V4-5 = brute force, criterion |Δn| < 1 mrad in >= 95 %) and l.503-510 (T_seed stability rule);
  `STAGE3_INDEX.json` (per-point events and CPU, p2/BM); `C12FC_v1/acceptance.json` (A is generator/truth level:
  fiducial x trigger x preselection, template half); `G2A_REPORT.md` l.113-118 (the 0.4 TB is 8e4 loose candidates x
  5 MB per rho = 1 trial without hit lists); `g3/G3_REPORT.md` l.77-90 (union-count vs per-hit-set closure);
  `P2_NOVELTY_AUDIT.md` §1 (Knapen, Li: methods, numbers, pages); `stage5/EXTERNAL_BOUNDS.md`;
  `research/experimental_status_2026.md` §2 (reference-analysis systematics); `research/theory_signal_model.md` l.155-170.
- 18:05 unit costs and budget script run (src/strategy_budget.py): MUST 2,950 CPU-h, SHOULD 848 full / 326 reduced. Strategy §0-§4.5 written.
- 18:08 strategy §4.6-§4.12 appended (B3-B7, T1, T2).
- 18:10 strategy §4.13-§4.16 appended (S1, S2, P1, S3-S5).
- 18:12 strategy §5-§7 appended (systematics enumeration, reference analyses, labels).
- 18:13 strategy §8-§12 appended; artifact complete in first draft. Next: self-check pass, COMMITMENTS.md, logs.
- 18:14 self-check pass on the strategy: budget table re-added by hand against the script (MUST 2,950; full 3,798;
  reduced 3,275); C1 comparison count corrected 39 -> 41; one garbled criterion (T1-g) rewritten; a line reference
  to the novelty audit corrected (l.245). erf value for the trigger substitution recomputed with math.erf.
- 18:15 COMMITMENTS.md rewritten (45 plan-item rows incl. sub-commitments, 7 strategy rows, 18 systematic rows).
- 18:16 experiment_log.md ([Brigitte] block) and retrieval_log.md (7 look-ups) appended. No git add/commit.
- Open at hand-back: strategy is about 1,250 lines (longer than the 15-25 page target); retrieval tasks R-1..R-11
  unresolved by design; rho = 2 cost and memory, signal-row cost, MLM cost, toy cost for the real workspace unmeasured.
- 18:17 note: the milestone times above were first written as guesses and are now set from the system clock and the
  file modification times (plan 18:03, budget script 18:04, strategy last write 18:14, COMMITMENTS 18:15).
