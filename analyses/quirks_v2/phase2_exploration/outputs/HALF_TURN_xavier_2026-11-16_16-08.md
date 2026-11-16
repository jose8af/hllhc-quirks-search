# The half-turn limit of the detector chain — Xavier, 2026-11-16 16:08

Asked for by the orchestrator after `outputs/A1_TRUNCATION_xavier_2026-11-16_15-40.md`. Tags: [V] run or read by me
(campaign, or file:line); [E] estimate; [U] not verified. Campaigns: markers `ledger/markers/<campaign>/000/`, data
`/nfs/cajuela/jdochoa/quirks_v2/data/p2c/px_validation/<campaign>/000/` (validation slices, streams `px.*`; not pilot
data). CPU of this study: 0.42 CPU-h (p2-c-px-ht 0.27, p2-c-px-htg 0.16, p2-c-px-a1d/-a1e 0.002) of the 3 allowed.
Background only; no signal sample and no selection quantity.

## Statement

**Phase 1 assumed** that the chain propagates curling particles: v1's plan lists in-time loopers ("repeated crossings,
2 hits per layer from one particle") as simulated (`TT/acts/stage4/plan.md` l.1267), kept a looper gun as a topology,
and the strategy's hand-over gives "the parent's hits up to the vertex" (STR l.744).
**Phase 2 found** that in this chain (Fatras of pyacts 48.0.0 as `run_chain.py` calls it) no particle leaves a hit
beyond half a turn of its helix. With Geant4 as the reference, the generated charged particles of a no-pile-up Z(νν)
event cross the barrel counting surfaces 958 times, of which 204 (21 %) after half a turn; of a minimum-bias
interaction 312 times, of which 89 (29 %). The chain's hit record lacks them: 25 % and 37 % more hits than written,
40–58 % more on the TBPS layers.
**Implications.** (1) Review finding A-1 cannot be closed by any truncation rule: the parents of DIF-C and NI-C reach
their vertex after half a turn by definition of these classes. (2) Own-hit counts H of every no-pile-up sample
(pilot, pool) and the pile-up occupancy from Fatras are without the later arcs of particles below p_T ≈ 0.63 GeV.
(3) v1's looper result (0 in 10⁵) is what the limit gives by construction, not a measured rejection. (4) The limit
is compiled into the installed ACTS: lifting it needs a rebuild or a new multi-pass construction; neither was done.

## a. Mechanism

VERIFIED from the installed software (`acts/.pixi/envs/default/lib/python3.12/site-packages/acts/`, wheel
`pyacts-48.0.0`; the wheel has no C++ headers or sources):
- `run_chain.build_sequencer` calls `addFatras(s, tg, field, rnd=rnd, pMin=0.03 GeV, inputParticles=…, logLevel=…)`
  and nothing else for the simulation (`acts/stage4/code/run_chain.py` l.326-327). There is no loop, path-limit or
  step setting anywhere in `acts/stage4/code/*.py` (grep).
- `addFatras` builds `acts.examples.FatrasSimulation` with level, input/output names, random numbers, geometry,
  field, `generateHitsOnSensitive=True`, the four EM switches and `pMin` (`examples/simulation.py` l.481-535).
- `FatrasSimulation.Config` as exposed to Python has exactly: `emScattering`, `emEnergyLossIonisation`,
  `emEnergyLossRadiation`, `emPhotonConversion`, `generateHitsOnSensitive/Material/Passive`, `inputParticles`,
  `outputParticles`, `outputSimHits`, `randomNumbers`, `trackingGeometry`, `magneticField`,
  `averageHitsPerParticle`, `pMin` (`examples/ActsExamplesPythonBindings.pyi` l.2599-2630). **No field for loop
  protection, loop fraction, path limit or maximum steps.** (`ptLoopers` and `maxSteps` in that file belong to
  `PropagationAlgorithm` and another class, not to Fatras.)
- `libActsExamplesFatras.so` contains the Fatras propagator with the actor list
  `SimulationActor<RandomEngine, NoDecay, InteractionList<PhotonConversion>, …>` **plus `Acts::PathLimitReached`**, and
  the messages of ACTS's loop protection, "Path aborter limit set to … (full helix = …" (`strings`).
