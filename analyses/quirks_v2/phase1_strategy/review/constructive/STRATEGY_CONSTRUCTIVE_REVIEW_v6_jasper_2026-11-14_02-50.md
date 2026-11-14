# Constructive review: Phase 1 STRATEGY v6 (quirks v2), review cycle 6

Reviewer: Jasper (constructive), 2026-11-14 02:50. I am new to this panel and saw no earlier cycle.
Role: `agents/constructive_reviewer.md`. Being constructive does not mean being lenient, and I applied the
honest-framing check.
Artifact: `phase1_strategy/outputs/STRATEGY_ingrid_2026-11-14_02-20.md` ("v6"; "l." means a line of v6). I also used
`QV2/COMMITMENTS.md` ("COM") and `outputs/budget_stdout_v6.txt` ("stdout").

**Scope.** The scope is the one the cycle-5 arbiter set (`STRATEGY_ARBITER_v5_hugo_2026-11-14_01-55.md` §9, "AV5"). I
read the §0 leading sentence and §12.1 Q2 and Q4 as the human will read them. I then wrote the final Gate-A package.
New findings are A only for a genuine error, and B only if the text would mislead the human at Gate A. Everything
else is C.

**What I read.** These sections of v6, in full:
- §0 (l.31–130) and Table 4.0 (l.328–360);
- §4.4 points 4–5, Table 4.4c and the scenario text (l.770–1020);
- §4.6 (l.1214–1281), §9 (l.2386–2404), §11 (l.2470–2751), §12 (l.2754–2930) and §13.5.

Also read in full: AV5, `FIX_REPORT_cycle5_ingrid.md`, `LOG.md`, and §3 and §5 of the cycle-5 constructive review.
Read in part: COM rows ST-1 and TG-1; the brief `prompt.md` §3 (D1–D10) and l.362 (the 3-page package rule); the PLAN
reach table (l.108–127) and outcome table (l.495–516); and the summaries of FEAS_A, FEAS_B and FEAS_C.

**My own arithmetic.** One niced run, standard library only. It loads the strategy's script with `runpy`
(scratchpad `jasper_check.py`; session log `logs/constructive_jasper_2026-11-14_02-50.md`). It checks one wording
question (Jp-C2). None of its numbers enters the package.

**Rules followed.** No git, no sub-agents, nothing heavy. I wrote only this file and the session log.

---

## 1. T1–T3 as the human reads them

### 1.1 Status

| item | status | where, quoted |
|---|---|---|
| **T1** (the expected reach with the strategy's own width) | **RESOLVED** | Leading sentence, l.101–107: "With the normalisation uncertainty this strategy itself assigns to that background (≈ 0.17, the generator difference of §4.7) the reach is below 243 GeV, at or near the existing bounds of ≈ 180 GeV; the ≈ 270–300 GeV at the 84 % edge (≈ 390–420 GeV for a background known exactly) hold only for its counting width alone." §0 "Expected", l.64–72: "≈ 0.7–1.0×10⁴ events (v1's N_trig-weighted and maximum photon rates, 0.255 and 0.379 per event)". Q2 stem, l.2772–2775: "With the normalisation width this strategy assigns to that background (≈ 0.17, §4.7) the reach is below 243 GeV, at or near the existing bounds". Q2 (b), l.2788–2791: "expected below 243 GeV … In the expected case this paper reports no mass reach beyond the existing bounds". §12.5 point 3, l.2918–2919. On wording: the phrase "statistics-only" is now attached to every 270–420 GeV figure in §0, Q2 and §12.5, and to the upper branches (l.79–81, l.2777). |
| **T2** (nothing in the (α) family, and no veto alone, avoids the pause) | **RESOLVED** | §0 "The pause.", l.90–93: "The pause fires in the first upper branch too ((α1) without credit, B₅₀ 587–975, of which decays in flight 385–647), so neither a steeper conversion fall nor a conversion-removing conditional … avoids it on its own." Q2 stem, l.2778–2779: "This branch also pauses at day 15 … so a conversion veto alone does not avoid the pause." Q2 (c), l.2795–2797: "It works if the projected B₅₀ is at most 300. That needs the conversions reduced by ×31–52 (96.8–98.1 %) **and** the decays in flight (385–647 events) reduced by a credit or a faster fall. The veto's rejection has not been measured." §4.4, l.1013–1014. |
| **T3** (the calendar includes the expected pause) | **RESOLVED** | Q4, l.2825–2827: "**60 days** (57.8 without the day-15 pause; under the recommended Q2 (a) the pause is the expected branch and costs ≈ 2 days of turnaround, so the approved calendar includes it; a redesign under Q2 (c) adds its own time, reported at day 15)". §0 Calendar, l.119: "60 days, of which ≈ 2 are the expected day-15 pause; 58 days without it". §11.2 l.2522, §11.3 l.2592, §11.6 l.2680–2681, COM ST-1 (COM l.209). |

