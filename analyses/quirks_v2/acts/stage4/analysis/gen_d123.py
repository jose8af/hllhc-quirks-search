"""gen_d123.py -- generator-level Pythia inputs of the B sum (FIXER R2, orchestrator 2026-10-14; D1, D2, D3).

Runs in the ACTS env (pythia8):  nice -n 15 pixi run --manifest-path acts/pixi.toml python \
        acts/stage4/analysis/gen_d123.py nt <n_acc> <n_minbias> <out.json>
                                         smregen <out.json> <sm job npz> [...]

Generator: the production SM configuration, imported unchanged from acts/stage4/code/s4pu.py (HardScatter: Pythia 8 CP5,
14 TeV, pT-hat > 150 GeV, MPI + hadronisation, truth MET(nu) > 200 GeV).  No detector simulation.

PRESELECTION (USER D1, 2026-10-14: N_trig after the same event-level preselection as the signal eps; plan §3,
WP_RULE §1.3 l.143-147), per accepted event, generator-level:
  MET_reco = truth MET(nu) + N(0, 25 GeV) per component; trigger weight eps_trig = 0.98 x 0.5 [1 + erf((MET_reco - 200)
  / (20 sqrt 2))]; MET_reco > 250 GeV; >= 1 jet pT > 100 GeV |eta| < 2.4; min dphi(jet_1-4, MET_reco) > 0.5; vetoes on
  isolated e/mu (pT > 10) and gamma (pT > 15).
  Generator-level proxies (each the LOOSER choice, listed in PROXIES): jets = Pythia SlowJet anti-kT R = 0.4 on the
  visible final state (pT > 30, |eta| < 4.7), pT smeared 10 %/sqrt(E) (+) 5 % (plan §3); the leading 4 such jets enter
  min dphi; an e/mu/gamma is vetoed only if PROMPT (no hadron ancestor) and ISOLATED (visible sum pT in dR < 0.3 below
  0.2 pT) within |eta| < 2.5; the tau_h veto is NOT applied (no generator proxy for the tau ID; looser).
  Event weight w = eps_trig x pass.
D3: sigma = sigma_gen x N_acc / (tries x (1 - N_hadfail / attempts)), attempts = tries reaching forceHadronLevel
  (REVIEW R2 A-1; the production generator counts a failed forceHadronLevel as a try).  D2: C' rates per preselected event in the road |dphi(., phi_MET_reco)| < 0.15 rad (frozen
  delta95, WP_RULE §1.3), gun phase space of code/s4cp.py; gamma/V0/PV-pair/looper from the HS vertex; NI parents and
  DIF from the HS event + Poisson(200) minimum-bias interactions (per-interaction rates x 200).
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT / 'acts' / 'stage4' / 'code'))
import s4pu  # noqa: E402
import pythia8  # noqa: E402

CP5 = TT / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat'
# REVIEW_ANALYSIS_R2 B-1: processes that 'enter N_trig only' (WP_RULE l.326), generator level, same filter/preselection.
# Injected into s4pu.SM_SAMPLES at RUN time only (the production file is not edited).
EXTRA = {
    'ttbar_2l': (["Top:gg2ttbar = on", "Top:qqbar2ttbar = on"], 150.0),             # exactly two W -> l nu (filter)
    'top_t': (["Top:qq2tq(t:W) = on"], 150.0),
    'WW': (["WeakDoubleBoson:ffbar2WW = on"], 150.0),
    'WZ': (["WeakDoubleBoson:ffbar2ZW = on", "WeakZ0:gmZmode = 2"], 150.0),
    'ZZ': (["WeakDoubleBoson:ffbar2gmZgmZ = on", "WeakZ0:gmZmode = 2"], 150.0),
}
s4pu.SM_SAMPLES.update(EXTRA)
VETO_INEFF = 0.05      # B-1 (ii): flat 5 % per veto-able prompt isolated e/mu/gamma (neither plan nor WP_RULE defines one)
W_ROAD = 0.15
MK, MPI_ = 0.493677, 0.13957039
PROC = ['Znunu_j', 'Wtaunu_j', 'Wtauhnu_j', 'Wenu_j', 'Wmunu_j', 'ttbar_1l'] + list(EXTRA)
PROXIES = ['jets: SlowJet anti-kT R=0.4 on visible final state, pT>30, |eta|<4.7, smeared 10%/sqrt(E)+5% (plan §3)',
           'min dphi over the leading 4 jets (pT>30) and MET_reco',
           'e/mu/gamma veto only for PROMPT (no hadron ancestor) and ISOLATED (sum visible pT in dR<0.3 < 0.2 pT) '
           'objects with |eta|<2.5; each such object passes the veto with a flat 5 % inefficiency allowance '
           '(weight x 0.05 per object; REVIEW R2 B-1 (ii), neither plan nor WP_RULE defines one)',
           'tau_h veto NOT applied (no generator-level proxy for tau ID; looser)',
           'MET_reco = neutrino MET + N(0, 25 GeV)/component; events with truth MET < 200 GeV are not generated '
           '(production filter): their migration above 250 GeV (> 2 sigma) is neglected',
           'sigma_t,trig: eps_trig weight (plateau 0.98, T50 200, width 20 GeV; plan §3 ESTIMATE)']
BINS_PT = np.geomspace(0.05, 50.0, 41)
NPROC = dict(Znunu_j=2000, Wtaunu_j=3000, Wtauhnu_j=3000, Wenu_j=4000, Wmunu_j=4000, ttbar_1l=3500,
             ttbar_2l=400, top_t=600, WW=800, WZ=800, ZZ=800)


def dphi(a, b):
    return (a - b + math.pi) % (2 * math.pi) - math.pi


def hadron_ancestor(ev, k):
    """True if any ancestor of particle k is a hadron (|id| > 100, not a beam particle): non-prompt."""
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
            if 100 < ev[m].idAbs() < 10_000_000 and ev[m].idAbs() not in (2101, 2103, 2201, 2203, 1103, 3101, 3103,
                                                                          3201, 3203, 3303):
                return True
            stack.append(m)
    return False


def presel(ev, met, rng, sj, phm_override=None):
    """Generator-level preselection of one accepted event -> (weight, details, phi_met_reco).  phm_override: the
    production road phi_MET (stored trials.phimet of a hit-level SM event; REVIEW R2 C-2) for the min dphi cut."""
    mr = np.asarray(met, float) + rng.normal(0.0, 25.0, 2)
    m = float(np.hypot(*mr)); phm = math.atan2(mr[1], mr[0]) if phm_override is None else float(phm_override)
    eps = 0.98 * 0.5 * (1 + math.erf((m - 200.0) / (20.0 * math.sqrt(2))))
    sj.analyze(ev)
    jets = []
    for i in range(sj.sizeJet()):
        p = sj.p(i)
        e = p.e(); pt = p.pT()
        res = math.hypot(0.10 / math.sqrt(max(e, 1e-3)), 0.05)
        pts = pt * max(0.0, 1 + res * rng.standard_normal())
        jets.append((pts, p.eta(), p.phi()))
    jets.sort(key=lambda x: -x[0])
    jets = [j for j in jets if j[0] > 30.0 and abs(j[1]) < 4.7]
    lead = any(j[0] > 100 and abs(j[1]) < 2.4 for j in jets)
    mdp = min([abs(dphi(j[2], phm)) for j in jets[:4]], default=9.0)
    vis = [(ev[k].pT(), ev[k].eta(), ev[k].phi()) for k in range(ev.size())
           if ev[k].isFinal() and ev[k].idAbs() not in (12, 14, 16)]
    veto = dict(e=False, mu=False, gamma=False); n_veto = 0
    for k in range(ev.size()):
        p = ev[k]
        if not p.isFinal():
            continue
        a = p.idAbs(); pt = p.pT()
        kind = 'e' if a == 11 else 'mu' if a == 13 else 'gamma' if a == 22 else None
        if kind is None or abs(p.eta()) > 2.5 or pt < (15.0 if kind == 'gamma' else 10.0):
            continue
        iso = sum(q[0] for q in vis if 0 < math.hypot(q[1] - p.eta(), dphi(q[2], p.phi())) < 0.3) - 0.0
        if iso >= 0.2 * pt:
            continue
        if hadron_ancestor(ev, k):
            continue
        veto[kind] = True; n_veto += 1
    ok = (m > 250.0) and lead and (mdp > 0.5)
    wveto = VETO_INEFF ** n_veto
    det = dict(met_reco=m, eps_trig=eps, met250=m > 250.0, jet100=lead, mindphi=mdp > 0.5, veto_e=veto['e'],
               veto_mu=veto['mu'], veto_gamma=veto['gamma'], n_veto=n_veto)
    return (eps * wveto if ok else 0.0), det, phm


def tau_class(ev):
    for k in range(ev.size()):
        p = ev[k]
        if p.idAbs() == 15 and p.daughter1() > 0 and ev[p.daughter1()].idAbs() != 15:
            ds = [ev[j].idAbs() for j in range(p.daughter1(), p.daughter2() + 1)]
            return 'lep' if any(x in (11, 13) for x in ds) else 'had'
    return 'none'


def road_objects(ev, phm, hs=True):
    """C' objects in the road (gun phase space of s4cp.py), with their pT for the spectrum fold."""
    o = dict(gamma=[], v0=[], looper=[], ni=[], dif=[], ch_phi=[])
    for k in range(ev.size()):
        p = ev[k]
        a = p.idAbs(); pt = p.pT()
        if pt <= 0:
            continue
        eta = p.eta(); inw = abs(dphi(p.phi(), phm)) < W_ROAD
        prompt = (abs(p.xProd()) + abs(p.yProd()) + abs(p.zProd())) == 0
        if a in (310, 3122) and 0.5 < pt < 50 and abs(eta) < 1 and inw and not p.isFinal() \
                and ev[p.daughter1()].idAbs() != a:
            o['v0'].append((pt, 0.692 if a == 310 else 0.639))
        if not p.isFinal():
            continue
        if a == 22 and 0.5 < pt < 50 and abs(eta) < 1 and inw:
            o['gamma'].append((pt, 1.0))
        if p.charge() != 0 and prompt:
            if pt > 0.05 and abs(eta) < 1.2:
                o['ch_phi'].append(p.phi())
            if a in (211, 11) and 0.05 < pt < 0.7 and abs(eta) < 0.3 and inw:
                o['looper'].append((pt, 1.0))
            if a in (211, 321, 2212) and 0.5 < pt < 20 and abs(eta) < 1 and inw:
                o['ni'].append((pt, math.cosh(eta)))
            if a in (211, 321) and 0.5 < pt < 10 and abs(eta) < 1 and inw:
                M, ct = (MK, 3712.0) if a == 321 else (MPI_, 7804.5)
                lam = pt / M * ct
                o['dif'].append((pt, math.exp(-30.0 / lam) - math.exp(-1000.0 / lam)))
    return o


