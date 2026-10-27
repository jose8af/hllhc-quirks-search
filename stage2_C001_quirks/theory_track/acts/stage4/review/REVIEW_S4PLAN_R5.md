# Critical review R5 (narrow verifier): Stage-4 plan after fix R4 (`acts/stage4/plan.md`), C001 quirks theory track

Reviewer: S4PLAN-R5, a fresh critical reviewer, 2026-10-13. Role: `jfc/src/agents/critical_reviewer.md`; methodology
`01-core.md` and `03-review.md` §6.

Classification, as in R2-R4:
- **A** blocks or invalidates;
- **B** must be fixed in the plan before the user decides and before `WP_RULE.md` is frozen;
- **C** is minor.

The verdict is PASS only with 0 A and 0 B. Approved decisions (D4-1…D4-15, D4-17 (i), Mac only, the deadline, the
per-run cap) are not reopened.

**Scope.** This round checks whether R4's B-1 and C-1…C-6 are genuinely resolved, and whether fix R4 introduced a new A or
B. Inputs:
- `plan.md`: §0, §2.5, §2.6, §4.1, §4.2, §5, §6.2-§6.5, §10-§12 in full, and the header;
- `REVIEW_S4PLAN_R4.md`, `FIX_S4PLAN_R4.md`;
- `probes/f4r_deadline.py`, `probes/f4r_admissibility.py` and their JSON outputs;
- the LOG.md decisions of 2026-10-13;
- `sim/stage3/results/P2.json`.

The finder speed-up files were not read.

**Independent checks** (`data/acts_stage4/review_r5/r5_checks.py` → `r5_checks.json`; 0.05 CPU-s; system python3,
standard library only; no acts env, no finder, no simulation).

1. **Campaigns.** Re-implemented from the plan text of §6.2 and §4.2, without importing f3r or f4r:
   - C1 with C′;
   - the largest t₁ per campaign;
   - the decision-table rows, the G2b t₂,max and the G3 overrun of the schedule slot.
2. **Bethe and restricted loss in Si,** with the PDG constants fetched today from
   `pdg.lbl.gov/2024/AtomicNuclearProperties/MUE/muE_silicon_Si.txt`:

   | constant | PDG value |
   |---|---|
   | I | 173.0 eV |
   | ρ | 2.329 g/cm³ |
   | a | 0.1492 |
   | k | 3.2546 |
   | x₀ | 0.2015 |
   | x₁ | 2.8716 |
   | C̄ | 4.4355 |
   | δ₀ | 0.14 |
   | minimum ionisation | 1.664 MeV cm²/g at βγ ≈ 3.44 |

   K, Z/A and ρ cancel in every ratio used; ρ enters only through the Sternheimer parameters. The levels are re-evaluated
   at the median βγ_IT and per point (the max rule), with I ± 10 %, T_cut = 50, 100 and 200 keV, and βγ_μ = 10-300.
3. **Smoothed Λ_R(m),** evaluated independently from `P2.json` → `edge_fits_in_m`.
4. **The expected number of NI passes in C′_PU,** from the plan's own §4.2 factors.

**Hashes verified.**

| file | sha256 | matches |
|---|---|---|
| `P2.json` | `e63d19d8…b502442459` | the plan ✓ |
| `f4r_deadline.json` | `e8058663…34975bd04` | the fix report ✓ |
| `f4r_admissibility.json` | `45847697…13bda97a` | the fix report ✓ |

---

## 1. Status of the R4 items

| R4 item | Verdict | Evidence / residual |
|---|---|---|
| **B-1** C′ uncapped, its with-PU part uncosted | **Resolved as asked** | See *B-1 detail* below the table. Residual: the role of the 500-event size and a zero-count rule. This is new **B-1**, which comes from the sizing chosen in the fix. |
| Deadline schedule and decision table | **Arithmetic correct; consistent** | See *Deadline detail* below the table. Minor nits: C-3. |
| C-1 documentation lag (D4-17, cloud) | Resolved | See *C-1 detail* below the table. |
| C-2 βγ_IT source; smoothed Λ_R | Resolved | See *C-2 detail* below the table. |
| C-3 βγ range; Ẽ500; MIP unit | Resolved; conclusions confirmed with PDG constants | See *C-3 detail* below the table. Nits: C-2. |
| C-4 mixed admissibility | Resolved | §2.6 "Mixed admissibility" is the one sentence asked for. It is consistent with §2.5 item 5's "exactly one category" branch. |
| C-5 unequal-category range | Resolved | §2.5 item 5 reads "0.13-0.22". |
| C-6 D4-1 lean / (c) | Resolved | D4-1 offers (a), (d) and (m) only. "Lean" survives only as the superseded §6.2 record column, explicitly marked. |

