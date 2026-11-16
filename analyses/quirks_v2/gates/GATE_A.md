> Phase-1 review PASSED in cycle 10 (`phase1_strategy/review/arbiter/STRATEGY_ARBITER_v10_quentin_2026-11-16_10-51.md`).
> Artifact of record: STRATEGY v10 (`phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`), `COMMITMENTS.md`,
> `budget_stdout_v9.txt`, `src/check_day15_text.py`. Times in file names before 2026-11-16 are sequence labels, not
> clock times (`LOG.md` correction of 2026-11-14 01:20).

# GATE A — quirks v2: strategy, benchmarks and schedule

Sources: STRATEGY v10 (STR, `STRATEGY_oscar_2026-11-16_10-41.md`), `budget_stdout_v9.txt`
(stdout). **All reach and background numbers: ESTIMATE on v1
placeholder efficiencies**.

## 1. Headline
**Expected (ESTIMATE).** By v1's counts the background at the R08–R09 selections is **≈ 0.7–1.0×10⁴ events, led by
hard-scatter photon conversions** (after CKF, as v1 counted them; a lower value). With the strategy's normalisation
width (0.17) the **reach is below 243 GeV, at or near the existing bounds (≈ 180 GeV; R-20 pending)**; ≈ 270–300 GeV
(84 % edge; 390–420 for a background known exactly) are statistics-only. Caveats: decays in flight rest on 1–2 v1
counts; the SM floor on a guessed 45 ms/event; v1's efficiencies are ×1/0.87 high. **The day-15 rule is expected to pause the study**: it
reads the pilot's own-hit counts before CKF, expected at B₅₀ ≈ 3×10⁴–3×10⁵ against 300 (the ×5–50 rests on an
assumed pair efficiency, not measured). A conversion veto counts only in a Q2 (c) redesign, and at v1's central
decays-in-flight size no conversion rejection suffices (without conversions B₅₀ is 458–718).

**Upside (ESTIMATE)** (84 % edge (median), statistics-only): 420–455 GeV (470–500) if conversions and decays in
flight fall like pile-up (310–370 at width 0.17; still pauses: ≈ 2.6×10³–4.2×10⁴ as the rule reads it); 705–640
(770–695) if Z(νν) is tested and the other ceilings count 10–100, conditional on the promotion model (post-freeze;
at day 15 read through the Z(νν) pilot count); 710 (790) if every ceiling is empty, an
upper edge.

## 2. What Phase 1 established
| 4 jobs/node | PU-200 event, chain | finder trial | ρ = 2 event | no-pile-up event |
|---|---|---|---|---|
| cost | 13.5 s | 11.7 s | 206 s, 1.46 GiB | 45 ms (guessed) |

Of 4,453 CPU-h: 753 measured, 2,322 derived, **1,378 guessed**.
- v1 chain on Linux. MG5 2.9.22 + Pythia 8.313 reproduce v1's LO σ (z = 0.91); NLO K = 1.165 at 200 GeV; Geant4 11.4.3 installs in ≈ 3 min. Runner tests pass.
- Incidents (`LOG.md` 14:06, 15:12): stale file handle after a cajuela directory rename; einstein out of memory.
  Since: the rules of `AGENT_RULES.md`.
- Review: cycles 1–10, Category A 11→4→1→0→0→0→0→0→0→0, Category B 24→14→15→5→3→1→4→1→1→0 (cycle 9: a stale
  count, fixed in v10; cycle 10: a mechanical check of v10, PASS).
  Cycles 4–8 turned on the day-15 reading; cycle 8 found rule 1 ambiguous and pinned it (Df-11: limit ≈ 12 Z(νν) pilot counts, not ≈ 20).

## 3. Your decisions
● = default; answer "Q1 ●; Q2 ●; …".

