"""INV item 1 mechanism: L-BFGS-B relative ftol vs the un-offset Poisson NLL at b ~ 1e8 (read-only)."""
import numpy as np
from scipy.optimize import minimize
from acts.stage4.analysis import stats as ST
s, b, sg = [0.0, 0.01], [75197332.8199878, 87531796.15767252], [0.8336, 1.1245]
nll, nA = ST._model(s, b, [{}, {}], sg); n = np.asarray(b); aux = np.zeros(nA)
const = float(np.sum(n - n * np.log(n)))
for mu in (2e6, 2e7, 1e8, 1e9):
    f = lambda a: nll(mu, a, n, aux)
    r = minimize(f, aux.copy(), method='L-BFGS-B', bounds=[(-5, 5)] * nA)
    r2 = minimize(lambda a: f(a) - const, aux.copy(), method='L-BFGS-B', bounds=[(-5, 5)] * nA)
    r3 = minimize(f, aux.copy(), method='L-BFGS-B', bounds=[(-5, 5)] * nA, options=dict(ftol=1e-15))
    print(f'mu={mu:.0e} |nll|={abs(r.fun):.3e} ftol*|nll|={2.22e-9*abs(r.fun):.2f}  frozen: alpha_G={r.x[1]:+.5f} nit={r.nit} '
          f'q={2*(r.fun-f(aux)):+.3f} | offset: alpha_G={r2.x[1]:+.5f} nit={r2.nit} q_gain={2*(r2.fun+const-f(aux)):+.3f} '
          f'| ftol=1e-15: alpha_G={r3.x[1]:+.5f}')
    print('   frozen qtilde =', round(ST.qtilde_asimov(mu, s, b, [{}, {}], sg), 4))
