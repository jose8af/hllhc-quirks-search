# Constructive review, cycle 9 — STRATEGY v9 (Mireille) — session Nora, 2026-11-14 07:25

Artifact: `outputs/STRATEGY_mireille_2026-11-14_06-55.md` ("v9", "l." = a line of v9) with `outputs/budget_stdout_v9.txt`
("stdout", saved output; the script was not run in this session). Scope (arbiter v8 §9): §0 and the Gate-A section
(§12.1) read as the human; agreement with the two printed tables and the clarified rule 1 (§11.7); the final Gate-A
package. Not a re-review of the design. Role: `agents/constructive_reviewer.md` (honest-framing check applied).
Also read: arbiter v8 (Margaret) §1, §2, §6, §7, §9, §10; Marcel's candidate package (Co v8 part 3); the cycle-8 fix
report; `LOG.md` 06:55; PLAN outcome table (l.498–512); `check_day15_text.py` (stale list, l.142).
Computation: one stdlib scratch run outside the repo (`nice -n 19 python3 -I`, about 10 s): arbiter §1.3's formula,
40,000 draws, seed 3 — VERIFIED (scratch): empty pilot 76.5; m_Z = 11 / 12 / 13 → 281.2 / 299.7 / 319.0; m_D = 3 / 4
→ 269.2 / 334.0; K_SM = 18.13, K_D = 65.13; f_D = 0 bar 9,527/(12 × 18.13) = ×43.8 and 6,421/218 = ×29.5. All agree
with stdout l.355–366 within the 1 % / 3 % stated precision. No sub-agents, no git.

---

## 1. W1 as the human reads it — RESOLVED

### 1.1 What the human must be told, reading only §0 and §12.1

| must be clear | where v9 says it | status |
|---|---|---|
| (i) what rule 1 measures at day 7 and 15, on which samples | §0 l.89–96 ("computed preliminarily at day 7 … reads every term from the pilot's own-hit counts before CKF … on the samples that exist at day 15: decays in flight and nuclear interactions on their own pilot samples, and every SM hard-scatter process and the multijets at the H per event of the Z(νν) pilot, with no S_CKF, no conditional …, no credit that exists only after the freeze and no pool floor"); Q2 stem l.2805–2807; caption l.2819; rule 1 l.2730–2737 | clear |
| (i) how SM processes without a day-15 sample are read | §0 l.93–95 (through the Z(νν) pilot, "One Z(νν) pilot count is 18 events"); digest row l.2814 "(β) and (γ) are read through this count"; Df-11 l.2949 "one count m_Z for all of them, their conversions included, since no other SM sample exists before the freeze" | clear |
| (i) that the reading was pinned in review, why, and that it is overridable | Df-11 l.2949: "pinned in review cycle 8"; why: "rule 1 as previously written did not say what those processes contribute, so the same pilot result could read as proceed or pause"; overridable: it is in the table "Defaults the user can override"; §0 l.141 "Eleven defaults … can be overridden" | clear in §12.1; **§0 does not say it** (C-1); Df-11's consequence and alternative carry no number (C-2) |
| (ii) threshold 300 and where it is crossed | §0 l.90–91 (300 or both pile-up estimators above cap); §0 l.99–101 ("B₅₀ ≈ 76 with every pilot count at zero; the limit is at ≈ 12 Z(νν) pilot counts … or between 3 and 4 decays-in-flight pilot counts"); digest l.2814–2816; caption l.2819 ("four decays-in-flight counts alone pause the study") | clear |
| (iii) expected reading and its caveats → the pause is expected | §0 l.96–99 (×5–50, "ε_pair assumed 0.8–0.98, not measured, and not bounded above"; "the pause is the expected branch"); caption l.2819 states all three caveats (ESTIMATE on v1 placeholder inputs; DIF on 1–2 v1 counts; ×5–50 on an assumed ε_pair); Q2 l.2805; Q4 l.2915 (≈ 2 days inside the 60) | clear |
| (iv)(a) cost, paper | l.2842–2843: ≈ 2 days turnaround, reserve spent by rule 3(b) (inside 4,609, Q4 l.2913), then (b) or (c) | clear |
| (iv)(b) cost, paper | l.2844–2849: 0 CPU-h, no delay; "real background"; below 243 GeV; "no mass reach beyond the existing bounds" | clear |
| (iv)(c) cost, paper, bar | l.2850–2862: time "not estimable now, reported at day 15"; CPU-h in development allowance + reserve; "middle" if it works, else (b); bar ×44 [×30] / ×75–150 [×51–101] / ×114 [×77] or none / none at central size; ×n/1.14; ×219–2,186 without S_CKF; "The veto's rejection has not been measured" l.2885 | clear |
| (v) optional rider | l.2891–2898: trigger ≥ 3,000 at day 7, expected to trigger, +7.0 CPU-h (4,616 / 6,001), gain ≤ 8 days, cost of declining | clear |

