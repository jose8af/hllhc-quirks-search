# Constructive review, Stage 1 (theory track), round 1

Reviewer: constructive (Sonnet). Date 2026-10-10. Files read: NEAR_MISS_IMPULSE.md v3 (all), NUMERICS.md (§0-1, 5.3, 7-9, FU2-3), NOVELTY_AUDIT.md §4, BRIEF, synthesis S-1/S-3/§5, LOG. No code was re-run; correctness is the critical reviewer's job. Classes: A = rejection risk, B = weakens P1, fix in this track, C = style/clarity.

## Summary (15 lines)
1. As physics the result is paper-grade: an exact reduction (lab B becomes a uniform E* in the pair frame), a derived odd-crossing miss b_odd (0.1 % vs numerics), a derived log coefficient (G to 0.2 %, vacuum A-hat to 1.2 %, kappa confirmed), the NR constant 3 ln 2 - 2 (confirmed 0.0791 vs 0.0794), and thickness numbers c, B^0.91, Lambda^-1.8 that agree with blind numerics at 1 keV (about 1-2 sigma).
2. No A finding. Nothing found that makes the physics wrong or the claim unsupported. (Correctness is for the critical reviewer.)
3. 12 B findings, 8 C findings. The B items are framing, scope, unexplained discrepancies and notation, all fixable in this track at low cost.
4. Biggest framing risk: c is presented as the headline, but c = 1/(L+K) is "one over the log" and a referee will call it trivial. The strong result is the mechanism (log-enhanced coherent rotation generated only at odd crossings) and what it does to the Delta-s formula and to any simulation (B1).
5. The title promises multiple scattering and "exact string dynamics". The MS mechanism is a CONJECTURE (§6.3) and K and the accumulation are numerical or model-based (B2).
6. The observable Delta-s is never defined in the note, and the in-plane versus out-of-plane check is untested (B3).
7. The accumulation model is 10-35 % off for gamma* >~ 2 and the B* correction is not analytic; the fraction of events affected is not quoted (B4).
8. Open discrepancies a referee will find: 3 keV excess at k >= 4, Li/NG ratio at gamma* = 2 (0.50 vs 0.69), model medians 5-20 % below T3 medians, low-gamma* residual (B6).
9. The q-dependence (|q| = 2) and scalar Ẽ are not stated in the note, but both follow from the per-event law at once (B7). Angle dependence is only qualitative (B8).
10. Notation conflicts between the two notes: L, k, J, psi/eta, G/A_o, K variants, epsilon (B9). Section 0 is not readable by a phenomenologist (B10).
11. Credit: 5 of 10 audit sentences are reflected (2 more partly); the Knapen comparison (§5.2: "larger by G(L+K) = 10-15") conflicts with the audit's statement that the two are of the same order (B12).
12. Upstream cascade (T2 even-crossing erratum, synthesis X-2/S-3 wording) is proposed but not yet propagated (B13).
13. For later stages: store (gamma*, alpha, n_z, eps_perp) per event; use max_boost 1e-3 and the b_odd/l0 >= 1e-6 rule at >= 3 keV; give the tail gamma* > 1.5 its own statistics; ACTS needs a custom near-miss-aware propagator.
14. P2: c is a weak handle on Lambda (dc/c = -0.2 dlnLambda) and needs B scans a collider does not have; the useful P2 output is a theory systematic on Delta-s (from about 10-20 % to 1-4 %) and the q and L-dependence.
15. Recommended order: B1/B2 (scope), B3, B9, B10 (text), B6, B7, B8 (cheap reruns of c06/c07), B4/B13.

## 1. Completeness against the Stage-1 brief

