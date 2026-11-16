# Cost reduction, pool and toy projections — channel (iii), Tatiana, 2026-11-16 13:25

Tags: [V] measured (campaign under `data/p2c/`, `logs/p2c/`), [E] estimate. Projections: `src/p2c_rule1.py` with a
byte-identical copy of the Phase-1 budget script (`data/p2c/p2-c-rule1b/000/p2-c-rule1b-0.json`). Cost of this study:
0.27 CPU-h (campaigns p2-c-prof, p2-c-prof2, p2-c-rule1, p2-c-rule1b).

## 1. Where the no-pile-up hard-scatter event spends its time

Per kept event, ms. Chain stages from the 10⁴-event timing jobs [V: p2-c-t-hs0]; generator split from the step-timed
generator loop [V: p2-c-prof, 1,500 / 1,000 / 300 kept events; that job ran on a node with 5 jobs, so its absolute
times are ≈ 20 % high and only the shares are used].

| step | Z(νν) | W(τν) | tt̄ 1ℓ | reducible without changing physics or content? |
|---|---|---|---|---|
| generator tries per kept event | 3.3 | 9.1 | 48 (23.7 with forced decays) | tt̄ only (below) |
| Pythia `next()` per try (hard process, showers, MPI; hadronisation off) | 9.1 | 9.8 | 9.7 | no: showers and MPI are interleaved, and the filter needs them |
| hard process alone (process level) | 0.04 | 0.02 | 0.03 | — |
| all tries (job) | ≈ 30 | ≈ 86 | ≈ 450 | see below |
| hadronisation of pre-filtered events | 4.5 | 6.4 | 6.1 | no |
| Python loops in the generator (MET sums per try, particle list, selection; tt̄: lepton count per try) | ≈ 6 | ≈ 10 | ≈ 45 | partly: tt̄ lepton count (28) disappears with forced decays; the rest needs a rewrite of `s4pu` loops (not done) |
| my generator-level summary (v1 preselection weight, jets, leptons) | 9.7 | 11 | 14 | partly (a rewrite; ≈ −5, not done); dropping it changes the recorded content |
| Fatras + digitisation | 38 | 38 | 50 | no |
| seeding + CKF | 22.5 | 23 | 32 | no (the CKF flag is recorded) |
| dump (Python in `run_chain.Dump`) | 17.5 | 18 | 25 | not resolved: cProfile does not see callbacks made from ACTS; not attempted |
| compression and write | 2 | 2 | 3 | no |
| **job CPU per kept event, before** | **127** | **171** | **571** | [V: p2-c-t-hs0] |
| **after** | **127** (no verified gain) | **171** (no verified gain) | **≈ 310** [E from V parts] | |

What was tried:
- **Filter placed earlier.** A veto at process level would save 9–10 ms per vetoed try, but it is not a subset of
  the filter. Z(νν): the process-level neutrino MET equals p̂T, and 18.5 % of the kept events (278 of 1,500) have
  p̂T < 200 GeV, down to the generator cut at 150 (showers raise the Z pT). W(τν): 40 % of tries have process-level
  MET < 75 GeV and 0 of 1,000 kept events do (upper limit 0.3 % at 95 %); 1 kept event is below 100 GeV. tt̄: kept
  events reach down to 34 GeV. So no provable early cut exists; for W an empirical cut at 75 GeV would give
  171 → ≈ 137 ms with a measured leak below 0.3 % [E]. It is not applied: it changes the sample.
- **tt̄ forced decays [V: p2-c-prof-gen-tt1f].** W⁺ → ℓν and W⁻ → hadrons forced in the decay table (and the
  charge-conjugate configuration for the other half): 23.7 tries per kept event instead of 48.3, every try has exactly
  one leptonic W (0 of 7,100 fail the test), σ_gen = 3.16×10⁻⁸ mb = 0.2187 × the unforced 1.445×10⁻⁷ mb, the expected
  branching factor. Generator cost 0.536 → 0.287 s per kept event (0.274 without the now redundant lepton count). Job cost
  571 → ≈ 310 ms [E: 571 − (536 − 274); the chain part is unchanged]. This is the same physics by construction; it
  needs two generator configurations per tt̄-type sample and is a change of `s4pu.SM_SAMPLES` (chain code, to be
  logged in `CHAIN_PROVENANCE.md`); not yet run through the chain.