### 1.2 Every number of the family in §0 and §12.1 against the printed cells

| # | v9 statement | stdout cell | agrees? |
|---|---|---|---|
| 1 | §0 l.95 "One Z(νν) pilot count is 18 events and one decays-in-flight pilot count is 65" | l.355: 18.1; 65.1 | yes |
| 2 | §0 l.96 "×5–50 … ε_pair 0.8–0.98" | 1/(1−0.8) = 5, 1/(1−0.98) = 50 (l.362–363 basis) | yes |
| 3 | §0 l.97 "B₅₀ ≈ 3×10⁴–3×10⁵ … ((α1′))" | l.363: 3.2e4–3.3e4 / 3.2e5–3.3e5 | yes |
| 4 | §0 l.98 "≈ 2.6×10³–4.2×10⁴ … ((α1))" | l.362: 2.6e3–4.3e3 / 2.5e4–4.2e4 | yes (outer span) |
| 5 | §0 l.99 "B₅₀ ≈ 76 with every pilot count at zero" | l.358: 76 | yes |
| 6 | §0 l.100 "limit … ≈ 12 Z(νν) pilot counts, which is also how the rule reads (β) and (γ)" | l.359: 300 at 12 "at the limit"; l.361 (γ)/(β) = Z(νν)-count row | yes |
| 7 | §0 l.101 "between 3 and 4 decays-in-flight pilot counts" | l.360: 266 at 3 below, 331 at 4 above | yes |
| 8 | §0 l.62 "(projected B₅₀ 590–980; (α1); after CKF … the day-15 rule reads this branch on all own hits, (α1) row of the v9 table)" | l.314, 316: 587 / 975 (after CKF); l.362 own hits | yes |
| 9 | §0 l.79 "(β) … the day-15 rule reads it as (γ), through the Z(νν) pilot count" | l.361 | yes |
| 10 | §0 l.102 "A conversion veto or a fit-probability credit enters only the test of a Q2 (c) redesign" | l.364–365 "(c) only" | yes |
| 11 | leading sentence l.117 "projected B₅₀ ≈ 3×10⁴–3×10⁵ … limit of 300" | l.363 | yes |
| 12 | leading sentence l.118–119 "at v1's central decays-in-flight size (1–2 counts) no conversion rejection suffices" | l.369: none suffices at f_D = 1 | yes |
| 13 | rule 1 l.2747–2748 "5.9×10³ events after CKF by v1's Z(νν) photon rate against the 6.4–9.5×10³ of Table 4.4c" | 5,918 = 3,559 × 1.663 (arbiter §1.3; self-test 6, l.396, 3.158e4 = 5,918/0.2 + DIF + floor); 6.42e3 / 9.53e3 l.331, 327 | yes |
| 14 | rule 1 l.2755–2756 "limit at ≈ 12 … between 3 and 4" | l.359–360 | yes |
| 15 | Q2 l.2807 "×5–50" | as 2 | yes |
| 16–21 | Q2 digest table, six rows (l.2812–2817): 3.2–3.3×10⁴ / 3.2–3.3×10⁵; 2.6×10³–4.2×10⁴; 281/300/317 at 11/12/13; 266/331 at 3/4; 76 (37–152); 109–130 | l.363; 362; 359; 360; 358; 364 | yes, every cell |
| 22 | caption l.2819 "pile-up … median 6.7 events; 88–148 at an R08 selection" | l.355 (6.7); Table 4.4c R08 row | yes |
| 23 | caption l.2819 "four decays-in-flight counts alone pause the study" | l.360: 331 at 4 | yes |
| 24 | Q2 l.2837 "This branch also pauses (table)" | l.362 above | yes |
| 25 | Q2 l.2839 "Their day-15 readings are the Z(νν)-count and zero-count rows" | l.358–359, 361 | yes |
| 26 | Q2 (c) l.2854–2855 "385–647 events … B₅₀ is 458–718" | l.314, 316 (385, 647); l.369 (458 / 718) | yes |
| 27 | Q2 (c) l.2857 "at least ×44 (97.7 %) [×30]" | l.366 | yes |
| 28 | Q2 (c) l.2857–2858 "×75–150 (98.7–99.3 %) [×51–101]" | l.367 | yes |
| 29 | Q2 (c) l.2858–2859 "×114 (99.1 %) [×77] at ×e⁻¹ with fall ×339; with ×201 none suffices" | l.368 | yes |
| 30 | Q2 (c) l.2861–2862 "×219–2,186 … none from a quarter … on" | l.370 | yes |
| 31 | Q2 (c) l.2885 "(α1) with credit, B₅₀ 109–130) acts on both" | l.364 | yes |
| 32 | Q2 l.2887 "reach ≈ 560 GeV or more" | l.379–380 (563 / 559 GeV at B₅₀ 291 / 302) | yes |
| 33 | rider l.2892 "≥ 3,000 … expected at ≈ 3×10⁴–3×10⁵" | l.363 | yes (see C-3) |
| 34 | the two verbatim blocks l.2821–2832, 2874–2880 | l.354–364, 365–370 | identical (text check (A): 17/17, fix report) |

