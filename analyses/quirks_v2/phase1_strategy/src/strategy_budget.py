#!/usr/bin/env python3
"""Arithmetic behind the Phase-1 STRATEGY v4 (STRATEGY_fiona_2026-11-13_23-05.md).

Standard library only; run as `python3 -I strategy_budget.py` (about ten seconds; allowed on einstein).
History: v1 by Brigitte (17:55); rewritten by the fixer Dmitri for review cycle 1 (arbiter findings M1-M35);
updated by the fixer Emeric for review cycle 2 (findings N1-N18 and the residuals of M4, M5, M11, M12, M15, M24, M26);
updated by the fixer Fiona for review cycle 3 (findings P1-P16 and the adopted C items; "v4" lines below);
updated by the fixer Gunnar for review cycle 4 (findings R1, R3, R5; "v5" lines below; STRATEGY_gunnar_2026-11-14_00-50.md).
Every unit cost carries a provenance letter:
  M = measured in the feasibility phase (source in the comment);
  D = derived from measured parts, or measured on one event / toy inputs;
  G = guess (not benchmarked).
CPU-h are slot-hours on a worker with 4 jobs per node (the "4 concurrent" columns of FEAS_A).
Sections printed: [1] unit costs, [2] capacity, [3] budget table, [4] totals and variants, [5] deltas per finding,
[6] contingency, [7] calendar, [8] storage, [9] zero-count floors (M6), [10] zero-count likelihood checks (M1),
[9b] projection per outcome (N7; v4: scenarios alpha, beta, gamma of P2), [11] closure-test size and power (N4),
ceiling-test family (P6), statistics for the MUST closures (N2), [12] extrapolation width (N5; v4: P7, P8),
[13] other checks (v4: T1 coverage family, P11).
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
PV_LINE = 0.22                        # v1 "PV-line factor": background.json -> cprime.ni*.rate.pv_line_factor; wp.py l.40 P_PV_LINE
RATE = {"PV pair": 30.31, "DIF": 1.5945, "gamma": 0.379, "looper": 0.30, "V0": 0.052,
        "NI 22 mm": 0.09823 * PV_LINE, "NI 30 mm": 0.12408 * PV_LINE, "NI 61.5 mm": 0.12408 * PV_LINE}
#   PV pair, DIF, gamma: D4 l.395 (cprime.<t>.rate); looper 0.30, V0 0.052: D2 l.69 (UNVERIFIED);
#   v4 (Ph-C1/K-C5): NI from background.json -> cprime.ni22/ni30/ni61.rate.value (read this session), one rate set
RATE_D2 = dict(RATE, **{"NI 22 mm": 0.11 * 0.22, "NI 30 mm": 0.11 * 0.22, "NI 61.5 mm": 0.11 * 0.22})  # v2 history only
SM_NTRIG_V1 = {"Z(nunu)+j": 25078824.8, "W(tau_h)": 5407122.7, "W(e nu)": 2536644.1, "tt 1l": 2379799.0,
               "W(tau_l)": 2257327.6, "W(mu nu)": 2238036.6, "tW": 259273.4, "tt 2l": 212934.8, "WZ": 137419.5,
               "WW": 126435.9, "t-channel": 110124.9, "ZZ": 104504.5}   # bsum_wp.json -> n_trig.breakdown (read this session)
# v4 (P1): the two additions with a no-pile-up pool share. N_trig is not known before the MET model (day 12); planning
# values [E]: Z(tautau) = r_tt x f_MET x N_Z(nunu), r_tt = B(Z->tautau)/B(Z->nunu) = 0.17 (review N-A1, UNVERIFIED),
# f_MET = fraction with MET_reco > 250 GeV after the lepton veto, 0.1 (range 0.024-0.3); lost-lepton Z(ll) = r_ll x f_lost
# x N_Z(nunu), r_ll = 0.34 (= 2 x 0.17, UNVERIFIED), f_lost = 3.5e-3 (range 1.2e-3-1.2e-2) [E, guesses fixed by the MET model].
NZ = SM_NTRIG_V1["Z(nunu)+j"]
ADD_PLAN = {"Z(tautau)": 0.17 * 0.1 * NZ, "Z(ll) lost": 0.34 * 3.5e-3 * NZ}
ADD_LO = {"Z(tautau)": 1e5, "Z(ll) lost": 1e4}
ADD_HI = {"Z(tautau)": 1.3e6, "Z(ll) lost": 1e5}
SM_NTRIG = dict(SM_NTRIG_V1, **ADD_PLAN)
MJ_PLAN, MJ_LO, MJ_HI = 4e5, 4e4, 4e6   # multijets after the MET selection [E: 1 % (0.1-10 %) of N_trig; R-4 and the MET model fix it]
MJ_LOOSE = 1e6                        # loose multijet population through the no-pile-up chain (B4-e factorisation)
G4_DEC, G4_NI = 0.011, 0.042   # M  vertices per pion gun (pT 1-10 GeV, |eta| < 1): decays, inelastic: FEAS_B Task 5
# N8 (cycle 2): one route per particle origin. Particles of the hard-scatter vertex that Fatras traces (prompt tracks,
# loopers, photon conversions, V0 decays) are counted by B4 on real events. The pool keeps, as single-interaction
# terms, only what needs Geant4: decays in flight and nuclear interactions (hard-scatter share + 200 x minimum bias).
# The cost per event of these terms includes the Geant4 guns needed for one distinct vertex per event.
POOL_SI = ["DIF", "NI 22 mm", "NI 30 mm", "NI 61.5 mm"]
C_SI = {"DIF": NOPU + G4GUN / G4_DEC, "NI 22 mm": NOPU + G4GUN / G4_NI, "NI 30 mm": NOPU + G4GUN / G4_NI,
        "NI 61.5 mm": NOPU + G4GUN / G4_NI}
terms_v2 = [(t, NTRIG * r, NOPU) for t, r in RATE_D2.items()] + [(p, n, NOPU_HS) for p, n in SM_NTRIG_V1.items()]
terms_v3 = [(t, NTRIG * RATE_D2[t], C_SI[t]) for t in POOL_SI] + [(p, n, NOPU_HS) for p, n in SM_NTRIG_V1.items()]
terms = [(t, NTRIG * RATE[t], C_SI[t]) for t in POOL_SI] + [(p, n, NOPU_HS) for p, n in SM_NTRIG.items()]


def terms_with(add):
    return [(t, NTRIG * RATE[t], C_SI[t]) for t in POOL_SI] + [(p, n, NOPU_HS) for p, n in dict(SM_NTRIG_V1, **add).items()]
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
add("2", "B1", "MUST", "Geant4 vertices of the pilot's unbiased DIF and NI events (one vertex per event)", 1e6 * G4GUN / G4_DEC + 3e6 * G4GUN / G4_NI,
    "1e6 x 12.2 ms + 3e6 x 3.2 ms (gun yields 1.1 %, 4.2 %)", "D", "P4 (K-C10)")
PILOT_HS = 2.3e6
add("2", "B4", "MUST", "pilot: N_t x H before the freeze for the largest term, 2.3e6 no-PU Z(nunu)+jets events", PILOT_HS * NOPU_HS, "2.3e6 x 45 ms", "G", "N1/N7")
add("2", "B1", "MUST", "enrichment pilot: 1000 overlays of near-pass events", 1000 * SIG, "1000 x 25.2 s", "D", "M3/M6")
add("2", "B3", "MUST", "time-tag: hit-level late-hit density on the C1 events", 5 * H, "", "G", "M16")
add("2", "all", "MUST", "unit-cost timing jobs (no-PU hard scatter, signal row, MLM, 60-100-parameter workspace)", 5 * H, "", "G", "M19")
# Phase 3 (development, signal blind)
add("3", "B1", "MUST", "Geant4 hand-over tests, small P_geo and overlay samples", 60 * H, "", "G")
add("3", "B1", "MUST", "pile-up-vertex secondaries test: 1000 PU events with Geant4 secondaries", 1000 * (B1EV + 2.7), "1000 x (60.4 + 2.7) s", "D", "M26")
N_DEVOVL = 1000
add("3", "B1", "MUST", "development ceiling and completeness tests: 1000 unbiased Geant4 DIF overlays", N_DEVOVL * (SIG + NOPU + G4GUN / G4_DEC),
    "1000 x (25.2 s + 23.7 ms)", "D", "P4")
add("3", "B4", "MUST", "MET model and its validation, biased multijet generation tests (no SM hit-level sample, P14)", 50 * H, "", "G")
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
N_PAIRED = 4 * 1000 + 4 * 1000 + 11 * 1000   # unbiased B1 test overlays (DIF 1,000; NI 3 x 1,000) + 1,000 hit-level test-half events of each of the fifteen SM processes (v5, R5)
add("4a", "B1", "MUST", "paired pile-up-only finder pass (term hits removed) on the 4,000 unbiased B1 test overlays", 4000 * TRIAL,
    "4000 x 11.7 s", "M", "P5")
add("4a", "B4", "MUST", "paired pile-up-only finder pass on 1,000 test-half events of each of the four supplied B4 processes", 4000 * TRIAL,
    "4000 x 11.7 s", "M", "P5")
add("4a", "B4", "MUST", "paired pile-up-only finder pass on 1,000 test-half events of each of the eleven other SM processes (incl. Z(tautau), lost-lepton Z(ll), multijets)",
    11000 * TRIAL, "11000 x 11.7 s", "M", "R5")
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
TOYS_V2 = (5 * 20 * 8 + 3 * 40 * 8) * TOYS1000 / H
TOYS_V3 = (5 + 3) * (NFT + NCHK) * 8 * TOYS1000 / H
RESERVE2 = TOYS_V2 - TOYS_V3          # the CPU freed by C-1: the day-15 redirection reserve (Q2)
# v4 (P13): the reserve is spent by default (rule 3 of STR §11.7), so it is inside the approved figure of every variant.
APPROVED = {"MUST only": must + RESERVE2, "MUST + SHOULD reduced": must + shr + RESERVE2, "MUST + SHOULD full": must + shf + RESERVE2}
print(f"  approved figure = total + day-15 reserve {RESERVE2:.1f} CPU-h (P13):")
for k_, v_ in APPROVED.items():
    print(f"    {k_}: {v_ - RESERVE2:.1f} + {RESERVE2:.1f} = {v_:.1f} CPU-h; stop-and-ask threshold 1.3 x {v_:.0f} = {1.3 * v_:.0f}")
V3 = {"MUST": 3945.0, "RED": 4378.0, "FULL": 4891.0, "THR": 5691.0, "DAYS": 56.6}
P_ADD = sum(h for p, i, pr, lab, h, a, pv, f in items if f.startswith("P4") or f.startswith("P5"))
R_ADD = sum(h for p, i, pr, lab, h, a, pv, f in items if f.startswith("R5"))   # v5 (R5): kept out of the v3 -> v4 history line
print(f"  v3 -> v4: review additions (P4, P5, K-C10) {P_ADD:.1f} CPU-h; MUST {V3['MUST']:.0f} -> {must - R_ADD:.0f}; reduced {V3['RED']:.0f} -> {must - R_ADD + shr:.0f};"
      f" full {V3['FULL']:.0f} -> {must - R_ADD + shf:.0f}; approved (reduced + reserve) {APPROVED['MUST + SHOULD reduced'] - R_ADD:.0f}, threshold {V3['THR']:.0f} -> {1.3 * (APPROVED['MUST + SHOULD reduced'] - R_ADD):.0f}")
V4 = {"MUST": 3983.6, "RED": 4417.1, "FULL": 4930.4, "APP": 4573.6, "THR": 5946.0}   # v4 printed values (budget_stdout_v4.txt)
print(f"  v4 -> v5: review addition (R5) {R_ADD:.2f} CPU-h; MUST {V4['MUST']:.1f} -> {must:.1f}; reduced {V4['RED']:.1f} -> {must + shr:.1f};"
      f" full {V4['FULL']:.1f} -> {must + shf:.1f}; approved (reduced + reserve) {V4['APP']:.1f} -> {APPROVED['MUST + SHOULD reduced']:.1f}, threshold {V4['THR']:.0f} -> {1.3 * APPROVED['MUST + SHOULD reduced']:.0f}")

# ---- [5] deltas v2 -> v3 per finding (cycle 2; history) -----------------------------------------------------------------
V1 = {"MUST": 2950.0, "RED": 3275.0, "FULL": 3798.0}
V2 = {"MUST": 3968.0, "RED": 4401.0, "FULL": 4915.0, "DAYS": 57.9, "NONPROD": 44}
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
print(f"  v1 -> v2 -> v3: MUST {V1['MUST']:.0f} -> {V2['MUST']:.0f} -> {V3['MUST']:.0f}; reduced {V1['RED']:.0f} -> {V2['RED']:.0f} -> {V3['RED']:.0f};"
      f" full {V1['FULL']:.0f} -> {V2['FULL']:.0f} -> {V3['FULL']:.0f} (v3 values; v4 in [4])")
print(f"  day-15 redirection reserve (CPU freed by C-1; v4: inside the approved figure, P13): {RESERVE2:.0f} CPU-h = {RESERVE2 / CAP_PROD:.1f} production days")
print("\n[5'] deltas v3 -> v4, per finding (CPU-h; days on the Phase-4a critical path at the production capacity)")
for p, i, pr, lab, h, a, pv, f in items:
    if f.startswith("P4") or f.startswith("P5"):
        crit = h / CAP_PROD if p == "4a" else 0.0
        print(f"  {h:+8.1f} CPU-h  {crit:+5.2f} d   {f}: {lab} (phase {p})")
print(f"  {RESERVE2:+8.1f} CPU-h  {RESERVE2 / CAP_PROD:+5.2f} d   P13: day-15 reserve inside the approved figure, spent in 4a production by rule 3")
print("  P1: Z(tautau) and lost-lepton Z(ll) get pool shares inside the same 665 CPU-h (0 CPU-h); S-1: B5 and the B6 signal arm out of the 4a window (0 CPU-h; days in [7])")
print("\n[5''] deltas v4 -> v5, per finding (CPU-h; days on the Phase-4a critical path at the production capacity)")
for p, i, pr, lab, h, a, pv, f in items:
    if f.startswith("R5"):
        print(f"  {h:+8.2f} CPU-h  {(h / CAP_PROD if p == '4a' else 0.0):+5.2f} d   {f}: {lab} (phase {p})")
print("  R1, R2, R4: text, table and [9b] rows only (0 CPU-h); R3: the pilot keeps its no-pile-up hit records (0 CPU-h; storage in [8])")

# ---- [6] contingency from provenance --------------------------------------------------------------------------------------
FRAC = {"M": 0.10, "D": 0.30, "G": 1.00}
print("\n[6] provenance and contingency (reduced variant)")
cont = 0.0
for pv in "MDG":
    s = sum(h for p, i, pr, lab, h, a, v, f in items if v == pv and (is_must(pr) or sh_red(p, i, pr)))
    cont += FRAC[pv] * s
    print(f"  provenance {pv}: {s:.0f} CPU-h, carried at {FRAC[pv]:.0%} -> {FRAC[pv] * s:.0f}")
RESERVE = 24000 * B1EV / H
APP = APPROVED["MUST + SHOULD reduced"]
print(f"  contingency from provenance {cont:.0f} CPU-h; fresh-sample reserve (one B2 direct sample) {RESERVE:.0f} CPU-h")
print(f"  approved figure (reduced + day-15 reserve) {APP:.0f} CPU-h; with contingency and the fresh-sample reserve: {APP + cont + RESERVE:.0f};"
      f" stop-and-ask threshold 1.3 x {APP:.0f} = {1.3 * APP:.0f}")
print(f"  thresholds for the other variants (each with the reserve): MUST only 1.3 x {APPROVED['MUST only']:.0f} = {1.3 * APPROVED['MUST only']:.0f};"
      f" full 1.3 x {APPROVED['MUST + SHOULD full']:.0f} = {1.3 * APPROVED['MUST + SHOULD full']:.0f};"
      f" envelope alternative (Q4): {APP:.0f} + {cont:.0f} = {APP + cont:.0f}, threshold {1.3 * (APP + cont):.0f}")
print(f"  if every guessed (G) unit cost doubled: {APP:.0f} + {FRAC['G'] * sum(h for p, i, pr, lab, h, a, v, f in items if v == 'G' and (is_must(pr) or sh_red(p, i, pr))):.0f}"
      f" = {APP + sum(h for p, i, pr, lab, h, a, v, f in items if v == 'G' and (is_must(pr) or sh_red(p, i, pr))):.0f} CPU-h against the threshold {1.3 * APP:.0f}")
G_MEAS1 = sum(h for p, i, pr, lab, h, a, v, f in items if v == "G" and (is_must(pr) or sh_red(p, i, pr))
              and ("45 ms" in a or "50 ms" in a or "652 s" in a or "FxFx" in lab or "V4-5" in lab or "T_seed" in lab))
print(f"  K-C13: G-provenance CPU-h whose unit cost the day-5 timing jobs measure (45 ms no-PU event, MLM, FxFx, toy scaling): {G_MEAS1:.0f};"
      f" the rest of the G total (allowances, Geant4 spectra and variations, development) is fixed only at checkpoint 2 or later")
print("  conditional draws (none is inside the approved figure; each is reported as an overrun when drawn and counts toward the threshold):")
for lab, h in (("exact toys in both passes if the f_T check of pass 1 fails (upper value; the check toys are reused)",
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
SLOTS = [("Phase 2, days 0-5", [("(i) C1 campaigns and C2; the sealed C1 comparison as a short separate session inside this slot, after the C1 counts", 5),
                                 ("(ii) S2, P1, retrievals R-2/R-3 first, Herwig install attempt", 5),
                                 ("(iii) pilot, T1 workspace builder on v1 counts, Geant4 geometry, B1-d scan, hand-over code", 5)]),
         ("Phase 3, days 5-17", [("(i) B1 + B3 development", 12),
                                 ("(ii) B2 development (days 5-16), then the one Phase-3 1-bot review of SELECTION.md (days 16-17)", 12),
                                 ("(iii) T1 + B4 development (days 5-12: MET model by day 10, A and m_mig day 12), then the PREREG_v2 drafter with the T2 script (days 12-17)", 12)])]
print("  v4 agent-slot table (P16; at most three agents at a time; executors + reviewers + drafter):")
for ph_, rows_ in SLOTS:
    print(f"    {ph_}: {len(rows_)} concurrent slots; " + "; ".join(f"{r_} [{d_} d]" for r_, d_ in rows_))
DEV3, DRAFT3, REV3 = 12 + 11 + 7, 5, 1
print(f"  Phase 3 channel-days: development {DEV3} + PREREG drafting {DRAFT3} + 1-bot review {REV3} = {DEV3 + DRAFT3 + REV3} = 3 x 12 (cap);"
      f" PLAN estimates 35-50 person-days of development; each 3 channel-days more lengthen Phase 3 by one day (decision point 2 moves the freeze)")
FIXED = [("Phase 2 (three agents)", 5), ("Phase 3 development (three channels; PREREG drafted in channel (iii) from day 12; one 1-bot review)", 12),
         ("freeze: 4-bot review of PREREG_v2, hash", 2), ("ITERATE allowance (freeze)", 2),
         ("closure analysis of the last campaign, T1 expected results, note and PDF before the 4a review (N-C12; bought by S-1)", 1.5),
         ("4a review (4-bot + bib)", 3), ("ITERATE allowance (4a)", 2), ("4b: T2, toys, 4-bot + bib", 3), ("ITERATE allowance (4b)", 2),
         ("Gate B turnaround", 2), ("4c and 1-bot review", 3), ("Phase 5 (sections 1-6, 8-10 drafted during 4a)", 4), ("ITERATE allowance (5-bot)", 2)]
nonprod = sum(d for _, d in FIXED)
for lab, d in FIXED:
    print(f"    {d:4.1f} d  {lab}")
print(f"  non-production days: {nonprod} (v3: 42; v2: {V2['NONPROD']}) -> already above the 28 days of a 4-week target; without the four ITERATE allowances: {nonprod - 8}")
# S-1 (adopted): B5 and the B6 signal arm leave the 4a production window and run in days 36-48 beside the S1 chain and the toys.
B6SIG_RED = 4 * 300 * 6 * SIG + 4 * 300 * SIG + 2 * 2 * 300 * (s3_at[1.5] + 2 * s3_at[3] + s3_at[5])
B6SIG_FULL = 6 * 500 * 6 * SIG + 6 * 500 * SIG + 2 * 2 * 500 * (s3_at[1.5] + s3_at[3] + s3_at[5])
MOVED = {"MUST-only": 0.0,
         "MUST + SHOULD reduced": (6000 * 7 * TRIAL + 500 * 16 * TRIAL + 20 * H + B6SIG_RED) / H,
         "MUST + SHOULD full": (8000 * 19 * TRIAL + 500 * 16 * TRIAL + 20 * H + B6SIG_FULL) / H}
print(f"  S-1: moved out of the 4a window: reduced {MOVED['MUST + SHOULD reduced']:.0f} CPU-h (B5 163 + prototype 20 + B6 signal arm {B6SIG_RED / H:.0f});"
      f" full {MOVED['MUST + SHOULD full']:.0f} CPU-h")
CAL = {}
for name, cpu in [("MUST-only", prod_must_bkg), ("MUST + SHOULD reduced", prod_must_bkg + prod_red), ("MUST + SHOULD full", prod_must_bkg + prod_full)]:
    crit = cpu - MOVED[name] + RESERVE2
    d = crit / CAP_PROD
    CAL[name] = nonprod + d
    late = prod_s1 + MOVED[name]
    print(f"  {name}: 4a production on the critical path {cpu:.0f} - {MOVED[name]:.0f} (S-1) + {RESERVE2:.0f} (day-15 reserve, P13) = {crit:.0f} CPU-h = {d:.1f} days;"
          f" S1 chain {prod_s1:.0f} + moved {MOVED[name]:.0f} + toys pass 1 {5 * (NFT + NCHK) * 8 * TOYS1000 / H:.0f} = {late + 5 * (NFT + NCHK) * 8 * TOYS1000 / H:.0f} CPU-h"
          f" run between the end of production and Gate B ({(nonprod - 5 - 12 - 4 - 3 - 4 - 2) * CAP_PROD:.0f} core-h available); total {nonprod + d:.1f} days = {(nonprod + d) / 7:.1f} weeks; at utilisation 0.50 in production: {nonprod + crit / CAP_DEV:.1f} days")
print(f"  range: every review passes at once and MUST only: {CAL['MUST-only'] - 8:.1f} days; two ITERATE cycles per panel review: +8 days")
# v6 (T3): under the recommended Q2 (a) the day-15 pause is the expected branch ("the study pauses and the user is asked",
# STR §11.7 rule 1); it costs the Gate-B turnaround (2 d, FIXED above), so the approved calendar includes it.
PAUSE15 = 2.0
print(f"  v6 (T3): expected branch under Q2 (a): + {PAUSE15:.1f} d day-15 pause turnaround (the Gate-B turnaround) -> MUST + SHOULD reduced"
      f" {CAL['MUST + SHOULD reduced'] + PAUSE15:.1f} d = {(CAL['MUST + SHOULD reduced'] + PAUSE15) / 7:.1f} weeks; MUST-only {CAL['MUST-only'] + PAUSE15:.1f};"
      f" full {CAL['MUST + SHOULD full'] + PAUSE15:.1f} (without the pause: {CAL['MUST + SHOULD reduced']:.1f} / {CAL['MUST-only']:.1f} / {CAL['MUST + SHOULD full']:.1f})")
# v6 (H-C1 rider, verdict §7): an optional Gate-A rider, not in the default figures. Part (3) is an addition: the 100 CPU-h
# development allowance is already a booked MUST item.
RIDER_H = 1000 * SIG / H
print(f"  H-C1 rider (if accepted at Gate A): 1,000 gamma development overlays 1000 x {SIG:.1f} s = {RIDER_H:.1f} CPU-h, added: approved"
      f" {APPROVED['MUST + SHOULD reduced'] + RIDER_H:.1f} CPU-h, threshold 1.3 x {APPROVED['MUST + SHOULD reduced'] + RIDER_H:.1f} = {1.3 * (APPROVED['MUST + SHOULD reduced'] + RIDER_H):.1f}"
      f" (default {APPROVED['MUST + SHOULD reduced']:.1f} / {1.3 * APPROVED['MUST + SHOULD reduced']:.1f}); calendar unchanged (idle pre-freeze capacity"
      f" {PRE * CAP_DEV - ph2_cpu - ph3_cpu:.0f} core-h); the veto measurement on the stored pilot records and the day-7 question 0 CPU-h")
t4b, t4c = 5 * (NFT + NCHK) * 8 * TOYS1000 / H, 3 * (NFT + NCHK) * 8 * TOYS1000 / H
print(f"  toys 4b {t4b:.1f} + 4c {t4c:.1f} = {t4b + t4c:.1f} CPU-h (v2: {TOYS_V2:.1f}); at {CAP_PROD:.0f}/day: {t4b / CAP_PROD:.1f} and {t4c / CAP_PROD:.1f} days (inside the 3-day windows)")
print(f"  time-ordered checkpoints: decision point 1 and stop-rule checkpoint 1 at day 5; decision point 2 at day 15; freeze days 17-19; production from day {PRE};"
      f" Gate B at about day {PRE + (prod_must_bkg + prod_red - MOVED['MUST + SHOULD reduced'] + RESERVE2) / CAP_PROD + 1.5 + 3 + 2 + 3 + 2 + 2:.0f};"
      f" v4: rule 1 of decision point 2 computed preliminarily at day 7 from the finished pilot, binding at day 15")
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
    "v5 (R3): pilot no-PU full hit records, classified in Phase 3 ((4e6 + %.2g) x 8.2 kB; more for the hard-scatter events)" % PILOT_HS: (4e6 + PILOT_HS) * 8.2e3 / 1e9,
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
f_v1_sm = sum(U68 * n / 1e6 for n in SM_NTRIG_V1.values())
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
    print(f"  v4 routes (fourteen SM processes), pool {c_h:.0f} CPU-h (chain + Geant4 vertices): sum of floors {s68:.1f} (DIF and NI {si68:.1f}, SM {s68 - si68:.1f}); sum of means {sum(r[4] for r in rows):.1f}")
rows_v3 = floor_table(C_POOL, tt=terms_v3)
print(f"  v3 routes for comparison (twelve SM processes, NI at 0.11 x 0.22): sum of floors {sum(r[3] for r in rows_v3):.2f}")
print(f"  | term | N_t in 3 ab^-1 | cost per event (ms) | M_t planned | transfer factor N_t/M_t | floor at 68 % (1.14 N/M) |   (pool {C_POOL:.0f} CPU-h)")
rows = floor_table(C_POOL)
cost = {t: c for t, n, c in terms}
for t, n, m, f68, mean in rows:
    print(f"  | {t} | {n:.3g} | {1e3 * cost[t]:.1f} | {m:.3g} | {mean:.2f} | {f68:.2f} |")
EVAL4 = ("Z(nunu)+j", "W(tau_h)", "W(tau_l)", "tt 1l")
print(f"  events in the pool: DIF and NI {m_si:.3g} ({c_si_h / H:.0f} CPU-h), SM {m_sm:.3g} ({m_sm * NOPU_HS / H:.0f} CPU-h)")
PROXY8 = ("W(e nu)", "W(mu nu)", "tW", "tt 2l", "t-channel", "WW", "WZ", "ZZ")
print(f"  floors by group: DIF {rows[0][3]:.2f}; NI (three) {sum(r[3] for r in rows[1:4]):.2f}; the four SM processes with an evaluable closure {sum(r[3] for r in rows if r[0] in EVAL4):.2f};"
      f" the eight proxied processes {sum(r[3] for r in rows if r[0] in PROXY8):.2f}; the two pooled additions {sum(r[3] for r in rows if r[0] in ADD_PLAN):.2f}")
print(f"  N_trig share: four evaluable processes {sum(SM_NTRIG[p] for p in EVAL4) / NTRIG:.3f}; eight proxied processes {sum(SM_NTRIG[p] for p in PROXY8) / NTRIG:.3f};"
      f" the two additions at their planning N_trig {sum(ADD_PLAN.values()) / NTRIG:.3f} (N_trig itself is kept at v1's 4.0848e7; the additions raise it by {sum(ADD_PLAN.values()) / NTRIG:.1%} at day 12)")
# P1: the additions in the pool, their range, and the cost of keeping the v3 floor instead
F_V3 = sum(r[3] for r in rows_v3)
F_V4 = sum(r[3] for r in rows)
print(f"  P1: Z(tautau) planning N_trig {ADD_PLAN['Z(tautau)']:.3g} (range 1e5-1.3e6), lost-lepton Z(ll) {ADD_PLAN['Z(ll) lost']:.3g} (range 1e4-1e5) [E]")
for lab_, add_ in (("low", ADD_LO), ("planning", ADD_PLAN), ("high", ADD_HI)):
    rr_ = floor_table(C_POOL, tt=terms_with(add_))
    al_ = allocate(C_POOL, tt=terms_with(add_))
    fz_ = [r for r in rr_ if r[0] == "Z(tautau)"][0]
    fl_ = [r for r in rr_ if r[0] == "Z(ll) lost"][0]
    s_ = sum(r[3] for r in rr_)
    print(f"    {lab_}: Z(tautau) M = {al_['Z(tautau)']:.3g} ({al_['Z(tautau)'] * NOPU_HS / H:.1f} CPU-h), floor {fz_[3]:.2f}; Z(ll) M = {al_['Z(ll) lost']:.3g}"
          f" ({al_['Z(ll) lost'] * NOPU_HS / H:.1f} CPU-h), floor {fl_[3]:.2f}; summed pool floor {s_:.2f}; to keep {F_V3:.2f} the pool needs"
          f" {C_POOL * s_ / F_V3:.0f} CPU-h (+{C_POOL * s_ / F_V3 - C_POOL:.0f})")
    print(f"      without a pool share (direct bound on 2,000 hit-level events, N_t x 1.14 / 2000): Z(tautau) {U68 * add_['Z(tautau)'] / 2000:.0f}, Z(ll) {U68 * add_['Z(ll) lost'] / 2000:.0f} events")
MJF = {k_: U68 * v_ / MJ_LOOSE for k_, v_ in (("low", MJ_LO), ("planning", MJ_PLAN), ("high", MJ_HI))}
print(f"  multijet floor through the factorisation (N_MJ x 1.14 / 1e6 loose events) [E]: {MJF['planning']:.2f} (range {MJF['low']:.2f}-{MJF['high']:.2f})")
print(f"  headline sum of 68 % floors: pool {F_V4:.2f} + multijets {MJF['planning']:.2f} = {F_V4 + MJF['planning']:.1f} (range {F_V4 + MJF['low']:.1f}-{F_V4 + MJF['high']:.1f}; with the additions"
      f" at their low / high N_trig: {sum(r[3] for r in floor_table(C_POOL, tt=terms_with(ADD_LO))) + MJF['low']:.1f} / {sum(r[3] for r in floor_table(C_POOL, tt=terms_with(ADD_HI))) + MJF['high']:.1f})")
tt_2c = [(t, n, (2 * c if c == NOPU_HS else c)) for t, n, c in terms]
r2c = floor_table(C_POOL, tt=tt_2c)
print(f"  if the no-PU hard-scatter event costs 90 ms instead of 45 (G provenance): SM pool floor {sum(r[3] for r in r2c if r[0] in SM_NTRIG):.1f}"
      f" (now {sum(r[3] for r in rows if r[0] in SM_NTRIG):.1f}), summed pool floor {sum(r[3] for r in r2c):.1f}")
C_NI6 = NOPU + G4GUN / (G4_NI / 6)
tt_slab = [(t, n, (C_NI6 if t.startswith("NI") else c)) for t, n, c in terms]
print(f"  K-C6: if the inelastic gun yield per slab is a sixth of 4.2 % (c_NI = {1e3 * C_NI6:.1f} ms), the summed pool floor is {sum(r[3] for r in floor_table(C_POOL, tt=tt_slab)):.2f} (D provenance)")
print(f"  pilot: one H count in 2.3e6 Z(nunu) no-PU events = {SM_NTRIG['Z(nunu)+j'] / PILOT_HS:.1f} events in 3 ab^-1; in 1e6 DIF events = {NTRIG * RATE['DIF'] / 1e6:.0f}")
print(f"  v1 best B84 against the v4 zero-count floor: log10(1.2346e6 / {sum(r[3] for r in rows):.1f}) = {math.log10(1.2346e6 / sum(r[3] for r in rows)):.2f} decades")
random.seed(20261113)
means = [r[4] for r in rows]
draws = sorted(sum(mu * random.expovariate(1.0) for mu in means + [MJ_PLAN / MJ_LOOSE]) for _ in range(200000))
q = lambda f: draws[int(f * len(draws))]
print(f"  predictive distribution of the summed floor, pool terms and the multijet planning term (each N/M x Exp(1)): 16 % {q(0.16):.1f}, median {q(0.5):.1f}, 84 % {q(0.84):.1f},"
      f" mean {sum(means) + MJ_PLAN / MJ_LOOSE:.1f}; sigma_ln = 0.5 ln(q84/q16) = {0.5 * math.log(q(0.84) / q(0.16)):.2f}")
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
    """Marginal pmf of n for B = sum kappa x Gamma(m + 1) + sum of log-normal terms (median, width, cap).
    cap: a number (fixed censoring value), None (no cap), or a negative number -c: the cap is drawn per pseudo-experiment
    as c x Exp(1), the predictive draw of a no-credit zero-count bound (v4, Ph-C9). The Poisson sum per draw is taken over
    b +- (10 sqrt(b) + 10) only (v4: avoids the underflow of exp(-b) above b = 745; the tails beyond are below 1e-20)."""
    rnd = random.Random(seed)
    bs = []
    for _ in range(nd):
        b = sum(k * rnd.gammavariate(m + 1, 1.0) for k, m in gam)
        for med, sw, capv in lnn:
            x = med * math.exp(sw * rnd.gauss(0, 1))
            if capv is not None:
                x = min(x, capv if capv >= 0 else -capv * rnd.expovariate(1.0))
            b += x
        bs.append(b)
    kmax = int(max(bs) + 10 * math.sqrt(max(bs)) + 20)
    pmf = [0.0] * (kmax + 1)
    for b in bs:
        k0 = max(0, int(b - 10 * math.sqrt(b) - 10))
        k1 = min(kmax, int(b + 10 * math.sqrt(b) + 10))
        if b <= 0:
            pmf[0] += 1.0
            continue
        lp = k0 * math.log(b) - b - math.lgamma(k0 + 1)
        for k in range(k0, k1 + 1):
            pmf[k] += math.exp(lp)
            lp += math.log(b) - math.log(k + 1)
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
        # v4: Poisson terms in log space (exp(-sig) underflows above sig = 745)
        tot_, c, lp, ls = 0.0, 0.0, -sig, math.log(sig)
        cdf = []
        for j in range(nobs + 1):
            c += math.exp(lp)
            cdf.append(c)
            lp += ls - math.log(j + 1)
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


PLAN_REACH = [(0.0, 1026.0), (1.0, 971.0), (10.0, 866.0), (30.0, 799.0), (100.0, 717.0), (1e3, 548.0), (1e4, 393.0), (1e5, 243.0)]   # PLAN l.121, sigma_ln = 0 row (EST, v1 efficiencies); v5 (R1 (h)): 1e5 column added
MAPR = [(s95_fixed(b), r) for b, r in PLAN_REACH]


def reach_of(s95v):
    """reach read from the plan's sigma_ln = 0 row at equal one-bin expected limit (linear in ln s95)"""
    for (s1, r1), (s2, r2) in zip(MAPR, MAPR[1:]):
        if s95v <= s2:
            return r1 + (r2 - r1) * (math.log(max(s95v, s1)) - math.log(s1)) / (math.log(s2) - math.log(s1))
    return MAPR[-1][1]


