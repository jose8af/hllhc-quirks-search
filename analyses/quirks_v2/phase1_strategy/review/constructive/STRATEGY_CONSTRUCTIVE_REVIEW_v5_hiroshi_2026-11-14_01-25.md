# Constructive review: Phase 1 STRATEGY v5 (quirks v2), review cycle 5

Reviewer: Hiroshi (constructive), 2026-11-14 01:25. I am new to this panel and saw no earlier cycle. I follow
`agents/constructive_reviewer.md` (prompt template, honest-framing check, escalation to A) and the cycle-5 scope set
by the cycle-4 arbiter (`STRATEGY_ARBITER_v4_greta_2026-11-14_00-25.md` §9). Under that scope a new finding is raised
only if it is a regression, a factual error in a number shown to the user, or a genuine A. Under my brief, B means
"would mislead the human at Gate A or weakens the analysis".

**Artifact.** `outputs/STRATEGY_gunnar_2026-11-14_00-50.md` ("v5", 2,943 lines; line numbers below are v5's),
`COMMITMENTS.md` ("COM"), `outputs/budget_stdout_v5.txt` ("stdout", with its line numbers).

**What I read.** In full: the agent definition, `AGENT_RULES.md`, the study and phase `CLAUDE.md`, the cycle-4
verdict, v5 §0 (l.1–117), §4.4 (l.699–1082), §4.6 (l.1193–1260), §11–§13 (l.2448–2943). Skimmed: §4.7 head, COM
change tables and ST-1/B1-f rows, `FIX_REPORT_cycle4_gunnar.md` (its claims checked independently, not trusted),
PLAN l.105–127 and l.494–521, `LOG.md` l.18–80, the summaries of FEAS_A/B/C.

**My own checks.** (i) I re-ran `python3 -I phase1_strategy/src/strategy_budget.py` niced on einstein (standard
library, 16.7 s): the output is **byte-identical** to `budget_stdout_v5.txt` (`diff` empty). (ii) Grep of every
user-facing budget/calendar number across v5 and COM. (iii) Standard-library arithmetic for the new items (session
log). No sub-agents, no git, nothing heavy.

**Verdict of this review: not yet, two short text fixes (0 CPU-h).** R1–R5 are all RESOLVED. **0 Category A;
2 Category B (new, both Gate-A framing in Q2/Q4, one clause each); 10 Category C.** The two B items are suitable for
the "short focused fix verified by the arbiter" of the cycle-4 verdict §9; they do not need another full panel.

---

## 1. Verification of R1–R5

| # | status | where in v5 | quoted phrase | my check |
|---|---|---|---|---|
| **R1** headline | **RESOLVED** | §0 point 3 l.55–61; "Expected" l.63–89; leading sentence l.91–94; Table 4.4c l.946–952; scenario text l.959–974; §4.4 pt 4 l.770–772; pt 5 l.852; l.991–993; §11.7 rule 1 l.2702–2703; Q2 l.2743–2764; §12.5 pt 3 l.2867–2870 | "by v1's own counts the default plan's background at R08–R09 is led by hard-scatter conversions, ≈ 10⁴ events, with a reach of ≈ 270 GeV at the 84 % edge (median ≈ 315; ≈ 390 GeV if the background were known exactly), and the day-15 rule is expected to pause the study before production" | The leading sentence and Q2 are the arbiter's §5.2/§7 texts word for word, with the printed values: (α1′) B₅₀ 9,929–10,193, median 317–314, 84 % edge 273–270, fixed B 394–392 (stdout l.318–322, 327); P(≥ 2) 7.2×10⁻⁴ / 2.0×10⁻³ (l.285); mapping extended to (621.5, 243) (l.277); e^(±1) rows (l.324–325) match Table 4.4c l.948; m_H = 1000 counted 2,299 / 168 / 415 [369] (l.305) matches l.943; Z(νν) conversion m_H 1.56×10³, pilot 326 (l.342) matches l.771–772 and l.852. "therefore weak" is gone (l.959–962). "realistic branch" survives only in the §13.3 history row (l.2904); "promotion credit": 0 hits; "below 393": 0 hits. Three Q2 options present with time, CPU and paper. |
| **R2** Q3 annex | **RESOLVED** | annex l.2827–2829; Q3 l.2771–2774 | "route 5: promotion model not submitted"; "route 6: S_CKF NOT TESTED"; "floor N_MJ × 1.14/100 = **4.6×10³ events**" | The three rows carry the arbiter's columns; the route list adds "B4-e (… ≈ 4.6×10³ events) … the promotion model not submitted; S_CKF not tested" and the (β) clause "705–640 GeV at the 84 % edge … if the promotion model is submitted" (stdout l.327: 706 / 641). |
| **R3** pilot vs code | **RESOLVED** (C residue, H-C8) | §4.4 pt 5 l.847–850; pt 4 l.817; §11.3 l.2543; §11.4 l.2595; §11.7 l.2683–2697; stdout l.215 | "classified by channel (i) as its first Phase-3 task … provisionally by day 7 and with the frozen hand-over variant by day 12"; "at the latest by day 14" | Consistent: the pilot is generated in Phase 2 (days 0–5, channel (iii)), the classifier is the first task of channel (i) from day 5 (§11.3 "classification of the pilot's records (by day 7)"), the day-7 projection uses the v1-based pile-up rows because the occupancy model's R04–R05 inputs exist only by day 14 (l.2693–2696), the per-k comparison runs by day 14. Storage 51.7 GB printed and in the 469 GB total. Residue (C): the hand-over variant used to *generate* the pilot's DIF/NI hits is fixed before the Phase-3 comparison; the 7 CPU-h near-pass overlays are still booked in Phase 2 (stdout l.39) but made after the day-7 classification. |
| **R4** S_CKF samples | **RESOLVED** | l.757–763; Df-9 l.2809; COM B1-f l.127 and change row l.32 | "for DIF on the enriched test overlays with their weights … for NI by the rung split, derivation R04, test R05; for each SM process on its hit-level halves" | The arbiter's text verbatim, plus the sentence about conditioning on the no-pile-up class. The ceiling-test paragraph (l.778–783) keeps "only on unbiased samples": consistent. |
| **R5** eleven paired passes | **RESOLVED** | stdout l.61, l.123, l.126, l.163–165, l.202; §4.4 l.798; §4.0 l.435; §11.2 l.2491–2515; §11.6 l.2656–2660; Q4 l.2779–2787; COM l.39, l.202 | "1,000 test-half events of **each of the fifteen SM processes**"; "For SM processes H′ may exceed H by orders of magnitude" | Row 35.78 CPU-h; reduced 4,452.9 + 156.5 = 4,609.4; threshold 5,992; MUST only 4,176 / 5,429; full 5,123 / 6,660; envelope 6,759 / 8,787; all guesses doubled 5,987; critical path 2,489 CPU-h = 14.3 d; calendar 57.8 / 56.9 / 58.1 d. **Identical in §0 (l.99–112), §11.2, §11.3 (l.2546, 2553, 2570), §11.6, Q4 and COM ST-1.** "closest in topology": 0 hits. Q4 "39 + 36 = 75" = stdout 39.1 + 35.78. Stale 4,574 / 5,946 / 57.6 only in history rows (l.2515, 2915, 2919, COM v4 change table l.56). |

**Adopted C items.** Spot-checked G-C1 (§0 l.99–101 uses the printed 4,609 / 4,966 / 5,123), N-C1 (Q4 l.2780–2781),
N-C4 (Q2 "≈ 2 days of turnaround"), N-C6 (Df-8 l.2808), N-C11 (§11.3 ends at 57.8, l.2553), G-C9 (l.2715–2716),
G-C2 (Df-10 "4.7–4.9 %"), G-C11 / G-C3 (COM change rows l.36–37). All present.

---

## 2. The Gate-A section read as the human will (§12.1 alone)

| question | self-contained? | one-line answer? | default sensible? | alternatives costed (CPU-h, days, reach)? | numbers = rest of v5? |
|---|---|---|---|---|---|
| Q1 | mostly (what "six v1 signal counts that are also v2 candidate efficiencies" means needs §4.1) | yes | yes | CPU 14 in all; days 0; physics cost stated | yes |
| Q2 | yes for the expected case and upside; **no** for "does the upside avoid the pause" (H-B1) and "is the veto's gain known" (H-C4) | yes | yes (pause and ask is the reversible choice) | (a) ≈ 2 d, 156 CPU-h; (b) 0 / 0; (c) days not estimable, CPU inside allowances; papers named | yes (stdout l.318–327) |
| Q3 | yes with the annex | yes | yes | +680 CPU-h (100–1,230), +3.9 d; reach under default (β) | yes |
| Q4 | the labels [DP1] [DP2] [DP4] [DP5] are not explained in §12.1 (H-C7) | yes | yes | MUST only 4,176 / 57 d; full 5,123 / 58 d; envelope 6,759 | yes, **but the 58 days exclude the expected day-15 pause** (H-B2) |
| Q5 | yes | yes | yes | +47 CPU-h, +1.8 d | yes |
| Df-1…Df-10 | yes, technical | — | yes | CPU-h and days where they exist | yes |

Q2 against the four points of my brief:
- (i) *What is expected and why.* What: yes. Why: Q2 says "By v1's own counts" but not which counts; the reason
  (86 → 13 → 2 conversions per 500 events, a fall of ×6.5 per width step against ×200–340 for pile-up) is in §0
  only. One clause would make Q2 self-contained (H-C5).
- (ii) *Upside.* Yes, at the 84 % edge with medians.
- (iii) *What each option commits the human to.* Time, CPU and paper are named for (a), (b), (c). Two gaps: the
  reach of the (b) paper is quoted as "≈ 270–390 GeV", the statistics-only range, while two lines above Q2 says
  "below 200 GeV with a 20 % systematic width", i.e. at the existing bounds (H-C3); and the human is not told that
  the pause also fires in the first upside branch (H-B1), so the default (a) costs its turnaround in nearly every
  branch v5 tabulates (H-B2).
- (iv) *The veto's gain is unmeasured.* Not stated. The upside sentence puts "a conversion-removing conditional
  (vertex veto B3-b, fit probability) … tested close to where it is applied" in the same clause as the 420–455 GeV
  range, which reads as if the veto would give that range. Its rejection is unknown, and it must remove ≥ 97 % of the
  conversions to reach the (α1) conversion level (H-C4).

Q4 and the decision points: the human sees "58 days (against your 2–4 weeks; 43.5 days have no critical-path
production …)". That is plain. The decision points are not listed in §12.1: day 5 appears only as "the day-5 or freeze
re-projection may trigger the stop rule" (Q4), day 7 only as "(preliminary at day 7)" (Q2), day 12 only inside Q5 and
not as a decision point, day 15 in Q2. A human reading §12.1 alone would not know what day 7 and day 12 can change.
The package below adds a decision-point card (this is the arbiter's deferred N-C2, an orchestrator task).

---

## 3. Findings

### Category A
None. Nothing in v5 is a physics error, a tautological validation or a hidden problem. The expected branch leads,
the upside is labelled, and every reach number is marked ESTIMATE on v1 placeholder efficiencies.

### Category B (new; both one-clause text fixes, 0 CPU-h)

**H-B1. Q2 (and the §0 "Expected" paragraph) suggests that the first upside branch avoids the pause. By v5's own
numbers it does not.** Q2 l.2747–2750: "Upside: if the conversions fall like the pile-up background, or a
conversion-removing conditional … is tested close to where it is applied, ≈ 420–455 GeV …". That is (α1) without
credit, B₅₀ = 587–975 events (Table 4.4c l.946; stdout l.312, 314), above the day-15 class B₅₀ ≤ 300 (l.2699–2702).
v5 says so itself at l.993 ("(α1) without credit is above it too"), and the DIF part alone is 385–647 events
(stdout l.286, 288). Even a perfect conversion veto leaves the pause in force unless DIF earns a credit or falls faster
than the pile-up background. The pause is avoided only in the (β) and empty-ceiling branches, i.e. if the pilot's
own ceilings at R08–R09 are close to empty. On the central question of the gate, the human would read "the pause is
expected, but the upside avoids it", while v5's own numbers say the pause fires in every (α) branch.
*Fix (Q2, after "an upper edge."):* "The day-15 pause fires in the (α1) branch too (B₅₀ 587–975, of which decays in
flight alone are 385–647), so a conversion veto alone does not avoid it; only the (β) and empty-ceiling branches (B₅₀
≤ 300) do." Add the same clause to §0 l.83–84 after "tested close to where it is applied".