### 1.2 The six checks of my brief (read as the human, §0 and §12.1 only)

| # | does the human see it without reading further? | verdict |
|---|---|---|
| (i) | Expected background ≈ 0.7–1.0×10⁴ events, led by hard-scatter conversions; reach < 243 GeV with the strategy's own width; at or near the bounds of ≈ 180 GeV; all ESTIMATE on v1 placeholders; and why (v1's 86 → 13 → 2) | **Yes.** All of it is in the leading sentence and the Q2 stem, and the "why" clause is at l.2771–2772. The §12.1 preamble (l.2759–2761) and the Q2 stem carry "ESTIMATE, v1 placeholder efficiencies". |
| (ii) | The upside, and what it would take | **Yes.** Q2 stem l.2776–2782 names each branch with its condition. The conditions are: conversions and DIF fall like pile-up; Z(νν) tested with the promotion model submitted; every ceiling empty. Each is quoted statistics-only, with the 0.17 value for (α1). Two refinements are C items: Jp-C4 (one avoiding branch may not be reachable at day 15) and Jp-C5 (the class boundary "≈ 560 GeV" is unlabelled). |
| (iii) | The day-15 pause is expected, and a veto alone would not avoid it (DIF alone is above the threshold) | **Yes**, in §0, in the Q2 stem and in Q2 (c). The script prints the same thing (stdout l.346–350). |
| (iv) | For each option of Q2: time, CPU, and the paper under PLAN §8 | **Yes.** (a): about 2 days; the 156 CPU-h reserve, inside the approved figure; then (b) or (c). (b): 0 CPU-h, no delay; the "real background" paper, expected below 243 GeV, "at or near the existing bounds". (c): time not estimable, reported at day 15; CPU inside the allowance and the reserve; the "middle" paper if it works, otherwise (b). Wording refinements are Jp-C1, C2, C6, C7. |
| (v) | The rider is optional, costed, and answerable in the same line | **Yes.** l.2802–2809: "*Optional rider (… not part of the default; answer "Q2 ● + rider" to accept)*". It gives the day-7 trigger at B₅₀ ≥ 3,000, the veto fraction on the stored pilot records (0 CPU-h) and the 1,000 γ overlays: "+7.0 CPU-h: approved 4,616, threshold 6,001". Gain: "up to ≈ 8 days earlier". |
| (vi) | Q4: 4,609 CPU-h, threshold 5,992, about 60 days including the expected pause, against the 2–4 week target; decision points at days 5, 7, 12 and 15 | **Mostly.** The budget, threshold, calendar and target are in Q4 (l.2824–2836). Days 7 and 15 are in Q2, and day 5 is in Q4 ("The day-5 or freeze re-projection may trigger the stop rule"). Day 12 appears only in the rider. No single list of decision points is visible from §12.1 (Jp-C10, C). The package's §6 supplies one. |

### 1.3 Number identity (Gate-A section = §0 = §11 = stdout)

| quantity | §12.1 | §0 / §11 / COM | stdout | identical |
|---|---|---|---|---|
| expected background | 0.7–1.0×10⁴ | §0 l.66, l.103 | l.356: B₅₀ 6,825–10,193 | yes |
| reach with w = 0.17 | < 243 | §0 l.69 | l.330–342, l.356 | yes |
| statistics-only 84 % edge / median / fixed B | 270–300 / — / 390–420 | §0 l.71: 270–300 / 315–340 / 390–420 | l.356: 270–297 / 314–342 / 392–419 | yes (rounded) |
| (α1) edge, statistics-only and with w = 0.17 | 420–455 (median 470–500); 310–370 | §0 l.73, l.80 | l.354; l.343–344: 421–455, 469–504; 312–372 | yes |
| B₅₀ of (α1); DIF alone | 587–975; 385–647 | §0 l.91 | l.346 | yes |
| conversion rejection needed | ×31–52 (96.8–98.1 %) | — | l.349–350 | yes |
| avoiding branches | (α1) + credit; (β) 705–640 [770–695]; empty ceilings 710 (790) | §0 l.75–78, l.93 | l.315, 317, 308–310, 354 | yes |
| doubled pool | median 790 → 814 | — | [9b] (H-C6 line) | yes |
| rider | +7.0; 4,616 / 6,001 | — | l.206: 4,616.4 / 6,001.3 | yes |
| approved figure / threshold | 4,609 / 5,992 | §0 l.113, l.125; §11.2 l.2513, l.2522; §11.6 l.2680–2683; COM ST-1 | l.123 | yes |
| calendar | 60 (57.8) | §0 l.119; §11.2 l.2522; §11.3 l.2592; §11.6 l.2680; COM ST-1 | l.202, l.205: 57.8 / 59.8 | yes |
| alternatives | MUST only 4,176, 59 (57) d; full 5,123, 60 (58) d; envelope 6,759 (8,787) | §11.2 l.2521–2523 | l.122–124, l.164, l.205 | yes |
| contingency; all guesses doubled | 2,150; 5,987 | §11.2 l.2556–2558 | l.162, l.165 | yes |

