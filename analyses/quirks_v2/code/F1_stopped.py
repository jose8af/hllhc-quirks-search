"""F1_stopped.py -- fix pass F1 (answers R1-critical B-6 and R1-constructive B5/B8): stopped-pair (delayed
annihilation) reach with (i) a lifetime-dependent empty-BX live fraction instead of the flat 21 % of the 2016 fill,
(ii) a non-zero background bracket, and (iii) a Run-2+3 (13-13.6 TeV) recast estimate besides the HL-LHC projection.

Inputs (all ESTIMATE unless a source is given):
  * sigma_DY(E, N_IC=1), LO 14 TeV: figures/T6_xsec_table.txt (T6); x N_IC = 2; K = 1.2 (reproduces T6's 7-11 events
    at 500 GeV, f_stop = 1 %, 3 ab-1, which used the model-doc NLO normalisation).
  * yield model of T6 G-T6-4: N = sigma L f_stop x eps_live x 0.55 (eps_reco) x 0.83 (vetoes) x BR_vis (0.4-0.65)
    [1801.00359 Tab.1-2 values as read by T6].
  * f_stop(EB+HB, inclusive) = 1.0 % (x2 band) [T3 Sec.7]; full calorimeter 6-9 % (Phase-2 only, endcap empty-BX
    trigger UNVERIFIED).
  * trigger: "at least two BXs away from any proton bunch" [1801.00359 Sec.3]; eps_live(tau) computed below for a
    schematic 25 ns filling scheme (trains of 72 bunches with 8-slot gaps, 4 trains per SPS batch, 38-slot batch gaps,
    9 batches, abort gap filling the orbit: 2592 bunches; UNVERIFIED stand-in for both the 2016-18 and the HL-LHC
    schemes). eps_live(tau) = probability that an exponential decay (mean tau, after production in a filled BX)
    falls in an eligible empty BX. Normalised so that eps_live(tau -> infinity) = 0.21 (the 2016 value used by T6
    and Evans-Luty) to isolate the lifetime dependence.
  * annihilation delay tau: internal-energy dissipation 0.02-0.5 us (T6_stopping.py), E-L Fig.4 0.1-100 us.
  * background: 2016 calorimeter search 11.4 events in 586 h of trigger livetime [1801.00359 Tab.4], i.e. 16.3 h of
    livetime per fb-1. HL-LHC: livetime per fb-1 scaled by 1/4 (leveled 5e34 vs ~1.2e34) -> ~4 h/fb-1 ->
    ~1.2e4 h for 3 ab-1 -> ~230 events at the 2016 selection (jet E > 50 GeV). A tighter energy threshold for
    2 m_Q-scale deposits will cut this by an unknown factor: we bracket B = 0, 10, 230.
  * Run 2+3: 138 fb-1 at 13 TeV (sigma x 0.82 rel. to 14 TeV) + ~250 fb-1 at 13.6 TeV (x 0.90) -- luminosity and
    sqrt(s) ratios are ESTIMATE/UNVERIFIED; background scaled from 2016 by livetime (16.3 h/fb-1 x ~0.6 for the higher
    Run-3 luminosity) -> ~4000 h -> ~80 events at the 2016 selection.
Limit: expected 95 % CL CLs upper limit on the signal for n_obs = round(B).
Run (from theory_track/): pixi run python code/F1_stopped.py     Output copy: figures/F1_stopped_out.txt
"""
import os
import numpy as np
from scipy.stats import poisson
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MASS = np.array([100, 120, 200, 300, 500, 750, 1000, 1500], float)
SIG_E = np.array([1114, 595.6, 98.69, 21.52, 2.564, 0.3618, 0.07132, 0.00405])  # fb, LO 14 TeV, N_IC = 1 (T6)


def sigma(m, nic=2, K=1.2):
    return np.exp(np.interp(m, MASS, np.log(SIG_E))) * nic * K


