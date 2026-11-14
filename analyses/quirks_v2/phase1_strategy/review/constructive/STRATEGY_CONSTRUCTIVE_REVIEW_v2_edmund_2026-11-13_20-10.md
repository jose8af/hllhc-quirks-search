# Constructive review, cycle 2: Phase 1 STRATEGY v2 (quirks v2)

Reviewer: Edmund (constructive, fresh to the panel), 2026-11-13 20:10. Role file `agents/constructive_reviewer.md`. I
followed its prompt template in full, including the honest-framing check.
Artifact: `phase1_strategy/outputs/STRATEGY_dmitri_2026-11-13_19-25.md` ("STR", 2,391 lines). I read it in full in six
consecutive chunks. I also read `COMMITMENTS.md` ("COM") in full.
Also read: the cycle-1 constructive review (Cosima), the arbiter verdict (Dagmar, M1–M35 and §5), the fix report (Dmitri),
`AGENT_RULES.md`, the study and phase `CLAUDE.md`, the brief §3 (D1–D10), PLAN l.100–131, l.192–236 and l.494–545, and
`ORCHESTRATOR_STATE.md` l.20 (cap of 3 concurrent subagents).
I ran `src/strategy_budget.py` ("script [n]"; standard library, about 1 s). My own arithmetic is in two standard-library
scratch scripts (`edmund_calc.py`, `edmund_calc2.py`), quoted as **[R: calc]**. One check against the script: a one-bin
zero-count term at κ = 35 gives a median limit of 27.7, against 27.8 in script [10].
No RAG corpus exists (deviation V8). No sub-agents were spawned (AGENT_RULES). No git commands were run.
Tags: [V] means I re-derived the number or read it at the line cited; [E] means an estimate with its arithmetic.
Classification follows JFC 06 §6.1: **A** blocks, **B** must be fixed before PASS, **C** is a suggestion.

---

## 0. Summary

v2 is a real improvement. The zero-count likelihood is now specified, derived and tested against analytic limits
(§4.11). The closure battery has disjoint derivation and test sets, a precision rule and a family-wise rule. The floor
table tells the user plainly that the expected paper is "middle in size, bounded in kind" (§0, §4.4). Every cycle-1
constructive A and B item has a v2 location. Fourteen of the 17 are resolved, three are partly resolved and none is
left unresolved.

Three things still need fixing before the strategy is approvable, and one of them is a genuine error:

1. **[N-A1] The pre-registered reading of the central target is met by construction in the expected outcome.** TG-1
   says "target met" if the total σ_ln ≤ 1. When every leading term is a zero-count bound, that width is 0.41: a sum of
   20 independent exponential bounds averages out. The paper would therefore declare the plan's central target met
   exactly when nothing was estimated. The fix is one sentence.
2. **[N-B1] The headline (45 events, 495–662 GeV) leaves out the term that will probably set it.** PV pairs are
   expected NOT TESTED, so they enter at the ceiling H = P_geo + Σ f_k. That ceiling includes events missing up to half
   the required layers, so it is likely to have counts. Each counted event is 16 events in 3 ab⁻¹. At m_H = 3 or 10 the
   reach drops to about 560 or below 495 GeV [R: calc]. In the other direction, if H is also empty, the true bounded
   reach is about 700 GeV, not 495–662 GeV.
3. **[N-B3, with N-B2] The extrapolation convention for untested cut families is not a measurement**, and its numbers
   are understated by STR's own rule. It can be replaced, at no CPU cost, by "crossing" test rungs: each deep family's
   cut applied on top of the R05/R06 width, where the direct sample has 10⁴–10⁶ candidates. This takes the pile-up width
   at R11–R14 from 1.3–2.5 to about 0.5 [R: calc].

On proportion: the 44 non-production days are mostly real. Phase 2 and Phase 5 can be compressed by about 5 days
(§2.6). Phase 3, however, assumes six parallel development channels while the cap is three (N-B6), which is +9 days
unless the Phase-3 load is trimmed. Low-value lines can be removed or staged without touching any
MUST criterion (§2.5: about 460 CPU-h). Spent instead on the no-pile-up pool, the same CPU raises the bounded-outcome reach by about
50–80 GeV EST. The Gate-A package can be cut from ten questions to five decisions plus five defaults (Part 3).

**Counts.** Re-review: 14 RESOLVED, 3 PARTIALLY, 0 NOT RESOLVED; two of these carry a Gate-A deferral (B-1 → GA-3,
B-5 credit → GA-9). New findings: **A = 1, B = 7, C = 11.**

---

## Part 1. Re-review of the cycle-1 constructive findings (Cosima → arbiter mapping)

