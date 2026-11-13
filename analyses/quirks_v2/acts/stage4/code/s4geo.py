"""code/s4geo.py -- Stage-4 PRODUCTION geometry (G1, 2026-10-13), copied from probes/s4geo.py (E9) with three changes:
  (1) the JSON scratch files go to a caller-given directory (default: a fresh per-process temp dir; the probe wrote a
      shared data/acts_stage4/p0/ file, a race between parallel production workers);
  (2) production resolutions RES_PROD (plan §1.5 table: BTL axes corrected, rphi 16 mm along the bar, z 0.9 mm);
  (3) the BTL time smearing is given in ACTS internal units (sigma_t * u.ns; the probe/interim chains wrote 0.035 into
      the digitisation JSON, i.e. 0.035 mm/c = 0.12 ps).
Probe description follows.

ACTS Gen-3 tracking geometry built from the Stage-3 simplified surfaces.

Contract (HANDOVER_STAGE4 §2, user decision U-4 (a)): every physical Stage-3 recording surface (kinds IT, PS, 2S, BTL, ETL;
the virtual T3V layers are skipped) becomes ONE sensitive ACTS surface (full cylinder or full disc, D111 nominal
position from sim/stage3/code/surfaces_s3.json).  Fatras PU-200 hits are then simulated on exactly these surfaces.

Material (same numbers as the Stage-3 kernel, T3_causal_s3.phase2_tracker + disc_material, UNVERIFIED baseline,
x0.5/x2 systematic): homogeneous Si-equivalent surface material on the sensitive surfaces (a stacked OT layer's x/X0 is
split equally over its two sensors), plus passive cylinders for the Be beam pipe (r = 22 mm, 0.23 % X0) and the IT
service cylinder (r = 190 mm, 1.0 % X0).  The Stage-3 kernel spreads each layer over a 1-2 cm radial slab; here the
material sits on the sensor surface (thin-scatterer approximation, standard for Fatras).

Volume layout (no overlaps):  R-container [beam pipe | tracker | BTL shell], wrapped in a Z-container [ETL- | ... | ETL+];
tracker = Z-container [fwd- | central | fwd+]; central = R-container [IT (Z: TFPX-, TBPX, TFPX+) | IT service | OT barrel];
fwd = Z-container [(R: TFPX D8 | TEDD D1-2) , (R: TEPX D1-4 | TEDD D3-5)].
(Production copy: JSON scratch files go to the per-process directory given to build().)
"""
import json
import math
from pathlib import Path

import acts
import acts.json
from acts import UnitConstants as u

TT = Path(__file__).resolve().parents[3]
SURF = TT / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json'
SCR = None   # set per process by build(scratch=...)
SI = [93.7, 465.2, 28.0855, 14.0, 0.0831e-3]      # Si: X0, L0 [mm], A, Z, molar density [mol/mm3 = ACTS native] (PDG Si 2.329 g/cm3)
BE = [352.8, 421.0, 9.012, 4.0, 0.2051e-3]         # Be beam pipe (PDG, 1.848 g/cm3) [mol/mm3]
BARREL_XX0 = {'IT': 0.012, 'PS': 0.025, '2S': 0.018}   # T3_causal_s3.phase2_tracker (UNVERIFIED baseline)


def _tr(z):
    return {"translation": [0.0, 0.0, float(z)], "rotation": [1, 0, 0, 0, 1, 0, 0, 0, 1]}


def _slab(xX0, mat=SI):
    """Homogeneous slab with thickness = xX0 * X0 [mm] of `mat`."""
    return {"material": mat, "thickness": float(xX0 * mat[0])}


def load_surfaces():
    d = json.loads(SURF.read_text())
    surfs = [dict(s, sid=i) for i, s in enumerate(d['surfaces'])]
    dmat = {m['name']: m['xX0'] for m in d['disc_material']}
    return surfs, dmat


def surface_xX0(s, dmat, scale=1.0):
    """x/X0 assigned to one sensitive surface (layer value split over the stacked pair)."""
    k, n = s['kind'], s['name']
    if k in ('BTL', 'ETL', 'T3V'):
        return 0.0
    nsens = 2 if (n.endswith('_in') or n.endswith('_out')) else 1
    if s['type'] == 0:
        x = BARREL_XX0[k]
    else:
        key = n.replace('_p', '').replace('_n', '').replace('_in', '').replace('_out', '')
        key = key.replace('TEDD_D1_PS', 'TEDD_D1_PS')
        x = dmat.get(key, BARREL_XX0[k])
    return scale * x / nsens


