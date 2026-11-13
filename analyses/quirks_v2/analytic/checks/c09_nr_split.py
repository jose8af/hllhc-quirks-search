"""c09_nr_split.py -- E1 (written after E2's numerics, for NEAR_MISS_IMPULSE.md §9): non-relativistic closed forms for
(a) the vacuum per-crossing axis rotation of a yo-yo with constant angular momentum J (E2's M2a quantity), and
(b) the split of the field-driven rotation per period into the odd-crossing and even-crossing parts as E2 defines them
    (change of the turning-point axis across each crossing; E2 M2b), same method as c05 (mu = sigma = 1, speed v0 at the
    crossing, l_max = v0^2/2).
(a) outer: 2 J int_delta^{v0} dtau/x^2, x = tau (v0 - tau/2) (apocentre at tau = v0), inner as in c05 with fixed b = J/v0.
(b) psi_even = 2 int_0^{v0} J(t)/x^2 dt (J grows from 0 at the even crossing), psi_odd = eta_NR - psi_even.
Run: pixi run python analytic/checks/c09_nr_split.py > analytic/checks/c09_nr_split_out.txt
"""
import sympy as sp

tau, v0, d, R, b, eps, t, w = sp.symbols('tau v0 delta R b epsilon t w', positive=True)
J = b * v0
x = tau * (v0 - tau / 2)
Iout = 2 * J * sp.integrate(1 / x**2, (tau, d, v0))
dR = v0 - sp.sqrt(v0**2 - 2 * R)
Iout_R = sp.series(sp.simplify(Iout.subs(d, dR)), R, 0, 1).removeO()
inner = sp.pi - 2 * b / R + (2 * b / v0**2) * (sp.log(2 * R / b) - 1)
psi_vac = sp.simplify(sp.expand_log(sp.expand(Iout_R + inner - sp.pi), force=True))
print('(a) vacuum per-crossing rotation psi =', psi_vac)
lmax = v0**2 / 2
print('    psi / [(b/l_max) ln(l_max/b)] - 1 =', sp.simplify(sp.expand_log(psi_vac / ((b / lmax) * sp.log(lmax / b)) - 1, force=True)),
      ' -> A_hat = 1, K_vac,NR = ln 8 - 2 = 3 ln 2 - 2 (label corrected 2026-10-17)')
# (b) field split
Jt = eps * (v0 * t**2 / 2 - t**3 / 6)
xt = t * (v0 - t / 2)
psi_even = sp.simplify(2 * sp.integrate(sp.simplify(Jt / xt**2), (t, 0, v0)))
print('(b) psi_even/eps =', sp.nsimplify(sp.simplify(psi_even / eps)), '=', float(psi_even / eps), '  (E2 M2b at gamma*=1.05: 1.606)')
eta = sp.Rational(4, 3) * eps * (sp.log(6 / eps) - 2)
psi_odd = sp.expand(sp.expand_log(eta - psi_even, force=True))
print('    psi_odd/eps =', sp.simplify(psi_odd / eps), '; constant =', float((psi_odd / eps).subs(eps, 1)),
      '  (E2 M2b at 1.05: 1.318 ln(1/eps) - 1.91)')
bodd = sp.Rational(2, 3) * eps * v0**2
law_at_bodd = (bodd / lmax) * sp.log(lmax / bodd)
dodd = sp.simplify(sp.expand_log((psi_odd - law_at_bodd) / eps, force=True))
print('    odd non-log offset (psi_odd - vacuum law at b_odd)/eps =', dodd, '=', float(dodd), '  (E2 at 1.05: -1.561 +- 0.02)')
print('    pair residual (psi_odd + psi_even - vacuum law)/eps =', sp.simplify(dodd + psi_even / eps), '=',
      float(dodd + psi_even / eps), ' = (4/3)(3 ln2 - 2)  (E2 at 1.05: +0.04)')