| # | Item | Status | Where / comment |
|---|---|---|---|
| 1 | Argument of the log and its cutoffs | done (coefficient); partial (constants) | §3.4: force sigma b/(2|s| artanh beta*), lower cutoff set by the inner region |x| <~ b gamma*^2/artanh, upper cutoff ~ l_max. Constants enter only via K(gamma*), which is numerical for gamma* > 1 (§4.2, §10.1). |
| 2 | gamma* dependence | done; partial for gamma* >~ 2 | b_odd, G, K table (§4.2, §6.2). Accumulation model 10-35 % off at gamma* >~ 2 (§5.1); B* effect (−0.2 to −7 %) measured, not analytic (§9.3). |
| 3 | Crossing angle | partial | alpha (E* versus n̂ in the CM) defined in §6.3; only sin alpha enters. The lab-frame out-of-plane projection e_perp·N is qualitative ("16 % quantile ~ 0.3 x median"). No explicit formula or figure. See B8. |
| 4 | Odd versus even crossings | done | §3.1, §6.1 (J = 0 at even crossings; psi_even = (2/3 + 4/3 ln2) eps, no log; b_even second order; T2 erratum). |
| 5 | NG validity for b < 1/Lambda | partial | §7: b_odd Lambda ≈ 1.8e4 (keV/Lambda)^3, valid to about 26 keV (12 keV for small eps); below the cutoff the response is a CONJECTURE; flux-tube physics not modelled. Acceptable if said plainly (C1). |
| 6 | Closed-form or quasi-closed-form c | partial | c_ev = 1/[ln(l_max/b_odd) + K] with K numerical (fit good to 0.002). NR closed form eta_NR derived. Population c from the rotating-yo-yo model on the T3 sample, not analytic. |
| 7 | Predicted exponents | done | Lambda^(-2+2c), B^(1-c), m via ln M only (§5.4). Measured: −1.80, 0.911 +/- 0.003. |
| 8a | Validation, S_Bnonlin / R1_Blinearity (B response) | done | §5.3 table: R(1/4, 1/20, 1/80) = 1.144/1.311/1.455 versus 1.15-1.19 (S), 1.14/1.31 (R1), E2 1.147/1.320/1.460. |
| 8b | Validation, S_Bscan | partial | The only extra point (B/1000, 1.83) is at the precision floor and was dropped. No S_Bscan output file exists; numbers are from the synthesis. |
| 8c | Validation, T3 thickness tables | partial | §5.4 and §9.2 row 20: medians within 1.3 sigma of E2's M3. Model medians are 5-20 % below the T3 causal medians (31 vs 34 µm at 1 keV; 4.2 vs 4.9; 0.45 vs 0.58), explained only as "different event draws" (B6). |
| 8d | Validation, conformal solver | partial | Done for CM-field per-crossing quantities at gamma* = 1.05-3, and for Delta-s and response at 500 GeV, 1-2 keV. Not done for 3-10 keV, 200 GeV, 1 TeV scans (causal only; NUMERICS §7). |
| 9 | Explanation of discrepancies | partial | Explained: c at 3 keV (mostly step bias and round-off, FU1), K_vac NR, odd residual at high gamma* (B*), T2 even-crossing artefact, B/1000 floor. Not explained: items in B6. |
| 10 | Straight-string (Li) check | done | M5 (same response within 1-2 %), §4.4. The thickness ratio at gamma* = 2 is open. |
| 11 | q and scalar | missing | Not in the note. B7. |
| 12 | MS / single-kick connection | missing (CONJECTURE only) | §6.3. B2. |

## 2. Findings

### B findings (must fix in this track)

**B1. Lead claim is the wrong one.** c = 1/(L+K) is "one over the log", and L = ln(sigma/qB) + O(1) is already 9-10. A referee will say any B ln(1/B) has such a c. The strong, non-trivial results are: (i) the rotation is generated only at odd crossings, by b_odd from the torque law; (ii) it carries the relativistic log with retardation 1/artanh beta*; (iii) the secular rate is log-enhanced; (iv) Delta-s_B is not the Eq.III.12 formula and not linear in B or q; (v) every integrator needs near-miss control. Fix: lead with Delta-s_B = (qBR/sigma) F [ln(l_max/b_odd) + K] and present c as its logarithmic derivative; state that at the operating point B0 the log changes the absolute size (factor L+K ≈ 10), not the local B slope beyond 1-c.

**B2. The title promises more than is derived.** "Multiple scattering" rests on §6.3 (CONJECTURE) and "exact string dynamics" on a K and an accumulation model that are numerical. Fix, either (a) derive the MS part from the verified vacuum law psi = A-hat (b/l_max) ln(L/b) (constant J, rotation at both parities, coherent): predict Delta-s(delta p) for one kick and for random kicks, test against T3's single-kick test and the MS exponent 0.517 (check whether the log shifts it from 0.5); or (b) narrow the title to "plane thickness" and move MS to a companion paper. Replace "exact" with "classical Nambu-Goto".

