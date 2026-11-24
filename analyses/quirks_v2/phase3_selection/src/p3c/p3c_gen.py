"""p3c_gen.py -- generator-level summaries for the MET model of B4-b (Phase 3, work package p3-c, executor Birgit).

  <acts python> p3c_gen.py <process> <out.npz> <n_events> <stream> <chunk>

Pythia 8 (CP5, 14 TeV, MPI + hadronisation, decay settings of the chain), NO truth-MET filter, no detector chain.
Background and validation processes only (no signal process exists in this script).
Processes (PROC): znn, ztt, zll (Z+parton, pT-hat > 80 GeV, biased pT-hat^4), mjw (multijets, pT-hat > 100, biased
pT-hat^5), mjs0..mjs4 (multijets, unweighted pT-hat slices), zmm (inclusive Z -> mu mu, validation), tt (inclusive
tt-bar, validation).

Per event (same definitions as the pilot summaries of p2c_hs0 / p2x_hs0, so one model code reads both):
  evt (n, len(EVT_COLS))
  jets (J, 4), jet_off     SlowJet anti-kT 0.4 on the visible final state, pT > 20 GeV, |eta| < 4.7: pT, eta, phi, m
  lep (L, 6), lep_off      final e, mu (pT > 5) and gamma (pT > 10), |eta| < 5: pdg, pT, eta, phi, iso(dR<0.3), prompt
meta: sigma_gen [mb] and its error, sum of weights, tries, seeds, code hashes.
"""
import hashlib
import json
import logging
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import pythia8

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[2]
CP5 = QV2 / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat'
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p3c_gen')

ZJ = ["WeakBosonAndParton:qqbar2gmZg = on", "WeakBosonAndParton:qg2gmZq = on", "WeakZ0:gmZmode = 2", "23:onMode = off"]
BIAS4 = ["PhaseSpace:bias2Selection = on", "PhaseSpace:bias2SelectionPow = 4.", "PhaseSpace:bias2SelectionRef = 200."]
QCD = ["HardQCD:all = on"]
SLICES = [(100., 200.), (200., 400.), (400., 800.), (800., 1600.), (1600., -1.)]
PROC = {
    'znn': ZJ + ["23:onIfAny = 12 14 16", "PhaseSpace:pTHatMin = 80."] + BIAS4,
    'ztt': ZJ + ["23:onIfAny = 15", "PhaseSpace:pTHatMin = 80."] + BIAS4,
    'zll': ZJ + ["23:onIfAny = 11 13", "PhaseSpace:pTHatMin = 80."] + BIAS4,
    'mjw': QCD + ["PhaseSpace:pTHatMin = 100.", "PhaseSpace:bias2Selection = on", "PhaseSpace:bias2SelectionPow = 5.",
                  "PhaseSpace:bias2SelectionRef = 300."],
    'zmm': ["WeakSingleBoson:ffbar2gmZ = on", "WeakZ0:gmZmode = 2", "23:onMode = off", "23:onIfAny = 13",
            "PhaseSpace:mHatMin = 60."],
    'tt': ["Top:gg2ttbar = on", "Top:qqbar2ttbar = on"],
}
for _k, (_a, _b) in enumerate(SLICES):
    PROC[f'mjs{_k}'] = QCD + [f"PhaseSpace:pTHatMin = {_a}", f"PhaseSpace:pTHatMax = {_b}"]
BASE = ["Beams:eCM = 14000.", "ParticleDecays:limitTau0 = on", "ParticleDecays:tau0Max = 1000.", "211:mayDecay = off",
        "321:mayDecay = off", "13:mayDecay = off", "130:mayDecay = off", "Print:quiet = on", "Next:numberCount = 0",
        "PartonLevel:MPI = on", "Random:setSeed = on"]
EVT_COLS = ['weight', 'pthat', 'met_x', 'met_y', 'px_eta5', 'py_eta5', 'sumet_eta5', 'sumpt_eta5', 'n_final_vis',
            'n_tau', 'n_tau_had', 'px_all', 'py_all']
HADRON_OK = (2101, 2103, 2201, 2203, 1103, 3101, 3103, 3201, 3203, 3303)


def qv2_seed(stream, chunk, mod=900_000_000):
    s = f'qv2|{stream}|{chunk}'
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % mod


def dphi(a, b):
    return (a - b + math.pi) % (2 * math.pi) - math.pi


def hadron_ancestor(ev, k):
    """As gen_d123.hadron_ancestor (v1): True if any ancestor of particle k is a hadron."""
    seen = set(); stack = [k]
    while stack:
        j = stack.pop()
        if j in seen or len(seen) > 400:
            continue
        seen.add(j)
        p = ev[j]
        for m in (p.mother1(), p.mother2()):
            if m <= 2 or m == j:
                continue
            if 100 < ev[m].idAbs() < 10_000_000 and ev[m].idAbs() not in HADRON_OK:
                return True
            stack.append(m)
    return False


