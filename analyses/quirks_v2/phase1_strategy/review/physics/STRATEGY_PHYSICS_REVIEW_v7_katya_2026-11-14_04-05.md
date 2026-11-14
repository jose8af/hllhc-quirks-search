# Physics review: Phase 1 STRATEGY v7 (quirks v2), review cycle 7

Reviewer: Katya (physics), 2026-11-14 04:05. Fresh session; I saw no earlier cycle. I followed the prompt template of
`agents/physics_reviewer.md` and did not read the methodology spec or the conventions. Phase 1 has no figures, so the
figure inspection does not apply.

**Artifact.** `phase1_strategy/outputs/STRATEGY_jules_2026-11-14_03-40.md` ("v7"; "l." is a line of v7), diffed
against v6 `STRATEGY_ingrid_2026-11-14_02-20.md`.
**Inputs.** FRAMING; arbiter v6 (Johanna) §7, §8, §12; physics review v6 (Isolde); `FIX_REPORT_cycle6_jules.md`;
`src/strategy_budget.py` (run in full, plus a scratch script that reuses its own `pmf_pred`, rows and scenario inputs
without modifying it); v1 `C12FC_v1/background.json` → `cprime.gamma`, `cprime.dif`.
**Scope (verdict §12).** The physics of U1, O1, O2 and the "1–2 counts" caveat, and a physics reading of the v6→v7 diff.

## Verdict

- **U1: PARTIALLY RESOLVED.** All eight items of verdict §7 are applied and correct (§1–§2 below). Two statements
  still fail the test of task 1(b)/(c), both text only, 0 CPU-h:
  - **B-1.** (β) is still listed as avoiding the pause for ceilings of 10–100 counts (§0 l.95; Q2 stem l.2794). Its
    B₅₀ (24–79) needs a Z(νν) credit that the day-15 projection does not admit. On the rule's basis the branch is the
    (γ) row, which is above 300 at 100 counts.
  - **B-2.** The new (c) sentence "at its size ×e⁻¹ the conversions alone would suffice (B₅₀ 159–256)" holds only if
    the conversions are removed **entirely**. A ×31–52 veto, the bar stated two lines earlier, gives B₅₀ 345–566 at
    that DIF size. Reaching 300 there needs ≈ ×70 to ≈ ×250.
- **Additions O1, O2 and the "1–2 counts" caveat: acceptable** (C remarks only).
- **New findings: 0 A, 2 B, 6 C.**
- **Judgment: not yet.** The blocking list is B-1 and B-2. Both are wording fixes that the arbiter can check in the
  diff, with no new review.

---

## 1. Reproduction

- `python3 src/strategy_budget.py` (38 s) gives output **identical** to `outputs/budget_stdout_v7.txt`. v7 stdout
  differs from v6 only by the two `v7 (U1)` lines in [9b] (`diff` = 2 added lines).
- Script l.849–852, read: (i) `U1_I` is `pmf_pred(kap_nodif + DIF·e⁻¹, PU9)`, i.e. floors + pile-up + DIF/e with **no
  conversion term**. (ii) `U1_II` is the sum of medians of the (α1′) terms, with DIF and conversions ×1/(1 − ε).
  These are the methods ordered in §7 item 1.
- Arithmetic check: floors + pile-up = 401 − 385 = 16. 16 + 385/e = 157.6 and 16 + 647/e = 254.0, against the
  printed 159 / 256 (the pmf median; difference < 1 %). Own-hit basis: 9,929 × 5 = 4.96×10⁴, 10,193 × 50 =
  5.10×10⁵, against the printed 4.96–5.09×10⁴ / 4.96–5.09×10⁵. Correct.
