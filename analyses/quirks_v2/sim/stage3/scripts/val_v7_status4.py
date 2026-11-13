"""val_v7_status4.py -- Stage-3 V7 follow-up (plan §5 V7, §6.3): the production events that ended with status 4 (string
queue deadlock after the bootstrap, nsteps >= 1000, so the kernel's built-in label-swap retry did not apply) are
(a) rerun exactly as in production on the Mac (determinism; for PC events also a cross-machine check), and
(b) rerun with the label swap the plan prescribes ("rerun ... with the label swap", §6.3): the pair is passed as
    (p_qm, p_qp) with charges (-1, +1) -- the same physical event, the first string vector given to the other quirk --
    and the quirk labels are swapped back, exactly as the kernel wrapper does for bootstrap deadlocks.
The production files are NOT modified.  The swapped reruns are stored as replacement candidates in
data/sim_stage3/validation/v7_status4/status4_rerun.npz (hits in mm/ns/GeV, production hit columns; per event the job id,
event index, row, status, nsteps, ds_*), so Stage 4 can substitute them if it wants complete events.
Output: sim/stage3/results/V7_status4.json.  Run (theory_track/): pixi run python sim/stage3/scripts/val_v7_status4.py
"""
import json
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import s3common as C

VD = C.DATA / 'validation' / 'v7_status4'


def one(task):
    import run_stage3 as R
    from T3_causal_s3 import run_causal_s3, load_surfaces
    from s3_physics import plane_fit
    jid, path, i, spin, m, lam, cfg, mb, hmax, vertex, p1, p2, v, row = task
    kw = dict(R.CONFIGS[cfg])
    seed = R.event_seed(spin, m, row, lam, cfg)
    x0 = np.array([v[3] * R.C_CM_PER_NS, v[0] / 10, v[1] / 10, v[2] / 10]) if vertex == 'lumi' else np.zeros(4)
    t0 = time.process_time()
    ra = run_causal_s3(p1, p2, m, lam, max_boost=mb, hmax_trk=hmax, seed=seed, vertex=x0, **kw)
    ta = time.process_time() - t0
    t0 = time.process_time()
    rb = run_causal_s3(p2, p1, m, lam, max_boost=mb, hmax_trk=hmax, seed=seed, vertex=x0, charges=(-1.0, 1.0),
                       _swapped=True, **kw)
    tb = time.process_time() - t0
    h = rb['hits'].copy()
    if len(h):
        h[:, 0] = 1 - h[:, 0]
    S = load_surfaces(); kinds = np.array(S['kinds'])
    L = h[:, 1].astype(int) if len(h) else np.zeros(0, int)
    org = x0[1:]
    ds = {}
    for nm, ks in (('ds_barrel_um', ['T3V']), ('ds_all_um', ['IT', 'PS', '2S']), ('ds_itps_um', ['IT', 'PS'])):
        sel = np.isin(L, np.where(np.isin(kinds, ks))[0])
        ds[nm] = plane_fit(h[sel, 4:7], org)[0] * 1e4 if len(h) else np.nan
    hh = np.zeros((len(h), 12))
    if len(h):
        hh[:, :3] = h[:, :3]; hh[:, 3] = h[:, 3] / R.C_CM_PER_NS; hh[:, 4:7] = h[:, 4:7] * 10; hh[:, 7:11] = h[:, 7:11]
        hh[:, 11] = h[:, 11] * 10
    return dict(id=jid, file=path, i=i, row=row, cfg=cfg, lam=lam, m=m, spin=spin, status_rerun=int(ra['status']),
                nsteps_rerun=int(ra['nsteps']), nhit_rerun=len(ra['hits']), cpu_rerun=ta, status_swap=int(rb['status']),
                nsteps_swap=int(rb['nsteps']), nhit_swap=len(h), cpu_swap=tb, hits=hh, **ds)


def main():
    idx = C.load_index()
    tasks = []; orig = {}
    for key, P in idx['points'].items():
        if key.startswith('xover/'):
            continue
        for ch in P['chunks']:
            if ch['status'][4] == 0:
                continue
            with np.load(C.DATA / ch['file']) as z:
                inp = np.load(C.DATA / 'inputs' / P['input'])
                for i in np.where(z['status'] == 4)[0]:
                    k = int(z['ev_index'][i])
                    tasks.append((ch['id'], ch['file'], int(i), P['spin'], float(P['m']), float(P['lam_keV']), P['cfg'],
                                  float(P['max_boost']), 0.2, P['vertex'], z['p_qp'][i], z['p_qm'][i], inp['vtx_lumi'][k],
                                  int(z['row'][i])))
                    orig[(ch['id'], int(i))] = dict(nsteps=int(z['nsteps'][i]), nhit=int(z['hit_offsets'][i + 1] - z['hit_offsets'][i]),
                                                    machine=ch['machine'], swapped=bool(z['swapped'][i]))
    print(len(tasks), 'status-4 events', flush=True)
    tasks.sort(key=lambda t: -t[5])
    tic = time.time()
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        R = list(ex.map(one, tasks))
    VD.mkdir(parents=True, exist_ok=True)
    offs = np.cumsum([0] + [len(r['hits']) for r in R])
    H = np.concatenate([r['hits'] for r in R]) if R else np.zeros((0, 12))
    np.savez_compressed(VD / 'status4_rerun.npz', job_id=np.array([r['id'] for r in R]), event_index_in_file=np.array([r['i'] for r in R]),
                        row=np.array([r['row'] for r in R]), status=np.array([r['status_swap'] for r in R]),
                        nsteps=np.array([r['nsteps_swap'] for r in R]), ds_barrel_um=np.array([r['ds_barrel_um'] for r in R]),
                        ds_all_um=np.array([r['ds_all_um'] for r in R]), ds_itps_um=np.array([r['ds_itps_um'] for r in R]),
                        hit_offsets=offs, hits=H,
                        hit_columns=np.array(['quirk', 'surf', 'icross', 't', 'x', 'y', 'z', 'px', 'py', 'pz', 'E', 'dl']),
                        note=np.array('label-swapped reruns of the production status-4 events (V7); units mm, ns, GeV; '
                                      'no dE_sensor column (recompute with s3_physics.dE_sensor if needed)'))
    rows = []
    for r in R:
        o = orig[(r['id'], r['i'])]
        rows.append({k: v for k, v in r.items() if k != 'hits'} | dict(machine=o['machine'], nsteps_prod=o['nsteps'],
                                                                     nhit_prod=o['nhit'], swapped_prod=o['swapped'],
                                                                     reproduced=bool(r['status_rerun'] == 4 and r['nsteps_rerun'] == o['nsteps']
                                                                                     and r['nhit_rerun'] == o['nhit'])))
    st = np.array([r['status_swap'] for r in R])
    res = dict(n_events=len(R), wall_s=time.time() - tic, cpu_h=sum(r['cpu_rerun'] + r['cpu_swap'] for r in R) / 3600,
               n_reproduced_status4=int(sum(r['reproduced'] for r in rows)),
               reproduced_by_machine={m_: [int(sum(r['reproduced'] for r in rows if r['machine'] == m_)),
                                           int(sum(1 for r in rows if r['machine'] == m_))] for m_ in ('mac', 'pc')},
               swap_status_counts=np.bincount(st, minlength=6).tolist(), events=rows)
    C.dump('V7_status4.json', res)
    print(json.dumps({k: v for k, v in res.items() if k != 'events'}, indent=1, default=C._default))


if __name__ == '__main__':
    main()