**H-B2. Under the recommended Q2 (a), the expected pause costs ≈ 2 days. The 58-day calendar of Q4 does not contain
them.** The calendar items (stdout [7] l.187–198; §11.3 l.2542–2553) have no day-15 turnaround. Q2 (a) says
"production waits for your answer (≈ 2 days of turnaround)", and §0, §11.7 rule 1 and Q2 call that pause the expected
branch. So the human approves, in Q4, a calendar that the default plan expects to overrun by ≈ 2 days (57.8 + 2 ≈ 60),
and the overrun would then be "reported under D6" as if it were unforeseen. *Fix (Q4 and §11.3 calendar paragraph):*
"58 days without the day-15 pause; ≈ 60 days in the expected branch under Q2 (a) (≈ 2 days turnaround); a redesign
under Q2 (c) adds its time, reported at day 15." The alternative fix, putting the 2 days into the approved calendar, is
equally acceptable. The point is that the human sees the number.

### Category C

**H-C1 (the constructive question of my brief: the first two weeks; recommendation for the orchestrator and the
Gate-A package).** *Is the cheapest decisive measurement scheduled as early as it can be?* Mostly yes. The decisive
number for the conversion term is the pilot's own-hit ceiling H(r) of the 2.3×10⁶ no-pile-up Z(νν) events at R05–R09
with its fall per width step (§4.4 pt 5 l.844–855). It is generated in days 0–5 and classified by day 7, and the
pilot expects ≈ 3×10² conversion counts at R08 if v1's fall holds (stdout l.342). That is decisive by day 7. Three
things are missing, and they can be added at zero or small cost:
1. *Escalate at day 7, not only at day 15.* For the SM terms the day-15 projection reads the **same** pilot H as the
   day-7 one: no SM hit-level sample exists before the freeze (l.2689–2690), so no SM credit (S_CKF, π_k,
   conditionals) can enter by day 15. What changes between day 7 and day 15 is the final classification, N_trig from
   the MET model (day 12) and the pile-up row. If the day-7 B₅₀ exceeds the class by a wide margin (proposal: ≥ 10×,
   i.e. B₅₀ ≥ 3,000), the orchestrator puts Q2's choice (b)/(c) to the user at day 7. Days 7–15 are then not spent
   waiting, and a redesign under (c) starts eight days earlier: up to ≈ 8 days off the (c) calendar, 0 CPU-h. The
   binding rule stays at day 15.
