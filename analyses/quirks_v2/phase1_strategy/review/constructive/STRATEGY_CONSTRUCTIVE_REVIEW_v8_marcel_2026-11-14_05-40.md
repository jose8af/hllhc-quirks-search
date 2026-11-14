# Constructive review, cycle 8 — STRATEGY v8 (Leopold) — session Marcel, 2026-11-14 05:40

Artifact: `outputs/STRATEGY_leopold_2026-11-14_05-00.md` ("v8", "l." = a line of v8) with `outputs/budget_stdout_v8.txt`
("stdout"). Scope (arbiter v7 §11): §0 and §12.1 read as the human; family V1; the final Gate-A package. Not a
re-review of the design. Role: `agents/constructive_reviewer.md` (honest-framing check applied). Also read: arbiter
v7 (Lena) in full, Klaus's candidate package (Co v7 §3), the fix report, §11.7, PLAN l.495–512, brief D7, LOG 05:00/05:40.

Computation: one standard-library scratch run on einstein (`nice -n 19 python3 -I`, 143 s, 36 MB max RSS) that loads
the script with `runpy` (stdout suppressed) and calls its own `pmf_pred`, `rows`, `PU9`, `MJK`, `kz`, `K_DIF`, `G_A1P`,
`ALPHA`, `F_GAM`, `PILOT_HS` without modifying it. Scratch file outside the record. Values from it are tagged
VERIFIED (scratch). No sub-agents, no git.

---

## 1. Family V1 as the human reads it — RESOLVED in the text; one new defect in the (c) grid's caption (B-1)

### 1.1 What the human is told, reading only §0 and §12.1

| must be clear | where v8 says it | status |
|---|---|---|
| what rule 1 measures at day 7 and 15: own hits before CKF, no S_CKF, no conditional, no post-freeze credit | §0 l.90–94 ("reads every no-pile-up term at max(zero-count floor, N_t·H) on all own hits before CKF, from the pilot's counts, with no S_CKF, no conditional (no veto, no fit-probability credit) and no credit that exists only after the freeze"); Q2 l.2796–2797; caption l.2810; Df-9 row l.2939 | clear |
| the threshold 300 (and the second trigger, both pile-up estimators above cap) | §0 l.90–91; Q2 l.2837; caption l.2810 | clear |
| expected reading and its caveats: ESTIMATE on v1 placeholder inputs; DIF on 1–2 v1 counts; ×5–50 on an assumed ε_pair | §0 l.94–96 ("ε_pair assumed 0.8–0.98, not measured, and not bounded above"); Q2 l.2798–2799 ("assumed, not measured"); caption l.2810 states all three verbatim; Q2 (c) l.2850 "resting on 1–2 counts" | clear |
| therefore the pause is expected | §0 l.74, l.96 ("the pause is the expected branch"), leading sentence l.114–115; Q2 l.2796; Q4 l.2907–2908 (≈ 2 days inside the 60) | clear |
| (a) cost, paper | l.2838–2839: ≈ 2 days, the 156 CPU-h reserve spent by rule 3(b), then (b) or (c) | clear |
| (b) cost, paper | l.2840–2845: 0 CPU-h, no delay; "real background"; below 243 GeV; "no mass reach beyond the existing bounds" in the expected case | clear |
| (c) cost, paper, bar | l.2846–2856: time not estimable, reported at day 15; CPU-h in development allowance + remaining reserve; "middle" if it works, else (b); bar ≥ ×34 / ×52–81 / ×69–235; ×n/1.14; ×5–50 without S_CKF; "The veto's rejection has not been measured" l.2877 | clear, **but see B-1** for the basis of the bar |
| (c) must also target decays in flight at v1's central size | l.2875–2877 | clear |

### 1.2 Every branch / factor / day-7–15 sentence against the two tables

Table rows cited as stdout lines (day-15 table l.354–369, grid l.370–376).

