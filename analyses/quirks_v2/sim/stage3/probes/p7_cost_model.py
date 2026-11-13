"""p7_cost_model.py -- Stage-3 probe 7: total CPU and wall time of the proposed grid from the measured per-event costs.

Inputs: data/sim_stage3/probes/p1_summary.json (|eta| < 2.5, 4 masses x 9 Lambda, configs/settings), p4_summary.json
(40 keV BM), p6_summary.json (|eta| < 1 costs for P1), p3 (recorder overhead).  Per-event cost = the MEAN wall time per
event measured with 7 workers busy (so the P/E-core mix of production is included); interpolated linearly in log m between
the measured masses and log-log in Lambda between the measured Lambda values (extrapolated with the last segment).
Wall time = total / 7 workers.  All numbers are ESTIMATEs (8-16 events per measured cell; the cost distribution has a
long tail: p90/mean ~ 1.6-2).
Run: pixi run python sim/stage3/probes/p7_cost_model.py  -> data/sim_stage3/probes/p7_cost_model.json + printed tables
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
P = os.path.join(TT, 'data', 'sim_stage3', 'probes')
S1 = json.load(open(os.path.join(P, 'p1_summary.json')))['cost']
S4 = json.load(open(os.path.join(P, 'p4_summary.json'))) if os.path.exists(os.path.join(P, 'p4_summary.json')) else {}
S6 = json.load(open(os.path.join(P, 'p6_summary.json')))['cost'] if os.path.exists(os.path.join(P, 'p6_summary.json')) else {}
OVER = 1.05          # recorder with ~60 surfaces (p3: +4-6 % for 36)
NW = 7
MASSES = [200, 500, 1000, 1500]


def table(cfg, s):
    """cost[m][lam] from p1 (+ 40 keV BM c from p4)."""
    T = {}
    for k, v in S1.items():
        m, lam, c, ss = k.split('_')
        if c == cfg and ss == s:
            T.setdefault(int(m), {})[float(lam)] = v['mean']
    if cfg == 'BM' and s == 'c':
        for m in (500, 1500):
            t = S4.get(f'm{m}_L40_BM_1e-2_time')
            if t:
                T.setdefault(m, {})[40.0] = float(np.mean(t))
    return T


def interp_lam(d, lam):
    ls = np.array(sorted(d)); ts = np.array([d[x] for x in ls])
    if lam in d:
        return d[lam]
    x, y = np.log(ls), np.log(ts)
    if lam < ls[0]:
        return ts[0]
    if lam > ls[-1]:
        p = (y[-1] - y[-2]) / (x[-1] - x[-2])
        return float(np.exp(y[-1] + p * (np.log(lam) - x[-1])))
    return float(np.exp(np.interp(np.log(lam), x, y)))


def cost(m, lam, cfg, s):
    T = table(cfg, s)
    ms = sorted(m_ for m_ in T if len(T[m_]) >= 2)
    vals = {m_: interp_lam(T[m_], lam) for m_ in ms}
    if m in vals:
        return vals[m] * OVER
    lm = np.log([float(x) for x in ms]); lv = np.log([vals[x] for x in ms])
    return float(np.exp(np.interp(np.log(m), lm, lv))) * OVER


def central_factor(cfg_p6, s_p6, cfg_p1, s_p1, lams):
    """ratio of |eta|<1 (p6) to |eta|<2.5 (p1) mean cost, averaged over the common (m, Lambda) cells."""
    r = []
    for m in (500, 1000):
        for lam in lams:
            a = S6.get(f'm{m}_L{lam:g}_{cfg_p6}_{s_p6}'); b = S1.get(f'{m}_{lam:g}_{cfg_p1}_{s_p1}')
            if a and b and b['mean'] > 0:
                r.append(a['mean'] / b['mean'])
    return (float(np.mean(r)), r) if r else (1.0, [])


LAM_P2 = [0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.85, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
E_MASSES = list(range(200, 1600, 100))


def setting(lam):
    return 'f' if lam <= 1.5 else 'c'      # max_boost 1e-3 up to 1.5 keV, 1e-2 above (p1/p4/p6 convergence)


out = {}
# ---------------- P2 ----------------
fc_bm, rr = central_factor('BM', '0.01', 'BM', 'c', (1.0, 3.0, 5.0, 10.0))
print(f'central/all cost ratio BM 1e-2 (p6/p1): {fc_bm:.2f} {np.round(rr, 2)}')
rows = []
for spin, masses in (('E', E_MASSES), ('S', [200, 500, 1000])):
    for m in masses:
        lams = LAM_P2 + ([40.0] if (spin == 'E' and m >= 1000) or (spin == 'S' and m >= 500) else [])
        for lam in lams:
            t = cost(m, lam, 'BM', setting(lam))
            if spin == 'S':
                t *= 1.0   # scalar: same kernel; gamma* spectrum harder (x_med x1.7) -> ESTIMATE same cost
            rows.append((spin, m, lam, t))
P2 = {}
for spin, m, lam, t in rows:
    P2.setdefault(lam, 0.0)
    P2[lam] += t
print('\nP2 BM nominal, per-event cost summed over masses (E 14 + Etilde 3) [s], per Lambda:')
for lam in sorted(P2):
    print(f'  {lam:5g} keV: {P2[lam]:9.1f} s  -> 400 events: {P2[lam] * 400 / 3600:8.1f} CPU-h; 200 events: {P2[lam] * 200 / 3600:7.1f}')
tot400 = sum(P2.values()) * 400 / 3600
hi = sum(v for k, v in P2.items() if k >= 15) * 400 / 3600
print(f'  P2 total 400 ev/point: {tot400:.0f} CPU-h (of which Lambda >= 15 keV: {hi:.0f}); 200 ev/point: {tot400 / 2:.0f}')
out['P2_per_lambda_sum_s'] = P2; out['P2_total_400_cpuh'] = tot400; out['P2_hi_400_cpuh'] = hi
# alternatives for Lambda >= 15 keV
sub = [200, 300, 500, 700, 1000, 1200, 1500]
alt = {}
for name, masses_hi, nev_hi in (('all14_400', E_MASSES, 400), ('all14_200', E_MASSES, 200), ('sub7_400', sub, 400), ('sub7_200', sub, 200)):
    s = 0.0
    for spin, m, lam, t in rows:
        if lam < 15:
            s += t * 400
        elif spin == 'S' or m in masses_hi:
            s += t * nev_hi
    alt[name] = s / 3600
    print(f'  option {name:10s}: {s / 3600:7.0f} CPU-h, wall {s / 3600 / NW:6.1f} h ({s / 3600 / NW / 24:.1f} d)')
out['P2_options_cpuh'] = alt
# ---------------- P1 ----------------
fcB, r1 = central_factor('B', '0.001', 'B', 'f', (1.0, 3.0, 5.0, 10.0))
print(f'\ncentral/all ratio B 1e-3: {fcB:.2f} {np.round(r1, 2)}')
P1cfg = {}
for spin, m in (('E', 200), ('E', 500), ('E', 1000), ('E', 1500), ('S', 500)):
    for lam in (0.45, 0.6, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0):
        nev = 300 if lam <= 5.0 else 200
        tB = cost(m, lam, 'B', 'f') * fcB
        tBM = cost(m, lam, 'BM', 'c') * fc_bm; tM = cost(m, lam, 'M', 'c') * fc_bm
        add = lambda k, v: P1cfg.__setitem__(k, P1cfg.get(k, 0.0) + v / 3600)
        add('B (1e-3)', tB * nev)
        if lam <= 5.0:
            add('B/2 (1e-3)', tB * nev)
        if lam in (1.0, 3.0):
            add('V (1e-3)', cost(m, lam, 'V', 'c') * 10 * fcB * nev)
            add('M,BM x0.5,x2', 2 * (tBM + tM) * 1.1 * nev)
        add('M (1e-2)', tM * nev); add('BM (1e-2)', tBM * nev)
P1 = sum(P1cfg.values())
for k, v in P1cfg.items():
    print(f'  P1 {k:14s}: {v:6.1f} CPU-h')
print(f'P1 total: {P1:.1f} CPU-h')
out['P1_cpuh'] = P1; out['P1_by_cfg_cpuh'] = P1cfg
# ---------------- material variants (P2 subset) ----------------
MV = 0.0
for spin, m in (('E', 200), ('E', 500), ('E', 1000), ('E', 1500), ('S', 500)):
    for lam in (0.4, 0.6, 1.0, 3.0, 10.0, 20.0):
        MV += 2 * cost(m, lam, 'BM', setting(lam)) * 1.1 * 200
print(f'P2 material variants (x0.5, x2; 5 points x 6 Lambda (to 20 keV) x 200 ev): {MV / 3600:.1f} CPU-h')
out['MATVAR_cpuh'] = MV / 3600
# ---------------- recommended P2 option B ----------------
anchors = (1000, 1200)
sB = 0.0
for spin, m, lam, t in rows:
    if lam < 15:
        sB += t * 400
    elif spin == 'S' or m in sub:
        sB += t * (400 if (spin == 'E' and m in anchors) else 200)
out['P2_optionB_cpuh'] = sB / 3600
print(f'P2 option B (all masses 400 ev to 10 keV; >= 15 keV: 7-mass subset + Etilde at 200 ev, 400 at E 1000/1200): {sB / 3600:.0f} CPU-h')
lo = sum(t * 400 for spin, m, lam, t in rows if lam < 15) / 3600
print(f'  of which Lambda <= 10 keV: {lo:.0f} CPU-h')
out['P2_le10_cpuh'] = lo
json.dump(out, open(os.path.join(P, 'p7_cost_model.json'), 'w'), indent=1)
