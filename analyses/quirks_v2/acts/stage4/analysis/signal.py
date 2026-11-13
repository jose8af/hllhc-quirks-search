"""signal.py -- signal efficiencies per hypothesis (spin, m, Lambda) and per rung for A1 (no PU), A2core and A5core
(PU 200, TDR top-up), with the PRE-DECLARED signal match (hitrec.signal_match), the D4-17 (i) admissibility logic
(admissibility.py) and the per-event D4-13 / P2 observables.

What 'event passes rung r' means here (WP_RULE §1.2, §3, §8; LOG 2026-10-13 20:35):
  some candidate of the event's trial (a) is signal-matched (>= 3 core quirk hits in >= 3 distinct layers, >= 50 % of
  its core hits), (b) passes the cumulative in-job rung flags (fixed cuts |dphi| < delta95, |eta(n3)| < 1.0 included),
  (c) has f_CKF < 0.2 (a selection cut for signal at every rung, §1.2), and for the factorised F1 rungs (d) passes the
  h / o thresholds (undefined passes, §1.4 [D6]).
  The match needs the core, i.e. the stored full hit record (S4: R04 and (w_core < 37.5 or p > 1e-3)).  Every rung
  >= R05 and every fallback selection lies inside S4, so these are exact.  R01-R04 (and the N_L2 diagnostics) are
  LOWER BOUNDS (a matched candidate passing R04 with w_core >= 37.5 and p <= 1e-3 has no hit record); they are labelled.
Denominator: every counting row not probe-excluded (WP_RULE §5.4 item 10), whether or not a trial ran; Stage-3
status != 1 rows count as failures (REVIEW R1 B-6, plan §1.3 'carried as an efficiency loss').
SR-T: only the in-job first factor (>= 1 in-band BTL hit, cand.btl_n_band > 0) here; the PC-19 window / PV time / OOT
overlay part is srt.signal_srt (needs C1 B1 S5 hits).

THIS MODULE REPORTS NUMBERS ONLY.  No physics conclusion, no optimisation; WP_RULE §5.4 item 8: signal templates are
used only to report efficiencies at the selections the rule fixes.
"""
import time

import numpy as np

from acts.stage4.analysis import common as C
from acts.stage4.analysis import hitrec as HR

NL = 23
FB_COLS = [C.COL[n] for n in C.RUNGS[17:37]]          # FB0..FB4, FB_k e>x  (20 fallback F0 parts)
FB_NAMES = C.RUNGS[17:37]
F0E_COLS = [14, 15, 16]


def point_of(job, lam=None):
    if job['kind'] == 'a2':
        return job['spin'], float(job['m']), float(lam)
    sp = job['point'].split('/')
    spin, m = sp[1].split('_m')
    cfg = sp[2].split('_', 1)[1] if '_' in sp[2] else 'BM'
    return spin, float(m), float(sp[2].split('_')[0][1:]), cfg, sp[0]


def ladder_flags(F, hv, ov):
    """(ncand, 23) cumulative ladder flags from the in-job F (ncand, 43) and h, o (WP_RULE §3, §6.2 composition)."""
    n = len(F)
    L = np.zeros((n, NL), bool)
    L[:, :14] = F[:, :14]
    hv = np.asarray(hv, float); ov = np.asarray(ov, float)
    hp = [~np.isfinite(hv) | (hv > t) for t in C.H_MIN]                   # undefined passes (§1.4 [D6])
    op = [~np.isfinite(ov) | (ov > t) for t in C.O_MIN]
    L[:, 14] = L[:, 13] & hp[0]; L[:, 15] = L[:, 13] & hp[1]; L[:, 16] = L[:, 13] & hp[2]
    L[:, 17] = L[:, 16] & op[0]; L[:, 18] = L[:, 16] & op[1]; L[:, 19] = L[:, 16] & op[2]
    for i, c in enumerate(F0E_COLS):                      # R21-R23 = R14 & dE/dx > e_x (column F0e>x) & h>5 & o>5
        L[:, 20 + i] = F[:, c] & hp[2] & op[2]
    fb = F[:, FB_COLS] & (hp[2] & op[2])[:, None]         # r_fb candidates: FB_k[e] & h > 5 & o > 5
    return L, fb


