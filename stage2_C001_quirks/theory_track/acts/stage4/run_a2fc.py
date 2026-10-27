"""run_a2fc.py -- campaign A2FC (2026-10-16): the V4-6 revert rule (plan l.1254-1255, l.1813) applied to A2.

NEW driver file; it changes NO frozen production file.  The A2 points listed in investigation/V46_REVERT_SET.json
(V4-6 > 5 % from the production A1 full chain) are re-produced through the full chain with PU, i.e. the frozen 'a5'
job kind of run_g1b.run_signal_job (run_chain.py sig: quirk SimHits through ACTS digitisation + CKF, PU 200 with the
per-row seeds hseed('sigpu', spin, m, row), same top-up / PV / MET / trial seeds as A2, T_seed = 4).

Pairing with A2: one A2FC job per (revert point, A2 job): rows = the A2 job's rows in the same order (same ACTS event
numbers), chain seed = the A2 job seed (same ACTS RandomNumbers seed -> same Fatras simulation of the same Pythia PU
events).  Only the quirk-hit path differs (ACTS digitisation + CKF instead of numpy smearing appended after CKF).

The jobs go to jobs/A2FC.json and run through the unchanged run_stage4.cmd_run / cmd_check (campaign name passed
programmatically; run_stage4's argparse choices are not touched).  Outputs: data/acts_stage4/prod/A2FC/.

  pixi run python -m acts.stage4.run_a2fc manifest
  pixi run python -m acts.stage4.run_a2fc run [--workers 7 --mem-gb 19]
  pixi run python -m acts.stage4.run_a2fc check
"""
import argparse
import json
import sys
import time

from acts.stage4 import run_stage4 as RS
from acts.stage4 import run_g1b as RG

CAMP = 'A2FC'
REVERT = RS.HERE / 'investigation' / 'V46_REVERT_SET.json'


def make_manifest():
    S = RG.s4sig()
    rv = json.loads(REVERT.read_text())
    a2 = [j for j in json.loads((RS.JOBS / 'C1.json').read_text())['jobs'] if j['sample'] == 'A2']
    jobs = []
    for p in rv['revert_set']:
        spin, m, lam = p['spin'], int(p['m']), float(p['lam'])
        key = S.point_key(spin, m, lam)
        assert key == p['point'], (key, p['point'])
        src = sorted((j for j in a2 if j['spin'] == spin and int(j['m']) == m), key=lambda j: j['chunk'])
        assert src and all(lam in j['lams'] for j in src)
        for j in src:
            n = len(j['rows'])
            jobs.append(dict(id=f"A2FC_{spin}{m}_L{lam:g}_{j['chunk']:03d}", campaign=CAMP, sample='A2FC', kind='a5',
                             point=key, rows=list(j['rows']), chunk=j['chunk'], n_events=n, roads=1, rho=1,
                             seed=j['seed'], dump_events=n,
                             est_s=RG.COST['job_overhead'] + n * RG.COST['a5_ev'], mem_gb=1.5, order=1,
                             out=f"{CAMP}/A2FC_{spin}{m}_L{lam:g}_{j['chunk']:03d}.npz", requires='G1b',
                             paired_a2_id=j['id'], paired_a2_out=j['out'], lam=lam))
    d = dict(campaign=CAMP, runner=RS.RUNNER_VERSION, created=time.strftime('%Y-%m-%d %H:%M'), jobs=jobs,
             revert_set_file='acts/stage4/investigation/V46_REVERT_SET.json',
             note='V4-6 revert (plan l.1254-1255/l.1813): A2 points with V4-6 > 5 % through the full chain with PU '
                  '(a5 kind); rows/order/chain seed = the paired A2 job (paired_a2_id)')
    (RS.JOBS / f'{CAMP}.json').write_text(json.dumps(d, indent=1))
    print(f'{CAMP}: {len(jobs)} jobs, {sum(j["n_events"] for j in jobs)} events, est '
          f'{sum(j["est_s"] for j in jobs) / 3600:.1f} CPU-h')
    return d


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['manifest', 'run', 'check', 'status'])
    ap.add_argument('--workers', type=int, default=7)
    ap.add_argument('--mem-gb', type=float, default=19.0)
    ap.add_argument('--max-jobs', type=int, default=0)
    ap.add_argument('--nice', type=int, default=10)
    ap.add_argument('--deep', action='store_true')
    a = ap.parse_args(argv)
    if a.cmd == 'manifest':
        make_manifest()
        return 0
    if not (RS.JOBS / f'{CAMP}.json').exists():
        make_manifest()
    ns = argparse.Namespace(campaign=CAMP, workers=a.workers, mem_gb=a.mem_gb, max_jobs=a.max_jobs, nice=a.nice,
                            deep=a.deep, allow_interim=False)
    return dict(run=RS.cmd_run, check=RS.cmd_check, status=RS.cmd_status)[a.cmd](ns)


if __name__ == '__main__':
    sys.exit(main())