print("\n[9b] projection per outcome: one-bin expected CLs limit on the signal yield and the reach read from the plan's table (EST)")
print("  mapping s95 -> reach (PLAN l.121, sigma_ln = 0 row; fixed B, median expected limit):", [(round(a, 1), int(b)) for a, b in MAPR])
MJK = (MJ_PLAN / MJ_LOOSE, 0)                          # multijet planning floor term (v4, P1 point 2)
kap = [(r[4], 0) for r in rows] + [MJK]
kz = SM_NTRIG["Z(nunu)+j"] / alloc["Z(nunu)+j"]
r07 = 35 / 48000.0
PU_R07 = NTRIG * r07                                   # direct v1 rate at R07
PU_R08 = (PU_R07 / (0.2470 / r07), PU_R07 / (49.72 / 0.2470))   # width-step fall x339 (R06->R07) and x201 (R05->R06)
CHI = (2 / 35.0, 32 / 126.0, 12 / 32.0)                # v1 conditional fit-probability fractions R09, R10, R11 (D4 l.266, UNVERIFIED)
PU_R09 = tuple(x * CHI[0] for x in PU_R08)
PU_R11 = tuple(x * CHI[0] * CHI[1] * CHI[2] for x in PU_R08)
PU_NC = NTRIG * U68 / 96000                            # no-credit value of the pile-up term (68 % upper value)
PU_CAP = -NTRIG / 96000                                # v4 (Ph-C9): the cap is drawn as (N_trig / 96,000) x Exp(1) in every pseudo-experiment
print(f"  EST pile-up medians from v1 numbers: R07 direct {PU_R07:.3g}; R08 {PU_R08[0]:.0f}-{PU_R08[1]:.0f} (width-step fall x339 / x201);"
      f" R09 {PU_R09[0]:.1f}-{PU_R09[1]:.1f}; R11 {PU_R11[0]:.2f}-{PU_R11[1]:.2f}; R14: no v1 number, at most the R11 value; no-credit value {PU_NC:.0f}"
      f" (68 % upper value; mean {NTRIG / 96000:.0f}; drawn as {NTRIG / 96000:.0f} x Exp(1) in the projection)")
