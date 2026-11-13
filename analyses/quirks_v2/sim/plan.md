# Stage 2 plan: MadGraph5_aMC + Pythia8 generation of quirk pairs (replaces code/T2_kinematics.py)

Executor E4, 2026-10-11. Status: **APPROVED 2026-10-11 (decisions in §7.1); production and validation DONE; revised after
review S2-R1 (fixer, 2026-10-11: `review/FIX_S2_R1.md`). Results: SAMPLES.md, VALIDATION.md; deferred items: DEFERRED.md.**
The plan turn ran only small probes (≤ 1000 events each; logs and scripts in `sim/probes/`); production (≈ 2.41 M LHE events
over 47 points, SAMPLES.md) followed after approval; milestones in `sim/E4_session_log.md`. Stage 2 PASS at review R2
(2026-10-11, `review/REVIEW_S2_R2.md`).
Conventions follow BRIEF.md: Λ ≡ √σ; benchmark E = (1,1)₋₁ Dirac fermion (SU(2) singlet, hypercharge −1), N_IC = 2;
alternate scalar Ẽ, also an SU(2) singlet (1,1)₋₁.
Tags: `[probe tN]` = measured here (log `sim/probes/tN_*.log`); `ESTIMATE` = my extrapolation; `[TH §x]` =
`research/theory_signal_model.md`; `[T6]`, `[T2 §x]`, `[S-13]` = theory-track reports.

---

## 0. Summary (read first)

- **Environment works.** MG 2.9.22 runs in a new, separate pixi workspace `sim/pixi.toml`: env `mg` (Python 3.9 +
  six + conda-forge LHAPDF 6.5.5) and env `ana` (Python 3.11 + pyhepmc + fastjet + mplhep) for conversion. System
  Python 3.14 fails. FeynRules runs in batch with wolframscript (Mathematica 13.3.1).
- **Model works and is cross-checked.** Hand-written UFO `sim/models/quirkE` = MG `sm` + `xe` (E, PDG 9000011)
  + `sxe` (Ẽ, PDG 9000013), with hypercharge-only couplings g_Z/g_A = −s_W/c_W. It is imported by absolute path,
  so **no symlink and no change in the MG install are needed** (§7 D10).
  - The LO σ reproduces the reference numbers of `theory_signal_model` App. A, after rescaling for α, to −0.6…+0.2 %,
    at 200/500/1000 GeV, for both E and Ẽ.
  - An independent FeynRules UFO has identical Feynman rules and gives the same σ to ≤ 0.12 %.
- **Matched generation works.** Chain: 0/1/2-jet MLM (xqcut 30, qCut 45) → Pythia8 8.313 (quirks stable, status 1)
  → HepMC → compact npz → thin loader `sim/scripts/mg_events.py`. The loader has the same return type as
  `T3_propagator.sample_events`, and a smoke test with `T3_causal.run_causal` passes.
- **Two findings from the probes change the design.**
  1. **The trigger sample needs a matrix-element (ME) cut of pT(QQ̄) > 100 GeV, not 150.** MLM matches jets to
     partons by angle, so hard ISR can be absorbed into a soft ME jet. With a 150 GeV ME cut, ≈ 6 % of the
     pT(QQ̄) > 200 GeV tail is lost; below 100 GeV the loss is ≲ 1-2 % [probe t10]. **[Overturned in production:
     the 100 GeV cut misses 4.0-7.1 % of the tail; remedy = stitched TRGS samples, VALIDATION §4.4.]**
  2. **MG prints the merged cross section in the wrong unit.** It labels it "pb", but the value is in fb. We compute
     σ from the HepMC weights ourselves.
- **First look at the ISR model (1000-event probes, so not yet conclusive).** At m = 500 GeV with pT > 200 GeV and
  |η| < 2.5, the median γ*−1 is 0.249 in MG MLM and 0.274 in T2's LO V*+jet. So T2's ℓ_max may be ≈ 9 ± 6 % high.
  Production statistics will settle this (§6 V3). **[Settled: a fluctuation; T2 V*+jet is good to −4…+0.5 %, VALIDATION §3.]**
- **Proposed production.** ≈ 2.3 M showered LHE events, ≈ 35 CPU-h (≈ 6-7 h wall on 6 cores) and ≈ 2.5 GB kept,
  plus ≤ 2 GB of transient HepMC (§4).
- **Decisions needed from the user: §7.** The main ones are the tune (CP5 vs Monash), the ME cut, the mass grid,
  the normalisation (K-factor vs NLO), the PDF download, and the EW scheme.

---

## 1. Environment findings

| Item | Result | Evidence |
|---|---|---|
| System `python3` 3.14 | MG fails at start-up (`six` missing; Python 3.14 is untested with MG 2.9) | [probe t0] |
| conda env `/opt/miniconda3/envs/madgraph` (Python 3.9.21, numpy 2.0.2, six) | MG runs | [probe t0]; used read-only, not chosen |
| **`sim/pixi.toml` env `mg`** (Python 3.9, six, numpy 1.26, conda-forge `lhapdf` 6.5.5) | **MG runs, including the python `systematics` module**. **Chosen** (reproducible, separate from `../pixi.toml`) | [probes t1-t14] |
| `sim/pixi.toml` env `ana` (Python 3.11, numpy, scipy, matplotlib, mplhep, pyhepmc 2.16, numba, fastjet 3.5.2 via PyPI) | conversion, validation, plots | [probe inspect_hepmc] |
| theory-track env `../pixi.toml` (Python 3.12) | untouched; runs `code/T3_causal.py` with the new loader | smoke test (§5) |
| HEPTools LHAPDF Python bindings (py3.9) | **segfault**: they link `@rpath/libpython3.9.dylib`, which no current Python provides | [otool] |
| Workaround | each MG output gets its own `Cards/me5_configuration.txt` pointing to the pixi LHAPDF (`scripts/mg_configure.py`). The MG install is not changed | [probe t3] |
| CT18NLO with LHAPDF 6.5.5 + MG Fortran glue | needs metadata keys missing from the CT18NLO .info, both the local copy and the current official file: `AlphaS_FlavorScheme`, `AlphaS_NumFlavors`, `AlphaS_Lambda4/5`. A patched copy is in `data/sim/lhapdf/`. Changing the Λ placeholders leaves σ identical (2.454 fb both times) | [probes t3, t14] |
| Pythia8 (HEPTools) | 8.313, with the MG5aMC_PY8_interface; MLM in weight mode with merging-scale variations works | [probe t5] |
| FeynRules + wolframscript | Mathematica 13.3.1 batch OK. `sim/models/fr/make_ufo.wls` writes `quirkE_FR_UFO` in ≈ 2 min. MG needs `convert model` (py2 → py3) once | [probe t11] |
| Fastjet for MG | not configured; MG falls back to fjcore (fine for MLM) | MG banner |
| Delphes | not used, not installed | — |