There is no mismatch.

---

## 2. Honest-framing question: the paths to a stronger paper, and what remains publishable

**What v6 says.** In the expected case (b) "reports no mass reach beyond the existing bounds; (c) is then the only
route in this strategy to one" (l.2789–2791). (c) needs a conversion rejection ×31–52 "**and**" a reduction of the
decays in flight, and "the veto's rejection has not been measured" (l.2795–2797). §0 l.109–111 lists "three things
[that] can improve the bounded outcome": biased generation, the conditionals and time tag, and counts in the large
samples. That list is about the *bounded* branch, not the expected one.

**What is missing from §0 and §12.1**, the two places the human reads:
- **The realistic paths to a stronger paper, stated as paths that are not demonstrated.** There are three:
  1. A pre-freeze redesign that removes about 97 % of the conversions **and** suppresses the decays in flight. (c) as
     worded covers only the first half (Jp-C1).
  2. The B3 conditionals that run in production under every option. These are the fit probability, the
     displaced-vertex veto (T2 keeps every selection with and without it, l.1783) and the time tag. Their credit is
     unmeasured. On v1's numbers the route is weak (Jp-C2).
  3. A pilot that counts far fewer conversions and decays in flight than v1 did. For DIF this includes the
     PV-placement caveat of l.982–983.
- **What remains publishable if none of these works.** The items exist in v6 but are scattered, and none is in §0 or
  Q2:
  - the thickness law with its scattering floor (P1, §4.15; Fig. 2);
  - the full hit-level chain at pile-up 200 with the signal efficiency map (S1; Figs. 1, 3);
  - the background anatomy, with the first *measured* quirk-plane background term by term (ladder Fig. 4, Table 4.4c);
  - the simulation-statistics barrier documented: v1's bounds 7.05 decades above budget, and the v2 floors
    (§0 l.36–37, Table 4.4a);
  - the data-driven sideband recipe, closed in simulation or reported as not closing (B5, §4.8 l.1427);
  - the closure tests (Fig. 5) and the reproduction package.

  PLAN §8 rates this kind of paper "still publishable but less strong" (PLAN l.509–510).

**Classification: C (Jp-C9), as content for the Gate-A package.** The human is not misled about what they approve.
§0 and Q2 (b) say plainly that the expected reach is at or near the existing bounds. The missing sentences are about
*value*, not about the outcome. Where they should go: two sentences after the leading sentence of §0 (l.107), or at
the end of Q2 (b). Proposed text:

> "Paths to a stronger paper exist, and none is demonstrated. They are a redesign that removes ≈ 97 % of the
> conversions *and* suppresses the decays in flight (Q2 (c)), the purpose-built conditionals measured in production
> (credit unmeasured), and a pilot that counts far fewer conversions than v1. If none works, the paper still contains
> the plane-thickness law, the full hit-level chain at pile-up 200, the background anatomy with the first measured
> quirk-plane background, the documented simulation-statistics barrier and the data-driven sideband recipe."

The package (§5 below) includes this text.

---

## 3. Findings

### Category A
None. No number shown to the user is wrong, and no framing hides a problem.

### Category B
None. Every point of (i)–(vi) is visible to the human from §0 and §12.1, and the numbers are identical across the
document and stdout.

### Category C (each needs 0 CPU-h; the package text already applies them)

