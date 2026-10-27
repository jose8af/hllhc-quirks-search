"""R1 constructive check 1: Lambda exponents, measured vs -2+2c_ev vs full MG model (P1.json)."""
import json
d = json.load(open('sim/stage3/results/P1.json'))
print(f"{'point':8s} {'interval':10s} {'ev_slope':>9s} {'err':>6s} {'-2+2c':>7s} {'pull':>6s} | {'pop':>7s} {'perr':>6s} {'MGmodel':>8s} {'d/perr':>6s}")
for pt, v in d['points'].items():
    for iv, e in v['exponents'].items():
        if e.get('median_event_slope') is None: continue
        mp = e.get('pred_MG_model_population')
        ps, pe = e.get('population_slope'), e.get('population_err')
        dd = (ps - mp)/pe if (mp is not None and ps is not None and pe) else float('nan')
        print(f"{pt:8s} {iv:10s} {e['median_event_slope']:9.3f} {e['err']:6.3f} {e['pred_MG_event_median']:7.3f} {e['pull_MG']:6.1f} | {ps if ps is not None else float('nan'):7.3f} {pe if pe else float('nan'):6.3f} {mp if mp is not None else float('nan'):8.3f} {dd:6.1f}")