W_PU = {"R08": 0.43, "R09": 0.59, "R11": 1.29, "R14": 2.47}    # s_tot of [12], occupancy model, no crossing test
for rr, med in (("R08", PU_R08), ("R09", PU_R09), ("R11", PU_R11), ("R14", PU_R11)):
    print(f"    {rr}: B50 {med[0]:.3g}-{med[1]:.3g}; B84 = B50 x exp({W_PU[rr]}) = {med[0] * math.exp(W_PU[rr]):.3g}-{med[1] * math.exp(W_PU[rr]):.3g}"
          + (f" (2S crossing test PASS, s_tot 1.30: {med[0] * math.exp(1.30):.3g}-{med[1] * math.exp(1.30):.3g}; v4, P7: no credit from the fit-probability and shape crossing comparisons)" if rr == "R14" else ""))
pu9 = 0.5 * (PU_R09[0] + PU_R09[1])
pu8 = 0.5 * (PU_R08[0] + PU_R08[1])
pmf_v2, _ = pmf_pred([(r[4], 0) for r in rows_v2])
print(f"  check against the constructive review (v2 floors, all empty): s95 = {s95_pmf(pmf_v2, quant_pmf(pmf_v2, 0.5)):.1f} (review: 24.1)")
PU9 = (pu9, 0.59, PU_CAP)