| # | sentence (v8) | table cell | agrees? |
|---|---|---|---|
| 1 | §0 l.95 "B₅₀ ≈ 5.0×10⁴–5.1×10⁵ … ((α1′))" | l.367: 4.96e+04–5.09e+04 / 4.96e+05–5.09e+05 | yes (rounded) |
| 2 | §0 l.95–96 "≈ 2.8×10³–4.8×10⁴ … ((α1))" | l.365–366: 2.85e+03 / 2.84e+04; 4.79e+03 / 4.78e+04 | yes (2.85→"2.8", rounding down at the low end; harmless, C-3) |
| 3 | §0 l.97 "B₅₀ ≈ 75 with every pilot ceiling at zero" | l.356: 75 [38–148] below | yes |
| 4 | §0 l.98 "Z(νν) alone may count up to ≈ 20 pilot ceiling events" | l.357: m = 20 → 300, "below" (≤ 300); m = 25 → 352 | yes |
| 5 | §0 l.98–99 "every SM ceiling up to ≈ 60 pool-equivalent counts (≈ 13 in the pilot) … (β) is read as (γ)" | l.361: 60 → 294 below; l.362: 70 → 331 above; l.364 (β) | yes |
| 6 | §0 l.62 "(α1) … projected B₅₀ 590–980 … the day-15 rule reads this branch on all own hits" | l.365–366: 587 / 975 after CKF, own-hit cells | yes |
| 7 | §0 l.79 "(β) … the day-15 rule reads the same ceilings as (γ)" | l.364 | yes |
| 8 | §0 l.99–100 "A conversion veto or a fit-probability credit enters only the test of a Q2 (c) redesign" | l.368–369 "(c) only" | yes |
| 9 | leading sentence l.115–117 "B₅₀ ≈ 5×10⁴–5×10⁵ … no conversion rejection suffices without a reduction of the decays in flight" | l.367; grid l.375 f_D = 1 "none suffices" | yes |
| 10 | Q2 l.2798 "B₅₀ ≈ 5.0–5.1×10⁴ at ε_pair = 0.8 and ≈ 5.0–5.1×10⁵ at 0.98" | l.367 | yes |
| 11 | Q2 summary table, 6 rows (l.2803–2808) | l.367, 365–366, 358–363, 357, 356, 368–369 | yes, every cell; wording C-2 ("below under ≈ 20" vs "up to ≈ 20") |
| 12 | Q2 l.2833 "This branch also pauses (table)" | l.365–366 above | yes |
| 13 | Q2 l.2835 "Their day-15 readings are the (γ) and empty-ceiling rows" | l.356, 358–363 | yes |
| 14 | Q2 (c) l.2850–2851 "At v1's central … size (385–647 …) no conversion rejection suffices: with the conversions removed, B₅₀ is 401–663" | l.375; stdout l.347–348 | yes (but on the pool-floor basis, B-1) |
| 15 | Q2 (c) l.2852–2854 "×34 (97.0 %) [×23] … ×52–81 (98.1–98.8 %) [×35–55] … ×69–235 (98.6–99.6 %) [×47–159]" | l.371–373 | yes, every cell |
| 16 | Q2 (c) l.2855–2856 "×1/(1 − ε_pair) larger (×5–50, not measured)" | l.376 | yes |
| 17 | Q2 l.2877 "(α1) with credit, B₅₀ 51–74 acts on both" | l.368–369 | yes |
| 18 | Q2 l.2879 "at most 300 events (reach ≈ 560 GeV or more, statistics-only)" | stdout l.385–386 (m_H = 120–125: 563–559 GeV) | yes |
| 19 | rider l.2884 "expected at ≈ 5×10⁴–5×10⁵" | l.367 | yes |
| 20 | Q2 (c) grid caption l.2860–2861 "with the remaining terms read as rule 1 reads them (all own hits before CKF, no S_CKF, no credit …)" | code: `_need` uses `kap_nodif` (pool floors, script l.718) and the after-CKF (α1) DIF on κ_DIF (pool) | **no** — B-1 |

Result: 19 of 20 statements agree with the printed cells. The one that does not is a caption claim about the basis of
the grid (B-1).

