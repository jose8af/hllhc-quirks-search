"""p2t_classify.py -- PROVISIONAL own-hit classification of pilot files with the frozen v1 finder (Tove, 2026-11-19).

  <tt python> p2t_classify.py --id ID --out /ABS/OUT.npz (--files a.npz,b.npz | --manifest m.json) [--max-events N] [--check-prefilter] [--no-ckf-pass]

Plan: outputs/RULE1_PRELIM_PLAN_tove_2026-11-19.md section 3.  Read-only on pilot files (members meta, hits, hit_off,
tru, evt, n_early_prod).  Per event and road orientation the pool is every row on the barrel counting surfaces, merged
with v1's chain_inputs.merge_pool, no top-up; variant 0 keeps the CKF-flagged rows (Df-9: all own hits, before CKF),
variant 1 drops them (v1's pool; information only; run only for events
that have a variant-0 candidate unless --ckf-pass-all).  The frozen finder (finder.find, configuration of
frozen_inputs.json, store='loose') runs unchanged; every candidate with |dphi(n3, MET)| < delta95 and |eta(n3)| < eta_max
is stored (CAND_COLS).  Rung logic is applied later (p2t_rule1_prelim.py) from the stored N_IT2, N_IP2, N_2S2, w_core.

Orientations: Z(nunu) one (stored phimet_reco_v1; only events with w_v1 > 0 are classified: the others are in no term);
B1 class streams and lowpt 21 (phi_road + 2 pi k / 21); hs one (phi_road, the event's own road).
Exact shortcut: an orientation goes to the finder only if its road hits (finder.road_select) hold >= 4 IP layers with
>= 2 hits each, which every loose candidate (N_IP2 >= 4) needs.  --check-prefilter runs the finder on every orientation
with >= 3 road hits and counts stored candidates in orientations the shortcut would have skipped (must be 0).
No signal file is read; no efficiency is formed.
"""
import argparse
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
log = logging.getLogger('p2t_classify')

CAND_COLS = ['file', 'event', 'orient', 'variant', 'nit2', 'nip2', 'n2s2', 'nl2', 'dw_core', 'p_chi2core', 'n_core', 'nhit',
             'dphi_met', 'eta_axis', 'n_ckf_flag', 'n_product', 'n_fatras_gen', 'n_particles', 'cls', 'n_early_prod', 'w']
EV_COLS = ['file', 'event', 'cls', 'n_early_prod', 'w', 'n_bar_hits', 'n_orient_run_v0', 'n_orient_run_v1', 'n_cand_v0',
           'n_cand_v1']


