#!/usr/bin/env python3
"""Arithmetic behind the Phase-1 STRATEGY v3 (STRATEGY_emeric_2026-11-13_21-10.md).

Standard library only; run as `python3 -I strategy_budget.py` (about ten seconds; allowed on einstein).
History: v1 by Brigitte (17:55); rewritten by the fixer Dmitri for review cycle 1 (arbiter findings M1-M35);
updated by the fixer Emeric for review cycle 2 (findings N1-N18 and the residuals of M4, M5, M11, M12, M15, M24, M26).
Every unit cost carries a provenance letter:
  M = measured in the feasibility phase (source in the comment);
  D = derived from measured parts, or measured on one event / toy inputs;
  G = guess (not benchmarked).
CPU-h are slot-hours on a worker with 4 jobs per node (the "4 concurrent" columns of FEAS_A).
Sections printed: [1] unit costs, [2] capacity, [3] budget table, [4] totals and variants, [5] deltas per finding,
[6] contingency, [7] calendar, [8] storage, [9] zero-count floors (M6), [10] zero-count likelihood checks (M1),
[9b] projection per outcome (N7), [11] closure-test size and power (N4), statistics for the MUST closures (N2),
[12] extrapolation width (N5), [13] other checks, [14] deltas v2 -> v3 per finding.
"""
import math
import random

H = 3600.0
# ---- [1] unit costs (seconds) -----------------------------------------------------------------------------------
CHAIN = 13.53      # M  PU-200 event, chain, 4 concurrent: FEAS_A §3.3
TRIAL = 11.71      # M  finder trial incl. top-up, CKF removal, merging, packing: FEAS_A §3.4
B1EV = 60.4        # M  chain + 4 trials, whole job per event: FEAS_A §1 / §3.7
RHO2 = 206.0       # D  one rho = 2 event (2 crossings, 2 roads), one smoke event: FEAS_A §3.7
NOPU = 0.0115      # M  no-PU single minimum-bias interaction through the chain: FEAS_A §3.6
GUN = 0.0141       # M  10-muon gun through Fatras: FEAS_A §3.6
G4GUN = 0.000134   # M  Geant4 pion gun, primary-only mode: FEAS_B Task 5
LHE = 0.034        # D  MG LO + Pythia shower + npz conversion per LHE event: FEAS_B (listed there as derived)
MLM = 0.050        # G  MLM 0-2j per LHE event: not benchmarked (FEAS_B open issue 7)
SHOWER = 0.021     # M  Pythia shower per signal event: FEAS_B Task 3
SHOWER_ZJ = 0.0234  # M  Pythia shower per Z(nunu)+j event: FEAS_B Task 3
MINBIAS = 0.0025   # M  Pythia minimum bias per interaction (2.0-2.5 ms): FEAS_B Task 3
NOPU_HS = 0.045    # G  no-PU hard-scatter event = shower 23.4 ms + chain on a few tracks 14.1 ms + 7.5 ms margin;
#                       the generation filter efficiency is not measured (arbiter §2: 15 ms was below the shower alone)
S3 = {1: 0.651, 3: 18.8, 5: 67.8}   # D  Stage 3, F 500 toy kinematics, s/event: FEAS_A §3.5
TOYS1000 = 652.0   # D  pyhf 1000 s+b and 1000 b toys at one mu point, 31 parameters: FEAS_C R9 (scaling unmeasured)
SCAN20 = 10.44     # D  pyhf 20-point asymptotic scan, 31 parameters: FEAS_C R9
FIT = 0.12         # D  one pyhf fit, 31 parameters: FEAS_C R9
SIG = CHAIN + TRIAL  # D  one PU-200 row with one trial (signal row, overlay, hit-level SM event)

v1s3 = {0.45: 0.037, 0.6: 0.080, 0.85: 0.212, 1: 0.334, 1.5: 1.070, 2: 2.528, 3: 8.175, 5: 32.286}  # STAGE3_INDEX.json
ratio = sum(S3[k] for k in S3) / sum(v1s3[k] for k in S3)
s3_sum = sum(S3[k] for k in S3) + ratio * sum(v for k, v in v1s3.items() if k not in S3)
s3_at = {k: (S3[k] if k in S3 else ratio * v) for k, v in v1s3.items()}

print("[1] unit costs")
print(f"  Stage 3: maxwell/M3 ratio at the 3 anchors = {ratio:.2f}; sum over 8 Lambda = {s3_sum:.1f} s/event")
print("  per Lambda:", {k: round(v, 2) for k, v in s3_at.items()})
print(f"  PU-200 row with one trial = {SIG:.1f} s; trial share of a B1-type event = {4 * TRIAL / B1EV:.3f}")

# ---- [2] capacity --------------------------------------------------------------------------------------------------
# 12 worker cores; 9 on weekdays 08-19 (brief §5.3). Two of three workers had a graphical session at preflight
# (LOG.md 14:34) and are capped at 3 jobs: 3 + 3 + 4 = 10 slots off-hours.
slot_week_12 = 5 * (11 * 9 + 13 * 12) + 2 * 24 * 12
slot_week = 5 * (11 * 9 + 13 * 10) + 2 * 24 * 10
slot_day = slot_week / 7.0
CAP_DEV, CAP_AVG, CAP_PROD = 0.50 * slot_day, 0.60 * slot_day, 0.75 * slot_day
print("\n[2] capacity")
print(f"  slot-h per week: {slot_week} with 10 off-hours slots ({slot_week_12} with 12); per day {slot_day:.1f}")
print(f"  effective core-h per day: development 0.50 -> {CAP_DEV:.0f}; average 0.60 -> {CAP_AVG:.0f}; production 0.75 -> {CAP_PROD:.0f}")
print(f"  if utilisation is 0.40: {0.40 * slot_day:.0f} per day")

# ---- [9a] zero-count floors: inputs (needed before the budget because the no-PU pool is allocated from them) ------
NTRIG = 4.0848e7                      # bsum_wp.json -> n_trig.value (read this session)
RATE = {"PV pair": 30.31, "DIF": 1.5945, "gamma": 0.379, "looper": 0.30, "V0": 0.052,
        "NI 22 mm": 0.11 * 0.22, "NI 30 mm": 0.11 * 0.22, "NI 61.5 mm": 0.11 * 0.22}
#   PV pair, DIF, gamma: D4 l.395 (cprime.<t>.rate); looper 0.30, V0 0.052, NI 0.10-0.12 x 0.22: D2 l.69 (UNVERIFIED)
SM_NTRIG = {"Z(nunu)+j": 25078824.8, "W(tau_h)": 5407122.7, "W(e nu)": 2536644.1, "tt 1l": 2379799.0,
            "W(tau_l)": 2257327.6, "W(mu nu)": 2238036.6, "tW": 259273.4, "tt 2l": 212934.8, "WZ": 137419.5,
            "WW": 126435.9, "t-channel": 110124.9, "ZZ": 104504.5}   # bsum_wp.json -> n_trig.breakdown (read this session)
G4_DEC, G4_NI = 0.011, 0.042   # M  vertices per pion gun (pT 1-10 GeV, |eta| < 1): decays, inelastic: FEAS_B Task 5
# N8 (cycle 2): one route per particle origin. Particles of the hard-scatter vertex that Fatras traces (prompt tracks,
# loopers, photon conversions, V0 decays) are counted by B4 on real events. The pool keeps, as single-interaction
# terms, only what needs Geant4: decays in flight and nuclear interactions (hard-scatter share + 200 x minimum bias).
# The cost per event of these terms includes the Geant4 guns needed for one distinct vertex per event.
POOL_SI = ["DIF", "NI 22 mm", "NI 30 mm", "NI 61.5 mm"]
C_SI = {"DIF": NOPU + G4GUN / G4_DEC, "NI 22 mm": NOPU + G4GUN / G4_NI, "NI 30 mm": NOPU + G4GUN / G4_NI,
        "NI 61.5 mm": NOPU + G4GUN / G4_NI}
terms_v2 = [(t, NTRIG * r, NOPU) for t, r in RATE.items()] + [(p, n, NOPU_HS) for p, n in SM_NTRIG.items()]
terms = [(t, NTRIG * RATE[t], C_SI[t]) for t in POOL_SI] + [(p, n, NOPU_HS) for p, n in SM_NTRIG.items()]
C_POOL_V2 = 600.0                     # v2: chain only; the Geant4 vertices were a separate line
G4_V2 = 65.1                          # v2 Geant4 vertex line (script v2 [3])
C_POOL = C_POOL_V2 + G4_V2            # v3: one envelope for the no-PU chain and its Geant4 vertices (same CPU as v2)


def allocate(c_total_h, sel=lambda t: True, tt=None):
    """M_t proportional to sqrt(N_t / c_t) at fixed total cost: minimises sum_t N_t / M_t (Lagrange multiplier)."""
    use = [(t, n, c) for t, n, c in (terms if tt is None else tt) if sel(t)]
    norm = sum(math.sqrt(n * c) for t, n, c in use)
    return {t: (c_total_h * H) * math.sqrt(n / c) / norm for t, n, c in use}


alloc = allocate(C_POOL)
SI = list(POOL_SI)
SMP = [p for p in SM_NTRIG]
m_si = sum(alloc[t] for t in SI)
m_sm = sum(alloc[p] for p in SMP)

# ---- [3] budget ------------------------------------------------------------------------------------------------------
items = []  # (phase, item, priority, label, cpu_h, arithmetic, provenance, finding)


def add(phase, item, prio, label, seconds, arith, prov, finding=""):
    items.append((phase, item, prio, label, seconds / H, arith, prov, finding))