def build(mat_scale=1.0, with_material=True, level=acts.logging.WARNING, passive=True, root_env=0.0, nphi=1, scratch=None):
    """Returns (trackingGeometry, elements, sid_of_geoid, geoid_of_sid, surfs, passive).
    nphi > 1: every cylinder/disc is split into nphi azimuthal sectors (same geometric surface; CKF speed, plan §1.5);
    then geoid_of_sid maps (sid, sector) -> GeometryIdentifier and sector = floor((phi + pi) / (2 pi / nphi))."""
    import tempfile
    scr = Path(scratch) if scratch else Path(tempfile.mkdtemp(prefix='s4geo_'))
    surfs, dmat = load_surfaces()
    phys = [s for s in surfs if s['kind'] not in ('T3V', 'ETL')]
    jl = []; owner = []
    for s in phys:
        ns = nphi if s['kind'] not in ('BTL',) else 1
        hp = math.pi / ns
        for k in range(ns):
            avg = -math.pi + (2 * k + 1) * hp if ns > 1 else 0.0
            if s['type'] == 0:
                R, z0, z1 = s['p0'] * 10, s['p1'] * 10, s['p2'] * 10
                js = {"type": "CylinderSurface", "bounds": {"type": "CylinderBounds",
                      "values": [R, 0.5 * (z1 - z0), hp, avg, 0.0, 0.0]}, "transform": _tr(0.5 * (z0 + z1))}
            else:
                js = {"type": "DiscSurface", "bounds": {"type": "RadialBounds",
                      "values": [s['p1'] * 10, s['p2'] * 10, hp, avg]}, "transform": _tr(s['p0'] * 10)}
            js.update(sensitive=True, portal=False)
            jl.append(js); owner.append((s['sid'], k if ns > 1 else 0))
    scr.mkdir(parents=True, exist_ok=True)
    fj = scr / f's4geo_surfaces_n{nphi}.json'
    fj.write_text(json.dumps({"det": jl}))
    o = acts.json.SurfaceJsonOptions(); o.inputFile = str(fj); o.jsonEntryPath = ["det"]
    els = acts.json.readDetectorElementsFromJson(o, 0.15)
    assert len(els) == len(jl)
    tabs = {s['sid']: s for s in phys}
    by = {}
    for (sid, k), e in zip(owner, els):
        by.setdefault(tabs[sid]['name'], []).append((tabs[sid], e))

    def pick(pred):
        return [it for n in by for it in by[n] if pred(it[0])]

    root = acts.Blueprint(envelope=acts.ExtentEnvelope(r=[0.0, root_env], z=[root_env, root_env]))
    gap = acts.VolumeAttachmentStrategy.Gap
    Ltype = acts.LayerBlueprintNode.LayerType

    def layer(parent, name, items, ltype, env_r=0.4, env_z=0.4):
        ly = parent.addLayer(name)
        ly.surfaces = [e.surface() for _, e in items]
        ly.layerType = ltype
        ly.envelope = acts.ExtentEnvelope(r=[env_r * u.mm, env_r * u.mm], z=[env_z * u.mm, env_z * u.mm])
        return ly

    def cont(parent, name, axis):
        c = parent.addCylinderContainer(name, axis)
        c.attachmentStrategy = gap
        return c

    AZ, AR = acts.AxisDirection.AxisZ, acts.AxisDirection.AxisR
    # ETL (|z| = 2920 mm, timing proxy) is NOT in the probe geometry: Z-stacking it with the r = 0 beam region fails
    # ("Invalid inner cylinder configuration"); quirk ETL hits stay analysis-level (plan §1).
    mid = cont(root, 'Mid', AR)
    # passive beam pipe: plain (non-sensitive) cylinder in its own layer
    mid.addStaticVolume(acts.Transform3(acts.Vector3(0, 0, 0)), acts.CylinderVolumeBounds(0.0, 20.0 * u.mm, 2700.0 * u.mm), name='BeamRegion')
    bp = acts.Surface.createCylinder(acts.Transform3(acts.Vector3(0, 0, 0)), acts.CylinderBounds(22.0 * u.mm, 2700.0 * u.mm))
    lbp = mid.addLayer('BeamPipe') if passive else None
    if passive: lbp.surfaces = [bp]; lbp.layerType = Ltype.Cylinder
    if passive: lbp.envelope = acts.ExtentEnvelope(r=[1.0 * u.mm, 1.0 * u.mm], z=[0.0, 0.0])
    trk = cont(mid, 'Tracker', AZ)
    btl = layer(mid, 'BTL', pick(lambda s: s['name'] == 'BTL'), Ltype.Cylinder, env_r=2.0, env_z=0.0)

    def fwd(parent, sign):
        sfx = '_p' if sign > 0 else '_n'
        f = cont(parent, 'Fwd' + sfx, AZ)
        order = [1, 2] if sign > 0 else [2, 1]
        for part in order:
            g = cont(f, f'F{part}{sfx}', AR)
            inner = cont(g, f'F{part}in{sfx}', AZ)
            outer = cont(g, f'F{part}out{sfx}', AZ)
            if part == 1:
                inn = ['TFPX_D8']
                out = ['TEDD_D1', 'TEDD_D2']
            else:
                inn = ['TEPX_D1', 'TEPX_D2', 'TEPX_D3', 'TEPX_D4']
                out = ['TEDD_D3', 'TEDD_D4', 'TEDD_D5']
            if sign < 0:
                inn, out = inn[::-1], out[::-1]
            for nm in inn:
                layer(inner, nm + sfx, pick(lambda s, nm=nm: s['name'] == nm + sfx), Ltype.Disc)
            for nm in out:
                layer(outer, nm + sfx, pick(lambda s, nm=nm: s['name'].startswith(nm + sfx + '_')), Ltype.Disc)
        return f

    fwd(trk, -1)
    cen = cont(trk, 'Central', AR)
    it = cont(cen, 'IT', AZ)
    for k in range(7, 0, -1):
        layer(it, f'TFPX_D{k}_n', pick(lambda s, k=k: s['name'] == f'TFPX_D{k}_n'), Ltype.Disc)
    itb = cont(it, 'TBPX', AR)
    for k in range(1, 5):
        layer(itb, f'TBPX_L{k}', pick(lambda s, k=k: s['name'] == f'TBPX_L{k}'), Ltype.Cylinder)
    for k in range(1, 8):
        layer(it, f'TFPX_D{k}_p', pick(lambda s, k=k: s['name'] == f'TFPX_D{k}_p'), Ltype.Disc)
    svc = acts.Surface.createCylinder(acts.Transform3(acts.Vector3(0, 0, 0)), acts.CylinderBounds(190.0 * u.mm, 1200.0 * u.mm))
    lsv = cen.addLayer('ITService') if passive else None
    if passive: lsv.surfaces = [svc]; lsv.layerType = Ltype.Cylinder
    if passive: lsv.envelope = acts.ExtentEnvelope(r=[1.0 * u.mm, 1.0 * u.mm], z=[0.0, 0.0])
    ot = cont(cen, 'OTB', AR)
    for nm in ['TBPS_L1', 'TBPS_L2', 'TBPS_L3', 'TB2S_L1', 'TB2S_L2', 'TB2S_L3']:
        layer(ot, nm, pick(lambda s, nm=nm: s['name'].startswith(nm + '_')), Ltype.Cylinder)
    fwd(trk, +1)

    gctx = acts.GeometryContext.dangerouslyDefaultConstruct()
    tg = root.construct(options=acts.BlueprintOptions(), gctx=gctx, level=level)
    sid_of = {}; geo_of = {}
    for (sid, k), e in zip(owner, els):
        sid_of[e.surface().geometryId] = sid
        geo_of[(sid, k)] = e.surface().geometryId
    if with_material:
        entries = []
        for (sid, k), e in zip(owner, els):
            s = tabs[sid]
            x = surface_xX0(s, dmat, mat_scale)
            if x <= 0:
                continue
            g = e.surface().geometryId
            entries.append(_mat_entry(g, _slab(x)))
        for srf, x, m in (((bp, 0.0023, BE), (svc, 0.010, SI)) if passive else ()):
            entries.append(_mat_entry(srf.geometryId, _slab(mat_scale * x, m)))
        hdr = {"format-version": 0, "value-identifier": "Material Surface Map"}
        jm = {"Surfaces": {"acts-geometry-hierarchy-map": hdr, "entries": entries},
              "Volumes": {"acts-geometry-hierarchy-map": {"format-version": 0, "value-identifier": "Material Volume Map"},
                          "entries": []}}
        fm = scr / f's4geo_material_x{mat_scale:g}_n{nphi}.json'
        fm.write_text(json.dumps(jm))
        dec = acts.json.JsonMaterialDecorator(acts.json.MaterialMapJsonConverter.Config(), str(fm), acts.logging.WARNING)
        for e in els:
            dec.decorate(e.surface())
        if passive:
            dec.decorate(bp); dec.decorate(svc)
    return tg, els, sid_of, geo_of, surfs, (bp, svc)


