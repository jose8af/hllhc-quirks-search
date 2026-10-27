# REVIEW_SRT_TMIN_R3: narrow verification of FIX_SRT_TMIN_R3 (final PC-19 block)

Fresh critical reviewer (narrow verifier), 2026-10-14.

**Target.** `acts/stage4/review/FIX_SRT_TMIN_R3.md` (incl. the final PC-19 block), `acts/stage4/g3/srt_tmin_check.py`
(incl. `--combine`), `data/acts_stage4/g3/srt_tmin_check_{v1_rerun,v2,v2_spv150,v2_spv230,v2_st60}.json`,
`srt_sigma_ln_pv.json`, `srt_dt_hist_{k0,kp1}_v2*.npy`.

**Read.** REVIEW_SRT_TMIN_R2 (findings to verify), FIX_SRT_TMIN_R2 §1 (C-1 edit), WP_RULE §4.1 (l.329-347), §4.2
(l.351-365), §6.2 factorisation table and composition (l.454-472), §S sample table (S2/S3, l.736-737); `jobs/G3.json`,
`jobs/C1.json` (n_events per B1 job).

**Signal-blindness.** No signal sample, efficiency or yield was opened or computed. The signal-side text of PC-19 was
read as rule text only.

**Compute.** One reviewer script (scratchpad only, not in the project): the in-time pass of the 77 G3B1 jobs with and
without the σ_t 60 ps smearing, 26 s, 1 core, nice 15. It imports only `band_kernel` / `tpv_of_event` / salts from the
module and recomputes the earliest-raw-t in-time late count itself. Plus JSON/histogram reads (< 5 s).

## Verdict

**PASS: 0 A, 0 B, 5 C.**

R2 B-1 is resolved: the σ_t,PV → σ_ln term is now fully mechanical (quantity, variation set, formula, population ladder
with ≥ 10-count qualification and fallback, scope, §4.1 slot), and `--combine` implements it. All six R2 C items are
resolved. Every spot-checked number reproduces. The PC-19 block is complete, self-consistent, signal-independent and
conservative for B. One implementation gap in the σ_t 60 ps variation (C-1) under-states σ_ln,σt at loose
(0.000 vs 0.032 reviewer); it is immaterial at G3 but must be fixed before the script produces the C1 binding values.

---

## 1. Status of the R2 findings

| R2 finding | status | evidence |
|---|---|---|
| **B-1** σ_t,PV → σ_ln underspecified | **RESOLVED** | (a) formula σ_ln,X = max_v \|ln(L_v/L_nom)\|; (b) quantity L = f_pres·P(late) + f_¬pres·P_OOT on the fixed nominal window; population ladder S3 ∧ r (r < R04) / S2 ∧ r (r ≥ R04), qualification C ≥ 10 in nominal **and** every variation, fallback = deepest qualifying rung before it, F1 → parent in-job rung, none → 1.0; (c) scope B_PU SR-T only, both summands; not B_SM / C′ / SR-G; (d) §4.1 line extended with σ_ln,PV² + σ_ln,σt² (matches WP_RULE l.331 + two terms). Script `combine()` implements (a)-(b) literally. |
| C-1 parity labels | RESOLVED | FIX R2 l.95: even [6.205, 24.025], odd [5.95, 24.025]; JSON `edges_even_jobs` / `edges_odd_jobs` identical. |
| C-2 provenance | RESOLVED | Script mtime 01:15; all outputs 01:15:56-01:28:21. v1_rerun reproduces R1 (6.12 / 24.275; 34 / 31 loose, 48 / 10 R04). v2 edges 6.07 / 24.025 and every R2 count unchanged (36; 39/20/24; 48; 16/8/19). |
| C-3 k ≤ −1 bound / M | RESOLVED | Mixing primary; P_OOT = [n̄₊₁ + n_{k≤−1}]/M_¬pres as one §4.2 factor; enters at measured value, bound reported. See §2. |
| C-4 grid / per pair | RESOLVED | Stated in the block. |
| C-5 σ_t 60 ps | RESOLVED (text) | Enters σ_ln by the same rule. Implementation gap → C-1 below. |
| C-6 signal wording / pinning | RESOLVED | "earliest in-band hit (Δt > −Δt_bx/2)"; in-time PU-late credit bounded (R04 P(late\|present) = 1.499e-4, matches "≈ 1.5e-4"); hash assignment; road-0 fallback in text and script (l.194, lowest road). Residual detail → C-4. |

