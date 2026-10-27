# C001: open questions for the user (Phase 1)

Date: 2026-10-07 (v3 — Phase-1 PASS, round 2). Companion to `STRATEGY_DRAFT.md` (STRAT) and `../../phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md` (SREQ).
Each question lists the options and a recommendation. Questions Q1-Q3 block Phase 2; the rest can be answered during weeks 1-4.

---

### Q1. Analysis scope (blocking)

**Options**
- **S1. CMS Phase-2 sensitivity/design study** (PU 200, trigger proposal, MTD, late-hit/BX study).
  - First result in 12-18 months (ESTIMATE).
  - Reach at Λ = 3 keV, 3 ab⁻¹, expected 95% CL: ≈ 1.2 TeV with zero background; 0.94-0.97 TeV with the μ = 50 background rate; 0.57 TeV (×16) or ≈ 0.3 TeV (×256) if PU 200 scales that rate without new handles and the background is known to 20% (STRAT §6.1). Phase 2 beats Run 2+3 only if the PU-200 background is controlled.
  - Novel vs ATLAS: PU 200, a lowered L1 MET (P2), a muon-system slow-pair seed (P5: gain at low m_Q and a β tag, **not** ISR-free), MTD, BX. It is a projection, not data.
- **S2. CMS Run-3 (+2017-18) search on data, then a Phase-2 extension.**
  - First result 2029-30 (ESTIMATE).
  - Reach at Λ = 3 keV: ≈ 0.72-0.87 TeV for Run 3 = 150-350 fb⁻¹ plus 2017-18, with and without the μ = 50 background rate.
  - Head-on race with ATLAS (expected 2028-29). Needs ~2-3 FTE for 2-3 years.
- **S3. Staged.** Common tools first, then the S1 note plus a measurement of the random-plane background in Run-3 data, then a go/no-go gate for S2 at month ~9 (gate criteria in STRAT §6.3).

**Recommendation: S3.** The critical-path tools are shared by all scopes. The PU-dependent background is the largest unknown, and only data can anchor it. Committing to the S2 race first would start about a year behind ATLAS (STRAT §6.3).

### Q2. CMS-internal landscape and convener contact (blocking)
Nobody has searched CDS/CADI; CDS was blocked by a bot challenge [EX §1.1 item 1]. A CMS-internal quirk effort may exist.

**Options**
- (a) Check CADI, CDS, McM and DAS ("quirk"; SREQ §5 block 0), then contact the EXO-LLP conveners before investing.
- (b) Proceed silently and contact them later.
- (c) Approach the ATLAS group (burzynski-lab) directly.

**Recommendation: (a), in week 1.** Option (c) is not advisable: cross-collaboration contact about an unpublished ATLAS analysis is sensitive. Cite only their public repositories, and only if needed.

### Q3. Manpower, partners and compute (blocking for S2; important for S1)
The quirk Geant4 port (W1) is 1-3 person-months for an experienced CMSSW/Geant4 developer [ST §1C]. USFQ T2/T3 access is UNVERIFIED.

**Options**
- (a) USFQ alone.
- (b) Partner with a CMS group that has SimG4 / HSCP / LLP-tracking expertise.
- (c) Request central PdmV production after a private validation.

**Recommendation: (b) + (c).** Find a SimG4 co-developer for W1. Use a group CPU allocation for exploration (≈ 24-34k core-h, ≈ 8-12.5 TB for S1 Phase 2; SREQ §2). Use central production for the full grid (≈ +53k core-h, +11-19 TB).

### Q4. Benchmarks

**Options**
- (a) E only.
- (b) E + Ẽ (scalar; spin/kinematics; σ ×1/11-1/18).
- (c) E + Ẽ + L doublet (topology test; Q^± → Q^0 π^± with cτ ≈ 7 mm, ESTIMATE).

**Recommendation: (b) for results, plus 2 L points as a topology demonstration (c-lite).** E is the common denominator of FASER, Knapen and Li et al. [TH §1.3].

### Q5. Signal grid size for Phase 2

**Options**
- (a) The full 48-point grid now (6.6×10⁵ events including edge oversampling: ≈ 46k core-h, 9.9-16.5 TB).
- (b) A 15-point exploration subset {200, 500, 1000} GeV × {0.3, 0.6, 2, 10, 30} keV (≈ 5k core-h + unknown Geant4 overhead), with the full grid in Phase 3.
- (c) The 25-point grid of ST §3.1.

**Recommendation: (b).** It spans all regime boundaries and the timing transition at ~500 GeV. The Geant4 CPU per quirk event (A7) must be measured before a large production.

### Q6. Trigger ambition (S1/S3)

