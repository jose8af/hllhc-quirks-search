"""p2x_ht_chain.py -- half-turn study, step 1: events through the unchanged chain with the FULL input particle table.

  <acts python> p2x_ht_chain.py <znn|mb> <out.npz> <n_events> <stream> <chunk>

znn: no-pile-up Z(nunu)+jets events (s4pu.SMEvent, mu = 0; generator and seeds as p2c_hs0).
mb : one minimum-bias interaction per event (s4pu.MinBias.event with n_int = 1): the unit of a pile-up crossing.
Output: hits / hit_off (run_chain.COLS, written measurements on the barrel counting surfaces and BTL), tru, v41,
timing, and `pin` / `pin_off`: every row given to Fatras (s4pu.PCOLS) in input order (barcode particle = running
count per (vp, vsec)).  Validation data for outputs/HALF_TURN_*.md; not a pilot sample.
"""
import shutil
import sys
import tempfile
import time

import numpy as np

import signal  # noqa: F401
import subprocess  # noqa: F401

import p2c_common as C
import p2x_common as X

sys.path.insert(0, str(C.CODE))
import run_chain as rc  # noqa: E402
import s4pu  # noqa: E402

log = C.setup_logging('p2x_ht_chain')


def run(kind, out, n_events, stream, chunk):
    t0 = time.time()
    job_seed = C.qv2_seed(stream, chunk)
    scratch = tempfile.mkdtemp(prefix='p2x_ht_', dir='.')
    try:
        G = rc.geometry(scratch)
        rc.BTL_SIDS.update(s['sid'] for s in G['surfs'] if s['kind'] == 'BTL')
        bs = s4pu.load_beamspot(rc.TT)
        if kind == 'znn':
            src = s4pu.SMEvent(rc.CP5, bs, 'Znunu_j', mu=0.0, tt=rc.TT)
            ev_seeds = [s4pu.hseed('sm', 'Znunu_j', job_seed, i, mod=2 ** 62) for i in range(n_events)]
            gen = lambda i: src.event(ev_seeds[i])  # noqa: E731
        else:
            src = s4pu.MinBias(rc.CP5, bs, mu=1.0, tt=rc.TT)
            ev_seeds = [s4pu.hseed('p2x-ht-mb', job_seed, i, mod=2 ** 62) for i in range(n_events)]
            gen = lambda i: src.event(ev_seeds[i], n_int=1)  # noqa: E731
        store = {}; pin = {}
        rc.TIMES.clear()

        def provider(i):
            P, vz, info = gen(i)
            pin[i] = np.array(P, float).reshape(-1, 12)
            return P, vz, info
        s = rc.build_sequencer(G, n_events, job_seed, provider, store, with_ckf=True)
        s.run()
        v41 = np.zeros((n_events, len(rc.V41_COLS))); tim = np.zeros((n_events, len(rc.T_COLS)))
        st = {}
        for e, nm, t in rc.TIMES:
            st.setdefault(e, {})[nm] = t
        hits = []; tru = []; pins = []
        for i in range(n_events):
            r = store[i]; ev = r['ev']
            v41[i] = (r['nh'], r['nm'], r['nmap'], r['bij'], r['nunm'], len(ev), r['onsurf'], 0, 0, 0, r['ntr'], r['nckf'], r['n_in'])
            x = st.get(i, {})
            t2 = x.get('t2_digi', 0.0); t3 = x.get('t3_seed', t2); t4 = x.get('t4_ckf', t3)
            tim[i] = (r['t_gen'], r['t_source'], t2 - x.get('t1_source', t2), t3 - t2, t4 - t3, r['t_dump'])
            hits.append(ev); tru.append(r['tru']); pins.append(pin[i])
        H, hoff = C.concat(hits, len(rc.COLS), np.float32)
        T, _ = C.concat(tru, 3, np.float32)
        PIN, poff = C.concat(pins, 12, np.float64)
        v41_pass = bool(np.all(v41[:, 3] == 1) and np.all(v41[:, 4] == 0) and np.all(v41[:, 6] < 1.0)
                        and np.all(v41[:, 0] - v41[:, 1] <= np.maximum(2, 1e-5 * v41[:, 0])))
        meta = dict(mode='ht-chain', kind=kind, stream=stream, chunk=chunk, job_seed=job_seed, n_events=n_events,
                    columns=rc.COLS, pcols=s4pu.PCOLS, v41_cols=rc.V41_COLS, timing_cols=rc.T_COLS, v41_pass=v41_pass,
                    n_hits=int(len(H)), n_simhits_all_surfaces=int(v41[:, 0].sum()), n_particles_in=int(len(PIN)),
                    mean_s_per_event={c: float(tim[:, k].mean()) for k, c in enumerate(rc.T_COLS)},
                    t_total_s=round(time.time() - t0, 2),
                    code_sha256=dict(C.code_hashes(), **X.src_hashes('p2x_ht_chain.py', 'p2x_common.py', 'p2c_common.py')))
        X.save(out, dict(hits=H, hit_off=hoff, tru=T, v41=v41, timing=tim, pin=PIN, pin_off=poff), meta)
        log.info('%s', {k: meta[k] for k in ('kind', 'n_events', 'v41_pass', 'n_hits', 'n_particles_in', 'mean_s_per_event',
                                             't_total_s', 'bytes')})
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1], int(a[2]), a[3], int(a[4]))
