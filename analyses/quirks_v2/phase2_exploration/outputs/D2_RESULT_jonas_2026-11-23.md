# D2 result: robustness row "later arcs restored" (Jonas, executor, 2026-11-23, written 15:29 -0500)

Successor of Ulrika (her session died in the 19 Nov 17:54 power loss). Frozen plan:
`outputs/D2_PLAN_ulrika_2026-11-19.md` (committed 564fa1a before any event was generated; **not changed**). Frozen
criterion: ADD1 v5 §1.5 l.308-321, copied in plan §6. Background only: no signal file was read, no signal quantity was
formed. Tags: [V] verified by me (command / file cited), [E] estimate, [U] unverified (transcribed).

## 1. Verdict

**"Effect, robust", with r < 1 at every rung: no B6-d correction (no credit for r < 1); [L15] is stated with the
measured size.** The row is **evaluated at R06** (paired bootstrap error on ln r = 0.061 < 0.1).

Restoring the later arcs (Geant4 crossings beyond half a turn, exchanged one for one against v1 top-up crossings so
that the raw hit density is unchanged) **lowers** the pile-up candidate count by 23-28 %: r(R04) = 0.766,
r(R05) = 0.759, r(R06) = 0.720, each many σ from 1, with no trend from R04 to R06. In 599 of 600 events the varied arm
has fewer R04 groups than the nominal [V]. The v1 chain plus top-up is therefore conservative (it over-counts) for
this effect, at the precision of 600 events.

## 2. Numbers (600 events, 2,400 paired trials; `trials.n_grp` = [SD4] count)

Source: `p2-c-d2-sum` output `/nfs/cajuela/jdochoa/quirks_v2/data/p2c/d2/p2-c-d2-sum/000/p2-c-d2-sum.json`
(sha256 84edaf0f…, marker `ledger/markers/p2-c-d2-sum/000/p2-c-d2-sum.marker`) [V]. B, r and the paired widths were
re-derived independently from the npz files with my own script and bootstrap seed
(`/var/tmp/jdochoa/jonas_d2/rederive.py`, 4,000 replicas): B and r identical, widths 0.0029 / 0.0045 / 0.0605, trend
0.0603 [V].

| rung | B_nom (per trial) | B_var (per trial) | r | ln r | σ paired boot | σ unpaired boot | σ Poisson |
|---|---|---|---|---|---|---|---|
| R04 | 397,410 (165.6) | 304,519 (126.9) | 0.766 | −0.266 | 0.0028 | 0.039 | 0.0024 |
| R05 | 114,962 (47.9) | 87,240 (36.4) | 0.759 | −0.276 | 0.0043 | 0.042 | 0.0045 |
| R06 | 593 (0.247) | 427 (0.178) | 0.720 | −0.328 | 0.061 | 0.068 | 0.063 |

Trend ln r(R06) − ln r(R04) = −0.062 ± 0.061 (paired), z = −1.02 [V]. 2,000 replicas, seed 20261119, none dropped.

### Reading against the pre-declared criterion (plan §6, applied as written)

| test | requirement | measured | result |
|---|---|---|---|
| Evaluated (B6-a) | σ(ln r) at R06 < 0.1 | 0.061 | **evaluated** |
| No effect | \|ln r\| ≤ 0.1 and within 2σ of 0 at R04-R06, \|trend\| ≤ 2σ | \|ln r\| = 0.27-0.33, 94σ / 63σ / 5.4σ | not met |
| Not robust | \|ln r\| > ln 2 = 0.693 at a rung, or trend > +2σ | max \|ln r\| 0.328; trend z −1.02 | not met |
| → Effect, robust | otherwise (plan §7 item 6: a significant negative effect falls here) | | **yes** |
| B6-d correction | only if r(R06) > 1 under "effect, robust" | r(R06) = 0.720 | **does not apply** |

So: no correction of the pile-up estimate; the day-15 reading is unchanged by D2; [L15] carries the measured size
r(R06) = 0.72, ln r = −0.33 ± 0.06 (paired event bootstrap, 600 events).

### Additional readings, no verdict (ADD l.309)

- (b) r at "N_2S2 ≥ k on top of R04/R05/R06" [V]: k = 1: 0.766 / 0.759 / 0.720; k = 2: 0.767 / 0.759 / 0.720;
  k = 3: 0.765 / 0.756 / 0.722 (paired σ as the base rungs). The requirement removes almost nothing at k ≤ 2 and
  does not change r.
- (a) varied arm, candidates with a sensor holding ≥ 2 hits of one particle, ≥ 1 of them injected [V]: R04 14,505 of
  118,579 hit-recorded candidates (12.2 %; partial at R04, plan §7 item 8), R05 14,494 of 118,449 (12.2 %),
  R06 62 of 446 (13.9 %), i.e. 55 of the 427 varied R06 groups. Almost every same-particle double involves an injected
  hit (R04: 14,505 of 14,507). The restored arcs do enter candidates; the net count still falls because the top-up
  crossings they replace make more candidates than they do.

## 3. What changed between the arms (per event means, [V] from p2-c-d2-sum.json)

- Chain: 10,518 charged generator particles; Geant4 crossings 144,968, of which 31,608 beyond half a turn; injected
  SimHits 31,592 (17,962 on written surfaces = injected written measurements); 12.6 injected from particles with no
  Fatras hit; 3,133 crossings that pass only the time condition were not injected (plan §7 item 1); seam duplicates
  12.5.
- Finder input: 48,701 nominal barrel hits (dumps), 17,761 injected barrel hits; top-up after the exchange 93,158
  hits; per layer the n_inj crossings dropped equal n_inj in every layer and event (no excess anywhere, 0 events with
  excess) [V]. Largest exchange TBPS_L1: 2,991 of 8,569 top-up crossings replaced (35 %); TBPX_L1 522 of 11,420 (4.6 %).
