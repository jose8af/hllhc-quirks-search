# Executor Edgar — Phase 2, channel (ii) (successor of Sebastian): S2-b…f, f₂₀₀, retrievals, P1 diagnostic, final EXPLORATION (session log, append-only)

Session start 2026-11-17 08:13 -05 (`date`). Read in full: PHASE2_BRIEF.md, AGENT_RULES.md, CLAUDE.md overrides, agents/executor.md,
ledger/README.md, phase2_exploration/CLAUDE.md, runner entry `tools/runner/bin/qv2run` (no separate runner README exists under
tools/runner; the campaign JSON schema read from Sebastian's campaign files), Sebastian's log (whole) and EXPLORATION_ii
(whole), LOG.md entries 16:12, 18:56, 22:41, 01:27, 08:14 (channel (ii) rulings), STR §4.14, §4.15, §6.4, COM rows S2-a…f,
P1-a…d, REF-2, B6-d, BL-1, retrieval_log.md #1–#23, src/s2/{f200,s2f_infracolour,resummino_job}.py, src/p1/{p1_runs,p1_eval}.py,
the diff nm_kernel.py → nm_kernel_t44.py, v1 NEAR_MISS_IMPULSE.md l.700-745 (floor tests as specified by v1).

## 0. State checked against the markers (08:15)
- `qv2run status`: p2-b-s2c-inc 25/25 done; p2-b-s2c-rs 27 done, 1 running, 22 pending (maxwell, 1 slot; driver pid 2338816).
- landau: my slot is lent to channel (iii) (Albert's multi-lane launch test, SLOTS.md 08:14, ≈ 20 min); 2 channel (i) jobs there.
- outputs/s2: kval, kref, kdy, kfactors (both PDF sets), met_compare; outputs/p1: p1_eval, floor_paired, m2_compare, p1d_table;
  outputs/dp5/mb_compare.json. All as Sebastian's RESUME STATE says.

## 1. Plan (written before any code or job)

Budget: channel (ii) ≈ 24 of 139 CPU-h used. Everything below adds ≈ 3 CPU-h (ESTIMATE). Stop-and-report threshold 181.
Rules kept: no git, no subagents, compute only through the runner, einstein only for editing and light stdlib/json scripts
(nice 19), `date` for every time, every lookup in retrieval_log.md, no installs (none planned).

| # | item | script(s) | campaign / where | CPU | order |
|---|---|---|---|---|---|
| D | P1 diagnostic: round-to-nearest 44-bit mdot (as Sebastian's caveat), plus RN at 47 bits (u′ = 64u, the precision v1's spec "44 bits (u′ ≈ 64u)" actually names: 2⁻⁴⁴/2⁻⁵³ = 512, not 64 — found while reading the spec); same events, settings and fractions as floor-e500/e1000-t44 | `src/p1/nm_kernel_rn.py` (copy of the t44 copy, rint instead of trunc, bits as a module constant set from an env var), `p1_runs.py` (+kernels rn44, rn47), `src/p1/p1_rn_eval.py` | `p2-b-p1-rn` (4 jobs), landau slot | ≈ 0.3 CPU-h | when landau frees |
| B-f | S2-f: δ(β) per mass from the generated β of the inclusive nominal samples (existing script, vectorised; marker-listed files only) | `src/s2/s2f_infracolour.py` | `p2-b-s2f` (1 job), landau | minutes | after D or with it |
| B-b | S2-b: σ_norm(m) table, both PDF sets, scale and PDF errors (from kfactors.json; einstein light script); resummed cross-check: Resummino NLO+NLL/NLO for the decoupled scalar at all 14 masses, CT18NLO and PDF4LHC21 | `src/s2/sigma_norm_table.py`, `resummino_job.py` (+ --pdf, --decouple for NLL) | `p2-b-s2-nll` on maxwell after s2c-rs (Resummino env exists only node-local on maxwell) | ≈ 1.5 CPU-h | queued behind rs |
| B-d | S2-d: QED-FSR nominal statement from the 25 inc chunk JSONs (nominal.qedfsr) and the Pythia card | read-only | — | 0 | now |
| B-e | S2-e: turn-on from L1 TDR Table 4.1 p. 210 (50 % 128, 90 % 200 GeV vs gen MET), Fig. 3.125 p. 188 read for the plateau; erf parametrisation through the two points (ESTIMATE); branch decision facts (no stated uncertainty) | `src/s2/trigger_turnon.py` (stdlib) | einstein light | 0 | now |
| C | Retrievals: status table R-1…R-20; web for R-7, R-15, R-16, R-17, R-18 (day 15), R-12, R-14 (freeze); log each | — | web | 0 | now, interleaved |
| A | f₂₀₀: f200.py reworked (file list from done markers of s2c-inc and s2c-rs; 7- and 9-point scale; CT18 Hessian 90 % CL and its 68 % equivalent if a source gives the conversion; variant shifts with stat errors; asymmetric log-normal κ; v1 comparison) | `src/s2/f200.py` | `p2-b-s2c-f200` (1 job) after rs completes (~17:30) | minutes | after rs |
| E | final EXPLORATION_ii_edgar_<stamp>.md; DAILY_NOTES at each report | — | — | 0 | last |

Checks: the RN kernel reproduces nominal to ≤ 1e-3 relative in Δs at f = 1 for p ≥ 47 bits (sanity), and t44 vs rn44 differ;
S2-f substitution check reproduces STR's 0.045 / +3.3 / +6.3 / +13.3 %; f₂₀₀ nominal against v1 values (0.04764, 0.10418,
0.14585, 0.16876, 0.1135); the σ_norm table reproduces kfactors.json numbers exactly.

Reports: (1) after B–D (except f₂₀₀ and the NLL scan); (2) at f₂₀₀; (3) at the final file.

## 2. Log
- 2026-11-17 08:18 plan written.
- 08:20 D: `src/p1/nm_kernel_rn44.py`, `nm_kernel_rn47.py` generated from nm_kernel_t44.py (only the docstring, `_rn` and `mdot` differ; diff checked); stdlib unit check of the rounding: max rel. error 5.67e-14 ≤ 2⁻⁴⁴ and 7.10e-15 ≤ 2⁻⁴⁷ over 2×10⁵ random values, ties to even checked. **Finding:** v1's spec "44 bits (u′ ≈ 64u)" is inconsistent: 2⁻⁴⁴/2⁻⁵³ = 512; 64u is a 47-bit significand. Both are run. `p1_runs.py` accepts kernels rn44, rn47. Campaign `tools/campaigns/p2-b/p2-b-p1-rn.json` (4 jobs: e500/e1000 × rn44/rn47, same 40 events, s = 1/9, fractions as t44).
- 08:22 S2-f script reworked (files from done markers with sha256 check; vectorised; weighted β quantiles; weight fraction at β < 0.1); `src/s2/marker_files.py` (done-marker file lists) written. Campaign p2-b-s2f (1 job).
- 08:23 S2-d checked: all 25 p2-b-s2c-inc chunk JSONs (done markers) have nominal {tune CP5, qCut 45, xqcut 30, qedfsr true}, 100,000 LHE per species-mass; the card `sim/cards/pythia8_quirk_qedfsr.dat` (3 lines: SLHA:useDecayTable off, 9000011/9000013 isResonance on). `s2_job.py` makes QED-FSR opt-in (`--qedfsr`); channel (i)'s C1 Stage-2 campaigns do not pass it (correct for C1: v1 had no QED FSR).
- 08:21–08:28 Retrievals R-7, R-15–R-18, R-14, R-12, CT18 CL, L1 TDR Fig. 3.125: retrieval_log #24–#31.
- 08:26 landau slot free again (Albert's test ended); chain_edgar.sh started (p2-b-p1-rn → p2-b-s2f), then chain 2 (p2-b-p1-rneval → p2-b-s2c-f200t, a partial-data code test of f200.py). SLOTS lines appended.
- 08:29 S2-e: `src/s2/trigger_turnon.py` → `outputs/s2/trigger_turnon.json` (Fig. 3.125 readings; 2-point erf μ 128, σ 56.18 GeV; v1 function reproduces STR's 0.974 at 250 GeV).
- 08:31 f200.py reworked (see docstring); campaigns p2-b-s2c-f200t (test) and p2-b-s2c-f200 (final). Resummino job takes --pdf; campaign p2-b-s2-nll (6 jobs). maxwell: `queue_maxwell_edgar.sh` started (waits for "queue_maxwell5 end", then f200 → nll). `src/s2/sigma_norm_table.py` → `outputs/s2/sigma_norm.json` (R column empty until p2-b-s2-nll).

## State for a successor (2026-11-17 08:33 -05)
- landau: chain_edgar1 (p2-b-p1-rn → p2-b-s2f) then chain_edgar2 (p2-b-p1-rneval → p2-b-s2c-f200t). Logs landau:/home/scratch/jdochoa/drivers/chain_edgar{1,2}.log.
- maxwell: Sebastian's queue_maxwell5 (p2-b-s2c-rs) → my queue_maxwell_edgar.sh (p2-b-s2c-f200 → p2-b-s2-nll). Log maxwell:/home/scratch/jdochoa/drivers/queue_maxwell_edgar.log.
- After nll: rerun `python3 -I src/s2/sigma_norm_table.py outputs/s2/sigma_norm.json` on einstein (stdlib) to fill the resummed column.
- After f200: copy the f200.json from data/p2-b-s2c-f200/000 to outputs/s2/f200.json; write the f₂₀₀ section.
- 08:37 S2-f done (p2-b-s2f → outputs/s2/s2f_infracolour.json): substitution check reproduces STR (α 0.0448; δ 3.26/6.28/13.32 %). Mean δ at 1 keV: E200 5.68 %, E500 6.14 %, E1000 7.03 %, E1500 7.94 %, Ẽ500 3.60 % (S-wave form; the P-wave scalar needs its own factor).
- 08:38 D done (p2-b-p1-rn 4 jobs, p2-b-p1-rneval → outputs/p1/p1_rn_eval.json): rn44 ≈ t44 (KS p 1.4e-10 / 1.2e-7: the rounding mode is not the cause); rn47 (u′ = 64u): KS(nominal Δc(20), rn47 Δc(2.5)) p = 0.53 / 0.47; medians 0.0043 vs 0.0032 (E500), 0.0109 vs 0.0080 (E1000). Diagnostic only.
- 08:40–08:46 f200.py tested on partial re-showers (p2-b-s2c-f200t; test2 failed by design on a partial chunk-tag mismatch, fixed: key on chunk number). Paired shift errors via LHE-momentum matching work (self-check 0). Orchestrator 08:4x: no interim reports; one final report ≤ 15 lines.
- 09:35 EXPLORATION_ii_edgar_2026-11-17_08-17.md written except the placeholders CAMPAIGN-TABLE-PLACEHOLDER, TABLE-CPU, SIGMA-NORM-ROWS, NLL-RESULT-PLACEHOLDER, F200-PLACEHOLDER, RS-COST, RESUMMINO-COST (filled after maxwell's p2-b-s2c-rs → p2-b-s2c-f200 → p2-b-s2-nll). Experiment log appended.

## State for a successor (update 2026-11-17 09:35 -0500)
- Waiting (background) for maxwell: queue_maxwell_edgar.sh → p2-b-s2c-f200 then p2-b-s2-nll. Check: `ssh -x maxwell tail -3 /home/scratch/jdochoa/drivers/queue_maxwell_edgar.log`.
- Then: cp data/p2-b-s2c-f200/000/f200.json → outputs/s2/f200.json; rerun `python3 -I src/s2/sigma_norm_table.py outputs/s2/sigma_norm.json` and `python3 -I src/s2/cpu_tally.py outputs/s2/cpu_tally.json` (einstein, stdlib); fill the placeholders; one final report ≤ 15 lines (orchestrator instruction), DAILY_NOTES two lines.
- landau slot: idle (all my landau work done).
- 10:29 **FxFx exception** granted by the user on 2026-11-17 (relayed by the orchestrator): two single-core first-launch jobs of ≈ 1.5 h, E 500 and 1500, maxwell only; later gen batches ≤ 30 min. Recorded in tools/campaigns/p2-b/p2-b-s2-fxfx.json (description + per-job timeout_exception, timeout_s 6000). **Blocker:** the runner hard-codes MAX_JOB_SECONDS = 1800 (tools/runner/qv2run/paths.py:24; campaign.py:109-110 rejects the campaign). Not changed by me (outside my write scope); orchestrator told via SendMessage with a 6-line proposal. s2_job.py fxfx gained --save-procdir / --restore. p2-b-s2-fxfx-c (compile, ≤ 30 min ×2) + p2-b-s2-fxfx queued by queue_maxwell_fxfx.sh after queue_maxwell_edgar.
- 16:54 p2-b-s2c-rs complete (50/50); p2-b-s2c-f200 done → outputs/s2/f200.json. 17:37 p2-b-s2-nll done (6/6) → sigma_norm.json resummed column. EXPLORATION_ii_edgar final written (all placeholders filled). FxFx: orchestrator decision 2026-11-17: runner not changed now; compile jobs p2-b-s2-fxfx-c running on maxwell since 17:37; p2-b-s2-fxfx prepared, NOT submitted.

## State for a successor (final, 2026-11-17 17:38 -0500)
- Channel (ii) is finished except FxFx. maxwell runs queue_maxwell_fxfx.sh: p2-b-s2-fxfx-c (2 compile jobs), then it logs that p2-b-s2-fxfx is rejected by the runner and ends. Log: maxwell:/home/scratch/jdochoa/drivers/queue_maxwell_fxfx.log.
- After the runner change (orchestrator, ≈ 19 Nov): follow EXPLORATION_ii_edgar §2.8 (commands; the FxFx f₂₀₀ comparison; band enlargement rule).
- CPU: 39.5 CPU-h charged (38.3 marker CPU-h) for channel (ii) at 17:38.
