# HASH_ADDENDUM: additive changes to hashed Stage-4 files after the WP_RULE freeze (G1b, 2026-10-13)

> **2026-10-14 00:35, orchestrator decision (admission).** This addendum (§1–§5) is part of WP_RULE A.3 for the
> item-11 admission (§5.4): every change it records is either bit-identical in regression (§1–§3, §5 scheduling/timing)
> or the pre-declared T_seed action (§5). WP_RULE.md itself is not edited.
>
> **2026-10-14 01:50, orchestrator instruction (user-approved PC-19).** `acts/stage4/WP_RULE_PC19.md` (sha256 in §6) is
> part of A.3. It amends WP_RULE for all SR-T quantities and takes precedence there.

`WP_RULE.md` and `frozen_inputs.json` are not modified. This file records every post-freeze change to a file whose
sha256 is listed in `frozen_inputs.json` (Appendix A.3), with the reason and the regression evidence. Executor G1b.

## Status at writing (20:40): PREPARED, NOT YET APPLIED

**Update 2026-10-14 00:16: APPLIED** by `validation/g1b_post_g3.sh` after G3 exited (shas 1258e82a… / bdea0e27… confirmed; PU/SM/dens regression on the applied files bit-identical 97/86/82 keys, `data/acts_stage4/g1b/regress_before_vs_after_applied.json`). `frozen_inputs.json` was later changed by the pre-declared T_seed action, §5.

The G3 pilot was still running (`pgrep -f "run_stage4 run --campaign G3"`; ETA ≈ 22:58). G3 has two dependencies on
these files:
- it calls `code/run_chain.py` once per job;
- each G3 output records `run_stage4.py`'s sha256 when the job ends. WP_RULE §5.4 item 11 admits G3 to the union only
  with the frozen hashes.

So neither file was touched. Both patches are exact-anchor scripts. Each one:
- refuses while a `run_stage4 run` process is alive;
- refuses unless the target has the frozen sha256;
- was applied to a candidate copy and tested there.

**Apply right after G3 exits** with `acts/stage4/validation/g1b_post_g3.sh`. It runs:
1. both apply scripts;
2. a check that each resulting sha256 equals the tested candidate's;
3. deletion of the candidates;
4. the PU/SM/dens regression on the applied files;
5. regeneration of `jobs/C1.json`.

It does not launch C1.

## Changed files (old → new sha256)

| file | frozen sha256 | new sha256 (after apply) | reason |
|---|---|---|---|
| `acts/stage4/run_stage4.py` | `85b978f5d85cee28d290d298bb96bb9895299f916bc4df632a9cf2bb66a4879e` | `1258e82a6ba0fd34d14c9aa6293075ef6e23bd6b90c0ff96298ef0b7dc07571c` | G1b job kinds hook (below) |
| `acts/stage4/code/run_chain.py` | `b1130b40f6c729a1145d23ad15b8a176060d0cf3b718e8794f2efe5a9819e8c0` | `bdea0e276e30473908f93b7b23e75d3876e4d6b43893b78077accf21f24aec8d` | ACTS navigation-assertion recovery (G3 failures, below) |
| `acts/stage4/finder/chain_inputs.py` | `8f5a8177…` | unchanged | — |
| `finder/production.py`, `finder.py`, `kernels.py`, `weights.py`, `pu_inputs.py`, `eloss.py` | frozen | unchanged | — |

**New files.** They are not in the frozen hash list; their sha256 is recorded in every G1b output as `meta.g1b_sha256`.

| file | sha256 at writing |
|---|---|
| `acts/stage4/run_g1b.py` | `0f8989bf9828c0de1b55499a309daedd90d80e0993c5935ed3d3c1821fe188ed` |
| `acts/stage4/finder/g1b_tt.py` | `a2e4ddffe751628eb18a297731d5fd4bfeecb3f9b36937d4664a09f6bdfaaead` |
| `validation/g1b_apply_hook.py` | `d8219d80cbb4f6155013bc845882e924ae85a72256df250f333f667b00b065b9` |
| `validation/g1b_apply_chainfix.py` | `904e53943e1f65486d1a8c91d3fe7b006cbaef41fd091d96b03327645f1e6c5f` |
| `validation/g1b_regress.py` | `1dd7b17e10a50470c205abb4d3fb88146b0f81bf3ba4eec81720150e353e557a` |
| `validation/g1b_chainfix_test.py` | `f2a6808f5fd0035dd1c93e32a7141a102e68d359c929b5db65dae52232f15a03` |
| `validation/g1b_post_g3.sh` | `964f2c83afce13ef538b1675a249c504d540dd785be416fce9dc07ecfe55654e` |

