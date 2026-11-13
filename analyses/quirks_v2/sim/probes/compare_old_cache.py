import numpy as np
def wq(v, w, qs=(0.16, 0.5, 0.84)):
    i = np.argsort(v); v = v[i]; c = np.cumsum(w[i]); c /= c[-1]
    return [v[min(np.searchsorted(c, q), len(v) - 1)] for q in qs]
old = np.load('data/cache/T2_kinematics_cache.npz')
def oldset(key):
    g = old[key + '_gamma_star']; w = old[key + '_w']; bg = old[key + '_bg_pair']; eta = old[key + '_eta_pair']
    M = 2 * 500 * g; pt = M * bg / np.cosh(eta)
    return dict(g=g, w=w, pt=pt, eta=eta, M=M)
def newset(path):
    c = np.load(path); return dict(g=c['gamma_star'], w=c['w'], pt=c['pt_pair'], eta=c['eta_pair'], M=c['m_pair'])
O_inc = oldset('F_500_incl'); O_isr = oldset('F_500_isr')
N_inc = newset('data/sim/probes/E_m500_mlm_probe.npz'); N_trg = newset('data/sim/probes/E_m500_pt150_probe.npz')
def show(name, d, sel=None):
    s = np.ones(len(d['w']), bool) if sel is None else sel(d)
    w = d['w'] * s
    neff = w.sum() ** 2 / np.sum(w ** 2)
    print(f"{name:42s} Neff={neff:8.0f}  gamma*-1 16/50/84 = " + ' '.join(f'{x-1:.3f}' for x in wq(d['g'], w)) +
          "  M50=%.0f  pT 16/50/84 = %s" % (wq(d['M'], w)[1], ' '.join(f'{x:.0f}' for x in wq(d['pt'], w))))
show('old LO incl (pT=0)', O_inc)
show('MG+PY8 MLM inclusive (probe, 543 ev)', N_inc)
sel = lambda d: (d['pt'] > 200) & (np.abs(d['eta']) < 2.5)
show('old LO V*+jet pT>200 |eta|<2.5', O_isr, sel)
show('MG+PY8 pT(QQ)>150 gen cut; pT>200 |eta|<2.5', N_trg, sel)
show('MG+PY8 MLM inclusive; pT>200 |eta|<2.5', N_inc, sel)
# fraction of inclusive matched sigma with pT(QQ)>200 (after shower)
w = N_inc['w']; print('MG incl: frac sigma with pT(QQ)>200 = %.3f, >150 = %.3f' % (w[N_inc['pt'] > 200].sum() / w.sum(), w[N_inc['pt'] > 150].sum() / w.sum()))
w = N_trg['w']; print('MG trig sample: sigma(pT>200, after shower) = %.4f fb, frac of sample with pT<150 after shower = %.3f' % (w[N_trg['pt'] > 200].sum(), w[N_trg['pt'] < 150].sum() / w.sum()))
