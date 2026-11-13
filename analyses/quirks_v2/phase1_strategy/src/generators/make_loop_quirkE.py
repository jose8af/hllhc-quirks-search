"""make_loop_quirkE.py -- build a loop-capable UFO `loop_quirkE` = MG's bundled loop_sm (NLO QCD UV/R2 counterterms)
+ the v1 quirk states E (xe, Dirac, PDG 9000011) and Etilde (sxe, complex scalar, PDG 9000013), hypercharge-only couplings
copied verbatim from the v1 hand-written UFO (TT/sim/models/quirkE: parameters.py l.500-545, couplings.py l.445-470,
vertices.py l.930-975).  The quirks are colour singlets, so they enter no QCD loop: no new counterterm is needed for
NLO QCD of p p > xe+ xe- (DY-like; the QCD corrections live on the q qbar V vertex already in loop_sm).
Feasibility tool (executor Basil, quirks v2 Phase 1).  Usage: python3 make_loop_quirkE.py <MG5_DIR> <out_dir>
"""
import os
import re
import shutil
import sys

mg, out = sys.argv[1], sys.argv[2]
src = os.path.join(mg, 'models', 'loop_sm')
if os.path.exists(out):
    shutil.rmtree(out)
shutil.copytree(src, out, ignore=shutil.ignore_patterns('*.pyc', '__pycache__', '*.pkl'))

PARAMS = '''
# ---- quirk additions (copied from v1 TT/sim/models/quirkE/parameters.py) ----
MXE = Parameter(name = 'MXE', nature = 'external', type = 'real', value = 500., texname = 'M_E',
                lhablock = 'MASS', lhacode = [ 9000011 ])
MSXE = Parameter(name = 'MSXE', nature = 'external', type = 'real', value = 501., texname = 'M_{\\\\tilde{E}}',
                 lhablock = 'MASS', lhacode = [ 9000013 ])
WXE = Parameter(name = 'WXE', nature = 'external', type = 'real', value = 0., texname = '\\\\Gamma_E',
                lhablock = 'DECAY', lhacode = [ 9000011 ])
WSXE = Parameter(name = 'WSXE', nature = 'external', type = 'real', value = 0., texname = '\\\\Gamma_{\\\\tilde{E}}',
                 lhablock = 'DECAY', lhacode = [ 9000013 ])
QXE = Parameter(name = 'QXE', nature = 'internal', type = 'real', value = '-1.', texname = 'Q_E')
'''
PARTS = '''
# ---- quirk additions (copied from v1 TT/sim/models/quirkE/particles.py) ----
xe__minus__ = Particle(pdg_code = 9000011, name = 'xe-', antiname = 'xe+', spin = 2, color = 1, mass = Param.MXE,
                       width = Param.WXE, texname = 'E^-', antitexname = 'E^+', charge = -1, LeptonNumber = 0,
                       GhostNumber = 0)
xe__plus__ = xe__minus__.anti()
sxe__minus__ = Particle(pdg_code = 9000013, name = 'sxe-', antiname = 'sxe+', spin = 1, color = 1, mass = Param.MSXE,
                        width = Param.WSXE, texname = 'Et^-', antitexname = 'Et^+', charge = -1, LeptonNumber = 0,
                        GhostNumber = 0)
sxe__plus__ = sxe__minus__.anti()
'''
COUPS = '''
# ---- quirk additions (copied from v1 TT/sim/models/quirkE/couplings.py) ----
GC_XEA = Coupling(name = 'GC_XEA', value = 'complex(0,1)*ee*QXE', order = {'QED':1})
GC_XEZ = Coupling(name = 'GC_XEZ', value = '-(complex(0,1)*ee*QXE*sw)/cw', order = {'QED':1})
GC_XEAA = Coupling(name = 'GC_XEAA', value = '2*complex(0,1)*ee**2*QXE**2', order = {'QED':2})
GC_XEAZ = Coupling(name = 'GC_XEAZ', value = '-(2*complex(0,1)*ee**2*QXE**2*sw)/cw', order = {'QED':2})
GC_XEZZ = Coupling(name = 'GC_XEZZ', value = '(2*complex(0,1)*ee**2*QXE**2*sw**2)/cw**2', order = {'QED':2})
'''
VERTS = '''
# ---- quirk additions (copied from v1 TT/sim/models/quirkE/vertices.py; photon is P.A in loop_sm) ----
V_XE_A = Vertex(name = 'V_XE_A', particles = [ P.xe__plus__, P.xe__minus__, P.A ], color = [ '1' ],
                lorentz = [ L.FFV1 ], couplings = {(0,0):C.GC_XEA})
V_XE_Z = Vertex(name = 'V_XE_Z', particles = [ P.xe__plus__, P.xe__minus__, P.Z ], color = [ '1' ],
                lorentz = [ L.FFV1 ], couplings = {(0,0):C.GC_XEZ})
V_SXE_A = Vertex(name = 'V_SXE_A', particles = [ P.A, P.sxe__minus__, P.sxe__plus__ ], color = [ '1' ],
                 lorentz = [ L.VSS1 ], couplings = {(0,0):C.GC_XEA})
V_SXE_Z = Vertex(name = 'V_SXE_Z', particles = [ P.Z, P.sxe__minus__, P.sxe__plus__ ], color = [ '1' ],
                 lorentz = [ L.VSS1 ], couplings = {(0,0):C.GC_XEZ})
V_SXE_AA = Vertex(name = 'V_SXE_AA', particles = [ P.A, P.A, P.sxe__minus__, P.sxe__plus__ ], color = [ '1' ],
                  lorentz = [ L.VVSS1 ], couplings = {(0,0):C.GC_XEAA})
V_SXE_AZ = Vertex(name = 'V_SXE_AZ', particles = [ P.A, P.Z, P.sxe__minus__, P.sxe__plus__ ], color = [ '1' ],
                  lorentz = [ L.VVSS1 ], couplings = {(0,0):C.GC_XEAZ})
V_SXE_ZZ = Vertex(name = 'V_SXE_ZZ', particles = [ P.Z, P.Z, P.sxe__minus__, P.sxe__plus__ ], color = [ '1' ],
                  lorentz = [ L.VVSS1 ], couplings = {(0,0):C.GC_XEZZ})
'''
for fn, add in (('parameters.py', PARAMS), ('particles.py', PARTS), ('couplings.py', COUPS), ('vertices.py', VERTS)):
    p = os.path.join(out, fn)
    txt = open(p).read()
    if fn == 'vertices.py' and 'all_CTvertices' in txt:
        # loop_sm/vertices.py ends with CT-vertex bookkeeping; the additions go before it, after the last tree vertex
        pass
    open(p, 'a').write(add)
for r in [f for f in os.listdir(out) if f.startswith('restrict_')]:
    p = os.path.join(out, r)
    txt = open(p).read()
    txt = re.sub(r'(?im)^(Block MASS[^\n]*\n)', r'\1  9000011 5.000000e+02 # MXE\n  9000013 5.010000e+02 # MSXE\n', txt,
                 count=1)
    txt += '\nDECAY 9000011 0.000000e+00 # WXE\nDECAY 9000013 0.000000e+00 # WSXE\n'
    open(p, 'w').write(txt)
print('wrote', out)
