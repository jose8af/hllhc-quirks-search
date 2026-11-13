# Physics review of STRATEGY_brigitte_2026-11-13_17-55.md (Phase 1, quirks v2)

Reviewer: Casimir (physics reviewer, 4-bot panel), 2026-11-13 18:20.
Inputs read: `outputs/FRAMING.md`; the artifact (all 1,249 lines); digest `outputs/digests/D4_v1_record_alfred.md`
l.170-203, `D2_paper_agnes.md` l.69-71 (opened to check the per-term counts and sample needs the artifact cites).
I did not read the methodology spec or the conventions files. Arithmetic: `python3 -I` with the standard library only.
Line numbers ("l.") refer to the artifact unless another file is named.

Classification: **A** = must resolve (blocks), **B** = must fix before PASS, **C** = suggestion.

---

## Summary verdict

The strategy is careful and honest about v1. Its process design is sound: a pre-registration hashed before
production, no scale-factor patches, failures reported as failures, toys as the primary method, Poisson auxiliary
counts instead of log-normal bounds, and a signal split by hash. Most of the arithmetic I re-derived is correct
(list at the end).

The physics core still has a gap, in two linked parts, and it would decide the paper's message.
(i) The results will be quoted at rungs R09–R20. The background there is a product of conditionals, and several
of those conditionals will again be **zero counts**. In the proposed likelihood ([SD7]) a zero auxiliary count has
maximum-likelihood rate 0, so unless the expected-limit construction says otherwise, these terms drop out of the
expected limit. v1 handled them too conservatively, and this would err the other way: too optimistic.
(ii) The closure tests at R04–R07 have nearly no power to validate the 2–5-decade extrapolation to the working
rungs. For the leading single-interaction term (PV pairs) no closure test can run at all. The planned sample sizes
are two to three decades below what v0.4 itself computed would be needed.

As written, the paper could be read as "estimated, not bounded" (FRAMING l.38-39) while still resting on sample
size. I would not approve the strategy until findings A1–A5 are resolved. The B items are mostly additions that a
JHEP/PRD referee would ask for.

Counts: **A = 5, B = 12, C = 8.**

---

## Findings

### A1. Zero simulated counts in the likelihood: the expected limit is undefined and possibly optimistic by construction (§4.11, l.611-625, l.639-657)
- **Evidence.** B_{t,c} = N_t · Π_j (λ_{t,j}/M_{t,j}) with m_{t,j} ~ Pois(λ_{t,j}) and λ = γ an *unconstrained*
  normalisation factor (l.611-623). For m = 0 the auxiliary likelihood e^(−λ) has its maximum at λ = 0. So any term
  with one zero factor has an MLE background of 0. The text calls this "an ordinary observation" (l.618) and never
  says which λ generates the background-only Asimov dataset or the toys. If the nominal is m/M = 0, then Pois(0) is
  always 0: those terms contribute nothing to the median expected limit, and "toys fluctuate the simulated counts too"
  (l.625) fluctuates nothing. The self-consistency test T1-g (l.654-657) compares toys with toys from the same
  generating hypothesis, so it cannot detect this. The problem matters because at the working rungs zero factors are
  expected, not exceptional (A4: PV pairs, SM hard scatter, loopers, NI).
- **Why a referee cares.** v1 was criticised for zero-count bounds that were too conservative (1.14/M with
  σ_ln = 1). If the same zeros silently go to zero, the error has the opposite sign, and the paper's reach would then
  reflect the treatment rather than the physics.
- **Fixed looks like.** (1) State the generating hypothesis for Asimov data and toys for every auxiliary count with
  m = 0. Options: the Bayesian posterior mean (m+1)/M with a flat prior, the 68 % upper value 1.14/M, or a
  frequentist construction that profiles λ inside every toy *and* draws the true λ from its allowed range. Justify
  the choice. (2) Add a **coverage test with non-zero truth**: generate pseudo-experiments with true λ = 0.5, 1.14, 2,
  3 (all compatible with observing m = 0 at 61–5 %), and show that the quoted median expected limit and its band
  hold, or quantify how far they move. (3) Report, at the chosen selection, the fraction of B₈₄ carried by factors
  with m = 0. If it exceeds 50 %, the paper must say the result is still sample-size limited.