**B-1 detail.**
- **Classification.** C′ is production inside C1. §0 l.179 and §11 item 5 say so, and C′ is gone from the "not capped"
  list.
- **Counts.** They are pre-defined: C′₀ ≈ 5.4 × 10⁵ events with no PU; C′_PU is 8 × 500 = 4 000 events with PU.
- **Costs, reproduced independently:**
  - C′ in total: 19.4 / 20.6 / 22.8 / 26.1 CPU-h at t₁ = 2 / 3 / 5 / 8 s;
  - C1: 91.3 / 106.6 / 137.1 / 182.9 CPU-h;
  - C1-C4: 315.2 / 391.6 / 544.6 / 774.1 CPU-h.
- **Largest t₁ for one Mac day:**
  - C1 7.02 s ("7.0 s"), and 8.79 s without C′ ("8.7 s before C′");
  - C2 5.64, C3 8.29, C4 6.11, C4′ 8.71, C5 10.68 s.
- **G2b.** C1 alone gives t₂,max = 134.6 / 95.6 s at t₁ = 3 / 5 s (plan: 135 / 96).
- **Consistency.** §0, §4.2, §5, §6.2, §10 D4-1 and §11 are consistent. In the §6.2 block table, C + C′ = 47 + 12 + 7 = 66
  ≈ 67.
- **Wording.** The §4.2 "no PU, fast" contradiction is gone.