- Pairing: 0 of 2,400 trials with a different trial seed, PV or road angle [V]; group recount = `trials.n_grp` in both
  arms [V].

Mechanism (hypothesis, not tested here [E]): a v1 top-up crossing is a pair of hits at the same (φ, z) on both
sensors of a stacked layer (`acts/stage4/finder/pu_inputs.py` l.46-53), a radial, stiff-looking stub at uniform φ;
a restored arc of a looper is a strongly bent, locally clustered set of hits. At fixed raw density the first is the
more dangerous for the finder, so replacing it lowers the count.

## 4. Acceptance checks (plan §4)

1. Chain smoke (Ulrika, 19 Nov) passed [U: her log 11:25-11:30]. Production: V4-1 ok in all 600 events [V];
   injected written measurements 10,777,255 vs injected SimHits on written surfaces 10,777,258 [V].
2. Non-injected written hits vs the nominal dumps: equal in 591 of 600 events; **9 events** (Ulrika's log said 8)
   differ by one hit: 6 with one hit fewer, 3 with one more; the 3 "+1" events are exactly the 3 injected
   measurements not recognised by truth position [V: `/var/tmp/jdochoa/jonas_d2/check_ctl_chain.py`]. The finder takes
   the nominal part from the dumps, so the only effect is 3 missing injected hits in 10.8 M: negligible. CKF flags of
   nominal hits changed by the injection: 222.6 per event (0.45 %), not propagated by construction (plan §1,
   experiment_log 19 Nov 11:26) [V]. (The stored total 133,538 includes −1 for each of the 9 mismatched events.)
3. Control p2-c-d2-ctl (injection off, 20 events of c1pu1-0000): all 31 per-trial arrays equal to the nominal
   (n_grp, n_pass, n_grp_T, n_pass_T with 43 columns, seeds, PV, phimet, …), except timing columns and
   `dz_nearest_pu` (|Δ| ≤ 3×10⁻⁶ mm, the dump path rounds vertex z to 10⁻⁶; diagnostic, not a counted quantity) [V].
   c1pu1-0000…0029 therefore serve as the nominal arm; no nominal re-run was needed.
4. Pairing in every varied job: see §3 [V]. Both arms complete over the same 600 events: p2-c-d2-find 60/60 done
   (`qv2run status`, 15:25), c1pu1-0000…0029 done [V].

## 5. CPU (markers, one row per campaign / job_id / attempt, terminal lines; `/var/tmp/jdochoa/jonas_d2/cpu.py`) [V]

| campaign | jobs | attempt rows | CPU-s | CPU-h |
|---|---|---|---|---|
| p2-c-d2s-chain / -find / -find2 (smoke) | 4 | 4 (1 failed) | 244 | 0.07 |
| p2-c-d2-chain | 30 | 30 | 29,415 | 8.17 |
| p2-c-d2-ctl | 2 | 2 | 893 | 0.25 |
| p2-c-d2-find | 60 | 62 (2 lost) | 26,414 | 7.34 |
| p2-c-d2-sum | 1 | 1 | 13 | 0.00 |
| **total measured** | | | **56,979** | **15.83** |

The 2 lost attempts (0014-a/b on landau, killed by the power loss after ≤ 3.0 and ≤ 0.7 min) have no CPU record:
≤ 0.06 CPU-h [E]. Total ≈ 15.9 CPU-h, against the plan's 12.4-14.5 [E] and the stop rule 28: inside. The nominal arm
(33,455 CPU-s, p2-a-c1-pu1) was reused, not spent by D2. Unit costs measured: varied chain 49.0 CPU-s per event
(plan estimate ≈ 24.5 s: generation + Fatras + digitisation + Geant4 + injection; 2.0× the estimate), varied finder
44.0 CPU-s per event (plan 43.5-56.6) [V].

## 6. Flags for the orchestrator / user

1. The effect is large and significant but negative: the frozen rule gives no credit, so nothing changes in the
   day-15 reading. It does say the v1 top-up model gives 1.39× (1/0.720) the R06 pile-up candidates of
   restored arcs at equal density (ESTIMATE of meaning; the mechanism in §3 is a hypothesis).
2. The plan's open ambiguities (§7 items 1-9) stand as Ulrika wrote them; in particular 3,133 per event crossings
   that are later than the last Fatras hit but before half a turn were not injected (item 1); their effect is not
   measured.
3. 9 (not 8) events with a ±1-hit nominal mismatch; negligible (§4.2).
4. The varied chain cost twice the plan's unit estimate; the total stayed under the stop rule.
5. Plan §7 item 7: the 600 events are the C1 reproduction / B2 development events, not a closure sample.

---
**Orchestrator note, 2026-11-23 15:45 -0500 (supersedes wording at l.16 and l.113-114; text above left as written).** Advisor ruling Olav (LOG.md 2026-11-23 15:32), binding for EXPLORATION.md, [L15] and the paper: "conservative (it over-counts)" holds only at R04–R06, at fixed raw hit density, on 600 development events, assuming the TDR density; it is not a statement about the pile-up term at R08+. 1/r(R06) = 1.39 ± 0.08 is a nominal/varied ratio at R06, not a property of the top-up model, and is never used as a factor (no credit). "Robust" is the B6-b label = below the factor-2 threshold. "No trend" → "no significant trend (−0.062 ± 0.061)". Caveat: 55 of 427 varied R06 groups (12.9 %) are a same-particle-double class absent in v1; net r < 1 does not show it stays subdominant at R07+.