def pvpairs(ch_phi, phm):
    n = len(ch_phi)
    if n < 2:
        return 0.0
    a = np.array(ch_phi); i, j = np.triu_indices(n, 1)
    d = (a[j] - a[i] + np.pi) % (2 * np.pi) - np.pi
    mean = a[i] + 0.5 * d
    return float((np.abs((mean - phm + np.pi) % (2 * np.pi) - np.pi) < W_ROAD).sum())


def generate_counted(hs, seed, max_tries=200000):
    """s4pu.HardScatter.generate with the hadronisation failures COUNTED (identical event stream)."""
    py = hs.gen.py
    py.rndm.init(int(seed) % 900_000_000)
    hadfail = 0; attempts = 0
    for n_try in range(1, max_tries + 1):
        if not py.next():
            continue
        ev = py.event
        if hs.name == 'ttbar_1l' and hs._nlep_w(ev) != 1:
            continue
        if hs.name == 'ttbar_2l' and hs._nlep_w(ev) != 2:
            continue
        mx, my = hs._met(ev)
        if math.hypot(mx, my) < s4pu.PRE_MET:
            continue
        attempts += 1                     # REVIEW R2 A-1: hadronisation ATTEMPTS (tries passing the pre-filters)
        if not py.forceHadronLevel():
            hadfail += 1
            continue
        ev = py.event
        mx, my = hs._met(ev)
        if math.hypot(mx, my) < s4pu.MET_MIN:
            continue
        generate_counted.attempts = attempts
        return ev, np.array([mx, my]), n_try, hadfail, py.infoPython().sigmaGen()
    raise RuntimeError('no event accepted')


