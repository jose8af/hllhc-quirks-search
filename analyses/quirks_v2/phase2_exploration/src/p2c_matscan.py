"""p2c_matscan.py -- B1-d (STR §4.4): Geant4 geometry against the ACTS geometry and material, Fatras physics record.

  <acts python> p2c_matscan.py <out.json> <g4 scan npz of p2c_g4vtx.py scan>

1. Positions: every number given to ACTS (the surfaces JSON and the material JSON that s4geo.build writes for the
   geometry it constructs) against the Geant4 geometry file inside the scan record: radius / z position, z or r
   extents (criterion: equal to 1 um) and x/X0 per surface.
2. Material: Geant4 geantino scan, x/X0 seen along the ray in each slab, against the ACTS slab x/X0 times the
   path factor of the ray (cosh eta for a cylinder, cosh eta / |sinh eta| for a disc); criterion |delta| <= 1 % per layer.
3. Fatras physics actually configured by the chain's addFatras call (defaults of pyacts 48), printed and recorded.
"""
import inspect
import json
import math
import sys
import tempfile
from pathlib import Path

import numpy as np

import p2c_common as C

sys.path.insert(0, str(C.CODE))
import s4geo  # noqa: E402
import acts  # noqa: E402
import acts.examples  # noqa: E402
from acts.examples.simulation import addFatras  # noqa: E402

log = C.setup_logging('p2c_matscan')


def acts_tables(scratch, nphi=32):
    tg, els, sid_of, geo_of, surfs, passive = s4geo.build(nphi=nphi, scratch=scratch)
    tab = {s['sid']: s for s in surfs}
    js = json.loads((Path(scratch) / f's4geo_surfaces_n{nphi}.json').read_text())['det']
    jm = json.loads((Path(scratch) / f's4geo_material_x1_n{nphi}.json').read_text())['Surfaces']['entries']
    mat = {}
    for e in jm:
        key = (e['volume'], e.get('layer', 0), e.get('sensitive', 0))
        slab = e['value']['material']['data'][0][0]
        mat[key] = slab['thickness'] / slab['material'][0]
    out = {}
    # the JSON list is in the order of (surface, sector) used by s4geo.build: recover one entry per surface name
    phys = [s for s in surfs if s['kind'] not in ('T3V', 'ETL')]
    k = 0
    for s in phys:
        ns = nphi if s['kind'] != 'BTL' else 1
        j = js[k]; k += ns
        b = j['bounds']['values']; z0 = j['transform']['translation'][2]
        g = geo_of[(s['sid'], 0)]
        x = mat.get((g.volume, g.layer, g.sensitive), 0.0)
        if j['type'] == 'CylinderSurface':
            out[s['name']] = dict(type='C', a=b[0], b=z0 - b[1], c=z0 + b[1], xx0=x)
        else:
            out[s['name']] = dict(type='D', a=z0, b=b[0], c=b[1], xx0=x)
    for nm, srf in zip(('BeamPipe', 'ITService'), passive):
        g = srf.geometryId
        key = [kk for kk in mat if kk[0] == g.volume and kk[1] == g.layer and kk[2] == 0]
        out[nm] = dict(type='C', a=None, b=None, c=None, xx0=mat[key[0]] if key else None)
    return out, tab


def fatras_record():
    rec = dict(addFatras_signature=str(inspect.signature(addFatras)))
    try:
        cfg = acts.examples.FatrasSimulation.Config()
        rec['FatrasSimulation.Config'] = {k: str(getattr(cfg, k)) for k in dir(cfg) if not k.startswith('_')}
    except Exception as e:  # noqa: BLE001
        rec['FatrasSimulation.Config'] = f'not accessible: {e}'
    rec['acts.fatras_members'] = [k for k in dir(acts.fatras) if not k.startswith('_')]
    rec['acts_version'] = str(getattr(acts, 'version', '48.0.0'))
    return rec


def main(out, scan_file):
    z, meta = C.load_job(scan_file)
    g4 = {}
    for ln in meta['geometry'].splitlines():
        w = ln.split()
        if w and w[0] in ('C', 'D'):
            g4[w[1]] = dict(type=w[0], a=float(w[2]), b=float(w[3]), c=float(w[4]), xx0=float(w[5]), mat=w[6])
    with tempfile.TemporaryDirectory(prefix='p2c_matscan_', dir='.') as scr:
        ac, _ = acts_tables(scr)
    pos = []
    for n, a in ac.items():
        g = g4.get(n)
        if g is None:
            pos.append(dict(name=n, missing_in_g4=True)); continue
        d = dict(name=n, type=a['type'], xx0_acts=a['xx0'], xx0_g4=g['xx0'])
        if a['a'] is not None:
            d.update(d_pos_um=1e3 * abs(a['a'] - g['a']), d_lo_um=1e3 * abs(a['b'] - g['b']), d_hi_um=1e3 * abs(a['c'] - g['c']))
        pos.append(d)
    missing_in_acts = sorted(set(g4) - set(ac))
    # scan: per volume and eta, mean x/X0 along the ray against the ACTS expectation
    S = z['scan']; vols = meta['volumes']
    rows = []
    for vi, vn in enumerate(vols):
        a = ac.get(vn)
        if a is None or not a['xx0']:
            continue
        m = S[:, 1] == vi
        for eta in np.unique(S[m, 0]):
            mm = m & (S[:, 0] == eta)
            f = math.cosh(eta) if g4[vn]['type'] == 'C' else math.cosh(eta) / max(abs(math.sinh(eta)), 1e-9)
            x = float(S[mm, 3].mean())
            rows.append((vn, float(eta), x, a['xx0'] * f, x / (a['xx0'] * f) - 1.0, float(S[mm, 5].mean()), float(S[mm, 6].mean())))
    worst = {}
    for vn, eta, x, xe, d, r, zz in rows:
        if abs(d) > abs(worst.get(vn, (0, 0))[1]):
            worst[vn] = (eta, d)
    res = dict(n_surfaces_acts=len(ac), n_slabs_g4=len(g4), missing_in_acts=missing_in_acts, positions=pos,
               max_position_diff_um=max([max(p.get('d_pos_um', 0), p.get('d_lo_um', 0), p.get('d_hi_um', 0)) for p in pos]),
               max_xx0_table_reldiff=max([abs(p['xx0_g4'] / p['xx0_acts'] - 1) for p in pos
                                          if p.get('xx0_acts') and p.get('xx0_g4') is not None]),
               scan_worst_reldiff_per_volume={k: dict(eta=v[0], reldiff=v[1]) for k, v in worst.items()},
               scan_max_abs_reldiff=max(abs(v[1]) for v in worst.values()) if worst else None,
               scan_rows=len(rows), g4_overlap_messages=meta.get('n_overlap_messages'), fatras=fatras_record(),
               scan_cols=['volume', 'eta', 'x_over_X0_g4', 'x_over_X0_acts_expected', 'reldiff', 'r_mid_mm', 'z_mid_mm'],
               scan=rows, g4_summary=meta['g4'])
    Path(out + '.tmp').write_text(json.dumps(res, indent=1, default=str))
    Path(out + '.tmp').replace(out)
    log.info('positions: max diff %.4f um; table x/X0 max rel diff %.2e; scan max |rel diff| %s; overlaps %s',
             res['max_position_diff_um'], res['max_xx0_table_reldiff'], res['scan_max_abs_reldiff'],
             res['g4_overlap_messages'])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
