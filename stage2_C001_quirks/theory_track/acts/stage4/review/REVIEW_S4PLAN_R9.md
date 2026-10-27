# Critical review R9 (narrow verifier): Stage-4 plan after fix R8 (`acts/stage4/plan.md`), C001 quirks theory track

Reviewer: S4PLAN-R9, a fresh critical reviewer, 2026-10-13. Role: `jfc/src/agents/critical_reviewer.md`; methodology
`03-review.md` §6.

Classification, as in R2-R8:
- **A** blocks or invalidates;
- **B** must be fixed in the plan before the user decides and before `WP_RULE.md` is frozen;
- **C** is minor.

The verdict is PASS only with 0 A and 0 B. Approved decisions are not reopened.

**Scope.** This round checks whether R8 B-1, C-1 and C-2 are resolved, and whether fix R8 introduced a new A or B.

**Inputs.**
- `plan.md` (2109 lines, mtime 15:21:57): header R6/R7/R8 bullets (l.83-116), §2.1 band (l.424-427), §2.2 steps 2-4
  (l.479-503), §2.5 item 9 (l.840-846), §4.1 (l.1058-1262, incl. the method table and storage paragraph l.1134-1150 and
  row-major A2 l.1249-1254), §4.2 overlay, preselection, "why exact", attribution and the R7 C-4 note (l.1316-1423),
  §8 V4-10 (l.1815), §11 item 5 (l.1952-1957);
- `REVIEW_S4PLAN_R8.md`, `FIX_S4PLAN_R8.md`.

The finder speed-up files were not read.

**Method.** Grep and reading only, < 0.001 CPU-h:
- every occurrence of `δn`, `δn_fit`, `δn_max`, `σ_tot`, `cap`, `satisf`, `normal-uncertainty`, `merg` and `insert` was
  listed and read in context;
- no scratch data was needed.

---

## 1. Status of the R8 items

| R8 item | Verdict | Evidence |
|---|---|---|
| **B-1** frozen σ_tot ambiguous (δn = 0 vs min(δn_fit, 2 mrad)) | **Resolved** (option (a)) | See *B-1 detail* below. |
| C-1 "merged" vs "inserted" | Resolved | See *C-1 detail* below. |
| C-2 merged-hit attribution | Resolved | See *C-2 detail* below. |

**B-1 detail.** σ_tot² = σ_n² + t_tol² with δn = 0 is now the only frozen definition, and is stated identically
everywhere it appears:

| Place | Line | Text |
|---|---|---|
| Header R6 bullet | l.83-84 | "σ_tot has no δn term since fix R8" |
| Header R8 block | l.109-113 | "σ_tot² = σ_n² + t_tol², with no normal-uncertainty term (δn = 0), is the frozen finder definition" |
| §2.1 band | l.425 | "σ_tot² = σ_n² + t_tol², δn = 0: the frozen definition of §2.2 step 3" |
| §2.2 step 3 | l.485-491 | the definition, labelled "the frozen nominal" |
| §2.5 item 9 | l.842 | "σ_tot with δn = 0 (§2.2 step 3; fix R8)" |
| §4.2 σ̂_h paragraph | l.1337 | "σ_tot has no δn term (δn = 0, §2.2 step 3)" |
| §4.2 attribution | l.1405-1406, l.1417, l.1419 | "σ_tot has no δn term" |

The early F0 summary (l.170, "±3σ_tot (resolution ⊕ 30 µm thickness tolerance)") is consistent with this. §4.1 does not
define or use σ_tot (no `δn`/`σ_tot` hit in l.1058-1262), so it cannot contradict it. See C-1 below.

The capped δn_fit survives only as a pre-declared variation, and nowhere as the default:
- §2.2 step 3 (l.492-495): "*Pre-declared variation (not the default):* δn = min(δn_fit, δn_max) … run in A5/B1 beside
  t_tol = 0/100 µm";
- header l.111-112: "is only a pre-declared A5/B1 variation";
- the R7 header bullet (l.96-98) is the history record, explicitly marked "**superseded in fix R8**: σ_tot has δn = 0";
- the other mentions (l.1347 "under the capped-δn variation", l.1419 "under the capped-δn variation δn ≤ δn_max") are
  labelled as the variation.

δn_max = 2 mrad now enters only σ̂_h:
- the σ̂_h² formula (l.1334);
- §2.2 l.490-491 ("enters **only** σ̂_h");
- the R7 C-4 note (l.1419-1420, the ≈ ±8 mrad margin of σ̂_h);
- the variation's cap.

No instance remains of "satisfies the cap" or "caps δn" (as a definition), and none of σ_tot carrying δn_max as nominal.