def rfmt(sv):
    return f"< {MAPR[-1][1]}" if sv > MAPR[-1][0] else f"{reach_of(sv):.0f}"


def wm(m):
    return math.sqrt(trigamma(m + 1))


# (alpha): DIF and hard-scatter conversions from v1's own attributed counts per 500 full-pile-up events (Table 4.4b):
# DIF 2 at R06, 1 at R07; gamma 13 at R06, 2 at R07. R07 value = N_t x count / 500; R08 = R07 / fall; R09 = R08 (no credit)
# or R08 x 2/35 (v1's pile-up fit-probability fraction as credit). Width = count width w_m of the R07 count (+) one
# untested width step at F = 2 (b0 = ln 2), in quadrature [E].
DIF_R07 = NTRIG * RATE["DIF"] * 1 / 500.0
GAM_R07 = NTRIG * RATE["gamma"] * 2 / 500.0
W_DIF, W_GAM = math.sqrt(wm(1) ** 2 + math.log(2) ** 2), math.sqrt(wm(2) ** 2 + math.log(2) ** 2)
print(f"  (alpha) inputs: R07 DIF {DIF_R07:.3g} (1 count in 500), conversions {GAM_R07:.3g} (2 in 500; R06: {NTRIG * RATE['gamma'] * 13 / 500:.3g});"
      f" uncertainty of the v1-based size: sqrt(w_m^2 + ln2^2) = factor e^{W_DIF:.2f} (DIF, m = 1), e^{W_GAM:.2f} (conversions, m = 2) [a projection uncertainty, not a width of the v2 term]")
