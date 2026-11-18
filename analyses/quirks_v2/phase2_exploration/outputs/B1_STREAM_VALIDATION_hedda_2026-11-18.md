# B1 pilot (p2-c-pilot_b1): one validated job per stream (addendum P7) — executor Hedda, 2026-11-18

**Verdict: 8 of 8 streams pass under the agreed reading `hard_except_early_product_hits` (16 of 16 files). Under the
strict hard check 4 files fail, in 4 streams (nix, ni30, ni61, lowpt), each on the one known check "no product hit
before its own production time": 8 flagged events and 18 hits in 469,318 events. pilot.c0.hs is not yet produced and
not validated.** Every number below is VERIFIED from the files named, unless tagged [E].

Reading rule: decision of 17 Nov 08:15 (B1_READY_albert §2 option (a), §9 end): β cut stays 0.1, flagged events are
counted and reported. No signal sample is involved. Nothing of the pilot was written or changed; the validator
(`src/p2x_validate.py`, sha256 in the PLAN) was run as it is.

## 1. What was run
Campaign `p2-c-pilot-val-s1` (file `tools/runner/examples/p2x/b1_val/p2-c-pilot-val-s1.json`, sha256 7e7d7081fe94…),
launched by the orchestrator on maxwell, one job at a time, 8 of 8 jobs `done` (exit 0). One job per stream:
`p2x_validate.py <out> outputs/partition_p2-c-part-0.json <chain files 0000 and 0001 of the stream's first chain
campaign>`. Outputs `D/p2-c-pilot-val-s1-<s>.json` with
`D = /nfs/cajuela/jdochoa/quirks_v2/data/p2c/pilot_validation/p2-c-pilot-val-s1/000`; markers
`M/p2-c-pilot-val-s1-<s>.marker` with `M = analyses/quirks_v2/ledger/markers/p2-c-pilot-val-s1/000`.
Cost (markers): **90.2 CPU-s = 0.025 CPU-h** (estimate before launch: 88.5 CPU-s), max RSS 246–549 MB (estimate
≤ ≈ 580 MB), wall 18–46 s per job.

## 2. Verdict per stream
Columns: events = sum of the two files; "early hits" = `product_hits_earlier_than_own_production` (hits) in
`events_with_product_hits_earlier_than_own_production` (events), file 0000 + file 0001; A1 = Geant4 pre-vertex
crossings of the parent without a Fatras hit, `a1_frac_g4_without_fatras` (criterion ≤ 2 %), the two files.

| stream `pilot.c0.<s>` | hand-over | events | `hard` (0000, 0001) | `hard_except_early_product_hits` | early hits: hits / events | A1, % | output sha256 (first 16); CPU-s; RSS MB |
|---|---|---|---|---|---|---|---|
| dif (dif + k0l) | radius | 72,638 | pass, pass | **pass, pass** | 0 / 0 | 0.103, 0.098 | 4de942571218e866; 12.1; 297 |
| difc | hybrid | 66,530 | pass, pass | **pass, pass** | 0 / 0 | 0.060, 0.058 | 683dcd3f90c98f95; 14.7; 475 |
| nix | radius | 65,316 | pass, **FAIL** | **pass, pass** | 0 + 13 / 0 + 5 | 0.149, 0.165 | 8629788a59f302a4; 11.4; 331 |
| nic | hybrid | 67,356 | pass, pass | **pass, pass** | 0 / 0 | 0.040, 0.044 | 6c0b2be02f29a92c; 16.7; 549 |
| ni22 | radius | 41,220 | pass, pass | **pass, pass** | 0 / 0 | 0 (no crossing), 0 | 8ce2486c4116153e; 6.9; 246 |
| ni30 | radius | 55,586 | pass, **FAIL** | **pass, pass** | 0 + 1 / 0 + 1 | 0.000, 0.000 | ed28099e35841fed; 9.7; 316 |
| ni61 | radius | 55,354 | pass, **FAIL** | **pass, pass** | 0 + 2 / 0 + 1 | 0.000, 0.003 | cc7ac64f537e6094; 9.8; 297 |
| lowpt (alarm sample) | autoh | 45,318 | pass, **FAIL** | **pass, pass** | 0 + 2 / 0 + 1 | 0.113, 0.114 | 1a184131e242df49; 8.9; 291 |
| **sum** | | **469,318** | 12 pass, 4 fail | **16 pass** | **18 hits / 8 events** | | 90.2; max 549 |

