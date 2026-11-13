# D6: decision history of v1 (Andrzej, 2026-11-13)

Sources read in full or in the relevant ranges: TL = `stage2_C001_quirks/theory_track/LOG.md` (336 lines, 127 kB; read in full), S2 = `stage2_C001_quirks/LOG.md` (27 lines, read in full), R = `research/LOG.md` (17 lines, read in full). Line numbers refer to those files. Tags: V = VERIFIED (read at file:line), U = UNVERIFIED (not found in the three logs; taken from the publication plan or from my memory of other files). Timestamps in the logs are Ecuador local time. "M3" means the MacBook Air M3 (4P+4E cores, 7 workers used); "PC" means the Windows 7800X3D box. Dates in the logs are 2026-10-xx.

Caveat on scope: several items you asked about are not decided in these three logs. They live in the stage reports. Where the log only points to them I say so. Items missing from the logs: the Lambda>=15 keV cost of 371 CPU-h (U, plan only), the rho=3 cost of 128 h (U, plan only), the pre-merge "routes" bookkeeping. The factor 117 is not in the logs; I found it at `acts/stage4/STAGE4_RESULTS.md:256` (V): model spread ln(P_fact/P_main) = ln 117, which only enters sigma_ln.

## 1. Timeline

| Date | Milestone | Ref |
|---|---|---|
| 10-05 | Research project starts: env audit, plan, tools | R:2 |
| 10-05/06 | Scouting 199 seeds, 986 papers, 74 candidates; Gate 2 27 PASS/37 HOLD/10 REJECT; Gate 3 only 27 PASS reviewed; Gate 4 top 10 | R:3-11 |
| 10-06 | Arbiter ranks C001 (quirks) and C005 Tier A; human checkpoint | R:15-16 |
| 10-07 | User picks C001; 4 research agents; strategy draft S1/S2/S3, recommends S3 staged; review loop to PASS (R2) | S2:2-20 |
| 10-07 | Theory track T1-T6 created (Lambda, string dynamics, propagation, trajectory fit, literature, model space) | TL:2-26 |
| 10-08 | Synthesis v1 to v4 over reviews R1-R4 (R4 PASS); 48-page theory report | TL:27-65 |
| 10-10/11 | Stage 1: analytic near-miss law, numerics, reviews S1-R1..R4 PASS; user fixes P1 scope = option (b) | TL:66-108, 95 |
| 10-11 | Stage 2: hand-written UFO, MG5+Pythia8 samples, ~23.5 of 35 CPU-h used; PASS R2 | TL:109-133 |
| 10-11 | Stage 3 plan; V2b gate FAILED as pre-registered; user proceeds; production launched 14:19 | TL:134-137 |
| 10-12/13 | Stage 3 Mac share done 29.7 h; PC share received; merged 218 571 events; PASS | TL:138-145 |
| 10-13 | Stage 4 plan, nine review rounds R1-R9, PASS | TL:147-175 |
| 10-13 | G2a finder speed t1 3.76 s; Phase A weights; G1 chain; WP_RULE frozen 18:19; G3 pilot launched | TL:176-196 |
| 10-14 | G3 verdict FAIL (closure x1.32/x1.42); T_seed 6 to 4; C1a launched 00:28; PC-19 SR-T fix frozen 01:50; analysis pipeline frozen after R1-R5 | TL:201-264 |
| 10-15 | Token-outage plan; deadline moved to Sun 10-18 | TL:266-268 |
| 10-16 | C1b done 09:11 (24.7 h); C2B done 08:55 (23.3 h); no WP; A2FC revert; results PASS 13:41; Stage 5 PASS 13:26; Stage 6 PASS ~12:00 | TL:270-314 |
| 10-16 | Paper note PASS (35 pp); f_200 normalisation bug found and fixed (limits x21 weaker) | TL:315-327, 321-323 |
| 10-17 | Paper v0.4, appendix D | TL:329-335 |
| 10-18 | 46 GB data moved to external drive | TL:336, S2:27 |

## 2. Decisions that constrain v2