2. *Measure the veto's handle on the pilot records (0 CPU-h).* The records are kept in full (R3) and carry truth. In
   channel (i), days 7–12: report H(r) split by truth origin class (conversion, V⁰, prompt pair, other), and the
   fraction of conversion-attributed passing and near-pass configurations at R05–R07 that carry a reconstructed
   two-prong vertex above a trial radius. Label it a development number, not a credit, and make it a day-15 input.
   This is the number Q2 (c) depends on, and v5 today produces it only in 4a ("B3: unknown until the pool exists",
   annex route 3 l.2825).
3. *Look at the fall with pile-up and the v2 chain before the freeze (≈ 7 CPU-h, inside the 100 CPU-h enlarged
   development allowance, stdout l.49).* The four sub-topology overlays (γ among them) are 4a samples (stdout l.56).
   1,000 γ development overlays with seeds disjoint from 4a (1,000 × 25.2 s = 7.0 CPU-h) would give, by Table 4.4b
   (l.1033), ≈ 172 / 26 attributed counts at R05 / R06. That checks v1's ×6.6 fall on the Linux chain and with v2's
   attribution rule, and gives the veto's rejection with pile-up at R05–R06, by day 12. This follows the precedent of
   the 1,000 DIF development overlays (sample 13a).
v5 as written wastes no MUST effort: everything in days 5–15 (estimators, MET model, occupancy model, S1 propagation)
is needed under every Q2 option, and the PREREG drafting from day 12 is the only work a redesign would partly redo.
That is why this is C and not B.

