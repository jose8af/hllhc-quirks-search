"""run_g1b.py -- G1b job kinds for campaign C1 (2026-10-13, post-freeze): signal A1 / A2 / A5 and C' (C'0, C'_PU).

NEW module; run_stage4.py dispatches the kinds below to run_job() (additive hook, HASH_ADDENDUM.md).  Every kind writes
ONE npz per job atomically through run_stage4.pack() (the frozen per-trial S1-S5 records of process_trial) plus its
own 'sig.*' / 'cp.*' arrays.  Finder config = the frozen one (run_stage4.finder_configs: road = delta95, eta_max,
mip_gev, require_btl).  All signal / C' trials are rho = 1.

Kinds (plan §5 table, §6.2 C1 core; WP_RULE §7):
  'a1'   A1: signal only (no PU), one job per Stage-3 point (all 307 p2 + 60 mv points, status == 1, all eta, both
         halves), full chain run_chain.py sig --no-pu (mv: --mat-scale 0.5 / 2).  Per event the nominal trial plus the
         V4-3 variations W_c 50/100/150 mm (t_tol 30 um) and t_tol 0/100 um (W_c 75 mm): per-rung matched-pass flags.
  'a2'   A2 core, row-major: E200/500/1000/1500 + E~500 x Lambda {0.45, 0.6, 0.85, 1, 1.5, 2, 3, 5} keV, all template
         counting rows (~200 per species-mass; 1 000 rows, 8 000 events).  One PU event per row (run_chain.py pu with
         the per-row seeds hseed('sigpu', spin, m, row) = the A5 sig-mode PU seeds), then per Lambda: numpy quirk
         digitisation (s4sig.digitise), the same top-up (PU rows only, same seed at every Lambda), CKF removal, U-5 b
         merging, PV/MET from hseed('sig-pvmet', spin, m, row) -> process_trial.  V4-1: chain + numpy counters.
  'a5'   A5 core: 5 points (the 5 A2 species-masses at Lambda = 1 keV; G1b choice, flagged), full chain with PU
         (run_chain.py sig), 200 template counting rows each (1 000 events); S6-style dumps of every event (TT-level
         variations); V4-1 (chain + injected = measured) and V4-6 (quirk measurements on CKF tracks).
  'cp0'  C'0: guns gamma / v0 / pvpair / looper 1e5 each, NI 22/30/61.5 mm 3e4 each, DIF 5e4; no PU, no top-up; per
         event: exhaustive-triple preselection, V4-10 hash, process_trial, attribution of every candidate.  Stores the
         toy measurements + SimHits of the events C'_PU may overlay (guns: global index < 500; NI/DIF: preselected).
  'cppu' C'_PU: 8 topologies x 500 with PU.  Needs ALL C'0 jobs of its topology; refuses (job error) if V4-10 fails
         for that topology (NI/DIF: attributed candidates in non-preselected C'0 events must be 0).  Slot s overlays
         source event pre[s mod N_pre] (pre = preselected NI/DIF events / gun events 0..499 by global index); stored
         SimHits inserted (run_chain.py cppu), toy measurement rows replaced by the stored C'0 rows (V4-10 hash checked
         per event), same stored PV and road.

  pixi run python -m acts.stage4.run_g1b smoke        dev smoke (2 small jobs of each kind) -> data/acts_stage4/prod/smokeG1b
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from acts.stage4 import run_stage4 as RS

TT = RS.TT
PROD = RS.PROD
KINDS = ('a1', 'a2', 'a5', 'cp0', 'cppu')
G1B_VERSION = 'g1b-1'
G1B_FILES = ['acts/stage4/run_g1b.py', 'acts/stage4/finder/g1b_tt.py']
# plan §6.2 C1 core
A2_SPECIES = [('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)]
A2_LAMS = [0.45, 0.6, 0.85, 1.0, 1.5, 2.0, 3.0, 5.0]
A5_LAM = 1.0                     # G1b choice (plan: '5 points'): the 5 species-masses at 1 keV, paired with A2 rows
A1_VARIANTS = [('Wc50', 50.0, 0.030), ('Wc100', 100.0, 0.030), ('Wc150', 150.0, 0.030), ('tt0', 75.0, 0.0),
               ('tt100', 75.0, 0.100)]
ROWS_PER_JOB = {'a2': 10, 'a5': 10}
CP_N = {'gamma': 100_000, 'v0': 100_000, 'pvpair': 100_000, 'looper': 100_000, 'ni22': 30_000, 'ni30': 30_000,
        'ni61': 30_000, 'dif': 50_000}
CP_PER_JOB = 5000
CPPU_N = 500
CPPU_PER_JOB = 20
CP_GUNS = ('gamma', 'v0', 'pvpair', 'looper')
# measured costs (G1b smoke; per event, 1 process under the G3 load) -- manifest estimates
COST = dict(a1_ev=0.03, a2_lam=RS.T1_S + 0.15, a5_ev=RS.PU_S + 0.6 + RS.T1_S, cp0_ev=0.012, cppu_ev=RS.PU_S + RS.T1_S + 0.3,
            job_overhead=12.0)


def s4sig():
    from acts.stage4.code import s4sig as S
    return S


def index():
    return json.loads((TT / 'data' / 'sim_stage3' / 'STAGE3_INDEX.json').read_text())


def probe_excluded(point_key, rows, P=None):
    """WP_RULE §5.4 item 10: probe rows excluded from the template efficiencies (flagged per trial, still run)."""
    ex = set()
    f1r = TT / 'data' / 'acts_stage4' / 'fix_r1' / 'f1r_summary.json'
    sp = point_key.split('/')
    short = f'{sp[1]}/{sp[2].split("_")[0]}'
    if f1r.exists():
        d = json.loads(f1r.read_text()).get('sig_t0', {})
        if short in d:
            ex |= {int(r) for r in d[short]['rows']}
    if sp[0] == 'p2' and sp[1] == 'F_m1000' and sp[2].split('_')[0] in ('L0.6', 'L1', 'L3') and P is not None:
        z = P.z[0]
        idx = [7, 8, 15, 16, 24, 26, 39, 42]
        ex |= {int(z['row'][i]) for i in idx if i < len(z['row'])}
    return np.array([int(r) in ex for r in rows], bool)


# ------------------------------------------------------------------------------------------------------- manifests
def manifest_jobs(camp):
    S = s4sig()
    jobs = []
    if camp not in ('C1', 'smokeG1b'):
        return jobs
    idx = index()
    smoke = camp == 'smokeG1b'
    # ---- A1
    pts = sorted(k for k in idx['points'] if (k.startswith('p2/') and k.endswith('_BM')) or k.startswith('mv/'))
    if smoke:
        pts = ['p2/F_m1000/L1_BM', 'mv/F_m500/L1_BMx2']
    for k in pts:
        nev = sum(c['status'][1] for c in idx['points'][k]['chunks'])
        nmax = 6 if smoke else 0
        n = min(nev, nmax) if nmax else nev
        tag = k.replace('/', '_')
        jobs.append(dict(id=f'A1_{tag}', campaign=camp, sample='A1', kind='a1', point=k, max_rows=nmax, n_events=n,
                         roads=1, rho=1, seed=RS.hash_seed(f'stage4|A1|{k}'), dump_events=0,
                         est_s=COST['job_overhead'] + n * COST['a1_ev'], mem_gb=1.0, order=3,
                         out=f'{camp}/A1/A1_{tag}.npz', requires='G1b'))
    # ---- A2 (row-major) and A5
    for spin, m in A2_SPECIES:
        P = S.Point(S.point_key(spin, m, A2_LAMS[0]), idx)
        rows = P.rows(template=True, counting=True, status1=False)
        if smoke:
            rows = rows[:2] if (spin, m) == ('F', 1000) else []
        per = ROWS_PER_JOB['a2']
        for ch, r0 in enumerate(range(0, len(rows), per)):
            rr = rows[r0:r0 + per]
            jobs.append(dict(id=f'A2_{spin}{m}_{ch:03d}', campaign=camp, sample='A2', kind='a2', spin=spin, m=m,
                             lams=A2_LAMS, rows=rr, chunk=ch, n_events=len(rr), roads=1, rho=1,
                             seed=RS.hash_seed(f'stage4|A2|{spin}{m}|{ch}'), dump_events=0,
                             est_s=COST['job_overhead'] + len(rr) * (RS.PU_S + len(A2_LAMS) * COST['a2_lam']),
                             mem_gb=1.5, order=1, out=f'{camp}/A2/A2_{spin}{m}_{ch:03d}.npz', requires='G1b'))
        k5 = S.point_key(spin, m, A5_LAM)
        P5 = S.Point(k5, idx)
        rows5 = P5.rows(template=True, counting=True, status1=True)
        if smoke:
            rows5 = rows5[:2] if (spin, m) == ('F', 1000) else []
        per = ROWS_PER_JOB['a5']
        for ch, r0 in enumerate(range(0, len(rows5), per)):
            rr = rows5[r0:r0 + per]
            jobs.append(dict(id=f'A5_{spin}{m}_L{A5_LAM:g}_{ch:03d}', campaign=camp, sample='A5', kind='a5', point=k5,
                             rows=rr, chunk=ch, n_events=len(rr), roads=1, rho=1,
                             seed=RS.hash_seed(f'stage4|A5|{k5}|{ch}'), dump_events=len(rr),
                             est_s=COST['job_overhead'] + len(rr) * COST['a5_ev'], mem_gb=1.5, order=1,
                             out=f'{camp}/A5/A5_{spin}{m}_L{A5_LAM:g}_{ch:03d}.npz', requires='G1b'))
    # ---- C'0 and C'_PU
    cpn = {t: (200 if smoke else n) for t, n in CP_N.items()}
    if smoke:
        cpn = {'ni30': 200, 'looper': 200}
    per0 = 200 if smoke else CP_PER_JOB
    cp_out = {}
    for topo, n in cpn.items():
        for ch, e0 in enumerate(range(0, n, per0)):
            nn = min(per0, n - e0)
            o = f'{camp}/Cp0/Cp0_{topo}_{ch:03d}.npz'
            cp_out.setdefault(topo, []).append(o)
            jobs.append(dict(id=f'Cp0_{topo}_{ch:03d}', campaign=camp, sample='Cp0', kind='cp0', topo=topo, chunk=ch,
                             ev0=e0, n_events=nn, roads=1, rho=1, seed=RS.hash_seed(f'stage4|Cp0|{topo}|{ch}'),
                             dump_events=0, est_s=COST['job_overhead'] + nn * COST['cp0_ev'], mem_gb=1.0, order=0,
                             out=o, requires='G1b'))
    nslot = 2 if smoke else CPPU_N
    perp = 2 if smoke else CPPU_PER_JOB
    for topo in cpn:
        for ch, s0 in enumerate(range(0, nslot, perp)):
            nn = min(perp, nslot - s0)
            jobs.append(dict(id=f'CpPU_{topo}_{ch:03d}', campaign=camp, sample='CpPU', kind='cppu', topo=topo, chunk=ch,
                             slot0=s0, n_events=nn, roads=1, rho=1, seed=RS.hash_seed(f'stage4|CpPU|{topo}|{ch}'),
                             dump_events=0, est_s=COST['job_overhead'] + nn * COST['cppu_ev'], mem_gb=1.5, order=2,
                             needs=cp_out[topo], out=f'{camp}/CpPU/CpPU_{topo}_{ch:03d}.npz', requires='G1b'))
    return jobs


def needs_ok(job):
    nd = job.get('needs')
    if not nd:
        return True
    nd = [nd] if isinstance(nd, str) else nd
    return all(PROD.joinpath(*p.split('/')).is_file() for p in nd)


def validate(job, deep=False):
    p = RS.out_path(job)
    if not p.is_file() or p.stat().st_size == 0:
        return False
    if not deep:
        return True
    try:
        with np.load(p, allow_pickle=False) as z:
            return str(z['job_id']) == job['id'] and int(z['complete']) == 1 and int(z['g1b.n_events']) == job['n_events']
    except Exception:
        return False


# --------------------------------------------------------------------------------------------------------- helpers
def chain(job, tmp, args):
    cmd = ['pixi', 'run', '--manifest-path', str(RS.ACTS_MANIFEST), 'python', str(RS.CHAIN_PROD)] + [str(a) for a in args]
    t0 = time.time()
    p = subprocess.run(cmd, cwd=str(TT / 'acts'), capture_output=True, text=True)
    if p.returncode != 0 or not Path(tmp).exists():
        raise RuntimeError(f'chain failed ({p.returncode}): {p.stderr[-3000:]}')
    return time.time() - t0


def g1b_hashes():
    return {f: (RS.sha256_file(TT / f) if (TT / f).exists() else None) for f in G1B_FILES}


def finish(job, out, meta_extra, t_w0, t_c0, cfg, wcfg, fz, chain_meta, t_chain, n_trials):
    final = RS.out_path(job)
    meta = dict(runner=RS.RUNNER_VERSION, g1b=G1B_VERSION, job=job, chain_meta=chain_meta, t_chain_s=t_chain,
                code_sha256=RS.code_hashes(), g1b_sha256=g1b_hashes(), wcfg=vars(wcfg),
                finder_cfg=dict(road=cfg.road, w_c=cfg.w_c, t_tol=cfg.t_tol, tseed=cfg.tseed, iters=cfg.iters),
                frozen_inputs=fz, env=RS.env_info(), created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                wall_s=time.perf_counter() - t_w0, cpu_s_tt=time.process_time() - t_c0, **meta_extra)
    out['meta_json'] = np.array(json.dumps(meta, default=str))
    out['g1b.n_events'] = np.array(job['n_events'])
    tmp = final.with_name(final.name[:-4] + f'.tmp{os.getpid()}.npz')
    with open(tmp, 'wb') as f:
        np.savez_compressed(f, **out)
    os.replace(tmp, final)
    return dict(id=job['id'], wall=meta['wall_s'], est=job['est_s'], n_trials=n_trials, t_chain=t_chain,
                bytes=final.stat().st_size, v41_pass=meta.get('v41_pass'))


def pack_trials(job, trials, cands, hitrec, btl, dumps):
    if not trials:
        return dict(job_id=np.array(job['id']), complete=np.array(1), n_trials=np.array(0))
    return RS.pack(job, trials, cands, hitrec, btl, dumps)


def add_trial(res, trials, cands, hitrec, ev, extra):
    row = res['row']
    if 'road' in row:
        row['road_cfg'] = row['road']
    row.update(ev=ev, road=0, dz_nearest_pu=np.nan, trial_seed=row['seed'], **extra)
    ti = len(trials)
    trials.append(row)
    c = res['cand']; c['trial'] = np.full(len(c['idx']), ti, np.int32)
    cands.append(c)
    if res['hit'] is not None:
        hitrec.append((ti, res['hit']))
    return ti


def cat_records(recs, tcol='trial'):
    """list of (trial index, dict of arrays) -> dict of concatenated arrays (+ trial column)."""
    recs = [(t, r) for t, r in recs if r is not None and len(r['idx'])]
    if not recs:
        return {}
    out = {tcol: np.concatenate([np.full(len(r['idx']), t, np.int32) for t, r in recs])}
    for k in recs[0][1]:
        out[k] = np.concatenate([r[k] for _, r in recs])
    return out


def btl_rows(P, ie):
    b = P['btl']
    return np.c_[np.full(len(b), ie), b[:, :6], b[:, 11:13], P['btl_INT']]


# ----------------------------------------------------------------------------------------------------------- signal
SIG_COLS = ['row', 'lam', 'status', 'probe_excluded', 'n_q_written', 'n_q_ckf', 'n_q_pool', 'n_q_road', 'n_cand_q',
            'best_frac', 'phimet_true', 'skipped']


def sig_event_inputs(S, P, row, spin, m):
    h, ev = P.event(row)
    met_true = np.asarray(ev['p_qp'][:2], float) + np.asarray(ev['p_qm'][:2], float)
    rs = np.random.default_rng(S.hseed('sig-pvmet', spin, m, row))
    from acts.stage4.finder import g1b_tt as GT
    pv, phimet = GT.pv_met(ev['vtx'], met_true, rs)
    tseed = int(S.hseed('sig-trial', spin, m, row, mod=2 ** 62))
    return h, ev, met_true, pv, phimet, tseed


def sig_trial(GT, Pp, n_q_written, pv, phimet, tseed, cfg, wcfg):
    btl = (Pp['btl'], Pp['btl_INT'])
    if len(Pp['H']) < 3:
        return None, None, None
    res, X = GT.trial(Pp['H'], Pp['sid'], Pp['INT'], pv, phimet, tseed, cfg, wcfg, ckf=Pp['ckf'], btl=btl)
    summ, rec = GT.signal_summary(Pp, X, n_q_written, pv, phimet, cfg, Pp['ckf'], btl)
    return res, summ, rec


def run_signal_job(job):
    """'a1' (no PU, chain sig --no-pu), 'a5' (chain sig with PU), 'a2' (chain pu once per row + numpy quirks per Lambda)."""
    from acts.stage4.finder import g1b_tt as GT
    S = s4sig()
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    final = RS.out_path(job)
    final.parent.mkdir(parents=True, exist_ok=True)
    fz = RS.frozen_inputs()
    cfg, wcfg = RS.finder_configs(fz, job, False)
    idx = index()
    kind = job['kind']
    tmpc = final.with_name(final.name[:-4] + f'.chain{os.getpid()}.npz')
    rowsf = final.with_name(final.name[:-4] + f'.rows{os.getpid()}.json')
    trials = []; cands = []; hitrec = []; btl = []; dumps = []; sig = []; srec = []; evstats = []; var_eff = []
    qbtl = []
    v41_numpy_fail = 0
    try:
        if kind in ('a1', 'a5'):
            P = S.Point(job['point'], idx)
            spin = job['point'].split('/')[1].split('_')[0]
            if kind == 'a1':
                rows = P.rows(template=False, counting=False, status1=True)
                if job.get('max_rows'):
                    rows = rows[:job['max_rows']]
            else:
                rows = job['rows']
            assert len(rows) == job['n_events'], (len(rows), job['n_events'])
            rowsf.write_text(json.dumps(rows))
            mat = 1.0
            cfgname = job['point'].split('_')[-1]
            if cfgname.startswith('BMx'):
                mat = float(cfgname[3:])
            args = ['sig', tmpc, len(rows), job['seed'], '--point', job['point'], '--rows', rowsf, '--mat-scale', mat]
            if kind == 'a1':
                args.append('--no-pu')
            t_chain = chain(job, tmpc, args)
            z = np.load(tmpc)
            cm = json.loads(str(z['meta']))
            excl = probe_excluded(job['point'], rows, P)
            for ie, row in enumerate(rows):
                h, ev, met_true, pv, phimet, tseed = sig_event_inputs(S, P, row, spin, P.m)
                e = z[f'ev{ie}']; tr = z[f'tru{ie}']
                rs = np.random.default_rng(S.hseed('sig-topup', spin, P.m, row))
                Pp = GT.assemble(e, tr, 0, rs, inserted_vp=(GT.SIG_VP,), do_topup=(kind == 'a5'))
                evstats.append([ie, 0] + [Pp['stats'].get(c, 0) for c in RS.EVSTAT_COLS])
                barq = Pp['H0'][:, 7].astype(np.int64) == GT.SIG_VP
                nqw = int(barq.sum()); nqc = int((barq & Pp['H0_ckf']).sum())
                btl.append(btl_rows(Pp, ie))
                if kind == 'a5':      # S6-style dump of the chain event (barrel counting + BTL, pre-top-up)
                    dumps.append(dict(ev=ie, k=0, tru=tr.astype(np.float32), flag=e[:, 6].astype(np.int8),
                                      vz=z[f'vz{ie}'].astype(np.float32), sid=e[:, 0].astype(np.int16),
                                      xyz=e[:, 1:4].astype(np.float64), s01=e[:, 4:6].astype(np.float32),
                                      vp=e[:, 7].astype(np.int32), particle=e[:, 8].astype(np.int32),
                                      gen=e[:, 9].astype(np.int8), vsec=e[:, 10].astype(np.int32),
                                      dE=e[:, 11].astype(np.float32), t=e[:, 12].astype(np.float32)))
                res, summ, rec = sig_trial(GT, Pp, nqw, pv, phimet, tseed, cfg, wcfg)
                base = [row, P.lam, ev['status'], int(excl[ie]), nqw, nqc]
                if res is None:
                    sig.append(dict(cols=base + [0, 0, 0, 0.0, float(np.arctan2(met_true[1], met_true[0])), 1],
                                    ti=-1, summ=None))
                    if kind == 'a1':
                        var_eff.append(np.zeros((len(A1_VARIANTS), 4, RS_NR()), bool))
                    continue
                ti = add_trial(res, trials, cands, hitrec, ie, dict(sig_row=row, sig_lam=P.lam))
                sig.append(dict(cols=base + [summ['n_q_pool'], summ['n_q_road'], summ['n_cand_q'], summ['best_frac'],
                                             float(np.arctan2(met_true[1], met_true[0])), 0], ti=ti, summ=summ))
                srec.append((ti, rec))
                if kind == 'a1':      # V4-3: W_c and t_tol variations (signal summary only)
                    ve = np.zeros((len(A1_VARIANTS), 4, RS_NR()), bool)
                    for vi, (_, wc, tt) in enumerate(A1_VARIANTS):
                        cv = GT.with_cfg(cfg, w_c=wc, t_tol=tt)
                        r2, s2, _ = sig_trial(GT, Pp, nqw, pv, phimet, tseed, cv, wcfg)
                        if s2 is not None:
                            ve[vi] = np.array([s2['eff'], s2['eff_fckf'], s2['eff_T'], s2['eff_fckf_T']])
                    var_eff.append(ve)
            v41 = z['v41']; v41c = cm['v41_cols']; ctim = z['timing']
            v41_pass = bool(cm.get('v41_pass')) and bool(cm.get('sig_v41_pass'))
            chain_meta = cm
            z.close()
        elif kind == 'a2':
            spin, m = job['spin'], job['m']
            Ps = {lam: S.Point(S.point_key(spin, m, lam), idx) for lam in job['lams']}
            mm = Ps[job['lams'][0]].m
            rows = job['rows']
            seeds = [S.hseed('sigpu', spin, mm, r, mod=2 ** 62) for r in rows]
            rowsf.write_text(json.dumps(seeds))
            t_chain = chain(job, tmpc, ['pu', tmpc, len(rows), job['seed'], '--event-seeds', rowsf])
            z = np.load(tmpc)
            cm = json.loads(str(z['meta']))
            if [int(x) for x in cm['event_seeds']] != [int(x) for x in seeds]:
                raise RuntimeError('A2 PU event seeds not applied by the chain')
            slab = S.slab_table(1.0)
            excl = {lam: probe_excluded(S.point_key(spin, m, lam), rows, Ps[lam]) for lam in job['lams']}
            for ie, row in enumerate(rows):
                e_pu = z[f'ev{ie}']; t_pu = z[f'tru{ie}']
                btl_pu_done = False
                for lam in job['lams']:
                    P = Ps[lam]
                    if row not in P.rowmap:
                        continue
                    h, ev, met_true, pv, phimet, tseed = sig_event_inputs(S, P, row, spin, P.m)
                    if ev['status'] != 1:
                        sig.append(dict(cols=[row, lam, ev['status'], int(excl[lam][job['rows'].index(row)]), 0, 0, 0, 0,
                                              0, 0.0, float(np.arctan2(met_true[1], met_true[0])), 1], ti=-1, summ=None))
                        continue
                    d = S.digitise(h, ev, P.m, spin, row, lam, slab)
                    v41_numpy_fail += int(not d['v41']['pass'])
                    e = np.concatenate([e_pu, d['meas']]); tr = np.concatenate([t_pu, d['tru'].astype(np.float32)])
                    rs = np.random.default_rng(S.hseed('sig-topup', spin, P.m, row))    # same top-up at every Lambda
                    Pp = GT.assemble(e, tr, 0, rs, inserted_vp=(GT.SIG_VP,), do_topup=True)
                    barq = Pp['H0'][:, 7].astype(np.int64) == GT.SIG_VP
                    nqw = int(barq.sum())
                    qb = Pp['btl_INT'] % 1_000_000 == GT.SIG_VP
                    if not btl_pu_done:          # PU BTL once per row (S5); quirk BTL per trial below
                        b = btl_rows(Pp, ie)
                        btl.append(b[~qb]); btl_pu_done = True
                        evstats.append([ie, 0] + [Pp['stats'].get(c, 0) for c in RS.EVSTAT_COLS])
                    res, summ, rec = sig_trial(GT, Pp, nqw, pv, phimet, tseed, cfg, wcfg)
                    base = [row, lam, ev['status'], int(excl[lam][job['rows'].index(row)]), nqw, 0]
                    if res is None:
                        sig.append(dict(cols=base + [0, 0, 0, 0.0, float(np.arctan2(met_true[1], met_true[0])), 1],
                                        ti=-1, summ=None))
                        continue
                    ti = add_trial(res, trials, cands, hitrec, ie, dict(sig_row=row, sig_lam=lam))
                    qbtl.append(np.c_[np.full(qb.sum(), ti), Pp['btl'][qb][:, :6], Pp['btl'][qb][:, 11:13]])
                    sig.append(dict(cols=base + [summ['n_q_pool'], summ['n_q_road'], summ['n_cand_q'], summ['best_frac'],
                                                 float(np.arctan2(met_true[1], met_true[0])), 0], ti=ti, summ=summ))
                    srec.append((ti, rec))
            v41 = z['v41']; v41c = cm['v41_cols']; ctim = z['timing']
            v41_pass = bool(cm.get('v41_pass')) and v41_numpy_fail == 0
            chain_meta = {k: v for k, v in cm.items() if k != 'ev_info'}
            z.close()
        else:
            raise KeyError(kind)
    finally:
        for p in (tmpc, rowsf):
            Path(p).unlink(missing_ok=True)
    out = pack_trials(job, trials, cands, hitrec, btl, dumps)
    out['chain.v41'] = v41; out['chain.v41_cols'] = np.array(v41c)
    out['chain.timing'] = ctim; out['chain.timing_cols'] = np.array(chain_meta['timing_cols'])
    if evstats:
        out['chain.evstats'] = np.array(evstats, np.int64)
        out['chain.evstats_cols'] = np.array(['ev', 'k'] + RS.EVSTAT_COLS)
    out['sig.cols'] = np.array(SIG_COLS)
    out['sig.tab'] = np.array([s['cols'] for s in sig], np.float64)
    out['sig.trial'] = np.array([s['ti'] for s in sig], np.int32)
    nR = RS_NR()
    for k in ('eff', 'eff_fckf', 'eff_T', 'eff_fckf_T'):
        out['sig.' + k] = np.packbits(np.array([s['summ'][k] if s['summ'] is not None else np.zeros(nR, bool)
                                                for s in sig], bool).reshape(-1, nR), axis=1)
    for k, v in cat_records(srec).items():
        out['sig.cand.' + k] = v
    if qbtl:
        out['sig.qbtl'] = np.concatenate(qbtl).astype(np.float32)
        out['sig.qbtl_cols'] = np.array(['trial', 'sid', 'x', 'y', 'z', 's0', 's1', 'dE', 't'])
    if var_eff:
        out['sig.var_eff'] = np.packbits(np.array(var_eff, bool), axis=-1)
        out['sig.var_names'] = np.array([v[0] for v in A1_VARIANTS])
        out['sig.var_eff_axes'] = np.array(['event', 'variant', 'eff|eff_fckf|eff_T|eff_fckf_T', 'rung(packed)'])
    v46 = None
    if kind == 'a5':
        sv = chain_meta.get('sig_v41', [])
        nsm = sum(r.get('n_meas_all', 0) for r in sv); nck = sum(r.get('ckf_sig', 0) for r in sv)
        v46 = dict(n_quirk_meas_all_surfaces=nsm, n_on_ckf_tracks=nck, frac=nck / max(nsm, 1))
    extra = dict(v41_pass=v41_pass, v41_numpy_fail=v41_numpy_fail, v46=v46, rungs=list(RS_RUNGS()),
                 sig_definition='eff[r] = some candidate passes rung r (aligned, frozen F0 ladder) and holds >= 50 % of '
                                'the event written barrel quirk measurements (pre-CKF, pre-merge); eff_fckf adds '
                                'f_CKF < 0.2; *_T adds BTL presence')
    if 'ev_info' in chain_meta and kind != 'a5':
        chain_meta = {k: v for k, v in chain_meta.items() if k not in ('ev_info', 'sig_v41')}
    return finish(job, out, extra, t_w0, t_c0, cfg, wcfg, fz, chain_meta, t_chain, len(trials))


def RS_NR():
    from acts.stage4.finder import production as PR
    return PR.NR


def RS_RUNGS():
    from acts.stage4.finder import production as PR
    return PR.RUNGS


# --------------------------------------------------------------------------------------------------------------- C'
CP_EV_COLS = ['ev_global', 'pre', 'chi2pre', 'n_triples', 'n_toy_bar', 'n_toy_all', 'n_key_unmatched', 'n_cand',
              'n_attr_any', 'n_attr_all', 'phimet', 'pv_x', 'pv_y', 'pv_z', 'eligible', 'skipped', 'n_impl', 'n_impl_fail']


def cp_process_event(GT, e, tr, toysim, pv, phimet, tseed, cfg, wcfg, looper, rs, do_topup):
    """One C' event (C'0: no top-up; C'_PU: toy rows already replaced): -> (res or None, attr dict, X, Pp, keys info)."""
    Pp = GT.assemble(e, tr, 0, rs, inserted_vp=(GT.GUN_VP,), do_topup=do_topup)
    H0 = Pp['H0']; T0 = Pp['T0']
    toy0 = np.where(H0[:, 7].astype(np.int64) == GT.GUN_VP)[0]
    keys0, nun = GT.toy_keys(H0[toy0], T0[toy0], toysim)
    if len(Pp['H']) < 3:
        return None, None, None, Pp, (toy0, keys0, nun)
    btl = (Pp['btl'], Pp['btl_INT'])
    res, X = GT.trial(Pp['H'], Pp['sid'], Pp['INT'], pv, phimet, tseed, cfg, wcfg, ckf=Pp['ckf'], btl=btl)
    # toy links in Hp (Fatras part): Hp row j <- H0 row H0_keep[j]
    j, _ = GT.links(Pp, (GT.GUN_VP,))
    kmap = np.full(len(H0), -1, np.int64); kmap[toy0] = keys0
    kj = kmap[Pp['H0_keep'][j]]
    att = GT.attribute(X, Pp, j, kj, pv, looper=looper)
    return res, att, X, Pp, (toy0, keys0, nun)


