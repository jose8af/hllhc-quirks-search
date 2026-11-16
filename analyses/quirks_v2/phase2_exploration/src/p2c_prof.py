"""p2c_prof.py -- where the no-PU hard-scatter event and the Geant4 firing spend their time (cost-reduction study).

  <acts python> p2c_prof.py gen <out.json> <sample> <n_accept> [variant]   generator and filter, timed per step
  <acts python> p2c_prof.py chain <out.json> <sample> <n_events>           p2c_hs0 under cProfile (Python-side shares)
  <acts python> p2c_prof.py g4 <out.json>                                  Geant4 cost per firing: spectrum / geometry / stop

gen: the loop of s4pu.HardScatter.generate re-timed step by step (same event stream).  Per try it records pT-hat,
the neutrino MET of the PROCESS record (hard process + resonance decays, before showers and MPI), the parton-level
neutrino MET (the quantity of the production pre-filter, PRE_MET) and whether the event is kept.  A second generator
instance with PartonLevel:all = off measures the cost of a process-level-only event.
variant 'tt_forced': W+ -> l nu, W- -> hadrons forced in the decay table (one of the two charge-conjugate halves of
"exactly one W -> l nu"); the 1-lepton test is still applied and counted.
"""
import cProfile
import io
import json
import math
import pstats
import sys
import time
from pathlib import Path

import numpy as np

import signal  # noqa: F401  (stdlib module, imported before acts/stage4/analysis/signal.py can shadow it)
import subprocess  # noqa: F401

import p2c_common as C

sys.path.insert(0, str(C.CODE))
sys.path.insert(0, str(C.ANA))
import s4pu  # noqa: E402

log = C.setup_logging('p2c_prof')
CP5 = C.QV2 / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat'
FORCED = ["24:onMode = off", "24:onPosIfAny = 11 13 15", "24:onNegIfAny = 1 2 3 4 5"]


def nu_met(rec):
    mx = my = 0.0
    for k in range(rec.size()):
        p = rec[k]
        if p.isFinal() and abs(p.id()) in (12, 14, 16):
            mx += p.px(); my += p.py()
    return math.hypot(mx, my)


