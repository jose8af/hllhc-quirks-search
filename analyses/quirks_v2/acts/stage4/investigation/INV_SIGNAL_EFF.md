# INV_SIGNAL_EFF: why the detector-level signal efficiency looks wrong (C001 TT, Stage 4)

Investigator, 2026-10-16. Read-only on every frozen and production file. The scripts are in
`acts/stage4/investigation/*.py` and the scratch outputs in `data/acts_stage4/investigation/`. Nothing was written to
`data/acts_stage4/prod/` or `analysis/`.

Triggered by `STAGE4_RESULTS.md` §6 V4-3 and §10 items 1, 2 and 6, and by the five symptoms (a)-(e) in the brief.

Classes:
- (i) genuine physics, or genuine behaviour of the frozen algorithm;
- (ii) definition mismatch in the report;
- (iii) bug in the analysis code;
- (iv) bug or coverage gap in the production code or campaign.

**Tags.** [V] means measured here from production outputs or from re-runs of the production code path. [E] means
estimated.

---

## 0. Bottom line

There is **no single bug that invalidates ε**. The symptoms come from four effects, listed by size:

| # | root cause | class | symptoms | effect on ε |
|---|---|---|---|---|
| 1 | **The A1 and A2 numbers are not comparable.** V4-3's "ε ≥ 0.9" is a finder efficiency inside the fiducial, but it was compared with the all-η A1 R_A number. A1's denominator is all-η and both halves; A2's is the template half with \|η_pair\| < 2.5. | (ii) | (a), part of (b) | A1 barrel fraction is 0.19-0.28, so the all-η number is ×0.19-0.28 of the fiducial one. On the same rows as A2, A1 rises ×1.0-1.5 (e.g. E500 3 keV: 0.171 → 0.245). **Inside \|η_pair\| < 1, A1's finder efficiency (some matched candidate) is 0.90-0.97 at 1.5-3 keV [V]. The V4-3 expectation is met there.** |
| 2 | **The R04 counting rung and the seed geometry cannot handle near-degenerate ribbons without PU; PU hits fill the gap.** R04 = N_IP2 ≥ 7 needs ≥ 2 hits on *every* one of the 10 IP surfaces (PS: min(in, out)). One U-5 b merge (IT 25 × 100 µm, PS 100 µm × 1.47 mm) or one 1 % inefficiency on any surface fails R04. The seed cut sin∠(PV→a, PV→b) ≥ 10⁻³ (`finder/kernels.py:292`) gives no seed at all when the pair is a line at TBPX L3/L4. Under PU, in-band PU hits supply the missing second hit, and an (a, b) seed with one PU hit defines a plane that contains the quirk "line". | (i) algorithm/physics; (ii) for the "A1 = optimistic bound" reading and the truth-edge comparison | (b), (c), (d) | At E500 central: A1 R04 0.62 (3 keV) / 0.44 (5 keV) vs paired A2 0.82 / 0.76 [V]. The truth prediction (any IP surface merged or seed degenerate) is 33 % / 58 % of central events [V]. |
| 3 | **A2 never puts quirk measurements through ACTS CKF.** The numpy quirk rows carry flag 0 (`code/s4sig.py:148`) and are appended after the chain (`run_g1b.py:383-387`). CKF stealing is therefore absent from A2. Plan §4.1 (l. 1254) and V4-6 (l. 1813) require reverting a point to the full chain if V4-6 > 5 %. V4-6 was measured only on A5 at Λ = 1 keV, so the rule could never fire. A1 (full chain) shows a quirk-on-CKF fraction of 5-7 % at 3 keV, 10-17 % at 5 keV and 23-40 % at 10 keV in the fiducial [V]. | (iv) campaign/coverage gap (not a code error in a frozen file) | part of (b) | Paired full-chain re-run (60 central rows per point): in-job ε 0.933 vs 1.000 (E500 3 keV), 0.917 vs 1.000 (E500 5 keV), 0.817 vs 0.933 (E200 5 keV) [V], i.e. **A2 is high by 7-12 % at 3-5 keV** |
| 4 | **The sep_IT^det estimator uses every band hit.** It splits all of the candidate's in-band hits at the median (`analysis/hitrec.py:209-223`; `signal.py:144` calls it with the full record). Under PU, the ±W_c = 75 mm band of PU hits dominates the two "cluster means". | (iii) | (e) | No effect on ε, B or the limits. The P2 handle is unusable at PU 200 as computed. A core-only restriction helps only partly (§5). |

