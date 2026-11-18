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
- **Observation (RESOLVED in §6: chance, the pattern is absent in the full count):** all 8 flagged events are in the files 0001 and none in the files 0000 (4 streams
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

## 6. Pilot-wide count of flagged events, and the 0000 / 0001 pattern (added 11:02)
Campaign `p2-c-pilot-val-eph` (file `tools/runner/examples/p2x/b1_val/p2-c-pilot-val-eph.json`, script
`src/p2h_ephcount.py`, manifest `b1_val/p2-c-pilot-val-eph_files.json`), launched by the orchestrator on maxwell:
1 job done, 7.8 CPU-s, 47 MB RSS, 236 s wall. Output (all numbers of this section are VERIFIED from it)
`/nfs/cajuela/jdochoa/quirks_v2/data/p2c/pilot_validation/p2-c-pilot-val-eph/000/p2-c-pilot-val-eph-0.json`
(sha256 18b2955ace722223…). It read `meta` and `n_early_prod` of all 546 done chain files of the 8 streams: 546 read,
0 errors; in every file the array sums equal the sums stored in the meta and the array length equals the events
(`meta_consistent` true); β cut 0.1 in all.

**Total: 318 flagged events (524 hits) in 17,200,000 events = 1.85×10⁻⁵ per event.** B1_READY §2 expected "of order
10²" in 1.9×10⁷ [its estimate from 4 slice events]: the measured number is about three times that; my §4 estimate
from 8 events (≈ 3×10²) holds. The hs stream (2×10⁶ events, not produced yet) is not included.

| stream | files | events | flagged events | hits | rate per event | files with ≥ 1 | per-file counts vs Poisson, χ²/dof |
|---|---|---|---|---|---|---|---|
| dif | 111 | 4,000,000 | 0 | 0 | 0 (< 7.5×10⁻⁷ at 95 %) | 0 | — |
| difc | 121 | 4,000,000 | 0 | 0 | 0 (< 7.5×10⁻⁷ at 95 %) | 0 | — |
| nix | 123 | 4,000,000 | 212 | 351 | 5.3×10⁻⁵ | 100 | 136.4 / 122 |
| nic | 60 | 2,000,000 | 59 | 97 | 3.0×10⁻⁵ | 37 | 58.8 / 59 |
| ni22 | 49 | 1,000,000 | 10 | 16 | 1.0×10⁻⁵ | 10 | 38.5 / 48 |
| ni30 | 36 | 1,000,000 | 15 | 25 | 1.5×10⁻⁵ | 12 | 35.4 / 35 |
| ni61 | 37 | 1,000,000 | 18 | 28 | 1.8×10⁻⁵ | 14 | 38.2 / 36 |
| lowpt | 9 | 200,000 | 4 | 7 | 2.0×10⁻⁵ | 4 | 4.8 / 8 |
| **sum** | **546** | **17,200,000** | **318** | **524** | **1.85×10⁻⁵** | 177 | |

(The 95 % limit for zero observed is 3 / N. The χ² compares the count of each file with the stream's mean rate times
the file's events; small expectations per file make it approximate for the NI-layer streams.)
Hits per flagged event: 1 in 178 events, 2 in 99, 3 in 22, 4 in 14, 5 in 4, 6 in 1. Every flagged event has a
nuclear-interaction class (nix 212, nic 59, ni61 18, ni30 15, ni22 10; lowpt: 3 nic + 1 ni22): **none in 8×10⁶ decay
events**, as expected for a residue of slow protons and fragments. New against the slices: nic (59 events; the
slices saw none in the nic files; B1_READY §2) and the three NI-layer streams. NI-X: 5.3×10⁻⁵ against
3×10⁻⁵ from 2 slice events (compatible).

**The 0000 / 0001 pattern is not real.** Breakdown by chunk index (= job index of the stream):

| split | flagged events | events | reading |
|---|---|---|---|
| even chunk index / odd chunk index | 157 / 161 | 8,641,569 / 8,558,431 | binomial expectation 159.8 / 158.2: no difference (0.3 σ) |
| nix only, even / odd | 106 / 106 | 2,007,862 / 1,992,138 | none |
| first half / second half of a vertex file (`first_vertex` = 0 / > 0; nix) | 106 / 106 | same | none |
| chunk 0 / chunk 1 / chunk 2 / chunk 3 / chunks ≥ 4 | 0 / 8 / 3 / 3 / 304 | 234,659 each / 16,261,364 | expected 4.3 per chunk index from the stream rates |
| nix by node: schrodinger / maxwell | 116 / 96 | 2,090,112 / 1,909,888 | 5.6 / 5.0 ×10⁻⁵, 0.9 σ apart |

Simple test: with the stream rates of the table, the eight files 0000 expect 4.30 flagged events and the eight files
0001 expect 4.30. Observed 0 (Poisson probability 1.4 %) and 8 (probability of ≥ 8: 7 %); their sum, 8, against 8.6
expected is ordinary. Over all chunk indices the counts per file follow Poisson statistics in every stream (χ²/dof
in the table; nix 136.4 / 122, p ≈ 0.2 [E, normal approximation]), and even and odd indices agree. The zero in the files 0000 is a
fluctuation at the 1.4 % level in one of ≈ 120 chunk indices that could have been looked at; the validation happened
to pick it. **No dependence on the chunk index, on the half of the vertex file or on the node is seen**, so the code
was not searched for one and nothing is to be changed. (By construction the chunk enters only the job seed,
`C.qv2_seed(stream, chunk)` at `src/p2x_b1.py:190`, and the first vertex row used.)

Consequences. (i) The verdicts of §2 stand; the strict `hard` check fails in 177 of the 314 chain files of the six
streams with nuclear interactions (nix 100 of 123), so `hard_except_early_product_hits` is the only usable per-file
reading for them, as decided. (ii) The pilot holds 318 flagged events, each marked by `n_early_prod` > 0 in its
file; with hs about 3.5×10² are to be expected [E: 2×10⁶ × the low-p_T mixture rate 2×10⁻⁵ ≈ 40]. (iii) The number is
three times the "order 10²" on which the decision of 17 Nov was taken: the rate per event is the same order as
estimated then (1.85×10⁻⁵ against 4 / 4.3×10⁵ = 0.9×10⁻⁵), the decision's basis is not changed in kind, but the
orchestrator should see the measured value. FLAG FOR HUMAN: information only.
