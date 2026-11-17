# Orchestrator state (resume point)

A fresh session reads `prompt.md` (the brief), then this file, then resumes at "Next action".

**Updated:** 2026-11-17 08:14 -05 (measured) · **Branch:** `v2-jfc` · **Phase:** 2 (Exploration), day 0 of the calendar = 2026-11-16

**Gate A passed by the user 2026-11-16** with all defaults (`COMMITMENTS.md`, "Gate A answers"): 4,609 CPU-h approved,
stop-and-ask 5,992, about 60 days. Artifact of record: `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`.

**Running (2026-11-17 08:20, day 1):**
- **PILOT part 1** on schrodinger, 2 lanes (launched by the orchestrator 16 Nov 16:39): 149 of 500 jobs at 08:12,
  0 failed; ends about 18 Nov 17:30. Status `bash tools/runner/examples/p2x/pilot/STATUS_p2-c-pilot_mb-znn.sh`;
  resume = `bash tools/runner/examples/p2x/pilot/LAUNCH_p2-c-pilot_mb-znn_2slots.sh` (idempotent).
- **PILOT part 2 (B1 streams) READY, NOT LAUNCHED:** `tools/runner/examples/p2x/b1/` (762 jobs, 48 CPU-h, 91 GB;
  `phase2_exploration/outputs/B1_READY_albert_2026-11-16_20-24.md`). Launch ONLY after the user approves addendum
  D1–D9; the orchestrator launches (agents are refused by the permission system). The hs block needs the finished
  Z(νν) files. Slow-fragment residue: option (a) (β 0.1 kept, events flagged) unless the user objects.
- **WAITING FOR THE USER:** (1) addendum 1 v5 decisions D1–D9, deadline 18 Nov 14:00 (notice 16 Nov 18:33 + INFO
  20:28; document `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md`); (2) exception to the
  30-minute job rule for FxFx (two single-core jobs of ~1.5 h); (3) COMING: one DECISION notice on three Gate-A
  criteria that do not match what they can test — C1-b B₈₄ tolerance (FAIL as frozen on 29/86, within v1's MC
  scatter), C2-a V4-5 (expected FAIL as frozen on PU trials; Rosalie's result file pending), T1-b (Flora) — to be
  sent when V4-5 and T1-b numbers exist; they bear on decision point 1 (day 5 = 21 Nov).
- Agents: **Rosalie** (i; V4-5 result, then a successor takes the 41 C1 comparisons, T_seed, V4-4, sealed-comparison
  prep; projected all verdicts by Thu 19 Nov midday). **Edgar** (ii, Opus; f₂₀₀ after re-showers ~17:30, S2-b/d/e/f,
  retrievals, final EXPLORATION). **Albert** (iii; multi-lane launch test, then idle until the B1 launch).
  **Flora** (T1-b with jax on one schrodinger lane). Node shares: landau (i) 2 + (ii) 1; maxwell (i) 2 + (ii) 1;
  schrodinger pilot 2 + one lane for Albert/Flora (cap 3, graphical login).
- Settled on 16 Nov: toys (jax; 47/108/228 CPU-h at 60/80/100 parameters); half-turn limit kept as limitation
  [L15] by the user's option B (looper gun 0 of 2×10⁵); P1 readings (B* attribution not supported; population
  estimator fails at 3 of 5 points; no effect on the search); S2-a three validations PASS.
- After Phase-2 items close: consolidate `EXPLORATION.md` (channel files of Rosalie/successor, Edgar, Tatiana,
  Xavier, Albert, Flora), self-review + plot validator (JFC Phase-2 tier), decision point 1 and stop-rule
  checkpoint 1 at day 5, then Phase 3 (read the deferred JFC files first, DEVIATIONS V11).

**Orchestrator duties now:** commit on each report; resume executors; spawn the separate sealed C1 comparison session
when channel (i) has the campaigns and the tested script (writes only PASS/FAIL per criterion; six sealed points);
day 5 (21 Nov): decision point 1 (C1, C2) + stop-rule checkpoint 1 (re-project CPU with measured unit costs and
utilisation); consolidate `EXPLORATION.md`, self-review + plot validator (JFC Phase-2 tier), then Phase 3.
**Daily report** (user request; DEVIATIONS V14): `daily/YYYY-MM-DD.tex` + compiled `.pdf` (LaTeX, built in `/var/tmp/jdochoa/tex`), STATUS.md, bundle, then **commit and `git push origin v2-jfc`** (authorised by the user 2026-11-16 for the daily reports; never force) each evening; a session cron (18:47,
session-only, expires after 7 days: re-create) triggers it; if the session was restarted, re-create the cron.
**Notifications to the user (user instruction 2026-11-16, DEVIATIONS V15b):** `tools/notify/notify.sh <KIND> "<subject>" <body.md>`
writes a NEW FILE `notices/<date_time>_<KIND>_<slug>.md`, commits only it and pushes `v2-jfc` (the user watches the
repository by hand; no mail exists; nothing is pushed to `main` any more). Only the orchestrator notifies. Send one
ONLY when: (DECISION) a decision of the user is needed, with options, recommendation and deadline; (PROBLEM) a
cluster or infrastructure fault needs the user or an admin, or a stop rule fires; (RESULT) a result that changes the
expected outcome, a decision point or gate is reached, or a criterion fails. The evening daily report (LaTeX + PDF in
`daily/`) is itself the routine notice. Batch what arrives within about an hour. Each notice stands alone: numbers
with tags, what is asked, by when. No sealed signal quantity ever. When the user has answered a DECISION notice,
say so in the next notice or daily report.

