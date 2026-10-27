# Fix report R4: Stage-4 plan (`acts/stage4/plan.md`), C001 quirks theory track

Fixer R4, 2026-10-13.

**Inputs:**
- `review/REVIEW_S4PLAN_R4.md` (0 A, 1 B, 6 C, plus the "Fit to the 4.5-day deadline" section), with the reviewer's
  scratch in `data/acts_stage4/review_r4/` (`r4_checks.json`, `r4_deadline.json`);
- the user decisions of 2026-10-13 (LOG.md):
  - D4-1…D4-15 as recommended, including D4-10 (a′), D4-13, D4-14 and D4-15;
  - D4-17 option (i) approved;
  - the cloud dropped (Mac only);
  - the deadline: Stage 4 (production, analysis, review), the Stage-5 figures with the final summary, and a short
    Stage-6 feasibility note, all by Saturday 2026-10-17 night;
  - the per-run ≲ 1-day cap still applies;
  - the Stage-5 label approved.

**What was done:**
- The plan was edited in place.
- New scripts:
  - `acts/stage4/probes/f4r_deadline.py` (arithmetic only; it reuses the block costs of `f3r_campaigns.py`), output
    `data/acts_stage4/fix_r4/f4r_deadline.json` (sha256 `e8058663…34975bd04`);
  - `acts/stage4/probes/f4r_admissibility.py` (Stage-3 truth only), output `fix_r4/f4r_admissibility.json` (sha256
    `45847697…13bda97a`).
- **Compute: ≈ 0.003 CPU-h.** The admissibility script reads the 307 p2 points in 12 s, in the TT env; the rest is
  arithmetic.
- No acts-env use, no install, no simulation, no PU, no detector-level signal look.
- The finder speed-up files (`acts/stage4/finder/`, `data/acts_stage4/g2/`, `acts/stage4/G2A_REPORT.md`) were not touched.

## Items

| # | Finding | Status | What changed (plan section) |
|---|---|---|---|
| B-1 | C′ feeds the B sum but was classed as uncapped development; its with-PU part was never sized or costed vs t₁ | **RESOLVED** | See *B-1 detail* below the table. |
| Deadline | Replace the §11 timeline with a schedule; campaign-vs-t₁ decision table | **DONE** | §11: new deadline schedule (12 blocks) + decision table; old timeline removed. §0 deadline paragraph; §12 new risk 12. Detail below. |
| C-1 | Lag from today's decisions (D4-17, cloud) | RESOLVED | D4-17 marked approved in §2.6 (heading, alternatives paragraph) and §10. Cloud withdrawn: §6.5 reduced to one paragraph (considered and dropped, nothing ever created); D4-8 = (a) Mac only; Mac + cloud columns, "largest t₁" cloud values and G2b cloud t₂,max removed from §0, §2.4, §6.2, §11; "≈ 280 CPU-h" removed; §6.4 status updated; §11 item 6 and §12 risk 10 left as one-line "withdrawn" stubs, to keep the numbering. Remaining "cloud" hits are the header history and these stubs. |
| C-2 | βγ_IT(m) not published; per-mass vs smoothed Λ_R(m) | RESOLVED | See *C-2/C-3 detail* below the table. |
| C-3 | Wrong βγ range; Ẽ500 has no dE/dx level; MIP unit vs Bethe minimum | RESOLVED | See *C-2/C-3 detail* below the table. |
| C-4 | Mixed admissibility branch | RESOLVED | §2.6 "Primary result" adds the sentence: if r*_c is admissible for only one category, the pair is (r*_c, r_fb,c′). The "exactly one category has a WP" branch of §2.5 item 5 applies: the background-free claim is made for the admissible category alone, and the other bin enters at r_fb with its own B. |
| C-5 | Unequal-category range | RESOLVED | §2.5 item 5: "0.13-0.22 if the two categories are unequal, for B₈₄,G = 5-50 % of B₈₄,T" (`f3r_split.json` → `unequal`: 0.125 / 0.161 / 0.218). |
| C-6 | D4-1 options (b) lean and (c) not in campaign terms | RESOLVED | See *C-6 detail* below the table. |

### B-1 detail: C′ as production

**Classification.** C′ is production. It runs inside C1 (§0, §4.2, §5, §6.2, §11 item 5); it is no longer in the
"not capped" list.