| Decision | Date | Reason given | Ref |
|---|---|---|---|
| Model: E=(1,1)_-1 fermion, N_IC=2 primary; Etilde as second species; sigma14 ~220/6.1/0.20 fb at 200/500/1000 GeV (agent LO x K, ESTIMATE) | 10-07 | FASER/Knapen comparable | S2:11 (V) |
| Grid: E 200-1500 GeV in 100 GeV steps, Etilde 200/500/1000 | 10-11 | user approved plan | TL:121 (V) |
| Generator chain: MG5_aMC LO MLM 0-2j + Pythia8, CP5 (check vs 1903.12179) + Monash check, MPI on, xqcut 30 / qCut 45, ME cut pT(QQ)>100, vertex at origin, FxFx later (not done) | 10-11 | ME cut 150 lost ~6 % of pT>200 tail | TL:120-121 (V) |
| PDF: CT18NLO (full download), MG default EW with alpha(MZ) norm, LO x K-factor | 10-11 | user approved | TL:121 (V) |
| QED FSR off quirks: kept, not regenerated; carry one-sided l_max systematic -1.1 +- 0.8 % | 10-11 | re-shower costs ~15 CPU-h > budget; diagnosed: QEDshowerByOther needs isResonance, SLHA DECAY resets it | TL:130,133 (V) |
| Tail-rate systematic of LO-MLM +12..+15 / -11..-13 % (alps-dominated, ESTIMATE); fixed-pT ISR trick biases l_max median -26/-10/-5 % | 10-11 | validation | TL:128,130 (V) |
| String Lambda range: window 0.6-15 keV at 3.8 T from theory; 50 % eff edge 0.45-0.7 keV; Stage-3 grid 0.45-10 keV for P1, 0.3-1.2 band, 1.5-10, then 15/20/30 (+40 for heavy) added by user | 10-07 to 10-11 | N_osc<1 at 0.28-0.33 keV, l_max=R_IT at 0.43-0.94, merging l_max=100 um at 13-25 keV | S2:11; TL:22,133-134,140 (V) |
| Cost of high Lambda: BM (B plus MS) is 5-10x B at >=20 keV; B-only b_odd/l0 at 3e-8 double-precision floor at >=20 keV; Athena MaxSteps 2e6 kills Lambda >~24 keV | 10-08/11 | per-step MS kicks | TL:18,134 (V). The 371 CPU-h for Lambda>=15 keV (64 % of string bill) is U, plan only. |
| Straight-string models not used; causal Nambu-Goto propagator (T3_causal) is the reference; Li et al. algorithm ~15 % low at gamma*=1.28, gamma*-dependent | 10-08 | independent conformal solver agrees <=1 % | TL:22,32-36,42 (V) |
| P1 scope = option (b): B-field crossing physics; MS only as measured numerical floor | 10-11 | R2 reviewer, user | TL:95 (V) |
| Geometry: public rebuild from TDR + tkLayout OT806_IT742 (D111), material not public so x0.5-x2 systematic; hybrid ACTS only (Fatras plus injected quirk SimHits), no custom stepper (6-12 wk) | 10-11 | no per-layer material public; user approved | TL:124-125 (V) |
| PU: TDR-normalised top-up baseline (Fatras in-time PU too low x2.3-7 vs CMS-TDR-014 Fig 6.3), PU200, sigma_z 45 mm, sigma_t 190 ps | 10-13 | V4-2 comparison | TL:126,150,153,155 (V) |
| doMerge=False in ACTS smearing; merging at analysis level (U-5 b) | 10-13 | doMerge merges close quirk hits and silently drops them (V8) | TL:142,146 (V) |
| Finder design: IT-triplet seeds plus PV plane; seed threshold T_seed 6 then 4; window W_c=75 mm; t_tol 30 um; no Delta-w cut; road = delta95 = 0.15 rad; counting rungs R01-R09+, width rung, core chi2, dE/dx only with PU-dilution admissibility; 10 layers, CKF pT>0.9 GeV with per-measurement flag | 10-13/14 | A-1 review: Delta-w cut kills signal; G3 pass fraction moved >2 sigma | TL:150,153,184,186,217 (V) |
| Fast path for signal: 31 numpy A2 points, row-major numpy digitisation with Fatras-model deposits, full chain only at A5 (5 species-masses at 1 keV) and A2FC (9 points) | 10-13/16 | cost; V4-6 revert rule pre-declared | TL:199,278,312 (V) |
| Barrel-only: frozen |eta(n3)|<1.0, endcap = future work | 10-13 | user re-decided D4-12 | TL:184,186 (V) |
| Working-point rule: B84 <= 0.11 per category (0.11 + 0.11 split SR-T/SR-G, combined 0.30 at sigma_ln 2.3), one ladder, frozen at G2 | 10-13 | 0.3/2.71=0.11 | TL:150,158; `WP_RULE.md:374-377` (V) |
| Thinning: exact interaction-count thinning (conservative x2.1-2.9 over 2.5 decades in pilot); closure gate T1-T3 with failure path | 10-13 | density ladder unmotivated power law | TL:150,153 (V) |
| Thinning closure FAILED at G3: x1.32/x1.42 (T_seed 6); at T_seed 4 x1.500/x1.606, patched x2.41 (=1.5 x 1.606) at rungs >=R05; trend in sigma_ln only; no +50 % stat steps, no union rule change | 10-14, 10-16 | user accepted pre-registered conservative end state | TL:201,210-211,274,298 (V) |
| Factor 117 (model spread) | 10-16 | upper envelope, adds only sigma_ln | `STAGE4_RESULTS.md:256` (V), not in logs |
| rho=3 (C5) sample: optional behind gate G2c, never run; 128 h/0.6 decade (U, plan only) | 10-13 | cost; deadline | TL:158,163,198; STAGE4_RESULTS.md:657,744 (V for "not run") |
| Pre-registration: V2b gate (10-11), WP_RULE frozen 10-13 18:19 with hashes (21 files), no signal efficiency looked at; HASH_ADDENDUM admission; PC-19 frozen 10-14 01:50; analysis freeze (30-32 files, re-frozen R1-R6); signal match definition declared before any signal efficiency (10-13 20:35); V4-6 revert set declared 10:19 before launch (10-16) | various | | TL:136,195,200,241-247,257,262,275,278 (V) |
| Discarded/deferred: A3/A4, C2-C, C3, C4' (future work), cloud (dropped), C5 rho=3, endcap finder, NLO FxFx, shower-weight variations, gamma-gamma sample, O-1 test, floor tests (double-double/mpmath), Open Data (note only, CMS policy) | 10-11 to 10-16 | deadline/cost | TL:128,146,198,209,160,161,102,179 (V) |
| Final result: no WP in either category (min B84 1.23e6 at R09; 7.05 decades over 0.11); best sigma95/sigma_th 37.6 corrected to 790 after f_200 fix | 10-16 | | TL:298,322 (V) |

