"""patch_ptqq_cut.py -- insert a generator-level cut pT(QQbar) > PTMIN into SubProcesses/dummy_fct.f of a MadGraph
output directory (sim/mg_out/..., never the MG install).  pT(QQbar) is computed as |sum of pT of all final-state
particles that are not jets| (in our processes the only non-jet final-state particles are the two quirks), so
0-jet subprocesses get zero cross section and the 1/2-jet ME carry the recoil.
Usage: python scripts/patch_ptqq_cut.py <mg_out_dir> <PTMIN_GeV>
"""
import os, sys
d, ptmin = sys.argv[1], float(sys.argv[2])
f = os.path.join(d, 'SubProcesses', 'dummy_fct.f')
t = open(f).read()
marker = '      dummy_cuts=.true.\n'
assert t.count(marker) == 1, 'unexpected dummy_fct.f layout (already patched?)'
decl = ('c     E4 quirk patch: pT(QQbar) generation cut\n'
        '      integer iq\n      double precision pxq, pyq, ptqqmin\n'
        f'      parameter (ptqqmin = {ptmin:.4f}d0)\n')
body = ('      dummy_cuts=.true.\n'
        '      pxq = 0d0\n      pyq = 0d0\n'
        '      do iq = nincoming+1, nexternal\n'
        '         if (.not.is_a_j(iq)) then\n'
        '            pxq = pxq + p(1,iq)\n            pyq = pyq + p(2,iq)\n'
        '         endif\n      enddo\n'
        '      if (pxq**2 + pyq**2 .lt. ptqqmin**2) dummy_cuts=.false.\n')
anchor = '      COMMON /TO_SPECISA/IS_A_J,IS_A_A,IS_A_L,IS_A_B,IS_A_NU,IS_HEAVY,\n     . IS_A_ONIUM, do_cuts\n'
assert t.count(anchor) == 1
t = t.replace(anchor, anchor + decl).replace(marker, body)
open(f, 'w').write(t)
print('patched', f, 'ptqqmin =', ptmin)