### A2. The extrapolation from the closure rungs (R04–R07) to the working rungs carries no guaranteed uncertainty (§4.0 l.213-221; B1-b l.377-380; B2-c l.441; T1 l.626-627)
- **Evidence.** Closure is required only where N ≥ 20 (l.215), in practice R05–R06, plus R07 for γ and pile-up
  (see A5). The closure nuisance s_model is capped at ln F (l.217), i.e. at most 0.41 or 0.69 *whatever the distance
  of extrapolation*. An extrapolation term is added only if the trend slope is significant at 2σ (l.377-378). My
  estimate of that test's power (script in the log): with the expected DIF closure counts in 6,000 events
  (≈ 970 / 24 / 12 at R05 / R06 / R07, scaled from D4 l.196: 81, 2, 1 per 500), the statistical error on the slope is
  about 0.11 per rung. Including s_model = 0.69 per point it is about 0.5 per rung. A real slope of 0.22 per rung
  (stat only), or up to 1 per rung (with s_model), therefore passes. Over the 2–13 rungs between R07 and the
  candidate selections (R09…R20, l.668), v1's own slope of −0.36 per rung (l.379) is a factor e^(0.36·k) =
  2.1 (k = 2), 12 (k = 7), 108 (k = 13). A trend of that size would pass B1-b on these statistics. The B2-b comparison
  of the two pile-up estimators at deep rungs is the only deep-rung handle, and it is weak (B1).
- **Fixed looks like.** (1) An extrapolation uncertainty that is *always* added and grows with distance, e.g.
  σ_extr = σ_slope × (r_sel − r_last closed), where σ_slope includes s_model. It is not conditional on the slope
  being significant. (2) A held-out test of the extrapolation itself: derive (or tune) on R04–R05 and test blind at
  R06–R07, with the same F, so that the closure measures extrapolation error and not interpolation. (3) In T2, make
  the distance of extrapolation visible: tabulate, per candidate selection, the last closed rung of every leading
  term and the resulting σ_extr.

### A3. The P_geo × C_PU closure is close to tautological as specified, and has a conditioning hole (§4.4 l.357-362, B1-a l.373-376; same structure in B3 l.488-491 and B4-c l.538-540)
- **Evidence.** C_PU is "the ratio of the pass probability with pile-up overlaid to that without … at rungs where
  both have counts" (l.359-360). B1-a then tests P_geo × C_PU against the direct pile-up count "at each of R05, R06,
  R07" (l.374-375), and those are the same rungs. Overlay samples (no-PU topology + independent PU) and "full
  pile-up samples of that topology" are the same physical construction. At a rung where C_PU was measured,
  P_geo(r) · P_ov(r)/P_noPU,ov(r) ≈ P_direct(r) by definition, up to statistics. The test therefore checks the
  arithmetic, not the factorisation that is used at the working rungs. Second, only no-PU events *passing a loose
  rung* are overlaid (l.360). Candidates that fail the loose rung without pile-up but are *promoted* by pile-up hits
  (extra crossings that raise N_IP2) are outside C_PU by construction. At loose rungs that promotion is small (v1
  f_pre = 0.95 for DIF, D4 l.392, i.e. 5 % promoted). Nothing shows it stays small where the per-layer crossing cuts
  tighten. B3 (l.488-491) and B4-c have the same structure.
- **Fixed looks like.** State the rung (or rung range) where each C_PU and each conditional is derived and a
  *disjoint* range where it is tested, with disjoint samples. Measure the promoted fraction as a function of rung
  (overlay a random subset of loose-rung *failers* as well) and add it as a term, or show it is bounded. Label any
  remaining same-rung comparison as a consistency check, not validation.

