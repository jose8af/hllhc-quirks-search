"""make_geom.py -- barrel geometry text file for g4sv from the v1 public geometry (read-only TT tree):
radii and half-lengths from TT/acts/geometry/cms_phase2_public.json `simplified.cylinders`, material x/X0 per layer from
`material.T3_slabs_used` (the v1 baseline, UNVERIFIED in v1), plus the beam pipe and the IT service cylinder of that table.
Beam-pipe radius 22 mm: ESTIMATE (not in the JSON).  Usage: python3 -I make_geom.py <TT> <out.txt>
"""
import json
import sys

tt, out = sys.argv[1], sys.argv[2]
d = json.load(open(f'{tt}/acts/geometry/cms_phase2_public.json'))
m = d['material']['T3_slabs_used']
rows = [('beam_pipe', 22.0, 3000.0, m['beam_pipe'])]
for c in d['simplified']['cylinders']:
    x = m['TBPX_each'] if c['name'].startswith('TBPX') else m['PS_layers_each'] if c['name'].startswith('TBPS') else m['two_S_layers_each']
    rows.append((c['name'], c['r_mm'], c['half_z_mm'], x))
rows.append(('IT_service', 190.0, 1200.0, m['IT_service_cylinder_r190']))
rows.sort(key=lambda r: r[1])
with open(out, 'w') as f:
    f.write('# name r_mm half_z_mm x_over_X0  (from cms_phase2_public.json simplified + material.T3_slabs_used)\n')
    for r in rows:
        f.write('%s %.3f %.3f %.4f\n' % r)
print(open(out).read())