**Q2 (central): what if the day-15 projection exceeds B₅₀ = 300 (or both pile-up estimators miss their cap)?** Rule 1
reads the pilot's own-hit counts before CKF: no S_CKF, no veto or fit-probability credit, nothing post-freeze, no
pool floor. Every SM process is read through the one Z(νν) pilot count, a proxy, since no sample of another SM process exists
at day 15 (stdout l.354–364).

| pilot counts (branch) | day-15 B₅₀ | vs 300 |
|---|---|---|
| (α1′) v1's conversion counts (expected) | ≈ 3×10⁴ (ε_pair 0.8) to 3×10⁵ (0.98) | above |
| (α1) DIF, conversions fall like pile-up | ≈ 2.6×10³–4.2×10⁴ | above |
| Z(νν) pilot count, the others zero (also (β), (γ)) | 281 at 11, 300 at 12, 317 at 13 | limit at ≈ 12 |
| decays-in-flight pilot count, the others zero | 266 at 3, 331 at 4 | below up to 3 |
| every pilot count zero | 76 (37–152) | below |
| (c) test only: (α1) with fit-probability credit on DIF and conversions | 109–130 | below |

Rejection a (c) conditional needs (stdout l.365–370; pilot basis, S_CKF estimated, photon rate 0.379 [0.255]):
- none suffices at v1's central decays-in-flight size;
- ≥ ×44 (97.7 %) [×30] if the pilot counts no decay in flight; ×75–150 [×51–101] at a quarter of that size; ×114
  (99.1 %) [×77] or none at ×e⁻¹;
- all unmeasured; zero survivors among n show ≤ ×n/1.14; without S_CKF ×219–2,186, and none from a quarter of that
  size on.

- **● (a) Pause and ask at day 15:** ≈ 2 days (inside the 60), 0 extra CPU-h (the 156 CPU-h reserve tests the
  leading term); then (b) or (c).
- **(b) Proceed now:** 0 CPU-h, no delay. Paper: the plan's "real background" outcome; reach expected below
  243 GeV, not beyond existing bounds.