**Footprint in the MG install (please note).**
- My first probe used `set auto_update 0`, which wrote `input/mg5_configuration.txt`. I **reverted it by hand**:
  - the line is back to `# auto_update = 7`;
  - one `mg5_path` line that had just been appended was removed (three identical ones remain, as before).
- MG rewrites `input/.autoupdate` (its update-check timestamp) at every launch. This cannot be avoided without
  editing the install.
- Production scripts will never use `set <config option>`.
- No symlink was created.

---

## 2. Model design

### 2.1 Hand-written UFO `sim/models/quirkE/` (primary)
- **Base.** A verbatim copy of MG's `sm` UFO v1.3 (Gμ scheme: inputs aEWM1 = 132.507, G_F, M_Z = 91.188 GeV;
  derived s_W² = 0.22225). Additions are appended to `parameters.py`, `particles.py`, `couplings.py` and
  `vertices.py`, inside blocks marked "quirkE additions".
- **Fields.**

| name (MG) | PDG | spin | charge | colour | mass param (SLHA) | width |
|---|---|---|---|---|---|---|
| `xe-` / `xe+` (E, Dirac) | 9000011 | 1/2 | −1 | 1 | `MXE` (MASS 9000011), default 500 | `WXE` = 0 (DECAY 9000011) |
| `sxe-` / `sxe+` (Ẽ, complex scalar) | 9000013 | 0 | −1 | 1 | `MSXE` (MASS 9000013), default 500 (501 in the restrict cards, so that MG does not merge the two masses) | `WSXE` = 0 |

  The PDG ids are free in Pythia's ParticleData; its 900xxxx entries are 9000111, 9000211, 9000221, 9010221 and 99xxxxx.
- **Couplings.** Hypercharge only; no Yukawa, Higgs portal or mixing with SM leptons. With Z = c_W W³ − s_W B and
  A = s_W W³ + c_W B, a T₃ = 0 state couples through g′YB = eQ A − eQ (s_W/c_W) Z. Hence **g_Z/g_A = −s_W/c_W**.
  This ratio does not depend on the sign convention, given the SM file. The internal parameter `QXE = −1`
  appears explicitly in the couplings.

| vertex | Lorentz | coupling (MG sm normalisation: γ vertex of charge Q = i e Q) | value for Q = −1 |
|---|---|---|---|
| xe+ xe− A | FFV1 = γ^μ | `GC_XEA` = i e Q | −i e (MG merges it with `GC_3`) |
| xe+ xe− Z | FFV1 | `GC_XEZ` = −i e Q s_W/c_W | +i e s_W/c_W (= 2·GC_59, the e_R coupling) |
| A sxe− sxe+ | VSS1 = p₂ − p₃ | `GC_XEA` | as in the SM [a, G−, G+] (GC_3) |
| Z sxe− sxe+ | VSS1 | `GC_XEZ` | |
| A A sxe− sxe+ | VVSS1 | 2 i e² Q² | = GC_6 |
| A Z sxe− sxe+ | VVSS1 | −2 i e² Q² s_W/c_W | |
| Z Z sxe− sxe+ | VVSS1 | 2 i e² Q² s_W²/c_W² | |

- **Normalisation of the seagulls** (identical-boson factor) was checked against the SM Goldstones:
  GC_6/GC_63/GC_64 = 2ie²·(1, r, r²) with r = (c²−s²)/(2sc). For Ẽ, r = −s_W/c_W.
- **Checks of the coupling sign against App. A of the model reference.**
  - T2 and App. A use v_E = (T₃ − 2Q s_W²)/(2 s_W c_W) = +s_W/c_W and a_E = 0, which is the same ratio.
  - The γ-Z interference is large: −39 % of Q_u² for uū at M ~ 1 TeV. A sign error would therefore change σ by
    ~×1.8, and the 0.1-0.6 % agreement in §2.3 excludes it.
  - The task's g_Z = −(g/c_W)(−Q s_W²) together with a photon coupling −eQ gives the same ratio −s_W/c_W.
- **Restrictions.** `restrict_no_b_mass.dat` (5-flavour, massless b; used in production) and `restrict_default.dat`,
  both extended with the new MASS/DECAY entries.
- **Infracolour.** Not in the UFO. **Every σ and weight in the samples is for N_IC = 1.** The loader's
  `sigma_lo_mlm_fb(..., n_ic=2)` (alias `sigma_fb`) applies N_IC = 2; `sigma_norm_fb` includes N_IC = 2 and K.

### 2.2 FeynRules cross-check UFO `sim/models/fr/` (independent, done)
- **Model.** `quirkE.fr` declares only the two classes F[100], S[100] with QuantumNumbers {Y → −1, Q → −1}. Their
  Lagrangian is `I xebar.Ga[mu].DC[xe,mu] − MXE xebar.xe + DC[sxebar,mu] DC[sxe,mu] − MSXE² sxebar sxe`, with the
  SM.fr covariant derivative. So the couplings come from FeynRules' own U(1)_Y machinery, not from my file.
