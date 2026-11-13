"""srt.py -- SR-T background factors per WP_RULE_PC19.md (takes precedence over WP_RULE for every SR-T quantity).

Reference implementation: acts/stage4/g3/srt_tmin_check.py (sha 9d0c902a..., HASH_ADDENDUM §6); its numba kernel,
edge rule and PV-time draw are imported unchanged.  Generalised here from the two G3 populations (loose, R04) to every
SR-T rung population:  S3 & r for r < R04, S2 & r for r >= R04 (PC-19 'Population for SR-T ladder rung r').

Per B1 job (n_ev >= 13 required for the mixing), per candidate of (S3 & R01) | S2, with t_PV = 0 in the kernel (the raw
time order and max dt are t_PV-invariant; t_PV is subtracted per event afterwards, so the sigma_PV variations are free):
  in time:   n_band, dt of the earliest-by-raw-time hit (stored btl_dt0 used at nominal), (per-hit histogram, loose)
  k = +1:    partners e+1, e+2, e+3 at +25 ns: n_band, earliest raw dt  (realisation j = 1 also fills the edge histogram)
  k <= -1:   partners e+j, j = 1..12: max dt (unshifted) -> crossing -j in window iff max dt >= t_min + 25 j
'Earliest' = the smallest raw t among in-band hits with dt > -dt_bx/2 (PC-19); the in-time hits always satisfy it.
sigma_t = 60 ps variation: +48.7 ps Gaussian smearing of the stored S5 t, seeded [job seed, 0x534D], kernel re-run.
"""
import numpy as np

from acts.stage4.analysis import common as C
from acts.stage4.g3 import srt_tmin_check as RT       # frozen reference (A.3 via HASH_ADDENDUM §6)

HLO, HBW, HN = RT.HLO, RT.HBW, RT.HN
SIG_PV_NOM = 0.190
SIG_PV_VAR = (0.150, 0.230)
EXTRA_SMEAR_NS = 0.0487
PARTNERS_KP1 = (1, 2, 3)
KM = tuple(range(1, 13))


