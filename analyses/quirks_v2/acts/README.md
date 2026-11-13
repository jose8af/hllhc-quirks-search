# theory_track/acts — Stage 4: ACTS-based CMS Phase-2-like tracker layer (public geometry only)

Goal: realistic hit-level layer for the quirk coplanarity search. Hybrid first: T3_causal trajectories intersected
with ACTS surfaces and passed through ACTS digitisation (pixel/strip segmentation, 2S without z), Fatras for SM
tracks (PU-200 overlay, prompt-track background). Custom ACTS stepper: assessed and rejected (hybrid only, user D2).
Deliverables: resolution-aware coplanarity finder χ²(n) = Σ(n·hᵢ)²/σ_n,ᵢ², signal vs background efficiency,
realistic lower window edge in Λ at fixed background efficiency.

Status 2026-10-11: feasibility check done (E5, `INSTALL_CHECK.md`); user approved route R1. Env `pixi.toml` installed
(pyacts 48.0.0 + Pythia8 8.312 + pyhepmc; 640 MB); `scripts/smoke_test.py` passes (output `scripts/smoke_test_output.txt`).
Public D111 geometry: `geometry/cms_phase2_public.json`. Physics work (finder, efficiencies) queued behind Stage-2/3 checkpoints.
Run: `cd theory_track/acts && nice pixi run python scripts/smoke_test.py`.
Geometry inputs: ../data/tdr_geometry/ (TDR CMS-TDR-014, tkLayout OT806_IT742 = CMSSW D111, beam-spot sources; see ../data/README.md).