### A4. The sample-size floor at the working rungs is not computed; the planned samples are 2–3 decades below v0.4's own requirement (§4.4 l.392-396; §4.7 l.506-507, l.543-545)
- **Evidence.** The artifact computes the P_geo floor only for DIF: zero in 10⁷ gives about 8 events (l.395-396;
  I get 1.14×10⁻⁷ × 4.0848×10⁷ × 1.5945 = 7.4, consistent). It does not do the same for the term with the largest
  rate, PV pairs, at 30.31 per triggered event (l.255; D4 l.395). There the same 10⁷ events give 1.14×10⁻⁷ ×
  1.238×10⁹ = **141 events**. For the SM hard scatter with 10⁶ no-PU events per process (l.506), the floor summed
  over processes is 1.14×10⁻⁶ × N_trig = **47 events**, of which Z(νν) alone is 29. These are numbers *before*
  conditionals. Any conditional measured on zero passers adds nothing. v0.4 itself states that 2.8×10⁹ (PV pairs),
  2.2×10⁹ (DIF) and 8.4×10⁸ (Z(νν)) events are needed to reach 0.11 (D2 l.71). The v2 plan is 10⁷ and 10⁶. With
  B ≈ 50–200 events of zero-count origin, the result is again a sample-size statement, only 4 decades lower than v1,
  and the T2 "background-free flag" cannot be met. Combined with A1, either such terms dominate the limit (honest,
  but not "estimated") or they vanish from it (not honest).
- **Fixed looks like.** A table, per term and per candidate selection, of the projected floor from the planned
  sample sizes (with v1 conditionals where they exist), set against the signal yields that matter (v1 placeholder at
  the reach masses). Then either (a) resize or bias the generation of the dominant terms (PV pairs need importance
  sampling in the opening angle and pT, as §4.4 point 4 does for B1, and a no-PU cost of 11.5 ms makes 10⁸–10⁹
  feasible only with such biasing), or (b) restate the expected paper message at Gate A as "bounded at the
  X-event level for terms T…". The user should see this before approving.

### A5. Leading terms with no testable closure have no defined verdict, so they can be eligible by default (§4.4 B1-a l.373-376, l.392-394; §4.12 [SD8] l.678-679)
- **Evidence.** Expected direct counts in the planned closure samples, scaled from v1 (D4 l.196-201): PV pairs, 6,000
  events → ≈ 12 at R04 and 0 at R05+ (v1 0/24 at R06); loopers 0; NI (1,000 events) ≈ 0 at R06; V⁰ (1,000 events)
  ≈ 12 at R06; Z(νν) at R07 0/81 in v1. B1-a applies "where the direct count is ≥ 20" (l.375). It does not say what
  happens when no rung qualifies. B3 defines "not testable" (l.491-492), B1-a and B4-c do not. [SD8] makes a
  selection eligible if "every closure criterion that applies to its leading terms has the verdict PASS" (l.678).
  A criterion that never applies is vacuously satisfied. PV pairs are the term with the largest floor (A4).
- **Fixed looks like.** Define "NOT TESTED" as a verdict distinct from PASS for every criterion. A selection whose
  leading term is NOT TESTED is not eligible, or is eligible only with an extrapolation width fixed in advance
  (≥ the A2 rule from the nearest closed rung) and a flag in the ladder figure. Size the PV-pair closure sample (or
  bias it) so that at least R05–R06 can be tested.

### B1. Thinning ρ = 2 → 1 gives no statistical reach beyond the direct ρ = 1 count, so B2-b rests on the occupancy model alone (§4.5 l.433-452, B2-b l.439-440)
- **Evidence.** ρ = 2: 3,000 events × 2 trials = 6,000 trials. The direct ρ = 1 sample is 96,000 trials. With the v1
  per-trial rates at R06 (0.389 at ρ = 2, 0.247 at ρ = 1, D4 l.188-189), expected counts are 2,334 against 23,712. At
  R07 I estimate about 7 (thinning) against 70 (direct). Where the direct count is already zero (R08+), thinning has
  ten times less exposure and will also be zero. B2-b ("the two estimators agree at every deeper rung", l.439) can
  therefore not be evaluated beyond R07. The fail branches (l.442-445) do not cover "B2-b not evaluable because
  thinning has no counts", although it is the expected outcome.
- **Fixed looks like.** Either give thinning a reach advantage (higher density, ρ = 3–4, where fake rates grow
  steeply, with exact thinning weights; or many more ρ = 2 trials), or state at Gate A that the deep pile-up term is
  a one-estimator extrapolation (occupancy model) and give it the A2 extrapolation width. Add the "not evaluable"
  branch with its consequence for [SD8].