**Counts, pre-defined now (§4.2):**
- **C′₀, no PU:**
  - γ, K⁰_S/Λ, PV-pair and looper guns, 10⁵ events each;
  - the NI toy, 3 × 10⁴ events per r_NI ∈ {22, 30, 61.5 mm};
  - the DIF toy, 5 × 10⁴ events;
  - ≈ 5.4 × 10⁵ events in total, **≈ 12 CPU-h flat** (review R3's S-cap value).
- **C′_PU, with PU:** 8 topologies (γ, V0, PV pair, looper, NI × 3 r_NI, DIF) × 500 events = **4 000 events**. Each is a
  TDR-normalised PU-200 event plus the gun/toy particles, with 1 road. The cost is that of an SM event, 4 000 × (4.7 + t₁) s.

| t₁ (s) | 2 | 3 | 5 | 8 | 10 | 20 |
|---|---|---|---|---|---|---|
| C′_PU (CPU-h) | 7.4 | 8.6 | 10.8 | 14.1 | 16.3 | 27.4 |
| C′ total (CPU-h) | 19.4 | 20.6 | 22.8 | 26.1 | 28.3 | 39.4 |

- For comparison, review R4's quote: 10⁴ with-PU events would cost 19 / 27 / 41 CPU-h and 10⁵ would cost 186 / 269 /
  408 CPU-h at t₁ = 2 / 5 / 10 s (reproduced in `f4r_deadline.json` → `Cprime_cost_vs_t1`).
- **Method for the with-PU part:** the gun/toy interaction is always kept and the PU is thinned, as for the SM
  hard-scatter candidates. h, o and dE/dx are factorised at ρ = 1 from C′₀, with T3 where counts allow. Only candidates
  with ≥ 1 gun/toy hit count. A +50 % step is available as a separate approved run if < 10 passes in 500.
- **Neighbourhood fix:** the γ, V0 and looper guns now also get a with-PU subsample. The same PU refilling of missing
  inner hits that the NI paragraph describes applies to them.
- §4.2 no longer says "≈ 10-15 CPU-h (no PU, fast)" next to "with PU". The PV-pair gun line now reads "10⁵ without PU
  and 500 with PU".

**Effect on C1** (`f4r_deadline.json` → `campaigns`, `t1_max_one_mac_day`):
- C1 = 91 / 107 / 137 / 183 CPU-h at t₁ = 2 / 3 / 5 / 8 s (was 72 / 86 / 114 / 157).
- **C1 fits one Mac day up to t₁ = 7.0 s** (was 8.7 s).
- C1-C4 = 315 / 392 / 545 / 774 CPU-h (was 296 / … / 748).
- C2-C5 are unchanged.
- Pre-defined sub-runs: C1a (A1, A2, A5, C′; one day up to 36 s) and C1b (B1, B2, C; up to 12.3 s).
- G2b examples: C1 t₂,max = 135 s at t₁ = 3 s and 96 s at t₁ = 5 s (was 136 s at 5 s, before C′).
- The t₁ = 8 s example was removed: C1 no longer fits at 8 s.
- The §6.2 reconciliation now reads 315 vs ≈ 330 (validation 30 vs 40; A5 32 vs 30; block total 326 rounded up).

**Propagated:** §0 table and text; §2.4 reference speeds; §6.1 finder row; §6.2 (block-table C + C′ basis,
reconciliation, speed and cap, contents, cost table, largest t₁, not-capped list, gates); §10 D4-1/D4-16; §11 G2a/G2b,
items 5-7; §12 risk 1. `grep "8.7 s"` now hits only C4′ (8.7 s, a coincidence) and the history note "(8.7 s before C′
was added)". "296", "522", "748", "136 s" and "84 s" have no hits left.

### Deadline schedule and decision table (§11, new)

**Schedule (targets, ESTIMATE).**

