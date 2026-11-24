"""step4_acceptance.py -- STR §4.1 order, step (4): A = eps_fid x eps_trig x eps_presel and m_mig, ONCE, with the
frozen MET model.  Written and tested on BACKGROUND files only by work package p3-c (Birgit, 2026-11-24).

*** NOT TO BE RUN ON SIGNAL BY p3-c.  Running it on Stage-2 signal files is the single step-(4) computation of COM
*** BL-1 / S1-f; it needs --approve <file>, the orchestrator's record that the MET model is reviewed and frozen (the
*** file's sha256 is written into the output).  Without --approve the script accepts only --test-background.

  step (4):  <python> step4_acceptance.py --approve <record> --model <model.json> --out <A.json> \
                 --point <label> --s2 <stage2 npz,...> [--mig <150 GeV stage2 npz,...>] [--gen-cut 200]
  test:      <python> step4_acceptance.py --test-background --model <model.json> --out <test.json> \
                 --point znn --s2 <p3c_gen znn npz,...>

Inputs (sim/scripts/convert_hepmc.py layout): recoil_eta5[N,4] (E, px, py, pz of everything visible except the
quirks, |eta| < 5), jets[N,J,4] (pt, eta, phi, m; pT > 20 GeV), p_qp_hard, p_qm_hard (pair before the shower: the
generator cut acts on its pT), eta_pair, w.  The pair is invisible to the model (STR §4.13: not an isolated lepton,
calorimeter deposits neglected, limitation L11); the signal has no prompt lepton list (none is expected).
REQUIREMENT on the S1 Stage-2 conversion: store ALL jets above 20 GeV (convert_hepmc keeps 4; with 4, jets beyond
the fourth stay unsmeared in U_true; the output records n_jets_stored and the fraction of events with njet > stored).
Definitions (v1 `products.acceptance_point`, with the v2 model in place of the 25 GeV smearing):
  eps_fid = sum w F / sum w, F = |eta_pair| < 2.5;  eps_trig = sum w F <eps_trig> / sum w F;
  A = sum w F <eps_trig x presel> / sum w;  eps_presel = A / (eps_fid eps_trig);
  m_mig = sum_{pT_hard(pair) < gen-cut} w F <eps_trig x presel> / sum w F <eps_trig x presel> on the 150 GeV sample.
Output: A.json with, per variation of metmodel.VARIATIONS, A, the factors, m_mig, effective counts; nothing else.
"""
import argparse
import hashlib
import json
import logging
from pathlib import Path

import numpy as np

import metmodel as M
import p3c_io as IO

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('step4_acceptance')
K = 20
CHUNK = 5000


def from_stage2(path):
    z = np.load(path)
    J = z['jets']; n = len(J)
    hard = z['p_qp_hard'] + z['p_qm_hard']
    return dict(px5=z['recoil_eta5'][:, 1], py5=z['recoil_eta5'][:, 2], jets=J, njet=z['njet'], w=z['w'],
                eta_pair=z['eta_pair'], pt_hard=np.hypot(hard[:, 1], hard[:, 2]), n=n)


def from_background(path):
    """Adapter for the test: a p3c_gen file in the Stage-2 layout; the neutrino system plays the pair."""
    d = IO.load(path); n = d['n']; jp, jm = d['inp']['jp'], d['inp']['jm']
    J = np.zeros((n, M.JMAX, 4)); J[:, :, :3] = np.where(jm[:, :, None], jp, 0.0)
    # put the prompt leptons back into the visible sum as unclustered energy (the signal layout has no lepton list)
    return dict(px5=d['px5'], py5=d['py5'], jets=J, njet=jm.sum(1), w=d['w_gen'], eta_pair=np.zeros(n),
                pt_hard=np.hypot(d['met'][:, 0], d['met'][:, 1]), n=n)


def inputs(s):
    """Stage-2 layout -> model inputs (jets >= 30 GeV, |eta| < 4.7; no leptons; U_true = visible - jets)."""
    n = s['n']; J = s['jets']; nj = min(J.shape[1], M.JMAX)
    jp = np.zeros((n, M.JMAX, 3)); jm = np.zeros((n, M.JMAX), bool)
    jp[:, :nj] = J[:, :nj, :3]
    jm[:, :nj] = (J[:, :nj, 0] >= M.JET_PT_MIN) & (np.abs(J[:, :nj, 1]) < M.JET_ETA_MAX)
    jx = (jp[:, :, 0] * np.cos(jp[:, :, 2]) * jm).sum(1); jy = (jp[:, :, 0] * np.sin(jp[:, :, 2]) * jm).sum(1)
    return dict(jp=jp, jm=jm, lp=np.zeros((n, M.LMAX, 5)), lm=np.zeros((n, M.LMAX), bool), ngam=np.zeros(n),
                ux=s['px5'] - jx, uy=s['py5'] - jy)


