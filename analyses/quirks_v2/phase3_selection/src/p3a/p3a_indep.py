"""p3a_indep.py -- independent re-derivation of the subset-pass counts at the widths and s that Nils's review did not
cover (R04 with the 75 mm width, R05, R06, R07; s = 0 and s = 3; R08 optional as a reproduction of his numbers).
Aurora, 2026-11-24.  Addresses the condition "R04-R07 and s = 3 read, not re-derived" (LOG 2026-11-23 19:44).

  <tt python> -B p3a_indep.py --part I --nparts N --out /ABS/OUT.json [--stride 2 --offset 0] [--max-files K]

The search (search_event) and the pure-numpy verifier (verify) are those of phase2_exploration/src/review_nils_subset.py,
IMPORTED UNCHANGED (sha256 recorded); they do not import p2w_subset and were not written by the classifier's author
or by me.  W is an argument of both.  Added here: the loop over widths, and N_2S2 of each verified witness (2S layer:
>= 2 hits on each of its two sensors, the rule of p2w_subset._eval l.177-185) so that k(s = 3) = k_IP + max(0, 3 - N_2S2)
of that witness can be formed.  Nils's search keeps the witness of the smallest k_IP only and looks at planes with
N_IP2 >= 4 only: its s = 3 value is a valid witness (a lower bound on the count), and rows whose s = 3 pass needs
k_IP in {4, 5} are outside its reach (reported as such downstream).
Events and widths: for every Z(nunu) pilot event with a row in the Phase-2 outputs p2-c-r1v-s[23][ab] (w > 0), each
width at which that row is COUNTED in reading S (k <= 3 at s = 0 or k <= 5 at s = 3): R04 -> W = 1e9 ('none') and 75 mm,
R05..R08 -> 37.5, 18.75, 9.4, 4.7 mm.  (R08, s = 0 repeats Nils's own run; R08, s = 3 was not covered by it.)
The question answered is "is each counted event confirmed by an independent search"; events only his search would
find are not looked for here (his review did that at R08).
Pool, PV draw: as p2t_classify.py / p2w_subset.py (merged pool, blake2b seed string).  No signal file is read.
"""
import argparse
import glob
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[2]
sys.path.insert(0, str(QV2 / 'phase2_exploration' / 'src'))
import review_nils_subset as NR  # noqa: E402

log = logging.getLogger('p3a_indep')


def n2s2_of(LC, SD, mask):
    n = 0
    for l in (7, 8, 9):
        if min(int((mask & (LC == l) & (SD == 1)).sum()), int((mask & (LC == l) & (SD == 2)).sum())) >= 2:
            n += 1
    return n