| # | Block | When | Wall h | Mac |
|---|---|---|---|---|
| 1 | Plan R4 fix → R5 review → plan PASS | Tue 16:00-21:00 | 5 | none |
| 2 | G1/G2a speed-up (running) | now → Tue 22:00 | — | light |
| 3 | WP_RULE freeze; G2a report; user scope choice | Tue 21:00-23:00 | 2 | none |
| 4 | G1 final + G2 (A1/V4-3, V4-5, G2b) | Tue 23:00 → Wed 01:00 | 2 | full |
| 5 | G3 pilot (closure tests) | Wed 01:00-05:00 | 2-4 | full |
| 6 | G3 report; C1 approval | Wed 05:00-10:00 | 5 | light |
| 7 | Production window | Wed 10:00 → Fri 12:00 | 47 net | full |
| 8 | Stage-4 analysis (on C1 from Thu; final on the union) | Wed → Fri 20:00 | concurrent + 8 | light |
| 9 | Stage-4 review loop (R1 critical + constructive → fixer → R2) | Fri 20:00 → Sat 14:00 | 18 | light |
| 10 | Stage 5 figures (approved label) + final summary | Sat 08:00-18:00 (scripts from Thu) | ≈ 10 | light |
| 11 | Stage 6 feasibility note | draft Wed-Thu; final Sat 14:00-20:00 | ≈ 3 | none |
| 12 | Buffer / handover | Sat 20:00-24:00 | 4 | — |

Reviews and analysis are agent work and run concurrently with the Mac. A slip before production comes out of the
production window through the deferral order, never out of blocks 8-12.

**Decision table** (window 47 h ≈ 329 CPU-h). The deferral order is C5, A3, A4, C3; C5 is deferred in every row.

| t₁ | campaigns in order | Mac wall | t₂,max |
|---|---|---|---|
| ≲ 2 s | C1 → C2 → C4′ → C3 → A4 → A3 (all of C1-C4, tight) | 45 h | 21 s (27 s without A3/A4; 68 s without C3 as well) |
| ≈ 3 s | C1 → C2 → C4′ (A4, A3 only if ≥ 3 h ahead) | 42 h | 44 s |
| ≈ 5 s | C1 → C2 | 42 h | 53 s |
| 5-7 s | C1 → C2-B (the B1/B2 part of C2) | 34-43 h | — |
| 7-12 s | C1 as C1a + C1b | 24-35 h | — |
| 12-16.5 s | C1r (reduced C1: A2 core 100 ev/pt, A5 3 pts, B1 2 500, B2 500, C 3 × 1 000, C′_PU 250/topology) | 19-24 h | — |
| > 16.5 s | ask the user: C1r as two runs (to ≈ 37 s), or no production | — | — |

The reviewer's sets are reproduced. The table includes C′: at 3 s, C1 + C2 + C4′ is 42.2 h (the reviewer had 39 h
without C′). Gates and development take 21 / 25 / 34 CPU-h (3.0 / 3.6 / 4.9 h) at t₁ = 2 / 3 / 5 s.

**G2b.** It keeps one criterion. t₂,max is now the largest t₂ at which every chosen campaign fits one Mac day **and** the
chosen set fits the production window.

### C-2/C-3 detail: the admissibility inputs and the dE/dx expectation

**Λ_R(m) (C-2).** The smoothed value is used, as HANDOVER §5.3 recommends:
- source: `P2.json` → `edge_fits_in_m`, E `deg2` and Ẽ `deg1` (the only Ẽ fit); P2.json sha256 is quoted in the plan;
- the per-mass values have pulls up to ±1.6σ against the smoothed curve (E800 +1.54, E900 −1.60);
- smoothed range: 0.431-0.741 keV (E) and 0.594 / 0.773 / 0.944 keV (Ẽ), so the k_adm examples (2.4-5.3 keV and
  0.86-1.9 keV) are unchanged.

**βγ_IT (C-2).** It is now pre-declared and computed for all 17 species-masses by `f4r_admissibility.py`:
- selection: template half, in_eta25 ∧ status 1, BM; per-event median IT |p|/m; per-point median; per-mass median over
  all Λ points;
- it reproduces `r1c_signal_handles.json` (sha256 `14aba918…f270170c7`) exactly at all 18 overlapping points;
- it is re-run unchanged at the freeze, with the output hash written into `WP_RULE.md`.

**New finding:** βγ_IT is not Λ-independent at the lowest Λ. It is flat within a few % above ≈ 0.6 keV but up to +18 %
at 0.3 keV (E500: 1.08 vs a median of 0.92). The reviewer's ±4 % covered 0.6-10 keV only. The plan therefore uses
βγ_IT(m, Λ) = max(the median over Λ, the per-point value). This is conservative for the signal, deterministic and
truth-only.

