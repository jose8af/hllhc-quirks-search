# Fix R6: Stage-4 plan after review R6 (C001 quirks theory track)

Fixer S4PLAN-R6, 2026-10-13. Input: `review/REVIEW_S4PLAN_R6.md` (0 A, 1 B, 4 C). Only `acts/stage4/plan.md` was edited.

**Output.** `data/acts_stage4/fix_r6/f6r_numbers.py` → `f6r_numbers.json`:
- sha256 (py) `a23e478f0b7a96df54202927b5ac415ccb9c6f51b54dc9bfa673089ea151ff19`;
- sha256 (json) `a007ff42a1f1458fd68d06d210dd95f132e03debba519dde972f6ca57bccc268`;
- input `review_r6/r6_checks.json` (sha256 `60d50226…1dec6`, matches the review);
- arithmetic only, standard library, < 0.1 CPU-s.

**Unchanged:** the C′ cost, every campaign and decision-table number, the schedule, the approved decisions, and the finder
speed-up files (`acts/stage4/finder/`, `data/acts_stage4/g2/`, `G2A_REPORT.md`).

## B-1: RESOLVED (text and design only; zero cost)

§4.2 C′ bullet, with the matching changes in §2.5 item 9, §8 and §11 item 5:

1. **n-independent tolerance.** The preselection uses σ̂_h² = σ²_loc,max,h + t_tol² + (δn_max·|u_h|)², with:
   - σ_loc,max,h = the larger local error, i.e. the largest σ_n(n, hit) over all n (the along-strip σ for 2S, as before);
   - t_tol = 30 µm;
   - δn_max = 2 mrad, the §2.2 candidate-merge tolerance.

   So σ̂_h ≥ σ_tot,h(n) for every n and every δn ≤ δn_max. The **attribution rule uses the same σ̂_h**. The implication
   "attributed ⇒ ∃ triple with χ²₃ ≤ 48" then holds exactly with the same σ, PV and hits, for any δn. For δn ≤ δn_max
   this only loosens R5's attribution, which is conservative. For a candidate with δn > δn_max, the hits within 4σ_tot but
   outside 4σ̂_h are reported as a diagnostic.
2. **Same PV draw.** The smeared PV is drawn once from the toy seed in C′₀, stored, and used as the with-PU event's PV.
   No σ_PV term is needed.
3. **Stored hits.** The stored C′₀ Fatras toy SimHits are merged into the PU event, as the signal injection does. The toy
   is not re-simulated. Smearing and hit efficiency use the toy seed, so the measurements are identical too.
4. **New gate V4-10** (§8 table, the §4.2 bullet and §11 item 5).
   - *Check.* On the full C′₀ sample, the number of attributed candidates in non-preselected events must be 0 exactly. It
     is reported with f_pre. A per-event hash also confirms that the toy hits and the PV match. The check costs nothing,
     because the finder and the attribution already run on every C′₀ event.
   - *Failure path.* A non-zero count is treated as a bug: that topology's C′_PU events are not run or used until the bug
     is fixed and the check is re-run. If it cannot be fixed inside C1:
     - f_pre becomes f_pre × (1 + N_leak/N_attr,pre);
     - |ln(1 + N_leak/N_attr,pre)| is added to σ_ln;
     - the term is flagged and the user is told.
   - *Freeze.* V4-10 is added to the §2.5 item 9 freeze list, together with σ̂_h, δn_max and the PV/hit hand-over.

## C-1: RESOLVED (ESTIMATE tags kept)

- **§4.2 table, 22 mm row.** The row now reads:
  - f_pre ≈ 0.07-0.5 (line + near-vertex-hit path, from the per-hit 4σ bound to the full χ²₃ budget; a lower bound, since
    σ̂_h only loosens it);
  - N_pre ≈ 2 × 10³-1.5 × 10⁴, with 1 overlay per event;
  - passes ≈ the kink row (250-440 / 30-180 / 3-40).

  The R5 two-prong numbers are kept in the explanatory note as a sub-population.
- **NI note.** It now covers every r_NI: the two-prong estimate is not an upper bound anywhere. The attributable rate at R0
  is ≈ 0.6-3.6 per event, 1.3-3.3 decades above the old 2 × 10⁻³-3 × 10⁻².
- **"6-7 decades".** §2.6 feasibility, the §4.2 NI paragraph and §12 risk 3b now say "≈ 8-9 decades (9-10 under the
  strict B₈₄ rule)". This is computed from the review's rates: log₁₀(0.64-3.64 / 3 × 10⁻⁹) = 8.3-9.1, and 9.3-10.1 vs
  3 × 10⁻¹⁰. The old two-prong value is kept for context.
- **Zero-count reach.** "10⁻⁴ per r_NI" is replaced by 1.14/M under item 4a:
  - 1.1 × 10⁻⁵ for the guns;
  - for NI/DIF, 1.14/N_pre: ≈ 8 × 10⁻⁵-6 × 10⁻⁴ at 22 mm and ≈ 4 × 10⁻⁵-1.3 × 10⁻⁴ for the kinks.

## C-2: RESOLVED

§2.5 item 4a: the zero factor with the **largest M_j** (ties → first along the ladder) carries 1.14/M_j, with σ_ln = 1.
The other zero factors enter as 1. The text states that an upper bound enters once per term. The "only bounded factor"
wording replaces "final factor", and the ×200 (×2 000) example is cited.

## C-3: RESOLVED

§2.5 item 4a: c cannot be measured for a zero factor. It is evaluated among the non-zero factors only, and a zero-branch
term carries the largest c of its other factors (1 if none) and is flagged.

## C-4: RESOLVED

§4.2: the NI toy places the parent at the true PV, so B_NI = Σ_r_NI (NIs/event) × **P_PV-line ≈ 0.22** × P(pass | r_NI) ×
N_trig. The factor is explicit and tagged ESTIMATE. *Neighbourhood:* the DIF toy also starts its parent at the PV, and B_DIF
takes no PV-line factor (1, conservative); this is now stated.

## Propagation and neighbourhood check

- **Header.** An R6 revision note is added.
- **Stale values.** A grep finds no remaining unqualified "6-7 decades", "10⁻⁴ per r_NI", "first zero" rule or ±4σ_tot
  attribution. The "6-7" and "4 × 10⁻⁴…12-200" values survive only as labelled history.
- **V4 list.** The §1 file table now lists V4-1…V4-10 (it previously said V4-8 while V4-9 already existed).
- **Other sections.** §0, §5 and the §4.2 B-sum formula need no change: f_pre × P(pass | preselected, PU) is unchanged.