## 3. Recorded compute costs (M3-laptop CPU-h unless stated)

| Item | Cost | Ref |
|---|---|---|
| Stage 2 plan | ~2.3 M events, ~35 CPU-h, ~2.5 GB | TL:120 (V) |
| Stage 2 top-ups | +5.5 CPU-h, total ~23.5 of 35 | TL:130 (V) |
| Stage 3 probes | ~6 CPU-h | TL:134 (V) |
| Stage 3 plan | ~330 CPU-h = 47 h on 7 workers (range 250-460), full 615, disk ~2 GB | TL:134 (V) |
| Stage 3 job list at gate | 402 CPU-h (Mac 148 / PC 253) | TL:136 (V) |
| Stage 3 production | 4576 jobs, 498 CPU-h ESTIMATE; Mac 207 CPU-h, 29.7 h wall, 7 workers; PC 290 ESTIMATE, 10 workers | TL:137-138 (V) |
| Stage 3 actual | 218 571 events; Mac 207.5 / PC 375.5 CPU-h; reruns 1.26 CPU-h | TL:140 (V) |
| Stage 3 fix/B*-off | ~1.0 CPU-h | TL:142 (V) |
| Stage 4 plan, first | ~450 CPU-h (lean ~210), 70 h Mac wall, ~6 GB | TL:147 (V) |
| Fixer R1 probes | 5.5 CPU-h (over 3 target) | TL:150 (V) |
| Finder at full density before speed-up | 48 s/trial (72 % O(N^2) merge), 211 s/trial vectorised; realistic 560-1700 CPU-h | TL:153 (V) |
| Cap decisions | Mac 7 M3-CPU-s per wall-s; 170-200 CPU-h per production day; cloud est. +110 (UNVERIFIED, then dropped) | TL:155,157,160 (V) |
| G2a | t1 3.76 s median (x1.12 at 4 parallel), t2 27 s; ~3.5 CPU-h | TL:176 (V) |
| Phase A | t2 33.9 s; ~1.0 CPU-h; storage 37-42 GB | TL:182 (V) |
| G1 | chain 4.83 s/event; t1 3.26 s, t2 20.1 s; ~1.3 CPU-h | TL:190 (V) |
| G3 pilot | 130 jobs, 16.9 CPU-h est., wall/est 1.74 then 1.85; t1 5.60 s, t2 37.1 s under load; ~3 CPU-h reruns | TL:196-197,201 (V) |
| C1 | 95.7 CPU-h (G1b 26.8), 1635 jobs; after T_seed 4: C1a 52.9 + C1b 162.4 per-worker-h | TL:199,229-230 (V) |
| C1a/C1b/C2B walls | C1a 7.6-8.7 h est.; C1b actual 24.7 h; C2B actual 23.3 h (est. 28-33) | TL:229-231,271-272 (V) |
| A2FC | 180 jobs, 1800 events, 9.7 CPU-h, 1.41 h wall, 4.4 GB | TL:279 (V) |
| Stage 4 total | 382 CPU-h production, 2295 jobs | TL:298 (V) |
| Analysis pipeline | ~1.3 CPU-h; 64 CPU-min D2; 98 CPU-min fixer R3 | TL:255,259,261 (V) |
| ACTS PU-200 event | 1.5 s/event Fatras, ~95k measurements; CKF 23-60 s whole cylinder, 1.6-3.4 s with 32 sectors | TL:126,147 (V) |
| Strategy phase | 24-34k core-h Phase 2 estimate (planning, not spent) | S2:17 (V) |
| Hardware | MacBook Air M3 (4P+4E), Windows 7800X3D, GCP free trial only (dropped) | TL:155,157,160,197 (V) |
| Lambda>=15 keV string 371 CPU-h; rho=3 128 h | | U (plan only) |

