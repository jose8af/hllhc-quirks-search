"""T6: production channels for EW quirks at the LHC: DY (gamma*/Z, W) for singlet/doublet/triplet/multi-charged
representations, and photon-initiated gamma gamma -> Q Qbar (LUXqed inelastic+elastic, EPA elastic with PPS acceptance).
All numbers: LO, per unit N_IC (multiply by N_IC), fb.  PDF: NNPDF31_nnlo_as_0118_luxqed (member 0) for both qqbar and photon.
Run (needs python with lhapdf):  /opt/miniconda3/envs/root_env/bin/python code/T6_production.py
(the repo's pixi env has no lhapdf; LHAPDF 6.5.5 + this PDF set are in /opt/miniconda3/envs/root_env).
Inputs: alpha=1/127.9, sw2=0.2222 (same as research/theory_signal_model.md App.A).  Output: figures/T6_xsec_table.txt and stdout.
"""
import sys, numpy as np, lhapdf
from scipy.integrate import quad
lhapdf.setVerbosity(0)
PDF = lhapdf.mkPDF("NNPDF31_nnlo_as_0118_luxqed", 0)
ALPHA = 1/127.9; SW2 = 0.2222; sw = np.sqrt(SW2); cw = np.sqrt(1-SW2)
MZ, GZ, MW = 91.1876, 2.4952, 80.379
GEV2FB = 0.3894e12
MP = 0.938272

# ---------- partonic cross sections ----------
def beta_of(shat, m): return np.sqrt(max(1-4*m*m/shat, 0.0))
def zc(T3, Q): return (T3 - Q*SW2)/(sw*cw)      # Z coupling (per chirality) in units of e
QUARKS = {1:(-.5,-1/3), 2:(.5,2/3), 3:(-.5,-1/3), 4:(.5,2/3), 5:(-.5,-1/3)}   # |pid|:(T3L,Q)

def sig_nc(shat, m, q, QF, T3F, spin):
    """q qbar -> gamma*/Z* -> F Fbar, F vector-like (same T3F, QF for both chiralities). per N_IC, colour averaged, GeV^-2"""
    b = beta_of(shat, m)
    if b == 0: return 0.0
    T3, Qq = QUARKS[q]
    chi = shat/(shat - MZ**2 + 1j*MZ*GZ)
    gFg, gFz = QF, zc(T3F, QF)
    amp = 0.0
    for T3q in (T3, 0.0):     # L and R quark chirality
        a = Qq*gFg + zc(T3q, Qq)*gFz*chi
        amp += abs(a)**2
    V = 0.5*amp
    pre = 4*np.pi*ALPHA**2/(3*shat)/3.0
    return pre*b*((3-b*b)/2*V) if spin == 'F' else pre*b**3/4*V

def sig_W(shat, m, cF, spin='F'):
    """q qbar' -> W* -> F F'bar, degenerate masses, cF = SU(2) Clebsch (1 doublet, sqrt2 triplet). GeV^-2 (without CKM)"""
    b = beta_of(shat, m)
    if b == 0: return 0.0
    chi = shat/(shat - MW**2)
    a = (1/(np.sqrt(2)*sw))*(cF/(np.sqrt(2)*sw))*chi
    V = 0.5*abs(a)**2       # only left-handed quarks
    pre = 4*np.pi*ALPHA**2/(3*shat)/3.0
    return pre*b*((3-b*b)/2*V) if spin == 'F' else pre*b**3/4*V

def sig_gg(shat, m, QF, spin):
    """gamma gamma -> F Fbar (Breit-Wheeler / scalar QED), GeV^-2, per N_IC"""
    b = beta_of(shat, m)
    if b == 0: return 0.0
    L = np.log((1+b)/(1-b))
    if spin == 'F':
        return 4*np.pi*ALPHA**2*QF**4/shat*((1+4*m*m/shat-8*m**4/shat**2)*L - b*(1+4*m*m/shat))
    return 2*np.pi*ALPHA**2*QF**4/shat*(b*(2-b*b) - 0.5*(1-b**4)*L)

# ---------- parton luminosities on a (ln tau, y) grid ----------
NT, NY = 160, 90
def grid(m, sqrts):
    S = sqrts**2; tau0 = 4*m*m/S
    lt = np.linspace(np.log(tau0)+1e-6, 0.0, NT)
    return S, lt

def pdf_all(x, Q):
    x = min(max(x, 1e-9), 1-1e-9)
    return {pid: PDF.xfxQ(pid, x, Q)/x for pid in (1,2,3,4,5,-1,-2,-3,-4,-5,22)}