- Empirically the cut is at 0.50 turn: the Fatras parent's last hit is at ≤ 0.50 turn in all eight B1 slice files
  [V: p2-c-px-a1d]; in 5,000 Z(νν) slice events 231 of 3.94×10⁶ hits of generated charged particles are beyond
  0.5 turn, behind a sharp edge [V: p2-c-px-a1e].

INFERENCE (not read in source, which is not installed): the propagator inside Fatras runs with ACTS's default loop
protection, which sets a path limit of half a helix turn. I do not quote the default's name or value from memory.

**Configurable from Python without rebuilding ACTS: no** (the algorithm is compiled; its configuration has no such
field). Per instruction no build was attempted and no slice with the limit lifted exists (item c of the request is
therefore not done). One thing that is possible without a rebuild but was not tried: simulated particles expose
their final state (`SimParticle.finalState`, same file l.2382), so a second and third Fatras pass could be started
from where the first one stopped, with the hit containers merged. That is new chain code with its own validation
(double counting at the hand-over point, scattering and energy loss across passes, barcodes), not a setting.

## b. Size, with Geant4 as the reference [V: p2-c-px-ht (chain), p2-c-px-htg (comparison)]

Method. 2,000 no-pile-up Z(νν) events and 20,000 single minimum-bias interactions through the unchanged chain
(`p2x_ht_chain.py`; V4-1 closure passes in both). Every charged particle given to Fatras was then fired through
Geant4 (FTFP_BERT, the validated geometry, 3.8 T) from its own production point, time and momentum, and every
crossing of a sensitive surface recorded until the particle decays, interacts, stops, leaves the tracker (r > 1.2 m,
|z| > 2.7 m) or reaches 25 ns (`p2x_ht_g4.py`; `g4hv` option `allx`, added to Tatiana's `g4/g4hv.cc`: 18 changed
lines, default behaviour unchanged, sha fd10a890… → b5ad93a0…). Crossings and hits are compared per particle and
barrel counting surface, with multiplicity. So the reference is what Geant4 lets the particle do, not an ideal helix.
Not in the comparison: secondaries made in the detector (conversion legs, δ-rays; Fatras hits of generation ≥ 1 are
5 % of the written hits and are left out on both sides), so the missing crossings below are a lower bound.

| per event | Z(νν), no pile-up | one minimum-bias interaction | × 200 (one PU-200 crossing) [E] |
|---|---|---|---|
| charged particles given to Fatras; central (\|η\| < 1) | 138.6; 40.1 | 52.6; 12.5 | |
| central with p_T < 0.63 GeV (2R < 1.1 m: turns inside the barrel) | 19.3 (48 % of central) | 8.7 (70 %) | |
| written hits on counting surfaces (of which generation 0) | 833 (789) | 244 (234) | 4.9×10⁴ |
| Geant4 crossings of those particles | 958 | 312 | 6.2×10⁴ |
| of which after half a turn | **204 (21.3 %)** | **88.8 (28.5 %)** | 1.8×10⁴ |
| Geant4 crossings without a Fatras hit | 209 = 25 % of the written hits | 91.0 = 37 % of the written hits | 1.8×10⁴ |
| Fatras hits without a Geant4 crossing (particle decayed, interacted or stopped earlier in Geant4) | 39.7 (5 %) | 13.8 (6 %) | |

By layer, Geant4 crossings without a Fatras hit as a fraction of the Fatras hits on that layer (Z(νν) / minimum bias):
TBPX L1 6.5 / 8.3 %, L2 10.9 / 14.4 %, L3 14.9 / 20.9 %, L4 17.8 / 25.9 %; TBPS L1 42 / 58 %, L2 39 / 57 %, L3 34 /
53 %; TB2S L1 27 / 46 %, L2 20 / 38 %, L3 11 / 24 %. In absolute numbers per Z(νν) event: 6.0–7.9 per pixel layer,
34 / 24 / 16 per TBPS surface, 9 / 5 / 2 per TB2S surface.

By parent p_T (missing crossings per Z(νν) event): 0.05–0.1 GeV 2.6; 0.1–0.2 24.7; 0.2–0.3 45.8; 0.3–0.45 63.9;
0.45–0.63 49.3; 0.63–1.0 22.6; above 1 GeV 0.4. By turn (Geant4 crossings per Z(νν) event): 0.5–0.75 turn 36.5;
0.75–1 47.0; 1–1.5 48.5; 1.5–2 30.2; 2–3 28.8; 3–5 12.3; beyond 5 0.8.