**B3. The observable is undefined in the note.** Delta-s appears from §5 with "plane fit through the origin" as its only definition. Fix: define Delta-s (hit set, layers, fit, truth level, B only), state that the theory gives the same per-event factor for in-plane and out-of-plane rotation (§10.5, untested), and run the in/out-of-plane check with the causal code (one c06-type run).

**B4. Accuracy per gamma* bin is not stated.** The rotating-yo-yo model is 1-4 % for gamma* <~ 1.5 and 10-35 % off above 2; B* gives 4-9 % on c in the tail; the fraction of the T3 sample above 1.5 and 2 is quoted only as "about 15 % above 2" (§9.2). Fix: add a table Delta-s_model/Delta-s_causal and c versus gamma* bins with population fractions; either distribute the rotation over the half-period (§10.2) or quote "c to +/-0.5 % overall, tail +4-9 %". Give the accuracy claim in P1 per bin, not as a single number.

**B5. Solver independence is overstated.** E2's nm_kernel is a line-by-line copy of T3_causal, and c03 uses T2's CausalNullString (same Athena-type map). "Blind" is blind to E1's coefficient, not independent of the E1 code lineage. Fix: add a table of which numbers rest on two solvers (causal + conformal) and which on one (NUMERICS §7 has the content), and say "analytic derivation versus numerics, with a second solver for X". The Athena C++ standalone comparison (LOG 2026-10-08) would be the strongest third check.

**B6. Unexplained discrepancies a referee will find.** (a) c at 3 keV: the excess at k = 4, 20 (+0.005, +0.012) is attributed to round-off amplification, but no decisive test (quad precision or a controlled noise injection that reproduces the excess size) is shown; FU1b gives 0.15-0.9 % noise, an estimate. (b) Li/NG ratio at gamma* = 2: 0.50 predicted versus 0.69 measured (§4.4, §10.9). (c) Model medians 5-20 % below the T3 causal medians. (d) Low-gamma* full-event residual (+0.5 eps, "mostly numerical"). Fix: (a) a noise-injection ensemble of 1e-14 perturbations on 3-4 events, or mpmath on one event at k = 20; (b) remove the numeric claim from P1 or reproduce it with Li's lab-frame s-hat; (c) rerun c07 on exactly the T3 event list (c06 is already event-matched and gives 0.97-1.00, so this is cheap) and quote the paired ratio; (d) rerun FU3 at 1e-3 steps on more than 20 events.

**B7. |q| = 2 and scalars not stated.** The note has no q-dependence. It follows from the per-event law: eps_perp and b_odd ∝ q, so L → L − ln q and Delta-s ∝ q (L + K − ln q). For |q| = 2 this gives Delta-s(2)/Delta-s(1) = 2(1 − ln2/(L+K)) ≈ 1.86 (not 2) and c(2) = 1/(L+K−ln2) ≈ 0.112 versus 0.104; sample-level numbers need a rerun with the q = 2 kinematics (S-17 gives reach and cross-section). Scalar Ẽ: classical NG has no spin, so the same per-event law holds; only the gamma* distribution (and l_max × 1.7, N_osc × 0.81 [S-11]) changes. Scalars populate larger gamma* (beta^3 threshold), so the less accurate region (B4) weighs more. Fix: add §6.4 "charge and spin" with these formulas; rerun c06/c07 with a scalar DY sample and with q = 2 (hours). The same formula gives the audit's 7 % deviation for Li's factor-2 charge test (c ln2).

**B8. Angle dependence is only qualitative.** "Crossing angle" is read here as alpha, the angle of E* to the initial axis in the CM; the near-miss geometry itself (b/l ~ 1e-9, nearly head-on) has no free angle. Only sin alpha (eps_perp) and the out-of-plane projection e_perp·N (∝ n_z) matter, but the projection is not given as a formula in lab variables. Fix: write eps_perp and e_perp·N in terms of (theta*, phi*, beta_cm) for B ∥ z; add Delta-s/median versus n_z and versus sin alpha from c06 (the data exist). Say explicitly that the term "crossing angle" does not appear because the near-miss is head-on at 1e-9 rad.

