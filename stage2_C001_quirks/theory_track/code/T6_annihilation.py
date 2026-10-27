"""T6: quirkonium / annihilation numbers for E=(1,1)_{-1}, N_IC=2.
 (a) alpha_IC(m_Q) (1-loop pure SU(2)), (b) S-wave annihilation branching fractions of the stopped/ground-state pair (spin singlet/triplet),
 (c) vacuum annihilation length L_ann (Evans-Luty Eq.4.4) vs Lambda -> where the prompt-resonance regime starts,
 (d) sigma x BR for dilepton / diphoton resonances at M = 2 m_Q vs ATLAS limits (limit values are rough readings, UNVERIFIED).
Run: python3 code/T6_annihilation.py
"""
import numpy as np
HBARC = 1.973269804e-14  # GeV cm
N = 2; alpha = 1/127.9; sw2 = 0.2222; cw2 = 1-sw2
def alpha_IC(m, Lam):  # 1-loop, b0 = 11N/3, alpha = 2 pi/(b0 ln(m/Lam))
    return 2*np.pi/((11*N/3)*np.log(m/Lam))
print('alpha_IC(500 GeV): Lam=1 keV %.4f, 30 keV %.4f, 1 MeV %.4f' % tuple(alpha_IC(500, L) for L in (1e-6, 3e-5, 1e-3)))
# --- BRs (QCD-onium analogy: Gamma(gg)/Gamma(gammagamma) = alpha_s^2 (N^2-1)/(4 N^2 e^4 alpha^2) with N->N_IC)
aIC = alpha_IC(500, 1e-6)
r_IC = aIC**2*(N**2-1)/(4*N**2*alpha**2)           # Gamma(1S0->IC gg)/Gamma(1S0->gamma gamma) , e_Q=1
G_BB_over_gg = 1/cw2**2                            # singlet couples to B only: gg:Zg:ZZ = cw^4 : 2cw^2sw^2 : sw^4
br_gg_s = 1/(G_BB_over_gg + r_IC); br_Zg_s = 2*cw2*sw2/cw2**2*br_gg_s; br_ZZ_s = (sw2**2/cw2**2)*br_gg_s
br_IC_s = r_IC*br_gg_s
print('1S0: Gamma_ICgg/Gamma_gg = %.2f ; BR(gg)=%.3f BR(Z gamma)=%.3f BR(ZZ)=%.3f BR(IC glueballs)=%.3f' % (r_IC, br_gg_s, br_Zg_s, br_ZZ_s, br_IC_s))
# 3S1 -> B* -> f fbar, H H*: weights Y^2 per Weyl fermion, Y^2/4 per complex scalar
Y = {'Q': (6, 1/6), 'u': (3, 2/3), 'd': (3, -1/3), 'L': (2, -1/2), 'e': (1, -1)}
w = {k: n*y*y for k, (n, y) in Y.items()}
tot_f = 3*sum(w.values()); tot = tot_f + 2*0.25*0.25     # + Higgs doublet
w_lep = 3*(w['e'] + w['L']/2)
print('3S1: BR(each charged lepton)=%.3f  BR(ee+mumu)=%.3f  BR(quarks)=%.3f  BR(nu nu)=%.3f  BR(HH*~WW/ZH)=%.3f' % (
    (w['e']+w['L']/2)/tot, 2*(w['e']+w['L']/2)/tot, 3*(w['Q']+w['u']+w['d'])/tot, 3*w['L']/2/tot, 0.125/tot))
fs = 0.25  # statistical singlet fraction
print('spin-averaged (1:3): BR(ee)=BR(mumu)=%.3f, BR(ee+mumu)=%.3f, BR(gamma gamma)=%.3f, BR(Z gamma)=%.3f, visible=%.2f'
      % (0.75*(w['e']+w['L']/2)/tot, 1.5*(w['e']+w['L']/2)/tot, fs*br_gg_s, fs*br_Zg_s, 0.75+fs*(1-br_IC_s)))
# --- (c) L_ann = (beta gamma)_0 (beta gamma)_cm * m*E_int/(eps*Lam^3)
m = 500.; g0 = 1.25; Eint = 2*m*(g0-1); bg0 = np.sqrt(g0**2-1); bgcm = 0.5; eps = 0.1
for Lam in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2):
    L = bg0*bgcm*m*Eint/(eps*Lam**3)*HBARC
    print('Lam=%.0e GeV (%.0f keV): L_ann(vacuum, m=500) = %.3g cm' % (Lam, Lam*1e6, L))
# --- (d) resonance reach.  sigma(pp->E Ebar), N_IC=2, 14 TeV from theory_signal_model Sec2.3
sig = {200: 220., 300: 49., 400: 15.7, 500: 6.11, 600: 2.69, 700: 1.29, 800: 0.660, 1000: 0.197}
BRll = 1.5*(w['e']+w['L']/2)/tot; BRgg = fs*br_gg_s
print('m_Q  M=2m  sigma  sigma*BR(ee+mumu)  sigma*BR(gg)  [fb]  (f_annih=1, A*eps=1)')
for mq, s in sig.items():
    print(mq, 2*mq, s, round(s*BRll, 3), round(s*BRgg, 4))
print('ATLAS dilepton 139/fb: limit 3.6 fb @250 GeV ... 0.014 fb @6 TeV [1903.06248 text]; diphoton: 1.1 fb @400 GeV, 0.03 fb @2.8 TeV [2102.13405 via search snippet]')