def accept(samples, par, rng):
    """-> sums over files: sw, swF, swF<trig>, swF<trig x presel>, same below the generator cut, and squared sums."""
    acc = dict(sw=0.0, swF=0.0, swFt=0.0, swFa=0.0, sw2=0.0, swFa2=0.0, lo=0.0, n=0, n_more=0)
    for s in samples:
        inp = inputs(s); F = np.abs(s['eta_pair']) < 2.5; w = s['w']
        a = np.zeros(s['n']); t = np.zeros(s['n'])
        for c in range(0, s['n'], CHUNK):
            sl = slice(c, c + CHUNK)
            o = M.apply(IO.sub(inp, sl), par, rng, K, return_met=True)
            a[sl] = o['w'].mean(1); t[sl] = M.trig_eff(o['met'], par['trig']).mean(1)
        acc['sw'] += w.sum(); acc['swF'] += (w * F).sum(); acc['swFt'] += (w * F * t).sum()
        acc['swFa'] += (w * F * a).sum(); acc['sw2'] += (w ** 2).sum(); acc['swFa2'] += ((w * F * a) ** 2).sum()
        acc['lo'] += (w * F * a)[s['pt_hard'] < par['_gen_cut']].sum(); acc['n'] += s['n']
        acc['n_more'] += int((s['njet'] > s['jets'].shape[1]).sum())
    return acc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--approve'); ap.add_argument('--test-background', action='store_true')
    ap.add_argument('--model', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--point', required=True); ap.add_argument('--s2', required=True); ap.add_argument('--mig')
    ap.add_argument('--gen-cut', type=float, default=200.0)
    a = ap.parse_args()
    if a.test_background == bool(a.approve):
        raise SystemExit('exactly one of --approve <record> (step 4, signal, once) or --test-background is required')
    if a.approve and Path(a.out).exists():
        raise SystemExit(f'{a.out} exists: step (4) is computed once (STR §4.1); refusing to overwrite')
    read = from_background if a.test_background else from_stage2
    model = json.loads(Path(a.model).read_text())
    res = dict(point=a.point, mode='TEST ON BACKGROUND (not a signal quantity)' if a.test_background else 'step 4',
               approval_record=a.approve, approval_sha256=hashlib.sha256(Path(a.approve).read_bytes()).hexdigest()
               if a.approve else None, model_sha256=hashlib.sha256(Path(a.model).read_bytes()).hexdigest(),
               gen_cut=a.gen_cut, K=K, files=a.s2.split(','), files_mig=a.mig.split(',') if a.mig else None, var={})
    s2 = [read(f) for f in a.s2.split(',')]
    mig = [read(f) for f in a.mig.split(',')] if a.mig else None
    res['n_jets_stored'] = int(s2[0]['jets'].shape[1])
    for v in M.VARIATIONS:
        if v == 'lost_e_kept':
            continue
        par = dict(M.params(v, model), _gen_cut=a.gen_cut)
        rng = np.random.default_rng([20261124, 4])
        x = accept(s2, par, rng)
        A = x['swFa'] / x['sw']; ef = x['swF'] / x['sw']; et = x['swFt'] / max(x['swF'], 1e-300)
        r = dict(A=A, eps_fid=ef, eps_trig=et, eps_presel=A / max(ef * et, 1e-300), n_events=x['n'],
                 n_eff_generated=x['sw'] ** 2 / x['sw2'], n_eff_accepted=x['swFa'] ** 2 / max(x['swFa2'], 1e-300),
                 frac_events_with_more_jets_than_stored=x['n_more'] / x['n'])
        if mig:
            y = accept(mig, par, rng)
            r['m_mig'] = y['lo'] / max(y['swFa'], 1e-300); r['m_mig_n_eff_accepted'] = y['swFa'] ** 2 / max(y['swFa2'], 1e-300)
        res['var'][v] = r
    res['trigger_nuisance_erf_shifted_A'] = accept(s2, dict(M.params('nominal', model), trig='erf_shifted', _gen_cut=a.gen_cut),
                                                   np.random.default_rng([20261124, 4]))['swFa'] / sum(s['w'].sum() for s in s2)
    Path(a.out).write_text(json.dumps(res, indent=1) + '\n')
    log.info('written %s (%s)', a.out, res['mode'])


if __name__ == '__main__':
    main()
