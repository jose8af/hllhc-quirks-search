"""nm_stats.py -- E2: bootstrap statistics and JSON helpers for the Stage-1 numerics.
Library.  All bootstrap errors use n_boot resamples with a fixed seed (reproducible)."""
import json
import numpy as np


def q68(a):
    a = np.abs(np.asarray(a, float)); a = a[np.isfinite(a)]
    return float(np.quantile(a, 0.68)) if len(a) else np.nan


def boot(stat, *arrays, n_boot=2000, seed=12345, paired=True):
    """Bootstrap a statistic of one or several (paired) arrays. Returns (value, std error, 16%, 84%)."""
    rng = np.random.default_rng(seed)
    arrs = [np.asarray(a, float) for a in arrays]
    n = len(arrs[0])
    val = stat(*arrs)
    if n < 2:
        return float(val), np.nan, np.nan, np.nan
    out = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        out[i] = stat(*[a[idx] for a in arrs]) if paired else stat(*[a[rng.integers(0, len(a), len(a))] for a in arrs])
    out = out[np.isfinite(out)]
    return float(val), float(np.std(out)), float(np.quantile(out, 0.16)), float(np.quantile(out, 0.84))


def med(a):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    return float(np.median(a)) if len(a) else np.nan


def local_exponent(x1, x2, y1, y2, stat=med):
    """d ln stat(y) / d ln x between two grid points with paired events (same events at both points)."""
    return np.log(stat(y2) / stat(y1)) / np.log(x2 / x1)


def summarize(a, n_boot=2000, seed=1):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    if len(a) == 0:
        return dict(n=0)
    m, me, _, _ = boot(med, a, n_boot=n_boot, seed=seed)
    q, qe, _, _ = boot(q68, a, n_boot=n_boot, seed=seed + 1)
    return dict(n=int(len(a)), median=m, median_err=me, q68=q, q68_err=qe, p16=float(np.quantile(a, 0.16)),
                p84=float(np.quantile(a, 0.84)), mean=float(np.mean(a)), mean_err=float(np.std(a) / np.sqrt(len(a))))


class NpEnc(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return super().default(o)


def dump(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f, cls=NpEnc, indent=1, allow_nan=True)