def classify(Hm, pv, phim, FF, widths):
    """-> {W: [[k_IP, N_2S2] or None for S, F, H]} (verified witnesses only), n_bad."""
    U, CX, CY, S0, S1, LC, SD = NR.road_arrays(Hm, pv, phim, FF)
    out = {}; nbad = 0
    if len(U) < 8:
        return out, nbad
    cr = np.zeros((7, 3), np.int64)
    np.add.at(cr, (LC[LC <= 6], SD[LC <= 6]), 1)
    if sum((cr[l, 0] if l < 4 else min(cr[l, 1], cr[l, 2])) >= 2 for l in range(7)) < 4:
        return out, nbad
    c = NR.CFG
    for W in widths:
        bk, wm, wn, st = NR.search_event(U, CX, CY, S0, S1, LC, SD, float(phim), float(W), c['w_c'], c['t_tol'], c['iters'],
                                         c['delta95'], c['eta_max'])
        res = [None, None, None]
        for cat in range(3):
            if bk[cat] < 99:
                v = NR.verify(U, CX, CY, S0, S1, LC, SD, wm[cat], wn[cat], phim, W=float(W))
                good = v['ok'] and v['k'] <= bk[cat] and (cat != 1 or v['nit2'] >= 3) and (cat != 2 or v['hard'])
                if good:
                    res[cat] = [int(v['k']), n2s2_of(LC, SD, wm[cat])]
                elif bk[cat] <= 3:              # a witness that would have counted was rejected by the verifier
                    nbad += 1
        out[str(W)] = res
    return out, nbad


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s p3a_indep %(message)s', stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', type=int, default=0)
    ap.add_argument('--nparts', type=int, default=1)
    ap.add_argument('--max-files', type=int, default=0)
    ap.add_argument('--stride', type=int, default=1, help='every stride-th Z file (sorted paths), offset --offset')
    ap.add_argument('--offset', type=int, default=0)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    WMAP = [(0, 1e9), (0, 75.0), (1, 37.5), (2, 18.75), (3, 9.4), (4, 4.7)]      # (Phase-2 width index, W)
    t_c0 = time.process_time(); t_w0 = time.perf_counter()
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    sys.path.insert(0, str(QV2)); os.chdir(QV2)
    from acts.stage4.finder import chain_inputs as CI
    from acts.stage4.finder import finder as FF
    theirs = {}
    for f in sorted(glob.glob(f'{NR.V}/p2-c-r1v-s[23][ab]/000/r1v-s2-znn-*.npz')):
        z = np.load(f); m = json.loads(str(z['meta'])); r = z['rows']
        if any(abs(m['config'][k] - NR.CFG[k]) > 1e-12 for k in NR.CFG):
            raise SystemExit(f'{f}: config differs from CFG')
        for fi, fm in enumerate(m['files']):
            assert fm['stream'] == 'pilot.hs0.znn' and fm['path'] not in theirs
            k0 = m['row_cols'].index('k_R04_s0_S')
            theirs[fm['path']] = {int(x[1]): x[k0:k0 + 20].astype(np.int64).reshape(5, 2, 2) for x in r[r[:, 0] == fi]}
        z.close()
    paths = sorted(theirs)
    if len(paths) != 460:
        raise SystemExit(f'{len(paths)} Z files, expected 460')
    out = dict(part=a.part, nparts=a.nparts, stride=a.stride, offset=a.offset, wmap=WMAP, files=[], events=[], n_bad=0, cfg=NR.CFG,
               nils_sha256=hashlib.sha256(Path(NR.__file__).read_bytes()).hexdigest())
    sub = [(gi, p) for gi, p in enumerate(paths) if gi % a.stride == a.offset]
    todo = [x for j, x in enumerate(sub) if j % a.nparts == a.part]
    if a.max_files:
        todo = todo[:a.max_files]
    for gi, path in todo:
        z = np.load(path); meta = json.loads(str(z['meta'])); ec = meta['evt_cols']
        hits = z['hits']; off = z['hit_off'].astype(np.int64); evt = z['evt']; tru = z['tru']
        w = evt[:, ec.index('w_v1')]; ph = evt[:, ec.index('phimet_reco_v1')]
        vtx = evt[:, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]]
        for i in sorted(theirs[path]):
            assert w[i] > 0
            kk = theirs[path][i]
            widths = [W for wi, W in WMAP if kk[wi, 0, 0] <= 3 or kk[wi, 1, 0] <= 5]
            if not widths:
                continue
            hsh = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
            pv = vtx[i] + np.random.default_rng(int.from_bytes(hsh, 'little')).normal(0.0, 1.0, 3) * NR.PV_SIGMA
            s = slice(int(off[i]), int(off[i + 1]))
            hh = hits[s].astype(np.float64); tt = tru[s].astype(np.float64)
            b = FF.LC_OF[hh[:, 0].astype(np.int64)] >= 0
            if b.sum() < 8:
                continue
            Hm = CI.merge_pool(hh[b], tt[b])[0]
            phim = float((ph[i] + np.pi) % (2 * np.pi) - np.pi)
            r, nb = classify(Hm, pv, phim, FF, widths)
            out['n_bad'] += nb
            out['events'].append([path, i, float(w[i]), r, kk.reshape(-1).tolist()])
        out['files'].append(dict(gi=gi, path=path, n_rows=len(theirs[path])))
        z.close()
        log.info('%d %s rows=%d cpu=%.0f', gi, Path(path).name, len(theirs[path]), time.process_time() - t_c0)
    out['cpu_s'] = time.process_time() - t_c0; out['wall_s'] = time.perf_counter() - t_w0
    out['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    p = Path(a.out); part = p.with_name(p.name + '.part')
    with open(part, 'w') as f:
        f.write(json.dumps(out)); f.flush(); os.fsync(f.fileno())
    part.replace(p)
    log.info('done cpu %.0f s, %d events, %d bad', out['cpu_s'], len(out['events']), out['n_bad'])


if __name__ == '__main__':
    main()