The signal match is **not** broken by merging (§6). The MET, PV, road and BTL treatment are identical in A1 and A2
(§2). No production job has to be re-run for symptoms (a), (c), (d) or (e). The only re-production with a physics
effect is item 3: the full-chain A2 at Λ ≥ 3 keV (§7).

---

## 1. V4-3: what ≥ 0.9 was supposed to be measured on (symptom a)

`plan.md` l. 1810 defines V4-3 as: "Finder on truth-only (no PU) events vs the Stage-3 truth edges. Efficiency vs Λ at
every p2 point … Expect ε ≥ 0.9 at 1-5 keV (an expectation, not a cut)". This is a **finder** efficiency, read next to
the truth window study (`f1r_truth_window.json`, a fraction of central template events). It is not ε at R_A with an
all-η denominator.

`STAGE4_RESULTS.md` §6 compares 0.9 with "the measured maximum 0.21 (all-η A1, barrel only)". That number folds in three
things:
- the barrel fiducial (\|η(n₃)\| < 1 is a fixed cut at every rung). The A1 barrel fraction is 0.19-0.28 [V];
- the R04 requirement, which costs ≥ 1 − 0.99²⁰ ≈ 18 % from hit efficiency alone on 20 IP hits, before any merging;
- f_CKF and the core match.

A1 cumulative efficiencies inside \|η_pair\| < 1 (status 1, not probe-excluded), from production A1 outputs [V]
(`a1_ladder_*.json`). Columns: matched candidate = some candidate with ≥ 50 % of the written quirk hits / + R04 / the
report's all-η R_A.

| Λ (keV) | E200 | E500 | E1000 | E1500 | Ẽ500 |
|---|---|---|---|---|---|
| 0.6 | 0.55 / 0.31 / 0.089 | 0.47 / 0.33 / 0.091 | 0.38 / 0.19 / 0.042 | 0.36 / 0.27 / 0.069 | 0.23 / 0.18 / 0.043 |
| 1 | 0.90 / 0.63 / 0.164 | 0.80 / 0.64 / 0.177 | 0.83 / 0.64 / 0.120 | 0.75 / 0.55 / 0.132 | 0.79 / 0.52 / 0.127 |
| 1.5 | 0.92 / 0.65 / 0.181 | **0.94** / 0.77 / 0.213 | **0.93** / 0.74 / 0.163 | **0.92** / 0.69 / 0.175 | — |
| 2 | **0.91** / 0.64 / 0.179 | **0.90** / 0.68 / 0.189 | **0.90** / 0.68 / 0.140 | **0.93** / 0.73 / 0.179 | **0.96** / 0.75 / 0.193 |
| 3 | 0.85 / 0.50 / 0.138 | 0.84 / 0.62 / 0.171 | 0.83 / 0.61 / 0.126 | 0.87 / 0.60 / 0.150 | **0.97** / 0.76 / 0.181 |
| 5 | 0.58 / 0.31 / 0.084 | 0.65 / 0.44 / 0.120 | 0.74 / 0.48 / 0.100 | 0.69 / 0.47 / 0.116 | 0.84 / 0.52 / 0.130 |
| 10 | 0.28 / 0.05 / 0.013 | 0.33 / 0.10 / 0.029 | 0.35 / 0.14 / 0.030 | 0.44 / 0.18 / 0.045 | 0.54 / 0.18 / 0.047 |

**Verdict (ii).** The V4-3 expectation holds at 1.5-2 keV (Ẽ500 up to 3 keV). It fails at 1 keV (the low edge) and at
≥ 3-5 keV (item 2, §3) for genuine reasons. "Measured maximum 0.21" is not the V4-3 quantity and should not be
reported against 0.9.

---

## 2. Is A1 "the same events without PU"? Code-path comparison (symptom b)