def gen(out, sample, n_acc, variant=''):
    import gen_d123
    import pythia8
    import p2c_hs0
    name = sample
    if variant == 'tt_forced':
        name = 'ttbar_1l_pos'
        s4pu.SM_SAMPLES[name] = (s4pu.SM_SAMPLES['ttbar_1l'][0] + FORCED, 150.0)
    hs = s4pu.HardScatter(CP5, name, tt=C.QV2)
    py = hs.gen.py
    is_tt = sample == 'ttbar_1l'
    T = dict(next=0.0, nlep=0.0, met_parton=0.0, met_process=0.0, hadron=0.0, met_final=0.0, list=0.0, select=0.0,
             summary=0.0)
    tries = []; kept = 0; nfail = 0; n1l_fail = 0; n_pre = 0
    sj20 = pythia8.SlowJet(-1, 0.4, 20.0, 4.7, 2, 1); sj30 = gen_d123.slowjet()
    py.rndm.init(C.qv2_seed('prof.' + name, 0))
    c = time.perf_counter
    t_all = c()
    while kept < n_acc:
        t0 = c(); ok = py.next(); T['next'] += c() - t0
        if not ok:
            nfail += 1; continue
        ev = py.event
        t0 = c(); n1 = hs._nlep_w(ev) if is_tt else 1; T['nlep'] += c() - t0
        t0 = c(); mproc = nu_met(py.process); T['met_process'] += c() - t0
        pth = py.infoPython().pTHat()
        if n1 != 1:
            n1l_fail += 1; tries.append((pth, mproc, -1.0, 0)); continue
        t0 = c(); mx, my = hs._met(ev); T['met_parton'] += c() - t0
        mp = math.hypot(mx, my)
        if mp < s4pu.PRE_MET:
            tries.append((pth, mproc, mp, 0)); continue
        n_pre += 1
        t0 = c(); ok = py.forceHadronLevel(); T['hadron'] += c() - t0
        if not ok:
            nfail += 1; continue
        ev = py.event
        t0 = c(); mx, my = hs._met(ev); T['met_final'] += c() - t0
        if math.hypot(mx, my) < s4pu.MET_MIN:
            tries.append((pth, mproc, mp, 0)); continue
        t0 = c()
        parts = [(p.id(), p.charge(), p.m(), p.px(), p.py(), p.pz(), p.e(), p.xProd(), p.yProd(), p.zProd(), p.tProd())
                 for p in (ev[j] for j in range(ev.size())) if p.isFinal()]
        T['list'] += c() - t0
        t0 = c(); s4pu.select_and_place(parts, s4pu.HS_VP, np.zeros(4)); T['select'] += c() - t0
        t0 = c(); p2c_hs0.gen_summary(py, [mx, my], sample, kept, sj20, sj30); T['summary'] += c() - t0
        tries.append((pth, mproc, mp, 1)); kept += 1
    t_all = c() - t_all
    A = np.array(tries)
    acc = A[A[:, 3] == 1]
    sig = py.infoPython().sigmaGen()
    # process-level-only instance: cost of a try that a process-level veto would stop
    lines, pth_min = s4pu.SM_SAMPLES[name]
    p0 = pythia8.Pythia('', False)
    p0.readFile(str(CP5))
    for ln in ["Beams:eCM = 14000.", f"PhaseSpace:pTHatMin = {pth_min}", "PartonLevel:all = off", "HadronLevel:all = off",
               "Print:quiet = on", "Next:numberCount = 0"] + list(lines):
        p0.readString(ln)
    p0.init()
    t0 = c()
    for _ in range(3000):
        p0.next()
    t_proc = (c() - t0) / 3000
    q = lambda a, ps: [float(np.quantile(a, p)) for p in ps] if len(a) else None  # noqa: E731
    res = dict(sample=sample, variant=variant, n_accept=kept, n_tries=len(A) + nfail, tries_per_accept=(len(A) + nfail) / kept,
               n_fail=nfail, n_not_one_lepton=n1l_fail, n_pass_prefilter=n_pre, sigma_gen_mb=sig,
               s_per_accept=t_all / kept, ms_per_accept={k: 1e3 * v / kept for k, v in T.items()},
               ms_per_try_next=1e3 * T['next'] / (len(A) + nfail), ms_process_level_only_event=1e3 * t_proc,
               accepted_pthat_min_q001_q01=[float(acc[:, 0].min())] + q(acc[:, 0], (0.001, 0.01)),
               accepted_process_met_min_q001_q01=[float(acc[:, 1].min())] + q(acc[:, 1], (0.001, 0.01)),
               accepted_parton_met_min=float(acc[:, 2].min()),
               frac_tries_process_met_below={str(x): float((A[:, 1] < x).mean()) for x in (50, 75, 100, 125, 150)},
               n_accepted_process_met_below={str(x): int((acc[:, 1] < x).sum()) for x in (50, 75, 100, 125, 150)},
               frac_tries_pthat_below={str(x): float((A[:, 0] < x).mean()) for x in (160, 170, 180, 190, 200)},
               n_accepted_pthat_below={str(x): int((acc[:, 0] < x).sum()) for x in (160, 170, 180, 190, 200)},
               accepted_final_met_mean=None)
    Path(out).write_text(json.dumps(res, indent=1))
    log.info('%s', json.dumps(res))


def chain(out, sample, n):
    import p2c_hs0
    pr = cProfile.Profile()
    pr.enable()
    meta = p2c_hs0.run(sample, 'prof_chain.npz', n, 'prof.chain.' + sample, 0)
    pr.disable()
    s = io.StringIO()
    pstats.Stats(pr, stream=s).sort_stats('cumulative').print_stats(45)
    st = pstats.Stats(pr)
    top = sorted(((v[3], v[2], k[2], Path(k[0]).name) for k, v in st.stats.items()), reverse=True)[:40]
    res = dict(sample=sample, n=n, t_total_s=meta['t_total_s'], mean_s_per_event=meta['mean_s_per_event'],
               top_cumulative_ms_per_event=[dict(func=f, file=fl, cum_ms=1e3 * cu / n, self_ms=1e3 * tt / n)
                                            for cu, tt, f, fl in top])
    Path(out).write_text(json.dumps(res, indent=1))
    log.info('%s', s.getvalue()[:6000])