def cp_records(GT, X, att, F_any, pv, phimet, cfg, Pp):
    sel = np.where(att['attributed'] | (att['n_links'] >= 2))[0]       # attributed + near misses (>= 2 passing links)
    if not len(sel):
        return None
    bt = GT.PR.btl_inputs((Pp['btl'], Pp['btl_INT']), pv, X['A']['INTu'])
    nck, fck, nbt = GT.cand_extra(X, sel, pv, phimet, cfg, Pp['ckf'], bt)
    V = X['r']['vars']
    return dict(idx=sel.astype(np.int32), attributed=att['attributed'][sel], any_rung=F_any[sel],
                n_links=att['n_links'][sel], n_layers=att['n_layers'][sel], n_part=att['n_part'][sel],
                max_cross=att['max_cross'][sel], rungs=np.packbits(X['F'][sel], axis=1),
                n_ckf_band=nck.astype(np.int32), f_ckf=fck.astype(np.float32),
                btl_n_band=np.minimum(nbt, 32767).astype(np.int16), n_band=np.diff(X['hoff'])[sel].astype(np.int32),
                p_chi2core=X['pchi'][sel].astype(np.float32), dedx=X['dedx'][sel].astype(np.float32),
                normal=X['r']['normal'][sel].astype(np.float32), axis=X['r']['axis'][sel].astype(np.float32),
                dphi_met=X['r']['dphi_met'][sel].astype(np.float32), eta_axis=X['eta'][sel].astype(np.float32),
                **{k: V[k][sel].astype(np.float32) for k in ('chi2ndf', 'dw_core', 'chi2_core')},
                **{k: V[k][sel].astype(np.int16) for k in ('nit2', 'nip2', 'n2s2', 'nl2', 'nhit', 'n_core')})


