"""srt_tmin_check.py -- PU-only check of the AMENDED SR-T window proposed in acts/stage4/review/FIX_SRT_TMIN_R1/R2.md.

NOT a frozen-rule computation: it evaluates a proposed (unapplied) amendment on the G3B1 sample (rho = 1, PU-only,
77 admitted jobs).  No signal input of any kind.  Read-only on data/acts_stage4/prod/G3; writes only
data/acts_stage4/g3/srt_tmin_check*.json and srt_dt_hist_kp1*.npy.

--version v1  (FIX R1): t_PV = 0 for the PU-only trial PV; k = +1 overlay from partner event e+1 only.
              Reproduces data/acts_stage4/g3/srt_tmin_check.json (written to srt_tmin_check_v1_rerun.json).
--version v2  (FIX R2, review A-1): per-EVENT PV time t_PV = sigma_PV * z, z ~ N(0, 1) from
              numpy default_rng([trial_seed of the event's road-0 trial, 0x5254]) (the 4 roads share one PV, so they
              share t_PV); sigma_PV = 190 ps (plan l.288, luminous region; geometry json sigma_t_ps).  dt = t_BTL - t_PV
              - |u|/c for every hit (k = 0, +1).  k = +1 overlay: partners e+1, e+2, e+3 (mod n_ev, same job) as three
              independent realisations (review C-4); P_oot is their mean.  Also reported: k <= -1 delayed hits
              (B-1), raw-t vs min-dt 'earliest' (B-3 iii), even/odd-job split of edges vs measurement (C-2), event
              clustering (C-3).  Options --sigma-pv-ps (sensitivity 150/230) and --extra-smear-ps (sigma_t 60 ps
              variation: sqrt(60^2 - 35^2) = 48.7 ps added to every stored BTL t, seeded per job; C-6).

Definitions (FIX_SRT_TMIN_R2 §5, the PC-19 block):
  R_k(a, b) = N_k(dt in [a, b]) / N_k: per-hit rate of the in-band BTL hits of the B1 loose candidates (S3 & R01)
              from crossing k, normalised per hit of that crossing.
  t_max = min(dt_acc, largest t <= dt_bx with R_+1(dt_bx/2, t) < 1e-4);  t_min = smallest t >= 0 with R_0(t, t_max) < 1e-4.

    cd theory_track && nice -n 15 pixi run python -m acts.stage4.g3.srt_tmin_check --version v2
"""
import argparse
import json
import os
import time

import numpy as np
from numba import njit

from acts.stage4.g3.analyse_g3 import HLO, HBW, HN, EXCLUDED, PROD, OUT, NR, S4
from acts.stage4.finder import weights as WG

DT_ACC = 25.0          # ns, frozen (WP_RULE §1.4)
DT_BX = 25.0           # ns, bunch spacing
RATE = 1e-4            # frozen per-hit threshold
GRID = 0.005           # ns, as analyse_g3
SALT_TPV = 0x5254      # seed salt of the PU-only trial PV time
SALT_SMEAR = 0x534D    # seed salt of the sigma_t-variation extra smearing
KEYS = ['tag', 'trial', 'rungs', 'normal', 'axis', 'btl_n_band', 'btl_dt0']
_inb = WG._btl_inband
_C = WG.C_MM_PER_NS


