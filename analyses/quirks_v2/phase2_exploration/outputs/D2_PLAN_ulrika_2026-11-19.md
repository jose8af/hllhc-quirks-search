# D2 plan: robustness row "later arcs restored" (Ulrika, executor, 2026-11-19, written 11:19 -0500)

Written and committed **before any event is generated**. Frozen sources (read in full for the parts cited):
COMMITMENTS.md l.318-319 (D2 accepted, "a measured increase enters the binding day-15 reading"), l.353 (B6-a / B6-c
row), l.354 (B6-d); `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md` §1.5 (l.272-327;
called ADD below); STR l.1495-1507 (B6 criterion, paired design); amendment E4 (COMMITMENTS l.300-309: event-level
clustered bootstrap errors). Mechanism: `outputs/A1_OPTION_A_xavier_2026-11-16_16-17.md` (option (a), class
`HybridParent` of `src/p2x_b1.py`), `outputs/HALF_TURN_xavier_2026-11-16_16-08.md`, `outputs/LOOPER_GUN_xavier_*.md`.
Background only: no signal file is read, no signal quantity is formed (the optional signal arm of ADD §1.5 is not
run). Tags: [V] verified by me (file:line or campaign), [E] estimate, [U] unverified.

## 1. What the row is

- **Events.** 600 ρ = 1 pile-up events (one bunch crossing at μ = 200 each, 4 roads per event = 2,400 trials):
  events 0-599 of the C1 pile-up sample `c1.pu1`, i.e. the 30 jobs `c1pu1-0000` … `c1pu1-0029` of campaign
  `p2-a-c1-pu1` (20 events per job, frozen v1 finder: road 0.15, T_seed 4; every event has its pre-top-up chain
  output dumped) [V: `tools/runner/campaigns/p2-a-c1-pu1.json`, markers `ledger/markers/p2-a-c1-pu1/000/c1pu1-00{00..29}.marker`
  all `done`; `meta_json.job.dump_events = 20` in c1pu1-0000.npz].
- **Varied arm ("later arcs restored").** Per event: the same generator events (the event seeds stored in the
  nominal file's `chain_meta.event_seeds`), the same Fatras random seed (job seed), the unchanged chain
  (`acts/stage4/code/run_chain.py` imported, not modified). Every charged row given to Fatras (the generated
  particles of the 200 interactions; generation 0) is also fired through Geant4 (`g4hv` option `allx`, FTFP_BERT,
  validated geometry, 3.8 T, until decay, interaction, stop, exit or 25 ns; products not followed), and its
  Geant4 crossings of sensitive surfaces are added as SimHits after Fatras and before digitisation (the
  `run_chain.Inject` / `HybridParent` mechanism), then digitised, seeded and CKF-tracked by the chain.
  **Injection rule** (fixed here): a Geant4 crossing of particle P is injected iff (i) it is beyond half a turn
  of P (turn computed as in `p2x_ht_g4.py`: transverse path from time and initial momentum / 2πR) **and** (ii) it
  is later than P's last Fatras SimHit (any surface) by more than the validated seam 0.005 ns (if P has no
  Fatras SimHit, condition (ii) is void). The injected hit carries P's barcode, Geant4 position, time and
  momentum, no energy deposit (dE = 0), as in option (a) and the looper gun.
- **Finder input of the varied arm** (paired at the hit level): the **nominal event's own pre-top-up hits**
  (the dumps of `c1pu1-*`, i.e. exactly the hits the nominal finder saw, with their CKF flags) **plus the injected
  measurements** of the varied chain (matched by their truth position to the injected SimHits; with the CKF flag
  the varied chain gave them). Reason: the digitisation draws its smearing from one per-event stream, so the extra
  SimHits re-smear every later nominal hit; with the finder's 30 µm plane tolerance that would make the two arms
  nearly independent at the candidate level and destroy the pairing that STR l.1505-1507 asks for. The varied
  chain's own copy of the nominal hits is used only for checks (§4: same truth positions and counts as the dumps;
  CKF flags changed by the injected hits are counted and reported).