| cycle-1 id (merged) | topic | status | v2 location | my check |
|---|---|---|---|---|
| A-1 (M1) | zero counts in the expected limit | **RESOLVED** | §4.11 points 1–4 (l.1097–1220); T1-c (l.1240–1252); T2-e (l.1340–1346) | The generation hypothesis is stated: λ ~ Gamma(m + 1), with the auxiliary observations fixed. The derivation (integration by parts, l.1150–1153) is correct. The m = 0 quantiles 0.174 / 0.693 / 1.139 / 1.833 / 2.996 = −ln(0.84, 0.5, 0.32, 0.16, 0.05) are [V]. I re-derived the one-bin κ = 35 median of 27.7 independently. The coverage table (0.945–1.000) is stated honestly with its dip. The limiting-case tests (i)/(ii) would catch the λ̂ = 0 failure. Nothing more is needed. |
| B-1 (M6) | central target: definition, floors, allocation, enrichment | **PARTIALLY**; reachability **DEFERRED TO GATE A (GA-3)** | §0 (l.38–51); §4.4 Table 4.4a (l.606–650); §4.11 point 3 (l.1179–1193); COM TG-1; GA-3 | Done well: the definitions, a √(N/c) allocation (I reproduce the summed 68 % floor 45.3 and the 86.2 / 22.7 of the other pools from script [9]), the pilot, and the honest statement "middle, bounded". **Not done:** (i) the reading of the target is satisfied by construction in the bounded case (N-A1); (ii) the projection uses P_geo floors, while the expected verdict for the largest term sends it to H (N-B1). The target is now defined, and it is honestly shown unreachable at G = 1. The *measured* projection is still missing. |
| B-2 (M15) | size and power of the closure battery; "rejects a correct analysis half the time" | **RESOLVED** (for r = 1) | §4.0 points 2–5 (l.280–322); script [11] | Recomputed: for K = 12 the per-test false-fail probability is 0.0042 outright + 0.0458 × 0.05 on re-test = 0.0065, so the family rate is 7.5 %. With criterion (a) at two evaluable rungs per test it is 1 − 0.925 × 0.9973²⁴ = **13 %** [R: calc], against 46–54 % before. The "about half" problem is gone for an exactly unbiased analysis. It comes back for an analysis whose estimators are inside the tolerance but not perfect: see N-B5. |
| B-3 (M4) | trend rule discontinuous; rung index across families | **PARTIALLY** | §4.0 point 7 (l.336–366) | The rule is now continuous, always added and fitted within a family, which is the right form. Its substitution contradicts its own rule (N-B2). The width in untested families is a convention, not a measurement (N-B3). |
| B-4 (M4) | conditionals measured after loose rungs, applied deep | **RESOLVED** | §4.6 B3-d (l.841–858); COM B3-d | The conditionals are measured after ≥ 3 preceding rungs, with a derivation/test split by seed parity, and the width is counted from the deepest measured rung. This answers referee Q4 for B3. The truncation issue is in N-B4. |
| B-5 (M16) | late-hit credit "not testable" | **RESOLVED (design testable)**; credit **DEFERRED TO GATE A (GA-9)** | §4.6 (l.860–879) | The test is now testable. On R04 candidates (171.55 × 96,000 = 1.6×10⁷) a widened window at about 10⁻² gives about 1.6×10⁵ late counts, and the late-hit density at the nominal edge comes directly from millions of pile-up hits. The credit is floored at the sourced tail fraction. The test population is the wrong one (pile-up candidates, not prompt ones): N-B7. |
| B-6 (M31) | sideband cannot see the non-flatness | **RESOLVED** | §4.8 (l.978–1010) | T(Δφ) of the hard-scatter component is now measured on the no-pile-up pool. For Z(νν) that is 5.5×10⁶ events (Table 4.4a). At v1's R06 rate of 0.0162 per event this gives about 9×10⁴ signal-road candidates, so a ×2 non-flatness is resolved at > 100σ [E]. The with-pile-up closure on attributed hard-scatter candidates is evaluable only at R04–R05 per process (R06: 24 counts in 1,500 events, 32 in 2,000; N ≥ 55 is needed). That is not stated (C-3). |
| B-7 (M12) | detector variations do not reach the leading terms | **PARTIALLY** | §4.9 table (l.1035–1042) | The propagation path exists, and the 51 CPU-h of reruns are budgeted. But 2×10⁶ no-pile-up events per variation give **zero counts at every T2 candidate** for the leading topologies (the nominal floors need 10⁷–10⁸ events), so the shift is measured only at R04–R07. The rule that carries it to depth is not written. Also, a zero-count bound N_t × 1.14/M does not depend on the detector at all, so for bounded terms the nuisance is void. This should be said. *Fixed looks like:* two sentences in §4.9: the shift is measured at the deepest rung with counts and carried with s_tot; for bounded terms the detector nuisances act only through H and the conditionals. About 30 min. |
| B-8 (M32) | weighted samples | **RESOLVED** | §4.11 model table (l.1111) | Correct: one auxiliary channel per weight class, and effective counts with a flag. |
| B-9 (M33) | multijet population | **RESOLVED** | §4.7 (l.943–949); COM B4-e | A 10⁶-event loose population, a factorisation test in MET bins on Z(νν) and W, and a fallback are all stated. |
| B-10 (M9) | MET validation circular | **RESOLVED** (execution depends on R-3) | §4.7 (l.910–941) | The tuning is removed, an external Phase-2 PU-200 figure is used with the tolerance fixed before multijets exist, and "not validated" has a branch. |
| B-11 (M18) | MVA infeasibility overstated | **RESOLVED** | §3.2 (l.203–232) | The three reasons that hold are given, and the hybrid is excluded for blinding. |
| B-12 (M5) | "leading" loophole | **RESOLVED** | §4.0 point 6 (l.333–334); §4.12 rule 1 (l.1313–1314) | "Leading" is decided with no-credit values, which are the same values the likelihood uses. |
| B-13 (M34) | failure after the freeze | **RESOLVED** | §8 (l.1820–1834); COM FP-1 | There is a three-branch protocol and a reserved sample. A minor gap (no fresh sample is named for the B3 conditionals) is C-10. |
| B-14 (M8, M19) | toy budget, nested T1-g | **RESOLVED** | §4.11 point 5 (l.1222–1231); T1-h (l.1272–1276); script [7] | Both passes are budgeted (145 + 174 CPU-h), and the nested 1,449 CPU-h is avoided. The f_T-grid lever is offered but not adopted by default (C-1). |
| B-15 (M25) | identifiers | **RESOLVED** | COM (l.23–51), all of STR §4 | Spot-checked B2-c (agreement), T1-g/T1-h, B3-c/B3-d, B5-a…c, T2-d…g, BL-1, FP-1: STR and COM agree. |
| B-16 (M14) | thinning reach | **RESOLVED** | §4.5 (l.742–800) | K = 64, N_eff from the bootstrap. The projection gives a gain of ×19 at R06 (27,778 / 1,482) and N_eff ≈ 80 at R07 (4.4 × 19 = 84) [V: script [11]]. "B2-c expected NOT EVALUABLE at most deep rungs" is stated in advance. |