**Result: 34 of 34 statements agree; none lacks its basis.** The text checker (fix report, 45/45 OK) and my reading
agree. Rule 1 (§11.7 l.2730–2737, l.2753) now states both points that were ambiguous (what a process without a day-15
sample gets; the (c) factors never multiply a floor), so it is single-valued.

### 1.3 Q1, Q3, Q4, Q5 — unchanged and self-contained

Q1 l.2792–2796 (14 CPU-h every option); Q3 l.2900–2911 (≈ +680, 100–1,230, ≈ +3.9 days); Q4 l.2913–2925 (4,609;
threshold 5,992; 60 days, 57.8 without the pause; 43.5 days without critical-path production; envelope 6,759 /
8,787; MUST only 4,176 / 59 (57); full 5,123 / 60 (58)); Q5 l.2927–2933 (47 + 266; +47, +1.8 days). Each states its
question, default, alternatives and cost; they agree with §11.2 l.2534–2538 and §0 l.124–137. Unchanged from v8
except the family (fix report diff table: no hunk outside T1–T18, O6, bookkeeping).

### 1.4 W1 status: RESOLVED

The family is closed in the text: every number agrees with a printed cell, the reading is stated in §0, Q2 and rule 1
on one basis, and the pinned reading is shown to the human as an overridable default (Df-11). Two presentation gaps
remain, both Category C, both closed in the package (part 3): §0 does not say the reading was pinned or point to
Df-11 (C-1), and Df-11 gives its consequence only by reference and its alternative without its effect (C-2).

---

## 2. Final judgment: YES — v9 is a sound, honest basis to put to the human at Gate A

