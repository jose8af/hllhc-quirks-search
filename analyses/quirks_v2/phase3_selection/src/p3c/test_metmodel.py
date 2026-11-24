"""test_metmodel.py -- unit checks of metmodel.py (limiting cases of STR l.1334 and of the formula verification rule).
Run: <python with numpy> test_metmodel.py <one p3c_gen or pilot npz>"""
import json
import logging
import sys

import numpy as np

import metmodel as M

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('test_metmodel')


def main(path):
    z = np.load(path); meta = json.loads(str(z['meta']))
    if meta.get('mode') == 'p3c_gen':
        c = meta['evt_cols']; e = z['evt']
        px, py = e[:, c.index('px_eta5')], e[:, c.index('py_eta5')]
        mx, my = e[:, c.index('met_x')], e[:, c.index('met_y')]; ax, ay = e[:, c.index('px_all')], e[:, c.index('py_all')]
    else:
        g = z['gsum']; c = meta['gsum_cols']; px, py = g[:, c.index('px_eta5')], g[:, c.index('py_eta5')]
        mx, my = z['evt'][:, 0], z['evt'][:, 1]; ax = ay = None
    n = min(len(px), 3000)
    inp = M.build_inputs(px[:n], py[:n], z['jets'], z['jet_off'], z['lep'], z['lep_off'])
    rng = np.random.default_rng(1)
    # 1. limiting case: R = 1, no lost lepton, S = 0  ->  reconstructed sum = visible sum in |eta| < 5
    p = dict(M.NOMINAL, jer_scale=0.0, f_tail=0.0, sigma_soft=0.0, lost_electron_in_sum=False, trig='none')
    eff = M.eff_lepton
    M.eff_lepton = lambda pdg, pt, eta: np.ones_like(np.asarray(pt, float))
    o = M.apply(inp, p, rng, 1, return_met=True)
    M.eff_lepton = eff
    d = np.hypot(o['hx'][:, 0] - px[:n], o['hy'][:, 0] - py[:n]).max()
    assert d < 1e-3, d            # float32 summaries
    log.info('limit R=1, no lost lepton, S=0: max |sum_reco - sum_visible(|eta|<5)| = %.2e GeV  PASS', d)
    # neutrino MET against the visible sum: equal up to particles beyond |eta| = 5
    r = np.hypot(px[:n] + mx[:n], py[:n] + my[:n])
    log.info('|visible(|eta|<5) + neutrinos|: median %.2f GeV, 95 %% quantile %.2f GeV (particles beyond |eta| = 5)',
             np.median(r), np.quantile(r, 0.95))
    if ax is not None:
        r2 = np.hypot(ax[:n] + mx[:n], ay[:n] + my[:n]).max()
        assert r2 < 1e-3 * 14000, r2
        log.info('all visible + neutrinos: max |sum pT| = %.3f GeV (momentum conservation)  PASS', r2)
    # 2. systematic -> 0 when the variation -> 0: same seed, same result
    q = dict(M.NOMINAL, sigma_soft=29.0)
    a = M.apply(inp, q, np.random.default_rng(5), 4)['w']; b = M.apply(inp, dict(q), np.random.default_rng(5), 4)['w']
    assert np.array_equal(a, b)
    # 3. resolution table and efficiencies in range; spot values
    assert abs(M.jer_sigma([100.], [0.])[0] - 0.13) < 1e-12 and abs(M.jer_sigma([1000.], [0.])[0] - 0.067) < 1e-12
    assert abs(M.jer_sigma([20.], [2.0])[0] - 0.27) < 1e-12
    assert M.eff_lepton([13], [50.], [2.9])[0] == 0.0 and M.eff_lepton([11], [25.], [2.0])[0] == 0.81
    t = M.trig_eff([250., 0., 1000.])
    assert abs(t[0] - 0.975) < 1e-9 and 0 <= t[1] <= 0.05 and t[2] == 1.0
    assert abs(M.trig_eff([250.], 'erf_shifted')[0] - 0.879) < 2e-3      # EDG §2.6 table: 0.879 at 250 GeV
    # 4. smearing width reproduces the table: one jet of 100 GeV at eta 0
    one = dict(jp=np.zeros((20000, M.JMAX, 3)), jm=np.zeros((20000, M.JMAX), bool), lp=np.zeros((20000, M.LMAX, 5)),
               lm=np.zeros((20000, M.LMAX), bool), ngam=np.zeros(20000), ux=np.zeros(20000), uy=np.zeros(20000))
    one['jp'][:, 0] = (100., 0., 0.); one['jm'][:, 0] = True
    o = M.apply(one, dict(M.NOMINAL, f_tail=0.0, sigma_soft=0.0), np.random.default_rng(2), 5, return_met=True)
    s = o['hx'].std() / 100.0
    assert abs(s - 0.13) < 0.002, s
    o = M.apply(one, dict(M.NOMINAL, sigma_soft=0.0), np.random.default_rng(2), 5, return_met=True)
    ft = np.mean(o['hx'] < 100 * (1 - 3 * 0.13))
    log.info('one 100 GeV jet: core sigma %.4f (table 0.13); fraction below 1 - 3 sigma with the nominal tail %.4f '
             '(Gaussian alone 0.00135; expected 0.985 x 0.00135 + 0.015 x P(|N(0,3 sigma)| > 3 sigma) = %.4f)',
             s, ft, 0.985 * 0.00135 + 0.015 * 0.3173)
    assert abs(ft - (0.985 * 0.00135 + 0.015 * 0.3173)) < 0.001
    log.info('all checks PASS')


if __name__ == '__main__':
    main(sys.argv[1])
