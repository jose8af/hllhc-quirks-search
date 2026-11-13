"""make_jobs.py -- Stage 3 (E7): build the full job list (plan §1, §2, §6 with the approved decisions D1-D16), estimate
the cost of every job, and split it between the Mac and the Windows PC.

Grid (approved: D5 option B, D10 |eta| < 4 counted inside 2.5, D11 B-only 7-10 keV at E 500/1000 only, D12 not run):
  P1 (campaign 'p1', input <spin>_m<m>_p1.npz, |eta| < 1, vertex at the origin): E 200/500/1000/1500 + Etilde 500 x
     Lambda {0.45, 0.6, 1, 2, 3, 5, 7, 10} keV; events: first 300 (Lambda <= 5) / first 200 (7, 10 keV);
     B (1e-3; 7-10 keV only E 500/1000), B2 = B0/2 (1e-3, Lambda <= 5), V (1e-3, 1 and 3 keV), M and BM (1e-2, all),
     Mx0.5/Mx2/BMx0.5/BMx2 (1e-2, 1 and 3 keV).
  P2 (campaign 'p2', input <spin>_m<m>_p2.npz, |eta| < 4, luminous vertex, BM): E 200-1500 (14) + Etilde 200/500/1000 x
     16 Lambda 0.3-10 keV, 200 template + 200 toy events counted inside |eta| < 2.5 (the forward 2.5-4 events in between
     ride along); Lambda 15/20/30 keV (+40 keV for E >= 1000, Etilde >= 500) at E {200, 300, 500, 700, 1000, 1200, 1500}
     + Etilde 3: 200 template (200 + 200 toy at E 1000/1200).  max_boost 1e-3 for Lambda <= 1.5 keV, 1e-2 above.
  MV (campaign 'mv'): BMx0.5 and BMx2 at E 200/500/1000/1500 + Etilde 500 x Lambda {0.4, 0.6, 1, 3, 10, 20} keV, 200
     template events (P2 selection and settings).
Cost model: the p7 probe model (mean measured wall s/event with 7 workers busy on the M3, interpolated in log m and
  log-log in Lambda; data/sim_stage3/probes/p1,p4,p6 summaries), x1.05 recorder, x1.34 (BM/M) / x1.40 (B) for |eta| < 1
  (p6/p1), x1.10 for disc material in P2 (ESTIMATE, plan §6.2), B2 = B cost, V(1e-3) = 10 x V(1e-2).  Units: "M3 CPU-s".
Chunks: 25 events if est > 5 s/event, 50 if > 0.5 s, else 100.
Split: PC (14 workers, ESTIMATE ~1.9x the Mac's 7-worker throughput) gets ~63 % of the estimated CPU, starting with
  every P2 job at Lambda >= 15 keV; the Mac keeps P1 (needed first for the physics checks) and P2 <= 10 keV.
  overlap.json: 3 cheap jobs cloned under campaign 'xover' that BOTH machines run (statistical cross-machine check).
Outputs: sim/stage3/jobs/{all,mac,pc,overlap,smoke,v2b}.json and jobs/split_summary.json.
Run (theory_track/): pixi run python sim/stage3/code/make_jobs.py
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TT = HERE.parents[2]
S3 = HERE.parent
INP = TT / 'data' / 'sim_stage3' / 'inputs'
PRB = TT / 'data' / 'sim_stage3' / 'probes'
JOBS = S3 / 'jobs'

S1 = json.load(open(PRB / 'p1_summary.json'))['cost']
S4 = json.load(open(PRB / 'p4_summary.json'))
OVER = 1.05
F_CENT = {'BM': 1.34, 'M': 1.34, 'B': 1.40, 'V': 1.40}
F_DISC = 1.10
E_MASSES = list(range(200, 1600, 100))
S_MASSES = [200, 500, 1000]
P1_POINTS = [('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)]
LAM_P1 = [0.45, 0.6, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
LAM_P2_LO = [0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.85, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0]
LAM_P2_HI = [15.0, 20.0, 30.0, 40.0]
SUB7 = [200, 300, 500, 700, 1000, 1200, 1500]
MV_POINTS = [('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)]
LAM_MV = [0.4, 0.6, 1.0, 3.0, 10.0, 20.0]
# PC (7800X3D) shares the CPU with the user (decision 2026-10-11): 10 workers at below-normal priority.
# Throughput of PC(10 workers) relative to Mac(7 workers): R_PC = 1.4 (ESTIMATE, inside the requested 1.3-1.5):
#   Mac 7 workers = 4 P + 3 E cores ~ 5.2 P-core equivalents (E ~ 0.4 P);  PC 10 workers on 8 Zen 4 cores / 16 threads:
#   8 cores x ~1.0 M3-P-core each + 2 SMT threads x ~0.25 = ~8.5, minus the user's concurrent load and below-normal
#   priority (~15 %) -> ~7.2 -> 7.2/5.2 ~ 1.4.  Unmeasured; refine from the first hours of _progress files.
R_PC = 1.4
PC_TARGET = R_PC / (1.0 + R_PC)


def table(cfg, s):
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


_T = {}


def interp_lam(d, lam):
    ls = np.array(sorted(d)); ts = np.array([d[x] for x in ls])
    if lam in d:
        return d[lam]
    x, y = np.log(ls), np.log(ts)
    if lam < ls[0]:
        return float(ts[0])
    if lam > ls[-1]:
        p = (y[-1] - y[-2]) / (x[-1] - x[-2])
        return float(np.exp(y[-1] + p * (np.log(lam) - x[-1])))
    return float(np.exp(np.interp(np.log(lam), x, y)))


def base_cost(m, lam, cfg, s):
    key = (cfg, s)
    if key not in _T:
        _T[key] = table(cfg, s)
    T = _T[key]
    ms = sorted(m_ for m_ in T if len(T[m_]) >= 2)
    vals = {m_: interp_lam(T[m_], lam) for m_ in ms}
    lm = np.log([float(x) for x in ms]); lv = np.log([vals[x] for x in ms])
    return float(np.exp(np.interp(np.log(m), lm, lv))) * OVER


def est_event(m, lam, cfg, mb, camp):
    s = 'f' if mb < 5e-3 else 'c'
    fam = 'B' if cfg in ('B', 'B2') else ('V' if cfg == 'V' else ('M' if cfg.startswith('M') else 'BM'))
    if fam == 'V':
        t = base_cost(m, lam, 'V', 'c') * (10.0 if s == 'f' else 1.0)
    elif fam == 'B':
        t = base_cost(m, lam, 'B', s)
    elif fam == 'M':
        t = base_cost(m, lam, 'M', 'c') * (10.0 if s == 'f' else 1.0)
    else:
        t = base_cost(m, lam, 'BM', s)
    if 'x' in cfg:
        t *= 1.1
    if camp == 'p1':
        t *= F_CENT[fam]
    else:
        t *= F_DISC
    return t


def p2_lists(spin, m):
    z = np.load(INP / f'{spin}_m{m}_p2.npz')
    spl = z['tt_split']; ins = z['in_eta25']
    out = {}
    for s, nm in ((0, 'template'), (1, 'toy')):
        idx = np.where(spl == s)[0]
        c = np.cumsum(ins[idx])
        last = int(np.searchsorted(c, 200))           # position of the 200th in_eta25 event of the split
        if c[-1] < 200:
            raise RuntimeError(f'{spin} {m}: only {c[-1]} {nm} events in |eta| < 2.5')
        out[nm] = idx[:last + 1].tolist()
    return out


def mb_p2(lam):
    """P2/MV max_boost: 1e-3 up to 5 keV (plan D8 had 1.5 keV; extended to 2-5 keV after V3, user decision 2026-10-11),
    1e-2 at 7 keV and above."""
    return 1e-3 if lam <= 5.0 else 1e-2


def chunk_size(e):
    return 25 if e > 5.0 else (50 if e > 0.5 else 100)


def make(camp, spin, m, lam, cfg, mb, ev, vertex, jobs):
    e = est_event(m, lam, cfg, mb, camp)
    cs = chunk_size(e)
    for c in range(0, (len(ev) + cs - 1) // cs):
        sub = ev[c * cs:(c + 1) * cs]
        jid = f'{camp}/{spin}_m{m}/L{lam:g}_{cfg}_c{c:02d}'
        jobs.append(dict(id=jid, out=jid + '.npz', campaign=camp, spin=spin, m=m, lam=lam, cfg=cfg, chunk=c,
                         input=f'{spin}_m{m}_{"p1" if camp == "p1" else "p2"}.npz', ev=[int(x) for x in sub],
                         max_boost=mb, hmax=0.2, vertex=vertex, est_s=round(e * len(sub), 2), est_s_per_event=round(e, 4)))


def build():
    jobs = []
    # ---- P1
    for spin, m in P1_POINTS:
        n_in = len(np.load(INP / f'{spin}_m{m}_p1.npz')['row'])
        for lam in LAM_P1:
            nev = 300 if lam <= 5.0 else 200
            assert n_in >= nev
            ev = list(range(nev))
            cfgs = []
            if lam <= 5.0 or (spin, m) in (('F', 500), ('F', 1000)):
                cfgs.append(('B', 1e-3))
            if lam <= 5.0:
                cfgs.append(('B2', 1e-3))
            if lam in (1.0, 3.0):
                cfgs += [('V', 1e-3), ('Mx0.5', 1e-2), ('Mx2', 1e-2), ('BMx0.5', 1e-2), ('BMx2', 1e-2)]
            cfgs += [('M', 1e-2), ('BM', 1e-2)]
            for cfg, mb in cfgs:
                make('p1', spin, m, lam, cfg, mb, ev, 'origin', jobs)
    # ---- P2
    lists = {}
    for spin, ms in (('F', E_MASSES), ('S', S_MASSES)):
        for m in ms:
            L = p2_lists(spin, m); lists[(spin, m)] = L
            for lam in LAM_P2_LO:
                make('p2', spin, m, lam, 'BM', mb_p2(lam), L['template'] + L['toy'], 'lumi', jobs)
            if spin == 'S' or m in SUB7:
                for lam in LAM_P2_HI:
                    if lam == 40.0 and not ((spin == 'F' and m >= 1000) or (spin == 'S' and m >= 500)):
                        continue
                    ev = L['template'] + (L['toy'] if (spin == 'F' and m in (1000, 1200)) else [])
                    make('p2', spin, m, lam, 'BM', 1e-2, ev, 'lumi', jobs)
    # ---- MV
    for spin, m in MV_POINTS:
        for lam in LAM_MV:
            for cfg in ('BMx0.5', 'BMx2'):
                make('mv', spin, m, lam, cfg, mb_p2(lam), lists[(spin, m)]['template'], 'lumi', jobs)
    return jobs


def summarize(jobs):
    out = {}
    for j in jobs:
        k = j['campaign'] + ('_hi' if (j['campaign'] == 'p2' and j['lam'] >= 15) else '')
        d = out.setdefault(k, dict(jobs=0, events=0, cpu_h=0.0))
        d['jobs'] += 1; d['events'] += len(j['ev']); d['cpu_h'] += j['est_s'] / 3600
    return out


if __name__ == '__main__':
    JOBS.mkdir(exist_ok=True)
    jobs = build()
    OUT = TT / 'data' / 'sim_stage3' / 'out'
    done = {j['id'] for j in jobs if (OUT / j['out']).is_file()}
    for j in jobs:
        j['est_s_remaining'] = 0.0 if j['id'] in done else j['est_s']
    tot = sum(j['est_s_remaining'] for j in jobs)
    # ---- split (on the remaining work)
    pc, mac = [], []
    for j in jobs:
        (pc if (j['campaign'] == 'p2' and j['lam'] >= 15) else mac).append(j)
    share = sum(j['est_s_remaining'] for j in pc) / tot
    if share < PC_TARGET:
        # move the most expensive remaining non-P1 jobs (MV first, then P2 <= 10 keV) to the PC until the target
        cand = sorted([j for j in mac if j['campaign'] != 'p1'], key=lambda j: (j['campaign'] != 'mv', -j['est_s']))
        for j in cand:
            if sum(x['est_s_remaining'] for x in pc) / tot >= PC_TARGET:
                break
            pc.append(j); mac.remove(j)
    elif share > PC_TARGET + 0.01:
        # give high-Lambda jobs back to the Mac, the cheapest Lambda first (15 keV, then 20 ...), so the longest
        # jobs stay on the PC
        for j in sorted(pc, key=lambda j: (j['lam'], j['est_s'])):
            if sum(x['est_s_remaining'] for x in pc) / tot <= PC_TARGET:
                break
            mac.append(j); pc.remove(j)
    # ---- overlap (cloned jobs under campaign 'xover')
    pick = ['p1/F_m500/L1_B_c00', 'p2/F_m500/L1_BM_c00', 'p2/F_m1000/L3_BM_c00']
    byid = {j['id']: j for j in jobs}
    overlap = []
    for pid in pick:
        j = dict(byid[pid]); j['id'] = 'xover/' + pid.replace('/', '__'); j['out'] = j['id'] + '.npz'
        j['campaign'] = 'xover'; j['clone_of'] = pid
        overlap.append(j)
    # ---- smoke (bundle self-test, ~2 min) and the V2b subset (P1 B, B2 at 0.6/1/2 keV)
    smoke = []
    for pid, n in (('p2/F_m500/L1_BM_c00', 12), ('p1/F_m500/L3_B_c00', 4)):
        j = dict(byid[pid]); j['id'] = 'smoke/' + pid.replace('/', '__'); j['out'] = j['id'] + '.npz'
        j['campaign'] = 'smoke'; j['ev'] = j['ev'][:n]; j['est_s'] = round(j['est_s_per_event'] * n, 2)
        smoke.append(j)
    v2b = [j for j in jobs if j['campaign'] == 'p1' and j['cfg'] in ('B', 'B2') and j['lam'] in (0.6, 1.0, 2.0)]
    meta = dict(created_by='make_jobs.py (E7, 2026-10-11)', units_est='M3 CPU-s (7 workers busy)', plan='sim/stage3/plan.md')
    for name, L in (('all', jobs), ('mac', mac), ('pc', pc), ('overlap', overlap), ('smoke', smoke), ('v2b', v2b)):
        json.dump(dict(meta=meta, name=name, n_jobs=len(L), est_cpu_h=sum(j['est_s'] for j in L) / 3600, jobs=L),
                  open(JOBS / f'{name}.json', 'w'))
    rem = lambda L: sum(j['est_s_remaining'] for j in L) / 3600
    summ = dict(split_rule=dict(R_PC=R_PC, pc_target_share=PC_TARGET, pc_workers=10, pc_priority='below normal',
                                mac_workers=7, how_chosen='PC(10 workers) / Mac(7 workers) throughput ratio 1.4 = middle of '
                                'the requested conservative 1.3-1.5x (ESTIMATE): Mac 7 workers ~ 5.2 M3-P-core equivalents '
                                '(4 P + 3 E at ~0.4); PC 8 Zen-4 cores ~1.0 P-core each + 2 SMT threads ~0.25 = ~8.5, '
                                'minus ~15 % for the user working at the same time and below-normal priority -> ~7.2; '
                                '7.2/5.2 = 1.4. Equal finish time needs PC share = 1.4/2.4 = 58 % of the remaining work. '
                                'Unmeasured; check against the first hours of the _progress_<host>.jsonl files.'),
                remaining_cpu_h=dict(mac=rem(mac), pc=rem(pc), done_already=len(done)),
                total_cpu_h=sum(j['est_s'] for j in jobs) / 3600, n_jobs=len(jobs), n_events=sum(len(j['ev']) for j in jobs),
                by_campaign=summarize(jobs), mac=dict(n_jobs=len(mac), cpu_h=sum(j['est_s'] for j in mac) / 3600,
                                                      by_campaign=summarize(mac)),
                pc=dict(n_jobs=len(pc), cpu_h=sum(j['est_s'] for j in pc) / 3600, by_campaign=summarize(pc)),
                overlap=dict(n_jobs=len(overlap), cpu_h=sum(j['est_s'] for j in overlap) / 3600, ids=[j['id'] for j in overlap]),
                pc_share=rem(pc) / (tot / 3600),
                pc_hi_lambda_jobs=dict(on_pc=sum(1 for j in pc if j['campaign'] == 'p2' and j['lam'] >= 15),
                                       on_mac=sum(1 for j in mac if j['campaign'] == 'p2' and j['lam'] >= 15)),
                wall_estimate_h=dict(mac_7w=rem(mac) / 7, pc_10w_at_1p4x=rem(pc) / 7 / R_PC,
                                     note='ESTIMATE: M3 CPU-s / 7 workers; kernel s3.2 ran at 0.86x the estimate on the V2b jobs; '
                                          'cost-model uncertainty about +-25 %'),
                longest_job_h=max(j['est_s'] for j in jobs) / 3600)
    json.dump(summ, open(JOBS / 'split_summary.json', 'w'), indent=1)
    print(json.dumps(summ, indent=1))
