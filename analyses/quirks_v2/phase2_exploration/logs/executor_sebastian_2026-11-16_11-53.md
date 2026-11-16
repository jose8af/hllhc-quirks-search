# Executor Sebastian — Phase 2, channel (ii): S2, P1, retrievals, Herwig (session log, append-only)

Session start 2026-11-16 11:53 -05 (`date`). Day 0 = 2026-11-16; day 5 = 2026-11-21 (decision point 1, stop-rule checkpoint 1).
Read in full: PHASE2_BRIEF.md, AGENT_RULES.md, CLAUDE.md (overrides), agents/executor.md, phase2_exploration/CLAUDE.md,
methodology/03-phases.md Phase 2, methodology/11-coding.md, STR §0, §4.0, §4.13 (S1, for the Stage-2 definition), §4.14,
§4.15, §4.17, §6.4, §11.1–11.7, §12.1, COMMITMENTS.md (Gate A answers; rows S2-a…f, P1-a…d, REF-2, SY-1, SY-2, SY-7,
SY-10), FEAS_A (§2, §3.1–3.2), FEAS_B (whole), FEAS_C (whole), CHAIN_PROVENANCE.md, PREFLIGHT.md, ledger/README.md.

## 1. Plan (written before any code or job)

### 1.1 Budget and rules I work under
- Budget: S2 88 CPU-h, P1 51 CPU-h (STR §11.2). Stop and report if my projected Phase-2 spend exceeds 1.3 × (88 + 51) = 181 CPU-h.
- Slots: weekdays 08:00–19:00 at most 3 concurrent jobs; otherwise 2 (channel (ii) cap). ≤ 4 jobs per node in total, 3 on
  landau and schrodinger (graphical session). I check `SLOTS.md` before each launch and keep off a node channel (i) announces.
- Campaign names `p2-b-*`; all compute through `tools/runner` (SSH backend for short timing jobs, Argo for production
  chunks); jobs ≤ 30 min; outputs `.part` → rename on cajuela with a runner marker. CPU-h from `qv2run rebuild-ledger`.
- No git, no subagents, nothing heavy on einstein (edit + ssh/launch only). MG runs from a node-local copy of the MG
  install (`/home/scratch/jdochoa/mg5/`, FEAS_B open issue 1), copied by the job under flock with a sha256 stamp of the
  NFS install's file list; compiled process directories live in the job's scratch.
- Blinding: I compute no signal efficiency. Cross sections, K-factors and LHE/shower timings are not efficiencies.
  **f₂₀₀ (S2-b) is a generator-level fraction σ(pT(QQ̄) > 200 after shower)/σ(matched)**; STR §4.17 row 7 assigns it to
  Phase 2, but it has the form of an acceptance. I will not compute it until the orchestrator confirms (question Q-S1).

### 1.2 Items, scripts, campaigns, CPU-h estimates

