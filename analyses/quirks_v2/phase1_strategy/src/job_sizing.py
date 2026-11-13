"""job_sizing.py -- feasibility A (Anselm): projected per-job sizes from benchmarks_chain.json (stdlib only).

For each stage: per-unit wall at 4 concurrent jobs per node (the production packing) if measured, else the single-job
value x the measured 4-concurrent slowdown of the most similar stage; fixed per-job overhead = mean job wall - units x
per-unit wall at that concurrency.  Events per job = floor((budget - overhead) / per-unit), budget = 1500 s (30 min less
a 5-min safety margin for slow events, cold NFS starts and the marker).  RSS is the measured max RSS (it does not grow
with the event count for these chains: each event is processed and discarded; ESTIMATE, checked only at the sizes run).
Prints a Markdown table and writes outputs/feasibility/job_sizing.json.
Run: python3 -I phase1_strategy/src/job_sizing.py
"""
import json
from pathlib import Path

QV2 = Path(__file__).resolve().parents[2]
FEAS = QV2 / 'phase1_strategy' / 'outputs' / 'feasibility'
BUDGET = 1500.0
RSS_CAP_MIB = 1.6e9 / 2 ** 20      # 1.6 GB per job (brief 5.1)
# output bytes per event of the guns (out.npz of the 20 000-event runs, stat -c %s on maxwell, rep 1):
GUN_BYTES = {'cp_pvpair': 163325828 / 20000, 'gun': 280388290 / 20000}


def main():
    b = json.loads((FEAS / 'benchmarks_chain.json').read_text())
    G = {(g['label'], g['conc'], g['start']): g for g in b['groups']}
    rows = []

    def add(stage, label, conc, per_unit, unit, bytes_per_unit, note=''):
        g = G.get((label, conc, 'warm'))
        if g is None or g['wall_s'] is None:
            return
        n = g['units']
        over = max(g['wall_s']['mean'] - n * per_unit, 0.0)
        k = int((BUDGET - over) // per_unit) if per_unit > 0 else None
        rows.append(dict(stage=stage, label=label, conc=conc, unit=unit, per_unit_wall_s=per_unit, overhead_s=over,
                         units_per_job=k, max_rss_mib=g['max_rss_mb']['max'], bytes_per_unit=bytes_per_unit,
                         bytes_per_job=(k * bytes_per_unit if (k and bytes_per_unit) else None), note=note))

    # Stage 4, PU 200: per event = chain + roads x TT side (from the BENCH_S4 lines)
    for conc in (1, 4):
        g = G.get(('s4pu_n5_roads4_rho1', conc, 'warm'))
        if g and 's4' in g:
            s = g['s4']
            per = s['chain_s_per_event']['mean'] + s['n_trials'] / g['units'] * s['tt_side_s_per_trial']['mean']
            add('Stage 4 PU 200 (B1: chain + 4 finder trials)', 's4pu_n5_roads4_rho1', conc, per, 'PU-200 event',
                s['bytes_per_event']['mean'])
    # Stage 3: per event = job wall / events (kernel-dominated)
    for g in b['groups']:
        if g['label'].startswith('s3_') and g['start'] == 'warm':
            m, lam = g['label'][3:].split('_L')
            ks = [k for k in b['stage3_kernel'] if f"m{k['m']}" == m and f"{k['lam']:g}" == lam and k['conc'] == g['conc']]
            per = ks[0]['cpu_s_per_event_rep']['mean'] if ks else g['wall_s_per_unit']['mean']
            byt = ks[0]['bytes_per_event']['mean'] if ks else None
            add(f'Stage 3 string propagation F {m[1:]} GeV, Lambda {lam} keV', g['label'], g['conc'], per, 'event', byt,
                'toy kinematics; per-event cost varies x5-x10 between events')
    # no-PU guns: startup dominates, so per event = slope between two job sizes (same topology, same concurrency)
    fam = {}
    for g in b['groups']:
        if (g['label'].startswith('cp_') or g['label'].startswith('gun_')) and g['start'] == 'warm' and g['wall_s']:
            base = g['label'].rsplit('_n', 1)[0] if g['label'].startswith('cp_') else 'gun'
            fam.setdefault((base, g['conc']), []).append(g)
    for (base, conc), gs in sorted(fam.items()):
        gs.sort(key=lambda g: g['units'])
        if len(gs) >= 2:
            a, z = gs[0], gs[-1]
            per = (z['wall_s']['mean'] - a['wall_s']['mean']) / (z['units'] - a['units'])
            rss_slope = (z['max_rss_mb']['mean'] - a['max_rss_mb']['mean']) / (z['units'] - a['units'])
            rss0 = a['max_rss_mb']['mean'] - a['units'] * rss_slope
            n_rss = int((RSS_CAP_MIB - rss0) / rss_slope)
            add(f'no-PU single interaction / gun ({base})', z['label'], conc, per, 'event', None,
                'per event from the slope between job sizes %d and %d' % (a['units'], z['units']))
            if rows and rows[-1]['label'] == z['label']:
                r = rows[-1]
                r.update(rss_mib_per_unit=rss_slope, rss0_mib=rss0, units_at_rss_cap=n_rss,
                         units_per_job=min(r['units_per_job'], n_rss), bytes_per_unit=GUN_BYTES.get(base))
                r['bytes_per_job'] = r['units_per_job'] * r['bytes_per_unit'] if r['bytes_per_unit'] else None
    (FEAS / 'job_sizing.json').write_text(json.dumps(dict(budget_s=BUDGET, rows=rows), indent=1) + '\n')
    b['job_sizing'] = dict(budget_s=BUDGET, rss_cap_mib=RSS_CAP_MIB, rows=rows)
    (FEAS / 'benchmarks_chain.json').write_text(json.dumps(b, indent=1) + '\n')
    print('| stage | conc | per unit (wall) | fixed overhead | units per <= 25-min job | max RSS | bytes/unit | bytes/job |')
    print('|---|---|---|---|---|---|---|---|')
    for r in rows:
        bu = f"{r['bytes_per_unit'] / 1e3:.1f} kB" if r['bytes_per_unit'] else '-'
        bj = f"{r['bytes_per_job'] / 1e6:.1f} MB" if r['bytes_per_job'] else '-'
        print(f"| {r['stage']} | {r['conc']} | {r['per_unit_wall_s']:.3g} s | {r['overhead_s']:.0f} s | {r['units_per_job']} | "
              f"{r['max_rss_mib']:.0f} MiB | {bu} | {bj} |")


if __name__ == '__main__':
    main()