Cycle-1 C items: C-1 (Gate-A sheet) is applied, but at three pages (Part 3 condenses it). C-2 to C-11 are applied. C-4's
baseline "R07-direct" will be weak, and its size should be printed (C-9).

---

## Part 2. New findings on v2

### 2.1 Category A

#### N-A1 (A). "Target met" is guaranteed in the expected bounded outcome

*Evidence.* STR l.1183–1185 (COM TG-1, l.144): "Total σ_ln = ½ ln(B₈₄/B₁₆) … 'target met' if σ_ln ≤ 1 at the chosen
selection in both categories." The f₀ "sample-size limited" statement (l.1191–1193) is a separate flag; it does not
condition the verdict. The plan's target has two parts: "turn every leading zero-count bound into an estimate, and
bring the total background width to σ_ln ≲ 1" (PLAN l.129–131).
With every leading term a zero-count bound (the outcome STR expects, l.645–650 and §12.5 item 2), the predictive sum of
the 20 floors of Table 4.4a has σ_ln = **0.41** (script [9]; I reproduce 0.41, B₁₆–B₈₄ = 24.3–55.2). Adding a pile-up
estimate at R09 (median 20, s_tot 0.61) gives 0.36, and with a counted PV-pair ceiling it gives 0.17–0.31 [R: calc,
E4]. So in every plausible bounded case the pre-registered reading prints "target met". The narrow width comes from
averaging 20 independent bounds, not from any measurement.
*Why A.* This is a pre-declared outcome label that passes by construction in exactly the case it should flag. It would
be read as the headline claim ("central target met") and would hide that the background is bounded. That is the
"tautological comparison presented as evidence" of the escalation list, and it fails the honest-framing check.
*Fixed looks like.* In §4.11 point 3, COM TG-1 and GA-3, make "target met" require **σ_ln ≤ 1 and f₀ ≤ 0.5, with no
leading term that is a bound or no-credit**. Report the other cases as "width small, background bounded (f₀ = …)".
Effort: 15 minutes and one COM row.

### 2.2 Category B

#### N-B1 (B). The headline projection omits the no-credit ceiling H of the largest term

