"""Check that a p3-e-devpu1 output has the c1.pu1 schema and is read by the p3-b readers unchanged (p3-e, Hilde).

  python reader_check.py NEW.npz REF.npz OUT.json        (tt env, on a worker, niced)

1. same npz keys, dtypes and per-key trailing shapes as the reference c1.pu1 file (row counts may differ);
2. meta job: stream, seed = hash_seed("qv2|<stream>|<chunk>"), n_events, rho, roads, dump_events;
3. p3b direct_job.job_counts (with its in-job identity checks of R04-R14 counts and rung bits) on both files;
4. p3b occ_replay.replay of event 0 and the last event of NEW: replayed PV / phimet equal the stored trials (the
   occin_job check).
"""
import json
import sys
from pathlib import Path

import numpy as np

AN = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(AN / 'phase3_selection/src/p3b'))
sys.path.insert(0, str(AN))
import direct_job as DJ  # noqa: E402
import occ_replay as RP  # noqa: E402
from acts.stage4 import run_stage4 as RS  # noqa: E402


def schema(path):
    with np.load(path) as z:
        return {k: (str(z[k].dtype), list(z[k].shape[1:])) for k in z.files}


def main():
    new, ref, out = sys.argv[1:4]
    sn, sr = schema(new), schema(ref)
    # dump.<ie>_0.* keys are per event; compare the key templates
    tmpl = lambda s: {('dump.*' + k.split('.', 2)[2]) if k.startswith('dump.') else k: v for k, v in s.items()}  # noqa
    tn, tr = tmpl(sn), tmpl(sr)
    res = dict(new=new, ref=ref, n_keys_new=len(sn), n_keys_ref=len(sr),
               keys_only_new=sorted(set(tn) - set(tr)), keys_only_ref=sorted(set(tr) - set(tn)),
               dtype_or_shape_diff=sorted(k for k in set(tn) & set(tr) if tn[k] != tr[k] and not
                                          (tn[k][0][:2] == tr[k][0][:2] == '<U' and tn[k][1] == tr[k][1])),
               unicode_length_only_diff={k: [tn[k][0], tr[k][0]] for k in set(tn) & set(tr) if tn[k] != tr[k] and
                                         tn[k][0][:2] == tr[k][0][:2] == '<U' and tn[k][1] == tr[k][1]})
    z, job = RP.open_job(new)
    res['job'] = {k: job[k] for k in ('id', 'sample', 'qv2_stream', 'chunk', 'ev0', 'n_events', 'rho', 'roads', 'seed',
                                      'dump_events')}
    res['seed_ok'] = job['seed'] == RS.hash_seed(f"qv2|{job['qv2_stream']}|{job['chunk']}")
    zr, jr = RP.open_job(ref)
    res['ref_seed_ok'] = jr['seed'] == RS.hash_seed(f"qv2|{jr['qv2_stream']}|{jr['chunk']}")
    for tag, f in (('new', new), ('ref', ref)):
        g, p, d = DJ.job_counts(Path(f))
        res[f'direct_{tag}'] = dict(n_trials=int(len(g)), n_events=int(len(np.unique(d['trials.ev']))),
                                    grp_R04_R07_sum=[int(x) for x in g[:, :4].sum(0)], identity_checks='passed')
    tev, tpv, tph, trd = z['trials.ev'], z['trials.pv'], z['trials.phimet'], z['trials.road']
    rp = {}
    for ie in (0, job['n_events'] - 1):
        r = RP.replay(z, job, ie)
        t = np.where(tev == job['ev0'] + ie)[0]
        rp[str(ie)] = bool(len(t) > 0 and np.array_equal(tpv[t], np.repeat(r['pv'][None, :], len(t), 0)) and
                           np.allclose(tph[t], r['phimets'][trd[t]], rtol=0, atol=1e-12))
    res['replay_pv_phimet_equal'] = rp
    res['ok'] = (not res['keys_only_new'] and not res['keys_only_ref'] and not res['dtype_or_shape_diff'] and
                 res['seed_ok'] and res['ref_seed_ok'] and all(rp.values()) and job['qv2_stream'] == 'dev.pu1')
    Path(out).write_text(json.dumps(res, indent=1, default=str) + '\n')
    print(json.dumps(res, indent=1, default=str))


if __name__ == '__main__':
    main()