- v1 record: `cprime.gamma.n_attr_c0 = 0` and `cprime.dif.n_attr_c0 = 0`. With no pile-up, v1's after-CKF
  classification passes nothing for either topology. Each row carries an `f_CKF<0.2` factor (γ R01: 2,901 / 2,907),
  but the record has **no** quantity that measures ε_pair, the CKF removal of own-hit configurations. ×5–50 therefore
  rests on the assumed ε_pair = 0.8–0.98 alone. The text says so ("assumed 0.8–0.98, not measured", l.787; "assumed,
  not measured", l.2788; "×5–50, not measured", l.2814).

Extra numbers I computed with the script's own `pmf_pred` and inputs (scratch only, not in the artifact):

| case | B₅₀ |
|---|---|
| DIF ×e⁻¹, conversions at the (α1) level (i.e. the ×31–52 veto), ×339 / ×201 falls | 345 / 566 |
| DIF ×e⁻¹, conversions 9,527 reduced ×70 / ×100 / ×250, ×339 fall | 299 / 258 / 200 |
| same, ×201 fall: ×150 / ×200 / ×250 | 323 / 307 / 298 |
| (γ) every SM ceiling at H, m_H = 50 / 60 / 70 / 80 (printed: 10 → 56, 30 → 133, 100 → 398) | 209 / 247 / 284 / 323 |

## 2. U1, point by point

**(a) Day 7 and day 15, ×5–50.**
- Rule 1 (l.2729–2731): "The projection of a no-pile-up term is N_t·H on all own hits, with no S_CKF and no conditional
  credit (Df-9); its DIF and conversion terms are therefore expected ×1/(1 − ε_pair) above the after-CKF rows of Table
  4.4c (×5–50 at the assumed ε_pair = 0.8–0.98…)". Rule 1 defines the single projection that is computed at day 7 and
  becomes binding at day 15, so the sentence covers both days.
- §0 l.101: "The day-7 and day-15 projections read own hits before CKF (Df-9) and are expected ×5–50 above the
  after-CKF figures of this summary."
- Q2 stem l.2786–2789: "The day-7 and day-15 projections count own hits before CKF … expected ×5–50 above this figure
  (… assumed, not measured…)".
- The old phrase "The day-7 reading counts own hits" now appears nowhere in v7.
- **Is ×5–50 supported?** Only as an assumption, and it is labelled as one in rule 1, Q2 and §4.4. Physically the
  direction is right and the size is if anything a minimum. H is the no-credit ceiling (S, π_k, S_CKF ≤ 1), so H
  divided by v1's with-pile-up after-CKF count is at least 1/S_CKF, which is at least 1/(1 − ε_pair). That
  v1 finds zero no-pile-up passes for γ and DIF fits a CKF that removes most stiff own-hit pairs. A high ε_pair for
  stiff conversion electrons and DIF parents is plausible. Nothing bounds it at 0.98 (C-1).

**(b) Which branches cross or avoid 300 under the rule as written.**

| claim in v7 | location | rule-basis value | status |
|---|---|---|---|
| (α1) no credit pauses (587–975) | §0 l.91, Q2 l.2791 | after CKF 587–975; on own hits ×5–50 more | correct |
| a conversion veto alone does not avoid, at v1's central DIF size | §0 l.93, l.111, l.1018, Q2 l.2793 | after CKF 401–663 with conversions removed | correct (and a fortiori on own hits) |
| (α1) with fit-probability credit 51–74 avoids, "admitted … only under Q2 (c)" | §0 l.94, Q2 l.2794 | needs a conditional credit, which only the (c) test admits | correct as restricted. See C-3: the credit acts on DIF as well |
| DIF ×e⁻¹ with the conversions removed: 159–256 | Q2 (c) l.2813 | on the (c) basis (S_CKF EST) | number correct, wording incomplete: **B-2** |
| **(β) at 10–100 counts avoids** | **§0 l.95, Q2 l.2794** | Z(νν) "tested and credited" rests on its B4-c test (l.1000), which is post-freeze. Rule 1 enters every term as max(floor, N_t·H), so at day 15 Z(νν) sits at its pilot ceiling and the branch is (γ): 56 / 133 / 398 at 10 / 30 / 100 counts, crossing 300 at ≈ 75 | **B-1** |
| empty ceilings avoid | §0 l.95, Q2 l.2795 | pilot zeros give Gamma(1) bounds per term, far below 300 | correct |

**(c) The bar for Q2 (c).**
- The bar is stated on the rule's basis: "It works if the projected B₅₀ is at most 300, with the redesigned conditional
  and S_CKF estimated on development samples (EST, §11.7 rule 1)" (l.2809–2810). Rule 1 gives the samples and adds
  "No credit in the result comes from these estimates" (l.2734).
- The fallback if S_CKF cannot be estimated is stated ("every reduction must be ×1/(1 − ε_pair) larger (×5–50, not
  measured)"). The decision on whether (c) may target DIF is put to the human. This is physically meaningful. A
  pre-freeze go/no-go can only rest on development estimates. Credit in the result still needs the post-freeze tests.
  An optimistic estimate therefore costs redesign time and returns the (b) paper. It cannot produce a wrong
  background in the result.
- What the rule does not say is how a development survival fraction with **zero or few survivors** enters. C′_PU γ has
  ≈ 172 attributed candidates at R05 per 1,000 events (v1: 86 / 500), ≈ 26 at R06 and ≈ 4 at R07. A veto at the
  required ×31–250 leaves 0.7–5.5 survivors at R05. Taken at its central value, a zero count would "remove" the term
  down to its floor. That would assume a gain that was not measured, for the go/no-go only. Classified C (C-2), since
  it does not reach the result.
- **B-2.** The sentence at l.2811–2813 reads: "That needs the conversions reduced by ×31–52 … **and** the decays in
  flight reduced: with the conversions removed, B₅₀ is 401–663 … at its size ×e⁻¹ the conversions alone would suffice
  (B₅₀ 159–256…)". 159–256 is the value with the conversions removed **entirely** (script l.849: no conversion term).
  At DIF ×e⁻¹ a ×31–52 veto gives 345 / 566, still above 300. The rejection actually needed there is ≈ ×70 (98.6 %)
  for the ×339 fall and ≈ ×250 (99.6 %) for the ×201 fall (table in §1). A human weighing (c) would read ×31–52 as
  enough "if DIF is e lower". It is not. For a displaced-vertex veto on the near-collinear pairs that pass a narrow
  ribbon, the gap between 96.8 % and 99.6 % rejection is the feasibility question.

**(d) Default and expected numbers unchanged.** In the diff, option (a) (l.2798–2799) has no hunk. Every number
changed in v6→v7 is a new clause; no existing figure (4,609 / 5,992 CPU-h, 60 days, ≈ 0.7–1.0×10⁴, reaches, ×31–52,
401–663, 587–975, 51–74) is altered. Confirmed.

## 3. Additions

- **O1** (l.824: C′_PU "serves C1 and, for the conversions, the development estimate of a Q2 (c) redesign"). This is
  physically sensible, and consistent with rule 1 l.2732. C′_PU γ is v1's own gun-photon-with-pile-up topology, the
  one whose 86 → 13 → 2 counts define the conversion term. It runs CKF with pile-up and carries truth own hits, so both
  the veto rejection and S_CKF of the conversions can be estimated on it. It is background-only, which is what a
  rejection needs. The signal cost is correctly deferred to Gate B (l.2816). Limits: no Geant4 (no bremsstrahlung
  or material-dependent conversion radius and pair asymmetry), a gun spectrum, and statistics only to R05–R06. The
  rider's 1,000 γ overlays are the better sample for the veto (C-4).
- **O2** ("after CKF, as v1 counted them; a lower value where S_CKF is not tested", l.66–67, l.106–107, l.2937; Q2
  l.2781 in its long form). The label is correct. v1's counts are after CKF with pile-up. In the result, an untested
  S_CKF puts the term at H on own hits, ×1/(1 − ε_pair) or more above. "A lower value" is the right direction, and
  by the argument in §2(a) it is close to a lower bound. The short form can be misread as "the background is lower
  where S_CKF is not tested" (C-5).
- **"1–2 counts" caveat** (l.93, l.111, l.1018–1019, l.2792; the explanation at l.2812). It is factually right: the
  DIF size of (α1) comes from v1's 2 and 1 attributed DIF at R06–R07 (l.55). It is physically warranted, since a
  single count has a 68 % Poisson range of roughly ×0.2–×3, so DIF ×e⁻¹ is a one-sigma case. The text also notes
  that v2's own-z DIF vertices may lower DIF (l.84). It appears at every live copy of the claim. l.3015 is a v6
  history row and correctly keeps its old wording. One over-reach of scope: in §0 l.92–93 the caveat also qualifies
  "a steeper conversion fall". That branch pauses even at DIF ×e⁻¹ (345 / 566, no credit, after CKF), so the
  qualifier is unnecessary there. It is harmless (C-6).

## 4. Consistency (§0, §4.4, rule 1, Df-9, Q2 (a)/(b)/(c), rider, risk list)

- **Contradiction 1 (B-1).** §0 l.95 and Q2 l.2794 list (β) among the branches that avoid the pause. Rule 1
  l.2720–2721 and l.2729 ("max(zero-count floor, N_t·H) per term"; "no conditional credit") put Z(νν) at its pilot
  ceiling at day 15. §4.4 l.1000 makes (β) depend on Z(νν)'s B4-c test, which only happens after the freeze.
- **Tension (B-2).** Q2 (c) l.2811 (×31–52) against l.2813 (159–256 at DIF ×e⁻¹, conversions removed).
- **No contradiction:**
  - Df-9 row l.2877 ("credited only where tested") describes the result basis, and route 6 (l.2896, "×1/(1 − ε_pair)
    above H_CKF") matches rule 1 and the O2 label.
  - The §4.4 labels at l.790 and l.870 match rule 1.
  - The rider (l.2822–2827) is consistent with rule 1's sample list.
  - The §12.5 point 3 (l.2936–2939) label matches §0.
  - The Q3 reach clause for (β) (l.2837) is a post-freeze reach and is correct as such.
- §0 l.101 says "expected ×5–50" without "assumed", where rule 1 and Q2 carry the label (C-1).

## 5. Diff reading (v6 → v7)

Every hunk is traceable:
- header and status (administrative);
- O2: l.66, l.106, l.2937;
- U1: l.93–95 (caveat, "only under Q2 (c)"), l.101, l.2729–2734 (rule 1), l.2781–2789 (stem), l.2792–2794,
  l.2808–2816 ((c), with Jp-C6/C7);
- self-declared caveat: l.111, l.1019;
- item 6 labels: l.790, l.870;
- O1: l.824;
- C items: Cr C2 (l.125, l.2602), Ph C-4 (l.1659), Cr C1 (l.2565, l.2709), Cr C3 (l.2659), Jp-C8 (l.2801), Jp-C2
  (l.2804), Jp-C5 (l.2817), Cr C4 (l.2826);
- §13.6 change table.

No hunk changes a criterion, a sample or a cost. Physics of the C items: dropping "irreducible" (Jp-C8) is a physics
improvement, since conversions are reducible by a veto. "The conditionals measured in production may add some reach"
(Jp-C2) is honest. Ph C-4 now says "if the day-15 pause does not fire" twice in one sentence (l.1659–1660); this is
cosmetic. The script's stdout has only the two new lines.

## 6. Findings

**B-1 (β presented as avoiding the pause on a basis rule 1 does not admit).**
- *Locations:* §0 l.95; Q2 stem l.2794–2795.
- *Fix (text, 0 CPU-h):* in both places, after "(β)", add "(its Z(νν) credit comes only after the freeze; the day-15
  projection sees it with Z(νν) at its pilot ceiling, as (γ): B₅₀ 56 / 133 / 398 at 10 / 30 / 100 counts, so below
  300 only up to ≈ 70 counts; script [9b] (γ) rows)". The ≈ 70 is my interpolation (70 → 284, 80 → 323). Either quote
  only the printed rows, or add one print line.
- *Why B:* it is a claim shown to the human about which branches avoid the pause. It is of the same kind as the (α1)
  credit item fixed in U1.

**B-2 (the (c) bar at DIF ×e⁻¹).**
- *Location:* Q2 (c) l.2812–2813.
- *Fix:* after "(B₅₀ 159–256, script [9b], v7 line)" add "with the conversions removed entirely. At that size a ×31–52
  veto leaves B₅₀ ≈ 345–566, and 300 needs ≈ ×70–250 (98.6–99.6 %)". Add a print line in [9b] for these numbers
  (0 CPU-h; my values from `pmf_pred` are in §1).
- *Why B:* it is a number shown to the user that misstates the rejection needed, by a factor of 2–5.

**C items.**
- C-1. §0 l.101: write "expected ×5–50 (ε_pair assumed 0.8–0.98, not measured; a minimum factor, since H ≥ P/S_CKF)".
  The factor could exceed 50.
- C-2. Rule 1 / Q2 (c): state that a development survival or conditional fraction enters the (c) test as its
  Gamma(m + 1)-type upper value, as H does for the pilot. A zero-survivor sample of ≈ 170 at R05 then credits at most
  ≈ ×100–170. Also state that this is near the ×70–250 needed.
- C-3. "(α1) with fit-probability credit, which the day-15 projection admits only under (c)": that credit acts on DIF
  (385 → 22 and 647 → 37 events) as well as on the conversions. It is therefore available only if the human lets (c) target the
  decays in flight. Say so in the stem.
- C-4. O1: name the rider's Geant4 γ overlays as the preferred veto sample when the rider is taken, and C′_PU (gun,
  no Geant4) as the fallback.
- C-5. Use the long O2 form of Q2 l.2781 everywhere, or say "a lower bound: where S_CKF is not tested the term carries
  ×1/(1 − ε_pair) or more".
- C-6. §0 l.92–93: limit the "1–2 counts" qualifier to the conversion-removing conditional, since the steeper-fall
  branch pauses at DIF ×e⁻¹ as well. Ph C-4 duplicate: drop the second "if the day-15 pause does not fire".

## 7. Overall

The v7 fixes are correct in substance and labelled honestly. The ×5–50 is an assumption, it is stated as one, and it
points the right way. The (c) test on development estimates is a sound pre-freeze decision rule that cannot leak
credit into the result. Two statements put to the human at Gate A remain wrong or incomplete: B-1 and B-2. **Not yet**,
with blocking list {B-1, B-2}. Both are wording fixes (plus optional print lines) that a diff check can verify.
