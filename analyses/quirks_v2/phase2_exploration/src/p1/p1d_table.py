"""p1d_table.py -- P1-d (COM P1-d, STR §4.15 'Validity window'): the validity-window table from the TRACKED v1 result
stage2_C001_quirks/theory_track/sim/stage3/results/P1.json (key 'v2b_revisit.cells': one cell per (point, Lambda) with the
population difference Dc = median(c2) - median(c_ev), its bootstrap sigma, the relative difference, the k_B < 6
sub-population and v1's pass flag at 1.5 %), plus the per-(point, Lambda) k_B-split rows of 'points.*.by_lambda.*.c'.
No new computation: the numbers are v1's (tag UNVERIFIED-transcribed by program, as in P1.json meta); the script only
tabulates them so that the paper's P1 text can follow a table.
Run (light, stdlib): python3 -I p1d_table.py -> ../../outputs/p1/p1d_table.json and a Markdown table on stdout (log)
"""
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('p1d')
SRC = Path('/home/users/jdochoa/hllhc-quirks-search/stage2_C001_quirks/theory_track/sim/stage3/results/P1.json')
OUT = Path(__file__).resolve().parents[2] / 'outputs' / 'p1'


def main():
    d = json.load(open(SRC))
    cells = d['v2b_revisit']['cells']
    rows = []
    for c in cells:
        bl = d['points'][c['point']]['by_lambda'].get(f"L{c['lam']:g}", {}).get('c', {})
        rows.append(dict(point=c['point'], lam_keV=c['lam'], Dc=c['Dc'], sigma=c['sig'], rel=c['rel'],
                         frac_kB_ge6=c.get('frac_kB6'), Dc_kB_lt6=c.get('Dc_lt6'), rel_kB_lt6=c.get('rel_lt6'),
                         paired_median_r=c.get('paired'), paired_err=c.get('paired_err'), pass_1p5=c.get('pass_1p5'),
                         kB_lt6=bl.get('kB_lt6'), kB_ge6=bl.get('kB_ge6')))
    n_pass = sum(1 for r in rows if r['pass_1p5'])
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(dict(source=str(SRC), n_cells=len(rows), n_pass_1p5=n_pass, rows=rows,
                   tag='v1 numbers tabulated (UNVERIFIED as transcribed; P1.json meta)'), open(OUT / 'p1d_table.json', 'w'),
              indent=1)
    log.info('cells %d, pass (v1 1.5 %% rule) %d', len(rows), n_pass)
    log.info('| point | Λ [keV] | Dc | σ | rel | k_B≥6 frac | Dc (k_B<6) | paired median r | v1 pass |')
    log.info('|---|---|---|---|---|---|---|---|---|')
    for r in rows:
        log.info('| %s | %g | %+.4f | %.4f | %+.3f | %s | %s | %s | %s |', r['point'], r['lam_keV'], r['Dc'], r['sigma'], r['rel'],
                 r['frac_kB_ge6'], f"{r['Dc_kB_lt6']:+.4f}" if r['Dc_kB_lt6'] is not None else '—',
                 f"{r['paired_median_r']:+.4f} ± {r['paired_err']:.4f}" if r['paired_median_r'] is not None else '—',
                 r['pass_1p5'])


if __name__ == '__main__':
    main()