def ip_double_layers(lc):
    c = np.bincount(lc[lc < 7], minlength=7)
    return int((c >= 2).sum())


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s p2t_classify %(message)s', stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--files', default='')
    ap.add_argument('--max-events', type=int, default=0)
    ap.add_argument('--check-prefilter', action='store_true')
    ap.add_argument('--no-ckf-pass', action='store_true')
    ap.add_argument('--ckf-pass-all', action='store_true')
    ap.add_argument('--manifest', default='', help='JSON {job id: [paths]}; replaces --files')
    a = ap.parse_args()
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    sys.path.insert(0, str(QV2))
    os.chdir(QV2)
    from acts.stage4 import run_stage4 as RS
    from acts.stage4.finder import chain_inputs as CI
    from acts.stage4.finder import finder as FF
    from acts.stage4.finder import production as PR
    fz = RS.frozen_inputs()
    if fz is None or fz.get('wp_rule_sha256') != RS.sha256_file(RS.HERE / 'WP_RULE.md'):
        raise SystemExit('frozen_inputs / WP_RULE.md mismatch')
    cfg, wcfg = PR.config_from_frozen(fz)
    PV_SIGMA = np.array([0.010, 0.010, 0.015])          # mm; v1 g1b_tt.PV_SIGMA (plan §1.7), checked below
    from acts.stage4.finder import g1b_tt as GT
    if not np.allclose(GT.PV_SIGMA, PV_SIGMA):
        raise SystemExit('PV_SIGMA differs from v1 g1b_tt.PV_SIGMA')
    variants = (0,) if a.no_ckf_pass else (0, 1)
    cands = []; evrows = []; files = []; errors = []
    n_skipped_with_cand = 0; n_checked = 0
    t_find = 0.0; n_find = 0
    paths = json.loads(Path(a.manifest).read_text())[a.id] if a.manifest else a.files.split(',')
    for fi, path in enumerate(paths):
        z = np.load(path)
        meta = json.loads(str(z['meta']))
        stream = meta['stream']; ec = meta['evt_cols']
        hits = z['hits']; off = z['hit_off']; tru = z['tru']; evt = z['evt']
        nev = int(meta['n_events'])
        if len(off) != nev + 1 or len(evt) != nev:
            raise SystemExit(f'{path}: offsets/evt do not match n_events')
        is_z = stream == 'pilot.hs0.znn'
        if is_z:
            w = evt[:, ec.index('w_v1')]; cls = np.full(nev, -1); nep = np.zeros(nev, np.int64)
            axis0 = evt[:, ec.index('phimet_reco_v1')]; norient = 1
            vtx = evt[:, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]]
            pvs = np.empty((nev, 3))
            for i in range(nev):
                h = hashlib.blake2b(f'p2t-pv|{stream}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
                pvs[i] = vtx[i] + np.random.default_rng(int.from_bytes(h, 'little')).normal(0.0, 1.0, 3) * PV_SIGMA
        else:
            w = np.ones(nev); cls = evt[:, ec.index('cls')].astype(np.int64); nep = z['n_early_prod'].astype(np.int64)
            axis0 = evt[:, ec.index('phi_road')]
            norient = 1 if stream == 'pilot.c0.hs' else int(meta['road_orientations']['n'])
            pvs = evt[:, [ec.index('pv_x'), ec.index('pv_y'), ec.index('pv_z')]].astype(np.float64)
        sid_all = hits[:, 0].astype(np.int64)
        bar_all = FF.LC_OF[sid_all] >= 0
        nmax = nev if not a.max_events else min(nev, a.max_events)
        files.append(dict(path=path, stream=stream, chunk=meta['chunk'], n_events=nev, n_classified_range=nmax,
                          content_sha256=meta.get('content_sha256'), n_orient=norient,
                          n_per_class=meta.get('n_per_class'), sum_w_v1=meta.get('sum_w_v1'),
                          n_w_positive=int((w[:nmax] > 0).sum()), n_early_events=int((nep[:nmax] > 0).sum()),
                          w_values=np.unique(np.round(w[:nmax], 6), return_counts=True)[0][:50].tolist()))
        for i in range(nmax):
            if is_z and not w[i] > 0:
                continue
            s = slice(int(off[i]), int(off[i + 1]))
            b = bar_all[s]
            nb = int(b.sum())
            row = [fi, i, cls[i], nep[i], w[i], nb, 0, 0, 0, 0]
            if nb >= 8 and ip_double_layers(FF.LC_OF[sid_all[s][b]]) >= 4 or (a.check_prefilter and nb >= 3):
                H0 = hits[s][b].astype(np.float64); T0 = tru[s][b].astype(np.float64)
                ck = (H0[:, 6].astype(np.int64) & 1) == 1
                for v in variants:
                    if v == 1 and not row[8] and not a.ckf_pass_all:
                        continue          # after-CKF pass (information only) only for events with a variant-0 candidate
                    Hp = H0 if v == 0 else H0[~ck]; Tp = T0 if v == 0 else T0[~ck]
                    if len(Hp) < 3:
                        continue
                    Hm = CI.merge_pool(Hp, Tp)[0]
                    sidm = Hm[:, 0].astype(np.int64); lcm = FF.LC_OF[sidm]
                    for k in range(norient):
                        phim = float((axis0[i] + 2 * np.pi * k / norient + np.pi) % (2 * np.pi) - np.pi)
                        m, _ = FF.road_select(Hm, sidm, pvs[i], phim, cfg)
                        nr = int(m.sum())
                        ok = nr >= 8 and ip_double_layers(lcm[m]) >= 4
                        if not ok and not (a.check_prefilter and nr >= 3):
                            continue
                        try:
                            t0 = time.perf_counter()
                            r = FF.find(Hm, sidm, pvs[i], phim, cfg=cfg, store='loose', want_csr=True)
                            t_find += time.perf_counter() - t0; n_find += 1
                        except Exception as x:          # reported in the output, never silently dropped
                            errors.append(dict(file=fi, event=i, orient=k, variant=v, n_road=nr, error=repr(x)[:300]))
                            continue
                        row[6 + v] += 1
                        V = r['vars']; nc = len(V['nit2'])
                        if not nc:
                            continue
                        ax = r['axis']
                        eta = np.arcsinh(ax[:, 2] / np.maximum(np.hypot(ax[:, 0], ax[:, 1]), 1e-12))
                        al = (r['dphi_met'] < wcfg.delta95) & (np.abs(eta) < wcfg.eta_max)
                        if not al.any():
                            continue
                        if not ok:
                            n_skipped_with_cand += int(al.sum())
                        n_checked += 1
                        _, pchi = PR.full_set_flags(V, np.full(nc, np.nan))
                        road_idx = np.where(r['road_mask'])[0]
                        ho = r['csr_off']; hh = r['csr_hits']
                        for c in np.where(al)[0]:
                            hc = Hm[road_idx[hh[ho[c]:ho[c + 1]]]]
                            cands.append([fi, i, k, v, V['nit2'][c], V['nip2'][c], V['n2s2'][c], V['nl2'][c], V['dw_core'][c],
                                          pchi[c], V['n_core'][c], V['nhit'][c], r['dphi_met'][c], eta[c],
                                          int(((hc[:, 6].astype(np.int64) & 1) == 1).sum()), int((hc[:, 10] >= 1).sum()),
                                          int((hc[:, 9] >= 1).sum()), len(np.unique(hc[:, [7, 8, 10]], axis=0)), cls[i],
                                          nep[i], w[i]])
                            row[8 + v] += 1
            if row[8] or row[9] or nep[i] > 0:
                evrows.append(row)
        if is_z:        # per-event weights of the classified range (M = sum w / w_max is formed downstream)
            files[-1]['w_sum'] = float(w[:nmax].sum()); files[-1]['w_max'] = float(w[:nmax].max())
            files[-1]['w_hist'] = {str(k): int(c) for k, c in zip(*np.unique(np.round(w[:nmax], 4), return_counts=True))}
        else:
            files[-1]['cls_counts'] = {str(k): int(c) for k, c in zip(*np.unique(cls[:nmax], return_counts=True))}
            files[-1]['cls_counts_flagged'] = {str(k): int(c) for k, c in zip(*np.unique(cls[:nmax][nep[:nmax] > 0],
                                                                                         return_counts=True))}
        z.close()
        log.info('%s: %d events, %d candidates so far, %d finder calls, %.1f s', Path(path).name, nmax, len(cands), n_find,
                 time.perf_counter() - t_w0)
    summ = dict(id=a.id, files=files, cand_cols=CAND_COLS, ev_cols=EV_COLS, n_errors=len(errors), errors=errors[:200],
                n_find=n_find, t_find_s=t_find, check_prefilter=bool(a.check_prefilter),
                n_candidates_in_skipped_orientations=n_skipped_with_cand, variants=list(variants),
                finder_config=dict(road=cfg.road, tseed=cfg.tseed, w_c=cfg.w_c, t_tol=cfg.t_tol, iters=cfg.iters,
                                   delta95=wcfg.delta95, eta_max=wcfg.eta_max),
                frozen_inputs_sha256=RS.sha256_file(RS.HERE / 'frozen_inputs.json'),
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                wall_s=time.perf_counter() - t_w0, cpu_s=time.process_time() - t_c0)
    out = Path(a.out)
    part = out.with_name(out.name + '.part')
    with open(part, 'wb') as f:
        np.savez_compressed(f, meta=json.dumps(summ), cand=np.array(cands, np.float64).reshape(-1, len(CAND_COLS)),
                            ev=np.array(evrows, np.float64).reshape(-1, len(EV_COLS)))
        f.flush(); os.fsync(f.fileno())
    part.replace(out)
    log.info('done: %d candidates, %d event rows, %d errors, cpu %.1f s', len(cands), len(evrows), len(errors), summ['cpu_s'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