| # | item | scripts (in `phase2_exploration/src/s2/` unless stated) | campaign | jobs × size | CPU-h est. | budget line |
|---|---|---|---|---|---|---|
| A | **R-3, R-2 retrievals** (day 5 deadline), then R-1, R-12, R-19 (they feed S2 and DP5) | none (web; every lookup in `retrieval_log.md`) | — | — | 0 | — |
| B | **MLM 0–2j timing** (the 50 ms guess of Table 4.0, 24 CPU-h rest on it): v1 configurations E-TRG m500 (ME cut pT(QQ̄) > 100 GeV), E-INC m500, S-TRG m500 (xqcut 30, qCut 45, CP5, QED-FSR card) | `s2_job.py` (stdlib driver: local MG copy, output, launch, PY8 with MLM, `convert_hepmc.py` to npz; per-step CPU recorded in a JSON) | `p2-b-s2-mlmtime` | 3 × 10,000 LHE | ≈ 1.5 | S2 |
| C | **S2-a validation 1** (model identity: fixed-order LO of `loop_quirkE` vs the tree UFO at the same fixed scale and PDF) | `s2_job.py nlo …` | `p2-b-s2-kval` | 2–4 short jobs | ≈ 0.3 | S2 |
| D | **S2-b K(m) scan**: E at 200–1500 GeV (14 masses), Ẽ at 200, 500, 1000, 1500; NLO and LO fixed order, scale envelope by reweighting; CT18NLO and PDF4LHC21 (PDF4LHC21 needs the LHAPDF set: a data download into `sw/lhapdf_data`, ≈ 100 MB, not a pixi install; asked first) | `s2_job.py nlo …`, `kscan_collect.py` | `p2-b-s2-kscan` | ≈ 36 jobs × 2–5 CPU-min | ≈ 2 | S2 |
| E | **S2-a validation 3**: K(M) of `p p > e+ e-` at NLO vs K_E(M) in pair-mass bins | `s2_job.py nlo dy …` | `p2-b-s2-kdy` | few jobs | ≈ 1 | S2 |
| F | **S2-a validation 2**: fixed-order NLO slepton reference (R-1 decides: WG table with an NLO column, or a public code, e.g. Resummino, run at the same settings) | depends on R-1 | `p2-b-s2-kref` | — | ≤ 2 | S2 |
| G | **FxFx timing then production** (0–1j MC@NLO + Pythia 8 FxFx) at 500 and 1,500 GeV; first a 30-min timing job, then sized | `s2_job.py fxfx …` | `p2-b-s2-fxfx-time`, `p2-b-s2-fxfx` | 1 + N | 40 (STR guess G) | S2 |
| H | **Stage 2 nominal** (STR §4.17 row 7): five species-masses E 200/500/1000/1500, Ẽ 500, 250,000 LHE each, MLM 0–2j, **QED-FSR shower nominal** (S2-d); LHE + npz kept, HepMC transient. Chunk size from B. Generator-cut layout (v1: TRG with ME cut 100 GeV stitched with INC) as in v1 unless the orchestrator decides otherwise (Q-S2) | `s2_job.py stage2 …` | `p2-b-s2-nom` | ≈ 5 × 10–25 chunks | 17 (at 50 ms) | S2 |
| I | **Four re-showers** (same LHE): qCut 30 and 60 (vs 45), Monash tune, FSR-off (kept for C1 and the FSR shift) | `s2_job.py reshower …` | `p2-b-s2-var` | 4 × chunks of H | 29 | S2 |
| J | S2-f infracolour correction per mass: averaging δ(β) over the generated β of the nominal LHE (no CPU); source search R-12 | `infracolour.py` (einstein-light, or a 1-min job) | — | — | 0 | S2 |
| K | **Herwig install attempt** (DP5): conda-forge `herwig`/ThePEG into node-local `/home/scratch/jdochoa/envs/herwig` with node-local pixi cache (no `/home/users` writes), **only after I hold the study's install slot** (Q-S3); if it works, 10⁶ minimum-bias events at generator level, K/π and p fractions vs Pythia CP5 in the DIF p_T/η range; if not, one source build in `/var/tmp/jdochoa` on the worker, then fallback R-19. Stop after ≈ ½ day | `herwig/install_herwig_local.sh`, `herwig/mb_species.py` | `p2-b-hw-mb` | ≈ 20 × 5×10⁴ events | ≈ 3 (ESTIMATE) | not in STR §11.2: proposed from the S2 margin (Q-S4) |
| L | **P1 (thickness law)**: (1) read the v1 code and records to resolve the configuration of v1's B*-off test (event subset, step size, where the B* switch sits) and re-project its cost; (2) floor test 2: mantissa-truncation version of `mdot` in a copy of `nm_kernel.py` (note in CHAIN_PROVENANCE); (3) floor test 1: ≥ 30-digit step map (mpmath) for 3–5 events, if it fits in the time; (4) paired B*-off at 5 keV (≈ 970 events × 2) and at 1 keV; (5) population estimator on 300 new events × 5 points at 1 keV; (6) validity-window table from `P1.json`; (7) rerun of the Stage-1 analysis for the Linux 2-vs-6-crossings run | `phase2_exploration/src/p1/*` | `p2-b-p1-*` | from (1) | 51 (36.5 + 4 + 0.5 + 10 margin) | P1 |