C_MM_NS = 299.792458
_POINTS = {}


def stage3_point(spin, m, lam):
    from acts.stage4.code import s4sig as S
    k = S.point_key(spin, m, lam)
    if k not in _POINTS:
        _POINTS[k] = S.Point(k)
    return _POINTS[k]


def met_reco(spin, m, lam, row):
    """Reproduces run_g1b.sig_event_inputs -> g1b_tt.pv_met: rng = default_rng(hseed('sig-pvmet', spin, m, row)),
    3 PV normals then MET = truth MET + N(0, 25 GeV) per component.  -> (MET vector, t_PV = true vertex time in ns)."""
    from acts.stage4.code import s4sig as S
    P = stage3_point(spin, m, lam)
    h, ev = P.event(row)
    met_true = np.asarray(ev['p_qp'][:2], float) + np.asarray(ev['p_qm'][:2], float)
    rs = np.random.default_rng(S.hseed('sig-pvmet', spin, P.m, row))
    rs.normal(0.0, 1.0, 3)
    met = met_true + rs.normal(0.0, 25.0, 2)
    return met, float(ev['vtx'][3]), float(ev['eta'])


def btl_inband(B, pv, n, a, ttol=0.030, wc=75.0):
    """numpy replica of weights._btl_inband (WP_RULE §1.4 in-band BTL hit).  B columns: sid, x, y, z, s0, s1, dE, t."""
    if not len(B):
        return np.zeros(0, bool), np.zeros((0, 3))
    u = B[:, 1:4] - pv[None, :]
    n2 = np.cross(n, a)
    r = np.hypot(B[:, 1], B[:, 2]); cx = B[:, 1] / r; cy = B[:, 2] / r
    aa = -n[0] * cy + n[1] * cx
    sn = np.sqrt(aa ** 2 * B[:, 4] ** 2 + n[2] ** 2 * B[:, 5] ** 2)
    st2 = np.maximum(sn, 1e-4) ** 2 + ttol ** 2
    m = (u @ a > 0) & (np.abs(u @ n2) < wc) & ((u @ n) ** 2 < 9.0 * st2)
    return m, u


def tof_obs(B, pv, n, a, t_pv):
    """beta_ToF of the earliest in-band BTL hit (PC-19 'earliest': smallest raw t among in-band hits with
    dt > -12.5 ns), t_PV = the true vertex time (PC-19 signal convention)."""
    m, u = btl_inband(B, pv, n, a)
    if not m.any():
        return dict(beta=np.nan, dt=np.nan, n_band=0, t_raw=np.inf)
    L = np.linalg.norm(u, axis=1)
    dt = B[:, 7] - t_pv - L / C_MM_NS
    ok = m & (dt > -12.5)
    if not ok.any():
        return dict(beta=np.nan, dt=np.nan, n_band=int(m.sum()), t_raw=np.inf)
    j = np.where(ok)[0][np.argmin(B[ok, 7])]
    tof = B[j, 7] - t_pv
    beta = L[j] / (C_MM_NS * tof) if tof > 0 else np.inf
    return dict(beta=float(beta), dt=float(dt[j]), n_band=int(m.sum()), t_raw=float(B[j, 7]))