- **Batch run.** `wolframscript -file make_ufo.wls` writes `quirkE_FR_UFO` [probe t11; log `models/fr/make_ufo.log`].
- **Feynman rules printed by FeynRules.**
  - E: −ie γ^μ (A) and +ie (s_W/c_W) γ^μ (Z).
  - Ẽ: −ie(p_sxe − p_sxebar) (A), +ie(s_W/c_W)(p_sxe − p_sxebar) (Z), 2ie² (AA), −2ie² s_W/c_W (AZ),
    2ie² s_W²/c_W² (ZZ).
  - These are identical to §2.1.
- **σ comparison** [probe t12]. Settings: p = g u d s ū d̄ s̄; CT18NLO; μ = √ŝ; m = 500 GeV; identical EW inputs
  (aEWM1 132.507, G_F 1.16639e-5, M_Z 91.188).

| | FeynRules UFO | hand-written UFO | ratio |
|---|---|---|---|
| σ(pp → EĒ) [fb, N_IC = 1] | 2.413 ± 0.005 | 2.410 ± 0.006 | 1.0012 ± 0.003 |
| σ(pp → ẼẼ*) [fb] | 0.1816 ± 0.0005 | 0.1818 ± 0.0005 | 0.999 ± 0.004 |

### 2.3 Cross section vs the reference LO numbers (done) [probes t3, t4]
Settings: inclusive pp → QQ̄; 5 flavours; CT18NLO member 0; μ_F = μ_R = √ŝ; MG Gμ inputs (α = 1/132.507,
s_W² = 0.22225). App. A [TH App. A] uses α = 1/127.9 and s_W² = 0.2222, so its numbers are scaled by
(127.9/132.507)² = 0.9317.

| m_Q | E: MG [fb] | E: App. A × 0.9317 | Δ | Ẽ: MG [fb] | Ẽ: TH §2.3 (14 TeV)/(2K) × 0.9317 | Δ |
|---|---|---|---|---|---|---|
| 200 | 92.52 ± 0.20 | 92.33 | +0.2 % | 8.046 ± 0.022 | 8.06 | −0.2 % |
| 500 | 2.454 ± 0.006 | 2.456 | −0.1 % | 0.1843 ± 0.0005 | 0.1843 | 0.0 % |
| 1000 | 0.0727 ± 0.0002 | 0.0731 | −0.6 % | 0.004377 ± 0.000012 | 0.004384 | −0.2 % |

Note on the T2 cache: T2's cache weights are in arbitrary units, so T2 has no absolute σ of its own. Its
normalisation is the App. A / TH §2.3 table above.

---

## 3. Processes and cards

### 3.1 Processes (MG syntax; model `import model <abs>/sim/models/quirkE-no_b_mass`; `define p = p b b~`, `define j = j b b~`)

| key | process | matching |
|---|---|---|
| `LOPS` | `p p > xe+ xe-` | none (ISR only from the Pythia shower; the "old-style" reference for S-13) |
| `INC` | `p p > xe+ xe- @0`; `add process p p > xe+ xe- j @1`; `add process p p > xe+ xe- j j @2` | MLM, 5F, kT-MLM, `ickkw = 1`, `xqcut = 30`, `maxjetflavor = 5`, `asrwgtflavor = 5`, `dynamical_scale_choice = -1` (CKKW clustering), `JetMatching:qCut = 45`, `nJetMax = 2` |
| `TRG` | as `INC`, plus the ME cut pT(QQ̄) > 100 GeV (`scripts/patch_ptqq_cut.py` patches `SubProcesses/dummy_fct.f` of the output directory: \|Σ p_T of non-jet final states\| > PTMIN, so the 0-jet subprocess gives 0) | MLM as `INC` |
| `S-*` | same with `sxe+ sxe-` | same |
| `NJ1` (validation) | 0/1-jet only | MLM |
| `GAMGAM` (optional) | `a a > xe+ xe-` with NNPDF23_lo_as_0130_qed (photon PDF) | none |

### 3.2 Cards (templates go to `sim/cards/`; `scripts/mg_configure.py` applies them per output directory)
- **run_card.**
  - `ebeam1/2 = 7000`, `pdlabel = lhapdf`, `lhaid = 14400` (CT18NLO), `nevents ≤ 20000` per chunk, fixed `iseed`
    per chunk (recorded in SAMPLES.md).
  - `use_syst = True`, with `systematics_arguments = ['--mur=0.5,1,2', '--muf=0.5,1,2', '--dyn=-1,1,2,3,4',
    '--pdf=CT18NLO']`. This gives 9 μ points × 4 dynamical scales and 58 Hessian members, if the full set is
    installed (§7 D7). During the probes only `@0` was available.
  - `event_norm = average` (the default).
- **param_card.** `MXE` / `MSXE` set per run (`set MXE <m>` in the launch script); widths 0; SM defaults otherwise.
  `QNUMBERS` blocks are written by MG and read by Pythia.
- **pythia8_card.** The MG default plus `sim/cards/pythia8_quirk_common.dat`:
  - `9000011:all = xe- xe+ 2 -3 0 m ...`, `mayDecay = off`, `isResonance = off`; the same for 9000013.
  - Pythia then imports the masses from the SLHA in the LHE header [probe t5 log].
  - `JetMatching:qCut = 45`. In weight mode the MG interface also writes the qCut = 67.5 and 90 variation weights.
  - Tune: §7 D1. MPI on, hadronisation on (§7 D2). Vertex spread off (§7 D9). QED FSR from quirks on (default).
- **Seeds and chunks.** Each (sample, mass) is split into ≤ 20k-event MG runs with distinct seeds. Each run is
  showered, converted, and its HepMC deleted before the next starts.

### 3.3 Orchestration scripts (to write in the execution turn; all in `sim/scripts/`)
- `produce.py <sample> <spin> <m> <N>`: `output` (once per process class) → `mg_configure.py` → `patch_ptqq_cut.py`
  (TRG only) → `launch` chunk → `convert_hepmc.py` → delete HepMC → append the entry to `SAMPLES.md` and
  `../data/sim/SAMPLES_INDEX.json`.
- It runs with `LHAPDF_DATA_PATH=../data/sim/lhapdf`, uses MG multicore with `nb_core = 6`, and logs to
  `sim/logs/`.