### 1.3 B-1 (new, Category B): the (c) rejection grid is not on the basis its caption states, and the difference makes (c) look easier

**Evidence.**
- Caption, l.2860–2861: the grid is "with the remaining terms read as rule 1 reads them".
- Rule 1 as written (§11.7 l.2729–2745, and the v8 day-15 table's row 1, stdout l.356) reads Z(νν), DIF and each NI
  radius at the **pilot** exposures (κ = 10.9 for Z(νν), 0.88–1.12 per NI radius, 65.1 for DIF). The (c) test is that
  same projection with the redesigned conditional and S_CKF applied to the leading terms (l.2738–2743).
- The grid code (`_need`, as ordered by arbiter v7 §4 item S and printed) uses `kap_nodif` = the **pool** floors
  (script l.718: κ = 2.28 for Z(νν), 0.25–0.28 per NI radius). So does the 401–663 "conversions removed" line
  (stdout l.347–348).
- VERIFIED (scratch, script functions): with DIF and conversions absent, the remaining terms give B₅₀ = **15** on pool
  floors and **25** on the pilot exposures rule 1 uses. The rejection needed for B₅₀ ≤ 300, recomputed with the same
  bisection on rule 1's pilot exposures (DIF kept on κ_DIF as in the grid, photon rate 0.379, falls ×339 / ×201):

| f_D | printed grid (pool floors) | rule-1 basis (pilot exposures) |
|---|---|---|
| 0 | ×34 / ×34 | ×35 / ×35 |
| 1/4 | ×52 / ×81 | ×55 / ×90 |
| e⁻¹ | ×69 / ×235 | ×75 / ×311 |
| 1/2 | ×110 / none | ×124 / none |

  Reading the hypothesised DIF itself from a pilot count (κ = 65.1, i.e. ≈ 6 counts for 385 events) would raise
  them further; I did not compute that, since how the pilot would count an (α1)-size DIF is not defined by the text.
- The (c)-only rows 51 / 74 (stdout l.368–369) are likewise on the pool floors (Table 4.4c `pmf_cache`); on pilot
  exposures they rise by about the 10-event base difference and stay below 300 (not recomputed exactly; C-1).

**Why B and not C.** It is a factual statement shown to the human (the basis of the (c) bar), it is false as worded,
and the error is in the gentle direction: the printed factors are lower edges, by up to ×1.3 (×235 → ×311) at the
×201 / e⁻¹ cell. That is the same pattern the cycle-7 arbiter recorded under motivated reasoning (§8), and the same
kind of item as V1-c. It is admissible under arbiter v7 §11 ("a factual error in a number shown to the user"). It does
not change the default, the expected outcome, any CPU-h or day, or any conclusion: "none suffices at v1's central
size" holds a fortiori, and (c) is only harder.

**Fix (text only, 0 CPU-h; either suffices).**
- (minimal) Caption l.2860–2861: "with the remaining terms read as rule 1 reads them (all own hits before CKF, no
  S_CKF, no credit that exists only after the freeze)" → "with the remaining terms at their Table 4.4a pool floors
  (rule 1 reads Z(νν) and NI at the pilot exposures, which raises every factor: these are lower edges)". And in Q2 (c)
  l.2852: "is at least ×34" stays; "×52–81 … and ×69–235" → "at least ×52–81 … and at least ×69–235".
- (complete) Print the grid on rule 1's pilot exposures (`kd15_noz`-style base) and quote those cells. I recommend
  the minimal fix for cycle 8: the arbiter's code is settled, and the package below already uses lower-edge wording.

### 1.4 Two tables in the Gate-A section: harmless, but only one belongs in the package

The 6-row summary table (l.2801–2808) is a faithful digest of the verbatim block (l.2812–2829); I checked every cell
(row 11 above). The verbatim block is ASCII ("nunu", "eps_pair", "x339") and 16 rows long; it is the audit anchor
that removes the paraphrase mechanism, and it should stay in the strategy. For the human the duplication is mildly
confusing only because the summary does not say it is a digest. C-2: add "(digest of the printed lines below)" to the
summary's lead-in. **For the package: show the 6-row summary table**, cite the stdout lines, and do not show the block.

