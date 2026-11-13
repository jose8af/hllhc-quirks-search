"""G2b: rho = 2 timing at the normalised density INCLUDING the in-job weights (plan §11 G2b), PU-only, one process,
one thread.  The trial set is the G2a one (trials.py, rho = 2 trial i = fix-R1 events (2i, 2i+1) superposed, each with
its own IT + OT top-up), so t2 here is directly comparable with the G2a finder-only t2.  Each trial runs the full
production per-trial path (production.process_trial): finder, distinct-hit-set grouping, full-set rung flags, exact
counting DP on every set, IS per-subset weights on the pre-declared group sub-sample, sums, storage selection; and the
per-trial output is written to a compressed npz to measure the disk size per trial.
Run (theory_track): nice -n 10 pixi run python -m acts.stage4.finder.bench_g2b <i0> <i1> <nsub> <f_is> [tag]
  -> data/acts_stage4/g2b/timing_g2b[_tag].json, per-trial outputs data/acts_stage4/g2b/out_<tag>/
"""
import io
import json
import resource
import sys
import time

import numpy as np

from . import production as PR
from . import trials as TR

G2B = TR.TT / 'data' / 'acts_stage4' / 'g2b'
MIP_TIMING = 4.4e-4     # GeV: median path-corrected dE of PU IT hits with dE > 0 (timing only; NOT the G1 calibration)


def npz_bytes(d):
    b = io.BytesIO()
    flat = {}
    for k, v in d.items():
        if v is None:
            continue
        if isinstance(v, dict):
            for kk, vv in v.items():
                if isinstance(vv, np.ndarray):
                    flat[k + '.' + kk] = vv
        elif isinstance(v, np.ndarray):
            flat[k] = v
    np.savez_compressed(b, **flat)
    return b.getbuffer().nbytes, flat


def main(i0, i1, nsub, f_is, tag):
    out_dir = G2B / f'out_{tag}'
    out_dir.mkdir(parents=True, exist_ok=True)
    wcfg = PR.WCfg(nsub=nsub, f_is=f_is, mip_gev=MIP_TIMING)
    rows = []
    first = True
    for i in range(i0, i1):
        x = TR.trial_inputs(i, 2)
        if first:            # numba compile / cache load: once per job, not per trial
            t0 = time.perf_counter()
            PR.process_trial(x['H'], x['sid'], x['INT'], x['pv'], x['phimet'], 2.0, 1, wcfg=PR.WCfg(nsub=4, f_is=0.01,
                                                                                                      mip_gev=MIP_TIMING))
            t_first = time.perf_counter() - t0
            first = False
        w0 = time.perf_counter(); c0 = time.process_time()
        res = PR.process_trial(x['H'], x['sid'], x['INT'], x['pv'], x['phimet'], 2.0, 9_000_000 + i, wcfg=wcfg)
        wall = time.perf_counter() - w0; cpu = time.process_time() - c0
        nb, flat = npz_bytes(dict(cand=res['cand'], hit=res['hit']))
        rw = res['row']
        np.savez_compressed(out_dir / f'trial_{i:03d}.npz', **flat,
                            **{'row.' + k: np.asarray(v) for k, v in rw.items() if k != 'times'})
        row = dict(trial=i, wall_s=round(wall, 3), cpu_s=round(cpu, 3), times_s={k: round(v, 3) for k, v in rw['times'].items()},
                   n_loose=rw['n_loose'], n_groups=rw['n_groups'], n_ip2ge7=rw['n_ip2ge7'], n_ip2ge6=rw['n_ip2ge6'],
                   n_is_groups=rw['n_is_groups'], n_is_sets=rw['n_is_sets'], M_max=rw['M_max'],
                   is_zero_draw_frac=rw['is_zero_draw_frac'], bytes_store=int(nb),
                   S_uni={k: float(v) for k, v in zip(PR.RUNGS, rw['S_uni'])},
                   S_ded={k: float(v) for k, v in zip(PR.RUNGS, rw['S_ded'])},
                   relerr_is_uni={k: (float(np.sqrt(vv) / v) if v > 0 else None) for k, v, vv in
                                  zip(PR.RUNGS, rw['S_uni'], rw['V_uni'])},
                   n_pass={k: int(v) for k, v in zip(PR.RUNGS, rw['n_pass'])},
                   n_grp={k: int(v) for k, v in zip(PR.RUNGS, rw['n_grp'])},
                   maxrss_GB=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3))
        rows.append(row)
        print(json.dumps({k: row[k] for k in ('trial', 'wall_s', 'times_s', 'n_loose', 'n_groups', 'n_is_sets',
                                              'bytes_store', 'maxrss_GB')}), flush=True)
    t = np.array([r['wall_s'] for r in rows])
    rngb = np.random.default_rng(7)
    bs = rngb.choice(t, (4000, len(t)))
    summ = dict(n=len(t), mean=float(t.mean()), median=float(np.median(t)), p90=float(np.percentile(t, 90)),
                min=float(t.min()), max=float(t.max()), mean_err=float(t.std(ddof=1) / np.sqrt(len(t))) if len(t) > 1 else 0,
                median_boot68=[float(np.percentile(np.median(bs, 1), 16)), float(np.percentile(np.median(bs, 1), 84))])
    stages = {k: float(np.mean([r['times_s'].get(k, 0) for r in rows])) for k in rows[0]['times_s']}
    out = dict(rho=2, nsub=nsub, f_is=f_is, mip_timing_gev=MIP_TIMING, first_call_s=round(t_first, 2), summary_wall=summ,
               stage_means_s=stages, bytes_per_trial_mean=float(np.mean([r['bytes_store'] for r in rows])),
               maxrss_GB=max(r['maxrss_GB'] for r in rows), trials=rows,
               note='one process, one thread; input preparation (PU read + top-up) excluded as in G2a')
    (G2B / f'timing_g2b_{tag}.json').write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ('summary_wall', 'stage_means_s', 'bytes_per_trial_mean', 'maxrss_GB')}, indent=1))


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]),
         sys.argv[5] if len(sys.argv) > 5 else 'dev')
