"""R1 check 7: spot-check VALIDATION §2 / §4.2 / §5 numbers directly from npz."""
import os, numpy as np
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'data', 'sim', 'npz')
L = lambda n: dict(np.load(os.path.join(D, n + '.npz'), allow_pickle=False))
def wmed(v, w):
    i = np.argsort(v); c = np.cumsum(w[i]); c /= c[-1]; return v[i][np.searchsorted(c, 0.5)]
c = L('E-TRGS_m500'); s = (c['w'] != 0) & (c['pt_pair'] > 200) & (np.abs(c['y_pair']) < 3.5)
print('§2 E500 tail TRGS median g*-1 =', round(wmed(c['gamma_star'][s] - 1, c['w'][s]), 4), ' m(QQ) =', round(wmed(c['m_pair'][s], c['w'][s]), 1))
for n in ('V-MERGE-20_m500', 'E-INC_m500', 'V-MERGE-50_m500', 'V-NJ1_m500', 'V-TUNE-INC_m500'):
    c = L(n); w = c['w']
    print(f'§4.2 {n}: sigma={w.sum():.4f}  f200={w[c["pt_pair"]>200].sum()/w.sum():.4f}  f300={w[c["pt_pair"]>300].sum()/w.sum():.4f}')
c = L('E-INC_m500'); names = [str(x) for x in c['wvar_names']]
for q in ('67.500', '90.000'):
    j = names.index(f'Weight_MERGING={q}'); w = c['wvar'][:, j]
    print(f'§4.2 in-weight qCut {q}: sigma={w.sum():.4f} f200={w[c["pt_pair"]>200].sum()/w.sum():.4f}')
for a, b in (('E-TRG_m500', 'V-TUNE-TRG_m500'), ('E-TRG_m500', 'V-MPI_m500')):
    A, B = L(a), L(b)
    f = lambda C: C['w'][C['pt_pair'] > 200].sum() / C['w'].sum()
    med = lambda C: wmed(C['pt_pair'][C['w'] != 0], C['w'][C['w'] != 0])
    print(f'§5 {a}->{b}: sigma {A["w"].sum():.4f}->{B["w"].sum():.4f} ({100*(B["w"].sum()/A["w"].sum()-1):+.1f}%), f200 {f(A):.4f}->{f(B):.4f}, pT median {med(A):.1f}->{med(B):.1f}')