def analyse_file(rec, want_f1=True, obs=True):
    """One A1/A2/A5 output -> list of per-entry dicts (one per sig.tab row) with pass flags and observables."""
    d = rec['d']; job = rec['job']
    tab = d['sig.tab']; cols = [str(c) for c in d['sig.cols']]
    ci = {c: i for i, c in enumerate(cols)}
    strial = d['sig.trial']
    lk = HR.cand_lookup(d) if 'cand.trial' in d else {}
    Fc = C.rung_flags(d['cand.rungs']) if 'cand.rungs' in d else np.zeros((0, C.NR), bool)
    # matched full-record candidates, per trial
    per_trial = {}
    chk = dict(n_records=0, n_core_mismatch=0, max_rel_dw=0.0, n_matched=0)
    for k, tr, cidx, h in HR.iter_records(d):
        i = lk[(tr, cidx)]
        pv = d['trials.pv'][tr]
        g = HR.geom(d, h, pv, d['cand.normal'][i], d['cand.axis'][i])
        cm, c, w = HR.core(g)
        chk['n_records'] += 1
        chk['n_core_mismatch'] += int(cm.sum() != int(d['cand.n_core'][i]))
        if np.isfinite(w) and d['cand.dw_core'][i] > 0:
            chk['max_rel_dw'] = max(chk['max_rel_dw'], abs(w / float(d['cand.dw_core'][i]) - 1))
        mt, nc, nq, nl = HR.signal_match(d, h, g, cm)
        if not mt:
            continue
        chk['n_matched'] += 1
        F = Fc[i]
        need_f1 = want_f1 and (F[13] or F[FB_COLS].any())
        hv = HR.h_var(g, c, pv) if need_f1 else np.nan
        ov = HR.o_var(g, c) if need_f1 else np.nan
        per_trial.setdefault(tr, []).append(dict(i=i, F=F, h=hv, o=ov, f1_done=need_f1, n_core=nc, n_q_core=nq,
                                                 n_q_layers=nl, sep_it=HR.sep_it(g, c, cm), k=k))   # R6: core only
    ents = []
    for e in range(len(tab)):
        row = tab[e]
        ti = int(strial[e])
        lam = float(row[ci['lam']])
        ent = dict(row=int(row[ci['row']]), lam=lam, status=int(row[ci['status']]),
                   probe_excluded=int(row[ci['probe_excluded']]), skipped=int(row[ci['skipped']]), trial=ti,
                   n_q_written=int(row[ci['n_q_written']]))
        cands = per_trial.get(ti, []) if ti >= 0 else []
        P = np.zeros(C.NR, bool); PT = np.zeros(C.NR, bool); L = np.zeros(NL, bool); LT = np.zeros(NL, bool)
        FBp = np.zeros(20, bool); FBpT = np.zeros(20, bool)
        best = None
        if cands:
            idx = np.array([x['i'] for x in cands])
            F = np.array([x['F'] for x in cands])
            okf = np.nan_to_num(d['cand.f_ckf'][idx].astype(float), nan=1.0) < 0.2
            pres = d['cand.btl_n_band'][idx] > 0 if 'cand.btl_n_band' in d else np.zeros(len(idx), bool)
            hv = np.array([x['h'] for x in cands]); ov = np.array([x['o'] for x in cands])
            Lc, fbc = ladder_flags(F, hv, ov)
            sel = okf[:, None]
            P = (F & sel).any(0); PT = (F & (sel & pres[:, None])).any(0)
            L = (Lc & sel).any(0); LT = (Lc & (sel & pres[:, None])).any(0)
            FBp = (fbc & sel).any(0); FBpT = (fbc & (sel & pres[:, None])).any(0)
            if obs:      # observables of the best matched candidate (rank order = finder order: lowest index)
                j = int(np.argmin(idx))
                ii = int(idx[j])
                best = dict(cand=ii, eta_axis=float(d['cand.eta_axis'][ii]), dedx=float(d['cand.dedx'][ii]),
                            w_core=float(d['cand.dw_core'][ii]), p_chi2core=float(d['cand.p_chi2core'][ii]),
                            f_ckf=float(d['cand.f_ckf'][ii]), btl_n_band=int(d['cand.btl_n_band'][ii])
                            if 'cand.btl_n_band' in d else -1, btl_dt0=float(d['cand.btl_dt0'][ii])
                            if 'cand.btl_dt0' in d else np.nan, h=float(cands[j]['h']), o=float(cands[j]['o']),
                            dphi_met=float(d['cand.dphi_met'][ii]), nip2=int(d['cand.nip2'][ii]),
                            n2s2=int(d['cand.n2s2'][ii]))
        if obs and cands:
            spin_, m_, lam_ = (job['spin'], float(job['m']), lam) if job['kind'] == 'a2' else point_of(job)[:3]
            met, t_pv, eta_pair = met_reco(spin_, m_, lam_, ent['row'])
            ie = int(d['trials.ev'][ti])
            pv = d['trials.pv'][ti]
            B = np.zeros((0, 8))
            if 'btl' in d:
                bb = d['btl'][d['btl'][:, 0] == ie]
                B = bb[:, 1:9].astype(np.float64)
            if 'sig.qbtl' in d:
                qb = d['sig.qbtl'][d['sig.qbtl'][:, 0] == ti]
                B = np.concatenate([B, qb[:, 1:9].astype(np.float64)])
            rows_ = []
            for q, x in enumerate(cands):
                ii = x['i']
                nrm = d['cand.normal'][ii].astype(np.float64); axs = d['cand.axis'][ii].astype(np.float64)
                to = tof_obs(B, pv, nrm, axs, t_pv)
                bg = to['beta'] / np.sqrt(1 - to['beta'] ** 2) if (np.isfinite(to['beta']) and to['beta'] < 1) else np.nan
                eta = float(d['cand.eta_axis'][ii])
                rows_.append(dict(cand=int(ii), met=float(np.hypot(*met)), phimet_reco=float(np.arctan2(met[1], met[0])),
                                  phimet_stored=float(d['trials.phimet'][ti]), eta_axis=eta, eta_pair=eta_pair,
                                  dedx=float(d['cand.dedx'][ii]), w_core=float(d['cand.dw_core'][ii]),
                                  h=float(x['h']), o=float(x['o']), beta_tof=to['beta'], dt_earliest=to['dt'],
                                  btl_n_band=to['n_band'], btl_n_band_stored=int(d['cand.btl_n_band'][ii])
                                  if 'cand.btl_n_band' in d else -1,
                                  M_est=float(np.hypot(*met) * np.cosh(eta) / bg) if np.isfinite(bg) and bg > 0
                                  else np.nan, f_ckf=float(d['cand.f_ckf'][ii]),
                                  spin=spin_, m=m_, lam=lam_, t_pv=t_pv, t_raw_in=to['t_raw'], pv=pv.tolist(),
                                  sep_it_det_mm=float(x['sep_it']), hitrec=int(x['k']), src_file=str(rec['path']),
                                  normal=nrm.tolist(), axis=axs.tolist(),
                                  L=Lc[q], FB=fbc[q]))
            ent['obs'] = rows_
        ent.update(P=P, PT=PT, L=L, LT=LT, FB=FBp, FBT=FBpT, best=best)
        # in-job definition (>= 50 % of written quirk measurements): diagnostic only
        ent['P_injob_def'] = np.unpackbits(d['sig.eff_fckf'][e])[:C.NR].astype(bool)
        ents.append(ent)
    return ents, chk