def _mat_entry(g, slab):
    d = {"volume": g.volume, "layer": g.layer, "sensitive": g.sensitive}
    for k in ("boundary", "approach", "extra"):
        v = getattr(g, k, 0)
        if v:
            d[k] = v
    d["value"] = {"material": {"binUtility": {"binningdata": []}, "data": [[slab]], "mapMaterial": True,
                               "type": "homogeneous"}}
    return d


if __name__ == '__main__':
    import sys
    tg, els, sid_of, geo_of, surfs, passive = build(level=acts.logging.INFO)
    gctx = acts.GeometryContext.dangerouslyDefaultConstruct()
    n = []
    tg.visitSurfaces(lambda s: n.append((s.geometryId, s.isSensitive, s.surfaceMaterial is not None)))
    print('surfaces visited', len(n), 'sensitive', sum(1 for x in n if x[1]), 'with material', sum(1 for x in n if x[2]))
    print('mapped stage-3 ids', len(sid_of))
    for p in passive:
        print('passive', p.geometryId, p.surfaceMaterial is not None)


RES = {'IT': (7.2e-3, 28.9e-3), 'PS': (28.9e-3, 0.423), '2S': (26.0e-3, 14.5), 'BTL': (0.87, 16.0)}   # PROBE values (BTL swapped)
RES_PROD = {'IT': (7.2e-3, 28.9e-3), 'PS': (28.9e-3, 0.423), '2S': (26.0e-3, 14.5), 'BTL': (16.0, 0.9)}   # plan §1.5 (mm)
SIG_T_BTL = 0.035   # ns, plan §1.5 baseline (35 ps; 60 ps variation)


