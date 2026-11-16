# Status — quirks v2

**2026-11-16 10:53 -05 (measured).** Phase 1 (Strategy): **review PASSED in cycle 10; stopped at human Gate A.**

- Gate package: `gates/GATE_A.md` (five questions Q1–Q5, eleven overridable defaults, budget, risks).
- Artifact of record: `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md` (v10,
  sha256 `d806bb36…020b779`), `COMMITMENTS.md`, `phase1_strategy/outputs/budget_stdout_v9.txt`.
- Verdict: `phase1_strategy/review/arbiter/STRATEGY_ARBITER_v10_quentin_2026-11-16_10-51.md` (0 A, 0 B, 2 C; the one
  C edit is applied).
- Nothing runs. No production, no worker job and no CPU-h are spent until Gate A is answered.

| | |
|---|---|
| Schedule | proposed at Gate A: 4,609 CPU-h, stop-and-ask at 5,992, about 60 days (ESTIMATE) |
| CPU-h used / planned | 0 of production / to be approved at Gate A |
| cajuela, this project | under 1 GB of 1.5 TB soft budget (bundles only) |
| last repo bundle | `repo-2026-11-16.bundle` |
| Review history | A 11→4→1→0→0→0→0→0→0→0; B 24→14→15→5→3→1→4→1→1→0 |

**Incidents so far:** 13 Nov 14:06 stale file handle after a directory rename on cajuela (admin fix); 13 Nov 15:12
einstein out of memory (orchestrator now capped at 10 GB); 14 Nov about 00:47 to 16 Nov cajuela NFS and ssh to the
workers hung (cause not established by us; the user confirmed the cluster healthy on 16 Nov).

**Limits in force:** 10 GB cap, nothing heavy on einstein, one pixi install at a time, at most 3 subagents, never
rename a directory on cajuela, no push.

**Open risks:** see `gates/GATE_A.md` §7. The expected outcome on v1 placeholder efficiencies is a real background
and a reach near existing bounds; the day-15 rule is expected to pause the study.
