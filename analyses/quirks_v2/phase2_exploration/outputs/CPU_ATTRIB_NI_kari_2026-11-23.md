# C′_PU attribution, NI 22 mm: v1's link rule vs the frozen own-hit rule j ≥ n/2 (result)

Kari (executor, Opus; successor of Eskil), 2026-11-23 16:26 -0500. This is the read of the NI addendum to Eskil's frozen
plan (`CPU_ATTRIB_PLAN_eskil_2026-11-19.md` l.56-73, written before generation). The plan, the rules, the rungs and the
script are **unchanged**: `src/cpu_attrib.py` as committed (its glob already includes `p2-a-c1-cppuni-[ab]`, l.59-60).
Output: `cpu_attrib_ni_kari_2026-11-23.json` (all classes, 150 files). I ran it on landau at nice 19: 3 min 54 s wall,
78 CPU-s, max RSS 1.73 GB (`/usr/bin/time -v`). No signal file was opened.

## 1. Headline
- **NI 22 mm at R05 (the NI test rung): 2 of 82 v1-attributed candidates pass j ≥ 4. ρ_NI = 0.024. Both come from one
  slot (one source event) of 1,000** [VERIFIED counts, json l.1064-1073, l.1113]. Clustered bootstrap 16/50/84 %:
  0 / 0.022 / 0.047, with ρ = 0 in 37 % of the replicas. The event-level 95 % UL is 4.74/37 = **0.13** (ESTIMATE, the
  same method as Eskil's).
- **R06: 0 v1-attributed and 0 j ≥ 4 candidates** (v1 also had 0 per 500) [VERIFIED, json l.1123-1132].
- As for DIF, γ, V⁰ and the PV pair, no candidate passes j ≥ 4 without also passing v1's rule (N_j_only = 0 at every rung).
- At R05, 85 % of v1's NI candidates (70/82) are **pure pile-up** (j = 0), 12 % are **mixed** and 2 % are attributed.
- **Expected NI test count at R05: ≈ 2 attributed per 1,000 unbiased events, not 92** (95 % UL ≈ 5 slots) [ESTIMATE].
  With so few events the NI R05 ceiling test has almost no power. This is a strategy-revision input (§4).

## 2. Sample, cost and checks
- **Sample.** `p2-a-c1-cppuni-a` (13 jobs) and `-b` (12 jobs), 25 × 40 = 1,000 slots in total, from 1,000 distinct source
  C′₀ ni22 events (n_clusters = 1,000, json l.944). Every slot is therefore its own cluster. All 25 jobs `done`, 0
  failed (markers under `ledger/markers/p2-a-c1-cppuni-[ab]/000/`; drivers `finished`).
- **CPU (stop rule, 9 CPU-h).** The 25 done attempts used 25,427 CPU-s = **7.06 CPU-h** [VERIFIED, sum of `cpu_s` in the
  done marker lines]. The two attempts killed by the power loss (006, 015) add at most 0.16 h, taken as their wall time
  from `started` to 19 Nov 17:54:50, an upper bound. Total ≤ 7.22 CPU-h, under the ≈ 7.2 projected in the plan (l.63) and
  under the 9 CPU-h stop. The mean job was 1,017 CPU-s and the longest 1,068 CPU-s, against the 1,033 s per 40 slots
  that the plan assumed.
- **Reproduction of Eskil's read.** The DIF, γ, V⁰ and PV-pair counts (N_v1, N_j, overlap, N_pass) at all four rungs are
  identical to `cpu_attrib_eskil_2026-11-19.json` [VERIFIED, scripted comparison, 0 differences]. The checks are
  clean on all 150 files: the crossings recomputed from the hit records match the stored `cand.cross` on 415,996 records
  (0 bad), with 0 rung-flag mismatches and 0 v1-attributed R04 candidates missing from `cand` (json l.3).
- **v1-rule counts against v1.** Per 1,000 slots this sample gives R02 6,918, R04 309 and R05 82. v1 gave 3,915, 127
  and 46 per 500 (`stage2_C001_quirks/theory_track/data/acts_stage4/analysis/C12FC_v1/background.json` → `cprime.ni22`,
  l.38346 ff.), i.e. 7,830, 254 and 92 per 1,000 [VERIFIED read]. The relative differences (−12 %, +22 %, −11 %) lie
  within the clustered relative error on N_v1 (0.17, 0.24, 0.22; json `s_rel_Nv1_clustered`) [ESTIMATE judgment].
- **Merged-hit labelling.** In the recorded v1-attributed candidates there are 543 own-INT hits against 546 pre-merge core
  links, so the labelling hides about 0.5 % of own hits [VERIFIED, json `sum_*_v1_rec`].

## 3. Counts (NI 22 mm, M = 1,000 slots = 1,000 clusters)
| rung | N_v1 | N_j (j ≥ 4) | overlap | v1 only | j only | clusters v1 / j | ρ = N_j/N_v1 | ρ bootstrap 16/50/84 % | event-level 95 % UL on ρ |
|---|---|---|---|---|---|---|---|---|---|
| R02 | 6,918 | n.e. (c) | — | — | — | 330 / — | — | — | — |
| R04 | 309 | 2 (b) | 2 | 307 | 0 | 71 / 1 | 0.0065 (lower bracket) | 0 / 0.006 / 0.014 | < 4.74/71 = 0.067 (recorded part) |
| **R05** | **82** | **2** | 2 | 80 | 0 | 37 / 1 | **0.024** | **0 / 0.022 / 0.047** | **< 4.74/37 = 0.13** |
| R06 | 0 | 0 | — | — | — | 0 / 0 | n/a (v1: 0/500) | — | — |

All counts are VERIFIED (json l.946-1132). The ρ values and their quantiles are VERIFIED as computed. The ULs are
ESTIMATE: Poisson 95 % on 1 cluster = 4.74, divided by the clusters that hold a v1 candidate.
(b) **The R04 value is a bracket.** 227 of the 309 v1-attributed R04 candidates have no hit record (v1 writes records
only for w_core < 37.5 or p > 10⁻³), so j is known on 82 of them. Bracket [2, 2 + 227 = 229]. The loose link bound
(max_cross ≥ 2 and ≥ 4 link layers) gives 44 in 14 clusters at R04. In the complete R05 sample the same bound gives 10,
against the 2 that actually pass.
(c) Below R04 only a 1 % sample has hit records, so j is NOT EVALUABLE at R02. The script's R02 N_j = 2 counts only the
recorded R04 passers.

**j of the v1-attributed candidates at R05** (j = 0 / 1 / 2 / 3 / 4 / 5): 70 / 7 / 2 / 1 / 0 / 2 (json `j_hist_v1`).
max_cross of the v1-attributed R05 candidates: 66 have 1, 12 have 2, 4 have 3.
Under STR l.747-753 this sorts them into pure pile-up 85 %, mixed 12 % and attributed 2 %. Eskil's table for
comparison: DIF 100 / 0 / 0, γ 34 / 60 / 6, V⁰ 67 / 28 / 4.

## 4. Implications (all ESTIMATE; v1 placeholder efficiencies as in Gate A; no v2 signal efficiency used)
**Revised estimate of the attributed conversion-led term against Gate A's 0.7–1.0×10⁴** (GATE_A.md l.13-14; STR l.980:
conversions 9,530, or 6.4×10³ with v1's N_trig-weighted photon rate, plus DIF 385–647, total 9,929–10,193 central).
- **Conversions** × ρ_γ. ρ_γ is not changed by this run: 0.057 at R05 and 0.091 at R06 (`CPU_ATTRIB_eskil_2026-11-19.md`
  l.42-43), with an event-level UL of 0.22. This gives 540–870 (3.6–5.8×10² on the 6.4×10³ variant); 2.1×10³ at the UL.
- **DIF** × ρ_DIF. 0 at R05 (UL 0.064, Eskil l.39), so DIF contributes < 25–41.
- **NI.** STR l.980 does not list NI as a separate entry. The 14–16 events left after conversions and DIF are not
  decomposed there (UNVERIFIED what they hold). If NI is part of them, ρ_NI ≈ 0.024 (UL 0.13) leaves < 1 event (< 2
  at the UL). NI does not change the total at the stated precision.
- **Attributed total ≈ 4×10²–9×10² events** (central over both photon-rate variants; 5.4–8.7×10² on the central
  9,530), instead of 0.7–1.0×10⁴. The upper end is ≈ 2.2×10³ at the γ UL. In 37 % of the γ replicas it reaches about 0.
  The NI result **confirms Eskil's estimate and does not move it**. The γ ratio still rests on one source event.
- **Caveat (unchanged and dominant).** These numbers are the size of the *attributed* term. They are not the selected
  background. For NI, 12 % of v1's candidates become mixed (bounded only by the completeness test, STR l.751-752) and 85 %
  become pure pile-up (B2). Gate A's range remains an upper envelope (attributed + mixed + pure pile-up).

**NI test (STR l.1054-1059, Table 4.4b l.1068).** The R05 test on 1,000 unbiased full-pile-up events per radius was
sized at 92 / 120 / 378 attributed candidates, taken from v1's rule.
- **22 mm, measured:** ≈ 2 attributed per 1,000 events (here 2 candidates in 1 slot). The 95 % UL is 4.7 slots per
  1,000 [VERIFIED count; UL ESTIMATE]. At R06 the count is 0, as in v1.
- **30 and 61.5 mm, not measured:** by analogy with 22 mm (ρ ≈ 0.024, UL 0.13) the expected counts are ≈ 3 (UL 15) and
  ≈ 9 (UL 48) instead of 120 and 378 [ESTIMATE, analogy only; the NI multiplicity grows with radius, so the 61.5 mm
  value is the least certain].
- The claim that "the criterion gets a verdict at no extra cost" (l.1057-1058) therefore does not hold under the frozen
  rule at 22 mm and probably not at 30 mm. This is a strategy-revision input for Phase 3, in the same way as Eskil's
  DIF R06 finding (31 → ≈ 0). The NI S and promotion width derived at R04 (l.1056) are not affected by this
  measurement. I make no recommendation on the redesign here: the plan does not cover one, and a redesign is not a
  change to the frozen read.

## 5. Line of v1's C′_PU link rule (coordinator request)
`stage2_C001_quirks/theory_track/acts/stage4/finder/g1b_tt.py`, v1 commit **d724a1c** (the only commit touching the
file). The rule is at **l.354-355**: `base = len(li) >= 3 and nly[c] >= 3 and bool((lay <= 6).any())` and
`att[c] = base and (mcr[c] >= 2 if looper else npt[c] >= 2)`. The 4σ link cut is at l.344 and `NSIG_ATTR = 4.0` at
l.47; `def attribute` starts at l.300 [VERIFIED, read]. The v2 copy `analyses/quirks_v2/acts/stage4/finder/g1b_tt.py` is
byte-identical (sha256 a2e4ddffe751…). l.356-357, as cited by STR and LOG 19 Nov 15:37, is the comment of the
preselection positive control, not the rule. So Eskil's l.354-355 is correct.

## 6. Open issues
1. **More γ source events: NOT RUN, and no run is defined.** The addendum (plan l.70-73) states that v1's gun topologies
   allow only C′₀ events g < CPPU_N = 500 as sources and that C1's 1,000 γ slots already use all 500. A run with more
   γ sources would need new C′₀ γ events or a change to v1's source rule: that means a new plan and a new approval, and
   it is not within the approved NI budget. ρ_γ (one source event) stays the weakest input of the revised estimate.
2. NI at 30 and 61.5 mm has no C′_PU sample, so it is covered by analogy only (§4).
3. The NI R05 test sizing (STR l.1054-1059) needs revising in Phase 3 (§4).