# Phase 2
add("2", "S2", "MUST", "Stage 2: 5 species-masses, MLM, 250k LHE each", 5 * 250e3 * MLM, "1.25e6 x 50 ms", "G")
add("2", "S2", "MUST", "NLO K(m): 18 masses + 2 process generations; same scan with PDF4LHC21", 2 * 18 * 120 + 2 * 180, "2 x 18 x 2 min + 2 x 3 min", "M", "C(P-C4)")
add("2", "S2", "MUST", "FxFx 0-1j points at 500 and 1500 GeV", 2 * 20 * H, "2 x 20 CPU-h (upper value of FEAS_B's 5-20)", "G", "C(P-C5)")
add("2", "S2", "MUST", "re-showers: QED FSR, qCut 30/60, Monash (4 variants)", 4 * 1.25e6 * SHOWER, "4 x 1.25e6 x 21 ms", "M")
add("2", "S1", "MUST", "migration sample: generator cut lowered to 150 GeV, 5 x 100k LHE", 5 * 1e5 * MLM, "5e5 x 50 ms", "G", "M27")
add("2", "C1", "MUST", "Stage 3 at the 3 C1 points", 463 * s3_at[1.5] + 463 * s3_at[2] + 492 * s3_at[3], "463 x 2.3 + 463 x 5.4 + 492 x 18.8 s", "D")
add("3", "S1", "MUST", "Stage 3 truth, 2000 rows x 5 species-masses x 8 Lambda (after A is fixed, N15)", 5 * 2000 * s3_sum, f"1e4 x {s3_sum:.1f} s", "D", "N15")
add("2", "P1", "MUST", "B*-off paired, 970 events at 5 keV, on and off", 970 * 2 * S3[5], "970 x 2 x 67.8 s (maxwell timing)", "D", "M19")
add("2", "P1", "MUST", "floor tests, 1 keV B*-off and 5 x 300 new gate events, margin", 14.5 * H, "4 (floor) + 0.5 (1 keV) + 10 margin", "G", "M19")
add("2", "C1", "MUST", "PU rho = 1, 4000 events x 4 roads", 4000 * B1EV, "4000 x 60.4 s", "M")
add("2", "C1", "MUST", "PU rho = 2, 1000 events (pre-merge dump on)", 1000 * RHO2, "1000 x 206 s", "D")
add("2", "C1", "MUST", "no-PU C'0, v1 sizes (5.4e5 events)", 5.4e5 * NOPU, "5.4e5 x 11.5 ms", "M")
add("2", "C1", "MUST", "C'_PU: 5000 events x 1 road", 5000 * SIG, "5000 x 25.2 s", "D")
add("2", "C1", "MUST", "SM Z(nunu) hit level, 2000 events x 1 road", 2000 * SIG, "2000 x 25.2 s", "D")
add("2", "C1", "MUST", "generator-level N_trig and rates", 5 * H, "", "G")
add("2", "C1", "MUST", "signal: 3 points x 400 rows on the v1 path", 3 * 400 * SIG, "1200 x 25.2 s", "D")
add("2", "C1", "MUST", "signal: full-chain twins of the two fast-path points", 2 * 400 * SIG, "800 x 25.2 s", "D", "M21")
add("2", "C2", "MUST", "V4-5 brute force, 100 events", 100 * 0.3 * H, "100 x 0.3 CPU-h", "G")
add("2", "C2", "MUST", "T_seed 4 -> 2 regression (500 rho=1 + 200 rho=2 events)", 500 * 4 * TRIAL * 3 + 200 * 2 * 74 * 3, "trials x 3", "G")
add("2", "C2", "MUST", "V4-4: 20 jobs x 2 reruns x 2 nodes", 20 * 4 * 300, "80 x 5 min", "M")
add("2", "B2", "MUST", "rho = 2 RSS, pre-merge size, thinning N_eff per rung, frozen-road timing", 10 * H, "", "G")
add("2", "B1", "MUST", "enrichment pilot: 1e7 minimum-bias interactions at generator level", 1e7 * MINBIAS, "1e7 x 2.5 ms", "M", "M6")
add("2", "B1", "MUST", "enrichment pilot: 1e6 unbiased no-PU events each for DIF and the three NI radii (f_k, H, sagitta bound)", 4e6 * NOPU, "4e6 x 11.5 ms", "M", "M6")
PILOT_HS = 2.3e6
add("2", "B4", "MUST", "pilot: N_t x H before the freeze for the largest term, 2.3e6 no-PU Z(nunu)+jets events", PILOT_HS * NOPU_HS, "2.3e6 x 45 ms", "G", "N1/N7")
add("2", "B1", "MUST", "enrichment pilot: 1000 overlays of near-pass events", 1000 * SIG, "1000 x 25.2 s", "D", "M3/M6")
add("2", "B3", "MUST", "time-tag: hit-level late-hit density on the C1 events", 5 * H, "", "G", "M16")
add("2", "all", "MUST", "unit-cost timing jobs (no-PU hard scatter, signal row, MLM, 60-100-parameter workspace)", 5 * H, "", "G", "M19")
# Phase 3 (development, signal blind)
add("3", "B1", "MUST", "Geant4 hand-over tests, small P_geo and overlay samples", 60 * H, "", "G")
add("3", "B1", "MUST", "pile-up-vertex secondaries test: 1000 PU events with Geant4 secondaries", 1000 * (B1EV + 2.7), "1000 x (60.4 + 2.7) s", "D", "M26")
add("3", "B4", "MUST", "MET model, biased multijet generation, small hit samples", 50 * H, "", "G")
add("3", "B3", "MUST", "conditionals on development samples", 10 * H, "", "G")
add("3", "B2", "MUST", "occupancy estimator on the Phase-2 PU samples", 10 * H, "", "G")
add("3", "T1", "MUST", "workspace on v1 counts; zero-count tests (limiting case, large count, coverage); injection", 60 * H, "30 (v1) + 30", "G", "M1/M7")
add("3", "dev", "MUST", "enlarged development closure samples (idle pre-freeze capacity)", 100 * H, "about 5,960 B1-type events", "G", "C(N-C-6)")
# Phase 4a (production, after the freeze)
add("4a", "B2", "MUST", "PU rho = 1 direct, 24000 events x 4 roads", 24000 * B1EV, "24000 x 60.4 s", "M")
add("4a", "B2", "MUST", "PU rho = 2 with pre-merge candidates, 3000 events", 3000 * RHO2, "3000 x 206 s", "D")
add("4a", "B1", "MUST", "Geant4: realistic spectra, discs, I/O", 15 * H, "", "G")
add("4a", "B1", "MUST", "QGSP_BERT and composition variations: Geant4 + 5e6 no-PU events each", 2 * (10 * H + 5e6 * NOPU), "2 x (10 CPU-h + 5e6 x 11.5 ms)", "G", "M19")
c_si_h = sum(alloc[t] * C_SI[t] for t in SI)
g4_h = (alloc["DIF"] / G4_DEC + 3 * alloc["NI 22 mm"] / G4_NI) * G4GUN
add("4a", "B1", "MUST", f"no-PU pool, DIF and NI share: {m_si:.3g} events, chain {m_si * NOPU / H:.0f} + Geant4 vertices {g4_h / H:.0f} CPU-h", c_si_h,
    f"{m_si:.3g} x 11.5 ms + ({alloc['DIF']:.3g} / 0.011 + {3 * alloc['NI 22 mm']:.3g} / 0.042) guns x 0.134 ms", "D", "N8")
add("4a", "B4", "MUST", f"no-PU pool, SM hard-scatter share: {m_sm:.3g} events", m_sm * NOPU_HS, f"{m_sm:.3g} x 45 ms", "G", "N8")
N_OVL = 9000 + 3 * 1500 + 4 * 1000     # DIF (derivation + test); NI x 3 (rung split); gamma, V0, PV pair, looper (unbiased)
add("4a", "B1", "MUST", "overlays: DIF 9000 + NI 3 x 1500 + 4 sub-topologies x 1000 unbiased events", N_OVL * SIG, f"{N_OVL} x 25.2 s", "D", "N8/N2")
SCAN = 2e6
add("4a", "B1", "MUST", "no-PU scan slice for the test overlays (disjoint seed stream), 2e6 events", SCAN * (NOPU + G4GUN / G4_DEC), "2e6 x (11.5 + 12.2) ms", "D", "N17")
add("4a", "B2", "MUST", "crossing test rungs: re-analysis of the direct, overlay and hit-level samples", 5 * H, "", "G", "N5")
add("4a", "B3", "MUST", "conditionals, vertex veto, stability across rungs, time-tag closure (re-analysis)", 25 * H, "20 + 5", "G", "M16")
# N2: test half sized where v1 has a count: evaluable needs N_eff >= 24 at R06 (F = 2, s_P = 0.1); the sample is sized for an
# expected count of 31, which gives at least 24 with probability 0.91 (Poisson; printed in [11]). v1 presel-weighted counts at R06
# and class events (background.json -> sm.<p>.rows, n_class_events; read this session):
SM_R06 = {"Z(nunu)+j": (32.300, 2000), "W(tau_h)": (8.957, 1625), "W(tau_l)": (3.035, 375), "tt 1l": (5.193, 2000)}
N_EVAL, N_TARGET = 24, 31


def hit_need(p, target=N_TARGET):
    n, m = SM_R06[p]
    return 2 * math.ceil(target / (n / m))


HIT_EXTRA = {p: max(0, hit_need(p) - 2000) for p in ("W(tau_h)", "W(tau_l)", "tt 1l")}
N_HIT = 38000 + sum(HIT_EXTRA.values())
add("4a", "B4", "MUST", "hit level: 11 new processes x 2000 + Z(nunu) 10000 + 3 x 2000 (v2 sizes)", 38000 * SIG, "38000 x 25.2 s", "D")
for p_, x_ in HIT_EXTRA.items():
    add("4a", "B4", "MUST", f"hit level: {p_} raised to {2000 + x_} events (test half evaluable at R06)", x_ * SIG, f"{x_} x 25.2 s", "D", "N2")
add("4a", "B4", "MUST", "multijet generator level, 1e7 biased events", 1e7 * SHOWER_ZJ, "1e7 x 23.4 ms (shower alone)", "D", "M19")
add("4a", "B4", "MUST", "multijet loose population through the no-PU chain, 1e6 events", 1e6 * NOPU_HS, "1e6 x 45 ms", "G", "M33")
add("4a", "S1", "MUST", "signal full chain, 40 points x 2000 rows", 80000 * SIG, "80000 x 25.2 s", "D")
add("4a", "T1", "MUST", "expected results with v1 placeholders", 20 * H, "", "G")
add("4a", "T1", "MUST", "coverage test: null distributions for m' = 0..6 at 2 points", 2 * 7 * 8 * TOYS1000, "2 x 7 x 8 x 652 s", "G", "M1")
add("4a", "B5", "SHOULD", "FULL: 20 roads on 8000 SM + 500 PU events", 8000 * 19 * TRIAL + 500 * 16 * TRIAL, "(8000 x 19 + 500 x 16) x 11.7 s", "M")
add("4a", "B5", "SHOULD-red", "REDUCED: 8 roads on 6000 SM + 20 roads on 500 PU events", 6000 * 7 * TRIAL + 500 * 16 * TRIAL, "(6000 x 7 + 500 x 16) x 11.7 s", "M")
add("4a", "B5", "SHOULD-both", "hard-scatter T(dphi) on the no-PU samples (road rotation, inline in the pool jobs)", 10 * H, "", "G", "M31")
add("4a", "B5", "SHOULD-both", "sideband prototype (moved from Phase 3 into the production window)", 20 * H, "", "G", "N18")
add("4a", "B6", "SHOULD-both", "variation switches, PU-hit inefficiency (moved from Phase 3 into the production window)", 10 * H, "", "G", "N18")
add("4a", "B6", "SHOULD", "FULL: bkg 7 var x 1000 ev; signal 6 pts x 500 rows x 6 var; Stage-3 material",
    7 * 1000 * B1EV + 6 * 500 * 6 * SIG + 2 * 2 * 500 * (s3_at[1.5] + s3_at[3] + s3_at[5]), "see text", "D")
add("4a", "B6", "SHOULD-red", "REDUCED: bkg 7 var x 600 ev; signal 4 pts x 300 rows x 6 var; Stage-3 material",
    7 * 600 * B1EV + 4 * 300 * 6 * SIG + 2 * 2 * 300 * (s3_at[1.5] + 2 * s3_at[3] + s3_at[5]), "points E200/1.5, E500/3, E500/5, E1000/3", "D", "M13")
add("4a", "B6", "SHOULD", "FULL: nominal partners of the varied samples (1000 bkg events, 6 x 500 signal rows)", 1000 * B1EV + 6 * 500 * SIG, "1000 x 60.4 s + 3000 x 25.2 s", "D", "M17")
add("4a", "B6", "SHOULD-red", "REDUCED: nominal partners (600 bkg events, 4 x 300 signal rows)", 600 * B1EV + 4 * 300 * SIG, "600 x 60.4 s + 1200 x 25.2 s", "D", "M17")
add("4a", "B6", "SHOULD-both", "variations propagated to single-interaction and SM terms: 4 x (2e6 + 5e5) no-PU events",
    4 * (2e6 * NOPU + 5e5 * NOPU_HS), "4 x (2e6 x 11.5 ms + 5e5 x 45 ms)", "G", "M12")
