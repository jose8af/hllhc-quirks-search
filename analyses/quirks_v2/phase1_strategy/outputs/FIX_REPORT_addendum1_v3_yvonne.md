# Fix report — strategy addendum 1, version 2 → version 3 (fixer: Yvonne, 2026-11-16)

Review fixed: `review/critical/ADDENDUM_1_v2_CRITICAL_REVIEW_wanda_2026-11-16_14-37.md` (ITERATE; 2 A, 5 B, 12 C), and the
items the first review (`ADDENDUM_1_CRITICAL_REVIEW_ulrich_2026-11-16_13-51.md`) left PARTIALLY resolved.
Result: `STRATEGY_ADDENDUM_1_v3_yvonne_2026-11-16_15-04.md` ("v3"; versions 1 and 2 unchanged). Tables: new script
`phase2_exploration/src/p2y_addendum1.py` (a copy of `p2c_addendum1.py`, which is not edited, with the named
`OVERRIDES_V3`), stdout `addendum1_v3_stdout.txt` ("[n]" = its section). Run on einstein, `nice -n 19`, 2 min 06 s,
125 MB, pure Python. No job on a worker, no git command, no subagent. Protocol of `agents/fixer.md` per finding.

**Open when I finished: the A-1 re-validation.** v3 P6 carries the one placeholder line "A-1 re-validation: pending,
campaign `p2-c-px-tr`". The campaign is defined (session Xavier) and had not run at 15:04.

## Findings of the second review