| step | A1 (`run_g1b.py` kind 'a1') | A2 (kind 'a2') | same? |
|---|---|---|---|
| rows | `P.rows(template=False, counting=False, status1=True)`: all η, both halves (l. 299) | template half, `in_eta25`, all status; status ≠ 1 rows written with trial −1 (l. 379-382) | **no**: different denominators (item 1) |
| quirk hits | Stage-3 SimHits injected into ACTS (late > 25 ns and 1 % inefficiency removed with the same draws as numpy; `run_chain.py:514-536`), then Fatras-chain digitisation | `s4sig.digitise` numpy smearing (same sigmas, same late/eff draws) | equivalent at 1 keV (A5 ≈ A2) |
| CKF on quirk hits | **yes** (`with_ckf`); stolen quirk hits are removed from the pool and counted in f_CKF | **no**: flag forced to 0 (`s4sig.py:148`) | **no** (item 3) |
| top-up | none (`do_topup=False`) | PU rows only | n/a |
| U-5 b merging | `chain_inputs.merge_pool` on quirk-only pool | the same on quirk + PU pool | same rule |
| PV, MET (road and Δφ cut) | `sig_event_inputs`: hseed('sig-pvmet', spin, m, row): truth vertex + N(10, 10, 15 µm); MET = truth (quirk pair) + N(0, 25 GeV) | identical call, identical seed | **identical** (no PU term in MET) |
| finder config | frozen (δ₉₅ = 0.15, η_max = 1, T_seed = 4) | identical | identical |
| BTL requirement | not in ε (SR-T factor only) | identical | identical |
| no trial | if fewer than 3 pool hits (`run_g1b.py:271`) | never happens in practice (PU) | cosmetic (§3.3) |

So apart from the denominator, A1 differs from A2 only by **(1) the absence of PU hits** and **(2) the CKF on quirk
hits**. There is no MET-from-PU, PV-choice or road difference.

Per-row comparison on the same rows, from production outputs (`cmp_rows.py`; `cmp_p2_*.json`; R04, analysis match) [V]:

| point | A1 all rows | A1 on A2's rows | A2 | rows passing only in A2 / only in A1 |
|---|---|---|---|---|
| E500 3 keV | 0.171 | 0.245 | 0.320 | 19 / 4 |
| E500 5 keV | 0.120 | 0.185 | 0.300 | 24 / 1 |
| E200 5 keV | 0.084 | 0.085 | 0.215 | 26 / 0 |
| E1500 5 keV | 0.116 | 0.120 | 0.275 | 32 / 1 |

The pattern over all 40 points is in `cmp_all.txt` [V]. On A2's own rows, A1 > A2 at Λ ≤ 1-1.5 keV, because PU hurts
wide ribbons. The ordering crosses at 1.5-2 keV for every species-mass, and A1 < A2 at ≥ 2-3 keV. For example, A1 vs A2:
- E1500: 0.210 vs 0.095 at 1 keV; 0.120 vs 0.275 at 5 keV.
- Ẽ500: 0.180 vs 0.100 at 1 keV; 0.160 vs 0.265 at 5 keV.

### 2.1 Traced events (E500, Λ = 3 keV; production A1 and A2 and re-runs of the A1 path)

Stage-3 truth → chain → pool → finder → match → R04:

- **Row 3112** (η_pair −0.93).
  - Truth: all 7 IP layers have 2 quirk hits.
  - A1 chain: nqw = 32, no CKF. U-5 b merges 2 quirk pairs (4 hits → 2) on PS surfaces, leaving TBPS_L3_in with 1 hit.
  - Finder: one candidate containing all 32 quirk hits, frac 1.0, f_CKF 0, w_core 0.33 mm, but N_IP2 = 6. **R04 fails.**
  - A2 (same row, numpy quirk hits, same PV/MET): the matched candidate has TBPS_L3_in = 1 quirk + 1 PU hit, N_IP2 = 7,
    so **R04 passes**. The core holds 59 hits, 30 of them quirk (51 %), and w_core = 13.0 mm (8 PU hits in the TBPX_L1
    core).
- **Rows 852, 2706, 5715, 5957, 4209.** Same mechanism: N_IP2 6 (or 5) in A1 from 1-5 merged quirk pairs or one lost
  hit (numpy digitisation shows TBPX_L3 or TBPS_L3/L1 with 1 hit). A2's band contains 1-3 PU hits on exactly those
  surfaces.