def aggregate(files, log=print, want_f1=True, obs=True):
    """-> dict keyed 'sample|spin|m|lam[|cfg]' with counts per rung, and per-row pass matrices (for the row bootstrap)."""
    acc = {}
    checks = dict(n_files=0, n_records=0, n_core_mismatch=0, max_rel_dw=0.0, n_matched=0)
    t0 = time.time()
    for rec in files:
        job = rec['job']
        ents, chk = analyse_file(rec, want_f1=want_f1, obs=obs)
        checks['n_files'] += 1
        for k in ('n_records', 'n_core_mismatch', 'n_matched'):
            checks[k] += chk[k]
        checks['max_rel_dw'] = max(checks['max_rel_dw'], chk['max_rel_dw'])
        for e in ents:
            if job['kind'] == 'a2':
                spin, m, lam = point_of(job, e['lam']); cfg = 'BM'; camp = 'p2'
            else:
                spin, m, lam, cfg, camp = point_of(job)
            key = f"{job['sample']}|{spin}|{m:g}|{lam:g}|{cfg}"
            a = acc.setdefault(key, dict(sample=job['sample'], spin=spin, m=m, lam=lam, cfg=cfg, rows=[], P=[], PT=[],
                                         L=[], LT=[], FB=[], FBT=[], Pinj=[], status_ne1=0, probe_excluded=0,
                                         no_trial=0, best=[]))
            if e['status'] != 1:               # REVIEW R1 B-6: carried in the denominator as a failure (plan §1.3)
                a['status_ne1'] += 1
                for k_ in ('P', 'PT', 'L', 'LT', 'FB', 'FBT', 'P_injob_def'):
                    e[k_] = np.zeros_like(e[k_])
                e['obs'] = []
            if e['probe_excluded']:
                a['probe_excluded'] += 1; continue
            a['no_trial'] += int(e['trial'] < 0)
            a['rows'].append(e['row'])
            for k_, s_ in (('P', 'P'), ('PT', 'PT'), ('L', 'L'), ('LT', 'LT'), ('FB', 'FB'), ('FBT', 'FBT'),
                           ('Pinj', 'P_injob_def')):
                a[k_].append(e[s_])
            a['best'].append(e['best'])
            for o in e.get('obs') or []:
                a.setdefault('obs', []).append(dict(o, row=e['row']))
        if checks['n_files'] % 20 == 0:
            log(f"signal: {checks['n_files']} files, {time.time() - t0:.0f} s")
    for a in acc.values():
        for k in ('P', 'PT', 'L', 'LT', 'FB', 'FBT', 'Pinj'):
            a[k] = np.array(a[k], bool).reshape(len(a['rows']), -1)
    return acc, checks