def job_arrays(d, smear=False):
    """Kernel pass over one B1 job (d = background.to_g3_job layout with 'btl').  Returns per-candidate arrays for the
    selected records and the per-hit histograms (loose candidates, k = 0 and k = +1 partner 1), all at t_PV = 0."""
    if 'btl' not in d or 'normal' not in d['cand']:          # streaming: load the per-job SR-T inputs from disk
        with np.load(d['path'], allow_pickle=False) as z:
            c = {k: z['cand.' + k] for k in ('tag', 'rungs', 'trial', 'normal', 'axis', 'btl_n_band', 'btl_dt0', 'nip2',
                                             'dw_core', 'p_chi2core')}
            Bz = z['btl']
        d = dict(d, cand=c, btl=Bz)
    c = d['cand']; tr = d['tr']; meta = d['meta']
    ttol = float(meta['finder_cfg']['t_tol']); wc = float(meta['finder_cfg']['w_c'])
    ev0 = int(meta['job']['ev0']); n_ev = int(meta['job']['n_events'])
    if n_ev < 13:
        raise RuntimeError(f"{d['job_id']}: n_ev = {n_ev} < 13 (PC-19 mixing needs >= 13 events per job)")
    B = d['btl'].astype(np.float64)
    if smear:
        B = B.copy()
        B[:, 8] += EXTRA_SMEAR_NS * np.random.default_rng([int(meta['job']['seed']), RT.SALT_SMEAR]).standard_normal(len(B))
    F = C.rung_flags(c['rungs'])
    loose = ((c['tag'] & 2) > 0) & F[:, 0]
    s2 = (c['tag'] & 1) > 0
    sel = np.where(loose | s2)[0]
    sel = sel[np.argsort(c['trial'][sel], kind='stable')]
    ti = c['trial'][sel]
    n_tr = len(tr['ev'])
    starts = np.searchsorted(ti, np.arange(n_tr + 1))
    nrm = np.ascontiguousarray(c['normal'], np.float64); axs = np.ascontiguousarray(c['axis'], np.float64)
    bev = B[:, 0].astype(np.int64)
    ns = len(sel)
    parts = sorted(set((0,) + PARTNERS_KP1 + KM))
    out = {p: dict(nh=np.zeros(ns, np.int64), raw=np.full(ns, np.nan), mn=np.full(ns, np.inf), mx=np.full(ns, -np.inf))
           for p in parts}
    h0 = np.zeros(HN, np.int64); h1 = np.zeros(HN, np.int64)
    hsel = loose[sel]
    # t_PV per event (PC-19: z from the road-0 trial seed, or the lowest road present)
    z_ev = np.zeros(n_ev)
    for ie_ in np.unique(tr['ev'] - ev0):
        ts = np.where(tr['ev'] - ev0 == ie_)[0]
        z_ev[int(ie_)] = np.random.default_rng([int(tr['trial_seed'][ts[np.argmin(tr['road'][ts])]]),
                                                RT.SALT_TPV]).standard_normal()
    tpv_nom = SIG_PV_NOM * z_ev                     # histograms at the nominal PV time (PC-19 edge rule)
    for t in range(n_tr):
        a_, b_ = starts[t], starts[t + 1]
        if a_ == b_:
            continue
        ie = int(tr['ev'][t]) - ev0
        for p in parts:
            bb = B[bev == ((ie + p) % n_ev)]
            UB = np.ascontiguousarray(bb[:, 2:5] - tr['pv'][t][None, :])
            r = np.hypot(bb[:, 2], bb[:, 3])
            shift = C.DT_BX if p in PARTNERS_KP1 else 0.0
            TB = np.ascontiguousarray(bb[:, 8] + shift - tpv_nom[ie])
            hist = h0 if p == 0 else (h1 if p == 1 else np.zeros(1, np.int64))
            hs = hsel[a_:b_] if p in (0, 1) else np.zeros(b_ - a_, np.bool_)
            o = out[p]
            RT.band_kernel(nrm, axs, sel[a_:b_].astype(np.int64), hs, UB, np.ascontiguousarray(bb[:, 2] / r),
                           np.ascontiguousarray(bb[:, 3] / r), np.ascontiguousarray(bb[:, 5]),
                           np.ascontiguousarray(bb[:, 6]), TB, ttol, wc, HLO, HBW, hist,
                           o['nh'][a_:b_], o['raw'][a_:b_], o['mn'][a_:b_], o['mx'][a_:b_])
    back = tpv_nom[tr['ev'][ti] - ev0]             # stored per-candidate times: t_PV = 0 (fractions subtract it)
    for p in parts:
        out[p]['raw'] = out[p]['raw'] + back
        out[p]['mx'] = out[p]['mx'] + back
    f32 = np.float32
    rec = dict(F=np.packbits(F[sel], axis=1), loose=loose[sel], s2=s2[sel], z=z_ev[tr['ev'][ti] - ev0].astype(f32),
               ev=(tr['ev'][ti].astype(np.int64) + 100_000 * int(meta['job'].get('chunk', 0))),
               n0=np.minimum(out[0]['nh'], 32767).astype(np.int16),
               nip2=c['nip2'][sel].astype(np.int8), w=c['dw_core'][sel].astype(f32), pchi=c['p_chi2core'][sel].astype(f32),
               nroad=tr['n_road'][ti].astype(np.int32),
               raw0=(c['btl_dt0'][sel].astype(f32) if not smear else out[0]['raw'].astype(f32)))
    for p in PARTNERS_KP1:
        rec[f'n{p}'] = np.minimum(out[p]['nh'], 32767).astype(np.int16); rec[f'raw{p}'] = out[p]['raw'].astype(f32)
    for j in KM:
        sh = C.DT_BX if j in PARTNERS_KP1 else 0.0
        rec[f'mxu{j}'] = (out[j]['mx'] - sh).astype(f32)
    chk = dict(n_sel=ns, n_mismatch_nband=int(np.sum(np.minimum(out[0]['nh'], 32767) != c['btl_n_band'][sel])),
               max_abs_ddt0=float(np.nanmax(np.abs(out[0]['raw'] - c['btl_dt0'][sel]))) if ns else 0.0)
    return rec, h0, h1, chk


def merge(recs):
    return {k: np.concatenate([r[k] for r in recs]) for k in recs[0]}


def edges(h0, h1):
    """PC-19 window edges on a 5 ps grid (srt_tmin_check.edges, unchanged)."""
    return RT.edges(h0, h1)