- `merge_chunks.py`: concatenates the chunk npz files of one sample and renormalises the weights to the total N_LHE.
- `validate_*.py`: §6. Plots use mplhep with a non-CMS label (Stage-5 convention), in `sim/figures/`.

---

## 4. Sample table, CPU and disk

**Measured per-event costs** [probes t5-t10; M3, 6 parallel jobs]:
- **MG (survey + refine, 0-2j MLM).** About 20-25 s overhead per launch (startup and survey; the refine for 1000
  events takes < 5 s wall), so ≈ 3 ms CPU/event at large N (ESTIMATE). The systematics module with 92 weights adds
  a few seconds per 1000 events; with the full CT18NLO set (≈ 150 weights) ESTIMATE ≈ 5-10 ms/event.
- **Pythia8** (MLM weight mode, MPI, hadronisation, HepMC write): ≤ 36 ms CPU/event (6 s wall for 1000 events on
  6 jobs, initialisation included).
- **Conversion** (pyhepmc + fastjet): 4.6 ms per HepMC event. In weight mode all events stay in the HepMC; vetoed
  ones are skipped in the npz.
- **MLM matching efficiency.** 0.40 (INC) and 0.38 (TRG, cut 150) at 500 GeV. Of the matched TRG events with an
  ME cut of 100 GeV, ≈ 50 % have pT(QQ̄) > 200 GeV after the shower (ESTIMATE between 0.41 at 80 GeV and 0.76 at
  150 GeV [probes t7, t10]).
- **Sizes.**
  - HepMC: 75-84 MB per 1000 events (1342 particles/event), transient only.
  - LHE.gz with 92 weights: 0.42-0.49 kB/event; ≈ 0.7 kB with the full PDF set (ESTIMATE).
  - npz: 0.45 kB per kept event (92 weights); ≈ 0.7 kB with 150 weights; half that if `wvar` is stored as float32.
- **Total per LHE event:** ≈ 45-50 ms CPU.
- **Measured in production (2026-10-11):** all 46 points (2.07 M LHE events; the first VALIDATION draft said 2.40 M) took 2 h 48 min wall with our own parallel Pythia jobs (≈ 4 min per 50k chunk: MG 1 min, PY8 2 min, conversion in parallel), ≈ 18 CPU-h (ESTIMATE from wall × cores). Kept on disk: data/sim ≈ 4.5 GB (npz 2.0 GB including the stitched TRGS files, LHE 1.6 GB, aux 0.9 GB). See SAMPLES.md and VALIDATION.md.
- **Review S2-R1 additions (fixer, 2026-10-11), within this budget:** top-ups E-TRG/E-INC 200 GeV +100k LHE each, E-TRG 300
  +40k, E-INC 300 +50k (B-4: effective tail statistics ≥ 5× the expected 3 ab⁻¹ signal after ε = 0.18); off-grid V-INTERP
  550 GeV INC 50k (B-7); V-SHOWER as 4 × 50k re-showers of 500 GeV chunk 0 (this table); MG `--alps` weights on the benchmark
  LHE. ≈ 5.5 CPU-h, total ≈ 23.5 CPU-h of the 35 CPU-h budget; delivered total 2.41 M LHE events.

**Matched cross sections at 500 GeV** [probes t5, t7, t10] (fermion, N_IC = 1, LO, CT18NLO, scale −1):
- σ_LHE(0-2j) = 5.395 fb, and σ_matched(qCut = 45 / 67.5 / 90) = 2.131 / 2.314 / 2.428 fb.
- For comparison, the inclusive LO at μ = √ŝ is 2.454 fb.
- TRG with ME cut 150: σ_LHE = 0.776 fb and σ_matched = 0.297 fb. With ME cut 80: σ_LHE = 1.487 fb and
  σ_matched = 0.571 fb.

| ID | process | spin | masses [GeV] | N_LHE per mass | cuts | kept (matched) per mass | of which pT(QQ̄) > 200 | CPU [h] | kept disk |
|---|---|---|---|---|---|---|---|---|---|
| E-LOPS | pp→EĒ + PS | F | 200, 500, 1000 | 50k | — | 50k | ≈ 4-5k | 1.9 | 0.1 GB |
| E-INC | 0-2j MLM | F | 200, 500, 1000 | 100k | — | ≈ 40k | ≈ 4k | 3.8 | 0.3 GB |
| E-TRG | 0-2j MLM | F | 200, 500, 1000 | 100k | ME pT(QQ̄) > 100 | ≈ 40k | ≈ 20k | 3.8 | 0.3 GB |
| E-TRG-fine | 0-2j MLM | F | 300, 400, 600, 700, 800, 900, 1100, 1200, 1300, 1400, 1500 | 40k | ME pT(QQ̄) > 100 | ≈ 16k | ≈ 8k | 5.6 | 0.4 GB |
| E-INC-fine | 0-2j MLM | F | same 11 | 20k | — | ≈ 8k | ≈ 0.8k | 2.8 | 0.2 GB |
| S-INC | 0-2j MLM | S | 200, 500, 1000 | 50k | — | ≈ 20k | ≈ 2k | 1.9 | 0.15 GB |
| S-TRG | 0-2j MLM | S | 200, 500, 1000 | 50k | ME pT(QQ̄) > 100 | ≈ 20k | ≈ 10k | 1.9 | 0.15 GB |
| S-LOPS | pp→ẼẼ* + PS | S | 200, 500, 1000 | 20k | — | 20k | ≈ 2k | 0.8 | 0.05 GB |
| S-TRG-fine (optional) | 0-2j MLM | S | 300, 400, 600, 700, 800 | 40k | ME pT(QQ̄) > 100 | ≈ 16k | ≈ 8k | 2.6 | 0.2 GB |
| V-MERGE | INC, (xqcut, qCut) = (20, 30) and (50, 75) | F | 500 | 2 × 50k | — | ≈ 20k each | | 1.3 | 0.1 GB |
| V-NJ1 | 0-1j MLM | F | 500 | 50k | — | | | 0.6 | 0.05 GB |
| V-MPI | TRG, MPI off (and a hadronisation-off copy) | F | 500 | 50k | ME > 100 | | | 0.5 | 0.05 GB |
| V-TUNE | TRG with the other tune (§7 D1) | F | 500 | 50k | ME > 100 | | | 0.6 | 0.05 GB |
| V-SHOWER | ISR/FSR ×2, ×½ (Pythia `UncertaintyBands` weights if the MG interface passes them to HepMC; else 2 runs) | F | 500 | 0-100k | ME > 100 | | | 0-1.3 | 0.1 GB |
| V-GAMGAM (optional) | γγ → EĒ, NNPDF23_lo_as_0130_qed | F | 500 | 10k | — | 10k | | 0.1 | 0.01 GB |
| **Total** | | | | **≈ 2.3 M** | | **≈ 1.0 M** | | **≈ 30 + 3-5 (MG overhead, systematics) ≈ 35 CPU-h ≈ 6-7 h wall** | **≈ 2.5 GB** (LHE ≈ 1.6 GB + npz ≈ 0.8 GB), plus ≤ 2 GB transient HepMC |

