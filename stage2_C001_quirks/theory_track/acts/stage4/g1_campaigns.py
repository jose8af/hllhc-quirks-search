"""G1: campaign CPU-h and Mac wall by the plan formula (probes/f4r_deadline.py blocks = f3r blocks + C' in C1, read-only),
re-evaluated with the G1-measured per-event chain cost (PU_S) and the finder times at the freeze-candidate road
(delta95 = 0.15).  Arithmetic only.  Run (theory_track): pixi run python -m acts.stage4.g1_campaigns
-> data/acts_stage4/g1/g1_campaigns.json
"""
import json
from pathlib import Path

TT = Path(__file__).resolve().parents[2]
SRC = (TT / 'acts' / 'stage4' / 'probes' / 'f4r_deadline.py').read_text()
OUT = TT / 'data' / 'acts_stage4' / 'g1'


def load_ns(pu):
    ns = {'__file__': str(TT / 'acts' / 'stage4' / 'probes' / 'f4r_deadline.py')}
    exec(SRC[:SRC.index('res = {')], ns)
    ns['PU'] = pu
    ns['ns']['PU'] = pu
    return ns


def bench(tag):
    p = OUT / 'bench' / tag / 'summary.json'
    return json.loads(p.read_text()) if p.exists() else None


def main():
    single = json.loads((OUT / 'timing' / 'pu_single_24.log').read_text())
    pu_single = sum(single['mean_s_per_event'].values())
    b1 = bench('rho1f'); b2 = bench('rho2f')
    scen = {
        'plan_convention(1 thread chain; t1,t2 at 4/2 parallel workers, road 0.15)':
            dict(PU=pu_single, t1=b1['trial_s']['mean'], t2=b2['trial_s']['mean'] if b2 else None),
        'loaded(4 parallel workers: chain + finder as measured)':
            dict(PU=b1['chain_s_per_chain_event']['mean'], t1=b1['trial_s']['mean'],
                 t2=b2['trial_s']['mean'] if b2 else None),
    }
    res = dict(inputs={k: v for k, v in scen.items()}, note='CAP = 7 workers x 24 h = 168 CPU-h per Mac day (plan '
               'convention); wall h = CPU-h / 7', campaigns={})
    for name, sc in scen.items():
        ns = load_ns(sc['PU'])
        t1 = sc['t1']; t2 = sc['t2'] if sc['t2'] else 8 * t1
        rows = {}
        for c, drop in (('C1', ()), ('C2', ()), ('C4', ('A3', 'A4')), ('C3', ())):
            bl = ns['blocks'](c, t1, t2)
            cpu = sum(v for k, v in bl.items() if k not in drop)
            rows[c + ("'" if drop else '')] = dict(cpu_h=round(cpu, 1), mac_wall_h_7w=round(cpu / ns['MAC_W'], 1),
                                                   blocks={k: round(v, 1) for k, v in bl.items() if k not in drop})
        tot = rows['C1']['cpu_h'] + rows['C2']['cpu_h']
        rows['C1+C2'] = dict(cpu_h=round(tot, 1), mac_wall_h_7w=round(tot / ns['MAC_W'], 1))
        tot3 = tot + rows["C4'"]['cpu_h']
        rows["C1+C2+C4'"] = dict(cpu_h=round(tot3, 1), mac_wall_h_7w=round(tot3 / ns['MAC_W'], 1))
        res['campaigns'][name] = rows
    (OUT / 'g1_campaigns.json').write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