### B2. Background list incomplete: secondaries from pile-up vertices, noise hits, out-of-time hits (§2, Table 2.1 l.107-120)
- **Evidence.** The single-interaction terms are per *triggered* (hard-scatter) event (l.101, l.362). Decays,
  conversions and especially **nuclear interactions of pile-up particles** (about 200 vertices per crossing) are in
  neither B1 (hard event only) nor the pile-up overlay, because Fatras has no hadronic interactions (l.386-388). PU
  vertices lie on the beam line, so a plane through the PV that is close to containing the beam axis also contains
  them. Also absent: random **noise hits** (Phase-2 pixel/strip noise occupancy), **out-of-time pile-up** hits and
  low-pT loopers from neighbouring crossings, δ-ray secondary hits, and merged clusters. All of these add hits that
  are uncorrelated with helices and feed the combinatorial term. The time-tag credit (B7) also depends on them.
- **Fixed looks like.** Add the terms to Table 2.1 with a class and an order-of-magnitude estimate: PU-vertex
  secondaries as a rate × geometric acceptance from the Geant4 setup of B1 run on minimum-bias spectra; noise and
  out-of-time occupancy from a public Phase-2 source (a retrieval task). Then either include them in the overlay or
  show they are below 10 % of the term they would join.

### B3. Closure χ² ignores the correlations between nested rungs and the common s_model (§4.0 l.215-218)
- **Evidence.** Condition (b) is a χ² "of the ln r values against zero, with variance s_P² + 1/N + s_model²" (l.216).
  This is diagonal. The rungs are cumulative (R07 ⊂ R06 ⊂ R05), so the counts are positively correlated, and s_model
  is one parameter per estimator, i.e. fully correlated across rungs. The diagonal χ² rewards a coherent bias:
  four rungs each at ln r = s_model give χ² = 4 for 4 dof, p = 0.41. It also mis-weights a trend.
- **Fixed looks like.** Build the full covariance: bootstrap the nested counts jointly, and add s_model² to all
  matrix elements. Then report the χ² and p with it. Or test the coherent shift and the trend as two separate
  one-dof statistics.

### B4. Signal-side detector response: MET, trigger, calorimeter/muon system and timing acceptance are not modelled consistently with the backgrounds (§1 l.64-66; §4.7 l.514-531; §4.14(d) l.766-772)
- **Evidence.** The reconstruction-level MET model is defined for the backgrounds (l.518-526). For the signal the
  text keeps the generator cut pT(QQ̄) > 200 GeV, the offline MET > 250 GeV and A from generator quantities (l.64-65,
  l.710-711). It never says the signal MET goes through the same jet response, soft term and lepton treatment. With
  the non-Gaussian tails that B4 introduces, events with pT(QQ̄) < 200 GeV can migrate above 250 GeV on a steeply
  falling spectrum, and the 200 GeV generator cut removes them by construction. The quirk pair's behaviour beyond the
  tracker is not discussed: ionisation deposits in the calorimeters, possible reconstruction as (standalone) muons in
  the muon system, and therefore the lepton veto efficiency and the particle-flow MET. A referee will ask whether a
  quirk pair is vetoed as a muon. Finally, slow pairs (high mass) arrive late. Late hits are the SR-T category (l.70),
  but the tracker's own in-time readout acceptance for late quirk hits is not modelled.
- **Fixed looks like.** The signal passes the same MET_reco model, with the nuisance correlated between signal and
  background. Lower the generator cut (e.g. 150 GeV) on a validation sample to measure the migration. State the
  assumption for calorimeter, muon system and lepton veto, with a number for the veto efficiency or a limitation
  label. Apply a hit-time acceptance window for tracker hits from a public Phase-2 readout description, at least as a
  systematic at the highest mass.

