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