@njit(cache=False)
def band_kernel(NRM, AXS, sel, hsel, UB, CXB, CYB, S0B, S1B, TB, ttol, wc, lo, binw, hist, nh, dt_raw, dt_min, dt_max):
    """Per candidate sel[s]: in-band count, dt of the hit with the smallest RAW time (TB is t - t_PV + k*25, a per-trial
    constant shift, so the raw order is unchanged), min dt, max dt.  Per-hit dt histogram only where hsel[s]."""
    nb = UB.shape[0]
    nbin = hist.shape[0]
    for s in range(sel.shape[0]):
        c = sel[s]
        nx = NRM[c, 0]; ny = NRM[c, 1]; nz = NRM[c, 2]
        ax = AXS[c, 0]; ay = AXS[c, 1]; az = AXS[c, 2]
        n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
        tb = np.inf
        for b in range(nb):
            if not _inb(nx, ny, nz, ax, ay, az, n2x, n2y, n2z, UB[b, 0], UB[b, 1], UB[b, 2], CXB[b], CYB[b],
                        S0B[b], S1B[b], ttol, wc):
                continue
            dt = TB[b] - np.sqrt(UB[b, 0] ** 2 + UB[b, 1] ** 2 + UB[b, 2] ** 2) / _C
            nh[s] += 1
            if TB[b] < tb:
                tb = TB[b]; dt_raw[s] = dt
            if not (dt >= dt_min[s]):
                dt_min[s] = dt
            if not (dt <= dt_max[s]):
                dt_max[s] = dt
            if hsel[s]:
                i = int(np.floor((dt - lo) / binw))
                if i < 0:
                    i = 0
                elif i >= nbin:
                    i = nbin - 1
                hist[i] += 1


def centres():
    return HLO + HBW * (np.arange(HN) + 0.5)


def rate_window(hist, a, b):
    """R(a, b) = hits with a <= dt(bin centre) <= b over all hits of the histogram."""
    c = centres()
    cs = np.concatenate([[0], np.cumsum(hist)])
    i0 = np.searchsorted(c, a, 'left'); i1 = np.searchsorted(c, b, 'right')
    return (cs[i1] - cs[i0]) / max(hist.sum(), 1)


def edges(h0, h1):
    """t_max from the k = +1 per-hit spectrum h1, then t_min from the in-time spectrum h0 (5 ps grid)."""
    g_up = np.arange(DT_BX / 2, DT_BX + 1e-9, GRID)
    r1 = np.array([rate_window(h1, DT_BX / 2, t) for t in g_up])
    ok = np.where(r1 < RATE)[0]
    t_max = min(DT_ACC, float(g_up[ok[-1]])) if len(ok) else None
    g_lo = np.arange(0.0, t_max + 1e-9, GRID)
    r0 = np.array([rate_window(h0, t, t_max) for t in g_lo])
    ok0 = np.where(r0 < RATE)[0]
    t_min = float(g_lo[ok0[0]]) if len(ok0) else None
    # k <= -1 (copy method; previous crossings are independent PU events): crossing -j lands in the window if its
    # in-time dt is in [t_min + 25 j, t_max + 25 j]; the windows are disjoint, so the sum is <= R_0(dt >= t_min + 25)
    r_m = sum(rate_window(h0, t_min + DT_BX * j, t_max + DT_BX * j) for j in range(1, 13))
    return dict(t_min_ns=round(t_min, 4), t_max_ns=round(t_max, 4),
                R0_window=float(rate_window(h0, t_min, t_max)), R1_window=float(rate_window(h1, t_min, t_max)),
                Rm_window_k_le_m1=float(r_m), Rm_window_k_le_m1_upper95=float(3.0 / max(h0.sum(), 1)) if r_m == 0 else None,
                R0_tail_probe={f'{t:g}': float(rate_window(h0, t, t_max)) for t in (2, 5, 6, 6.12, 6.5)},
                R1_edge_probe={f'{t:g}': float(rate_window(h1, DT_BX / 2, t)) for t in (23.8, 23.9, 24.0, 24.1, 24.2,
                                                                                         24.3, 24.4, 25.0)},
                in_time_dt_range_ns=[float(centres()[np.nonzero(h0)[0][0]]), float(centres()[np.nonzero(h0)[0][-1]])])


def tpv_of_event(trial_seed_road0, sigma_ns):
    return sigma_ns * np.random.default_rng([int(trial_seed_road0), SALT_TPV]).standard_normal()


LADDER_POPS = ['loose_S3_R01', 'R04_S2']      # SR-T ladder order of the populations this G3 check stores