### B5. Infracolour corrections to the production cross section are missing (§4.14(a) l.734-754, [SD11])
- **Evidence.** The K-factor is pure QCD on the initial state. The pair is produced in an infracolour singlet and
  feels the attractive IC Coulomb potential (C_F = 3/4 for SU(2)) at production, the analogue of the threshold
  correction in e⁺e⁻ → QQ̄. One-loop running of pure SU(2) (b₀ = 22/3) from Λ = 0.45–5 keV gives
  α_IC(m_Q = 200–1500 GeV) ≈ 0.041–0.049 (my computation). The O(α) correction C_F α (π/(2β) − 4/π) is then +3 % at
  β = 0.7, +6 % at β = 0.5 and +13 % at β = 0.3, and the resummed Sommerfeld factor is 1.07–1.20 over the same range.
  Heavy masses are dominated by small β. The effect is comparable to or larger than the QCD scale envelope quoted
  (+1.6/−1.1 %, l.737), it depends on mass, and it is absent from both σ_norm and its uncertainty.
- **Fixed looks like.** Compute the IC correction (O(α_IC) at least, with the β distribution of the generated
  events) per mass, cite the treatment in the quirk literature (a retrieval task), and either apply it or carry it as
  a mass-dependent one-sided theory uncertainty on the theory line. State the Λ dependence of α_IC used.

### B6. The K-factor validation tolerances are too loose to detect plausible model errors (§4.14(a) validations 2, 3, l.742-750)
- **Evidence.** Validation 2 accepts agreement within 10 % against NLO+NLL slepton tables, and validation 3 within
  5 % against SM Drell–Yan at the same invariant mass. The NLL resummation effect for sleptons at 200–1000 GeV is a
  few per cent, so 10 % passes a model error of about 5–8 %. At equal dσ/dM, the QCD K of a colour-singlet pair is
  spin independent, so validation 3 should agree to about the integration error (≈ 1 %) once the invariant-mass
  spectra are matched. A 5 % window is three to five times the quoted envelope. Both tests can pass with errors
  larger than the uncertainty that is then assigned.
- **Fixed looks like.** Validation 3 compares K(M) differentially in invariant-mass bins, with a 2 % (or 3σ of the
  integration error) criterion. Validation 2 compares against NLO-only numbers where available (e.g. a public NLO
  code run as a cross-check), with a criterion of ≲ 3 %, or the NLL/NLO ratio is subtracted explicitly using the
  tables' own NLO column if one is given.

### B7. The time-tag credit for prompt backgrounds needs modelling of the timing tails (§4.6 point 3, l.486-487; §12.1 l.1197-1199)
- **Evidence.** The artifact itself says the credit "can move the SR-T background by orders of magnitude"
  (l.1198-1199). The probability that a prompt candidate has a late BTL hit at the 10⁻²–10⁻⁴ level is set by tails:
  the luminous-region time spread (≈ 0.2 ns), non-Gaussian resolution tails, out-of-time pile-up, slow protons and
  kaons, and noise (B2). The only timing input is one Gaussian resolution, retrieval task R-7 (l.926; v1 35 ps). A
  Gaussian 35 ps model will overstate the rejection by orders of magnitude if the true tail fraction is about 1 %.
- **Fixed looks like.** The timing model includes the beam-spot time spread and a non-Gaussian tail fraction from a
  public BTL performance source. The credit is then capped at that tail fraction, or the tail is a nuisance, and the
  B3 closure for the time-tag conditional is required with at least one rung of counts.

### B8. Detector-variation sizes are round numbers that enter the likelihood at their full measured effect (§4.9 l.577-587; §4.4 B1-c l.381-383, risk (1) l.404-405)
- **Evidence.** Hit resolution ×1.5, inefficiency 99 → 97 %, material ×0.5 and ×2, "a C/Si/Cu mixture", and the
  B1-c "material band (×0.5–×2)". None is sourced. Yet "the measured shift enters the likelihood at its measured
  size" (l.587). A ×2 material variation of an NI- or scattering-dominated term is then an arbitrary nuisance that
  can dominate. This is the "arbitrary conservative inflation" pattern that §5.1 l.847 itself forbids.
- **Fixed looks like.** Either source each variation from a public Phase-2 material budget, resolution or
  inefficiency statement (retrieval tasks) and use that size in the likelihood, or keep the round-number variations
  as robustness tests (reported, classified robust or not robust) and not as nuisances.

