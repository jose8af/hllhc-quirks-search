"""f200_fxfx.py -- f200 from the FxFx (MC@NLO 0-1j) sample at E 500 against the S2-c band.  Channel (ii) successor
Sune, 2026-11-19.  Run in the sim 'ana' env (numpy) on a worker:

  sim/.pixi/envs/ana/bin/python -I phase2_exploration/src/s2/f200_fxfx.py

Definition: f200 = sum w [pt_pair > 200 GeV] / sum w, after the shower and the FxFx matching, no eta cut (the only
definition, Edgar's file section 2.4 and f200.py). The weights are the signed MC@NLO weights. The statistical error
is the formula of f200.py `frac` (weighted binomial).
Inputs: npz files of campaign p2-b-s2-fxfx-gen with done markers (sha256 re-checked).
Rule (frozen STR, STRATEGY_oscar_2026-11-16_10-41.md l.2021-2022): "If the FxFx value lies outside the band, the band
is enlarged to contain it."  The band is the nominal E500 entry of outputs/s2/f200.json.  'Outside' is read on the
central value; the FxFx statistical error is reported next to it.
Output: outputs/s2/f200_fxfx.json.
"""
import json
import logging
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from f200 import PT, frac  # noqa: E402
from marker_files import done_outputs  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('f200_fxfx')
OUTD = os.path.join(HERE, '..', '..', 'outputs', 's2')


def main():
    files = done_outputs('p2-b-s2-fxfx-gen', suffix='.npz', verify=True)
    if not files:
        sys.exit('no done npz files')
    cols = {k: [] for k in ('w', 'pt_pair', 'n_me', 'njet30', 'npnlo')}
    n_lhe = n_out = 0
    for f in files:
        d = np.load(f)
        for k in cols:
            cols[k].append(d[k])
        n_out += int(d['summary_n_out'])
        n_lhe += int(json.load(open(f[:-4] + '.timing.json'))['n_lhe'])
    c = {k: np.concatenate(v) for k, v in cols.items()}
    w, pt = c['w'], c['pt_pair']
    f, e = frac(pt, w)
    neff = w.sum() ** 2 / (w ** 2).sum()
    per_file = []
    for fl in files:
        d = np.load(fl)
        per_file.append(frac(d['pt_pair'], d['w'])[0])
    nom = json.load(open(os.path.join(OUTD, 'f200.json')))['points']['E500']
    f0, up, dn = nom['nom']['f200'], nom['band']['up'], nom['band']['dn']
    rel = f / f0 - 1
    outside = not (-dn <= rel <= up)
    up2, dn2 = (max(up, rel), max(dn, -rel)) if outside else (up, dn)
    mult = {k: {int(u): int(n) for u, n in zip(*np.unique(c[k], return_counts=True))} for k in ('n_me', 'njet30', 'npnlo')}
    r = dict(point='E500', definition='f200 = sum w[pt_pair > %g] / sum w, signed MC@NLO weights, after FxFx matching, no eta cut' % PT,
             files=files, n_lhe=n_lhe, n_matched=int(len(w)), matched_fraction=len(w) / n_lhe, n_out_check=n_out,
             neg_weight_fraction=float((w < 0).mean()), n_eff=float(neff),
             f200_fxfx=f, stat=e, stat_rel=e / f, per_file_f200=per_file, multiplicities=mult,
             nominal=dict(f200=f0, stat=nom['nom']['stat'], band_up=up, band_dn=dn),
             rel_shift_fxfx_vs_nominal=rel, rel_shift_stat=float(np.hypot(e / f0, f * nom['nom']['stat'] / f0 ** 2)),
             outside_band=outside, band_after_fxfx=dict(up=up2, dn=dn2),
             T1_nuisance_after_fxfx=dict(kappa_up=1 + up2, kappa_dn=1 - dn2),
             rule='STR l.2021-2022: if the FxFx value lies outside the band, the band is enlarged to contain it (central value)')
    json.dump(r, open(os.path.join(OUTD, 'f200_fxfx.json'), 'w'), indent=1)
    log.info('E500 FxFx f200 = %.5f +- %.5f (%.1f %%) from %d matched / %d LHE events; nominal %.5f band +%.4f/-%.4f; '
             'shift %+.4f +- %.4f; outside=%s; band -> +%.4f/-%.4f', f, e, 100 * e / f, len(w), n_lhe, f0, up, dn, rel,
             r['rel_shift_stat'], outside, up2, dn2)


if __name__ == '__main__':
    main()