## 4. Failed attempts and dead ends

- Straight-string / lab-simultaneous string headline (x0.04-60 thickness, mm fake MS) was an artefact of T2's own algorithm, not Li's; withdrawn. Do not use a straight string with material. TL:32,36 (V).
- Pre-registered V2b gate failed: population median c excess +0.7 to +3.2 % at 1 keV on MG events; later explained as scatter/estimator effect +1.85 +- 0.19 %. Never claim the c law to better than 1.5 % per event. TL:136,140 (V).
- 3-5 keV c excess attributed to B* with ESTIMATE only; floor not excluded (k_B>=10). TL:141-144 (V).
- Delta-w < 1 cm cut kills signal; F0 alone gives only ~x3 PU separation, 7-9 decades short. TL:149-151 (V).
- Trimmed core-width variant collapses on PU, rejected. TL:153 (V).
- Per-step factorisation on a common population is anti-conservative by orders of magnitude (nested tails). TL:255 (V).
- Per-hit-set grouping at rho=2 over-merges (anti-conservative closure) and full loose grouping costs 144 s/trial. TL:182,201 (V).
- G3 closure at T_seed 6 failed; SR-T window was empty because t_min = 25 ns = dt_acc; fixed by PC-19. TL:201,213 (V).
- Asymptotic CLs 2.7e-4 x toys (NLL offset saturation), fixed in R6; use toys primary. TL:274-275 (V).
- Normalisation bug: N_exp omitted f(pT>200) (limits 6-21x too optimistic) found only at paper review. Check N_exp <= N(pT>200). TL:321-322 (V).
- ACTS pyacts on Windows impossible (no win-64 wheel); conda-forge acts-core has no bindings. TL:147,124 (V).
- Downloaded TDR geometry files were 404/bot pages. TL:124 (V).
- Scouts' "no search found" claims unreliable. R:6 (V).
- FASER exclusion read by eye was flat; real contour C-shaped. TL:45 (V).
- Cloud: dropped; session rate limits (429) interrupted agents repeatedly (TL:16,20,35; S2:16; R:10,12). Plan for reruns.

## 5. Bugs and platform quirks relevant to a Linux port or re-run

