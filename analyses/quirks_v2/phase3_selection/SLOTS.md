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