### 1.5 V1 status

V1-a (β), V1-b (×e⁻¹), V1-c (×31), V1-d (credit acts on DIF): **RESOLVED** — rows 5, 7, 13 / 15 / 15 / 17 above;
grep of §0 and §12.1 for "would suffice", "×31", "avoid": only the printed comparison line and "no … suffices". The
one remaining defect is in the grid's caption basis (B-1), new in v8, not a member of V1 as defined.

---

## 2. Final judgment: NOT YET — one blocking item (B-1), a caption fix

Honest-framing check: the expected outcome (≈ 10⁴ events after CKF, reach at or near the existing bounds, the pause
expected) comes first in §0, the leading sentence and Q2; every upside is labelled statistics-only and post-freeze
where it is; the day-15 reading is now quoted from printed lines. The only gentle framing left is B-1. Otherwise v8
is a sound, honest basis for Gate A. Blocking list: **B-1 only** (§1.3, two-line text fix).

New findings: **A 0, B 1, C 3.**
- **B-1** — §1.3.
- **C-1.** Same basis remark for the (c)-only rows 51–74 (pool floors): add "(on pool floors; somewhat higher on
  the pilot exposures, still below 300)" or recompute. Not a decision input (both stay far below 300).
- **C-2.** Summary table: say it is a digest of the printed lines; row "Z(νν) alone": "below under ≈ 20" → "below up
  to ≈ 20 (300 at 20)", matching §0 l.98 and stdout l.357.
- **C-3.** §0 l.96 "≈ 2.8×10³": the printed cell is 2.85e+03; "≈ 2.9×10³" or "≈ 3×10³" avoids a reader finding a
  rounding mismatch. Cosmetic.

Also for the human (not a defect; arbiter v7 §9 obs. 1): one DIF pilot count is ≈ 65 events (κ_DIF on 10⁶ events,
VERIFIED scratch 65.13), so the day-15 reading is sensitive to pilot statistics; the package carries it as a risk.

---

## 3. Gate-A package — final text (copy verbatim into `gates/GATE_A.md`)

Word count: **1,499 by `wc -w`** on the block from "# GATE A" to the end of "## 9. Files" (tables, headings and
symbols included). Every number is from v8 or `budget_stdout_v8.txt`. The eleven corrections of arbiter v7 §7 are
applied: (1) sources v8; (2) headline last sentence; (3) upside (rule's reading of (α1); (β) post-freeze, read as (γ)
at day 15); (4) paths, ≥ ×34 / ×69–235 / none at v1's size; (5) review line in the form the orchestrator asked for
(cycles 1–7, "[cycle 8: …]", cycle-7 sentence added); (6) the Q2 short table, here the one 6-row table; (7) Q2 (c) via
the three-line grid summary; (8) risk 1, 98.1–99.6 % (97.0 % only if decays in flight vanished); (9) arbiter verdicts
pointed to by directory, so the line stays true after cycle 8; (10) placeholder; (11) length: within 1,500 by
compressing the incident, defaults and Phase-1 lines (the cycle 1–6 narrative was dropped; the counts remain). The
B-1 wording is applied ("lower edges, other terms at pool floors"). Order as required: headline, Phase 1, decisions
(Q2 first, then Q1, Q3, Q4, Q5), defaults, budget, decision points, risks, paths and fallback, files. "Publishable but
less strong" is not used: PLAN l.508–509 gives it to "Closure fails", and the fallback is described with the plan's
"real background" row (l.506–507).

---

# GATE A — quirks v2: strategy, benchmarks and schedule

Sources: STRATEGY v8 (STR), `budget_stdout_v8.txt` (stdout). **Every reach and background number is an ESTIMATE on
v1 placeholder efficiencies** (best Λ per mass).

