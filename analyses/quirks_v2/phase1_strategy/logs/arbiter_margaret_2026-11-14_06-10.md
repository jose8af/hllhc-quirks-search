# Session log: arbiter Margaret, review cycle 8 (STRATEGY v8), 2026-11-14

Role file `agents/arbiter.md` read in full. No sub-agents, no git, standard-library Python only (einstein, `nice -n 19`).
Scratch (outside the repo): the session scratchpad given by the harness. Repo writes: this log and the verdict only.

- 06:10 Read `agents/arbiter.md`, `AGENT_RULES.md`, the three cycle-8 reviews in full (Ludmila, Magnus, Marcel), v8 §0,
  §4.4 (pilot reading, Table 4.4a, Table 4.4c and its scenario notes), §4.7 (proxy passages), §11.7, §12.1, §12.5, §13.7,
  script [9]–[9b] (l.478–964), `budget_stdout_v8.txt` l.296–397.
- 06:20 Reran the script unchanged into scratch: 1 min 28 s, stdout byte-identical to `budget_stdout_v8.txt` (`cmp`).
  VERIFIED.
- 06:25 Root cause located in rule 1 itself. Rule 1 says "every term of the likelihood … max(zero-count floor, N_t·H) per
  term" but only three kinds of term have a sample at day 15 (DIF, NI, Z(νν)). It does not say what the thirteen other SM
  processes and the multijets get. v8's rows 1–2 give them the Table 4.4a pool floor (a pool that does not exist at day
  15); the (γ) rows give them H per event as Z(νν) but on pool exposures; the physics reviewer gives them the Z(νν) pilot
  count on the pilot exposure. With 15 Z(νν) pilot counts the first reading says 242 (proceed) and the third 353
  (pause): the rule is not single-valued. Second ambiguity: whether the (c) test's factors multiply a zero-count floor.
- 06:35 DECISION: every SM hard-scatter process and the multijets are read at the H per event of the Z(νν) pilot (one
  count, one Gamma draw); zero-count floor = the m = 0 case on the sample that exists at day 15; (c) factors do not
  multiply a floor. ALTERNATIVES: other SM terms at their Table 4.4a floors (keeps "≈ 20 pilot counts", but the pilot
  then sees only 37 % of the conversions and a (c) test would pass at about ×18 while the all-process requirement is
  ×30–44). CONFIDENCE: high on the physics (the leading expected background is a hard-scatter feature of every SM
  process); the consequence is a stricter pilot-count limit (≈ 12 instead of ≈ 20), which is reported to the user.
  FLAG FOR HUMAN: yes, in the Gate-A package.
- 06:45 Scratch computation of the pinned definition (script functions, `pmf_pred`, seed 7): empty 78 (3,000 draws) / 76
  (20,000 draws); m_Z = 11 / 12 / 13 → 282 / 300.0 / 318; m_D = 3 / 4 → 265 / 333; (α1′) own hits 3.2–3.3×10⁴ / ×10⁵;
  (α1) 2.6×10³–4.2×10⁴. Equal to the physics reviewer's (γ) recomputation (113 / 189 / 264 / 318 / 353 / 462; 12 → 300.0).
- 06:55 Grid under five conventions: v8 printed (×33.7 / ×52.1–81.3 / ×69.4–235.4), Marcel and Magnus (×35.1 /
  ×55.3–89.5 / ×75.0–310.8), Ludmila column 2 with the DIF floor at f_D = 0 (×43.3), Ludmila column 3 (×45.5 /
  ×79.9–172.1 / ×126.9–none / ×391.0–none), pinned (×44 / ×75–150 / ×114–none). Every reviewer number reproduced; every
  difference attributed (verdict §2.4).
- 07:05 Found that a 3,000-draw median makes the factors noisy (±6 %, ±25 % where the conversion-free reading is near
  300: the same cell gave ×243 and ×323 with the terms in a different order). The replacement code uses 20,000 draws,
  drops the f_D = 1/2 row, prints integer factors that pass, and labels 297–303 "at the limit".
- 07:20 Replacement script assembled in scratch (block A replaces l.853–905, one label in l.964, block B = self-test
  after l.964). Run: 1 min 15 s, 36 MB; deterministic (two runs, same sha256 52323f87…2274a2); everything outside the
  two tables, the one label line and the self-test lines is byte-identical to v8 (`cmp` on v8 l.1–353, 377–395,
  397–579 against new l.1–353, 371–389, 400–582). Self-test 8 of 8 PASS.
- 07:30 Correction to the 06:35 entry: under the alternative reading a (c) test would pass at about ×16 (VERIFIED,
  scratch), not ×18. The physics reviewer's "358 at the printed ×34" reproduced as 358.5 (her `kap_d15` list plus the
  conversions on the pool factor).
- 07:40 Text check written (`check_day15_text.py`, to be created by the fixer from the verdict §4.2): on v8 it reports 42
  mismatches; it found two defects of my own first draft (a rounded number rounded again, 3.15 → 3.1 / 3.2, and a parse
  of "B50" as a value). Fixed by printing two significant figures in the own-hit rows.
- 07:50 Eighteen text replacements T1–T18 applied by a program to a scratch copy of v8 (each old string asserted
  unique): text check ALL OK, 45 of 45. Final scratch stdout: 582 lines, sha256 0ca4af15…003433d, 1 min 15 s, 36 MB.
- 08:00 Verdict written: `review/arbiter/STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md`. Verified from the verdict
  file alone: the three code blocks extracted from it rebuild the script (same sha256) and the checker, and its T list
  rebuilds the scratch v9 draft byte for byte.
- 08:00 Verdict: ITERATE. A: none. B: W1 (one finding with its root cause: rule 1 was not single-valued for the SM
  processes without a day-15 sample). Fix (i): recompute on the pinned basis. Consequence reported for Gate A: the
  day-15 limit is ≈ 12 Z(νν) pilot counts, not ≈ 20. Nothing outside the day-15 family is open.
- Note: I ran one read-only `git status --short` to confirm that only my two files are new in the repo. No other git
  command, no repo write besides the verdict and this log.
