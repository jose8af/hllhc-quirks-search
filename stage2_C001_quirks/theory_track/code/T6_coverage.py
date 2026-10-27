"""T6: schematic (m_Q, Lambda) coverage map for the E=(1,1)_{-1}, N_IC=2 quirk (Lambda = sqrt(sigma_string)).
Region boundaries are taken from the cited sources or are ESTIMATEs from the T6 report (all schematic, +-factor 2 in Lambda edges).
Run: /opt/miniconda3/envs/root_env/bin/python code/T6_coverage.py  -> figures/T6_coverage.png"""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
C = dict(track='#0072B2', stop='#D55E00', hsc='#009E73', res='#CC79A7', disp='#E69F00', ex='#56B4E9', grey='#888888')
fig, ax = plt.subplots(figsize=(11, 7.2), dpi=150)
ax.set_xscale('linear'); ax.set_yscale('log')
ax.set_xlim(50, 1500); ax.set_ylim(1e-1, 3e7)       # Lambda in eV
def poly(pts, **kw): ax.add_patch(Polygon(pts, closed=True, **kw))
# existing exclusions (observed): FASER (HEPData t2 via theory_signal_model 6.3), D0, LEP
fas = [(57, 300), (72, 500), (113, 1e3), (149, 1.7e3), (163, 3e3), (179, 1e4), (173, 3e4), (71, 1e5)]
poly([(50, 300)] + fas + [(50, 1e5)], fc=C['grey'], alpha=.35, ec='k', lw=.8, zorder=2)
ax.text(55, 3e3, 'FASER\n(excl.)', fontsize=8, va='center')
ax.add_patch(Rectangle((50, 1e4), 57, 9.9e5, fc=C['grey'], alpha=.35, ec='k', lw=.8, zorder=2))
ax.text(52, 3e5, 'D0\n(excl.)', fontsize=8, rotation=90, va='center')
ax.axvline(100, color='k', lw=.8, ls=':'); ax.text(101, 2e7, 'LEP ~100', fontsize=7, va='top')
# HSCP / monojet at low Lambda (Farina-Low 650 GeV @1 eV, 150 @100 eV)
poly([(50, 1), (650, 1), (500, 20), (150, 100), (50, 100)], fc=C['hsc'], alpha=.28, ec=C['hsc'], lw=1.2)
ax.text(300, 4, 'HSCP / monojet recast\n[1703.00912 Tab.II]', color='k', fontsize=8, ha='center')
# Tracker coplanar window (CMS Phase-2 target; ESTIMATE reach 1.1-1.2 TeV)
poly([(110, 600), (1150, 600), (1150, 1.5e4), (110, 1.5e4)], fc=C['track'], alpha=.22, ec=C['track'], lw=1.8, zorder=3)
ax.text(900, 2.5e3, 'CMS Phase-2 tracker:\nnon-helical coplanar hits\n(plane finder 0.6-15 keV; GNN 0.3-0.6 keV)\n[1708.02243, 2410.00269, T-signal-model Sec.4]', fontsize=8, ha='center', va='center', bbox=dict(fc='white', ec='none', alpha=.8))
# merged HIP straight track (Lambda 20 keV - ~3 MeV), existing D0/FASER, HSCP recast TODO
poly([(110, 2e4), (1000, 2e4), (1000, 3e6), (110, 3e6)], fc=C['disp'], alpha=.18, ec=C['disp'], lw=1.2, ls='--')
ax.text(560, 2.2e5, 'merged 2xMIP straight HIP track (CMS HSCP recast: TODO; D0 [1008.3547], FASER <=100 keV)\n+ monojet; vacuum annihilation length > 3 mm below ~3 MeV (ESTIMATE, E-L Eq.4.4)', fontsize=7.5, ha='center', va='center', bbox=dict(fc='white', ec='none', alpha=.8))
# stopped out-of-time annihilation: 0.1 keV .. ~1 MeV (E-L), reach ~0.8 TeV (ESTIMATE f_stop 3-6%)
poly([(110, 100), (800, 100), (800, 1.5e6), (110, 1.5e6)], fc='none', ec=C['stop'], lw=2.0, hatch='/', alpha=.5, zorder=1)
ax.text(640, 160, 'stopped-pair annihilation, out-of-time calo/yoke\n(CMS-like 1801.00359; E-L 1811.08903; reach ~0.7-0.8 TeV, ESTIMATE)', fontsize=8, color='#8a3a00', ha='center', va='bottom', bbox=dict(fc='white', ec='none', alpha=.85))
# displaced annihilation band 0.1 - 3 MeV
ax.text(780, 7.5e5, 'displaced annihilation\n(0.3-3 MeV): no dedicated search', fontsize=8, ha='center', va='center', color='#7a5200')
# prompt resonance: Lambda >~ 3 MeV, mQ < ~0.9 TeV (ESTIMATE vs 1903.06248, 2102.13405)
poly([(50, 3e6), (900, 3e6), (900, 3e7), (50, 3e7)], fc=C['res'], alpha=.3, ec=C['res'], lw=1.5)
ax.text(470, 9e6, 'prompt quirkonium -> ll, gamma gamma, Z gamma at M=2 m_Q\nESTIMATE excluded to m_Q ~ 0.8-1 TeV (S-wave BRs, unverified limits)', fontsize=8.5, ha='center', va='center')
# PPS exclusive strip
ax.add_patch(Rectangle((130, 0.13), 520, 0.45, fc=C['ex'], alpha=.6, ec='k', lw=.8, zorder=4))
ax.text(390, 0.5, 'exclusive gamma gamma -> QQ with PPS-2 tags (any Lambda <~ 100 keV; m_Q 130-650; ~35 evts @500 GeV, 3/ab)', fontsize=7, ha='center', va='top', zorder=5)
# doublet note
ax.text(1480, 0.22, 'Doublet / triplet: Q+- -> Q0 pi+- (c tau ~8 / 60 mm) -> pair neutral & invisible:\nmonojet-like, Lambda-independent (not on this map)', fontsize=7.5, ha='right', va='bottom', color='k')
ax.set_xlabel('quirk mass  m_Q  [GeV]'); ax.set_ylabel(r'$\Lambda\equiv\sqrt{\sigma_{\rm string}}$  [eV]')
ax.set_title('Schematic (m_Q, Lambda) coverage, E=(1,1)_{-1}, N_IC=2, 14 TeV, HL-LHC 3/ab  (edges +-factor 2; T6 report)', fontsize=10)
ax.grid(alpha=.2, which='both')
plt.tight_layout(); plt.savefig('figures/T6_coverage.png')