# v5 (R1): is v1's conversion fall pile-up-like? v1 counts per 500 events (background.json -> cprime.gamma.rows, cprime.dif.rows):
# conversions 86 (R05) -> 13 (R06) -> 2 (R07); DIF 2 (R06) -> 1 (R07). Pile-up fall per width step x339 (R06->R07), x201 (R05->R06).
FALL_PU = (0.2470 / r07, 49.72 / 0.2470)
p_ge = lambda n, mu: sum(pois_pmf(k, mu) for k in range(n, n + 200))   # upper tail summed directly (no 1 - cdf cancellation)
print(f"  v5 (R1) conversion fall test: v1 measured x{86 / 13:.1f} (R05->R06, 86 -> 13) and x{13 / 2:.1f} (R06->R07, 13 -> 2); with a pile-up-like fall from 13 at R06:"
      f" mu(R07) = {13 / FALL_PU[0]:.3f} / {13 / FALL_PU[1]:.3f} counts (x339 / x201), P(>= 2) = {p_ge(2, 13 / FALL_PU[0]):.1e} / {p_ge(2, 13 / FALL_PU[1]):.1e};"
      f" from 86 at R05: mu(R06) = {86 / FALL_PU[0]:.2f} / {86 / FALL_PU[1]:.2f}, P(>= 13) = {p_ge(13, 86 / FALL_PU[0]):.1e} / {p_ge(13, 86 / FALL_PU[1]):.1e};"
      f" DIF from 2 at R06: P(>= 1 at R07) = {p_ge(1, 2 / FALL_PU[0]):.2%} / {p_ge(1, 2 / FALL_PU[1]):.2%}")
kap_nodif = [(r[4], 0) for r in rows if r[0] != "DIF"] + [MJK]
ALPHA = {}
for tag, fd, fg in (("alpha1 (pile-up fall x339)", 0.2470 / r07, 0.2470 / r07), ("alpha1 (pile-up fall x201)", 49.72 / 0.2470, 49.72 / 0.2470),
                    ("alpha2 (own R06->R07 fall: DIF x2, conversions x6.5)", 2.0, 13 / 2.0),
                    ("alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339)", 0.2470 / r07, 13 / 2.0),   # v5 (R1)
                    ("alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201)", 49.72 / 0.2470, 13 / 2.0)):
    for credit in (False, True):
        c_ = CHI[0] if credit else 1.0
        ALPHA[(tag, credit)] = (DIF_R07 / fd * c_, GAM_R07 / fg * c_)
        print(f"    {tag}, {'with' if credit else 'no'} fit-probability credit at R09: DIF {DIF_R07 / fd * c_:.3g}, conversions {GAM_R07 / fg * c_:.3g}")
pmf_cache = {}


def row(lab, gam, lnn, store=None, pred=False):
    med_sum = sum(k * (m + 0.67) for k, m in gam) + sum(x[0] for x in lnn)
    if med_sum > 5000 and not pred:   # v5 (R1): pred=True forces the predictive (counted-ceiling) branch
        b = med_sum
        sv = s95_fixed(b)
        print(f"  | {lab} | ≈ {b:.0f} (sum of medians; fixed-B limit, an upper edge of the reach) | | {sv:.0f} | {rfmt(sv)} |")
        if store is not None:
            pmf_cache[store] = (b, b, b, sv, sv, sv)
        return
    pmf, (b16, b50, b84) = pmf_pred(gam, lnn)
    lim = [s95_pmf(pmf, quant_pmf(pmf, f)) for f in (0.16, 0.5, 0.84)]
    print(f"  | {lab} | {b16:.0f} / {b50:.0f} / {b84:.0f} | {0.5 * math.log(b84 / b16):.2f} | {lim[1]:.1f} [{lim[0]:.1f}, {lim[2]:.1f}] | {rfmt(lim[1])} [{rfmt(lim[2])}, {rfmt(lim[0])}] |")
    if store is not None:
        pmf_cache[store] = (b16, b50, b84) + tuple(lim)


print("  | outcome | B16 / B50 / B84 | sigma_ln = 0.5 ln(B84/B16) | s95 median [16 %, 84 %] | reach, EST (GeV): median [84 % edge, 16 % edge] |")
row("floors only (every count zero, every ceiling H empty, no pile-up term; multijets at their planning floor)", kap, (), "floors")
row("R09-like: floors + EST pile-up median %.0f (s_tot 0.59)" % pu9, kap, (PU9,), "R09")
row("R08-like: floors + EST pile-up median %.0f (s_tot 0.43)" % pu8, kap, ((pu8, 0.43, PU_CAP),), "R08")
kap_noz = [(r[4], 0) for r in rows if r[0] != "Z(nunu)+j"] + [MJK]
for mh in (3, 10, 30, 100):
    row("R09-like, Z(nunu) enters at its ceiling (estimator not credited): m_H = %d simulated ceiling counts (%.0f events)" % (mh, kz * mh),
        kap_noz + [(kz, mh)], (PU9,), "Z%d" % mh)
b1000 = kz * 1001 + pu9 + sum(k for k, m in kap_noz)
print(f"  m_H = 1000: B about {b1000:.0f}, fixed-B s95 = {s95_fixed(b1000):.0f}, reach {rfmt(s95_fixed(b1000))} GeV")
row("v5 (Ph-C2): R09-like, Z(nunu) enters at its ceiling (estimator not credited): m_H = 1000 simulated ceiling counts (%.0f events), with the count width" % (kz * 1000),
    kap_noz + [(kz, 1000)], (PU9,), "Z1000")
MZ = alloc["Z(nunu)+j"]
LATE = list(PROXY8) + list(ADD_PLAN)
for mh in (10, 30, 100):
    gam_b = [(r[4], 0) for r in rows if r[0] not in LATE] + [(r[4], mh * r[2] / MZ) for r in rows if r[0] in LATE] + [(MJ_PLAN / MJ_LOOSE, mh * MJ_LOOSE / MZ)]
    row("(beta) Z(nunu) tested and credited (at its floor); the eight proxied processes, the additions and multijets at H, H per event as Z(nunu) with m_H = %d" % mh,
        gam_b, (PU9,), "beta%d" % mh)
SMSET = [p for p in SM_NTRIG]
for mh in (10, 30, 100):
    gam_g = [(r[4], 0) for r in rows if r[0] not in SMSET] + [(r[4], mh * r[2] / MZ) for r in rows if r[0] in SMSET] + [(MJ_PLAN / MJ_LOOSE, mh * MJ_LOOSE / MZ)]
    row("(gamma) every SM ceiling at H per event as Z(nunu) (scales with N_trig, x%.2f), m_H = %d" % ((sum(SM_NTRIG.values()) + MJ_PLAN) / NZ, mh),
        gam_g, (PU9,), "gamma%d" % mh)
# How the (alpha) terms enter the projection: without credit they are counted ceilings (the term at H, counted on its pool
# share with m = B / kappa counts, like the Z(nunu) ceiling rows: DIF kappa of the pool, conversions with the Z(nunu) kappa);
# with credit, the counted size times v1's fit-probability fraction as a conditional applied one rung beyond where it is
# measured, a log-normal of width s_tot = sqrt(0.135^2 + 0.405^2) = 0.43 (STR §4.0 point 7, F = 1.5).
K_DIF = [r[4] for r in rows if r[0] == "DIF"][0]
W_COND1 = math.sqrt((math.log(1.5) / 3) ** 2 + math.log(1.5) ** 2)
for (tag, credit), (d_, g_) in ALPHA.items():
    lab_ = "%s, %s: DIF %.3g + conversions %.3g" % (tag, "fit-probability credit at R09" if credit else "no credit (R09 = R08)", d_, g_)
    if credit:
        row(lab_, kap_nodif, (PU9, (d_, W_COND1, None), (g_, W_COND1, None)), (tag, credit))
    else:
        row(lab_, kap_nodif + [(K_DIF, d_ / K_DIF), (kz, g_ / kz)], (PU9,), (tag, credit), pred=tag.startswith("alpha1'"))
        if tag.startswith("alpha1'"):
            bfx = pmf_cache[(tag, credit)][1]
            print(f"    v5 (R1): the same at fixed B = B50 {bfx:.0f} (background known exactly): s95 {s95_fixed(bfx):.1f}, reach {rfmt(s95_fixed(bfx))} GeV")