**Jp-C1. Q2 (c) does not say whether the redesign may target the decays in flight.** (c) authorises "a
conversion-removing conditional" (l.2792). Its own success condition also needs DIF "reduced by a credit or a faster
fall" (l.2796). DIF at 385–647 is already the *favourable* reading: the pile-up fall, against v1's own 2 → 1
(l.977–980). So a "faster fall" is unlikely, and the credit is not in the scope of (c) as worded. The displaced-vertex
veto targets two-prong vertices (l.1221), and a decay in flight is a kink. Suggested addition to (c): "As worded, (c)
targets the conversions. If you choose (c), say whether the redesign may also target the decays in flight (for
example a fit-probability or shape conditional measured on the pilot's 10⁶ DIF events)." The pilot sample size is
from l.854–856.

**Jp-C2. "(c) is then the only route in this strategy to one" (l.2790–2791) is stronger than v6 supports.** Under
(b) the B3 conditionals are still measured on the pool in 4a and credited where they pass. This is annex route 3:
"B3: unknown until the pool exists" (l.2874). T2 also contains every selection with and without the veto (l.1783).
My own run [E, not printed by the script]: (α1′) with v1's pile-up fit-probability fraction 2/35 as credit and the
width 0.17 gives a median of ≈ 325 GeV, with the 84 % edge below 243. With v1's conversion conditional 2/13 it gives
below 243. So the route exists, and on v1's numbers it is weak. Suggested wording: "(c) is then the route this
strategy designs for it. The conditionals measured in production may add some reach; their credit is not measured."

**Jp-C3. "The day-7 reading counts own hits before CKF (Df-9) and may be ×5–50 above this figure" (l.2775–2776).**
No S_CKF is tested before production: for SM it is tested on the 4a hit-level halves (l.773, annex route 6, l.2877).
So the *day-15* reading is inflated in the same way, and the clause should not invite the reading that day 15 will
correct it. The cycle-5 item it implements (H-C2) said "day-7/15". Suggested: "The day-7 and day-15 readings count
own hits before CKF …". A consequence for the rider: in the expected branch the 3,000 trigger is then all but certain
to fire, which is what the rider intends.

**Jp-C4. "(α1) with fit-probability credit" is listed among the branches that avoid the pause (l.92–93,
l.2780).** The day-15 inputs of §11.7 rule 1 (l.2707–2723) list ceilings, falls, enrichments, gains and N_trig, but
no conditional credit. An untested conditional is 1 (l.789–790), and B3 credit is a 4a measurement. Unless a
conditional measured on the development or pilot samples may enter the day-15 projection, which the rule does not
say, this branch cannot be the day-15 reading under (a) or (b). Only (c), or rider part (2) as information, could
bring it before the freeze. Suggested: one clause in §11.7 rule 1 saying whether development-sample conditionals
enter the projection. If they do not, add "(a credit that only a pre-freeze conditional, Q2 (c), could bring)" to the
two locations above. Either way the default answer does not change.

**Jp-C5. "If the projection is at most 300 events (reach ≈ 560 GeV or more)" (l.2798) is the only reach figure in
Q2 without the label "statistics-only".** With w = 0.17 the m_H = 100 row is a median of 513 GeV with an 84 % edge of
454 (stdout l.345). Suggested: "(reach ≈ 560 GeV or more statistics-only; 513 [454] with the width 0.17 at
m_H = 100)".

**Jp-C6. Q2 (c) omits the signal-side risk of a veto.** §4.6 says the veto is designed without v2 signal, that its
signal efficiency is unknown until unblinding, and that "a quirk pair may itself form two-prong vertices" (l.1276–1280).
One clause in (c) would cover it: "its signal cost is known only at Gate B; T2 keeps the selections without it."

**Jp-C7. The reserve is spent twice in the text.** (a) spends the 156 CPU-h reserve by rule 3(b) (l.2784–2785).
(c), which the user may choose after (a), says its CPU is "inside the development allowance and the reserve"
(l.2794). Suggested: "inside the development allowance and what remains of the reserve".

**Jp-C8. "The first measured irreducible quirk-plane background" (l.2787).** This is PLAN's wording (PLAN l.507).
But the term that leads the expected branch, the conversions, is the *reducible* part: a veto exists for it, and that
veto is option (c). The §2 table calls only Z(νν) hard-scatter tracks irreducible (l.199). Suggested: "the first
measured quirk-plane background (led by conversions)". The package uses this wording.

**Jp-C9. Paths to a stronger paper, and what remains publishable.** See §2. Content for the package.

**Jp-C10. Q4 has no list of decision points.** The days are spread over Q2 (days 7 and 15), Q4 (day 5 and the
freeze) and the rider (day 12). Suggested: one line in Q4, "Decision points: day 5 (C1/C2, first re-projection), day 7
(preliminary projection), day 12 (MET model, final pilot classification), day 15 (binding projection, possible pause),
freeze days 17–19 (second re-projection, hash), Gate B ≈ day 49 (≈ 51 after the pause)." The days are from §11.3.
The package §6 supplies this.