def integrate(m, sqrts, kernels, mu_fac=1.0, ycut=None):
    """kernels: dict name -> function(shat, flav_lumi) ; returns sigma [fb] per name.
    flav_lumi(pidA,pidB) gives parton lumi product f_A(x1) f_B(x2) (+ swap handled by caller)"""
    S, lt = grid(m, sqrts)
    res = {k: np.zeros(NT) for k in kernels}
    for i, l in enumerate(lt):
        tau = np.exp(l); shat = tau*S; Q = mu_fac*np.sqrt(shat)
        ymax = -0.5*l
        ys = np.linspace(-ymax, ymax, NY)
        if ycut is not None:
            if ymax < 1e-9: continue
            ys = np.linspace(-min(ymax, ycut), min(ymax, ycut), NY)
        # accumulate lumi integrals over y: need f(x1)f(x2) for pairs -> tabulate
        F1 = []; F2 = []
        for y in ys:
            x1 = np.sqrt(tau)*np.exp(y); x2 = np.sqrt(tau)*np.exp(-y)
            F1.append(pdf_all(x1, Q)); F2.append(pdf_all(x2, Q))
        for k, ker in kernels.items():
            vals = np.array([ker(shat, f1, f2) for f1, f2 in zip(F1, F2)])
            res[k][i] = np.trapezoid(vals, ys)*tau   # d sigma/d ln tau, with tau factor from x1 x2 f f
    return {k: np.trapezoid(v, lt)*GEV2FB for k, v in res.items()}

def make_kernels(m):
    ker = {}
    def dy(QF, T3F, spin):
        def f(shat, f1, f2):
            t = 0.0
            for q in QUARKS:
                t += (f1[q]*f2[-q] + f1[-q]*f2[q])*sig_nc(shat, m, q, QF, T3F, spin)
            return t
        return f
    def dyW(cF):
        def f(shat, f1, f2):
            t = 0.0
            # W+ : u dbar, c sbar ; W- : d ubar, s cbar ; (CKM: Vud^2=.95,Vus^2=.05,Vcs^2=.95,Vcd^2=.05)
            pairs = [(2,-1,.95),(2,-3,.05),(4,-3,.95),(4,-1,.05)]
            for u, d, w in pairs:
                t += w*(f1[u]*f2[d] + f1[d]*f2[u] + f1[-u]*f2[-d] + f1[-d]*f2[-u])
            return t*sig_W(shat, m, cF)
        return f
    def gg(QF, spin):
        def f(shat, f1, f2): return f1[22]*f2[22]*sig_gg(shat, m, QF, spin)
        return f
    ker['DY E (1,1)-1 F'] = dy(-1, 0.0, 'F')
    ker['DY Et scalar'] = dy(-1, 0.0, 'S')
    ker['DY L- L+ doublet charged pair'] = dy(-1, -0.5, 'F')
    ker['DY L0 L0bar (Z)'] = dy(0, 0.5, 'F')
    ker['DY L+- L0 (W) doublet'] = dyW(1.0)
    ker['DY T+ T- (Y=0 triplet, charged pairs x2 species)'] = lambda s, a, b: 2*dy(1, 1.0, 'F')(s, a, b)
    ker['DY T+- T0 (W) triplet'] = dyW(np.sqrt(2))
    ker['DY |q|=2 singlet F'] = dy(-2, 0.0, 'F')
    ker['DY |q|=3 singlet F'] = dy(-3, 0.0, 'F')
    ker['gg(PDF, el+inel) E F'] = gg(1, 'F')
    ker['gg(PDF) Et scalar'] = gg(1, 'S')
    ker['gg(PDF) |q|=2 F'] = gg(2, 'F')
    ker['gg(PDF) L- (doublet charged) F'] = gg(1, 'F')
    return ker

# ---------- elastic photon flux (EPA, dipole form factors) ----------
def flux_el(x):
    """dN/dx of elastic photons from a proton (Budnev et al.), dipole FFs"""
    if x >= 0.5: return 0.0     # flux negligible / EPA invalid; also avoids overflow
    qmin2 = MP**2*x*x/(1-x)
    def integrand(lq2):
        q2 = np.exp(lq2)
        GE = (1+q2/0.71)**-2; GM = 2.79*GE
        FE = (4*MP**2*GE**2 + q2*GM**2)/(4*MP**2+q2); FM = GM**2
        return (1-x)*(1-qmin2/q2)*FE + 0.5*x*x*FM
    v, _ = quad(integrand, np.log(qmin2), np.log(1e4), limit=200)
    return ALPHA/np.pi/x*v