def eff_table(a):
    """Counts and efficiencies of one hypothesis/sample (CP 68 % intervals; row bootstrap is done jointly across
    Lambda by the caller where needed)."""
    n = len(a['rows'])

    def tab(M, names):
        k = M.sum(0) if n else np.zeros(len(names))
        lo, hi = C.clopper_pearson(k, max(n, 1))
        return {nm: dict(k=int(k[i]), eps=float(k[i] / n) if n else None, cp68=[float(lo[i]), float(hi[i])])
                for i, nm in enumerate(names)}
    out = dict(sample=a['sample'], spin=a['spin'], m=a['m'], lam=a['lam'], cfg=a['cfg'], n_den=n,
               excluded=dict(probe_excluded=a['probe_excluded']), status_ne1_counted_as_failure=a['status_ne1'],
               no_trial=a['no_trial'],
               injob_columns=tab(a['P'], C.RUNGS), injob_columns_T_present=tab(a['PT'], C.RUNGS),
               ladder=tab(a['L'], C.LADDER_NAMES), ladder_T_present=tab(a['LT'], C.LADDER_NAMES),
               fallback=tab(a['FB'], [f + '&h>5&o>5' for f in FB_NAMES]),
               fallback_T_present=tab(a['FBT'], [f + '&h>5&o>5' for f in FB_NAMES]),
               injob_definition_diag=tab(a['Pinj'], C.RUNGS),
               lower_bound_columns=[C.RUNGS[i] for i in (0, 1, 2, 3)] + C.RUNGS[37:] + C.LADDER_NAMES[:4],
               lower_bound_label='LOWER BOUND (D9): matched only via S4 hit records',
               note='eps = matched (pre-declared core match) & rung & f_CKF<0.2; R01-R04 and L2>= columns are lower '
                    'bounds (S4 hit-record coverage); *_T_present = SR-T first factor only (>=1 in-band BTL hit), not '
                    'the PC-19 window; injob_definition_diag = the run_g1b (>=50 % of written quirk measurements) '
                    'definition, diagnostic only')
    out['report_rungs'] = {k: out['ladder'][C.LADDER_NAMES[i]] for k, i in
                           (('R_A', 3), ('R_B', 5), ('R_C', 7), ('R_D', 13), ('R_E', 22))}
    return out