## 3. Hard checks (the same in all 16 files unless said)
True in 16 of 16 files: stored content hash = recomputed (`content_hash_recomputed_equal`), V4-1 closure
(`v41_pass`), offsets (`offsets_ok`), distinct event seeds (`seeds_distinct`), parent truncation
(`parent_truncation_ok`: 0 parent hits beyond the vertex radius in radius-cut events, 0 parent hits later than the
vertex time in hybrid events, `ev_mode_consistent`), class recomputed from the stored vertex = stored class
(`class_recomputed_equal`), class inside the sample's list (`class_in_sample`), first-arc flag (`first_arc_equal`),
parent inside the phase space of its vertex file (`parent_in_phase_space`; lowpt: 0.3–0.5 GeV window), road offset
< 0.15 (`road_offset_ok`), every hit owned by the gun vertex (`hits_all_gun`), vertex-file provenance (`provenance`),
A1 ≤ 2 % (`a1_ok`). Zero in 16 of 16 files: `nan_hits`, `evt_nan`, `product_hits_without_input_row`,
`mean_injected_slow` (no product with β < 0.1 handed over). `beta_min` = 0.1 and the planned hand-over in every file.
The only failing item is `product_hits_earlier_than_own_production` > 0 in the four files 0001 of §2.

Per-job summaries: `all_hard_checks_pass` true for dif, difc, nic, ni22; false for nix, ni30, ni61, lowpt (one file
each in `files_failing`). **Another chunk gives another content hash: true in 8 of 8 streams** (2 jobs, 2 hashes;
`all_different_seeds_differ`), the first time this check runs on production files. No rerun pair exists in the
pilot, so `all_reruns_identical` has nothing to compare (it reads false for that reason; not a failure).

Information, not criteria: events per class and mode as planned (dif 34,418 + 1,901 k0l in file 0000; difc and nic
all in mode 3; lowpt a mixture of 8 classes, 15,212 hybrid + 7,027 radius + 420 neutral); parent hits without a
Geant4 crossing (`a1_frac_fatras_without_g4`): difc 1.60 %, nic 1.54–1.57 %, lowpt 2.08 % (seam duplicates, as in
the slices: 1.58 / 1.58 / 2.08 %), ≤ 0.04 % elsewhere; `product_hits_earlier_than_vertex` (old form): nix 4 and 17,
ni30 0 and 1, ni61 0 and 2, lowpt 0 and 2, others 0.

## 4. The flagged events (slow-fragment residue)
- Rate here: 8 events in 469,318 = 1.7×10⁻⁵ per event; NI-X 5 in 65,316 = 7.7×10⁻⁵ (slices: 2 in 6.7×10⁴ = 3×10⁻⁵;
  the two agree within their Poisson errors). Scaled to the pilot's 1.92×10⁷ events: of order 3×10² flagged events
  [E, from 8 events, stream mixture not weighted], against "of order 10²" in B1_READY §2 [E from 4].
- **New with respect to the slices:** flagged events also in ni30 (1), ni61 (1) and lowpt (1); the slices had seen
  them only in nix and offroad. One event each: no rate can be quoted per stream.
- **Observation, not explained:** all 8 flagged events are in the files 0001 and none in the files 0000 (4 streams
  of 4). If the events were spread evenly, 8 of 8 on one side has probability 2 × 2⁻⁸ = 0.8 %; counting streams
  instead of events (the 5 NI-X events may not be independent of each other within a job), 4 of 4 has 12.5 %. I did
  not open the event files (nothing heavy on einstein; no slot was assigned to me for more than the validation).
  The files carry `n_early_prod` per event and its sum in their meta, so the count over all 546 class and low-p_T
  chain files needs no validation pass: one light job on a worker that reads only that array of each file.
  This would give the pilot-wide number that the decision of 17 Nov asks to report, and settle whether the 0000 / 0001
  pattern is chance. Not done: it needs a slot and the orchestrator's word.

## 5. Not covered, and what is prepared
- **pilot.c0.hs** (and its inputs pilot.c0.hs.pool, pilot.g4 chunks 2000–2010): campaigns hph, g4h, c0-hs pending at
  10:45 (the lanes wait for the Z(νν) pilot). Prepared, not launched:
  `tools/runner/examples/p2x/b1_val/p2-c-pilot-val-s2.json` (sha256 2836666e2cae…), 3 jobs: `-hs` (chain files
  0000, 0001 of p2-c-pilot-c0-hs), `-hspool` (pool files 000, 001 of p2-c-pilot-hph, validator mode hspool-x),
  `-g4h` (vertex files 0000, 0001 of p2-c-pilot-g4h). Its `after` lists the campaign file of p2-c-pilot-c0-hs: the
  queue starts it only when all 77 jobs of c0-hs are done. ≈ 30 CPU-s, ≤ ≈ 0.6 GB per job [E from the s1 markers
  and p2-c-pa-val1-g4: 26 CPU-s, 420 MB for 982 MB of vertex files].
- **Vertex files of the class block (pilot.g4 'all', 'ni', low-p_T passes) were not validated as files.** The chain
  validation covers their content only through the events built from them (class recomputed from the stored vertex
  row, provenance hash). The yield-per-firing check against the partition file (`g4prod` mode) has not been run on
  pilot files. It would be one more job of ≈ 30 CPU-s on, e.g., g4a-0000 (4 groups), g4n-0000 (3 groups), g4l-0000.
- One job (two files) per stream is validated, as P7 asks; the other 530 chain files of these streams are not.
