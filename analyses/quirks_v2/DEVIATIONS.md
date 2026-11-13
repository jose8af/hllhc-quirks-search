# Documented deviations from the JFC design

Each is required by the user's brief (`prompt.md`) or by the environment. None removes a review, a gate or an artifact.

| # | JFC default | Here | Reason |
|---|---|---|---|
| V1 | each analysis is its own git repo (scaffolder runs `git init`) | nested `.git` removed; commits go to the parent repo, branch `v2-jfc` | brief §2: one repo |
| V2 | `conventions/`, `methodology/`, `agents/` are absolute symlinks into a separate JFC checkout | relative symlinks into `tools/jfc/src/`, vendored at commit `9eecb0e0` | portability of the single repo |
| V3 | `experiment_log.md` at the analysis root | named `LOG.md` | brief §7 |
| V4 | all subagents `model: "opus"` | Opus by default; other models where the orchestrator decides, logged in `MODEL_LEDGER.md` | brief §4 |
| V5 | SLURM for jobs over 15 min | Argo Workflows / SSH runner on the lab minicluster | brief §5.3 |
| V6 | human gate only after 4b | three human gates: A (after Phase 1), B (4b → 4c), C (final paper) | brief D7 |
| V7 | Phase 4b = 10% of real data | no collider data: 4b = selection rule on the signal optimisation half; 4c = evaluation half | brief §6 |
| V8 | RAG corpus via MCP | none available; repo literature cache and public sources, logged in `retrieval_log.md` | environment |
| V9 | `pixi.lock` git-ignored | `pixi.lock` tracked | reproduction package (brief §6, Phase 5 iii) |
| V10 | mplhep experiment label ("CMS Open Data" style) | "Private work (simulation)", no experiment name | brief §6 Phase 5 |
| V11 | orchestrator reads all JFC files at start | read at start: README, methodology README, 01, 02, 03 (philosophy + Phase 1), 03a, 04, 05, 06, 12, appendix-prompts, appendix-sessions, agents README/executor/investigator, root and phase-1 templates, conventions README/search, scaffolder. The remaining files (03 Phases 2–5, 07, 09, 11, analysis-note, other appendices, other agent definitions, phase 2–5 templates) are read at the start of the phase that uses them, before spawning the agent concerned | context economy over a multi-week run; flagged to the user 2026-11-13 |
| V12 | brief §5.1: einstein may run up to 3 niced heavy jobs, builds and light jobs | nothing heavy on einstein at all: no installs, solves, builds, benchmarks | user decision after the 15:12 out-of-memory incident, 2026-11-13 |
