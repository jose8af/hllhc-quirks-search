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
2026-11-24 14:55 -0500 | p3-b fix (Ivar) | maxwell | actual count: 3 jobs (B3 check, launched 14:52, running to completion, ~21 min wall each); per orchestrator, no further parallel job: the plot job (1 job) starts only after all 3 have ended
2026-11-24 15:04 -0500 | p3-f (Jorunn) | maxwell | 1 job, nice 10-19 | p3-f code smoke/timing tests (interactive, <= 10 min each) then p3-f-occx validation + campaign (1 job until 19:00; after 19:00 up to 4 minus running qv2run jobs), then p3-f-refind | until ~26 Nov
2026-11-24 15:13 -0500 | p3-b fix (Ivar) | maxwell | B3 check: 3 jobs ended 15:12 (3 × 1,063 s user = 0.886 CPU-h, max RSS 0.26 GB, exit 0); now 1 job, nice 19: plots.py regeneration (<= 10 min)
2026-11-24 15:15 -0500 | p3-b fix (Ivar) | maxwell | RELEASED (B3 check 3 jobs 0.886 CPU-h + plot job 4.5 s CPU done; no Ivar process left)
2026-11-24 15:17 -0500 | p3-c (Birgit) | schrodinger | still <= 2 jobs: one slot p3-c-mjw (stops after 4 jobs), one slot p3-c-mjs2 + p3-c-ap-mjs2 (second driver, max-per-node 1); p3-d has its own 1 job here | until about 18:00
2026-11-24 15:19 -0500 | p3-b review cycle 2 (Liv) | maxwell | 1 job, nice 19, read-only IS re-analysis (review/critical/liv_ischeck.py), < 2 min
2026-11-24 15:19 -0500 | p3-b review cycle 2 (Liv) | maxwell | RELEASED
2026-11-24 15:32 -0500 | p3-f (Jorunn) | maxwell | 1 job (weekday cap) | p3-f-occx (100 jobs, ~15 CPU-h ESTIMATE); raise to 4 - running qv2run jobs after 19:00 | ~24-25 Nov
2026-11-24 15:43 -0500 | p3-d (Gorm) | orchestrator note acknowledged (schrodinger at 4). Checked now: schrodinger runs 1 p3-d job (p3-d-one-c1-k35, driver --max-per-node 1) beside 2 p3-c; p3-d-pyhf runs on maxwell only (1 job). The 4th process seen earlier was probably one of my development probes run by ssh (14:40-15:03, now ended). From now on: schrodinger <= 1 p3-d job, no ssh probes there beside it; numpy jobs on maxwell only after checking that qv2run job count <= 3 (cap 4 shared with Jorunn)
2026-11-24 16:03 -0500 | p3-d (Gorm) | schrodinger: p3-d-one driver stopped (SIGINT) to free the single slot for the R1'/conditioning probes (advisor point 3); its running job p3-d-one-c2-k1-m100 finishes; p3-d-one is relaunched (pending jobs resume) after the probes; still <= 1 p3-d job on schrodinger
2026-11-24 16:29 -0500 | p3-d (Gorm) | schrodinger: probes done (p3-d-pchk, -pchk2, -probe); p3-d-one relaunched (14 pending: T1-c (ii), recipe), <= 1 job
- 2026-11-24 16:44 -0500 p3-a Aurora: RELEASED landau (campaigns p3-a-cls-m [stopped], p3-a-clsxz 115/115, p3-a-clsxb 116/116; nothing running). Left on landau scratch: /home/scratch/jdochoa/p3a_slice (slices, numba cache), /home/scratch/jdochoa/p3a_cache_seed.
2026-11-24 16:45 -0500 | p3-e-devpu1 (orchestrator launch) | landau | 3 jobs (cap) | 297 jobs × ≈ 18 min ≈ 92 CPU-h, ≈ 31 h wall at 3; driver on landau | campaign p3-e-devpu1 (dev.pu1, sealed per Freja A2)
2026-11-24 16:46 -0500 | p3-a review (Sindre) | maxwell | 1 light job (nice 15, read-only recount of p3a outputs, < 0.1 CPU-h) | checked: qv2run job count 1
2026-11-24 16:52 -0500 | p3-a review (Sindre) | RELEASED maxwell (one 23 s job, done)
2026-11-24 16:59 -0500 | p3-a review round 2 (Vilde) | maxwell | 1 job (nice 15, ionice idle; 8 sequential parts of p3a_indep.py --stride 2 --offset 1, ~0.74 CPU-h ESTIMATE, read-only on Z(nunu) pilot files, no signal) | checked: qv2run job count 2
2026-11-24 17:02 -0500 | p3-g (Tormod) | maxwell | 1 job, nice 10 | smoke tests (p3g_prep dif slice, p3g_ovl_job 2 events), each <= 10 min | qv2run jobs 2 at check
2026-11-24 17:10 -0500 | p3-c (Birgit) | schrodinger | RELEASED (all p3-c campaigns finished or stopped; 11.2 CPU-h in the ledger)
2026-11-24 17:13 -0500 | p3-c (Birgit) | schrodinger | <= 2 jobs for about 10 min: p3-c-pw2 (pilot weights again with the MET_reco azimuth column) | then RELEASED
2026-11-24 17:19 -0500 | p3-c (Birgit) | schrodinger | RELEASED (p3-c-pw2 done 17:18; 11.3 CPU-h in the ledger in total)
2026-11-24 17:21 -0500 | p3-g (Tormod) | schrodinger | <= 2 jobs (orchestrator assignment; Gorm holds 1) | campaigns p3-g-prep, then p3-g-npo, p3-g-npo0, p3-g-ovldif, p3-g-g4pu, p3-g-zhl (≈ 69 CPU-h ESTIMATE), jobs <= 30 min, driver on schrodinger | uptime 1.48, who 0, 1 qv2 job (p3-d) at check
2026-11-24 17:21 -0500 | p3-g (Tormod) | maxwell | RELEASED (smoke tests done, no p3-g process left)