---

## 4. Final judgment

**Is v6 a sound, honest basis to put to the human at Gate A? Yes.**
- T1, T2 and T3 are resolved where the human reads them.
- Every number in §12.1 is identical to §0, §11, COM and stdout.
- The expected outcome comes first. It is a large measured background with no reach beyond the existing bounds under
  the strategy's own width, and an expected pause. The text says plainly that neither the first upside nor a veto
  alone avoids the pause.

There is no blocking item. The ten C items are wording refinements. Jp-C1, Jp-C3 and Jp-C4 are the most useful, and
the package below already applies them as statements derived from v6's own text and printed numbers. If the
orchestrator applies them to v6 as well, the change is about one clause each and needs no re-review (C items).

---

## 5. Gate-A package (final text, at most 3 pages)

> # GATE A — quirks v2: strategy, benchmarks and schedule for your approval
> Sources: `analyses/quirks_v2/phase1_strategy/outputs/STRATEGY_ingrid_2026-11-14_02-20.md` ("STR"),
> `QV2/COMMITMENTS.md`, and `phase1_strategy/outputs/budget_stdout_v6.txt`, which prints every number.
> **Every reach below is an ESTIMATE on v1 placeholder efficiencies** (best Λ per mass, the plan's reach table). No v2
> signal efficiency has been computed.
>
> ## 1. Headline
> **Expected outcome.**
> - By v1's own counts, the background of the default plan at the R08–R09 selections is
>   **≈ 0.7–1.0×10⁴ events, led by hard-scatter photon conversions**.
> - Why: v1 counted 86 → 13 → 2 conversions per 500 events at R05–R07. That is a fall of ×6.5 per width step, against
>   ×200–340 for the pile-up background, and a pile-up-like fall is rejected at p ≈ 10⁻³.
> - The strategy gives this background a normalisation width of ≈ 0.17 (the generator difference; K, luminosity and
>   material come on top). With that width the **reach is below 243 GeV, at or near the existing bounds of ≈ 180 GeV**.
>   The search for newer bounds (R-20) is pending.
> - The often-quoted ≈ 270–300 GeV (84 % edge) and ≈ 390–420 GeV (background known exactly) are statistics-only.
> - **The day-15 rule is therefore expected to pause the study before production.** Removing the conversions alone
>   would not avoid the pause, because the decays in flight alone are 385–647 events against the class limit of 300.
>
> **Upside**, given as 84 % edge (median), statistics-only:
> - ≈ 420–455 GeV (470–500) if conversions and decays in flight fall like the pile-up background. This is ≈ 310–370
>   GeV with the width 0.17, and the branch still pauses: B₅₀ 587–975.
> - ≈ 705–640 GeV (770–695) if Z(νν) is tested and credited and the other ceilings count 10–100 events. This requires
>   the promotion model to be submitted.
> - ≈ 710 GeV (790) if every ceiling is empty. That is an upper edge.
> - 1,026 GeV for a negligible background.
>
> **What the upside would take.** One of the following, and none of them has been demonstrated:
> - a pilot that counts far fewer conversions and decays in flight than v1 did;
> - a conditional that removes ×31–52 (96.8–98.1 %) of the conversions *and* a credit for the decays in flight;
> - credit from the purpose-built cuts measured in production.
>
> **If none works, the paper still contains:**
> - the plane-thickness law with its scattering floor;
> - the full hit-level chain at pile-up 200 with the signal efficiency map;
> - the background anatomy, with the first measured quirk-plane background term by term;
> - the documented simulation-statistics barrier (v1's bounds were 7.05 decades above budget);
> - the data-driven sideband recipe, closed in simulation or reported as not closing;
> - the closure tests and a reproduction package.
>
> The plan rates such a paper "publishable but less strong".
>
> ## 2. What Phase 1 established
> **Cluster costs**, measured on the workers at 4 jobs per node (STR Table 4.0; FEAS_A/B/C):
>
> | unit | cost |
> |---|---|
> | PU-200 event through the chain | 13.5 s |
> | finder trial | 11.7 s |
> | chain + 4 trials | 60.4 s |
> | ρ = 2 event (one smoke event) | 206 s at 1.46 GiB |
> | no-pile-up interaction | 11.5 ms |
> | Pythia shower | 21 / 23.4 ms |
> | Geant4 gun | 0.134 ms |
> | NLO K-factor | ≈ 2 CPU-min per mass |
> | pyhf, 1,000 toys | 652 s |
> | job overhead | Argo 16.8 s, SSH 2.4 s |
>
> Of the 4,453 CPU-h total, 753 rest on measured unit costs, 2,322 on derived ones and **1,378 on guesses**.
>
> **Software and runner.**
> - The v1 chain runs on Linux with no source build (FEAS_A: the pyacts 48 wheel; the v1 smoke tests pass).
> - MG5 2.9.22 + Pythia 8.313 reproduce v1's LO cross-section: 92.33 ± 0.07 against 92.26 ± 0.04 fb (FEAS_B).
> - NLO K-factors are cheap: K = 1.165 at 200 GeV.
> - Geant4 11.4.3 installs on each worker's local scratch in ≈ 3 min.
> - The job runner passes the kill/resume, memory-limit and I/O-error tests under both Argo and SSH (FEAS_C).
>
> **Incidents and the constraints that followed** (`LOG.md`):
> - 14:06: a cajuela rename returned a stale file handle. The admin fixed it; directories are never renamed.
> - 15:12: einstein ran out of memory, killing the orchestrator and three executors, and cajuela returned I/O errors
>   until 15:20. Since then: a 10 GB memory cap for all agents, nothing heavy on einstein, and at most three agents
>   at a time.
> - 15:20: an install over the `sync` NFS home ran at ≈ 1 MB/s and slowed the lab. Since then: one install at a time,
>   job work on node-local scratch, and Geant4 per worker.
> - Two workers carry graphical sessions, which leaves 10 usable job slots off-hours.
>
> **Review.** Five review cycles reduced the must-resolve findings 11 → 4 → 1 → 0 → 0:
> - cycles 1–2 redesigned the likelihood and closure tests and made every MUST criterion testable;
> - cycle 3 completed the background pool;
> - cycles 4–5 corrected how the expected outcome is stated to you: conversions lead, the reach is quoted with the
>   strategy's own width, the pause is expected, and the calendar includes the pause.
>
> Cycle 6 verified these changes.
>
> ## 3. Your five decisions
> Answer in one line, e.g. "Q1 ●; Q2 ●; Q3 ●; Q4 ●; Q5 ●". ● marks the recommended default.
>
> **Q2 (the central decision): what happens if the day-15 projection exceeds B₅₀ = 300 events** (or both pile-up
> estimators miss their cap)? This is the expected case.
> - **● (a) Pause and ask you at day 15.**
>   - Time: production waits ≈ 2 days for your answer (included in the 60 days).
>   - CPU: the 156 CPU-h reserve, already inside the approved figure, tests the leading term at R06–R07.
>   - Then you choose (b) or (c), with measured pilot counts in hand.
> - **(b) Authorise now: proceed with the measured background.**
>   - Time and CPU: 0 extra CPU-h, no delay.
>   - Paper: the plan's "real background" outcome. That is the first measured quirk-plane background (led by
>     conversions), the reach at that background, and the sideband recipe as the way out.
>   - Expected reach: below 243 GeV, at or near the existing bounds. In the expected case this paper shows no mass
>     reach beyond existing bounds.
>   - The purpose-built cuts measured in production may add some reach. Their credit is unmeasured.
> - **(c) Authorise now: redesign before the freeze.** A conversion-removing conditional is developed and tested on
>   the development and pilot samples.
>   - Time: the freeze and everything after it move by the redesign time. That time cannot be estimated now; it is
>     reported at day 15 and counted as an overrun.
>   - CPU: inside the development allowance and what remains of the reserve.
>   - Paper: the plan's "middle" outcome if it works, otherwise (b).
>   - It works only if the projected B₅₀ is at most 300. That needs the conversions reduced ×31–52 **and** the decays
>     in flight (385–647 events) reduced by a credit. As worded, (c) targets the conversions; if you choose it, say
>     whether it may also target the decays in flight.
>   - Two things are unknown: the veto's background rejection has not been measured, and its signal cost is known only
>     at Gate B. Selections without the veto are kept.
> - If the projection is 300 events or fewer (≈ 560 GeV or more, statistics-only), production proceeds under every
>   option. The paper is then the plan's "middle" outcome, labelled "target not met: sample-size limited".
> - A doubled pool (+665 CPU-h, ≈ +3.8 days) helps only if the ceilings are empty (median 790 → 814 GeV).
> - Note: the day-7 and day-15 readings count own hits before track cleaning (CKF), so they may show ×5–50 more
>   background than the ≈ 10⁴ quoted above.
>
> ***Optional rider to Q2*** (not part of the default; answer "Q2 ● + rider" to accept). It has three parts:
> 1. If the day-7 preliminary B₅₀ is 3,000 events or more, the choice between (b) and (c) is put to you at day 7
>    instead of day 15. The day-15 rule stays binding.
> 2. By day 12, the stored pilot records are used to measure how many conversion configurations a vertex veto would
>    catch. This costs 0 CPU-h.
> 3. 1,000 γ development overlays check v1's ×6.6 fall with pile-up on the v2 chain. This costs +7.0 CPU-h, so the
>    approved figure becomes **4,616 CPU-h** and the threshold **6,001**.
>
> Gain: under (c), up to ≈ 8 days earlier. Cost of declining: those days, nothing else.
>
> **Q1, C1 blinding exception.** May the C1 reproduction compare six v1 signal counts that are also efficiencies of v2
> candidate selections, before the closure verdicts?
> - **● Yes, sealed:** PASS/FAIL only until Gate B, with four counts open. A sealed FAIL cannot be diagnosed from its
>   size.
> - Alternatives: all ten counts open and disclosed; or the six dropped.
> - Cost: 14 CPU-h in every option.
>
> **Q3, exception to brief D4.** When a MUST closure criterion ends untested, may its term enter at its tested ceiling,
> labelled "no credit", with the selection still eligible? The routes by which this can happen are:
> - the eight proxied SM processes and the three additions;
> - a fluctuation (≈ 30 %);
> - the cap rule;
> - the conditionals, and the multijet factorisation (which alone sets a floor of ≈ 4.6×10³ events if it fails);
> - the pile-up crossing test at depth;
> - the promotion model or the CKF survival factor not tested.
>
> Options:
> - **● Yes.**
> - Comply where costed: ≈ +680 CPU-h (100–1,230), ≈ +3.9 days.
> - Strict: such selections are not eligible, and "closure fails" becomes a likely paper.
>
> **Q4, budget, calendar and stop rule.**
> - **● Approve 4,609 CPU-h and 60 days.** The 4,609 CPU-h are 4,453 plus the 156 CPU-h day-15 reserve. The 60 days
>   are 57.8 plus the ≈ 2-day expected pause; a redesign under (c) is extra and reported as an overrun.
> - The approval includes four proposals:
>   - [DP1] the B5 sideband reduced (−358 CPU-h);
>   - [DP2] the B6 detector variations at 4 points (−155 CPU-h);
>   - [DP4] S4 and S5 not included;
>   - [DP5] a second hadronisation model at generator level only, after an install attempt.
> - **Stop and ask at 5,992 CPU-h** (1.3×).
> - 1,378 CPU-h rest on guessed unit costs. If they all doubled the projection would be 5,987 CPU-h, so the
>   re-projection at day 5 or at the freeze may stop the study.
> - The contingency (2,150 CPU-h) and the conditional costs are listed in STR §11.2 but not pre-approved. Every draw is
>   reported.
> - **Your 2–4 week target is not reachable:** 43.5 days contain no production (development and freeze 19, reviews and
>   writing 14.5, ITERATE allowances 8, Gate B 2).
> - Alternatives:
>   - MUST only: 4,176 CPU-h, 59 days (threshold 5,429);
>   - full SHOULD: 5,123 CPU-h, 60 days (threshold 6,660);
>   - pre-approved envelope: 6,759 CPU-h (threshold 8,787).
>
> **Q5, truth-level signal before the hash.** May Stage 2 and the string propagation (47 + 266 CPU-h) exist before
> the pre-registration hash? They depend on the MET model, the trigger and the generator cut (all frozen by day 12),
> not on any selection.
> - **● Yes**, in idle pre-freeze capacity, 0 days.
> - Alternative: after the hash, +47 CPU-h and +1.8 days.
>
> ## 4. Defaults that apply unless you override them (STR §12.1)
> | # | default | alternative (cost) |
> |---|---|---|
> | Df-1 | 2,000 signal rows per point (15 % error) | 4,000 rows (+827 CPU-h, +4.7 d) |
> | Df-2 | closure rules F = 1.5 / 2, cap ln F/3, one re-test at p′ ≥ 0.05/K; false-FAIL loss 6.9–8.9 % | looser cap or distance rules |
> | Df-3 | NLO cross-section nominal; resummed beside it; infracolour +3 to +13 % as a band | resummed nominal |
> | Df-4 | dE/dx not a candidate; forgone gain measured (2 CPU-h) | model the deposit (≈ +390 CPU-h, ≈ 1 week) |
> | Df-5 | time-tag credit only where it closes, with sourced tails | no credit (−10 CPU-h) |
> | Df-6 | endcap outlook "signal ×1.5–3.2" (D1) | "×2.1–3.2" |
> | Df-7 | unsourced detector variation: no nuisance, shift reported; no MET sources → stop and ask | flagged unsourced nuisance |
> | Df-8 | toys parametrised, exact check at 3 points | exact toys (+156 CPU-h) |
> | Df-9 | ceiling on all own hits, CKF survival credited only where tested | CKF inside the ceiling, with a width |
> | Df-10 | coverage checks as one family of 10 | pooled per point |
>
> ## 5. Budget and calendar (proposed variant; days after Gate A, without the pause)
> | phase | CPU-h | days |
> |---|---|---|
> | 2: C1, C2, S2, P1, pilot | 506 | 0–5 |
> | 3: development, S1 string | 580 | 5–17 |
> | freeze review + ITERATE allowance | — | 17–21 |
> | 4a: MUST 2,737 + reduced SHOULD 434 + reserve 156 (2,489 on the critical path, 14.3 d) | 3,327 | 21–41.8 incl. review |
> | 4b + Gate B | 118 | 41.8–48.8 |
> | 4c; 5 + Gate C | 68; 10 | 48.8–57.8 |
> | **total** | **4,609** (stop at 5,992) | **57.8; 60 with the expected pause** |
>
> Range: 49 days if every review passes at once and only MUST items run; 65 at 50 % utilisation; +8 days with two
> ITERATE cycles per review. Storage: ≈ 470 GB on cajuela (670 at the cap) against a 1.5 TB budget.
>
> ## 6. Decision points after Gate A
> - **Day 5:** is v1 reproduced on Linux (C1), and does the finder pass (C2)? First CPU re-projection with measured
>   costs; the stop rule may fire here. A failed family moves everything day for day.
> - **Day 7:** preliminary projection from the pilot, reported in `STATUS.md`. With the rider, Q2 (b)/(c) is asked
>   here if B₅₀ ≥ 3,000.
> - **Day 12:** MET model and the N_trig of the additions; final pilot classification; generator-cut decision. With the
>   rider, the veto fraction and the γ-overlay fall are also reported.
> - **Day 15 (binding):** projection for every term. If B₅₀ > 300 or both pile-up estimators miss their cap, the study
>   pauses (Q2). The reserve is spent by rule 3. Estimators above their cap are redesigned or declared "not submitted".
> - **Freeze (days 17–19):** second CPU re-projection; the pre-registration is hashed and you are notified.
> - **Gate B (≈ day 49; ≈ 51 after the pause):** the background verdicts first, then the signal.
> - **Gate C (≈ day 58; ≈ 60):** the paper.
>
> ## 7. Top risks
> 1. **The conversion background (expected):** no reach beyond the existing bounds unless a demonstrated ≈ 97 %
>    conversion rejection is combined with a credit for the decays in flight.
> 2. **CPU:** 1,378 CPU-h rest on guesses, so the stop rule may fire at day 5 or at the freeze.
> 3. **Development effort:** Phase 3 has 30 channel-days against the plan's 35–50 person-days. Each 3 channel-days more
>    adds one day.
> 4. **Pile-up at depth:** a single estimator beyond R07. If both pile-up estimators fail, no validated pile-up term
>    remains.
> 5. **Other risks:** the Geant4 → Fatras hand-over; the MET model needing two public sources (stop if absent);
>    infrastructure (two incidents on day one).
>
> ## 8. Files
> - STR: §0 summary; §4.4 Table 4.4c (projection per outcome); §11 schedule and stop rules; §12.1 questions and the Q3
>   annex; §12.5 failure modes.
> - `COMMITMENTS.md`; `budget_stdout_v6.txt`.
> - `phase1_strategy/outputs/feasibility/FEAS_{A_chain_anselm,B_generators_basil,C_runner_boris}.md`.
> - `phase1_strategy/review/arbiter/` (verdicts of cycles 1–6); `LOG.md` (incidents, constraints, cycle summaries).

**Package notes for the orchestrator.**
- Every number above is printed in `budget_stdout_v6.txt` or quoted in v6, except the generator and runner
  validation lines, which are from FEAS_B and FEAS_C §1 (read this session).
- Gate B ≈ 51 and Gate C ≈ 60 with the pause are 48.8 + 2 and 57.8 + 2 (stdout l.205).
- The 4a row's 3,327 CPU-h is 2,737 + 434 + 156 (stdout l.96, l.121–123). The rows sum to 4,609.
- Remove the words "Cycle 6 verified these changes" if the cycle-6 arbiter does not PASS.
- If the orchestrator decides that development-sample conditionals may enter the day-15 projection (Jp-C4), nothing
  in the package changes.