- ACTS navigation assertion "Checking volume outside of bounds"/GridPortalLink insideBounds kills jobs (~1/700 events), phi-sector portal artefact; absent at nphi=1; fix = deterministic per-event seed replacement. TL:197,199,201 (V). Expect on Linux too (U).
- ACTS bounded smearing loses ~3 SimHits per 3e6 (tolerance max(2,1e-5 n)). TL:190,280,284 (V).
- ACTS per-event RNG stream: PU measurement smearing is re-drawn between paired jobs. TL:280 (V).
- Fatras pMin default 0.5 GeV to 30 MeV; mol/cm3 vs mol/mm3 material bug. TL:147 (V).
- scipy.stats.landau != CERNLIB Landau (x pi/2 + shift). TL:185 (V).
- Interim chain: time column in mm/c and BTL sigma_t 0.12 ps (smoke only). TL:185 (V).
- run_stage4.pack key collision: runner "road" index overwrote process_trial half-width (stored as road_cfg); products.py l.205-206 'trials_phimet' lookup bug (frozen). TL:194,195,311 (V).
- Cross-machine reproducibility: kernel output bit-identical in 224/225 overlap events (1 event 4.4 um); code md5 identical; PC runs needed no changes. TL:139-140 (V).
- Numerical: double-precision floor b/l0 ~3e-8 (>=20 keV); max_boost 1e-2 step-biased for c, 1e-3 used, 3e-2 rejected; R1 conformal needs N>=1024; round-off amplification at head-on even crossings. TL:134,72,76,136,137 (V).
- Seeds: TRGS rows shuffled with recorded seed; deterministic unweighting; Pythia per-interaction reseed; toys seed 20261014, 5000 toys. TL:130,185,257 (V).
- MG5: pythia8_card reordering resets CP5 (Tune:pp), use own Pythia jobs; MG rewrites input/.autoupdate each launch; MG .pyc footprints; LHAPDF 6.5.5 on py3.9 with six. TL:120-121,128,130,132 (V).
- macOS specifics: pixi on macos 26.0 virtual package, numba in theory env, sandbox harness refused subagent writes of .md files. TL:61,126,255 (V).
- Data/state living outside git: 46 GB theory_track/data, kinematics cache 170 MB, CT18NLO grid, Athena snapshot. TL:56-57,336 (V).
- A2FC admitted with 1 V4-1 FAIL; ID clash D12/D13. TL:283-284,299 (V).

## 6. Open items left in the logs, mapped to plan items

| Open item | Ref | Plan item |
|---|---|---|
| Pile-up closure x2.41 unexplained residual x1.6-1.8; T3 not informative; deeper PU needs rho=3 or lever arm at R07-R09 | TL:152-153,201; STAGE4_RESULTS.md:744 | B2 |
| C' DIF/PV-pair and SM zero-count bounds dominate deep rungs; needs 1e8-2.8e9 events/term vs 500-2000 | TL:298 | B1, B4 |
| Fatras has no hadronic physics; SM proxy samples (W e/mu proxy, tW allowance 0.10 x tt, tt K=1.9 conservative) | TL:258,261 | B1, B4 |
| PU density x2.3-7 below TDR (top-up systematic) | TL:150 | B6 |
| Endcap finder, barrel-only | TL:184 | S3 |
| Signal stats 31 numpy A2 points, 200 events each; E500 3 keV A2FC full chain loss, ε(FB2)=9/200, systematic CKF loss x0.83-0.87 | TL:312-313 | S1 |
| FxFx NLO, K-factor transcribed, tail-rate +12..15 % not propagated, shower weights, gamma-gamma | TL:128,323 | S2 |
| No WP, nothing excluded; need likelihood and selection rule with a budget | TL:274,298 | T1, T2 |
| SR-T BTL timing definition (PC-19) fixed; in-job BTL for rho>1 | TL:192,213,241 | T2 |
| Merging-tolerant rung for Lambda>~3 keV; sep_IT not measurable at PU 200; upper Lambda edge 4.6-7.5 keV vs truth 13-25 keV | TL:274,298 | S4, S5 |
| Floor tests (double-double/mpmath), O-1 B*-off | TL:102,141-142 | P1 |
| Cosmics/halo not studied (Open Data note only) | TL:179 | B7 |
| Paper: N_IC label in HANDOVER_STAGE4, tail-rate unpropagated, 0805.4642 two authors | TL:299,323 | C3 |
| Data restore from external drive (46 GB) | TL:336 | C1 |
| CMS Open Data policy confirmation | TL:179,289 | out of scope per plan |