**B9. Notation conflicts** (same quantity under different names or one symbol with two meanings). See §3 below. The JFC output rule (04-output) classes same-quantity-different-name as Category A for a final document; for P1 it must be fixed before the draft. Fix: one symbol table in P1 and a one-time rename in the two notes (or an explicit mapping table at the head of NUMERICS).

**B10. Section 0 is not readable by a phenomenologist.** It uses E*, B*, yo-yo, odd crossing, axis rotation, K, A-hat without definitions and has no physical picture. See §4.

**B12. Knapen comparison inconsistent.** §5.2 says the secular part is "larger by G(L+K) ≈ 10-15" than Knapen et al.'s torque rotation, while the audit (C2) found their estimate of the same order as the causal Delta-s_B at 2 keV, 2 T (about 10 µm versus about 5 µm). Knapen's rotation alternates and then accumulates (Fig.3), so the comparison depends on what is compared. Fix: compare Delta-s numerically at their benchmark point (2 keV, 2 T, same geometry) and state the ratio; drop "larger by 10-15" unless it survives. Also soften §5.2's "their order-of-magnitude relation misses the logarithm" (Li et al. claim only "~").

**B13. Upstream cascade not done.** The T2 erratum (even-crossing b of 16-31 Å at 1 keV are step artefacts), the replacement of the synthesis "10-30 % for Lambda >~ 10-20 keV" by 3-8 % at 30 keV, and the B* correction touch synthesis X-2/X-3/S-3/S-19 and the 48-pp report. Fix: list the sentences to change (the orchestrator edits them); keep ε-per-crossing statements marked "upper bound".

### C findings (style, clarity)
- **C1.** §7: state in one sentence the claim region (Lambda <~ 10 keV safely, <~ 26 keV typical) and that Delta-s_B is below the MS floor there anyway; mark the below-cutoff response CONJECTURE in the abstract, not only in §7.
- **C2.** Credit sentences 4, 8, 9, 10 of NOVELTY_AUDIT §4 are not in the note (Li charge-linearity, Athena/Artru/Lund causal string, KLN/Evans-Luty "check", Barbashov/Petrov-Sharov). Sentences 1, 2, 3, 5, 6 are present with locations; 7 (MS) belongs to another section. Put all ten in P1 §1/§2. Artru/Lund are "UNVERIFIED, not opened" in the note: resolve before printing.
- **C3.** NUMERICS §0 item 1 and §8.2 still say "non-relativistically L = l_max, K → 0"; §11 FU2 supersedes it (L/l_max → 8/e² = 1.082). Edit the two lines.
- **C4.** State the initial conditions: straight string, pair produced at one point (J0 = 0), no transverse string excitation, no infracolour radiation; classical (quantum numbers ~1e16).
- **C5.** §0 gives "b_odd ≈ 3.5 µm (keV/Lambda)^4" without its conditions (m = 500 GeV, 3.8 T, median of the T3 sample); add them.
- **C6.** epsilon is also T2/S-19's glueball emission probability; rename the latter or the dimensionless field (suggest eps_E for q|E*_perp|/sigma and keep eps_B = qB/sigma).
- **C7.** The note is 69 kB with an audit trail (v1-v3 remarks). For P1 split: main text (§0-§6, 12 pages), appendix A (NR matched asymptotics, K fit), appendix B (comparison tables). Drop the "v1 said" remarks.
- **C8.** Figure style for the later plotting stage: JFC 04-output (mplhep CMS style, 10x10, PDF+PNG, no ax.set_title, no raw ax.text on data, legend via mpl_magic, "Open Simulation" labels not applicable to a theory plot; use no experiment label). Also state that results depend on sigma only, i.e. are independent of N_IC and of the representation once Lambda = sqrt(sigma).

## 3. Notation conflicts between NEAR_MISS_IMPULSE.md (E1) and NUMERICS.md (E2)

