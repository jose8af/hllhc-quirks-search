"""Code check of a validate-mode output: basin volumes at R04 only (no R05/R06 ratio printed)."""
import sys
import numpy as np
z = np.load(sys.argv[1])
mp = z['v_map']; V = z['v_V']; nd = z['v_ndbl']; nm = z['v_nmem']; h = z['v_h']; aux = z['v_aux']
for k in (0, 1):
    m = mp == k
    print('map', k, 'n', m.sum(), 'V_R04 median %.3g min %.3g max %.3g' % (np.median(V[m, 0]), V[m, 0].min(), V[m, 0].max()),
          'ndbl mean %.2f' % nd[m].mean(), 'nmem median', np.median(nm[m]), 'h median', np.median(h[m], 0),
          '|S| median', np.median(aux[m, 1]))
print('1/median V (fixed) = %.3g' % (1 / np.median(V[mp == 0, 0])))
