# A-1 re-validation: truncation of the Fatras parent at the Geant4 vertex — Xavier, 2026-11-16 15:40

For: strategy addendum 1 v3, §2 P6 ("A-1 re-validation: pending"). Campaigns (all VERIFIED = run by me, markers
`ledger/markers/<campaign>/000/`, data `/nfs/cajuela/jdochoa/quirks_v2/data/p2c/px_validation/<campaign>/000/`):
`p2-c-px-tr` (27 jobs: 9 streams × cut by radius / time / both; 2,000 events each, the same vertices and seeds in the
three cuts; vertex files of `p2-c-px-g4`), `p2-c-px-val2` (validation, `p2x_validate.py`), `p2-c-px-a1d` and
`p2-c-px-a1e` (diagnostics `p2x_diag_a1.py`, `p2x_diag_turns.py`). Validation slices, not pilot data.

## Result in three lines

1. **The time cut does not repair DIF-C and NI-C.** With it, 40 % (DIF-C) and 45 % (NI-C) of the Geant4 parent's
   crossings of a counting surface before the vertex still have no Fatras parent hit (59 % and 67 % with v1's radius
   cut). The ≤ 2 % check **fails for both streams under every cut**.
2. **Cause, measured: in this chain Fatras leaves no hit beyond half a turn of a particle.** The Fatras parent's last
   hit is at ≤ 0.50 turn in every stream (transverse path / 2πR), while the Geant4 parent of these classes reaches its
   vertex at a median of 1.0 turn (99 %: 2.4–2.5). Inside the first half turn the time cut matches Geant4 to
   99.9 % / 98–99 %. No truncation rule can supply hits that Fatras never makes.