## 1. Headline
**Expected (ESTIMATE).** By v1's counts the background at the R08–R09 selections is **≈ 0.7–1.0×10⁴ events, led by
hard-scatter photon conversions** (after CKF, as v1 counted them; a lower value). v1's conversions fell ×6.5 per
width step, not like pile-up (×200–340; p ≈ 10⁻³). With the strategy's normalisation width (0.17) the **reach is
below 243 GeV, at or near the existing bounds (≈ 180 GeV; search R-20 pending)**, already so at width 0.05. The
≈ 270–300 GeV (84 % edge; 390–420 for a background known exactly) are statistics-only. Caveats: decays in flight rest on 1–2 v1
counts; the SM floor on a guessed 45 ms/event; v1's efficiencies are ×1/0.87 high. **The day-15
rule is expected to pause the study**: it reads own hits before CKF, expected at B₅₀ ≈ 5×10⁴–5×10⁵ against 300 (the
×5–50 rests on an assumed pair efficiency, not measured). A conversion veto counts only in a Q2 (c) redesign, and at
v1's central decays-in-flight size no conversion rejection suffices (without conversions B₅₀ is 401–663).

**Upside (ESTIMATE)** (84 % edge (median), statistics-only): 420–455 GeV (470–500) if conversions and decays in flight fall like
pile-up (310–370 at width 0.17; still pauses: B₅₀ 587–975 after CKF, ≈ 2.8×10³–4.8×10⁴ as the rule reads it);
705–640 (770–695) if Z(νν) is tested and the other ceilings count 10–100, conditional on the promotion model (post-freeze;
at day 15 read as (γ), below 300 only up to ≈ 60 pool counts); 710 (790) if every ceiling is
empty, an upper edge; 1,026 at negligible background.

## 2. What Phase 1 established
| unit (4 jobs/node) | cost |
|---|---|
| PU-200 event through the chain | 13.5 s |
| finder trial | 11.7 s |
| ρ = 2 event | 206 s at 1.46 GiB |
| no-pile-up event | 45 ms (guessed) |

Of 4,453 CPU-h: 753 measured, 2,322 derived, **1,378 guessed**.
- v1 chain runs on Linux. MG5 2.9.22 + Pythia 8.313 reproduce v1's LO σ (92.33 ± 0.07 vs
  92.26 ± 0.04 fb); NLO K = 1.165 at 200 GeV; Geant4 11.4.3 installs node-locally in ≈ 3 min. The runner passes
  kill/resume, memory and I/O tests.
- Incidents (`LOG.md`): 14:06 stale file handle after a cajuela directory rename; 15:12 einstein out of memory,
  agents killed. Since: no directory renames, nothing heavy on einstein, 10 GB agent cap, ≤ 3 agents, one install at
  a time, local scratch, 10 off-hours slots.
- Review: cycles 1–7, Category A 11 → 4 → 1 → 0 → 0 → 0 → 0, Category B 24 → 14 → 15 → 5 → 3 → 1 → 4; [cycle 8: …].
  Cycle 7 corrected which branches pass the day-15 rule and the (c) bar.

## 3. Your decisions
Answer "Q1 ●; Q2 ●; …" (● = default).

**Q2 (central): what if the day-15 projection exceeds B₅₀ = 300 (or both pile-up estimators miss their cap)?** Rule 1
reads the pilot on own hits before CKF: no S_CKF, no veto or fit-probability credit, nothing post-freeze (stdout
l.354–369).

| branch | day-15 B₅₀ | vs 300 |
|---|---|---|
| (α1′) v1's conversion counts (expected) | ≈ 5×10⁴ (ε_pair 0.8) to 5×10⁵ (0.98) | above |
| (α1) DIF, conversions fall like pile-up | 587–975 after CKF; ≈ 2.8×10³–4.8×10⁴ own hits | above |
| (γ), and (β) at day 15: SM ceilings 10–100 pool counts | 104–448 | below up to ≈ 60 |
| Z(νν) alone at its ceiling | 300 at 20 pilot counts | below up to 20 |
| every pilot ceiling empty | 75 (38–148) | below |
| (c) test only: (α1) with fit-probability credit on DIF and conversions | 51–74 | below |

