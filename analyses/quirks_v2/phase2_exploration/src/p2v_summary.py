"""p2v_summary.py -- table of the T1 toy-cost runs (p2-c-toy-*) and the projection of the toy programme (light; einstein).

  python3 -I p2v_summary.py <out.json> <campaign> [<campaign> ...]

Reads data/p2c/<campaign>/000/*.json only for jobs with a `done` marker.  For each job: parameters, config, CPU s per
1000 + 1000 toys (with its statistical error), fits per toy and function evaluations, failures, CLs.  Paired check:
for jobs with the same (size, mu, toy seed) as a baseline job (numpy + scipy, std), the per-toy q differences.

Toy programme (STR §4.11 pt 5, l.1715-1719 and pt 6 l.1733): units of 1000 s+b + 1000 b toys at one mu:
pass 1 5 x 11 x 8 = 440, its exact check 5 x 3 x 8 = 120, pass 2 3 x 11 x 8 = 264, its check 3 x 3 x 8 = 72,
T1-c (iii) 20 CPU-h at 652 s per unit = 110.4 units; total 1006.4 units = 182.3 CPU-h at 652 s (STR: 183).
Conditional draw (all-exact toys, l.1719): 236 CPU-h at 652 s = 1303 units.
"""
import json
import os
import sys
from pathlib import Path

QV2 = Path(__file__).resolve().parents[2]
UNITS = dict(pass1=5 * 11 * 8, pass1_check=5 * 3 * 8, pass2=3 * 11 * 8, pass2_check=3 * 3 * 8, t1c_iii=20 * 3600 / 652)
COND_UNITS = 236 * 3600 / 652


def done_jobs(camp):
    out = {}
    for mk in sorted((QV2 / 'ledger' / 'markers' / camp).glob('0*/*.marker')):
        last = None
        for line in mk.read_text().splitlines():
            if line.strip():
                last = json.loads(line)
        if last and last.get('status') == 'done':
            for o in last.get('outputs', []):
                out[last['job_id']] = dict(path=o['path'], cpu_s_marker=last.get('cpu_s'))
    return out


def main(argv):
    out = argv[0]
    rows = []
    for camp in argv[1:]:
        for jid, m in done_jobs(camp).items():
            d = json.loads(Path(m['path']).read_text())
            r = dict(job=jid, n_par=d['n_par'], mu=d['mu_test'], toy_seed=d.get('toy_seed', d['seed'] + 1),
                     n_toys=d['n_toys'], config={k: v for k, v in d['config'].items() if v not in (None, 0, 0.0, '0')},
                     cpu_1000=d['cpu_s_per_1000_sb_plus_1000_b'], cpu_1000_err=d.get('cpu_s_per_1000_plus_1000_stat_err'),
                     cpu_s_marker=m['cpu_s_marker'], warmup_cpu_s=d.get('warmup_cpu_s'),
                     dropped=d['sb']['dropped'] + d['b']['dropped'], retried=d['sb']['retried'] + d['b']['retried'],
                     fit_fail=d['sb']['fits'].get('n_fit_fail', 0) + d['b']['fits'].get('n_fit_fail', 0),
                     nfev_mean=[d[k]['fits'].get('nfev', {}).get('mean') for k in ('sb', 'b')],
                     nit_mean=[d[k]['fits'].get('nit', {}).get('mean') for k in ('sb', 'b')],
                     cls=d.get('cls'), q={k: d[k]['q'] for k in ('sb', 'b')})
            rows.append(r)
    base = {(r['n_par'], r['mu'], r['toy_seed']): r for r in rows
            if r['config'].get('backend') == 'numpy' and r['config'].get('opt') == 'scipy'
            and r['config'].get('layout') == 'std' and r['config'].get('start') == 'std' and len(r['config']) == 4}
    for r in rows:
        b = base.get((r['n_par'], r['mu'], r['toy_seed']))
        if b is None or b is r:
            continue
        dq = []; nq = 0
        for k in ('sb', 'b'):
            for x, y in zip(r['q'][k], b['q'][k]):
                if x is not None and y is not None:
                    dq.append(abs(x - y)); nq += 1
        dq = sorted(dq)
        r['paired'] = dict(baseline=b['job'], n=nq, max_abs_dq=dq[-1] if dq else None,
                           n_dq_gt_1e3=sum(x > 1e-3 for x in dq), n_dq_gt_1e2=sum(x > 1e-2 for x in dq),
                           n_dq_gt_0p1=sum(x > 0.1 for x in dq), speedup=b['cpu_1000'] / r['cpu_1000'])
    for r in rows:
        r.pop('q')
        tot = sum(UNITS.values())
        r['programme_cpu_h'] = tot * r['cpu_1000'] / 3600
        r['conditional_all_exact_cpu_h'] = COND_UNITS * r['cpu_1000'] / 3600
    res = dict(units=UNITS, units_total=sum(UNITS.values()), conditional_units=COND_UNITS, rows=rows)
    with open(out + '.tmp', 'w') as f:
        json.dump(res, f, indent=1)
    os.replace(out + '.tmp', out)
    for r in rows:
        p = r.get('paired', {})
        sys.stdout.write(f"{r['job']:42s} n{r['n_par']:3d} mu{r['mu']:5.1f} {r['cpu_1000']:9.0f}±{r['cpu_1000_err'] or 0:6.0f} s "
                         f"prog {r['programme_cpu_h']:8.1f} h fail {r['fit_fail']} drop {r['dropped']} "
                         f"nfev {r['nfev_mean']} cls {None if not r['cls'] else (round(r['cls']['cls'], 4), round(r['cls']['cls_err'], 4))} "
                         f"pair {p.get('n')} maxdq {p.get('max_abs_dq')} >0.01:{p.get('n_dq_gt_1e2')} x{p.get('speedup') and round(p['speedup'], 1)}\n")


if __name__ == '__main__':
    main(sys.argv[1:])