*Evidence.* PV pairs carry 18.5 of the 45.3-event floor (Table 4.4a, l.617). Their closure is "not evaluable unbiased
even at R04" and needs an enrichment of 10²–10³ (Table 4.4b, l.671). The default for NOT TESTED is entry at H
(l.677–679, l.1311, partial-outcome row l.1366).
H = P_geo + Σ_{k ≤ k_max} f_k, where k_max is half the layers the rung requires (l.568–571). At the fit-probability and
shape rungs, H applies only the counting and width cuts (l.573–575). H is therefore populated by events that pass the
width cut with half the double-crossing layers. It is far more populous than P_geo and is likely counted (m_H ≥ 1) in
7.65×10⁷ events at the R07–R11 widths. STR acknowledges this only in passing ("these floors apply … to the ceiling H as
well as to P_geo if H also counts zero", l.640–641). §0 and GA-3 quote the zero-count floor.
Each counted H event is N_t/M_t = 16.2 events. One-bin CLs limits on the full predictive distribution at R09
[R: calc2]:

| case (pool 600 CPU-h) | one-bin s₉₅ | equivalent B at σ_ln = 1 | reach, PLAN tab:reach [E] |
|---|---|---|---|
| all terms empty, H empty | 24.1 | 22 | ≈ 700 GeV |
| + pile-up median 20 (s_tot 0.61) | 33.9 | 35 | ≈ 640 GeV |
| + PV-pair H counted, m_H = 3 | 57.3 | 62 | ≈ 560 GeV |
| + PV-pair H counted, m_H = 10 | 95.9 | 108 | < 495 GeV |

So the stated range of 495–662 GeV (l.45–47) is too low if H is empty and too high if H counts a few events. The §0 one-bin
"about 28 events" (l.47–48) is the single-term κ = 35 value. The summed predictive gives 24.
*A second point on H: it is a ceiling only if the near-pass classes are defined over hit subsets.* With pile-up, the
finder can build a narrower core from a subset of the topology's hits plus pile-up hits. If f_k is computed from the
finder's single no-pile-up candidate (a wider one that fails the width cut), that event is neither "passer" nor
"near-pass", and P(r | t) ≤ H is violated.
*Fixed looks like.*
(i) In §0, §4.4 and GA-3, state the projection as max(zero-count floor, N_t·H) for every term expected NOT TESTED. Make
decision point 2 (l.2164) compute N_t·H at the T2 candidates from the pilot's f_k.
(ii) Enlarge the PV-pair pilot from 10⁶ to 10⁷ events (+29 CPU-h). This uses idle pre-freeze capacity, so it has no
calendar effect (§11.3: about 1,250 core-h idle). At 10⁷ it measures H for the leading term down to ~10⁻⁷ and makes the
headline a measured projection before the freeze.
(iii) Define f_k over subsets of the topology's own hits, or by the finder run with the width cut only. Add a **leak
test** on the 1,000 unbiased full-pile-up test events per topology: attributed passers whose no-pile-up event was neither
passer nor near-pass must be consistent with zero. This is re-analysis, 0 CPU.
Effort: 2 h of text, +29 CPU-h.

#### N-B2 (B). The extrapolation widths quoted do not follow STR's own rule

*Evidence.* l.344–345: "With fewer than three evaluable rungs in the family, σ_b := b₀." The held-out tests use two
rungs, R06–R07 (B2-b l.755–756; B1 l.656–658). So for the occupancy model, which is the only pile-up estimator beyond
R07 (l.793–795), and for the B1 promotion term, σ_b = b₀. The substitution at l.357–360 and in script [12] instead uses
the cycle-1 slope errors 0.029 and 0.097. Those were computed for three tested rungs R05–R07, and in v2 R05 is a
derivation rung.
Recomputed [R: calc, E2]:
- Pile-up (s_model 0.20, F 1.5) at R08 / R09 / R11 / R14 is **0.45 / 0.61 / 1.30 / 2.47**, against 0.20 / 0.45 / 1.23 / 2.44 in STR.
- Single interaction (s_model 0.35, F 2) is **0.78 / 1.04 / 2.22 / 4.23**, against 0.36 / 0.78 / 2.11 / 4.17.
The difference matters most at R08–R09, where T2 is likely to land (§2.4).
*Fixed looks like.* Either correct script [12], §4.0, §4.5 and GA-4, or let thinning, which has three test rungs
R05–R07 in the width family (l.748), set the R07 → R08 slope. In that case say that the occupancy model inherits that
slope only where B2-c passes. Effort: 1 h.

#### N-B3 (B). The width in untested cut families is a convention, and a measurement can replace it

*Evidence.* b₀ = ln F per rung, coherent (l.348–355). It is anchored to "v1's thinning drifted by 0.36 per rung", which
is the drift of the estimator v2 declares broken (§4.5). The fixer flags it as contestable (fix report §6 item 1). The
study rules say every systematic must be motivated by a measurement, and arbitrary conservative inflations are not
allowed (`CLAUDE.md`, "Systematic variation sizing"). This width enters the likelihood (l.1112). It makes every
extrapolated factor beyond R11 worthless (pile-up 1.3 at R11, 2.5 at R14), so T2 will not use the fit-probability, 2S or
shape families for pile-up at all (§2.4).
*Opportunity.* The ladder is cumulative, but each deep family's cut can also be applied **on top of a looser width**.
The direct sample has 4.8×10⁶ candidates at R05 and 2.4×10⁴ at R06 (49.72 and 0.247 per trial × 96,000). Applying the
R09–R11 fit-probability cut, the R12–R14 2S counting or the R15–R20 shape cuts there gives test points with hundreds to
thousands of counts in every family.
The occupancy model already factorises these cuts: it takes the fit-probability pass fraction from R06 finder
candidates (l.758–761). These crossing rungs therefore test exactly its assumption, and they make d_out = 0. What
remains is the R07 → R08 width step plus a measured factorisation term (|ln r| of the crossing test, or its stability
over the R05/R06/R07 widths as in B3-d).
Pile-up width at R09–R17 becomes about 0.48 (with σ_b := b₀ for the one width step) or 0.25 (with a fitted width slope),
against 0.61–3.68 [R: calc, E2]. The same construction applies to the B1 promotion term on the no-pile-up pool.
*Fixed looks like.* Define the crossing test rungs per estimator in §4.0 and §4.5 (and §4.4 for B1), with the same
evaluable-rung rule and verdict classes. Keep b₀ only where no crossing test is evaluable. Cost: re-analysis of the
direct and development samples, provided the trial records keep the fit-probability, 2S and shape variables for
R05–R06 candidates (they are computed by the finder). Check storage in §11.4. Effort: half a day of design, about 5 CPU-h.

#### N-B4 (B). Log-normal widths on probability factors can turn a credit into a penalty

*Evidence.* Conditionals, S, π_k and p_late enter as "nominal value with a log-normal nuisance: bootstrap error ⊕
s_tot(r)" (l.1112). With s_tot from point 7 they reach 1.2–3.7. A conditional with median 0.1 and s_tot 2.44 has mean
1.96 and is above 1 with probability 0.17. At s_tot 3.65 the mean is 78 [R: calc, E3]. A probability above 1 is
unphysical, and in the predictive mean the "credit" then exceeds the no-credit value. That contradicts the stated
logic that an untested factor only makes a selection worse (l.1315).
*Fixed looks like.* Truncate each such factor at its no-credit value (φ_eff = min(φ, 1)), or use the no-credit value
when the factor's predictive mean exceeds it. State this in §4.11 point 1 and in the prereg. Effort: 30 min.

#### N-B5 (B). Criterion (a) fails estimators that are inside the tolerance, and it has no re-test route

*Evidence.* The quoted size, 0.27 % per rung, is for r = 1 exactly at the evaluable limit (l.284–288). For an estimator
biased by half the tolerance (|ln r| = 0.2 at F = 1.5, or 0.35 at F = 2), which is "within a factor F" by definition,
the fail probability per evaluable rung at the limit precision is **6.7 %**. At three quarters of the tolerance it is
22.7 % [R: calc, E1].
A battery with 6 F = 1.5 rung checks near the limit (σ 0.12) and 6 F = 2 checks (σ 0.2), all biased by 0.2, fails a
within-tolerance analysis with probability **32 %** including (b). With 10–20 such checks it is 50–75 %. (a) violations
are outright FAIL (l.312) with no INVESTIGATE route, unlike (b).
*Fixed looks like.* Give (a) the same route as (b). A violation by less than 2σ_tot (ln F < |ln r| < ln F + 2σ_tot)
becomes INVESTIGATE with one fresh re-test; a larger one stays FAIL. The family rate for the case above drops from 32 %
to 8.6 % [R: calc]. List the power at |ln r| = 0.5 ln F next to the 0.27 % in the prereg. F is not loosened. Effort: 1 h.

#### N-B6 (B). Phase 3 is staffed with six channels; the study allows three

*Evidence.* l.2062–2064: "The schedule gives them 9 calendar days in Phase 3 … With six parallel channels this is about
54 channel-days". `ORCHESTRATOR_STATE.md` l.20: "at most 3 at a time". At three channels, 54 channel-days take
**18 days**, so +9 days on the critical path. Equivalently, 9 days give 27 channel-days, about 55–75 % of the PLAN's
35–50 person-days (l.2062).
Phase 3 holds: B1 (estimator, H, promotion, the Geant4 hand-over variants), B2 (re-grouping, a new occupancy model),
B4 (MET model with its external validation), B3, T1 zero-count tests, the T2 script, B5/B6 prototypes and the
per-channel 1-bot reviews (l.2045).
*Fixed looks like.* One of two:
(a) state Phase 3 at about 14–18 days, with the calendar at about 63–67 days;
(b) trim Phase 3 to three channels on the critical path (B1 + B3; B2; T1 + T2 + B4), and move the B5 and B6 prototypes
and the BDT recipe into the production window. Their *definitions* still go into the prereg (§8 item 3), but prototype
runs are not needed before it.
Re-state decision point 2 with the channel count. Effort: 1 h of schedule text.

#### N-B7 (B). The time-tag closure is tested on the wrong population

*Evidence.* Step 3 of B3-c (l.871–874) closes the late fraction on "the R04 candidates of the direct sample". These are
pile-up candidates: their own timing-layer hits come from many pile-up vertices, each with its own collision time.
The credit is for **prompt** hard-vertex candidates (single-interaction and SM terms, l.860–862), whose own hit is
prompt and whose late hit comes from an unrelated pile-up hit in the footprint. The density × footprint factorisation
is the same for both, but the pile-up candidates add an own-time component. A closure on them tests a mixture that
differs from the population the credit is applied to.
A prompt population exists. The Z(νν) hit-level sample (10,000 events) has 19.52 attributed hard-scatter candidates
per event at R04, i.e. 1.95×10⁵ candidates. That gives about 2,000 late counts at the widened 10⁻² window and about 20
at the nominal 10⁻⁴ window (σ_ln 0.23, so a direct nominal-window check is evaluable for F = 2) [R: calc, E7].
The B1 test overlays add about 10⁴ attributed R04 candidates.
*Fixed looks like.* Make the test population the truth-attributed prompt candidates (SM hit-level and B1 test
overlays). Keep the pile-up candidates as a separate consistency check. Add the nominal-window direct count on prompt
candidates as a second test point. 0 CPU. Effort: 1 h.

### 2.3 Category C

- **C-1 Toy parametrisation by default.** Adopt lever (ii) (l.2120–2122) for **both** passes, with exact toys at 3–5
  points as the check: pass 1 is 5 × 11 f_T × 8 μ × 652 s = 80 CPU-h instead of 145, and pass 2 is 48 instead of 174.
  That saves **191 CPU-h**. Calendar effect: less than 1 day, because both passes sit inside 3-day windows.
- **C-2 Stage the B1 overlays on the pilot.** Overlays for topologies expected NOT TESTED (NI × 3 and loopers: 6,000 ×
  25.2 s = 42 CPU-h; PV pairs: 9,000 events, 63 CPU-h, if the pilot's enrichment is below 10²) buy no verdict and no
  credit, because those terms enter at H. Produce them only for topologies whose pilot-projected test is evaluable.
  Saves up to **105 CPU-h (0.6 day)**. No MUST criterion changes: B1-a's verdict is NOT TESTED either way.
- **C-3 B5 with pile-up.** In the reduced form, the sideband on SM + pile-up (136.5 CPU-h) gives B5-a on attributed
  hard-scatter candidates at R04–R05 only. The hard-scatter non-flatness is measured far better on the no-pile-up pool.
  Two cheap improvements:
  - Count the signal road on **all 10,000** Z(νν) hit-level events, which are already produced for B4. That gives 162
    counts at R06, so R06 becomes evaluable with the sideband from 1,500 events.
  - Alternatively, take lever (iii) (−137 CPU-h, −0.8 day). Keep the 500 pile-up events × 20 roads for B5-c.
  Either way, run the road rotation **inline** in the no-pile-up pool jobs: the pool stores 50-byte summaries only
  (l.712–714), so the 10 CPU-h of rotation cannot be done afterwards.
- **C-4 Reallocate saved CPU to the pool (GA-3).** The pool is the line with the largest payoff. For pools of 315 / 600 /
  1,200 CPU-h, the one-bin limit in the bounded case is s₉₅ = 42 / 24 / 14, i.e. reach ≈ 613 / 697 / 778 GeV EST
  (σ_ln = 1 row of PLAN tab:reach at equal s₉₅) [R: calc2]. Cutting C-1 to C-3 and the composition variation until R-17
  gives a range (§2.5) frees about 460 CPU-h, which brings the pool to about 1,060 CPU-h at the same total. Stage it:
  600 first, the rest after decision point 2 if N_t·H does not dominate (N-B1).
- **C-5 Compress Phase 2 and Phase 5** (§2.6): about −5 days with three agents.
- **C-6 GA-8 and the stop rule.** STR itself expects the stop rule to trigger at checkpoint 1 (l.2154–2155). Present it
  as a choice: approve 4,401 CPU-h, with a likely re-ask at day 7 using measured costs, or pre-approve 4,401 + 1,989
  contingency = 6,390 (threshold 8,307). Either is compliant with brief §7.
- **C-7 Figures** (figure-scrolling test). Add:
  - B3-c closure ln r against t_cut on prompt candidates;
  - B1 decomposition P_geo, f_k, H against rung per topology (it carries N-B1 and referee Q1/Q4);
  - G for the 16 T2 candidates with verdict flags and the bootstrap winner frequency (Q12, Q14);
  - s_tot against rung per estimator (Q4).
  Fig. 7: the v2 predictive distribution is not log-normal (a sum of exponentials). Compute the v2 reach directly and
  mark it at (B₅₀, reach_v2), stating its equivalent σ_ln. Do not place it on a σ_ln = 1 curve.
- **C-8 Message bracket.** In the bounded outcome the abstract should quote the bracket: "≈ X GeV if the background is
  as large as the simulation allows (conservative, quoted); ≈ 1,026 GeV if negligible (B = 0)". It should also give
  the v1 → v2 change of the bound (1.2×10⁶ → ≈ 45, 4.4 decades). Both are true and publishable statements, and the
  second is a strong one.
- **C-9** Print the expected size of the always-eligible baseline "R07-direct". Its single-interaction terms rest on
  overlay-sized bounds (for example PV pairs N_t × 1.14/9,000 ≈ 1.6×10⁵), so it is about v1's level. Say so.
- **C-10** Failure protocol (§8): name the fresh sample for B3 conditionals (a new pool slice by seed stream) and its cost.
- **C-11** Composition variation (26 CPU-h of the 52): run it only once R-17 gives a range. Otherwise it is a
  robustness test that changes nothing (l.706–708).

### 2.4 The redesigned estimators and the closure scheme: weakest links and total width

| estimator | weakest link | cheapest extra validation that most raises confidence |
|---|---|---|
| B1 P_geo·S + Σ f_k π_k, ceiling H | (1) whether H is a true ceiling (subset definition of f_k); (2) π_k as a product of independent per-layer occupancies | the leak test of N-B1 (0 CPU); π_k against near-pass overlays at R06 is already there (B1-f) |
| B2 thinning | reach stops at R07 (N_eff ≈ 80), at R08 ≤ 10 | B2-g measures it before the freeze (already there) |
| B2 occupancy model | layer-to-layer correlations; fit-probability and shape inputs from finder candidates (l.758–761) | the crossing test rungs of N-B3 (0 CPU) |
| B3 conditionals | transfer across families (B3-d) | already measured after ≥ 3 preceding rungs; add the truncation of N-B4 |
| B3-c time tag | test population (N-B7); the sourced tail (R-7) | prompt-candidate closure at nominal and widened windows (0 CPU) |
| B4 MET model | an external Phase-2 PU-200 figure must exist and differ from the parameter source | retrieval R-3 first, in week 1, before the B4 design |
| B5 | with pile-up only R04–R05 evaluable | C-3 |

**Would the extrapolation convention and the NOT TESTED policy make the result uninformative?** No, and the reason
matters for the design. Under the default, NOT TESTED terms enter at H, a measured number with only counting
statistics, and factors with large s_tot are simply not chosen by T2. I computed the predictive total for typical
cases [R: calc, E4/E5]:

| chosen selection (illustrative) | B₅₀ | total σ_ln | f₀ | one-bin s₉₅ |
|---|---|---|---|---|
| R08, pile-up median 100 (s 0.45) | 140 | 0.34 | 0.27 | 73 |
| R09, pile-up median 20 (s 0.61) | 60 | 0.36 | 0.62 | 34 |
| R11, pile-up median 2 (s 1.30) | 40 | 0.40 | 0.90 | 26 |
| R14, pile-up median 0.5 (s 2.47) | 39 | 0.44 | 0.78 | 26 |
| bounds only | 36 | 0.41 | 1.00 | 24 |

The pile-up medians are illustrative [E], from the R05→R07 fall of ×200–340 per width rung. The total σ_ln stays at
0.3–0.45 in every case. The result is not uninformative.
The cost lies elsewhere. The zero-count floors do not depend on the rung, so beyond about R09–R11 going deeper buys
nothing in background and loses signal. T2 will choose about R09–R11. The deep machinery (conditionals for R15–R20,
widths beyond R11, the promotion model for untested topologies) then earns no credit in the expected outcome. It
matters only if the floors fall: through biasing gain, conditional credits multiplying the one allowed zero (l.643–644),
or the time tag in SR-T. This is not over-engineering of the likelihood, which must handle every outcome, but it argues
for *staging* the production that only those cases use (C-2, C-3).

### 2.5 Proportion: what the +1,018 CPU-h and +1,143 lines buy

| addition (script [5]) | CPU-h | verdict |
|---|---|---|
| no-PU pool 600 (incl. +125 unit-cost correction) | +410 | **keep; highest value** (reach +85 GeV per doubling, C-4) |
| enrichment pilot | +27 | **keep; enlarge the PV-pair part to 10⁷ (+29)** (N-B1). It decides the headline |
| second toy pass, five selections | +145 | needed; parametrise (C-1, −191 over both passes) |
| T1 development and validation | +51 | keep (M1/M7 tests are the core of the zero-count claim) |
| enlarged development samples | +100 | keep (idle capacity, no calendar effect) |
| Geant4 vertices sized correctly | +60 | keep (correctness) |
| QGSP_BERT + composition | +52 | keep physics list; composition only with a sourced range (C-11, −26) |
| multijet cost and loose population | +50 | keep |
| overlays 42,000 | +21 | keep the size, stage by topology (C-2, −105) |
| P1, PDF4LHC21, FxFx 1,500 | +42 | keep (MUST, plan items) |
| secondaries test, T2 bootstrap, time tag, migration, twins | +63 | keep (cheap, referee-proof) |
| SHOULD: B6 to all terms, 5 keV and 1 TeV, partners; B5 no-PU | +108 | keep. B5 with pile-up per C-3 (−137 or a 0-CPU improvement) |

Removable or stageable without weakening any MUST acceptance criterion: C-1 (−191), C-2 (−105), C-3 lever (iii) (−137),
C-11 (−26). That is **−459 CPU-h, about 1.5–2 production days**; C-1 is mostly off the critical path. Spending it on the
pool instead (C-4) is cost-neutral and buys about 50–80 GeV in the bounded outcome [E].
On text: the 2,391 lines are acceptable for a binding strategy. The repetition between §4, §12.1, §13 and COM is the main
excess; it can stay, because COM is now the master.

### 2.6 Where the 44 non-production days go, and what parallel executors can compress

From script [7]:
- Phase 2: 7 days
- Phase 3: 9 days
- freeze: 2 days, plus 2 for an ITERATE
- 4a review: 3 days, plus 2 for an ITERATE
- 4b: 3 days, plus 2 for an ITERATE
- Gate B: 2 days
- 4c: 3 days
- Phase 5: 7 days, plus 2 for an ITERATE

That sums to 44 [V]. With at most 3 agents and 12 cores:

| block | days | compressible? |
|---|---|---|
| Phase 2 | 7 | **to about 5.** The critical CPU is 471 CPU-h: 2.7 days at 174/day, because C1 campaigns are queued production-like, or 4.1 at 116. Run C1 + C2, S2 + P1 + retrieval, and pilot + T1 builder + Geant4 hand-over as three agents. Decision point 1 at day 5 |
| Phase 3 | 9 | **not compressible; at risk of +9 (N-B6).** Trim to three critical channels |
| freeze + ITERATE | 4 | draft `PREREG_v2.md` during Phase 3 so that the freeze is review only. Keep the ITERATE |
| reviews and ITERATEs (4a, 4b, 5) | 13 | not compressible. The 4a review already overlaps the S1 chain. The ITERATE allowances are realistic, as this cycle shows |
| Gate B | 2 | human; not compressible |
| 4c | 3 | keep |
| Phase 5 | 7 | **to about 4.** Sections 1–6, 8–10 do not depend on the signal and can be drafted during the 4a production (the note-writer channel already exists, l.2048). Phase 5 then only fills §7, the abstract and the review |

The net effect is about −5 days (C-5), set against +0 to +9 days of Phase-3 risk. A realistic calendar is **55–65 days**.
The 8-week estimate is honest. The 2–4 week target is unreachable on non-production days alone, as STR says (l.2113).

### 2.7 The honest headline per outcome

| outcome (PLAN §8) | what v2 would show | proposed message (GA-3 (i)) | honest? publishable? |
|---|---|---|---|
| bounded middle (expected) | B₅₀ ≈ 36–60, f₀ ≈ 0.6–1, total σ_ln ≈ 0.4 | "bounded at the N-event level by simulation statistics, pile-up estimated", band and conservative edge | honest **once N-A1 is fixed**. Publishable as a strong projection: ≈ 640–700 GeV EST, about 3.5× the existing bounds of ≈ 180 GeV, with a pre-registered and closure-tested method. Use the C-8 bracket |
| bounded, PV-pair ceiling counted | B₅₀ ≈ 120–240 | as above, with PV pairs "no credit" | honest; reach ≈ 490–560 GeV. Still above existing bounds |
| real background | counts in the large samples | measured irreducible background | honest; "the first measured background" is a genuine result |
| good | needs a gain G ≈ 5–50 or conditional credits (l.649–650) | "estimated" | honest only with N-A1's two-part reading |
| closure fails | R07-direct only (≈ 10⁵ level, C-9) | method and anatomy paper | honest; weaker but publishable (P1, efficiencies, anatomy) |

**The single additional measurement that most moves "bounded" toward "estimated"** is the pilot's PV-pair
measurement: f_k (hence N_t·H) at R04–R09 and the test-overlay enrichment. PV pairs are 41 % of the floor. Under the
default they can never be labelled "estimate" unless that enrichment reaches 10²–10³ (Table 4.4b). The pilot is
scheduled at days 0–7, which is early enough.
What is missing is a **pre-declared redirection rule** at decision point 2. If the PV-pair enrichment is between 10 and
10², move overlay CPU from the untested topologies (C-2) to PV-pair test overlays. If N_t·H dominates the projection,
stop enlarging the pool and spend the CPU on biased PV-pair generation. Today only the pool biasing (GA-3 (ii)) is
linked to the pilot. For SR-T, the zero-CPU lever is retrieval R-7 (the timing tails) in week 1.

### 2.8 Paper readiness

- The seven flagship figures map to planned outputs (§9 l.1862–1875); I checked each source row.
- Fig. 4 and Fig. 5 now carry the estimate / bound / no-credit labels and the derivation/test markers, which is good.
- Fig. 7 has a marking issue (C-7).
- The supporting figures cover C1, C2, B5, T1, B6, S2, MET and the BDT. Missing: B3-c, the B1 decomposition, the T2
  ranking and s_tot (C-7).
- All 25 referee questions still map to items (§10 l.1902–1930).
- Q1's honest answer in the bounded outcome is "bounded by simulation statistics, with f₀ = …". It is only honest with
  N-A1 fixed.
- Q4's answer improves materially with N-B3.
- Q13 is served by T1-b.
- No orphan question.

---

## Part 3. Gate-A package: the one-line questions

Assessment of §12.1 (l.2172–2263, about 3 pages): every item has a default and costs. GA-1, GA-2, GA-6, GA-7 and GA-8
are clear. GA-3 mixes three questions. GA-4 bundles four technical rules, of which only one is a user-level choice. GA-5,
GA-9 and GA-10 have no real alternative the user needs to weigh. Proposed one-page form: **five decisions and five
defaults**.

**Decisions for the user**

1. **GA-1 (blinding exception, must be the user's):** "May the C1 reproduction compare six v1 signal counts that are
   also v2 candidate efficiencies, reported only as PASS/FAIL and sealed until Gate B (4 others open)? Yes, recommended
   / open all 10 and disclose / drop the 6 (best-point check lost)." CPU 14 CPU-h in every option. Drop options (d)
   and (e): they add nothing a user would choose.
2. **GA-3 (paper message and pool):**
   - "The expected result is a background *bounded* at about 25–55 events (reach ≈ 640–700 GeV EST), or worse if the
     PV-pair ceiling counts. Proceed to production without asking if the Phase-2 pilot confirms this (recommended), or
     pause at decision point 2 for you?"
   - Second line: "No-pile-up pool 600 CPU-h (recommended; ≈ 700 GeV bounded) / 1,200 (+600 CPU-h, +3.4 days, or
     cost-neutral with C-1…C-3; ≈ 780 GeV) / 315 (≈ 610 GeV)."
   The reporting rule (i) is not optional and should not be asked.
3. **GA-4 (only the user-level part):** "A background term whose closure cannot be tested enters at its directly
   measured ceiling (no credit; the selection stays eligible and is flagged). Approve (recommended), or make such
   selections ineligible ('closure fails' becomes the likely paper)?"
4. **GA-7 + GA-8 (merged, budget and calendar):**
   - "Approve 4,401 CPU-h and about 58 days (8 weeks, against your 2–4 weeks; not reachable even with zero production)
     with the downscopes DP1, DP2, DP4, DP5 (they save 513 CPU-h, 3 days)?"
   - Stop-rule form (C-6): "Re-ask at day 7 if measured costs exceed 5,722 (likely), or pre-approve the contingency up
     to 6,390 (stop above 8,307)?"
5. **GA-2 (optional, can default):** "Signal 2,000 rows per point (recommended; 15 % MC error at the best point) or 4,000
   (10 %; +827 CPU-h, +4.7 days)?"

**Defaults to report, settled without the user unless they object**

- GA-4 technical parts: F = 1.5 / 2 unchanged; the family-wise rule; the extrapolation convention, to be replaced
  where possible by crossing tests (N-B3).
- GA-5: σ_NLO nominal, resummed cross-check beside every limit; the infracolour correction as a one-sided band.
- GA-6: dE/dx excluded; the forgone gain is measured (2 CPU-h).
- GA-9: time-tag credit only if its closure passes and the tails are sourced. The alternative saves 10 CPU-h, so it is
  not a real choice.
- GA-10: the endcap wording as fixed by brief D1, with the provenance note. It is an FYI, because D1 is not open.

---

## Verdict input for the arbiter

PASS is not possible yet: one A item (N-A1) and seven B items (N-B1 … N-B7), plus the PARTIALLY items B-1 (via N-A1 and
N-B1), B-3 (via N-B2 and N-B3) and B-7 (two sentences). Each fix is text, design or re-analysis. The only CPU added is
+29 CPU-h (PV-pair pilot) and about 5 CPU-h (crossing tests), which the savings of §2.5 more than cover. None reopens a
brief §3 decision, introduces ρ ≥ 3 or ×100 growth, or loosens an F. Total fixer effort is about 1–1.5 days.