def sigma_el(m, sqrts, spin, QF, xmin=1e-4, xmax=0.5, S2=1.0, nx=220, semi=False):
    """exclusive (both protons intact) gamma gamma -> F Fbar with xi in [xmin,xmax], x_i=xi_i (photon energy fraction)."""
    S = sqrts**2
    x0 = 4*m*m/S
    lo = max(xmin, 1e-12); xs = np.exp(np.linspace(np.log(lo), np.log(xmax), nx))
    fl = np.array([flux_el(x) for x in xs])
    tot = 0.0
    X1, X2 = np.meshgrid(xs, xs, indexing='ij')
    sh = X1*X2*S
    sg = np.vectorize(lambda s: sig_gg(s, m, QF, spin))(sh)
    integ = fl[:, None]*fl[None, :]*sg*xs[:, None]*xs[None, :]      # dx = x dlnx
    val = np.trapezoid(np.trapezoid(integ, np.log(xs), axis=1), np.log(xs))
    return val*GEV2FB*S2

def sigma_semi(m, sqrts, spin, QF, S2=0.5):
    """one proton elastic (EPA), other photon from the LUXqed inelastic-only part ~ (total - elastic): ESTIMATE via integrating over PDF photon"""
    S = sqrts**2; x0 = 4*m*m/S
    xs = np.exp(np.linspace(np.log(x0), 0, 160)); fl = np.array([flux_el(x) for x in xs])
    tot = 0.0
    # x1 elastic (grid), x2 from PDF photon at Q=m ; inelastic part = total - elastic flux (clip at 0)
    out = 0.0
    lx = np.log(xs)
    for i, x1 in enumerate(xs):
        x2s = np.exp(np.linspace(np.log(x0/x1), 0, 120)) if x0/x1 < 1 else None
        if x2s is None: continue
        sh = x1*x2s*S
        gam = np.array([PDF.xfxQ(22, min(x2, 1-1e-9), m)/x2 for x2 in x2s])        # f(x2)
        fel = np.array([flux_el(min(x2, 1-1e-9)) for x2 in x2s])
        inel = np.clip(gam - fel, 0, None)
        sg = np.array([sig_gg(s, m, QF, spin) for s in sh])
        out += np.trapezoid(inel*sg*x2s, np.log(x2s))*fl[i]*x1*(lx[1]-lx[0])
    return 2*out*GEV2FB*S2     # factor 2: either proton elastic

if __name__ == '__main__':
    sq = 14000.
    masses = [100, 120, 200, 300, 500, 750, 1000, 1500]
    rows = {}
    for m in masses:
        r = integrate(m, sq, make_kernels(m))
        r['EPA el-el (S2=1, all xi)'] = sigma_el(m, sq, 'F', 1)
        r['EPA el-el PPS-Ph2 0.01<xi<0.2 S2=0.8'] = sigma_el(m, sq, 'F', 1, 0.0095, 0.2, 0.8)
        r['EPA el-el PPS-Ph2+420m 0.003<xi<0.2 S2=0.8'] = sigma_el(m, sq, 'F', 1, 0.003, 0.2, 0.8)
        r['EPA el-el PPS-Run3 0.02<xi<0.15 S2=0.8'] = sigma_el(m, sq, 'F', 1, 0.02, 0.15, 0.8)
        r['EPA el-el scalar (S2=1, all xi)'] = sigma_el(m, sq, 'S', 1)
        r['EPA el-el scalar 0.02<xi<0.15 (1812.04886-like)'] = sigma_el(m, sq, 'S', 1, 0.02, 0.15, 1.0)
        r['EPA semi-el E F (S2=0.5)'] = sigma_semi(m, sq, 'F', 1)
        rows[m] = r
        print(m, {k: float(f'{v:.4g}') for k, v in r.items()}, flush=True)
    names = list(rows[masses[0]].keys())
    with open(__file__.replace('code/T6_production.py', 'figures/T6_xsec_table.txt'), 'w') as f:
        f.write('# sigma [fb] at 14 TeV, LO, per unit N_IC (x N_IC). columns: ' + ' '.join(map(str, masses)) + '\n')
        for n in names:
            f.write(n + ' | ' + ' '.join(f'{rows[m][n]:.4g}' for m in masses) + '\n')