- **(c) Redesign before the freeze:** a conversion-removing conditional; freeze delay reported at day 15; CPU-h from
  development allowance and reserve. Works if B₅₀ ≤ 300 (bar above). Say whether it may also target decays in flight (needed at v1's central size). Paper: "middle" if it works, else (b).
- If B₅₀ ≤ 300 (≥ 560 GeV, statistics-only): production proceeds; "middle" outcome.
- *Optional rider* ("Q2 ● + rider"): (b)/(c) asked at day 7 if B₅₀ ≥ 3,000 (expected in the expected branch); 1,000 γ overlays
  (+7.0 CPU-h). Gain: ≤ 8 days under (c).

**Q1, C1 blinding.** ● Six v1 signal counts sealed until Gate B, four open. Alternatives: all ten open;
six dropped. 14 CPU-h each.

**Q3, D4 exception.** An untested MUST closure criterion enters at its ceiling, "no credit", selection eligible.
● Yes. Alternatives: comply where costed, ≈ +680 CPU-h (100–1,230), +3.9 days; strict ("closure fails" likely).

**Q4, budget and calendar.** ● **4,609 CPU-h, 60 days**, stop-and-ask at **5,992**, with [DP1] B5 reduced
(−358), [DP2] B6 at 4 points (−155), [DP4] S4/S5 out, [DP5] second hadronisation model generator-level only.
Contingency 2,150 CPU-h not pre-approved. **Your 2–4 weeks is missed by 4–5 weeks** (43.5 days without
critical-path production). Alternatives: §5; envelope 6,759 (threshold 8,787).

**Q5, truth-level signal before the hash** (313 CPU-h). ● Yes, idle capacity, 0 days. Alternative: after the
hash, +47 CPU-h, +1.8 days.

## 4. Eleven defaults (overridable; STR §12.1)
| # | default | # | default |
|---|---|---|---|
| Df-1 | 2,000 signal rows/point | Df-6 | endcap outlook "signal ×1.5–3.2" |
| Df-2 | closure F = 1.5/2, cap ln F/3 | Df-7 | unsourced detector variation: no nuisance, shift reported |
| Df-3 | NLO σ nominal, resummed beside it | Df-8 | parametrised toys, exact check at 3 points |
| Df-4 | dE/dx not a candidate | Df-9 | ceiling on own hits, S_CKF where tested; sets the day-7/15 basis |
| Df-5 | time-tag credit only where it closes | Df-10 | coverage checks: one family of 10 |
| **Df-11, NEW (pinned in cycle 8)** | rule 1 reads only day-15 samples: every SM process via the Z(νν) pilot count (a proxy, probably lenient: by v1's photon rates their conversions are under-read by ≈ 8 %, at most ×1.6), no pool floor; (c) factors never multiply a floor; ties pause → limit ≈ 12 counts (R09 candidate; ≈ 6–7 at R08) | alternative | SM at pool floors: limit ≈ 20, more lenient, blind to most conversions, (c) looks easier |

"Ties pause" in Df-11 is the sentence added in cycle 9 (binding B₅₀ from ≥ 10⁵ draws; a reading within that precision
of 300 pauses). You may drop it; it is then fixed in Phase 2.

## 5. Budget and calendar
| variant | CPU-h | threshold | days (no pause / pause) |
|---|---|---|---|
| MUST only | 4,176 | 5,429 | 56.9 / 58.9 |
| **MUST + reduced SHOULD (●)** | **4,609** | **5,992** | **57.8 / 59.8** |
| full SHOULD | 5,123 | 6,660 | 58.1 / 60.1 |

4,609 = MUST 4,019 + SHOULD 434 + reserve 156; rider 4,616 / 6,001. Capacity assumed: 174 core-h/day production, 116
development. Range 49–65 days; +8 with two ITERATEs per review. Storage ≈ 470 GB (670 at cap)
of 1.5 TB.

## 6. Decision points after Gate A
**Day 5:** C1, C2; CPU re-projection (stop rule may fire). **Day 7:** preliminary projection.
**Day 12:** MET model, final pilot classification. **Day 15 (binding):** rule 1; (c) on development estimates; pause
if B₅₀ > 300. Freeze days 17–19; Gate B ≈ day 49 (51 with pause); Gate C ≈ 58 (60).

## 7. Top risks
1. Conversions: no reach beyond existing bounds without a demonstrated rejection ≥ 98.7–99.3 % (quarter of v1's
   decays-in-flight size; 97.7 % if the pilot counts none; 99.1 % or none at ×e⁻¹) and fewer decays in flight.
2. Pilot statistics: an empty pilot reads B₅₀ 76 of 300; each decays-in-flight pilot count adds 65
   events, and four pause the study (two at R08).
3. Conversion normalisation sets the reach (s95 2,697 against 352 statistics-only): likely > 80 % of the
   uncertainty.
4. CPU: 1,378 CPU-h guessed; the stop rule may fire (day 5, freeze).
5. Pile-up beyond R07 on one estimator; Geant4→Fatras hand-over.

## 8. Paths to a stronger paper (none demonstrated)
A pilot counting far fewer conversions and decays in flight; under (c), conversion rejection ≥ ×44 (×114 or none
if decays in flight are e times below v1's central size, none at that size) plus fewer decays in flight;
conditionals measured in production. **If none works**, the plan's "real background" paper: the first measured
quirk-plane background, the reach at that B, the sideband recipe as the way out.

## 9. Files
STR v10 (§0, §12.1); `budget_stdout_v9.txt`; `src/check_day15_text.py` (45 of 45 on v10); `COMMITMENTS.md`;
`phase1_strategy/outputs/feasibility/`; `phase1_strategy/review/arbiter/` (cycle-10 verdict); `LOG.md`; `DEVIATIONS.md`.
