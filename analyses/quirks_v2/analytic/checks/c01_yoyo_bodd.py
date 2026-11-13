"""c01_yoyo_bodd.py -- E1 check of NEAR_MISS_IMPULSE.md §2 and §3.1-3.2 (sympy).

Checks
 (1) vacuum yo-yo in the CM frame (T2 §2.1): separation x(t) = 2 l0 [g - sqrt(1 + (rho - t/l0)^2)], t in [0, 2 rho l0]
     (units sigma = 1 time/length in units of l0 = m/sigma); x(0) = x(T/2) = 0, max = l_max = 2(g-1) l0,
     crossing speed of each end = beta*, relative momentum p* = m rho.
 (2) half-period integral  I = int_0^{T/2} x dt = 2 l0^2 [g rho - asinh(rho)]  (rho = g beta).
 (3) angular momentum at the 1st (odd) crossing from the torque  dJ/dt = q r x E  (exact 1st order):
     J_odd = qE_perp I ;  b_odd = J_odd / p* = 2 (qE_perp m / sigma^2) [g - asinh(rho)/rho].
     Limits: non-relativistic -> (4/3) qE m beta*^2/sigma^2 (direct NR computation); m -> inf at fixed velocities
     -> b ~ m (grows), b/l_max fixed; E -> 0 -> 0.
 (4) the B*-force gives no torque on the relative motion for equal masses and opposite charges.
 (5) Li et al. d_E [2002.07503 Eq.V.8] = (2 m qE/Lambda^4) rho asinh(rho) vs the exact b_odd/2 (ratio printed).
 (6) G(gamma*) = 2 [g - asinh(rho)/rho] / (rho artanh beta*)  and its NR limit 4/3.
Run: pixi run python analytic/checks/c01_yoyo_bodd.py > analytic/checks/c01_yoyo_bodd_out.txt
"""
import sympy as sp

t, l0, g, m, sig, qE, u = sp.symbols('t l0 gamma m sigma qE u', positive=True)
rho = sp.sqrt(g**2 - 1)
x = 2 * l0 * (g - sp.sqrt(1 + (rho - t / l0)**2))
T2 = 2 * rho * l0
print('(1) x(0) =', sp.simplify(x.subs(t, 0)), '; x(T/2) =', sp.simplify(x.subs(t, T2)))
print('    x(T/4) = l_max =', sp.simplify(x.subs(t, rho * l0)), ' (expect 2 l0 (gamma-1))')
# speed of each end = (1/2) dx/dt at t=0
v_end = sp.simplify(sp.diff(x, t).subs(t, 0) / 2)
print('    end speed at crossing =', v_end, ' == beta* =', sp.simplify(v_end - rho / g) == 0)
# check the end obeys hyperbolic motion with force sigma (=1 in these units, m = l0): p = m gamma v
xe = x / 2
ve = sp.diff(xe, t)
pe = l0 * ve / sp.sqrt(1 - ve**2)   # m = l0 sigma, sigma = 1
dpdt = sp.diff(pe, t)
print('    dp/dt of each end (expect -1 = -sigma), numeric at (l0=1, gamma=1.28, t=0.1,0.5,1.2):',
      [round(float(dpdt.subs({l0: 1, g: 1.28, t: tv})), 12) for tv in (0.1, 0.5, 1.2)])

# (2) half-period integral
I = sp.integrate(x.subs(t, l0 * (rho - u)) * l0, (u, -rho, rho))   # t = l0 (rho - u), dt = -l0 du
I = sp.simplify(I)
I_claim = 2 * l0**2 * (g * rho - sp.asinh(rho))
print('(2) int x dt =', I, ';  claim 2 l0^2 (g rho - asinh rho); difference =', sp.simplify(I - I_claim))
for gv in (1.05, 1.28, 2.0, 3.0):
    print(f'    numeric gamma*={gv}: I/l0^2 = {float(I.subs({g: gv, l0: 1})):.6f} vs claim {float(I_claim.subs({g: gv, l0: 1})):.6f}')

# (3) b_odd
p_star = m * rho
b_odd = sp.simplify(qE * I_claim.subs(l0, m / sig) / p_star)
b_claim = 2 * qE * m / sig**2 * (g - sp.asinh(rho) / rho)
print('(3) b_odd = J_odd/p* =', b_odd, '; minus claim =', sp.simplify(b_odd - b_claim))
# NR limit: gamma = 1/sqrt(1-beta^2), beta -> 0
be = sp.symbols('beta', positive=True)
b_nr = sp.series((b_claim / (qE * m / sig**2)).subs(g, 1 / sp.sqrt(1 - be**2)), be, 0, 5).removeO()
print('    NR series of b_odd/(qE m/sigma^2) =', sp.simplify(b_nr), ' (expect 4/3 beta^2 + ...)')
# direct NR computation: mu x'' = -sigma, mu = m/2, relative speed 2 beta
tt = sp.symbols('tt', positive=True)
xnr = 2 * be * tt - sig * tt**2 / m
Th = 2 * be * m / sig
Jnr = qE * sp.integrate(xnr, (tt, 0, Th))
print('    direct NR: J/(p*) =', sp.simplify(Jnr / (m * be)), ' (expect 4/3 qE m beta^2/sigma^2)')
print('    E->0 limit:', sp.limit(b_claim, qE, 0), '; b_odd/l_max (m-independent at fixed gamma):',
      sp.simplify(b_claim / (2 * (g - 1) * m / sig)))

# (4) B* torque: x2 = -x1, v2 = -v1, q2 = -q1 (zeroth order, CM frame)
x1 = sp.Matrix(sp.symbols('x1:4')); v1 = sp.Matrix(sp.symbols('v1:4')); Bs = sp.Matrix(sp.symbols('B1:4'))
q = sp.symbols('q')
F1 = q * v1.cross(Bs); F2 = (-q) * (-v1).cross(Bs)
tau = x1.cross(F1) + (-x1).cross(F2)
print('(4) magnetic torque about CM =', sp.simplify(tau.T), '; force on relative coord (F1-F2)/2 =', sp.simplify(((F1 - F2) / 2).T))

# (5) Li d_E vs exact half offset
dE_li = 2 * m * qE / sig**2 * rho * sp.asinh(rho)
for gv in (1.05, 1.28, 2.0, 3.0):
    r = float((dE_li / (b_claim / 2)).subs({g: gv}))
    print(f'(5) gamma*={gv}: Li d_E / (exact b_odd/2) = {r:.3f}')

# (6) G(gamma*)
G = 2 * (g - sp.asinh(rho) / rho) / (rho * sp.atanh(rho / g))
print('(6) G NR series:', sp.simplify(sp.series(G.subs(g, 1 / sp.sqrt(1 - be**2)), be, 0, 3).removeO()))
for gv in (1.05, 1.28, 1.6, 2.0, 3.0):
    rv = (gv**2 - 1)**0.5
    print(f'    gamma*={gv}: beta*={rv/gv:.4f}, rho={rv:.4f}, [g-asinh(rho)/rho]={float((g - sp.asinh(rho)/rho).subs(g, gv)):.4f}, '
          f'G={float(G.subs(g, gv)):.4f}, ln((g-1)/(g-asinh(rho)/rho))={float(sp.log((g-1)/(g - sp.asinh(rho)/rho)).subs(g, gv)):.4f}')