**Deadline detail.**
- **Rows** (`r5_checks.json` → `deadline_rows`):

  | t₁ | set | Mac wall | margin |
  |---|---|---|---|
  | 2 s | C1-C4 | 45.0 h | 2.0 h |
  | 3 s | C1 + C2 + C4′ | 42.2 h | 4.8 h |
  | 5 s | C1 + C2 | 41.6 h | 5.4 h |
  | 7 s | C1 + C2-B | 43.4 h (with C2's 5 CPU-h of validation) | — |
  | 12 s | C1 | 34.9 h | — |

- **A3 and A4 at 2 s:** 1.0 h and 1.4 h ✓.
- **t₂,max per row:** 20.98 / 44.33 / 52.7 s ✓.
- **C1r** fits one Mac day up to 16.5 s, and fits the window as two runs up to 37.5 s ✓.
- **Gates and development:** 20.8 / 25.2 / 34.1 CPU-h ✓. The G3 pilot grows by 0.635 h of wall per +1 s of t₁ ✓.
- **Schedule blocks:**
  - block 9 (Fri 20 → Sat 14) is 18 h ✓;
  - block 12 is 4 h ✓;
  - block 8 has ≈ 8 h after the production stop ✓.
- **The slip rule** ("never out of blocks 8-12") is stated identically in §0, §11 (rules) and §12 risk 12.
- **The deferral order** C5, A3, A4, C3 is the same in §0, §5, §11 and §12. Risk 12 extends it with "then C4′, C2".
- **§12 risk 11** ("C3 deferred at t₁ ≳ 2.5 s") follows from the "next-slower row" rule ✓.

**C-1 detail.**
- D4-17 is marked approved in §2.6 (heading and alternatives) and in §10.
- "pending" survives only at D4-16, as intended.
- "PROPOSED" survives only in the R1 history line.
- The remaining cloud text is all "considered and dropped":
  - the header history (l.38-62);
  - the one §6.5 paragraph;
  - the D4-8 option list;
  - two "withdrawn" stubs, kept for numbering.

  No live cloud content is left. The brief allows one dropped-option note, and the header and stub lines are history. I
  accept this, and it is not a finding.

**C-2 detail.**
- The βγ_IT source is pre-declared: template half, counting set, per-event median, per-point median, then the median over
  Λ.
- The script reproduces `r1c_signal_handles.json` exactly at its 18 points.
- The output hash goes into `WP_RULE.md`.
- The smoothed Λ_R uses deg2 for E and deg1 for Ẽ. My evaluation agrees to ≤ 5 × 10⁻⁵ keV at all 17 species-masses. The
  fit's stored form is "ln(edge/keV) = Σ p_i (ln m − ln 500)^i", the convention the script uses.
- The max(median, per-point) rule is conservative in the right direction. A larger βγ means a lower R, which means fewer
  admissible dE/dx levels, so the hypothesis's signal is kept. The rule is deterministic and uses truth only.

**C-3 detail.** The script's Si constants are the Sternheimer (1984) set: C̄ 4.4351, x₀ 0.2014, x₁ 2.8715, a 0.14921.
They agree with the PDG 2024 values to ≤ 0.05 %. Re-run with the PDG constants (`r5_checks.json` → `bethe_PDG`):

| species-mass | R (pre-declared muon-gun unit) | e_adm (nominal) | e_adm range under variations |
|---|---|---|---|
| E200 | 1.07-1.14 | none | none |
| E300 | 1.30-1.39 | none | none |
| E400 | 1.38-1.49 | none | none |
| Ẽ200 | 1.08-1.16 | none | none |
| Ẽ500 | 1.46-1.57 | none | none |
| E500 | 1.68-1.81 | 1.3 | 1.3 |
| E600 | 1.64-1.77 | 1.3 | 1.3 |
| E700, E800 | 1.91-2.07 | 1.3 | 1.3-1.6 |
| E900 | 2.17-2.34 | 1.6 | 1.6 |
| Ẽ1000 | 2.10-2.26 | 1.6 | 1.6 |
| E1000 | 2.35-2.54 | 1.6 | 1.6-2.0 |
| E1100-E1500 | ≥ 2.63 | 2.0 | 2.0 |

**The plan's admissibility conclusions do not change:**
- there is no dE/dx level at E200-E400, Ẽ200 or Ẽ500;
- E500 gets 1.3;
- E900 and Ẽ1000 get 1.6;
- E1000 gets 1.6-2.0;
- E1100-E1500 get 2.0.

E500 sits at the 1.3 boundary **only in R4's mean/minimum convention** (R_BB = 1.619, so R/1.25 = 1.295). In the
pre-declared muon-gun unit its level is robust: R/1.25 = 1.34-1.44 across I ± 10 %, T_cut 50-200 keV and βγ_μ 10-300. The
mean-loss minimum is at βγ = 3.44, as in PDG.

---

## 2. Category A

None.

---

## 3. Category B

### B-1. C′_PU at 500 events per topology cannot measure P(pass | NI, DIF) for its role in the B sum. The stated deep-rung mechanism ("PU thinned") gives no reach at ρ = 1, and no zero-count rule exists for a C′ factor.

This was introduced by fix R4's sizing choice: "500 per topology is the size that fits C1 under the cap" (§4.2). No
precision requirement is stated.

**Evidence.**

1. **Expected counts, from the plan's own §4.2 NI factors.** The NI toy places the parent on the PV line. Per NI, the
   F0-level pass probability is about f₂ × P(coplanar) = (0.3-0.5) × (10⁻³-10⁻²) = 3 × 10⁻⁴ to 5 × 10⁻³.
   - In 500 events per r_NI that gives **0.15-2.5 expected passes** at the F0 level, before any width or χ²_core rung
     (`r5_checks.json` → `NI_CprimePU_expected_F0_passes_in_500`).
   - The plan's remedy, "< 10 passes in 500 → +50 % step", gives 750 events and 0.2-3.8 passes, so it cannot reach 10.
   - The DIF kink topology is similar: it fails N_IT2/N_OT2 without random refills.

   These are the topologies C′_PU exists for: "random crossings refill the missing inner hits of NI, DIF and conversions".
2. **"Deeper rungs come from … the PU interactions are thinned (§4.1 step 2)" (§4.2, the C′_PU bullet) gives no reach.**
   - Exact k-thinning maps a density-ρ superposition onto density 1 with weights ρ^−k. It gains depth only from ρ ≥ 2
     samples.
   - C′_PU, like the SM samples C, exists only at ρ = 1. Thinning a ρ = 1 sample gives densities < 1, not deeper rungs at
     ρ = 1. T1 (ρ = 2 → 1) cannot be evaluated on these samples.
   - The same sentence has stood for the SM hard-scatter candidates since R1 ("extrapolated with the same thinning … with
     tests T1/T3 … on that sample"). It is the same flaw, pre-existing, and the same text fix covers it.
   - The only valid depth mechanisms here are:
     - rung-to-rung factorisation with T3 on the sample;
     - the C′₀ factorisation of h, o and dE/dx.
3. **No pre-declared treatment of a zero-count factor.**
   - §2.5 item 4 gives each B term a central value and a log-normal σ_ln. A factor with N_pass = 0, in C′_PU or in a C′₀
     conditional, has no log-normal central value.
   - Entering it as 0 is anti-conservative and would let a background-free claim rest on missing information.
   - Entering it as the 95 % CL value (3/N) gives, for NI, B ≈ 26 NI/event × 0.22 × 3/500 × 10⁻⁴ (the C′₀ zero-count
     value) × 3.3 × 10⁷ ≈ **10² events**, far above 0.11, so no category would have a WP.
   - The plan has to say which applies before the freeze. The outcome then follows from a pre-declared rule and not from
     a post-hoc choice.

**Required fix** (text and design; no compute; C1 cost unchanged):
1. **Replace the thinning claim** in the §4.2 C′_PU bullet, and in the SM hard-scatter sentence of §4.2, with what is
   actually available at ρ = 1:
   - rung factorisation (§4.1 step 3) from the deepest rung with ≥ 10 counts in the sample, with T3 on that sample;
   - h, o and dE/dx factorised from C′₀.

   Thinning on these samples is at most a k-decomposition diagnostic, and T1 is not applicable to them.
2. **Make the NI × 3 and DIF with-PU samples measure the conditional they are needed for.**
   - *Preferred: importance sampling.* Overlay on PU only toy configurations that pass a pre-declared no-PU, toy-level
     candidate-geometry preselection (≥ 2 prongs within the band of the PV plane, reaching the OT). Weight them by the
     preselection fraction, which C′₀ measures with 3 × 10⁴ (NI) or 5 × 10⁴ (DIF) events. The 500 events then measure
     P(F0/width/χ²_core rungs | preselected topology, PU) with O(10²) loose-rung counts. The preselection is independent
     of the PU, so the weight is exact.
   - *Alternative:* enlarge those 4 samples. This costs +1.9 CPU-h per +1 000 events at t₁ = 2 s, and it must then be
     re-fitted into the decision-table margins.
3. **Pre-declare the zero- and low-count rule for every C′ (and SM C) factor.** For example: a conditional with
   N_pass = 0 enters at its 95 % CL value 3/N with a pre-declared σ_ln, never 0; terms dominated by such a value are
   flagged in the B table; if that makes B₈₄,c > 0.11, the §2.6 fallback applies. Record it in §2.5 item 4 and in
   `WP_RULE.md`.
4. Keep §0, §4.2, §5 and §11 item 5 consistent with the result.

---

## 4. Category C

- **C-1. Attribution of C′_PU and C candidates.**
  - "Only candidates with ≥ 1 in-band hit from the gun/toy particles count." At the normalised density there are
    ≈ 1.1 × 10⁵ candidates per trial, so many pure-PU candidates contain one incidental gun hit. They are then counted in
    B_t and again in B_PU. With Σ rate_t ≈ 30 per event (NI alone ≈ 26), even a few % incidental inclusion inflates the
    C′ terms to O(1) × B_PU.
  - This is conservative, so it costs efficiency and not validity.
  - Consider requiring the gun/toy particles to supply ≥ 2 crossings in at least one IT + PS layer of the candidate, or
    the core, mirroring the k = 1 attribution of B1.
- **C-2. dE/dx wording and citation (§2.6).**
  1. The max rule changes a level beyond "Λ ≲ 0.6 keV": Ẽ1000 goes 1.6 → 1.3 at 0.6 and 0.7 keV, and E1100 goes
     2.0 → 1.6 up to 0.5 keV (`r5_checks.json` → `maxrule_level_changes`, 24 point-levels in total). Write "Λ ≲ 0.7 keV".
     Also qualify "flat within a few % for Λ ≳ 0.6 keV": Ẽ1000 is +8 % at 0.7 keV.
  2. The Si constants are now verifiable. Cite the PDG 2024 Si table, drop "recalled, UNVERIFIED", and note that K, Z/A
     and ρ cancel in R.
  3. "Borderline" for E500 applies only to R4's mean/minimum convention. In the pre-declared unit, 1.3 is robust at the
     median βγ, and it is lost only at Λ ≤ 0.45 keV through the max rule.
- **C-3. Schedule nits (§11).**
  1. "47 net (50 gross)": the 3 h deduction is not explained. The `f4r_deadline.py` docstring says "Wed 14 13:00 → Fri
     16 12:00 = 47 h", while the plan says the window starts Wed 10:00. Harmonise them, e.g. "3 h for inter-campaign
     reports and approvals".
  2. The G3 pilot overruns block 5's 4-h slot for t₁ ≳ 5.4 s: by 1.0 h at 7 s and 4.2 h at 12 s. The slip rule covers
     this, and the margins stay positive (3.3 h at 7 s, 8.0 h at 12 s), but only the > 16.5 s row mentions the longer G3.
  3. No rule is given for a slip that shrinks the window below the row's C1. Say that the next-slower row's content then
     applies (C1a/C1b, then C1r).
  4. A1 appears in both G2 (block 4, "all of A1 + V4-3") and the C1 contents. State that C1 reuses the G2 A1 output
     (2 CPU-h; it does not change any row).

---

## Verdict

**ITERATE.** 0 Category A, 1 Category B, 3 Category C.

R4 B-1 (classification, counts, t₁-dependent cost, propagation) and R4 C-1…C-6 are genuinely resolved. All campaign,
deadline-row, t₁,max, t₂,max and gate numbers reproduce independently from the plan text. The admissibility conclusions
hold with the PDG Si constants. The one new B concerns the role of the 500-event C′_PU samples:
- for NI and DIF, the plan's own factors predict ≲ 3 F0-level passes;
- the stated thinning mechanism gives no depth at ρ = 1;
- zero-count factors have no pre-declared treatment.

It is a text and design fix (importance-sampled preselection, factorisation-only depth, a zero-count rule) with no change
to cost, schedule or approved decisions.