Rejection a (c) conditional needs (stdout l.370–376; lower edges, other terms at pool floors):
- none suffices at v1's central decays-in-flight size;
- ≥ ×34 (97.0 %) if they vanished; ×52–81 at a quarter of that size; ×69–235 (98.6–99.6 %) at ×e⁻¹;
- all unmeasured; zero survivors among n show ≤ ×n/1.14; without S_CKF every factor is ×5–50 larger.

- **● (a) Pause and ask at day 15:** ≈ 2 days (inside the 60), 0 extra CPU-h; the 156 CPU-h reserve tests the
  leading term; then (b) or (c).
- **(b) Proceed now:** 0 CPU-h, no delay. Paper: the plan's "real background" outcome, reach expected below 243 GeV,
  none beyond the existing bounds.
- **(c) Redesign before the freeze:** a conversion-removing conditional; the freeze moves by a time reported at
  day 15; CPU-h from development allowance and reserve. Works if B₅₀ ≤ 300 with conditional and S_CKF estimated on development samples (bar above). Say whether it
  may also target decays in flight; at v1's central size it cannot work otherwise. Paper: "middle" if it works, else (b).
- If B₅₀ ≤ 300 (≥ 560 GeV, statistics-only): production proceeds; "middle" outcome.
- *Optional rider* ("Q2 ● + rider"): (b)/(c) asked at day 7 if B₅₀ ≥ 3,000 (expected to trigger);
  1,000 γ overlays (+7.0 CPU-h). Gain: ≤ 8 days under (c).

**Q1, C1 blinding.** ● Six v1 signal counts sealed (PASS/FAIL only) until Gate B, four open. Alternatives: all ten
open; six dropped. 14 CPU-h each.

**Q3, D4 exception.** An untested MUST closure criterion enters at its tested ceiling, "no credit", selection eligible.
● Yes. Alternatives: comply where costed, ≈ +680 CPU-h (100–1,230), +3.9 days; strict
("closure fails" likely).

**Q4, budget and calendar.** ● **4,609 CPU-h, 60 days**, stop-and-ask at **5,992** (1.3×), with [DP1] B5 reduced
(−358), [DP2] B6 at 4 points (−155), [DP4] S4/S5 out, [DP5] second hadronisation model at generator level.
Contingency 2,150 CPU-h not pre-approved. **Your 2–4 weeks is missed by four
to five weeks**: 43.5 days have no critical-path production. Alternatives: §5; envelope 6,759 (threshold 8,787).

**Q5, truth-level signal before the hash** (47 + 266 CPU-h). ● Yes, idle capacity, 0 days.
Alternative: after the hash, +47 CPU-h, +1.8 days.

## 4. Defaults (overridable; STR §12.1)
| # | default | # | default |
|---|---|---|---|
| Df-1 | 2,000 signal rows/point (4,000: +827 CPU-h, +4.7 d) | Df-6 | endcap outlook "signal ×1.5–3.2" |
| Df-2 | closure F = 1.5/2, cap ln F/3, one re-test | Df-7 | unsourced detector variation: shift reported, no nuisance |
| Df-3 | NLO σ nominal, resummed beside it | Df-8 | parametrised toys, exact check at 3 points |
| Df-4 | dE/dx not a candidate | Df-9 | ceiling on own hits, S_CKF where tested; sets the day-7/15 basis |
| Df-5 | time-tag credit only where it closes | Df-10 | coverage checks: one family of 10 |

## 5. Budget and calendar
| variant | CPU-h | threshold | days (no pause / pause) |
|---|---|---|---|
| MUST only | 4,176 | 5,429 | 56.9 / 58.9 |
| **MUST + reduced SHOULD (●)** | **4,609** | **5,992** | **57.8 / 59.8** |
| full SHOULD | 5,123 | 6,660 | 58.1 / 60.1 |