def run_cp0_job(job):
    from acts.stage4.finder import g1b_tt as GT
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    final = RS.out_path(job)
    final.parent.mkdir(parents=True, exist_ok=True)
    fz = RS.frozen_inputs()
    cfg, wcfg = RS.finder_configs(fz, job, False)
    topo = job['topo']
    tmpc = final.with_name(final.name[:-4] + f'.chain{os.getpid()}.npz')
    try:
        t_chain = chain(job, tmpc, ['cp', tmpc, job['n_events'], job['seed'], '--topo', topo])
        z = np.load(tmpc)
        cm = json.loads(str(z['meta']))
        trials = []; cands = []; hitrec = []; btl = []; evrows = []; hashes = []; recs = []; store = {}
        preselect_topo = not (topo in CP_GUNS)
        looper = topo == 'looper'
        for ie in range(job['n_events']):
            info = cm['ev_info'][ie]
            pv = np.array(info['pv'], float); phimet = float(info['phimet'])
            e = z[f'ev{ie}']; tr = z[f'tru{ie}']
            toysim = z[f'toy{ie}'] if f'toy{ie}' in z.files else np.zeros((0, 18))
            g = job['ev0'] + ie
            tseed = RS.hash_seed(f'stage4|Cp0trial|{topo}|{g}')
            toy_all = np.where(e[:, 7].astype(np.int64) == GT.GUN_VP)[0]
            hsh = GT.toy_hash(e[toy_all], tr[toy_all], pv)
            bar = GT.FF.LC_OF[e[toy_all, 0].astype(np.int64)] >= 0
            rb = e[toy_all][bar]
            kb, nun = GT.toy_keys(rb, tr[toy_all][bar], toysim)
            pre, chi2pre, ntri = GT.preselect(rb, kb, pv)
            rs = np.random.default_rng(tseed)
            res, att, X, Pp, _ = cp_process_event(GT, e, tr, toysim, pv, phimet, tseed, cfg, wcfg, looper, rs, False)
            eligible = (pre if preselect_topo else g < CPPU_N)
            if eligible:
                store[f'cp.toyev.{g}'] = e[toy_all]
                store[f'cp.toytru.{g}'] = tr[toy_all]
                store[f'cp.toysim.{g}'] = toysim
            hashes.append(hsh)
            if res is None:
                evrows.append([g, pre, chi2pre, ntri, len(rb), len(toy_all), nun, 0, 0, 0, phimet, *pv, eligible, 1, 0, 0])
                continue
            F_any = X['F'].any(1)
            ti = add_trial(res, trials, cands, hitrec, ie, dict(cp_ev=g))
            btl.append(btl_rows(Pp, ie))
            recs.append((ti, cp_records(GT, X, att, F_any, pv, phimet, cfg, Pp)))
            evrows.append([g, pre, chi2pre, ntri, len(rb), len(toy_all), nun, X['nc'],
                           int((att['attributed'] & F_any).sum()), int(att['attributed'].sum()), phimet, *pv, eligible, 0,
                           att['n_impl'], att['n_impl_fail']])
        v41 = z['v41']; v41c = cm['v41_cols']; ctim = z['timing']
        chain_meta = {k: v for k, v in cm.items() if k != 'ev_info'}
        chain_meta['ev_info_trunc'] = None
        z.close()
    finally:
        Path(tmpc).unlink(missing_ok=True)
    out = pack_trials(job, trials, cands, hitrec, btl, [])
    out.update(store)
    out['chain.v41'] = v41; out['chain.v41_cols'] = np.array(v41c)
    out['chain.timing'] = ctim; out['chain.timing_cols'] = np.array(chain_meta['timing_cols'])
    E = np.array(evrows, np.float64)
    out['cp.ev'] = E; out['cp.ev_cols'] = np.array(CP_EV_COLS)
    out['cp.hash'] = np.array(hashes)
    for k, v in cat_records(recs).items():
        out['cp.cand.' + k] = v
    nonpre = E[:, 1] == 0
    leak = int(E[nonpre, 8].sum())
    n_attr_pre = int(E[~nonpre, 8].sum())
    v410 = dict(topo=topo, preselected_topology=preselect_topo, n_events=len(E), n_pre=int((~nonpre).sum()),
                f_pre=float((~nonpre).mean()) if len(E) else float('nan'), n_attr_nonpre_any_rung=leak,
                n_attr_pre_any_rung=n_attr_pre, pass_=(leak == 0) if preselect_topo else None,
                n_key_unmatched=int(E[:, 6].sum()), n_impl=int(E[:, 16].sum()), n_impl_fail=int(E[:, 17].sum()))
    extra = dict(v41_pass=bool(chain_meta.get('v41_pass')), v410=v410, rungs=list(RS_RUNGS()))
    return finish(job, out, extra, t_w0, t_c0, cfg, wcfg, fz, chain_meta, t_chain, len(trials))