### B9. [DP2] removes exactly the signal points most sensitive to the detector variations (§4.9 l.590-593)
- **Evidence.** The reduced B6 drops 5 keV, 1,000–1,500 GeV and the scalar. Above 1.2–1.9 keV the ribbon thickness
  is scattering-dominated (l.784, D5 §7.13), so the material variation acts most strongly at 5 keV. The heaviest
  masses are the slowest pairs and carry the largest late-hit and material effects. The points that set the mass
  reach would then have no measured detector systematic, and no extrapolation rule is given.
- **Fixed looks like.** Keep at least 5 keV and one high-mass point (E 1000 or E 1500) in the reduced set, dropping
  instead an intermediate Λ that the others bracket. Declare how the measured shifts are interpolated to unmeasured
  points.

### B10. The selection rule picks the minimum background without splitting the background samples (§4.12 l.677-701)
- **Evidence.** The signal is split into optimisation and evaluation halves (l.692-697), but the background inputs
  are not split. Choosing among 16 selections the one with the lowest G, where G depends on background estimates made
  from small or zero counts, selects downward fluctuations of the background estimate. T2-c measures the bias only on
  the signal side (l.700-701).
- **Fixed looks like.** Quantify the background-side bias by repeating the choice on bootstrap replicas of the
  background inputs, and report how often the same selection wins and the shift of its B. Or reserve independent
  background samples (or seeds) for the final evaluation of the chosen selection's B.

### B11. The MET-model validations do not validate against physics (§4.7 validations (a)–(c), l.527-531)
- **Evidence.** (a) compares the new reco-MET model with v1's truth MET plus 25 GeV smearing, which itself has no
  source. Agreement within 10 % shows only that the two toy models agree. (c) accepts a factor 3 against a published
  monojet analysis taken under different conditions (√s and pile-up). Multijet fake MET at ⟨μ⟩ = 200 is driven by
  the pile-up soft term, which (c) cannot test.
- **Fixed looks like.** Validate the model's MET resolution as a function of ΣE_T or ⟨μ⟩ and its tail fraction
  against a published Phase-2 PU-200 MET performance figure (part of R-3). Drop (a) as a validation, keeping it as a
  continuity check with v1. State in (c) the pile-up conditions of the reference.

### B12. Dropping dE/dx gives up a primary discriminant without quantifying the loss (§4.12 [SD9], l.672-675)
- **Evidence.** Heavy, slow quirk constituents are highly ionising: this is the standard handle against minimum
  ionising backgrounds, and v1 had three dE/dx rungs. The physics reason given, that the "pixel charge tail … not
  modelled by the Gaussian digitisation", can be repaired. The Geant4 setup of B1 provides energy deposits, and a
  Landau/Bichsel straggling model is standard. A competing group would use dE/dx. Unlike the MVA ([DP3]), no measure
  of the sensitivity forgone is planned.
- **Fixed looks like.** Either model the charge deposit with straggling and keep one dE/dx candidate (with its own
  closure), or report ε(R_k + dE/dx)/ε(R_k) on the evaluation half at a directly counted background, as for the BDT,
  so that the paper states what was left on the table.

### C1. The MVA infeasibility argument is partly wrong (§3.2 l.160-174)
"None of them applies to an arbitrary score" (l.162-163) is not true for exact thinning, which acts on hits and
re-runs everything downstream, or for P_geo (a pass probability of any selection). It is true for the occupancy
model and the conditionals. The training-statistics argument (l.164-166) holds by itself. Also, l.170 sets the BDT
working point at equal *pile-up* rate, while Table 3.2 (l.153) says equal *directly counted background*. At R07 the
leading terms are not pile-up (l.123-124). Use the total counted background.

### C2. Make T1-c and T1-g test something (§4.11 l.650-657)
"Within 20 % of the injected value" at injection 0 is meaningless: use an absolute criterion in units of the fit
error. T1-g passes by construction if the quoted median comes from the same toys. State that the median is from
Asimov/asymptotics and the 500 toys are independent, and add the non-zero-truth version of A1.

### C3. Asymptotic ranking in a regime where asymptotic/toy ratios span 0.32–1.07 (l.640-642, l.685-686)
A spread of a factor 3 between selections can misrank them. Re-evaluate all eligible selections with toys at the
20 window points (about 29 CPU-h each at the quoted unit cost), or at least the top five.