def slowjet():
    return pythia8.SlowJet(-1, 0.4, 30.0, 4.7, 2, 1)


def hist(vals):
    if not vals:
        return np.zeros(len(BINS_PT) - 1)
    v = np.array(vals)
    return np.histogram(v[:, 0], bins=BINS_PT, weights=v[:, 1])[0]


def mode_nt(n_acc, n_mb, out, procs=None, tag='fixer-r2-d123', n_force=0):
    res = dict(created=time.strftime('%Y-%m-%d %H:%M:%S'), w_road=W_ROAD, proxies=PROXIES, bins_pt=BINS_PT.tolist(),
               processes={}, s4pu_sha=None)
    import hashlib
    res['s4pu_sha256'] = hashlib.sha256((TT / 'acts/stage4/code/s4pu.py').read_bytes()).hexdigest()
    for name in (procs or PROC):
        t0 = time.time()
        hs = s4pu.HardScatter(CP5, name, tt=None)
        sj = slowjet()
        N = n_force or (NPROC.get(name, n_acc) if n_acc > 0 else 20)  # sized for <= 5 % stat (f_presel 0.1-0.5)
        tries = 0; hadfail = 0; att = 0; sg = None
        W = []; det_acc = {}; cls = dict(lep=[0, 0.0], had=[0, 0.0], none=[0, 0.0])
        R = dict(gamma=0.0, v0=0.0, pvpair=0.0, looper=0.0, ni=0.0, dif=0.0)
        H = {k: np.zeros(len(BINS_PT) - 1) for k in ('gamma', 'v0', 'looper', 'ni', 'dif')}
        for i in range(N):
            seed = s4pu.hseed(tag, name, i)
            ev, met, nt, hf, sg = generate_counted(hs, seed)
            tries += nt; hadfail += hf; att += generate_counted.attempts
            rng = np.random.default_rng(s4pu.hseed(tag + '-presel', name, i, mod=2 ** 62))
            w, det, phm = presel(ev, met, rng, sj)
            W.append(w)
            for k, v in det.items():
                if isinstance(v, bool):
                    det_acc[k] = det_acc.get(k, 0) + int(v)
            if name.startswith('Wtau'):
                c = tau_class(ev); cls[c][0] += 1; cls[c][1] += w
            if w > 0:
                o = road_objects(ev, phm)
                for k in ('gamma', 'v0', 'looper', 'ni', 'dif'):
                    R[k] += w * sum(x[1] for x in o[k])
                    H[k] += w * hist(o[k])
                R['pvpair'] += w * pvpairs(o['ch_phi'], phm)
        W = np.array(W)
        f_att = hadfail / max(att, 1)                       # failures per hadronisation ATTEMPT (A-1)
        sig_pb = sg * 1e9 * N / (tries * (1 - f_att))        # = sigma_gen (A/T) N / (A - F)
        f = float(W.mean())
        npass = int((W > 0).sum())
        rel_sig = math.sqrt(max(1 - N / (tries * (1 - f_att)), 0) / N)
        rel_f = float(np.std(W, ddof=1) / max(W.mean(), 1e-12) / math.sqrt(N))
        sw = W.sum()
        res['processes'][name] = dict(
            n_acc=N, tries=tries, hadfail=hadfail, attempts=att, f_hadfail_per_attempt=f_att,
            r_hadfail=hadfail / tries, sigma_gen_pb=sg * 1e9,
            sigma_MET200_pb=sig_pb, rel_stat_sigma=rel_sig, f_presel_weighted=f, n_pass=npass, rel_stat_f=rel_f,
            rel_stat_total=math.hypot(rel_sig, rel_f), counts_acc=det_acc,
            tau_class=({k: dict(n=v[0], sum_w=v[1]) for k, v in cls.items()} if name.startswith('Wtau') else None),
            rates_per_presel_event={k: (v / sw if sw > 0 else None) for k, v in R.items()},
            pt_spectra_presel={k: (v / sw).tolist() if sw > 0 else None for k, v in H.items()},
            seconds=time.time() - t0, seed_tag=tag, sum_w=float(sw), sum_w2=float((W ** 2).sum()))
        print(name, json.dumps({k: v for k, v in res['processes'][name].items() if k != 'pt_spectra_presel'}),
              flush=True)
        Path(out).write_text(json.dumps(res, indent=1))
    if n_mb <= 0:
        return
    # minimum bias, per interaction (in the road; road is fixed at phi = 0 for isotropic sources)
    t0 = time.time()
    mb = s4pu.PythiaGen(CP5)
    acc = dict(ni=0.0, dif=0.0, gamma=0.0, v0=0.0, looper=0.0)
    H = {k: np.zeros(len(BINS_PT) - 1) for k in acc}
    for i in range(n_mb):
        parts, ev = mb.generate(s4pu.hseed('fixer-r2-mb', i))
        o = road_objects(ev, 0.0)
        for k in acc:
            acc[k] += sum(x[1] for x in o[k]); H[k] += hist(o[k])
    res['minbias'] = dict(n_int=n_mb, per_interaction=({k: v / n_mb for k, v in acc.items()}),
                          per_PU200_event={k: 200 * v / n_mb for k, v in acc.items()},
                          rel_stat={k: (1 / math.sqrt(max(acc[k], 1e-9))) for k in acc},   # C-8: 1/sqrt(objects)
                          pt_spectra_per_interaction={k: (v / n_mb).tolist() for k, v in H.items()},
                          seconds=time.time() - t0, seed_tag=tag, sum_w=float(sw), sum_w2=float((W ** 2).sum()))
    print('minbias', json.dumps(res['minbias']['per_PU200_event']), flush=True)
    Path(out).write_text(json.dumps(res, indent=1))