**Options**
- (a) Baseline MET path only (P1/P1', ε ≈ 0.1-0.18).
- (b) Also study a lowered L1 MET (P2; +42 kHz).
- (c) Also prototype a new GMT "trackless slow straight muon" seed (P5) with L1-DPG involvement.

**Recommendation (revised after review A1): (b) as the main trigger case; (c) only as a small feasibility study.**
- The bound pair reaches the muon system with β ≳ 0.15 only when pT(QQ̄) ≳ 0.15 M_QQ̄/cosh η, i.e. ≳ 140-190 GeV at m_Q = 500 GeV. That is the same ISR recoil the MET path needs (STRAT §10.1a).
- P5 therefore gives ε ≈ 0.03-0.08 at 500 GeV and ≈ 0.01-0.04 at 800 GeV, nearly all overlapping with P2.
- It adds acceptance mainly at low mass: the union with P2 is ≈ 0.2-0.3 at m_Q ≈ 200 GeV and ≈ 0.17-0.28 at 300 GeV.
- The main Phase-2 trigger gain comes from the lowered L1 MET, P2 (ε ≈ 0.15-0.25 vs 0.10).
- P5 remains interesting as an independent pair-β tag, and its fake rate can be measured in 2024 L1DS data.

### Q7. Primary reconstruction method

**Options**
- (a) A classical plane finder + trajectory fit as primary.
- (b) A GNN/MaskFormer as primary.
- (c) Decide in Phase 3 on the common figure of merit (STRAT §9.3), with both kept.

**Recommendation: (c).** The prior expectation is (a) in the core window 0.6-15 keV and (b) at 0.3-0.6 keV and at high PU. JFC method parity requires implementing both anyway.

### Q8. Public prototype geometry

**Options**
- (a) ODD/ColliderML only (3 T, real Geant4 PU hits).
- (b) Own CMS-like parametric geometry at 3.8 T only.
- (c) Both.

**Recommendation: (c).** Use the CMS-like geometry for signal regime maps and timing. Use ODD/ColliderML for the PU-hit background and the μ = 50 closure test. Label all numbers as prototype [L2].

### Q9. Λ range of the analysis

**Options**
- (a) The coplanar window only (0.6-15 keV).
- (b) 0.3-30 keV with three reconstruction categories (low-Λ ML/trajectory; core coplanar; high-Λ straight pair).
- (c) Also ≲ 0.2 keV (HSCP-like).

**Recommendation: (b).** 0.3-0.6 keV is where FASER is weakest (57-72 GeV) [HEPData t2] and where CMS is disadvantaged vs ATLAS (3.8 T). Leaving it out would cede it. Below 0.2 keV, HSCP searches apply [D4].

### Q10. Quick-win reinterpretation
No full-Run-2/3 recast of HSCP, disappearing-track or monojet searches for quirks exists [EX §1.1 item 8].

**Options**
- (a) A CMS-internal reinterpretation of 2410.09164 (HSCP dE/dx) and 2601.20063 (L1DS HSCP) for quirks at the Λ edges (merged straight 2×MIP pairs at ≳ 20 keV; long strings at ≲ 0.3 keV).
- (b) Skip it.

**Recommendation: (a), only if (i) the CMS publication policy for members allows the chosen route and (ii) it does not delay W1.** It could give an early CMS statement on the edges. Confirm the route with the conveners.

Anchor: 2410.09164 already excludes the DY τ′ with Q = 1e, which has the E = (1,1)₋₁ quantum numbers, below **1.02 TeV (ionisation method) / 1.14 TeV (mass method)** for helical tracks [2410.09164 l.986-987, Tab. 3]. That is the Λ → 0 limit the reinterpretation would connect to. Two caveats: it is for N_IC = 1 (the N_IC = 2 equivalent is roughly +0.1 TeV higher, ESTIMATE), and it applies only for Λ ≲ 0.1 keV, where ℓ_max ≫ detector size (STRAT §13).

### Q11. Late-hit / BX open item (OI-1)
Default CMSSW Phase-2 digitisation drops OT hits more than 12.5 ns late (STRAT C8). Heavy pairs arrive late: the median BTL delay is ≈ 16 ns at 500 GeV and ≈ 33 ns at 1 TeV (pT(QQ̄) = 250 GeV; STRAT §4.2).

**Options**
- (a) Treat it as a simulation systematic only.
- (b) Also engage the tracker DPG (front-end delay scans) and the MTD DPG (BTL TOA range).
- (c) Also propose BX+1 readout for quirk-seeded events.

**Recommendation: (b) now, and (c) if Phase 2 shows a > 30% acceptance loss at m_Q ≥ 500 GeV.** The 30% threshold is a proposed decision threshold, not a cited number.

### Q12. Phase-2 MC campaign and geometry

**Options**
- (a) D110 / Phase2Spring24 (backgrounds verified to exist) [ST §1C].
- (b) The newest geometry (D126 "most up-to-date", or D128 "baseline for trigger studies") [ST §1C].

**Recommendation: match whatever background campaign DAS shows at PU 200.** Use (a) if no newer PU-200 backgrounds exist, and keep the geometry configurable.

### Q13. Publication route for S1
**Options**
- (a) A CMS FTR-type projection PAS.
- (b) A CMS Detector Performance note (trigger/BX/MTD content).
- (c) A Phase-2 L1/DAQ technical contribution (P5, BX+1).

**Recommendation: decide with the conveners after Q2.** (a) carries the physics reach; (b)/(c) carry the CMS-specific novelties and may be faster.
