"""G1b hash-addendum regression (HASH_ADDENDUM.md): one small PU-only, SM and dens job through run_stage4.run_pu_job with
the FROZEN config, before and after the additive run_stage4.py change; every data array must be bit-identical.

  PYTHONPATH=. pixi run python -m acts.stage4.validation.g1b_regress run before|after|before2 [runner module [chain script]]
  PYTHONPATH=. pixi run python -m acts.stage4.validation.g1b_regress compare before after
Outputs: data/acts_stage4/prod/_regress/<tag>/...; compare -> data/acts_stage4/g1b/regress_<a>_vs_<b>.json
Arrays compared: every npz key except meta_json (timestamps, wall times, code hashes) and the wall-clock timers
chain.timing, trials.times, trials.t_total.
"""
import json
import sys

import numpy as np

from acts.stage4 import run_stage4 as RS

SKIP = {'meta_json', 'chain.timing', 'trials.times', 'trials.t_total'}    # wall-clock timers only


def jobs(tag):
    base = f'_regress/{tag}'
    pu = dict(id='RGB1_00000', campaign='C1', sample='RGB1', kind='pu', chunk=0, ev0=0, n_events=1, roads=2, rho=1,
              seed=RS.hash_seed('stage4|RGB1|0'), dump_events=1, est_s=30.0, mem_gb=1.5, order=0,
              out=f'{base}/RGB1/RGB1_00000.npz', requires='pu-chain')
    sm = dict(id='RGC_Znunu_j_00000', campaign='C1', sample='RGC_Znunu_j', sm_sample='Znunu_j', kind='sm', chunk=0,
              ev0=0, n_events=1, roads=1, rho=1, seed=RS.hash_seed('stage4|RGC_Znunu_j|0'), dump_events=0, est_s=20.0,
              mem_gb=1.5, order=1, out=f'{base}/RGC/RGC_Znunu_j_00000.npz', requires='G1')
    dens = dict(id='DENSlow_00000', campaign='C1', sample='DENSlow', kind='dens', topup='low', src_id='RGB1_00000',
                src_out=pu['out'], chunk=0, ev0=0, n_events=1, roads=2, rho=1, seed=pu['seed'], dump_events=0,
                est_s=20.0, mem_gb=1.5, order=2, needs=pu['out'], out=f'{base}/DENSlow/DENSlow_00000.npz', requires='G1')
    return [pu, sm, dens]


def run(tag, module='acts.stage4.run_stage4', chain=None):
    import importlib
    from pathlib import Path
    M = importlib.import_module(module)        # 'after' before the hook is applied: the patched candidate copy
    if chain:                                  # ... and the patched candidate chain
        M.CHAIN_PROD = Path(chain).resolve()
    print('runner module', module, M.__file__, RS.sha256_file(M.__file__), 'chain', M.CHAIN_PROD,
          RS.sha256_file(M.CHAIN_PROD), flush=True)
    for j in jobs(tag):
        r = M.run_pu_job(j, False)
        print(json.dumps(r, default=str), flush=True)


def compare(a, b):
    out = {}
    ok_all = True
    for ja, jb in zip(jobs(a), jobs(b)):
        za = np.load(RS.out_path(ja)); zb = np.load(RS.out_path(jb))
        ka = set(za.files) - SKIP; kb = set(zb.files) - SKIP
        diff = []
        for k in sorted(ka | kb):
            if k not in za.files or k not in zb.files:
                diff.append(k + ' (missing)')
                continue
            x = za[k]; y = zb[k]
            if x.dtype != y.dtype or x.shape != y.shape or x.tobytes() != y.tobytes():
                diff.append(k)
        ma = json.loads(str(za['meta_json'])); mb = json.loads(str(zb['meta_json']))
        out[ja['kind']] = dict(n_keys=len(ka), n_diff=len(diff), diff=diff[:30],
                               run_stage4_sha_a=ma['code_sha256']['acts/stage4/run_stage4.py'],
                               run_stage4_sha_b=mb['code_sha256']['acts/stage4/run_stage4.py'],
                               n_trials=int(za['n_trials']))
        ok_all &= not diff
    out['bit_identical'] = bool(ok_all)
    p = RS.TT / 'data' / 'acts_stage4' / 'g1b' / f'regress_{a}_vs_{b}.json'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0 if ok_all else 1


if __name__ == '__main__':
    if sys.argv[1] == 'run':
        run(sys.argv[2], *sys.argv[3:5])
    else:
        sys.exit(compare(sys.argv[2], sys.argv[3]))