add("4a", "B7", "SHOULD-both", "toy acceptance for cosmics, halo, beam gas", 5 * H, "", "G")
# Phase 4b/4c, 5
add("4b", "T2", "MUST", "ranking: 16 selections x 40 points asymptotic", 16 * 40 * SCAN20, "640 x 10.4 s", "D")
add("4b", "T2", "MUST", "background-side bootstrap: 50 replicas x 5 selections x 20 points", 50 * 5 * 20 * SCAN20, "5000 x 10.4 s", "D", "M29")
NFT, NCHK = 11, 3                   # f_T grid values per selection; exact-toy check points per selection (C-1)
add("4b", "T1", "MUST", "toys pass 1, parametrised in f_T: 5 selections x 11 f_T x 8 signal values x 1000", 5 * NFT * 8 * TOYS1000, "440 x 652 s", "G", "C-1")
add("4b", "T1", "MUST", "toys pass 1, exact-toy check: 5 selections x 3 points x 8 mu x 1000", 5 * NCHK * 8 * TOYS1000, "120 x 652 s", "G", "C-1")
add("4c", "T1", "MUST", "toys pass 2, parametrised in f_T: 3 selections x 11 f_T x 8 signal values x 1000", 3 * NFT * 8 * TOYS1000, "264 x 652 s", "G", "C-1")
add("4c", "T1", "MUST", "toys pass 2, exact-toy check: 3 selections x 3 points x 8 mu x 1000", 3 * NCHK * 8 * TOYS1000, "72 x 652 s", "G", "C-1")
add("4c", "T1", "MUST", "coverage at injected mu: 500 pseudo-experiments x 2 points x 16 fits", 500 * 2 * 16 * FIT, "16000 x 0.12 s", "D", "M8")
add("4c", "MVA", "MUST", "BDT cross-check; dE/dx forgone-gain ratio", 7 * H, "5 + 2", "G", "M30")
add("5", "figs", "MUST", "figures, reproduction package tests", 10 * H, "", "G")

print("\n[3] budget lines")
print("| phase | item | priority | what | CPU-h | arithmetic | prov. | finding |")
print("|---|---|---|---|---|---|---|---|")
for p, i, pr, lab, h, a, pv, f in items:
    print(f"| {p} | {i} | {pr} | {lab} | {h:.1f} | {a} | {pv} | {f} |")


def tot(pred):
    return sum(h for p, i, pr, lab, h, a, pv, f in items if pred(p, i, pr))


def is_must(pr):
    return pr == "MUST"


def in_red(pr):
    return pr in ("SHOULD-red", "SHOULD-both")


def in_full(pr):
    return pr in ("SHOULD", "SHOULD-both")


def sh_red(p, i, pr):
    return in_red(pr)


def sh_full(p, i, pr):
    return in_full(pr)


PH = ["2", "3", "4a", "4b", "4c", "5"]
print("\n[4] totals")
for ph in PH:
    print(f"  phase {ph}: MUST {tot(lambda p, i, pr: p == ph and is_must(pr)):.0f}"
          f" | SHOULD full {tot(lambda p, i, pr: p == ph and sh_full(p, i, pr)):.0f}"
          f" | SHOULD reduced {tot(lambda p, i, pr: p == ph and sh_red(p, i, pr)):.0f}")
must = tot(lambda p, i, pr: is_must(pr))
shf = tot(sh_full)
shr = tot(sh_red)
print(f"  MUST-only {must:.0f}; MUST + SHOULD reduced {must + shr:.0f}; MUST + SHOULD full {must + shf:.0f}")
print(f"  SHOULD reduced {shr:.0f}; SHOULD full {shf:.0f}; DP1 + DP2 saving {shf - shr:.0f}")
for it in ["C1", "C2", "P1", "S1", "S2", "B1", "B2", "B3", "B4", "T1", "T2", "MVA", "dev", "all", "figs", "B5", "B6", "B7"]:
    print(f"  {it}: MUST {tot(lambda p, i, pr: i == it and is_must(pr)):.0f}"
          f" | SHOULD full {tot(lambda p, i, pr: i == it and sh_full(p, i, pr)):.0f}"
          f" | reduced {tot(lambda p, i, pr: i == it and sh_red(p, i, pr)):.0f}")
prod_must_bkg = tot(lambda p, i, pr: p == "4a" and is_must(pr) and i != "S1")
prod_s1 = tot(lambda p, i, pr: p == "4a" and i == "S1")
prod_red = tot(lambda p, i, pr: p == "4a" and sh_red(p, i, pr))
prod_full = tot(lambda p, i, pr: p == "4a" and sh_full(p, i, pr))
print(f"  Phase 4a: background and T1 MUST {prod_must_bkg:.0f}; S1 chain {prod_s1:.0f}; SHOULD reduced {prod_red:.0f}; SHOULD full {prod_full:.0f}")

# ---- [5] deltas v2 -> v3 per finding (cycle 2) ---------------------------------------------------------------------------
V1 = {"MUST": 2950.0, "RED": 3275.0, "FULL": 3798.0}
V2 = {"MUST": 3968.0, "RED": 4401.0, "FULL": 4915.0, "DAYS": 57.9, "NONPROD": 44}
TOYS_V2 = (5 * 20 * 8 + 3 * 40 * 8) * TOYS1000 / H
TOYS_V3 = (5 + 3) * (NFT + NCHK) * 8 * TOYS1000 / H
RESERVE2 = TOYS_V2 - TOYS_V3          # the CPU freed by C-1: the day-15 redirection reserve (Q2), not in the totals
deltas = [   # (label, CPU-h, CPU-h on the Phase-4a critical path)
    ("N1/N7 pilot: N_t x H of the largest term before the freeze (2.3e6 no-PU Z(nunu) events; idle pre-freeze capacity)", PILOT_HS * NOPU_HS / H, 0.0),
    ("N2 hit level: W(tau_h) to %d events" % (2000 + HIT_EXTRA["W(tau_h)"]), HIT_EXTRA["W(tau_h)"] * SIG / H, HIT_EXTRA["W(tau_h)"] * SIG / H),
    ("N2 hit level: W(tau_l) to %d events" % (2000 + HIT_EXTRA["W(tau_l)"]), HIT_EXTRA["W(tau_l)"] * SIG / H, HIT_EXTRA["W(tau_l)"] * SIG / H),
    ("N2 hit level: tt 1l to %d events" % (2000 + HIT_EXTRA["tt 1l"]), HIT_EXTRA["tt 1l"] * SIG / H, HIT_EXTRA["tt 1l"] * SIG / H),
    ("N8/N2/C-2 overlays: %d events instead of 42,000" % N_OVL, (N_OVL - 42000) * SIG / H, (N_OVL - 42000) * SIG / H),
    ("N17 no-PU scan slice for the test overlays", SCAN * (NOPU + G4GUN / G4_DEC) / H, SCAN * (NOPU + G4GUN / G4_DEC) / H),
    ("N5 crossing test rungs (re-analysis)", 5.0, 5.0),
    ("N8 pool: Geant4 vertices inside the pool envelope (600 + 65 = 665 CPU-h), allocation re-run", c_si_h / H + m_sm * NOPU_HS / H - C_POOL_V2 - G4_V2, c_si_h / H + m_sm * NOPU_HS / H - C_POOL_V2 - G4_V2),
    ("C-1 toys parametrised in f_T in both passes, with exact-toy checks (v2: %.0f)" % TOYS_V2, -RESERVE2, 0.0),
    ("N9 secondaries: truth-attributed counting on the same 17.5 CPU-h sample; N1 ceiling and completeness tests, N16 prompt-population time-tag closure: re-analysis", 0.0, 0.0),
    ("N15 S1 string propagation moved from Phase 2 to Phase 3 (after A is fixed)", 0.0, 0.0),
    ("N18 B5 and B6 prototypes moved from Phase 3 into the production window (SHOULD)", 0.0, 30.0),
]
print("\n[5] deltas v2 -> v3, per finding (CPU-h; days = effect on the Phase-4a critical path at the production capacity)")
for lab, d, dcrit in deltas:
    print(f"  {d:+8.1f} CPU-h  {dcrit / CAP_PROD:+5.2f} d   {lab}")
print(f"  sum {sum(d for _, d, _ in deltas):+.1f} CPU-h; critical path {sum(c for _, _, c in deltas) / CAP_PROD:+.2f} d")
print("  calendar, non-production days: N18 Phase 3 from 9 to 12 days (+3); C-5 Phase 2 from 7 to 5 (-2) and Phase 5 from 7 to 4 (-3)")
print(f"  v1 -> v2 -> v3: MUST {V1['MUST']:.0f} -> {V2['MUST']:.0f} -> {must:.0f} ({must - V2['MUST']:+.0f}); reduced {V1['RED']:.0f} -> {V2['RED']:.0f} -> {must + shr:.0f}"
      f" ({must + shr - V2['RED']:+.0f}); full {V1['FULL']:.0f} -> {V2['FULL']:.0f} -> {must + shf:.0f} ({must + shf - V2['FULL']:+.0f})")
print(f"  day-15 redirection reserve (CPU freed by C-1, not in the totals): {RESERVE2:.0f} CPU-h = {RESERVE2 / CAP_PROD:.1f} production days if drawn")

# ---- [6] contingency from provenance --------------------------------------------------------------------------------------
FRAC = {"M": 0.10, "D": 0.30, "G": 1.00}
print("\n[6] provenance and contingency (reduced variant)")
cont = 0.0
for pv in "MDG":
    s = sum(h for p, i, pr, lab, h, a, v, f in items if v == pv and (is_must(pr) or sh_red(p, i, pr)))
    cont += FRAC[pv] * s
    print(f"  provenance {pv}: {s:.0f} CPU-h, carried at {FRAC[pv]:.0%} -> {FRAC[pv] * s:.0f}")
RESERVE = 24000 * B1EV / H
print(f"  contingency from provenance {cont:.0f} CPU-h; fresh-sample reserve (one B2 direct sample) {RESERVE:.0f} CPU-h")
print(f"  reduced total with both: {must + shr + cont + RESERVE:.0f} CPU-h; stop-and-ask threshold 1.3 x {must + shr:.0f} = {1.3 * (must + shr):.0f}")
print(f"  thresholds for the other variants: MUST only 1.3 x {must:.0f} = {1.3 * must:.0f}; full 1.3 x {must + shf:.0f} = {1.3 * (must + shf):.0f};"
      f" envelope alternative (Q4): {must + shr:.0f} + {cont:.0f} = {must + shr + cont:.0f}, threshold {1.3 * (must + shr + cont):.0f}")
print("  conditional draws (none is inside the approved figure; each is reported as an overrun when drawn and counts toward the threshold):")
for lab, h in (("day-15 redirection reserve (pre-approved by the Q2 default)", RESERVE2),
               ("exact toys in both passes if the f_T check of pass 1 fails (upper value; the check toys are reused)",
                (5 * 20 * 8 - 5 * NCHK * 8) * TOYS1000 / H + 3 * 40 * 8 * TOYS1000 / H - 3 * (NFT + NCHK) * 8 * TOYS1000 / H),
               ("DIF test overlays raised to 7,750 unbiased events if the enrichment is below 1.7", 2750 * SIG / H),
               ("second direct pile-up sample (INVESTIGATE or bug re-test)", RESERVE),
               ("fresh test overlays after a bug (all of sample 19)", N_OVL * SIG / H),
               ("fresh hit-level test halves of the four evaluable processes", sum(hit_need(p) for p in SM_R06) / 2 * SIG / H),
               ("fresh pool slice for a B3 conditional re-test: half the Z(nunu) sample", alloc["Z(nunu)+j"] / 2 * NOPU_HS / H),
               ("  same, half the DIF sample", alloc["DIF"] / 2 * C_SI["DIF"] / H)):
    print(f"    {h:6.0f} CPU-h  {lab}")
print(f"  S1 at 4000 rows (GA-2): +{80000 * SIG / H + 5 * 2000 * s3_sum / H:.0f} CPU-h = {(80000 * SIG / H + 5 * 2000 * s3_sum / H) / CAP_PROD:.1f} production days")
print(f"  S4 if requested: finder rerun on background samples = {(24000 * 4 * TRIAL + 3000 * 2 * 74 + (N_OVL + N_HIT) * TRIAL) / H:.0f} CPU-h")
print(f"  Q5 alternative: Stage 2 and Stage 3 signal samples after the freeze: {(5 * 250e3 * MLM + 4 * 1.25e6 * SHOWER + 5 * 2000 * s3_sum) / H:.0f} CPU-h = {(5 * 250e3 * MLM + 4 * 1.25e6 * SHOWER + 5 * 2000 * s3_sum) / H / CAP_PROD:.1f} production days")

