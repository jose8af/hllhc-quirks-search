"""val_probe_rerun.py -- B7 reproducibility check of the cross-section probes (fixer S2-R1, 2026-10-11): t3/t4/t16 rerun with
every EW input set explicitly in the scripts (probes/*_rerun.mg, t3_E_incl.mg) vs the original 2026-10-11 logs.
t16 has fixed seeds (expect identical numbers); t3/t4 had automatic seeds (expect agreement within MC error).
Run: pixi run -e ana python scripts/val_probe_rerun.py  ->  results/probe_rerun.json"""
import json
import os

from val_xsec import parse, first_xs, SIM

rows = {}
for tag, a, b in (('t16', 't16_lo_grid.log', 't16_lo_grid_rerun.log'), ('t4', 't4_xsec.log', 't4_xsec_rerun.log')):
    o = {n: (v, e) for n, v, e in parse(a)}
    r = {n.replace('rerun_', ''): (v, e) for n, v, e in parse(b)}
    for k in o:
        rows[f'{tag}_{k}'] = dict(original_fb=o[k][0], rerun_fb=r[k][0], rel=r[k][0] / o[k][0] - 1, mc_rel_err=o[k][1] / o[k][0])
a, b = first_xs('t3_E_incl.log'), first_xs('t3_E_incl_rerun.log')
rows['t3_E_m500'] = dict(original_fb=a[0], rerun_fb=b[0], rel=b[0] / a[0] - 1, mc_rel_err=a[1] / a[0])
json.dump(rows, open(os.path.join(SIM, 'results', 'probe_rerun.json'), 'w'), indent=1)
for k, v in rows.items():
    print(f"{k}: {v['original_fb']:.5g} -> {v['rerun_fb']:.5g} ({100 * v['rel']:+.2f} %, MC {100 * v['mc_rel_err']:.2f} %)")
