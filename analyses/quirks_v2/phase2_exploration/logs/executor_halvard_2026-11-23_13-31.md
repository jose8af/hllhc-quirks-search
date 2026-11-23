# Halvard (Opus, channel (ii) successor of Sune), FxFx E 1500 — session log

## Plan (2026-11-23 13:31 -0500)
Inputs read: AGENT_RULES.md, PHASE2_BRIEF.md, Sune's log and `outputs/FXFX_sune_2026-11-19.md` (§6-§7), LOG.md
19 Nov 14:26-17:22 and 23 Nov 13:30, SLOTS.md tail, campaigns `p2-b-s2-fxfx-e1500.json` / `p2-b-s2-fxfx-gen1500.json`,
`s2_job.py cmd_fxfx`, `f200_fxfx.py`.

1. **Wait** for `fxfx-e1500-grids4` (dispatched 13:27:06 by the orchestrator, maxwell, timeout_exception 7,200 s,
   user 19 Nov; expected ≈ 6,900 s ESTIMATE → ≈ 15:22, hard stop 15:27). Background wait on its marker (no polling).
   At 13:31 maxwell runs grids4 (madevent_mintMC) + 2 D2 find jobs (load 3.1).
   - timeout → record E 1500 FxFx **NOT DONE** (user rule: no further retry), read-only diagnosis, stop.
   - failed → read-only diagnosis of the cause, record, stop (no retry without the orchestrator).
2. **If done:** E 1500 gen batches = Sune's pre-written campaign `p2-b-s2-fxfx-gen1500` (6 × 15,000 LHE events,
   `--stage gen --shower --restore`, each job ≤ 1,800 s, no exception), with the `--restore` path changed from the
   never-produced grids3 procdir to `fxfx-e1500-grids4.procdir.tar.gz`. On maxwell the node-local `E_m1500` dir
   (COMPILED + READY from grids4) is used directly; the tarball is only for another node.
   - Sizing (ESTIMATE): matched ≈ 63 % (E 500), negative weights ≈ 17-20 % → N_eff ≈ 90k × 0.63 × 0.36-0.42 ≈
     2.0-2.4×10⁴; with f ≈ 0.168, σ_f/f = √((1−f)/(f·N_eff)) ≈ 1.4-1.6 % (target ≈ 2 %, as E 500's 1.6 %).
   - Time per job (ESTIMATE): E 500 20k took 619-658 s; E 1500 ≈ 1.3× slower per event (Sune §6.1) → 15k ≈ 650 s.
     Job 01 checked before trusting the rest; all 6 ≈ 1.1 CPU-h.
   - Launch: SLOTS.md line first (node count ≤ 4 checked), driver on maxwell itself (workers cannot resolve each other):
     `ssh -x maxwell "nohup $R/bin/qv2run ssh launch $C/p2-b-s2-fxfx-gen1500.json --nodes maxwell --max-per-node 1 --on maxwell"`;
     jobs run nice 10 (runner).
3. f₂₀₀^FxFx(E 1500) with `f200_fxfx.py E1500` (sim `ana` env, on maxwell) → `outputs/s2/f200_fxfx_E1500.json`;
   compare with MLM nominal 0.16755 ± 0.00185, band +5.96/−5.94 % (κ 1.060/0.941) [VERIFIED, outputs/s2/f200.json
   points.E1500]; enlarge the band if the central value lies outside (STR l.2021-2022).
4. Write `outputs/FXFX_E1500_halvard_2026-11-23.md`, experiment_log.md entry, commit (plan + campaign before
   production; results after).

CPU budget (ESTIMATE): grids4 ≈ 1.9 CPU-h (already approved and running) + gen ≈ 1.1 CPU-h + analysis < 0.01.

## Entries
- 2026-11-23 13:31 -0500 plan written; background wait on the grids4 marker started.