# ---- [7] calendar -------------------------------------------------------------------------------------------------------------
print("\n[7] calendar (days after Gate A)")
ph2_cpu = tot(lambda p, i, pr: p == "2" and is_must(pr))
ph3_cpu = tot(lambda p, i, pr: p == "3" and is_must(pr))
string_h = 5 * 2000 * s3_sum / H
print(f"  Phase 2 CPU {ph2_cpu:.0f}: {ph2_cpu:.0f} / {CAP_DEV:.0f} = {ph2_cpu / CAP_DEV:.1f} days of the 5 available")
PRE = 5 + 12 + 2 + 2
print(f"  Phase 3 CPU {ph3_cpu:.0f} (of which the S1 string propagation {string_h:.0f}, days 12-19); capacity in Phases 2 + 3 + freeze ({PRE} days x {CAP_DEV:.0f}) = {PRE * CAP_DEV:.0f};"
      f" idle {PRE * CAP_DEV - ph2_cpu - ph3_cpu:.0f}")
print(f"  Phase 3 development effort: 3 channels x 12 days = 36 channel-days (v2: 6 x 9 = 54 with twice the allowed concurrency; PLAN: 35-50 person-days)")
FIXED = [("Phase 2 (three agents)", 5), ("Phase 3 development (three critical channels; PREREG drafted)", 12), ("freeze: 4-bot review of PREREG_v2, hash", 2), ("ITERATE allowance (freeze)", 2),
         ("4a review (4-bot + bib)", 3), ("ITERATE allowance (4a)", 2), ("4b: T2, toys, 4-bot + bib", 3), ("ITERATE allowance (4b)", 2),
         ("Gate B turnaround", 2), ("4c and 1-bot review", 3), ("Phase 5 (sections 1-6, 8-10 drafted during 4a)", 4), ("ITERATE allowance (5-bot)", 2)]
nonprod = sum(d for _, d in FIXED)
for lab, d in FIXED:
    print(f"    {d:2d} d  {lab}")
print(f"  non-production days: {nonprod} (v2: {V2['NONPROD']}) -> already above the 28 days of a 4-week target; without the four ITERATE allowances: {nonprod - 8}")
for name, cpu in [("MUST-only", prod_must_bkg), ("MUST + SHOULD reduced", prod_must_bkg + prod_red), ("MUST + SHOULD full", prod_must_bkg + prod_full)]:
    d = cpu / CAP_PROD
    s1d = prod_s1 / CAP_PROD
    print(f"  {name}: 4a background production {cpu:.0f} CPU-h = {d:.1f} days; S1 chain {prod_s1:.0f} CPU-h = {s1d:.1f} days runs during the"
          f" 4a review (5 days); total {nonprod + d:.1f} days = {(nonprod + d) / 7:.1f} weeks;"
          f" at utilisation 0.50 in production: {nonprod + cpu / CAP_DEV:.1f} days")
t4b, t4c = 5 * (NFT + NCHK) * 8 * TOYS1000 / H, 3 * (NFT + NCHK) * 8 * TOYS1000 / H
print(f"  toys 4b {t4b:.1f} + 4c {t4c:.1f} = {t4b + t4c:.1f} CPU-h (v2: {TOYS_V2:.1f}); at {CAP_PROD:.0f}/day: {t4b / CAP_PROD:.1f} and {t4c / CAP_PROD:.1f} days (inside the 3-day windows)")
print(f"  time-ordered checkpoints: decision point 1 and stop-rule checkpoint 1 at day 5; decision point 2 at day 15; freeze days 17-19; production from day {PRE};"
      f" Gate B at about day {PRE + (prod_must_bkg + prod_red) / CAP_PROD + 3 + 2 + 3 + 2 + 2:.0f}")
print(f"  old T1-g if done with nested toys: 500 x 2 x 8 x 652 s = {500 * 2 * 8 * 652 / H:.0f} CPU-h (not done)")

# ---- [8] storage (GB) -----------------------------------------------------------------------------------------------------------
MB_EV = 0.52
pu_events = (4000 + 5000 + 2000 + 1200 + 800 + 1000 + 1000) + (24000 + N_OVL + N_HIT + 80000) + (8 * 600 + 4 * 300 * 7) + 5960
rho2_events = 1000 + 3000 + 200
nopu_events = m_si + m_sm + 5.4e5 + 4e6 + PILOT_HS + SCAN + 1e7 + 1e6 + 4 * 2.5e6
sto = {
    "PU-200 chain + trial records (%d events x 0.52 MB)" % pu_events: pu_events * MB_EV / 1024,
    "rho = 2 events with dumps (%d x 4.0 MB)" % rho2_events: rho2_events * 4.0 / 1024,
    "hit dumps for 10,000 events (C2 700, B5 6,500, occupancy model and time tag 2,800; 2.4 MB each)": 10000 * 2.4 / 1024,
    "rho = 2 pre-merge candidates (planning value; cap 400)": 200.0,
    "no-PU samples as per-event summaries (%.3g x 50 B) + full records of R04 passers and near-pass events" % nopu_events: nopu_events * 50 / 1e9 + 25,
    "Stage 2: 1.75e6 LHE events, 5 shower variants": 1.75e6 * (0.72 + 5 * 1.05) / 1e6,
    "Stage 3 (8 kB x 85000 rows)": 85000 * 8 / 1e6,
    "Geant4 vertices, job logs, pyhf outputs, toy distributions": 8.0,
    "crossing-test variables (fit probability, 2S, shape) of the R05-R06 candidates: 49.72 x 96,000 x 64 B, x 3 for overlays, hit level, development": 3 * 49.72 * 96000 * 64 / 1e9,
    "repo bundles (7 + gates)": 10.0,
}
print("\n[8] storage")
for k, v in sto.items():
    print(f"  {k}: {v:.1f} GB")
print(f"  storage total {sum(sto.values()):.0f} GB (with the pre-merge cap of 400 GB: {sum(sto.values()) + 200:.0f} GB)")
print(f"  no-PU full records if kept (8.2 kB x {nopu_events:.3g}): {8.2e3 * nopu_events / 1e9:.0f} GB -> not kept")
print(f"  jobs: reduced total / 0.4 h per job = {(must + shr) / 0.4:.0f}; Argo overhead 17 s each = {(must + shr) / 0.4 * 17 / H:.0f} slot-h")

# ---- [9] zero-count floors (M6) ----------------------------------------------------------------------------------------------------
print("\n[9] zero-count floors: events in 3 ab^-1 that a zero count still allows (before pile-up factors and conditionals)")
print("  convention: 68 % upper value 1.14 N_t / M_t (= -ln 0.32); predictive mean N_t / M_t")
U68 = -math.log(0.32)
v1_m = {"PV pair": 1e7, "DIF": 1e7, "gamma": 1e7, "V0": 1e7}
print("  v1 plan (1e7 for four topologies, 1e6 per SM process):")
f_v1 = {t: U68 * NTRIG * RATE[t] / v1_m[t] for t in v1_m}
f_v1_sm = sum(U68 * n / 1e6 for n in SM_NTRIG.values())
print("   ", {t: round(v, 2) for t, v in f_v1.items()}, f"sum {sum(f_v1.values()):.1f}; SM sum {f_v1_sm:.1f} (Z(nunu) {U68 * SM_NTRIG['Z(nunu)+j'] / 1e6:.1f})")
sq = sum(math.sqrt(RATE[t]) for t in v1_m)
f_sq = {t: U68 * NTRIG * RATE[t] / (4e7 * math.sqrt(RATE[t]) / sq) for t in v1_m}
print(f"    same 4e7 events by sqrt(rate): sum {sum(f_sq.values()):.1f}")


def floor_table(c_h, tt=None):
    al = allocate(c_h, tt=tt)
    rows = [(t, n, al[t], U68 * n / al[t], n / al[t]) for t, n, c in (terms if tt is None else tt)]
    return rows


rows_v2 = floor_table(C_POOL_V2, tt=terms_v2)
print(f"  v2 routes (PV pairs, gamma, V0, loopers as gun terms beside the SM real events; pool 600 CPU-h + 65 Geant4): sum of floors {sum(r[3] for r in rows_v2):.1f},"
      f" of which PV pairs {[r[3] for r in rows_v2 if r[0] == 'PV pair'][0]:.1f}, gamma + looper + V0 {sum(r[3] for r in rows_v2 if r[0] in ('gamma', 'looper', 'V0')):.1f}")
for c_h in (C_POOL, C_POOL + RESERVE2, 2 * C_POOL):
    rows = floor_table(c_h)
    s68 = sum(r[3] for r in rows)
    si68 = sum(r[3] for r in rows if r[0] in SI)
    print(f"  v3 routes, pool {c_h:.0f} CPU-h (chain + Geant4 vertices): sum of floors {s68:.1f} (DIF and NI {si68:.1f}, SM {s68 - si68:.1f}); sum of means {sum(r[4] for r in rows):.1f}")
print(f"  | term | N_t in 3 ab^-1 | cost per event (ms) | M_t planned | transfer factor N_t/M_t | floor at 68 % (1.14 N/M) |   (pool {C_POOL:.0f} CPU-h)")
rows = floor_table(C_POOL)
cost = {t: c for t, n, c in terms}
for t, n, m, f68, mean in rows:
    print(f"  | {t} | {n:.3g} | {1e3 * cost[t]:.1f} | {m:.3g} | {mean:.2f} | {f68:.2f} |")
EVAL4 = ("Z(nunu)+j", "W(tau_h)", "W(tau_l)", "tt 1l")
print(f"  events in the pool: DIF and NI {m_si:.3g} ({c_si_h / H:.0f} CPU-h), SM {m_sm:.3g} ({m_sm * NOPU_HS / H:.0f} CPU-h)")
print(f"  floors by group: DIF {rows[0][3]:.2f}; NI (three) {sum(r[3] for r in rows[1:4]):.2f}; the four SM processes with an evaluable closure {sum(r[3] for r in rows if r[0] in EVAL4):.2f};"
      f" the eight proxied processes {sum(r[3] for r in rows if r[0] in SM_NTRIG and r[0] not in EVAL4):.2f}")
print(f"  N_trig share: four evaluable processes {sum(SM_NTRIG[p] for p in EVAL4) / NTRIG:.3f}; eight proxied processes {sum(v for p, v in SM_NTRIG.items() if p not in EVAL4) / NTRIG:.3f}")
print(f"  pilot: one H count in 2.3e6 Z(nunu) no-PU events = {SM_NTRIG['Z(nunu)+j'] / PILOT_HS:.1f} events in 3 ab^-1; in 1e6 DIF events = {NTRIG * RATE['DIF'] / 1e6:.0f}")
print(f"  v1 best B84 against the v3 zero-count floor: log10(1.2346e6 / {sum(r[3] for r in rows):.1f}) = {math.log10(1.2346e6 / sum(r[3] for r in rows)):.2f} decades")
random.seed(20261113)
means = [r[4] for r in rows]
draws = sorted(sum(mu * random.expovariate(1.0) for mu in means) for _ in range(200000))
q = lambda f: draws[int(f * len(draws))]
print(f"  predictive distribution of the summed floor (each term N/M x Exp(1)): 16 % {q(0.16):.1f}, median {q(0.5):.1f}, 84 % {q(0.84):.1f},"
      f" mean {sum(means):.1f}; sigma_ln = 0.5 ln(q84/q16) = {0.5 * math.log(q(0.84) / q(0.16)):.2f}")
