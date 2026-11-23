"""p2u_d2_find.py -- D2 robustness row "later arcs restored" (plan outputs/D2_PLAN_ulrika_2026-11-19.md), step 2: the frozen
v1 finder on the varied events (or, with --no-inject, the control on the nominal dumps).

  <tt python> p2u_d2_find.py --id ID --nom <c1pu1-K.npz> [--var <p2u_d2_chain output>] --lo A --hi B [--no-inject]

Per event ie in [A, B) of the nominal job (the same per-event random stream SeedSequence(job seed).spawn(n)[ie] as
run_stage4.run_pu_job, so PV, road angles and trial seeds are those of the nominal):
  finder input = the nominal event's own pre-top-up hits (its S6 dump: barrel counting + BTL, with the CKF flags the
  nominal chain gave) + (unless --no-inject) the injected measurements of the varied chain;
  top-up = pu_inputs.topup drawn on the NOMINAL hits only (identical draws), then the last n_inj(layer) top-up crossings
  of each layer dropped (both sensors; n_inj = injected measurements on the layer, inner sensor for stacked layers,
  before CKF removal); CKF removal, U-5 b merging, PV, roads and production.process_trial as run_stage4.run_pu_job.
No v1 file is changed.  Output <ID>.npz in $QV2_OUT_DIR in the layout of run_stage4.pack (trials.*, cand.*, hit.*) plus
hit.inj / hit.vsec (pool row of each hit-record hit: injected member, vsec), d2.layer (per event and layer: n_inj,
top-up crossings, dropped, excess) and meta_json.  No signal file is read.
"""
import argparse
import inspect
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
log = logging.getLogger('p2u_d2_find')


def event_from_dump(z, ie):
    """The nominal chain event ie (barrel counting + BTL written measurements) from its S6 dump, run_chain.COLS order."""
    p = f'dump.{ie}_0.'
    n = len(z[p + 'sid'])
    ev = np.zeros((n, 13))
    ev[:, 0] = z[p + 'sid']; ev[:, 1:4] = z[p + 'xyz']; ev[:, 4:6] = z[p + 's01']; ev[:, 6] = z[p + 'flag']
    ev[:, 7] = z[p + 'vp']; ev[:, 8] = z[p + 'particle']; ev[:, 9] = z[p + 'gen']; ev[:, 10] = z[p + 'vsec']
    ev[:, 11] = z[p + 'dE']; ev[:, 12] = z[p + 't']
    return ev, z[p + 'tru'], z[p + 'vz'].astype(np.float64)


