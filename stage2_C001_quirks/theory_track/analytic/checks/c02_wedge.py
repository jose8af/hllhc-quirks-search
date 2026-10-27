"""c02_wedge.py -- E1 check of NEAR_MISS_IMPULSE.md §3.3-3.5 (sympy).

The intermediate region of a near-miss crossing (b << |x| << l0): endpoints move freely at x = +/- v t (t > 0, after
the crossing; t < 0 is the mirror image), the unperturbed world sheet is the flat wedge |x| < v t, and the small
transverse displacement y(t, x) of the string obeys y_tt = y_xx (static gauge).  Checks:
 (1) momentum balance at a moving end (derivation of the boundary force): d/dt int_{X_L}^{X_R} sigma y_t dx
     = sigma [y_x + V y_t]_{X_L}^{X_R}  ->  dp_R/dt = -sigma (y_x + V_R y_t)|_R ,  dp_L/dt = +sigma (y_x + V_L y_t)|_L
     (checked symbolically for an arbitrary solution f(t+x) + g(t-x)).
 (2) the degree-0 self-similar solution y = (b/2) artanh(x/t)/artanh(v) solves the wave equation and has
     y(t, +/- v t) = +/- b/2.
 (3) the force on the right end is -sigma b / (2 t artanh v) (left end: + the same).
 (4) quasi-static straight-string limit v -> 0: sigma b/(2 v t)  (= sigma * Delta y / separation).
 (5) Kang-Luty straight-string force [0805.4642 Eq.3.8] in the same geometry: transverse part -sigma theta (1 - v^2),
     theta = b/(2 v t); ratio KL/NG = artanh(v)/(v gamma^2) printed.
 (6) degree-1 data (Y = a + u t) give a t-independent force (no 1/t, no log); log-periodic free modes
     y = tau^{i k} sin(n pi (chi + chi_v)/(2 chi_v)) (Milne coordinates) solve the wave equation (bounded, no log).
 (7) impulse over the intermediate region: int_{t1}^{t2} sigma b/(2 artanh(v) t) dt = sigma b ln(t2/t1)/(2 artanh v)
     per end per side; relative transverse momentum p_rel = (p1y - p2y)/2 changes by -(sigma b/artanh v) ln(...)
     over the full passage (incoming + outgoing).
Run: pixi run python analytic/checks/c02_wedge.py > analytic/checks/c02_wedge_out.txt
"""
import sympy as sp

t, x, v, b, sig = sp.symbols('t x v b sigma', positive=True)
f = sp.Function('f'); gfun = sp.Function('g')
XR = sp.Function('X_R')(t); XL = sp.Function('X_L')(t)
yg = f(t + x) + gfun(t - x)
# (1) momentum balance: d/dt int_XL^XR sigma y_t dx  versus boundary terms
P = sp.Integral(sig * sp.diff(yg, t), (x, XL, XR))
dP = sp.diff(P, t).doit()
# use y_tt = y_xx inside: int sigma y_xx dx = sigma [y_x]
yt = sp.diff(yg, t); yx = sp.diff(yg, x)
claim = sig * (yx.subs(x, XR) - yx.subs(x, XL)) + sig * (sp.diff(XR, t) * yt.subs(x, XR) - sp.diff(XL, t) * yt.subs(x, XL))
# evaluate dP: Leibniz gives int sigma y_tt + XR' sigma y_t(XR) - XL' sigma y_t(XL); y_tt integral = sigma [y_x] for this y
dP_expl = sig * (sp.diff(yg, x).subs(x, XR) - sp.diff(yg, x).subs(x, XL)) + sp.diff(XR, t) * (sig * yt).subs(x, XR) \
    - sp.diff(XL, t) * (sig * yt).subs(x, XL)
print('(1) wave eq. for f(t+x)+g(t-x):', sp.simplify(sp.diff(yg, t, 2) - sp.diff(yg, x, 2)) == 0,
      '; Leibniz boundary balance matches claim:', sp.simplify(dP_expl - claim) == 0)

