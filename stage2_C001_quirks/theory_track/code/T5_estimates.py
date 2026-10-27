#!/usr/bin/env python3
"""T5: order-of-magnitude ESTIMATEs used to rank assumption-audit gaps (all ESTIMATE; inputs stated below).
Run from theory_track/:  pixi run python code/T5_estimates.py
Items:
 (1) Lambda-convention conversion factors (lattice: Teper 0912.3339 Eq.33 Tc/sqrt(sigma)=0.597+0.45/N^2; Forsyth-Low sigma=3.6 Lambda'^2).
 (2) Multiple-Coulomb-scattering induced out-of-plane displacement of a quirk in the Phase-2 tracker (not included in ANY
     published quirk propagation except possibly Geant4 in FASER). Highland formula, per-layer x/X0 is an ASSUMPTION (UNVERIFIED).
 (3) Closest approach d_min = L/p of a pair carrying B-field-induced angular momentum (Knapen 1708.02243 Eq.5-7 scaling) vs 1/Lambda:
     tests the 'eps = 0.1 glueball emission per crossing' prescription (needs d <~ 1/Lambda).
 (4) String-causality: light-crossing time of the string vs time a quirk spends inside a sensor; F_ion/Lambda^2.
Natural units conversion: 1 eV^-1 = 1.973e-7 m.
"""
import numpy as np
HBARC_EV_M = 1.973269804e-7  # eV*m
def eV_inv_to_um(x): return x*HBARC_EV_M*1e6

print("(1) Lambda conventions (everything expressed relative to sqrt(sigma))")
for N in (2,3,4,10**6):
    r = 0.597+0.45/N**2
    print(f"  N={N:>7}: Tc/sqrt(sigma)={r:.3f}  -> [2512.20696 'Lambda=Tc'] = {r:.3f} sqrt(sigma); using 0.6 instead of {r:.3f} is a {100*(0.6/r-1):+.0f}% shift in Lambda, {100*((0.6/r)**2-1):+.0f}% in sigma")
print(f"  Forsyth-Low [2504.02940]: sigma=3.6 Lambda'^2 -> Lambda' = {1/np.sqrt(3.6):.3f} sqrt(sigma); 1 keV(sqrt sigma) = {np.sqrt(3.6):.2f} keV(Lambda')")
print(f"  length scale l ~ 1cm (m/100GeV)(keV/Lambda)^2: if Lambda there meant Tc=0.71 sqrt(sigma) (SU(2)) l would be x{1/0.71**2:.2f}; (0.6): x{1/0.36:.2f}")

print("\n(2) Multiple scattering of a quirk crossing Phase-2 tracker layers (Highland)")
def theta0(m_GeV, beta, x_X0):
    g = 1/np.sqrt(1-beta**2); p = m_GeV*beta*g       # GeV
    return 13.6e-3/(beta*p)*np.sqrt(x_X0)*(1+0.038*np.log(x_X0))
for m in (200,500,1000):
  for beta in (0.1,0.2,0.4):
    for x in (0.01,0.03):
      t=theta0(m,beta,x)
      # N layers crossing once each (6 OT + 4 IT assumed), lever arm to the last layer ~ 100 cm; plane through origin forced
      nL=10; R=np.linspace(5,100,nL)
      # displacement of last hit from a plane fixed by the earlier hits: random walk, sum of (theta/2)*(R_last-R_i)  [theta/2: CM direction change when ONE quirk is kicked]
      sig = 0.5*t*np.sqrt(np.sum((R[-1]-R)**2))*1e4  # um
      print(f"  m={m:5} GeV beta_q={beta:.1f} x/X0={x:.2f}/layer: theta0={t*1e3:.3f} mrad ; out-of-plane rms at outer layer ~ {sig:6.0f} um  (Knapen cut ds<100 um [1708.02243 Fig.5])")

print("\n(3) Closest approach with B-induced angular momentum vs 1/Lambda (Knapen Eq.5-7 scaling)")
eB_per_T = (7.7)**2  # eV^2 per Tesla  (e B = 0.2998 GeV/m per T = (7.7 eV)^2)
for m_GeV in (500.,):
  for Lam_keV in (1.,3.,10.,30.,100.):
    for vcm in (0.14,):
        v=0.3                    # internal CM-frame max speed of each quirk
        g=1/np.sqrt(1-v**2); gcm=1/np.sqrt(1-vcm**2)
        m=m_GeV*1e9; Lam=Lam_keV*1e3; B=3.8
        d=(g-1)*m/Lam**2                 # eV^-1, CM amplitude (half-separation)
        dt=2*v*g*m/Lam**2                # eV^-1, period
        tau=2*np.sqrt(eB_per_T*B)**2*gcm*vcm*d   # torque ~ 2 d e E_cm, E_cm = gcm vcm B  (eB in eV^2, d in eV^-1 -> eV)
        L=tau*dt                          # hbar
        p=m*v*g
        dmin=L/p                          # eV^-1
        print(f"  m={m_GeV:.0f} GeV Lambda={Lam_keV:5.0f} keV B=3.8T: amplitude={eV_inv_to_um(d)/1e4:9.3g} cm  L={L:9.3g} hbar  d_min=L/p={eV_inv_to_um(dmin):9.3g} um  d_min*Lambda={dmin*Lam:9.3g}  (need <~1 for glueball emission)")

print("\n(4) String causality / ionisation force")
for Lam in (300.,1000.,3000.):   # eV
    for m_GeV in (100.,500.):
        d_cm = 1.0*(m_GeV/100.)*(1000./Lam)**2     # cm, Kang-Luty amplitude scale
        t_light_ps = d_cm*1e-2/2.998e8*1e12
        for beta in (0.14,):
            t_sensor_ps = 300e-6/(beta*2.998e8)*1e12   # 300 um Si
            print(f"  Lambda={Lam:6.0f} eV m={m_GeV:4.0f} GeV: amplitude~{d_cm:6.2f} cm, string light-crossing {t_light_ps:7.1f} ps vs sensor transit {t_sensor_ps:5.1f} ps (beta={beta}); F_ion/Lambda^2 = ({90.}/{Lam})^2 = {(90./Lam)**2:.3f} (max ionisation ~(90-100 eV)^2 [0805.4642 Sec.3.4])")
