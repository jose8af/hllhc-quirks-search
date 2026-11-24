"""Column names of the B2 counts (p3-b, Casper): cumulative R04-R14, crossing rungs, s = 3 family, FB0-FB4.
Shared by thin_core (numba) and the numpy-only analysis scripts."""
P_MIN = (1e-3, 0.01, 0.05)
COLS = (['R04', 'R05', 'R06', 'R07', 'R08', 'R09', 'R10', 'R11', 'R12', 'R13', 'R14'] +
        ['R04x2S>=%d' % j for j in (1, 2, 3)] + ['R05x2S>=%d' % j for j in (1, 2, 3)] +
        ['R06x2S>=%d' % j for j in (1, 2, 3)] +
        ['R07x2S>=3', 'R08x2S>=3', 'R09x2S>=3'] +
        ['R05xp>%g' % p for p in P_MIN] + ['R06xp>%g' % p for p in P_MIN] +
        ['FB%d' % k for k in range(5)])
NCOL = len(COLS)          # 34
