"""f1r_density_bench.py -- Stage-4 plan FIXER R1 probe (TT env): V4-2 benchmark of the Fatras in-time PU-200 hit density
against the public CMS Phase-2 Tracker TDR (CMS-TDR-014) occupancies (critical review B-7).

Probe density: the 56 fresh PU-200 events of f1r_pu_gen.py (data/acts_stage4/fix_r1/pu/), measurements per sensor in the
central slice |eta| < 0.3 (|z| < R sinh 0.3, taken from the origin), per cm^2 per bunch crossing.
TDR reference (tt + PU 200, 14 TeV, includes 12 previous + 3 following bunch crossings, TDR §6.2.1 l.4286-4288 of the text
copy; readout window +-12.5 ns, l.4331-4333):
  * Fig. 6.3 (PDF p.101): hit occupancy = fraction of channels with a digitized hit, vs eta, per layer.  Values at eta ~ 0
    (IT) / eta ~ 0.25 (OT) read graphically from the rendered page (data/acts_stage4/fix_r1/tdr/, pixel positions of the
    markers against the major tick marks; reading uncertainty ~ +-0.02 decade = +-5 %).
  * Channel sizes as simulated (TDR §6.2.1, PDF p.100, l.4277-4282): IT pixel 25 x 100 um^2; PS-s strip 100 um x 23.13 mm;
    PS-p macro-pixel 100 um x 1446 um; 2S strip 90 um x 50.25 mm.
  * Cluster size (channels per cluster): OT from Fig. 12.3 left (PDF p.277), graphical mean ~1.8 (PS strips, macro-pixels)
    and ~2.2 (2S strips), +-0.2.  The IT pixel cluster size is NOT given in the TDR: bracket 1.5-3 pixels (ESTIMATE).
  clusters/cm^2 = occupancy / (channel area) / <cluster size>.  One Fatras measurement = one particle crossing = one cluster
  (doMerge = False), so the ratio TDR/probe is the density normalisation factor per layer.
Run (theory_track): pixi run python acts/stage4/probes/f1r_density_bench.py
Output: data/acts_stage4/fix_r1/f1r_density_bench.json
"""
import json
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
PU = TT / 'data' / 'acts_stage4' / 'fix_r1' / 'pu'
S = json.loads((TT / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json').read_text())['surfaces']
NAME = {i: s['name'] for i, s in enumerate(S)}
R = {i: s['p0'] * 10.0 for i, s in enumerate(S) if s['type'] == 0}     # cm -> mm

# TDR Fig. 6.3 graphical readings (see docstring); channel area [cm^2]; cluster size (lo, nominal, hi)
TDR = {
    'TBPX_L1': (2.04e-3, 25e-4 * 100e-4, (1.5, 2.0, 3.0)), 'TBPX_L2': (4.86e-4, 25e-4 * 100e-4, (1.5, 2.0, 3.0)),
    'TBPX_L3': (2.25e-4, 25e-4 * 100e-4, (1.5, 2.0, 3.0)), 'TBPX_L4': (1.55e-4, 25e-4 * 100e-4, (1.5, 2.0, 3.0)),
    'TBPS_L1_strip': (2.82e-2, 100e-4 * 2.313, (1.6, 1.8, 2.0)), 'TBPS_L1_macro': (1.93e-3, 100e-4 * 0.1446, (1.6, 1.8, 2.0)),
    'TBPS_L2_strip': (1.46e-2, 100e-4 * 2.313, (1.6, 1.8, 2.0)), 'TBPS_L2_macro': (9.5e-4, 100e-4 * 0.1446, (1.6, 1.8, 2.0)),
    'TBPS_L3_strip': (8.3e-3, 100e-4 * 2.313, (1.6, 1.8, 2.0)), 'TBPS_L3_macro': (5.1e-4, 100e-4 * 0.1446, (1.6, 1.8, 2.0)),
    'TB2S_L1': (8.3e-3, 90e-4 * 5.025, (2.0, 2.2, 2.4)), 'TB2S_L2': (5.26e-3, 90e-4 * 5.025, (2.0, 2.2, 2.4)),
    'TB2S_L3': (3.34e-3, 90e-4 * 5.025, (2.0, 2.2, 2.4)),
}
# probe sensor used for each TDR entry (stacked layers: _in = macro-pixel side / _out = strip side; both have the same
# Fatras density to < 2 %, checked below)
PROBE = {'TBPX_L1': 'TBPX_L1', 'TBPX_L2': 'TBPX_L2', 'TBPX_L3': 'TBPX_L3', 'TBPX_L4': 'TBPX_L4',
         'TBPS_L1_strip': 'TBPS_L1_out', 'TBPS_L1_macro': 'TBPS_L1_in', 'TBPS_L2_strip': 'TBPS_L2_out',
         'TBPS_L2_macro': 'TBPS_L2_in', 'TBPS_L3_strip': 'TBPS_L3_out', 'TBPS_L3_macro': 'TBPS_L3_in',
         'TB2S_L1': 'TB2S_L1_in', 'TB2S_L2': 'TB2S_L2_in', 'TB2S_L3': 'TB2S_L3_in'}
SID = {v: k for k, v in NAME.items()}

dens = {n: [] for n in SID if n.startswith(('TBPX', 'TBPS', 'TB2S'))}
nev = 0
for f in sorted(PU.glob('pu_w*.npz')):
    d = np.load(f)
    for k in [k for k in d.files if k.startswith('ev')]:
        e = d[k]; nev += 1
        for n in dens:
            sid = SID[n]; Rm = R[sid]; zc = Rm * np.sinh(0.3)
            m = (e[:, 0] == sid) & (np.abs(e[:, 3]) < zc)
            area = 2 * np.pi * Rm * 2 * zc / 100.0          # mm^2 -> cm^2
            dens[n].append(m.sum() / area)
probe = {n: dict(mean=float(np.mean(v)), sem=float(np.std(v) / np.sqrt(len(v)))) for n, v in dens.items()}
rows = {}
for key, (occ, area, cs) in TDR.items():
    fired = occ / area
    cl = [fired / c for c in cs]          # hi cs -> lo clusters
    p = probe[PROBE[key]]['mean']
    rows[key] = dict(tdr_occupancy=occ, channels_per_cm2=1.0 / area, tdr_fired_per_cm2=fired,
                     tdr_clusters_per_cm2_nominal=cl[1], tdr_clusters_per_cm2_range=[cl[2], cl[0]],
                     probe_hits_per_cm2=p, probe_sem=probe[PROBE[key]]['sem'],
                     ratio_tdr_over_probe_nominal=cl[1] / p, ratio_range=[cl[2] / p, cl[0] / p])
    print(f"{key:15s} TDR occ {occ:.2e} -> {cl[1]:7.3f} cl/cm2 [{cl[2]:.3f},{cl[0]:.3f}]  probe {p:7.3f}  ratio {cl[1]/p:5.2f} [{cl[2]/p:.2f},{cl[0]/p:.2f}]")
inout = {n[:7]: probe[n[:7] + '_out']['mean'] / probe[n[:7] + '_in']['mean'] for n in dens if n.endswith('_in')}
out = dict(n_events=nev, eta_slice=0.3, probe_hits_per_cm2=probe, out_over_in=inout, comparison=rows,
           sources=dict(occupancy='CMS-TDR-014 Fig. 6.3, PDF p.101 (graphical reading)',
                        channel_sizes='CMS-TDR-014 §6.2.1, PDF p.100 (text copy l.4277-4282)',
                        cluster_size_OT='CMS-TDR-014 Fig. 12.3 left, PDF p.277 (graphical reading)',
                        cluster_size_IT='not in the TDR: 1.5-3 pixels ESTIMATE',
                        oot='TDR simulation includes 12 previous and 3 following crossings (l.4286-4288)'))
(TT / 'data' / 'acts_stage4' / 'fix_r1' / 'f1r_density_bench.json').write_text(json.dumps(out, indent=1))
print('out/in', {k: round(v, 3) for k, v in inout.items()})