Honest-framing check: the expected outcome (≈ 0.7–1.0×10⁴ events after CKF, reach below 243 GeV at or near the
existing bounds, the pause expected) comes first in §0, the leading sentence and Q2; every upside is labelled
statistics-only and post-freeze where it is; the day-15 reading is quoted from printed lines on the rule's own basis;
the pinned reading is the stricter one and its two remaining leniencies are printed (credit row at v1's central
2/35 instead of its 68 % upper value; pilot-own photon rate 8 % below the 0.255 column). Nothing hides a problem.
Blocking list: **none**.

New findings: **A 0, B 0, C 4.**
- **C-1** (§0 "The pause", l.89–102): add after "no pool floor": "(this reading was pinned in review cycle 8 and is
  overridable, Df-11)". The human reading §0 alone otherwise does not learn that the basis was a review decision.
- **C-2** (Df-11, l.2949): consequence by reference ("the Z(νν) pilot count that the … row marks 'at the limit'") and
  alternative "see the arbiter verdict §1" — the only Df row whose alternative has no stated effect. The plain
  statement, "≈ 12 Z(νν) pilot counts; the alternative (other SM processes at pool floors) gives ≈ 20, sees only the
  Z(νν) share (37 %) of the conversions and makes (c) pass at about ×16" (arbiter §1.2 point 2), is blocked in v9 by
  the checker's stale pattern `≈ 20 … pilot` (l.142). The package states it; in a later version the stale pattern
  could exempt the Df-11 row.
- **C-3** (rider l.2892): "expected to trigger" holds for (α1′); under (α1) at ε_pair = 0.8 and fall ×339 the reading
  is ≈ 2.6×10³ (l.362), below the 3,000 trigger. Not wrong as worded; one clause ("in the expected branch") would
  make it exact.
- **C-4** (proxy): §0 and the Q2 digest do not say that reading W, tt̄ and the other processes through the Z(νν) H per
  event is a proxy (tag: ESTIMATE; the 0.231 photon-rate column of the grid is the only stated caveat, l.2870). Not a
  decision input (the expected reading is two orders above 300 under every reading); worth one clause in the caption.

Also checked (package, not v9): Marcel's risk 3 "Conversion normalisation likely > 80 % of the uncertainty
(investigated)" had no source line in v8/v9; the package now cites stdout l.327 / l.330 (s95 352 counting-only
against 2,697 with the 0.17 width) and drops "(investigated)", which no line supports.

---

## 3. Gate-A package — final text (copy verbatim into `gates/GATE_A.md`)

Word count: **1,499 by `wc -w`** on the block from "# GATE A" to the end of "## 9. Files" (tables, headings, pipes
and symbols included). Every number is from v9 or `budget_stdout_v9.txt` (check list in §4). Built from Marcel's
part 3 with the thirteen corrections of arbiter v8 §7 applied: (1) sources v9; (2) headline last two sentences;
(3) upside ((α1) reading 2.6×10³–4.2×10⁴; (β) read through the Z(νν) count, limit ≈ 12); (4) review line cycles 1–8
with "[cycle 9: …]" and the cycle 4–8 root cause; (5) Q2 stem and the compact table exactly as ordered; (6)
rejection bullets; (7) risk 1; (8) risk 2; (9) paths; (10) files; (11) Df-9 cell unchanged; (12) notes below; (13)
length. Added beyond §7 as the brief to this session requires: the Df-11 row, marked NEW, with its consequence
(≈ 12, not ≈ 20) and alternative. Compressions to fit: the σ comparison given as z = 0.91 (FEAS_B l.15), Df-1's
cost, the rider's day-12 report (0 CPU-h; STR l.2893–2896), "1,026 at negligible background", the ×6.5-vs-pile-up
sentence of the headline (it remains in STR §0 and Q2). "Publishable but less strong" is not used: PLAN l.508–509
gives it to "Closure fails"; the fallback uses the plan's "real background" row (l.506–507).

---

# GATE A — quirks v2: strategy, benchmarks and schedule

Sources: STRATEGY v9 (STR), `budget_stdout_v9.txt` (stdout). **All reach and background numbers: ESTIMATE on v1
placeholder efficiencies** (best Λ per mass).

