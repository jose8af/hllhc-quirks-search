"""merge_chunks.py -- merge the chunk npz files of one (sample, mass) point written by convert_hepmc.py.
Weights: each chunk has w [fb/event] with sum = sigma_chunk; the merged weight is w * N_LHE,chunk / N_LHE,total so that
sum(w) = N_LHE-weighted mean sigma.  Usage: python merge_chunks.py <out.npz> <chunk1.npz> [chunk2.npz ...]
An already merged file can be given as a 'chunk' (top-ups, produce.py --topup): its per-chunk metadata arrays are flattened."""
import sys
import numpy as np

out, files = sys.argv[1], sys.argv[2:]
cs = [dict(np.load(f, allow_pickle=False)) for f in files]
names = cs[0]['wvar_names']
for c in cs[1:]:
    assert list(c['wvar_names']) == list(names), 'weight names differ between chunks'
ntot = sum(int(c['nlhe']) for c in cs)
per_event = [k for k, v in cs[0].items() if hasattr(v, 'shape') and v.ndim >= 1 and len(v) == len(cs[0]['w']) and k != 'wvar_names']
m = {}
for k in per_event:
    parts = []
    for c in cs:
        v = c[k]
        if k in ('w', 'wvar'):
            v = v * (int(c['nlhe']) / ntot)
        parts.append(v)
    m[k] = np.concatenate(parts)
m['wvar_names'] = names
for k in ('mq', 'spin', 'merging_nominal', 'n_ic_included'):
    m[k] = cs[0][k]
m['nlhe'] = ntot
m['n_in_file'] = sum(int(c['n_in_file']) for c in cs)
m['sigma_lhe_fb'] = sum(float(c['sigma_lhe_fb']) * int(c['nlhe']) for c in cs) / ntot
flat = lambda c, k, alt: list(np.atleast_1d(c[k])) if k in c else [alt(c)]
m['sigma_lhe_fb_chunks'] = np.array([float(x) for c in cs for x in flat(c, 'sigma_lhe_fb_chunks', lambda c: c['sigma_lhe_fb'])])
m['source'] = np.array([str(x) for c in cs for x in np.atleast_1d(c['source'])])
m['tag'] = np.array([str(x) for c in cs for x in np.atleast_1d(c['tag'])])
np.savez_compressed(out, **m)
print(f'merged {len(cs)} chunks -> {out}: {len(m["w"])} events, N_LHE={ntot}, sigma(nominal)={m["w"].sum():.5g} fb (N_IC=1)')
