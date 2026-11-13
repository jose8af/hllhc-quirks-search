# FEAS_B — Generators and Geant4 on the Linux cluster (executor Basil, Phase 1 feasibility)

Status: **all five tasks done** (2026-11-13, ≈ 17:05). Geant4 is installed on schrodinger only (landau/maxwell: script
ready, not run). The machine-readable copy is `benchmarks_generators.json` (same directory); raw timings in `bench_raw/`. Session log:
`phase1_strategy/logs/executor_basil_2026-11-13_14-50.md`; decisions and failed attempts: `phase1_strategy/experiment_log.md`
(`[Basil]` entries). Tags: **VERIFIED** (measured here; command/log cited), **ESTIMATE**, **UNVERIFIED** (transcribed).

## Summary
1. **MG5_aMC 2.9.22 + Pythia 8.313 + MG5aMC_PY8_interface V1.3 + LHAPDF 6.5.5 work on the Ubuntu 24.04 workers**
   (installed under `/home/users/jdochoa/sw`, 580 MB, VERIFIED `du`). MG runs under a pixi Python 3.9 env (MG itself
   calls Python 3.12 "experimental … not for production"). The v1 PDF sets are installed with the **v1 patched `.info`
   files** (the official CT18NLO/NNPDF23 `.info` lack the `AlphaS_*` keys LHAPDF 6.5.5 + MG's Fortran glue need).
2. **v1 is reproduced:** the v1 UFO imports unchanged; the MG run card for E-LOPS equals the v1 effective card key by key
   (35 keys; only `nevents`/`iseed` differ). LO σ(pp → E⁺E⁻, m = 200 GeV, 14 TeV) = **92.33 ± 0.07 fb** vs v1
   **92.26 ± 0.04 fb**: **z = 0.91** (VERIFIED). Test samples (1000 showered events each, E 200 GeV and Z(νν)+jet) are on
   cajuela with MANIFEST and markers.
3. **NLO K-factors can be computed, cheaply.** A loop-capable UFO (`loop_quirkE` = MG's `loop_sm` + the v1 quirk
   states; the quirks are colour singlets so no new counterterm is needed for NLO QCD) runs `p p > xe+ xe- [QCD]` at
   fixed order on these nodes: **K = σ_NLO/σ_LO = 1.165 ± 0.002 at m_E = 200 GeV** (CT18NLO, μ = H_T/2; scale envelope
   NLO +1.6/−1.1 %), for **≈ 2 CPU-min per mass point** after a one-off 3 CPU-min process generation (VERIFIED, single
   runs). This contradicts the digest statement that "no loop-capable UFO exists" (`D5_stages_amara.md`): it did not exist
   in v1, it is buildable in minutes. NLO+NNLL (Resummino-like) and the FxFx point remain separate items (see Task 4).
4. **Geant4 11.4.3** (conda-forge, noqt, 12 data sets 2.2 GB) installs **node-locally** in ≈ 3 min with no NFS writes
   (`tools/install/install_g4_local.sh`); a minimal pion-gun application on the v1 barrel geometry in 3.8 T builds and
   runs (VERIFIED on schrodinger): **0.13 ms per pion gun** with secondaries handed over (0.27 ms with full tracking),
   5.3 % of guns give a vertex → **≈ 0.7 CPU-h per 10⁶ single-interaction events** (ESTIMATE, unbiased guns).
6. Headline costs on schrodinger (VERIFIED means of 3): MG LO 2.1 ms/event + 6.6 s per launch; **Pythia shower
   21 ms/event**; QED-FSR re-shower the same 21 ms/event (≈ 14 CPU-h for all v1 samples); Pythia minimum bias
   2.0–2.5 ms per interaction + 11 s init; full LO signal chain ≈ 34 ms per LHE event (M3 → schrodinger ≈ 1.3, ESTIMATE).
5. Seven Linux/NFS pitfalls were found and fixed (list in "Validation → pitfalls"); three of them would silently break
   or slow production (conda `libgfortran` shadowing, missing `-DGZIP`, unpatched HepMC2 → 20 HepMC files per job).

## Method
- Everything heavy ran on **schrodinger** (≤ 3 jobs, `nice -n 10`), work dirs on node-local `/home/scratch/jdochoa/…`,
  builds in `/var/tmp/jdochoa/…`; NFS writes only as tarball unpacks under `nice -n 19 ionice -c3` (rules of
  AGENT_RULES "einstein and NFS home rules"). Nothing heavy on einstein after the 15:12 incident.
- Generation flow = v1 (`TT/sim/scripts/produce.py`): MG with shower OFF; Pythia run by us through the
  MG5aMC_PY8_interface with the v1 card (CP5 first, then `pythia8_quirk_common.dat`; optional `pythia8_quirk_qedfsr.dat`);
  driver `src/generators/feas_mg.py`.
- Benchmarks: `src/generators/bench.sh` (3 sequential single jobs + 3 concurrent jobs, `/usr/bin/time -v`; CPU = user +
  sys including waited children), driven by `bench_all.sh`; merged by `collect_bench.py`.

## Results

### Task 1 — installation (VERIFIED unless stated)
| component | version / source | where | how | NFS disk |
|---|---|---|---|---|
| MG5_aMC | 2.9.22, launchpad LTS (`…/mg5amcnlo/lts/2.9.x/+download/`), sha256 c15fac43…3092, md5 = launchpad `+md5` | `sw/mg5/MG5_aMC_v2_9_22` | release tarball; only `input/.autoupdate` changed (last_check = 2100) | 268 MB incl. HEPTools |
| Python for MG | 3.9 + six + numpy 1.26 + LHAPDF 6.5.5 (conda-forge) | `sw/envs/mg` (pixi) | `pixi install` | 244 MB |
| Pythia | 8.313 (pythia.org/releases), gzip on, **no LHAPDF** (v1 never used it inside Pythia: CP5 = internal `PDF:pSet = 20`) | `…/HEPTools/pythia8` | built in `/var/tmp`, final prefix baked in, one tarball (925 files) | in MG line |
| MG5aMC_PY8_interface | V1.3 (madgraph.mi.infn.it), HepMC 2.06.09 static with MG's named-weight patch, `-DHEPMC2HACK -DGZIP` | `…/HEPTools/MG5aMC_PY8_interface` | as above | in MG line |
| PDF sets | CT18NLO (59 members, lhaid 14400) + NNPDF23_lo_as_0130_qed member 0 (lhapdfsets.web.cern.ch/current) | `sw/lhapdf_data` | official members + v1 tracked `.info`, `lhapdf.conf`, `pdfsets.index` | 69 MB |
| Geant4 | 11.4.3 conda-forge `noqt` + 12 data sets; extra header packages expat, zlib, freetype | `/home/scratch/jdochoa/envs/g4` **per worker** (schrodinger only so far) | `tools/install/install_g4_local.sh` (`pixi install --frozen`, node-local cache) | 0 (local: env 3.3 GB, cache 3.3 GB) |

Total software on the NFS home: **580 MB** of the 150 GB budget (VERIFIED `du -sh /home/users/jdochoa/sw`).

**Why the PDF `.info` files are patched (kept).** v1 added `AlphaS_FlavorScheme`, `AlphaS_NumFlavors`,
`AlphaS_Lambda4`, `AlphaS_Lambda5` to CT18NLO.info and `AlphaS_FlavorScheme`, `AlphaS_NumFlavors` to
NNPDF23_lo_as_0130_qed.info because LHAPDF 6.5.5 + MG's Fortran glue need them (TT/sim/plan.md l.56; REPRODUCE §2.3);
changing the Λ placeholders left σ unchanged in v1 (2.454 fb both times). I diffed the official files of
2026-11-13 against the tracked ones: the differences are exactly these keys (VERIFIED). The tracked files are used verbatim.

**Component choice (HEPTools installer vs conda-forge).** MG and the interface must come from MG (no conda package);
Pythia 8.313 could come from conda-forge, but the interface links Pythia's `Makefile.inc` flags and v1 used the
HEPTools layout, so Pythia was built from the pinned tarball with the HEPToolsInstaller V168 recipe, but outside the
installer (the installer builds inside the install tree, i.e. on NFS). LHAPDF comes from conda-forge in the MG env (as
v1). Geant4 from conda-forge (no build needed). Scripts: `tools/install/install_generators.sh` (sources + sha256, MG,
env, PDFs, HEPTools), `tools/install/build_heptools.sh` (local build → one tarball), `tools/install/install_g4_local.sh`.

### Task 2 — v1 model and cards, test samples (VERIFIED)
- Model: copy of v1 `TT/sim/models/quirkE` imported as `quirkE-no_b_mass` with `define p = p b b~`, `define j = j b b~`
  (as `produce.py`). Process `p p > xe+ xe-` (5 processes, 10 diagrams). Run card = v1 `cards/run_card_prod_E-LOPS.dat`
  (key-by-key comparison: identical except `nevents`, `iseed`). Pythia log: `PDF:pSet = 20`, `pT0Ref = 1.41`,
  `ColourReconnection:range = 5.18` (CP5 applied, not reset by `Tune:pp`), quirk mass 200 GeV from the SLHA block,
  1000 events, 209 named weights in one HepMC file.
- SM process: v1 had no MG SM sample (its SM hard scatters were Pythia 2→2, `TT/acts/stage4/code/s4pu.py` SM_SAMPLES).
  I used the leading v1 MET background, **Z(νν)+jet**, as `p p > vl vl~ j` with `misset = 200 GeV` (45 processes).

| sample | v2 σ (LO) | v2 N / seed | v1 reference | z or ratio |
|---|---|---|---|---|
| E, m = 200 GeV, `p p > xe+ xe-` | **92.33 ± 0.07 fb** | 20000 / 21902101 | 92.26 ± 0.04 fb (`TT/sim/logs/launch_E-LOPS_m200_c0.log` l.118; SAMPLES.md E-LOPS m200) | **z = +0.91** |
| same, the 1000-event test sample | 92.65 ± 0.27 fb | 1000 / 21902001 (v1's seed) | as above | z = +1.45 |
| Z(νν)+j, MET > 200 GeV | 12.21 ± 0.03 pb | 20000 / 7101 | 14.6 pb, Pythia 2→2 p̂T > 150 GeV + truth MET > 200 GeV (`TT/acts/stage4/plan.md` l.1060) | ratio 0.84 — different generator, scale and PDF: **ESTIMATE, not a validation** |

z = (σ_v2 − σ_v1)/√(δ_v2² + δ_v1²), MC integration errors only. Check: the probe value of VALIDATION §1.1
(92.52 ± 0.20 fb, μ = √ŝ, different seed) is +1.1σ from v1's E-LOPS and −0.9σ from v2: all three agree.

Test samples on cajuela (final names, `.part` → rename, sha256 checked after the copy; markers
`ledger/markers/feasibility_generators/feasibility__generators__<sample>__<file>.marker`):

| directory `data/feasibility/generators/…` | file | bytes | sha256 (prefix) | content |
|---|---|---|---|---|
| `E_LOPS_m200/` | `unweighted_events.lhe.gz` | 717 599 | 9b1de853 | 1000 LHE events, 104 systematics weights |
| | `events.hepmc.gz` | 67 798 442 | e345ea47 | Pythia 8.313 CP5 shower, HepMC2 (IO_GenEvent), 1000 events, ≈ 1184 particles/event |
| | `aux.tar.gz` | 13 429 | 560584eb | run/param/proc cards, banner, PY8Card, PY8 log, MG logs |
| `ZNN_J/` | `unweighted_events.lhe.gz` | 829 928 | ce810aba | 1000 LHE events |
| | `events.hepmc.gz` | 79 148 845 | d0569808 | shower as above |
| | `aux.tar.gz` | 14 983 | a7732de8 | as above |

Each directory has `MANIFEST.txt` (sha256, bytes, name). Seeds: MG iseed 21902001 / 7001; Pythia 219020011 / 70011
(v1 rule (iseed × 10 + j) mod 9×10⁸ + 1). The samples have no vertex smearing (v1: vertex at the origin).

### Task 3 — benchmarks on schrodinger (VERIFIED, `bench_raw/`, `benchmarks_generators.json`)
CPU = user + sys (s) including waited children, mean [min, max] over N = 3; "single" = 3 sequential jobs, "3 conc" =
3 jobs at once on the 4-core node (nothing else of mine running). Max RSS is the largest over the 3 runs.

| benchmark (1 process per job, nb_core = 1) | single: CPU s | single: wall s | 3 conc: CPU s | max RSS MB |
|---|---|---|---|---|
| MG output (import model + generate + output), E `p p > xe+ xe-` | 2.56 [2.43, 2.78] | 2.99 | 2.56 [2.55, 2.57] | 54 |
| MG output, Z(νν)+j (45 subprocesses) | 3.81 [3.78, 3.83] | 3.95 | 4.00 [3.99, 4.02] | 56 |
| MG output + **first** launch (compilation + survey/refine + systematics), 1000 ev, E | 16.84 [16.77, 16.91] | 17.36 | 18.02 [17.99, 18.05] | 213 |
| same, Z(νν)+j | 24.74 [24.65, 24.80] | 25.09 | 26.52 [26.42, 26.57] | 213 |
| MG launch on a compiled dir, **1000 ev**, E (timed step) | 8.71 [8.49, 9.07] | 8.81 | 9.37 [9.20, 9.69] | 213 |
| same, **10 000 ev**, E | 27.70 [27.68, 27.73] | 27.85 | 29.31 [29.23, 29.45] | 213 |
| same, 1000 ev, Z(νν)+j | 14.86 [14.39, 15.33] | 14.99 | 15.94 [15.41, 16.41] | 213 |
| Pythia 8.313 shower (PY8 interface, v1 card), 1000 ev, E m = 200 | 21.18 [20.51, 21.63] | 21.38 | 21.88 [21.23, 22.28] | 29 |
| same, Z(νν)+j | 23.41 [22.39, 23.95] | 23.42 | 24.25 [23.25, 24.76] | 29 |
| same, E with the **QED-FSR** card (`pythia8_quirk_qedfsr.dat`) | 21.13 [20.70, 21.63] | 21.15 | 21.93 [21.52, 22.45] | 29 |
| Pythia minimum bias, 1000 interactions, v1 `PY_MB` + CP5 (incl. 11.0 s MPI init) | 13.03 [12.87, 13.18] | 13.06 | 13.37 [13.20, 13.53] | 25 |
| Geant4 FTFP_BERT π± gun, 20 000 ev, full tracking | 5.43 [5.38, 5.52] | 5.43 | 5.56 [5.51, 5.60] | 71 |
| same, primary only (products recorded, then killed) | 2.86 [2.84, 2.89] | 2.87 | 2.93 [2.91, 2.95] | 71 |

Derived (ESTIMATE, arithmetic on the means above):
- **MG**: one-off per process class ≈ 2.6 (output) + 5.6 (compilation) CPU-s; per launch ≈ 6.6 s fixed (survey, refine,
  `systematics` with 104 weights) + **2.1 ms per LHE event** (E LO). Z(νν)+j ≈ 15 s per 1000.
- **Pythia shower: 21 ms/event** (E 200 GeV, ≈ 1184 particles/event), 23 ms (Z+j). It dominates Stage 2.
- **QED-FSR re-shower** costs the same as the nominal shower (21.1 vs 21.2 ms/event): re-showering the 2.41 M v1 LHE
  events ≈ **14 CPU-h** on schrodinger (v1 DEFERRED estimate ≈ 15 CPU-h on the M3, UNVERIFIED).
- **Signal LO chunk of 50k** (MG + shower + v1 npz conversion at 10.9 ms/event): **≈ 34 ms per LHE event**; v1 quoted
  ≈ 27 ms per LHE event on the M3 for the same chain (DEFERRED.md l.5, UNVERIFIED) → M3 → schrodinger factor ≈ 1.26 for
  Stage 2 (ESTIMATE; a second estimate from v1's 122 s wall for 6 parallel showers of 50k events, `TT/sim/logs/produce.log`
  l.190, gives ≈ 1.45). MLM 0–2j samples (v1 INC/TRG) were not benchmarked; they add the matching veto (v1: ≈ 40–60 %
  of LHE events kept) and more subprocesses.
- **Pythia minimum bias: 2.0–2.5 ms per interaction** after an 11 s MPI initialisation per job (v1's `reuseInit = 2`
  file removes it); a PU-200 crossing ≈ 0.46 CPU-s of Pythia (Fatras not included). 96–105 particles per interaction
  enter Fatras (charged + γ, pT > 50 MeV, |η| < 4).
- **3 concurrent vs single**: +3–8 % CPU per job on 4 cores (MG +7 %, Pythia +3 %, Geant4 +2 %): running 3 jobs per
  worker is efficient; RSS ≤ 0.22 GB for all generator steps (MG NLO output: 1.0 GB).

**Output size per event** (VERIFIED, test samples): LHE.gz 0.72 kB (E), 0.83 kB (Z+j); HepMC2 text 193 kB (E;
gzip -6: 68 kB; Z+j gz 79 kB); v1 npz format 1.05 kB (209 weight columns; `convert_hepmc.py` run once). v1 kept LHE
and npz, deleted HepMC: for S1 (×10 signal rows, ≈ 24 M LHE events, ESTIMATE) that is ≈ 17 GB LHE.gz + 25 GB npz; HepMC
must stay transient (≈ 4.6 TB uncompressed).

### Task 4 — NLO K-factors (item S2, DEFERRED D-1)
**Is the model available at NLO?** Not in v1: the v1 UFO has no `CT_vertices`/`CT_couplings` (VERIFIED grep). But E and
Ẽ are colour singlets coupling only to γ/Z, so at NLO QCD the only loops are on the q q̄ γ*/Z* vertex, whose UV/R2
counterterms are already in MG's `loop_sm`. `src/generators/make_loop_quirkE.py` copies `loop_sm` and appends the v1
quirk particles, parameters, couplings and vertices verbatim (photon renamed `a` → `A`). This is the "hand-written
`loop_sm` extension" route of DEFERRED D-1, done in minutes; no FeynRules/NLOCT needed for NLO **QCD**.
(Not covered: NLO EW, which would need EW counterterms for the quirk — it is not part of the K-factor item.)

**Does aMC@NLO 2.9.22 run here?** Yes (VERIFIED): `output` with MadLoop (CutTools + IREGI, compiled once into
`vendor/`), then fixed-order LO and NLO at m_E = 200 GeV:

| quantity (E, m = 200 GeV, 14 TeV, CT18NLO, μ_R = μ_F = H_T/2, Gμ scheme, N_IC = 1) | value | CPU |
|---|---|---|
| σ_LO (fixed order, same model) | 92.87 ± 0.14 fb, scale envelope +0.0/−0.5 % | 92 s (incl. compilation) |
| σ_NLO QCD | 108.2 ± 0.14 fb, scale envelope +1.6/−1.1 % | 36 s |
| **K = σ_NLO/σ_LO** | **1.165 ± 0.002** | — |
| process generation (one-off per spin) | — | 169 CPU-s, 299 s wall, 1.0 GB RSS |

Consistency: the FO-LO of the loop model (92.87, μ = H_T/2) and the tree model (92.33, MG default scale) differ by
0.6 %, inside the LO μ_F band of VALIDATION §1.4 (+0.5/−0.8 %): consistent but not a same-scale identity test
(open item). The v1 normalisation used K_WG(200 GeV) = 1.110 transcribed from NLO+NNLL slepton tables and applied to an
LO with α = 1/127.9 (VALIDATION §1.2); that is a different definition (LO-PDF and EW-scheme conventions), so 1.165 and
1.110 are **not** directly comparable (ESTIMATE). What v2 can now do (cost VERIFIED per point, totals ESTIMATE):
- **NLO QCD K(m) for every mass point, E and Ẽ** (the Ẽ uses the same model; `p p > sxe+ sxe- [QCD]`): 15 E + 3 Ẽ masses
  × ≈ 2 CPU-min ≈ **0.6 CPU-h**, plus 2 × 3 CPU-min process generation; scale and PDF bands by reweighting.
- **Threshold resummation (NLO+NNLL)** — not in MG. Options: (a) Resummino for the right-handed selectron (Ẽ exactly;
  for E only with a fermion extension that Resummino does not ship: UNVERIFIED), ≈ CPU-minutes per point (ESTIMATE);
  (b) keep the WG NLO+NNLL tables for the resummation part only, i.e. σ = σ_NLO(MG, computed) × (NNLL/NLO)_tables,
  which turns the transcribed number into a ≈ few-% correction (ESTIMATE); (c) published electroweak pair-production
  tables (LHC SUSY WG) as now. Recommended: compute NLO QCD here for E and Ẽ and take only the NNLL/NLO ratio from
  tables, with its own systematic.
- **FxFx 0–1j at 500 GeV, ~200k events** (D-1): needs `p p > xe+ xe- [QCD]` + `p p > xe+ xe- j [QCD]` MC@NLO event
  generation (Pythia 8 with FxFx). StdHEP failed to compile in `vendor/` (needed only for MC@NLO + Herwig/old flows,
  not for Pythia 8 via HepMC: to be checked). Cost: D-1 estimated 10–20 CPU-h on the M3 (UNVERIFIED); here ESTIMATE
  from the FO timing (NLO ≈ 1/3 of the LO+compile cost at this precision, MC@NLO event generation typically
  ~10× LO): **≈ 5–20 CPU-h**, to be measured in Phase 2.

**QED-FSR re-shower** (v1 opt-in card `pythia8_quirk_qedfsr.dat`): supported by `feas_mg.py shower … qedfsr`; timed
in Task 3 (`py8_qed_E`).

### Task 5 — Geant4 route (item B1) (VERIFIED on schrodinger)
- conda-forge route works: `install_g4_local.sh` → Geant4 11.4.3, `conda-meta` check 0 missing of 62 802 files, stamp
  `/home/scratch/jdochoa/envs/g4/INSTALLED`. A source build was not needed.
- Application `src/generators/g4sv/g4sv.cc` (C++, CMake): world of G4_Galactic, 12 barrel cylinders from the v1
  geometry as Si tubes of thickness x/X0 × X0(Si) (`geom_barrel.txt` from `make_geom.py`), uniform B_z = 3.8 T,
  FTFP_BERT, π± gun (pT log-uniform 1–10 GeV, |η| < 1, from the origin), records every inelastic interaction and decay of
  the primary with its products to CSV. Tracks are killed after 25 ns or 5 m (loopers; see pitfalls).
- Benchmark (20 000 guns per job, table above): **0.134 ms per gun** (primary-only, the hand-over mode) and
  0.265 ms (full tracking of all secondaries), **RSS 71 MB**, initialisation 0.14 s. The primary makes a recorded vertex in
  **5.3 %** of the guns (4.2 % inelastic, 1.1 % decays; 1035/1046/1076 vertices in the three 20k runs).
- **CPU per 10⁶ single-interaction events (vertices), unbiased: ≈ 0.7 CPU-h (primary mode) / 1.4 CPU-h (full)**
  (ESTIMATE = 10⁶/0.053 guns × per-gun CPU). Geant4 is therefore cheap compared with the plan's 1–5k CPU-h for B1: the
  cost of B1 sits in the Fatras propagation, the pile-up overlay and the finder, not in Geant4. Not included: the
  realistic primary spectrum (PU-like, |η| < 4, softer), the discs, and the hand-over I/O.
- The sanity of the interaction rate (≈ 4 % per pion through ≈ 0.19 X0 of Si-equivalent at |η| < 1) is not yet a
  validation: B1's criterion compares Geant4 rates with the v1 generator rates (Phase 3).

## Geant4 build and integration plan (item B1)
- **Version and route.** Geant4 11.4.3 from conda-forge (`noqt` build), pinned by `tools/install/g4/pixi.lock`
  (sha256 edbcef24…7291), installed **per worker on local disk** at `/home/scratch/jdochoa/envs/g4` (user decision;
  same path in pods through the scratch hostPath). Install ≈ 3 min, 0 NFS writes. A source build is not needed.
  **Pre-flight for every Geant4 job:** `grep -q "lock_sha256=$(sha256sum $REPO/tools/install/g4/pixi.lock | cut -d' ' -f1)" /home/scratch/jdochoa/envs/g4/INSTALLED`
  (fail the job, do not install inside a job). landau and maxwell: run `install_g4_local.sh` there when the
  orchestrator allows (not done by me).
- **Physics list.** FTFP_BERT (Geant4 reference list for HEP; the v1 documents name no Geant4 list because v1 had no
  Geant4). Systematic: QGSP_BERT and FTFP_BERT_ATL (different string models / Bertini transition) on the same geometry,
  for the nuclear-interaction multiplicity and the stiff-prong tail.
- **Data sets** (VERIFIED sizes, conda-forge `geant4-data-*`): G4NDL 4.7.1 1.1 GB, G4EMLOW 8.8 726 MB, RealSurface 2.2
  128 MB, CHANNELING 2.0 68 MB, PhotonEvaporation 6.1.2 49 MB, PARTICLEXS 4.2 49 MB, PII 1.3 25 MB, RadioactiveDecay
  6.1.2 15 MB, ENSDFSTATE 3.0, ABLA 3.3, INCL 1.3, SAIDDATA 2.0 (< 2 MB each): **2.2 GB** total. FTFP_BERT needs
  G4PARTICLEXS, G4ENSDFSTATE, PhotonEvaporation, G4EMLOW, (G4NDL only for _HP lists).
- **Geometry identical to ACTS.** One source of truth, the v1 public geometry `TT/acts/geometry/cms_phase2_public.json`
  (`simplified` cylinders/discs + `material.T3_slabs_used`), which ACTS reads through `sim/stage3/code/surfaces_s3.json`.
  `src/generators/g4sv/make_geom.py` writes the Geant4 description from the same JSON (now: barrel cylinders + beam pipe
  + IT service cylinder as material-equivalent Si tubes, thickness = x/X0 × X0(Si)). For production: (i) add the discs
  (TFPX/TEPX/TEDD) the same way; (ii) export GDML with G4GDMLParser for the record and hash it with the JSON;
  (iii) **closure test**: geantino/material scan in Geant4 vs the ACTS material map along η, |Δ(x/X0)| per layer ≤ 1 %
  (criterion to fix in STRATEGY), and the same radii/z extents to < 1 µm.
- **Material model risk.** v1 slabs are specified in x/X0; nuclear interactions scale with λ_I, and a Si slab has
  λ_I/X0 ≈ 5 while real modules (C fibre, Cu, Al, coolant) have a different ratio. The NI rate per layer must therefore
  carry a material-composition systematic (e.g. Si vs a C/Si/Cu mixture at equal x/X0; size to be measured) on top of
  the B6 ×0.5/×2 material variation.
- **Hand-over to Fatras.** Geant4 tracks the primary (π±, K±, p, …) through the material in the 3.8 T field and
  records each **inelastic interaction or decay of the primary**: vertex (x, y, z, t), process, parent PDG/momentum and
  every product (PDG, p, E) — the CSV of `g4sv` now; in production one compressed `.npz`/parquet per job with the v1
  particle-array columns of `s4pu.py` (`vp, vsec, pdg, q, m, x, y, z, t, px, py, pz`, `vsec ≥ 1` per secondary vertex),
  so v1's `ParticleSource` injects the products into Fatras unchanged. The primary's own hits up to the vertex:
  either Fatras propagates the primary with its hadronic interaction switched off and is stopped at the recorded vertex
  (needs a Fatras-side stop: risk), or Geant4 records the primary's crossings of the sensitive surfaces and they are
  converted to ACTS SimHits by layer name (geometry identifiers must map 1:1: risk). Decide in Phase 3 with a 100-event
  comparison of the two.
- **Biased generation** of the stiff tail (B1 item 3): sample primaries in the stiff configurations and force/weight
  the interaction (G4 `G4GenericBiasingPhysics` cross-section biasing ×k in the tracker volumes, weight 1/k), so that
  10⁶ *interacting* events do not need 10⁷–10⁸ guns.
- **Risks.** (1) composition systematic above; (2) the primary-hit hand-over; (3) Geant4 and Fatras multiple
  scattering of the products differ only after hand-over (products are Fatras-only, fine); (4) conda-forge env is
  3.3 GB per worker plus 3.3 GB cache (local disks have ≥ 340 GB); (5) CMake must be told to ignore `/usr`
  (`-DCMAKE_IGNORE_PREFIX_PATH=/usr`), else it finds old system expat/zlib headers.
- **CPU per 10⁶ single-interaction events:** from the benchmark below.

## Validation
- **Cross section:** z = 0.91 vs v1 (E 200 GeV LO), see Task 2.
- **Run-card identity** with v1 (35 keys) and **CP5 really applied** (Pythia "changed settings" table), see Task 2.
- **Pitfalls found and fixed** (all in `experiment_log.md`):
  1. MG 2.9.22 download URL: series `lts/2.9.x`, not `2.0/2.9.x` (the latter is an HTML 404 page).
  2. MG under Python 3.12: starts but is "experimental, not for production" → pixi Python 3.9.
  3. `auto_update = 0` in `input/mg5_configuration.txt` crashes MG's exit hook (`abs(str)`) → reverted; `input/.autoupdate`
     with `last_check` in 2100 instead (no prompt, no rewrite of the file by every job).
  4. **conda `libgfortran` 16 on `LD_LIBRARY_PATH`** shadows the system gfortran 13 runtime that MG's Fortran is compiled
     with; its runtime rejects the `$` edit descriptor (`symmetry.f` l.233 `(I1$)`: "Missing comma between descriptors")
     and MG fails in `get_helicity` with `could not convert string to float: '#7'` → never put the conda lib dir on
     `LD_LIBRARY_PATH` (MG finds LHAPDF itself).
  5. **PY8 interface without `-DGZIP`**: "Les Houches initialization failed" on `.lhe.gz`, then an **endless loop at
     100 % CPU** → compile with Pythia's `CXX_COMMON`.
  6. **HepMC2 without MG's named-weight patch**: one HepMC file per weight (20 × 190 MB per 1000 events) → patch +
     `-DHEPMC2HACK`; now one file with 209 named weights.
  7. MG writes into its own install at run time: `models/sm` pickles, repeated `mg5_path` blocks in
     `input/mg5_configuration.txt`, and at the first NLO output it **downloads and builds OneLOop/ninja inside the
     install** (stopped, removed) and compiles CutTools/IREGI into `vendor/` (179 files, one-off, kept). → For
     production the install should be read-only to jobs (see Open issues).

## Open issues
1. **MG writes into the shared install** (pitfall 7): concurrent jobs would append to `input/mg5_configuration.txt`
   on NFS. Proposal for Phase 2: jobs run MG from a per-node local copy (`/home/scratch/jdochoa/mg5/`, 268 MB, copied
   once per node with a hash check) or make `sw/mg5` read-only after a warm-up that creates all pickles. Needs a
   decision by the orchestrator/runner (Boris).
2. FO-LO of `loop_quirkE` vs the tree UFO at an identical fixed scale (model-identity test; minutes).
3. Ẽ at NLO (`sxe`), the K(m) scan, NNLL/NLO ratio, FxFx cost: Phase 2 (S2).
4. Geant4 on landau and maxwell: `install_g4_local.sh` not yet run there (not my nodes). The canonical
   `tools/install/g4/pixi.{toml,lock}` changed after the first copy (added `expat`, `zlib`, `freetype` headers; lock
   sha256 now edbcef24…7291): **the orchestrator must commit the new pair**; the stamp check then forces a reinstall on
   any node installed from the older lock.
5. **A compiled MG process dir is not relocatable** (relative `lib/libLHAPDF.a` symlink): the production runner must
   create the process dir in the job's own scratch dir (or rewrite that symlink as absolute) — relevant for gridpacks
   and for Boris's runner.
6. Kept on schrodinger scratch for Phase 2 reuse: `/home/scratch/jdochoa/basil_samples` (699 MB, compiled E_LOPS and
   ZNN_J dirs, 20k-event σ runs) and `/home/scratch/jdochoa/basil_nlo` (182 MB, compiled `E_NLO`); regenerable, delete
   when not needed. Benchmark scratch deleted.
7. Not benchmarked: MLM 0–2j merged samples (v1 INC/TRG), Ẽ, the Argo-vs-SSH overhead (Boris's item).
8. Notes for Anselm (no edits made in `analyses/quirks_v2/sim/`): the v2 `sim/` port must (a) set `MG5_DIR` to
   `sw/mg5/MG5_aMC_v2_9_22`, (b) **not** add the conda env's `lib/` to `LD_LIBRARY_PATH` (pitfall 4) — v1 `produce.py`
   only set `DYLD_LIBRARY_PATH` to HEPTools/lib, which on Linux becomes `LD_LIBRARY_PATH=…/HEPTools/lib` and is
   harmless (that directory does not exist in this install; the interface has a RUNPATH), (c) point
   `mg_configure.py`'s `lhapdf-config` to `sw/envs/mg/.pixi/envs/default/bin/lhapdf-config` and `LHAPDF_DATA_PATH` to
   `sw/lhapdf_data`, (d) write MG output dirs to node-local scratch.

## Code reference (exact commands)
```
# installation (on a worker)
ssh -x schrodinger 'bash /home/users/jdochoa/hllhc-quirks-search/tools/install/install_generators.sh'
ssh -x schrodinger 'bash /home/users/jdochoa/hllhc-quirks-search/tools/install/build_heptools.sh'      # called by the above
ssh -x <worker>    'bash /home/users/jdochoa/hllhc-quirks-search/tools/install/install_g4_local.sh'
# task 2 test samples (node-local work dir, cajuela outputs, markers)
ssh -x schrodinger 'bash $QV2/phase1_strategy/src/generators/make_test_samples.sh'
# single steps
QV2_MODELS=<local copy of src/generators/models> python3 src/generators/feas_mg.py output E_LOPS <dir>
python3 src/generators/feas_mg.py launch <dir> <run> <nevents> <iseed> [mass]
python3 src/generators/feas_mg.py shower <dir> <run> <py8seed> [qedfsr]
# NLO
python3 -I src/generators/make_loop_quirkE.py $QV2_SW/mg5/MG5_aMC_v2_9_22 <models>/loop_quirkE
QV2_MODELS=<models> python3 src/generators/feas_mg.py output E_NLO <dir>
python3 src/generators/feas_mg.py launch <dir> E200_LO 0 21902001 200    # run name *_LO -> order=LO
python3 src/generators/feas_mg.py launch <dir> E200_NLO 0 21902001 200
# benchmarks
ssh -x schrodinger 'bash $QV2/phase1_strategy/src/generators/bench_all.sh'
python3 -I src/generators/collect_bench.py <bench_raw dir> outputs/feasibility/benchmarks_generators.json
# Geant4 app
cd /home/scratch/jdochoa/envs/g4 && pixi run --frozen bash -c "cmake -S src/generators/g4sv -B /var/tmp/jdochoa/g4sv_build \
   -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=\$CONDA_PREFIX -DCMAKE_IGNORE_PREFIX_PATH=/usr && make -C /var/tmp/jdochoa/g4sv_build"
pixi run --frozen /var/tmp/jdochoa/g4sv_build/g4sv src/generators/g4sv/geom_barrel.txt <nev> <seed> full|primary <out.csv>
```
