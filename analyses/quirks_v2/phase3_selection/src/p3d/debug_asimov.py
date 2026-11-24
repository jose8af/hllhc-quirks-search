"""debug: Asimov fits on a spec, per start: t values and Newton decrements (no verdict)."""
import logging, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import p3d_toys as pt, p3d_specs
logging.basicConfig(level=logging.INFO, format='%(message)s'); log = logging.getLogger('dbg')
logging.getLogger('pyhf').setLevel(logging.WARNING)
st = pt.parse_settings(sys.argv[2] if len(sys.argv) > 2 else '-'); pt.set_backend(st['tol'])
eng = pt.Engine(p3d_specs.get(sys.argv[1]), st); ex = eng.ex; pyhf = pt.pyhf
lam = np.where(ex.fixed, ex.fixval, ex.m + 1.0)
n = ex.expected(np.array([0.0]), lam[None, :], np.zeros((1, len(ex.nk))))[0]
aux = np.where(ex.fixed, ex.m, ex.m + 1.0)
d = eng.tl.astensor(eng.data(n, aux))
log.info('n %s', n)
for mu in [float(x) for x in sys.argv[3].split(',')]:
    for lab, s0 in (('gen', eng.gen_pars(0.0, lam, np.zeros(len(ex.nk)))), ('default', eng.default_init(aux, mu))):
        s0 = np.clip(s0, eng.bounds[:, 0], eng.bounds[:, 1]); s0[eng.i_mu] = mu
        try:
            pf, tf, pu, tu = eng.two_fits(d, mu, s0)
            n1 = eng.newton(pf, d, True); n2 = eng.newton(pu, d, False)
            g = np.asarray(eng._g(eng.tl.astensor(pf), d)); worst = np.argsort(-np.abs(g))[:3]
            log.info('mu %g %s: t_fix %.6g t_free %.6g q %.4g muhat %.4g newton %.3g %.3g; |grad| top %s', mu, lab, tf, tu,
                     tf - tu, pu[eng.i_mu], n1, n2, [(eng.cfg.par_order[i] if i < len(eng.cfg.par_order) else i, float(g[i]), float(pf[i])) for i in worst])
        except Exception as e:
            log.info('mu %g %s: exception %r', mu, lab, e)
