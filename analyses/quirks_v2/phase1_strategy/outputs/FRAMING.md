# Quirks v2: framing (one page, for every agent)

Author: Agnes (Phase 1 investigator), 2026-11-13. Sources: `publication_plan/publication_plan.tex` (the plan), paper v0.4
(`stage2_C001_quirks/theory_track/paper/`, here TT/paper). Tags: VERIFIED / ESTIMATE / UNVERIFIED (transcribed), with file:line.

**Physics question.** Can a central tracker at the High-Luminosity LHC (HL-LHC: 14 TeV, 3 ab⁻¹, about 200 simultaneous
proton collisions per bunch crossing, called *pile-up 200*) find *electroweak quirks*? If so, up to which mass?
A quirk is a heavy charged particle that also carries a new confining charge ("infracolour") with no light matter
that could break the flux tube. A produced quirk-antiquirk pair therefore stays tied by a string of tension σ = Λ²,
and oscillates. For Λ ≈ 0.5–10 keV the oscillation is mm to cm in size. The pair then leaves tracker hits that are
**not helices** but lie in a **thin plane through the collision vertex** (a "ribbon").

**Model.** Benchmark E = (1,1)₋₁: a vector-like Dirac fermion, SU(2) singlet with hypercharge −1, in the fundamental
of SU(2) infracolour (N_IC = 2), pair-produced by Drell–Yan. Alternate: its scalar partner Ẽ with the same charges.
v1 grid: fermion m_Q = 200–1500 GeV (detector level: 200, 500, 1000, 1500; scalar 500), Λ = 0.45–5 keV at detector
level (8 values) and 0.45–10 keV at truth level, i.e. 40 detector points (UNVERIFIED, TT/paper/sections/05_detector_chain.tex:109-111;
04_truth_p1.tex:26-27). The v2 grid is set by the strategy.

**Signature and search idea.** The trigger is missing transverse momentum from initial-state radiation. After standard
track finding removes helical tracks, a dedicated *plane finder* looks for a ribbon: a plane through the primary vertex,
aligned with the missing-momentum direction, with repeated crossings of the same barrel layers, a narrow width and a
small out-of-plane thickness. The thickness is set by a magnetic-field effect that v0.4 derived (the *thickness law*)
and by multiple scattering in material. The detector is a Phase-2-like tracker built from public design reports and
simulated with ACTS/Fatras, with pile-up 200 overlaid and scaled to public occupancies. Selections form an ordered
*ladder* of 23 tightening cuts ("rungs", R01–R23).

**What v1 found, and why it is not a physics statement.** No working point (final selection) met the frozen
"background-free" rule. The lowest 84th-percentile background B₈₄ is 1.23×10⁶ events at R09, 7.05 decades above the
budget of 0.11 (UNVERIFIED value, decades VERIFIED by arithmetic; 07_backgrounds.tex:102-103). The fallback gives a best
expected limit of 790 times the predicted cross section (E, 200 GeV, 1.5 keV, efficiency 9/200), so nothing is excluded
(08_results_p2.tex:74-77; ratio VERIFIED as 1.25×10⁷/1.58×10⁴). From R08 on, every leading background term is a
*zero-count bound* (no simulated event passed, so the term is about 1.14/sample size). It measures the size of the
simulated samples, not the background. The pile-up extrapolation also failed its own closure test (×1.50, ×1.61) and was
patched by ×2.41 (07:44-46). So v1 showed that counting simulated events cannot prove the background is small. It did not
show that the background is large.

**What v2 must deliver.** (1) One submission-ready paper (JHEP/PRD style; structure: plan §3.2, figures: plan §3.3,
referee answers: plan §7). Its message: the plane search works on the signal side, and with a background that is
*estimated* (with closure tests and a stated width), not bounded, it reaches X GeV, beyond existing limits (all below
about 180 GeV in this Λ range). (2) A JFC analysis note. (3) A reproduction package: code, configuration, efficiency
tables and a pyhf likelihood, ready to upload to Zenodo when the user decides.

**Analysis type.** Search. Simulation only: there is no collider data, and no CMS data or tools are used. Blinding means
that no v2 signal efficiency is computed or looked at until the background estimators' closure verdicts (pass or fail
against criteria fixed in advance) are recorded. v2 is pre-registered and hashed before production. v1 stays the frozen
record in an appendix.

**Fixed user decisions (binding).**
- **Barrel only.** The endcap item S3 is dropped. The endcap gain is stated only as an outlook estimate: signal ×1.5–3.2,
  reach 866 → 1062 GeV at an assumed background B = 10 for g = 1, where g is the endcap efficiency as a fraction of the
  barrel's (ESTIMATE; plan:379, book `ch29_account.tex`:107, :197-201).
- **No cloud computing.** Use the lab cluster only (einstein head node; workers landau, maxwell, schrodinger).
- **No pile-up scans.** Results are at pile-up 200 only.
- **No CMS Open Data.** v0.4 §11 is removed.
