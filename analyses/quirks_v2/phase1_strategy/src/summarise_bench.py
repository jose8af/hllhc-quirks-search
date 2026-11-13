"""summarise_bench.py -- feasibility A (Anselm): bench_logs/*.jsonl -> outputs/feasibility/benchmarks_chain.json.

Groups the /usr/bin/time -v records of bench_run.py by (label, conc), keeps successful runs (returncode 0) and reports
N, mean and sample standard deviation of CPU (user+sys), wall, max RSS and the per-unit values; cold runs (the first
run of an environment on a node, flagged with note 'cold') are kept separate. Stage-3 per-event kernel CPU
(bench_logs/s3_events.jsonl) and the Stage-4 bench lines (BENCH_S4 in the output tail) are summarised as well.
Run: python3 -I phase1_strategy/src/summarise_bench.py
"""
import json
import statistics as st
from collections import defaultdict
from pathlib import Path

QV2 = Path(__file__).resolve().parents[2]
FEAS = QV2 / 'phase1_strategy' / 'outputs' / 'feasibility'
LOGS = FEAS / 'bench_logs'


def ms(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None
    return dict(n=len(xs), mean=st.fmean(xs), sd=(st.stdev(xs) if len(xs) > 1 else 0.0), min=min(xs), max=max(xs))


def main():
    groups = defaultdict(list)
    for f in sorted(LOGS.glob('*.jsonl')):
        if f.name == 's3_events.jsonl':
            continue
        for line in f.read_text().splitlines():
            r = json.loads(line)
            key = (r['label'], r['conc'], 'cold' if 'cold' in r.get('note', '') else 'warm')
            groups[key].append(r)
    out = dict(description=__doc__.strip().splitlines()[0], host_cpu='Intel i5-7500 (maxwell)', units=dict(
        cpu_s='user+sys seconds', wall_s='seconds', max_rss_mb='MiB (max RSS of the largest process in the tree)'),
        groups=[])
    for (label, conc, cold), rs in sorted(groups.items()):
        ok = [r for r in rs if r['returncode'] == 0]
        g = dict(label=label, conc=conc, start=cold, n_runs=len(rs), n_ok=len(ok), unit_name=ok[0]['unit_name'] if ok else None,
                 units=ok[0]['units'] if ok else None, cpu_s=ms([r.get('cpu_s') for r in ok]),
                 wall_s=ms([r.get('wall_s') for r in ok]), max_rss_mb=ms([r['max_rss_kb'] / 1024 for r in ok if r.get('max_rss_kb')]),
                 cpu_s_per_unit=ms([r.get('cpu_s_per_unit') for r in ok]), wall_s_per_unit=ms([r.get('wall_s_per_unit') for r in ok]),
                 hosts=sorted({r['host'] for r in rs}), log=f'bench_logs/{label}.jsonl')
        s4 = []
        for r in ok:
            for line in r.get('out_tail', []):
                if line.startswith('BENCH_S4 '):
                    s4.append(json.loads(line[9:]))
        if s4:
            n = s4[0]['n_events']
            g['s4'] = dict(chain_s_per_event=ms([x['t_chain_s'] / n for x in s4]),
                           tt_side_s_per_trial=ms([x['finder_s_per_trial'] for x in s4]),
                           bytes_per_event=ms([x['bytes'] / n for x in s4]), n_trials=s4[0]['n_trials'],
                           chain_stage_s_per_event={k: ms([x['chain_stage_s'][k] / n for x in s4 if x.get('chain_stage_s')])
                                                    for k in (s4[0].get('chain_stage_s') or {})})
        out['groups'].append(g)
    ev = defaultdict(list)
    p = LOGS / 's3_events.jsonl'
    if p.exists():
        for line in p.read_text().splitlines():
            r = json.loads(line)
            ev[(r['m'], r['lam'], r['conc'])].append(r)
    out['stage3_kernel'] = []
    for (m, lam, conc), rs in sorted(ev.items()):
        per_rep = [sum(r['cpu_ev']) / r['n'] for r in rs]
        out['stage3_kernel'].append(dict(m=m, lam=lam, conc=conc, n_reps=len(rs), n_events=rs[0]['n'],
                                         cpu_s_per_event_rep=ms(per_rep), bytes_per_event=ms([r['bytes'] / r['n'] for r in rs]),
                                         hits_per_event=rs[0]['n_hits'] / rs[0]['n'], status=rs[0]['status']))
    (FEAS / 'benchmarks_chain.json').write_text(json.dumps(out, indent=1) + '\n')
    for g in out['groups']:
        c, w, r = g['cpu_s'], g['wall_s'], g['max_rss_mb']
        if c:
            print(f"{g['label']:28s} conc {g['conc']} {g['start']}: N {c['n']} cpu {c['mean']:.1f}±{c['sd']:.1f} s, "
                  f"wall {w['mean']:.1f}±{w['sd']:.1f} s, rss {r['mean']:.0f}±{r['sd']:.0f} MB"
                  + (f", per {g['unit_name']} {g['cpu_s_per_unit']['mean']:.3g} s" if g['cpu_s_per_unit'] else ''))
    for k in out['stage3_kernel']:
        print(f"S3 kernel m{k['m']} L{k['lam']} conc {k['conc']}: {k['cpu_s_per_event_rep']['mean']:.3g}±"
              f"{k['cpu_s_per_event_rep']['sd']:.2g} s/ev (N reps {k['n_reps']}, {k['n_events']} ev), {k['bytes_per_event']['mean']:.0f} B/ev")


if __name__ == '__main__':
    main()