def combine():
    """PC-19 sigma_ln terms, mechanically: L = SR-T late composite at the FIXED nominal window; at population r it
    qualifies if its late count C >= 10 in every run of the variation set; sigma = max |ln(L_var / L_nom)|; a rung
    that does not qualify takes the value of the deepest qualifying population before it; none qualifies -> 1.0."""
    J = {t: json.loads((OUT / f'srt_tmin_check_{t}.json').read_text()) for t in ('v2', 'v2_spv150', 'v2_spv230', 'v2_st60')}
    w = J['v2']['fixed_window']
    assert all(J[t]['fixed_window'] == w for t in J), 'all runs must use the nominal fixed window'
    out = dict(window=w, rule='PC-19 (FIX_SRT_TMIN_R3)')
    for name, var in (('sigma_ln_PV', ('v2_spv150', 'v2_spv230')), ('sigma_ln_sigma_t', ('v2_st60',))):
        res = {}; last = None
        for pn in LADDER_POPS:
            fw = {t: J[t]['populations'][pn]['fixed_window'] for t in ('v2',) + var}
            ok = all(fw[t]['late_count_C'] >= 10 for t in fw)
            if ok:
                last = max(abs(np.log(fw[t]['L_composite'] / fw['v2']['L_composite'])) for t in var)
            res[pn] = dict(qualifies=ok, counts={t: fw[t]['late_count_C'] for t in fw},
                           L={t: fw[t]['L_composite'] for t in fw},
                           sigma_ln=float(last) if last is not None else 1.0,
                           source=('own' if ok else ('deepest qualifying' if last is not None else 'none -> 1.0')))
        out[name] = res
    (OUT / 'srt_sigma_ln_pv.json').write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', choices=['v1', 'v2'], default='v2')
    ap.add_argument('--combine', action='store_true', help='only compute sigma_ln,PV and sigma_ln,sigma_t (PC-19 '
                    'rule) from srt_tmin_check_{v2,v2_spv150,v2_spv230,v2_st60}.json')
    ap.add_argument('--sigma-pv-ps', type=float, default=190.0, help='v2: PV time spread (plan l.288: 190 ps)')
    ap.add_argument('--extra-smear-ps', type=float, default=0.0, help='v2: extra Gaussian smearing of every BTL t')
    ap.add_argument('--tag', default='', help='suffix of the output JSON')
    ap.add_argument('--fixed-window', nargs=2, type=float, default=None,
                    help='also report the fractions in this fixed [t_min, t_max] (systematic of a mis-set sigma_PV/sigma_t)')
    a = ap.parse_args(argv)
    if a.combine:
        return combine()
    try:
        os.nice(15)
    except OSError:
        pass
    v2 = a.version == 'v2'
    smear_on = v2 and a.extra_smear_ps > 0
    sig_pv = a.sigma_pv_ps * 1e-3 if v2 else 0.0
    partners = [1, 2, 3] if v2 else [1]
    # k <= -1 by MIXING (R3, review R2 C-3): crossing -j uses partner e+j, j = 1..12 (partners 1..3 reuse their +25 ns
    # pass: dt_max(unshifted) = dt_max - 25); only dt_max is needed (proxy: an in-band hit with dt >= t_min + 25 j)
    kle_extra = list(range(4, 13)) if v2 else []
    t0 = time.time()
    man = json.loads((S4 / 'jobs' / 'G3.json').read_text())['jobs']
    jobs = [j for j in man if j['sample'] == 'G3B1' and j['id'] not in EXCLUDED]
    # per-hit histograms per job parity (C-2): h0[par], h1[par] (k = +1 from partner e+1 only, as the edge rule)
    h0 = np.zeros((2, HN), np.int64); h1 = np.zeros((2, HN), np.int64)
    pops = {'loose_S3_R01': (2, 0), 'R04_S2': (1, 3)}
    acc = {p: {} for p in pops}
    chk = dict(n_jobs=0, n_sel=0, n_mismatch_nband=0, max_abs_ddt0_ns_vs_stored_minus_tpv=0.0)
    for jn, j in enumerate(jobs):
        par = int(j['chunk']) % 2
        with np.load(PROD / 'G3B1' / (j['id'] + '.npz'), allow_pickle=False) as z:
            meta = json.loads(str(z['meta_json']))
            c = {k: z['cand.' + k] for k in KEYS}
            ev = z['trials.ev']; pv = z['trials.pv']; road = z['trials.road']; tsd = z['trials.trial_seed']
            B = z['btl'].astype(np.float64)
            n_tr = int(z['n_trials'])
        ttol = float(meta['finder_cfg']['t_tol']); wc = float(meta['finder_cfg']['w_c'])
        ev0 = int(meta['job']['ev0']); n_ev = int(meta['job']['n_events'])
        if v2 and a.extra_smear_ps > 0:
            B[:, 8] += a.extra_smear_ps * 1e-3 * np.random.default_rng([int(meta['job']['seed']), SALT_SMEAR]) \
                .standard_normal(len(B))
        # per-event PV time from the trial seed of the event's lowest road present (road 0 in every G3 event)
        tpv_ev = np.zeros(n_ev)
        if v2:
            for ie_ in np.unique(ev - ev0):
                ts = np.where(ev - ev0 == ie_)[0]
                tpv_ev[int(ie_)] = tpv_of_event(tsd[ts[np.argmin(road[ts])]], sig_pv)
        flags = np.unpackbits(c['rungs'], axis=1)[:, :NR].astype(bool)
        loose = ((c['tag'] & 2) > 0) & flags[:, 0]
        r04 = ((c['tag'] & 1) > 0) & flags[:, 3]
        sel = np.where(loose | r04)[0]
        sel = sel[np.argsort(c['trial'][sel], kind='stable')]
        ti = c['trial'][sel]
        starts = np.searchsorted(ti, np.arange(n_tr + 1))
        nrm = np.ascontiguousarray(c['normal'], np.float64); axs = np.ascontiguousarray(c['axis'], np.float64)
        bev = B[:, 0].astype(np.int64)
        ns = len(sel)
        out = {k: dict(nh=np.zeros(ns, np.int64), raw=np.full(ns, np.nan), mn=np.full(ns, np.inf),
                       mx=np.full(ns, -np.inf)) for k in [0] + partners + kle_extra}
        hsel_all = loose[sel]
        for t in range(n_tr):
            a_, b_ = starts[t], starts[t + 1]
            if a_ == b_:
                continue
            ie = int(ev[t]) - ev0
            for p in [0] + partners + kle_extra:
                bb = B[bev == ((ie + p) % n_ev)]
                UB = np.ascontiguousarray(bb[:, 2:5] - pv[t][None, :])
                r = np.hypot(bb[:, 2], bb[:, 3])
                # partners 1..3: k = +1 realisations (+25 ns); partners 4..12 (k <= -1 only): unshifted in-time dt
                TB = np.ascontiguousarray(bb[:, 8] + (DT_BX if p in partners else 0.0) - tpv_ev[ie])
                hist = h0[par] if p == 0 else (h1[par] if p == 1 else np.zeros(1, np.int64))
                hs = hsel_all[a_:b_] if p in (0, 1) else np.zeros(b_ - a_, np.bool_)
                o = out[p]
                band_kernel(nrm, axs, sel[a_:b_].astype(np.int64), hs, UB, np.ascontiguousarray(bb[:, 2] / r),
                            np.ascontiguousarray(bb[:, 3] / r), np.ascontiguousarray(bb[:, 5]),
                            np.ascontiguousarray(bb[:, 6]), TB, ttol, wc, HLO, HBW, hist,
                            o['nh'][a_:b_], o['raw'][a_:b_], o['mn'][a_:b_], o['mx'][a_:b_])
        # in-time kernel vs stored production fields: btl_n_band, and btl_dt0 - t_PV (raw order is t_PV-invariant)
        sn = c['btl_n_band'][sel].astype(np.int64)
        tpv_c = tpv_ev[ev[c['trial'][sel]] - ev0]
        sd = c['btl_dt0'][sel].astype(np.float64) - tpv_c
        both = np.isfinite(sd) & np.isfinite(out[0]['raw'])
        chk['n_jobs'] += 1; chk['n_sel'] += int(ns)
        chk['n_mismatch_nband'] += int(np.sum(np.minimum(out[0]['nh'], 32767) != sn))
        if both.any():
            chk['max_abs_ddt0_ns_vs_stored_minus_tpv'] = max(chk['max_abs_ddt0_ns_vs_stored_minus_tpv'],
                                                             float(np.max(np.abs(out[0]['raw'][both] - sd[both]))))
        evkey = jn * 1000 + ev[c['trial'][sel]].astype(np.int64)
        for pn, (bit, col) in pops.items():
            m = ((c['tag'][sel] & bit) > 0) & flags[sel, col]
            d = acc[pn]
            d.setdefault('par', []).append(np.full(int(m.sum()), par))
            d.setdefault('evkey', []).append(evkey[m])
            d.setdefault('n0', []).append(sn[m])
            # in-time earliest-hit dt: STORED btl_dt0 - t_PV at nominal; with --extra-smear-ps the stored field is
            # unsmeared, so the value recomputed from the smeared S5 hits is used (review R3 C-1)
            d.setdefault('raw0', []).append(out[0]['raw'][m] if smear_on else sd[m])
            for f in ('raw', 'mn', 'mx'):
                d.setdefault(f + '0r', []).append(out[0][f][m])        # recomputed from S5
            for p in partners + kle_extra:
                sh_ = DT_BX if p in partners else 0.0
                d.setdefault(f'mxu{p}', []).append(out[p]['mx'][m] - sh_)      # unshifted max dt of partner p
            for p in partners:
                d.setdefault(f'n{p}', []).append(out[p]['nh'][m])
                d.setdefault(f'raw{p}', []).append(out[p]['raw'][m])
                d.setdefault(f'mn{p}', []).append(out[p]['mn'][m])
        if jn % 10 == 0:
            print(j['id'], ns, '%.0f s' % (time.time() - t0), flush=True)
    tag = a.tag or (a.version if a.version == 'v2' else 'v1_rerun')
    H0 = h0.sum(0); H1 = h1.sum(0)
    np.save(OUT / f'srt_dt_hist_k0_{tag}.npy', H0); np.save(OUT / f'srt_dt_hist_kp1_{tag}.npy', H1)
    E = edges(H0, H1)
    sh = int(round(DT_BX / HBW))
    h1c = np.zeros(HN, np.int64); h1c[sh:] = H0[:-sh]
    E_par = [edges(h0[q], h1[q]) for q in (0, 1)]
    res = dict(created=time.strftime('%Y-%m-%d %H:%M:%S'), version=a.version, sigma_pv_ps=a.sigma_pv_ps if v2 else 0.0,
               extra_smear_ps=a.extra_smear_ps if v2 else 0.0, partners=partners, fixed_window=a.fixed_window, kernel_check=chk,
               n_hits_k0=int(H0.sum()), n_hits_kp1=int(H1.sum()), amended_edges_mixing=E,
               amended_edges_copy=edges(H0, h1c), edges_even_jobs=E_par[0], edges_odd_jobs=E_par[1], populations={})
    tmin, tmax = E['t_min_ns'], E['t_max_ns']
    win = lambda x, lo, hi: np.isfinite(x) & (x >= lo) & (x <= hi)      # noqa: E731
    for pn, d in acc.items():
        d = {k: np.concatenate(v) for k, v in d.items()}
        N = len(d['n0']); pres = d['n0'] > 0; npres = int((~pres).sum())

        def fractions(lo_, hi_, earliest, mask=None):
            mk = np.ones(N, bool) if mask is None else mask
            e0 = d['raw0'] if earliest == 'raw' else d['mn0r']
            li = pres & win(e0, lo_, hi_) & mk
            lo_p = [(~pres) & (d[f'n{p}'] > 0) & win(d[('raw' if earliest == 'raw' else 'mn') + str(p)], lo_, hi_) & mk
                    for p in partners]
            n_np = max(int(((~pres) & mk).sum()), 1)
            p_oot = float(np.mean([x.sum() for x in lo_p]) / n_np)
            n_mk = max(int(mk.sum()), 1)
            # k <= -1 (mixing, v2): crossing -j from partner e+j; counted on the candidates WITHOUT an in-time hit
            # (the same M as P_oot); summed over j (conservative vs the union)
            lo_m = [(~pres) & mk & np.isfinite(d[f'mxu{j}']) & (d[f'mxu{j}'] >= lo_ + DT_BX * j)
                    for j in range(1, 13)] if v2 else []
            n_km_ = int(sum(x.sum() for x in lo_m))
            p_km = n_km_ / n_np
            n_count = int(li.sum() + sum(x.sum() for x in lo_p) + n_km_)
            return dict(n_late_kle_m1_mixing=n_km_ if v2 else None, P_kle_m1_late_given_not_present=p_km if v2 else None,
                        P_kle_m1_upper95=(3.0 / n_np if (v2 and n_km_ == 0) else None),
                        P_oot_total_given_not_present=p_oot + p_km, M_not_present=n_np,
                        late_count_C=n_count,
                        L_composite=float(li.sum() / n_mk + (p_oot + p_km) * ((~pres) & mk).sum() / n_mk),n_late_in_time=int(li.sum()), n_events_late_in_time=int(len(np.unique(d['evkey'][li]))),
                        P_late_given_present=float(li.sum() / max(int((pres & mk).sum()), 1)),
                        n_late_oot_per_partner=[int(x.sum()) for x in lo_p],
                        n_events_late_oot_per_partner=[int(len(np.unique(d['evkey'][x]))) for x in lo_p],
                        P_oot_late_given_not_present=p_oot,
                        P_srt_per_candidate=float(li.sum() / n_mk + p_oot * ((~pres) & mk).sum() / n_mk))
        # k <= -1 delayed hits (B-1): a crossing -j hit is in the window iff the candidate has an in-band hit of that
        # (independent) crossing with in-time dt in [t_min + 25 j, t_max + 25 j]; proxy: in-time max dt >= t_min + 25
        n_km = int(np.sum(np.isfinite(d['mx0r']) & (d['mx0r'] >= tmin + DT_BX)))
        P = dict(n_cand=N, n_present=int(pres.sum()), frac_present=float(pres.mean()),
                 frac_kp1_present=float(np.mean([(d[f'n{p}'] > 0).mean() for p in partners])),
                 earliest_raw_t=fractions(tmin, tmax, 'raw'),
                 earliest_min_dt=fractions(tmin, tmax, 'mn'),
                 n_raw_vs_mindt_disagree_in_time=int(np.sum(pres & (win(d['raw0'], tmin, tmax)
                                                                     != win(d['mn0r'], tmin, tmax)))),
                 k_le_m1_copy_crosscheck=dict(n_cand_with_in_time_dt_ge_tmin_plus_25=n_km,
                              upper95_single_count=float(3.0 / N) if n_km == 0 else None,
                              note='copy method (cross-check only; the rule uses the mixing count in fractions()): '
                                   'sum over j of candidates with a copy hit in window j is ONE count, so its 95% bound '
                                   'is 3/N (review R2 C-3); Fatras slow-particle tail only'),
                 frozen_edge_25ns=fractions(tmin, DT_ACC, 'raw'),
                 window_R1_proposal_6p12_24p275=fractions(6.12, 24.275, 'raw'))
        if a.fixed_window:
            P['fixed_window'] = dict(window=list(a.fixed_window), **fractions(a.fixed_window[0], a.fixed_window[1], 'raw'))
        # C-2: edges from one parity, fractions measured on the other
        P['split_edges_other_parity'] = {
            f'measure_{"even" if q == 0 else "odd"}': dict(
                edges=[E_par[1 - q]['t_min_ns'], E_par[1 - q]['t_max_ns']],
                **fractions(E_par[1 - q]['t_min_ns'], E_par[1 - q]['t_max_ns'], 'raw', mask=(d['par'] == q)))
            for q in (0, 1)}
        res['populations'][pn] = P
    res['seconds'] = time.time() - t0
    (OUT / f'srt_tmin_check_{tag}.json').write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