a1 = [pmf_cache[("alpha1 (pile-up fall x339)", False)], pmf_cache[("alpha1 (pile-up fall x201)", False)]]
# v6 (T1): the (alpha1') no-credit row (i) counted, as above, and (ii) with the conversion term as a log-normal of median g and
# width sqrt(w^2 + 1/(m + 1)), m = g / kz (count width (+) a normalisation width w); DIF counted, kap_nodif and PU9 unchanged.
# Photon rate factor: background.json -> cprime.gamma.rate.nt_weighted_mean / .value = 0.25518676537664065 / 0.3786327036399709
# (read this session; the script's RATE["gamma"] = 0.379 is the .value, "max over SM processes (conservative)").
F_GAM = {"max rate 0.379": 1.0, "N_trig-weighted rate 0.255": 0.25518676537664065 / 0.3786327036399709}
W_NORM = 0.17   # |ln 0.84|: normalisation width of the SM terms (generator difference, STR §4.7); K, luminosity, material not included
S95_243 = MAPR[-1][0]


def rfmt6(sv):
    return rfmt(sv) + (" (beyond the plan's table; PLAN sigma_ln = 0.2 row: below 200 GeV at B = 1e4)" if sv > S95_243 else "")


print(f"  v6 (T1): (alpha1') no credit with a normalisation width on the conversion term (s95 = {S95_243:.1f} <-> 243 GeV, the last column of the plan's table):")
A1P6 = {}
for tag in ("alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339)", "alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201)"):
    d_, g0_ = ALPHA[(tag, False)]
    for rk, fr in F_GAM.items():
        g_ = g0_ * fr
        m_ = g_ / kz
        pm_, bq_ = pmf_pred(kap_nodif + [(K_DIF, d_ / K_DIF), (kz, m_)], (PU9,))
        l_ = [s95_pmf(pm_, quant_pmf(pm_, f)) for f in (0.5, 0.84)]
        A1P6[(tag, rk, 0.0)] = (bq_[1],) + tuple(l_)
        print(f"    {tag[-5:-1]}, {rk}: conversions {g_:.3g}; (i) counted: B16/B50/B84 {bq_[0]:.0f} / {bq_[1]:.0f} / {bq_[2]:.0f}, s95 median {l_[0]:.1f} [84 % {l_[1]:.1f}],"
              f" reach {rfmt(l_[0])} [84 % edge {rfmt(l_[1])}] GeV; fixed B = B50: s95 {s95_fixed(bq_[1]):.1f}, reach {rfmt(s95_fixed(bq_[1]))} GeV")
        for w in (0.03, 0.05, W_NORM):
            pm_, bq_ = pmf_pred(kap_nodif + [(K_DIF, d_ / K_DIF)], (PU9, (g_, math.sqrt(w ** 2 + 1 / (m_ + 1)), None)))
            l_ = [s95_pmf(pm_, quant_pmf(pm_, f)) for f in (0.5, 0.84)]
            A1P6[(tag, rk, w)] = (bq_[1],) + tuple(l_)
            lw = (" = normalisation width of the SM terms, |ln 0.84| (generator difference, §4.7); K, luminosity and material not included"
                  if w == W_NORM else "")
            print(f"      (ii) w = {w:.2f}{lw}: B50 {bq_[1]:.0f}, s95 median {l_[0]:.1f} [84 % {l_[1]:.1f}], reach {rfmt6(l_[0])} [84 % edge {rfmt(l_[1])}] GeV")
UP6 = []
for tag in ("alpha1 (pile-up fall x339)", "alpha1 (pile-up fall x201)"):
    d_, g_ = ALPHA[(tag, False)]
    md_, mg_ = d_ / K_DIF, g_ / kz
    pm_, bq_ = pmf_pred(kap_nodif, (PU9, (d_, math.sqrt(W_NORM ** 2 + 1 / (md_ + 1)), None), (g_, math.sqrt(W_NORM ** 2 + 1 / (mg_ + 1)), None)))
    l_ = [s95_pmf(pm_, quant_pmf(pm_, f)) for f in (0.5, 0.84)]
    UP6.append((bq_[1],) + tuple(l_))
    print(f"  v6 (T1) upside with w = {W_NORM}: {tag}, no credit, DIF and conversions log-normal of width sqrt(w^2 + 1/(m + 1)): B50 {bq_[1]:.0f},"
          f" median reach {rfmt(l_[0])} [84 % edge {rfmt(l_[1])}] GeV (statistics-only rows above: {rfmt(pmf_cache[(tag, False)][4])} [{rfmt(pmf_cache[(tag, False)][5])}])")
pm_, bq_ = pmf_pred(kap_noz, (PU9, (kz * 101, math.sqrt(W_NORM ** 2 + 1 / 101), None)))
l_ = [s95_pmf(pm_, quant_pmf(pm_, f)) for f in (0.5, 0.84)]
Z100_6 = (bq_[1],) + tuple(l_)
print(f"  v6 (T1) upside with w = {W_NORM}: R09-like, Z(nunu) ceiling m_H = 100 as a log-normal of width sqrt(w^2 + 1/(m + 1)) around kz (m + 1): B50 {bq_[1]:.0f},"
      f" median reach {rfmt(l_[0])} [84 % edge {rfmt(l_[1])}] GeV (count width only: {rfmt(pmf_cache['Z100'][4])} [{rfmt(pmf_cache['Z100'][5])}])")
# v6 (T2): does any (alpha) branch avoid the day-15 pause (class limit B50 <= 300)?
G_A1P = ALPHA[("alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339)", False)][1]
A1P_CR = [pmf_cache[("alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x%s)" % x, True)][1] for x in ("339", "201")]
print(f"  v6 (T2) day-15 class limit B50 <= 300: (alpha1) no credit B50 {a1[0][1]:.0f} / {a1[1][1]:.0f} (x339 / x201) -> above; decays in flight alone"
      f" DIF {ALPHA[('alpha1 (pile-up fall x339)', False)][0]:.0f} / {ALPHA[('alpha1 (pile-up fall x201)', False)][0]:.0f} events -> above")
for tag in ("alpha1 (pile-up fall x339)", "alpha1 (pile-up fall x201)"):
    d_ = ALPHA[(tag, False)][0]
    pm_, bq_ = pmf_pred(kap_nodif + [(K_DIF, d_ / K_DIF)], (PU9,))
    print(f"    {tag}, conversions removed entirely (floors + pile-up + DIF counted): B50 {bq_[1]:.0f} -> {'above' if bq_[1] > 300 else 'at or below'} 300")
for tag in ("alpha1 (pile-up fall x339)", "alpha1 (pile-up fall x201)"):
    g_ = ALPHA[(tag, False)][1]
    print(f"    conversion rejection needed to reach the {tag} conversion level: {G_A1P:.0f} / {g_:.0f} = x{G_A1P / g_:.1f} ({1 - g_ / G_A1P:.1%}); not sufficient by itself (DIF above)")
print(f"    avoided only with B50 <= 300: (alpha1) with fit-probability credit B50 {pmf_cache[('alpha1 (pile-up fall x339)', True)][1]:.0f} / {pmf_cache[('alpha1 (pile-up fall x201)', True)][1]:.0f};"
      f" (alpha1') with credit {A1P_CR[0]:.0f} / {A1P_CR[1]:.0f} (above)")
# v7 (U1, verdict cycle 6 §7 item 1): (i) conversions removed and the DIF size x e^-1 (the factor-e planning uncertainty);
# (ii) the day-15 projection basis (Df-9, §11.7 rule 1: own hits before CKF, no S_CKF): the (alpha1') DIF and conversion
# terms x 1/(1 - eps_pair), eps_pair assumed 0.8-0.98 (not measured); sum of medians (fixed-B reading, as in row() above 5000).
U1_I = [pmf_pred(kap_nodif + [(K_DIF, ALPHA[(t_, False)][0] * math.exp(-1) / K_DIF)], (PU9,))[1][1] for t_ in ("alpha1 (pile-up fall x339)", "alpha1 (pile-up fall x201)")]
U1_II = {eps: [sum(k * (m + 0.67) for k, m in kap_nodif + [(K_DIF, ALPHA[(t_, False)][0] / (1 - eps) / K_DIF), (kz, ALPHA[(t_, False)][1] / (1 - eps) / kz)]) + pu9 for t_ in ("alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339)", "alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201)")] for eps in (0.8, 0.98)}
print(f"    v7 (U1): (alpha1) conversions removed, DIF x e^-1 (both falls): B50 {U1_I[0]:.0f} / {U1_I[1]:.0f} (x339 / x201) -> {'at or below' if max(U1_I) <= 300 else 'above'} 300")
print(f"    v7 (U1): (alpha1') on the day-15 own-hit basis, conversions and DIF x 1/(1 - eps_pair) at eps_pair = 0.8 / 0.98 (assumed, not measured; photon rate 0.379): B50 ≈ {U1_II[0.8][0]:.3g}-{U1_II[0.8][1]:.3g} / {U1_II[0.98][0]:.3g}-{U1_II[0.98][1]:.3g} (sum of medians)")
# v5 (R1 (c)): the factor-e size uncertainty of (alpha1) as size rows B x e^(-1), B x e^(+1) (counted-ceiling reading), and the
# log-normal reading (width e^1.06 / e^0.94 on DIF / conversions) that is shown but not used.
for tag in ("alpha1 (pile-up fall x339)", "alpha1 (pile-up fall x201)"):
    d_, g_ = ALPHA[(tag, False)]
    out_ = []
    for ex in (-1, 1):
        pm_, bq_ = pmf_pred(kap_nodif + [(K_DIF, d_ * math.exp(ex) / K_DIF), (kz, g_ * math.exp(ex) / kz)], (PU9,))
        l_ = [s95_pmf(pm_, quant_pmf(pm_, f)) for f in (0.5, 0.84)]
        out_.append(f"B x e^{ex:+d}: B50 {bq_[1]:.0f}, median reach {rfmt(l_[0])}, 84 % edge {rfmt(l_[1])}")
    pm_, bq_ = pmf_pred(kap_nodif, (PU9, (d_, W_DIF, None), (g_, W_GAM, None)))
    l_ = [s95_pmf(pm_, quant_pmf(pm_, f)) for f in (0.5, 0.84)]
    print(f"  v5 (R1) {tag}, no credit: " + "; ".join(out_) + f"; log-normal reading (not used): B16/B50/B84 {bq_[0]:.0f} / {bq_[1]:.0f} / {bq_[2]:.0f},"
          f" median reach {rfmt(l_[0])}, 84 % edge {rfmt(l_[1])} GeV")