**βγ values (C-3), median over Λ:**

| species-mass | βγ_IT |
|---|---|
| E200 | 1.82 |
| E300 | 1.25 |
| E400 | 1.14 |
| E500 | 0.92 |
| E600 | 0.94 |
| E700 | 0.81 |
| E800 | 0.81 |
| E900 | 0.72 |
| E1000 | 0.68 |
| E1100 | 0.62 |
| E1200 | 0.60 |
| E1300 | 0.58 |
| E1400 | 0.53 |
| E1500 | 0.52 |
| Ẽ200 | 1.76 |
| Ẽ500 | 1.07 |
| Ẽ1000 | 0.74 |

The §2.6 table cell and the bullet now carry these values.

**Unit conversion (C-3).** It is pre-declared: R = the restricted loss in Si (T_cut = 100 keV) at βγ_IT, divided by the
restricted loss of the calibration muon gun (pT 1-10 GeV) at its median βγ. That is directly the muon-gun MIP-peak unit
of e_min. Constants are cited at the freeze.

**Expectation (ESTIMATE, Si constants recalled, UNVERIFIED):**

| species-masses | e_adm |
|---|---|
| E200-E400, Ẽ200, **Ẽ500** | none |
| E500-E600 | 1.3 (borderline: R/1.25 = 1.29 with the reviewer's mean/minimum ratio, 1.35-1.44 in the muon-gun unit) |
| E700-E800 | 1.3-1.6 |
| E900, Ẽ1000 | 1.6 |
| E1000 | 1.6-2.0 |
| E1100-E1500 | 2.0 |

The §2.6 plausibility line now says that Ẽ500 at Λ ≳ 2 keV is plausible only if the width rungs and SR-T suffice.

### C-6 detail: D4-1 options

D4-1 now offers only sets of the pre-defined campaigns:
- (a) C1-C4;
- (d) the deadline decision-table row;
- (m) C1 alone.

"Lean" and "(a) plus all toys" are withdrawn: C1 supersedes lean, and C4 already holds all A3 toys. The §6.2 lean column
is marked as the R1-R2 record, superseded, and "(≈ 270-850 lean)" was removed.

## Consistency check (§0, §5, §6, §10, §11, §12)

**Campaign contents.** C1 includes C′ in §0, §5 (table row and bullets), §6.2 (contents, table), §10 D4-1 and §11 item 5.
C4′ is defined in §5, §6.2 and §11.

**Speeds and costs.**
- 7.0 s (C1) in §0, §2.4, §6.1, §6.2, §11 and §12; 5.6 s for all campaigns everywhere.
- 315 / 392 / 545 / 774 CPU-h in §0, §6.2 and §10.

**Reach.** 5 × 10⁻¹⁰ (C1), 1.6 × 10⁻¹⁰ (+ C2) and 10⁻¹⁰ (+ C3) in §0, §2.6, §6.2 and §12 risk 11. §12 risk 11 notes
that C3 is deferred under the deadline at t₁ ≳ 2.5 s.

**Gates and the deadline.**
- G2b: one criterion, worded consistently in §0, §6.2 and §11.
- C5 deferred under the deadline in §0, §5, §6.2 and §11.
- The production window (Wed 10:00 → Fri 12:00, 47 h, 329 CPU-h) is the same in §0, §11 and the script.

**Labels.** The Stage-5 label is updated in the header and the §11 figure list.

**Grep checks.**
- No "PROPOSED" except the R1 history line.
- No "pending" except D4-16 (at G2a, as intended).
- No "published Stage-3", "0.9-1.0", "0.16-0.22", "3-4 days", "Mac + cloud" outside history and withdrawn stubs.

## Needs user input

1. **D4-16 at G2a:** the scope choice from the decision-table row at the measured t₁. To avoid idle Mac hours at night,
   the user may **pre-approve the decision-table row** at G2a. Each campaign would still end with a short report, and
   the sequence can be stopped at any report.
2. The **schedule's critical path** is G2a by ≈ Tue 22:00 and a user answer that night. Each hour later comes out of
   production, through the deferral order.
3. No other open decision. D4-17 (i) is approved and the cloud is dropped. C′ as production needed no ruling: it sits
   inside C1 under the cap.