| Quantity | E1 | E2 | Problem |
|---|---|---|---|
| log argument / scale | L ≡ ln(l_max/b_odd) (§5.2); also L = outer length scale in "ln(L/b)" (§3.4) | L = scale in psi = A-hat (b/l_max) ln(L/b), L/l_max = 0.985/0.90/0.56/0.43 | one symbol, three meanings. E2's ln(L/l_max) is K_vac; E1 relates K = K_vac + delta_pair/G only in §9.1 |
| crossing index k | k = 1, 2, ... (odd/even) | M3/FU: "k = 2-80" is the B0/k divisor; M1: k also crossing index | clash inside E2 |
| angular momentum J | J = total angular momentum (b p*) | ΔJ = string impulse along b, "J⁴" cumulative impulse | clash |
| rotation per crossing / period | eta (per period, absolute), psi not used | psi_k (per crossing, in units of eps), psi_pair = psi_odd + psi_even = eta/eps | same quantity, different names and normalisation |
| log coefficient per period | G(gamma*) | A_o, "a" in psi_pair/eps = a ln(1/eps) + b | same quantity |
| constants | K (field, per period), K'' (below cutoff), kappa_0 | K_vac, K_o, kappa_0, "b" | K and K_vac differ by delta_pair/G; no table with all |
| transverse relative momentum | p_rel,perp | Pi | same quantity |
| relative speed | v = 2 beta* (NR, §3.3) and v = beta* (§3.4) | v = CM speed of one end | v has two meanings in E1 |
| field strength | eps_perp, eps_B, eps_par | eps = q|E_perp|/sigma and eps_perp | eps also = glueball emission in T2/S-19 |
| b_odd normalisation | b_odd = 2 eps l0 [gamma* − asinh rho/rho] | c_b = b_odd/(eps l_max) = 1.33/1.30/1.24/1.19 | same quantity; E2's l_k ≈ l_max |
| thickness | Delta-s, Delta-s_B | Delta-s_B, "thickness" | OK, but Li's D, d differ; P1 needs one definition |
| NR vacuum constant | K_vac,NR = 3 ln2 − 2 | NUMERICS §0, §8.2: "K → 0" | stale (C3) |
| B0 and f | B0 = 3.8112 T, f = B/B0, R(f) | same | consistent |
| Lambda exponents | d ln Delta-s/d ln Lambda = −2 + 2c | n, "Lambda^−1.8" | consistent in sign |

## 4. Section 0 for a collider phenomenologist (B10)
Not readable as it stands. Missing: (i) a physical picture; (ii) definitions; (iii) why the logarithm appears; (iv) what is the observable; (v) what is new. Proposed replacement in five sentences: "A quirk pair is two heavy charged particles joined by a string of constant tension sigma = Lambda^2. Without fields they oscillate through each other along a line (a yo-yo) and the string is always straight. In the pair rest frame the detector's B field is a weak uniform electric field, which gives the pair a small angular momentum J, so the two ends miss each other by b ~ 3.5 µm at every second crossing (odd crossings). At a near-miss the string pulls the ends sideways with a force sigma b/|x|, which integrates to a logarithm ln(l_max/b); the result is a small rotation of the oscillation axis at every odd crossing, always in the same direction. These rotations add up and make the hits depart from one plane by Delta-s ∝ (qBR/sigma)[ln(l_max/b) + K], i.e. approximately Lambda^−1.8 B^0.91 and independent of m_Q." Then define E*, odd crossing, K, A-hat at first use, and give a boxed notation table.