- **Row 268** (η −0.31, 83 quirk hits, looping pair).
  - Production A1: CKF took 46/83 quirk hits, the best candidate has 37 hits (frac 0.45 < 0.5) and f_CKF 0.59. Fail.
  - Re-run in a different job composition: CKF took 0, then 39 (60-row job). CKF stealing in A1 is stochastic per
    event index, because the ACTS RNG is keyed by the event number in the job.
  - A2: no CKF on quirks, so it passes.
- **E500 5 keV no-candidate rows** (e.g. 6717, 9685, 774; `seed_diag.py`).
  - The road holds all 16-32 quirk hits. TBPX L4/L3 have 1-2 hits each, because IT merging leaves one hit.
  - Every cross-quirk (a ∈ L4, b ∈ L3) pair has sin ∈ [9 × 10⁻⁵, 9.8 × 10⁻⁴] < 10⁻³ and is rejected
    (`kernels.py:292`). No seed, so `n_kept_all` = 0.
  - Under PU (A2) the same events pass via planes seeded with a PU hit.

### 2.2 Failure decomposition of A1 inside the fiducial (production outputs, `classify.py`) [V]

E500. Counts out of 135 central events.

| Λ | pass R04 | no candidate with any quirk hit | Δφ(n₃, MET) ≥ δ₉₅ | N_IP2/N_IT2 fail with a quirk merge in the event | N_IP2 fail, other (inefficiency/loops) | f_CKF |
|---|---|---|---|---|---|---|
| 0.6 | 45 | 71 (wide ribbon: low edge) | 1 | 3 | 15 | 0 |
| 1 | 86 | 27 | 3 | 1 | 18 | 0 |
| 2 | 92 | 12 | 3 | 14 | 13 | 0 |
| 3 | 84 | 19 | 3 | 18 | 9 | 0 |
| 5 | 59 | 44 (seed degeneracy and/or CKF stealing) | 2 | 23 | 4 | 0 |

E200, E1500 and Ẽ500 behave the same way (`classify_*.json`). The Δφ cut costs 1-9 % of central events at every Λ in
both samples alike (identical MET); it is not a difference.

---

## 3. Upper edge 4.6-7.5 keV vs the Stage-3 "merging edge" 12.8-25 keV (symptoms c, d)

### 3.1 The Stage-3 edge is a different quantity (ii)

The Stage-3 edge is f(**median** truth IT pair separation < 100 µm) = 50 % (`sim/stage3/HANDOVER_STAGE4.md` l. 274). The
detector-level R04 efficiency instead needs **every** IP surface unmerged (any one merge on 10 surfaces kills N_IP2 = 7),
plus a seed opening ≥ 1 mrad at TBPX L3/L4. The quirk separation oscillates through zero along the path, so a merge
somewhere happens long before the *median* separation reaches 100 µm.

Truth-level prediction (Stage-3 hits, central events, U-5 b pitch rule; `truth_degeneracy.py`) [V]:

| Λ (keV) | E500: f(any IP surface merged) | f(seed degenerate) | f(either) | median IT sep (mm) | f(median sep < 100 µm) |
|---|---|---|---|---|---|
| 2 | 0.21 | 0.06 | 0.24 | 5.3 | 0.00 |
| 3 | 0.29 | 0.07 | 0.33 | 2.2 | 0.01 |
| 5 | **0.51** | 0.22 | 0.58 | 0.80 | 0.05 |
| 7 | 0.67 | 0.33 | 0.73 | 0.39 | 0.16 |
| 10 | 0.75 | 0.49 | 0.82 | 0.18 | 0.30 |
| 20 | 0.96 | 0.84 | 0.97 | 0.05 | 0.72 |

f(any IP surface merged) = 50 % falls at ≈ 5 keV for every species-mass: at 5 keV it is E200 0.48, E500 0.51,
E1000 0.56, E1500 0.52 and Ẽ500 0.47.
That reproduces the A1 detector upper edges (E200 4.7, E500 5.4, E1500 6.0 keV, `edges_det.json`). The truth
f(median < 100 µm) reaches 50 % only at 13-20 keV, which is the Stage-3 edge. **Class (i) + (ii):** the detector edge is
real for this selection, but the report compares it with the wrong truth edge. The right truth comparator is f(any IP
surface merged ∨ seed degenerate).

The V4-3 W_c/t_tol attribution, which the report lists as OPEN, is in the A1 files (`sig.var_eff`; `v43_variants.py`)
[V]. For E500 central events (R01/R04):
- **At 2-5 keV, W_c = 50/100/150 mm and t_tol = 0/100 µm leave R01 and R04 unchanged** (±0.01, except t_tol = 0 at
  3 keV: −0.06 on R04).
