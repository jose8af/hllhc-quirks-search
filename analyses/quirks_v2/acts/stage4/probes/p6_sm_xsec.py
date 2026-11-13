"""p6_sm_xsec.py -- Stage-4 PROBE (E9): LO Pythia8 (CP5, 14 TeV) cross sections of the MET-trigger backgrounds, to size the
required fake rate per triggered event (plan §4.1).  Z(nunu)+jet and W(lnu)+jet (l = e, mu, tau) from 2->2 V+parton with
pTHatMin = 150 GeV; truth MET = |sum pT(neutrinos)| > 200 GeV counted (no detector, no vetoes, no K-factor).  ESTIMATE only.
Run (theory_track/acts): pixi run python stage4/probes/p6_sm_xsec.py [n=3000]   Output: data/acts_stage4/p6/p6_xsec.json"""
import json, sys
from pathlib import Path
import numpy as np
import pythia8
TT = Path(__file__).resolve().parents[3]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
res = {}
for name, lines in {
    'Znunu_j': ["WeakBosonAndParton:qqbar2gmZg = on", "WeakBosonAndParton:qg2gmZq = on", "WeakZ0:gmZmode = 2",
                "23:onMode = off", "23:onIfAny = 12 14 16"],
    'Wlnu_j': ["WeakBosonAndParton:qqbar2Wg = on", "WeakBosonAndParton:qg2Wq = on", "24:onMode = off", "24:onIfAny = 11 13 15"]}.items():
    py = pythia8.Pythia("", False)
    py.readFile(str(TT / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat'))
    for l in ["Beams:eCM = 14000.", "PhaseSpace:pTHatMin = 150.", "Print:quiet = on", "Random:setSeed = on", "Random:seed = 7",
              "PartonLevel:MPI = off", "HadronLevel:all = off"] + lines:
        py.readString(l)
    py.init()
    npass = 0
    for i in range(N):
        if not py.next():
            continue
        ev = py.event
        px = sum(ev[k].px() for k in range(ev.size()) if ev[k].isFinal() and abs(ev[k].id()) in (12, 14, 16))
        pyy = sum(ev[k].py() for k in range(ev.size()) if ev[k].isFinal() and abs(ev[k].id()) in (12, 14, 16))
        npass += (px * px + pyy * pyy) ** 0.5 > 200.
    sig = py.infoPython().sigmaGen() * 1e9   # mb -> pb
    res[name] = dict(sigma_gen_pb_pthat150=sig, f_truthMET_gt200=npass / N, sigma_MET200_pb=sig * npass / N, n=N)
    print(name, res[name])
res['N_3ab_sum'] = sum(v['sigma_MET200_pb'] for v in res.values() if isinstance(v, dict)) * 3e6
res['note'] = 'LO Pythia 2->2, no K-factor, no tt, no multijet, no vetoes; truth MET from neutrinos only. ESTIMATE.'
(TT / 'data' / 'acts_stage4' / 'p6' / 'p6_xsec.json').write_text(json.dumps(res, indent=1))
print('N(3/ab) =', res['N_3ab_sum'])