**Sizing rationale (Stage 3: ≥ 200 events per (m_Q, Λ) point after any selection).** [S2-R1, B-4: read "≥ 200
*effective* events (Kish N_eff = (Σw)²/Σw²) after selection, and MC stat ≤ ⅓ of the 3 ab⁻¹ data stat for P2 template points".
TRGS tail N_eff/N is 0.70-0.90; SAMPLES.md quotes N_eff per file.]
- Kinematics do not depend on Λ. Stage 3 propagates **the same events** at Λ ∈ {0.3, 0.45, 0.6, 1, 2, 3, 5, 10} keV.
- With N(pT > 200) ≈ 20k at the benchmarks, 200 events survive down to a total selection efficiency of 1 %.
  On the fine grid (≈ 8k), they survive down to ≈ 2.5 %.
- Knapen's ε_fid × ε_reco ≈ 0.28 × 0.65 = 0.18 [1708.02243 Tab. I, via TH §7] is ≫ 1 %. Points with ε < 1 %
  (deep Λ edges) can be topped up with extra TRG chunks at ≈ 1 CPU-h per 20k matched events.
- The 50k LO+PS and 100k INC samples give the ISR-tail comparison (§6 V3) a statistical error of ≤ 1-1.5 % on the
  median of ℓ_max (≈ 4-20k tail events).

---

## 5. Output format and loader

**Converter `sim/scripts/convert_hepmc.py` (written and tested).** One npz per (chunk, merged sample), in
`../data/sim/npz/`. Each row is an event with a non-zero weight at any merging scale.
- **Quirk momenta.** `p_qp`, `p_qm`: (E, px, py, pz) [GeV] of the positive and negative quirk after the shower.
  `p_qp_hard`, `p_qm_hard`, `p_qq_hard`: the same before the shower (LHE kinematics).
- **Vertex.** `vtx` = (x, y, z, ct) [cm]: the origin, because Pythia's vertex spread is off (§7 D9).
- **ISR-recoil system** (for S-4/S-5 MET studies):
  - `recoil`: Σ of final-state particles except quirks and ν;
  - `recoil_eta5`: the same with |η| < 5;
  - `nu`: Σ of the neutrinos;
  - `jets[4]`: (pT, η, φ, m) of the 4 leading anti-kT R = 0.4 jets with pT > 20 GeV and |η| < 5; `njet`;
  - `n_me`: the ME jet multiplicity (0/1/2).
- **Weights.**
  - `w` [fb per event, N_IC = 1]: Σ w = σ_matched at the nominal qCut.
  - `wvar[N, K]` with `wvar_names`: every variation in the HepMC (3 merging scales, 9 μ × 4 dynamical scales, PDF
    members), in the same units.
  - Normalisation: MG writes pb with `event_norm = average`, so w_fb = w_pb × 10³ / N_LHE.
  - Check: Σ w reproduces MG's merged σ (2.1309 "pb" printed by MG = 2.1309 fb) [probe t5].
- **Derived columns:** `gamma_star`, `cstar` (T2 convention: cos between the quirk axis and the pair velocity),
  `bg_pair`, `eta_pair`, `y_pair`, `pt_pair`, `m_pair`.
- **Metadata:** `mq`, `spin`, `sigma_lhe_fb`, `nlhe`, `n_in_file`, `merging_nominal`, `source`, `tag`,
  `n_ic_included = 0`.
- **Pythia record [probe t5].**
  - Exactly two status-1 quirks per event (998/998), with history codes 23 → 44 (ISR recoil) → 52.
  - No decays; vertex (0, 0, 0, 0).
  - 998 of 1000 LHE events reached the HepMC. The loss comes from splitting into 6 shower jobs; normalisation uses N_LHE.

**Loader `sim/scripts/mg_events.py` (written; needs no change in `code/`).**
- `sample_events_mg(m, n, sample='trig', spin='F', rng, eta_max, ptmin)` has **the same return type as
  `T3_propagator.sample_events`**: a list of `(p1, p2, info)`.
  - p1 is the **positive** quirk, matching the default `run_causal(..., charges=(+1, −1))`.
  - `info` holds w, γ*, cos θ*, (βγ)_pair, η, pT, M, vtx, recoil, jets and the row index.
- `iter_events(...)` yields the selected events in file order, so Stage 3 can take the first N at every Λ, **provided the
  per-event weights `info['w']` are used** (the TRGS INC rows carry 3.7-9.6× the TRG weight; TRGS rows are shuffled so a prefix
  is fair) or `iter_events(..., unweight=True)` (deterministic hit-or-miss) is used. `split='template'|'toy'` selects
  disjoint halves for P2 (column `tt_split`). [S2-R1, A1 / B-8]
  `sigma_lo_mlm_fb(..., n_ic=2, weight=...)` (old name `sigma_fb`) returns the LO-MLM σ of a selection (Gμ, no K) for any
  weight variation; **yields use `sigma_norm_fb(...)`** = σ_norm (N_IC = 2, LO × K) × Σw_sel/σ_ref. [S2-R1, B6]