3. **It is not specific to the hand-over.** In 5,000 no-pile-up Z(νν) slice events, of 3.94×10⁶ hits of generated
   charged particles, 231 (0.006 %) are beyond 0.5 turn, behind a sharp edge at 0.5 [V: p2-c-px-a1e]. Every sample
   of the chain (v1's and v2's: same code, no loop setting in `run_chain.py`) lacks the later arcs of curling
   particles. Mechanism not read in the ACTS source [U: presumably the propagator's loop protection at half a turn].

## Table [V: p2-c-px-val2-0.json]

"G4 crossings": crossings of a barrel counting surface by the Geant4 parent before its vertex, all events with a
charged parent, counted with multiplicity (a parent that crosses a layer twice counts twice). "Reviewer count": the
measure of the second review (`p2c_validate`: first 100 events, a surface counts once): it does not see the missing
return arcs, because they cross the same surfaces as the outward arc. "≤ 2 %" is on the first measure.

| stream | cut | events with charged parent | G4 crossings matched | G4 crossings without Fatras hit (fraction) | Fatras parent hits without G4 crossing | parent hits later than vertex time | parent hits beyond vertex radius | reviewer count, first 100 ev: only G4 / both | <= 2 % | other hard checks |
|---|---|---|---|---|---|---|---|---|---|---|
| dif | radius | 1895 | 18715 | 20 (0.11 %) | 9 (0.05 %) | 19 of 18792 | 0 | 0 / 994 | PASS | pass |
| dif | time | 1895 | 18688 | 47 (0.25 %) | 33 (0.18 %) | 0 of 18792 | 27 | 0 / 994 | PASS | FAIL |
| dif | both | 1895 | 18688 | 47 (0.25 %) | 9 (0.05 %) | 0 of 18765 | 0 | 0 / 994 | PASS | pass |
| difc | radius | 2000 | 20356 | 28692 (58.50 %) | 1 (0.00 %) | 0 of 20409 | 0 | 435 / 1035 | FAIL | pass |
| difc | time | 2000 | 29246 | 19802 (40.37 %) | 51 (0.17 %) | 0 of 29803 | 9394 | 20 / 1450 | FAIL | FAIL |
| difc | both | 2000 | 20356 | 28692 (58.50 %) | 1 (0.00 %) | 0 of 20409 | 0 | 435 / 1035 | FAIL | pass |
| ni22 | radius | 1740 | 0 | 0 (0.00 %) | 0 (0.00 %) | 0 of 0 | 0 | 0 / 0 | PASS | pass |
| ni22 | time | 1740 | 0 | 0 (0.00 %) | 0 (0.00 %) | 0 of 0 | 0 | 0 / 0 | PASS | pass |
| ni22 | both | 1740 | 0 | 0 (0.00 %) | 0 (0.00 %) | 0 of 0 | 0 | 0 / 0 | PASS | pass |
| ni30 | radius | 1768 | 893 | 0 (0.00 %) | 0 (0.00 %) | 0 of 893 | 0 | 0 / 53 | PASS | pass |
| ni30 | time | 1768 | 889 | 4 (0.45 %) | 3 (0.34 %) | 0 of 892 | 3 | 0 / 53 | PASS | FAIL |
| ni30 | both | 1768 | 889 | 4 (0.45 %) | 0 (0.00 %) | 0 of 889 | 0 | 0 / 53 | PASS | pass |
| ni61 | radius | 1740 | 2627 | 0 (0.00 %) | 0 (0.00 %) | 0 of 2627 | 0 | 0 / 154 | PASS | pass |
| ni61 | time | 1740 | 2598 | 29 (1.10 %) | 31 (1.18 %) | 0 of 2629 | 31 | 1 / 153 | PASS | FAIL |
| ni61 | both | 1740 | 2598 | 29 (1.10 %) | 0 (0.00 %) | 0 of 2598 | 0 | 1 / 153 | PASS | pass |
| nix | radius | 1786 | 15353 | 15 (0.10 %) | 3 (0.02 %) | 208 of 15356 | 0 | 1 / 884 | PASS | pass |
| nix | time | 1786 | 14862 | 506 (3.29 %) | 350 (2.30 %) | 0 of 15212 | 347 | 21 / 864 | FAIL | FAIL |
| nix | both | 1786 | 14862 | 506 (3.29 %) | 3 (0.02 %) | 0 of 14865 | 0 | 21 / 864 | FAIL | pass |
| nic | radius | 2000 | 17796 | 35335 (66.51 %) | 2 (0.01 %) | 0 of 17798 | 0 | 498 / 977 | FAIL | pass |
| nic | time | 2000 | 29110 | 24021 (45.21 %) | 31 (0.11 %) | 0 of 29553 | 11754 | 16 / 1459 | FAIL | FAIL |
| nic | both | 2000 | 17796 | 35335 (66.51 %) | 2 (0.01 %) | 0 of 17798 | 0 | 498 / 977 | FAIL | pass |
| hs | radius | 1883 | 16791 | 10253 (37.91 %) | 6 (0.04 %) | 51 of 16830 | 0 | 210 / 847 | FAIL | pass |
| hs | time | 1883 | 20056 | 6988 (25.84 %) | 124 (0.61 %) | 0 of 20338 | 3624 | 12 / 1045 | FAIL | FAIL |
| hs | both | 1883 | 16676 | 10368 (38.34 %) | 6 (0.04 %) | 0 of 16714 | 0 | 216 / 841 | FAIL | pass |
| lowpt | radius | 1967 | 13756 | 20790 (60.18 %) | 2 (0.01 %) | 62 of 13758 | 0 | 290 / 684 | FAIL | pass |
| lowpt | time | 1967 | 18236 | 16310 (47.21 %) | 103 (0.56 %) | 0 of 18339 | 4662 | 2 / 972 | FAIL | FAIL |
| lowpt | both | 1967 | 13674 | 20872 (60.42 %) | 2 (0.01 %) | 0 of 13676 | 0 | 290 / 684 | FAIL | pass |

"Other hard checks" FAIL in the time rows is only the check "no parent hit beyond the vertex radius", which is not
applicable to a time cut (for a parent that has turned, earlier hits at larger radius are correct). Every other hard
check passes in all 27 files (V4-1 closure, no NaN, offsets, distinct seeds, no product hit before its production
time, one class per event equal to the class recomputed from the stored vertex, parent inside its phase space, no
product with β < 0.1 handed over, stored content hash = recomputed). `hs` and `lowpt` are the mixed slices (all eight
classes; parents of the old-style slice pools).

Where the hits are missing [V: p2-c-px-a1d-0.json], crossings / hits by turn of the parent, time cut:

| stream | 0–0.25 turn: Geant4 / Fatras | 0.25–0.5 | 0.5–0.75 | 0.75–1 | 1–1.5 | 1.5–2 | 2–3 | last Fatras hit, turn (median; max) | vertex, turn (median; 99 %) |
|---|---|---|---|---|---|---|---|---|---|
| DIF-C | 23,380 / 23,353 | 5,999 / 5,944 | 4,360 / 0 | 7,674 / 0 | 5,705 / 0 | 1,544 / 0 | 386 / 0 | 0.35; 0.50 | 1.04; 2.53 |
| NI-C | 23,032 / 22,993 | 6,275 / 6,148 | 5,172 / 0 | 9,290 / 0 | 6,368 / 0 | 2,443 / 0 | 551 / 0 | 0.36; 0.49 | 0.99; 2.36 |
| DIF (radius cut) | 17,630 / 17,625 | 1,105 / 1,099 | 0 / 0 | | | | | 0.14; 0.48 | 0.17; 0.49 |
| NI-X (radius cut) | 14,787 / 14,781 | 581 / 575 | 0 / 0 | | | | | 0.09; 0.48 | 0.10; 0.47 |

## Which truncation, on this evidence

- **First-arc streams (DIF, NI 22 / 30 / 61.5 mm, NI-X): keep v1's radius cut.** Geant4 crossings without a Fatras hit:
  0.00–0.11 % (radius) against 0.25–3.29 % (time; NI-X 3.29 % fails the 2 % check, because the Fatras parent often
  reaches the last surface a few picoseconds after the Geant4 vertex time). What the radius cut leaves: parent hits
  later than the vertex time, 19 of 18,792 (DIF) and 208 of 15,356 (NI-X, 1.4 %); they are extra hits (strict side
  for a ceiling on own hits). "Both" removes them at the price of the time cut's losses; not recommended.
- **Streams after a turn (DIF-C, NI-C, and such events in the mixed samples): no cut passes.** The time cut is the
  better of the two (it restores the first half turn: 58.5 → 40.4 % and 66.5 → 45.2 % missing), but 40–45 % of the
  pre-vertex crossings stay without a hit. As simulated, these two classes would be read low on own hits; the
  statement of addendum v3 P6 "truncated by time" does not make them valid.
- Options for the two classes (none implemented or validated): (a) hybrid parent: Fatras up to half a turn, and the
  stored Geant4 crossings beyond it injected as SimHits through the chain's existing `Inject` algorithm (the second
  variant of STR l.744-746, restricted to what Fatras cannot do); (b) the same for the whole parent (pure second
  variant); (c) a chain-wide change of the Fatras loop limit, which changes every sample including the C1
  reproduction of v1; (d) the classes stay terms that the chain cannot simulate, said as a limitation. In (a), (b)
  and (d) the **products** of any vertex, and all particles of the SM and pile-up samples, still lose their arcs
  beyond half a turn.

## Phase 1 assumed / Phase 2 found / implications

Phase 1 assumed that the chain propagates curling particles (v1 had a "looper" gun topology, STR §4.4 scope; the
hand-over was to give "the parent's hits up to the vertex"). Phase 2 found that no particle leaves a hit beyond half
a turn in this chain. Implications: (1) A-1 is not closed by truncation; DIF-C and NI-C (1.5×10⁸ of the 3.7×10⁸
vertices) need option (a)–(d). (2) Own-hit ceilings H of every sample are counted without the later arcs of soft
particles; whether those arcs can make candidates is the same open question as for the after-turn classes. (3) This
holds for the Z(νν) pilot as well; it is the v1 chain's behaviour, so the pilot is self-consistent with C1, but a
decision for (c) would mean regenerating it. **For that reason I have not launched `pilot.mb` / Z(νν) on the earlier
go and ask for it to be confirmed with this known.** (`pilot.mb` is generator level and is not affected.)