def fill_pattern():
    slots = []
    for b in range(9):
        for tr in range(4):
            slots += [1] * 72
            slots += [0] * (8 if tr < 3 else 38)
    slots += [0] * (3564 - len(slots))
    f = np.array(slots[:3564])
    filled = np.where(f == 1)[0]
    # eligible: empty and at least 2 BX away from any filled slot (cyclic)
    dist = np.full(3564, 10 ** 6)
    for k in filled:
        d = np.abs(np.arange(3564) - k)
        d = np.minimum(d, 3564 - d)
        dist = np.minimum(dist, d)
    elig = (f == 0) & (dist >= 2)
    return f, elig


def eps_live(tau_ns, f, elig, nsamp=400000, rng=np.random.default_rng(3)):
    filled = np.where(f == 1)[0]
    k0 = rng.choice(filled, nsamp)
    t = k0 * 25.0 + rng.uniform(0, 25.0, nsamp) * 0.1 + rng.exponential(tau_ns, nsamp)   # bunch at start of BX
    slot = (np.floor(t / 25.0).astype(np.int64)) % 3564
    return elig[slot].mean()


def s95(B):
    n = int(round(B))
    cls = lambda s: poisson.cdf(n, s + B) / poisson.cdf(n, B) - 0.05
    return brentq(cls, 1e-6, 1e4)


def reach(L_fb, xsec_scale, fstop, live, B, brvis):
    need = s95(B)
    ms = np.linspace(150, 1500, 2000)
    N = sigma(ms) * xsec_scale * L_fb * fstop * live * 0.55 * 0.83 * brvis
    ok = ms[N >= need]
    return (ok.max() if len(ok) else np.nan), need


if __name__ == '__main__':
    f, elig = fill_pattern()
    print(f'schematic fill: {f.sum()} bunches, eligible empty-BX fraction of the orbit {elig.mean():.3f}')
    taus = [25, 50, 100, 200, 500, 1000, 3000, 10000, 100000]
    raw = {t: eps_live(t, f, elig) for t in taus}
    rinf = elig.mean()
    print('tau [ns] : eps_live/eps_live(inf)  ->  eps_live normalised to 0.21 at tau = inf')
    for t in taus:
        print(f'  {t:>7}: {raw[t]/rinf:.3f} -> {0.21*raw[t]/rinf:.3f}')
    print('\n3-event-type expected reach (95 % CL, CLs), N_IC = 2, E singlet; BR_vis 0.4-0.65 -> range')
    cases = [('HL-LHC 3 ab-1, EB+HB f_stop 1 %', 3000, 1.0, 0.01),
             ('HL-LHC 3 ab-1, EB+HB f_stop 0.5 % (x2 low)', 3000, 1.0, 0.005),
             ('HL-LHC 3 ab-1, EB+HB f_stop 2 % (x2 high)', 3000, 1.0, 0.02),
             ('HL-LHC 3 ab-1, full calo f_stop 7.5 %', 3000, 1.0, 0.075),
             ('Run 2 (138 fb-1, 13 TeV), EB+HB f_stop 1 %', 138, 0.82, 0.01),
             ('Run 2+3 (138 @13 + ~250 @13.6 TeV), EB+HB 1 %', 138 * 0.82 / 0.9 + 250, 0.90, 0.01)]
    for live_label, live in [('live 0.21 (tau >> orbit; T6/S v1 assumption)', 0.21),
                             ('live(tau = 100 ns)', 0.21 * raw[100] / rinf),
                             ('live(tau = 500 ns)', 0.21 * raw[500] / rinf)]:
        print(f'\n  [{live_label} = {live:.3f}]')
        for name, L, xs, fs in cases:
            Bs = (0, 10, 230) if 'HL' in name else (0, 10, 80)
            cells = []
            for B in Bs:
                lo, need = reach(L, xs, fs, live, B, 0.4)
                hi, _ = reach(L, xs, fs, live, B, 0.65)
                cells.append(f'B={B}: {lo/1000:.2f}-{hi/1000:.2f} TeV (s95={need:.1f})')
            print(f'    {name:<50s} ' + ' | '.join(cells))