def fractions(R, mask, tmin, tmax, sig_pv):
    """P(late) and P_OOT on the population mask at window [tmin, tmax] with t_PV = sig_pv * z (ns)."""
    tpv = sig_pv * R['z'].astype(np.float64)
    win = lambda x: np.isfinite(x) & (x >= tmin) & (x <= tmax)                       # noqa: E731
    pres = R['n0'] > 0
    raw0 = R['raw0'] - tpv
    li = mask & pres & win(raw0)
    oot = [mask & ~pres & (R[f'n{p}'] > 0) & win(R[f'raw{p}'] - tpv) for p in PARTNERS_KP1]
    km = [mask & ~pres & np.isfinite(R[f'mxu{j}']) & ((R[f'mxu{j}'] - tpv) >= tmin + C.DT_BX * j) for j in KM]
    M_p = int((mask & pres).sum()); M_np = int((mask & ~pres).sum()); M = int(mask.sum())
    n_kp1 = float(np.mean([x.sum() for x in oot])); n_km = int(sum(x.sum() for x in km))
    P_late = li.sum() / M_p if M_p else None
    P_oot = (n_kp1 + n_km) / M_np if M_np else None
    L = ((li.sum() / M if M else 0.0) + (P_oot or 0.0) * M_np / max(M, 1))
    return dict(M=M, M_present=M_p, M_not_present=M_np, n_late_in_time=int(li.sum()), n_kp1_mean=n_kp1,
                n_kp1_per_partner=[int(x.sum()) for x in oot], n_km=n_km, P_late=P_late, P_oot=P_oot,
                late_count_C=int(li.sum() + sum(x.sum() for x in oot) + n_km), L=L,
                n_events_late_in_time=int(len(np.unique(R['ev'][li]))))


