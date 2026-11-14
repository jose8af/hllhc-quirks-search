# Constructive review, cycle 7 — STRATEGY v7 (Jules) — session Klaus, 2026-11-14 04:05

Artifact: `outputs/STRATEGY_jules_2026-11-14_03-40.md` (v7), with `outputs/budget_stdout_v7.txt`. Scope (arbiter v6
§12): Q2 and §0 read as the human; U1; the final Gate-A package. Not a re-review of the design. Role:
`agents/constructive_reviewer.md` (honest-framing check applied). Line numbers are v7's.

## 1. U1 as the human reads it — RESOLVED

Reading only §0 and §12.1:

| what the human must understand | where v7 says it | status |
|---|---|---|
| basis of the day-7 and day-15 readings, ×5–50 above the after-CKF figure | §0 l.101–102 "The day-7 and day-15 projections read own hits before CKF (Df-9) and are expected ×5–50 above the after-CKF figures of this summary"; Q2 l.2786–2789 "count own hits before CKF, with no S_CKF and no conditional credit (Df-9, §11.7 rule 1), and are expected ×5–50 above this figure (… B₅₀ ≈ 5.0–5.1×10⁴ at ε_pair = 0.8 and ≈ 5.0–5.1×10⁵ at 0.98, assumed, not measured …)"; §11.7 rule 1 l.2729–2734 | clear |
| crossing 300 at day 15 is expected | §0 l.73 and l.90–91 "By v1's conversion counts this is the expected branch"; Q2 l.2786 "expected to pause the study before production"; the after-CKF figure ≈ 10⁴ is already ≫ 300, and the own-hit basis only strengthens it | clear |
| the after-CKF figure is a lower value | §0 l.66–67, Q2 l.2781–2782 "(after CKF, as v1 counted them; a lower value, since terms whose S_CKF test is not evaluable stay on all own hits, annex route 6)" | clear |
| options (a)/(b)/(c), cost in days and CPU-h, paper each leads to | Q2 l.2798–2816: (a) ≈ 2 days, reserve 156 CPU-h inside the figure; (b) 0 CPU-h, no delay, "real background", "no mass reach beyond the existing bounds" in the expected case; (c) time not estimable, reported at day 15, CPU-h inside development allowance and remaining reserve, "middle" if it works else (b) | clear |
| how a (c) redesign is judged before the freeze; gain unmeasured | Q2 l.2809–2816 "with the redesigned conditional and S_CKF estimated on development samples (EST, §11.7 rule 1)"; "If S_CKF cannot be estimated before the freeze, every reduction must be ×1/(1 − ε_pair) larger (×5–50, not measured)"; "The veto's rejection has not been measured; its signal cost is known only at Gate B"; rule 1 l.2731–2734 "No credit in the result comes from these estimates" | clear |
| the decays-in-flight term behind "a veto alone would not avoid the pause" rests on 1–2 counts | §0 l.93 "at v1's central decays-in-flight size (1–2 counts)"; Q2 l.2792, l.2812–2813 "That size rests on 1–2 counts; at its size ×e⁻¹ the conversions alone would suffice (B₅₀ 159–256 …)" | clear; stdout l.352 prints 159 / 256 (the verdict's draft 158–254 is superseded by the printed values, §13.6) |
| optional rider: decision at day 7, +7.0 CPU-h | Q2 l.2821–2828: day 7 if B₅₀ ≥ 3,000; +7.0 CPU-h, approved 4,616, threshold 6,001 (stdout l.206) | clear (C1 below) |

**Consistency between §0, Q2, §11.7 rule 1 and Df-9.** No contradiction found. §0 l.93–95 and Q2 l.2794 both say
(α1) with fit-probability credit is admitted in the day-15 projection only under (c); rule 1 l.2731 says only the
(c) test multiplies by the redesigned conditional and S_CKF; Df-9 l.2877 ("credited only where tested") is
consistent with this, since no S_CKF test exists before the freeze. Annex route 6 l.2896 uses the same ×1/(1 − ε_pair).
The §4.4 labels l.790 and l.870 carry the after-CKF / own-hit wording. stdout v7 differs from v6 by exactly the two
U1 lines (l.352–353; `diff` checked). The phrases "day-7 reading counts own hits" and "only route in this strategy"
no longer appear in v7 (grep).

**Q1, Q3, Q4, Q5 unchanged and self-contained.** `diff` of §12.1 v6 → v7: the only hunks are in Q2 (stem, (b), (c),
rider part 3). Q4 l.2843–2855 still reads 4,609 CPU-h, threshold 5,992, 60 days (57.8 without the pause) against the
2–4 week target, with the (c) redesign time excluded and reported as an overrun.

## 2. Final judgment: YES — v7 is a sound, honest basis for Gate A

Honest-framing check: the expected outcome (≈ 10⁴ events, reach at or near existing bounds, expected pause) is
stated before the upside in §0, the leading sentence and Q2; the upside is labelled statistics-only and conditional;
the (c) bar is stated on the basis on which it will actually be judged. Nothing hides a problem.

New findings: **A 0, B 0, C 4.**

- **C1 (rider).** Q2 l.2822 sets the rider's trigger at a day-7 B₅₀ ≥ 3,000 but does not say that it is expected to
  fire: the after-CKF figure alone is 0.7–1.0×10⁴ (stdout l.358), and the day-7 basis is ×5–50 above it (l.353). The
  human would read "up to ≈ 8 days earlier" as a contingency rather than the expected gain under (c). Fix: append
  "(expected to trigger)" after "at least 3,000 events". The package states it.
- **C2 (Df-9 row).** The defaults table l.2877 does not say that Df-9 sets the basis of the day-7/day-15 projection;
  a human scanning the defaults would not see that its alternative (CKF inside H) would put the projection on the
  after-CKF basis. It does not change the expected pause (≈ 10⁴ > 300). Fix: add "(sets the basis of the day-7 and
  day-15 projections, §11.7 rule 1)". The package does so.