## 2. Spot-check of the numbers (reviewer recomputation from the JSON counts)

| quantity | FIX R3 / JSON | reviewer | |
|---|---|---|---|
| loose L_nom = 36/N + mean(39,20,24)/M · M/N, N = 1 963 659, M = 1 475 930 | 3.2422e-5 | 1.8333e-5 + 1.4089e-5 = 3.2422e-5 | ✓ |
| loose C nom / 150 / 230 | 119 / 54 / 266 | 36+83 / 39+15 / 39+227 | ✓ |
| **σ_ln,PV loose** | **0.588** | max(\|ln 0.6911\| = 0.370, \|ln 1.8010\| = 0.588) | ✓ |
| R04 C nom / 150 / 230 | 91 / 51 / 158 | 48+43 / 47+4 / 48+110 | ✓ |
| **σ_ln,PV R04** | **0.306** | max(\|ln 0.7754\| = 0.254, \|ln 1.3583\| = 0.306) | ✓ |
| **M_¬pres** (candidates without an in-time in-band hit) | 1 475 930 / 1 503 921 | N − n_present = 1 963 659 − 487 729; 1 824 063 − 320 142 | ✓ |
| **k ≤ −1 bound 3/M_¬pres** | **2.0e-6** | 2.03e-6 (loose), 1.99e-6 (R04); n_{k≤−1} = 0 (mixing) in all 4 v2 runs | ✓ |
| copy cross-check 3/N | 1.5-1.6e-6 | 1.53e-6 / 1.64e-6, count 0 | ✓ |
| all four v2 runs use window [6.07, 24.025]; same z draws (spv runs keep `max_abs_ddt0` 7.9e-7) | yes | `combine()` asserts it; confirmed | ✓ |
| salts 0x5254 = 21076, 0x534D = 21325; √(60² − 35²) = 48.7 ps | as stated | ✓ | ✓ |
| σ_ln,σt R04 | 0.016 | 48 in-time unchanged under smearing (reviewer), OOT 43 → 46: ln(3.4721/3.4173) = 0.016 | ✓ |
| **σ_ln,σt loose** | **0.000** | **0.032** (in-time late 36 → 34 with smeared t, reviewer) | see C-1 |

## 3. The final PC-19 block

- **Complete.** Window edges (definition, grid, pair counting, population, threshold with the user split flagged), PV time
  (PU-only seeded, signal/SM true vertex time), "earliest", mixing (k = +1 three realisations, k = −1…−12), P(late),
  P_OOT as one factor on M_¬pres, k ≤ −1 at measured value with its bound, σ_ln terms with a mechanical fallback,
  §4.1 slot, signal-side conventions, frozen_inputs keys, PC table row. No post-hoc choice remains for B (C-2, C-3 are
  wording precision only).
- **Self-consistent.** The block, the FIX tables, the JSONs and `combine()` agree. The PC-18 composition text
  ([t_min, Δt_acc]) is replaced consistently by [t_min, t_max] in §1.4, §6.2 and the "not in-job" line.
- **Signal-independent.** Edges, P(late), P_OOT and both σ_ln terms are PU-only B1 quantities at a frozen threshold;
  σ_t,PV and its variation set are plan constants. The signal OOT event assignment is a hash of row identifiers, not of
  any signal outcome.
- **Conservative for B.** The k ≤ −1 sum over j (≥ union), the max-Δt proxy (ignores the upper edge), prompt
  previous-crossing hits not vetoing, max over variations, and 1.0 when nothing qualifies all bias B up or leave it
  unchanged. The fallback to a shallower rung is a model extrapolation, not a guaranteed bound (at G3 σ_ln,PV falls with
  depth, 0.59 → 0.31, so it does not under-cover there); this is the same convention as PC-11 and was requested by R2.