## 1. Headline
**Expected (ESTIMATE).** By v1's counts the background at the R08–R09 selections is **≈ 0.7–1.0×10⁴ events, led by
hard-scatter photon conversions** (after CKF, as v1 counted them; a lower value). With the strategy's normalisation
width (0.17) the **reach is below 243 GeV, at or near the existing bounds (≈ 180 GeV; R-20 pending)**; ≈ 270–300 GeV
(84 % edge; 390–420 for a background known exactly) are statistics-only. Caveats: decays in flight rest on 1–2 v1
counts; the SM floor on a guessed 45 ms/event; v1's efficiencies are ×1/0.87 high. **The day-15 rule is expected to pause the study**: it
reads the pilot's own-hit counts before CKF, expected at B₅₀ ≈ 3×10⁴–3×10⁵ against 300 (the ×5–50 rests on an
assumed pair efficiency, not measured). A conversion veto counts only in a Q2 (c) redesign, and at v1's central
decays-in-flight size no conversion rejection suffices (without conversions B₅₀ is 458–718).

**Upside (ESTIMATE)** (84 % edge (median), statistics-only): 420–455 GeV (470–500) if conversions and decays in
flight fall like pile-up (310–370 at width 0.17; still pauses: ≈ 2.6×10³–4.2×10⁴ as the rule reads it); 705–640
(770–695) if Z(νν) is tested and the other ceilings count 10–100, conditional on the promotion model (post-freeze;
at day 15 read through the Z(νν) pilot count, at the limit at ≈ 12 counts); 710 (790) if every ceiling is empty, an
upper edge.

## 2. What Phase 1 established
| 4 jobs/node | PU-200 event, chain | finder trial | ρ = 2 event | no-pile-up event |
|---|---|---|---|---|
| cost | 13.5 s | 11.7 s | 206 s, 1.46 GiB | 45 ms (guessed) |

Of 4,453 CPU-h: 753 measured, 2,322 derived, **1,378 guessed**.
- v1 chain on Linux. MG5 2.9.22 + Pythia 8.313 reproduce v1's LO σ (z = 0.91); NLO K = 1.165 at 200 GeV; Geant4 11.4.3 installs node-locally in ≈ 3 min. Runner: kill/resume, memory, I/O pass.
- Incidents (`LOG.md`): 14:06 stale file handle after a cajuela directory rename; 15:12 einstein out of memory.
  Since: no directory renames; nothing heavy on einstein; 10 GB agent cap; ≤ 3 agents; one install at a time.
- Review: cycles 1–8, Category A 11→4→1→0→0→0→0→0, Category B 24→14→15→5→3→1→4→1; [cycle 9: …].
  Cycles 4–8 turned on the day-15 reading; cycle 8 traced this to an ambiguity in rule 1 and made it single-valued (Df-11: limit ≈ 12 Z(νν) pilot counts, not ≈ 20).

## 3. Your decisions
● = default; answer "Q1 ●; Q2 ●; …".

**Q2 (central): what if the day-15 projection exceeds B₅₀ = 300 (or both pile-up estimators miss their cap)?** Rule 1
reads the pilot's own-hit counts before CKF: no S_CKF, no veto or fit-probability credit, nothing post-freeze, no
pool floor. Every SM process is read through the one Z(νν) pilot count, since no other SM sample exists at day 15
(stdout l.354–364).

| pilot counts (branch) | day-15 B₅₀ | vs 300 |
|---|---|---|
| (α1′) v1's conversion counts (expected) | ≈ 3×10⁴ (ε_pair 0.8) to 3×10⁵ (0.98) | above |
| (α1) DIF, conversions fall like pile-up | ≈ 2.6×10³–4.2×10⁴ | above |
| Z(νν) pilot count, the others zero (also (β), (γ)) | 281 at 11, 300 at 12, 317 at 13 | limit at ≈ 12 |
| decays-in-flight pilot count, the others zero | 266 at 3, 331 at 4 | below up to 3 |
| every pilot count zero | 76 (37–152) | below |
| (c) test only: (α1) with fit-probability credit on DIF and conversions | 109–130 | below |

