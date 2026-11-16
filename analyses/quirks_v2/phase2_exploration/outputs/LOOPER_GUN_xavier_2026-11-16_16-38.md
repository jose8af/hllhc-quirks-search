# A proper looper gun through the frozen v1 finder — Xavier, 2026-11-16 16:38

Asked for by the orchestrator after `outputs/HALF_TURN_xavier_2026-11-16_16-08.md`. Campaigns [V] (markers
`ledger/markers/<campaign>/000/`, data `/nfs/cajuela/jdochoa/quirks_v2/data/p2c/px_validation/<campaign>/000/`):
`p2-c-px-lp0` (smoke, 2 × 200 events), **`p2-c-px-lp`** (40 jobs × 5,000 events: 10⁵ events per set), `p2-c-px-lps`
(summary, `p2-c-px-lps-0.json`), `p2-c-px-lpb` / `p2-c-px-lpbs` (the same events again, with per-layer counts). 0.60 CPU-h + 0.6 for the rerun. Validation slices (streams `px.looper.*`), not pilot data. Background only.

## Result

**No candidate at any rung in 2×10⁵ looper events (10⁵ per set).** Not one event has a candidate in v1's record
(N_L2 ≥ 4 after the refit), so R01–R07 and every deeper rung count 0 events and 0 candidates in both sets.
**The zero bounds little:** one count would stand for 1.9×10⁴ events in 3 ab⁻¹ (below), so the 68 % upper value of
the zero is 2.2×10⁴ events, against the scale of 300.

| funnel of the frozen finder (events) | natural spectrum | flat in p_T 0.1–0.63 GeV | which fixed cut |
|---|---|---|---|
| generated | 100,000 | 100,000 | |
| fewer than 3 hits in the finder's pool: no trial | 3,847 | 3,853 | — |
| finder run | 96,153 | 96,147 | |
| with at least one seed triple (TBPX L4–L3 pair in the road with an L2 hit in the seed plane) | 72,105 | 73,756 | road ± 0.15 and seed geometry |
| with a seed of score N_L2 ≥ T_seed = 4 (layers with ≥ 2 crossings in the seed band) | **33** | **34** | **the seed threshold** removes 99.95 % of what is left |
| with a candidate after the refit (N_L2 ≥ 4) | **0** | **0** | the plane refit (t_tol 30 µm, 3σ re-collection) |
| R01 (N_IP2 ≥ 4) … R07 (w < 9.4 mm), R08–R14 | 0 at every rung | 0 at every rung | |

Hits in the road per trial: median 6 (10–90 %: 4–8/9; 99 %: 18). No event has a candidate, so v1's record holds no
candidate variable for these events.

**Near-pass classes on the particle's own crossings** [V: rerun of the same events with the per-layer counts stored,
`p2-c-px-lpb` (40 jobs) and `p2-c-px-lpbs-0.json`, key `own_crossing_upper_bounds`; the rerun reproduces the funnel
above number for number]. A layer can be a double-crossing layer of some ribbon only if the particle crosses it at
least twice (pixel layers: crossings; stacked layers: min(inner, outer)); counted with **no plane, road or width
requirement**, this is an upper bound on every count a ribbon could reach:

| per 10⁵ events | natural | flat |
|---|---|---|
| ≥ 3 pixel layers crossed at least twice (the fixed cut N_IT2 ≥ 3 could be met) | 10,860 | 10,350 |
| … and ≥ 4 / 5 / 6 / 7 of the seven inner (pixel + PS) layers (R01 / R02 / R03 / R04 could be met) | 10,068 / 8,007 / 5,799 / 3,453 | 10,080 / 7,714 / 5,608 / 3,574 |
| deficit k_IP at R04 by multiplicity alone: 0 / 1 / 2 / 3 / ≥ 4 | 3,453 / 2,346 / 2,405 / 2,311 / 89,485 | 3,574 / 2,034 / 2,277 / 2,598 / 89,517 |
| at least one 2S layer crossed twice in both sensors | 19,585 | 22,942 |

