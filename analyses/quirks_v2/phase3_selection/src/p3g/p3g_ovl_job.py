"""p3g_ovl_job.py -- overlay job of work package p3-g (Tormod, 2026-11-24).  Runner job, tt environment.

  <tt python> p3g_ovl_job.py --id ID --mode npo|dif --src SRC.npz --first F --n N --stream S --chunk C [--trials T1,T2,T0]
  <tt python> p3g_ovl_job.py --id ID --mode zhl --chunk C --n 40 [--trials T1,T0]

Chain (no chain file changed):
  npo, dif  v1's run_chain.py 'cppu' mode: a PU-200 event (s4pu.MinBias, event seeds from the job seed) with the STORED
            SimHits of the no-pile-up event inserted (vp 3500).  dif: the stored Fatras SimHits of the pilot event
            (TOY_COLS, full four-momenta).  npo: the Z(nunu) pilot stores no SimHit momenta; the SimHits are built from
            the stored truth position and time of every written measurement, momentum = 1 GeV along PV -> hit (the
            smearing digitisation reads the position only; check C1 of the plan).  After the chain the inserted rows
            are replaced by the stored no-pile-up rows (g1b_tt.replace_toy_rows, v1's C'_PU procedure; CKF flag from
            the pile-up event), so the own measurements are those P3A classified.
  zhl       v1's 'sm' chain with the job dict of C1 job c1sm-<chunk> (stream c1.sm, same seeds): the regeneration of
            sample 5; own class = hard-scatter vp 3000; PV, MET and trial seed drawn in run_pu_job's order, so trial T1
            must reproduce the stored sample-5 candidates (check C2).
Pool: g1b_tt.assemble (top-up from the non-inserted rows; zhl: from all rows, = prepare_event), CKF removal, merging.
Trials (same trial seed, same PU pool and top-up in all variants):
  T1  nominal (frozen finder configuration; f_CKF stored)
  T2  own rows NOT CKF-removed (pile-up rows CKF-removed as usual), no f_CKF: P(pass) without the CKF factor
  T0  paired pile-up-only pass: own rows removed from the pre-merge pool, pool re-merged (STR l.822-823)
Per candidate passing R04 (float32): rung bits, N_IT2, N_IP2, N_2S2, w_core,
p(chi2_core), band hits, own band hits, f_CKF, crossings per layer (own / all), j per class (p3g_common).
Output $QV2_OUT_DIR/ID.npz.  No signal quantity.
"""
import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p3g_common as G  # noqa: E402

log = G.setup_logging('p3g_ovl_job')
G4_VP = 3600


def toy_rows_from_hits(H, T, pv):
    """SimHit rows (run_chain.TOY_COLS) for stored measurements: truth position, stored time, 1 GeV along PV -> hit."""
    d = T - pv[None, :]
    d /= np.maximum(np.linalg.norm(d, axis=1), 1e-9)[:, None]
    n = len(H)
    out = np.zeros((n, 18))
    out[:, 0] = H[:, 0]
    out[:, 1:4] = T
    out[:, 4] = H[:, 12]
    out[:, 5:8] = d; out[:, 8] = 1.0
    out[:, 9:12] = d; out[:, 12] = 1.0
    out[:, 13] = G.OWN_VP
    out[:, 14] = H[:, 10]
    out[:, 15] = H[:, 8]
    out[:, 16] = H[:, 9]
    out[:, 17] = 0
    return out


def replace_own(ev, tru, own_ev, own_tru):
    """g1b_tt.replace_toy_rows (v1's C'_PU procedure: inserted rows -> the stored no-pile-up rows, matched by SimHit
    truth position, CKF flag of the pile-up event) with one addition: the per-surface resolutions s0, s1 (columns 4, 5)
    are kept from the chain row, because the pilot files store float32 copies and the finder index requires one
    resolution value per surface (finder.build_index assertion)."""
    ev = ev.copy()
    t_idx = np.where(ev[:, 7].astype(np.int64) == G.OWN_VP)[0]
    if not len(t_idx) or not len(own_ev):
        return ev, 0, len(t_idx), len(own_ev)
    d = np.abs(np.asarray(tru, np.float64)[t_idx][:, None, :] - np.asarray(own_tru, np.float64)[None, :, :]).max(2)
    j = np.argmin(d, 1)
    ok = d[np.arange(len(t_idx)), j] < 1e-4
    jj = j[ok]
    if len(np.unique(jj)) != len(jj):
        raise RuntimeError('own-row matching is not one-to-one')
    rows = t_idx[ok]
    keep = ev[rows][:, [4, 5, 6]].copy()
    ev[rows] = own_ev[jj]
    ev[rows, 4:7] = keep
    return ev, int(ok.sum()), int((~ok).sum()), int(len(own_ev) - ok.sum())


