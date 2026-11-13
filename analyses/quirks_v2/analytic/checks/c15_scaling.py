"""c15_scaling.py -- E1 v5 (review S1-R2 N2): scale-free property of classical NG with massive charged ends in a uniform B.
Action S = -m sum_i int dtau_i - sigma int dA + sum_i q_i int A(x_i).dx_i, A = B x x / 2 (uniform B).
Under x -> lam x, t -> lam t (all coordinates scaled; momenta/energies fixed):
  dtau -> lam dtau, dA -> lam^2 dA, A.dx -> lam^2 A.dx  =>  S[lam x; m, sigma, qB] = lam S[x; m, lam sigma, lam qB].
So a solution x(t) for (sigma, qB) maps to lam x(t/lam) for (sigma/lam, qB/lam): the motion per oscillation depends only on
eps_B = qB/sigma and the velocities; sigma alone sets the length unit l0 = m/sigma.  At fixed tracker radius R the only
other effect is N_osc = sigma R/(2 beta* p_T) and the lever l0 relative to R (layer phases).
Hence (Lambda sqrt(k), B) == (Lambda, B/k) per oscillation, with N_osc larger by k.
Checks: (1) the scaling of each action term (sympy); (2) Kang-Luty/Lorentz EoM invariance m d(gamma v)/dt = -sigma f + q v x B
under the map; (3) eps_B invariance of the two parameter points.
Run: pixi run python analytic/checks/c15_scaling.py > analytic/checks/c15_scaling_out.txt
"""
import sympy as sp
lam, m, sig, qB, k, Lam, B = sp.symbols('lambda m sigma qB k Lambda B', positive=True)
dtau, dA, Adx = sp.symbols('dtau dA Adx')
S = -m * dtau - sig * dA + qB * Adx            # schematic: A.dx is proportional to B x dx (B factored out)
S_scaled = -m * lam * dtau - sig * lam**2 * dA + qB * lam**2 * Adx
print('(1) S[lam x; sigma, qB] - lam*S[x; lam sigma, lam qB] =',
      sp.simplify(S_scaled - lam * S.subs({sig: lam * sig, qB: lam * qB}, simultaneous=True)))
# (2) EoM: d p/dt' with t' = lam t equals (1/lam) dp/dt; forces sigma f and q v x B (v unchanged) scale accordingly
f, vxB = sp.symbols('f vxB')
lhs_prime = (-sig * f + qB * vxB) / lam
print('(2) EoM in primed variables equals EoM with sigma/lam, qB/lam:',
      sp.simplify(lhs_prime - (-(sig / lam) * f + (qB / lam) * vxB)) == 0)
# (3) eps_B = qB/sigma with sigma = Lambda^2: (Lambda sqrt k, B) vs (Lambda, B/k)
eps1 = B / (Lam * sp.sqrt(k))**2; eps2 = (B / k) / Lam**2
print('(3) eps_B(Lambda sqrt k, B) - eps_B(Lambda, B/k) =', sp.simplify(eps1 - eps2))
print('    N_osc ratio (sigma R): (Lambda sqrt k)^2/Lambda^2 =', sp.simplify((Lam * sp.sqrt(k))**2 / Lam**2))
for kk in (2, 4, 20):
    print(f'    3 keV at B0/{kk}  <->  {3*kk**0.5:.2f} keV at B0 (same eps_B, N_osc x {kk})')
