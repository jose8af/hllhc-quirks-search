"""p3-f Task B analysis (investigator Jorunn): N_eff per rung and per CPU-h of the thinning re-find variant on the 400
control trials, variance components (between events / draw to draw), projection to 3,000 rho = 2 events.  No direct
count is compared; the evaluability arithmetic uses the expected 96,000-trial direct counts of P3B's B2-g table.
Writes outputs/p3f/refind_yield.json."""
import glob
import json
import logging
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'p3b'))
import cols as TC  # noqa: E402

DATA = Path('/nfs/cajuela/jdochoa/quirks_v2/data/p3f/p3-f-refind')
OUT = HERE.parents[1] / 'outputs' / 'p3f'
P3B = HERE.parents[1] / 'outputs' / 'p3b' / 'b2_dev_closure.json'
log = logging.getLogger('refind3_ana')
SHOW = ['R04', 'R05', 'R06', 'R07', 'R08', 'R04x2S>=3', 'R05x2S>=3', 'R06x2S>=3', 'R07x2S>=3', 'R05xp>0.001',
        'R05xp>0.01', 'R06xp>0.001']
CAP = np.log(1.5) / 3
NB = 2000
KS = (1, 3, 8, 16, 64)
NEV3000 = 3000


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    dd = [np.load(f) for f in sorted(glob.glob(str(DATA / '*' / 'refind3-*.npz')))]
    G = np.concatenate([d['grp'] for d in dd]).astype(float)            # (ntr, K, ncol)
    cpu = np.concatenate([d['cpu'] for d in dd])
    key = np.char.add(np.char.add(np.concatenate([d['job'] for d in dd]).astype(str), '|'),
                      np.concatenate([d['ev'] for d in dd]).astype(str))
    u, inv = np.unique(key, return_inverse=True)
    nev = len(u); ntr, K, _ = G.shape
    tpe = ntr / nev
    # per event and draw: sum over the event's trials
    Y = np.zeros((nev, K, G.shape[2])); np.add.at(Y, inv, G)
    rng = np.random.default_rng(31)
    W = rng.multinomial(nev, np.full(nev, 1 / nev), size=NB).astype(float)
    b2g = json.loads(P3B.read_text())['thinning']['B2g_projection']
    cpu_draw = float(cpu.mean())
    res = dict(trials=int(ntr), events=int(nev), draws=int(K), cpu_s_per_refind_mean=cpu_draw,
               cpu_s_per_refind_sd=float(cpu.std()), total_refind_cpu_h=float(cpu.sum() / 3600), columns={})
    for c in SHOW:
        j = TC.COLS.index(c)
        y = Y[:, :, j]                                   # (nev, K)
        mu_e = y.mean()                                  # mean per event per draw
        rate = mu_e / tpe                                # per trial
        rec = dict(count=float(G[:, :, j].sum()), rate_per_trial=float(rate))
        if mu_e > 0:
            sw2 = float(np.mean(np.var(y, axis=1, ddof=1)))                     # draw-to-draw, within event
            sb2 = float(np.var(y.mean(1), ddof=1) - sw2 / K)                    # between events
            rec.update(sigma_w2_per_event=sw2, sigma_b2_per_event=sb2, fano_w=sw2 / mu_e)
            # direct bootstraps for K' = 1..K (first K' draws)
            sb = {}
            for kk in range(1, K + 1):
                ym = y[:, :kk].mean(1)
                rep = (W @ ym) / nev
                sb[str(kk)] = float(np.std(rep, ddof=1) / mu_e)
            rec['s_boot_measured'] = sb
            rec['N_eff_measured_400trials'] = {k: 1 / v ** 2 for k, v in sb.items()}
            proj = {}
            for kk in KS:
                s2 = (max(sb2, 0.0) + sw2 / kk) / (NEV3000 * mu_e ** 2)
                ne = 1 / s2
                n96 = b2g.get(c, {}).get('N_direct_96k_expected')
                st = float(np.sqrt(1 / n96 + 1 / ne)) if n96 else None
                proj[str(kk)] = dict(N_eff=float(ne), cpu_h=float(NEV3000 * tpe * kk * cpu_draw / 3600),
                                     N_eff_per_cpu_h=float(ne / (NEV3000 * tpe * kk * cpu_draw / 3600)),
                                     N_direct_96k_expected=n96, sigma_tot=st,
                                     evaluable=None if st is None else bool(st <= CAP))
            rec['projection_3000_events'] = proj
        res['columns'][c] = rec
        log.info('%-12s count %6d rate %.4g  %s', c, rec['count'], rate,
                 {k: round(v['N_eff']) for k, v in rec.get('projection_3000_events', {}).items()})
    (OUT / 'refind_yield.json').write_text(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