- **C3 (candidate package, not v7).** Co v6 §5 says the residual paper is rated "publishable but less strong" by the
  plan. PLAN l.508–509 gives that rating to the "Closure fails" outcome, not to the "real background" outcome
  (l.506–507). Removed from the package below.
- **C4 (rule 1 inputs).** §11.7 l.2716 lists "S_CKF on the development overlays" among the day-15 inputs while the
  projection takes no S_CKF credit (l.2729). Fix: "(used only in the test of a Q2 (c) redesign)". Wording only.

None is blocking.

## 3. Gate-A package — final text (copy verbatim into `gates/GATE_A.md`)

Word count: **1,499 words by `wc -w`** (tables, headings and symbols included; 1,336 counting only tokens with a
letter or digit). Every number is from v7 or `budget_stdout_v7.txt`; the eleven corrections of verdict §9 and the
§8(ii) items are applied (robustness sentence at width ≥ 0.05: stdout l.329, 333, 337, 341; the 5–52 % is STR
l.2199; paths to a stronger paper and residual paper; decision-point list; the > 80 % item, STR l.2159). Changes
from Co v6 §5 besides length: "publishable but less strong" removed (C3); Geant4 "schrodinger so far" (FEAS_B
l.53); the rider marked "expected" (C1); 43.5 days stated as without critical-path production (STR §11.3).

---

# GATE A — quirks v2: strategy, benchmarks and schedule

Sources: STRATEGY v7 (STR), `budget_stdout_v7.txt`. **Every reach is an ESTIMATE on v1
placeholder efficiencies** (best Λ per mass).

## 1. Headline
**Expected (ESTIMATE).** By v1's counts the background at the R08–R09 selections is **≈ 0.7–1.0×10⁴ events, led by
hard-scatter photon conversions** (after CKF, as v1 counted them; the day-7 and day-15 projections read own hits
before CKF and are expected ×5–50 higher). v1's conversions fell ×6.5 per width step, not like
pile-up (×200–340; p ≈ 10⁻³). With the strategy's normalisation width (0.17) the **reach is below 243 GeV, at or near the existing bounds (≈ 180 GeV; R-20 pending)**.
This holds for any width of 0.05 or more (the reference sideband analysis quotes 5–52 %). The ≈ 270–300 GeV (84 %
edge; 390–420 for a background known exactly) are statistics-only. **The day-15 rule is expected to pause the
study.** At v1's central decays-in-flight size (1–2 counts), the background without conversions is 401–663 events,
of which decays in flight 385–647, so removing conversions alone would not avoid the pause. 

**Upside (ESTIMATE**, 84 % edge (median), statistics-only): 420–455 GeV (470–500) if conversions and decays in flight fall
like pile-up (310–370 at width 0.17; still pauses, B₅₀ 587–975); 705–640 (770–695) if Z(νν) is tested and other
ceilings count 10–100, conditional on the promotion model being submitted; 710 (790) if every ceiling is empty, an
upper edge; 1,026 at negligible background.

**Paths to a stronger paper, none demonstrated:** a pilot counting far fewer conversions and decays in flight than
v1; under (c), a conditional removing ×31–52 of the conversions plus a reduction of the decays in flight, judged
on development estimates of the conditional and of S_CKF; credit from conditionals measured in production
(unmeasured). **If none works**, the "real background" paper remains: thickness law, hit-level chain at
pile-up 200 with efficiency map, first measured quirk-plane background term by term, the simulation-statistics
barrier, sideband recipe, closure tests.