So multiplicity is not what removes the loopers: 10 % of them cross enough layers twice for R01 and 3.5 % for R04.
What removes them is the plane: the crossings of successive turns do not lie in one plane through the PV within the
finder's seed band and refit tolerance (seed score ≥ 4 in 33–34 events of 10⁵, no candidate after the refit). The
subset classification of STR §4.4 point 4 (widest-holding ribbon of the rung's width through the PV) does not exist
as code yet; the numbers above are its upper bound, not its value.

## What was done, and how it differs from v1's looper gun

| | v1 looper gun (`s4cp.py` l.15; 0 of 10⁵ and 0 of 500) | this gun |
|---|---|---|
| particle | π± or e± (50/50), p_T uniform 0.05–0.7 GeV, \|η\| < 0.3 | species, p_T and η of a prompt charged particle of a minimum-bias interaction with \|η\| < 1 and p_T < 0.63 GeV (set "nat": 91 % π±, 7 % K±, 2 % p/p̄; median p_T 0.33 GeV); set "flat": the same with p_T uniform in 0.1–0.63 GeV |
| propagation | Fatras: **stops at half a turn**, no decay, no hadronic interaction | **Geant4** (FTFP_BERT, validated geometry, 3.8 T) until the particle decays, interacts, stops, leaves the tracker (r > 1.2 m, \|z\| > 2.7 m) or reaches **25 ns** |
| hits | Fatras hits of the first half turn | **every** Geant4 crossing of a sensitive surface injected as a SimHit through `run_chain.Inject` (the path of v1's stored C′₀ hits and of the quirk hits), then the chain's digitisation, seeding and CKF, unchanged |
| vertex, PV, road | luminous-region vertex (z offset ± 0.5 mm), PV smeared by (10, 10, 15) µm, φ_MET uniform, particle azimuth φ_MET ± 0.1 | the same draws (`s4cp.CPrime.event` l.110-116, l.127), without the z offset: **v1's road draw, one road per event, the one the particle starts in; not 21 orientations** |
| finder and ladder | `run_g1b.run_cp0_job`, frozen configuration | **the same function, unchanged**; only its `chain()` (the producer of the chain file) is replaced. Recorded configuration: road 0.15, W_c 75 mm, t_tol 0.03 mm, **T_seed 4**, 3 iterations [V: `finder_cfg` in every output] |
| attribution | looper rule: ≥ 2 crossings in a layer | the same rule (`looper=True`) |

The 25 ns is `TMAX` of `g4/g4hv.cc` (Tatiana; the bunch spacing). The chain applies no time window to tracker hits:
`finder/pu_inputs.py`, `finder/g1b_tt.py` and `finder/finder.py` contain none (grep); hit times are used only for
the BTL time tag.

What the particles do in Geant4 (set "nat"; "flat" agrees within 0.02): 87 % are alive after half a turn and 76 %
after one turn; the track ends after a median of 1.9 turns (90 %: 4.6); by decay 28 %, inelastic interaction 14 %,
stopped or captured 3 %, left the tracker 33 %, still circulating at 25 ns 21 %, no Geant4 record 1 % (985 events
without a single injected hit: counted in the 10⁵, so the sample is effectively 1 % smaller). Per event 18.1
crossings of barrel counting surfaces, **9.1 of them after half a turn** (67 % of the events have at least one);
all 22.0 sensitive-surface crossings per event were injected and digitised (V4-1 closure passes in 39 of 40 jobs;
in `p2-c-px-lp-nat-008` one injected SimHit of 1.1×10⁵ has no measurement, the known loss of ACTS's bounded
smearing, `run_chain.py` l.141-143).

## What a zero does and does not bound

Prompt charged particles with |η| < 1 and p_T < 0.63 GeV: **7.30 per minimum-bias interaction** [V: 145,991 in the
20,000 interactions of p2-c-px-ht-mb]. The gun starts the particle within ± 0.1 of the road axis: a fraction
0.2/2π = 0.0318, i.e. 46.5 such loopers per triggered event at 200 interactions, N_t = N_trig × 200 × 7.30 × 0.0318
= **1.9×10⁹ in 3 ab⁻¹** (N_trig = 4.0848×10⁷, STR l.200) [E]. With M = 10⁵: **one count = 1.9×10⁴ events; a zero
allows 2.2×10⁴ events at 68 %.** For a zero to allow 25 events one needs M ≈ 9×10⁷ gun events (≈ 270 CPU-h at the
measured 11 ms per event) [E]. So this gun shows that single loopers do not readily make candidates (seed score
≥ 4 in 3.4×10⁻⁴ of the events, none surviving the plane refit); it does not bound them at the scale the study needs.
Not covered at all: loopers starting outside ± 0.1 of the road (the other 97 % of them, whose later arcs can enter
the road), loopers with |η| > 1, displaced ones, several loopers or a looper plus other particles in one event (with
pile-up that is the pile-up term, where these arcs are now known to be missing from the Fatras hits), products of
the looper's decay or interaction (not followed), and the dE/dx rungs (injected hits carry no energy deposit).

## Arc times

Crossings after half a turn (set "nat"; quantiles 10 / 50 / 90 / 99 %): the first such crossing at 2.7 / 4.6 / 7.1 /
11.8 ns after the collision, the median one of an event at 3.9 / 6.9 / 13.0 / 15.8 ns; the last crossing of an event
at 1.3 / 6.4 / 19.8 / 24.9 ns. A window of 25 ns keeps all of them by construction, so **a hit-time window of one
bunch crossing removes none of the late arcs**. They are 1–20 ns later than a prompt particle at the same radius
(a prompt track reaches r = 1.1 m in 3.7 ns), so a per-hit time measurement at the 0.1 ns level would separate
them; the chain has no per-hit tracker time, and the BTL time tag sees a looper only if it reaches the BTL.

## Addendum 17:20: the two loose ends [V: p2-c-px-lpc (rerun of job nat-008 with records kept), p2-c-px-pv1 not involved]

1. **The V4-1 flag of `p2-c-px-lp-nat-008`.** One injected SimHit of about 1.1×10⁵ in that job has no measurement: event 4,793, a
   crossing of the endcap surface `TEDD_D2_p_2S_in` at r = 663.4 mm, 6.5 mm inside the inner edge of that disc
   (r = 656.9–1,074.4 mm, `surfaces_s3.json`). This is the loss that `run_chain.py` l.141-143 documents for Fatras hits
   ("ACTS's bounded smearing fails minMaxRetries = 10 times at a surface/sector bound"; 3 of 3.0×10⁶ there): the
   digitisation redraws a smeared position until it is inside the surface and gives up after ten tries; a 2S hit
   close to an edge in its coarse coordinate can fail. My flag used v1's strict form (injected SimHits = injected
   measurements), hence "false". It is not a barrel counting surface, so the finder input is unaffected. **Can it
   happen in option (a) production? Yes, at the same rate as for any hit (order 10⁻⁶ per SimHit near an edge);** the
   B1 job's closure (`p2x_b1.py`) uses v1's tolerance for lost SimHits (≤ max(2, 10⁻⁵ of the hits) per event), counts
   them in `meta['n_lost_simhits']`, and does not fail on one.
2. **The 1 % without a Geant4 record.** They are not stopped protons: in job nat-008, 44 of 5,000, all π± (39) and
   K± (5), p_T 0.16–0.59 GeV. Their track ended with no process other than transportation, for which the first
   version of the `allx` option wrote no record, so the event had no hits at all. With the record added (`g4hv.cc`
   55b434a3…, label `Stopped`), these particles have on average 13.2 counting-surface crossings and up to 5 crossings
   of one layer: they are multi-turn loopers, presumably ended by Geant4's own killing of looping tracks in the
   field [U: not read from a Geant4 message]. **So the first two runs were missing 0.9 % of the events, and those were
   among the most looping ones: a bias against candidates, small in number.** The rerun of this job with them
   included still has no seed above threshold and no candidate (4,853 trials). The whole gun is being rerun with the
   fixed record on one lane (`p2-c-px-lpd`, summary `p2-c-px-lpds/000/p2-c-px-lpds-0.json`); until it is read, the
   table above stands for 99.1 % of the sample. Even with the record these tracks end where Geant4 stops them, before
   25 ns. The same 1 % ("no record") is in the Geant4 reference of `HALF_TURN_xavier_2026-11-16_16-08.md`: its
   missing-crossing numbers are low by at most that share of the particles.

## Rerun with the transportation-ended tracks included (2026-11-16 17:58; appended by Albert, successor of Xavier)

Campaigns [V]: `p2-c-px-lpd` (40 jobs × 5,000 events, 40 of 40 done, 0.55 CPU-h; the same events, seeds and finder
configuration as `p2-c-px-lp`, with `g4hv.cc` 55b434a3…, which records a track that ends by transportation only),
summary `p2-c-px-lpds` (read: `data/p2c/px_validation/p2-c-px-lpds/000/p2-c-px-lpds-0.json`; first run:
`…/p2-c-px-lpbs/000/p2-c-px-lpbs-0.json`). Validation slices, not pilot data. Background only.

**Result: still no seed-threshold event beyond the first run's, and no candidate at any rung.** Not one of the
2×10⁵ events has a candidate in v1's record; R01–R14 count 0 events and 0 candidates in both sets
(`events_passing_rung`, `candidates_passing_rung`, `trials_passing_R04_or_deeper` all zero or empty). The number of
events with a seed of score ≥ T_seed = 4 is unchanged (33 and 34): **none of the recovered events has a seed above
threshold.** Nothing to report in hits per layer, width, thickness or time spread: no candidate exists.

| funnel of the frozen finder (events) | natural: first run → rerun | flat: first run → rerun |
|---|---|---|
| generated | 100,000 → 100,000 | 100,000 → 100,000 |
| fewer than 3 hits in the finder's pool: no trial | 3,847 → 2,863 | 3,853 → 2,851 |
| finder run | 96,153 → 97,137 | 96,147 → 97,149 |
| with at least one seed triple | 72,105 → 72,773 | 73,756 → 74,446 |
| with a seed of score N_L2 ≥ T_seed = 4 | 33 → **33** | 34 → **34** |
| with a candidate after the refit (N_L2 ≥ 4) | 0 → **0** | 0 → **0** |
| R01 … R14 | 0 → 0 at every rung | 0 → 0 at every rung |

**Events recovered: 985 (natural) and 1,003 (flat)**, 0.99 % and 1.00 % of the sample: the tracks whose end process was
"none" in the first run are now recorded as `Stopped` (985 / 1,003 in `particles.end_process`), with all their
crossings injected. Of them, 984 and 1,002 give a finder trial; 668 and 690 more events have a seed triple; none
reaches the seed threshold. Every other end-process count is identical to the first run (decay 28,310, left 32,613,
at 25 ns 21,103, … in the natural set): the other 99 % of the events are the same events.

Particle and crossing numbers with the recovered tracks (natural; flat within 0.01): alive after half a turn 87.9 %
(was 86.9 %), after one turn 76.5 % (75.5 %); 18.20 crossings of barrel counting surfaces per event (18.06), 9.19 of
them after half a turn (9.14), in 67.3 % of the events (66.6 %). Own-crossing upper bounds (no plane, road or width
requirement): ≥ 3 pixel layers crossed at least twice 10,862 / 10,350 per 10⁵ (10,860 / 10,350); and ≥ 7 inner layers
(R04 could be met) 3,453 / 3,574 (unchanged); at least one 2S layer crossed twice in both sensors 19,741 / 23,107
(19,585 / 22,942). So the recovered tracks add crossings mainly in the outer layers and none to the inner-layer
classes that the ladder needs.

V4-1 closure: passes in 39 of 40 jobs; `p2-c-px-lpd-nat-008` again reads false (the one endcap SimHit near a disc
edge of the 17:20 addendum, same event sample). The bound is unchanged: one count = 1.9×10⁴ events in 3 ab⁻¹, a zero
allows 2.2×10⁴ events at 68 %. **The zero now stands for the whole sample of 2×10⁵ events (it stood for 99.0 %); what
it does and does not bound is as written above.**