print(f"  enrichment G needed to bring the summed 68 % floor to 10 / 1 / 0.11 events: {sum(r[3] for r in rows) / 10:.1f} / {sum(r[3] for r in rows):.0f} / {sum(r[3] for r in rows) / 0.11:.0f}")
print(f"  road-multiplicity ceiling for unoriented single interactions: 2 pi / 0.30 = {2 * math.pi / 0.30:.1f}")


def trigamma(x):
    s = 0.0
    while x < 30:
        s += 1.0 / (x * x)
        x += 1
    return s + 1 / x + 1 / (2 * x * x) + 1 / (6 * x ** 3) - 1 / (30 * x ** 5)


print("  sd of ln(lambda) for lambda ~ Gamma(m + 1):", {m: round(math.sqrt(trigamma(m + 1)), 2) for m in (0, 1, 2, 3, 5, 10, 100)})
print("  quantiles of Gamma(1) (m = 0): 16 %% %.3f, median %.3f, 68 %% %.3f, 84 %% %.3f, 95 %% %.3f" % (
    -math.log(0.84), math.log(2), U68, -math.log(0.16), -math.log(0.05)))

# ---- [9b] projection per outcome (N7) ----------------------------------------------------------------------------------------------
# One bin. Background = sum_t kappa_t x Gamma(m_t + 1) (zero-count floors, or a counted ceiling H with m_H events)
# + an EST pile-up term (log-normal, censored at its no-credit value, N6). Expected CLs limit on the signal yield from
# the marginal (hybrid) distribution, as in [10] but for the summed predictive distribution (Monte Carlo over the rates).


