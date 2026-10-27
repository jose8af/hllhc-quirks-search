"""products.py -- Stage-5 inputs requested by stage5/proposed_schema.json (orchestrator, round 3 addition, 2026-10-14).

  acceptance.json   trigger + preselection acceptance A(m, Lambda, spin) per hypothesis (D1 preselection definition) and
                    the efficiency FACTOR BREAKDOWN (trigger / preselection / PV / fiducial / finder);
  edges_det.json    detector-level edges vs the Stage-3 truth edges (plan §11 item 3; V4-3);
  sep_it_det.json   sep_IT^det calibration vs the Stage-3 truth sep_IT (plan §11 item 4);
  event_display.npz one signal event and the best PU-only fake candidate, in-band hit dumps (plan §11 Stage-5 list).
LEVELS: the acceptance is TRUTH level (Stage-3 generator records: quirk-pair pT as the MET, the 4 stored truth jets
smeared 10 %/sqrt(E) + 5 %, plan §3) with exactly the D1 preselection of gen_d123.presel (trigger weight, MET_reco > 250,
>= 1 jet pT > 100 |eta| < 2.4, min dphi(jets pT > 30, MET_reco) > 0.5; vetoes cost the signal ~0, plan §3); edges,
sep_IT^det and the display are DETECTOR level (ACTS-hybrid A1 / A2 outputs).  Numbers only; no conclusion here.
"""
import json
import math

import numpy as np
from scipy.special import erf

from acts.stage4.analysis import common as C

NREP = 20
P2 = C.TT / 'sim' / 'stage3' / 'results' / 'P2.json'


def _dphi(a, b):
    return np.abs((a - b + np.pi) % (2 * np.pi) - np.pi)


def acceptance_point(spin, m, lam, seed=C.SEED):
    """A = sum_e w_e <eps_trig x presel>_rep 1[in_eta25] / sum_e w_e over the template half (tt_split == 0)."""
    idx = json.loads((C.TT / 'data' / 'sim_stage3' / 'STAGE3_INDEX.json').read_text())
    key = f'p2/{spin}_m{int(m)}/L{lam:g}_BM'
    if key not in idx['points']:
        return None
    P = []; J = []; W = []; F = []
    for ch in idx['points'][key]['chunks']:
        z = np.load(C.TT / 'data' / 'sim_stage3' / ch['file'])
        sel = z['tt_split'] == 0
        P.append((z['p_qp'] + z['p_qm'])[sel][:, :2]); J.append(z['jets'][sel]); W.append(z['w'][sel])
        F.append(z['in_eta25'][sel] > 0)
    P = np.concatenate(P); J = np.concatenate(J); W = np.concatenate(W); F = np.concatenate(F)
    rng = np.random.default_rng([seed, int(m), int(round(lam * 1000)), 0 if spin == 'F' else 1])
    met = P[None] + rng.normal(0, 25.0, (NREP,) + P.shape)
    mv = np.hypot(met[..., 0], met[..., 1]); ph = np.arctan2(met[..., 1], met[..., 0])
    trig = 0.98 * 0.5 * (1 + erf((mv - 200.0) / (20.0 * math.sqrt(2))))
    jpt, jeta, jphi = J[:, :, 0], J[:, :, 1], J[:, :, 2]
    e = jpt * np.cosh(jeta)
    res = np.hypot(0.10 / np.sqrt(np.maximum(e, 1e-3)), 0.05)
    spt = jpt[None] * np.maximum(0.0, 1 + res[None] * rng.standard_normal((NREP,) + jpt.shape))
    lead = ((spt > 100) & (np.abs(jeta[None]) < 2.4)).any(-1)
    jdp = np.where((spt > 30) & (np.abs(jeta[None]) < 4.7), _dphi(jphi[None], ph[..., None]), 9.0).min(-1)
    pre = (mv > 250) & lead & (jdp > 0.5)
    wt = W.sum()
    eps_fid = float((W * F).sum() / wt)
    trig_m = trig.mean(0); tp = (trig * pre).mean(0)
    eps_trig = float((W * F * trig_m).sum() / max((W * F).sum(), 1e-300))
    A = float((W * F * tp).sum() / wt)
    eps_pre = A / max(eps_fid * eps_trig, 1e-300)
    n_eff = wt ** 2 / (W ** 2).sum()
    return dict(A_trig_presel=A, err_rel=float(math.sqrt(max(1 - A, 0) / max(A * n_eff, 1e-12))), level='truth (Stage-3)',
                factors=dict(fiducial_eta25=eps_fid, trigger=eps_trig, preselection_given_trigger=eps_pre,
                             PV=1.0, PV_note='PV-ID not modelled (truth vertex smeared; plan §3 factor eps_PV-ID = 1, '
                                             'UNVERIFIED)'),
                n_events=int(len(W)), definition='A = eps_fid x eps_trig x eps_presel|trig (template half, w-weighted)')