def mode_smregen(out, paths):
    """Per SM hit-level job: regenerate each event's hard scatter from the stored seeds (production MPI init file,
    read-only), VERIFY the regenerated truth MET equals the stored hs_met, and return its tau decay class and the
    preselection weight (same footing as N_trig)."""
    res = {}
    gens = {}
    for p in paths:
        with np.load(p, allow_pickle=False) as z:
            meta = json.loads(str(z['meta_json']))
            tphi = z['trials.phimet'] if 'trials.phimet' in z.files else None
            tev = z['trials.ev'] if 'trials.ev' in z.files else None
        job = meta['job']; name = job['sm_sample']
        cm = meta.get('chain_meta', {})
        seeds = cm.get('event_seeds') or [s4pu.hseed('sm', name, job['seed'], i, mod=2 ** 62)
                                           for i in range(job['n_events'])]
        info = cm.get('ev_info') or []
        f = TT / 'data' / 'acts_stage4' / 'g1' / 'pythia_init' / f'mpi_cp5_14tev_hs_{name}.dat'
        if name not in gens:
            if not f.exists():
                raise SystemExit(f'REFUSED: MPI init file {f.name} missing (would be created by s4pu): cannot '
                                 'reproduce the production events')
            gens[name] = (s4pu.HardScatter(CP5, name, tt=TT), slowjet())
        hs, sj = gens[name]
        rows = []
        for i, sd in enumerate(seeds):
            ev, met, nt, hf, sg = generate_counted(hs, s4pu.hseed('hs', sd))
            stored = info[i].get('hs_met') if i < len(info) else None
            ok = stored is not None and np.allclose(met, stored, rtol=1e-9, atol=1e-6)
            rng = np.random.default_rng(s4pu.hseed('presel', sd, mod=2 ** 62))
            ph_road = None
            if tphi is not None:                     # C-2: the production road phi_MET of this event (one road)
                k = np.where(tev - int(job.get('ev0', 0)) == i)[0]
                ph_road = float(tphi[k[0]]) if len(k) else None
            w, det, phm = presel(ev, met, rng, sj, phm_override=ph_road)
            rows.append(dict(ev=i, met_match=bool(ok), stored_available=stored is not None, tau=tau_class(ev),
                             w_presel=w, tries=nt, hadfail=hf))
        res[job['id']] = dict(sample=job['sample'], sm_sample=name, rows=rows,
                              n_met_match=sum(r['met_match'] for r in rows), n=len(rows))
        print(job['id'], res[job['id']]['n_met_match'], '/', len(rows), flush=True)
    import hashlib
    res['_provenance'] = {f: hashlib.sha256((TT / f).read_bytes()).hexdigest() for f in
                          ('acts/stage4/analysis/gen_d123.py', 'acts/stage4/code/s4pu.py')}
    Path(out).write_text(json.dumps(res, indent=1))


if __name__ == '__main__':
    if sys.argv[1] == 'nt':
        mode_nt(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4],
                procs=(sys.argv[5].split(',') if len(sys.argv) > 5 else None),
                tag=(sys.argv[6] if len(sys.argv) > 6 else 'fixer-r2-d123'),
                n_force=(int(sys.argv[7]) if len(sys.argv) > 7 else 0))
    elif sys.argv[1] == 'smregen':
        mode_smregen(sys.argv[2], sys.argv[3:])