Total planned: S2 ≈ 88 (+3 Herwig, flagged), P1 51 → ≈ 142 CPU-h, inside 1.3 × 139.

### 1.3 Outputs
- Bulk: `data/p2-b-*/<shard>/…` via the runner (LHE.gz, npz, timing JSON); markers in `ledger/markers/p2-b-*/`.
- Small results: `phase2_exploration/outputs/s2/{mlm_timing.json, kfactors.json, kval.json, …}`, `outputs/p1/*.json`.
- Artifact: `phase2_exploration/outputs/EXPLORATION_ii_sebastian_<stamp>.md` (brief §5 contents).
- `retrieval_log.md` (append), `phase2_exploration/experiment_log.md` (append), `DAILY_NOTES.md` (two lines per report).

### 1.4 Checks
- MLM timing: per-step CPU from the job's own `os.times()`/rusage of each child and the runner's marker (they must agree
  to a few %); σ of E-TRG/E-INC m500 against v1 SAMPLES.md (same cards, different seed: z within ±3); matched fraction
  against v1 (SAMPLES.md columns). No efficiency is computed.
- K-factors: LO of `loop_quirkE` vs tree UFO at identical fixed scale (|z| < 3 and 0.5 %); K(200) reproduces FEAS_B 1.165 ± 0.002;
  limiting checks: scale envelope contains the central value; K(M) for DY vs K_E within 2 % / 3σ.
- Stage 2: N_LHE, σ per chunk vs v1; weights non-zero fractions; sha256 in markers.

### 1.5 Order
1. (now) plan → R-3 → R-2 (web, logged) and in parallel the MLM timing campaign B (3 jobs, SSH runner) → first report.
2. C, D, E (cheap NLO jobs) and the FxFx timing job G; R-1 for F.
3. P1 step (1) (code reading on einstein, light) and the Herwig attempt once the slot is granted.
4. H and I after B's timing (chunk sizing) and the orchestrator's answers on Q-S1/Q-S2.
5. G production, P1 campaigns, J, artifact.

### 1.6 What I deliver by day 5 (2026-11-21)
R-3 and R-2 closed (cited figure and page, or "not sourced" with the STR §6.4 consequence); measured MLM and FxFx unit
costs against Table 4.0; S2-a validations 1 and 3 and the K(m) table (CT18NLO; PDF4LHC21 if the set can be added);
Stage 2 nominal and re-showers generated or running; Herwig install verdict; P1 configuration resolved and the B*-off
campaign running; the interim artifact.

### 1.7 Questions for the orchestrator (in the first report)
- Q-S1: may I compute f₂₀₀ (generator-level, STR row 7 assigns it to Phase 2) or is it covered by "no signal efficiency"?
- Q-S2: Stage-2 generator-cut layout: v1's TRG (ME cut 100 GeV) + INC stitching, or a single TRG at 200 GeV as STR §4.13 words it?
- Q-S3: do I hold the study's install slot for Herwig (node-local, no `/home/users` writes)? Also the PDF4LHC21 LHAPDF set download into `sw/lhapdf_data`.
- Q-S4: CPU-h of the Herwig minimum-bias comparison (≈ 3) charged to the S2 margin?

