"""make_s3_toy_input.py -- feasibility A (Anselm): a self-contained Stage-3 input file for smoke tests and benchmarks.

NOT a physics sample.  No Stage-2 (MG5+Pythia) output exists yet in v2, so this builds the runner input schema of
sim/stage3/code/run_stage3.py:run_job from the v1 T2 toy generator (code/T2_kinematics.py: LO q qbar -> V* g and
q g -> V* q matrix elements on CT18NLO member 0, pT(QQ) > 200 GeV), i.e. the parton-level DY+ISR kinematics v1 used before
MadGraph.  The quirk pair decays in its rest frame along an axis drawn from the T2 angular law (F: 2 - beta^2 sin^2 theta
about the Collins-Soper axis; implemented here with the T2 CS-axis construction), then is boosted to the lab.
Events are unweighted by hit-or-miss (seed below); every event gets w = w_max.  Fields the runner only copies
(recoil, jets, systematic weights) are filled with neutral placeholders and flagged in selection_json.

Run in the TT env (from analyses/quirks_v2):
  pixi run --manifest-path envs/tt/pixi.toml python phase1_strategy/src/make_s3_toy_input.py <out_dir> <spin> <m> <n>
PDF: env T2_PDF (default /home/users/jdochoa/sw/lhapdf_data/CT18NLO/CT18NLO_0000.dat, installed by executor Basil).
Writes <out_dir>/<spin>_m<m>_toy.npz via <name>.part + fsync + rename.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

QV2 = Path(__file__).resolve().parents[2]
os.environ.setdefault('T2_PDF', '/home/users/jdochoa/sw/lhapdf_data/CT18NLO/CT18NLO_0000.dat')
os.environ.setdefault('T2_CACHE', '/dev/null')          # never written: only the sampler functions are used
sys.path.insert(0, str(QV2 / 'code'))
import T2_kinematics as T2  # noqa: E402

SEED = 20261113
SIG_XY_MM, SIG_Z_MM, SIG_T_NS = 5.0e-3, 45.0, 0.190     # acts/geometry/cms_phase2_public.json 'beamspot' (v1 D2)


def hseed(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little')


def boost(p4, b):
    """Boost 4-vectors p4 (n,4: E,px,py,pz) by velocity b (n,3)."""
    b2 = np.sum(b * b, 1)
    g = 1 / np.sqrt(1 - b2)
    bp = np.sum(b * p4[:, 1:], 1)
    coef = np.where(b2 > 0, (g - 1) * bp / np.where(b2 > 0, b2, 1), 0) + g * p4[:, 0]
    out = np.empty_like(p4)
    out[:, 0] = g * (p4[:, 0] + bp)
    out[:, 1:] = p4[:, 1:] + coef[:, None] * b
    return out


def build(spin, m, n_out):
    pdf = T2.PDF(os.environ['T2_PDF'])
    T2.rng = np.random.default_rng(SEED)
    rng = np.random.default_rng(hseed(f'toy|{spin}|{m}'))
    ev = T2.sample_isr(pdf, float(m), spin, n=400000)
    w = ev['w']
    wmax = w.max()
    acc = rng.uniform(0, wmax, len(w)) < w
    ids = np.where(acc)[0]
    M, pT, y, phi = ev['M'][ids], ev['pT'][ids], ev['y'][ids], ev['phi'][ids]
    nn = len(ids)
    beta = np.sqrt(np.clip(1 - 4 * m * m / M ** 2, 0, 1))
    mT = np.sqrt(M ** 2 + pT ** 2)
    P4 = np.stack([mT * np.cosh(y), pT * np.cos(phi), pT * np.sin(phi), mT * np.sinh(y)], 1)
    bvec = P4[:, 1:] / P4[:, :1]
    # Collins-Soper axis in the pair rest frame (same construction as T2_kinematics.decay_and_observables)
    za = np.tile([1.0, 0, 0, 1.0], (nn, 1)); zb = np.tile([1.0, 0, 0, -1.0], (nn, 1))
    ka = boost(za, -bvec)[:, 1:]; kb = boost(zb, -bvec)[:, 1:]
    ka /= np.linalg.norm(ka, axis=1)[:, None]; kb /= np.linalg.norm(kb, axis=1)[:, None]
    zcs = ka - kb; zcs /= np.linalg.norm(zcs, axis=1)[:, None]
    tmp = np.where(np.abs(zcs[:, [0]]) < 0.9, np.array([[1.0, 0, 0]]), np.array([[0, 1.0, 0]]))
    e1 = np.cross(zcs, tmp); e1 /= np.linalg.norm(e1, axis=1)[:, None]; e2 = np.cross(zcs, e1)
    ct = np.empty(nn); todo = np.arange(nn)
    while len(todo):
        c = rng.uniform(-1, 1, len(todo)); r = rng.uniform(0, 1, len(todo))
        ok = (r * 2 <= 2 - beta[todo] ** 2 * (1 - c ** 2)) if spin == 'F' else (r <= 1 - c ** 2)
        ct[todo[ok]] = c[ok]; todo = todo[~ok]
    ph = rng.uniform(0, 2 * np.pi, nn); st = np.sqrt(1 - ct ** 2)
    nvec = ct[:, None] * zcs + (st * np.cos(ph))[:, None] * e1 + (st * np.sin(ph))[:, None] * e2
    pstar = 0.5 * M * beta
    q1 = np.concatenate([(M / 2)[:, None], pstar[:, None] * nvec], 1)
    q2 = np.concatenate([(M / 2)[:, None], -pstar[:, None] * nvec], 1)
    p1 = boost(q1, bvec); p2 = boost(q2, bvec)
    eta = np.arcsinh(P4[:, 3] / np.maximum(pT, 1e-9))
    bhat = bvec / np.linalg.norm(bvec, axis=1)[:, None]
    cstar = np.sum(nvec * bhat, 1)
    # keep the detector-relevant region, file order, first n_out events
    sel = np.where(np.abs(eta) < 2.5)[0][:n_out]
    k = len(sel)
    vt = np.zeros((k, 4))
    for i in range(k):
        g = np.random.default_rng(hseed(f'vtx|{spin}|{m}|{i}'))
        vt[i] = g.normal(0.0, [SIG_XY_MM, SIG_XY_MM, SIG_Z_MM, SIG_T_NS])
    one = np.ones(k)
    selection = dict(sample='TOY: T2_kinematics LO V*+jet, pT(QQ) > 200 GeV, |eta_pair| < 2.5, hit-or-miss unweighted',
                     seed=SEED, n_isr_trials=400000, n_accepted=int(nn), not_physics=True,
                     placeholders=['recoil', 'jets', 'wvar_ratio', 'w_lmax_*', 'w_qed*', 'sigma_*'])
    return dict(
        row=np.arange(k, dtype=np.int64), chunk=np.zeros(k, np.int64), ievt_lhe=np.arange(k, dtype=np.int64),
        py8_seed=np.zeros(k, np.int64), tt_split=np.zeros(k, np.int64), origin=np.zeros(k, np.int64), w_orig=one.copy(),
        wvar_ratio=np.ones((k, 1), np.float32), wvar_names=np.array(['placeholder']),
        p_qp=p1[sel, 1:].copy(), p_qm=p2[sel, 1:].copy(), recoil=-P4[sel].copy(), jets=np.zeros((k, 1, 4)),
        njet=np.ones(k, np.int64), gstar=(1 / np.sqrt(1 - beta ** 2))[sel], cstar=cstar[sel], eta=eta[sel], pt=pT[sel],
        M=M[sel], in_eta25=np.ones(k, bool), vtx_lumi=vt, w_lmax_up=one.copy(), w_lmax_dn=one.copy(), w_qed=one.copy(),
        w_qed_19=one.copy(), source_file=np.array('TOY(T2_kinematics)'), source_md5=np.array('none'),
        sigma_norm_fb=np.array(1.0), sigma_ref_fb=np.array(1.0), w_max=np.array(1.0),
        selection_json=np.array(json.dumps(selection)), spin=np.array(spin), m=np.array(float(m)), sel=np.array('toy'))


def main():
    out_dir, spin, m, n = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    d = build(spin, m, n)
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / f'{spin}_m{m}_toy.npz'
    part = out_dir / (final.name + '.part')
    with open(part, 'wb') as f:
        np.savez_compressed(f, **d)
        f.flush(); os.fsync(f.fileno())
    os.replace(part, final)
    sys.stderr.write(f'wrote {final} ({len(d["row"])} events)\n')


if __name__ == '__main__':
    main()
