"""pyhf timing benchmark for item T1 (Phase-1 feasibility, session Boris). TOY WORKSPACE ONLY: no study numbers.

Workspace shape (what T1 will need, not its content): 3 counting categories, 25 background terms in total (9+8+8),
each with a Poisson/Gamma auxiliary constraint (pyhf `shapesys`, tau = n_MC) on a small or zero simulated count,
5 correlated normalisation nuisances shared across terms, one signal strength `mu`.

    python bench_pyhf.py --part fit  --out fit.json    # 1 MLE fit, 1 asymptotic CLs point, 20-point UL scan
    python bench_pyhf.py --part toys --out toys.json   # 1000 toys for one point (toy-based CLs)

Per step: CPU s (process_time), wall s, and max RSS (getrusage) after the step.
"""
import os

for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(v, "1")  # one core per job (Argo request cpu 1)

import argparse  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import platform  # noqa: E402
import resource  # noqa: E402
import socket  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402
import pyhf  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("bench_pyhf")

SEED = 20261113
CATS = {"cat_a": 9, "cat_b": 8, "cat_c": 8}
NUIS = {"lumi": 0.02, "eff": 0.05, "xsec": 0.10, "pu": 0.08, "closure": 0.30}


def toy_workspace():
    """Deterministic toy: MC counts n in {0,1,2,3,5,8}, per-event weights 0.01-0.3."""
    rng = np.random.default_rng(SEED)
    channels, observations = [], []
    k = 0
    for cat, nterms in CATS.items():
        samples = []
        tot = 0.0
        for t in range(nterms):
            n = int(rng.choice([0, 0, 1, 1, 2, 3, 5, 8]))
            w = float(rng.uniform(0.01, 0.3))
            # toy convention only: a zero count is represented by one event's weight with 100% (tau = 1) constraint
            nom, tau = (w * n, n) if n > 0 else (w, 1)
            mods = [{"name": f"mcstat_{cat}_{t}", "type": "shapesys", "data": [nom / np.sqrt(tau)]}]
            for j, (nu, s) in enumerate(NUIS.items()):
                if nu in ("lumi", "eff") or (k + j) % 3 == 0:
                    mods.append({"name": nu, "type": "normsys", "data": {"hi": 1 + s, "lo": 1 - s}})
            samples.append({"name": f"bkg_{t}", "data": [nom], "modifiers": mods})
            tot += nom
            k += 1
        samples.append({"name": "signal", "data": [1.5],
                        "modifiers": [{"name": "mu", "type": "normfactor", "data": None},
                                      {"name": "lumi", "type": "normsys", "data": {"hi": 1.02, "lo": 0.98}}]})
        channels.append({"name": cat, "samples": samples})
        observations.append({"name": cat, "data": [float(round(tot))]})
    spec = {"version": "1.0.0", "channels": channels, "observations": observations,
            "measurements": [{"name": "toy", "config": {"poi": "mu", "parameters": []}}]}
    return pyhf.Workspace(spec)


def timed(name, fn, results):
    c0, w0 = time.process_time(), time.time()
    out = fn()
    c1, w1 = time.process_time(), time.time()
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    results[name] = {"cpu_s": round(c1 - c0, 3), "wall_s": round(w1 - w0, 3), "max_rss_mb_after": round(rss, 1)}
    log.info("%-22s cpu %8.3f s  wall %8.3f s  maxRSS %7.1f MB", name, c1 - c0, w1 - w0, rss)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", choices=("fit", "toys"), required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ntoys", type=int, default=1000)
    a = ap.parse_args()
    pyhf.set_backend("numpy", "scipy")
    np.random.seed(SEED)
    ws = toy_workspace()
    model = ws.model()
    data = ws.data(model)
    res = {"part": a.part, "host": socket.gethostname(), "python": platform.python_version(),
           "pyhf": pyhf.__version__, "numpy": np.__version__, "n_parameters": model.config.npars,
           "n_shapesys": sum(1 for m in model.config.modifiers if m[1] == "shapesys"),
           "n_channels": len(model.config.channels), "n_samples": len(model.config.samples),
           "toy": "TOY WORKSPACE, not study numbers", "steps": {}}
    st = res["steps"]
    if a.part == "fit":
        bf = timed("mle_fit", lambda: pyhf.infer.mle.fit(data, model), st)
        res["bestfit_mu"] = float(bf[model.config.poi_index])
        cls = timed("asymptotic_cls_mu1", lambda: pyhf.infer.hypotest(1.0, data, model, test_stat="qtilde",
                                                                         return_expected_set=True), st)
        res["cls_obs_mu1"] = float(cls[0])
        scan = np.linspace(0.0, 6.0, 20)
        ul = timed("ul_scan_20pt", lambda: pyhf.infer.intervals.upper_limits.upper_limit(data, model, scan=scan,
                                                                                         level=0.05), st)
        res["ul_obs"] = float(ul[0])
        res["ul_exp"] = [float(x) for x in ul[1]]
        pyhf.set_backend("numpy", pyhf.optimize.minuit_optimizer(verbose=0))
        timed("mle_fit_minuit", lambda: pyhf.infer.mle.fit(data, model), st)
    else:
        cls = timed(f"toys_{a.ntoys}_mu1", lambda: pyhf.infer.hypotest(
            1.0, data, model, test_stat="qtilde", calctype="toybased", ntoys=a.ntoys, track_progress=False), st)
        res["cls_obs_mu1_toys"] = float(cls)
        res["ntoys_per_hypothesis"] = a.ntoys
    ru = resource.getrusage(resource.RUSAGE_SELF)
    res["total_cpu_s"] = round(ru.ru_utime + ru.ru_stime, 3)
    res["max_rss_mb"] = round(ru.ru_maxrss / 1024, 1)
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
    log.info("wrote %s", a.out)


if __name__ == "__main__":
    main()