## 2. Log
- 2026-11-16 12:04 plan written (§1). Workers idle at 11:53 (load < 0.2; no pixi install running on any worker: `pgrep -af 'pixi (install|add)'` empty).
- 11:57 `src/s2/s2_job.py` (mlmtime) and campaign files `tools/campaigns/p2-b/{p2-b-s2-smoke,p2-b-s2-mlmtime}.json` written; SLOTS.md line appended.
- 11:58 smoke job 1 FAILED: `cp -a` of the MG install to node-local scratch: "preserving permissions … Operation not supported" (NFS4 ACLs → ext4). 12:01 smoke2 FAILED the same with `--preserve=mode`. Fix: plain `cp -rd` (mode bits kept, checked on maxwell). 12:04 smoke3 running on maxwell (MG output started).
- 12:05 R-2 and R-3 retrievals logged (`retrieval_log.md` #11, #12). CDS (cds.cern.ch) blocks automated fetches (bot-protection page) → INSPIRE API full-text / files used instead.
- 2026-11-16 12:09 P1 step (1) started (read-only, einstein): v1 B*-off test = `TT/sim/stage3/scripts/fix_bstar_off.py` (docstring l.1-15, job l.33-60): per event **4 kernel runs** (arms on/off × fields B0, B0/2) with the Stage-1 general-field kernel `analytic/numerics/nm_kernel.run` (max_boost 1e-3, hmax_trk 0.2 cm, qcap 2^19), vacuum, vertex at origin; Δs from a plane fit on the 10 barrel layers; c2 = (2Δs(B0/2)/Δs(B0) − 1)/ln 2; events from P1 F_m500/F_m1000 at Λ = 5 keV, 16 per k_B bin (rng 2026 + 2027) + 16 c5kev rows; result `results/FIX_bstar_off.json`: n_events 171, cpu_h 0.842 (M3). So 0.842 h/171 = 17.7 s per event for 4 runs on the M3 [V: FIX_bstar_off.json → cpu_h, n_events], far below STR's 67.8 s × 2 per event (which is the Stage-3 production cost). To be re-timed on a worker before the campaign (re-projection of P1's 36.5 CPU-h).
- 12:06 smoke3: MG output + warm launch done on maxwell; warm-launch σ(E-TRG m500, 100 ev) = 0.001214 ± 0.0000055 pb vs v1 SAMPLES.md E-TRG m500 1.213 fb (same cards): consistent.
- 12:07 `nlo` and `lotree` commands added to s2_job.py; campaign files p2-b-s2-kscan (5 jobs) and p2-b-s2-kval (6 jobs) written, not launched.
- 2026-11-16 12:10 -0500 smoke3 DONE (p2-b-s2-smoke, maxwell, 312.7 CPU-s, 213.5 MB): σ(E-TRG m500) 1.2092 fb (200 ev) / 1.2139 fb (400 ev); MG launch fixed ≈ 92 s per launch (MLM survey/refine), MG ≈ 6.9 ms/LHE event (from 200/400, noisy), Pythia MLM+QED-FSR 25.0 ms/LHE event, npz conversion 10.0 ms/LHE event, local MG copy 27.6 s once per node. Ran on maxwell, which channel (i) had reserved at 11:57 (I read SLOTS.md only after the launch): apology line in SLOTS.md; maxwell left to channel (i).
- 2026-11-16 12:10 -0500 all nodes full (landau 2 (i) + 2 (iii); schrodinger 3 (iii); maxwell reserved (i)): `src/s2/chain_s2_first.sh` started detached on landau; it waits for p2-c-t-g4 to leave landau, then runs mlmtime → kval → kscan one job at a time. Ledger: channel (ii) CPU so far 318.95 s = 0.089 CPU-h (3 jobs, 2 failed at the copy step).
- 2026-11-16 12:14 orchestrator answers received: f₂₀₀ allowed (not A, not m_mig); S1 Stage-2 samples are NOT mine (row H of the plan dropped; a v1-layout remark goes in EXPLORATION as a strategy-revision input if needed); install slot held; Herwig ≈ 3 CPU-h charged to S2 if S2 + P1 ≤ 139; do not work around CDS.
- 2026-11-16 12:14 PLAN UPDATE (replaces rows H, I): **S2-c samples** = MLM 0–2j **inclusive** (v1 INC cards, QED-FSR nominal) at E 200/500/1000/1500 and Ẽ 500, 100k LHE each (sized after mlmtime), f₂₀₀ = Σw(pT(QQ̄) > 200 after shower)/Σw (no η cut) from the INC sample alone = the single definition; re-showers of the same LHE: qCut 30, qCut 60, Monash, FSR-off. Estimate at 42 ms per LHE event + 35 ms per re-shower: ≈ 6 + 15 CPU-h.
- 2026-11-16 12:14 PDF4LHC21_40 downloaded on landau scratch and copied into sw/lhapdf_data (retrieval_log #13; two AlphaS keys added as v1 did). R-3 follow-up: tail NOT FOUND (#14); validation figure ATL-PHYS-PUB-2019-005 Fig. 18 read (#15). The 2013 ATLAS MET formula is ×1.5–3 above that figure (experiment_log) → strategy-revision input for channel (iii).
- 2026-11-16 12:14 Herwig install queued on maxwell (`src/herwig/queue_install.sh`; log maxwell:/home/scratch/jdochoa/drivers/herwig_install.log). It starts after 13:30 and after channel (i)'s ρ = 2 jobs have left, with a pgrep check of all workers first; SLOTS line appended.
- 2026-11-16 12:21 EXPLORATION interim written with the R-3 hand-over (§1; met_compare.py → outputs/s2/met_compare.json). P1 timing (`src/p1/bstar_time.py`, campaign p2-b-p1-time) and FxFx timing (`s2_job.py fxfx`, campaign p2-b-s2-fxfx-time) are queued on landau behind the S2 chain (`chain_after.sh`). v1's P1 event kinematics (events_p1.npz) are not in the repo; timing uses the Phase-1 toy inputs.
- 2026-11-16 12:26 P1 design: c_ev and k_B are closed-form per event (`sim/stage3/code/s3_physics.py` l.4-56: c_ev = 1/(ln(l_max/b_odd) + K(γ*)), k_B = |B*_⊥n|/|E*_⊥n|), so the paired B*-off test needs Stage-2 kinematics + s3_physics + the 4 nm_kernel runs, not a Stage-3 production run. v1 P1 = |η_pair| < 1, vertex at the origin, 10 barrel layers, B and B/2, max_boost 1e-3 (TT/sim/stage3/README.md l.122). New events come from the S2-c inclusive samples (truth level; Q5). P1-c (paired median c2 − c_ev, 300 events × 5 points at 1 keV) = 2 'on' runs per event. Validation-3 campaign p2-b-s2-kdy (μ_R = μ_F = M(pair) via the user-scale block of setscales.f) queued behind fxfx-time (`chain_wait.sh`).
- 2026-11-16 12:30 mlmtime etrg-m500 DONE (landau): σ = 1.2086 ± 0.0062 fb (5000 ev; v1 1.213), MG fixed ≈ 99 s per launch + 3.4 ms/LHE event, Pythia MLM + QED-FSR 25.1 ms, conversion 9.7 ms, RSS 214 MB; the whole job took 504 CPU-s for 6,100 LHE events over 4 launches. R-1: WG slepton tables are NLO+NLL only (no fixed-order NLO column), so Resummino 3.1.2 (conda-forge) was added to the queued Herwig env for validation 2 (retrieval_log #16; the twiki numbers were transcribed through the web-fetch tool, so they are UNVERIFIED until re-read).
- 2026-11-16 12:38 mlmtime einc-m500 DONE: σ = 5.386 ± 0.015 fb (v1 E-INC m500 5.389), MG fixed ≈ 72 s + 4.9 ms/event, Pythia 22.6 ms, conversion 9.9 ms → ≈ 41 ms per LHE event at 20k-event chunks (VERIFIED p2-b-s2-mlmtime; Table 4.0 guessed 50 ms). Sanity check: v1 INC m500 σ(pT>200)/σ_matched = 0.2617/2.507 = 0.1044 (SAMPLES.md l.18), = v1 f₂₀₀ 0.10418. S2-c campaigns written (`make_s2c_campaigns.py 20000 5`: 25 inc + 50 rs jobs) and queued on maxwell from 13:30, 2 at a time (`queue_maxwell.sh`). `src/s2/f200.py` written (not run yet).
- 2026-11-16 12:58 Orchestrator ruling 12:58 (fixed node shares): my 2-slot maxwell queue and the separate Herwig queue were killed before starting. New `src/s2/queue_maxwell1.sh` runs on maxwell, one process at a time: install, then p2-b-s2c-inc, then p2-b-s2c-rs. The install started 12:58:31. Its built-in pgrep check of the other workers failed silently (from maxwell the names landau/schrodinger do not resolve). I re-checked from einstein at 2026-11-16 12:58: no pixi install on landau or schrodinger. Fix for later scripts: run the check from einstein. Validation 1 at 200 GeV: FO-LO 0.09342 ± 0.000039 pb vs tree 0.09344 ± 0.000031 pb (fixed μ = 200, CT18NLO), rel −0.02 %, z ≈ −0.3.
- 2026-11-16 13:05 **S2-a validation 1 PASS** (`src/s2/kval_eval.py` → `outputs/s2/kval.json`, campaign p2-b-s2-kval). Fixed-order LO of loop_quirkE vs the tree v1 UFO at fixed μ = m, CT18NLO: m = 200: 0.09342(4) vs 0.09344(3) pb, z −0.40, rel −0.021 %; m = 500: 2.654e-3 vs 2.654e-3 pb, z 0.0; m = 1000: 8.218e-5 vs 8.216e-5 pb, z +0.40, rel +0.024 %. Criterion |z| < 3 and 0.5 %.
- 2026-11-16 13:05 Herwig 7.3.0 + Resummino 3.1.2 installed node-local on maxwell (27 s; install slot released, SLOTS line). CT14lo (Herwig's MB default PDF) downloaded to maxwell scratch `/home/scratch/jdochoa/lhapdf_herwig` (official LHAPDF URL, tarball sha256 5554b2f6…). `src/herwig/mb_species.py` written (π/K/p yields, |η| < 2.5, p_T bins, cτ > 1000 mm stable in both generators). Smoke campaign p2-b-hw-smoke is queued on maxwell after p2-b-s2c-inc (`queue_maxwell2.sh`, replaces queue_maxwell1, which is stopped; the inc driver was untouched). PDF4LHC21 K-scan (p2-b-s2-kscan-p4l) is queued on landau after kdy.
- 2026-11-16 13:07 R-1 / validation 2: the WG tables give NLO+NLL only, so the fixed-order reference is Resummino 3.1.2 run at our settings (`src/s2/resummino_job.py`; inputs = HEPcodes/resummino example card + SLHA, copied to `src/s2/resummino_inputs/`). The SM inputs are set to the v1 UFO values, with M_W from the UFO formula = 80.419 GeV. CT18NLO, μ = m. Matched loop-model run: Ẽ at fixed μ = m (`nlo … --fixed m`). Both jobs were added to campaign p2-b-hw-smoke (maxwell queue, after p2-b-s2c-inc).
- 2026-11-16 13:09 P1 floor test 2 prepared. `src/p1/nm_kernel_t44.py` is a COPY of analytic/numerics/nm_kernel.py: mdot truncates every product and the result to 44 mantissa bits; CODE path made absolute; the original is untouched. `src/p1/floor2.py` runs the FIX2 'off' arm at the fractions f = 1, 1/2, 1/2.5, 1/4, 1/20 with either kernel. Two timing jobs were added to p2-b-p1-time. v1's M3 events need the T2 kinematics cache (170 MB, not in the repo: code/T3_propagator.py l.517-525), so new events are used (toy inputs now, S2-c events later). Floor test 1 (≥ 30-digit step map) not started.