Frozen copies of the two old files: `data/acts_stage4/g1b/frozen_copies/` (read-only).

## 1. `run_stage4.py`: G1b hook (6 anchored insertions; `validation/g1b_apply_hook.py`)

1. `G1B_KINDS = ('a1','a2','a5','cp0','cppu')` is added to `RUNNABLE`.
2. `make_manifest` appends `run_g1b.manifest_jobs(camp)`. The G1_BLOCKS placeholders A1/A2core/A5core/Cp0/CpPU are
   skipped when G1b jobs exist. `val` stays a placeholder.
3. `validate()` dispatches G1b kinds to `run_g1b.validate`.
4. `_safe_run` dispatches G1b kinds to `run_g1b.run_job`.
5. `needs` may be a list. C′_PU needs every C′₀ job of its topology. A string behaves as before.
6. `check` also reports V4-10 for C′ outputs: the C′₀ leak count, the C′_PU per-event hash and the implication
   control.

None of these paths runs for the kinds `pu`, `sm`, `dens`.

## 2. `run_chain.py`: navigation-assertion recovery (8 anchored insertions; `validation/g1b_apply_chainfix.py`)

**Failure (G3B1_00021, G3B1_00059).** `Sequencer.run()` raised
`Checking volume outside of bounds: Assertion 'surface().insideBounds(position, BoundaryTolerance::None())' failed`
(`GridPortalLink.hpp:584`) and the whole chain job died.

**Investigation** (`data/acts_stage4/g1b/navfix/`):
- **The failing event is reproduced.** The failing event of G3B1_00021 is event 3, with seed
  hseed('pu', 85067245817463, 3) = 3930681229184174995.
- **It is in the Fatras simulation, not the CKF.** The same 4 events with `--no-ckf` fail identically
  (`inv_nockf.log`).
- **It looks like a φ-sector-boundary artefact.** The same events on the 1-sector geometry (`--nphi 1`) run
  (`inv_n1.log`). The Gen-3 grid portals between the 32 φ-sectors are the likely place.
- **Rate:** 2 failures in ≈ 56 G3 jobs × 25 events, i.e. ≈ 1 event in 700.

**Why no geometry fix.** A geometry or tolerance fix would change every event, so PU-only outputs would not stay
bit-identical.

**Fix.** If `s.run()` raises this assertion:
1. The failing event k is the first event without a Dump record.
2. The job is re-run in-process (fresh geometry and sequencer) with `--replace-event k`. Event k's generator seed
   becomes hseed('nav-replace', mode, job seed, k, old seed) (deterministic).
3. At most 5 replacements per job; any other error is re-raised.

The replaced events (event, old seed, new seed, reason) are written to `chain_meta.replaced_events`, and therefore to
the job output meta. The modes `pu`, `sm`, `sig`, `cp` and `cppu` are covered; `gun` is not. The TT side is
unchanged: the number of events is unchanged and the TT seed streams are per event index.

**Bias note (flag).** Replacing an event conditions on "no navigation assertion". That is a geometric artefact, not a
physics selection, and affects ≈ 0.14 % of events. The replaced ids are listed per job, so they can be dropped or
studied.

## 3. Regression evidence

| test | result | file |
|---|---|---|
| PU-only (1 ev × 2 roads, with S6 dump), SM Z(νν) (1 ev), dens low (1 ev × 2 roads); frozen config. Frozen `run_stage4.py` (before) vs the patched candidate module `_rs4_candidate.py` (sha 1258e82a…) | **bit-identical**: pu 97/97, sm 86/86, dens 82/82 keys. Wall-clock timers (`trials.times`, `trials.t_total`, `chain.timing`) and `meta_json` are excluded | `data/acts_stage4/g1b/regress_before_vs_after_candidate.json` |
| determinism control: before vs before2 (same code, rerun) | bit-identical | `regress_before_vs_before2.json` |
| chain fix: frozen `run_chain.py` vs patched candidate (sha bdea0e27…), 3 PU events | **every array bit-identical** without replacement. With `--replace-event 1`, events 0 and 2 are bit-identical, event 1 is replaced and the meta records it | `data/acts_stage4/g1b/navfix/chainfix_test.json` (PASS) |
| failing G3 job G3B1_00021 (25 events) through the patched candidate | completes; event 3 replaced (old 3930681229184174995 → new 124286083603878367); V4-1 PASS | `navfix/G3B1_00021.log` |
| applied files (after G3) | to be run by `g1b_post_g3.sh`: `regress compare before after_applied` | `regress_before_vs_after_applied.json` (pending) |

The candidate and the applied files are byte-identical by construction: the same anchored script on the same frozen
input, and the post-G3 script checks both sha256 values.

## 4. G3 provenance consequence (for the orchestrator)