**H-C2. The day-7/15 number will look much larger than the "≈ 10⁴" headline. Say why in Q2 and in §4.4.** (α1′) uses
v1's attributed counts *after CKF* (l.766, stdout l.342). Under the default Df-9, H is counted on all own hits before
CKF, H = H_CKF/(1 − ε_pair), with ε_pair assumed 0.8–0.98 and not measured (l.768–770). No SM S_CKF can be tested
before production (it is tested on the 4a hit-level halves, l.760). So the pilot's conversion m_H for Z(νν) is
expected at ≈ 1.6×10³–1.6×10⁴ rather than 326, and the projected conversion term at ≈ 5×10⁴–5×10⁵ events rather than
9.5×10³ [E: 326 and 9,530 × 1/(1 − ε_pair) for ε_pair = 0.8–0.98; my arithmetic, session log]. For the ≈ 14 % of
N_trig in processes without an evaluable S_CKF test, the factor remains in the final background as well (annex route
6, l.2828). Direction: the pause becomes more certain and the (b) reach lower, so the decision does not change. But the
human should not be surprised by a day-7 B₅₀ of order 10⁵. Fix: label l.771–772 and l.852 "after CKF; ×1/(1 − ε_pair)
on all own hits (Df-9)", and add one clause in Q2.

**H-C3. Q2 option (b): give the realistic low end in the option itself.** "(≈ 270–390 GeV as above)" is the
statistics-only range. A simulated conversion background of 10⁴ events carries at least material and
conversion-modelling uncertainty, and at σ_ln = 0.2 PLAN l.122 gives below 200 GeV, i.e. at the existing bounds
(≲ 180 GeV, PLAN l.116). Suggested: "(≈ 270–390 GeV statistics-only; below 200 GeV, at the existing bounds, with a 20 %
systematic width)".