### C4. PDF set for the signal normalisation (l.751)
PDF4LHC21 is the usual recommendation for BSM cross sections. Quote CT18NLO as a variant, or justify it as the
nominal.

### C5. FxFx at a single mass (l.760-762)
The ISR tail shape changes with m_Q. Add one FxFx point at E 1500, the reach-setting mass.

### C6. Comparison with Knapen et al. (§6.2 l.898, l.907)
v1's total f·A·ε ≈ 0.005 against ≤ 0.021 for R1 is a factor of about 4. The paper needs a like-for-like breakdown
(ε_trig, ε_fid, ε_reco against R1's Table I), as v2 numbers, to show where the difference comes from. Label the
300 fb⁻¹ curves as "PU-200 detector, scaled luminosity".

### C7. B7 criterion and non-collision list (l.603-604)
"Below 10 % of the smallest term" depends on the smallest term in an arbitrary way. Use 10 % of the total B or of
its 1σ uncertainty. Add beam-gas and satellite bunches as one line with a public rate, or an argument.

### C8. Literature completeness (§6)
Before the paper, run a dedicated retrieval for any ATLAS or CMS search for non-helical or quirk tracks, and for
recent HL-LHC quirk projections (2020–2026), and log it. A referee will check, and the claim "beyond existing
limits" (FRAMING l.38-40) depends on it.

---

## Items checked and found correct (with evidence)

- Signal-yield substitution (l.94): 219.2 × 0.04764 × 3000 × 0.5035 = 15,773.7, and 1.2458×10⁷/15,775 = 789.7. Verified.
- v1 deficit of 7.05 decades (l.30-31): log₁₀(1.2346×10⁶/0.11) = 7.05. Verified.
- Power of V4-5 (l.320): P(≥ 48/50) = 0.014 / 0.112 / 0.922 at p = 0.85 / 0.90 / 0.98. Verified; the statement
  "rejects agreement below 85–90 % and no better" is honest.
- B2 statistics at R07 (l.447-448): 96,000 × 7.29×10⁻⁴ = 70.0 counts, σ_ln = 0.120, ln 1.5/0.12 = 3.4σ. Verified.
- Trigger substitution (l.768): 0.98 × ½[1 + erf(50/(20√2))] = 0.974. Verified.
- DIF P_geo floor "about 8 events" (l.395-396): 7.4 events. Verified. The same check exposes A4 for PV pairs.
- [DP1] precision loss √(38,000/10,500) = 1.90 (l.571). Verified.
- T1-g binomial error √(0.25/500) = 2.2 % (l.657). Verified.
- Z(νν) closure counts at R06: 81 raw candidates per 2,000 events in v1 (D4 l.191) gives ≈ 400 in 10,000 (l.539-540). Verified.
- The C1 comparison design (Bonferroni over 41, global χ²₄₁, family coherence, stated power, l.266-280) is sound.
  It is the best part of the statistical plan.
- The signal split by event hash, independent of Λ (l.692-694), correctly keeps one physical event in the same half
  at all eight Λ.
- The quirk kinematics are self-consistent: the amplitude ~ m/Λ² = 200 GeV/(10⁻⁶ GeV)² ≈ 4 cm at 1 keV, matching the
  "mm to cm" signature (l.57-58).

## Overall judgment

**Not approved in the present form (5 A, 12 B, 8 C).** The plan is well organised, and v1's procedural failures
(post-hoc patches, unfrozen code, proxies) are addressed. The physical background estimate at the working rungs is
not yet secured. The core of a fix is short to write: a zero-count convention and coverage test for the likelihood
(A1), a mandatory distance-dependent extrapolation width with a held-out-rung test (A2), disjoint derive/test rungs
for every factorised estimator (A3), a projected-floor table with resized or biased samples for PV pairs and the SM
hard scatter (A4), and a NOT TESTED verdict (A5). Compute may grow by the biasing work in A4. If after A4 the floor
stays at tens of events, the user should be told at Gate A that the paper's message will be "bounded at the
tens-of-events level, with an estimated pile-up term", not "estimated". The signal-side additions (B4, B5) and the
missing backgrounds (B2) are what a JHEP/PRD referee would raise first after the background question.