## 5. Credit check (NOVELTY_AUDIT §4)
| Sentence | In the note? | Comment |
|---|---|---|
| 1 KLN Eq.5.64 scale | yes, §3.2 | good; "Eq.III.12 describes b" is stated as fact: add "as to its scaling" |
| 2 Li eta, Eq.A.6, A.17, V.5-6, B.9 | yes, §1.2, §5.2 | good; soften "misses the logarithm" (B12) |
| 3 log not a retardation effect, straight string has it | yes, §4.4 and §4.3; M5 confirms | caveat in audit satisfied (M5 run) |
| 4 Li charge test, 7 % | no | add with the q formula (B7) |
| 5 Knapen, m-independence | yes, §5.2 | the "10-15 x" statement conflicts with audit C2 (B12) |
| 6 Li App.C and App.A after A.13 | partly, §1.2, §3.2-3.3 | Fig.8, D_N/D_A not mentioned |
| 7 MS credit | no | belongs to MS section (B2) |
| 8 Artru, Lund, Athena | only "Athena-type"; Artru/Lund UNVERIFIED | resolve (C2) |
| 9 KLN §3.2 and Evans-Luty check | partly, §4.4 | add the sentence |
| 10 Barbashov, Petrov-Sharov | no | add |
Over-claims: "exact" (title, B2), "blind" (B5), "DERIVED" on items with numerical K (the tag legend is clear but §0 says "DERIVED: items 1-4 except K", fine). Under-claims: the NR closed form eta_NR and the retardation factor are stated modestly; the P-21 turning-point transfer (post-hoc, matches E2 to 0.3 sigma) is a nice result worth one sentence, flagged post-hoc. The honest statement that the log is elementary orbit mechanics (§4.3) is good: keep it prominent.

## 6. Draft P1 story paragraph
"We study the classical motion of a heavy charged quirk pair joined by a Nambu-Goto string (sigma = Lambda^2, Lambda ~ keV) in the uniform field of a collider solenoid. Boosting to the pair rest frame turns the lab B field into a uniform electric field E*, exactly. The field gives the pair a small angular momentum, so the ends miss each other by b ~ 3.5 µm (keV/Lambda)^4 at every odd crossing and meet head-on at every even one. At an odd crossing the string pulls the ends sideways with a force sigma b/(2|s| artanh beta*), whose integral is a logarithm ln(l_max/b): the oscillation axis turns by eta = eps_perp G(gamma*)[ln(l_max/b) + K(gamma*)] in the same sense every period, so the rotations add coherently. This is the analytic origin of the per-period rotation that Li et al. fitted numerically. It makes the plane thickness scale as Lambda^(-2+2c) B^(1-c) with c = 1/(ln(l_max/b)+K) ≈ 0.10, independent of m_Q, instead of the naive B/Lambda^2 or the miss-distance formula, which describes b, not the thickness. We verify the per-crossing laws to 0.1-1 % against independent crossing-resolved numerics (causal and conformal-gauge solvers), the thickness response to 1-2 %, and show that a converged straight-string integrator has the same logarithm. We give the regime of validity (b_odd > 1/Lambda), the dependence on gamma*, charge and spin, and the consequences for simulation: any propagator must resolve the near-miss and the B and Lambda scalings are not the ones usually assumed."

## 7. Figure list for P1 (at most 8)
Lead: F1 + F3 (mechanism and proof of the log).
| # | Content | Source | Status |
|---|---|---|---|
| F1 | Schematic: yo-yo in lab B, E* in the pair frame, world sheet as a chain of lenses, the odd-crossing near miss with b and the wedge, axis rotation eta | none | missing (draw) |
| F2 | b_odd/(eps l_max) versus gamma* (analytic curve, causal and conformal points, ratio panel) and G(gamma*) with the retardation 1/beta* comparison | M2.json, c01, c11 | data exist |
| F3 | Vacuum near-miss law: psi versus b/l_max over 4.5 decades, slopes A-hat(gamma*) NG versus KL (straight string) | M2.json M2a | data exist |
| F4 | Where the log lives: impulse profile kappa ln(tau) near the crossing versus turning-point-to-turning-point transfer without log | M2.json | data exist |
| F5 | Coherent accumulation: axis angle versus crossing index (odd steps, even smooth torque term), and event-by-event rotating yo-yo versus causal Delta-s versus gamma* | c06 outputs | partly (needs a plot) |
| F6 | Response per unit B: R(f) versus ln(1/f), prediction, E2 points, converged Li (M5), floor region shaded | M3, M5, c07 | data exist |
| F7 | Delta-s_B versus Lambda (analytic band, E2 medians), local exponent −2+2c, b_odd Lambda = 1 line, MS floor (T3) | M3, c07, T3 | data exist; MS curve from T3 |
| F8 | c versus (Lambda, m_Q) plus Delta-s/median versus n_z and sin alpha, q = 2 and scalar bands | c07, B7/B8 reruns | missing (B7, B8) |
If MS enters P1 (B2 option a), replace F4 by "single kick to rotation: Delta-s(delta p)".

