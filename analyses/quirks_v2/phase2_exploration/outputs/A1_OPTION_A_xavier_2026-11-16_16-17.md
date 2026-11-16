# Option (a) for DIF-C / NI-C: Fatras parent to half a turn + Geant4 crossings beyond it — Xavier, 2026-11-16 16:17

Follows `outputs/A1_TRUNCATION_xavier_2026-11-16_15-40.md` and `outputs/HALF_TURN_xavier_2026-11-16_16-08.md`.
Campaigns [V] (markers `ledger/markers/<campaign>/000/`, data
`/nfs/cajuela/jdochoa/quirks_v2/data/p2c/px_validation/<campaign>/000/`): `p2-c-px-hy` (8 jobs, 2,000 events each, the same
vertices and seeds as `p2-c-px-tr`), `p2-c-px-val3` (`p2x_validate.py`). Validation slices, not pilot data.

## What was implemented (`src/p2x_b1.py`, class `HybridParent`; modes `hybrid`, `autoh`)

For an event of a class after a turn: the Fatras parent is kept up to the Geant4 vertex time (Fatras stops it at
half a turn anyway); the stored Geant4 crossings of the parent before the vertex that are later than its last kept
Fatras hit by more than 0.005 ns (1.5 mm of flight; fixed before the run, not tuned) are added as SimHits with the
parent's barcode, at the Geant4 position, time and momentum, and go through the chain's digitisation, seeding and
CKF like every other hit (the mechanism of `run_chain.Inject`). `autoh` applies this to the classes difc and nic and
v1's radius cut to the first-arc classes (mixed samples). No file of the v1 chain is changed.

## Result [V: p2-c-px-val3-0.json]

Geant4 crossings of a barrel counting surface by the parent before its vertex against written parent hits, all
events with a charged parent, with multiplicity (my measure, not the once-per-surface one).

| stream | cut | matched | Geant4 crossings without a hit | hits without a Geant4 crossing | ≤ 2 % check | before: radius cut / time cut (p2-c-px-tr) |
|---|---|---|---|---|---|---|
| DIF-C | hybrid | 49,030 | 18 (0.04 %) | 785 (1.58 %) | **PASS** | 58.5 % / 40.4 % |
| NI-C | hybrid | 53,106 | 25 (0.05 %) | 828 (1.54 %) | **PASS** | 66.5 % / 45.2 % |
| hs (mixed, slice pool) | autoh | 27,014 | 30 (0.11 %) | 297 (1.09 %) | PASS | 37.9 % / 25.8 % |
| lowpt (mixed, slice pool) | autoh | 34,505 | 41 (0.12 %) | 694 (1.97 %) | PASS | 60.2 % / 47.2 % |
| DIF | autoh (= radius) | 18,715 | 20 (0.11 %) | 9 (0.05 %) | PASS | 0.11 % (identical to the radius row) |
| NI-X | autoh (= radius) | 15,353 | 15 (0.10 %) | 3 (0.02 %) | PASS | 0.10 % (identical) |

- V4-1 closure passes in all 8 files; no NaN; offsets and seeds in order; no product hit before its production time;
  no product with β < 0.1 handed over; class of every event equal to the class recomputed from its stored vertex;
  stored content hash = recomputed.
- Reproducibility: difc -r0 = -r1 and nic -r0 = -r1 (identical content hash).
- Parent hits added from Geant4: 12.6 per DIF-C event and 14.0 per NI-C event; written hits per event 27.8 and 31.7.
  CPU per job unchanged within the start-up (12–15 CPU-s for 2,000 events).
- The 1.5 % "hits without a Geant4 crossing" are duplicates at the seam: the last Fatras hits and the first injected
  Geant4 crossings of the same passage when the two codes differ in arrival time by more than the 0.005 ns window.
  They are extra parent hits (strict side for a ceiling on own hits). I did not tune the window to shrink them.
- The validation's old check "no parent hit beyond the vertex radius" does not apply to a parent that has turned
  (19,643 and 25,945 such hits are the correct earlier arcs) and is why `all_hard_checks_pass` reads false for
  these files; every other hard check passes.

## What this does not change

**Products of the vertex, and every other particle of every sample, still stop at half a turn** (Fatras). Only the
parent of a DIF-C / NI-C event gets its later arcs, from Geant4, with Geant4's scattering and energy loss rather than
Fatras's. The first half turn of the parent stays the Fatras one (it agrees with Geant4 to 99–99.9 %). The mixed
slices above use the old slice pools (repeated parents), not the pools addendum v3 defines.