e0 = pmf_cache["R09"]
print(f"  HEADLINE (P2): empty ceilings, R09-like: reach {rfmt(e0[5])} GeV at the 84 % edge, median {rfmt(e0[4])}; (alpha1) no credit: B50 {a1[0][1]:.0f}-{a1[1][1]:.0f},"
      f" median reach {rfmt(a1[1][4])}-{rfmt(a1[0][4])} GeV, 84 % edge {rfmt(a1[1][5])}-{rfmt(a1[0][5])}; (beta) m_H = 10: median {rfmt(pmf_cache['beta10'][4])}, 84 % edge {rfmt(pmf_cache['beta10'][5])};"
      f" negligible background 1026 GeV")
a1p = [pmf_cache[("alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339)", False)],
       pmf_cache[("alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201)", False)]]
print(f"  HEADLINE v5 (R1): (alpha1') no credit: B50 {a1p[0][1]:.0f}-{a1p[1][1]:.0f}, median reach {rfmt(a1p[0][4])}-{rfmt(a1p[1][4])} GeV, 84 % edge {rfmt(a1p[0][5])}-{rfmt(a1p[1][5])},"
      f" fixed B {rfmt(s95_fixed(a1p[0][1]))}-{rfmt(s95_fixed(a1p[1][1]))}; (beta) m_H = 10 / 30 / 100: median {rfmt(pmf_cache['beta10'][4])} / {rfmt(pmf_cache['beta30'][4])} / {rfmt(pmf_cache['beta100'][4])},"
      f" 84 % edge {rfmt(pmf_cache['beta10'][5])} / {rfmt(pmf_cache['beta30'][5])} / {rfmt(pmf_cache['beta100'][5])}; Z(nunu) m_H = 1000 with the count width: B50 {pmf_cache['Z1000'][1]:.0f},"
      f" median reach {rfmt(pmf_cache['Z1000'][4])}")
T6, R6 = ("alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339)", "alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201)"), tuple(F_GAM)
print(f"  HEADLINE v6 (T1): (alpha1') no credit, photon rate 0.255-0.379: B50 {A1P6[(T6[0], R6[1], 0.0)][0]:.0f}-{A1P6[(T6[1], R6[0], 0.0)][0]:.0f};"
      f" with the normalisation width {W_NORM}: s95 median {min(A1P6[(t, r, W_NORM)][1] for t in T6 for r in R6):.0f}-{max(A1P6[(t, r, W_NORM)][1] for t in T6 for r in R6):.0f}"
      f" -> reach {rfmt(min(A1P6[(t, r, W_NORM)][1] for t in T6 for r in R6))} GeV (already at w = 0.03: 84 % edge {rfmt(max(A1P6[(t, r, 0.03)][2] for t in T6 for r in R6))});"
      f" statistics-only (count width): 84 % edge {rfmt(max(A1P6[(t, r, 0.0)][2] for t in T6 for r in R6))}-{rfmt(min(A1P6[(t, r, 0.0)][2] for t in T6 for r in R6))},"
      f" median {rfmt(max(A1P6[(t, r, 0.0)][1] for t in T6 for r in R6))}-{rfmt(min(A1P6[(t, r, 0.0)][1] for t in T6 for r in R6))},"
      f" fixed B {rfmt(s95_fixed(max(A1P6[(t, r, 0.0)][0] for t in T6 for r in R6)))}-{rfmt(s95_fixed(min(A1P6[(t, r, 0.0)][0] for t in T6 for r in R6)))};"
      f" (alpha1) with w = {W_NORM}: 84 % edge {rfmt(UP6[1][2])}-{rfmt(UP6[0][2])}, median {rfmt(UP6[1][1])}-{rfmt(UP6[0][1])}; Z(nunu) m_H = 100 with w = {W_NORM}: 84 % edge {rfmt(Z100_6[2])}")
print(f"  one-bin limit with every zero-count term dropped: {-math.log(0.05):.2f}; with the floors: {e0[4] if False else s95_pmf(pmf_pred(kap)[0], quant_pmf(pmf_pred(kap)[0], 0.5)):.1f}")
for c_h in (C_POOL + RESERVE2, 2 * C_POOL):
    kp = [(r[4], 0) for r in floor_table(c_h)] + [MJK]
    pmf, (b16, b50, b84) = pmf_pred(kp, (PU9,))
    l50 = s95_pmf(pmf, quant_pmf(pmf, 0.5))
    print(f"  R09-like with the pool at {c_h:.0f} CPU-h, ceilings empty: B50 {b50:.0f}, s95 {l50:.1f}, reach {rfmt(l50)} GeV")
for mh in (120, 125, 130, 135):
    pmf, (b16, b50, b84) = pmf_pred(kap_noz + [(kz, mh)], (PU9,))
    l50 = s95_pmf(pmf, quant_pmf(pmf, 0.5))
    print(f"  class limit of decision point 2 (B50 = 300 events): m_H = {mh} gives B50 {b50:.0f}, s95 {l50:.0f}, reach {rfmt(l50)} GeV")
print(f"  change of the bound against v1's best B84 of 1.2346e6: empty ceilings B84 = {e0[2]:.0f} -> {math.log10(1.2346e6 / e0[2]):.1f} decades;"
      f" Z(nunu) m_H = 100: B84 = {pmf_cache['Z100'][2]:.0f} -> {math.log10(1.2346e6 / pmf_cache['Z100'][2]):.1f}; (alpha1) no credit x201: B84 = {a1[1][2]:.0f} -> {math.log10(1.2346e6 / a1[1][2]):.1f}")
print(f"  projection rule per term: max(zero-count floor, N_t x H); one counted ceiling event of Z(nunu) at the final sample size = {kz:.2f} events in 3 ab^-1")
print(f"  R07-direct baseline, size from v1 counts: pile-up direct {PU_R07:.3g} + DIF attributed 1/500 x N_t = {NTRIG * RATE['DIF'] / 500:.3g} events (order 1e5)")
# P3 / P14: EST of the Z(nunu) ceiling at R08. v1's attributed hard-scatter rate with pile-up (after CKF removal) is 4.51 / 0.0162
# per event at R05 / R06 (fall x278); two more width steps at x100-300 each give H_CKF(R08). Option (a) of Df-9 classifies on all
# own hits: H_a = H_CKF / (1 - eps_pair), eps_pair = probability that CKF removes a passing own-hit configuration (assumed 0.8-0.98).
H_CKF = (0.0162 / 300 ** 2, 0.0162 / 100 ** 2)
print(f"  P3/P14 EST: H_CKF(R08) = {H_CKF[0]:.2g}-{H_CKF[1]:.2g} per event; m_H(CKF) in {MZ:.3g} events = {H_CKF[0] * MZ:.1f}-{H_CKF[1] * MZ:.1f};"
      f" pilot (2.3e6 events) expects {H_CKF[0] * PILOT_HS:.1f}-{H_CKF[1] * PILOT_HS:.1f} counts at R08")
for eps in (0.8, 0.9, 0.98):
    print(f"    option (a), eps_pair = {eps}: m_H = {H_CKF[0] * MZ / (1 - eps):.0f}-{H_CKF[1] * MZ / (1 - eps):.0f}; pilot counts {H_CKF[0] * PILOT_HS / (1 - eps):.1f}-{H_CKF[1] * PILOT_HS / (1 - eps):.1f}")
# v5 (R1, point 4): the same with the conversions' own fall (x6.5 per width step, v1's 13 -> 2) instead of the pile-up fall.
# Z(nunu) photon rate per event: background.json -> cprime.gamma.rate.per_process.Znunu_j = 0.2306 (read this session).
GZ = 0.23059926668409783
EV_GZ = NZ * GZ * (2 / 500.0) / 6.5
print(f"  v5 (R1) P3/P14 EST with the conversions' own fall: Z(nunu) conversion part at R08 = {NZ:.3g} x {GZ:.4f} x (2/500) / 6.5 = {EV_GZ:.3g} events in 3 ab^-1;"
      f" m_H = {EV_GZ / kz:.3g} in {MZ:.3g} pool events, {EV_GZ / kz * PILOT_HS / MZ:.3g} in the pilot's {PILOT_HS:.2g} events (day-15 class limit m_H = 125)")

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


def one_rung(L, smod, sg, K, delta=None, v2rule=False, rt05=False):
    """Verdict probabilities of a one-rung test. v3 rule: pass |x| <= min(L, T05); FAIL |x| > min(L + 2 sg, TK);
    INVESTIGATE between; the re-test (same delta, new eps) passes if |x'| <= min(L, TK).
    v2 rule: FAIL if |x| > L (no route for (a)); (b): FAIL p < 0.05/K, INVESTIGATE p < 0.05, re-test needs p' > 0.05."""
    tau = math.sqrt(smod ** 2 + sg ** 2)
    t05, tk = inv_phi(0.975) * tau, inv_phi(1 - 0.025 / K) * tau
    if v2rule:
        lo_, up_, rt_ = min(L, t05), min(L, tk), min(L, t05)
    else:
        lo_, up_, rt_ = min(L, t05), min(L + 2 * sg, tk), (min(L, t05) if rt05 else min(L, tk))

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
print(f"  v3 ceiling test per rung (one-sided, FAIL at p < 0.001, INVESTIGATE at p < 0.05, re-test FAIL at p' < 0.05): false fail at the boundary P = H: {0.001 + 0.049 * 0.05:.4f} per test;"
      f" over 16 / 30 / 55 such tests: {1 - (1 - 0.00345) ** 16:.3f} / {1 - (1 - 0.00345) ** 30:.3f} / {1 - (1 - 0.00345) ** 55:.3f} (the finding P6)")
