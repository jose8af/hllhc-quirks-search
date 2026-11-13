"""compare_raw.py -- feasibility A (Anselm): Linux re-run of Stage-1 numerics vs the tracked v1 (M3) raw outputs.

Usage (TT env, on a worker): python compare_raw.py <new_dir> <v1_dir>
For every npz present in both: per array, identical bytes? else max |a-b| and max |a-b| / max|b|.
Prints one JSON summary line (counts, worst arrays) to stdout.
"""
import json
import sys
from pathlib import Path

import numpy as np

TIMING = ('cpu', 'cpu_s', 'wall', 'wall_s', 't_cpu', 'dt')


def main():
    new, old = Path(sys.argv[1]), Path(sys.argv[2])
    names = sorted({p.name for p in new.glob('*.npz')} & {p.name for p in old.glob('*.npz')})
    n_arr = n_ident = n_shape = 0
    worst = []
    cpu_new, cpu_old = [], []
    for nm in names:
        with np.load(new / nm, allow_pickle=False) as a, np.load(old / nm, allow_pickle=False) as b:
            for k in sorted(set(a.files) & set(b.files)):
                x, y = a[k], b[k]
                if k in TIMING:
                    cpu_new.append(float(np.sum(x))); cpu_old.append(float(np.sum(y)))
                    continue
                n_arr += 1
                if x.shape != y.shape:
                    n_shape += 1
                    worst.append((float('inf'), nm, k, f'shape {x.shape} vs {y.shape}'))
                    continue
                if x.dtype.kind not in 'fc' or np.array_equal(x, y):
                    n_ident += int(np.array_equal(x, y))
                    continue
                d = float(np.nanmax(np.abs(x - y))) if x.size else 0.0
                s = float(np.nanmax(np.abs(y))) if y.size else 0.0
                worst.append((d / s if s > 0 else d, nm, k, f'max_abs {d:.3g} scale {s:.3g}'))
    worst.sort(key=lambda t: -t[0])
    rel = [w[0] for w in worst if np.isfinite(w[0])]
    print(json.dumps(dict(files_compared=len(names), arrays=n_arr, identical=n_ident, shape_mismatch=n_shape,
                          differing=len(worst), timing_arrays=len(cpu_new),
                          cpu_sum_new=float(np.sum(cpu_new)), cpu_sum_old=float(np.sum(cpu_old)),
                          cpu_ratio_median=(float(np.median(np.array(cpu_new) / np.maximum(cpu_old, 1e-9))) if cpu_new else None), median_rel_diff=(float(np.median(rel)) if rel else 0.0),
                          worst=[dict(rel=w[0], file=w[1], array=w[2], info=w[3]) for w in worst[:8]])))


if __name__ == '__main__':
    main()
