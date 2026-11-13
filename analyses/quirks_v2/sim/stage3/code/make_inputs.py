"""make_inputs.py -- Stage 3 (E7): extract the selected Stage-2 events into compact per-(species, mass, selection) npz
files for the job runner (Mac only: reads the Stage-2 files through sim/scripts/mg_events.py, not modified).

Selection (plan §2, decisions D10 as approved):
  sample   : stitched trigger-region file <P>-TRGS_m<m>.npz ('trig'); rows with w > 0;
  cut      : pT(QQbar) > 200 GeV (L1-MET proxy);
  unweight : the loader's deterministic hit-or-miss unweighting, seed 12345 (iter_events(..., unweight=True)); every
             event carries the common weight w_max, so N_eff = N;
  'p2'     : |eta_pair| < 4 (Stage-4 input; D10), file order, template and toy rows; the event COUNT of a P2 point is
             defined inside |eta_pair| < 2.5 (flag in_eta25).  Stored: per split, events in file order up to the
             N_STORE_P2-th in_eta25 event of that split (N_STORE_P2 = 300 >= the 200 used; margin for extensions);
  'p1'     : |eta_pair| < 1 (P1, Stage-1 conventions), template split, except E 1500 (both halves, file order: 168 + 157
             template/toy events, plan §1.2); first N_STORE_P1 = 400 events (300 used).
Per event: Stage-2 provenance (row, chunk, ievt_lhe, py8_seed, tt_split, origin), weights (w_orig, the merged
  '_MERGING=' weight columns divided by w_orig as float32 'wvar_ratio'), the quirk 3-momenta, recoil, jets, pair kinematics,
  the luminous-region vertex and the systematic tilt weights.
Luminous-region vertex (D2): (x, y, z, t) ~ N(0, 5 um), N(0, 5 um), N(0, 45 mm), N(0, 190 ps), independent
  (acts/geometry/cms_phase2_public.json 'beamspot'), drawn with default_rng(blake2b("vtx|spin|m|row")): the same vertex
  for an event at every Lambda and configuration.  Stored as vtx_lumi = (x, y, z, t) in mm, ns.
Tilt weights (plan §7): w_tilt = (x/x~)^a / mean[(x/x~)^a] with x = 2(gamma* - 1) (prop. to l_max at fixed m, Lambda)
  and x~ its median; a solved (bisection) per file so that the weighted median of x moves by +5 % (w_lmax_up), -5 %
  (w_lmax_dn), -1.1 % (w_qed) and -1.9 % (w_qed_19).  Solved on the counting set (in_eta25 for p2; all for p1).
Output: data/sim_stage3/inputs/<spin>_m<m>_<sel>.npz + inputs_index.json.
Run (theory_track/): pixi run python sim/stage3/code/make_inputs.py
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TT = HERE.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(TT / 'sim' / 'scripts'))
import mg_events as mg  # noqa: E402

OUT = TT / 'data' / 'sim_stage3' / 'inputs'
UNW_SEED = 12345
PTMIN = 200.0
N_STORE_P2 = 300
N_STORE_P1 = 400
SIG_XY_MM, SIG_Z_MM, SIG_T_NS = 0.005, 45.0, 0.190
E_MASSES = list(range(200, 1600, 100))
S_MASSES = [200, 500, 1000]
P1_POINTS = [('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)]


def md5_file(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def hseed(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little')


def wmedian(x, w):
    o = np.argsort(x); xs = x[o]; cw = np.cumsum(w[o]); cw /= cw[-1]
    return float(np.interp(0.5, cw, xs))


def tilt(x, target):
    """exponent a with weighted median of x under (x/x~)^a equal to (1 + target) x median."""
    xt = np.median(x)
    goal = (1 + target) * wmedian(x, np.ones_like(x))

    def f(a):
        w = (x / xt) ** a
        return wmedian(x, w) - goal
    lo, hi = (0.0, 20.0) if target > 0 else (-20.0, 0.0)
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise RuntimeError('tilt bracket failed')
    for _ in range(80):
        mid = 0.5 * (lo + hi); fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def extract(spin, m, sel):
    path = mg.sample_file(m, 'trig', spin)
    c = mg.load(path)
    acc, wmax = mg.unweight_mask(c, UNW_SEED)
    eta_max = 4.0 if sel == 'p2' else 1.0
    ids = mg._select(c, eta_max=eta_max, ptmin=PTMIN)          # w > 0, file order
    ids = ids[acc[ids]]
    eta = c['eta_pair'][ids]; spl = c['tt_split'][ids]
    keep = np.zeros(len(ids), bool)
    if sel == 'p2':
        for s in (0, 1):
            ins = (spl == s) & (np.abs(eta) < 2.5)
            csum = np.cumsum(ins)
            last = np.searchsorted(csum, N_STORE_P2)        # index of the N-th in_eta25 event of the split
            keep |= (spl == s) & (np.arange(len(ids)) <= last)
    else:
        if (spin, m) == ('F', 1500):
            keep[:N_STORE_P1] = True
        else:
            tmpl = np.where(spl == 0)[0][:N_STORE_P1]
            keep[tmpl] = True
    ids = ids[keep]
    names = [str(x) for x in c['wvar_names']]
    merged = [i for i, nm in enumerate(names) if '_MERGING=' in nm]
    w_orig = c['w'][ids]
    d = dict(
        row=ids.astype(np.int64), chunk=c['chunk'][ids], ievt_lhe=c['ievt_lhe'][ids], py8_seed=c['py8_seed'][ids],
        tt_split=c['tt_split'][ids], origin=c['origin'][ids], w_orig=w_orig,
        wvar_ratio=(c['wvar'][ids][:, merged] / w_orig[:, None]).astype(np.float32),
        wvar_names=np.array([names[i] for i in merged]),
        p_qp=c['p_qp'][ids, 1:].copy(), p_qm=c['p_qm'][ids, 1:].copy(), recoil=c['recoil'][ids], jets=c['jets'][ids],
        njet=c['njet'][ids], gstar=c['gamma_star'][ids], cstar=c['cstar'][ids], bg=c['bg_pair'][ids], eta=c['eta_pair'][ids],
        pt=c['pt_pair'][ids], M=c['m_pair'][ids], in_eta25=np.abs(c['eta_pair'][ids]) < 2.5)
    vt = np.zeros((len(ids), 4))
    for i, r in enumerate(ids):
        g = np.random.default_rng(hseed(f'vtx|{spin}|{m}|{int(r)}'))
        vt[i] = g.normal(0.0, [SIG_XY_MM, SIG_XY_MM, SIG_Z_MM, SIG_T_NS])
    d['vtx_lumi'] = vt
    x = 2 * (d['gstar'] - 1)
    cset = d['in_eta25'] if sel == 'p2' else np.ones(len(ids), bool)
    tilts = {}
    for key, tgt in (('w_lmax_up', 0.05), ('w_lmax_dn', -0.05), ('w_qed', -0.011), ('w_qed_19', -0.019)):
        a = tilt(x[cset], tgt)
        w = (x / np.median(x[cset])) ** a
        d[key] = w / w[cset].mean()
        tilts[key] = dict(a=a, target=tgt, check=wmedian(x[cset], d[key][cset]) / np.median(x[cset]) - 1)
    selection = dict(sample='trig (TRGS)', file=os.path.basename(path), positive_weights=True, ptmin=PTMIN,
                     eta_max=eta_max, count_region_eta=2.5 if sel == 'p2' else 1.0,
                     split=('template+toy' if sel == 'p2' else ('both (file order)' if (spin, m) == ('F', 1500) else 'template')),
                     unweight=True, unweight_seed=UNW_SEED, w_max=wmax, vertex=dict(sig_xy_mm=SIG_XY_MM, sig_z_mm=SIG_Z_MM,
                     sig_t_ns=SIG_T_NS, seed_rule='default_rng(blake2b("vtx|spin|m|row") 8-byte little endian)'), tilts=tilts)
    d.update(source_file=np.array(os.path.relpath(path, TT)), source_md5=np.array(md5_file(path)),
             sigma_norm_fb=np.array(float(c['sigma_norm_fb'])), sigma_ref_fb=np.array(float(c['sigma_ref_fb'])),
             w_max=np.array(wmax), selection_json=np.array(json.dumps(selection, default=float)), spin=np.array(spin),
             m=np.array(float(m)), sel=np.array(sel))
    mg._CACHE.clear()
    return d, selection


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    index = {}
    todo = [(s, m, 'p2') for s, ms in (('F', E_MASSES), ('S', S_MASSES)) for m in ms] + [(s, m, 'p1') for s, m in P1_POINTS]
    for spin, m, sel in todo:
        d, selection = extract(spin, m, sel)
        fn = OUT / f'{spin}_m{m}_{sel}.npz'
        np.savez_compressed(fn, **d)
        n = len(d['row'])
        info = dict(n=n, n_template=int(np.sum(d['tt_split'] == 0)), n_toy=int(np.sum(d['tt_split'] == 1)),
                    n_in_eta25_template=int(np.sum(d['in_eta25'] & (d['tt_split'] == 0))),
                    n_in_eta25_toy=int(np.sum(d['in_eta25'] & (d['tt_split'] == 1))), md5=md5_file(fn),
                    tilts={k: round(v['a'], 4) for k, v in selection['tilts'].items()})
        index[fn.name] = info
        print(fn.name, info, flush=True)
    json.dump(index, open(OUT / 'inputs_index.json', 'w'), indent=1)