def acceptance(sig):
    out = dict(label='trigger + preselection acceptance (truth level) and efficiency factor breakdown', points={})
    for kind in ('a2',):              # REVIEW R3 B-2: only A2 shares A's denominator (template half, in_eta25, all status)
        for key, t in sig.get(kind, {}).get('points', {}).items():
            if t.get('cfg') != 'BM':
                continue
            a = acceptance_point(t['spin'], t['m'], t['lam'])
            if a is None:
                continue
            fin = {k: v['eps'] for k, v in t.get('report_rungs', {}).items()}
            a['factors']['finder_at_report_rungs'] = fin
            a['factors']['finder_note'] = ('A2 finder eps = matched & rung & f_CKF < 0.2 over every TEMPLATE-half, '
                                           '|eta_pair| < 2.5 (in_eta25) counting row, status != 1 as failures -- the same '
                                           'events as A (whose eps_fid covers in_eta25); eps_total = A x eps_finder '
                                           'assumes the finder eps independent of the preselection (factorised chain, '
                                           'plan §3). A1 (both halves, all eta, status 1) and A5 (status 1) have other '
                                           'denominators and are NOT paired with A here.')
            out['points'][key] = a
    return out


def _half_max_edges(lams, eff):
    """Lower / upper edges = ln-Lambda interpolated half-maximum crossings of eps(Lambda)."""
    x = np.log(np.asarray(lams, float)); y = np.asarray(eff, float)
    o = np.argsort(x); x = x[o]; y = y[o]
    if not len(y) or y.max() <= 0:
        return None, None
    h = 0.5 * y.max(); k = int(np.argmax(y))
    lo = up = None
    for i in range(k, 0, -1):
        if y[i - 1] < h <= y[i]:
            lo = float(np.exp(x[i - 1] + (h - y[i - 1]) / (y[i] - y[i - 1]) * (x[i] - x[i - 1]))); break
    for i in range(k, len(y) - 1):
        if y[i] >= h > y[i + 1]:
            up = float(np.exp(x[i] + (y[i] - h) / (y[i] - y[i + 1]) * (x[i + 1] - x[i]))); break
    return lo, up


def edges(sig_rows, b84=None, nboot=200, seed=C.SEED):
    """Detector-level edges per spin|m and sample at R04 (R_A) and R14 (R_D), with a row-level bootstrap applied
    JOINTLY across Lambda (A2 rows are shared across Lambda; plan §4.1), vs the Stage-3 truth edges (P2.json)."""
    truth = json.loads(P2.read_text())['edges'] if P2.exists() else {}
    rng = np.random.default_rng(seed)
    groups = {}
    for kind, z in sig_rows.items():
        keys = sorted({k.rsplit('|', 1)[0] for k in z.files if k.count('|') == 5})   # REVIEW R4 B-1: skip 'provenance'
        for key in keys:
            smp, spin, m, lam, cfg = key.split('|')
            if cfg != 'BM':
                continue
            groups.setdefault((smp, spin, m), []).append((float(lam), z[key + '|rows'], z[key + '|L']))
    out = dict(label='detector-level edges (half-maximum crossings in ln Lambda; row-level bootstrap jointly across '
                     'Lambda) vs Stage-3 truth edges', points={})
    for (smp, spin, m), lst in groups.items():
        lst.sort()
        lams = [x[0] for x in lst]
        ent = dict(sample=smp, lam_keV=lams, truth=truth.get(f'{spin}_m{m}'))
        allrows = np.unique(np.concatenate([x[1] for x in lst]))
        for rname, col in (('R04', 3), ('R14', 13)):
            eff = [float(x[2][:, col].mean()) if len(x[1]) else 0.0 for x in lst]
            lo, up = _half_max_edges(lams, eff)
            bl, bu = [], []
            for _ in range(nboot):
                pick = rng.choice(allrows, len(allrows), replace=True)
                cnt = {r: c for r, c in zip(*np.unique(pick, return_counts=True))}
                eb = []
                for lam, rows, L in lst:
                    wv = np.array([cnt.get(r, 0) for r in rows], float)
                    eb.append(float((wv * L[:, col]).sum() / max(wv.sum(), 1)))
                a, b = _half_max_edges(lams, eb)
                bl.append(a); bu.append(b)
            sd = lambda v: float(np.std([q for q in v if q is not None], ddof=1)) if sum(q is not None for q in v) > 2 \
                else None                                                     # noqa: E731
            ent[rname] = dict(eff=eff, lower=dict(value=lo, stat_err=sd(bl), definition='half-maximum, ln Lambda'),
                              upper=dict(value=up, stat_err=sd(bu), definition='half-maximum, ln Lambda'),
                              b84_label=(b84 or {}).get(rname))
        out['points'][f'{smp}|{spin}|{m}'] = ent
    return out


