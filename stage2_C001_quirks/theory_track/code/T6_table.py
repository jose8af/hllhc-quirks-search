"""T6: build the production-channel table (N_IC=2, 14 TeV) from figures/T6_xsec_table.txt (LO, per N_IC, run T6_production.py first).
DY channels get the colour-singlet-DY K-factor of research/theory_signal_model.md Sec.2.3 (1.110/1.158/1.254 at 200/500/1000, N_IC-independent);
photon-initiated channels are LO (no K).  Run: python3 code/T6_table.py"""
import os
f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'T6_xsec_table.txt')
rows = {}
for l in open(f):
    if l.startswith('#'): masses = None; continue
    n, v = l.rsplit(' | ', 1); rows[n.strip()] = [float(x) for x in v.split()]
M = [100, 120, 200, 300, 500, 750, 1000, 1500]
K = {200: 1.110, 500: 1.158, 1000: 1.254}
NIC = 2
print('channel | sigma(fb) N_IC=2 at m=200, 500, 1000 GeV')
for n, v in rows.items():
    out = []
    for m in (200, 500, 1000):
        s = v[M.index(m)]*NIC*(K[m] if n.startswith('DY') else 1.0)
        out.append(f'{s:.3g}')
    print(n, '|', ' / '.join(out))
# ratios
for m in (200, 500, 1000):
    i = M.index(m)
    print(m, 'gg(PDF)/DY (E):', rows['gg(PDF, el+inel) E F'][i]/rows['DY E (1,1)-1 F'][i],
          ' L+-L0/L+L-:', rows['DY L+- L0 (W) doublet'][i]/rows['DY L- L+ doublet charged pair'][i],
          ' doublet total/E:', (rows['DY L+- L0 (W) doublet'][i]+rows['DY L- L+ doublet charged pair'][i]+rows['DY L0 L0bar (Z)'][i])/rows['DY E (1,1)-1 F'][i],
          ' triplet total/E:', (rows['DY T+ T- (Y=0 triplet, charged pairs x2 species)'][i]+rows['DY T+- T0 (W) triplet'][i])/rows['DY E (1,1)-1 F'][i],
          ' q2/q1:', rows['DY |q|=2 singlet F'][i]/rows['DY E (1,1)-1 F'][i], ' q3/q1:', rows['DY |q|=3 singlet F'][i]/rows['DY E (1,1)-1 F'][i],
          ' gg(q=2)/DY(q=2):', rows['gg(PDF) |q|=2 F'][i]/rows['DY |q|=2 singlet F'][i])
# exclusive yields
L = 3000.
for m in (200, 300, 500, 750):
    i = M.index(m)
    for k in ('EPA el-el PPS-Ph2 0.01<xi<0.2 S2=0.8', 'EPA el-el PPS-Run3 0.02<xi<0.15 S2=0.8'):
        print(m, k, 'sigma(N_IC=2)=%.3g fb  N(3/ab)=%.3g' % (rows[k][i]*NIC, rows[k][i]*NIC*L))