**User's next interventions:** day 5 only if the stop rule fires or C1 fails after three remediation attempts;
**day 15 = 1 Dec: expected pause (Q2 a)**; freeze notification days 17–19 (3–5 Dec); Gate B about 4–6 Jan 2027;
Gate C about 13–15 Jan 2027.
Session names used through Tatiana; next free: Ulrich.

**Clock warning:** times in `LOG.md` and in file names before 2026-11-14 01:20 are sequence labels, not clock times;
git commit times are authoritative. Always call `date` before writing a time.

Read `LOG.md` entry "15:12 — INTERRUPTION" for the constraints in force (10 GB cap, nothing heavy on einstein, one
pixi install at a time, at most 3 subagents).

## Phase tracker
- [x] Preflight — PASS on re-run after the cajuela fix (`PREFLIGHT.md`)
- [x] Scaffold, state files, first bundle, first commit
- [x] Phase 1: Strategy — review PASS cycle 10; Gate A passed by the user 2026-11-16
- [ ] Phase 2: Exploration / regenerate the base — executor(s) + self-review + plot validator; decision point 1
- [ ] Phase 3: Processing, signal blind — parallel channels B1–B7, T1, T2, each 1-bot; consolidation; PREREG_v2 (4-bot, hash, notify user)
- [ ] Phase 4a: Expected — production, closure verdicts; executor + note writer + typesetter + 4-bot+bib
- [ ] Phase 4b: selection rule on optimisation half — executor + note writer + typesetter + 4-bot+bib → GATE B (human)
- [ ] Phase 4c: evaluation half — executor + note writer + 1-bot (escalate to 4-bot per JFC 06 §6.4)
- [ ] Phase 5: AN + journal paper + Zenodo-ready package — executor + note writer + typesetter + 5-bot + adversarial 25-question review → GATE C (human)

## Active subagents (at most 3 at a time; nothing heavy on einstein)
DONE and committed: investigators D1–D6 + `FRAMING.md` (`980d207`); feasibility C runner (`0ff12df`), B generators/Geant4
(`6c1b760`), A chain (`3502634`). Reports: `phase1_strategy/outputs/feasibility/FEAS_{A,B,C}_*.md` + `benchmarks_*.json`.

No subagent is running.

Phase-1 review history: cycles 1–9 all ITERATE (arbiters Dagmar, Eloise, Felix, Greta, Hugo, Johanna, Lena, Margaret,
Odette); A 11→4→1→0→0→0→0→0→0; B 24→14→15→5→3→1→4→1→1. Versions kept: v1 Brigitte … v9 Mireille
(`phase1_strategy/outputs/STRATEGY_mireille_2026-11-14_06-55.md` is the current strategy).
Settled (cycle-7, -8 and -9 arbiters): design, criteria, samples, budget 4,609 CPU-h / threshold 5,992 / 60 days incl.
the expected pause, default answers, expected outcome; day-15 family closed with script self-test and text checker.
If the user authorises cycle 10: fixer applies verdict-v9 edits (B-1 + E2–E14; the arbiter's tested script is
`/var/tmp/jdochoa/arbiter_odette/apply_edits.py`, to be used only as a reference) → v10; verification per verdict §9
(narrow, mechanical, fresh sessions: diff v9→v10 equals the edit list; checker 45/45; script output unchanged).
Draft Gate-A package: `gates/GATE_A_DRAFT.md` (1,496 words; describes v9 with the edits applied).
KEY FOR GATE A: expected outcome = background ≈ 0.7–1.0×10⁴ events (after CKF, as v1 counted) led by hard-scatter
conversions; reach below 243 GeV with the 0.17 normalisation width (bounds ≈ 180 GeV); day-15 pause expected; no
conversion rejection alone lifts it at v1's central decays-in-flight size (1–2 v1 counts). Q2 central; Df-11 new.

Geant4 env (per-worker local, V13): schrodinger, landau, maxwell all installed, stamps match lock `edbcef24…`.
Install slot for the shared home: FREE, nothing pending.

Session names used so far: Ada … Brigitte, Casimir, Celeste, Cosima, Dagmar, Dmitri. Dolores, Dorothea, Edmund, Eloise, Emeric. Estelle, Fabian, Fabiola, Felix, Fiona. Florence, Gerald, Gertrude, Greta, Gunnar. Hana, Hedwig, Hiroshi, Hugo, Ingrid. Isolde, Ivan, Jasper, Johanna, Jules. Katya, Kenji, Klaus, Lena, Leopold. Ludmila, Magnus, Marcel, Margaret, Mireille. Nadia, Nikolai, Nora, Odette. Next free: Oscar.
pixi 0.84.2 at `~/.pixi/bin`; every shell sources `tools/env.sh`.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
WAIT for the user's answers to the two items at the top. Nothing else.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