## 8. What a referee asks first
| # | Objection | Answered now? |
|---|---|---|
| R1 | "The log is textbook near-radial orbit mechanics; what is new?" | Partly. §4.3 and the audit state it; the new content (odd-only, retarded coefficient, K, consequences) must be in the abstract. |
| R2 | "Could it be an integrator artefact? Same code lineage?" | Partly. Two solvers, derived coefficients, converged Li; but shared Athena-type map, and only one third-party check absent (Athena C++). B5, B6. |
| R3 | "Classical point-mass NG at micron scales: flux-tube width, quantum corrections, glueball emission" | Partly. §7 gives b_odd Lambda >> 1 up to about 26 keV; even-crossing physics and the below-cutoff response are CONJECTURE. C1. |
| R4 | "Does it matter? Above 1.5 keV the MS floor and 17 µm hit resolution dominate" | Not in Stage 1. P1 must carry the T3/S-2 comparison and say what the log changes at the operating point (absolute size ×(L+K) ≈ 10 versus naive estimate; the Eq.III.12 formula). B1, B2. |
| R5 | "Generality: LO DY sample, q = 1 fermion, 10-35 % model error in the tail, K numerical, B* not analytic" | Partly. B4, B7, B8. |

## 9. Implications for later stages and P2
**MadGraph samples (>= 200 events per point).** The per-event law c_ev depends on (gamma*, alpha, n_z, gamma_cm beta_T): store them with each event so the analytic prediction can be evaluated event by event on the same sample (paired test, no draw excuse). With a c spread of about +/-7 %, 200 events give about 0.5 % on the median, adequate. The gamma* > 1.5 tail is about 15 % of events, so it gets only about 30 events at 200: oversample it (or run it separately) to check B4. Use V+jet ISR (S-13). Use causal max_boost <= 1e-3 for Lambda >= 3 keV and report only B ratios with b_odd/l0 >= 1e-6 (k <= 80 at 1 keV, k <= 2-4 at 3 keV). Run scalar and |q| = 2 samples too (B7).

**ACTS tracker.** The string propagator is custom; ACTS supplies material, digitisation and track finding. The propagator needs adaptive stepping at odd crossings (resolution of b ~ 1e-6 l0) or the analytic rotating-yo-yo surrogate (1-4 % for gamma* <~ 1.5, causal fallback for the tail). Validate the surrogate against the causal code before using it for the efficiency maps. Per-hit out-of-plane resolution (17 µm IT, 0.25 mm PS, 8 mm 2S) and MS floor (11-22 µm) are comparable to Delta-s_B (about 30 µm at 1 keV), so the truth-level B-only theory is an input to, not a prediction of, the reconstructed thickness.

**Resolution-aware finder.** Delta-s_B only enters through its Lambda-dependence in the signal model; the finder needs the distribution of Delta-s per event (spread with n_z and gamma*), not just the median. Use F8 (angle dependence) for that. The log gives a 20 % correction to the local Lambda slope (−1.8 instead of −2), which matters for window edges.

**P2 (measuring m_Q and Lambda).** (i) Delta-s ∝ Lambda^(−2+2c) times a theory factor; with the analytic F the theory systematic on the Lambda inference can be set by the model accuracy (1-4 % for gamma* <~ 1.5) instead of "10-20 %" estimates. (ii) m_Q enters Delta-s only through ln M and the gamma* spectrum, so Delta-s is mostly a Lambda measurement; m_Q comes from kinematics, l_max and N_osc. (iii) c is a weak handle: dc/c = −2 dlnLambda/(L+K) ≈ −0.2 dlnLambda, so a 5 % measurement of c gives about 25 % on Lambda, and measuring it needs data at different B (CMS has special-field runs, not a scan). Treat it as a consistency check of the NG picture, not a measurement. (iv) q enters through q(L+K−ln q): a 7 % effect separating |q| = 1 and 2 beyond the factor 2. (v) The sign and direction of the tilt follow E* = gamma beta x B (towards E*_perp); whether this can fix the charge assignment of the two ends is a CONJECTURE worth a check.
