"""c05_nr_matched.py -- E1: sympy check of the matched-asymptotics derivation of the non-relativistic rotation
per period (NEAR_MISS_IMPULSE.md §4.3):  eta_NR = (4/3) eps [ln(6/eps) - 2],  eps = qE_perp/sigma.

Units mu = 1 (reduced mass), sigma = 1; relative speed at the crossing v0; half period 2 v0; l_max = v0^2/2.
Outer:  theta' = J(t)/x(t)^2,  x = t (v0 - t/2),  J = eps (v0 t^2/2 - t^3/6) on [0, 2 v0], mirrored after the odd
        crossing; integral over one period with |x| > R removed (R = matching radius):
        I_out(R) = (2b/R) + (2b/v0^2)[ln(2 v0^2/R) - 1] + O(R/v0^2),  b = J1/v0 = (2/3) eps v0^2.
Inner:  sweep angle between the two passages through radius R, first order in the potential (radial action
        S = 2 int sqrt(v0^2 - 2r - J^2/r^2) dr, Delta phi = -dS/dJ):
        Delta phi_in(R) = pi - 2 b/R + (2b/v0^2)[ln(2R/b) - 1].
Sum:    eta = (2b/v0^2)[ln(4 v0^2/b) - 2] = (4/3) eps [ln(6/eps) - 2].
Limits printed: eps -> 0 (eta -> 0, eta/eps ~ (4/3) ln(1/eps)); R-independence of the sum.
Run: pixi run python analytic/checks/c05_nr_matched.py > analytic/checks/c05_nr_matched_out.txt
"""
import sympy as sp

t, v0, eps, R, d, w, r, b, J = sp.symbols('t v0 epsilon R delta w r b J', positive=True)
x = t * (v0 - t / 2)
Jt = eps * (v0 * t**2 / 2 - t**3 / 6)
print('J(2 v0) = J1 =', sp.simplify(Jt.subs(t, 2 * v0)), ' (expect 2/3 eps v0^3)')
integrand = sp.simplify(Jt / x**2)
print('J/x^2 =', integrand)
# integral from 0 to 2 v0 - delta, times 2 (mirror)
Iout_d = 2 * sp.integrate(integrand, (t, 0, 2 * v0 - d))
Iout_d = sp.simplify(Iout_d)
ser = sp.series(Iout_d, d, 0, 1).removeO()
print('I_out(delta) small-delta expansion:', sp.simplify(sp.expand(ser)))
# convert delta -> R:  R = delta (v0 - delta/2)  =>  delta = v0 - sqrt(v0^2 - 2R)
dR = v0 - sp.sqrt(v0**2 - 2 * R)
Iout_R = sp.series(Iout_d.subs(d, dR), R, 0, 1).removeO()
bval = sp.Rational(2, 3) * eps * v0**2
claim_out = 2 * bval / R + (2 * bval / v0**2) * (sp.log(2 * v0**2 / R) - 1)
print('I_out(R) - claim =', sp.simplify(sp.expand(Iout_R - claim_out)))

# inner: first-order radial action
S1 = -(2 / v0) * sp.integrate(r**2 / sp.sqrt(r**2 - b**2), (r, b, R))
S1 = sp.simplify(S1)
print('S1(b,R) =', S1)
dphi1 = sp.simplify(sp.diff(-S1, b) / v0)     # Delta phi_1 = -dS1/dJ = -(1/v0) dS1/db
dphi1_ser = sp.series(dphi1.subs(b, sp.Symbol('k') * R), sp.Symbol('k'), 0, 2).removeO()
print('Delta phi_1 (b << R) =', sp.simplify(dphi1_ser.subs(sp.Symbol('k'), b / R)))
claim_in1 = (2 * b / v0**2) * (sp.log(2 * R / b) - 1)
print('Delta phi_1 - claim =', sp.simplify(sp.expand_log(dphi1_ser.subs(sp.Symbol('k'), b / R) - claim_in1, force=True)))
# zeroth order: pi - 2 asin(b/R)
S0 = 2 * sp.integrate(sp.sqrt(v0**2 - J**2 / r**2), (r, J / v0, R))
dphi0 = sp.simplify(-sp.diff(S0, J))
print('Delta phi_0 =', dphi0, ' (expect pi - 2 asin(J/(v0 R)))')

total = sp.pi - 2 * bval / R + claim_in1.subs(b, bval) + claim_out
eta = sp.simplify(sp.expand_log(total - sp.pi, force=True))
print('eta = ', eta)
claim = sp.Rational(4, 3) * eps * (sp.log(6 / eps) - 2)
print('eta - (4/3) eps [ln(6/eps) - 2] =', sp.simplify(sp.expand_log(eta - claim, force=True)))
print('R-dependence of eta:', sp.simplify(sp.diff(eta, R)))
print('numeric K_NR = 3 ln 2 - 2 =', float(3 * sp.log(2) - 2), ' (c04 numerics: 0.079447 at gamma*=1.00001)')
print('limit eps->0 of eta:', sp.limit(claim, eps, 0))