4,609 = MUST 4,019 + SHOULD 434 + reserve 156; rider 4,616 / 6,001. Capacity: 174 core-h/day production, 116
development (measured in week 1). Range 49–65 days; +8 with two ITERATEs per review. Storage ≈ 470 GB (670 at cap) of 1.5 TB.

## 6. Decision points after Gate A
- **Day 5:** C1, C2 pass?; CPU re-projection (stop rule may fire).
- **Day 7:** preliminary projection; with the rider, Q2 asked.
- **Day 12:** MET model, final pilot classification.
- **Day 15 (binding):** rule 1 for every term; (c) judged on development estimates; pause if B₅₀ > 300.
- Freeze days 17–19; Gate B ≈ day 49 (51 with pause); Gate C ≈ 58 (60).

## 7. Top risks
1. Conversions: no reach beyond existing bounds without a demonstrated conversion rejection of ≥ 98.1–99.6 % (97.0 %
   only if decays in flight vanished) plus a reduction of decays in flight.
2. Pilot statistics: an empty pilot already reads B₅₀ 75 of the 300.
3. Conversion normalisation likely > 80 % of the uncertainty (investigated).
4. CPU: 1,378 CPU-h guessed; the stop rule may fire at day 5 or at the freeze.
5. Pile-up beyond R07 on one estimator; Geant4 → Fatras hand-over.

## 8. Paths to a stronger paper (none demonstrated)
A pilot counting far fewer conversions and decays in flight; under (c), a conversion rejection of ≥ ×34
(×69–235 if decays in flight are e times below v1's central size, none at that size) with a reduction of decays in
flight; conditionals measured in production. **If none works**, the plan's "real background" paper: the
first measured quirk-plane background, the reach at that B, the sideband recipe as the way out; with the thickness
law and the hit-level chain at pile-up 200.

## 9. Files
STR v8 (§0, Table 4.4c, §11, §12.1); `budget_stdout_v8.txt`; `COMMITMENTS.md`;
`phase1_strategy/outputs/feasibility/FEAS_{A,B,C}_*.md`; arbiter verdicts, `phase1_strategy/review/arbiter/`;
`LOG.md`; `DEVIATIONS.md`.

---

## 4. Notes for the orchestrator
- Fill "[cycle 8: …]" after the cycle-8 arbiter.
- Numbers checked against stdout v8: 5×10⁴–5×10⁵ (l.367); 587–975 / 2.85e3–4.78e4 (l.365–366); 104–448, ≈ 60 / 13
  (l.358–363); 300 at 20 (l.357); 75 (38–148) (l.356); 51–74 (l.368–369); grid ×34, ×52–81, ×69–235, 97.0 / 98.6–99.6 %
  (l.371–373); 401–663 (l.347–348); 270–297 / 392–419 and "< 243" at w = 0.05 (l.326–342, l.381); 310–370 (l.343–344);
  706/684/641 and 767/749/695 (l.308–310, quoted as in STR); 710 (790), 1,026 (l.379); ≥ 560 GeV (l.385–386);
  4,616 / 6,001 (STR l.2889); budget table STR l.2534–2536; 753 / 2,322 / 1,378 STR l.2567; DP savings STR l.2646–2647.
- Risk 1's "98.1–99.6 %" is the grid's f_D = 1/4 and e⁻¹ cells (l.372–373); with B-1 these are lower edges.
- Risk 2 ("an empty pilot already reads B₅₀ 75 of the 300") is stdout l.356; it reflects arbiter v7 §9 observation 1
  (one DIF pilot count ≈ 65 events, VERIFIED scratch κ_DIF = 65.13), which is not printed in v8 and so not quoted.
- Removed from the cycle-7 candidate to fit: Geant4 "(schrodinger so far)", the cycle 1–6 narrative, "all guesses
  doubled gives 5,987", the rider's 0-CPU-h day-12 veto fraction, "(routes: STR Q3 annex)". All remain in STR §12.1.
- If B-1 is fixed by recomputing the grid on pilot exposures, replace the grid numbers in §1, §3, §7, §8 of the
  package with the printed ones and drop "lower edges".
