"""p5_finder_triplet.py -- Stage-4 PROBE (E9, plan turn): second finder prototype (plan §2, F0 seeding), after p4 showed that
PS-pair seeds (0.25 mm out-of-plane errors) give ~1e5 loose seeds per PU-200 event with no discrimination.

Seeding here: IT triplets constrained to the PV inside the MET road.
  MET = pair pT = -recoil_T (Stage-3 `recoil` = ISR-system 4-vector; truth, the plan smears it).  Road: seed hits with
  |dphi(u, phi_MET)| < 0.25 + asin(min(1, W/r)), W = 20 mm (placeholder).
  Triplet: a in TBPX_L4, b in TBPX_L3 (|dphi_ab| < 0.3, |deta_ab| < 0.2), plane n = unit(u_a x u_b) through the PV;
  c in TBPX_L2 accepted if |n.u_c| < 3 sigma_tot,c (sigma incl. the seed-plane error); seed plane refitted from (a, b, c).
Collection and score as p4 (layers with >= 1 / >= 2 hits within 3 sigma_tot, forward of the PV, |u.n2| < 50 mm);
then 3 x PV-constrained weighted refit.  Signal flag is truth (measurement -> SimHit -> barcode 4000).
Placeholders only; nothing tuned on signal.  Run (theory_track):
  pixi run python acts/stage4/probes/p5_finder_triplet.py data/acts_stage4/p2/meas_sig_pu_L1_BM_c00.npz
Output: data/acts_stage4/p4/p5_<stem>.json
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
from numba import njit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_finder_proto import LAYC, STYPE, SID, sig_n, refit, OUT  # noqa: E402

W_ROAD = 20.0


@njit(cache=True)
def wrap(d):
    while d > np.pi:
        d -= 2 * np.pi
    while d < -np.pi:
        d += 2 * np.pi
    return d


@njit(cache=True)
def seeds_triplet(U, X, Y, TYP, S0, S1, LC, nlay, A, B, C, phiU, etaU, phimet, road):
    out = []
    ntrip = 0; npair = 0
    for ia in A:
        ra = np.hypot(U[ia, 0], U[ia, 1])
        if abs(wrap(phiU[ia] - phimet)) > road + np.arcsin(min(1.0, W_ROAD / ra)):
            continue
        for ib in B:
            rb = np.hypot(U[ib, 0], U[ib, 1])
            if abs(wrap(phiU[ib] - phimet)) > road + np.arcsin(min(1.0, W_ROAD / rb)):
                continue
            if abs(wrap(phiU[ia] - phiU[ib])) > 0.3 or abs(etaU[ia] - etaU[ib]) > 0.2:
                continue
            ua = U[ia]; ub = U[ib]
            c = np.cross(ua, ub); na = np.linalg.norm(ua); nb = np.linalg.norm(ub)
            sn = np.linalg.norm(c) / (na * nb)
            if sn < 1e-3:
                continue
            npair += 1
            n = c / np.linalg.norm(c)
            sseed = 0.03 / (nb * sn)            # ~ IT out-of-plane error / lever arm (rad)
            for ic in C:
                if abs(wrap(phiU[ic] - phiU[ib])) > 0.4:
                    continue
                uc = U[ic]
                d = uc[0] * n[0] + uc[1] * n[1] + uc[2] * n[2]
                sg = sig_n(n, X[ic], Y[ic], TYP[ic], S0[ic], S1[ic])
                if abs(d) > 3 * np.sqrt(sg * sg + (sseed * np.linalg.norm(uc)) ** 2):
                    continue
                ntrip += 1
                axis = ua / na + ub / nb; axis = axis / np.linalg.norm(axis)
                n2 = np.cross(n, axis)
                cnt = np.zeros(nlay, np.int32)
                for i in range(U.shape[0]):
                    if LC[i] < 0:
                        continue
                    if U[i, 0] * axis[0] + U[i, 1] * axis[1] + U[i, 2] * axis[2] <= 0:
                        continue
                    if abs(U[i, 0] * n2[0] + U[i, 1] * n2[1] + U[i, 2] * n2[2]) > 50.0:
                        continue
                    di = U[i, 0] * n[0] + U[i, 1] * n[1] + U[i, 2] * n[2]
                    ui = np.sqrt(U[i, 0] ** 2 + U[i, 1] ** 2 + U[i, 2] ** 2)
                    sgi = sig_n(n, X[i], Y[i], TYP[i], S0[i], S1[i])
                    if abs(di) < 3 * np.sqrt(sgi * sgi + (sseed * ui) ** 2):
                        cnt[LC[i]] += 1
                n1 = 0; n2c = 0
                for k in range(nlay):
                    if cnt[k] >= 1:
                        n1 += 1
                    if cnt[k] >= 2:
                        n2c += 1
                out.append((ia, ib, ic, n1, n2c))
    return out, npair, ntrip


def event(h, vtx, phimet, keep_signal=True, road=0.25):
    if not keep_signal:
        h = h[h[:, 6] == 0]
    # road pre-selection of ALL hits once per event (collection width 50 mm): |dphi(u, MET)| < road + asin(min(1, 50/r))
    u0 = h[:, 1:4] - vtx[None, :3]; r0 = np.hypot(u0[:, 0], u0[:, 1])
    dph = np.abs((np.arctan2(u0[:, 1], u0[:, 0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    h = h[dph < road + np.arcsin(np.minimum(1.0, 50.0 / r0))]
    sid = h[:, 0].astype(int)
    U = h[:, 1:4] - vtx[None, :3]
    X, Y = h[:, 1], h[:, 2]
    TYP = STYPE[sid]; LC = LAYC[sid]; S0, S1 = h[:, 4], h[:, 5]
    phiU = np.arctan2(U[:, 1], U[:, 0]); etaU = np.arcsinh(U[:, 2] / np.hypot(U[:, 0], U[:, 1]))
    t0 = time.time()
    A = np.where(sid == SID['TBPX_L4'])[0]; B = np.where(sid == SID['TBPX_L3'])[0]; C = np.where(sid == SID['TBPX_L2'])[0]
    out, npair, ntrip = seeds_triplet(U, X, Y, TYP, S0, S1, LC, LAYC.max() + 1, A, B, C, phiU, etaU, phimet, road)
    t_seed = time.time() - t0
    out.sort(key=lambda c: (-c[4], -c[3]))
    sigtrip = [o for o in out if h[o[0], 6] > 0 and h[o[1], 6] > 0 and h[o[2], 6] > 0][:20]
    fits = []
    for ia, ib, ic, n1, n2 in out[:30] + sigtrip:
        n = np.cross(U[ia], U[ib]); n /= np.linalg.norm(n)
        axis = U[ia] / np.linalg.norm(U[ia]) + U[ib] / np.linalg.norm(U[ib]); axis /= np.linalg.norm(axis)
        f = refit(U, X, Y, TYP, S0, S1, LC, n, axis)
        if f is None:
            continue
        fl = h[f['sel'], 6]
        f['n_sig_in'] = int(np.sum(fl > 0)); f['n_sig_tot'] = int(np.sum(h[:, 6] > 0)); f.pop('sel')
        f['seed_score'] = (int(n1), int(n2))
        fits.append(f)
    fits.sort(key=lambda f: (-f['nl2'], f['chi2ndf']))
    sigfits = [f for f in fits if f['n_sig_in'] >= 0.5 * f['nhit']]
    sig_ab = int(np.sum([(h[a, 6] > 0) and (h[b, 6] > 0) and (h[c, 6] > 0) for a, b, c, _, _ in out]))
    return dict(n_hits_road=len(h), n_pairs=npair, n_triplets=ntrip, n_triplets_all_signal=sig_ab,
                score_hist={f'{k}': int(sum(1 for o in out if o[4] == k)) for k in range(0, 12)},
                t_seed_s=round(t_seed, 2), t_total_s=round(time.time() - t0, 2),
                best_signal=None if not sigfits else {k: sigfits[0][k] for k in ('nl1', 'nl2', 'nhit', 'chi2ndf', 't_est_um', 'dw_mm', 'n_sig_in', 'n_sig_tot', 'seed_score')},
                rank_best_signal=None if not sigfits else fits.index(sigfits[0]),
                top3=[{k: f[k] for k in ('nl1', 'nl2', 'nhit', 'chi2ndf', 't_est_um', 'dw_mm', 'n_sig_in', 'n_sig_tot', 'seed_score')} for f in fits[:3]])


if __name__ == '__main__':
    f = Path(sys.argv[1])
    d = np.load(f)
    evs = sorted([k for k in d.files if k.startswith('ev') and k[2:].isdigit()], key=lambda k: int(k[2:]))
    rng = np.random.default_rng(7)
    res = dict(file=str(f), events=[])
    event(d[evs[0]][:3000], d['vtx'][0], 0.0)
    for i, k in enumerate(evs):
        h = d[k]; vtx = d['vtx'][i]; rec = d['recoil'][i]
        phimet = float(np.arctan2(-rec[2], -rec[1]))
        r_sig = event(h, vtx, phimet, True)
        r_pu = [event(h, vtx, float(rng.uniform(-np.pi, np.pi)), False) for _ in range(3)]   # PU-only, 3 random MET directions
        res['events'].append(dict(sig_pu=r_sig, pu_only=r_pu))
        b = r_sig['top3'][0] if r_sig['top3'] else None
        print(i, 'road hits', r_sig['n_hits_road'], 'pairs', r_sig['n_pairs'], 'trip', r_sig['n_triplets'], '(all-signal', r_sig['n_triplets_all_signal'], ') t', r_sig['t_total_s'],
              's | best:', None if b is None else (b['nl1'], b['nl2'], b['nhit'], round(b['chi2ndf'], 2), round(b['t_est_um'], 1), round(b['dw_mm'], 2), f"{b['n_sig_in']}/{b['n_sig_tot']}"),
              '| best SIGNAL cand:', None if r_sig['best_signal'] is None else (r_sig['best_signal']['nl1'], r_sig['best_signal']['nl2'], r_sig['best_signal']['nhit'], round(r_sig['best_signal']['chi2ndf'], 2), round(r_sig['best_signal']['t_est_um'], 1), round(r_sig['best_signal']['dw_mm'], 2), r_sig['best_signal']['n_sig_in'], 'rank', r_sig['rank_best_signal']),
              '| PU-only trip', [r['n_triplets'] for r in r_pu], 'best nl2', [r['top3'][0]['nl2'] if r['top3'] else None for r in r_pu],
              't', [r['t_total_s'] for r in r_pu])
    (OUT / f'p5_{f.stem}.json').write_text(json.dumps(res, indent=1, default=float))