- At 0.6-1 keV, W_c moves R04 from 0.27/0.61 (W_c 50) to 0.35/0.69 (W_c 150), i.e. the low edge.

So the high-Λ loss is merging, seed degeneracy and CKF, **not** the window or the plane thickness.

### 3.2 No-trial count rising with Λ (c)

The A1 no-trial rows are predominantly **forward**: median \|η_pair\| 2.6-2.8 at every Λ (`notrial.py`). Inside
\|η_pair\| < 1, no-trial counts are 0-3 at ≤ 5 keV (E500) and up to 25/129 at E1500 10 keV. There the CKF took almost every
quirk hit, leaving fewer than 3 pool hits. A forward event fails in A1 and A2 alike. The difference is only that in A2 a
trial still runs on the PU. The rise with Λ is the narrow pair leaving no barrel hits, plus CKF at high Λ. **(ii)
cosmetic, no ε impact; the no-trial count is not an efficiency-loss diagnostic.**

### 3.3 Why A2 > A1 at high Λ (b)

Three mechanisms, all present in the traced events:
1. **PU hits complete N_IP2.** This is a genuine effect of the frozen rule, which counts all band hits.
2. **PU hits seed planes for degenerate (line-like) ribbons.** Any plane through the quirk line contains it.
3. **A2 has no CKF stealing.** This is item 3, a coverage gap.

The A2 in-job flag (≥ 50 % of the written quirk hits in a candidate passing R04, f_CKF < 0.2) is **1.00 for all 60
central E500 3-keV rows** [V]. Under PU every central event gets a candidate holding the quirk hits. What then limits A2
is the core-purity match (≥ 50 % quirk among core hits; 0.82). The high-Λ A2 candidates are therefore **PU-assisted**:
w_core is set by PU (floor ≈ 10-13 mm, as in §5 of the report), and so are sep_IT^det and the plane orientation.

**Consequence (ii):** A1 is **not** an optimistic bound on A2 for Λ ≳ 2 keV, and the report's §7 item 10 is right to
drop the label. The physical reading is that at Λ ≳ 3 keV the R04 ribbon signature is satisfied with PU's help by a
quirk "line". Detector-level observables that assume a ribbon carry no Λ information there.

---

## 4. CKF stealing missing from A2 (item 3): A1 measurement and paired full-chain re-run

A1 (production, full chain, no PU), central events [V] (`ckf_stats.py`). Columns: ⟨quirk-on-CKF fraction⟩ / P(fraction
> 0.2) / failures with fraction > 0.2.

| Λ | E200 | E500 | E1000 | E1500 | Ẽ500 |
|---|---|---|---|---|---|
| 1 | 0.002 / 0.01 / 1/44 | 0.003 / 0.01 / 1/49 | 0 / 0 / 0/33 | 0 / 0 / 0/53 | 0 / 0 / 0/54 |
| 2 | 0.019 / 0.03 / 4/47 | 0.020 / 0.04 / 6/43 | 0.018 / 0.04 / 4/32 | 0.018 / 0.05 / 6/38 | 0.003 / 0.01 / 1/31 |
| 3 | **0.055** / 0.09 / 11/62 | **0.052** / 0.11 / 15/51 | **0.071** / 0.13 / 13/39 | **0.059** / 0.10 / 13/53 | 0.008 / 0.03 / 3/31 |
| 5 | **0.141** / 0.30 / 39/91 | **0.135** / 0.24 / 32/76 | **0.117** / 0.18 / 19/56 | **0.174** / 0.25 / 33/71 | **0.096** / 0.18 / 22/61 |
| 10 | 0.230 / 0.35 | 0.251 / 0.41 | 0.343 / 0.46 | 0.395 / 0.50 | 0.225 / 0.40 |

At 1 keV this matches A5/V4-6 (0.2-0.6 %), which is why A5 = A2 there. By the plan's own rule (V4-6 > 5 %, then revert
to the full chain), **every E point at 3 keV and every point at 5 keV should have been produced in full chain.** The rule
could not fire because A5 was placed only at 1 keV (`run_g1b.py:50`, flagged as a "G1b choice"). The A1 CKF fractions
are without PU. With PU the CKF environment differs, so this must be measured with PU.