## 2. What Phase 1 established
| unit (4 jobs/node) | cost |
|---|---|
| PU-200 event through the chain | 13.5 s |
| finder trial | 11.7 s |
| ρ = 2 event | 206 s at 1.46 GiB |
| no-pile-up event, SM pool | 45 ms (guessed) |

Of 4,453 CPU-h: 753 on measured unit costs, 2,322 derived, **1,378 guessed** (STR Table 4.0).
- v1 chain runs on Linux, no source build. MG5 2.9.22 + Pythia 8.313 reproduce v1's LO
  σ (92.33 ± 0.07 vs 92.26 ± 0.04 fb); NLO K = 1.165 at 200 GeV; Geant4 11.4.3 installs node-locally in ≈ 3 min
  (schrodinger so far). The runner passes kill/resume, memory and I/O-error tests (Argo, SSH).
- Incidents (`LOG.md`): 14:06, stale file handle after a cajuela rename (admin fix; directories are never renamed);
  15:12, einstein out of memory, orchestrator and executors killed, cajuela I/O errors to 15:20. Constraints since:
  10 GB cap for all agents, nothing heavy on einstein, ≤ 3 agents, one install at a time, job work on local scratch,
  Geant4 per worker; 10 slots off-hours.
- Review: seven cycles; Category A 11 → 4 → 1 → 0 → 0 → 0, B 24 → 14 → 15 → 5 → 3 → 1 (cycles 1–6); [cycle 7: …].
  Cycles 1–2 rebuilt likelihood and closure tests; 3 completed the background pool; 4–5 restated the expected outcome
  and fixed the S_CKF samples and mixed-excess pass (+36 CPU-h); 6 corrected the day-15 projection basis.

## 3. Your decisions
Answer "Q1 ●; Q2 ●; …" (● = recommended default).

**Q2 (central): what if the day-15 projection exceeds B₅₀ = 300 (or both pile-up estimators miss their cap)?** The projection counts own hits before CKF, with no S_CKF and no conditional credit: expected
×5–50 above 10⁴ (B₅₀ ≈ 5×10⁴ at ε_pair = 0.8, ≈ 5×10⁵ at 0.98, assumed). Crossing 300 is therefore expected.
- **● (a) Pause and ask at day 15:** ≈ 2 days (inside the 60), 0 extra CPU-h; the 156 CPU-h reserve tests the
  leading term. You then choose (b) or (c).
- **(b) Proceed now with the measured background:** 0 CPU-h, no delay. Paper: "real background", reach expected
  below 243 GeV, i.e. none beyond existing bounds; production conditionals may add some, credit unmeasured.
- **(c) Redesign before the freeze:** a conversion-removing conditional built on development and pilot samples;
  the freeze moves by an unestimated time (reported at day 15, an overrun); CPU-h from the development allowance and
  the remaining reserve. Works if projected B₅₀ ≤ 300 with conditional and S_CKF estimated on development samples
  (EST): conversions ×31–52 lower **and** decays in flight reduced (their size rests on 1–2 v1 counts;
  at ×e⁻¹ conversions alone suffice, B₅₀ 159–256). Without an S_CKF estimate every reduction must be ×5–50 larger.
  Veto rejection unmeasured; signal cost known at Gate B. Say whether (c) may also target decays in flight. Paper:
  "middle" if it works, else (b).
- If B₅₀ ≤ 300 (≥ 560 GeV, statistics-only): production proceeds; "middle" outcome.
- *Optional rider* ("Q2 ● + rider"): (b)/(c) asked at day 7 if B₅₀ ≥ 3,000 (expected, given ×5–50); pilot veto
  fraction by day 12 (0 CPU-h); 1,000 γ overlays (+7.0 CPU-h: 4,616 approved, threshold 6,001). Gain: up to ≈ 8
  days under (c).

**Q1, C1 blinding.** ● Sealed: six v1 signal counts compared PASS/FAIL only until Gate B, four open. Alternatives:
all ten open; six dropped. 14 CPU-h each.

**Q3, D4 exception.** An untested MUST closure criterion enters at its tested ceiling, "no credit", selection
eligible (routes: STR Q3 annex). ● Yes. Alternatives: comply where costed, ≈ +680 CPU-h (100–1,230), +3.9 days;
strict ("closure fails" likely).

**Q4, budget and calendar.** ● **4,609 CPU-h, 60 days**, stop-and-ask at **5,992** (1.3×), with [DP1] B5 reduced
(−358), [DP2] B6 at 4 points (−155), [DP4] S4/S5 out, [DP5] second hadronisation model at generator level after an
install attempt. Contingency 2,150 CPU-h listed, not pre-approved; all guesses doubled gives 5,987, near the
threshold. **Your 2–4 weeks is missed by four to five weeks**: 43.5 days have no critical-path production.
Alternatives: table §5; envelope 6,759 (threshold 8,787).

