"""debug: per-attempt log of the fit ladder on the first N b-only toys of a spec (no verdict)."""
import logging, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import p3d_toys as pt, p3d_specs
logging.basicConfig(level=logging.INFO, format='%(message)s'); log = logging.getLogger('dbg')
logging.getLogger('pyhf').setLevel(logging.ERROR); logging.getLogger('pyhf.optimize.mixins').setLevel(logging.CRITICAL)
st = pt.parse_settings('-'); pt.set_backend(st['tol'])
eng = pt.Engine(p3d_specs.get(sys.argv[1]), st); ex = eng.ex
mu = float(sys.argv[2]); N = int(sys.argv[3]); e = int(sys.argv[4])
rng = np.random.default_rng(np.random.SeedSequence([20261124, e, pt.mu_key(mu)]))
n, lam, th = eng.draw(0.0 if e == 0 else mu, N, rng, 1.0)
names = list(eng.cfg.par_order)
for i in range(N):
    gen = eng.gen_pars(0.0 if e == 0 else mu, lam[i], th[i])
    d = eng.tl.astensor(eng.data(n[i], ex.m))
    msg = [f'toy {i}: n {n[i]} th_gen trend {th[i][ex.nk.index("trend")]:.2f}']
    for lab, m_ in (('fix', mu), ('free', None)):
        for sl, s0 in (('gen', gen), ('def', eng.default_init(ex.m, mu))):
            for meth in eng.METHODS:
                r = eng.fit1(d, m_, s0.copy(), meth)
                if r is None:
                    msg.append(f'  {lab} {sl} {meth}: exception'); continue
                nd = eng.newton(r[0], d, m_ is not None)
                atb = [names[j] for j in range(len(r[0])) if (r[0][j]-eng.bounds[j,0]) <= 1e-6*(eng.bounds[j,1]-eng.bounds[j,0]) or (eng.bounds[j,1]-r[0][j]) <= 1e-6*(eng.bounds[j,1]-eng.bounds[j,0])]
                msg.append(f'  {lab} {sl} {meth}: t {r[1]:.8g} newton {nd:.3g} mu {r[0][eng.i_mu]:.4g} at bound {atb}')
    log.info('\n'.join(msg))