Paired re-run (production code path, `rerun_a1.py --pu`). This is the exact A5 path: same PU event seeds
hseed('sigpu', …) as the A2 row, same PV/MET/top-up seeds, quirk hits through ACTS digitisation + CKF. Each event also
gets the "noCKFq" variant, with the quirk CKF flags cleared (the A2 treatment). Population: 60 central (\|η_pair\| < 1)
template rows per point. In-job definition (≥ 50 % of the written quirk hits in an R04 candidate, f_CKF < 0.2):

| point (60 central rows) | A2 production (numpy, no quirk CKF) | full chain + PU (A5 path) | full chain, quirk CKF flags cleared | pairs (both / full only / A2 only / neither) | ⟨quirk-on-CKF⟩ with PU |
|---|---|---|---|---|---|
| E500 3 keV | 1.000 | **0.933** | 0.983 | 56 / 0 / 4 / 0 | 0.030 |
| E500 5 keV | 1.000 | **0.917** | 1.000 | 55 / 0 / 5 / 0 | 0.102 |
| E200 5 keV | 0.933 | **0.817** | 0.967 | 47 / 2 / 9 / 2 | 0.108 |

[V] Every full-chain loss relative to A2 disappears when the quirk CKF flags are cleared. One example is E500 5 keV row
3112: with PU, CKF takes 32/32 quirk hits. The numpy-vs-ACTS smearing difference is ≤ 2/60. The CKF stealing missing
from A2 is therefore **7-12 % of the (in-job) efficiency at 3-5 keV** (absolute −0.07 to −0.12), and it rises with Λ
(A1: ⟨f⟩ 0.23-0.40 at 10 keV).

For reference, the A1 no-PU re-runs on the same rows (in-job R04):

| point | base | quirk CKF cleared | no U-5 b merging |
|---|---|---|---|
| E500 3 keV | 0.700 | 0.733 | 0.767 |
| E500 5 keV | 0.483 | 0.617 | 0.617 |
| E200 5 keV | 0.283 | 0.417 | 0.417 |

Without PU, CKF and merging each cost 3-13 points. The rest of the A1-A2 gap is the PU-assisted seeding and N_IP2
completion (item 2).

---

## 5. sep_IT^det flat at 41-58 mm under PU (symptom e), class (iii)

`hitrec.sep_it(g, c)` (`analysis/hitrec.py:209-223`) splits **all** hits of the stored record at the median along n₂ in
each TBPX layer. `signal.analyse_file` (`signal.py:144`) passes the full record `g`, which under PU contains the PU hits
of the ±W_c band. The two "cluster means" then measure the PU spread, not the quirk separation. Production A2 records of
matched R04 candidates, E500 (`sepit_core.py`) [V]:

| Λ (keV) | as computed (all band hits) | core hits only | quirk-labelled hits only (diagnostic) | Stage-3 truth median |
|---|---|---|---|---|
| 1 | 43.0 mm | 20.0 | 13.1 | 29.1 |
| 2 | 41.6 | 19.7 | 7.5 | 7.0 |
| 3 | 42.8 | 13.4 | 4.6 | 3.1 |
| 5 | 40.6 | 18.2 | 2.0 | 1.1 |

Fix options. All of them belong to the P2 deliverable only and have no ε, B or limit impact:
- (a) Minimal: restrict to the core (`m = (g['LC'] == lay) & cm`). This is still PU-dominated at ≥ 2 keV.
- (b) Use a PU-robust estimator, e.g. per IT layer the separation of the two hits nearest the core centre that are
  consistent with two straight lines from the PV across ≥ 3 IT layers.
- (c) Report sep_IT^det at PU 200 as "not measurable with this estimator".

Because of item 2, at ≳ 3 keV the candidate plane is itself PU-defined, so no estimator built on the candidate's core
will recover Λ⁻² there. **Recommendation: (c) for the present report, (b) as future work.** The A1 values (no PU) remain
valid.

---

## 6. Signal-match labelling after merging (A02 reading): no problem found

