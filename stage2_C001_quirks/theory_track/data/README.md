# theory_track/data — inputs the scripts need (copied from the session scratchpad on 2026-10-08)
- `pdf/CT18NLO/` — LHAPDF grid (CT18NLO member 0) used by `code/T2_kinematics.py` (env `T2_PDF` overrides).
- `cache/T2_kinematics_cache.npz` (~170 MB) — DY+ISR kinematics cache from `T2_kinematics.py`; read by
  `T3_propagator.load_cache` and many T3/T4/S/F1/R scripts (env `T2_CACHE` overrides). Regenerable.
- `athena_quirks_snapshot/` — snapshot of ATLAS Athena `Simulation/G4Extensions/Quirks` (gitlab.cern.ch/atlas/athena,
  Apache-2.0 per project; QuirkTransportation carries the Geant4 licence header) read by T2 on 2026-10-07 for the
  causal-string port and the MaxSteps finding. Reference copy only; do not redistribute without checking licences.
- `tdr_geometry/` — public CMS Phase-2 tracker geometry and beam-spot sources (re-downloaded by E5 on 2026-10-11; read by
  `../acts/geometry/build_cms_phase2_public.py` → `../acts/geometry/cms_phase2_public.json`).
  - `broken_downloads_2026-10-08/`: the original 2026-10-08 files. All were failed downloads: `idx.html` and
    `OT6xx_200_IT4025.html` are identical CERN "404 - Not found" pages; `tdr.pdf` is a 7.5 KB HTML bot-check page
    ("Making sure you're not a bot!"). T3's material/layer model could not have come from them (see
    `../acts/PROPOSED_CHANGES.md`). Kept for the record only.
  - `CMS-TDR-014_Phase2_Tracker_TDR.pdf` (+ `.txt`, `pdftotext -layout`): CMS, "The Phase-2 Upgrade of the CMS Tracker",
    CERN-LHCC-2017-009 (2017), INSPIRE 1614103, from https://inspirehep.net/files/338a99fa62dec25fcbc18d806bd7fb71
    (2026-10-11). Cite printed page numbers (e.g. Table 9.1 p.149, Table 10.1 p.236).
  - `tkLayout_OT806_IT742_D111/`: public tkLayout pages of layout OT806_IT742, from
    https://cms-tklayout.web.cern.ch/cmssw/OT806_IT742/ (2026-10-11). This is the tracker geometry exported to CMSSW as
    scenario **D111** (CMSSW_14_1_X; page generated 2024-04-08, tkLayout revision current_xml-3600-89b31835), i.e. the
    current Phase-2 layout, which supersedes the 2017 TDR numbers (IT barrel radii, TB2S L3, TEPX z). Files:
    `layout.html` (OT layers/discs, tilted rings, endcap ring radii, module-type table), `layoutpixel.html` (IT),
    `index.html`/`info.html` (configuration, simulation parameters), `DetId_modules_list.csv` / `DetId_sensors_list.csv`
    (per-module/sensor position, tilt, corners, size, spacing, thickness), `summary.root` (resolution/trigger plots; no
    material histograms).
  - `tkLayout_indexes/`: index pages of https://cms-tklayout.web.cern.ch/{cmssw,main,recent,reference}/ and the tkLayout
    documentation home (https://tklayout.web.cern.ch/), 2026-10-11.
  - `beamspot_sources/`: HL-LHC luminous region. `CMS-TDR-020_MTD_TDR.pdf/.txt` (CMS MIP Timing Detector TDR,
    CERN-LHCC-2019-003, INSPIRE 1819664; p.2: line spread ≈ 4.5 cm rms in z averaged over the fill, peak line density
    1.9 mm⁻¹ at PU 200 (Fig.1.1 p.3); p.2-3: time spread 180-200 ps rms). `CERN-2020-010_HL-LHC_TDR.pdf` (+ text of pp.1-120;
    INSPIRE 1840718; Table 2-1 p.18: β* = 0.15 m, ε_n = 2.50 µm, 7 TeV, bunch length 7.61/9.0 cm rms).
- `sim/` — Stage 2 (E4, 2026-10-11): MadGraph5_aMC + Pythia8 quirk-pair samples. `sim/lhapdf/` local LHAPDF data dir
  (full CT18NLO, NNPDF23_lo_as_0130_qed member 0; metadata-patched .info files), `sim/npz/<ID>_m<m>.npz` converted samples
  (+ `chunks/`), `sim/lhe/<ID>/` LHE with systematics weights, `sim/aux/<ID>/` banners, Pythia logs and DJR histograms,
  `sim/SAMPLES_INDEX.json` loader index. Details: `sim/README.md` here and `../sim/SAMPLES.md`. Regenerable with
  `../sim/scripts/produce.py` (~35 CPU-h). HepMC files are transient (deleted after conversion).
- `sim_stage3/` — Stage 3 (E6 plan, E7 execution, 2026-10-11): T3_causal_s3 propagation of the Stage-2 events (truth
  level). Code and documents: `../sim/stage3/` (plan.md, VALIDATION_GATE.md, code/, validation/, jobs/, results/).
  - `probes/` — E6 planning probes p0-p7 (22 MB).
  - `inputs/<spin>_m<m>_<sel>.npz` — selected Stage-2 events (`../sim/stage3/code/make_inputs.py`): TRGS, w > 0,
    pT(QQ) > 200 GeV, deterministic unweighting (seed 12345); `p2` = |eta_pair| < 4 (count in |eta| < 2.5), `p1` =
    |eta_pair| < 1; per event: provenance, merged weight ratios, momenta, recoil/jets, luminous-region vertex, tilt weights
    (`inputs_index.json`). 7.3 MB. Regenerable in about 1 min.
  - `out/<campaign>/<spin>_m<m>/L<Lambda>_<cfg>_c<chunk>.npz` — production outputs of `run_stage3.py`, one file per job
    (schema: plan §4.3; hits in mm/ns/GeV as a CSR table, per-event truth, weights, thickness observables in um; header
    with kernel version/md5, platform, hostname, numba/numpy versions, wall/CPU time). Mac share: 3989 files (3986 jobs of
    jobs/mac.json + 3 xover clones), 204 345 events, 1.0 GB, finished 2026-10-12 (29.7 h, 0 errors). Schema for Stage 4:
    `../sim/stage3/HANDOVER_STAGE4.md`.
  - `out_pc/` — the PC share (AMD 7800X3D, Windows 11), copied from the USB: 590 jobs of jobs/pc.json (every P2 job at
    Lambda >= 15 keV + 137 MV jobs) + 3 xover clones, 14 226 events, 70 MB; `_smoke/` is the PC bundle self-test (not
    indexed). Same code md5 as the Mac; kernel output bit-identical to the Mac in 224/225 overlap events
    (`../sim/stage3/results/xover.json`).
  - `STAGE3_INDEX.json` — the canonical production (E8, `../sim/stage3/scripts/merge_index.py`): every job of
    jobs/all.json exactly once, point -> chunk files (paths relative to `sim_stage3/`, machine, events, hits, md5, CPU,
    status counts) + the xover clones per machine. `canon/` — the same as relative symlinks in the plan layout (no copies).
  - `summary/events_<campaign>.npz` — per-event summary tables (truth, thickness, hit multiplicities, timing, IT pair
    separation, status) from `../sim/stage3/scripts/extract.py`; `summary/p1_model_mg.npz` — the E1 rotating-yo-yo model
    Delta_s on the MG P1 events (`p1_model_mg.py`). Regenerable in minutes.
  - `validation/` — V1-V8 run products and stdout (V2a raw per-event Delta_s, V6 rerun trees, `v2b_s31/` = 21 V2b files
    from kernel s3.1, bit-identical to s3.2); post-production (E8): `v9/` (weighted-mode input + output, V9),
    `v7_status4/status4_rerun.npz` (label-swapped reruns of the 108 status-4 events; 18 complete).
  - `fix_r1/` — Stage-3 fix pass R1 (2026-10-13): `bstar/<point>_r<row>.npz` = B*-on and B*-off Delta_s at B0 and B0/2
    for 171 P1 events at 5 keV (E 500/1000; `../sim/stage3/scripts/fix_bstar_off.py`, Stage-1 FIX2 method, 0.84 CPU-h;
    summary `../sim/stage3/results/FIX_bstar_off.json`) and the run logs. Regenerable in ≈ 0.8 CPU-h.
  - `bundle/quirks_sim/` — the verified Windows bundle (code, inputs, jobs, RUN.md, PROMPT_FOR_CLAUDE.md, env), staged
    by `../sim/stage3/code/make_bundle.py stage` and copied to the USB `/Volumes/J8A/quirks_sim` (md5-verified).