def self_consistency(acc, checks):
    """Mechanical checks (no physics): monotonic cumulative ladder; eps(new match) <= 1; T-present <= full; the core
    recomputation agrees with the stored n_core / w_core."""
    res = dict(core_recompute=dict(n_records=checks['n_records'], n_core_mismatch=checks['n_core_mismatch'],
                                   max_rel_dw=checks['max_rel_dw'],
                                   pass_=checks['n_core_mismatch'] <= 1e-5 * max(checks['n_records'], 1) and
                                   checks['max_rel_dw'] < 1e-3,
                                   tolerance='<= 1e-5 of the records: float32 xyz / normal at the closed core boundary '
                                             '(A2: 2 / 620 118 seen; cf. the 1 / 2e6 BTL band-edge case at G3)'))
    bad_mono = []; bad_T = []; bad_fb = []
    for key, a in acc.items():
        if not len(a['rows']):
            continue
        L = a['L']
        lad = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        for i in range(1, len(lad)):
            if np.any(L[:, lad[i]] & ~L[:, lad[i - 1]]):
                bad_mono.append((key, C.LADDER_NAMES[lad[i]]))
        for i in (20, 21, 22):                         # R21-23 subset of R20? R2x = R14&e&h5&o5 subset of R20
            if np.any(L[:, i] & ~L[:, 19]):
                bad_mono.append((key, C.LADDER_NAMES[i]))
        if np.any(a['PT'] & ~a['P']) or np.any(a['LT'] & ~a['L']):
            bad_T.append(key)
        # FB_k & F1 subset of FB_{k-1} & F1 (tighter width), and FB4 & F1 within ladder R20 for k = 4 is NOT implied
        # (FB has no R12/R13 ordering issue: FB0 = R04 & p>0.05 & 2S2>=3)
        FB = a['FB']
        for k in range(1, 5):
            if np.any(FB[:, k] & ~FB[:, k - 1]):
                bad_fb.append((key, k))
    ob = [o for a in acc.values() for o in a.get('obs', [])]
    if ob:
        dphi = np.array([abs(np.angle(np.exp(1j * (o['phimet_reco'] - o['phimet_stored'])))) for o in ob])
        dn = np.array([o['btl_n_band'] - o['btl_n_band_stored'] for o in ob])
        bt = np.array([o['beta_tof'] for o in ob])
        res['met_recompute'] = dict(n=len(ob), max_abs_dphi=float(dphi.max()), pass_=bool(dphi.max() < 1e-6))
        res['btl_inband_recompute'] = dict(n=len(ob), n_mismatch=int(np.sum(dn != 0)), pass_=bool(np.all(dn == 0)))
        res['beta_tof_range'] = dict(n_finite=int(np.isfinite(bt).sum()), n_ge1=int(np.sum(bt >= 1)),
                                     note='beta >= 1: earliest in-band hit not later than light from the PV (PU or '
                                          'prompt); M_est undefined there')
    res.update(ladder_monotonic=dict(pass_=not bad_mono, violations=bad_mono[:20]),
               T_present_subset=dict(pass_=not bad_T, violations=bad_T[:20]),
               fb_nested=dict(pass_=not bad_fb, violations=bad_fb[:20]))
    return res


# ================================================================================================ V4-6 revert (FIX R6)
REVERT_SET = C.S4 / 'investigation' / 'V46_REVERT_SET.json'