- **Top-up (density fixed at the raw level, ADD l.282).** The top-up of each layer is drawn **exactly as in the
  nominal** (v1 `pu_inputs.topup` on the nominal hits, same per-event random stream `SeedSequence(job seed)
  .spawn(20)[ie]`, so the PV draw, the road angles and the trial seeds that follow are identical to the nominal's)
  and then the **last n_inj(layer) top-up crossings of that layer are dropped** (both sensors of a stacked layer),
  where n_inj(layer) = injected measurements on the layer before CKF removal (pixel layers: the layer's surface;
  stacked layers: the inner sensor, the one the v1 top-up counts). If n_inj(layer) > top-up crossings, the top-up
  of that layer is zero and the excess is reported per layer. CKF removal, U-5 b merging, the PV, the roads and
  the frozen finder then run as in v1 (`chain_inputs.prepare_event`, `run_stage4.run_pu_job`, `production.process_trial`;
  reproduced in my job script without changing any v1 file).
- **Nominal (comparison baseline).** The same 600 events on the present chain: the existing `c1pu1-0000…0029`
  outputs, **if** my finder job run on the dumps with injection switched off reproduces their per-trial rung counts
  bit for bit (control job, §4). If it does not (e.g. the float32 storage of the dumps changes a candidate), the
  nominal arm is re-run from the dumps with my job and injection off for all 600 events (+ 7.3 CPU-h [E], inside
  the cap of §5), so that the two arms differ only by the exchange of top-up crossings for arcs.

## 2. Quantity per rung

r(R) = B_var / B_nom, with B = pile-up candidates per trial counted as the frozen object of [SD4] (STR l.1128:
distinct hit sets after grouping at the target density; at ρ = 1 the direct count `trials.n_grp[:, R]`, as
`c1_compare.py` uses for pu1), summed over the same 2,400 trials in both arms (so r = Σ n_grp,var / Σ n_grp,nom).
Rungs **R04, R05, R06** (RUNGS columns 3, 4, 5 of `acts/stage4/finder/production.py` l.28). Reported per rung:
B_nom, B_var, ln r, its error, and the trend ln r(R06) − ln r(R04) with its error.
Read in addition, no verdict (ADD l.309): (a) in the varied arm, R04–R06 candidates with ≥ 1 double-crossing layer
whose two hits come from one particle with at least one of them injected (truth); (b) r at "N_2S2 ≥ 1, 2, 3 on top
of R04, R05, R06" (groups with a member passing the rung and n2s2 ≥ k, counted from the candidate records).

## 3. Error

**Event-level clustered bootstrap, paired** (amendment E4 Q1: every quantity counted per candidate gets an
event-level width, not 1/√N): resample the 600 events with replacement, the **same** resample for both arms and for
all rungs (joint replicas, `c1_compare.cluster_boot_ln` pattern), each replica gives ln(Σ_var/Σ_nom) per rung and the
trend difference; error = standard deviation of the replicas, 2,000 replicas, fixed seed. The unpaired error
(the two arms bootstrapped independently) and the Poisson 1/√N value are quoted beside it, as ADD l.291-292 says
those are only bounds. Both arms are complete over the same 600 events or the row is not read.

## 4. Checks before the row is read

1. Chain smoke (2 events): runs, V4-1 closure of the chain passes (injected SimHits = injected measurements up to
   v1's tolerance), injected counts per event plausible against HALF_TURN (≈ 1.8×10⁴ crossings on counting
   surfaces per crossing of 200 interactions [E from 89.3 per interaction, p2-c-pa-htg]).
2. In every chain job: the non-injected written hits of each event equal the nominal dump (count per surface and
   truth position); CKF flag differences counted. Duplicates at the seam counted (injected crossing within 0.005–0.05 ns
   of a Fatras hit of the same particle on the same surface).
3. Control: my finder job with injection off on the 20 events of `c1pu1-0000` reproduces that file's `trials.n_grp`
   and `trials.n_pass` (all 43 columns) for all 80 trials.
4. Every varied finder job: PV, road angle and trial seed of each trial identical to the nominal's (pairing check).

## 5. CPU estimate (measured unit costs)

| item | unit cost [source] | 600 events |
|---|---|---|
| nominal (existing) | 1,115 CPU-s per 20-event job, 33,439 CPU-s for jobs 0000-0029 [V: markers] | 0 (exists) |
| varied chain: generation + Fatras + digi + seeding + CKF | 13.4 s/event nominal [V: c1pu1-0000 `t_chain_s` 267.5 s / 20]; × ≈ 1.37 on the post-Fatras stages for 37 % more hits [E] → ≈ 18 s | 3.0 h |
| Geant4 for every charged particle | 0.478 ms per particle [V: p2-c-pa-htg-mb.json `g4_ms_per_particle`] × 52.58 charged per interaction [V: same file] × 200 = 5.0 s | 0.8 h |
| Python injection overhead | ≈ 1–2 s/event [E] | 0.3 h |
| varied finder (density fixed: pool ≈ nominal) | 870 CPU-s per 80 trials [V: c1pu1-0000 `cpu_s_tt`] = 43.5 s/event; × 1.0–1.3 [E] | 7.3–9.4 h |
| checks (smoke, control, analysis) | [E] | ≈ 1 h |
| **total** | | **≈ 12.4–14.5 CPU-h [E]**; +7.3–9.4 if the nominal must be re-run (§1): ≤ 24 |

Below the 22–28 CPU-h of ADD l.299 (12–18 with an existing partner): no stop-and-ask. Stop rule: if the measured
cost of the first jobs projects the total above 28 CPU-h, I stop and ask before launching the rest.
Job layout: `p2-c-d2-chain` 30 jobs × 20 events (≈ 500 s each [E]); `p2-c-d2-find` 60 jobs × 10 events (≈ 450–570 s
[E]); `p2-c-d2-ctl` 2 jobs × 10 events (control); `p2-c-d2-sum` 1 job. All ≤ 30 min, nice 10, ≤ 2 jobs per node,
landau / maxwell / schrodinger only, ≤ 3 jobs per node in total (SLOTS.md line first). Data prefix `p2c/d2`.

## 6. Pre-declared reading (ADD l.308-321, copied, not changed)

- **Evaluated (B6-a):** error on ln r below 0.1 at R06. If not reached with 600 events, the row is "not evaluated
  at R06"; no events are added without asking.
- **No effect:** |ln r| ≤ 0.1 and within 2σ of zero at all three rungs, and no trend of ln r from R04 to R06 beyond
  2σ. Then [L15] is stated with a measured size; the chain is kept.
- **Effect, robust** (|ln r| ≤ ln 2 at R04–R06): if r(R06) > 1 the pile-up estimate is multiplied by r(R06), with a
  width of its bootstrap error and the width of STR §4.0 point 7 counted from R06; no credit for r < 1.
- **Effect, not robust** (|ln r| > ln 2 at a rung, or ln r(R06) − ln r(R04) > 0 by more than 2σ): limitations and
  abstract level; the user chooses between the correction and a chain fix, before the freeze.

**What B6-d does with it** (COMMITMENTS l.354, with D2 accepted l.318-319): only if the row shows an increase
(r(R06) > 1 under "effect, robust"), the pile-up estimate is corrected by the factor r(R06) with its measured
bootstrap error as a source-defined variation (STR l.1477-1478), and by the user's D2 answer this corrected
pile-up term enters the binding day-15 reading. No effect, or r(R06) ≤ 1: no correction, [L15] stated with the
measured size. "Not robust": no automatic correction; the question goes to the user.

## 7. Ambiguities in the frozen text (flagged, not resolved by me beyond the working choice stated)

1. **Which crossings are "beyond half a turn".** ADD l.275-276 says "crossings beyond half a turn"; the validated
   option-(a) mechanism (A1_OPTION_A) injects crossings later than the last Fatras hit + 0.005 ns, with no turn
   condition. Working choice: both conditions (§1). Crossings that pass only the time condition (Fatras ended before
   half a turn, Geant4 did not) are counted and reported, not injected.
2. **Particles without any Fatras SimHit** (p < 30 MeV Fatras pMin, or no sensitive crossing in the first half turn):
   working choice: their crossings beyond half a turn are injected. Reported separately.
3. **Detector secondaries** (Fatras generation ≥ 1: conversion legs, δ-rays) also stop at half a turn and are
   not restored: "every charged particle of the 200 interactions" read as the generator particles given to Fatras.
4. **n_inj per stacked layer**: the v1 top-up counts the inner sensor; working choice as §1. BTL and endcap
   injected hits have no top-up to exchange against and are simply added (BTL enters only the time tag columns,
   not R04–R06).
5. **Nominal hits re-smeared** by the injection (digitisation stream): resolved by the dump composition of §1; this is
   a construction choice, documented, and its size (CKF-flag changes) is measured.
6. **"No effect" vs "effect, robust"**: a significant |ln r| ≤ 0.1, or a significant negative trend, satisfies neither
   "no effect" nor "not robust": it falls under "effect, robust" (correction only if r(R06) > 1). The "no effect"
   trend test is two-sided, the "not robust" one one-sided; I apply them as written.
7. **"Development-role events"** (ADD l.305): the C1 pile-up events are used. They are the C1 reproduction sample
   and B2 development events, not a Phase-4 closure sample; no closure verdict reads them. Flagged for the orchestrator.
8. **R04 truth reading (a)**: v1's ρ = 1 storage keeps full hit records only for R04 candidates that also pass
   w < 37.5 mm or p > 10⁻³ (`production.py` l.400); reading (a) is complete at R05–R06 and partial at R04.
9. **Width of the B6-d correction**: "the width of STR §4.0 point 7 counted from R06" is not computed here; I report
   r(R06) and its bootstrap error only.
