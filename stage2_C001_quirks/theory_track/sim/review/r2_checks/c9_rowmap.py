"""R2 c9: row map spot-check -- for random TRGS m500 rows (both origins), read LHE event ievt_lhe of chunk `chunk` and compare its
quirk 4-momenta (pid +-9000011) with the stored pre-shower p_qp_hard / p_qm_hard."""
import gzip
import numpy as np
D = '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/data/sim'
c = np.load(f'{D}/npz/E-TRGS_m500.npz')
rng = np.random.default_rng(4)
rows = rng.choice(len(c['w']), 300, replace=False)
need = {}
for r in rows:
    src = 'E-INC' if c['origin'][r] == 1 else 'E-TRG'
    need.setdefault((src, int(c['chunk'][r])), {})[int(c['ievt_lhe'][r])] = r
dev = []; nexact = 0
for (src, k), want in need.items():
    evs = {}
    with gzip.open(f'{D}/lhe/{src}/m500_c{k}.lhe.gz', 'rt') as f:
        i = -1; inev = False; buf = []
        for line in f:
            if line.startswith('<event'):
                i += 1; inev = i in want; buf = []
                continue
            if inev:
                if line.startswith('</event') or line.startswith('<'):
                    if buf:
                        evs[i] = buf; buf = []
                    inev = False if line.startswith('</event') else inev
                    continue
                buf.append(line)
    for ie, r in want.items():
        L = [l.split() for l in evs[ie][1:]]
        P = {int(t[0]): np.array([float(t[9]), float(t[6]), float(t[7]), float(t[8])]) for t in L if abs(int(t[0])) == 9000011}
        pp, pm = P[-9000011], P[9000011]    # p1 = positive quirk = pid < 0
        d = max(np.max(np.abs(pp - c['p_qp_hard'][r])), np.max(np.abs(pm - c['p_qm_hard'][r])))
        dev.append(d); nexact += d < 1e-3
dev = np.array(dev)
print(f'rows checked {len(dev)}: |dp|<1e-3 GeV for {nexact}; max |dp| = {dev.max():.3g} GeV; 99th pct {np.percentile(dev, 99):.3g}')