def sep_it_det(obs_by_kind):
    """Per point: median sep_IT^det (mm) of the matched candidates passing R04 vs the Stage-3 truth median sep_IT."""
    truth = json.loads(P2.read_text()).get('sep_IT_handle', {}) if P2.exists() else {}
    out = dict(label='sep_IT^det (detector level; median over matched CANDIDATES passing R04, f_CKF not applied; CORE '
                     'hits only, FIX R6) vs Stage-3 truth median sep_IT', points={},
               pu200_measurable=False, pu200_note='PU-200 (A2/A5) values flagged NOT MEASURABLE per point; only the A1 '
                                                  '(no PU) values are a detector-level sep_IT^det')
    for kind, z in obs_by_kind.items():
        keys = z['key']; L = z['L']; s = z['sep_it_det_mm']
        for key in np.unique(keys):
            m_ = (keys == key) & L[:, 3] & np.isfinite(s)
            smp, spin, mm, lam, cfg = str(key).split('|')
            t = truth.get(f'{spin}_m{mm}', {})
            tl = t.get('lam_keV', []); tv = t.get('sep_IT_med_um', [])
            tmed = next((v / 1000.0 for l_, v in zip(tl, tv) if abs(l_ - float(lam)) < 1e-9), None)
            v = s[m_]
            pu = smp != 'A1'                     # A2 / A5 (and the A2FC replacements): PU 200
            out['points'][str(key)] = dict(sep_det_median_mm=float(np.median(v)) if len(v) else None,
                                           err_mm=float(1.2533 * np.std(v) / math.sqrt(len(v))) if len(v) > 1 else None,
                                           n=int(len(v)), sep_truth_median_mm=tmed, pu200=bool(pu),
                                           measurable=not pu,
                                           flag=('NOT MEASURABLE AT PU 200 with this estimator (FIX R6, INV_SIGNAL_EFF '
                                                 '§5): core-only still PU-dominated (13-20 mm vs 1-7 mm truth at E500); '
                                                 'number kept for the record, not a Lambda handle') if pu else None)
    return out


def event_display(obs_a2, b1_jobs, out_path):
    """One signal event (the first A2 matched candidate passing the deepest ladder rung reached) and the best-ranked
    PU-only fake (B1 S4 record passing the deepest in-job ladder rung), in-band hit dumps."""
    X = []; Y = []; Z = []; CL = []
    lab = {}
    if obs_a2 is not None and len(obs_a2['key']):
        L = obs_a2['L']; depth = L[:, :14].sum(1)
        i = int(np.argmax(depth))
        d = C.load_npz(str(obs_a2['src_file'][i]), prefix=('hit.',))
        k = int(obs_a2['hitrec'][i]); h = d['hit.ref'][d['hit.off'][k]:d['hit.off'][k + 1]]
        q = (d['hit.INT'][h] % 1_000_000) == C.SIG_VP
        X += list(d['hit.xyz'][h, 0]); Y += list(d['hit.xyz'][h, 1]); Z += list(d['hit.xyz'][h, 2])
        CL += [1 if x else 0 for x in q]
        lab['signal'] = dict(key=str(obs_a2['key'][i]), row=int(obs_a2['row'][i]), depth=int(depth[i]),
                             met_phi=float(obs_a2['phimet_reco'][i]))
    best = None
    for dj in b1_jobs:
        c = dj['cand']
        F = C.rung_flags(c['rungs']); full = (c['tag'] & 4) > 0
        dep = F[:, :14].sum(1) * full
        if len(dep) and (best is None or dep.max() > best[0]):
            best = (int(dep.max()), dj, int(np.argmax(dep)))
    if best is not None:
        dep, dj, i = best
        d = C.load_npz(dj['path'], prefix=('hit.',))
        c = dj['cand']
        t, ci = int(c['trial'][i]), int(c['idx'][i])
        k = int(np.where((d['hit.trial'] == t) & (d['hit.cand'] == ci))[0][0])
        h = d['hit.ref'][d['hit.off'][k]:d['hit.off'][k + 1]]
        X += list(d['hit.xyz'][h, 0]); Y += list(d['hit.xyz'][h, 1]); Z += list(d['hit.xyz'][h, 2])
        CL += [2] * len(h)
        lab['pu_fake'] = dict(job=dj['job_id'], trial=t, depth=dep, met_phi=float(dj['tr']['trials_phimet'][t])
                              if 'trials_phimet' in dj['tr'] else None)
    np.savez_compressed(out_path, x=np.array(X, np.float32), y=np.array(Y, np.float32), z=np.array(Z, np.float32),
                        cls=np.array(CL, np.int8), cls_names=np.array(['PU (signal event)', 'quirk', 'PU-only fake']),
                        met_phi=np.array([lab.get('signal', {}).get('met_phi', np.nan)]),
                        label=np.array(json.dumps(lab)))
    return lab