**Inequality checks.**
- σ_tot,h ≤ σ̂_h with δn = 0: σ_n(n, hit) ≤ σ_loc,max,h, and t_tol is common to both. This holds trivially, and also for
  2S hits, where σ_loc,max is the along-strip σ.
- Under the variation: (δn·|u|)² ≤ (δn_max·|u|)², with the same |u| about the same stored PV. So the l.494-495 claim is
  correct.

**f_pre exactness (l.1341-1347) is correct and does not depend on σ_tot.**
- An attributed candidate has passing toy-linked stored positions in ≥ 3 distinct layers, from ≥ 2 particles, each within
  ±4σ̂_h of the candidate's PV plane.
- Choosing one hit per layer in three of those layers, and swapping in a second-particle hit where needed (in its own
  layer, or replacing one of the three), always gives a triple from 3 distinct layers and ≥ 2 particles. That triple has
  Σ(n·u)²/σ̂_h² ≤ 48 about the candidate normal, so λ_min ≤ 48.
- The triple uses the same σ̂_h, the same stored PV and the same stored pre-merge, pre-CKF measurements as the
  preselection (l.1324-1329).
- σ_tot and δn never enter. The plan states this explicitly: "never σ_tot, so it holds for any δn in σ_tot".

**No ripple into the numbers.** Every number stated to rest on δn = 0 (T_seed, μ_c, the margin study, t₁, the §4.1
storage figures) was already a δn = 0 number. That is R8's premise, from `f1r_finder.py`.

**C-1 detail.**
- The toy hits put into the PU event are now "inserted" in all three places: header l.84, §4.2 overlay l.1318-1319, and
  §11 item 5 l.1955 ("the C′_PU job inserts the stored C′₀ toy hits").
- Every remaining "merg*" in the plan refers to something else:
  - U-5 b analysis-level merging (l.167, 248, 341-350, 1252, 1324-1328, 1407-1408);
  - doMerge = False;
  - the 2-mrad candidate merge;
  - the O(N²) duplicate-merge loop;
  - the merged regime.
- l.1252 (row-major A2: Stage-3 hits "appended to the PU measurements, merged at analysis level (U-5 b)") is correct U-5 b
  usage.

**C-2 detail.** The added sentence is at l.1407-1410: "tested at each of its toy-linked stored C′₀ positions, never at its
merged position; this cannot leak, since the preselection uses all stored toy measurements".
- It is consistent with the overlay hand-over (l.1324-1329) and with the R8 header bullet (l.114-115).
- See C-2 below for an optional sharpening of the particle credit.

---

## 2. Category A

None.

---

## 3. Category B

None.

---

## 4. Category C

- **C-1 (fix-report wording, no plan action needed).** `FIX_S4PLAN_R8.md` says the "§4.1 storage column" is "now labelled
  explicitly as δn = 0".
  - §4.1 itself (l.1058-1262) carries no δn label.
  - The label exists only by reference: §2.2 step 3 l.487 and header l.110 say the §4.1 storage rests on δn = 0.
  - This is harmless. §4.1 neither defines nor uses σ_tot, so it cannot be read the other way.
  - *Optional:* add "(δn = 0, §2.2 step 3)" after "candidates" in the storage paragraph (l.1140-1141), or correct the fix
    report.
- **C-2 (optional sharpening of the C-2 sentence).** l.1407-1410 tests a toy-toy merged measurement "at each of its
  toy-linked stored positions". It does not say explicitly that each passing link counts as a hit **of its own particle
  only**.
  - The natural reading is per-link credit, and under it no leak is possible: the passing links are a subset of the
    stored toy measurements that the preselection scans.
  - A reading in which the measurement passes if any link passes, while being credited to all of its linked particles,
    could count a second particle that has no passing stored hit. That would violate "attribution ⇒ preselection" in a
    rare toy-toy-merge edge case. V4-10 on C′₀ would partly catch it empirically.
  - *Optional fix (one clause):* "…each toy link counting as a hit of its own particle only if its own stored position
    is within ±4σ̂_h."
  - Freeze it in `WP_RULE.md` with that wording.

---

## Verdict

**PASS.** 0 Category A, 0 Category B, 2 Category C (both optional).

R8 B-1 is resolved by option (a).
- σ_tot² = σ_n² + t_tol² (δn = 0) is the single frozen definition. It reads the same in the header, §2.1, §2.2 step 3,
  §2.5 item 9 and §4.2, and §4.1 does not define σ_tot.
- The capped δn_fit appears only as a labelled, pre-declared A5/B1 variation, plus a history bullet marked superseded.
- δn_max = 2 mrad enters only σ̂_h.
- σ_tot,h ≤ σ̂_h holds trivially.
- The f_pre exactness argument is correct and independent of σ_tot.

R8 C-1 and C-2 are resolved, and fix R8 introduced no new A or B.