- Samples are found through `../data/sim/SAMPLES_INDEX.json`, keyed `'{spin}_{m}_{sample}'`.
- **Legacy path.** `write_t2_compat_cache()` writes an npz with the old keys
  `{spin}_{m}_{isr}_{gamma_star,w,cstar,bg_pair,eta_pair}`, so old scripts run unchanged with
  `export T2_CACHE=<file>`.
  - The old reader re-randomises the azimuths, which loses the ISR-jet ↔ quirk-plane correlation (needed for S-5).
  - Its key `incl` assumes pT = 0, so MG samples must always go in under `isr`.
- **Smoke test** [§ "smoke test", 2026-10-11]. 3 events from the 150-GeV probe were run through
  `T3_causal.run_causal(p1, p2, 500, 1 keV, material=False)` in the theory-track env: status 1, 4-24 hits,
  plane thickness 11-30 µm, < 0.1 s per event.

---

## 6. Validation plan (with pass criteria)

| ID | Check | Method | Pass criterion |
|---|---|---|---|
| V1a | LO σ, hand-written UFO vs App. A [TH App. A] | inclusive, μ = √ŝ, α rescaled | \|Δ\| ≤ 1 % at 200/500/1000, F and S. **Done: −0.6…+0.2 % PASS** |
| V1b | hand-written vs FeynRules UFO | §2.2 | ≤ 0.5 % (3σ_MC). **Done: 0.12 % / 0.1 % PASS**. In execution: repeat at 200 and 1000 GeV and on one MLM shape (pT(QQ̄)) |
| V1c | vs T6 [T6 §2] and TH §2.3 | LO_CT18 × K_WG × N_IC = 2 vs T6's LO × K with NNPDF3.1 luxqed (219 / 5.94 / 0.179 fb) | within 10 % (different PDF; T6 itself is within 9 % of TH) |
| V1d | vs the literature K-factors | MG systematics reweighting to NNPDF23_lo (set in the HEPTools tarball): K_lit = K_WG × σ_LO^CT18/σ_LO^NNPDF23LO vs 2404.13814 Sec. 3 (E: 1.33 at 200 GeV, 1.45 at 1 TeV, 13 TeV) | within 6 % (as TH §2.2 found) |
| V1e | MLM normalisation | σ_matched (3 qCut values, 4 dynamical scales) vs inclusive LO at the same scale choice | within ±15 %. Normalisation is in any case taken from TH §2.3 (§7 D6) |
| V2 | kinematics vs the old cache `data/cache/T2_kinematics_cache.npz` (keys `{F,S}_{200,500,1000}_{incl,isr}_{gamma_star,w,cstar,bg_pair,eta_pair}`) | weighted 16/50/84 quantiles (bootstrap errors) and normalised-shape χ² of pT(QQ̄), γ*, m(QQ̄), y/η_pair, cos θ* | inclusive (E-LOPS γ* and m(QQ̄) vs T2 `incl`): medians within 2 %, which tests ME + PDF. Tail (pT > 200, \|η\| < 2.5, vs T2 `isr`): measured, no criterion (it is the measurement of the T2 bias); every difference > 3σ must be explained |
| V3 | **ISR tail and ℓ_max bias (S-13)** | for F and S at 200/500/1000, compare four models against (iv): (i) T2's fixed-pT = 250 trick on LO kinematics; (ii) T2 LO V*+jet; (iii) MG LO+PS; (iv) MG MLM nominal. Observables: f(pT > 200) and the 16/50/84 quantiles of 2(γ*−1) ∝ ℓ_max and of N_osc (T2 formula, R = 110 cm, \|z\| = 270 cm), with \|η\| < 2.5 | stat. error of the (iv) median ≤ 1.5 %. The bias of (i)-(iii) relative to (iv) is quoted with MC-stat + merging + scale uncertainties, and S-13's "ℓ_max −10…−25 %, N_osc +20 %" is confirmed or corrected. Probe hint: (ii) vs (iv) median γ*−1 is 0.274 vs 0.249 ± ~0.015 |
| V4a | MLM DJR | `tag_*_djrs.dat` (d01, d12 by multiplicity), mplhep plots | the summed DJR is smooth across qCut: no step > 10 % in the two bins next to log₁₀(qCut) |
| V4b | merging-scale variation | (20, 30), (30, 45), (50, 75) runs and in-weight 67.5/90 | change in f(pT > 200) and the pT(QQ̄) tail shape ≤ 10 %, else assigned as a systematic. In-weight and separate-run results agree within stat. (tests MG's weight-mode variations) |
| V4c | multiplicity | 0-1j vs 0-2j | f(pT > 200) within 5 % at 500 GeV |
| V4d | **ME-cut closure** | TRG vs INC for pT(QQ̄) > 200 after the shower; migration fraction (ME pT < 100 among final pT > 200) measured in INC | σ ratio = 1 within max(2 %, 2σ). Migration ≤ 1 %, else lower the cut to 80 GeV (probe: ≈ 1.3 % below 100) |
| V5 | scale and PDF bands | systematics weights: 9-point μ, 4 dynamical scales, CT18NLO Hessian (90 % CL → 68 %: ÷1.645), optionally PDF4LHC21_40; Pythia shower weights | LO scale band on σ matches TH §2.3 (+5.3/−4.9 % at 500 GeV, μ×½/×2 at √ŝ) within 1 percentage point. The bands on f(pT > 200) and on the ℓ_max median are reported |
| V6 | Pythia sanity | per sample | 2 status-1 quirks per event, no daughters, \|Σ p_T(all final incl. ν, quirks)\| < 1 GeV, fraction of events with a quirk-FSR photon pT > 10 GeV reported |
| V7 | interface to T3 | loader + `run_causal` on 200 events per benchmark at Λ = 1 keV (B on, material on); plane-thickness and N_hits distributions vs the same with the old cache | runs without error. Differences are consistent with the V2/V3 kinematic changes; no criterion on physics |
| V8 | MPI / tune / shower | V-MPI, V-TUNE, V-SHOWER at 500 GeV | f(pT > 200) and the γ* median shift ≤ 3 % (MPI); tune and shower shifts are reported as systematics |

Deliverables of the validation: `sim/VALIDATION.md` (tables above filled in), `sim/figures/*.png` (mplhep, non-CMS
label), and `sim/SAMPLES.md` (inventory with σ, N, seeds, files, md5).

---

## 7. Decisions needed from the user (my recommendation, confidence)

| # | Decision | Recommendation | Confidence |
|---|---|---|---|
| D1 | Pythia tune | **CP5** (CMS standard; parameters to be verified from the CMS tune paper 1903.12179 before use, since I am quoting them from memory) for the nominal samples; Monash (Pythia default) as V-TUNE. Shower PDF follows the tune | MEDIUM |
| D2 | MPI | **ON**, with hadronisation ON. MPI does not change the quirk kinematics beyond the sub-% interleaved-ISR competition (checked in V-MPI). It makes the recoil, MET and underlying-event occupancy realistic for S-4/S-5 and the Stage-4 ACTS overlay. With only compact summaries stored, the cost is CPU (≈ 30 %), not disk | MEDIUM-HIGH |
| D3 | Matching | kT-MLM, 0-2 jets, 5F, **xqcut = 30, qCut = 45 GeV** for all masses, well below the 200 GeV trigger scale. Validated by V4a-c. Alternative: mass-dependent qCut ≈ m/10. Literature: Knapen MLM ≤ 1j [1708.02243 §III.A]; Li et al. MLM ≤ 2j [1911.02223 §III] | MEDIUM |
| D4 | Trigger sample | **ME cut pT(QQ̄) > 100 GeV** (unweighted, simple for Stage 3; ≈ 1-2 % tail loss to be closed by V4d). Alternative: MG `ptj_bias` weighted generation (unbiased, but weighted events complicate the "≥ 200 events" bookkeeping) | MEDIUM |
| D5 | Mass grid | F: 200-1500 GeV in 100 GeV steps (14 masses; full samples at 200/500/1000, TRG + small INC elsewhere). This covers the ≈ 1.1-1.2 TeV reach [TH §7] and the \|q\| = 2 reach ≈ 1.3 TeV [T6]. S: 200/500/1000 full; TRG at 300-800 optional (reach ≲ 600 GeV [TH §7]) | MEDIUM (F) / LOW (S fine grid) |
| D6 | NLO / K-factors | Use LO-MLM shapes and normalise to σ_E(14 TeV) of TH §2.3 (LO_CT18 × K_WG, NNLL slepton-based, N_IC = 2), interpolated on the grid, with the WG PDF band. **No NLO generation now.** Optional later: MG5_aMC NLO + FxFx at 500 GeV as the ISR systematic (S-13). That needs a loop-capable UFO, i.e. our additions on top of MG's `loop_sm`: ≈ 1-2 days | MEDIUM |
| D7 | PDF | **CT18NLO** (consistent with T2, TH and T6 checks). **Download** the full set (59 members, 19 MB tarball from lhapdfsets.web.cern.ch) into `data/sim/lhapdf/`. Optionally PDF4LHC21_40 (the WG recommendation used in TH §2.3) for reweighting. NNPDF23_lo_as_0130_qed comes from the HEPTools tarball (extracted, the install is not modified), used for V1d and the γγ sample. Not NNPDF23 LO as nominal: it is ~8-15 % lower, and LO PDFs are not what TH normalises to | MEDIUM |
| D8 | EW scheme | Generate in the MG `sm` Gμ scheme (α = 1/132.5, shapes unaffected). Normalise with TH §2.3, which uses α(M_Z) = 1/127.9. Carry the ±7 % EW-scheme nuisance of TH §2.4. **[Corrected S2-R1 (B1): TH §2.4/§5 recommend ±5 % (K transfer + scheme); 7 % is the α² ratio; σ_norm inherits the WG scheme through K_WG, VALIDATION §1.3]** | MEDIUM |
| D9 | Production vertex | Pythia vertex spread off; the converter writes the origin; the HL-LHC beam spot is applied in Stage 4. `T3_causal` already assumes production at the origin | LOW |
| D10 | MG `models/` symlink | **Not needed** (import by absolute path works), so I propose not to create it and to leave the install untouched. I will create it only if you want `import model quirkE` convenience | LOW |
| D11 | Scale of production | ≈ 2.3 M events, ≈ 35 CPU-h (≈ 6-7 h wall on 6 cores), ≈ 2.5 GB kept in `data/sim/`. Optional items: S-TRG-fine, V-GAMGAM, V-SHOWER separate runs | LOW-MEDIUM |
| D12 | QED FSR off the quirks in Pythia | keep (default `TimeShower:QEDshowerByOther = on`). It is physical at production, where the string is irrelevant on the hard-emission scale. Its rate is reported (V6). **[S2-R1: did not take effect: `QEDshowerByOther` acts only on resonances and the SLHA DECAY block resets the flag; opt-in fix `cards/pythia8_quirk_qedfsr.dat`; effect −0.1…−1.1 % (stat. ±0.5…0.8 %) on the ℓ_max median; samples not regenerated, VALIDATION §7. Default: not applied; pending user decision: re-shower ≈ 15 CPU-h vs one-sided systematic (S2-R2)]** | LOW-MEDIUM |
| D13 | \|q\| = 2 singlet variant (T6 G-T6-3, WORTH A CHECK) | out of scope unless requested. It would be a one-line model variant (QXE = −2 plus a new particle charge) | LOW |

### 7.1 Decisions APPROVED by the user (2026-10-11, via the orchestrator)
| # | Approved | Implementation / evidence |
|---|---|---|
| D1 | CP5 nominal, Monash as check | `cards/pythia8_tune_CP5.dat`. Every value is checked against CMS, arXiv:1903.12179 (text cache `research/cache/pdf/1903.12179.txt`): **Table 3** (txt l.897-918, CP5 column): NNPDF3.1 NNLO; α_S(m_Z) = 0.118 with NLO running for ISR, FSR, MPI and ME; `SpaceShower:rapidityOrder = on`; `MultipartonInteractions:EcmRef = 7000`; `pT0Ref = 1.41`; `ecmPow = 0.03`; `coreRadius = 0.76`; `coreFraction = 0.63`; `ColorReconnection:range = 5.18`. **Sec. 3** (l.702 MPI-based CR model; l.715-721 CP5 = CP4 + rapidity-ordered ISR, hadronisation and beam remnants at Monash; l.721-726 double-Gaussian overlap → `bProfile = 2`). **Corrections to my memory:** I had coreRadius 0.63 / coreFraction 0.758 (wrong; the paper gives 0.76 / 0.63) and ecmPow 0.03344 (the paper prints 0.03). PDF: Pythia-internal `PDF:pSet = 20` (NNPDF3.1 QCD+LUXQED NNLO, α_S = 0.118). The paper uses NNPDF3.1 NNLO without LUXQED; the effect on hadronic UE of the photon PDF is negligible (ESTIMATE). Monash = `Tune:pp = 14` (`cards/pythia8_tune_Monash.dat`). **Implementation note (VERIFIED, E4_session_log):** if the tune is given through MG's `pythia8_card.dat`, MG 2.9.22 re-orders the card and places `Tune:pp = 14` after `PDF:pSet`/`SpaceShower:alphaS*`/`TimeShower:alphaS*`, which resets them to Monash. Production therefore runs the MG5aMC_PY8_interface jobs itself with our card order (`scripts/produce.py`, `py8_card`), and the Pythia 'changed settings' table confirms the full CP5 |
| D2 | MPI on | V-MPI (MPI off) sample at 500 GeV |
| D3 | xqcut 30 / qCut 45 | DJR plots and qCut variation: (20, 30), (50, 75) separate runs; in-weight 67.5/90 |
| D4 | ME cut pT(QQ̄) > 100 GeV | `scripts/patch_ptqq_cut.py` on `mg_out/prod_{F,S}_TRG` |
| D5 | E: 200-1500 GeV in 100 GeV steps; Ẽ at 200/500/1000 only | `scripts/produce.py` TASKS |
| D6 | LO-MLM shapes normalised to the K-factor table TH §2.3; FxFx later | VALIDATION.md §1 |
| D7 | full CT18NLO set in `data/sim/lhapdf/` | downloaded 2026-10-11 from lhapdfsets.web.cern.ch (59 members; member 0 and .info byte-identical to `data/pdf/CT18NLO`); the .info is patched as before. NNPDF23_lo_as_0130_qed member 0 is downloaded from the same site, because the HEPTools tarballs are empty (0-byte) files |
| D8 | MG default (Gμ) scheme, normalised to α(M_Z) | σ ratio between schemes computed in probe t15 (VALIDATION.md §1.3); nuisance ±5 % (TH), not the LO scheme spread |
| D9/D10 | vertex at the origin; no symlink | — |
| D11 | budget ≈ 35 CPU-h, 6 parallel jobs | `nb_core = 6` |

---

## 8. Risks

1. **MLM tail physics.** Angular matching lets hard ISR be absorbed into soft ME jets. The probes show that an ME
   cut biases the tail (6 % at 150 GeV). Mitigation: 100 GeV cut + V4d closure; fall back to 80 GeV or to the
   bias module.
2. **MG weight-mode merging variations.** They exist only upward of the nominal qCut. Their consistency with
   separate runs is not guaranteed; V4b tests it. The printed merged σ carries a pb/fb label bug (cosmetic; we
   compute σ ourselves).
3. **LO + K normalisation.** The ISR-tail fraction may change at NLO (S-13: 37 % reach spread between groups,
   partly from ISR/K handling [T5 I2]). Mitigation: the merging, scale and shower bands (V4, V5, V8), and the
   optional NLO-FxFx point (D6).
4. **Toolchain fragility.**
   - The patched CT18NLO metadata is harmless for σ (probe t14) but non-standard; it is documented in
     `data/sim/README.md`.
   - HEPTools LHAPDF Python bindings are unusable, so we depend on conda-forge LHAPDF 6.5.5 for both the Fortran
     link and the systematics.
   - MG still rewrites `input/.autoupdate`.
5. **Pythia event loss** (2/1000 from job splitting). Normalising to N_LHE biases σ by 0.2 %. It is monitored per
   chunk; more chunks can push it to ≤ 0.5 %.
6. **Disk.** Transient HepMC is ≈ 80 MB per 1000 events. Chunks of ≤ 20k (≤ 1.7 GB) are converted and deleted
   immediately. The mg_out directories are ≈ 15-20 MB each (≈ 0.45 GB now, including probes).
7. **Tune parameters from memory** (CP5). They must be verified against the CMS paper before production (D1).
8. **Physics scope.** The UFO has no infracolour. N_IC enters only as a σ factor. Sommerfeld (+5-15 % [TH §2.4])
   and γγ (+4.0-4.2 % [T6]; corrected S2-R2 C-3, was +4.5-5 %) are not in the nominal samples. γγ can be checked with V-GAMGAM.
9. **Stage-3 cost is outside this stage.** `run_causal` cost grows with N_osc ∝ Λ²: 20k events × 8 Λ per mass may
   be heavy at Λ = 10 keV with material. `iter_events` lets Stage 3 take the first N events (weighted, or with
   `unweight=True`; see §5).

---

## 9. Execution order (after approval)
1. Download the CT18NLO full set (and PDF4LHC21_40 if approved D7); extract NNPDF23 LO qed from HEPTools into
   `data/sim/lhapdf/`.
2. Write `produce.py` and `merge_chunks.py`, plus the tune card per D1, `cards/run_*.dat` and `cards/pythia8_*.dat`.
3. Pilot at 500 GeV F: INC 20k + TRG 20k + LOPS 20k. Measure the real costs and run V4d/V6 on the pilot; then
   update this table.
4. Run the benchmarks (E, S) → V1-V3, V5-V7 → the fine grid → the validation samples (V4, V8).
5. Write `VALIDATION.md`, `SAMPLES.md` and the figures; append the LOG line. Then hand over for review.