**H-C4. Q2: state that the veto's rejection is unmeasured and how large it must be.** To bring the conversions from
9,530 to the (α1) level of 183–308 events, a veto must remove 96.8–98.1 % of them [E: 1 − 308/9,530, 1 − 183/9,530].
With H-B1, it does not avoid the pause by itself.

**H-C5. Q2: one clause for the "why"**: "(v1 counted 86 → 13 → 2 conversions per 500 events at R05–R07, a fall of
×6.5 per width step, against ×200–340 for the pile-up background; a pile-up-like fall is rejected at p ≈ 10⁻³)".

**H-C6. "≈ +25 GeV" for a doubled pool (Q2 last line, l.2764) is not printed by the script.** The summed floor at
twice the pool is printed (6.3, stdout l.233, and §4.4 l.911), but the reach is not. The rule of the cycle-4 verdict §6
is that every number shown to the user comes from a printed line. Print it in [9b], or tag it [E, unprinted].

**H-C7. Q4: gloss the labels in one line each** ([DP1] reduced B5, −358 CPU-h; [DP2] reduced B6, −155 CPU-h; [DP4] no
S4/S5; [DP5] Herwig at generator level only after an install attempt). Without §11.5 the human cannot tell what is
being approved.

**H-C8. Residue of R3 (scheduling hygiene).** (a) The pilot's DIF/NI hits are generated in days 0–5 with one
hand-over variant, while the variant is frozen in Phase 3 (§4.4 pt 2 l.720–721, no date given). If the other variant
is frozen, either the records must hold the Geant4 parent crossings or the 18.8 CPU-h of DIF/NI pilot events (stdout
l.36–37) are regenerated. State which, and date the hand-over freeze "by day 12" in §4.4 pt 2. Z(νν), and so the
conversion question, is unaffected. (b) The 1,000 near-pass overlays (7.0 CPU-h) are booked in Phase 2 (stdout l.39;
§11.3 "the pilot (61)") but are made after the day-7 classification, so they belong in Phase 3. (c) Classifying the
6.3×10⁶ stored events is not costed. It is small at a few ms per event, but it should be named inside the Phase-3
development allowance.

**H-C9. Stale label in the script.** stdout l.121 prints "v4 approved figure = total + day-15 reserve" above the v5
numbers. Cosmetic.

**H-C10. The pilot runs before decision point 1.** The pilot (days 0–5, channel (iii)) uses the Linux chain while C1
decides at day 5 whether the chain reproduces v1. Say in §11.7 that the day-7 projection is conditional on C1 PASS for
the no-pile-up family (C′₀). If that family fails, the pilot is re-read, or re-run (61 CPU-h, idle capacity), after
remediation.

---

## 4. Final judgment