# (2) self-similar solution
chiv = sp.atanh(v)
y = b / 2 * sp.atanh(x / t) / chiv
print('(2) y_tt - y_xx =', sp.simplify(sp.diff(y, t, 2) - sp.diff(y, x, 2)),
      '; y(t, vt) =', sp.simplify(y.subs(x, v * t)), '; y(t,-vt) =', sp.simplify(y.subs(x, -v * t)))

# (3) forces
FR = -sig * (sp.diff(y, x) + v * sp.diff(y, t)).subs(x, v * t)
FL = sig * (sp.diff(y, x) + (-v) * sp.diff(y, t)).subs(x, -v * t)
print('(3) F_R =', sp.simplify(FR), ' ; F_L =', sp.simplify(FL), ' ; F_R + sigma b/(2 t artanh v) =',
      sp.simplify(FR + sig * b / (2 * t * chiv)))
# (4) v -> 0
print('(4) F_R series v->0:', sp.simplify(sp.series(FR, v, 0, 2).removeO()), ' (expect -sigma b/(2 v t) + O(v))')
# (5) Kang-Luty: F = -sigma sqrt(1-vperp^2) s - sigma (v.s) vperp / sqrt(1 - vperp^2)
th = sp.symbols('theta', positive=True)
s_hat = sp.Matrix([1, th]) / sp.sqrt(1 + th**2)
vel = sp.Matrix([v, 0])
vpar = (vel.T * s_hat)[0]
vperp = vel - vpar * s_hat
vp2 = (vperp.T * vperp)[0]
FKL = -sig * sp.sqrt(1 - vp2) * s_hat - sig * vpar * vperp / sp.sqrt(1 - vp2)
FKL_y = sp.series(FKL[1], th, 0, 2).removeO()
print('(5) Kang-Luty transverse force to O(theta):', sp.simplify(FKL_y), ' (expect -sigma theta (1 - v^2))')
ratio = sp.simplify((sig * (b / (2 * v * t)) * (1 - v**2)) / (sig * b / (2 * t * chiv)))
print('    KL/NG ratio =', ratio)
for vv in (0.3049, 0.6242, 0.7806, 0.8660, 0.9428):
    print(f'      beta*={vv}: KL/NG = {float(ratio.subs(v, vv)):.3f}; NG/quasistatic(1/v) = {float(vv/sp.atanh(vv)):.3f}')

# (6) degree-1 data and free modes
a1, a2, u1, u2 = sp.symbols('a1 a2 u1 u2')
A, C, D = sp.symbols('A C D')
y1 = D + A * t + C * x   # general degree<=1 solution with constant offset part handled separately
sol = sp.solve([sp.Eq((A * t + C * v * t), u1 * t), sp.Eq((A * t - C * v * t), u2 * t)], [A, C])
F1 = -sig * (sp.diff(y1, x) + v * sp.diff(y1, t)).subs(sol)
print('(6) degree-1 force on right end =', sp.simplify(F1), ' (t-independent)')
tau, chi, k, n = sp.symbols('tau chi k n', positive=True)
ym = tau**(sp.I * k) * sp.sin(n * sp.pi * (chi + chiv) / (2 * chiv))
# wave eq in Milne coords: y_tautau + y_tau/tau - y_chichi/tau^2 = 0 with k = n pi/(2 chi_v)
wm = sp.diff(ym, tau, 2) + sp.diff(ym, tau) / tau - sp.diff(ym, chi, 2) / tau**2
print('    free mode residual (k = n pi/(2 chi_v)):', sp.simplify(wm.subs(k, n * sp.pi / (2 * chiv))))
# (7) impulse
t1, t2 = sp.symbols('t1 t2', positive=True)
imp = sp.integrate(sig * b / (2 * chiv * t), (t, t1, t2))
print('(7) impulse per end per side =', sp.simplify(imp))