- The 128 successful G3 jobs are unaffected: they were produced with the frozen hashes.
- The 2 failed G3 jobs can only be produced with the patched `run_chain.py` (bdea0e27…) and `run_stage4.py`
  (1258e82a…). For PU-only jobs that hit no assertion, both files are bit-identical in output to the frozen ones.
- If they are re-run (`run_stage4 run --campaign G3 --workers 2` after the patch), their outputs carry the new
  hashes and list the replaced event.
- Admitting them to the union under WP_RULE §5.4 item 11 is an orchestrator decision. Accepting this addendum as part
  of A.3 is the natural reading.

## 5. T_seed := 4 (G3 §4, WP_RULE §6.4 pre-declared action)

Applied 2026-10-14 00:18:48 (local, -05) by the Stage-4 C1 launch executor on orchestrator instruction. Authority:
WP_RULE §6.4 ("if at G3 the per-family pass fractions move by > 2σ between T_seed = 6 and 4, T_seed(ρ) := 4, the jobs
are re-timed (G2b criterion) and the change is logged; this is the only pre-declared T_seed action"); G3_REPORT §4
(R06 trial pass fraction +16 %, z = +3.16 at ρ = 1; +37 %, z = +2.61 at ρ = 2). `WP_RULE.md` itself is NOT modified
(sha256 1b2ea9bd… unchanged, so `run_stage4 run` still passes its WP_RULE check).

| file | old sha256 | new sha256 | change |
|---|---|---|---|
| `acts/stage4/frozen_inputs.json` (read-only; chmod u+w → edit → chmod a-w) | `7574e0b570413218871d319bf0958e473664066d2c8835cd636fa97c7a714902` | `2adc8f9d9e71fc6fc6763a5a4e74d157ae06773df7133ffcddccc3de42368928` | `"t_seed": 6 → 4`; `finder_config` `{"road": 0.15}` → `{"road": 0.15, "tseed": 4}` (the key `production.config_from_frozen` applies to `finder.Config`, for every job kind and both ρ). Nothing else changed |
| `data/acts_stage4/frozen/frozen_inputs.json` (A.4 copy, used by dev campaigns) | `7574e0b5…` | `2adc8f9d…` | identical edit; the two copies are byte-identical |
| `acts/stage4/run_stage4.py` | `1258e82a6ba0fd34d14c9aa6293075ef6e23bd6b90c0ff96298ef0b7dc07571c` (G1b, §1) | `0d122cfc3fbc0d3baac92651260b7870c086d7b74153709997769d855518f5f9` | re-timing constants + C1a/C1b/C2B sub-run campaigns (below); no change to any job-execution path |

**Hash list.** `run_stage4` checks only `wp_rule_sha256` (unchanged). The `sha256` dict inside `frozen_inputs.json`
mirrors WP_RULE A.3 and is read by no code; it was left unchanged so that it keeps matching A.3. Every output records
the actual `code_sha256` and the full `frozen_inputs` dict (incl. `finder_config.tseed = 4`) plus `finder_cfg.tseed`,
so the meta is self-consistent. Admission (WP_RULE §5.4 item 11) of C1/C2 outputs therefore rests on A.3 + this
addendum (run_stage4.py 0d122cfc…, run_chain.py bdea0e27…).

**Re-timing (run_stage4.py constants; units now per-worker seconds under the 7-worker production load, G3-measured).**
`T1_S` 3.26 → 8.02 s, `T2_S` 20.1 → 50.6 s (G3 paired re-run at T_seed = 4; T_seed 6 under the same load 5.52 / 34.4 s),
`PU_S` 4.83 → 10.2 s (chain per PU event, B1), new `PU_S_RHO2` = 9.3 s (B2). `run_g1b.COST` follows (it uses
`RS.T1_S`/`RS.PU_S`). These constants only set `est_s` (job ordering, `status` ETA); they do not enter any output array.
G2b criterion: t₂ = 50.6 s ≤ t₂,max = 66 s (C1 → C2): still PASS (ESTIMATE, as in G3_REPORT §4).

**Sub-run campaigns (plan §11 row "7-12 s"; C2B user-approved 2026-10-14).** `SPLITS` in run_stage4.py:
`C1a` = C1 jobs of kinds a1/a2/a5/cp0/cppu (875), `C1b` = C1 kinds pu/sm/dens + the `val` placeholder (760 + 1),
`C2B` = C2 kind pu only (480; C2-C 'sm' and C2 'val' excluded). Job dicts, seeds and output paths are those of the
parent manifest (outputs and progress/STOP files in `prod/C1/` resp. `prod/C2/`); C1a ∪ C1b = C1 exactly (checked).

**Verification (production path really uses T_seed = 4): PASS.** `validation/tseed4_verify.py` (sha
`ca21fe4a9496ac721b71bc135828719e6a10a3d866e284d23a3a092e1975b569`) ran G3 job G3B1_00000 (unchanged G3 job dict, 25 events ×
4 roads = 100 trials) through `run_stage4.run_pu_job` with the applied files and no override, output redirected to
`data/acts_stage4/tseed4_verify/`. Result (`data/acts_stage4/tseed4_verify/tseed4_verify.json`):
- vs the stored T_seed = 4 re-run `data/acts_stage4/g3/rerun/tseed4/G3B1_00000.npz` (g3_rerun.py: frozen runner,
  `cfg.tseed = 4` set after `finder_configs`, i.e. the same Config): **85/85 arrays bit-identical** (only meta_json and the
  wall-clock timers excluded, as in g1b_regress);
- negative control vs the stored T_seed = 6 production file `prod/G3/G3B1/G3B1_00000.npz`: 57/85 arrays differ (all
  finder outputs), chain arrays identical;
- meta: `finder_cfg.tseed = 4`, `frozen_inputs.finder_config = {road 0.15, tseed 4}`, run_stage4 0d122cfc…,
  run_chain bdea0e27…, no event replaced. This also confirms the G1b hook + chain fix leave the PU path bit-identical.

**New files (not hashed in A.3).** `validation/tseed4_verify.py` (above); `validation/chain_c1.sh`
`8e25d33710edec71e4c56db85ffa20be669825d6e0f96d9de371f31f20007af1`.

**Update 2026-10-14 00:31 (orchestrator, C1_LAUNCH §4 option a).** `run_stage4.py` 0d122cfc… → `e371c2b2ef6f3792380b5d38ab3e9d763134f71ce7cbee1891550c2aa22dca46`:
in `cmd_run`, for campaign `C2B` only, the to-do list is sorted by `-est_s` (B2 and B1 interleaved under the 19 GB budget)
instead of `(order, -est_s)`. **Only the scheduling order changes**; no job dict, seed, id, output path or execution path.
Checked by dict compare against the manifests before the change: C1b 761/761 and C2B 480/480 job dicts identical;
C1b run order identical. C1a runs on 0d122cfc… (loaded at start); C1b and C2B load e371c2b2…. New helper
`validation/prodstop_fri.sh` (`9b85500f6bcc786a5c273c8aeb73a3c2ab1465a0ce44c3f214d25d16131ecf2a`, PID 83550): creates
run_stage4's existing graceful-stop file `prod/C2/STOP` (and `prod/C1/STOP` if C2B has not started) at Fri 2026-10-16
12:00 -05; completed jobs are kept.

## 6. PC-19: the SR-T window amendment (2026-10-14; user-approved; REVIEW_SRT_TMIN_R3 PASS)

**New files.** Both are part of A.3 by the admission note above. Neither is read by any production code.

| file | sha256 | note |
|---|---|---|
| `acts/stage4/WP_RULE_PC19.md` (read-only, chmod a-w) | `d30bcc2fd271de9fcc2111d6379bbe8cb897a81c36506b4332091f4fc04d5c8e` | PC-19 rule text; amends WP_RULE §1.4 / §4.1 / §6.2 / App. A for all SR-T quantities and takes precedence there |
| `acts/stage4/g3/srt_tmin_check.py` | `9d0c902ae128ba27c620f316dafb9fa4b86e327a8fbeccbb55ed6be9017dcd9e` | reference implementation (G3 check; `--combine` for σ_ln,PV / σ_ln,σt); includes the REVIEW R3 C-1 fix (σ_t 60 ps smearing applied to the in-time term) |

**Unchanged files.**
- `WP_RULE.md` (`1b2ea9bd…`, still checked by `run_stage4`) is not edited.
- `frozen_inputs.json` (`2adc8f9d…`) is not edited.
- Production code and outputs are not edited. C1a → C1b → C2B production is unaffected: the window, the PV time and
  the overlay are offline, and all inputs are stored.

**G3 evidence** (regenerated with the script above; files in `data/acts_stage4/g3/`).
- `srt_tmin_check_v2.json` (`980e1996…`): edges 6.07 / 24.025 ns; SR-T PU fraction 3.24e-5 (loose) and 3.42e-5 (R04).
- `srt_sigma_ln_pv.json` (`95b38131…`):
  - σ_ln,PV = 0.588 (loose) and 0.306 (R04);
  - σ_ln,σt = 0.032 (loose; it was 0.000 before the C-1 fix) and 0.016 (R04).
- v1_rerun still reproduces FIX R1: 6.12 / 24.275; 34 / 31 loose; 48 / 10 R04.
- The binding values come from C1 B1.