- **Implemented by the script.** R_k, edge order, t_PV, mixing, P_OOT on M_¬pres, k ≤ −1 by mixing (partners 1-3 reuse
  their +25 ns pass with the shift removed; 4-12 unshifted), L, C, qualification, formula and fallback all match, except
  C-1.

## 4. Findings

### C-1. σ_t 60 ps variation is not applied to the in-time summand (script). Fix before the C1 evaluation.

- `fractions()` uses `d['raw0']` = **stored** `btl_dt0` − t_PV (l.243, 274) for the in-time late count. The stored field
  is unsmeared, so with `--extra-smear-ps` only the OOT summand is varied. Evidence: in `v2_st60.json` the in-time counts
  are identical to nominal (36 / 48), `max_abs_ddt0` = 0.50 ns, and the loose raw-vs-min-Δt disagreements are 3 (they
  compare stored vs recomputed-smeared).
- The rule text ("+48.7 ps smearing of the stored t"; earliest by raw t) is correct; only the script deviates.
- Reviewer recomputation with the smeared S5 times: in-time late loose 36 → 34, R04 48 → 48. Corrected σ_ln,σt:
  loose |ln(3.1404/3.2422)| = **0.032** (FIX: 0.000), R04 0.016 (unchanged). In quadrature with σ_ln,PV ≥ 0.31 this is
  < 0.002, so immaterial at G3; but the in-time late hits sit at the t_min edge (55 of the 57 in-window k = 0 pairs are in
  [5.9, 6.3] ns), so the term need not stay negligible at deeper C1 rungs.
- **Fix:** use the recomputed `raw0r` (from the smeared S5 hits) for the in-time term whenever `extra_smear_ps > 0`
  (or always; it agrees with the stored field to 7.9e-7 ns at nominal), and re-run st60 + `--combine`. Correct the C-5
  row (0.000 → 0.032) in FIX R3.

### C-2. Fallback edge case wording.

`combine()` gives 1.0 to a non-qualifying rung with no qualifying rung *before* it, even if a deeper rung qualifies; the
text says "if **no** rung qualifies". Say "if no rung before it qualifies". Practically moot (loose R01 has C = 119).

### C-3. F1 parent rung for R21-R23.

"(h, o, e) takes the value of its parent in-job rung (R14, or FB_k[∧ e])" omits F0 ∧ e_x (R14 ∧ e_x, column F0e>x), the
parent of R21-R23 in the §6.2 composition. Name it, so the population for dE/dx F1 rungs is unambiguous.

### C-4. Signal OOT hash details.

Specify the digest → integer map (e.g. first 8 bytes, big-endian) and the collision scope ("unused" within the row's 15
crossings; the C1 B1 pool of 5 000 events cannot be globally unused across all signal rows × 15 crossings).

### C-5. Mixing assumptions to state.

- k = −j needs n_ev ≥ 13 per job so that e+j ≠ e (G3B1 and C1 B1 jobs have n_ev = 25: satisfied).
- Crossings +1 (realisation j) and −j share partner e+j for j = 1-3. This leaves the expectation of the additive
  P_OOT unbiased (each term is separately unbiased) and only affects the bootstrap variance; state it.

## 5. Items verified without finding

- `WP_RULE.md` (Oct 13 18:18), `frozen_inputs.json` (00:18) and the G3B1 inputs (last written Oct 13 20:53) are unchanged
  by this fix; outputs only in `data/acts_stage4/g3/`. The block is marked NOT applied, and applying it requires a logged
  change, re-hash and re-review before any SR-T signal ε.
- `combine()` reads exactly the four v2 runs, asserts the common window, and evaluates the ladder in order.
- The "per-candidate" C counts in-time late + the sum over the three k = +1 realisations + n_{k≤−1}, as the text states
  (not the mean), so the ≥ 10 gate is on the raw count.
- Scope of the σ_ln terms leaves B_SM untouched, consistent with SM t_PV = true `hs_vtx[3]` (R2-verified).