def prepare_event_d2(ev, tru, vz, inj, tag, rng, FF, PI, CI):
    """chain_inputs.prepare_event (do_topup, nominal ratios, ckf_remove, merge, scale 1) with the D2 top-up exchange.
    inj: bool per row of ev (injected measurement).  With no injected row the result equals prepare_event's."""
    sid_all = ev[:, 0].astype(np.int64)
    INT_all = tag * 1_000_000 + ev[:, 7].astype(np.int64)
    bar = FF.LC_OF[sid_all] >= 0
    btl = CI.KIND[sid_all] == 'BTL'
    H0 = ev[bar]; s0 = sid_all[bar]; I0 = INT_all[bar]; T0 = tru[bar].astype(np.float64); J0 = inj[bar]
    st = dict(n_fatras=int(np.sum(~J0)), n_inj_barrel=int(J0.sum()))
    t, ti = PI.topup(H0[~J0], s0[~J0], rng, tag, None)           # the nominal draws, from the nominal hits only
    lay = []
    keep = np.ones(len(t), bool)
    base = tag * 1_000_000 + 500_000
    for li, name in enumerate(FF.LAYERS):
        ids = [FF.SID[name]] if li < 4 else [FF.SID[name + '_in'], FF.SID[name + '_out']]
        n_inj = int(np.sum(J0 & (s0 == ids[0])))
        on = np.isin(t[:, 0].astype(np.int64), ids)
        kk = ti[on] - base
        ntop = int(len(np.unique(kk)))
        ndrop = min(n_inj, ntop)
        if ndrop:
            kmax = kk.max()
            drop = on.copy(); drop[on] = kk > kmax - ndrop
            keep &= ~drop
        lay.append((li, n_inj, int(np.sum(J0 & (s0 == ids[-1]))), ntop, ndrop, max(0, n_inj - ntop)))
    t = t[keep]; ti = ti[keep]
    st['n_topup'] = int(len(t))
    ck = (H0[:, 6].astype(np.int64) & 1) == 1
    st['n_ckf_removed'] = int(ck.sum())
    Hp = np.concatenate([H0[~ck], t]); Ip = np.concatenate([I0[~ck], ti])
    Tp = np.concatenate([T0[~ck], t[:, 1:4]])
    Jp = np.concatenate([J0[~ck], np.zeros(len(t), bool)])
    Vp = np.concatenate([H0[~ck, 10], np.full(len(t), -1.0)])
    Hm, mapi, ng, nh, nenl = CI.merge_pool(Hp, Tp, 1.0)
    Im = np.zeros(len(Hm), np.int64)
    Im[mapi] = Ip
    if ng:
        sz = np.bincount(mapi, minlength=len(Hm))
        for j in np.where(sz > 1)[0]:
            mem = np.where(mapi == j)[0]
            Im[j] = Ip[mem[np.argmax(Hp[mem, 11])]]
    Jm = np.zeros(len(Hm), bool); np.logical_or.at(Jm, mapi, Jp)
    Vm = np.full(len(Hm), -1.0); Vm[mapi] = Vp
    st.update(n_pool=int(len(Hm)), n_merged_groups=ng, n_merged_hits=nh, n_sigma_enlarged=nenl, n_inj_pool=int(Jm.sum()))
    uz = np.array(sorted(set(np.round(vz[:, 3], 6)))) if len(vz) else np.zeros(0)
    return dict(H=Hm, sid=Hm[:, 0].astype(np.int64), INT=Im, btl=ev[btl], btl_INT=INT_all[btl], uz=uz, ckf=H0[ck],
                inj=Jm, vsec=Vm, stats=st, layers=lay)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--id', required=True); ap.add_argument('--nom', required=True); ap.add_argument('--var', default=None)
    ap.add_argument('--lo', type=int, required=True); ap.add_argument('--hi', type=int, required=True)
    ap.add_argument('--no-inject', action='store_true')
    ap.add_argument('--check-prepare', action='store_true', help='also assert equality with chain_inputs.prepare_event')
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', stream=sys.stderr)
    out_dir = Path(os.environ.get('QV2_OUT_DIR', '.'))
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    sys.path.insert(0, str(QV2))
    os.chdir(QV2)
    from acts.stage4 import run_stage4 as RS
    from acts.stage4.finder import production as PR
    from acts.stage4.finder import pu_inputs as PI
    from acts.stage4.finder import chain_inputs as CI
    from acts.stage4.finder import finder as FF
    PT_PARAMS = inspect.signature(PR.process_trial).parameters
    fz = RS.frozen_inputs()
    if fz is None or fz.get('wp_rule_sha256') != RS.sha256_file(RS.HERE / 'WP_RULE.md'):
        raise SystemExit('frozen_inputs / WP_RULE.md mismatch')
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    zn = np.load(a.nom)
    mn = json.loads(str(zn['meta_json']))
    njob = mn['job']
    assert njob['rho'] == 1 and njob['kind'] == 'pu'
    seed = int(njob['seed']); n_ev = int(njob['n_events']); roads = int(njob['roads'])
    zv = None
    if not a.no_inject:
        zv = np.load(a.var)
        mv = json.loads(str(zv['meta']))
        assert int(mv['job_seed']) == seed and mv['nominal_job']['id'] == njob['id'], 'varied chain is not of this nominal job'
    job = dict(id=a.id, campaign='D2', sample=njob['sample'], kind='pu', chunk=njob['chunk'], ev0=njob['ev0'], n_events=n_ev,
               roads=roads, rho=1, seed=seed, dump_events=0, out=f'{a.id}.npz', d2_events=[a.lo, a.hi],
               d2_inject=not a.no_inject, nominal=njob['id'])
    cfg, wcfg = RS.finder_configs(fz, job, False)
    ev_streams = np.random.SeedSequence(seed).spawn(n_ev)
    trials = []; cands = []; hitrec = []; btl = []; layrec = []; evstats = []; hinj = []; hvsec = []
    for ie in range(a.lo, a.hi):
        rs = np.random.default_rng(ev_streams[ie])
        ev, tru, vz = event_from_dump(zn, ie)
        inj = np.zeros(len(ev), bool)
        if zv is not None:
            ei = zv[f'inj{ie}'].copy(); et = zv[f'injtru{ie}']
            for c_ in (4, 5, 11, 12):          # the dumps store s0, s1, dE, t as float32: same precision for injected rows
                ei[:, c_] = ei[:, c_].astype(np.float32).astype(np.float64)
            ev = np.concatenate([ev, ei]); tru = np.concatenate([tru, et.astype(tru.dtype)])
            inj = np.concatenate([inj, np.ones(len(ei), bool)])
        if a.check_prepare and not inj.any():
            ref = CI.prepare_event(ev, tru, vz, 0, np.random.default_rng(ev_streams[ie]),
                                   ratios=RS.topup_ratios(job.get('topup', 'nominal')))
        p = prepare_event_d2(ev, tru, vz, inj, 0, rs, FF, PI, CI)
        if a.check_prepare and not inj.any():
            for k in ('H', 'sid', 'INT', 'btl', 'btl_INT', 'uz', 'ckf'):
                assert np.array_equal(ref[k], p[k]), f'prepare_event_d2 differs from prepare_event in {k} (event {ie})'
        evstats.append([ie] + [p['stats'][c] for c in ('n_fatras', 'n_inj_barrel', 'n_topup', 'n_ckf_removed', 'n_pool',
                                                        'n_merged_groups', 'n_merged_hits', 'n_sigma_enlarged', 'n_inj_pool')])
        layrec += [[ie, *x] for x in p['layers']]
        H = p['H']; sid = p['sid']; INT = p['INT']; uz = p['uz']
        key = {(int(s_), np.float32(x_), np.float32(y_), np.float32(z_)): j
               for j, (s_, x_, y_, z_) in enumerate(zip(sid, H[:, 1], H[:, 2], H[:, 3]))}
        pv = PI.lum_pv(rs)
        phi0 = rs.uniform(-np.pi, np.pi)
        dz = float(np.min(np.abs(uz - pv[2]))) if len(uz) else np.nan
        b = p['btl']
        btl.append(np.c_[np.full(len(b), ie), b[:, :6], b[:, 11:13], p['btl_INT']])
        for road in range(roads):
            phimet = float((phi0 + road * 2 * np.pi / roads + np.pi) % (2 * np.pi) - np.pi)
            tseed = int(rs.integers(0, 2 ** 62))
            kw = {}
            if 'ckf' in PT_PARAMS:
                kw['ckf'] = p['ckf']
            if 'btl' in PT_PARAMS:
                kw['btl'] = (p['btl'], p['btl_INT'])
            res = PR.process_trial(H, sid, INT, pv, phimet, 1.0, tseed, cfg=cfg, wcfg=wcfg, **kw)
            row = res['row']
            if 'road' in row:
                row['road_cfg'] = row['road']
            row.update(ev=job['ev0'] + ie, road=road, dz_nearest_pu=dz, trial_seed=tseed)
            ti = len(trials)
            trials.append(row)
            c = res['cand']; c['trial'] = np.full(len(c['idx']), ti, np.int32)
            if 'n_ckf_band' not in c:
                c['n_ckf_band'] = CI.ckf_band_counts(p['ckf'], pv, phimet, c['normal'], c['axis'], w_c=cfg.w_c, road=cfg.road,
                                                     t_tol=cfg.t_tol)
            cands.append(c)
            h = res['hit']
            if h is not None:
                hitrec.append((ti, h))
                j = np.array([key.get((int(s_), x_[0], x_[1], x_[2]), -1) for s_, x_ in zip(h['sid'], h['xyz'])], np.int64)
                if np.any(j < 0):
                    raise RuntimeError(f'hit record row not found in the pool (event {ie})')
                hinj.append(p['inj'][j]); hvsec.append(p['vsec'][j])
        log.info('event %d: %s', ie, json.dumps(p['stats']))
    out = RS.pack(job, trials, cands, hitrec, btl, [])
    if hinj:
        out['hit.inj'] = np.concatenate(hinj); out['hit.vsec'] = np.concatenate(hvsec).astype(np.int32)
    out['d2.layer'] = np.array(layrec, np.int64)
    out['d2.layer_cols'] = np.array(['ev', 'layer', 'n_inj', 'n_inj_outer', 'n_topup_cross', 'n_dropped', 'excess'])
    out['d2.evstats'] = np.array(evstats, np.int64)
    out['d2.evstats_cols'] = np.array(['ev', 'n_fatras', 'n_inj_barrel', 'n_topup', 'n_ckf_removed', 'n_pool', 'n_merged_groups',
                                       'n_merged_hits', 'n_sigma_enlarged', 'n_inj_pool'])
    meta = dict(job=job, nominal_file=a.nom, varied_file=a.var, finder_cfg=dict(road=cfg.road, w_c=cfg.w_c, t_tol=cfg.t_tol,
                                                                                  tseed=cfg.tseed, iters=cfg.iters),
                wcfg=vars(wcfg), frozen_inputs=fz, code_sha256=dict(RS.code_hashes(), **{Path(__file__).name: RS.sha256_file(Path(__file__))}),
                created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), wall_s=time.perf_counter() - t_w0,
                cpu_s=time.process_time() - t_c0, rungs=PR.RUNGS)
    out['meta_json'] = np.array(json.dumps(meta, default=str))
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = out_dir / f'{a.id}.tmp.npz'
    with open(tmp, 'wb') as f:
        np.savez_compressed(f, **out)
    os.replace(tmp, out_dir / f'{a.id}.npz')
    log.info('done: %d trials, %.1f s', len(trials), meta['wall_s'])


if __name__ == '__main__':
    main()