- **Stated plainly:** for Z(νν) and W nothing above ≈ 10 % is recoverable without changing the sample, the recorded
  content or the chain code; the ×2.8 against the 45 ms guess is real (the guess left out the 3–9 tries and took a
  10-track gun for a 900-hit event).

**Geant4 firing, 0.41 against 0.134 ms [V: p2-c-prof2-g4, 2×10⁵ firings each, one job].**

| configuration | ms per firing |
|---|---|
| FEAS gun (π±, pT log-uniform 1–10 GeV), FEAS geometry (12 unsplit barrel tubes) | 0.113 |
| FEAS gun, full geometry (83 slabs with the discs, sensitive slabs in two halves) | 0.264 |
| natural π/K spectrum (pT > 0.5 GeV), FEAS geometry | 0.159 |
| natural spectrum, full geometry | 0.391 (pT > 1 GeV: 0.263; pT < 1 GeV, 69 % of firings: 0.436) |
| natural spectrum, full geometry, QGSP_BERT | 0.382 |

It is the geometry (×2.3) and the soft spectrum (×1.5), not the node load (0.41 with 3 jobs, 0.39 alone) and not the
physics list. The geometry is the one B1-d requires; unsplitting the sensitive slabs would recover part of the
×2.3 but loses the exact parent crossings (variant B input). Not changed. Effect on the plan: the DIF vertex costs
11.6 ms (STR 12.2), the NI pass 0.047 ms per firing serves the three radii at once.

## 2. Pool at the approved CPU (user decision 2026-11-16): replacement rows for STR Table 4.4a [E]

Rule of STR §4.4: M_t ∝ √(N_t/c_t) at G = 1, hard-scatter share fixed at its planned 457 CPU-h and the B1 share at
its planned 208 CPU-h. c_t: [V] for Z(νν), tt̄ 1ℓ and the B1 terms; W(τν)'s 171 ms used for every W and WW/WZ, tt̄'s
for tW, tt̄ 2ℓ, t-channel, Z(νν)'s for ZZ, Z(ττ), Z(ℓℓ) [E: not measured]. N_t as in Table 4.4a.