def own_class_rows(H):
    """(vsec, particle, gen) of stored rows must be unique per SimHit barcode -> nothing to do; returns a copy with vp."""
    E = H.copy()
    E[:, 7] = G.OWN_VP
    return E


def cand_records(X, ev_i, trial_code, P_INT, own_code, F, ckf_info, g4=None):
    """Records of the candidates of one trial (see module doc)."""
    A = X['A']; hoff = X['hoff']; hits = X['hits']
    V = X['r']['vars']
    INTh = A['INTu'][A['INTl']]
    vpc = INTh % 1_000_000
    own = vpc == own_code
    nc = X['nc']
    recs = []
    if nc == 0:
        return recs
    sel = F[:, 3]                       # every candidate passing R04 (all tests are at R04-R07 and their crossings)
    for c in np.where(sel)[0]:
        h = hits[hoff[c]:hoff[c + 1]]
        lc = A['LC'][h]; sd = A['SD'][h]
        o = own[h]
        cro = G.layer_crossings(lc, sd, o)
        cra = G.layer_crossings(lc, sd, np.ones(len(h), bool))
        if g4 is not None:
            gm = g4['is_g4'][h]
            pu = ~o & ~gm
            crg = G.layer_crossings(lc, sd, gm)
            jg = G.j_split(crg)
            vid = g4['vtx_of'][h]
            nlv = 0; vset = set()
            for L in range(10):
                if crg[L] >= 2:            # distinct secondary vertices among the double-crossing layers of the class
                    vset |= set(int(v) for v in vid[(lc == L) & gm & (vid >= 0)])
            nlv = len(vset)
            nv = len(set(int(v) for v in vid[gm & (vid >= 0)]))
        else:
            pu = ~o
            jg = (0, 0); nlv = 0; nv = 0
        crp = G.layer_crossings(lc, sd, pu)
        jo = G.j_split(cro); jp = G.j_split(crp)
        recs.append([ev_i, trial_code, c, G.rbits(F[c]), V['nit2'][c], V['nip2'][c], V['n2s2'][c], V['dw_core'][c],
                     X['pchi'][c], len(h), int(o.sum()), ckf_info[0][c] if ckf_info is not None else -1,
                     ckf_info[1][c] if ckf_info is not None else np.nan, jo[0], jo[1], jp[0], jp[1], jg[0], jg[1], nlv, nv,
                     *cro, *cra])
    return recs