**Is v5 a sound, honest, executable basis to put to the human at Gate A? Not yet, by two clauses.** The design is
stable, the arithmetic reproduces exactly, R1–R5 are resolved, and the expected branch leads honestly. Blocking list:
1. **H-B1**: Q2 and §0 must say that the pause also fires in the (α1) upside (B₅₀ 587–975; DIF alone 385–647), so a
   conversion veto alone does not avoid it.
2. **H-B2**: Q4 and §11.3 must show the ≈ 2-day turnaround of the expected day-15 pause under Q2 (a): 58 days without
   it, ≈ 60 in the expected branch.
Both are 0 CPU-h text fixes that the arbiter can verify directly. H-C1 (escalation at day 7, veto handle on the pilot
records, 7 CPU-h of γ development overlays), H-C2 and H-C3 are the C items I recommend most strongly for the Gate-A
package. The package below already includes the B and C items as statements derived from v5's own numbers.

---

## 5. Gate-A package (final text, at most 3 pages)

> **GATE A — quirks v2: strategy, benchmarks and schedule for your approval**
> Source: `analyses/quirks_v2/phase1_strategy/outputs/STRATEGY_gunnar_2026-11-14_00-50.md` (STR), `COMMITMENTS.md`,
> `phase1_strategy/outputs/budget_stdout_v5.txt` (all numbers). Every reach is an ESTIMATE on v1 placeholder
> efficiencies (best Λ per mass, PLAN Table reach); no v2 signal efficiency has been computed.
>
> **1. Headline**
>
> **Expected:** by v1's own counts, the background of the default plan at the R08–R09 selections is led by
> hard-scatter photon conversions, **≈ 10⁴ events, with a reach of ≈ 270 GeV at the 84 % edge** (median ≈ 315;
> ≈ 390 GeV if that background were known exactly; **below 200 GeV, at the existing bounds of ≈ 180 GeV, if it
> carries a 20 % systematic width**). Why: v1 counted 86 → 13 → 2 conversions per 500 events at R05–R07, a fall of ×6.5
> per width step, while the pile-up background falls ×200–340. A pile-up-like fall is rejected at p ≈ 10⁻³. The
> day-15 decision rule is therefore **expected to pause the study before production** (Q2).
>
> **Upside**, as 84 % edge (median): ≈ 420–455 GeV (470–500) if conversions and decays in flight fall like the
> pile-up background (this branch also pauses at day 15: B₅₀ 590–980 > 300); ≈ 705–640 GeV (770–695) if Z(νν) is
> tested and the other ceilings count 10–100 events; ≈ 710 GeV (790) with every ceiling empty, an upper edge; 1,026 GeV
> for a negligible background. The day-7/15 projection reads the no-credit ceiling (all own hits, before CKF), so it
> may show B₅₀ of order 10⁵ even if the eventual background is ≈ 10⁴ (STR §4.4 pt 4; factor 1/(1 − ε_pair), assumed
> 5–50).
>
> **2. What Phase 1 established**
> - *The chain runs on the Linux cluster with no source build* (pyacts 48 wheel; v1 smoke tests pass; FEAS_A).
>   MG5 2.9.22 + Pythia 8.313 reproduce v1's LO cross-section (92.33 ± 0.07 vs 92.26 ± 0.04 fb, z = 0.91). NLO
>   K-factors cost ≈ 2 CPU-min per mass (K = 1.165 at 200 GeV). Geant4 11.4.3 installs node-locally in ≈ 3 min (FEAS_B).
>   The job runner passes kill/resume, memory and I/O-error tests under Argo and SSH (FEAS_C).
> - *Measured unit costs (maxwell/landau, 4 jobs per node):* PU-200 event + 4 finder trials 60.4 s; PU-200 hit-level
>   event 25.2 s; ρ = 2 event 206 s; no-pile-up single interaction 11.5 ms; Pythia shower 21 ms; Geant4 gun 0.13 ms;
>   finder pass 11.7 s; pyhf 1,000 toys 652 s; Argo overhead 16.8 s per job (SSH 2.4 s).
> - *Incidents that changed the operating rules (LOG.md):* 15:12, einstein ran out of memory, killing the orchestrator
>   and three executors, with cajuela I/O errors 15:12–15:20. Since then: 10 GB memory cap for all agents, nothing
>   heavy on einstein, about 3 concurrent agents. 15:20: a pixi install over the sync NFS home ran at ≈ 1 MB/s and
>   slowed the lab, so now one install at a time from a worker, job work on per-worker scratch, and Geant4 on local
>   scratch. Two workers carry graphical sessions, which leaves 10 usable slots off-hours.
> - *Design:* each background term is counted on samples large enough to count it where possible, closed on rungs and
>   samples it was not derived from, and otherwise kept as a tested ceiling or a bound. With zero counts everywhere,
>   the sample-size floor is ≈ 13 events.
>
> **3. Your five decisions** (answer in one line, e.g. "Q1 ●; Q2 ●; Q3 ●; Q4 ●; Q5 ●"; ● = recommended)
>
> **Q1, C1 blinding exception.** May the C1 reproduction compare six v1 signal counts that are also v2 candidate
> efficiencies, before the closure verdicts? ● Yes, sealed (PASS/FAIL only until Gate B). Alternatives: all open and
> disclosed; or the six dropped. 14 CPU-h, 0 days in every option.
>
> **Q2, the deliverable if the background is large (the expected case).** If the day-15 projection exceeds B₅₀ = 300
> events (or both pile-up estimators miss their cap):
> ● (a) Pause and ask you at day 15. Production waits ≈ 2 days; the 156 CPU-h reserve tests the leading term at
> R06–R07; you then choose (b) or (c).
> (b) Proceed now with the measured background: 0 CPU-h, no delay. Paper: the plan's "real background" outcome, with
> reach ≈ 270–390 GeV statistics-only and below 200 GeV with a 20 % systematic width.
> (c) Redesign before the freeze with a conversion-removing conditional (displaced-vertex veto, fit probability). Its
> rejection is **not measured**: it must remove ≥ 97 % of conversions to reach the 420–455 GeV branch, and it does not
> lift the pause by itself (decays in flight alone are 385–647 events). Time: not estimable now, reported at day 15.
> CPU inside the development allowance and the reserve. Paper: the "middle" outcome if it works, otherwise (b).
> If the projection is ≤ 300 events (reach ≈ 560 GeV or more): production proceeds, and the paper is the "middle"
> outcome, "target not met: sample-size limited". A doubled pool (+665 CPU-h, ≈ +3.8 days) helps only if the
> ceilings are empty.
>
> **Q3, exception to brief D4.** For every MUST closure criterion that ends untested (eight proxied SM processes, the
> three additions, a fluctuation ≈ 30 %, the cap rule, conditionals, multijet factorisation, which alone sets a
> ≈ 4.6×10³-event floor if it fails, pile-up crossing at depth, the promotion model or S_CKF not tested), may the term
> enter at its tested ceiling, labelled "no credit", with the selection eligible? ● Yes. Alternatives: comply where
> costed (≈ +680 CPU-h, 100–1,230; ≈ +3.9 days); or strict, which makes "closure fails" a likely paper.
>
> **Q4, budget, calendar, stop rule.** ● Approve **4,609 CPU-h** (MUST 4,019 + reduced SHOULD 434 + 156 day-15
> reserve) and **58 days** (≈ 8 weeks; ≈ 60 days in the expected branch with the Q2 (a) pause), with: [DP1] B5
> sideband reduced (−358 CPU-h); [DP2] B6 detector variations at 4 points (−155 CPU-h); [DP4] S4/S5 not included;
> [DP5] second hadronisation model at generator level after an install attempt. Stop and ask at **5,992 CPU-h**
> (1.3×). 1,378 CPU-h rest on unit costs never measured: if all doubled, 5,987. The day-5 or freeze re-projection may
> therefore stop the study. The 2–4-week target (D6) is not reachable: 43.5 days contain no production. Alternatives:
> MUST only, 4,176 CPU-h / 57 days (threshold 5,429); full SHOULD, 5,123 / 58 days (6,660); pre-approved envelope 6,759
> (8,787).
>
> **Q5, truth-level signal before the hash.** May Stage 2 and the string propagation (47 + 266 CPU-h) run before the
> pre-registration hash? They depend on the MET model, trigger and generator cut (frozen by day 12), not on any
> selection. ● Yes, in idle capacity, 0 days. Alternative: after the hash, +47 CPU-h and +1.8 days.
>
> Ten technical defaults (Df-1…Df-10, STR §12.1) apply unless you override them. For example, Df-1: 2,000 signal rows
> per point (4,000: +827 CPU-h, +4.7 days).
>
> **4. Budget and calendar (proposed variant)**
>
> | | CPU-h | days after Gate A |
> |---|---|---|
> | Phase 2 (C1, C2, S2, P1, pilot) | 506 | 0–5 |
> | Phase 3 (development, S1 string 266) | 580 | 5–17 |
> | freeze + ITERATE allowance | — | 17–21 |
> | Phase 4a: MUST 2,737 + reduced SHOULD 434 + reserve 156 (of which 2,489 on the critical path) | 3,327 | 21–35.3 production |
> | 4a analysis and review; S1 chain, B5, B6 signal arm off the critical path | (in the 3,327) | 35.3–41.8 |
> | 4b, Gate B (2-day turnaround) | 118 | 41.8–48.8 |
> | 4c; Phase 5, Gate C | 68; 10 | 48.8–57.8 |
> | **total** | **4,609** (threshold 5,992) | **57.8** (+≈ 2 if the day-15 pause fires) |
>
> Storage ≈ 470 GB on cajuela (670 at the pre-merge cap), against the 1.5 TB budget.
>
> **5. Decision points**
> - **Day 5:** does the v1 chain reproduce on Linux (C1) and does the finder pass (C2)? First re-projection of CPU
>   with measured unit costs: this is where the stop rule may fire. A failed family delays everything day for day.
> - **Day 7:** preliminary projection from the pilot's ceilings (2.3×10⁶ Z(νν) and 10⁶ DIF/NI no-pile-up events),
>   reported in STATUS.md. It shows whether the conversion term is ≈ 10⁴ or more. Recommended: if B₅₀ ≥ 10× the class
>   (≥ 3,000), Q2 is put to you then rather than at day 15.
> - **Day 12:** MET model and N_trig of the additions; final classification of the pilot; pool re-allocation;
>   generator-cut decision. These can change the size of the floors and the conversion share.
> - **Day 15 (binding):** the projection for every term. If B₅₀ > 300 or both pile-up estimators miss their cap, the
>   study pauses (Q2). The reserve is spent by rule 3, and estimators above their cap are redesigned or declared "not
>   submitted".
> - **Freeze (days 17–19):** second CPU re-projection, the pre-registration hash, and you are notified. **Gate B
>   (≈ day 49):** background verdicts before any signal efficiency. **Gate C (≈ day 58):** the paper.
>
> **6. Top risks**
> 1. The conversion background (≈ 10⁴ events, expected): the reach is near or below the existing bounds unless a
>    conversion veto is measured to remove ≥ 97 % of conversions and decays in flight earn a credit.
> 2. CPU: 1,378 CPU-h on guessed unit costs; the stop rule may fire at day 5 or at the freeze.
> 3. Development effort: Phase 3 has 30 channel-days against PLAN's 35–50 person-days. Each 3 channel-days more
>    lengthen Phase 3 by one day.
> 4. Pile-up at depth: one estimator beyond R07. If both estimators fail, no validated pile-up term remains.
> 5. Infrastructure (two incidents on day one); Geant4–Fatras hand-over; MET model sourcing (B4-b infeasible → stop).
>
> **7. Files.** STR §0 (summary), §4.4 Table 4.4c (projection per outcome), §11 (schedule, stop rules), §12.1
> (questions, annex to Q3); `COMMITMENTS.md`; `budget_stdout_v5.txt` (every number);
> `phase1_strategy/outputs/feasibility/FEAS_{A,B,C}_*.md` (benchmarks); `review/arbiter/` (cycle verdicts); `LOG.md`
> (incidents and constraints).

*Package notes for the orchestrator.* Q2 (c) "≥ 97 %" and the "+≈ 2 days" are my arithmetic from v5's printed values
(H-B1, H-B2, H-C4). The day-7 escalation (H-C1.1) is a recommendation: include it only if the arbiter adopts it. If
not, delete that sentence from the day-7 bullet. The "order of 10⁵" sentence (H-C2) rests on the assumed ε_pair
0.8–0.98 (STR l.768–770, not measured). The table rows sum to 4,609 (506 + 580 + 3,327 + 118 + 68 + 10; stdout l.94–100,
l.123). Of the 3,327 CPU-h of 4a, 2,489 are on the critical path (stdout l.202).