Rejection a (c) conditional needs (stdout l.365–370; pilot basis, S_CKF estimated, photon rate 0.379 [0.255]):
- none suffices at v1's central decays-in-flight size;
- ≥ ×44 (97.7 %) [×30] if the pilot counts no decay in flight; ×75–150 [×51–101] at a quarter of that size; ×114
  (99.1 %) [×77] or none at ×e⁻¹;
- all unmeasured; zero survivors among n show ≤ ×n/1.14; without S_CKF ×219–2,186, and none from a quarter of that
  size on.

- **● (a) Pause and ask at day 15:** ≈ 2 days (inside the 60), 0 extra CPU-h (the 156 CPU-h reserve tests the
  leading term); then (b) or (c).
- **(b) Proceed now:** 0 CPU-h, no delay. Paper: the plan's "real background" outcome; reach expected below
  243 GeV, not beyond existing bounds.
- **(c) Redesign before the freeze:** a conversion-removing conditional; freeze delay reported at day 15; CPU-h from
  development allowance and reserve. Works if B₅₀ ≤ 300 (bar above). Say whether it may also target decays in flight (needed at v1's central size). Paper: "middle" if it works, else (b).
- If B₅₀ ≤ 300 (≥ 560 GeV, statistics-only): production proceeds; "middle" outcome.
- *Optional rider* ("Q2 ● + rider"): (b)/(c) asked at day 7 if B₅₀ ≥ 3,000 (expected to trigger); 1,000 γ overlays
  (+7.0 CPU-h). Gain: ≤ 8 days under (c).

**Q1, C1 blinding.** ● Six v1 signal counts sealed until Gate B, four open. Alternatives: all ten open;
six dropped. 14 CPU-h each.

**Q3, D4 exception.** An untested MUST closure criterion enters at its ceiling, "no credit", selection eligible.
● Yes. Alternatives: comply where costed, ≈ +680 CPU-h (100–1,230), +3.9 days; strict ("closure fails" likely).

**Q4, budget and calendar.** ● **4,609 CPU-h, 60 days**, stop-and-ask at **5,992**, with [DP1] B5 reduced
(−358), [DP2] B6 at 4 points (−155), [DP4] S4/S5 out, [DP5] second hadronisation model generator-level only.
Contingency 2,150 CPU-h not pre-approved. **Your 2–4 weeks is missed by 4–5 weeks** (43.5 days without
critical-path production). Alternatives: §5; envelope 6,759 (threshold 8,787).

**Q5, truth-level signal before the hash** (313 CPU-h). ● Yes, idle capacity, 0 days. Alternative: after the
hash, +47 CPU-h, +1.8 days.

## 4. Defaults (overridable; STR §12.1)
| # | default | # | default |
|---|---|---|---|
| Df-1 | 2,000 signal rows/point | Df-6 | endcap outlook "signal ×1.5–3.2" |
| Df-2 | closure F = 1.5/2, cap ln F/3 | Df-7 | unsourced detector variation: no nuisance, shift reported |
| Df-3 | NLO σ nominal, resummed beside it | Df-8 | parametrised toys, exact check at 3 points |
| Df-4 | dE/dx not a candidate | Df-9 | ceiling on own hits, S_CKF where tested; sets the day-7/15 basis |
| Df-5 | time-tag credit only where it closes | Df-10 | coverage checks: one family of 10 |
| **Df-11, NEW (pinned in cycle 8)** | rule 1 reads only day-15 samples: every SM process via the Z(νν) pilot count, no pool floor; (c) factors never multiply a floor → limit ≈ 12 counts | alternative | SM at pool floors: limit ≈ 20, blind to most conversions, (c) looks easier (arbiter v8 §1.2) |

## 5. Budget and calendar
| variant | CPU-h | threshold | days (no pause / pause) |
|---|---|---|---|
| MUST only | 4,176 | 5,429 | 56.9 / 58.9 |
| **MUST + reduced SHOULD (●)** | **4,609** | **5,992** | **57.8 / 59.8** |
| full SHOULD | 5,123 | 6,660 | 58.1 / 60.1 |

4,609 = MUST 4,019 + SHOULD 434 + reserve 156; rider 4,616 / 6,001. Capacity assumed: 174 core-h/day production, 116
development (measured in week 1). Range 49–65 days; +8 with two ITERATEs per review. Storage ≈ 470 GB (670 at cap)
of 1.5 TB.

## 6. Decision points after Gate A
**Day 5:** C1, C2; CPU re-projection (stop rule may fire). **Day 7:** preliminary projection.
**Day 12:** MET model, final pilot classification. **Day 15 (binding):** rule 1; (c) on development estimates; pause
if B₅₀ > 300. Freeze days 17–19; Gate B ≈ day 49 (51 with pause); Gate C ≈ 58 (60).

## 7. Top risks
1. Conversions: no reach beyond existing bounds without a demonstrated rejection ≥ 98.7–99.3 % (quarter of v1's
   decays-in-flight size; 97.7 % if the pilot counts none; 99.1 % or none at ×e⁻¹) and fewer decays in flight.
2. Pilot statistics: an empty pilot reads B₅₀ 76 of 300; each decays-in-flight pilot count adds 65
   events, and four pause the study.
3. Conversion normalisation sets the reach (s95 2,697 against 352 statistics-only): likely > 80 % of the
   uncertainty.
4. CPU: 1,378 CPU-h guessed; the stop rule may fire (day 5, freeze).
5. Pile-up beyond R07 on one estimator; Geant4→Fatras hand-over.

## 8. Paths to a stronger paper (none demonstrated)
A pilot counting far fewer conversions and decays in flight; under (c), conversion rejection ≥ ×44 (×114 or none
if decays in flight are e times below v1's central size, none at that size) plus fewer decays in flight;
conditionals measured in production. **If none works**, the plan's "real background" paper: the first measured
quirk-plane background, the reach at that B, the sideband recipe as the way out; plus the thickness law.

## 9. Files
STR v9 (§0, §12.1); `budget_stdout_v9.txt`; `COMMITMENTS.md`; `phase1_strategy/outputs/feasibility/FEAS_{A,B,C}_*.md`;
arbiter verdicts, `phase1_strategy/review/arbiter/`; `LOG.md`; `DEVIATIONS.md`.

---

## 4. Number check of the package (number → source)

| package number | source |
|---|---|
| ≈ 0.7–1.0×10⁴ events, after CKF | STR l.67; stdout l.331–339 (6,825–10,193) |
| below 243 GeV with width 0.17; ≈ 180 GeV; R-20 pending | stdout l.330, 334, 338, 342; STR l.83 |
| ≈ 270–300 (84 % edge); 390–420 known exactly | stdout l.375 (270–297; 392–419) |
| caveats 1–2 counts; 45 ms; ×1/0.87 | STR l.118, l.87, l.88 |
| 3×10⁴–3×10⁵; ×5–50 | stdout l.363; STR l.96 |
| 458–718 | stdout l.369 |
| 420–455 (470–500); 310–370 at 0.17 | stdout l.373 (421–455; 469–504); l.375 (312–372) |
| 2.6×10³–4.2×10⁴ | stdout l.362 |
| 705–640 (770–695) | stdout l.308–310 (706/684/641; 767/749/695), quoted as STR l.77 |
| limit ≈ 12 counts | stdout l.359 |
| 710 (790) | stdout l.373 (712; 790) |
| 13.5 s; 11.7 s; 206 s, 1.46 GiB; 45 ms guessed | STR Table 4.0 l.350–356 |
| 4,453: 753 / 2,322 / 1,378 | STR l.2569 |
| MG5 2.9.22, Pythia 8.313; z = 0.91 | STR l.2089; FEAS_B l.14–15 |
| K = 1.165 at 200 GeV | STR l.1966 |
| Geant4 11.4.3, ≈ 3 min node-local | STR l.2090; FEAS_B l.23 |
| runner kill/resume, memory, I/O | FEAS_C l.21–22 |
| 14:06, 15:12 incidents; constraints | LOG.md l.7, l.44; AGENT_RULES l.18, 23–35; STR l.2490 |
| A 11→…→0, B 24→…→1 | arbiter v8 §9 table; LOG 06:55 |
| ≈ 12, not ≈ 20 | arbiter v8 §1.2 ("≈ 20 … becomes ≈ 12"); LOG 06:55 |
| Q2 table: 3×10⁴ / 3×10⁵; 2.6×10³–4.2×10⁴; 281/300/317; 266/331; 76 (37–152); 109–130 | stdout l.363; 362; 359; 360; 358; 364 |
| ×44 (97.7 %) [×30]; ×75–150 [×51–101]; ×114 (99.1 %) [×77] or none | stdout l.366; 367; 368 |
| none at central size | stdout l.369 |
| ×n/1.14; ×219–2,186; none from a quarter on | STR l.2752–2753; stdout l.370 |
| (a) ≈ 2 days, 156 CPU-h reserve | STR l.2842–2843, l.2914 |
| (b) 0 CPU-h; < 243 GeV | STR l.2844–2846 |
| ≥ 560 GeV | stdout l.379–380; STR l.2887 |
| rider 3,000; +7.0; ≤ 8 days; 4,616 / 6,001 | STR l.2892–2897 |
| Q1 six / four; 14 CPU-h | STR l.2794–2796 |
| Q3 +680 (100–1,230), +3.9 days | STR l.2910 |
| Q4 4,609; 5,992; 60; −358; −155; 2,150; 43.5; 6,759 / 8,787 | STR l.2913–2924; l.2648–2649; l.2571 |
| 2–4 weeks missed by 4–5 weeks | (60 or 57.8 days − 28) / 7 = 4.6 / 4.3 weeks, arithmetic on STR l.2915 |
| Q5 313 CPU-h; +47, +1.8 days | STR l.2928 (47 + 266 = 313); l.2932–2933 |
| Df-1…Df-10 cells | STR l.2939–2948 |
| Df-11 content; ≈ 20 alternative, "blind to most conversions" | STR l.2949; arbiter v8 §1.2 (Z(νν) share 37 %) |
| budget table 4,176/5,429/56.9/58.9; 4,609/5,992/57.8/59.8; 5,123/6,660/58.1/60.1 | STR l.2536–2538 |
| 4,019 + 434 + 156 | STR l.2522–2528 (4,453 − 4,019 = 434) |
| 174 / 116 core-h/day | STR l.2499–2500 (§11.1) |
| 49–65 days; +8 | STR §11.3 calendar paragraph (l.2607–2613); §0 l.131–133 |
| 470 GB (670) of 1.5 TB | STR l.134 |
| days 5 / 7 / 12 / 15; freeze 17–19; Gate B ≈ 49 (51); Gate C ≈ 58 (60) | STR §11.7 table l.2717–2718, l.2722–2742; §11.3 l.2581, 2588–2590 |
| risk 1: 98.7–99.3 %; 97.7 %; 99.1 % | stdout l.367; 366; 368 |
| risk 2: 76; 65; four | stdout l.358; 355; 360 |
| risk 3: s95 2,697 vs 352 | stdout l.330 (2697.4); l.327 (352.2) |
| risk 4: 1,378 | STR l.2569 |

No number in the package lacks a source; none disagrees with it.

## 5. Notes for the orchestrator
- Fill "[cycle 9: …]" after the cycle-9 arbiter.
- The package is outside the reach of `check_day15_text.py` (it scans the strategy only); its day-15 numbers were
  checked by hand against stdout l.354–370 (§4).
- If the arbiter wants C-1/C-2 in the strategy too, the Df-11 row would need an exemption from the stale pattern
  `≈ 20 … pilot` (checker l.142).
