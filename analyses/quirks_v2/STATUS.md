# Status — quirks v2

**2026-11-23 19:20 -05 (measured), day 7.** Phase 2 (Exploration): all items in except the independent review of the
subset-pass classifier (running tonight); `phase2_exploration/outputs/EXPLORATION.md` written. **Waiting for the user:**
the calendar shift after the power loss (DECISION 23 Nov 13:41, default C on Wed 25 Nov 12:00); the C1-c docker permission
(DECISION 19 Nov, no default, needed by Phase 5); optional objection to D8 (Z(νν) top-up not drawn). Daily report:
`daily/2026-11-23.pdf`. Notices: `notices/`.

| | |
|---|---|
| Approved schedule | 4,609 CPU-h, stop-and-ask at 5,992, about 60 days (Gate A, 16 Nov); ≈ 64 days if the dates shift by 4 (ESTIMATE) |
| CPU-h used | 445.7 (markers, every attempt, 3,348 jobs; VERIFIED) + ≈ 3–5 not in markers (ESTIMATE); 13.6 today |
| Projected total | ≈ 4,600 [4,070–5,050] CPU-h (ESTIMATE, checkpoint 1, 23 Nov) |
| cajuela, this project | 248 GiB (266 GB) (VERIFIED, du); ≈ 0.68 TB projected |
| cajuela pool free | 3.7 TB of 4.5 TB |
| last repo bundle | `repo-2026-11-23.bundle` |

**Outage:** power loss Thu 19 Nov 17:54 – Mon 23 Nov ≈ 13:00 (3.8 calendar days); 9 jobs killed, all retried and done;
no data lost. Worker hostname resolution fixed by the admin (never configured; not an outage effect).

**Running:** only Nils's review of `p2w_subset.py` (schrodinger, 1 slot, ≤ 1.5 CPU-h). landau and maxwell idle (no
planned Phase-2 compute left).

**Results today:** decision point 1 passed (C1 41/41 with E1–E4, sealed 6/6 PASS); checkpoint 1 no stop rule near;
rule-1 validation: subset-pass m_Z = 1,501 at R08 (B₅₀ ≈ 63,170, classifier under review; finder lower bound 253 →
10,777): pause at day 15 still expected; D2 r(R06) = 0.72, below the factor-2 threshold, no correction; FxFx E1500
−2.4 ± 1.8 % vs MLM, inside band, S2-c FxFx complete; NI C′_PU ρ = 0.024 at R05; D8 top-up not drawn; reach re-estimate.

**Open problems / risks:** subset classifier unreviewed (stand-in lower bound is still "above"); ρ_γ rests on one source
event; 60 % "mixed" conversion candidates unmeasured (decide the reach outlook); NI and SM closure tests (B4-c, B5) have
little or no power → pause package; per-job numba cache before production; FxFx untested below 500 GeV.

**Reach (ESTIMATE):** Gate A envelope below 243 GeV; attributed-only edge 350–445 GeV; back below 243 GeV once more than
≈ 14–24 % of the mixed conversion candidates survive. **Reach outlook vs last report: more promising, weakly; not
established.** A pause at day 15 remains expected.

**Limits in force:** 10 GB cap, nothing heavy on einstein, one pixi install at a time, never rename a directory on
cajuela, pushes only of `v2-jfc` for daily reports and notices, never forced.

**Next interventions:** by Wed 25 Nov 12:00 the calendar shift (default C); shifted day 15 = Sat 5 Dec binding
projection, pause expected; freeze 7–9 Dec (if shifted).
