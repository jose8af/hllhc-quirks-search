"""make_geom_g4.py -- Geant4 geometry text file for g4hv, from the same source the ACTS geometry is built from.

  python3 -I make_geom_g4.py <out.txt> [mat_scale]

Source of truth (STR §4.4 pt 1, COM B1-d): `sim/stage3/code/surfaces_s3.json` (the simplified surfaces generated from
the tracked public geometry `acts/geometry/cms_phase2_public.json`), read exactly as `acts/stage4/code/s4geo.py` reads
it: every physical surface of kind IT, PS, 2S, BTL becomes one sensitive surface; a stacked outer-tracker layer's x/X0
is split equally over its two sensors (`s4geo.surface_xX0`); disc x/X0 from `disc_material`; passive Be beam pipe
(r = 22 mm, x/X0 = 0.0023, |z| < 2700 mm) and Si service cylinder (r = 190 mm, x/X0 = 0.010, |z| < 1200 mm) as in
`s4geo.build`.  The numbers are copied here from s4geo.py (BARREL_XX0, the two passive cylinders); `p2c_matscan.py`
checks them against the ACTS geometry actually built.  ETL and the virtual T3V surfaces are skipped, as in ACTS.
"""
import json
import sys
from pathlib import Path

QV2 = Path(__file__).resolve().parents[3]
SURF = QV2 / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json'
BARREL_XX0 = {'IT': 0.012, 'PS': 0.025, '2S': 0.018}        # s4geo.py l.36
B_T = 3.8112                                                  # run_chain.py l.58
PASSIVE = [('BeamPipe', 22.0, -2700.0, 2700.0, 0.0023, 'G4_Be'), ('ITService', 190.0, -1200.0, 1200.0, 0.010, 'G4_Si')]


def surface_xx0(s, dmat, scale=1.0):
    """Copy of s4geo.surface_xX0."""
    k, n = s['kind'], s['name']
    if k in ('BTL', 'ETL', 'T3V'):
        return 0.0
    nsens = 2 if (n.endswith('_in') or n.endswith('_out')) else 1
    if s['type'] == 0:
        x = BARREL_XX0[k]
    else:
        key = n.replace('_p', '').replace('_n', '').replace('_in', '').replace('_out', '')
        x = dmat.get(key, BARREL_XX0[k])
    return scale * x / nsens


def rows(scale=1.0):
    d = json.loads(SURF.read_text())
    dmat = {m['name']: m['xX0'] for m in d['disc_material']}
    out = []
    for s in d['surfaces']:
        if s['kind'] in ('T3V', 'ETL'):
            continue
        x = surface_xx0(s, dmat, scale)
        if s['type'] == 0:
            out.append(('C', s['name'], s['p0'] * 10, s['p1'] * 10, s['p2'] * 10, x, 'G4_Si', 1))
        else:
            out.append(('D', s['name'], s['p0'] * 10, s['p1'] * 10, s['p2'] * 10, x, 'G4_Si', 1))
    for n, r, z0, z1, x, m in PASSIVE:
        out.append(('C', n, r, z0, z1, scale * x, m, 0))
    return out


def main(out, scale=1.0):
    lines = ['# g4hv geometry from surfaces_s3.json (+ passive cylinders of s4geo.py); mat_scale = %g' % scale,
             'B %.4f' % B_T]
    for r in rows(scale):
        lines.append('%s %s %.6f %.6f %.6f %.8f %s %d' % r)
    Path(out).write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 1.0)