def pmf_pred(gam, lnn=(), nd=3000, seed=7):
    rnd = random.Random(seed)
    bs = []
    for _ in range(nd):
        b = sum(k * rnd.gammavariate(m + 1, 1.0) for k, m in gam)
        for med, sw, capv in lnn:
            b += min(med * math.exp(sw * rnd.gauss(0, 1)), capv)
        bs.append(b)
    kmax = int(max(bs) + 8 * math.sqrt(max(bs)) + 20)
    pmf = [0.0] * (kmax + 1)
    for b in bs:
        p = math.exp(-b)
        for k in range(kmax + 1):
            pmf[k] += p
            p *= b / (k + 1)
    bs.sort()
    return [x / nd for x in pmf], (bs[int(0.16 * nd)], bs[nd // 2], bs[int(0.84 * nd)])


def quant_pmf(pmf, f):
    c = 0.0
    for k, p in enumerate(pmf):
        c += p
        if c >= f:
            return k
    return len(pmf) - 1


def s95_pmf(pmf, nobs):
    den = sum(pmf[: nobs + 1])

    def cls(sig):
        tot_, c, p = 0.0, 0.0, math.exp(-sig)
        cdf = []
        for j in range(nobs + 1):
            c += p
            cdf.append(c)
            p *= sig / (j + 1)
        for k in range(nobs + 1):
            tot_ += pmf[k] * cdf[nobs - k]
        return tot_ / den
    lo, hi = 0.0, 60.0 + 12.0 * (nobs + 1)
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if cls(mid) > 0.05:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def pois_pmf(k, mu):
    if mu <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(k * math.log(mu) - mu - math.lgamma(k + 1))


def s95_fixed(bfix):
    n, c = 0, pois_pmf(0, bfix)
    while c < 0.5:
        n += 1
        c += pois_pmf(n, bfix)
    pmf = [pois_pmf(k, bfix) for k in range(n + 1)]
    return s95_pmf(pmf, n)


PLAN_REACH = [(0.0, 1026.0), (1.0, 971.0), (10.0, 866.0), (30.0, 799.0), (100.0, 717.0), (1e3, 548.0), (1e4, 393.0)]   # PLAN l.121, sigma_ln = 0 row (EST, v1 efficiencies)
MAPR = [(s95_fixed(b), r) for b, r in PLAN_REACH]


def reach_of(s95v):
    """reach read from the plan's sigma_ln = 0 row at equal one-bin expected limit (linear in ln s95)"""
    for (s1, r1), (s2, r2) in zip(MAPR, MAPR[1:]):
        if s95v <= s2:
            return r1 + (r2 - r1) * (math.log(max(s95v, s1)) - math.log(s1)) / (math.log(s2) - math.log(s1))
    return MAPR[-1][1]


print("\n[9b] projection per outcome: one-bin expected CLs limit on the signal yield and the reach read from the plan's table (EST)")
print("  mapping s95 -> reach (PLAN l.121, sigma_ln = 0 row; fixed B, median expected limit):", [(round(a, 1), int(b)) for a, b in MAPR])
kap = [(r[4], 0) for r in rows]
kz = SM_NTRIG["Z(nunu)+j"] / alloc["Z(nunu)+j"]
r07 = 35 / 48000.0
PU_R07 = NTRIG * r07                                   # direct v1 rate at R07
PU_R08 = (PU_R07 / (0.2470 / r07), PU_R07 / (49.72 / 0.2470))   # width-step fall x339 (R06->R07) and x201 (R05->R06)
CHI = (2 / 35.0, 32 / 126.0, 12 / 32.0)                # v1 conditional fit-probability fractions R09, R10, R11 (D4 l.266, UNVERIFIED)
PU_R09 = tuple(x * CHI[0] for x in PU_R08)
PU_R11 = tuple(x * CHI[0] * CHI[1] * CHI[2] for x in PU_R08)
PU_NC = NTRIG * U68 / 96000                            # no-credit value of the pile-up term
print(f"  EST pile-up medians from v1 numbers: R07 direct {PU_R07:.3g}; R08 {PU_R08[0]:.0f}-{PU_R08[1]:.0f} (width-step fall x339 / x201);"
      f" R09 {PU_R09[0]:.1f}-{PU_R09[1]:.1f}; R11 {PU_R11[0]:.2f}-{PU_R11[1]:.2f}; R14: no v1 number, at most the R11 value; no-credit value {PU_NC:.0f}")
W_PU = {"R08": 0.43, "R09": 0.59, "R11": 1.29, "R14": 2.47}    # s_tot of [12], occupancy model, no crossing test
for rr, med in (("R08", PU_R08), ("R09", PU_R09), ("R11", PU_R11), ("R14", PU_R11)):
    print(f"    {rr}: B50 {med[0]:.3g}-{med[1]:.3g}; B84 = B50 x exp({W_PU[rr]}) = {med[0] * math.exp(W_PU[rr]):.3g}-{med[1] * math.exp(W_PU[rr]):.3g}"
          f" (with crossing tests, s_tot 0.45-0.47: {med[0] * math.exp(0.46):.3g}-{med[1] * math.exp(0.46):.3g})")
pu9 = 0.5 * (PU_R09[0] + PU_R09[1])
pu8 = 0.5 * (PU_R08[0] + PU_R08[1])
pmf_v2, _ = pmf_pred([(r[4], 0) for r in rows_v2])
print(f"  check against the constructive review (v2 floors, all empty): s95 = {s95_pmf(pmf_v2, quant_pmf(pmf_v2, 0.5)):.1f} (review: 24.1)")
kap_noz = [(r[4], 0) for r in rows if r[0] != "Z(nunu)+j"]
SCEN = [("floors only (every count zero, every ceiling H empty, no pile-up term)", kap, ()),
        ("R09-like: floors + EST pile-up median %.0f (s_tot 0.59)" % pu9, kap, ((pu9, 0.59, PU_NC),)),
        ("R08-like: floors + EST pile-up median %.0f (s_tot 0.43)" % pu8, kap, ((pu8, 0.43, PU_NC),))]
for mh in (3, 10, 30, 100):
    SCEN.append(("R09-like, Z(nunu) at its ceiling with m_H = %d counts" % mh, kap_noz + [(kz, mh)], ((pu9, 0.59, PU_NC),)))
print("  | outcome | B16 / B50 / B84 | sigma_ln = 0.5 ln(B84/B16) | s95 median [16 %, 84 %] | reach, EST (GeV) |")
for lab, gam, lnn in SCEN:
    pmf, (b16, b50, b84) = pmf_pred(gam, lnn)
    lim = [s95_pmf(pmf, quant_pmf(pmf, f)) for f in (0.16, 0.5, 0.84)]
    print(f"  | {lab} | {b16:.0f} / {b50:.0f} / {b84:.0f} | {0.5 * math.log(b84 / b16):.2f} | {lim[1]:.1f} [{lim[0]:.1f}, {lim[2]:.1f}] | {reach_of(lim[1]):.0f} [{reach_of(lim[2]):.0f}, {reach_of(lim[0]):.0f}] |")
b1000 = kz * 1001 + pu9 + sum(k for k, m in kap_noz)
print(f"  m_H = 1000: B about {b1000:.0f}, fixed-B s95 = {s95_fixed(b1000):.0f}, reach {reach_of(s95_fixed(b1000)):.0f} GeV")
print(f"  one-bin limit with every zero-count term dropped: {-math.log(0.05):.2f}; with the floors: {s95_pmf(pmf_pred(kap)[0], quant_pmf(pmf_pred(kap)[0], 0.5)):.1f}")
for c_h in (C_POOL + RESERVE2, 2 * C_POOL):
    kp = [(r[4], 0) for r in floor_table(c_h)]
    pmf, (b16, b50, b84) = pmf_pred(kp, ((pu9, 0.59, PU_NC),))
    l50 = s95_pmf(pmf, quant_pmf(pmf, 0.5))
    print(f"  R09-like with the pool at {c_h:.0f} CPU-h, ceilings empty: B50 {b50:.0f}, s95 {l50:.1f}, reach {reach_of(l50):.0f} GeV")
pmf, (b16, b50, b84) = pmf_pred(kap_noz + [(kz, 130)], ((pu9, 0.59, PU_NC),))
l50 = s95_pmf(pmf, quant_pmf(pmf, 0.5))
print(f"  class limit of decision point 2 (B50 = 300 events): m_H = 130 gives B50 {b50:.0f}, s95 {l50:.0f}, reach {reach_of(l50):.0f} GeV")
print(f"  change of the bound against v1's best B84 of 1.2346e6: B84 = 24 -> {math.log10(1.2346e6 / 24):.1f} decades; B84 = 260 -> {math.log10(1.2346e6 / 260):.1f} decades")
print(f"  projection rule per term: max(zero-count floor, N_t x H); one counted ceiling event of Z(nunu) at the final sample size = {kz:.2f} events in 3 ab^-1")
print(f"  R07-direct baseline, size from v1 counts: pile-up direct {PU_R07:.3g} + DIF attributed 1/500 x N_t = {NTRIG * RATE['DIF'] / 500:.3g} events (order 1e5)")

# ---- [10] zero-count likelihood: one-bin analytic checks (M1) ----------------------------------------------------------------------
# One bin, one background term B = kappa * lambda, auxiliary count m = 0, lambda ~ Gamma(1) (flat prior).
# Marginal: P(n | s) = sum_k Pois(k | s) q^(n-k) (1-q), q = kappa / (1 + kappa)   [integral of Pois(n | kappa lambda) e^-lambda].
# CLs(s; n_obs) = P(n <= n_obs | s) / P(n <= n_obs | 0); s95 solves CLs = 0.05.


def cdf_hybrid(nobs, s, kappa):
    qq = kappa / (1.0 + kappa)
    return sum(pois_pmf(k, s) * (1.0 - qq ** (nobs - k + 1)) for k in range(0, nobs + 1))


def cdf_pois(nobs, mu):
    return sum(pois_pmf(k, mu) for k in range(0, nobs + 1))


def s95(nobs, cls):
    lo, hi = 0.0, 50.0 + 20.0 * (nobs + 1)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if cls(nobs, mid) > 0.05:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def quant_geo(kappa, f):
    qq = kappa / (1.0 + kappa)
    n = 0
    while 1.0 - qq ** (n + 1) < f:
        n += 1
    return n


def median_pois(mu):
    n, c = 0, pois_pmf(0, mu)
    while c < 0.5:
        n += 1
        c += pois_pmf(n, mu)
    return n


print("\n[10] one bin, one zero-count term with transfer factor kappa = N/M: expected 95 % CLs limit on the signal yield s")
print("  check of the marginal: sum_n kappa^n/(1+kappa)^(n+1) = 1 and mean = kappa:",
      [(k, round(sum((k / (1 + k)) ** n / (1 + k) for n in range(4000)), 6), round(sum(n * (k / (1 + k)) ** n / (1 + k) for n in range(4000)), 3)) for k in (0.5, 10.0)])
print("  | kappa | term dropped (lambda = 0) | fixed B = 1.14 kappa | hybrid Gamma(1): median [16 %, 84 %] | true lambda = 0.5 / 1.14 / 2 / 3: median limit of the same procedure |")
for kappa in (0.1, 1.0, 10.0, 35.0, 124.0):
    cls_h = lambda n, s, k=kappa: cdf_hybrid(n, s, k) / cdf_hybrid(n, 0.0, k)
    cls_f = lambda n, s, k=kappa: cdf_pois(n, s + U68 * k) / cdf_pois(n, U68 * k)
    hyb = [s95(quant_geo(kappa, f), cls_h) for f in (0.16, 0.5, 0.84)]
    fix = s95(median_pois(U68 * kappa), cls_f)
    tru = [s95(median_pois(lam * kappa), cls_h) for lam in (0.5, U68, 2.0, 3.0)]
    print(f"  | {kappa:g} | {-math.log(0.05):.2f} | {fix:.1f} | {hyb[1]:.1f} [{hyb[0]:.1f}, {hyb[2]:.1f}] | " + " / ".join(f"{x:.1f}" for x in tru) + " |")
print("  coverage of the hybrid limit, one bin, true signal s = 10, simulation redone in every pseudo-experiment (exact sums):")
for kappa in (1.0, 10.0):
    for lam in (0.5, U68, 2.0, 3.0):
        # m ~ Pois(lam): for m = 0 the procedure above; for m >= 1 the posterior Gamma(m+1) (negative binomial marginal)
        def cdf_nb(nobs, s, m, k=kappa):
            p = 1.0 / (1.0 + k)
            tot_ = 0.0
            for j in range(0, nobs + 1):
                pj = pois_pmf(j, s)
                if pj < 1e-15:
                    continue
                c = 0.0
                for b in range(0, nobs - j + 1):
                    c += math.exp(math.lgamma(b + m + 1) - math.lgamma(b + 1) - math.lgamma(m + 1) + (m + 1) * math.log(p) + b * math.log(1 - p))
                tot_ += pj * c
            return tot_
        cov = 0.0
        cov0 = 0.0
        for m in range(0, 14):
            pm = pois_pmf(m, lam)
            if pm < 1e-6:
                continue
            mu_true = 10.0 + lam * kappa
            cm = 0.0
            for n in range(0, int(mu_true + 12 * math.sqrt(mu_true) + 12)):
                pn = pois_pmf(n, mu_true)
                if pn < 1e-9:
                    continue
                cls = cdf_nb(n, 10.0, m) / cdf_nb(n, 0.0, m)
                if cls > 0.05:      # s = 10 not excluded: limit >= true value
                    cm += pn
            cov += pm * cm
            if m == 0:
                cov0 = cm
        print(f"    kappa {kappa:g}, true lambda {lam:.2f}: P(m = 0) = {math.exp(-lam):.2f}; coverage {cov:.3f}; given m = 0: {cov0:.3f}")

# ---- [11] closure tests: size and power (M5, M15) ----------------------------------------------------------------------------------


def Phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


print("\n[11] closure criterion (a) |ln r| <= ln F evaluated only where sigma_tot = sqrt(1/N + s_P^2) <= ln F / 3")
for F in (1.5, 2.0):
    lim = math.log(F) / 3
    nmin = {sp: (math.ceil(1.0 / (lim * lim - sp * sp)) if lim > sp else None) for sp in (0.0, 0.05, 0.10)}
    print(f"  F = {F}: ln F = {math.log(F):.3f}, sigma limit {lim:.3f}; minimum direct count N for s_P = 0 / 0.05 / 0.10: {nmin[0.0]} / {nmin[0.05]} / {nmin[0.10]}")
    for mult in (1.0, 1.5, 2.0):
        d = mult * math.log(F)
        pf = Phi((d - math.log(F)) / lim) + Phi((-d - math.log(F)) / lim)
        print(f"    at the limit precision: P(fail | true ln r = {mult} ln F) = {pf:.4f}")
    print(f"    false fail at r = 1: {2 * Phi(-3):.4f}")
print("  v1 criterion (N >= 20, s_P = 0.1) for comparison: false fail at r = 1, F = 1.5: %.3f at N = 20, %.3f at N = 30; F = 2 at N = 20: %.4f" % (
    2 * Phi(-math.log(1.5) / math.sqrt(1 / 20 + 0.01)), 2 * Phi(-math.log(1.5) / math.sqrt(1 / 30 + 0.01)), 2 * Phi(-math.log(2) / math.sqrt(1 / 20 + 0.01))))
lnr = [0.406, 0.474, -0.455, -0.954]
print(f"  retroactive v1 thinning (ln r = {lnr}): v2 criterion (a) at F = 1.5 fails at {sum(abs(x) > math.log(1.5) for x in lnr)} of 4 rungs;"
      f" diagonal chi2 with s_model = ln 1.5 = {sum(x * x for x in lnr) / math.log(1.5) ** 2:.1f} on 4 dof, p = {math.exp(-4.6) * 5.6:.3f}")
print(f"  the same under the v3 rule (sigma_tot about 0.01): rungs beyond ln 1.5 + 2 sigma = {math.log(1.5) + 0.02:.3f}: {sum(abs(x) > math.log(1.5) + 0.02 for x in lnr)} of 4;"
      f" r.m.s. of ln r = {math.sqrt(sum(x * x for x in lnr) / 4):.2f} against the cap {math.log(1.5) / 3:.3f}")

# N4 (cycle 2): rates at the declared model width. ln r = delta + eps; delta = model bias of the estimator at the test
# rung (the same in a re-test), eps ~ N(0, sigma_tot^2) statistical (new in a re-test). A "correct-as-declared"
# estimator has delta ~ N(0, s_model^2).


def inv_phi(p):
    lo, hi = -10.0, 10.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if Phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def band(lo, hi, d, sg):
    """P(lo < |delta + eps| <= hi)"""
    def cdf_abs(a):
        return Phi((a - d) / sg) - Phi((-a - d) / sg)
    return max(0.0, cdf_abs(hi) - cdf_abs(lo))


def one_rung(L, smod, sg, K, delta=None, v2rule=False):
    """Verdict probabilities of a one-rung test. v3 rule: pass |x| <= min(L, T05); FAIL |x| > min(L + 2 sg, TK);
    INVESTIGATE between; the re-test (same delta, new eps) passes if |x'| <= min(L, TK).
    v2 rule: FAIL if |x| > L (no route for (a)); (b): FAIL p < 0.05/K, INVESTIGATE p < 0.05, re-test needs p' > 0.05."""
    tau = math.sqrt(smod ** 2 + sg ** 2)
    t05, tk = inv_phi(0.975) * tau, inv_phi(1 - 0.025 / K) * tau
    if v2rule:
        lo_, up_, rt_ = min(L, t05), min(L, tk), min(L, t05)
    else:
        lo_, up_, rt_ = min(L, t05), min(L + 2 * sg, tk), min(L, tk)

    def given(d):
        p_dir = band(0.0, lo_, d, sg)
        p_inv = band(lo_, up_, d, sg)
        p_out = 1.0 - p_dir - p_inv
        p_rt_fail = 1.0 - band(0.0, rt_, d, sg)
        return p_dir, p_inv, p_out, p_out + p_inv * p_rt_fail
    if delta is not None or smod == 0.0:
        return given(delta or 0.0)
    acc = [0.0, 0.0, 0.0, 0.0]
    n = 2001
    for i in range(n):
        z = -8.0 + 16.0 * i / (n - 1)
        w = math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi) * 16.0 / (n - 1)
        g = given(z * smod)
        for j in range(4):
            acc[j] += w * g[j]
    return tuple(acc)


K_FAM = 10      # eligibility family fixed now: B1-a (DIF, NI 22, NI 30, NI 61.5), B4-c (Z(nunu), W(tau_h), W(tau_l), tt 1l), B2-a, B2-b
N2, N15 = 8, 2  # tests at F = 2 and at F = 1.5
print(f"\n  N4: the finding reproduced. v2 criterion (a) at the v2 placeholder widths, P(|ln r| > ln F) for a correct-as-declared estimator:")
for F, sm in ((1.5, 0.20), (2.0, 0.35)):
    L = math.log(F)
    p0, p1 = 2 * Phi(-L / sm), 2 * Phi(-L / math.sqrt(sm ** 2 + (L / 3) ** 2))
    print(f"    F = {F}, s_model = {sm}: {p0:.3f} at sigma_tot = 0, {p1:.3f} at the evaluable limit; over 12 tests {1 - (1 - p0) ** 12:.2f} to {1 - (1 - p1) ** 12:.2f};"
          f" at s_model = ln F: {2 * Phi(-1.0):.2f}")
print(f"  N4: v3 rule. Cap (c): s_model <= ln F / 3 = {math.log(1.5) / 3:.3f} (F = 1.5), {math.log(2) / 3:.3f} (F = 2);"
      f" a correct-as-declared estimator at the cap is outside the tolerance with probability {2 * Phi(-3):.4f}")
print(f"  K = {K_FAM}: outright (b) threshold p < {0.05 / K_FAM:.4f}, |z| > {inv_phi(1 - 0.025 / K_FAM):.3f}")
print("  per-test probabilities for a correct-as-declared estimator, one evaluable rung (direct PASS / INVESTIGATE / outright FAIL / final FAIL):")
PT = {}
for F in (1.5, 2.0):
    L = math.log(F)
    for fs in (0.0, 0.5, 1.0):
        for fsig in (0.5, 1.0):
            r_ = one_rung(L, fs * L / 3, fsig * L / 3, K_FAM)
            PT[(F, fs, fsig)] = r_[3]
            print(f"    F = {F}, s_model = {fs:.1f} x cap = {fs * L / 3:.3f}, sigma_tot = {fsig:.1f} x limit = {fsig * L / 3:.3f}:"
                  f" {r_[0]:.4f} / {r_[1]:.4f} / {r_[2]:.4f} / {r_[3]:.4f}")
print("  (the probabilities do not depend on F when s_model and sigma_tot are scaled with ln F)")
print("  battery of K = 10 independent tests, all at the same relative width (sigma_tot at the evaluable limit):")
for fs in (0.0, 0.5, 1.0):
    p = PT[(2.0, fs, 1.0)]
    any_fail = 1 - (1 - p) ** K_FAM
    elig = 1 - (1 - p / 2) ** N2 * (1 - p * p)
    retest = K_FAM * one_rung(math.log(2), fs * math.log(2) / 3, math.log(2) / 3, K_FAM)[1]
    print(f"    s_model = {fs:.1f} x cap: per test {p:.4f}; at least one FAIL {any_fail:.3f}; at least one FAIL that removes eligibility"
          f" (under-prediction in one of the 8 B1-a / B4-c tests, or both pile-up estimators) {elig:.3f}; expected re-tests {retest:.2f}")
for dv in (2.5,):
    pa = one_rung(math.log(2), math.log(2) / dv, math.log(2) / 3, K_FAM)[3]
    print(f"  alternative cap s_model <= ln F / {dv} ({math.log(1.5) / dv:.3f}, {math.log(2) / dv:.3f}): per test {pa:.4f}; at least one FAIL in ten {1 - (1 - pa) ** K_FAM:.3f};"
          f" one that removes eligibility {1 - (1 - pa / 2) ** N2 * (1 - pa * pa):.3f}; outside the tolerance by declaration {2 * Phi(-dv):.4f}")
p_v2 = one_rung(math.log(2), math.log(2) / 3, math.log(2) / 3, 12, v2rule=True)[3]
print(f"  the v2 rule at the same widths (s_model at the v3 cap, K = 12): per test {p_v2:.4f}, family {1 - (1 - p_v2) ** 12:.3f}")
print("  power, one rung at the evaluable limit, s_model at the cap in the (b) covariance; P(final PASS | true ln r = x ln F):")
for mult in (0.0, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0):
    L = math.log(2)
    r_ = one_rung(L, L / 3, L / 3, K_FAM, delta=mult * L)
    print(f"    x = {mult}: PASS {1 - r_[3]:.4f} (FAIL {r_[3]:.4f}); with sigma_tot at half the limit: PASS {1 - one_rung(L, L / 3, L / 6, K_FAM, delta=mult * L)[3]:.4f}")
rnd = random.Random(11)
L = math.log(2)
sm_, sg_ = L / 3, L / 3
c05, ck = -2 * math.log(0.05), -2 * math.log(0.05 / K_FAM)


def two_rung_level(d):
    x1, x2 = d + rnd.gauss(0, sg_), d + rnd.gauss(0, sg_)
    chi = (x1 + x2) ** 2 / (2 * (sg_ ** 2 + 2 * sm_ ** 2)) + (x1 - x2) ** 2 / (2 * sg_ ** 2)
    a = max(abs(x1), abs(x2))
    return a, chi


nfail, nmc = 0, 200000
for _ in range(nmc):
    d = rnd.gauss(0, sm_)
    a, chi = two_rung_level(d)
    if a > L + 2 * sg_ or chi > ck:
        nfail += 1
    elif a > L or chi > c05:
        a2, chi2 = two_rung_level(d)
        if a2 > L or chi2 > ck:
            nfail += 1
print(f"  two evaluable rungs with a common delta (Monte Carlo, {nmc} draws, s_model at the cap, sigma_tot at the limit): per-test final FAIL {nfail / nmc:.4f}")
p1_, p2_ = PT[(2.0, 1.0, 1.0)], nfail / nmc
print(f"  battery as planned at the cap and the limit (8 one-rung tests of B1-a and B4-c, 2 multi-rung pile-up tests): at least one FAIL {1 - (1 - p1_) ** N2 * (1 - p2_) ** N15:.3f};"
      f" at least one FAIL that removes eligibility {1 - (1 - p1_ / 2) ** N2 * (1 - p2_ * p2_):.3f}")
print(f"  ceiling test (one-sided, FAIL at p < 0.001, INVESTIGATE at p < 0.05, re-test FAIL at p' < 0.05): false fail at the boundary P = H: {0.001 + 0.049 * 0.05:.4f} per test")


def ceil_p(nd, t_exp, mh, m_exp):
    """one-sided conditional binomial p-value for direct > H: nd direct counts in exposure t_exp, mh ceiling counts in m_exp"""
    n = nd + mh
    q = t_exp / (t_exp + m_exp)
    lq, l1q = math.log(q), math.log(1 - q)
    low = sum(math.exp(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * lq + (n - j) * l1q) for j in range(0, nd))
    return max(0.0, 1.0 - low)


print(f"  ceiling test, substitution: 8 direct attributed counts in 4,000 events against H measured as 2,000 counts in 1e6 no-PU events (H = 2e-3 = the direct rate): p = {ceil_p(8, 4000, 2000, 1e6):.2f};"
      f" against H = 5e-4 (500 counts): p = {ceil_p(8, 4000, 500, 1e6):.4f}; limiting case H very large: p = {ceil_p(8, 4000, 200000, 1e6):.3g}")
print(f"  completeness bound: leak + mixed fraction <= F^(1/3) - 1 = {2 ** (1 / 3) - 1:.3f} (ln = {math.log(2) / 3:.3f}); 95 % upper limit with zero leaks in N passers: 3/N <= 0.26 needs N >= {math.ceil(3 / (2 ** (1 / 3) - 1))}")

# N2: statistics for the MUST closures
print("\n  N2: attributed counts per 500 C'_PU events in v1 (background.json -> cprime.<t>.rows[].factors; read this session), R04 / R05 / R06 / R07:")
per500 = {"DIF": (166, 81, 2, 1), "NI 22 mm": (127, 46, 0, 0), "NI 30 mm": (173, 60, 1, 0), "NI 61.5 mm": (553, 189, 1, 0),
          "gamma": (153, 86, 13, 2), "V0": (859, 358, 6, 0), "PV pair (24 at R02)": (1, None, 0, 0)}
for t, c in per500.items():
    print(f"    {t}: per 500: {c}; in 1,000 unbiased events R04 / R05 / R06: {c[0] * 2} / {c[1] * 2 if c[1] is not None else 'n/a'} / {c[2] * 2};"
          f" unbiased events for N = 24 at R06: " + (f"{24 / c[2] * 500:.0f}" if c[2] else "no count in v1") + "; at R05: " + (f"{24 / c[1] * 500:.0f}" if c[1] else "n/a"))
print(f"  sizing target: expected count {N_TARGET} in the test half; P(Poisson({N_TARGET}) >= {N_EVAL}) = {1 - sum(pois_pmf(k, N_TARGET) for k in range(N_EVAL)):.3f};"
      f" sized at an expectation of {N_EVAL} it would be {1 - sum(pois_pmf(k, N_EVAL) for k in range(N_EVAL)):.2f}")
print(f"  pile-up direct count at R07, expectation 70: P(N >= 55) = {1 - sum(pois_pmf(k, 70) for k in range(55)):.2f}, P(N >= 64) = {1 - sum(pois_pmf(k, 70) for k in range(64)):.2f}")
print(f"  thinning at R07: with 70 direct counts and N_eff = 80, sigma_tot = {math.sqrt(1 / 70 + 1 / 80):.3f} (limit 0.135); evaluable needs N_eff >= {math.ceil(1 / ((math.log(1.5) / 3) ** 2 - 1 / 70))}")
print("  SM hit level, presel-weighted (effective) counts at R06 in v1 and the sample sized for the target in the test half:")
for p_, (n_, m_) in SM_R06.items():
    need = hit_need(p_)
    plan_ = 10000 if p_.startswith("Z") else 2000 + HIT_EXTRA[p_]
    print(f"    {p_}: {n_} per {m_} events = {n_ / m_:.5f} per event; needed {need} events; planned {plan_}: N_eff in the test half {plan_ / 2 * n_ / m_:.1f};"
          f" at the v2 size of {10000 if p_.startswith('Z') else 2000}: {(10000 if p_.startswith('Z') else 2000) / 2 * n_ / m_:.1f}; extra {max(0, need - (10000 if p_.startswith('Z') else 2000)) * SIG / H:.1f} CPU-h")
rate_p = {"W(tau_l)-like": 3.035 / 375, "W(tau_h)-like": 8.957 / 1625, "tt-like": 5.193 / 2000, "Z-like": 32.300 / 2000}


def comp_cost(rate):
    return max(0, 2 * math.ceil(N_TARGET / rate) - 2000) * SIG / H


PROXY = {"W(e nu)": "W(tau_l)-like", "W(mu nu)": "W(tau_l)-like", "tW": "tt-like", "tt 2l": "tt-like", "t-channel": "tt-like", "WW": "W(tau_h)-like", "WZ": "W(tau_h)-like", "ZZ": "Z-like"}
print("  cost of compliance for the eight proxied processes if their R06 rate equals that of their v1 proxy (ESTIMATE; no v1 count exists):")
tot_c = 0.0
for p_, pr_ in PROXY.items():
    tot_c += comp_cost(rate_p[pr_])
    print(f"    {p_} ({pr_}): +{comp_cost(rate_p[pr_]):.0f} CPU-h; floor {[r[3] for r in rows if r[0] == p_][0]:.2f}; N_trig share {SM_NTRIG[p_] / NTRIG:.3f}")
print(f"    sum {tot_c:.0f} CPU-h; range if every rate is tt-like to Z-like: {8 * comp_cost(rate_p['tt-like']):.0f} to {8 * comp_cost(rate_p['Z-like']):.0f}")
print(f"  NI at R06 unbiased: at 1 count per 500 events, N = 24 needs 12,000 events = {12000 * SIG / H:.0f} CPU-h per radius; at R05 (rung split) the 1,000 unbiased events give 92 / 120 / 378 counts")
print(f"  DIF at R06: 4,000 enriched (16 x enrichment) + 1,000 unbiased (4) events reach {N_TARGET} expected counts for an enrichment >= {(N_TARGET - 4) / 16:.1f};"
      f" else {N_TARGET / 4 * 1000:.0f} unbiased events: +{(N_TARGET / 4 * 1000 - 5000) * SIG / H:.0f} CPU-h")
print(f"  time tag on prompt candidates: hard-scatter candidates at R04 in the hit-level samples: Z(nunu) 10,000 x 19.52 = {10000 * 19.52:.3g};"
      f" all four evaluable processes {10000 * 19.52 + (2000 + HIT_EXTRA['W(tau_h)']) * 12.93 + (2000 + HIT_EXTRA['tt 1l']) * 6.857 + (2000 + HIT_EXTRA['W(tau_l)']) * 9.534:.3g};"
      f" late counts at a fraction 1e-4: {1e-4 * (10000 * 19.52 + (2000 + HIT_EXTRA['W(tau_h)']) * 12.93 + (2000 + HIT_EXTRA['tt 1l']) * 6.857 + (2000 + HIT_EXTRA['W(tau_l)']) * 9.534):.0f} (55 needed for F = 1.5)")
print(f"  crossing rungs on the direct sample: candidates at R05 {49.72 * 96000:.3g}, at R06 {0.2470 * 96000:.3g}; after the R09 fit-probability cut at v1's 2/35: {0.2470 * 96000 * 2 / 35:.0f};"
      f" after R11: {0.2470 * 96000 * CHI[0] * CHI[1] * CHI[2]:.0f}; evaluable (N >= 55) if the pass fraction at R06 is above {55 / (0.2470 * 96000):.4f}")
print(f"  pile-up direct: 96,000 trials x 7.29e-4 = {96000 * 35 / 48000:.0f} counts at R07, sigma_ln = {1 / math.sqrt(70):.3f} (limit for F = 1.5: {math.log(1.5) / 3:.3f})")
print(f"  thinning effective counts per 6000 rho = 2 trials (1/s_boot^2): R04 {1 / 0.0077 ** 2:.0f}, R05 {1 / 0.0079 ** 2:.0f}, R06 {1 / 0.0060 ** 2:.0f};"
      f" direct counts in 6000 rho = 1 trials at R06: {0.2470 * 6000:.0f}, at R07: {35 / 48000 * 6000:.1f}")

# ---- [12] extrapolation width (M4) ----------------------------------------------------------------------------------------------------
print("\n[12] extrapolation width (N5): s_tot^2 = s_model^2 + sum_f s_f^2 + (b^2 + sigma_b^2) d_in^2 + b0^2 d_out^2")
print("  d counts only rungs that change a cut the quantity depends on; with fewer than three evaluable cumulative test rungs sigma_b := b0 = ln F")


def s_tot(smod, F, d_in, d_out, cross=(), bhat=0.0, sb=None):
    b0 = math.log(F)
    sb = b0 if sb is None else sb
    return math.sqrt(smod ** 2 + sum(x * x for x in cross) + (bhat ** 2 + sb ** 2) * d_in ** 2 + (b0 * d_out) ** 2)


RUNGS = (8, 9, 11, 14, 17, 20)
print("  the reviewers' recomputation reproduced (rung-index distance, sigma_b = b0, v2 placeholder s_model):")
print("    pile-up, s_model 0.20, F 1.5:", {("R%02d" % r): round(s_tot(0.20, 1.5, 1, max(0, r - 8)), 2) for r in RUNGS})
print("    single interaction, s_model 0.35, F 2:", {("R%02d" % r): round(s_tot(0.35, 2.0, 1, max(0, r - 8)), 2) for r in RUNGS})
c15, c2 = math.log(1.5) / 3, math.log(2) / 3
print(f"  v3 planning values: s_model at the cap ({c15:.3f} for F = 1.5, {c2:.3f} for F = 2); crossing terms s_f at the same value")
print("    occupancy model (all families act), no crossing test evaluable:", {("R%02d" % r): round(s_tot(c15, 1.5, 1, max(0, r - 8)), 2) for r in RUNGS})
ncross = {8: 0, 9: 1, 11: 1, 14: 2, 17: 3, 20: 3}
print("    occupancy model, crossing tests PASS in the fit-probability, 2S and shape families:", {("R%02d" % r): round(s_tot(c15, 1.5, 1, 0, cross=[c15] * ncross[r]), 2) for r in RUNGS})
print("    occupancy model, as above and three evaluable cumulative rungs in the width family with sigma_b = 0.03:", {("R%02d" % r): round(s_tot(c15, 1.5, 1, 0, cross=[c15] * ncross[r], sb=0.03), 2) for r in RUNGS})
d2s = {8: 0, 9: 0, 11: 0, 14: 3, 17: 3, 20: 3}
print("    promotion pi_k (counting and width rungs act; fit-probability and shape rungs do not), no crossing test:", {("R%02d" % r): round(s_tot(c2, 2.0, 1, d2s[r]), 2) for r in RUNGS})
print("    promotion pi_k, crossing test PASS in the 2S family:", {("R%02d" % r): round(s_tot(c2, 2.0, 1, 0, cross=[c2] * (1 if r >= 12 else 0)), 2) for r in RUNGS})
print("    promotion pi_k tested at R05 only (rung split, NI): d_in = 3 to R08:", round(s_tot(c2, 2.0, 3, 0), 2))
print(f"    conditional (F = 1.5) measured after R09 at the deepest and applied after R14 (5 rungs act): {s_tot(c15, 1.5, 0, 5):.2f}; after R11 (2 rungs): {s_tot(c15, 1.5, 0, 2):.2f};"
      f" measured after R07 and applied after R14 (7 rungs): {s_tot(c15, 1.5, 0, 7):.2f}")
print(f"    independent-steps alternative (ln F x sqrt d) for the occupancy model at R14, no crossing test: {math.sqrt(c15 ** 2 + math.log(1.5) ** 2 * (1 + 6)):.2f}")


def cens_mean(phi0, sw):
    """mean of min(phi0 exp(sw Z), 1)"""
    a = math.log(1.0 / phi0) / sw
    return phi0 * math.exp(0.5 * sw * sw) * Phi(a - sw) + 1.0 - Phi(a)


for phi0, sw in ((0.1, 0.59), (0.1, 1.29), (0.1, 2.47)):
    print(f"  N6 censoring: probability factor {phi0} with width {sw}: uncensored mean {phi0 * math.exp(0.5 * sw * sw):.3f}, P(> 1) = {1 - Phi(math.log(1 / phi0) / sw):.3f};"
          f" censored at 1: mean {cens_mean(phi0, sw):.3f}")
print("  v1 thinning slope for scale: 0.36 per rung; ln 1.5 = %.3f, ln 2 = %.3f" % (math.log(1.5), math.log(2)))

# ---- [13] other checks -------------------------------------------------------------------------------------------------------------------
print("\n[13] other checks")
r07 = 35 / 48000.0
for n in (4000, 12000, 24000):
    c = r07 * 4 * n
    print(f"  R07 direct counts for {n} events x 4 roads (v1 rate): {c:.0f}, sigma_ln = {1 / math.sqrt(c):.2f}")


def binom_tail(n, k, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


print(f"  V4-5: P(>= 48 of 50 | true agreement 0.85) = {binom_tail(50, 48, 0.85):.4f}; | 0.90: {binom_tail(50, 48, 0.90):.3f}; | 0.98: {binom_tail(50, 48, 0.98):.3f}")
print(f"  B*-off paired: N for 5 sigma from 2.1 sigma at N = 171: {171 * (5 / 2.1) ** 2:.0f}")
for n in (1000, 2000):
    print(f"  S1 with {n} rows on the evaluation half (v1 placeholder efficiencies): relative binomial error "
          + ", ".join(f"eps {e}: {math.sqrt(e * (1 - e) / n) / e:.3f}" for e in (0.03, 0.045, 0.2)))
print(f"  v1 best point: eps 0.045 on 200 rows: {math.sqrt(0.045 * 0.955 / 200) / 0.045:.2f}")
print(f"  checks: 0.3/2.71 = {0.3 / 2.71:.4f}; log10(1.2346e6/0.11) = {math.log10(1.2346e6 / 0.11):.2f}")
print(f"  N_exp(E200) = 219.2 fb x 0.04764 x 3000 fb^-1 x 0.5035 = {219.2 * 0.04764 * 3000 * 0.5035:.0f}; x 9/200 = {15775 * 9 / 200:.0f}; 1.2458e7 / 15775 = {1.2458e7 / 15775:.1f}")
print(f"  sideband example: 1.14 x 0.05 x exp(1.105) = {1.14 * 0.05 * math.exp(1.105):.3f}")
print(f"  injection test: standard error of the mean of mu_hat over 200 pseudo-experiments = {1 / math.sqrt(200):.3f} sd(mu_hat)")
print(f"  coverage test: binomial error at 95 % on 500 pseudo-experiments = {math.sqrt(0.05 * 0.95 / 500):.4f}")
print(f"  coverage test, criterion >= 0.93 of 500 (>= 465): P(fail | true coverage 0.95) = {1 - binom_tail(500, 465, 0.95):.3f}; P(pass | true coverage 0.90) = {binom_tail(500, 465, 0.90):.3f}")
b0 = 22.0 / 3.0
for mq, lam_kev in ((200.0, 1.0), (200.0, 0.45), (1500.0, 5.0)):
    a = 2 * math.pi / (b0 * math.log(mq / (lam_kev * 1e-6)))
    print(f"  one-loop alpha_IC(m = {mq:g} GeV, Lambda = {lam_kev} keV), b0 = 22/3: {a:.4f}; C_F alpha (pi/(2 beta) - 4/pi) at beta 0.7/0.5/0.3: "
          + "/".join(f"{0.75 * a * (math.pi / (2 * b) - 4 / math.pi):+.3f}" for b in (0.7, 0.5, 0.3)))
print(f"  B5 hard-scatter share of candidates in SM + PU samples: R04 {19.52 / (19.52 + 171.55):.3f}, R05 {4.51 / (4.51 + 49.72):.3f}, R06 {0.0162 / (0.0162 + 0.2470):.3f};"
      f" DP1 R07 counts per process: {10500 * r07:.1f} (full: {38000 * r07:.1f})")
print(f"  B6 pooled error on eps_var/eps_nom, unpaired, eps = 0.2: 1200 rows {math.sqrt(2 * 0.8 / (0.2 * 1200)):.3f}, 3000 rows {math.sqrt(2 * 0.8 / (0.2 * 3000)):.3f}")
print(f"  pile-up vertices per crossing, upper estimate: 200 x 100 particles x 0.053 = {200 * 100 * 0.053:.0f}; Geant4 per PU event 200 x 100 x 0.134 ms = {200 * 100 * 0.134e-3:.1f} s")
for n2 in (200, 400, 1000):
    def mde(eps, s1):
        return 2 * math.sqrt(s1 ** 2 + (1 - eps) / (eps * n2))
    print(f"  C1 signal, {n2} v2 rows against 200 v1 rows: detectable shift (2 sigma) at R04 (eps 0.205, v1 14 %): {mde(0.205, 0.14):.2f};"
          f" at FB2 (eps 0.045, v1 33 %): {mde(0.045, 0.33):.2f}")
print(f"  pile-up no-credit value beyond the last direct count: N_trig x 1.14 / 96,000 trials = {NTRIG * U68 / 96000:.0f} events (mean {NTRIG / 96000:.0f})")
print(f"  S1 chain share that could be cut by 500 rows at the 15 points below 1 keV: {15 * 1500 * SIG / H:.0f} CPU-h (listed, not proposed)")
print(f"  paired B6 at six points, 300 rows: signal {6 * 300 * 6 * SIG / H:.0f} CPU-h (reduced unpaired at four points: {4 * 300 * 6 * SIG / H:.0f})")
print(f"  GA-1: 1 sigma binomial error of a v2 count on 400 rows (v1 placeholders): R07 (eps 0.09) {math.sqrt(0.91 / (0.09 * 400)):.2f}; fallback (eps 0.045) {math.sqrt(0.955 / (0.045 * 400)):.2f}")
print(f"  GA-6: re-digitisation of 24,000 direct + 80,000 signal events at the chain cost: {104000 * CHAIN / H:.0f} CPU-h")
print(f"  GA-7: paired B6 at six points: signal +{2 * 300 * 6 * SIG / H:.0f}, partners +{2 * 300 * SIG / H:.0f}, Stage-3 material for two more points at 3 to 5 keV +{2 * 2 * 300 * s3_at[3] / H:.0f} to +{2 * 2 * 300 * s3_at[5] / H:.0f} CPU-h")
print(f"  lever on the SHOULD item B5 (Q4 option): sideband with pile-up on the 500 pile-up events only: -{6000 * 7 * TRIAL / H:.0f} CPU-h = -{6000 * 7 * TRIAL / H / CAP_PROD:.1f} days")
print(f"  B5 with the signal road counted on all 10,000 Z(nunu) hit-level events: weighted hard-scatter candidates at R06 = {10000 * 0.01615:.0f}")
a_ic = 2 * math.pi / (b0 * math.log(200.0 / 1e-6))
print("  infracolour correction with the vector-current threshold factor quoted in the physics review (P-C4), C_F alpha [pi/(2 beta) - (3 + beta)/(4 pi) (pi^2/2 - 3/4)], at beta 0.7/0.5/0.3: "
      + "/".join(f"{0.75 * a_ic * (math.pi / (2 * b) - (3 + b) / (4 * math.pi) * (math.pi ** 2 / 2 - 0.75)):+.3f}" for b in (0.7, 0.5, 0.3)))
print(f"  T1-e per-nuisance reading: P(|pull| > 2) = {2 * Phi(-2):.3f}; on 200 pseudo-experiments its binomial error is {math.sqrt(2 * Phi(-2) * (1 - 2 * Phi(-2)) / 200):.3f}; threshold 0.10 is {(0.10 - 2 * Phi(-2)) / math.sqrt(2 * Phi(-2) * (1 - 2 * Phi(-2)) / 200):.1f} sigma above")
print("  B1-g test, expected secondary-attributed counts in 4,000 trials at R04/R05/R06/R07 (rate 1.57 x v1 counts per 500): "
      + " / ".join(f"{4000 * 1.57 * c / 500:.0f}" for c in (166, 81, 2, 1)))
print(f"  DIF rate per triggered event by process (background.json -> cprime.dif.rate.per_process): 1.569 (Z nunu) to 1.5945 (tt 2l): spread {1.5945 / 1.5691 - 1:.3f}")