def write_digi(sid_of, surfs, path, res=RES_PROD, sig_t_ns=SIG_T_BTL):
    """Smearing digitisation config (one entry per sensitive surface/sector), see p2_inject_digi.py header."""
    tab = {s['sid']: s for s in surfs}
    entries = []
    for g, sid in sid_of.items():
        s = tab[sid]; k = s['kind']
        srp, slong = res[k]
        if s['type'] == 0:
            sm = [dict(index=0, mean=0.0, stddev=srp, type='Gauss'), dict(index=1, mean=0.0, stddev=slong, type='Gauss')]
        else:
            rmid = 0.5 * (s['p1'] + s['p2']) * 10
            sm = [dict(index=0, mean=0.0, stddev=slong, type='Gauss'), dict(index=1, mean=0.0, stddev=srp / rmid, type='Gauss')]
        if k == 'BTL':
            sm.append(dict(index=5, mean=0.0, stddev=sig_t_ns * u.ns, type='Gauss'))   # ACTS time unit = mm/c
        entries.append(dict(volume=g.volume, sensitive=g.sensitive, value=dict(smearing=sm)))
    j = {"acts-geometry-hierarchy-map": {"format-version": 0, "value-identifier": "digitization-configuration"}, "entries": entries}
    Path(path).write_text(json.dumps(j))
    return path


def sector(x, y, nphi):
    return min(int((math.atan2(y, x) + math.pi) / (2 * math.pi / nphi)), nphi - 1) if nphi > 1 else 0