# v4 (P6): one ceiling verdict per term. p_t = Sidak-corrected minimum one-sided p over the term's evaluable rungs,
# p_t = 1 - (1 - min_r p_r)^n_r (exact for independent rungs, conservative for nested ones). Family: the T_C terms with a
# ceiling test; Bonferroni alpha_c = 0.05 / T_C. FAIL at p_t < alpha_c; INVESTIGATE for alpha_c <= p_t < 5 alpha_c, one re-test on
# a fresh unbiased sample, FAIL if p_t' < alpha_c. Sub-topology tests are dropped (P4 (iii), default).
CEIL_TERMS = ["DIF", "NI 22 mm", "NI 30 mm", "NI 61.5 mm"] + list(SM_NTRIG) + ["multijets"]
T_C = len(CEIL_TERMS)
A_C = 0.05 / T_C
p_term = A_C + 4 * A_C * A_C
p_fam_c = 1 - (1 - p_term) ** T_C
print(f"  v4 ceiling family (P6): {T_C} terms ({', '.join(CEIL_TERMS)}); alpha_c = 0.05 / {T_C} = {A_C:.5f}; per-term false FAIL at the boundary"
      f" {A_C:.5f} + 4 alpha_c x alpha_c = {p_term:.5f}; family-wise {p_fam_c:.4f}; limiting case: a term strictly below its ceiling fails less often")
for nr in (2, 3, 4):
    print(f"    Sidak over {nr} rungs: per-rung threshold equivalent to p_t < alpha_c is p_r < {1 - (1 - A_C) ** (1 / nr):.5f}")
ELIG_CL = {fs: 1 - (1 - PT[(2.0, fs, 1.0)] / 2) ** N2 * (1 - PT[(2.0, fs, 1.0)] ** 2) for fs in (0.0, 0.5, 1.0)}
for fs, e_ in ELIG_CL.items():
    print(f"    s_model = {fs:.1f} x cap: closure family removes a selection with {e_:.3f}; with the ceiling family at its boundary: {1 - (1 - e_) * (1 - p_fam_c):.3f}")
E_ALL = (1 - (1 - ELIG_CL[0.0]) * (1 - p_fam_c), 1 - (1 - ELIG_CL[1.0]) * (1 - p_fam_c))
print(f"  v4 statement for Df-2 / §4.12: a correct-as-declared analysis loses a selection to a false FAIL with probability at most {E_ALL[0]:.1%}-{E_ALL[1]:.1%}"
      f" (closure family {ELIG_CL[0.0]:.1%}-{ELIG_CL[1.0]:.1%}, ceiling family {p_fam_c:.1%} at the boundary)")
print("  K-C1: price of the re-test threshold p' >= 0.05/K against v2's p' > 0.05 (one rung at the evaluable limit, s_model at the cap), P(final PASS | true |ln r| = x ln F):")
for mult in (1.0, 1.25, 1.5):
    L_ = math.log(2)
    a_ = one_rung(L_, L_ / 3, L_ / 3, K_FAM, delta=mult * L_)
    b_ = one_rung(L_, L_ / 3, L_ / 3, K_FAM, delta=mult * L_, rt05=True)
    print(f"    x = {mult}: re-test at 0.05/K {1 - a_[3]:.3f}; re-test at 0.05 {1 - b_[3]:.3f}; no re-test (direct PASS only) {a_[0]:.3f}")


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
P_EV = 1 - sum(pois_pmf(k, N_TARGET) for k in range(N_EVAL))
print(f"  P10 fluctuation route: the four terms sized at an expected {N_TARGET} (DIF, W(tau_h), W(tau_l), tt 1l; Z(nunu) at 81 is evaluable with"
      f" P = {1 - sum(pois_pmf(k, 80.8) for k in range(N_EVAL)):.4f}): P(at least one NOT TESTED) = 1 - {P_EV:.3f}^4 = {1 - P_EV ** 4:.3f} (before the 33-57 % errors of v1's rates)")
print(f"  P10 B3-c nominal edge: 58 expected late counts, 55 needed: P(N >= 55) = {1 - sum(pois_pmf(k, 58) for k in range(55)):.2f}")
print(f"  K-C9 C2-c family: 4 rung families x 2 densities = 8 tests; |z| < 2 each gives a false 'not converged' in {1 - (1 - 2 * Phi(-2)) ** 8:.2f};"
      f" Bonferroni |z| < {inv_phi(1 - 0.05 / 16):.2f} gives {1 - (1 - 0.05 / 8) ** 8:.3f}")
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
print("    v3 row (withdrawn, P7): occupancy model, crossing tests PASS in the fit-probability, 2S and shape families:", {("R%02d" % r): round(s_tot(c15, 1.5, 1, 0, cross=[c15] * ncross[r]), 2) for r in RUNGS})
# v4 (P7, Df-2 option (a)): the occupancy comparisons at R09xR06, R11xR06 and R15-R20xR06 share the finder-candidate pass
# fraction with the derivation (STR §4.5) and are consistency checks: no distance credit. Only the 2S crossing test (hits
# only) can remove its family (R12-R14) from d_out; the width step R07 -> R08 always counts (d_in = 1).
d_out_2s = {r: (r - 8) - min(3, max(0, r - 11)) for r in RUNGS}
print("    v4: occupancy model, only the 2S crossing test PASS (fit-probability and shape comparisons are consistency checks):",
      {("R%02d" % r): round(s_tot(c15, 1.5, 1, d_out_2s[r], cross=[c15] * (1 if r >= 12 else 0)), 2) for r in RUNGS})
print("    occupancy model, as above and three evaluable cumulative rungs in the width family with sigma_b = 0.03:", {("R%02d" % r): round(s_tot(c15, 1.5, 1, 0, cross=[c15] * ncross[r], sb=0.03), 2) for r in RUNGS})
d2s = {8: 0, 9: 0, 11: 0, 14: 3, 17: 3, 20: 3}
print("    promotion pi_k tested at R06-R07 (conditional row: DIF only if the enrichment is >= 4), no crossing test:", {("R%02d" % r): round(s_tot(c2, 2.0, 1, d2s[r]), 2) for r in RUNGS})
# v4 (P8): the expected case. One evaluable width rung (R06): n = 1, b_hat = 0, sigma_b = b0 = ln 2; d_in = 2 (R07, R08).
print("    v4 (P8): promotion pi_k tested at R06 only (expected for DIF at G < 4 and for every B4 term), no crossing test:",
      {("R%02d" % r): round(s_tot(c2, 2.0, 2, d2s[r]), 2) for r in RUNGS},
      "; with a 2S crossing PASS:", {("R%02d" % r): round(s_tot(c2, 2.0, 2, 0, cross=[c2] * (1 if r >= 12 else 0)), 2) for r in RUNGS})
print(f"    check: sqrt(0.231^2 + 0.693^2 x 2^2) = {math.sqrt(0.231 ** 2 + 4 * 0.693 ** 2):.3f}; at R14 + 0.693^2 x 3^2: {math.sqrt(0.231 ** 2 + 4 * 0.693 ** 2 + 9 * 0.693 ** 2):.3f};"
      f" limiting case d_in = 0: {s_tot(c2, 2.0, 0, 0):.3f} = s_model")
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
    return sum(math.exp(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * math.log(p) + (n - j) * math.log(1 - p)) for j in range(k, n + 1))


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
print(f"  v3 family (P11): 8 checks of T1-c (iii) + 2 of T1-h at >= 465 of 500: false fail at a true 0.95: {1 - binom_tail(500, 465, 0.95) ** 8:.3f} (8) /"
      f" {1 - binom_tail(500, 465, 0.95) ** 10:.3f} (10); at 0.945: {1 - binom_tail(500, 465, 0.945) ** 10:.3f} (10)")


def k_below(n, p, a):
    """largest k with P(X < k | n, p) <= a"""
    k, c = 0, 0.0
    while True:
        pk = math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log(1 - p))
        if c + pk > a:
            return k
        c += pk
        k += 1


# v4 (P11, Df-10): one family of N_COV = 10 checks (T1-c (iii): 4 true lambda x 2 points; T1-h: 2 points), 500
# pseudo-experiments per (point, lambda). Reference c_ref = the convention's computed coverage at the workspace's kappa and
# lambda (one-bin analogue of [10]), at most 0.95. FAIL if X < k_F (P(X < k_F | c_ref) <= 0.05 / N_COV); INVESTIGATE if
# k_F <= X < k_05 (P(X < k_05 | c_ref) <= 0.05); one re-test on 500 new pseudo-experiments, FAIL if X' < k_F.
N_COV = 10
for c_ref in (0.95, 0.945):
    kF, k05 = k_below(500, c_ref, 0.05 / N_COV), k_below(500, c_ref, 0.05)
    pF = 1 - binom_tail(500, kF, c_ref)
    pI = binom_tail(500, kF, c_ref) - binom_tail(500, k05, c_ref)
    fam = 1 - (1 - pF - pI * pF) ** N_COV
    pw = binom_tail(500, k05, 0.90) + (binom_tail(500, kF, 0.90) - binom_tail(500, k05, 0.90)) * binom_tail(500, kF, 0.90)
    print(f"  v4 T1 coverage family, c_ref = {c_ref}: FAIL below {kF} of 500 (P = {pF:.4f} per check), INVESTIGATE {kF}-{k05 - 1} (P = {pI:.3f}),"
          f" re-test FAIL below {kF}; family-wise false FAIL {fam:.3f}; P(final PASS | true coverage 0.90) = {pw:.4f}")
kPool = k_below(2000, 0.95, 0.05 / 4)
print(f"  alternative (pooled lambda): 2 pooled T1-c (iii) checks of 2,000 + 2 T1-h checks of 500: at c_ref 0.95 FAIL below {kPool} of 2,000 or"
      f" {k_below(500, 0.95, 0.05 / 4)} of 500 (family-wise {1 - (1 - (1 - binom_tail(2000, kPool, 0.95))) ** 2 * (1 - (1 - binom_tail(500, k_below(500, 0.95, 0.05 / 4), 0.95))) ** 2:.3f} without re-test)")
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
print(f"  DIF rate per triggered event by process (background.json -> cprime.dif.rate.per_process): 1.5687 (WZ; v5, G-C14) to 1.5945 (tt 2l): spread {1.5945 / 1.5687 - 1:.3f}")
