"""c11_e2_compare.py -- E1: numbers for NEAR_MISS_IMPULSE.md §9 (comparison with E2's blind numerics).
Evaluates the E1 formulas (unchanged from v1 except where marked post-hoc) at E2's gamma* values:
  b_odd/(eps_perp l_max) = [g - chi/rho]/(g - 1)              (§3.2; chi = artanh beta* = asinh rho)
  A_hat_vac (NG)  = 2(g-1)/(rho chi)                           (log coefficient of §3.4 in E2's normalisation)
  A_hat_vac (KL)  = 2(g-1)(1-beta^2)/(rho beta)                (§4.4 force law, vacuum, b = J/p*)
  kappa           = beta*/chi                                  (§3.4 force law in E2's profile normalisation sigma b/v)
  G, and the per-pair constant G[ln((g-1)/(g-chi/rho)) + K(g)] vs E2's K_o + psi_even (M2b)
  TP-to-TP transfer (post-hoc): Delta Pi/(sigma b/v) = rho beta/((g-1)(1+(g-1)/3))  [rigidly rotating straight string at
      the turning point: J = J_ends + sigma omega l^3/12]
  NR closed forms (post-hoc, c09): psi_even = (2/3 + (4/3) ln 2) eps, psi_odd const = (4/3) ln 3 - 10/3, K_vac,NR = 3 ln 2 - 2.
Run: pixi run python analytic/checks/c11_e2_compare.py > analytic/checks/c11_e2_compare_out.txt
"""
import numpy as np
E2 = {  # gamma*: (A_hat, L/lmax, kappa, TP, b_odd/(eps lmax), A_o, K_o, psi_even, A_hat_SS)
    1.05: (0.996, 0.985, 0.963, 1.92, 1.328, 1.318, -1.91, 1.606, 0.934),
    1.3: (0.951, 0.90, 0.840, 1.61, 1.298, 1.241, -2.01, 1.611, 0.670),
    2.0: (0.878, 0.56, 0.653, 1.15, 1.240, 1.0875, -2.22, 1.646, 0.332),
    3.0: (0.793, 0.43, 0.52, 0.79, 1.189, 0.954, -2.40, 1.696, 0.167)}
KNR = 3 * np.log(2) - 2


def K_fit(g):
    x = np.log(g)
    return KNR - 0.5061 * x - 0.0767 * x * x


print('gamma* | b/(eps lmax) pred/E2 | A_hat pred/E2 | A_hat_KL pred/E2 | kappa pred/E2 | G vs A_o | per-pair const pred/E2 | TP pred/E2 | K - ln(L/lmax)')
for g, (Ah, Lr, ka, tp, bc, Ao, Ko, pe, Ass) in E2.items():
    rho = np.sqrt(g * g - 1); be = rho / g; chi = np.arctanh(be)
    bpred = (g - chi / rho) / (g - 1)
    Ahp = 2 * (g - 1) / (rho * chi)
    Akl = 2 * (g - 1) * (1 - be * be) / (rho * be)
    kap = be / chi
    G = 2 * (g - chi / rho) / (rho * chi)
    const = G * (np.log((g - 1) / (g - chi / rho)) + K_fit(g))
    tpp = rho * be / ((g - 1) * (1 + (g - 1) / 3))
    print(f'{g} | {bpred:.4f}/{bc} | {Ahp:.4f}/{Ah} | {Akl:.4f}/{Ass} | {kap:.4f}/{ka} | {G:.4f}/{Ao} | {const:+.4f}/{Ko + pe:+.4f} | '
          f'{tpp:.3f}/{tp} | K_fit={K_fit(g):+.4f}, ln(L/lmax)_E2={np.log(Lr):+.4f}, implied delta_pair/G = {K_fit(g) - np.log(Lr):+.4f}')
print(f'NR: psi_even/eps = {2/3 + 4/3*np.log(2):.4f} (E2 1.05: 1.606); psi_odd const = {4/3*np.log(3) - 10/3:.4f} (E2 1.05: K_o = -1.91); '
      f'K_vac,NR = {KNR:.4f} (E2: L/lmax -> 1 extrapolated; 1.05: ln 0.985 = -0.015)')
# thickness-level comparisons (E1 c07 vs E2 M3)
pred = {'R500_1keV': (1.072, 1.144, 1.311, 1.455), 'meas500_1keV': (1.073, 1.147, 1.320, 1.460),
        'R1000_1keV': (1 + 0.0998*np.log(2), 1.138, 1.299, 1.437), 'meas1000_1keV': (1.070, 1.141, 1.302, 1.443),
        'R500_3keV': (1 + 0.0846*np.log(2), 1.117, 1.253, 1.371), 'meas500_3keV': (1.066, 1.130, 1.278, None)}
for k in ('500_1keV', '1000_1keV', '500_3keV'):
    print(k, 'pred R(1/2,1/4,1/20,1/80) =', np.round(pred['R' + k], 3), ' meas =', pred['meas' + k])
