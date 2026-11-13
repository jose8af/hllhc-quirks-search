"""val_qed.py -- QED FSR off the quirks (plan D12; review S2-R1 B-9 / C-7; fixer 2026-10-11).  Output results/qed_fsr.json.
Diagnosis: Pythia 8.313 `TimeShower:QEDshowerByOther` acts only on particles flagged isResonance; the production card sets
isResonance = off and the SLHA DECAY block (width 0) in the MG LHE header resets the flag even when set on.  With
cards/pythia8_quirk_qedfsr.dat (SLHA:useDecayTable = off, 900001{1,3}:isResonance = on) the quirk pair radiates.
Test samples (data/sim/aux/fixer/qed/): one Pythia job per point re-showered with the fix (scripts/reshower.py, same LHE and
seed as production).  Without QED FSR off the quirks m(QQ) after the shower equals the LHE m(QQ) exactly, so the per-event
effect is exactly delta x = (M_LHE - M_shower)/m with x = 2(gamma*-1): the comparison below is paired (same events).
Statistical errors (review S2-R2 C-5): paired bootstrap over events (the same resampled events enter x and x_LHE),
500 resamples, seed 5; *_err = standard deviation of the bootstrap ratios.  Central values are unchanged by this.
Photon spectrum: E-LOPS m500 job 1, first 2000 events, from the HepMC (text summary in the same directory).
Run: pixi run -e ana python scripts/val_qed.py"""
import glob
import os
import re

import numpy as np

from vlib import DATA, save, wquant, _boost_gamma_star

Q = os.path.join(DATA, 'aux', 'fixer', 'qed')


def main():
    R = dict(note=__doc__, points={})
    for f in sorted(glob.glob(os.path.join(Q, '*_qedfsr.npz'))):
        c = dict(np.load(f)); m = float(c['mq']); w = c['w']
        _, Mh = _boost_gamma_star(c['p_qp_hard'], c['p_qm_hard'])
        dM = Mh - c['m_pair']
        out = {}
        for lab, sel in (('all', w > 0), ('tail', (w > 0) & (c['pt_pair'] > 200) & (np.abs(c['eta_pair']) < 2.5))):
            x = 2 * (c['gamma_star'][sel] - 1); x0 = Mh[sel] / m - 2
            q, q0 = wquant(x, w[sel])[1], wquant(x0, w[sel])[1]
            out[lab] = dict(n=int(sel.sum()), P_dM_gt1=float(np.mean(dM[sel] > 1)), P_dM_gt5=float(np.mean(dM[sel] > 5)),
                            P_dM_gt20=float(np.mean(dM[sel] > 20)), mean_dM_GeV=float(dM[sel].mean()),
                            x_median_rel=float(q / q0 - 1),
                            x_mean_rel=float(np.average(x, weights=w[sel]) / np.average(x0, weights=w[sel]) - 1))
            ws = w[sel]; rng = np.random.default_rng(5); bmed, bmean = [], []
            for _ in range(500):
                ix = rng.integers(0, len(x), len(x))
                bmed.append(wquant(x[ix], ws[ix])[1] / wquant(x0[ix], ws[ix])[1] - 1)
                bmean.append(np.average(x[ix], weights=ws[ix]) / np.average(x0[ix], weights=ws[ix]) - 1)
            out[lab].update(x_median_rel_err=float(np.std(bmed)), x_mean_rel_err=float(np.std(bmean)))
        R['points'][os.path.basename(f)[:-11]] = out
    t = open(os.path.join(Q, 'E-LOPS_m500_c0_job1_first2000_photons.txt')).read()
    g = lambda k: float(re.search(k + r' ([0-9.eE+-]+)', t).group(1))
    R['photons_LOPS500'] = dict(frac_events_with_quirk_photon=g('quirk->gamma'), P_Egamma_gt5=g(r'P\(Egamma>5\)'),
                                P_Egamma_gt20=g(r'P\(Egamma>20\)'), n_events=2000)
    save('qed_fsr.json', R)
    for k, v in R['points'].items():
        print(k, {a: round(100 * b, 2) for a, b in v['tail'].items() if a.startswith('x_') or a.startswith('P_')})
    print(R['photons_LOPS500'])


if __name__ == '__main__':
    main()