def g4(out):
    import p2c_g4vtx as GV
    rng = np.random.default_rng(C.qv2_seed('prof.g4', 0))
    n = 200_000
    full = GV.geom_file()
    feas = Path('geom_feas.txt').resolve()          # the 12 unsplit barrel tubes of the feasibility benchmark, as passive slabs
    rows = [ln.split() for ln in (C.QV2 / 'phase1_strategy/src/generators/g4sv/geom_barrel.txt').read_text().splitlines()
            if ln and not ln.startswith('#')]
    feas.write_text('B 3.8\n' + '\n'.join(f'C {r[0]} {r[1]} -{r[2]} {r[2]} {r[3]} G4_Si 0' for r in rows) + '\n')
    arrays, mm = __import__('p2c_mbgen').generate(15000, 'prof.g4', 0)
    pool = dict(pdg=arrays['pool_pdg'], pt=arrays['pool_pt'], eta=arrays['pool_eta'])
    ch = np.isin(np.abs(pool['pdg']), (211, 321))

    def run(label, pt, eta, pdg, geom, rmax, plist='FTFP_BERT'):
        phi = rng.uniform(-np.pi, np.pi, len(pt))
        with open('p.txt', 'w') as f:
            for i in range(len(pt)):
                f.write('%d %d 0 0 0 0 %.9g %.9g %.9g\n' % (i, pdg[i], pt[i] * math.cos(phi[i]), pt[i] * math.sin(phi[i]),
                                                              pt[i] * math.sinh(eta[i])))
        kv, _ = GV.run_g4([geom, plist, 12345, 'v.txt', 'prim', 'p.txt', rmax])
        return dict(label=label, n=len(pt), ms_per_firing=float(kv['cpu_ms_per_event']), nvtx=int(kv['nvtx']),
                    ndropped=int(kv['ndropped']))
    idx = np.nonzero(ch)[0][rng.integers(0, ch.sum(), n)]
    ptn, etan, pdgn = pool['pt'][idx].astype(float), pool['eta'][idx].astype(float), pool['pdg'][idx]
    ptl = np.exp(rng.uniform(0, math.log(10.0), n)); etl = rng.uniform(-1, 1, n); pdl = rng.choice([211, -211], n)
    hard = ptn > 1.0
    res = [run('FEAS gun (pi, pT log-uniform 1-10, |eta|<1), FEAS 12-tube geometry', ptl, etl, pdl, feas, 1200.0),
           run('FEAS gun, full geometry (83 slabs, sensitive ones split)', ptl, etl, pdl, full, 1200.0),
           run('natural pi/K spectrum pT>0.5, full geometry', ptn, etan, pdgn, full, 1200.0),
           run('natural pi/K spectrum, only pT>1 GeV, full geometry', ptn[hard], etan[hard], pdgn[hard], full, 1200.0),
           run('natural pi/K spectrum, only pT<1 GeV, full geometry', ptn[~hard], etan[~hard], pdgn[~hard], full, 1200.0),
           run('natural pi/K spectrum pT>0.5, FEAS geometry', ptn, etan, pdgn, feas, 1200.0),
           run('natural pi/K spectrum pT>0.5, full geometry, QGSP_BERT', ptn, etan, pdgn, full, 1200.0, 'QGSP_BERT')]
    Path(out).write_text(json.dumps(dict(runs=res, frac_below_1GeV=float((~hard).mean())), indent=1))
    for r in res:
        log.info('%s', json.dumps(r))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'gen':
        gen(a[1], a[2], int(a[3]), a[4] if len(a) > 4 else '')
    elif a[0] == 'chain':
        chain(a[1], a[2], int(a[3]))
    else:
        g4(a[1])
