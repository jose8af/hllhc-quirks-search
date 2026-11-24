# Phase-3 slot table (append-only; see PHASE3_BRIEF.md §2)

Caps (state rule 5): landau 3, schrodinger 3 (graphical logins), maxwell 4; weekdays 08:00-19:00 at most 9 jobs in total.
Assignments 2026-11-24 10:08 -0500: p3-a (Aurora) landau <=3; p3-b (Casper) maxwell <=3; p3-c (Birgit) schrodinger <=2.

- 2026-11-24 10:16 -0500 p3-a Aurora: landau, <= 3 jobs (weekday cap), until about 20:00 today, campaigns p3-a-cls-m, p3-a-cls-u, p3-a-cls-pv0, p3-a-cls-pv2, p3-a-ind + ssh slices (nice 10). uptime 0.14, who 2, no qv2 process at 10:12.
2026-11-24 10:17 -0500 | p3-c (Birgit) | schrodinger | <= 2 jobs | until about 25 Nov, jobs <= 30 min | campaigns p3-c-* (generator-level Pythia, MET model; ~32 CPU-h)
2026-11-24 10:24 -0500 | p3-b (Casper) | maxwell | <=3 jobs | p3-b-thin (50 jobs, ~1.5 CPU-h ESTIMATE) then p3-b-direct (4 jobs, ~0.1 CPU-h) | ~1 h wall
2026-11-24 13:23 -0500 | p3-b (Casper) | maxwell | p3-b-thin finished (50/50); p3-b-direct launched (<=2) beside p3-b-occin (1); total <=3
2026-11-24 13:33 -0500 | p3-b (Casper) | maxwell | p3-b-refind (20 jobs, 1 slot, ~1.7 CPU-h) + p3-b-occmod (8 jobs, 1 slot -> 2 after occin) + occin last job; total <=3
2026-11-24 13:55 -0500 | p3-b (Casper) | maxwell | occmod done (8/8 + forced rerun of occmod-000); p3-b-refind driver restarted with <=3
2026-11-24 14:17 -0500 | p3-b (Casper) | maxwell | RELEASED (all p3-b-* campaigns finished; no p3-b process left)
2026-11-24 14:25 -0500 | p3-b review (Dorte) | maxwell | 1 job, nice 19 | re-derivation of p3-b closure numbers from p3-b-* outputs (read only, no campaign) | <= 1 CPU-h, ~30 min wall
2026-11-24 14:28 -0500 | p3-e (Hilde) | maxwell | 1 job, nice 10 | p3-e-devpu1 test job devpu1-0000 only (20 events, ~20-25 min, ~0.3 CPU-h) + p3-b reader check (nice 19, < 5 min) | uptime 1.19, who 0, no qv2 process
2026-11-24 14:45 -0500 | p3-b review (Dorte) | maxwell | RELEASED (re-derivation done, ~0.17 CPU-h, no process left)
2026-11-24 14:48 -0500 | p3-e (Hilde) | maxwell | RELEASED (devpu1-0000 done 14:47, reader check done; no p3-e process left)
2026-11-24 14:52 -0500 | p3-b fix (Ivar) | maxwell | 3 jobs, nice 19 | B3 check: is_check.py --mode strat --all (plain 1e5 toys + fresh IS 2000 toys on each of the 6,400 stored occmod stage-B configurations; read only, no campaign) | <= 0.9 CPU-h, ~20 min wall; then 1 plot job (<= 10 min) | uptime 0.53, who 2, no jdochoa python process
2026-11-24 14:54 -0500 | p3-d (Gorm) | maxwell <= 2 jobs (numpy) + schrodinger 1 job (jax) | maxwell: p3-d-pyhf (11 jobs, ~2 CPU-h) now; schrodinger: dev smoke now, then p3-d-one and p3-d-lim/st/cov (jax toys), until about 26 Nov | uptime maxwell 2.77 (reviewer job present), schrodinger 1.1; no p3-d process before