What happens in reality to the particles that could loop (central, p_T < 0.63 GeV; Geant4, 38,665 in Z(νν) and
174,722 in minimum bias, the two samples agree within 0.01): 11 % end before half a turn, 11 % between half and one
turn, **77 % are still alive after one full turn**. How they end within 25 ns: decay 28 %, inelastic interaction
14 %, stopped, captured or annihilated 3 %, left the tracker 33 %, still circulating at 25 ns 21 %, no record 1 %.
So absorption and range-out remove about a fifth of them before the second half turn; the rest make the crossings
counted above.

Cost side of a lifted limit, estimates only (no slice exists): hits per event would rise by at least 25 % (Z(νν))
and 37 % (minimum bias), concentrated in the TBPS layers; the Fatras + digitisation stage is 40 of 133 ms per
Z(νν) event and would grow about in proportion to the path simulated [E]; for a PU-200 crossing (channel (i): 12.3 s)
the same +37 % of hits enters the finder's combinatorics, whose scaling I have not measured [U]. Whether the step-limit
drops and V4-1 change cannot be said without the slice.

## d. v1 code and documents

Looked in: `stage2_C001_quirks/` (all `*.md`, `*.py`, `*.tex`, `*.json`, `*.txt`), `book/`, `publication_plan/`,
`analyses/quirks_v2/CHAIN_PROVENANCE.md`, `analyses/quirks_v2/{acts,sim}` with grep for "loop protection",
"loopFraction", "half a turn / half-turn", "path limit", and for "looper". **No v1 file mentions a loop or path
limit of Fatras.** The only hit is a listing of the ACTS source tree (`TT/acts/probe/src/tree.json` l.3741:
`Core/include/Acts/Propagator/detail/LoopProtection.hpp`), not its content. What v1 does say about loopers:
`TT/acts/stage4/plan.md` l.149 records only the `pMin` pitfall ("the default pMin is 0.5 GeV, which drops every
looper. It is set to 30 MeV"); l.1267 lists "In-time low-pT loopers (PU): repeated crossings, 2 hits per layer from
one particle" as present in Pythia + Fatras ("**yes**"); l.299-301 explains the Fatras density deficit against the TDR
(×2.3–7.3, "rising with radius") by "out-of-time loopers and missing secondaries"; the looper gun (π/e, p_T 0.05–0.7
GeV, `code/s4cp.py` l.15) is attributed by "≥ 2 crossings in a layer" (`G1_REPORT.md` l.210) and counted 0 of 10⁵
without pile-up and 0 of 500 with it (`investigation/INV_STATS_BKG.md` l.247-249). A particle stopped at half a turn
moves outward only and cannot cross a layer twice, so that zero follows from the limit. v1 therefore had the limit
(same pyacts version, same chain code, `run_chain.py` unchanged) and did not know it. Part of the in-time density
deficit that v1 covers with its TDR top-up is this effect [E: 37 % of the hits per minimum-bias interaction, against
a deficit of ×2.3–7.3].

## Options (C1 must reproduce v1 with v1's setting in every case)

| option | what it costs | what it leaves inconsistent or open |
|---|---|---|
| (a) DIF-C / NI-C only: Fatras parent up to half a turn (time cut), the stored Geant4 crossings of the parent beyond it injected as SimHits through the chain's `Inject` algorithm | code in `p2x_b1.py` and one slice with the ≤ 2 % check: a few hours of work, < 0.1 CPU-h; no change of any other sample | the products of every vertex, and every particle of the SM and pile-up samples, still stop at half a turn; the injected parent hits carry Geant4's scattering, the others Fatras's |
| (b) the same with all parent hits from Geant4 crossings (second variant of STR l.744-746) for these two classes | as (a) | as (a); in addition the parent's first half turn is no longer the Fatras one used in the first-arc classes |
| (c) lift the limit in the whole chain: rebuild ACTS with the loop protection changed, or (c′) repeated Fatras passes from the final states | (c): a build of ACTS on the workers (not allowed without a decision; cost not estimated) and a second environment, since C1 keeps v1's; (c′): new chain code and its validation, days rather than hours [E]. Then: every v2 sample regenerated with it, the Z(νν) pilot included (85 CPU-h if it had been run); hits per event + 25–37 % or more, with the PU-200 chain and finder cost to be re-measured; v1's top-up ratios, occupancy model inputs and every v1-based planning number re-derived | C1 reproduces v1 at v1's setting while every v2 number is at another: the v1-to-v2 comparison then contains this change; the top-up and the lifted limit must not count the in-time loopers twice |
| (d) keep the chain; state the limit | nothing | DIF-C and NI-C (1.5×10⁸ of the 3.7×10⁸ single-interaction vertices) are terms whose parent hits the chain cannot make: read low on own hits, or dropped with a written argument; H of every sample is without the later arcs (21 % of the true crossings of the event's own particles for Z(νν)); the pile-up density is corrected in number by the top-up but not in its correlations |

What I would do for DIF-C and NI-C: **(a)**, validated on a slice before any B1 campaign file is written, and said
in the addendum as a hybrid that only these two classes have. It answers A-1 as the review posed it (the parent's
hits before the vertex), touches no frozen file and no other sample, and stays valid whichever chain-wide choice is
made: under (c) the injected crossings are simply no longer needed. I would not choose (b) (it discards a Fatras
parent that agrees with Geant4 to 99 % on its first half turn). No recommendation on (c) against (d).

## What this means for the Z(νν) pilot launch

The Z(νν) pilot as prepared is the v1 chain: self-consistent with C1 and with every existing v2 number, and without
the 204 crossings per event that particles below ≈ 0.63 GeV make after half a turn. Under (a), (b) or (d) it is
final as generated. Under (c) or (c′) it would be regenerated. `pilot.mb` is generator level and does not depend on
the choice.

## Corrected Geant4 reference with the transportation-ended tracks included (2026-11-16 18:13; appended by Albert, successor of Xavier)

The Geant4 reference of section b lacked the tracks that end by transportation only ("no record 1 %", see the 17:20
addendum of `LOOPER_GUN_xavier_2026-11-16_16-38.md`). Rerun of the comparison on the same chain events with the fixed
`g4hv.cc` (55b434a3…) [V: campaign `p2-c-pa-htg`, 2 jobs, 0.20 CPU-h; `data/p2c/pa_validation/p2-c-pa-htg/000/
p2-c-pa-htg-{znn,mb}.json` against `data/p2c/px_validation/p2-c-px-htg/000/`]. The Fatras side is unchanged (the same
chain files). **No statement of the note changes; the missing-crossing numbers rise by about 0.5 %.**

| per event (first value: as published above → corrected) | Z(νν), no pile-up | one minimum-bias interaction |
|---|---|---|
| Geant4 crossings of barrel counting surfaces | 958.3 → 965.4 | 311.6 → 314.4 |
| of which after half a turn | 204.1 (21.3 %) → 205.1 (21.2 %) | 88.8 (28.5 %) → 89.3 (28.4 %) |
| Geant4 crossings without a Fatras hit | 209.2 → 210.3 | 91.0 → 91.5 |
| the same relative to the written hits | 25.1 % → 25.2 % | 37.3 % → 37.5 % |
| Fatras hits without a Geant4 crossing | 39.7 → 33.6 | 13.8 → 11.5 |
| central particles with p_T < 0.63 GeV without a Geant4 record | 375 of 38,665 → 0 (now `Stopped`: 375) | 1,676 of 174,722 → 0 (`Stopped`: 1,676) |
| of those particles, alive after one full turn | 29,717 (76.9 %) → 30,071 (77.8 %) | 133,891 (76.6 %) → 135,512 (77.6 %) |

Missing crossings per layer and Z(νν) event, corrected: TBPX L1–L4 6.0 / 7.7 / 7.9 / 7.5; TBPS L1–L3 (inner sensor)
34.1 / 24.3 / 15.8; TB2S L1–L3 9.3 / 5.2 / 2.2 (were 6.0 / 7.7 / 7.9 / 7.5; 33.8 / 24.1 / 15.7; 9.2 / 5.2 / 2.1). The
recovered tracks also had crossings on the first half turn (crossings before a quarter turn 695.3 → 700.7 per Z(νν)
event), which is why the "Fatras hits without a Geant4 crossing" fall.