def a2fc_revert_set(path=REVERT_SET):
    """Pre-registered V4-6 revert rule (plan l.1254-1255, l.1813): the (spin, m, Lambda) A2 points whose CKF
    signal-stealing fraction exceeds 5 % (investigation/V46_REVERT_SET.json, 'revert_set').  -> [(spin, m, lam)]."""
    import json
    if not path.exists():
        return []
    d = json.loads(path.read_text())
    rs = d.get('revert_set')
    if rs is None:
        rs = [x for x in d.get('table', []) if x.get('revert')]
    return [(str(x['spin']), float(x['m']), float(x['lam'])) for x in rs]


def apply_a2fc(acc_a2, acc_fc, revert, fc_jobs=None, dev=False, log=print):
    """FIX R6 (V4-6 revert rule): for every revert-set point the A2 (numpy quirk hits, no quirk CKF) entry is REPLACED
    by the A2FC full-chain entry (ACTS digitisation + CKF with PU; same rows, same PU seeds, same PV/MET/top-up/trial
    seeds; run_a2fc.py).  The replacement must cover exactly the same rows (and the same probe-excluded / status != 1
    counts) as the A2 entry it replaces.  A revert-set point without complete A2FC outputs is REFUSED (SystemExit)
    unless dev (then recorded under 'missing' and the A2 entry is kept, the output being DEV anyway).
    Modifies acc_a2 in place; -> provenance dict."""
    import json
    prov = dict(rule='plan.md l.1254-1255 / l.1813 (V4-6 > 5 % -> the A2 point reverts to the full chain)',
                revert_set_file=str(REVERT_SET.relative_to(C.TT)),
                revert_set_sha256=C.sha256(REVERT_SET) if REVERT_SET.exists() else None,
                n_revert=len(revert), points={}, missing=[])
    for spin, m, lam in revert:
        ka = f'A2|{spin}|{m:g}|{lam:g}|BM'; kf = f'A2FC|{spin}|{m:g}|{lam:g}|BM'
        a = acc_a2.get(ka); f = acc_fc.get(kf)
        if a is None:
            prov['missing'].append(f'{ka}: no A2 entry to replace'); continue
        if f is None:
            prov['missing'].append(f'{ka}: no A2FC output ({kf})'); continue
        same = (sorted(a['rows']) == sorted(f['rows']) and a['probe_excluded'] == f['probe_excluded']
                and a['status_ne1'] == f['status_ne1'])
        if not same:
            prov['missing'].append(f'{ka}: A2FC rows differ from A2 (A2 {len(a["rows"])} rows, A2FC {len(f["rows"])}; '
                                   f'probe-excl {a["probe_excluded"]}/{f["probe_excluded"]}, status!=1 '
                                   f'{a["status_ne1"]}/{f["status_ne1"]}) -- incomplete A2FC'); continue

        def eps(x, i):
            return float(x['L'][:, i].mean()) if len(x['rows']) else None
        new = dict(f, sample='A2', replaced_by_a2fc=True)
        prov['points'][ka] = dict(replaced_by=kf, n_den=len(f['rows']), jobs=(fc_jobs or {}).get(kf, []),
                                  eps_R04_a2_numpy=eps(a, 3), eps_R04_a2fc=eps(f, 3),
                                  eps_R14_a2_numpy=eps(a, 13), eps_R14_a2fc=eps(f, 13))
        acc_a2[ka] = new
    if prov['missing']:
        msg = 'REFUSED (V4-6 revert, FIX R6): revert-set point(s) without complete A2FC full-chain outputs: ' + \
              json.dumps(prov['missing'][:5])
        if not dev:
            raise SystemExit(msg)
        log('DEV: ' + msg + ' -- A2 kept for those points')
    log(f"V4-6 revert: {len(prov['points'])}/{len(revert)} A2 points replaced by A2FC (full chain)")
    return prov