def cp0_sources(job):
    """All C'0 outputs of job['topo'] -> (V4-10 summary, ordered list of source global event ids, file of each)."""
    pre = []; leak = 0; npre = 0; nev = 0; files = {}
    for p in sorted(job['needs']):
        with np.load(PROD.joinpath(*p.split('/')), allow_pickle=False) as z:
            E = z['cp.ev']
            m = json.loads(str(z['meta_json']))
            leak += int(m['v410']['n_attr_nonpre_any_rung'])
            npre += int(m['v410']['n_pre']); nev += int(m['v410']['n_events'])
            el = E[E[:, 14] == 1, 0].astype(np.int64)
            for g in el:
                files[int(g)] = p
            pre += el.tolist()
    return dict(leak=leak, n_pre=npre, n_events=nev), sorted(pre), files


def run_cppu_job(job):
    from acts.stage4.finder import g1b_tt as GT
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    final = RS.out_path(job)
    final.parent.mkdir(parents=True, exist_ok=True)
    fz = RS.frozen_inputs()
    cfg, wcfg = RS.finder_configs(fz, job, False)
    topo = job['topo']
    v410, pre, files = cp0_sources(job)
    preselect_topo = topo not in CP_GUNS
    if preselect_topo and v410['leak'] != 0:
        raise RuntimeError(f"V4-10 FAILED for {topo}: {v410['leak']} attributed candidates in non-preselected C'0 events; "
                           "C'_PU not run (WP_RULE §7)")
    if not pre:          # N_pre = 0: f_pre under §4.2, conditional = 1, the with-PU events are not run
        out = dict(job_id=np.array(job['id']), complete=np.array(1), n_trials=np.array(0))
        extra = dict(v410_sources=v410, note='N_pre = 0: not run (WP_RULE §7 sampling)', v41_pass=True)
        return finish(job, out, extra, t_w0, t_c0, cfg, wcfg, fz, {}, 0.0, 0)
    slots = list(range(job['slot0'], job['slot0'] + job['n_events']))
    src = [pre[s % len(pre)] for s in slots]
    rep = [s // len(pre) for s in slots]
    tmpc = final.with_name(final.name[:-4] + f'.chain{os.getpid()}.npz')
    cpf = final.with_name(final.name[:-4] + f'.cp{os.getpid()}.npz')
    evf = final.with_name(final.name[:-4] + f'.ev{os.getpid()}.json')
    srcd = {}
    for g in sorted(set(src)):
        with np.load(PROD.joinpath(*files[g].split('/')), allow_pickle=False) as z:
            E = z['cp.ev']
            k = int(np.where(E[:, 0] == g)[0][0])
            srcd[g] = dict(ev=z[f'cp.toyev.{g}'], tru=z[f'cp.toytru.{g}'], sim=z[f'cp.toysim.{g}'], hash=str(z['cp.hash'][k]),
                           pv=E[k, 11:14].copy(), phimet=float(E[k, 10]))
    try:
        info = [dict(pv=srcd[g]['pv'].tolist(), phimet=srcd[g]['phimet'], src=g) for g in src]
        np.savez(cpf, meta=np.array(json.dumps(dict(topo=topo, job_seed=job['seed'], ev_info=info))),
                 **{f'toy{i}': srcd[g]['sim'] for i, g in enumerate(src)})
        evf.write_text(json.dumps(list(range(len(src)))))
        t_chain = chain(job, tmpc, ['cppu', tmpc, len(src), job['seed'], '--cp-file', cpf, '--cp-events', evf])
        z = np.load(tmpc)
        cm = json.loads(str(z['meta']))
        trials = []; cands = []; hitrec = []; btl = []; evrows = []; recs = []; hrows = []; evstats = []
        for ie, g in enumerate(src):
            sd = srcd[g]
            pv = sd['pv']; phimet = sd['phimet']
            e0 = z[f'ev{ie}']; tr = z[f'tru{ie}']
            e, nmat, nun_pu, nun_c0 = GT.replace_toy_rows(e0, tr, sd['ev'], sd['tru'])
            toy_all = np.where(e[:, 7].astype(np.int64) == GT.GUN_VP)[0]
            hsh = GT.toy_hash(e[toy_all], tr[toy_all], pv)
            hrows.append([ie, g, rep[ie], nmat, nun_pu, nun_c0, int(hsh == sd['hash'])])
            tseed = RS.hash_seed(f'stage4|CpPUtrial|{topo}|{slots[ie]}')
            rs = np.random.default_rng(tseed)
            res, att, X, Pp, kinfo = cp_process_event(GT, e, tr, sd['sim'], pv, phimet, tseed, cfg, wcfg,
                                                      topo == 'looper', rs, True)
            evstats.append([ie, 0] + [Pp['stats'].get(c, 0) for c in RS.EVSTAT_COLS])
            btl.append(btl_rows(Pp, ie))
            F_any = X['F'].any(1)
            ti = add_trial(res, trials, cands, hitrec, ie, dict(cp_ev=g, cp_slot=slots[ie]))
            recs.append((ti, cp_records(GT, X, att, F_any, pv, phimet, cfg, Pp)))
            evrows.append([slots[ie], g, rep[ie], X['nc'], int((att['attributed'] & F_any).sum()),
                           int(att['attributed'].sum()), kinfo[2], att['n_impl'], att['n_impl_fail']])
        v41 = z['v41']; v41c = cm['v41_cols']; ctim = z['timing']
        chain_meta = {k: v for k, v in cm.items() if k not in ('ev_info', 'toy_info')}
        z.close()
    finally:
        for p in (tmpc, cpf, evf):
            Path(p).unlink(missing_ok=True)
    out = pack_trials(job, trials, cands, hitrec, btl, [])
    out['chain.v41'] = v41; out['chain.v41_cols'] = np.array(v41c)
    out['chain.timing'] = ctim; out['chain.timing_cols'] = np.array(chain_meta['timing_cols'])
    out['chain.evstats'] = np.array(evstats, np.int64)
    out['chain.evstats_cols'] = np.array(['ev', 'k'] + RS.EVSTAT_COLS)
    out['cp.ev'] = np.array(evrows, np.float64)
    out['cp.ev_cols'] = np.array(['slot', 'src_ev_global', 'repeat', 'n_cand', 'n_attr_any', 'n_attr_all',
                                  'n_key_unmatched', 'n_impl', 'n_impl_fail'])
    H = np.array(hrows, np.int64)
    out['cp.hashcheck'] = H
    out['cp.hashcheck_cols'] = np.array(['ev', 'src', 'repeat', 'n_matched', 'n_pu_toy_unmatched', 'n_c0_unmatched',
                                         'hash_equal'])
    for k, v in cat_records(recs).items():
        out['cp.cand.' + k] = v
    hash_pass = bool(np.all(H[:, 6] == 1))
    EV = np.array(evrows, np.float64)
    impl = dict(n_impl=int(EV[:, 7].sum()), n_impl_fail=int(EV[:, 8].sum()))
    extra = dict(v41_pass=bool(chain_meta.get('v41_pass')) and bool(cm.get('v41_pass', True)), v410_sources=v410,
                 v410_hash_pass=hash_pass, n_pre=len(pre), implication=impl, rungs=list(RS_RUNGS()))
    return finish(job, out, extra, t_w0, t_c0, cfg, wcfg, fz, chain_meta, t_chain, len(trials))


def run_job(job, allow_interim=False):
    if job['kind'] in ('a1', 'a2', 'a5'):
        return run_signal_job(job)
    if job['kind'] == 'cp0':
        return run_cp0_job(job)
    if job['kind'] == 'cppu':
        return run_cppu_job(job)
    raise KeyError(job['kind'])


def check_job(job):
    """V4-1 / V4-10 per output (run_stage4 check hook): -> dict(v41_pass, v410_pass or None)."""
    with np.load(RS.out_path(job), allow_pickle=False) as z:
        m = json.loads(str(z['meta_json']))
    v410 = None
    if job['kind'] == 'cp0' and m.get('v410', {}).get('preselected_topology'):
        v410 = bool(m['v410']['pass_'])
    if job['kind'] == 'cppu' and 'v410_hash_pass' in m:
        v410 = bool(m['v410_hash_pass']) and int(m.get('implication', {}).get('n_impl_fail', 0)) == 0
    if job['kind'] == 'cp0' and int(m.get('v410', {}).get('n_impl_fail', 0)) > 0:
        v410 = False
    return dict(v41_pass=m.get('v41_pass'), v410_pass=v410)


# ---------------------------------------------------------------------------------------------------------- driver
def cmd_smoke(argv):
    camp = 'smokeG1b'
    jobs = manifest_jobs(camp)
    RS.JOBS.mkdir(parents=True, exist_ok=True)
    (RS.JOBS / f'{camp}.json').write_text(json.dumps(dict(campaign=camp, jobs=jobs), indent=1))
    only = argv[0].split(',') if argv else None
    order = sorted(jobs, key=lambda j: j.get('order', 0))
    res = []
    for j in order:
        if only and j['kind'] not in only:
            continue
        if validate(j, deep=True):
            print('skip (done)', j['id'], flush=True)
            continue
        if not needs_ok(j):
            print('skip (needs)', j['id'], flush=True)
            continue
        t0 = time.time()
        r = run_job(j)
        r['t'] = time.time() - t0
        res.append(r)
        print(json.dumps(r, default=str), flush=True)
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'smoke':
        sys.exit(cmd_smoke(sys.argv[2:]))
    print(__doc__)