`chain_inputs.merge_pool` gives a merged measurement the INT of its largest-dE member (`g1b_tt.assemble`). Both quirks
carry vp 4000 (INT % 10⁶ = 4000), so a quirk-quirk merge stays a quirk hit. The match (`hitrec.signal_match`) uses only
INT % 10⁶ == 4000, never the particle index, so a merge cannot "label as one quirk only" and kill the match. A
quirk + PU merge is labelled by dE, and the heavy, slow quirk usually wins.

The A1 "nomerge" variant (merge_scale → 0), on the same 60 E500 3-keV central rows, raises the in-job ε through N_IP2
(`rerun_summary.json`), not through labelling. In the production A1 files, `n_core_mismatch` = 0 and every stored record
of a matched candidate re-matches (13 390/13 390). **No (iii) here.** Merging hurts through N_IP2 (item 2), not through
the label.

---

## 7. Remedies and cost

| item | class | remedy | re-run? | cost |
|---|---|---|---|---|
| 1 | (ii) | Report V4-3 as A1 finder ε inside \|η_pair\| < 1 (table §1), and A1 vs A2 on **the same rows** (§2). Drop "max 0.21 vs 0.9". | no | 0 |
| 2 | (i)/(ii) | State in the report that R04 needs all 10 IP surfaces unmerged and a seed opening ≥ 1 mrad. Give the detector upper edge vs the truth f(any IP surface merged) = 50 % (≈ 5 keV), not vs the 100 µm median edge. Label A2 at ≳ 3 keV as PU-assisted. No rule change after the freeze; a merging-robust counting rung or a line-topology category would need a new pre-registration (cf. D4-14 (b)). | no | 0 |
| 3 | (iv) | Apply the plan's V4-6 revert rule: produce the A2 points with Λ ≥ 3 keV (E) and Λ = 5 keV (all five species-masses) through the full chain (the A5 kind, same rows, same seeds; it is paired to A2 by construction), and replace those A2 entries. Minimal set: {3, 5} keV × 5 species-masses × ≈ 200 template rows ≈ 2 000 events. | **yes** | 2 000 × (PU_S 10.2 + 0.6 + T1_S 8.0) s ≈ **10.5 CPU-h** (≈ 2 h wall on 6 cores). Then re-run `analysis.run_all` (signal + limits stages, ≈ 40 min). |
| 4 | (iii) | `analysis/hitrec.py:209-223`: label sep_IT^det at PU 200 as not measurable, or switch to a core-restricted, line-consistent estimator, and re-run `run_all --stages products` (minutes). | no production | < 0.1 CPU-h |

Impact of item 3 on the headline: [E] At the analysis-level match, the same relative loss applies to A2 ε at the affected points. Examples:
- E500 3 keV FB3: ε(r_fb) 0.145 → ≈ 0.135;
- E500 5 keV and the 5-keV FB4 points: −8 to −12 %;
- E200 at 5 keV: ≈ −12 %.

μ₉₅/N_exp at those points worsens by the same 7-12 %. The best point (E200 1.5 keV, FB2) is untouched, because the
quirk-on-CKF fraction is ≤ 2 % at ≤ 2 keV. **No conclusion of `STAGE4_RESULTS.md` changes:** there is still no WP and no
exclusion. The re-production is needed for correctness of the published ε at Λ ≥ 3 keV and to close V4-6 as the plan
defines it, not to rescue sensitivity.

---

## 8. Files

- Scripts (read-only use of frozen code): `acts/stage4/investigation/`
  - `cmp_rows.py`, `classify.py`, `a1_ladder.py`, `ckf_stats.py`, `notrial.py`, `truth_layers.py`, `truth_degeneracy.py`,
    `seed_diag.py`, `a2_record.py`, `sepit_core.py`, `nq_rows.py`
  - `rerun_a1.py` (production A1/A5 path for chosen rows, with noCKFq/nomerge variants)
  - `summarise.py`
- Outputs: `data/acts_stage4/investigation/`
  - `cmp_*.json`, `cmp_all.txt`, `classify_*.json`, `a1_ladder_*.json`, `truth_degeneracy_*.json`
  - `inv_A1_*.json`, `inv_A5like_*.json` (+ chain npz), `rerun_summary.json`, `logs/`
- The PU chain npz files (≈ 115 MB each, 9 files) can be deleted; the JSON summaries hold the results.
- Compute used: about 1.5 CPU-h, ≤ 7 processes (6 re-run workers + 1 niced reader), about 25 min wall.
