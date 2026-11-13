"""T6: stopped-quirk annihilation: dissipation time of the internal (string) energy in dense material and expected
yield of out-of-time annihilations at HL-LHC.  (A first attempt at a full 1D string+friction ODE was dropped: the CM stopping of a
pair with a decreasing stopping-power curve is not captured by a naive 1D toy, so the CM stopped fraction is taken from Evans-Luty
[1811.08903 Fig.2/6] and only the energy-dissipation time and the yield are computed here.)
Model: each quirk (charge 1) has time-uniform momentum in [0,p*] (linear potential) [theory_signal_model.md Sec.4.3];
power per quirk = S(beta)*beta*c with S = Bethe (Bragg-peak-limited, linear below beta=0.02) in brass rho=8.6;
dE_int/dt = -2 <S beta> c ; integrate until beta* < 0.03.  tau is ESTIMATE, independent of Lambda as long as ell > ~1 Angstrom
(Lambda < ~ 24 MeV x sqrt((gamma*-1)/0.3 * m/500GeV)... see report), as in [1811.08903 Sec.3: tau_stop indep. of Lambda for Lambda > 300 eV].
Yield: N = sigma(14 TeV, N_IC=2) * L * f_stop * f_window * eps_reco * BR_vis * eps_veto, f_stop scanned.
Run: python3 code/T6_stopping.py
"""
import numpy as np
ME = 0.511e-3; K = 0.307075e-3; ZA, RHO, IEV = 0.456, 8.6, 320.0
C = 2.99792458e10
def S(beta, bp=0.02):
    b = max(beta, bp)
    L = max(np.log(2*ME*b*b/(1-b*b)/(IEV*1e-9)), 0.6)
    s = K*ZA*RHO/(b*b)*(L - b*b)
    return s if beta >= bp else s*beta/bp
def mean_Sbeta(bstar, n=400):
    bs = np.linspace(1e-3, bstar, n)       # p uniform -> beta ~ p/E ; approximate beta uniform-in-p
    p = bs*np.sqrt(1/(1-bs**2))            # p/m
    ps = np.linspace(1e-3, bstar/np.sqrt(1-bstar**2), n)
    be = ps/np.sqrt(1+ps**2)
    return np.trapezoid([S(b)*b for b in be], ps)/ps[-1]
def tau_diss(m, gstar):
    Eint = 2*m*(gstar-1); t = 0.0; Elim = 2*m*(1/np.sqrt(1-0.03**2)-1)
    n = 0
    while Eint > Elim and n < 100000:
        g = (Eint+2*m)/(2*m); bstar = np.sqrt(1-1/g**2)
        P = 2*mean_Sbeta(bstar)*C          # GeV/s
        dE = min(0.01*Eint, Eint-Elim); t += dE/P; Eint -= dE; n += 1
    return t
if __name__ == '__main__':
    print('S(beta) [GeV/cm, brass]:', {b: round(S(b), 4) for b in (0.02, 0.05, 0.1, 0.3, 0.6)})
    for m, g in ((200, 1.30), (500, 1.25), (1000, 1.19)):
        for gg in (g, 1+(g-1)*0.3, 1+(g-1)*2):
            print(f'm={m} gamma*={gg:.2f} E_int0={2*m*(gg-1):.0f} GeV  tau_diss ~ {tau_diss(m, gg)*1e9:.0f} ns')
    # yield (sigma from T6_xsec_table: N_IC=2 DY E at 14 TeV, use theory_signal_model table values)
    sig = {200: 220., 500: 6.11, 800: 0.66, 1000: 0.197}
    Lum = 3000.; fwin = 0.21; eps_reco = 0.55; eps_veto = 0.877*0.944
    print('N_events(3 ab^-1) = sigma*L*f_stop*0.21*0.55*0.83*BR_vis:')
    for m, s in sig.items():
        row = []
        for fstop in (0.01, 0.03, 0.06):
            for br in (0.4, 0.65):
                row.append(s*Lum*fstop*fwin*eps_reco*eps_veto*br)
        print(m, 'sigma=', s, 'fb ; f_stop=1%(BRvis .4,.65), 3%, 6%:', [round(x, 2) for x in row])
