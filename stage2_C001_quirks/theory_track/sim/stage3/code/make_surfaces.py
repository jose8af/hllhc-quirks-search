"""make_surfaces.py -- Stage 3 (E7): build the recording-surface table and the endcap-disc material table for the
Stage-3 kernel (T3_causal_s3.py) from the `simplified` block of acts/geometry/cms_phase2_public.json (D1 option (a),
approved 2026-10-11) and write them to surfaces_s3.json next to this file (the bundle ships the JSON, not the builder).

Surfaces (kernel units: cm):
  type 0 = cylinder (R, zmin, zmax); type 1 = disc (z, rmin, rmax).  Every root of a chord is recorded.
  kind  IT  : TBPX L1-4 cylinders, TFPX D1-8 and TEPX D1-4 discs (both sides)            -- single sensor
        PS  : TBPS L1-3 cylinders and the PS part of TEDD D1-5 (r < ps_2s_boundary)       -- two sensors at +-s/2
        2S  : TB2S L1-3 cylinders and the 2S part of TEDD D1-5                            -- two sensors at +-s/2
        BTL : cylinder r = 114.8 cm, |z| < 260 cm (inner boundary of the BTL envelope, MTD TDR §2)
        ETL : proxy disc |z| = 292 cm, r 29.2-118.5 cm (|eta| < 3 inner edge; exact z UNVERIFIED, plan §4.2)
        T3V : VIRTUAL copies of the 10 T3 barrel radii (REC_RADII[:10], |z| < REC_ZMAX), used only for the Stage-1
              plane-thickness definition ds_barrel (P1 compares with Stage 1 on exactly these layers).  Not detector
              surfaces: Stage 4 must ignore kind T3V.
  Stacked OT sensor spacing s: barrel TBPS L1 2.6 mm, L2 1.6 mm, L3 1.6 mm (smallest listed spacing of the layer:
  UNVERIFIED simplification -- tilted rings carry 2.6/4.0 mm), TB2S 1.8 mm; TEDD PS rings 4.0 mm, 2S rings 1.8 mm.
  Discs are flat at z_nominal (the ring z staggering of +-1.5 cm is not modelled; same approximation as the JSON block).
Disc material (D4, approved): TFPX/TEPX slabs x/X0 = 0.012, width 1.0 cm in z (= the T3 TBPX barrel slab), TEDD
  PS part 0.025 / 2S part 0.018, width 2.0 cm (= the T3 PS / 2S barrel slabs).  UNVERIFIED, inside the x0.5-x2 band.
Run (from theory_track/): pixi run python sim/stage3/code/make_surfaces.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TT = HERE.parents[2]
SRC = TT / 'acts' / 'geometry' / 'cms_phase2_public.json'

T3_RADII = [3.0, 6.1, 10.4, 14.6, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3]
T3_ZMAX = [20.0] * 4 + [120.0] * 6
BARREL_SPACING_MM = {'TBPS_L1': 2.6, 'TBPS_L2': 1.6, 'TBPS_L3': 1.6, 'TB2S_L1': 1.8, 'TB2S_L2': 1.8, 'TB2S_L3': 1.8}
SENSOR_T_CM = {'IT': 0.015, 'PS': 0.020, '2S': 0.020, 'BTL': 0.0, 'ETL': 0.0, 'T3V': 0.0}   # active Si thickness


def build():
    g = json.load(open(SRC))
    s = g['simplified']
    surf = []      # dict(name, type, p0, p1, p2, kind)

    def cyl(name, R, hz, kind):
        surf.append(dict(name=name, type=0, p0=R, p1=-hz, p2=hz, kind=kind, t_sens=SENSOR_T_CM[kind]))

    def disc(name, z, rmin, rmax, kind):
        surf.append(dict(name=name, type=1, p0=z, p1=rmin, p2=rmax, kind=kind, t_sens=SENSOR_T_CM[kind]))

    for c in s['cylinders']:
        R = c['r_mm'] / 10; hz = c['half_z_mm'] / 10; kind = {'IT_1x2': 'IT', 'IT_2x2': 'IT'}.get(c['module_type'], c['module_type'])
        if kind == 'IT':
            cyl(c['name'], R, hz, 'IT')
        else:
            sp = BARREL_SPACING_MM[c['name']] / 10
            cyl(c['name'] + '_in', R - sp / 2, hz, kind)
            cyl(c['name'] + '_out', R + sp / 2, hz, kind)
    dmat = []
    for side, sg in (('p', 1.0), ('n', -1.0)):
        for d in s['discs']:
            z = sg * d['z_mm'] / 10; rmin = d['r_min_mm'] / 10; rmax = d['r_max_mm'] / 10
            nm = f"{d['name']}_{side}"
            if d['name'].startswith(('TFPX', 'TEPX')):
                disc(nm, z, rmin, rmax, 'IT')
            else:
                rb = d['ps_2s_boundary_mm'] / 10
                for part, r0, r1, sp in (('PS', rmin, rb, 0.40), ('2S', rb, rmax, 0.18)):
                    disc(f'{nm}_{part}_in', z - sg * sp / 2, r0, r1, part)
                    disc(f'{nm}_{part}_out', z + sg * sp / 2, r0, r1, part)
    for d in s['discs']:
        zc = d['z_mm'] / 10; rmin = d['r_min_mm'] / 10; rmax = d['r_max_mm'] / 10
        if d['name'].startswith(('TFPX', 'TEPX')):
            dmat.append(dict(name=d['name'], zc=zc, rmin=rmin, rmax=rmax, xX0=0.012, w=1.0))
        else:
            rb = d['ps_2s_boundary_mm'] / 10
            dmat.append(dict(name=d['name'] + '_PS', zc=zc, rmin=rmin, rmax=rb, xX0=0.025, w=2.0))
            dmat.append(dict(name=d['name'] + '_2S', zc=zc, rmin=rb, rmax=rmax, xX0=0.018, w=2.0))
    cyl('BTL', 114.8, 260.0, 'BTL')
    disc('ETL_p', 292.0, 29.2, 118.5, 'ETL')
    disc('ETL_n', -292.0, 29.2, 118.5, 'ETL')
    for i, (R, zm) in enumerate(zip(T3_RADII, T3_ZMAX)):
        cyl(f'T3V_{i}', R, zm, 'T3V')
    return dict(source=str(SRC.relative_to(TT)), note=__doc__.split('Run (from')[0], units='cm', surfaces=surf,
                disc_material=dmat, sensor_thickness_cm=SENSOR_T_CM)


if __name__ == '__main__':
    out = build()
    p = HERE / 'surfaces_s3.json'
    json.dump(out, open(p, 'w'), indent=1)
    from collections import Counter
    print(len(out['surfaces']), 'surfaces', Counter(x['kind'] for x in out['surfaces']), len(out['disc_material']), 'disc slabs ->', p)