**Q5, truth-level signal before the hash** (47 + 266 CPU-h; selection-independent). ● Yes, idle capacity, 0 days.
Alternative: after the hash, +47 CPU-h, +1.8 days.

## 4. Defaults (override if you wish; STR §12.1)
| # | default |
|---|---|
| Df-1 | 2,000 signal rows/point (4,000: +827 CPU-h, +4.7 d) |
| Df-2 | closure F = 1.5/2, cap ln F/3, one re-test |
| Df-3 | NLO σ nominal, resummed beside it |
| Df-4 | dE/dx not a candidate |
| Df-5 | time-tag credit only where it closes |
| Df-6 | endcap outlook "signal ×1.5–3.2" |
| Df-7 | unsourced detector variation: shift reported, no nuisance |
| Df-8 | toys parametrised, exact check at 3 points |
| Df-9 | ceiling on all own hits, S_CKF credited only where tested (sets the day-15 basis; alternative: CKF inside the ceiling) |
| Df-10 | coverage checks as one family of 10 |

## 5. Budget and calendar
| variant | CPU-h | threshold | days (no pause / pause) |
|---|---|---|---|
| MUST only | 4,176 | 5,429 | 56.9 / 58.9 |
| **MUST + reduced SHOULD (●)** | **4,609** | **5,992** | **57.8 / 59.8** |
| full SHOULD | 5,123 | 6,660 | 58.1 / 60.1 |

4,609 = MUST 4,019 + SHOULD 434 + reserve 156. Capacity assumed: 174 core-h/day production, 116 development (0.75 /
0.50 of 232; measured in week 1). Range: 49 days (all reviews pass, MUST only); 65 at 0.50
utilisation; +8 with two ITERATEs per review (all without pause). Storage ≈ 470 GB (670 at cap) of 1.5 TB.

## 6. Decision points after Gate A
- **Day 5:** C1 and C2 pass?; first CPU re-projection (stop rule may fire).
- **Day 7:** preliminary projection from the pilot (own hits before CKF); with the rider, Q2 asked.
- **Day 12:** MET model, final pilot classification, generator cut; rider readings.
- **Day 15 (binding):** projection for every term, own hits before CKF; a (c) redesign judged on development
  estimates. Pause if B₅₀ > 300; reserve by rule 3; estimators above cap redesigned or "not submitted".
- Freeze days 17–19 (second re-projection); Gate B ≈ day 49 (51 with pause); Gate C ≈ 58 (60).

## 7. Top risks
1. Conversions: no reach beyond existing bounds unless a demonstrated ≈ 97 % conversion rejection is combined with
   a reduction of decays in flight, judged on development estimates.
2. The conversion normalisation will likely exceed 80 % of the uncertainty: investigated, not accepted; sideband
   recipe as the way out.
3. CPU: 1,378 CPU-h guessed; stop rule may fire at day 5 or the freeze.
4. Development: 30 channel-days against the plan's 35–50 person-days.
5. Pile-up beyond R07 on one estimator; Geant4 → Fatras hand-over; MET model needs two public sources.

## 8. Files
STR v7 (§0, Table 4.4c, §11, §12); `budget_stdout_v7.txt`; `COMMITMENTS.md`;
`phase1_strategy/outputs/feasibility/FEAS_{A,B,C}_*.md`; the six arbiter verdicts in `phase1_strategy/review/arbiter/`;
`LOG.md`; `DEVIATIONS.md`.

---

## 4. Notes for the orchestrator
- Fill "[cycle 7: …]" after the cycle-7 arbiter (e.g. "cycle 7: 0 A, 0 B, PASS").
- If C1/C2 are applied to v7, the package already matches; if not, the package's "(expected …)" and "(sets the
  day-15 basis …)" are derived from v7's own numbers and remain correct.
- Numbers checked against stdout v7: 159–256 (l.352); 5×10⁴ / 5×10⁵ (l.353); 401–663, 385–647, ×31–52 (l.346–350);
  587–975 (l.346); 270–297 / 392–419 (l.358); 310–370 (l.343–344, 312–372); 706/684/641 and 767/749/695 (l.308–310,
  quoted as 705–640 (770–695) as in STR); 710 (790), 1,026 (l.356); 4,616 / 6,001 (l.206); 4,019 + 434 + 156 =
  4,609, 1.3 × 4,609 = 5,992 (python3); calendar table = STR §11.2 three-variant table.
