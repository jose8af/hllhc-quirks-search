# E3 2026-10-10: audit side-check (not a P1 result). Nonrelativistic orbit in V = sigma*r (m=1, E=1, sigma=1):
# apsidal angle - pi/2 vs angular momentum L; tests for an L ln(1/L) term (near-radial precession log).
# Run: cd theory_track && pixi run python analytic/novelty_sources/E3_apsidal_check.py
# Nonrelativistic V = r (m=1, E such that rmax=1): apsidal angle vs small L; test pi/2 + a L ln(1/L) + b L
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
def aps(L):
    E=1.0  # V=r, rmax solves 2(E-r)-L^2/r^2=0
    f=lambda r: 2*(E-r)-L**2/r**2
    rmin=brentq(f,1e-14,0.5); rmax=brentq(f,0.5,1.0)
    # substitution r = rmin + (rmax-rmin) sin^2 u to remove endpoint singularities
    def g(u):
        r=rmin+(rmax-rmin)*np.sin(u)**2
        dr=2*(rmax-rmin)*np.sin(u)*np.cos(u)
        val=f(r)
        return L/(r**2*np.sqrt(max(val,1e-300)))*dr
    return quad(g,0,np.pi/2,limit=400,epsabs=1e-13,epsrel=1e-12)[0]
Ls=np.array([1e-2,3e-3,1e-3,3e-4,1e-4,3e-5,1e-5])
d=np.array([aps(L)-np.pi/2 for L in Ls])
for L,x in zip(Ls,d): print(f"L={L:.0e}  dphi={x:.6e}  dphi/L={x/L:.4f}  ln(1/L)={np.log(1/L):.3f}")
A=np.vstack([Ls*np.log(1/Ls),Ls]).T
print("fit a,b:",np.linalg.lstsq(A,d,rcond=None)[0])