| term | N_t | c_t (ms): STR → measured (after forced tt̄) | M_t: STR → measured (after) | floor at 68 %: STR → measured (after) |
|---|---|---|---|---|
| Z(νν)+jets | 2.51×10⁷ | 45 → 127 | 1.10×10⁷ → 3.08×10⁶ (3.33×10⁶) | 2.60 → 9.28 (8.58) |
| W(τ_h) | 5.41×10⁶ | 45 → 171 | 5.10×10⁶ → 1.23×10⁶ (1.33×10⁶) | 1.21 → 5.00 (4.62) |
| W(eν) | 2.54×10⁶ | 45 → 171 | 3.50×10⁶ → 8.44×10⁵ (9.13×10⁵) | 0.83 → 3.43 (3.17) |
| tt̄ 1ℓ | 2.38×10⁶ | 45 → 571 (309) | 3.39×10⁶ → 4.47×10⁵ (6.58×10⁵) | 0.80 → 6.06 (4.12) |
| W(τ_ℓ) | 2.26×10⁶ | 45 → 171 | 3.30×10⁶ → 7.96×10⁵ (8.61×10⁵) | 0.78 → 3.23 (2.99) |
| W(μν) | 2.24×10⁶ | 45 → 171 | 3.28×10⁶ → 7.92×10⁵ (8.57×10⁵) | 0.78 → 3.22 (2.97) |
| tW | 2.59×10⁵ | 45 → 571 (309) | 1.12×10⁶ → 1.48×10⁵ (2.17×10⁵) | 0.26 → 2.00 (1.36) |
| tt̄ 2ℓ | 2.13×10⁵ | 45 → 571 (309) | 1.01×10⁶ → 1.34×10⁵ (1.97×10⁵) | 0.24 → 1.81 (1.23) |
| WZ | 1.37×10⁵ | 45 → 171 | 8.14×10⁵ → 1.96×10⁵ (2.12×10⁵) | 0.19 → 0.80 (0.74) |
| WW | 1.26×10⁵ | 45 → 171 | 7.80×10⁵ → 1.88×10⁵ (2.04×10⁵) | 0.18 → 0.76 (0.71) |
| t-channel | 1.10×10⁵ | 45 → 571 (309) | 7.28×10⁵ → 9.6×10⁴ (1.41×10⁵) | 0.17 → 1.30 (0.89) |
| ZZ | 1.05×10⁵ | 45 → 127 | 7.10×10⁵ → 1.99×10⁵ (2.15×10⁵) | 0.17 → 0.60 (0.55) |
| Z(ττ) | 4.26×10⁵ | 45 → 127 | 1.43×10⁶ → 4.01×10⁵ (4.34×10⁵) | 0.34 → 1.21 (1.12) |
| lost-lepton Z(ℓℓ) | 2.98×10⁴ | 45 → 127 | 3.79×10⁵ → 1.06×10⁵ (1.15×10⁵) | 0.09 → 0.32 (0.30) |
| **SM hard scatter, sum** | | | 3.65×10⁷ → 8.66×10⁶ (9.69×10⁶) | **8.6 → 39.0 (33.3)** |
| DIF | 6.51×10⁷ | 23.7 → 15.3 | 2.44×10⁷ → 3.66×10⁷ | 3.04 → 2.03 |
| NI 22 / 30 / 61.5 mm | 0.88 / 1.12 / 1.12×10⁶ | 14.7 → 11.2 / 13.3 / 13.3 | 3.61 / 4.06 / 4.06×10⁶ → 4.96 / 5.12 / 5.12×10⁶ | 0.28 / 0.31 / 0.31 → 0.20 / 0.25 / 0.25 |
| **DIF and NI, sum** | | | | **3.9 → 2.7** |
| **all pool terms** | | | | **12.6 → 41.7 (36.0)** |

- If the 665 CPU-h are re-allocated jointly over B1 and SM by the same rule: summed floor 37.2 (32.6) [E].
- "Planned pool, more CPU": the planned M_t cost 2,409 CPU-h (1,954 with forced tt̄) instead of 665.
- Not in the table: the multijet population (10⁶ events at an unmeasured cost) and the open N_t questions of the memo
  (O3, O12) change the B1 rows. If pool events must be preselected events (memo, pilot size), every SM floor is
  further divided by the preselection weight of its process (0.40 for Z(νν) [V on 200 events]; others unmeasured).

## 3. Toys against the 183 CPU-h toy budget [E from V unit costs: p2-c-t-pyhf]

| parameters | s per 1000 + 1000 hybrid toys at one μ | ratio to STR's 652 s | toy budget at that cost (CPU-h) |
|---|---|---|---|
| 31 | 638 (200 toys) | 0.98 | 179 |
| 60 | 11.1×10³ (110 toys) | 17 | 3.1×10³ |
| 80 | 17.8×10³ (12 toys) | 27 | 5.0×10³ |
| 100 | 48.6×10³ (12 toys) | 75 | 13.6×10³ |

Items scaled: pass 1 80, its exact check 22, pass 2 48, its check 13, T1-c (iii) 20 (STR §4.11 pt 5, pt 6). Synthetic
workspace of the T1 form (auxiliary Poisson channel per counted term, censored nuisances), pyhf 0.7.6, numpy
backend, scipy SLSQP with numerical gradients. The toy budget holds only near 31 parameters.
What I would test, in this order, none of it done: (1) a gradient backend (jax or pytorch) with the same model;
(2) minuit with a tuned strategy; (3) fewer free parameters per fit: the λ of terms whose transfer factor is below
1 % of the bin content fixed at their posterior mean (pruning rule T1-f applies); (4) the auxiliary channels merged
into one multi-bin channel (fewer pyhf channels, same likelihood). (1) needs the install slot, held by channel (ii).