def summary(py, sj):
    ev = py.event
    mx = my = 0.0; s5x = s5y = et5 = pt5 = 0.0; ax = ay = 0.0; nvis = 0
    vis = []; cand = []
    for k in range(ev.size()):
        p = ev[k]
        if not p.isFinal():
            continue
        a = p.idAbs()
        if a in (12, 14, 16):
            mx += p.px(); my += p.py()
            continue
        nvis += 1
        pt = p.pT(); eta = p.eta()
        ax += p.px(); ay += p.py()
        if abs(eta) < 5.0:
            s5x += p.px(); s5y += p.py(); pt5 += pt
            pa = p.pAbs()
            et5 += p.e() * pt / pa if pa > 0 else 0.0
            if a in (11, 13, 22) and pt >= (10.0 if a == 22 else 5.0):
                cand.append(k)
        vis.append((pt, eta, p.phi()))
    lep = []
    for k in cand:
        p = ev[k]
        iso = sum(q[0] for q in vis if 0 < math.hypot(q[1] - p.eta(), dphi(q[2], p.phi())) < 0.3)
        lep.append((p.id(), p.pT(), p.eta(), p.phi(), iso, 0.0 if hadron_ancestor(ev, k) else 1.0))
    sj.analyze(ev)
    jets = [(sj.pT(i), sj.p(i).eta(), sj.phi(i), sj.m(i)) for i in range(sj.sizeJet())]
    ntau = nth = 0
    for k in range(ev.size()):
        p = ev[k]
        if p.idAbs() != 15 or p.daughter1() <= 0 or ev[p.daughter1()].idAbs() == 15:
            continue
        ds = [ev[j].idAbs() for j in range(p.daughter1(), p.daughter2() + 1)]
        ntau += 1; nth += 0 if any(x in (11, 13) for x in ds) else 1
    info = py.infoPython()
    return (info.weight(), info.pTHat(), mx, my, s5x, s5y, et5, pt5, nvis, ntau, nth, ax, ay), jets, lep


def concat(arrs, width):
    off = np.zeros(len(arrs) + 1, np.int64)
    for i, a in enumerate(arrs):
        off[i + 1] = off[i] + len(a)
    if off[-1] == 0:
        return np.zeros((0, width), np.float32), off
    return np.concatenate([np.asarray(a, np.float32).reshape(-1, width) for a in arrs]), off


def run(proc, out, n_events, stream, chunk):
    t0 = time.time()
    seed = qv2_seed(stream, chunk)
    py = pythia8.Pythia("", False)
    py.readFile(str(CP5))
    for line in BASE + PROC[proc] + [f"Random:seed = {seed}"]:
        if not py.readString(line):
            raise RuntimeError(f'bad Pythia line: {line}')
    if not py.init():
        raise RuntimeError('Pythia init failed')
    sj = pythia8.SlowJet(-1, 0.4, 20.0, 4.7, 2, 1)
    evt = np.zeros((n_events, len(EVT_COLS))); jets = []; leps = []
    n_fail = 0; i = 0
    while i < n_events:
        if not py.next():
            n_fail += 1
            if n_fail > 1000 + n_events // 10:
                raise RuntimeError('too many Pythia failures')
            continue
        e, jj, ll = summary(py, sj)
        evt[i] = e; jets.append(jj); leps.append(ll); i += 1
    info = py.infoPython()
    J, joff = concat(jets, 4); L, loff = concat(leps, 6)
    meta = dict(mode='p3c_gen', process=proc, lines=BASE + PROC[proc], stream=stream, chunk=chunk, job_seed=seed,
                n_events=n_events, n_failed_next=n_fail, sigma_gen_mb=info.sigmaGen(), sigma_err_mb=info.sigmaErr(),
                weight_sum=info.weightSum(), n_tried=info.nTried(), n_selected=info.nSelected(),
                n_accepted=info.nAccepted(), evt_cols=EVT_COLS, jet_cols=['pt', 'eta', 'phi', 'm'],
                lep_cols=['pdg', 'pt', 'eta', 'phi', 'iso_dr03', 'prompt'], pythia='8.312 (acts env)',
                code_sha256={Path(__file__).name: hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                             CP5.name: hashlib.sha256(CP5.read_bytes()).hexdigest()},
                t_total_s=round(time.time() - t0, 2))
    outp = Path(out); tmp = outp.with_name(outp.name + '.tmp.npz')
    np.savez_compressed(tmp, meta=np.array(json.dumps(meta)), evt=evt.astype(np.float64), jets=J, jet_off=joff, lep=L,
                        lep_off=loff)
    os.replace(tmp, outp)
    log.info(json.dumps({k: meta[k] for k in ('process', 'n_events', 'sigma_gen_mb', 'sigma_err_mb', 'weight_sum',
                                              't_total_s', 'n_failed_next')}))


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1], int(a[2]), a[3], int(a[4]))