def run_trials(GT, CI, PR, P, own_mask_H0, own_code, pv, phimet, tseed, cfg, wcfg, which, ev_i, out_recs, ev_stats,
               g4maps=None, road=0):
    """P = g1b_tt.assemble output; own_mask_H0 (len H0) marks own rows; which: list of 'T1', 'T2', 'T0'."""
    H0 = P['H0']; T0 = P['T0']; ck = P['H0_ckf']
    nF = len(P['H0_keep'])
    t = P['Hp'][nF:]; tt = P['Tp'][nF:]; ti = P['Ip'][nF:]
    I0 = H0[:, 7].astype(np.int64)                  # tag 0: INT = vp for every chain row (g1b_tt.assemble)
    if not np.array_equal(I0[P['H0_keep']], P['Ip'][:nF]):
        raise RuntimeError('INT of the chain rows differs from g1b_tt.assemble')
    btl = (P['btl'], P['btl_INT'])
    for w in which:
        if w == 'T1':
            keep = ~ck
            ckf_rows = H0[ck]
        elif w == 'T2':
            keep = ~ck | own_mask_H0
            ckf_rows = H0[ck & ~own_mask_H0]
        else:
            keep = ~ck & ~own_mask_H0
            ckf_rows = H0[ck & ~own_mask_H0]
        Hp = np.concatenate([H0[keep], t]); Ip = np.concatenate([I0[keep], ti]); Tp = np.concatenate([T0[keep], tt])
        if w == 'T1' and not np.array_equal(Hp, P['Hp']):
            raise RuntimeError('T1 pool differs from g1b_tt.assemble')
        Hm, mapi, ng, nh, nenl = CI.merge_pool(Hp, Tp)
        Im = np.zeros(len(Hm), np.int64)
        Im[mapi] = Ip
        if ng:
            sz = np.bincount(mapi, minlength=len(Hm))
            for j in np.where(sz > 1)[0]:
                mem = np.where(mapi == j)[0]
                Im[j] = Ip[mem[np.argmax(Hp[mem, 11])]]
        if w == 'T1' and not (np.array_equal(Hm, P['H']) and np.array_equal(Im, P['INT'])):
            raise RuntimeError('T1 merged pool differs from g1b_tt.assemble')
        sid = Hm[:, 0].astype(np.int64)
        res, X = GT.trial(Hm, sid, Im, pv, phimet, tseed, cfg, wcfg, ckf=ckf_rows, btl=btl)
        nc = X['nc']
        ckf_info = None
        if w == 'T1' and nc:
            ckf_info = GT.cand_extra(X, np.arange(nc), pv, phimet, cfg, ckf_rows, None)[:2]
        g4 = None
        if g4maps is not None:
            ri = X['road_idx']
            isg = (Im[ri] % 1_000_000) == G4_VP
            g4 = dict(is_g4=isg, vtx_of=np.where(isg, Hm[ri, 10].astype(np.int64) // 16, -1))
        code = {'T1': 1, 'T2': 2, 'T0': 0}[w] + 10 * road
        out_recs.extend(cand_records(X, ev_i, code, Im, own_code, X['F'], ckf_info, g4=g4))
        ev_stats.append([ev_i, code, nc, int(X['F'][:, 3].sum()), int(X['F'][:, 4].sum()), int(X['F'][:, 5].sum()),
                         int(X['F'][:, 6].sum()), len(Hm), int((Im % 1_000_000 == own_code).sum())])
    return None


EVS_COLS = ['ev', 'trial', 'n_cand', 'n_R04', 'n_R05', 'n_R06', 'n_R07', 'n_pool', 'n_own_pool']
EV_COLS = ['ev', 'src_index', 'n_own_written', 'n_matched', 'n_pu_own_unmatched', 'n_src_unmatched', 'n_ckf_own',
           'n_own_H0', 'pv_x', 'pv_y', 'pv_z', 'phimet', 'tseed_lo', 'tseed_hi']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--mode', choices=['npo', 'dif', 'zhl', 'g4pu'], required=True)
    ap.add_argument('--roads', type=int, default=4, help='g4pu: road orientations (trials) per event')
    ap.add_argument('--src', default='')
    ap.add_argument('--first', type=int, default=0)
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--stream', default='')
    ap.add_argument('--chunk', type=int, required=True)
    ap.add_argument('--trials', default='T1,T2,T0')
    ap.add_argument('--mu', type=float, default=200.0, help='pile-up; 0 only for check C1')
    a = ap.parse_args()
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    outd = Path(os.environ.get('QV2_OUT_DIR', '.')).resolve()
    work = Path.cwd().resolve() / 'p3gwork'
    work.mkdir(parents=True, exist_ok=True)
    os.environ['QV2_S4_DATA'] = str(work)
    sys.path.insert(0, str(G.QV2))
    os.chdir(G.QV2)
    from acts.stage4 import run_stage4 as RS
    from acts.stage4 import run_g1b as RG
    from acts.stage4.finder import g1b_tt as GT
    from acts.stage4.finder import chain_inputs as CI
    from acts.stage4.finder import production as PR
    fz = RS.frozen_inputs()
    if fz is None or fz.get('wp_rule_sha256') != RS.sha256_file(RS.HERE / 'WP_RULE.md'):
        raise SystemExit('frozen_inputs / WP_RULE.md mismatch')
    which = a.trials.split(',')
    tmpc = work / f'{a.id}.chain.npz'
    srcinfo = {}
    if a.mode in ('npo', 'dif'):
        S = np.load(a.src)
        sm = json.loads(str(S['meta']))
        evcols = sm['ev_cols']
        E = S['ev']
        idx = list(range(a.first, min(a.first + a.n, len(E))))
        if not idx:                                  # a job beyond the end of its source part: empty output, no chain
            outd.mkdir(parents=True, exist_ok=True)
            fn = outd / f'{a.id}.npz'
            np.savez_compressed(fn.with_name(fn.name + '.tmp.npz'), meta=np.array(json.dumps(dict(
                id=a.id, mode=a.mode, n_events=0, src=a.src, first=a.first, cand_cols=G.CAND_COLS, evs_cols=EVS_COLS,
                ev_cols=EV_COLS))), cand=np.zeros((0, len(G.CAND_COLS)), np.float32),
                evs=np.zeros((0, len(EVS_COLS)), np.int64), ev=np.zeros((0, len(EV_COLS))))
            os.replace(fn.with_name(fn.name + '.tmp.npz'), fn)
            log.info('%s: no event at first = %d (source has %d)', a.id, a.first, len(E))
            return
        job_seed = G.qv2_seed(a.stream, a.chunk, mod=2 ** 31)
        cpf = work / f'{a.id}.cp.npz'; evf = work / f'{a.id}.ev.json'
        toys = {}; own_rows = {}; info = []
        for q, j in enumerate(idx):
            g = dict(zip(evcols, E[j]))
            pv = np.array([g['pv_x'], g['pv_y'], g['pv_z']])
            Hs = S[f'h{j}']; Ts = S[f't{j}']
            if a.mode == 'npo':
                toys[q] = toy_rows_from_hits(Hs, Ts, pv)
                own_rows[q] = (own_class_rows(Hs), Ts)
            else:
                toys[q] = S[f'toy{j}']
                m = Hs[:, 7].astype(np.int64) == G.OWN_VP
                own_rows[q] = (Hs[m], Ts[m])
            info.append(dict(pv=pv.tolist(), phimet=float(g['phimet']), src=int(j)))
        np.savez(cpf, meta=np.array(json.dumps(dict(topo=f'p3g{a.mode}', job_seed=job_seed, ev_info=info))),
                 **{f'toy{q}': toys[q] for q in toys})
        evf.write_text(json.dumps(list(range(len(idx)))))
        args = ['cppu', tmpc, len(idx), job_seed, '--cp-file', cpf, '--cp-events', evf, '--mu', a.mu]
        t_chain = RG.chain(dict(), tmpc, args)
        srcinfo = dict(src=a.src, src_meta={k: sm[k] for k in sm if k not in ('columns',)}, first=a.first, idx=idx)
        n_ev = len(idx)
    elif a.mode == 'g4pu':
        job_seed = G.qv2_seed(a.stream, a.chunk, mod=2 ** 31)
        cmd = ['pixi', 'run', '--manifest-path', str(RS.ACTS_MANIFEST), 'python', str(HERE / 'p3g_g4pu_chain.py'),
               str(tmpc), str(a.n), str(job_seed)]
        import subprocess
        t0 = time.time()
        p = subprocess.run(cmd, cwd=str(work), capture_output=True, text=True)
        if p.returncode != 0 or not tmpc.exists():
            raise RuntimeError(f'g4pu chain failed ({p.returncode}): {p.stderr[-3000:]}')
        t_chain = time.time() - t0
        n_ev = a.n
        srcinfo = dict(job_seed=job_seed)
    else:
        seed = RS.hash_seed(f'qv2|c1.sm|{a.chunk}')
        job = dict(id=f'c1sm-{a.chunk:04d}', campaign='C1', sample='c1.sm', kind='sm', chunk=a.chunk, ev0=a.chunk * 40,
                   n_events=a.n, roads=1, rho=1, seed=seed, dump_events=0, est_s=0.0, mem_gb=0.0, out='x.npz',
                   requires='pu-chain', qv2_stream='c1.sm', sm_sample='Znunu_j')
        t_chain, _ = RS.run_chain(job, tmpc, False)
        ev_streams = np.random.SeedSequence(seed).spawn(a.n)
        n_ev = a.n
        srcinfo = dict(regenerated_job=job)
    z = np.load(tmpc)
    cm = json.loads(str(z['meta']))
    cfg, wcfg = RS.finder_configs(fz, dict(campaign='C1'), False)
    recs = []; evs = []; evrows = []
    for q in range(n_ev):
        e0 = z[f'ev{q}']; tr = z[f'tru{q}']
        if a.mode == 'g4pu':
            from acts.stage4.finder import pu_inputs as PI
            rs = np.random.default_rng(G.qv2_seed(a.stream, f'{a.chunk}|ev|{q}', mod=2 ** 63))
            P = GT.assemble(e0, tr, 0, rs, inserted_vp=(G4_VP,), do_topup=True)
            own0 = np.zeros(len(P['H0']), bool)
            pv = PI.lum_pv(rs)
            phi0 = rs.uniform(-np.pi, np.pi)
            for road in range(a.roads):
                phimet = float((phi0 + road * 2 * np.pi / a.roads + np.pi) % (2 * np.pi) - np.pi)
                tseed = int(rs.integers(0, 2 ** 62))
                run_trials(GT, CI, PR, P, own0, G.OWN_VP, pv, phimet, tseed, cfg, wcfg, ['T1'], q, recs, evs,
                           g4maps=True, road=road)
            evrows.append([q, q, int((e0[:, 7].astype(np.int64) == G4_VP).sum()), 0, 0, 0, 0, 0, *pv, phi0, 0, 0])
            continue
        if a.mode in ('npo', 'dif'):
            oe, ot = own_rows[q]
            e, nmat, nun_pu, nun_c0 = replace_own(e0, tr, oe, ot)
            inf = info[q]
            pv = np.array(inf['pv']); phimet = inf['phimet']
            tseed = RS.hash_seed(f'qv2|{a.stream}|trial|{a.chunk}|{q}')
            rs = np.random.default_rng(tseed)
            P = GT.assemble(e, tr, 0, rs, inserted_vp=(G.OWN_VP,), do_topup=True)
            own0 = P['H0'][:, 7].astype(np.int64) == G.OWN_VP
            src_i = inf['src']
        else:
            rs = np.random.default_rng(ev_streams[q])
            P = GT.assemble(e0, tr, 0, rs, inserted_vp=(), do_topup=True)
            ii = cm['ev_info'][q]
            pv = np.array(ii['hs_vtx'][:3]) + rs.normal(0.0, 1.0, 3) * np.array([0.010, 0.010, 0.015])
            met = np.array(ii['hs_met']) + rs.normal(0.0, 25.0, 2)
            phimet = float((float(np.arctan2(met[1], met[0])) + np.pi) % (2 * np.pi) - np.pi)
            tseed = int(rs.integers(0, 2 ** 62))
            own0 = P['H0'][:, 7].astype(np.int64) == G.HS_VP
            nmat = nun_pu = nun_c0 = 0; src_i = a.chunk * 40 + q
            e = e0
        run_trials(GT, CI, PR, P, own0, G.OWN_VP if a.mode != 'zhl' else G.HS_VP, pv, phimet, tseed, cfg, wcfg, which, q,
                   recs, evs)
        own_all = e[:, 7].astype(np.int64) == (G.OWN_VP if a.mode != 'zhl' else G.HS_VP)
        evrows.append([q, src_i, int(own_all.sum()), nmat, nun_pu, nun_c0, int((P['H0_ckf'] & own0).sum()), int(own0.sum()),
                       *pv, phimet, tseed % 2 ** 31, tseed // 2 ** 31])
    z.close()
    C = np.array(recs, np.float32).reshape(-1, len(G.CAND_COLS))
    meta = dict(id=a.id, mode=a.mode, stream=a.stream, chunk=a.chunk, trials=which, mu=a.mu, n_events=n_ev,
                cand_cols=G.CAND_COLS, evs_cols=EVS_COLS, ev_cols=EV_COLS, store_rungs=G.STORE_RUNGS, nreq=G.NREQ,
                chain_meta={k: v for k, v in cm.items() if k not in ('ev_info', 'toy_info')}, t_chain_s=t_chain,
                v41_pass=cm.get('v41_pass'), src=srcinfo, finder_cfg=dict(road=cfg.road, w_c=cfg.w_c, t_tol=cfg.t_tol,
                                                                         tseed=cfg.tseed, iters=cfg.iters),
                frozen_inputs_sha256=G.sha256_file(RS.FROZEN), code_sha256=dict(RS.code_hashes(), **{
                    p.name: G.sha256_file(p) for p in (Path(__file__), HERE / 'p3g_common.py')}),
                wall_s=time.perf_counter() - t_w0, cpu_s_self=time.process_time() - t_c0)
    outd.mkdir(parents=True, exist_ok=True)
    fn = outd / f'{a.id}.npz'
    tmp = fn.with_name(fn.name + '.tmp.npz')
    np.savez_compressed(tmp, meta=np.array(json.dumps(meta, default=str)), cand=C,
                        evs=np.array(evs, np.int64).reshape(-1, len(EVS_COLS)), ev=np.array(evrows, np.float64))
    os.replace(tmp, fn)
    shutil.rmtree(work, ignore_errors=True)
    log.info('done %s: %d events, %d records, chain %.0f s, wall %.0f s', a.id, n_ev, len(C), t_chain, meta['wall_s'])


if __name__ == '__main__':
    main()