def population(R, col):
    """PC-19 population for in-job column col: S3 & r for r < R04 (cols 0-2), S2 & r otherwise."""
    fc = ((R['F'][:, col // 8] >> (7 - col % 8)) & 1).astype(bool)          # packed rung flags
    if col < 3:
        return R['loose'] & fc
    return R['s2'] & fc


def srt_factors(R_nom, R_smear, h0, h1):
    """Edges (nominal), and per in-job column: measuring population (tightest with M >= 10 along the column's ladder
    ancestors, WP_RULE §4.2), P(late), P_OOT and the PC-19 sigma_ln,PV / sigma_ln,sigma_t with the mechanical fallback."""
    E = edges(h0, h1)
    tmin, tmax = E['t_min_ns'], E['t_max_ns']
    out = dict(edges=E, columns={})
    last = dict(PV=None, st=None)
    ladder_vals = []
    anc = C.supersets
    NOM = [fractions(R_nom, population(R_nom, col), tmin, tmax, SIG_PV_NOM) for col in range(C.NR)]
    for col in range(C.NR):
        nom = NOM[col]
        # measuring populations for the two factors (tightest ancestor with M >= 10)
        mp = next((c for c in anc(col) if NOM[c]['M_present'] >= 10), None)
        mn = next((c for c in anc(col) if NOM[c]['M_not_present'] >= 10), None)
        fp = NOM[mp] if mp is not None else None
        fn = NOM[mn] if mn is not None else None
        # timing sigma_ln terms (own population, qualification C >= 10 in nominal and every variation)
        var_pv = [fractions(R_nom, population(R_nom, col), tmin, tmax, s) for s in SIG_PV_VAR]
        var_st = [fractions(R_smear, population(R_smear, col), tmin, tmax, SIG_PV_NOM)] if R_smear is not None else []
        q_pv = nom['late_count_C'] >= 10 and all(v['late_count_C'] >= 10 for v in var_pv)
        q_st = bool(var_st) and nom['late_count_C'] >= 10 and all(v['late_count_C'] >= 10 for v in var_st)
        own_pv = max(abs(np.log(v['L'] / nom['L'])) for v in var_pv) if (q_pv and nom['L'] > 0) else None
        own_st = max(abs(np.log(v['L'] / nom['L'])) for v in var_st) if (q_st and nom['L'] > 0) else None
        if col <= 13:                      # ladder: deepest qualifying rung before it (PC-19 mechanical fallback)
            if own_pv is not None:
                last['PV'] = own_pv
            if own_st is not None:
                last['st'] = own_st
            val_pv, val_st = last['PV'], last['st']
            ladder_vals.append((val_pv, val_st))
        else:                              # non-ladder columns: own value, else (conservative reading) the largest
            lv = [v for v in ladder_vals[3:] if v[0] is not None]       # carried ladder value R04..R14
            val_pv = own_pv if own_pv is not None else (max(v[0] for v in lv) if lv else None)
            lv = [v for v in ladder_vals[3:] if v[1] is not None]
            val_st = own_st if own_st is not None else (max(v[1] for v in lv) if lv else None)
        out['columns'][C.RUNGS[col]] = dict(
            own=nom, late_population=C.RUNGS[mp] if mp is not None else None,
            P_late=dict(N=fp['n_late_in_time'], M=fp['M_present']) if fp else None,
            oot_population=C.RUNGS[mn] if mn is not None else None,
            P_oot=dict(N=fn['n_kp1_mean'] + fn['n_km'], M=fn['M_not_present'], n_km=fn['n_km'],
                       n_km_upper95=(3.0 / fn['M_not_present']) if fn['n_km'] == 0 else None) if fn else None,
            qualifies_PV=q_pv, qualifies_sigma_t=q_st,
            sigma_ln_PV=float(val_pv) if val_pv is not None else 1.0,
            sigma_ln_sigma_t=float(val_st) if val_st is not None else 1.0)
    # F1 rungs and fallback selections inherit their parent in-job column's timing terms (PC-19 fallback)
    return out


# ================================================================================================ signal SR-T (PC-19)
def oot_events(spin, m, row, n_b1):
    """PC-19 'Assigning OOT events': crossing k of signal row (spin, m, row) uses C1 B1 event index
    i_k = blake2b(f"srt-oot|{spin}|{m}|{row}|{k}", 8 bytes, big) mod N_B1, crossings in the order -12..-1, +1..+3;
    a collision with an earlier crossing of the SAME row increments mod N_B1 until unused."""
    import hashlib
    used = set(); out = {}
    for k in list(range(-12, 0)) + [1, 2, 3]:
        i = int.from_bytes(hashlib.blake2b(f"srt-oot|{spin}|{m}|{row}|{k}".encode(), digest_size=8).digest(),
                           'big') % n_b1
        while i in used:
            i = (i + 1) % n_b1
        used.add(i); out[k] = i
    return out


def c1_b1_event_index(manifest_jobs, prod=None, sample='B1'):
    """REVIEW R1 A-4: C1 B1 events ordered by (job id, ev) FROM THE MANIFEST (N_B1 does not depend on which outputs
    exist).  -> list of (job id, path or None, ev0, job-relative event index)."""
    prod = prod or C.PROD
    out = []
    for j in sorted((j for j in manifest_jobs if j['kind'] == 'pu' and j['sample'] == sample), key=lambda j: j['id']):
        p = prod.joinpath(*j['out'].split('/'))
        for e in range(int(j['n_events'])):
            out.append((j['id'], p if p.is_file() else None, int(j['ev0']), e))
    return out


def signal_srt(obs, ev_index, tmin, tmax, m_fmt=lambda m: f'{m:g}', log=print):
    """SR-T tag per matched signal candidate (PC-19 'Signal eps_SR-T'): the earliest in-band BTL hit (smallest raw t
    among in-band hits with dt > -12.5 ns), over the in-time hits of the signal event (stored: t_raw_in) and the OOT
    crossings from the assigned C1 B1 events (hits shifted by 25 k ns, taken about the candidate's plane, axis, PV and
    t_PV), must be in-time (an OOT PU earliest hit earns no credit) and have dt in [t_min, t_max].
    ev_index = c1_b1_event_index(...): the B1 S5 column 0 is the JOB-RELATIVE event index (A-4).
    -> (list of dicts (srt, earliest, k), check dict)."""
    from acts.stage4.analysis.signal import btl_inband
    NB = len(ev_index)
    need = {}
    for q, o in enumerate(obs):
        for k, i in oot_events(o['spin'], m_fmt(o['m']), o['row'], NB).items():
            jid, p, ev0, e = ev_index[i]
            need.setdefault(p, []).append((q, k, e))
    chk = dict(N_B1=NB, n_lookups=0, n_lookups_missing_file=0, n_lookups_with_btl_hits=0, n_oot_inband_hits=0)
    best = [dict(t=o['t_raw_in'], src='in-time', k=0) for o in obs]
    missing_row = np.zeros(len(obs), bool)        # REVIEW R2 C-1: a row with a missing-file crossing gets no SR-T credit
    for p, lst in need.items():
        chk['n_lookups'] += len(lst)
        if p is None:
            chk['n_lookups_missing_file'] += len(lst)
            for q, k, e in lst:
                missing_row[q] = True
            continue
        with np.load(p, allow_pickle=False) as z:
            B = z['btl'].astype(np.float64)
        bev = B[:, 0].astype(np.int64)
        for q, k, e in lst:
            o = obs[q]
            bb = B[bev == e][:, 1:9].copy()
            if not len(bb):
                continue
            chk['n_lookups_with_btl_hits'] += 1
            bb[:, 7] += C.DT_BX * k
            m, u = btl_inband(bb, np.asarray(o['pv']), np.asarray(o['normal']), np.asarray(o['axis']))
            if not m.any():
                continue
            chk['n_oot_inband_hits'] += int(m.sum())
            dt = bb[:, 7] - o['t_pv'] - np.linalg.norm(u, axis=1) / 299.792458
            ok = m & (dt > -0.5 * C.DT_BX)
            if ok.any():
                tr = float(bb[ok, 7].min())
                if tr < best[q]['t']:
                    best[q] = dict(t=tr, src='OOT PU', k=k)
    out = []
    for q, o in enumerate(obs):
        b = best[q]
        dt_in = o['dt_earliest']
        tag = (b['src'] == 'in-time') and np.isfinite(dt_in) and (tmin <= dt_in <= tmax) and not missing_row[q]
        out.append(dict(srt=bool(tag), earliest=b['src'], k=b['k']))
    chk['n_earliest_oot'] = sum(1 for x in out if x['earliest'] == 'OOT PU')
    chk['frac_rows_missing_file'] = float(missing_row.mean()) if len(obs) else 0.0
    chk['pass_'] = bool(chk['n_lookups'] == 0 or (chk['n_lookups_with_btl_hits'] > 0 and chk['n_oot_inband_hits'] > 0))
    return out, chk


def time_independence(R, tmin, tmax, rng):
    """REVIEW R1 B-4 (WP_RULE §6.2 SR-T row, §6.4 'part of the same gate'): late fraction of the BTL-present candidates
    (earliest in-time in-band hit in [t_min, t_max], nominal t_PV) in bins of N_IP2 and terciles of w_core,
    p(chi2_core) and road-hit count, on the loose (S3 & R01) and R04 (S2) populations; analyse_g3.indep_test (Rao-Scott,
    pass p > 0.05).  On failure the correlation factor c_time = max over bins of (bin fraction / pooled fraction)
    multiplies P(late) (the §6.4 c rule applied to the time factor)."""
    from acts.stage4.g3 import analyse_g3 as G3
    out = {}
    c_time = 1.0
    for name, col in (('loose_S3_R01', 0), ('R04_S2', 3)):
        m = population(R, col) & (R['n0'] > 0)
        dt = R['raw0'][m].astype(np.float64) - SIG_PV_NOM * R['z'][m].astype(np.float64)
        late = np.isfinite(dt) & (dt >= tmin) & (dt <= tmax)
        ev = R['ev'][m]
        nip = np.clip(R['nip2'][m].astype(int), 4, 7) - 4
        res = dict(n=int(m.sum()), n_late=int(late.sum()),
                   by_nip2=G3.indep_test(late, nip, rng, ev), by_wcore=G3.indep_test(late, G3.tercile_bins(R['w'][m]), rng, ev),
                   by_chi2core_p=G3.indep_test(late, G3.tercile_bins(R['pchi'][m]), rng, ev),
                   by_density=G3.indep_test(late, G3.tercile_bins(R['nroad'][m]), rng, ev))
        ps = [v.get('p_value') for k, v in res.items() if k.startswith('by_') and v.get('p_value') is not None]
        res['all_pass'] = all(p > 0.05 for p in ps) if ps else None
        if res['all_pass'] is False:
            for k, v in res.items():
                if k.startswith('by_') and v.get('p_value') is not None and v['p_value'] <= 0.05 and v.get('p_pool'):
                    c_time = max(c_time, max(f / v['p_pool'] for f in v['frac']))
        out[name] = res
    out['c_time'] = c_time
    return out
