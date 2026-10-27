"""r1_derivations.py -- S1-R1 critical reviewer: independent re-derivation of the E1 closed forms (not re-running E1's checks).

(a) Field transformation to the pair rest frame; equal/opposite-charge force bookkeeping for E* and B*.
(b) J_odd = q|E*perp| * int_0^{T_h} x dt, b_odd = J_odd/p*; NR limit; ratio to Li's d_E (2002.07503 Eq.V.8, A.13 at g=1)
    and to Kang-Luty Eq.5.64 scale.
(c) G(gamma*) = sigma b_odd/(p* artanh beta* eps); NR expansion.  NR closed form eta_NR = (4/3)eps[ln(6/eps) - 2]
    checked with an INDEPENDENT high-precision integration of the NR straight-string two-body problem
    (relative coordinate: r'' = -r/|r| + eps y_hat, units mu = sigma = 1, v0 = 1), apocentre-to-apocentre axis angle.
(d) c = 1/(L+K) and exponents; the convention issue of the literal form Ds ~ eps_B [1 + c ln(Lambda^2/qB)].
Run: pixi run python analytic/review/r1_checks/r1_derivations.py > analytic/review/r1_checks/r1_derivations_out.txt
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

print('=== (a) field transformation (E = 0 in the lab) ===')
g, bx, by, bz, Bx, By, Bz = sp.symbols('gamma b_x b_y b_z B_x B_y B_z', real=True)
beta = sp.Matrix([bx, by, bz]); Bv = sp.Matrix([Bx, By, Bz]); Ev = sp.zeros(3, 1)
b2 = (beta.T * beta)[0]
# general boost: E' = g(E + beta x B) - g^2/(g+1) beta (beta.E);  B' = g(B - beta x E) - g^2/(g+1) beta (beta.B)
Ep = g * (Ev + beta.cross(Bv)) - g ** 2 / (g + 1) * beta * (beta.T * Ev)[0]
Bp = g * (Bv - beta.cross(Ev)) - g ** 2 / (g + 1) * beta * (beta.T * Bv)[0]
E1_Bp = g * Bv - (g - 1) * beta * (beta.T * Bv)[0] / b2
diffB = sp.simplify((Bp - E1_Bp).subs(g, 1 / sp.sqrt(1 - b2)))
print('E* = gamma beta x B :', sp.simplify(Ep - g * beta.cross(Bv)) == sp.zeros(3, 1))
print("B* = gamma B - (gamma-1)(B.bhat)bhat :", diffB == sp.zeros(3, 1))
# sign check by force: a charge at rest in the moving frame moves with beta in the lab, force q beta x B (lab);
# transverse force transforms F'_perp = gamma F_perp -> q E'_perp = gamma q (beta x B) : consistent with E* = gamma beta x B.
print('force bookkeeping in the rest frame, x2=-x1, v2=-v1, q2=-q1:')
q, x1, v1, Es, Bs = sp.symbols('q x1 v1 Es Bs')
X1 = sp.Matrix(sp.symbols('X1x X1y X1z')); V1 = sp.Matrix(sp.symbols('V1x V1y V1z'))
Esv = sp.Matrix(sp.symbols('Ex Ey Ez')); Bsv = sp.Matrix(sp.symbols('Bsx Bsy Bsz'))
F1 = q * (Esv + V1.cross(Bsv)); F2 = -q * (Esv + (-V1).cross(Bsv))
print('  F1 + F2 (CM force)      =', sp.simplify(F1 + F2).T, ' -> E* cancels, B* adds (CM shake)')
print('  F1 - F2 (relative force) =', sp.simplify(F1 - F2).T, ' -> only E* acts on the relative motion')
tau = X1.cross(F1) + (-X1).cross(F2)
print('  torque about CM          =', sp.simplify(tau).T, ' -> = q (x1-x2) x E*, no B* torque (linear order)')

print()
print('=== (b) b_odd ===')
t, l0, rho = sp.symbols('t ell_0 rho', positive=True)
gam = sp.sqrt(1 + rho ** 2)
x = 2 * l0 * (gam - sp.sqrt(1 + (rho - t / l0) ** 2))
I = sp.simplify(sp.integrate(x, (t, 0, 2 * rho * l0)))
print('I = int_0^{T_h} x dt =', sp.simplify(I), '; target 2 l0^2 (gamma rho - asinh rho):',
      sp.simplify(I - 2 * l0 ** 2 * (gam * rho - sp.asinh(rho))) == 0)
eps, m, sig = sp.symbols('epsilon m sigma', positive=True)
# J_odd = q|E*perp| I = eps sigma I ; p* = m rho ; l0 = m/sigma
b_odd = sp.simplify((eps * sig * I / (m * rho)).subs(l0, m / sig))
target = 2 * eps * (m / sig) * (gam - sp.asinh(rho) / rho)
print('b_odd = eps sigma I/p* equals 2 eps l0 [gamma - asinh(rho)/rho]:', sp.simplify(b_odd - target) == 0)
nr = sp.series((gam - sp.asinh(rho) / rho), rho, 0, 6).removeO()
print('gamma - asinh(rho)/rho series:', sp.expand(nr), ' -> NR b_odd = (4/3) eps l0 beta^2 = (4/3) qE m beta^2/sigma^2')
# Li d_E = (2 m q E/Lambda^4) rho asinh(rho) = z^-_o0(1), z^- = (z1 - z2)/2 [2002.07503 Eq.II.18]: compare with b_odd/2
ratio = (2 * rho * sp.asinh(rho)) / (gam - sp.asinh(rho) / rho)
for gs in (1.05, 1.28, 2.0, 3.0):
    r_ = np.sqrt(gs ** 2 - 1)
    print(f'  gamma*={gs}: d_E/(b_odd/2) = {float(ratio.subs(rho, r_)):.3f}; 2[g - asinh rho/rho] = '
          f'{2 * (gs - np.arcsinh(r_) / r_):.3f}')
print('  NR limit of d_E/(b_odd/2):', sp.limit(ratio, rho, 0))
# Li A.13 at g=1 (as parsed): (mqE/L^4)[sqrt(1+r^2) - sqrt(1+r^2(1-2g)^2) - r(1-2g)(asinh r - asinh(r(1-2g)))]
gg = sp.symbols('g')
zA13 = sp.sqrt(1 + rho ** 2) - sp.sqrt(1 + rho ** 2 * (1 - 2 * gg) ** 2) - rho * (1 - 2 * gg) * (sp.asinh(rho) - sp.asinh(rho * (1 - 2 * gg)))
print('  Li A.13 (parsed) at g=0:', sp.simplify(zA13.subs(gg, 0)), ', at g=1:', sp.simplify(zA13.subs(gg, 1)),
      '(= 2 rho asinh rho -> Eq.V.8)')
# NR free-particle check of A.13: z = qE t^2/(2m) at t = T_h = 2 m beta/sigma -> 2 qE m beta^2/sigma^2 = (2mqE/L^4) rho^2
print('  KL Eq.5.64 scale: Delta r ~ (v_cm B/m)(m/Lambda^2)^2 = q v_cm B m/sigma^2 = b_odd/(2[g-asinh rho/rho] sin(alpha) gamma_cm-factors)')

print()
print('=== (c) G(gamma*) ===')
b = sp.symbols('beta', positive=True)
G = 2 * (gam - sp.asinh(rho) / rho) / (rho * sp.atanh(b))
Gb = sp.simplify(G.subs(rho, b / sp.sqrt(1 - b ** 2)))
print('G NR series:', sp.series(Gb, b, 0, 4))
for gs in (1.05, 1.28, 1.3, 1.6, 2.0, 3.0):
    bb = np.sqrt(1 - 1 / gs ** 2); r_ = gs * bb
    print(f'  G({gs}) = {2 * (gs - np.arcsinh(r_) / r_) / (r_ * np.arctanh(bb)):.4f};  '
          f'ln[(g-1)/(g-asinh rho/rho)] = {np.log((gs - 1) / (gs - np.arcsinh(r_) / r_)):+.4f};  '
          f'b_odd/(eps l0) = {2 * (gs - np.arcsinh(r_) / r_):.4f}')
# check that sigma b_odd/(p* artanh beta*) = eps G
expr = sp.simplify((sig * target / (m * rho * sp.atanh(b))) / (eps * G))
print('sigma b_odd /(p* artanh beta*) / (eps G) =', expr)

print()
print('--- independent NR two-body integration (straight string, NR ends) ---')


def rhs(t, s, e):
    x, y, vx, vy = s
    r = np.hypot(x, y)
    return [vx, vy, -x / r, -y / r + e]


def apo(t, s, e):
    return s[0] * s[2] + s[1] * s[3]


apo.direction = -1


def nr_run(e, nper=4):
    t0 = 1e-7
    s0 = [t0 - t0 ** 2 / 2, e * t0 ** 2 / 2, 1 - t0, e * t0]
    sol = solve_ivp(rhs, (t0, 4.0 * nper + 1.0), s0, args=(e,), method='DOP853', rtol=1e-13, atol=1e-17,
                    events=apo, dense_output=True)
    ye = sol.y_events[0]
    ph = np.arctan2(ye[:, 1], ye[:, 0])
    ph = (ph + np.pi / 2) % np.pi - np.pi / 2
    ph = np.unwrap(2 * ph) / 2
    # closest approach near the first (odd) crossing, t ~ 2
    tt = np.linspace(1.98, 2.02, 400001)
    rr = np.hypot(*sol.sol(tt)[:2])
    i = np.argmin(rr)
    return ph, rr[i]


print(' eps      b_1/((2/3)eps)   eta/eps (per period)  K = eta/((4/3)eps) - ln(3/(4 eps))   psi_even/eps (ap1->ap2)  psi_odd/eps (ap2->ap3)')
Ks = []
for e in (1e-6, 3e-6, 1e-5, 3e-5, 1e-4):
    ph, bmin = nr_run(e)
    etas = ph[2:] - ph[:-2]
    eta = np.mean(etas[1:])     # skip the first difference (contains the production transient? no: same J=0 start)
    Kv = eta / (4 / 3 * e) - np.log(3 / (4 * e))
    Ks.append(Kv)
    print(f' {e:7.0e}   {bmin / (2 / 3 * e):.6f}        {eta / e:10.5f}  (spread {np.ptp(etas) / e:.1e})   {Kv:+.5f}'
          f'     {(ph[2] - ph[1]) / e:8.4f}   {(ph[3] - ph[2]) / e:8.4f}')
print(f' 3 ln2 - 2 = {3 * np.log(2) - 2:+.5f};  psi_even NR (E1 c09) = 2/3 + (4/3) ln 2 = {2 / 3 + 4 / 3 * np.log(2):.4f};'
      f'  sign: eta > 0 means rotation toward +E (end of charge +q toward E)')

print()
print('=== (d) c and exponents; convention of the literal form ===')
Lam, Bq, C = sp.symbols('Lambda B C', positive=True)
# per event: Ds = A * (qB/sigma) * [ln(sigma/qB) + C],  C = -ln(g_cm b_T sin a) + ln[(g-1)/(g - asinh/rho)] + K
lnS = sp.log(Lam ** 2 / Bq)
Ds = (Bq / Lam ** 2) * (lnS + C)
dB = sp.simplify(sp.diff(sp.log(Ds), Bq) * Bq)
dL = sp.simplify(sp.diff(sp.log(Ds), Lam) * Lam)
print('d ln Ds/d ln B =', dB, '  = 1 - c with c = 1/(ln(sigma/qB) + C) = 1/(L + K)')
print('d ln Ds/d ln Lambda =', dL, '  = -2 + 2c')
# literal form with a CONSTANT c':  Ds ~ eps_B [1 + c' ln(Lambda^2/qB)]  ->  c' = 1/C, not 1/(L+K)
for lam, cE1 in ((0.6, 0.116), (1.0, 0.104), (3.0, 0.085), (10.0, 0.070)):
    lnsq = 8.397 + 2 * np.log(lam)
    Cv = 1 / cE1 - lnsq
    print(f'  Lambda={lam:4.1f} keV: c_E1 = {cE1:.3f} -> L+K = {1 / cE1:6.2f}, ln(sigma/qB) = {lnsq:6.3f}, '
          f'C = L+K-ln(sigma/qB) = {Cv:5.2f}; literal-form constant c\' = 1/C = {1 / Cv:.2f}; '
          f'B exponent implied by literal form with c=c_E1: {1 - cE1 / (1 + cE1 * lnsq):.3f} (vs 1-c = {1 - cE1:.3f})')