| finding | what it asked | what changed | evidence | status |
|---|---|---|---|---|
| **A-1** parent truncation for DIF-C, NI-C | truncate by time or use the Geant4 crossings; report 433 / 1,464, 514 / 1,463, and the 8 and 88 late parent hits; add the hard check | v3 P6 rewritten: what v2 validated, what it did not report (all four numbers and the 0 / 988, 2 / 877 of the first-arc classes), the consequence (6×10⁶ of 1.7×10⁷ events), "validated as proposed" withdrawn; rule: truncation at the vertex **time** for the classes after a turn; hard check ≤ 2 % missing crossings per stream; v3 §0.1 item 5 says it first; decision D8 | numbers read by the script from `data/p2c/p2-c-b1yv/000/p2-c-b1yv-val.json` [7]; code: `p2x_b1.py` (modes radius / time / both / auto), `p2x_validate.py` (`A1_MAX = 0.02`), both by Xavier | **PARTIALLY**: the rule and the honest record are in; the re-validation (`p2-c-px-tr`) has not run; placeholder line in P6 |
| **A-2** `pilot.c0.hs` in rule 1 | computable reading, in the script and in §3.1; three options; number of distinct parents; own road, all central hadrons | the sample is in the script (`HS_SIZES`, section [3]) and in every rule-1 row; options H1 (2×10⁶ vertices, parents from the Z(νν) pilot events), H2 (v2's 2×10⁵), H3 (not read) with readings as one term and as seven weight classes; distinct parents printed (7,200 from 2×10⁴ events; 8.3×10⁵ from the pilot's events, 2.4 vertices each); drafted: **H1 as one term (161; 238 / 262 / 284)**, stated to be 24 events more lenient than the literal reading of STR l.1564 (185; 262 / 286 / 307); decision D2 | [3], [4]; first direct measurement of the share: 0.872 ± 0.032 in-road pool parents per triggered event, 35.5 at any azimuth [V: p2-c-px-hsg-r0, read with `/var/tmp/jdochoa/yvonne/slices.py`] | **RESOLVED** for the reading and the tables. **Not adopted:** firing all central hard-scatter hadrons. They are 41 per in-road parent (N_t ≈ 1.8×10⁸ [E]); in one unweighted 2×10⁶ sample a count would be 93 events. v3 states the population as unread (P2, §6.1) and offers a second stratum (7.3×10⁶ vertices, 15 CPU-h, reading 186; 263 / 287 / 309) in D2 |
| **B-1** the road | m = (event, orientation) passes over 21 orientations; remove "nothing measures outside the road" | pinned in v3 P2 and in the rule-1 wording of §3.3; exposure check 21 × 0.30 = 6.30 against 2π (+ 0.27 %, strict side); N_t and events per count unchanged; multiple passes of one event counted each time and flagged | [6]; `p2x_b1.py` records the 21 orientations in its metadata | **RESOLVED** for the minimum-bias share; hard-scatter hadrons outside the road: see A-2 |
| **B-2** `pilot.c0.lowpt`, \|η\| > 1 | N_t and events per count; say that a zero bounds nothing; what rule 1 does; η: sample or statement | measured parent counts: 5.20 per interaction at 0.3–0.5 GeV (73 % of the pool), 3.64 at 1 < \|η\| < 1.5 (51 %) [V: p2-c-px-mbb-big, 125,000 interactions]; N_t 2.6–5.2×10⁸ at one to two times the pool's vertex yield (not measured), one count in 2×10⁵ = 1,300–2,600 events, zero allows 1,500–3,000: said in §0.1 item 4 and P2; in the draft the sample is an alarm (no zero allowance; one count at a candidate rung pauses), the population an untested limitation with its consequence (§6.1); sizing it as a term costs 21–35 CPU-h and reads 186; 263 / 287 / 309 (D4); η: stated untested, the second pool is kept in `pilot.mb` | [6], [4] | **RESOLVED** as a statement with numbers; the vertex yields of both populations remain unmeasured (flagged [E]) |
| **B-3** consequences and bookkeeping | K 10 → 13; PR-1, T2-a, COM header, INV-1 rows 17 and 19; missing superseded lines; decays-in-flight size and Q2 (c) table | K = 13, T_c = 22 with the family sizes recomputed by the strategy's `one_rung` (7.0–9.9 % against 6.9–8.9 %) in v3 §3.2, §4; COM section: header note, B1-f, T2-a, PR-1, VC-3, INV-1 (samples 11, 17, 18, 18a, 18b, 19), T1-a; superseded list of §3.3 extended (l.52, 407-411, 421-424, 472, 811-813, 955, 968-976, 1091, 1813, 2104, 2111-2115, 2345-2348, 2829-2832, 2854-2862, 2875-2880, 2888-2889, 2940); §3.6: (α1) 385–647 → 481–810, (γ) row, the (c) grid recomputed on the draft reading (f_D = 0: ×67 [×46] against ×44 [×30]) | [5], [12]; regression: the 4-term row of [5] reproduces `budget_stdout_v9.txt` l.453-477 | **RESOLVED** |
| **B-4** state of the pilot code | say what is written; one validated job per stream; β cut not an environment default; calendar margin | v3 P7: what exists and has run, what was written 14:34–14:55 and is not validated (named), "nothing here claims the B1 production code is ready", one job per stream through `p2x_validate.py` before bulk release, β as a campaign parameter; §4: 45 h on 3 slots, 67 h on 2, day 5 = 2026-11-21, no margin on 2 slots | Xavier's log (read 14:56) and `p2x_*.py` headers; [8] | **RESOLVED** (as a statement; readiness is Xavier's deliverable) |
| **B-5** B1 pool floor | one shared Geant4 pass | `[9]`: one 'all' pass at 0.904 ms per firing with the chain, optimum 86 % of 208 CPU-h: B1 sum **23.0** (43.1 in v2; reviewer's estimate ≈ 24); sums 201 / 168 / 152 / 121 with the low-weight classes | [9] | **RESOLVED** |
| C-1 | Z(νν) and `pilot.mb` first | stated in v3 P1 and §4 (cleared by the orchestrator) | — | applied |
| C-2 | 190,730 → 193,313; 53 % → 61 % | both corrected; the sum is asserted in the script | [1] | applied |
| C-3 | frozen 13 → 12; ≈ 7,660 → 7,700; "3–4 / 3 / 2" | frozen row printed by this script with the tie rule: 12 (299.6; 300.2 with the strategy's sampler); projection 7,710 with the v3 pilot; row "6–7; 3–4 / 2–3 / 2" | [4], [11] | applied |
| C-4 | writer of the partition JSON in `p2c_g4vtx.py` | **not applied as code**: `p2c_g4vtx.py` is imported unchanged, with its hash recorded, by the slice jobs now running, and a writer needs the acts environment on a worker, which I may not use. v3 P7 states the provenance (hand-run after the last edit of `classify`; npz metadata of 14:07; reproduced by both reviewers) and that the pilot's own partition, written by `p2x_g4prod.py` with its code hash, supersedes the file | — | not applied, reason given |
| C-5 | pile-up-photon conversions in one sentence | v3 §0.2, below the table: 2.4 per triggered event, 1.0×10⁸, B2, read through the pile-up estimate only | [1] | applied |
| C-6 | share 0–3 % | v3 P2: 1.560 / 1.613 and a third value 1.594 on 125,000 interactions; 1.3 % by direct parent count; 1.022 kept as upper side | [1] | applied |
| C-7 | 3 % more in the 'all' pass | `ALL_PASS_MARGIN = 1.03` (+ 0.2 CPU-h); stated in P7 | [8] | applied in the script and text; to be set in Xavier's campaign parameters |
| C-8 | sums, softer jets, hadron list in the Z(νν) summary | present in `p2x_hs0.py` (ΣE_T in \|η\| < 5 and < 3, hadrons and photons with \|η\| < 1.5, p_T > 0.3 GeV); jets to 15 GeV, not 10; v3 P1 says so; + 1 kB per event in the storage | Xavier's log 14:43 | applied (jets: 15 GeV, stated) |
| C-9 | 'all' jobs ≤ 2×10⁶ firings | 62 jobs of 10 min; P7 | [8]; `p2x_pilot_campaigns.py` `all_per_job` | applied |
| C-10 | low-weight-class floors | row in §3.4: + 8.6 / + 7.1 / + 6.3 / + 4.8; in the sums and in the reach | [9], [10] | applied |
| C-11 | reading with fewer terms | §3.1 rows, §3.2, decision D1 (c): three terms 96 (99 with H1), one term 62 (65) | [4] | applied |
| C-12 | toys at 80, 100 parameters; jax | §4 and §0.2: 9,604 / 18,246; jax 4,729–5,141 tagged [U], "not reviewed" | [11] | applied; the jax numbers stay [U] until their run is reviewed |

## Items of the first review that were PARTIALLY resolved

| item | state in v3 | status |
|---|---|---|
| A3 hand-over validation | superseded by A-1: the fault is reported, the rule changed, re-validation pending | PARTIALLY (same placeholder) |
| B3 what the strict option changes | completed by B-3 (K, PR-1, T2-a, header, inventory rows) | RESOLVED |
| B7 hard-scatter share | sample defined with size, parents, reading and cost (A-2); the job exists in Xavier's generator, not validated; 1.022 remains a planning value, with a first direct count beside it | RESOLVED as a definition; measurement pending with the pilot |
| B10 resolving power; lower p_T edge; η; road | B-1 and B-2: the road is pinned; the low-p_T sample has N_t and events per count and is called what it is; η stated untested with a measured parent count | RESOLVED as statements; two populations remain untested (v3 §6.1) |

## Judgment calls (also in `experiment_log.md`)

1. **Seven terms drafted** (strategy's convention: one term, one sample, one Gamma(m + 1) per population; STR l.1563,
   l.1575-1578, l.726-727, l.2733-2734 quoted in v3 §3.2). Four, three and one are given with readings, families and cost.
2. **Hard-scatter sample as one term**, not seven weight classes: more lenient than STR l.1564 read literally by 24
   events; disclosed in v3 §0.3 D2 and §3.2. A fourth route exists and is not drafted because it is a design change:
   mixing the hard-scatter vertices into each class sample at their natural proportion (no extra zero; this is what
   the frozen "unbiased" samples implied and what v3 proposes for the 4a pool). It needs the class yields of the
   hard-scatter parents before the B1 streams are produced. The orchestrator may prefer it.
3. **Low p_T, |η| > 1 and off-road hard-scatter hadrons left unread**, stated first, with the cost of reading them.
4. **Truncation of first-arc classes** left at v1's radius cut unless `p2-c-px-tr` shows the time cut is as good.

## Propagation

Old → new, all inside the new files (v1 and v2 are kept as records): per-count values with the hard-scatter share
on its own sample 26.5 / 24.4 / 4.9 / 6.6 / 6.6 / 23.7 / 24.9 → 25.9 / 23.9 / 4.8 / 6.5 / 6.5 / 23.2 / 24.3 (v3 §0.2, P3 table,
§3.3 wording, COM ST-1); empty reading 159; 237–283 → 161; 238–284 (§0.1, §0.2, §0.3, §3.1, §3.2, §3.6, COM ST-1); B1
pool floor 43.1 → 23.0 and sums 213 / 182 / 166 / 137 → 201 / 168 / 152 / 121 (§0.1, §0.2, §0.3 D6, §3.4, COM B4-c); reach
506–597 [443–524] → 514–584 [445–514] seven terms, 522 / 597 four terms (§0.1, §0.2, §3.5); pilot 131 CPU-h, 144 GB →
134.5 (135), 156 GB (§0.2, §4, COM ST-1, INV-1); projection 7,700 → 7,710 (§0.1, §0.2, §4, COM T1-i); T_c 22 kept,
K 13 added (§0.2, §3.2, §4, §5, COM header, B1-f, T2-a, PR-1, VC-3). `grep` of v3 and of the COM section for the
old values 159 (kept only where labelled version 2 or H3), 213, 137, 131 CPU-h, 144 GB, 190,730, 53 %: no stale use.
COM: only the section "Changes of rows by addendum 1" was replaced (the 285 lines above are byte-identical: `diff`).

## Regression check

The script prints the frozen numbers before any override acts: 76.1 [36–152] (d15_q of the unchanged budget script:
76.6); frozen m_Z = 11 / 12 / 13 → 281.6 / 300.2 / 318.5 (STR 281 / 300 / 317); reach 790 [712] and R08-like 113, 496
[435]; planned floors 8.64 / 3.94 / 12.59; K = 10, T_c = 19: 5.1–10.2 %, 2.1–4.2 %, 4.9 %, 6.9–8.9 %. Version 2's rows
reproduce: 388.5 / 466.6–514.5; 159.2 / 236.7–282.2; SM 169.4 / 138.3 / 122.5 / 93.4; B1 43.1 and 5.8 with v2's costing;
reach 506 [442], 522 [451], 565 [503], 597 [524]; both reviewers' values where they differ from v2 (frozen m_Z = 12;
"2–3" in the 3.5×10⁶ row; hs rows 195.9 / 273.1–319.1 and 431.7). Budget copy sha256 548b5ba8… unchanged.

## Neighbourhood check

1. A sample named in the text but absent from the script (A-2): checked every stream of P7 against the script:
   `pilot.c0.lowpt` was also absent; it is now in [6] and in the cost.
2. A wrong sum row (C-2): re-derived every sum and species split of the P3 table from the JSON (the NI 30 and 61.5 mm
   species splits are now printed too); the script asserts B1 + conversions + other = all vertices.
3. Cells on the limit (C-3): all crossings recomputed at 10⁵ draws with the tie rule; the frozen R08 crossings are now
   given for all three pile-up values (8 / 7 / 6 and 3 / 2 / 2; v2 gave 7 and 2 for the central value only).
4. A cost charged per class instead of per pass (B-5): checked the other cost models: the pilot (already one shared
   pass), the SM rows (per process, correct), the four-term variant (one large class, correct as it was).
5. "Validated" claimed too widely (A-1): re-read the other "verified" statements of v2: the Fatras no-decay check stands
   [V, reproduced by the second review]; the partition file's provenance is now stated (C-4); "\|η\| < 1 and the road
   are physics" (v2 P2) is withdrawn: neither is a bound.
6. v2's "182" for the forced-tt̄ sum was 138.3 + 43.1 = 181.4.
7. My own first low-p_T number came from the slice of `p2x_mbgen.py`'s first version, which had a known fault in the
   v1-rate cuts (Xavier's log); replaced by the rewritten slice `p2-c-px-mbb-big` (5.20 against 5.12 per interaction).
8. Every STR and COM line cited in v3 and in the COM section was read at that line in this session.

## Diff-level list, version 2 → version 3

- Header: self-contained; tags; script and stdout named.
- New §0 (was the five-item list): §0.1 seven statements, §0.2 the frozen → v1 → v2 → v3 table, the conversion fact,
  §0.3 eight decisions with options, costs and a recommendation.
- §1: unchanged in content; item 4 no longer says the proposed hand-over is validated.
- §2 P1: "provisional" kept; summary columns of C-8; start order. P2: split into pool / N_t / hard-scatter parents /
  road orientations / lower p_T edge / |η| > 1, each with numbers. P3–P5 table: per-count column on the minimum-bias
  share, sum row corrected, hard-scatter row added, species of NI 30 and 61.5 mm; 53 % → 61 %; the 4a treatment of the
  hard-scatter share. P6: rewritten (A-1). P7: state of the code (B-4), C-4, C-7, C-9.
- §3.1: frozen row from this script (12; R08 range); rows for H1, H1 as weight classes, H2, H2 as weight classes, the
  off-road stratum, low p_T as a term, three terms, one term, each also with H1; doubled B1 samples.
- §3.2 (new): the number of terms, the strategy's lines quoted, families and cost per choice.
- §3.3 (was 3.2): wording with the orientations, the hard-scatter term and the low-p_T rule; superseded list extended.
- §3.4 (was 3.3): B1 row 43.1 → 23.0, low-weight row, sums; what the preselection-first column gives up.
- §3.5: reach on the v3 floors; R08-like B₅₀ in the result. §3.6 (new): (α1), (γ), Q2 (c).
- §4: pilot 134.5 CPU-h, order and calendar; families; projection at 80 and 100 parameters and the jax readings [U].
- §5: K, the truncation rule, the Q2 (c) numbers added to "changed". §6: point 1 (three unread populations), 6, 8 new.
- COM: section replaced (header note, B1-a…g, B4-c, T1-a, T1-i, T2-a, PR-1, ST-1, INV-1, VC-3).

**Not done.** No pilot campaign; no edit of STR, of addendum versions 1 and 2, of `p2c_*.py`, of `s4pu.py`; no
measurement of mine on a worker (the slice numbers cited are Xavier's outputs, read on einstein).
